# Q117 來源筆記（逐字引文）

查核日：2026-11-19（檔頭 CHECKED 依派工統一寫 2026-11-18）。維基百科頁面由製作代理以 `action=raw` 取得原始 wikitext（2026-11-19；查 revision id 的 API 當時回應限流，未記錄版本號）。學程內部簡報、簡報原始稿與動畫程式由製作代理讀取。程式由製作代理實際執行。

## Greenberger–Horne–Zeilinger state（Wikipedia）

- 「a '''Greenberger–Horne–Zeilinger''' ('''GHZ''') '''state''' is an entangled quantum state that involves at least three subsystems (particle states, qubits, or qudits). Named for the three authors that first described this state」
- 「The four-particle version was first studied by Daniel Greenberger, Michael Horne and Anton Zeilinger in 1989」「The following year Abner Shimony joined in and they published a three-particle version」
- 「The GHZ state is an entangled quantum state for 3 qubits and it can be written |GHZ⟩ = (|000⟩ + |111⟩)/√2」
- 「In the case of each of the subsystems being two-dimensional, that is for a collection of M qubits, it reads |GHZ⟩ = (|0⟩^⊗M + |1⟩^⊗M)/√2.」
- 「If a measurement is made on one of the photons using a two-channel polarizer aligned with the axes of the coordinate system, each orientation will be observed with 50% probability. However the result of all three measurements on the state gives the same result」
- 「The N-qubit GHZ state becomes unentangled if even one qubit is lost」
- 「Generation of the 3-qubit GHZ state using quantum logic gates.」（頁首圖說）

## Controlled NOT gate（Wikipedia）

- 「The CNOT gate flips the second qubit (the target qubit) if and only if the first qubit (the control qubit) is |1⟩.」

## No-cloning theorem（Wikipedia）

- 「the '''no-cloning theorem''' states that it is impossible to create an independent and identical copy of an arbitrary unknown quantum state」

## 學程內部簡報（slides/output/basic-circuits.pptx；原始稿 slides/reports/basic-circuits.js）

用 python-pptx 讀出：第 13 頁「範例 4｜GHZ 態：CNOT 一路串下去」、第 14 頁「振幅逐步看：一次多綁一顆」（課綱寫 p13–14，無誤）。

- 第 13 頁：線路 q0、q1、q2 都是 |0⟩；「① H 閘（q0）(|000⟩ + |001⟩)/√2 q0 進入疊加，其他位元還在 0」「② CNOT（q0 → q1）(|000⟩ + |011⟩)/√2 q0 的值『複製』到 q1：兩顆綁在一起」「③ CNOT（q1 → q2）(|000⟩ + |111⟩)/√2 三顆全部糾纏：不是全 0 就是全 1」。
- 第 13 頁備註：「第四個範例把 Bell 電路的 CNOT 一路串下去。先對 q0 做 H，然後 CNOT 從 q0 到 q1，把 q0 的值複製給 q1；再 CNOT 從 q1 到 q2。三顆位元全部糾纏，量測結果不是 000 就是 111，各一半。要注意這裡的複製只是在計算基底上把 0、1 對應起來，並不是把一個未知的量子態複製一份，那是不可能的。動畫裡可以切換成 4 顆位元。」
- 第 14 頁：「橫軸是 q2 q1 q0 的 8 種結果」；「① H（q0）+1/√2 000、+1/√2 001｜000、001 各半」「② CNOT（q0 → q1）｜001 搬到 011」「③ CNOT（q1 → q2）｜011 搬到 111：只剩 000、111」；callout「硬體常用 GHZ 態測試糾纏品質：雜訊越大，量到 000、111 以外結果的比例越高」。
- 第 14 頁備註：「每做一次 CNOT，就把 q0 等於 1 的那一根往右搬一次：001 搬到 011，再搬到 111。最後只剩 000 和 111 兩根。GHZ 電路的深度會隨位元數增加，每多一顆就多一個 CNOT，所以硬體廠常用它來測試多位元糾纏的品質：理想情況只會量到全 0 或全 1，雜訊越大，其他結果出現的比例就越高。我們的動畫是理想模擬，所以不會出現其他結果。」

## 互動動畫程式（animations/basic-circuits.html #ghz）

- `id: "ghz", short: "GHZ 態", title: "GHZ 態：多顆位元一起糾纏"`；lead「把 Bell 電路的 CNOT 一路串下去，就能讓任意多顆位元糾纏在一起：量測結果不是全 0 就是全 1。」
- 選項 `{ key: "n", label: "位元數", def: "3", choices: [["3", "3 顆"], ["4", "4 顆"]] }`；步驟：`H 閘：q0 進入疊加`，再 `CNOT：q${i} → q${i + 1}`（i = 0 … n − 2）。
- CNOT 說明：「CNOT 把 q${i} 的值『複製』到 q${i + 1}：q${i} 是 1 的那一半，q${i + 1} 也翻成 1。現在有 ${i + 2} 顆位元綁在一起。」最後一步：「最後一個 CNOT 完成後，${n} 顆位元全部糾纏：只剩 |0…0⟩ 和 |1…1⟩ 兩項，各 50%。量到任何一顆，其他 ${n − 1} 顆的結果也就確定了。」
- 重點：「GHZ 電路的深度隨位元數增加，每多一顆就多一個 CNOT。硬體廠常用它來測試多位元糾纏的品質：雜訊越大，量到全 0、全 1 以外結果的比例就越高（這裡是理想模擬，所以不會出現）。」
- GHZ 範例沒有 `bloch` 欄位，所以不畫 Bloch 球；`buildBars`：2ⁿ > 8 時 `.bars.dense`（標籤不加 |⟩、振幅數字隱藏）；`histRender` 只列理論機率不為 0 的結果；`rebuild(false)` 改選項時停在最後一步並清除量測；柱子在兩步間 650 ms 內插。

