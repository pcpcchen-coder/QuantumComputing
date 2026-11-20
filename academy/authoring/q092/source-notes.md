# Q092 來源筆記（逐字引文）

查核日：2026-11-18。學程內部簡報、演講稿與動畫程式由製作代理讀取；圈數由製作代理依場景程式碼計算。

## 量子電腦的周邊系統（slides/QC_Peripheral_Systems_Talk.pptx）第 22 頁「時脈與同步：所有儀器踩同一個節拍」

- 「銣原子鐘 / GPS 馴服 10 MHz 參考」
- 「10 MHz 參考：所有 LO、DAC、ADC 的頻率都由它倍頻而來 → 相位彼此鎖定」
- 「相位雜訊：直接造成量子位元失相 → 選用低相位雜訊的參考與合成器」
- 「量子閘的相位就是微波的相位：驅動 LO 與讀取 LO 若沒有鎖定，每次量測的參考相位都會漂移」

## speech/周邊系統演講稿.md

- 「所有儀器都鎖在同一個 10 MHz 參考時脈上，常用銣原子鐘，有時再用 GPS 馴服。」

## speech/離子阱與中性原子演講稿.md

- 「大自然保證同一種同位素的每一顆原子完全相同，能階頻率可以精確到小數點後很多位——原子鐘就是用這個特性。所以量子位元不需要逐顆調頻」

## animations/js/scenes/01_bloch.js（index.html#bloch）

- 「Ramsey / 失相 (T2)：赤道上的態因頻率失諧而繞 z 軸進動，雜訊使相位擴散、向量縮短。」
- `ui.radio([['rabi', 'Rabi 振盪'], ['ramsey', 'Ramsey 進動 + T2'], ['t1', 'T1 能量弛豫'], ['manual', '手動 θ / φ']], …)`
- `ui.slider('失諧 Δ（Ramsey）', 0, 2, 0.05, detune, …)`，預設 `detune = 0.8`、`T2 = 6`
- `const a = detune * t * 1.5, r = Math.exp(-t / T2); vec.set(r * Math.cos(a), r * Math.sin(a), 0);`；`if (t > 12) { reset(); t = 0; }`
- 計算：每輪圈數 = 1.5·Δ·12 ÷ 2π ≈ 2.86·Δ（Δ = 0.5 → 1.4 圈；0.8 → 2.3；1 → 2.9；1.5 → 4.3；2 → 5.7）

## animations/js/peripherals/10_bringup.js（peripherals.html#bringup）

- 「⑤ Rabi（找 π 脈衝振幅）→ ⑥ Ramsey（精修頻率、T₂*）」
- `ramsey: '兩個 π/2 之間等待時間 τ，條紋頻率 = 失諧量 → 修正頻率；包絡給出 T₂*'`
- 插圖：`0.5 + 0.45 * Math.exp(-t / 6) * Math.cos(2 * Math.PI * 0.6 * t)`，τ 0–10 μs

## animations/js/peripherals/06_electronics.js（peripherals.html#electronics）

- 「所有儀器鎖在同一個 10 MHz 參考時脈（常用銣原子鐘）與觸發網路上，確保相位一致、時序精確。」
- `['clock', '銣原子鐘 / 10 MHz 分配', 0xffd166]`（機櫃最上層）；`const pulse = (clkT % 1) < 0.15;`

## Wikipedia

- Second：the SI second is defined by the caesium-133 hyperfine transition frequency, 9,192,631,770 Hz.
- Atomic clock：an electronic oscillator is locked to the frequency of an atomic transition by feedback; GPS satellites carry atomic clocks.
- Ramsey interferometry：two π/2 pulses separated by a period of free evolution; the accumulated phase difference is read out as a transition probability.
- Quantum sensor／Nitrogen-vacancy center／Atom interferometer：NV 中心磁力計、原子干涉重力儀。
- Global Positioning System：receivers compute position from the time signals broadcast by satellites.
- Network Time Protocol：stratum 0 reference clocks such as atomic clocks and GPS clocks.
