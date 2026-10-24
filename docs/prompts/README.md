# Prompts catalog

The reusable prompts used in this repository are skills. None are defined here: they come from the `toothpaste-kit/` subtree or from HumanLayer's plugins. This catalog links them rather than copying them, so each description stays where it is maintained.

## From toothpaste-kit

toothpaste-kit's own catalog lists every skill with its description: [`toothpaste-kit/docs/prompts/README.md`](../../toothpaste-kit/docs/prompts/README.md). The ones in use here:

| Skill | Used for |
|---|---|
| [`working-preferences`](../../toothpaste-kit/skills/working-preferences/SKILL.md) | The Q-block question format, the command codes (`f`, `d`, `j`, `pr:`) and the correction protocol |
| [`document-standards`](../../toothpaste-kit/skills/document-standards/SKILL.md) | Every document in `docs/` and the root Markdown files |
| [`redaction-gate`](../../toothpaste-kit/skills/redaction-gate/SKILL.md) | Before anything crosses outward, such as a push or a pull request body |
| [`session-log`](../../toothpaste-kit/skills/session-log/SKILL.md) | The session summary format in `.claude/session-summary.md` |
| [`orient`](../../toothpaste-kit/skills/orient/SKILL.md) | Re-establishing state after a context compaction |

## From HumanLayer

HumanLayer's `rpi` plugin supplies the research, plan and implement workflow for a task. Its skills are installed per machine, not stored in this repository.

| Skill | Used for |
|---|---|
| `rpi:create-research`, `rpi:iterate-research` | Researching a task's codebase questions |
| `rpi:create-plan`, `rpi:iterate-plan` | Writing and revising an implementation plan as a task artifact |
| `rpi:implement-plan` | Carrying out an approved plan phase by phase |
| `rpi:describe-pr` | Drafting a pull request description from a plan |
| `rpi:review-artifact-comments` | Answering review comments left on a task artifact |

Task artifacts, such as plans and research, live in HumanLayer's task directory, which `.gitignore` keeps out of this repository.
