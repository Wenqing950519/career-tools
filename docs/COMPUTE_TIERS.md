# Compute Tiers

平台主線 skill 已獨立 repo，仍列於此以維持成本比較的完整性。

| Skill | Repo | Input sources | Web search | Code | Estimated tokens | Tier | Reason |
| --- | --- | --- | --- | --- | ---: | --- | --- |
| `direction-explorer` | 本庫 | Quiz answers, conversation, profile snapshot | No | No | 4,000 | `instant` | Bounded 2–4 hypothesis synthesis. |
| `experience-curator` | 本庫 | One narrated experience | No | No | 4,000 | `instant` | One-record evidence extraction. |
| `opportunity-review` | 本庫 | One pasted listing and user constraints | No | No | 5,000 | `instant` | Bounded review without discovery. |
| `interview-story` | 本庫 | One confirmed experience and question type | No | No | 4,000 | `instant` | One spoken STAR transformation. |
| `skill-gap` | career-skill-gap | Target, explicit ratings, evidence, market requirements | Yes | No | 6,000 | `agent` | May need current primary market sources. |
| `resume-composer` | career-resume-composer | Interviewed experiences or injected confirmed evidence, optional JD | No | No | 6,000 | `instant` | Traceable transformation; standalone mode adds interview turns. |
| `opportunity-catch` | career-opportunity-catch | Resume summary or minimal intent, mode choice | Yes | No | 12,000 | `agent` | Live search, dedup, deadline verification, lazy deep-verify. |
| `offercheck` | career-offercheck | Company, JD, interview, terms, constraints, alternatives | Yes | Yes | 18,000 | `agent` | Deep evidence report, validation, and HTML rendering. |

`offercheck` is intentionally not offered on chat-only platforms because its full workflow requires code execution and validated report artifacts.
