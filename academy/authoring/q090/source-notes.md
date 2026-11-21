# Q090 來源筆記（逐字引文）

查核日：2026-11-18。學程 repo 沒有 BB84 簡報或場景（課綱「需新增：◆ 新簡報：BB84；★ BB84 場景」）；以下維基百科原始 wikitext 由製作代理讀取；動畫程式由製作代理讀取。

## Wikipedia: BB84（https://en.wikipedia.org/wiki/BB84）

- 「The BB84 protocol, invented in 1984 by Charles Bennett and Gilles Brassard … is a prepare-and-measure quantum key distribution (QKD) protocol」
- 「The BB84 QKD scheme is the first quantum cryptography protocol」
- 「provably secure assuming a perfect implementation, relying on two conditions: (1) … information gain is only possible at the expense of disturbing the signal if the two states … are not orthogonal (see no-cloning theorem); and (2) the existence of an authenticated public classical channel」
- 「The proof of BB84 QKD scheme depends on a perfect implementation. Side channel attacks exist」
- 「Her measurements, however, risk disturbing a particular qubit with probability 1/2 if she guesses the wrong basis.」
- 「Both Alice and Bob now discard the bits in a and a′ where b and b′ do not match.」「If this check passes, Alice and Bob proceed to use information reconciliation and privacy amplification … Otherwise, they cancel and start over.」
- （頁首另寫 2025 ACM A.M. Turing Award；本集未使用）

## Wikipedia: Quantum key distribution（https://en.wikipedia.org/wiki/Quantum_key_distribution）

- 「the process of measuring a quantum system in general disturbs the system. This means, a third party attempting to eavesdrop on the key must in some way measure it, thus introducing detectable anomalies」
- 「Quantum key distribution is used to produce and distribute only a key, not to transmit any message data.」「The algorithm most commonly associated with QKD is the one-time pad」
- 「This protocol, known as BB84 after its inventors and year of publication, was originally described using photon polarization states」
- 「a 0 is encoded in the rectilinear basis (+) as a vertical polarization state, and a 1 is encoded in the diagonal basis (x) as a 135° state」（基底表：＋ 0 = ↑、1 = →；× 0 = ↗、1 = ↘）
- 「They both discard photon measurements (bits) where Bob used a different basis, which is half on average」
- 「Other environmental conditions can cause errors in a similar fashion. If more than p bits differ they abort the key and try again」
- Intercept and resend：「The probability an intercepted photon generates an error in the key string is then 50% × 50% = 25%.」「P_d = 1 − (3/4)^n」「to detect an eavesdropper with probability P_d = 0.999999999 Alice and Bob need to compare n = 72 key bits」
- 「Quantum key distribution is vulnerable to a man-in-the-middle attack when used without authentication」
- 「As it is impossible to distinguish between these two types of errors, guaranteed security requires the assumption that all errors are due to eavesdropping.」
- NSA：「The actual security provided by a QKD system is not the theoretical unconditional security from the laws of physics … but rather the more limited security that can be achieved by hardware and engineering designs.」

## animations/js/operation/01_qubit.js

- 「測量只會得到 0 或 1：得到 0 的機率是 cos²(θ/2)。測量後狀態塌縮到北極或南極」
- 預設按鈕 `[['|0⟩', 0, 0], ['|1⟩', 180, 0], ['|+⟩', 90, 0], ['|+i⟩', 90, 90], ['θ=60°', 60, 30]]`；`ui.button('一次跑 1000 shots', …)`、`ui.button('測量一次', …)`
- 塌縮動畫：`k = Math.min(1, collapse.t / 0.25)`、`if (collapse.t < 1.4)`、閃光 `0.35 * (1 - collapse.t / 0.4)`

## animations/js/operation/07_readout.js

- 「硬體只會在 Z 基底量測（|0⟩ 或 |1⟩）。想量 X 或 Y，就先加一個旋轉閘：量 X 前加 H」
- `ui.radio([['Z', '量 Z（直接量）'], ['X', '量 X（先 H）'], ['Y', '量 Y（先 S†H）']], …)`；`ui.slider('準備狀態 θ', 0, 180, …)`；`ui.slider('兩團雲的間距（色散位移/放大器）', 0.3, 1.6, …)`
- `blochVec = [sinθ·cos0.4, sinθ·sin0.4, cosθ]`；`pTrue1 = (1 − c)/2`

## 重算紀錄（製作代理）

| 抽查位數 n | 1 − (3/4)^n |
|---|---|
| 1 | 25% |
| 10 | 94.4% |
| 20 | 99.7% |
| 72 | 0.999999999 |

讀取場景：間距 1.6 時讀錯約 0.18%；θ = 90 量 X 的 P(1) = (1 − cos0.4)/2 ≈ 3.9%。
