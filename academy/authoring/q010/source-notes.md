# Q010 來源筆記（逐字引文）

查核日：2026-11-18。維基百科頁面由製作代理直接開啟（revision id 取自頁面的 wgRevisionId）。學程內部簡報與動畫程式由製作代理讀取。程式由製作代理實際執行。

## Bell state（Wikipedia，oldid=1365950086）

- 「The Bell states are four specific maximally entangled quantum states of two qubits.」
- 「Through communication they would discover that, although their outcomes separately seemed random, these were perfectly correlated.」

## Controlled NOT gate（Wikipedia，oldid=1357848270）

- 「The CNOT gate flips the second qubit (the target qubit) if and only if the first qubit (the control qubit) is |1⟩.」
- 「It can be used to entangle and disentangle Bell states.」

## Qiskit（Wikipedia，oldid=1382602577）

- 「Qiskit (Quantum Information Software Kit) is an open-source, Python-based, high-performance software stack for quantum computing」
- 「executing them on quantum computers or classical simulators.」
- 「Qiskit Aer (qiskit-aer) – A high‑performance simulator for quantum circuits, featuring multiple simulation backends and support for realistic noise models.」

## 學程內部簡報

- slides/QC_Operation_Talk.pptx 第 27 頁「實際操作：用 Qiskit 跑一個 Bell 態」：`qc.h(0)`、`qc.cx(0, 1)`、`qc.measure_all()`；「理想：00、11 各 50%」「01、10 出現 = 雜訊（閘、讀取錯誤）」。講者備註：「程式介面依版本會調整，實際使用時以官方文件為準。」（該頁用 IBM 雲端真機；本集改用本機模擬器，不需帳號。）
- slides/output/basic-circuits.pptx 第 10 頁：「① 起點 |00⟩」「② H 閘（q0）(|00⟩ + |01⟩)/√2」「③ CNOT（q0 → q1）(|00⟩ + |11⟩)/√2」「各自隨機、彼此一致……這就是糾纏」。
- 第 28 頁：「Bell 態：量測 1,000 次」；備註「右圖是 Bell 態量測 1,000 次，只出現 00 和 11。」

## 互動動畫程式

- animations/basic-circuits.html：Bell 範例選項 Φ⁺、Φ⁻、Ψ⁺、Ψ⁻（準備步驟分別為無、X(q0)、X(q1)、X(q0)X(q1)）；caption「注意 Φ⁻ 和 Φ⁺ 量起來一模一樣，差在負號」；頁首「寫成位元字串時 q0 在最右邊」；按鈕「量測 1,000 次」；「Qiskit 程式碼」區塊。
- animations/js/operation/06_circuit.js：bell 線路、「單步 ▶」、「加入雜訊（每閘 1%、讀取 3%）」開關、最後量測欄跑 1000 shots。

## 實跑紀錄（bell_simulator.py，qiskit 2.6.2、qiskit-aer 0.18.4）

```
{'00': 516, '11': 508}          # seed_simulator=2026
{'11': 506, '00': 518} / {'00': 494, '11': 530} / {'00': 510, '11': 514}   # 不固定種子另跑三次
x(1) 在前：{'10': 516, '01': 508}；x(0) 在前：{'00': 524, '11': 500}；x(0)、x(1) 在前：{'01': 524, '10': 500}
qc.x(0) 後量測：{'01': 10}       # 位元字串最右邊是 q0
```
