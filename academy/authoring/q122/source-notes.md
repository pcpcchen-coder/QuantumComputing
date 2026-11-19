# Q122 來源筆記（逐字引文）

查核日：2026-11-19（檔頭 CHECKED 依派工統一寫 2026-11-18）。維基百科頁面由製作代理直接讀取原始 wikitext（action=raw），revision id 由 MediaWiki API（prop=revisions）取得。學程內部簡報（讀出實際頁碼、文字與備註）、文件與動畫程式由製作代理讀取，畫面以 Playwright 單張截圖確認。程式由製作代理實際執行。

## Grover's algorithm（Wikipedia，oldid=1385418712）

- 「'''Grover's algorithm''', also known as the '''quantum search algorithm''', is a quantum algorithm for unstructured search that finds with high probability the unique input to a black box function that produces a particular output value, using just O(√N) evaluations of the function … It was devised by Indian-American computer scientist Lov Grover in 1996.」
- 「there is no better approach than trying out all input values one after the other, which, on average, takes N/2 steps」
- 「Charles H. Bennett, Ethan Bernstein, Gilles Brassard, and Umesh Vazirani proved that any quantum solution to the problem needs to evaluate the function Ω(√N) times, so Grover's algorithm is asymptotically optimal.」
- 「Unlike other quantum algorithms, which may provide exponential speedup over their classical counterparts, Grover's algorithm provides only a quadratic speedup.」
- 「It is straightforward to check that the operator U_s U_ω of each Grover iteration step rotates the state vector by an angle of θ = 2 arcsin(1/√N).」「the angle θ/2 between |s⟩ and |s′⟩ is given by sin(θ/2) = 1/√N.」
- 「We need to stop when the state vector passes close to |ω⟩; after this, subsequent iterations rotate the state vector ''away'' from |ω⟩, reducing the probability of obtaining the correct answer. The exact probability of measuring the correct answer is sin²((r + ½)θ), where ''r'' is the (integer) number of Grover iterations. The earliest time that we get a near-optimal measurement is therefore r ≈ π√N/4.」
- Multiple matching entries：「If, instead of 1 matching entry, there are ''k'' matching entries, the same algorithm works, but the number of iterations must be (π/4)√(N/k) instead of (π/4)√N.」「There are several ways to handle the case if ''k'' is unknown.」
- 換算（本課自行推導，非原文）：維基的 θ/2 就是動畫與師生對話寫的 θ（sin θ = 1/√N）；每輪轉 2θ，r 輪後與「非答案」軸夾角 (2r + 1)θ，成功機率 sin²((2r + 1)θ)。N = 8：θ = 20.7°，每輪 41.4°。

## 學程內部簡報：slides/output/basic-circuits.pptx

課綱寫 p25–27，頁碼無誤。
- 第 25 頁「3 顆位元：轉太多會轉過頭」：「8 個可能、答案是 101；每一輪 = 標記 + 擴散」「H 之後 +0.35 …（八根）各 12.5%」「1 輪 +0.18 … +0.88（101）… 答案 78.1%」「2 輪（最佳）−0.09 … +0.97 … 答案 94.5%」「3 輪 −0.31 … +0.57 … 降到 33.0%：轉過頭了」「每一輪把狀態往答案轉一個固定角度；最佳輪數約 (π/4)√N，再轉下去機率反而下降」。
  備註：「做一輪，答案升到 78.1%；做兩輪，升到 94.5%，這是最佳輪數。如果再做第三輪，答案反而掉到 33%，其他的振幅變成負的。原因是每一輪其實是把狀態往答案的方向轉一個固定角度，轉到最接近答案的時候就要停，再轉就轉過頭了。最佳輪數大約是四分之 π 乘上根號 N。」
- 第 26 頁「搜尋範圍變大：√N 的威力」表格：「4（2 顆位元）2.5 次 1 輪 100%」「8（3 顆）4.5 次 2 輪 94.5%」「16（4 顆）8.5 次 3 輪 96.1%」「1,024（10 顆）512.5 次 25 輪 99.9%」「1,048,576（20 顆）約 52 萬次 804 輪 > 99.99%」「古典約 N/2 次、Grover 約 (π/4)√N 輪：平方加速，而且已經證明黑盒搜尋不可能更快」。
  備註：「古典隨機一個一個試，平均要試 N 加 1 除以 2 次 … N 等於 1024 的時候，古典平均要五百多次，Grover 只要 25 輪，成功機率 99.9% … 這是平方加速，不像 Shor 那樣是指數加速」。
- 第 27 頁「動畫：看平均值和輪數」：「可以選 2 或 3 顆位元、點選答案，以及重複 1–3 輪（預設是最佳輪數）」「振幅圖上的綠色虛線是平均值：標記後平均下降，擴散就是對這條線翻轉」「說明文字會算出每一步答案的機率，轉過頭時會提醒」。

## 學程文件：docs/超導量子電腦師生對話教學紀錄.md 第 8 課

- 「**擴大到 N 個**：約 (π/4)√N 次（100 萬個選項約 785 次 vs 古典平均 50 萬次），是**平方加速**。每次迭代朝答案轉 2θ（sin θ = 1/√N）；N = 4 剛好一次到 90°，N 更大時**轉過頭機率反而下降**。」
- 課後練習「3. 兩位元 Grover 做兩次迭代，結果如何？」參考答案「3. 轉過頭，四個結果回到各 25%。」

## 互動動畫原始碼

