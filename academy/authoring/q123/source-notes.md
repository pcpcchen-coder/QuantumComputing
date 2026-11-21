# Q123 來源筆記（逐字引文）

查核日：2026-11-19（檔頭 CHECKED 依派工統一寫 2026-11-18）。維基百科頁面由製作代理直接讀取原始 wikitext（action=raw），revision id 由 MediaWiki API（prop=revisions）或頁面歷史取得。學程內部簡報（讀出實際頁碼、文字與備註）與動畫程式由製作代理讀取，畫面以 Playwright 單張截圖確認。程式由製作代理實際執行。

## Deutsch–Jozsa algorithm（Wikipedia，oldid=1381683602）

- 「The Deutsch–Jozsa problem is specifically designed to be easy for a quantum algorithm and hard for any deterministic classical algorithm. It is a black box problem that can be solved efficiently by a quantum computer with no error, whereas a deterministic classical computer would need an exponential number of queries to the black box to solve the problem.」
- 「Although of little practical use, it is one of the first examples of a quantum algorithm that is exponentially faster than any possible deterministic classical algorithm.」
- Classical solution：「For a conventional deterministic algorithm where n is the number of bits, 2^{n-1} + 1 evaluations of f will be required in the worst case. To prove that f is constant, just over half the set of inputs must be evaluated and their outputs found to be identical (because the function is guaranteed to be either balanced or constant, not somewhere in between).」
- 「For a conventional randomized algorithm, a constant k evaluations of the function suffices to produce the correct answer with a high probability … However, k = 2^{n-1} + 1 evaluations are still required if we want an answer that has no possibility of error. The Deutsch-Jozsa quantum algorithm produces an answer that is always correct with a single evaluation of f.」
- 「Since the problem is easy to solve on a probabilistic classical computer, it does not yield an oracle separation with BPP」。

## Bernstein–Vazirani algorithm（Wikipedia，oldid=1371471620）

- Problem statement：「f(x) is promised to be the dot product between x and a secret string s ∈ {0,1}^n modulo 2, f(x) = x · s = x₁s₁ ⊕ x₂s₂ ⊕ ⋯ ⊕ xₙsₙ, find s.」
- 「Classically, the most efficient method to find the secret string is by evaluating the function n times with the input values x = 2^i for all i ∈ {0, 1, …, n−1}」
- 「In contrast to the classical solution which needs at least n queries of the function to find s, only one query is needed using quantum computing.」
- 「it is an example of a problem solvable by a Quantum Turing machine (QTM) with O(1) queries to the problem's oracle, but for which any Probabilistic Turing machine (PTM) algorithm must make Ω(n) queries.」

## Grover's algorithm（Wikipedia，oldid=1385418712）

- 「The analogous problem in classical computation would have a query complexity O(N) (i.e., the function would have to be evaluated O(N) times: there is no better approach than trying out all input values one after the other, which, on average, takes N/2 steps).」
- 「Charles H. Bennett, Ethan Bernstein, Gilles Brassard, and Umesh Vazirani proved that any quantum solution to the problem needs to evaluate the function Ω(√N) times, so Grover's algorithm is asymptotically optimal.」
- 「Unlike other quantum algorithms, which may provide exponential speedup over their classical counterparts, Grover's algorithm provides only a quadratic speedup.」
- 「The major barrier to instantiating a speedup from Grover's algorithm is that the quadratic speedup achieved is too modest to overcome the large overhead of near-term quantum computers.」

## Shor's algorithm（Wikipedia，oldid=1384103273）

- 「On a quantum computer, to factor an integer n, Shor's algorithm runs in polynomial time, meaning the time taken is polynomial in log n.」
- 「Shor's algorithm is asymptotically faster than the most scalable classical factoring algorithm, the general number field sieve, which works in sub-exponential time.」
- 「no classical algorithm is known that can factor integers in polynomial time.」

## 學程內部簡報：slides/output/basic-circuits.pptx

