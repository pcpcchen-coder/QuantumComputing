# Q061 來源筆記（逐字引文）

查核日：2026-11-18。維基百科頁面由製作代理以 `index.php?action=raw` 取得 wikitext（存於 `/home/user/qwork/q061wiki/`，未記 oldid）。學程內部簡報與動畫程式由製作代理讀取。

## Quantum Fourier transform（Wikipedia）

- 「In quantum computing, the quantum Fourier transform (QFT) is a linear transformation on quantum bits, and is the quantum analogue of the discrete Fourier transform.」
- 「The quantum Fourier transform is a part of many quantum algorithms, notably Shor's algorithm for factoring and computing the discrete logarithm, the quantum phase estimation algorithm for estimating the eigenvalues of a unitary operator, and algorithms for the hidden subgroup problem.」
- 「The discrete Fourier transform on 2^n amplitudes can be implemented as a quantum circuit consisting of only O(n^2) Hadamard gates and controlled phase shift gates, where n is the number of qubits.」
- 「Because measurement collapses the quantum state to a single basis state, not every task that uses the classical Fourier transform can take advantage of the quantum Fourier transform's exponential speedup.」
- 「In case that |x⟩ is a basis state, the quantum Fourier transform can also be expressed as the map QFT: |x⟩ ↦ (1/√N) Σ_k ω_N^{xk} |k⟩.」
- 「Summing up the number of gates, excluding the ones needed for the output reversal, gives n + (n−1) + ⋯ + 1 = n(n+1)/2 = O(n^2) gates」；「the number of gates used is n(n+1)/2 which is equal to 6, for n=3.」
- 「a swap operation of the qubits must be performed to reverse their order. At most n/2 swaps are required.」

## Quantum phase estimation algorithm（Wikipedia）

- 「the quantum phase estimation algorithm is a quantum algorithm to estimate the phase corresponding to an eigenvalue of a given unitary operator.」「initially introduced by Alexei Kitaev in 1995.」
- 「Phase estimation is frequently used as a subroutine in other quantum algorithms, such as Shor's algorithm, …」
- 步驟：H^{⊗n} 作用在第一暫存器；受控 U：「U_C = ∏ C_ℓ(U^{2^ℓ})」；「Apply inverse quantum Fourier transform」；「Measurement」。
- 「It follows that Pr(a)=1 if δ=0, that is, when θ can be written as θ=a/2^n, one always finds the outcome y=a.」
- 「We conclude that the algorithm provides the best n-bit estimate (i.e., one that is within 1/2^n of the correct answer) of θ with probability at least 4/π^2.」
- 「the algorithm returns with high probability an approximation for θ, within additive error ε, using n=O(log(1/ε)) qubits in the first register, and O(1/ε) controlled-U operations.」
- Toy example：「If on the other hand λ=e^{2πi/3}, then p± = [1 ± cos(2π/3)]/2, that is, p+=1/4 and p−=3/4.」「Applying the inverse QFT amounts in this case to applying a Hadamard gate.」

## 學程內部簡報：slides/QC_Operation_Talk.pptx

- 第 41 頁「Shor 演算法：用干涉找週期」：「③ 量測第二暫存器後：間隔 r = 4 的「梳子」」「④ QFT 後：峰值在 64k/r = 0、16、32、48」；表格「④ QFT／週期 r → 頻率峰值 64k/r（其他位置干涉抵消）」。講者備註：「第四步，量子傅立葉轉換把間隔 r 的梳子變成位置在 64k/r 的峰值，其他位置因為干涉抵消」。
- 第 44 頁「量子電腦能算什麼：應用地圖」：「化學、材料、藥物；量子相位估計、VQE、Trotter 模擬」。

## 互動動畫程式

- operation.html 場景 6 circuit（js/operation/06_circuit.js 第 60–69 行）：`qft: { name: '量子傅立葉轉換（QFT，輸入 |110⟩）', n: 3 …}`，欄位：X(1)、X(2)「準備輸入 |110⟩ = 6」→ H q2 → P(π/2) → P(π/4) → H q1 → P(π/2) → H q0 →「SWAP 調整位元順序 → 振幅大小相同，相位依 e^{2πi·6k/8} 變化（看顏色）」→「量測：8 個結果機率相同 —— 資訊都在相位裡，所以 QFT 要搭配其他步驟（如 Shor）」。描述「下方柱子是當下的狀態向量（高度 = 機率，顏色 = 相位）」。CP 方塊顏色 COL.CP = 0x8a5cd0（紫）。按鈕：範例列（第 168–169 行）、「⏮ 重設」「單步 ▶」「播放」（第 171–173 行）、toggle「加入雜訊（每閘 1%、讀取 3%）」（第 174 行）。
- operation.html 場景 10 shor（js/operation/10_shor.js）：STEPS（第 55 行）「③ 量測第二暫存器 → 只留下 f(x) 相同的 x（間隔 = r）」「④ QFT：週期 r 轉成峰值，位置 ≈ 64·k / r」；峰值標籤 teal（0x38c6d9）；讀數「峰值應在 64k/r：…」；按鈕「下一步 ▶」「自動播放」「重設」（第 80–82 行）。
- operation.html 場景 8 interference（js/operation/08_interference.js）：「H 把 |0⟩ 分成兩條路徑，中間在 |1⟩ 路徑加相位 φ，第二個 H 再合併」；滑桿「A：相位 φ」（第 71 行）；讀數「P(0) = cos²(φ/2)」；小圖「結果 P(0) 與 φ 的關係（干涉條紋）」。

## 數值重算

`/home/user/qwork/q061calc/checks.py`（qiskit 2.6.2、qiskit-aer 0.18.4，`AerSimulator(seed_simulator=61)`，輸出 `checks.out`）；截圖 `/home/user/qwork/q061shots/`（1600×900 Chromium swiftshader）。
