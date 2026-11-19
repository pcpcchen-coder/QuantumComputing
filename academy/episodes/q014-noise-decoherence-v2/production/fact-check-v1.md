# Q014 事實查核

查核日：2026-11-18。查核者：製作代理（Claude）。逐字引文見 `source-notes.md`。
方法：維基百科 Quantum decoherence（oldid=1384689551）與 Relaxation (NMR)（oldid=1385738005）由製作代理直接開啟並摘錄；學程簡報「超導量子電腦的核心：JJ 與微波讀取」第 5–6 頁、「量子電腦的周邊系統」第 6 頁的文字與講者備註，以及 `animations/index.html`、`animations/js/scenes/01_bloch.js`、`animations/js/core.js` 由製作代理讀取；240 mK、1/24、e⁻²⁴、4000 個閘由製作代理重新計算。
限制：本集只講直覺與量級，沒有真機量測數據；動畫的衰減時間是放慢的示意。動畫段尚未試錄。

| # | 本集的說法（幕） | 依據 | 結論 |
|---|---|---|---|
| 1 | 上一堂：格羅弗搜尋在十六個抽屜裡一輪一輪放大寶藏的機率；那時的動畫沒有雜訊（1） | academy/lessons/Q013/brief.md；09_grover.js 只做理想振幅計算（Q013 fact-check 的限制） | 相符 |
| 2 | 周圍的干擾讓疊加慢慢壞掉，叫退相干（1） | 維基：loss of quantum coherence…loss of information of a system to its environment | 相符 |
| 3 | 能量弛豫：一態自己放出能量掉回零態（2、5） | 維基 T₁：decays from the excited state |1⟩ to the ground state |0⟩；jj_talk p6「|1⟩ 自發放出能量回到 |0⟩」 | 相符 |
| 4 | 失相：赤道上的箭頭被雜訊打散、一邊轉一邊縮短（2、5、6） | jj_talk p6 講者備註「向量在赤道上轉、同時越縮越短，那就是失相」；01_bloch.js desc「雜訊使相位擴散、向量縮短」 | 相符 |
| 5 | 冷到約十毫克耳文，只比絕對零度高百分之一度（2、7） | pe_talk p6「為什麼要 10 mK？」；10 mK = 0.01 K | 相符 |
| 6 | 量子位元不是完全隔絕的孤島；資訊漏到環境，越漏越像普通的猜硬幣（3） | 維基：not perfectly isolated…coherence is shared with the environment；begins to obey classical probability rules | 相符（「猜硬幣」是比喻） |
| 7 | 超導量子電腦常見干擾：多餘的熱、電磁雜訊、材料缺陷（3、9） | pe_talk p6 熱激發、熱光子；jj_talk p6 低頻雜訊（磁通、電荷）、JJ 缺陷與準粒子；維基 Electromagnetic shielding、Better materials（defects） | 相符 |
| 8 | 布洛赫球：北極零態、南極一態、赤道一半一半（4） | jj_talk p5 | 相符 |
| 9 | 健康的量子態箭頭尖端碰到球面；箭頭變短＝失去相干性（4） | 01_bloch.js 讀數：|r| < 0.98 顯示「混態：失去相干性」，否則「純態」 | 相符 |
| 10 | 箭頭縮到球心，量測只剩一半一半（4） | 球心 z = 0 → P(1) = (1 − z)/2 = 0.5（01_bloch.js 第 95 行同一公式） | 相符 |
| 11 | 能量弛豫時，箭頭從南極回到北極那一側（5） | 01_bloch.js T1 模式 vec = (0, 0, 1 − 2e^(−t/5)) | 相符 |
| 12 | 失相時能量沒有變少（5） | Ramsey 模式 z 固定 0、P(1) 固定 0.5；維基把 T₁（loses energy）和 T₂（phase coherence）分開定義 | 相符（指單純失相；真實的 T₂ 也包含能量弛豫的貢獻，T₂ ≤ 2T₁） |
| 13 | 兩個時間：能量弛豫時間和相位相干時間，越久越好（5） | jj_talk p6 標題「T1：能量弛豫時間」「T2：相位相干時間」；維基：Extending these times is a major goal | 相符 |
| 14 | 用九十度脈衝把箭頭放到赤道，讓它繞赤道轉；拉姆齊實驗（6） | 維基：Ramsey…prepared in a superposition state and freely evolves, precessing；jj_talk p5「轉 90 度就是 π/2 脈衝，產生疊加態」 | 相符 |
| 15 | 每次轉速不同、平均起來箭頭散開變短（6） | 維基：coherence terms decay as the spread of the random phase increases；01_bloch.js desc「雜訊使相位擴散」 | 相符 |
| 16 | 失相期間得到一的機率一直一半；要等干涉才看得出來（6） | Ramsey 模式 P(1) = 0.5；維基：Ramsey…the decay of the resulting oscillation envelope yields T₂（需第二個脈衝干涉才量得到） | 相符 |
| 17 | 五吉赫的量子位元，零態到一態的能量約等於 240 mK 的熱（7） | pe_talk p6「hf ≈ 20 μeV ≈ 240 mK × kB」；重算 0.240 K | 相符 |
| 18 | 十毫克耳文時熱只剩量子位元能量的 1/24，被熱踢上去的機會幾乎是零（7） | pe_talk p6「kBT 只有 hf 的 1/24 → 熱激發 ≈ e−24」；重算 3.8×10⁻¹¹ | 相符（限制見 not_verified） |
| 19 | 先用脈衝管冷到約四克耳文，再用稀釋冷凍機降到十毫克耳文（7） | pe_talk p6「300 K → 50 K → 4 K：脈衝管」「4 K → … → 10 mK：稀釋循環」 | 相符 |
| 20 | 冷是為了讓熱雜訊遠小於量子位元的能量，不是為了跑得更快（8） | 課綱常見誤解；pe_talk p6 | 相符 |
| 21 | 經驗法則：相位相干時間 ÷ 閘時間；100 微秒 ÷ 25 奈秒 ≈ 4000 個閘（8） | jj_talk p6「可執行的操作數 ≈ T2 / 閘時間」「T2 = 100 μs、閘 = 25 ns → 約 4000 個閘」；維基：gate operations must complete before the quantum states decohere | 相符 |
| 22 | 暫停題：讀取比能量弛豫時間還久會怎樣（8；答案：讀到一半就掉下來） | jj_talk p6「讀取時間必須 ≪ T1，否則讀取途中就衰減」 | 相符 |
| 23 | 冷卻擋熱、金屬屏蔽擋外面的電磁波、更乾淨的材料減少缺陷（10） | 維基 Isolation from environment：Cryogenic cooling、Electromagnetic shielding（mu-metal or superconducting materials）、Better materials（highly pure…defects） | 相符（維基這三條標 citation needed；簡報 pe_talk p6／p7 亦有低溫、屏蔽、濾波） |
| 24 | 屏蔽能擋外面的電磁波，卻不能讓環境變冷（10） | 屏蔽的作用是阻擋外部電磁場（維基）；降溫靠冷凍機（pe_talk p6） | 相符 |
| 25 | 限制：再冷，量子態也只能撐很短的時間，計算要在壞掉前做完（12） | 維基：T₁ and T₂ together set a practical upper bound on the size of quantum circuits；jj_talk p6 | 相符 |
| 26 | 下一堂：迷你專案，量子逃脫室，整合疊加、測量、干涉、糾纏與格羅弗搜尋，設計五關（12） | academy/lessons/Q015/brief.md | 相符 |

