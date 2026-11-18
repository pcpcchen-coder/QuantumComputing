/*
 * 六個基礎量子電路：疊加、干涉、Bell 態、GHZ 態、Deutsch、Bernstein–Vazirani
 *
 * 對應互動動畫：animations/basic-circuits.html（每個範例有自己的網址錨點）
 *   #superposition  #interference  #bell  #ghz  #deutsch  #bv
 * 每個範例頁右上角的「▶ 動畫」按鈕直接開到該範例。截圖以 node slides/capture_basic_circuits.js 重新擷取。
 *
 * 位元順序和 Qiskit、動畫頁相同：電路圖 q0 在最上面，位元字串 q0 在最右邊（|01⟩ = q1 為 0、q0 為 1）。
 * 振幅長條的數值都和動畫頁的模擬器、Qiskit Statevector 一致（見 slides/README.md 的檢查指令）。
 *
 * 產生：cd slides && node build_deck.js reports/basic-circuits.js
 */

const BC = "https://pcpcchen-coder.github.io/QuantumComputing/animations/basic-circuits.html";
const S = {
  sup: { label: "疊加", url: `${BC}#superposition`, prefix: "動畫" },
  intf: { label: "干涉", url: `${BC}#interference`, prefix: "動畫" },
  bell: { label: "Bell 態", url: `${BC}#bell`, prefix: "動畫" },
  ghz: { label: "GHZ 態", url: `${BC}#ghz`, prefix: "動畫" },
  deu: { label: "Deutsch", url: `${BC}#deutsch`, prefix: "動畫" },
  bv: { label: "BV", url: `${BC}#bv`, prefix: "動畫" },
};
const R2 = Math.SQRT1_2;
const Q = R2 / 2; // 1/(2√2)
const K1 = ["|0⟩", "|1⟩"];
const K2 = ["|00⟩", "|01⟩", "|10⟩", "|11⟩"];
const K3 = ["000", "001", "010", "011", "100", "101", "110", "111"];

