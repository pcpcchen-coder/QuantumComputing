# Q078 來源筆記（逐字引文）

查核日：2026-11-18。維基百科頁面由製作代理以 WebFetch 讀取（工具回傳的摘錄）；學程動畫程式由製作代理讀取。學程沒有半導體自旋平台的簡報。

## Wikipedia: Spin qubit quantum computer

- 「controlling the spin of charge carriers (electrons and electron holes) in semiconductor devices」
- 「the intrinsic spin-1/2 degree of freedom of individual electrons confined in quantum dots as qubits」
- 「The first spin qubit quantum computer was proposed by Daniel Loss and David P. DiVincenzo in 1997」（參考文獻列期刊論文為 1998）
- 「A narrow gate between the two dots can modulate the coupling, allowing swap operations.」
- 「The swap operation is achieved by applying a pulsed inter-dot gate voltage」；脈衝時間減半 →「results in a square root of swap gate」
- 「local magnetic fields (or any other local spin manipulation)」
- 「locally depleting two-dimensional electron gases in semiconductors such a gallium arsenide」；germanium 亦列為材料
- 「A more recent development is using silicon spin qubits, an approach that is pursued by Intel, among others.」
- 「can be produced at industry standard silicon semiconductor wafer fabs」「allows using modern semiconductor device fabrication for making the qubits」
- 「Some of these devices have a comparably high operation temperature of a few kelvins (hot qubits)」
- 未涵蓋：讀取方式（Pauli spin blockade、電荷感測）、ESR／微磁鐵、保真度、毫克耳文溫度、量子點差異

## Wikipedia: Quantum dot

- 「semiconductor particles a few nanometres in size」
- 「quantum dots are sometimes referred to as artificial atoms」
- 「Quantum dots defined by lithographically patterned gate electrodes」，橫向尺寸約 20–100 nm
- 側向量子點「are also used as spin qubits」
- 矽 CMOS 元件：「progressive charging of electrons (holes) one by one」（庫侖阻斷）

## Wikipedia: Electron paramagnetic resonance

- 自旋排列各有「a specific energy due to the Zeeman effect」；「the splitting of the energy levels is directly proportional to the magnetic field's strength」
- 「An unpaired electron can change its electron spin by either absorbing or emitting a photon」

## animations/js/atoms/13_compare.js

- 標籤：`ctx.label('10 mK 稀釋冷凍機', …)`；desc「超導…需要 10 mK 稀釋冷凍機與大量佈線」
- `speed`：`fin: { sc: 50e-6, ion: 0.1, atom: 0.3e-3 }`，動畫 1 秒 = 20 ms
- `coh`：`txt.sc = 'T₂ ~0.1 ms / 50 ns<br>≈ <b>2×10³</b>'`
- 按鈕：`ui.radio([['conn', '連接性'], ['speed', '閘速度'], ['coh', '相干時間'], ['scale', '規模']], 'conn', setMode)`、`ui.button('↻ 重播', …)`

## animations/js/scenes/08_chip.js（index.html#chip）

- 「λ/4 讀取諧振腔：一段彎曲的共平面波導（CPW），長度約 4 mm → 共振頻率約 6–8 GHz」
- 標籤「超導接地面（Al / Nb / Ta 薄膜）on 矽基板」
