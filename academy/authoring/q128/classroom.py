"""Q128 課堂教材：發表模板（五分鐘講稿）、海報版面與觀眾三問紀錄卡、改說明紀錄、最後一關檢核表；
可執行的 exhibit_helper.py（純 Python：八張展品卡、振幅逐步、海報檢查）與 qiskit_check.py（Qiskit Statevector 重算）；八個範例展品目錄與解答。

不需要帳號：動畫用瀏覽器開 animations/basic-circuits.html；exhibit_helper.py 只要 Python 3；qiskit_check.py 需要 pip install qiskit。
建置時會真的執行一次 exhibit_helper.py，確認輸出和影片、教材寫的結果一致；Qiskit 部分（portable-runtime 沒有 Qiskit）比對製作代理已記錄的實跑輸出，
並確認兩邊的八個理想機率相同。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q128/classroom.py
"""
from pathlib import Path
import os
import re
import subprocess
import sys
import tempfile

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 製作代理實跑紀錄：Python 3.13.18，無外部套件，結果固定（無亂數）
RUN_OUTPUT = '''一、八張展品卡（basic-circuits.html 預設選項，理想機率）
  範例 1 疊加（量子硬幣）：1 顆位元、1 步；量 q0 → 0 50.0%、1 50.0%  ✓ 和頁面一樣
  範例 2 干涉（H‑Z‑H = X）：1 顆位元、3 步；量 q0 → 1 100.0%  ✓ 和頁面一樣
  範例 3 Bell 態 Φ⁺：2 顆位元、2 步；量 q1 q0 → 00 50.0%、11 50.0%  ✓ 和頁面一樣
  範例 4 GHZ 態（3 顆）：3 顆位元、3 步；量 q2 q1 q0 → 000 50.0%、111 50.0%  ✓ 和頁面一樣
  範例 5 隱形傳態（ψ = √¾|0⟩+½|1⟩）：3 顆位元、4 步；量 q2 → 0 75.0%、1 25.0%  ✓ 和頁面一樣
  範例 6 Deutsch（f(x) = x）：2 顆位元、4 步；量 q0 → 1 100.0%  ✓ 和頁面一樣
  範例 7 BV（密碼 101）：4 顆位元、4 步；量 q2 q1 q0 → 101 100.0%  ✓ 和頁面一樣
  範例 8 Grover（2 顆，答案 11，1 輪）：2 顆位元、3 步；量 q1 q0 → 11 100.0%  ✓ 和頁面一樣
  結果：8/8 個範例和頁面一樣
二、振幅逐步（MY_EXHIBIT = 'bell'：Bell 態 Φ⁺）
  起點：+1.000|00⟩
  步驟 1 H 閘：q0 進入疊加：+0.707|00⟩  +0.707|01⟩
  步驟 2 CNOT：糾纏：+0.707|00⟩  +0.707|11⟩
  量測 q1 q0 的理想機率：00 50.0%、11 50.0%
三、海報檢查（MY_POSTER）
  ✓ 有「作品名」
  ✓ 有「一句話」
  ✓ 有「線路」
  ✓ 有「振幅逐步」
  ✓ 有「量測結果」
  ✓ 出處寫了動畫或程式的檔名（.html# 或 .py）
  ✓ 觀眾問題 3 個、回答 3 個（要三個都有回答）
  ✓ 有「注意事項」（錯誤、限制或提醒）
  結果：8/8 項通過
'''

# 製作代理實跑紀錄：qiskit 2.6.2（Python 3.13.18），Statevector，結果固定（無亂數）
QISKIT_OUTPUT = '''範例 1 疊加：1 顆位元、1 個閘 → 0 50.0%、1 50.0%
範例 2 干涉：1 顆位元、3 個閘 → 1 100.0%
範例 3 Bell 態 Φ⁺：2 顆位元、2 個閘 → 00 50.0%、11 50.0%
範例 4 GHZ 態（3 顆）：3 顆位元、3 個閘 → 000 50.0%、111 50.0%
範例 5 隱形傳態：3 顆位元、7 個閘 → 0 75.0%、1 25.0%
範例 6 Deutsch：2 顆位元、5 個閘 → 1 100.0%
範例 7 BV（密碼 101）：4 顆位元、10 個閘 → 101 100.0%
範例 8 Grover（答案 11）：2 顆位元、12 個閘 → 11 100.0%
'''

