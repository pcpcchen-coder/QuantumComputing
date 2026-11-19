# Q069 來源筆記（逐字引文）

擷取日：2026-11-19。維基百科以 `index.php?title=…&action=raw` 取得當日版本（存於 `/home/user/qwork/q069wiki/`，未記 oldid）。

## Normal mode（Wikipedia）

- 「A normal mode of a dynamical system is a pattern of motion in which all parts of the system move sinusoidally with the same frequency and with a fixed phase relation.」
- 「The free motion described by the normal modes takes place at fixed frequencies.」
- 兩個質量、三根彈簧的例子：「Which corresponds to both masses moving in the same direction at the same time.」「This corresponds to the masses moving in the opposite directions, while the center of mass remains stationary.」

## Trapped-ion quantum computer（Wikipedia）

- 「Qubits are stored in stable electronic states of each ion, and quantum information can be transferred through the collective quantized motion of the ions in a shared trap (interacting through the Coulomb force).」
- 「At this very low temperature, vibrational energy in the ion trap is quantized into phonons by the energy eigenstates of the ion strand, which are called the center of mass vibrational modes.」

## Cirac–Zoller controlled-NOT gate（Wikipedia）

- 「…proposed by Ignacio Cirac and Peter Zoller in 1995 … The key idea of the Cirac–Zoller proposal is to mediate the interaction between the two qubits through the joint motion of the complete chain of trapped ions.」
- 「Due to their mutual Coulomb repulsion the ions line up in a linear chain. The ions are cooled to their collective ground state, so that the quantization of the motion of the chain becomes relevant.」
- 步驟：「A red sideband pulse is directed onto ion A … at the end of the pulse the ion is in state g and the chain in its first excited state 1」「A 2π-pulse is applied to the ion B … this changes the phase of the ion B if it is in the state g and the chain is in the first excited state」
  「Another red sideband π-pulse on ion A completes the two-qubit gate. This returns ion A and the motion of the chain to its initial state.」
- 「The Cirac–Zoller gate was experimentally first realized in 2003 (in slightly modified form) at the University of Innsbruck … using two calcium ions.」

## 學程簡報 slides/Ion_NeutralAtom_Talk.pptx 第 17 頁「集體振動：離子之間的『量子匯流排』」

- 「離子之間有很強的庫侖排斥 → 一起振動，形成 N 個正規模」「COM 模：全部一起動，頻率 = ωz；breathing 模：√3 ωz」
  「任一顆離子被雷射『推』，振動會傳到整條鏈 → 同一鏈內任兩顆都能直接做閘（全連接）」「代價：N 變大 → 模態擁擠、離子變重 → 閘變慢、加熱與串擾變嚴重」
  「一條鏈約 20–30 顆以內最好用；更多量子位元需要把鏈拆開 → QCCD 或光子互連。」
- 講者備註：「N 顆離子在軸向有 N 個正規模：最低的是質心模，所有離子一起左右擺動，頻率等於單顆離子的軸向頻率；第二個是呼吸模，頻率是根號三倍」
  「這些共同的振動模態就像一條『量子匯流排』：用雷射推任何一顆離子，振動就會傳到整條鏈上的每一顆離子。所以同一條鏈裡任何兩顆離子都可以直接做兩位元閘，這叫全連接」
  「離子數變多，模態越來越擠，彼此難以分辨；整條鏈變重，閘變慢；加熱和串擾也更嚴重。實務上一條鏈大約二、三十顆以內最好用」。
  備註提到「右上的圖是模態頻率隨離子數的變化」；現行動畫的頻率譜在右下、畫的是目前離子數的頻率，本集依動畫原始碼描述。

## 互動動畫 animations/js/atoms/04_modes.js（atoms.html#modes，場景 4／13「離子鏈的集體振動：量子匯流排」）

- 副標：「離子之間靠庫侖力連在一起，像彈簧串起的珠子；共享的振動模態就是傳遞量子資訊的『匯流排』」。
- 說明：「平衡位置：軸向是諧振位勢（頻率 ω_z），離子又互相排斥，於是排成一列，中間較密、兩端較疏。」
  「軸向：最低的是 COM（質心）模，所有離子一起動，頻率 = ω_z；第二個是呼吸模，頻率 = √3 ω_z（與 N 無關）。徑向：COM 頻率最高 = ω_r，其他模往下排。」
  「雷射可以讓『某顆離子的自旋』推動『整條鏈的某個模態』，模態再影響另一顆離子 → 同一條鏈裡任兩顆離子都能直接做兩位元閘（全連接）。」
  「N 變大時模態越擠越密、雷射難以單獨定址，閘也變慢；ω_r/ω_z 不夠大時鏈會折成鋸齒形。所以大系統把離子分成很多短鏈，靠搬運（QCCD）或光子互連連接。」
- 控制項：按鈕「軸向模態」「徑向模態」；滑桿「離子數 N」2–12（預設 5）、「模式編號」1–12（預設 1）、「徑向/軸向頻率比 ω_r/ω_z」1.5–10（預設 5）。
- 標籤：「COM（質心）模」「呼吸模（breathing）」「徑向 COM 模」「徑向傾斜（rocking）模」＋「ω = … ω_z」；
  「箭頭 = 各離子在此模態中的相對位移（沿軸向）」；「⚠ ω_r/ω_z 太小：最低徑向模頻率變虛數 → 鏈折成鋸齒形（zigzag）」。
- 讀數：「軸向：COM = 1.000 ω_z、呼吸 = 1.732 ω_z（≈ √3）、最高 = … ω_z」「徑向（ω_r = 5 ω_z）：COM = 5.000 ω_z、最低 = …」「相鄰徑向模最小間距：… ω_z（越小越難單獨定址）」。
- 插圖「模態頻率譜（藍：軸向，紅：徑向）」，文字「軸向 COM」「徑向 COM」「徑向模擠在 ω_r 下方」。

## 課綱

- Q069 lesson.json：動手任務「全家排成一列手拉手，示範質心模與呼吸模」；孩子獨立改造「在場景增加離子數，觀察模式頻率怎麼擠在一起」；好玩機制「角色扮演（人肉離子鏈）」；
  作品「正規模觀察表」；生活技能「群體運動與個別運動」；常見誤解「離子越多，模式越擠，閘越難做得又快又準」。
- Q068「¹⁷¹Yb⁺ 量子位元與雷射冷卻」，學習目標含超精細量子位元、Doppler 冷卻、光泵浦初始化。
- Q070「Mølmer–Sørensen 閘」，學習目標「理解自旋相依力讓運動在相空間繞一圈，留下糾纏」。
