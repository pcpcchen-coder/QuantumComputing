# Q049 來源筆記（逐字引文）

查核日：2026-11-18。維基百科頁面由製作代理直接開啟（revision id 取自頁面的 wgRevisionId）。學程內部簡報、文件與動畫程式由製作代理讀取。

## Bottleneck (production)（Wikipedia，oldid=1374872546）

- 「a bottleneck is a process in a chain of processes, such that its limited capacity reduces the capacity of the whole chain.」
- 「Bottlenecks can be found through: identifying the areas where accumulation occurs, evaluating the throughput, assessing whether each machine is being used at full capacity, and finding the machine with the high wait time.」

## 學程內部簡報（slides/QC_Operation_Talk.pptx）

- 第 3 頁「一次量子計算的生命週期」：「① 寫程式 / 線路 + shots」「② 轉譯 / 原生閘、配置」「③ 脈衝排程 / 奈秒時間軸」「④ 控制電子 / AWG / FPGA」「⑤ 晶片執行 / N 次 shots」「⑥ 判別與結果 / 直方圖」；「一次執行 = 很多 shots：每個 shot 都從 |0⟩ 重來」。講者備註：「第二站是轉譯，把我們寫的閘換成硬體真正會的『原生閘』，並決定每個邏輯量子位元要放在晶片上哪一顆實體量子位元。第三站把每個原生閘換成校準好的微波或磁通脈衝，排在奈秒等級的時間軸上。」「一個 shot 的時間裡，被動重置……往往佔了 98% 以上，真正的計算只有幾微秒。」
- 第 12 頁「兩種『操作者』」：雲端使用者看到的「後端清單、校準資料、佇列 / 送出線路 → 拿回 counts / 期望值」。
- 第 13 頁「初始化：每個 shot 都要回到 |0⟩」：被動重置「等待 ~5 T₁ 讓 |1⟩ 自然衰減」「簡單、不需回饋，但慢：數百 μs（如 250 μs）」；主動重置「先量測：若結果是 1 → 立刻送 π 脈衝翻回 0」「快：~1–5 μs」；「重置時間常常佔一個 shot 的 90% 以上 → 決定吞吐量」。
- 第 15 頁表：T₁「數十 ~ 數百 μs」；單位元閘「0.02% ~ 0.1%（20–50 ns）」；兩位元閘「0.1% ~ 1%（40–500 ns）」；讀取「0.5% ~ 3%（0.3–2 μs）」；使用者的選擇「挑錯誤率低的量子位元 / 避開不相鄰的配置」。
- 第 16 頁表：shots「重複次數 → 統計誤差 ∝ 1/√N」；最佳化等級（0–3）「一般用 1–2；越高轉譯越久」；重複延遲 / 初始化「影響吞吐量與初始化錯誤」。
- 第 20 頁：「長度 | ~20–50 ns」；備註「一個 X 閘在硬體上到底是什麼？答案是：一段大約 20 到 50 奈秒、頻率對準 f01 的微波脈衝。」
- 第 30 頁：「讀取脈衝 / ~0.3–2 μs」「在 FPGA 中用閾值（或線性判別）即時判成位元」。
- 第 32 頁：「精度 ×10 → shots ×100」；備註「100 shots 誤差約 5%，1000 shots 約 1.6%」。

## 學程文件

- docs/超導量子電腦師生對話教學紀錄.md「二、跟著 Bell 電路走一遍」：「原生閘只有 Rz（任意角）、√X、CZ」「H = Rz(π/2)·√X·Rz(π/2)；CNOT = 目標 H → CZ → 目標 H」「路由：不相鄰就插 SWAP」「Rz 是虛擬 Z、**0 ns**」；脈衝表「√X … 20–40 ns」「Rz(θ) 不送東西，改後續脈衝相位 … 0 ns」「CZ … 40–60 ns」「量測 … 0.3–1 μs」；「所有通道鎖同一個 10 MHz 參考時鐘」；「**編譯、上傳、排隊常比跑還久**，所以要打包成 job」。

## 互動動畫程式

- animations/js/operation/12_workflow.js：六站名稱「① 寫程式」「② 轉譯」「③ 脈衝排程」「④ 控制電子」「⑤ 晶片執行 shots」「⑥ 判別與結果」（第 18–23 行）；程式螢幕 `qc = QuantumCircuit(2) / qc.h(0) / qc.cx(0, 1) / qc.measure_all() / sampler.run([qc], shots=N)`（第 36 行）；映射標籤「q0→Q3」「q1→Q1」（第 41 行）；時間軸標籤「D=驅動 Z=磁通 M=讀取」（第 48 行）；機櫃標籤「AWG / LO / ADC / FPGA」（第 52 行）；NOTES（第 65–70 行）：「透過雲端 API 送出工作，進入佇列」「所有儀器鎖在同一個 10 MHz 參考時脈，觸發後同步輸出」「量子態只活幾十～幾百 μs，所以每次都要重來」「FPGA 把每個讀取訊號積分、判別成 0/1，累積成計數，回傳給使用者」；控制項 `ui.toggle('自動播放')`、`ui.button('下一站 ▶')`、`ui.slider('shots N', 2, 5, …)`、`ui.slider('線路深度（層）', 1, 1000, …)`、`ui.toggle('主動重置（量測 + 條件 π 脈衝）')`（第 73–77 行）；`times()`：重置 主動 2.0／被動 250 μs、閘 = 深度 × 0.1 μs、讀取 1.0 μs（第 79 行）；插圖「一個 shot 的時間組成（μs）與總執行時間」「另加：佇列、轉譯、波形載入、網路傳輸（秒～分鐘）」「數值為典型量級（依系統而異）」（第 81–93 行）。
- animations/js/operation/03_pulse.js：預設 `area = 180, Tg = 40`（第 39 行）；滑桿「脈衝面積 → 旋轉角」「閘長度（ns）」10–80（第 71、74 行）；按鈕「▶ 送出脈衝」「虛擬 Z（90°）」「重設 |0⟩」（第 76–78 行）；說明「虛擬 Z 閘：不送任何脈衝，只把之後所有脈衝的相位平移 —— 零時間、零誤差」（第 10 行）；讀數「峰值 Rabi 頻率 ≈ … MHz」（第 129 行）。
