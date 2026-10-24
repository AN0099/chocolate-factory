# Agents

Instructions for a coding agent working in this repository. `toothpaste-kit/` is a subtree with its own `AGENTS.md`; where the two disagree inside `toothpaste-kit/`, this file wins.

## Hard rules

These are not defaults. An agent does not weigh them against convenience, and does not rephrase a blocked command to get past the check that blocked it. If one stands in the way of the work, stop and ask the person.

### 1. Branch and tag names are chosen, short, and never derived from a request

A branch name is public the moment it is pushed. Copies of public push events persist outside GitHub, so deleting the branch, or the repository, does not take the name back. On 2026-10-22 a HumanLayer task branch, named automatically from the opening words of the request that started the task, was pushed and published that way. Nothing sensitive was in it; the next one could carry anything a request says.

- **Allowed names:** `main`, or `<prefix>/<words>`, with `<prefix>` one of `feat`, `fix`, `docs`, `chore`, `sync`, `acmm`, `record`, `ci`, `quality`, `skills`, `scripts`, `release`, `test` or `licence`, and `<words>` lowercase `a-z` and `0-9` joined by single hyphens or dots (`release/0.4.0`), 40 characters in all. Names GitHub suggests, such as `AN0099-patch-1` from the web editor or an issue-titled branch, are refused: type a name instead. Only the Dependabot app may create `dependabot/` branches. Tags look like `v1.2.3`. `scripts/check-branch-name` is the one definition; check a name with it before using it.
- **Never push a task branch.** HumanLayer names each task's branch `local/<task slug>`, and that name never leaves the machine. To publish work, choose a name and push to it explicitly:

  ```sh
  scripts/check-branch-name chore/short-name
  git push origin HEAD:refs/heads/chore/short-name
  ```

- **Always give the destination.** Every `git push` names its destination with a `:` refspec, and every `gh pr create` passes `--head`. Without them, the remote name comes from whatever the local branch is called.
- **Never skip or redirect hooks.** No `--no-verify`, no `git commit -n`, no `core.hooksPath`.
- **Words from a request never become a name.** This covers branch names, tags, PR titles, commit subjects and file names. Describe the change in your own words, and leave out anything a request says that does not need to be public.

The same rule is enforced at five points, so that one failing does not let a name out:

| Layer | Where | What it does |
|---|---|---|
| `scripts/check-branch-name` | Called by every layer below | The one definition of an allowed name, with `--selftest` |
| `.githooks/pre-push` | Every local push, agent or person | Refuses the push before anything leaves the machine. Enabled per clone by `git config core.hooksPath .githooks`, which HumanLayer's `setupCommand` runs for every task workspace |
| `.claude/hookify.branch-name-guard.local.md` | Agent sessions | Blocks pushes without a refspec, `gh pr create` without `--head`, and any way of skipping hooks. `scripts/check-branch-guard` tests it against `tests/branch-guard-cases.tsv` |
| `.github/rulesets/branch-names.json`, `tag-names.json` | GitHub's servers | Refuse to create a branch or tag outside the allowed prefixes, with no bypass. The layer that holds when a hook does not run |
| `.github/workflows/branch-name.yml` | Every push and pull request | Fails a non-conforming name, and runs both selftests. A backstop: by then the name is public |

### 2. Provenance, never attribution

- No `Co-Authored-By` line naming an AI, no "Generated with" footer, in a commit or a pull request.
- A commit you write ends with the lines `scripts/agent-trailers` prints. The `prepare-commit-msg` hook adds them; do not type them yourself, and never fill in a value the script left out.
- A pull request you open ends its body with the same lines inside `<details><summary>Provenance</summary> … </details>`.
- Sign every commit with the agent key. `main` refuses unsigned commits.

## Working here

- Read `CONTRIBUTING.md`: setup, pull requests, and the `toothpaste-kit/` subtree.
- Do not edit `toothpaste-kit/` in this repository. Changes go to toothpaste-kit first, then come here with `git subtree pull`.
- Inside `toothpaste-kit/`, its own `AGENTS.md` applies wherever it does not contradict this file.
- Long pull request bodies go in a file passed with `--body-file`. The branch guard matches the whole command text, so prose that mentions a blocked command gets blocked too.
- `.github/copilot-instructions.md`, `.cursor/rules/agents.mdc` and `CLAUDE.md` only point here. A rule belongs in this file.
