# Career Tools 平台總 PRD v1.0

> 本文件是整套平台的唯一基準。個別產品細節見 `docs/products/`，入口頁見 `docs/ENTRY_PAGE.md`。
> 取代舊的 `CAREER_TOWN_MVP_BRIEF.md`（該文件保留作為方法論與 governance 的來源，不再作為開發基準）。

---

## 1. 一句話定位

**給不知道下一步的大學生，一條從「我是誰」走到「該不該去」的路。**

統一入口：`lisheng.cv/career-tools`。五個產品各自獨立可用，但串在同一條主線上，前一步的產出是後一步的輸入。

## 2. 目標使用者

- 對未來仍不確定的大三、大四生，文組為主
- 把 AI 當 Google 用：一句話提問、不給脈絡、不追問
- 不安裝任何東西、不讀說明文件、不理解什麼是 skill 或 prompt
- 有真實的截止日壓力（實習投遞、競賽報名、offer 回覆）

**設計鐵律：使用者只做兩種動作——「填空／點選」與「複製貼上」。**
不出現的詞：JSON、schema、skill、prompt engineering、匯入、同步、安裝。

## 3. 五階段主線

| 階段 | 使用者的話 | 產品 | 形態 | 產出 |
|---|---|---|---|---|
| ① 我是誰 | 「我大三了，還不知道自己想做什麼」 | **career-test** | 純 HTML 測驗 | 求職傾向報告 |
| ② 我有什麼 | 「我大概知道方向，但不知道自己有什麼、缺什麼」 | **skill-gap** | Web app（分期：v0 零後端 → v1 LLM API + Google 登入 + DB） | 能力地圖 + 學習計畫 |
| ③ 怎麼寫出來 | 「我做過一些事，但不會寫成履歷」 | **resume-composer** | 純 skill + 單頁履歷 HTML | 可自訂版面、可匯出 PDF 的履歷 |
| ④ 投哪裡 | 「履歷有了，我要去哪找實習／競賽」 | **opportunity-catch** | 純 skill（職缺 + 競賽雙模式） | 排序過、附理由的機會清單 |
| ⑤ 該不該去 | 「我拿到 offer 了，但不知道該不該去，還是要快逃」 | **offercheck** | 純 skill（已完成） | 背調 + 取捨的 HTML 報告 |

**支線（不上平台首頁，方法論保留）：** direction-explorer、experience-curator（精華併入 resume-composer 引導流程）、interview-story、opportunity-review（由 opportunity-catch 的篩選模式取代）。

## 4. 端到端驗收情境（唯一的完成標準）

> 一個迷茫的大三生，不看任何說明文件，能獨自走完以下流程：

1. **進入入口頁**，在五句「你卡在哪裡」中認出自己，點進去。
2. **career-test**：15 分鐘內做完測驗，拿到一份看得懂的求職傾向結果，畫面明確告訴他「下一步：盤點你有什麼」。
3. **skill-gap**：把測驗結果帶入（自動或一鍵複製），盤點能力精熟度，得到一張**可截圖的能力地圖**與一份「先補哪三項、去哪學」的計畫。
4. **resume-composer**：在 ChatGPT 或 Claude 貼上觸發內容，被引導把「幫忙處理系上活動」這種模糊描述變成可量化、不編造的經歷；把結果貼進履歷 HTML，**長成一份排版好的履歷**，自訂版面後匯出 PDF。
5. **opportunity-catch**：貼上履歷重點與求職意向，選「實習」或「競賽」，拿到一份**排序過、每項附「為什麼適合你」與截止日**的清單。
6. **offercheck**：拿到 offer 後輸入公司與 JD，得到一份帶證據的評估報告，做出去或不去的決定。

### 每階段的通過條件

- 每一步的產出都是**一個看得到的東西**（報告／地圖／履歷／清單），不是一段聊天訊息。
- 每一步結束畫面都有**明確的下一步入口**。
- 任何一步單獨進入也能完整使用（沒做過前面的步驟不會被擋住，只是引導欄位要自己填）。
- 全程零安裝、零帳號（唯一例外：skill-gap v1 的 Google 登入，且 v0 不需要）。
- AI 產出遵守 governance：不編造數字、不打人格分數、推論標明是推論。

## 5. 架構總覽

