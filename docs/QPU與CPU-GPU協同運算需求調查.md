# QPU 與 CPU／GPU 協同運算：哪些量子工作需要大量古典算力？

> 調查日期：2026-11-20
> 問題：未來資料中心會同時擺 CPU、GPU、QPU。哪些 QPU 的運算工作，需要大量 CPU + GPU 介入配合？（例如控制 RF？或像 Shor 這類計算流程？）
> 寫法：先給結論與總表，再分九大類逐項說明「古典端在做什麼、為什麼重、需要多快、用什麼硬體」，每類附實際案例。最後一節專門拆解 Shor。
> 註記：文中數字凡標「廠商宣稱」者，為公司新聞稿或部落格，尚無獨立驗證；標「粗估」者為本文依公開參數自行估算，用來抓量級。

---

## 0. 一句話結論

**QPU 從來不是獨立運作的機器，它是一顆「被古典電腦包圍的協處理器」。** 古典算力介入的地方可以依「要多快回應」分成五層：

| 時間尺度 | 典型工作 | 主要古典硬體 |
|---|---|---|
| 奈秒（ns） | 產生 RF／微波脈衝、ADC 取樣、解調、判斷 0/1 | FPGA、RFSoC、ASIC（緊貼 QPU） |
| 微秒（µs） | **即時錯誤更正解碼**、中途量測後的條件回饋（feed-forward）、中性原子重排 | FPGA／ASIC 為主，GPU 透過低延遲互連（如 NVQLink）開始加入 |
| 毫秒～秒（ms–s） | 校準、漂移追蹤、離子阱／原子陣列的路徑與波形計算、變分演算法每一輪的參數更新 | GPU 伺服器（Grace Hopper 等）、CPU |
| 分鐘～小時 | 誤差緩解後處理、SQD 對角化、QC-AFQMC 後處理、電路切割重組、解碼器訓練 | GPU 叢集、超級電腦 |
| 天～月（離線） | 編譯大型演算法、化學哈密頓量前處理、資源估算、晶片電磁模擬、驗證量子結果 | 超級電腦、雲端 HPC |

**最重要的反直覺結論**：以 Shor 為例，大家以為「前處理（選 a、gcd）」和「後處理（連分數）」很重，其實這兩段在筆電上就能算完；**真正吃掉大量古典算力的，是 QPU 跑的那幾天裡，每一微秒都不能停的錯誤更正解碼**（第 7 節詳算：百萬位元的機器，解碼器要持續吞下約 0.5 Tb/s 的症狀資料）。換句話說，**容錯量子電腦時代，GPU／FPGA 最大的工作不是「幫忙算題目」，而是「讓 QPU 活著」。**

---

## 1. 總覽表：所有需要大量 CPU／GPU 介入的 QPU 工作

| # | 類別 | 古典端在做什麼 | 延遲要求 | 運算量來源 | 代表案例 |
|---|---|---|---|---|---|
| 1 | RF 脈衝產生與讀取訊號處理 | 波形合成、解調、0/1 判別（含神經網路判別） | ns | 每條讀取線 GS/s 等級原始資料 | RFSoC 上 5 顆位元 NN 判別 < 50 ns |
| 2 | 校準與漂移追蹤 | 數百～數萬個參數的閉迴路最佳化、強化學習 | ms–min | 參數維度 × 量測次數 | Quantum Machines + NVIDIA DGX Quantum：CZ 閘 25 秒校準完成（廠商宣稱） |
| 3 | 脈衝最佳控制 | GRAPE、自動微分模擬多能階系統 | 離線～分鐘 | 矩陣指數、梯度 | Schuster lab GPU 自動微分最佳控制 |
| 4 | 中性原子陣列重排 | 拍照 → 找原子 → 指派問題 → 算全像圖／AOD 頻率 | ms | 影像處理 + 匈牙利演算法 + FFT | GPU 每張全像圖 0.284 ms；萬顆原子重排 < 60 ms |
| 5 | 離子阱 shuttling | 移動排程、電極電壓波形 | ms | 組合最佳化 + 電位求解 | TUM QCCD 編譯器 |
| 6 | **即時量子錯誤更正（QEC）解碼** | 從症狀推出錯誤、追蹤 Pauli frame、決定修正 | **µs（超導）～ms（離子）** | 每 µs 數十萬 bit 症狀 | Google Willow 63 µs；Quantinuum Helios + GH200 BP+OSD 67 µs；IBM Relay-BP FPGA |
| 7 | 邏輯層排程 | lattice surgery 排程、魔術態工廠調度 | µs–ms | 動態排程 | Gidney 2025 RSA 估算假設 10 µs 反應時間 |
| 8 | 編譯 | 分解、映射、路由、Clifford+T 合成、可逆算術電路合成 | 離線 | 兆級閘數 | 2048-bit RSA 需數十億～兆級 Toffoli |
| 9 | 化學前處理 | HF、積分、活性空間、DF/THC 張量分解、DMRG 初始態 | 離線 | O(N⁴)～O(N⁵) 張量 | FeMoCo THC 資源估算 |
| 10 | AI 生成電路 | Transformer 產生量子電路 | 小時 | 模型訓練 | NVIDIA GQE：173 h → 48 顆 H100 3.5 h |
| 11 | 變分演算法迴圈 | VQE/QAOA 的最佳化器、梯度 | s/輪 | 迭代次數 × 電路數 | Qiskit Runtime Session |
| 12 | **樣本式量子對角化（SQD）** | 量子抽樣 → 古典組態回復 → 超大矩陣對角化 | 分鐘～小時 | 子空間維度 | IBM Heron + RIKEN 富岳（158,976 節點全機） |
| 13 | QC-AFQMC | 古典 Monte Carlo 搭配量子試探波函數 | 小時 | 陰影（shadow）重建 | IonQ + AWS + NVIDIA + AstraZeneca：後處理 656× 加速 |
| 14 | 量子退火混合求解 | 古典啟發式 + 問題分解 + QPU 子問題 | s | 問題規模 | D-Wave Leap Hybrid |
| 15 | 電路切割／縫合 | 子電路結果的古典重組 | 小時 | 隨切割數指數成長 | CutQC、Qiskit addon |
| 16 | 誤差緩解 | ZNE、PEC、twirling、張量網路誤差緩解 | 分鐘～小時 | 取樣與張量收縮 | IBM 2023 Nature 127 位元；Algorithmiq TEM |
| 17 | 驗證與基準 | 用超級電腦模擬量子電路、比對 XEB | 天 | 指數級模擬 | 認證隨機數：Frontier + Summit + Polaris + Perlmutter |
| 18 | 硬體設計 | 晶片電磁模擬、Hamiltonian 擷取 | 離線 | 十億級自由度有限元 | AWS Palace：14 億自由度、12,800 核心 |
| 19 | 資料中心編排 | Slurm 排程 QPU、混合工作流、低延遲互連 | — | 系統整合 | NVQLink、DGX Quantum、EuroHPC、IBM × AMD |

以下逐類說明。

---

## 2. 第一類：控制層——RF、讀取、校準（貼著 QPU 的古典電子）

這層回答了「控制 RF 要不要 CPU／GPU？」的問題。答案是：**RF 本身由 FPGA／DAC 即時產生，CPU／GPU 不直接吐 RF，但它們負責「決定 RF 長什麼樣子」**——波形設計、校準參數、編譯排程都在 CPU／GPU 上完成，再下載到 FPGA。

