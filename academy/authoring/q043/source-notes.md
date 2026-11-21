# Q043 來源筆記（逐字引文）

查核日：2026-11-18。維基百科頁面原始碼由製作代理直接讀取（`?action=raw`，未取得 revision id）。學程內部簡報與動畫程式由製作代理讀取。

## Dilution refrigerator（Wikipedia，2026-11-18 讀取）

- 「at very low temperatures the concentrated phase is essentially pure ³He, while the dilute phase contains about 6.6% ³He and 93.4% ⁴He.」
- 「The working fluid is ³He, which is circulated by vacuum pumps at room temperature.」
- 「the pure ³He enters the mixing chamber, the coldest area of the device.」
- 「The heat necessary for the dilution is the useful cooling power of the refrigerator, as the process of moving the ³He through the phase boundary is endothermic and removes heat from the mixing chamber environment.」
- 「The vapor in the still is practically pure ³He, which has a much higher partial pressure than ⁴He at 500–700 mK. Heat is supplied to the still to maintain a steady flow of ³He.」
- 「Q̇m [W] = 84 (ṅ3 [mol/s]) (T [K])²」
- 「The cooling power is provided by the heat of mixing of the helium-3 and helium-4 isotopes.」

## 學程內部簡報（slides/QC_Peripheral_Systems_Talk.pptx）

- 第 8 頁：脈衝管規格表；02_pulsetube.js「二級冷端 ~3 K」。
- 第 9 頁「稀釋冷凍原理：³He 溶入 ⁴He 時吸熱」：①凝結（4 K、流阻 ~500 mbar）②預冷（熱交換器）③溶解（製冷）④蒸發（Still ~0.8 K）⑤抽回；「Q̇ ≈ 84 ṅ T²」「ṅ ≈ 0.5 mmol/s → 20 mK 時 ~17 μW → 100 mK 時 ~420 μW」。備註：「在 0.87 K 以下會自動分成兩相：上層幾乎是純 ³He 的濃相，下層是 ³He 溶在超流 ⁴He 裡的稀相，即使到絕對零度，稀相裡還是會有 6.6% 的 ³He。」「就像液體蒸發需要吸熱一樣，這個溶解過程也要吸熱」。
- 第 10 頁「冷卻功率與溫度的關係」：「溫度減半，冷卻功率只剩 1/4」「熱負載多 4 倍 → 基溫升高 2 倍」「把熱負載擋在上層，比追求更大冷卻功率有效」。
- 第 11 頁「氣體處理系統（GHS）」：渦輪分子泵抽 Still；冷阱；混合氣儲存槽「停機時儲存 ³He/⁴He」；「³He：最昂貴的『耗材』」。

## 互動動畫程式

- animations/js/peripherals/03_dilution.js：desc「脈衝管只能到約 3 K」「低於 0.87 K 時分成兩相」「Q̇ ≈ 84 ṅ T²」；滑桿「³He 循環率 ṅ (mmol/s)」0.1–1.5 預設 0.5、「MXC 上的熱負載 (μW)」0.5–60 預設 10；讀數「平衡溫度 T = √(Q̇ / 84ṅ) ≈ … mK」「20 mK 時冷卻功率 ≈ … μW；100 mK 時 ≈ … μW」「（實際機台因熱交換器效率等因素低於理想值）」。
- animations/js/peripherals/01_overview.js：按鈕「脈衝管氦氣」「冷卻水」「混合氣循環」「真空」「微波 / DC」「資料 / 時脈」「電力」「全部顯示」「只看冷卻相關」「只看訊號相關」；混合氣循環（紫色）：Still 抽氣粗管 → GHS → 凝結回流細管；GHS → 混合氣儲存槽。
