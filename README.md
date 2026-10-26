# Chocolate Factory

Bridle Works' R&D software factory: a testing environment for toothpaste-kit, HumanLayer and the agent tooling around them.

## Layout

| Path | What it holds |
|---|---|
| `toothpaste-kit/` | A `git subtree` of [AN0099/toothpaste-kit](https://github.com/AN0099/toothpaste-kit), the kit under test. Not edited here |
| `AGENTS.md` | The rules for agents working here; `CLAUDE.md`, Copilot and Cursor files point to it |
| `scripts/`, `tests/`, `.githooks/` | The gates: branch names, provenance lines, the test suite |
| `docs/` | Quality, governance and control documents |
| `.github/` | Workflows, templates, labels and the ruleset records |
| `.humanlayer/workspace.json` | How HumanLayer creates a task workspace from this repository |

## Where to start

1. Read `CONTRIBUTING.md`, then run `git config core.hooksPath .githooks` in your clone.
2. Run `./tests/run`. It runs this repository's gates, then toothpaste-kit's.
3. Agents read `AGENTS.md` first.

## The subtree

`toothpaste-kit/` changes only by `git subtree pull --prefix=toothpaste-kit`, in its own pull request, merged with a merge commit. Changes to the kit itself go to toothpaste-kit first. `CONTRIBUTING.md` has the steps.

## Security and licensing

- Agent permissions and limits: `SECURITY-AI.md`.
- Vulnerabilities in the kit: toothpaste-kit's private reporting, as `toothpaste-kit/SECURITY.md` describes.
- The kit is Apache-2.0 (`toothpaste-kit/LICENSE`). This repository's own files carry no licence yet.
