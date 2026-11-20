# Q115 來源筆記（逐字引文）

查核日：2026-11-19（檔頭 CHECKED 依派工統一寫 2026-11-18）。維基百科頁面由製作代理以 `action=raw` 取得原始 wikitext（2026-11-19）；MediaWiki API 查 revision id 時回 429（請求過多），本次未記 oldid（Quantum logic gate、Born rule 的引文與 Q114 記錄的 oldid=1376542851、oldid=1368836124 內容一致）。學程內部簡報、簡報原始稿與動畫程式由製作代理讀取。程式由製作代理實際執行。

## Quantum logic gate（Wikipedia）

- 「Pauli ''Z'' leaves the basis state |0⟩ unchanged and maps |1⟩ to −|1⟩. Due to this nature, Pauli ''Z'' is sometimes called phase-flip.」
- 「It is sometimes called a bit-flip as it maps |0⟩ to |1⟩ and |1⟩ to |0⟩.」（Pauli-X）
- 「[The Hadamard gate] acts on a single qubit. It maps the basis states |0⟩ ↦ (|0⟩ + |1⟩)/√2 and |1⟩ ↦ (|0⟩ − |1⟩)/√2 … The Hadamard gate performs a rotation of π about the axis (x̂+ẑ)/√2 at the Bloch sphere, and is therefore involutory.」
- 「If the Hermitian (so H† = H⁻¹ = H) Hadamard gate is used to perform a change of basis, it flips x̂ and ẑ. For example, HZH = X and H√X H = √Z = S.」

## Born rule（Wikipedia）

- 「it is common to describe the Born rule as saying that probability is equal to the amplitude-squared (really the amplitude times its own complex conjugate).」

## Probability amplitude（Wikipedia）

- 「The complex amplitudes which represent the electron passing each slit (ψ_first and ψ_second) follow the law of precisely the form expected: ψ_total = ψ_first + ψ_second. This is the principle of quantum superposition. The probability, which is the modulus squared of the probability amplitude, then, follows the interference pattern under the requirement that amplitudes are complex」
- 「The crucial term 2|ψ_first||ψ_second| cos(φ1 − φ2) is called the "interference term", and this would be missing if we had added the probabilities.」
- 「However, one may choose to devise an experiment in which the experimenter observes which slit each electron goes through. Then, due to wavefunction collapse, the interference pattern is not observed on the screen.」

## 學程內部簡報（slides/output/basic-circuits.pptx；原始稿 slides/reports/basic-circuits.js）

用 python-pptx 讀出：第 7 頁「範例 2｜干涉：H‑Z‑H = X」、第 8 頁「振幅逐步看：負號怎麼變成結果」、第 9 頁「路徑加總：為什麼會抵消」（課綱寫 p7–9，無誤）。

- 第 7 頁：線路 q0 |0⟩ ① H ② Z ③ H；「① 第一個 H |+⟩ 做出疊加：位元同時走『0』和『1』兩條路徑」「② Z 閘 |−⟩ = (|0⟩ − |1⟩)/√2 只給 |1⟩ 加負號。機率仍是各 50%，這一步量不出差別」「③ 第二個 H |1⟩ 兩條路徑重新混合：到 |0⟩ 的互相抵消，到 |1⟩ 的互相加強」；callout「拿掉中間的 Z：H·H 什麼都沒做，結果回到 100% 的 0。只差一個看不到的負號，結果就完全相反」。備註：「…第三步再做一次 H，結果變成 100% 的 1。如果把中間的 Z 拿掉，兩個 H 互相抵消，結果是 100% 的 0。只差一個量不到的負號，最後的結果就完全相反，這就是干涉。動畫裡可以切換有沒有 Z 來比較。」
- 第 8 頁：「① H 之後 +1/√2 |0⟩ +1/√2 |1⟩ |+⟩：兩條路徑都是正的」「② Z 之後 +1/√2、−1/√2 |−⟩：|1⟩ 變號，機率仍各 50%」「③ 第二個 H 0、+1 100% 量到 1：H·Z·H = X」「對照：沒有 Z +1、0 H·H = I：100% 量到 0」；callout「② 和 ① 的機率完全相同，差別只在正負號；③ 的 H 把正負號『翻譯』成 0 或 1」。備註：「第二步 Z 之後，|1⟩ 那根變成負的，但長度沒變，所以機率一樣。」
- 第 9 頁：「到 |0⟩：(+½) + (−½) = 0 從 |−⟩ 做 H：兩條路徑正負相反，互相抵消（破壞性干涉）」「到 |1⟩：(+½) + (+½) = 1 從 |−⟩ 做 H：兩條路徑同號，互相加強（建設性干涉）」「沒有 Z：½ + ½ = 1，½ − ½ = 0 從 |+⟩ 做 H：到 |0⟩ 加強、到 |1⟩ 抵消，所以 H·H = I」；條列「量子力學裡，每一條路徑都帶一個振幅，最後把同一個結果的振幅相加」「振幅有正有負，所以相加時可以互相抵消，這是古典機率做不到的」。備註：「古典機率只會相加、不會抵消，振幅有正負號才會抵消」。

