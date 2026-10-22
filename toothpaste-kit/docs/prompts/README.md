# Prompts catalog

This kit's reusable prompts are its skills. Each entry below names a skill directory under
`skills/`, links to its `SKILL.md`, and gives the `description` field from that file's
frontmatter, copied without change. The commands are listed with their brevity codes in the
`commands` skill, which the entry for it links to.

## commands

[`skills/commands/SKILL.md`](../../skills/commands/SKILL.md)

Gateway and index for the project command vocabulary. Lists all twenty-seven commands with their brevity codes and one-line summaries, and resolves HELP and MAN directly. Does not hold the behavioral rules themselves; those live in working-preferences, which is the source of truth for what each command does.

## daily-dashboard

[`skills/daily-dashboard/SKILL.md`](../../skills/daily-dashboard/SKILL.md)

Open a working day with a dashboard of where the tree actually stands. Reads the standing files, verifies carry-over work against the working trees rather than trusting the last session's closing report, then presents project state, ranked todos, roadmap, and the decisions waiting on the human. Invoke at the start of a working session. The mirror of session-close, which writes what this reads; it does not capture session residue, and it does not begin the work it lists.

## daily-review

[`skills/daily-review/SKILL.md`](../../skills/daily-review/SKILL.md)

Once-a-day pass over the task board's lanes. Clarifies the Inbox to empty, checks each open task's priority quadrant, carries unfinished Doing work forward with its count, offers the Verify lane for close, and sets the order of Next and the day's Most Important Task. A tool prepares every list; the person decides every move, and nothing moves before they answer. Invoke once a day, after the dashboard if one is run. Does not replace the dashboard, which is the state view and may run any number of times.

## document-standards

[`skills/document-standards/SKILL.md`](../../skills/document-standards/SKILL.md)

Universal writing and quality standards for any standalone document Claude generates, reports, essays, letters, resumes, README files, technical docs, and everything else. Covers formality/density/audience dials, a Content Read step, a pre-flight checklist, and a full anti-slop reference. Does not cover conversational chat responses (see working-preferences) or document-type presets specific to network admin and DevOps audiences (see technical-documents).

## jot

[`skills/jot/SKILL.md`](../../skills/jot/SKILL.md)

Agent-callable micro-capture at a clean boundary. Appends one short, marked entry of decisions, corrections and findings from the stretch just finished to the day's capture file. Costs about one reply. Does not replace or satisfy session-log or session-close.

## merge-proxy

[`skills/merge-proxy/SKILL.md`](../../skills/merge-proxy/SKILL.md)

Session-scoped accommodation, invoked by a person only. Lets the agent run a merge into a trunk and push it, on a repository whose remote is internal or absent, after explaining the exact plan in full and halting for explicit approval of that plan. The decision stays the person's; only the keystrokes move. Never applies to a public or internet remote, including GitHub.

## monthly-review

[`skills/monthly-review/SKILL.md`](../../skills/monthly-review/SKILL.md)

Once-a-month pass over the parts of the task board that only a long interval shows. Adopts or rejects each Someday/Maybe item, asks whether each long-stalled Waiting task is still committed work, and lets the person choose which of the tool's archive candidates leave the board, and by which door. A tool prepares every list; the person decides every move, and nothing moves before they answer. Invoke once a month, after that week's weekly review. Does not replace the weekly review, which chases blockers and reads the Done lane.

## orient

[`skills/orient/SKILL.md`](../../skills/orient/SKILL.md)

Re-establish where things actually stand before acting. Runs the tree's own reorient tool for the mechanical half, then answers four questions against its output: what moved, where the record disagrees with the tree, which carried assumption did not survive, and whether the next action changes. Deliberately cheap. Use after a compaction, after a handoff, when returning to a session, or before acting on any summary. Not a replacement for daily-dashboard, which opens a working day and ranks the work.

## redaction-gate

[`skills/redaction-gate/SKILL.md`](../../skills/redaction-gate/SKILL.md)

