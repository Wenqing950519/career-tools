# Skills

平台的四個主線 skill 已各自獨立 repo，此處只保留支線 skill 與共用契約。

## 平台主線（獨立 repo）

| Skill | Label | Main output | Tier | Repo |
| --- | --- | --- | --- | --- |
| `skill-gap` | 找差距 | Prioritized capability gaps and validation actions | `agent` | [career-skill-gap](https://github.com/Wenqing950519/career-skill-gap) |
| `resume-composer` | 打履歷 | Traceable resume draft from interviewed or confirmed evidence | `instant` | [career-resume-composer](https://github.com/Wenqing950519/career-resume-composer) |
| `opportunity-catch` | 抓機會 | Live, deduplicated, deadline-verified opportunity list | `agent` | [career-opportunity-catch](https://github.com/Wenqing950519/career-opportunity-catch) |
| `offercheck` | 選 offer | Deep scored offer report with JSON, Markdown, and HTML validation | `agent` | [career-offercheck](https://github.com/Wenqing950519/career-offercheck) |

## 支線（本 repo）

| Skill | Label | Main output | Tier | Web | Custom GPT | Claude Skill | Claude Code |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `direction-explorer` | 挖方向 | 2–4 direction hypotheses, sources, unknowns, 30-minute actions | `instant` | ✓ | ✓ | ✓ | ✓ |
| `experience-curator` | 寫經歷 | Five-section evidence and contribution boundary | `instant` | ✓ | ✓ | ✓ | ✓ |
| `opportunity-review` | 評機會 | Hard-constraint and multi-axis opportunity review | `instant` | ✓ | ✓ | ✓ | ✓ |
| `interview-story` | 說故事 | Spoken STAR story and honesty boundary | `instant` | ✓ | ✓ | ✓ | ✓ |

`experience-curator` 的證據方法與貢獻邊界紀律已併入 `resume-composer` 的 standalone 訪談模式。`opportunity-review` 的單一機會檢視在平台上由 `opportunity-catch` 的篩選階段承接。

## Validation and idempotency

Each round-trip skill includes `schemas/envelope.schema.json`, its record-data schema, and `scripts/validate_response.py`. Importers must validate the complete response, enforce pending-only state, and upsert deterministic proposal IDs or canonical payload fingerprints rather than append every rerun. The fingerprint recursively excludes `generated_at`, `created_at`, and `updated_at`, so generation time does not turn an otherwise identical proposal into a duplicate.

The validator enforces each fallback ID. When the website injects an existing ID, pass a context JSON file with `injected_ids`. For `interview-story`, also pass `confirmed_source_ids` and the exact `question_type`. Example: `python scripts/validate_response.py response.md --context invocation-context.json`. Context-dependent provenance cannot be proven from the response alone, so production imports must provide this context.
