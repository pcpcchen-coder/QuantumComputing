# Q127 來源筆記（逐字引文）

查核日：2026-11-19（檔頭 CHECKED 依派工統一寫 2026-11-18）。維基百科頁面由製作代理直接讀取原始 wikitext（action=raw，2026-11-19），revision id 未取得。學程內部簡報（以 zipfile 讀出實際頁碼與文字）與動畫程式由製作代理讀取，畫面以 Playwright 單張截圖確認（nice -n 19，未錄影、未跑 QV2_DRY）。程式由製作代理實際執行。

## Quantum logic gate（Wikipedia，2026-11-19 raw wikitext）

- Phase shift gates：「The phase shift is a family of single-qubit gates that map the basis states |0⟩ ↦ |0⟩ and |1⟩ ↦ e^{iφ}|1⟩. The probability of measuring a |0⟩ or |1⟩ is unchanged after applying this gate, however it modifies the phase of the quantum state. This is equivalent to tracing a horizontal circle (a line of constant latitude), or a rotation about the z-axis on the Bloch sphere by φ radians.」
- 「Some common examples are the T gate where φ = π/4 (historically known as the π/8 gate), the phase gate (also known as the S gate …) where φ = π/2 and the Pauli-Z gate where φ = π.」
- 「S = … = P(π/2) = √Z」「T = … = P(π/4) = √S = ⁴√Z」（所以 S² = Z、T² = S、T⁴ = Z）。
- 「Pauli Z leaves the basis state |0⟩ unchanged and maps |1⟩ to −|1⟩. Due to this nature, Pauli Z is sometimes called phase-flip.」
- 本課的白話：S 念「四分之一圈相位閘」（繞 z 軸 90°），T 念「八分之一圈相位閘」（繞 z 軸 45°）；相位閘不改機率，只改相位。

## HARKing（Wikipedia，2026-11-19 raw wikitext）

- 「HARKing (hypothesizing after the results are known) is an acronym coined by social psychologist Norbert Kerr that refers to the questionable research practice of "presenting a post hoc hypothesis in the introduction of a research report as if it were an a priori hypothesis".」
- 「Hence, a key characteristic of HARKing is that post hoc hypothesizing is falsely portrayed as a priori hypothesizing.」
- 本課的白話：「看到結果才編出假設，再假裝一開始就這麼想」，旁白念「事後假設」；對應課綱常見誤解「先寫預測再跑，避免看結果才找理由」。

## Backward design（Wikipedia，2026-11-19 raw wikitext）

- 「Backward design is a method of designing an educational curriculum by setting goals before choosing instructional methods and forms of assessment.」
- 三階段：「Identify the results desired (big ideas and skills)」「Determine acceptable levels of evidence that support that the desired results have occurred」「Design activities that will make desired results happen」。
- 本課的白話（生活技能「從目標反推設計」的類比）：先決定要說明什麼（目標）→ 什麼結果能當證據 → 最後才挑閘（設計）。原文講的是課程設計，本課只借用「目標 → 證據 → 設計」的順序。

## 學程簡報：如何操作量子電腦（slides/QC_Operation_Talk.pptx）

- 第 18 頁「單位元量子閘一覽」：「Z｜[[1, 0], [0, −1]]｜繞 z 軸 180°｜|1⟩ 變號（相位翻轉）」「H｜…｜|0⟩ → |+⟩：產生疊加」「S｜[[1, 0], [0, i]]｜繞 z 軸 90°｜相位 i；S² = Z」「T｜[[1, 0], [0, e^{iπ/4}]]｜繞 z 軸 45°｜容錯計算的關鍵非 Clifford 閘」「X｜…｜0 ↔ 1，量子版 NOT」。
- 第 22 頁「兩位元閘：產生糾纏的唯一方法」：「CZ｜兩個都是 1 時加負號（對稱）」「等價關係｜CNOT = (I⊗H) · CZ · (I⊗H)｜CZ 對稱：不分控制與目標」。
- 第 28 頁「動態線路：中途量測與即時回饋」：「3D 場景 6 的「量子隱形傳態」範例以延遲量測原理把條件操作改成受控閘，結果相同：q2 最後得到 q0 原本的狀態（P(1) = 0.75）」。
- 第 52 頁「操作一台量子電腦：檢查表」：「2｜設計線路｜疊加 → 用結構安排相位 → 干涉；估算寬度、深度、兩位元閘數」「3｜先用模擬器｜驗證邏輯正確（≤ ~30 位元可精確模擬）」「8｜後處理與驗證｜…與模擬比較；答案可驗證就驗證」。
- 課綱沒有列「沿用簡報頁」（素材寫「沒有可直接沿用的現有頁面或場景」），以上頁碼由製作代理讀出。

