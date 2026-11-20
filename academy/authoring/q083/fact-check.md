# Q083 事實查核

查核日：2026-11-18。查核者：製作代理（Claude）。逐字引文見 `source-notes.md`。
方法：學程文件（師生對話教學紀錄第 11 課）、簡報 QC_Operation_Talk.pptx 第 48–49 頁、transmon-3d.html 第 10 章原始碼由製作代理讀取；維基百科 Quantum error correction 與 Repetition code 以原始 wikitext 讀取；邏輯錯誤率由製作代理重算。
限制：本學程沒有重複碼專用簡報與場景；邏輯錯誤率公式假設每顆獨立、機率相同、症狀量測不出錯。

| # | 本集的說法（幕） | 依據 | 結論 |
|---|---|---|---|
| 1 | 上一堂：錯誤緩解（放大雜訊再外插）讓期望值更準，但不保護量子資訊本身（1） | Q082 課綱（零雜訊外插）；簡報 p48「錯誤緩解改善的是期望值的估計，不保護量子資訊本身」 | 相符 |
| 2 | 古典重複碼：零傳三個零、一傳三個一（3） | Repetition code：Example（101 → 111 000 111） | 相符 |
| 3 | 三個不一樣時少數服從多數，收到零一零判為零（3） | Repetition code：majority decision | 相符 |
| 4 | 錯一份救得回來；三倍位元；很少單獨用，最大優點是簡單（3） | Repetition code：可修正 (n−1)/2 個；low code rate、poor performance as stand-alone；chief attraction is ease of implementation | 相符 |
| 5 | 不可複製定理：未知量子態不能複製成三份（4） | QEC：no-cloning theorem prevents copying an unknown qubit；對話紀錄「未知量子態不能複製三份」 | 相符 |
| 6 | 再拿兩顆零態位元，兩個受控反閘編碼，零→三個零、一→三個一，疊加變糾纏態（4） | QEC：|0⟩→|000⟩、|1⟩→|111⟩，two CNOT gates，ancillary qubits initialized in |0⟩；α|000⟩+β|111⟩ | 相符 |
| 7 | 每一輪：雜訊翻一顆→量兩組奇偶→翻轉閘翻回（4） | QEC：若結果為 P_i 則對第 i 顆做 Pauli X；對話紀錄 Z₁Z₂、Z₂Z₃ | 相符 |
| 8 | 直接讀資料會讓疊加塌縮（5） | 簡報 p49「不能直接量資料（會塌縮）」；對話紀錄「一量就塌縮」 | 相符 |
| 9 | 症狀只說哪裡不同，不說資料是零還是一（5） | QEC：reveals which qubits are different … without … giving information about the state of the qubits themselves | 相符 |
| 10 | 兩顆輔助位元，各比較一、二與二、三（6） | 對話紀錄：輔助位元量 Z₁Z₂、Z₂Z₃ | 相符 |
| 11 | 兩顆資料位元各對輔助位元做受控反閘；相同維持零、不同變一；只量輔助（6） | 對話紀錄「把資料位元用 CNOT 加總 mod 2 到輔助位元」；0⊕a⊕b | 相符 |
| 12 | 三個零與三個一的比較結果一樣，症狀與疊加比例無關（6） | 對話紀錄「|000⟩ 和 |111⟩ 的奇偶一樣，所以量到的資訊和 α、β 無關」 | 相符 |
| 13 | 四種症狀對照（7） | 對話紀錄表：同同沒錯、異同第 1 顆、異異第 2 顆、同異第 3 顆；classroom.py 逐一驗算 | 相符 |
| 14 | 一、二同時被翻→症狀同、異→看起來是第三顆→修完三顆全翻（8） | QEC：if the first and second qubits are flipped, the syndrome … P_3, and the third qubit is flipped | 相符 |
| 15 | 三位元重複碼最多修一個錯；修更多要更多位元（8） | Repetition code：(n−1)/2 | 相符 |
| 16 | 翻兩枚三種挑法、翻三枚一種；p = 10% 時邏輯錯誤率約 2.8%（10） | QEC：兩顆 3p²(1−p)、三顆 p³；3×0.01×0.9 + 0.001 = 0.028 | 相符 |
| 17 | 超過一半時編碼反而更糟（10） | QEC：p < 1/2 時修正後較好；p = 0.6 → 0.648 > 0.6（製作代理重算） | 相符 |
| 18 | 只防位元翻轉，防不了相位翻轉（12） | QEC：repetition code 對應只修 X 或只修 Z 的 biased code；sign-flip 是另一種碼；動畫「表面碼同時防 X、Z 兩種錯誤，這是 3 位元重複碼做不到的」 | 相符 |
| 19 | 預告下一堂：表面碼，同時抓兩種錯誤（12） | academy/lessons/Q084/brief.md；transmon-3d.html 第 10 章步驟 ④ | 相符 |
| 20 | 動畫：步驟 ③ 中間一顆翻轉、兩塊青色格子亮、白線配對、補翻轉（展示 1） | transmon-3d.html G10STEPS[2] cues、inject10(4,"X")、decode10()、TILE.Z.lit 0x3cf0dc | 相符（固定腳本） |
| 21 | 動畫：步驟 ⑥ 相鄰兩顆翻轉、共用格子不亮、只亮邊上半圓、去翻第三顆、紅線與邏輯錯誤紅字（展示 2） | G10STEPS[5] cues；logi10 紅線；logTag10 文字「邏輯錯誤！（邏輯 X）」 | 相符（固定腳本） |
