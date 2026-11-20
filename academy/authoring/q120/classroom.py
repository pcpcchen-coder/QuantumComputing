"""Q120 課堂教材：BV 密碼紀錄、古典 vs 量子次數表、指紋對照單、可執行的 bv_lab.py（純 Python）與選用的 qiskit_check.py、最後一關檢核表與解答。

不需要帳號：動畫用瀏覽器開 animations/basic-circuits.html#bv、transmon-3d.html#bv 與 operation.html#circuit；bv_lab.py 只要 Python 3；
qiskit_check.py 選用（pip install qiskit）。建置時會真的執行一次 bv_lab.py，確認輸出和影片、教材寫的結果一致。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q120/classroom.py
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

# 製作代理實跑紀錄：Python 3.13.18，只用標準函式庫，random.Random(1120)（固定種子；只有第五段的讀取雜訊模擬用到亂數）
RUN_OUTPUT = '''一、古典逐位查詢（密碼 s = 011）
  例：丟 x = 110 → 0＋1＋0 = 1 → 回答 1
  一開始有 8 種可能的密碼
  第 1 次：丟 x = 100 → 回答 0 → 還剩 4 種可能
  第 2 次：丟 x = 010 → 回答 1 → 還剩 2 種可能
  第 3 次：丟 x = 001 → 回答 1 → 還剩 1 種可能
  問了 3 次，只剩 011
  不管丟哪一個 x（000 除外），8 種密碼裡回答 1 的都剛好 4 種：每問一次，最多只能把可能砍掉一半
二、量子線路（密碼 s = 011，振幅順序 000 001 010 011 100 101 110 111）
  ①哈達瑪閘：+0.35 +0.35 +0.35 +0.35 +0.35 +0.35 +0.35 +0.35   每個機率 12.5%
  ②查詢一次：+0.35 −0.35 −0.35 +0.35 +0.35 −0.35 −0.35 +0.35   每個機率 12.5%
    翻成負號的是：001、010、101、110
  ③哈達瑪閘：+0.00 +0.00 +0.00 +1.00 +0.00 +0.00 +0.00 +0.00   讀到 011 的機率 100%
  量子只查詢了 1 次
三、密碼的指紋：查詢一次之後的正負號排列
  s = 000：++++++++   和「對 |000⟩ 做哈達瑪閘」的正負號一樣
  s = 001：+−+−+−+−   和「對 |001⟩ 做哈達瑪閘」的正負號一樣
  s = 010：++−−++−−   和「對 |010⟩ 做哈達瑪閘」的正負號一樣
  s = 011：+−−++−−+   和「對 |011⟩ 做哈達瑪閘」的正負號一樣
  s = 100：++++−−−−   和「對 |100⟩ 做哈達瑪閘」的正負號一樣
  s = 101：+−+−−+−+   和「對 |101⟩ 做哈達瑪閘」的正負號一樣
  s = 110：++−−−−++   和「對 |110⟩ 做哈達瑪閘」的正負號一樣
  s = 111：+−−+−++−   和「對 |111⟩ 做哈達瑪閘」的正負號一樣
  任兩個不同密碼的排列：同號的格數都是 4，另外 4 格反號 → 再做一次哈達瑪閘就分得開
四、次數表：密碼越長
  位數   可能的密碼    古典要問   量子要問   線路的閘（密碼全是 1 時）
    1            2        1 次        1 次        5 個
    2            4        2 次        1 次        8 個
    3            8        3 次        1 次       11 個
    4           16        4 次        1 次       14 個
    5           32        5 次        1 次       17 個
    6           64        6 次        1 次       20 個
    8          256        8 次        1 次       26 個
   10        1,024       10 次        1 次       32 個
   20    1,048,576       20 次        1 次       62 個
五、讀取雜訊：每顆位元讀錯 3%
   3 位元：讀出完整密碼的機率 0.97^3 = 91.3%；模擬 1000 次（random 種子 1120）讀對 894 次，最多的就是密碼
  10 位元：讀出完整密碼的機率 0.97^10 = 73.7%；模擬 1000 次（random 種子 1120）讀對 707 次，最多的就是密碼
  20 位元：讀出完整密碼的機率 0.97^20 = 54.4%；模擬 1000 次（random 種子 1120）讀對 545 次，最多的就是密碼
六、改造區
  我的密碼 110：古典問了 3 次 → 110；量子查詢 1 次
  查詢後的正負號 ++−−−−++；最後讀到 110：100%
'''

# 製作代理實跑紀錄：qiskit 2.6.2，StatevectorSampler(seed=2026)，shots=1000（理想模擬，每個密碼都是 100%，次數不隨種子改變）
QISKIT_OUTPUT = '''密碼 000   ：量 1000 次 {'000': 1000}
密碼 001   ：量 1000 次 {'001': 1000}
密碼 010   ：量 1000 次 {'010': 1000}
密碼 011   ：量 1000 次 {'011': 1000}
密碼 100   ：量 1000 次 {'100': 1000}
密碼 101   ：量 1000 次 {'101': 1000}
密碼 110   ：量 1000 次 {'110': 1000}
密碼 111   ：量 1000 次 {'111': 1000}
密碼 101101：量 1000 次 {'101101': 1000}
     ┌───┐          ┌───┐          ┌─┐   
q_0: ┤ H ├───────■──┤ H ├──────────┤M├───
     ├───┤       │  └───┘     ┌───┐└╥┘┌─┐
q_1: ┤ H ├───────┼─────────■──┤ H ├─╫─┤M├
     ├───┤┌───┐  │   ┌─┐   │  └───┘ ║ └╥┘
q_2: ┤ H ├┤ H ├──┼───┤M├───┼────────╫──╫─
     ├───┤├───┤┌─┴─┐ └╥┘ ┌─┴─┐      ║  ║ 
q_3: ┤ X ├┤ H ├┤ X ├──╫──┤ X ├──────╫──╫─
     └───┘└───┘└───┘  ║  └───┘      ║  ║ 
c: 3/═════════════════╩═════════════╩══╩═
                      2             0  1 
'''

PROGRAM = '''"""父子科技學院 量子電腦學程 Q120：範例 7 BV——查一次讀出整串密碼（純 Python，不需安裝任何套件）

