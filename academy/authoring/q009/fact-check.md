# Q009 事實查核

查核日：2026-11-18。查核者：製作代理（Claude）。逐字引文見 `source-notes.md`。
方法：維基百科 Quantum circuit、Quantum logic gate 兩頁由製作代理開啟並摘錄逐字引文；學程簡報（QC_Operation_Talk 第 25 頁、basic-circuits 第 3、4 頁）與 3D 場景程式（animations/js/operation/06_circuit.js、animations/basic-circuits.html）由製作代理讀取；H–Z–H、Z–H–H 的結果以手算並在 classroom.py 中以 2×2 矩陣重算。
限制：「樂譜」是比喻；本集不談雙線古典位元、受控閘細節（Q010 才做 Bell 態）。

| # | 本集的說法（幕） | 依據 | 結論 |
|---|---|---|---|
| 1 | 一條橫線代表一個量子位元（2、3） | Quantum circuit：Horizontal lines are qubits；Quantum logic gate：single lines are qubits；C p25 | 相符 |
| 2 | 橫的方向是時間，由左往右讀（2、3） | Quantum circuit：horizontal axis is time, starting at the left；C p25 | 相符 |
| 3 | 方塊是量子閘；儀表是測量（2） | C p25「方塊＝單位元閘」「M／儀表＝量測」；Quantum logic gate 的測量線路符號圖說 | 相符 |
| 4 | 每條線一開始習慣上是狀態零（3） | Quantum logic gate：register … all initialized to |0⟩；basic-circuits.html 每條線左端標 |0⟩；06_circuit.js「初始狀態：所有量子位元都是 |0⟩」 | 相符（慣例） |
| 5 | H 把北極轉到赤道；Z 繞赤道轉半圈；第二個 H 轉到南極；測量一定得到一（4） | G p4：H、Z 的作用；basic-circuits.html 干涉範例「H·Z·H = X」「100% 是 1」；06_circuit.js interf 說明 | 相符（理想情況） |
| 6 | 同一欄的閘可以同時執行（5） | C p25「同一欄的閘可同時執行」 | 相符 |
| 7 | 同一條線上的閘順序不能隨便交換（6） | Quantum logic gate：order … reversed when multiplying（乘積和順序有關）；課綱常見誤解 | 相符 |
| 8 | Z–H–H 一定得到零（6） | Z|0⟩=|0⟩，H·H=I（G p4；basic-circuits.html「H·H 等於什麼都沒做」） | 相符 |
| 9 | X 接測量一定得一；H 接測量一半一半（7） | G p4：X 把 |0⟩ 翻成 |1⟩；H 產生等量疊加 | 相符 |
| 10 | 3D 場景可以單步執行，執行中的閘發光，下方柱子跟著變；量測欄跑一千次（8） | 06_circuit.js：單步、emissiveIntensity、AmpBars、sample() 1000 shots | 相符 |
| 11 | 下一堂寫第一個量子程式：貝爾態（12） | academy/lessons/Q010 課綱 | 相符 |

## 課程

- 主題、學習目標、動手任務（臨摹 3 條線路並說出箭頭怎麼變）、孩子獨立改造（3 步線路請爸爸預測）、好玩機制（臨摹挑戰）、作品（手繪 3 條線路）、120 分鐘流程與常見誤解依 `academy/lessons/Q009/lesson.json` 核對。
- 旁白把 H、X、Z 說成哈達瑪閘、翻轉閘、相位翻轉閘，避免英文字母；投影片保留符號。
- 沒有課堂錄音；未虛構孩子作品或對話。
