#!/bin/sh
# The mechanical checks for chocolate-factory's own files. toothpaste-kit/
# has its own gates, run by tests/run.
#
#   scripts/gates.sh             run the gates
#   scripts/gates.sh --selftest  first prove each gate fails on a planted
#                                positive, then run the gates
#
# GATES_RANGE, when set (CI sets it), is a commit range whose messages the
# attribution gate checks, for example base..head.

cd "$(dirname "$0")/.." || exit 1

failed=0
fail() { echo "FAIL: $*" >&2; failed=1; }

# Gate 1: no AI attribution in a commit message. Provenance lines
# (Assisted-by, Agent-Effort) are allowed; AGENTS.md rule 2.
attribution_pattern='^Co-Authored-By:.*(Claude|Anthropic|Copilot|GPT|Gemini|Cursor)|Generated with .*(Claude|Copilot)|^Claude-Session:'

check_message() {
    grep -inE "$attribution_pattern" "$1"
}

gate_attribution() {
    [ -n "${GATES_RANGE:-}" ] || return 0
    tmp=$(mktemp)
    for c in $(git rev-list --no-merges "$GATES_RANGE"); do
        git log -1 --format=%B "$c" > "$tmp"
        if hits=$(check_message "$tmp"); then
            fail "attribution in $c: $hits"
        fi
    done
    rm -f "$tmp"
}

# Gate 2: every tracked JSON file outside the subtree parses.
check_json() {
    python3 -c 'import json, sys; json.load(open(sys.argv[1]))' "$1" 2>/dev/null
}

gate_json() {
    for f in $(git ls-files '*.json' | grep -v '^toothpaste-kit/'); do
        check_json "$f" || fail "JSON does not parse: $f"
    done
}

# Gate 3: scripts and hooks are executable, or git will not run them.
gate_exec() {
    for f in $(git ls-files 'scripts/*' '.githooks/*' tests/run); do
        mode=$(git ls-files -s "$f" | cut -d' ' -f1)
        [ "$mode" = 100755 ] || fail "not executable in git: $f"
    done
}

# Gate 4: the branch-name rule and the agent guard pass their own tests.
gate_branch_rules() {
    scripts/check-branch-name --selftest >/dev/null || fail "check-branch-name --selftest"
    scripts/check-branch-guard >/dev/null || fail "check-branch-guard"
}

selftest() {
    dir=$(mktemp -d)
    printf 'Subject\n\nCo-Authored-By: Claude <noreply@anthropic.com>\n' > "$dir/bad"
    printf 'Subject\n\nAssisted-by: claude-opus-5-5 via claude-code/2.1.308\nAgent-Effort: low\n' > "$dir/good"
    printf '{"a": 1,}\n' > "$dir/bad.json"
    printf '{"a": 1}\n' > "$dir/good.json"

    ok=1
    check_message "$dir/bad" >/dev/null || { echo "selftest: attribution gate missed a planted line" >&2; ok=0; }
    check_message "$dir/good" >/dev/null && { echo "selftest: attribution gate flagged provenance lines" >&2; ok=0; }
    check_json "$dir/bad.json" && { echo "selftest: JSON gate passed invalid JSON" >&2; ok=0; }
    check_json "$dir/good.json" || { echo "selftest: JSON gate failed valid JSON" >&2; ok=0; }
    rm -rf "$dir"
    [ "$ok" = 1 ] || exit 1
    echo "gates selftest: each gate caught its planted positive"
}

[ "${1:-}" = --selftest ] && selftest

gate_attribution
gate_json
gate_exec
gate_branch_rules

[ "$failed" = 0 ] || exit 1
echo "gates: all pass"
