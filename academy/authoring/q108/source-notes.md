# Q108 來源筆記（逐字引文）

查核日：2026-11-18。維基百科頁面由製作代理透過 MediaWiki 直接讀取原始 wikitext（Shor's algorithm 的 revision id 取自 API 回應；Post-quantum cryptography 頁讀取當下 API 限流，未取得 revision id）。學程內部文件、簡報與動畫程式由製作代理讀取。程式由製作代理實際執行。

## Shor's algorithm（Wikipedia，oldid=1384103273）

- 「'''Shor's algorithm''' is a [[quantum algorithm]] for finding the [[prime factor]]s of an integer. It was developed in 1994 by the American mathematician [[Peter Shor]].」
- 「However, beating classical computers may require quantum computers with millions of [[Qubit|qubits]] due to the overhead caused by [[quantum error correction]].」（引用 Gidney & Ekerå「How to factor 2048 bit RSA integers in 8 hours using 20 million noisy qubits」）
- 「On a quantum computer, to factor an integer n, Shor's algorithm runs in [[polynomial time]], meaning the time taken is polynomial in log n.」（數學式由 <math> 轉寫）
- 「Since we have factored the expression in this way, the algorithm doesn't work for odd r (because a^(r/2) must be an integer), meaning that the algorithm would have to restart with a new a.」
- 「If d = 1, then N ∣ a^(r/2) + 1 was true, and a nontrivial factor of N cannot be achieved from a, and the algorithm must restart with a new a.」
- 「Use the [[simple continued fraction|continued fractions algorithm]] to extract the period r from the measurement outcomes obtained in the previous stage. This is a procedure to post-process (with a classical computer) the measurement data」
- 「The runtime bottleneck of Shor's algorithm is quantum [[modular exponentiation]], which is by far slower than the [[quantum Fourier transform]] and classical pre-/post-processing. … Reversible circuits typically use on the order of n³ gates for n qubits.」
- 「In 2001, Shor's algorithm was demonstrated by a group at [[IBM]], who factored 15 into 3 × 5, using an [[Nuclear magnetic resonance quantum computer|NMR implementation]] of a quantum computer with seven qubits.」
- 「However, none of these demonstrations fulfill the requirements of Shor's algorithm: they compile the circuit using prior knowledge of the solution, and some have even oversimplified the algorithm in a way that makes it equivalent to coin flipping.」
- 「The algorithm restated shortly … # Pick a random number 1 < a < N. # Compute K = gcd(a, N) … # If K ≠ 1, then K is a nontrivial factor of N … # If r is odd, then go back to step 1. # Compute g = gcd(N, a^(r/2) + 1). If g is nontrivial, the other factor is N/g, and we're done. Otherwise, go back to step 1.」

## Post-quantum cryptography（Wikipedia，2026-11-18 讀取）

- 「NIST finalized the first three FIPS Post-Quantum Cryptography standards in August 2024.」
- 「Data that is currently not quantum-safe, whether it is stored or transmitted, and that must remain confidential for a long time, may be compromised in the future by quantum computers ("harvest now, decrypt later" attacks).」
- 表格：「FIPS-203: [[CRYSTALS-Kyber]] || ML-KEM」。

## 學程內部文件：docs/超導量子電腦師生對話教學紀錄.md 第 10 課

