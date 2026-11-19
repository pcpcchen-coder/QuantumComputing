"""Q119 課堂教材：四種黑盒判讀表、偵探辦案卡片遊戲、8 顆球改造單、可執行的 deutsch_lab.py（純 Python）與選用的 qiskit_check.py、最後一關檢核表與解答。

不需要帳號：動畫用瀏覽器開 animations/basic-circuits.html#deutsch 與 operation.html#interference；deutsch_lab.py 只要 Python 3；
qiskit_check.py 選用（pip install qiskit）。建置時會真的執行一次 deutsch_lab.py，確認輸出和影片、教材寫的結果一致。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q119/classroom.py
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

# 製作代理實跑紀錄：Python 3.13.18，只用標準函式庫，random.Random(1119)（固定種子；只有第一段的模擬次數用到亂數）
RUN_OUTPUT = '''一、古典偵探搖球
  兩顆球：搖 1 次只看到一個顏色，什麼都不能判斷；四種黑盒子都要搖 2 次
          2 顆球：運氣最差要搖 2 次
          8 顆球：運氣最差要搖 5 次
         50 顆球：運氣最差要搖 26 次
  1,000,000 顆球：運氣最差要搖 500,001 次
  8 顆球把 72 種放法全部試一遍，最多搖了 5 次（和上面相同）
  允許出錯：隨機搖 10 顆（每次放回），全部同色就判常數
    一半一半的機器被誤判成常數的機率 2 × (1/2)^10 = 0.00195（約 0.2%）
    50 顆球、搖出不放回時：2 × C(25,10) / C(50,10) = 0.00064
    真的模擬 100,000 台一半一半的機器（random 種子 1119）：誤判 191 台（0.191%）
二、德意志線路：四種黑盒子各問一次（振幅順序 |00⟩ |01⟩ |10⟩ |11⟩，字串 |q1 q0⟩）
  f(x)=0   兩顆都紅（常數）
    ①翻轉輔助：+0.00 +0.00 +1.00 +0.00   量 q0 得到 1 的機率 0.00
    ②兩顆哈達瑪：+0.50 +0.50 −0.50 −0.50   量 q0 得到 1 的機率 0.50
    ③問黑盒一次：+0.50 +0.50 −0.50 −0.50   量 q0 得到 1 的機率 0.50
    ④輸入哈達瑪：+0.71 +0.00 −0.71 +0.00   量 q0 得到 1 的機率 0.00
    判讀：q0 = 0 → 常數 ✓（只問了黑盒子 1 次）
  f(x)=1   兩顆都綠（常數）
    ①翻轉輔助：+0.00 +0.00 +1.00 +0.00   量 q0 得到 1 的機率 0.00
    ②兩顆哈達瑪：+0.50 +0.50 −0.50 −0.50   量 q0 得到 1 的機率 0.50
    ③問黑盒一次：−0.50 −0.50 +0.50 +0.50   量 q0 得到 1 的機率 0.50
    ④輸入哈達瑪：−0.71 +0.00 +0.71 +0.00   量 q0 得到 1 的機率 0.00
    判讀：q0 = 0 → 常數 ✓（只問了黑盒子 1 次）
  f(x)=x   一紅一綠（平衡）
    ①翻轉輔助：+0.00 +0.00 +1.00 +0.00   量 q0 得到 1 的機率 0.00
    ②兩顆哈達瑪：+0.50 +0.50 −0.50 −0.50   量 q0 得到 1 的機率 0.50
    ③問黑盒一次：+0.50 −0.50 −0.50 +0.50   量 q0 得到 1 的機率 0.50
    ④輸入哈達瑪：+0.00 +0.71 +0.00 −0.71   量 q0 得到 1 的機率 1.00
    判讀：q0 = 1 → 平衡 ✓（只問了黑盒子 1 次）
  f(x)=1−x 一綠一紅（平衡）
    ①翻轉輔助：+0.00 +0.00 +1.00 +0.00   量 q0 得到 1 的機率 0.00
    ②兩顆哈達瑪：+0.50 +0.50 −0.50 −0.50   量 q0 得到 1 的機率 0.50
    ③問黑盒一次：−0.50 +0.50 +0.50 −0.50   量 q0 得到 1 的機率 0.50
    ④輸入哈達瑪：+0.00 −0.71 +0.00 +0.71   量 q0 得到 1 的機率 1.00
    判讀：q0 = 1 → 平衡 ✓（只問了黑盒子 1 次）
三、8 顆球的版本：3 個輸入位元、8 條路
  常數 全紅
    每條路的章 ++++++++   |000⟩ 的振幅 +1.000 → P(000) = 1.000
    最後量到：000：100.0%   判讀：全 0 → 常數
  常數 全綠
    每條路的章 −−−−−−−−   |000⟩ 的振幅 -1.000 → P(000) = 1.000
    最後量到：000：100.0%   判讀：全 0 → 常數
  平衡 紅綠紅綠紅綠紅綠
    每條路的章 +−+−+−+−   |000⟩ 的振幅 +0.000 → P(000) = 0.000
    最後量到：001：100.0%   判讀：一定有 1 → 平衡
  平衡 紅綠綠紅綠紅紅綠
    每條路的章 +−−+−++−   |000⟩ 的振幅 +0.000 → P(000) = 0.000
    最後量到：111：100.0%   判讀：一定有 1 → 平衡
  沒守承諾 5 綠 3 紅
    每條路的章 −−+−−+−+   |000⟩ 的振幅 -0.250 → P(000) = 0.062
    最後量到：000：6.2%、001：6.2%、010：6.2%、011：6.2%、100：6.2%、101：56.2%、110：6.2%、111：6.2%   判讀：有時全 0、有時有 1：判不準
四、改造區
  我的 8 顆球 [0, 0, 1, 1, 1, 1, 0, 0]（平衡）   正號 4 條、負號 4 條
    |000⟩ 的振幅 = (4 − 4) / 8 = +0.000 → P(000) = 0.000
    最後量到：110：100.0%
'''

# 製作代理實跑紀錄：qiskit 2.6.2，StatevectorSampler(seed=2026)，shots=1000（沒守承諾那一台的次數是隨機的，換種子會不同）
QISKIT_OUTPUT = '''f(x)=0   量 q0 1000 次：{'0': 1000}
f(x)=1   量 q0 1000 次：{'0': 1000}
f(x)=x   量 q0 1000 次：{'1': 1000}
f(x)=1−x 量 q0 1000 次：{'1': 1000}
常數 全綠：量 1000 次，全 0（000）出現 1000 次；最多的是 000
平衡 紅綠紅綠紅綠紅綠：量 1000 次，全 0（000）出現 0 次；最多的是 001
平衡 紅綠綠紅綠紅紅綠：量 1000 次，全 0（000）出現 0 次；最多的是 111
沒守承諾 5 綠 3 紅：量 1000 次，全 0（000）出現 51 次；最多的是 101
     ┌───┐          ┌───┐┌─┐
q_0: ┤ H ├───────■──┤ H ├┤M├
     ├───┤┌───┐┌─┴─┐├───┤└╥┘
q_1: ┤ X ├┤ H ├┤ X ├┤ X ├─╫─
     └───┘└───┘└───┘└───┘ ║ 
c: 1/═════════════════════╩═
                          0 
'''

PROGRAM = '''"""父子科技學院 量子電腦學程 Q119：範例 6 Deutsch——紅綠球搖獎機（純 Python，不需安裝任何套件）

