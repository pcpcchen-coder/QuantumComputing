# Q031 來源筆記（逐字引文）

查核日：2026-11-18。課綱、簡報、動畫程式由製作代理讀取（簡報以 python-pptx 擷取投影片文字與講者備註）。程式由製作代理實際執行。
維基百科 Quantum decoherence 的引文沿用 Q014 來源筆記（`academy/authoring/q014/source-notes.md`，oldid=1384689551，2026-11-18 取得），本集未重新開啟頁面。

## 課綱（academy/lessons/Q031/lesson.json）

- 課程主題「退相干：敵人在哪裡」；階段「第二階段 硬體怎麼做」；模組「QM02 超導量子位元：從超導到 transmon」。
- 學習目標「認識 TLS 缺陷、準粒子、輻射、磁通雜訊等退相干來源與對策」。
- 動手任務「把雜訊來源寫成嫌犯卡，依證據（T₁、T₂ 變化）配對對策」；孩子獨立改造「替其中一個嫌犯設計一個量測實驗來確認」；好玩機制「偵探辦案」。
- 作品「雜訊來源關係圖」；家長課前準備「嫌犯卡模板；index.html#bloch」；生活技能支線「從症狀推回原因」。
- 常見誤解與安全提醒「T₂ 永遠不會大於 2T₁；看到這種數據要先懷疑量測」。
- 沿用簡報頁：JJ_Microwave_Readout_Talk.pptx p6、p24；沿用 3D 場景：i:bloch。
- Q030 brief：「晶片長什麼樣子」「在 Xmon 晶片上找出量子位元、讀取腔、饋線與控制線，理解頻率多工」。
- Q032 brief：「模組發表：設計我的 transmon」「選定頻率、非諧性、E_J／E_C，說明每個數字背後的取捨」。

## 簡報（slides/JJ_Microwave_Readout_Talk.pptx）

- p6「量子位元的品質指標」：「T1：能量弛豫時間 |1⟩ 自發放出能量回到 |0⟩ 的時間常數。最佳 transmon 約 0.1–1 ms。」
  「T2：相位相干時間 疊加態相位資訊保留多久；T2 ≤ 2T1。受低頻雜訊（磁通、電荷）影響。」
  「所有指標都和 JJ 品質（缺陷、準粒子）與讀取電路設計（Purcell 效應）有關」。
  備註：「T2 是相位相干時間：疊加態的相對相位能維持多久。它受到低頻雜訊影響，例如磁通雜訊、電荷雜訊。理論上 T2 最多是 2 倍 T1。在 3D 場景 1 中可以切到「Ramsey 進動 + T2」模式，會看到向量在赤道上轉、同時越縮越短，那就是失相。」
- p24「退相干來源與對策」：
  「二能階系統（TLS）缺陷：介面氧化物、JJ 阻障內的原子缺陷吸收量子位元能量 → T1 下降、頻率漂移 / 對策：表面處理、Ta/Nb 電容板、藍寶石/高阻矽、增大電容板間距」
  「準粒子（Quasiparticle）：紅外線、宇宙射線拆散 Cooper pair；準粒子穿隧 JJ 造成能量損失 / 對策：紅外屏蔽、Eccosorb 濾波、準粒子陷阱、間隙工程」
  「磁通雜訊（1/f）：表面自旋造成低頻磁通漂移 → 可調頻量子位元 T2 下降 / 對策：停在甜蜜點、不對稱 SQUID、磁屏蔽」
  「熱光子與 Purcell 效應：讀取腔中殘留熱光子造成失相；經讀取腔向外輻射造成 T1 下降 / 對策：輸入線衰減器、Purcell 濾波器、良好接地與封裝」。
  備註：「在金屬和基板的介面、氧化層裡，有一些原子尺度的缺陷，它們本身像小小的二能階系統，會把量子位元的能量吸走，造成 T1 下降，還會讓頻率隨時間漂移。對策是改善表面處理、換材料，例如鉭電容板，以及把電場集中區域設計得離有損介面遠一點。」
  「正常情況下 10 mK 幾乎沒有被拆散的電子，但紅外線、甚至宇宙射線，都可能打斷 Cooper pair 產生準粒子，它們穿隧過 JJ 時會帶走量子位元的能量。對策是紅外屏蔽、濾波器和準粒子陷阱。」
  「第三是磁通雜訊，主要影響可調頻量子位元。對策是停在甜蜜點、用不對稱 SQUID。」

