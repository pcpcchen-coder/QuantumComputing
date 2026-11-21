# Q087 來源筆記（逐字引文）

查核日：2026-11-18。學程內部簡報與動畫程式由製作代理讀取；維基百科兩頁由製作代理讀取；玩具題目由製作代理以 classroom.py 重算。

## 如何操作量子電腦（slides/QC_Operation_Talk.pptx）

第 18 頁「單位元量子閘一覽」表格最後一列
- 「Rx/Ry/Rz(θ) ; e−iθσ/2 ; 繞 x/y/z 軸 θ ; 任意角度：變分演算法的參數」

第 34 頁「從計數到答案：兩種輸出」
- 「期望值估計（Estimator）」「輸出：⟨ψ|O|ψ⟩ 與誤差棒」「變分演算法（VQE、QAOA）、量子模擬」「需要多個量測基底、大量 shots」

第 44 頁「量子電腦能算什麼：應用地圖」
- 「化學、材料、藥物 ; 量子相位估計、VQE、Trotter 模擬 ; 指數級（多數） ; 小分子已示範；工業級分子需數百萬實體位元等級」
- 「最佳化 ; QAOA、量子退火、Grover 類 ; 啟發式 / 平方 ; 實用優勢尚未確立」

## Wikipedia：Variational quantum eigensolver

- 「a hybrid algorithm that uses both classical computers and quantum computers」
- 「if we can vary |ψ⟩ arbitrarily then min ⟨ψ|H|ψ⟩ will be the ground state energy」
- 「The ansatz has to be adaptable enough to not miss the desired state.」
- 「A classical optimizer is used to improve the guess.」「Classical optimizers using gradient descent can be used for this purpose.」（另提參數平移規則）
- 「One can measure the expectation value of each Pauli string.」；量測次數多於量子相位估計
- 「Originally proposed in 2014」（Peruzzo、Aspuru-Guzik、O'Brien 為通訊作者）
- 「If the ansatz is not chosen adequately the procedure may halt at suboptimal parameters that do not correspond to a minimum.」「In this situation, the algorithm is said to have reached a 'barren plateau'.」
- 「It is a heuristic method and thus does not guarantee convergence to the ground state value.」
- 「As of 2022, the variational quantum eigensolver can only simulate small molecules」

## Wikipedia：Quantum approximate optimization algorithm（導向 Quantum optimization algorithms）

- 引用 Farhi、Goldstone、Gutmann（2014）「A Quantum Approximate Optimization Algorithm」
- 「the problem can be phrased as a maximization of an objective function which is a sum of Boolean functions」
- cost Hamiltonian 的基態編碼答案；mixer；「repeated application of the oracles UC and UM」；「2p angles (parameters)」
- 「The angles are then updated classically」；靈感來自「the Quantum Adiabatic theorem」
- 「a study of QAOA and MaxCut algorithm shows that p>11 is required for scalable advantage」
- 「no proven exponential speed up has ever been found」；QAOA 曾有「a better approximation ratio than any known polynomial time classical algorithm」，直到「a more effective classical algorithm was proposed」
- 「avoiding barren plateaus, which represent parameters leading to eigenstates which correspond to plateaus in the energy landscape」

## animations/js/operation/01_qubit.js

- 「得到 0 的機率是 cos²(θ/2)」；「誤差約 √(p(1−p)/N)，要精度提高 10 倍就要 100 倍的 shots」
- `ui.slider('θ（極角）', 0, 180, 1, th, (v) => { th = v; clear(); } …)`；預設鈕 `['θ=60°', 60, 30]`；`ui.button('一次跑 1000 shots', …)`
- 統計柱藍 0x4f8cff（得到 0）、紅 0xff5a5f（得到 1）；「青線 = 理論機率」

## animations/js/operation/02_gates.js

- 「點下方的閘，看狀態向量怎麼轉。粉紅線是旋轉軸。」「Rx/Ry/Rz(θ)：任意角度。」
- `ui.slider('旋轉角 θ（給 Rx / Ry / Rz）', -180, 180, 5, theta, …)`；`ui.button('Ry(θ)', …)`；`ui.button('重設 |0⟩', …)`
- 閘動畫時間 `(0.5 + |ang|/π × 0.8) / speed`；插圖「最後一個閘的矩陣與線路紀錄」

## 重算紀錄（製作代理，classroom.py，SHOTS = 0，學習率 0.4）

| 起點 | 第 40 次能量 |
|---|---|
| (20°, 20°) | −0.400 |
| (60°, 60°) | −0.400 |
| (100°, 30°) | −0.400 |
| (90°, 90°) | −1.600 |
| (120°, 120°) | −1.600 |
| (45°, 135°) | −1.600 |
| (160°, 160°) | −1.600 |
