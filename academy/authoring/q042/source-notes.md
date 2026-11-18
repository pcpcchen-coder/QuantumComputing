# Q042 來源筆記（逐字引文）

查核日：2026-11-18。維基百科頁面由製作代理直接開啟（Pulse tube refrigerator 的 revision id 取自 API；另兩頁以 action=raw 讀取當日版本，API 限流未取得 revision id）。學程內部簡報與動畫程式由製作代理讀取。

## Pulse tube refrigerator（Wikipedia，oldid=1300227488）

- 「this cryocooler can be made without moving parts in the low temperature part of the device」
- 「In research, PTRs are often used as precoolers of dilution refrigerators.」
- 「a regenerator consisting of a porous medium with a large specific heat (which can be stainless steel wire mesh, copper wire mesh, phosphor bronze wire mesh, lead balls, lead shot, or rare earth materials)」
- 「The pressure varies gradually and the velocities of the gas are low. So the name "pulse" tube cooler is misleading, since there are no pulses in the system.」
- 「it enters the regenerator with temperature TH and leaves the regenerator at the cold end with temperature TL, hence heat is transferred into the regenerator material. On its return, the heat stored within the regenerator is transferred back into the gas.」
- 「At the cold end of the tube, the gas enters the tube via X2 when the pressure is high with temperature TL and returns when the pressure is low with a temperature below TL, hence taking up heat from X2」
- 「Due to its clever design, the PTR does not have such a displacer, making the construction of a PTR simpler, cheaper, and more reliable.」
- 「PTRs for temperatures below 20 K usually operate at frequencies of 1 to 2 Hz and with pressure variations from 10 to 25 bar.」
- 「A system of valves (usually a rotating valve) alternately connects the high-pressure and the low-pressure side of the compressor to the hot end of the regenerator.」
- 「The lowest temperature reached with single-stage PTRs is just above 10 K. However, one PTR can be used to precool the other.」
- 「For many low temperature experiments, mechanical vibrations caused by PTRs can cause microphonics on measurement lines」

## Adiabatic process（Wikipedia，2026-11-18 版本）

- 「The adiabatic compression of a gas causes a rise in temperature of the gas. Adiabatic expansion against pressure, or a spring, causes a drop in temperature.」

## Gas duster（Wikipedia，2026-11-18 版本）

- 「the cans do not actually contain air … but rather contain other gases that are compressible into liquids.」
- 「When using gas duster, it is recommended to not hold the can upside down, as this can result in spraying liquid on to the surface. The liquid, when released from the can, boils at a very low temperature, rapidly cooling any surface it touches. … This can cause mild to moderate frostbite」

## 學程內部簡報（slides/QC_Peripheral_Systems_Talk.pptx）

- 第 7 頁表格：「50 K 級 ~35 K 30 W @ 45 K 輻射屏蔽、纜線第一次熱錨定」「4 K 級 ~2.85 K 1.5 W @ 4.2 K HEMT 放大器、衰減器、凝結混合氣」；觀念欄「基溫約 10 mK；空機降溫約 1–2 天」。
- 第 8 頁「脈衝管冷卻器與氦壓縮機」表格：PT415「冷卻功率 @ 4.2 K 1.5 W」「冷卻功率 @ 45 K 40 W」「壓縮機 CPA1110」「耗電（60 Hz）10.7 kW」「冷卻水 11.5 L/min，≤ 27 °C」「氦氣工作壓力 15–17 bar（靜態）」；文字「旋轉閥約 1.4 Hz 切換高/低壓；冷端無活動零件」「遠端馬達可降低振動，但約損失 20 % 冷卻功率」；資料來源「Bluefors / Cryomech PT415、PT420 規格頁；遠端馬達：CUORE（arXiv:1904.05745）」。
- 第 8 頁講者備註：「稀釋冷凍機的上半段靠脈衝管冷卻器。它由兩部分組成：放在地上的氦壓縮機，和裝在冷凍機頂部的冷頭」「蓄冷器是填滿金屬網或稀土合金的管子，像海綿一樣儲存和交換熱量，形成上熱下冷的溫度梯度；脈衝管和緩衝槽調整相位，使膨脹發生在冷端，冷端就持續吸熱」。

## 互動動畫程式

- animations/js/peripherals/02_pulsetube.js：subtitle「『乾式』冷凍機的心臟：不需液氦，持續提供 ~45 K 與 ~3 K」；desc「壓縮機把氦氣壓縮到高壓（約 2 MPa），熱量交給冷卻水帶走」「旋轉閥以約 1–1.4 Hz 交替接通高壓與低壓」「冷端沒有活動零件，振動小、可靠度高」「兩級設計：一級約 40–50 K（冷卻輻射屏蔽、熱錨定纜線），二級約 3–4 K（冷卻 4 K 板並凝結混合氣）」；標籤「氦壓縮機 電力 ~10 kW · 水冷」「高壓氦（~2 MPa）」「低壓氦（~0.8 MPa）」「一級冷端 ~45 K（~40 W）」「二級冷端 ~3 K（~1.5 W @ 4.2 K）」「緩衝槽 + 孔口（相位調節）」；滑桿「顯示速度（實際約 1.4 Hz）」；小圖「冷頭內壓力（旋轉閥切換高/低壓）」；讀數「高壓相：氣體壓縮」「低壓相：氣體膨脹 → 冷端吸熱」。
- animations/js/peripherals/01_overview.js：按鈕「只看冷卻相關」（顯示脈衝管氦氣、冷卻水、混合氣循環、真空）、「視角：冷凍機頂部」；設備標籤「脈衝管壓縮機（~11 kW）」「冷卻水機」；小圖「典型用電分配（kW，示意）」。
- animations/js/peripherals/common.js：PD.power「脈衝管壓縮機 10.7」「冷卻水系統 10.0」…；`App.tempColor` 對數色階。
