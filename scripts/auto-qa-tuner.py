#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2026 Aidan Naveja
#
# SPDX-License-Identifier: Apache-2.0

"""Propose job timeouts from the repository's own run history.

A timeout is the one numeric limit in this repository's QA that has no rule
behind its value: it was a guess when it was written. This reads how long each
workflow's runs actually took and how they ended, and proposes a timeout for
each job in `.github/auto-qa-tuning.json`:

1. A job with no `timeout-minutes` runs under GitHub's 360 minute default, so
   it always gets a proposal.
2. Otherwise the proposal is the larger of p95 times `p95_factor` and the
   longest run times `max_factor`, rounded up to a whole minute, never below
   `floor_minutes`. It is reported as a change only when it differs from the
   current value by `change_ratio` or more either way, so the value does not
   move with every week's noise.
3. A failed or cancelled run that lasted `timeout_ratio` of the current
   timeout or longer is read as a timeout, and the proposal is at least twice
   the current value.

It proposes and never edits. A person changes the workflow and the record in
the JSON, by pull request. The rules the gates enforce are absolute, not
thresholds, and nothing here reads or proposes anything about them; the gates
workflow's jobs get timeouts like any other job. A count of failed runs is
reported in each job's row and changes no value.

Coverage, stated because a check that does not state its coverage is not a
check: a run's duration is from its start to its last update, which bounds
each of its jobs from above, so a proposal for one job of several is
conservative. Queue time before a run starts is not counted. A workflow with
fewer than `min_runs` runs in the history gets no proposal beyond rule 1.
The workflow file is read for `timeout-minutes` by indentation, not by a YAML
parser, and only at the job level. A job the file does not hold, or a timeout
that is not a plain whole number above 0, gets a row saying so and no
proposal, never a guess. So does a file of more than one YAML document, a
job that takes keys from a merge key (`<<:`), a key in the job that is explicit
(`?`), tagged (`!`), an anchor or alias, or double-quoted with an escape (`\\`),
a job named twice, and a timeout set twice, since this reader cannot follow
them. Which YAML version GitHub reads is not checked: a number
with a leading 0 (`010`) is read as decimal, as YAML 1.2 reads it.

Usage:
  scripts/auto-qa-tuner.py RUNS.json   RUNS.json is the runs of each listed
      workflow, joined into one list, in bash:
      set -eo pipefail
      for w in $(scripts/auto-qa-tuner.py --workflows); do
        gh run list -w "$w" -L 100 --json workflowName,conclusion,startedAt,updatedAt
      done | jq -s add
  scripts/auto-qa-tuner.py --workflows   prints each listed workflow file name
  scripts/auto-qa-tuner.py --selftest
Prints a Markdown report. Exits 0 whether or not it proposes anything, 2 if
an input is missing or malformed.
"""

import contextlib
import datetime
import io
import json
import math
import os
import re
import sys
import tempfile

CONFIG = ".github/auto-qa-tuning.json"
GITHUB_DEFAULT = 360


def parse_time(s):
    return datetime.datetime.fromisoformat(s.replace("Z", "+00:00"))


class Unread(Exception):
    """The workflow file does not say plainly what the job's timeout is."""


def strip_comment(line):
    m = re.search(r"\s#", line)   # one pass: \s+#.*$ backtracks quadratically on a long run of spaces
    return (line[:m.start()] if m else line).rstrip()


def mapping_key(text):
    m = re.match(r"""(['"]?)([^'":]+)\1:$""", text)
    return m.group(2) if m else None


