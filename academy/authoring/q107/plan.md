# Q107 第 9 課：Deutsch 演算法與相位回踢

依課綱製作的課前教學版；12 頁原生可編輯簡報（父子科技學院 L001 版型）、36 句旁白、zh-TW-YunJheNeural、原片頭 v2、靜態淡化、無背景音樂。
課綱屬「師生對話」型（QM07 超導量子電腦深入第 9 課）；影片沿用父子課堂的口吻與結構，內容依 docs/超導量子電腦師生對話教學紀錄.md 第 9 課與《量子金魚》008 簡報改寫，不虛構對話。

| 分鐘 | 內容 |
|---|---|
| 00–10 | 開場：從格羅弗的負號回到源頭；只准問一次 |
| 10–25 | 概念示範：紅綠球、可逆黑盒子、相位回踢、疊加→查詢→干涉 |
| 25–65 | 在 transmon-3d#deutsch-lab 自由實驗跑四種黑盒，對照《量子金魚》紅綠球比喻，填四種黑盒判讀表 |
| 65–75 | 休息 |
| 75–105 | 孩子獨立改造：自己當黑盒子（deutsch_box.py 的 SECRET、紙卡），讓爸爸只問一次猜類型；改 PREP 看忘了準備會怎樣 |
| 105–115 | 孩子教爸爸：操作與原理 |
| 115–120 | 錄音總結、作品命名、保存 |

教材：四種黑盒判讀表、可執行的 `deutsch_box.py`（純 Python，不需套件）、盲測紀錄表、三個容易錯的地方、教爸爸檢核表、解答（`academy/authoring/q107/classroom.py`）。
v2 動畫展示段：transmon-3d.html#deutsch-lab 單步跑 f₃（相位回踢）、basic-circuits.html#deutsch 的 f(x)=1−x 與布洛赫球、transmon-3d.html#deutsch-lab 隨機隱藏盲測，見 `academy/authoring/v2/demos_extra/q107.py`。
