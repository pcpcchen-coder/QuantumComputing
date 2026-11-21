# Q041 來源筆記（逐字引文）

查核日：2026-11-18。維基百科頁面由製作代理以 `action=raw` 讀取原始碼（revision id 未取得：維基 API 當時限流）。學程內部簡報與動畫程式由製作代理讀取。

## Boltzmann constant（Wikipedia）

- 「The Boltzmann constant is defined to be exactly 1.380649×10⁻²³ joules per kelvin」

## Planck constant（Wikipedia）

- 「… fixing the numerical value of h to be 6.62607015×10⁻³⁴ when expressed in the unit J⋅s …」

## Boltzmann distribution（Wikipedia）

- 「The ratio of probabilities of two states is known as the Boltzmann factor and only depends on the states' energy difference」

## Liquid nitrogen（Wikipedia）

- 「It can be stored and transported in vacuum flasks, the temperature being held constant at 77 K by slow boiling of the liquid.」

## Liquid helium（Wikipedia）

- 表格：helium-4 常壓沸點 4.2 K；圖說「Liquid helium (in a vacuum bottle) at 4.2 K and 1 bar boiling slowly.」

## Aluminium（Wikipedia）

- 「Aluminium is capable of superconductivity, with a superconducting critical temperature of 1.2 kelvin」

## 學程內部簡報 slides/QC_Peripheral_Systems_Talk.pptx

- 第 6 頁「為什麼要 10 mK？」：「5 GHz」「量子位元能量 hf ≈ 20 μeV ≈ 240 mK × kB」「10 mK」「kBT 只有 hf 的 1/24 → 熱激發 ≈ e−24」「2Δ ≈ 360 μeV」「鋁超導能隙；溫度越低，準粒子越少」。
- 第 6 頁「溫度不夠低會發生什麼？」：「量子位元有殘留熱激發 → 初始化錯誤」「讀取腔中有熱光子 → 量子位元失相（T2 下降）」「準粒子增加 → 穿隧過 JJ 帶走能量（T1 下降）」「超導體（Al，Tc ≈ 1.2 K）根本無法超導」。
- 第 6 頁：「溫度是『階梯』降下來的　300 K → 50 K → 4 K：脈衝管（機械式冷凍）　4 K → 0.9 K → 100 mK → 10 mK：稀釋循環」。
- 第 6 頁講者備註：「在 10 mK 下，熱能只有它的 24 分之一，熱激發機率是 e 的負 24 次方，幾乎為零。如果溫度只有 100 mK，熱激發就會到百分之一的量級」（後半句與驗算不符，本集不採用，見 fact-check.md）。
- 第 7 頁「稀釋冷凍機：各級溫度與冷卻功率」：MXC「~6–10 mK」；「基溫約 10 mK；空機降溫約 1–2 天」（量測值：Krinner et al., EPJ Quantum Technol. 6, 2 (2019)）。

## 互動動畫程式

- animations/transmon-3d.html 第 5 章 `readout`，G5STEPS[0].body：「量子位元的一個激發只有 h × 5.21 GHz ≈ 22 μeV（約相當於 0.25 K 的熱能）」；G5STEPS[6] cue：「稀釋冷凍機全程維持約 10 mK，重新降溫要好幾天」；看板：「位元等效溫度常為 40–60 mK：靜置時仍有約 0.1–1% 在 |1⟩」。步驟按鈕由 bindChapter(4) 建在 `#g5steps`。
- animations/js/peripherals/04_cooldown.js（`#cooldown`）：PD.stages 300 K 頂板、50 K 級、4 K 級、Still、Cold plate、MXC；TMODEL 各級溫度；按鈕「⏸ 暫停」「⟲ 重新開始」、滑桿「時間 (小時)」0–36、「播放速度（小時/秒）」。
- animations/js/scenes/11_fridge.js（`#fridge`）：六層板、三個「衰減器 −20 dB」；readout「熱光子數 n_th = 1/(e^{hf/kT} − 1)：7 GHz 時 300 K ≈ 890，10 mK ≈ 10⁻¹⁵」；滑桿「動畫速度」、按鈕「視角：整體」「放大混合腔」。
