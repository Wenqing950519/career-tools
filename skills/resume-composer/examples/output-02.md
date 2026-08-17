# Example output — standalone mode

已確認的兩段經歷（皆由你在對話中親自確認）：

**chat-1 — 系學會迎新活動（校園經歷）**
你負責的是文案與報名表單，場地與預算由其他夥伴負責，所以這段只寫你自己做的部分。報名 130 餘筆是你提供的數字，籌備六週也是你說的，兩者都保留原值。

**chat-2 — 系學會粉專經營（校園經歷）**
這段是你獨立負責，所以動詞可以用「經營」。粉專從 200 餘人成長至近 900 人、每週約兩篇，都是你提供的數字。你自己把「大幅成長」改成實際數字，最終版本以你改過的為準。

未納入的內容：

- 迎新活動是否帶動社團招募成長——你表示不知道，因此沒有寫進成果，也沒有用任何替代說法補上。
- 場地與預算的執行——不是你負責的部分，依貢獻邊界排除。

尚未解決的欄位：姓名以外的個人資料、學校、科系全名、電話、電子郵件、居住城市、證照與技能、興趣，你都還沒提供，這些保留空值，你可以在履歷頁直接補。粉專經營的起訖月份你只說「三個學期」，沒有具體月份，時間欄先寫你說的範圍。

```careertown
{
  "schema_version": 1,
  "skill": "resume-composer",
  "generated_at": "2026-08-17T12:00:00Z",
  "records": [
    {
      "type": "resume_draft",
      "status": "pending",
      "data": {
        "photo": null,
        "name": null,
        "birthDate": null,
        "phone": null,
        "politicalStatus": null,
        "email": null,
        "city": null,
        "certifications": null,
        "skills": null,
        "hobbies": null,
        "education": [
          {
            "school": null,
            "major": null,
            "degree": null,
            "time": null,
            "details": null
          }
        ],
        "experiences": [
          {
            "category": "校園經歷",
            "title": "系學會迎新活動",
            "role": "文案與報名流程",
            "time": "2025 年 9 月（籌備約六週）",
            "details": "與兩名同學共同籌辦系上迎新活動，個人負責活動文案撰寫與報名表單設計及維護，最終收得 130 餘筆報名。場地與預算由其他夥伴負責。",
            "sourceId": "chat-1"
          },
          {
            "category": "校園經歷",
            "title": "系學會社群粉專經營",
            "role": "獨立經營",
            "time": "三個學期",
            "details": "獨立負責系學會社群粉專的內容規劃與發布，維持每週約兩篇貼文；接手時追蹤人數 200 餘人，卸任時接近 900 人。",
            "sourceId": "chat-2"
          }
        ]
      }
    }
  ],
  "unknowns": [
    "缺少姓名、生日、電話、電子郵件與居住城市",
    "缺少學校、科系與學位資料",
    "缺少證照、技能與興趣欄位內容",
    "粉專經營缺少具體起訖月份，僅有「三個學期」的敘述",
    "迎新活動是否影響社團招募成果，使用者表示不知道，未納入"
  ]
}
```