執行：  python deutsch_lab.py
它印出：
  一、古典偵探搖球：兩顆球要搖幾次？50 顆、8 顆球運氣最差要搖幾次？允許一點點出錯時，隨機搖 10 顆會猜錯多少？
  二、德意志線路：四種黑盒子各問一次（和 basic-circuits.html#deutsch 相同），每一步的四個振幅與量到 1 的機率
  三、8 顆球的版本（3 個輸入位元）：每條路蓋的正負號、|000⟩ 的振幅，以及最後量到哪些結果
  四、改造區：自己設計 8 顆球的顏色，先預測，再執行
紅色記 0、綠色記 1。第 x 顆球的顏色就是 f(x)。
位元字串寫成 |q1 q0⟩：最右邊那位是 q0（輸入），左邊是 q1（輔助位元），和 Qiskit、basic-circuits.html 一樣。
"""
import random
from math import comb, sqrt

R2 = 1 / sqrt(2)

# 兩顆球的四種黑盒子：(名字, 第 1 次搖 f(0), 第 2 次搖 f(1))
BOXES = [('f(x)=0   兩顆都紅', 0, 0), ('f(x)=1   兩顆都綠', 1, 1),
         ('f(x)=x   一紅一綠', 0, 1), ('f(x)=1−x 一綠一紅', 1, 0)]


def kind(colors):
    """顏色清單 → 常數、平衡，或「沒守承諾」"""
    g = sum(colors)
    return '常數' if g in (0, len(colors)) else '平衡' if 2 * g == len(colors) else '沒守承諾'


def worst_case(n):
    """n 顆球（一半一半或全同色），搖出不放回，保證知道答案最多要搖幾顆：一顆一顆試所有可能的排列太多，
    用道理算：運氣最差時前面一直同色；同色的球最多 n/2 顆，所以第 n/2 + 1 顆一定揭曉。這裡再用 n = 8 全部排列驗證一次。"""
    return n // 2 + 1


def brute_worst(n):
    """n 顆球全部可能的放法都試一遍：每次搖到「已經能確定」為止，記下最多搖了幾顆"""
    from itertools import permutations
    worst = 0
    machines = [tuple([0] * n), tuple([1] * n)] + list(set(permutations([0] * (n // 2) + [1] * (n // 2))))
    for m in machines:
        seen = set()
        for k, c in enumerate(m, 1):
            seen.add(c)
            if len(seen) == 2 or k == n // 2 + 1:      # 看到兩種顏色 → 平衡；同色已超過一半 → 常數
                worst = max(worst, k)
                break
    return worst


def deutsch(f0, f1):
    """兩顆位元的德意志線路，回傳每一步之後的四個振幅（順序 |00⟩ |01⟩ |10⟩ |11⟩，字串是 |q1 q0⟩）"""
    s = [1.0, 0.0, 0.0, 0.0]
    out = []
    s = [s[i ^ 2] for i in range(4)]                                   # ① X(q1)：輔助位元翻成 1
    out.append(('①翻轉輔助', s))
    s = h(h(s, 0), 1)                                                  # ② 兩顆都做 H
    out.append(('②兩顆哈達瑪', s))
    f = (f0, f1)
    s = [s[i ^ 2] if f[i & 1] else s[i] for i in range(4)]             # ③ 黑盒：|x⟩|y⟩ → |x⟩|y ⊕ f(x)⟩
    out.append(('③問黑盒一次', s))
    s = h(s, 0)                                                        # ④ 輸入位元再做 H
    out.append(('④輸入哈達瑪', s))
    return out


def h(s, q):
    m, new = 1 << q, s[:]
    for i in range(len(s)):
        if not i & m:
            a, b = s[i], s[i | m]
            new[i], new[i | m] = (a + b) * R2, (a - b) * R2
    return new


def p_q0_is_1(s):
    return sum(a * a for i, a in enumerate(s) if i & 1)


def eight(colors):
    """8 顆球（3 個輸入位元）：H⊗3 → 每條路蓋 (−1)^f(x) → H⊗3。回傳每個結果 y 的振幅"""
    n = len(colors)
    return [sum((-1) ** (colors[x] + bin(x & y).count('1')) for x in range(n)) / n for y in range(n)]


def show(v):
    return ' '.join(f'{a + 0.0:+.2f}'.replace('-', '−') for a in v)


if __name__ == '__main__':
    print('一、古典偵探搖球')
    print('  兩顆球：搖 1 次只看到一個顏色，什麼都不能判斷；四種黑盒子都要搖 2 次')
    for n in (2, 8, 50, 1_000_000):
        print(f'  {n:>9,} 顆球：運氣最差要搖 {worst_case(n):,} 次')
    print(f'  8 顆球把 72 種放法全部試一遍，最多搖了 {brute_worst(8)} 次（和上面相同）')
    k = 10
    print(f'  允許出錯：隨機搖 {k} 顆（每次放回），全部同色就判常數')
    print(f'    一半一半的機器被誤判成常數的機率 2 × (1/2)^{k} = {2 * 0.5 ** k:.5f}（約 {2 * 0.5 ** k:.1%}）')
    print(f'    50 顆球、搖出不放回時：2 × C(25,{k}) / C(50,{k}) = {2 * comb(25, k) / comb(50, k):.5f}')
    rng = random.Random(1119)
    trials = 100_000
    wrong = sum(len({rng.random() < 0.5 for _ in range(k)}) == 1 for _ in range(trials))
    print(f'    真的模擬 {trials:,} 台一半一半的機器（random 種子 1119）：誤判 {wrong} 台（{wrong / trials:.3%}）')

    print('二、德意志線路：四種黑盒子各問一次（振幅順序 |00⟩ |01⟩ |10⟩ |11⟩，字串 |q1 q0⟩）')
    for name, f0, f1 in BOXES:
        steps = deutsch(f0, f1)
        print(f'  {name}（{kind([f0, f1])}）')
        for tag, s in steps:
            print(f'    {tag}：{show(s)}   量 q0 得到 1 的機率 {p_q0_is_1(s):.2f}')
        verdict = '常數' if p_q0_is_1(steps[-1][1]) < 0.5 else '平衡'
        print(f'    判讀：q0 = {0 if verdict == "常數" else 1} → {verdict} {"✓" if verdict == kind([f0, f1]) else "✗"}（只問了黑盒子 1 次）')

    print('三、8 顆球的版本：3 個輸入位元、8 條路')
    MACHINES = [('常數 全紅', [0] * 8), ('常數 全綠', [1] * 8),
                ('平衡 紅綠紅綠紅綠紅綠', [0, 1] * 4), ('平衡 紅綠綠紅綠紅紅綠', [0, 1, 1, 0, 1, 0, 0, 1]),
                ('沒守承諾 5 綠 3 紅', [1, 1, 0, 1, 1, 0, 1, 0])]
    for name, c in MACHINES:
        amps = eight(c)
        signs = ''.join('+' if x == 0 else '−' for x in c)
        hits = '、'.join(f'{y:03b}：{a * a:.1%}' for y, a in enumerate(amps) if abs(a) > 1e-9)
        print(f'  {name}')
        print(f'    每條路的章 {signs}   |000⟩ 的振幅 {amps[0]:+.3f} → P(000) = {amps[0] ** 2:.3f}')
        print(f'    最後量到：{hits}   判讀：{"全 0 → 常數" if amps[0] ** 2 > 0.999 else "一定有 1 → 平衡" if amps[0] ** 2 < 1e-9 else "有時全 0、有時有 1：判不準"}')

    # 四、改造區：設計自己的 8 顆球。紅寫 0、綠寫 1，先預測 P(000)，再執行
    MY_BALLS = [0, 0, 1, 1, 1, 1, 0, 0]
    amps = eight(MY_BALLS)
    print('四、改造區')
    print(f'  我的 8 顆球 {MY_BALLS}（{kind(MY_BALLS)}）   正號 {MY_BALLS.count(0)} 條、負號 {MY_BALLS.count(1)} 條')
    print(f'    |000⟩ 的振幅 = ({MY_BALLS.count(0)} − {MY_BALLS.count(1)}) / 8 = {amps[0]:+.3f} → P(000) = {amps[0] ** 2:.3f}')
    print('    最後量到：' + '、'.join(f'{y:03b}：{a * a:.1%}' for y, a in enumerate(amps) if abs(a) > 1e-9))
'''

QISKIT_PROGRAM = '''"""父子科技學院 量子電腦學程 Q119：用本機 Qiskit 重現德意志演算法與 8 顆球的版本（選用，不需要帳號）

