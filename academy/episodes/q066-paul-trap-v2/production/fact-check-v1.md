# Q066 事實查核

查核日：2026-11-19（內容稿日期標 2026-11-18）。查核者：製作代理（Claude）。逐字引文見 `source-notes.md`。
方法：學程簡報 slides/Ion_NeutralAtom_Talk.pptx 第 7–8 頁（含講者備註）、Q065／Q067 課綱、互動動畫 animations/js/atoms/02_paul.js 由製作代理讀取；
維基百科 Earnshaw's theorem、Ion trap、Wolfgang Paul 以 action=raw 取得 2026-11-19 版本；保羅 1989 年諾貝爾演講 PDF 取自 nobelprize.org 並以 pdftotext 讀取。
數值以 python 驗算（`/home/user/qwork/q066calc/`：calc.py／calc.out、paul_trap_q.py／paul_trap_q.out；paul_trap_q.py 也放進教材）。

| # | 本集的說法（幕） | 依據 | 結論 |
|---|---|---|---|
| 1 | 上一堂比較人造原子和真的原子（1） | academy/lessons/Q065/brief.md「人造原子 vs 真的原子」 | 相符 |
| 2 | 離子阱用真的原子，拿掉一個電子變成帶電離子（1） | ion_talk p9「光游離 399 nm + 369 nm」、講者備註「用兩道雷射把它游離…把電子打掉」；¹⁷¹Yb⁺ 為一價離子 | 相符 |
| 3 | 三步、好玩機制「科學實驗（旋轉鞍面滾球）」、作品「鞍面實驗影片」、生活技能「動態平衡」（2、5、11） | lesson.json 好玩機制、作品／交付、生活技能支線 | 相符 |
| 4 | 1842 年恩紹證明只靠固定電場不能穩定抓住電荷（3） | Earnshaw's theorem 首段「cannot be maintained in a stable stationary equilibrium … solely by the electrostatic interaction … first proven … in 1842」 | 相符 |
| 5 | 空間裡沒有三維谷底，最好是鞍形（3） | Earnshaw's theorem「no local minima or maxima of the field potential in free space, only saddle points」；ion_talk p7「靜電位勢沒有三維極小值」「靜電鞍形：x 方向抓住、y 方向推開」 | 相符 |
| 6 | 射頻讓鞍形快速翻面，離子來不及滑走，被推回（4） | ion_talk p7「鞍形每半週期翻一次」「離子來不及跑掉」；Ion trap「confining and anti-confining directions of the potential are switched faster than the time it takes for an ion to escape」 | 相符 |
| 7 | 每秒來回好幾千萬次（4） | ion_talk p7「RF 電壓（~10–50 MHz）」；02_paul.js desc「每秒翻轉數千萬次」 | 相符（10–50 MHz） |
| 8 | 時間平均成指向中心的碗，叫擬位勢（4） | ion_talk p7「時間平均的擬位勢（pseudopotential）」「結果：一個三維的『碗』」 | 相符 |
| 9 | 保羅和另外兩位科學家共同獲得 1989 年諾貝爾物理獎（4） | Wolfgang Paul「shared one-half of the Nobel Prize in Physics in 1989 … with Hans Georg Dehmelt; the other half … Norman Foster Ramsey」 | 相符 |
| 10 | 諾貝爾演講的機械模型：圓盤上磨出鞍形曲面、小鋼珠；不動時滾下（5） | Paul Nobel lecture p.611「We have machined such a surface on a round disc. If one puts a small steel ball on it, then it will roll down: its position is unstable.」 | 相符 |
| 11 | 合適轉速、每秒幾圈，鋼珠在中心附近小幅晃動、留下（5） | 同上「rotate with the right frequency … (in our case a few turns/s) the ball becomes stable, makes small oscillations and can be kept in position」 | 相符 |
| 12 | 旋轉和翻面效果一樣，每個方向輪流當谷和坡（5） | 鞍形 x² − y² 旋轉 90° 變成 −(x² − y²)，每個方向輪流變成谷與坡；ion_talk p7 標題「用旋轉的鞍形電場」與「翻轉」並用 | 相符（幾何推論） |
| 13 | 轉太慢，鋼珠來不及推回就滾走（5） | q ∝ V/(mΩ²)（Ion trap 方程：2q = 4eV₀/(Mr₀²Ω²)）：轉速越慢 q 越大，超過界線就不穩定；保羅演講「the related Mathieu parameter q be in the permitted range」 | 相符（推論，見未查證事項） |
| 14 | 翻轉參數：電壓越大越大；離子越重、頻率越高越小，頻率是平方（6） | Ion trap：d²xᵢ/dτ² = −(4eV₀/(Mr₀²Ω²)) cos(2τ) xᵢ，與 Mathieu 標準式比較得 q = 2eV₀/(Mr₀²Ω²) | 相符 |
| 15 | 不加直流電壓時 q < 0.908 穩定（6、10） | ion_talk p8「穩定條件（a = 0）：q < 0.908」；python 單週期轉移矩陣跡 \|tr\| < 2 的二分法界線 q = 0.908 | 相符 |
| 16 | 實際操作 q 大多 0.1–0.4（6） | ion_talk p8 講者備註「實際操作在 q 約 0.1 到 0.4 之間」 | 相符（學程簡報） |
| 17 | 兩層運動：大而慢的擺動＋跟著射頻的小而快的抖動（微運動）（7） | Ion trap「secular motion … superimposed by an oscillation at frequency Ω but with small amplitude called micromotion」；ion_talk p8 | 相符 |
| 18 | 慢擺動頻率 ≈ qΩ/(2√2)（7） | ion_talk p8「ωsec ≈ qΩ / (2√2)」；02_paul.js 讀數同式（q 小時的近似） | 相符 |
| 19 | q = 0.4、射頻 30 MHz → 約 4.24 MHz，比射頻慢七倍多（7） | 0.4 × 30 / (2√2) = 4.2426；30 / 4.2426 = 7.07 | 相符 |
| 20 | 線性阱：四根桿，對角一組加射頻、另一組接地，徑向；兩端直流、軸向，離子排成一串（8） | 02_paul.js 標籤「RF 桿（對角一組）」「接地桿」「端蓋 DC（軸向囚禁）」「離子鏈」；ion_talk p7 備註「四根桿子加 RF 提供徑向囚禁，兩端的電極加直流電壓提供軸向囚禁，離子在中間排成一列」；Ion trap 圖說 | 相符 |
| 21 | 表面電極阱，離子浮在表面上方約 50–100 μm（8） | ion_talk p8 表「離子到電極表面距離 ~50–100 μm」、備註「現代的阱大多是做在晶片上的表面電極阱」 | 相符 |
| 22 | 投影片：射頻數十 MHz、數百伏特（8） | ion_talk p8「RF 頻率 10–50 MHz」「RF 振幅 ~100–300 V」 | 相符 |
| 23 | 實驗分工、不轉／慢轉／快轉各三次、安全提醒（9） | lesson.json 動手任務；本課設計 | 課程設計 |
| 24 | 動畫左邊面板有翻轉參數滑桿；下方標籤穩定／逃逸；右下軌跡圖；可關射頻（10） | 02_paul.js 第 92–93 行（q 參數 0.1–1.0、RF 開／關）、第 25、89 行標籤、第 97 行插圖 | 相符 |
| 25 | 120 分鐘流程（11） | lesson.json 2 小時課程流程 | 相符 |
| 26 | 常見誤解：多放電極、配好固定電壓就能抓住；只用靜電場一定做不到（12） | lesson.json 常見誤解「Earnshaw 定理：只用靜電場無法穩定囚禁電荷」 | 相符 |
| 27 | 下一堂：離子阱系統全景，真空腔、雷射、電子系統（12） | academy/lessons/Q067/brief.md 學習目標「認識真空腔、原子源、雷射、成像與電子系統如何連在一起」 | 相符 |