PROGRAM = '''"""父子科技學院 量子電腦學程 Q128：模組發表——量子電路展（純 Python，不需要安裝任何套件，沒有亂數）

執行：  python exhibit_helper.py
一、八張展品卡：照 basic-circuits.html（量子電路入門互動動畫）八個範例的預設選項，
    一步一步算出狀態向量，印出每個範例的位元數、步驟數、量哪幾顆、理想機率，並和頁面上讀到的理想機率比對。
二、振幅逐步：把 MY_EXHIBIT 改成你要發表的範例，印出起點和每一步之後的振幅（發表時的「振幅逐步」那一段）。
三、海報檢查：把海報內容寫進 MY_POSTER，檢查該有的欄位是否齊全、出處有沒有寫、觀眾的問題是不是三個都有回答。
位元字串最右邊是 q0（和動畫、Qiskit 相同）。
"""

# 改造區 1：你要發表的範例（superposition、interference、bell、ghz、teleport、deutsch、bv、grover）
MY_EXHIBIT = 'bell'

# 改造區 2：你的海報（每一行用「標記：內容」）
MY_POSTER = \'\'\'
作品名：兩顆位元的默契——貝爾態
一句話：一個哈達瑪閘加一個受控反閘，兩顆位元量起來永遠一樣
線路：q0 做 H，再做 CNOT（q0 控制、q1 目標），最後量 q1 q0
振幅逐步：起點 |00⟩；H 之後 |00⟩、|01⟩ 各 0.707；CNOT 之後 |00⟩、|11⟩ 各 0.707
量測結果：理想 00、11 各 50%；動畫量 1,000 次只出現 00 和 11
出處：量子電路入門互動動畫 basic-circuits.html#bell 範例 3；程式 exhibit_helper.py（Q128 教材）
問題 1：為什麼不會出現 01？
回答 1：CNOT 讓 q1 跟著 q0 翻，所以兩顆永遠一樣
問題 2：如果先把 q1 翻成 1 會怎樣？
回答 2：變成第三種貝爾態，只出現 01 和 10，兩顆永遠相反
問題 3：真的量子電腦也一樣嗎？
回答 3：真實機器有雜訊，會冒出少量 01、10，要量很多次看比例
注意事項：這是理想模擬的結果，不是真實機器的實測
\'\'\'

from math import cos, sin, pi, sqrt

R = 1 / sqrt(2)


def apply(st, op):
    """把一個閘作用在狀態向量上（振幅都是實數）"""
    n = len(st)
    g = op[0]
    out = st[:]
    if g in ('h', 'x', 'z', 'ry'):
        q = op[1]
        if g == 'h':
            m = (R, R, R, -R)
        elif g == 'x':
            m = (0, 1, 1, 0)
        elif g == 'z':
            m = (1, 0, 0, -1)
        else:
            th = op[2]
            m = (cos(th / 2), -sin(th / 2), sin(th / 2), cos(th / 2))
        for i in range(n):
            if not (i >> q) & 1:
                j = i | (1 << q)
                a, b = st[i], st[j]
                out[i], out[j] = m[0] * a + m[1] * b, m[2] * a + m[3] * b
    elif g == 'cx':
        c, t = op[1], op[2]
        for i in range(n):
            if (i >> c) & 1:
                out[i] = st[i ^ (1 << t)]
    elif g == 'cz':
        for i in range(n):
            if all((i >> q) & 1 for q in op[1:]):
                out[i] = -st[i]
    elif g == 'diff':
        mean = sum(st) / n
        out = [2 * mean - a for a in st]
    return out


# 八個範例（照 basic-circuits.html 的預設選項；每一步可以有好幾個閘）
EXAMPLES = {
    'superposition': ('疊加（量子硬幣）', 1, [0], [('H 閘：做出疊加', [('h', 0)])]),
    'interference': ('干涉（H‑Z‑H = X）', 1, [0], [('第一個 H', [('h', 0)]), ('Z 閘：只改正負號', [('z', 0)]), ('第二個 H：干涉', [('h', 0)])]),
    'bell': ('Bell 態 Φ⁺', 2, [0, 1], [('H 閘：q0 進入疊加', [('h', 0)]), ('CNOT：糾纏', [('cx', 0, 1)])]),
    'ghz': ('GHZ 態（3 顆）', 3, [0, 1, 2], [('H 閘：q0 進入疊加', [('h', 0)]), ('CNOT q0→q1', [('cx', 0, 1)]), ('CNOT q1→q2', [('cx', 1, 2)])]),
    'teleport': ('隱形傳態（ψ = √¾|0⟩+½|1⟩）', 3, [2], [
        ('準備 ψ（q0）', [('ry', 0, pi / 3)]), ('建立糾纏對（q1、q2）', [('h', 1), ('cx', 1, 2)]),
        ('Alice：CNOT 與 H', [('cx', 0, 1), ('h', 0)]), ('Bob：依 2 個位元修正', [('cx', 1, 2), ('cz', 0, 2)])]),
    'deutsch': ('Deutsch（f(x) = x）', 2, [0], [('X：輔助位元', [('x', 1)]), ('H：兩顆都疊加', [('h', 0), ('h', 1)]),
                                              ('黑盒（只查一次）', [('cx', 0, 1)]), ('H：把相位轉成 0/1', [('h', 0)])]),
    'bv': ('BV（密碼 101）', 4, [0, 1, 2], [('X：輔助位元', [('x', 3)]), ('H：全部疊加', [('h', 0), ('h', 1), ('h', 2), ('h', 3)]),
                                          ('黑盒（只查一次）', [('cx', 0, 3), ('cx', 2, 3)]), ('H：干涉讀出密碼', [('h', 0), ('h', 1), ('h', 2)])]),
    'grover': ('Grover（2 顆，答案 11，1 輪）', 2, [0, 1], [('H：所有答案一樣大', [('h', 0), ('h', 1)]),
                                                     ('第 1 輪・標記', [('cz', 0, 1)]), ('第 1 輪・擴散（對平均值翻轉）', [('diff',)])]),
}

# 製作時在 basic-circuits.html 讀到的理想機率（預設選項，跑到最後一步）
PAGE = {
    'superposition': {'0': 0.5, '1': 0.5}, 'interference': {'1': 1.0}, 'bell': {'00': 0.5, '11': 0.5},
    'ghz': {'000': 0.5, '111': 0.5}, 'teleport': {'0': 0.75, '1': 0.25}, 'deutsch': {'1': 1.0},
    'bv': {'101': 1.0}, 'grover': {'11': 1.0},
}


def run(key):
    name, n, meas, steps = EXAMPLES[key]
    st = [0.0] * (1 << n)
    st[0] = 1.0
    hist = [st]
    for _, ops in steps:
        for op in ops:
            st = apply(st, op)
        hist.append(st)
    return hist


def probs(st, meas):
    out = {}
    for i, a in enumerate(st):
        p = a * a
        if p < 1e-12:
            continue
        k = ''.join(str((i >> q) & 1) for q in sorted(meas, reverse=True))
        out[k] = out.get(k, 0) + p
    return dict(sorted(out.items()))


def ket(st, n):
    return '  '.join(f'{a:+.3f}|{i:0{n}b}⟩' for i, a in enumerate(st) if abs(a) > 1e-9)


def fmt(pr):
    return '、'.join(f'{k} {v * 100:.1f}%' for k, v in pr.items())


FIELDS = ['作品名', '一句話', '線路', '振幅逐步', '量測結果', '注意事項']


def check_poster(text):
    lines = [s.strip() for s in text.strip().splitlines() if s.strip()]
    tags = {}
    for s in lines:
        k, _, v = s.partition('：')
        tags.setdefault(k, v)
    res = [(f'有「{f}」', bool(tags.get(f))) for f in FIELDS[:5]]
    src = tags.get('出處', '')
    res.append(('出處寫了動畫或程式的檔名（.html# 或 .py）', '.html#' in src or '.py' in src))
    q = [k for k in tags if k.startswith('問題')]
    a = [k for k in tags if k.startswith('回答') and tags[k]]
    res.append((f'觀眾問題 {len(q)} 個、回答 {len(a)} 個（要三個都有回答）', len(q) == 3 and len(a) == 3))
    res.append(('有「注意事項」（錯誤、限制或提醒）', bool(tags.get('注意事項'))))
    return res


if __name__ == '__main__':
    print('一、八張展品卡（basic-circuits.html 預設選項，理想機率）')
    ok = 0
    for i, key in enumerate(EXAMPLES, 1):
        name, n, meas, steps = EXAMPLES[key]
        pr = probs(run(key)[-1], meas)
        same = pr.keys() == PAGE[key].keys() and all(abs(pr[k] - PAGE[key][k]) < 1e-9 for k in pr)
        ok += same
        who = ' '.join(f'q{q}' for q in sorted(meas, reverse=True))
        print(f'  範例 {i} {name}：{n} 顆位元、{len(steps)} 步；量 {who} → {fmt(pr)}  {"✓ 和頁面一樣" if same else "✗ 和頁面不同"}')
    print(f'  結果：{ok}/{len(EXAMPLES)} 個範例和頁面一樣')
    name, n, meas, steps = EXAMPLES[MY_EXHIBIT]
    hist = run(MY_EXHIBIT)
    print(f'二、振幅逐步（MY_EXHIBIT = {MY_EXHIBIT!r}：{name}）')
    print(f'  起點：{ket(hist[0], n)}')
    for k, (label, _) in enumerate(steps, 1):
        print(f'  步驟 {k} {label}：{ket(hist[k], n)}')
    print(f'  量測 {" ".join(f"q{q}" for q in sorted(meas, reverse=True))} 的理想機率：{fmt(probs(hist[-1], meas))}')
    print('三、海報檢查（MY_POSTER）')
    res = check_poster(MY_POSTER)
    for label, good in res:
        print(f'  {"✓" if good else "✗"} {label}')
    print(f'  結果：{sum(g for _, g in res)}/{len(res)} 項通過')
'''

