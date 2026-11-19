# Q065 來源筆記（逐字引文）

查核日：2026-11-18。維基百科頁面由製作代理以 `index.php?action=raw` 取得 wikitext（存於 `/home/user/qwork/q065wiki/`），未另查 revid。
學程內部簡報以 python-pptx 讀取（含講者備註）；動畫程式由製作代理讀取，畫面以 1600×900 截圖確認（`/home/user/qwork/q065shots/`）。

## DiVincenzo's criteria（Wikipedia）

- 「The first five conditions regard quantum computation itself. Two additional conditions regard implementing quantum communication」
- 「# A scalable physical system with well-characterized qubit」「# The ability to initialize the state of the qubits to a simple fiducial state」
  「# Long relevant quantum coherence times」「# A "universal" set of quantum gates」「# A qubit-specific measurement capability」
- 「Long decoherence times are desired, much longer than the average gate time」
- 「conditions proposed in 1996 by the theoretical physicist David P. DiVincenzo」（簡報第 4 頁講者備註寫「2000 年」；本集不念年份）

## Trapped-ion quantum computer（Wikipedia）

- 「Ions, or charged atomic particles, can be confined and suspended in free space using electromagnetic fields.」
- 「quantum information can be transferred through the collective quantized motion of the ions in a shared trap」
- 「Ionic qubit states can be prepared in a specific qubit state using a process called optical pumping.」
- 「Typically, a laser is applied to the ion that couples only one of the qubit states. … resulting in a photon being released」

## Neutral atom quantum computer（Wikipedia）

- 「Neutral atom quantum computing makes use of several technological advancements in the field of laser cooling, magneto-optical trapping and optical tweezers.」
- 「In each of these atoms, two levels of hyperfine ground subspace are isolated. The qubits are prepared in some initial state using optical pumping.」
- 「The CZ gate is carried out by leveraging the Rydberg blockade」「Measurement is enforced at the end of the computation with a camera that generates an image of the outcome by measuring the fluorescence of the atoms.」

## 學程內部簡報 slides/Ion_NeutralAtom_Talk.pptx

- 第 3 頁「人造原子 vs 真的原子」：超導 transmon「做出來的：鋁 + 約瑟夫森接面的電路 / 囚禁：不用囚禁，元件固定在晶片上 / 操控：微波脈衝（ns） /
  讀取：色散微波讀取（μs） / 環境：10 mK 稀釋冷凍機」；離子阱「天然的：¹⁷¹Yb⁺、¹³⁷Ba⁺、⁴⁰Ca⁺ 等離子 / 囚禁：RF 電場（Paul 阱），真空中懸浮 /
  操控：雷射或微波（μs） / 讀取：狀態相依螢光（~100 μs） / 環境：超高真空，室溫或 4–20 K」；中性原子「天然的：⁸⁷Rb、¹³³Cs、⁸⁷Sr、¹⁷¹Yb 原子 /
  囚禁：聚焦雷射『光鑷』陣列 / 操控：雷射 / 微波 + 芮德堡態（μs） / 讀取：螢光成像（ms） / 環境：超高真空，原子冷到 μK」；
  「天然原子：每顆完全相同、相干時間長；代價是要用電場或雷射一顆顆抓住，並用大量雷射精準操控。」
  講者備註：「好處是可以用半導體製程大量製作、速度很快；壞處是每一顆都有製程差異，而且需要 10 mK 的低溫。」「大自然保證同一種同位素的每一顆原子完全相同…原子鐘就是用這個特性。
  所以量子位元不需要逐顆調頻，相干時間也長得多。」「原子不會乖乖待在晶片上…這兩種量子電腦，與其說是電子設備，不如說是一張非常精密的光學桌。」
- 第 4 頁「量子位元的五個條件」：①「離子的兩個超精細能階（例：¹⁷¹Yb⁺ 12.6 GHz）」「原子的兩個超精細能階（例：⁸⁷Rb 6.8 GHz）」；
  ②「雷射冷卻 + 光泵浦（> 99.9 %，μs）」「雷射冷卻 + 光泵浦；先成像、重排出完整陣列」；③「T₂ 秒～小時（時鐘躍遷 + 動態解耦）」「T₂ ~1 s（回波）；Caltech 2025：12.6 s」；
  ④「單位元：微波 / Raman；雙位元：共享振動模態（MS 閘）」「單位元：全域 + 局部定址；雙位元：芮德堡阻斷（CZ）」；
  ⑤「狀態相依螢光 → PMT / 相機（> 99.9 %）」「推出一個態 + 螢光成像 → 相機（> 99 %）」；「數值為代表值；實際依原子種類與系統而異。」
