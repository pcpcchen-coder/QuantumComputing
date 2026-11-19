# Q055 事實查核

查核日：2026-11-18。查核者：製作代理（Claude）。逐字引文見 `source-notes.md`。
方法：維基百科四頁（Superconducting quantum computing、Quantum logic gate、Controlled NOT gate、Avoided crossing）由製作代理取得 wikitext 並摘錄；學程簡報 `QC_Operation_Talk.pptx` 第 22–24 頁與 `transmon.pptx` 第 21 頁（含講者備註）以 python-pptx 讀取；對話紀錄第 4 課；互動動畫原始碼（operation 05_twoqubit.js、transmon-3d.html 第 6 章）由製作代理讀取，並以 1600×900 Chromium（swiftshader）截圖確認畫面與讀數；數字以 Python／Node 重算（`/home/user/qwork/q055calc/`，輸出附在文末）。
限制：動畫的頻率、耦合與「洩漏風險（示意）」是教學模型的值，不是特定硬體的量測；閘時間與誤差是簡報的概括數字。

| # | 本集的說法（幕） | 依據 | 結論 |
|---|---|---|---|
| 1 | 上一堂：任意旋轉都能拆成三個旋轉（1） | academy/lessons/Q054/brief.md（任意旋轉 = 三個旋轉） | 相符 |
| 2 | 只轉單獨一顆做不出糾纏，一定要有兩位元閘（1、3） | op_talk p22「單位元閘無法產生糾纏」；Wikipedia SQC「single-qubit gates combined with two-qubit gates form a universal gate set」 | 相符 |
| 3 | 受控反閘：控制是一才翻目標，是零目標不動（3） | Wikipedia Quantum logic gate（CNOT 只在第一顆是 |1⟩ 時做 NOT）；op_talk p22 | 相符 |
| 4 | 受控相位翻轉閘：只有一一加負號，其他不變，對稱不分控制與目標（3、4） | op_talk p22「CZ 兩個都是 1 時加負號（對稱）」「CZ 對稱：不分控制與目標」；checks.py：交換兩顆後矩陣不變 | 相符 |
| 5 | 負號直接量測看不出、要疊加干涉後才顯現（4） | 相位因子 −1 不改變 |11⟩ 的機率；checks.py：CZ 作用在 |++⟩ 後 Schmidt 係數 0.707、0.707（糾纏，干涉可見）；transmon.pptx p21「CZ 只把 |11⟩ 翻成負號 … 就拆不回兩顆各自的狀態」 | 相符 |
| 6 | 目標前後各加哈達瑪閘，受控相位翻轉閘變成受控反閘（4） | op_talk p22「CNOT = (I⊗H) · CZ · (I⊗H)」；checks.py 矩陣驗算 True | 相符 |
| 7 | 磁通調頻：谷歌和許多可調頻率晶片，約四十到七十奈秒（5） | op_talk p23「CZ：磁通調頻（Google 等）… 約 40–70 ns」；05_twoqubit.js desc「CZ（Google、多數可調頻架構）」 | 相符（簡報概括值，not_verified 註明） |
| 8 | 交叉共振：國際商業機器公司固定頻率晶片、只用微波、約兩百到五百奈秒（5、7） | op_talk p23「交叉共振 CR（IBM 固定頻率）… ~200–500 ns」；Wikipedia SQC（Chow 等 2011 "All-Microwave … Fixed-Frequency"） | 相符 |
| 9 | 兩條路線都要搭配單一位元修正（5、6、7） | op_talk p23「ZX(π/2) + 單位元修正 = CNOT」；05_twoqubit.js desc「其他態的單位元相位用虛擬 Z 修正掉」 | 相符 |
| 10 | 磁通脈衝把甲的頻率往下拉，讓一一靠近二零（甲在第三能階、乙在零）（6） | op_talk p23；05_twoqubit.js：E11 = f_A + f_B、E20 = 2f_A + α，f_A 從 6.0 往下到交叉點 5.25 GHz（= f_B − α） | 相符 |
| 11 | 兩能階因耦合互相排斥、不真的交叉＝迴避交叉；一一被推低、只有它多累積相位（6） | op_talk p23「能階排斥（迴避交叉）→ 只有 |11⟩ 多累積相位」；Wikipedia Avoided crossing；cz.js：下支 branch(fa,−1) < E11，zeta < 0 | 相符 |
| 12 | 調深度與時間讓相位剛好一百八十度＝負號；其他單一位元相位用虛擬繞垂直軸旋轉修正（6） | op_talk p23 備註「調整脈衝的深度和長度，讓這個額外相位剛好是 π」；05_twoqubit.js desc；Wikipedia SQC（高能階產生條件相位、以磁通調頻實現） | 相符 |
| 13 | 交叉共振：微波送到甲、頻率對準乙；乙繞水平軸轉、方向由甲決定（7） | op_talk p23「以 B 的頻率驅動 A｜B 繞 ±x 旋轉，方向取決於 A」；Wikipedia SQC 原文 | 相符 |
| 14 | 兩個方向各轉九十度、再加單一位元修正＝受控反閘（7） | op_talk p23「ZX(π/2) + 單位元修正 = CNOT」；checks.py：CNOT = e^{iπ/4}(Rz(−π/2)⊗Rx(−π/2))·exp(−iπ/4 Z⊗X) | 相符 |
| 15 | 交叉共振不必改變頻率、適合固定頻率晶片（7） | Wikipedia SQC（Chow 等 2011 標題）；對話紀錄第 4 課「固定頻率的 CR 閘」 | 相符 |
| 16 | 兩位元閘誤差通常比單位元閘高大約十倍，是最主要錯誤來源（8、12） | 課綱常見誤解；op_talk p23 備註「錯誤率也高大約 10 倍，是目前量子電腦誤差的主要來源」；05_twoqubit.js desc「錯誤率 0.1–1%，是目前誤差的主要來源」 | 相符（概括說法） |
| 17 | 太靠近交叉點或改變得太急，會留在第三能階＝洩漏（8） | 05_twoqubit.js desc「脈衝太快或太靠近交叉點，會讓狀態跑到 |20⟩（洩漏）」；op_talk p23 備註 | 相符 |
| 18 | 角色扮演規則（9） | 課綱好玩機制「角色扮演」；左右倒是代表兩個相反方向的教學約定 | 教學設計 |
| 19 | 原生閘＝硬體直接會做的閘（10） | op_talk p24 備註「每台量子電腦只會一小組『原生閘』，其他閘都要轉換成原生閘才能執行」 | 相符 |
| 20 | 國際商業機器公司較早的固定頻率處理器用交叉共振構成的閘；新一代加可調耦合器、原生閘改 CZ（10） | op_talk p24 表與備註（Eagle：ECR，基於交叉共振；Heron：可調耦合器、CZ） | 相符（not_verified：未查官方文件） |
| 21 | 谷歌用受控相位翻轉閘或交換類兩位元閘；原生閘隨世代改變、以官方文件為準（10） | op_talk p24「Google Sycamore / Willow｜CZ（或 √iSWAP 類）」「各平台原生閘依世代而異，以官方文件為準」 | 相符 |
| 22 | 120 分鐘安排（11） | 課綱 2 小時流程 | 相符 |
| 23 | 下一堂：轉譯，把邏輯線路變成硬體能執行的樣子（12） | academy/lessons/Q056/brief.md（轉譯：邏輯線路到硬體） | 相符 |