Run the pre-publish redaction pass before content crosses a sensitivity tier boundary outward, such as a vendor API call, a Git commit, a repomix pack, or a handoff to an agent on another account. Checks candidate output against the local restricted corpus.

## session-close

[`skills/session-close/SKILL.md`](../../skills/session-close/SKILL.md)

Run the end-of-session capture procedure for this PKD. Sweeps the session for reasoning, decisions, and near misses that exist nowhere on disk, then updates the six files that must stay current. Invoke before ending any working session.

## session-log

[`skills/session-log/SKILL.md`](../../skills/session-log/SKILL.md)

Mid-session capture, run when the conversation is about to be compacted, handed off, or otherwise lose its detail while the work is unfinished. Records the decisions, corrections, open questions and findings from the recent stretch to one append-only file in a single pass, with no verification sweep and no standing-file updates. Deliberately cheaper and narrower than session-close, which it does not replace and does not satisfy.

## skill-creation

[`skills/skill-creation/SKILL.md`](../../skills/skill-creation/SKILL.md)

How to add a new skill to this system, once the decision to build one is already made. Naming convention, required section shape, a sizing target and split ceiling, and the integration and pre-publish checklists a new skill runs through before it counts as live. Does not decide whether a recurring need is worth a skill in the first place (see skill-discovery) or check a skill file's prose against content-quality standards (see document-standards, which still governs SKILL.md and CHANGELOG.md as generated documents).

## skill-discovery

[`skills/skill-discovery/SKILL.md`](../../skills/skill-discovery/SKILL.md)

How a recurring need gets recognized as worth turning into a skill, and how an existing skill in this system gets located once built. Covers the worthiness test and the discovery process itself, not what happens inside a skill once it's triggered (each skill's own frontmatter description handles that) or how to structure a new skill file (see skill-creation).

## surface-regimes

[`skills/surface-regimes/SKILL.md`](../../skills/surface-regimes/SKILL.md)

Detects which of three behavioral regimes the current session runs under, interactive-synchronous, autonomous-asynchronous, or programmatic-contractual, and adjusts working-preferences dials and mechanics, and document-standards/technical-documents applicability, accordingly. Regime is derived from a session's capability profile rather than from a vendor's product name, so it holds on any vendor's surface. Applies to any single session on any agent surface, not only multi-agent relay threads. Trigger on any mention of Cowork, Routine, headless, Agent SDK, raw API call, a CLI or IDE coding agent from any vendor, or an explicit regime, capability, or surface field in a relay or handoff message.

## technical-documents

[`skills/technical-documents/SKILL.md`](../../skills/technical-documents/SKILL.md)

Document-type presets and audience-specific vocabulary for technical documents (runbooks, incident postmortems, ADRs, README files, on-call handoff notes, change-management docs, SOPs) aimed at senior network admin, DevOps, and DevSecOps readers. Extends document-standards; does not redefine its dials, checklist, or anti-slop references.

## touch

[`skills/touch/SKILL.md`](../../skills/touch/SKILL.md)

Agent-callable single-fact update to a standing file, made right after the work it records. One queue status, one new flag, or one state line, plus a marked ledger line in the day's capture file. Never moves, resolves or rewrites; never runs checks. Does not replace or satisfy session-close.

## weekly-review

[`skills/weekly-review/SKILL.md`](../../skills/weekly-review/SKILL.md)

Once-a-week pass over the task board's slower lanes. Chases each Waiting task's blocker, names every task carried in Doing by its count, reads the week's Done lane back against what was planned, and schedules one important task that nothing urgent is forcing. A tool prepares every list; the person decides every move, and nothing moves before they answer. Invoke once a week, after a daily review. Does not replace the daily review, which empties the Inbox and orders Next.

## working-preferences

[`skills/working-preferences/SKILL.md`](../../skills/working-preferences/SKILL.md)

Standing behavioral defaults, register, prohibitions, correction protocol, and command vocabulary for working with this user. Near-always relevant, load for any task requiring sustained interaction, judgment calls, or multi-step work. Does not cover technical document authoring standards (see document-standards) or frontend/UI design (deferred, not yet built).
