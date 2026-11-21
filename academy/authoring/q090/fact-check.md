# Q090 事實查核

查核日：2026-11-18。查核者：製作代理（Claude）。逐字引文見 `source-notes.md`。
方法：學程 repo 沒有 BB84 簡報或場景（課綱標示需新增），協定事實取自維基百科 BB84 與 Quantum key distribution 兩頁（2026-11-18 讀取原始 wikitext）；抽查機率以 1 − (3/4)^n 重算；動畫展示依 js/operation/01_qubit.js、07_readout.js 原始碼。
限制：25% 錯誤率與抽查機率只適用於攔截重送攻擊（Eve 攔截每一顆光子）；遊戲是教學模擬，不是光學實驗。

| # | 本集的說法（幕） | 依據 | 結論 |
|---|---|---|---|
| 1 | 上一堂：分辨量子最佳化與機器學習的合理宣稱與誇大宣傳（1） | academy/lessons/Q089/brief.md 學習目標 | 相符 |
| 2 | 量子金鑰分發解決「共用秘密鑰匙、確定途中沒人偷看」（1） | QKD 頁：能偵測第三者試圖得知金鑰 | 相符 |
| 3 | 最早的協定由 Bennett 與 Brassard 在 1984 年提出，以姓氏字頭加年份命名（3） | QKD 頁「known as BB84 after its inventors and year of publication」；BB84 頁「first quantum cryptography protocol」 | 相符 |
| 4 | 偏振：直線基底垂直＝0、水平＝1；斜線基底 45°＝0、135°＝1（3） | QKD 頁基底表與「a 0 is encoded in the rectilinear basis (+) as a vertical polarization state, and a 1 is encoded in the diagonal basis (x) as a 135° state」 | 相符 |
| 5 | 對的基底一定讀對；錯的基底一半一半隨機（3） | QKD 頁「measures the correct state… rectilinear measurement instead returns either horizontal or vertical at random」 | 相符 |
| 6 | 四步：Alice 隨機位元＋隨機基底送光子；Bob 隨機選基底量；公開基底不說結果；丟掉不同，平均一半；抽查一部分（4） | QKD 頁 BB84 段；BB84 頁 Description | 相符 |
| 7 | 沒人偷聽時理想上完全一樣，只因設備雜訊偶爾出錯（5） | QKD 頁「Other environmental conditions can cause errors in a similar fashion」；「imperfections in the transmission line and detectors」 | 相符 |
| 8 | Eve 攔截每顆、照結果重送，約四分之一對不上（5、10） | QKD 頁 Intercept and resend：50% × 50% = 25% | 相符 |
| 9 | 抽查過的位元公開後不能再用；錯太多就放棄重來（5、7） | QKD 頁「thus discarding them as key bits, as they are no longer secret」；「If more than p bits differ they abort the key and try again」 | 相符 |
| 10 | Eve 不知道基底只能猜；猜錯時結果隨機、狀態被改掉（6） | QKD 頁 Intercept and resend；BB84 頁「risk disturbing a particular qubit with probability 1/2 if she guesses the wrong basis」 | 相符 |
| 11 | 不可複製定理：無法完美複製未知量子狀態（6） | BB84 頁（no-cloning theorem；Eve 除非量測否則不能擁有副本） | 相符 |
| 12 | 比十位約 94%；比七十二位，躲過約十億分之一（7） | QKD 頁 P_d = 1 − (3/4)^n、n = 72 → 0.999999999；重算 n = 10 → 0.9437 | 相符 |
| 13 | QKD 只產生金鑰，訊息另外加密（8） | QKD 頁「used to produce and distribute only a key, not to transmit any message data」 | 相符 |
| 14 | 公開通道必須能認證，否則中間人冒充兩邊（8） | BB84 頁「authenticated public classical channel」；QKD 頁 Man-in-the-middle attack | 相符 |
| 15 | 原理安全不代表機器沒漏洞（8、12） | BB84 頁「depends on a perfect implementation. Side channel attacks exist」；QKD 頁 NSA 意見；課綱常見誤解 | 相符 |
| 16 | 雜訊與竊聽分不出，一律當成被偷聽（8） | QKD 頁「impossible to distinguish between these two types of errors… assumption that all errors are due to eavesdropping」 | 相符 |
| 17 | 遊戲：硬幣定位元、方向卡定基底；基底不同擲硬幣當結果（9） | 課綱動手任務（硬幣＋方向卡）；規則依協定設計的教學模擬 | 教學模擬，已在教材註明 |
| 18 | 兩小時流程、生活技能資訊安全意識（11） | 課綱 lesson.json | 相符 |
| 19 | 預告下一堂：Shor 為什麼威脅公開金鑰密碼、後量子密碼遷移（12） | academy/lessons/Q091/brief.md | 相符 |
| 20 | 動畫：|0⟩ 量一千次全為 0；|+⟩ 約各半；測量一次箭頭跳到極點、約 1.4 s 後自動復原（展示一） | 01_qubit.js：p0 = cos²(θ/2)、collapse 0.25 s、1.4 s 後恢復、閃光 0.4 s | 相符 |
| 21 | 動畫：θ = 0 量 Z 幾乎全藍、量 X 藍紅各半；θ = 90 量 X 大多數藍、量 Z 各半（展示二） | 07_readout.js：blochVec 含 0.4 rad 方位角 → θ = 90 量 X 的 P(1) ≈ 3.9%；間距 1.6 讀錯約 0.2% | 相符（所以旁白用「大多數」「幾乎」） |
