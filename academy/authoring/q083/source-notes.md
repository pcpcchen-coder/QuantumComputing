# Q083 來源筆記（逐字引文）

查核日：2026-11-18。學程文件、簡報與動畫程式由製作代理讀取；維基百科以原始 wikitext 讀取；邏輯錯誤率由製作代理重算。

## docs/超導量子電腦師生對話教學紀錄.md（第 11 課）

- 「不可複製定理｜未知量子態不能複製三份｜用**糾纏**分散資訊：α|000⟩ + β|111⟩」
- 「一量就塌縮｜直接量資料會毀掉疊加｜只量位元之間的**奇偶**」
- 「三、3 位元重複碼（只防 X）。輔助位元量 Z₁Z₂、Z₂Z₃」；表：同同→沒錯、異同→第 1 顆翻、異異→第 2 顆翻、同異→第 3 顆翻
- 「|000⟩ 和 |111⟩ 的奇偶一樣，所以量到的資訊**和 α、β 無關**，疊加完整保留。量奇偶就是把資料位元用 CNOT「加總 mod 2」到輔助位元」

## slides/QC_Operation_Talk.pptx

第 48 頁「錯誤緩解改善的是期望值的估計，不保護量子資訊本身；成本隨規模指數上升 → 是通往錯誤更正之前的過渡工具」
第 49 頁「難題 / 不能複製量子態，也不能直接量資料（會塌縮）」「解法：只量『奇偶』」「奇偶改變 = 症狀；量子資訊本身不被讀取」「碼距 d：可修正 ⌊(d−1)/2⌋ 個錯誤」

## animations/transmon-3d.html 第 10 章（G10STEPS）

- 步驟 ③：`[0.3, "在中間的 D5 注入一個 X 錯誤（紅色，位元翻轉）。", () => inject10(4, "X")]`、`[4.5, "含 D5 的兩個青色格子（Z 穩定子）亮了…"]`、`[11, "解碼器只看得到亮點。它把兩個亮點配成一對（白線），最短路徑正好經過 D5。", () => decode10()]`，dur 22
- 步驟 ④ body：「表面碼同時防兩種錯誤，這是 3 位元重複碼做不到的。」
- 步驟 ⑥：`inject10(0, "X"); inject10(3, "X")`；「D1、D4 在同一個青色格子裡，兩個翻轉互相抵消，它沒亮；只有左邊界的半圓（含 D4、D7）亮了。」「解碼器只看到一個亮點，最省的解釋是「D7 錯了一個」，於是在 D7 補 X。」「結果 D1、D4、D7 整行都是 X…邏輯位元被翻轉了，而且沒人發現！」，dur 31；第 25 秒才開導引線
- 解碼動畫：配對線 0–2.0 s、1.3 s 套用修正、2.0 s 判定；邏輯錯誤時畫紅線（logi10）並顯示紅色標籤
- `#g10auto`「自動接續」預設勾選

## Wikipedia: Quantum error correction（Bit-flip code、Sign-flip code、Classical repetition codes 段）

- 「the no-cloning theorem prevents copying an unknown qubit」「the three-qubit bit-flip code, first proposed by Asher Peres in 1985」
- 「|0⟩→|000⟩ and |1⟩→|111⟩ … This mapping can be realized for example using two CNOT gates, entangling the system with two ancillary qubits initialized in the state |0⟩.」
- 「No qubit is flipped with probability (1−p)³, a single qubit is flipped with probability 3p(1−p)², two qubits are flipped with probability 3p²(1−p), and all three qubits are flipped with probability p³.」
- 「This reveals which qubits are different from the others, without at the same time giving information about the state of the qubits themselves.」
- 「if the first and second qubits are flipped, then the syndrome measurement gives the outcome P_3, and the third qubit is flipped, instead of the first two.」
- 「F(ψ′) … ≥ 1−3p²+2p³ … the fidelity after error correction is greater than the one without for p<1/2.」
- 「Classical error-correcting codes that employ redundancy can be mapped to biased quantum codes that correct either Pauli X (bit-flip) or Pauli Z (phase-flip) errors. The simplest, though inefficient, example is the repetition code.」

## Wikipedia: Repetition code

- 「the receiver can recover the original message by looking at the received message in the data stream that occurs most often」
- 「error correcting capacity of (n−1)/2」「Decoding is usually done by a simple majority decision」
- 「Because of the bad error correcting performance coupled with the low code rate … The chief attraction of the repetition code is the ease of implementation.」

## 重算紀錄（製作代理）

P_L = 3p²(1−p) + p³：p = 1% → 0.0298%；5% → 0.725%；10% → 2.8%；20% → 10.4%；50% → 50%；60% → 64.8%。
八種翻法逐一套用解碼表（classroom.py 內 assert）：翻 0、1 枚回到 000，翻 2、3 枚變成 111。
