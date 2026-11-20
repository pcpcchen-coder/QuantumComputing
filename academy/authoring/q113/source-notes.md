# Q113 來源筆記（逐字引文）

查核日：2026-11-19（檔頭 CHECKED 依派工統一寫 2026-11-18）。維基百科頁面由製作代理以 `action=raw` 取得原始 wikitext，revision id 取自 MediaWiki API。學程內部簡報、簡報原始稿與動畫程式由製作代理讀取。程式由製作代理實際執行。

## Quantum circuit（Wikipedia，oldid=1383192653）

- 「Circuits are written such that the horizontal axis is time, starting at the left hand side and ending at the right. Horizontal lines are qubits, doubled lines represent classical bits.」
- 「These lines define the sequence of events, and are usually not physical cables.」

## Quantum logic gate（Wikipedia，oldid=1376542851）

- 「The Pauli-X gate is the quantum equivalent of the NOT gate for classical computers with respect to the standard basis |0⟩, |1⟩ … It is sometimes called a bit-flip as it maps |0⟩ to |1⟩ and |1⟩ to |0⟩.」
- 「Pauli Z leaves the basis state |0⟩ unchanged and maps |1⟩ to −|1⟩. Due to this nature, Pauli Z is sometimes called phase-flip.」
- 「The Pauli X, Y and Z equate, respectively, to a rotation around the x, y and z axes of the Bloch sphere by π radians.」
- 「[The Hadamard gate] maps the basis states |0⟩ ↦ (|0⟩ + |1⟩)/√2 and |1⟩ ↦ (|0⟩ − |1⟩)/√2 (it creates an equal superposition state if given a computational basis state).」
- 「The Hadamard gate performs a rotation of π about the axis (x̂+ẑ)/√2 at the Bloch sphere」
- 「the controlled NOT gate (or CNOT or CX) acts on 2 qubits, and performs the NOT operation on the second qubit only when the first qubit is |1⟩, and otherwise leaves it unchanged.」

## Born rule（Wikipedia，oldid=1368836124）

- 「it is common to describe the Born rule as saying that probability is equal to the amplitude-squared (really the amplitude times its own complex conjugate).」

## 學程內部簡報（slides/output/basic-circuits.pptx；原始稿 slides/reports/basic-circuits.js）

- 第 2 頁「八個範例，由淺到深」：範例 1 疊加（1 顆位元）、範例 2 干涉（1 顆）、範例 3–4 Bell、GHZ 態（2–4 顆）、範例 5 隱形傳態（3 顆）、範例 6–7 Deutsch、BV（2–4 顆）、範例 8 Grover（2–3 顆）。備註：「前兩個範例只有一顆位元……第三、第四個講糾纏。第五個用糾纏做隱形傳態。第六、第七個是只查一次的演算法，第八個是 Grover 搜尋，會把前面學到的疊加、干涉、相位全部用上。」
- 第 3 頁「讀圖之前：三個約定」：「位元順序 q0 寫在最右邊」「電路圖：q0 在最上面／位元字串：q0 在最右邊，和 Qiskit 相同／例：|01⟩ 代表 q1 = 0、q0 = 1」；「振幅 長條有正有負」「每個結果有一個振幅，可以是負的／機率 = 振幅²，所以負號量不到／簡報裡金色是正、紅色是負」；「互動動畫 每個範例都能自己玩」「逐步播放、量測 1,000 次」。
- 第 4 頁「今天用到的閘」（表格在原始稿 basic-circuits.js）：H Hadamard「|0⟩ → (|0⟩ + |1⟩)/√2，|1⟩ → (|0⟩ − |1⟩)/√2」「繞 x、z 中間的斜軸轉 180°」；X NOT「|0⟩ ↔ |1⟩」「繞 x 軸轉 180°」；Z 相位翻轉「|0⟩ 不變，|1⟩ → −|1⟩」「繞 z 軸轉 180°」；CNOT 控制 NOT「控制位元是 1 時，翻轉目標位元」；CZ／CCZ 控制 Z「全部位元都是 1 時，才加一個負號」；Ry(θ)「準備任意的實數振幅」。備註：「單位元閘都可以想成在 Bloch 球上轉 180 度，只是轉軸不同。」「後半段還會用到控制 Z……以及 Ry」。
- 課綱「家長課前準備」寫簡報 p3–4、素材寫 p2–4：實際內容與頁碼一致（第 2 頁地圖、第 3 頁約定、第 4 頁閘表）。

