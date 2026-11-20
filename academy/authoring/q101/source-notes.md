# Q101 來源筆記（逐字引文）

查核日：2026-11-18。維基百科頁面由製作代理開啟（revision id 取自頁面的永久連結）。學程內部文件、簡報與動畫程式由製作代理讀取。程式由製作代理實際執行。

## Transmon（Wikipedia，oldid=1377984572）

- 「designed to have reduced sensitivity to charge noise」
- 「This is accomplished through the use of a large shunting capacitor.」
- 「The disadvantage is the reduced anharmonicity」

## SQUID（Wikipedia，oldid=1379580433）

- 「based on superconducting loops containing Josephson junctions」
- 「It has two Josephson junctions in parallel in a superconducting loop.」
- 「The periodicity is equal to one flux quantum, Φ0.」

## Superconducting quantum computing（Wikipedia，oldid=1382042448）

- 「Individual qubits may be addressed by a dedicated transmission line or by a shared one if the other qubits are off resonance.」
- 「tuning out of resonance one from another, making the energy gaps between their computational states different.」
- 「This method relies on the frequency tunability of the qubit, and does not work in fixed-frequency cases.」
- 「are induced by microwave pulses sent to an antenna or transmission line coupled to the qubit.」
- 「cooled in dilution refrigerators below 15 mK」

## 學程內部文件：docs/超導量子電腦師生對話教學紀錄.md

- 第 3 課學生原話：「你的意思是說～我用 XY 驅動線寫入我要的量子狀態，讓十字電容跟 JJ 來回振盪（變成量子位元），然後 SQUID 是用來修正製程差異用的！只要控制好 Z，我就可以得到數個特性接近的量子位元？」
- 「大方向對，但有三處要修正，第三點最重要：實務上不會把位元調成「特性一樣」，反而刻意排在不同頻率。」
- 修正二：「SQUID 的用途有：修製程誤差（JJ 氧化層差幾個原子，頻率可偏約 100 MHz）、閃避會飄移的 TLS、做 CZ。限制是只能往下調（最高在 Φ = 0），所以 E_J 要刻意做大一點；離 sweet spot 越遠 T₂ 越差。」
- 修正三表格：頻率 f₀₁ ✅；非諧性（十字電容幾何）❌；T₁、T₂（材料、介面缺陷、雜訊）❌；耦合強度 g（電容幾何）❌；讀取腔頻率、χ（共振腔設計）❌。
- 「頻率一樣反而是災難：相鄰同頻會共振交換能量（串擾），XY 脈衝也分不出要打哪一顆。所以要做頻率配置，平常各自停在不同頻率；要做雙位元閘時，才用 Z 脈衝短暫拉到共振。」
- 「樂團比喻：Z 是調音師，任務是把每把樂器調到各自分配到的音；要合奏（雙位元閘）時，指揮才讓兩把樂器短暫對上同一個音。」
- 「「不一樣」不是問題，「不穩定」才是問題。」
- 第 2 課 Step 0：「晶片在 10–20 mK，熱能約 0.2–0.4 GHz，遠小於 5.21 GHz，靜置後 > 99% 在 |0⟩。」
- 動畫演示：「第 6 章 案例 步驟 1–2：三顆位元頻率因製程散開又互撞；SQUID 調頻只能往下、離開 sweet spot 會抖動。」

## 學程內部簡報：slides/transmon.pptx 第 20 頁

- 標題「案例：三顆可調 transmon 的頻率配置」；「① 製程誤差 JJ 氧化層差幾個原子，E_J 就差好幾 %，三顆頻率散亂、互相碰撞。② SQUID 調頻 E_J(Φ) = E_J,max |cos(πΦ/Φ₀)|，用 Z 線磁通把頻率往下調。③ 頻率配置 …④ XY 寫入 頻率錯開，對準 f₀₁ 的脈衝才不會串擾到鄰居。⑤ CZ 閘 把 Q3 推到 f_Q2 − α，|11⟩ 繞一圈多一個 −1 相位。⑥ 自由實驗 自己拖三條 Z 線，製造或消除碰撞。」
- （課綱寫 p21；第 21 頁實為「振幅長條：糾纏、Grover 與 Deutsch」。）

## 動畫程式：animations/transmon-3d.html 第 6 章

- `const QC = { EC: 0.25, alpha: -0.283, d: 0.013, EJmax: [14.49, 14.381, 15.978] };   // sweet spot 頻率 5.12 / 5.10 / 5.39 GHz（製程誤差）`
- `const ALLOC = [phiFor(0, 4.90), 0, phiFor(2, 5.30)];`；`const WIN = { same: 0.03, x12: 0.025, tp: 0.012 };   // 碰撞判定窗（GHz，示意）`
- applyPi：「π 脈衝打 Q_k：其他位元看到洩漏的驅動（相鄰 60%、隔一顆 25%，示意）」
- startCZ：「Q3 推到 f_Q2 − α，|11⟩ ↔ |20⟩ 共振一個週期」；包絡 1 s 上升、3 s 停留、1 s 下降；`cplMat[1].emissiveIntensity = 0.9 * czEnv`
- 步驟 5 字幕：「這正是平常要避開的禁區：做閘時才刻意去，而且只停留幾十 ns。」
- 自由實驗按鈕：`π → Q1`（data-pi="0"）、`CZ（Q2–Q3）`（#c6cz）、`回到配置`（#c6alloc）、`回到製程原貌`（#c6raw）；滑桿 #c6phi0–2（0–0.3 Φ₀）；步驟按鈕在 #c6steps；「暫停」#c6play、「重播」#c6re、「自動接續」#c6auto。
- 製作代理用同公式重算：製程原貌 5.1203／5.1000／5.3900 GHz、碰撞 3 處；π → Q1 時 Q2 P₁ = 0.353；Q1 Φ = 0.2 時 4.579 GHz；CZ 交會點 5.383 GHz。

## 實跑紀錄（freq_case.py，Python 3.13）

```
製程原貌（三顆都在 Φ = 0）：Q1 5.120 GHz  Q2 5.100 GHz  Q3 5.390 GHz
    Q1–Q2 同頻（差 20 MHz）；Q2 0→1 ≈ Q3 1→2；旁觀者：Q1 0→1 ≈ Q3 1→2
迷思：全部調成 5.100：Q1 5.100 GHz  Q2 5.100 GHz  Q3 5.100 GHz
    Q1–Q2 同頻（差 0 MHz）；Q2–Q3 同頻（差 0 MHz）；旁觀者：Q1 ≈ Q3
棋盤格（Q1 = Q3 = 4.90）：…  旁觀者：Q1 ≈ Q3
頻率配置（4.90／5.10／5.30）：…  無碰撞
Q2 想往上調到 5.20 GHz： None （None = 做不到，只能往下調）
```
