# Q026 來源筆記（逐字引文）

查核日：2026-11-18（維基百科原始 wikitext 於 2026-11-20 取得）。課綱、簡報、動畫程式由製作代理讀取。程式由製作代理實際執行。

## 課綱（academy/lessons/Q026/lesson.json）

- 課程主題「傾斜洗衣板」；階段「第二階段 硬體怎麼做」；模組「QM02 超導量子位元：從超導到 transmon」；難度 4。
- 學習目標「用相位粒子在洗衣板位勢中的運動理解 RCSJ 模型與 I–V 遲滯」。
- 動手任務「在場景加大偏壓電流，記錄粒子何時從井中滑出；用彈珠與波浪紙板模擬」；孩子獨立改造「解釋為什麼電流往下調時不會在同一點停下（遲滯）」；好玩機制「科學實驗」。
- 作品「洗衣板觀察紀錄」；家長課前準備「波浪紙板、彈珠；index.html#washboard」；生活技能支線「同一條件、不同歷史，結果可能不同」。
- 常見誤解與安全提醒「相位粒子是數學上的類比，不是真的有一顆球在跑」。
- 沿用簡報頁：JJ_Microwave_Readout_Talk.pptx p16；沿用 3D 場景：i:washboard。
- Q025 brief：「E_J 與 E_C：兩個能量尺度」。Q027 brief：「SQUID：用磁場轉頻率」「知道兩個 JJ 並聯成環可以用磁通調整頻率，認識甜蜜點」。

## 簡報（python-pptx 擷取）

- JJ_Microwave_Readout_Talk p15「兩個能量尺度：EJ 與 EC」；表「Cooper pair 穿隧的耦合能（位勢深度）」「多加一顆電子的靜電能（『質量』的倒數）」；
  「類比：一顆『質量 ∝ 1/EC』的粒子在『深度 ∝ EJ』的餘弦井中運動」；備註「EC 越小、粒子越重、越不容易被量子漲落晃動。」
- JJ_Microwave_Readout_Talk p16「RCSJ 模型與傾斜洗衣板位勢」「3D 場景 5：相位粒子在井中振盪，電流超過 Ic 即滾下坡」
  「C(ħ/2e) φ̈ + (ħ/2eR) φ̇ + Ic sin φ = I」「U(φ) = −EJ cos φ − (ħI/2e) φ」；
  表「電路量｜力學類比」「電容 C｜質量」「1/R（並聯電阻）｜摩擦」「偏壓電流 I｜傾斜角度」「井中振盪｜電漿頻率 ωp」「滾下坡｜dφ/dt ≠ 0 → 出現電壓」。
  備註：「真實的 JJ 除了理想的約瑟夫森元件，還並聯了自身的電容和一個電阻，這叫 RCSJ 模型。寫出電路方程式，會發現它和『一顆球在傾斜的洗衣板上滾動』的方程式完全一樣：電容扮演質量、電阻扮演摩擦、偏壓電流決定洗衣板傾斜多少。」
  「金色的球就是『相位粒子』。在小電流時它被困在某個井裡做小幅振盪，振盪頻率叫電漿頻率；這時相位不隨時間增加，所以沒有電壓。把電流拉超過 Ic，最後一個井消失，球開始一路滾下坡，dφ/dt 不為零，就出現了電壓。」
  「按『掃描』按鈕會把電流從 0 拉到 1.3 再降回來，右下角會畫出 I-V 曲線：低阻尼時有遲滯，電流降到 Ic 以下球還是繼續滾，直到回捕電流才停下來。」
  「早期的『相位量子位元』就是在接近 Ic 的偏壓下，利用井中最低的兩個能階。現代的 transmon 則是在不加偏壓的情況下工作，也就是洗衣板完全水平。」

## 維基百科（原始 wikitext，2026-11-20 取得）

- Phase qubit：「A phase qubit is a current-biased Josephson junction, operated in the zero voltage state with a non-zero current bias.」
  「This is the washboard potential, so-called because it has an overall linear dependence −I δ, modulated by the washboard modulation −I0 cos δ.」
  「The zero voltage state……corresponds to when the particle is trapped in one of the local minima in the washboard potential. These minima exist for bias currents |I| < I0……With the phase particle trapped in a minimum, it has zero average velocity and therefore zero average voltage. A Josephson junction will allow currents up to I0 to pass through without any voltage」
  「The voltage state……corresponds to the phase particle free-running down the slope of the potential, with a non-zero average velocity and therefore non-zero voltage. This behavior always occurs for currents I above the critical current, i.e. for |I| > I0, and for large resistances R also occurs for currents somewhat below the critical current……the zero-voltage and voltage branches overlap for some range of currents below the critical current, so the device behavior is hysteretic.」
  「which is known as the plasma frequency of the junction. This corresponds to the oscillation frequency of the phase particle in the bottom of one of the minima of the washboard potential.」「the plasma frequency approaches zero as the bias current approaches the critical current.」
  「The phase qubit uses the lowest two energy levels in the local minimum……The slope in the washboard potential is set by the bias current I」。
