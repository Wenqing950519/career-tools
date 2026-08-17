# Output Contract

Return Traditional Chinese prose followed by one final `careertown` JSON block validating against `schemas/envelope.schema.json`.

Use `schema_version: 1`, `skill: "opportunity-review"`, a UTC timestamp, one pending `opportunity` record, and unique unknowns.

Map fields exactly:

- `id`: reuse an injected ID. Otherwise use `opportunity:<organization>:<title>` exactly. Never generate a random ID.
- `title`, `organization`: copy supported source facts.
- `bucket`: pending judgment mapping defined in the review method.
- `deadline`: source deadline in `YYYY-MM-DD`, or `null` when absent or ambiguous.
- `summary`: concise source summary plus separate hard-constraint and axis conclusions.
- `directions`: relevant supplied direction IDs or labels; never infer suitability.
- `source_url`: supplied canonical URL, or `null` when absent.
- `confirmation_status`: always `pending`.

If either title or organization is absent, emit `records: []` and list the missing identity fields in `unknowns`. Do not use an empty string, placeholder organization, or invented identity.

All user-facing strings are Traditional Chinese. Add nothing after the block.
