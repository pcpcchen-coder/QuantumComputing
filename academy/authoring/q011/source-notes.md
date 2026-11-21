# Q011 來源筆記（逐字引文）

查核日：2026-11-18。維基百科頁面由製作代理直接開啟（revision id 取自頁面的 wgRevisionId）。學程內部簡報與動畫程式由製作代理讀取；動畫引擎由製作代理在 Node 執行。

## Quantum teleportation（Wikipedia，oldid=1384656230）

- 「Quantum teleportation is a technique for transferring quantum information from a sender at one location to a receiver some distance away.」
- 「While teleportation is commonly portrayed in science fiction as a means to transfer physical objects from one location to the next, quantum teleportation only transfers quantum information.」
- 「The sender does not have to know the particular quantum state being transferred.」
- 「Because classical information needs to be sent, quantum teleportation cannot occur faster than the speed of light.」
- 「The resources required for quantum teleportation are a communication channel capable of transmitting two classical bits, a means of generating an entangled Bell state of qubits and distributing to two different locations, performing a Bell measurement on one of the Bell state qubits, and manipulating the quantum state of the other qubit from the pair.」
- 「Since the initial quantum information is "destroyed" as it becomes part of the entangled state, the no-cloning theorem is maintained as the information is recreated from the entangled state and not copied during teleportation.」
- 「Teleportation does not result in the copying of qubits, and hence is consistent with the no-cloning theorem. There is no transfer of matter or energy involved. Alice's particle has not been physically moved to Bob; only its state has been transferred.」
- 「For every qubit teleported, Alice needs to send Bob two classical bits of information.」
- 「The result of Alice's (local) measurement is a collection of two classical bits (00, 01, 10 or 11) related to one of the following four states (with equal probability of 1/4)」
- 「(This is the only potentially time-consuming step after step 1 since information transfer is limited by the speed of light.)」

## 學程內部簡報（slides/output/basic-circuits.pptx）

- 第 15 頁「範例 5｜隱形傳態：用糾纏把狀態送過去」：「q0 |0⟩（Alice）」「q1 |0⟩（Alice）」「q2 |0⟩（Bob）」；「① 準備 ψ（q0）例：ψ = √¾|0⟩ + ½|1⟩。Alice 不必知道 ψ 是什麼」「② 建立糾纏對 H + CNOT：q1、q2 成為 Bell 態；q2 交給遠方的 Bob」「③ Alice：CNOT、H Bell 量測的前半；量 q0、q1 得到 2 個位元」「④ Bob：依結果修正 q1 = 1 做 X、q0 = 1 做 Z：q2 就變成 ψ」。備註：「她把這兩個位元用電話告訴 Bob……整個過程沒有搬動任何粒子。」
- 第 16 頁「Alice 量到什麼、Bob 怎麼修」：00 ¼ ψ 不用修；01 ¼ Zψ Z；10 ¼ Xψ X；11 ¼ XZψ 先 X、再 Z；「收到 2 個位元之前，Bob 不知道是哪一種，q2 對他來說完全隨機：隱形傳態不能超光速」。
- 第 17 頁「動畫：用 Bloch 球看狀態搬家」：「② 之後 q2 縮到球心：糾纏中的 q2 單看完全隨機」「④ 之後 q2 指向 ψ，q0 卻不再是 ψ：狀態是搬過去，不是複製（不可複製定理）」「動畫用受控閘代替『量測後再修正』（延遲量測原理），q2 的結果相同」。

## 互動動畫程式

- animations/basic-circuits.html（SCENES id "teleport"）：選項「要傳的狀態 ψ」：√¾|0⟩+½|1⟩（預設）、|1⟩、|+⟩、|−⟩；四步「準備要傳的狀態 ψ（q0）」「建立糾纏對（q1、q2）」「Alice：CNOT 與 H（Bell 量測的前半）」「Bob：依 2 個位元修正」（方框「修正（2 個古典位元）」）；meas: [2]、bloch: [0, 2]；verdict「→ 對照 ψ：q2 的量測機率和 ψ 相同」；take「……量子網路與模組化量子電腦都靠它在不同晶片之間搬運量子態。」；量測卡說明「灰色底是理論機率，綠色是實際次數」。
- animations/js/operation/06_circuit.js（tele）：「量子隱形傳態」八欄 Ry(2π/3)、H、CX(1,2)、CX(0,1)、H、CX(1,2)、CZ(0,2)、M；最後一欄註「量測 q2：P(1) = 0.75，和一開始的 q0 相同」；量測跑 1000 shots；插圖標題「量測 1000 shots 的結果（青線 = 理想機率）」。

## 引擎實算（Node 執行 basic-circuits.html 的 engine script）

```
ψ = √¾|0⟩+½|1⟩：q2 量測理論  步 0–1 {0:1}；步 2–3 {0:.5, 1:.5}；步 4 {0:.75, 1:.25}
                單看 q0：步 1 (.87,0,.5)；步 3 (.5,0,0)；步 4 (1,0,0)   單看 q2：步 2–3 (0,0,0)；步 4 (.87,0,.5)
ψ = |1⟩：       單看 q0：步 1 (0,0,−1)；步 3 (−1,0,0)；步 4 (1,0,0)    單看 q2：步 1 (0,0,1)；步 2–3 (0,0,0)；步 4 (0,0,−1)
```
