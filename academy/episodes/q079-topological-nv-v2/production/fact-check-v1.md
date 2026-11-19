# Q079 事實查核

查核日：2026-11-18。查核者：製作代理（Claude）。逐字引文見 `source-notes.md`。
方法：學程沒有拓樸量子位元或 NV 色心的簡報與場景（課綱標為「需新增」），本集事實取自維基百科五個條目（製作代理以 WebFetch 讀取）；動畫展示段依 `animations/js/operation/11_qec.js` 原始碼。
限制：維基百科是二手整理；拓樸量子位元的實驗現況變動快，本集只陳述「尚未被確認」與「有爭議」，不替任何宣稱背書。

| # | 本集的說法（幕） | 依據 | 結論 |
|---|---|---|---|
| 1 | 上一堂：半導體自旋量子位元，電子關進量子點，可借用晶片製程（1） | academy/lessons/Q078/brief.md 學習目標「量子點、電子自旋與 CMOS 製程的關係」 | 相符 |
| 2 | 錯誤更正把一個邏輯量子位元分散到很多實體量子位元（3） | 11_qec.js subtitle「用很多實體量子位元編碼 1 個邏輯量子位元」 | 相符 |
| 3 | 拓樸想讓材料本身把資訊分散保存（3） | Wikipedia TQC：資訊存在任意子的編織中、不受路徑小誤差影響 | 相符（概括說法） |
| 4 | 拓樸眼裡咖啡杯和甜甜圈分不出來（4） | Wikipedia Topology「a topologist cannot distinguish a coffee mug from a doughnut」 | 相符 |
| 5 | 拉一拉抖一抖辮子不變，換交叉順序才變（4、9） | 辮子群的基本性質；解答表以 A、B 交換逐步推算 | 相符（經典繩子類比） |
| 6 | 資訊存在好幾顆非阿貝爾任意子共同的狀態，運算靠編織（5） | Wikipedia TQC | 相符 |
| 7 | 編織結果只和繞的方式與順序有關，小誤差改不了，可能天生抗雜訊（5） | Wikipedia TQC「depends only on the topology of the braid」「impervious to small errors in the trajectories」 | 相符 |
| 8 | 一九九七年基塔耶夫提出（6） | Wikipedia TQC「proposed by … Alexei Kitaev in 1997」 | 相符 |
| 9 | 非阿貝爾任意子尚未在實驗上被確認（6、12） | Wikipedia TQC「have yet to be experimentally confirmed」 | 相符 |
| 10 | 候選者馬約拉納零能模；二零一八年宣稱看到孤立的馬約拉納粒子，二零二一年撤回（6） | Wikipedia TQC「claim of isolated Majorana particles from 2018 … was retracted in 2021」 | 相符（見 not_verified） |
| 11 | 二零二五年微軟發表馬約拉納一號；論文寫明量測本身不能確定是拓樸的（6） | Wikipedia Majorana 1（2025 年 2 月；作者：measurements "do not, by themselves, determine whether the low-energy states … are topological"） | 相符 |
| 12 | 鑽石中氮原子取代碳、旁邊一個空位（7） | Wikipedia NV center | 相符 |
| 13 | 綠光照射發紅光；亮度和自旋有關，可讀取；綠光可初始化（7） | Wikipedia NV center（red light excited by green；spin-dependent photoluminescence；optical spin-polarization initializes） | 相符 |
| 14 | 室溫下自旋相干最多可維持到毫秒（7） | Wikipedia NV center「long spin coherence at room temperature, lasting up to milliseconds」 | 相符 |
| 15 | 常當成很小的磁場感測器，也被研究用於量子網路與量子計算（7） | Wikipedia NV center（nanoscale magnetic/electric field measurement；algorithms and networks；explored for quantum computing） | 相符 |
| 16 | 工程答辯三問、新聞稿不等於證據（8、12） | 課綱「宣稱需要看同行審查與後續驗證」 | 相符（課綱教學要點） |
| 17 | 預告下一堂：時間尺度、連接性、錯誤率、設施、供電大比較（12） | academy/lessons/Q080/brief.md | 相符 |
| 18 | 展示段：表面碼是一種拓樸量子錯誤更正碼；貫穿上下邊界的鏈才是邏輯錯誤 | Wikipedia Toric code；11_qec.js desc「由上貫穿到下的鏈，就是邏輯錯誤」 | 相符 |
