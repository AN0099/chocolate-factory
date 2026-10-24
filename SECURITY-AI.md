# Security for AI agents

What an AI agent may and may not do in this repository. Each rule restates `AGENTS.md`, `CONTRIBUTING.md` or `docs/control-layers.md`; this file adds none.

This repository delegates more than toothpaste-kit does. There, an agent edits and a person commits and pushes. Here, an agent may also commit, push and open pull requests, within the limits below, because testing that delegation is part of what this repository is for. Merging stays with a person.

## An agent may

- Edit files, run `./tests/run`, and raise findings in an issue or pull request.
- Commit, signed with the agent key, with the provenance lines `scripts/agent-trailers` prints. Source: `AGENTS.md`, rule 2.
- Push to a branch name it chose and checked with `scripts/check-branch-name`, always with an explicit `:` destination. Source: `AGENTS.md`, rule 1.
- Open a pull request with `--head` given, ending with the Provenance block.

## An agent may not

- Merge, push to `main`, tag, or change repository settings or rulesets. The `main` ruleset refuses direct pushes, and the agent's token cannot change settings.
- Push a HumanLayer task branch, or use words from a request in any name, title or commit subject. Source: `AGENTS.md`, rule 1.
- Skip or redirect hooks. Source: `AGENTS.md`, rule 1.
- Put AI attribution in a commit or pull request, or type provenance values instead of reading them. Source: `AGENTS.md`, rule 2.
- Edit `toothpaste-kit/` other than by `git subtree pull`. Source: `AGENTS.md`, "Working here".
- Rephrase a command that a guard blocked to get past it. Stop and ask the person. Source: `AGENTS.md`, "Hard rules".
- Report its own work as verified. CI and the merging person are the second party.

## Limits an agent works inside

The sandbox, the token's scope and the guard are described in `docs/control-layers.md`, with how each fails. The guard is pattern-based and is not a boundary on its own.

Vulnerabilities in toothpaste-kit go to its private reporting, per `toothpaste-kit/SECURITY.md`.
