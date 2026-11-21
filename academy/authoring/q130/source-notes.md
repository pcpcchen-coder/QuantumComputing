# Q130 來源筆記（逐字引文）

查核日：2026-11-18。LRZ／IQM 論文由製作代理讀取 arXiv HTML 全文（arxiv.org/html/2509.12949）與 arXiv API 摘要；維基百科頁面由製作代理直接讀取原始 wikitext（revision id 取自 MediaWiki API）。學程內部文件、簡報與動畫程式由製作代理讀取。程式由製作代理實際執行。

## LRZ／IQM：First Practical Experiences Integrating Quantum Computers with HPC Resources: A Case Study With a 20-qubit Superconducting Quantum Computer（arXiv:2509.12949）

- 摘要：「Here we report the integration of a superconducting 20-qubit quantum computer into the HPC infrastructure at Leibniz Supercomputing Centre (LRZ)」「(3) redundant power and cooling infrastructure is essential」
- §3.6 Recovering from outages：「Unplanned warm up events can also be caused by the cooling water temperature exceeding the upper temperature limit, triggering a shutdown of the cryogenic pumps. Once active cooling ceases, the calibration state of the QPU can be largely maintained if the QPU temperature remains below 1K. In practice, it takes two minutes to exceed this temperature after a fault in the cooling system.」
- 「Fortunately, the vacuum integrity of the system is typically maintained during outages for several weeks, unless the system is deliberately opened or physically moved.」
- 「Once the issue is addressed, the cryostat must be cooled down to its operating temperature, a process that can take from two to five days depending on the thermal mass of the cryostat and the temperature reached during the outage. Once the system is below 100 mK, and ideally back to 10 mK, recalibration and benchmark verification of the system can occur.」
- 結論：「worst case scenarios resulting in cryostat cooldown periods of up to ten days and the need for a full calibration after cooldown. The presence of redundant cooling water and uninterruptible power supplies mitigates these risks.」
- 論文提到自動校準讓系統「more than 100 days of continuous operation」，未寫「運轉一年多」；本集旁白只說「放進機房實際運轉」。

## Uninterruptible power supply（Wikipedia，oldid=1372628605）

- 「A UPS differs from an auxiliary or emergency power system or standby generator in that it will provide near-instantaneous protection from input power interruptions, by supplying energy stored in batteries, supercapacitors, or flywheels.」
- 「The on-battery run-time of most uninterruptible power sources is relatively short (typically ranging from 5 to 15 minutes) but sufficient to start a standby power source or properly shut down the protected equipment.」

## Dilution refrigerator（Wikipedia，oldid=1375073377，引自 Q104 來源筆記）

- 「A 3He/4He dilution refrigerator, or simply dilution refrigerator, is a cryogenic device that provides continuous cooling to temperatures as low as 2 mK, with no moving parts in the low-temperature region.」

## 學程內部簡報：slides/output/qc-power-supply.pptx

- 第 7 頁「斷電的代價：2 分鐘換數天」：「約 2 分鐘／冷卻中斷 → 超過 1 K／1 K 以下：校準狀態大多保得住　超過 1 K：必須整套重新校準」「2–5 天／重新降溫／最壞情況約 10 天　降到 100 mK 以下才開始重新校準」「數週／真空還撐得住／損失主要是停機時間與校準時間　不是硬體損壞」「冷卻水超過溫度上限，也會讓低溫泵浦跳機 → 冰水機也是關鍵負載（LRZ arXiv:2509.12949）」「▶ 動畫：斷電時間軸」。
- 第 8 頁「推論：備援要怎麼設計」：「UPS 範圍／涵蓋整條冷卻鏈／壓縮機、GHS、冰水機泵浦與控制　不能只顧控制電子　撐到發電機與 ATS 接手」「冷卻水／蓄冷桶／緩衝水槽／冰水機停了，泵浦照常循環　幾分鐘內水溫不超過上限」「啟動電流／壓縮機與 UPS 一起設計／軟啟動或變頻驅動　UPS 容量可以小一個級距」。
- 第 8 頁講者備註：「這一頁是我根據文獻推出來的設計原則，沒有直接出處。可以容忍的中斷時間大約兩分鐘，比發電機啟動加自動切換開關的十到三十秒長，但比修好一台冰水機短很多。」
- 課綱寫 p7–8，內容確實在第 7、8 頁（第 6 頁是「耗電量不是問題」）。

## 學程內部文件：docs/量子電腦供電設計文獻回顧與我們切入點.md §2

- 「LRZ 把 IQM 20 位元超導機放進超算中心，運轉了一年多。」（論文本文未見此說法，本集不採用「一年多」）
- 「【推論】…可容忍的中斷時間只有約 2 分鐘，這比發電機啟動加上 ATS 切換（約 10–30 秒）長，但比修好一台冰水機短。所以 UPS 必須涵蓋整條冷卻鏈，包括 PT 壓縮機、GHS、冰水機的泵浦與控制，不能只顧控制電子。UPS 的任務是撐到發電機接手。」
- 「冷卻水這一側可以加蓄冷桶或緩衝水槽。」「壓縮機的啟動電流與 UPS 容量必須一起設計。軟啟動或變頻驅動可以大幅降低 UPS 需要的容量」
- §6 切入點 1：「壓縮機停機後再啟動通常要等一段時間，需要和 OEM 確認」。