課綱寫 p30，頁碼無誤。
- 第 30 頁「古典 vs 量子：要查幾次？」表格（問題｜黑盒回答什麼｜古典最少查詢｜量子查詢｜量子用到的技巧）：
  「Deutsch｜f(x)，x 是 1 個位元｜2 次｜1 次｜相位回踢 + 干涉」「Deutsch–Jozsa（n 位元）｜f(x)，保證常數或平衡｜最壞 2ⁿ⁻¹ + 1 次｜1 次｜同上，輸入改成 n 顆」
  「Bernstein–Vazirani｜s·x（mod 2）｜n 次（每次問一位）｜1 次｜同上，答案寫在每一位的相位」「Grover 搜尋｜x 是不是答案｜平均約 N/2 次｜約 (π/4)√N 輪｜標記 + 擴散，重複約 √N 輪」；
  頁尾「前三個是同一個套路：疊加 → 黑盒把答案寫進正負號 → H 干涉；Grover 則要重複約 √N 輪」。
  備註：「Bernstein–Vazirani 古典可以每次只問一位，用 001、010、100 去問，需要 n 次；量子 1 次就讀出整串 … Grover 的黑盒一次只能把答案標記一點點，所以要重複大約根號 N 輪，是平方加速。要提醒的是，這些是黑盒查詢次數的比較，是展示量子加速原理的教學範例，還不是實用的應用。」
- 第 26 頁「搜尋範圍變大：√N 的威力」：「8（3 顆）4.5 次 2 輪 94.5%」「1,024（10 顆）512.5 次 25 輪 99.9%」；備註「古典隨機一個一個試，平均要試 N 加 1 除以 2 次」。

## 學程內部簡報：slides/QC_Operation_Talk.pptx

課綱寫 p42，頁碼無誤。
- 第 42 頁「快在哪？加速的等級」表格：「質因數分解 / 離散對數｜exp(O(n1/3(log n)2/3))｜O(n³) 左右｜超多項式（指數級）」「量子系統模擬｜一般為指數｜多項式｜指數級（多數情況）」「無結構搜尋｜O(N)｜O(√N)｜平方」「蒙地卡羅估計｜O(1/ε²)｜O(1/ε)｜平方」；
  「平方加速：差距是 N 和 √N，好處要在 N 很大時才顯現，而且容易被量子閘較慢、錯誤更正的開銷吃掉」「實際比較要算總時間：shots、錯誤更正、資料載入」。
  備註：「質因數分解，古典最好的一般數域篩法是次指數時間，Shor 是多項式時間 … 平方加速則要小心：量子閘比古典運算慢很多，加上錯誤更正的額外開銷，平方加速要在問題非常大時才能真正勝出」。
- 第 45 頁「哪些事不會變快」：「把 N 筆資料載入量子態通常要 ~N 步」「n 個量子位元只能讀出 n 位元」「加減乘除、排序、資料庫查詢、渲染、文書：沒有已知的量子加速」「量子閘 ~100 ns、錯誤更正開銷大；問題不夠大時古典更快」「結論：最適合量子電腦的問題是『輸入小、計算難、輸出小』」；備註「分解質因數就是完美的例子：輸入是一個數字，輸出是兩個數字，中間的計算極難」。
- 第 40 頁：「平方加速：N = 10⁶ 時，古典平均 50 萬次，Grover ~785 次」；備註「N = 64 時 … 6 次就到 99.7%」。
- 第 39 頁：「古典：最壞要查 2ⁿ⁻¹ + 1 次才能確定」「Bernstein–Vazirani：1 次查詢讀出 n 位元的秘密字串（古典要 n 次）」。

## 互動動畫原始碼

- `animations/js/operation/08_interference.js`：`ui.radio([['A', '單一量子位元：兩條路徑'], ['B', '3 位元：8 條路徑（Deutsch–Jozsa）']], …)`；`FN = { c0: ['常數 f = 0', …], c1: ['常數 f = 1', …], b0: ['平衡 f = x₀', (x) => x & 1], bp: ['平衡 f = 奇偶', …], rnd: ['隨機（非保證）', null] }`、`let fkey = 'b0'`；
  readout `函數：${FN[fkey][0]}　f(x) = 1 的有 ${ones} 個<br>|000⟩ 的振幅 = (1/8)·Σ(−1)^f(x) = ${sx.toFixed(3)}　→　P(000) = ${P0.toFixed(3)}<br>` + `'<b>常數函數：完全相長</b>' : … '<b>平衡函數：完全相消</b>'` + `'　（古典最壞要查 2ⁿ⁻¹+1 = 5 次）'`。
