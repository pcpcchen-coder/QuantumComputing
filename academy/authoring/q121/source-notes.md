# Q121 來源筆記（逐字引文）

查核日：2026-11-19（檔頭 CHECKED 依派工統一寫 2026-11-18）。維基百科頁面由製作代理直接讀取原始 wikitext（action=raw），revision id 取自頁面的 wgRevisionId。學程內部簡報（python-pptx 讀出實際頁碼、文字與備註）、文件與動畫程式由製作代理讀取，畫面以 Playwright 單張截圖確認。程式由製作代理實際執行。

## Grover's algorithm（Wikipedia，oldid=1385418712）

- 「'''Grover's algorithm''', also known as the '''quantum search algorithm''', is a quantum algorithm for unstructured search that finds with high probability the unique input to a black box function that produces a particular output value, using just O(√N) evaluations of the function … It was devised by Indian-American computer scientist Lov Grover in 1996.」
- 「The analogous problem in classical computation would have a query complexity O(N) (i.e., the function would have to be evaluated O(N) times: there is no better approach than trying out all input values one after the other, which, on average, takes N/2 steps).」
- 「Unlike other quantum algorithms, which may provide exponential speedup over their classical counterparts, Grover's algorithm provides only a quadratic speedup.」
- Algorithm：「Initialize the system to the uniform superposition over all states」「Perform the following "Grover iteration" r(N) times: Apply the operator U_ω; Apply the ''Grover diffusion'' operator U_s = 2|s⟩⟨s| − I」「Measure the resulting quantum state in the computational basis.」
- 「The operator U_s = 2|s⟩⟨s| − I is a reflection through |s⟩.」
- 由定義推得（本課自行推導，非原文）：|s⟩ 的每個分量是 1/√N，所以 (2|s⟩⟨s| − I) 作用在振幅 a 上，第 i 個分量 = 2·(Σa/√N)·(1/√N) − aᵢ = 2 × 平均 − aᵢ，即「對平均值翻轉」。

## 學程內部簡報：slides/output/basic-circuits.pptx

課綱寫 p23–24，頁碼無誤（p25 是「3 顆位元：轉太多會轉過頭」，留給 Q122）。
- 第 23 頁「範例 8｜Grover：把答案的機率放大」：「① H：均勻疊加　4 個答案各 25%　每個振幅都是 ½；直接量測只有 ¼ 的機會猜中」「② 標記（Oracle）　CZ：|11⟩ 變號　Oracle 認得答案 |11⟩，只把它的振幅變成負的；機率不變」「③ 擴散　新振幅 = 2 × 平均 − a　H、X、CZ、X、H：每個振幅對平均值翻轉，答案變成 100%」「答案是別的值時，Oracle 先用 X 把答案變成 11，做 CZ 之後再用 X 還原」。
- 第 24 頁「振幅逐步看：對平均值翻轉」：「2 顆位元、答案是 |11⟩；擴散的規則：新振幅 = 2 × 平均 − 舊振幅」「四個都是 ½，平均 = ½」「答案變號；平均降到 ¼」「2 × ¼ − ½ = 0；2 × ¼ − (−½) = 1 → 100%」「比平均高的翻下來、比平均低的翻上去：被標記成負的答案離平均最遠，翻得最高」。
  備註：「補充一點：用 H、X、CZ、X、H 實際接出來的電路會多一個整體負號，在 Qiskit 裡答案的振幅會是負 1，但這個整體負號量不到，機率一樣是 100%。」

## 學程文件：docs/超導量子電腦師生對話教學紀錄.md 第 8 課

- 步驟表「步驟 3　擴散：　平均 = ¼；新振幅 = 2×平均 − 原振幅」。
- 「oracle 把答案「挖成洞」；擴散以平均值為鏡子翻過去，最深的那個翻成最高。」
- 擴散「H⊗H → X⊗X → **CZ** → X⊗X → H⊗H」「「對 |00⟩ 翻號」夾 H 就是「對平均翻轉」」。
- 「**「oracle 已經知道答案，不是作弊嗎？」** 重點是**認出答案比找出答案容易**——像數獨，驗證容易、填出來難。真正的 oracle 是「檢查條件的電路」，寫的人不需要知道答案。」

## 互動動畫原始碼

