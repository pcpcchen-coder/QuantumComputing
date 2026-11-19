# Q057 來源筆記（逐字引文）

查核日：2026-11-18。GHZ 頁的 wikitext 與 revision id（頁面 wgRevisionId）由製作代理直接取得；Bell state、Qiskit 引文沿用 Q010（同 revision）。學程內部簡報與動畫程式由製作代理讀取。程式由製作代理實際執行。

## Greenberger–Horne–Zeilinger state（Wikipedia，oldid=1384329441）

- 「a Greenberger–Horne–Zeilinger (GHZ) state is an entangled quantum state that involves at least three subsystems (particle states, qubits, or qudits). Named for the three authors that first described this state」
- 「The GHZ state is an entangled quantum state for 3 qubits and it can be written |GHZ⟩ = (|000⟩ + |111⟩)/√2」
- 「If a measurement is made on one of the photons using a two-channel polarizer aligned with the axes of the coordinate system, each orientation will be observed with 50% probability. However the result of all three measurements on the state gives the same result」
- 「for a collection of M qubits, it reads |GHZ⟩ = (|0⟩^⊗M + |1⟩^⊗M)/√2」

## Bell state（Wikipedia，oldid=1365950086；引自 Q010）

- 「The Bell states are four specific maximally entangled quantum states of two qubits.」

## Qiskit（Wikipedia，oldid=1382602577；引自 Q010）

- 「Qiskit (Quantum Information Software Kit) is an open-source, Python-based, high-performance software stack for quantum computing」
- 「executing them on quantum computers or classical simulators.」
- 「Qiskit Aer (qiskit-aer) – A high‑performance simulator for quantum circuits, featuring multiple simulation backends and support for realistic noise models.」

## 學程內部簡報

- slides/QC_Operation_Talk.pptx 第 27 頁「實際操作：用 Qiskit 跑一個 Bell 態」：「理想：00、11 各 50%」「01、10 出現 = 雜訊（閘、讀取錯誤）」。講者備註：「程式介面依版本會調整，實際使用時以官方文件為準。」（該頁連 IBM 雲端真機；本集只用本機模擬器。）
- slides/output/basic-circuits.pptx 第 13 頁「範例 4｜GHZ 態：CNOT 一路串下去」：「① H 閘（q0）(|000⟩ + |001⟩)/√2」「② CNOT（q0 → q1）(|000⟩ + |011⟩)/√2」「③ CNOT（q1 → q2）(|000⟩ + |111⟩)/√2」「三顆全部糾纏：不是全 0 就是全 1」。
- 第 14 頁：「硬體常用 GHZ 態測試糾纏品質：雜訊越大，量到 000、111 以外結果的比例越高」；備註「GHZ 電路的深度會隨位元數增加，每多一顆就多一個 CNOT」。
- 第 28 頁：互動動畫「右下可以量測 1 次或 1,000 次：灰底是理論機率、綠色是實際次數」。第 29 頁：「頁面底部附會隨選項改變的 Qiskit 程式碼，可以複製到自己的電腦執行」。

## 互動動畫程式

- animations/basic-circuits.html：範例 4 id "ghz"，選項「位元數」3 顆／4 顆；build() 依序 H(0)、CX(i, i+1)；最後一步 caption「…只剩 |000⟩ 和 |111⟩ 兩項，各 50%」；take「硬體廠常用它來測試多位元糾纏的品質…（這裡是理想模擬，所以不會出現）」；按鈕 #bNext「下一步 ▶」、#m1000「量測 1,000 次」、#mClear「清除」；量測列只列出理論機率不為零的結果；qiskitCode() 產生 `qc.cx(2, 3)` 等程式碼。
- animations/js/operation/06_circuit.js：範例按鈕「GHZ 態（3 位元糾纏）」4 欄（H、CNOT q0→q1、CNOT q1→q2、量測）；「單步 ▶」；「加入雜訊（每閘 1%、讀取 3%）」開關；量測欄 1000 shots，右下插圖「量測 1000 shots 的結果（青線 = 理想機率）」。

## 實跑紀錄（bell_ghz_release.py，Python 3.13.18、qiskit 2.6.2、qiskit-aer 0.18.4、seed_simulator=2026）

```
N=2 理想 {'00': 516, '11': 508}
N=2 雜訊 {'00': 478, '01': 49, '10': 32, '11': 465} → 錯誤結果 81 次，出現 4 種
N=3 理想 {'000': 514, '111': 510}
N=3 雜訊 {'000': 471, '001': 20, '010': 11, '011': 19, '100': 23, '101': 15, '110': 21, '111': 444} → 錯誤結果 109 次，出現 8 種
N=4 理想 {'0000': 499, '1111': 525}；雜訊 錯誤結果 158 次，出現 15 種
N=5 理想 {'00000': 476, '11111': 548}；雜訊 錯誤結果 173 次，出現 21 種
qc.x(0) 後量 3 顆：{'001': 1024}
```
