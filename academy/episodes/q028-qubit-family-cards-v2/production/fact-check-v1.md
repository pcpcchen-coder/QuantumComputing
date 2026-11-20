# Q028 事實查核

查核日：2026-11-20。查核者：製作代理（Claude）。逐字引文見 `source-notes.md`。
方法：課綱 `academy/lessons/Q026、Q027、Q028、Q029`；課綱指定簡報 `slides/JJ_Microwave_Readout_Talk.pptx` p18–20，另讀同一份簡報 p16（投影片文字、表格與講者備註以 python-pptx 擷取）；動畫原始碼 `animations/index.html`、`animations/js/scenes/04_potential.js`、`animations/js/scenes/05_washboard.js`、`animations/js/core.js`、`animations/transmon-3d.html` 由製作代理讀取，讀數以頁面同一段程式在 Node 實算；維基百科 Charge qubit、Transmon、Fluxonium、Phase qubit（原始 wikitext，2026-11-20 取得）。
限制：四種量子位元的比值、頻率、非諧性是學程簡報的典型範圍（簡報註明「實際依設計而異」），不是特定晶片的量測；年份與獎項取自維基百科，未另查原始論文；本集沒有實作程式，圖鑑卡內容都來自上述來源。動畫段尚未試錄。

| # | 本集的說法（幕） | 依據 | 結論 |
|---|---|---|---|
| 1 | 上一堂：兩個約瑟夫森接面並聯成環，用磁通調整頻率（1） | Q027 brief「知道兩個 JJ 並聯成環可以用磁通調整頻率，認識甜蜜點」 | 相符 |
| 2 | 同樣是約瑟夫森接面，配上不同電路就能做出好幾種超導量子位元（1） | JJ 簡報 p18 標題「以 JJ 為核心的量子位元家族」；備註「JJ 加上不同的電路拓樸，就形成不同的超導量子位元」 | 相符 |
| 3 | 學習目標與作品：比較四位成員的結構、頻率、優點、弱點；四張圖鑑卡、理想量子位元卡（1、2） | Q028 lesson.json 學習目標、動手任務、孩子獨立改造、作品「量子位元圖鑑卡」 | 相符 |
| 4 | 四種都靠約瑟夫森接面提供不耗損能量的非線性，差別在旁邊接了什麼與比值（2、3） | JJ 簡報 p18「共同點：都靠 JJ 提供『無耗散的非線性』；差別在 EJ/EC 比值與電路拓樸」 | 相符（「無耗散」說成「不耗損能量」） |
| 5 | 沒有一種在所有指標都最好，廠商的選擇各有考量（2、8、12） | 課綱常見誤解「沒有在所有指標都最好的量子位元；廠商選擇各有考量」；p18 表各列優缺點不同 | 相符 |
| 6 | 家族表列出以接面為核心的幾種量子位元；另有超導環加三、四個接面的磁通量子位元（3） | JJ 簡報 p18 表五列；「磁通（Flux）｜超導環 + 3–4 JJ」 | 相符 |
| 7 | 電荷型也叫庫柏電子對盒子；小超導島經一個接面接出去；以小島上有沒有多一對電子分零和一（4） | p18「電荷（CPB）｜小島 + 1 JJ」；維基 Charge qubit「also known as Cooper-pair box」「presence or absence of excess Cooper pairs in the island」「tiny superconducting island coupled by a Josephson junction……to a superconducting reservoir」 | 相符 |
| 8 | 最早的超導量子位元；一九九九年實驗第一次看到它在兩個狀態間來回振盪（4） | p18「最早的超導量子位元」；維基 Charge qubit「In 1999, coherent oscillations in the charge qubit were first observed by Nakamura et al.」 | 相符 |
| 9 | 電荷型比值約一、頻率五到十吉赫、非諧性很大（4） | p18「~1｜5–10 GHz｜大」 | 相符（典型範圍） |
| 10 | 怕背景電荷；頻率隨背景電荷飄動的幅度叫電荷色散；相位相干時間約一到兩微秒（4） | p18「對電荷雜訊極敏感」；p19 備註背景電荷一跳頻率就跟著變；transmon.pptx p15 備註（Q025 已引）「電荷色散是 f01 隨背景電荷 n_g 的最大漂移量」；維基 Charge qubit「Typical T2 coherence times for a charge qubit are on the order of 1–2 μs」 | 相符（典型值） |
| 11 | 大電容型和電荷型用同一條能量公式，差別是並聯大電容，比值五十到一百；二零零七年由耶魯大學等團隊提出（5） | 維基 Transmon「both are described by the same Hamiltonian, with the only difference being the EJ/EC ratio」「large shunting capacitor」「at Yale University and Université de Sherbrooke in 2007」；p18「JJ/SQUID ∥ 大電容｜50–100」 | 相符 |
| 12 | 頻率四到六吉赫、非諧性負兩百到負三百兆赫；幾乎不怕背景電荷、結構簡單、業界主流；上一堂的可調環也常裝在它身上（5） | p18「4–6 GHz｜−200～−300 MHz｜業界主流；抗電荷雜訊、結構簡單」「JJ/SQUID」；transmon-3d 第 1 章「下端經由 SQUID（兩個約瑟夫森結）接地」 | 相符 |
| 13 | 弱點是非諧性小，脈衝太快可能漏到更高能階；最佳實驗能量弛豫時間約零點一到一毫秒（5） | 維基 Fluxonium 背景段「the transmon suffers from low anharmonicity」；transmon-3d 第 1 章「電容太大，α 太小，脈衝容易漏到 \|2⟩」；p20「0.1–1 ms｜T1（最佳實驗）」 | 相符（只引用簡報範圍，見 not_verified） |
| 14 | 超電感型：小接面並聯超電感，超電感通常是上百個較大的接面串在一起；二零零九年耶魯大學團隊提出（6） | p18「Fluxonium｜1 JJ ∥ 超電感（JJ 陣列）」；備註「這個超電感通常是由上百個大 JJ 串成的陣列」；維基 Fluxonium「first proposed……by an experimental group at Yale University led by Michel Devoret in 2009」、圖說「larger area Josephson junctions and one smaller area Josephson junction」 | 相符 |
| 15 | 頻率零點一到一吉赫、非諧性極大、能量弛豫時間可到毫秒等級；通常停在半個磁通量子，對磁通雜訊一階不敏感（6） | p18「0.1–1 GHz｜極大｜T1 可達 ms」；維基 Fluxonium「The most common operating point is the half-flux point……insensitive to flux noise at first order」「relaxation time of over 1 ms」 | 相符 |
| 16 | 也不怕背景電荷；那一大串接面讓製作複雜、難大量擴充；頻率低，閘通常較慢（6） | 維基 Fluxonium「insensitive to offset charge noise」「requires complex fabrication methods, and is therefore difficult to scale」「operating at lower frequencies usually means slower gate times」 | 相符 |
| 17 | 相位型是電流偏壓的接面，即第二十六堂的傾斜洗衣板；偏壓接近臨界電流時山谷變淺、位障變低，用最低兩個能階當零和一（7） | p18「相位（Phase）｜電流偏壓 1 JJ｜洗衣板井中能階」；p16 備註「早期的『相位量子位元』就是在接近 Ic 的偏壓下，利用井中最低的兩個能階」；維基 Phase qubit「uses the lowest two energy levels in the local minimum」；05_washboard.js 位障標籤隨偏壓變小 | 相符 |
| 18 | 比值遠大於一、頻率五到十吉赫；零到一的頻率約等於山谷裡的振動頻率，改電流就能調；電流一抖頻率也抖、狀態慢慢亂掉（7） | p18「≫ 1｜5–10 GHz」；維基 Phase qubit「E01 ≈ ħωp」「the phase qubit has a tunable energy splitting」「fluctuations in current generate fluctuations in the plasma frequency, which causes dephasing」 | 相符（「約等於」見 not_verified） |
| 19 | 一九八五年三位科學家在這種接面量到量子化能階，二零二五年得諾貝爾物理學獎；相位型現在較少用（7） | 維基 Phase qubit「first demonstrated experimentally by John Clarke, Michel Devoret and John M. Martinis in 1985, for which they were awarded the Nobel Prize in Physics in 2025」；p18「已較少使用」 | 相符 |
| 20 | 誤解：一定有一種在所有指標都最好；指標常顧此失彼（8） | 課綱常見誤解；p18 各列優缺點互異（例如大電容型抗電荷雜訊但非諧性小、超電感型非諧性極大但製作複雜） | 相符 |
| 21 | 簡報備註：幾家大公司用大電容型的變形；也有公司專門發展超電感型（8） | p18 備註「Google、IBM 都用它的變形」；維基 Fluxonium「some companies like D-Wave, Atlantic Quantum, and Qilimanjaro focused specifically on developing fluxonium-based quantum computing hardware」 | 相符（不念公司名、不評論現況） |
| 22 | 暫停題：不怕背景電荷又要很大的非諧性，先看哪一張卡（8） | 超電感型：維基 Fluxonium「insensitive to offset charge noise」「high anharmonicity」；p18「極大」；解答寫在教材 `04_解答.md` | 相符 |
| 23 | 實作：每張卡四格（結構、頻率、優點、弱點）；結構圖四種畫法；解鎖章；照比值排序（9） | 課綱動手任務、好玩機制「解鎖成就（圖鑑卡）」；p18 電路結構與比值欄 | 相符 |
| 24 | 改造：理想量子位元卡，每個優點寫出跟誰借，例如向大電容型借結構簡單、向超電感型借很大的非諧性；寫下代價（10） | 課綱孩子獨立改造；p18「結構簡單」「極大」 | 相符 |
| 25 | 120 分鐘安排（11） | lesson.json 2 小時課程流程 | 相符 |
| 26 | 下一堂：晶片怎麼做，兩個角度斜斜蒸鍍鋁，讓兩層金屬重疊出接面（12） | Q029 brief「理解 Dolan bridge 兩次斜向蒸鍍如何做出重疊的 JJ」；JJ 簡報 p21「第二次斜角蒸鍍 Al（−θ）：在橋正下方與第一層重疊」 | 相符 |

