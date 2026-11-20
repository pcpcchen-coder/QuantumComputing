# CPU + GPU + QPU 算力群：怎麼配置？會遇到哪些挑戰（尤其是電力）？

> 調查日期：2026-11-20
> 承接：[`docs/QPU與CPU-GPU協同運算需求調查.md`](QPU與CPU-GPU協同運算需求調查.md) 與簡報最後一頁的討論題「QPU 旁的 GPU 機櫃該怎麼設計？」
> 問題：(1) CPU + GPU + QPU 的算力群要怎麼配置？找實際案例。(2) 會遇到哪些挑戰？尤其是電力。
> 註記：標「廠商宣稱」者為公司新聞稿或部落格；標「粗估」者為本文依公開參數自行估算，只用來抓量級；標「推論」者為本文的工程判斷，沒有直接出處。OCP 白皮書指 2026 年 4 月版〈Integrating Quantum Processing Units into Data Center Infrastructure〉（以下簡稱 OCP 2026）。

---

## 0. 一頁結論

1. **配置已經從「雲端遠端」走到「同機房緊耦合」**。目前看得到五種配置：雲端遠端、HPC 中心同址（鬆耦合）、GPU–QPU 緊耦合節點、商用機房託管、專用量子資料中心。2024–2026 年新案大多是後三種。
2. **功率比例極度不對稱**：一台 QPU 本體 3–30 kW（OCP 2026），旁邊一個 GPU 機櫃就是 120–264 kW，2027 年 NVIDIA 要推 1 MW 機櫃。真實案例裡古典端功率是 QPU 的 **數十到上千倍**（ABCI-Q：2,020 張 H100；RIKEN：一台 Heron 配約 28–30 MW 的富岳）。**電力規劃的主角是 GPU，但最難伺候的是 QPU。**
3. **電力挑戰不是「電不夠」，而是「大負載與敏感負載住在一起」**。八個面向：電網容量、斷電與備援分級、AI 負載擺盪、電能品質（諧波、電壓驟降）、匯流排磁場、接地與 EMI、冷卻水溫衝突、振動與聲學。
4. **兩個容易被忽略的耦合**：(a) AI 訓練的功率在計算與通訊階段之間大幅擺盪（數十 MW 級，Microsoft/NVIDIA/OpenAI 2025），**擺盪的大電流會在匯流排周圍產生低頻變動磁場**，對中性原子、離子阱、自旋量子位元是雜訊；(b) **解碼器斷電＝量子計算失敗**，所以「QPU 旁的 GPU」要和 QPU 同一級備援，不能當成一般 AI 機櫃。
5. **建議的配置原則**：分區（量子靜區／即時控制區／GPU 液冷區／機電區）、分饋線（GPU、QPU 乾淨電源、低溫機組各自獨立變壓器）、分級備援（解碼器與 QPU 同級）、高壓直流（800 VDC 降低電流與磁場）、儲能平滑 AI 擺盪、光纖隔離接地。
6. **對我們的供電產品**：最直接的機會是「QPU 乾淨電源島」「低溫機組 UPS」「AI 擺盪平滑＋磁場感知配電」「電能品質＋磁場＋接地雜訊監測」四項（第 8 節）。

---

## 1. 算力群由哪些東西組成？

把一個「CPU + GPU + QPU」算力群拆開，從量子晶片往外有五層。每一層的功率、對環境的要求、能不能斷電，差異非常大：

| 層 | 內容 | 典型功率 | 環境敏感度 | 斷電容忍 |
|---|---|---|---|---|
| ① QPU 島 | 稀釋冷凍機／真空腔、雷射、光學桌、壓縮機、冷卻水 | 3–30 kW／台（OCP 2026） | **極高**：磁場、振動、溫度、EMI | 極低：恢復要 48 小時以上（OCP 2026）到 2–5 天（LRZ） |
| ② 即時控制層 | RF/AWG、FPGA/RFSoC、讀取鏈 | 數 kW～數十 kW | 高：低雜訊電源、接地 | 極低：斷了 QPU 就停 |
| ③ 即時解碼層 | FPGA/ASIC 解碼器＋GPU 伺服器（如 8×H200，約 11–12 kW／台，OCP 2026） | 數十 kW～數百 kW | 中：要在 QPU 幾公尺內 | **極低：斷了量子計算就失敗** |
| ④ 加速運算層 | GPU 叢集（AI 校準、SQD、誤差緩解、模擬） | 數百 kW～MW（GB200 機櫃 120–132 kW；Dell IR7000 最高 264 kW） | 低 | 中：可 checkpoint |
| ⑤ HPC／儲存／網路 | CPU 叢集、排程、儲存（QEC 資料量可達 100 TB/s 等級） | MW～數十 MW | 低 | 中 |

**重點**：第 ③ 層是新東西。它的功率像 AI 機櫃，可靠度要求卻像 QPU，位置還必須貼著 QPU。這就是「QPU 旁的 GPU 機櫃」難設計的根本原因。

---

## 2. 五種配置模式與案例

### 2.1 總覽

| 模式 | QPU 與古典的距離 | 互連延遲 | 適合的工作 | 代表案例 |
|---|---|---|---|---|
| A. 雲端遠端 | 不同城市 | 秒～分鐘（排隊） | 批次實驗、教學 | IBM Poughkeepsie、IBM Ehningen |
| B. HPC 中心同址（鬆耦合） | 同園區、同棟或同機房 | 毫秒～秒（乙太網路、Slurm） | VQE、SQD、誤差緩解 | RIKEN（Heron + 富岳）、LRZ、Jülich JUNIQ、CESGA QMIO、ORNL Pathfinder、EuroHPC 六站 |
| C. GPU–QPU 緊耦合 | 同機房、數公尺 | **< 4 µs**（NVQLink、DGX Quantum） | 即時解碼、AI 校準、動態電路 | IQCC（以色列）、Quantinuum Helios + GH200、ABCI-Q（日本）、NVAQC（波士頓） |
| D. 商用機房託管 | 進駐一般資料中心 | 取決於客戶連線 | 企業雲端服務、資料主權 | OQC 進駐 Equinix TY11（東京） |
| E. 專用量子資料中心 | 為量子設計的整棟建築 | 內部緊耦合 | 容錯量子計算 | PsiQuantum 布里斯本／芝加哥、Magne（丹麥） |

