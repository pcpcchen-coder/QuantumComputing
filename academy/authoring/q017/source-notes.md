# Q017 來源筆記（逐字引文）

查核日：2026-11-18。課綱、簡報、動畫程式由製作代理讀取。程式由製作代理實際執行。

## 課綱（academy/lessons/Q017/lesson.json）

- 課程主題「為什麼要做「人造原子」」；階段「第二階段 硬體怎麼做」；模組「QM02 超導量子位元：從超導到 transmon」。
- 學習目標「知道量子位元需要可控制的二態系統，認識 DiVincenzo 五條件」。
- 動手任務「用五條件檢核一枚硬幣、一顆燈泡、一個原子和一顆 transmon」；孩子獨立改造「再找一個生活中的「二態系統」並檢核它缺哪一條」；好玩機制「冒險任務」。
- 作品「五條件檢核卡」；家長課前準備「列印五條件卡」；生活技能支線「用清單做系統性判斷」。
- 常見誤解與安全提醒「「有兩個狀態」還不夠，還要能初始化、操控、讀取並維持夠久」。
- 沿用簡報頁：ep049-superconducting-qubit.pptx p3–4、Ion_NeutralAtom_Talk.pptx p3–4；沿用 3D 場景：無（本集動畫段另選 index.html#potential、atoms.html#ionqubit、atoms.html#compare）。
- Q016 brief：「成果發表：我的量子小百科」「用自己的話解釋 10 個量子名詞」。Q018 brief：「超導：電阻消失、磁鐵懸浮」「知道超導的兩個特徵：零電阻與排斥磁場」。

## 簡報（python-pptx 擷取）

- ep049 p2：「LC 電路與超導」「JJ 讓能階不等距：把電感換成 JJ → 多出四次方項 → 二態系統出現」；備註「說明它為什麼能把『樓梯』變成可以只操作兩階的二態系統」。
- ep049 p4：「科學上需要的是 two-state system：只有兩個基底態、可以疊加，而且要能操控」；「薛丁格的貓：只是思想實驗／不可能真的把貓關進箱子當量子位元」；「原子：挑兩個能階，忽略其他能階／問題：單一電子、原子實在太小、太難操控」；「超導是巨觀的量子現象／可以用比較大、比較好操作的東西做量子位元／關鍵元件：JJ」。
- Ion_NeutralAtom_Talk p3：「超導 transmon（人造原子）：做出來的：鋁 + 約瑟夫森接面的電路／囚禁：不用囚禁，元件固定在晶片上／操控：微波脈衝（ns）／讀取：色散微波讀取（μs）／環境：10 mK 稀釋冷凍機」；「天然原子：每顆完全相同、相干時間長；代價是要用電場或雷射一顆顆抓住，並用大量雷射精準操控。」；備註「超導量子位元是「人造原子」：我們用鋁和約瑟夫森接面做出一個非線性的 LC 電路，它的能階看起來像原子。好處是可以用半導體製程大量製作、速度很快；壞處是每一顆都有製程差異，而且需要 10 mK 的低溫。」「與其說是電子設備，不如說是一張非常精密的光學桌」。
- Ion_NeutralAtom_Talk p4 表格：「① 可擴展、定義清楚的二能階系統」「② 可以初始化到 |0⟩：雷射冷卻 + 光泵浦（> 99.9 %，μs）」「③ 相干時間遠長於閘時間：T₂ 秒～小時（離子）；T₂ ~1 s（中性原子）」「④ 通用量子閘」「⑤ 可以量測單一量子位元：狀態相依螢光」；備註「2000 年 David DiVincenzo 提出一台量子電腦需要滿足的五個條件」。

## 維基百科（DiVincenzo's criteria，原始 wikitext）

- 「conditions proposed in 1996 by the theoretical physicist David P. DiVincenzo」。
- 前五條：「A scalable physical system with well-characterized qubit」「The ability to initialize the state of the qubits to a simple fiducial state」「Long relevant quantum coherence times」「A "universal" set of quantum gates」「A qubit-specific measurement capability」；另兩條關於量子通訊。
- 「One can demonstrate that DiVincenzo's criteria are satisfied by a classical computer.」

## 其他文件

- docs/超導量子電腦師生對話教學紀錄.md 第 6 課：「稀釋冷凍機整個實驗期間都維持在約 10 mK」「每讀完一次，只需要讓「這顆位元」回到 |0⟩，最快幾 μs。」

## 互動動畫程式

- js/scenes/04_potential.js：desc「LC 諧振子的位勢是拋物線，能階等間距（ħω）。用頻率 ω 的微波驅動時，0→1、1→2、2→3… 全部同時共振，無法只操作兩個能階。」「把電感換成 JJ，位勢變成 −E_J cos φ，越往上越「寬」，能階間距逐漸縮小 → 非諧性 α = ω₁₂ − ω₀₁ ≈ −E_C。如此就能只選擇 |0⟩ 與 |1⟩ 當作量子位元。」（第 6–7 行）；`EC = 0.25`、`ratio = 50, mode = 'transmon'`（第 12–13 行）；按鈕「LC 諧振子（線性）」「JJ / Transmon（非線性）」（第 114 行）；讀數「非諧性 α/2π = … MHz（等間距 → 無法單獨定址）」（第 111 行）。
- js/atoms/03_ionqubit.js：按鈕「① Doppler 冷卻」「② 光泵浦初始化 |0⟩」「③ 微波 π/2」「④ 微波 π」「⑤ 偵測（螢光）」「一次跑 1000 shots」「重置」（第 119–127 行）；desc「⑤ 偵測：369 nm 只和 |1⟩ …… 共振……→ 亮；|0⟩ …… → 暗」（第 10 行）。
- js/atoms/13_compare.js：desc「超導：人造原子（電路），閘最快（約 20–100 ns）……相干時間短（約 0.1 ms）」（第 6 行）；按鈕「連接性」「閘速度」「相干時間」「規模」（第 75 行）；DATA.coh 標籤「T₂ ~0.1 ms / 50 ns ≈ 2×10³」「T₂ ~1 s（可更長）/ 100 μs ≈ 10⁴ 以上」「T₂ ~1 s / 0.3 μs ≈ 3×10⁶ 計入搬運約 10³–10⁴」（第 70 行）。

## 實跑紀錄（ladder_check.py，Python 3，無套件）

```
LC 電路（線性）    相鄰兩階的間距（GHz）： [5.0, 5.0, 5.0]
約瑟夫森接面（非線性）相鄰兩階的間距（GHz）： [4.735, 4.448, 4.127]
非諧性 = (1→2 間距) − (0→1 間距) = -287 MHz；LC 電路是 0 MHz
結論：LC 電路每一階一樣高，微波會一路往上推；換成約瑟夫森接面，0→1 和 1→2 的頻率不同，微波就能只推 0 和 1。
```

與 numpy `eigvalsh`（同一哈密頓量，N = 14）結果相同：4.7355、4.4482、4.1272 GHz，非諧性 −287.3 MHz。
