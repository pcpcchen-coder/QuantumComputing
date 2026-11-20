# Q070 來源筆記（逐字引文）

擷取日：2026-11-19。維基百科以 `index.php?title=…&action=raw` 取得當日版本（存於 `/home/user/qwork/q070wiki/`，未記 oldid）。

## Mølmer–Sørensen gate（Wikipedia）

- 「In quantum computing, Mølmer–Sørensen gate scheme (or MS gate) refers to an implementation procedure for various multi-qubit quantum logic gates used mostly in trapped ion quantum computing. This procedure is based on the original proposition by Klaus Mølmer and Anders Sørensen in 1999–2000.」
- 「In 1999, Mølmer and Sørensen proposed a native multi-qubit trapped ion gate as an alternative to Cirac and Zoller's scheme, insensitive to the vibrational state of the system and robust against changes in the vibrational number during gate operation.」
- 「In both regimes, a red and blue sideband interaction are applied simultaneously to each ion, with the red and blue tones symmetrically detuned by δ′ from the sidebands. This results in laser detunings ±(ω_k + δ′), where ω_k is the motional mode frequency.」
- 「When the gate is performed on a single pair of ions, it reduces to the R_XX gate. Thus, the CNOT gate can be decomposed into an MS gate and combination of single particle rotations.」
- 「The Mølmer–Sørensen gate implementation has the advantage that it does not fail if the ions were not cooled completely to the ground state, and it does not require the ions to be individually addressed. However, this thermal insensitivity is only valid in the Lamb–Dicke regime, so most implementations first cool the ions to the motional ground state.」
- 「Care must be taken to end the gate at a time when all motional modes have returned to the origin in phase space, and so the gate time is defined by α = 0 → μ_k t_gate = 2π for each mode k.」
- 「In the strong field regime, ions are coherently excited and the motional state is highly entangled with the internal state until all undesirable excitations are deterministically removed toward the end of the interaction.」
- 「The first experimental demonstration of the MS gate was performed in 2000 by David J. Wineland's group at the National Institute of Standards and Technology (NIST), with fidelities of F= .83 for 2 ions」（旁白未使用）

## Trapped-ion quantum computer（Wikipedia）

- 「vibrational energy in the ion trap is quantized into phonons by the energy eigenstates of the ion strand, which are called the center of mass vibrational modes.」
- 「In a trapped-ion quantum computer, the state of the center of mass phonon functions as the control qubit …」（Cirac–Zoller 閘：離子之間透過共享的振動做兩位元閘）

## 學程簡報 slides/Ion_NeutralAtom_Talk.pptx（python-pptx 讀取）

### 第 17 頁「集體振動：離子之間的『量子匯流排』」

- 「任一顆離子被雷射『推』，振動會傳到整條鏈 → 同一鏈內任兩顆都能直接做閘（全連接）」
- 備註：「兩位元閘的關鍵是離子之間怎麼溝通。答案是振動。」「用雷射推任何一顆離子，振動就會傳到整條鏈上的每一顆離子。」

### 第 18 頁「Mølmer–Sørensen 閘：用振動做糾纏」

- 「兩道雷射頻率 ω₀ ± (ω_m + δ)：自旋相依的力」
- 「不同自旋組合把離子往不同方向推 → 運動在相空間繞圈」
- 「繞完整圈（t = 2π/δ）運動回到原點，只留下依自旋而定的幾何相位」
- 「U = exp(−i π/4 · X1X2)」「|00⟩ → (|00⟩ − i|11⟩)/√2」
- 「閘時間 10–200 μs；對離子溫度不敏感（迴圈閉合）」
- 「幾何相位只看『圈的面積』，與運動初始狀態無關 —— 這就是 MS 閘高保真度的來源。」
- 備註：「做法是同時打兩道頻率：一道比量子位元頻率高一個振動頻率再多一點點 δ，另一道低同樣的量。這樣的光會對離子施加一個『自旋相依』的力：不同的自旋組合，力的方向不同。」
- 備註：「經過 t 等於 2π/δ 的時間，圈剛好繞完，運動回到原點，跟自旋完全解耦，只留下一個相位」「這個相位就產生最大糾纏：|00⟩ 變成 |00⟩ 和 |11⟩ 的疊加，就是一個 Bell 態。」
- 備註：「可以試著在迴圈還沒閉合時停下，會看到自旋和運動仍然糾纏，這就是錯誤。」
- 備註：「離子阱最經典的兩位元閘是 Mølmer–Sørensen 閘」「實務上閘時間 10 到 200 微秒。」

## 互動動畫 animations/js/atoms/05_ms.js

- desc：「合起來對每顆離子產生一個自旋相依力：自旋 σx = +1 往一邊推、−1 往另一邊推。」
- desc：「振動模態的狀態 α(t) = (ηΩ/δ)(e^{iδt} − 1) 在相空間畫圓。兩顆離子自旋相同（S_x = ±2）的分量往相反方向繞，自旋相反（S_x = 0）的分量不動。」
- desc：「在 t = 2πK/δ 時所有迴圈都回到原點，振動回到原來的狀態（不管原本多熱），只留下和圓面積成正比的幾何相位 → 等效於 exp(−iπ/4 · σxσx)。從 |00⟩ 出發得到 (|00⟩ − i|11⟩)/√2。」
- desc：「閘時間由 δ 決定，代表值 10–200 μs；保真度 > 99.9%（Quantinuum Helios 2025：99.921%）。若在迴圈還沒閉合時停下，自旋和振動仍然糾纏 → 錯誤。」
- 標籤：「振動模態的相空間」「位置 x」「動量 p」「S_x = +2（|++⟩）」「S_x = −2（|−−⟩）」「S_x = 0 不動」「離子 1　　離子 2」「ω₀ + (ω_m + δ)」「ω₀ − (ω_m + δ)」
- 控制項：「▶ 執行閘」、「失諧 δ/2π (kHz)」（5–50，預設 10）、「停止時刻（迴圈比例）」（0.1–1.0）、「顯示 2 個迴圈（K=2）」
- 讀數：「時間：… μs / 閘時間 … μs（δ/2π = … kHz，K = …）」「P(00) = …，P(11) = …，幾何相位 2Φ = … π」「迴圈閉合：振動回到原狀態，自旋和振動解開糾纏」／「迴圈未閉合（|α| = …）：自旋與運動仍糾纏 → 錯誤」
- 小圖「布居數與運動位移 vs 時間」：P(00) 藍、P(11) 紅、|α| 虛線、P(01)+P(10) = 0、黃色直線為目前時間；橫軸「時間 (μs)，閘時間 = … μs」

## 課綱

- Q070 lesson.json／brief.md：學習目標、動手任務、孩子獨立改造、好玩機制「解鎖成就」、作品「MS 閘說明圖」、生活技能「繞一圈回到原點的設計」、常見誤解「迴圈沒閉合時，運動與自旋仍糾纏，會造成錯誤」。
- Q069 brief.md：離子鏈的集體振動；正規模是讓離子彼此溝通的「量子匯流排」。
- Q071 brief.md：螢光讀取與 QCCD；知道狀態相依螢光怎麼讀取，以及 QCCD 如何搬運離子擴大規模。
