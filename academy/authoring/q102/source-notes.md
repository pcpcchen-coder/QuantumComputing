# Q102 來源筆記（逐字引文）

查核日：2026-11-18。維基百科頁面由製作代理直接開啟（revision id 取自頁面的永久連結 oldid）。學程內部簡報、文件與動畫程式由製作代理讀取。程式由製作代理實際執行。

## Transmon（Wikipedia，oldid=1377984572）

- 非諧性定義：α = (E21 − E10)/E10。
- 「Reduced anharmonicity complicates the device operation as a two level system」

## Superconducting quantum computing（Wikipedia，oldid=1382042448）

- 「Qubit energy level separation is frequently adjusted by controlling a dedicated bias current line」
- 「An Xmon is essentially a tunable transmon.」
- 「Large anharmonicity is beneficial because it allows fast local microwave control and mitigates spectral crowding problems」
- 「Most decoherence is attributed to the quality of the Josephson junction and imperfections in the chip substrate.」

## SQUID（Wikipedia，oldid=1379580433）

- 「It has two Josephson junctions in parallel in a superconducting loop.」
- 「The periodicity is equal to one flux quantum, Φ0.」

## Graph coloring（Wikipedia，oldid=1386063130）

- 「a labeling of the graph's vertices with colors such that no two vertices sharing the same edge have the same color.」
- 「Vertex coloring models to a number of scheduling problems.」

## 超導量子電腦師生對話教學紀錄（docs/），第 3、4 課

- 第 4 課：「驅動選擇性：20 ns 的 π 脈衝頻寬約 50 MHz，鄰居落在頻寬內就被誤打；相鄰位元要錯開數十到上百 MHz。」
- 「耦合造成交換：耦合 g 約數–20 MHz；失諧接近 0 就互換激發」
- 「多能階：A 的 0→1 = 5.21、1→2 = 4.93、0→2 雙光子 = 5.07 GHz。任何一條撞上鄰居任何一條，就是碰撞。」
- 禁區表：① 同頻 ~5.21；② A₀₁ 撞 B₁₂ ~5.49；③ B₀₁ 撞 A₁₂ ~4.93；④ 雙光子 ~5.07／~5.35；⑤ 旁觀者。「禁區寬約 ±10–30 MHz。」
- 「棋盤格 H/L 避開了 ①～④，但中間的 H 有四個同頻的 L 鄰居 → 旁觀者碰撞。」「變成帶連續禁區的圖著色問題」
- 「TLS 缺陷會隨時間飄移，昨天的最佳配置今天可能撞上缺陷。」
- 第 3 課：「JJ 氧化層差幾個原子，頻率可偏約 100 MHz」「限制是只能往下調（最高在 Φ = 0），所以 E_J 要刻意做大一點；離 sweet spot 越遠 T₂ 越差。」

## 學程內部簡報

- slides/transmon.pptx 第 20 頁「案例：三顆可調 transmon 的頻率配置」：「③ 頻率配置　Q2 留在 sweet spot（5.10 GHz），避開同頻、0→1 撞 1→2（±283 MHz）、雙光子（±141 MHz）禁區。」「⑤ CZ 閘　把 Q3 推到 f_Q2 − α，|11⟩ 繞一圈多一個 −1 相位。」備註：「CZ 閘反而是刻意、短暫地拜訪碰撞點」。
- slides/QC_Operation_Talk.pptx 第 23 頁：「磁通脈衝把 A 的頻率往下拉，使 |11⟩ 靠近 |20⟩」「累積到 π 即為 CZ；約 40–70 ns」。

## 互動動畫程式（animations/transmon-3d.html 第 6 章 #case）

- `const QC = { EC: 0.25, alpha: -0.283, d: 0.013, EJmax: [14.49, 14.381, 15.978] };   // sweet spot 頻率 5.12 / 5.10 / 5.39 GHz（製程誤差）`
- `const WIN = { same: 0.03, x12: 0.025, tp: 0.012 };   // 碰撞判定窗（GHz，示意）`
- `const ALLOC = [phiFor(0, 4.90), 0, phiFor(2, 5.30)];`
- applyPi：「π 脈衝打 Q_k：其他位元看到洩漏的驅動（相鄰 60%、隔一顆 25%，示意），依失諧算激發機率」；Rabi 頻率 25 MHz（20 ns π 脈衝）。
- 步驟 ③ cue：「先試棋盤格：用 Z 線把 Q1、Q3 都調到 4.90 GHz。」「Q1、Q3 都避開了 Q2 的禁區，但 Q1 = Q3：兩者都是 Q2 的鄰居 → 旁觀者碰撞。」「零碰撞：三顆位元各有自己的地址，彼此相距約 200 MHz。」
- 步驟 ⑤ cue：「這正是平常要避開的禁區：做閘時才刻意去，而且只停留幾十 ns。」
- 自由實驗控制項：`c6phi0..2`（Q1–Q3 Φ 滑桿，0–0.3）、`data-pi` 按鈕「π → Q1／Q2／Q3」、`c6cz`、`c6alloc`「回到配置」、`c6raw`「回到製程原貌」、`c6zones`「顯示 Q2 鄰居的禁區」；碰撞清單 `c6col`，無碰撞顯示「無碰撞 ✓」（青色）。

## 實跑紀錄（collision_checker.py，Python 3.13.18，只用標準函式庫）

```
Q2 在 5.10 GHz 時，鄰居的禁區：4.817、4.958、5.100、5.241、5.383 GHz
剛做好（製程原貌）：5.12、5.10、5.39 → 碰撞 3 處：Q1 ≈ Q2（同頻，差 20 MHz）；Q2 0→1 ≈ Q3 1→2；旁觀者：Q1 0→1 ≈ Q3 1→2
棋盤格：4.90、5.10、4.90 → 碰撞 1 處：旁觀者：Q1 ≈ Q3（同頻，差 0 MHz）
動畫的配置：4.90、5.10、5.30 → 無碰撞 ✓
第二個空位：4.90、5.10、5.00 → 無碰撞 ✓
五顆（第一次嘗試）：4.90、5.10、5.30、5.00、4.80 → 碰撞 1 處：Q4 0→1 ≈ Q3 1→2
五顆（範例解）：4.90、5.10、5.30、4.90、5.10 → 無碰撞 ✓
```
