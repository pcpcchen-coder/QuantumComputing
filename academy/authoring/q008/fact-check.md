# Q008 事實查核

查核日：2026-11-18。查核者：製作代理（Claude）。逐字引文見 `source-notes.md`。
方法：維基百科三頁由製作代理以擷取工具開啟，工具回報逐字引文（未記錄 oldid）；學程簡報 QC_Operation_Talk 第 10 頁、basic-circuits 第 10–12 頁與 3D 場景程式由製作代理讀取；古典最高勝率由製作代理列舉全部 16 種固定策略重算（最多贏 4 種情況中的 3 種）。
限制：本集不推導量子策略的測量角度，也不談貝爾定理的詮釋；「神祕骰子」是比喻。

| # | 本集的說法（幕） | 依據 | 結論 |
|---|---|---|---|
| 1 | 單看一顆完全隨機；兩顆對答案每次都一樣（3、4） | 簡報 G p10：「單獨量任一顆：50% / 50%」「兩顆一起量：結果永遠相同（00 或 11）」；Entanglement：perfectly correlated | 相符 |
| 2 | 資訊不在任何一顆，而在兩顆的關聯裡（3） | 簡報 G p10 標題「糾纏：資訊存在『關聯』裡」；Entanglement：state of each particle cannot be described independently | 相符 |
| 3 | 貝爾態兩步：先疊加，再用兩位元閘讓第二顆跟著走（4） | basic-circuits p10：H（q0）→ CNOT（q0 → q1）→ (|00⟩+|11⟩)/√2 | 相符 |
| 4 | 一起量只得到零零或一一，各一半，不會出現零一或一零（4） | basic-circuits p10–11：「只剩 00、11」 | 相符（Φ⁺ 貝爾態） |
| 5 | 量一顆不能傳訊息；對方看到的仍是一半一半（5、6） | No-communication theorem：impossible for one observer to transmit information；簡報 G p10 備註 | 相符 |
| 6 | 要對答案才看得出關聯，而對答案的方式不會比光快（5、6） | No-communication theorem：does not violate special relativity；Entanglement：cannot be used for faster-than-light communication | 相符 |
| 7 | 合作遊戲規則：各自隨機拿到紅卡或藍卡，不能溝通；兩張藍卡答案不同才贏，其他情況答案相同才贏（7） | CHSH game：隨機 x、y；回答 a、b；贏的條件 a⊕b = x∧y；forbidden from directly communicating（紅＝0、藍＝1） | 相符 |
| 8 | 永遠答零，四種情況贏三種（8） | 00⊕00 = 0：x∧y = 0 的三種情況都贏，只輸兩張藍卡 | 相符 |
| 9 | 不用量子，勝率最高四分之三（8、10） | CHSH game：impossible to win with probability higher than 75%；製作代理列舉 16 種策略，最多贏 3/4 | 相符 |
| 10 | 用糾纏，勝率約百分之八十五（8、12） | CHSH game：~85%、cos²(π/8) ≈ 0.854 | 相符 |
| 11 | 3D 動畫按「Bell 態」，上排箭頭縮成一點（展示段） | animations/js/operation/04_register.js desc 與「Bell 態」按鈕 | 相符 |

## 課程

- 主題、學習目標、動手任務（父子分開回答的合作遊戲）、孩子獨立改造（自己想古典策略算勝率）、好玩機制（角色交換）、作品（CHSH 遊戲勝率表）與 120 分鐘流程依 `academy/lessons/Q008/lesson.json` 核對。
- 旁白不念英文縮寫：CHSH 遊戲改說「合作遊戲」；Bell 態說「貝爾態」。教材第一次出現時註明 CHSH。
- 兩人版玩法（各自從自己的牌堆抽卡）保留「隨機、互不知道」兩個條件，和 CHSH 遊戲等價。
- 沒有課堂錄音；未虛構孩子作品或對話。
