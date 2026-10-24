#!/usr/bin/env sh

# SPDX-FileCopyrightText: 2026 Aidan Naveja
#
# SPDX-License-Identifier: Apache-2.0

# Compliance checks that need a tool from outside this repository.
#
# scripts/gates.sh needs nothing but sh and python3, so a fresh clone can run
# every gate at once. Checks that depend on an installed linter live here
# instead, which keeps the gates runnable everywhere and gives each external
# tool one place to be named, pinned and explained.
#
# Coverage: REUSE compliance via `reuse lint`, which checks that every file
# declares a copyright and a licence and that each licence named has its text
# in LICENSES/. It does NOT check that a declaration is true: a passing lint is
# not an ownership clearance.
#
# A tool that is not installed is reported as SKIP, not checked, and never
# counted as a pass. CI runs with --require, so there a missing tool fails.
#
# Usage: scripts/compliance.sh                       run every check
#        scripts/compliance.sh --selftest            show each check can fire, then run them
#        scripts/compliance.sh --require [--selftest] a missing tool fails
#
# Install the linter: pipx install reuse==6.2.0 (the version CI pins in
# .github/workflows/compliance.yml).

cd "$(dirname "$0")/.." || exit 1

selftest=0
require=0
for arg in "$@"; do
  case "$arg" in
    --selftest) selftest=1 ;;
    --require)  require=1 ;;
    *) printf 'compliance: unknown argument %s\n' "$arg" >&2; exit 2 ;;
  esac
done

fail=0
pass_n=0
skip_n=0
total=0

check_start() { printf '\n== %s ==\n' "$1"; total=$((total + 1)); }
check_ok()    { printf 'PASS  %s\n' "$1"; pass_n=$((pass_n + 1)); }
check_bad()   { printf 'FAIL  %s\n' "$1"; fail=1; }
check_skip()  {
  if [ "$require" -eq 1 ]; then
    printf 'FAIL  %s: %s is not installed, and --require is set\n' "$1" "$2"; fail=1
  else
    printf 'SKIP  %s: %s is not installed, so this is NOT checked (%s)\n' "$1" "$2" "$3"
    skip_n=$((skip_n + 1))
  fi
}

# The tracked and new files, copied to a scratch root, so a plant never
# touches the working tree. Ignored files are left out, as reuse would.
copy_tree() {
  git ls-files -z --cached --others --exclude-standard \
    | tar --null -T - -cf - | tar -xf - -C "$1"
}

check_reuse() {
  check_start "REUSE compliance"
  if ! command -v reuse >/dev/null 2>&1; then
    check_skip "REUSE compliance" reuse "pipx install reuse==6.2.0"
    return
  fi
  if [ "$selftest" -eq 1 ]; then
    scratch=$(mktemp -d) || { check_bad "REUSE compliance: no scratch directory"; return; }
    copy_tree "$scratch" || { check_bad "REUSE compliance: copy failed"; return; }
    if ! reuse --root "$scratch" lint >/dev/null 2>&1; then
      printf 'PLANT FAIL  reuse rejected the clean copy, so a non-zero on the plant proves nothing\n'
      check_bad "REUSE compliance"; return
    fi
    printf 'no declaration here\n' > "$scratch/planted-undeclared.txt"
    if reuse --root "$scratch" lint >/dev/null 2>&1; then
      printf 'PLANT FAIL  reuse passed a file with no declaration\n'
      check_bad "REUSE compliance"; return
    fi
    printf 'PLANT ok    reuse rejects a file with no declaration and accepts the clean copy\n'
  fi
  if reuse lint; then
    check_ok "REUSE compliance"
  else
    check_bad "REUSE compliance"
  fi
}

check_reuse

printf '\n%s of %s checks passed, %s not checked\n' "$pass_n" "$total" "$skip_n"
if [ "$fail" -ne 0 ]; then
  printf 'compliance: FAILED\n'; exit 1
fi
if [ "$skip_n" -ne 0 ]; then
  printf 'compliance: incomplete, %s check(s) not run\n' "$skip_n"; exit 0
fi
printf 'compliance: all passed\n'
