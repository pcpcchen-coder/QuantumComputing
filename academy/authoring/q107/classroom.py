"""Q107 課堂教材：四種黑盒判讀表、可執行的 deutsch_box.py、盲測紀錄表（自己當黑盒子）、容易錯的地方、教爸爸檢核表與解答。

不需要帳號，也不需要安裝套件：動畫用瀏覽器開 animations/transmon-3d.html#deutsch-lab；程式只要 Python 3。
建置時會真的執行一次 deutsch_box.py，確認輸出和影片、教材寫的結果一致。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q107/classroom.py
"""
from pathlib import Path
import os
import subprocess
import sys
import tempfile

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 製作代理實跑紀錄：Python 3.13.18，無外部套件，結果固定（無亂數）
RUN_OUTPUT = '''輔助位元準備成 |−⟩（先翻轉再哈達瑪）
  f1（永遠 0，常數）問完後振幅 +0.50 −0.50 +0.50 −0.50｜量到 1 的機率 0%｜判讀 常數 ✓
  f2（永遠 1，常數）問完後振幅 −0.50 +0.50 −0.50 +0.50｜量到 1 的機率 0%｜判讀 常數 ✓
  f3（f(x) = x，平衡）問完後振幅 +0.50 −0.50 −0.50 +0.50｜量到 1 的機率 100%｜判讀 平衡 ✓
  f4（f(x) = NOT x，平衡）問完後振幅 −0.50 +0.50 +0.50 −0.50｜量到 1 的機率 100%｜判讀 平衡 ✓
忘了先翻轉：輔助位元變成 |+⟩
  f1（永遠 0，常數）問完後振幅 +0.50 +0.50 +0.50 +0.50｜量到 1 的機率 0%｜判讀 常數 ✓
  f2（永遠 1，常數）問完後振幅 +0.50 +0.50 +0.50 +0.50｜量到 1 的機率 0%｜判讀 常數 ✓
  f3（f(x) = x，平衡）問完後振幅 +0.50 +0.50 +0.50 +0.50｜量到 1 的機率 0%｜判讀 常數 ✗
  f4（f(x) = NOT x，平衡）問完後振幅 +0.50 +0.50 +0.50 +0.50｜量到 1 的機率 0%｜判讀 常數 ✗
古典電腦：要分別問 f(0)、f(1) 共 2 次；量子：只問 1 次
盲測：黑盒子 ？ 只問 1 次 → 輸入位元量到 1 → 平衡
'''

PROGRAM = r'''"""父子科技學院 量子電腦學程 Q107：Deutsch 演算法與相位回踢——四種黑盒子（純 Python，不需要安裝任何套件）

執行：  python deutsch_box.py
兩顆位元：q0 是輸入位元 x，q1 是輔助位元 y。狀態用 4 個振幅表示，順序是 |x y⟩ = |00⟩、|01⟩、|10⟩、|11⟩
（和 transmon-3d.html 第 7 章的四根長條相同）。
"""
import math

R = 1 / math.sqrt(2)
PREP = True     # 改造區 1：輔助位元要不要先翻成 1？（True = 照課本；False = 忘了準備，看看會怎樣）
SECRET = 'f3'   # 改造區 2（盲測）：孩子偷偷改成 f1、f2、f3 或 f4，只讓爸爸看最後一行

BOXES = [
    ('f1', '永遠 0', '常數', lambda x: 0),
    ('f2', '永遠 1', '常數', lambda x: 1),
    ('f3', 'f(x) = x', '平衡', lambda x: x),
    ('f4', 'f(x) = NOT x', '平衡', lambda x: 1 - x),
]


def hadamard(s, q):
    """對第 q 顆做哈達瑪閘（q = 0 是輸入位元，q = 1 是輔助位元）"""
    bit = 2 if q == 0 else 1
    out = s[:]
    for i in range(4):
        if not i & bit:
            a, b = s[i], s[i | bit]
            out[i], out[i | bit] = R * (a + b), R * (a - b)
    return out


def flip(s, q):
    """對第 q 顆做翻轉閘"""
    bit = 2 if q == 0 else 1
    return [s[i ^ bit] for i in range(4)]


def oracle(s, f):
    """量子黑盒子：|x y⟩ → |x, y ⊕ f(x)⟩（只查詢這一次）"""
    out = [0.0] * 4
    for x in (0, 1):
        for y in (0, 1):
            out[2 * x + (y ^ f(x))] += s[2 * x + y]
    return out


def deutsch(f, prep=True):
    s = [1.0, 0.0, 0.0, 0.0]          # |00⟩
    if prep:
        s = flip(s, 1)                 # 輔助位元翻成 1
    s = hadamard(hadamard(s, 0), 1)    # 兩顆都做哈達瑪閘
    s = oracle(s, f)                   # 問黑盒子一次
    after = s
    s = hadamard(s, 0)                 # 輸入位元再做一次哈達瑪閘
    p1 = s[2] ** 2 + s[3] ** 2         # 量到輸入位元 = 1 的機率
    return after, p1


def sign(v):
    return ('+' if v > 1e-9 else '−' if v < -1e-9 else ' ') + f'{abs(v):.2f}'


if __name__ == '__main__':
    for prep in (PREP, not PREP):
        print('輔助位元準備成 |−⟩（先翻轉再哈達瑪）' if prep else '忘了先翻轉：輔助位元變成 |+⟩')
        for name, rule, kind, f in BOXES:
            after, p1 = deutsch(f, prep)
            guess = '平衡' if p1 > 0.5 else '常數'
            print(f'  {name}（{rule}，{kind}）問完後振幅 ' + ' '.join(sign(v) for v in after)
                  + f'｜量到 1 的機率 {p1 * 100:.0f}%｜判讀 {guess} ' + ('✓' if guess == kind else '✗'))
    print('古典電腦：要分別問 f(0)、f(1) 共 2 次；量子：只問 1 次')
    box = next(b for b in BOXES if b[0] == SECRET)
    _, p1 = deutsch(box[3], PREP)
    print(f'盲測：黑盒子 ？ 只問 1 次 → 輸入位元量到 {round(p1)} → {"平衡" if p1 > 0.5 else "常數"}')
'''
