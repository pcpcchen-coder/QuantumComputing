# Q025 來源筆記（逐字引文）

查核日：2026-11-18。課綱、簡報、動畫程式由製作代理讀取。程式由製作代理實際執行。

## 課綱（academy/lessons/Q025/lesson.json）

- 課程主題「E_J 與 E_C：兩個能量尺度」；階段「第二階段 硬體怎麼做」；模組「QM02 超導量子位元：從超導到 transmon」。
- 學習目標「知道 E_J／E_C 比值決定量子位元的性格，以及電荷色散為什麼會被壓下來」。
- 動手任務「在場景掃描 E_J／E_C，記錄非諧性與電荷色散的變化」；孩子獨立改造「找出一個「非諧性夠、電荷雜訊又小」的折衷點並說明理由」；好玩機制「設計改造」。
- 作品「E_J／E_C 掃描圖」；家長課前準備「index.html#potential」；生活技能支線「在兩個互相衝突的目標中取捨」。
- 常見誤解與安全提醒「E_J／E_C 越大不是越好；非諧性會跟著變小」。
- 沿用簡報頁：JJ_Microwave_Readout_Talk.pptx p15、p19；transmon.pptx p14–15；沿用 3D 場景：i:potential、tr:potential。
- Q024 brief：「JJ 是非線性電感」「知道 JJ 的電感會隨電流改變，這個非線性是做出量子位元的關鍵」。Q026 brief：「傾斜洗衣板」「用相位粒子在洗衣板位勢中的運動理解 RCSJ 模型與 I–V 遲滯」「在場景加大偏壓電流，記錄粒子何時從井中滑出」。

## 簡報（python-pptx 擷取）

- JJ_Microwave_Readout_Talk p14「JJ 是一個『非線性電感』」；備註「它的值會隨相位、也就是隨流過的電流改變——這就是非線性」「把它和電容並聯，就得到一個非線性振盪器，也就是 transmon 量子位元。」
- JJ_Microwave_Readout_Talk p15「兩個能量尺度：EJ 與 EC」「H = 4EC(n̂ − ng)² − EJ cos φ̂」；表「約瑟夫森能 EJ｜EJ = Φ0 Ic / 2π = ħ Ic / 2e｜Cooper pair 穿隧的耦合能（位勢深度）｜接面面積、氧化層 → Ic｜Ic = 30 nA → ≈ 15 GHz」
  「充電能 EC｜EC = e² / 2CΣ｜多加一顆電子的靜電能（『質量』的倒數）｜總電容 CΣ（含大電容板）｜CΣ = 80 fF → ≈ 240 MHz」；「類比：一顆『質量 ∝ 1/EC』的粒子在『深度 ∝ EJ』的餘弦井中運動；EJ/EC 決定量子位元類型」；
  備註「EC 越小、粒子越重、越不容易被量子漲落晃動。」「ng 是環境中背景電荷造成的偏移。」
- JJ_Microwave_Readout_Talk p18「以 JJ 為核心的量子位元家族」：「電荷（CPB）｜小島 + 1 JJ｜~1｜……｜大｜最早的超導量子位元；對電荷雜訊極敏感」「Transmon｜JJ/SQUID ∥ 大電容｜50–100｜4–6 GHz｜−200～−300 MHz｜業界主流；抗電荷雜訊、結構簡單」「數值為典型範圍，實際依設計而異」；
  備註「最早的是電荷量子位元，也叫 Cooper pair box，EJ 和 EC 差不多大，它對環境中的背景電荷非常敏感」「Transmon 就是在電荷量子位元旁邊並聯一個大電容，把 EJ/EC 拉到 50 到 100」。
- JJ_Microwave_Readout_Talk p19「Transmon 深入：EJ/EC 與電荷色散」「EJ/EC 越大，能階越平直」「ħω01 ≈ √(8EJEC) − EC」「α ≈ −EC（只以冪次下降）」「εm ∝ e−√(8EJ/EC)（指數下降）」；
  備註「橫軸是背景電荷 ng——它來自基板或介面中隨機跳動的電荷，是一種無法完全消除的雜訊。」「EJ/EC 等於 1 的時候，能階隨 ng 劇烈起伏，只要背景電荷一跳，量子位元頻率就跟著變，相干性很差。比值增加到 5、10，起伏迅速變小；到 50，能階幾乎是平的。」
  「我們犧牲一點點非諧性，換來對電荷雜訊幾乎免疫。」「把 EJ/EC 從 1 拉到 50，右下角的插圖就是這張電荷色散圖，會即時更新。」
