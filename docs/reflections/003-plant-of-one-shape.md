# 003: a planted positive of one shape

**Row**: `docs/security-posture.md`, row 4.7, "Second party check on the markdown gate", at commit
`451f63ea78baaaa33a1e6ce14d45f0ad0a0bf068`.

**Records**: `markdownlint-cli2` runs the real tool against the same rule IDs as
`scripts/mdlint.py`. On its first run, 2026-09-18, it found `MD034` at `CODE_OF_CONDUCT.md` line 52
where `mdlint.py` reported the file clean. The rule fired on a whitespace delimited bare URL and not
on one inside parentheses, and its only planted positive used the delimited shape, so the selftest
proved the rule could fire rather than that it covered its field. `MD034` now carries two
differently shaped plants.

**Lesson**: A planted positive proves that a rule can fire, not that the rule covers its field.

**Supersedes**: none.

**Filed**: 2026-10-21.

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
