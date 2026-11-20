# Q023 來源筆記（逐字引文）

查核日：2026-11-18。課綱、簡報、筆記、動畫程式由製作代理讀取。程式由製作代理實際執行。

## 課綱（academy/lessons/Q023/lesson.json）

- 課程主題「約瑟夫森接面：超導三明治」；階段「第二階段 硬體怎麼做」；模組「QM02 超導量子位元：從超導到 transmon」。
- 學習目標「認識 SIS 結構、Cooper pair 穿隧與 DC／AC Josephson 效應」。
- 動手任務「用兩片吐司夾一層薄紙做 JJ 模型，標出超導、絕緣、相位差」；孩子獨立改造「寫一段 30 秒說明，解釋「穿隧」不是挖洞穿過去」；好玩機制「Maker 挑戰（紙模型）」。
- 作品「JJ 紙模型＋標註」；家長課前準備「紙材或食物模型；index.html#jj；notes/josephson-junction-wave-and-tunneling.md」；生活技能支線「用模型說明結構」。
- 常見誤解與安全提醒「絕緣層只有約 1–2 奈米；穿隧是波的性質，不是粒子打洞」。
- 沿用簡報頁：JJ_Microwave_Readout_Talk.pptx p12–13、ep049-superconducting-qubit.pptx p5；沿用 3D 場景：i:jj。
- Q022 brief：「量子諧振子：等距的梯子」「知道 LC 電路的能階等距，所以無法只挑出兩個能階當量子位元」。Q024 brief：「JJ 是非線性電感」「知道 JJ 的電感會隨電流改變，這個非線性是做出量子位元的關鍵」。

## 簡報（python-pptx 擷取）

- JJ_Microwave_Readout_Talk p12「JJ 的結構：超導–絕緣–超導」；表「材料 Al / AlOx / Al」「氧化層厚度 1–2 nm」「接面面積 ~0.01–0.05 μm²」「正常態電阻 Rn 5–15 kΩ」「臨界電流 Ic 20–60 nA」「電容 CJ ~1–2 fF」；
  「絕緣層夠薄 → Cooper pair 可整對量子穿隧」「兩側超導體各有相位 φ1、φ2；一切由相位差 φ 決定」；
  備註「量子電路裡最常見的是鋁 / 氧化鋁 / 鋁，絕緣層只有一到兩奈米，也就是幾個原子層。」「臨界電流幾十奈安培」「藍紫色的小球對是 Cooper pair，它們穿過阻障時會閃一下。」
- JJ_Microwave_Readout_Talk p13「Josephson 的兩大關係式」：「DC Josephson 效應」「I = Ic sin φ」「零電壓下就能有超電流」「電流大小由相位差 φ 決定」「最大值 Ic：超過就進入電壓態」；
  「AC Josephson 效應」「dφ/dt = 2eV / ħ」「加電壓 V → 相位持續旋轉」「電流以 f = V/Φ0 振盪」「483.6 GHz / mV：電壓標準的基礎」；
  備註「1962 年 Josephson 預測了兩個效應，後來得了諾貝爾獎。」「把偏壓電流拉到 0.5 Ic，相位差停在 30 度，電壓為零；拉到接近 Ic，相位差趨近 90 度；超過 Ic，例如 1.4 Ic，大家看相位鐘開始一直轉，這就是電壓態，右下角的 I-V 圖上工作點跳到了電阻分支。」
- ep049 p5「回顧：JJ 是什麼」：「超導體 S」「絕緣體 I」「庫柏電子對（2e）成對穿隧 → 超導電流」「結構：超導體｜絕緣體｜超導體」「和一般穿隧不同：不是單顆電子，而是兩個兩個成對過去，形成超導電流」。

## 筆記（notes/josephson-junction-wave-and-tunneling.md）