## 動畫展示段（demos_extra/q028.py）

### charge：index.html#potential（js/scenes/04_potential.js）

| 說法 | 依據 | 結論 |
|---|---|---|
| 左邊面板現在停在比值五十，也就是大電容型 | 第 13 行 ratio = 50；第 115 行滑桿顯示 50.0；第 116 行「Transmon：50」為 on；本課第 5 頁比值五十到一百 | 相符（初始狀態，不說「出現」） |
| 右下角小圖藍、紅、綠三條線是最低的三個能階，現在都是平的 | 第 118 行標題、第 124 行三色、第 69–74 行 bands 取最低三個能階；Node 實算比值 50 變化 < 0.001 | 相符 |
| 下排最左邊、寫著等於一的按鈕，換成電荷型的比值 | 第 116 行「CPB：E_J/E_C = 1」；本課第 4 頁「比值大約是一」 | 相符 |
| 藍線和紅線變成了上下起伏的波浪 | Node：藍 0～0.595、紅 1.595～4.117（頂端截在 2.6，第 122、126 行）；綠線整條貼上緣，旁白不提 | 相符（與 Q025 查核畫格一致） |
| 橫軸是背景電荷；電荷一跳能階就跟著動；這就是電荷型怕背景電荷、電荷色散很大的原因 | 第 123 行「背景電荷 n_g」；p19 備註；以「就是……原因」連接，屬解讀 | 相符 |
| 按五十回到大電容型的比值，三條線又都是平的 | 第 116 行 → rs.set(log10 50) → rebuild | 相符 |
| 同一條能量公式，只差一個比值 | 本課第 5 頁；維基 Transmon | 相符（總結） |

