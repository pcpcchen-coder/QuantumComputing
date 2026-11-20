# Q063 事實查核

查核日：2026-11-18。查核者：製作代理（Claude）。逐字引文見 `source-notes.md`。
方法：維基百科 Grover's algorithm、Quantum supremacy（2026-11-18 由製作代理取得 wikitext；API 查 revid 時遭限流，未取得版本號）與 Shor's algorithm（revid 1384103273）摘錄；學程簡報 `QC_Operation_Talk.pptx` 第 36–37、42–45 頁（含講者備註）以 python-pptx 讀取；互動動畫 operation.html（grover）與 transmon-3d.html（第 8 章）原始碼由製作代理讀取，並以 1600×900 Chromium（swiftshader）截圖確認（`/home/user/qwork/q063shots/`）；所有數字以 Python 重算（`/home/user/qwork/q063calc/checks.py`，輸出附在文末；格羅弗部分照抄 09_grover.js 的 Oracle／擴散計算）。
限制：「十的三十五次方、十的十次方」是略去常數的示意量級；交叉點與硬體速度只做定性說明，教材裡的數字例子明確標成假設。

| # | 本集的說法（幕） | 依據 | 結論 |
|---|---|---|---|
| 1 | 上一堂用秀爾演算法分解十五和二十一（1） | academy/lessons/Q062/brief.md | 相符 |
| 2 | 三種等級：指數級、平方級、沒有加速；另有「未定」一格（2、4） | 課綱學習目標；op_talk p42 表格「超多項式（指數級）／指數級／平方」；p44「未定」「啟發式／平方」「實用優勢尚未確立」 | 相符 |
| 3 | 誤解：幾十顆量子位元同時試完所有答案；量測只拿到一個隨機結果，沒有干涉等於亂猜（3） | op_talk p36「計算確實作用在 2ⁿ 個振幅上，但量測只得到其中 1 個隨機結果；沒有干涉，等於隨機猜」 | 相符 |
| 4 | 只有具備特殊結構的問題才有加速（3） | op_talk p36「只有特定結構的問題有加速」；p45 結論「有可利用的數學或物理結構」 | 相符 |
| 5 | 配方：疊加 → 安排相位 → 干涉讓錯的答案抵消 → 量測（3） | op_talk p37「量子演算法的配方：疊加（展開所有可能）→ 用問題結構安排相位 → 干涉（集中到答案）→ 量測」 | 相符 |
| 6 | 指數級例子：分解質因數、模擬分子；平方級：無結構搜尋、蒙地卡羅估計（4） | op_talk p42 表格；p44「化學、材料、藥物…指數級（多數）」 | 相符 |
| 7 | 沒有已知加速：加減乘除、排序、文書處理（4） | op_talk p45「加減乘除、排序、資料庫查詢、渲染、文書：沒有已知的量子加速」 | 相符 |
| 8 | 未定：量子機器學習、最佳化，仍在研究（4） | op_talk p44「機器學習…未定…仍在研究」「最佳化…實用優勢尚未確立」 | 相符（見 not_verified） |
| 9 | 一百萬個抽屜，古典平均打開五十萬個；格羅弗約七百八十五輪 = √10⁶ × 約 0.785（5） | op 場景 desc「N = 100 萬時，古典平均 50 萬次，Grover 約 785 次」；Wikipedia「r ≈ π√N/4」；checks.out `(pi/4)sqrt(N)= 785.398`、`pi/4= 0.785` | 相符 |
| 10 | 抽屜多一百倍，古典多一百倍，格羅弗只多十倍（5） | √100 = 10（checks.out） | 相符 |
| 11 | 量子每一步比較慢，問題要非常大才划算（5） | op_talk p42「平方加速…容易被量子閘較慢、錯誤更正的開銷吃掉」；Wikipedia「the quadratic speedup achieved is too modest to overcome the large overhead of near-term quantum computers」 | 相符 |
| 12 | 分解 2048 位元：古典最好的方法約 10³⁵ 量級；秀爾約位元數三次方、約 10¹⁰；示意量級（6） | op_talk p42 講者備註「古典曲線在 2048 位元時大約是 10 的 35 次方等級，量子大約是 10 的 10 次方等級——這張圖只是示意趨勢，常數都略去了」；checks.out 一般數域篩法 L 值 `10^35.2`、`2048^3 = 8.59e+09 ~10^9.93`；Quantum supremacy「Õ(n³)」 | 相符 |
| 13 | 指數級是本質上的差別（6） | op_talk p42 講者備註「指數級加速是質的差別」 | 相符 |
| 14 | 精確模擬要存 2ⁿ 個複數、每個 16 bytes；三十顆約十六吉位元組；每多十顆大約一千倍；五十顆超過頂級超級電腦總記憶體（7） | op_talk p43「2ⁿ 個複數 × 16 bytes」「~50 個量子位元就超過最大超級電腦的記憶體」；checks.out 30 顆 16 GiB、40 顆 17.6 TB、50 顆 18 PB；2¹⁰ = 1024 | 相符 |
| 15 | 糾纏不多的線路有古典捷徑，量子優勢需要大量糾纏（7） | op_talk p43「張量網路、Clifford 模擬等方法可處理低糾纏或特殊閘的線路 → 量子優勢需要高糾纏 + 非 Clifford 閘」 | 相符（旁白只講糾纏，未講非 Clifford 閘） |
| 16 | 輸入：一百萬筆約一百萬步；沒有實用的量子隨機存取記憶體（8、12） | op_talk p45「把 N 筆資料載入量子態通常要 ~N 步；沒有實用的 QRAM」；課綱常見誤解；Wikipedia Grover「Reading a full database item by item… may take a lot longer than Grover's search」 | 相符 |
| 17 | 輸出：幾顆量子位元只能讀出幾個零或一（8） | op_talk p45「n 個量子位元只能讀出 n 位元」 | 相符 |
| 18 | 小問題：量子閘慢又要錯誤更正，一般電腦更快（8） | op_talk p45「量子閘 ~100 ns、錯誤更正開銷大；問題不夠大時古典更快」 | 相符 |
| 19 | 最適合：輸入小、計算難、輸出小；分解質因數輸入一個數、輸出兩個因數（8） | op_talk p45 結論與講者備註「輸入是一個數字，輸出是兩個數字，中間的計算極難」 | 相符 |
| 20 | 2019 年宣稱兩百秒做完超級電腦要一萬年的工作；對手說最佳化後兩天半（9） | Wikipedia Quantum supremacy「200 seconds that would take a supercomputer about 10,000 years」「IBM contended… could be performed in just 2.5 days」；op_talk p43「後續古典演算法大幅追近」 | 相符（兩天半為 IBM 的估計） |
| 21 | 要算總時間：重複量測次數、錯誤更正開銷、資料載入（10） | op_talk p42「實際比較要算總時間：shots、錯誤更正、資料載入」 | 相符 |
| 22 | 120 分鐘安排（11） | 課綱 2 小時流程 | 相符 |
| 23 | 下一堂：模組專題，在模擬器跑我的線路（12） | academy/lessons/Q064/brief.md | 相符 |

