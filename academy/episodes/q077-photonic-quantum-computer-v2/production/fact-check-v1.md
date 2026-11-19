# Q077 事實查核

查核日：2026-11-18。查核者：製作代理（Claude）。逐字引文見 `source-notes.md`。
方法：學程沒有光子平台的簡報或 3D 場景（課綱標為需新增），事實取自維基百科七個條目（製作代理於查核日讀取）；兩路干涉的數學以 `js/operation/08_interference.js` 交叉比對。
限制：家用鏡子與壓克力片只能示意光路，不是單光子實驗；「H＋相位＋H」與分光鏡干涉儀的對應只作直觀對照（相差相位慣例）。

| # | 本集的說法（幕） | 依據 | 結論 |
|---|---|---|---|
| 1 | 上一堂：原子陣列直接扮演磁性材料，不一定寫成線路（1） | academy/lessons/Q076/brief.md 學習目標 | 相符 |
| 2 | 用光子當量子位元（1） | Linear optical quantum computing；Jiuzhang「photons serve as the qubits」 | 相符 |
| 3 | 一顆光子用兩條路或偏振分零和一（3） | LOQC：「a single photon in two modes, vertical (V) and horizontal (H)」 | 相符（路徑編碼為兩模態的同一想法） |
| 4 | 光纖傳遞網路資訊（3） | 一般常識；Quantum computing 條目提到光纖可傳量子資訊 | 相符 |
| 5 | 兩顆光子幾乎不直接互相作用，兩位元閘難做（3、8、12） | LOQC：「photons hardly interact with each other」；課綱常見誤解 | 相符 |
| 6 | 四元件：鏡子、分光鏡、相位器、單光子偵測器（4） | LOQC：「mirrors, beam splitters, phase shifters」；KLM：「photon detectors」 | 相符 |
| 7 | 分光鏡一半穿過、一半反射（4） | Beam splitter：半鍍銀鏡約一半穿透一半反射 | 相符 |
| 8 | 一顆光子進分光鏡，處在兩個出口的疊加（4） | Beam splitter：creates a superposition on the outputs | 相符 |
| 9 | 兩條路都開時光子每次同一個出口（5） | Mach–Zehnder：「only detector 1 receives light」（無樣品、理想） | 相符（假設等臂、理想） |
| 10 | 擋住一條路，干涉消失，通過的光子兩出口各半（5） | Mach–Zehnder：blocking one arm → no interference；50:50 分光鏡 | 相符 |
| 11 | 光子兩條路一起走，在第二片分光鏡加強或抵消（5） | Mach–Zehnder：單光子也干涉，處於兩路疊加 | 相符 |
| 12 | 相位改變，加強和抵消的出口換位置；同 H、相位、H 數學（6） | Mach–Zehnder：相位改變兩偵測器的分配；08_interference.js：P(0)=cos²(φ/2) | 相符（直觀對照） |
| 13 | 兩顆相同光子同時從兩邊進，總是同一出口（7） | Hong–Ou–Mandel effect：「always exit the beam splitter in the same (but random) output mode」 | 相符 |
| 14 | 一九八七年測到；抵達時間錯開效應消失（7） | HOM：1987，Hong、Ou、Mandel；dip 只在時間重疊時為零 | 相符 |
| 15 | 玻色取樣：多光子進大干涉儀、看出口；對一般電腦難（8） | Boson sampling | 相符 |
| 16 | 二零二零年中國科學技術大學九章最多偵測七十六顆光子（8） | Jiuzhang：2020 年 12 月、USTC、「a maximum of 76 detected photons」 | 相符 |
| 17 | 玻色取樣不是萬用量子電腦（8） | Boson sampling：non-universal | 相符 |
| 18 | 測量式：先準備糾纏的光子再逐一測量（8） | One-way quantum computer：先準備資源態（叢集態）再單量子位元測量；主要考慮光子 | 相符 |
| 19 | 損耗是主要挑戰（12） | 課綱驗收與常見誤解；LOQC 提及光子損耗需容錯編碼 | 相符（以課綱為主） |
| 20 | 預告下一堂：半導體自旋量子位元、量子點（12） | academy/lessons/Q078/brief.md | 相符 |
| 21 | 動畫展示：相位 0 時右下 P=0；180° 換出口；偵測路徑 → 各半、白色總和箭頭隱藏（展示） | 08_interference.js update()：`s.visible = !which`、`P0 = 0.5` | 相符 |