### phase：index.html#washboard（js/scenes/05_washboard.js）

| 說法 | 依據 | 結論 |
|---|---|---|
| 金色小球是相位粒子，停在一個山谷的底部 | 第 19–21 行金色球、標籤「相位粒子 φ」；第 15 行 phi = 0、阻尼後在谷底附近小幅振盪 | 相符（初始狀態） |
| 偏壓電流零點三零；小球右邊的位障標著一點一五 | 第 15、64 行 iB = 0.3、toFixed(2)；第 46–47、59–60 行位障標籤在所在井右側，Node：1.148 → 「1.15」 | 相符 |
| 一格一格加到零點九零，洗衣板越來越斜、山谷越來越淺，位障數字一路往下掉，最後停在零點零六 | 第 17 行 U = −cos φ − iB·φ；Node：0.50 → 0.68、0.70 → 0.31、0.90 → 0.0600；滑桿 12 格在第 2 句 0.6–8.08 秒 | 相符（變化時正在說） |
| 小球還是留在山谷裡，讀數仍寫著零電壓態 | 每格多出能量約 0.002 E_J ≪ 0.06；q026.py 同類模擬 300 次不滑出；第 115–116 行 | 相符（待試錄確認） |
| 讀數下面那行的山谷振動頻率已經從零點九八倍降到零點六六倍 | 第 117 行 ω_p(I)：0.30 → 0.98、0.90 → 0.66；「已經」 | 相符 |
| 相位型的兩面：調電流就能調頻率，電流一抖頻率也抖 | 本課第 7 頁；維基 Phase qubit；屬總結，不是畫面觀察 | 相符 |

