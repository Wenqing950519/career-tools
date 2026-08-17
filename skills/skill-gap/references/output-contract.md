# Output Contract

Return Traditional Chinese prose followed by one final `careertown` JSON block validating against `schemas/envelope.schema.json`.

The prose is not free-form. The platform's capability map parses it directly, so it must follow the block structure below. Both consumers are served by one response: humans read the prose, the web app parses the same prose, and Career Town imports the JSON block.

## Prose structure

### 1. Opening line (strength first)

One sentence stating what the user already has before any gap is named.

```
你已經有 11 項能力在路上（熟練 3、初學 8），另外 7 項等你決定要不要碰。
```

### 2. Capability blocks

One block per capability, ordered 精通 → 熟練 → 初學 → 待學習. Use these exact headings; omit a line only when the contract below allows it.

```
### 能力：簡報（課堂／提案場合）
自評線索：（引用使用者原話）「系學會成發是我上台報告的」
建議精熟度：初學
學習感受：有興趣
差距：目標「數位行銷實習」常要求對客戶提案，你的經驗在校內場合
```

- `能力：` one independently ratable capability, granularity rules in `gap-method.md`. A cluster name may appear as a `##` grouping heading above several blocks, never as the capability itself.
- `自評線索：` quote the user's own wording. When the user gave an explicit rating instead of a narrative, write `使用者已自評`.
- `建議精熟度：` one of 待學習｜初學｜熟練｜精通. This is a suggestion awaiting the user's confirmation, never a rating on the user's behalf. When the user already gave an explicit rating, use the heading `目前自評：` instead of `建議精熟度：`.
- `學習感受：` preserve the user's description of readiness, interest, or resistance. Write `未提及` when absent.
- `差距：` phrased as something addable. Write `以你提供的資訊看不出明顯缺口` when there is none.
- `證據：` optional extra line, present only when confirmed evidence exists; cite the evidence and what it demonstrates.

Never write a number, percentage, decimal, or score anywhere in a capability block.

### 3. Prioritized gaps and source limits

After the blocks, give the prioritized gap order with one minimum validation action each, and state what the market-requirement lane was based on and how confident it is.

## Machine block

The envelope uses `schema_version: 1`, `skill: "skill-gap"`, a UTC timestamp, pending `skill` records, and unique unknowns.

Map each record to existing fields:

- `id`: reuse an injected capability ID; otherwise use `skill:<exact capability title>`. Never generate a random ID.
- `title`: capability name, identical to the prose block's `能力：` value.
- `level`: the user's explicit 1–4 self-rating only.
- `learning_feeling`: preserve the user's description of readiness or uncertainty.
- `related_directions`: target direction IDs or supplied labels.
- `evidence_ids`: confirmed evidence IDs only.
- `assessment_note`: keep market requirement, source status, gap interpretation, and `high|medium|low` action priority visibly separated.
- `next_practice`: one minimum validation action.
- `updated_at`: generation timestamp.

A `建議精熟度` suggestion is not a self-rating and must not become a record. If no explicit level exists for any capability, emit `records: []`, explain in prose and `unknowns`, and do not manufacture a level — the prose blocks still carry the full map for the web app to render as unconfirmed cards. Empty records are therefore a valid guarded response. Add nothing after the block.
