# Q118 來源筆記（逐字引文）

查核日：2026-11-19（檔頭 CHECKED 依派工統一寫 2026-11-18）。維基百科頁面由製作代理以 `action=raw` 取得原始 wikitext（2026-11-19；查 revision id 的 API 當時回應限流，未記錄版本號）。學程內部簡報、簡報原始稿與動畫程式由製作代理讀取。程式由製作代理實際執行。

## Quantum teleportation（Wikipedia）

- 「'''Quantum teleportation''' is a technique for transferring [[quantum information]] from a sender at one location to a receiver some distance away. While [[teleportation]] is commonly portrayed in [[science fiction]] as a means to transfer physical objects from one location to the next, quantum teleportation only transfers quantum information.」
- 「The sender does not have to know the particular quantum state being transferred. Moreover, the location of the recipient can be unknown, but to complete the quantum teleportation, classical information needs to be sent from sender to receiver. Because classical information needs to be sent, quantum teleportation cannot occur faster than the speed of light.」
- 「This process involves moving the information ''between carriers'' and not movement of the ''actual carriers''」
- 「Since the initial quantum information is "destroyed" as it becomes part of the entangled state, the no-cloning theorem is maintained as the information is recreated from the entangled state and not copied during teleportation.」
- 「Because of this need for the traditional channel, the speed of teleportation can be no faster than the speed of light (hence the [[no-communication theorem]] is not violated).」
- 「The resources required for quantum teleportation are a [[communication channel]] capable of transmitting two classical bits, a means of generating an entangled [[Bell state]] of qubits and distributing to two different locations, performing a [[Bell measurement]] on one of the Bell state qubits, and manipulating the quantum state of the other qubit from the pair.」
- 「A Bell measurement of the Bell state qubit and the qubit to be teleported (|φ⟩) is performed at location A. This yields one of four measurement outcomes which can be encoded in two classical bits of information.」
- 「Of these four possible states, one is identical to the original quantum state |φ⟩, and the other three are closely related. ... The Bell state qubit at location B is then modified in one of three ways, or not at all, which results in a qubit identical to |φ⟩」
- 「First proposed theoretically in 1993, quantum teleportation has since been demonstrated in many different guises. ... In 1997, two groups experimentally achieved quantum teleportation.」（本課旁白未用年代，只記在教材背景）

## Deferred measurement principle（Wikipedia）

- 「The '''deferred measurement principle''' is a result in [[quantum computing]] which states that delaying measurements until the end of a quantum computation doesn't affect the [[probability distribution]] of outcomes.」
- 「A consequence of the deferred measurement principle is that measuring commutes with conditioning.」
- 圖說（隱形傳態電路的兩種寫法）：「Measurement is performed early and the resulting classical bits are sent. The classical bits control if the 1-qubit X and Z gates are executed, allowing teleportation.」「By moving the measurement to the end, the 2-qubit controlled-X and -Z gates need to be applied, which requires both qubits to be near (i.e. at a distance where 2-qubit quantum effects can be controlled), and thus limits the distance of the teleportation. While logically equivalent, deferring the measurement have physical implications.」

## No-cloning theorem（Wikipedia）

- 「the '''no-cloning theorem''' states that it is impossible to create an independent and identical copy of an arbitrary unknown [[quantum state]]」

## No-communication theorem（Wikipedia）

- 「It asserts that during the measurement of an [[Quantum entanglement|entangled quantum state]], it is impossible for one observer to transmit information to another observer, regardless of their spatial separation. This conclusion preserves the principle of causality in [[quantum mechanics]] and ensures that information transfer does not violate special relativity by exceeding the speed of light.」

## 學程內部簡報（slides/output/basic-circuits.pptx；原始稿 slides/reports/basic-circuits.js）

用 python-pptx 讀出：第 15 頁「範例 5｜隱形傳態：用糾纏把狀態送過去」、第 16 頁「Alice 量到什麼、Bob 怎麼修」、第 17 頁「動畫：用 Bloch 球看狀態搬家」（課綱寫 p15–17，無誤）。

- 第 15 頁：「q0 |0⟩（Alice）」「q1 |0⟩（Alice）」「q2 |0⟩（Bob）」；「① 準備 ψ（q0）例：ψ = √¾|0⟩ + ½|1⟩。Alice 不必知道 ψ 是什麼」「② 建立糾纏對 H + CNOT：q1、q2 成為 Bell 態；q2 交給遠方的 Bob」「③ Alice：CNOT、H Bell 量測的前半；量 q0、q1 得到 2 個位元」「④ Bob：依結果修正 q1 = 1 做 X、q0 = 1 做 Z：q2 就變成 ψ」。
- 第 15 頁備註：「用一個 Ry 閘準備出來」「她把這兩個位元用電話告訴 Bob，Bob 依照結果修正：q1 是 1 就做 X，q0 是 1 就做 Z，q2 就變成 ψ。整個過程沒有搬動任何粒子。」
- 第 16 頁表格：00 ¼ ψ 不用修 ψ／01 ¼ Zψ Z ψ／10 ¼ Xψ X ψ／11 ¼ XZψ 先 X、再 Z ψ；「收到 2 個位元之前，Bob 不知道是哪一種，q2 對他來說完全隨機：隱形傳態不能超光速」。
- 第 16 頁備註：「四種等量混在一起，q2 對他來說完全隨機。所以隱形傳態不能超光速，資訊還是要靠古典通訊送過去。」
- 第 17 頁：「② 之後 q2 縮到球心：糾纏中的 q2 單看完全隨機」「④ 之後 q2 指向 ψ，q0 卻不再是 ψ：狀態是搬過去，不是複製（不可複製定理）」「上方可換 ψ：|+⟩ 和 |−⟩ 量起來都是 50/50，要看 Bloch 球才分得出來」「動畫用受控閘代替「量測後再修正」（延遲量測原理），q2 的結果相同」。