### 2.1 RF／微波脈衝產生

- **在做什麼**：每顆超導位元需要 XY 驅動（4–8 GHz 微波，幾十 ns 的 DRAG 脈衝）、Z 磁通偏壓（調頻、做 CZ）、讀取音調。離子阱需要雷射的 AOM/AOD 射頻音調；中性原子需要 AOD 多音 RF 與 SLM 全像圖。
- **誰負責**：任意波形產生器（AWG）、RFSoC（如 AMD/Xilinx ZCU111、ZCU216）把波形以 GS/s 速率送出。這是 FPGA 的工作，延遲在 ns。
- **CPU／GPU 的角色**：
  - 把電路編譯成「脈衝時間表」（pulse schedule），計算每個脈衝的振幅、頻率、相位、虛擬 Z 旋轉的相位累加。
  - 支援動態電路（mid-circuit measurement + 條件分支）時，控制器要能依量測結果即時切換波形；複雜的分支邏輯（例如 Shor 的半古典 QFT、魔術態注入的條件修正）就會牽涉到上層解碼器的回饋。
- **規模化後的壓力**：1,000 顆位元時，每顆約 2–3 條控制線，總共數千條 RF 通道；波形記憶體、同步時脈（見本 repo [`docs/周邊系統連接與啟動指南.md`](周邊系統連接與啟動指南.md)）都是古典電子的負擔。

### 2.2 讀取訊號處理

