# Q087 事實查核

查核日：2026-11-18。查核者：製作代理（Claude）。逐字引文見 `source-notes.md`。
方法：學程簡報（QC_Operation_Talk.pptx 第 18、34、44 頁）與兩個操作場景的原始碼由製作代理讀取；VQE／QAOA 的事實取自維基百科兩頁（2026-11-18 讀取）；本機模擬器的玩具題目由製作代理重算。
限制：課綱規劃的「◆ 新簡報：VQE 與 QAOA」「★ 變分能量地形場景」尚未製作；本集不依賴它們。模擬器題目為自訂教學模型。

| # | 本集的說法（幕） | 依據 | 結論 |
|---|---|---|---|
| 1 | 上一堂：容錯量子電腦要做某些閘需魔術態工廠蒸餾、代價高（1） | academy/lessons/Q086/brief.md 學習目標 | 相符 |
| 2 | 量子電腦與古典電腦組隊（1） | 維基 VQE：hybrid algorithm that uses both classical computers and quantum computers | 相符 |
| 3 | 基態＝能量最低的狀態（3） | 維基 VQE：finds the ground state | 相符（一般定義） |
| 4 | 變分原理：猜的平均能量不低於基態（3） | 維基 VQE Formulation：任意變動 |ψ⟩ 時 ⟨ψ|H|ψ⟩ 的最小值就是基態能量 | 相符（由「最小值」推得；見 not_verified） |
| 5 | 帶可調角度的線路＝試探線路（3） | 維基 VQE ansatz；簡報 p18「Rx/Ry/Rz(θ)：任意角度：變分演算法的參數」 | 相符 |
| 6 | 迴圈四步：古典挑角度、量子跑線路、重複量測算平均能量、古典更新（4） | 維基 VQE：quantum processor calculates the expectation value；a classical optimizer is used to improve the guess | 相符 |
| 7 | VQE 2014 年提出；只模擬過很小的分子（5） | 維基 VQE：Originally proposed in 2014；As of 2022 … can only simulate small molecules | 相符 |
| 8 | QAOA 2014 年提出；組合最佳化，例如 MaxCut（5） | 維基 QAOA（Quantum optimization algorithms）：Farhi, Goldstone, Gutmann 2014；MaxCut | 相符 |
| 9 | 能量拆成好幾項分別量、再加總（6） | 維基 VQE：measure the expectation value of each Pauli string；簡報 p34「需要多個量測基底」 | 相符 |
| 10 | 量測次數比量子相位估計多很多（6） | 維基 VQE：number of measurements higher than for quantum phase estimation | 相符 |
| 11 | 誤差約和次數平方根成反比；小十倍要多百倍（6） | 01_qubit.js desc：誤差約 √(p(1−p)/N)，要精度提高 10 倍就要 100 倍的 shots | 相符 |
| 12 | QAOA 兩種層輪流：問題層、混合層（7） | 維基：cost Hamiltonian 與 mixer、repeated application of UC and UM | 相符（口語化說明） |
| 13 | 每層兩個角度，共兩倍層數個角度，交古典調（7） | 維基：2p angles；angles are updated classically | 相符 |
| 14 | 靈感來自絕熱定理；MaxCut 研究指 p > 11 才有可擴展優勢（7） | 維基：inspired by the Quantum Adiabatic theorem；a study of QAOA and MaxCut shows that p>11 is required for scalable advantage | 相符（單一研究） |
| 15 | 局部最小值（8、10） | 課綱孩子獨立改造；維基 VQE：heuristic, does not guarantee convergence；模擬器重算 (0°,0°) 為 −0.4 局部最小 | 相符 |
| 16 | 貧瘠高原：線路選不好、地形平、停在非最低點（8） | 維基 VQE：may halt at suboptimal parameters … 'barren plateau'；維基 QAOA：plateaus in the energy landscape | 相符 |
| 17 | 啟發式、不保證找到基態（8） | 維基 VQE | 相符 |
| 18 | QAOA 曾短暫領先，後被古典演算法追上（8） | 維基：briefly had a better approximation ratio … until a more effective classical algorithm was proposed | 相符 |
| 19 | 沒有被證明的普遍加速（12） | 課綱常見誤解；維基：no proven exponential speed up；簡報 p44 最佳化「實用優勢尚未確立」 | 相符 |
| 20 | 玩具題目兩谷底 −1.6、−0.4；近 0° 出發停 −0.4、近 180° 出發到 −1.6；四十次迭代（9、10） | classroom.py 重算（學習率 0.4）：(20°,20°) → −0.400、(160°,160°) → −1.600 | 相符 |
| 21 | 預告下一堂：量子化學與材料、氫分子能量曲線（12） | academy/lessons/Q088/brief.md | 相符 |

## 動畫展示段

| 段 | 說法 | 依據 | 結論 |
|---|---|---|---|
| knob | 重設回零態、箭頭指北極 | 02_gates.js resetTo([0,0,1]) | 相符 |
| knob | 旋轉角四十五度，按旋轉閘，繞粉紅軸轉四十五度 | 滑桿步進 5；Ry 推入 RY 旋轉；desc「粉紅線是旋轉軸」 | 相符 |
| knob | 再按三次停在南極，留軌跡，右下線路紀錄四個方塊 | 4 × 45° = 180°；trailN 900；seq 每完成一閘加一格、重設清空 | 相符 |
| loop | 六十度跑一千次，藍柱約四分之三、與青線同高 | P(0) = cos²(30°) = 0.75；ideal0 = 青線 | 相符（隨機約 ±1.4%） |
| loop | 一百二十度，箭頭往南，藍柱約四分之一 | cos²(60°) = 0.25；滑桿改動清空統計 | 相符 |
| loop | 一百八十度，藍柱消失 | cos²(90°) ≈ 4×10⁻³³ | 相符 |
