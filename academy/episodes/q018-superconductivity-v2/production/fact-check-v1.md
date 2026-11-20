# Q018 事實查核

查核日：2026-11-18。查核者：製作代理（Claude）。逐字引文見 `source-notes.md`。
方法：課綱 `academy/lessons/Q017–Q019`；學程簡報「超導量子電腦的核心：JJ 與微波讀取」第 7–8 頁的文字由製作代理讀取；`animations/index.html`、`animations/js/scenes/02_cooper.js`、`animations/js/core.js` 由製作代理讀取；維基百科 Superconductivity、Meissner effect 兩頁由製作代理於查核日開啟並摘錄；「低一百倍以上」由製作代理重新計算（1.2 K ÷ 10 mK = 120）。
限制：本集只看影片與動畫，沒有實際實驗或量測；動畫的電子成對與晶格扭曲是示意畫面。臨界溫度在不同資料裡略有差異。動畫段尚未試錄。

| # | 本集的說法（幕） | 依據 | 結論 |
|---|---|---|---|
| 1 | 上一堂：超導量子電腦要用超導電路做出人造原子（1） | academy/lessons/Q017/brief.md；q017 旁白 | 相符 |
| 2 | 超導兩個現象：電阻消失、磁鐵懸浮；學習目標零電阻與排斥磁場（1、2） | Q018 lesson.json 課程主題、學習目標 | 相符 |
| 3 | 作品是超導觀察筆記；下半場查三種材料的臨界溫度並排序（2、10） | lesson.json 作品、孩子獨立改造 | 相符 |
| 4 | 某些材料冷到臨界溫度以下，性質突然改變（3） | jj_talk p7「低於臨界溫度 Tc」；02_cooper.js Tc = 1.2，低於 Tc 為超導態 | 相符 |
| 5 | 1911 年昂內斯把汞冷到約 4.2 K，電阻突然消失（3） | 維基 Superconductivity：discovered in solid mercury on April 8, 1911, by Heike Kamerlingh Onnes；about 4.2 K；the resistance abruptly disappeared | 相符 |
| 6 | 4.2 K 只比絕對零度高四度多一點（3） | 克耳文溫標以絕對零度為 0 K；1 K 的間隔等於 1 °C | 相符 |
| 7 | 電阻不是慢慢降到零，而是在臨界溫度一下子掉下去（3） | 維基「abruptly disappeared」；02_cooper.js 插圖 R = 0（T < Tc）、1 + 0.08(T − Tc)（T ≥ Tc） | 相符 |
| 8 | 一般電線裡電子被晶格振動撞來撞去，能量變成熱＝電阻（4） | 02_cooper.js 正常態標籤「電子被晶格振動散射 → 有電阻」、讀數「電子與聲子碰撞 → 焦耳熱」 | 相符（簡化說法；雜質與缺陷也會散射電子） |
| 9 | 超導時電子兩兩成對、整齊前進、不被撞散；電阻是零（4） | 02_cooper.js desc「整體同步移動，不再被晶格散射 → 直流電阻為零」；jj_talk p7「零直流電阻」 | 相符（「零」指直流電阻） |
| 10 | 電流在超導環裡流好幾年都不衰減（4） | jj_talk p7「電流可在超導環中流動多年不衰減」；維基 currents in superconducting coils can persist for years without any measurable degradation | 相符 |
| 11 | 邁斯納效應：1933 年邁斯納和奧克森菲爾德發現，超導體把內部磁場推出去（5） | 維基 Meissner effect：Walther Meissner and Robert Ochsenfeld, 1933；expulsion of a magnetic field from a superconductor；jj_talk p7「磁場被完全排出超導體內部」 | 相符 |
| 12 | 先放進磁場再冷下來，磁場也會被趕出去；光靠零電阻解釋不了（5） | 維基 Meissner effect：transitions…in a constant magnetic field, it actively expels magnetic flux；perfect conductor has no mechanism for flux expulsion | 相符 |
| 13 | 磁場能鑽進表面約 50–100 奈米（5） | jj_talk p7「只在表面穿透深度 λ ~ 50–100 nm 內存在」；維基 penetrates a short distance from the surface（London penetration depth） | 相符（數值依投影片，隨材料而異） |
| 14 | 表面電流像一塊電磁鐵，把磁鐵推開；推力等於重量時停在半空（6） | 維基 Superconductivity：This current effectively forms an electromagnet that repels the magnet；力平衡為一般力學 | 相符 |
| 15 | 磁鐵浮在已經是超導的材料上方，嚴格說不能證明邁斯納效應（6） | 維基 Meissner effect：subsequent levitation of a magnet above an already superconducting material does not demonstrate the Meissner effect | 相符 |
| 16 | 鋁約 1.2 K、鉭 4.5 K、鈮 9.2 K（7） | jj_talk p7「Al ≈ 1.2 K、Ta ≈ 4.5 K、Nb ≈ 9.2 K」 | 相符 |
| 17 | 汞 4.2 K；釔鋇銅氧約 93 K，高於液態氮沸點 77 K（7） | 維基 Superconductivity：mercury 4.2 K；raised the critical temperature to about 93 K；liquid nitrogen 77 K | 相符 |
| 18 | 動畫裡的超導體是鋁；量子晶片在約 10 mK 工作，比鋁的 Tc 低一百倍以上（7） | 02_cooper.js 標籤「正離子晶格（Al）」、Tc = 1.2；jj_talk p7「量子電路在 10 mK 工作 ≪ Tc」；1.2 ÷ 0.01 = 120 | 相符 |
| 19 | 觀察與推論分開；生活技能（8） | lesson.json 生活技能支線「分辨「觀察」與「推論」」 | 相符（例句為本集設計） |
| 20 | 液態氮會凍傷；只看影片，不在家操作（9、12） | lesson.json 常見誤解與安全提醒 | 相符 |
| 21 | 用動畫溫度滑桿對照正常態與超導態（9） | lesson.json 動手任務；02_cooper.js 滑桿「溫度 T (K)」、按鈕「超導態 0.3 K」「正常態 2.5 K」 | 相符 |
| 22 | 120 分鐘安排（11） | lesson.json 2 小時課程流程 | 相符 |
| 23 | 下一堂：電子為什麼成對、全家當晶格、庫柏對和能隙（12） | academy/lessons/Q019/brief.md | 相符 |