QPROGRAM = '''"""父子科技學院 量子電腦學程 Q128：用本機 Qiskit 重現展覽的八個範例（理想機率，沒有亂數）

安裝（只要一次）：  pip install qiskit
執行：              python qiskit_check.py
用 Qiskit 的 Statevector 算出八個範例（basic-circuits.html 預設選項）最後的理想機率，
結果應該和 exhibit_helper.py 第一段、以及動畫頁面完全一樣。位元字串最右邊是 q0。
Grover 的擴散用 H、X、CZ、X、H 接成，會多一個整體負號，機率完全相同。
"""
from math import pi

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


def superposition():
    qc = QuantumCircuit(1); qc.h(0); return qc, [0]


def interference():
    qc = QuantumCircuit(1); qc.h(0); qc.z(0); qc.h(0); return qc, [0]


def bell():
    qc = QuantumCircuit(2); qc.h(0); qc.cx(0, 1); return qc, [0, 1]


def ghz():
    qc = QuantumCircuit(3); qc.h(0); qc.cx(0, 1); qc.cx(1, 2); return qc, [0, 1, 2]


def teleport():
    qc = QuantumCircuit(3); qc.ry(pi / 3, 0); qc.h(1); qc.cx(1, 2); qc.cx(0, 1); qc.h(0); qc.cx(1, 2); qc.cz(0, 2)
    return qc, [2]


def deutsch():
    qc = QuantumCircuit(2); qc.x(1); qc.h([0, 1]); qc.cx(0, 1); qc.h(0); return qc, [0]


def bv():
    qc = QuantumCircuit(4); qc.x(3); qc.h([0, 1, 2, 3]); qc.cx(0, 3); qc.cx(2, 3); qc.h([0, 1, 2]); return qc, [0, 1, 2]


def grover():
    qc = QuantumCircuit(2); qc.h([0, 1]); qc.cz(0, 1)
    qc.h([0, 1]); qc.x([0, 1]); qc.cz(0, 1); qc.x([0, 1]); qc.h([0, 1])
    return qc, [0, 1]


EXAMPLES = [('疊加', superposition), ('干涉', interference), ('Bell 態 Φ⁺', bell), ('GHZ 態（3 顆）', ghz),
            ('隱形傳態', teleport), ('Deutsch', deutsch), ('BV（密碼 101）', bv), ('Grover（答案 11）', grover)]

if __name__ == '__main__':
    for i, (name, f) in enumerate(EXAMPLES, 1):
        qc, meas = f()
        pr = Statevector(qc).probabilities_dict(qargs=meas, decimals=6)
        txt = '、'.join(f'{k} {v * 100:.1f}%' for k, v in sorted(pr.items()) if v > 1e-9)
        print(f'範例 {i} {name}：{qc.num_qubits} 顆位元、{qc.size()} 個閘 → {txt}')
'''

