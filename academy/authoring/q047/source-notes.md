# Q047 來源筆記（逐字引文）

查核日：2026-11-18。維基百科頁面由製作代理以 Wikipedia REST API（`/api/rest_v1/page/html/…`）取得，revision id 取自回應 HTML 的 `Special:Redirect/revision/…`。學程內部簡報、文件與動畫程式由製作代理讀取。

## Interlock (engineering)（Wikipedia，oldid=1379609315）

- 「An interlock is a feature or device that is commonly used in engineering and safety systems to keep machines, devices, and processes from operating until the guards are in place or the required circumstances are met.」
- 「When being utilized, interlocks are used to prevent or reduce the chances of injury to the operator, damage to the equipment, and actions being completed in the wrong order or in an unsafe way.」
- 「Software-based interlocks can be implemented by using computer logic or control logic such as Programmable Logic Controllers (PLCs).」

## Microwave oven（Wikipedia，oldid=1386433439）

- 「Furthermore, ovens are equipped with redundant safety interlocks, which remove power from the magnetron if the door is opened.」
- 「Microwave ovens are sold with a protective interlock so that it cannot be run when the door is open or improperly latched.」

## Helium-3（Wikipedia，oldid=1383917684）

- 「due to its high price, the helium-3 is usually contained in a closed system to avoid losses」
- 「A dilution refrigerator uses a mixture of helium-3 and helium-4 to reach cryogenic temperatures as low as a few thousandths of a kelvin.」
- 「Helium-3 is the primary coolant for superconducting quantum computing.」

## 學程內部簡報：slides/QC_Peripheral_Systems_Talk.pptx

- 第 25 頁「軟體堆疊：從量子程式到微波」表：使用者／雲端 API「Qiskit、Cirq、OpenQASM；工作佇列與權限」；編譯器「原生閘分解、量子位元映射、路由（SWAP）、最佳化」；脈衝層「查校準資料 → 脈衝；排出時間表」；控制韌體「FPGA 序列器、波形記憶體、即時分支」；校準／監控「自動校準、參數漂移追蹤、日誌與告警」。備註：「控制韌體在 FPGA 上以奈秒精度播放，處理即時分支。」「綠色球是結果往上傳：IQ 原始資料、0/1 位元串、最後變成直方圖或期望值。」
- 第 26 頁要點：「全部由軟體自動執行，結果寫入校準資料庫」「單量子位元：數十分鐘；整個處理器：數小時」「參數會漂移（TLS、溫度、磁通）→ 每日/每週自動重校」。
- 第 27 頁「監控與聯鎖」表：50 K 級「PT100 / 矽二極體」；4 K、Still「Cernox」；Cold plate、MXC「RuO₂」；GHS「壓力計 P1–P6、³He 流量計」；真空「OVC 真空計」；壓縮機「冷卻水溫、氦壓、馬達狀態」；機房「市電、UPS、室溫、濕度」。「聯鎖：冷卻水過溫 → 壓縮機停機；停電/控制器故障 → 閥門關閉、混合氣經背壓閥回儲存槽」「遠端監控：24 小時趨勢紀錄、簡訊/郵件告警、遠端操作」「3D 場景 9：冷卻水中斷 → 告警、聯鎖、回收混合氣」。備註：「冷凍機一旦降溫，通常會連續運轉好幾個月，所以 24 小時監控非常重要。」「冷卻水過溫，壓縮機自動停機保護自己」。
- 第 28 頁「常見故障與處置」表：冷卻水中斷／過溫「水溫上升｜壓縮機聯鎖停機｜恢復水路後重啟壓縮機；檢查冷卻水機」；流阻堵塞「³He 流量下降、凝結壓力升高、MXC 升溫｜告警｜回收混合氣、清理冷阱；必要時升溫至 ~4 K 以上」；真空洩漏「OVC 壓力上升、各級升溫｜告警、停止循環｜檢漏（氦質譜）、更換密封、重新抽真空」。註：「停電反應依 Bluefors LD 使用手冊；其餘為典型經驗，實際以設備手冊為準」。備註：「流阻堵塞……多半是雜質在冷阱或流阻處凍結」。

## 學程文件：docs/周邊系統連接與啟動指南.md

- 第 5 節表：「冷卻水溫度與流量｜連續紀錄｜≤ 27 °C、~11.5 L/min（PT415）」「校準參數漂移｜每日｜自動重校」；「告警建議透過 24 小時趨勢紀錄、簡訊或郵件通知、遠端操作來處理。」
- 第 6 節表：「冷卻水中斷／過溫｜壓縮機聯鎖停機。｜恢復水路、檢查冷卻水機後重啟壓縮機。」「真空洩漏｜告警：OVC 壓力上升、各級升溫，系統停止循環。｜用氦質譜檢漏、更換密封，重新抽真空。」「**原則**：任何異常都必須優先確保**混合氣（³He）不外洩**。」

## 互動動畫程式

- animations/js/peripherals/07_software.js：五層 `['使用者程式 / 雲端 API', …]、['編譯器', '原生閘分解 · 映射 · 路由 · 最佳化']、['脈衝層', '閘 → 脈衝（查校準資料）· 排程']、['控制韌體 / 序列器', 'FPGA · 波形記憶體 · 即時分支']、['硬體', '電子學 · 冷凍機 · 量子晶片']`；側邊「校準資料庫」「自動校準服務」「工作佇列 / 排程器」「監控 / 日誌」；下行標籤 `['量子電路（H、CNOT…）', '原生閘 + 實體量子位元', '脈衝序列（含時間表）', '波形 + 指令', '微波脈衝']`；上行標籤 `['IQ 原始資料', '0 / 1 位元串', '位元串', '直方圖 / 期望值', '結果回到使用者']`；滑桿「播放速度」0.3–2；插圖「同一個程式在不同層的樣子」；讀數「校準參數每隔數小時～數天需重新量測（頻率、振幅、讀取閾值會漂移）」；說明「脈衝層：每個原生閘查校準資料庫（頻率、振幅、DRAG 係數、讀取參數…）」。
- animations/js/peripherals/09_monitor.js：選項按鈕「正常運轉」「冷卻水中斷」「真空洩漏」「流阻堵塞」；模型 `water = 18 + Math.min(30, tf * 2.2)`、`comp_on = water < 32`、`status = water > 27 ? 'ALARM' : 'WARN'`、動作「水溫超限 → 聯鎖停止壓縮機；GHS 準備回收混合氣」；真空洩漏 `pOVC = 1e-5 * Math.exp(Math.min(tf, 20) * 0.6)`、`pOVC > 1e-3` 為 ALARM、動作「OVC 壓力過高：氣體導熱使各級升溫 → 停止循環、檢漏」；流阻堵塞 `flow = 0.5 * Math.exp(-tf / 3)`、`pCond = 500 + Math.min(600, tf * 60)`、`flow < 0.2` 為 ALARM、動作「³He 流量歸零、凝結壓力升高 → 多為雜質在冷阱/流阻凍結；需升溫清理冷阱」；感測器小球比例 > 3 紅、> 1.3 橘；插圖「監控曲線（最近 60 秒，時間加速）」。
