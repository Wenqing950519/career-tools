# ③ resume-composer — 履歷生成器

**形態**：純 skill（貼到任何 LLM 觸發）＋ 單頁履歷 HTML（自訂版面、匯出 PDF）
**階段**：怎麼寫出來 ／「我做過一些事，但不會寫成履歷」
**架構重量**：零後端；renderer 基底已存在（`简历生成器-原木优化.html`，6208 行）

## 目的

兩段式閉環：

1. **Skill 端（在使用者的 ChatGPT/Claude 裡）**：引導使用者把模糊經歷（「幫忙處理系上活動」）變成可量化、**不編造**的履歷語言。併入 `experience-curator` 的精華：先問「你實際做了什麼、哪部分是你自己做的、有沒有任何可數的東西」，才動筆改寫。
2. **HTML 端（瀏覽器）**：把 AI 產出貼進來 → 自動長成排版好的履歷 → 自訂版面 → 匯出 PDF。

**使用者的完整動線**：複製觸發內容 → 貼到 AI → 對話幾輪 → 全選複製 AI 最後一則回覆 → 貼進履歷頁的匯入框 → 履歷出現 → 微調 → 下載 PDF。

## Skill 端規格

### 基底
沿用 `skills/resume-composer/`（SKILL.md、governance、output-contract、schema 均已存在）。

### 要改的三件事

1. **鬆綁 sourceId 前置條件**。現行 contract 要求每段經歷有 confirmed sourceId（為 Career Town 匯入設計）。平台版沒有 confirmed 資料庫，改為：skill 內建 experience-curator 式的訪談引導，在對話中完成「使用者確認」——AI 改寫後必須問「這樣寫有沒有超過事實？」，使用者說沒有，該段才進最終輸出。`sourceId` 改為對話內自生的 `chat-1`、`chat-2`。
2. **輸出雙格式**：先繁中散文（給人看、確認用），最後一個 ```careertown JSON block（給 HTML 匯入用，結構見下）。此順序已是現行 contract，不變。
3. **量化紀律具體化**（寫進 references/）：
   - 有可數的東西 → 問到數字（幾人、幾週、幾篇、多少預算）
   - 沒有可數的東西 → 用範圍或頻率（「每週 2 篇」），仍不可捏造
   - 完全問不出 → 該句保持質性描述並標註，**寧可不量化也不編造**——這是產品招牌

### 觸發方式
- 入口頁提供一鍵複製的觸發 prompt（內嵌 GitHub raw SKILL 連結 + 內容），貼到 ChatGPT 或 Claude 即啟動
- Claude 使用者可另外安裝為正式 skill（進階選項，不是主路徑）

## HTML 端規格

### 基底選擇
以 `简历生成器-原木优化.html` 為基底（不是 career-test 的 `ResumeBuilder.tsx`）。理由：前者已有即時預覽、html2pdf 匯出、localStorage 歷史、多版面能力；後者只有 192 行表單。**ResumeBuilder.tsx 退役**，`/resume` 路由改掛新單頁。

### 改造清單

| # | 項目 | 說明 |
|---|---|---|
| 1 | **簡轉繁** | 全 UI 文案 zh-CN → zh-TW（简历→履歷、导出→匯出…），`lang="zh-TW"`，字型改 Noto Sans TC / Noto Serif TC |
| 2 | **欄位在地化** | `politicalStatus`（政治面貌）→ `status`（狀態：可即刻上班／應屆／延畢…，自由填）；schema 欄名保留 `politicalStatus` 不動（避免破壞既有 skill schema），僅 UI label 改 |
| 3 | **貼上匯入**（核心新增） | 頁首新增「從 AI 匯入」摺疊區：一個大貼上框 + 「匯入」按鈕。解析規則見下節 |
| 4 | **移除簡中特有內容** | 「成長的痕跡」漫畫小冊等與主線無關的模組評估移除或隱藏，維持單一任務：做履歷 |
| 5 | **求職語言庫** | `job_language_lib.js` 的線上更新機制保留但改為選配；預設走內建庫，避免對外部檔案的依賴造成載入失敗 |
| 6 | **求職摘要按鈕** | 履歷完成後提供「複製求職摘要」：姓名以外的匿名重點（教育、能力、經歷一句版、意向），餵給下一步 opportunity-catch |
| 7 | **下一步導引** | 匯出 PDF 成功的 toast 之後，顯示「履歷好了，下一步：找機會」→ opportunity-catch |
| 8 | **CDN 依賴內嵌** | html2pdf.js 與字型改為本地 vendor 或保底降級（列印模式），單檔在無網路下仍可用 |

### 匯入解析規格（容錯優先）

使用者貼的是**整段 AI 回覆**，不是乾淨 JSON。解析順序：

1. 找**最後一個** ```careertown fenced block → `JSON.parse`
2. 失敗 → 剝常見雜訊再試：block 前後的散文、結尾逗號、全形引號、`json` 語言標記
3. 再失敗 → 掃描全文任何 `{...}` 平衡括號段落逐一嘗試
4. 全部失敗 → **不白屏**：顯示「沒抓到結構化資料」+ 把貼上內容按行呈現，提供「手動填表」入口，並給一句可複製的話讓使用者丟回 AI：「請把剛才的履歷內容用 careertown JSON 格式重新輸出一次」

匯入成功後：欄位逐一填入表單、`null` 欄位留空、未知 category 落到「校園經歷」並標示，立即觸發即時預覽。**匯入永遠是預填，使用者可改任何一格。**

### 資料模型對齊（現狀落差清單）

| 欄位 | skill schema | 原木 HTML | career-test RB | 決議 |
|---|---|---|---|---|
| 經歷分類 | 實習經歷／實踐經歷／校園經歷 | 实习／实践／校园 | 實習/工作經歷／項目經歷／校園經歷 | **以 skill schema 三值為準**，HTML 繁化時對齊，RB 退役 |
| politicalStatus | 有 | 有（政治面貌） | 無（status） | 欄名保留，UI label 改「狀態」 |
| sourceId | 必填 confirmed | 無 | 無 | skill 端改為對話內確認（見上），HTML 端忽略此欄 |
| photo | nullable string | dataURL + 獨立 key | dataURL | 沿用原木 HTML 的獨立 PHOTO_KEY 存法（省 localStorage） |

## 驗收

- 一個沒讀說明的人：入口頁複製 → ChatGPT 對話 → 整段回覆貼進 `/resume` → 3 秒內看到排版好的履歷 → 匯出 PDF 成功
- AI 對話中出現使用者沒說過的數字時，skill 會主動退回追問，最終 JSON 不含未確認數字
- 匯入框貼入任意垃圾文字不會白屏
- 匯出的 PDF 一頁式、列印正常、照片不變形