## 互動動畫程式

- animations/power1000.html 場景 5（id: outage）：標題「斷電時間軸：2 分鐘換 2–5 天」、副標「示意曲線：依 LRZ 公開數據（約 2 分鐘超過 1 K、恢復 2–5 天）繪製」；說明「時間軸是對數座標（1 秒到 10 天），曲線是混合腔溫度」「曲線為教學示意，非實測」。
  控制項：select「備援方案」（none「A：只有控制電子接 UPS」、full「B：冷卻鏈 UPS＋發電機接手」、gen「C：冷卻鏈 UPS，但發電機沒起來」）；range「UPS 撐住冷卻鏈的時間（方案 C）」5–60 分、預設 15。兩者改變時 st.play = 0。
  curve()：A 的 t0 = 0、B 為 Infinity、C 為 UPS 分鐘 × 60；升溫 0.01 × (1 + Δt/1.2) K（約 120 秒到 1 K），1 小時後恢復、3.5 天對數降回 0.01 K。刻度 1 秒、1 分、2 分、1 小時、1 天、5 天；1 K 紅色虛線與「超過 1 K → 需要完整校準」；白點 12 秒走完一輪；讀數「方案」「冷卻鏈負載 55–110 kW」「停機時間（示意）」：A「約 3–5 天（含重新降溫與完整校準）」、B「0（不受影響）」、C「約 3–5 天（UPS 耗盡後同 A）」。
- animations/js/peripherals/04_cooldown.js（peripherals.html#cooldown）：副標「乾式稀釋冷凍機一次完整降溫約 1–2 天；升溫回室溫也需約 1 天」；phase()「① 抽真空 / 檢漏」(<2 h)「② 脈衝管預冷」(<25 h)「③ 凝結混合氣」(<27.5 h)「④ 稀釋循環 → 基溫」(<33 h)「✓ 基溫穩定，可開始量測」；說明「② 脈衝管預冷…這是最耗時的階段」「④ 循環…MXC 在數小時內降到 ~10 mK」；控制項「時間 (小時)」0–36、「⏸ 暫停」「⟲ 重新開始」「播放速度（小時/秒）」；液滴 0x8ef0ff 只在 25–28 h 顯示；readout「時間尺度為典型示意，依機型與負載而異」。
- animations/js/peripherals/09_monitor.js（peripherals.html#monitor）：標題「監控、聯鎖與故障處置」；說明「聯鎖（interlock）：冷卻水溫過高 → 壓縮機停機；停電或控制器異常 → 閥門關閉、混合氣經背壓閥回收至儲存槽，保護昂貴的 ³He。」；按鈕「正常運轉」「冷卻水中斷」「真空洩漏」「流阻堵塞」；water 情境 water = 18 + 2.2·tf（上限 48），>27 °C ALARM、否則 WARN，<32 °C 壓縮機運轉，否則「水溫超限 → 聯鎖停止壓縮機；GHS 準備回收混合氣」；告警球綠／黃／紅、ALARM 時跳動；recov 紫色流到混合氣儲存槽；溫度計小球比值 >3 紅、>1.3 黃；右下「監控曲線（最近 60 秒，時間加速）」。

## 製作代理試拍（2026-11-18，Playwright 單張截圖，nice -n 19，非正式錄影）

- pw#outage：選 none 後 4.6 秒「t = 3.3 分 MXC ≈ 1.6 K」、7.6 秒「t = 1.7 小時 MXC ≈ 28.1 K」、12.3 秒「t = 10.0 天 MXC ≈ 10 mK」；C＋30 分：曲線平到 30 分鐘後上升，讀數「約 3–5 天（UPS 耗盡後同 A）」。
- pe#cooldown：暫停後拖時間到 27 h 顯示「③ 凝結混合氣」與液滴；34–36 h 顯示「✓ 基溫穩定，可開始量測」、MXC ≈ 10.2–11.5 mK。
- pe#monitor：正常運轉「狀態：OK…冷卻水入水 18.0 °C…壓縮機 運轉」；按冷卻水中斷後 WARN → ALARM →「壓縮機 停止」，入水封頂 48.0 °C；50 K 級溫度計為黃色、其餘轉紅。

## 實跑紀錄（outage_timeline.py，Python 3.13.18，無外部套件）

```
容忍時間 2 分鐘；發電機接手 30 秒
A 只有控制電子接 UPS，市電停 1 分鐘：冷卻鏈停 1 分鐘 → 保住：1 K 以下
A 只有控制電子接 UPS，市電停 5 分鐘：冷卻鏈停 5 分鐘 → 超過 1 K：停機 2–5 天＋完整校準
B 冷卻鏈接 UPS＋發電機，市電停 3 小時：冷卻鏈停 0 分鐘 → 保住：1 K 以下
C 冷卻鏈接 UPS、發電機沒起來，市電停 10 分鐘：冷卻鏈停 0 分鐘 → 保住：1 K 以下
C 冷卻鏈接 UPS、發電機沒起來，市電停 16 分鐘：冷卻鏈停 1 分鐘 → 保住：1 K 以下
C 冷卻鏈接 UPS、發電機沒起來，市電停 60 分鐘：冷卻鏈停 45 分鐘 → 超過 1 K：停機 2–5 天＋完整校準
6 個案例，保住 4 個
```
