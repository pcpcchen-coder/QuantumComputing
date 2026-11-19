# Q113 事實查核

查核日：2026-11-19（檔頭 CHECKED 依派工統一寫 2026-11-18）。查核者：製作代理（Claude）。逐字引文見 `source-notes.md`。
方法：維基百科三頁（Quantum circuit、Quantum logic gate、Born rule）由製作代理取得原始 wikitext 並摘錄；學程簡報 basic-circuits.pptx 第 2–4 頁（含原始稿 slides/reports/basic-circuits.js）與互動動畫 basic-circuits.html 的程式由製作代理讀取，動畫畫面以 Playwright 實拍確認；程式結果由製作代理在本機實際執行。
執行環境：Python 3.13.18（read_order.py，只用標準函式庫）；Qiskit 2.6.2（qiskit_check.py，StatevectorSampler seed=2026）。
限制：本集只講約定與閘的符號，不完整示範任何一個範例（留給 Q114–Q121）；沒有隨機數值念進旁白（量測一千次只說「大約各一半」；零一、一零為確定結果）。

| # | 本集的說法（幕） | 依據 | 結論 |
|---|---|---|---|
| 1 | 新模組用八個量子電路範例，從一顆位元的疊加走到格羅弗搜尋（1、3） | 課綱 QM08 模組名稱；簡報第 2 頁 | 相符 |
| 2 | 前兩個一顆位元講疊加和干涉；第三、四講糾纏；第五個隱形傳態；兩個查一次的演算法；最後格羅弗用上疊加、干涉、正負號（3） | 簡報第 2 頁與備註 | 相符 |
| 3 | 接下來八堂課一堂一個範例（3） | academy/lessons/Q114–Q121 brief 標題（範例 1–8） | 相符 |
| 4 | 線路圖由左往右，橫軸是時間；橫線是量子位元，不是真的電線（4） | Quantum circuit：horizontal axis is time…left…right；Horizontal lines are qubits；usually not physical cables | 相符 |
| 5 | 起點零態、方塊是閘、最右邊儀表是量測（4） | basic-circuits.html 電路圖（`|0⟩` 標籤、閘方塊、量測錶）；Quantum circuit：operations…such as measurements or gates | 相符 |
| 6 | 同一欄的閘同一拍一起做；第九堂的樂譜比喻（4） | 動畫同一 cols 的閘同一步作用（applyOp 依 cols）；Q009 課名「量子線路像樂譜」 | 相符 |
| 7 | 編號從零開始；編號零在圖上最上面，字串裡最右邊；零一 = 編號一是零、編號零是一（5） | 簡報第 3 頁；basic-circuits.html 頁首；read_order.py、qiskit_check.py 實跑 X(q0) → 01 | 相符 |
| 8 | 常用的開源量子程式套件也這樣寫；換工具順序可能相反（5、12） | Qiskit 實跑；Qiskit 原始碼稱其為 little-endian convention 並提供 reverse_bits 轉成 big-endian；課綱常見誤解 | 相符（其他工具未逐一核對，只說「可能」） |
| 9 | 每種結果一個振幅，畫成柱子，往上正、往下負（6） | 簡報第 3 頁；動畫「柱子往上是正振幅、往下是負振幅」 | 相符 |
| 10 | 機率 = 振幅自己乘自己；0.707² ≈ 0.5；負號量不到（6） | Born rule：probability is equal to the amplitude-squared；0.707² = 0.4998；簡報第 3 頁「負號量不到」 | 相符（本課振幅皆為實數） |
| 11 | 動畫藍正、橘負；簡報金色正、紅色負（6） | 動畫 CSS `--pos #1D6A8B`、`--neg #B65C12` 與圖例；簡報第 3 頁文字 | 相符（深色主題為淺藍／淺橘，仍是藍正橘負） |
| 12 | 哈達瑪閘把零態變成各一半的疊加（7） | Quantum logic gate：Hadamard maps |0⟩ ↦ (|0⟩+|1⟩)/√2；實跑 +0.707、50% | 相符 |
| 13 | 翻轉閘是量子版的「反」，零和一對調；相位翻轉閘零態不變、一態加負號（7） | Quantum logic gate：Pauli-X…NOT gate…bit-flip；Pauli Z…phase-flip；實跑 | 相符 |
| 14 | 三種都是布洛赫球上轉半圈，轉軸不同（7） | Quantum logic gate：X、Z rotation by π；Hadamard rotation of π about (x̂+ẑ)/√2；簡報第 4 頁備註 | 相符 |
| 15 | 動畫裡 H 藍、X 酒紅、Z 紫（7、動畫段） | basic-circuits.html CSS `--h #1D6A8B`、`--x #A23B5C`、`--z #7348A3`；實拍 | 相符 |
| 16 | 受控反閘：實心點是控制、圓圈加號是目標；控制是一才翻轉目標（8） | Quantum logic gate：performs the NOT operation on the second qubit only when the first qubit is |1⟩；動畫 CNOT 畫法；實跑 CX | 相符 |
| 17 | 閘表還列了受控相位翻轉閘與可轉任意角度的旋轉閘（8） | 簡報第 4 頁原始稿：CZ／CCZ、Ry(θ) | 相符 |
| 18 | 只翻零號 → 零一；只翻一號 → 一零，和動畫一樣（10） | read_order.py、qiskit_check.py 實跑；動畫實拍 |ψ⟩ = |01⟩、|10⟩ | 相符 |
| 19 | 120 分鐘流程、生活技能「先統一規則再溝通」（11） | 課綱 | 相符 |
| 20 | 下一堂：範例一，疊加，量子硬幣與兩種疊加態（12） | academy/lessons/Q114/brief.md「範例 1：疊加——量子硬幣與 |+⟩、|−⟩」 | 相符 |

