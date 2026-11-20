# Q043 事實查核

查核日：2026-11-18。查核者：製作代理（Claude）。逐字引文見 `source-notes.md`。
方法：維基百科 Dilution refrigerator 頁的原始碼（wikitext，2026-11-18 讀取）由製作代理直接開啟並摘錄；學程簡報 `slides/QC_Peripheral_Systems_Talk.pptx` 第 8–11 頁與講者備註、動畫程式 `animations/js/peripherals/01_overview.js`、`03_dilution.js`、`common.js` 由製作代理讀取；所有 Q̇ = 84ṅT² 的數字由製作代理用 Python 重算。
限制：Q̇ = 84ṅT² 是理想值，實際機台低於理想值（動畫讀數亦註明）；本集只用它算趨勢，不當成某台機器的規格。

## Python 驗算

```python
Q = lambda T, n=0.5e-3: 84 * n * T**2      # W；T 用 K，n 用 mol/s
# 100 mK → 420.0 μW；50 mK → 105.0 μW；40 mK → 67.2 μW；30 mK → 37.8 μW
# 20 mK → 16.8 μW；10 mK → 4.2 μW；5 mK → 1.05 μW
# Q(0.01)/Q(0.02) = 0.25（溫度減半剩 1/4）；Q(0.1)/Q(0.01) = 100
T_bal = lambda load, n=0.5e-3: (load / (84 * n)) ** 0.5
# 10 μW → 15.43 mK；40 μW → 30.86 mK（熱負載 ×4 → 溫度 ×2）
# ṅ = 1.2 mmol/s、10 μW → 9.96 mK；20 mK 時 40.3 μW
```

| # | 本集的說法（幕） | 依據 | 結論 |
|---|---|---|---|
| 1 | 脈衝管把冷凍機冷到大約三克耳文（1） | 簡報 p8；02_pulsetube.js「二級冷端 ~3 K」；03_dilution.js「脈衝管只能到約 3 K」 | 相符 |
| 2 | 量子晶片要十毫克耳文左右（1） | 03_dilution.js 標題「從 4 K 到 10 mK」、「混合腔 MXC ~10 mK」；簡報 p9 備註 | 相符 |
| 3 | 氦四常見、氦三稀少昂貴，氦三比較輕（3） | 簡報 p11「³He：最昂貴的耗材」「供應有限」；質量數 3 < 4 | 相符 |
| 4 | 約 0.87 K 以下混合液自己分成兩層（3） | 03_dilution.js desc「低於 0.87 K 時分成兩相」；簡報 p9 備註「在 0.87 K 以下會自動分成兩相」 | 相符 |
| 5 | 上層幾乎全是氦三（濃相），下層是溶在氦四裡的稀相，接近絕對零度仍有 6.6 %（3） | Wikipedia：concentrated phase is essentially pure ³He…dilute phase contains about 6.6% ³He；簡報 p9 備註「即使到絕對零度…6.6%」；場景濃相在上 | 相符 |
| 6 | 四站：4 K 板凝結、熱交換器被回流冷液體預冷、混合腔越過界面溶入稀相吸熱、蒸餾室蒸發被室溫幫浦抽走淨化後送回（4） | 簡報 p9 五步（凝結、預冷、溶解、蒸發、抽回）；03_dilution.js desc ①–④；Wikipedia counterflow heat exchangers、pumps at room temperature | 相符（第五步「抽回」併入第四站一起說） |
| 7 | 蒸餾室加熱到一克耳文以下，氦三比氦四容易蒸發（4） | 場景「Still ~0.8 K 加熱 → ³He 優先蒸發」；Wikipedia：³He has a much higher partial pressure than ⁴He at 500–700 mK；Heat is supplied to the still | 相符（兩來源溫度不同，旁白只說一克耳文以下） |
| 8 | 氦三越過界面溶入稀相需要吸熱，能量從周圍拿走（5） | Wikipedia：moving the ³He through the phase boundary is endothermic and removes heat from the mixing chamber environment | 相符 |
| 9 | 流汗蒸發帶走熱，用來類比（5） | 蒸發吸熱為常識；簡報 p9 備註「就像液體蒸發需要吸熱一樣，這個溶解過程也要吸熱」 | 相符（類比，已在 not_verified 註明不是同一過程） |
| 10 | 晶片的熱一路傳到混合腔，混合腔最冷（5） | 03_dilution.js「熱流：晶片 → 樣品盒 → 支架 → MXC 板 → 混合液」；Wikipedia：mixing chamber, the coldest area of the device | 相符 |
| 11 | Q̇ = 84 × 循環率 × 溫度平方；循環率 mol/s、溫度 K、功率 W（6） | Wikipedia：Q̇m [W] = 84 (ṅ3 [mol/s]) (T [K])²；簡報 p9 | 相符 |
| 12 | 0.5 mmol/s = 0.0005 mol/s（7） | 換算 | 相符 |
| 13 | 100 mK 約 420 μW；20 mK 約 17 μW；10 mK 4.2 μW；少一百倍（7） | Python：420.0、16.8、4.2；420/4.2 = 100；簡報 p9「20 mK 時 ~17 μW、100 mK 時 ~420 μW」 | 相符 |
| 14 | 溫度減半，功率剩 1/4（8、10） | Python：Q(10 mK)/Q(20 mK) = 0.25；簡報 p10 | 相符 |
| 15 | 停在冷卻功率等於熱負載的溫度；熱負載 ×4 → 溫度 ×2（8） | 03_dilution.js 平衡溫度 T = √(Q̇/84ṅ)；簡報 p10「熱負載多 4 倍 → 基溫升高 2 倍」；Python 15.43 → 30.86 mK | 相符 |
| 16 | 20 mK → 10 mK：17 μW 變成約 4.2 μW（8，暫停題；答案在教材） | Python | 相符 |
| 17 | 單位換算：mK ÷ 1000、mmol ÷ 1000、W → μW（9） | 單位定義 | 相符 |
| 18 | 40→20、20→10、10→5 mK 都剩 1/4（10） | Python：67.2→16.8、16.8→4.2、4.2→1.05 μW | 相符 |
| 19 | 限制：越冷越難冷；要把熱擋在上面幾層（12） | 課綱常見誤解；簡報 p10「把熱負載擋在上層，比追求更大冷卻功率有效」 | 相符 |
| 20 | 下一堂：降溫一次要幾天，降溫時間軸（12） | academy/lessons/Q044/brief.md | 相符 |

