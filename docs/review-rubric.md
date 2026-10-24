# Review rubric

A reviewer here works through toothpaste-kit's rubric, [`toothpaste-kit/docs/review-rubric.md`](../toothpaste-kit/docs/review-rubric.md), items 1 to 6, then the items below, which cover what differs in this repository. Record the items checked by number; mark an item that does not apply as not applicable, with a reason.

## 7. The branch name was chosen

The head branch passes `scripts/check-branch-name`, and its words describe the change rather than repeating a request. Source: `AGENTS.md`, rule 1.

## 8. Every commit is signed and carries provenance, not attribution

Each commit shows Verified. An agent's commit ends with the `scripts/agent-trailers` lines and no `Co-Authored-By` naming an AI; an agent's pull request ends with the collapsed Provenance block. Source: `AGENTS.md`, rule 2; `CONTRIBUTING.md`, "Provenance, not attribution".

## 9. `toothpaste-kit/` changed only by subtree pull

A change under `toothpaste-kit/` arrives as a `git subtree pull` in its own pull request, and `git subtree split --prefix=toothpaste-kit HEAD` gives the upstream commit. The `subtree` label flags it. Source: `CONTRIBUTING.md`, "The `toothpaste-kit/` subtree".

## 10. Merge with a merge commit

Squash and rebase are turned off, so this is enforced; the item is a reminder of why. A squash would drop the subtree history and the commit signatures.
