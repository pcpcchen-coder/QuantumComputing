# Q028 來源筆記（逐字引文）

查核日：2026-11-20。課綱、簡報、動畫程式由製作代理讀取；維基百科為 2026-11-20 取得的原始 wikitext。

## 課綱（academy/lessons/Q028/lesson.json）

- 課程主題「量子位元家族圖鑑」；階段「第二階段 硬體怎麼做」；模組「QM02 超導量子位元：從超導到 transmon」。
- 學習目標「比較 transmon、fluxonium、電荷與相位量子位元的結構與優缺點」。
- 動手任務「為四種量子位元各做一張圖鑑卡：結構、頻率、優點、弱點」；孩子獨立改造「自己設計一張「理想量子位元」卡，說明它要跟誰借優點」；好玩機制「解鎖成就（圖鑑卡）」。
- 作品「量子位元圖鑑卡」；家長課前準備「圖鑑卡模板」；生活技能支線「整理比較表」。
- 常見誤解與安全提醒「沒有在所有指標都最好的量子位元；廠商選擇各有考量」。
- 沿用簡報頁：JJ_Microwave_Readout_Talk.pptx p18–20；沿用 3D 場景：無；需新增素材「◆ 圖鑑卡模板」（本集教材的列印包第 1–2 頁）。
- Q026 brief「傾斜洗衣板」「用相位粒子在洗衣板位勢中的運動理解 RCSJ 模型與 I–V 遲滯」。Q027 brief「SQUID：用磁場轉頻率」「知道兩個 JJ 並聯成環可以用磁通調整頻率，認識甜蜜點」。
  Q029 brief「晶片怎麼做：雙角度蒸鍍」「理解 Dolan bridge 兩次斜向蒸鍍如何做出重疊的 JJ」。

## 簡報（python-pptx 擷取）

- JJ_Microwave_Readout_Talk p16「RCSJ 模型與傾斜洗衣板位勢」；備註「早期的『相位量子位元』就是在接近 Ic 的偏壓下，利用井中最低的兩個能階。現代的 transmon 則是在不加偏壓的情況下工作，也就是洗衣板完全水平。」
- JJ_Microwave_Readout_Talk p18「以 JJ 為核心的量子位元家族」，表（類型｜電路結構｜EJ/EC｜頻率｜非諧性｜特點）：
  「電荷（CPB）｜小島 + 1 JJ｜~1｜5–10 GHz｜大｜最早的超導量子位元；對電荷雜訊極敏感」
  「Transmon｜JJ/SQUID ∥ 大電容｜50–100｜4–6 GHz｜−200～−300 MHz｜業界主流；抗電荷雜訊、結構簡單」
  「磁通（Flux）｜超導環 + 3–4 JJ｜~50｜1–10 GHz｜大｜以環流方向編碼；對磁通雜訊敏感」
  「Fluxonium｜1 JJ ∥ 超電感（JJ 陣列）｜~1–10｜0.1–1 GHz｜極大｜T1 可達 ms；低頻、高非諧性」
  「相位（Phase）｜電流偏壓 1 JJ｜≫ 1｜5–10 GHz｜中｜洗衣板井中能階；已較少使用」；
  「共同點：都靠 JJ 提供『無耗散的非線性』；差別在 EJ/EC 比值與電路拓樸」「數值為典型範圍，實際依設計而異」。
  備註「JJ 加上不同的電路拓樸，就形成不同的超導量子位元。」「最早的是電荷量子位元，也叫 Cooper pair box，EJ 和 EC 差不多大，它對環境中的背景電荷非常敏感，相干時間很短。」
  「Transmon 就是在電荷量子位元旁邊並聯一個大電容，把 EJ/EC 拉到 50 到 100，對電荷雜訊幾乎免疫，結構簡單，是目前業界主流，Google、IBM 都用它的變形。」
  「Fluxonium 是一個 JJ 並聯一個『超電感』，這個超電感通常是由上百個大 JJ 串成的陣列。它頻率低、非諧性極大，T1 可以到毫秒等級，是近年很熱門的方向。」「相位量子位元就是剛才洗衣板的那種，現在比較少用了。」
- JJ_Microwave_Readout_Talk p19「Transmon 深入：EJ/EC 與電荷色散」；備註「橫軸是背景電荷 ng——它來自基板或介面中隨機跳動的電荷」「EJ/EC 等於 1 的時候，能階隨 ng 劇烈起伏，只要背景電荷一跳，量子位元頻率就跟著變，相干性很差……到 50，能階幾乎是平的。」
  「【切換到 3D 場景 4】把 EJ/EC 從 1 拉到 50，右下角的插圖就是這張電荷色散圖」。
- JJ_Microwave_Readout_Talk p20「Transmon 典型參數」「4–6 GHz｜f01 量子位元頻率」「−200～−300 MHz｜非諧性 α ≈ −EC」「50–100｜EJ/EC 比值」「0.1–1 ms｜T1（最佳實驗）」。
- JJ_Microwave_Readout_Talk p21「第二次斜角蒸鍍 Al（−θ）：在橋正下方與第一層重疊」（下一堂預告用）。

