# Output Contract

Traditional Chinese. List of 8–12 opportunity cards, then exactly one summary block. No JSON. Nothing after the summary block.

## Opportunity card (per item)

```
### {#}. {名稱} — {公司／主辦}
截止：{日期}（{官方確認｜⚠️ 未確認，請點官網核對}）
資格：{在學要求／地點／組隊}
連結：{canonical URL}
為什麼排這裡：{必須引用使用者的話或履歷摘要行，說明對上哪段經歷}
缺什麼：{JD/簡章要求但使用者未提及的項目；沒有就寫「以你提供的資訊看不出明顯缺口」}
注意：{可選；薪資未揭露、需作品集、報名與繳件是兩個日期等提醒}
```

Jobs additionally include 地點／遠端 and 關鍵要求 lines; competitions additionally include 獎金 and 繳交物 lines when known. Unknown facts are written as 未查到, never guessed.

## Summary block (exactly one, at the end)

```
## 本次結果摘要
搜尋時間：{YYYY-MM-DD}
模式：{實習／職缺｜競賽}
候選數：{n}（已濾除 {x} 個過期、{y} 個資格不符{、z 個不符硬條件}）
建議先看：{#a、#b}（一句理由）
深入確認：挑 2–3 個回覆編號，我會到官方頁面確認細節
下一步：{見下方 mode-specific 規則}
```

### Next-step line by mode

**Mode A (jobs/internships)** — hand off to offercheck, which is scoped to a single internship or job offer decision:

```
下一步：等你拿到 offer，用 offercheck 評估該不該去——複製下面這段開始：
「請用 offercheck 幫我評估：{公司}，職缺：{名稱}，連結：{URL}」
```

**Mode B (competitions)** — do **not** hand off to offercheck. It only evaluates employment offers; a competition is not an offer and falls outside its stated scope. Close with the deadline action instead:

```
下一步：把 #{a}、#{b} 的報名截止日記到行事曆，並確認組隊人數與繳交物。要我幫你細看某一個的簡章就回覆編號。
```

## Prohibitions

- No numeric fit scores, no percentages, no 適合度
- No expired items anywhere in the output
- No opportunity without a URL
- Removal reasons for every filtered-out category, by count and rule
