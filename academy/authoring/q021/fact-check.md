# Q021 事實查核

查核日：2026-11-18。查核者：製作代理（Claude）。逐字引文見 `source-notes.md`。
方法：課綱 `academy/lessons/Q020、Q021、Q022`；課綱指定簡報 `slides/output/ep049-superconducting-qubit.pptx` p6–8、`slides/transmon.pptx` p8，另加 `slides/JJ_Microwave_Readout_Talk.pptx` p8（投影片文字與講者備註以 python-pptx 擷取）；維基百科 Simple harmonic motion、Pendulum (mechanics)、LC circuit、Mechanical–electrical analogies、Harmonic oscillator（原始 wikitext，2026-11-18 取得）；動畫原始碼 `animations/lc-vs-jj.html` 由製作代理讀取，讀數以頁面同一段程式在 Node 實算；週期與 5 GHz 例子由製作代理實際執行 `oscillation_table.py`（只要 Python 3）重算。
限制：類比不只一種，本集採課綱的「質量↔電感、彈簧↔電容」（阻抗類比）；家中實驗的彈簧有質量、擺錘不是質點，量到的週期會和公式差一點。動畫段尚未試錄。

| # | 本集的說法（幕） | 依據 | 結論 |
|---|---|---|---|
| 1 | 上一堂：超導環裡的磁通只能一格一格地變（1） | Q020 brief「知道超導環裡的磁通只能是 Φ₀ 的整數倍」 | 相符 |
| 2 | 超導量子位元的出發點是一個會振盪的電路（1） | 簡報 ep049 p8「結論：超導 LC 電路就能成為一個會出現量子現象的諧振子」；Q022 brief 由 LC 電路的能階談起 | 相符 |
| 3 | 學習目標：把力學振盪和電路振盪對起來，質量對應電感、彈簧對應電容；作品是類比對照表（2） | Q021 lesson.json 學習目標、作品 | 相符 |
| 4 | 彈簧：力和伸開的距離成正比；中間最快、兩端停一下；位能與動能換手、總和不變（3） | 簡報 ep049 p6「K + U = const.」「動能＋位能為定值，一高一低互相交換」；維基百科 Simple harmonic motion（restoring force 與位移成正比） | 相符 |
| 5 | 單擺被重力拉回，回復力和擺角的正弦成正比；小角度時正弦約等於角度，是簡諧運動（4） | 維基百科 Pendulum (mechanics)：方程式含 sin θ、Small-angle approximation「sin θ ≈ θ」「The motion is simple harmonic motion」；transmon p8「U = −mgl cos θ」 | 相符（「回復力」指沿圓弧方向的分力 mg sin θ） |
| 6 | 單擺週期只看擺繩多少公尺，換更重的重物幾乎不變；一公尺約兩秒（4） | 維基百科 Simple harmonic motion「independent of the amplitude and mass of the pendulum but not of……g」；Pendulum「T₀ ≈ 2√ℓ」；oscillation_table.py：2π√(1/9.81) = 2.006 s | 相符（同一地點、g 不變） |
| 7 | 電容和電感接成一圈；電容放電、電流流過電感；電感抗拒電流改變，把電容反向充電再流回來（5） | 維基百科 LC circuit Operation「inductors oppose changes in current」「recharge the capacitor with a voltage of opposite polarity」 | 相符 |
| 8 | 能量在電容的電場與電感的磁場間換手；電荷來回流動，像重物擺動（5） | 維基百科 LC circuit「capacitor stores energy in the electric field……inductor……magnetic field」「The charge flows back and forth」「similar to a pendulum」；簡報 ep049 p8「電容能 ⇄ 電感能」「電荷來回流動」 | 相符（有電阻時會漸漸停，教材解答另說明） |
| 9 | 位置↔電荷、速度↔電流、質量↔電感（6） | 維基百科 Mechanical–electrical analogies 阻抗類比表：Velocity↔Current、Displacement↔Charge、Mass↔Inductance；Harmonic oscillator 類比表 m ↔ L | 相符 |
| 10 | 彈簧對應電容；彈簧越硬，對應電容越小（6） | 阻抗類比表 Compliance ↔ Capacitance；Harmonic oscillator 類比表 Spring constant k ↔ Elastance 1/C | 相符 |
| 11 | 彈簧週期跟著質量的根號變，質量四倍週期兩倍（7） | 維基百科 Simple harmonic motion T = 2π√(m/k)；oscillation_table.py：0.444 s → 0.889 s（2.0 倍） | 相符 |
| 12 | 電路週期跟著電感乘電容的根號變；電感或電容換大就變慢；彈簧換硬就變快（7） | 維基百科 LC circuit ω₀ = 1/√(LC)；Harmonic oscillator f = (1/2π)√(k/m) | 相符 |
| 13 | 一奈亨、一皮法約每秒五十億次、五吉赫，落在超導量子位元常用的微波頻率附近（7） | oscillation_table.py：1/(2π√(10⁻²¹)) = 5.033 × 10⁹ Hz；簡報 JJ_Microwave_Readout_Talk p8「量子位元 f01 ≈ 5 GHz」 | 相符（1 nH、1 pF 是整數例子，不是特定元件值） |
| 14 | 類比的前提是振幅要小（8、12） | lesson.json 常見誤解「類比只在小振幅時成立；大振幅單擺就不再是簡諧運動」 | 相符 |
| 15 | 大角度單擺週期比小角度時更久；一公尺的擺從九十度放手，週期約多百分之十八（8） | 維基百科 Pendulum「Arbitrary-amplitude period」、AGM 公式 T = T₀ / M(1, cos(θ₀/2))；oscillation_table.py：90° → 1.1803 倍；transmon p8「頻率會隨振幅略降」 | 相符（「一公尺」只是舉例，比例和擺繩多長無關） |
| 16 | 暫停題：彈簧拉過頭、變形回不去，對照表還成立嗎（8） | 維基百科 Simple harmonic motion（線性回復力才是簡諧運動）；解答：不成立 | 相符 |
| 17 | 量週期：數十次再除以十，反應時間被分攤（9） | 課綱動手任務「量彈簧和單擺的週期」；數十次的方法為本集設計 | 相符（方法為本集設計） |
| 18 | 改造：重物四倍、擺繩四分之一、換更重的擺錘（10） | 課綱孩子獨立改造「改變質量或擺長，預測週期變化並驗證」；oscillation_table.py：擺繩 1/4 → 0.5 倍 | 相符 |
| 19 | 120 分鐘安排（11） | lesson.json 2 小時課程流程 | 相符 |
| 20 | 下一堂：量子諧振子，電感電容電路的能階像間距相等的梯子，所以不能直接當量子位元（12） | Q022 brief「量子諧振子：等距的梯子」「知道 LC 電路的能階等距，所以無法只挑出兩個能階當量子位元」；簡報 ep049 p7「相鄰能階的間距固定：像樓梯一樣「等距」」 | 相符 |

