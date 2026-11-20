# Q058 來源筆記（逐字引文）

查核日：2026-11-18。維基百科頁面由製作代理以 `index.php?action=raw` 取得 wikitext（存於 `/home/user/qwork/q058wiki/`；查 revision id 的 API 當時回應限流，所以未記 oldid）。學程內部簡報與動畫程式由製作代理讀取。

## Expectation value (quantum mechanics)（Wikipedia）

- 「In quantum mechanics, the expectation value is the probabilistic expected value of the result (measurement) of an experiment. It can be thought of as an average of all the possible outcomes of a measurement as weighted by their likelihood, and as such it is not the most probable value of a measurement; indeed the expectation value may have zero probability of occurring」
- 「The eigenvalues a_j are the possible outcomes of the experiment, and their corresponding coefficient |⟨ψ|φ_j⟩|² is the probability that this outcome will occur」

## Bloch sphere（Wikipedia）

- 「In this basis, the values u, v, w are the expectations of the three Pauli matrices X, Y, Z, allowing one to identify the three coordinates with x y and z axes.」
- 「With z = cos θ, the probability of finding the state |0⟩ in a measurement in the standard basis depends linearly on the height: |⟨0|ψ⟩|² = cos²(θ/2) = (1+z)/2」
- 「The height z is first of all a coordinate of the state: it is the expectation value ⟨σz⟩ of the Pauli matrix」

## 學程內部簡報：slides/QC_Operation_Talk.pptx

- 第 30 頁「一個 shot 的讀取流程」：「量子位元在 |0⟩ 或 |1⟩ 時，讀取腔的共振頻率差 2χ（~MHz）」「解調、積分後成為 IQ 平面上的一個點」「在 FPGA 中用閾值（或線性判別）即時判成位元」。
- 第 31 頁「量測基底：硬體只會量 Z」表格：「Z｜（直接量）｜計算基底 |0⟩/|1⟩」「X｜H｜H 把 |+⟩/|−⟩ 轉成 |0⟩/|1⟩」「Y｜S† 再 H｜把 |+i⟩/|−i⟩ 轉到 |0⟩/|1⟩」「Z⊗Z（兩位元奇偶）｜各自量 Z，再乘起來」；「⟨Z⟩ = P(0) − P(1)」「⟨Z₀Z₁⟩ = P(00) + P(11) − P(01) − P(10)」；「很多問題的答案是期望值 ⟨ψ|O|ψ⟩，例如分子能量 = Σ 係數 × ⟨Pauli 字串⟩」「只量 Z 看不到相位；量 X、Y 才能還原整個 Bloch 向量」「3D 場景 7：切換「量 X / 量 Y」，同一個狀態得到不同的統計」。
  講者備註：「硬體只能在 Z 基底，也就是 |0⟩、|1⟩ 的方向量測。想量別的方向怎麼辦？在量測前先加一個旋轉，把想量的方向轉到 z 軸。」「【在 3D 場景 7】把準備狀態設為 θ = 90 度，切換「量 Z」、「量 X」、「量 Y」，會看到同一個狀態得到完全不同的統計結果。」
- 第 32 頁：「σ(P̂) = √(P(1−P)/N)｜期望值 ⟨Z⟩ 的誤差 ≈ 2σ」「估計期望值到 ±0.01：~10,000」（本集只說「次數太少誤差很大」，數字留給 Q059）。
- 第 33 頁講者備註：「典型的讀取錯誤率是百分之零點五到三」（只用於 not_verified 的說明）。
- 第 34 頁「從計數到答案：兩種輸出」：「取樣（Sampler）｜輸出：各位元字串的計數 / 機率分佈｜答案集中在少數結果：Shor、Grover、BV」「期望值估計（Estimator）｜輸出：⟨ψ|O|ψ⟩ 與誤差棒｜變分演算法（VQE、QAOA）、量子模擬｜需要多個量測基底、大量 shots」。

## 互動動畫程式：animations/operation.html

- 場景 7（js/operation/07_readout.js）：desc「硬體只會在 Z 基底量測（|0⟩ 或 |1⟩）。想量 X 或 Y，就先加一個旋轉閘：量 X 前加 H，量 Y 前加 S†·H。」；blochVec 相位固定 0.4（第 61 行）；pTrue1 依基底取 z、x 或 y（第 62 行）；滑桿「準備狀態 θ」第 78 行；radio 第 79 行；基底方塊標籤第 103 行；讀數「量測基底：X（先做 H 再量 Z）」與「⟨X⟩ = …（理想 …）」第 113–116 行（⟨·⟩ = 1 − 2P̂(1)）。
- 場景 1（js/operation/01_qubit.js）：p0 = cos²(θ/2)（第 39 行）；滑桿「θ（極角）」第 48 行；「一次跑 1000 shots」第 54 行；讀數「理論：P(0) = …」第 99 行。
- 場景 2（js/operation/02_gates.js）：H 繞 (x+z)/√2 軸 180°（desc）；「重設 |0⟩」「重設 |1⟩」第 32–33 行；「動畫速度」第 40 行；讀數「測量機率：P(0) = …，P(1) = …」第 80 行。

## 數值重算

`/home/user/qwork/q058calc/checks.py`（numpy，輸出 `checks.out`）；截圖 `/tmp/.../scratchpad/q058/*.png`（製作代理暫存，1600×900 Chromium swiftshader）。