## 投影片上的數字與符號

- 第 3–4 頁：CNOT、CZ、|11⟩ → −|11⟩、CNOT＝(I⊗H)·CZ·(I⊗H) 同第 3–6 列。
- 第 5 頁「約 40–70 ns」「~200–500 ns」逐字取自 op_talk p23。
- 第 7 頁「ZX(π/2)＋修正＝CNOT」「B 繞 ±x 轉」取自 op_talk p23。
- 第 8 頁「典型 0.1–1%」取自 05_twoqubit.js desc。
- 第 10 頁「IBM Eagle：ECR」「IBM Heron：CZ＋可調耦合器」「Google：CZ 或 √iSWAP 類」取自 op_talk p24。

## 課程

- 主題、學習目標、動手任務、孩子獨立改造、好玩機制（角色扮演）、作品（兩種實現對照表）、生活技能（同一目標有不同做法）、120 分鐘流程、驗收依 `academy/lessons/Q055/lesson.json` 核對。
- 旁白不念英文：CZ 說成「受控相位翻轉閘」、CNOT 說成「受控反閘」、H 說成哈達瑪閘、A／B 說成甲／乙、|11⟩ 說成「一一」「兩顆都是一的狀態」、|20⟩ 說成「甲在第三能階、乙在零」、Google 說成谷歌、IBM 說成國際商業機器公司；交叉共振照念。投影片保留符號。
- 沒有課堂錄音；未虛構孩子作品或對話。

