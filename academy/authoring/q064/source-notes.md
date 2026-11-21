# Q064 來源筆記（逐字引文）

查核日：2026-11-18。Qiskit 維基百科引文沿用 Q010／Q057（同 revision）。Qiskit 與 Qiskit Aer 的定義取自本機安裝版本的函式說明文件。
學程內部簡報與動畫程式由製作代理讀取。程式由製作代理實際執行（Python 3.13.18、qiskit 2.6.2、qiskit-aer 0.18.4，/home/user/qwork/q057venv）。

## Qiskit（Wikipedia，oldid=1382602577；引自 Q010／Q057）

- 「Qiskit (Quantum Information Software Kit) is an open-source, Python-based, high-performance software stack for quantum computing」
- 「executing them on quantum computers or classical simulators.」
- 「Qiskit Aer (qiskit-aer) – A high‑performance simulator for quantum circuits, featuring multiple simulation backends and support for realistic noise models.」

## Qiskit 2.6.2 `transpile()` 說明文件

- 「optimization_level: How much optimization to perform on the circuits. Higher levels generate more optimized circuits, at the expense of longer transpilation time.」
- 「0: no optimization」「1: light optimization」「2: heavy optimization」「3: even heavier optimization」
- 「If ``None``, level 2 will be chosen as default.」

## Qiskit Aer 0.18.4 `depolarizing_error()` 說明文件

- 「The depolarizing channel is defined as: E(ρ) = (1 - λ) ρ + λ Tr[ρ] I / 2^n」
- 「If λ = 1 this is a completely depolarizing channel E(ρ) = I / 2^n」

## 學程內部簡報

- slides/QC_Operation_Talk.pptx 第 52 頁「操作一台量子電腦：檢查表」：「1 定義問題：是否『輸入小、計算難、輸出小』？要取樣還是期望值？」「2 設計線路：疊加 → 用結構安排相位 → 干涉；估算寬度、深度、兩位元閘數」「3 先用模擬器：驗證邏輯正確（≤ ~30 位元可精確模擬）」「4 挑後端」「5 轉譯：最佳化等級、初始配置；檢查轉譯後的深度與 SWAP 數」「6 設定執行：shots（依精度）…」「7 執行與讀取：取回 counts / 期望值與誤差棒」「8 後處理與驗證：讀取緩解、統計檢定、與模擬比較；答案可驗證就驗證」。講者備註：「把今天的內容整理成一份實際操作的檢查表。」
- 第 53 頁「重點回顧」：「每個 shot 重置到 |0⟩；校準決定頻率、π 脈衝、讀取閾值」「單位元閘 = 微波脈衝（面積→角度、相位→軸）+ 虛擬 Z；兩位元閘 = CZ / CR；轉譯成原生閘」「誤差 ∝ 1/√N」「Shor 指數級、Grover 平方級」。

## 本模組課綱（academy/lessons/Q049–Q063）

- Q049 一次量子計算的生命週期、Q050 初始化與校準、Q051 看懂後端校準資料、Q052 微波脈衝：面積與相位、Q053 DRAG 與虛擬 Z、Q054 任意旋轉 = 三個旋轉、Q055 兩位元閘：CZ 與交叉共振、Q056 轉譯：邏輯線路到硬體、Q057 Qiskit 實作：Bell 與 GHZ、Q058 量測基底與期望值、Q059 shots、統計誤差與讀取誤差緩解、Q060 動態線路、Q061 QFT 與相位估計、Q062 Shor：用干涉找週期、Q063 快在哪？加速的等級。
- Q013「Grover：16 個抽屜找寶藏」；Q012「Deutsch–Jozsa：一次看穿」。Q065「人造原子 vs 真的原子」：「比較超導、離子阱、中性原子如何滿足 DiVincenzo 五條件」。

## 互動動畫程式

- animations/basic-circuits.html 範例 8 id "grover"：lead「Grover 演算法只要大約 (π/4)√N 輪」；選項「位元數」2 顆（N = 4）／3 顆（N = 8）、答案、重複輪數（最佳／1／2／3 輪），best = n === 2 ? 1 : 2；3 顆預設答案 101；第 2 輪擴散 caption「答案的機率升到 94.5%」；量測列與「→ 找到答案 ✓」；take「每一輪由『標記』（把答案變號）和『擴散』（對平均值翻轉）組成」。
- 同檔範例 6 id "deutsch"：選項「黑盒裡的函數」f(x)=0、f(x)=1、f(x)=x、f(x)=1−x（預設 x）；4 步：X 閘（輔助位元）、兩顆 H、黑盒 U_f、q0 做 H；verdict「→ 常數函數」「→ 平衡函數」。
- animations/js/operation/06_circuit.js：「Grover 搜尋（2 位元，找 |11⟩）」8 欄：均勻疊加 H、H；Oracle CZ；擴散 H、X、CZ、X、H；量測「一次就找到 11（N = 4 時恰好 1 次迭代）」；「加入雜訊（每閘 1%、讀取 3%）」：sample() 以 1 − 0.99^閘數 的機率換成均勻隨機結果，再對每顆位元 3% 翻轉。

## 實跑紀錄（my_circuit_release.py，種子 2026，shots 1024，seed_transpiler 2026）

```
grover2 等級 0：深度 26、sx+x 14、cx 2、rz 20；理想 {'11': 1024}；有雜訊 {'00': 25, '01': 67, '10': 66, '11': 866}
grover2 等級 3：深度 12、sx+x 6、cx 2、rz 8；理想 {'11': 1024}；有雜訊 {'00': 18, '01': 46, '10': 45, '11': 915}
grover3 等級 0：深度 156、sx+x 47、cx 51；理想 101：969；有雜訊 101：458
grover3 等級 3：深度 95、sx+x 27、cx 39；理想 101：970；有雜訊 101：550
bell    等級 0／3 相同：深度 5；理想 {'00': 516, '11': 508}；有雜訊 {'00': 478, '01': 49, '10': 32, '11': 465}
ghz3    等級 0／3 相同：深度 6；理想 {'000': 514, '111': 510}
deutsch 等級 0：深度 9、有雜訊 1：953；等級 3：深度 7、有雜訊 1：958
```
