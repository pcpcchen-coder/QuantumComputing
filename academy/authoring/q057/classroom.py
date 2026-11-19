"""Q057 課堂教材：可執行的筆記本 bell_ghz_release.ipynb（與同內容的 .py）、Release 檢查清單、直方圖紀錄、五顆改造表、
更新紀錄與說明卡、解答。

只用本機模擬器，不需要帳號；需要在自己的電腦安裝開源套件（pip install qiskit qiskit-aer；畫圖另需 matplotlib，可省略）。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q057/classroom.py
"""
from pathlib import Path
import json
import os
import re
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 製作代理實跑紀錄：Python 3.13.18、qiskit 2.6.2、qiskit-aer 0.18.4、shots=1024、seed_simulator=2026
# 雜訊模型：h、cx 去極化 1%，每顆讀取 3% 讀反
TESTED = 'Python 3.13.18, qiskit 2.6.2, qiskit-aer 0.18.4'
RUNS = {  # N: (理想, 有雜訊)
    2: ({'00': 516, '11': 508}, {'00': 478, '01': 49, '10': 32, '11': 465}),
    3: ({'000': 514, '111': 510}, {'000': 471, '001': 20, '010': 11, '011': 19, '100': 23, '101': 15, '110': 21, '111': 444}),
    4: ({'0000': 499, '1111': 525}, None),
    5: ({'00000': 476, '11111': 548}, None),
}
NOISY_SUMMARY = {2: (81, 4, 4), 3: (109, 8, 8), 4: (158, 15, 16), 5: (173, 21, 32)}  # N: (錯誤次數, 出現幾種, 共幾種)
SEEDS_BELL = {1: 93, 2: 52, 3: 75, 4: 79, 5: 56}
for n, (ideal, noisy) in RUNS.items():
    assert sum(ideal.values()) == 1024 and set(ideal) == {'0' * n, '1' * n}
    if noisy:
        assert sum(noisy.values()) == 1024
        assert 1024 - noisy['0' * n] - noisy['1' * n] == NOISY_SUMMARY[n][0] and len(noisy) == NOISY_SUMMARY[n][1]

