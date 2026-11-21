# Q004 來源筆記（逐字引文）

查核日：2026-11-18。維基百科頁面由製作代理以網頁擷取工具開啟；學程內部簡報與 3D 場景程式由製作代理讀取。

## Quantum logic gate（Wikipedia，oldid=1376542851）

- 「The Pauli X, Y and Z equate, respectively, to a rotation around the x, y and z axes of the Bloch sphere by π radians.」
- 「The Pauli-X gate is the quantum equivalent of the NOT gate for classical computers」
- 「It is sometimes called a bit-flip as it maps |0⟩ to |1⟩ and |1⟩ to |0⟩.」
- 「Due to this nature, Pauli Z is sometimes called phase-flip.」
- 「The Hadamard gate performs a rotation of π about the axis (x̂+ẑ)/√2 at the Bloch sphere, and is therefore involutory.」（擷取文字顯示為 /2，根號在轉換時遺失；學程場景 ROT 表用 [s2, 0, s2]，s2=1/√2）
- 「(it creates an equal superposition state if given a computational basis state)」
- 「Unlike many classical logic gates, quantum logic gates are reversible.」
- 「Measurement (sometimes called observation) is irreversible and therefore not a quantum gate,」

## 學程內部簡報：slides/QC_Operation_Talk.pptx 第 18 頁（講者備註）

- 「單位元閘就是 Bloch 球上的旋轉，數學上是 2 乘 2 的么正矩陣。」
- 「X 閘繞 x 軸轉 180 度，把 0 和 1 對調，是量子版的 NOT。」
- 「Z 閘繞 z 軸轉 180 度，|0⟩ 不變、|1⟩ 變號——這種只改相位的閘，單獨量測看不出差別，但在干涉中非常重要。」
- 「H，也就是 Hadamard 閘，繞 x 和 z 中間的軸轉 180 度，把 |0⟩ 變成 |+⟩，是產生疊加的主力」
- 「依序按 H、Z、H，會發現效果等於 X」

## 3D 場景：animations/operation.html#gates（js/operation/02_gates.js、common.js）

- ROT 表：X: [[1,0,0], π]、Z: [[0,0,1], π]、H: [[s2,0,s2], π]。
- 說明：「點下方的閘，看狀態向量怎麼轉。粉紅線是旋轉軸。」
- 按鈕：X、Y、Z、H、S、S†、T、T†、√X、Rx(θ)、Ry(θ)、Rz(θ)、重設 |0⟩、重設 |1⟩、清除軌跡、示範：H → Z → H = X；讀數顯示布洛赫向量與 P(0)、P(1)；插圖顯示最後一個閘的矩陣與線路紀錄。
- 布洛赫座標 (x,y,z) → three.js (y,z,x)；預設相機 [3.8, 2.6, 4.6]，所以 +x（|+⟩）朝向觀眾的前方。

## 六關答案推算（製作代理）

1. 到南極：X。 2. 到赤道前方：H。 3. 到赤道後方：X→H 或 H→Z（兩顆）。
4. 不用 X 到南極：H→Z→H。 5. X→H→Z→H：|0⟩→|1⟩→|−⟩→|+⟩→|0⟩，回到北極。 6. 只用 X、Z：只在兩極之間，到不了赤道（無解）。
