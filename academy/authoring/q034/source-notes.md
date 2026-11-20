# Q034 來源筆記（逐字引文）

查核日：2026-11-18。課綱、簡報、筆記、動畫程式由製作代理讀取（簡報以 python-pptx 擷取投影片文字與講者備註）；維基百科頁面由製作代理開啟（action=raw）。程式由製作代理實際執行。

## 課綱（academy/lessons/Q034/lesson.json）

- 課程主題「電路 QED：量子位元＋諧振腔」；階段「第二階段 硬體怎麼做」；模組「QM03 讀取量子位元與周邊系統」，模組內課次 2。
- 學習目標「知道讀取是透過共振腔「間接」看量子位元」。
- 動手任務「用兩個音叉或兩條橡皮筋示範耦合；在場景指出量子位元與讀取腔」；孩子獨立改造「畫出量子位元、讀取腔、饋線三者的連接圖」；好玩機制「角色扮演」。
- 作品「電路 QED 示意圖」；家長課前準備「音叉或橡皮筋；index.html#chip；notes/dispersive-readout.md」；生活技能支線「透過「代理」間接量測」。
- 常見誤解與安全提醒「讀取腔與量子位元頻率要分得夠開，才不會直接交換能量」。
- 沿用簡報頁：JJ_Microwave_Readout_Talk.pptx p27、transmon.pptx p16；沿用 3D 場景：i:chip。
- Q033 brief：「讀取要快、準、不破壞」「說出讀取量子位元的三個條件：時間 ≪ T₁、高保真度、量子非破壞」。
- Q035 brief：「色散位移 ±χ」「理解腔頻率會隨量子位元狀態偏移 ±χ，並能從 S21 判讀狀態」。

## 簡報（slides/JJ_Microwave_Readout_Talk.pptx）

- p26「讀取要滿足什麼條件？」：「可擴展、低串擾 多顆量子位元共用線路（頻率多工），讀取不干擾相鄰量子位元」
  「解法：讓量子位元間接影響一個諧振腔，再用微波「探測」諧振腔 → 這就是色散讀取（dispersive readout），目前超導量子電腦的標準方法」。
  備註：「所以實際的作法是讓量子位元去「間接」影響一個諧振腔，我們再用微波去探測這個諧振腔——這就是色散讀取。」
- p27「電路 QED：量子位元 + 讀取諧振腔」：表格「原子腔 QED | 電路 QED」「原子 | Transmon（人造原子）」「光學共振腔 | CPW 微波諧振腔」
  「光子（可見光） | 微波光子（~7 GHz）」「耦合 g ~ kHz–MHz | g/2π ~ 50–200 MHz」；「λ/4 諧振腔長度約 4 mm（矽基板上）→ fr ≈ 6–8 GHz」；
  「HJC = ħωr a†a + ½ħωq σz + ħg (a†σ− + aσ+)」。
  備註：「它的概念借自原子物理：把一顆原子放進一個光學共振腔，研究原子和光子的交互作用。在超導電路裡，原子換成 transmon 這種「人造原子」，光學腔換成一段共平面波導做成的微波諧振腔。」
  「第三項是兩者以耦合強度 g 交換能量。電路 QED 的優勢是耦合可以做得非常強，g 可以到一兩百 MHz，比原子系統大好幾個數量級。」
  「這是一個四量子位元的晶片模型。每個十字形就是一顆 Xmon，也就是十字形的 transmon，上端的紅色小環是 SQUID。每顆量子位元下方有一條彎來彎去的線，
  那是四分之一波長的讀取諧振腔，大約 4 毫米長，共振頻率大約 7 GHz。所有讀取諧振腔都耦合到最下方同一條饋線。」
  （注意：備註的「上端」「下方」「最下方」是以晶片座標描述；在場景預設視角的畫面上，饋線在最上方、SQUID 小環在十字下方，旁白依畫面描述。）
