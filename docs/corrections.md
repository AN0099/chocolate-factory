# Correction capture

The Correction Protocol in `skills/working-preferences/SKILL.md` tells an agent to stand down
permanently on a point once the user has confirmed their position or the challenge limit is
reached. "Permanently" has to outlast the session, so the agent keeps a record of each such point
and reads it before raising a point again.

## Where the records live

**In the user's own workspace, outside any repository.** A record holds what was said in a
conversation, and a repository can be shared or published. The `corrections.jsonl` at this
repository's root is empty and stays empty: it marks the format, and nothing is recorded in it.

## Format

`corrections.jsonl`: one JSON object per line, one line per point.

| Field | Type | Meaning |
|---|---|---|
| `kind` | `"error"` or `"challenge"` | The agent corrected its own error, or stated a case against the user's position |
| `point` | string | The point, in one sentence |
| `explained` | boolean | Whether an explanation was given, which happens only under REVIEW or on request |
| `severity` | `"low"`, `"medium"` or `"high"` | How hard the agent may persist |
| `challenges` | integer, 0 to 3 | Challenges made so far; the protocol allows three |
| `stood_down` | `null`, `"limit"` or `"confirmed"` | Open, ended at the limit, or ended when the user confirmed their position |

An invented example:

```json
{"kind": "challenge", "point": "the backup job runs before the index rebuild", "explained": false, "severity": "medium", "challenges": 2, "stood_down": "confirmed"}
```

The agent writes or updates a line when it corrects an error, states a case, or stands down.