## 簡報（slides/QC_Peripheral_Systems_Talk.pptx）p6「為什麼要 10 mK？」

- 「讀取腔中有熱光子 → 量子位元失相（T2 下降）」「準粒子增加 → 穿隧過 JJ 帶走能量（T1 下降）」（引文同 Q014 來源筆記）。

## Quantum decoherence（Wikipedia，oldid=1384689551，引文見 Q014 來源筆記）

- 「The relaxation time T₁ characterizes how quickly a qubit loses energy to its environment as it decays from the excited state |1⟩ to the ground state |0⟩.」
- 「T₂ is commonly measured via the Ramsey interference experiment, in which a qubit is prepared in a superposition state and freely evolves, precessing, for a variable interval.」
- 「T_2 ≤ 2T_1 … with equality only when energy relaxation is the sole source of decoherence.」

## 互動動畫程式（animations/）

- index.html：第 40 行載入 `js/scenes/01_bloch.js`；`#panel`、`#controls`、右下 `#inset-wrap`。
- js/scenes/01_bloch.js：`id: 'bloch'`（第 3 行）；desc「Rabi 振盪：在共振微波驅動下，狀態繞 x 軸旋轉」「Ramsey / 失相 (T2)：赤道上的態因頻率失諧而繞 z 軸進動，雜訊使相位擴散、向量縮短」「能量弛豫 (T1)：|1⟩ 會自發放出能量回到 |0⟩」（第 7–9 行）；
  第 35–36 行北極標「|0⟩」、南極標「|1⟩」；第 41 行金色箭頭 0xe0a54a；`let mode = 'rabi'`、`T2 = 6, T1 = 5`（第 49–50 行）；
  `ui.radio([['rabi', 'Rabi 振盪'], ['ramsey', 'Ramsey 進動 + T2'], ['t1', 'T1 能量弛豫'], ['manual', '手動 θ / φ']], …)`（第 55 行，每按一次 reset）；
  插圖「激發態機率 P(|1⟩) 隨時間變化」，橫軸 0–12、縱軸 0–1（第 64–66 行）；`if (t > 12) { reset(); t = 0; }`（第 75 行）；
  Rabi：`vec.set(0, -Math.sin(a), Math.cos(a))`，a = 1.2Ωt（第 76–78 行）；Ramsey：`r = Math.exp(-t / T2)`（第 80–81 行）；T1：`vec.set(0, 0, 1 - 2 * pe)`（第 83–84 行）；
  尖端小字 `P(1) = …`（第 97–98 行）；讀數 `|r| = … ${L < 0.98 ? '（混態：失去相干性）' : '（純態）'}`（第 100 行）。
- js/core.js：ui.button／ui.radio／ui.slider／ui.readout 都放進 `#controls`（第 338–370 行）；radio 初值加 on（第 349 行）；dt 每格上限 0.05 秒（第 269 行）。
- css/style.css：`#panel` 在左、max-height calc(100vh − 96px)、可捲動（第 32 行）。

## 重新計算（suspect_check.py，製作代理實跑）

```
鐵律：T1 = 50 μs → 2T1 = 100 μs；T2 = 150 μs > 100 μs → 不可能
動畫 T1 模式：P(1) = e^(−t/5)；z = 1 − 2e^(−t/5)；t = 3.47 時 z = 0（經過球心）；t = 12 時 z = 0.82
動畫 Ramsey 模式：|r| = e^(−t/6)；t = 12 時 0.14；P(1) 固定 0.50；每圈 2π/1.2 = 5.24
動畫 Rabi 模式：P(1) = sin²(0.6t)；t = 2.62 到 |1⟩、5.24 回 |0⟩；|r| = 1（純態）
```
