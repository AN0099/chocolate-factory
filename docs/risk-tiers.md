# Risk tiers

Which changes need which review. A change takes the highest tier among the paths it touches, and each tier's review includes every tier below it. The `labeler` workflow adds the labels shown; a label prompts the reviewer and decides nothing.

| Tier | Touches | Labels |
|---|---|---|
| 1 | Documentation: `docs/`, root Markdown files other than `AGENTS.md` and `CLAUDE.md`, `.editorconfig`, `.gitignore`, `corrections.jsonl` | `documentation` |
| 2 | Agent configuration: `AGENTS.md`, `CLAUDE.md`, `.claude/`, `.cursor/`, `.github/copilot-instructions.md`, `.humanlayer/` | `agent-config` |
| 3 | Gates and workflows: `scripts/`, `tests/`, `.githooks/`, `.github/`, including `.github/rulesets/` | `gates`, `workflows` |
| 4 | The subtree: anything under `toothpaste-kit/` | `subtree` |

## What each tier needs

- **Tier 1.** `./tests/run` passes; the review rubric's items 1 to 8.
- **Tier 2.** Also: a pointer file adds no rule of its own (`AGENTS.md` holds them); a hook rule is tested against something it must catch and something it must let through. These files steer agents, so a wrong one misleads every later session.
- **Tier 3.** Also: every gate added or changed shows its planted positive caught (rubric item 1). A change to a file in `.github/rulesets/` needs the matching change applied on GitHub by a person, because the files are a record and GitHub does not read them.
- **Tier 4.** Only a `git subtree pull`, in its own pull request, with `git subtree split` matching the upstream commit and `toothpaste-kit/tests/run` passing (rubric item 9). Any other change under `toothpaste-kit/` is refused here and made upstream instead.

Tier 4 is highest because this copy is what the experiments here run against: a local edit would make the results describe a toothpaste-kit that does not exist.
