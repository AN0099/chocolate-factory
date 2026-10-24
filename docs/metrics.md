# Metrics

The pull request acceptance metric: what is measured, the command that measures it, and the figures on the day it was last run.

## Definition

**Acceptance** is the share of closed pull requests that were merged. A pull request that is still open is not counted, because its outcome is not known.

- **Merged**: `state` is `MERGED`.
- **Closed unmerged**: `state` is `CLOSED`, which means closed without a merge.
- **Open**: `state` is `OPEN`. Reported separately and left out of the rate.

Acceptance rate is merged divided by merged plus closed unmerged.

**Review rounds per PR** is the number of entries in a pull request's `reviews` list, as GitHub records them. It counts reviews submitted through GitHub's review feature. A comment left on an issue thread, a conversation held outside GitHub, or a review given by commit suggestion does not appear in it, so a count of zero means no recorded review and not that nobody looked.

## The command

Read-only. It changes nothing in the repository.

```sh
gh pr list --repo AN0099/toothpaste-kit --state all --limit 200 --json number,state,mergedAt,closedAt,reviews
```

`--limit 200` is a ceiling. If the command returns exactly 200 pull requests, raise the limit before trusting a count.

To reduce the output to the figures below:

```sh
gh pr list --repo AN0099/toothpaste-kit --state all --limit 200 --json number,state,reviews \
  --jq '{total: length,
         merged: ([.[] | select(.state == "MERGED")] | length),
         closed_unmerged: ([.[] | select(.state == "CLOSED")] | length),
         open: ([.[] | select(.state == "OPEN")] | length),
         reviews_total: ([.[] | .reviews | length] | add),
         prs_with_a_review: ([.[] | select((.reviews | length) > 0)] | length)}'
```

## Figures

Run on 2026-10-20 with the second command above, the one that reduces the list to the figures, against `AN0099/toothpaste-kit`.

| Measure | Value |
|---|---|
| Pull requests, all states | 24 |
| Merged | 24 |
| Closed unmerged | 0 |
| Open | 0 |
| Acceptance rate | 24 of 24 |
| Pull requests with at least one recorded review | 2 |
| Reviews recorded across all pull requests | 4 |

The two pull requests with recorded reviews carry three and one reviews, and every one of the four has the state `COMMENTED`. The other 22 have none. Pull request numbers run to 37 because issues share the numbering.

## How to read it

A rate of 24 of 24 says that nothing was closed unmerged. It does not say the changes were good, and it does not say they were reviewed. Read it with the review count beside it: 22 merged pull requests have no recorded review, so for most of them the checks that bound were the automated gates and not a second reader. See `docs/review-rubric.md` for what a reviewer checks and `docs/quality.md` for where the other measures live.

The figures change with every merge. Rerun the command and replace the table and its date together, and do not edit one without the other.

## What this does not cover

- Time to merge, time to first review, and size of change.
- Reviews that happen outside GitHub's review feature.
- Pull requests closed by a bot or by their author for reasons unrelated to quality, which count as closed unmerged here and are not separable by this command.
- Anything about commits pushed directly to a branch without a pull request.

<!--
SPDX-FileCopyrightText: 2026 Aidan Naveja

SPDX-License-Identifier: Apache-2.0
-->
