# Q126 來源筆記（逐字引文）

查核日：2026-11-19（檔頭 CHECKED 依派工統一寫 2026-11-18）。維基百科頁面由製作代理直接讀取原始 wikitext（action=raw，2026-11-19），revision id 未取得。學程內部簡報（讀出實際頁碼與文字）與動畫程式由製作代理讀取，畫面以 Playwright 單張截圖確認（nice -n 19，未錄影、未跑 QV2_DRY）。程式由製作代理實際執行。

## Fault injection（Wikipedia，2026-11-19 raw wikitext）

- 「In [[computer science]], '''fault injection''' is a testing technique for understanding how computing systems behave when stressed in unusual ways.」
- 「In [[software testing]], fault injection is a technique for improving the coverage of a test by introducing faults to test code paths; in particular error handling code paths, that might otherwise rarely be followed. It is often used with stress testing and is widely considered to be an important part of developing robust software.」

## Quantum depolarizing channel（Wikipedia，2026-11-19 raw wikitext）

- 「A '''quantum depolarizing channel''' is a model for [[quantum noise]] in quantum systems. The d-dimensional depolarizing channel … maps a state ρ onto a linear combination of itself and the maximally mixed state, Δλ(ρ) = (1 − λ)ρ + (λ/d)I.」
- 「In the case where λ = 1 the channel returns the maximally-mixed state for any input state ρ, which corresponds of the complete contraction of the Bloch-sphere down to the single-point I/2 given by the origin.」
- 本課的白話：有 λ 的機會，狀態被換成「完全打亂」的最大混合態；最大混合態量起來每個結果機率相同（所以量子硬幣看不出差別）。qiskit-aer 的 `depolarizing_error(p, n)` 參數 p 就是這裡的 λ。

## Noisy intermediate-scale quantum computing（Wikipedia，2026-11-19 raw wikitext；Noisy_intermediate-scale_quantum_era 轉址至此）

- 「However, these qubits are inherently "noisy" – they suffer from decoherence, gate errors, and measurement errors that accumulate during computation」
- 「Gate fidelities hover around 99-99.5% for single-qubit operations and 95–99% for two-qubit gates, which while impressive, still introduce significant errors in circuits with thousands of operations.」

## 學程簡報：如何操作量子電腦（slides/QC_Operation_Talk.pptx）

- 第 47 頁「錯誤預算：能跑多深的線路？」：「F線路 ≈ (1 − ε1Q)G₁ (1 − ε2Q)G₂ (1 − εM)n」「直覺」「兩位元閘錯誤 0.3% → 約 230 個兩位元閘後成功率剩 50%」
  「Shor 分解 RSA-2048 需要數十億個閘 → 必須把錯誤率降到 ~10−10 以下」「靠改善硬體只能到 ~10−3–10−4 → 剩下的差距靠錯誤更正」。驗算：0.997^230 = 0.501。
- 第 48 頁「錯誤緩解：現在就能用的方法」表：「讀取誤差緩解｜量混淆矩陣，反推分佈（M3、TREX）｜低；只修讀取」「零雜訊外插（ZNE）｜故意放大雜訊（閘折疊、拉長脈衝），外插回雜訊 0｜shots 數倍；外插有偏差」
  「後選擇 / 對稱性檢查｜丟掉違反守恆量的結果｜丟棄部分資料」；結語「錯誤緩解改善的是期望值的估計，不保護量子資訊本身；成本隨規模指數上升 → 是通往錯誤更正之前的過渡工具」。
- 第 32 頁「shots 與統計誤差」：「σ(P̂) = √(P(1−P)/N)」（一千次一半一半約 ±1.6 個百分點）。
- 課綱寫 p47–48，內容確實在第 47、48 頁（python-pptx 讀出）。

## 學程動畫：animations/operation.html#circuit（js/operation/06_circuit.js）