- 「電子兩兩配成庫柏對（Cooper pair），全部凝聚成同一個巨觀波函數」「整塊超導體共用同一個相位 φ，就像千萬人踩著同一個節拍前進。」
- 「JJ 的結構是：超導體 A ｜ 超薄絕緣層（約 1–2 nm）｜ 超導體 B」「絕緣層把一個大波切成兩個波，各自有相位 φ₁、φ₂。」
- 「V = 0｜固定不變｜直流超電流 I = I_c sin φ」「V ≠ 0｜隨時間持續轉動｜交流電流，頻率約 483.6 GHz/mV」「電壓不是推動電流的力，電壓決定的是相位轉動的速度。」
- 「左邊的波函數進入絕緣層後不會立刻消失，而是指數衰減（evanescent wave）。」「絕緣層夠薄時，衰減到右邊還剩一點振幅，與右邊的波函數重疊。」「『粒子鑽過牆』只是古典的畫面；真正的內容是『波函數重疊，產生轉移振幅』。」
- 「電流隨厚度呈指數衰減：I_c ∝ e^(−2κd)。」「把電感換成 JJ（例如 transmon 的結構），能階變得不等距（anharmonic）」。

## 維基百科（原始 wikitext，2026-11-18 取得）

- Josephson effect：「The Josephson effect produces a current, known as a supercurrent, that flows continuously without any voltage applied, across a device known as a Josephson junction (JJ).」
  「The weak link can be a thin insulating barrier (known as a superconductor–insulator–superconductor junction, or S-I-S)」「The effect is named after the British physicist Brian Josephson, who predicted in 1962 the mathematical relationships for the current and voltage across the weak link.」
- Brian Josephson：「It was during this period, in 1962, that he carried out the research that led to his discovery of the Josephson effect」「received a Doctor of Philosophy in 1964」「He won the 1973 Nobel Prize in Physics "for his theoretical predictions of the properties of a supercurrent through a tunnel barrier……"」。
- Quantum tunnelling：「The solutions of this equation are rising and falling exponentials in the form of evanescent waves.」「the probability of transmission of a wave packet through a barrier decreases exponentially with the barrier height, the barrier width, and the tunnelling particle's mass」。
- Josephson voltage standard：「It is the most accurate method to generate or measure voltage and has been, since an international agreement in 1990, the basis for voltage standards around the world.」「the constant K_J-90 was assigned the value 483597.9 GHz/V and adopted by all standards laboratories」（K_J = 2e/h）。

## 動畫程式（animations/js/scenes/03_jj.js、index.html#jj）

- 第 1–10 行場景說明：「兩片超導鋁中間夾一層僅 1–2 nm 的氧化鋁（AlOx）」「兩側各有自己的巨觀相位 φ1、φ2（圖中旋轉的『相位鐘』）」「DC Josephson：I = Ic sin φ　不加電壓也能有超電流」「AC Josephson：dφ/dt = 2eV/ħ……電流以 483.6 GHz/mV 振盪」「I < Ic 時相位差固定、無電壓；I > Ic 時進入電壓態」。
- 第 26–28 行標籤「超導體 Al（電極 1）· 相位 φ₁」「超導體 Al（電極 2）· 相位 φ₂」「AlOx 穿隧阻障 ~1–2 nm」；第 68–69 行滑桿「偏壓電流 I / Ic」、按鈕「I = 0.5 Ic（超電流）」「I ≈ Ic」「I = 1.4 Ic（電壓態）」。
- 第 105 行金字「φ = φ₂ − φ₁ = …°　I = Ic sin φ = … Ic」；第 124–125 行讀數「電壓態：相位差持續旋轉 → 電流以 2eV/h 振盪」「同時出現準粒子（電阻性）電流 → 有耗散」「超電流態：φ = arcsin(I/Ic) = …°」「電壓為零，能量不耗散」。
- 第 73 行右下小圖標題「電流–相位關係 I = Ic sin φ 與 I–V 特性」。

## 實跑紀錄（tunnel_check.py，Python 3，無套件）

見 `classroom.py` 執行時寫入的 `04_解答.md`；重點：Ic = 40 nA（簡報 20–60 nA 之間的例子）時，相位差 30° → 20 nA、78.5° → 39.2 nA、90° → 40 nA；
2e/h = 483.6 GHz/mV（1 μV → 0.4836 GHz、10 μV → 4.836 GHz）；穿隧的指數例子：原本剩 1 %，厚一倍剩 0.01 %，不是 0.5 %。
