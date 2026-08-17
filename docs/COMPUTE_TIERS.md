# Compute Tiers

| Skill | Input sources | Web search | Code | Estimated tokens | Tier | Reason |
| --- | --- | --- | --- | ---: | --- | --- |
| `direction-explorer` | Quiz answers, conversation, profile snapshot | No | No | 4,000 | `instant` | Bounded 2–4 hypothesis synthesis. |
| `experience-curator` | One narrated experience | No | No | 4,000 | `instant` | One-record evidence extraction. |
| `skill-gap` | Target, explicit ratings, evidence, market requirements | Yes | No | 6,000 | `agent` | May need current primary market sources. |
| `opportunity-review` | One pasted listing and user constraints | No | No | 5,000 | `instant` | Bounded review without discovery. |
| `resume-composer` | Selected confirmed evidence and optional JD | No | No | 6,000 | `instant` | Traceable transformation. |
| `interview-story` | One confirmed experience and question type | No | No | 4,000 | `instant` | One spoken STAR transformation. |
| `offercheck` | Company, JD, interview, terms, constraints, alternatives | Yes | Yes | 18,000 | `agent` | Deep evidence report, validation, and HTML rendering. |
| `opportunity-catch` | Resume summary or minimal intent, mode choice | Yes | No | 12,000 | `agent` | Live search, dedup, deadline verification, lazy deep-verify. |

`offercheck` is intentionally not offered on chat-only platforms because its full workflow requires code execution and validated report artifacts.