- `animations/basic-circuits.html` Grover 場景：`{ key: "n", label: "位元數", def: "2", choices: [["2", "2 顆（N = 4）"], ["3", "3 顆（N = 8）"]] }`、`{ key: "t3", label: "答案（q2 q1 q0，點一下切換）", def: "101", bits: 3, when: o => o.n === "3" }`、`{ key: "k", label: "重複輪數", def: "best", choices: [["best", "最佳"], ["1", "1 輪"], ["2", "2 輪"], ["3", "3 輪"]] }`；`best = n === 2 ? 1 : 2`；
  標記 cap「但看綠色虛線，平均值被拉低到 …」；擴散 cap 三種：「答案的振幅離平均最遠，翻過去後變得最大：答案的機率升到 …」「這次答案的振幅已經太大，平均值變成負的，翻過去反而變小：答案的機率降到 …。轉過頭了，Grover 不是越多輪越好，要停在最佳輪數。」「… 顆位元的最佳輪數是 …」。
- `animations/transmon-3d.html` 第 7 章：第 8 步「自由實驗」說明「・一鍵 Grover 後再按 Oracle、擴散：轉過頭。」；`#g7run`「一鍵 Grover」：`g7Reset` 後 H(0)、H(1)、（答案不是 11 才夾 X）、CZ、`{ t: "D", col: c, mean: true }`、`Mg(50, c)`；`g7Apply` 的 `"O"`：`a[op.w] = -a[op.w]`、`"D"`：`m = (a[0] + a[1] + a[2] + a[3]) / 4; a[i] = 2 * m - a[i]`；`DUR = { H: 1.0, …, CZ: 1.0, O: 1.0, D: 2.4 }`；負振幅 `RED`、正振幅 `COL.gold`；`meanTag` 文字 `平均 ${mean >= 0 ? "+" : "−"}${Math.abs(mean).toFixed(2)}`。
  第 6 步「⑥ 再多做一次：轉過頭了」body「翻轉後四個振幅都是 −½」與 cue「四個振幅都變成 −½」：依 `g7Apply` 實算，從 [0, 0, 1, 0] 標記再擴散得 [−½, −½, +½, −½]（答案 +½、其他 −½），文字和程式不符，本課不採用第 6 步，旁白依實算與畫面數值。
- `animations/js/operation/09_grover.js`：`ui.slider('量子位元數 n', 2, 6, …)`、`ui.slider('答案（標記的項目）', 0, 63, …)`、`ui.button('完整一輪', () => { if (phase !== 'oracle') oracle(); setTimeout(() => diffuse(), 700); })`；
  `const theta = () => Math.asin(1 / Math.sqrt(N))`、`kOpt = () => Math.max(1, Math.round(Math.PI / (4 * theta()) - 0.5))`；插圖標題「幾何圖：每輪在「答案–非答案」平面轉 2θ」、右側「P(成功) vs 輪數」：`km = Math.max(kOpt() * 2 + 1, 3)`、曲線 `Math.sin((2 * x + 1) * th) ** 2`、`P.dot(…, j === k ? 5 : 2.5, j === k ? '#fff' : '#e0a54a')`；
  說明「每一輪讓狀態在「答案 / 非答案」平面上轉 2θ（右下插圖），sin θ = 1/√N。轉太多次反而會轉過頭！」；正振幅 0xe0a54a（金）、負振幅 0x4f8cff（藍）。

## Playwright 實拍紀錄（1600×900，nice -n 19，單張截圖）

- bc#grover：位元數按「3 顆（N = 8）」→ 答案「q2=1 q1=0 q0=1」；點 q2 → 「q2=0 q1=0 q0=1」；按「3 輪」→ 步驟 7 / 7。起點 `+1.000 0 …`；第 1 步八根 `+.354`（12.5%）；第 2 步 `−.354`、平均 `+.265`；第 3 步答案 `+.884`、其他 `+.177`、「升到 78.1%」；第 4 步 `−.884`、平均 `+.044`；第 5 步 `+.972`、其他 `−.088`、「升到 94.5%」；第 6 步 `−.972`、其他 `−.088`、平均 `−.199`；第 7 步 `+.575`、其他 `−.309`、「平均值變成負的，翻過去反而變小：答案的機率降到 33%。轉過頭了…」。
- tr#grover 第 8 步、答案 11：一鍵 Grover 後 `+0.00 ・ 0%`×3、`+1.00 ・ 100%`、「平均 +0.25」、量測 11 有 50 次；Oracle `−1.00`、「平均 −0.25」；擴散 `−0.50 ・ 25%`×3、`+0.50 ・ 25%`；Oracle 四根 `−0.50`、「平均 −0.50」；擴散不變；Oracle `+0.50`、「平均 −0.25」；擴散 `−1.00 ・ 100%`。
- op#grover：n 拉到 3 → 「N = 8，第 0 輪 / 答案的機率 P = 0.125 … 最佳輪數 ≈ (π/4)√N ≈ 2　古典平均要查 4 次」；完整一輪 ×5：P = 0.781、0.945、0.330、0.012、0.548；第 4 輪八根全藍、白點在曲線谷底。

## 程式實跑（課堂教材 classroom.py 內嵌全文）

- `grover_rounds.py`（Python 3.13.18，只用標準函式庫，沒有亂數）與 `qiskit_check.py`（Qiskit 2.6.2，Statevector 與 StatevectorSampler seed=2026）輸出全文見 `classroom.py` 的 RUN_OUTPUT、QISKIT_OUTPUT；建置時會再跑一次 grover_rounds.py 比對。