# 展品目錄（basic-circuits.html 八個分頁、預設選項、理想機率；對應課次）
EXHIBITS = [
    ('1', '疊加（量子硬幣）', '一顆位元區', '#superposition', '1 顆、1 步', '0、1 各 50%', 'Q114'),
    ('2', '干涉 H‑Z‑H = X', '一顆位元區', '#interference', '1 顆、3 步', '1 = 100%', 'Q115'),
    ('3', 'Bell 態 Φ⁺', '糾纏區', '#bell', '2 顆、2 步', '00、11 各 50%', 'Q116'),
    ('4', 'GHZ 態（3 顆）', '糾纏區', '#ghz', '3 顆、3 步', '000、111 各 50%', 'Q117'),
    ('5', '隱形傳態（ψ = √¾|0⟩+½|1⟩）', '糾纏區', '#teleport', '3 顆、4 步（只量 q2）', '0 = 75%、1 = 25%', 'Q118'),
    ('6', 'Deutsch（f(x) = x）', '演算法區', '#deutsch', '2 顆、4 步（只量 q0）', '1 = 100%（平衡）', 'Q119'),
    ('7', 'BV（密碼 101）', '演算法區', '#bv', '4 顆、4 步', '101 = 100%', 'Q120'),
    ('8', 'Grover（2 顆、答案 11、1 輪）', '演算法區', '#grover', '2 顆、3 步', '11 = 100%', 'Q121'),
]

