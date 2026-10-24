# Session summary format

This file is the format only. Real session summaries are kept outside this repository, in the HumanLayer task's artifacts, because they record a conversation and this repository is public.

The format is toothpaste-kit's, unchanged: [`toothpaste-kit/.claude/session-summary.md`](../toothpaste-kit/.claude/session-summary.md), defined by its `session-log` skill. In short, each entry answers what applies of:

1. Decisions and the alternative rejected
2. Corrections
3. Open questions
4. Findings the tree does not hold
5. Where the work stands: the next concrete action

Append only, one entry per stretch of work, headed with the time.

## Continuity between sessions

A new session, or one resumed after its context was compacted, reads the task's latest summary and plan before acting, then checks them against the tree with the `orient` skill. A summary is a claim about the tree, not the tree.
