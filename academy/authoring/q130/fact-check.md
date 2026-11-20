# Q130 事實查核

查核日：2026-11-18。查核者：製作代理（Claude）。逐字引文見 `source-notes.md`。
方法：LRZ／IQM 論文（arXiv:2509.12949）由製作代理讀取 HTML 全文；維基百科兩頁（Uninterruptible power supply、Dilution refrigerator）讀原始 wikitext；學程「技術分享：量子電腦的供電設計」簡報第 7、8 頁（含講者備註）、供電文獻回顧 §2 與 §6、兩個互動動畫的程式由製作代理讀取；備援案例由製作代理實際執行 `outage_timeline.py`。
執行環境：Python 3.13.18，無外部套件，結果固定（無亂數）。
限制：2 分鐘、2–5 天是 LRZ 一台 20 位元系統的經驗；發電機＋ATS 10–30 秒與 UPS 設計原則是學程文件的推論；動畫曲線為教學示意。

| # | 本集的說法（幕） | 依據 | 結論 |
|---|---|---|---|
| 1 | 上一課：電從哪裡來、到哪裡去（1） | academy/lessons/Q129/brief.md「電從哪裡來、到哪裡去」 | 相符 |
| 2 | 冷卻停兩分鐘晶片回溫，之後兩到五天才能重新降溫、校準好（1、4、12） | LRZ §3.6「two minutes to exceed this temperature」「two to five days」；簡報 p7 | 相符 |
| 3 | 好玩機制故障注入；作品斷電時間軸與處置卡（2、9、10） | 課綱 lesson.json | 相符 |
| 4 | 稀釋冷凍機維持在只比絕對零度高約百分之一度（約 10 mK）（3） | LRZ「normal 10 mK operating temperature」；Dilution refrigerator 頁（可到 2 mK） | 相符 |
| 5 | 冷卻鏈三環：脈衝管壓縮機、氣體處理系統、冰水機與泵浦（3） | 簡報 p8「壓縮機、GHS、冰水機泵浦與控制」；文獻回顧 §2；pe#monitor 壓縮機水溫聯鎖 | 相符 |
| 6 | 任何一環停下，熱抽不走、溫度上升（3） | LRZ「Once active cooling ceases…」；pe#monitor 冷卻水中斷 → 停壓縮機 → 各級升溫 | 相符 |
| 7 | 德國一座超算中心把二十位元超導量子電腦放進機房實際運轉（4） | LRZ 摘要「superconducting 20-qubit quantum computer into the HPC infrastructure at LRZ」 | 相符（未採用文獻回顧的「一年多」） |
| 8 | 約兩分鐘超過一克耳文；重新降溫兩到五天，最壞約十天（4） | LRZ §3.6 與結論「up to ten days」；簡報 p7 | 相符 |
| 9 | 真空通常撐好幾週，損失的是停機與重新校準時間，不是硬體（4） | LRZ「vacuum integrity…maintained during outages for several weeks」；簡報 p7 | 相符 |
| 10 | 一克耳文以下大部分校準狀態保得住；超過要整套重新校準（5） | LRZ「calibration state…largely maintained if…below 1K」；結論「full calibration after cooldown」 | 相符 |
| 11 | 降到零點一克耳文以下才能開始校準（5） | LRZ「Once the system is below 100 mK…recalibration…can occur」；簡報 p7 | 相符 |
| 12 | 不斷電系統靠電池幾乎立刻接手（6） | UPS 頁「near-instantaneous protection…energy stored in batteries」 | 相符 |
| 13 | 發電機起動加自動切換開關約十到三十秒，比兩分鐘短（6） | 文獻回顧 §2【推論】；簡報 p8 講者備註 | 相符（學程文件推論） |
| 14 | 不斷電系統的任務是撐到發電機接手（6、12） | 文獻回顧 §2「UPS 的任務是撐到發電機接手」；簡報 p8；UPS 頁「sufficient to start a standby power source」 | 相符（推論） |
| 15 | 動畫三種方案 A／B／C 的定義（7） | power1000.html#outage select 三個選項 | 相符 |
| 16 | 要保護的是冷卻鏈連續運轉，不是每台儀器都要長時間備援（8） | 課綱常見誤解；簡報 p8「涵蓋整條冷卻鏈…不能只顧控制電子」 | 相符 |
| 17 | 冰水機是關鍵負載：冷卻水太熱，低溫泵浦會跳機；蓄冷水槽讓泵浦繼續循環（8） | LRZ「cooling water temperature exceeding the upper temperature limit, triggering a shutdown of the cryogenic pumps」；簡報 p7、p8 | 相符（蓄冷桶為推論） |
| 18 | 壓縮機啟動電流大，UPS 容量要一起算；軟啟動或變頻可小一個級距（8） | 簡報 p8「軟啟動或變頻驅動　UPS 容量可以小一個級距」；文獻回顧 §2（Jefferson Lab 19.5 A 例） | 相符（推論） |
| 19 | 遊戲分工：出題者設定方案／UPS 時間／冷卻水中斷，值班工程師判斷（9） | pw#outage 控制項；pe#monitor「冷卻水中斷」按鈕 | 相符 |
| 20 | 程式算六種情況，保住四個；沒保住的是「冷卻鏈無備援、停五分鐘」「發電機沒起來、停一小時」（10） | `outage_timeline.py` 實跑輸出 | 相符（模型假設下的計算） |
| 21 | 溫度曲線是教學示意、非實測；程式假設電一回來冷卻鏈立刻恢復（12） | pw#outage「曲線為教學示意，非實測」；程式 cooling_gap()；文獻回顧 §6「壓縮機停機後再啟動通常要等一段時間」 | 相符 |
| 22 | 下一課：冷卻鏈不斷電與壓縮機驅動（12） | academy/lessons/Q131/brief.md | 相符 |