- 說明：「最後的量測欄會跑 1000 shots，插圖顯示直方圖（青線 = 理想機率）；可加入雜訊比較真實硬體的結果。」
- 雜訊規則（sample()）：`const gates = C.cols.reduce((a, [ops]) => a + ops.filter((o) => o.g !== 'M').length, 0);`
  `const pg = noise ? 1 - Math.pow(0.99, gates) : 0, pr = noise ? 0.03 : 0;`；每個 shot `if (Math.random() < pg) k = Math.floor(Math.random() * K);`（均勻隨機），
  否則照理想機率抽；再 `for (let j = 0; j < m.length; j++) if (Math.random() < pr) k ^= 1 << j;`（每顆位元 3% 翻轉）。
- 開關：`ui.toggle('加入雜訊（每閘 1%、讀取 3%）', false, (v) => { noise = v; if (counts) sample(); });`（已有量測時立刻重抽）。按鈕列（Playwright 讀出）：
  「Bell 態 / GHZ 態（3 位元糾纏） / 干涉：H–Z–H / Deutsch–Jozsa（平衡函數） / Bernstein–Vazirani（秘密字串 101） / Grover 搜尋（2 位元，找 |11⟩） / 量子隱形傳態 / 量子傅立葉轉換（QFT，輸入 |110⟩） / ⏮ 重設 / 單步 ▶ / 播放 / 加入雜訊（每閘 1%、讀取 3%）」。
- GHZ：`[[H(0)], [CX(0, 1)], [CX(1, 2)], M([0, 1, 2])]` → 3 個閘、4 欄；Grover：`[H(0), H(1)]、[CZ]、[H, H]、[X, X]、[CZ]、[X, X]、[H, H]、M` → 12 個閘、8 欄。
- Playwright 截圖紀錄（scratchpad q126/shot_op.js）：GHZ 4 次單步後「1000 shots：000: 503，111: 497」；開雜訊後「000: 469，111: 427，110: 23（含雜訊）」，插圖兩根降到青線下、六根貼地小柱子；
  Grover 8 次單步，理想「11: 1000」；開雜訊三次重抽「11: 857／894／867」，01、10 各數十次（次數隨機，旁白不念）。

## 學程動畫：animations/basic-circuits.html#ghz（範例 4 重點卡）

- 「GHZ 電路的深度隨位元數增加，每多一顆就多一個 CNOT。硬體廠常用它來測試多位元糾纏的品質：雜訊越大，量到全 0、全 1 以外結果的比例就越高（這裡是理想模擬，所以不會出現）。」

## 學程動畫：animations/transmon-3d.html#bv（第 9 章 BV 密碼）

- 第 8 步「自由實驗」說明：「勾選「讀取雜訊」會加入每顆位元 3% 的讀取誤判。」；註解：「振幅由 8 維實數態向量逐閘計算（H、Z、黑盒子）；量測依 振幅² 隨機取樣。「讀取雜訊」為每顆位元 3% 的獨立誤判（示意值）。」
- 程式：`if (S.noisy) for (const bit of BIT9) if (Math.random() < 0.03) k ^= bit;`；`#g9run`「一鍵執行」：H⊗3 → 黑盒子 → H⊗3 → 量測 50 次（g9Reset 先清空）；`[data-op9="M"]`「④ 量測 50 次」累加。
- Playwright 截圖紀錄（scratchpad q126/shot_tr.js、shot_tr2.js）：五輪 50 次的錯誤結果只有 001、100、111；一鍵執行約 8.3 秒、④ 約 3.0 秒；累加 100 次「001 3、100 3、101 86、111 8」。

## 製作代理實跑紀錄

- page_noise.py（Python 3.13.18，只用標準函式庫，沒有亂數）輸出全文見 classroom.py 的 RUN_OUTPUT。
- noise_lab.py（qiskit 2.6.2、qiskit-aer 0.18.4，AerSimulator seed_simulator=126）輸出全文見 classroom.py 的 QISKIT_OUTPUT；雜訊模型.ipynb 的程式格接起來重跑，輸出逐字相同。
- 讀取 3% 下 50 次出現兩位元以上錯誤的機會：每次 3 × 0.03² × 0.97 + 0.03³ = 0.26%，50 次至少一次 ≈ 12.4%（所以旁白說「大多」）。