## 動畫展示段（demos_extra/q113.py）

| 段 | 說法 | 依據（實拍） | 結論 |
|---|---|---|---|
| read | 左邊編號零、零態出發、藍色哈達瑪閘、右邊量測；虛線從閘左邊走到右邊；柱子一根變兩根一樣高；量一千次約各半 | #superposition 實拍 a0／a1／a2 | 相符（次數隨機，不念數值） |
| order | 上面編號零、下面編號一；第二個選項翻轉閘在編號零的線上；升起零一、量一千次全是零一；第三個選項變一零；後面淡色閘今天不按 | #bell 選 Φ⁻／Ψ⁺ 實拍；`.future` 淡色 | 相符 |
| zgate | 藍色哈達瑪閘、紫色相位翻轉閘；做完 H 兩根藍柱一樣高；做完 Z 一的柱子翻下變橘色負振幅；機率仍各 50% | #interference 實拍 c1／c2 | 相符 |

## 課程

- 主題、學習目標、動手任務、孩子獨立改造、好玩機制（臨摹挑戰）、作品（讀圖約定卡）、120 分鐘流程、驗收（位元順序在不同工具可能相反）依 `academy/lessons/Q113/lesson.json` 核對。
- 課綱素材寫簡報 p2–4、家長準備寫 p3–4：內容實際在第 2（地圖）、3（約定）、4（閘表）頁，頁碼無誤。
- 課綱「對象與上課方式」寫「逐步播放振幅長條、量測 1000 次，再用本機 Qiskit 模擬器重現」：教材提供 qiskit_check.py（選用，pip install qiskit）與免安裝的 read_order.py。
- 旁白不念英文：q0 念「編號零」、H 念「哈達瑪閘」、X「翻轉閘」、Z「相位翻轉閘」、CNOT「受控反閘」、CZ「受控相位翻轉閘」、Grover「格羅弗」、Qiskit 稱「開源量子程式套件」；投影片保留符號。
- 沒有課堂錄音；未虛構孩子作品或對話。
