# QuantumComputing

量子計算學習筆記。

## 筆記目錄

> 所有簡報都另附 PDF 版：[`slides/pdf/`](slides/pdf/)（`JJ_Microwave_Readout_Talk.pdf`、`QC_Peripheral_Systems_Talk.pdf`、`QC_Operation_Talk.pdf`、`Ion_NeutralAtom_Talk.pdf`、`transmon.pdf`、`QC_Power_Supply.pdf`、`QFISH008_Deutsch_Algorithm.pdf`、`Basic_Quantum_Circuits.pdf`）。

1. [約瑟夫森結（JJ）：巨觀量子波、相位差與「穿隧」的真正意義](notes/josephson-junction-wave-and-tunneling.md)
2. [Transmon：約瑟夫森電感、電路結構與量子位元機制](notes/transmon-josephson-inductance.md)
   - 簡報：[`slides/transmon.pptx`](slides/transmon.pptx)（27 頁，PowerPoint；每頁右上角「▶ 3D 第 N 章」按鈕直接開啟動畫，第 17–26 頁為 3D 動畫導覽與十二章的介紹：操控與讀取、案例、振幅長條、Shor、BV 密碼、表面碼、邏輯閘、軟體堆疊；產生腳本 [`slides/build/add_transmon_3d_links.py`](slides/build/add_transmon_3d_links.py)）
   - 3D 互動動畫：[`animations/transmon-3d.html`](animations/transmon-3d.html)（12 章；第 5 章「讀取」為 8 步驟導覽：色散偏移、IQ、讀取鏈、單發積分與判別、QND、讀完後的重設方式；第 6 章「案例」示範 SQUID 調頻、頻率配置與頻率碰撞、XY 寫入、CZ 原理（能階圖上 |11⟩ 與 |20⟩ 交會、|20⟩ 比例與相位變化、四種輸入對照、沒有 JJ 的對照）與 CZ 實戰；第 7 章「振幅長條」示範糾纏、兩位元 Grover 搜尋與 Deutsch 演算法；第 8 章示範 Shor 演算法（QFT 找週期分解 15，可自選 N、a、計數位元數）；第 9 章「BV 密碼」為基本操作案例：3 顆位元用 Bernstein–Vazirani 演算法只查詢一次猜出密碼（可隱藏密碼猜謎、和古典查詢比賽）；第 10 章「表面碼」示範量子錯誤更正：d = 3 表面碼的穩定子、一個週期的 CZ 順序、X/Z/Y 錯誤與邊界、最小權重完美匹配解碼、兩個錯誤造成邏輯錯誤、碼距與閾值（自由實驗可點位元注入錯誤、換 d = 3/5/7、跑蒙地卡羅統計）；第 11 章「邏輯閘」示範 lattice surgery（兩塊 d = 3 補丁合併量 X_A·X_B、拆開、三步 CNOT、T 閘傳送）與 15-to-1 魔術態蒸餾工廠（可調注入錯誤率、跑統計）；第 12 章「軟體堆疊」跟著電路走完整條編譯與控制堆疊（七層架構、分解成 Rz／√X／CZ、校準感知映射、SWAP 路由、H·H 抵消與 Rz 合併、ASAP 排程與脈衝時間軸、FPGA 即時回饋、2000 shots 結果、校準依賴圖；自由實驗可選 Bell／GHZ／BV 與直線／方格晶片比較 SWAP 數與總時間）；線上版 https://pcpcchen-coder.github.io/QuantumComputing/animations/transmon-3d.html，或下載後用瀏覽器開啟（已內附 three.js，離線可用）；網址加 `#deutsch` 直接進 Deutsch 步驟、`#deutsch-lab` 進自由實驗）
   - 2D 互動圖解：[`animations/lc-vs-jj.html`](animations/lc-vs-jj.html)（線上版 https://pcpcchen-coder.github.io/QuantumComputing/animations/lc-vs-jj.html；transmon.pptx 第 4–8、14、16 頁有「▶ 圖解」按鈕；為什麼 LC 是線性、JJ 是非線性；6 步：電流–磁通曲線與等效電感 L_J、正弦驅動與諧波、拋物線 vs 餘弦位能與數值對角化能階、躍遷頻率與 qubit 定址、泰勒展開的四次項、DRAG 脈衝抑制洩漏到 |2⟩（三能階 RK4 模擬、頻譜缺口、洩漏 vs 閘長度）；單一 HTML 檔，離線可用（字型需連網，離線時自動改用系統字型）；屬獨立圖解頁，未列入下方動畫 ↔ 簡報對照表）
   - 教學紀錄：[`docs/超導量子電腦師生對話教學紀錄.md`](docs/超導量子電腦師生對話教學紀錄.md)（師生對話形式，3 篇 13 課：SQUID、寫入、頻率配置、能階與 Rabi、讀取、BV、糾纏與 Grover、Deutsch、Shor、表面碼、lattice surgery 與魔術態、軟體堆疊；每課附學習目標、重點整理、動畫連結與課後練習）
3. [色散讀取：用諧振腔頻率「看見」超導量子位元](notes/dispersive-readout.md)（原理、IQ 判別、設計取捨、整條讀取鏈設備與校準流程）
   - 對應動畫：[`animations/index.html`](animations/index.html) 場景 9、10；[`animations/peripherals.html`](animations/peripherals.html) 場景 5、6
