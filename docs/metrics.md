# Metrics

The pull request acceptance metric, defined as in [`toothpaste-kit/docs/metrics.md`](../toothpaste-kit/docs/metrics.md): merged divided by merged plus closed unmerged, with open pull requests reported separately. Review rounds are the entries in each pull request's `reviews` list.

## The command

Read-only:

```sh
gh pr list --repo AN0099/chocolate-factory --state all --limit 200 --json number,state,reviews \
  --jq '{total: length,
         merged: ([.[] | select(.state == "MERGED")] | length),
         closed_unmerged: ([.[] | select(.state == "CLOSED")] | length),
         open: ([.[] | select(.state == "OPEN")] | length),
         reviews_total: ([.[] | .reviews | length] | add),
         prs_with_a_review: ([.[] | select((.reviews | length) > 0)] | length)}'
```

If it returns exactly 200 pull requests, raise `--limit` before trusting a count.

## Figures

Run on 2026-10-24 against `AN0099/chocolate-factory`.

| Measure | Value |
|---|---|
| Pull requests, all states | 4 |
| Merged | 4 |
| Closed unmerged | 0 |
| Open | 0 |
| Acceptance rate | 4 of 4 |
| Pull requests with at least one recorded review | 0 |
| Reviews recorded | 0 |

## How to read it

4 of 4 says nothing was closed unmerged. It does not say anything was reviewed: no pull request has a recorded GitHub review. Each was read by the person who merged it, and the checks that bound were the automated ones. Read it with `docs/review-rubric.md`.

Rerun the command and replace the table and its date together.