## 互動動畫程式（animations/operation.html#register，js/operation/04_register.js）

- 滑桿「量子位元數 n」1–4（改值時 `setup()` 重建，狀態回到 |0…0⟩）；按鈕「目標 q0」…「目標 q3」「H」「X」「Z」「S」「T」「CNOT（控制 = 目標+1 → 目標）」「CZ」「均勻疊加 H⊗ⁿ」「Bell 態」「GHZ 態」「測量全部」「只測 q0」「重設 |0…0⟩」。
- 「GHZ 態」按鈕：`st.gate('H', n - 1); for (let q = n - 1; q > 0; q--) st.cx(q, q - 1);`（從最高位往下串）。
- Bloch 球位置 `x = ((n - 1) / 2 - q) * 2.3`：n = 3 時左 q2、中 q1、右 q0。讀數「各量子位元 Bloch 長度：q0 …，q1 …，q2 …」；任一顆 < 0.98 時「有糾纏：單一量子位元的向量變短（約化態是混態）」，否則「無糾纏（可分離態）：每個量子位元各自是純態」。

## 實跑紀錄

`ghz_lab.py`（Python 3.13.18，只用標準函式庫，random.Random(1117)）：輸出全文見 `classroom.py` 的 `RUN_OUTPUT`（建置時會重跑並逐字比對）。重點：

```
  H(q0)         |000⟩ +0.707  |001⟩ +0.707        單看 q0 1.0  q1 1.0  q2 1.0
  CNOT(q0→q1)   |000⟩ +0.707  |011⟩ +0.707        單看 q0 0.0  q1 0.0  q2 1.0
  CNOT(q1→q2)   |000⟩ +0.707  |111⟩ +0.707        單看 q0 0.0  q1 0.0  q2 0.0
  3 顆： 000 → 495 次  111 → 505 次
  4 顆： 0000 → 470 次  1111 → 530 次
  3 顆少接 CNOT(q0→q1) 只量到 000、001
  3 顆少接 CNOT(q1→q2) 只量到 000、011
  4 顆少接 CNOT(q1→q2) 只量到 0000、0011
  3 顆 H(q0) → CNOT(q0→q1) → CNOT(q0→q2)   和串下去一樣嗎？ True
  3 顆（2 個 CNOT）：量到全 0、全 1 以外的機率 4.0%
  4 顆（3 個 CNOT）：量到全 0、全 1 以外的機率 5.9%
  8 顆（7 個 CNOT）：量到全 0、全 1 以外的機率 13.2%
```

`qiskit_check.py`（Qiskit 2.6.2，StatevectorSampler seed=2026；四個線路用同一個種子，所以次數的數字相同）：

```
3 顆 理論機率 {'000': 0.5, '111': 0.5} 量測 1000 次 {'000': 464, '111': 536}
4 顆 理論機率 {'0000': 0.5, '1111': 0.5} 量測 1000 次 {'0000': 464, '1111': 536}
3 顆，少接 CNOT(q1→q2) 理論機率 {'000': 0.5, '011': 0.5} 量測 1000 次 {'000': 464, '011': 536}
4 顆，少接 CNOT(q1→q2) 理論機率 {'0000': 0.5, '0011': 0.5} 量測 1000 次 {'0000': 464, '0011': 536}
```

## 動畫畫面（製作代理以 Playwright 1600×900 實拍；basic-circuits.html zoom 0.8）

- #ghz（3 顆）逐步：「(|000⟩ + |001⟩) / √2｜第 1 步 H 閘：q0 進入疊加」→「(|000⟩ + |011⟩) / √2｜第 2 步 CNOT：q0 → q1」→「(|000⟩ + |111⟩) / √2｜第 3 步 CNOT：q1 → q2」；柱子 +.707、50%；量測 1,000 次只列 000、111 兩列（實拍一次 535／465，隨機）。
- 選「4 顆」：「步驟 4 / 4」，|ψ⟩ = (|0000⟩ + |1111⟩) / √2，16 根細柱只剩最左、最右兩根，各寫 50%；起點逐步：0001 → 0011 → 0111 → 1111。量測 1,000 次只列 0000、1111（實拍一次 494／506）。
- operation.html#register，n = 3：起點「1.00 |000⟩」長度 1.00、1.00、1.00 無糾纏；目標 q2 → H：「0.71 |000⟩ + 0.71 |100⟩」1.00、1.00、1.00 無糾纏；目標 q1 → CNOT：「0.71 |000⟩ + 0.71 |110⟩」q0 1.00、q1 0.00、q2 0.00「有糾纏」（左、中兩球的箭頭縮成一點，右邊 q0 的箭頭仍指向 |0⟩）；目標 q0 → CNOT：「0.71 |000⟩ + 0.71 |111⟩」三個 0.00。右下記憶體插圖蓋住最右邊柱子的標籤 |111⟩，旁白不提該標籤。