TEMPLATE_MD = '''# 發表模板（每人 5 分鐘＋觀眾三問）

> 寫法：每一行用「標記：內容」，貼進 exhibit_helper.py 的 MY_POSTER 就能自動檢查。

作品名：＿＿＿＿＿＿＿＿（例：兩顆位元的默契——貝爾態）
一句話：（不認識量子的家人也聽得懂的一句話）
線路：（幾顆位元、幾步、每一步是什麼閘、量哪幾顆）
振幅逐步：（起點 → 每一步之後的振幅；每一步一句話）
量測結果：（理想機率；動畫量 1,000 次的比例；兩者差多少）
出處：（動畫檔名＋#範例＋範例編號；程式檔名＋版本；截圖日期）
問題 1：
回答 1：
問題 2：
回答 2：
問題 3：
回答 3：
注意事項：（錯誤、限制或提醒，例如「這是理想模擬，不是真實機器的實測」）

## 五分鐘講稿分配

| 時間 | 講什麼 | 畫面 |
|---|---|---|
| 0:00–1:00 | 作品名、一句話、線路（幾顆位元、幾步） | basic-circuits.html 該範例的電路 |
| 1:00–4:00 | 振幅逐步：每按一次「下一步 ▶」說一句柱子怎麼變 | 振幅與機率卡 |
| 4:00–5:00 | 量測：先說理想機率，再按「量測 1,000 次」比較；說出出處 | 量測卡＋海報右下角 |

觀眾常問的三種問題（本課整理，課綱只規定「回答三個問題」）：為什麼會這樣？改一個閘會怎樣？真的量子電腦也一樣嗎？
'''

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q128：模組發表——量子電路展（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。QM08「動手寫量子電路：從八個範例到自己的線路」走完了，今天是模組發表：孩子當策展人，把八個範例布置成「量子電路展」，挑一件展品向家人發表五分鐘（線路、振幅逐步、量測結果），回答觀眾的三個問題，完成一張量子電路展海報。好玩機制是「首映會」：作品第一次正式面對觀眾。

## 需要準備

| 項目 | 說明 |
|---|---|
| 動畫 | 下載學程的 `animations/` 資料夾，用瀏覽器開 `basic-circuits.html`（量子電路入門，八個範例）。免安裝、不需帳號 |
| 程式 | `exhibit_helper.py`：只要有 Python 3 就能跑，不需安裝套件；`qiskit_check.py`：需要 `pip install qiskit`（選用） |
| 發表模板 | `06_發表模板.md`（可直接複製）、列印包第 1 頁 |
| 海報 | A3 或 A4 白紙、彩色筆；也可以用簡報軟體做一頁 |
| 列印 | `02_列印包_量子電路展海報.pdf`（A4，共 4 頁） |

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片；孩子先說「八個範例裡我最想展出哪一個？為什麼？」 | 影片、`03_展品目錄.csv` |
| 10–25 | 概念示範：五分鐘三段、以範例 3 Bell 態示範、觀眾三問、海報版面、註明出處 | 影片第 3–8 段、`05_動畫導覽.md` |
| 25–65 | 父子共同實作：每人輪流發表五分鐘、互相提三個問題；跑 exhibit_helper.py 拿展品卡與振幅逐步 | 列印包第 1、2 頁、`exhibit_helper.py` |
| 65–75 | 休息 | |
| 75–105 | 孩子獨立改造：根據觀眾問題修改海報說明，再講一次；用 exhibit_helper.py 檢查海報 | 列印包第 2 頁、`06_發表模板.md` |
| 105–115 | 角色互換：孩子不看稿教爸爸操作與原理 | 列印包第 3、4 頁 |
| 115–120 | 錄音總結（錄音四問）、作品命名、版本存檔 | 列印包第 3 頁 |

## 課前準備（約 20 分鐘）

- 打開 `basic-circuits.html`，點上方八個分頁各看一次；每個範例按「▶ 播放」走到最後一步，再按「量測 1,000 次」。
- 捲到每個範例最下面的「重點」卡，看「延伸：」連結怎麼寫出另一個動畫的名稱與場景：這就是海報出處的寫法。
- 跑一次 `python exhibit_helper.py`，確認「一、八張展品卡」是 8/8、「三、海報檢查」是 8/8。
- 讀一遍 `04_解答.md`，想好你要當觀眾問的三個問題。

## 觀眾（爸爸）的原則

- 認真當觀眾：至少問三個問題，建議三種各一題：為什麼會這樣？改一個閘會怎樣？真的量子電腦也一樣嗎？
- 問倒了不要急著給答案：請孩子先記下來，下半場改說明時再一起查。
- 驗收三件事：孩子能不用看稿說出核心原理；能用動畫示範並說出出處（檔名、#範例、範例編號）；能指出至少一個錯誤、限制或注意事項。

## 誠實說明