## 投影片上的數字與符號

- 第 5 頁 50 萬次、785 輪、「N 多百倍，輪數只多十倍」見第 9–10 列；第 6 頁 10³⁵、n³、10¹⁰ 見第 12 列；第 7 頁 16 bytes、30 顆 16 GB、40 顆 16 TB、50 顆 18 PB（依簡報第 43 頁講者備註的寫法；精確值 16 GiB、17.6 TB／16 TiB、18 PB）見第 14 列；第 8 頁「載入 N 筆約 N 步」「n 顆只讀出 n 位元」「閘約 100 ns」「QRAM」見第 16–18 列。

## 課程

- 主題、學習目標、動手任務（12 個問題排進加速等級表）、孩子獨立改造（判斷新聞）、好玩機制（工程答辯）、作品（加速等級表）、生活技能（量化比較）、120 分鐘流程、驗收與常見誤解依 `academy/lessons/Q063/lesson.json` 核對。
- 旁白不念英文：Grover 念格羅弗、Shor 念秀爾演算法、QRAM 念「量子隨機存取記憶體」、GB 念吉位元組；投影片保留符號。
- 沒有課堂錄音；未虛構孩子作品或對話。

## 動畫展示段（demos_extra/q063.py）

- scale（op#grover，after 5）：滑桿「量子位元數 n」（09_grover.js 第 44 行）設 2、4、6；讀數（第 89–90 行）截圖 n2／n4／n6：「N = 4…最佳輪數 ≈ (π/4)√N ≈ 1　古典平均要查 2 次」「N = 16…≈ 3…8 次」「N = 64…≈ 6…32 次」。checks.out 以同公式（Math.round(π/(4θ) − 0.5)）重算一致。4 → 64 是十六倍，古典 2 → 32 也是十六倍，量子 1 → 6。
- exp（tr#shor，after 6）：#g8auto 關掉（transmon-3d.html 第 963 行）後，#g8steps 第 3、5、6 顆按鈕（第 1118–1119 行由 G8STEPS 產生）。截圖 tr3a：右側標題「③ 模指數：一次算出所有 f(x)，產生糾纏」，說明「這一步是整個演算法最花資源的部分…閘數約 n³」；看板「（可逆的模乘法電路，約 n³ 個閘）」。tr5a／tr5b：右側最後一段「只要約 n² 個閘；古典 FFT 處理 2ⁿ 個點要約 n・2ⁿ 步。指數級加速就來自這裡。」。tr6a：步驟 6 的 setup 直接把長條設成 QFT 後狀態，0、4、8、12 四根 ±0.50（金、紅），其他貼平。
- output（op#grover，after 8）：新頁面 n = 6 時答案為 11（mark 預設 11）；「② Oracle」「③ 擴散」交替六次（第 48–49 行，同步計算）後讀數「第 6 輪」「答案的機率 P = 0.997」（checks.out 0.9966）；其他振幅為負、柱子貼平呈藍色（第 38 行顏色規則）。「測量」用 Math.random 固定 0.5 → 測量結果 11（checks.out `seeded measure -> 11`；截圖 meas.png 讀數「測量結果：… ✓ 找到了」）。

