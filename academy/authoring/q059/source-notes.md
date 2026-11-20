# Q059 來源筆記（逐字引文）

查核日：2026-11-18。維基百科頁面由製作代理以 `index.php?action=raw` 取得 wikitext（存於 `/home/user/qwork/q059wiki/`，未記 oldid）。學程內部簡報與動畫程式由製作代理讀取。

## Standard error（Wikipedia）

- 「the standard error of the mean equals the standard deviation divided by the square root of the sample size」
- 「due to the factor 1/√n, reducing the error on the estimate by a factor of two requires acquiring four times as many observations in the sample; reducing it by a factor of ten requires a hundred times as many observations.」

## Binomial distribution（Wikipedia）

- 資訊框與內文：「Var(X) = npq = np(1 − p)」（除以 n² 得比例 X/n 的變異數 p(1 − p)/n，開根號即 σ = √(p(1−p)/n)）。

## Confusion matrix（Wikipedia）

- 「Each row of the matrix represents the instances in an actual class while each column represents the instances in a predicted class, or vice versa – both variants are found in the literature.」
- 「The diagonal of the matrix therefore represents all instances that are correctly predicted.」
- 「The name stems from the fact that it makes it easy to identify whether the system is confusing two classes」

## 學程內部簡報：slides/QC_Operation_Talk.pptx

- 第 32 頁「shots 與統計誤差」：「σ(P̂) = √(P(1−P)/N)」「期望值 ⟨Z⟩ 的誤差 ≈ 2σ」「只要看哪個結果最常出現：數百～數千」「估計機率到 ±1%：~2,500」「估計期望值到 ±0.01：~10,000」「錯誤緩解會再放大所需 shots」「精度 ×10 → shots ×100」。
  講者備註：「估計一個機率的標準誤差是根號 P(1−P)/N，P 等於 0.5 時最大。圖上可以看到：100 shots 誤差約 5%，1000 shots 約 1.6%，一萬 shots 約 0.5%，十萬 shots 約 0.16%。」
- 第 33 頁「讀取誤差與緩解」：「兩團 IQ 雲重疊：SNR 不足」「讀取期間 |1⟩ 衰減成 |0⟩：T₁」「pmeas = M · ptrue」「M = [[P(0|0), P(0|1)], [P(1|0), P(1|1)]]」「→ ptrue ≈ M−1 · pmeas」「先跑校準線路：準備 0、1，量出混淆矩陣 M」「把量測到的分佈乘上 M 的反矩陣（或最小平方）」「n 位元的完整 M 是 2ⁿ × 2ⁿ → 實務上假設各位元獨立或用 M3、TREX」「開關「讀取誤差緩解」→ 估計值回到理想值附近」。
  講者備註：「讀取本身也會出錯，典型的讀取錯誤率是百分之零點五到三，比單位元閘錯誤還高。」「M 的元素就是「準備 j 量到 i」的機率。量測到的分佈等於 M 乘上真正的分佈，所以只要乘上 M 的反矩陣就能還原。」

## 互動動畫程式

- operation.html 場景 1（js/operation/01_qubit.js）：desc「誤差約 √(p(1−p)/N)，要精度提高 10 倍就要 100 倍的 shots」（第 8 行）；「一次跑 1000 shots」第 54 行；預設按鈕「|+⟩」第 57 行；小圖「估計值 P̂(1) 隨 shots 數收斂（灰帶 = ±1σ）」第 60 行；讀數「估計 P̂(1) = … ± …（1σ）」第 97–100 行。
- operation.html 場景 7（js/operation/07_readout.js）：desc「讀取誤差緩解：先量好「混淆矩陣」（準備 0 量到 1 的機率、準備 1 量到 0 的機率），再把結果反推回去。」（第 9 行）；混淆矩陣計算第 56–62 行；滑桿「準備狀態 θ」第 78 行、「兩團雲的間距（色散位移/放大器）」第 81 行；開關「讀取誤差緩解」第 87 行；緩解公式第 110 行；讀數第 113–116 行。
- index.html 場景 10（js/scenes/10_iq.js）：desc「T1 衰減會讓 |1⟩ 在讀取途中掉到 |0⟩，形成兩團之間的「拖尾」」「讀取保真度 F = 1 − [P(0|1) + P(1|0)] / 2」；開關「包含讀取期間的 T1 衰減」第 46 行；滑桿「每秒量測次數（動畫）」第 48 行；點顏色依製備狀態第 74 行；讀數第 110 行。

## 數值重算

`/home/user/qwork/q059calc/checks.py`（輸出 `checks.out`）、`qiskit_readout.py`（輸出 `qiskit.out`，用 `/home/user/qwork/q057venv`）；動畫截圖 `/home/user/qwork/q059shots/*.png`（`shot.js`、`sim.js`）。
