# Q120 來源筆記（逐字引文）

查核日：2026-11-19（檔頭 CHECKED 依派工統一寫 2026-11-18）。維基百科頁面由製作代理直接讀取原始 wikitext（action=raw），revision id 取自頁面的 wgRevisionId。學程內部簡報（python-pptx 讀出實際頁碼、文字與備註）、文件與動畫程式由製作代理讀取，畫面以 Playwright 單張截圖確認。程式由製作代理實際執行。

## Bernstein–Vazirani algorithm（Wikipedia，oldid=1371471620）

- 「The '''Bernstein–Vazirani algorithm''', which solves the '''Bernstein–Vazirani problem''', is a quantum algorithm invented by Ethan Bernstein and Umesh Vazirani in 1997.」
- 「It is a restricted version of the Deutsch–Jozsa algorithm where instead of distinguishing between two different classes of functions, it tries to learn a string encoded in a function.」
- Problem statement：「f(x) is promised to be the dot product between x and a secret string s ∈ {0,1}^n modulo 2, f(x) = x · s = x_1s_1 ⊕ x_2s_2 ⊕ ⋯ ⊕ x_ns_n, find s.」
- 「Classically, the most efficient method to find the secret string is by evaluating the function n times with the input values x = 2^{i} for all i ∈ {0, 1, …, n−1}」
- 「In contrast to the classical solution which needs at least n queries of the function to find s, only one query is needed using quantum computing.」
- 「Next, apply the oracle U_f which transforms |x⟩ → (−1)^{f(x)}|x⟩. This can be simulated through the standard oracle that transforms |b⟩|x⟩ → |b ⊕ f(x)⟩|x⟩ by applying this oracle to (|0⟩ − |1⟩)/√2 |x⟩.」
- 「Another Hadamard transform is applied to each qubit which makes it so that for qubits where s_i = 1, its state is converted from |−⟩ to |1⟩ and for qubits where s_i = 0, its state is converted from |+⟩ to |0⟩.」
- 「Since s ⊕ y = 0 is only true when s = y, this means that the only non-zero amplitude is on |s⟩. So, measuring the output of the circuit in the computational basis yields the secret string s.」

## Hadamard transform（Wikipedia，oldid=1382060647）

- Short description：「Involutive change of basis in linear algebra」；首段「It performs an orthogonal, symmetric, involutive, linear operation on a tuple of 2^m numbers.」
- 「The rows of the Hadamard matrices are the Walsh functions.」
- 「However, if the Hadamard gate is applied twice in succession (as is effectively being done in the last two operations), then the final state is always the same as the initial state.」
- 「For example, this is used in the Deutsch–Jozsa algorithm, Simon's algorithm, the Bernstein–Vazirani algorithm, and in Grover's algorithm.」

## 學程內部簡報：slides/output/basic-circuits.pptx

課綱寫 p21–22，頁碼無誤。
- 第 21 頁「範例 7｜BV：查一次讀出整串密碼」：「q0 |0⟩」「q1 |0⟩」「q2 |0⟩」「q3 |0⟩（輔助）」「① 輔助 q3 翻成 1　q0–q2 是輸入，q3 接收答案」「② 全部 H　q0–q2 同時代表 8 種輸入；q3 變成 |−⟩」「③ 黑盒：密碼 s = 101　q0、q2 各接一條 CNOT 到 q3；每個輸入帶上 (−1)s·x」「④ 再做 H、量測　q2 q1 q0 = 101：正好就是密碼」。
  備註：「黑盒的做法很簡單：密碼哪一位是 1，就從那顆位元接一條 CNOT 到 q3」。
- 第 22 頁「振幅逐步看：密碼藏在正負號的排列裡」：「只畫 q2 q1 q0 的 8 種結果；輔助位元 q3 一直停在 |−⟩，先提出來不畫」「8 種輸入振幅都是 1/(2√2) ≈ 0.35」「s·x 為奇數的輸入多一個負號：機率仍各 12.5%」「只剩 101：機率 100%」「③ 的正負號排列，正好是 H 作用在 |101⟩ 上的結果；所以 ④ 再做一次 H，就把它還原成 |101⟩」。
  備註：「這個正負號的排列，剛好就是對 |101⟩ 做 H 會得到的樣子，而 H 做兩次等於什麼都沒做，所以第四步再一個 H，就把它還原成 |101⟩，百分之百讀出密碼。」

## 學程文件：docs/超導量子電腦師生對話教學紀錄.md 第 7 課