- basic-circuits.html 的振幅是頁面內建的狀態向量模擬器算出來的「理想」結果；「量測 1,000 次」用亂數抽樣，每次比例略有不同。
- exhibit_helper.py 照頁面八個範例的預設選項重算，結果和頁面一樣；qiskit_check.py 用 Qiskit 再算一次，八個理想機率也相同。兩支程式都不是真實機器。
- Grover 的擴散步驟：頁面照理想的「對平均值翻轉」計算；用 H、X、CZ 接成的實際電路會多一個整體負號，機率完全相同（頁尾說明）。
- 「海報檢查」只檢查格式（欄位、出處、三題都有回答），不會判斷內容對不對；內容要爸爸和孩子對照動畫。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：挑展品、五分鐘發表、互相提問（約 40 分鐘）

1. 打開 `03_展品目錄.csv`（或列印包第 1 頁下方），挑一件展品；用瀏覽器開 `animations/basic-circuits.html`，點上方對應的分頁（範例 1–8）。
2. 執行 `python exhibit_helper.py`，看「一、八張展品卡」裡你那一件的位元數、步驟數、理想機率；把最上面的 `MY_EXHIBIT` 改成你的範例（例如 `'ghz'`），再跑一次，抄下「二、振幅逐步」。
3. 照 `06_發表模板.md` 寫五分鐘講稿：線路（1 分鐘）→ 振幅逐步（3 分鐘，每按一次「下一步 ▶」說一句）→ 量測結果與出處（1 分鐘，按「量測 1,000 次」）。
4. 先排練一次，再正式發表；觀眾至少問三個問題，發表者把問題記在列印包第 2 頁。
5. 換人發表（爸爸也挑一件），孩子當觀眾提問。

## 下半場：改說明、做海報、上台（約 30 分鐘＋10 分鐘）

1. 找出觀眾卡住的那一句，換成更白話的說法，或多畫一張圖（例如三格振幅）。
2. 做海報：上面作品名＋一句話、中間線路圖＋三格振幅、下面直方圖＋出處。
3. 把海報內容貼進 `exhibit_helper.py` 的 `MY_POSTER`，看「三、海報檢查」是不是 8/8。
4. （選用）有 Qiskit 時執行 `python qiskit_check.py`，確認你那一件的理想機率和頁面一樣，海報出處就寫上「qiskit_check.py（Qiskit 版本）」。
5. 角色互換：孩子不看稿，教爸爸怎麼操作動畫、背後的原理是什麼。
6. 錄音總結：回答列印包第 3 頁的錄音四問；替作品取名字、存一個版本（例如「v1」）。
''',
}

FILES.update({
'exhibit_helper.py': PROGRAM,
'qiskit_check.py': QPROGRAM,
'06_發表模板.md': TEMPLATE_MD,

'04_解答.md': '# 解答（爸爸用）\n\n## 示範：範例 3 Bell 態（Φ⁺）\n\n'
  '- 線路：2 顆位元、2 步：H（q0）→ CNOT（q0 控制、q1 目標）；量 q1 q0。\n'
  '- 振幅逐步（位元字串最右邊是 q0）：起點 +1.000|00⟩ → H 之後 +0.707|00⟩ +0.707|01⟩ → CNOT 之後 +0.707|00⟩ +0.707|11⟩。\n'
  '- 量測：理想 00、11 各 50%；量 1,000 次只會出現 00 和 11（比例每次略有不同）。\n'
  '- 觀眾三問示範：① 為什麼不會出現 01？→ CNOT 讓 q1 跟著 q0 翻，兩顆永遠一樣。'
  '② 先把 q1 翻成 1 會怎樣？→ 第三種貝爾態 Ψ⁺，只出現 01、10，兩顆永遠相反（頁面上方選 Ψ⁺ 就能當場示範）。'
  '③ 真的量子電腦也一樣嗎？→ 有雜訊，會冒出少量 01、10（operation.html#circuit 的「加入雜訊（每閘 1%、讀取 3%）」可示範），所以要量很多次看比例。\n'
  '\n## 八件展品（basic-circuits.html 預設選項）\n\n| 範例 | 名稱 | 展區 | 網址 | 位元與步驟 | 理想機率 | 課次 |\n|---|---|---|---|---|---|---|\n'
  + ''.join(f'| {a} | {b} | {c} | basic-circuits.html{d} | {e} | {f} | {g} |\n' for a, b, c, d, e, f, g in EXHIBITS)
  + '\n## exhibit_helper.py 實跑（Python 3.13.18）\n\n```\n' + RUN_OUTPUT + '```\n\n'
  '## qiskit_check.py 實跑（Qiskit 2.6.2，Statevector，沒有亂數）\n\n```\n' + QISKIT_OUTPUT + '```\n\n'
  '- 兩支程式的八個理想機率完全相同，也和頁面一樣。Qiskit 的閘數比頁面的「步驟」多，因為頁面把同一欄或同一段的閘算成一步（例如 Grover 的擴散一步裡有 9 個閘）。\n'
  '- Grover：Qiskit 用 H、X、CZ、X、H 接成擴散，會多一個整體負號，機率相同；exhibit_helper.py 照頁面用「對平均值翻轉」計算。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載整個資料夾後用瀏覽器開啟，不需要伺服器或帳號（operation.html 需 three.js：資料夾內附 lib/，沒有時會連網下載）。

## `basic-circuits.html`：量子電路入門（八個基礎量子電路）

- 上方八個分頁：範例 1 疊加、2 干涉、3 Bell 態、4 GHZ 態、5 隱形傳態、6 Deutsch、7 BV、8 Grover；網址後加 `#bell` 這類代號可以直接開到那個範例。
- 每個範例：上方選項（例如 Bell 態的 Φ⁺、Φ⁻、Ψ⁺、Ψ⁻）、電路卡（⏮ 起點、◀ 上一步、▶ 播放、下一步 ▶）、振幅與機率卡、量測卡（量測 1 次、量測 1,000 次、清除）。
- 最下面「重點」卡：一段重點說明＋「延伸：」連結（動畫名＋場景或章節）＋可展開的 Qiskit 程式碼。海報出處照「延伸」連結的格式寫。
- 快捷鍵：← → 上一步／下一步，空白鍵播放。

## `operation.html#circuit`：量子線路——一步一步執行（選用）

- 八個預設線路：Bell 態、GHZ 態、干涉、Deutsch–Jozsa、Bernstein–Vazirani、Grover、量子隱形傳態、量子傅立葉轉換。「單步 ▶」一欄一欄執行；最後量 1000 shots。
- 「加入雜訊（每閘 1%、讀取 3%）」：回答「真的量子電腦也一樣嗎？」時可以當場示範。

## `operation.html#workflow`：一次量子計算的完整流程（選用）

- 程式螢幕寫著 Bell 態的程式；關掉「自動播放」，按「下一站 ▶」逐站看：寫程式 → 轉譯 → 脈衝排程 → 控制電子 → 晶片執行 shots → 判別與結果。

## 引用畫面

截圖時寫出檔名、#範例代號與範例編號，例如「basic-circuits.html#bell 範例 3」；程式寫檔名與版本，例如「qiskit_check.py（Qiskit 2.6.2）」。
''',
})