## 動畫展示段（demos_extra/q055.py）

- cz（op#twoqubit）：能階圖金色下支（|11⟩）、紫色上支（標 |20⟩），左下青色「迴避交叉」標籤；按執行：A 發藍光、白點沿金色線滑到交叉旁、停留、滑回（sim 截圖 +1.9／+4.9／+7.9 秒確認）；再按：只有 |11⟩ 金色箭頭從右轉到左；讀數預設 180°、19 MHz、「高」（紅）；深度 0.90 → 97°；自動找 π → 110 ns、180°、57 MHz、「低」（cz.js 與 DOM 讀數一致）。
- cr（op#twoqubit）：點「交叉共振 CR」→ 兩顆布洛赫球，左標「控制 A = |0⟩ 時的目標 B」金色箭頭、右「控制 A = |1⟩ 時的目標 B」紅色箭頭，皆指北極；執行中 A 發藍光、B 發紅光，左箭頭往左倒、右箭頭往右倒（checks.py：控制 0 → −y、控制 1 → +y），停在赤道，讀數「ZX 旋轉角 = 90°（目標 90°）」；右下插圖藍線往上到 π/2、紅線往下到 −π/2。
- case（tr#case）：關掉自動接續、按下一步五次到「⑥ 換你操作」；頻率尺 Q1 4.900、Q2 5.100、Q3 5.300；π → Q2、π → Q3 後兩顆發亮；CZ：耦合器發光、Q3 移到 5.383（= 5.100 + 0.283）、碰撞帶出現、P(|20⟩) 升到 0.93–0.99 再回 0.00，最後「180°（= −1，CZ 完成）」、Q3 回到 5.300（sim 截圖與 DOM 讀數確認）。
- op#twoqubit 用 0.25 倍速驅動（見 q055.py 說明），tr#case 無法外部驅動；旁白順序已依截圖時間安排。

## Python／Node 輸出

```
cz.js（05_twoqubit.js 模型）
init depth 0.95 Tp 59 fmin 5.269 phase 180 gap 19 leak 11.60 高
nochange depth 0.9 Tp 59 fmin 5.307 phase 97 gap 57 leak 0.02 低
auto depth 0.9 Tp 110 fmin 5.307 phase 180 gap 57 leak 0.01 低
auto depth 1 Tp 26 fmin 5.230 phase 182 gap -20 leak 30.00 高
sqrt2g 21.21 MHz

checks.py
CZ symmetric (swap)? True
CNOT == (I⊗H)CZ(I⊗H)? True
CNOT = phase*(Rz(-1.57)⊗Rx(-1.57))·ZX(π/2) phase (0.707+0.707j)
control 0 target bloch [0, -1, 0]；control 1 target bloch [0, 1, 0]
CZ|++> schmidt [0.707 0.707]
crossing fA = fB − alpha = 5.25；tr：5.100 + 0.283 = 5.383；|02⟩ 路線 Q3 = 4.817
```
