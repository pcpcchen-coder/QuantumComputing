# Q062 來源筆記（逐字引文）

查核日：2026-11-18。維基百科頁面由製作代理以 `index.php?action=raw` 取得 wikitext（存於 `/home/user/qwork/q062wiki/shor.txt`；API 查得 revid 1384103273，2026-11-06）。學程內部簡報、對話紀錄與動畫程式由製作代理讀取。

## Shor's algorithm（Wikipedia）

- 「Shor's algorithm is a quantum algorithm for finding the prime factors of an integer. It was developed in 1994 by the American mathematician Peter Shor.」
- 「However, beating classical computers may require quantum computers with millions of qubits due to the overhead caused by quantum error correction.」
- 「On a quantum computer, to factor an integer n, Shor's algorithm runs in polynomial time…」「Shor's algorithm is asymptotically faster than the most scalable classical factoring algorithm, the general number field sieve, which works in sub-exponential time.」
- 「RSA can be broken if factoring large integers is computationally feasible. As far as is known, this is not possible using classical (non-quantum) computers」
- 「Shor's algorithm consists of two parts: A classical reduction of the factoring problem to the problem of order-finding… A quantum algorithm to solve the order-finding problem.」
- 「using Euclid's algorithm, we can always compute the GCD between two integers efficiently.」
- 「N ∣ (a^{r/2} − 1)(a^{r/2} + 1)… the algorithm doesn't work for odd r… meaning that the algorithm would have to restart with a new a」
- 「If d = 1, then N ∣ a^{r/2} + 1 was true, and a nontrivial factor of N cannot be achieved from a, and the algorithm must restart with a new a.」
- 「Use the continued fractions algorithm to extract the period r from the measurement outcomes obtained in the previous stage. This is a procedure to post-process (with a classical computer)…」
- 「In 2001, Shor's algorithm was demonstrated by a group at IBM, who factored 15 into 3 × 5, using an NMR implementation of a quantum computer with seven qubits.」「Later, in 2012, the factorization of 21 was achieved.」
- 「However, none of these demonstrations fulfill the requirements of Shor's algorithm: they compile the circuit using prior knowledge of the solution…」
- 「The runtime bottleneck of Shor's algorithm is quantum modular exponentiation, which is by far slower than the quantum Fourier transform and classical pre-/post-processing.」

## 學程內部簡報

- slides/QC_Operation_Talk.pptx 第 41 頁「Shor 演算法：用干涉找週期」：表格「① H⊗⁶｜x = 0…63 均勻疊加」「② 模指數｜計算 f(x) = 7ˣ mod 15 = 1, 7, 4, 13, 1, …（週期 4）」「③ 量測 f｜只留下 f(x) 相同的 x：間隔 = r」「④ QFT｜週期 r → 頻率峰值 64k/r（其他位置干涉抵消）」「⑤ 量測 + 古典｜y/64 ≈ k/r → 連分數得 r = 4」；圖說「④ QFT 後：峰值在 64k/r = 0、16、32、48」；「7^{4/2} = 49 ≡ 4 (mod 15)／gcd(4 − 1, 15) = 3，gcd(4 + 1, 15) = 5／→ 15 = 3 × 5」。
  講者備註：「選一個和 N 互質的 a，函數 f(x) = a 的 x 次方 mod N 是週期函數…只要 r 是偶數，a 的 r/2 次方加減 1 和 N 的最大公因數，通常就是 N 的因數。」「第三步，量測第二個暫存器，x 暫存器只剩下 f(x) 相同的那些 x，間隔正好是週期，像一把梳子」「按「下一步」逐步執行，可以換 a，也可以試 N = 21。右下插圖是 f(x) 的週期圖形。」
- slides/transmon.pptx 第 22 頁「Shor 演算法：用 QFT 找週期，分解 15」（課綱寫第 23 頁，實為 BV 密碼頁）。

## 對話教學紀錄 第 10 課 Shor 演算法（docs/超導量子電腦師生對話教學紀錄.md）

- 「r = 4；7² ≡ 4；gcd(3, 15) = 3、gcd(5, 15) = 5。若 r 為奇數或 a^(r/2) ≡ −1（例如 a = 14）就換 a，成功率至少一半。古典找不到 r：2048 位元時 r 可大到 2²⁰⁴⁸ 量級，序列看起來完全隨機。」
- 「分解 15、21 的實驗多半是事先簡化的 compiled Shor。」

## 互動動畫程式

- operation.html 場景 10 shor（js/operation/10_shor.js）：desc「① x 暫存器（6 個量子位元，64 個值）做 H → 均勻疊加」「③ 量測第二個暫存器 → 只剩 f(x) 相同的那些 x：間隔正好是 r 的「梳子」」「④ 對 x 暫存器做 QFT：梳子的間隔 r 變成峰值位置 64·k/r（干涉讓其他位置抵消）」「⑤ 量測得到 y，用連分數從 y/64 ≈ k/r 推出 r，再用古典電腦算 gcd」；readout 第 110–111 行「（教學用暫存器只有 64；正式 Shor 需 Q ≥ N²，峰值會更尖）」；第 106–107 行「r 為奇數 → 換一個 a 重來」「得到平凡因數 → 換 a 重來」。
- transmon-3d.html 第 8 章 shor（G8STEPS）：「量子電腦只負責「找週期」這一段」「N 有 2048 位元時，r 可能大到 2²⁰⁴⁸ 量級，序列看起來完全隨機，古典電腦只能一個一個算」「直接量測只會隨機得到一組 (x, f(x))，看不出週期」「這一步是整個演算法最花資源的部分」「y = 0：沒有資訊，重跑」「真實的 RSA-2048 估計需要約百萬顆實體位元與錯誤更正，目前的機台還差很遠」。

## 數值重算

`/home/user/qwork/q062calc/checks.py`（輸出 `checks.out`）；`opshor.py` 照抄 10_shor.js 的機率與連分數邏輯，重現動畫段的固定亂數情境。截圖在 `/home/user/qwork/q062shots/`（1600×900 Chromium swiftshader）。