def job_timeout(path, job):
    """The job's timeout-minutes, or None when the job sets none.

    Raises Unread when the file holds no such job, when its timeout is not a
    plain whole number above 0 (an expression, say), or when the file or the
    job is a shape this reader cannot follow, since a guess there would be wrong.
    """
    lines = [strip_comment(l) for l in open(path, encoding="utf-8").read().splitlines()]
    lines = [l for l in lines if l.strip() and not l.lstrip().startswith("#")]
    if any(re.match(r"---(\s|$)", l) for l in lines[1:]) or "..." in lines[:-1]:
        raise Unread("the file holds more than one YAML document")
    top = min((len(l) - len(l.lstrip()) for l in lines), default=0)
    in_jobs = False
    child = None      # indent of the job keys under jobs:
    body = None       # indent of this job's own keys
    found = False
    seen = False
    timeout = None
    for line in lines:
        indent = len(line) - len(line.lstrip())
        text = line.strip()
        if indent == top:
            in_jobs = mapping_key(text) == "jobs"
            continue
        if not in_jobs:
            continue
        if child is None:
            child = indent
        if indent == child:
            found = mapping_key(text) == job
            if found and seen:
                raise Unread("the job %r is named twice" % job)
            seen = seen or found
            continue
        if not found:
            continue
        if body is None:
            body = indent
        if indent != body:
            continue
        if text.startswith("<<"):
            raise Unread("the job takes keys from a merge key")
        if text[:1] in ("?", "!", "&", "*"):
            raise Unread("the job has a key this reader cannot follow: %r" % text)
        q = re.match(r'"([^"]*)', text)
        if q and "\\" in q.group(1):
            raise Unread("the job has a quoted key with an escape: %r" % text)
        m = re.match(r"""(['"]?)timeout-minutes\1\s*:\s*(.*)$""", text)
        if m:
            m2 = re.match(r"""(['"]?)(\d+)\1$""", m.group(2))
            if not m2 or int(m2.group(2)) == 0:
                raise Unread("timeout-minutes is %r, not a plain number above 0" % m.group(2))
            if timeout is not None:
                raise Unread("timeout-minutes is set twice")
            timeout = int(m2.group(2))
    if not seen:
        raise Unread("no job %r in the file" % job)
    return timeout


def check_runs(runs):
    """Raise ValueError on a history this cannot read, naming the first fault."""
    if not isinstance(runs, list):
        raise ValueError("the history is not a list of runs")
    for i, r in enumerate(runs):
        if not isinstance(r, dict):
            raise ValueError("run %d is not an object" % i)
        if not r.get("startedAt"):
            continue
        if not isinstance(r.get("updatedAt"), str) or not isinstance(r["startedAt"], str):
            raise ValueError("run %d has a start and no readable end" % i)
        try:
            minutes = (parse_time(r["updatedAt"]) - parse_time(r["startedAt"])).total_seconds()
        except ValueError:
            raise ValueError("run %d has a timestamp that is not ISO 8601" % i)
        if minutes < 0:
            raise ValueError("run %d ends before it starts" % i)


def durations(runs, workflow):
    out = []
    for r in runs:
        if r.get("workflowName") != workflow or not r.get("startedAt"):
            continue
        minutes = (parse_time(r["updatedAt"]) - parse_time(r["startedAt"])).total_seconds() / 60
        out.append((minutes, r.get("conclusion") or ""))
    return out


def propose(policy, current, runs):
    """Return (proposed or None, reason)."""
    if not runs:
        if current is None:
            return policy["floor_minutes"], "no timeout set and no runs; the floor"
        return None, "no runs"
    ds = sorted(d for d, _ in runs)
    p95 = ds[int(0.95 * (len(ds) - 1))]
    longest = ds[-1]
    value = max(policy["floor_minutes"],
                math.ceil(max(p95 * policy["p95_factor"], longest * policy["max_factor"])))
    if current is not None:
        timed_out = [d for d, c in runs
                     if c in ("failure", "cancelled") and d >= policy["timeout_ratio"] * current]
        if timed_out:
            return max(value, 2 * current), "%d run(s) ended at the timeout" % len(timed_out)
    if current is None:
        return value, "no timeout set, so GitHub's %d minute default applies" % GITHUB_DEFAULT
    if len(runs) < policy["min_runs"]:
        return None, "%d runs, under min_runs" % len(runs)
    ratio = max(value, current) / min(value, current)
    if ratio >= policy["change_ratio"]:
        return value, "current is %.1fx the evidence" % ratio if current > value else \
            "evidence is %.1fx the current" % ratio
    return None, "within change_ratio"


