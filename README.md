# 超導量子電腦：JJ 元件與微波讀取 — 技術分享素材

給同仁的內部技術分享：約瑟夫森接面（Josephson Junction, JJ）的相關知識，以及如何用微波讀取量子位元狀態。內容包含簡報、完整演講稿與互動 3D 動畫。

## 內容

| 路徑 | 說明 |
|---|---|
| `slides/JJ_Microwave_Readout_Talk.pptx` | 主簡報，43 頁，每頁都有詳細講者備註；右上角「▶ 3D 場景」按鈕可直接開啟對應動畫 |
| `speech/演講稿.md` | 完整演講稿（與講者備註同步）、時間規劃、60 分鐘精簡版建議、Q&A 準備、公式速查 |
| `animations/index.html` | 互動 3D 動畫（three.js，已內附函式庫，**離線可用**），共 11 個場景 |
| `slides/figures/` | 簡報用物理圖表（matplotlib）與 3D 場景截圖 |
| `slides/build/` | 產生簡報與圖表的腳本 |

## 簡報架構

1. **背景知識**：量子位元與 Bloch 球、品質指標（T1/T2）、超導與 Cooper pair、BCS 能隙、磁通量子化、為什麼需要非線性
2. **JJ 元件**：SIS 結構、DC/AC Josephson 關係、非線性電感、E_J 與 E_C、RCSJ 洗衣板、SQUID、量子位元家族、transmon 與電荷色散、Dolan bridge 製程、頻率定位、JJ 的其他角色（耦合器、JPA、TWPA…）、退相干來源
3. **微波讀取**：讀取需求、電路 QED、色散位移 χ、S21 振幅/相位、外差解調與 IQ、單發判別與保真度、稀釋冷凍機讀取鏈、輸入線衰減與熱光子、量子極限放大器、κ/χ/Purcell 設計權衡、多工與進階技術、數值範例
4. **整合與總結**：全流程、重點回顧、3D 動畫導覽、參考文獻、Q&A

## 3D 動畫

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

## 重新產生簡報與圖表

```bash
cd slides/build && npm install && pip install matplotlib numpy
```

```bash
python3 slides/build/make_figures.py
```

```bash
cd slides/build && node build_deck.js
```

`build_deck.js` 同時輸出 `slides/JJ_Microwave_Readout_Talk.pptx` 與 `speech/演講稿.md`，修改講者備註只需改一處。3D 截圖（`slides/figures/3d/`）是以 Playwright 對 `animations/index.html?noui=1&clean=1#場景` 擷取。

## 字型

簡報使用「微軟正黑體（Microsoft JhengHei）」，方程式使用 Cambria，Windows / Office 皆內建。
