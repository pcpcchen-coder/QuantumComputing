# Q052 來源筆記（逐字引文）

查核日：2026-11-18。維基百科頁面由製作代理直接開啟（revision id 取自頁面的 wgRevisionId）。學程內部簡報、對話紀錄與動畫程式由製作代理讀取。

## Rabi cycle（Wikipedia，oldid=1383859287）

- 「In physics, the Rabi cycle (or Rabi flop) is the cyclic behaviour of a two-level quantum system in the presence of an oscillatory driving field.」
- 「The Rabi effect is important in quantum optics, magnetic resonance and quantum computing.」

## Rabi frequency（Wikipedia，oldid=1380075348）

- 「It is proportional to the transition dipole moment of the two levels and to the amplitude (not intensity) of the electromagnetic field.」
- 「The quantity √(Ω² + δ²) is commonly referred to as the "generalized Rabi frequency." For cases in which δ ≠ 0, Rabi flopping actually occurs at this frequency, where δ is the detuning」
- 「Also note that as the incident light frequency shifts further from the transition frequency, the amplitude of the Rabi oscillation decreases」

## Bloch sphere（Wikipedia，oldid=1381941389）

- 「The north and south poles of the Bloch sphere are typically chosen to correspond to the standard basis vectors |0⟩ and |1⟩, respectively」
- 「only the relative phase between the coefficients of the two basis vectors has any physical meaning」「The coefficient of |0⟩ can therefore be taken to be real and non-negative.」

## In-phase and quadrature components（Wikipedia，oldid=1386419474）

- 「it is possible to create an arbitrarily phase-shifted sine wave, by mixing together in different proportions two sine waves that are 90° out of phase.」

## Scientific control（Wikipedia，oldid=1384711202）

- 「A scientific control is an element of an experiment or observation designed to minimize the influence of variables other than the independent variable under investigation, thereby reducing the risk of confounding.」

## 學程內部簡報：slides/QC_Operation_Talk.pptx

- 第 20 頁「閘的物理實現：微波脈衝」表格：「頻率 = f₀₁｜共振才能有效驅動」「包絡面積（振幅×時間）｜旋轉角：π → X、π/2 → √X」「相位 φ（I/Q 比例）｜旋轉軸：0° → x、90° → y」「形狀（高斯、DRAG）｜頻寬 → 洩漏到 |2⟩」「長度｜~20–50 ns：越短越不受退相干影響，但越寬頻」；「V(t) = I(t)cos(ωt) − Q(t)sin(ωt)／旋轉座標中：H = (Ω(t)/2)(cos φ·σx + sin φ·σy) + (Δ/2)σz」「失諧 Δ ≠ 0 → 旋轉軸往 z 傾斜，轉不到目標／AWG 產生 I、Q 包絡，IQ 混頻器搬到 5 GHz（或直接數位合成）」。講者備註：「一段大約 20 到 50 奈秒、頻率對準 f01 的微波脈衝」「脈衝的相位，也就是 I 和 Q 兩個分量的比例，決定旋轉軸」。
- 第 21 頁：「transmon 不是完美的二能階：|1⟩→|2⟩ 只比 f₀₁ 低 ~200–300 MHz／短脈衝頻譜寬 → 打到 f₁₂ → 洩漏與相位誤差／方波：sinc 旁瓣大；高斯：較窄／DRAG：Q 通道加上 I 的導數 × 係數 → 在 f₁₂ 挖出頻譜零點」；「虛擬 Z 閘：零時間、零誤差」。

## 對話紀錄：docs/超導量子電腦師生對話教學紀錄.md 第 5 課

- 「微波一停，疊加態就留下來：π/2 脈衝就是在半路停下（寫入疊加態的方法）。」
- 「疊加態還有相位：X 軸與 Y 軸 π/2 都是 50/50，但在赤道上指向不同方向；干涉靠的就是相位。」
- 「脈衝越短越強，頻譜越寬，越容易碰到 4.93 GHz，所以要用 DRAG」。

## 互動動畫程式

- animations/js/operation/03_pulse.js：subtitle「振幅×時間 = 旋轉角；相位 = 旋轉軸；頻率要對準 f₀₁」；desc「面積 π → X 閘；π/2 → √X」「0° → 繞 x，90° → 繞 y」「失諧（頻率沒對準）會讓旋轉軸往 z 傾斜，轉不到南極」「f₁₂ ≈ f₀₁ − 220 MHz」；預設 shape='gauss'、area=180、Tg=40（第 39 行）；ALPHA = −0.22 GHz（第 40 行）；ui.slider「脈衝面積 → 旋轉角」「脈衝相位 φ → 旋轉軸方向」「頻率失諧 Δ（MHz）」「閘長度（ns）」（第 71–74 行）；ui.button「▶ 送出脈衝」「虛擬 Z（90°）」「重設 |0⟩」（第 76–78 行）；頻譜插圖標「f₁₂ 處 … dB」（第 94 行）；粉紅旋轉軸 Bl.showAxis([cos φ, sin φ, Δ/平均Ω])（第 119 行）；讀數「峰值 Rabi 頻率 ≈ … MHz」（第 129 行）。
- animations/js/operation/common.js：布洛赫球 x 軸橘 0xff9f43、y 軸綠 0x2ecc71、z 軸藍 0x8ab4ff（第 125 行），旋轉軸粉紅 0xff6bd5（第 136 行）。
- animations/transmon-3d.html 第 4 章（id "control"）：按鈕 #c4xpi「X 軸 π」、#c4xh「X 軸 π/2」、#c4yh「Y 軸 π/2」、#c4rabi、#c4r「重設 |0⟩」（第 929 行）；面板 #r4psi「此刻的狀態」、#r4kind「類型」（第 926 行）；說明「X 軸 π/2」和「Y 軸 π/2」都得到 50/50，但箭頭指向赤道上不同方向（狀態式子裡的係數一個是 −i、一個是實數）。

## 數值重算

`/home/user/qwork/q052calc/pulse_sim.py`（以 Python 逐行重現 03_pulse.js 的 wave()、update() 積分與 spec()）。輸出見 fact-check.md。
