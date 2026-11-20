# Q088 來源筆記（逐字引文）

查核日：2026-11-18。學程內部簡報與動畫程式由製作代理讀取；維基百科由製作代理讀取；H₂ 能量由製作代理計算。

## 如何操作量子電腦（slides/QC_Operation_Talk.pptx）

第 44 頁「量子電腦能算什麼：應用地圖」
- 表列：「化學、材料、藥物｜量子相位估計、VQE、Trotter 模擬｜指數級（多數）｜小分子已示範；工業級分子需數百萬實體位元等級」
- 「物理模擬（自旋、凝態）｜哈密頓模擬｜指數級｜最可能最早實用；已有超越古典的實驗」
- 頁尾：「其餘為文獻常見結論，依技術進展會變動」
- 講者備註：「小分子已經示範過，但工業上有意義的分子，例如固氮酶的活性中心，估計需要數百萬實體量子位元等級。」

第 4 頁：「模擬量子系統：分子、材料、催化劑、高溫超導」；備註「大自然本來就是量子的，用量子電腦模擬最自然」
第 31 頁：「很多問題的答案是期望值 ⟨ψ|O|ψ⟩，例如分子能量 = Σ 係數 × ⟨Pauli 字串⟩」
第 51 頁：「NISQ 數十～上千實體位元」「早期容錯…中等規模化學、物理模擬」「大規模容錯 百萬實體位元等級 Shor、大型分子、材料設計」「需解決佈線、低溫電子、即時解碼」

## animations/js/operation/04_register.js

- `ui.slider('量子位元數 n', 1, 4, 1, n, …)`；`ui.button('均勻疊加 H⊗ⁿ', …)`
- `ctx.inset('精確模擬 n 個量子位元所需記憶體（2ⁿ × 16 bytes）', …)`；標籤「16 GB（筆電）」「16 TB（大型伺服器）」「18 PB」；「頂級超級電腦總記憶體 ≈ 10 PB」（紅色虛線）

## Wikipedia

- Quantum simulator：「A universal quantum simulator is a quantum computer proposed by Yuri Manin in 1980 and Richard Feynman in 1982.」「the dimension of the Hilbert space grows exponentially with particle number」
- Quantum computational chemistry：「the exponential growth of a quantum system's wave function with each added particle」；Jordan–Wigner「maps these fermionic orbitals to qubits」，qubit count「scales linearly with K」；「proof-of-principle chemistry calculations, though currently limited to small systems」
- Variational quantum eigensolver：「hybrid algorithm that uses both classical computers and quantum computers」；「originally proposed in 2014」；「heuristic method and thus does not guarantee convergence to the ground state value」；「may halt at suboptimal parameters」
- Hydrogen：「bond dissociation energy of 435.7 kJ/mol」
- Quantum chemistry：「the electronic wave function is adiabatically parameterized by the nuclear positions」

## 重算紀錄（製作代理，STO-3G ζ=1.24，解析高斯積分，2×2 完整組態交互作用）

| 距離（Å） | HF（Ha） | 完整（Ha） |
|---|---|---|
| 0.3 | −0.594 | −0.602 |
| 0.5 | −1.043 | −1.055 |
| 0.735（最低點） | −1.117 | −1.1373 |
| 1.0 | −1.066 | −1.101 |
| 1.5 | −0.911 | −0.998 |
| 2.0 | −0.784 | −0.949 |
| 3.0 | −0.656 | −0.934 |
| 10.0 | — | −0.9332 |

井深 0.2041 Ha ≈ 536 kJ/mol（簡化模型，大於維基實際值 435.7 kJ/mol）。0.74 Å 單參數變分：θ = 0° −1.1168（＝HF），θ ≈ 6.5° −1.1373（＝完整）。