- 第 31 頁「芮德堡原子：把原子『吹大』」：「基態原子之間幾乎沒有交互作用」「激發到芮德堡態 → 偶極交互作用增加 10¹² 倍以上」；備註「電子軌道半徑…比基態大一千多倍」。
- 第 39 頁「綜合比較表」：超導「~25 ns / ~60 ns」「~0.1–1 ms」「最近鄰（固定）」「色散微波 ~0.5 μs」「~100–1000+」；離子阱「~5 μs / 10–200 μs」「秒～小時」
  「同鏈全連接；QCCD 搬運」「螢光 ~200 μs」「~100（Helios 98）」；中性原子「~1 μs / ~0.3 μs」「~1–10 s」「搬運重排 → 任意配對」「成像 ~ms」「數百～6000+ 顆原子」；
  「代表值，依系統與年份差異很大」。
- 第 40 頁「時間尺度：快不一定贏」：「T₂ / 閘時間：一個量子位元在失去相干前能做幾個閘 / 超導 ~10³、離子 ~10⁴、原子 ~10⁶（只看閘） / 但真正的循環時間還包含讀取、搬運、冷卻」；
  「超導贏在速度；離子贏在品質；中性原子贏在數量與並行。」備註：「這也是為什麼目前三條路線都有大量投資。」
- 第 42 頁：「2025 中性原子 6100 顆原子陣列，相干時間 12.6 s，成像 > 99.99 %（Manetsch et al., Nature 2025（Caltech））」。

## slides/JJ_Microwave_Readout_Talk.pptx

- 第 3 頁：「10 mK 工作溫度」「20–50 ns 單量子位元閘時間」「相干時間仍有限（T1、T2 約 0.1–1 ms 量級）」「需稀釋冷凍機與大量微波佈線，擴展受限」
  「製程變異造成頻率散佈，需頻率定位技術」；備註「單量子位元閘只要二三十奈秒」「它是『人造原子』，頻率、耦合強度都可以設計」。
- 第 10 頁：「LC 振盪器能階等間距：頻率 ω 的微波同時激發 0→1→2→3…，無法只用兩個能階」「把電感換成 JJ：位勢由拋物線變成餘弦，能階間距逐漸變小」
  「於是可以只選擇 |0⟩、|1⟩ 作為量子位元」；「EJ/h = 12.5 GHz、EC/h = 250 MHz（EJ/EC = 50）」。

## slides/QC_Operation_Talk.pptx

- 第 13 頁「初始化：每個 shot 都要回到 |0⟩」：「被動重置（等待熱化）/ 10 mK 下熱平衡幾乎全在 |0⟩ / 等待 ~5 T₁ 讓 |1⟩ 自然衰減」「主動重置（量測 + 回饋）」。

## 課綱

- Q065 lesson.json（全文見 academy/lessons/Q065/）；Q017 brief「知道量子位元需要可控制的二態系統，認識 DiVincenzo 五條件」「『有兩個狀態』還不夠，還要能初始化、操控、讀取並維持夠久」；
  Q064「模組專題：在模擬器跑我的線路」；Q066「Paul 阱：旋轉鞍形電場」。

## 互動動畫程式（動畫段，詳見 v2/demos_extra/q065.py 檔頭）

- animations/js/scenes/04_potential.js：E_C = 0.25 GHz、預設 E_J/E_C = 50；說明「非諧性 α/2π = … MHz」「（等間距 → 無法單獨定址）」。
- animations/js/atoms/07_atomsys.js：laser 說明「同一顆原子要被 5–7 種波長的雷射照射，全部要鎖頻、對準、功率穩定。」；fac 說明「沒有稀釋冷凍機與氦壓縮機…」；
  插圖 footer「合計約 10 kW 等級；不需稀釋冷凍機（依系統而異）」。
- animations/js/atoms/13_compare.js：DATA.speed／coh／scale 的標籤文字（50 μs、0.1 s、0.3 ms；2×10³、10⁴ 以上、3×10⁶、10³–10⁴；Willow 105、Condor 1121、Helios 98、Caltech 6100）。
