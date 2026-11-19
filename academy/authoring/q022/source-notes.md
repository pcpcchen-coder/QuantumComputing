# Q022 來源筆記（逐字引文）

查核日：2026-11-18。課綱、簡報、動畫程式由製作代理讀取。程式由製作代理實際執行。

## 課綱（academy/lessons/Q022/lesson.json）

- 課程主題「量子諧振子：等距的梯子」；階段「第二階段 硬體怎麼做」；模組「QM02 超導量子位元：從超導到 transmon」；難度 3。
- 學習目標「知道 LC 電路的能階等距，所以無法只挑出兩個能階當量子位元」。
- 動手任務「在場景切到 LC 模式，數能階間距；用梯子圖說明「一路往上爬」的問題」；孩子獨立改造「畫出不等距梯子，說明為什麼能只在 0 與 1 之間跳」；好玩機制「闖關」。
- 作品「能階梯子圖」；家長課前準備「index.html#potential」；生活技能支線「找出設計失敗的根本原因」。
- 常見誤解與安全提醒「「等距」才是問題所在，不是能量太高或太低」。
- 沿用簡報頁：ep049-superconducting-qubit.pptx p7、p10、transmon.pptx p14；沿用 3D 場景：i:potential、lj:s3。
- Q021 brief：「把力學振盪和電磁振盪對應起來：質量↔電感、彈簧↔電容」。Q023 brief：「約瑟夫森接面：超導三明治」「認識 SIS 結構、Cooper pair 穿隧與 DC／AC Josephson 效應」。

## 簡報（python-pptx 擷取）

- ep049 p7「量子諧振子：出現等距的能階」：「En = (n + ½) ħω」「能階 n = 0, 1, 2, …」「ΔE = ħω」「相鄰能階的間距固定：像樓梯一樣「等距」」
  「零點能：最低能量 ½ħω 不是零；位置和動量不能同時確定，所以不能「完全靜止」」「等距能階：每一階的能量差都一樣；原子的能階通常不等距」
  「實際上很難做：要縮到夠小才有量子效應，還要極低溫避開熱擾動」。備註「第二是今天的重點：能階是等距的，像樓梯一樣。」
- ep049 p10「問題來了：二態系統在哪裡？」：「超導 LC 電路」「等距能階（示意）」「同一個微波頻率都吸收」「超導 LC 電路給了我們一座樓梯，但不是兩個態」
  「控制方法：打進微波（電磁波）來激發系統」「能階等距 → 每一階的間隔一樣，同一個微波能把系統一路往上推」「所有態都會被影響，沒辦法只在 |0⟩ 和 |1⟩ 之間操作」
  「→ 必須想辦法讓能階不等距」。備註「因為每一階的間隔都一樣，同一個微波可以讓它一路往上跳，所有的態都會被影響，就不是二態系統了。」
- transmon p14「非諧性：能階不再等距」：「線性 LC 諧振子」三個「5.48 GHz」；「Transmon」「5.21 GHz」「4.93 GHz」「4.62 GHz」；
  「LC：每階間距相同 / 一個頻率會一路往上激發，挑不出兩個能階 / Transmon：越上越密 / E12 比 E01 低 283 MHz。用 5.21 GHz 微波（青色箭頭）驅動，只會在 |0⟩、|1⟩ 之間來回。」
  備註「非諧性 α = E12 − E01 = −283 MHz，遠大於控制脈衝的頻寬（約數十 MHz），所以可以只操作最低兩個能階。」「2D 圖解：能階間距 …lc-vs-jj.html#s3」「2D 圖解：只停在 |0⟩|1⟩ …lc-vs-jj.html#s4」。

## 維基百科（原始 wikitext，2026-11-18 取得）

- Quantum harmonic oscillator：「First, the energies are quantized, meaning that only discrete energy values (integer-plus-half multiples of ħω) are possible」
  「Second, these discrete energy levels are equally spaced, unlike in the Bohr model of the atom, or the particle in a box.」
  「Third, the lowest achievable energy (the energy of the n = 0 state, called the ground state) is not equal to the minimum of the potential well, but ħω/2 above it; this is called zero-point energy.」
  「If we ignore the zero-point energy then the levels are evenly spaced at 0, ħω, 2ħω, 3ħω, ⋯」。
