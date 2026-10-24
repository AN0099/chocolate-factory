# 001: the DOI's date

**Row**: `docs/security-posture.md`, row 3.2b, "The DOI's date matches neither document", at commit
`451f63ea78baaaa33a1e6ce14d45f0ad0a0bf068`.

**Records**: The row previously predicted that the DOI would inherit `2026-09-18` from the tagged
`CITATION.cff`, and that prediction was wrong. Zenodo records `publication_date: 2026-09-20`, which
matches neither the tag nor `main`. The row names a likely cause, that Zenodo stamps in its own
timezone rather than UTC. That cause is not confirmed, since one observation cannot distinguish it
from any other rule Zenodo applies, and the next release is the trial that would settle it.
`date-released` in this repository does not drive the DOI's date.

**Lesson**: A date that an outside system assigns is measured from that system, not predicted from
this repository's files.

**Supersedes**: none.

**Filed**: 2026-10-21.

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
