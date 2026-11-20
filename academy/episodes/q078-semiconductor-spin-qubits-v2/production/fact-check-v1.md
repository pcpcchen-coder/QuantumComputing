# Q078 事實查核

查核日：2026-11-18。查核者：製作代理（Claude）。逐字引文見 `source-notes.md`。
方法：學程沒有半導體自旋平台的簡報或場景（課綱標為需新增），平台事實由製作代理以 WebFetch 讀取維基百科三個頁面；超導比較值取自學程動畫原始碼。
限制：維基頁面沒有寫讀取方式、典型毫克耳文工作溫度、量子點差異與保真度，這些本集不談或列在未查證。

| # | 本集的說法（幕） | 依據 | 結論 |
|---|---|---|---|
| 1 | 上一堂：光子不怕熱，但很難讓兩個光子直接作用（1） | academy/lessons/Q077/brief.md 驗收例句 | 相符 |
| 2 | 三步、偵探辦案、平台卡（2） | Q078 課綱 | 相符 |
| 3 | 量子點：半導體裡很小的區域，離散能階，被叫做人造原子（3） | Wikipedia Quantum dot：「sometimes referred to as artificial atoms」 | 相符 |
| 4 | 微影做的金屬電極加電壓圍出量子點，寬約 20–100 nm（3） | Quantum dot：「defined by lithographically patterned gate electrodes」，橫向約 20–100 nm | 相符 |
| 5 | 調電壓讓電子一顆一顆進出，可只留一顆（3） | Quantum dot：矽 CMOS 元件「progressive charging of electrons (holes) one by one」；閘電壓決定載子數 | 相符 |
| 6 | 自旋在磁場中分成兩種能量、當零和一（4） | EPR：季曼效應；Spin qubit：「spin-1/2 degree of freedom of individual electrons confined in quantum dots as qubits」 | 相符 |
| 7 | 磁場越強能量差越大；頻率相符的微波翻轉自旋（4） | EPR：分裂與磁場成正比；吸收能量相符的光子改變自旋 | 相符（一般原理；未查特定晶片） |
| 8 | 1997 年 Loss 與 DiVincenzo 提出（4） | Spin qubit：「proposed by Daniel Loss and David P. DiVincenzo in 1997」（期刊論文 1998） | 相符 |
| 9 | 兩點間窄閘電極控制耦合（5） | Spin qubit：「A narrow gate between the two dots can modulate the coupling」 | 相符 |
| 10 | 電壓脈衝讓自旋交換；半個脈衝得交換閘平方根（5） | Spin qubit：「pulsed inter-dot gate voltage」；half duration →「square root of swap gate」 | 相符 |
| 11 | 配單位元閘組成受控反閘、產生糾纏（5） | Spin qubit：CNOT 由 √SWAP 與個別自旋旋轉組成 | 相符 |
| 12 | 矽自旋可在業界標準矽晶圓廠製作（6） | Spin qubit：「can be produced at industry standard silicon semiconductor wafer fabs」 | 相符 |
| 13 | 英特爾投入；也有砷化鎵、鍺（6） | Spin qubit：「pursued by Intel, among others」；gallium arsenide、germanium | 相符 |
| 14 | 一片晶片理論上可塞很多顆（6） | 依尺寸推論 | 推論，列入未查證 |
| 15 | 超導要 10 mK 稀釋冷凍機（7、10） | js/atoms/13_compare.js 標籤「10 mK 稀釋冷凍機」 | 相符 |
| 16 | 超導讀取諧振腔約 4 mm（7、10） | js/scenes/08_chip.js「長度約 4 mm」 | 相符 |
| 17 | 部分矽元件可在幾 K 工作，叫熱量子位元（7） | Spin qubit：「a comparably high operation temperature of a few kelvins (hot qubits)」 | 相符 |
| 18 | 比 10 mK 暖一百倍以上，有助於做多（7） | 1 K ÷ 10 mK = 100；維基稱有助擴展 | 相符（估算） |
| 19 | 每顆量子點性質不同、校準難（8、12） | 課綱常見誤解欄 | 相符（課綱）；細節列入未查證 |
| 20 | 自旋會被環境打亂，仍需低溫與控制線（8） | 一般性描述 | 列入未查證 |
| 21 | 尺寸差好幾萬倍（10） | 4 mm ÷ 100 nm = 4 萬、÷ 20 nm = 20 萬 | 相符（估算） |
| 22 | 預告下一堂：拓樸量子位元與色心，可能天生抗雜訊（12） | academy/lessons/Q079/brief.md | 相符 |
| 23 | 動畫展示：超導與中性原子閘速度柱一瞬到頂、離子阱好幾秒；超導相干時間柱最矮約兩千（展示） | 13_compare.js DATA.speed、DATA.coh（log₁₀(1e-4/5e-8) ≈ 3.3 最小） | 相符 |