## Python 輸出（checks.out）

```
Grover N=1e6: classical avg 500000.0  (pi/4)sqrt(N)= 785.3981633974482
sqrt(100)= 10.0  pi/4= 0.7853981633974483
n=2 N=4 kOpt=1 classical=2 P_after_k=1.0000 others=0.0000 other_amp_sign=pos
n=3 N=8 kOpt=2 classical=4 P_after_k=0.9453 others=0.0078 other_amp_sign=neg
n=4 N=16 kOpt=3 classical=8 P_after_k=0.9613 others=0.0026 other_amp_sign=neg
n=5 N=32 kOpt=4 classical=16 P_after_k=0.9992 others=0.0000 other_amp_sign=neg
n=6 N=64 kOpt=6 classical=32 P_after_k=0.9966 others=0.0001 other_amp_sign=neg
N 4->64 ratio 16.0  classical 2->32 16.0  quantum 1->6
seeded measure -> 11
GNFS L ~ 10^35.2  n^3 = 8.59e+09 ~10^9.93
30 qubits 17179869184 bytes = 17.2 GB(1e9) = 16 GiB  TB 0.0172  PB 1.72e-05
40 qubits 17592186044416 bytes = 1.76e+04 GB(1e9) = 1.64e+04 GiB  TB 17.6  PB 0.0176
50 qubits 18014398509481984 bytes = 1.8e+07 GB(1e9) = 1.68e+07 GiB  TB 1.8e+04  PB 18
load 1000000 + grover 785 >= classical avg 500000
crossover sqrtN=1.571e+06 N=2.47e+12
N=1e+06 classical 0.0005 s  grover 0.785 s
N=1e+12 classical 500 s  grover 785 s
N=1e+14 classical 5e+04 s  grover 7.85e+03 s
2^128 sqrt = 2^64 True
QFT n^2 16  FFT n*2^n 64
n=50 QFT n^2 2500  FFT n2^n 5.63e+16
```
