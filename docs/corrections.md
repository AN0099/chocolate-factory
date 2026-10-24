# Correction capture

When an agent is corrected, or stands down on a point, it keeps a record so the point is not raised again in a later session. The protocol is in toothpaste-kit's `working-preferences` skill, and the format is in [`toothpaste-kit/docs/corrections.md`](../toothpaste-kit/docs/corrections.md). This repository uses both unchanged.

## Where the records live

**Outside this repository**, in the person's own workspace or the HumanLayer task's artifacts. A record holds what was said in a conversation, and this repository is public.

`corrections.jsonl` at the root is empty and stays empty. It marks the format; nothing is recorded in it.

## When a correction becomes a rule

A correction that should bind every future session becomes a rule in `AGENTS.md`, or upstream in toothpaste-kit, through a pull request. The rule describes the behaviour in general terms. It never quotes the conversation that produced it.
