# Q042 事實查核

查核日：2026-11-18。查核者：製作代理（Claude）。逐字引文見 `source-notes.md`。
方法：維基百科三頁（Pulse tube refrigerator、Adiabatic process、Gas duster）由製作代理直接開啟並摘錄；學程簡報「量子電腦的周邊系統」第 7、8 頁（含講者備註）以 python-pptx 讀取；周邊系統動畫原始碼（`animations/js/peripherals/01_overview.js`、`02_pulsetube.js`、`common.js`）由製作代理逐行讀取；比例與換算以 Python 計算（見文末）。
限制：規格數字（PT415／CPA1110）來自簡報所引的廠商規格頁，製作代理未直接開啟廠商網站；家中實驗的溫度變化不給數字。

| # | 本集的說法（幕） | 依據 | 結論 |
|---|---|---|---|
| 1 | 上一堂：比較溫度和量子位元能量，晶片要冷到約 10 mK（1） | academy/lessons/Q041/brief.md（為什麼要 10 mK；hf 與 k_BT 比較） | 相符 |
| 2 | 壓縮變熱、膨脹變冷（2、5） | Adiabatic process：compression…causes a rise in temperature；expansion…causes a drop in temperature | 相符 |
| 3 | 稀釋冷凍機上半段由脈衝管從室溫冷到約 3 K，下半段交給稀釋冷凍（3） | Pulse tube refrigerator：PTRs are often used as precoolers of dilution refrigerators；簡報 p7：4 K 級量測約 2.85 K；p8 備註「稀釋冷凍機的上半段靠脈衝管冷卻器」；p9 備註「下半段 4 K 到 10 mK 靠的是稀釋冷凍」 | 相符 |
| 4 | 冷頭裝在冷凍機頂部、兩級；不必補充液態氦，稱為乾式（3） | 02_pulsetube.js subtitle「『乾式』冷凍機的心臟：不需液氦」、desc「兩級設計」；common.js buildFridge 的脈衝管冷頭在頂板上方 | 相符 |
| 5 | 壓縮機放在地上，把氦氣壓到高壓，熱交給冷卻水（4） | 02_pulsetube.js desc「壓縮機把氦氣壓縮到高壓（約 2 MPa），熱量交給冷卻水帶走」；簡報 p8 備註「放在地上的氦壓縮機」 | 相符 |
| 6 | 旋轉閥每秒約切換 1.4 次，輪流接通高壓和低壓（4） | 簡報 p8「旋轉閥約 1.4 Hz 切換高/低壓」；Pulse tube refrigerator：rotating valve alternately connects the high-pressure and the low-pressure side | 相符（場景 desc 寫 1–1.4 Hz；維基寫 1–2 Hz） |
| 7 | 蓄冷器塞滿金屬網或稀土合金，像海綿暫存熱量（4） | 02_pulsetube.js「填滿金屬網／稀土合金」；簡報 p8 備註「像海綿一樣儲存和交換熱量」；維基：wire mesh…rare earth materials | 相符 |
| 8 | 脈衝管搭配緩衝槽和小孔調整節奏，讓膨脹發生在冷端（4） | 02_pulsetube.js「脈衝管 + 緩衝槽/孔口調整壓力與流量的相位，使膨脹發生在冷端」；維基：orifice、buffer volume | 相符 |
| 9 | 打氣筒底部變溫：一部分壓縮、一部分摩擦（5） | Adiabatic process（壓縮升溫）；摩擦生熱為一般物理常識；本集不給比例 | 相符（比例未查證，故不說） |
| 10 | 除塵罐噴一陣子變冰；裡面是液化氣體，汽化、膨脹吸熱（5） | Gas duster：contain other gases that are compressible into liquids；The liquid…boils at a very low temperature, rapidly cooling | 相符 |
| 11 | 壓縮的熱在室溫端丟掉，膨脹的冷留在冷端（5、6） | 維基 Principle of operation：heat released at room temperature（X1、X3）、cooling power at X2；Comparison：cooling (due to expansion) takes place in a different region…than the heating | 相符 |
| 12 | 循環：高壓灌入→穿過蓄冷器留下熱→低壓時冷端膨脹吸熱、回程把熱帶回（6） | 維基：enters the regenerator with temperature TH and leaves…with TL, heat is transferred into the regenerator material. On its return, the heat stored…is transferred back into the gas；returns when the pressure is low with a temperature below TL, hence taking up heat from X2 | 相符 |
| 13 | 一輪約 0.7 秒（6） | 1 ÷ 1.4 Hz = 0.714 秒 | 相符（計算） |
| 14 | 單級最低只到 10 K 出頭，所以串兩級（7） | 維基：The lowest temperature reached with single-stage PTRs is just above 10 K. However, one PTR can be used to precool the other | 相符 |
| 15 | 一級約 45 K、約 40 W；冷卻輻射屏蔽、纜線熱錨定（7） | 簡報 p8 PT415「冷卻功率 @ 45 K 40 W」；02_pulsetube.js「一級約 40–50 K（冷卻輻射屏蔽、熱錨定纜線）」、標籤「一級冷端 ~45 K（~40 W）」；p7 50 K 級用途「輻射屏蔽、纜線第一次熱錨定」 | 相符（p7 Krinner 量測該台為 30 W @ 45 K，屬另一機型量測；本集用 PT415 規格 40 W） |
| 16 | 二級約 3 K，4.2 K 時 1.5 W；冷卻 4 K 板、凝結混合氣（7、8） | 簡報 p8 PT415「冷卻功率 @ 4.2 K 1.5 W」；02_pulsetube.js 標籤「二級冷端 ~3 K（~1.5 W @ 4.2 K）」、desc「二級約 3–4 K（冷卻 4 K 板並凝結混合氣）」 | 相符 |
| 17 | 壓縮機用電約 10.7 kW、冷卻水每分鐘 11.5 L（8） | 簡報 p8：CPA1110 耗電（60 Hz）10.7 kW；冷卻水 11.5 L/min，≤ 27 °C | 相符 |
| 18 | 用掉的電約是二級冷卻功率的七千倍（8） | 10700 ÷ 1.5 = 7133 | 相符（計算；兩者溫度條件不同，只作量級比較） |
| 19 | 越冷越難把熱搬出去（8，提問） | 卡諾效率 T_L/(T_H−T_L)：4.2 K 對 300 K 為 1.42 %；實際 1.5/10700 = 0.014 %，約為卡諾上限的 1 %；維基 COP 段落 | 相符（答案放在教材解答） |
| 20 | 除塵罐倒置會噴出極冷液體、可能凍傷；家長操作、不對人噴（9、12） | 課綱常見誤解與安全提醒；Gas duster：not to hold the can upside down…This can cause mild to moderate frostbite | 相符 |
| 21 | 冷端沒有會動的零件；振動小、少磨損、構造簡單可靠（10） | 維基：without moving parts in the low temperature part；PTR does not have such a displacer, making the construction…simpler, cheaper, and more reliable；簡報 p8「冷端無活動零件」 | 相符 |
| 22 | 冷端在真空罩裡，修理要整台回溫，再花一兩天重新降溫（10） | 簡報 p7「空機降溫約 1–2 天」；common.js 真空罩（OVC）包住各級板 | 相符（回溫時間另計，本集不說） |
| 23 | 旋轉閥仍會晃；遠端馬達約損失兩成冷卻功率（10、12） | 簡報 p8「遠端馬達可降低振動，但約損失 20 % 冷卻功率」（引 CUORE arXiv:1904.05745）；維基：mechanical vibrations caused by PTRs can cause microphonics | 相符 |
| 24 | 下一堂：兩種氦混在一起吸熱，冷到 10 mK（12） | academy/lessons/Q043/brief.md（稀釋冷凍原理：³He 溶入 ⁴He 時吸熱）；簡報 p9 | 相符 |

