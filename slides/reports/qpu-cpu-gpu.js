/*
 * QPU 與 CPU／GPU 協同運算需求調查（簡報版）
 * 內容來源：docs/QPU與CPU-GPU協同運算需求調查.md
 * 產生：cd slides && node build_deck.js reports/qpu-cpu-gpu.js
 *
 * 規則：數字都來自報告引用的論文、官方部落格與報導；
 *       標「廠商宣稱」者尚無獨立驗證；標「粗估」者為依公開參數自行估算，只用來抓量級。
 */

module.exports = {
  meta: {
    title: "QPU 與 CPU／GPU 協同運算：哪些量子工作需要大量古典算力？",
    subject: "未來資料中心 CPU + GPU + QPU 並存時的古典算力需求調查",
    series: "技術分享｜量子 × 古典協同運算",
    footer: "QPU 與 CPU／GPU 協同運算需求調查",
    output: "qpu-cpu-gpu-hybrid.pptx",
  },
  slides: [
    // ───────── 開場 ─────────
    {
      type: "title",
      section: "開場",
      kicker: "技術分享｜量子 × 古典協同運算",
      title: "QPU 需要多少 CPU 與 GPU？\n量子資料中心的古典算力地圖",
      subtitle: "從 RF 控制、錯誤更正解碼到 Shor 演算法，逐項拆解古典端在做什麼",
      meta: [
        "範圍：九大類、19 項需要大量古典算力的 QPU 工作，依 ns 到月的時間尺度分層，每類附實際案例",
        "書面報告：docs/QPU與CPU-GPU協同運算需求調查.md（含完整出處）",
      ],
      notes:
        "今天的題目是：未來資料中心裡 CPU、GPU、QPU 會放在一起，那到底有哪些量子運算工作，需要大量的 CPU 和 GPU 介入配合？很多人直覺會想到兩個地方：一個是控制 RF 微波，一個是像 Shor 這種演算法的計算流程。我把所有可能的地方整理成九大類、十九項工作，依照需要多快回應來分層，每一類都找了實際的案例。最後會專門拆解 Shor，答案可能跟大家想的不一樣。",
    },
    {
      type: "agenda",
      section: "開場",
      title: "今天的脈絡",
      items: [
        { head: "時間尺度分層", body: "從 **ns** 到**月**，每一層由 FPGA、GPU、CPU 或 HPC 負責" },
        { head: "控制層", body: "RF 脈衝、讀取判別、**AI 校準**、中性原子重排、離子搬移" },
        { head: "即時錯誤更正", body: "未來**最大**的古典負擔：每 µs 都不能停的解碼" },
        { head: "編譯與混合迴圈", body: "化學前處理、VQE、**SQD × 富岳**、QC-AFQMC、誤差緩解" },
        { head: "Shor 專題", body: "前處理、執行期、後處理，**古典算力到底花在哪**" },
        { head: "資料中心啟示", body: "驗證、互連、排程、平台比較與**供電規劃**" },
      ],
      notes:
        "整份分享分成六段。先建立一個時間尺度的框架，因為古典算力介入的方式，取決於它必須多快回應。接著是控制層，也就是貼著量子晶片的古典電子。第三段是即時錯誤更正，這是未來最大的古典負擔。第四段是編譯和各種混合演算法。第五段專門拆解 Shor。最後談驗證、資料中心的互連與排程，以及對機房規劃的啟示。",
    },
    {
      type: "summary",
      section: "開場",
      title: "一頁結論",
      points: [
        "**QPU 是被古典電腦包圍的協處理器**：從開機、校準、執行到驗證，每一步都要古典算力",
        "**RF 本身由 FPGA 即時產生**；CPU／GPU 負責決定 RF 長什麼樣子：波形設計、校準、編譯",
        "**最重的古典工作是即時錯誤更正解碼**：百萬位元的機器要持續處理約 **0.5 Tb/s** 症狀資料（粗估）",
        "**Shor 的前處理與後處理很輕**（筆電就夠）；重的是執行那幾天裡**每 µs 都不能停的解碼**",
        "**規劃時要假設「一台 QPU ↔ 一整排 GPU／FPGA 機櫃」**，而且要放在 QPU 旁邊、用專用低延遲互連",
      ],
      notes:
        "先講結論。第一，量子處理器從來不是獨立運作的機器，它是一顆被古典電腦包圍的協處理器。第二，控制 RF 這件事，真正吐出微波的是 FPGA 和 DAC，CPU 和 GPU 負責的是決定微波長什麼樣子。第三，未來最重的古典工作是即時錯誤更正的解碼，百萬位元的機器，解碼器要持續吞下大約每秒 0.5 Tb 的資料，這是我依公開參數粗估的量級。第四，Shor 的前處理和後處理其實很輕，真正重的是執行期間的解碼。第五，機房規劃要假設一台 QPU 旁邊配一整排 GPU 和 FPGA 機櫃。",
    },

    // ───────── 時間尺度分層 ─────────
    {
      type: "table",
      section: "時間尺度分層",
      title: "依回應速度分成五層",
      headers: ["時間尺度", "典型工作", "主要古典硬體"],
      colW: [2.2, 6.0, 3.933],
      rows: [
        ["奈秒（ns）", "RF 脈衝產生、ADC 取樣、解調、判斷 0/1", "FPGA、RFSoC、ASIC"],
        ["微秒（µs）", "即時錯誤更正解碼、量測後條件回饋、原子重排", "FPGA／ASIC，GPU 開始加入"],
        ["毫秒～秒", "校準、漂移追蹤、搬移路徑、變分演算法每一輪", "GPU 伺服器、CPU"],
        ["分鐘～小時", "誤差緩解、SQD 對角化、QC-AFQMC、解碼器訓練", "GPU 叢集、超級電腦"],
        ["天～月（離線）", "大型演算法編譯、化學前處理、晶片模擬、驗證", "超級電腦、雲端 HPC"],
      ],
      callout: "越往上越要**貼近 QPU**；越往下越可以放在**遠端 HPC**",
      notes:
        "這張表是整份分享的框架。最上面是奈秒層，產生微波、取樣、判斷 0 或 1，只有 FPGA 或 ASIC 做得到。第二層是微秒層，錯誤更正的解碼、量測之後依結果決定下一步，傳統上也是 FPGA，現在 GPU 透過低延遲互連開始加入。第三層是毫秒到秒，校準、路徑計算、變分演算法的每一輪更新，是 GPU 伺服器的工作。第四層是分鐘到小時的大量後處理，用 GPU 叢集或超級電腦。最下面是離線工作。原則很簡單：越即時的越要貼近量子晶片。",
    },
    {
      type: "flow",
      section: "時間尺度分層",
      title: "資料怎麼在 QPU 與古典之間流動",
      steps: [
        { head: "QPU", body: "量子晶片、離子阱或原子陣列\n輸出微弱類比訊號", tone: "quantum" },
        { head: "FPGA／RFSoC", body: "產生 RF、取樣、解調\n**只往上送 0/1 位元**", tone: "warn" },
        { head: "解碼器", body: "FPGA／ASIC＋GPU\n每 µs 解一次症狀", tone: "bad" },
        { head: "GPU 伺服器", body: "校準、重排、AI 解碼\n毫秒～秒", tone: "neutral" },
        { head: "CPU／HPC", body: "編譯、排程、後處理\n分鐘以上", tone: "good" },
      ],
      boxHeight: 2.3,
      bullets: [
        "往上走：資料量**越來越小**（類比波形 → 位元 → 症狀 → 結果）",
        "往下走：指令**越來越即時**（演算法 → 電路 → 脈衝時間表 → 波形）",
        "瓶頸在中間兩格：**資料量最大、延遲要求又最嚴**",
      ],
      notes:
        "這張圖看資料怎麼流動。量子晶片輸出的是很微弱的類比訊號，第一站是 FPGA 或 RFSoC，負責產生微波、取樣和解調，它只往上送 0 和 1。第二站是解碼器，每一微秒要解一次症狀。再往上是 GPU 伺服器做校準和 AI，最上面是 CPU 和 HPC 做編譯和後處理。往上走資料量越來越小，往下走指令越來越即時。真正的瓶頸在中間兩格：資料量最大，延遲要求又最嚴。",
    },

    // ───────── 控制層 ─────────
    {
      type: "cards",
      section: "控制層",
      title: "控制 RF：CPU／GPU 不直接吐微波",
      cards: [
        { icon: "md:MdSettingsInputAntenna", tone: "warn", badge: "FPGA／RFSoC", head: "即時產生 RF", body: ["XY 驅動 4–8 GHz、數十 ns 脈衝", "Z 磁通、讀取音調", "離子／原子：AOM、AOD 射頻"] },
        { icon: "fa:FaMicrochip", tone: "neutral", badge: "CPU／GPU", head: "決定 RF 長怎樣", body: ["電路編譯成**脈衝時間表**", "振幅、頻率、相位、虛擬 Z", "動態電路的條件分支"] },
        { icon: "fa:FaLayerGroup", tone: "bad", badge: "規模化", head: "千條通道", body: ["1,000 位元 ≈ 數千條 RF 通道", "波形記憶體、同步時脈", "全部要古典電子撐住"] },
      ],
      callout: "回答「控制 RF 要不要 CPU／GPU？」：**即時輸出靠 FPGA，波形設計與排程靠 CPU／GPU**",
      notes:
        "先回答第一個問題：控制 RF 需不需要 CPU 和 GPU？超導位元要 XY 驅動、Z 磁通和讀取音調；離子阱和中性原子要雷射調變器的射頻音調。這些即時輸出都是 FPGA 和 RFSoC 的工作，延遲在奈秒。CPU 和 GPU 的角色是決定這些微波長什麼樣子：把電路編譯成脈衝時間表，算出每個脈衝的振幅、頻率、相位。規模化之後，一千顆位元就是數千條 RF 通道，波形記憶體和同步時脈都是古典電子的負擔。",
    },
    {
      type: "cards",
      section: "控制層",
      title: "讀取：資料大到不可能送去 GPU",
      cards: [
        { icon: "fa:FaWaveSquare", tone: "bad", badge: "粗估 1.5 Pb/s", head: "原始資料量", body: ["每條讀取線 1 GS/s × 12 bit", "每條多工 8 顆位元", "百萬位元 ≈ 12.5 萬條線"] },
        { icon: "fa:FaBrain", tone: "quantum", badge: "< 50 ns", head: "神經網路判別", body: ["5 顆多工位元做進 RFSoC", "指派錯誤最多降 **25%**", "串擾降一個數量級"] },
        { icon: "fa:FaCamera", tone: "neutral", badge: "原子／離子", head: "讀取是影像", body: ["螢光照片判斷有無原子", "上萬格點的影像分割", "典型 GPU 影像運算"] },
      ],
      callout: "解調與判別必須在 **ADC 旁的 FPGA** 完成；GPU 負責**訓練與定期重訓**判別模型",
      notes:
        "讀取的部分。假設每條讀取線用 1 GS/s、12 位元取樣，每條線多工 8 顆位元，百萬位元的機器有十二萬五千條線，原始資料加起來大約每秒 1.5 Pb，這是粗估，但足以說明不可能把原始波形送到 GPU。所以解調和判別一定在 ADC 旁邊的 FPGA 裡完成。進階做法是用神經網路判別，可以補償多工讀取的串擾，已經有團隊把它做進 RFSoC，五顆位元小於 50 奈秒。GPU 的角色是訓練和定期重訓模型。中性原子和離子的讀取則是拍照，上萬格點的影像處理是 GPU 擅長的工作。",
    },
    {
      type: "cards",
      section: "控制層",
      title: "校準：從人工掃描到 AI 代理人",
      cards: [
        { icon: "fa:FaSlidersH", tone: "warn", badge: "千萬級參數", head: "為什麼重", body: ["每顆位元約 10 個參數", "每對位元再加約 10 個", "會漂移，要持續背景重校"] },
        { icon: "fa:FaRobot", tone: "quantum", badge: "25 秒 vs 15 分鐘", head: "DGX Quantum", body: ["OPX1000 ＋ GH200", "往返延遲 < 4 µs", "RL 代理人調好 CZ 閘（廠商宣稱）"] },
        { icon: "fa:FaTrophy", tone: "good", badge: "99.9%／98.5%", head: "Rigetti AI 校準挑戰", body: ["9 位元 Novera", "Quantum Elements、Qruise", "單／雙位元閘保真度"] },
      ],
      callout: "連**解碼器本身的校準**都上 GPU：Riverlane ＋ H100 表面碼每秒 **420 萬**症狀，比單核 CPU 快 71 倍",
      notes:
        "校準是第三個控制層的工作。每顆位元大約十個參數，每對位元再加十個，百萬位元就是千萬級參數，而且會漂移，要持續在背景重新校準。傳統的人工或依賴圖掃描跟不上，開始改用強化學習。Quantum Machines 和 NVIDIA 的 DGX Quantum 把控制器接到 Grace Hopper，往返延遲小於 4 微秒；和中研院的示範中，強化學習代理人約 25 秒調好 CZ 閘，人工要 15 分鐘，這是廠商的數字。Rigetti 的 AI 校準挑戰也達到單位元 99.9%、雙位元 98.5%。連解碼器本身的權重校準都搬到 GPU 上了。",
    },
    {
      type: "flow",
      section: "控制層",
      title: "中性原子重排：GPU 進入即時迴路",
      steps: [
        { head: "① 隨機裝載", body: "光鑷約 50% 機率\n抓到原子", tone: "neutral" },
        { head: "② 拍照判讀", body: "螢光影像\n判斷每格有無原子", tone: "neutral" },
        { head: "③ 指派問題", body: "哪顆搬到哪格\n匈牙利演算法 O(N³)", tone: "warn" },
        { head: "④ 算全像圖", body: "每一步 SLM 全像圖\n或 AOD 多音頻率", tone: "bad" },
        { head: "⑤ 搬移確認", body: "再拍照補洞\n才開始計算", tone: "good" },
      ],
      boxHeight: 2.1,
      bullets: [
        "單顆 GPU 每張全像圖 **0.284 ms**，比 SLM 刷新 0.696 ms 還快（arXiv:2610.21609）",
        "AI 產生全像圖：**1,000～10,000 顆**原子成本幾乎不變，萬顆重排估計 **< 60 ms**（arXiv:2412.14647）",
        "另一條路：全部做進 FPGA，50×50 陣列延遲比 CPU 低約 **54 倍**（arXiv:2411.12401）",
      ],
      notes:
        "中性原子的重排是 GPU 進入即時迴路的典型例子。光鑷隨機裝載，大約一半的格子有原子；拍照判讀；接著解指派問題，決定哪顆原子搬到哪一格；然後算出每一步的全像圖或聲光偏轉器的頻率；搬完再拍照補洞，才能開始計算。陣列從幾百擴到上萬顆，指派問題和全像圖的計算量都很大。最新的研究中，單顆 GPU 算一張全像圖只要 0.284 毫秒，瓶頸反而變成空間光調制器的刷新速度；用 AI 產生全像圖，萬顆原子重排估計 60 毫秒以內。也有團隊選擇全部做進 FPGA。",
    },
    {
      type: "cards",
      section: "控制層",
      title: "最佳控制、離子搬移、光子前饋",
      cards: [
        { icon: "fa:FaChartArea", tone: "quantum", badge: "離線～分鐘", head: "脈衝最佳控制", body: ["GRAPE：反覆算時間演化與梯度", "多能階＋耦合器＋串擾", "GPU 自動微分加速（Leung 2017）"] },
        { icon: "fa:FaRoute", tone: "warn", badge: "毫秒", head: "離子阱 shuttling", body: ["電路 → 移動排程（組合最佳化）", "數十～數百個電極電壓波形", "搬越多次越熱，要最少化"] },
        { icon: "fa:FaBolt", tone: "bad", badge: "最嚴苛", head: "光子前饋", body: ["光子停不下來", "融合結果要在延遲線內決定", "幾乎全靠 FPGA／ASIC"] },
      ],
      notes:
        "控制層還有三項。第一是脈衝最佳控制，用 GRAPE 這類方法在多能階、耦合器和串擾的模型下求出最好的脈衝形狀，要反覆計算時間演化和梯度，GPU 自動微分可以大幅加速。第二是離子阱的搬移，古典端要把電路變成移動排程，再為每一步算出幾十到幾百個電極的電壓波形，而且搬越多次離子越熱，所以要最少化。第三是光子量子電腦，光子停不下來，每一次融合量測的結果要在光子飛過延遲線之前決定下一步，是延遲最嚴苛的平台。",
    },

    // ───────── 即時錯誤更正 ─────────
    {
      type: "cards",
      section: "即時錯誤更正",
      title: "為什麼解碼一定要即時？",
      scene: { prefix: "動畫", label: "表面碼", url: "https://pcpcchen-coder.github.io/QuantumComputing/animations/transmon-3d.html" },
      cards: [
        { icon: "fa:FaSyncAlt", tone: "neutral", badge: "每 ~1 µs", head: "症狀不停產生", body: ["每週期量所有輔助位元", "解碼器推斷發生了什麼錯", "Clifford 閘可以先記帳"] },
        { icon: "fa:FaCodeBranch", tone: "warn", badge: "T 閘、條件分支", head: "必須馬上知道", body: ["魔術態注入要決定補不補 S", "量測後分支要知道目前錯誤", "解不出來就不能往下走"] },
        { icon: "fa:FaHourglassHalf", tone: "bad", badge: "積壓問題", head: "跟不上就爆掉", body: ["解碼速度 < 症狀產生速度", "未處理資料無限堆積", "計算**指數變慢**（Terhal）"] },
      ],
      callout: "粗估：百萬位元、一半是輔助位元 → 每 µs 約 50 萬 bit → **約 0.5 Tb/s，持續不斷**",
      notes:
        "錯誤更正為什麼會是最大的古典負擔？表面碼每一個週期，超導大約一微秒，就要量一次所有輔助位元，得到症狀，解碼器要從症狀推斷發生了什麼錯誤。如果只是 Clifford 閘，可以先記帳最後再修；但遇到 T 閘的魔術態注入、或量測之後的條件分支，就必須馬上知道目前累積了什麼錯誤。如果解碼速度跟不上症狀產生的速度，資料會無限堆積，這就是 Terhal 提出的積壓問題。粗估一下，百萬位元、一半是輔助位元，每微秒就有五十萬個位元，大約每秒 0.5 Tb，而且一刻都不能停。右上角可以開啟表面碼動畫。",
    },
    {
      type: "table",
      section: "即時錯誤更正",
      title: "解碼演算法與適合的硬體",
      headers: ["解碼器", "特性", "適合硬體"],
      colW: [3.6, 5.4, 3.133],
      rows: [
        ["MWPM（PyMatching 等）", "表面碼標準、精度高", "CPU、FPGA"],
        ["Union-Find／Collision Clustering", "近線性時間、可平行", "FPGA、ASIC"],
        ["BP + OSD", "qLDPC 常用，OSD 矩陣消去較重", "GPU"],
        ["Relay-BP（IBM）", "只保留訊息傳遞，硬體精簡", "FPGA"],
        ["神經網路（AlphaQubit 等）", "精度最高，能學真實雜訊，但慢", "GPU／TPU"],
        ["張量網路／最大似然", "最精準、最慢，多用於基準", "GPU"],
      ],
      callout: "趨勢：**內層快速解碼放 FPGA／ASIC**，**外層視窗與 AI 解碼放 GPU**",
      notes:
        "解碼演算法有好幾種。最小權重完美匹配是表面碼的標準做法，精度高，可以在 CPU 或 FPGA 上跑。Union-Find 和 Riverlane 的 Collision Clustering 接近線性時間、可以平行，適合 FPGA 和 ASIC。BP 加 OSD 是 qLDPC 碼常用的，OSD 那一步是矩陣消去，比較重，適合 GPU。IBM 的 Relay-BP 只保留訊息傳遞的部分，可以做進 FPGA。神經網路解碼器精度最高，因為能學到真實雜訊，但推論慢。趨勢是內層快速解碼放 FPGA，外層的視窗解碼和 AI 解碼放 GPU。",
    },
    {
      type: "table",
      section: "即時錯誤更正",
      title: "即時解碼的代表案例",
      headers: ["案例", "硬體與方法", "結果"],
      colW: [3.4, 4.6, 4.133],
      rows: [
        ["Google Willow（2024）", "d=5 表面碼即時解碼，週期 1.1 µs", "平均延遲 63 µs，連續百萬週期"],
        ["Riverlane Deltaflow 2", "同一份 Willow d=5 資料", "平均延遲 16.32 µs"],
        ["Quantinuum Helios（2025）", "GH200 ＋ NVQLink，GPU BP+OSD", "中位數 67 µs，比 2 ms 要求快 32 倍"],
        ["IBM Relay-BP（FPGA）", "[[144,12,12]] gross code，AMD VU19P", "12 週期視窗 < 240 ns"],
        ["QuEra ＋ NVIDIA", "Transformer 解魔術態蒸餾", "< 1 ms；訓練用 42 顆 H100"],
        ["Google AlphaQubit", "Transformer 解碼器", "精度最佳，但仍太慢、無法即時"],
      ],
      notes:
        "看幾個代表案例。Google Willow 在 2024 年的 Nature 論文，距離 5 的表面碼即時解碼，平均延遲 63 微秒，連續跑了一百萬個週期。Riverlane 用同一份資料把延遲降到 16 微秒。Quantinuum 的 Helios 用 NVIDIA GH200 加 NVQLink，在 GPU 上跑 BP 加 OSD，中位數 67 微秒，比 Helios 要求的 2 毫秒快 32 倍，這是 GPU 直接進入量子即時迴路的第一個代表案例。IBM 的 Relay-BP 在 FPGA 上 240 奈秒內解完 12 個週期，但光是一個方向的解碼就用掉最大型 FPGA 一半以上的邏輯。QuEra 和 NVIDIA 的 AI 解碼器小於 1 毫秒，但訓練就用了 42 顆 H100。AlphaQubit 精度最好，但 Google 自己說它還太慢。",
    },
    {
      type: "chart",
      section: "即時錯誤更正",
      title: "解碼延遲 vs 平台容許時間",
      chart: {
        kind: "bar",
        title: "解碼延遲（µs）",
        labels: ["Willow d=5", "Riverlane", "Helios GPU", "IBM FPGA"],
        series: [{ name: "µs", values: [63, 16.32, 67, 0.24], color: "1A9DB0" }],
        yTitle: "µs",
        options: { dataLabelFormatCode: "General" },
      },
      chartWidth: 6.6,
      caption: "IBM＝12 週期視窗平均；Helios＝中位數；Willow、Riverlane＝平均",
      bullets: [
        "超導：週期 **~1 µs**，Gidney 2025 假設反應時間 **10 µs** → GPU 單獨仍偏慢",
        "離子阱：Helios 容許 **2 ms** → GPU 綽綽有餘",
        "**延遲有界**也可以：Willow 的 63 µs ≈ 50 多個週期，只要吞吐量跟得上就不會積壓",
        "IBM 的速度代價：X 方向解碼就用掉 VU19P **一半以上**邏輯資源",
      ],
      notes:
        "把延遲放在一起看。超導的週期大約 1 微秒，Gidney 2025 年的 RSA 估算假設反應時間 10 微秒，所以 GPU 單獨跑還是偏慢，內層要靠 FPGA。離子阱的 Helios 容許 2 毫秒，GPU 綽綽有餘。另外要注意，延遲有界也可以運作，Willow 的 63 微秒大約是 50 多個週期，只要吞吐量跟得上就不會積壓。IBM 的 FPGA 快到 240 奈秒，但代價是硬體資源，解碼器的硬體量會隨邏輯位元數一起長大。",
    },
    {
      type: "cards",
      section: "即時錯誤更正",
      title: "解碼之外的 QEC 古典工作",
      cards: [
        { icon: "fa:FaGraduationCap", tone: "quantum", badge: "GPU 訓練", head: "解碼器訓練", body: ["真實症狀或大量模擬資料", "雜訊漂移後要重訓", "d=3 就要 42 顆 H100"] },
        { icon: "fa:FaDice", tone: "neutral", badge: "數十億次取樣", head: "蒙地卡羅模擬", body: ["設計新碼、評估閾值", "驗證解碼器", "Stim 等工具大量取樣"] },
        { icon: "fa:FaIndustry", tone: "warn", badge: "µs–ms", head: "邏輯層排程", body: ["lattice surgery 路由", "魔術態工廠調度", "依解碼結果補修正"] },
        { icon: "fa:FaExclamationTriangle", tone: "bad", badge: "即時", head: "洩漏與遺失", body: ["transmon 跳到 |2⟩", "中性原子遺失", "觸發 reset 或補原子"] },
      ],
      callout: "**古典解碼與排程的延遲，直接決定量子演算法的總執行時間**",
      notes:
        "錯誤更正除了解碼本身，還有四項古典工作。第一是解碼器訓練，雜訊漂移後還要重訓。第二是大量的蒙地卡羅模擬，用來設計新碼、評估閾值、驗證解碼器。第三是邏輯層的排程：容錯的邏輯閘用 lattice surgery 完成，T 閘要從魔術態工廠取貨，古典控制器要即時決定走哪條路由、用哪個工廠的魔術態、要不要補修正。第四是洩漏與遺失的偵測。重點是：古典解碼和排程的延遲，會直接決定量子演算法的總執行時間。",
    },

    // ───────── 編譯與混合迴圈 ─────────
    {
      type: "cards",
      section: "編譯與混合迴圈",
      title: "QPU 開跑之前：編譯與前處理",
      cards: [
        { icon: "fa:FaCogs", tone: "neutral", badge: "兆級閘數", head: "電路編譯", body: ["分解、映射、SWAP 路由", "Clifford+T 合成", "CFS 法原始約 **2 兆** Toffoli"] },
        { icon: "fa:FaPuzzlePiece", tone: "warn", badge: "可逆電路", head: "Oracle 合成", body: ["Grover 的判斷條件", "Shor 的模指數", "窗口化算術等最佳化"] },
        { icon: "fa:FaFlask", tone: "good", badge: "O(N⁴) 張量", head: "化學前處理", body: ["HF、積分、選活性空間", "DF／THC 張量分解", "DMRG 準備 QPE 初始態"] },
        { icon: "fa:FaMagic", tone: "quantum", badge: "約快 49 倍", head: "AI 生成電路", body: ["NVIDIA GQE：Transformer", "30 位元 CO₂", "48 顆 H100 平行化"] },
      ],
      callout: "化學的關鍵：QPE 成功率取決於初始態重疊 → **古典先算得越好，量子跑得越少**",
      notes:
        "接著看量子處理器開跑之前的工作。第一是電路編譯，容錯演算法的閘數動輒數十億到兆級，Gidney 提到 Chevignard、Fouque、Schrottenloher 的方法原始用了約兩兆個 Toffoli，要靠最佳化才壓到可行。第二是 oracle 合成，把古典函數變成可逆量子電路。第三是化學前處理：Hartree-Fock、積分、選活性空間、張量分解，最後還要用 DMRG 這類方法準備好的初始態。第四是用 AI 生成電路，NVIDIA 的 GQE 用 Transformer 產生電路，30 位元的實驗在單顆 H100 要 173 小時，48 顆平行化縮到 3.5 小時。化學的重點是：古典先算得越好，量子就跑得越少。",
    },
    {
      type: "flow",
      section: "編譯與混合迴圈",
      title: "VQE／QAOA：古典與 QPU 的往返",
      steps: [
        { head: "古典給參數", body: "最佳化器提出\n一組 θ", tone: "neutral" },
        { head: "QPU 執行", body: "參數化電路\n量測數千 shots", tone: "quantum" },
        { head: "古典算期望值", body: "能量與梯度\n參數平移法 ×2 電路", tone: "warn" },
        { head: "更新參數", body: "數百～數千輪\n直到收斂", tone: "good" },
      ],
      boxHeight: 2.1,
      bullets: [
        "單輪古典運算**不重**，但**往返延遲**很關鍵：雲端排隊會讓一輪從秒變成分鐘",
        "因此出現 Qiskit Runtime Session、「QPU 旁邊就放 CPU／GPU」的架構",
        "大規模 QAOA 還要古典端先把問題**切小**（分而治之）",
      ],
      notes:
        "變分演算法是近期最常見的協同模式。古典的最佳化器給一組參數，量子處理器跑參數化電路、量測幾千次，古典端算期望值和梯度，用參數平移法的話每個參數要多跑兩個電路，然後更新參數，重複幾百到幾千輪。單輪的古典運算其實不重，但往返延遲很關鍵，雲端排隊會讓一輪從幾秒變成幾分鐘，所以才會有 Qiskit Runtime Session，以及把 CPU、GPU 直接放在量子處理器旁邊的架構。",
    },
    {
      type: "cards",
      section: "編譯與混合迴圈",
      title: "SQD：一台 QPU 配整台富岳",
      cards: [
        { icon: "fa:FaAtom", tone: "quantum", badge: "QPU", head: "抽樣電子組態", body: ["IBM Heron", "產生大量位元串", "挑出值得算的組態"] },
        { icon: "fa:FaWrench", tone: "warn", badge: "古典", head: "組態回復", body: ["修正雜訊造成的", "粒子數不守恆樣本", "張成子空間"] },
        { icon: "fa:FaServer", tone: "bad", badge: "158,976 節點", head: "超大矩陣對角化", body: ["富岳全機、760 萬核心", "[Fe₂S₂(SH)₄]²⁻", "閉迴路連續協同"] },
      ],
      callout: "IBM ＋ RIKEN（2026/1）：宣稱量子電腦上**最大、最準**的化學計算；下一步加入 GPU（IBM 宣稱）",
      notes:
        "樣本式量子對角化 SQD 是超級電腦加量子處理器的旗艦案例。量子處理器對分子的電子組態抽樣，產生一大堆位元串；古典端先做組態回復，修正雜訊造成粒子數不守恆的樣本；再用這些組態張成子空間，在超級電腦上把哈密頓量對角化。今年一月 IBM 和 RIKEN 用富岳全機，十五萬八千多個節點、七百六十萬核心，和 IBM Heron 閉迴路協同，計算鐵硫簇，宣稱是量子電腦上規模最大、最準的化學計算，下一步要加入 GPU。這個案例裡古典算力遠大於量子端。",
    },
    {
      type: "cards",
      section: "編譯與混合迴圈",
      title: "QC-AFQMC、量子退火、電路切割",
      cards: [
        { icon: "fa:FaVial", tone: "good", badge: "後處理 656×", head: "QC-AFQMC", body: ["IonQ Forte 24 顆位元", "AWS ＋ NVIDIA CUDA-Q", "AstraZeneca 鎳催化反應"] },
        { icon: "fa:FaProjectDiagram", tone: "neutral", badge: "古典前端", head: "D-Wave 混合求解", body: ["古典啟發式探索解空間", "找出難核心、切小送 QPU", "大部分時間在古典端"] },
        { icon: "fa:FaCut", tone: "bad", badge: "指數成長", head: "電路切割／縫合", body: ["大電路切給小 QPU", "每切一刀成本乘一倍數", "GPU 平行重組"] },
      ],
      notes:
        "還有三種混合模式。第一是 QC-AFQMC，量子處理器準備試探波函數，古典端用陰影量測做蒙地卡羅，後處理非常重。IonQ、AWS、NVIDIA 和 AstraZeneca 合作，用 24 顆位元模擬鎳催化反應，GPU 讓後處理的解題時間快了 656 倍。第二是 D-Wave 的混合求解器，古典啟發式探索解空間、找出最難的核心切小送進量子處理器，大部分時間其實花在古典端。第三是電路切割，把大電路切給小的量子處理器跑，再由古典端縫回去，每切一刀成本就乘上一個倍數，總成本隨切割數指數成長。",
    },
    {
      type: "table",
      section: "編譯與混合迴圈",
      title: "誤差緩解：用古典算力換精度",
      headers: ["方法", "古典端在做什麼", "成本特性"],
      colW: [3.0, 5.4, 3.733],
      rows: [
        ["Pauli twirling", "產生成百上千個隨機化等效電路", "編譯量 × 變體數"],
        ["零雜訊外插 ZNE", "放大雜訊分別量測，外插回零", "取樣 × 雜訊等級"],
        ["機率誤差消除 PEC", "學雜訊模型，準機率取樣抵消", "隨電路指數成長"],
        ["張量網路 TEM", "後處理中把雜訊反向作用", "由 bond dimension 決定"],
        ["古典陰影", "隨機量測後重建大量可觀測量", "重建與估計運算"],
      ],
      callout: "IBM 2023 Nature：127 位元、2,880 個 CNOT 用 ZNE；驗證時**古典張量網路在強糾纏區不可靠**",
      notes:
        "完全容錯之前，主流手段是用古典算力換精度。Pauli twirling 要產生成百上千個隨機化的等效電路；零雜訊外插要把雜訊放大成幾個等級分別量測再外插；機率誤差消除要先學雜訊模型，取樣次數隨電路大小指數成長；Algorithmiq 的張量網路誤差緩解把所有工作移到古典後處理；古典陰影則要重建大量可觀測量。IBM 2023 年在 Nature 的量子效用實驗，127 顆位元、2,880 個 CNOT，用的就是零雜訊外插，而驗證時發現古典張量網路在強糾纏區反而不可靠，之後引發一波古典模擬的競賽。",
    },

    // ───────── Shor 專題 ─────────
    {
      type: "flow",
      section: "Shor 專題",
      title: "Shor：古典算力花在哪一段？",
      scene: { prefix: "動畫", label: "Shor 15", url: "https://pcpcchen-coder.github.io/QuantumComputing/animations/shor-15.html" },
      steps: [
        { head: "前處理（輕）", body: "檢查偶數、質數冪\n選 a、gcd(a, N)\n筆電微秒級", tone: "good" },
        { head: "編譯（重，一次）", body: "模指數 → 可逆電路\n數十億 Toffoli\n離線 HPC", tone: "warn" },
        { head: "執行期（極重）", body: "每 µs 解碼\n每個 T 閘補修正\n持續數天", tone: "bad" },
        { head: "後處理（輕～中）", body: "連分數 → 週期 r\ngcd 得因數\nRegev 版用格約化", tone: "neutral" },
      ],
      boxHeight: 2.3,
      bullets: [
        "直覺以為重的是**前處理與後處理**，其實筆電就能完成",
        "真正吃掉大量古典算力的是**執行期間的即時錯誤更正**",
        "編譯雖重，但**只做一次、可以重複使用**",
      ],
      notes:
        "現在專門拆解 Shor。分成四段。前處理：檢查 N 是不是偶數、是不是質數冪，隨機選 a，算 gcd，在筆電上微秒級就完成。編譯：把模指數合成為可逆電路，數十億個 Toffoli，是離線的 HPC 工作，但只做一次。執行期：每一微秒都要解碼，每一個 T 閘都要決定要不要補修正，持續好幾天，這是最重的。後處理：連分數展開得到週期，再用 gcd 得到因數，毫秒級。所以大家直覺以為重的前後處理其實很輕，真正重的是執行期間。右上角可以開啟我們的 Shor 分解 15 動畫，裡面有後處理的逐步範例。",
    },
    {
      type: "equations",
      section: "Shor 專題",
      title: "執行期的古典負擔有多大？",
      eqs: [
        { eq: "5×10^{5} bit/µs ≈ 0.5 Tb/s", label: "約 50 萬顆輔助位元，每 1 µs 量一次（粗估）" },
        { eq: "6×10^{11} 週期，約 37 PB", label: "一週持續運轉 → 累計要即時處理的症狀資料（粗估）" },
        { eq: "反應時間 ≤ 10 µs", label: "每個 T 閘：解碼 → 決定是否補 S 閘" },
      ],
      bullets: [
        "依據：Gidney 2025，**少於 100 萬**顆雜訊位元、**不到一週**分解 RSA-2048",
        "假設 0.1% 閘錯誤率、1 µs 表面碼週期、10 µs 控制反應時間",
        "另外還要：魔術態**培育（cultivation）**的調度、yoked surface code 的外層解碼、**不能停的背景校準**",
        { text: "出處：arXiv:2505.15917", sub: true },
      ],
      notes:
        "執行期到底有多重？以 Gidney 2025 年的估算為準：少於一百萬顆雜訊物理位元，不到一週分解 RSA 2048，假設 0.1% 的閘錯誤率、1 微秒的表面碼週期、10 微秒的控制反應時間。粗估一下，大約五十萬顆輔助位元每微秒量一次，就是每秒 0.5 Tb；一週大約六千億個週期，累計要即時處理大約 37 PB 的症狀資料。每個 T 閘都要在 10 微秒內完成解碼、決定要不要補 S 閘。另外還有魔術態培育的調度、邏輯位元記憶體的外層解碼，以及一週內不能停的背景校準。",
    },

    // ───────── 實例：分解 15，再放大到 RSA-2048 ─────────
    {
      type: "flow",
      section: "Shor 專題",
      title: "實例：分解 15，每一步花多久？",
      scene: { prefix: "動畫", label: "Shor 15", url: "https://pcpcchen-coder.github.io/QuantumComputing/animations/shor-15.html" },
      steps: [
        { head: "① 編譯（古典）", body: "筆電 1 次\n約 0.1–1 秒\n53 個 CNOT → 約 100 個", tone: "neutral" },
        { head: "② QPU 執行", body: "2,000 shots\n每 shot 約 0.5 ms\n共約 1 秒", tone: "quantum" },
        { head: "③ 判讀（FPGA）", body: "6,000 次判別\n每次 < 1 µs\n在 shot 之間完成", tone: "warn" },
        { head: "④ 後處理（古典）", body: "直方圖＋連分數＋gcd\n筆電 < 1 ms", tone: "good" },
        { head: "⑤ 答案", body: "週期 r = 4\n15 = 3 × 5", tone: "good" },
      ],
      boxHeight: 2.3,
      bullets: [
        "每個 shot：運算約 **10 µs**、量測約 1 µs，其餘約 **0.5 ms 都在等位元回到 |0⟩**（等 5 T₁）",
        "交給古典電腦的資料只有 **2,000 × 3 bits = 750 bytes**；今天的 15 沒有錯誤更正，**古典端幾乎不重**",
        { text: "假設：超導、雙位元閘 50–100 ns、被動重置 5 T₁ ≈ 0.5 ms（本 repo transmon-3d 第 12 章）、2,000 shots；理想電路 53 個 CNOT（shor-15.html），加上路由約 100 個（推論）", sub: true },
      ],
      notes:
        "用最小的例子把上一頁變具體：分解 15，a 取 7，電路是 7 顆位元，3 顆計數、4 顆工作，理想電路約 53 個 CNOT，放到真實晶片上加上路由大約 100 個。第一步，古典電腦編譯一次，筆電大約 0.1 到 1 秒。第二步，量子電腦跑 2,000 個 shot，每個 shot 運算本身只要大約 10 微秒、量測 1 微秒，但要等大約 0.5 毫秒讓位元回到 0，所以 2,000 個 shot 大約 1 秒。第三步，FPGA 把每個 shot 的 3 顆計數位元判成 0 或 1，共 6,000 次判別，每次不到 1 微秒。第四步，古典後處理：做直方圖、連分數、gcd，筆電不到 1 毫秒。交給古典電腦的資料只有 750 bytes。結論：今天的 15 沒有錯誤更正，古典端幾乎不重，量子端的時間也大多花在等待。右上角可以開 Shor 15 的逐閘動畫。",
    },
    {
      type: "table",
      section: "Shor 專題",
      title: "分解 15：誰算、幾次、多久、多少資料",
      headers: ["步驟", "誰算", "次數", "時間", "資料量"],
      colW: [2.4, 2.4, 2.6, 2.3, 2.433],
      rows: [
        ["編譯成脈衝", "CPU（筆電）", "1 次", "0.1–1 秒", "電路 → 脈衝時間表"],
        ["跑電路", "QPU", "2,000 shots", "約 1 秒", "—"],
        ["讀取判 0/1", "FPGA", "6,000 次", "每次 < 1 µs", "750 bytes"],
        ["直方圖", "CPU", "1 次", "微秒級", "8 個格子"],
        ["連分數＋驗證", "CPU", "最多 8 次", "微秒級", "得到 r = 4"],
        ["gcd", "CPU", "2 次", "微秒級", "3 和 5"],
      ],
      callout: "比例：QPU 約 **1 秒**、古典後處理 **< 1 ms**；實務上最久的反而是**雲端排隊**（分鐘～小時）",
      notes:
        "把每一步列成表。編譯一次，0.1 到 1 秒。量子電腦跑 2,000 個 shot，約 1 秒，不包含雲端排隊。FPGA 判別 6,000 次，每次不到 1 微秒，產生 750 bytes。古典電腦做一次直方圖，把 2,000 筆結果分到 8 個格子；最多做 8 次連分數加驗證，得到週期 4；最後做 2 次 gcd 得到 3 和 5，全部加起來不到 1 毫秒。所以在今天沒有錯誤更正的小例子裡，量子約 1 秒、古典後處理不到 1 毫秒，實務上最久的反而是雲端排隊。",
    },
    {
      type: "cards",
      section: "Shor 專題",
      title: "750 bytes 怎麼變成 3 × 5？",
      lead: "理想情況下，3 顆計數位元只會量到 **0、2、4、6**，各約 25%（a = 7）",
      cards: [
        { icon: "fa:FaTimesCircle", tone: "bad", badge: "y = 0", head: "0/8 = 0", body: ["沒有資訊", "丟掉"] },
        { icon: "fa:FaCheckCircle", tone: "good", badge: "y = 2", head: "2/8 = 1/4", body: ["猜 r = 4", "7⁴ mod 15 = 1 ✓"] },
        { icon: "fa:FaExclamationCircle", tone: "warn", badge: "y = 4", head: "4/8 = 1/2", body: ["猜 r = 2", "7² mod 15 = 4 ✗"] },
        { icon: "fa:FaCheckCircle", tone: "good", badge: "y = 6", head: "6/8 = 3/4", body: ["猜 r = 4", "7⁴ mod 15 = 1 ✓"] },
      ],
      callout: "r = 4 → gcd(7² − 1, 15) = gcd(48, 15) = **3**；gcd(7² + 1, 15) = gcd(50, 15) = **5**；約一半的 shot 有用",
      notes:
        "750 bytes 怎麼變成答案？理想情況下，3 顆計數位元只會量到 0、2、4、6，各大約 25%。量到 0，相位是 0，沒有資訊，丟掉。量到 2，2/8 等於 1/4，猜週期是 4，驗證 7 的 4 次方除以 15 餘 1，成立。量到 4，4/8 等於 1/2，猜週期是 2，但 7 的平方除以 15 餘 4，不成立，丟掉。量到 6，6/8 等於 3/4，同樣得到週期 4。有了週期 4，gcd(48, 15) 等於 3，gcd(50, 15) 等於 5。大約一半的 shot 有用；真實硬體有雜訊，其他值也會出現，所以才要跑 2,000 次看直方圖。要提醒的是，目前實驗分解 15 多半用精簡版電路，是先知道答案結構才簡化的，shor-15 動畫頁的 3.6 節有說明。",
    },
    {
      type: "table",
      section: "Shor 專題",
      title: "放大：15 → 容錯版 15 → RSA-2048",
      headers: ["項目", "15（今天）", "15（容錯版，假想）", "RSA-2048"],
      colW: [2.6, 2.7, 3.2, 3.633],
      rows: [
        ["實體位元", "7", "約 1,500", "< 100 萬"],
        ["每次執行", "約 0.5 ms", "約 1 ms", "數天"],
        ["執行次數", "2,000 shots", "約 10 次", "1～少數幾次"],
        ["QPU 總時間", "約 1 秒", "約 10 ms", "< 1 週"],
        ["即時交給古典", "0（只判 0/1）", "約 1 MB 症狀", "約 37 PB 症狀"],
        ["即時解碼", "0", "約 1 萬輪", "約 6×10¹¹ 輪 × 上千區塊"],
        ["最後結果", "750 bytes", "30 bits", "幾 kB"],
        ["後處理", "< 1 ms", "< 1 ms", "秒～分鐘（推論）"],
      ],
      notes:
        "現在放大。第一欄是今天的 15，剛剛算過。第二欄是假想：如果 15 也用錯誤更正跑，表面碼距離 7、週期 1 微秒，7 個邏輯位元加上路由和魔術態工廠，大約 1,500 顆實體位元；每次執行大約 100 個邏輯步驟乘 7 微秒，約 1 毫秒；理想的 Shor 只要跑幾次，取 10 次。這時候每一微秒有大約 750 個症狀位元要即時解碼，10 次加起來大約 1 MB、1 萬輪解碼，但最後結果只有 30 bits。第三欄是 RSA 2048，依 Gidney 2025：不到一百萬顆實體位元、不到一週，即時症狀資料大約 37 PB，每個邏輯區塊都要解碼，上千個區塊同時進行大約六千億輪；最後結果只有幾 kB，後處理用格的方法或連分數，一般電腦秒到分鐘，這是我的推論。容錯版 15 的數字是我依假設粗估的。",
    },
    {
      type: "equations",
      section: "Shor 專題",
      title: "放大後的比例：古典算力長在哪裡？",
      eqs: [
        { eq: "位元：7、1,500、10^{6}", label: "今天的 15 → 容錯版 15 → RSA-2048，放大約 14 萬倍" },
        { eq: "即時資料：0、1 MB、37 PB", label: "從沒有 → 長到數十 PB（粗估）" },
        { eq: "即時資料：結果 ＝ 0、2.5×10^{5}、10^{13}", label: "三種情況的比例；結果始終只有幾 kB" },
      ],
      bullets: [
        "**結果資料**幾乎不變：750 bytes → 30 bits → 幾 kB",
        "**後處理**只從 < 1 ms 長到秒～分鐘",
        "**QPU 時間**從 1 秒長到 1 週",
        "**長大的幾乎全是即時解碼**：從 0 長到每秒 0.5 Tb、持續一週",
        { text: "假想容錯版：d = 7、週期 1 µs、物理錯誤 0.1%、約 1,500 實體位元、10 次執行（粗估）；RSA-2048：Gidney 2025", sub: true },
      ],
      notes:
        "把比例抽出來看。位元數從 7 到 1,500 到一百萬，放大大約十四萬倍。即時交給古典的資料從 0 到 1 MB 到 37 PB。即時資料和最後結果的比例，從 0、到二十五萬比一、到十的十三次方比一。反過來看：最後結果始終只有幾 kB；後處理只從不到 1 毫秒長到秒到分鐘；量子時間從 1 秒長到 1 週。長大的幾乎全是即時解碼。這就是為什麼前面說，容錯時代古典算力最大的工作不是幫忙算題目，而是讓量子電腦活著。",
    },
    {
      type: "cards",
      section: "Shor 專題",
      title: "換成負載：一週不停的解碼機房",
      cards: [
        { icon: "fa:FaServer", tone: "warn", badge: "0.25–0.6 MW", head: "解碼層功率", body: ["8×H200 伺服器約 11–12 kW", "可支援數萬實體位元（OCP）", "百萬位元需 20–50 台（粗估）"] },
        { icon: "fa:FaBolt", tone: "neutral", badge: "42–100 MWh", head: "一週的電", body: ["0.25–0.6 MW × 168 小時", "不是尖峰", "是**穩定的大負載**"] },
        { icon: "fa:FaShieldAlt", tone: "bad", badge: "零中斷", head: "不能停", body: ["任何一刻跟不上就積壓", "斷電＝一週白跑", "要 **T0 等級**備援"] },
      ],
      callout: "對比分解 15：一台筆電、1 秒；RSA-2048：**一排解碼機櫃不停跑一週，而且一秒都不能斷**",
      notes:
        "最後把它換成負載，接到電力的討論。OCP 白皮書舉例，一台 8 顆 H200 的伺服器大約 11 到 12 kW，搭配 FPGA 可以支援數萬顆實體位元的錯誤更正。百萬位元粗估需要 20 到 50 台，解碼層就是 0.25 到 0.6 MW。持續一週，大約 42 到 100 MWh。這不是 AI 訓練那種尖峰擺盪，而是穩定的大負載；更關鍵的是不能停，任何一刻跟不上就會積壓，斷電就等於一週白跑，所以解碼機櫃要 T0 等級備援。對比分解 15：一台筆電、1 秒；RSA 2048：一排解碼機櫃不停跑一週，而且一秒都不能斷。",
    },
    {
      type: "cards",
      section: "Shor 專題",
      title: "後處理的三種版本",
      cards: [
        { icon: "fa:FaCalculator", tone: "good", badge: "毫秒", head: "原版 Shor", body: ["量測值 → 連分數展開", "得到週期 r", "gcd(a^{r/2} ± 1, N)"] },
        { icon: "fa:FaThLarge", tone: "neutral", badge: "一般電腦", head: "Ekerå–Håstad", body: ["改用格的方法", "後處理稍重", "換得量子電路變短"] },
        { icon: "fa:FaBorderAll", tone: "warn", badge: "格基約化", head: "Regev（2023）", body: ["電路跑約 √n 次", "LLL 類演算法、多項式時間", "電路更短 → 可能指數時間"] },
      ],
      callout: "典型取捨：**用古典後處理，換量子資源**（Ragavan–Vaikuntanathan、Ekerå–Gärtner 進一步容錯）",
      notes:
        "後處理有三種版本。原版 Shor 用連分數展開得到週期，再用 gcd 得到因數，毫秒級。Ekerå 和 Håstad 的變體改用格的方法，後處理稍微重一點，但量子電路變短。Regev 在 2023 年提出的演算法，電路跑大約根號 n 次，後處理用格基約化，多項式時間可以完成；如果再進一步縮短電路，後處理可能要解困難的格問題，變成指數時間。這是典型的取捨：用古典後處理換量子資源。",
    },
    {
      type: "cards",
      section: "Shor 專題",
      title: "其他演算法的對照",
      cards: [
        { icon: "fa:FaSearch", tone: "warn", badge: "平方加速", head: "Grover", body: ["前：oracle 合成", "中：同樣是 QEC 主導", "後：驗證答案很輕", "QEC 常數開銷大 → 贏 GPU 的範圍窄"] },
        { icon: "fa:FaSquareRootAlt", tone: "bad", badge: "讀寫瓶頸", head: "HHL 線性系統", body: ["狀態準備（載入資料）", "讀出整個解要指數次量測", "常把速度優勢吃掉"] },
        { icon: "fa:FaNetworkWired", tone: "quantum", badge: "GPU 為主", head: "量子機器學習", body: ["資料編碼", "核矩陣計算", "古典陰影後處理"] },
      ],
      notes:
        "其他演算法也可以用同樣的框架看。Grover 的前處理是 oracle 合成，執行期同樣是錯誤更正主導，後處理只是驗證答案。由於 Grover 只有平方加速，而錯誤更正和古典控制的常數開銷很大，實務上能贏過 GPU 暴力搜尋的範圍非常窄。HHL 的瓶頸在資料載入和讀出。量子機器學習的資料編碼、核矩陣和陰影後處理都是 GPU 的工作。",
    },

    // ───────── 資料中心啟示 ─────────
    {
      type: "cards",
      section: "資料中心啟示",
      title: "用超級電腦檢查量子電腦",
      cards: [
        { icon: "fa:FaRandom", tone: "quantum", badge: "四台超級電腦", head: "認證隨機數", body: ["Quantinuum H2 56 位元", "Frontier、Summit、Polaris、Perlmutter", "認證 71,313 bits 熵"] },
        { icon: "fa:FaSatelliteDish", tone: "warn", badge: "2.1 h vs 3.2 年", head: "Quantum Echoes", body: ["Willow 65 位元 OTOC", "估計 Frontier 要 3.2 年", "40 位元 GPU 要數天"] },
        { icon: "fa:FaCopy", tone: "neutral", badge: "數百 GB～數十 TB", head: "數位孿生與除錯", body: ["GPU 狀態向量模擬", "30–40 位元先跑一遍", "上線前的標準步驟"] },
      ],
      callout: "認證隨機數這類應用中，**古典驗證算力是產品本身的一部分**",
      notes:
        "量子電腦宣稱古典做不到的時候，需要最強的古典電腦來證明它。Quantinuum 和 JPMorgan 的認證隨機數實驗，用 56 位元的 H2 跑隨機電路，驗證動用了 Frontier、Summit、Polaris、Perlmutter 四台超級電腦，最後認證 71,313 位元的熵。Google 的 Quantum Echoes 在 Willow 上 65 顆位元每組資料約 2.1 小時，估計 Frontier 要 3.2 年，40 位元的版本 GPU 也要數天。另外，每個量子程式上線前，用 GPU 模擬器先跑一遍也是標準步驟。在認證隨機數這類應用中，古典驗證算力本身就是產品的一部分。",
    },
    {
      type: "cards",
      section: "資料中心啟示",
      title: "整合：互連、排程、硬體設計",
      cards: [
        { icon: "fa:FaLink", tone: "bad", badge: "< 4 µs、400 Gb/s", head: "NVIDIA NVQLink", body: ["FPGA → GPU → FPGA", "乙太網路 RDMA", "17 家 QPU、5 家控制廠商"] },
        { icon: "fa:FaTasks", tone: "neutral", badge: "Slurm GRES", head: "工作排程", body: ["QPU 當成可排程資源", "EuroHPC 六平台整合", "IBM × AMD 合作"] },
        { icon: "fa:FaDraftingCompass", tone: "good", badge: "14 億自由度", head: "晶片電磁模擬", body: ["AWS Palace 有限元", "12,800 顆 Graviton2 核心", "萃取電容、耦合、Purcell"] },
      ],
      notes:
        "資料中心層級的整合有三件事。第一是低延遲互連，NVIDIA 的 NVQLink 宣稱 FPGA 到 GPU 再回 FPGA 小於 4 微秒、每秒 400 Gb，已經有 17 家量子處理器廠商和 5 家控制系統廠商支援。第二是工作排程，把量子處理器註冊成 Slurm 的通用資源，讓混合工作和一般 HPC 工作一起排程，歐洲有六個平台在統一介面，IBM 也和 AMD 合作整合 CPU、GPU、FPGA。第三是硬體設計本身，AWS 的 Palace 曾用 12,800 顆核心跑 14 億自由度的晶片電磁模擬。",
    },
    {
      type: "table",
      section: "資料中心啟示",
      title: "各平台的古典即時預算",
      headers: ["平台", "週期／閘時間", "即時反應窗", "GPU 能直接進即時迴路？"],
      colW: [2.6, 2.6, 2.4, 4.533],
      rows: [
        ["超導", "~1 µs", "~10 µs", "內層需 FPGA／ASIC；GPU 做外層視窗解碼"],
        ["離子阱", "數十 µs～ms", "~2 ms", "可以：GH200 ＋ NVQLink 67 µs"],
        ["中性原子", "閘 µs、讀取 ms", "ms", "可以：重排、AI 解碼 < 1 ms"],
        ["光子", "ns（飛行時間）", "極短", "幾乎全靠 FPGA／ASIC"],
      ],
      callout: "平台越慢，GPU 越容易進入即時迴路；**超導與光子仍以 FPGA／ASIC 為核心**",
      notes:
        "四種平台放在一起比較。超導週期大約 1 微秒、反應窗大約 10 微秒，內層必須 FPGA 或 ASIC，GPU 做外層。離子阱反應窗 2 毫秒，GPU 已經可以直接進即時迴路，Helios 就是案例。中性原子是毫秒級，重排和 AI 解碼都已經小於 1 毫秒。光子最嚴苛，幾乎全靠 FPGA 和 ASIC。結論是平台越慢，GPU 越容易進入即時迴路。",
    },
    {
      type: "cards",
      section: "資料中心啟示",
      title: "對資料中心規劃的啟示",
      cards: [
        { icon: "fa:FaMapMarkerAlt", tone: "bad", badge: "公尺級", head: "GPU 放 QPU 旁", body: ["µs 延遲不能走一般網路", "專用互連", "同機房、同排"] },
        { icon: "fa:FaBalanceScale", tone: "warn", badge: "高配比", head: "QPU 配一排機櫃", body: ["富岳全機配一台 Heron", "0.5 Tb/s 持續解碼", "FPGA＋GPU＋CPU 分層"] },
        { icon: "fa:FaPlug", tone: "good", badge: "新應用場景", head: "供電與雜訊", body: ["GPU 機櫃數十 kW", "雜訊與地迴路干擾 QPU", "**量子等級電源的新市場**"] },
        { icon: "fa:FaCode", tone: "neutral", badge: "開放介面", head: "軟體堆疊", body: ["CUDA-Q", "Qiskit Runtime／Functions", "Slurm GRES"] },
      ],
      callout: "「QPU 旁的 GPU 機櫃」要**高功率**、又要**低傳導與輻射雜訊**，還要和 QPU **共地或隔離**",
      notes:
        "最後是對資料中心規劃的四點啟示。第一，GPU 要放在量子處理器旁邊，微秒級延遲不能走一般網路。第二，古典算力的配比很高，規劃時要假設一台量子處理器配一整排機櫃。第三，供電與雜訊：GPU 機櫃是數十 kW 的負載，會產生電磁雜訊和地迴路，要和量子處理器的低雜訊電源、接地系統一起設計，這對我們的量子等級電源產品是一個新的應用場景，可以和之前的 1,000 位元供電設計報告連起來看。第四，軟體堆疊要選支援 CUDA-Q、Qiskit、Slurm 這些開放介面的硬體。",
    },
    {
      type: "summary",
      section: "資料中心啟示",
      title: "重點整理",
      points: [
        "**五層時間尺度**：ns 靠 FPGA、µs 靠 FPGA＋GPU、ms–s 靠 GPU、分鐘以上靠 HPC",
        "**控制 RF**：即時輸出靠 FPGA；CPU／GPU 負責波形設計、校準（AI 代理人）、編譯排程",
        "**即時錯誤更正是最大負擔**：Willow 63 µs、Helios GPU 67 µs、IBM FPGA 240 ns",
        "**Shor 的古典算力花在執行期**：持續 0.5 Tb/s 解碼、每個 T 閘 10 µs 內補修正",
        "**近期混合應用古典端遠大於量子端**：SQD × 富岳、QC-AFQMC、誤差緩解、驗證",
      ],
      notes:
        "整理一下今天的重點。第一，五層時間尺度決定了誰來做。第二，控制 RF 的即時輸出靠 FPGA，CPU 和 GPU 負責波形設計、校準和編譯。第三，即時錯誤更正是最大的古典負擔。第四，Shor 的古典算力花在執行期，不在前後處理。第五，近期的混合應用中，古典端的算力往往遠大於量子端。",
    },
    {
      type: "closing",
      section: "資料中心啟示",
      title: "討論與延伸",
      question: "如果我們要為量子資料中心提供供電方案，「QPU 旁的 GPU 機櫃」該怎麼設計？",
      prompts: [
        "數十 kW 的 GPU 負載，如何不把雜訊傳到 QPU 的偏壓與讀取鏈？",
        "共地還是隔離？光纖互連能不能切斷地迴路？",
        "解碼器斷電等於計算失敗：UPS 要涵蓋到哪一層？",
        "超導、離子阱、中性原子的需求差在哪裡？",
      ],
      refsHead: "延伸閱讀與資料來源",
      refs: [
        "書面報告：docs/QPU與CPU-GPU協同運算需求調查.md（完整出處）",
        "表面碼、lattice surgery、軟體堆疊：animations/transmon-3d.html 第 10–12 章",
        "Shor 分解 15 後處理：animations/shor-15.html",
        "Google Willow, Nature (2024)；Quantinuum Helios ＋ NVQLink (2025)",
        "IBM Relay-BP FPGA, arXiv:2510.21600；Gidney, arXiv:2505.15917",
        "IBM ＋ RIKEN 富岳 SQD (2026)；QC-AFQMC, arXiv:2506.22408",
      ],
      notes:
        "最後留一個討論題，和我們的本業連起來：如果要為量子資料中心提供供電方案，量子處理器旁邊的 GPU 機櫃該怎麼設計？幾十 kW 的負載怎麼不把雜訊傳到量子處理器？共地還是隔離？解碼器斷電就等於計算失敗，UPS 要涵蓋到哪一層？三種平台的需求又差在哪裡？右邊列了延伸閱讀，完整的出處都在書面報告裡。謝謝大家。",
    },
  ],
};
