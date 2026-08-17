# Output Contract

Return Traditional Chinese prose followed by one final `careertown` JSON block validating against `schemas/envelope.schema.json`.

Use `schema_version: 1`, `skill: "resume-composer"`, a UTC timestamp, one pending `resume_draft` record, and unique unknowns.

The draft uses exactly these existing fields: `photo`, `name`, `birthDate`, `phone`, `politicalStatus`, `email`, `city`, `certifications`, `skills`, `hobbies`, `education`, and `experiences`.

Education entries use `school`, `major`, `degree`, `time`, and `details`. Experience entries use `category`, `title`, `role`, `time`, `details`, and `sourceId`. Use only the allowed Traditional Chinese category values. Use `null` for unknown string fields as permitted by the exchange schema.

`politicalStatus` is retained as a field name for schema compatibility. The web resume builder labels it 狀態 and uses it for availability such as 應屆畢業 or 可即刻上班. Never ask a user for political affiliation.

## Source IDs

Every experience must have a non-empty `sourceId`.

- **Injected mode** — the ID must appear in the supplied `confirmed_source_ids`. If no eligible selected confirmed evidence exists, emit `records: []` and explain the exclusions in `unknowns`; do not emit an empty draft.
- **Standalone mode** — use `chat-1`, `chat-2`, … assigned in the order the user affirmed each experience. An experience the user did not affirm has no ID and must not appear. If nothing was affirmed, emit `records: []` and explain in `unknowns`.

The importer upserts one current pending draft per user, selected source-ID set, and target role supplied in invocation context. The validator's payload fingerprint excludes generation time but does not replace the target-role key.

## Consumption by the web resume builder

The platform's resume page parses the final `careertown` block out of a pasted response, tolerating surrounding prose and common formatting damage, and pre-fills its form from `data`. Because the paste is user-driven, the block must be the last thing in the response and must be valid JSON: double quotes, no trailing commas, no comments, no Markdown inside strings. Every field the schema requires must be present even when its value is `null`.

All generated resume content remains pending. Add nothing after the block.
