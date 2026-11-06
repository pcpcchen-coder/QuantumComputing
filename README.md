# QuantumComputing

量子計算學習筆記。

## 筆記目錄

> 所有簡報都另附 PDF 版：[`slides/pdf/`](slides/pdf/)（`JJ_Microwave_Readout_Talk.pdf`、`QC_Peripheral_Systems_Talk.pdf`、`transmon.pdf`）。

1. [約瑟夫森結（JJ）：巨觀量子波、相位差與「穿隧」的真正意義](notes/josephson-junction-wave-and-tunneling.md)
2. [Transmon：約瑟夫森電感、電路結構與量子位元機制](notes/transmon-josephson-inductance.md)
   - 簡報：[`slides/transmon.pptx`](slides/transmon.pptx)（17 頁，PowerPoint）
   - 3D 互動動畫：[`animations/transmon-3d.html`](animations/transmon-3d.html)（下載後用瀏覽器開啟；需連網載入 three.js）
3. [技術分享：超導量子電腦的 JJ 元件與微波讀取](#技術分享超導量子電腦的-jj-元件與微波讀取)
   - 簡報：[`slides/JJ_Microwave_Readout_Talk.pptx`](slides/JJ_Microwave_Readout_Talk.pptx)（43 頁，含講者備註）
   - 演講稿：[`speech/演講稿.md`](speech/演講稿.md)
   - 3D 互動動畫：[`animations/index.html`](animations/index.html)（11 個場景，離線可用）
4. [技術分享（續篇）：量子電腦的周邊系統與整合](#技術分享續篇量子電腦的周邊系統與整合)
   - 簡報：[`slides/QC_Peripheral_Systems_Talk.pptx`](slides/QC_Peripheral_Systems_Talk.pptx)（42 頁，含講者備註）
   - 演講稿：[`speech/周邊系統演講稿.md`](speech/周邊系統演講稿.md)
   - 建置文件：[`docs/周邊系統連接與啟動指南.md`](docs/周邊系統連接與啟動指南.md)（連接清單、啟動流程、異常處置）
   - 3D 互動動畫：[`animations/peripherals.html`](animations/peripherals.html)（10 個場景，離線可用）

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
