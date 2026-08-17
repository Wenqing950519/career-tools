# Evidence Method

## Unit of work

Handle one bounded episode: one internship assignment, project, competition, research effort, club activity, volunteer activity, or job episode. If the input mixes episodes, curate the clearest one and list the boundary as an unknown instead of merging unrelated claims.

## Five sections

Map supported content into these exact arrays:

1. `background` — setting, organization, timeframe, purpose, and relevant context.
2. `actions` — responsibility, personal actions, tools, methods, decisions, and handoffs.
3. `results` — observable outcomes supported by the user's words; process outputs are valid when outcome metrics are absent.
4. `contribution` — what the user did, what the team or mentor did, and which ownership boundary remains unclear.
5. `unknowns` — unresolved date, title, duration, scale, audience, metric, attribution, ownership, or result.

Do not put a missing fact into another section as if it were known. Do not use empty praise such as “excellent performance” as a result.

## Contribution tests

- Preserve the user's verb strength.
- Separate “I did” from “we did.”
- Attribute a team result to the team unless individual causality is supported.
- Treat tools as methods used, not proof of proficiency.
- Treat participation as evidence of exposure, not mastery.
- When ownership is ambiguous, state the observed action and add ownership to `unknowns`.

## Derived fields

- `title`: use the user's stated episode name; otherwise use a neutral descriptive title based only on known context.
- `summary`: write one compact neutral sentence.
- `skills`: include only explicitly used skills or methods; do not rate them.
- `resume_text`: provide conservative candidate wording from supported facts. It remains generated text, not confirmed evidence.
- `source`: identify the supplied source generically, such as `user_statement` or a label present in the injected context.
- `created_at`: use response generation time, not an inferred event date.

If a later turn adds facts, preserve the earlier raw wording and add the new wording rather than rewriting history.