def report(config, runs, root="."):
    policy = config["policy"]
    rows = []
    for j in config["jobs"]:
        rs = durations(runs, j["workflow"])
        try:
            current = job_timeout(os.path.join(root, j["file"]), j["job"])
            value, reason = propose(policy, current, rs)
        except OSError:
            current, value, reason = None, None, "workflow file missing"
        except Unread as e:
            current, value, reason = "unread", None, "not proposed: %s" % e
        fails = sum(1 for _, c in rs if c == "failure")
        longest = "%.1f" % max(d for d, _ in rs) if rs else "-"
        rows.append((j["file"], j["job"], len(rs), fails, longest,
                     "none" if current is None else str(current),
                     "-" if value is None else str(value), reason))
    out = ["## Auto-QA timeout proposals", "",
           "Proposals only. Accept one by editing the workflow and `%s` in a pull request." % CONFIG, "",
           "| File | Job | Runs | Failed | Longest (min) | Timeout now | Proposed | Why |",
           "|---|---|---|---|---|---|---|---|"]
    out += ["| `%s` | %s | %d | %d | %s | %s | %s | %s |" % r for r in rows]
    return "\n".join(out) + "\n", sum(1 for r in rows if r[6] != "-")


def workflows(config):
    """The workflow file names the config lists, once each, for `gh run list -w`."""
    return sorted({os.path.basename(j["file"]) for j in config["jobs"]})


def run(runs_path, root="."):
    try:
        config = json.load(open(os.path.join(root, CONFIG), encoding="utf-8"))
        runs = json.load(open(runs_path, encoding="utf-8"))
        check_runs(runs)
    except (OSError, ValueError) as e:
        print("auto-qa-tuner: %s" % e, file=sys.stderr)
        return 2
    text, _ = report(config, runs, root)
    sys.stdout.write(text)
    return 0