### 2.2 模式 A：雲端遠端

- **IBM Quantum Data Center（Poughkeepsie, 2019）**：IBM 第一座量子資料中心，集中放置多台量子電腦，使用者透過 IBM Quantum Platform 遠端存取（[The Quantum Insider](https://thequantuminsider.com/2024/10/01/ibm-opens-its-first-quantum-data-center-in-europe-featuring-16x-more-performant-heron-based-systems/)）。
- **IBM 歐洲量子資料中心（德國 Ehningen, 2024/10）**：IBM 第二座、美國以外第一座；開幕時有兩台 Eagle 系統，並規劃加入 Heron；**所有工作資料在歐盟境內處理**，回應資料主權法規（同上）。
- **特點**：QPU 由廠商集中維運，設施是「為量子而建」；缺點是古典端在遠端，只適合不講延遲的工作。

### 2.3 模式 B：HPC 中心同址（鬆耦合）

- **RIKEN 神戶：IBM Quantum System Two + 富岳（2025/6/24 啟用）**：第一套在美國以外、也不在 IBM 資料中心內的 System Two，搭載 156 位元 Heron；與富岳同在 RIKEN 計算科學研究中心，以高速網路連接，用來測試量子–古典低延遲通訊與 SQD 工作流程；NEDO 資助（[Verdict](https://www.verdict.co.uk/first-ibm-quantum-system/)、[w.media](https://w.media/ibm-deploys-first-overseas-quantum-system-two-in-japan/)）。2026 年 1 月以富岳全機（158,976 節點）＋Heron 完成鐵硫簇計算（見前一份報告）。富岳本身約 28.33 MW（Fujitsu SC20 TOP500 量測），含設施約 30 MW（[Fujitsu](https://www.fujitsu.com/downloads/SUPER/topics/sc20/supercomputer-fugaku-and-fujitsu-commercial-supercomputers.pdf)、[CACM](https://cacm.acm.org/magazines/2021/1/249447-fugaku-takes-the-lead/fulltext)）。
- **Jülich：JUNIQ + JUPITER**：JUPITER 是歐洲第一台百億億次（exascale）超級電腦，採 NVIDIA Grace Hopper，完整系統平均用電估計約 **11 MW**（[Techzine](https://www.techzine.eu/news/infrastructure/136413/europes-first-exascale-supercomputer-is-massive-yet-efficient)）；Jülich 是全球第一個購買 D-Wave Advantage 退火機的 HPC 中心，整合進 JUNIQ 並連到 JUPITER（[Quantum Computing Report](https://quantumcomputingreport.com/julich-supercomputing-centre-utilizes-jupiter-exascale-hardware-to-set-50-qubit-quantum-simulation-benchmark/)）；另有 Pasqal 中性原子系統接到 JURECA DC（[Pasqal](https://www.pasqal.com/wp-content/uploads/2025/03/Technical-Overview-for-Advanced-Users-Orion-Beta.pdf)）。
- **GENCI／CEA TGCC（法國）**：Pasqal 交付第一台 100+ 位元中性原子 QPU「Ruby」，由 CEA 在 TGCC 超算中心安裝運轉（[HPCQS](https://hpcqs.eu/news/pasqal-delivers-first-100-qubit-quantum-processor-unit-to-genci-and-cea)）。Pasqal Orion Beta 規格：峰值 10 kW、尺寸 270×530×310 cm、重 2,500 kg、需要隔振地板（[Pasqal 技術文件](https://www.pasqal.com/wp-content/uploads/2025/03/Technical-Overview-for-Advanced-Users-Orion-Beta.pdf)）；Pasqal 2026 永續白皮書則稱典型 2–3 kW（[Pasqal](https://www.pasqal.com/resources/2026-sustanability-whitepaper/)）。
- **LRZ（德國）**：IQM 20 位元超導機整合進 HPC 機房；冷卻中斷約 2 分鐘晶片就超過 1 K、重新降溫 2–5 天；降溫峰值約 30 kW（[arXiv:2509.12949](https://arxiv.org/abs/2509.12949)，本 repo [`docs/量子電腦供電設計文獻回顧與我們切入點.md`](量子電腦供電設計文獻回顧與我們切入點.md) 有詳細整理）。
- **CESGA QMIO（西班牙）**——**目前公開資料最完整的「同一機房」配置**（[arXiv:2505.19267](https://arxiv.org/abs/2505.19267)）：
  - OQC 32 位元超導 QPU（Oxford Instruments ProteoxLX 稀釋冷凍機），與 23 個 x86 節點（每節點 64 核、1 TB）及 16 個 A64FX 模擬節點**放在同一個標準 HPC 資料中心**；平面圖上 HPC 與量子硬體以**玻璃牆**分隔，線路從高架地板下相連。
  - 設施作法：電源備援、系統接 UPS、**壓縮機刻意與 UPS 迴路隔離**、檢查接地阻抗；冷凍機加裝調平地板層與**隔振框架**；液態氮每週補充，放在建築外的開放式籠子。
  - 軟體：只用 Slurm 排程。第一版把量子控制節點當成 Slurm 節點，每個電路多 **1–3 秒**排程開銷，使用者不滿意；第二版改成專用閘道節點＋ZeroMQ 訊息匯流排，延遲大幅下降。
  - **教訓**：保真度和「鄰近土木施工、有人進入機房、其他建築工程」相關——**同機房配置時，周邊活動就是雜訊源**。
- **ORNL Pathfinder（美國，2026/6/16 啟用）**：ORNL 第一台自購的在地量子電腦（IQM Radiance 20 位元超導），放在 Frontier 所在的國家計算科學中心，接到技術整合組的測試平台，用來發展量子–HPC 混合方法（[The Quantum Insider](https://thequantuminsider.com/2026/06/17/iqm-deploys-its-first-u-s-quantum-computer-at-oak-ridge-national-laboratory/)）。
- **EuroHPC 量子電腦網絡**：第一批六站在捷克（LUMI-Q）、德國（Euro-Q-Exa，LRZ）、西班牙、法國（GENCI/CEA）、義大利（CINECA，中性原子模擬器）、波蘭；第二批加上盧森堡、荷蘭（SURF）（[EuroHPC](https://eurohpc-ju.europa.eu/signature-procurement-contract-eurohpc-quantum-computer-located-italy-2025-03-26_en)、[Science|Business](https://sciencebusiness.net/news/quantum-computing/ecosystem-europes-quantum-computing-infrastructure-get-six-new-engines)）。EuroQHPC-Integration 專案（2025–2029）統一六站使用體驗；歐洲站點普遍用 Slurm 把 QPU 當成可排程資源（[CSC](https://csc.fi/project/euroqhpc-i/)、[Qt.eu](https://qt.eu/news/2025/2025-11-18_inauguration_of_jade_and_ruby_quantum_processors)）。

### 2.4 模式 C：GPU–QPU 緊耦合

- **以色列量子計算中心 IQCC（特拉維夫大學，2024/6/17 啟用）**：**第一個用 NVIDIA DGX Quantum 把多種 QPU 和超級電腦緊密整合的中心**；三台量子電腦（超導、冷離子、光子），控制層是 Quantum Machines OPX1000，古典端有 4 顆 Grace Hopper 超級晶片、128 個 AMD EPYC vCPU，另接 AWS 雲端；DGX Quantum 往返延遲 < 4 µs（[DCD](https://datacenterdynamics.com/en/news/quantum-machines-opens-israeli-quantum-computing-center-housing-three-systems)、[postquantum.com](https://postquantum.com/quantum-policy/israels-iqcc-quantum-data-center/)、[Times of Israel](https://www.timesofisrael.com/nvidia-builds-quantum-classical-computing-system-with-israels-quantum-machines/)）。
- **Quantinuum Helios + NVIDIA GH200 + NVQLink（2025）**：Helios 以 GH200 作為即時主機，GPU 跑 BP+OSD 解碼 67 µs（[Quantinuum](https://www.quantinuum.com/blog/real-time-error-correction-at-increased-scale)）。
- **ABCI-Q（日本 AIST G-QuAT，2025/5）**：**2,020 張 H100**，以 Quantum-2 InfiniBand 互連，同時接 Fujitsu 超導、QuEra 中性原子、OptQC 光子三種 QPU，用 CUDA-Q 協調，主打錯誤更正與應用開發（[NVIDIA 新聞稿](https://nvidianews.nvidia.com/news/nvidia-powers-worlds-largest-quantum-research-supercomputer)）。粗估：2,020 張 H100 × 700 W ≈ 1.4 MW，僅 GPU 本身；加上伺服器、網路與冷卻，整體應在 2–3 MW 等級（推論；官方未公布）。對照 QPU 每台 10–30 kW，**古典：量子 ≈ 50～100 : 1**。
- **NVIDIA NVAQC（波士頓，2025/3 宣布）**：以 GB200 NVL72（報導為 576 顆 Blackwell GPU）支援 Quantinuum、Quantum Machines、QuEra 與哈佛、MIT 的研究（[NVIDIA 部落格](https://blogs.nvidia.com/blog/nvidia-accelerated-quantum-research-center)、[DCD](https://datacenterdynamics.com/en/news/nvidia-to-build-quantum-computing-research-center-in-boston)）。
- **特點**：解碼器、AI 校準 GPU 放在 QPU 旁，**電力與可靠度設計要以「QPU 等級」對待 GPU**。

### 2.5 模式 D：商用機房託管（colocation）

- **OQC × Equinix TY11（東京）**：2023 年宣布，在 Equinix 東京 TY11 機房內部署企業級量子電腦，客戶透過 Equinix Fabric 從全球連線；在此之前 OQC 已在英國 Cyxtera 機房做過第一個「量子電腦進駐託管機房」（[Data Center Frontier](https://www.datacenterfrontier.com/colocation/article/33001720/equinix-will-host-a-quantum-computer-in-its-tokyo-colocation-center)、[OQC](https://oqc.tech/access/deployment/)）。
- **Oxford Instruments**：為資料中心設計的 ProteoxLX 用專用框架與防振波紋管（[Oxford Instruments](https://nanoscience.oxinst.com/resources/blog/from-concept-to-colocation-building-quantum-systems-for-data-centres-since-2020)）。
- **特點**：最考驗「實驗室等級設備進入營運機房」。OCP 2026 指出，量子電腦的供應鏈仍多是實驗室規格，**元件層級缺少雙電源輸入**，因此享受不到資料中心雙路供電的韌性。

### 2.6 模式 E：專用量子資料中心（容錯時代）

- **PsiQuantum 布里斯本／芝加哥**：布里斯本廠區分三部分，其中一個是 Linde 建造的大型低溫機組（cryoplant），規模被比作 SLAC 國家加速器實驗室的冷卻系統，要把光子晶片的低溫機櫃維持在數 K；主建築是「倉庫大小、配置類似資料中心」；目標 2027 年底運轉；芝加哥廠設在前 US Steel South Works 舊址，目標 2028 年（[Brisbane Development](https://brisbanedevelopment.com.au/inside-psiquantums-1-billion-plan-to-build-the-worlds-first-useful-quantum-computer-in-brisbane/?amp=1)、[PsiQuantum × Linde](https://www.psiquantum.com/news-import/psiquantum-linde)、[Business Wire](https://www.businesswire.com/news/home/20240725638752/en/PsiQuantum-To-Build-First-US-Based-Utility-Scale-Quantum-Computer-in-Chicago-Illinois)）。PsiQuantum 技術頁稱每個低溫機櫃約 30 W 冷卻功率、是最大稀釋冷凍機的數千倍（[PsiQuantum](https://psiquantum.com/technology)）。
- **Magne（丹麥）**：Atom Computing（硬體）＋Microsoft（軟體），1,225 顆中性原子、50 個邏輯位元，由 EIFO 與諾和諾德基金會合資的 QuNorth 購置，預計 2026 年底～2027 年初可用（[Quantum Computing Report](https://quantumcomputingreport.com/denmarks-qunorth-to-acquire-50-logical-qubit-magne-quantum-computer-from-atom-computing-and-microsoft/)、[IEEE Spectrum](https://spectrum.ieee.org/neutral-atom-quantum-computing)）。
- **集中式低溫架構**：OCP 2026 介紹 Maybell 的做法——用集中的液氦層取代每台獨立的冷凍機，支援多個模組化量子節點、電子放在相鄰機櫃；好處是單位能耗的冷卻效率較高，代價是多了一個共用封閉迴路、**冗餘度降低**。

---

## 3. 配比怎麼抓？

### 3.1 案例中的古典：量子功率比

| 案例 | 古典端 | QPU 端 | 古典：量子（粗估） |
|---|---|---|---|
| RIKEN 神戶 | 富岳約 28–30 MW | 1 台 Heron System Two（數十 kW 等級，推論） | **約 1,000 : 1** |
| ABCI-Q | 2,020 張 H100，粗估 2–3 MW | 3 種 QPU 各一，每台 10–30 kW | **約 50–100 : 1** |
| Jülich | JUPITER 平均約 11 MW | D-Wave（15–30 kW）＋中性原子（≤10 kW） | **約 300 : 1** |
| QMIO | 39 個 CPU 節點（數十 kW） | 1 台 32 位元超導（15–30 kW） | **約 1–3 : 1**（小型示範） |

### 3.2 依工作量估算（推論）

- **即時解碼**：OCP 2026 舉例，一台 4U、8×H200 的伺服器約 11–12 kW，搭配 FPGA，可支援「數萬顆物理位元」的錯誤更正。粗估：百萬物理位元需要數十台這類伺服器，**即時解碼層 0.3–1 MW**，必須放在 QPU 旁。
- **AI 加速層**：OCP 2026 的 Dell 例子是 GB200 NVL4 架構的 IR7000 機櫃，最高 264 kW／櫃、液冷。校準、SQD、誤差緩解等非即時工作可以放在一般 AI 機房。
- **儲存**：OCP 2026 估計未來容錯量子電腦可能產生約 **100 TB/s** 的錯誤更正資料；以 1,000 個物理位元組成的一個邏輯位元、每秒 1,000 週期、每樣本 4 bytes 計，每個邏輯位元每天約 **345 GB**。**儲存量跟著「位元×運轉小時」成長，不跟著使用者工作數量成長**——量子電腦像一台持續寫入的飛航記錄器。

### 3.3 一個參考規模：1,000 位元超導機＋解碼＋一個 GPU 單元（粗估）

| 項目 | 功率 | 依據 |
|---|---|---|
| 低溫鏈（壓縮機群、GHS、冰水機泵浦） | 55–110 kW | 本 repo [`docs/1000量子位元系統供電設計.md`](1000量子位元系統供電設計.md) |
| 室溫控制電子 | 數十 kW | 同上 |
| 即時解碼（FPGA＋GPU 伺服器） | 5–50 kW | 同上；OCP 2026 單台 11–12 kW |
| AI 加速（1–4 個 GB200 機櫃） | 130–530 kW | NVIDIA／HPE 機櫃規格 |
| **合計** | **約 0.25–0.75 MW** | GPU 占 **50–70%** |

---

## 4. 電力挑戰（核心）

### 4.1 電網容量與選址

- **規模差距**：QPU 3–30 kW；GB200 NVL72 約 120–132 kW、HPE 建議匯流排以約 192 kW 峰值設計（[HPE](https://www.hpe.com/int/en/collaterals/collateral.a50009224enw.html)）；NVIDIA 計畫 2027 年以 800 VDC 支援 **1 MW 以上**的 Kyber 機櫃（[NVIDIA 技術部落格](https://developer.nvidia.com/blog/nvidia-800-v-hvdc-architecture-will-power-the-next-generation-of-ai-factories/)）。
- **全球趨勢**：IEA 估計全球資料中心用電從 2024 年約 415 TWh 增加到 2030 年約 945 TWh，略高於日本全國用電（[IEA](https://www.iea.org/news/ai-is-set-to-drive-surging-electricity-demand-from-data-centres-while-offering-the-potential-to-transform-how-the-energy-sector-works)）。
- **台灣的限制**：台電 2024 年 8 月表示桃園以北不再核供 5 MW 以上資料中心，經濟部說明主因是北部電廠與電網瓶頸（[科技新報](https://finance.technews.tw/2024/08/12/want-big-ai-companies-to-invest-please-support-building-power-plants/)）；2025 年 11 月起 5 MW 以上資料中心納入能效管理，新設 PUE 須在 1.3–1.4 以下，核供審查約 3–6 個月（[自由時報](https://ec.ltn.com.tw/article/breakingnews/5234171)）；之後有專案審查放寬的報導，最新規定請以經濟部與台電公告為準。
- **含意（推論）**：一個「QPU＋解碼＋GPU 單元」就可能接近或超過 0.5 MW；若再加上大型 AI 叢集就是數 MW。**在台灣北部，GPU 才是決定能不能拿到電的主角**；QPU 島本身很小，但它要的是「乾淨、不能斷」的電。

### 4.2 斷電與備援分級

- **QPU 的代價**：OCP 2026 指出某些平台斷電後要 **48 小時以上**才能恢復；LRZ 實測冷卻中斷約 2 分鐘晶片就超過 1 K、重新降溫 2–5 天、最壞約 10 天。
- **解碼器的代價**：容錯計算進行中解碼器斷電，等於整個計算失敗（Gidney 2025 的 RSA 估算要連續跑將近一週）。
- **GPU 的代價**：AI 訓練可以從 checkpoint 恢復，損失有限。
- **實務分歧**：CESGA QMIO 把**壓縮機與 UPS 迴路隔離**（避免壓縮機啟動電流與雜訊影響 UPS 負載）；LRZ 的結論則是冷卻鏈必須有備援電力。兩者並不矛盾：關鍵是「壓縮機要有能撐到發電機接手的電源」，但不一定要和敏感電子共用同一台 UPS（推論）。
- **其他做法**：有建築師事務所的客戶要求全設施 UPS 撐 10 分鐘，只為避開發電機啟動時的電壓突波（[HOK](https://www.hok.com/news/2025-09/designing-quantum-research-labs-hok-qa/)）。

**建議的分級（推論）**：

| 等級 | 負載 | 目標 | 作法 |
|---|---|---|---|
| T0 不可中斷 | 即時控制電子、解碼器（FPGA＋GPU）、QPU 偏壓源 | 0 ms 切換、持續到發電機穩定之後 | 線上雙轉換 UPS、雙路供電、獨立電池 |
| T1 分鐘級 | 壓縮機群、GHS、冰水機泵浦、雷射 | 撐 2 分鐘以上到發電機接手 | 專用 UPS 或飛輪＋軟啟動／變頻；冷卻水蓄冷槽 |
| T2 可短暫中斷 | AI 加速 GPU（校準、SQD） | 秒級，可 checkpoint | 一般資料中心 UPS＋儲能平滑 |
| T3 一般 | HPC、儲存、辦公 | 一般標準 | 標準資料中心設計 |

### 4.3 AI 負載擺盪：GPU 會「搖」整個電網

- **現象**：大型 AI 訓練在「計算」與「通訊」階段之間切換，前者接近 GPU 熱設計極限，後者接近閒置；規模越大擺盪越大（[Microsoft Tech Community](https://techcommunity.microsoft.com/blog/azurecompute/power-stabilization-for-ai-training-datacenters/4460937)；Microsoft、NVIDIA、OpenAI 合著論文 "Power Stabilization for AI Training Datacenters"）。SemiAnalysis 描述整個資料中心可在瞬間擺盪**數十 MW**（[SemiAnalysis](https://newsletter.semianalysis.com/p/ai-training-load-fluctuations-at-gigawatt-scale-risk-of-power-grid-blackout)）。
- **對策**：NVIDIA GB300 NVL72 的電源架加入電解電容處理短時擺盪（每顆 GPU 約 65 J 儲能），宣稱訓練 Megatron 時電網看到的峰值降 30%（廠商宣稱，[NVIDIA 技術部落格](https://developer.nvidia.com/blog/how-new-gb300-nvl72-features-provide-steady-power-for-ai)）；Microsoft 論文建議 GPU 層平滑＋儲能並用，大型部署要考慮長時間電池儲能。
- **對 QPU 的影響（推論）**：
  1. **共用匯流排的電壓閃爍與驟降**：QPU 控制電子與精密偏壓源若和 GPU 共用變壓器，擺盪會變成電源雜訊。
  2. **低頻磁場雜訊**：擺盪的大電流讓匯流排周圍的磁場跟著變動（次 Hz 到數十 Hz），見 4.5。
  3. **冷卻系統聯動**：GPU 液冷 CDU 與冰水機跟著負載調速，振動與水溫也跟著變。

### 4.4 電能品質：諧波、驟降、雜訊

- GPU 電源供應器、壓縮機變頻器、冰水機變頻器都是非線性負載，會注入諧波；量子設施的電力工程職缺明確要求處理**諧波失真、驟降、突升、暫態、不平衡、閃爍**（[PsiQuantum 職缺](https://jobs.chicagoquantum.org/companies/psiquantum/jobs/73994843-principal-power-systems-architect-quantum-infrastructure)）。
- OCP 2026 的離子阱設施表要求電場符合 **FCC Class B**；選址章節提醒有些平台要遠離「高功率設備或大型變壓器」的電氣雜訊。
- **作法（推論）**：QPU 島用獨立變壓器（必要時加隔離變壓器）、線上雙轉換 UPS 當作濾波器、主動式諧波濾波器裝在 GPU 與變頻器那一側（從源頭抑制），並持續量測（可沿用本 repo [`docs/QGP量測規範草案.md`](QGP量測規範草案.md) 的量測項目）。

### 4.5 匯流排磁場：高電流就是磁場源

- **限制**：一份設施準備指南引用的門檻是冷凍機附近直流磁場 < 100 µT、交流磁場 < 1 µT；地磁本身就有 25–65 µT（[postquantum.com](https://postquantum.com/building-quantum-computers/quantum-computer-facility-preparation/)；本文未能在 OCP 原文中找到這兩個數字，僅作參考）。OCP 2026 表 1 將磁場敏感度標為：**中性原子、矽自旋「高」**，退火機「中」，閘式超導、離子阱「低」（各廠商自評，依系統設計而定）。
- **電流有多大**：1 MW 機櫃若用 54 V 供電，電流約 **18,500 A**；改用 800 VDC 約 **1,250 A**。NVIDIA 指出 54 V 下 1 MW 機櫃要約 200 kg 銅匯流排（[NVIDIA](https://developer.nvidia.com/blog/nvidia-800-v-hvdc-architecture-will-power-the-next-generation-of-ai-factories/)）。
- **磁場粗估**（理想雙導體模型，正負導體間距 0.1 m，B ≈ µ₀·I·d／(2π·r²)）：

| 供電方式 | 電流 | 距離 3 m | 距離 10 m |
|---|---|---|---|
| 54 V、1 MW | 18,500 A | 約 41 µT | 約 3.7 µT |
| 800 V、1 MW | 1,250 A | 約 2.8 µT | 約 0.25 µT |

  若 AI 負載擺盪 30%，54 V 在 3 m 處的磁場變動約 12 µT，**遠超過 1 µT 的交流門檻**；800 V 在 10 m 處約 0.08 µT（粗估）。實際值取決於導體排列、遮蔽與鋼構，**必須現場量測**。
- **結論（推論）**：**800 VDC 不只是省銅與提升效率，對 QPU 共置也是降低磁場的關鍵**；配電路由要避開 QPU 島，並保持距離。

### 4.6 接地與 EMI

- 超導位元的工作頻段在 4–8 GHz，該頻段的干擾會直接耦合到位元；設施準備指南建議至少 25 小時的 4–8 GHz 頻譜量測（[postquantum.com](https://postquantum.com/building-quantum-computers/quantum-computer-facility-preparation/)）。OCP 2026 也建議遠離無線電發射台、基地台、日光燈，必要時在冷凍機外加室溫磁遮蔽。
- **地迴路**：GPU 機櫃與 QPU 控制電子若用銅纜（PCIe、乙太網路）直接相連，兩者的地電位差會形成地迴路。QMIO 的作法是檢查接地阻抗。**推論**：解碼器與 QPU 控制層之間優先用光纖（NVQLink、RoCE 都可走光纖），切斷電氣連接；QPU 島採單點接地，GPU 區另成系統，兩者在主接地匯流排會合。

### 4.7 冷卻水與熱：兩套溫度、兩種脾氣

- **QPU 側**（OCP 2026 表 3）：D-Wave 冷卻水最低 15 °C（9.4 L/min）、最高 25 °C（20.5 L/min），最大水壓 88 psi；Diraq 自旋系統 10–28 °C、每 kW 1–2 L/min；超導機房溫度 20–25 °C、**12 小時內變化 < 1 °C**；離子阱 20–24 °C、48 小時內 < 2 °C；Pasqal 水溫 14–18 °C。
- **GPU 側**：GB200 NVL72 以直接液冷為主（約 115 kW 走液冷、17 kW 走風冷，QCT 文件），需要專用液冷迴路與 CDU（[QCT](https://blog.qct.io/wp-content/uploads/2025/04/QCT-Qoolrack-Stand-Alone_Advanced-Liquid-Cooling-for-NVIDIA-GB200-NVL72-Systems.pdf)）；業界液冷趨勢是較高的供水溫度（溫水冷卻）以提高效率（一般資料中心做法）。
- **衝突（推論）**：QPU 要低溫、穩定的冷卻水，GPU 要大流量、可較高溫的冷卻水；**不能共用同一迴路**。GPU 區排出的大量廢熱也不能影響 QPU 房的室溫穩定度（< 1 °C／12 h）。可行做法是兩套迴路、QPU 房獨立精密空調，GPU 廢熱另行回收再利用。

### 4.8 振動與聲學

- **限制**（OCP 2026）：離子阱 1–200 Hz 範圍內 **12.5 µm/s**、噪音 ≤ 65 dBA；中性原子 50 µm/s、≤ 75 dBA；超導（OQC、IQM）表列 400 µm/s；退火機 50 µm/s。
- **振動源**：GPU 高速風扇、液冷泵浦與 CDU、冰水機、壓縮機、鄰近交通與施工。QMIO 觀察到保真度和鄰近施工、人員進出相關。
- **作法**：冷凍機與光學桌用隔振框架或負剛度隔振器（Maybell 的隔振器標稱低於 0.5 Hz，[postquantum.com](https://postquantum.com/building-quantum-computers/quantum-computer-facility-preparation/)），QPU 島與機電區分開的結構基礎；GPU 區與 QPU 島之間保持距離或做結構斷開（推論）。

### 4.9 結構、空間與物流

- **地板與空間**（OCP 2026）：稀釋冷凍機平台地板承重 1,000 kg/m²、最重元件 750 kg、儲存區 2.4×6.1×3 m；離子阱與中性原子 500 kg/m²、需 40–70 m² 組裝區、走道 1.5 m、門寬 1.2–2 m、淨高 3 m。Pasqal Orion Beta 整機 2,500 kg。
- **冷媒**：OCP 2026 表列超導、退火、自旋系統每 15 天補一次液態氮；稀釋冷凍機混合氣中氦-3 約占 6–7%（氦-3 供應本身是全球性瓶頸）。QMIO 每週補液氮、放在建築外。
- **設備等級**：OCP 2026 強調目前多數量子設備是實驗室規格，缺少雙電源輸入與熱插拔電源，資料中心的韌性設計用不上。

### 4.10 擴大之後：低溫系統的電力外推

- 目前的超導量子電腦，耗電大宗是低溫系統：OCP 2026 指出冷凍機（壓縮機）占了表列功率的大部分，單台壓縮機 3–11 kW、需水冷，功率隨所需冷卻力增加。
- Fellous-Asiani 等人（PRX Quantum 2023）建立全堆疊能耗模型：未經最佳化的大型容錯計算可能接近 GW，最佳化後可降到數 MW；對六種開發中的機器、各擴大到 4,000 個邏輯位元的粗略預測，功率從 **不到 1 MW 到超過 100 MW**（[arXiv:2209.05469](https://arxiv.org/abs/2209.05469)、[Physics Today](https://physicstoday.aip.org/news/how-much-electricity-does-a-quantum-computer-need)）。
- **控制電子**：Google 的低溫 CMOS 脈衝調變器低於 2 mW，但每位元功率必須降到毫瓦以下；Google 72 位元處理器已有 168 條同軸線進冷凍機（[IEEE Spectrum](https://spectrum.ieee.org/google-team-builds-circuit-to-solve-one-of-quantum-computings-biggest-problems)）。**線材與低溫功率，是超導擴大的雙重瓶頸**。
- **含意（推論）**：容錯時代的「量子島」會從數十 kW 長到 MW 級，屆時 QPU 本身也會成為大負載，而它旁邊的解碼與 AI 層可能更大。

---

## 5. 建議的配置藍圖（推論）

### 5.1 平面分區

```
┌──────────────────────────── 機電區（遠離量子靜區） ────────────────────────────┐
│ 中壓進線 ×2 → 變壓器 T1（GPU）  T2（QPU 乾淨電源）  T3（低溫機組）   發電機  電池／儲能 │
│ 冰水機、冷卻塔、壓縮機群（可遠端放置，以氦氣管線連到冷凍機）                         │
└─────────────────────────────────────────────────────────────────────────────┘
        ║ 800 VDC（GPU）              ║ 乾淨 AC（UPS 後）          ║ 壓縮機饋線
┌───────────────┐   光纖   ┌────────────────────┐        ┌──────────────────┐
│ GPU 液冷區      │◀───────▶│ 即時控制＋解碼區       │◀ 光纖 ▶│ 量子靜區（QPU 島）     │
│ AI 校準、SQD、  │  < 數十 m │ FPGA、RFSoC、解碼 GPU │ < 10 m │ 冷凍機／真空腔、光學桌  │
│ 誤差緩解、模擬   │          │ T0 等級備援            │        │ 隔振基礎、磁遮蔽、精密空調│
└───────────────┘          └────────────────────┘        └──────────────────┘
        ║                                                    （玻璃牆或結構斷開）
┌───────────────┐
│ HPC／儲存／網路   │  QEC 資料：數百 GB／邏輯位元／天
└───────────────┘
```

### 5.2 電力架構重點

1. **三組獨立變壓器**：GPU（大電流、擺盪）、QPU 乾淨電源（小、敏感）、低溫機組（啟動電流大）分開，避免互相干擾。
2. **GPU 走 800 VDC**：降低電流、銅量與磁場；在 GPU 側加電容／電池儲能，平滑 AI 擺盪，不讓擺盪傳到共用的中壓匯流排。
3. **QPU 乾淨電源島**：隔離變壓器＋線上雙轉換 UPS＋低雜訊配電，量測 THD、閃爍、共模雜訊。
4. **解碼器與 QPU 同級（T0）**：解碼 GPU 機櫃雖然功率像 AI 機櫃，備援要比照 QPU。
5. **低溫機組專用 UPS（T1）**：軟啟動或變頻壓縮機降低啟動電流；冷卻水加蓄冷槽；與敏感電子的 UPS 分開（QMIO 作法）。
6. **磁場感知配電**：大電流匯流排與 QPU 島保持距離（依 4.5 的粗估，800 VDC 需約 10 m 等級；54 V 需更遠或遮蔽），實地量測直流與交流磁場。
7. **光纖隔離**：控制與解碼之間、解碼與 GPU 區之間全部走光纖。

### 5.3 一張檢查表（給規劃者）

| 類別 | 要確認的事 |
|---|---|
| 電網 | 可用容量、核供時程（台灣約 3–6 個月審查）、雙路進線 |
| 備援 | T0／T1 範圍、UPS 撐多久、發電機啟動突波 |
| 電能品質 | THD、閃爍、驟降容忍、共模雜訊；GPU 與變頻器側濾波 |
| 磁場 | 直流 < 100 µT、交流 < 1 µT（參考值）；匯流排路由與距離；擺盪造成的低頻磁場 |
| 接地與 EMI | 單點接地、光纖隔離、4–8 GHz 頻譜量測 ≥ 25 小時 |
| 冷卻 | QPU 水溫 10–28 °C（依平台）、室溫 ΔT < 1 °C／12 h；GPU 液冷獨立迴路 |
| 振動 | 12.5–400 µm/s（依平台）；風扇、泵浦、壓縮機位置 |
| 結構 | 500–1,000 kg/m²、淨高 3 m、搬運路徑 |
| 冷媒 | 液氮每 1–2 週補充、氦-3 庫存 |
| 資料 | QEC 資料儲存與網路頻寬 |

---

## 6. 不同平台的配置差異

| 平台 | 本體功率（OCP 2026） | 最敏感 | 配置重點 |
|---|---|---|---|
| 超導閘式（IBM、IQM、OQC） | 15–30 kW | 溫度（Teflon 介電）、振動、斷電 | 壓縮機與冷卻水、T1 備援；解碼要在 µs 級，GPU 只做外層 |
| 退火（D-Wave） | 15–30 kW | 振動高、磁場中 | 隔振、冷卻水 15–25 °C |
| 離子阱（Quantinuum、IonQ） | 15–30 kW（OCP 表 2 峰值 27 kW） | 振動 12.5 µm/s、噪音 65 dBA、溫濕度 | GPU 可直接進即時迴路（Helios 2 ms 窗） |
| 中性原子（Pasqal、QuEra、Infleqtion、Atom Computing） | 3.5–10 kW | **磁場高**、濕度（自由空間光學） | 遠離大電流匯流排；重排與 AI 解碼 GPU 就在旁邊 |
| 光子（ORCA、PsiQuantum） | 3 kW（ORCA）；公用規模為大型低溫機組 | 低 | 小型可放標準機櫃；大型要專用低溫廠 |
| 室溫鑽石 NV（Quantum Brilliance） | 0.3–0.6 kW | 低 | 可直接放進一般機櫃 |

---

## 7. 尚未解決的問題

1. **沒有公開的「QPU 與 GPU 共置」量測數據**：AI 擺盪造成的磁場與電源雜訊，到底讓量子位元錯誤率增加多少？目前沒有找到實測論文。
2. **磁場門檻沒有統一標準**：100 µT／1 µT 只見於二手資料；OCP 2026 只給定性等級。
3. **實驗室規格設備**：缺雙電源、缺熱插拔，資料中心韌性設計用不上（OCP 2026）。
4. **容錯時代的解碼功率**：沒有找到百萬位元解碼器總功率的公開估算；本文的 0.3–1 MW 是依 OCP 單台規格外推。
5. **集中式低溫的冗餘問題**：省電但降低冗餘（OCP 2026 對 Maybell 架構的評論）。

---

## 8. 對我們供電產品的啟示

| 挑戰 | 產品機會 | 優先 |
|---|---|---|
| QPU 與控制電子要乾淨、不能斷（4.2、4.4） | **QPU 乾淨電源島**：隔離變壓器＋線上 UPS＋低雜訊配電的模組化方案 | ★★★ |
| 壓縮機斷電 2 分鐘就要付出數天（4.2） | **低溫機組 UPS**：針對壓縮機啟動電流設計，搭配軟啟動與蓄冷槽 | ★★★ |
| AI 擺盪傳到 QPU（4.3、4.5） | **擺盪平滑儲能＋磁場感知配電**：GPU 側電容／電池、800 VDC 路由設計服務 | ★★ |
| 沒人量測共置干擾（4.4–4.6、第 7 節） | **電能品質＋磁場＋接地雜訊監測**：把 QGP 量測規範延伸到磁場與共模雜訊，做成長期監測產品 | ★★ |
| 解碼 GPU 要 T0 等級（4.2） | **解碼機櫃供電**：高功率液冷機櫃的高可靠度供電（雙路、儲能） | ★★ |
| 設備缺雙電源（4.9） | **自動切換開關（STS）與雙路轉單路模組**：讓實驗室設備也能接雙路供電 | ★ |

> 這張表可以接到本 repo [`docs/我們量子供電產品開發計畫.md`](我們量子供電產品開發計畫.md) 的路線圖：前兩項對應現有的「分層機房參考設計」，後四項是 GPU 共置帶來的新需求。

---

## 9. 參考資料

**配置案例**
- IBM 量子資料中心（Ehningen、Poughkeepsie）：https://thequantuminsider.com/2024/10/01/ibm-opens-its-first-quantum-data-center-in-europe-featuring-16x-more-performant-heron-based-systems/
- IBM × RIKEN System Two：https://www.verdict.co.uk/first-ibm-quantum-system/ 、https://w.media/ibm-deploys-first-overseas-quantum-system-two-in-japan/
- 富岳功率：https://www.fujitsu.com/downloads/SUPER/topics/sc20/supercomputer-fugaku-and-fujitsu-commercial-supercomputers.pdf 、https://cacm.acm.org/magazines/2021/1/249447-fugaku-takes-the-lead/fulltext
- JUPITER 功率：https://www.techzine.eu/news/infrastructure/136413/europes-first-exascale-supercomputer-is-massive-yet-efficient
- Jülich D-Wave／JUNIQ：https://quantumcomputingreport.com/julich-supercomputing-centre-utilizes-jupiter-exascale-hardware-to-set-50-qubit-quantum-simulation-benchmark/
- Pasqal Orion Beta 規格：https://www.pasqal.com/wp-content/uploads/2025/03/Technical-Overview-for-Advanced-Users-Orion-Beta.pdf ；永續白皮書：https://www.pasqal.com/resources/2026-sustanability-whitepaper/ ；GENCI/CEA：https://hpcqs.eu/news/pasqal-delivers-first-100-qubit-quantum-processor-unit-to-genci-and-cea
- LRZ／IQM：https://arxiv.org/abs/2509.12949
- CESGA QMIO：https://arxiv.org/abs/2505.19267
- ORNL Pathfinder：https://thequantuminsider.com/2026/06/17/iqm-deploys-its-first-u-s-quantum-computer-at-oak-ridge-national-laboratory/
- EuroHPC：https://eurohpc-ju.europa.eu/signature-procurement-contract-eurohpc-quantum-computer-located-italy-2025-03-26_en 、https://sciencebusiness.net/news/quantum-computing/ecosystem-europes-quantum-computing-infrastructure-get-six-new-engines 、https://csc.fi/project/euroqhpc-i/ 、https://qt.eu/news/2025/2025-11-18_inauguration_of_jade_and_ruby_quantum_processors
- IQCC：https://datacenterdynamics.com/en/news/quantum-machines-opens-israeli-quantum-computing-center-housing-three-systems 、https://postquantum.com/quantum-policy/israels-iqcc-quantum-data-center/
- Quantinuum Helios：https://www.quantinuum.com/blog/real-time-error-correction-at-increased-scale
- ABCI-Q：https://nvidianews.nvidia.com/news/nvidia-powers-worlds-largest-quantum-research-supercomputer
- NVAQC：https://blogs.nvidia.com/blog/nvidia-accelerated-quantum-research-center
- OQC × Equinix：https://www.datacenterfrontier.com/colocation/article/33001720/equinix-will-host-a-quantum-computer-in-its-tokyo-colocation-center 、https://oqc.tech/access/deployment/
- Oxford Instruments 資料中心型冷凍機：https://nanoscience.oxinst.com/resources/blog/from-concept-to-colocation-building-quantum-systems-for-data-centres-since-2020
- PsiQuantum：https://brisbanedevelopment.com.au/inside-psiquantums-1-billion-plan-to-build-the-worlds-first-useful-quantum-computer-in-brisbane/?amp=1 、https://www.psiquantum.com/news-import/psiquantum-linde 、https://psiquantum.com/technology
- Magne：https://quantumcomputingreport.com/denmarks-qunorth-to-acquire-50-logical-qubit-magne-quantum-computer-from-atom-computing-and-microsoft/

**設施與電力**
- OCP 2026 白皮書：https://www.opencompute.org/documents/integrating-qpus-into-dc-infrastructure-pdf
- 設施準備指南（磁場、EMI、振動）：https://postquantum.com/building-quantum-computers/quantum-computer-facility-preparation/
- NVIDIA 800 VDC：https://developer.nvidia.com/blog/nvidia-800-v-hvdc-architecture-will-power-the-next-generation-of-ai-factories/
- GB200 NVL72 功率與液冷：https://www.hpe.com/int/en/collaterals/collateral.a50009224enw.html 、https://blog.qct.io/wp-content/uploads/2025/04/QCT-Qoolrack-Stand-Alone_Advanced-Liquid-Cooling-for-NVIDIA-GB200-NVL72-Systems.pdf
- AI 負載擺盪：https://techcommunity.microsoft.com/blog/azurecompute/power-stabilization-for-ai-training-datacenters/4460937 、https://developer.nvidia.com/blog/how-new-gb300-nvl72-features-provide-steady-power-for-ai 、https://newsletter.semianalysis.com/p/ai-training-load-fluctuations-at-gigawatt-scale-risk-of-power-grid-blackout
- IEA Energy and AI：https://www.iea.org/news/ai-is-set-to-drive-surging-electricity-demand-from-data-centres-while-offering-the-potential-to-transform-how-the-energy-sector-works
- 台灣北部資料中心供電：https://finance.technews.tw/2024/08/12/want-big-ai-companies-to-invest-please-support-building-power-plants/ 、https://ec.ltn.com.tw/article/breakingnews/5234171
- 量子設施電力工程職缺（電能品質項目）：https://jobs.chicagoquantum.org/companies/psiquantum/jobs/73994843-principal-power-systems-architect-quantum-infrastructure
- HOK 量子實驗室設計：https://www.hok.com/news/2025-09/designing-quantum-research-labs-hok-qa/
- 全堆疊能耗：https://arxiv.org/abs/2209.05469 、https://physicstoday.aip.org/news/how-much-electricity-does-a-quantum-computer-need
- 低溫 CMOS 與線材：https://spectrum.ieee.org/google-team-builds-circuit-to-solve-one-of-quantum-computings-biggest-problems