```
lisheng.cv/career-tools（統一入口，靜態）
│
├─ ① career-test        純 HTML（已有，quiz + 結果頁）
├─ ② skill-gap          v0: 靜態頁 + prompt 產生器 + 貼回渲染（零後端）
│                        v1: Next.js + LLM API + Google OAuth + DB（唯一重架構）
├─ ③ resume-composer    skill（GitHub raw 觸發）+ 履歷 HTML（單檔，localStorage）
├─ ④ opportunity-catch  skill（跑在使用者自己的 Claude/ChatGPT，用其 web search）
└─ ⑤ offercheck         skill（已完成，含 HTML 報告）

獨立 v2 專案（不擋平台上線）：
- 職缺爬蟲服務（104 provider，參考 boss-zhipin-scraper 思路）
- 競賽爬蟲服務（BHuntr + WebDiscovery，見 opportunity-catch PRD 附錄）
```

**架構原則：**
1. 全平台只有 skill-gap v1 一個有後端。其他一律靜態 + skill，寫完就結束、不需維運。
2. 爬蟲不在 v1。抓取靠使用者自己的 AI（web search），平台零維運成本；爬蟲服務做好後再接進 opportunity-catch 當升級。
3. 狀態存在瀏覽器（localStorage）。跨階段傳遞用「一鍵複製上一步結果」+「貼回」，不做帳號同步（skill-gap v1 除外）。

## 6. 跨階段資料流

| 從 | 到 | 傳什麼 | 怎麼傳 |
|---|---|---|---|
| career-test | skill-gap | 傾向結果（方向 2-4 個） | 結果頁「帶著結果去盤點能力」按鈕，寫入 localStorage；跨產品時提供一鍵複製文字塊 |
| skill-gap | resume-composer | 能力清單 + 有佐證的經歷 | 能力地圖頁提供「複製給履歷生成器」文字塊 |
| resume-composer | opportunity-catch | 履歷重點摘要 + 求職意向 | 履歷 HTML 提供「複製求職摘要」按鈕 |
| opportunity-catch | offercheck | 選中的機會（公司 + JD） | offercheck 觸發 prompt 直接貼入 |

傳遞格式一律是**人看得懂的文字塊**（帶固定標題的段落），不是 JSON。機器可解析性靠固定標題 + 容錯解析達成。

## 7. 上線順序

| 波次 | 內容 | 依賴 |
|---|---|---|
| Wave 1 | resume-composer 履歷 HTML 打通（匯入 + 繁化 + 下一步導引） | 無，renderer 已存在 |
| Wave 2 | opportunity-catch skill 上線 | 無 |
| Wave 3 | 入口頁改版為五階段路徑，掛上 1-5（skill-gap 掛 v0） | Wave 1、2 |
| Wave 4 | skill-gap v0（prompt 產生器 + 能力地圖前端渲染） | 無後端 |
| Wave 5 | skill-gap v1（LLM API + Google 登入 + DB） | Wave 4 驗證有人走到這一步 |
| 平行 | 爬蟲 v2 專案（獨立 repo，獨立時程） | 不擋任何 Wave |

**Wave 1-4 全部零後端。Wave 3 完成即可對外發布整套平台。**

## 8. 成功指標

- **主線完走率**：進入任一階段的人，有多少走到下一階段（目標：每階段 ≥ 30%）
- **產出分享**：能力地圖／履歷／機會清單被截圖分享的次數（質性觀察 Threads/IG/Dcard）
- **回訪**：skill-gap v1 上線後，7 日內回來更新能力地圖的比例
- 明確**不是**指標：GitHub star、prompt 複製次數、頁面停留時間

## 9. 不做的事（v1）

- 自動投遞履歷
- 大規模爬蟲、登入求職平台代抓
- 人格測驗式的適配演算法、任何形式的「適合度打分」
- 社群、留言、多人協作
- App、瀏覽器擴充
- career-test 以外的階段做遊戲化（XP、徽章、排行榜）

## 10. Governance（全產品共同遵守）

沿用 `skills/_shared/governance.md` 八條，對使用者的呈現方式：

- AI 不編造任何數字、頭銜、規模——這是平台的招牌，行銷素材直接打這點
- 推論一律標示「這是從你哪句話推論的」
- 所有 AI 產出預設是草稿，使用者確認才算數
- 方向與能力呈現「目前狀態」，永不呈現「你適合什麼」的裁決
