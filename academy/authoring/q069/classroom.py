"""Q069 課堂教材：人肉離子鏈口令卡、正規模觀察表、離子數紀錄表（atoms.html#modes）、說明卡與最後一關、正規模計算程式與解答。

不需要帳號，也不需要安裝任何套件（動畫用瀏覽器開啟；ion_chain_modes.py 只用 Python 內建功能）。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q069/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 製作代理實跑 ion_chain_modes.py（Python 3.13）的結果，與動畫 04_modes.js 讀數一致（頻率單位：軸向頻率 ω_z）
# (離子數, 最高軸向, 最低徑向 @ 頻率比 5, 最低徑向 @ 頻率比 10)
TABLE = [
    (2, '1.732', '4.899', '9.950'), (3, '2.408', '4.754', '9.879'), (4, '3.051', '4.566', '9.790'),
    (5, '3.671', '4.332', '9.683'), (6, '4.274', '4.046', '9.559'), (7, '4.864', '3.698', '9.417'),
    (8, '5.443', '3.269', '9.257'), (9, '6.013', '2.724', '9.079'), (10, '6.576', '1.970', '8.881'),
    (11, '7.132', '0.264', '8.664'), (12, '7.682', '不穩定（鋸齒形警告）', '8.426'),
]
# 觀察表要演、要看的模：(名稱, 動畫怎麼選, 頻率, 樣子, 人肉離子鏈口令)
MODES = [
    ('軸向質心模', '軸向模態、模式編號 1', '1.000 ω_z', '全部同向、一樣大', '「質心！」大家一起往左、往右踏步'),
    ('呼吸模', '軸向模態、模式編號 2', '1.732 ω_z（≈ √3）', '中間不動，兩邊反向，越外面動得越多', '「呼吸！」左右兩半同時往外、再同時往內'),
    ('軸向第三模', '軸向模態、模式編號 3', '2.412 ω_z（五顆）', '兩端同向，中間三顆往反方向', '挑戰：兩端和中間反著走'),
    ('徑向質心模', '徑向模態、模式編號 1', '5.000 ω_z（頻率比 5）', '全部一起上下', '「蹲！」大家一起蹲下、站起'),
    ('徑向傾斜模', '徑向模態、模式編號 2', '4.899 ω_z（頻率比 5）', '中間不動，左邊下、右邊上，像翹翹板', '「翹翹板！」左半蹲、右半站，再交換'),
]

PROGRAM = r'''"""父子科技學院 量子電腦學程 Q069：離子鏈的正規模（只用 Python 內建功能，不需要安裝套件）

和動畫 atoms.html#modes 用同一組方程：長度以 ℓ = (e²/4πε₀mω_z²)^(1/3) 為單位、頻率以軸向頻率 ω_z 為單位。
執行：python ion_chain_modes.py          （預設：頻率比 ω_r/ω_z = 5）
      python ion_chain_modes.py 10       （改頻率比）