PROGRAM = r'''"""父子科技學院 量子電腦學程 Q057：程式實作——貝爾態與 GHZ 態（本機模擬器，不需要帳號）

安裝（只要一次）：  pip install qiskit qiskit-aer        （想畫圖再加 matplotlib）
執行：              python bell_ghz_release.py
同一份程式也做成筆記本：bell_ghz_release.ipynb（Jupyter 或 VS Code 開啟，按「全部重新執行」）
"""
# ── 第 0 格：記錄版本（Release 檢查清單第 2 項）──────────────────────────
import sys
import qiskit
import qiskit_aer
print('Python', sys.version.split()[0], '| qiskit', qiskit.__version__, '| qiskit-aer', qiskit_aer.__version__)
# 影片與解答用的版本：Python 3.13.18、qiskit 2.6.2、qiskit-aer 0.18.4

# ── 第 1 格：建線路 ───────────────────────────────────────────────────────
from qiskit import QuantumCircuit, transpile


def ghz(n):
    """n 顆位元的 GHZ 態；n = 2 就是貝爾態。"""
    qc = QuantumCircuit(n, n)
    qc.h(0)                       # 哈達瑪閘：q0 進入疊加
    for i in range(n - 1):
        qc.cx(i, i + 1)           # 受控反閘一路串下去：q0→q1、q1→q2…
    qc.measure(range(n), range(n))
    return qc


print(ghz(3).draw())

# ── 第 2 格：兩台模擬器，一台理想、一台加雜訊模型 ─────────────────────────
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error, ReadoutError

P_GATE, P_READ = 0.01, 0.03       # 每個閘 1% 被打亂、每次讀取 3% 讀反（教學用的假設值）
noise = NoiseModel()
noise.add_all_qubit_quantum_error(depolarizing_error(P_GATE, 1), ['h'])
noise.add_all_qubit_quantum_error(depolarizing_error(P_GATE, 2), ['cx'])
noise.add_all_qubit_readout_error(ReadoutError([[1 - P_READ, P_READ], [P_READ, 1 - P_READ]]))
ideal_sim = AerSimulator()
noisy_sim = AerSimulator(noise_model=noise)

SHOTS, SEED = 1024, 2026          # 固定種子：每次重跑都得到同一組數字（Release 檢查清單第 3 項）


def run(sim, qc, seed=SEED):
    counts = sim.run(transpile(qc, sim), shots=SHOTS, seed_simulator=seed).result().get_counts()
    return dict(sorted(counts.items()))


def wrong(counts, n):
    """全 0、全 1 以外的結果一共幾次。"""
    return SHOTS - counts.get('0' * n, 0) - counts.get('1' * n, 0)


# ── 第 3 格：跑、比、自動檢查 ─────────────────────────────────────────────
N = 2                             # 改造區：改成 3、4、5 試試看
qc = ghz(N)
ideal = run(ideal_sim, qc)
noisy = run(noisy_sim, qc)
print('理想  ', ideal)
print('有雜訊', noisy, '→ 錯誤結果', wrong(noisy, N), '次，出現', len(noisy), '種')

# 自動檢查（Release 檢查清單第 4 項）：沒過就會停下來
assert sum(ideal.values()) == SHOTS and sum(noisy.values()) == SHOTS
assert set(ideal) <= {'0' * N, '1' * N}, '理想模擬只該出現全 0 和全 1'
assert run(ideal_sim, qc) == ideal, '同一個種子重跑，數字應該一模一樣'
print('自動檢查全部通過')

# ── 第 4 格（選用）：畫成兩張並排的直方圖 ─────────────────────────────────
try:
    import matplotlib.pyplot as plt
    keys = [format(i, f'0{N}b') for i in range(2 ** N)]
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.5), sharey=True)
    for a, (title, c) in zip(ax, [('ideal', ideal), ('noisy', noisy)]):
        a.bar(keys, [c.get(k, 0) for k in keys])
        a.set_title(f'GHZ n={N} {title}')
        a.tick_params(axis='x', rotation=90 if N > 3 else 0)
    plt.tight_layout()
    plt.savefig(f'ghz{N}_histograms.png')
    print('直方圖存成', f'ghz{N}_histograms.png')
except ImportError:
    print('沒有安裝 matplotlib：跳過畫圖，用上面的數字畫在列印包上就好')

# 影片中的結果（seed=2026）：
#   N=2 理想 {'00': 516, '11': 508}；有雜訊 {'00': 478, '01': 49, '10': 32, '11': 465}，錯誤 81 次
#   N=3 有雜訊錯誤 109 次（8 種結果都出現）；N=5 有雜訊錯誤 173 次（32 種裡出現 21 種）
'''


def notebook(program):
    """把程式依「# ── 第 k 格」切成筆記本的程式格，前面各加一格說明。"""
    head, *parts = re.split(r'\n(?=# ── 第 )', program)
    title = ('# Q057 程式實作：貝爾態與 GHZ 態（Release 任務）\n\n'
             '父子科技學院 量子電腦學程。只用本機模擬器，不需要帳號。\n\n'
             '**Release 檢查清單**：① 從頭「全部重新執行」不出錯 ② 第 0 格印出版本號 ③ 固定種子，數字能重現 '
             '④ 自動檢查全部通過 ⑤ 檔名寫上版本（例如 `bell_ghz_v1.0.ipynb`）\n\n'
             '| 版本 | 日期 | 改了什麼 |\n|---|---|---|\n| v1.0 | | Bell 理想 vs 雜訊 |\n| v1.1 | | GHZ 擴大到 5 顆 |')
    cells = [{'cell_type': 'markdown', 'metadata': {}, 'source': title.splitlines(True)}]
    for p in parts:
        first, _, body = p.partition('\n')
        note = first.strip('# ─').strip()
        cells.append({'cell_type': 'markdown', 'metadata': {}, 'source': [f'## {note}']})
        cells.append({'cell_type': 'code', 'metadata': {}, 'execution_count': None, 'outputs': [],
                      'source': body.strip('\n').splitlines(True)})
    nb = {'cells': cells, 'metadata': {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
                                       'language_info': {'name': 'python'}}, 'nbformat': 4, 'nbformat_minor': 5}
    return json.dumps(nb, ensure_ascii=False, indent=1) + '\n'


