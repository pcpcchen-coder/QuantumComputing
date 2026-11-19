# Q125 來源筆記（逐字引文）

查核日：2026-11-19（檔頭 CHECKED 依派工統一寫 2026-11-18）。維基百科頁面由製作代理直接讀取原始 wikitext（action=raw，2026-11-19），revision id 未取得。學程內部簡報（讀出實際頁碼與文字）與動畫程式由製作代理讀取，畫面以 Playwright 單張截圖確認（nice -n 19，未錄影）。程式由製作代理實際執行。

## Law of large numbers（Wikipedia，2026-11-19 raw wikitext）

- 「In probability theory, the '''law of large numbers''' is a mathematical law which states that the average of the results obtained from a large number of independent random samples converges to the true value, if it exists.」
- 「Importantly, the law applies (as the name indicates) only when a ''large number'' of observations are considered. There is no principle that a small number of observations will coincide with the expected value or that a streak of one value will immediately be "balanced" by the others (see: Gambler's fallacy).」

## Binomial proportion confidence interval（Wikipedia，2026-11-19 raw wikitext）

- 「The analytic formula for a binomial sample standard deviation is σₙ = √( p (1 − p) / n ).」（原文為 `<math> \sigma_n = \sqrt{\frac{ p \left( 1 - p \right) }{n} }</math>`）
- 「The '''standard error''' of p̂ is the square root of this quantity. … For otherwise unweighted data … The SE becomes √( (1/n) p̂ (1 − p̂) ), leading to the familiar formulas」

## 68–95–99.7 rule（Wikipedia，2026-11-19 raw wikitext）

- 「approximately 68%, 95%, and 99.7% of the values lie within one, two, and three standard deviations of the mean, respectively.」
- 圖說：「Shown percentages are rounded theoretical probabilities intended only to approximate the empirical data derived from a normal population.」

## 學程簡報：如何操作量子電腦（slides/QC_Operation_Talk.pptx）

- 第 32 頁「shots 與統計誤差」：「σ(P̂) = √(P(1−P)/N)」「期望值 ⟨Z⟩ 的誤差 ≈ 2σ」「設定 shots 的經驗法則」「只要看哪個結果最常出現：數百～數千」「估計機率到 ±1%：~2,500」
  「估計期望值到 ±0.01：~10,000」「錯誤緩解會再放大所需 shots」「精度 ×10 → shots ×100」「：統計誤差是量子計算真正的『讀取成本』，也是比較量子與古典效率時必須算進去的部分」。課綱寫 p32，內容確實在第 32 頁。
- 第 30 頁「一個 shot 的讀取流程」（▶ 3D 場景 7：讀取與統計）：「解調、積分後成為 IQ 平面上的一個點」「多個 shot 形成兩團雲：|0⟩ 雲與 |1⟩ 雲」「在 FPGA 中用閾值（或線性判別）即時判成位元」。
- 第 33 頁「讀取誤差與緩解」：「兩團 IQ 雲重疊：SNR 不足」「讀取期間 |1⟩ 衰減成 |0⟩：T₁」「讀取誤差緩解」「先跑校準線路：準備 0、1，量出混淆矩陣 M」
  「3D 場景 7 可以試」「縮短積分時間 → 雲變胖、重疊增加」「開關『讀取誤差緩解』→ 估計值回到理想值附近」。

## 學程簡報：量子電路入門：八個範例（slides/output/basic-circuits.pptx）

- 第 28 頁「互動動畫：逐步播放、自己量測」：「右下可以量測 1 次或 1,000 次：灰底是理論機率、綠色是實際次數」。

## 學程動畫：animations/basic-circuits.html

- 量測卡：「每次量測只會得到一個結果，狀態也就此塌縮。要重複很多次，才看得出機率分布。灰色底是理論機率，綠色是實際次數。」按鈕 `#m1`「量測 1 次」、`#m1000`「量測 1,000 次」、`#mClear`「清除」；「最近一次：」`#chip`／「尚未量測」。
- `sample(th)`：每次用 `Math.random()` 照 `theory()`（目前步驟的邊際機率）抽一個結果；`addShots(m)` 累加 `counts`、`total`。
- `#m1000`：`setInterval` 每 30 ms 加 40 次，直到 1000 次（`if (shotTimer) return;`：跑的時候再按會被忽略）。
- `histRender()`：每列 `次數（百分比 .toFixed(1)）`，灰色 `.exp` 寬度 = 理論機率、綠色 `.got` 寬度 = 實際比例；最後一行「共 N 次；理論：key p、…」。
- `showLast(key)`：量一顆時綠框寫 `q2 = 0` 形式，量多顆時是整串；`#verdict` 只在最後一步顯示（BV：「→ 密碼 s = 101」）。
- `go()` 內呼叫 `clearShots()`：換步驟、換選項（rebuild(false)）、換範例（rebuild(true)）都會歸零；`#dots` 每個點對應一步（最後一個 = 最後一步）。
- Playwright 截圖紀錄（scratchpad q125/shot1.js）：#ghz 最後一步量測卡只有 000、111 兩列，「共 4 次；理論：000 50%、111 50%」；#bv 最後一步量 1 次 → 「101」「→ 密碼 s = 101」「101 1（100.0%）」；
  #teleport 最後一步「理論：0 75%、1 25%」，量 1 次 × 8 後再量 1,000 次 × 3：「共 1,008 次」「共 2,008 次」「共 3,008 次」。

## 學程動畫：animations/operation.html#readout（js/operation/07_readout.js）

- 標題「讀取：從微波訊號到 0/1，再到期望值」；說明「每一個 shot：送出讀取脈衝 … 得到 IQ 平面上的一個點，再用閾值判成 0 或 1」「誤差來源：兩團雲重疊（SNR 不足）、讀取期間 |1⟩ 衰減成 |0⟩（T₁）」
  「讀取誤差緩解：先量好『混淆矩陣』…再把結果反推回去」。
- 預設：`th = 70`、`basis = 'Z'`、`tau = 1.0`、`auto = true`、`rate = 60`、`mitig = true`、`t1on = true`；點的顏色 `m ? [1, 0.36, 0.38] : [0.31, 0.55, 1]`（判成 1 紅、判成 0 藍）。
- 控制項：滑桿「準備狀態 θ」「積分時間 τ」（0.1–4 μs）「兩團雲的間距（色散位移/放大器）」「判別閾值位置」；按鈕「清除」；開關「連續 shots」「讀取期間 T₁ 衰減（T₁ = 50 μs）」「讀取誤差緩解」。改滑桿都會 `clear()`。
- 面板（實際讀出）：「量測基底：Z　理想 P(1) = 0.329」；τ = 1.00 μs「混淆矩陣：P(1|0) = 3.5%，P(0|1) = 4.4%，讀取保真度 F = 96.1%」；τ = 0.10 μs「P(1|0) = 28.3%，P(0|1) = 28.3%，讀取保真度 F = 71.7%」；
  開關關閉時第四行「未緩解 P̂(1) = …」，打開時「緩解後 P̂(1) = …」。左側 #panel 要捲到底，readout 才入鏡。
- 01_qubit.js 說明：「所以『讀取』一個量子程式要重複執行很多次（shots），用統計估計機率；誤差約 √(p(1−p)/N)，要精度提高 10 倍就要 100 倍的 shots。」

## 製作代理實跑紀錄

- shots_lab.py（Python 3.13.18，只用標準函式庫，random.Random(1125)）輸出全文見 classroom.py 的 RUN_OUTPUT。
- qiskit_shots.py（Qiskit 2.6.2，StatevectorSampler seed=1125）輸出全文見 classroom.py 的 QISKIT_OUTPUT。
- 625 次一半一半、落在 ±2%（300–325 次）以內的二項分布精確機率：0.663（Python math.comb 計算）。
- 讀取場景未緩解估計的期望：Node 以 07_readout.js 同一段 shot() 邏輯蒙地卡羅（τ = 0.1、θ = 70°、2000 輪 × 300 次）：平均 0.426，第 1 百分位 0.360、第 99 百分位 0.490；τ = 1.0 時平均 0.339。