## 維基百科（原始 wikitext，2026-11-20 取得）

- Charge qubit：「a charge qubit (also known as Cooper-pair box) is a qubit whose basis states are charge states (i.e. states which represent the presence or absence of excess Cooper pairs in the island)」
  「a charge qubit is formed by a tiny superconducting island coupled by a Josephson junction……to a superconducting reservoir」「Typical T2 coherence times for a charge qubit are on the order of 1–2 μs.」
  「In 1999, coherent oscillations in the charge qubit were first observed by Nakamura et al.」
- Transmon：「developed by……at Yale University and Université de Sherbrooke in 2007」「both are described by the same Hamiltonian, with the only difference being the EJ/EC ratio」
  「This is accomplished through the use of a large shunting capacitor.」另列 T1「approximately 30 μs to 40 μs」「95 μs」「up to 0.3 ms」（旁白不引用，只用簡報 p20 範圍）。
- Fluxonium：「insensitive to offset charge noise. It is constructed from a Josephson junction, a capacitor, and a “superinductor”」「first proposed……by an experimental group at Yale University led by Michel Devoret in 2009」
  「long coherence times and high anharmonicity」「the design requires complex fabrication methods, and is therefore difficult to scale」「millisecond-level coherence times」
  「some companies like D-Wave, Atlantic Quantum, and Qilimanjaro focused specifically on developing fluxonium-based quantum computing hardware」「the transmon suffers from low anharmonicity, Purcell decay, and leakage」
  「The most common operating point is the half-flux point……because it is insensitive to flux noise at first order」「a resonant frequency between 100 MHz and 1 GHz, and can have a relaxation time of over 1 ms」
  「operating at lower frequencies usually means slower gate times」；圖說「a collection of larger area Josephson junctions and one smaller area Josephson junction」。
- Phase qubit：「For phase qubit, this ratio is on the order of 10⁶」「The quantization based on phase of the Josephson junction was first demonstrated experimentally by John Clarke, Michel Devoret and John M. Martinis in 1985, for which they were awarded the Nobel Prize in Physics in 2025.」
  「A phase qubit is a current-biased Josephson junction, operated in the zero voltage state with a non-zero current bias.」「the lowest (ground to first excited state) transition at an energy E01 ≈ ħωp」
  「The phase qubit uses the lowest two energy levels in the local minimum」「Hence the phase qubit has a tunable energy splitting.」
  「fluctuations in current generate fluctuations in the plasma frequency, which causes dephasing of the quantum states」。

## 動畫程式

- animations/js/scenes/04_potential.js（index.html#potential）：第 8 行場景說明「比值小（電荷量子位元）時能階對背景電荷 n_g 極敏感；比值大（transmon，約 50）時電荷色散指數級下降」；
  第 13 行 `let ratio = 50, mode = 'transmon'`；第 116 行按鈕「CPB：E_J/E_C = 1」「10」「Transmon：50」；第 118 行小圖標題「電荷色散：能階隨背景電荷 n_g 的變化」；第 124 行三色 #4f8cff、#ff5a5f、#2ecc71。
- animations/js/scenes/05_washboard.js（index.html#washboard）：第 9 行場景說明「早期的相位量子位元就是利用這些能階；現代 transmon 則在 I = 0（不傾斜）下工作」；
  第 15 行 `let iB = 0.3, Q = 8, phi = 0, v = 0, follow = true`；第 21 行標籤「相位粒子 φ」；第 60 行「位障 ΔU ≈ x.xx E_J」；第 64 行滑桿「偏壓電流 I / Ic（傾斜）」；
  第 116 行「零電壓態：相位被困在井中做電漿振盪」；第 117 行「ω_p(I) = ω_p0 (1 − (I/Ic)²)^{1/4} = x.xx ω_p0」。
- animations/transmon-3d.html 第 1 章：第 874 行「中央的十字金屬板就是 transmon 的大電容，下端經由 SQUID（兩個約瑟夫森結）接地」；第 880 行「十字金屬板就是 transmon 的並聯電容 C_Σ」；
  第 883 行「電容太大，α 太小，脈衝容易漏到 |2⟩」；第 887–889 行滑桿「C_Σ」、讀數、按鈕「回到 77.5 fF」；第 1206 行判斷「電荷雜訊主導（接近 Cooper pair box）」「transmon 區間」「非諧性偏小，閘需放慢」。

## Node 實算（頁面同一段程式）

- 04_potential.js：比值 50 三條線平；比值 1 藍 0～0.595、紅 1.595～4.117（截在 2.6）、綠整條貼上緣。
- 05_washboard.js：位障 0.30 → 1.148、0.90 → 0.0600；ω_p 0.30 → 0.977、0.90 → 0.660。
- transmon-3d capStats／fillCap：77.5 fF → 250 MHz、60.0、5.21 GHz、−283 MHz、1.9 kHz、transmon 區間；20 fF → 969 MHz、15.5、9.69 GHz、−1.33 GHz、53.1 MHz、電荷雜訊主導。