- Josephson effect，RCSJ model 一節：「The resistively capacitance shunted junction (RCSJ) model, or simply shunted junction model, includes the effect of AC impedance of an actual Josephson junction」
  「the AC impedance of the junction can be represented by a capacitor and a shunt resistor, both parallel to the ideal Josephson Junction」「I_ext = C_J dV/dt + I_c sin φ + V/R」。

## 動畫程式（animations/js/scenes/05_washboard.js，index.html#washboard）

- 第 4–5 行 title「RCSJ 模型：傾斜洗衣板位勢」、subtitle「U(φ) = −E_J cos φ − (ħI / 2e)·φ」。
- 第 6–9 行場景說明：「把真實 JJ 視為『理想 JJ ∥ 電阻 R ∥ 電容 C』（RCSJ 模型），相位差 φ 的運動就像一顆球在傾斜的洗衣板上滾動」「電容 ↔ 質量　• 1/R ↔ 摩擦　• 偏壓電流 ↔ 傾斜角度」
  「球在井底振盪 ↔ 電漿頻率 ω_p = √(2eIc/ħC)」「球滾下坡 ↔ dφ/dt ≠ 0 ↔ 出現電壓」「在井中，能量是量子化的（圖中短線）。早期的相位量子位元就是利用這些能階；現代 transmon 則在 I = 0（不傾斜）下工作。低阻尼（Q 大）時會看到遲滯：電流降回 Ic 以下，球仍持續滾動。」
- 第 15 行 `let iB = 0.3, Q = 8, phi = 0, v = 0, follow = true`；第 17 行 `Uf = (p) => -Math.cos(p) - iB * p`；第 20 行標籤「相位粒子 φ」。
- 第 60 行位障標籤「位障 ΔU ≈ ${dU.toFixed(2)} E_J」（iB ≥ 1 時隱藏，第 43 行）。
- 第 64–69 行：滑桿「偏壓電流 I / Ic（傾斜）」0–1.6、step 0.01、初值 0.3、toFixed(2)；滑桿「品質因子 Q（阻尼越小 Q 越大）」1–20、step 0.5、初值 8；按鈕「掃描：0 → 1.3 → 0（看遲滯）」「重設」；開關「相機跟隨相位粒子」。
- 第 74–83 行小圖「I–V 特性（RCSJ，低阻尼時有遲滯）」；軸「平均電壓 ⟨V⟩ / IcR」「I / Ic」；`ir = Math.min(1, 4 / (Math.PI * Q))`；文字「回捕電流 I_r ≈ 4Ic/πQ = ${ir.toFixed(2)} Ic」；青色曲線 #38c6d9、金色圓點 #e0a54a。
- 第 89–94 行掃描「14 秒完成」，0 → 1.3 → 0；第 95–99 行 `a = iB - sin(phi) - v/Q + 0.03*gauss()`；第 100 行 vAvg 平滑；第 110–113 行相機跟隨。
- 第 115–117 行讀數「電壓態：相位持續滾動，⟨dφ/dt⟩ ≠ 0 → V = (ħ/2e)⟨dφ/dt⟩」／「零電壓態：相位被困在井中做電漿振盪」、「ω_p(I) = ω_p0 (1 − (I/Ic)²)^{1/4} = x.xx ω_p0」。

## 實跑紀錄

- washboard_sim.py（Python 3，無套件，沒有雜訊，Q = 8）：往上加到 1.00 才變電壓態；往回調 0.16 還在滑（平均電壓 0.093）、0.15 停下；同樣 0.50 上升時 0.000、下降時 0.499；
  Q = 2、4、16 時往回調最後還在滑的電流 0.60、0.32、0.08（估計值 4/(πQ) = 0.64、0.32、0.08）。完整輸出見 `classroom.py` 寫入的 `04_解答.md`。
- Node 重跑場景更新式（含 0.03 雜訊、dt = 0.04 × 0.97）：每 3 秒加 0.01 時，讀數在 1.00（16%）或 1.01（84%）變電壓態；從 1.10 每 5 秒降 0.01 時，60 次都在 0.16 變回零電壓態；
  固定電流 0.16 停 8 秒，100 次中 42 次停下、0.14 全部停下。位障與電漿頻率讀數（0.30／0.90）：1.15／0.06 E_J、0.98／0.66 ω_p0。