- 「Shor（1994）在多項式時間內分解大整數，直接威脅 RSA。」
- 「選和 N 互質的 a，f(x) = aˣ mod N 會週期重複，最小週期 r 滿足 aʳ ≡ 1。若 r 為偶數，aʳ − 1 = (a^(r/2) − 1)(a^(r/2) + 1) ≡ 0 (mod N)，所以 **gcd(a^(r/2) ± 1, N) 就是因數**。」
- 表：「7ˣ mod 15 | 1 | 7 | 4 | 13 | **1** | 7 | 4 | 13」；「r = 4；7² ≡ 4；gcd(3, 15) = **3**、gcd(5, 15) = **5**。若 r 為奇數或 a^(r/2) ≡ −1（例如 a = 14）就換 a，成功率至少一半。古典找不到 r：2048 位元時 r 可大到 2²⁰⁴⁸ 量級，序列看起來完全隨機。」
- 「二、量子部分（N = 15、計數 4 顆、Q = 16）：1. 計數暫存器 H⊗4：x = 0～15 均勻疊加。2. **模指數** |x⟩|0⟩ → |x⟩|7ˣ mod 15⟩：一次算進 16 個值，**產生大量糾纏**（Shor 真的需要糾纏）。3. （觀念上）量工作暫存器得到 4 → 計數暫存器剩 (|2⟩+|6⟩+|10⟩+|14⟩)/2：間隔 4 的**梳子**，起點隨機。4. **QFT**：梳子 → 間隔 Q/r = 4 的尖峰：y = 0、4、8、12 各 25%，其他 12 個完全抵消。起點只影響尖峰的相位，不影響位置。5. 古典後處理：y/Q ≈ k/r。y = 4 → 1/4 → r = 4；y = 12 → 3/4 → r = 4；y = 8 → 1/2 → 試倍數得 4；y = 0 → 重跑。真實情況用**連分數**。」
- 「QFT 像稜鏡：把藏在振幅裡的週期轉成量得到的尖峰。古典 FFT 約 n·2ⁿ 步，QFT 約 n² 個閘——**指數加速從這裡來**。」
- 「**三、真正難的是模指數**：閘數約 n³，RSA-2048 需上億到數十億個邏輯閘、全程不能錯。」表：「Gidney & Ekerå（2019）| 約 2000 萬 | 約 8 小時」「Gidney（2025）| 不到 100 萬 | 不到一週」；「前提：實體錯誤率約 0.1% 加表面碼。分解 15、21 的實驗多半是事先簡化的 compiled Shor。」
- 「NIST 2024 年 8 月公布 **ML-KEM（FIPS 203）、ML-DSA（FIPS 204）、SLH-DSA（FIPS 205）**。最急迫的風險是「**現在先收集，以後再解密**」。」
- 第 7 課（BV）與第 9 課（Deutsch）原文都寫明沒有用到糾纏（本集「和伯恩斯坦、德意志那兩個演算法不同」之依據；transmon-3d 第 8 章步驟 3 亦寫「和 Deutsch、BV 不同，Shor 真的需要糾纏」）。

## 學程內部簡報

- slides/transmon.pptx 第 23 頁「Shor 演算法：用 QFT 找週期，分解 15」：「① 古典歸約　分解 N = 15 → 找 f(x) = 7ˣ mod 15 的週期 r。」「② 均勻疊加　4 顆計數位元，16 個 x 同時存在。」「③ 模指數　一次算出所有 f(x)，兩組暫存器產生糾纏。」「④ 梳子　f(x) = 4 時只剩 x = 2、6、10、14。」「⑤ QFT　間隔 r 的梳子 → 間隔 Q/r = 4 的尖峰。」「⑥–⑦ 量測與後處理　量到 0、4、8、12；連分數找 r = 4，gcd(7² ± 1, 15) = 3、5。」「⑧ 自由實驗　換 N（15、21）、a 與計數位元數。」
- 第 19 頁十二章一覽：「▶ 3D 第 8 章：Shor | p22 | Shor：用 QFT 找週期，分解 15」（一覽表寫 p22；實際內容在 p23，課綱寫 p23，本集引 p23）。
- slides/QC_Operation_Talk.pptx 第 41 頁「Shor 演算法：用干涉找週期」：「① H⊗⁶ | x = 0…63 均勻疊加」「② 模指數 | 計算 f(x) = 7ˣ mod 15 = 1, 7, 4, 13, 1, …（週期 4）」「④ QFT 後：峰值在 64k/r = 0、16、32、48」「gcd(4 − 1, 15) = 3，gcd(4 + 1, 15) = 5 | → 15 = 3 × 5」。
- 第 44 頁應用地圖：「密碼分析（RSA、ECC） | Shor | 指數級 | 需容錯；RSA-2048 估計 < 100 萬實體位元、< 1 週（2025）」「資源估計：Gidney, arXiv:2505.15917（2025）」。

## 互動動畫程式