## 互動動畫程式（animations/basic-circuits.html）

- 頁首：「讀法和 Qiskit 相同：電路圖 q0 在最上面，但寫成位元字串時 q0 在最右邊，例如 |01⟩ 代表 q1 = 0、q0 = 1。」
- 振幅卡：圖例「正振幅」「負振幅」；「柱子往上是正振幅、往下是負振幅，長度 1 頂到虛線。量到某個結果的機率 = 振幅²。」CSS（淺色）：`--pos:#1D6A8B`（藍）、`--neg:#B65C12`（橘）；`--h:#1D6A8B`、`--x:#A23B5C`、`--z:#7348A3`。
- 量測卡：「灰色底是理論機率，綠色是實際次數。」按鈕「量測 1 次」「量測 1,000 次」「清除」；標題列「量測 q1 q0」。
- 電路圖：每條線左邊 `q0`、`|0⟩`；最右邊量測錶；CNOT 畫成實心點（控制）與圓圈加十字（目標）；橘色虛線 `.head` 標示目前步驟；尚未執行的閘加 `.future`（淡色）。
- 範例選項：疊加「起始態 |0⟩／|1⟩」；干涉「有 Z／沒有 Z」，步驟為 H、Z、H；Bell「Φ⁺、Φ⁻、Ψ⁺、Ψ⁻」，準備步驟分別為無、X(q0)、X(q1)、X(q0)X(q1)。

## 實跑紀錄

`read_order.py`（Python 3.13.18，只用標準函式庫，結果固定）：

```
一、約定二：位元字串裡 q0 寫在最右邊（兩顆位元，字串是 q1 q0）
  X(q0)            |01⟩ +1.000（100%）
  X(q1)            |10⟩ +1.000（100%）
二、約定三：振幅有正有負，機率 = 振幅²，負號量不到
  H                |0⟩ +0.707（50%）  |1⟩ +0.707（50%）
  H → Z            |0⟩ +0.707（50%）  |1⟩ −0.707（50%）
三、四種閘（CX：控制 q0 = 0 → |00⟩；控制 q0 = 1 → |11⟩）
四、改造區：X(q1) → H(q0) → |10⟩ +0.707（50%）  |11⟩ +0.707（50%）
```

`qiskit_check.py`（Qiskit 2.6.2，StatevectorSampler seed=2026）：

```
只翻 q0 機率 {'01': 1.0} 量測 1000 次 {'01': 1000}
只翻 q1 機率 {'10': 1.0} 量測 1000 次 {'10': 1000}
H → Z 振幅 [0.707, -0.707] 機率 {'0': 0.5, '1': 0.5}
```

Qiskit 原始碼 `qiskit/circuit/quantumcircuit.py`（reverse_bits 說明）：「This method is useful for converting a circuit written in little-endian convention to the big-endian equivalent, and vice versa.」

## 動畫畫面（製作代理以 Playwright 1600×900、zoom 0.8 實拍）

- #bell 選 Φ⁻、起點、下一步：|ψ⟩ = |01⟩，|01⟩ 柱子 +1.000；量測 1,000 次：01 1000（100.0%）。選 Ψ⁺ 同樣操作：|ψ⟩ = |10⟩。
- #interference 下一步兩次：|ψ⟩ = (|0⟩ − |1⟩) / √2；|0⟩ 藍色 +.707、|1⟩ 橘色 −.707，下方都是 50%。
- #superposition：起點時虛線在 H 左邊；下一步後在 H 右邊，兩根柱子 +.707。
