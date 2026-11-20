# Q067 來源筆記（逐字引文）

擷取日：2026-11-19。維基百科以 `index.php?title=…&action=raw` 取得當日版本（未記 oldid）。
學程簡報 `slides/Ion_NeutralAtom_Talk.pptx` 以 python-pptx 讀取第 6、9、10、11 頁（含講者備註）；
`docs/離子阱與中性原子系統指南.md`、`animations/js/atoms/01_ionsys.js`、`03_ionqubit.js`、`animations/js/peripherals/01_overview.js`、`common.js` 由製作代理直接閱讀。

## Trapped-ion quantum computer（Wikipedia）

- 偵測：「Typically, a laser is applied to the ion that couples only one of the qubit states. When the ion collapses into this state during the measurement process, the laser will excite it, resulting in a photon being released when the ion decays from the excited state. After decay, the ion is continually excited by the laser and repeatedly emits photons. These photons can be collected by a photomultiplier tube (PMT) or a charge-coupled device (CCD) camera. If the ion collapses into the other qubit state, then it does not interact with the laser and no photon is emitted. By counting the number of collected photons, the state of the ion may be determined with a very high accuracy (>99.99%).」
- 冷卻：「This can be achieved by a combination of Doppler cooling and resolved sideband cooling.」
- 單位元閘：「In a trapped-ion system, this is often done using magnetic dipole transitions or stimulated Raman transitions for hyperfine qubits」
- 保羅阱：「an electric field oscillating at radio frequency (RF) is applied, forming a potential with the shape of a saddle spinning at the RF frequency.」

## 離子阱與中性原子量子電腦（學程簡報）

- 第 6 頁：六個子系統「真空與阱：超高真空腔、阱晶片、離子泵」「雷射與光學：369 / 935 / 399 / 355 nm、AOM、光纖」「成像與偵測：高 NA 物鏡、PMT / 相機」
  「電子與訊號：RF、多通道 DC、微波、DDS」「控制與軟體：FPGA（ARTIQ 類）、時脈、編譯」「設施：恆溫空調、冷卻水、防振、UPS」。
  備註：「和超導量子電腦最明顯的差別是：中間不是一台稀釋冷凍機，而是一張光學桌和一個超高真空腔。」「面板上可以切換『只看雷射』『只看電子訊號』『只看設施』」
- 第 9 頁：「原子爐 / 雷射燒蝕 產生中性原子束」→「光游離 399 nm + 369 nm」→「Paul 阱捕捉 離子懸浮」→「雷射冷卻 形成離子晶體」→「確認顆數 相機成像」；
  「壓力 < 10⁻¹¹ mbar：與背景氣體碰撞約每小時以下一次」「離子泵 + 非蒸散型吸氣劑（NEG）持續抽氣」「一顆離子可以留在阱裡數小時到數週」。
  備註：「用兩道雷射把它游離：第一道 399 nm 只會共振激發鐿-171 這個同位素，第二道把電子打掉。」
- 第 10 頁：「369.5 nm（紫外）冷卻、初始化、偵測」「935 nm（紅外）回泵（repump）離子偶爾掉到 ²D₃/₂，把它拉回循環」「399 nm 光游離（裝載）」
  「355 nm 脈衝雷射 量子閘（Raman）拍頻 = 12.6 GHz」「一台離子阱量子電腦常有 5–10 種波長、數十道光束」。
- 第 11 頁：「RF 源 + 螺旋共振器升壓到數百伏」「多通道 DAC（數十～數百通道）」「12.6 GHz 微波號角（單位元閘）」「PMT / EMCCD / SPAD 陣列」
  「FPGA 即時計數、判別」「和超導系統相比：不需要上百條低溫微波線，但需要大量雷射調變通道與阱電極 DAC 通道。」

## 離子阱與中性原子系統指南（docs/）

- 第 1 節表：「RF 電場（Paul 阱），離子懸浮於電極上方 50–100 μm」「環境：超高真空 < 10⁻¹¹ mbar；室溫或 4–20 K 低溫恆溫器」「¹⁷¹Yb⁺ 超精細 … 12.6428 GHz」。
- 第 2.1 節：「設施：恆溫空調（光學桌 ±0.1 °C 等級）、雷射冷卻水、防振光學桌、潔淨度、UPS、網路」；「控制：FPGA 時序系統…10 MHz 參考時脈」。
- 第 4 節表：「主要環境設備：稀釋冷凍機 + 壓縮機｜超高真空腔（± 小型低溫恆溫器）」「單套用電：~25 kW（實測型）｜Helios 官方 < 40 kW」
  「最大負載：壓縮機 ~10.7 kW、冷卻水 ~10 kW｜雷射與其冷卻、控制電子、精密空調」
  「停電影響：重新降溫 2–5 天（最壞約 10 天）…｜雷射重新鎖頻、重新裝載離子（數十分鐘～數小時）」；
  「UPS 涵蓋雷射控制器、鎖頻電子、真空控制器與控制電腦：避免短暫停電造成雷射失鎖、離子 / 原子遺失。」「溫度漂移會直接造成光路漂移與頻率漂移。」

## 互動動畫原始碼

- 01_ionsys.js desc：「中央是超高真空腔（< 10⁻¹¹ mbar），裡面有一片表面電極阱晶片，一串離子懸浮在晶片上方約 50–100 μm」；
  「RF：RF 源 → 螺旋共振器升壓（約 100–300 V、數十 MHz）→ 阱的 RF 電極」「DC：多通道 DAC（數十到數百通道）→ 分段電極，決定離子位置、搬運離子」
  「微波：12.6 GHz 號角，直接驅動量子位元（單位元閘）」「FPGA 時序控制（ARTIQ 類）以奈秒精度指揮所有 AOM、DAC、RF；PMT / 相機計數回傳；銣鐘 10 MHz 同步」。
- 01_ionsys.js INFO：all「典型一輪：冷卻 → 初始化 → 閘（雷射或微波）→ 偵測螢光。」；laser「經 AOM 在 μs 內開關、調頻調相，再經光纖送入真空腔。369 nm 同時負責冷卻、初始化與偵測；
  355 nm 脈衝雷射的兩道光頻差 = 12.6 GHz，做 Raman 閘。」；fac「沒有稀釋冷凍機；主要負載是雷射、電子與它們的散熱。光學桌與雷射要恆溫（±0.1 °C 等級）」。
- 01_ionsys.js 插圖：「典型用電（示意；Quantinuum Helios 官方 < 40 kW）」，空調 / 冷卻水 10、雷射與光學 6、控制電子 5、低溫恆溫器（選配）7、真空泵 0.2；「無稀釋冷凍機；雷射與散熱是主要負載」。
- 03_ionqubit.js：「369 nm 只和 |1⟩（F=1 → F′=0）共振…→ 亮；|0⟩ 偏離 14.7 GHz → 暗。數 PMT 的光子數，超過閾值判為 1。」
- peripherals/01_overview.js：「稀釋冷凍機（量子晶片在 10 mK）」；peripherals/common.js power：脈衝管壓縮機 10.7、冷卻水系統 10.0、控制電子機櫃 3.0、氣體處理系統（泵）1.5、電腦 / 監控 / 網路 1.0。
