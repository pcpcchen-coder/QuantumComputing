# Q063 來源筆記（逐字引文）

查核日：2026-11-18。維基百科頁面由製作代理以 `index.php?action=raw` 取得 wikitext（存於 `/home/user/qwork/q063wiki/`）；Shor's algorithm 的 revid 1384103273（2026-11-06）由 API 查得，另兩頁查版本號時 API 限流，未取得。學程內部簡報與動畫程式由製作代理讀取。

## Grover's algorithm（Wikipedia）

- 「…a quantum algorithm for unstructured search that finds with high probability the unique input to a black box function that produces a particular output value, using just O(√N) evaluations of the function」
- 「Unlike other quantum algorithms, which may provide exponential speedup over their classical counterparts, Grover's algorithm provides only a quadratic speedup. However, even quadratic speedup is considerable when N is large」
- 「Grover's algorithm could brute-force a 128-bit symmetric cryptographic key in roughly 2^64 iterations, or a 256-bit key in roughly 2^128 iterations.」
- 「Since classical algorithms for NP-complete problems require exponentially many steps, and Grover's algorithm provides at most a quadratic speedup over the classical solution for unstructured search, this suggests that Grover's algorithm by itself will not provide polynomial-time solutions for NP-complete problems」
- 「Reading a full database item by item and converting it into such a representation may take a lot longer than Grover's search.」
- 「The major barrier to instantiating a speedup from Grover's algorithm is that the quadratic speedup achieved is too modest to overcome the large overhead of near-term quantum computers.」
- 「The earliest time that we get a near-optimal measurement is therefore r ≈ π√N/4.」

## Quantum supremacy（Wikipedia）

- 「Google claims to have reached quantum supremacy with an array of 54 qubits out of which 53 were functional, which were used to perform a series of operations in 200 seconds that would take a supercomputer about 10,000 years to complete」（轉引 Financial Times，2019-09-20）
- 「IBM contended that the calculation Google claimed would take 10,000 years could be performed in just 2.5 days on its own Summit supercomputer if its architecture were optimized」
- 「This algorithm finds the prime factorization of an n-bit integer in Õ(n³) time whereas the best known classical algorithm requires 2^{O(n^{1/3})} time」
- 「A later tensor network-based study, however, questioned this advantage…」（D-Wave 2024 宣稱）

## Shor's algorithm（Wikipedia，revid 1384103273）

- 「On a quantum computer, to factor an integer n, Shor's algorithm runs in polynomial time…」「…asymptotically faster than the most scalable classical factoring algorithm, the general number field sieve, which works in sub-exponential time.」
- 「However, beating classical computers may require quantum computers with millions of qubits due to the overhead caused by quantum error correction.」

## 學程內部簡報 slides/QC_Operation_Talk.pptx

- 第 36 頁「常見誤解 vs 事實」：「計算確實作用在 2ⁿ 個振幅上，但量測只得到其中 1 個隨機結果；沒有干涉，等於隨機猜」「只有特定結構的問題有加速；加速幅度從平方級到指數級不等」「普遍認為不能有效解（BQP 不包含 NP-complete）；Grover 只給平方加速」。
- 第 37 頁「量子加速的三個資源」：「量子演算法的配方：疊加（展開所有可能）→ 用問題結構安排相位 → 干涉（集中到答案）→ 量測」；「沒有糾纏的線路可以被古典有效模擬」。
- 第 42 頁「快在哪？加速的等級」：表格（質因數分解／離散對數 超多項式；量子系統模擬 指數級；無結構搜尋 O(N) → O(√N) 平方；蒙地卡羅 O(1/ε²) → O(1/ε) 平方）；「平方加速…容易被量子閘較慢、錯誤更正的開銷吃掉」「實際比較要算總時間：shots、錯誤更正、資料載入」。講者備註：「古典曲線在 2048 位元時大約是 10 的 35 次方等級，量子大約是 10 的 10 次方等級——這張圖只是示意趨勢，常數都略去了」「指數級加速是質的差別」。
- 第 43 頁：「精確狀態向量：2ⁿ 個複數 × 16 bytes／~50 個量子位元就超過最大超級電腦的記憶體」「張量網路、Clifford 模擬等方法可處理低糾纏或特殊閘的線路」；講者備註「30 個量子位元要 16 GB…40 個要 16 TB；50 個要 18 PB」「優勢的邊界一直被古典演算法挑戰」。
- 第 44 頁應用地圖：「機器學習｜量子核方法、HHL 類｜未定｜資料載入是瓶頸；仍在研究」「最佳化｜QAOA、量子退火、Grover 類｜啟發式 / 平方｜實用優勢尚未確立」。
- 第 45 頁「哪些事不會變快」：「把 N 筆資料載入量子態通常要 ~N 步；沒有實用的 QRAM → 大數據分析難以加速」「n 個量子位元只能讀出 n 位元」「加減乘除、排序、資料庫查詢、渲染、文書：沒有已知的量子加速」「量子閘 ~100 ns、錯誤更正開銷大；問題不夠大時古典更快」「結論：最適合量子電腦的問題是「輸入小、計算難、輸出小」」；講者備註「分解質因數就是完美的例子：輸入是一個數字，輸出是兩個數字，中間的計算極難」。

## 互動動畫程式

- operation.html 場景 9 grover（js/operation/09_grover.js）：subtitle「古典平均 N/2 次，量子約 (π/4)√N 次」；desc「加速是平方級：N = 100 萬時，古典平均 50 萬次，Grover 約 785 次」；第 44 行滑桿「量子位元數 n」2–6；第 89–90 行讀數「最佳輪數 ≈ (π/4)√N ≈ …　古典平均要查 … 次」「測量結果：… ✓ 找到了」。
- transmon-3d.html 第 8 章 shor（G8STEPS，第 1920 行起）：③「這一步是整個演算法最花資源的部分：必須用可逆的量子加法器、乘法器組成，閘數約 n³」；⑤「只要約 n² 個閘；古典 FFT 處理 2ⁿ 個點要約 n·2ⁿ 步。指數級加速就來自這裡。」；⑥「40 次結果只會落在 0、4、8、12」。

## 數值重算

`/home/user/qwork/q063calc/checks.py`（輸出 `checks.out`）。截圖在 `/home/user/qwork/q063shots/`（1600×900 Chromium swiftshader）。
