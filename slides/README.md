# 影片 → 報告用 PPT 範本

把《量子超級英雄》（QuBear 量子熊 ✕ 龍騰文化）這類科普影片整理成可以直接上台報告的 PowerPoint。

- **引擎**：`build_deck.js`，負責主題、版面和各種投影片類型，每集共用
- **內容**：`episodes/epXXX.js`，每集一個檔，只寫內容
- **成品**：`output/*.pptx`

第一個樣本：`episodes/ep049.js` → `output/ep049-superconducting-qubit.pptx`（16 張，含講稿）

《量子金魚》008 Deutsch 演算法：`episodes/qfish008.js` → `output/qfish008-deutsch-algorithm.pptx`（30 張，含講稿；PDF：`pdf/QFISH008_Deutsch_Algorithm.pdf`）。依影片逐字稿整理，並加上「案例實算（補充）」：振幅逐步計算、四種黑盒子、現場猜謎，每頁都有紫色按鈕直接開啟對應的 3D 動畫（`animations/transmon-3d.html#deutsch`、`#deutsch-lab`、`animations/operation.html#interference`）。3D 截圖以 `node capture_3d_deutsch.js` 重新擷取到 `figures/3d_deutsch/`。

引擎也可以用在非影片的報告：`reports/qc-power.js` → `output/qc-power-supply.pptx`（量子電腦供電設計，超導／離子阱／中性原子三平台，77 張，含講稿）。這類內容不需要 `time` 欄位。

《十個基礎量子電路》：`reports/basic-circuits.js` → `output/basic-circuits.pptx`（48 張，含講稿；PDF：`pdf/Basic_Quantum_Circuits.pdf`）。開頭「理論基礎」6 堂課（右上角「▶ 互動」連到 `animations/quantum-basics.html` 各課），接著疊加、干涉、Bell、GHZ、隱形傳態、Deutsch、BV、Grover、QFT、Shor 各有電路圖、振幅逐步長條或表格，右上角「▶ 動畫」按鈕開到 `animations/basic-circuits.html` 的對應範例；振幅數值都和動畫頁的模擬器一致。截圖以 `node capture_basic_circuits.js` 重新擷取到 `figures/basic_circuits/`。

## 每集的製作流程

1. **取得逐字稿**：用電腦打開 YouTube 影片，展開說明欄，點「顯示轉錄稿」，全選複製（保留時間戳記）。
   - 雲端環境會被 YouTube 擋下，無法自動抓字幕，所以由人工複製貼上。
   - 影片中重要的圖表可以另外截圖補充。
2. **寫內容檔**：複製 `episodes/ep049.js` 改成 `episodes/epXXX.js`，依影片順序填入每張投影片。
3. **產生簡報**：
   ```bash
   cd slides
   npm install        # 第一次才需要
   node build_deck.js episodes/epXXX.js
   ```
4. **檢查**：用 PowerPoint 打開 `output/` 裡的檔案，確認沒有文字溢出。

## 內容規則（讓每集風格一致）

- **只寫影片講到的內容**，不自行補充影片沒提的知識；必要的說明加上「示意」字樣。
- 每張投影片放 `time`（對應影片時間，例如 `"5:15–7:46"`），右上角會顯示成標籤，方便回頭對照影片。
- 每張投影片放 `notes`：口語化的講稿，放在 PowerPoint 的備忘稿。
- 結構建議：封面 → 本集脈絡（agenda）→ 依影片段落的內容頁 → 重點整理 → 討論與延伸。
- 標題 20 字以內；每頁一個重點。

## 文字標記

所有文字欄位都支援：

| 寫法 | 效果 |
|---|---|
| `**重點**` | 粗體＋強調色 |
| `E_{J}` | 下標 |
| `2^{N}` | 上標 |

## 投影片類型

