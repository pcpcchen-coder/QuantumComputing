# Q055 來源筆記（逐字引文）

查核日：2026-11-18。維基百科頁面由製作代理以 `index.php?action=raw` 取得 wikitext（revision id 取自 API `prop=revisions`）。學程內部簡報（python-pptx 讀取，含講者備註）、對話紀錄與動畫程式由製作代理讀取。

## Superconducting quantum computing（Wikipedia，oldid=1382042448）

- 「One popular gating mechanism uses two qubits and a bus, each tuned to different energy level separations. Applying microwave excitation to the first qubit, with a frequency resonant with the second qubit, causes a σx rotation of the second qubit. Rotation direction depends on the state of the first qubit, allowing a controlled phase gate construction.」（引用 Chow 等，"Simple All-Microwave Entangling Gate for Fixed-Frequency Superconducting Qubits", PRL 107, 080502 (2011)）
- 「Higher levels (outside of the computational subspace) of a pair of coupled superconducting circuits can be used to induce a geometric phase on one of the computational states of the qubits. This leads to an entangling conditional phase shift of the relevant qubit states. This effect has been implemented by flux-tuning the qubit spectra」（引用 DiCarlo 等，Nature 460, 240 (2009)）
- 「single-qubit gates combined with two-qubit gates form a universal gate set」

## Quantum logic gate（Wikipedia，oldid=1376542851）

- 「the controlled NOT gate (or CNOT or CX) acts on 2 qubits, and performs the NOT operation on the second qubit only when the first qubit is |1⟩, and otherwise leaves it unchanged.」
- 「When U is one of the Pauli operators, X, Y, Z, the respective terms "controlled-X", "controlled-Y", or "controlled-Z" are sometimes used. Sometimes this is shortened to just CX, CY and CZ.」

## Controlled NOT gate（Wikipedia，oldid=1357848270）

- 「A quantum circuit that performs a Hadamard transform followed by CNOT then another Hadamard transform, can be described as performing the CNOT gate in the Hadamard basis (i.e. a change of basis)」——本課用的等式 CNOT = (I⊗H)·CZ·(I⊗H) 取自學程簡報 p22，並以矩陣驗算（fact-check.md）。

## Avoided crossing（Wikipedia，oldid=1368929468）

- 「an avoided crossing … is the phenomenon where two eigenvalues of a Hermitian matrix representing a quantum observable and depending on k continuous real parameters cannot become equal in value ("cross") except on a manifold of dimension k − 2.」

## 學程內部簡報：slides/QC_Operation_Talk.pptx

- 第 22 頁「兩位元閘：產生糾纏的唯一方法」：「CNOT（CX）控制 = 1 時翻轉目標」「CZ 兩個都是 1 時加負號（對稱）｜|11⟩→ −|11⟩」「CNOT = (I⊗H) · CZ · (I⊗H)」「CZ 對稱：不分控制與目標」「單位元閘無法產生糾纏」「任一兩位元糾纏閘 + 單位元閘 = 通用」「SWAP … = 3 個 CNOT」。
- 第 23 頁「兩位元閘的物理實現：CZ 與交叉共振」：「CZ：磁通調頻（Google 等）｜磁通脈衝把 A 的頻率往下拉，使 |11⟩ 靠近 |20⟩｜能階排斥（迴避交叉）→ 只有 |11⟩ 多累積相位｜累積到 π 即為 CZ；約 40–70 ns」「交叉共振 CR（IBM 固定頻率）｜以 B 的頻率驅動 A｜B 繞 ±x 旋轉，方向取決於 A（ZX 交互作用）｜ZX(π/2) + 單位元修正 = CNOT；~200–500 ns」。
  講者備註：「調『脈衝深度』越靠近交叉點，相位累積越快，但洩漏到 |20⟩ 的風險也越高」「切換到『交叉共振 CR』模式，可以看到兩個 Bloch 球往相反方向轉」「兩位元閘比單位元閘慢、錯誤率也高大約 10 倍，是目前量子電腦誤差的主要來源。」
