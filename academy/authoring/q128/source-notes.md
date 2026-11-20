# Q128 來源筆記（逐字引文）

查核日：2026-11-19（檔頭 CHECKED 依派工統一寫 2026-11-18）。維基百科頁面由製作代理直接讀取原始 wikitext（action=raw，2026-11-19），revision id 未取得。學程內部動畫程式與課綱由製作代理讀取，畫面以 Playwright 單張截圖確認（nice -n 19，未錄影、未跑 QV2_DRY）。程式由製作代理實際執行。

## Poster session（Wikipedia，2026-11-19 raw wikitext）

- 「A poster presentation, at a congress or conference with an academic or professional focus, is the presentation of research information in the form of a paper poster that conference participants may view. A poster session is an event at which many such posters are presented.」
- 「Presentations usually consist of affixing the research poster to a portable board with the researcher in attendance answering questions posed by passing colleagues.」
- 「Poster sessions are used as an alternative to oral presentations as a form of academic assessment.」
- 本課的白話：「研討會的海報展，作者也是站在海報旁邊，回答走過的人提出的問題」；量子電路展海報就是借用這個形式。

## Curator（Wikipedia，2026-11-19 raw wikitext）

- 「An "exhibitions curator" is a person in charge of conceiving and organising exhibitions.」
- 「The title "curator" identifies someone who selects and often interprets works for an exhibit. In addition to selecting works, the curator is often responsible for writing labels, catalog essays, and other content supporting exhibitions.」
- 本課的白話：孩子當「策展人」＝挑展品、替展品寫說明（展品卡、海報）。

## Plagiarism（Wikipedia，2026-11-19 raw wikitext）

- 「Plagiarism is the representation of another person's language, thoughts, ideas, or expressions as one's own original work.」
- 本課的白話：「把別人的文字、想法或作品當成自己的原創，叫做抄襲」；對應課綱常見誤解「截圖與程式要註明出處」。

## 學程動畫：量子電路入門 basic-circuits.html

- 頁首：「量子電路入門 · 互動動畫」「八個基礎量子電路」；說明「讀法和 Qiskit 相同：電路圖 q0 在最上面，但寫成位元字串時 q0 在最右邊」。
- 分頁（#tabs，由 SCENES 產生 `<small>範例 i</small><b>short</b>`）：範例 1 疊加、範例 2 干涉、範例 3 Bell 態、範例 4 GHZ 態、範例 5 隱形傳態、範例 6 Deutsch、範例 7 BV、範例 8 Grover；點選後 #sceneNo 顯示「範例 i / 8」。
- 各範例預設選項（opts.def）：疊加起始態 |0⟩；干涉「有 Z」；Bell「Φ⁺」；GHZ「3 顆」；隱形傳態 ψ = √¾|0⟩+½|1⟩；Deutsch f(x)=x；BV 密碼 101；Grover 2 顆、答案 11、輪數「最佳」（1 輪）。
- Bell 態：「H 閘：q0 進入疊加」→「CNOT：糾纏」；選第三種 Ψ⁺ 時先「用 X 把 q1 翻成 1，之後 CNOT 會讓兩顆位元『相反』」，量測「永遠相反（01 或 10）」。
- 量測卡：「量測 1 次」「量測 1,000 次」「清除」；「灰色底是理論機率，綠色是實際次數」。
- 重點卡：每個範例下方「延伸：」連結，例如 Grover：「如何操作量子電腦 · Grover 搜尋：振幅放大」「Transmon 3D · 第 7 章 振幅長條：糾纏、Grover 與 Deutsch」。
- 頁尾：「所有振幅都由頁面內建的狀態向量模擬器即時計算，和 Qiskit 的 Statevector 結果一致（Grover 的擴散步驟照理想的『對平均值翻轉』計算；用 H、X、多控制 Z 組成的實際電路會多一個整體負號，機率完全相同）」。
- 製作代理以 Node 載入頁面 `<script id="engine">`（SCENES、simulate、marginal），算出八個預設範例最後的理想機率：疊加 0、1 各 50%；干涉 1 100%；Bell 00、11 各 50%；GHZ 000、111 各 50%；隱形傳態（量 q2）0 75%、1 25%；Deutsch（量 q0）1 100%；BV 101 100%；Grover 11 100%。步驟數依序 1、3、2、3、4、4、4、3。

## 學程動畫：如何操作量子電腦 operation.html

- 場景 6 量子線路（06_circuit.js）：預設線路按鈕「Bell 態」「GHZ 態（3 位元糾纏）」「干涉：H–Z–H」「Deutsch–Jozsa（平衡函數）」「Bernstein–Vazirani（秘密字串 101）」「Grover 搜尋（2 位元，找 |11⟩）」「量子隱形傳態」「量子傅立葉轉換（QFT，輸入 |110⟩）」；開關「加入雜訊（每閘 1%、讀取 3%）」。
- 場景 12 完整流程（12_workflow.js）：程式螢幕 `qc = QuantumCircuit(2)`、`qc.h(0)`、`qc.cx(0, 1)`、`qc.measure_all()`；轉譯標籤「q0→Q3」「q1→Q1」；「下一站 ▶」「自動播放」。（動畫段使用，見 v2/demos_extra/q128.py）

## 課綱（academy/lessons）

- Q128 lesson.json：學習目標「向家人展示自己的線路，回答三個問題」；動手任務「每人 5 分鐘：線路、振幅逐步、量測結果」；孩子獨立改造「根據觀眾問題修改說明」；好玩機制「首映會」；作品「量子電路展海報」；生活技能「發表與回饋」；家長課前準備「發表模板」；常見誤解「截圖與程式要註明出處」。
- QM08：Q113 讀圖之前：三個約定與今天用到的閘；Q114–Q121 範例 1–8；Q122 Grover 三位元；Q123 古典 vs 量子：要查幾次？；Q124 用 Qiskit 重現八個範例；Q125 量測 1 次與 1000 次；Q126 加入雜訊；Q127 專題：設計自己的線路。
- Q129 brief.md：「Q129 電從哪裡來、到哪裡去」。

## 程式實跑

- exhibit_helper.py（Python 3.13.18，標準函式庫，沒有亂數）：八張展品卡 8/8 和頁面一樣；Bell 態振幅逐步「+1.000|00⟩」→「+0.707|00⟩  +0.707|01⟩」→「+0.707|00⟩  +0.707|11⟩」；海報檢查 8/8。
- qiskit_check.py（Qiskit 2.6.2，Statevector，沒有亂數）：八個範例的理想機率與 exhibit_helper.py 完全相同；閘數依序 1、3、2、3、7、5、10、12。