- p28「色散區域：諧振腔頻率依狀態偏移 ±χ」：「當 |Δ| = |ωq − ωr| ≫ g（色散區域）」「ωq ≈ 5 GHz」「Δ ≈ −2 GHz」「ωr − χ |0⟩」「ωr + χ |1⟩」
  「失諧很大 → 不交換能量，只互相「推」頻率」「諧振腔頻率成為量子位元狀態的「指示器」」「量測只碰諧振腔，量子位元狀態不被翻轉 → QND」。
  備註：「例如量子位元 5 GHz、諧振腔 7 GHz，失諧 Δ 大約負 2 GHz，遠大於耦合 g。在這個條件下，兩者不會真正交換能量，而是互相「推」對方的頻率。」
- p29「讀取原理：穿透訊號的振幅與相位」：「送入頻率在 ωr 附近的微波脈衝」「穿透（或反射）後的訊號相位依狀態不同」「放大、解調 → 得到 (I, Q)」。
  備註：「我們送一個頻率在 ωr 附近的微波脈衝穿過諧振腔，量測出來的穿透訊號。」「在振幅圖上，兩條 Lorentzian 曲線左右錯開；在相位圖上，兩條相位曲線也錯開。」

## 簡報（slides/transmon.pptx）

- p16「控制與讀取（電路量子電動力學）」：「色散讀取 χ/2π ≈ −0.77 MHz 共振腔頻率依位元狀態偏移，量反射訊號的相位判斷 |0⟩ 或 |1⟩」。

## 學程筆記（notes/dispersive-readout.md）

- §0：「量子位元不直接量。我們把它耦合到一個微波諧振腔，量子位元的狀態會讓諧振腔的頻率往左或往右偏一點。」
  「可以想成在敲一個鈴：鈴裡面的東西（量子位元）不同，敲出來的音高就不同。我們只聽音高，不去打開鈴。」
- §1：「色散讀取是 QND 量測：它不交換能量，只讓頻率偏移」。
- §2.1：表格「ω_r 諧振腔頻率 6–8 GHz」「ω_q 量子位元頻率 4–6 GHz」「g 耦合強度 g/2π ≈ 50–200 MHz」「κ 諧振腔線寬（光子漏到外面傳輸線的速率） κ/2π ≈ 0.5–10 MHz」。
- §2.2：「條件是失諧量遠大於耦合強度：|Δ| = |ω_q − ω_r| ≫ g」「這時兩者不會真正交換能量（不做真空 Rabi 振盪），只會互相「推」頻率。」
- 文首：「文中的數值範例統一使用 ω_q/2π = 5 GHz、ω_r/2π = 7 GHz、g/2π = 100 MHz、α/2π = −250 MHz。」

## 維基百科

- Sympathetic resonance：「The classic example is demonstrated with two similarly-tuned tuning forks. When one fork is struck and held near the other, vibrations are induced in the unstruck fork, even though there is no physical contact between them.」
  「The effect is most noticeable when the two bodies are tuned in unison or an octave apart」「coupled oscillators, in this case coupled through vibrating air」。
- Circuit quantum electrodynamics：「As in the field of cavity quantum electrodynamics, a single photon within a single mode cavity coherently couples to a quantum object (atom). In contrast to cavity QED, the photon is stored in a one-dimensional on-chip resonator and the quantum object is no natural atom but an artificial one.」
  「superconducting coplanar waveguide microwave resonators」。

## 互動動畫程式（animations/）

