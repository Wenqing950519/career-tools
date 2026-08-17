# Career Town Round-Trip Contract

Each skill receives a prompt containing the user's request plus any relevant profile snapshot. Treat the snapshot as read-only context. Do not assume any persistent storage or request a transfer step.

## Response shape

Return exactly two consecutive parts:

1. A human-readable Traditional Chinese explanation.
2. One fenced block tagged `careertown` containing a single JSON object. This block is the final response content; add nothing after its closing fence.

```careertown
{
  "schema_version": 1,
  "skill": "experience-curator",
  "generated_at": "2026-08-13T10:00:00Z",
  "records": [
    {
      "type": "experience",
      "status": "pending",
      "data": {}
    }
  ],
  "unknowns": ["缺少專案期間"]
}
```

## Machine-block rules

- Conform the envelope to `output-envelope.schema.json`.
- Set `schema_version` to `1` and `generated_at` to an RFC 3339 UTC timestamp.
- Set every record `status` to `pending`, without exception.
- Validate each `data` object against the producing skill's output schema.
- Use `null` for an unknown field when that schema permits `null`. When it does not, do not invent a replacement value; preserve the gap in the record's unknown section and in top-level `unknowns`.
- Use Traditional Chinese for all user-facing strings, including strings inside the JSON, except identifiers and controlled enum values.
- Preserve source wording in the source field defined by the record schema. Do not replace it with a summary.
- Return valid JSON: double quotes, no comments, no trailing commas, and no Markdown inside JSON strings.
- Do not put a second machine-readable block elsewhere in the response.

## Import behavior

The receiving product parses only the final `careertown` block, validates the envelope and each record, and stores valid records as pending proposals. Validation failure must not partially import a response. Confirmation and rejection occur only through a later explicit user action.