module.exports = {
  meta: {
    title: "六個基礎量子電路",
    subject: "量子電路入門：疊加、干涉、Bell 態、GHZ 態、Deutsch、Bernstein–Vazirani",
    series: "量子計算學習筆記｜量子電路入門",
    footer: "六個基礎量子電路",
    output: "basic-circuits.pptx",
  },
  slides: [
    // ───────────── 開場 ─────────────
    {
      type: "title",
      section: "開場",
      kicker: "量子計算學習筆記｜量子電路入門",
      title: "六個基礎\n量子電路",
      subtitle: "從一顆位元的疊加，一路做到「查詢一次就猜中密碼」",
      meta: [
        "疊加 → 干涉 → Bell 態 → GHZ 態 → Deutsch 演算法 → Bernstein–Vazirani 演算法",
        "互動動畫：animations/basic-circuits.html（每個範例都能逐步播放、實際量測 1,000 次）",
      ],
      notes:
        "今天用六個最基本的量子電路，帶大家走一遍量子計算的核心概念。前兩個只用一顆位元，講疊加和干涉；中間兩個講糾纏；最後兩個是真正的量子演算法，Deutsch 和 Bernstein–Vazirani，它們都只要查詢一次就能得到答案。每一個範例右上角都有一顆「動畫」按鈕，點下去會直接開到互動動畫的那個範例，可以一步一步播放、自己量測。",
    },
    {
      type: "agenda",
      section: "開場",
      title: "六個範例，由淺到深",
      items: [
        { head: "疊加", body: "H 閘把確定的 |0⟩ 變成 **50/50** 的量子硬幣", time: "1 顆位元" },
        { head: "干涉", body: "H‑Z‑H = X：看不到的**正負號**變成看得到的結果", time: "1 顆位元" },
        { head: "Bell 態", body: "H + CNOT：兩顆位元**糾纏**，結果永遠一致", time: "2 顆位元" },
        { head: "GHZ 態", body: "CNOT 串下去：**n 顆**位元一起糾纏", time: "3–4 顆位元" },
        { head: "Deutsch", body: "查詢**一次**分辨常數或平衡函數", time: "2 顆位元" },
        { head: "Bernstein–Vazirani", body: "查詢**一次**讀出整串密碼", time: "4 顆位元" },
      ],
      notes:
        "這是今天的路線。前兩個範例只有一顆位元，先建立兩個觀念：疊加和干涉。第三、第四個加進第二顆以上的位元，講糾纏。最後兩個是演算法，會把前面學到的疊加、干涉、相位全部用上。右上角的小字是每個範例用到幾顆位元。",
    },
    {
      type: "cards",
      section: "開場",
      title: "讀圖之前：三個約定",
      cards: [
        { icon: "md:MdFormatListNumbered", tone: "neutral", badge: "位元順序", head: "q0 寫在最右邊", body: ["電路圖：q0 在**最上面**", "位元字串：q0 在**最右邊**，和 Qiskit 相同", "例：|01⟩ 代表 q1 = 0、q0 = 1"] },
        { icon: "md:MdBarChart", tone: "warn", badge: "振幅", head: "長條有正有負", body: ["每個結果有一個**振幅**，可以是負的", "機率 = 振幅^{2}，所以**負號量不到**", "簡報裡金色是正、紅色是負"] },
        { icon: "md:MdTouchApp", tone: "quantum", badge: "互動動畫", head: "每個範例都能自己玩", body: ["右上角 **▶ 動畫** 直接開到該範例", "逐步播放、量測 1,000 次", "附可直接執行的 Qiskit 程式碼"] },
      ],
      notes:
        "開始之前先講三個約定。第一，位元順序：電路圖上 q0 在最上面，但是寫成位元字串的時候 q0 在最右邊，這是 Qiskit 的習慣，所以 |01⟩ 是 q1 等於 0、q0 等於 1。第二，振幅：每一種可能的結果都有一個振幅，振幅可以是負的，機率是振幅的平方，所以負號本身量不到，但它會影響後面的干涉，這是今天最重要的觀念。簡報裡的振幅長條金色是正、紅色是負。第三，每個範例都有對應的互動動畫，可以自己操作。",
    },
    {
      type: "table",
      section: "開場",
      title: "今天用到的四種閘",
      headers: ["閘", "名稱", "作用", "在 Bloch 球上"],
      rows: [
        ["H", "Hadamard", "|0⟩ → (|0⟩ + |1⟩)/√2，|1⟩ → (|0⟩ − |1⟩)/√2", "繞 x、z 中間的斜軸轉 180°"],
        ["X", "NOT", "|0⟩ ↔ |1⟩", "繞 x 軸轉 180°"],
        ["Z", "相位翻轉", "|0⟩ 不變，|1⟩ → −|1⟩", "繞 z 軸轉 180°"],
        ["CNOT", "控制 NOT", "控制位元是 1 時，翻轉目標位元", "兩位元閘，用來產生糾纏"],
      ],
      colW: [1.3, 1.9, 5.53, 3.4],
      callout: "只靠這四種閘，就能做出今天全部六個電路",
      notes:
        "今天只會用到四種閘。H 是 Hadamard，把 |0⟩ 變成 0 和 1 的等量疊加，把 |1⟩ 變成帶負號的疊加。X 是量子版的 NOT，把 0 和 1 對調。Z 是相位翻轉，|0⟩ 不變、|1⟩ 多一個負號。單位元閘都可以想成在 Bloch 球上轉 180 度，只是轉軸不同。CNOT 是兩位元閘：控制位元是 1 的時候，才翻轉目標位元。只用這四種閘，就能做出今天全部六個電路。",
    },

    // ───────────── 1. 疊加 ─────────────
    {
      type: "circuit",
      section: "1. 疊加",
      title: "範例 1｜疊加：量子硬幣",
      scene: S.sup,
      circuitHeight: 1.75,
      circuit: {
        wires: ["q0  |0⟩"],
        cols: [{ g: ["H"] }, { m: [true] }],
        marks: [{ after: -1, label: "①" }, { after: 0, label: "②" }, { after: 1, label: "③" }],
      },
      stages: [
        { head: "① 起點", eq: "|0⟩", body: "振幅 = 1：量測**一定**得到 0。Bloch 向量指向北極", tone: "neutral" },
        { head: "② H 閘", eq: "(|0⟩ + |1⟩)/√2 = |+⟩", body: "兩個振幅都是 +0.707，平方後**各 50%**。向量轉到赤道 +x", tone: "quantum" },
        { head: "③ 量測", eq: "0 或 1，各 50%", body: "量測時才隨機決定，狀態就此**塌縮**；重複 1,000 次約各 500 次", tone: "good" },
      ],
      callout: "量測之前兩種可能**同時存在**：這不是「我們不知道」，而是兩個振幅都在，之後還能互相干涉",
      notes:
        "第一個範例是疊加，只有一個 H 閘。起點是 |0⟩，振幅是 1，量測一定得到 0。經過 H 之後變成 |0⟩ 加 |1⟩ 除以根號 2，叫做 |+⟩，兩個振幅都是 0.707，平方之後各 50%。量測的時候才隨機決定結果，像丟一枚公平的硬幣。要注意，量測之前兩種可能是同時存在的，不只是我們不知道而已，因為兩個振幅之後還可以互相干涉，這在下一個範例就會看到。動畫裡可以按「量測 1,000 次」，結果大約各 500 次。",
    },
    {
      type: "amps",
      section: "1. 疊加",
      title: "|+⟩ 和 |−⟩：機率一樣，差在正負號",
      scene: S.sup,
      lead: "起始態換成 |1⟩（先加一個 X），H 之後的振幅多了一個負號",
      labels: K1,
      panels: [
        { head: "起點 |0⟩", amps: [1, 0], note: "量測一定得到 0" },
        { head: "H|0⟩ = |+⟩", amps: [R2, R2], note: "兩個都是 +0.707：機率各 50%", tone: "quantum", focus: true },
        { head: "起點 |1⟩", amps: [0, 1], note: "量測一定得到 1" },
        { head: "H|1⟩ = |−⟩", amps: [R2, -R2], note: "|1⟩ 的振幅是 **−0.707**：機率仍各 50%", tone: "quantum", focus: true },
      ],
      callout: "量測分不出 |+⟩ 和 |−⟩：機率 = 振幅^{2}，負號在平方後消失。但這個負號**會影響下一步**",
      notes:
        "動畫裡可以把起始態切換成 |1⟩，等於先加一個 X 閘。比較這四張圖：|0⟩ 經過 H 變成 |+⟩，兩根長條都是正的；|1⟩ 經過 H 變成 |−⟩，|1⟩ 那根變成負的。可是機率都是振幅的平方，所以 |+⟩ 和 |−⟩ 量起來完全一樣，都是 50 比 50。這個看不到的負號就是所謂的相位，它雖然量不到，卻會改變後面干涉的結果。",
    },

    // ───────────── 2. 干涉 ─────────────
    {
      type: "circuit",
      section: "2. 干涉",
      title: "範例 2｜干涉：H‑Z‑H = X",
      scene: S.intf,
      circuitHeight: 1.75,
      circuit: {
        wires: ["q0  |0⟩"],
        cols: [{ g: ["H"] }, { g: ["Z"] }, { g: ["H"] }, { m: [true] }],
        marks: [{ after: 0, label: "①" }, { after: 1, label: "②" }, { after: 2, label: "③" }],
      },
      stages: [
        { head: "① 第一個 H", eq: "|+⟩", body: "做出疊加：位元同時走「0」和「1」兩條路徑", tone: "neutral" },
        { head: "② Z 閘", eq: "|−⟩ = (|0⟩ − |1⟩)/√2", body: "只給 |1⟩ 加負號。機率**仍是各 50%**，這一步量不出差別", tone: "quantum" },
        { head: "③ 第二個 H", eq: "|1⟩", body: "兩條路徑重新混合：到 |0⟩ 的互相**抵消**，到 |1⟩ 的互相**加強**", tone: "good" },
      ],
      callout: "拿掉中間的 Z：H·H 什麼都沒做，結果回到 100% 的 0。只差一個看不到的負號，結果就完全相反",
      notes:
        "第二個範例在兩個 H 中間夾一個 Z。第一個 H 做出疊加，第二步 Z 只給 |1⟩ 加一個負號，從 |+⟩ 變成 |−⟩，這時候量測，機率還是各 50%，完全看不出差別。但是第三步再做一次 H，結果變成 100% 的 1。如果把中間的 Z 拿掉，兩個 H 互相抵消，結果是 100% 的 0。只差一個量不到的負號，最後的結果就完全相反，這就是干涉。動畫裡可以切換有沒有 Z 來比較。",
    },
    {
      type: "amps",
      section: "2. 干涉",
      title: "振幅逐步看：負號怎麼變成結果",
      scene: S.intf,
      labels: K1,
      panels: [
        { head: "① H 之後", amps: [R2, R2], note: "|+⟩：兩條路徑都是正的" },
        { head: "② Z 之後", amps: [R2, -R2], note: "|−⟩：|1⟩ 變號，機率仍各 50%", tone: "quantum", focus: true },
        { head: "③ 第二個 H", amps: [0, 1], note: "100% 量到 **1**：H·Z·H = X", tone: "good", focus: true },
        { head: "對照：沒有 Z", amps: [1, 0], note: "H·H = I：100% 量到 **0**" },
      ],
      callout: "② 和 ① 的機率完全相同，差別只在正負號；③ 的 H 把正負號「翻譯」成 0 或 1",
      notes:
        "把振幅一步一步畫出來。第一步 H 之後兩根都是正的。第二步 Z 之後，|1⟩ 那根變成負的，但長度沒變，所以機率一樣。第三步再一個 H，|0⟩ 的長條消失、|1⟩ 的長條變成 1，所以 100% 量到 1。最右邊是對照組：沒有 Z 的話，第二個 H 會把狀態帶回 |0⟩。重點是第二張和第一張的機率完全相同，最後一個 H 把正負號翻譯成 0 或 1。",
    },
    {
      type: "equations",
      section: "2. 干涉",
      title: "路徑加總：為什麼會抵消",
      scene: S.intf,
      eqs: [
        { eq: "到 |0⟩：(+½) + (−½) = 0", label: "從 |−⟩ 做 H：兩條路徑正負相反，互相抵消（破壞性干涉）" },
        { eq: "到 |1⟩：(+½) + (+½) = 1", label: "從 |−⟩ 做 H：兩條路徑同號，互相加強（建設性干涉）" },
        { eq: "沒有 Z：½ + ½ = 1，½ − ½ = 0", label: "從 |+⟩ 做 H：到 |0⟩ 加強、到 |1⟩ 抵消，所以 H·H = I" },
      ],
      bullets: [
        "量子力學裡，每一條路徑都帶一個**振幅**，最後把同一個結果的振幅**相加**",
        "振幅有正有負，所以相加時可以**互相抵消**，這是古典機率做不到的",
        "量子演算法的套路：**先疊加**，讓答案以**正負號**做記號，再用**干涉**讀出來",
        "後面的 Deutsch 和 BV 都是這個套路",
      ],
      notes:
        "為什麼會抵消？可以用路徑加總來算。從 |−⟩ 出發做 H，到 |0⟩ 有兩條路徑：一條從 |0⟩ 來，振幅正二分之一，一條從 |1⟩ 來，振幅負二分之一，加起來是 0。到 |1⟩ 的兩條路徑都是正二分之一，加起來是 1。古典機率只會相加、不會抵消，振幅有正負號才會抵消，這是量子計算能加速的關鍵。量子演算法的共同套路就是：先疊加、用正負號做記號、再用干涉讀出來。",
    },

    // ───────────── 3. Bell 態 ─────────────
    {
      type: "circuit",
      section: "3. Bell 態",
      title: "範例 3｜Bell 態：兩顆位元糾纏",
      scene: S.bell,
      circuitHeight: 2.3,
      circuit: {
        wires: ["q0  |0⟩", "q1  |0⟩"],
        cols: [{ g: ["H", null] }, { cx: [0, 1] }, { m: [true, true] }],
        marks: [{ after: -1, label: "①" }, { after: 0, label: "②" }, { after: 1, label: "③" }],
      },
      stages: [
        { head: "① 起點", eq: "|00⟩", body: "兩顆位元都在 0", tone: "neutral" },
        { head: "② H 閘（q0）", eq: "(|00⟩ + |01⟩)/√2", body: "q0 進入疊加；q1 還沒參與，兩顆位元**互不相干**", tone: "neutral" },
        { head: "③ CNOT（q0 → q1）", eq: "(|00⟩ + |11⟩)/√2", body: "q0 是 1 的那一半，q1 也翻成 1。兩顆的結果**永遠相同**", tone: "quantum" },
      ],
      callout: "各自隨機、彼此一致，而且無法拆成兩顆位元各自的狀態：這就是**糾纏**",
      notes:
        "第三個範例加入第二顆位元。先對 q0 做 H，這時狀態是 |00⟩ 加 |01⟩，q0 在疊加、q1 還是 0，兩顆位元互不相干。接著做 CNOT，以 q0 為控制：q0 是 1 的那一半，q1 也被翻成 1，結果變成 |00⟩ 加 |11⟩。量測的時候，單看任何一顆都是 50 比 50，但兩顆對照永遠相同，不會出現 01 或 10。這個狀態沒辦法拆成兩顆位元各自的狀態，這就是糾纏。",
    },
    {
      type: "amps",
      section: "3. Bell 態",
      title: "振幅逐步看：CNOT 把機率搬到 |11⟩",
      scene: S.bell,
      lead: "位元字串是 |q1 q0⟩：右邊那位是 q0",
      labels: K2,
      panels: [
        { head: "① 起點", amps: [1, 0, 0, 0], note: "只有 |00⟩" },
        { head: "② H（q0）", amps: [R2, R2, 0, 0], note: "q0 疊加：|00⟩、|01⟩ 各半" },
        { head: "③ CNOT → Φ⁺", amps: [R2, 0, 0, R2], note: "|01⟩ 的振幅搬到 |11⟩：只剩 00、11", tone: "quantum", focus: true },
        { head: "對照：Φ⁻", amps: [R2, 0, 0, -R2], note: "先加 X(q0)：|11⟩ 帶負號，量起來和 Φ⁺ 一樣" },
      ],
      callout: "CNOT 不改變長條的高度，只是把 q0 = 1 那一半的振幅**搬到 q1 也是 1 的位置**",
      notes:
        "把振幅畫出來，位元字串右邊那位是 q0。起點只有 |00⟩。H 之後，|00⟩ 和 |01⟩ 各一半。CNOT 只做一件事：q0 等於 1 的那一半，把 q1 翻過來，所以 |01⟩ 的振幅整根搬到 |11⟩，最後只剩 00 和 11。最右邊是 Φ⁻，|11⟩ 帶負號，量起來和 Φ⁺ 一模一樣，差別只在正負號。",
    },
    {
      type: "table",
      section: "3. Bell 態",
      title: "四個 Bell 態：只差開頭的 X",
      scene: S.bell,
      headers: ["Bell 態", "H、CNOT 之前先加", "狀態（|q1 q0⟩）", "量測結果"],
      rows: [
        ["Φ⁺", "無", "(|00⟩ + |11⟩)/√2", "00 或 11（永遠相同）"],
        ["Φ⁻", "X(q0)", "(|00⟩ − |11⟩)/√2", "00 或 11（永遠相同）"],
        ["Ψ⁺", "X(q1)", "(|01⟩ + |10⟩)/√2", "01 或 10（永遠相反）"],
        ["Ψ⁻", "X(q0)、X(q1)", "(|10⟩ − |01⟩)/√2", "01 或 10（永遠相反）"],
      ],
      colW: [1.6, 2.9, 3.8, 3.83],
      callout: "直接量測只分得出相同或相反；正負號要再做 CNOT、H 干涉才看得到（**Bell 量測**）",
      notes:
        "Bell 態一共有四個，電路都一樣是 H 加 CNOT，只差開頭有沒有先加 X。q0 先翻成 1，H 會帶進一個負號，得到 Φ⁻；q1 先翻成 1，CNOT 之後兩顆就會相反，得到 Ψ⁺；兩個都翻就是 Ψ⁻。直接量測只分得出相同還是相反，正負號要把電路倒過來，再做一次 CNOT 和 H 干涉才看得到，這叫做 Bell 量測，是量子隱形傳態的關鍵步驟。動畫裡上方可以切換四個 Bell 態。",
    },

    // ───────────── 4. GHZ 態 ─────────────
    {
      type: "circuit",
      section: "4. GHZ 態",
      title: "範例 4｜GHZ 態：CNOT 一路串下去",
      scene: S.ghz,
      circuitHeight: 3.3,
      circuit: {
        wires: ["q0  |0⟩", "q1  |0⟩", "q2  |0⟩"],
        cols: [{ g: ["H", null, null] }, { cx: [0, 1] }, { cx: [1, 2] }, { m: [true, true, true] }],
        marks: [{ after: 0, label: "①" }, { after: 1, label: "②" }, { after: 2, label: "③" }],
      },
      stages: [
        { head: "① H 閘（q0）", eq: "(|000⟩ + |001⟩)/√2", body: "q0 進入疊加，其他位元還在 0", tone: "neutral" },
        { head: "② CNOT（q0 → q1）", eq: "(|000⟩ + |011⟩)/√2", body: "q0 的值「複製」到 q1：兩顆綁在一起", tone: "neutral" },
        { head: "③ CNOT（q1 → q2）", eq: "(|000⟩ + |111⟩)/√2", body: "三顆全部糾纏：**不是全 0 就是全 1**", tone: "quantum" },
      ],
      notes:
        "第四個範例把 Bell 電路的 CNOT 一路串下去。先對 q0 做 H，然後 CNOT 從 q0 到 q1，把 q0 的值複製給 q1；再 CNOT 從 q1 到 q2。三顆位元全部糾纏，量測結果不是 000 就是 111，各一半。要注意這裡的複製只是在計算基底上把 0、1 對應起來，並不是把一個未知的量子態複製一份，那是不可能的。動畫裡可以切換成 4 顆位元。",
    },
    {
      type: "amps",
      section: "4. GHZ 態",
      title: "振幅逐步看：一次多綁一顆",
      scene: S.ghz,
      lead: "橫軸是 q2 q1 q0 的 8 種結果",
      labels: K3,
      panels: [
        { head: "① H（q0）", amps: [R2, R2, 0, 0, 0, 0, 0, 0], note: "000、001 各半" },
        { head: "② CNOT（q0 → q1）", amps: [R2, 0, 0, R2, 0, 0, 0, 0], note: "001 搬到 011" },
        { head: "③ CNOT（q1 → q2）", amps: [R2, 0, 0, 0, 0, 0, 0, R2], note: "011 搬到 111：只剩 000、111", tone: "quantum", focus: true },
      ],
      callout: "硬體常用 GHZ 態測試糾纏品質：雜訊越大，量到 000、111 以外結果的比例越高",
      notes:
        "振幅的變化和 Bell 態很像，每做一次 CNOT，就把 q0 等於 1 的那一根往右搬一次：001 搬到 011，再搬到 111。最後只剩 000 和 111 兩根。GHZ 電路的深度會隨位元數增加，每多一顆就多一個 CNOT，所以硬體廠常用它來測試多位元糾纏的品質：理想情況只會量到全 0 或全 1，雜訊越大，其他結果出現的比例就越高。我們的動畫是理想模擬，所以不會出現其他結果。",
    },

    // ───────────── 5. Deutsch ─────────────
    {
      type: "circuit",
      section: "5. Deutsch",
      title: "範例 5｜Deutsch：查一次分辨常數或平衡",
      scene: S.deu,
      circuit: {
        labelWidth: 2.3,
        wires: ["q0  |0⟩（輸入）", "q1  |0⟩（輔助）"],
        cols: [{ g: [null, "X"] }, { g: ["H", "H"] }, { blk: "U_{f}" }, { g: ["H", null] }, { m: [true, false] }],
        marks: [{ after: 0, label: "①" }, { after: 1, label: "②" }, { after: 2, label: "③" }, { after: 3, label: "④" }],
      },
      stages: [
        { head: "① 輔助位元翻成 1", eq: "|q1 q0⟩ = |10⟩", body: "q0 是要問黑盒的輸入，q1 接收答案", tone: "neutral" },
        { head: "② 兩顆都做 H", eq: "q0：|+⟩，q1：|−⟩", body: "x = 0、1 **同時**送進黑盒；q1 的 |−⟩ 是相位回踢的關鍵", tone: "neutral" },
        { head: "③ 黑盒（只問一次）", eq: "U_{f}|x⟩|y⟩ = |x⟩|y ⊕ f(x)⟩", body: "f(x) = 1 的項多一個**負號**（相位回踢）", tone: "quantum" },
        { head: "④ q0 做 H 再量測", eq: "0 或 1", body: "**0 → 常數**（f(0) = f(1)）；**1 → 平衡**（f(0) ≠ f(1)）", tone: "good" },
      ],
      notes:
        "第五個範例是第一個量子演算法。黑盒裡有一個函數 f，輸入一個位元、輸出一個位元，它可能是常數，也就是 f(0) 等於 f(1)，也可能是平衡，f(0) 不等於 f(1)。古典電腦要問兩次才知道。量子電路這樣做：q0 是輸入，q1 是輔助位元。先把 q1 翻成 1，兩顆都做 H，q0 變成 |+⟩，代表 0 和 1 同時送進去；q1 變成 |−⟩。黑盒做的是把 f(x) 加到 q1 上，因為 q1 在 |−⟩，翻轉它等於讓那一項多一個負號，這叫相位回踢。最後 q0 再做 H 量測，0 是常數，1 是平衡，只問一次。",
    },
    {
      type: "amps",
      section: "5. Deutsch",
      title: "振幅逐步看：f(x) = x 的相位回踢",
      scene: S.deu,
      lead: "位元字串是 |q1 q0⟩；黑盒 f(x) = x 就是一個 CNOT（q0 → q1）",
      labels: K2,
      panels: [
        { head: "① X（q1）", amps: [0, 0, 1, 0], note: "q1 = 1、q0 = 0" },
        { head: "② H、H", amps: [0.5, 0.5, -0.5, -0.5], note: "四個 ±½；q1 = 1 的兩根是負的（|−⟩ 的負號）" },
        { head: "③ 黑盒 U_{f}", amps: [0.5, -0.5, -0.5, 0.5], note: "q0 = 1 的兩根**變號**：q0 從 |+⟩ 變成 |−⟩", tone: "quantum", focus: true },
        { head: "④ H（q0）", amps: [0, R2, 0, -R2], note: "只剩 q0 = 1：**平衡** ✓", tone: "good", focus: true },
      ],
      callout: "看 ③：四個機率都還是 25%，但負號換了位置。答案藏在正負號裡，④ 的 H 才把它變成 q0 = 1",
      notes:
        "實際把振幅算一次，黑盒選 f(x) 等於 x，它就是一個從 q0 到 q1 的 CNOT。第一步 q1 翻成 1。第二步兩個 H，四根長條都是正負二分之一，q1 等於 1 的兩根是負的。第三步問黑盒，q0 等於 1 的兩根互換，結果是這兩根變號，等於 q0 從 |+⟩ 變成 |−⟩。注意這時候四個機率都還是 25%，完全看不出來，答案藏在正負號裡。第四步對 q0 做 H，只剩 q0 等於 1 的兩根，所以判定平衡，正確。",
    },
    {
      type: "table",
      section: "5. Deutsch",
      title: "四種黑盒全部跑一次",
      scene: S.deu,
      headers: ["黑盒函數", "類型", "黑盒裡的閘", "黑盒之後的 q0", "量 q0"],
      rows: [
        ["f(x) = 0", "常數", "什麼都不做", "|+⟩", "0（100%）"],
        ["f(x) = 1", "常數", "X(q1)", "−|+⟩（整體負號量不到）", "0（100%）"],
        ["f(x) = x", "平衡", "CNOT(q0 → q1)", "|−⟩", "1（100%）"],
        ["f(x) = 1 − x", "平衡", "CNOT(q0 → q1) 再 X(q1)", "−|−⟩", "1（100%）"],
      ],
      colW: [2.0, 1.3, 3.3, 3.53, 2.0],
      callout: "古典要問 f(0)、f(1) **兩次**；量子只問 **1 次**，四種黑盒都 100% 判斷正確",
      notes:
        "四種黑盒全部跑一次。f 等於 0 什麼都不做；f 等於 1 對輔助位元做 X，結果每一項都多一個負號，這是整體相位，量不到，所以 q0 還是 |+⟩。f 等於 x 是一個 CNOT，q0 變成 |−⟩。f 等於 1 減 x 是 CNOT 之後再一個 X，q0 變成負的 |−⟩。所以黑盒之後 q0 只有兩種：常數是正負 |+⟩，平衡是正負 |−⟩，最後的 H 把它們分開，四種都百分之百判斷正確。這是 Deutsch 在 1985 年提出的，是第一個被證明比古典更快的量子演算法。",
    },

    // ───────────── 6. Bernstein–Vazirani ─────────────
    {
      type: "circuit",
      section: "6. Bernstein–Vazirani",
      title: "範例 6｜BV：查一次讀出整串密碼",
      scene: S.bv,
      circuitHeight: 3.65,
      circuit: {
        labelWidth: 2.3,
        wires: ["q0  |0⟩", "q1  |0⟩", "q2  |0⟩", "q3  |0⟩（輔助）"],
        cols: [{ g: [null, null, null, "X"] }, { g: ["H", "H", "H", "H"] }, { cx: [0, 3] }, { cx: [2, 3] }, { g: ["H", "H", "H", null] }, { m: [true, true, true, false] }],
        marks: [{ after: 0, label: "①" }, { after: 1, label: "②" }, { after: 3, label: "③" }, { after: 4, label: "④" }],
      },
      stages: [
        { head: "① 輔助 q3 翻成 1", body: "q0–q2 是輸入，q3 接收答案", tone: "neutral" },
        { head: "② 全部 H", body: "q0–q2 同時代表 **8 種輸入**；q3 變成 |−⟩", tone: "neutral" },
        { head: "③ 黑盒：密碼 s = 101", body: "q0、q2 各接一條 CNOT 到 q3；每個輸入帶上 (−1)^{s·x}", tone: "quantum" },
        { head: "④ 再做 H、量測", body: "q2 q1 q0 = **101**：正好就是密碼", tone: "good" },
      ],
      notes:
        "最後一個範例是 Bernstein–Vazirani。黑盒裡藏了一組 3 位元密碼 s，每次查詢只回答 s 點 x 除以 2 的餘數，也就是密碼和你的猜測有幾個共同的 1，是奇數還是偶數。量子電路和 Deutsch 幾乎一樣：輔助位元 q3 先翻成 1，全部做 H，q0 到 q2 同時代表 8 種輸入。黑盒的做法很簡單：密碼哪一位是 1，就從那顆位元接一條 CNOT 到 q3，這裡密碼是 101，所以接 q0 和 q2。最後再做一次 H，量到的 q2 q1 q0 正好就是密碼 101。",
    },
    {
      type: "amps",
      section: "6. Bernstein–Vazirani",
      title: "振幅逐步看：密碼藏在正負號的排列裡",
      scene: S.bv,
      lead: "只畫 q2 q1 q0 的 8 種結果；輔助位元 q3 一直停在 |−⟩，先提出來不畫",
      labels: K3,
      panels: [
        { head: "② H 之後", amps: [Q, Q, Q, Q, Q, Q, Q, Q], note: "8 種輸入振幅都是 1/(2√2) ≈ 0.35" },
        { head: "③ 黑盒（s = 101）", amps: [Q, -Q, Q, -Q, -Q, Q, -Q, Q], note: "s·x 為奇數的輸入多一個**負號**：機率仍各 12.5%", tone: "quantum", focus: true },
        { head: "④ 再做 H", amps: [0, 0, 0, 0, 0, 1, 0, 0], note: "只剩 **101**：機率 100%", tone: "good", focus: true },
      ],
      callout: "③ 的正負號排列，正好是 H 作用在 |101⟩ 上的結果；所以 ④ 再做一次 H，就把它還原成 |101⟩",
      notes:
        "把輸入三顆位元的振幅畫出來，輔助位元 q3 一直停在 |−⟩，所以先提出來不畫。H 之後 8 個振幅都一樣，大約 0.35。問完黑盒之後，s 點 x 是奇數的那些輸入多了一個負號，例如 001、011、100、110，但機率還是各 12.5%，看不出來。關鍵在於：這個正負號的排列，剛好就是對 |101⟩ 做 H 會得到的樣子，而 H 做兩次等於什麼都沒做，所以第四步再一個 H，就把它還原成 |101⟩，百分之百讀出密碼。",
    },
    {
      type: "table",
      section: "6. Bernstein–Vazirani",
      title: "古典 vs 量子：要查幾次？",
      headers: ["問題", "黑盒回答什麼", "古典最少查詢", "量子查詢", "量子用到的技巧"],
      rows: [
        ["Deutsch", "f(x)，x 是 1 個位元", "2 次", "1 次", "相位回踢 + 干涉"],
        ["Deutsch–Jozsa（n 位元）", "f(x)，保證常數或平衡", "最壞 2ⁿ⁻¹ + 1 次", "1 次", "同上，輸入改成 n 顆"],
        ["Bernstein–Vazirani", "s·x（mod 2）", "n 次（每次問一位）", "1 次", "同上，答案寫在每一位的相位"],
      ],
      colW: [2.6, 2.8, 2.5, 1.4, 2.83],
      callout: "三個演算法是同一個套路：**疊加** → 黑盒把答案寫進**正負號** → **H 干涉**讀出來",
      notes:
        "把查詢次數整理一下。Deutsch 古典要 2 次、量子 1 次。推廣到 n 位元的 Deutsch–Jozsa，古典最壞要 2 的 n 減 1 次方加 1 次，量子還是 1 次。Bernstein–Vazirani 古典可以每次只問一位，用 001、010、100 去問，需要 n 次；量子 1 次就讀出整串。三個演算法其實是同一個套路：先疊加，黑盒把答案寫進正負號，最後用 H 干涉讀出來。要提醒的是，這些是黑盒查詢次數的比較，是展示量子加速原理的教學範例，還不是實用的應用。",
    },

    // ───────────── 互動動畫 ─────────────
    {
      type: "scene3d",
      section: "互動動畫",
      title: "互動動畫：逐步播放、自己量測",
      image: ["figures/basic_circuits/interf_z.jpg", "figures/basic_circuits/bell_final.jpg"],
      imageLabels: ["干涉：Z 之後", "Bell 態：量測 1,000 次"],
      layout: "wide",
      bullets: [
        "上方是**電路**：▶ 播放、← → 換步，點閘直接跳到那一步；橘色虛線是目前進度",
        "左下是**振幅長條**（藍＝正、銅＝負）與狀態式子；只有一顆位元時另有 **Bloch 球**",
        "右下可以**量測 1 次或 1,000 次**：灰底是理論機率、綠色是實際次數",
      ],
      link: { label: "六個基礎量子電路", url: BC, prefix: "開啟互動動畫" },
      imageHeight: 3.55,
      notes:
        "這是互動動畫的畫面。上方是電路，可以按播放、用左右鍵換步，也可以直接點電路上的閘，橘色虛線是目前的進度。左下是振幅長條，動畫頁用藍色表示正、銅色表示負，下面寫出目前的狀態式子；只有一顆位元的範例還會畫 Bloch 球，向量照閘真正的旋轉軸轉動。右下可以量測：按一次只得到一個結果，按 1,000 次就能看到分布，灰色底是理論機率，綠色是實際次數。左圖是干涉範例停在 Z 之後，機率還是各一半；右圖是 Bell 態量測 1,000 次，只出現 00 和 11。",
    },
    {
      type: "scene3d",
      section: "互動動畫",
      title: "互動動畫：Deutsch 與 BV",
      image: ["figures/basic_circuits/deutsch_oracle.jpg", "figures/basic_circuits/bv_final.jpg"],
      imageLabels: ["Deutsch：剛問完黑盒", "BV：讀出密碼 101"],
      layout: "wide",
      bullets: [
        "上方按鈕可以**換黑盒**（Deutsch 四種函數）或**點選密碼位元**（BV 共 8 種密碼）",
        "Deutsch 停在黑盒之後：q0 = 1 的兩根**變號**；量測後直接顯示「常數／平衡」",
        "頁面底部附**會隨選項改變**的 Qiskit 程式碼，可以複製到自己的電腦執行",
      ],
      link: { label: "Deutsch", url: `${BC}#deutsch`, prefix: "開啟互動動畫" },
      imageHeight: 3.55,
      notes:
        "後兩個演算法在動畫裡可以自己換題目。Deutsch 可以切換四種黑盒函數，BV 可以點選密碼的每一位，共 8 種密碼。左圖是 Deutsch 剛問完黑盒的瞬間，q0 等於 1 的兩根長條變號，和剛才算的一樣；右圖是 BV 量測 1,000 次，每次都是 101，畫面直接顯示密碼。頁面最下面還附了 Qiskit 程式碼，會跟著選項改變，可以複製到自己的電腦執行。按鈕連到 Deutsch 範例，網址錨點換成 #bv 就是 BV。",
    },

    // ───────────── 總結 ─────────────
    {
      type: "summary",
      section: "總結",
      title: "重點整理",
      points: [
        "**疊加**：H 把 |0⟩ 變成兩個振幅各 0.707；機率 = 振幅^{2}，負號量不到",
        "**干涉**：振幅有正負，路徑相加時會**抵消**；H‑Z‑H = X，只差一個負號結果就相反",
        "**糾纏**：H + CNOT 做出 Bell 態，CNOT 串下去就是 GHZ 態；各自隨機、彼此一致",
        "**相位回踢**：輔助位元在 |−⟩ 時，黑盒的答案變成輸入位元的**正負號**",
        "**Deutsch、BV**：疊加 → 黑盒寫入正負號 → H 干涉讀出，查詢**只要 1 次**",
      ],
      notes:
        "整理五個重點。一，疊加：H 把 |0⟩ 變成兩個振幅都是 0.707 的狀態，機率是振幅的平方，所以負號量不到。二，干涉：振幅有正有負，路徑相加時會抵消，H、Z、H 就等於 X。三，糾纏：H 加 CNOT 做出 Bell 態，CNOT 一路串下去就是 GHZ 態，各自隨機，但彼此一致。四，相位回踢：輔助位元在 |−⟩ 的時候，黑盒的答案會變成輸入位元的正負號。五，Deutsch 和 BV 都是疊加、黑盒寫入正負號、H 干涉讀出，只要查詢一次。",
    },
    {
      type: "closing",
      section: "總結",
      title: "討論與延伸",
      question: "如果把 BV 的黑盒換成一般函數，還能只查一次嗎？",
      prompts: [
        "提示：BV 成功，是因為黑盒寫下的正負號排列剛好是 H|s⟩",
        "動手做：在動畫裡把密碼改成 000，看看黑盒裡剩下什麼",
        "下一步：量子隱形傳態、Grover 搜尋、量子傅立葉轉換",
      ],
      refs: [
        "互動動畫：animations/basic-circuits.html（#superposition、#interference、#bell、#ghz、#deutsch、#bv）",
        "延伸動畫：animations/operation.html#interference、#grover",
        "延伸動畫：animations/transmon-3d.html#deutsch、#bv",
        "D. Deutsch, Proc. R. Soc. Lond. A 400, 97 (1985)",
        "E. Bernstein & U. Vazirani, SIAM J. Comput. 26, 1411 (1997)",
        "D. M. Greenberger, M. A. Horne, A. Zeilinger, arXiv:0712.0921",
      ],
      notes:
        "最後留一個討論題：如果把 BV 的黑盒換成一般的函數，還能只查一次嗎？提示是，BV 之所以成功，是因為黑盒寫下的正負號排列剛好等於 H 作用在密碼上的結果，所以一個 H 就能還原；一般的函數沒有這種結構。也可以在動畫裡把密碼改成 000，看看黑盒裡剩下什麼。學完這六個電路，下一步可以看量子隱形傳態、Grover 搜尋和量子傅立葉轉換。參考資料和延伸動畫列在右邊。",
    },
  ],
};
