# Q020 來源筆記（逐字引文）

查核日：2026-11-18。課綱、簡報、動畫程式由製作代理讀取。程式由製作代理實際執行。

## 課綱（academy/lessons/Q020/lesson.json）

- 課程主題「磁通量子化 Φ₀ = h/2e」；階段「第二階段 硬體怎麼做」；模組「QM02 超導量子位元：從超導到 transmon」；模組內課次 4；難度 3。
- 學習目標「知道超導環裡的磁通只能是 Φ₀ 的整數倍，以及 2e 從哪裡來」。
- 動手任務「用繩圈與相位時鐘貼紙，示範繞一圈相位必須回到原點」；孩子獨立改造「算出 Φ₀ 的數值，換算成地磁場穿過多大的面積」；好玩機制「解鎖成就」。
- 作品「環形相位圖」；家長課前準備「繩子、時鐘貼紙、計算機」；生活技能支線「用單位換算感受尺度」。
- 常見誤解與安全提醒「分母是 2e 而不是 e，正是 Cooper pair 帶兩個電子電荷的證據」。
- 沿用簡報頁：JJ_Microwave_Readout_Talk.pptx p9；沿用 3D 場景：無；需新增素材「★ 磁通量子化場景」。
- Q019 brief：「Cooper pair 與能隙」；Q019 講稿：所有電子對進入同一個量子狀態，整塊超導體只需要一個相位來描述。
  Q021 brief：「彈簧、單擺與 LC 電路」「把力學振盪和電磁振盪對應起來：質量↔電感、彈簧↔電容」。

## 簡報（slides/JJ_Microwave_Readout_Talk.pptx p9，python-pptx 擷取）

- 標題「磁通量子化：Φ₀ = h / 2e」；圖說「穿出紙面的磁通 Φ」；公式「∮ ∇φ · dl = 2π n」「Φ = n · Φ0」「Φ0 = h / 2e ≈ 2.068 × 10−15 Wb」。
- 條列「波函數繞超導環一圈必須回到原值 → 相位變化只能是 2π 的整數倍」「環內磁通因此被「量子化」為 Φ0 的整數倍」
  「分母是 2e 而不是 e —— 直接證明載流子是 Cooper pair」「Φ0 是超導電路的「自然單位」：SQUID 的調頻週期、JJ 電感、AC Josephson 頻率都由它決定」。
- 備註「既然整塊超導體共享一個波函數，那麼沿著一個超導環繞一圈，波函數必須回到自己，相位的總變化只能是 2π 的整數倍。這個條件換算過來，就是環內的磁通只能是一個基本單位 Φ0 的整數倍。」
  「Φ0 等於 h 除以 2e，約 2.07 乘 10 的負 15 次方韋伯。這裡分母是 2e 而不是 e，正是實驗上證明「載流子是成對電子」的直接證據。」

## 維基百科（原始 wikitext，2026-11-18 取得）

- Magnetic flux quantum：「The magnetic flux through some contour is defined as the magnetic field multiplied by the loop area. In some physical systems, such as in superconductors, the magnetic flux can only take certain fixed (or, quantized) values. The values allowed to be taken by the magnetic flux are integer multiples of the magnetic flux quantum.」
- 同條註腳：「In superconductors, for instance, the flux quantum is half the Dirac magnetic flux quantum because Cooper pairs have a charge of 2e.」
- 同條：「The quantization of the magnetic flux originates from the requirement that the wave function describing a particle must be single-valued.」「the wave function can only remain single-valued if the magnetic flux takes on a quantized value for which the phase shift is equal to 2π」。
- 同條：「Φ0 = h/(2e) … is a combination of fundamental physical constants: the Planck constant h and the electron charge e. Its value is, therefore, the same for any superconductor.」
- 同條：「the supercurrent in a superconductor is carried by Cooper pairs which have twice the charge of an electron q = 2e」。
- 同條：「The phenomenon of flux quantization was first discovered in superconductors experimentally by B. S. Deaver and W. M. Fairbank, and independently by R. Doll and M. Näbauer, in 1961.」參考文獻標題「Experimental Evidence for Quantized Flux in Superconducting Cylinders」「Experimental Proof of Magnetic Flux Quantization in a Superconducting Ring」（Physical Review Letters 7, 1961）。
- 同條：「The magnetic flux frozen in a loop/hole (plus its λL-layer) will always be quantized. However, the value of the flux quantum is equal to Φ0 only when the path … can be chosen so that it lays in the superconducting region without screening currents」；「The flux quantization is a key idea behind a SQUID」。
- Weber (unit)：「the weber (symbol: Wb) is the unit of magnetic flux in the International System of Units」「One weber is also the total magnetic flux across a surface of one square meter perpendicular to a magnetic flux density of one tesla」。
- Earth's magnetic field：「The 13th International Geomagnetic Reference Field in 2019 recorded approximately 60000 nT … over Siberia and 30000 nT … over Brazil」「a strong refrigerator magnet has a field of about 10000 μT」。

