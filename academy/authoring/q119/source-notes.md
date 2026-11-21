# Q119 來源筆記（逐字引文）

查核日：2026-11-19（檔頭 CHECKED 依派工統一寫 2026-11-18）。維基百科頁面由製作代理直接讀取原始 wikitext（action=raw），revision id 取自頁面的 wgRevisionId。學程內部簡報（python-pptx 讀出實際頁碼、文字與備註）、文件與動畫程式由製作代理讀取。程式由製作代理實際執行。

## Deutsch–Jozsa algorithm（Wikipedia，oldid=1381683602）

- 「Although of little practical use, it is one of the first examples of a quantum algorithm that is exponentially faster than any possible deterministic classical algorithm.」
- 「We are promised that the function is either constant (0 on all inputs or 1 on all inputs) or ''balanced'' (1 for exactly half of the input domain and 0 for the other half).」
- 「For a conventional deterministic algorithm where n is the number of bits, 2^{n-1} + 1 evaluations of f will be required in the worst case.」「The best case occurs where the function is balanced and the first two output values are different.」
- 「For a conventional randomized algorithm, a constant k evaluations of the function suffices to produce the correct answer with a high probability (failing with probability ε ≤ 1/2^{k} with k ≥ 1). However, k=2^{n-1} + 1 evaluations are still required if we want an answer that has no possibility of error. The Deutsch-Jozsa quantum algorithm produces an answer that is always correct with a single evaluation of f.」
- 「The Deutsch–Jozsa algorithm generalizes earlier (1985) work by David Deutsch, which provided a solution for the simple case where n = 1.」
- 「The algorithm, as Deutsch had originally proposed it, was not deterministic. The algorithm was successful with a probability of one half.」
- 「Further improvements to the Deutsch–Jozsa algorithm were made by Cleve et al., resulting in an algorithm that is both deterministic and requires only a single query of f.」（Cleve 等人的論文年份 1998：條目開頭「with improvements by Richard Cleve, Artur Ekert, Chiara Macchiavello, and Michele Mosca in 1998」）
- 「The probability of measuring k = 0, corresponding to |0⟩^{⊗n}, is |1/2^n Σ(−1)^{f(x)}|^2 which evaluates to 1 if f(x) is constant (constructive interference) and 0 if f(x) is balanced (destructive interference). In other words, the final measurement will be |0⟩^{⊗n} (all zeros) if and only if f(x) is constant and will yield some other state if f(x) is balanced.」
- Deutsch's algorithm 一節：「We need to check the condition f(0)=f(1). It is equivalent to check f(0)⊕f(1) … if zero, then f is constant, otherwise f is not constant.」

## Promise problem（Wikipedia，oldid=1381407752）

- 「a promise problem is a generalization of a decision problem where the input is promised to belong to a particular subset of all possible inputs.」
- 「If such an input is given to an algorithm for solving a promise problem, the algorithm is allowed to output anything, and may even not halt.」

## 學程內部簡報：slides/output/qfish008-deutsch-algorithm.pptx（《量子金魚》008）

課綱寫 p5–25；實際用到第 5–10、14、25、27 頁（第 27 頁在課綱範圍外，但驗收標準點名「簡報 p27 有三個誠實的限制」，頁碼與內容相符）。
- 第 5 頁：「盒子裡有 50 顆球，準備時只有兩種方式；放進搖獎機，每次只能搖出一顆」「全部同一色 全紅（或全綠） → 等一下叫做「常數」」「一半紅、一半綠 25 紅 ＋ 25 綠 → 等一下叫做「平衡」」「搖出來的球不放回」。
- 第 6 頁：「x ＝ 第幾次搖、f(x) ＝ 搖出的顏色（0 或 1）」；表格 f₁ 0（紅）0（紅）常數 兩顆都紅／f₂ 1（綠）1（綠）常數 兩顆都綠／f₃ 0（紅）1（綠）平衡 一紅一綠／f₄ 1（綠）0（紅）平衡 一綠一紅。
- 第 7 頁：「只搖一次，一定只看到一個顏色，什麼都不能回答」「古典電腦一次只能問一個問題：兩顆球的情況，至少要問 2 次」。
- 第 8 頁：「運氣好 第 2 顆就結束」「明明一半紅一半綠，卻連抽 25 抽都是紅的」「第 26 顆 一定知道答案」「最壞情況要檢查「球數的一半再加一顆」：N/2 + 1；50 顆 → 26 次，100 萬顆 → 50 萬零 1 次」。
- 第 10 頁表格：「100 萬｜500,001｜1｜約 20」。
- 第 14 頁：「量到全部都是 0 → 常數 / 只要有任何一個 1 → 平衡」。
- 第 25 頁「案例五：8 顆球的相長與相消」：「3 個量子位元 → 8 顆球、8 條路徑 / 神諭在每條路蓋一個 (−1)f(x) 的章 / 常數：8 支箭頭同向 → P(000) = 1 → 全部 0 / 平衡：4 正 4 負，頭尾相接回到原點 → P(000) = 0 → 一定有 1」。
- 第 27 頁「（補充）誠實看待：三個限制」：「有承諾的問題 要先保證只有兩種 只能是「全同色」或「剛好一半一半」 / 其他比例的搖獎機不適用」「古典也不差 允許一點點出錯的話 隨機搖 10 顆都同色 → 判常數 / 猜錯機率 ≤ 2−9（約 0.2%） / 量子的優勢在「100% 確定」」「實機有雜訊 需要重複量測 … 實際上會跑很多次（shots）看統計 / 1985 年的原始版本也只有一半機會成功，1998 年才改成 100% 確定」。

## 學程內部簡報：slides/output/basic-circuits.pptx

