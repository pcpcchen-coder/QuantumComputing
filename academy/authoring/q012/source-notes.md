# Q012 來源筆記（逐字引文）

查核日：2026-11-18。維基百科頁面由製作代理直接開啟（revision id 取自頁面的 wgRevisionId）。學程內部簡報與動畫程式由製作代理讀取。程式由製作代理實際執行。

## Deutsch–Jozsa algorithm（Wikipedia，oldid=1381683602）

- 「Although of little practical use, it is one of the first examples of a quantum algorithm that is exponentially faster than any possible deterministic classical algorithm.」
- 「We are promised that the function is either constant (0 on all inputs or 1 on all inputs) or balanced (1 for exactly half of the input domain and 0 for the other half).」
- 「For a conventional deterministic algorithm where n is the number of bits, 2^(n−1)+1 evaluations of f will be required in the worst case.」
- 「The best case occurs where the function is balanced and the first two output values are different.」
- 「For a conventional randomized algorithm, a constant k evaluations of the function suffices to produce the correct answer with a high probability」
- 「The Deutsch-Jozsa quantum algorithm produces an answer that is always correct with a single evaluation of f.」
- 「The algorithm begins with the n+1 bit state |0⟩⊗n|1⟩ … A Hadamard gate is applied to each bit」
- 「which evaluates to 1 if f(x) is constant (constructive interference) and 0 if f(x) is balanced (destructive interference).」
- 「the final measurement will be |0⟩⊗n (all zeros) if and only if f(x) is constant and will yield some other state if f(x) is balanced.」
- 歷史段（本集未採用）：「The algorithm, as Deutsch had originally proposed it, was not deterministic. The algorithm was successful with a probability of one half.」

## 多伊奇-喬薩演算法（維基百科中文版，oldid=93934717）

- 頁面標題「多伊奇-喬薩演算法」。
- 「當f(x)是常函數（建設性干涉）時此機率為1，當f(x)是平衡函數（破壞性干涉）時此機率為0。」

## 學程內部簡報

- slides/QC_Operation_Talk.pptx 第 39 頁「一次查詢看出全域性質：Deutsch–Jozsa」：表格「常數 … 100%」「平衡 … 0%」；「古典：最壞要查 2ⁿ⁻¹ + 1 次才能確定」「量子：1 次查詢」「本身不實用，但展示了『疊加 + 相位 + 干涉』的完整配方」。講者備註：「中間 8 個小圓盤是 8 條路徑，箭頭朝右是 +1、朝左是 −1；最右邊大圓盤把 8 支箭頭頭尾相接。選常數函數，8 支箭頭同向……100% 量到 000；選平衡函數，正負各半，完全抵消」。
- slides/output/qfish008-deutsch-algorithm.pptx 第 8 頁：「最壞情況要檢查『球數的一半再加一顆』：N/2 + 1」；第 10 頁表格「1,024 = 2¹⁰ | 513 | 1 | 10」；第 13 頁「疊加 → 查詢 → 干涉」；第 14 頁「量到全部都是 0 → 常數 / 只要有任何一個 1 → 平衡」；第 15 頁「乩童：0 → X → 1 → H → |−⟩」；第 17 頁「常見誤會：『量子計算只要平行化，答案就出來了』——不是！光靠疊加還不夠」；第 19 頁「疊加負責『同時碰到所有可能』，干涉負責『只留下想要的答案』」；第 25 頁「常數：8 支箭頭同向 → P(000) = 1」「平衡：4 正 4 負，頭尾相接回到原點 → P(000) = 0」。
- slides/output/basic-circuits.pptx 第 18–20 頁：四步「① 輔助位元翻成 1 ② 兩顆都做 H ③ 黑盒（只問一次）④ q0 做 H 再量測」；「看 ③：四個機率都還是 25%，但負號換了位置」；「量子只問 1 次，四種黑盒都 100% 判斷正確」。

## 互動動畫程式

- animations/js/operation/08_interference.js：第 61–64 行 FN（常數 f = 0、常數 f = 1、平衡 f = x₀、平衡 f = 奇偶、隨機（非保證））；第 70 行模式按鈕「3 位元：8 條路徑（Deutsch–Jozsa）」；第 119–133 行箭頭方向 s = ±1、P(000) = sx²、readout「常數函數：完全相長」「平衡函數：完全相消」「古典最壞要查 2ⁿ⁻¹+1 = 5 次」；第 88–90 行右下直方圖（000 金色）。
- animations/js/operation/06_circuit.js：第 27–34 行 dj 範例「Deutsch–Jozsa（平衡函數）」（X(q2)、H×3、CX(0,2)、CX(1,2)、H×3、量測 q0 q1）；第 144 行量測 1000 shots。
- animations/basic-circuits.html：第 419–443 行 deutsch 範例（選項 f(x)=0、f(x)=1、f(x)=x、f(x)=1−x；量測 q0；verdict「→ 常數函數」「→ 平衡函數」）。

## 實跑紀錄（dj_check.py，Python 3.13，只用標準函式庫）

```
常數 f = 0  00000000 → P(000)=1.0（只有 000）
常數 f = 1  11111111 → P(000)=1.0（只有 000）
平衡 f = x₀ 01010101 → P(000)=0.0（只有 001）
平衡 奇偶   01101001 → P(000)=0.0（只有 111）
00001111 → P(000)=0.0（只有 100）
00010111 → P(000)=0.0（001、010、100、111 各 0.25）
10010111（五個 1，違反保證）→ P(000)=0.062，111 為 0.562，其他各 0.062
三位元平衡函數窮舉：70 種，全部 P(000)=0
```