安裝（只要一次）：  pip install qiskit
執行：              python qiskit_check.py
"""
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler


def deutsch(box):
    """兩顆位元：q0 輸入、q1 輔助；box 是黑盒裡的閘（和 basic-circuits.html#deutsch 相同）"""
    qc = QuantumCircuit(2, 1)
    qc.x(1)
    qc.h([0, 1])
    if box in ('x', '1-x'):
        qc.cx(0, 1)
    if box in ('1', '1-x'):
        qc.x(1)
    qc.h(0)
    qc.measure(0, 0)
    return qc


def eight(colors):
    """8 顆球：3 個輸入位元 q0–q2，輔助位元 q3。第 x 顆是綠色（1）就讓那一條路翻轉輔助位元"""
    qc = QuantumCircuit(4, 3)
    qc.x(3)
    qc.h(range(4))
    for x, c in enumerate(colors):
        if c:
            ctrl = [q for q in range(3) if not (x >> q) & 1]
            if ctrl:
                qc.x(ctrl)
            qc.mcx([0, 1, 2], 3)
            if ctrl:
                qc.x(ctrl)
    qc.h(range(3))
    qc.measure(range(3), range(3))
    return qc


sampler = StatevectorSampler(seed=2026)
for box, name in (('0', 'f(x)=0'), ('1', 'f(x)=1'), ('x', 'f(x)=x'), ('1-x', 'f(x)=1−x')):
    counts = sampler.run([deutsch(box)], shots=1000).result()[0].data.c.get_counts()
    print(f'{name:<8} 量 q0 1000 次：{dict(sorted(counts.items()))}')