- transmon.pptx p14「非諧性：能階不再等距」「Transmon：越上越密」「E12 比 E01 低 283 MHz」；備註「非諧性 α = E12 − E01 = −283 MHz，遠大於控制脈衝的頻寬（約數十 MHz），所以可以只操作最低兩個能階。」
- transmon.pptx p15「為何 EJ/EC 要大」「約 3 萬倍」「EJ/EC 從 10 到 60，電荷色散 62.8 MHz → 1.9 kHz」「只少兩成」「同一範圍內，非諧性 −353 → −283 MHz」「電荷色散隨 √(8EJ/EC) 指數下降，非諧性只以冪次下降。大電容換來對電荷雜訊幾乎免疫。」；
  備註「電荷色散是 f01 隨背景電荷 n_g 的最大漂移量，E_C 固定為 250 MHz，數值解。Cooper pair box 的 E_J/E_C 約 1，頻率會被電荷雜訊大幅擾動」。

## 維基百科（原始 wikitext，2026-11-18 取得）

- Transmon：「a type of superconducting charge qubit designed to have reduced sensitivity to charge noise」「developed by……at Yale University and Université de Sherbrooke in 2007」
  「The transmon achieves its reduced sensitivity to charge noise by significantly increasing the ratio of the Josephson energy to the charging energy. This is accomplished through the use of a large shunting capacitor.」
  「both are described by the same Hamiltonian, with the only difference being the EJ/EC ratio」「The benefit of increasing the EJ/EC ratio is the insensitivity to charge noise……The disadvantage is the reduced anharmonicity」
  「while the variation of E10 with respect to ng tend to decrease exponentially with EJ/EC, the anharmonicity only has a weaker, algebraic dependence on EJ/EC as ~(EJ/EC)^−1/2」。
- Charge qubit：「a charge qubit (also known as Cooper-pair box) is a qubit whose basis states are charge states (i.e. states which represent the presence or absence of excess Cooper pairs in the island)」「ng = CgVg/(2e) is a control parameter known as effective offset charge」。

## 動畫程式

- animations/js/scenes/04_potential.js（index.html#potential）：第 6–8 行場景說明「調整 E_J/E_C：比值小（電荷量子位元）時能階對背景電荷 n_g 極敏感；比值大（transmon，約 50）時電荷色散指數級下降，但非諧性只以冪次減少。」
  第 13 行 `let ratio = 50, mode = 'transmon'`；第 114–116 行按鈕「LC 諧振子（線性）」「JJ / Transmon（非線性）」、滑桿「E_J / E_C（對數刻度）」、按鈕「CPB：E_J/E_C = 1」「10」「Transmon：50」；
  第 118 行小圖標題「電荷色散：能階隨背景電荷 n_g 的變化」、第 123 行座標「背景電荷 n_g」「(E − E₀)/E₀₁」、第 124 行三色 #4f8cff、#ff5a5f、#2ecc71。
- animations/transmon-3d.html 第 1 章 #capacitor 分頁：第 880 行「十字金屬板就是 transmon 的並聯電容 C_Σ（約 77.5 fF），JJ 自己的電容只有 1–2 fF」；
  第 882 行「E_C = e²/2C_Σ 被壓低，背景電荷雜訊造成的頻率漂移隨 √(8E_J/E_C) 指數下降」；第 883 行「f₀₁ ≈ √(8E_J E_C) − E_C，α ≈ −E_C。電容太大，α 太小，脈衝容易漏到 |2⟩。」
  第 887–889 行滑桿「C_Σ」5–200、讀數「電容 C_Σ」「充電能 E_C/h」「E_J/E_C」「f₀₁」「非諧性 α」「電荷色散」「判斷」、按鈕「回到 77.5 fF」；第 890 行「E_J/h 固定為 15 GHz……十字板粗細只是示意電容大小，未按比例」；
  第 1206 行判斷「電荷雜訊主導（接近 Cooper pair box）」「transmon 區間」「非諧性偏小，閘需放慢」。
- transmon-3d.html 第 3 章（#potential）：「脈衝越短越強、頻譜越寬，就越容易碰到 4.93 GHz，所以脈衝不能無限縮短……這也是非諧性越大、閘可以做得越快的原因。」

## 實跑紀錄（ejec_scan.py，Python 3，無套件）

見 `classroom.py` 執行時寫入的 `04_解答.md`；重點（E_J/h = 15 GHz）：10 fF → 比值 7.7、−2.44 GHz、940 MHz；20 fF → 15.5、−1.33 GHz、53.1 MHz；77.5 fF → 60.0、−283 MHz、1.9 kHz；
200 fF → 154.9、−104 MHz、< 0.1 Hz。標準「非諧性至少 200 MHz、電荷色散低於 10 kHz」兩條都符合的電容 66.0–107.0 fF（比值 51.1–82.9）。與 Node 以頁面程式（capStats、fmtF）實算的讀數相同。
