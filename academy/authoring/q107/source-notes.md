# Q107 來源筆記（逐字引文）

查核日：2026-11-18。維基百科頁面由製作代理直接讀取原始 wikitext（action=raw），revision id 取自頁面的 wgRevisionId。學程內部文件、簡報與動畫程式由製作代理讀取。程式由製作代理實際執行。

## Deutsch–Jozsa algorithm（Wikipedia，oldid=1381683602）

- 「The '''Deutsch–Jozsa algorithm''' is a deterministic quantum algorithm proposed by David Deutsch and Richard Jozsa in 1992 with improvements by Richard Cleve, Artur Ekert, Chiara Macchiavello, and Michele Mosca in 1998.」
- 「Although of little practical use, it is one of the first examples of a quantum algorithm that is exponentially faster than any possible deterministic classical algorithm.」
- 「For a conventional deterministic algorithm where n is the number of bits, 2^{n-1} + 1 evaluations of f will be required in the worst case.」
- 「The Deutsch–Jozsa algorithm generalizes earlier (1985) work by David Deutsch, which provided a solution for the simple case where n = 1.」
- 「The algorithm, as Deutsch had originally proposed it, was not deterministic. The algorithm was successful with a probability of one half.」
- 「Further improvements to the Deutsch–Jozsa algorithm were made by Cleve et al., resulting in an algorithm that is both deterministic and requires only a single query of f.」
- 「The oracle maps its input state |x⟩|y⟩ to |x⟩|y⊕f(x)⟩, where ⊕ denotes addition modulo 2.」
- Deutsch's algorithm 一節：「We begin with the two-qubit state |0⟩|1⟩ and apply a Hadamard gate to each qubit.」「f(0)⊕f(1) = 0 if and only if we measure |0⟩ and f(0)⊕f(1)=1 if and only if we measure |1⟩. So with certainty we know whether f(x) is constant or balanced.」
- 同節推導：「=(−1)^{f(0)}\frac{1}{2}\left(|0⟩ + (−1)^{f(0)⊕f(1)}|1⟩\right)(|0⟩ − |1⟩).」（前面的 (−1)^{f(0)} 即整體相位）

## Controlled NOT gate（Wikipedia，oldid=1357848270）

- 「Working through each of the Hadamard basis states, the results on the right column show that the first qubit flips between |+⟩ and |−⟩ when the second qubit is |−⟩」
- 「When viewed in the computational basis, it appears that qubit A is affecting qubit B. Changing our viewpoint to the Hadamard basis demonstrates that, in a symmetrical way, qubit B is affecting qubit A.」（相位回踢的另一種說法；也呼應生活技能「換個角度讀資訊」）

## 學程內部文件：docs/超導量子電腦師生對話教學紀錄.md 第 9 課

- 四種函數表：「f₁ 永遠 0｜0｜0｜常數」「f₂ 永遠 1｜1｜1｜常數」「f₃ = x｜0｜1｜平衡」「f₄ = NOT x｜1｜0｜平衡」；「古典一定要問 **2 次**；量子只問 **1 次**」。
- 「**量子黑盒子**必須可逆：U_f|x⟩|y⟩ = |x⟩|y ⊕ f(x)⟩。把 y 準備在 **|−⟩**：f(x) = 0 不變；f(x) = 1 時 |−⟩ 變 −|−⟩。所以 **U_f|x⟩|−⟩ = (−1)^f(x)|x⟩|−⟩**——f(x) 變成正負號，「回踢」到輸入位元上（和 Grover 的 oracle 同一招）。」
- 結果表：「f₁｜(+, +)｜+|0⟩｜0」「f₂｜(−, −)｜−|0⟩｜0」「f₃｜(+, −)｜+|1⟩｜1」「f₄｜(−, +)｜−|1⟩｜1」；「結果 100% 確定；前面的 ± 是整體相位，量不到」。
- 「以 f₃ 用四根振幅長條看：H⊗H 後 (+½, −½, +½, −½)；CNOT 交換 |10⟩、|11⟩ 後 (+½, −½, −½, +½) = |−⟩|−⟩，**q0 從 |+⟩ 變成 |−⟩**，而且兩個乘積相等，**全程乘積態**。」
- 硬體表：「q1 準備 |1⟩｜π 脈衝」「H｜π/2 脈衝（＋虛擬 Z）」「f₁｜什麼都不做」「f₂｜對 q1 做 X」「f₃｜CNOT = q1 的 H → **CZ** → q1 的 H」「f₄｜CNOT 再對 q1 做 X」。
- 「**誠實看待**：沒用到糾纏（q1 是 CNOT 的特徵態）；優勢是「查詢次數」不是速度；價值在於提出「只回答**全域性質**」的新觀念。」
- 開頭：「Deutsch（1985）是第一個證明「量子在某件事上比古典少做工」的演算法，它的機制 **phase kickback** 後來一路用到 Shor。」（維基百科補充：1985 原始版本成功機率一半，見上；旁白不說原始版本就是 100%）
- 課後練習答案：「只有 |−⟩ 會讓 f(x) 變成相位 (−1)^f(x) 回踢到 q0；|0⟩ 只會把 f(x) 寫在 q1 上。」「不能。兩者只差整體相位，量測看不到。」「沒有；它是概念示範，價值在觀念（全域性質、phase kickback）。」

