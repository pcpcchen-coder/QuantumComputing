# Q019 來源筆記（逐字引文）

查核日：2026-11-18。課綱、簡報、動畫程式由製作代理讀取。程式由製作代理實際執行。

## 課綱（academy/lessons/Q019/lesson.json）

- 課程主題「Cooper pair 與能隙」；階段「第二階段 硬體怎麼做」；模組「QM02 超導量子位元：從超導到 transmon」。
- 學習目標「用晶格扭曲的直覺說明電子為什麼成對，以及能隙保護了什麼」。
- 動手任務「全家當晶格原子，一人走過時大家靠近，讓第二個人被「吸」過來」；孩子獨立改造「畫出有能隙與沒能隙時，小擾動造成的差別」；好玩機制「角色扮演（人肉晶格）」。
- 作品「能隙示意圖」；家長課前準備「客廳空間；index.html#cooper」；生活技能支線「用身體演出看不見的機制」。
- 常見誤解與安全提醒「這是簡化圖像；BCS 理論的細節在大學物理才會完整推導」。
- 沿用簡報頁：JJ_Microwave_Readout_Talk.pptx p8；沿用 3D 場景：i:cooper。
- Q018 brief：「超導：電阻消失、磁鐵懸浮」「知道超導的兩個特徵：零電阻與排斥磁場」。Q020 brief：「磁通量子化 Φ₀ = h/2e」「知道超導環裡的磁通只能是 Φ₀ 的整數倍，以及 2e 從哪裡來」。

## 簡報（slides/JJ_Microwave_Readout_Talk.pptx，python-pptx 擷取）

- p7：「臨界溫度 Tc」「Al ≈ 1.2 K、Ta ≈ 4.5 K、Nb ≈ 9.2 K、NbTiN ≈ 14 K。量子電路在 10 mK 工作 ≪ Tc。」；備註「在 2.5 K 的正常態，電子被晶格振動散射、亂跑，這就是電阻的來源；降到 0.3 K，電子兩兩配對成 Cooper pair，整體同步往同一個方向流動，不再被散射。」
- p8：「電子經過時吸引正離子 → 晶格局部扭曲（聲子）→ 吸引第二顆電子」「兩顆自旋相反、動量相反的電子形成 Cooper pair（電荷 2e，玻色子）」「所有 Cooper pair 凝聚為同一個巨觀量子態」「拆散一對需要能量 2Δ（超導能隙）→ 小擾動無法散射 → 零電阻」「整塊超導體只需一個「相位 φ」描述」；
  能量尺度（鋁）「超導能隙 2Δ/h ≈ 88 GHz（2Δ ≈ 360 μeV）」「量子位元 f01 ≈ 5 GHz（≈ 20 μeV）」「熱能 kBT/h @10 mK ≈ 0.2 GHz」「量子位元光子能量 ≪ 2Δ → 無法拆散 Cooper pair，電路幾乎無耗散」「熱能 ≪ 量子位元能量 → 熱激發機率極低」；
  備註「一顆電子經過晶格，會把周圍帶正電的離子稍微吸過來，留下一條短暫的正電荷尾跡——這就是聲子；這條尾跡又吸引了第二顆電子。」

## 維基百科（原始 wikitext，2026-11-18 取得）

- Cooper pair：「The electron is repelled from other electrons due to their negative charge, but it also attracts the positive ions that make up the rigid lattice of the metal. This attraction distorts the ion lattice, moving the ions slightly toward the electron, increasing the positive charge density of the lattice in the vicinity. This positive charge can attract other electrons. At long distances, this attraction between electrons due to the displaced ions can overcome the electrons' repulsion due to their negative charge, and cause them to pair up.」
- Cooper pair：「paired electrons may still be many hundreds of nanometers apart. This distance is usually greater than the average interelectron distance so that many Cooper pairs can occupy the same space.」「The tendency for all the Cooper pairs in a body to "condense" into the same ground quantum state is responsible for the peculiar properties of superconductivity.」
- BCS theory：「Δ(T=0) = 1.764 k_B T_c, independent of material」（gap_scale.py 用來重算 2Δ）。

## 互動動畫程式（animations/js/scenes/02_cooper.js）

- 第 3–8 行：id 'cooper'、標題「超導體：Cooper pair 與零電阻」；desc「低於臨界溫度 Tc（鋁約 1.2 K）時，所有 Cooper pair 凝聚為同一個巨觀量子態……不再被晶格散射 → 直流電阻為零」「拆散一對需要 2Δ 的能量（鋁 2Δ/h ≈ 90 GHz），遠高於量子位元 ~5 GHz 的能量尺度」。
- 第 43–46 行：`T = 0.3`、`Tc = 1.2`；滑桿「溫度 T (K)」0.05–3；按鈕「超導態 0.3 K」「正常態 2.5 K」；讀數。
- 第 48–53 行：右下小圖「電阻 R 對溫度 T（鋁，Tc ≈ 1.2 K）」，`R = t < Tc ? 0 : 1 + 0.08 (t − Tc)`。
- 第 59–60 行：`frac = sc ? 1 − (T/Tc)^4 : 0`（註解「超流體比例（示意）」）、`nPaired = round(frac × NP)`，NP = 10。
- 第 61–62 行：「超導態：Cooper pair 同步流動，無散射」（#8ef0ff）／「正常態：電子被晶格振動散射 → 有電阻」（#ffb0b2）。
- 第 106 行：讀數「能隙 Δ 打開：小擾動無法散射 Cooper pair」／「無能隙：電子與聲子碰撞 → 焦耳熱」。

## 實跑紀錄（gap_scale.py，Python 3，無套件）

見 `classroom.py` 執行時寫入的 `04_解答.md`；製作代理以同樣常數另行計算：2Δ/h = 88.2 GHz（365 μeV）、量子位元 5 GHz = 20.7 μeV、10 mK 熱能 0.208 GHz；
能隙 ÷ 量子位元 ≈ 17.6、量子位元 ÷ 熱能 ≈ 24、1.2 K ÷ 10 mK = 120；動畫示意公式的配對比例：1.1 K 29 %、1.0 K 52 %、0.8 K 80 %、0.6 K 94 %、0.45 K 98 %、0.3 K 100 %。