執行：  python bv_lab.py
它印出：
  一、古典逐位查詢：黑盒子怎麼回答、每問一次還剩幾種可能的密碼
  二、量子線路：哈達瑪閘 → 查詢一次 → 哈達瑪閘，每一步的八個振幅（順序 000～111）
  三、密碼的指紋：八個密碼各自的正負號排列，任兩排剛好 4 格同號、4 格反號
  四、次數表：密碼越長，古典要問幾次、量子要問幾次、線路有幾個閘
  五、讀取雜訊：每顆位元讀錯 3% 時，讀出完整密碼的機率
  六、改造區：換成自己的密碼，先預測，再執行
位元字串寫成 s2 s1 s0（最右邊是 s0），和 basic-circuits.html#bv、Qiskit 一樣。
"""
import random
from math import sqrt

SECRET = '011'      # 影片和教材用的密碼


def answer(s, x):
    """黑盒子：對應位相乘、加起來，只回答奇數（1）或偶數（0）"""
    return sum(int(a) * int(b) for a, b in zip(s, x)) % 2


def all_strings(n):
    return [format(i, f'0{n}b') for i in range(2 ** n)]


def classical(s):
    """古典逐位查詢：依序問 100…、010…、…001，記下每次還剩幾種可能"""
    n, alive, log = len(s), all_strings(len(s)), []
    for k in range(n):
        x = '0' * k + '1' + '0' * (n - k - 1)
        a = answer(s, x)
        alive = [c for c in alive if answer(c, x) == a]
        log.append((x, a, len(alive)))
    return log, alive


def h_all(v):
    """每顆位元都做一次哈達瑪閘（n 顆一起）"""
    n = len(v).bit_length() - 1
    for q in range(n):
        m, new = 1 << q, v[:]
        for i in range(len(v)):
            if not i & m:
                a, b = v[i], v[i | m]
                new[i], new[i | m] = (a + b) / sqrt(2), (a - b) / sqrt(2)
        v = new
    return v


def quantum(s):
    """哈達瑪閘 → 查詢一次（s·x 奇數的翻負號）→ 哈達瑪閘；回傳三步的振幅"""
    n = len(s)
    v = [1.0] + [0.0] * (2 ** n - 1)
    v1 = h_all(v)
    v2 = [(-1) ** answer(s, x) * a for x, a in zip(all_strings(n), v1)]
    v3 = h_all(v2)
    return v1, v2, v3


def show(v):
    return ' '.join(f'{a + 0.0:+.2f}'.replace('-', '−') for a in v)


def signs(v):
    return ''.join('+' if a > 0 else '−' for a in v)


def gates(n, ones):
    """教科書版線路的閘數：輔助位元 1 個翻轉閘、n+1 個哈達瑪閘、每個 1 一條受控反閘、最後 n 個哈達瑪閘"""
    return 1 + (n + 1) + ones + n


def noisy_shots(s, shots, p, rng):
    """理想時每次都讀到 s；每顆位元有 p 的機率讀錯（0、1 對調）"""
    out = {}
    for _ in range(shots):
        r = ''.join(('1' if b == '0' else '0') if rng.random() < p else b for b in s)
        out[r] = out.get(r, 0) + 1
    return out


if __name__ == '__main__':
    print(f'一、古典逐位查詢（密碼 s = {SECRET}）')
    print(f'  例：丟 x = 110 → {"＋".join(str(int(a) * int(b)) for a, b in zip(SECRET, "110"))} = '
          f'{sum(int(a) * int(b) for a, b in zip(SECRET, "110"))} → 回答 {answer(SECRET, "110")}')
    log, alive = classical(SECRET)
    print('  一開始有 8 種可能的密碼')
    for k, (x, a, left) in enumerate(log, 1):
        print(f'  第 {k} 次：丟 x = {x} → 回答 {a} → 還剩 {left} 種可能')
    print(f'  問了 {len(log)} 次，只剩 {alive[0]}')
    split = {x: sum(answer(c, x) for c in all_strings(3)) for x in all_strings(3)[1:]}
    print('  不管丟哪一個 x（000 除外），8 種密碼裡回答 1 的都剛好 '
          f'{set(split.values()).pop()} 種：每問一次，最多只能把可能砍掉一半')

    print(f'二、量子線路（密碼 s = {SECRET}，振幅順序 000 001 010 011 100 101 110 111）')
    v1, v2, v3 = quantum(SECRET)
    print(f'  ①哈達瑪閘：{show(v1)}   每個機率 {v1[0] ** 2:.1%}')
    print(f'  ②查詢一次：{show(v2)}   每個機率 {v2[0] ** 2:.1%}')
    print('    翻成負號的是：' + '、'.join(x for x, a in zip(all_strings(3), v2) if a < 0))
    print(f'  ③哈達瑪閘：{show(v3)}   讀到 {all_strings(3)[max(range(8), key=lambda i: v3[i] ** 2)]} 的機率 {max(a * a for a in v3):.0%}')
    print('  量子只查詢了 1 次')

    print('三、密碼的指紋：查詢一次之後的正負號排列')
    pats = {}
    for s in all_strings(3):
        pats[s] = signs(quantum(s)[1])
        ket = [1.0 if x == s else 0.0 for x in all_strings(3)]
        same = signs(h_all(ket)) == pats[s]
        print(f'  s = {s}：{pats[s]}   和「對 |{s}⟩ 做哈達瑪閘」的正負號{"一樣" if same else "不一樣"}')
    agree = {sum(a == b for a, b in zip(pats[s], pats[t])) for s in pats for t in pats if s < t}
    print(f'  任兩個不同密碼的排列：同號的格數都是 {agree.pop()}，另外 4 格反號 → 再做一次哈達瑪閘就分得開')

    print('四、次數表：密碼越長')
    print('  位數   可能的密碼    古典要問   量子要問   線路的閘（密碼全是 1 時）')
    for n in (1, 2, 3, 4, 5, 6, 8, 10, 20):
        print(f'  {n:>3}   {2 ** n:>10,}   {n:>6} 次   {1:>6} 次   {gates(n, n):>6} 個')

    print('五、讀取雜訊：每顆位元讀錯 3%')
    rng = random.Random(1120)
    for n in (3, 10, 20):
        s = (SECRET * 7)[:n]
        got = noisy_shots(s, 1000, 0.03, rng)
        best = max(got, key=got.get)
        print(f'  {n:>2} 位元：讀出完整密碼的機率 0.97^{n} = {0.97 ** n:.1%}；'
              f'模擬 1000 次（random 種子 1120）讀對 {got.get(s, 0)} 次，最多的{"就是" if best == s else "不是"}密碼')

    # 六、改造區：換成自己的 3 位元密碼（只寫 0 和 1），先預測，再執行
    MY_SECRET = '110'
    log, alive = classical(MY_SECRET)
    v1, v2, v3 = quantum(MY_SECRET)
    print('六、改造區')
    print(f'  我的密碼 {MY_SECRET}：古典問了 {len(log)} 次 → {alive[0]}；量子查詢 1 次')
    print(f'  查詢後的正負號 {signs(v2)}；最後讀到 '
          + '、'.join(f'{x}：{a * a:.0%}' for x, a in zip(all_strings(3), v3) if a * a > 1e-9))
'''

QISKIT_PROGRAM = '''"""父子科技學院 量子電腦學程 Q120：用本機 Qiskit 重現 BV 密碼線路（選用，不需要帳號）