## 課程

- 主題、學習目標（壓力波與蓄冷器、約 3 K）、動手任務（打氣筒、除塵罐）、孩子獨立改造（冷端無活動零件的優點）、好玩機制（科學實驗：壓縮與膨脹）、作品（實驗紀錄）、生活技能支線（安全使用壓縮氣體）、120 分鐘流程與驗收依 `academy/lessons/Q042/lesson.json` 核對。
- 課綱「壓力波」：維基指出系統裡壓力是逐漸升降、並沒有真的「脈衝」；本集旁白說「壓力一高一低」，不說成一陣陣的衝擊。
- 旁白不念英文：K 念「克耳文」、mK 念「毫克耳文」、W 念「瓦」、kW 念「千瓦」、Hz 改說「每秒切換幾次」；投影片保留符號。
- 沒有課堂錄音；未虛構孩子作品或對話。

## 計算（Python 3.13）

```
1 / 1.4                    = 0.714 s（一輪）
10700 / 1.5                = 7133（約七千倍）
11.5 L/min × 60            = 690 L/h
1.5 W × (1 − 0.20)         = 1.2 W（遠端馬達）
2.0 MPa / 101.325 kPa      = 19.7 atm；0.8 MPa = 7.9 atm
卡諾 4.2/(300−4.2)          = 0.0142；實際 1.5/10700 = 0.000140；比值 0.0099
10700 W /(11.5/60 kg/s × 4186 J/kg·K) = 13.3 K（冷卻水若全吸收壓縮機熱量的升溫，只作參考，未寫入旁白）
動畫：相位速率 2π×0.7×速度 → 1× 時一輪 1.43 s；0.3× 時 4.76 s；0.5× 時 2.86 s
用電長條圖合計 10.7+10+3+1.5+1 = 26.2 kW（場景顯示「合計約 26 kW」）
```

## 動畫段（demos_extra/q042.py）的畫面依據

- 粒子顏色：`App.tempColor` 為對數色階 HSL，300 K 色相 0°（紅）、45 K 約 43°（橘黃）、3 K 約 104°（綠）。場景讀數文字寫「紅 300 K → 藍 3 K」，但粒子實際最冷處是綠色，旁白依實際顏色說「綠色」。
- 冷頭壓力小圖：`pr = 1.4 + 0.6·tanh(3·sin φ)`，在 0.8 與 2.0 MPa 之間像方波一樣切換；讀數在 sin φ > 0 時寫「高壓相：氣體壓縮」，否則寫「低壓相：氣體膨脹 → 冷端吸熱」。
- 粒子擺幅：蓄冷器 amp 0.25／0.18，脈衝管 0.6／0.5（顯示時再乘 0.5）；半徑小於 0.15 的管（兩根脈衝管）相位落後 0.9 弧度。
- 「顯示速度（實際約 1.4 Hz）」滑桿在 1× 時動畫一秒約 0.7 輪，並不等於真實頻率；旁白只說「放慢了，真實的旋轉閥約每秒 1.4 次」。
