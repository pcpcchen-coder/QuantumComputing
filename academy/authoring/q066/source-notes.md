# Q066 來源筆記（逐字引文）

擷取日：2026-11-19。維基百科以 `index.php?title=…&action=raw` 取得當日版本（API 查 revision id 時被限流，未記 oldid）。
保羅諾貝爾演講 PDF：https://www.nobelprize.org/uploads/2018/06/paul-lecture.pdf（22 頁），以 pdftotext 讀取。

## Earnshaw's theorem（Wikipedia）

- 「Earnshaw's theorem states that a collection of point charges cannot be maintained in a stable stationary equilibrium configuration solely by the electrostatic interaction of the charges. This was first proven by British mathematician Samuel Earnshaw in 1842.」
- 「Therefore, there are no local minima or maxima of the field potential in free space, only saddle points. A stable equilibrium of the particle cannot exist and there must be an instability in some direction.」

## Ion trap（Wikipedia；Paul trap、Quadrupole ion trap 皆重新導向至此）

- 「Due to Earnshaw's theorem it is not possible to confine an ion using only static electric fields. However, … the combination of an oscillating electric field with a static electric field (a Paul trap), can trap ions.」
- 「Named after its inventor Wolfgang Paul, a Paul trap (also known as a quadrupole ion trap) uses static direct current (DC) and radio frequency (RF) oscillating electric fields to trap ions.」
- 「The confining and anti-confining directions of the potential are switched faster than the time it takes for an ion to escape.」
- 圖說：「A radio frequency electric field is applied to the four rods which confines the ion in the two radial directions … Endcap electrodes … generate a trapping potential along the axial direction」
- 「φ = φ₀ + (V₀/2r₀²) cos(Ωt)(x² − y²)」「Defining τ = Ωt/2 … d²xᵢ/dτ² = −(4eV₀/(Mr₀²Ω²)) cos(2τ) xᵢ」
- 「the average trajectory is called "secular motion", and is superimposed by an oscillation at frequency Ω but with small amplitude called "micromotion".」

## Wolfgang Paul（Wikipedia）

- 「He shared one-half of the Nobel Prize in Physics in 1989 for this work with Hans Georg Dehmelt; the other half of the Prize in that year was awarded to Norman Foster Ramsey, Jr.」

## W. Paul, Electromagnetic Traps for Charged and Neutral Particles（Nobel Lecture, 1989，第 611 頁）

- 「The dynamic stabilization in the trap can easily be demonstrated in a mechanical analogue device. In the trap the equipotential lines form a saddle surface as is shown in Fig. 8. We have machined such a surface on a round disc. If one puts a small steel ball on it, then it will roll down: its position is unstable. But if one let the disk rotate with the right frequency appropriate to the potential parameters and the mass of the ball (in our case a few turns/s) the ball becomes stable, makes small oscillations and can be kept in position over a long time. Even if one adds a second or a third ball they stay near the center of the disc. The only condition is that the related Mathieu parameter q be in the permitted range.」
- 圖 8 說明：「Mechanical analogue model for the ion trap with steelball as "particle"」

## 學程簡報 slides/Ion_NeutralAtom_Talk.pptx

- 第 7 頁「Paul 阱：用旋轉的鞍形電場抓住離子」：「Earnshaw 定理：靜電位勢沒有三維極小值，總有一個方向會讓離子跑掉」「靜電鞍形：x 方向抓住、y 方向推開」
  「電極加 RF 電壓（~10–50 MHz）：鞍形每半週期翻一次」「離子來不及跑掉，感受到時間平均的擬位勢（pseudopotential）」「結果：一個三維的『碗』，徑向頻率 ~MHz」「1989 諾貝爾物理獎（Wolfgang Paul）」。
  講者備註：「右邊是實際常用的線性 Paul 阱：四根桿子加 RF 提供徑向囚禁，兩端的電極加直流電壓提供軸向囚禁，離子在中間排成一列。」
- 第 8 頁表格：「RF 頻率 Ω/2π 10–50 MHz」「RF 振幅 ~100–300 V」「徑向 secular 頻率 2–5 MHz」「軸向頻率（由 DC 電極決定）0.2–2 MHz」「離子到電極表面距離 ~50–100 μm」；「ωsec ≈ qΩ / (2√2)」「穩定條件（a = 0）：q < 0.908」。
  講者備註：「q 是一個無因次參數，正比於 RF 電壓、反比於離子質量和 RF 頻率的平方。q 太大會不穩定…實際操作在 q 約 0.1 到 0.4 之間。」「現代的阱大多是做在晶片上的表面電極阱，離子懸浮在表面上方約 50 到 100 微米。」

## 互動動畫 animations/js/atoms/02_paul.js（atoms.html#paul，場景 2／13「Paul 阱原理」）

- 標題「Paul 阱：用振盪電場抓住離子」、副標「靜電場抓不住電荷（Earnshaw 定理），讓鞍形位勢快速翻轉，平均起來就變成一個碗」。
- 控制項：「q 參數」滑桿 0.1–1.0（預設 0.40）、「RF 開 / 關」、「RF 頻率 Ω/2π (MHz)」10–60（預設 30）、「重設離子位置」。
- 3D 標籤：「旋轉鞍形位勢 φ ∝ (x² − y²) cos Ωt」「穩定：被困住」／「不穩定：逃逸」「線性 Paul 阱」「RF 桿（對角一組）」「接地桿」「端蓋 DC（軸向囚禁）」「離子鏈」。
- 插圖「x(τ)：secular 大振盪 + micromotion 小抖動」，穩定時標「慢：secular」「快：micromotion」。

## 課綱

- Q066 lesson.json：動手任務「在旋轉的鞍形曲面（或轉盤上的鞍形紙板）放小球，觀察何時能留住」；孩子獨立改造「在場景改 q 參數，找出穩定與不穩定的界線」；常見誤解「Earnshaw 定理：只用靜電場無法穩定囚禁電荷」。
- Q065「人造原子 vs 真的原子」；Q067「離子阱系統全景」，學習目標「認識真空腔、原子源、雷射、成像與電子系統如何連在一起」。