## 動畫段（v2）的數字與畫面

- 02_paul.js info()：讀數 secular = qΩ/(2√2)；q = 0.40、30 MHz → 4.24；q = 0.70 → 7.42；q = 0.40、50 MHz → 7.07；micromotion = Ω/2π。截圖讀數逐字確認（p1、p_q070、p_f50）。
- stable() = rf && q < 0.908：q = 0.95 → 「不穩定：q > 0.908，離子每個週期被推得更遠」；RF 關 → 「不穩定：沒有 RF，鞍形位勢消失，離子直接逃走」（截圖 p_q095、p_rfoff）。
- 插圖曲線（computeCurve，h = 0.02、3000 步、|x| > 5 中止）：q = 0.40 最大 |x| = 0.85（框內 ±1.6）；q = 0.70 約 1.4；q = 0.95 在 τ ≈ 7.2 超過 5（截圖可見衝出圖框）。
- 鞍面振幅 0.32·(q/0.4)·cos 2τ，RF 關時為 0（攤平）；τ 每場景秒 +4，翻面週期 π/4 ≈ 0.79 場景秒。
- 3D 小球出界（|x| 或 |z| > 1.55，以場景同樣的 RK4、h = 4/60/12 驗算）：q ≤ 0.70 不出界；q = 0.75 約 τ = 4.5、q = 0.85 約 τ = 3.9 出界後 1.2 秒重設。
  因此 q 在 0.75–0.90 時標籤寫「穩定」但小球看起來會跑掉（動畫的畫面範圍限制，不是物理不穩定）；動畫段只用 0.40、0.95、0.70，教材另行提醒。
- RF 頻率滑桿只改讀數，不改運動（q 固定）；旁白說「翻轉參數維持零點四」。

## 計算（python，`/home/user/qwork/q066calc/paul_trap_q.out`）

```
q 0.10 +1.951 穩定 … 0.40 +1.213 穩定 … 0.85 −1.512 穩定、0.90 −1.931 穩定、0.95 −2.371 不穩定、1.00 −2.833 不穩定
穩定界線 q ≈ 0.908
q = 0.4、30 MHz → 4.24 MHz；q = 0.4、50 MHz → 7.07 MHz；q = 0.7、30 MHz → 7.42 MHz
```

## 未查證或刻意不說的事

- 「實際操作 q 大多 0.1–0.4」只來自學程簡報講者備註。
- 「轉太慢會滾走」是由 q ∝ 1/Ω² 推論；保羅演講只說要合適的轉速。旁白沒有說「轉太快也不行」。
- 家用轉盤＋紙板鞍面能否真的留住小球，取決於形狀、轉速、摩擦，本集未實測；教材要求孩子記錄觀察，不保證成功。
- qΩ/(2√2) 是 q 小時的近似；q 接近 0.9 時誤差變大，旁白只用 q = 0.4 的例子計算。
