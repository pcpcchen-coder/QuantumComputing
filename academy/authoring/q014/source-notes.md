# Q014 來源筆記（逐字引文）

查核日：2026-11-18。維基百科頁面由製作代理直接開啟（Quantum decoherence 以 `action=raw` 取得 wikitext，與 `oldid=1384689551` 的內容逐位元組相同；Relaxation (NMR) 的 revision id 取自 MediaWiki API 的 revid）。學程內部簡報與動畫程式由製作代理讀取。數字由製作代理重新計算。

## Quantum decoherence（Wikipedia，oldid=1384689551）

- 「Quantum decoherence is the loss of quantum coherence. It involves generally a loss of information of a system to its environment.」
- 「Quantum computing relies on quantum coherence and is one of the primary practical applications of the concept.」
- 「if the system is "open", that is, not perfectly isolated, for example during a measurement, coherence is shared with the environment and appears to be lost with time — a process called quantum decoherence or environmental decoherence.」
- 「Decoherence is needed to understand why a quantum system begins to obey classical probability rules after interacting with its environment (due to the suppression of the interference terms …)」
- 「Decoherence is a central challenge for the practical realization of quantum computers, which rely on evolution of quantum systems isolated from the environment to perform computation. Two timescales, T₁ and T₂, characterise this challenge and serve as standard metrics for qubit fidelity across most platforms.」
- 「The relaxation time T₁ characterizes how quickly a qubit loses energy to its environment as it decays from the excited state |1⟩ to the ground state |0⟩. The excited-state population decays exponentially」
- 「The dephasing time T₂ characterizes how quickly phase coherence in the qubit's state decays.」
- 「T₂ is commonly measured via the Ramsey interference experiment, in which a qubit is prepared in a superposition state and freely evolves, precessing, for a variable interval.」
- 「T_2 ≤ 2T_1 … with equality only when energy relaxation is the sole source of decoherence. Because gate operations must complete before the quantum states decohere, the timescales T₁ and T₂ together set a practical upper bound on the size of quantum circuits.」
- 「In superconducting transmon qubits, T₂ values of 50–200 μs are routinely achieved」
- 「The most basic and direct way to reduce decoherence is to prevent the quantum system from interacting with the environment by any type of isolation.」
- 「Cryogenic cooling: Operating quantum systems at extremely low temperatures to reduce thermal vibrations and noise.」「Electromagnetic shielding: Enclosing quantum systems in materials that block external electromagnetic fields - such as mu-metal or superconducting materials - reduces decoherence caused by unwanted electromagnetic interference.」「Better materials: Fabricating qubits from special materials, like highly pure or isotopically enriched ones, to minimize intrinsic noise of the material, including noise from defects or nuclear spins.」（這三條在維基上標有 citation needed，本集只當作「真實量子電腦用的方法」的概述，不引數字）
- 「Observe that the off-diagonal elements—the coherence terms—decay as the spread of the random phase, σ, increases over time」（隨機相位散開 → 相干項衰減；本集「每次轉速不同、平均起來箭頭變短」的依據）

## Relaxation (NMR)（Wikipedia，oldid=1385738005）

- 「The decay of RF-induced NMR spin polarization is characterized in terms of two separate processes, each with their own time constants. One process, called T1 … The other process, called T2」
- 「T2 relaxation affects the coherent components of M perpendicular to B0.」
- 「In NMR systems, the following relation holds absolute true T2≤2T1.」

## 學程內部簡報

