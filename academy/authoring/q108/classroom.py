"""Q108 課堂教材：Shor 實驗紀錄（N = 15 試三個 a）、可執行的 shor_lab.py、古典驗算表、會失敗的 a 改造表、容易錯的地方、教爸爸檢核表與解答。

不需要帳號，也不需要安裝套件：動畫用瀏覽器開 animations/transmon-3d.html#shor 與 operation.html#shor；程式只要 Python 3。
建置時會真的執行一次 shor_lab.py（原始設定，以及 A = 14、A = 4、N = 21 兩種計數位元、A = 5 五種改造），確認輸出和影片、教材寫的數字一致。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q108/classroom.py
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

# 製作代理實跑紀錄：Python 3.13.18，無外部套件，固定亂數種子（SEED = 7），結果可重現
RUN_OUTPUT = '''N = 15，a = 7，計數位元 4 顆（Q = 16）
f(x) = 7^x mod 15：1, 7, 4, 13, 1, 7, 4, 13, 1, 7, 4, 13 …
真實週期 r = 4（古典驗算：7^4 mod 15 = 1）
量測工作暫存器得到 4 → 梳子 x = 2, 6, 10, 14
QFT 後機率最大的 y：0（25.0%）、4（25.0%）、8（25.0%）、12（25.0%）
量測 20 次：y=0 8 次、y=4 2 次、y=8 6 次、y=12 4 次
  y = 0（8 次）：y = 0 → 沒有週期資訊，重跑 ✗
  y = 4（2 次）：4/16 → r = 4 → 7^2 mod 15 = 4 → gcd(3, 15) = 3，gcd(5, 15) = 5 → 15 = 3 × 5 ✓
  y = 8（6 次）：8/16 → r = 4 → 7^2 mod 15 = 4 → gcd(3, 15) = 3，gcd(5, 15) = 5 → 15 = 3 × 5 ✓
  y = 12（4 次）：12/16 → r = 4 → 7^2 mod 15 = 4 → gcd(3, 15) = 3，gcd(5, 15) = 5 → 15 = 3 × 5 ✓
成功分解 12 / 20 次
'''
# 改造試跑：(要改的那幾行, 輸出裡必須出現的字串)
VARIANTS = [
    (('A = 14',), ('真實週期 r = 2', 'QFT 後機率最大的 y：0（50.0%）、8（50.0%）', '14^1 mod 15 = 14 ≡ −1 → 換一個 a ✗', '成功分解 0 / 20 次')),
    (('A = 4',), ('真實週期 r = 2', '4^1 mod 15 = 4 → gcd(3, 15) = 3，gcd(5, 15) = 5 → 15 = 3 × 5 ✓', '成功分解 10 / 20 次')),
    (('N = 21', 'A = 2'), ('真實週期 r = 6', '找不到 r，重跑或加大 Q', '21 = 7 × 3 ✓', '成功分解 8 / 20 次')),
    (('N = 21', 'A = 2', 'COUNT_QUBITS = 5'), ('計數位元 5 顆（Q = 32）', '平凡因數', '成功分解 13 / 20 次')),
    (('A = 5',), ('gcd(5, 15) = 5：運氣好，直接找到因數 5，不用量子電腦',)),
]

PROGRAM = r'''"""父子科技學院 量子電腦學程 Q108：Shor 實驗——自選 N、a 找週期（純 Python，不需要安裝任何套件）

