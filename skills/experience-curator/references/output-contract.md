# Experience Curator Output Contract

Return a Traditional Chinese human summary followed by one final `careertown` JSON block validating against `schemas/envelope.schema.json`. The JSON contains one `experience` record unless the input contains no identifiable experience; in that case return an empty `records` array and explain the missing source account in `unknowns`.

## Envelope

Use these exact top-level fields:

- `schema_version`: integer `1`.
- `skill`: `experience-curator`.
- `generated_at`: current RFC 3339 UTC timestamp.
- `records`: pending record proposals.
- `unknowns`: unique Traditional Chinese descriptions of unresolved facts.

Each record contains `type: "experience"`, `status: "pending"`, and `data` conforming to the output schema.

## Experience field mapping

- `id`: reuse the injected event or proposal ID. If none exists, use `experience:1`; never create a random ID. The website must inject a unique event ID for multiple distinct events and upsert repeated runs.
- `title`: supported or neutral episode title.
- `raw_text`: the user's wording, preserved without polishing.
- `summary`: neutral compact summary.
- `skills`: supported skill or method labels only.
- `resume_text`: conservative candidate wording; never strengthen ownership or results.
- `confirmation_status`: always `pending`.
- `created_at`: response generation timestamp.
- `updated_at`: include only when updating an injected record.
- `source`: source label when available.
- `relative_path`: legacy optional exchange field; omit it.
- `sections`: the five arrays defined in the evidence method. Always include this object.

All generated user-facing strings must be Traditional Chinese. Preserved source text, identifiers, and controlled values are exempt from translation. Derive envelope `unknowns` from `sections.unknowns` rather than regenerating a second wording. JSON must use double quotes, contain no comments or trailing commas, and be the last response content.
