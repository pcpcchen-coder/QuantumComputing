# Q010 事實查核

查核日：2026-11-18。查核者：製作代理（Claude）。逐字引文見 `source-notes.md`。
方法：維基百科三頁（Bell state、Controlled NOT gate、Qiskit）由製作代理直接開啟並摘錄；學程簡報第 27 頁（如何操作量子電腦）、第 10、28 頁（量子電路入門）與兩個互動動畫的程式由製作代理讀取；程式結果由製作代理在本機實際執行。
執行環境：Python 3.13、qiskit 2.6.2、qiskit-aer 0.18.4，AerSimulator，shots=1024，seed_simulator=2026（固定種子，數字可重現）。
限制：本集只用模擬器，不連雲端、不用帳號；真機雜訊不給數字。

| # | 本集的說法（幕） | 依據 | 結論 |
|---|---|---|---|
| 1 | 模擬器是在一般電腦上照量子規則計算的程式（3） | Qiskit 頁：executing them on quantum computers or classical simulators | 相符 |
| 2 | 開源量子程式套件、免費、高效能模擬器、不需帳號（3） | Qiskit 頁：open-source；Qiskit Aer – A high‑performance simulator；本機 pip 安裝後離線執行，未登入任何服務 | 相符 |
| 3 | 瀏覽器的線路動畫可逐步跑貝爾態（3） | animations/basic-circuits.html#bell（▶ 播放、下一步、量測 1,000 次）；課綱 2026-11-18 補充素材 | 相符 |
| 4 | 線路四格：00 起點、第一顆做 H、受控反閘、一起量（4） | 簡報 basic-circuits p10；op_talk p27 程式；06_circuit.js bell | 相符 |
| 5 | H 讓第一顆變成一半零一半一的疊加（4） | basic-circuits.html caption「H 讓 q0 進入疊加」；p10 (|00⟩+|01⟩)/√2 | 相符 |
| 6 | 受控反閘：第一顆是一時翻轉第二顆（4） | Controlled NOT gate：flips the second qubit…if and only if the first qubit…is |1⟩ | 相符 |
| 7 | 兩枚獨立硬幣四種結果都會出現（5） | 獨立事件，各 1/4 | 相符 |
| 8 | 貝爾態單看一顆一半一半、兩顆永遠一樣；只量到 00、11（5） | Bell state：outcomes separately seemed random…perfectly correlated；p10、p28；op_talk p27「理想：00、11 各 50%」 | 相符 |
| 9 | 這種關聯就是糾纏（5） | Bell state：four specific maximally entangled quantum states | 相符 |
| 10 | 程式三段：QuantumCircuit(2, 2)、h／cx／measure、模擬器 1024 次（6） | `bell_simulator.py`（classroom 教材）實跑 | 相符 |
| 11 | 實跑：00 516 次、11 508 次、01、10 為 0（7） | 本機輸出 `{'00': 516, '11': 508}` | 相符（固定種子；不固定時另跑三次得 518/506、494/530、510/514） |
| 12 | 有限次數會上下跳（7） | 二項分布；1024 次的標準差約 16 次（√(1024×0.25)=16） | 相符 |
| 13 | 套件把第一顆量子位元寫在最右邊（8） | 實測 qc.x(0) 得 '01'；basic-circuits.html「q0 在最右邊」；quantumcircuit.py docstring little-endian | 相符 |
| 14 | 模擬器沒有雜訊；真機的閘和讀取錯誤會多出少量 01、10（8、12） | op_talk p27「01、10 出現 = 雜訊（閘、讀取錯誤）」；課綱常見誤解 | 相符（AerSimulator 預設不加雜訊模型） |
| 15 | 貝爾態共四種（10） | Bell state：four specific maximally entangled quantum states | 相符 |
| 16 | 先對第二顆加反閘 → 01、10；對第一顆加反閘 → 直方圖同原本，差在正負號（10） | 實跑：x(1) 得 {'10': 516, '01': 508}；x(0) 得 {'00': 524, '11': 500}；Φ⁻=(|00⟩−|11⟩)/√2；basic-circuits.html 註「Φ⁻ 和 Φ⁺ 量起來一模一樣，差在負號」 | 相符 |
| 17 | 下一堂：隱形傳態，傳狀態不傳東西（12） | academy/lessons/Q011/brief.md | 相符 |

## 課程

- 主題、學習目標、動手任務、孩子獨立改造（另外三種貝爾態）、好玩機制（解鎖成就）、作品（貝爾態截圖＋說明卡）、120 分鐘流程、驗收（模擬器沒有雜訊；真機多出 01、10）依 `academy/lessons/Q010/lesson.json` 核對。
- 課綱寫「跑 1000 shots」；程式採學程決定的 1024 次（2 的次方，常見預設）；瀏覽器動畫按鈕是 1,000 次，教材兩者並列說明。
- 課綱寫「免安裝線路編輯器（需新增）」；依 2026-11-18 補充素材以 basic-circuits.html 替代，並提供本機模擬器程式。
- 旁白不念英文：Qiskit 稱「開源量子程式套件」、CNOT 稱「受控反閘」、H 稱「阿達瑪閘」、X 稱「反閘」、Bell 稱「貝爾」；投影片上程式碼保留英文。
- 沒有課堂錄音；未虛構孩子作品或對話。
