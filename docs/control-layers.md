# Control layers

The independent layers that stand between an agent's action and a published change in this repository, ordered from the agent outward. Each assumes the ones before it have failed. The vocabulary comes from [`toothpaste-kit/docs/control-layers.md`](../toothpaste-kit/docs/control-layers.md).

| Layer | Mechanism here | What it stops | How it fails |
|---|---|---|---|
| 1. Sandbox | Claude Code's OS sandbox: write access limited to the workspace; `.git/config`, `.claude/settings*.json`, `.claude/skills` and `.claude/hooks` read-only to agents; network through an allowlist | Writes outside the task, changes to the agent's own controls, unlisted hosts | A person widens it; it covers Bash commands, not a person's own shell |
| 2. Credentials | A fine-grained token scoped to this repository only | Pushing to any other repository, including toothpaste-kit | A broader token in the environment |
| 3. Agent guard | `.claude/hookify.branch-name-guard.local.md` | Pushes without a destination, `gh pr create` without `--head`, skipping or redirecting hooks | Pattern-based: a command phrased around it. Tested by `scripts/check-branch-guard` |
| 4. Local hooks | `.githooks/pre-push`, `.githooks/prepare-commit-msg` | A non-conforming branch or tag name leaving the machine; an agent commit without provenance | Not enabled in a clone without the hooks path set |
| 5. Server rulesets | `.github/rulesets/`: branch and tag names; `main` requires signatures, required checks, code scanning, no force push or deletion | A bad name created on GitHub, an unsigned or unchecked commit on `main` | Only Dependabot bypasses the name rule; nothing bypasses `main` |
| 6. CI | `branch-name`, `gates`, `ci`, CodeQL | A merge with failing checks, attribution in commits | A check not listed as required blocks nothing |
| 7. Human merge | The person merges every pull request, with a merge commit | Anything the layers above did not catch | The person not reading the change |

## Relief and containment

A branch name is public once pushed, and copies of push events persist outside GitHub. No layer can recall one. That is why layers 3 to 5 all act before a name is published, and layer 6 is only a backstop. The near miss of 2026-10-22, recorded in `AGENTS.md`, is the case these layers were built for.
