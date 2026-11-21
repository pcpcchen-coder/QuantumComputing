# Q116 來源筆記（逐字引文）

查核日：2026-11-19（檔頭 CHECKED 依派工統一寫 2026-11-18）。維基百科頁面由製作代理以 `action=raw` 取得原始 wikitext（2026-11-19）；Bell state 頁的 revision 為 1365950086（同一段落與工作區先前以 API 取得的版本一致）。學程內部簡報、簡報原始稿與動畫程式由製作代理讀取。程式由製作代理實際執行。

## Bell state（Wikipedia）

- 「the '''Bell's states''' or '''EPR pairs''' are specific quantum states of two qubits that represent the simplest examples of quantum entanglement.」
- 「The Bell states are four specific maximally entangled quantum states of two qubits.」
- 四個式子：|Φ⁺⟩ = (|0⟩_A⊗|0⟩_B + |1⟩_A⊗|1⟩_B)/√2、|Φ⁻⟩ = (|0⟩_A⊗|0⟩_B − |1⟩_A⊗|1⟩_B)/√2、|Ψ⁺⟩ = (|0⟩_A⊗|1⟩_B + |1⟩_A⊗|0⟩_B)/√2、|Ψ⁻⟩ = (|0⟩_A⊗|1⟩_B − |1⟩_A⊗|0⟩_B)/√2。
- 「the simplest takes a computational basis as the input, and contains a Hadamard gate and a CNOT gate」「For the four basic two-qubit inputs, |00⟩, |01⟩, |10⟩, |11⟩, the circuit outputs the four Bell states」
- 「The result of a measurement of a single qubit in a Bell state is indeterminate, but upon measuring the first qubit in the ''z''-basis, the result of measuring the second qubit is guaranteed to yield the same value (for the Φ Bell states) or the opposite value (for the Ψ Bell states).」
- 「Because Bell states are entangled states, information on the entire system may be known, while withholding information on the individual subsystems. For example, the Bell state is a pure state, but the reduced density operator of the first qubit is a mixed state. The mixed state implies that not all the information on this first qubit is known.」
- 「Bell states are maximally entangled in the sense that its reduced density operators are maximally mixed」

## Quantum entanglement（Wikipedia）

- 例子：(|0⟩_A⊗|1⟩_B − |1⟩_A⊗|0⟩_B)/√2 的 A 約化密度矩陣是 ρ_A = ½(|0⟩⟨0| + |1⟩⟨1|)。
- 「This demonstrates that the reduced density matrix for an entangled pure ensemble is a mixed ensemble. In contrast, the density matrix of A for the pure product state |ψ⟩_A ⊗ |φ⟩_B discussed above is ρ_A = |ψ⟩_A⟨ψ|_A」

## Bloch sphere（Wikipedia）

- 「The north and south poles of the Bloch sphere are typically chosen to correspond to the standard basis vectors |0⟩ and |1⟩, respectively」
- 「As a consequence, the surface of the Bloch sphere represents all the pure states of a two-dimensional quantum system, whereas the interior corresponds to all the mixed states.」
- 「the eigenvalues of ρ are ½(1 ± |a|)」（a = 0 即 ρ = I/2，位於球心）

## Controlled NOT gate（Wikipedia）

- 「The CNOT gate flips the second qubit (the target qubit) if and only if the first qubit (the control qubit) is |1⟩.」

## 學程內部簡報（slides/output/basic-circuits.pptx；原始稿 slides/reports/basic-circuits.js）

用 python-pptx 讀出：第 10 頁「範例 3｜Bell 態：兩顆位元糾纏」、第 11 頁「振幅逐步看：CNOT 把機率搬到 |11⟩」、第 12 頁「四個 Bell 態：只差開頭的 X」（課綱寫 p10–12，無誤）。

- 第 10 頁：「① 起點 |00⟩ 兩顆位元都在 0」「② H 閘（q0）(|00⟩ + |01⟩)/√2 q0 進入疊加；q1 還沒參與，兩顆位元互不相干」「③ CNOT（q0 → q1）(|00⟩ + |11⟩)/√2 q0 是 1 的那一半，q1 也翻成 1。兩顆的結果永遠相同」；callout「各自隨機、彼此一致，而且無法拆成兩顆位元各自的狀態：這就是糾纏」。
- 第 11 頁：「位元字串是 |q1 q0⟩：右邊那位是 q0」；四格「① 起點 只有 |00⟩」「② H（q0） q0 疊加：|00⟩、|01⟩ 各半」「③ CNOT → Φ⁺ |01⟩ 的振幅搬到 |11⟩：只剩 00、11」「對照：Φ⁻ 先加 X(q0)：|11⟩ 帶負號，量起來和 Φ⁺ 一樣」；callout「CNOT 不改變長條的高度，只是把 q0 = 1 那一半的振幅搬到 q1 也是 1 的位置」。
- 第 12 頁表格：「Φ⁺｜無｜(|00⟩ + |11⟩)/√2｜00 或 11（永遠相同）」「Φ⁻｜X(q0)｜(|00⟩ − |11⟩)/√2｜00 或 11（永遠相同）」「Ψ⁺｜X(q1)｜(|01⟩ + |10⟩)/√2｜01 或 10（永遠相反）」「Ψ⁻｜X(q0)、X(q1)｜(|10⟩ − |01⟩)/√2｜01 或 10（永遠相反）」；callout「直接量測只分得出相同或相反；正負號要再做 CNOT、H 干涉才看得到（Bell 量測）」。
- 第 12 頁備註（basic-circuits.js）：「Bell 態一共有四個，電路都一樣是 H 加 CNOT，只差開頭有沒有先加 X。q0 先翻成 1，H 會帶進一個負號，得到 Φ⁻；q1 先翻成 1，CNOT 之後兩顆就會相反，得到 Ψ⁺；兩個都翻就是 Ψ⁻。」

