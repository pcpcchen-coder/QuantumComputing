# Q111 來源筆記（逐字引文）

查核日：2026-11-18。維基百科頁面由製作代理直接讀取原始 wikitext（action=raw），revision id 取自 Wikimedia REST API（/api/rest_v1/page/title/…）。學程內部文件、簡報與動畫程式由製作代理讀取。程式由製作代理實際執行。

## OpenQASM（Wikipedia，oldid=1305446199）

- 「'''Open Quantum Assembly Language''' ('''OpenQASM'''; pronounced ''open kazm'') is a programming language designed for describing quantum circuits and algorithms for execution on quantum computers.」（連結標記與參考文獻已去除）
- 「It is designed to be an intermediate representation that can be used by higher-level compilers to communicate with quantum hardware, and allows for the description of a wide range of quantum operations, as well as classical feed-forward flow control based on measurement outcomes.」
- 「The language includes a mechanism for describing explicit timing of instructions, and allows for the attachment of low-level definitions to gates for tasks such as calibration.」
- 「Version 3.0 of the specification is the current one」

## Field-programmable gate array（Wikipedia，oldid=1385952866）

- 「A '''field-programmable gate array''' ('''FPGA''') is a type of configurable integrated circuit that can be repeatedly programmed after manufacturing.」

## Qiskit（Wikipedia，oldid=1382602577）

- 「… and a '''transpiler''' that optimizes and converts circuits to run on specific quantum hardware backends. For example, Qiskit allows users to create quantum circuits using an intuitive Python API, then employ the transpiler to adapt and optimize these circuits for a given device’s topology and constraints (reducing gate counts or circuit depth as needed).」

## Quantum logic gate（Wikipedia，oldid=1376542851）

- Swap gate：「The swap gate swaps two qubits.」
- 「In the model of computation used in this article (the quantum circuit model), a classic computer generates the gate composition for the quantum computer, and the quantum computer behaves as a coprocessor that receives instructions from the classical computer about which primitive gates to apply to which qubits.」

## 學程內部文件：docs/超導量子電腦師生對話教學紀錄.md 第 13 課

- 「軟體堆疊把「一行演算法」一路翻成「某條同軸線上、某個奈秒送出去的微波波形」，再把讀回的訊號翻回「0 和 1 的統計」。」
- 七層：「① 應用／演算法　Qiskit、Cirq、PennyLane、CUDA-Q、tket」「② 量子電路 IR　OpenQASM 3、QIR（與硬體無關）」「③ 編譯器　分解 → 映射 → 路由（SWAP）→ 最佳化 → 排程」「④ 脈衝層　原生閘 → 校準好的波形」「⑤ 即時控制　FPGA／RFSoC：時序、播放、中途量測、條件分支」「⑥ 類比硬體　DAC → 混頻 → 冷凍機 → 晶片 → 放大 → ADC」「⑦ 結果處理　判別 → 累積 shot → 讀取誤差緩解 → 直方圖」；「兩根支柱：**自動校準**（餵給 ③④）與**錯誤處理**（現在是緩解，容錯時代是即時解碼器）。」
- 「**分解**：原生閘只有 Rz（任意角）、√X、CZ（有些平台用 √iSWAP 或 ECR）。H = Rz(π/2)·√X·Rz(π/2)；CNOT = 目標 H → CZ → 目標 H；X = √X·√X。」
- 「**映射**：查今天的校準資料，挑錯誤率低且相鄰的實體位元（**校準感知映射**）。」「**路由**：不相鄰就插 SWAP（= 3 個 CNOT，約 3 個 CZ），找最少 SWAP 是 NP-hard，實務上用啟發式（如 SABRE）。」
- 「**最佳化**：Rz 是虛擬 Z、**0 ns**，可合併或消掉；相鄰抵消（如 H·H）。真正的成本是 √X、CZ 的數量與深度。」「**排程**：ASAP 並行；**相鄰 CZ 不能同時**（頻率碰撞，第 4 課）；閒置位元插動態去耦。」
- 脈衝表：「√X｜DRAG 高斯，頻率 f₀₁｜XY｜20–40 ns」「Rz(θ)｜不送東西，改後續脈衝相位｜—｜0 ns」「CZ｜磁通脈衝讓 |11⟩↔|20⟩ 共振｜Z（＋耦合器）｜40–60 ns」「量測｜約 7 GHz 讀取脈衝｜讀取饋線｜0.3–1 μs」。
- 「**即時控制**：所有通道鎖同一個 10 MHz 參考時鐘，以奈秒精度同步播放；條件分支（主動重設、錯誤更正回饋）要在**幾百 ns** 內完成；OpenQASM 3 用 `if`／`while` 描述動態電路。」「**結果處理**：重跑數千 shot；用讀取混淆矩陣修正；**編譯、上傳、排隊常比跑還久**，所以要打包成 job。」
- 「**校準依賴圖**：讀取腔頻譜 → 位元頻譜 → Rabi（π 振幅）→ Ramsey（精修 f₀₁、T₂*）→ T₁／T₂ → DRAG → 讀取最佳化 → 單位元 RB → CZ 校準 → 雙位元 RB／XEB → 頻率配置。失敗就退回上一步；每天甚至每小時自動跑，結果也餵給編譯器。」
- 錯誤處理表：「NISQ｜抑制與緩解｜動態去耦、Pauli twirling、讀取緩解、ZNE、PEC｜多跑很多次」「FTQC｜錯誤更正｜表面碼、即時解碼、lattice surgery、魔術態工廠｜很多實體位元（約 1000:1）」。
- 動畫實際編譯結果表：「Bell @ 直線 5 顆｜…｜0｜1 → 1｜約 0.7 μs」「BV（s = 111，4 位元）@ 直線｜輔助位元要和 3 顆互動，直線最多 2 個鄰居｜2｜3 → 9｜1320 ns」「BV（s = 111）@ 方格 3×3｜…｜0｜3 → 3｜840 ns」；「三個 CNOT 目標相同可以交換順序，先做 CNOT(1→3)、CNOT(2→3) 再搬一次就只要 1 個」。
- 課後練習 4：「GHZ（q0 對 q1、q2 各做 CNOT）放到直線晶片上需要 SWAP 嗎？」答「不需要。映射把 q0 放在中間，兩個鄰居分別放 q1、q2。」