for name, c in (('常數 全綠', [1] * 8), ('平衡 紅綠紅綠紅綠紅綠', [0, 1] * 4), ('平衡 紅綠綠紅綠紅紅綠', [0, 1, 1, 0, 1, 0, 0, 1]),
                ('沒守承諾 5 綠 3 紅', [1, 1, 0, 1, 1, 0, 1, 0])):
    counts = sampler.run([eight(c)], shots=1000).result()[0].data.c.get_counts()
    print(f'{name}：量 1000 次，全 0（000）出現 {counts.get("000", 0)} 次；最多的是 {max(counts, key=counts.get)}')
print(deutsch('1-x').draw())
'''

JUDGE = [  # (黑盒子, 第 1 次搖, 第 2 次搖, 類型, 黑盒裡的閘, 第 4 步剩下的柱子, 量 q0)
    ('f(x)=0', '紅 0', '紅 0', '常數', '什麼都沒有', '|00⟩ 朝上、|10⟩ 朝下', '0（100%）'),
    ('f(x)=1', '綠 1', '綠 1', '常數', 'X(q1)', '|00⟩ 朝下、|10⟩ 朝上', '0（100%）'),
    ('f(x)=x', '紅 0', '綠 1', '平衡', 'CNOT(q0 → q1)', '|01⟩ 朝上、|11⟩ 朝下', '1（100%）'),
    ('f(x)=1−x', '綠 1', '紅 0', '平衡', 'CNOT 再 X(q1)', '|01⟩ 朝下、|11⟩ 朝上', '1（100%）'),
]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q119：範例 6 Deutsch——紅綠球搖獎機（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。這一課是模組「動手寫量子電路：從八個範例到自己的線路」的範例 6。
上一課（Q118）用一對糾纏位元把狀態搬到遠方；今天玩偵探辦案：搖獎機是嫌疑犯，偵探要判斷它是「常數」（全同色）還是「平衡」（剛好一半一半）。
核心一句話：**問對問題，一次就夠。德意志的線路不問每一顆球的顏色，只問「一樣不一樣」（f(0) ⊕ f(1)）；量 q0：0 = 常數、1 = 平衡，四種黑盒都 100%。**
（Q107 已用 transmon-3d 自由實驗看過相位回踢與盲測；這一課改從紅綠球、古典搖球次數、8 顆球的相長相消與三個限制切入。）

## 紅綠球變成數學（《量子金魚》008 第 5–6 頁）

x = 第幾次搖、f(x) = 搖出的顏色：紅 = 0、綠 = 1。兩顆球時只有四種機器：

| 黑盒子 | 第 1 次搖 f(0) | 第 2 次搖 f(1) | 類型 | 黑盒裡的閘 | 第 4 步剩下的柱子 | 量 q0 |
|---|---|---|---|---|---|---|
''' + ''.join(f'| {" | ".join(r)} |\n' for r in JUDGE) + '''
這就是作品「四種黑盒判讀表」的答案。判讀只看柱子在哪兩格（q0 = 0 還是 1），不看朝上朝下：f(x)=1、f(x)=1−x 多一個整體負號，量不出來。

## 古典偵探要搖幾次（第 7、8、10 頁）

- 兩顆球：搖 1 次只看到一種顏色，什麼都不能判斷，一定要 2 次。
- 很多顆球、搖出不放回：運氣好第 2 顆就換色（平衡）；運氣最差要搖「球數的一半 + 1」：8 顆 5 次、50 顆 26 次、100 萬顆 500,001 次。
- 量子：不管幾顆球，只問黑盒子 1 次（8 顆球要 3 個輸入位元，100 萬顆約 20 個）。

## 德意志線路（basic-circuits.pptx 第 18 頁、basic-circuits.html#deutsch）

q0 是輸入、q1 是輔助位元，兩條線都從 |0⟩ 出發：① X(q1) ② 兩顆都做 H ③ 黑盒 U_f（只問這一次）④ q0 再做 H，量 q0。
動畫裡如果停在第 3 步就量（少了最後的 H），四種黑盒子都是 0、1 各一半，分不出來：光有疊加不夠，最後的 H 讓答案互相加強或抵消。

## 8 顆球：相長與相消（《量子金魚》008 第 25 頁、operation.html#interference 模式 B）

3 個輸入位元 → 8 條路。黑盒子在每條路蓋一個章：紅球 +、綠球 −。最後全部匯到 |000⟩：
- 全同色：8 個章同號，互相加強（相長），P(000) = 1 → 量到全 0 → 常數。
- 4 紅 4 綠：4 正 4 負，互相抵消（相消），P(000) = 0 → 一定有 1 → 平衡。落點依排法不同（紅綠交錯落在 001；紅綠綠紅綠紅紅綠落在 111）。
- 古典最壞要查 2ⁿ⁻¹ + 1 = 5 次。

## 三個誠實的限制（《量子金魚》008 第 27 頁；驗收要孩子說出至少一個）

1. 有承諾的問題：只能是全同色或剛好一半一半。5 綠 3 紅這種「沒守承諾」的機器，全 0 出現的機率是 1/16，判不準。
2. 古典也不差：允許一點點出錯，隨機搖 10 顆都同色就判常數，猜錯機率 2 × (1/2)^10 ≈ 0.2%（不到千分之二）。量子的優勢在「100% 確定、只問 1 次」。
3. 實機有雜訊，要重複跑很多次看統計；Deutsch 1985 年的原始版本只有一半機會成功，1998 年 Cleve 等人才改成今天這個 100% 的版本。
另外：Deutsch 解的是「玩具問題」，沒有實用價值，價值在觀念（只問全域性質）。

## 影片的念法

Deutsch 念「德意志」；H「哈達瑪閘」、X「翻轉閘」、CNOT「受控反閘」；q0、q1 念「編號零」「編號一」；|000⟩ 念「全零」；f(x)=1−x 念「先綠後紅」等顏色說法。

## 兩小時

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片；說明偵探辦案規則 | 影片、列印包第 2 頁 |
| 10–25 | 對照《量子金魚》第 5–10、25、27 頁與 basic-circuits.pptx 第 18–20 頁 | 簡報 |
| 25–65 | 卡片搖球（古典偵探）；在 basic-circuits.html#deutsch 四種函數輪流跑、量 1,000 次；填判讀表 | `01_操作步驟.md`、列印包第 1、2 頁 |
| 65–75 | 休息 | |
| 75–105 | 孩子設計 8 顆球的搖獎機：先預測 P(000)，再跑 deutsch_lab.py；在 operation.html#interference 模式 B 對照 | 列印包第 3 頁、`03_四種黑盒判讀表.csv` |
| 105–115 | 孩子教爸爸：問法、判讀、限制 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 下載學程的 `animations/` 資料夾，用瀏覽器開 `basic-circuits.html#deutsch`（上方「黑盒裡的函數」四個選項）與 `operation.html#interference`（左邊面板按「3 位元：8 條路徑（Deutsch–Jozsa）」）。
- 打開 `slides/output/qfish008-deutsch-algorithm.pptx`（課綱寫 p5–25；本課另用第 27 頁的三個限制）與 `slides/output/basic-circuits.pptx` 第 18–20 頁。
- 準備兩張（下半場可加到八張）一面紅、一面綠的卡片或紙杯，用來玩古典偵探。
- 列印 `02_列印包_四種黑盒判讀表.pdf`（A4，共 4 頁）。
- 有 Python 的電腦先跑一次 `python deutsch_lab.py`；想用 Qiskit 的再 `pip install qiskit` 後跑 `python qiskit_check.py`（選用，不需帳號）。

## 誠實說明

- 量 1,000 次的次數是隨機的；四種黑盒在最後一步是 100%，所以次數固定，第 3 步的一半一半則每次略有不同。
- 振幅柱子是模擬器才看得到的；真實的量子電腦只給量測結果，而且有雜訊。
- 卡片搖球是本課設計的古典活動，不是《量子金魚》節目內容。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：古典偵探，再換量子偵探（約 40 分鐘）

1. 古典偵探：爸爸把兩張卡片排好（紅紅、綠綠、紅綠、綠紅選一種），蓋住。孩子一次翻一張，記下翻幾張才能說出常數或平衡（答案：一定要 2 張）。四種都玩一次。
2. 打開 `animations/basic-circuits.html#deutsch`（範例 6）。上方「黑盒裡的函數」預設是 f(x)=x。
3. 選 f(x)=0：頁面直接跳到第 4 步。看柱子：|00⟩ 朝上、|10⟩ 朝下。按「量測 1,000 次」：全部 0，綠字「→ 常數函數」。
4. 依序換 f(x)=1、f(x)=x、f(x)=1−x，每一種都量 1,000 次。把柱子位置與量到的數字填進列印包第 1 頁。
5. 想看「少了最後一步」：選好函數後點電路下方右邊第 4 個小圓點（停在第 3 步），量 1,000 次：0、1 各約一半，沒有判定；按「下一步 ▶」再量，才是 100%。
6. 想逐步看：選函數後按「⏮ 起點」，再一路按「下一步 ▶」。

## 下半場：8 顆球的搖獎機（約 30 分鐘）

1. 在列印包第 3 頁設計自己的 8 顆球（紅 0、綠 1），先數正號、負號各幾條，預測 P(000)。
2. 打開 `deutsch_lab.py` 最下面的改造區，把 `MY_BALLS` 改成你的設計，執行 `python deutsch_lab.py`，看第四段。
3. 對照第三段：全紅、全綠 P(000) = 1；兩種一半一半 P(000) = 0，落點分別是 001、111；5 綠 3 紅（沒守承諾）P(000) = 0.062。
4. 打開 `animations/operation.html#interference`，左邊面板按「3 位元：8 條路徑（Deutsch–Jozsa）」，再按「常數 f = 0」「常數 f = 1」「平衡 f = x₀」「平衡 f = 奇偶」：看中間 8 支箭頭朝左朝右、右上 P(000)、右下的長條圖落在哪裡。
5. 有裝 Qiskit 的話，跑 `qiskit_check.py`：四種黑盒子 1000 次全是 0、0、1、1；8 顆球的平衡版全 0 出現 0 次。
''',