## 學程內部簡報

- slides/transmon.pptx 第 21 頁：「振幅長條：糾纏、Grover 與 Deutsch」「⑦ Deutsch　黑盒子只問一次，就判斷 f 是常數還是平衡。 / ⑧ 自由實驗　自己送閘，或抽一個隱藏黑盒子來猜。」（課綱寫 p22；p22 實為「Shor 演算法：用 QFT 找週期，分解 15」，故改引 p21。）
- slides/output/qfish008-deutsch-algorithm.pptx 第 5 頁：「盒子裡有 50 顆球，準備時只有兩種方式；放進搖獎機，每次只能搖出一顆」「全部同一色 … → 等一下叫做「常數」」「一半紅、一半綠 … → 等一下叫做「平衡」」。
- 第 6 頁表格：「f₁｜0（紅）｜0（紅）｜常數｜兩顆都紅」…「f₄：f(x) = NOT x｜1（綠）｜0（紅）｜平衡｜一綠一紅」；「x ＝ 第幾次搖、f(x) ＝ 搖出的顏色（0 或 1）」。
- 第 7 頁：「古典電腦一次只能問一個問題：兩顆球的情況，至少要問 2 次」。
- 第 11 頁：「量子計算必須「么正」　么正（Unitary）＝可逆」「多一顆輔助位元當乩童，把答案「附身」上去」。
- 第 12 頁：「Uf |x⟩|y⟩ = |x⟩|y ⊕ f(x)⟩」「再做一次 Uf：y ⊕ f(x) ⊕ f(x) = y，自己就能復原 → 可逆」。
- 第 15 頁：「|+⟩ 與 |−⟩ 的差別只在中間的正負號（相位） / 兩者直接量都是 50/50，分不出來」。
- 第 16 頁：「乩童本身沒變，負號跑到 x 身上 → 常稱 phase kickback（相位回踢）」。
- 第 17 頁：「常數：±(|0⟩ + |1⟩)/√2 = ±|+⟩」「平衡：±(|0⟩ − |1⟩)/√2 = ±|−⟩」「常見誤會：「量子計算只要平行化，答案就出來了」——不是！光靠疊加還不夠」。
- 第 18 頁：「加號（常數）→ H → 0；減號（平衡）→ H → 1」。
- 第 22 頁：「f₂（兩顆都綠）｜常數｜X(乩童)：單位元 π 脈衝｜−|+⟩｜0（100%）」「f₃（紅、綠）｜平衡｜CNOT(輸入→乩童) = H–CZ–H｜+|−⟩｜1（100%）」「f₄（綠、紅）｜平衡｜CNOT 後再 X(乩童)｜−|−⟩｜1（100%）」「常數的神諭完全沒碰輸入位元；平衡的才需要兩位元閘 CZ」。
- 第 24 頁：「按「隨機（隱藏）」：電腦偷偷準備好搖獎機，電路上只顯示 U_f ?」「量完自動揭曉是哪個黑盒子，並顯示判斷是否正確」。
- slides/output/basic-circuits.pptx 第 18 頁：「① 輔助位元翻成 1」「② 兩顆都做 H　q0：|+⟩，q1：|−⟩」「③ 黑盒（只問一次）… f(x) = 1 的項多一個負號（相位回踢）」「0 → 常數（f(0) = f(1)）；1 → 平衡（f(0) ≠ f(1)）」。
- 第 19 頁：「看 ③：四個機率都還是 25%，但負號換了位置。答案藏在正負號裡，④ 的 H 才把它變成 q0 = 1」。
- 第 20 頁表格：「f(x) = 1｜常數｜X(q1)｜−|+⟩（整體負號量不到）｜0（100%）」「f(x) = 1 − x｜平衡｜CNOT(q0 → q1) 再 X(q1)｜−|−⟩｜1（100%）」。

## 互動動畫程式