## 互動動畫程式（animations/basic-circuits.html #interference）

- `id: "interference", short: "干涉", title: "干涉：H‑Z‑H = X"`；選項 `{ key: "z", label: "中間的閘", def: "1", choices: [["1", "有 Z"], ["0", "沒有 Z"]] }`。
- 步驟「第一個 H：做出疊加」「Z 閘：只改正負號」（說明「Z 給 |1⟩ 的振幅加上負號：|+⟩ → |−⟩。看振幅長條：機率還是各 50%，這一步量測完全看不出差別。Bloch 向量繞 z 軸轉半圈。」）「第二個 H：干涉」（有 Z：「到 |0⟩ 的兩條路徑是 +½ 和 −½，互相抵消（破壞性干涉）；到 |1⟩ 的是 +½ 和 +½，疊加成 1（建設性干涉）。結果 100% 是 1，所以 H·Z·H = X。」；沒有 Z：「H·H 等於什麼都沒做，回到 100% 的 0。」）。
- CSS（淺色）：`--pos:#1D6A8B`（藍）、`--neg:#B65C12`（橘）、`--h:#1D6A8B`、`--z:#7348A3`（紫）、`--hit:#2C8A55`（綠）；`.bloch .vec{stroke:var(--neg)}`；`#circ .head` 橘色虛線。
- `rebuild(reset)`：「換範例時回到起點；只改選項時停在最後一步，方便比較結果。」`go()` 內呼叫 `clearShots()`；柱子在兩步間 650 ms 線性內插；單顆位元的 Bloch 向量照閘的旋轉軸轉 π（AXIS：H [R2, 0, R2]、Z [0, 0, 1]）。`histRender` 只列 `marginal` 中機率 ≥ 1e-12 的結果。

## 互動動畫程式（animations/operation.html#interference，js/operation/08_interference.js）

- 說明：「單一量子位元：H 把 |0⟩ 分成兩條路徑，中間在 |1⟩ 路徑加相位 φ，第二個 H 再合併。φ = 0 時通往 |1⟩ 的兩支箭頭方向相反 → 抵消，結果 100% 是 0；φ = 180° 時反過來。」「若中途『偷看』走哪一條路（測量），干涉消失，變成 50/50。」
- 標籤「藍 = 經由 |0⟩ 的貢獻　橙 = 經由 |1⟩ 的貢獻　白 = 總和」「相位 φ」「結果 |0⟩」「結果 |1⟩」；phBox 顏色 0x8a5cd0；pf0／pf1 用 'gold' 樣式（css `.lbl.gold{color:#ffd28a}`）。
- 計算：`c0a = [0.5, 0], c0b = [0.5cos φ, 0.5sin φ], c1a = [0.5, 0], c1b = [−0.5cos φ, −0.5sin φ]`；控制項 radio「單一量子位元：兩條路徑」、slider「A：相位 φ」0–360、toggle「A：自動掃描 φ」「A：中途偵測路徑（破壞干涉）」。

## 實跑紀錄

