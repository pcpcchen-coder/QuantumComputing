# Q056 來源筆記（逐字引文）

查核日：2026-11-18。維基百科頁面由製作代理以 `index.php?action=raw` 取得 wikitext（revision id 取自 API `prop=revisions`，存於 `/home/user/qwork/q056wiki/`）。學程內部簡報、對話紀錄與動畫程式由製作代理讀取。

## Quantum logic gate（Wikipedia，oldid=1376542851）

- 「The swap gate swaps two qubits. With respect to the basis |00⟩, |01⟩, |10⟩, |11⟩, it is represented by the matrix SWAP = [[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]].」
- 「Controlled gates act on 2 or more qubits, where one or more qubits act as a control for some operation. For example, the controlled NOT gate (or CNOT or CX) acts on 2 qubits, and performs the NOT operation on the second qubit only when the first qubit is |1⟩, and otherwise leaves it unchanged.」

## Controlled NOT gate（Wikipedia，oldid=1357848270）

- 「The CNOT gate can be further decomposed as products of rotation operator gates and exactly one two qubit interaction gate」
- 註：「H₂ · CNOT · H₂ = SWAP · CNOT · SWAP」（兩側夾 H 會交換控制與目標的角色）。

## 學程內部簡報：slides/QC_Operation_Talk.pptx

- 第 26 頁「轉譯（transpile）：從邏輯線路到硬體」：「① 分解 → 原生閘｜② 配置 邏輯→實體｜③ 路由 插入 SWAP｜④ 最佳化 合併/消去｜⑤ 排程 時間軸 + DD」；
  表格「H｜RZ(π/2) · SX · RZ(π/2)」「CNOT｜(I⊗H) · CZ · (I⊗H)」「SWAP｜3 × CNOT → 3 × CZ + 單位元閘」「任意 U｜RZ · SX · RZ · SX · RZ」；
  「為什麼重要：不相鄰的兩位元閘要先用 SWAP 搬近：每個 SWAP = 3 個兩位元閘｜同一個演算法，轉譯好壞可差數倍閘數｜配置要考慮當天校準的錯誤率｜轉譯後的線路才是真正執行的內容 → 看它的深度與兩位元閘數」；
  「範例：q0、q2 不相鄰 → CNOT(q0,q2) 變成 SWAP(q1,q2) + CNOT(q0,q1)，兩位元閘 1 → 4 個」。
- 第 26 頁講者備註：「硬體只有相鄰的量子位元能做兩位元閘，不相鄰的就要插入 SWAP 把它們搬近。每個 SWAP 等於三個兩位元閘，代價很高。」「第四，最佳化：合併相鄰的旋轉、消掉互相抵銷的閘。」「一定要看轉譯後的線路，因為那才是真正被執行的內容，尤其是它的深度和兩位元閘數量。」
- 第 15 頁「認識你的後端」表格：「兩位元閘錯誤｜每個 CZ / ECR 的錯誤率｜0.1% ~ 1%（40–500 ns）」「耦合圖｜哪些量子位元之間可做兩位元閘｜方格、重六角（heavy-hex）等」。
- 簡報第 25 頁（量子線路怎麼讀）與第 27 頁（Qiskit Bell 範例）只作背景，本集未引用數字。課綱另列的 transmon.pptx 第 27 頁是「一句話總結」與 3D 動畫連結，本集只用其連結的第 12 章。

## 師生對話紀錄：docs/超導量子電腦師生對話教學紀錄.md

- 第 13 課：「分解：原生閘只有 Rz（任意角）、√X、CZ（有些平台用 √iSWAP 或 ECR）。H = Rz(π/2)·√X·Rz(π/2)；CNOT = 目標 H → CZ → 目標 H」「映射：查今天的校準資料，挑錯誤率低且相鄰的實體位元」「路由：不相鄰就插 SWAP（= 3 個 CNOT，約 3 個 CZ），找最少 SWAP 是 NP-hard，實務上用啟發式（如 SABRE）」「最佳化：Rz 是虛擬 Z、0 ns，可合併或消掉；相鄰抵消（如 H·H）。真正的成本是 √X、CZ 的數量與深度。」
- 第 13 課動畫編譯結果表：「BV（s = 111，4 位元）@ 直線｜輔助位元要和 3 顆互動，直線最多 2 個鄰居｜2｜3 → 9｜1320 ns」「BV（s = 111）@ 方格 3×3｜輔助位元放在有 3–4 個鄰居的位置｜0｜3 → 3｜840 ns」；「直線上的簡單路由照原順序插了 2 個 SWAP；三個 CNOT 目標相同可以交換順序，先做 CNOT(1→3)、CNOT(2→3) 再搬一次就只要 1 個」。
- 第 13 課練習 4 答案：「不需要。映射把 q0 放在中間，兩個鄰居分別放 q1、q2。」
- 第 4 課：「降低連接度最有效：IBM 的 heavy-hex 每顆最多 2–3 個鄰居，代價是部分演算法需要更多 SWAP（第 13 課會再看到）」；第 13 課「軟硬體共同設計（heavy-hex 減碰撞但多 SWAP）」。

## 互動動畫程式：animations/transmon-3d.html 第 12 章

- TOPO12（第 3371–3374 行）：「直線 5 顆」邊 0–1、1–2、2–3、3–4；「方格 3×3」12 條邊。
- CIRC12（第 3694–3698 行）：bv = X(3)、H(3)、H(0..2)、CX(0,3)、CX(1,3)、CX(2,3)、H(0..2)、M。
- compile12（第 3701–3792 行）：分解 CNOT → H·CZ·H；映射窮舉、成本 = SWAP 需求 ×10 + 錯誤率；路由沿最短路徑每步插 SWAP；SWAP 展開成三個 CNOT（每個 H·CZ·H）；最佳化 H·H 抵消、H → Rz(π/2)·√X·Rz(π/2)、合併 Rz；排程 ASAP、相鄰 CZ 不重疊；DUR12 √X 32 ns、Rz 0、CZ 48、M 600。
- G12STEPS 第 4 步 body：「其實三個 CNOT 的目標相同、可以交換順序，先做 CNOT(1→3)、CNOT(2→3) 再搬一次，只要 1 個 SWAP——這正是真正的編譯器要搜尋的空間。在大電路裡找最少 SWAP 的安排是 NP-hard，實務上用啟發式演算法（例如 SABRE）。」
- 自由實驗按鈕：第 3885–3887 行；g12BindFree 第 3911–3923 行；stageNote12 第 3925–3935 行；看板圖例第 3988 行「青＝單位元閘　金＝Rz（虛擬 Z，0 ns）　橘＝CZ　紅＝兩端不相鄰　紫＝SWAP 展開　藍＝量測」。

## 數值重算

`/home/user/qwork/q056calc/`：checks.py（numpy 矩陣恆等式與窮舉最少 SWAP）、c12b.js（從 transmon-3d.html 擷取 compile12 在 Node 執行）、routing_lab.py（教材程式）。截圖：`/home/user/qwork/q056shots/`。
