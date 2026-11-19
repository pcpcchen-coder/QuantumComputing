# Q024 來源筆記（逐字引文）

查核日：2026-11-18。課綱、簡報、筆記、動畫程式由製作代理讀取。程式由製作代理實際執行。

## 課綱（academy/lessons/Q024/lesson.json）

- 課程主題「JJ 是非線性電感」；階段「第二階段 硬體怎麼做」；模組「QM02 超導量子位元：從超導到 transmon」。
- 學習目標「知道 JJ 的電感會隨電流改變，這個非線性是做出量子位元的關鍵」。
- 動手任務「比較單擺小振幅與大振幅的週期，對照 JJ 電感隨電流變大」；孩子獨立改造「用 transmon-3d 場景找出能階間距開始變小的地方」；好玩機制「科學實驗（單擺大小振幅）」。
- 作品「單擺週期紀錄」；家長課前準備「細繩、重物、量角器；transmon-3d.html；notes/transmon-josephson-inductance.md」；生活技能支線「注意「近似」什麼時候會失效」。
- 常見誤解與安全提醒「JJ 沒有電阻損耗，所以是「無耗散」的非線性元件」。
- 沿用簡報頁：JJ_Microwave_Readout_Talk.pptx p14、transmon.pptx p3–8、ep049-superconducting-qubit.pptx p11–12；沿用 3D 場景：t3d、lj:s5、tr:junction。
- Q023 brief：「約瑟夫森接面：超導三明治」。Q025 brief：「E_J 與 E_C：兩個能量尺度」「知道 E_J／E_C 比值決定量子位元的性格」。

## 簡報（python-pptx 擷取）

- JJ_Microwave_Readout_Talk p14「JJ 是一個「非線性電感」」：「由 I = Ic sin φ 與 V = (Φ0/2π) dφ/dt：V = LJ · dI/dt　LJ(φ) = Φ0 / (2π Ic cos φ)」
  「小電流時 LJ0 = Φ0/(2π Ic)」「例：Ic = 30 nA → LJ0 ≈ 11 nH」「電感隨電流（相位）改變 → 非線性」「無耗散：不像電阻會發熱」「同時也是 EJ（約瑟夫森能）的來源」
  「左：電流–相位關係；右：電感隨相位上升，φ → π/2 時發散」；備註「它的值會隨相位、也就是隨流過的電流改變——這就是非線性；第二，它沒有耗散，不會發熱。」
  「今天最重要的一句話是：JJ 是一個「無耗散的非線性電感」。把它和電容並聯，就得到一個非線性振盪器，也就是 transmon 量子位元。」
- transmon p3「JJ 為什麼能當電感」「從兩條約瑟夫森方程式出發，推出一個「會隨相位改變」的電感」。
- transmon p4「從約瑟夫森方程式推出電感」：「I = Ic sin φ 電流由相位差決定」「V = (Φ0/2π) dφ/dt 電壓決定相位轉動速度」「V = LJ · dI/dt 形式與電感完全相同」
  「LJ0 = Φ0/2πIc ≈ 10.9 nH（Ic ≈ 30 nA）」「dI/dt = Ic cos φ · dφ/dt = Ic cos φ · (2π/Φ0) V」。
- transmon p5「JJ 電感隨電流變大」：「I ≪ Ic：LJ ≈ LJ0，行為像普通電感」「I → Ic：LJ → ∞，超過後跳到有電壓的耗散態」「π/2 < φ < π：LJ < 0，出現負電感」；
  備註「L_J = L_J0 / sqrt(1-(I/Ic)^2)。量子位元運作時電流遠小於 Ic，所以落在曲線左邊平坦處，但仍帶有一點彎曲，也就是非線性。」
- transmon p6「小振幅像電感，大振幅變軟」：「U = EJ(1 − cos φ) ≈ EJφ²/2 − EJφ⁴/24」「二次項 → 等效電感 LJ0」「能量存在相位耦合裡，不是磁場（動感電感）」
  「四次項 → 非線性」「振幅越大，回復力比拋物線弱，頻率變低」；備註「四次項是負的，代表大振幅時位能井比拋物線平坦。量子位元靠的就是這一點點偏離。」
- transmon p7「為什麼要用 JJ 取代線性電感」：「非線性 α ≈ −283 MHz 能階不等距」「無耗散 0 Ω 唯一同時非線性又不耗能的元件；二極體、電晶體會耗能而破壞相干」
  「體積極小 ≈10 nH / 0.02 μm² 同樣電感若用線圈要毫米級繞線，還帶來寄生電容與損耗」。
- transmon p8「直覺圖像：量子單擺」：「θ ↔ φ」「U = −mgl cos θ」「EJ/EC 很大，就像又重、擺幅又小的擺：幾乎是簡諧振盪，但頻率會隨振幅略降。這一點點不簡諧，就是量子位元的關鍵。」
- ep049 p11「JJ 登場：把電感 L 換成 JJ」「後果：電感能量原本是平方函數，現在變成 cos 函數」；
  p12「泰勒展開：多出來的四次方項」「−EJ cos φ ≈ −EJ + (EJ/2) φ2 − (EJ/24) φ4 + …」「二次方項：跟 LC 一樣／只留到這裡，能階還是等距的樓梯」
  「四次方項：JJ 獨有／JJ 和電感的主要差別，讓能階變得不等距」；備註「往上 JJ 的位能井比拋物線寬，能階就會愈來愈密。」

