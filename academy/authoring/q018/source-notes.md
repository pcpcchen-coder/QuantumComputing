# Q018 來源筆記（逐字引文）

查核日：2026-11-18。課綱、簡報與動畫程式由製作代理讀取；維基百科兩頁由製作代理開啟摘錄。本集沒有計算程式。

## 課綱（academy/lessons/Q018/lesson.json）

- 課程主題「超導：電阻消失、磁鐵懸浮」；模組「QM02 超導量子位元：從超導到 transmon」，模組內課次 2；學習目標「知道超導的兩個特徵：零電阻與排斥磁場」。
- 動手任務「觀看懸浮影片並記錄現象；用場景的溫度滑桿對照正常態與超導態」；孩子獨立改造「查三種超導材料的臨界溫度，排出順序」；好玩機制「科學實驗（觀察紀錄）」。
- 作品「超導觀察筆記」；家長課前準備「安全的超導懸浮影片；index.html#cooper」；沿用簡報頁「JJ_Microwave_Readout_Talk.pptx p7」；沿用 3D 場景「i:cooper」。
- 常見誤解與安全提醒「液態氮會凍傷，本課只看影片，不在家操作」；生活技能支線「分辨「觀察」與「推論」」。
- Q017 brief：「為什麼要做「人造原子」」。Q019 brief：「Cooper pair 與能隙」「全家當晶格原子，一人走過時大家靠近，讓第二個人被「吸」過來」。

## 簡報（slides/JJ_Microwave_Readout_Talk.pptx）

- p7「超導現象：零電阻與完全抗磁」：「零直流電阻｜低於臨界溫度 Tc，電流可在超導環中流動多年不衰減。」「Meissner 效應｜磁場被完全排出超導體內部（完全抗磁），只在表面穿透深度 λ ~ 50–100 nm 內存在。」
  「臨界溫度 Tc｜Al ≈ 1.2 K、Ta ≈ 4.5 K、Nb ≈ 9.2 K、NbTiN ≈ 14 K。量子電路在 10 mK 工作 ≪ Tc。」「3D 場景 2：低於 Tc 時電子配對、整體同步流動」
- p8「BCS 理論：Cooper pair 與能隙」：「電子經過時吸引正離子 → 晶格局部扭曲（聲子）→ 吸引第二顆電子」（留給 Q019）。

## 維基百科

- Superconductivity：「Superconductivity was discovered in solid mercury on April 8, 1911, by Heike Kamerlingh Onnes.」約 4.2 K 時「the resistance abruptly disappeared」；
  「currents in superconducting coils can persist for years without any measurable degradation」；Meissner 與 Ochsenfeld 1933；「the complete cancellation of the magnetic field in the interior of the superconductor」；
  YBCO「raised the critical temperature to about 93 K」，液態氮沸點 77 K；懸浮：「This current effectively forms an electromagnet that repels the magnet.」圖說「Video of superconducting levitation of YBCO」。
- Meissner effect：「The German physicists Walther Meissner and Robert Ochsenfeld」「in 1933」；「the expulsion of a magnetic field from a superconductor during its transition to the superconducting state」；
  「when a material transitions to a superconducting state in a constant magnetic field, it actively expels magnetic flux」；完美導體「has no mechanism for flux expulsion」；
  「it penetrates a short distance from the surface, characterized by the London penetration depth」；「subsequent levitation of a magnet above an already superconducting material does not demonstrate the Meissner effect」。

## 互動動畫程式（animations/js/scenes/02_cooper.js，index.html 第 41 行載入）

- 第 3–8 行：id 'cooper'；title「超導體：Cooper pair 與零電阻」；desc「低於臨界溫度 Tc（鋁約 1.2 K）時……整體同步移動，不再被晶格散射 → 直流電阻為零」。
- 第 13 行離子 0xe0a54a；第 27 行 `NP = 10`；第 29 行 `U.glow(0x6fb4ff), U.glow(0x9d7bff)`；第 34 行連線 0x8ef0ff；第 39–40 行標籤「Cooper pair（↑↓ 電子對）」「正離子晶格（Al）」。
- 第 43–45 行：`let T = 0.3; const Tc = 1.2;`、`ui.slider('溫度 T (K)', 0.05, 3, 0.05, T, …)`、`ui.radio([[0.3, '超導態 0.3 K'], [2.5, '正常態 2.5 K']], …)`。
- 第 48–52 行：插圖「電阻 R 對溫度 T（鋁，Tc ≈ 1.2 K）」，`R = (t) => (t < Tc ? 0 : 1 + 0.08 * (t - Tc))`，青點 #38c6d9。
- 第 59–62 行：`frac = sc ? 1 - Math.pow(T / Tc, 4) : 0`、`nPaired = Math.round(frac * NP)`；「超導態：Cooper pair 同步流動，無散射」/「正常態：電子被晶格振動散射 → 有電阻」，顏色 #8ef0ff / #ffb0b2。
- 第 79 行散射機率 `dt * (2 + 3 * T)`；第 94 行 `amp = 0.02 + 0.05 * T`；第 106 行讀數「T / Tc = …　配對比例 ≈ …%」。
- js/core.js：ui.radio／ui.slider 把控制項放進 #controls（index.html 第 31 行）。
