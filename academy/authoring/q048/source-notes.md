# Q048 來源筆記（逐字引文）

查核日：2026-11-18。維基百科頁面由製作代理直接開啟（revision id 取自頁面的 wgRevisionId）。學程內部簡報、文件與動畫程式由製作代理讀取。

## Uninterruptible power supply（Wikipedia，oldid=1372628605）

- 「An uninterruptible power supply (UPS) or uninterruptible power source is an electrical apparatus that provides emergency power to a load when the input power source or mains power fails.」
- 「The on-battery run-time of most uninterruptible power sources is relatively short (typically ranging from 5 to 15 minutes) but sufficient to start a standby power source or properly shut down the protected equipment.」

## Ground loop (electricity)（Wikipedia，oldid=1383945498）

- 「a ground loop or earth loop occurs when two points of a circuit are intended to have the same ground reference potential but instead have a different potential between them.」
- 「interconnect all the metal chassis with heavy conductors like copper strips, then connect to the building ground wire system at one point; this is referred to as star grounding or single-point grounding.」

## Checklist（Wikipedia，oldid=1373591749）

- 「A checklist is a type of job aid used in repetitive tasks to reduce failure by compensating for potential limits of human memory and attention.」
- 「The best known example is the cockpit preflight checklist」
- 「An example is the WHO Surgical Safety Checklist developed for the World Health Organization and published in 2008」

## 學程內部簡報

- slides/QC_Peripheral_Systems_Talk.pptx 第 30 頁「電力：一套系統約 25 kW」：「Google Sycamore：冷凍 ~10 kW + 冷卻水 ≥10 kW + 電子 ~3 kW，最壞 ~26 kW（Arute et al., 2019 補充資料）」；「三相市電（壓縮機、冷卻水機）」「UPS 供應：控制電子、電腦、GHS 控制器與閥門、溫控器、監控網路（建議 ≥ 1–2 小時）」「壓縮機通常不接 UPS（功率大）；停電時依程序安全回收混合氣」「可選：發電機自動切換」。講者備註：壓縮機約 10.7 千瓦、冷卻水約 10 千瓦、電子約 3 千瓦、氣體處理系統和電腦監控各一兩千瓦。
- 第 31 頁：「PT415 壓縮機：11.5 L/min、入水 ≤ 27 °C；帶走 ~10 kW」；「冷凍機框架 + 吊裝空間（開罐需挑高與吊車）；壓縮機可置於隔壁降噪」；備註「冷卻水中斷是最常見的停機原因之一」。
- 第 32 頁：「脈衝管 ~1.4 Hz 及諧波振動」「纜線摩擦起電 → 5–10 kHz 雜訊」「纜線綁紮/包覆（改善 > 10×）」「單點（星形）接地，避免接地迴路」「冷凍機、機櫃、儀器共用同一參考」；來源 Kalra et al., Rev. Sci. Instrum. 87, 073905 (2016)（量測對象為電子自旋量子位元）。
- 第 33 頁：「冷凍機置中，四周留維護與開罐空間」「電子機櫃靠近冷凍機頂板 → 縮短室溫纜線」「壓縮機、冷卻水機放隔壁或室外 → 噪音、振動、廢熱隔離」「GHS 與儲存槽靠近冷凍機 → 抽氣管短」「頂部線槽分開：微波/直流 vs 電力」「單點接地、UPS 與配電盤集中」。
- 第 37 頁「從零到上線：整合檢查表」：1. 設施就緒（三相電、UPS、接地／冷卻水機與水路／壓縮空氣、空調／網路與時間同步）2. 冷卻系統 3. 低溫佈線（裝線、熱錨定／室溫/低溫各量一次穿透／屏蔽、樣品盒、打線／關罐、抽真空、檢漏）4. 降溫（脈衝管預冷／凝結混合氣／循環到基溫／確認各級溫度）5. 電子與校準（儀器鎖相、觸發／HEMT/TWPA 偏壓／自動校準流程／基準測試 → 上線）。
- slides/output/qc-power-supply.pptx 第 18 頁（LRZ 現場勘查規格）：「直流：每軸 < 100 µT／交流：每軸 ≪ 1 µT」「地板振動 < 400 µm/s RMS／噪音 < 80 dBA／電子櫃溫度 12 小時 ±1 °C」「基地台、無線電發射台 ≥ 100 m／日光燈 ≥ 2 m」。第 20 頁：「約 1.4 Hz 脈衝管振動：氣壓振盪本身，電子濾不掉／只能機械隔離與拉開距離」。

## 學程文件

- docs/周邊系統連接與啟動指南.md §1.2：脈衝管壓縮機 ~10.7 kW、冷卻水系統 ~10 kW、控制電子機櫃 ~3 kW、氣體處理系統 ~1–2 kW、電腦／監控／網路 ~1 kW，「合計約 25 kW（Google Sycamore 公開的最壞情況約 26 kW）」。
- 同 §6：「停電：壓縮機與冷卻水停止，UPS 維持控制系統。約 10 分鐘後混合液開始沸騰，除必要閥門外全部關閉，混合氣經背壓閥回收至儲存槽。」「復電後依序重啟（冷卻水 → 壓縮機 → GHS），重新降溫需數小時到 1 天。」「冷卻水中斷／過溫：壓縮機聯鎖停機。」「任何異常都必須優先確保混合氣（³He）不外洩。³He 每公升約 1,000–20,000 美元」。
- docs/量子電腦供電設計文獻回顧與我們切入點.md §2：「冷卻系統故障後，約 2 分鐘內 QPU 就會升溫超過 1 K。」「重新降溫需要 2–5 天，最壞情況約 10 天，降溫完成後還要整套重新校準。」【推論】「UPS 必須涵蓋整條冷卻鏈……UPS 的任務是撐到發電機接手。」§3.2 LRZ Table 1 現場要求。

## 互動動畫程式

- animations/js/peripherals/08_infra.js：subtitle「一套稀釋冷凍機系統約 20–30 kW；壓縮機與冷卻水是最大負載」；設備標籤「市電變壓器（三相）」「配電盤」「UPS + 電池」「隔離變壓器」「控制電子 + 電腦」「GHS（泵 · 閥 · 控制器）」「壓縮機 ~10.7 kW」「冷卻水機（≤27 °C）」「單點接地」「避震座 + 剛性框架」「室外」；`ui.toggle('⚡ 模擬停電', false, …)`（第 64 行）、`ui.toggle('脈衝管遠端馬達 + 纜線固定（降振）', true, …)`（第 65 行）；停電面板「壓縮機、冷卻水機停止；UPS 供電給電子、電腦、GHS 閥門控制／GHS 關閉閥門、混合氣經背壓閥回收至儲存槽（避免損失 ³He）」；正常面板「典型用電：壓縮機 ~10.7 kW、冷卻水 ~10 kW、電子 ~3 kW，合計 ~25 kW」；右下小圖「停電後的變化（示意）」。
- animations/js/peripherals/10_bringup.js：11 步（系統檢查、讀取腔頻譜、Punch-out、量子位元頻譜、Rabi、Ramsey、T₁ 量測、讀取最佳化、DRAG / 閘微調、隨機基準測試、上線 ✓）；`ui.button('◀ 上一步')`、`ui.button('下一步 ▶')`（第 28–29 行）、`ui.toggle('自動播放', true)`（第 30 行）；上線面板「參數寫入資料庫，開放給編譯器與使用者；之後定期自動重新校準」。
- animations/power1000.html 場景「斷電時間軸：2 分鐘換 2–5 天」：備援方案 A／B／C（select），曲線為教學示意，時間點引用 LRZ／IQM。
