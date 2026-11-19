# Q114 來源筆記（逐字引文）

查核日：2026-11-19（檔頭 CHECKED 依派工統一寫 2026-11-18）。維基百科頁面由製作代理以 `action=raw` 取得原始 wikitext，revision id 取自 MediaWiki API。學程內部簡報、簡報原始稿與動畫程式由製作代理讀取。程式由製作代理實際執行。

## Quantum logic gate（Wikipedia，oldid=1376542851）

- 「[The Hadamard gate] acts on a single qubit. It maps the basis states |0⟩ ↦ (|0⟩ + |1⟩)/√2 and |1⟩ ↦ (|0⟩ − |1⟩)/√2 (it creates an equal superposition state if given a computational basis state). The two states (|0⟩ + |1⟩)/√2 and (|0⟩ − |1⟩)/√2 are sometimes written |+⟩ and |−⟩ respectively. The Hadamard gate performs a rotation of π about the axis (x̂+ẑ)/√2 at the Bloch sphere, and is therefore involutory.」
- 「For example, HZH = X」
- 「Note that for a Hermitian matrix H† = H, and because of unitarity, HH† = I, so H² = I for all Hermitian gates. They are involutory. Examples of Hermitian gates are the Pauli gates, Hadamard, CNOT, SWAP and Toffoli.」
- （Q113 已引）「It is sometimes called a bit-flip as it maps |0⟩ to |1⟩ and |1⟩ to |0⟩.」

## Born rule（Wikipedia，oldid=1368836124）

- 「it is common to describe the Born rule as saying that probability is equal to the amplitude-squared (really the amplitude times its own complex conjugate).」

## Bloch sphere（Wikipedia，oldid=1381941389）

- 「The Bloch sphere is a unit 2-sphere, with antipodal points corresponding to a pair of mutually orthogonal state vectors. The north and south poles of the Bloch sphere are typically chosen to correspond to the standard basis vectors |0⟩ and |1⟩, respectively」

## 學程內部簡報（slides/output/basic-circuits.pptx；原始稿 slides/reports/basic-circuits.js）

用 python-pptx 讀出：第 5 頁標題「範例 1｜疊加：量子硬幣」，第 6 頁標題「|+⟩ 和 |−⟩：機率一樣，差在正負號」（課綱寫 p5–6，無誤）。

- 第 5 頁：線路「q0 |0⟩ → H → 量測」；「① 起點 |0⟩ 振幅 = 1：量測一定得到 0。Bloch 向量指向北極」；「② H 閘 (|0⟩ + |1⟩)/√2 = |+⟩ 兩個振幅都是 +0.707，平方後各 50%。向量轉到赤道 +x」；「③ 量測 0 或 1，各 50% 量測時才隨機決定，狀態就此塌縮；重複 1,000 次約各 500 次」；callout「量測之前兩種可能同時存在：這不是『我們不知道』，而是兩個振幅都在，之後還能互相干涉」。備註：「量測的時候才隨機決定結果，像丟一枚公平的硬幣。要注意，量測之前兩種可能是同時存在的，不只是我們不知道而已，因為兩個振幅之後還可以互相干涉」。
- 第 6 頁：lead「起始態換成 |1⟩（先加一個 X），H 之後的振幅多了一個負號」；四格「起點 |0⟩ 量測一定得到 0」「H|0⟩ = |+⟩ 兩個都是 +0.707：機率各 50%」「起點 |1⟩ 量測一定得到 1」「H|1⟩ = |−⟩ |1⟩ 的振幅是 −0.707：機率仍各 50%」；callout「量測分不出 |+⟩ 和 |−⟩：機率 = 振幅²，負號在平方後消失。但這個負號會影響下一步」。備註：「這個看不到的負號就是所謂的相位，它雖然量不到，卻會改變後面干涉的結果。」

## 互動動畫程式（animations/basic-circuits.html #superposition）