- `animations/basic-circuits.html` Grover 場景：`opts: [{ key: "n", label: "位元數", def: "2", … }, { key: "t2", label: "答案（q1 q0，點一下切換）", def: "11", bits: 2 }, …, { key: "k", label: "重複輪數", def: "best", choices: [["best", "最佳"], ["1", "1 輪"], ["2", "2 輪"], ["3", "3 輪"]] }]`；
  標記 cap「機率還沒變，答案仍是 …；但看綠色虛線，平均值被拉低到 …」；擴散 cap「擴散把每個振幅對平均值翻轉：a → 2 × 平均 − a。… 答案的振幅離平均最遠，翻過去後變得最大」；`meanLine: true`；圖例「平均值」（`border-top:2px dashed var(--hit)`，--hit 為綠色 #2C8A55／#5DCB8C）；`--pos` 藍、`--neg` 橘；
  `verdict: key => (key === t ? "→ 找到答案 ✓" : "→ 不是答案 ✗")`；頁尾「Grover 的擴散步驟照理想的「對平均值翻轉」計算；用 H、X、多控制 Z 組成的實際電路會多一個整體負號，機率完全相同」。
- `animations/transmon-3d.html` 第 7 章：第 2 步 body「**古典做法**最壞要檢查 3 次、平均 2.25 次；**Grover** 只查詢 1 次就能 100% 找到」；第 4 步 cue「金色橫線是四個振幅的平均」；
  第 8 步「自由實驗」控制項 `data-ans="0…3"`、`data-op="H0"`「H₁」、`"H1"`「H₂」、`"O"`「Oracle」、`"D"`「擴散」、`#g7meas`「量測 50 次」；`if (kind === "D") { … S.showMean = true; … }`；`meanTag.el.textContent = \`平均 ${mean >= 0 ? "+" : "−"}${Math.abs(mean).toFixed(2)}\``；`DUR = { H: 1.0, …, O: 1.0, D: 2.4 }`、擴散 `lead = 0.7`（先讓平均線出現）；負振幅 `RED`、正振幅 `COL.gold`。
- `animations/js/operation/09_grover.js`：`let n = 4, … mark = 11`；`ui.slider('量子位元數 n', 2, 6, …)`、`ui.slider('答案（標記的項目）', 0, 63, …)`；`ui.button('② Oracle', …)`、`ui.button('③ 擴散', …)`、`ui.button('完整一輪', …)`；
  `push = … (i) => (amp[i] >= 0 ? 0xe0a54a : 0x4f8cff)`；`meanPlane … color: 0xff6bd5, transparent: true, opacity: 0.25`；`meanPlane.visible = phase === 'oracle'`；讀數「（已做 Oracle，粉紅面 = 平均振幅）」「答案的機率 P = ${ps.toFixed(3)}」。

## Playwright 實拍紀錄（1600×900，nice -n 19，單張截圖）

- bc#grover 點答案的 q1 格 → 「q1=0 q0=1」；起點 `+1.000 0 0 0`（title「平均值 +.250」）；第 1 步 `+.500 +.500 +.500 +.500`（平均 +.500）；第 2 步 `+.500 −.500 +.500 +.500`（平均 +.250）；第 3 步 `0 +1.000 0 0`（平均 +.250）；量 1,000 次「→ 找到答案 ✓」、01 1000（100.0%）。
- tr#grover 第 8 步、答案 00：H₁ H₂ 後四根「+0.50 ・ 25%」；先按擴散：「平均 +0.50」金線貼柱頂、四根不變；Oracle：|00⟩「−0.50 ・ 25%」紅色、「平均 +0.25」；擴散：|00⟩「+1.00 ・ 100%」；量測 50 次：00 有 50 次。
- op#grover 答案滑桿 6：Oracle → P = 0.063（已做 Oracle，粉紅面 = 平均振幅）；擴散 → P = 0.473、其他每個 0.0352；Oracle → 答案柱深到下方；擴散 → P = 0.908、其他每個 0.0061。

## 程式實跑（課堂教材 classroom.py 內嵌全文）

- `grover_mean.py`（Python 3.13.18，只用標準函式庫，沒有亂數）與 `qiskit_check.py`（Qiskit 2.6.2，Statevector 與 StatevectorSampler seed=2026）輸出全文見 `classroom.py` 的 RUN_OUTPUT、QISKIT_OUTPUT；建置時會再跑一次 grover_mean.py 比對。
