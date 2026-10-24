# Contributing

chocolate-factory is an R&D repository for testing toothpaste-kit, HumanLayer and the agent tooling around them. Agents and people work here under the same rules; agents also follow `AGENTS.md`.

## Setting up a clone

```sh
git config core.hooksPath .githooks
```

HumanLayer runs this for every task workspace. It enables two hooks:

- `pre-push` refuses a branch or tag name that `scripts/check-branch-name` does not allow.
- `prepare-commit-msg` adds provenance lines to a commit an agent writes (see below). It does nothing for a person's commit.

## Branches and pull requests

- Name branches `<prefix>/<words>`, as `AGENTS.md` rule 1 defines. Check a name with `scripts/check-branch-name <name>` before using it.
- One change per pull request. Merge with a merge commit; squash and rebase are turned off, so that the subtree history and signatures survive.
- Every commit on `main` is signed. People sign with their own key; agents sign with the agent key registered on the account.

## Provenance, not attribution

Commits do not carry `Co-Authored-By` lines naming an AI, or "Generated with" footers. A commit an agent writes instead ends with:

```text
Assisted-by: <model> via claude-code/<version>
Agent-Effort: <level>
```

`scripts/agent-trailers` reads each value from its source when the commit is made, and leaves out any it cannot read. A pull request an agent opens ends its body with the same lines inside a collapsed `<details><summary>Provenance</summary>` block.

## The `toothpaste-kit/` subtree

`toothpaste-kit/` is a `git subtree` of AN0099/toothpaste-kit. Do not edit it here.

- To update it: `git subtree pull --prefix=toothpaste-kit <url> main`, in its own pull request, merged with a merge commit. Check afterwards that `git subtree split --prefix=toothpaste-kit HEAD` gives the upstream commit, and that `toothpaste-kit/tests/run` passes.
- To change it: make the change in toothpaste-kit itself, following its `CONTRIBUTING.md` (including its DCO sign-off and REUSE headers), then pull it here.