SHEET_HEADER = ['範例', '名稱', '展區', '網址', '位元與步驟', '理想機率', '我想展出？（○）', '我的一句話', '觀眾可能問什麼']
SHEET_ROWS = [[a, b, c, 'basic-circuits.html' + d, e, f, '', '', ''] for a, b, c, d, e, f, _ in EXHIBITS]

EXTRA_CSS = '''table.judge td{height:12mm;font-size:11pt}table.judge td.k{font-weight:bold;color:#0b2540;width:22%}
table.rec td{height:9mm;font-size:10pt}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
pre.code{font-size:9pt;background:#f2f6fa;border:1pt solid #cfdde8;padding:3mm;margin:2mm 0;white-space:pre-wrap}
.poster{border:1.2pt dashed #6f8fbf;height:58mm;margin:2mm 0;padding:2mm;font-size:10pt;color:#567}'''


def table_lines(text):
    """取出「範例 i 名稱：… → 機率」的機率部分，用來比對兩支程式"""
    return [re.sub(r'\s+✓.*$', '', ln.split('→', 1)[1]).strip() for ln in text.splitlines() if '→' in ln and '範例' in ln]


def check_program():
    """真的跑一次 exhibit_helper.py（隔離模式），確認輸出和影片、教材寫的結果一致；再比對 Qiskit 實跑紀錄。"""
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / 'exhibit_helper.py'
        p.write_text(PROGRAM, encoding='utf-8')
        out = subprocess.run([sys.executable, '-I', str(p)], capture_output=True, text=True, check=True,
                             env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}).stdout
    assert out == RUN_OUTPUT, out
    for needle in ('結果：8/8 個範例和頁面一樣', '起點：+1.000|00⟩', '步驟 1 H 閘：q0 進入疊加：+0.707|00⟩  +0.707|01⟩',
                   '步驟 2 CNOT：糾纏：+0.707|00⟩  +0.707|11⟩', '量測 q1 q0 的理想機率：00 50.0%、11 50.0%', '結果：8/8 項通過'):
        assert needle in out, needle
    a, b = table_lines(out), table_lines(QISKIT_OUTPUT)
    assert len(a) == len(b) == 8 and a == b, (a, b)
    compile(QPROGRAM, 'qiskit_check.py', 'exec')
    return out