| type | 用途 | 主要欄位 |
|---|---|---|
| `title` | 封面（深色） | `kicker`、`title`、`subtitle`、`meta[]` |
| `agenda` | 本集脈絡（3×N 卡片） | `items[{head, body, time}]` |
| `cards` | 2–4 張圖示卡片 | `lead`、`cards[{icon, tone, badge, head, body}]`、`callout` |
| `equations` | 左方程式、右說明 | `eqs[{eq, label}]`、`bullets[]`、`callout` |
| `chart` | 左原生圖表、右說明 | `chart{kind: "bar"/"line", labels, series[{name, values, color}], title, xTitle, yTitle}`、`bullets[]`、`caption` |
| `expansion` | 方程式橫條＋圖表＋各項說明 | `eq`、`chart`、`terms[{term, tone, head, body}]` |
| `ladder` | 能階圖（1–2 組） | `ladders[{name, sub, levels[], highlight[], arrows[{from, to, tone, label}]}]`、`bullets[]` |
| `table` | 對照表 | `headers[]`、`rows[][]`、`colW[]`、`callout` |
| `junction` | 約瑟夫森接面結構圖 | `arrowLabel`、`middle`、`symbol`、`bullets[]` |
| `summary` | 重點整理（深色） | `points[]` |
| `flow` | 流程／供電鏈（橫向方塊＋箭頭） | `steps[{head, body, tone}]`、`boxHeight`、`lead`、`bullets[]`、`callout` |
| `closing` | 討論題＋延伸觀看（深色） | `question`、`prompts[]`、`refs[]`；可選 `questionKicker`、`refsHead` 改兩個小標 |
| `circuit` | 量子線路圖（原生圖形）＋各階段狀態卡 | `circuit{wires[], cols[{g:[閘,…]} / {cx:[控制, 目標]} / {cz:[a, b]} / {cp:[a, b], label} / {swap:[a, b]} / {blk, tone, span:[第一條, 最後一條]} / {m:[true,false]}], marks[{after, label}]}`、`circuitHeight`、`stages[{head, eq, body, tone}]`、`callout` |
| `amps` | 振幅長條（金＝正、紅＝負，與 3D 動畫第 7 章同畫法） | `lead`、`panels[{head, amps[], note, tone, focus}]`、`labels[]`（長條數與 amps 相同；超過 4 根時數值縮小、0 不標）、`callout` |
| `scene3d` | 3D 動畫截圖＋說明＋「開啟 3D 動畫」超連結按鈕 | `image`（1–2 張）、`imageLabels[]`、`caption`、`bullets[]`、`link{label, url, prefix}`（`prefix` 改按鈕前綴）；`layout: "wide"` 讓兩張截圖橫排在上 |

共通欄位：`section`（PowerPoint 章節）、`time`、`notes`；`scene{label, url, prefix}` 會在右上角加一顆可點的「▶ 3D」小按鈕（`prefix` 可改按鈕前綴，例如「動畫」）。

> 3D 連結用 GitHub Pages 網址（例如 `https://pcpcchen-coder.github.io/QuantumComputing/animations/transmon-3d.html#deutsch`），簡報不必和 `animations/` 放在一起也能點開。已產生的 .pptx 可用 `python3 build/use_pages_links.py` 把舊的相對路徑改成網址。

`tone` 可用：`good`（綠 ✓）、`bad`（紅 ✗）、`warn`（琥珀）、`neutral`（青綠）、`quantum`（紫）。

`icon` 使用 [react-icons](https://react-icons.github.io/react-icons/)，格式為 `"套件:名稱"`，例如 `"md:MdBolt"`、`"fa:FaAtom"`。

如果某集需要新的圖（例如 SQUID 迴路），在 `build_deck.js` 加一個新的 `R.xxx` 類型即可，其他集不受影響。

## 主題

超導／低溫配色：深海軍藍（標題與深色頁）、冰藍（卡片底）、青綠（強調）、琥珀（能量、微波）。
字型為微軟正黑體，方程式用 Cambria。顏色定義在 `build_deck.js` 的 `THEME`，改一處就會套用到全部投影片。
