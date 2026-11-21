"""Q103 課堂教材：可執行的 14 能階模擬程式（rabi_ladder.py）、transmon-3d 第 3、4 章操作步驟、預測卡、觀察紀錄表、一圈拉比振盪作圖格、解釋卡與解答。

不需要帳號。動畫路線只要瀏覽器（下載 animations/ 資料夾，開 transmon-3d.html）；程式路線需要 Python 與 numpy（pip install numpy）。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q103/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 製作代理實跑紀錄：Python 3.13、numpy 2.5.3；與 transmon-3d.html 的模擬函式（Node 22）逐位相同
# (時間 ns, P0, P1, P2, P≥3, 平均階)
RUN_TR = [(0, 1.000, 0.000, 0.000, 0.000, 0.00), (10, 0.502, 0.496, 0.002, 0.000, 0.50), (20, 0.002, 0.994, 0.004, 0.000, 1.00),
          (30, 0.499, 0.499, 0.002, 0.000, 0.50), (40, 1.000, 0.000, 0.000, 0.000, 0.00)]
RUN_LC = [(0, 1.000, 0.000, 0.000, 0.000, 0.00), (10, 0.540, 0.333, 0.103, 0.025, 0.62), (20, 0.085, 0.209, 0.258, 0.448, 2.47),
          (30, 0.004, 0.022, 0.060, 0.915, 5.55), (40, 0.000, 0.001, 0.003, 0.997, 9.52)]
for r in RUN_TR + RUN_LC:
    assert abs(sum(r[1:5]) - 1) < 0.003, r

PROGRAM = r'''"""父子科技學院 量子電腦學程 Q103：能階、共振與拉比振盪（有 JJ／沒有 JJ 的十四階模擬）

和 transmon-3d.html 第 3、4 章用同一組數字：E_J/h = 15 GHz、E_C/h = 250 MHz、
驅動頻率對準 0→1、拉比頻率 25 MHz（π 脈衝 20 ns）、只算最低 14 個能階、不含雜訊與衰減。

