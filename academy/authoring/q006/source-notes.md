# Q006 來源筆記（逐字引文）

查核日：2026-11-18。維基百科四頁由製作代理用 MediaWiki API（`prop=revisions|extracts&explaintext=1`）取得純文字版並閱讀；學程內部簡報與 3D 場景程式由製作代理讀取；P(0)=cos²(φ/2) 由製作代理重算。

## Wave interference（Wikipedia，oldid=1383568553）

- 「If a crest of a wave meets a crest of another wave of the same frequency at the same point, then the amplitude is the sum of the individual amplitudes—this is constructive interference.」
- 「If a crest of one wave meets a trough of another wave, then the amplitude is equal to the difference in the individual amplitudes—this is known as destructive interference.」
- 「For example, when two pebbles are dropped in a pond, a pattern is observable」
- 「If the light from two point sources overlaps, the interference pattern maps out the way in which the phase difference between the two waves varies in space. This depends on the wavelength and on the separation of the point sources.」
- 「This extra term, which is called the quantum interference term, … can add (constructive interference) or subtract (destructive interference)」

## Double-slit experiment（Wikipedia，oldid=1385822520）

- 「This type of experiment was first described by Thomas Young in 1801 when making his case for the wave behavior of visible light.」
- 「The wave nature of light causes the light waves passing through the two slits to interfere, producing bright and dark bands on the screen」
- 「such experiments demonstrate that particles do not form the double-slit interference pattern if one detects which slit they pass through; the pattern instead becomes the sum of two single-slit interference patterns.」
- 「In 2012, Stefano Frabboni and co-workers sent single electrons onto nanofabricated slits (about 100 nm wide) and, by detecting the transmitted electrons with a single-electron detector, they could show the build-up of a double-slit interference pattern.」
- 限制：「There is some question as to whether he ever actually performed a double-slit interference experiment.」（因此旁白只說「兩百多年前就用光的干涉說明光有波的性質」）

## Mach–Zehnder interferometer（Wikipedia，oldid=1381469021）

- 「The Mach–Zehnder interferometer can be seen as a simplified version of the double-slit experiment.」
- 「Blocking one of the paths, or equivalently detecting the presence of a photon on a path eliminates interference between the paths: both photodetectors will be hit with probability 1/2.」

## Laser safety（Wikipedia，oldid=1373452331）

- 「Since even relatively small amounts of laser light can lead to permanent eye injuries, the sale and usage of lasers is typically subject to government regulations.」
- 「A Class 2 laser is considered to be safe because the blink reflex … will limit the exposure to no more than 0.25 seconds.」「Intentional suppression of the blink reflex could lead to eye injury. Some laser pointers and measuring instruments are class 2.」

## 學程內部簡報：slides/QC_Operation_Talk.pptx

- 第 37 頁：「干涉：讓錯誤答案互相抵消」「振幅有正負與相位，可以相加或相消」「演算法 = 安排相位，讓正確答案相長」。
- 第 38 頁：「a(結果) = Σ路徑 (各路徑振幅的乘積)」「P(結果) = |a(結果)|²」「φ = 0：|1⟩ 的兩支箭頭方向相反 → 抵消，100% 得到 0」「φ = 180°：反過來，100% 得到 1」「偷看走哪條路（測量）→ 干涉消失 → 50 / 50」「相位本來看不見，干涉把它變成可量測的機率」。

## 學程內部簡報：slides/output/basic-circuits.pptx

- 第 7 頁：「只差一個看不到的負號，結果就完全相反」。
- 第 8 頁：「② 和 ① 的機率完全相同，差別只在正負號；③ 的 H 把正負號『翻譯』成 0 或 1」。
- 第 9 頁：「振幅有正有負，所以相加時可以互相抵消，這是古典機率做不到的」。

## 3D 場景程式

- `animations/js/operation/08_interference.js`：控制項「單一量子位元：兩條路徑」「3 位元：8 條路徑（Deutsch–Jozsa）」「A：相位 φ」「A：自動掃描 φ」「A：中途偵測路徑（破壞干涉）」；插圖 P(0)=cos²(φ/2)、偵測時 0.5；圖例「藍 = 經由 |0⟩ 的貢獻　橙 = 經由 |1⟩ 的貢獻　白 = 總和」。
- `animations/basic-circuits.html` 範例 2「干涉：H‑Z‑H = X」：選項「有 Z／沒有 Z」；逐步按鈕「⏮ 起點」「下一步 ▶」；藍 = 正振幅、銅 = 負振幅。

## 重算

P(0) = cos²(φ/2)：0° → 1.000；45° → 0.854；90° → 0.500；135° → 0.146；180° → 0.000。
