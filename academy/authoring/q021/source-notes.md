# Q021 來源筆記（逐字引文）

查核日：2026-11-18。課綱、簡報、動畫程式由製作代理讀取。程式由製作代理實際執行。

## 課綱（academy/lessons/Q021/lesson.json）

- 課程主題「彈簧、單擺與 LC 電路」；階段「第二階段 硬體怎麼做」；模組「QM02 超導量子位元：從超導到 transmon」。
- 學習目標「把力學振盪和電磁振盪對應起來：質量↔電感、彈簧↔電容」。
- 動手任務「量彈簧和單擺的週期，填出力學與 LC 的對照表」；孩子獨立改造「改變質量或擺長，預測週期變化並驗證」；好玩機制「科學實驗（彈簧振盪計時）」。
- 作品「類比對照表」；家長課前準備「彈簧、重物、細繩、碼錶」；生活技能支線「用類比把新知識接到舊知識」。
- 常見誤解與安全提醒「類比只在小振幅時成立；大振幅單擺就不再是簡諧運動」。
- 沿用簡報頁：ep049-superconducting-qubit.pptx p6–8、transmon.pptx p8；沿用 3D 場景：lj:s1、lj:s2；需新增素材「★ 彈簧 ↔ LC 類比場景」（本集未新增，動畫段改用 lc-vs-jj.html 的直線與正弦說明小振幅）。
- Q020 brief：「知道超導環裡的磁通只能是 Φ₀ 的整數倍，以及 2e 從哪裡來」。Q022 brief：「量子諧振子：等距的梯子」「知道 LC 電路的能階等距，所以無法只挑出兩個能階當量子位元」。

## 簡報（python-pptx 擷取）

- ep049 p6「繞個遠路：從彈簧到哈密頓量」：「K + U = const.」「力學能守恆：動能＋位能為定值，一高一低互相交換」「H(x, p) = p²/2m + ½ kx²」；備註「彈簧拉著一個質量振盪，就是諧振子。它的力學能守恆：動能加位能是定值，一個高的時候另一個就低。」
- ep049 p7「量子諧振子：出現等距的能階」：「En = (n + ½) ħω」「相鄰能階的間距固定：像樓梯一樣「等距」」（下一堂預告）。
- ep049 p8「力學振盪 ↔ 電磁振盪：LC 電路」表：能量交換「動能 ⇄ 位能｜電容能 ⇄ 電感能」；振盪的東西「質量來回運動｜電荷來回流動」；哈密頓量「H = p²/2m + ½kx²｜H = Q²/2C + Φ²/2L」；一對共軛變數「位置 x、動量 p｜磁通量 Φ、電荷 Q」；
  「結論：超導 LC 電路就能成為一個會出現量子現象的諧振子」；備註「電感和電容之間能量換來換去，電荷跑過來跑過去，跟彈簧非常像。」
  （注意：這一列把 Φ 放在 x 的位置，是對偶的配法；本集依課綱採 Q ↔ x、L ↔ m。）
- transmon p8「直覺圖像：量子單擺」：「U = −mgl cos θ」「mgl（重力回復力）」「EJ/EC 很大，就像又重、擺幅又小的擺：幾乎是簡諧振盪，但頻率會隨振幅略降。」
- JJ_Microwave_Readout_Talk p8：「量子位元 f01」「≈ 5 GHz（≈ 20 μeV）」。

## 維基百科（原始 wikitext，2026-11-18 取得）

- Simple harmonic motion：「T = 2π√(m/k)」「These equations demonstrate that the simple harmonic motion is isochronous (the period and frequency are independent of the amplitude and the initial phase of the motion).」；單擺「the period of oscillation is independent of the amplitude and mass of the pendulum but not of the acceleration due to gravity, g」。
- Pendulum (mechanics)：「For θ ≈ 0, the approximation sin θ ≈ θ can be made.」「The motion is simple harmonic motion」「T₀ = 2π√(ℓ/g)」「under the small-angle approximation, the period is independent of the amplitude θ₀; this is the property of isochronism that Galileo discovered.」；
  經驗式「ℓ ≈ T₀²/4, T₀ ≈ 2√ℓ」；Arbitrary-amplitude period 與「Arithmetic-geometric mean solution for elliptic integral」（T = T₀ / M(1, cos(θ₀/2))）。
- LC circuit：「A capacitor stores energy in the electric field (E) between its plates……and an inductor stores energy in its magnetic field (B)」「because inductors oppose changes in current. This induced voltage causes a current to begin to recharge the capacitor with a voltage of opposite polarity」
  「The charge flows back and forth between the plates of the capacitor, through the inductor.」「is similar to a pendulum swinging back and forth」「internal resistance makes the oscillations die out」；「ω₀ = 1/√(LC)」。
- Mechanical–electrical analogies：「There is no one, unique way of doing this……two analogies that are widely used: the impedance analogy and the mobility analogy.」；阻抗類比表 Force↔Voltage、Velocity↔Current、Displacement↔Charge、Momentum↔Flux linkage、Mass↔Inductance、Compliance↔Capacitance。
- Harmonic oscillator 類比表：Mass m ↔ Inductance L（另一欄 Capacitance C）；Spring constant k ↔ Elastance 1/C（另一欄 Magnetic reluctance 1/L）；共振頻率 (1/2π)√(k/m) ↔ (1/2π)√(1/LC)。

## 互動圖解程式（animations/lc-vs-jj.html）

- 第 154–181 行 #s1：「第 1 步 · 本構關係」「電流與磁通：直線 vs 正弦」；圖例「電感 I = φ」「JJ I = sin φ」「JJ 在此點的切線」；滑桿「相位 φ」#phi（−4.71～4.71、預設 0.6）；讀數「電感電流 I/I_c」「JJ 電流 I/I_c」「JJ 等效電感 L_J / L_J0」。
- 第 391–396 行說明：「φ 很小：sin φ ≈ φ，JJ 跟普通電感幾乎一模一樣，這時它看起來是線性的。」「直線和正弦分開了：同樣的磁通，JJ 給的電流比電感少，等效電感變大了 … 倍。」
- 第 184–211 行 #s2：「第 2 步 · 疊加原理測試」「用正弦波去推，輸出長什麼樣？」「線性系統不會產生新的頻率」「把 A 調小，JJ 幾乎變回純正弦」；滑桿「驅動振幅 A（rad）」#amp（0.1～3、預設 1.4）；讀數「輸入加倍，輸出峰值變成（電感）」「（JJ）」「JJ 的 3ω 諧波 / 基頻」。
- 第 403–438 行 draw2：上圖兩個週期、±I_c 虛線；頻譜 1ω、3ω、5ω、7ω，藍色只有 1ω；r2a 固定「2.00 倍」。

## 實跑紀錄（oscillation_table.py，Python 3，無套件）

見 `classroom.py` 執行時寫入的 `04_解答.md`；重點：k = 20 N/m 時 100 g → 0.444 s、400 g → 0.889 s（2.0 倍）；單擺 1 m → 2.006 s、0.25 m → 1.003 s；
大角度比例 10° 1.0019、30° 1.0174、60° 1.0732、90° 1.1803；LC 1 nH、1 pF → 5.033 GHz，1 mH、1 μF → 5.033 kHz。
lc-vs-jj.html 讀數以頁面同一段程式在 Node 實算：φ = 0.2 → 0.200／0.199；φ = 1.0 → 1.000／0.841（1.85×）；A = 0.3 → 3ω 0.4 %；A = 2.5 → 3ω 43.6 %、輸入加倍 1.00 倍。