- 第 24 頁「通用閘組與各家的原生閘」：「IBM Eagle｜ECR、RZ、SX、X｜固定頻率、交叉共振、重六角耦合」「IBM Heron｜CZ、RZ、SX、X（+ 分數角 RZZ）｜可調耦合器」「Google Sycamore / Willow｜CZ（或 √iSWAP 類）、Phased-XZ｜可調頻率 + 可調耦合器、方格」「Rigetti｜RX(±π/2)、RZ、CZ / iSWAP｜可調耦合器」「離子阱（參考）｜R(θ,φ)、MS / ZZ｜全連接、閘較慢」「各平台原生閘依世代而異，以官方文件為準」；備註「ECR 是基於交叉共振的兩位元閘；新的 Heron 處理器有可調耦合器，原生兩位元閘換成 CZ」。
- slides/transmon.pptx 第 21 頁（課綱補充素材）：「① 糾纏　CZ 只把 |11⟩ 翻成負號，a₀₀·a₁₁ ≠ a₀₁·a₁₀，就拆不回兩顆各自的狀態。」

## 對話紀錄：docs/超導量子電腦師生對話教學紀錄.md 第 4 課（第 302–373 行）

- 「耦合造成交換：耦合 g 約數–20 MHz；失諧接近 0 就互換激發」「多能階：A 的 0→1 = 5.21、1→2 = 4.93 … 任何一條撞上鄰居任何一條，就是碰撞。」
- 「固定頻率的 CR 閘希望 B 落在 A 的 0→1 和 1→2 之間（straddling regime）。」
- 固定頻率（IBM）與可調頻率（Google）對照表；「可調耦合器把 g 關到近 0」。
- 動畫演示：「步驟 5：CZ 閘拿到 −1 相位；反例路徑會掃過 Q2」「步驟 6 自由實驗：三條 Z 線滑桿，碰撞清單即時更新」。

## 互動動畫程式

- animations/js/operation/05_twoqubit.js：desc（第 6–9 行）「用磁通脈衝把量子位元 A 的頻率往下拉，使 |11⟩ 接近 |20⟩ … 只有 |11⟩ 會額外累積相位。累積到 π 時就是 CZ」「其他態 … 的單位元相位用虛擬 Z 修正掉。脈衝太快或太靠近交叉點，會讓狀態跑到 |20⟩（洩漏）」「交叉共振 CR（IBM 固定頻率架構）：用『目標 B 的頻率』去驅動控制 A … B 會繞 x 軸旋轉，但方向取決於 A」「典型：兩位元閘 40–300 ns，錯誤率 0.1–1%，是目前誤差的主要來源」。
  模型參數（第 32 行）fB = 5.0、al = −0.25、gq = 0.015、fA0 = 6.0（GHz）；讀數（第 130–132 行）；CR 讀數（第 140 行）。
- animations/transmon-3d.html 第 6 章（第 940–947、1225–1351 行）：QC.alpha = −0.283（第 637 行）；ALLOC 4.90／5.10／5.30 GHz；
  步驟 5 字幕「目標：讓 Q2、Q3 做 CZ。交會點是 f_Q3 = f_Q2 − α = 5.383 GHz（|11⟩ ↔ |20⟩ 共振）」「這正是平常要避開的禁區：做閘時才刻意去，而且只停留幾十 ns」「|11⟩ 的振幅流到 |20⟩ 又流回來，多了一個 −1 相位」「反例：若改走 |11⟩↔|02⟩，Q3 得降到 4.817 GHz，途中會掃過 Q2 的 5.10 → 交換錯誤」。

## 數值重算

- `/home/user/qwork/q055calc/cz.js`：照抄 05_twoqubit.js 的 branch／fA／zeta／phaseTotal／autoPi 與讀數公式，用 Node 執行（輸出 cz.out）。
- `/home/user/qwork/q055calc/checks.py`：4×4 矩陣檢查 CZ 對稱、CNOT = (I⊗H)·CZ·(I⊗H)、ZX(π/2) 加單位元修正 = CNOT、CR 讓目標依控制往相反方向轉、CZ 對 |++⟩ 產生糾纏（輸出 checks.out）。
- `/home/user/qwork/q055calc/sim.js`、`mkspec.py`：依 demos_extra/q055.py 的時間表在 1600×900 Chromium（swiftshader）操作動畫並截圖（不錄影）。