## 學程內部簡報

- slides/transmon.pptx 第 26 頁（課綱寫 p27；p27 實為「一句話總結」，故改引 p26）：「編譯與控制軟體堆疊」「① 全貌　七層：從一行演算法，一路翻成某條同軸線上、某個奈秒的微波波形。」「② 分解　H、CNOT 換成原生閘：Rz、√X、CZ。」「③ 映射　依今天的校準資料，挑相鄰、錯誤率最低的實體位元。」「④ 路由　不相鄰就插 SWAP（每個 SWAP = 3 個 CZ）。」「⑤ 最佳化　H·H 抵消、合併 Rz、虛擬 Z（0 ns）。」「⑥ 排程與脈衝　ASAP 並行，但相鄰 CZ 不能同時做（頻率碰撞）。」「⑦–⑧ 回饋與校準　FPGA 幾百 ns 內完成量測回饋；參數會漂移，要依依賴圖定期重新校準。」
- slides/QC_Operation_Talk.pptx 第 26 頁「轉譯（transpile）：從邏輯線路到硬體」：「① 分解 → 原生閘」「② 配置 邏輯→實體」「③ 路由 插入 SWAP」「④ 最佳化 合併/消去」「⑤ 排程 時間軸 + DD」；表「H｜RZ(π/2) · SX · RZ(π/2)」「CNOT｜(I⊗H) · CZ · (I⊗H)」「SWAP｜3 × CNOT → 3 × CZ + 單位元閘」；「同一個演算法，轉譯好壞可差數倍閘數」「配置要考慮當天校準的錯誤率」。

## 互動動畫程式：animations/transmon-3d.html 第 12 章（CH id: "stack"）