## v2 動畫展示段（demos_extra/q130.py）

| # | 旁白說法 | 依據 | 結論 |
|---|---|---|---|
| D1 | 降溫流程副標「完整降溫約一到兩天」；暫停、時間拉回零（cooldown 1） | 04_cooldown.js subtitle、「⏸ 暫停」、「時間 (小時)」滑桿 | 相符 |
| D2 | 大字先抽真空，再換最花時間的脈衝管預冷，右邊各層溫度往下掉（cooldown 2） | phase()；desc「這是最耗時的階段」；tLbls 在各層右側 | 相符（截圖確認） |
| D3 | 約一天後凝結成淺藍液滴，稀釋循環啟動，混合腔幾小時內到最低溫（cooldown 3） | phase 25 h、液滴 0x8ef0ff（25–28 h）、④ 27.5–33 h | 相符 |
| D4 | 基溫穩定、可以開始量測；右下白線移到三十六小時；之後還要重新校準（cooldown 4） | phase「✓ 基溫穩定，可開始量測」；inset 白線；LRZ 降溫後要重新校準 | 相符 |
| D5 | 斷電時間軸：對數時間一秒到十天、金色曲線混合腔溫度、紅色虛線一克耳文（outage 1） | power1000.html outage desc 與 build() | 相符 |
| D6 | 第一種方案：約兩分鐘衝過紅線、一小時升到約三十克耳文、好幾天後降回（outage 2） | curve()：119 秒到 1 K、1 小時 30.0 K、3.5 天降回；截圖 | 相符 |
| D7 | 第二種方案曲線平貼、左邊停機時間變零（outage 3） | 方案 B t0 = Infinity；讀數「0（不受影響）」在左側面板 | 相符 |
| D8 | 第三種方案、UPS 三十分鐘：平到三十分鐘才上衝，停機時間又變三到五天（outage 4） | t0 = ups × 60；讀數「約 3–5 天（UPS 耗盡後同 A）」 | 相符 |
| D9 | 正常運轉：綠色狀態、入水十八度、壓縮機運轉（monitor 1） | readout「狀態：OK」綠字、18.0 °C、「壓縮機 運轉」 | 相符 |
| D10 | 冷卻水中斷：入水爬升，黃色警告後轉紅色告警，儀表櫃上圓燈變紅跳動（monitor 2） | water 情境 WARN／ALARM、alarm 球位於 GHS 儀表櫃上方 | 相符 |
| D11 | 超過上限聯鎖停壓縮機，紫色氣流改走儲存槽回收混合氣，保護昂貴的氦三（monitor 3） | comp_on = water < 32；recov 紫色流到儲存槽；desc「保護昂貴的 ³He」 | 相符 |
| D12 | 溫度計小球大多變紅，監控曲線往上翹；電還在，冷卻水一斷照樣回溫（monitor 4） | 截圖：50 K 級黃色、其餘紅色；inset 四條線上升 | 相符 |

## 課程

- 主題、學習目標、動手任務、孩子獨立改造（實驗室斷電處置卡）、好玩機制（故障注入）、作品（斷電時間軸與處置卡）、120 分鐘流程、驗收與常見誤解、生活技能（事先準備應變計畫）依 `academy/lessons/Q130/lesson.json` 核對。
- 課綱素材「p:monitor」：power1000.html 沒有 monitor 場景，指的是 peripherals.html#monitor，本集如此使用。簡報頁碼 p7–8 正確。
- 旁白不念英文與縮寫：UPS 念「不斷電系統」、ATS 念「自動切換開關」、GHS 念「氣體處理系統」、K 念「克耳文」、10 mK 念「只比絕對零度高約百分之一度」、LRZ 念「德國一座超級電腦中心」、³He 念「氦三」；投影片上保留符號。
- 課綱屬工程同仁型；沿用父子課堂口吻，未虛構孩子作品、課堂錄音或對話。
