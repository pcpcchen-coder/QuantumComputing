# Q129 來源筆記（逐字引文）

查核日：2026-11-18（維基百科擷取：2026-11-19）。維基百科頁面由製作代理直接讀取原始 wikitext（index.php?action=raw；查 revision id 的 API 當時被限流，未取得 oldid）。學程內部文件、簡報與動畫程式由製作代理讀取。程式由製作代理實際執行。

## Uninterruptible power supply（Wikipedia，2026-11-19 raw wikitext）

- 「An uninterruptible power supply (UPS) or uninterruptible power source is an electrical apparatus that provides emergency power to a load when the input power source or mains power fails.」
- 「A UPS differs from an auxiliary or emergency power system or standby generator in that it will provide near-instantaneous protection from input power interruptions, by supplying energy stored in batteries, supercapacitors, or flywheels.」
- 本課的白話：「接在不斷電系統後面；市電一中斷，電池幾乎立刻接手」。

## Pulse tube refrigerator（Wikipedia，2026-11-19 raw wikitext）

- 「The so-called coefficient of performance (COP; denoted ξ) of coolers is defined as the ratio between the cooling power Q̇L and the compressor power P.」
- 「PTRs for temperatures below 20 K usually operate at frequencies of 1 to 2 Hz and with pressure variations from 10 to 25 bar. … Therefore, the compressor is uncoupled from the cooler. A system of valves (usually a rotating valve) alternately connects the high-pressure and the low-pressure side of the compressor to the hot end of the regenerator.」
- 本課的白話：冷卻能力和壓縮機用電的比值（約 1.5 W ÷ 10 kW）很小，「一萬瓦的電只換到一點五瓦的冷」。

## 技術分享：量子電腦的供電設計（slides/output/qc-power-supply.pptx）

- p5「超導：用電設備」：「脈衝管壓縮機｜每台 10–15 kW｜最大負載；三相、不能斷、啟動電流大」「冷卻水（冰水機、泵浦）｜另需 10 kW 以上」「氣體處理系統（GHS）｜數 kW」「精密 DC 偏壓源｜每模組約 30 W｜nV/√Hz 雜訊、µV 漂移、低串擾」「整套（20 位元級）｜降溫峰值約 30 kW｜LRZ 實測；Google 整套最壞約 26 kW」。
- p6「耗電量不是問題」：「一套超導量子電腦約 20–30 kW，比一個 HPC 機櫃（約 140 kW）還小」「中性原子不需要稀釋冷凍機，約 3–10 kW，主要負載是雷射」「真正的挑戰是供電品質，以及不能斷電」；圖說「HPC 機櫃＝Cray EX4000」。
- p2–p4 為脈絡、一頁結論與文獻分類（「三個平台都不耗電，怕的東西不同」）。課綱列 p2–6；本集實際引用 p5、p6 的數字，p2–p4 只作脈絡。

## 量子電腦的周邊系統（slides/QC_Peripheral_Systems_Talk.pptx）p30

- 「電力：一套系統約 25 kW」「Google Sycamore：冷凍 ~10 kW + 冷卻水 ≥10 kW + 電子 ~3 kW，最壞 ~26 kW（Arute et al., 2019 補充資料）」
- 「三相市電（壓縮機、冷卻水機）」「UPS 供應：控制電子、電腦、GHS 控制器與閥門、溫控器、監控網路」

## 量子電腦供電設計：文獻回顧與我們的切入點（docs/）

- §0：「三個平台的耗電量都不大，『供電品質』和『不能斷』才是重點」；「超導的磁通偏壓（µV）」；「合規的漏電流（mA 等級）…都可能比量子位元能容忍的高好幾個數量級」。
- §1 表：與簡報 p5 相同；「中性原子：不需要稀釋冷凍機…這類系統的主要負載是雷射」。
- §7.1：「【推論】離子阱的電力大宗是『讓光路和雷射保持穩定的環境設備』…離子阱的大宗是精密空調與雷射冷卻水」；Quantinuum Helios「基本機組 < 40 kW」。
- §17 表：用電大宗——超導「稀釋冷凍機壓縮機（每台 10–15 kW）＋冷卻水」、離子阱「精密空調與雷射冷卻水、雷射、控制電子」、中性原子「精密空調與冷卻水、雷射（光纖放大器）、控制電子／GPU」；單套功率——超導「約 20–30 kW」、中性原子「約 3–10 kW」。

## 1,000 量子位元超導系統的供電設計（docs/）

- §4.1 用電預算【推論】：壓縮機 37.5–62.5、GHS 與泵 3–5、冰水機與泵 15–40、室溫控制電子 10–100、精密直流 3–7、時脈網路伺服器 2–5、即時解碼 5–50、電子區空調 5–50 kW；「合計 約 80 kW／約 320 kW；各項中點合計約 200 kW」。
- §5：「約 2,500–3,000 路精密直流：以 24 通道、2U 的市售儀器計算，約 105–125 台」。

## 動畫原始碼

- `animations/power1000.html` 場景 1 `overview`：標題「全景：電從哪裡來、到哪裡去」、副標「推論：1,000 位元設施約 80–320 kW（中點合計約 200 kW）」；節點「中壓進線／雙迴路＋發電機」「分層 UPS／80–270 kW」「機電匯流排 約 80 kW」「乾淨匯流排 約 70 kW」「運算匯流排 約 30 kW」；八個負載與區間同 §4.1；說明「粒子密度代表功率。紅色編號是痛點，點擊可看說明」；痛點 2「壓縮機：最大的單一負載」「每支脈衝管 ≈ 12.5 kW 壓縮機」、痛點 3「約 250–350 台設備，每台 0.5–1 mA 漏電流 → 地線 0.1–0.35 A → 數百 µV 到 mV 的地電位，偏壓要求是 µV」、痛點 4「2,500–3,000 路精密直流」「約 110 台 24 通道儀器」、痛點 7「解碼要緊鄰機台」；面板「設施總功率（中點）約 200 kW」。
- `animations/js/peripherals/common.js` `PD.power`：「脈衝管壓縮機 10.7、冷卻水系統 10.0、控制電子機櫃 3.0、氣體處理系統（泵）1.5、電腦 / 監控 / 網路 1.0」；`01_overview.js` 插圖標題「典型用電分配（kW，示意）」、頁尾「合計約 26 kW（依機型與規模而異）」；連接按鈕與「只看冷卻相關」「只看訊號相關」。
- `02_pulsetube.js`：「氦壓縮機 電力 ~10 kW · 水冷」「一級冷端 ~45 K（~40 W）」「二級冷端 ~3 K（~1.5 W @ 4.2 K）」；說明「壓縮機把氦氣壓縮到高壓（約 2 MPa），熱量交給冷卻水帶走」。
- `08_infra.js` 說明：「電力：三相市電 → 配電盤。壓縮機與冷卻水機直接由配電盤供電（功率大）；控制電子、電腦、GHS 控制器與閥門接 UPS」「冷卻水：壓縮機約 10 kW 的熱要由冷卻水帶走」。

## power_inventory.py 實跑（Python 3.13.18，無外部套件，無亂數）

完整輸出見 `classroom.py` 的 RUN_OUTPUT：一套 26.2 kW；冷凍 12.2（47%）、控制電子 3.0（11%）、設施 11.0（42%）；保冷 22.2 kW 佔 85%；1,000 位元 80.5–319.5 kW、中點 200 kW ＝ 1.4 個 HPC 機櫃；一套系統 ＝ HPC 機櫃的 19%。