- animations/transmon-3d.html 第 8 章（id: shor，「Shor 演算法：用 QFT 找週期，分解 15」）：G8STEPS 八步「古典歸約、均勻疊加、模指數運算、量測工作暫存器、QFT、量測、連分數與 gcd、自由實驗」；步驟按鈕 `#g8steps`、`#g8auto`「自動接續」。
- 步驟 2 setup「init」（只有 x = 0），cue 5 秒推 H；步驟 3 cue 0.3 秒推 U（tileOn 全亮，f8Tags 標 f(x)）；步驟 4 cue 0.3 秒推 MW（w: 4），cue 9 秒 `bracket = true`（金色括號、「間隔 r = ${S.rTrue}」）；步驟 5 cue 0.3 秒推 QFT（dft）。D8 = { H: 1.2, U: 1.4, MW: 1.6, QFT: 2.6 } 秒。
- 顏色：phaseColor 以 PH_ANCH = [金 0xd6b04a, 青 0x35b8ac, 紅 0xf0625a, 紫 0x9b7be0] 對應相位 0°、90°、180°、270°；說明文字「長條高度＝振幅大小 ｜ 顏色＝相位（金 0°・青 90°・紅 180°・紫 270°）｜ 後方青色＝量測次數」。
- 自由實驗 extra：`data-n8="15"|"21"`、`data-q8="16"|"32"`（「4 顆（Q = 16）」「5 顆（Q = 32）」）、`#g8alist` 以 gcd(a, N) = 1 列出 a 按鈕（`data-a8`）、「① 疊加」「② 模指數」「③ 量測工作」「④ QFT」「⑤ 量測 1 次」「量測 20 次」（`data-op8`）、`#g8run`「一鍵執行」、`#g8reset`「重設」。
- postProcess(y)：y = 0 →「y = 0，重跑」；找不到 r →「找不到 r，重跑或加大 Q」；r 奇數 →「r = … 為奇數」；h === N − 1 →「a^(r/2) ≡ −1」；成功 →「N = p × q」。自由實驗量完字幕：成功「量到 y = … → r = … → …。」、失敗「量到 y = …：…。再量一次或換 a 試試。」面板 `#g8r`「${rTrue}（${a}^${rTrue} mod ${N} = 1）」。
- 第 8 步說明文字：「N = 15、a = 14：r = 2，但 14 ≡ −1 → 失敗，要換 a。・N = 21、a = 2：週期 r = 6 不整除 Q，尖峰會「糊開」…改成 5 顆位元（Q = 32）尖峰更集中、成功率較高——理論上要 Q ≥ N²」。
- 注意：postProcess 的成功判斷只排除 h === N − 1，未排除 h === 1；當候選 r 是真實週期的倍數（例如 N = 21、a = 2、Q = 32、y = 23 → r = 12，2⁶ mod 21 = 1）時，會顯示「21 = 21 × 1」為成功。本集旁白未涉及此情況；教材程式把它判為平凡因數、重跑。
- animations/js/operation/10_shor.js（場景 10「Shor 週期尋找」）：Q = 64、nq = 6；STEPS「初始：|0⟩|1⟩」「① H⊗⁶：x 暫存器均勻疊加（64 個 x 同時存在）」「② 計算 f(x) = aˣ mod N（顏色 = f(x)）：週期性藏在疊加裡」「③ 量測第二暫存器 → 只留下 f(x) 相同的 x（間隔 = r）」「④ QFT：週期 r 轉成峰值，位置 ≈ 64·k / r」「⑤ 量測 x 暫存器得到 y（白色），交給古典電腦」；按鈕「N = 15」「N = 21」「a = …」「下一步 ▶」「自動播放」（先 reset，每 1.8 秒 next）「重設」；峰值柱子顏色 0x38c6d9（青）、量到的 y 為白色，峰值標籤（probs > 0.03）；右下角 inset「f(x) = aˣ mod N（週期函數）」畫 x = 0～32 並寫「a = …，週期 r = …」；readout 「峰值應在 64k/r：…」與連分數、gcd 推導。

## 實跑紀錄（shor_lab.py，Python 3.13.18，無外部套件，SEED = 7）

```
N = 15，a = 7，計數位元 4 顆（Q = 16）
f(x) = 7^x mod 15：1, 7, 4, 13, 1, 7, 4, 13, 1, 7, 4, 13 …
真實週期 r = 4（古典驗算：7^4 mod 15 = 1）
量測工作暫存器得到 4 → 梳子 x = 2, 6, 10, 14
QFT 後機率最大的 y：0（25.0%）、4（25.0%）、8（25.0%）、12（25.0%）
量測 20 次：y=0 8 次、y=4 2 次、y=8 6 次、y=12 4 次
  y = 0（8 次）：y = 0 → 沒有週期資訊，重跑 ✗
  y = 4（2 次）：4/16 → r = 4 → 7^2 mod 15 = 4 → gcd(3, 15) = 3，gcd(5, 15) = 5 → 15 = 3 × 5 ✓
  y = 8（6 次）：8/16 → r = 4 → 7^2 mod 15 = 4 → gcd(3, 15) = 3，gcd(5, 15) = 5 → 15 = 3 × 5 ✓
  y = 12（4 次）：12/16 → r = 4 → 7^2 mod 15 = 4 → gcd(3, 15) = 3，gcd(5, 15) = 5 → 15 = 3 × 5 ✓
成功分解 12 / 20 次
```

改造試跑：A = 14 → 真實週期 2，尖峰 y = 0、8 各 50%，y = 0 十次、y = 8 十次「14^1 mod 15 = 14 ≡ −1 → 換一個 a」，成功 0 / 20；A = 4 → 成功 10 / 20；N = 21、A = 2、COUNT_QUBITS = 4 → 真實週期 6，部分 y「找不到 r，重跑或加大 Q」，成功 8 / 20；COUNT_QUBITS = 5 → 成功 13 / 20（其中 y = 23 一次判為平凡因數）；A = 5 → 「gcd(5, 15) = 5：運氣好，直接找到因數 5，不用量子電腦」。
