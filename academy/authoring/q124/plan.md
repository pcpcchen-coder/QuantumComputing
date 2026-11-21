# Q124 用 Qiskit 重現八個範例

依課綱製作的課前教學版；12 頁原生可編輯簡報（父子科技學院 L001 版型）、36 句旁白、zh-TW-YunJheNeural、原片頭 v2、靜態淡化、無背景音樂。
QM08「動手寫量子電路：從八個範例到自己的線路」的第十二課：把 basic-circuits.html 八個範例頁底部的 Qiskit 程式碼搬到本機，每個範例用 Statevector（理論機率，要和頁面灰色底一模一樣）與 shots = 1000（次數只會接近）各跑一次，再用 qiskit-aer 重跑。
實跑：八個預設 8／8 一致；頁面 74 種選項組合的程式碼逐一在 Qiskit 2.6.2 執行，機率 74／74 一致；比振幅時 Grover 奇數輪 28 種差一個整體負號（量不到）。
注意事項：自己改過的版本頁面沒檢查過，要自己用數字比對，不要只看圖；measure_all() 的紀錄叫 meas（頁面用 c）；固定種子時三個各半的範例次數相同；比機率、不直接比振幅。
孩子獨立改造：BV 密碼改成 011（到頁面點同一組比）、隱形傳態角度改成 π/2（用 sin²(θ/2) 比）。好玩機制「Release 任務」（八格全勾才發布 v1.0），作品是八範例 notebook，生活技能「用工具驗證結果」。

| 分鐘 | 內容 |
|---|---|
| 00–10 | 開場：從瀏覽器搬到自己的電腦；Release 任務規則與作品 |
| 10–25 | 概念示範：頁面程式碼區塊（basic-circuits p29）、兩種跑法、灰色底與綠色柱（p28） |
| 25–65 | 父子共同實作：八段程式貼進 notebook，Statevector 與 shots 各跑一次，填八格檢查表；qiskit-aer 重跑 |
| 65–75 | 休息 |
| 75–105 | 孩子獨立改造：換一個參數，先預測，再和頁面或公式比對 |
| 105–115 | 角色互換：孩子教爸爸操作與原理 |
| 115–120 | 錄音總結、作品命名、存成 v1.0 |

教材：八格檢查表、兩種跑法紀錄、改造單、最後一關檢核表；八範例.ipynb 與同內容的 `eight_examples.py`（Qiskit）、純 Python 答案卷 `check_eight.py`、解答（`academy/authoring/q124/classroom.py`）。
v2 動畫展示段：basic-circuits.html#teleport 程式碼區塊（tpcode）、#grover 程式碼區塊與頁尾 Statevector 說明（grcode）、#bv 密碼改成 110 後量測並讀程式碼（bvparam），見 `academy/authoring/v2/demos_extra/q124.py`。