- `TOPO12`：line「直線 5 顆」edges [0,1],[1,2],[2,3],[3,4]；grid「方格 3×3」12 條邊。`ERR1`、`ERR2` 為固定的校準資料。`DUR12 = { SX: 32, RZ: 0, CZ: 48, M: 600, H: 32, X: 32 }`。
- `CIRC12`：bell「Bell」（H、CX(0,1)、M）；ghz「GHZ（3 位元）」（H、CX(0,1)、CX(0,2)、M）；bv「BV（s = 111，含輔助位元）」（X(3)、H×4、CX(0,3)、CX(1,3)、CX(2,3)、H×3、M）。
- compile12 註解：「① 分解：CX → H·CZ·H，X → √X·√X」「② 映射：窮舉初始配置，成本 = SWAP 需求 ×10 + 用到的邊與位元的校準錯誤率」「③ 路由：把 CX 的控制位元沿最短路徑搬到目標旁邊，每一步插一個 SWAP」「④ 最佳化：相鄰 H·H 抵消 → H 展開成 Rz(π/2)·√X·Rz(π/2) → 合併相鄰 Rz、刪掉 Rz(0)」「⑤ 排程：ASAP；同時進行的 CZ 不可彼此相鄰（避免頻率碰撞）」。
- simulate12：「理想結果：狀態向量模擬原始電路，再加上每位元 2% 的讀取誤判」。
- 看板 A 圖例：「青＝單位元閘　金＝Rz（虛擬 Z，0 ns）　橘＝CZ　紅＝兩端不相鄰　紫＝SWAP 展開　藍＝量測」。看板 B：「脈衝時間軸（總長 … ns）」、三條線「XY」「Z」「RO」、白色游標；直方圖「執行結果：…，2000 shots（每位元 2% 讀取誤判）」，最高一根金色。
- 晶片：選中位元金色（0xd6b04a），游標掃到 √X／量測時發光；CZ 進行中的連線變橘色（0xd77b45）。
- 步驟 ⑦ cue：「即時回饋：量到 1 就送 π 脈衝（主動重設）。下方時間軸：讀取 600 ns → FPGA 判斷約 300 ns → 條件脈衝。」「這整段要在幾百 ns 到 1 μs 內完成；錯誤更正的回饋也是同一套機制。OpenQASM 3 的 if／while 就是描述這種動態電路。」
- 步驟 ⑧：「Ramsey 量到頻率漂了太多、擬合失敗（紅色）——頻率不準，π 振幅也不可信，所以退回 Rabi 重做，再往下走。」「大型系統每天甚至每小時自動跑一次。」
- 自由實驗（g12BindFree）：`[data-ck12]`「Bell」「GHZ」「BV」、`[data-tp12]`「直線 5 顆」「方格 3×3」（換晶片保留目前階段）、`#g12prevS`「◀ 上一階段」、`#g12nextS`「下一階段 ▶」（capShow stageNote12）、`#g12play`「播放脈衝」、`#g12run`「執行 2000 shots」；stageNote12「路由：插入 … 個 SWAP，CZ 從 … 個變成 … 個。」

## 互動動畫程式：animations/js/operation/12_workflow.js（場景 12「一次量子計算的完整流程」）

- 六站：「① 寫程式」「② 轉譯」「③ 脈衝排程」「④ 控制電子」「⑤ 晶片執行 shots」「⑥ 判別與結果」；封包每站 2.2 秒（第 ⑤ 站 3.5 秒）自動前進。
- `times = () => { const reset = active ? 2.0 : 250, gates = depth * 0.1, meas = 1.0; … }`；插圖「一個 shot 的時間組成（μs）與總執行時間」「每 shot … μs × … shots = …」「另加：佇列、轉譯、波形載入、網路傳輸（秒～分鐘）」「數值為典型量級（依系統而異）」。
- 控制項：「自動播放」「下一站 ▶」「shots N」（log10，2–5）「線路深度（層）」（1–1000，預設 20）「主動重置（量測 + 條件 π 脈衝）」。NOTES：「所有儀器鎖在同一個 10 MHz 參考時脈，觸發後同步輸出。」

## 製作代理試拍（2026-11-18，單張截圖，非正式錄影、非 QV2_DRY，nice -n 19）

- #stack 點步驟 9 → 連按兩次「下一階段 ▶」：看板 A「② 映射到實體位元」、Q0–Q2 的 CZ 為紅色；看板 B「映射：…；有 1 個 CZ 兩端不相鄰。」再按一次：紫色 SWAP 展開，看板 B「路由：插入 2 個 SWAP，CZ 從 3 個變成 9 個。」按「方格 3×3」：看板 B「路由：插入 0 個 SWAP，CZ 從 3 個變成 3 個。」「映射：q0→Q0、q1→Q2、q2→Q4、q3→Q1；SWAP 0 個；總時間 840 ns」（左上角字幕不會因換晶片而更新）。
- 「播放脈衝」：看板 B「脈衝時間軸（總長 1320 ns）」（直線）／「（總長 840 ns）」（方格），方格時讀取（藍）從約 240 ns 到 840 ns。「執行 2000 shots」：直方圖最高一根「111」金色，其他幾根矮的（隨機，旁白不念）。
- operation.html#workflow：插圖「重置：250 μs（98.8%）」「閘：2.0 μs（0.8%）」「讀取：1.0 μs（0.4%）」「每 shot 253.0 μs × 1,000 shots = 253.0 ms」；打開主動重置後「重置：2.0 μs（40.0%）」「每 shot 5.0 μs × 1,000 shots = 5.0 ms」；shots N 拉到 5：「每 shot 5.0 μs × 100,000 shots = 500.0 ms」。