## 互動動畫程式（animations/basic-circuits.html #bell）

- `id: "bell", short: "Bell 態", title: "Bell 態：兩顆位元糾纏"`；選項 `{ key: "bell", label: "目標 Bell 態", def: "phi+", choices: [["phi+", "Φ⁺"], ["phi-", "Φ⁻"], ["psi+", "Ψ⁺"], ["psi-", "Ψ⁻"]] }`；準備 `{ "phi+": [], "phi-": [X(0)], "psi+": [X(1)], "psi-": [X(0), X(1)] }`。
- CNOT 步驟說明：「CNOT 以 q0 為控制：q0 = 1 的那一半，q1 也跟著翻。結果兩顆位元的量測永遠相同（00 或 11）／永遠相反（01 或 10），單看任一顆卻都是 50/50：右邊兩顆的 Bloch 向量都縮到球心。這個狀態無法拆成兩顆位元各自的狀態，這就是糾纏。」負號版本另加「注意 Φ⁻ 和 Φ⁺（Ψ⁻ 和 Ψ⁺）量起來一模一樣，差在負號，要靠干涉才分得出來。」
- 頁面說明：「多顆位元時，Bloch 球畫的是『單看這一顆』的狀態：向量變短代表它和別的位元糾纏，縮到球心就是單看它完全隨機。」`reducedBloch(state, n, q)` 註解「長度 < 1 表示它和別的位元糾纏」；Bloch 球標籤「單看 q0」「單看 q1」。
- `rebuild(reset)`：「換範例時回到起點；只改選項時停在最後一步」；選項按鈕 `if (o[op.key] === v) return;`（按目前的選項不動作）；`#dots` 每一點跳到對應步驟；柱子在兩步間 650 ms 線性內插，多顆位元時 Bloch 球依內插中的振幅即時重算。
- 用頁面自己的 `simulate`／`ketString`／`reducedBloch`（node 執行）算出：Ψ⁻ 起點 |00⟩ → |11⟩（兩顆向量 z = −1）→ (|10⟩ − |11⟩) / √2（q0 向量 (−1, 0, 0)、q1 (0, 0, −1)）→ (−|01⟩ + |10⟩) / √2（兩顆 (0, 0, 0)）；四種最後一步兩顆向量都是 (0, 0, 0)。

## 互動動畫程式（animations/operation.html#register，js/operation/04_register.js）

- 說明：「上排是每個量子位元『自己』的 Bloch 球」「按『Bell 態』：H + CNOT 得到 (|00⟩+|11⟩)/√2。注意上排的箭頭縮成一點：單獨看任何一個量子位元都是完全隨機的，但兩者的結果永遠相同 —— 這就是糾纏」。
- 按鈕：「目標 q0」…「目標 q3」「H」「X」「Z」「S」「T」「CNOT（控制 = 目標+1 → 目標）」「CZ」「均勻疊加 H⊗ⁿ」「Bell 態」「GHZ 態」「測量全部」「只測 q0」「重設 |0…0⟩」（Playwright 讀出的 #controls 按鈕順序）。
- 讀數：「各量子位元 Bloch 長度：q0 …，q1 …」；任一顆 < 0.98 時「有糾纏：單一量子位元的向量變短（約化態是混態）」（顏色 #ff9be6），否則「無糾纏（可分離態）：每個量子位元各自是純態」。Bloch 球位置 x = ((n − 1)/2 − q)·2.3：q0 在右、q1 在左。

## 實跑紀錄

`bell_lab.py`（Python 3.13.18，只用標準函式庫，random.Random(1116)）：

