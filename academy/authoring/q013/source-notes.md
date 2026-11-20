# Q013 來源筆記（逐字引文）

查核日：2026-11-18。維基百科頁面由製作代理直接開啟（revision id 取自 MediaWiki API 的 revid）。學程內部簡報與動畫程式由製作代理讀取。程式由製作代理實際執行。

## Grover's algorithm（Wikipedia，oldid=1385418712）

- 「Grover's algorithm, also known as the quantum search algorithm, is a quantum algorithm for unstructured search that finds with high probability the unique input to a black box function that produces a particular output value, using just O(√N) evaluations of the function」
- 「there is no better approach than trying out all input values one after the other, which, on average, takes N/2 steps」
- 「Unlike other quantum algorithms, which may provide exponential speedup over their classical counterparts, Grover's algorithm provides only a quadratic speedup.」
- 「so Grover's algorithm is asymptotically optimal」
- 「Instead, an oracle is invoked to evaluate an item by its index.」「In such applications, the oracle is a way to check the constraint and is not related to the search algorithm.」
- 「It is straightforward to check that the operator U_s U_ω of each Grover iteration step rotates the state vector by an angle of θ = 2 arcsin(1/√N).」
- 「We need to stop when the state vector passes close to |ω⟩; after this, subsequent iterations rotate the state vector away from |ω⟩, reducing the probability of obtaining the correct answer.」
- 「The earliest time that we get a near-optimal measurement is therefore r ≈ π√N/4.」

## 學程內部簡報

- slides/QC_Operation_Talk.pptx 第 40 頁「Grover 搜尋：振幅放大」：「3D 場景 9：N = 16，3 輪後答案（11 號）的機率 ≈ 96%」「Oracle：只把答案的振幅變號（機率不變）」「擴散：每個振幅 a → 2·平均 − a；答案離平均最遠 → 被放大」「每輪在「答案 / 非答案」平面上轉 2θ，sin θ = 1/√N」「轉太多會轉過頭 → 必須算好次數」「平方加速：N = 10⁶ 時，古典平均 50 萬次，Grover ~785 次」。講者備註：「N = 64 時成功機率隨迭代次數的變化：6 次就到 99.7%，但再繼續反而下降——轉過頭了。」
- slides/output/basic-circuits.pptx 第 23 頁：「② 標記（Oracle）……Oracle 認得答案 |11⟩，只把它的振幅變成負的；機率不變」「③ 擴散 新振幅 = 2 × 平均 − a」。
- 第 24 頁：「比平均高的翻下來、比平均低的翻上去：被標記成負的答案離平均最遠，翻得最高」。
- 第 25 頁：「1 輪 答案 78.1%」「2 輪（最佳）答案 94.5%」「3 輪 降到 33.0%：轉過頭了」「每一輪把狀態往答案轉一個固定角度；最佳輪數約 (π/4)√N，再轉下去機率反而下降」。
- 第 26 頁表格：「16（4 顆）｜8.5 次｜3 輪｜96.1%」；「古典約 N/2 次、Grover 約 (π/4)√N 輪：平方加速，而且已經證明黑盒搜尋不可能更快」；講者備註「這是平方加速，不像 Shor 那樣是指數加速」。

## 互動動畫程式

- animations/js/operation/09_grover.js：`n = 4, mark = 11`（第 15 行）；desc「柱子高度是振幅（不是機率），可以是負的。綠框是要找的答案」「Oracle：把答案的振幅變號（翻到下面）。機率沒變」「擴散（對平均值反射）：每個振幅 a → 2·平均 − a」「轉太多次反而會轉過頭！」（第 6–11 行）；正振幅顏色 0xe0a54a、負振幅 0x4f8cff（第 38 行）；`kOpt = max(1, round(π/(4θ) − 0.5))`（第 43 行）；滑桿「量子位元數 n」2–6、「答案（標記的項目）」0–63（第 44–45 行）；按鈕「② Oracle」「③ 擴散」「完整一輪」「自動跑到最佳次數」「測量」「重設」（第 48–54 行）；插圖「幾何圖：每輪在「答案–非答案」平面轉 2θ」與「P(成功) vs 輪數」曲線（第 58–79 行）；粉紅面只在做完 Oracle 時出現（第 85 行）；讀數「答案的機率 P」「最佳輪數 ≈ (π/4)√N」「古典平均要查 N/2 次」（第 89–90 行）。
- animations/basic-circuits.html#grover（約第 470–515 行）：2 或 3 顆位元、答案按鈕、重複輪數「最佳／1 輪／2 輪／3 輪」；`meanLine: true`（平均值虛線）；轉過頭時說明「Grover 不是越多輪越好，要停在最佳輪數」；重點「Grover 把搜尋從約 N 次降到約 √N 次（平方加速），而且已經證明黑盒搜尋不可能更快」。
- animations/transmon-3d.html 第 7 章（G7STEPS，約第 1598–1659 行）：「我們有一個只會回答「是／不是」的檢查器（oracle）」；「擴散……答案的機率從 25% 變成 100%」；「⑥ 再多做一次：轉過頭了……四個振幅都變成 −½：又回到各 25%」。

## 實跑紀錄（grover_rounds.py，Python 3，無套件）

```
N = 16：第 0–8 輪 0.062 0.473 0.908 0.961 0.582 0.125 0.020 0.365 0.836
N = 64：第 0–8 輪 0.016 0.135 0.344 0.591 0.816 0.964 0.997 0.907 0.718
N = 4 ：第 1 輪 1.000，第 2 輪 0.250
估算口訣 floor(0.785×√N) 與動畫 kOpt：N = 4、8、16、32、64 → 1、2、3、4、6（相同）
```