- **在做什麼**：讀取諧振腔的反射訊號經 HEMT、室溫放大、下變頻後被 ADC 取樣，接著要做：數位解調 → 積分 → 在 IQ 平面判斷 0/1（甚至 |2⟩ 洩漏）。細節見 [`notes/dispersive-readout.md`](../notes/dispersive-readout.md)。
- **為什麼重**（粗估）：假設每條讀取線 1 GS/s × 12 bit ≈ 12 Gb/s，每條線多工 8 顆位元。百萬位元的機器有約 12.5 萬條讀取線，原始資料總量 ≈ 1.5 Pb/s。**這麼大的資料量不可能送去 GPU**，所以解調與判別一定要在 ADC 旁邊的 FPGA／ASIC 內完成，往上只送「0/1 位元」。
- **進階：神經網路判別**。多工讀取會互相串擾，傳統的「每顆位元一個匹配濾波器 + 直線切分」不夠好：
  - **案例**：Lienhard 等人用全連接神經網路判別 5 顆頻率多工的超導位元，指派錯誤率最多降 25%，讀取串擾降一個數量級，而且位元越多優勢越大（[arXiv:2102.12481](https://arxiv.org/pdf/2102.12481)）。
  - **案例**：Gautam 等人把神經網路判別器做進 RFSoC ZCU111 FPGA，5 顆位元多工讀取 < 50 ns（[arXiv:2407.03852](https://arxiv.org/abs/2407.03852v2)）；LUNA 進一步用查表式神經網路省 FPGA 資源（[arXiv:2512.07808](https://arxiv.org/pdf/2512.07808)）。
  - **GPU 的角色**：推論在 FPGA 上，但**模型訓練、定期重訓（因為讀取腔頻率會漂移）在 GPU 上**。
- **中性原子／離子的「讀取」是影像**：EMCCD／sCMOS 相機拍螢光照片，要即時判斷每個格點有沒有原子、亮或暗。陣列上萬顆時，每張影像的處理（去背、分割、分類）就是 GPU 擅長的影像運算。

### 2.3 校準與漂移追蹤

- **在做什麼**：每顆位元要校頻率、π 脈衝振幅、DRAG 係數、讀取頻率與功率、判別門檻；每對位元要校 CZ 的磁通脈衝、相位修正；還要掃頻率碰撞、TLS 缺陷。參數會隨溫度、TLS、1/f 雜訊漂移，所以要**持續在背景重新校準**。本 repo 的 [`animations/transmon-3d.html`](../animations/transmon-3d.html) 第 12 章「校準依賴圖」示範了這種有向圖。
- **為什麼重**：參數數量 ≈ (每顆位元 ~10 個 + 每對 ~10 個) × 位元數；百萬位元就是千萬級參數，而且彼此耦合（頻率擁擠）。傳統人工或依賴圖逐步掃描已跟不上，轉向**貝氏最佳化、強化學習（RL）、數位孿生（digital twin）模擬**——都是 GPU 工作。
- **案例**：
  - **Quantum Machines + NVIDIA DGX Quantum**：OPX1000 控制器透過 PCIe 等級連線接 GH200 Grace Hopper 伺服器，往返延遲 < 4 µs。與中研院的示範中，RL 代理人約 25 秒把 CZ 閘調好，人工約需 15 分鐘（廠商宣稱，[Quantum Machines](https://quantum-machines.co/products/nvidia-dgx-quantum)、[RL 兩位元閘校準](https://www.quantum-machines.co/resources/blog/reinforcement-learning-two-qubit-gate-calibration/)）。
  - **Rigetti × Quantum Machines「AI 校準挑戰」**：Quantum Elements 與 Qruise 在同一套堆疊上校準 9 位元 Rigetti Novera，Quantum Elements 回報單位元 99.9%、雙位元 98.5% 保真度（[The Quantum Insider](https://thequantuminsider.com/2024/12/10/ai-driven-quantum-calibration-achieved-in-rigetti-and-quantum-machines-challenge/)）。
  - **以色列量子計算中心（IQCC）**：在 Grace Hopper 上跑 RL 代理人，宣稱單、雙位元閘校準速度創紀錄（同上 Quantum Machines 頁面）。
  - **Riverlane + NVIDIA**：連「解碼器本身的校準」（估計每個錯誤機制的權重）都搬到 GPU，H100 在重複碼上每秒處理約 1.55 億個症狀，比單核 CPU 快 121 倍；表面碼從每秒約 5.9 萬提升到 420 萬以上（71 倍）（[Quantum Computing Report](https://quantumcomputingreport.com/riverlane-and-nvidia-demonstrate-accelerated-qec-decoder-calibration-using-gpu-processing/amp/)）。

### 2.4 脈衝最佳控制（Optimal Control）

- **在做什麼**：用 GRAPE、Krotov 等方法，在多能階 transmon（含 |2⟩ 洩漏）、耦合器、串擾模型下，數值求出最好的脈衝形狀。要反覆計算時間演化（矩陣指數）與梯度。
- **為什麼重**：希爾伯特空間隨位元數指數成長；兩顆 transmon 各取 3–4 能階加耦合器，就已經是數十維的密度矩陣在數百個時間步上反覆微分。
- **案例**：Leung 等人（Schuster lab）用 GPU 自動微分加速量子最佳控制（[Leung 2017](https://schusterlab.stanford.edu/static/pdfs/Leung2017.pdf)）；2025 年預印本對 15 位元階梯結構、2% 頻率無序的超導系統做 GRAPE（QuTiP + 自製張量網路）（[arXiv:2510.25996](https://arxiv.org/pdf/2510.25996)）；Q-CTRL Boulder Opal 是商用的控制最佳化工具（[Q-CTRL 應用說明](https://docs.q-ctrl.com/boulder-opal/application-notes/designing-error-detectable-entangling-gates-for-superconducting-resonators-in-dual-rail-encoding)）。

### 2.5 中性原子陣列重排（Rearrangement）——典型的「GPU 進入即時迴路」

- **流程**：光鑷隨機裝載（約 50% 機率有原子）→ 相機拍照 → 影像判斷哪些格點有原子 → **指派問題**（哪顆原子搬到哪個目標格點，用匈牙利演算法或啟發式）→ 規劃不碰撞的路徑 → **計算每一步的 SLM 全像圖或 AOD 多音頻率** → 搬移 → 再拍照確認 → 補洞。
- **為什麼重**：原子必須在真空壽命與加熱前完成；陣列從數百擴到上萬顆，指派問題是 O(N³)、全像圖是大尺寸 FFT 迭代（Gerchberg–Saxton）。
- **案例**：
  - 2017 年匈牙利演算法研究就用 GPU 即時算 SLM 遮罩（[arXiv:1704.07074](https://arxiv.org/pdf/1704.07074)）。
  - 中國科大等團隊用 AI 模型產生每一步全像圖，路徑匹配 + GPU 全像計算 + SLM 刷新的成本在 1,000～10,000 顆原子之間幾乎不變，萬顆原子重排估計 < 60 ms（[arXiv:2412.14647](https://arxiv.org/pdf/2412.14647)）。
  - 2026 年預印本：單顆 GPU 每張中間全像圖 0.284 ms，比 SLM 刷新 0.696 ms 還快，瓶頸變成 SLM 硬體；從 256 個隨機裝載點組出 100 顆無缺陷陣列 < 20 ms（[arXiv:2610.21609](https://arxiv.org/pdf/2610.21609)）。
  - 圖神經網路路徑規劃在 RTX 5090 上約 5 ms、幾乎不隨陣列大小增加（[arXiv:2604.08669](https://arxiv.org/pdf/2604.08669)）；AAAI 2026 用 Fourier U-Net 即時生成全像圖（[AAAI](https://ojs.aaai.org/index.php/AAAI/article/view/39967)）。
  - 另一條路是全部做進 FPGA：50×50 陣列處理延遲比 CPU 低約 54 倍（[arXiv:2411.12401](https://arxiv.org/pdf/2411.12401)）。
- **趨勢**：重排不只在開機時做一次。要做連續運轉（持續補原子）與中途量測後的重新配置，就變成**每個電路都要跑的即時 GPU 工作**。

### 2.6 離子阱 QCCD 的 shuttling 排程與電極波形

- **在做什麼**：QCCD 架構要把離子在儲存區、閘區、讀取區之間搬移、分離、合併、經過交叉路口（Quantinuum Helios 就有交叉結構）。古典端要：(1) 把電路轉成移動排程（組合最佳化，要最少搬移次數，因為每次搬移都會加熱與失相）；(2) 為每一步算出數十～數百個 DC 電極的電壓波形（求解靜電位能、避免激發運動態）。
- **案例**：TUM 團隊的 shuttling 編譯流程把電路轉成精確的移動時程，且必須針對特定元件佈局與起始離子配置（[arXiv:2402.14065](https://arxiv.org/pdf/2402.14065)）；Kreppel 等人基於 pytket 的編譯器（[Quantum 期刊](https://quantum-journal.org/papers/q-2023-11-08-1176/)）；考慮雜散電場與離子遺失的強健編譯（[TUM 2026](https://www.cda.cit.tum.de/files/eda/2026_qsw_robust_ion_shuttling.pdf)）。
- **時間尺度**：離子閘較慢（數十 µs～ms），所以 Helios 的錯誤更正反應時間窗是 2 ms（見 3.3），這反而讓 GPU 有機會直接進入即時迴路。

### 2.7 光子量子電腦的前饋（feed-forward）

- 光子在光纖或波導裡無法「停下來等」，融合式（fusion-based）架構每一次融合量測的結果都要在光子飛過延遲線之前決定下一步的量測基底，並餵給解碼器。這是**對延遲最嚴苛**的平台，古典處理量與 FPGA/ASIC 規模都非常大（本次搜尋未找到 PsiQuantum 公開的古典處理量數字，此處僅就架構原理說明）。

---

## 3. 第二類：即時量子錯誤更正（QEC）解碼——未來最大的古典負擔

### 3.1 為什麼一定要即時、為什麼量這麼大

- 表面碼每一個週期（超導約 1 µs）量一次所有輔助位元，得到「症狀」（syndrome）。解碼器要從症狀推斷發生了什麼錯誤。本 repo [`animations/transmon-3d.html`](../animations/transmon-3d.html) 第 10 章有完整互動示範（d = 3/5/7、最小權重完美匹配）。
- **只存不解可以嗎？** 對 Clifford 閘可以（記在 Pauli frame 裡，最後再修）；但遇到 **T 閘（魔術態注入）、量測後的條件分支**，就必須先知道目前累積的錯誤才能決定下一步。如果解碼速度跟不上症狀產生速度，未處理的資料會無限堆積——這就是 Terhal 提出的**積壓問題（backlog problem）**，計算會指數變慢。
- **資料量（粗估）**：百萬顆物理位元、約一半是輔助位元 → 每 1 µs 產生約 50 萬 bit → **約 0.5 Tb/s（≈ 62.5 GB/s）持續不斷**，而且要在數 µs～十數 µs 內給出答案。

### 3.2 解碼演算法與適合的硬體

| 解碼器 | 特性 | 適合硬體 |
|---|---|---|
| MWPM（最小權重完美匹配，如 PyMatching、Sparse Blossom） | 表面碼標準、精度高 | CPU、FPGA |
| Union-Find／Collision Clustering | 近線性時間、可平行 | FPGA、ASIC |
| BP + OSD（信念傳播 + 有序統計） | qLDPC 碼常用，OSD 是矩陣消去較重 | GPU |
| Relay-BP（IBM） | 只保留訊息傳遞，適合 FPGA | FPGA |
| 神經網路解碼器（AlphaQubit、Transformer、Mamba、GNN） | 精度最高，能學到真實雜訊（串擾、洩漏），但推論慢 | GPU／TPU 訓練；推論要加速 |
| 張量網路／最大似然 | 最精準、最慢，多用於基準 | GPU |

### 3.3 案例

1. **Google Willow（Nature 2024）**：距離 5 的表面碼搭配即時解碼器，週期 1.1 µs，平均解碼延遲 63 µs，連續一百萬個週期；距離 7 的記憶體實驗每週期錯誤率 0.143%（[Princeton 收錄](https://collaborate.princeton.edu/en/publications/quantum-error-correction-below-the-surface-code-threshold/)）。63 µs 約等於 50 多個週期，所以是「延遲有界」而非「每週期即時」。
2. **Riverlane Deltaflow 2**：用同一份 Willow d=5 資料，平均延遲降到 16.32 µs（[Quantum Computing Report](https://quantumcomputingreport.com/riverlane-demonstrates-real-time-qec-latency-performance-advancements/)）；Collision Clustering 解碼器在 FPGA 上 810 ns 解完 881 位元表面碼、在 ASIC 上 240 ns 解完 1,057 位元，都超過每秒百萬週期（[The Quantum Insider](https://thequantuminsider.com/2025/01/07/riverlane-reports-new-decoder-tech-sets-new-standard-in-quantum-error-correction/)）。
3. **Quantinuum Helios + NVIDIA GH200 + NVQLink（2025）**：用 CUDA-Q QEC 函式庫的 GPU 版 BP+OSD 解碼器，中位數解碼時間 67 µs，比 Helios 要求的 2 ms 快 32 倍；8 個邏輯位元做 3 輪錯誤更正後，錯誤率從 4.95% 降到 0.925%（約 5.4 倍改善）。Helios 以 GH200 作為即時主機（[Quantinuum](https://www.quantinuum.com/blog/real-time-error-correction-at-increased-scale)、[NVIDIA 技術部落格](https://developer.nvidia.com/blog/nvidia-nvqlink-architecture-integrates-accelerated-computing-with-quantum-processors)）。**這是 GPU 直接進入 QPU 即時迴路的第一個代表案例。**
4. **IBM Relay-BP on FPGA**：針對 [[144,12,12]] gross code（雙變數 bicycle qLDPC 碼），BP 每次迭代 24 ns，12 個週期的視窗平均 < 240 ns 解完，遠低於 1 µs 週期，可避免積壓；但光是 X 方向解碼就用掉 AMD VU19P（最大型商用 FPGA 之一）一半以上的邏輯資源（[arXiv:2510.21600](https://arxiv.org/pdf/2510.21600)、[Relay-BP 演算法 arXiv:2506.01779](https://arxiv.org/pdf/2506.01779)）。**這說明解碼器的硬體量會隨邏輯位元數一起長大。**
5. **Google DeepMind AlphaQubit（Nature 2024）**：Transformer 解碼器精度最好，但 Google 自己說它還太慢，無法即時更正超導處理器的錯誤（[Google 部落格](https://blog.google/technology/google-deepmind/alphaqubit-quantum-error-correction/)）；後續有 Mamba 狀態空間模型（[arXiv:2510.22724](https://arxiv.org/html/2510.22724v1)）與平行滑動視窗 Transformer（[arXiv:2509.03815](https://arxiv.org/html/2509.03815v1)）設法解決速度問題。
6. **QuEra + NVIDIA：魔術態蒸餾的 AI 解碼器**：QuEra 用 35 顆中性原子編成 5 個邏輯魔術態做 5-to-1 蒸餾；NVIDIA 用 CUDA-Q + PhysicsNeMo 訓練的 Transformer 解碼器勝過最大似然解碼器，推論 < 1 ms（MLE 需數十 ms）。**訓練距離 3 的模型就用了 42 顆 H100、1 小時**；更大碼距預期需要 Blackwell（[NVIDIA 技術部落格](https://developer.nvidia.com/blog/nvidia-and-quera-decode-quantum-errors-with-ai)）。
7. **NVIDIA Ising Decoder（2026）**：開源色碼 AI 解碼器，宣稱邏輯錯誤率最多降 347.7 倍、比開源 Chromobius 快 7.3 倍（DGX GB300 對 Grace CPU，廠商宣稱，[The Quantum Insider](https://thequantuminsider.com/2026/07/15/nvidia-says-ai-decoder-achieved-up-to-347-x-cut-in-quantum-logical-error-rates/)）。
8. **IQM + Zurich Instruments**：以 NVQLink 建立 20 位元超導即時 QEC 示範系統（[pulse.bot 報導](https://www.pulse.bot/quantum/news/iqm-and-zurich-instruments-launch-real-time-quantum-error-correction-demonstrator-with-nvidia-nvqlin-09ab77f1-b5aa-4f36-aca3-dc7e4a76fb19/)）。

### 3.4 解碼器以外的 QEC 古典工作

- **解碼器訓練與重訓**：神經網路解碼器要用真實症狀資料或大量模擬資料訓練（見上 42 顆 H100 案例），硬體雜訊漂移後要重訓或微調。
- **解碼器參數校準**：估計每個錯誤機制的機率作為匹配圖權重（Riverlane + NVIDIA GPU 加速，見 2.3）。
- **大量蒙地卡羅模擬**：設計新碼、評估閾值、驗證解碼器，需要數十億次 Stim 等工具的取樣。NVIDIA 宣稱其 TCBP-JOBS 演算法讓 QEC 解碼研究加速最多 13,000 倍（[Interesting Engineering](https://interestingengineering.com/science/nvidia-quantum-error-correction-decoding-breakthrough)）。
- **洩漏偵測與處理**：transmon 跳到 |2⟩、中性原子遺失，要從症狀模式判斷並觸發 reset 或補原子。

### 3.5 邏輯層：lattice surgery 排程與魔術態工廠調度

- 容錯計算的邏輯閘是用 lattice surgery 合併／拆開補丁完成（本 repo 第 11 章動畫），T 閘要從魔術態工廠取貨。古典控制器要即時決定：哪個工廠的魔術態好了、走哪條路由通道、下一個 T 閘的修正是 S 還是不用修（取決於解碼結果）。
- Gidney 2025 的 RSA 資源估算明確假設**控制反應時間 10 µs**、表面碼週期 1 µs（[arXiv:2505.15917](https://arxiv.org/abs/2505.15917)）。反應時間越長，整個演算法就越慢——**古典解碼與排程的延遲，直接決定量子演算法的總執行時間。**

---

## 4. 第三類：編譯與前處理（QPU 開跑之前）

### 4.1 量子電路編譯

- **在做什麼**：把高階演算法分解成原生閘（如 Rz、√X、CZ）、映射到實體佈局（考慮校準品質）、插入 SWAP 路由、閘合併與抵消、排程、轉成脈衝。容錯時代還要做 Clifford+T 合成（任意角度旋轉要拆成數十～上百個 T 閘）、lattice surgery 佈局。本 repo [`animations/transmon-3d.html`](../animations/transmon-3d.html) 第 12 章示範了這整條流程。
- **為什麼重**：路由是 NP-hard；容錯演算法的閘數動輒數十億到兆級。例如 Gidney 2025 提到 Chevignard–Fouque–Schrottenloher 法使用約 2 兆個 Toffoli 閘，經最佳化後才壓到可行範圍（[The Quantum Insider](https://thequantuminsider.com/2025/05/24/google-researcher-lowers-quantum-bar-to-crack-rsa-encryption/)）。要編譯、驗證、模擬這種規模的電路，本身就是 HPC 工作。
- **AI 編譯**：IBM 的 AI transpiler、強化學習路由、LLM 輔助的 shuttling 編譯器，都需要 GPU 訓練模型。

### 4.2 Oracle 與算術電路合成

- Grover 的 oracle、Shor 的模指數（modular exponentiation）都要把古典函數變成可逆量子電路。要做窗口化算術（windowed arithmetic）、近似餘數、量測式反計算等最佳化——是離線的大型合成與驗證工作。本 repo [`animations/shor-15.html`](../animations/shor-15.html) 用 N = 15 展示了「×7 = 循環移位 + 翻轉」這種手工合成，到 2048 位元就必須靠程式自動合成。

### 4.3 量子化學的古典前處理

- **流程**：分子幾何 → Hartree–Fock → 計算單、雙電子積分（O(N⁴) 個）→ 選活性空間（哪些軌域交給量子電腦）→ 張量分解（double factorization、tensor hypercontraction, THC）以降低量子閘數 → 準備初始態（如 DMRG 算出的矩陣乘積態）→ 才進入 QPE。
- **案例**：
  - THC 讓 FeMoCo 活性空間模型的 Toffoli 數低於 double factorization（[Lee 等人摘要](https://indico.physik.uni-muenchen.de/event/84/attachments/243/404/S1.Berry.abstract.pdf)、[arXiv:2011.03494](https://www.arxiv-vanity.com/papers/2011.03494/)）；2025 年的對稱位移 THC 變體針對細胞色素 P450（[arXiv:2501.06165](https://arxiv.org/pdf/2501.06165)）。THC 本身是一個非線性最小平方擬合，大分子要在 GPU／HPC 上算。
  - Quantum Motion + NVIDIA：用 GPU 加速的 DMRG 算出矩陣乘積態作為 QPE 的初始猜測，由 CUDA-Q 協調（[Quantum Computing Report](https://quantumcomputingreport.com/quantum-motion-and-nvidia-partner-to-resolve-state-preparation-obstacles-in-quantum-chemistry/amp/)）。
- **重點**：QPE 的成功機率取決於初始態與真實基態的重疊，所以「古典先算得越好，量子跑得越少」——古典化學算力是量子化學的前提，不是被取代的對象。

### 4.4 AI 生成量子電路（GQE）

- **案例：NVIDIA Generative Quantum Eigensolver**：用 Transformer 把量子閘當成「字詞」來生成電路，再依能量評分回頭訓練模型。原始研究中 30 位元 CO₂ 實驗在單顆 H100 要 173 小時，用 48 顆 H100 平行化縮到 3.5 小時；已收錄在 CUDA-QX 0.4（[NVIDIA 技術部落格](https://developer.nvidia.com/blog/advancing-quantum-algorithm-design-with-gpt)、[CUDA-QX GQE API](https://nvidia.github.io/cudaqx/api/solvers/gqe_api.html)）。

---

## 5. 第四類：混合演算法迴圈（近期最常見的協同模式）

### 5.1 VQE／QAOA：古典最佳化器 ↔ QPU 的往返

- **流程**：古典端給一組參數 → QPU 跑參數化電路、量測數千 shots → 古典端算期望值與梯度（參數平移法每個參數要多跑 2 個電路）→ 更新參數 → 重複數百～數千輪。
- **古典負擔**：單輪不重，但往返延遲很關鍵（雲端排隊會讓一輪從秒變成分鐘），所以 IBM 推出 Qiskit Runtime Session、各家推「QPU 旁邊就放 CPU/GPU」的架構。大規模 QAOA 還會用古典預處理把問題切小（分而治之）。

### 5.2 樣本式量子對角化（SQD）——「超級電腦 + QPU」的旗艦案例

- **流程**：QPU 對分子的電子組態抽樣（產生一堆位元串）→ 古典端做「組態回復」（修正雜訊造成粒子數不守恆的樣本）→ 用這些組態張成子空間 → **在超級電腦上把子空間中的哈密頓量對角化**（矩陣維度可達數億到數十億）→ 迭代。
- **案例**：
  - 原始 SQD 論文（Robledo-Moreno 等，Science Advances 2025）把它定義為「以量子為中心的超級運算」架構，處理了 N₂ 與鐵硫簇（[arXiv:2405.05068](https://arxiv.org/html/2405.05068v3)）。
  - **IBM + RIKEN（2026 年 1 月）**：富岳超級電腦全機（158,976 個節點、超過 760 萬核心）與 IBM Heron 閉迴路連續協同，計算 [Fe₂S₂(SH)₄]²⁻，宣稱是量子電腦上規模最大、最準的化學計算，精度可與最先進的古典近似方法相比；下一步要把 GPU 加入加速（IBM 宣稱，[IBM 部落格](https://www.ibm.com/quantum/blog/riken-fugaku-qcsc)、[Quantum Computing Report](https://quantumcomputingreport.com/riken-and-ibm-demonstrate-quantum-centric-supercomputing-at-scale/)）。
- **重點**：這個案例中**古典端的算力遠大於量子端**——QPU 的角色是「挑出值得算的組態」，真正的對角化是整台超級電腦在做。

### 5.3 量子–古典輔助場量子蒙地卡羅（QC-AFQMC）

- **流程**：QPU 準備試探波函數，用「古典陰影（classical shadows，此處為 matchgate shadows）」量測；古典端用這些陰影在 AFQMC 的每一步計算重疊與局部能量——這一步的後處理非常重。
- **案例：IonQ + AWS + NVIDIA + AstraZeneca**：用 IonQ Forte 24 顆位元（16 顆試探態 + 8 顆輔助誤差緩解）模擬鎳催化 Suzuki–Miyaura 反應的氧化加成步驟；以 CUDA-Q + AWS ParallelCluster 的 GPU 做後處理，量測收集加速 9 倍、分散式平行後處理的解題時間比先前最佳實作快 656 倍；理想模擬下落在 CCSD(T) 參考值 ±4 kcal/mol 內，真機量測在 10 kcal/mol 內（[arXiv:2506.22408](https://arxiv.org/abs/2506.22408)、[Physical Review Research](https://journals.aps.org/prresearch/abstract/10.1103/n1tf-8kr7)、[IonQ 部落格](https://ionq.com/blog/ecosystem-innovation-ionqs-life-sciences-application-workflow-accelerates)）。
- 這條路線最早來自 Google 的 Huggins 等人（Nature 2022），當時古典後處理就已經是整個流程的瓶頸。

### 5.4 量子退火的混合求解器

- **案例：D-Wave Leap Hybrid Solver Service**：所有混合求解器都是「古典前端 + 量子後端」。古典啟發式模組探索解空間、找出問題中最難的核心、切成小問題送進 QPU，再用 QPU 回傳結果引導古典搜尋；可處理遠大於 QPU 位元數的問題（[D-Wave 白皮書](https://www.dwavequantum.com/media/4bnpi53x/14-1039a-b_d-wave_hybrid_solver_service_an_overview.pdf)、[D-Wave 文件](https://docs.dwavesys.com/docs/latest/handbook_hybrid.html)）。實際上大部分運算時間花在古典端。

### 5.5 電路切割與縫合（Circuit Cutting／Knitting）

- **在做什麼**：把太大的電路切成小塊，分別在小 QPU（或多台 QPU）上跑，再由古典端把結果「縫回去」。
- **為什麼重**：每切一刀，取樣次數與重組運算量都乘上一個常數，**總成本隨切割數指數成長**。
- **案例**：Argonne 的 CutQC 被 IBM Circuit Knitting Toolbox 採用（[Argonne](https://www.anl.gov/mcs/article/at-the-cutting-edge-of-quantum-computing)）；IBM 在 SC23 展示把 28 位元 GHZ 電路切開跑在 27 位元 Hanoi 上（[SC23 海報](https://sc23.supercomputing.org/proceedings/tech_poster/poster_files/rpost131s3-file3.pdf)）；GPU 伺服器上的硬體感知切割框架（[arXiv:2409.03870](https://www.arxiv.org/pdf/2409.03870)）；2026 年以糾纏導向分割 + GPU 平行重組，宣稱取樣開銷降低最多四個數量級（[arXiv:2603.12411](https://arxiv.org/html/2603.12411v1)）。
- **延伸：分散式量子計算**：多台 QPU 用光子互連（本 repo [`animations/atoms.html`](../animations/atoms.html) 場景 9）共享糾纏時，糾纏產生的排程、糾纏純化、跨機的條件回饋，也是古典網路與控制的工作。

---

## 6. 第五類：誤差緩解（Error Mitigation）與量測後處理

在完全容錯之前，「用古典算力換精度」是主流手段：

| 方法 | 古典端在做什麼 | 成本特性 |
|---|---|---|
| Pauli twirling／隨機編譯 | 產生成百上千個等效但隨機化的電路變體 | 編譯量 × 變體數 |
| 零雜訊外插（ZNE） | 把雜訊放大成數個等級分別量測，再外插回零雜訊 | 取樣數 × 雜訊等級數 |
| 機率誤差消除（PEC） | 先學雜訊模型（稀疏 Pauli–Lindblad），再用準機率取樣抵消 | 取樣數隨電路大小**指數**成長 |
| 張量網路誤差緩解（TEM） | 在後處理中用張量網路把雜訊「反過來」作用 | 張量收縮成本由 bond dimension 決定 |
| 古典陰影（classical shadows） | 隨機量測後，古典重建大量可觀測量 | 重建與估計運算 |
| 讀取誤差緩解 | 求解或近似反轉讀取混淆矩陣 | 位元數大時要用張量積或稀疏近似 |

- **案例：IBM「量子效用」實驗（Nature 2023）**：127 位元 Eagle、最多 60 層、2,880 個 CNOT 的 2D 橫場 Ising 模型，用 ZNE（雜訊增益 1、1.2、1.6）；為了驗證結果，研究者用 MPS、isoTNS 等張量網路方法比對，在強糾纏區域古典近似方法反而不可靠（[Nature](https://www.nature.com/articles/s41586-023-06096-3.pdf)）。這篇之後引發一波「古典能不能追上」的 GPU／張量網路模擬競賽——**量子實驗本身就刺激了大量古典算力的投入。**
- **案例：Algorithmiq TEM（IBM Qiskit Function）**：把誤差緩解完全移到古典後處理，不需要額外的量子電路；成本集中在取得資訊完備的量測資料、學雜訊模型、以及張量網路收縮（[IBM 文件](https://quantum.cloud.ibm.com/docs/guides/algorithmiq-tem)、[Algorithmiq](https://algorithmiq.fi/news/tem-tensor-network-error-mitigation/)）。

---

## 7. 第六類（專題）：Shor 演算法，古典算力到底花在哪？

把 Shor 拆成「前、中、後」三段來看，答案會出乎意料。

### 7.1 前處理（輕）

1. 檢查 N 是否為偶數、質數冪（多項式時間，筆電即可）。
2. 隨機選 a，算 gcd(a, N)（歐幾里得演算法，微秒級）。
3. **編譯模指數電路（重，但只做一次）**：把 a^x mod N 合成為可逆電路——窗口化算術、Ekerå–Håstad 變體、近似餘數等技巧，最後要變成數十億個 Toffoli、配置魔術態工廠、規劃 lattice surgery 佈局。這是離線 HPC 工作，可預先做好、重複使用。
4. 資源估算（例如 Azure Quantum Resource Estimator、Gidney 的估算工具）。

### 7.2 量子執行期間（極重，而且是即時的）

以 Gidney 2025 的估算為準：**少於 100 萬顆雜訊物理位元、不到一週分解 2048-bit RSA**，假設 0.1% 閘錯誤率、1 µs 表面碼週期、10 µs 控制反應時間（[arXiv:2505.15917](https://arxiv.org/abs/2505.15917)）。古典端在這一週裡要：

- **持續解碼**（粗估）：約 50 萬顆輔助位元 × 每 µs 一次 → 約 0.5 Tb/s。一週約 6×10¹¹ 個週期，**累計要即時處理約 37 PB 的症狀資料**，而且任何一刻跟不上就會積壓。
- **每一個 T 閘的條件修正**：要在 10 µs 反應時間內完成「解碼 → 決定是否補 S 閘」。數十億個 Toffoli 對應數百億個 T 閘量級的條件判斷。
- **魔術態工廠調度**：Gidney 2025 使用魔術態培育（cultivation），會依解碼結果丟棄失敗的嘗試、重新排程。
- **邏輯位元記憶體管理**：用 yoked surface code 儲存邏輯位元，需要額外的外層解碼。
- **持續校準**：一週內硬體一定會漂移，背景校準不能停（而且不能干擾計算）。

**結論**：Shor 在執行期間的古典負擔，就是第 3 節所有 QEC 工作的總和，放大到百萬位元、持續一週。這是 FPGA／ASIC 解碼陣列 + GPU 視窗解碼 + CPU 排程的大規模系統工程。

### 7.3 後處理（輕～中）

- **原版 Shor**：量測結果 → 連分數展開 → 得到週期 r → gcd(a^(r/2) ± 1, N)。在筆電上毫秒級（本 repo [`animations/shor-15.html`](../animations/shor-15.html) 第 7 段有逐步範例）。失敗（r 是奇數等）就重跑。
- **Ekerå–Håstad／短離散對數變體**：後處理改用格（lattice）的方法，計算量增加但仍可在一般電腦完成，換得量子電路變短。
- **Regev 演算法（2023）**：量子電路跑約 √n 次，後處理改用**格基約化（LLL 類演算法）**，在多項式時間內完成；若進一步縮短電路，後處理可能變成需要解困難格問題、指數時間（[arXiv:2308.06572](https://arxiv.org/pdf/2308.06572.pdf)）。Ragavan–Vaikuntanathan 的改良用格約化來偵測並剔除錯誤樣本（[arXiv:2310.00899](https://arxiv.org/html/2310.00899v5)）；Ekerå–Gärtner 把它延伸到離散對數，且容許部分執行失敗（[IACR ePrint 2023/1501](https://eprint.iacr.org/2023/1501.pdf)）。**這是「用古典後處理換量子資源」的典型取捨。**

### 7.4 Grover 與其他演算法的對照

- **Grover**：前處理是 oracle 合成（把判斷條件寫成可逆電路，見本 repo SAT 規則版 oracle）；執行期同樣是 QEC 主導；後處理只是驗證答案（很輕）。由於 Grover 只有平方加速，而 QEC 與古典控制的常數開銷很大，**實務上能贏過 GPU 暴力搜尋的範圍非常窄**——這也是古典算力需求反過來決定量子演算法是否划算的例子。
- **HHL／量子線性系統**：資料載入（狀態準備）與讀出（要估計整個解向量就要指數次量測）是古典瓶頸，常把速度優勢吃掉。
- **量子機器學習**：資料編碼、核矩陣計算、古典陰影後處理都由 GPU 負責。

---

## 8. 第七類：驗證、基準與模擬——用超級電腦檢查量子電腦

量子電腦宣稱「古典做不到」時，就需要最強的古典電腦來證明它、或在小規模上驗證它。

- **案例：認證隨機數（Quantinuum + JPMorganChase，Nature 2025）**：56 位元 H2 離子阱當作「不受信任的伺服器」執行隨機電路；用交叉熵基準（XEB）驗證回傳的樣本。**驗證動用了 Frontier、Summit（ORNL）、Polaris（Argonne）、Perlmutter（NERSC）四台超級電腦**，最後認證 71,313 bits 的熵（[ORNL](https://www.olcf.ornl.gov/2025/05/05/quantum-computing-experiment-realizes-verifiably-random-number/)、[JPMorganChase](https://www.jpmorganchase.com/about/technology/blog/certified-randomness)）。在這個應用中，**古典驗證算力是產品本身的一部分**。
- **案例：Google Quantum Echoes（OTOC，Nature 2025）**：Willow 上 65 顆位元量 OTOC(2)，每組資料約 2.1 小時（含校準與讀取）；估計 Frontier 要連續跑約 3.2 年。40 顆位元的較小實例在高階 GPU 上要花數天才能重現（[The Quantum Insider](https://thequantuminsider.com/2025/10/22/google-quantum-ai-shows-13000x-speedup-over-worlds-fastest-supercomputer-in-physics-simulation/)、[Quantum Computing Report](https://quantumcomputingreport.com/google-quantum-ai-achieves-verifiable-quantum-advantage-on-willow-chip-with-quantum-echoes-algorithm/)）。
- **其他基準工作**：隨機基準（RB）、閘集斷層掃描（GST）、層保真度、XEB——都要大量古典擬合與模擬。
- **數位孿生與除錯**：用 GPU 狀態向量／張量網路模擬器（如 cuQuantum、CUDA-Q）先在古典端跑一遍，驗證編譯正確、產生預期分布，是每個量子程式上線前的標準步驟。30–40 顆位元的狀態向量模擬就需要數百 GB～數十 TB 記憶體，屬於 GPU 叢集工作。

---

## 9. 第八類：量子硬體設計

- **晶片電磁模擬**：transmon、諧振腔、耦合器、封裝與佈線的電磁場模擬，用來萃取電容矩陣、耦合強度、Purcell 衰減，再轉成哈密頓量參數。
- **案例：AWS Palace**：開源有限元電磁求解器，AWS 量子中心用它做大型 3D 模擬；曾以 12,800 顆 Graviton2 核心跑到 14 億自由度的模型；transmon + 讀取諧振腔的粗／細模型約 1.5 分鐘／12 分鐘（[AWS 部落格](https://aws.amazon.com/blogs/quantum-computing/aws-releases-open-source-software-palace-for-cloud-based-electromagnetics-simulations-of-quantum-computing-hardware/)、[arXiv:2511.01220](https://arxiv.org/html/2511.01220v2)）。目前公開資料顯示以 CPU 為主。
- **其他**：約瑟夫森結參數與製程變異的統計模擬、TLS 缺陷模型、離子阱電極與雷射光路設計、中性原子光鑷與 SLM 光學設計——都是離線的 HPC 工作。

---

## 10. 第九類：資料中心層級的整合與編排

把 CPU、GPU、QPU 放在同一個資料中心，本身就有系統工作：

- **低延遲互連**：
  - **NVIDIA NVQLink**：FPGA → GPU → FPGA 最低延遲 < 4 µs、400 Gb/s，基於乙太網路 RDMA；整合 CUDA-Q，宣稱支援 17 家 QPU 廠商與 5 家控制系統廠商（[NVIDIA](https://www.nvidia.com/en-us/solutions/quantum-computing/nvqlink.md)、[Quantum Computing Report](https://quantumcomputingreport.com/nvidias-nvqlink-unites-quantum-ecosystem-for-real-time-error-correction/)）；多個國家級超算中心宣布採用（[NVIDIA 新聞稿](https://investor.nvidia.com/news/press-release-details/2025/Worlds-Leading-Scientific-Supercomputing-Centers-Adopt-NVIDIA-NVQLink-to-Integrate-Grace-Blackwell-Platform-With-Quantum-Processors/)）。
  - **DGX Quantum**（Quantum Machines OPX1000 + GH200）：見 2.3。
  - **Riverlane QECi**：主張 RoCE 介面在約 300 顆物理位元以上可能成為瓶頸，因此自訂協定（[postquantum.com](https://postquantum.com/engineering-news/altera-riverlane-qeci-agilex-fpga/)）。
- **IBM × AMD**：合作打造以量子為中心的超級運算架構，把 AMD 的 CPU、GPU、FPGA 與 IBM 量子電腦整合，目標是本十年末達到容錯（[Futurum](https://futurumgroup.com/insights/ibm-and-amd-join-forces-on-quantum-centric-supercomputing-initiative/)）。
- **工作排程**：把 QPU 註冊成 Slurm 的通用資源（GRES "QPU"），讓混合工作和一般 HPC 工作一起排程（[arXiv:2506.10052](https://arxiv.org/abs/2506.10052)）；EuroHPC 的 EuroQHPC-Integration 專案（2025–2029）要統一六個 HPC+QC 平台的使用體驗（[CSC](https://csc.fi/project/euroqhpc-i/)）；Alice & Bob 與 STFC Hartree 中心做貓態位元 QPU 的 Slurm 整合（[Hartree](https://www.hartree.stfc.ac.uk/news/2025/11/06/alice-bob-and-stfc-hartree-centre-integrate-cat-qubit-quantum-computers-into-standard-hpc-workflow-and-job-scheduling-software-slurm/)）；歐洲兩台 QPU 已透過 Slurm 等工作管理器整合進 HPC（[Qt.eu](https://qt.eu/news/2025/2025-11-18_inauguration_of_jade_and_ruby_quantum_processors)）。

---

## 11. 不同平台的「古典即時預算」比較

延遲預算決定了 GPU 能不能進入即時迴路：

| 平台 | QEC 週期／閘時間 | 即時反應時間窗 | GPU 能直接進即時迴路嗎？ |
|---|---|---|---|
| 超導（Google、IBM、IQM） | ~1 µs | ~10 µs（Gidney 2025 假設） | 內層必須 FPGA／ASIC；GPU 透過 < 4 µs 互連做視窗解碼、AI 解碼仍具挑戰 |
| 離子阱（Quantinuum） | 數十 µs～ms | ~2 ms（Helios） | **可以**，已有 GH200 + NVQLink 67 µs 案例 |
| 中性原子（QuEra、Atom Computing、Pasqal） | 閘 µs、讀取與重排 ms | ms | **可以**，重排與 AI 解碼 < 1 ms 已有案例 |
| 光子（PsiQuantum、Xanadu） | 光子飛行時間，ns | 極短 | 幾乎全靠 FPGA／ASIC |

---

## 12. 對資料中心規劃的啟示

1. **GPU 要放在 QPU 旁邊，不是放在雲端**：µs 級延遲意味著 GPU 機櫃要在稀釋冷凍機（或真空腔）幾公尺內，用專用互連，不能經過一般網路。
2. **古典算力的配比會很高**：以 IBM + RIKEN 為例，一台 QPU 配了整台富岳；以百萬位元 Shor 為例，即時解碼要持續處理 0.5 Tb/s。規劃時應該假設「一台 QPU ↔ 一整排 GPU／FPGA 機櫃」。
3. **分層設計**：ns 層 FPGA／RFSoC（貼著 QPU）→ µs 層 FPGA/ASIC 解碼 + GPU（同機房、專用互連）→ ms–s 層 GPU 伺服器（校準、重排、AI）→ 分鐘以上 HPC 叢集（SQD、誤差緩解、編譯、驗證）。
4. **電力與雜訊**：GPU 機櫃是數十 kW 等級的負載，且會產生電磁雜訊與地迴路，要和 QPU 的低雜訊電源、接地系統（見本 repo [`docs/1000量子位元系統供電設計.md`](1000量子位元系統供電設計.md)）一起設計。**「QPU 旁的 GPU 機櫃」本身就是量子等級電源的新應用場景**——它需要高功率、又要低傳導與輻射雜訊、還要與 QPU 共地或隔離。
5. **軟體堆疊整合**：CUDA-Q、Qiskit Runtime／Qiskit Functions、Slurm GRES 正在成為「CPU+GPU+QPU」的共同介面；選擇硬體時要看是否支援這些開放介面。

---

## 13. 延伸閱讀（本 repo 內）

- 表面碼與解碼：[`animations/transmon-3d.html`](../animations/transmon-3d.html) 第 10 章
- Lattice surgery 與魔術態工廠：同上第 11 章
- 編譯與控制堆疊、FPGA 即時回饋、校準依賴圖：同上第 12 章
- Shor 分解 15 的古典後處理：[`animations/shor-15.html`](../animations/shor-15.html)
- 讀取鏈與 IQ 判別：[`notes/dispersive-readout.md`](../notes/dispersive-readout.md)
- 光子互連（分散式量子計算）：[`animations/atoms.html`](../animations/atoms.html) 場景 9
- 1,000 位元系統的供電與周邊：[`docs/1000量子位元系統供電設計.md`](1000量子位元系統供電設計.md)

---

## 14. 參考資料

**錯誤更正與解碼**
- Google Quantum AI, "Quantum error correction below the surface code threshold," Nature (2024)：https://collaborate.princeton.edu/en/publications/quantum-error-correction-below-the-surface-code-threshold/
- Riverlane 即時解碼延遲：https://quantumcomputingreport.com/riverlane-demonstrates-real-time-qec-latency-performance-advancements/
- Riverlane 解碼器技術：https://thequantuminsider.com/2025/01/07/riverlane-reports-new-decoder-tech-sets-new-standard-in-quantum-error-correction/
- Riverlane + NVIDIA GPU 解碼器校準：https://quantumcomputingreport.com/riverlane-and-nvidia-demonstrate-accelerated-qec-decoder-calibration-using-gpu-processing/amp/
- Quantinuum Helios 即時錯誤更正：https://www.quantinuum.com/blog/real-time-error-correction-at-increased-scale
- NVIDIA NVQLink 架構：https://developer.nvidia.com/blog/nvidia-nvqlink-architecture-integrates-accelerated-computing-with-quantum-processors
- NVIDIA NVQLink 產品頁：https://www.nvidia.com/en-us/solutions/quantum-computing/nvqlink.md
- IBM Relay-BP FPGA 解碼：https://arxiv.org/pdf/2510.21600 ；演算法：https://arxiv.org/pdf/2506.01779
- AlphaQubit：https://blog.google/technology/google-deepmind/alphaqubit-quantum-error-correction/
- Mamba 解碼器：https://arxiv.org/html/2510.22724v1 ；平行滑動視窗：https://arxiv.org/html/2509.03815v1
- NVIDIA + QuEra AI 解碼器：https://developer.nvidia.com/blog/nvidia-and-quera-decode-quantum-errors-with-ai
- NVIDIA Ising 色碼解碼器：https://thequantuminsider.com/2026/07/15/nvidia-says-ai-decoder-achieved-up-to-347-x-cut-in-quantum-logical-error-rates/
- NVIDIA TCBP-JOBS：https://interestingengineering.com/science/nvidia-quantum-error-correction-decoding-breakthrough
- Riverlane QECi：https://postquantum.com/engineering-news/altera-riverlane-qeci-agilex-fpga/

**控制、讀取、校準、重排**
- Quantum Machines DGX Quantum：https://quantum-machines.co/products/nvidia-dgx-quantum
- RL 兩位元閘校準：https://www.quantum-machines.co/resources/blog/reinforcement-learning-two-qubit-gate-calibration/
- Rigetti × Quantum Machines AI 校準挑戰：https://thequantuminsider.com/2024/12/10/ai-driven-quantum-calibration-achieved-in-rigetti-and-quantum-machines-challenge/
- 神經網路多工讀取判別：https://arxiv.org/pdf/2102.12481 ；FPGA 版：https://arxiv.org/abs/2407.03852v2 ；LUNA：https://arxiv.org/pdf/2512.07808
- GPU 量子最佳控制（Leung 2017）：https://schusterlab.stanford.edu/static/pdfs/Leung2017.pdf
- 中性原子重排：https://arxiv.org/pdf/1704.07074 、https://arxiv.org/pdf/2412.14647 、https://arxiv.org/pdf/2610.21609 、https://arxiv.org/pdf/2604.08669 、https://arxiv.org/pdf/2411.12401 、https://ojs.aaai.org/index.php/AAAI/article/view/39967
- 離子阱 shuttling 編譯：https://arxiv.org/pdf/2402.14065 、https://quantum-journal.org/papers/q-2023-11-08-1176/

**演算法與應用**
- Gidney 2025, "How to factor 2048 bit RSA integers with less than a million noisy qubits"：https://arxiv.org/abs/2505.15917
- Regev 因數分解：https://arxiv.org/pdf/2308.06572.pdf ；Ragavan–Vaikuntanathan：https://arxiv.org/html/2310.00899v5 ；Ekerå–Gärtner：https://eprint.iacr.org/2023/1501.pdf
- SQD 原始論文：https://arxiv.org/html/2405.05068v3
- IBM + RIKEN 富岳：https://www.ibm.com/quantum/blog/riken-fugaku-qcsc
- QC-AFQMC（IonQ、AWS、NVIDIA、AstraZeneca）：https://arxiv.org/abs/2506.22408 、https://journals.aps.org/prresearch/abstract/10.1103/n1tf-8kr7
- NVIDIA GQE：https://developer.nvidia.com/blog/advancing-quantum-algorithm-design-with-gpt
- THC 化學：https://www.arxiv-vanity.com/papers/2011.03494/ 、https://arxiv.org/pdf/2501.06165
- Quantum Motion + NVIDIA DMRG 初始態：https://quantumcomputingreport.com/quantum-motion-and-nvidia-partner-to-resolve-state-preparation-obstacles-in-quantum-chemistry/amp/
- D-Wave 混合求解器：https://www.dwavequantum.com/media/4bnpi53x/14-1039a-b_d-wave_hybrid_solver_service_an_overview.pdf
- 電路切割：https://www.anl.gov/mcs/article/at-the-cutting-edge-of-quantum-computing 、https://www.arxiv.org/pdf/2409.03870 、https://arxiv.org/html/2603.12411v1
- IBM 量子效用實驗（Nature 2023）：https://www.nature.com/articles/s41586-023-06096-3.pdf
- Algorithmiq TEM：https://quantum.cloud.ibm.com/docs/guides/algorithmiq-tem

**驗證、設計、整合**
- 認證隨機數：https://www.olcf.ornl.gov/2025/05/05/quantum-computing-experiment-realizes-verifiably-random-number/
- Google Quantum Echoes：https://thequantuminsider.com/2025/10/22/google-quantum-ai-shows-13000x-speedup-over-worlds-fastest-supercomputer-in-physics-simulation/
- AWS Palace：https://aws.amazon.com/blogs/quantum-computing/aws-releases-open-source-software-palace-for-cloud-based-electromagnetics-simulations-of-quantum-computing-hardware/
- IBM × AMD：https://futurumgroup.com/insights/ibm-and-amd-join-forces-on-quantum-centric-supercomputing-initiative/
- Slurm QPU 外掛：https://arxiv.org/abs/2506.10052
- EuroQHPC-Integration：https://csc.fi/project/euroqhpc-i/
- Alice & Bob × Hartree Slurm 整合：https://www.hartree.stfc.ac.uk/news/2025/11/06/alice-bob-and-stfc-hartree-centre-integrate-cat-qubit-quantum-computers-into-standard-hpc-workflow-and-job-scheduling-software-slurm/
