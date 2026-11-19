"""Q062 課堂教材：分解推導單（15、21）、魔王戰關卡卡、為什麼能分解解說卡、可執行的 shor_lab.py、說明卡與解答。

不需要帳號；shor_lab.py 只用 Python 標準函式庫，模擬 operation.html#shor 的 6 顆計數位元（Q = 64）週期尋找。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q062/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

PROGRAM = r'''"""父子科技學院 量子電腦學程 Q062：Shor（秀爾）演算法 的小模擬器

執行：python shor_lab.py                 → 第一關 N = 15、a = 7，第二關 N = 21、a = 2，各跑一次完整五步
      python shor_lab.py 15 7            → 指定 N 和 a
      python shor_lab.py 15 7 8          → 計數暫存器改成 8 顆位元（Q = 256）
      python shor_lab.py 表 21           → 列出 N = 21 每個 a 的週期與能不能分解
      python shor_lab.py 魔王            → 魔王戰：電腦出題，你先在推導單上算，再按 Enter 對答案
五步：① 疊加＋模指數 ② 量第二組暫存器（梳子）③ 量子傅立葉轉換（尖峰）④ 量測得到 y ⑤ 連分數＋最大公因數。
只用 Python 標準函式庫；振幅用完整的離散傅立葉轉換計算，量測依 |振幅|² 隨機取樣。
"""
import cmath
import random
import sys
from fractions import Fraction
from math import gcd


def period(a, N):
    """古典驗算：最小的 r 使 a^r mod N = 1。"""
    r, v = 1, a % N
    while v != 1:
        v = v * a % N
        r += 1
    return r


def comb(N, a, Q, f0):
    """量完第二組暫存器（量到 f0）之後，第一組剩下的 x。"""
    return [x for x in range(Q) if pow(a, x, N) == f0]


def qft_probs(xs, Q):
    """對均勻的梳子做量子傅立葉轉換，回傳每個 y 的機率。"""
    out = []
    for y in range(Q):
        s = sum(cmath.exp(2j * cmath.pi * x * y / Q) for x in xs)
        out.append(abs(s) ** 2 / (len(xs) * Q))
    return out


def convergents(y, Q):
    """y/Q 的漸近分數（連分數一項一項截斷）。"""
    out, n, d = [], y, Q
    p1, p0, q1, q0 = 1, 0, 0, 1
    while d:
        t = n // d
        p1, p0 = t * p1 + p0, p1
        q1, q0 = t * q1 + q0, q1
        out.append(Fraction(p1, q1))
        n, d = d, n - t * d
    return out


def post(N, a, y, Q):
    """古典收尾：連分數找 r（只用分母 ≤ N 的漸近分數的分母），再算最大公因數。回傳 (結果文字, 因數或 None)。"""
    lines = [f'量到 y = {y}，y / {Q} = {y / Q:.4f}']
    if y == 0:
        return lines + ['y = 0：沒有週期資訊 → 重跑'], None
    cv = [c for c in convergents(y, Q) if c.denominator <= N]
    lines.append('漸近分數：' + '、'.join(f'{c.numerator}/{c.denominator}' for c in cv))
    r = next((c.denominator for c in reversed(cv) if pow(a, c.denominator, N) == 1), None)
    if r is None:
        return lines + ['沒有分母滿足 a^r mod N = 1（k 和 r 可能有公因數，或 Q 太小）→ 重跑'], None
    lines.append(f'週期 r = {r}（驗算 {a}^{r} mod {N} = 1）')
    if r % 2:
        return lines + [f'r = {r} 是奇數 → 魔王反擊，換一個 a'], None
    h = pow(a, r // 2, N)
    p, q = gcd(h - 1, N), gcd(h + 1, N)
    lines.append(f'{a}^{r // 2} mod {N} = {h} → gcd({h} − 1, {N}) = {p}，gcd({h} + 1, {N}) = {q}')
    if 1 < p < N:
        return lines + [f'{N} = {p} × {N // p} ✓'], (p, N // p)
    return lines + ['只拆出 1 和 N → 魔王反擊，換一個 a'], None


def run(N, a, bits=6, rng=random, show=True):
    Q = 2 ** bits
    if gcd(a, N) != 1:
        print(f'gcd({a}, {N}) = {gcd(a, N)}：運氣好，直接找到因數！')
        return
    seq = [pow(a, x, N) for x in range(min(Q, 12))]
    x0 = rng.randrange(Q)
    f0 = pow(a, x0, N)
    xs = comb(N, a, Q, f0)
    pr = qft_probs(xs, Q)
    y = rng.choices(range(Q), weights=pr)[0]
    peaks = [k for k in range(Q) if pr[k] > 0.03]
    if show:
        print(f'=== N = {N}，a = {a}，計數位元 {bits} 顆（Q = {Q}） ===')
        print(f'① 疊加＋模指數：f(x) = {a}^x mod {N} = ' + ', '.join(map(str, seq)) + ' …')
        print(f'② 量第二組暫存器得到 {f0} → 梳子 x = ' + ', '.join(map(str, xs[:6])) + f' …（共 {len(xs)} 根，間隔 {period(a, N)}）')
        print('③ 量子傅立葉轉換 → 尖峰 y = ' + '、'.join(f'{k}（{pr[k]:.1%}）' for k in peaks))
        lines, res = post(N, a, y, Q)
        print('④ ' + lines[0])
        for ln in lines[1:]:
            print('⑤ ' + ln)
    return y


def table(N):
    print(f'N = {N}：每個和 {N} 互質的 a')
    for a in range(2, N):
        if gcd(a, N) != 1:
            continue
        r = period(a, N)
        if r % 2:
            note = 'r 是奇數 → 換 a'
        else:
            h = pow(a, r // 2, N)
            p, q = gcd(h - 1, N), gcd(h + 1, N)
            note = f'{a}^{r // 2} mod {N} = {h}，gcd = {p}、{q}' + ('' if 1 < p < N else ' → 只拆出 1 和 N，換 a')
        print(f'  a = {a:2d}：r = {r}，{note}')


def boss():
    N = random.choice([15, 21])
    a = random.choice([x for x in range(2, N) if gcd(x, N) == 1])
    print(f'魔王出題：分解 N = {N}，用 a = {a}。先在推導單上寫出 {a}^x mod {N} 的週期，再按 Enter。')
    input()
    print(f'週期 r = {period(a, N)}。接著量子電腦跑一次：')
    run(N, a)


if __name__ == '__main__':
    args = sys.argv[1:]
    if args[:1] == ['表']:
        table(int(args[1]) if len(args) > 1 else 15)
    elif args[:1] in (['魔王'], ['boss']):
        boss()
    elif len(args) >= 2:
        run(int(args[0]), int(args[1]), int(args[2]) if len(args) > 2 else 6)
    else:
        rng = random.Random(17)   # 固定種子：第一關量到 48、第二關量到 11
        run(15, 7, rng=rng)
        print()
        run(21, 2, rng=rng)
'''

ns = {}
exec(compile(PROGRAM, 'shor_lab.py', 'exec'), ns)  # 用同一份程式算解答，避免手抄錯
gcd = ns['gcd']


def _table_rows(N):
    rows = ''
    for a in range(2, N):
        if gcd(a, N) != 1:
            continue
        r = ns['period'](a, N)
        if r % 2:
            rows += f'| {a} | {r} | — | — | r 是奇數，換 a |\n'
            continue
        h = pow(a, r // 2, N)
        p, q = gcd(h - 1, N), gcd(h + 1, N)
        rows += f'| {a} | {r} | {h} | {p}、{q} | ' + (f'{N} = {p} × {N // p}' if 1 < p < N else '只拆出 1 和 N，換 a') + ' |\n'
    return rows


def _peaks(N, a, f0x):
    xs = ns['comb'](N, a, 64, pow(a, f0x, N))
    pr = ns['qft_probs'](xs, 64)
    return '、'.join(f'{k}（{pr[k]:.1%}）' for k in range(64) if pr[k] > 0.03)


POST15 = '；'.join(ns['post'](15, 7, 48, 64)[0])
POST21 = '；'.join(ns['post'](21, 2, 53, 64)[0])
POST14 = '；'.join(ns['post'](15, 14, 32, 64)[0])
POST21_11 = '；'.join(ns['post'](21, 2, 11, 64)[0])

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q062：Shor：用干涉找週期（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。今天的核心一句：**Shor（秀爾）演算法把「分解 N」轉換成「找 aˣ mod N 的週期 r」：量子電腦用疊加一次算出所有餘數，再用量子傅立葉轉換讓週期干涉成尖峰；量到 y 之後，用連分數從 y/Q 找出 r，再算 gcd(a^(r/2) ± 1, N) 得到因數。** 好玩機制是魔王戰：爸爸當魔王出 N 和 a，孩子當勇者照五步寫推導單；魔王會反擊（y = 0、r 是奇數、a^(r/2) ≡ −1），遇到就換 a。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 打開 operation.html#shor，N = 15、a = 7，按「下一步」走完五步 | 列印包第 1 頁（推導單 15） |
| 25–65 | 父子分解 15 與 21，每一步寫在推導單；玩魔王戰 | 列印包第 1–3 頁、`shor_lab.py` |
| 65–75 | 休息 | |
| 75–105 | 改造：解釋為什麼找週期就能分解（平方差＋gcd） | 列印包第 4 頁、`shor_lab.py 表 21` |
| 105–115 | 孩子教爸爸：五步、尖峰怎麼來、一個限制 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 15 分鐘）

- 列印 `02_列印包_分解推導單.pdf`（A4，共 4 頁）。第 3 頁關卡卡沿虛線剪開。
- 下載學程的 `animations/` 資料夾，用瀏覽器開 `operation.html#shor`（也可看 `transmon-3d.html#shor` 第 8 章），不需要帳號。
- 電腦有 Python 3 就能執行 `shor_lab.py`（不用安裝套件）。
- 讀一遍 `04_解答.md`。

## 誠實說明

- 動畫和 `shor_lab.py` 都只用 6 顆計數位元（Q = 64）；正式做法要 Q ≥ N²（N = 21 要 441 以上），尖峰才夠尖、連分數才保證找得到 r。
- 動畫面板的連分數會連同分母的倍數一起試，所以只要 y ≠ 0 幾乎都會找到 r；`shor_lab.py` 只用漸近分數的分母，比較接近真實演算法，偶爾會「找不到 → 重跑」。
- 2001 年 IBM 用 7 顆量子位元分解 15、2012 年分解 21，但這些實驗都事先知道答案、把線路簡化了（維基百科 Shor's algorithm）。
- 分解 RSA-2048 需要大規模容錯量子電腦，估計要上百萬顆實體量子位元；現在的機器做不到。
''',

'01_操作步驟.md': '''# 操作步驟

## 先看動畫（約 15 分鐘）

1. 打開 `animations/operation.html#shor`。左邊選「N = 15」、「a = 7」；右下小圖是 f(x) = 7ˣ mod 15，標題寫「a = 7，週期 r = 4」。
2. 按「下一步 ▶」五次，每按一次就把面板（左下）讀數抄到推導單：
   ① 64 根柱子一樣高（均勻疊加）；② 柱子塗上顏色（同色＝同一個餘數）；③ 面板「第二暫存器量到 f = …」、只剩梳子；
   ④ 尖峰在 0、16、32、48；⑤ 量到 y（白色柱子），面板列出漸近分數、r、gcd 與分解結果。
3. 按「重設」再跑一次：量到的 y 可能不同，結果一樣是 15 = 3 × 5（量到 0 就重跑）。
4. 選「N = 21」（自動 a = 2）再走一次：尖峰在 0、11、21、32、43、53 附近，旁邊有矮柱子（64 不是 6 的倍數，尖峰糊開）。

## 父子實作（約 40 分鐘）

1. 先不看動畫，在推導單上用紙筆算 7ˣ mod 15、2ˣ mod 21，找出週期。
2. 執行 `python shor_lab.py`，對照程式印出的五步。
3. 魔王戰：爸爸抽一張關卡卡（N 和 a），孩子寫推導單；遇到魔王反擊就換 a。也可以 `python shor_lab.py 魔王` 讓電腦出題。

## 改造：為什麼找週期就能分解（約 30 分鐘）

1. 用 N = 15、a = 7、r = 4：7⁴ − 1 = 2400 = 160 × 15。
2. 平方差：2400 = (7² − 1)(7² + 1) = 48 × 50。
3. 15 的因數分在兩邊：gcd(48, 15) = 3、gcd(50, 15) = 5。
4. 換成 N = 21、a = 2 自己寫一遍；再想：為什麼 a = 14 對 15 會失敗？（提示：14 + 1 = 15。）
''',

'shor_lab.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n'
  '## 第一關 N = 15、a = 7\n\n'
  '- 7ˣ mod 15：1, 7, 4, 13, 1, …；週期 r = 4（7⁴ = 2401 = 160 × 15 + 1）。\n'
  f'- 量到第二組 4 時梳子 2, 6, 10, …, 62；尖峰：{_peaks(15, 7, 2)}。\n'
  f'- 量到 y = 48：{POST15}。\n\n'
  '## 第二關 N = 21、a = 2\n\n'
  '- 2ˣ mod 21：1, 2, 4, 8, 16, 11, 1, …；週期 r = 6。\n'
  f'- 量到第二組 1 時梳子 0, 6, …, 60（11 根）；尖峰：{_peaks(21, 2, 0)}（64k/6 = 0、10.7、21.3、32、42.7、53.3）。\n'
  f'- 量到 y = 53：{POST21}。\n'
  f'- 量到 y = 11：{POST21_11}。\n\n'
  '## 魔王反擊：N = 15、a = 14\n\n'
  f'- {POST14}。14 ≡ −1 (mod 15)，14 + 1 = 15 是 N 的倍數。\n\n'
  '## 每個 a 的結果（由 `shor_lab.py` 算出）\n\n'
  '### N = 15\n\n| a | r | a^(r/2) mod N | gcd(−1)、gcd(+1) | 結果 |\n|---|---|---|---|---|\n' + _table_rows(15) +
  '\n### N = 21\n\n| a | r | a^(r/2) mod N | gcd(−1)、gcd(+1) | 結果 |\n|---|---|---|---|---|\n' + _table_rows(21) +
  '\n## 為什麼找週期就能分解\n\n'
  'a^r ≡ 1 (mod N) → N 整除 a^r − 1 = (a^(r/2) − 1)(a^(r/2) + 1)。N 不會整除 a^(r/2) − 1（否則 r/2 才是週期）；'
  '只要 N 也不整除 a^(r/2) + 1，N 的因數就分在兩個括號裡，gcd 就能撈出來。r 是奇數時沒有 a^(r/2)，要換 a。\n\n'
  '## 常見誤解\n\n'
  '- 「量子電腦一次試完所有因數」：不是。它算的是週期，靠干涉讓週期變成尖峰；直接量只會隨機拿到一組。\n'
  '- 「現在就能破解 RSA」：分解 2048 位元 RSA 需要大規模容錯量子電腦（估計上百萬顆實體量子位元），現在的機器做不到。\n'
  '- 「分解 15、21 的實驗就是完整的 Shor」：那些實驗事先知道答案、簡化了線路。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要帳號。

## `animations/operation.html#shor`（場景 10：Shor 週期尋找，課綱指定）

- 按鈕：「N = 15」「N = 21」、a 的按鈕（和 N 互質的數）、「下一步 ▶」「自動播放」「重設」。
- 64 根柱子是 6 顆計數位元的 x = 0～63；右下小圖是 f(x) = aˣ mod N；左下面板寫出每一步的讀數與推導。
- 面板內容較多時，在左邊面板裡往下捲就看得到 gcd 與分解結果。

## `animations/transmon-3d.html#shor`（第 8 章：Shor 演算法，分解 15）

- 4 顆計數位元（Q = 16），長條顏色代表相位；八個步驟從古典歸約、均勻疊加、模指數、量測工作暫存器、QFT、量測到連分數與 gcd；第 8 步「自由實驗」可換 N、a 與計數位元數。

## 操作

滑鼠拖曳旋轉、滾輪縮放；左右方向鍵切換場景。
''',
}

SHEET_HEADER = ['回合', 'N', 'a', '週期 r', '量到的 y', 'y / 64', '漸近分數', 'a^(r/2) mod N', 'gcd(… − 1, N)', 'gcd(… + 1, N)', '結果／魔王反擊']
SHEET_ROWS = [[str(k)] for k in range(1, 11)]

EXTRA_CSS = '''.cards{display:grid;grid-template-columns:1fr 1fr;gap:4mm}.cards .cut{padding:4mm 5mm;height:52mm;text-align:center}
.cards h3{font-size:14pt;margin:0 0 2mm}.cards .big{font-size:26pt;font-weight:700;color:#0b2540;margin:2mm 0}.cards p{margin:1mm 0;font-size:11pt}
table.dv td{height:10mm}table.dv th{text-align:left;font-size:10.5pt}table.dv td:first-child{width:34mm;font-weight:700}
table.rw td{height:7mm;text-align:center}table.rw th{text-align:center;font-size:9.5pt}
.chk li{margin:2mm 0;font-size:12.5pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}'''

CARDS = [('15', '7', '標準關'), ('15', '2', '標準關'), ('15', '14', '反擊關'), ('21', '2', '糊開關'),
         ('21', '4', '反擊關'), ('21', '10', '進階關')]


def sheet(N, a, hint):
    rows = [('① 古典轉換', f'gcd({a}, {N}) = ＿＿（要是 1）'),
            ('② 模指數', f'{a}ˣ mod {N}：x = 0, 1, 2, 3, 4, 5, 6 → ＿＿＿＿＿＿＿＿＿＿＿＿；週期 r = ＿＿'),
            ('③ 量第二組', '量到 f = ＿＿；梳子 x = ＿＿、＿＿、＿＿ …（間隔 ＿＿）'),
            ('④ 干涉（QFT）', '尖峰在 y ≈ 64k / r = ＿＿＿＿＿＿＿＿＿＿；量到 y = ＿＿'),
            ('⑤ 連分數', 'y / 64 = ＿＿＿＿ ≈ ＿＿ / ＿＿ → r = ＿＿；驗算 aʳ mod N = 1'),
            ('⑥ gcd', f'a^(r/2) mod {N} = ＿＿；gcd(＿＿ − 1, {N}) = ＿＿；gcd(＿＿ + 1, {N}) = ＿＿'),
            ('結果', f'{N} = ＿＿ × ＿＿　　或　魔王反擊：＿＿＿＿＿＿')]
    body = ''.join(f'<tr><td>{k}</td><td>{v}</td></tr>' for k, v in rows)
    return (f'<h2>分解推導單：魔王 {N}</h2><p class="lead">a = {a}。{hint}</p>'
            f'<table class="dv"><tr><th>步驟</th><th>寫下你的推導</th></tr>{body}</table>')


def html():
    cards = ''.join(f'<div class="cut"><h3>關卡卡・{t}</h3><p class="big">N = {n}</p><p>a = {a}</p>'
                    '<p>魔王收好答案，勇者寫推導單</p></div>' for n, a, t in CARDS)
    rows = ''.join('<tr>' + '<td></td>' * 7 + '</tr>' for _ in range(6))
    pages = [
        sheet(15, 7, '在 operation.html#shor 選 N = 15、a = 7，按「下一步」五次，把面板讀數抄下來。'),
        sheet(21, 2, '選 N = 21（自動 a = 2）。64 不是 6 的倍數，尖峰會糊開，量到的 y 只是接近 64k/6。')
        + '<div class="box" style="margin-top:4mm"><h3>魔王反擊紀錄</h3>'
        '<table class="rw"><tr><th>N</th><th>a</th><th>r</th><th>量到 y</th><th>a^(r/2) mod N</th><th>反擊原因</th><th>換成的 a</th></tr>'
        f'{rows}</table><p class="note">反擊三種：y = 0（沒資訊，重跑）；r 是奇數；a^(r/2) ≡ −1（只拆出 1 和 N）。</p></div>',
        '<h2>魔王戰關卡卡</h2><p class="lead">沿虛線剪開。爸爸（魔王）抽一張、先偷偷算好答案；孩子（勇者）照五步寫推導單。</p>'
        f'<div class="cards">{cards}</div>',
        '<h2>說明卡：為什麼找週期就能分解</h2><div class="box">'
        '<p>1. aʳ ≡ 1 (mod N)，所以 aʳ − 1 是 N 的倍數。例：7⁴ − 1 = 2400 = 160 × 15。</p>'
        '<p>2. 平方差：aʳ − 1 = (a^(r/2) − 1)(a^(r/2) + 1)。例：2400 = 48 × 50。</p>'
        '<p>3. 兩半都不是 N 的倍數時，N 的因數分在兩邊：gcd(48, 15) = 3、gcd(50, 15) = 5。</p>'
        '<p>換你寫：N = 21、a = 2、r = 6 → ＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p></div>'
        '<div class="box" style="margin-top:3mm"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 秀爾演算法在解決什麼？</p><div class="line"></div><p>2. 我怎麼做？</p><div class="line"></div>'
        '<p>3. 哪裡容易錯？真實的量子電腦哪裡會用到？</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:3mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出五步：模指數、量測、QFT、連分數、gcd</li>'
        '<li>解釋為什麼干涉會讓週期變成尖峰</li>'
        '<li>指出一個限制：分解 RSA-2048 需要大規模容錯量子電腦，現在做不到</li>'
        '<li>替推導單取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q062 Shor：用干涉找週期 列印包', '父子科技學院 量子電腦學程 Q062｜Shor：用干涉找週期', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q062-shor-period', folder='Q062_Shor用干涉找週期', files=FILES,
        sheet=('03_推導紀錄表.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_分解推導單.pdf', pack_pages=4,
        pack_needles=('分解推導單', '魔王反擊紀錄', '關卡卡', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q062', episode_dir='specials/q062-shor-period',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'program': 'shor_lab.py', 'bossCards': [f'N={n},a={a}' for n, a, _ in CARDS],
               'shorFrom': 'slides/QC_Operation_Talk.pptx p41; animations/operation.html#shor', 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q062/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')
