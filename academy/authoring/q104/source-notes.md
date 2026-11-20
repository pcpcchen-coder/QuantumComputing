# Q104 來源筆記（逐字引文）

查核日：2026-11-18。維基百科頁面由製作代理直接讀取原始 wikitext（revision id 取自 MediaWiki API 或頁面的 wgRevisionId）。學程內部文件、簡報與動畫程式由製作代理讀取。程式由製作代理實際執行。

## Quantum nondemolition measurement（Wikipedia，oldid=1344809079）

- 「Quantum nondemolition (QND) measurement is a special type of measurement of a quantum system in which the uncertainty of the measured observable does not increase from its measured value during the subsequent normal evolution of the system.」
- 「Note that the term "nondemolition" does not imply that the wave function fails to collapse.」

## Dilution refrigerator（Wikipedia，oldid=1375073377）

- 「A 3He/4He dilution refrigerator, or simply dilution refrigerator, is a cryogenic device that provides continuous cooling to temperatures as low as 2 mK, with no moving parts in the low-temperature region.」

## In-phase and quadrature components（Wikipedia，oldid=1386419474）

- 「The two amplitude-modulated sinusoids are known as the in-phase (I) and quadrature (Q) components」
- 「For received signals, by determining how much in-phase carrier and how much quadrature carrier is present in the signal it is possible to represent that signal using in-phase and quadrature components」

## Circuit quantum electrodynamics（Wikipedia，oldid=1337143447）

- 「If the detuning is significantly larger than the combined cavity and atomic linewidth the cavity states are merely shifted by ±g²/Δ (with the detuning Δ=ω_a−ω_r) depending on the atomic state. This provides the possibility to read out the atomic (qubit) state by measuring the transition frequency.」（該句頁面標有 Citation needed；本集的數值依學程文件與簡報，維基只作為觀念佐證）

## Transmon（Wikipedia，oldid=1377984572）

- 「a transmon is a type of superconducting charge qubit designed to have reduced sensitivity to charge noise.」
- 「Planar on-chip transmon qubits have T1 coherence times approximately 30 μs to 40 μs. Recent work has shown significantly improved T1 times as long as 95 μs … T1 is further improved up to 0.3 ms.」（本集 T₁ = 100 μs 為動畫看板的示意值，落在此範圍內）

## 學程內部文件：docs/超導量子電腦師生對話教學紀錄.md 第 6 課

- 「先回答：**不用重新降溫。** 稀釋冷凍機整個實驗期間都維持在約 10 mK，重新降溫要好幾天。每讀完一次，只需要讓「這顆位元」回到 |0⟩，最快幾 μs。」
- 「一個激發只有約 22 μeV，比可見光光子小約 10 萬倍，沒有偵測器能直接數；而且把能量取出來就把 |1⟩ 打回 |0⟩。所以改用**間接讀取**：旁邊放一個約 7 GHz 的讀取共振腔，讓位元狀態改變共振腔的音高——像敲鈴，從聲音判斷鈴裡裝什麼。」
- 「位元 5.21 GHz、共振腔 7 GHz，失諧 Δ ≈ 1.8 GHz ≫ g ≈ 100 MHz（色散區）：不交換能量，只互相推頻率。共振腔變成 f_r ± χ（|0⟩ 往下、|1⟩ 往上），χ … ≈ 0.77 MHz，兩狀態只差約 1.5 MHz」
- 「在兩個頻率正中間送很弱的探測微波（約 10 個光子…）；兩種狀態的反射相位一正一負，拆成 I、Q 就是 IQ 平面上兩個點。設計 κ ≈ 2χ，兩狀態相位差正好 90°」
- 「輸入線讓訊號下去、熱雜訊上不來；輸出線讓訊號上去、放大器雜訊回不來；JPA/TWPA 只多加約半個光子雜訊；FPGA 幾百 ns 內解調、積分、判別」
- 「每個 shot 積分 τ（約 100 ns–1 μs）得到一個 IQ 點…重複幾千次形成兩團高斯，中間畫閾值。…τ 太短雜訊大、太長衰減多；業界約 100–300 ns 可達 99% 以上。」
- 「量疊加態 → 塌縮；色散讀取不交換能量，屬於量子非破壞性（QND）量測：量到 1 再量還是 1（錯誤更正靠這點）。」
- 重設表格：「① 被動等待｜等 T₁ 自己衰減｜約 5T₁ ≈ 0.5 ms｜殘留約 0.7%，每秒只能跑約 2000 次」「② 主動重設｜讀一次，是 1 就送 π 脈衝｜約 1–3 μs｜快上百倍；誤差來自讀錯，常讀兩次確認」「③ 無條件重設｜特殊驅動把激發倒進讀取腔再漏走｜數百 ns–2 μs｜不必先讀，還能清掉 |2⟩」
- 課後練習答案 4：「共振腔的光子讓位元頻率偏移 2χ/光子（AC Stark），光子數的漲落會破壞疊加態的相位。」

## 學程內部簡報

