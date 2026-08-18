# Career Tools

給大學生的求職工具箱。從「我大三了，還不知道自己想做什麼」，走到「有依據地決定該不該去」。

統一入口：**[lisheng.cv/career-tools](https://lisheng.cv/career-tools/)**

不用安裝、不用註冊、會複製貼上就會用。

這個 repo 是**平台總庫**：產品規格、共用契約與網頁應用。四個 skill 各自獨立在自己的 repo。

---

## 五個階段

| 階段 | 你的處境 | 產品 | 在哪裡 |
| --- | --- | --- | --- |
| ① 我是誰 | 「我大三了，還不知道自己想做什麼」 | 小測驗 | 網頁 |
| ② 我有什麼 | 「我大概知道方向，但不知道自己有什麼」 | 找差距 | [skillmap.lisheng.cv](https://skillmap.lisheng.cv) ＋ [career-skill-gap](https://github.com/Wenqing950519/career-skill-gap) |
| ③ 怎麼寫出來 | 「我做過一些事，但不會寫成履歷」 | 打履歷 | [career-resume-composer](https://github.com/Wenqing950519/career-resume-composer) ＋ [`apps/resume`](apps/resume) |
| ④ 投哪裡 | 「履歷有了，我要去哪找實習／競賽」 | 抓機會 | [career-opportunity-catch](https://github.com/Wenqing950519/career-opportunity-catch) |
| ⑤ 該不該去 | 「我拿到 offer 了，該去嗎，還是快逃」 | 選 offer | [career-offercheck](https://github.com/Wenqing950519/career-offercheck) |

每一步的產出都接得上下一步。從哪裡開始都可以。

## 這裡的 AI 有三條規矩

1. **不會幫你編造任何數字**——寫不出來的，它會反問你，而不是幫你掰
2. **不會給你「你適合當 XX」的判決**——只給你可以驗證的下一步
3. **每個結論都說得出「是從你哪句話推論的」**

這三條不是文案，是寫進每個 skill 的硬性規則。完整版見 [`contracts/governance.md`](contracts/governance.md)。

實際執行的例子：履歷生成器原本內建三個「一鍵潤色」功能，它們會憑空生出「提升約 20%」「修復核心缺陷 20 餘項」「帶領 5 人團隊」，並把使用者寫的「協助」改寫成「主導」。這些功能已全數移除，改由 [打履歷 Skill](https://github.com/Wenqing950519/career-resume-composer) 承接——它會反問你到底有沒有數字，問不出來就保持質性描述。

## 這個 repo 有什麼

```
docs/
├─ PLATFORM_PRD.md      平台總規格：五階段、端到端驗收情境、上線波次
├─ ENTRY_PAGE.md        入口頁改版規格
├─ COMPUTE_TIERS.md     各 skill 的運算成本分級
└─ products/            五個產品的個別 PRD
contracts/
├─ governance.md              全平台共同遵守的八條規則
├─ round-trip.md              skill 回應與匯入的交換契約
└─ output-envelope.schema.json
apps/
├─ index.html            入口頁：五階段路徑
├─ shared/platform.css   共用樣式
├─ opportunity-catch/    抓機會的 prompt 產生器
└─ resume/               履歷生成器網頁（單檔，可離線使用）
```

**這個 repo 零後端、零建置**：下載下來用瀏覽器打開就能跑。唯一需要後端的第 ② 步已經獨立成 [skillmap](https://github.com/Wenqing950519/skillmap)，跑在自己的子網域上。

想了解整套設計，從 [`docs/PLATFORM_PRD.md`](docs/PLATFORM_PRD.md) 開始。

## 能力地圖

搬到自己的 repo 與子網域了：**[skillmap.lisheng.cv](https://skillmap.lisheng.cv)**（原始碼：[skillmap](https://github.com/Wenqing950519/skillmap)）。

它是全平台唯一有後端的產品——Google 登入、資料庫、LLM API proxy 都在那邊，所以不放在這個純靜態的總庫裡。不用登入的複製貼上版也在同一個站上，是登入版的永久降級路徑。

## 履歷生成器

[`apps/resume/index.html`](apps/resume/index.html) 是單一檔案，直接用瀏覽器開就能用，資料只存在你自己的瀏覽器裡。

它接上第 ③ 步的打履歷 Skill：跟 AI 聊完之後，把整段回覆貼進「從 AI 匯入」，表單會自動填好。貼進去的內容格式亂掉也沒關係，解析器會盡量挖，挖不到會把原文排好給你手動填，不會白屏。

`convert_tw.py` 是簡轉繁的轉換腳本，可重複執行，帶有守衛檢查（會擋下破壞儲存鍵或經歷分類列舉值的轉換）。

---

Made by [Li-Sheng](https://lisheng.cv)
