# Q053 來源筆記（逐字引文）

查核日：2026-11-18。維基百科頁面由製作代理以 `index.php?action=raw` 取得 wikitext（revision id 取自 `action=info` 頁的 wgCurRevisionId）。學程內部簡報、對話紀錄與動畫程式由製作代理讀取。

## Transmon（Wikipedia，oldid=1377984572）

- 「The disadvantage is the reduced anharmonicity α = (E₂₁ − E₁₀)/E₁₀, where E_ij is the energy difference between eigenstates |i⟩ and |j⟩.」
- 「Reduced anharmonicity complicates the device operation as a two level system, e.g. exciting the device from the ground state to the first excited state by a resonant pulse also populates the higher excited state. This complication is overcome by complex microwave pulse design, that takes into account the higher energy levels, and prohibits their excitation by destructive interference.」

## Superconducting quantum computing（Wikipedia，oldid=1382042448）

- 「A single qubit gate is achieved by rotation in the Bloch sphere. Rotations between different energy levels of a single qubit are induced by microwave pulses sent to an antenna or transmission line coupled to the qubit with a frequency resonant with the energy separation between levels.」
- 「The axis of rotation is set by quadrature amplitude modulation of microwave pulse, while pulse length determines the angle of rotation.」（引用 Motzoi, Gambetta, Rebentrost, Wilhelm, "Simple Pulses for Elimination of Leakage in Weakly Nonlinear Qubits", PRL 103, 110501 (2009)）

## Quantum logic gate（Wikipedia，oldid=1376542851）

- 「The phase shift is a family of single-qubit gates that map the basis states |0⟩ ↦ |0⟩ and |1⟩ ↦ e^{iφ}|1⟩. The probability of measuring a |0⟩ or |1⟩ is unchanged after applying this gate, however it modifies the phase of the quantum state. This is equivalent to tracing a horizontal circle (a line of constant latitude), or a rotation about the z-axis on the Bloch sphere by φ radians.」
- 「Some common examples are the T gate where φ = π/4 …, the phase gate (also known as the S gate …) where φ = π/2 and the Pauli-Z gate where φ = π.」

## 學程內部簡報：slides/QC_Operation_Talk.pptx 第 21 頁「DRAG 脈衝與虛擬 Z 閘」

- 「DRAG：避免洩漏到 |2⟩」「transmon 不是完美的二能階：|1⟩→|2⟩ 只比 f₀₁ 低 ~200–300 MHz｜短脈衝頻譜寬 → 打到 f₁₂ → 洩漏與相位誤差｜方波：sinc 旁瓣大；高斯：較窄｜DRAG：Q 通道加上 I 的導數 × 係數 → 在 f₁₂ 挖出頻譜零點｜Motzoi et al., PRL 103, 110501 (2009)」
- 「虛擬 Z 閘：零時間、零誤差」「Rz(θ) 不送脈衝，而是把之後所有脈衝的相位 −θ｜物理上：改變「參考座標」，量子態本身沒動｜原本繞 x 的脈衝，在新座標下就像先做了 Rz｜軟體記帳即可：完美、瞬間｜所以轉譯器喜歡把閘都改寫成 Rz + √X｜McKay et al., PRA 96, 022330 (2017)」
- 講者備註：「切換「方波 / 高斯 / 高斯 + DRAG」，看右下插圖的頻譜，紅色虛線是 f12 的位置，可以看到 DRAG 把那裡壓到很低。」「在場景 3 按「虛擬 Z（90°）」可以看到座標旋轉，之後再送相位 0 的脈衝，旋轉軸就相對地改變了。」

## 對話紀錄：docs/超導量子電腦師生對話教學紀錄.md

- 第 204 行：「換成 JJ，位能變 cos 井，0→1 是 5.21 GHz、1→2 低了 283 MHz，所以 5.21 GHz 只作用在 0↔1（非諧性）。脈衝通常 20–50 ns，並用 DRAG 整形抑制漏到 |2⟩。」
- 第 217 行：「做 Z 旋轉（實務上多用虛擬 Z：軟體改後續脈衝相位，0 ns、0 誤差）」
- 第 744 行：「H｜π/2 脈衝（＋虛擬 Z）」；第 1035 行：「Rz 是虛擬 Z、0 ns，可合併或消掉」
- 第 1049 行（校準依賴圖）：「… Rabi（π 振幅）→ Ramsey（精修 f₀₁、T₂*）→ T₁／T₂ → DRAG → 讀取最佳化 …」

## 互動動畫程式

- animations/js/operation/03_pulse.js：desc「脈衝形狀：方波的頻譜很寬，會打到 |1⟩→|2⟩ 躍遷（f₁₂ ≈ f₀₁ − 220 MHz）造成「洩漏」；高斯脈衝較窄；DRAG 在 Q 通道加上導數項，在 f₁₂ 挖出零點」「虛擬 Z 閘：不送任何脈衝，只把之後所有脈衝的相位平移 —— 零時間、零誤差」（第 9–10 行）；ALPHA = −0.22 GHz、beta = 1/(2π·ALPHA)（第 40、47 行）；ui.radio「方波」「高斯」「高斯 + DRAG」（第 70 行）；「虛擬 Z（90°）」把 frame 加 90°、狀態向量繞 z 轉 90°（第 77 行）；頻譜插圖 db = max(−60, …)、標「f₁₂ 處 … dB」（第 90–94 行）；讀數「虛擬 Z 累積的座標相位」（第 127 行）。
- animations/lc-vs-jj.html 第 6 步（id "s6drag"，第 283–325 行；程式第 553–646 行）：「非諧性 |α| 只有 200～300 MHz。閘做得愈快，退相干的時間就愈少，但脈衝愈短，頻譜就愈寬」「這叫洩漏（leakage），而且 |2⟩ 已經不在 qubit 的計算空間裡」「β = 1 時，這個因子剛好在 Δ = α（也就是 1→2 躍遷）變成零。脈衝還是一樣快，只是在 ω₁₂ 那個頻率上沒有能量，所以推不動 |2⟩」「實務上 β 要用實驗校準，因為還有更高的能階、線路濾波造成的波形失真等等。常見做法是掃描 β … 找出誤差最小的點」。滑桿 #dT（π 脈衝長度，預設 6）、#dA（非諧性 α，預設 −250 MHz）、#dB（DRAG 係數 β，預設 1）；讀數 #rDa、#rDb、#rDc。
- animations/transmon-3d.html 第 912、919 行：「脈衝越短越強、頻譜越寬，就越容易碰到 4.93 GHz，所以脈衝不能無限縮短，還要用 DRAG 整形壓低洩漏」「|1⟩→|2⟩ 的頻率低了 283 MHz … 實務上脈衝長 20–50 ns，並用 DRAG 整形進一步抑制洩漏」。

## 數值重算

- `/home/user/qwork/q053calc/pulse.py`：以 Python 逐行重現 03_pulse.js 的 build() 與 spec()，算 f₁₂ 處 dB。
- `/home/user/qwork/q053calc/drag.js`：照抄 lc-vs-jj.html 的 makePulse()／simDrag()，用 Node 執行。
- `/home/user/qwork/q053calc/checks.py`：2×2 矩陣檢查 H = Rz(π/2)·√X·Rz(π/2)（差一個整體相位）與動畫的虛擬 Z 序列。
