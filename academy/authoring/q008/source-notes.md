# Q008 來源筆記（逐字引文）

查核日：2026-11-18。維基百科三頁由製作代理以擷取工具開啟，工具回報下列逐字引文（未記錄 oldid）。學程內部簡報與 3D 場景程式由製作代理讀取。

## Quantum entanglement（Wikipedia）

- 「the quantum state of each particle in a group cannot be described independently of the state of the others」
- 「can, in some cases, be found to be perfectly correlated」
- 「it cannot be used for faster-than-light communication.」

## No-communication theorem（Wikipedia）

- 「impossible for one observer to transmit information to another observer, regardless of their spatial separation.」
- 「information transfer does not violate special relativity by exceeding the speed of light.」

## CHSH inequality — CHSH game（Wikipedia）

- 「Charlie chooses bits x,y∈{0,1} uniformly at random, and then sends x to Alice and y to Bob.」
- 「Alice and Bob must then each respond to Charlie with bits a,b∈{0,1} respectively.」
- 「Charlie tests if a⊕b=x∧y」；「If this equality holds, then Alice and Bob win」
- 「Alice and Bob are forbidden from directly communicating with each other」
- 「it is impossible for them to win with a probability higher than 75%.」
- 「there exists a strategy which allows Alice and Bob to succeed with a probability of ~85%.」；「Since cos2(π8)≈85%」
- 製作代理重算：列舉兩人各 4 種固定策略（共 16 組），最多贏 3 種情況；cos²(π/8) = 0.8536。

## 學程內部簡報：slides/QC_Operation_Talk.pptx 第 10 頁

- 標題「糾纏：資訊存在『關聯』裡」；「Bell 態：兩顆的 Bloch 箭頭都縮成一點」。
- 「單獨量任一顆：50% / 50%，完全隨機」「兩顆一起量：結果永遠相同（00 或 11）」「糾纏是 Shor、錯誤更正、隱形傳態的必要資源；但不能用來超光速通訊」。
- 備註：「單方看到的結果是隨機的，沒辦法用來傳遞訊息，所以不違反相對論。」

## 學程內部簡報：slides/output/basic-circuits.pptx 第 10–12 頁

- 第 10 頁：「② H 閘（q0）」「③ CNOT（q0 → q1）」「(|00⟩ + |11⟩)/√2」「q0 是 1 的那一半，q1 也翻成 1。兩顆的結果永遠相同」「各自隨機、彼此一致，而且無法拆成兩顆位元各自的狀態：這就是糾纏」。
- 第 11 頁：「|01⟩ 的振幅搬到 |11⟩：只剩 00、11」。

## 3D 場景

- `animations/js/operation/04_register.js`：按鈕「Bell 態」「測量全部」「只測 q0」「重設 |0…0⟩」；說明「注意上排的箭頭縮成一點：單獨看任何一個量子位元都是完全隨機的，但兩者的結果永遠相同」。
- `animations/basic-circuits.html#bell`：步驟「H 閘：q0 進入疊加」「CNOT：糾纏」；「量測 1,000 次」按鈕。