- `animations/transmon-3d.html` 第 9 章：`classicalQuery()`「依序問 100、010、001」、看板文字 `古典第 ${S.cQ} 次：x = ${bits3(x)} → 回答 ${ans}（所以 s 的第 ${k + 1} 位是 ${ans}）`、`古典問了 3 次才知道 s = ${bits3(S.s)}`；
  步驟 1 cues `[0.3, "黑盒子藏著 3 位元密碼 s（這裡是 101）。你丟一個 x 給它，它只回答 s·x 的奇偶 …"]`、`[7.5, "古典做法：先問 x = 100 …"]`、`[12.5, "再問 x = 010，回答 0 → 第 2 位是 0。"]`、`[16.5, "最後問 x = 001，回答 1 → 第 3 位是 1。古典要問 3 次；n 位元密碼就要 n 次。"]`；
  步驟 5 cues `[0.3, … g9Push({ t: "M", n: 50, col: 3 })]`、`[6.5, "古典要問 3 次；n 位元密碼古典要 n 次，量子永遠只要 1 次。", () => { g9S.math = ["量子：查詢 1 次 → s = 101", "古典：查詢 3 次（n 位元要 n 次）"]; }]`；看板虛線框 `黑盒子 s = ${bits3(col.s)}`；`#g9play`、`#g9auto`。
- `animations/js/operation/09_grover.js`：`ui.slider('量子位元數 n', 2, 6, 1, n, …)`、`kOpt = () => Math.max(1, Math.round(Math.PI / (4 * theta()) - 0.5))`、readout `最佳輪數 ≈ (π/4)√N ≈ ${kOpt()}　古典平均要查 ${(N / 2).toFixed(0)} 次`；
  `ui.button('自動跑到最佳次數', () => { setup(); autoRun = true; acc = 0; }, r2)`、`if (acc > 0.8) { … if (phase !== 'oracle') oracle(); else { diffuse(); if (k >= kOpt()) autoRun = false; } }`；`meanPlane.visible = phase === 'oracle'`（粉紅 0xff6bd5）；白點 `j === k ? '#fff'`。

## Playwright 實拍紀錄（1600×900，nice -n 19，單張截圖）

- op#interference 模式 B：「函數：平衡 f = x₀　f(x) = 1 的有 4 個 / … = 0.000　→　P(000) = 0.000 / 平衡函數：完全相消　（古典最壞要查 2ⁿ⁻¹+1 = 5 次）」；常數 f = 0「有 0 個 … 1.000 → P(000) = 1.000 / 常數函數：完全相長」；常數 f = 1「有 8 個 … -1.000 → P(000) = 1.000」；平衡 f = 奇偶「有 4 個 … P(000) = 0.000」。
- tr#bv：取消自動接續、步驟 1、暫停 3 秒後播放：播放後 9 秒「古典 1 次」、14 秒「古典 2 次」、18.5 秒「古典 3 次」，看板四行「古典第 1 次 … 古典問了 3 次才知道 s = 101」；步驟 5：101（50/50）、看板「量子：查詢 1 次 → s = 101」「古典：查詢 3 次（n 位元要 n 次）」。
- op#grover：n = 2／4／6 → 「最佳輪數 ≈ … ≈ 1／3／6　古典平均要查 2／8／32 次」；n = 6 自動跑到最佳次數 P = 0.135、0.344、0.591、0.816、0.964、0.997，白點在曲線頂端。

## 程式實跑（課堂教材 classroom.py 內嵌全文）

- `query_count.py`（Python 3.13.18，只用標準函式庫，沒有亂數）與 `qiskit_check.py`（Qiskit 2.6.2，Statevector 與 StatevectorSampler seed=2026）輸出全文見 `classroom.py` 的 RUN_OUTPUT、QISKIT_OUTPUT；建置時會再跑一次 query_count.py 比對。
