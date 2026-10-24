# Quality

What this repository measures, where each measure lives, and how to read it.

| Measure | Where it lives | What it tells you |
|---|---|---|
| Test suite | `tests/run` | This repository's gates, then toothpaste-kit's |
| Gates and their selftest | `scripts/gates.sh --selftest` | Whether attribution, JSON, executable bits and the branch rules hold, after each gate has caught a planted positive |
| Branch-name rule | `scripts/check-branch-name --selftest`, `scripts/check-branch-guard` | Whether the rule and the agent guard behave as their cases say |
| CI matrix | `.github/workflows/ci.yml` | Whether the suite passes on Linux and macOS |
| Nightly | `.github/workflows/nightly.yml` | Whether the suite still passes with no change pushed |
| Code scanning | CodeQL default setup, Python and Actions | Known vulnerability patterns in scripts and workflows |
| PR acceptance | `docs/metrics.md` | Merged against closed unmerged, and recorded reviews |
| Review rubric | `docs/review-rubric.md` | What a reviewer checked |
| ACMM level | Hive's ACMM evaluation | Which agent-readiness criteria the repository meets |

## How to read them

Run `./tests/run`. Its last lines are toothpaste-kit's gate count and `gates: all passed`. A planted positive the gates missed stops the run before the real gates run, and the run is not to be trusted.

Required checks on `main` are listed in `.github/rulesets/main.json`. A workflow that is not listed there reports but blocks nothing.

## What these leave out

Prose quality, design quality, and whether a document's claims are true. Those are a reader's judgment.