- 選項 `{ key: "start", label: "起始態", def: "0", choices: [["0", "|0⟩"], ["1", "|1⟩"]] }`；選 |1⟩ 時先加步驟「X 閘：準備 |1⟩」，說明「X 閘是量子版的 NOT，把 |0⟩ 翻成 |1⟩，Bloch 向量從北極轉到南極。」
- H 步驟說明：|0⟩ 起點「H 閘：|0⟩ → (|0⟩ + |1⟩)/√2，稱為 |+⟩。兩個振幅都是 +0.707，平方後各 50%。Bloch 向量轉到赤道上的 +x 方向。」；|1⟩ 起點「H 閘：|1⟩ → (|0⟩ − |1⟩)/√2，稱為 |−⟩。|1⟩ 的振幅變成 −0.707（負號），但平方後機率仍是各 50%，量測分不出 |+⟩ 和 |−⟩。Bloch 向量指向 −x。」
- 重點：「機率 = 振幅²。|+⟩ 和 |−⟩ 量起來完全一樣，差別只在振幅的正負號（也就是『相位』）。」
- CSS（淺色）：`--pos:#1D6A8B`（藍）、`--neg:#B65C12`（橘）、`--x:#A23B5C`（酒紅）、`--hit:#2C8A55`（綠）；`.bloch .vec{stroke:var(--neg)}`；`.htrack .exp{background:var(--ghost)}`（灰）、`.htrack .got{background:var(--hit)}`（綠）。
- `rebuild(reset)`：「換範例時回到起點；只改選項時停在最後一步，方便比較結果。」`go()` 內呼叫 `clearShots()`；#m1 一次加 1 次、#m1000 每 30 ms 加 40 次直到 1000 次，量測會累加。

## 互動動畫程式（animations/operation.html#qubit，js/operation/01_qubit.js）

- 說明：「注意：改變 φ 不會改變 0/1 的機率 —— 相位在 Z 測量中看不見，只有經過干涉（量子閘）才會顯現出來。」
- `p0 = () => Math.cos((th * Math.PI) / 360) ** 2`；滑桿「θ（極角）」回呼會 clear()，「φ（相位）」回呼只設 ph；預設鈕 `['|+⟩', 90, 0]`；按鈕「一次跑 1000 shots」「清除統計」；標籤「青線 = 理論機率」；ideal0／ideal1 高度由 p0() 決定。

## 實跑紀錄

`coin.py`（Python 3.13.18，只用標準函式庫，random.Random(1114)）：

```
一、兩種疊加態（機率 = 振幅²）
  |+⟩ = H|0⟩    |0⟩ +0.707（50%）  |1⟩ +0.707（50%）
  |−⟩ = H|1⟩    |0⟩ +0.707（50%）  |1⟩ −0.707（50%）
二、各量測 1000 次
  |+⟩   0 → 491 次  1 → 509 次
  |−⟩   0 → 485 次  1 → 515 次
三、盲測 5 回合（先看次數猜，再看答案）
  第 1 回  0 → 486 次  1 → 514 次    答案：|+⟩
  第 2 回  0 → 518 次  1 → 482 次    答案：|+⟩
  第 3 回  0 → 494 次  1 → 506 次    答案：|−⟩
  第 4 回  0 → 508 次  1 → 492 次    答案：|−⟩
  第 5 回  0 → 483 次  1 → 517 次    答案：|−⟩
四、改造區：再加一個 H
  H → H         |0⟩ +1.000（100%）  |1⟩ 0（0%）
  X → H → H     |0⟩ 0（0%）  |1⟩ +1.000（100%）
```

`qiskit_check.py`（Qiskit 2.6.2，StatevectorSampler seed=2026）：

```
|+⟩ 振幅 [0.707, 0.707] 機率 {'0': 0.5, '1': 0.5} 量測 1000 次 {'0': 464, '1': 536}
|−⟩ 振幅 [0.707, -0.707] 機率 {'0': 0.5, '1': 0.5} 量測 1000 次 {'0': 464, '1': 536}
|+⟩ 再加 H 振幅 [1.0, 0.0] 機率 {'0': 1.0} 量測 1000 次 {'0': 1000}
|−⟩ 再加 H 振幅 [0.0, 1.0] 機率 {'1': 1.0} 量測 1000 次 {'1': 1000}
```

## 動畫畫面（製作代理以 Playwright 1600×900 實拍；basic-circuits.html zoom 0.8）

- #superposition 下一步：|ψ⟩ = (|0⟩ + |1⟩) / √2，兩根藍柱 +.707、50%，橘色向量在 +x。
- 選 |1⟩、起點、下一步：|ψ⟩ = |1⟩，|1⟩ 柱 +1.000、100%，向量在南極；X 方塊酒紅、H 方塊淡色（.future）。再下一步：|ψ⟩ = (|0⟩ − |1⟩) / √2，|1⟩ 橘柱 −.707、50%，向量在 −x。
- 選 |1⟩（直接停在第 2 步）、量測 1 次 × 3、量測 1,000 次：綠框「q0 = …」，共 1,003 次，綠條約各半；改選 |0⟩ 後量測清除，再量 1,000 次約各半。
- operation.html#qubit：|+⟩ → 一次跑 1000 shots（兩柱約一樣高）；φ 0→180：箭頭沿赤道轉到 x 軸反方向，柱子與青線不動，readout「β = 0.707·e^i180°」「理論：P(0) = 0.500，P(1) = 0.500」。