- index.html：第 47 行載入 `js/scenes/08_chip.js`。
- js/scenes/08_chip.js：`id: 'chip'`（第 3 行）；title「電路 QED 晶片：量子位元 + 讀取諧振腔」（第 4 行）；
  說明「Xmon（十字形 transmon）：十字形電容板 + 一端的 SQUID/JJ 接地。十字的四臂分別耦合到讀取諧振腔、XY 驅動線、Z 磁通線與鄰近量子位元。」（第 6 行）
  「λ/4 讀取諧振腔：一段彎曲的共平面波導（CPW），長度約 4 mm → 共振頻率約 6–8 GHz。一端靠近量子位元（電容耦合 g），另一端靠近饋線（耦合率 κ）。」（第 7 行）
  「頻率多工：每個諧振腔長度略有不同（頻率差數十 MHz），所以一條饋線送入「頻率梳」就能同時讀取多個量子位元。」（第 8 行）；
  相機 `pos: [0, 10.5, 9.5], target: [0, 0, 0.3]`（第 10 行）；饋線 `feedZ = -2.7`、x −6 到 6（第 25–27 行）；標籤「讀取饋線 IN」「OUT → 放大器」（第 29–30 行）；
  `FR = [6.82, 6.97, 7.11, 7.26]`（第 33 行）；`qColor = (s) => (s ? 0xff5a5f : 0x4f8cff)`（第 34 行）；讀取腔 emissive `0x38c6d9`（第 46 行）；
  耦合爪 z = 1.2（第 57 行）；SQUID 環 `0xff7a59`、`cz + arm + 0.2`（第 59–60 行）；標籤 `Q${i + 1}`（第 64 行）、「Xmon 量子位元」「SQUID / JJ」「XY 驅動線」「Z 磁通線」「λ/4 讀取諧振腔」（第 67–71 行）；
  封包 7 顆小球、顏色 `pcol`（第 75、80 行）；按鈕 `Q${i + 1}: |0⟩`、按下 `state ^= 1`（第 86 行）；「▶ 多工讀取（4 個頻率同時）」「只讀 Q2」（第 88–89 行）；
  `ui.toggle('自動重複讀取', true, …)`（第 91 行）；「視角：全晶片」「放大 Xmon」「放大饋線耦合」（第 93–95 行）；`chi = 0.004, kap = 0.006; // GHz（示意放大）`（第 97 行）；
  插圖「饋線穿透 |S21| 頻譜（4 個諧振腔的吸收凹陷）」（第 99 行）、`fr = q.f + (q.state ? chi * 6 : -chi * 6)`（第 101 行）、金色曲線（第 102 行）、彩色虛線（第 104 行）、`Q${i + 1}:|${q.state}⟩` 文字（第 105 行）；
  `tSend = 4.5`（第 113 行）；封包速度 `dt * 3.2`（第 115 行）、只點亮 `qubits[p.i]`（第 116–117 行）、x > 6.6 移除（第 118 行）；amp 衰減 `dt * 0.6`（第 121 行）、閃動 `sin(time * 18)`（第 122 行）；
  讀數「Q…：f_r = … GHz，狀態 |…⟩ → 腔頻 ±χ」「典型 κ/2π ≈ 1–5 MHz，2χ/2π ≈ 1–5 MHz」（第 125–126 行）。
- js/core.js：`flyTo(pos, target, dur = 1.2)`（第 55 行）；左側面板顯示時視角右移 180 px（第 235–236 行）；ui 控制項都放進 `#controls`（第 338–370 行）；
  Plot.frame 邊界 l 46、r 12（第 403–405 行）；插圖畫布 380 × 230（第 390–395 行）。
- css/style.css：`#panel` 在左、可捲動（第 32 行）；`#inset-wrap` 在右下（第 56–59 行）；`.lbl` 以標籤中心定位（第 11 行）。

## 重新計算（cqed_check.py，製作代理實跑）

```
|Δ|/g：5 GHz 對 7 GHz、g = 100 MHz → 20（色散區域）；6.95 對 7.0 → 0.5（太接近）
動畫四個讀取腔：6.82、6.97、7.11、7.26 GHz，相鄰間隔 150、140、150 MHz
右下 |S21| 頻譜：每 GHz 約 474 px；凹陷偏離虛線 24 MHz ≈ 11.4 px；切換一顆移動約 22.7 px；凹陷半深度寬約 5.7 px
```
螢幕座標（three.min.js 在 Node 投影 1600×900，含 180 px 視角右移）：見 `v2/demos_extra/q034.py` 檔頭。
