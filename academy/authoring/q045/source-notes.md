# Q045 來源筆記（逐字引文）

查核日：2026-11-18。維基百科頁面由製作代理以 MediaWiki API 取得（revision id 取自回應的 revid）。學程內部簡報與動畫程式由製作代理讀取。

## Wiedemann–Franz law（Wikipedia，oldid=1384450860）

- 「the Wiedemann–Franz law states that the ratio of the electronic contribution of the thermal conductivity (κ) to the electrical conductivity (σ) of a metal is proportional to the temperature (T).」
- 「who in 1853 reported that κ/σ has approximately the same value for different metals at the same temperature.」

## Niobium–titanium（Wikipedia，oldid=1370480366）

- 「Niobium–titanium (Nb-Ti) is a ductile alloy of niobium and titanium, used industrially as a type II superconductor wire」
- 「Its critical temperature is about 10 kelvins.」

## Dilution refrigerator（Wikipedia，oldid=1375073377）

- 「a cryogenic device that provides continuous cooling to temperatures as low as 2 mK, with no moving parts in the low-temperature region.」

## 學程內部簡報：slides/QC_Peripheral_Systems_Talk.pptx

- 第 14 頁「每顆量子位元需要哪些線？」表：XY 驅動「每顆 1 條；微波脈衝做單量子位元閘；−20 dB @4K、−20 @CP、−20 @MXC」；Z 磁通「每顆 1 條；SQUID 調頻、雙量子位元閘」；讀取輸入、輸出「每 4–8 顆 1 條」；TWPA 泵浦「每條輸出 1 條」；直流線「數十條；溫度計、加熱器、HEMT 偏壓」。「124／50 顆量子位元所需的 RF 線（50 XY + 50 Z + 8 輸入 + 8 輸出 + 8 泵浦）」「100 顆 ≈ 250 條」。備註：「射頻線數量大約是量子位元數的兩倍半」。
- 第 15 頁：「輸入總衰減約 60 dB（+ ~9 dB 線損）→ 6 GHz 殘留熱光子 ~10−3」「衰減器要熱錨定在對應溫層，吸收的功率才不會加熱下一級」「輸出線用 NbTi 超導同軸：低損耗、低導熱」；表：4 K「HEMT ~40 dB（~5–10 mW）」、MXC「隔離器、帶通、TWPA 20–30 dB」。
- 第 16 頁：「每條不鏽鋼同軸被動熱：50 K ~45 mW、4 K ~1 mW、CP ~0.4 μW、MXC ~0.015 μW」「HEMT 每顆 5 mW（4 K）」「冷卻功率取 XLD 量測值」「數百顆量子位元時，Cold plate 與 50 K 率先吃緊」。備註：「200 顆的時候，50 K 級用掉約四分之三，Cold plate 已經超過一百趴」。
- 第 17 頁表：不鏽鋼同軸「導熱 低；損耗 中；輸入、磁通線（室溫 → MXC）」；NbTi 超導同軸「導熱 極低（超導段）；損耗 極低；輸出線 MXC → 4 K」；銅／銀鍍同軸「導熱 高；損耗 低；只用在同一溫層內、室溫段」。備註：「纜線材料的選擇是導熱和損耗之間的權衡：導電好的金屬通常導熱也好。」

## 互動動畫程式

- animations/js/peripherals/common.js：`stages` 標籤「300 K 頂板」「50 K 級（~35–45 K）」「4 K 級（~3 K）」「Still（~0.9 K）」「Cold plate（~100 mK）」「MXC（~10 mK）」；`wiring.passive [45e-3, 1e-3, 3e-6, 0.4e-6, 0.015e-6]`、`attDiss [0, 2e-6, 0, 2e-8, 2e-9]`、`hemt 5e-3`、`cool [30, 1.5, 40e-3, 200e-6, 19e-6] // W（45 K / 4.2 K / 1.2 K / 140 mK / 20 mK）`；註「佈線熱負載（每條不鏽鋼同軸，Krinner 2019）與各級冷卻功率（Bluefors XLD 量測）」。
- animations/js/peripherals/05_wiring.js：`counts = (n) => ({ xy: n, z: n, rin: Math.ceil(n / 6), rout: Math.ceil(n / 6), pump: Math.ceil(n / 6), dc: 4 })`；滑桿「量子位元數（線束示意）」1–200、預設 20；選項按鈕「全部」「XY 驅動」「Z 磁通」「讀取輸入」「TWPA 泵浦」「讀取輸出」「直流線束」；插圖「各級熱負載 / 可用冷卻功率（示意估算）」、註「100 % = 該級冷卻功率用盡（紅色）」。
- animations/power1000.html 場景 heat「低溫熱預算：熱帳怎麼變成電」：「細線：被動熱負載降約 4 倍，但不鏽鋼磁通直流熱反而 ×4。NbTi 磁通線：消除直流主動熱負載。」；程式 `const k = o.thin ? 0.27 : 1`、`r.fluxDC = o.nbti ? 0 : L.flux * 0.050e-6 * (o.thin ? 4 : 1)`；開關「改用 0.047" 細同軸」「磁通線改用超導 NbTi」；預設 N=1000、稀釋單元 3 組；指標「熱帳：過關／不過關」。