4. [技術分享：超導量子電腦的 JJ 元件與微波讀取](#技術分享超導量子電腦的-jj-元件與微波讀取)
   - 簡報：[`slides/JJ_Microwave_Readout_Talk.pptx`](slides/JJ_Microwave_Readout_Talk.pptx)（43 頁，含講者備註）
   - 演講稿：[`speech/演講稿.md`](speech/演講稿.md)
   - 3D 互動動畫：[`animations/index.html`](animations/index.html)（11 個場景，離線可用）
5. [技術分享（續篇）：量子電腦的周邊系統與整合](#技術分享續篇量子電腦的周邊系統與整合)
   - 簡報：[`slides/QC_Peripheral_Systems_Talk.pptx`](slides/QC_Peripheral_Systems_Talk.pptx)（42 頁，含講者備註）
   - 演講稿：[`speech/周邊系統演講稿.md`](speech/周邊系統演講稿.md)
   - 建置文件：[`docs/周邊系統連接與啟動指南.md`](docs/周邊系統連接與啟動指南.md)（連接清單、啟動流程、異常處置）
   - 3D 互動動畫：[`animations/peripherals.html`](animations/peripherals.html)（10 個場景，離線可用）
6. [技術分享（第三篇）：如何操作量子電腦——設定、計算、讀取與加速原理](#技術分享第三篇如何操作量子電腦)
   - 簡報：[`slides/QC_Operation_Talk.pptx`](slides/QC_Operation_Talk.pptx)（56 頁，含講者備註）
   - 演講稿：[`speech/量子電腦操作演講稿.md`](speech/量子電腦操作演講稿.md)
   - 3D 互動動畫：[`animations/operation.html`](animations/operation.html)（12 個場景，離線可用）
7. [技術分享（第四篇）：離子阱與中性原子量子電腦——系統、量子位元、操作與量測](#技術分享第四篇離子阱與中性原子量子電腦)
   - 簡報：[`slides/Ion_NeutralAtom_Talk.pptx`](slides/Ion_NeutralAtom_Talk.pptx)（56 頁，含講者備註；PDF：[`slides/pdf/Ion_NeutralAtom_Talk.pdf`](slides/pdf/Ion_NeutralAtom_Talk.pdf)）
   - 演講稿：[`speech/離子阱與中性原子演講稿.md`](speech/離子阱與中性原子演講稿.md)
   - 系統指南：[`docs/離子阱與中性原子系統指南.md`](docs/離子阱與中性原子系統指南.md)（子系統、連接清單、啟動校準流程、異常處置、設施與電力）
   - 教學紀錄：[`docs/離子阱與中性原子師生對話教學紀錄.md`](docs/離子阱與中性原子師生對話教學紀錄.md)（師生對話形式，6 課：離子阱怎麼運算 / 讀取（超導對照）、氫邁射、中性原子怎麼運算 / 讀取、頻率基準與原子鐘、MS 閘 vs 芮德堡 CZ）
   - 3D 互動動畫：[`animations/atoms.html`](animations/atoms.html)（17 個場景，離線可用）
8. [影片報告簡報：《量子超級英雄》影片轉 PPT](#影片報告簡報量子超級英雄影片轉-ppt)
   - #049 超導量子位元：[`slides/output/ep049-superconducting-qubit.pptx`](slides/output/ep049-superconducting-qubit.pptx)（16 頁，含講稿）
   - 量子金魚 008 Deutsch 演算法：[`slides/output/qfish008-deutsch-algorithm.pptx`](slides/output/qfish008-deutsch-algorithm.pptx)（30 頁，含講稿；依影片逐字稿整理，另附「案例實算」：紅綠球搖獎機、振幅逐步計算、四種黑盒子、現場猜謎；每個案例都有按鈕直接開啟 3D 動畫）；PDF：[`slides/pdf/QFISH008_Deutsch_Algorithm.pdf`](slides/pdf/QFISH008_Deutsch_Algorithm.pdf)
   - 製作流程與產生器：[`slides/README.md`](slides/README.md)
9. [3D 動畫 ↔ PPT 簡報對照表](#3d-動畫--ppt-簡報對照)（摘要見下方；完整逐場景表格：[`docs/動畫與簡報對照表.md`](docs/動畫與簡報對照表.md)；5 個動畫頁、56 個場景／章節，逐一列出對應的簡報頁碼與動畫網址；`python3 slides/build/anim_ppt_map.py` 重新產生並檢查缺口）
10. [課程擴充規劃：量子電腦學院（參考父子科技學院格式，6 模組 × 16 堂）](docs/量子電腦學院_課程擴充規劃.md)（現有 223 頁簡報與 47 個 3D 場景的盤點、Q001–Q096 課表、新增動畫與簡報清單）
   - 學程資料夾：[`academy/`](academy/README.md)（96 堂課綱、每堂教案、製作指南、製作狀態）
11. [量子電腦供電設計：文獻回顧與我們的切入點](docs/量子電腦供電設計文獻回顧與我們切入點.md)（超導、離子阱、中性原子三平台分篇細部分析：精密電源、不斷電與分層備援、低干擾設計、能耗擴展，以及我們的產品 × 平台矩陣）
    - 簡報：[`slides/output/qc-power-supply.pptx`](slides/output/qc-power-supply.pptx)（77 頁，含講稿）；PDF：[`slides/pdf/QC_Power_Supply.pdf`](slides/pdf/QC_Power_Supply.pdf)
    - 簡報內容檔：[`slides/reports/qc-power.js`](slides/reports/qc-power.js)（`cd slides && node build_deck.js reports/qc-power.js` 重新產生）
    - 1,000 位元系統供電設計：[`docs/1000量子位元系統供電設計.md`](docs/1000量子位元系統供電設計.md)（線路與熱預算估算、設施用電與備援、接地與磁場、七層技術、我們三階段路線圖；簡報第 47–59 頁）
    - 互動動畫：[`animations/power1000.html`](animations/power1000.html)（8 個 2D 互動場景：全景、規模計算器、低溫熱預算、接地與共模、斷電時間軸、磁場與配電佈局、路線圖、開發計畫；離線可用）
    - 產品開發計畫：[`docs/我們量子供電產品開發計畫.md`](docs/我們量子供電產品開發計畫.md)（三階段路線圖 11 個項目：要做出什麼、開發步驟、困難與解法、檢查點）

12. 基礎量子電路互動動畫：[`animations/basic-circuits.html`](animations/basic-circuits.html)（線上版 https://pcpcchen-coder.github.io/QuantumComputing/animations/basic-circuits.html）
    - 先備理論：[`animations/quantum-basics.html`](animations/quantum-basics.html)〈量子理論基礎：看電路前的 6 堂課〉（量子位元與振幅、相位、量測與 Born 規則、量子閘＝么正矩陣、張量積與糾纏、干涉；每堂都有可拖拉的互動圖，網址加 `#qubit`、`#phase`、`#measure`、`#gates`、`#tensor`、`#interference`）
    - 10 個範例：疊加（|0⟩/|1⟩ 起始）、干涉 H‑Z‑H = X（可拿掉 Z 比較）、Bell 態（Φ⁺/Φ⁻/Ψ⁺/Ψ⁻）、GHZ 態（3 或 4 顆）、量子隱形傳態（四種 ψ，延遲量測版）、Deutsch 演算法（四種黑盒）、Bernstein–Vazirani（可自訂 3 位元密碼）、Grover 搜尋（2 或 3 顆位元、可選答案與 1–3 輪，平均值虛線看「對平均值翻轉」）、量子傅立葉轉換（基底態或週期態輸入，振幅下方的相位指針與三顆 Bloch 球看「位置變頻率」）、Shor 演算法（分解 15，a = 7、2、11、14；量測後自動做連分數與 gcd 後處理）
    - 每個範例都能逐步播放電路，同時顯示振幅長條（正負號分色）、狀態式子與 Bloch 球（Bell、隱形傳態、Deutsch 畫「單看某一顆位元」的 Bloch 球，看得出糾纏時向量縮短），也能量測 1 次或 1,000 次，對照理論機率；附會隨選項改變的 Qiskit 程式碼
    - 簡報：[`slides/output/basic-circuits.pptx`](slides/output/basic-circuits.pptx)（48 頁，含講稿；開頭「理論基礎」6 堂課 10 頁，每個範例都有電路圖、振幅逐步長條與表格，右上角「▶ 動畫」按鈕直接開到該範例）；PDF：[`slides/pdf/Basic_Quantum_Circuits.pdf`](slides/pdf/Basic_Quantum_Circuits.pdf)；內容檔：[`slides/reports/basic-circuits.js`](slides/reports/basic-circuits.js)（`cd slides && node build_deck.js reports/basic-circuits.js` 重新產生，截圖用 `node slides/capture_basic_circuits.js` 重新擷取）
    - 網址加 `#superposition`、`#interference`、`#bell`、`#ghz`、`#teleport`、`#deutsch`、`#bv`、`#grover`、`#qft`、`#shor` 可直接開啟指定範例；單一 HTML 檔，離線可用（字型需連網）；頁內模擬器支援複數振幅，88 種選項組合都已和 Qiskit `Statevector` 比對過，結果一致（Grover 的擴散照理想「對平均值翻轉」計算，和 H、X、多控制 Z 組成的電路只差一個整體負號）

---

## 3D 動畫 ↔ PPT 簡報對照

`animations/` 共 9 個動畫頁、91 個場景／章節／段落（含 2D 圖解 `lc-vs-jj.html` 的 7 段、`basic-circuits.html` 的 10 個範例、`quantum-basics.html` 的 6 堂課），**每一個都有對應的簡報投影片**。簡報上的「▶ 3D」按鈕直接開啟線上動畫，網址格式為 `https://pcpcchen-coder.github.io/QuantumComputing/animations/<頁面>.html#<場景代號>`（動畫首頁：<https://pcpcchen-coder.github.io/QuantumComputing/>）。離線時可改開 repo 內的 `animations/<頁面>.html#<場景代號>`。

逐場景的完整表格（含投影片標題與可點的動畫網址）：[`docs/動畫與簡報對照表.md`](docs/動畫與簡報對照表.md)。新增動畫或簡報後執行下列指令，會重新產生該表格與本段的總覽、頁碼表，並列出還沒有投影片介紹的場景（有缺口時結束碼為 1）：

```bash
python3 slides/build/anim_ppt_map.py
```

### 線上版（GitHub Pages）與全白畫面排除

動畫發布在 GitHub Pages：<https://pcpcchen-coder.github.io/QuantumComputing/>（首頁列出全部動畫）。`main` 上的 `animations/` 有變動時，[`.github/workflows/pages.yml`](.github/workflows/pages.yml) 會自動重新發布；網站只包含 `animations/` 與首頁 [`site/index.html`](site/index.html)，不含簡報、筆記與其他文件。

**第一次啟用（需要 repo 管理員在 GitHub 網頁上操作一次）**：Settings → Pages → Build and deployment → Source 選 **GitHub Actions**，再到 Actions 分頁手動執行一次「Deploy animations to GitHub Pages」。私人 repo 要使用 Pages，帳號需要 GitHub Pro／Team 以上的方案；而且發布出去的網站是公開的，任何人都能用網址開啟。

開啟動畫卻看到全白或全黑畫面時，常見原因：

| 情況 | 原因 | 處理 |
|---|---|---|
| 只下載單一 HTML，或在 GitHub 網頁、雲端硬碟、通訊軟體的預覽裡開啟 | `index`／`peripherals`／`operation`／`atoms` 需要同資料夾的 `css/`、`js/`、`lib/`，缺檔時原本會是一片白 | 改開線上版，或下載整個 `animations/` 資料夾；現在缺檔時會顯示原因與線上版連結 |
| 瀏覽器無法使用 WebGL（硬體加速關閉、遠端桌面、舊瀏覽器） | 3D 場景無法建立 | 改用桌面版 Chrome／Edge／Safari／Firefox 並開啟硬體加速；現在會顯示提示，不再是空白 |
| `transmon-3d.html` 離線開啟 | 原本從網路載入 three.js | 已內附 `lib/three-r128.min.js`，離線也能開啟；只有單一檔案又離線時才會顯示提示 |

<!-- anim-map:begin -->
### 總覽

> 這一段由 `python3 slides/build/anim_ppt_map.py` 自動更新，請不要手動修改。

| 動畫（線上版） | 場景數 | 對應簡報 | 狀態 |
|---|---|---|---|
| [`index.html`](https://pcpcchen-coder.github.io/QuantumComputing/animations/index.html)：JJ 元件與微波讀取 | 11 | [`JJ_Microwave_Readout_Talk.pptx`](slides/JJ_Microwave_Readout_Talk.pptx) | ✅ 全部有 |
| [`peripherals.html`](https://pcpcchen-coder.github.io/QuantumComputing/animations/peripherals.html)：量子電腦周邊系統 | 10 | [`QC_Peripheral_Systems_Talk.pptx`](slides/QC_Peripheral_Systems_Talk.pptx) | ✅ 全部有 |
| [`operation.html`](https://pcpcchen-coder.github.io/QuantumComputing/animations/operation.html)：如何操作量子電腦 | 12 | [`QC_Operation_Talk.pptx`](slides/QC_Operation_Talk.pptx)；[`qfish008-deutsch-algorithm.pptx`](slides/output/qfish008-deutsch-algorithm.pptx) | ✅ 全部有 |
| [`atoms.html`](https://pcpcchen-coder.github.io/QuantumComputing/animations/atoms.html)：離子阱與中性原子 | 17 | [`Ion_NeutralAtom_Talk.pptx`](slides/Ion_NeutralAtom_Talk.pptx) | ✅ 全部有 |
| [`transmon-3d.html`](https://pcpcchen-coder.github.io/QuantumComputing/animations/transmon-3d.html)：Transmon 3D（12 章） | 14 | [`transmon.pptx`](slides/transmon.pptx)；[`qfish008-deutsch-algorithm.pptx`](slides/output/qfish008-deutsch-algorithm.pptx) | ✅ 全部有 |
| [`power1000.html`](https://pcpcchen-coder.github.io/QuantumComputing/animations/power1000.html)：1,000 位元供電設計 | 8 | [`qc-power-supply.pptx`](slides/output/qc-power-supply.pptx) | ✅ 全部有 |
| [`lc-vs-jj.html`](https://pcpcchen-coder.github.io/QuantumComputing/animations/lc-vs-jj.html)：LC 與約瑟夫森接面（2D 圖解） | 7 | [`transmon.pptx`](slides/transmon.pptx) | ✅ 全部有 |
| [`basic-circuits.html`](https://pcpcchen-coder.github.io/QuantumComputing/animations/basic-circuits.html)：十個基礎量子電路（2D 互動） | 10 | [`basic-circuits.pptx`](slides/output/basic-circuits.pptx) | ✅ 全部有 |
| [`quantum-basics.html`](https://pcpcchen-coder.github.io/QuantumComputing/animations/quantum-basics.html)：量子理論基礎 6 堂課（2D 互動） | 6 | [`basic-circuits.pptx`](slides/output/basic-circuits.pptx) | ✅ 全部有 |

### 場景 → 投影片頁碼

主要簡報的頁碼不加前綴；其他簡報以簡稱標示（JJ、周邊、操作、離子阱、transmon、qfish008、供電、基礎電路）。

| 動畫 | 主要簡報 | 場景代號 → 頁碼 |
|---|---|---|
| **index.html** | JJ | bloch p5、6；cooper p7、8；jj p12、13；potential p10、15、19；washboard p16；squid p17；fab p21；chip p27、36；dispersive p28、29；iq p31；fridge p32、33 |
| **peripherals.html** | 周邊 | overview p3、11、35、36；pulsetube p8；dilution p9；cooldown p12；wiring p14–16；electronics p20、21；software p25；infra p30–33；monitor p27、28；bringup p26、37 |
| **operation.html** | 操作 | qubit p7、8；gates p18、19；pulse p14、20、21；register p9、10、43；twoqubit p23；circuit p25、28；readout p30、31、33；interference p38、39（另 qfish008 p14、15、18、25）；grover p40；shor p41；qec p49、50；workflow p3、52 |
| **atoms.html** | 離子阱 | ionsys p6；paul p7；ionqubit p13、16、19；modes p17；ms p18；qccd p20；ionflow p21、22；hmaser p23、24；atomsys p27；tweezer p30；atomqubit p33、34；rydberg p36–38；zoned p39；imaging p40；atomflow p41；atomclock p42；compare p47、48 |
| **transmon-3d.html** | transmon | chip p1、10、11、17、18、27；junction p4、5、18；potential p6–8、12、14、15、18；control p16、18、19；readout p16、18、19；case p16、18、20；grover p18、21；shor p18、22；bv p18、23；surface p18、24；surgery p18、25；stack p18、26；deutsch p21（另 qfish008 p13、20、23）；deutsch-lab p21（另 qfish008 p21、22、24） |
| **power1000.html** | 供電 | overview p47、52、56；scale p48、51、55；heat p49、50；ground p22、54；outage p7、53；field p24；roadmap p57–59；devplan p60–72 |
| **lc-vs-jj.html** | transmon | s1 p4、5；s2 p5；s3 p8、14；s4 p14；s5 p6；s6drag p16；s6 p7 |
| **basic-circuits.html** | 基礎電路 | superposition p13、14；interference p15–17；bell p18–20；ghz p21、22；teleport p23–25；deutsch p26–28、45；bv p29、30；grover p31–35；qft p36–38；shor p39–43 |
| **quantum-basics.html** | 基礎電路 | qubit p3；phase p4；measure p5；gates p6；tensor p7；interference p8 |
<!-- anim-map:end -->

### transmon-3d.html ↔ transmon.pptx

`transmon.pptx` 原本 17 頁、沒有任何動畫連結，現已補成 27 頁：既有 12 頁右上角加上青綠色「▶ 3D 第 N 章」按鈕，其中 7 頁另有銅色「▶ 圖解」按鈕連到 2D 圖解 [`lc-vs-jj.html`](https://pcpcchen-coder.github.io/QuantumComputing/animations/lc-vs-jj.html) 的對應段落（`#s1`–`#s6`、`#s6drag`），講者備註也附上網址；新增第 17–26 頁（3D 動畫導覽、操控與讀取、案例：頻率配置、振幅長條、Shor、BV 密碼、表面碼、邏輯閘、軟體堆疊），每頁都有 3D 截圖、按鈕與動畫網址。這份簡報由 [`slides/build/add_transmon_3d_links.py`](slides/build/add_transmon_3d_links.py) 從 `slides/build/transmon_base.pptx` 產生，截圖由 [`slides/capture_3d_transmon.js`](slides/capture_3d_transmon.js) 擷取（第 9–12 章另以 [`slides/build/autocrop_shots.py`](slides/build/autocrop_shots.py) 裁掉空白）。

各章對應的頁碼見上方「場景 → 投影片頁碼」。

> 簡報（.pptx 與 `slides/pdf/` 的 PDF）裡的動畫連結都是 GitHub Pages 網址，不必下載 repo 也能點開。所有簡報的連結由 [`slides/build/use_pages_links.py`](slides/build/use_pages_links.py) 統一改寫，各簡報產生器也已改用同一個網址。

---

## 技術分享：超導量子電腦的 JJ 元件與微波讀取

給同仁的內部技術分享：約瑟夫森接面（Josephson Junction, JJ）的相關知識，以及如何用微波讀取量子位元狀態。內容包含簡報、完整演講稿與互動 3D 動畫。

### 內容

| 路徑 | 說明 |
|---|---|
| `slides/JJ_Microwave_Readout_Talk.pptx` | 主簡報，43 頁，每頁都有詳細講者備註；右上角「▶ 3D 場景」按鈕可直接開啟對應動畫 |
| `speech/演講稿.md` | 完整演講稿（與講者備註同步）、時間規劃、60 分鐘精簡版建議、Q&A 準備、公式速查 |
| `animations/index.html` | 互動 3D 動畫（three.js，已內附函式庫，**離線可用**），共 11 個場景 |
| `slides/figures/` | 簡報用物理圖表（matplotlib）與 3D 場景截圖 |
| `slides/build/` | 產生簡報與圖表的腳本 |

### 簡報架構

1. **背景知識**：量子位元與 Bloch 球、品質指標（T1/T2）、超導與 Cooper pair、BCS 能隙、磁通量子化、為什麼需要非線性
2. **JJ 元件**：SIS 結構、DC/AC Josephson 關係、非線性電感、E_J 與 E_C、RCSJ 洗衣板、SQUID、量子位元家族、transmon 與電荷色散、Dolan bridge 製程、頻率定位、JJ 的其他角色（耦合器、JPA、TWPA…）、退相干來源
3. **微波讀取**：讀取需求、電路 QED、色散位移 χ、S21 振幅/相位、外差解調與 IQ、單發判別與保真度、稀釋冷凍機讀取鏈、輸入線衰減與熱光子、量子極限放大器、κ/χ/Purcell 設計權衡、多工與進階技術、數值範例
4. **整合與總結**：全流程、重點回顧、3D 動畫導覽、參考文獻、Q&A

### 3D 動畫

用瀏覽器開啟 `animations/index.html` 即可（Chrome / Edge / Firefox，無需網路與伺服器）。網址加 `#場景代號` 可直接跳轉。

| # | 代號 | 主題 |
|---|---|---|
| 1 | `bloch` | Bloch 球：Rabi 振盪、Ramsey + T2、T1 弛豫 |
| 2 | `cooper` | 超導與 Cooper pair（溫度滑桿：正常態 ↔ 超導態） |
| 3 | `jj` | JJ 三明治結構、Cooper pair 穿隧、DC/AC Josephson 效應 |
| 4 | `potential` | LC vs transmon 能階與波函數、E_J/E_C、電荷色散（數值對角化） |
| 5 | `washboard` | RCSJ 傾斜洗衣板位勢、相位粒子、I–V 遲滯 |
| 6 | `squid` | DC SQUID 磁通調頻、甜蜜點、不對稱 SQUID |
| 7 | `fab` | Dolan bridge 雙角度蒸鍍五步驟 |
| 8 | `chip` | Xmon 晶片、λ/4 讀取腔、饋線、頻率多工讀取 |
| 9 | `dispersive` | 色散讀取：±χ 頻移、振幅/相位響應、IQ 圓 |
| 10 | `iq` | 單發讀取軌跡、IQ 叢集、閾值判別、保真度（含放大器與 T1 效應） |
| 11 | `fridge` | 稀釋冷凍機讀取鏈：衰減、環行器、TWPA、HEMT、功率變化 |

操作：滑鼠拖曳旋轉、滾輪縮放、右鍵/Shift 拖曳平移；`←` `→` 切換場景、空白鍵暫停、`H` 隱藏面板（投影時使用）、`F` 全螢幕、`R` 重設視角。網址加 `?noui=1` 可直接以無面板模式開啟。

> PowerPoint 的按鈕連到線上版（`https://pcpcchen-coder.github.io/QuantumComputing/animations/index.html#…`）；離線時請直接開 repo 內的 `animations/index.html`。

### 重新產生簡報與圖表

```bash
cd slides/build && npm install && pip install matplotlib numpy
```

```bash
python3 slides/build/make_figures.py
```

```bash
cd slides/build && node build_deck.js
```

兩份簡報共用 `slides/build/deck_lib.js` 的版型。`build_deck.js` 同時輸出 `slides/JJ_Microwave_Readout_Talk.pptx` 與 `speech/演講稿.md`，修改講者備註只需改一處。3D 截圖（`slides/figures/3d/`）是以 Playwright 對 `animations/index.html?noui=1&clean=1#場景` 擷取。

### 字型

簡報使用「微軟正黑體（Microsoft JhengHei）」，方程式使用 Cambria，Windows / Office 皆內建。

---

## 技術分享（續篇）：量子電腦的周邊系統與整合

說明讓 10 mK 量子晶片真正運轉所需的所有周邊設備，以及它們如何連接、如何啟動到上線。

### 內容

| 路徑 | 說明 |
|---|---|
| `slides/QC_Peripheral_Systems_Talk.pptx` | 42 頁簡報：低溫系統、低溫佈線與封裝、控制電子學、軟體與運作、機房基礎設施、系統整合；每頁有講者備註 |
| `speech/周邊系統演講稿.md` | 與講者備註同步的演講稿、時間規劃、60 分鐘精簡版、Q&A 準備 |
| `docs/周邊系統連接與啟動指南.md` | 子系統規格、系統連接清單（冷卻／氣體／真空、訊號／資料／電力）、逐步啟動流程、日常監控、異常處置、升溫換樣 |
| `animations/peripherals.html` | 10 個 3D 場景（與 `index.html` 共用核心程式） |
| `slides/figures/3d_periph/` | 簡報用 3D 場景截圖 |

### 3D 場景

| # | 代號 | 主題 |
|---|---|---|
| 1 | `overview` | 機房全景：設備與 7 類連接（氦氣、冷卻水、混合氣、真空、微波/DC、資料/時脈、電力），可分類切換 |
| 2 | `pulsetube` | 脈衝管冷卻器與氦壓縮機：旋轉閥、蓄冷器、溫度梯度、壓力波形 |
| 3 | `dilution` | 稀釋冷凍原理：³He 循環路徑、相界面吸熱、Q̇ = 84ṅT² 互動計算 |
| 4 | `cooldown` | 降溫流程：抽真空 → 預冷 → 凝結 → 循環，各級溫度隨時間 |
| 5 | `wiring` | 低溫佈線：6 類線路與各級元件、依量子位元數估算熱負載 |
| 6 | `electronics` | 控制電子學：上傳 → 觸發 → 驅動 → 讀取 → 判別 → 回饋；外差 vs 直接合成；10 MHz 時脈 |
| 7 | `software` | 軟體堆疊：程式逐層下傳、結果回傳、校準資料庫 |
| 8 | `infra` | 機房基礎設施：電力/UPS、冷卻水、接地、防振；停電模擬 |
| 9 | `monitor` | 監控與聯鎖：冷卻水中斷、真空洩漏、流阻堵塞情境 |
| 10 | `bringup` | 啟動與校準 11 步驟與典型量測圖 |

### 重新產生

```bash
cd slides/build && node build_peripherals.js
```

數值來源：Krinner et al. (2019)、Bluefors／Oxford 規格與手冊、PT415/PT420 規格、Arute et al. (2019) 補充資料、各控制電子廠商公開規格等（詳見簡報參考資料頁與建置指南）。

---

## PDF 與相容性

- `slides/pdf/` 中的 PDF 由 LibreOffice 轉出；中文字型以 Noto Sans CJK TC 代替微軟正黑體，版面與 PowerPoint 相近但字形略有不同。
- 產生簡報時，`slides/build/apply_theme.js` 會為每頁的物件重新編號，修正 pptxgenjs 產生的重複 shape ID，否則 PowerPoint 開檔時會要求修復；箭頭線一律用 `deck_lib.js` 的 `link()` 繪製，不使用負的寬高。
- 修正既有 .pptx 的重複 ID：

```bash
cd slides/build && node fix_ids.js ../transmon.pptx
```

- 重新產生 PDF（需安裝 LibreOffice 與 `fonts-noto-cjk`）：

```bash
cd slides && soffice --headless --convert-to pdf --outdir pdf *.pptx
```

---

## 技術分享（第三篇）：如何操作量子電腦

回答四個問題：量子電腦可以算什麼？怎麼算（設定、各種量子閘）？怎麼讀取？為什麼可以加速、快在哪？

### 內容

| 路徑 | 說明 |
|---|---|
| `slides/QC_Operation_Talk.pptx` | 56 頁簡報：基礎、設定、計算、讀取、加速原理、實務與總結；每頁有講者備註 |
| `speech/量子電腦操作演講稿.md` | 與講者備註同步的演講稿、時間規劃、精簡版建議、Q&A 準備 |
| `animations/operation.html` | 12 個 3D 場景（與 `index.html` 共用核心程式；背後是狀態向量模擬，可自由操作） |
| `slides/figures/op/`、`slides/figures/3d_op/` | 簡報用圖表與 3D 場景截圖 |

### 簡報架構

1. **基礎**：古典位元 vs 量子位元、Bloch 球、Born 規則與 shots、2ⁿ 個振幅、糾纏
2. **設定**：兩種操作者（使用者 / 系統工程師）、初始化（被動 / 主動重置）、9 步校準流程、後端校準資料、送出工作的參數（shots、最佳化等級、DD、錯誤緩解…）
3. **計算**：單位元閘一覽、ZYZ 分解、微波脈衝（面積 → 角度、相位 → 軸）、DRAG 與虛擬 Z、兩位元閘（CNOT/CZ/SWAP/iSWAP）、CZ 與交叉共振的物理實現、各家原生閘、線路讀法、轉譯、Qiskit 範例、動態線路
4. **讀取**：讀取流程、量測基底（量 X/Y 先旋轉）、shots 與統計誤差、混淆矩陣與讀取誤差緩解、取樣 vs 期望值
5. **為什麼快**：常見誤解、三個資源（疊加、干涉、糾纏）、干涉、Deutsch–Jozsa、Grover、Shor、加速等級、古典模擬的極限、應用地圖、不會變快的事
6. **實務與總結**：錯誤預算、錯誤緩解、表面碼、低於門檻（Willow）、發展路線、操作檢查表

### 3D 場景

| # | 代號 | 主題 |
|---|---|---|
| 1 | `qubit` | 狀態與測量：θ/φ、單次/連續測量、塌縮、P̂ 隨 shots 收斂 |
| 2 | `gates` | 單位元閘：X Y Z H S T √X Rx/Ry/Rz，旋轉軸、矩陣、線路紀錄 |
| 3 | `pulse` | 微波脈衝：面積、相位、失諧、閘長、方波/高斯/DRAG 頻譜、虛擬 Z |
| 4 | `register` | 1–4 位元：2ⁿ 振幅、均勻疊加、Bell、GHZ、測量塌縮、模擬記憶體 |
| 5 | `twoqubit` | CZ（\|11⟩–\|20⟩ 迴避交叉、條件相位）與交叉共振（ZX） |
| 6 | `circuit` | 線路執行器：Bell、GHZ、干涉、Deutsch–Jozsa、Bernstein–Vazirani、Grover、隱形傳態、QFT；直方圖與雜訊 |
| 7 | `readout` | 讀取：量測基底、IQ 平面、閾值、積分時間、T₁ 衰減、讀取誤差緩解 |
| 8 | `interference` | 干涉：路徑振幅相加、偵測路徑破壞干涉、3 位元 Deutsch–Jozsa |
| 9 | `grover` | Grover：振幅、Oracle、對平均反射、幾何圖、成功機率 |
| 10 | `shor` | Shor 週期尋找：模指數、量測、QFT、連分數、gcd（N = 15 / 21） |
| 11 | `qec` | 表面碼：錯誤、症狀、最小權重配對解碼、即時蒙地卡羅門檻曲線 |
| 12 | `workflow` | 完整流程：程式 → 轉譯 → 脈衝 → 控制電子 → shots → 結果；時間預算 |

### 重新產生

```bash
cd slides/build && python3 make_op_figures.py
```

```bash
cd slides/build && node shoot_operation.js
```

```bash
cd slides/build && node build_operation.js
```

`shoot_operation.js` 以 Playwright 擷取 3D 截圖；擷取後若場景版面有變，需重新計算 `op_crops.json`（各截圖的裁切範圍）。

---

## 技術分享（第四篇）：離子阱與中性原子量子電腦

用「真的原子」當量子位元的兩種平台：系統由哪些設備組成、量子位元怎麼實現、怎麼做閘、怎麼量測，以及與超導平台的差異。

### 內容

| 路徑 | 說明 |
|---|---|
| `slides/Ion_NeutralAtom_Talk.pptx` | 56 頁簡報：離子阱系統與操作（含運算與讀取總覽、超導對照、氫邁射頻率基準）、中性原子系統與操作（含運算與讀取總覽、頻率基準與原子鐘）、三平台比較（含供電切入分析）、總結；每頁有講者備註 |
| `speech/離子阱與中性原子演講稿.md` | 與講者備註同步的演講稿、時間規劃、60 分鐘精簡版、Q&A 準備 |
| `docs/離子阱與中性原子師生對話教學紀錄.md` | 師生對話形式的 6 課：運算與讀取（超導對照）、氫邁射、中性原子運算與讀取、頻率基準、MS 閘 vs 芮德堡 CZ；附三平台總對照與迷思整理 |
| `docs/離子阱與中性原子系統指南.md` | 兩個平台的子系統、連接清單、從開機到上線的步驟、日常監控與異常、設施與電力比較；運算與讀取問答（含超導對照）、頻率基準與氫邁射 |
| `animations/atoms.html` | 17 個 3D 場景（與其他動畫共用核心程式；Paul 阱軌跡、離子鏈正規模、MS 閘、芮德堡阻斷、多位元狀態向量、氫邁射起振等為即時數值計算） |
| `slides/figures/atoms/`、`slides/figures/3d_atoms/` | 簡報用物理圖表與 3D 場景截圖 |

### 簡報架構

1. **開場**：人造原子 vs 真的原子、DiVincenzo 五條件在兩個平台的實現
2. **離子阱：系統**：系統全景、Paul 阱與 Mathieu 穩定條件、真空與裝載、雷射與光學（¹⁷¹Yb⁺）、電子與控制
3. **離子阱：操作**：量子位元編碼、一個 shot 的流程、雷射冷卻、光泵浦與單位元閘、集體振動、Mølmer–Sørensen 閘、螢光讀取、QCCD、運算與讀取一次走完、超導 vs 離子阱對照、氫邁射與相位誤差估算、擴展路線
4. **中性原子：系統**：系統全景、磁光阱、光鑷（SLM / AOD）、裝載成像與重排、雷射與光學（⁸⁷Rb）
5. **中性原子：操作**：編碼、全域 + 局部單位元閘、芮德堡原子、芮德堡阻斷、CZ 閘、MS 閘 vs 芮德堡 CZ、分區架構、成像讀取、運算與讀取一次走完、頻率基準（微波鏈 + 雷射鏈）與原子鐘、原子損失與連續運轉、類比模擬
6. **三平台比較**：綜合比較表、時間尺度、連接性與並行、錯誤率與錯誤更正進展、系統與設施需求、供電切入分析、主要廠商
7. **總結**：重點回顧、3D 動畫導覽、參考資料、Q&A

### 3D 場景

| # | 代號 | 主題 |
|---|---|---|
| 1 | `ionsys` | 離子阱系統全景：雷射、光學、真空腔、成像、RF/DC/微波電子、設施；連接分類顯示 |
| 2 | `paul` | Paul 阱原理：旋轉鞍形位勢、Mathieu 軌跡（secular + micromotion）、q 參數與穩定性 |
| 3 | `ionqubit` | ¹⁷¹Yb⁺ 量子位元：能階、冷卻、光泵浦、微波閘、螢光偵測與光子數直方圖 |
| 4 | `modes` | 離子鏈集體振動：平衡位置與軸向 / 徑向正規模（數值求解） |
| 5 | `ms` | Mølmer–Sørensen 閘：自旋相依力、相空間迴圈、族群演化 |
| 6 | `qccd` | QCCD 搬運架構：分段電極、分區、接面、共冷、時間預算 |
| 7 | `ionflow` | 離子阱運算與讀取總覽：5 顆離子跑完冷卻 → 光泵浦 → 全域微波 / Raman 定址 → 任意配對 MS 閘 → 螢光讀取；5 位元狀態向量、500 shots 統計、與超導的時間尺度對照 |
| 8 | `hmaser` | 氫邁射：解離器、六極磁鐵選態、鐵氟龍儲存泡 + 銅腔起振（可關選態器 / 調流量）、鎖相 10 MHz → 12.6 GHz；Allan 偏差與 Ramsey 相位誤差 |
| 9 | `atomsys` | 中性原子系統全景：MOT、光鑷光路（SLM + AOD）、芮德堡雷射、相機與即時控制 |
| 10 | `tweezer` | 光鑷裝載與重排：隨機裝載、成像、AOD 搬運成無缺陷陣列 |
| 11 | `atomqubit` | ⁸⁷Rb 量子位元：能階、全域微波與局部定址 |
| 12 | `rydberg` | 芮德堡阻斷：距離與阻斷半徑、四能階數值演化、CZ 協定 |
| 13 | `zoned` | 分區架構：儲存 / 糾纏 / 讀取區、並行 CZ、中途量測 |
| 14 | `imaging` | 螢光成像讀取：推出 \|1⟩、相機影像、直方圖與閾值 |
| 15 | `atomflow` | 中性原子運算與讀取總覽：裝載重排 → 光泵浦 → 全域 / 定址閘 → AOD 搬運 → 芮德堡 CZ → 推出 + 成像；6 位元狀態向量、三平台時間尺度 |
| 16 | `atomclock` | 頻率基準：氫邁射 / 銣鐘 → 6.835 GHz、光頻梳、ULE 參考腔鎖芮德堡雷射、原子噴泉鐘；類氫結構表、雷射線寬 vs CZ 錯誤 |
| 17 | `compare` | 三平台比較：連接性、閘速度、相干時間、規模 |

### 重新產生

```bash
cd slides/build && python3 make_atom_figures.py
```

```bash
cd slides/build && node shoot_atoms.js
```

```bash
cd slides/build && node build_atoms.js
```

`shoot_atoms.js` 依 `atoms_plan_ion.json`、`atoms_plan_atom.json` 的操作計畫擷取 3D 截圖，並自動計算裁切範圍寫入 `atoms_crops.json`。

---

## 影片報告簡報：《量子超級英雄》影片轉 PPT

把 QuBear 量子熊 ✕ 龍騰文化《量子超級英雄》的影片逐字稿整理成可以上台報告的簡報。每張投影片右上角標出對應的影片時間，備忘稿是講稿。

| 路徑 | 說明 |
|---|---|
| `slides/output/ep049-superconducting-qubit.pptx` | #049 超導量子位元：用「JJ」做出二態系統（16 頁） |
| `slides/episodes/ep049.js` | #049 的內容檔（文字、圖表資料、講稿） |
| `slides/build_deck.js` | 影片簡報產生器（與 `slides/build/` 的技術分享產生器分開） |
| `slides/README.md` | 每集的製作流程與投影片類型說明 |

```bash
cd slides && npm install && node build_deck.js episodes/ep049.js
```