def selftest():
    failures = 0

    def check(name, got, want):
        nonlocal failures
        ok = got == want
        failures += not ok
        print("%s %s%s" % ("PASS" if ok else "FAIL", name, "" if ok else ": got %r, want %r" % (got, want)))

    policy = {"min_runs": 3, "floor_minutes": 5, "p95_factor": 4, "max_factor": 1.5,
              "change_ratio": 2, "timeout_ratio": 0.9}
    with tempfile.TemporaryDirectory() as tmp:
        wf = os.path.join(tmp, "w.yml")
        with open(wf, "w", encoding="utf-8") as f:
            f.write("on:\n  push:\njobs:\n  a:\n    timeout-minutes: 15\n    steps:\n"
                    "      - run: x\n        timeout-minutes: 99\n  b:\n    steps:\n      - run: y\n")
        check("job timeout read", job_timeout(wf, "a"), 15)
        check("no job timeout is None", job_timeout(wf, "b"), None)

        def reads(text, job):
            with open(wf, "w", encoding="utf-8") as f:
                f.write(text)
            try:
                return job_timeout(wf, job)
            except Unread:
                return "unread"

        check("missing job is unread", reads("jobs:\n  a:\n    steps: []\n", "c"), "unread")
        check("step timeout not read as the job's",
              reads("jobs:\n  a:\n    steps:\n    - run: x\n      timeout-minutes: 99\n"
                    "    - timeout-minutes: 98\n", "a"), None)
        check("next job's timeout not read",
              reads("jobs:\n  a:\n    steps: []\n  b:\n    timeout-minutes: 9\n", "a"), None)
        check("job name elsewhere in the file not read",
              reads("on:\n  a:\n    timeout-minutes: 3\njobs:\n  a:\n    steps: []\n", "a"), None)
        check("nested key named like the job not read",
              reads("jobs:\n  b:\n    services:\n      a:\n        timeout-minutes: 3\n", "a"), "unread")
        check("comments, quotes and 4-space indent read",
              reads("jobs:  # all\n    'a':  # the job\n        timeout-minutes: '7'  # min\n", "a"), 7)
        check("expression timeout is unread",
              reads("jobs:\n  a:\n    timeout-minutes: ${{ 7 }}\n", "a"), "unread")
        check("a timeout of 0 is unread", reads("jobs:\n  a:\n    timeout-minutes: 0\n", "a"), "unread")
        check("a second document is unread",
              reads("jobs:\n  b:\n    steps: []\n---\njobs:\n  a:\n    timeout-minutes: 7\n", "a"), "unread")
        check("a leading document marker is read",
              reads("---\njobs:\n  a:\n    timeout-minutes: 7\n", "a"), 7)
        check("a merge key in the job is unread",
              reads("x: &d\n  timeout-minutes: 7\njobs:\n  a:\n    <<: *d\n    runs-on: y\n", "a"), "unread")
        check("a double-quoted timeout key is read",
              reads("jobs:\n  a:\n    \"timeout-minutes\": 9\n", "a"), 9)
        check("a spaced timeout key is read",
              reads("jobs:\n  a:\n    timeout-minutes : 9\n", "a"), 9)
        check("a tagged merge key is unread",
              reads("x: &d\n  timeout-minutes: 9\njobs:\n  a:\n    !!merge <<: *d\n", "a"), "unread")
        check("an explicit key is unread",
              reads("jobs:\n  a:\n    ? timeout-minutes\n    : 9\n", "a"), "unread")
        check("an anchored key is unread",
              reads("jobs:\n  a:\n    &k timeout-minutes: 9\n", "a"), "unread")
        check("an alias key is unread",
              reads("k: &k timeout-minutes\njobs:\n  a:\n    *k : 9\n", "a"), "unread")
        check("a single-quoted timeout key is read",
              reads("jobs:\n  a:\n    'timeout-minutes': 9\n", "a"), 9)
        check("a key with one stray quote is not the timeout",
              reads("jobs:\n  a:\n    timeout-minutes\": 9\n", "a"), None)
        check("a double-quoted key with an escape is unread",
              reads("jobs:\n  a:\n    \"timeout\\x2dminutes\": 9\n", "a"), "unread")
        check("a job named twice is unread",
              reads("jobs:\n  a:\n    timeout-minutes: 7\n  b:\n    steps: []\n  a:\n    timeout-minutes: 9\n", "a"), "unread")
        check("a job named twice, the first with no timeout, is unread",
              reads("jobs:\n  a:\n    steps: []\n  a:\n    timeout-minutes: 9\n", "a"), "unread")
        check("a timeout set twice is unread",
              reads("jobs:\n  a:\n    timeout-minutes: 7\n    timeout-minutes: 9\n", "a"), "unread")
        check("a second document after an end marker is unread",
              reads("jobs:\n  b:\n    steps: []\n...\njobs:\n  a:\n    timeout-minutes: 9\n", "a"), "unread")
        check("an end marker on the last line is read",
              reads("jobs:\n  a:\n    timeout-minutes: 7\n...\n", "a"), 7)
        check("a whole file indented is read",
              reads("  jobs:\n    a:\n      timeout-minutes: 7\n", "a"), 7)
        check("a key starting with jobs is not jobs",
              reads("jobs2:\n  a:\n    timeout-minutes: 3\njobs:\n  a:\n    steps: []\n", "a"), None)

        # The whole path, from config and history files to the report.
        os.makedirs(os.path.join(tmp, ".github"))
        with open(wf, "w", encoding="utf-8") as f:
            f.write("jobs:\n  a:\n    timeout-minutes: 15\n")
        config = {"policy": policy, "jobs": [
            {"workflow": "w", "file": "w.yml", "job": "a"},
            {"workflow": "w", "file": "w.yml", "job": "chek"},
            {"workflow": "v", "file": ".github/workflows/w.yml", "job": "a"}]}
        with open(os.path.join(tmp, CONFIG), "w", encoding="utf-8") as f:
            json.dump(config, f)
        check("--workflows lists each file name once", workflows(config), ["w.yml"])
        hist = os.path.join(tmp, "runs.json")

        def run_on(history):
            with open(hist, "w", encoding="utf-8") as f:
                json.dump(history, f)
            out = io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
                code = run(hist, tmp)
            return code, out.getvalue()

        quick_runs = [{"workflowName": "w", "conclusion": "success",
                       "startedAt": "2026-10-22T10:00:00Z", "updatedAt": "2026-10-22T10:00:24Z"}] * 5
        code, text = run_on(quick_runs)
        check("run exits 0 on a clean history", code, 0)
        check("run proposes the floor for 15 against 0.4 min runs",
              "| `w.yml` | a | 5 | 0 | 0.4 | 15 | 5 |" in text, True)
        check("a job the file does not hold shows unread, no proposal",
              "| `w.yml` | chek | 5 | 0 | 0.4 | unread | - | not proposed:" in text, True)
        check("run exits 2 on a malformed history", run_on([dict(quick_runs[0], updatedAt=None)])[0], 2)

    check("no timeout and no runs is the floor", propose(policy, None, [])[0], 5)
    check("max_factor can decide", propose(policy, None, [(1.0, "success")] * 2 + [(20.0, "success")])[0], 30)
    check("change_ratio is inclusive", propose(policy, 10, [(0.4, "success")] * 5)[0], 5)
    edge = [(4.0, "success")] * 2
    check("timeout_ratio is inclusive", propose(policy, 10, [(9.0, "failure")] + edge)[0], 20)
    check("a cancelled run at the timeout doubles it", propose(policy, 10, [(9.5, "cancelled")] + edge)[0], 20)
    check("a success at the timeout does not", propose(policy, 10, [(9.5, "success")] + edge)[0], None)

    quick = [(0.4, "success")] * 5
    check("no timeout set proposes", propose(policy, None, quick)[0], 5)
    check("15 against 0.4 min runs proposes the floor", propose(policy, 15, quick)[0], 5)
    check("within change_ratio holds", propose(policy, 8, quick)[0], None)
    check("too few runs holds", propose(policy, 15, quick[:2])[0], None)
    slow = [(9.5, "failure"), (4.0, "success"), (4.0, "success")]
    check("a run at the timeout doubles it", propose(policy, 10, slow)[0], 20)
    check("long run raises", propose(policy, 5, [(6.0, "success")] * 3)[0], 24)

    runs = [{"workflowName": "w", "conclusion": "success",
             "startedAt": "2026-10-22T10:00:00Z", "updatedAt": "2026-10-22T10:00:30Z"}] * 4
    check("durations from timestamps", durations(runs, "w")[0][0], 0.5)
    queued = [{"workflowName": "w", "startedAt": None, "updatedAt": None}]
    check("a run not started is skipped", durations(queued + runs, "w"), [(0.5, "success")] * 4)

    def malformed(history):
        try:
            check_runs(history)
            return False
        except ValueError:
            return True

    one = runs[0]
    check("history as an object is malformed", malformed({}), True)
    check("a run as a number is malformed", malformed([1]), True)
    check("a start with no end is malformed", malformed([dict(one, updatedAt=None)]), True)
    check("a bad timestamp is malformed", malformed([dict(one, startedAt="yesterday")]), True)
    check("an end before the start is malformed",
          malformed([dict(one, startedAt="2026-10-22T10:01:00Z")]), True)
    check("a clean history is not", malformed(queued + runs), False)
    print("FAILS: %d" % failures)
    return 1 if failures else 0


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        sys.exit(selftest())
    if sys.argv[1:] == ["--workflows"]:
        print("\n".join(workflows(json.load(open(CONFIG, encoding="utf-8")))))
        sys.exit(0)
    if len(sys.argv) != 2:
        print(__doc__.split("Usage:")[1], file=sys.stderr)
        sys.exit(2)
    sys.exit(run(sys.argv[1]))