執行：  python shor_lab.py
做法和學程動畫 transmon-3d.html 第 8 章相同：H → 模指數 → 量測工作暫存器 → QFT → 量測 → 連分數與 gcd。
這是小數字示範：電腦直接用 2^t 個振幅模擬，數字一大就算不動——這正是需要量子電腦的地方。
"""
import cmath
import math
import random

N = 15              # 改造區：要分解的數（動畫可選 15 或 21）
A = 7               # 改造區：和 N 互質的 a（N = 15 時可試 2、4、7、8、11、13、14）
COUNT_QUBITS = 4    # 計數位元幾顆：4 顆 → Q = 16；5 顆 → Q = 32
SHOTS = 20          # 量子電路重跑幾次（每次都重設 → 跑完整個電路 → 量一次）
SEED = 7            # 亂數種子：固定它，每次跑出來的結果都一樣


def convergents(y, q):
    """y/q 的連分數漸近分數 [(分子, 分母), ...]"""
    out, n, d, p1, p2, q1, q2 = [], y, q, 1, 0, 0, 1
    while d:
        ai = n // d
        p, qq = ai * p1 + p2, ai * q1 + q2
        out.append((p, qq))
        p2, p1, q2, q1 = p1, p, q1, qq
        n, d = d, n - ai * d
    return out


def post_process(y, n, a, q):
    """古典後處理（和動畫相同）：連分數找候選 r → 驗算 → gcd。回傳 (成功?, 說明)"""
    if y == 0:
        return False, 'y = 0 → 沒有週期資訊，重跑'
    cands = [(p, d) for p, d in convergents(y, q) if d <= n and p > 0]
    r = 0
    for p, d in reversed(cands):
        for m in range(1, 5):
            if m * d <= n and pow(a, m * d, n) == 1:
                r = m * d
                break
        if r:
            break
    frac = '、'.join(f'{p}/{d}' for p, d in cands) or '（無）'
    if not r:
        return False, f'{y}/{q} → 漸近分數 {frac} → 找不到 r，重跑或加大 Q'
    if r % 2:
        return False, f'{y}/{q} → r = {r} 是奇數 → 換一個 a'
    h = pow(a, r // 2, n)
    if h == n - 1:
        return False, f'{y}/{q} → r = {r}，但 {a}^{r // 2} mod {n} = {h} ≡ −1 → 換一個 a'
    f1, f2 = math.gcd(h - 1, n), math.gcd(h + 1, n)
    if f1 in (1, n) or f2 in (1, n):
        return False, f'{y}/{q} → 候選 r = {r}，但 gcd 只得到 1 和 {n}（平凡因數）→ 重跑'
    return True, f'{y}/{q} → r = {r} → {a}^{r // 2} mod {n} = {h} → gcd({h - 1}, {n}) = {f1}，gcd({h + 1}, {n}) = {f2} → {n} = {f1} × {f2}'


if __name__ == '__main__':
    q = 2 ** COUNT_QUBITS
    rng = random.Random(SEED)
    print(f'N = {N}，a = {A}，計數位元 {COUNT_QUBITS} 顆（Q = {q}）')
    g = math.gcd(A, N)
    if g != 1:
        print(f'gcd({A}, {N}) = {g}：運氣好，直接找到因數 {g}，不用量子電腦')
        raise SystemExit
    f = [pow(A, x, N) for x in range(q)]
    r_true = next(k for k in range(1, N + 1) if pow(A, k, N) == 1)
    print(f'f(x) = {A}^x mod {N}：' + ', '.join(map(str, f[:12])) + ' …')
    print(f'真實週期 r = {r_true}（古典驗算：{A}^{r_true} mod {N} = 1）')
    # 量測工作暫存器（觀念上）：隨機選一個 x，留下 f 值相同的 x —— 一把間隔 r 的梳子
    w = f[rng.randrange(q)]
    comb = [x for x in range(q) if f[x] == w]
    print(f'量測工作暫存器得到 {w} → 梳子 x = ' + ', '.join(map(str, comb)))
    # QFT：把梳子轉成尖峰
    amp = [sum(cmath.exp(2j * math.pi * x * y / q) for x in comb) / math.sqrt(len(comb) * q) for y in range(q)]
    prob = [abs(v) ** 2 for v in amp]
    peaks = [(y, p) for y, p in enumerate(prob) if p > 0.005]
    print('QFT 後機率最大的 y：' + '、'.join(f'{y}（{p:.1%}）' for y, p in sorted(peaks, key=lambda t: -t[1])[:8]))
    # 量測計數暫存器 SHOTS 次，每次都做後處理
    count, ok = {}, 0
    for _ in range(SHOTS):
        u, y = rng.random(), 0
        while y < q - 1 and u >= prob[y]:
            u -= prob[y]
            y += 1
        count[y] = count.get(y, 0) + 1
    print(f'量測 {SHOTS} 次：' + '、'.join(f'y={y} {c} 次' for y, c in sorted(count.items())))
    for y in sorted(count):
        good, why = post_process(y, N, A, q)
        ok += count[y] if good else 0
        print(f'  y = {y}（{count[y]} 次）：{why}' + (' ✓' if good else ' ✗'))
    print(f'成功分解 {ok} / {SHOTS} 次')
'''

# N = 15 每個 a 的古典驗算（由 shor_lab.py 的 pow 與 gcd 驗證）：(a, 前四項, r, a^(r/2) mod 15, 結果)
TABLE15 = [(2, '1, 2, 4, 8', 4, 4, '3 × 5'), (4, '1, 4, 1, 4', 2, 4, '3 × 5'), (7, '1, 7, 4, 13', 4, 4, '3 × 5'),
           (8, '1, 8, 4, 2', 4, 4, '3 × 5'), (11, '1, 11, 1, 11', 2, 11, '5 × 3'), (13, '1, 13, 4, 7', 4, 4, '3 × 5'),
           (14, '1, 14, 1, 14', 2, 14, '失敗：14 ≡ −1，換 a')]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q108：第 10 課 Shor 演算法——自選 N、a 找週期（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶出今天的任務：Shor 演算法是一條三段流水線——古典電腦把「分解 N」換成「找 f(x) = aˣ mod N 的週期 r」，量子電腦用模指數加 QFT 找出週期，古典電腦再用連分數與 gcd 收尾。課堂用「Boss 戰（魔王關）」的方式：魔王是 15，孩子是量子操作員，爸爸是古典驗算員。

## 需要準備

| 項目 | 說明 |
|---|---|
| 動畫 | 下載學程的 `animations/` 資料夾，用瀏覽器開 `transmon-3d.html#shor`（第 8 章）；加映 `operation.html#shor`（場景 10，64 格版本）。免安裝、不需帳號 |
| 程式 | `shor_lab.py`：只要有 Python 3 就能跑，不需安裝套件、不需帳號 |
| 列印 | `02_列印包_Shor實驗.pdf`（A4，共 4 頁） |

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片；先猜「15 = ? × ?」，再問「如果數字有 600 多位數呢？」 | 影片、列印包第 1 頁 |
| 10–25 | 概念示範：週期與 gcd、兩組暫存器、梳子 → QFT 尖峰、連分數 | 影片第 3–7 段、列印包第 2 頁 |
| 25–65 | 父子共同實作：第 8 章第 8 步，N = 15 試三個不同的 a，每個多跑幾次，填實驗紀錄；爸爸手算驗證 | `01_操作步驟.md`、列印包第 1、2 頁 |
| 65–75 | 休息 | |
| 75–105 | 孩子獨立改造：試會失敗的 a = 14，說明為什麼要重試；改 `shor_lab.py` 的 A、N、COUNT_QUBITS | `shor_lab.py`、列印包第 3 頁、`03_Shor實驗紀錄.csv` |
| 105–115 | 孩子教爸爸：操作與原理，指出一個限制 | 列印包第 4 頁 |
| 115–120 | 錄音總結、替實驗紀錄命名、存檔 | |

## 課前準備（約 20 分鐘）

- 自己先打開 `transmon-3d.html#shor`，讓步驟 1–7 自動播一次（約 2.5 分鐘）；左上方字幕會跟著動畫說明。第 8 步是自由實驗。
- 跑一次 `python shor_lab.py`，確認最後一行是「成功分解 12 / 20 次」。
- 讀一遍 `04_解答.md`。

## 魔王關規則

- 每個 a 是一次挑戰：孩子在動畫第 8 步選 a、按「一鍵執行」；爸爸在紙上算 aˣ mod 15、找週期、算 gcd，兩邊答案對上才算過關。
- 量到 y = 0、或 a 本身不行（例如 a = 14），不算輸——記下「為什麼失敗」也得分。這就是今天的生活技能：失敗也是資訊。

## 誠實說明

- 動畫和程式都是**小數字示範**（4–6 顆計數位元）。分解真正的 RSA 需要大規模、能容錯的量子電腦：學程文件引用的估計是 2019 年約 2000 萬顆實體位元、8 小時，2025 年不到 100 萬顆、不到一週（前提：錯誤率約 0.1%，加表面碼）。
- 目前分解 15、21 的實驗多半事先知道答案、用簡化過的電路（compiled Shor）。
- 程式的量測用固定亂數種子（SEED = 7），所以每次結果都一樣；動畫的量測每次隨機，成功或失敗的次數會不同。
- 動畫的後處理在 N = 21、5 顆計數位元時，偶爾會把倍數週期（r = 12）得到的「21 = 21 × 1」顯示成功；那其實是平凡因數，要重跑。`shor_lab.py` 已經把這種情況判為失敗。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：N = 15 試三個 a（約 40 分鐘）

1. 用瀏覽器開 `animations/transmon-3d.html#shor`（第 8 章：Shor）。
2. 取消「自動接續」，按步驟按鈕「1」到「7」看一遍：古典歸約 → 均勻疊加 → 模指數運算 → 量測工作暫存器 → QFT → 量測 → 連分數與 gcd。
3. 按步驟按鈕「8」（自由實驗）。N 選「15」，計數位元選「4 顆（Q = 16）」，a 先選「7」。
4. 依序按「① 疊加」「② 模指數」「③ 量測工作」「④ QFT」「⑤ 量測 1 次」，把每一步的畫面記在列印包第 1 頁（梳子在哪些 x？尖峰在哪些 y？）。
5. 改按「一鍵執行」至少 3 次，每次把面板的「最近量到的 y」「連分數 → 週期」「分解結果」抄進實驗紀錄。
6. 換另外兩個 a（建議 2、4、8、11、13 任選），重複第 5 步。爸爸同時在列印包第 2 頁手算 aˣ mod 15。
7. 加碼：按「量測 20 次」，看後方青色長條只長在哪幾個 y。

## 加映：64 格版本（約 10 分鐘，可選）

- `animations/operation.html#shor`：按「自動播放」，看右下角小圖的週期、64 根柱子的尖峰位置（a = 7：0、16、32、48）。
- 換「a = 4」再播一次，尖峰變成 0、32；換「N = 21」看尖峰糊開。

## 下半場：會失敗的 a（約 30 分鐘）

1. 動畫第 8 步選 a = 14，按「一鍵執行」幾次：量到 0 或 8，結果都失敗。看面板「真實週期」，說明為什麼。
2. 打開 `shor_lab.py`，把 `A = 7` 改成 `A = 14`，先在列印包第 3 頁寫預測，再執行 `python shor_lab.py`。
3. 改造：`A = 4`、`A = 5`（和 15 不互質會怎樣？）、`N = 21` 配 `A = 2`，再把 `COUNT_QUBITS` 改成 5。每次都先預測。
4. 想一想：失敗有幾種？哪一種換 a 就好、哪一種重跑就好？
''',

'shor_lab.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n## N = 15：每個 a 的古典驗算\n\n| a | aˣ mod 15（x = 0～3） | 週期 r | a^(r/2) mod 15 | 結果 |\n|---|---|---|---|---|\n'
  + ''.join(f'| {a} | {s} | {r} | {h} | {res} |\n' for a, s, r, h, res in TABLE15)
  + '\n- 7 的例子：7² = 49 ≡ 4，gcd(4 − 1, 15) = 3，gcd(4 + 1, 15) = 5。\n'
  '- a = 14：r = 2，但 14¹ ≡ 14 ≡ −1 (mod 15)，gcd(15, 15) = 15、gcd(13, 15) = 1，只得到平凡因數，一定要換 a。\n'
  '- a = 5、10 等和 15 有公因數的數：gcd(a, 15) 直接就是因數，不必用量子電腦（動畫的 a 按鈕只列互質的數）。\n\n'
  '## Q = 16 的尖峰與後處理\n\n- r = 4：QFT 後只剩 y = 0、4、8、12（各 25%）；y = 4 → 1/4、y = 12 → 3/4 → r = 4；y = 8 → 1/2 → 候選 2 不對、改試 4；y = 0 → 重跑。\n'
  '- r = 2：只剩 y = 0、8（各 50%）；y = 8 → 1/2 → r = 2。\n\n'
  '## shor_lab.py 實跑（Python 3.13.18，SEED = 7）\n\n```\n' + RUN_OUTPUT + '```\n\n'
  '- 改造參考：A = 14 → 成功 0 / 20（y = 0 十次、y = 8 十次碰上 −1）；A = 4 → 成功 10 / 20；N = 21、A = 2 → Q = 16 成功 8 / 20，Q = 32 成功 13 / 20；A = 5 → gcd(5, 15) = 5，直接找到因數。\n'
  '- N = 21 時週期 6 不能整除 Q，尖峰會糊開；計數位元越多，尖峰越集中（理論上要 Q ≥ N²）。\n'
  '- 常見誤解：動畫是小數字示範；分解真正的 RSA 需要大規模容錯量子電腦。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載整個資料夾後用瀏覽器開啟，不需要網路、伺服器或帳號。

## `transmon-3d.html#shor`（第 8 章：Shor，八步驟）

- 步驟按鈕 1–8；「◀ 上一步」「暫停」「重播」「下一步 ▶」；「自動接續」核取方塊。
- 畫面：長條是計數暫存器每個 x 的振幅（高度＝大小，顏色＝相位：金 0°、青 90°、紅 180°、紫 270°）；下方色塊是工作暫存器的 f(x)（同色＝同值）；後方青色長條是量測次數；上方看板左邊是電路、右邊是推導；左上方字幕跟著說明。
- 第 8 步（自由實驗）：N「15」「21」；計數位元「4 顆（Q = 16）」「5 顆（Q = 32）」；a 按鈕（只列和 N 互質的數）；「① 疊加」「② 模指數」「③ 量測工作」「④ QFT」「⑤ 量測 1 次」「量測 20 次」；「一鍵執行」「重設」。面板有「設定」「真實週期（古典驗算）」「最近量到的 y」「連分數 → 週期」「分解結果」。

## `operation.html#shor`（場景 10：Shor 週期尋找）

- x 暫存器 6 顆位元（0–63）。按鈕「N = 15」「N = 21」、a 按鈕、「下一步 ▶」「自動播放」「重設」。
- 步驟 ① H → ② 計算 f(x)（顏色 = f(x)）→ ③ 量測第二暫存器（梳子）→ ④ QFT（青色峰值，位置 64k/r）→ ⑤ 量測（白色）＋連分數與 gcd。
- 右下角小圖：f(x) = aˣ mod N 的週期函數。

## 操作

滑鼠拖曳旋轉、滾輪縮放；transmon-3d 按 ←→ 切換章節。
''',
}

SHEET_HEADER = ['挑戰', 'N', 'a', 'Q', '量到的 y', '連分數 → 週期 r', '爸爸手算的 r', '分解結果', '成功／失敗原因']
SHEET_ROWS = [['1', '15', '7', '16'], ['2', '15', '7', '16'], ['3', '15', '', '16'], ['4', '15', '', '16'], ['5', '15', '14', '16'], ['6', '21', '2', '32']]

EXTRA_CSS = '''table.rec td{height:10mm}table.rec th{white-space:nowrap;font-size:9.5pt}table.amp td,table.amp th{text-align:center;font-size:10.5pt;height:9mm}
.chk li{margin:2.5mm 0;font-size:12.5pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
pre.code{font-size:9pt;background:#f2f6fa;border:1pt solid #cfdde8;padding:3mm;margin:2mm 0;white-space:pre-wrap}'''


def run_program(text):
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / 'shor_lab.py'
        p.write_text(text, encoding='utf-8')
        return subprocess.run([sys.executable, '-I', str(p)], capture_output=True, text=True, check=True,
                              env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}).stdout


def check_program():
    """真的跑 shor_lab.py（隔離模式）：原始設定的輸出要逐字相同，五種改造要出現教材寫的數字。"""
    out = run_program(PROGRAM)
    assert out == RUN_OUTPUT, out
    for lines, needles in VARIANTS:
        text = PROGRAM
        for line in lines:
            key = line.split(' =')[0]
            text, n = re.subn(rf'^{key} = \S+', line, text, count=1, flags=re.M)
            assert n == 1, line
        o = run_program(text)
        for s in needles:
            assert s in o, (lines, s, o)
    return out


def html():
    xs = ''.join(f'<th>{x}</th>' for x in range(8))
    calc = ''.join(f'<tr><th>a = {a}</th>' + ''.join('<td></td>' for _ in range(8)) + '<td></td><td></td><td></td></tr>' for a in ('7', '＿', '＿', '14'))
    pages = [
        '<h2>Shor 實驗紀錄（魔王：15）</h2><p class="lead">transmon-3d.html#shor 第 8 步：N 選 15、計數位元 4 顆，選 a，按「一鍵執行」。</p>'
        '<p>開場先猜：15 = ＿＿ × ＿＿　　a = 7 時，梳子在 x = ＿＿、＿＿、＿＿、＿＿；QFT 後尖峰在 y = ＿＿、＿＿、＿＿、＿＿</p>'
        '<table class="rec"><tr><th>挑戰</th><th>a</th><th>量到的 y</th><th>y / 16</th><th>週期 r</th><th>分解結果</th><th>成功／失敗原因</th></tr>'
        + ''.join(f'<tr><td>{k}</td><td>{a}</td><td></td><td></td><td></td><td></td><td></td></tr>' for k, a in
                  [(1, '7'), (2, '7'), (3, '7'), (4, ''), (5, ''), (6, ''), (7, ''), (8, '')]) + '</table>'
        '<p class="note">規則：每個 a 至少跑 3 次。量到 y = 0 不算輸，寫下「為什麼要重跑」也得分。</p>',
        '<h2>古典驗算表（爸爸用紙筆）</h2><p class="lead">一直乘 a、每次只留除以 15 的餘數，看什麼時候回到 1。</p>'
        f'<table class="amp"><tr><th>x</th>{xs}<th>週期 r</th><th>a^(r/2) mod 15</th><th>gcd → 因數</th></tr>'
        '<tr><th>a = 7</th><td>1</td><td>7</td><td>4</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>'
        + calc.split('</tr>', 1)[1] +
        '</table>'
        '<h3>為什麼週期能分解？</h3><p>aʳ − 1 = (a^(r/2) − 1)(a^(r/2) + 1) 被 15 整除　→　gcd(a^(r/2) − 1, 15) = ＿＿，gcd(a^(r/2) + 1, 15) = ＿＿</p>'
        '<h3>連分數（後處理）</h3><p>量到 y = 12：12/16 = ＿/＿ → 候選 r = ＿＿　　量到 y = 8：8/16 = ＿/＿ → 候選 ＿＿，驗算 7^＿ mod 15 = ＿＿，改試 ＿＿</p>'
        '<p class="note">提示：a = 7 的序列是 1、7、4、13、1…；r 必須讓 aʳ mod 15 = 1。</p>',
        '<h2>會失敗的 a：改 shor_lab.py</h2><p class="lead">先預測，再執行 python shor_lab.py，把最後幾行抄進表格。</p>'
        '<pre class="code">N = 15              # 要分解的數\nA = 7               # 和 N 互質的 a\nCOUNT_QUBITS = 4    # 計數位元幾顆（Q = 2 的次方）\nSHOTS = 20          # 重跑幾次\nSEED = 7            # 亂數種子</pre>'
        '<table class="rec"><tr><th>N</th><th>A</th><th>COUNT_QUBITS</th><th>我的預測</th><th>真實週期 r</th><th>尖峰在哪些 y</th><th>成功幾次 / 20</th></tr>'
        '<tr><td>15</td><td>7</td><td>4</td><td></td><td></td><td></td><td></td></tr>'
        '<tr><td>15</td><td>14</td><td>4</td><td></td><td></td><td></td><td></td></tr>'
        '<tr><td>15</td><td>4</td><td>4</td><td></td><td></td><td></td><td></td></tr>'
        '<tr><td>21</td><td>2</td><td>4</td><td></td><td></td><td></td><td></td></tr>'
        '<tr><td>21</td><td>2</td><td>5</td><td></td><td></td><td></td><td></td></tr></table>'
        '<p>a = 14 為什麼一定失敗？＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p>'
        '<p class="note">失敗有幾種？哪一種換 a 就好、哪一種重跑就好？A = 5 會發生什麼事？＿＿＿＿＿＿＿＿</p>',
        '<h2>容易錯的地方 ＋ 教爸爸</h2><div class="box"><ul class="chk">'
        '<li>r 是奇數，或 a^(r/2) ≡ −1（例如 15 配 14）：換一個 a 重來</li>'
        '<li>量到 y = 0：沒有週期資訊，重跑量子電路</li>'
        '<li>直接量模指數之後的狀態看不出週期：要靠 QFT 把梳子變成尖峰</li>'
        '<li>動畫是小數字示範：分解真正的 RSA 需要大規模容錯量子電腦</li></ul>'
        '<p>我最容易搞錯的一點：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:4mm"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 三段流水線各做什麼？哪一段交給量子電腦？</p><div class="line"></div>'
        '<p>2. QFT 怎麼把梳子變成尖峰？為什麼起點不重要？</p><div class="line"></div>'
        '<ul class="chk"><li>示範動畫第 8 章第 8 步一次「一鍵執行」，並解釋畫面</li><li>指出一個限制</li><li>替實驗紀錄取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q108 Shor 實驗 列印包', '父子科技學院 量子電腦學程 Q108｜第 10 課：Shor 演算法——自選 N、a 找週期', pages, EXTRA_CSS)


if __name__ == '__main__':
    check_program()
    classroom_pack.build(
        slug='q108-shor-period', folder='Q108_Shor實驗', files=FILES,
        sheet=('03_Shor實驗紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_Shor實驗.pdf', pack_pages=4,
        pack_needles=('Shor 實驗紀錄', '古典驗算表', 'shor_lab.py', '容易錯', '教爸爸'),
        authoring_dir=XINEW / 'authoring/q108', episode_dir='specials/q108-shor-period',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'no（瀏覽器開動畫；shor_lab.py 只需 Python 3）',
               'program': 'shor_lab.py', 'testedWith': 'Python 3.13.18 (standard library only, SEED = 7)',
               'recordedRun': {'N': 15, 'a': 7, 'Q': 16, 'shots': 20, 'periodR': 4, 'successes': 12, 'yZero': 8,
                               'a14Successes': 0, 'n21Q16Successes': 8, 'n21Q32Successes': 13},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q108/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')