安裝（只要一次）：  pip install numpy
執行：              python rabi_ladder.py
"""
import numpy as np

EJ, EC, NL, RABI = 15.0, 0.25, 14, 0.025      # GHz；時間單位 ns


def transmon_levels(n_charge=25):
    """電荷基底對角化 H = 4E_C n² − E_J cos φ，回傳最低 NL 個能階（GHz）。"""
    n = np.arange(-n_charge, n_charge + 1)
    H = np.diag(4 * EC * n ** 2) - EJ / 2 * (np.eye(len(n), k=1) + np.eye(len(n), k=-1))
    return np.linalg.eigvalsh(H)[:NL]


E_TR = transmon_levels()
E_LC = np.arange(NL) * np.sqrt(8 * EJ * EC)     # 線性 LC：每一階都一樣寬


def hamiltonian(E):
    """微波對準這個電路自己的 0→1 頻率 f01；在跟著微波旋轉的座標裡：
    失諧 δn = En − E0 − n·f01，加上驅動 (Ω/2)(a + a†)。"""
    f01 = E[1] - E[0]
    det = E - E[0] - np.arange(NL) * f01
    a = np.diag(np.sqrt(np.arange(1, NL)), k=1)
    return np.diag(det) + RABI / 2 * (a + a.T)


def evolve(E, t_ns):
    w, v = np.linalg.eigh(hamiltonian(E))
    psi0 = np.zeros(NL); psi0[0] = 1
    psi = v @ (np.exp(-2j * np.pi * w * t_ns) * (v.T @ psi0))
    return np.abs(psi) ** 2


def report(name, E):
    print(f'== {name} ==')
    print('相鄰兩階的間距（GHz）：', '、'.join(f'{x:.2f}' for x in np.diff(E)[:4]))
    print(' 時間   P(0)   P(1)   P(2)  P(≥3)  平均第幾階')
    for t in (0, 10, 20, 30, 40):
        P = evolve(E, t)
        print(f'{t:3d} ns  {P[0]:.3f}  {P[1]:.3f}  {P[2]:.3f}  {P[3:].sum():.3f}  {np.arange(NL) @ P:5.2f}')
    print()


if __name__ == '__main__':
    report('有 JJ（transmon）', E_TR)
    report('沒有 JJ（線性 LC）', E_LC)
    print('有 JJ：20 ns 是 π 脈衝（停在 1），40 ns 轉一整圈回到 0。沒有 JJ：一路往上爬。')
'''


def _table(rows):
    return ('| 時間 | P(0) | P(1) | P(2) | P(≥3) | 平均第幾階 |\n|---|---|---|---|---|---|\n'
            + ''.join(f'| {t} ns | {a:.3f} | {b:.3f} | {c:.3f} | {d:.3f} | {n:.2f} |\n' for t, a, b, c, d, n in rows))


FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q103：能階、共振與拉比振盪（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。課綱形式是「超導量子電腦師生對話」第 5 課；內容依學程的《超導量子電腦師生對話教學紀錄》第 5 課整理。
今天的問題：如果晶片裡沒有約瑟夫森接面（JJ），只放普通電感，還做得出量子位元嗎？

## 兩條路線，選一條就好（也可以兩條都做）

| 路線 | 需要 | 適合 |
|---|---|---|
| A 3D 動畫（主路線） | 瀏覽器；下載學程 `animations/` 資料夾，開 `transmon-3d.html#potential`、`#control`；不需帳號 | 看得到能階梯、佔據機率和布洛赫球 |
| B 程式 | Python＋`pip install numpy`；執行 `rabi_ladder.py` | 想看完整數字表、自己改時間 |

兩條路線用同一組數字（E_J/h = 15 GHz、E_C/h = 250 MHz、拉比頻率 25 MHz、14 個能階、沒有雜訊），結果一致。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 能階是什麼、共振條件、寫下預測 | 影片第 3–4 段、列印包第 1 頁 |
| 25–65 | 第 3 章：有 JJ／沒有 JJ 送 π 脈衝、持續驅動 40 ns；第 4 章：持續驅動（拉比振盪） | `01_操作步驟.md`、列印包第 2 頁、`03_觀察紀錄.csv` |
| 65–75 | 休息 | |
| 75–105 | 孩子解釋：為什麼持續驅動 40 ns 會轉一圈回到 \\|0⟩ | 列印包第 3 頁、`rabi_ladder.py` |
| 105–115 | 孩子教爸爸：操作與原理 | 列印包第 4 頁（解釋卡） |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 自己先開 `transmon-3d.html#potential`，按「送 π 脈衝（20 ns）」，確認面板出現 P(|1⟩) ≈ 0.994。
- 想走路線 B：先執行一次 `python rabi_ladder.py`，會印出兩張表。
- 列印 `02_列印包_拉比振盪觀察紀錄.pdf`（A4，共 4 頁）。讀一遍 `04_解答.md`。

## 記錄員（爸爸）的原則

- 先預測再按按鈕：孩子沒寫預測就按，這一格先空著。
- 多問「為什麼」：數字不同時，請孩子用「梯子間距」「頻率對不對得上」來解釋。
- 常見誤解：「來回振盪」不是在 0、1 之間跳來跳去，中間每一刻都是疊加態。

## 誠實說明

- 所有數字都是 14 個能階、沒有雜訊、沒有衰減的模擬，不是實驗量測；5.21 GHz 等是學程範例參數，不是某一台真機。
- 沒有 JJ 持續驅動 40 ns 的「平均第 9.52 階」受 14 階截斷影響；不截斷時理論值約 π² ≈ 9.87。結論（一路往上爬）不變。
''',

'01_操作步驟.md': '''# 操作步驟

## 實驗一、二：第 3 章位能井（約 20 分鐘）

1. 打開 `animations/transmon-3d.html#potential`。右邊面板上方有「有 JJ（transmon）」「沒有 JJ（線性 LC）」兩個按鈕。
2. 先看梯子：有 JJ 時，梯子旁標著 5.21、4.93、4.62……GHz（越往上越密）；切到沒有 JJ，每一格都是 5.48 GHz。
3. 實驗一：選「有 JJ」，寫預測，按「送 π 脈衝（20 ns）」。看青色長條（佔據機率）搬到哪一階，記下面板的 P(|0⟩)・P(|1⟩)・P(|2⟩)、P(≥|3⟩)、平均能階。
4. 切到「沒有 JJ」，再按一次「送 π 脈衝（20 ns）」，同樣記下來。
5. 實驗二：兩種電路各按一次「持續驅動 40 ns」，記下結果。動畫 1 秒相當於 8 ns，20 ns 的脈衝跑約 2.5 秒、40 ns 跑約 5 秒。
6. 每次重新實驗前可以按「重設 |0⟩」。

## 實驗三：第 4 章操控（約 15 分鐘）

1. 點下方章節列的「04 操控」（或開 `transmon-3d.html#control`）。
2. 選「有 JJ」，按「持續驅動（Rabi 振盪）」：箭頭在布洛赫球上連續旋轉，面板的 P(|1⟩) 曲線上下起伏。觀察「類型」欄：大部分時間是「疊加態」。再按一次（按鈕變成「停止驅動」）停下。
3. 按「X 軸 π/2」和「Y 軸 π/2」（每次先按「重設 |0⟩」），比較兩個「此刻的狀態」：都是 50/50，但係數不同。
4. 切到「沒有 JJ」，按「持續驅動（Rabi 振盪）」：40 ns 後自動停下，箭頭縮到球心附近，「類型」變成紅字「已漏出 0/1：不是量子位元的狀態」。

## 路線 B：程式（約 10 分鐘）

1. `pip install numpy`，再執行 `python rabi_ladder.py`。
2. 對照兩張表的 20 ns、40 ns 兩列，和動畫面板的數字比較。
3. 改造：把 `for t in (0, 10, 20, 30, 40)` 改成每 5 ns 一格，畫出 P(1) 隨時間的曲線（列印包第 3 頁）。
''',

'rabi_ladder.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n## rabi_ladder.py 實跑（Python 3.13、numpy 2.5.3；和動畫面板相同）\n\n### 有 JJ（transmon），相鄰間距 5.21、4.93、4.62、4.25 GHz\n\n'
  + _table(RUN_TR) + '\n### 沒有 JJ（線性 LC），相鄰間距都是 5.48 GHz\n\n' + _table(RUN_LC)
  + '\n## 為什麼 40 ns 轉一圈回到 |0⟩？\n\n'
  '拉比頻率 25 MHz 表示每秒轉 2,500 萬圈，一圈 = 1 ÷ 25,000,000 秒 = 40 ns。20 ns 是半圈（π，停在 |1⟩），40 ns 是一圈（2π，回到 |0⟩，只差一個整體相位，量不出來）。'
  '有 JJ 時 1→2 需要 4.93 GHz，和 5.21 GHz 的微波差 283 MHz，所以狀態幾乎只在 |0⟩、|1⟩ 兩階之間轉。\n\n'
  '## 10 ns 和 30 ns\n\n兩個都約 50/50，但不是同一個狀態：10 ns（π/2）是 (|0⟩ − i|1⟩)/√2，30 ns（3π/2）是 (|0⟩ + i|1⟩)/√2，在布洛赫球赤道上指向相反方向。\n\n'
  '## 常見問題\n\n'
  '- 沒有 JJ 為什麼停不住？等距梯子每一對都是 5.48 GHz，對準 0→1 的微波對 1→2、2→3……也共振，狀態被一路往上推（相干態），像古典的電流振盪越推越大。\n'
  '- 沒有 JJ 為什麼連讀取都不行？色散偏移 χ = (g²/Δ)·α/(Δ+α)，α = 0 時 χ = 0，共振腔頻率不隨狀態改變（下一課詳談）。\n'
  '- 「|2⟩ 是 JJ 介面的第二層」對嗎？不對。|2⟩ 是整個電路振盪存了兩份能量，不是某個實體位置。\n'
  '- 為什麼 π 脈衝不能無限縮短？脈衝越短越強、頻譜越寬，越容易碰到 4.93 GHz，漏到 |2⟩；實務上 20–50 ns 並用 DRAG 整形。估計：Ω²/(Ω²+Δ²) = 25²/(25²+283²) ≈ 0.8%，模擬值 0.4%。\n'
  '- 「只能被吸收」精確嗎？精確說法：吸收能量的是一對相鄰能階之間的躍遷，而且是「幾乎只能」。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路、伺服器或帳號（3D 需要 WebGL）。

## `animations/transmon-3d.html#potential`（第 3 章：cos 位能井）

- 「有 JJ（transmon）」「沒有 JJ（線性 LC）」：切換位能形狀與能階梯（銅色 cos 井／灰色拋物線）。
- 「送 π 脈衝（20 ns）」「持續驅動 40 ns」「重設 |0⟩」：青色長條是各能階的佔據機率（最上面一條合併 |5⟩ 以上），小球擺幅代表平均能量。
- 面板：「此刻的狀態」「P(|0⟩)・P(|1⟩)・P(|2⟩)」「P(≥|3⟩)」「平均能階 ⟨n⟩」。

## `animations/transmon-3d.html#control`（第 4 章：用微波轉動布洛赫球）

- 「X 軸 π」「X 軸 π/2」「Y 軸 π/2」「持續驅動（Rabi 振盪）」「重設 |0⟩」。
- 面板：「此刻的狀態」「類型」「P(|1⟩)」與 P(|1⟩) 隨時間的曲線；左邊的小梯子標出「5.21 GHz 共振」「4.93 GHz 不共振」，沒有 JJ 時是「5.48 GHz 也共振！」。

## `animations/lc-vs-jj.html#s4`（圖解第 4 步：能不能只停在 |0⟩ 和 |1⟩？）

- 每條直線是一個躍遷頻率，陰影帶是驅動微波；拖上一步的 E_J / E_C 滑桿，看 transmon 的躍遷怎麼錯開。

## 操作

滑鼠拖曳旋轉、滾輪縮放；← → 切換章節。
''',
}

SHEET_HEADER = ['實驗', '電路（有 JJ／沒有 JJ）', '按了什麼', '預測', 'P(0)', 'P(1)', 'P(2)', 'P(≥3)', '平均能階', '和預測一樣嗎', '為什麼']
SHEET_ROWS = [['實驗一', '有 JJ', '送 π 脈衝（20 ns）'], ['實驗一', '沒有 JJ', '送 π 脈衝（20 ns）'],
              ['實驗二', '有 JJ', '持續驅動 40 ns'], ['實驗二', '沒有 JJ', '持續驅動 40 ns'],
              ['實驗三', '有 JJ', '持續驅動（Rabi 振盪）'], ['實驗三', '沒有 JJ', '持續驅動（Rabi 振盪）']]

EXTRA_CSS = '''table.rec td{height:11mm}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.ladder{display:grid;grid-template-columns:1fr 1fr;gap:8mm;margin-top:3mm}.ladder .box{min-height:52mm}
.rung{border-top:1.4pt solid #0b2540;margin:0 4mm 0 10mm;position:relative;font-size:10pt}
.rgrid{height:62mm;border-left:1.2pt solid #0b2540;border-bottom:1.2pt solid #0b2540;margin:3mm 0 0 12mm;position:relative;
background-image:linear-gradient(#cfdde8 .6pt,transparent .6pt),linear-gradient(90deg,#cfdde8 .6pt,transparent .6pt);background-size:100% 15.5mm,12.5% 100%}
.ylab{position:absolute;left:-11mm;font-size:9pt;color:#4a6a88}.xlab{display:flex;justify-content:space-between;margin:1mm 0 0 10mm;font-size:9.5pt;color:#4a6a88}'''


def _rungs(gaps):
    """由上往下畫能階：每條橫線是一階，兩線之間標出那一對的躍遷頻率。"""
    out, h, top = '', 60, len(gaps)
    for i, g in enumerate(gaps):
        k = top - i
        out += (f'<div class="rung" style="height:{h * g / 5.48:.1f}px"><span style="position:absolute;left:-6mm;top:-7px">|{k}⟩</span>'
                f'<span style="position:absolute;right:0;top:40%">{k - 1}→{k}：{g:.2f} GHz</span></div>')
    return out + '<div class="rung" style="height:6px"><span style="position:absolute;left:-6mm;top:-7px">|0⟩</span></div>'


def html():
    pages = [
        '<h2>預測卡：先猜再按</h2><p class="lead">科學實驗的規矩：先寫預測，再按按鈕。預測錯了也算數，寫下錯在哪裡。</p>'
        '<div class="ladder"><div class="box"><h3>有 JJ（transmon）</h3>' + _rungs([4.62, 4.93, 5.21]) + '</div>'
        '<div class="box"><h3>沒有 JJ（線性 LC）</h3>' + _rungs([5.48, 5.48, 5.48]) + '</div></div>'
        '<div class="box" style="margin-top:5mm"><p>有 JJ 時用 5.21 GHz（對準 0→1）的微波去推：哪一對對得上？圈起來。　0→1　1→2　2→3（沒有 JJ 時微波對準 5.48 GHz）</p>'
        '<p>預測一：送 π 脈衝（20 ns）後，有 JJ 停在第＿＿階；沒有 JJ 停在第＿＿階。</p>'
        '<p>預測二：持續驅動 40 ns 後，有 JJ 在第＿＿階；沒有 JJ 在第＿＿階。</p><p>我為什麼這樣猜：</p><div class="line"></div><div class="line"></div></div>',
        '<h2>觀察紀錄表</h2><p class="lead">transmon-3d 第 3 章（位能井）與第 4 章（操控）。實驗員唸面板數字，記錄員填表。</p>'
        '<table class="rec"><tr><th>實驗</th><th>電路</th><th>按了什麼</th><th>P(0)</th><th>P(1)</th><th>P(2)</th><th>P(≥3)</th><th>平均能階</th></tr>'
        + ''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td><td></td><td></td><td></td><td></td><td></td></tr>' for a, b, c in SHEET_ROWS[:4]) + '</table>'
        '<div class="box" style="margin-top:4mm"><h3>實驗三：第 4 章「持續驅動（Rabi 振盪）」</h3>'
        '<p>有 JJ：「類型」欄大部分時間寫的是＿＿＿＿＿＿；什麼時候會變成「純 |0⟩」或「純 |1⟩」？</p><div class="line"></div>'
        '<p>沒有 JJ：40 ns 後箭頭變得＿＿＿＿，「類型」欄寫的是＿＿＿＿＿＿＿＿。</p><div class="line"></div></div>'
        '<p class="note">面板數字取到小數點後三位；動畫 1 秒約等於 8 ns（第 3 章）。</p>',
        '<h2>換你解釋：40 ns 為什麼轉一圈</h2><p class="lead">拉比頻率 25 MHz：每秒轉＿＿＿＿＿＿圈，一圈要＿＿＿ ns。</p>'
        '<h3>把 P(1) 隨時間畫出來（有 JJ；程式改成每 5 ns 一格，或照解答的 10 ns 表）</h3>'
        '<div class="rgrid"><span class="ylab" style="top:-2mm">1</span><span class="ylab" style="top:29mm">0.5</span><span class="ylab" style="bottom:-2mm">0</span></div>'
        '<div class="xlab"><span>0</span><span>5</span><span>10</span><span>15</span><span>20</span><span>25</span><span>30</span><span>35</span><span>40 ns</span></div>'
        '<table class="rec" style="margin-top:4mm"><tr><th>時間</th><th>0 ns</th><th>10 ns</th><th>20 ns</th><th>30 ns</th><th>40 ns</th></tr>'
        '<tr><td>轉了幾圈</td><td>0</td><td></td><td></td><td></td><td></td></tr><tr><td>狀態（0、1 或疊加）</td><td>|0⟩</td><td></td><td></td><td></td><td></td></tr></table>'
        '<p class="note">再挑戰：10 ns 和 30 ns 量起來都是一半一半，它們是同一個狀態嗎？＿＿＿＿＿＿＿＿＿＿</p>',
        '<h2>解釋卡：拉比振盪觀察紀錄</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 微波什麼時候才會被吸收？</p><div class="line"></div><p>2. 沒有 JJ 時，π 脈衝和持續驅動各發生什麼事？</p><div class="line"></div><div class="line"></div>'
        '<p>3. 一個容易錯的地方：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出共振條件：相鄰兩階的頻率對上</li><li>說出沒有 JJ 的後果：一路漏上去，定義不出 0、1</li>'
        '<li>解釋為什麼 40 ns 轉一圈回到 |0⟩</li><li>指出一個誤解：振盪中每一刻都是疊加態，不是跳來跳去</li>'
        '<li>說出一個限制：數字來自沒有雜訊的模擬</li><li>替觀察紀錄取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q103 能階、共振與拉比振盪 列印包', '父子科技學院 量子電腦學程 Q103｜能階、共振與拉比振盪', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q103-rabi-oscillation', folder='Q103_拉比振盪觀察紀錄', files=FILES,
        sheet=('03_觀察紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_拉比振盪觀察紀錄.pdf', pack_pages=4,
        pack_needles=('預測卡', '觀察紀錄表', '換你解釋', '解釋卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q103', episode_dir='specials/q103-rabi-oscillation',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'optional（動畫路線免安裝；程式路線 pip install numpy）',
               'program': 'rabi_ladder.py', 'testedWith': 'Python 3.13, numpy 2.5.3',
               'recordedRun': {'transmon': RUN_TR, 'linearLC': RUN_LC}, 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q103/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')