'deutsch_lab.py': PROGRAM,
'qiskit_check.py': QISKIT_PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n## deutsch_lab.py 實跑輸出（Python 3.13.18，random.Random(1119)）\n\n```\n' + RUN_OUTPUT + '```\n\n'
  '## qiskit_check.py 實跑輸出（qiskit 2.6.2，StatevectorSampler seed=2026）\n\n```\n' + QISKIT_OUTPUT + '```\n\n'
  '## 常見問題\n\n'
  '- 量子偵探問的是什麼？不是 f(0) 或 f(1) 各是多少，而是兩個一不一樣（f(0) ⊕ f(1)）。所以只要問一次，但也只知道「常數或平衡」，不知道是哪一種顏色。\n'
  '- 為什麼量到 0 就是常數？常數時兩條路的正負號相同，最後的 H 讓通往 1 的路互相抵消；平衡時正負號相反，換成通往 0 的路抵消。\n'
  '- 為什麼 f(x)=1 和 f(x)=0 的柱子上下顛倒，結果卻一樣？那是整個狀態一起多一個負號（整體相位），量不出來。\n'
  '- 第 3 步就量會怎樣？0、1 各一半，常數和平衡看起來一樣（第二段第 ②、③ 步的機率都是 0.50）。\n'
  '- 8 顆球全 0 的機率怎麼算？|000⟩ 的振幅 = (正號條數 − 負號條數) / 8，平方就是機率。4 正 4 負 → 0；8 正或 8 負 → 1；5 負 3 正 → (3 − 5)/8 = −0.25 → 0.0625。\n'
  '- 古典最壞要幾次？球數的一半 + 1；8 顆 5 次、50 顆 26 次。允許出錯時隨機搖 10 顆，猜錯機率約 0.2%。\n'
  '- 改造區預設 [0, 0, 1, 1, 1, 1, 0, 0]：4 正 4 負，平衡，P(000) = 0，落在 110。\n'
  '- 下一課 Q120：範例 7 BV——查一次讀出整串密碼。\n',

