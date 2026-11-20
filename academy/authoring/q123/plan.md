# Q123 古典 vs 量子：要查幾次？

依課綱製作的課前教學版；12 頁原生可編輯簡報（父子科技學院 L001 版型）、36 句旁白、zh-TW-YunJheNeural、原片頭 v2、靜態淡化、無背景音樂。
QM08「動手寫量子電路：從八個範例到自己的線路」的第十一課：把 Deutsch、BV、Grover（再補 Shor）排進同一張「查詢次數比較表」（basic-circuits.pptx 第 30 頁）。
Deutsch：古典 2 次、量子 1 次；n 位元 Deutsch–Jozsa：古典最壞 2ⁿ⁻¹ + 1 次（3 位元 5 次、10 位元 513 次），量子 1 次；
BV：古典問 100、010、001 共 n 次，量子 1 次；Grover：古典平均 (N + 1)/2 次（N = 8 是 4.5 次、1,024 是 512.5 次），量子約 (π/4)√N 輪（2 輪、25 輪），平方根加速；
Shor：古典次指數、量子多項式（QC_Operation_Talk 第 42 頁：指數級 vs 平方級）。
注意事項：查詢次數少不等於總時間少（量子閘慢、錯誤更正、量測與重複）；允許出錯時，3 位元 Deutsch–Jozsa 古典抽 4 個問誤判只有 2.9%。
孩子獨立改造：找一個量子沒有優勢的問題（QC_Operation_Talk 第 45 頁：資料輸入、排序與一般計算、小規模問題），對照「輸入小、計算難、輸出小」。好玩機制「工程答辯」，作品是查詢次數比較表，生活技能「用數字比較」。

| 分鐘 | 內容 |
|---|---|
| 00–10 | 開場：把四個演算法排在同一張表；工程答辯規則與作品 |
| 10–25 | 概念示範：什麼叫查一次；Deutsch、BV、Grover、Shor 四列（basic-circuits p30、QC_Operation_Talk p42） |
| 25–65 | 父子共同實作：畫比較表，用 operation.html#interference、transmon-3d.html#bv、operation.html#grover 驗證三格，再跑 query_count.py |
| 65–75 | 休息 |
| 75–105 | 孩子獨立改造：找一個量子沒有優勢的問題，說明原因（QC_Operation_Talk p45）；選用 qiskit_check.py |
| 105–115 | 角色互換：孩子教爸爸操作與原理 |
| 115–120 | 錄音總結、作品命名、版本存檔 |

教材：查詢次數比較表、三格動畫驗證單、量子沒有優勢的問題、最後一關檢核表；可執行的 `query_count.py`（純 Python）與選用的 `qiskit_check.py`、解答（`academy/authoring/q123/classroom.py`）。
v2 動畫展示段：operation.html#interference 讀「回答一的有幾個」與古典最壞 5 次（five）、transmon-3d.html#bv 步驟 1 古典一位一位問與步驟 5（bvask）、operation.html#grover 位元數 2／4／6 的古典平均與最佳輪數並自動跑到最佳次數（scale），見 `academy/authoring/v2/demos_extra/q123.py`。
這是依課綱製作的課前教學版，不是實際上課錄音。
