# Output Contract

Return Traditional Chinese prose followed by one final `careertown` JSON block validating against `schemas/envelope.schema.json`.

Use `schema_version: 1`, `skill: "interview-story"`, a UTC timestamp, one pending `interview_story` record, and unique unknowns.

Map to the existing experience shape:

- `id`: reuse an injected story ID. Otherwise use `story:<source experience ID>:<exact question type>`. Never generate a random ID.
- `title`: target question type plus source episode title.
- `raw_text`: preserve the source experience wording.
- `summary`: one neutral sentence describing the story's focus.
- `skills`: supported methods used in the source.
- `resume_text`: the generated spoken STAR version.
- `confirmation_status`: always `pending`.
- `created_at`: generation timestamp.
- `source`: source experience ID.
- `sections`: retain supported background, actions, results, contribution, and unknowns.

When the selected source is not confirmed or the question type is absent, emit `records: []` and explain the ineligible input in `unknowns`. Otherwise emit exactly one record. Likely follow-up points appear in the human report. Unanswered follow-ups that expose missing facts also appear in envelope `unknowns`. Add nothing after the block.
