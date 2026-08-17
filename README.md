# Career Tools

給大學生的求職工具箱。從「我大三了，還不知道自己想做什麼」，走到「有依據地決定該不該去」。

統一入口：**[lisheng.cv/career-tools](https://lisheng.cv/career-tools/)**

不用安裝、不用註冊、會複製貼上就會用。

這個 repo 是**平台總庫**：產品規格、共用規則、履歷生成器網頁基底，以及尚未上平台的支線 skill。四個平台 skill 各自獨立在自己的 repo。

---

## 五個階段

| 階段 | 你的處境 | 產品 | Repo |
| --- | --- | --- | --- |
| ① 我是誰 | 「我大三了，還不知道自己想做什麼」 | career-test 小測驗 | 網頁 |
| ② 我有什麼 | 「我大概知道方向，但不知道自己有什麼」 | 找差距 | [career-skill-gap](https://github.com/Wenqing950519/career-skill-gap) |
| ③ 怎麼寫出來 | 「我做過一些事，但不會寫成履歷」 | 打履歷 | [career-resume-composer](https://github.com/Wenqing950519/career-resume-composer) |
| ④ 投哪裡 | 「履歷有了，我要去哪找實習／競賽」 | 抓機會 | [career-opportunity-catch](https://github.com/Wenqing950519/career-opportunity-catch) |
| ⑤ 該不該去 | 「我拿到 offer 了，該去嗎，還是快逃」 | 選 offer | [career-offercheck](https://github.com/Wenqing950519/career-offercheck) |

每一步的產出都接得上下一步。從哪裡開始都可以。

## 這裡的 AI 有三條規矩

1. **不會幫你編造任何數字**——寫不出來的，它會反問你，而不是幫你掰
2. **不會給你「你適合當 XX」的判決**——只給你可以驗證的下一步
3. **每個結論都說得出「是從你哪句話推論的」**

這三條不是文案，是寫進每個 skill 的硬性規則。完整版見 [`skills/_shared/governance.md`](skills/_shared/governance.md)。

## 這個 repo 有什麼

```
docs/
├─ PLATFORM_PRD.md      平台總規格：五階段、端到端驗收情境、上線波次
├─ ENTRY_PAGE.md        入口頁改版規格
├─ COMPUTE_TIERS.md     各 skill 的運算成本分級
├─ MIGRATION.md
└─ products/            五個產品的個別 PRD
skills/
├─ _shared/             共用 governance 與 round-trip 契約
└─ ...                  四個支線 skill（見下）
assets/
└─ resume-builder-base.html   履歷生成器網頁基底
```

想了解整套設計，從 [`docs/PLATFORM_PRD.md`](docs/PLATFORM_PRD.md) 開始。

## 支線 skill

方法論保留，但依收斂決策不上平台首頁：

| Skill | 中文 | 產出 |
| --- | --- | --- |
| [`direction-explorer`](skills/direction-explorer) | 挖方向 | 2–4 個職涯方向假設與 30 分鐘驗證行動 |
| [`experience-curator`](skills/experience-curator) | 寫經歷 | 五段式經歷證據與貢獻邊界（精華已併入打履歷） |
| [`opportunity-review`](skills/opportunity-review) | 評機會 | 單一機會的硬條件與多軸檢視 |
| [`interview-story`](skills/interview-story) | 說故事 | 可口說的 STAR 故事與誠實邊界 |

## 怎麼用這些 Skill

每個 skill 是一份純文字指令，貼進 ChatGPT、Claude 或任何 LLM 就能用，不需要安裝任何東西。

1. 打開 skill 資料夾，複製 `SKILL.md` 的內容
2. 貼到 AI 對話框，接著描述你的狀況
3. 照它問的回答

Claude 使用者也可以把整個資料夾放進 `.claude/skills/`。

## 驗證

每個 round-trip skill 都附驗證器，確認輸出符合契約：

```bash
cd skills/direction-explorer && python scripts/validate_response.py examples/output-01.md
```

---

Made by [Li-Sheng](https://lisheng.cv)