安裝（只要一次）：  pip install qiskit
執行：              python qiskit_check.py
線路和 basic-circuits.html#bv 的教科書版相同：q0–q2 是輸入，q3 是輔助位元。
"""
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler


def bv(s):
    """s 寫成 s2 s1 s0；密碼哪一位是 1，就從那顆位元接一條受控反閘到輔助位元"""
    n = len(s)
    qc = QuantumCircuit(n + 1, n)
    qc.x(n)                                  # 輔助位元翻成 1
    qc.h(range(n + 1))                       # 全部做哈達瑪閘
    for i in range(n):                       # 黑盒子（只查詢這一次）
        if s[n - 1 - i] == '1':
            qc.cx(i, n)
    qc.h(range(n))                           # 輸入位元再做哈達瑪閘
    qc.measure(range(n), range(n))
    return qc


sampler = StatevectorSampler(seed=2026)
for s in ('000', '001', '010', '011', '100', '101', '110', '111', '101101'):
    counts = sampler.run([bv(s)], shots=1000).result()[0].data.c.get_counts()
    print(f'密碼 {s:<6}：量 1000 次 {counts}')    # 位元字串的最右邊是 q0
print(bv('011').draw())
'''

RECORD = [  # (密碼, 古典問的 x 與回答, 黑盒子裡的受控反閘, 查詢後變負號的結果, 量 1,000 次)
    ('000', '100→0、010→0、001→0', '沒有（空的）', '沒有（全正）', '000（1000 次）'),
    ('011', '100→0、010→1、001→1', 'q0→q3、q1→q3', '001、010、101、110', '011（1000 次）'),
    ('101', '100→1、010→0、001→1', 'q0→q3、q2→q3', '001、011、100、110', '101（1000 次）'),
    ('111', '100→1、010→1、001→1', 'q0、q1、q2 各一條', '001、010、100、111', '111（1000 次）'),
]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q120：範例 7 BV——查一次讀出整串密碼（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。這一課是模組「動手寫量子電路：從八個範例到自己的線路」的範例 7。
上一課（Q119）用 Deutsch 線路問一次就分出常數或平衡；今天把同一個套路放大成 Bernstein–Vazirani（BV）：黑盒子藏著 3 位元密碼 s，每次只回答 s·x 的奇偶。
核心一句話：**密碼藏在振幅正負號的排列（指紋）裡；這排正負號剛好是 H 作用在 |s⟩ 的結果，H 做兩次等於沒做，所以查詢一次之後再做一次 H，就讀出整串密碼。**
（Q105 已用密碼 101 逐步追蹤八個振幅、玩過隨機隱藏的古典對決；這一課改用密碼 011，從「每問一次最多砍一半」、指紋、位數變多時的限制切入。）

## 題目與古典做法

- 黑盒子：把 s 和你丟的 x 對應位相乘、加起來，只回答奇數（1）或偶數（0）。例：s = 011、x = 110 → 0＋1＋0 = 1 → 回答 1。
- 古典逐位問 100、010、001：s = 011 時回答 0、1、1，三次湊出 011。
- 為什麼古典快不起來：不管丟哪個 x（000 除外），8 種可能的密碼裡剛好 4 種回答 1、4 種回答 0，每問一次最多砍掉一半：8 → 4 → 2 → 1。n 位元就要 n 次。

## 量子做法（basic-circuits.pptx 第 21–22 頁、basic-circuits.html#bv）

q0–q2 是輸入，q3 是輔助位元：① X(q3) ② 四顆都做 H（q3 變成 |−⟩）③ 黑盒子：密碼哪一位是 1，就從那一位接一條 CNOT 到 q3（只查詢這一次）④ q0–q2 再做 H，量 q2 q1 q0。
q3 在 |−⟩，CNOT 不會改變它，而是把負號「回踢」給輸入：s·x 為奇數的輸入多一個負號。

| 密碼 | 古典問的 x → 回答 | 黑盒子裡的 CNOT | 查詢後變負號的結果 | 量 1,000 次 |
|---|---|---|---|---|
''' + ''.join(f'| {" | ".join(r)} |\n' for r in RECORD) + '''
這張表也是作品「BV 密碼紀錄」的範例答案。

## 密碼的指紋（bv_lab.py 第三段）

- 查詢後的正負號排列（000 到 111 由左到右）：s = 011 是 + − − + + − − +。
- 這排正負號剛好等於「對 |011⟩ 做 H」的結果；H 做兩次等於沒做，所以第二次 H 把它還原成 |011⟩。
- 8 個密碼各有一排指紋：000 全正；任兩個不同密碼都是 4 格同號、4 格反號，所以一定分得開。

## 容易錯的地方與限制（驗收要孩子說出至少一個）

1. 位數越多，古典越多次（n 次），量子仍是 1 次查詢；但線路會變大：教科書版最多 3n + 2 個閘，20 位元最多 62 個。
2. 位元字串最右邊是 q0（動畫寫 s2 s1 s0、Qiskit 的 counts 也是），看反會把 011 讀成 110。
3. 查詢後直接量看不出答案（8 個仍各 12.5%），一定要再做一次 H。
4. 讀取有雜訊：每顆位元讀錯 3% 時，整串讀對的機率是 0.97ⁿ：3 位元 91.3%、10 位元 73.7%、20 位元 54.4%；正確的密碼仍是出現最多的，所以要重複跑很多次。
5. BV 全程沒有糾纏，古典電腦也能有效模擬；它的價值是示範「疊加 → 相位 → 干涉」的套路與查詢次數的差別。

## 影片的念法

BV 不念字母，說「範例七」「密碼」；H「哈達瑪閘」、X「翻轉閘」、CNOT「受控反閘」、Z「相位翻轉閘」；q0、q1 念「編號零」「編號一」；|−⟩「負號疊加態」；Qiskit 說「量子程式套件」。

## 兩小時

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片；說明程式對決規則 | 影片、列印包第 1 頁 |
| 10–25 | 對照 basic-circuits.pptx 第 21–22 頁：題目、教科書版線路、指紋 | 簡報 |
| 25–65 | 爸爸在 basic-circuits.html#bv 設密碼、孩子從起點逐步播放、量 1,000 次；填密碼紀錄；transmon-3d.html#bv 第 8 步試 000、111 | `01_操作步驟.md`、列印包第 1、3 頁 |
| 65–75 | 休息 | |
| 75–105 | 孩子跑 bv_lab.py，把 1–20 位元的古典 vs 量子查詢次數畫成表；改 MY_SECRET；（選用）qiskit_check.py | 列印包第 2 頁、`03_BV密碼紀錄.csv` |
| 105–115 | 孩子教爸爸：密碼藏在哪、怎麼讀出來、一個限制 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 下載學程的 `animations/` 資料夾，用瀏覽器開 `basic-circuits.html#bv`（上方三個密碼鈕 s2、s1、s0）、`transmon-3d.html#bv`（第 9 章，步驟按鈕 8 是自由實驗）與 `operation.html#circuit`（左邊面板「Bernstein–Vazirani（秘密字串 101）」）。
- 打開 `slides/output/basic-circuits.pptx` 第 21–22 頁（課綱頁碼正確）。
- 列印 `02_列印包_BV密碼紀錄.pdf`（A4，共 4 頁）；準備方格紙或直接用列印包第 2 頁畫次數表。
- 有 Python 的電腦先跑一次 `python bv_lab.py`；想用 Qiskit 的再 `pip install qiskit` 後跑 `python qiskit_check.py`（選用，不需帳號）。

## 誠實說明

- 動畫與程式是理想模擬（雜訊開關除外）；真實的量子電腦只給量測結果，看不到振幅柱子。
- 3% 讀取誤判是示意值，不代表特定機器；0.97ⁿ 只算讀取誤差，沒算閘誤差。
- 「20 位元最多 62 個閘」是教科書版接法（密碼全為 1）的閘數，不是硬體轉譯後的實際脈衝數。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：爸爸設密碼，孩子逐步播放（約 40 分鐘）

1. 打開 `animations/basic-circuits.html#bv`（範例 7）。上方「密碼 s（s2 s1 s0，點一下切換）」預設 101。
2. 爸爸點按鈕設密碼（例如點 s2、s1 → 011）。換密碼時頁面會停在最後一步；按「⏮ 起點」回到開頭。
3. 孩子每按一次「下一步 ▶」之前先預測，再看：
   - 第 1 步：輔助位元 q3 翻成 1（只有 1000 一根）。
   - 第 2 步：四顆都做 H，16 根柱子一樣大小，右邊 8 根（q3 = 1）整排朝下。
   - 第 3 步：黑盒子裡的 CNOT 數 = 密碼裡 1 的個數；左邊 8 根的上下排法就是指紋（011 是 上下下上上下下上）。
   - 第 4 步：只剩兩根（q3 的 0、1 各一根），按「量測 1,000 次」，下面寫「→ 密碼 s = …」。
4. 把密碼、古典要問的 x 與回答、黑盒子裡的 CNOT、量到什麼，填進列印包第 1 頁。至少做 000、011、111 和一個孩子自己出的密碼。
5. 想看特例：打開 `transmon-3d.html#bv`，按步驟 8（自由實驗），密碼選 000，依序按 ①②③④：黑盒子是空的，兩次 H 抵銷，50 次都是 000。再選 111、按「重設」、按 ①②：奇數個 1 的四根（001、010、100、111）翻紅。
6. 想看雜訊：打開 `operation.html#circuit`，按「Bernstein–Vazirani（秘密字串 101）」，按 5 次「單步 ▶」，再打開「加入雜訊（每閘 1%、讀取 3%）」。

## 下半場：古典 vs 量子次數表（約 30 分鐘）

1. 執行 `python bv_lab.py`，看第四段的次數表（1、2、3、4、5、6、8、10、20 位元）。
2. 在列印包第 2 頁的格子上畫兩條線：橫軸是位數，縱軸是查詢次數；古典一條、量子一條。再加一欄「線路的閘」。
3. 打開 `bv_lab.py` 最下面的改造區，把 `MY_SECRET` 改成自己的密碼（只寫 0 和 1，3 位），先在列印包第 3 頁預測指紋，再執行看第六段。
4. 有裝 Qiskit 的話，跑 `python qiskit_check.py`：8 個 3 位元密碼和 101101 各量 1000 次，全部讀對。
''',

'bv_lab.py': PROGRAM,
'qiskit_check.py': QISKIT_PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n## bv_lab.py 實跑輸出（Python 3.13.18，random.Random(1120)）\n\n```\n' + RUN_OUTPUT + '```\n\n'
  '## qiskit_check.py 實跑輸出（qiskit 2.6.2，StatevectorSampler seed=2026）\n\n```\n' + QISKIT_OUTPUT + '```\n\n'
  '## 常見問題\n\n'
  '- 密碼藏在哪？查詢一次之後，s·x 為奇數的輸入多一個負號；這排正負號（指紋）就是密碼。機率沒變，直接量看不出來。\n'
  '- 為什麼再做一次 H 就讀得出來？指紋剛好等於 H 作用在 |s⟩ 的結果，H 做兩次等於沒做，所以還原成 |s⟩。\n'
  '- 古典能不能少問幾次？不行：每個回答只有 0 或 1，任何 x（000 除外）都把可能的密碼剛好分成兩半，3 位元至少 3 次，n 位元至少 n 次。\n'
  '- 密碼 000 時黑盒子是空的，兩次 H 抵銷，讀到 000；密碼 111 時三條線都接 CNOT，有奇數個 1 的 001、010、100、111 翻負號，讀到 111。\n'
  '- 位數越多量子還是 1 次嗎？查詢是 1 次，但線路的閘變多（最多 3n + 2 個），讀錯其中一位的機會也變大（0.97ⁿ）。\n'
  '- 改造區預設 MY_SECRET = 110：指紋 + + − − − − + +，讀到 110（100%）。\n'
  '- 下一課 Q121：範例 8 Grover——對平均值翻轉。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要伺服器或帳號（transmon-3d.html、operation.html 需要能載入 three.js）。

## `animations/basic-circuits.html#bv`（範例 7 BV）

- 上方「密碼 s（s2 s1 s0，點一下切換）」三個按鈕；換密碼時停在最後一步、清除量測。
- 電路：q0–q2 輸入、q3 輔助；四步依序是 X(q3)、四個 H、虛線框「黑盒 U_s」（密碼為 1 的位各一條 CNOT；000 時寫「（無閘）」）、q0–q2 的 H；量 q2 q1 q0。
- 「⏮ 起點」「◀ 上一步」「▶ 播放」「下一步 ▶」與 5 個小圓點。
- 「振幅與機率」：16 根柱子（含 q3），藍色正、橘色負。「量測 1 次」「量測 1,000 次」「清除」；最後一步量測時出現「→ 密碼 s = …」。
- 頁面最下方「Qiskit 程式碼（會隨上面的選項改變）」可展開，和 qiskit_check.py 的線路相同。

## `animations/transmon-3d.html#bv`（第 9 章 BV 密碼）

- 步驟 1–7 是 101 的導覽；步驟 8「自由實驗」：密碼按鈕 000～111、「隨機（隱藏）」、①–④、「一鍵執行」「古典查詢一次」「重設」、「讀取雜訊」勾選框（每顆 3%）。
- 8 根柱子：金色正、紅色負；上方看板畫電路，黑盒子虛線框內放 Z（相位翻轉閘）。

## `animations/operation.html#circuit`（場景 6 量子線路）

- 左邊面板按「Bernstein–Vazirani（秘密字串 101）」，再按「單步 ▶」5 次走到量測欄；右下插圖是 1000 shots（青線 = 理想機率）。
- 「加入雜訊（每閘 1%、讀取 3%）」：切換時重新抽樣，101 變矮、其他結果冒出小柱子。
''',
}

SHEET_HEADER = ['密碼 s', '古典問 100', '古典問 010', '古典問 001', '古典查詢次數', '黑盒子裡的 CNOT', '查詢後變負號的結果', '量子查詢次數', '量 1,000 次讀到', '我的發現']
SHEET_ROWS = [['範例：011', '0', '1', '1', '3', 'q0→q3、q1→q3', '001、010、101、110', '1', '011（1000 次）', '指紋 + − − + + − − +'],
              ['000', '', '', '', '', '', '', '', '', ''], ['111', '', '', '', '', '', '', '', '', ''],
              ['爸爸出的密碼', '', '', '', '', '', '', '', '', ''], ['我出的密碼', '', '', '', '', '', '', '', '', '']]

EXTRA_CSS = '''table.rec td{height:10mm;font-size:11pt}table.rec td.k{font-weight:bold;color:#0b2540;width:15%}
table.rec th{font-size:10pt}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.grid{display:grid;grid-template-columns:repeat(20,1fr);grid-template-rows:repeat(20,4.2mm);border:1pt solid #4a6a85;margin:2mm 0}
.grid div{border:.3pt solid #c6d6e3}.signs td{text-align:center;width:9%;height:9mm}
pre.code{font-size:9.5pt;background:#f2f6fa;border:1pt solid #cfdde8;padding:3mm;margin:2mm 0;white-space:pre-wrap}'''


def check_program():
    """真的跑一次 bv_lab.py（隔離模式），確認輸出和影片、教材寫的結果一致。"""
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / 'bv_lab.py'
        p.write_text(PROGRAM, encoding='utf-8')
        out = subprocess.run([sys.executable, '-I', str(p)], capture_output=True, text=True, check=True,
                             env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}).stdout
    assert out == RUN_OUTPUT, out
    return out


def html():
    rec = lambda k: f'<tr><td class="k">{k}</td><td></td><td></td><td></td><td></td><td></td></tr>'  # noqa: E731
    cnt = lambda n: f'<tr><td class="k">{n} 位元</td><td></td><td></td><td></td><td></td></tr>'  # noqa: E731
    sg = lambda k: f'<tr><td class="k">{k}</td>' + '<td></td>' * 8 + '</tr>'  # noqa: E731
    head8 = ''.join(f'<th>{format(i, "03b")}</th>' for i in range(8))
    pages = [
        '<h2>BV 密碼紀錄</h2><p class="lead">basic-circuits.html#bv：爸爸設密碼 → 按「起點」→ 孩子一路按「下一步 ▶」→ 量測 1,000 次。</p>'
        '<table class="rec"><tr><th style="width:15%">密碼 s</th><th>古典問 100、010、001 的回答</th><th>古典問幾次</th>'
        '<th>黑盒子裡的 CNOT</th><th>查詢後變負號的結果</th><th>量 1,000 次讀到</th></tr>'
        + rec('000') + rec('011') + rec('111') + rec('爸爸出的') + rec('我出的') + '</table>'
        '<p>第 3 步（查詢後）直接量會怎樣？為什麼？</p><div class="line"></div>'
        '<p>密碼 000 的黑盒子裡有幾條 CNOT？最後為什麼回到 000？</p><div class="line"></div>'
        '<p>量子一共查詢了＿＿次；古典要問＿＿次。</p>',
        '<h2>程式對決：古典 vs 量子次數表</h2><p class="lead">執行 bv_lab.py，看第四段，填表再畫兩條線（橫軸：位數；縱軸：查詢次數）。</p>'
        '<table class="rec"><tr><th style="width:15%">位數</th><th>可能的密碼</th><th>古典要問</th><th>量子要問</th><th>線路的閘（最多）</th></tr>'
        + cnt(1) + cnt(3) + cnt(5) + cnt(10) + cnt(20) + '</table>'
        '<div class="grid">' + '<div></div>' * 400 + '</div>'
        '<p>位數變多時，量子還是只查 1 次；什麼也跟著變多？＿＿＿＿＿＿＿＿＿＿</p>',
        '<h2>密碼的指紋</h2><p class="lead">查詢一次之後，8 個結果的正負號（000 到 111）。先自己填，再跑 bv_lab.py 第三段或動畫第 3 步對答案。</p>'
        '<table class="rec signs"><tr><th style="width:18%">密碼</th>' + head8 + '</tr>'
        + sg('011（範例）').replace('<td></td>' * 8, ''.join(f'<td>{c}</td>' for c in '+−−++−−+'), 1)
        + sg('000') + sg('111') + sg('我的：＿＿＿') + '</table>'
        '<p>我的密碼和 011 的指紋，有幾格同號？幾格反號？＿＿＿＿＿＿</p>'
        '<p>為什麼再做一次 H，指紋就變回密碼？</p><div class="line"></div>'
        '<pre class="code"># bv_lab.py 最下面的改造區：只寫 0 和 1，3 位\n'
        "MY_SECRET = '110'\n"
        '# 改完先預測指紋，再執行 python bv_lab.py，看第六段</pre>',
        '<h2>最後一關：教爸爸讀密碼</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　版本：＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 密碼藏在哪裡（不看稿）：</p><div class="line"></div>'
        '<p>2. 為什麼查詢一次後再做一次 H 就讀得出來：</p><div class="line"></div>'
        '<p>3. 一個限制或容易錯的地方：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><ul class="chk">'
        '<li>說出：黑盒子只回答 s·x 的奇偶；古典每問一次最多砍一半</li><li>說出：線路四步 X、H、黑盒一次、H，量 q2 q1 q0</li>'
        '<li>說出：指紋 = H 作用在 |s⟩；H 做兩次 = 沒做</li><li>指出：位數越多線路變大、雜訊讓整串讀錯；字串最右邊是 q0</li>'
        '<li>完成 BV 密碼紀錄與次數表，和 bv_lab.py 一致</li><li>錄音總結、替作品命名、存一個版本</li></ul></div>',
    ]
    return printpack.document('Q120 BV 密碼紀錄 列印包', '父子科技學院 量子電腦學程 Q120｜範例 7：BV——查一次讀出整串密碼', pages, EXTRA_CSS)


if __name__ == '__main__':
    check_program()
    classroom_pack.build(
        slug='q120-bv-one-query', folder='Q120_範例7_BV_查一次讀出整串密碼', files=FILES,
        sheet=('03_BV密碼紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_BV密碼紀錄.pdf', pack_pages=4,
        pack_needles=('BV 密碼紀錄', '次數表', '密碼的指紋', 'MY_SECRET', '最後一關'),
        authoring_dir=XINEW / 'authoring/q120', episode_dir='specials/q120-bv-one-query',
        extra={'activityMinutes': 120, 'needsAccount': False,
               'needsInstall': 'no（瀏覽器開動畫；bv_lab.py 只需 Python 3；qiskit_check.py 選用：pip install qiskit）',
               'program': 'bv_lab.py', 'optionalProgram': 'qiskit_check.py',
               'testedWith': 'Python 3.13.18 (standard library only, random seed 1120); qiskit 2.6.2',
               'recordedRun': {'secret': '011', 'classicalAnswers': {'100': 0, '010': 1, '001': 1}, 'candidates': [8, 4, 2, 1],
                               'negativeAfterQuery': ['001', '010', '101', '110'], 'fingerprintAgree': 4,
                               'gatesAllOnes': {'3': 11, '10': 32, '20': 62},
                               'readoutExact': {'3': 0.913, '10': 0.737, '20': 0.544},
                               'qiskitAllCorrect': ['000', '001', '010', '011', '100', '101', '110', '111', '101101']},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q120/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')
