# Q077 來源筆記（逐字引文）

查核日：2026-11-18。學程內無光子平台簡報或場景；以下維基百科引文由製作代理讀取。動畫程式由製作代理讀取。

## Linear optical quantum computing（Wikipedia）
- 「LOQC usually only uses mirrors, beam splitters, phase shifters」
- 「a qubit state can be represented using a single photon in two modes, vertical (V) and horizontal (H)」
- 「An intrinsic problem in using photons as information carriers is that photons hardly interact with each other」
- KLM：「uses linear optical elements, single photon sources and photon detectors as resources」；可容錯「for photon loss, detector inefficiency and phase decoherence」

## Beam splitter（Wikipedia）
- 「splits a beam of light into a transmitted and a reflected beam」；半鍍銀鏡約一半穿透、一半反射
- 單光子：「creates a superposition on the outputs」

## Mach–Zehnder interferometer（Wikipedia）
- 「when there is no sample, only detector 1 receives light」
- 擋住一條路或拿掉第一片分光鏡：「there will no longer be interference between the paths」

## Hong–Ou–Mandel effect（Wikipedia）
- 「they will always exit the beam splitter in the same (but random) output mode」
- 1987 年，Chung Ki Hong、Zheyu Jeff Ou、Leonard Mandel（羅徹斯特大學）
- 「The coincidence rate of the detectors will drop to zero when the identical input photons overlap perfectly in time」

## Boson sampling（Wikipedia）
- 「a computational task particularly friendly to quantum computers as opposed to classical computers」
- 「a non-universal approach to linear optical quantum computing」；Aaronson 與 Arkhipov

## Jiuzhang (quantum computer)（Wikipedia）
- 2020 年 12 月 3 日於 Science 發表；中國科學技術大學；高斯玻色取樣；「with a maximum of 76 detected photons」

## One-way quantum computer（Wikipedia）
- 「first prepares an entangled resource state, usually a cluster state or graph state」「then performs single qubit measurements on it」
- 「The implementation of MBQC is mainly considered for photonic devices」

## animations/js/operation/08_interference.js
- desc：「H 把 |0⟩ 分成兩條路徑，中間在 |1⟩ 路徑加相位 φ，第二個 H 再合併。φ = 0 時…結果 100% 是 0；φ = 180° 時反過來。」「若中途『偷看』走哪一條路（測量），干涉消失，變成 50/50。」
- 控制：`ui.radio([['A', '單一量子位元：兩條路徑'], …])`、`ui.slider('A：相位 φ', 0, 360, 1, …)`、`ui.toggle('A：自動掃描 φ', …)`、`ui.toggle('A：中途偵測路徑（破壞干涉）', …)`
- 小圖：`P.curve(g, (x) => Math.cos((x * Math.PI) / 360) ** 2, …)`，即 P(0) = cos²(φ/2)
