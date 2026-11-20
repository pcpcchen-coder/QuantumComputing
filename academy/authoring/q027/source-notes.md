# Q027 來源筆記（逐字引文）

查核日：2026-11-18。課綱、簡報、動畫程式、課程文件由製作代理讀取。程式由製作代理實際執行。

## 課綱（academy/lessons/Q027/lesson.json）

- 課程主題「SQUID：用磁場轉頻率」；階段「第二階段 硬體怎麼做」；模組「QM02 超導量子位元：從超導到 transmon」。
- 學習目標「知道兩個 JJ 並聯成環可以用磁通調整頻率，認識甜蜜點」。
- 動手任務「在場景把量子位元調到指定頻率，並找出對磁通雜訊最不敏感的點」；孩子獨立改造「比較對稱與不對稱 SQUID 的調頻範圍」；好玩機制「闖關（調到指定頻率）」。
- 作品「調頻曲線」；家長課前準備「index.html#squid」；生活技能支線「在可調性與穩定性之間取捨」。
- 常見誤解與安全提醒「可調 = 多一個雜訊入口；甜蜜點是一階不敏感，不是完全不受影響」。
- 沿用簡報頁：JJ_Microwave_Readout_Talk.pptx p17；transmon.pptx p21；沿用 3D 場景：i:squid、tr:case；沿用文件：超導量子電腦師生對話教學紀錄 第 1–3 課。
- Q026 brief：「傾斜洗衣板」「在場景加大偏壓電流，記錄粒子何時從井中滑出」。Q028 brief：「量子位元家族圖鑑」「比較 transmon、fluxonium、電荷與相位量子位元的結構與優缺點」。

## 簡報（python-pptx 擷取）

- JJ_Microwave_Readout_Talk p15 表：「約瑟夫森能 EJ｜EJ = Φ0 Ic / 2π = ħ Ic / 2e｜Cooper pair 穿隧的耦合能（位勢深度）｜接面面積、氧化層 → Ic」「充電能 EC｜EC = e² / 2CΣ｜……｜總電容 CΣ（含大電容板）」。
- JJ_Microwave_Readout_Talk p17「SQUID：用磁通調整的 JJ」「EJ(Φ) = EJΣ |cos(πΦ/Φ0)| · √(1 + d² tan²(πΦ/Φ0))」；重點「兩個 JJ 並聯成環 = 一個臨界電流可調的 JJ」「用晶片上的 Z 線通電流產生磁通 → 即時調頻」
  「甜蜜點 Φ = 0：df/dΦ = 0，對磁通雜訊一階免疫」「不對稱 SQUID 縮小調頻範圍、降低雜訊敏感度」；
  備註「如果把兩個 JJ 並聯成一個小環，就是 DC SQUID。由於磁通量子化，穿過環的磁通會讓兩個 JJ 的相位產生干涉，整體效果等於一個『臨界電流可以用磁通調整』的 JJ，週期剛好是一個 Φ0。」
  「在量子晶片上，每顆量子位元旁邊會有一條 Z 控制線，通一點電流就能改變穿過 SQUID 的磁通，進而在奈秒尺度內調整量子位元頻率。這被用來做雙量子位元閘（把兩顆調到共振）、或是避開有缺陷的頻率。」
  「對稱 SQUID 在半個 Φ0 處頻率會掉到零；不對稱 SQUID 的調頻範圍比較小，但曲線比較平，對磁通雜訊比較不敏感。曲線最高點的地方叫甜蜜點，斜率為零，對磁通雜訊一階免疫，通常讓量子位元停在這裡。」
- transmon.pptx p20「案例：三顆可調 transmon 的頻率配置」「② SQUID 調頻　E_J(Φ) = E_J,max |cos(πΦ/Φ₀)|，用 Z 線磁通把頻率往下調。」「③ 頻率配置　Q2 留在 sweet spot（5.10 GHz）……」；
  備註「剛做好時頻率散亂，用 SQUID 加 Z 線磁通把頻率調開，給每顆位元一個地址」。
- transmon.pptx p21（課綱所列頁）實際是「振幅長條：糾纏、Grover 與 Deutsch」（第 7 章），與本課無關，改用 p20。

## 課程文件（docs/超導量子電腦師生對話教學紀錄.md）