NOTEBOOK = notebook(PROGRAM)

CHECKLIST = ['從頭「全部重新執行」不出錯', '第 0 格印出 Python、qiskit、qiskit-aer 版本號', '固定種子 2026，數字和上一次一樣',
             '自動檢查（assert）全部通過', '檔名寫上版本，例如 bell_ghz_v1.0.ipynb']

FILES = {
'00_爸爸先讀.md': f'''# 父子科技學院 量子電腦學程 Q057：程式實作——貝爾態與 GHZ 態（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶出今天的任務：在自己的電腦上用開源量子程式套件（Qiskit）與本機模擬器（Aer），
寫出貝爾態和 GHZ 態，加上雜訊模型比較直方圖，最後像軟體一樣通過檢查清單「發布」v1.0。

## 課前準備（約 20 分鐘，不需要帳號）

1. 安裝 Python 3.10 以上，接著在終端機輸入：`pip install qiskit qiskit-aer matplotlib jupyter`（matplotlib、jupyter 可省略）。
2. 先自己跑一次：`python bell_ghz_release.py`。應該看到版本號、三顆的線路圖、`理想 {{'00': 516, '11': 508}}` 和「自動檢查全部通過」。
   - 本程式在 {TESTED} 測試過。你的版本不同時，理想結果的數字可能不一樣，但仍然只會有 00 和 11；改版若讓程式跑不動，先看錯誤訊息最後一行。
3. 想用筆記本：`jupyter notebook bell_ghz_release.ipynb`（或用 VS Code 開啟），選「全部重新執行」。
4. 列印 `02_列印包_Release任務.pdf`（A4，共 4 頁）；準備一個印章當「v1.0 發布章」。讀一遍 `04_解答.md`。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 筆記本是什麼、GHZ 線路四格、理想 vs 雜訊 | 影片第 3–6 段 |
| 25–65 | 跑 Bell（N = 2）理想與有雜訊，畫兩張直方圖，照檢查清單發布 v1.0 | 筆記本、`01_操作步驟.md`、列印包第 1–2 頁 |
| 65–75 | 休息 | |
| 75–105 | 孩子改 N = 3、4、5，記錄錯誤次數，更新成 v1.1 | 列印包第 3 頁、`03_實驗紀錄.csv` |
| 105–115 | 孩子教爸爸：線路怎麼接、為什麼理想只有全 0 全 1、為什麼要記版本號 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 品管員（爸爸）的原則

- 檢查清單五項都打勾才蓋章；有一項沒過就退回去修，不替孩子修。
- 有雜訊的數字每換一個種子就會變（Bell 換 5 個種子，錯誤次數 52～93 次），不要求和影片一模一樣；固定種子 2026 時才會一樣。
- 程式出錯時，一起讀錯誤訊息最後一行，找出是哪一格、哪一行。

## 誠實說明

- 雜訊模型（每閘 1%、讀取 3%）是教學用的假設值，不代表任何一台真機。
- 只用本機模擬器；不連雲端、不需要帳號。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：Bell 態 v1.0（約 40 分鐘）

1. 開啟 `bell_ghz_release.ipynb`，選「全部重新執行」（或執行 `python bell_ghz_release.py`）。
2. 第 0 格：把印出來的三個版本號抄到列印包第 1 頁。
3. 第 1 格：看三顆的線路圖，對照影片的四格：三顆都是 0 → q0 做 H → CNOT q0→q1 → CNOT q1→q2。
4. 第 3 格（N = 2）：先在列印包第 2 頁寫預測，再看「理想」和「有雜訊」兩行數字，畫兩張直方圖。
5. 圈出有雜訊那張圖裡「不該出現」的柱子，算一共幾次。
6. 品管員照列印包第 1 頁的檢查清單核對五項；全過就把檔名改成 `bell_ghz_v1.0.ipynb`，蓋章。

## 下半場：GHZ 擴大到五顆 v1.1（約 30 分鐘）

1. 把第 3 格的 `N = 2` 改成 3，再跑；接著 4、5。每次都記在列印包第 3 頁和 `03_實驗紀錄.csv`。
2. 觀察：位元越多，錯誤次數怎麼變？出現的結果有幾種？
3. 想看看換種子會怎樣：把第 2 格的 `SEED = 2026` 改成別的數字（記得改回來才能和影片比對）。
4. 在第一格的更新紀錄寫上 v1.1 改了什麼，另存成 `bell_ghz_v1.1.ipynb`，再請品管員核對一次。

## 沒有電腦的備案

打開 `animations/basic-circuits.html#ghz`（量測 1,000 次、可切換 3 顆／4 顆、底下有程式碼）與 `animations/operation.html#circuit`
（選「GHZ 態」、按「單步 ▶」四次、打開「加入雜訊」）。動畫的雜訊算法和筆記本不同，數字不會一樣。
''',

'bell_ghz_release.py': PROGRAM,
'bell_ghz_release.ipynb': NOTEBOOK,

'04_解答.md': '# 解答（爸爸用）\n\n'
  f'## 影片中的實跑（{TESTED}、shots=1024、seed_simulator=2026）\n\n'
  '| N | 理想 | 有雜訊：全 0／全 1 | 錯誤結果次數 | 出現幾種（共幾種） |\n|---|---|---|---|---|\n'
  + ''.join(f'| {n} | ' + '、'.join(f'{k}：{v}' for k, v in RUNS[n][0].items()) + ' | '
            + (f"{RUNS[n][1]['0' * n]}／{RUNS[n][1]['1' * n]}" if RUNS[n][1] else '—') + f' | {NOISY_SUMMARY[n][0]} | {NOISY_SUMMARY[n][1]}（{NOISY_SUMMARY[n][2]}） |\n'
            for n in RUNS)
  + "\nBell 有雜訊的完整結果：{'00': 478, '01': 49, '10': 32, '11': 465}。\n\n"
  '換種子（Bell 有雜訊的錯誤次數）：' + '、'.join(f'種子 {s}：{v}' for s, v in SEEDS_BELL.items()) + '。\n\n'
  '用 20 萬次模擬估計的平均錯誤率：Bell 約 6.3%、三顆約 9.9%、五顆約 16.5%；其中只算讀取錯誤（每顆 3%）就有 5.8%、8.7%、14.1%。\n\n'
  '## 常見問題\n\n'
  '- 為什麼位元越多錯越多？每多一顆就多一個 CNOT、多讀一顆，每一步都可能出錯。\n'
  '- 為什麼理想結果每次都一樣？固定了種子；拿掉 `seed_simulator` 每次都會不同，但仍只有全 0 和全 1。\n'
  '- 位元字串怎麼讀？最右邊是 q0（第一顆）。\n'
  '- 版本不同跑不動？套件改版可能改名或搬家；先對照第 0 格的版本號，再查官方文件。這就是要記版本號的原因。\n',

'05_線路動畫導覽.md': '''# 線路動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路、伺服器或帳號。

## `animations/basic-circuits.html#ghz`（八個基礎量子電路：範例 4 GHZ 態）

- 上方「位元數」：3 顆、4 顆。
- 「下一步 ▶」按三次（4 顆按四次）：看振幅柱子最後只剩全 0、全 1 兩根。
- 「量測 1,000 次」：右邊只列出全 0、全 1 兩種結果（理想模擬，沒有雜訊）。
- 最下面「Qiskit 程式碼」：展開後是同一個線路的程式，會隨位元數改變。

## `animations/operation.html#circuit`（場景 6：量子線路）

- 範例選「GHZ 態（3 位元糾纏）」，按「單步 ▶」四次，最後一步跑 1000 次並在右下畫直方圖（青線是理想機率）。
- 「加入雜訊（每閘 1%、讀取 3%）」：打開後中間六個位置冒出矮柱子。算法和筆記本的雜訊模型不同，只看趨勢。

## 操作

`H` 隱藏面板；滑鼠拖曳旋轉、滾輪縮放（operation.html）；左右方向鍵換步（basic-circuits.html）。
''',
}