## 動畫原始碼（animations/basic-circuits.html，SCENES id "teleport"）

- 選項 `{ key: "psi", label: "要傳的狀態 ψ", def: "ry", choices: [["ry", "√¾|0⟩+½|1⟩"], ["1", "|1⟩"], ["plus", "|+⟩"], ["minus", "|−⟩"]] }`；準備 `ry: RY(0, π/3)`、`"1": X(0)`、`plus: H(0)`、`minus: X(0), H(0)`。
- `n: 3, meas: [2], bloch: [0, 2]`；步驟「準備要傳的狀態 ψ（q0）」「建立糾纏對（q1、q2）」[H(1)], [CX(1, 2)]「Alice：CNOT 與 H（Bell 量測的前半）」[CX(0, 1)], [H(0)]「Bob：依 2 個位元修正」[CX(1, 2)], [CZ(0, 2)]，`box: "修正（2 個古典位元）"`。
- 第 4 步說明：「這裡用受控閘代替「量測後再修正」（延遲量測原理），q2 的結果完全相同。修正後 q2 的向量回到 ψ，而 q0 不再是 ψ：狀態是搬過去，不是複製。」
- `verdict: () => "→ 對照 ψ：q2 的量測機率和 ψ 相同"`（只在最後一步顯示）；Bloch 球標籤 `單看 q${q}`；`rebuild(false)` 換選項時停在最後一步。

## 動畫原始碼（animations/js/operation/06_circuit.js，「量子隱形傳態」）

- `tele: { name: '量子隱形傳態', n: 3, meas: [2], cols: [ [[RY(0, 2π/3)], '準備要傳送的狀態：q0 = cos60°|0⟩ + sin60°|1⟩（P(1) = 0.75）'], … [[CX(1, 2)], 'Bob 依 q1 的結果做 X（延遲量測：改成受控閘）'], [[CZ(0, 2)], 'Bob 依 q0 的結果做 Z → q2 變成原本 q0 的狀態（看左側小球）'], [M([2]), '量測 q2：P(1) = 0.75，和一開始的 q0 相同'] ] }`（教材導覽選用）。

## 程式實跑

`teleport_lab.py`（Python 3.13.18，只用標準函式庫，random.Random(1118)）與 `qiskit_check.py`（Qiskit 2.6.2，StatevectorSampler seed=2026）的完整輸出見 `classroom.py` 的 RUN_OUTPUT、QISKIT_OUTPUT（建置時會重跑 teleport_lab.py 並比對）。摘要：

- 四種 ψ：② 之後單看 q2 大小 0.00；④ 之後 q2 = ψ（四種都 True）；單看 q0 四種傳完都是 (x +1.00, z +0.00)（True）；③ 之後 q0：√¾|0⟩+½|1⟩ 大小 0.50、|1⟩ (x −1.00)、|+⟩／|−⟩ 0.00。
- Alice 表（ψ = √¾|0⟩+½|1⟩）：四種結果各 0.25；Bob 手上 ψ、Zψ、Xψ、XZψ；修正後都是 ψ。
- 先量再修各 1000 次：每次修完都等於 ψ（程式內 assert）；Bob 量到 1：245、1000、524、517 次（理論 250、1000、500、500）。
- 不修：四種都「錯 0.50 0.00」；只修 X：|1⟩ 對，√¾|0⟩+½|1⟩ 錯 0.25 0.50，|+⟩、|−⟩ 錯 0.50 0.00；只修 Z：|+⟩、|−⟩ 對，|1⟩ 錯 0.50 0.00，√¾|0⟩+½|1⟩ 錯 0.50 0.87。
- Qiskit：兩個都修相似度 1.000；不修 0.500；只修 X：√¾|0⟩+½|1⟩ 0.625、|1⟩ 1.000、|+⟩／|−⟩ 0.500。

## 動畫畫面（製作代理以 Playwright 1600×900 實拍；basic-circuits.html zoom 0.8）

- #teleport 預設 ψ：起點兩支向量尖端 (100, 29.5)（北極）；① |ψ⟩ = 0.866|000⟩ + 0.500|001⟩，q0 尖端 (66.4, 84.1)；② q2 (100, 104)＝球心；③ q0 (80.6, 114.0) 變短；④ q2 (66.4, 84.1)＝① 的 q0 方向、q0 (61.2, 124.0)；量測 1,000 次：0、1 兩列，理論 0 75%、1 25%，實拍 766／234，綠字「→ 對照 ψ：q2 的量測機率和 ψ 相同」。
- 換 |1⟩：(|100⟩ + |101⟩ + |110⟩ + |111⟩) / 2，q2 (100, 178.5) 南極；|+⟩：8 根 +.354，q2 (61.2, 124.0)；|−⟩：|100⟩…|111⟩ −.354 橘，q2 (138.8, 84.0)；四種 q0 都在 (61.2, 124.0)。
- |1⟩ 按 `#dots button:nth-child(4)`：「步驟 3 / 4」，(|010⟩ − |011⟩ + |100⟩ − |101⟩) / 2，q2 在球心；量 1,000 次理論 0、1 各 50%（實拍 520／480），沒有綠字；下一步後量 1,000 次：只有「1」一列，1000 次，綠字出現。
