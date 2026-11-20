# Q108 事實查核

查核日：2026-11-18。查核者：製作代理（Claude）。逐字引文見 `source-notes.md`。
方法：維基百科兩頁（Shor's algorithm、Post-quantum cryptography）由製作代理讀取原始 wikitext 並摘錄；學程師生對話紀錄第 10 課、Transmon 筆記簡報第 19、23 頁、「如何操作量子電腦」簡報第 41、44 頁與兩個互動動畫的程式由製作代理讀取；週期、尖峰位置與成功次數由製作代理實際執行 `shor_lab.py`。
執行環境：Python 3.13.18，無外部套件；量測抽樣用固定亂數種子（SEED = 7），結果可重現。
限制：RSA-2048 的資源估計依學程文件與維基百科轉述，未另讀原論文；動畫的量測每次隨機，旁白不念隨機數值。

| # | 本集的說法（幕） | 依據 | 結論 |
|---|---|---|---|
| 1 | 上一課：德意志演算法、相位回踢，只問一次分出常數和平衡（1） | academy/lessons/Q107/brief.md；師生對話第 9 課 | 相符 |
| 2 | 秀爾演算法把分解問題變成找週期；三段：古典歸約、量子找週期、古典收尾（1、2） | 師生對話第 10 課學習目標「三段式流水線」；transmon-3d 第 8 章步驟 1 | 相符 |
| 3 | 秀爾在一九九四年提出（2） | Shor's algorithm 頁「developed in 1994 by … Peter Shor」 | 相符 |
| 4 | 底數和要分解的數互質；餘數序列會繞回一；繞一圈的步數叫週期（3） | 師生對話「選和 N 互質的 a … 最小週期 r 滿足 aʳ ≡ 1」；Wikipedia「a^r ≡ 1 mod N, and r is the smallest positive integer」 | 相符 |
| 5 | 週期偶數時 aʳ − 1 = (a^(r/2) − 1)(a^(r/2) + 1) 被 N 整除；gcd 通常就是因數；gcd 用輾轉相除法很快（3） | 師生對話；transmon-3d 步驟 1 body「gcd 用輾轉相除法很快」；Wikipedia「using Euclid's algorithm, we can always compute the GCD … efficiently」 | 相符 |
| 6 | 7ˣ mod 15 = 1, 7, 4, 13, 1…；r = 4；7² = 49 ≡ 4；gcd(3, 15) = 3、gcd(5, 15) = 5（4） | 師生對話表；transmon.pptx p23；QC_Operation_Talk.pptx p41；shor_lab.py 實跑 | 相符 |
| 7 | 2048 位元時週期可能大到天文數字（2²⁰⁴⁸ 量級），序列看似隨機（4） | 師生對話；transmon-3d 步驟 1 | 相符 |
| 8 | 計數暫存器 4 顆、H 後 0～15 同時存在；工作暫存器放函數值（5） | 師生對話；transmon-3d 步驟 2 | 相符 |
| 9 | 只做一次模指數，16 個函數值同時寫入，兩組暫存器糾纏；不同於伯恩斯坦—瓦齊拉尼與德意志，秀爾真的需要糾纏（5） | 師生對話「產生大量糾纏（Shor 真的需要糾纏）」；第 7、9 課「沒有用到糾纏」；transmon-3d 步驟 3「和 Deutsch、BV 不同」 | 相符 |
| 10 | 直接量只得到一組 (x, f(x))，看不出週期（5） | transmon-3d 步驟 3 body | 相符 |
| 11 | 觀念上量工作暫存器得 4 → 只剩 2、6、10、14，間隔 4，起點隨機（6） | 師生對話；transmon.pptx p23；transmon-3d 步驟 4 | 相符 |
| 12 | QFT 像稜鏡；間隔 r 的梳子 → 間隔 Q/r = 4 的尖峰；0、4、8、12 各 25%，其餘抵消；起點只改相位（6） | 師生對話；transmon-3d 步驟 5；shor_lab.py 實跑（各 25.0%） | 相符 |
| 13 | y = 12 → 3/4 → r = 4，驗算 7⁴ mod 15 = 1；y = 8 → 1/2 → 候選 2，7² mod 15 = 4 ≠ 1，改試 4；y = 0 沒資訊要重跑（7） | 師生對話；transmon-3d 步驟 7 cues；shor_lab.py post_process | 相符 |
| 14 | 真實情況用連分數（7） | Wikipedia「continued fractions algorithm to extract the period r」 | 相符 |
| 15 | QFT 約 n² 個閘；古典 FFT 約 n·2ⁿ 步，隨位元數指數增加（7） | 師生對話；transmon-3d 步驟 5 body | 相符（依學程文件） |
| 16 | r 奇數或 a^(r/2) ≡ −1（如 15 配 14）要換 a；y = 0 要重跑；動畫是小數字示範（8） | 師生對話；Wikipedia 重述步驟（r odd → step 1；g 平凡 → step 1）；課綱常見誤解 | 相符 |
| 17 | 模指數是瓶頸，閘數約位元數三次方（8） | 師生對話「閘數約 n³」；Wikipedia「Reversible circuits typically use on the order of n³ gates」 | 相符 |
| 18 | RSA-2048：2019 年估計約 2000 萬實體位元、8 小時；2025 年不到 100 萬、不到一週；前提錯誤率約 0.1% 加表面碼（8） | 師生對話表與前提；QC_Operation_Talk.pptx p44（Gidney 2025）；Wikipedia 引 Gidney & Ekerå「8 hours using 20 million noisy qubits」 | 相符（依學程文件與維基百科轉述，未讀原論文） |
| 19 | 分解 15、21 的實驗多半事先知道答案、簡化過的電路（8） | 師生對話「compiled Shor」；Wikipedia「compile the circuit using prior knowledge of the solution」 | 相符 |
| 20 | 密碼學界已開始換上抗量子標準（8） | Post-quantum cryptography 頁「NIST finalized the first three FIPS … in August 2024」；師生對話 FIPS 203/204/205 | 相符 |
| 21 | 動畫第 8 章第 8 步自由實驗：N 選 15、換 a、按一鍵執行（9） | transmon-3d.html G8STEPS[7].extra（data-n8、data-a8、#g8run） | 相符 |
| 22 | 每次量到的數不同，有時成功、有時要重跑（9） | g8Run MW／MC 用 Math.random；postProcess | 相符 |
| 23 | a = 14 一定失敗（10） | shor_lab.py 實跑：成功 0 / 20；14¹ ≡ −1 (mod 15)；動畫 postProcess：y = 0 → 重跑，y = 8 → a^(r/2) ≡ −1 | 相符 |
| 24 | 固定亂數種子跑 20 次：底數七成功 12 次、失敗 8 次都是量到零；底數十四 0 次，量到零重跑、量到八碰上負一（10） | shor_lab.py 實跑（SEED = 7） | 相符（固定種子下的一次抽樣） |
| 25 | N = 21、a = 2：週期 6 不能整除 16，尖峰糊開，部分 y 找不到週期；計數位元 5 顆時成功次數從 8 升到 13（10） | transmon-3d 第 8 步說明；shor_lab.py 實跑 | 相符（固定種子；教材程式把 r = 12 的平凡因數判為失敗） |
| 26 | 生活技能：失敗也是資訊（11） | 課綱生活技能支線 | 相符 |
| 27 | 限制：小數字示範；分解真正的公開金鑰需大規模容錯量子電腦（8、12） | 課綱常見誤解；Wikipedia「may require quantum computers with millions of qubits due to the overhead caused by quantum error correction」 | 相符 |
| 28 | 下一課：表面碼、穩定子、配對解碼（12） | academy/lessons/Q109/brief.md「表面碼——穩定子與匹配解碼」 | 相符 |

