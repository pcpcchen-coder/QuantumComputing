# Q054 來源筆記（逐字引文）

查核日：2026-11-18。維基百科頁面由製作代理以 `index.php?action=raw` 取得 wikitext（revision id 取自 API `prop=revisions`）。學程內部簡報與動畫程式由製作代理讀取。

## List of quantum logic gates（Wikipedia，oldid=1386001178）

- 「Any 2 × 2 unitary matrix in SU(2) can be written as a product (i.e. series circuit) of three rotation gates or less.」
- 「Rotation operators have interesting identities. For example, R_y(π/2)Z = H and X R_y(π/2) = H. Also, using the anticommuting relations we have Z R_y(−π/2) = H and R_y(−π/2)X = H.」
- 「Global phase and phase shift can be transformed into each other's with the Z-rotation operator: R_z(γ) Ph(γ/2) = P(γ).」
- 「The √X gate represents a rotation of π/2 about the x axis at the Bloch sphere √X = e^{iπ/4}R_x(π/2).」
- 「The global phase gate introduces a global phase e^{iφ} to the whole qubit quantum state. A quantum state is uniquely defined up to a phase. Because of the Born rule, a phase factor has no effect on a measurement outcome: |e^{iφ}| = 1 for any φ.」
- R_z(θ) = [[exp(−iθ/2), 0], [0, exp(iθ/2)]]；R_y(θ) = [[cos(θ/2), −sin(θ/2)], [sin(θ/2), cos(θ/2)]]。

## Quantum logic gate（Wikipedia，oldid=1376542851）

- 圖說：「Single qubit states that are not entangled and lack global phase can be represented as points on the surface of the Bloch sphere, written as |ψ⟩ = cos(θ/2)|0⟩ + e^{iφ} sin(θ/2)|1⟩. Rotations about the x, y, z axes of the Bloch sphere are represented by the rotation operator gates.」
- 「The Pauli X, Y and Z equate, respectively, to a rotation around the x, y and z axes of the Bloch sphere by π radians.」
- 「Controlled gates act on 2 or more qubits, where one or more qubits act as a control for some operation. For example, the controlled NOT gate (or CNOT or CX) acts on 2 qubits, and performs the NOT operation on the second qubit only when the first qubit is |1⟩, and otherwise leaves it unchanged.」
- 註：「However as the global phase is irrelevant in the measurement output, universal quantum subsets can be constructed e.g. the set containing R_y(θ), R_z(θ) and CNOT only spans all unitaries with determinant ±1 but it is sufficient for quantum computation.」

## Bloch sphere（Wikipedia，oldid=1381941389）

- 「An advantage of the Bloch sphere representation is that the unitary evolution of a qubit state is described by rotations of the Bloch sphere.」

## Euler angles（Wikipedia，oldid=1386434339）

- 「Starting with XYZ overlapping xyz, a composition of three intrinsic rotations can be used to reach any target orientation for XYZ.」
- 「There are six possibilities of choosing the rotation axes for proper Euler angles. In all of them, the first and third rotation axes are the same.」（列表含 z-y-z）
- 「Any orientation can be achieved by composing three elemental rotations, starting from a known standard orientation.」

## 學程內部簡報：slides/QC_Operation_Talk.pptx

- 第 18 頁「單位元量子閘一覽」表格：「H｜(1/√2)[[1, 1], [1, −1]]｜繞 (x+z)/√2 軸 180°」「S｜[[1, 0], [0, i]]｜繞 z 軸 90°」「T｜[[1, 0], [0, eiπ/4]]｜繞 z 軸 45°」「√X｜½[[1+i, 1−i], [1−i, 1+i]]｜繞 x 軸 90°｜IBM 原生閘（SX）」「Rx/Ry/Rz(θ)｜e−iθσ/2｜繞 x/y/z 軸 θ」。
- 第 19 頁「任意單位元操作 = 三個旋轉」：「U = eiγ Rz(φ) Ry(θ) Rz(λ)」「任何單位元閘都能分解成 z–y–z 三次旋轉（再加一個無意義的全域相位）｜硬體只需要兩種動作：繞 xy 平面某軸的微波脈衝 + 繞 z 軸的旋轉｜IBM 的作法：任意 U = Rz · √X · Rz · √X · Rz —— 只校準 √X 一種脈衝｜Rz 用「虛擬 Z」實現：零時間、零誤差（下一頁）」。
- 第 19 頁講者備註：「一個很實用的定理：任何單位元操作都可以分解成 z、y、z 三次旋轉，再乘上一個沒有物理意義的全域相位。這對硬體的意義是：我們不需要為每種閘各校準一個脈衝，只要能做『繞 xy 平面上某條軸的旋轉』和『繞 z 軸的旋轉』就夠了。」

## 互動動畫程式

- animations/js/operation/02_gates.js：subtitle「每個單位元閘 = 繞某一軸旋轉某一角度（2×2 么正矩陣）」；desc「任何單位元操作都能寫成 Rz·Ry·Rz 的組合 —— 實際硬體只需要『繞 x/y 軸的微波脈衝』加上『虛擬 Z』」（第 10 行）；按鈕 X、Y、Z、H、S、S†、T、T†、√X（第 22–23 行）；滑桿「旋轉角 θ（給 Rx / Ry / Rz）」−180～180、步進 5（第 24 行）；Rx(θ)、Ry(θ)、Rz(θ)（第 27–29 行）；重設 |0⟩、重設 |1⟩、清除軌跡（第 32–34 行）；插圖「最後一個閘的矩陣與線路紀錄」與「|0⟩ 起始 → 由左至右依序作用；矩陣相乘順序相反」「目前：…」（第 42–59 行）；閘動畫時間 0.5 + |角度|/π × 0.8 秒（第 69 行）。
- animations/js/operation/common.js：G.RX／RY／RZ 矩陣（第 22–24 行，與維基百科相同）；ROT 表：H 軸 (1/√2, 0, 1/√2)、S 繞 z 90°、T 繞 z 45°、SX 繞 x 90°（第 28–33 行）；B2T 把布洛赫 (x, y, z) 對應到畫面（第 111 行）；粉紅色旋轉軸 0xff6bd5（第 136 行）。
- animations/js/operation/01_qubit.js：「量子位元的狀態是 Bloch 球上的一個點，由兩個角度決定：θ 決定 |0⟩、|1⟩ 的比例，φ 是兩者的相對相位」（第 6 行）。

## 數值重算

`/home/user/qwork/q054calc/checks.py`（numpy）；輸出摘錄見 `fact-check.md` 文末。截圖：`/home/user/qwork/q054shots/`（h-*、t-*、d-*）。