## 動畫展示段（demos_extra/q018.py，animations/index.html#cooper）

| 說法 | 依據（js/scenes/02_cooper.js） | 結論 |
|---|---|---|
| 一開始 0.3 K；金色離子、藍色與紫色電子、青色連線、往右流 | 第 43 行 T = 0.3；第 13、29、34 行顏色；第 63、67 行 +x 方向；第 9 行相機在 +z 往原點看，+x 在畫面右方 | 相符 |
| 下方青色字「超導態……同步流動，無散射」；右下青色點在電阻 0 | 第 61–62 行；第 49、52 行 | 相符 |
| 按正常態：2.5 K，連線消失、電子亂撞、離子抖得更厲害 | 第 45 行；第 75–87 行；第 94 行振幅 0.02 + 0.05T（0.035 → 0.145） | 相符 |
| 點跳到上面那條線；字變粉紅色 | 第 49 行 R(2.5) ≈ 1.10；第 62 行 #ffb0b2 | 相符 |
| 0.9 K：配對約 68 %、三對拆開 | 第 59–60 行：1 − 0.75⁴ = 0.684；round(6.84) = 7 對，10 − 7 = 3 | 相符 |
| 1.1 K：只剩三對、約 29 %、點仍在零 | 1 − (1.1/1.2)⁴ = 0.294；round(2.94) = 3；R = 0 | 相符 |
| 1.3 K：全部拆散、字變正常態、點跳上去 | T ≥ Tc → frac = 0、R = 1.008 | 相符 |
| 降回 0.6 K：電子重新配對 | 1 − 0.5⁴ = 0.94 → 9 對 | 相符 |
| 0.05 K：配對比例 100 % | 1 − (0.05/1.2)⁴ ≈ 1.000 → 顯示「100 %」 | 相符 |
| 畫面裡沒有磁鐵、看不到懸浮 | 02_cooper.js 只有離子、電子、連線、外框與標籤 | 相符 |

## 課程

- 主題、學習目標、動手任務、孩子獨立改造、好玩機制（科學實驗（觀察紀錄））、作品、120 分鐘流程、驗收、常見誤解、生活技能（分辨觀察與推論）依 `academy/lessons/Q018/lesson.json` 核對。
- 旁白不念英文：Kelvin 說「克耳文」、Meissner 說「邁斯納」、YBCO 說「釔鋇銅氧」、Cooper pair 說「庫柏對」；投影片上保留 K、mK、nm 單位。
- 沒有課堂錄音；未虛構孩子作品、觀察筆記或實驗結果。
