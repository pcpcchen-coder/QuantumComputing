# Q103 來源筆記（逐字引文）

查核日：2026-11-18。維基百科頁面由製作代理直接開啟（revision id 取自頁面的永久連結）。學程內部文件、簡報與動畫程式由製作代理讀取。程式由製作代理實際執行。

## Rabi cycle（Wikipedia，oldid=1383859287）

- 「the cyclic behaviour of a two-level quantum system in the presence of an oscillatory driving field」
- 「it will cyclically absorb photons and emit them by stimulated emission」
- 「This is called a π pulse.」
- 「will not reach 1 unless Δω=0」（失諧時被激發的機率到不了 1）

## Transmon（Wikipedia，oldid=1377984572）

- 「a transmon is a type of superconducting charge qubit designed to have reduced sensitivity to charge noise」
- 「shunting the Josephson junction with an additional large capacitor」
- 「Reduced anharmonicity complicates the device operation as a two level system.」

## Quantum harmonic oscillator（Wikipedia，oldid=1380557618）

- 「Second, these discrete energy levels are equally spaced, unlike in the Bohr model of the atom, or the particle in a box.」

## Resonance（Wikipedia，oldid=1380373393）

- 「Resonance is a phenomenon that occurs when an object or system is subjected to an external force or vibration」（外力頻率要對上系統的共振頻率）
- 「Pushing a person in a swing in time with the natural interval of the swing (its resonant frequency)」（照節奏推才盪到最高；時機不對的推只得到較小的擺幅）

## 學程內部文件：docs/超導量子電腦師生對話教學紀錄.md 第 5 課

- 「把 JJ 換成普通電感，電路就是線性 LC 諧振器：位能變回拋物線，能階完全等距（每階都是 5.48 GHz）。對準 0→1 的微波對每一階都共振，狀態被一路往上推」
- 四個後果：「定義不出 0/1」「寫入不了」「讀不出來：色散偏移 χ = (g²/Δ)·α/(Δ+α)，α = 0 時 χ = 0」「做不了 CZ」
- 表：「π 脈衝（20 ns）｜有 JJ P(|1⟩) = 0.994，漏到 |2⟩ 只有 0.4%｜沒有 JJ 只有約 21% 在 |1⟩」「持續驅動 40 ns｜轉一整圈回到 |0⟩｜越爬越高，平均停在第 9.5 階」
- 「每一階不是某個位置或介面，而是『整個電路一起振盪』時能量的量子化等級——電路裡存了幾份微波能量（幾個光子）」
- 「JJ 那層 1–2 nm 氧化層本身不是『一階』，它只是讓電感變非線性」
- 「吸收能量的不是某一個能階，而是兩個能階之間的躍遷；『只能』其實是『幾乎只能』」
- 表：「|0⟩→|1⟩ 5.21 GHz 共振 ✓｜|1⟩→|2⟩ 4.93 GHz 差 283 MHz｜|2⟩→|3⟩ 4.62 GHz 差更多」
- 「共振是雙向的：在 |1⟩ 時被同一道微波推一下，會放出光子回到 |0⟩（受激輻射）」
- 「不共振躍遷最多被激發約 Ω²/(Ω²+Δ²)；Ω = 25 MHz、Δ = 283 MHz → 約 0.8%，模擬值 0.4%」「脈衝越短越強，頻譜越寬，越容易碰到 4.93 GHz」
- 「疊加態是『狀態』」「Rabi 振盪是『過程』」；表：π/2 →「(|0⟩ − i|1⟩)/√2」、3π/2 →「(|0⟩ + i|1⟩)/√2」、2π →「回到 |0⟩（差整體相位）」
- 「『來回振盪』不是在 0、1 之間跳來跳去：任一瞬間都是 cos(Ωt/2)|0⟩ − i·sin(Ωt/2)|1⟩」「微波一停，疊加態就留下來：π/2 脈衝就是在半路停下」

## 學程簡報：slides/transmon.pptx