## 學程動畫：animations/operation.html#register（js/operation/04_register.js）

- desc：「上排是每個量子位元「自己」的 Bloch 球，下方柱子是整個暫存器的 2ⁿ 個基底態振幅：高度 = 機率，顏色 = 相位（金 = +，藍 = −）。」
- 按鈕：`['H', 'X', 'Z', 'S', 'T'].forEach((gname) => ui.button(gname, () => ap(() => { if (tgt < n) st.gate(gname, tgt); }), g1));`；
  `ui.button('CZ', () => ap(() => { if (n > 1 && tgt < n) st.cz((tgt + 1) % n, tgt); }), g2);`；「均勻疊加 H⊗ⁿ」`st.reset(); for (q…) st.gate('H', q)`；「測量全部」「只測 q0」「重設 |0…0⟩」。
- 讀數：`|ψ⟩ = …`、「各量子位元 Bloch 長度：q0 …，q1 …」、長度 < 0.98 時粉紅色「有糾纏：單一量子位元的向量變短（約化態是混態）」，否則「無糾纏（可分離態）」。
- common.js：`phaseHue = (0.1 + atan2(im, re) / 2π) mod 1`（相位 0 金色約 36°、π/4 約 81°、π/2 約 126°、3π/4 約 171°、π 藍色約 216°）；T = [[1, 0], [0, e^{iπ/4}]]。
- Playwright 實拍讀數（2 顆，目標 q0）：H「0.71 |00⟩ + 0.71 |01⟩」；T 一到四次「0.50+0.50i |01⟩」「0.71i |01⟩」「−0.50+0.50i |01⟩」「−0.71 |01⟩」；再 H「1.00 |01⟩」；
  重設後 H、T×3、H「0.15+0.35i |00⟩ + 0.85−0.35i |01⟩」；均勻疊加「0.50 …×4」無糾纏；CZ「… + −0.50 |11⟩」、q0 0.00、q1 0.00、有糾纏；H「0.71 |00⟩ + 0.71 |11⟩」；測量全部後只剩一個基底態（該次 |11⟩，隨機）。

## 學程動畫：animations/operation.html#circuit（js/operation/06_circuit.js）

- `tele: { name: '量子隱形傳態', n: 3, meas: [2], cols: [ [[RY(0, 2π/3, 'Ry')], '準備要傳送的狀態：q0 = cos60°|0⟩ + sin60°|1⟩（P(1) = 0.75）'], [[H(1)], …], [[CX(1, 2)], …], [[CX(0, 1)], …], [[H(0)], …], [[CX(1, 2)], 'Bob 依 q1 的結果做 X（延遲量測：改成受控閘）'], [[CZ(0, 2)], 'Bob 依 q0 的結果做 Z → q2 變成原本 q0 的狀態（看左側小球）'], [M([2]), '量測 q2：P(1) = 0.75，和一開始的 q0 相同'] ] }`
- 線路由上到下 q0、q1、q2（`wy = (q) => 3.6 - q * 0.8`）；量測欄抽 1000 次，插圖「量測 1000 shots 的結果（青線 = 理想機率）」，xlabel「量測位元（q2）」。
- Playwright 實拍：步驟 1「0.50|000⟩ + 0.87|001⟩」；步驟 7「0.25|000⟩ + 0.25|001⟩ + 0.25|010⟩ + 0.25|011⟩ + 0.43|100⟩ + 0.43|101⟩ + …」；步驟 8 直方圖兩根、青線 0.25、0.75（該次 1: 751，0: 249，隨機）。

## 實跑紀錄

- `tiny_sim.py`（Python 3.13.18，只用標準函式庫，沒有亂數）：範例甲每一步振幅與 1 = 100%；範例乙 0.71|00⟩ + 0.71|11⟩；故意出錯甲 0 14.6%、1 85.4%；故意出錯乙四種各 25.0%。完整輸出見 `classroom.py` 的 RUN_OUTPUT。
- `my_circuit.py`（qiskit 2.6.2、qiskit-aer 0.18.4，AerSimulator seed_simulator=127）：範例甲理想與抽樣都是 1 = 100%；範例乙理想 00、11 各 50%，抽樣 48.3%、51.7%；故意出錯甲理想 14.6%／85.4%、抽樣 11.5%／88.5%；故意出錯乙理想各 25%。完整輸出見 `classroom.py` 的 QISKIT_OUTPUT。