- 第 1 課：「電流從左邊進來，分成兩條路，各穿過一個 JJ，再在右邊匯合，很像雙狹縫干涉。」「外加磁通 Φ 穿過迴路時，兩條路徑累積不同的相位」「SQUID 能承載的最大超電流是 I_c(Φ) = 2I_c₀|cos(πΦ/Φ₀)|」
  「可調 transmon 的代價：磁通雜訊會變成頻率抖動（dephasing）。對策是待在 sweet spot（Φ = 0，df/dΦ = 0），或用不對稱 SQUID（調頻範圍變小，但整段對雜訊較不敏感）。」
  「SQUID 用量子干涉，把『磁通』轉換成『臨界電流（也就是 E_J 和電感）』。」
- 第 2 課：「頻率旋鈕：兩個 JJ 圍成迴路，Z 線的磁通……讓 E_J(Φ) = E_J,max|cos(πΦ/Φ₀)|。」
- 第 3 課：「限制是只能往下調（最高在 Φ = 0），所以 E_J 要刻意做大一點；離 sweet spot 越遠 T₂ 越差。」表「非諧性（≈ −E_C）｜十字電容幾何｜❌」；「產業兩條路線：可調頻率（Google、祖沖之）vs 固定頻率＋可調耦合器或微波閘（IBM）」。

## 維基百科 SQUID（原始 wikitext，2026-11-18 取得）

- 「A SQUID (superconducting quantum interference device) is a very sensitive magnetometer used to measure extremely weak magnetic fields, based on superconducting loops containing Josephson junctions.」
- 「The DC SQUID was invented in 1964 by Robert Jaklevic, John J. Lambe, James Mercereau, and Arnold Silver of Ford Research Labs」「It has two Josephson junctions in parallel in a superconducting loop.」
- 圖說「Periodic voltage response due to flux through a SQUID. The periodicity is equal to one flux quantum, Φ0.」

## 動畫程式

- animations/js/scenes/06_squid.js（index.html#squid）：第 4 行標題「DC SQUID：可用磁通調整的 JJ」；第 6–8 行說明「整個 SQUID 就像一個臨界電流可調的 JJ」「E_J 隨 Φ 以 Φ₀ 為週期變化」
  「甜蜜點（sweet spot）：Φ = 0 處 df/dΦ = 0，對磁通雜訊一階不敏感。非對稱 SQUID（d ≠ 0）可縮小調頻範圍、降低雜訊敏感度。」；
  第 44–50 行 EC = 0.25、EJS = 20、f01 = √(8·E_J·E_C) − E_C、E_J = EJS√(cos² + d² sin²)；第 45 行初值 flux = 0.25、d = 0；
  第 51–52 行滑桿「外加磁通 Φ / Φ₀」（−1～1、0.005）、「接面不對稱度 d = (E_J1 − E_J2)/(E_J1 + E_J2)」（0～0.8、0.01）；第 54 行按鈕「自動掃描磁通」；
  第 57–63 行小圖「量子位元頻率 f₀₁ 與外加磁通（E_JΣ/h = 20 GHz, E_C/h = 250 MHz）」，灰色 d = 0 曲線、金色目前曲線、青點、「甜蜜點」字；
  第 81–82 行讀數「等效 E_J/h」「f₀₁ ≈ √(8E_JE_C) − E_C = <b>…GHz</b>」「磁通敏感度 df/dΦ = … GHz/Φ₀」與「（甜蜜點：對磁通雜訊一階免疫）」。
- animations/transmon-3d.html 第 6 章 #case（第 940–948 行分頁、第 1285 行起步驟腳本）：步驟 ② 字幕「E_J 變小 → f₀₁ 下降。最高點 Φ = 0 就是 sweet spot，所以頻率只能往下調。」（第 1305 行）
  「離開 sweet spot 時，磁通雜訊讓頻率抖動（dephasing）；回到 Φ = 0，抖動就消失。」（第 1306 行）。

## 實跑紀錄（squid_tuning.py，Python 3，無套件）

見 `classroom.py` 執行時寫入的 `04_解答.md`；重點：Φ = 0 → 6.075 GHz（斜率 0.00）；0.02 → 6.068（−0.62）；0.1 → 5.918；0.19 → 5.502；0.25 → 5.068（−8.35）；
抖 0.01 Φ₀：Φ = 0 差 1.6 MHz、Φ = 0.25 差 86 MHz；0 → 0.02 降 6.2 MHz；d = 0.6：0.25 → 5.493（−4.25）、谷底 4.649、範圍 1.426 GHz。與 Node 以場景公式實算的讀數相同。
