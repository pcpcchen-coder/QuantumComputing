# Q046 來源筆記（逐字引文）

查核日：2026-11-18。維基百科頁面由製作代理直接下載頁面 HTML 取得（revision id 取自頁面的 wgRevisionId；MediaWiki API 當天回應限流）。學程內部簡報與動畫程式由製作代理讀取。

## Rubidium standard（Wikipedia，oldid=1383394087）

- 「A rubidium standard or rubidium atomic clock is a frequency standard in which a specified hyperfine transition of electrons in rubidium-87 atoms is used to control the output frequency.」
- 「The Rb standard is the most inexpensive, compact, and widely produced atomic clock, used to control the frequency of television stations, cell phone base stations, in test equipment, and global navigation satellite systems like GPS.」

## Phase-locked loop（Wikipedia，oldid=1383556039）

- 「A phase-locked loop (PLL) is a control system that generates an output signal whose phase is fixed relative to the phase of an input signal.」
- 「By incorporating a frequency divider, a PLL can generate a stable frequency that is a multiple of the input frequency. These properties are used for clock synchronization, demodulation, frequency synthesis, clock multipliers, and signal recovery from a noisy communication channel.」

## Arbitrary waveform generator（Wikipedia，oldid=1279162486）

- 「These waveforms can be either repetitive or single-shot (once only) in which case some kind of triggering source is required (internal or external).」
- 「Unlike function generators, AWGs can generate any arbitrarily defined waveshape as their output.」

## Frequency mixer（Wikipedia，oldid=1380404812）

- 「In its most common application, two signals are input and two signals are output, having frequencies equal to the sum and the difference of the original frequencies.」
- 「Mixers are widely used to shift signals from one frequency range to another, a process known as heterodyning」

## Field-programmable gate array（Wikipedia，oldid=1385952866）

- 「A field-programmable gate array (FPGA) is a type of configurable integrated circuit that can be repeatedly programmed after manufacturing.」
- 「which benefit from their flexibility, high signal processing speed, and parallel processing abilities.」

## 學程內部簡報：slides/QC_Peripheral_Systems_Talk.pptx

- 第 20 頁「控制系統架構」：「3D 場景 6：上傳 → 觸發 → 驅動 → 讀取 → 判別 → 回饋 → 回傳（依序播放）」；「AWG / DAC：產生驅動與讀取波形（GSa/s 等級、14-bit）」「LO + IQ 混頻器：上變頻到 4–8 GHz（外差架構）」「ADC + 下變頻：讀取訊號數位化（數 GSa/s）」「FPGA：序列播放、解調、判別、即時回饋」「DC 電流源：磁通偏壓（低雜訊、高解析度）」「同步器 + 參考時脈：所有儀器同相位、同觸發」「每顆量子位元約需 2–3 個高速通道 + 1 個 DC 通道」。備註：「取樣率每秒數十億次、14 位元解析度」「再在幾百奈秒內回饋一個條件式的 π 脈衝做主動重置」。
- 第 21 頁「外差 IQ 混頻 vs 直接射頻合成」：「AWG 產生中頻（~100 MHz）I/Q」「LO + 類比 IQ 混頻器上變頻」「需校正 IQ 不平衡、LO 洩漏、鏡像」「元件成熟、成本較低」；「高速 DAC 直接合成 GHz 訊號」「數位上變頻（NCO），無類比混頻器」「免 IQ 校正、通道一致性好」「近年主流（RFSoC、新一代儀器）」。
- 第 22 頁「時脈與同步：所有儀器踩同一個節拍」：「銣原子鐘 / GPS 馴服 / 10 MHz 參考」「10 MHz 參考：所有 LO、DAC、ADC 的頻率都由它倍頻而來 → 相位彼此鎖定」「觸發 / 同步匯流排：讓數十台儀器在同一個時鐘週期開始播放（例：100 MHz 同步時脈）」「量子閘的相位就是微波的相位：驅動 LO 與讀取 LO 若沒有鎖定，每次量測的參考相位都會漂移」「雙量子位元閘需要兩個通道的脈衝奈秒級對齊」「觸發抖動（jitter）必須遠小於脈衝寬度（~數十 ns）」「實務：參考時脈用低雜訊分配放大器、等長纜線，並在軟體中校正固定延遲」。
- 第 23 頁「即時回饋與直流偏壓源」：「~350 ns 單機內回饋延遲（Zurich SHFQC）」「< 550 ns 跨機櫃系統回饋（經 PQSC）」「< 400 ns 量測結果分配網路（Qblox LINQ）」「主動重置：讀到 1 就送 π 脈衝，比等待 T1 衰減快百倍」「糾錯解碼器：每輪症狀（syndrome）須在 ~μs 內解碼」。

## 互動動畫程式

- animations/js/peripherals/06_electronics.js：模組標籤「銣原子鐘 / 10 MHz 分配」「同步器 / 觸發分配」「AWG / DAC（XY 驅動）」「LO 合成器」「IQ 混頻器（上變頻）」「讀取模組：AWG + 下變頻 + ADC」「FPGA 即時處理 / 回饋」「DC 電流源（磁通偏壓）」「HEMT 偏壓 · TWPA 泵浦源」；步驟標籤「① 上傳脈衝序列 → 同步器」「② 同步觸發」「② AWG 中頻 I/Q → 混頻器」「② 上變頻 → XY 驅動脈衝進入冷凍機」「② 直接合成 GHz 脈衝 → 冷凍機」「③ 讀取脈衝 → 晶片」「③ 讀取訊號返回 → 下變頻 + ADC」「③ FPGA 解調、判別 0 / 1」「④ 即時回饋（~0.35–0.55 μs）→ AWG」「④ 條件式 π 脈衝（主動重置）」「⑤ 結果回傳電腦」；選項按鈕「外差 IQ 混頻架構」「直接射頻合成（RFSoC 等）」；滑桿「播放速度」0.3–2；插圖「XY 驅動波形：中頻 I/Q 包絡 → 4–8 GHz 載波」、橫軸「時間（~40 ns 脈衝）」、「I：高斯包絡」「Q：DRAG 修正」「上變頻後的 RF」；說明「所有儀器鎖在同一個 10 MHz 參考時脈（常用銣原子鐘）與觸發網路上，確保相位一致、時序精確」；直接合成模式時 LO 與混頻器模組亮度由 0.12 降到 0.02。
- animations/js/operation/03_pulse.js：「脈衝面積（振幅 × 時間）決定旋轉角」「脈衝相位 φ 決定旋轉軸：0° → 繞 x，90° → 繞 y」；預設 `Tg = 40`（ns）、標籤「transmon（f₀₁ ≈ 5 GHz）」；滑桿「脈衝面積 → 旋轉角」「脈衝相位 φ → 旋轉軸方向」；按鈕「▶ 送出脈衝」「重設 |0⟩」。
