# Q051 來源筆記（逐字引文）

查核日：2026-11-18。維基百科頁面由製作代理以 MediaWiki API 直接取得（revision id 取自回應）。學程內部簡報與動畫程式由製作代理讀取。

## Quantum decoherence（Wikipedia，oldid=1384689551）

- 「Two timescales, T₁ and T₂, characterise this challenge and serve as standard metrics for qubit fidelity across most platforms.」
- 「The relaxation time T₁ characterizes how quickly a qubit loses energy to its environment as it decays from the excited state |1⟩ to the ground state |0⟩.」
- 「The dephasing time T₂ characterizes how quickly phase coherence in the qubit's state decays.」
- 「T₂ is commonly measured via the Ramsey interference experiment」
- 「The two timescales are related by T₂ ≤ 2T₁」

## Randomized benchmarking（Wikipedia，oldid=1370688133）

- 「Randomized benchmarking is an experimental method for measuring the average error rates of quantum computing hardware platforms.」
- 「Randomized benchmarking is the industry-standard protocol used by quantum hardware developers such as IBM and Google to test the performance of the quantum operations.」

## Confusion matrix（Wikipedia，oldid=1384661255）

- 「Each row of the matrix represents the instances in an actual class while each column represents the instances in a predicted class, or vice versa」
- 「The name stems from the fact that it makes it easy to identify whether the system is confusing two classes (i.e., commonly mislabeling one class as another).」

## Bell state（Wikipedia，oldid=1365950086）

- 「The Bell states are four specific maximally entangled quantum states of two qubits.」

## 學程內部簡報：slides/QC_Operation_Talk.pptx

- 第 14 頁：「校準結果存在『校準資料庫』→ 轉譯與脈衝排程時自動取用」「參數會漂移（溫度、TLS 缺陷、磁通雜訊）→ 雲端系統通常每天或每數小時自動重新校準；使用者看到的錯誤率就是最近一次的結果」。
- 第 15 頁「認識你的後端：校準資料怎麼看」表格：「T₁｜能量弛豫時間（|1⟩ 衰減）｜數十 ~ 數百 μs」「T₂｜相位相干時間｜數十 ~ 數百 μs（≤ 2T₁）」「單位元閘錯誤｜每個 √X / X 的錯誤率｜0.02% ~ 0.1%（20–50 ns）」「兩位元閘錯誤｜每個 CZ / ECR 的錯誤率｜0.1% ~ 1%（40–500 ns）」「讀取錯誤｜把 0 讀成 1 或反之｜0.5% ~ 3%（0.3–2 μs）」「耦合圖｜哪些量子位元之間可做兩位元閘｜方格、重六角（heavy-hex）等」；「使用者的選擇：挑錯誤率低的量子位元／避開不相鄰的配置／看 RB/EPLG、量子體積」。講者備註：「作為使用者，送出工作之前應該先看懂後端的校準資料」「單位元閘錯誤率大約萬分之二到千分之一」「把重要的邏輯量子位元放在錯誤率低的實體量子位元上，盡量讓需要互動的量子位元彼此相鄰」。（同頁的 Google Willow 數字本集未使用：簡報寫 T₁ ≈ 68 μs，維基百科 Willow processor 頁寫 100 μs，兩者不一致。）
- 第 16 頁：「initial_layout｜指定邏輯 → 實體量子位元｜手動挑低錯誤率、相鄰的量子位元」。

## 互動動畫程式

- animations/js/peripherals/10_bringup.js：見 fact-check.md 動畫段（第 28–29、40、43、54、55、57、58 行）。
- animations/js/scenes/10_iq.js：desc「積分時間越長 SNR 越好，但 T1 衰減會讓 |1⟩ 在讀取途中掉到 |0⟩，形成兩團之間的『拖尾』」「讀取保真度 F = 1 − [P(0|1) + P(1|0)] / 2」；`ui.toggle('量子極限放大器（JPA/TWPA）開啟', true)`（第 44 行）、`ui.slider('T1（與 τ_int 同單位，越大衰減越少）', 2, 40, 1, 8)`（第 47 行）。
- animations/transmon-3d.html 第 12 章步驟 3「③ 映射：挑今天狀況最好的實體位元」：「編譯器查今天的校準資料：每顆位元的單位元錯誤率、每條連線的 CZ 錯誤率…挑彼此相鄰、錯誤率最低的組合」「這叫『校準感知的映射』：同一個電路，昨天和今天可能被放到不同位置」；ERR1 = [0.031, 0.024, 0.018, 0.022, 0.045, …]、ERR2「0-1」0.62、「1-2」0.48、「2-3」0.55、「3-4」1.10（第 3375–3376 行）。