"""
import math
import sys


def hessian(x):
    n = len(x)
    H = [[0.0] * n for _ in range(n)]
    for i in range(n):
        s = 1.0
        for j in range(n):
            if j != i:
                c = 2.0 / abs(x[i] - x[j]) ** 3
                s += c
                H[i][j] = -c
        H[i][i] = s
    return H


def solve_linear(M, b):
    n = len(b)
    M = [r[:] for r in M]
    b = b[:]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c]))
        M[c], M[p] = M[p], M[c]
        b[c], b[p] = b[p], b[c]
        for r in range(c + 1, n):
            f = M[r][c] / M[c][c]
            for k in range(c, n):
                M[r][k] -= f * M[c][k]
            b[r] -= f * b[c]
    x = [0.0] * n
    for r in range(n - 1, -1, -1):
        x[r] = (b[r] - sum(M[r][k] * x[k] for k in range(r + 1, n))) / M[r][r]
    return x


def eigenvalues(A):
    """對稱矩陣的 Jacobi 旋轉法，回傳由小到大的特徵值。"""
    n = len(A)
    a = [r[:] for r in A]
    for _ in range(100):
        off = sum(a[p][q] ** 2 for p in range(n) for q in range(p + 1, n))
        if off < 1e-22:
            break
        for p in range(n):
            for q in range(p + 1, n):
                if abs(a[p][q]) < 1e-15:
                    continue
                th = (a[q][q] - a[p][p]) / (2 * a[p][q])
                t = math.copysign(1.0, th) / (abs(th) + math.sqrt(th * th + 1))
                c = 1 / math.sqrt(t * t + 1)
                s = t * c
                for k in range(n):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p], a[k][q] = c * akp - s * akq, s * akp + c * akq
                for k in range(n):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k], a[q][k] = c * apk - s * aqk, s * apk + c * aqk
    return sorted(a[i][i] for i in range(n))


def chain(n, ratio):
    # 平衡位置：牛頓法解 u_i = Σ sgn(u_i − u_j)/(u_i − u_j)²
    u = [(i - (n - 1) / 2) * (2.2 / n ** 0.44) for i in range(n)]
    for _ in range(200):
        g = [u[i] - sum(math.copysign(1.0, u[i] - u[j]) / (u[i] - u[j]) ** 2 for j in range(n) if j != i) for i in range(n)]
        d = solve_linear(hessian(u), g)
        u = [x - dx for x, dx in zip(u, d)]
        if max(abs(v) for v in d) < 1e-12:
            break
    A = hessian(u)
    axial = [math.sqrt(v) for v in eigenvalues(A)]
    R = [[(ratio ** 2 - (A[i][j] - 1) / 2) if i == j else -A[i][j] / 2 for j in range(n)] for i in range(n)]
    rv = eigenvalues(R)
    radial = [math.sqrt(v) if v > 0 else float('nan') for v in rv]
    return u, axial, radial, rv[0] <= 0


if __name__ == '__main__':
    ratio = float(sys.argv[1]) if len(sys.argv) > 1 else 5.0
    print(f'頻率比 ω_r/ω_z = {ratio}（頻率單位：軸向頻率 ω_z）')
    print('離子數 | 質心 | 呼吸 | 最高軸向 | 徑向質心 | 最低徑向 | 相鄰徑向最小間距')
    for n in range(2, 13):
        u, ax, rad, zig = chain(n, ratio)
        ok = [w for w in rad if w == w]
        gap = min(abs(ok[i] - ok[i - 1]) for i in range(1, len(ok))) if len(ok) > 1 else 0
        low = '不穩定（鋸齒形）' if zig else f'{min(rad):.3f}'
        print(f'{n:>4}   | {ax[0]:.3f} | {ax[1]:.3f} | {ax[-1]:.3f}    | {max(ok):.3f}    | {low} | {gap:.3f}')
    u, ax, rad, zig = chain(5, ratio)
    print('五顆離子的平衡位置：', ', '.join(f'{x:+.3f}' for x in u))
    print('相鄰間距（中間密、兩端疏）：', ', '.join(f'{u[i + 1] - u[i]:.3f}' for i in range(4)))
'''

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q069：離子鏈的集體振動（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶孩子看：好幾顆離子在阱裡排成一列，靠庫侖力連在一起，整條鏈有固定的幾種振動方式（正規模）；
雷射把一顆離子的狀態寫進共用的振動，振動再影響另一顆離子，所以振動就是離子之間的「量子匯流排」。
今天的好玩機制是「角色扮演（人肉離子鏈）」：全家排成一列手拉手，用身體演出質心模和呼吸模。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 概念示範：排成一列、正規模、質心模與呼吸模、量子匯流排 | 影片第 3–8 段 |
| 25–65 | 人肉離子鏈：演質心、呼吸（挑戰：翹翹板、第三模），每演一個就在觀察表畫箭頭；再用 `animations/atoms.html#modes` 對答案 | 列印包第 1–2 頁 |
| 65–75 | 休息 | |
| 75–105 | 改造：在動畫裡把離子數 2 → 12，記錄最高軸向、最低徑向頻率；遇到鋸齒形警告就拉高頻率比 | 列印包第 3 頁、`03_離子數紀錄表.csv` |
| 105–115 | 孩子教爸爸：兩個模怎麼動、為什麼是量子匯流排、離子越多為什麼越難 | 列印包第 4 頁 |
| 115–120 | 錄音總結、替觀察表命名、存檔 | |

## 課前準備（約 15 分鐘）

- 電腦或平板，用瀏覽器開 `animations/atoms.html#modes`（場景 4「離子鏈集體振動」；不需要網路、伺服器或帳號）。
- 列印 `02_列印包_離子鏈的集體振動.pdf`（A4，共 4 頁）；把第 2 頁的口令卡剪開。
- 清出一塊可以讓全家排一列、左右各踏一步的空地。人數最好三人以上（單數人時，呼吸模的正中間那位站著不動）。
- 讀一遍 `04_解答.md`。

## 安全與誠實說明

- 手拉手時輕輕拉、不要猛扯；「推一下最旁邊的人」只輕推肩膀，旁邊有家具時先移開。
- 人肉離子鏈只是比喻：真的離子不會碰在一起，隔著一段距離靠庫侖力互相推；振動的頻率也遠比人走路快。
- 動畫的頻率都以「軸向頻率 ω_z」為單位，不是實際的兆赫數；「一條鏈約 20–30 顆以內最好用」是學程簡報的代表說法。
- 動畫滑桿在面板下方，視窗不夠高時要捲動左邊面板才看得到。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：人肉離子鏈（約 40 分鐘）

1. 全家排成一列，手拉手；手臂就是彈簧，每個人是一顆離子。爸爸當指揮（人少時可以一邊當離子一邊喊）。
2. 指揮喊「質心！」：大家一起往左踏一步、再一起往右踏一步，步伐一樣大。
3. 指揮喊「呼吸！」：左半邊往左、右半邊往右（一起往外），再一起往內；正中間的人站穩不動，越外面的人動得越多。
4. 每演完一個模，在列印包第 1 頁的觀察表畫下每個人的箭頭。
5. 打開 `animations/atoms.html#modes`，看左下讀數與每顆離子上方的青色箭頭，和你們畫的比一比：
   - 「軸向模態」＋模式編號 1 → 質心模（1.000 ω_z）；模式編號 2 → 呼吸模（1.732 ω_z）。
6. 挑戰：模式編號 3（兩端和中間反著走）、「徑向模態」（上下動：質心＝一起蹲、傾斜＝翹翹板）。
7. 最後輕推最旁邊那位的肩膀一下，看看動作怎麼傳到整排：這就是「振動傳遍整條鏈」。

## 下半場：增加離子數（約 30 分鐘）

1. 動畫維持「軸向模態」、模式編號 1。把「離子數 N」從 2 一格一格加到 12。
2. 每加一次，在列印包第 3 頁記下：讀數的「最高」軸向頻率、徑向「最低」頻率，看右下頻率譜的藍線（軸向）和紅線（徑向）。
3. 加到 11、12 顆時，下方會跳出「鏈折成鋸齒形」的警告：把「徑向/軸向頻率比」拉到 10，再記一次。
4. 比一比「相鄰徑向模最小間距」：頻率比 5 時 0.101、頻率比 10 時 0.050。想一想：為了排更多離子得拉高頻率比，模的間距就跟著縮小。
5. 想看數字表的，執行 `python ion_chain_modes.py`（或 `python ion_chain_modes.py 10`），和動畫讀數對照。
''',

'ion_chain_modes.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n## 正規模觀察表\n\n| 模 | 動畫怎麼選 | 頻率 | 樣子 | 口令 |\n|---|---|---|---|---|\n'
  + ''.join(f'| {a} | {b} | {c} | {d} | {e} |\n' for a, b, c, d, e in MODES)
  + '\n## 離子數紀錄表（質心永遠 1.000、呼吸永遠 1.732）\n\n| 離子數 | 最高軸向 | 最低徑向（頻率比 5） | 最低徑向（頻率比 10） |\n|---|---|---|---|\n'
  + ''.join(f'| {n} | {a} | {r5} | {r10} |\n' for n, a, r5, r10 in TABLE)
  + '\n相鄰徑向模最小間距：頻率比 5 → 0.101 ω_z；頻率比 10 → 0.050 ω_z（這個最小間距是徑向質心模和傾斜模的差，約等於 1 ÷（2 × 頻率比））。'
    '十二顆、頻率比 5 時動畫讀數寫 0.040，因為不穩定的模被當成 0 計算。鋸齒形臨界頻率比：5 顆約 2.5、10 顆約 4.6、12 顆約 5.4。\n\n'
  + '## 常見問題\n\n'
  '- 為什麼離子會排成一列？阱沿軸向像一個碗把離子往中間推，離子都帶正電又互相排斥，兩種力平衡；中間的離子被兩邊夾，所以中間密、兩端疏。\n'
  '- 為什麼叫量子匯流排？振動是整條鏈共用的：雷射把一顆離子的狀態寫進振動，振動再影響另一顆離子（西拉克和佐勒 1995 年的想法），'
  '所以同一條鏈任兩顆離子都能直接做兩位元閘（全連接）。\n'
  '- 為什麼離子越多越難？模越多、頻率越擠，雷射越難只推其中一個；整條鏈越重，閘越慢；加熱與串擾更嚴重。所以大系統把鏈拆短，靠搬運或光子互連。\n'
  '- 常見誤解：「離子越多越好，一條鏈可以一直加」——離子越多，模式越擠，閘越難做得又快又準。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路、伺服器或帳號。

## atoms.html#modes（離子阱與中性原子 場景 4「離子鏈的集體振動：量子匯流排」）

- 中間：一排離子（黃色球）在四根淡色電極之間；每顆上方的青色箭頭是它在這個模裡的相對位移，旁邊的網格球是平衡位置。
- 上方金色標籤：目前的模和頻率，例如「COM（質心）模：ω = 1.000 ω_z」「呼吸模（breathing）：ω = 1.732 ω_z」。
- 下方標籤：平常說明箭頭的意思；頻率比太小時變成「⚠ … 鏈折成鋸齒形（zigzag）」警告。
- 左邊面板：按鈕「軸向模態」「徑向模態」；滑桿「離子數 N」（2–12）、「模式編號」（1–12）、「徑向/軸向頻率比 ω_r/ω_z」（1.5–10）；讀數列出質心、呼吸、最高、最低與相鄰徑向模最小間距。
- 右下小圖「模態頻率譜」：藍線＝軸向、紅線＝徑向，白線是目前選的模；寫著「徑向模擠在 ω_r 下方」。
- 操作：滑鼠拖曳旋轉、滾輪縮放、`R` 重設視角、`H` 隱藏面板、空白鍵暫停；左右方向鍵換場景（下一堂用場景 5「Mølmer–Sørensen 閘」）。
''',
}

SHEET_HEADER = ['離子數', '最高軸向（ω_z）', '最低徑向：頻率比 5', '最低徑向：頻率比 10', '有沒有鋸齒形警告（自己填）', '我的觀察（自己填）']
SHEET_ROWS = [[str(n), a, r5, r10, '', ''] for n, a, r5, r10 in TABLE]

EXTRA_CSS = '''table.obs td{height:27mm;font-size:10.5pt;vertical-align:top}table.obs{font-size:10.5pt}
table.rec td{height:12.5mm;font-size:10.5pt}table.rec{font-size:10.5pt}
.cards{display:grid;grid-template-columns:1fr 1fr;gap:4mm;margin-top:3mm}
.card{border:1.2pt dashed #7f9bb3;border-radius:3mm;height:52mm;padding:4mm;display:flex;flex-direction:column;justify-content:space-between}
.card b{font-size:20pt}.card .h{font-size:11pt;color:#4a6a88}
.chk li{margin:2mm 0;font-size:12pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}'''


def html():
    obs = ''.join(f'<tr><td>{a}<br><span style="color:#4a6a88">{b}</span></td><td></td><td></td><td></td></tr>' for a, b, *_r in MODES)
    cards = ''.join(f'<div class="card"><span class="h">口令 {i}</span><b>{e.split("」")[0].lstrip("「")}</b><span class="h">{e.split("」")[1] if "」" in e else e}</span></div>'
                    for i, (a, b, c, d, e) in enumerate(MODES[:2] + MODES[3:], 1))
    rows = ''.join(f'<tr><td>{n}</td><td></td><td></td><td></td><td></td></tr>' for n, *_r in TABLE)
    pages = [
        '<h2>正規模觀察表</h2><p class="lead">演完一個模，就畫下每個人（每顆離子）的箭頭；再到 atoms.html#modes 對答案、抄下頻率。</p>'
        '<table class="obs"><tr><th style="width:24%">模（動畫怎麼選）</th><th style="width:36%">畫箭頭（每個人一支）</th><th>頻率（ω_z）</th><th>一句話說它的樣子</th></tr>'
        + obs + '</table><p class="note">作品名稱：＿＿＿＿＿＿＿＿＿＿　提示：質心模是全部同向；呼吸模中間不動、兩邊反向。</p>',
        '<h2>人肉離子鏈口令卡</h2><p class="lead">全家排成一列手拉手，手臂當彈簧。指揮抽一張卡喊口令，大家一起演；演對了才換下一張。</p>'
        '<div class="cards">' + cards + '</div><p class="note">安全：輕輕拉手、不要猛扯；輕推肩膀，旁邊不要有家具。</p>',
        '<h2>離子數紀錄表</h2><p class="lead">在 atoms.html#modes 把離子數從 2 加到 12，記下讀數；出現鋸齒形警告時，把頻率比拉到 10 再記一次。</p>'
        '<table class="rec"><tr><th>離子數</th><th>最高軸向</th><th>最低徑向（比 5）</th><th>最低徑向（比 10）</th><th>警告？</th></tr>' + rows + '</table>'
        '<p class="note">質心永遠是 ＿＿＿，呼吸永遠是 ＿＿＿。相鄰徑向模最小間距：比 5 → ＿＿＿，比 10 → ＿＿＿。</p>',
        '<h2>說明卡與最後一關</h2><div class="box"><h3>量子匯流排說明卡（寫給爸爸看）</h3>'
        '<p>1. 離子為什麼排成一列：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p><p>2. 質心模和呼吸模怎麼動：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p>'
        '<p>3. 振動怎麼讓兩顆離子傳話：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p><p>4. 離子越多為什麼越難：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p></div>'
        '<div class="box" style="margin-top:4mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出：庫侖力讓離子一起振動，整條鏈有固定的正規模</li>'
        '<li>演出並說出質心模（全部同向，ω_z）與呼吸模（中間不動、兩邊反向，√3 ω_z）</li>'
        '<li>說出量子匯流排：雷射把狀態寫進振動，振動再影響另一顆離子；同一條鏈任兩顆都能做閘</li>'
        '<li>指出一個限制：離子越多，模式越擠，閘越難做得又快又準</li>'
        '<li>替正規模觀察表取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q069 離子鏈的集體振動 列印包', '父子科技學院 量子電腦學程 Q069｜離子鏈的集體振動', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q069-ion-chain-modes', folder='Q069_離子鏈的集體振動', files=FILES,
        sheet=('03_離子數紀錄表.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_離子鏈的集體振動.pdf', pack_pages=4,
        pack_needles=('正規模觀察表', '人肉離子鏈口令卡', '離子數紀錄表', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q069', episode_dir='specials/q069-ion-chain-modes',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'none（瀏覽器開啟動畫；程式只用 Python 內建功能）',
               'animation': 'animations/atoms.html#modes', 'modes': len(MODES), 'ionCounts': [n for n, *_r in TABLE],
               'program': 'ion_chain_modes.py', 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q069/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')
