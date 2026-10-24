# Session summary format

The format a session summary takes. This file is the format only. Real summaries are provenance: they record the reasoning and residue of work, and they are kept outside this repository, in the provenance layer described in `docs/document-layers.md`. Nothing in this file is session content, and a summary written from this format does not belong in this repository.

The format comes from `skills/session-log/SKILL.md`, which defines it and when to run it.

## Rules

- **Append only.** A file holds one day's summaries, named `session-<date>-<slug>.md`. Add a new entry below the last, and never rewrite an earlier one. A later entry that contradicts an earlier one is a correction, and both halves are worth keeping.
- **Head each entry with the time.**
- **No em dash anywhere in the file, headings included.** Join a date and a slug with a colon: `# Session 2026-10-01: store setup`.
- **Only what the files cannot say.** Do not restate what a file holds. Record why it looks as it does: the alternative rejected, the constraint that ruled it out, the thing that turned out false.
- **Skip empty questions.** Answer only the questions that have something to answer, without writing "none".

## The five questions

### 1. Decisions and the alternative rejected

The choice, the reason, and what was turned down.

### 2. Corrections

Anything stated as fact that turned out to be wrong, and what corrected it.

### 3. Open questions

Questions raised and unresolved, with who or what is blocking each.

### 4. Findings the tree does not hold

Something established by evidence about the harness, the tooling or the environment, which no file in the store records.

### 5. Where the work stands

One paragraph a future session can restart from, naming the next concrete action and not the goal.

A log written under this format does not satisfy `session-close`. If the session ended after it, say so in the entry.

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