課綱寫 p18–20，頁碼無誤。
- 第 18 頁：「範例 6｜Deutsch：查一次分辨常數或平衡」「q0 |0⟩（輸入）」「q1 |0⟩（輔助）」「① 輔助位元翻成 1」「② 兩顆都做 H」「③ 黑盒（只問一次）」「④ q0 做 H 再量測」「0 → 常數（f(0) = f(1)）；1 → 平衡（f(0) ≠ f(1)）」。
- 第 19 頁：「位元字串是 |q1 q0⟩；黑盒 f(x) = x 就是一個 CNOT（q0 → q1）」。
- 第 20 頁表格：「f(x) = 0｜常數｜什麼都不做｜|+⟩｜0（100%）」「f(x) = 1｜常數｜X(q1)｜−|+⟩（整體負號量不到）｜0（100%）」「f(x) = x｜平衡｜CNOT(q0 → q1)｜|−⟩｜1（100%）」「f(x) = 1 − x｜平衡｜CNOT(q0 → q1) 再 X(q1)｜−|−⟩｜1（100%）」；「古典要問 f(0)、f(1) 兩次；量子只問 1 次，四種黑盒都 100% 判斷正確」。

## 學程內部文件：docs/超導量子電腦師生對話教學紀錄.md 第 9 課

- 四種函數表「f₁ 永遠 0｜0｜0｜常數」「f₂ 永遠 1｜1｜1｜常數」「f₃ = x｜0｜1｜平衡」「f₄ = NOT x｜1｜0｜平衡」。
- 「古典一定要問 **2 次**；量子只問 **1 次**，而且**拿到的是兩值之間的關係，卻不知道各自是多少**。」
- 家族表：「Deutsch–Jozsa（1992）｜n 位元常數／平衡｜最壞 2ⁿ⁻¹+1 次｜1 次」。

## 互動動畫程式

- animations/basic-circuits.html 範例 6（id: deutsch）：`opts: [{ key: "f", label: "黑盒裡的函數", def: "x", choices: [["0", "f(x)=0"], ["1", "f(x)=1"], ["x", "f(x)=x"], ["nx", "f(x)=1−x"]] }]`；`oracle = { "0": [[]], "1": [[X(1)]], "x": [[CX(0, 1)]], "nx": [[CX(0, 1)], [X(1)]] }`；`n: 2, meas: [0], bloch: [0, 1]`；
  `verdict: k => (k === "0" ? "→ 常數函數" : "→ 平衡函數")`；showLast 只在 `k === b.steps.length`（最後一步）顯示判定；go() 會 clearShots()；`.hist .got` 綠色為實際次數、`.exp` 灰色為理論。
- animations/js/operation/08_interference.js：`ui.radio([['A', '單一量子位元：兩條路徑'], ['B', '3 位元：8 條路徑（Deutsch–Jozsa）']], …)`；`FN = { c0: ['常數 f = 0', …], c1: ['常數 f = 1', () => 1], b0: ['平衡 f = x₀', (x) => x & 1], bp: ['平衡 f = 奇偶', (x) => (x ^ (x >> 1) ^ (x >> 2)) & 1], rnd: ['隨機（非保證）', null] }`；`let fkey = 'b0'`；
  中間箭頭 `bMid[x].ar.setVec(new THREE.Vector3(0.3 * s, 0, 0))`（s = f(x) ? −1 : 1）；`pB.set(`P(000) = …`)`；插圖標題「最後量測的機率分佈（8 種結果）」，`color: (i) => (i === 0 ? '#e0a54a' : '#4f8cff')`；readout「常數函數：完全相長」「平衡函數：完全相消」「（古典最壞要查 2ⁿ⁻¹+1 = 5 次）」。

## 製作代理試拍（2026-11-19，Playwright 單張截圖，1600×900，nice -n 19；非正式錄影、非 QV2_DRY）

- bc#deutsch 第 4 步：f(x)=0 `|ψ⟩ = (|00⟩ − |10⟩) / √2`，|00⟩ +.707（fill p）、|10⟩ −.707（fill n）；量 1,000 次「0 1000（100.0%）」「→ 常數函數」。
  f(x)=1 `(−|00⟩ + |10⟩) / √2`；「→ 常數函數」1000 次 0。f(x)=x `(|01⟩ − |11⟩) / √2`；「→ 平衡函數」1000 次 1。f(x)=1−x `(−|01⟩ + |11⟩) / √2`；「→ 平衡函數」1000 次 1。
- bc#deutsch 第 3 步（#dots 第 4 個）：f(x)=0 `(|00⟩ + |01⟩ − |10⟩ − |11⟩) / 2`，理論「0 50%、1 50%」，實拍 531／469，無判定；f(x)=x `(|00⟩ − |01⟩ − |10⟩ + |11⟩) / 2`，實拍 505／495；按下一步後量 1,000 次：1000（100.0%）「→ 平衡函數」。
- op#interference 模式 B：常數 f = 1「f(x) = 1 的有 8 個 / |000⟩ 的振幅 … = -1.000 → P(000) = 1.000 / 常數函數：完全相長　（古典最壞要查 2ⁿ⁻¹+1 = 5 次）」，8 支箭頭朝左，插圖只有 000；
  平衡 f = x₀「P(000) = 0.000 / 平衡函數：完全相消」，插圖只有 001；平衡 f = 奇偶 P(000) = 0.000，插圖只有 111。面板捲到底後函數按鈕與 readout 同時入鏡。

## 實跑紀錄

見 `academy/authoring/q119/classroom.py` 的 RUN_OUTPUT（deutsch_lab.py，Python 3.13.18，random 種子 1119）與 QISKIT_OUTPUT（qiskit_check.py，Qiskit 2.6.2，StatevectorSampler seed=2026）；建置時會重跑 deutsch_lab.py 並比對輸出。