- 第 14 頁「非諧性：能階不再等距」：LC 每階「5.48 GHz」；Transmon「5.21 GHz」「4.93 GHz」「4.62 GHz」；「E12 比 E01 低 283 MHz。用 5.21 GHz 微波（青色箭頭）驅動，只會在 |0⟩、|1⟩ 之間來回。」
- 第 16 頁「XY 旋轉 20–50 ns」「XY 線送入 f01 微波脈衝產生 Rabi 振盪；DRAG 整形避免漏到 |2⟩」
- 第 19 頁「以 f₀₁ = 5.21 GHz 微波驅動，狀態在布洛赫球上繞 X 或 Y 軸旋轉；|1⟩→|2⟩ 低 283 MHz，不會被同一道微波推上去。」
- 第 20 頁「④ XY 寫入　頻率錯開，對準 f₀₁ 的脈衝才不會串擾到鄰居。」（承接上一堂的頻率配置）

## 互動動畫程式：animations/transmon-3d.html

- 參數：`transmonLevels(15, 0.25, 0, 14)`（E_J/h = 15 GHz、E_C/h = 250 MHz，電荷基底數值對角化）；`const NL = 14, RABI = 0.025;   // 0↔1 Rabi 頻率 25 MHz：π 脈衝 20 ns`；LC 間距 `Math.sqrt(8 * 15 * 0.25)`（5.48 GHz）。
- 第 3 章 `#potential`：按鈕 `c3tr`「有 JJ（transmon）」、`c3lc`「沒有 JJ（線性 LC）」、`c3pi`「送 π 脈衝（20 ns）」、`c3long`「持續驅動 40 ns」、`c3r`「重設 |0⟩」；面板 `r3p` 顯示「此刻的狀態」「P(|0⟩)・P(|1⟩)・P(|2⟩)」「P(≥|3⟩)」「平均能階 ⟨n⟩」；驅動模擬「1 秒動畫 = 8 ns」；青色長條是各能階的佔據機率（第 5 條以上合併在最上面一條）。
- 第 4 章 `#control`：`c4mtr`／`c4mlc` 切換、`c4rabi`「持續驅動（Rabi 振盪）」（有 JJ 時箭頭以每秒 π/1.1 弧度連續繞 X 軸；沒有 JJ 時以「1 秒動畫 = 16 ns」跑多能階模擬，40 ns 後自動停下並顯示說明）；「類型」欄：「純 |0⟩（量測必得 0）」「純 |1⟩（量測必得 1）」「疊加態（量測：0 有 …%、1 有 …%）」「已漏出 0/1：不是量子位元的狀態」（紅字）；能階梯標籤「5.21 GHz 共振」「4.93 GHz 不共振」，沒有 JJ 時「5.48 GHz 也共振！」（紅字）。
- animations/lc-vs-jj.html `#s4`「能不能只停在 |0⟩ 和 |1⟩？」：「LC 的所有躍遷疊在同一個頻率上，驅動會讓它一路往上爬（變成同調態）」。

## 實跑紀錄

`rabi_ladder.py`（Python 3.13、numpy 2.5.3）與從 transmon-3d.html 擷取的模擬函式（Node 22）結果一致：

```
== 有 JJ（transmon） ==
相鄰兩階的間距（GHz）： 5.21、4.93、4.62、4.25
 時間   P(0)   P(1)   P(2)  P(≥3)  平均第幾階
  0 ns  1.000  0.000  0.000  0.000   0.00
 10 ns  0.502  0.496  0.002  0.000   0.50
 20 ns  0.002  0.994  0.004  0.000   1.00
 30 ns  0.499  0.499  0.002  0.000   0.50
 40 ns  1.000  0.000  0.000  0.000   0.00

== 沒有 JJ（線性 LC） ==
相鄰兩階的間距（GHz）： 5.48、5.48、5.48、5.48
 時間   P(0)   P(1)   P(2)  P(≥3)  平均第幾階
  0 ns  1.000  0.000  0.000  0.000   0.00
 10 ns  0.540  0.333  0.103  0.025   0.62
 20 ns  0.085  0.209  0.258  0.448   2.47
 30 ns  0.004  0.022  0.060  0.915   5.55
 40 ns  0.000  0.001  0.003  0.997   9.52
```
動畫面板實測（Playwright 截圖，2026-11-18）：第 3 章有 JJ π 脈衝後「0.002・0.994・0.004」、平均能階 1.00；沒有 JJ 持續驅動 40 ns 後「0.000・0.001・0.003」、P(≥|3⟩) 0.997、平均能階 9.52；第 4 章沒有 JJ 持續驅動後「已漏出 0/1：不是量子位元的狀態」。