- LC circuit：「ω₀ = 1/√(LC)」。
- Transmon：「The disadvantage is the reduced anharmonicity α = (E21 − E10)/E10」「Reduced anharmonicity complicates the device operation as a two level system, e.g. exciting the device from the ground state to the first excited state by a resonant pulse also populates the higher excited state.」
- Superconducting quantum computing：「In this context, anharmonicity refers to the unequal spacing of energy levels in a superconducting circuit. Large anharmonicity is beneficial because it allows fast local microwave control and mitigates spectral crowding problems」。

## 動畫程式

- `animations/js/scenes/04_potential.js`（index.html 第 43 行載入）：第 3–8 行 id 'potential'、標題「非線性：從 LC 諧振子到 Transmon」，說明「LC 諧振子的位勢是拋物線，能階等間距（ħω）。用頻率 ω 的微波驅動時，0→1、1→2、2→3… 全部同時共振，無法只操作兩個能階。」
  「把電感換成 JJ，位勢變成 −E_J cos φ，越往上越「寬」，能階間距逐漸縮小 → 非諧性 α = ω₁₂ − ω₀₁ ≈ −E_C。如此就能只選擇 |0⟩ 與 |1⟩ 當作量子位元。」
  第 12–13 行 E_C = 0.25、ratio = 50、mode = 'transmon'；第 52–55 行 LC：E_n = √(8E_JE_C)(n + ½)；第 102 行金色標籤「ω{k}{k+1}/2π = … GHz」；第 109–112 行讀數，LC 時「（等間距 → 無法單獨定址）」；
  第 114–116 行按鈕「LC 諧振子（線性）」「JJ / Transmon（非線性）」、滑桿「E_J / E_C（對數刻度）」、「CPB：E_J/E_C = 1」「10」「Transmon：50」。
- `animations/lc-vs-jj.html`：第 214–243 行 #s3「第 3 步 · 位能與量子能階」「拋物線的能階等間距，餘弦的不是」「LC：U = Φ²/2L，是拋物線。量子化後能階完全等間距：E_n = ħω(n + ½)」
  「愈往上，餘弦位能井比拋物線更寬、更扁，能階就愈擠，間距一階比一階小」「這裡固定 E_C/h = 250 MHz，你可以調 E_J/E_C」；滑桿 #ratio 10–120、預設 50；讀數「LC：每一階間距」「Transmon：ω₀₁ / ω₁₂」「非諧性 α = ω₁₂ − ω₀₁」。
  第 246–260 行 #s4「第 4 步 · 用微波去驅動」「能不能只停在 |0⟩ 和 |1⟩？」「LC 的所有躍遷疊在同一個頻率上，驅動會讓它一路往上爬（變成同調態），沒辦法只用兩個能階。Transmon 的躍遷彼此錯開 |α|，驅動只打得到 0→1」；
  draw4 第 516–517 行圖上文字「0→1 = 1→2 = 2→3 = 3→4 全部重疊」「驅動一路往上爬」。

## 實跑紀錄

- ladder_table.py（Python 3，無套件）：LC 1 nH、1 pF → 每階 5.033 GHz；4 nH → 2.516；0.25 nH → 10.066，間距差都是 0；
  transmon E_J/E_C = 50 → 4.735、4.448、4.127、3.705 GHz，非諧性 −287 MHz；80 → 6.063、5.786、5.484、5.149，−277 MHz。
- 動畫讀數以頁面同一段程式在 Node 實算：index.html#potential LC 模式 ratio 50 → 5.000 GHz、α「0」；ratio 10 → 2.236 GHz、顯示三階、α「0」；ratio 1 → α 顯示「−0」（旁白不用）。
  lc-vs-jj.html #s3 ratio 50 → 左 5.00 ×4、右 4.74、4.45、4.13、3.70、3.50、r3c「−287 MHz」；ratio 80 → 左 6.32 ×4、右 6.06、5.79、5.48、5.15、4.78、「−277 MHz」；#s4 ratio 50 → LC 5.00 一條，transmon 4.74（打到）、4.45、4.13、3.70。
