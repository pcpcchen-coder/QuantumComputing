# Q032 模組發表：設計我的 transmon

依課綱製作的課前教學版；12 頁原生可編輯簡報（父子科技學院 L001 版型）、36 句旁白、zh-TW-YunJheNeural、原片頭 v2、靜態淡化、無背景音樂。

| 分鐘 | 內容 |
|---|---|
| 00–10 | 開場：從上一堂偵探辦案接到模組發表，好玩機制「工程答辯」 |
| 10–25 | 概念：三個數字（f₀₁ 4–6 GHz、α ≈ −E_C 約 −200～−300 MHz、E_J／E_C 50–100）與各自的取捨、範例卡、常見誤解（參數卡是設計目標） |
| 25–65 | 父子實作：用參數設計器（transmon_card.py 或 transmon-3d#capacitor）做一張 transmon 參數卡，再到 index.html#potential 驗證能階 |
| 65–75 | 休息 |
| 75–105 | 孩子改造：替參數卡加讀取腔頻率（例如 7 GHz），說明失諧為什麼要這麼大 |
| 105–115 | 孩子教爸爸：操作與原理（工程答辯） |
| 115–120 | 錄音總結、替參數卡取名字、保存 |

教材：transmon 參數卡、三個數字的取捨單、讀取腔改造單、說明卡（列印）、解答、可執行的 `transmon_card.py`（參數設計器，只要 Python 3，不需安裝套件）、動畫導覽（`academy/authoring/q032/classroom.py`）。
動畫展示段：`academy/authoring/v2/demos_extra/q032.py`（index.html#potential 兩段：拉比值看頻率怎麼走、等間距和不等距；transmon-3d.html#capacitor 一段：用參數設計器對準五吉赫）。
這是依課綱製作的課前教學版，不是實際上課錄音。