SHEET_HEADER = ['版本', 'N（位元數）', '雜訊', '種子', '全 0 次數', '全 1 次數', '錯誤結果次數', '出現幾種結果', '我的觀察']
SHEET_ROWS = ([['v1.0', '2', '無', '2026'], ['v1.0', '2', '有', '2026']]
              + [['v1.1', str(n), z, '2026'] for n in (3, 4, 5) for z in ('無', '有')]
              + [['v1.1', '2', '有', '（自己選）']])

EXTRA_CSS = '''.hgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:5mm;height:60mm;border-left:1.2pt solid #0b2540;border-bottom:1.2pt solid #0b2540;
margin:2mm 0 0 12mm;position:relative;background-image:linear-gradient(#cfdde8 .6pt,transparent .6pt);background-size:100% 10mm}
.ylab{position:absolute;left:-12mm;font-size:9pt;color:#4a6a88}.xlab{display:grid;grid-template-columns:repeat(4,1fr);gap:5mm;margin-left:12mm;
font-size:11pt;text-align:center}table.rec td{height:9mm}.chk li{margin:2.2mm 0;font-size:12.5pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.stamp{border:1.6pt dashed #0b2540;border-radius:50%;width:38mm;height:38mm;display:flex;align-items:center;justify-content:center;text-align:center;
font-size:12pt;color:#4a6a88;margin:3mm auto 0}.two{display:grid;grid-template-columns:1fr 1fr;gap:6mm}
pre.code{font-size:9.5pt;background:#f2f6fa;border:1pt solid #cfdde8;padding:3mm;margin:2mm 0;white-space:pre-wrap}'''