- slides/transmon.pptx 第 16 頁：「色散讀取 χ/2π ≈ −0.77 MHz　共振腔頻率依位元狀態偏移，量反射訊號的相位判斷 |0⟩ 或 |1⟩」。
- 第 18 頁：「▶ 3D 第 5 章：讀取　色散讀取：從頻移讀出狀態 / ±χ 頻移、IQ 點群、讀取鏈與重設」。
- 第 19 頁：「讀取　位元與 7 GHz 共振腔失諧約 1.8 GHz，共振腔頻率依狀態偏移 χ/2π ≈ ±0.77 MHz。」
- （課綱寫 p20；p20 實為「案例：三顆可調 transmon 的頻率配置」，與本課無關，故改引 p16、18、19。）
- slides/JJ_Microwave_Readout_Talk.pptx 第 28 頁：「失諧很大 → 不交換能量，只互相「推」頻率」「量測只碰諧振腔，量子位元狀態不被翻轉 → QND」「腔內每多一個光子，量子位元頻率偏移 2χ（AC Stark shift）→ 讀取光子會造成失相」。
- 第 29 頁：「探測於兩峰中點：相位差最大、振幅相同」「2χ ≈ κ 時兩狀態在 IQ 平面分離最遠」；備註「試著把 χ/κ 調到 0.5，分離距離達到最大值 1。」
- 第 30 頁：外差解調「結果是每次量測一個複數點 (I, Q)」。
- 第 31 頁：「重疊誤差：放大器雜訊使兩團變寬 → 用量子極限放大器、加長積分」「T1 衰減：|1⟩ 在讀取中掉到 |0⟩ → 讀取要快」；備註「試著關掉「量子極限放大器」，兩團會變得很寬、互相重疊，保真度明顯下降」。

## 互動動畫程式

- animations/transmon-3d.html 第 5 章（id: readout）：html「本章分 8 步：為什麼要間接讀、色散偏移、探測與 IQ、整條讀取鏈、積分與判別、量測反作用與 QND、量完之後怎麼回到 |0⟩，最後是自由實驗。左上方字幕會跟著動畫說明。」；按鈕 `#g5prev`「◀ 上一步」、`#g5play`、`#g5re`「重播」、`#g5next`「下一步 ▶」、核取方塊 `#g5auto`「自動接續」、步驟按鈕 `#g5steps` 1–8。
- 第 7 步「重設」cues：6.5 秒「最簡單：被動等待，讓它以 T₁ 自己衰減。」；16.5 秒主動重設；23 秒無條件重設；29.5 秒等效溫度；dur 36。看板 drawBoard5（timeline）：標題「量完之後：讓「位元」回到 |0⟩，不是重新降溫」、「稀釋冷凍機：全程維持 ~10 mK（重新降溫一次要好幾天）」、三列（① 被動等待：閘 0.5、讀取 1、等待 ≈ 500 μs（5 T₁）灰色截斷，「→ 每個 shot ≈ 0.5 ms，每秒約 2,000 個」；② 主動重設：閘、讀取、判斷 0.35、π 0.12、確認讀取 1，「→ 約 1–3 μs，快上百倍」；③ 無條件重設：閘、讀取、重設脈衝、腔光子漏光，「→ 約 2 μs，不必先讀，也清 |2⟩」）、「比例尺：1 μs ≈ 120 px（被動等待的長條已截斷）」。
- animations/js/scenes/09_dispersive.js（index.html#dispersive）：藍色 0x4f8cff = |0⟩、紅色 0xff5a5f = |1⟩；按鈕「量子位元 |0⟩」「量子位元 |1⟩」「自動切換 |0⟩ ↔ |1⟩」（每 3 秒切換）；滑桿「色散位移 χ / κ」（0.05–2，預設 0.5）、「探測頻率 (ω − ω_r) / κ」；金色探測線與標籤「探測微波」；面板「兩狀態相位差 Δθ」「IQ 分離距離」「目前 2χ/κ … ✓ 最佳」；右下 IQ 平面小圖。
- animations/js/scenes/10_iq.js（index.html#iq）：軌跡從「時間 t = 0」落到「t = τ_int」；藍點製備 |0⟩、紅點製備 |1⟩；金色「判別閾值」；開關「量子極限放大器（JPA/TWPA）開啟」（關掉 σ 由 0.33 變 1.25）；滑桿「T1（與 τ_int 同單位，越大衰減越少）」（預設 8）；面板「讀取保真度 F」；右下「沿判別軸投影的直方圖」。

## 製作代理試拍（2026-11-18，單張截圖，非正式錄影）

- #dispersive：χ/κ = 0.10 → 「兩狀態相位差 Δθ = 22.6°」「目前 2χ/κ = 0.20」；χ/κ = 0.50 → 「Δθ = 90.0°」「IQ 分離距離 = 1.000」「目前 2χ/κ = 1.00 ✓ 最佳」。
- #iq：放大器開 F ≈ 95.2%（SNR ≈ 4.7）；關掉約 6 秒後 F ≈ 83.0%（SNR ≈ 1.3）；放大器開、T1 = 3 約 8 秒後 F ≈ 88.6–88.8%，紅點落入藍團與兩團之間。
- #readout：取消自動接續、按第 7 步後，鏡頭移到時間軸看板；25 秒後仍停在第 7 步（自動接續已關）。

## 實跑紀錄（reset_timer.py，Python 3.13.18，無外部套件）

```
T₁ = 100 μs
被動等待：等幾倍 T₁ → 每個 shot 多久、每秒幾個、還留在 |1⟩ 的比例
  等 1 T₁：   101.5 μs，每秒     9,852 個，殘留  36.79 %
  等 3 T₁：   301.5 μs，每秒     3,317 個，殘留   4.98 %
  等 5 T₁：   501.5 μs，每秒     1,994 個，殘留   0.67 %
  等 7 T₁：   701.5 μs，每秒     1,426 個，殘留   0.09 %
主動重設：2.97 μs，每秒 336,700 個
主動重設比等 5 T₁ 快 169 倍
```
