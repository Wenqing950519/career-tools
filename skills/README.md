# Career Town Skills

The catalog contains six round-trip Career Town skills plus the deeper `offercheck` report engine. The six round-trip skills return Traditional Chinese prose followed by one final `careertown` JSON block, and every generated record is pending.

| Skill | Label | Main output | Tier | Web | Custom GPT | Claude Skill | Claude Code |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `direction-explorer` | 挖方向 | 2–4 direction hypotheses, sources, unknowns, 30-minute actions | `instant` | ✓ | ✓ | ✓ | ✓ |
| `experience-curator` | 寫經歷 | Five-section evidence and contribution boundary | `instant` | ✓ | ✓ | ✓ | ✓ |
| `skill-gap` | 找差距 | Prioritized capability gaps and validation actions | `agent` | ✓ | ✓ | ✓ | ✓ |
| `opportunity-review` | 評機會 | Hard-constraint and multi-axis opportunity review | `instant` | ✓ | ✓ | ✓ | ✓ |
| `resume-composer` | 打履歷 | Traceable resume draft from confirmed evidence | `instant` | ✓ | ✓ | ✓ | ✓ |
| `interview-story` | 說故事 | Spoken STAR story and honesty boundary | `instant` | ✓ | ✓ | ✓ | ✓ |
| `offercheck` | 選 offer | Deep scored offer report with JSON, Markdown, and HTML validation | `agent` | ✓ | — | — | ✓ |
| `opportunity-catch` | 抓機會 | Live web-searched, deduplicated, deadline-verified internship/competition list with traceable rank reasons | `agent` | ✓ | ✓ | ✓ | ✓ |

`opportunity-catch` is a platform-line skill (stage ④ of `docs/PLATFORM_PRD.md`). It outputs prose only (no `careertown` JSON block) and supersedes `opportunity-review` as the platform entry for stage ④; `opportunity-review` remains for single-listing review inside Career Town.

## Validation and idempotency

Each round-trip skill includes `schemas/envelope.schema.json`, its record-data schema, and `scripts/validate_response.py`. Importers must validate the complete response, enforce pending-only state, and upsert deterministic proposal IDs or canonical payload fingerprints rather than append every rerun. The fingerprint recursively excludes `generated_at`, `created_at`, and `updated_at`, so generation time does not turn an otherwise identical proposal into a duplicate.

The validator enforces each fallback ID. When the website injects an existing ID, pass a context JSON file with `injected_ids`. For `resume-composer` and `interview-story`, pass `confirmed_source_ids`; for `interview-story`, also pass the exact `question_type`. Example: `python scripts/validate_response.py response.md --context invocation-context.json`. Context-dependent provenance cannot be proven from the response alone, so production imports must provide this context.

`offercheck` deliberately retains its stronger report schema, evidence graph, validator, renderer, numeric decision model, and artifact workflow. It replaces the weaker round-trip `offer-decision`; the two are not retained together.