- slides/JJ_Microwave_Readout_Talk.pptx 第 5 頁：「Bloch 球：北極 |0⟩、南極 |1⟩、赤道為等權重疊加」；講者備註「3D 動畫 場景 1「Bloch 球」：animations/index.html#bloch」。
- 第 6 頁「量子位元的品質指標」：「T1：能量弛豫時間 |1⟩ 自發放出能量回到 |0⟩ 的時間常數。最佳 transmon 約 0.1–1 ms。」「T2：相位相干時間 疊加態相位資訊保留多久；T2 ≤ 2T1。受低頻雜訊（磁通、電荷）影響。」「可執行的操作數 ≈ T2 / 閘時間 / 例：T2 = 100 μs、閘 = 25 ns → 約 4000 個閘 / 讀取時間必須 ≪ T1，否則讀取途中就衰減 / 所有指標都和 JJ 品質（缺陷、準粒子）與讀取電路設計（Purcell 效應）有關」。講者備註：「在 3D 場景 1 中可以切到「Ramsey 進動 + T2」模式，會看到向量在赤道上轉、同時越縮越短，那就是失相。」「讀取時間必須遠小於 T1，否則讀到一半它就掉下來了」。
- slides/QC_Peripheral_Systems_Talk.pptx 第 6 頁「為什麼要 10 mK？」：「5 GHz 量子位元能量 hf ≈ 20 μeV ≈ 240 mK × kB」「10 mK kBT 只有 hf 的 1/24 → 熱激發 ≈ e−24」「量子位元有殘留熱激發 → 初始化錯誤 / 讀取腔中有熱光子 → 量子位元失相（T2 下降） / 準粒子增加 → 穿隧過 JJ 帶走能量（T1 下降） / 超導體（Al，Tc ≈ 1.2 K）根本無法超導」「300 K → 50 K → 4 K：脈衝管（機械式冷凍） / 4 K → 0.9 K → 100 mK → 10 mK：稀釋循環」。

## 互動動畫程式

- animations/index.html：第 31 行 `<div class="controls" id="controls">`；第 40 行載入 `js/scenes/01_bloch.js`；右下 `#inset-wrap`（第 35 行）。
- animations/js/scenes/01_bloch.js：`id: 'bloch'`（第 3 行）；desc「Ramsey / 失相 (T2)：赤道上的態因頻率失諧而繞 z 軸進動，雜訊使相位擴散、向量縮短」「能量弛豫 (T1)：|1⟩ 會自發放出能量回到 |0⟩」（第 8–9 行）；`let mode = 'rabi'`、`T2 = 6, T1 = 5`（第 49–50 行）；`ui.radio([['rabi', 'Rabi 振盪'], ['ramsey', 'Ramsey 進動 + T2'], ['t1', 'T1 能量弛豫'], ['manual', '手動 θ / φ']], …)`（第 55 行）；滑桿「失諧 Δ（Ramsey）」（第 58 行）；按鈕「π/2 脈衝 → 疊加態」（第 62 行）；插圖「激發態機率 P(|1⟩) 隨時間變化」（第 64 行）；`if (t > 12) { reset(); t = 0; }`（第 75 行）；Ramsey：`r = Math.exp(-t / T2); vec.set(r * Math.cos(a), r * Math.sin(a), 0)`（第 80–81 行）；T1：`pe = Math.exp(-t / T1 * 1.0); vec.set(0, 0, 1 - 2 * pe)`（第 83–84 行）；讀數 `|r| = … ${L < 0.98 ? '（混態：失去相干性）' : '（純態）'}`（第 100 行）。
- animations/js/core.js：ui.button／ui.radio／ui.slider 都加到 `#controls`（第 339–369 行）；動畫時間以秒累加（第 271–273 行）。

## 重新計算（製作代理）

```
h·f / k_B，f = 5 GHz：6.626e-34 × 5e9 / 1.381e-23 = 0.240 K（240 mK）
240 mK ÷ 10 mK = 24 → e^-24 ≈ 3.8e-11
100 μs ÷ 25 ns = 4000
10 mK = 0.01 K（比絕對零度高百分之一度）
動畫 T1 模式：P(1) = e^(−t/5)，t = 3.47 s 時 0.5（箭頭經過球心），t = 12 s 時 0.091，z = 0.82
動畫 Ramsey 模式：|r| = e^(−t/6)，t = 12 s 時 0.135；z = 0 → P(1) = 0.50
```
