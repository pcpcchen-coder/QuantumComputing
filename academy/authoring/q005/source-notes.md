# Q005 來源筆記（逐字引文）

查核日：2026-11-18。維基百科兩頁由製作代理開啟擷取（擷取時公式排版部分遺失，等式由製作代理以矩陣自行重算）。學程內部簡報與 3D 場景程式由製作代理讀取。

## Quantum logic gate（Wikipedia）

- 「Pauli Z leaves the basis state |0⟩ unchanged and maps |1⟩ to −|1⟩.」
- 「The Pauli X, Y and Z equate, respectively, to a rotation around the x, y and z axes of the Bloch sphere by π radians.」
- 「The Hadamard gate performs a rotation of π about the axis (x̂+ẑ)/√2 at the Bloch sphere, and is therefore involutory.」
- 「the phase gate (also known as the S gate …) where φ=π/2」
- 製作代理重算：S = diag(1, i)，S² = Z；HH = I；HZH = X；H·S·H|0⟩ 的 P(0) = 1/2。

## Bloch sphere（Wikipedia）

- 「only the relative phase between the coefficients of the two basis vectors has any physical meaning.」
- 「the phase of the quantum system is not directly measurable」
- 「the probability of finding the state |0⟩ in a measurement in the standard basis depends linearly on the height」

## 學程內部簡報：slides/QC_Operation_Talk.pptx

- 第 7 頁：「赤道 +x：|+⟩ = (|0⟩ + |1⟩)/√2」「赤道 −x：|−⟩ = (|0⟩ − |1⟩)/√2」「φ：相對相位 → Z 量測看不見，但會影響干涉」；講者備註「注意當你改 φ 時，右邊的理論機率完全不變——這就是『相位在 Z 測量中看不見』」。
- 第 18 頁：「Z｜[[1, 0], [0, −1]]｜繞 z 軸 180°｜|1⟩ 變號（相位翻轉）」；H「繞 (x+z)/√2 軸 180°」「|0⟩ → |+⟩」。
- 第 31 頁：「量測基底：硬體只會量 Z」「X｜H｜H 把 |+⟩/|−⟩ 轉成 |0⟩/|1⟩」。

## 3D 場景

- `animations/js/operation/02_gates.js`：按鈕 X、Y、Z、H、S、S†、T、T†、√X、重設 |0⟩、示範：H → Z → H = X；讀數顯示 P(0)、P(1)。
- `animations/js/operation/01_qubit.js`：φ（相位）滑桿只改 ph，不改理論機率；「一次跑 1000 shots」。
