# What this changes

<!-- One or two sentences: what changed, and why. -->

## Checks

```sh
./tests/run
```

- [ ] `./tests/run` passes
- [ ] The branch name passes `scripts/check-branch-name`, and was chosen, not taken from a request
- [ ] Every commit is signed
- [ ] No `Co-Authored-By` naming an AI and no "Generated with" footer; agent commits carry the `scripts/agent-trailers` lines
- [ ] `toothpaste-kit/` changes only through `git subtree pull`

## Verification

<!-- How you confirmed it works. An agent checking its own work does not count. -->

## Findings

<!-- Anything wrong that you did not fix here. -->

## Merge

Merge commit only.

<!-- An agent's pull request ends with:
<details>
<summary>Provenance</summary>

Assisted-by: ...
Agent-Effort: ...

</details>
-->