## 互動動畫程式

- animations/index.html 第 26–35 行：#panel、#controls、#inset-wrap；第 42、45 行載入 03_jj.js、06_squid.js。
- animations/js/scenes/03_jj.js 第 3–10 行：id 'jj'、標題「約瑟夫森接面（JJ）的結構與穿隧」；說明「兩側各有自己的巨觀相位 φ1、φ2（圖中旋轉的「相位鐘」）」。
  第 30–39 行：相位鐘（藍 0x4f8cff、紅 0xff5a5f）與金色大字；第 66–68 行：滑桿「偏壓電流 I / Ic」0–1.6、預設 0.5；第 95、102–105 行：相位差趨向 asin(I/Ic)、兩根指針一起轉、字「φ = φ₂ − φ₁ = …°」；第 108–113 行：電子對速度 1.6 sin φ。
- animations/js/scenes/06_squid.js 第 3–8 行：id 'squid'、標題「DC SQUID：可用磁通調整的 JJ」；說明「由於磁通量子化（Φ₀ = h/2e ≈ 2.07 × 10⁻¹⁵ Wb），E_J 隨 Φ 以 Φ₀ 為週期變化」。
  第 12–24 行：鋁環與兩個接面；第 33–42 行：青色磁通箭頭、環中央「Φ = … Φ₀」、環流光點；第 51 行：滑桿「外加磁通 Φ / Φ₀」−1～1；
  第 57–63 行：右下小圖 f₀₁ 對 Φ / Φ₀；第 69–80 行：箭頭長度 1.8 × Φ、光點角速度 ∝ sin(πΦ/Φ₀)（註解「示意」）、|sin| ≤ 0.03 時隱藏。
- animations/js/core.js 第 159–162 行：箭頭長度為 0 時隱藏；第 339–369 行：ui.button、ui.slider。

## 實跑紀錄（flux_scale.py，Python 3，無套件）

見 `classroom.py` 執行時寫入的 `04_解答.md`；製作代理以同樣常數另行計算：
Φ₀ = 6.62607015 × 10⁻³⁴ ÷ (2 × 1.602176634 × 10⁻¹⁹) = 2.0678 × 10⁻¹⁵ Wb；h/e = 4.1357 × 10⁻¹⁵ Wb（Φ₀ 的 2 倍）；
面積 = Φ₀ ÷ B：30 μT 68.9 μm²（每邊 8.30 μm）、50 μT 41.4 μm²（每邊 6.43 μm）、60 μT 34.5 μm²（每邊 5.87 μm）；1000 ÷ 6.43 ≈ 155；
8 張貼紙：45° → 360°（1 圈）、22.5° → 180°（0.5 圈）、90° → 720°（2 圈）、30° → 240°（0.67 圈）。
動畫 06_squid.js 的頻率小圖（d = 0）：f₀₁(0) = √(8 × 20 × 0.25) − 0.25 = 6.07 GHz、f₀₁(0.25) = 5.07、f₀₁(0.5) = max(0, −0.25) = 0、f₀₁(1) = 6.07。
