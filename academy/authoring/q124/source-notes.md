# Q124 來源筆記（逐字引文）

查核日：2026-11-19（檔頭 CHECKED 依派工統一寫 2026-11-18）。維基百科頁面由製作代理直接讀取原始 wikitext（action=raw，2026-11-19）；MediaWiki API 當時回應限流，revision id 未取得。學程內部簡報（讀出實際頁碼、文字與備註）與動畫程式由製作代理讀取，畫面以 Playwright 單張截圖確認。程式由製作代理實際執行。

## Qiskit（Wikipedia，2026-11-19 raw wikitext）

- 「'''Qiskit''' (''Quantum Information Software Kit'') is an open-source, Python-based, high-performance software stack for quantum computing, originally developed by IBM Research and first released in 2017. It provides tools for creating quantum programs (by defining quantum circuits and operations) and executing them on quantum computers or classical simulators.」
- 「Key features of the Qiskit SDK include modules for building quantum circuits …, a quantum information module for working with quantum states and operators, and a transpiler …」
- 「The SDK also provides tools for noise modeling and supports primitives – basic quantum program components (such as samplers and estimators for circuit outcomes) – which serve as building blocks for higher-level quantum algorithms and can be executed using local simulators or cloud services.」
- 「'''Qiskit Aer''' (qiskit-aer) – A high-performance simulator for quantum circuits, featuring multiple simulation backends and support for realistic noise models. It is maintained by IBM Quantum as the official simulation engine for Qiskit and is frequently used to validate algorithms before running on actual quantum processors.」

## Project Jupyter（Wikipedia，2026-11-19 raw wikitext，Jupyter Notebook 一節）

- 「A Jupyter Notebook application is a browser-based REPL containing an ordered list of input/output cells which can contain code, text (using GitHub Flavored Markdown), mathematics, plots and rich media.」
- 「Jupyter Notebook can colloquially refer to two different concepts, either the user-facing application to edit code and text, or the underlying file format which is interoperable across many implementations.」
- 「Visual Studio Code supports local development of Jupyter notebooks.」

## 學程簡報：量子電路入門：八個範例（slides/output/basic-circuits.pptx）

- 第 28 頁「互動動畫：逐步播放、自己量測」：「右下可以量測 1 次或 1,000 次：灰底是理論機率、綠色是實際次數」。備註：「按一次只得到一個結果，按 1,000 次就能看到分布，灰色底是理論機率，綠色是實際次數。」
- 第 29 頁「互動動畫：Deutsch 與 BV」：「上方按鈕可以換黑盒（Deutsch 四種函數）或點選密碼位元（BV 共 8 種密碼）」「頁面底部附會隨選項改變的 Qiskit 程式碼，可以複製到自己的電腦執行」。
  備註：「頁面最下面還附了 Qiskit 程式碼，會跟著選項改變，可以複製到自己的電腦執行。」
- 課綱素材寫 p28–29，內容確實在第 28–29 頁。

## 學程簡報：如何操作量子電腦（slides/QC_Operation_Talk.pptx）

- 第 27 頁「實際操作：用 Qiskit 跑一個 Bell 態」：`qc = QuantumCircuit(2)`、`qc.h(0)`、`qc.cx(0, 1)`、`qc.measure_all()` … `counts = job.result()[0].data.meas.get_counts()`、`print(counts)   # 例：{'00': 497, '11': 489, '01': 8, '10': 6}`；
  「結果怎麼解讀：理想：00、11 各 50%／01、10 出現 = 雜訊（閘、讀取錯誤）／統計誤差 ±1.6%」。備註：「程式介面依版本會調整，實際使用時以官方文件為準。」（課綱頁碼 p27 正確）
- 第 28 頁「動態線路：中途量測與即時回饋」：「# Qiskit：量測 q0，若為 1 則對 q1 做 X … with qc.if_test((qc.clbits[0], 1)): qc.x(1)」；「量子隱形傳態：依 2 個結果做 X / Z 修正」。

## 學程動畫：animations/basic-circuits.html