## 動畫展示段（demos_extra/q043.py）

| 段 | 說法 | 依據（原始碼） | 結論 |
|---|---|---|---|
| ghs | 「只看冷卻相關」按鈕；脈衝管氦氣、冷卻水、真空按鈕可關；混合氣循環是紫色 | 01_overview.js:75–85（names、只看冷卻相關）、:54–57（mix 顏色 0xc58bff／0xe0b8ff） | 相符 |
| ghs | 粗管從冷凍機頂抽到氣體處理系統，細管送回 | 01_overview.js:54（radius 0.07，從冷凍機頂 y 3.38 到 GHS）、:55（radius 0.035，GHS → 冷凍機頂） | 相符 |
| ghs | 旁邊連著儲存槽，停機時收回 | 01_overview.js:33–34、:56（GHS → 儲存槽）；簡報 p11「停機時儲存 ³He/⁴He」 | 相符 |
| cycle | 粒子是 ³He，室溫紅色往下變藍 | 03_dilution.js:47、:132（App.tempColor）；common.js:33–36（300 K 色相 0 紅、8 mK 色相 0.66 藍）；02_pulsetube.js「紅 300 K → 藍 3 K」 | 相符 |
| cycle | 沿螺旋熱交換器往下、濃相在上、越界面閃光 | 03_dilution.js:32–35（helix）、:26–30（濃相 y 1.0 在稀相 y 0.4 之上、界面 0xffd28a）、:133（越過 lens[8] 時閃光 0xffd28a） | 相符 |
| cycle | 稀相往上回到加熱環（蒸餾室）蒸發、頂端抽走 | 03_dilution.js:22–23（加熱環 0xff7a59 自發光、Still 標籤）、:44–45（路徑回 Still、上到 y 9）、:52 | 相符 |
| cycle | 循環率拉大 → 跑得更快、加熱環更亮 | 03_dilution.js:113（滑桿）、:127（速度 0.55 + 0.9ṅ）、:137（亮度 0.5 + 0.4ṅ） | 相符 |
| balance | 右下小圖：青色冷卻功率曲線、橘紅虛線熱負載、交點黃點 | 03_dilution.js:116–124（#38c6d9、#ff7a59 虛線、#ffd28a 點）；style.css #inset-wrap right/bottom | 相符 |
| balance | 預設 0.5、10 μW → 平衡溫度 15.4 mK | 03_dilution.js:112、:143–144（toFixed(1)）；Python 15.43 | 相符 |
| balance | 拉到 40 μW → 約 30.9 mK、約兩倍 | 03_dilution.js:114（滑桿 0.5–60）；Python 30.86 | 相符 |
| balance | 讀數「20 mK 時冷卻功率 ≈ 16.8 μW」 | 03_dilution.js:144（ṅ 未變 0.5） | 相符 |

## 課程

- 主題、學習目標、動手任務、孩子獨立改造（溫度減半）、好玩機制（闖關：Q̇ 計算）、作品（冷卻功率計算）、120 分鐘流程、驗收與常見誤解（越冷越難冷）依 `academy/lessons/Q043/lesson.json` 核對。
- 旁白不念英文：³He／⁴He 念「氦三」「氦四」，Still 稱「蒸餾室」，MXC 稱「混合腔」，GHS 稱「氣體處理系統」，單位念「毫克耳文」「微瓦」「毫莫耳每秒」；投影片保留符號。
- 沒有課堂錄音；未虛構孩子作品或對話。
- 投影片字型無法正確疊印 Q̇、ṅ 的上點（review sheet 看到錯位），投影片上寫成 Q = 84 n T²（Q：冷卻功率、n：循環率）；教材與來源保留原記號。
- 動畫控制項已用 Playwright 開頁實測：#overview 的「只看冷卻相關」「脈衝管氦氣」「冷卻水」「真空」按鈕存在（後三者預設 on）；#dilution 的「循環率」「熱負載」滑桿存在，讀數為「≈ 15.4 mK」「20 mK 時冷卻功率 ≈ 16.8 μW；100 mK 時 ≈ 420 μW」，右下小圖顯示。