'05_線路動畫導覽.md': '''# 線路動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路、伺服器或帳號（operation.html 需要能載入 three.js）。

## `animations/basic-circuits.html#deutsch`（範例 6 Deutsch）

- 上方「黑盒裡的函數」：f(x)=0、f(x)=1、f(x)=x（預設）、f(x)=1−x。換選項時頁面停在最後一步並清除量測。
- 電路：q0 輸入、q1 輔助；四步依序是 X、兩個 H、虛線框「黑盒 U_f」、q0 的 H；只量 q0。
- 「⏮ 起點」「◀ 上一步」「▶ 播放」「下一步 ▶」，右邊 5 個小圓點可直接跳到起點或某一步。
- 「振幅與機率」：4 根柱子，字串是 |q1 q0⟩；藍色正振幅、橘色負振幅；下面兩顆 Bloch 球「單看 q0」「單看 q1」。
- 「量測 1 次」「量測 1,000 次」「清除」：只在最後一步量測時出現綠字「→ 常數函數」或「→ 平衡函數」。

## `animations/operation.html#interference`（場景 8：干涉）

- 左邊面板按「3 位元：8 條路徑（Deutsch–Jozsa）」：|000⟩ → 8 個中間圓圈 → 大圓「結果 |000⟩」。
- 函數按鈕：「常數 f = 0」「常數 f = 1」「平衡 f = x₀」「平衡 f = 奇偶」「隨機（非保證）」（每按一次重新隨機，不保證是常數或平衡）。
- 中間金色箭頭朝右 = 正號、朝左 = 負號；右上金字 P(000)；右下「最後量測的機率分佈（8 種結果）」；面板下方寫著完全相長／完全相消與「古典最壞要查 2ⁿ⁻¹+1 = 5 次」。
''',
}

