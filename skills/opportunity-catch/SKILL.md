---
name: opportunity-catch
description: Search current Taiwan internships, jobs, or student competitions with live web search, filter by the user's hard constraints, deduplicate, and rank with traceable reasons tied to the user's own words. Use when the user has a resume summary or a stated intent and wants concrete opportunities to apply to. Do not use for application submission, resume writing, offer evaluation, or any fit scoring of the person.
---

# Opportunity Catch（抓機會）

Find live opportunities, kill expired ones, and rank with reasons the user can trace to their own words.

Read [references/governance.md](references/governance.md), then [references/catch-method.md](references/catch-method.md), then [references/sources.md](references/sources.md), then [references/output-contract.md](references/output-contract.md).

## Process

1. Ask exactly one opening question: 「你現在要找的是：A 實習／職缺，還是 B 競賽？」
2. Read the pasted resume summary (from the resume tool) if provided. If absent, ask at most three questions: direction, location constraint, student status. Then proceed; never demand a resume first.
3. Separate hard constraints (location, eligibility, language, student status) from preferences (remote, industry, prize size). Hard constraints eliminate; preferences only rank.
4. Run web search per [references/sources.md](references/sources.md) for the chosen mode. Collect 12–20 candidates before filtering.
5. Discard every opportunity whose deadline has passed. Mark unverifiable deadlines as ⚠️ 未確認. Never present an expired opportunity.
6. Deduplicate across sources; keep the official URL as canonical.
7. Filter by hard constraints and state what was removed and why.
8. Rank the survivors. Every rank reason must quote or paraphrase something the user actually said. Never output a numeric fit score.
9. Present 8–12 results. Offer deep verification: 「挑 2–3 個你有興趣的，我去官方頁面確認細節。」Deep-verify only what the user picks.
10. Close with the summary block defined in [references/output-contract.md](references/output-contract.md), using the next-step line that matches the mode. Hand off to offercheck only in job mode; offercheck evaluates employment offers and does not cover competitions.

## Output

Traditional Chinese list, one card per opportunity with the fields defined in the output contract, followed by exactly one 本次結果摘要 block. No JSON. No text after the summary block.