## 動畫展示段（demos_extra/q021.py，lc-vs-jj.html #s1、#s2）

| 說法 | 依據 | 結論 |
|---|---|---|
| 圖解第一步：藍色直線是普通電感，電流和磁通成正比；橘色曲線是正弦 | 第 154–157 行 #s1「電流與磁通：直線 vs 正弦」；第 167 行圖例「電感 I = φ」「JJ I = sin φ」；第 13–15 行 --lc #1D6A8B（藍）、--jj #B65C12（橘） | 相符 |
| 橘色正弦就像單擺的回復力 | transmon p8「U = −mgl cos θ」，回復力 ∝ sin θ；與圖中 I = sin φ 同形 | 相符（類比說法，畫面上沒有單擺） |
| 相位拉到零點二，兩個圓點幾乎疊在一起，讀數零點二和零點一九九 | 第 384–385 行兩個圓點 (φ, φ)、(φ, sin φ)；第 387–388 行讀數三位小數：0.200、0.199 | 相符 |
| 說明寫著：相位很小時，正弦幾乎等於直線，看起來是線性的 | 第 392 行 \|φ\| < 0.35：「φ 很小：sin φ ≈ φ，JJ 跟普通電感幾乎一模一樣，這時它看起來是線性的。」 | 相符（旁白是轉述） |
| 拉到一點零，兩個圓點分開，直線一點零、正弦零點八四 | 實算 sin 1 = 0.841；第 395 行說明換成「直線和正弦分開了……1.85 倍」 | 相符 |
| 第二步：同一個正弦波去推，上面兩個週期的電流，下面各頻率的柱子 | 第 191 行「施加同一個磁通 φ(t) = A·sin(ωt)」；第 409 行「時間 →（兩個週期）」；第 421 行「頻譜：各諧波振幅 / 基頻振幅」、1ω／3ω／5ω／7ω | 相符 |
| 振幅零點三：藍色和橘色幾乎疊在一起，柱子幾乎只剩基頻那一對 | 0.3 sin t 與 sin(0.3 sin t)（峰值 0.300 對 0.296）；實算 3ω 0.4 %、5ω、7ω 為 0（柱高最少 1.5 px） | 相符 |
| 讀數：電感輸入加倍，輸出峰值變成兩倍 | 第 435 行 r2a 固定「2.00 倍」，標籤「輸入加倍，輸出峰值變成（電感）」 | 相符 |
| 藍色頻譜永遠只有基頻一根；線性系統不會產生新的頻率 | 第 425 行 lv = k===1 ? 100 : 0；第 192 行「線性系統不會產生新的頻率」 | 相符 |
| 振幅慢慢加大到二點五；藍色變高，橘色最高只到臨界電流虛線，波峰中間凹下去 | 第 411 行 ±I_c 虛線；sin(A sin t) 最大 1；t = π/2 時 sin 2.5 = 0.60 → 波峰中間凹 | 相符 |
| 三倍頻柱子約基頻的四成多 | 實算 \|J₃(2.5)\| / \|J₁(2.5)\| = 43.6 %（柱上標 44） | 相符 |
| 讀數：輸入加倍，輸出峰值只變成一點零零倍 | 第 434、436 行 sin(min(5, π/2)) / sin(min(2.5, π/2)) = 1.00 | 相符 |
| 操作方式：頁面沒有 #controls，改用 ('js', …) 設定 #phi、#amp 並觸發 input | 第 170–171、201–202 行原生 range；第 398、439 行 input 事件；record_demo.js 的 click／slider 只找 #controls | 製作注意（待試錄確認） |

## 課程

- 旁白不念英文：LC 稱「電感電容電路」、GHz 稱「吉赫」、nH／pF 稱「奈亨／皮法」、sin 稱「正弦」；投影片與教材上保留 LC、sin θ、nH、pF、GHz、2π√(m/k)。
- 沒有課堂錄音；未虛構孩子作品或量測數據。