SHEET_HEADER = ['黑盒子', '第 1 次搖', '第 2 次搖', '類型', '古典要翻幾張', '黑盒裡的閘', '第 4 步剩下的柱子', '量 q0 1,000 次', '我的推理']
SHEET_ROWS = [['範例：f(x)=0', '紅 0', '紅 0', '常數', '2', '什麼都沒有', '|00⟩ 朝上、|10⟩ 朝下', '0 有 1000 次', '同色 → 通往 1 的路抵消'],
              ['f(x)=1', '', '', '', '', '', '', '', ''], ['f(x)=x', '', '', '', '', '', '', '', ''], ['f(x)=1−x', '', '', '', '', '', '', '', ''],
              ['8 顆球：我的設計', '', '', '', '', '', '', '', '']]

EXTRA_CSS = '''table.judge td{height:10mm;font-size:11pt}table.judge td.k{font-weight:bold;color:#0b2540;width:16%}
table.judge th{font-size:10.5pt}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.balls{display:flex;gap:3mm;margin:3mm 0}.ball{flex:1;border:1.5pt dashed #4a6a85;border-radius:50%;height:16mm;text-align:center;line-height:16mm;font-size:12pt;color:#4a6a85}
pre.code{font-size:9.5pt;background:#f2f6fa;border:1pt solid #cfdde8;padding:3mm;margin:2mm 0;white-space:pre-wrap}'''


def check_program():
    """真的跑一次 deutsch_lab.py（隔離模式），確認輸出和影片、教材寫的結果一致。"""
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / 'deutsch_lab.py'
        p.write_text(PROGRAM, encoding='utf-8')
        out = subprocess.run([sys.executable, '-I', str(p)], capture_output=True, text=True, check=True,
                             env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}).stdout
    assert out == RUN_OUTPUT, out
    return out