## 筆記（notes/transmon-josephson-inductance.md）

- 「所以 JJ 的電壓與電流變化率成正比，行為就是一個電感，只是這個電感值會隨相位 φ 改變。」
- 表「隨電流變化｜L_J(I) = L_{J0} / √(1 − (I/I_c)²)，電流越接近 I_c，電感越大」「φ = π/2（I = I_c）｜L_J → ∞，超過 I_c 後跳到有電壓的耗散態」「無耗散｜在能隙頻率（Al 約 80–100 GHz）以下不吸收能量」。
- 「數值範例：E_J/h = 15 GHz → I_c ≈ 30 nA，L_{J0} ≈ 10.9 nH。」
- 「二極體、電晶體也有非線性，但會耗能，耗能就會破壞量子相干。JJ 是目前已知唯一同時「非線性」又「無耗散」的電路元件。」
- 「約 100 nm × 200 nm 的接面就有約 10 nH。要用線圈做出 10 nH 需要毫米等級的繞線」。
- 表「E₁ − E₀｜5.477 GHz｜5.214 GHz」「E₂ − E₁｜5.477 GHz｜4.931 GHz」「非諧性 α｜0｜−283 MHz」。
- 「E_J/E_C 很大就像一個很重、擺幅很小的擺：它幾乎是簡諧振盪，但因為 cos 位能在邊緣比拋物線平坦，振幅越大頻率越低。這「一點點」不簡諧，就是量子位元的關鍵。」

## 維基百科（原始 wikitext，2026-11-18 取得）

- Josephson effect（Josephson inductance）：「V = \frac{\Phi_0}{2\pi I_c\cos\varphi} \frac{\partial I}{\partial t}=L(\varphi)\frac{\partial I}{\partial t}」「L(\varphi) = \frac{\Phi_0}{2\pi I_c\cos\varphi} = \frac{L_J}{\cos\varphi}」
  「Note that although the kinetic behavior of the Josephson junction is similar to that of an inductor, there is no associated magnetic field. This behaviour is derived from the kinetic energy of the charge carriers, instead of the energy in a magnetic field.」「This phenomenon is also known as kinetic inductance.」
- Pendulum (mechanics)：「== Arbitrary-amplitude period ==」「For amplitudes beyond the small angle approximation, one can compute the exact period……」；
  「=== Arithmetic-geometric mean solution for elliptic integral ===」「T = \frac{2\pi}{M\left(1, \cos\frac{\theta_0} 2 \right)} \sqrt\frac\ell g.」

## 動畫程式

- transmon-3d.html 第 892–897 行（第 2 章）：title「約瑟夫森結：非線性電感的本體」；「下層 Al、中間 1–2 nm 的 AlOx、上層 Al」「拖動相位差 φ：電流 I = I_c sin φ，等效電感 L_J = L_J0 / cos φ」；
  讀數「相位差 φ」「電流 I / I_c」「電感 L_J / L_J0」「L_J0（I_c ≈ 30 nA）≈ 10.9 nH」；滑桿 `<input type="range" id="c2phi" min="0" max="180" step="1" value="35">`、勾選「施加電壓 V ≠ 0（交流約瑟夫森效應）」。
- 同檔第 4128 行 `let jjPhi = 35 * Math.PI / 180`；第 4195–4208 行：`const I = Math.sin(jjPhi)`、庫柏對 `u.s + dt * 0.08 * I`、讀數 `(1 / c).toFixed(2)`、`Math.abs(c) < 0.02 ? "→ ∞"`。
- 同檔第 898–914 行（第 3 章）：title「cos 位能井：能階不再等距」；「cos 井的邊緣比拋物線平坦，量子化後能階越往上越密：0→1 是 5.21 GHz、1→2 只剩 4.93 GHz」；
  按鈕「有 JJ（transmon）」「沒有 JJ（線性 LC）」；「每階都是 √(8E_J E_C) ≈ 5.48 GHz」。第 1218–1222 行讀數「非諧性 α」「−283 MHz」／「0（等距）」。第 545–548 行標籤「−E_J cos φ（JJ）」「拋物線（線性電感）」「相位 φ」「同形的單擺」。
- lc-vs-jj.html 第 263–280 行（第 5 步）：「第 5 步 · 非線性藏在哪裡」「泰勒展開：多出來的四次項」「四次項讓位能比拋物線低（陰影區域），這就是非線性的來源，也是能階變擠的原因。只保留到四次項的近似（灰色點線）已經很貼近真正的餘弦」；
  圖例「1 − cos φ（真正的 JJ）」「φ²/2（只留二次項）」「φ²/2 − φ⁴/24」；第 549 行「四次項造成的差距」。

## 實跑紀錄（pendulum_check.py，Python 3，無套件）

見 `classroom.py` 執行時寫入的 `04_解答.md`；重點：一公尺擺 T0 = 2.006 秒；十次來回 10° 20.10 秒、60° 21.53 秒（多 7.3 %）、90° 週期多 18.0 %；
L_J / L_J0：0.5 Ic → 1.15、0.87 Ic → 2.03、0.98 Ic → 5.03；Ic = 30 nA → L_J0 = 11.0 nH。transmon-3d 能階（Node 實算）：5.21、4.93、4.62、4.25、3.91 GHz；線性 LC 5.48 GHz。