## 動畫展示段（v2）

| 段 | 說法 | 依據 | 結論 |
|---|---|---|---|
| pipeline | 取消自動接續；第二步 16 根、開始只有 0；約 5 秒後 H，16 根一樣高、金色；第三步色塊亮起標 1、7、4、13，同色同值、糾纏；第四步工作暫存器量到 4，只剩 2、6、10、14、高度 0.5，其他歸零，第 9 秒出現金色括號「間隔 r = 4」；第五步 QFT 成 0、4、8、12 四根，±0.50 金紅交替，其他抵消 | transmon-3d.html G8STEPS[1]～[4] setup／cues、g8Run、dft、phaseColor、bracket／brTag；手算 QFT：y = 4、12 的相位 e^{iπ} = −1 | 相符（全為固定腳本，無隨機） |
| op64 | 6 顆位元、0～63 共 64 根；右下小圖 7 的序列 1、7、4、13 上下起伏、每 4 格重複；自動播放：一樣高 → 四色 → 同色每隔 4 格 → 青色尖峰 0、16、32、48；64/4 = 16；第 ⑤ 步一根變白、左側面板寫出後處理；a = 4 小圖 1、4、1、4，週期 2，尖峰 0、32 | js/operation/10_shor.js（STEPS、setBars、fcol、peakLs、inset、readout、autoRun 每 1.8 秒）；style.css（#panel 在左、#inset-wrap 在右下） | 相符（量到的 y 隨機，旁白未念數值） |
| fail14 | 第 8 步，N 保留 15，a 選 14；一鍵執行 H→模指數→量測工作→QFT，只剩 0、8 兩根；量一次：0 → 沒資訊，8 → 週期 2、14 ≡ −1；字幕都以「再量一次或換 a 試試。」結尾；面板真實週期「2（14^2 mod 15 = 1）」 | transmon-3d.html g8BindFree、$("g8run")、postProcess、capShow 失敗字幕、#g8r | 相符（量到 0 或 8 隨機，旁白兩種都描述，未念出本次數值） |

## 課程

- 主題、學習目標、動手任務（N = 15 試三個 a，記錄週期與分解結果）、孩子獨立改造（試會失敗的 a，說明為什麼要重試）、好玩機制（Boss 戰，旁白稱「魔王關」）、作品（Shor 實驗紀錄）、生活技能、120 分鐘流程、驗收與常見誤解（小數字示範；分解真正的 RSA 需要大規模容錯量子電腦）依 `academy/lessons/Q108/lesson.json` 核對。
- 課綱列的 transmon.pptx p23 確為 Shor 頁（第 19 頁十二章一覽寫 p22，以實際內容為準）；QC_Operation_Talk.pptx p41 確為 Shor 頁。
- 旁白不念英文與縮寫：Shor 念「秀爾」、QFT 念「量子傅立葉轉換」、gcd 念「最大公因數」、mod 15 念「除以十五的餘數」、a 念「底數」、N 念「要分解的數」、r 念「週期」、y 念「量到的數」、RSA 念「公開金鑰」、H 念「哈達瑪閘」；投影片上保留符號。
- 課綱屬師生對話型；未虛構孩子作品、課堂錄音或對話。
- 發現：transmon-3d.html postProcess 未排除 a^(r/2) ≡ 1 的倍數週期（N = 21、Q = 32 偶發「21 = 21 × 1」顯示成功）。本集旁白與動畫段均未觸及；已記入 not_verified 與教材「誠實說明」，未修改動畫。