def html():
    row = lambda k: f'<tr><td class="k">{k}</td><td></td><td></td><td></td><td></td><td></td></tr>'  # noqa: E731
    clue = lambda k: f'<tr><td class="k">{k}</td><td></td><td></td><td></td></tr>'  # noqa: E731
    mine = lambda k: f'<tr><td class="k">{k}</td><td></td><td></td><td></td><td></td></tr>'  # noqa: E731
    pages = [
        '<h2>四種黑盒判讀表</h2><p class="lead">basic-circuits.html#deutsch：選函數 → 頁面跳到第 4 步 → 量測 1,000 次。紅 = 0、綠 = 1。</p>'
        '<table class="judge"><tr><th style="width:16%">黑盒子</th><th>兩顆球的顏色</th><th>常數或平衡</th><th>黑盒裡的閘</th><th>第 4 步剩下哪兩根柱子</th><th>量 q0 1,000 次</th></tr>'
        + row('f(x)=0') + row('f(x)=1') + row('f(x)=x') + row('f(x)=1−x') + '</table>'
        '<p>f(x)=0 和 f(x)=1 的柱子有什麼不一樣？為什麼量起來一樣？</p><div class="line"></div>'
        '<p>停在第 3 步（還沒做最後的 H）量 1,000 次，會看到什麼？＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p>'
        '<p>我的推理：量子偵探只問一次，憑什麼說它是常數還是平衡？</p><div class="line"></div>',
        '<h2>偵探辦案：古典偵探的卡片遊戲</h2><p class="lead">爸爸排好卡片並蓋住；你一次翻一張，記下翻到第幾張才敢破案。</p>'
        '<table class="judge"><tr><th style="width:16%">機器</th><th>翻開的順序</th><th>第幾張破案</th><th>常數或平衡</th></tr>'
        + clue('第 1 台') + clue('第 2 台') + clue('第 3 台') + clue('第 4 台') + '</table>'
        '<p>兩張卡片：翻 1 張能破案嗎？為什麼？</p><div class="line"></div>'
        '<p>50 顆球、搖出不放回：運氣最好第＿＿顆破案；運氣最差要搖＿＿顆。100 萬顆呢？＿＿＿＿＿＿</p>'
        '<p>量子偵探不管幾顆球，都只問＿＿次。</p>',
        '<h2>換你改造：8 顆球的搖獎機</h2><p class="lead">在球裡寫紅或綠，先預測，再用 deutsch_lab.py 驗證。|000⟩ 的振幅 = (正號條數 − 負號條數) / 8。</p>'
        '<div class="balls"><div class="ball">0</div><div class="ball">1</div><div class="ball">2</div><div class="ball">3</div>'
        '<div class="ball">4</div><div class="ball">5</div><div class="ball">6</div><div class="ball">7</div></div>'
        '<table class="judge"><tr><th style="width:22%">機器</th><th>正號／負號</th><th>預測 P(000)</th><th>程式的 P(000)</th><th>最後量到</th></tr>'
        + mine('全紅') + mine('紅綠紅綠紅綠紅綠') + mine('5 綠 3 紅') + mine('我的設計') + '</table>'
        '<p>哪裡互相加強（相長）、哪裡互相抵消（相消）？</p><div class="line"></div>'
        '<pre class="code"># deutsch_lab.py 最下面的改造區：紅寫 0、綠寫 1\n'
        'MY_BALLS = [0, 0, 1, 1, 1, 1, 0, 0]\n'
        '# 改完先預測 P(000)，再執行 python deutsch_lab.py</pre>',
        '<h2>最後一關：教爸爸破案</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　版本：＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 量子偵探問的是什麼問題（不看稿）：</p><div class="line"></div>'
        '<p>2. 為什麼量到 0 是常數、量到 1 是平衡：</p><div class="line"></div>'
        '<p>3. 一個限制或容易錯的地方：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><ul class="chk">'
        '<li>說出：不問顏色，只問兩顆一樣不一樣</li><li>說出：線路四步 X、H、黑盒一次、H，量 q0</li>'
        '<li>說出：8 顆球全同色相長、一半一半相消</li><li>指出：有承諾的玩具問題；古典允許出錯也很準；實機要重複跑</li>'
        '<li>完成四種黑盒判讀表，和 deutsch_lab.py 一致</li><li>錄音總結、替作品命名、存一個版本</li></ul></div>',
    ]
    return printpack.document('Q119 四種黑盒判讀表 列印包', '父子科技學院 量子電腦學程 Q119｜範例 6：Deutsch——紅綠球搖獎機', pages, EXTRA_CSS)


if __name__ == '__main__':
    check_program()
    classroom_pack.build(
        slug='q119-deutsch-ball-machine', folder='Q119_範例6_Deutsch_紅綠球搖獎機', files=FILES,
        sheet=('03_四種黑盒判讀表.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_四種黑盒判讀表.pdf', pack_pages=4,
        pack_needles=('四種黑盒判讀表', '古典偵探', '8 顆球', 'MY_BALLS', '最後一關'),
        authoring_dir=XINEW / 'authoring/q119', episode_dir='specials/q119-deutsch-ball-machine',
        extra={'activityMinutes': 120, 'needsAccount': False,
               'needsInstall': 'no（瀏覽器開動畫；deutsch_lab.py 只需 Python 3；qiskit_check.py 選用：pip install qiskit）',
               'program': 'deutsch_lab.py', 'optionalProgram': 'qiskit_check.py',
               'testedWith': 'Python 3.13.18 (standard library only, random seed 1119); qiskit 2.6.2',
               'recordedRun': {'classicalWorst': {'2': 2, '8': 5, '50': 26, '1000000': 500001},
                               'randomTen': 0.00195, 'simulatedWrong1119': 191,
                               'deutschQ0': {'f(x)=0': 0, 'f(x)=1': 0, 'f(x)=x': 1, 'f(x)=1−x': 1},
                               'eightBallP000': {'全紅': 1.0, '全綠': 1.0, '紅綠紅綠紅綠紅綠': 0.0, '紅綠綠紅綠紅紅綠': 0.0, '5綠3紅': 0.0625},
                               'eightBallLanding': {'紅綠紅綠紅綠紅綠': '001', '紅綠綠紅綠紅紅綠': '111'}},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q119/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')