def hist(title):
    return (f'<div><h3>{title}</h3><div class="hgrid"><span class="ylab" style="top:-2mm">600</span><span class="ylab" style="top:28mm">300</span>'
            '<span class="ylab" style="bottom:-2mm">0</span></div><div class="xlab"><span>00</span><span>01</span><span>10</span><span>11</span></div></div>')


def html():
    chk = ''.join(f'<li>{t}</li>' for t in CHECKLIST)
    pages = [
        '<h2>Release 檢查清單：Bell 筆記本 v1.0</h2><p class="lead">發布工程師（孩子）寫程式、跑結果；品管員（爸爸）一項一項核對，五項全過才蓋章。</p>'
        '<div class="box"><h3>版本資訊（抄自第 0 格）</h3><p>Python：＿＿＿＿＿＿　qiskit：＿＿＿＿＿＿　qiskit-aer：＿＿＿＿＿＿</p>'
        '<p>種子 SEED：＿＿＿＿　重複次數 SHOTS：＿＿＿＿　日期：＿＿＿＿＿＿</p></div>'
        f'<div class="box" style="margin-top:4mm"><h3>發布檢查清單</h3><ul class="chk">{chk}</ul></div>'
        '<div class="two"><div class="box" style="margin-top:4mm"><h3>更新紀錄</h3><p>v1.0：＿＿＿＿＿＿＿＿＿＿＿＿</p><p>v1.1：＿＿＿＿＿＿＿＿＿＿＿＿</p></div>'
        '<div><div class="stamp">v1.0<br>發布章</div></div></div>',
        '<h2>理想 vs 有雜訊：Bell 態（N = 2）</h2><p class="lead">先預測，再跑；把兩行數字畫成兩張直方圖，圈出不該出現的柱子。</p>'
        '<p>我的預測：理想會出現＿＿＿＿＿＿；有雜訊會多出＿＿＿＿＿＿</p>'
        '<table class="rec"><tr><th></th><th>00</th><th>01</th><th>10</th><th>11</th><th>錯誤結果共幾次</th></tr>'
        '<tr><td>理想</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>有雜訊</td><td></td><td></td><td></td><td></td><td></td></tr></table>'
        f'<div class="two" style="margin-top:4mm">{hist("理想（每格 100 次）")}{hist("有雜訊（每格 100 次）")}</div>'
        '<p class="note" style="margin-top:4mm">位元字串的最右邊是第一顆（q0）。有雜訊那張，哪兩根變矮了？為什麼？＿＿＿＿＿＿＿＿＿＿＿＿</p>',
        '<h2>換你改造：GHZ 擴大到五顆（v1.1）</h2><p class="lead">把第 3 格的 N 改成 3、4、5。每次都跑理想和有雜訊，記下錯誤結果的次數。</p>'
        '<table class="rec"><tr><th>N</th><th>CNOT 個數</th><th>理想：全 0／全 1</th><th>有雜訊：錯誤結果次數</th><th>出現幾種結果（共幾種）</th></tr>'
        + ''.join(f'<tr><td>{n}</td><td></td><td></td><td></td><td>（共 {2 ** n} 種）</td></tr>' for n in (2, 3, 4, 5)) + '</table>'
        '<pre class="code">def ghz(n):\n    qc = QuantumCircuit(n, n)\n    qc.h(0)\n    for i in range(n - 1):\n        qc.cx(i, i + 1)\n'
        '    qc.measure(range(n), range(n))\n    return qc\n\nN = 5   # 改造區</pre>'
        '<p class="note">位元越多，錯誤次數怎麼變？為什麼？＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p>',
        '<h2>說明卡：我的筆記本</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　最新版本：v＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. GHZ 線路怎麼接？</p><div class="line"></div><p>2. 為什麼理想的直方圖只有全 0 和全 1？</p><div class="line"></div><div class="line"></div>'
        '<p>3. 一個注意事項（例如：為什麼要記版本號？）：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出線路：哈達瑪閘加一串受控反閘</li><li>解釋為什麼理想只有全 0、全 1</li>'
        '<li>說出為什麼位元越多，雜訊造成的錯誤越多</li><li>指出一個注意事項：套件會改版，筆記本要記版本號</li>'
        '<li>替筆記本取名字、寫上版本號存檔</li></ul></div>',
    ]
    return printpack.document('Q057 Release 任務 列印包', '父子科技學院 量子電腦學程 Q057｜Qiskit 實作：Bell 與 GHZ', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q057-qiskit-bell-ghz', folder='Q057_Qiskit實作_Bell與GHZ', files=FILES,
        sheet=('03_實驗紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_Release任務.pdf', pack_pages=4,
        pack_needles=('Release 檢查清單', '理想 vs 有雜訊', '五顆', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q057', episode_dir='specials/q057-qiskit-bell-ghz',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'pip install qiskit qiskit-aer（matplotlib、jupyter 選用）',
               'program': 'bell_ghz_release.py', 'notebook': 'bell_ghz_release.ipynb', 'testedWith': TESTED,
               'recordedRun': {'seed': 2026, 'shots': 1024, 'bellIdeal': RUNS[2][0], 'bellNoisy': RUNS[2][1],
                               'wrongCounts': {str(n): v[0] for n, v in NOISY_SUMMARY.items()}},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q057/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')
