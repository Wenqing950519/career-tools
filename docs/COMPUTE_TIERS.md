# Compute Tiers

四個 skill 各自獨立 repo，仍列於此以維持成本比較的完整性。

| Skill | Repo | Input sources | Web search | Code | Estimated tokens | Tier | Reason |
| --- | --- | --- | --- | --- | ---: | --- | --- |
| `resume-composer` | career-resume-composer | Interviewed experiences or injected confirmed evidence, optional JD | No | No | 6,000 | `instant` | Traceable transformation; standalone mode adds interview turns. |
| `skill-gap` | career-skill-gap | Target, explicit ratings, evidence, market requirements | Yes | No | 6,000 | `agent` | May need current primary market sources. |
| `opportunity-catch` | career-opportunity-catch | Resume summary or minimal intent, mode choice | Yes | No | 12,000 | `agent` | Live search, dedup, deadline verification, lazy deep-verify. |
| `offercheck` | career-offercheck | Company, JD, interview, terms, constraints, alternatives | Yes | Yes | 18,000 | `agent` | Deep evidence report, validation, and HTML rendering. |

`offercheck` is intentionally not offered on chat-only platforms because its full workflow requires code execution and validated report artifacts.

## Validation

`resume-composer` and `skill-gap` follow the round-trip contract in [`../contracts/round-trip.md`](../contracts/round-trip.md) and each ships its own `schemas/envelope.schema.json`, record-data schema, and `scripts/validate_response.py` inside its repo.

Importers must validate the complete response, enforce pending-only state, and upsert deterministic proposal IDs or canonical payload fingerprints rather than append every rerun. The fingerprint recursively excludes `generated_at`, `created_at`, and `updated_at`, so generation time does not turn an otherwise identical proposal into a duplicate.

When the website injects an existing ID, pass a context JSON file with `injected_ids`; for `resume-composer` in injected mode, also pass `confirmed_source_ids`. Standalone mode assigns `chat-1`, `chat-2`, … at the moment the user affirms each experience, and the validator checks they are sequential without gaps or duplicates.

`opportunity-catch` outputs prose only and has no machine block to validate. `offercheck` uses its own stronger report schema and validator, documented in its repo.