### tradeoff：transmon-3d.html#capacitor（第 1 章大十字電容分頁）

| 說法 | 依據 | 結論 |
|---|---|---|
| 十字金屬板就是並聯的大電容 | 第 880 行「十字金屬板就是 transmon 的並聯電容 C_Σ」 | 相符 |
| 面板寫著七十七點五飛法拉、比值六十、非諧性負兩百八十三兆赫 | 第 1015 行 capC = 77.5；fillCap：「77.5 fF」「60.0」「−283 MHz」 | 相符（初始狀態） |
| 拉到二十飛法拉：十字板變細，比值十五點五，非諧性負一點三三吉赫，大了好幾倍 | 第 4168 行 sGoal 下限 0.3；Node：15.5、−1.33 GHz（約 4.7 倍） | 相符 |
| 電荷色散已經是五十三點一兆赫，原本只有一點九千赫；判斷寫著電荷雜訊主導 | Node：53.1 MHz、1.9 kHz；第 1206 行「電荷雜訊主導（接近 Cooper pair box）」 | 相符 |
| 比值太小，就往電荷型靠過去了 | 判斷文字括號「接近 Cooper pair box」= 本課第 4 頁的電荷型 | 相符（解讀畫面文字） |
| 按回到七十七點五，數字回到原來的樣子 | 第 889 行 #c1reset、第 1041 行 | 相符 |
| 非諧性和電荷色散互相拉扯，同一種設計也要取捨 | 第 1 章說明「電容太大，α 太小」與判斷三段；屬總結 | 相符 |

## 課程

- 旁白不念英文：transmon 稱「大電容型」、fluxonium 稱「超電感型」、charge qubit 稱「電荷型／庫柏電子對盒子」、phase qubit 稱「相位型」（第 3 頁說明這是今天的小名，投影片標題保留英文）；
  E_J／E_C 稱「比值」、T1 稱「能量弛豫時間」、T2 稱「相位相干時間」（沿用 Q014）、SQUID 稱「上一堂的可調環」；投影片與教材上保留 E_J、E_C、Ic、α、T1、GHz、MHz、μs。
- 旁白不念人名與公司名；諾貝爾獎只說「三位科學家」，公司只說「幾家大公司」「也有公司」。
- 沒有課堂錄音；未虛構孩子作品或量測數據。