- 「黑盒子藏著 s = 101，輸入 x 回答 s·x 的奇偶。古典要問 3 次（100、010、001），量子**只問 1 次**。」
- 八振幅表：「2 查詢一次 … x₁+x₃ 為奇數的翻負號；**機率仍各 12.5%**」。
- 「**重複多次是為了在雜訊中確認哪個答案最突出**，不是要讀出全部機率。」
- 課後練習 3：「若 s = 011，步驟 2 哪些基態會變負號？」參考答案：「x₂ + x₃ 為奇數者：001、010、101、110。」

## 互動動畫原始碼

- `animations/basic-circuits.html` BV 場景：`title: "Bernstein–Vazirani：查一次就猜中密碼"`；`opts: [{ key: "s", label: "密碼 s（s2 s1 s0，點一下切換）", def: "101", bits: 3 }]`；
  `for (let i = 0; i < 3; i++) if (s[2 - i] === "1") oracle.push([CX(i, 3)]);`；第 2 步 cap「振幅長條上有 16 根柱子，因為 q3 的 |−⟩ 也算在裡面」；第 3 步 cap「相位回踢讓每個輸入 x 帶上 (−1)^(s·x) 的正負號，密碼就藏在這些正負號的排列裡」；
  `verdict: k => "→ 密碼 s = " + k`；Qiskit 程式碼最後一行註解「位元字串的最右邊是 q0」。按鈕 `#bFirst`「⏮ 起點」、`#bNext`「下一步 ▶」、`#m1000`「量測 1,000 次」。
- `animations/transmon-3d.html` 第 9 章第 8 步「自由實驗」body：「勾選「讀取雜訊」會加入每顆位元 3% 的讀取誤判。」「值得試試：s = 000 時黑盒子什麼都不做，H⊗3 做兩次等於沒做，結果回到 000；s = 111 時三顆都被 Z，結果 111。」
  控制項：`data-s9="0"…"7"`、`data-op9="H3"|"O"|"H3b"|"M"`（「① H⊗3」「② 黑盒子」「③ H⊗3」「④ 量測 50 次」）、`#g9reset`「重設」；`RED` 負振幅、`COL.gold` 正振幅。
- `animations/js/operation/06_circuit.js`：`bv: { name: 'Bernstein–Vazirani（秘密字串 101）', n: 4, meas: [0, 1, 2], cols: [ [[X(3)], …], [all(4, H), …], [[CX(0, 3), CX(2, 3)], …], [all(4, H), …], [M([0, 1, 2]), '量測得到 101。量子：1 次查詢；古典：要 n = 3 次'] ] }`；
  `ui.toggle('加入雜訊（每閘 1%、讀取 3%）', …)`；`const pg = noise ? 1 - Math.pow(0.99, gates) : 0, pr = noise ? 0.03 : 0;`；插圖標題「量測 1000 shots 的結果（青線 = 理想機率）」。

## Playwright 實拍紀錄（1600×900，nice -n 19，單張截圖）

- bc#bv 點第 1、2 個密碼鈕 → 「s2=0 s1=1 s0=1」；從起點逐步：第 2 步 16 根 +.250 ×8、−.250 ×8；第 3 步 `+.250,−.250,−.250,+.250,+.250,−.250,−.250,+.250,−.250,+.250,+.250,−.250,−.250,+.250,+.250,−.250`；第 4 步只剩 0011 +.707、1011 −.707；量 1,000 次「→ 密碼 s = 011」。
- tr#bv 第 8 步：s = 000 ① 八根 +0.35 ② 虛線框「黑盒子 s = 000」內沒有 Z ③ |000⟩ +1.00 ④「量測最多的是 000（50/50 次），猜中 ✓」；s = 111：看板三條線都是 Z，001、010、100、111 變紅。
- op#circuit「Bernstein–Vazirani（秘密字串 101）」單步 5 次：readout「1000 shots：101: 1000」，插圖 101 一根頂到青線；打開加入雜訊：「101: 826，100: 50，111: 34（含雜訊）」（隨機，旁白不念）。

## 程式實跑（課堂教材 classroom.py 內嵌全文）

- `bv_lab.py`（Python 3.13.18，只用標準函式庫，random 種子 1120）與 `qiskit_check.py`（Qiskit 2.6.2，StatevectorSampler seed=2026）輸出全文見 `classroom.py` 的 RUN_OUTPUT、QISKIT_OUTPUT；建置時會再跑一次 bv_lab.py 比對。
