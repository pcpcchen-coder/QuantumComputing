# Q006 事實查核

查核日：2026-11-18。查核者：製作代理（Claude）。逐字引文見 `source-notes.md`。
方法：維基百科四頁（Wave interference、Double-slit experiment、Mach–Zehnder interferometer、Laser safety）由製作代理以 MediaWiki API 取得純文字版並逐段閱讀，修訂版號記在來源表；學程簡報（如何操作量子電腦第 37、38 頁、量子電路入門第 7–9 頁）與 3D 場景程式（`animations/js/operation/08_interference.js`、`animations/basic-circuits.html`）由製作代理讀取；P(0)=cos²(φ/2) 的數值由製作代理重算。
限制：本集不談詮釋問題，也不證明任何量子加速；「振幅」用「像箭頭」的說法，不用公式。

| # | 本集的說法（幕） | 依據 | 結論 |
|---|---|---|---|
| 1 | 波峰碰波峰疊成更高的浪；波峰碰波谷互相抵消（2、3） | Wave interference：crest meets crest → sum；crest meets trough → difference | 相符 |
| 2 | 兩個波源交會處出現幾乎不動的線（3、7） | Wave interference：two pebbles dropped in a pond, a pattern is observable；two point sources | 相符（「幾乎不動的線」即相消處） |
| 3 | 兩百多年前就用光的干涉說明光有波的性質（4） | Double-slit：Young 1801 論文、1803 演示；also: some question whether he performed a double-slit experiment | 相符；旁白刻意不說誰在哪年做了雙狹縫 |
| 4 | 雙狹縫讓光穿過兩條縫，牆上出現亮暗條紋（4） | Double-slit：interfere, producing bright and dark bands on the screen | 相符 |
| 5 | 電子一次只送一顆，累積後仍排出條紋（4） | Double-slit：Frabboni 2012 sent single electrons … build-up of a double-slit interference pattern | 相符 |
| 6 | 查出走哪一條縫，條紋不見，只剩兩條縫各自的光疊在一起（4） | Double-slit：pattern instead becomes the sum of two single-slit interference patterns | 相符 |
| 7 | 振幅像箭頭，方向相反可加成零；先加振幅再平方成機率，機率不能直接相加（5） | C p38：P(結果)=\|Σ路徑振幅\|²；G p9：古典機率只會相加、不會抵消；Wave interference：quantum interference term | 相符 |
| 8 | 零態分成兩條路，一條加相位，再合起來（6） | C p38：H → 相位 φ → H；Mach–Zehnder：simplified version of the double-slit；場景 8 模式 A | 相符 |
| 9 | 相位零度出口零最強；九十度一半一半；一百八十度出口零全暗（6） | C p38：φ=0 → 100% 得到 0、φ=180° → 100% 得到 1；cos²(45°)=0.5 | 相符 |
| 10 | 相位經干涉變成可量測的亮暗（6） | C p38：「相位本來看不見，干涉把它變成可量測的機率」 | 相符 |
| 11 | 兩支筆分開或點快，平靜的線數量會變（7） | Wave interference：pattern depends on the wavelength and on the separation of the point sources | 相符（一般規則；未實測水盆） |
| 12 | 3D 場景大圓盤把兩條路的箭頭頭尾相接；拖相位時出口零白箭頭縮短、出口一變大（8） | 08_interference.js：f0／f1 圓盤藍＋橙頭尾相接、白色總和；P(0)=cos²(φ/2) | 相符 |
| 13 | 偵測路徑後兩個出口各一半（8 的提問、教材解答） | Mach–Zehnder：detecting … both photodetectors will be hit with probability 1/2；C p38；場景「偵測路徑時：0.5」 | 相符 |
| 14 | 雷射不可直視、不可照人，由家長操作（9、11） | Laser safety：even relatively small amounts of laser light can lead to permanent eye injuries；Class 2 靠眨眼反射，刻意抑制可致傷；課綱安全提醒 | 相符 |
| 15 | 四十五度出口零較亮、一百三十五度較暗（10，教材解答） | cos²(22.5°)=0.854；cos²(67.5°)=0.146 | 相符 |
| 16 | 量子電腦不是同時試所有答案，而是安排相位讓錯的抵消、對的加強（12） | C p37：「演算法 = 安排相位，讓正確答案相長」；課綱常見誤解 | 相符（概念性說法） |

## 課程

- 主題、學習目標、動手任務（水盆、光源與場景兩條路徑）、孩子獨立改造（改變路徑相位預測亮暗）、好玩機制（科學實驗）、作品與 120 分鐘流程依 `academy/lessons/Q006/lesson.json` 核對；補充素材「簡報 G p7–9、場景 bc:interference」用在 v2 動畫展示與教材。
- 課綱的「手機光源＋梳子」：一般梳齒間距約一毫米，手機白光照過去主要看到的是影子條紋，不是乾淨的干涉條紋；教材把它當成「影子和干涉條紋有什麼不同」的討論題，不宣稱會看到干涉條紋。
- 課綱「需新增：雙狹縫／Mach–Zehnder 干涉儀場景」本集未新增；改用現有場景 8 的兩條路徑（等同 Mach–Zehnder 干涉儀的數學）說明。
- 旁白避開英文字母與人名：H 閘、Z 閘、φ、Young、Mach–Zehnder 都不念出來；投影片的「出口零」對應場景的「結果 |0⟩」。
- 沒有課堂錄音；未虛構孩子作品或對話。
