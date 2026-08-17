# Migration

| Legacy capability | Current destination |
| --- | --- |
| Onboarding direction follow-up | `direction-explorer` |
| One-experience evidence curation | `experience-curator` |
| Market-requirement lane from direction mapping | `skill-gap` |
| Evaluation portion of opportunity radar | `opportunity-review` |
| Confirmed-evidence resume composition | `resume-composer` |
| Spoken interview preparation formerly mixed into resume work | `interview-story` |
| Deep internship offer evaluation | `offercheck` |

Journal-only capture remains a website input. Direction projection is deterministic front-end logic. Opportunity discovery belongs to backend adapters. Persistence and confirmation belong to authenticated product APIs.

The weaker round-trip `offer-decision` was removed after comparative testing. `offercheck` was retained because it has materially stronger evidence traceability, schema enforcement, validation, and decision depth. Its scored final report is an explicit exception to the six round-trip skills' pending-only contract and requires an artifact-capable agent environment.
