# Output Contract

Return Traditional Chinese prose followed by one final `careertown` JSON block.

The envelope validates against `schemas/envelope.schema.json`: `schema_version: 1`, `skill: "direction-explorer"`, a UTC generation timestamp, 2–4 pending `direction` records, and deduplicated `unknowns`. Attention must total 100; the platform validator enforces this cross-record rule.

Map each record without adding fields:

- `id`: reuse an injected ID. Otherwise use `direction:1` through `direction:4` in descending attention order. Never generate a random ID; the importer upserts the current pending direction batch by these IDs.
- `title`: plain-language direction family.
- `status`: `observing` for a new hypothesis.
- `attention`: integer exploration allocation; all proposed directions total 100.
- `reasons`: source-labelled signals and the meaningful uncertainty.
- `related_skills`: only explicit skill labels from context.
- `related_experiences`: only traceable confirmed experience IDs.
- `recent_change`: state that this is a new hypothesis and include its 30-minute validation action.
- `updated_at`: generation timestamp.

All user-facing strings are Traditional Chinese. Envelope record status is always `pending`. Add nothing after the block.