def html():
    tpl_rows = [('作品名', ''), ('一句話', '（家人聽得懂）'), ('0:00–1:00 線路', '幾顆位元、幾步、量哪幾顆：'),
                ('1:00–4:00 振幅逐步', '每按一步說一句：'), ('4:00–5:00 量測', '理想機率＿＿＿；一千次＿＿＿'), ('出處', '檔名＋#範例＋範例編號：')]
    cat = '；'.join(f'{a} {b}' for a, b, *_ in EXHIBITS)
    pages = [
        '<h2>發表模板：五分鐘講稿</h2><p class="lead">挑一件展品，照三段寫講稿；每人五分鐘，先排練一次再正式發表。</p>'
        '<table class="judge">' + ''.join(f'<tr><td class="k">{a}</td><td>{b}</td></tr>' for a, b in tpl_rows) + '</table>'
        f'<p class="note">展品目錄（basic-circuits.html）：{cat}</p>',
        '<h2>海報草稿與觀眾三問紀錄</h2><p class="lead">由上到下：作品名＋一句話、線路圖＋三格振幅、直方圖＋出處。</p>'
        '<div class="poster">上：作品名＋一句話</div><div class="poster" style="height:40mm">中：線路圖＋三格振幅</div>'
        '<div class="poster" style="height:30mm">下：直方圖（理想 vs 一千次）＋出處</div>'
        '<table class="rec"><tr><th style="width:12%">問題</th><th style="width:44%">觀眾問了什麼</th><th style="width:44%">我怎麼回答／要改哪一句</th></tr>'
        '<tr><td>1 為什麼</td><td></td><td></td></tr><tr><td>2 改一個閘</td><td></td><td></td></tr><tr><td>3 真機器</td><td></td><td></td></tr></table>'
        '<pre class="code">MY_EXHIBIT = &#39;bell&#39;   # 改造區 1：你的展品（superposition、interference、bell、ghz、teleport、deutsch、bv、grover）\nMY_POSTER = &#39;&#39;&#39; ... &#39;&#39;&#39;  # 改造區 2：貼上海報內容（每行「標記：內容」）</pre>',
        '<h2>錄音四問與三個容易錯的地方</h2><div class="box"><p>1. 我的展品在解決什麼？</p><div class="line"></div>'
        '<p>2. 我怎麼做？</p><div class="line"></div><p>3. 哪裡容易錯？</p><div class="line"></div>'
        '<p>4. 生活中或真實的量子電腦哪裡會用到？</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><ul class="chk">'
        '<li>截圖與程式沒寫出處：要寫檔名、#範例、範例編號、程式版本</li>'
        '<li>把模擬器的理想機率當成真實機器的實測；或念出「一千次剛好 500 次」這種每次都會變的數字</li>'
        '<li>位元字串讀反：最右邊是 q0（和動畫、Qiskit 相同）</li></ul></div>',
        '<h2>最後一關：首映會</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　版本：＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 我的展品在解決什麼（一句話）：</p><div class="line"></div>'
        '<p>2. 核心原理：哪一步最關鍵？</p><div class="line"></div>'
        '<p>3. 一個錯誤、限制或注意事項：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><ul class="chk">'
        '<li>完成量子電路展海報（作品名、線路、振幅、直方圖、出處）</li><li>五分鐘發表：線路、振幅逐步、量測結果</li>'
        '<li>回答觀眾三個問題，並依問題修改說明</li><li>不看稿說出核心原理；exhibit_helper.py 海報檢查 8/8</li>'
        '<li>錄音總結、替作品命名、存一個版本</li></ul></div>',
    ]
    return printpack.document('Q128 量子電路展海報 列印包', '父子科技學院 量子電腦學程 Q128｜模組發表：量子電路展', pages, EXTRA_CSS)


if __name__ == '__main__':
    check_program()
    classroom_pack.build(
        slug='q128-circuit-expo', folder='Q128_模組發表_量子電路展', files=FILES,
        sheet=('03_展品目錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_量子電路展海報.pdf', pack_pages=4,
        pack_needles=('發表模板', '海報草稿', '觀眾三問', 'MY_EXHIBIT', 'MY_POSTER', '錄音四問', '容易錯', '最後一關'),
        authoring_dir=XINEW / 'authoring/q128', episode_dir='specials/q128-circuit-expo',
        extra={'activityMinutes': 120, 'needsAccount': False,
               'needsInstall': 'no（瀏覽器開動畫；exhibit_helper.py 只需 Python 3；qiskit_check.py 選用，需 pip install qiskit）',
               'program': 'exhibit_helper.py', 'testedWith': 'Python 3.13.18 (standard library only, no randomness); qiskit 2.6.2 Statevector',
               'recordedRun': {'exhibitCards': '8/8 match basic-circuits.html',
                               'bellSteps': ['+1.000|00⟩', '+0.707|00⟩ +0.707|01⟩', '+0.707|00⟩ +0.707|11⟩'],
                               'qiskitMatches': True, 'posterCheck': '8/8'},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q128/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')