`paths.py`（Python 3.13.18，只用標準函式庫，random.Random(1115)）：

```
一、逐步看振幅（有 Z）
  起點          |0⟩ +1.000（100%）  |1⟩ 0（0%）
  H           |0⟩ +0.707（50%）  |1⟩ +0.707（50%）
  H → Z       |0⟩ +0.707（50%）  |1⟩ −0.707（50%）
  H → Z → H   |0⟩ 0（0%）  |1⟩ +1.000（100%）
二、對照組（拿掉 Z）
  起點          |0⟩ +1.000（100%）  |1⟩ 0（0%）
  H           |0⟩ +0.707（50%）  |1⟩ +0.707（50%）
  H → H       |0⟩ +1.000（100%）  |1⟩ 0（0%）
三、路徑加總表（同一個結果的兩條路徑先相加，再平方）
  H → Z → H（最後一個 H 之前：|0⟩ +0.707、|1⟩ −0.707）
    到 |0⟩  經由 0：+0.500  經由 1：−0.500  總和 0  機率 0%
    到 |1⟩  經由 0：+0.500  經由 1：+0.500  總和 +1.000  機率 100%
  H → H（最後一個 H 之前：|0⟩ +0.707、|1⟩ +0.707）
    到 |0⟩  經由 0：+0.500  經由 1：+0.500  總和 +1.000  機率 100%
    到 |1⟩  經由 0：+0.500  經由 1：−0.500  總和 0  機率 0%
四、錯誤示範：把機率相加
  每條路徑的機率 0.25，兩條相加 0.50：到 |0⟩、到 |1⟩ 都是 50%，算不出抵消
五、各量測 1000 次
  H → Z → H   0 → 0 次  1 → 1000 次
  H → H       0 → 1000 次  1 → 0 次
六、改造區
  H → X → H   |0⟩ +1.000（100%）  |1⟩ 0（0%）
  H → X → H（最後一個 H 之前：|0⟩ +0.707、|1⟩ +0.707）
    到 |0⟩  經由 0：+0.500  經由 1：+0.500  總和 +1.000  機率 100%
    到 |1⟩  經由 0：+0.500  經由 1：−0.500  總和 0  機率 0%
```

`qiskit_check.py`（Qiskit 2.6.2，StatevectorSampler seed=2026）：

```
H‑Z‑H 振幅 [0.0, 1.0] 機率 {'1': 1.0} 量測 1000 次 {'1': 1000}
H‑H   振幅 [1.0, 0.0] 機率 {'0': 1.0} 量測 1000 次 {'0': 1000}
H‑Z‑H 和 X 是同一個運算嗎？ True
H‑H 和「什麼都不做」是同一個運算嗎？ True
```

## 動畫畫面（製作代理以 Playwright 1600×900 實拍；basic-circuits.html zoom 0.8）

- #interference（有 Z）起點：|ψ⟩ = |0⟩，步驟 0 / 3，向量在北極。下一步：(|0⟩ + |1⟩) / √2，兩根藍柱 +.707、50%。再下一步：(|0⟩ − |1⟩) / √2，|1⟩ 橘柱 −.707、50%，向量在赤道另一側（−x）。再下一步：|ψ⟩ = |1⟩，|0⟩ 0、|1⟩ +1.000 100%，向量在南極。量測 1,000 次：「1　1000（100.0%）共 1,000 次；理論：1 100%」。
- 選沒有 Z、按起點：步驟 0 / 2，兩個淡色 H 方塊。下一步：兩根藍柱 +.707。再下一步：|ψ⟩ = |0⟩，|0⟩ +1.000 100%，向量回北極。量測 1,000 次：「0　1000（100.0%）」。
- operation.html#interference：φ = 0°，readout「P(0) = cos²(φ/2) = 1.000」「P(1) = sin²(φ/2) = 0.000」，金色標籤 P(0) = 1.00、P(1) = 0.00，右下藍、橙箭頭相反；φ = 180°，P(0) = 0.00、P(1) = 1.00，右上藍、橙相反，右下白色總和箭頭，中間 |1⟩ 節點的橙色箭頭指向左。