## 實跑紀錄（stack_race.py，Python 3.13.18，無外部套件，無亂數）

```
一、原生閘驗算（只差一個整體相位就算相同）
  H = Rz(π/2)·√X·Rz(π/2)：相同 ✓
  X = √X·√X：相同 ✓
  CNOT = H·CZ·H（H 做在目標）：相同 ✓
  SWAP = 3 個 CNOT：相同 ✓
二、效能競賽（總時間含讀取 600 ns；√X 32 ns、Rz 0 ns、CZ 48 ns）
  Bell @ 直線 5 顆：SWAP 0 個，CZ 1 → 1 個，√X 3 個，總時間 712 ns，結果和原始電路相同 ✓
  Bell @ 方格 3×3：SWAP 0 個，CZ 1 → 1 個，√X 3 個，總時間 712 ns，結果和原始電路相同 ✓
  GHZ（3 位元） @ 直線 5 顆：SWAP 0 個，CZ 2 → 2 個，√X 5 個，總時間 760 ns，結果和原始電路相同 ✓
  GHZ（3 位元） @ 方格 3×3：SWAP 0 個，CZ 2 → 2 個，√X 5 個，總時間 760 ns，結果和原始電路相同 ✓
  BV（s = 111） @ 直線 5 顆：SWAP 2 個，CZ 3 → 9 個，√X 19 個，總時間 1320 ns，結果和原始電路相同 ✓
  BV（s = 111） @ 方格 3×3：SWAP 0 個，CZ 3 → 3 個，√X 9 個，總時間 840 ns，結果和原始電路相同 ✓
三、聰明一點的路由：BV 在直線晶片上，三個 CNOT 換順序
  CNOT(0→3) → CNOT(1→3) → CNOT(2→3)：SWAP 2 個，CZ 9 個，總時間 1320 ns，結果相同 ✓
  CNOT(0→3) → CNOT(2→3) → CNOT(1→3)：SWAP 2 個，CZ 9 個，總時間 1288 ns，結果相同 ✓
  CNOT(1→3) → CNOT(0→3) → CNOT(2→3)：SWAP 1 個，CZ 6 個，總時間 1112 ns，結果相同 ✓
  CNOT(1→3) → CNOT(2→3) → CNOT(0→3)：SWAP 1 個，CZ 6 個，總時間 1080 ns，結果相同 ✓
  CNOT(2→3) → CNOT(0→3) → CNOT(1→3)：SWAP 1 個，CZ 6 個，總時間 1080 ns，結果相同 ✓
  CNOT(2→3) → CNOT(1→3) → CNOT(0→3)：SWAP 1 個，CZ 6 個，總時間 1112 ns，結果相同 ✓
四、七層堆疊說明卡：GHZ（3 位元） @ 直線 5 顆（MY_CIRCUIT、MY_CHIP）
  ① 應用層：H(0) CX(0,1) CX(0,2) M(0,1,2)
  ② 電路 IR：4 個邏輯操作，還沒指定晶片
  ③ 編譯器：分解成 2 個 CZ；映射 q0→Q2、q1→Q1、q2→Q3；插 0 個 SWAP；抵消 0 對 H·H；剩 √X 5、Rz 10、CZ 2
  ④ 脈衝層：√X 變成 32 ns 的微波脈衝、CZ 變成 48 ns 的磁通脈衝、Rz 只改相位（0 ns）；閘在 160 ns 做完，讀取到 760 ns
  ⑤ 即時控制：控制電子照時間軸同步播放、讀取；動態電路要在幾百 ns 內判斷並回饋
  ⑥ 類比硬體：數位波形 → 混頻 → 冷凍機 → 晶片 → 放大 → 數位化
  ⑦ 結果處理：理想機率 {'000': 0.5, '111': 0.5}；實際要重跑數千次，再修正讀取誤差
```

另以 node 直接執行動畫原始碼中的 compile12（擷取 TOPO12、ERR1、ERR2、CIRC12、DUR12、compile12），六種組合的映射、SWAP、CZ、√X、Rz、抵消對數與總時間和 stack_race.py 完全相同（例：bv line L0 q0→Q0、q1→Q1、q2→Q3、q3→Q2，swap 2，CZ 3 → 9，√X 19、Rz 34，HH 4，total 1320；bv grid swap 0，total 840）。
