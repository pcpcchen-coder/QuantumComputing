# Q050 來源筆記（逐字引文）

查核日：2026-11-18。維基百科頁面由製作代理直接開啟（revision id 取自頁面的 wgRevisionId）。學程內部簡報與動畫程式由製作代理讀取。

## Rabi cycle（Wikipedia，oldid=1383859287）

- 「In physics, the Rabi cycle (or Rabi flop) is the cyclic behaviour of a two-level quantum system in the presence of an oscillatory driving field.」
- 「The effect is important in quantum optics, magnetic resonance, and quantum computing, and is named after Isidor Isaac Rabi.」

## Ramsey interferometry（Wikipedia，oldid=1324106550）

- 「Ramsey interferometry, also known as the separated oscillating fields method, is a form of particle interferometry that uses the phenomenon of magnetic resonance to measure transition frequencies of particles.」
- 「Most precision atomic measurements, such as modern atom interferometers and quantum logic gates, have a Ramsey-type configuration.」
- 「Ramsey improved upon Rabi's method by splitting the one interaction zone into two very short interaction zones, each applying a π/2 pulse.」

## Randomized benchmarking（Wikipedia，oldid=1370688133）

- 「Randomized benchmarking is an experimental method for measuring the average error rates of quantum computing hardware platforms. The protocol estimates the average error rates by implementing long sequences of randomly sampled quantum gate operations.」
- 「Randomized benchmarking is the industry-standard protocol used by quantum hardware developers such as IBM and Google to test the performance of the quantum operations.」

## Calibration（Wikipedia，oldid=1378207888）

- 「In measurement technology and metrology, calibration is the comparison of measurement values delivered by a device under test with those of a calibration standard of known accuracy.」
- 「The design has to be able to "hold a calibration" through its calibration interval.」

## Topological sorting（Wikipedia，oldid=1380558942）

- 「For instance, the vertices of the graph may represent tasks to be performed, and the edges may represent constraints that one task must be performed before another; in this application, a topological ordering is just a valid sequence for the tasks.」

## 學程內部簡報：slides/QC_Operation_Talk.pptx

- 第 13 頁「初始化：每個 shot 都要回到 |0⟩」：「被動重置（等待熱化）」「10 mK 下熱平衡幾乎全在 |0⟩／等待 ~5 T₁ 讓 |1⟩ 自然衰減／簡單、不需回饋，但慢：數百 μs（如 250 μs）」；「主動重置（量測 + 回饋）」「先量測：若結果是 1 → 立刻送 π 脈衝翻回 0／需要 FPGA 即時判別（數百 ns 延遲）／快：~1–5 μs，可重複以提高純度」；「殘留熱激發 P(1) ≈ exp(−hf / kBT)／f = 5 GHz、有效溫度 50 mK → ≈ 0.8%」；「初始化錯誤會直接變成結果錯誤／重置時間常常佔一個 shot 的 90% 以上 → 決定吞吐量／有些平台還會重置洩漏到 |2⟩ 的狀態」。講者備註：「比被動重置快上百倍」「量子位元的『有效溫度』常常比冷凍機高，例如 50 mK」。
- 第 14 頁「校準：讓每個閘『剛好轉對角度』」：1 讀取腔頻譜（找到讀取頻率與色散位移）、2 量子位元頻譜（找到 f₀₁、f₁₂（非諧性））、3 Rabi 實驗（掃振幅 → π 脈衝振幅）、4 Ramsey 實驗（精確校正頻率（~kHz））、5 T₁ / T₂ 量測（相干時間）、6 DRAG / 精修（減少洩漏與相位誤差）、7 讀取最佳化（頻率、功率、積分權重、閾值）、8 兩位元閘（CZ 振幅/時間、相位修正）、9 基準測試（RB、XEB 得到錯誤率）；「校準結果存在『校準資料庫』→ 轉譯與脈衝排程時自動取用」；「參數會漂移（溫度、TLS 缺陷、磁通雜訊）→ 雲端系統通常每天或每數小時自動重新校準；使用者看到的錯誤率就是最近一次的結果」。講者備註：「Ramsey 實驗用兩個 π/2 脈衝之間的干涉，把頻率校到 kHz 等級」「把頻率失諧調到幾 MHz，同樣的 π 脈衝就轉不到南極了」。
- 第 15 頁：「T₁ 能量弛豫時間（|1⟩ 衰減）數十 ~ 數百 μs」「T₂ 相位相干時間 數十 ~ 數百 μs（≤ 2T₁）」。

## 互動動畫程式

- animations/js/peripherals/10_bringup.js：steps＝系統檢查、讀取腔頻譜、Punch-out、量子位元頻譜、Rabi、Ramsey、T₁ 量測、讀取最佳化、DRAG / 閘微調、隨機基準測試、上線 ✓（第 12–15 行）；`ui.button('◀ 上一步')`、`ui.button('下一步 ▶')`（第 28–29 行）、`ui.toggle('自動播放', true)`（第 30 行）；info.res「掃頻找出每個讀取腔的共振凹陷」、info.qspec「找到 f₀₁（高功率時也看到 f₀₂/2 → 非諧性）」、info.ramsey「條紋頻率 = 失諧量 → 修正頻率；包絡給出 T₂*」、info.t1「π 脈衝後等待 τ 再讀取，指數衰減給出 T₁」、info.iq「設定判別閾值，得到讀取保真度」、info.drag「精修 π、π/2 振幅（重複脈衝放大誤差）」；小圖：讀取腔金色 #e0a54a 凹陷曲線（第 49 行）、量子位元頻譜藍色 #4f8cff 兩峰 f₀₁ = 4.74 GHz、f₀₂/2 = 4.596 GHz（第 51 行）、Ramsey 青色 #38c6d9 衰減振盪（第 53 行）、T₁ 紅色 #ff5a5f 指數衰減標「T₁ ≈ 90 μs」（第 54 行）、IQ 藍紅兩團點（第 55 行）。
- animations/js/operation/03_pulse.js：subtitle「振幅×時間 = 旋轉角；相位 = 旋轉軸；頻率要對準 f₀₁」；`ui.slider('脈衝面積 → 旋轉角', 0, 360, 5, 180)`（第 71 行）、`ui.slider('頻率失諧 Δ（MHz）', -20, 20, 0.5, 0)`（第 73 行）、`ui.button('▶ 送出脈衝')`、`ui.button('重設 |0⟩')`（第 76、78 行）；desc「失諧（頻率沒對準）會讓旋轉軸往 z 傾斜，轉不到南極 → 閘錯誤，所以要先用 Ramsey 實驗校準頻率」「DRAG 在 Q 通道加上導數項，在 f₁₂ 挖出零點」。
- animations/transmon-3d.html 第 5 章（G5STEPS）：步驟 7「重設」看板三列：「① 被動等待／等 ~5 T₁（T₁ ≈ 100 μs）／等待 ≈ 500 μs（5 T₁）／→ 每個 shot ≈ 0.5 ms，每秒約 2,000 個」「② 主動重設／量測 → FPGA 判斷 → π／閘、讀取、判斷、π、確認讀取／→ 約 1–3 μs，快上百倍」「③ 無條件重設」；步驟 8「自由實驗」按鈕 data-p5="one"（|1⟩）、#c5m「量測一次」、#c5act「主動重設」（字幕「量到 1：FPGA 在幾百 ns 內送出 π 脈衝（XY 線），把 |1⟩ 翻回 |0⟩。整個重設約 1–3 μs。」）、#c5pas「被動等待 5T₁」；#g5auto「自動接續」、#g5play「暫停／播放」。