## 動畫展示段（demos_extra/q014.py，animations/index.html#bloch）

| 說法 | 依據（js/scenes/01_bloch.js） | 結論 |
|---|---|---|
| 左邊面板有能量弛豫、拉姆齊進動、九十度脈衝的按鈕，以及失諧滑桿 | 第 55、58、62 行；#panel 在左（css/style.css 第 32 行） | 相符 |
| 按能量弛豫，箭頭立刻跳到最下面的一態 | 按鈕 → reset()，t = 0 時 vec = (0, 0, −1)（第 54–56、83–84 行） | 相符 |
| 箭頭沿縱軸往上縮、穿過球心，再指向零態那一側（不是沿球面轉） | vec 只有 z 分量；約 3.5 秒過球心，12 秒時 z ≈ 0.82 | 相符 |
| 右下小圖：曲線從一往下滑，先快後慢 | 插圖畫 P(1) = e^(−t/5)（第 64–70、95–96 行） | 相符 |
| 真實晶片：最好的能量弛豫時間約 0.1–1 毫秒；動畫是放慢的 | jj_talk p6；動畫 T1 = 5（秒） | 相符 |
| 拉姆齊進動：箭頭在赤道繞轉、往球心縮、留下往內捲的軌跡 | vec = e^(−t/6)(cos a, sin a, 0)、a = 1.2t（Δ = 0.8）；軌跡最近 600 點（第 45、80–81、92 行） | 相符 |
| 小圖是平平的線、停在 0.5；箭頭尖端數字也是 0.5 | z = 0 → P(1) = 0.50；尖端標籤 `P(1) = …`（第 98 行） | 相符 |
| 讀數的箭頭大小一路變小，出現「混態：失去相干性」 | 讀數 `|r| = …`（第 100 行） | 相符（每段句子開頭重按按鈕，避免 12 秒重來落在句中） |
| 失諧拉到零、再按一次：不轉圈但照樣縮 | Δ = 0 → a = 0，r 仍 = e^(−t/6) | 相符 |
| 九十度脈衝：箭頭停在赤道、碰著球面、讀數寫純態 | 手動 θ = 90°、φ = 270°，|r| = 1 →「（純態）」（第 62、85–87、100 行） | 相符 |

## 課程

- 主題、學習目標（T₁、T₂ 的直覺、為什麼要冷到 10 mK）、動手任務（雜訊卡，對照場景）、孩子獨立改造（防雜訊方法卡）、好玩機制（故障卡）、作品（雜訊卡牌組）、120 分鐘流程、驗收（冷不是為了跑更快）、生活技能（找出干擾來源再對症下藥）、家長準備（index.html#bloch 的 T1、Ramsey 模式）依 `academy/lessons/Q014/lesson.json` 核對。
- 旁白不念英文：T₁ 說「能量弛豫時間」、T₂ 說「相位相干時間」、Ramsey 說「拉姆齊」、mK 說「毫克耳文」、GHz 說「吉赫」、π/2 脈衝說「九十度脈衝」；投影片上保留 T1、T2、10 mK、5 GHz。
- 沒有課堂錄音；未虛構孩子作品或對話。