```
一、逐步看振幅（Φ⁺）  每列最後是「單看那一顆」的 Bloch 向量大小
  起點              |00⟩ +1.000  |01⟩ 0  |10⟩ 0  |11⟩ 0   單看 q0 1.000  單看 q1 1.000
  H(q0)           |00⟩ +0.707  |01⟩ +0.707  |10⟩ 0  |11⟩ 0   單看 q0 1.000  單看 q1 1.000
  H(q0) → CNOT    |00⟩ +0.707  |01⟩ 0  |10⟩ 0  |11⟩ +0.707   單看 q0 0.000  單看 q1 0.000
二、四個 Bell 態：同一條線路，只差開頭加的 X
  Φ⁺  開頭：不加           狀態 (|00⟩ + |11⟩)/√2    單看 q0 0.000  單看 q1 0.000
  Φ⁻  開頭：X(q0)        狀態 (|00⟩ − |11⟩)/√2    單看 q0 0.000  單看 q1 0.000
  Ψ⁺  開頭：X(q1)        狀態 (|01⟩ + |10⟩)/√2    單看 q0 0.000  單看 q1 0.000
  Ψ⁻  開頭：X(q0)、X(q1)  狀態 (−|01⟩ + |10⟩)/√2   單看 q0 0.000  單看 q1 0.000
三、各量測 1000 次（兩顆一起量；random 種子 1116）
  Φ⁺  00 → 465 次  01 → 0 次  10 → 0 次  11 → 535 次
  Φ⁻  00 → 516 次  01 → 0 次  10 → 0 次  11 → 484 次
  Ψ⁺  00 → 0 次  01 → 497 次  10 → 503 次  11 → 0 次
  Ψ⁻  00 → 0 次  01 → 475 次  10 → 525 次  11 → 0 次
四、對照組：只做 H(q0)，不做 CNOT；以及量完一顆之後
  單看 q0：量到 0 的機率 50%，Bloch 向量大小 1.000（一半一半，卻沒有變短）
  Φ⁺ 只量 q0 一次之後：單看 q0 1.000  單看 q1 1.000（量測把糾纏拆開，兩顆都回到 1）
五、開頭的 X 等於後面補一個 Z
  X(q0) → H(q0)：(|00⟩ − |01⟩)/√2   H(q0) → Z(q0)：(|00⟩ − |01⟩)/√2   一樣嗎？ True
  Φ⁻ = 先 X(q0)：(|00⟩ − |11⟩)/√2   Φ⁺ 之後補 Z(q0)：(|00⟩ − |11⟩)/√2   一樣嗎？ True
六、改造區
  X(q1) → H(q0) → CNOT(q0→q1) → Z(q0)
    狀態 (−|01⟩ + |10⟩)/√2   單看 q0 0.000  單看 q1 0.000
```

`qiskit_check.py`（Qiskit 2.6.2，StatevectorSampler seed=2026；四個線路都用同一個種子，所以次數的數字相同，對應的結果不同）：

```
Φ⁺ 振幅 [0.707, 0.0, 0.0, 0.707] 單看 q0 0.0 單看 q1 0.0 量測 1000 次 {'00': 464, '11': 536}
Φ⁻ 振幅 [0.707, 0.0, 0.0, -0.707] 單看 q0 0.0 單看 q1 0.0 量測 1000 次 {'00': 464, '11': 536}
Ψ⁺ 振幅 [0.0, 0.707, 0.707, 0.0] 單看 q0 0.0 單看 q1 0.0 量測 1000 次 {'01': 464, '10': 536}
Ψ⁻ 振幅 [0.0, -0.707, 0.707, 0.0] 單看 q0 0.0 單看 q1 0.0 量測 1000 次 {'01': 464, '10': 536}
先 X 再 H，和先 H 再 Z，是同一個運算嗎？ True
```

## 動畫畫面（製作代理以 Playwright 1600×900 實拍；basic-circuits.html zoom 0.8）

- #bell 選 Ψ⁻、按起點：「步驟 0 / 3」，|ψ⟩ = |00⟩，兩顆向量的尖端在 (100, 29.5)（北極）。下一步：|ψ⟩ = |11⟩，|11⟩ +1.000 100%，兩支向量在南極。下一步：(|10⟩ − |11⟩) / √2，|10⟩ 藍 +.707、|11⟩ 橘 −.707，「單看 q0」向量在赤道、「單看 q1」在南極。下一步：(−|01⟩ + |10⟩) / √2，|01⟩ 橘 −.707、|10⟩ 藍 +.707，兩顆向量都在球心（橘點）。量測 1,000 次：只有 01、10 兩列（實拍一次 493／507，隨機）。
- 依序按四個選項（最後一步）：Φ⁺ (|00⟩ + |11⟩) / √2 兩根藍；Φ⁻ (|00⟩ − |11⟩) / √2，|11⟩ 橘；Ψ⁺ (|01⟩ + |10⟩) / √2 兩根藍；Ψ⁻ (−|01⟩ + |10⟩) / √2，|01⟩ 橘；四種的兩顆 Bloch 球都只剩球心一點。頁面載入後按 `#dots button:last-child`：「步驟 2 / 2」(|00⟩ + |11⟩) / √2。
- operation.html#register：起點讀數「|ψ⟩ = 1.00 |00⟩／各量子位元 Bloch 長度：q0 1.00，q1 1.00／無糾纏（可分離態）…」；目標 q1 → H：「0.71 |00⟩ + 0.71 |10⟩」長度 1.00、1.00 無糾纏（q1 向量指向 +x，朝向鏡頭）；目標 q0 → CNOT：「0.71 |00⟩ + 0.71 |11⟩」長度 0.00、0.00，粉紅色「有糾纏」，右邊 q0 的箭頭縮成一點；只測 q0：狀態塌縮（實拍一次為 |11⟩），長度 1.00、1.00，無糾纏；均勻疊加：四個 0.50，長度 1.00、1.00，無糾纏。
