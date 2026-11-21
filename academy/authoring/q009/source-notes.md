# Q009 來源筆記（逐字引文）

查核日：2026-11-18。維基百科兩頁由製作代理開啟並摘錄逐字引文。學程內部簡報與 3D 場景程式由製作代理讀取。

## Quantum circuit（Wikipedia，oldid=1383192653）

- 「Circuits are written such that the horizontal axis is time, starting at the left hand side and ending at the right.」
- 「Horizontal lines are qubits, doubled lines represent classical bits.」
- 「the items that are connected by these lines are operations performed on the qubits, such as measurements or gates.」

## Quantum logic gate（Wikipedia，oldid=1376542851）

- 「In circuit diagrams, single lines are qubits, and doubled lines are bits.」
- 圖說：「Circuit representation of measurement. The two lines on the right hand side represent a classical bit.」
- 「The order in which they appear on the wire is reversed when multiplying them together.」（乘積依順序而定）
- 「Take a register A with n qubits all initialized to |0⟩」

## 學程內部簡報：slides/QC_Operation_Talk.pptx 第 25 頁「量子線路怎麼讀」

- 表格：「水平線｜一個量子位元（時間由左到右）」「方塊｜單位元閘（H、X、Rz…）」「M / 儀表｜量測 → 存到古典位元」「雙線｜古典位元」。
- 「同一欄的閘可同時執行」。
- 講者備註：「每條水平線是一個量子位元，時間從左往右；方塊是單位元閘……儀表符號是量測」；「按『單步』可以一步一步看狀態怎麼變；執行到最後的量測欄會跑 1000 shots」。

## 學程簡報：slides/output/basic-circuits.pptx 第 3、4 頁

- 第 3 頁：「電路圖：q0 在最上面」。
- 第 4 頁：H「|0⟩ → (|0⟩ + |1⟩)/√2」；X「|0⟩ ↔ |1⟩」；Z「|0⟩ 不變，|1⟩ → −|1⟩」「繞 z 軸轉 180°」。

## 3D／互動場景程式

- animations/js/operation/06_circuit.js：範例「干涉：H–Z–H」，說明「H 再把兩條路徑合併……→ 100% 得到 1」；按鈕「單步 ▶」「播放」「⏮ 重設」；執行中的閘 emissiveIntensity 0.8；量測欄 sample() 跑 1000 次；初始說明「所有量子位元都是 |0⟩」。
- animations/basic-circuits.html：每條線左端標「|0⟩」、右端畫量測錶（class="meter"）；干涉範例說明「H·Z·H = X」「H·H 等於什麼都沒做」。
