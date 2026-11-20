# Q093 來源筆記（逐字引文）

查核日：2026-11-18。學程內部簡報與動畫程式由製作代理讀取；熱負載百分比由製作代理以動畫參數重算。

## 如何操作量子電腦（slides/QC_Operation_Talk.pptx）

第 15 頁「認識你的後端」
- 「Google Willow（2024）」「105 顆量子位元」

第 50 頁「低於門檻：碼距越大，錯誤越少」
- 「實體錯誤率 p 低於門檻 pth（表面碼 ~1%）時，碼距每加 2，邏輯錯誤率乘上 1/Λ」
- 「Google Willow（Nature, 2025）d = 3 → 5 → 7，Λ ≈ 2.14」「d = 7（101 個量子位元）：每輪 0.143%」
- 「要到 10−6：d ≈ 27（~1,500 個實體量子位元 / 邏輯位元）」

第 51 頁「發展路線：從 NISQ 到容錯」
- 「NISQ 數十～上千實體位元」「早期容錯 數十～數百邏輯位元」「大規模容錯 數千邏輯位元以上」
- 「NISQ（現在）錯誤緩解 + 淺層線路 物理模擬、演算法研究、基準測試 線路深度受限於 ~1/ε」
- 「早期容錯（研發中）表面碼等邏輯量子位元 邏輯錯誤 10−6～10−9 中等規模化學、物理模擬」
- 「大規模容錯（目標）百萬實體位元等級 Shor、大型分子、材料設計 需解決佈線、低溫電子、即時解碼」
- 「今天學的 線路、轉譯、讀取、統計 在容錯時代依然適用——只是『量子位元』換成『邏輯量子位元』」

## 離子阱與中性原子量子電腦（slides/Ion_NeutralAtom_Talk.pptx）

第 45 頁「主要廠商與路線」
- 「Quantinuum：QCCD；H2（56 位元）→ Helios（98 位元，2025）」
- 「QuEra：⁸⁷Rb；Aquila（類比 256 顆）」「Atom Computing：…千顆級陣列」
- 「兩條路線都已有雲端可用的機器（Amazon Braket、Azure Quantum、各家雲端），並提出 2028–2030 年容錯運算的路線圖。」

第 46 頁「重點回顧」
- 「超導：速度；離子：品質；原子：規模。都已逼近錯誤更正門檻 → 競爭邏輯量子位元。」

## 量子電腦的周邊系統（slides/QC_Peripheral_Systems_Talk.pptx）第 38 頁「規模化趨勢」

- 「更大的冷凍平台」「模組化與互連」「低溫控制電子」「高密度佈線 … 降低每通道熱負載與體積」

## animations/js/atoms/13_compare.js

- `scale: { cap: '規模：已展示的量子位元 / 原子數（log₁₀，2024–2026 代表值）', val: { sc: Math.log10(1121), ion: Math.log10(98), atom: Math.log10(6100) }, txt: { sc: '約 100–1000+<br>（Willow 105、Condor 1121）', ion: '約 100<br>（Helios 98）', atom: '數百到數千<br>（Caltech 陣列 6100）' } }`
- `ui.radio([['conn', '連接性'], ['speed', '閘速度'], ['coh', '相干時間'], ['scale', '規模']], 'conn', setMode);`

## animations/js/operation/11_qec.js

- 標籤：「邏輯量子位元：d = ${d}，${d * d} 資料 + ${d * d - 1} 量測 = ${2 * d * d - 1} 實體量子位元」
- `ui.radio([[3, 'd = 3'], [5, 'd = 5'], [7, 'd = 7']], …)`；`ui.slider('實體錯誤率 p（每個資料量子位元）', 0.005, 0.2, …)`
- 插圖「邏輯錯誤率 vs 實體錯誤率（即時蒙地卡羅）」，顏色 `['#4f8cff', '#e0a54a', '#ff5a5f']` 對應 d = 3、5、7；白色直線＝目前 p

## animations/js/peripherals/05_wiring.js

- `ui.slider('量子位元數（線束示意）', 1, 200, 1, nq, …)`，預設 `nq = 20`
- `PD.wiring`：`passive: [45e-3, 1e-3, 3e-6, 0.4e-6, 0.015e-6]`、`attDiss: [0, 2e-6, 0, 2e-8, 2e-9]`、`hemt: 5e-3`、`cool: [30, 1.5, 40e-3, 200e-6, 19e-6]`
- 插圖顏色：`h / cpow > 1 ? '#ff5a5f' : h / cpow > 0.5 ? '#e0a54a' : '#2ecc71'`

## 重算紀錄（製作代理）

| 量子位元數 | 50 K | 4 K | Still | Cold plate | MXC |
|---|---|---|---|---|---|
| 20 | 8% | 5% | 0% | 11% | 4% |
| 100 | 38% | 22% | 2% | 52% | 21% |
| 200 | 75% | 45% | 4% | 103% | 42% |

Cold plate 約 97 顆轉橘、約 194 顆轉紅；50 K 約 134 顆轉橘。

## 維基百科

- Noisy intermediate-scale quantum era（https://en.wikipedia.org/wiki/Noisy_intermediate-scale_quantum_era）：NISQ 一詞的一般性描述，交叉比對用。
