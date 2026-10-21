# Reflections

A reflection entry is a bounded record about one documentation row in this repository. It restates
what the row records and states the lesson as one sentence shaped as a rule. The format is fixed by
`docs/document-layers.md`, exception 5, and this file summarises it.

## Format

One file per entry, named `NNN-short-slug.md`, where `NNN` is a three digit number assigned in
filing order. Numbers are not reused.

Each entry carries exactly these fields, in this order:

1. **Row**: the file and row it reflects on, at a pinned version: a release tag or a full commit
   hash.
2. **Records**: what that row records at the pinned version, restated from the row.
3. **Lesson**: one sentence, shaped as a rule, with no BCP 14 keyword. It may generalise from the
   row and does not contradict it.
4. **Supersedes**: the number of the entry it replaces, or "none".
5. **Filed**: the date the entry was filed.

An entry holds no session residue, no person's name, and nothing the cited row does not support at
the pinned version. A named outside system appears only where the cited row names it. Row support
is judged against the pinned version, so a later change to the row does not make the entry false.

An entry is not edited after filing. A correction is a new entry whose **Supersedes** field names
the entry it replaces, and the replaced entry stays as filed. A filed entry is a record dated by its
**Filed** field, not documentation of the current state.

## What may be reflected on

Only a row already published in this repository, such as a row in `docs/security-posture.md`. The
correction records described in `docs/corrections.md` live outside any repository and are not
reflected on here.

## Entries

| Number | Row | Pinned at | Superseded by |
|---|---|---|---|
| [001](001-predicted-doi-date.md) | `docs/security-posture.md`, row 3.2b | commit `451f63e` | none |
| [002](002-setting-not-visible-from-the-tree.md) | `docs/security-posture.md`, row 6.3 | commit `451f63e` | none |
| [003](003-plant-of-one-shape.md) | `docs/security-posture.md`, row 4.7 | commit `451f63e` | none |