- 頁首說明：「讀法和 Qiskit 相同：電路圖 q0 在最上面，但寫成位元字串時 q0 在最右邊」。
- 量測卡：「每次量測只會得到一個結果，狀態也就此塌縮。要重複很多次，才看得出機率分布。灰色底是理論機率，綠色是實際次數。」按鈕「量測 1 次」「量測 1,000 次」「清除」。
- 程式碼區塊：`<summary>Qiskit 程式碼（會隨上面的選項改變）</summary>`；「需要 pip install qiskit（Qiskit 1.x 或 2.x）。」按鈕「複製程式碼」。
- qiskitCode() 產生的固定行：`from qiskit import QuantumCircuit`、`from qiskit.primitives import StatevectorSampler`、`qc = QuantumCircuit(n, m)`、
  `counts = StatevectorSampler().run([qc], shots=1000).result()[0].data.c.get_counts()`、`print(counts)  # 位元字串的最右邊是 q0`；有 RY 時加 `from math import pi`。
- 隱形傳態註解：「# 真實硬體會先量測 q0、q1，再依結果做 X、Z（動態電路）；這裡用受控閘代替，結果相同」。
- Grover 擴散註解：「# 擴散：H、X、多控制 Z、X、H（這樣接會多一個整體負號，不影響機率）」；標記註解「# 標記：把答案變成全 1、多控制 Z 變號、再還原」。
- 頁尾：「所有振幅都由頁面內建的狀態向量模擬器即時計算，和 Qiskit 的 Statevector 結果一致（Grover 的擴散步驟照理想的『對平均值翻轉』計算；用 H、X、多控制 Z 組成的實際電路會多一個整體負號，機率完全相同）。」
- 引擎 applyOp：「擴散 = 2|s⟩⟨s| − I：每個振幅對平均值翻轉。用 H、X、CZ 組成的電路會多一個整體負號（量不到），這裡照理想算」。
- 選項（SCENES.opts）：疊加「起始態」2 種；干涉「中間的閘」2 種；Bell「目標 Bell 態」4 種；GHZ「位元數」2 種；隱形傳態「要傳的狀態 ψ」4 種；Deutsch「黑盒裡的函數」4 種；
  BV「密碼 s」3 位元 8 種；Grover「位元數」2 種 ×（2 顆答案 4 種／3 顆答案 8 種）×「重複輪數」最佳／1／2／3 共 48 種；合計 74。
- README.md：「頁內模擬器的 74 種選項組合都已和 Qiskit Statevector 比對過，結果一致（Grover 的擴散照理想『對平均值翻轉』計算，和 H、X、多控制 Z 組成的電路只差一個整體負號）」。

## 製作代理實跑紀錄

- Node 22 執行 basic-circuits.html 的 `<script id="engine">`：列出 74 種組合（8 種是預設），每種記下 marginal 機率、最終振幅與 qiskitCode() 產生的程式。
- Qiskit 2.6.2（Python 3.13.18）：74 個程式逐一執行（去掉 print 與 counts 兩行），`Statevector(qc.remove_final_measurements())` 對量測位元求機率，與頁面比：74／74 一致，最大差 3.0e-15。
  比整個振幅向量：46 種相同、28 種為 −1 倍；28 種全是 Grover 奇數輪（1 輪 16 種〔含 2 顆「最佳」〕、3 輪 12 種……依「・擴散」出現次數計），偶數輪 20 種相同。
- eight_examples.py（qiskit 2.6.2、qiskit-aer 0.18.4）與 check_eight.py（純 Python）輸出原文見 classroom.py 的 QISKIT_OUTPUT、RUN_OUTPUT；八範例.ipynb 的程式格依序執行，輸出與 eight_examples.py 逐字相同；nbformat 5 驗證通過。
- Playwright（1600×900，nice -n 19）截圖：#grover 程式碼（2 顆、3 顆）、頁尾；#bv 改成 110 後量測 1,000 次「110 1000（100.0%）」「→ 密碼 s = 110」與程式碼 `qc.cx(1, 3)`、`qc.cx(2, 3)`；#teleport 程式碼（預設與 |+⟩）。