- animations/transmon-3d.html：`HASH_ALIAS = { deutsch: ["grover", 6], "deutsch-lab": ["grover", 7] }`（#deutsch-lab 直接進第 7 章步驟 8「自由實驗」）。
- 第 7 章 extra 按鈕：`data-op="H0"`「H₁」、`"H1"`「H₂」、`"X0"`「X₁」、`"X1"`「X₂」、`"UF"`「U_f」；`#g7meas`「量測 50 次」、`#g7reset`「重設 |00⟩」、`#g7deu`「一鍵 Deutsch」；黑盒子 `data-fn="0"～"3"`「f₁：常數 0」「f₂：常數 1」「f₃：f(x) = x」「f₄：f(x) = NOT x」、`data-fn="hide"`「隨機（隱藏）」。
- 隨機隱藏字幕：「已隨機選好一個黑盒子（隱藏）。按「一鍵 Deutsch」只查詢一次，看能不能判斷它是常數還是平衡。」；一鍵 Deutsch 依序推入 X(q1)、H(q0)、H(q1)、U_f、H(q0)、量測 30 次；隱藏時電路方塊寫「U_f ?」，揭曉字幕「q0 量到 … → 平衡／常數。黑盒子揭曉是 …，判斷正確 ✓；整個過程只查詢了一次。」。
- 長條：負振幅為紅色（RED），正為金色；面板「a₀₀ · a₁₁」「a₀₁ · a₁₀」「判定 乘積態（C = 0）」；量測結果「量測結果（n 次）・第一位 q0：0 有 … 次、1 有 … 次」。U_f 對 f₃ 交換 |10⟩、|11⟩（`if (op.f === 2) sw(2, 3)`）。閘動畫時間：H 1.0、X 0.9、U_f 1.3（秒，依畫面幀推進，dt 上限 0.05）；量測每秒 20 次。
- 自由實驗 setup：`g7S.answer = 2`（長條下方「★ 答案」記號），一鍵 Deutsch 會設 `answer = -1`。
- animations/basic-circuits.html 範例 6（id: deutsch）：選項「黑盒裡的函數」`f(x)=0`、`f(x)=1`、`f(x)=x`、`f(x)=1−x`；四步「X 閘：輔助位元準備成 |1⟩」「H 閘：兩顆都疊加」「黑盒 U_f（只查詢這一次）」「H 閘：把相位轉成 0/1」；f(x)=1−x 的說明「只有 q0 = 0 的項會翻轉 q1 … q0 變成 −|−⟩ … q0 的 Bloch 向量一樣翻到 −x。」；布洛赫球「單看 q0」「單看 q1」；按鈕 `#bFirst`「⏮ 起點」、`#bNext`「下一步 ▶」、`#m1000`「量測 1,000 次」；判定 `verdict`「→ 常數函數／→ 平衡函數」。換選項時 `rebuild(false)` 停在最後一步。

## 製作代理試拍（2026-11-18，單張截圖，非正式錄影、非 QV2_DRY）

- #deutsch-lab 單步 f₃：X₂ → H₁ → H₂ → U_f 後長條為 +0.50、−0.50（紅）、−0.50（紅）、+0.50，面板「乘積態（C = 0）」；再按 H₁ 後只剩 |10⟩ +0.71、|11⟩ −0.71（紅）；量測 50 次「第一位 q0：0 有 0 次、1 有 50 次」。
- #deutsch-lab 隨機隱藏＋一鍵 Deutsch：電路方塊「U_f ?」，量完揭曉（該次為 f₂）「q0 量到 0 → 常數。黑盒子揭曉是 f₂：常數 1（常數），判斷正確 ✓；整個過程只查詢了一次。」。
- 一鍵 Deutsch 後立刻按重設 |00⟩：長條回到 |00⟩ +1.00、電路圖清空、「★ 答案」消失。面板捲到底時按鈕、判定與量測結果同時入鏡。
- basic-circuits.html#deutsch（zoom 0.74）f(x)=1−x：第 2 步單看 q0 的箭頭在左下（+x）、q1 在右上（−x）；第 3 步兩顆都在右上；第 4 步 q0 指向正下方 |1⟩；量測 1,000 次「q0 = 1」「→ 平衡函數」「1000（100.0%）」。

## 實跑紀錄（deutsch_box.py，Python 3.13.18，無外部套件，無亂數）

```
輔助位元準備成 |−⟩（先翻轉再哈達瑪）
  f1（永遠 0，常數）問完後振幅 +0.50 −0.50 +0.50 −0.50｜量到 1 的機率 0%｜判讀 常數 ✓
  f2（永遠 1，常數）問完後振幅 −0.50 +0.50 −0.50 +0.50｜量到 1 的機率 0%｜判讀 常數 ✓
  f3（f(x) = x，平衡）問完後振幅 +0.50 −0.50 −0.50 +0.50｜量到 1 的機率 100%｜判讀 平衡 ✓
  f4（f(x) = NOT x，平衡）問完後振幅 −0.50 +0.50 +0.50 −0.50｜量到 1 的機率 100%｜判讀 平衡 ✓
忘了先翻轉：輔助位元變成 |+⟩
  f1（永遠 0，常數）問完後振幅 +0.50 +0.50 +0.50 +0.50｜量到 1 的機率 0%｜判讀 常數 ✓
  f2（永遠 1，常數）問完後振幅 +0.50 +0.50 +0.50 +0.50｜量到 1 的機率 0%｜判讀 常數 ✓
  f3（f(x) = x，平衡）問完後振幅 +0.50 +0.50 +0.50 +0.50｜量到 1 的機率 0%｜判讀 常數 ✗
  f4（f(x) = NOT x，平衡）問完後振幅 +0.50 +0.50 +0.50 +0.50｜量到 1 的機率 0%｜判讀 常數 ✗
古典電腦：要分別問 f(0)、f(1) 共 2 次；量子：只問 1 次
盲測：黑盒子 ？ 只問 1 次 → 輸入位元量到 1 → 平衡
```
