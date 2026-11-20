# Q060 來源筆記（逐字引文）

查核日：2026-11-18。維基百科頁面由製作代理以 `index.php?action=raw` 取得 wikitext（存於 `/home/user/qwork/q060wiki/`，未記 oldid）。學程內部簡報與動畫程式由製作代理讀取。

## Deferred measurement principle（Wikipedia）

- 「The deferred measurement principle is a result in quantum computing which states that delaying measurements until the end of a quantum computation doesn't affect the probability distribution of outcomes.」
- 「A consequence of the deferred measurement principle is that measuring commutes with conditioning.」
- 「For example, measuring qubits as early as possible can reduce the maximum number of simultaneously stored qubits; potentially enabling an algorithm to be run on a smaller quantum computer or to be simulated more efficiently.」

## Quantum error correction — Bit-flip code（Wikipedia）

- 「In the case of the simple three-qubit repetition code, the encoding consists in the mappings |0⟩ → |000⟩ and |1⟩ → |111⟩.」
- 「One can then detect whether a qubit was flipped, without also querying for the values being transmitted, by asking whether one of the qubits differs from the others.」
- 「If the outcome corresponding to P_0 is obtained, no correction is applied, while if the outcome corresponding to P_i is observed, then the Pauli X gate is applied to the i-th qubit.」
- 「For example, if the first and second qubits are flipped, then the syndrome measurement gives the outcome P_3, and the third qubit is flipped, instead of the first two.」

## Quantum teleportation（Wikipedia）

- 「This yields one of four measurement outcomes which can be encoded in two classical bits of information.」
- 「The identity of the state actually obtained is encoded in two classical bits and sent to location B. The Bell state qubit at location B is then modified in one of three ways, or not at all, which results in a qubit identical to |φ⟩」

## 學程內部簡報：slides/QC_Operation_Talk.pptx

- 第 28 頁「動態線路：中途量測與即時回饋」：「線路中途量測部分量子位元／依結果（古典位元）決定後面的閘／需要控制電子在相干時間內完成判別與決策（~數百 ns）」；用途「主動重置：量到 1 就翻回 0／量子隱形傳態：依 2 個結果做 X / Z 修正／錯誤更正：每輪量測症狀、即時解碼／重複直到成功（repeat-until-success）」；程式「qc.measure(0, 0) / with qc.if_test((qc.clbits[0], 1)): qc.x(1)」；「3D 場景 6 的「量子隱形傳態」範例以延遲量測原理把條件操作改成受控閘，結果相同：q2 最後得到 q0 原本的狀態（P(1) = 0.75）」。
  講者備註：「這需要控制電子在相干時間內完成讀取、判別和決策，通常要在數百奈秒內。」
- 第 13 頁「初始化：每個 shot 都要回到 |0⟩」：「被動重置（等待熱化）… 等待 ~5 T₁ 讓 |1⟩ 自然衰減／簡單、不需回饋，但慢：數百 μs（如 250 μs）」「主動重置（量測 + 回饋）先量測：若結果是 1 → 立刻送 π 脈衝翻回 0／需要 FPGA 即時判別（數百 ns 延遲）／快：~1–5 μs，可重複以提高純度」。講者備註：「比被動重置快上百倍」。
- 第 33 頁講者備註：「典型的讀取錯誤率是百分之零點五到三」（只用於讀錯會補錯閘的說明）。

## 互動動畫程式

- basic-circuits.html 範例 5 teleport（第 396–413 行）：lead「Alice 只要做一次 Bell 量測、再傳 2 個古典位元，Bob 就能讓 q2 變成 ψ」；第 3 步說明「q2 的向量還在球心」；第 4 步 box「修正（2 個古典位元）」、說明「真實做法是 Alice 量測 q0、q1，把 2 個位元傳給 Bob：q1 = 1 就對 q2 做 X，q0 = 1 就做 Z。這裡用受控閘代替「量測後再修正」（延遲量測原理），q2 的結果完全相同。修正後 q2 的向量回到 ψ」。
- atoms.html 場景 11 zoned（js/atoms/11_zoned.js）：desc「讀取區：把要量測的原子（例如錯誤更正的輔助位元）搬到這裡成像，避免螢光干擾其他原子」；seqMeasure 第 99–108 行；小圖第 121–123 行（250 μs、0.3 μs、250 μs、1 ms；「閘本身只佔極小比例；整體速度由搬運與讀取決定」）。
- operation.html 場景 11 qec（js/operation/11_qec.js）：subtitle「只量「奇偶」不量資料」；desc「量奇偶不會破壞編碼的量子資訊」「每一輪：① 隨機發生錯誤（紅球）→ ② 量測穩定子，奇偶改變的方塊亮橘色（症狀）→ ③ 解碼器把症狀兩兩配對…→ ④ 修正」；控制項第 133–137 行。
- peripherals.html 場景 10 bringup（js/peripherals/10_bringup.js 第 54 行）：「T₁ ≈ 90 μs」。

## 數值重算

`/home/user/qwork/q060calc/checks.py`（qiskit 2.6.2、qiskit-aer 0.18.4，`AerSimulator(seed_simulator=7)`，輸出 `checks.out`）；截圖在製作代理暫存（1600×900 Chromium swiftshader）。
