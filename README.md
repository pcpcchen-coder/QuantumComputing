# QuantumComputing

量子計算學習筆記。

## 筆記目錄

> 所有簡報都另附 PDF 版：[`slides/pdf/`](slides/pdf/)（`JJ_Microwave_Readout_Talk.pdf`、`QC_Peripheral_Systems_Talk.pdf`、`QC_Operation_Talk.pdf`、`Ion_NeutralAtom_Talk.pdf`、`transmon.pdf`、`QC_Power_Supply_Delta.pdf`）。

1. [約瑟夫森結（JJ）：巨觀量子波、相位差與「穿隧」的真正意義](notes/josephson-junction-wave-and-tunneling.md)
2. [Transmon：約瑟夫森電感、電路結構與量子位元機制](notes/transmon-josephson-inductance.md)
   - 簡報：[`slides/transmon.pptx`](slides/transmon.pptx)（17 頁，PowerPoint）
   - 3D 互動動畫：[`animations/transmon-3d.html`](animations/transmon-3d.html)（7 章；第 6 章「案例」示範 SQUID 調頻、頻率配置與頻率碰撞、XY 寫入、CZ 閘；第 7 章「振幅長條」示範糾纏與兩位元 Grover 搜尋；下載後用瀏覽器開啟；需連網載入 three.js）
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
   - 簡報：[`slides/Ion_NeutralAtom_Talk.pptx`](slides/Ion_NeutralAtom_Talk.pptx)（49 頁，含講者備註）
   - 演講稿：[`speech/離子阱與中性原子演講稿.md`](speech/離子阱與中性原子演講稿.md)
   - 系統指南：[`docs/離子阱與中性原子系統指南.md`](docs/離子阱與中性原子系統指南.md)（子系統、連接清單、啟動校準流程、異常處置、設施與電力）
   - 3D 互動動畫：[`animations/atoms.html`](animations/atoms.html)（13 個場景，離線可用）
8. [影片報告簡報：《量子超級英雄》影片轉 PPT](#影片報告簡報量子超級英雄影片轉-ppt)
   - #049 超導量子位元：[`slides/output/ep049-superconducting-qubit.pptx`](slides/output/ep049-superconducting-qubit.pptx)（16 頁，含講稿）
   - 製作流程與產生器：[`slides/README.md`](slides/README.md)
9. [課程擴充規劃：量子電腦學院（參考父子科技學院格式，6 模組 × 16 堂）](docs/量子電腦學院_課程擴充規劃.md)（現有 223 頁簡報與 47 個 3D 場景的盤點、Q001–Q096 課表、新增動畫與簡報清單）
   - 學程資料夾：[`academy/`](academy/README.md)（96 堂課綱、每堂教案、製作指南、製作狀態）
10. [量子電腦供電設計：文獻回顧與台達電的切入點](docs/量子電腦供電設計文獻回顧與台達電切入點.md)（超導、離子阱、中性原子三平台分篇細部分析：精密電源、不斷電與分層備援、低干擾設計、能耗擴展，以及台達電的產品 × 平台矩陣）
    - 簡報：[`slides/output/qc-power-supply-delta.pptx`](slides/output/qc-power-supply-delta.pptx)（36 頁，含講稿）；PDF：[`slides/pdf/QC_Power_Supply_Delta.pdf`](slides/pdf/QC_Power_Supply_Delta.pdf)
    - 簡報內容檔：[`slides/reports/qc-power-delta.js`](slides/reports/qc-power-delta.js)（`cd slides && node build_deck.js reports/qc-power-delta.js` 重新產生）

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

> 從 PowerPoint 點按鈕開啟動畫時，請保持 `slides/` 與 `animations/` 的相對位置不變（連結為 `../animations/index.html#…`）。

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
| `slides/Ion_NeutralAtom_Talk.pptx` | 49 頁簡報：離子阱系統與操作、中性原子系統與操作、三平台比較（含供電切入分析）、總結；每頁有講者備註 |
| `speech/離子阱與中性原子演講稿.md` | 與講者備註同步的演講稿、時間規劃、60 分鐘精簡版、Q&A 準備 |
| `docs/離子阱與中性原子系統指南.md` | 兩個平台的子系統、連接清單、從開機到上線的步驟、日常監控與異常、設施與電力比較 |
| `animations/atoms.html` | 13 個 3D 場景（與其他動畫共用核心程式；Paul 阱軌跡、離子鏈正規模、MS 閘、芮德堡阻斷等為即時數值計算） |
| `slides/figures/atoms/`、`slides/figures/3d_atoms/` | 簡報用物理圖表與 3D 場景截圖 |

### 簡報架構

1. **開場**：人造原子 vs 真的原子、DiVincenzo 五條件在兩個平台的實現
2. **離子阱：系統**：系統全景、Paul 阱與 Mathieu 穩定條件、真空與裝載、雷射與光學（¹⁷¹Yb⁺）、電子與控制
3. **離子阱：操作**：量子位元編碼、一個 shot 的流程、雷射冷卻、光泵浦與單位元閘、集體振動、Mølmer–Sørensen 閘、螢光讀取、QCCD、擴展路線
4. **中性原子：系統**：系統全景、磁光阱、光鑷（SLM / AOD）、裝載成像與重排、雷射與光學（⁸⁷Rb）
5. **中性原子：操作**：編碼、全域 + 局部單位元閘、芮德堡原子、芮德堡阻斷、CZ 閘、分區架構、成像讀取、原子損失與連續運轉、類比模擬
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
| 7 | `atomsys` | 中性原子系統全景：MOT、光鑷光路（SLM + AOD）、芮德堡雷射、相機與即時控制 |
| 8 | `tweezer` | 光鑷裝載與重排：隨機裝載、成像、AOD 搬運成無缺陷陣列 |
| 9 | `atomqubit` | ⁸⁷Rb 量子位元：能階、全域微波與局部定址 |
| 10 | `rydberg` | 芮德堡阻斷：距離與阻斷半徑、四能階數值演化、CZ 協定 |
| 11 | `zoned` | 分區架構：儲存 / 糾纏 / 讀取區、並行 CZ、中途量測 |
| 12 | `imaging` | 螢光成像讀取：推出 \|1⟩、相機影像、直方圖與閾值 |
| 13 | `compare` | 三平台比較：連接性、閘速度、相干時間、規模 |

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
