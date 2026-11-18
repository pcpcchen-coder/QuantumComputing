"""Q111 課堂教材：七層堆疊說明卡、可執行的 stack_race.py、效能競賽計分表、容易錯的地方、最後一關檢核表與解答。

不需要帳號，也不需要安裝套件：動畫用瀏覽器開 animations/transmon-3d.html#stack（第 12 章）與 operation.html#workflow；程式只要 Python 3。
建置時會真的執行一次 stack_race.py，確認輸出和影片、教材寫的結果一致。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q111/classroom.py
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
RUN_OUTPUT = '''一、原生閘驗算（只差一個整體相位就算相同）
  H = Rz(π/2)·√X·Rz(π/2)：相同 ✓
  X = √X·√X：相同 ✓
  CNOT = H·CZ·H（H 做在目標）：相同 ✓
  SWAP = 3 個 CNOT：相同 ✓
二、效能競賽（總時間含讀取 600 ns；√X 32 ns、Rz 0 ns、CZ 48 ns）
  Bell @ 直線 5 顆：SWAP 0 個，CZ 1 → 1 個，√X 3 個，總時間 712 ns，結果和原始電路相同 ✓
  Bell @ 方格 3×3：SWAP 0 個，CZ 1 → 1 個，√X 3 個，總時間 712 ns，結果和原始電路相同 ✓
  GHZ（3 位元） @ 直線 5 顆：SWAP 0 個，CZ 2 → 2 個，√X 5 個，總時間 760 ns，結果和原始電路相同 ✓
  GHZ（3 位元） @ 方格 3×3：SWAP 0 個，CZ 2 → 2 個，√X 5 個，總時間 760 ns，結果和原始電路相同 ✓
  BV（s = 111） @ 直線 5 顆：SWAP 2 個，CZ 3 → 9 個，√X 19 個，總時間 1320 ns，結果和原始電路相同 ✓
  BV（s = 111） @ 方格 3×3：SWAP 0 個，CZ 3 → 3 個，√X 9 個，總時間 840 ns，結果和原始電路相同 ✓
三、聰明一點的路由：BV 在直線晶片上，三個 CNOT 換順序
  CNOT(0→3) → CNOT(1→3) → CNOT(2→3)：SWAP 2 個，CZ 9 個，總時間 1320 ns，結果相同 ✓
  CNOT(0→3) → CNOT(2→3) → CNOT(1→3)：SWAP 2 個，CZ 9 個，總時間 1288 ns，結果相同 ✓
  CNOT(1→3) → CNOT(0→3) → CNOT(2→3)：SWAP 1 個，CZ 6 個，總時間 1112 ns，結果相同 ✓
  CNOT(1→3) → CNOT(2→3) → CNOT(0→3)：SWAP 1 個，CZ 6 個，總時間 1080 ns，結果相同 ✓
  CNOT(2→3) → CNOT(0→3) → CNOT(1→3)：SWAP 1 個，CZ 6 個，總時間 1080 ns，結果相同 ✓
  CNOT(2→3) → CNOT(1→3) → CNOT(0→3)：SWAP 1 個，CZ 6 個，總時間 1112 ns，結果相同 ✓
四、七層堆疊說明卡：GHZ（3 位元） @ 直線 5 顆（MY_CIRCUIT、MY_CHIP）
  ① 應用層：H(0) CX(0,1) CX(0,2) M(0,1,2)
  ② 電路 IR：4 個邏輯操作，還沒指定晶片
  ③ 編譯器：分解成 2 個 CZ；映射 q0→Q2、q1→Q1、q2→Q3；插 0 個 SWAP；抵消 0 對 H·H；剩 √X 5、Rz 10、CZ 2
  ④ 脈衝層：√X 變成 32 ns 的微波脈衝、CZ 變成 48 ns 的磁通脈衝、Rz 只改相位（0 ns）；閘在 160 ns 做完，讀取到 760 ns
  ⑤ 即時控制：控制電子照時間軸同步播放、讀取；動態電路要在幾百 ns 內判斷並回饋
  ⑥ 類比硬體：數位波形 → 混頻 → 冷凍機 → 晶片 → 放大 → 數位化
  ⑦ 結果處理：理想機率 {'000': 0.5, '111': 0.5}；實際要重跑數千次，再修正讀取誤差
'''

PROGRAM = r'''"""父子科技學院 量子電腦學程 Q111：編譯與控制軟體堆疊——效能競賽（純 Python，不需要安裝任何套件）

執行：  python stack_race.py
一、原生閘驗算：H、CNOT、SWAP、X 換成 Rz、√X、CZ 以後，矩陣真的一樣（只差一個整體相位）。
二、效能競賽：Bell、GHZ、BV 放到「直線 5 顆」與「方格 3×3」兩種晶片，比較 SWAP 數、CZ 數與總時間。
    編譯步驟照 animations/transmon-3d.html 第 12 章的程式改寫（分解 → 映射 → 路由 → 最佳化 → 排程），數字應和動畫面板一樣；
    最後把編譯好的實體電路真的模擬一次，確認結果和原始電路相同。
三、聰明一點的路由：BV 的三個 CNOT 目標相同、可以交換順序，試遍所有順序，找最少 SWAP。
四、七層堆疊說明卡：MY_CIRCUIT 在 MY_CHIP 上，每一層做了什麼。
"""
import cmath
import math
from itertools import permutations, product

# 改造區 1：選一個電路（'bell'、'ghz'、'bv'）
MY_CIRCUIT = 'ghz'
# 改造區 2：選一種晶片（'line' 直線 5 顆、'grid' 方格 3×3）
MY_CHIP = 'line'

# ---------- 晶片與（固定的）校準資料：和動畫第 12 章相同 ----------
CHIPS = {
    'line': ('直線 5 顆', 5, [(0, 1), (1, 2), (2, 3), (3, 4)]),
    'grid': ('方格 3×3', 9, [(0, 1), (1, 2), (3, 4), (4, 5), (6, 7), (7, 8), (0, 3), (3, 6), (1, 4), (4, 7), (2, 5), (5, 8)]),
}
ERR1 = [0.031, 0.024, 0.018, 0.022, 0.045, 0.027, 0.019, 0.035, 0.028]          # 單位元閘錯誤率（%）
ERR2 = {'0-1': 0.62, '1-2': 0.48, '2-3': 0.55, '3-4': 1.10, '3-4g': 0.71, '4-5': 0.52, '6-7': 0.66, '7-8': 0.58,
        '0-3': 0.74, '3-6': 0.61, '1-4': 0.45, '4-7': 0.69, '2-5': 0.57, '5-8': 0.83}   # CZ 錯誤率（%）
DUR = {'SX': 32, 'RZ': 0, 'CZ': 48, 'M': 600}                                    # 每種原生操作花幾 ns
CIRCUITS = {
    'bell': ('Bell', 2, [('H', 0), ('CX', 0, 1), ('M', 0, 1)]),
    'ghz': ('GHZ（3 位元）', 3, [('H', 0), ('CX', 0, 1), ('CX', 0, 2), ('M', 0, 1, 2)]),
    'bv': ('BV（s = 111）', 4, [('X', 3), ('H', 3), ('H', 0), ('H', 1), ('H', 2), ('CX', 0, 3), ('CX', 1, 3), ('CX', 2, 3),
                               ('H', 0), ('H', 1), ('H', 2), ('M', 0, 1, 2)]),
}


def e2(chip, a, b):
    k = f'{min(a, b)}-{max(a, b)}'
    return ERR2['3-4g'] if chip == 'grid' and k == '3-4' else ERR2.get(k, 1)


def compile_circuit(ck, chip, ops=None):
    name, n, ops0 = CIRCUITS[ck]
    ops0 = ops or ops0
    cname, N, edges = CHIPS[chip]
    adj = [[] for _ in range(N)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    dist = []
    for s in range(N):
        d = [99] * N
        d[s], q = 0, [s]
        while q:
            u = q.pop(0)
            for v in adj[u]:
                if d[v] == 99:
                    d[v] = d[u] + 1
                    q.append(v)
        dist.append(d)

    def next_hop(s, t):
        return next(v for v in adj[s] if dist[v][t] == dist[s][t] - 1)

    # ① 分解：CX → H·CZ·H，X → √X·√X
    st1 = []
    for o in ops0:
        if o[0] == 'CX':
            st1 += [('H', o[2]), ('CZ', o[1], o[2]), ('H', o[2])]
        elif o[0] == 'X':
            st1 += [('SX', o[1]), ('SX', o[1])]
        else:
            st1.append(o)
    # ② 映射：試遍所有配置，成本 = SWAP 需求 × 10 + 用到的連線與位元的錯誤率（挑最小的）
    pairs = [o[1:] for o in ops0 if o[0] == 'CX']
    best = None
    for L in permutations(range(N), n):
        cost = sum((dist[L[a]][L[b]] - 1) * 10 + (e2(chip, L[a], L[b]) if dist[L[a]][L[b]] == 1 else 1.5) for a, b in pairs)
        cost += sum(ERR1[p] * 2 for p in L)
        if best is None or cost < best[0] - 1e-9:
            best = (cost, list(L))
    L0 = best[1]
    # ③ 路由：CX 兩端不相鄰，就把一端沿最短路徑搬一步（插一個 SWAP），選「之後所有 CX 距離總和」較小的那一端
    L, inv = L0[:], {p: l for l, p in enumerate(L0)}
    routed, n_swap, cx_i = [], 0, 0
    for o in ops0:
        if o[0] == 'CX':
            a, b = o[1], o[2]
            rest = pairs[cx_i:]
            cx_i += 1
            while dist[L[a]][L[b]] > 1:
                cands = []
                for m, nx in ((a, next_hop(L[a], L[b])), (b, next_hop(L[b], L[a]))):
                    T2 = L[:]
                    if nx in inv:
                        T2[inv[nx]] = L[m]
                    T2[m] = nx
                    cands.append((sum(dist[T2[u]][T2[v]] for u, v in rest), m, nx))
                c, m, nx = min(cands, key=lambda x: x[0])
                pa, other = L[m], inv.get(nx)
                routed.append(('SWAP', pa, nx))
                n_swap += 1
                L[m], inv[nx] = nx, m
                if other is not None:
                    L[other], inv[pa] = pa, other
                else:
                    del inv[pa]
            routed.append(('CX', L[a], L[b]))
        else:
            routed.append((o[0],) + tuple(L[l] for l in o[1:]))
    st3 = []                                              # (閘, 實體位元…, 是否來自 SWAP)

    def cx(c, t, sw):
        st3.extend([('H', (t,), sw), ('CZ', (c, t), sw), ('H', (t,), sw)])
    for o in routed:
        if o[0] == 'SWAP':
            cx(o[1], o[2], 1), cx(o[2], o[1], 1), cx(o[1], o[2], 1)
        elif o[0] == 'CX':
            cx(o[1], o[2], 0)
        elif o[0] == 'X':
            st3 += [('SX', o[1:], 0), ('SX', o[1:], 0)]
        else:
            st3.append((o[0], o[1:], 0))
    # ④ 最佳化：相鄰 H·H 抵消 → H 展開成 Rz(π/2)·√X·Rz(π/2) → 合併相鄰 Rz、刪掉角度 0 的 Rz
    opsx, n_hh, changed = [list(o) for o in st3], 0, True
    while changed:
        changed = False
        for i in range(len(opsx)):
            if opsx[i][0] != 'H':
                continue
            q = opsx[i][1][0]
            for j in range(i + 1, len(opsx)):
                if q not in opsx[j][1]:
                    continue
                if opsx[j][0] == 'H':
                    del opsx[j], opsx[i]
                    changed, n_hh = True, n_hh + 1
                break
            if changed:
                break
    exp = []
    for g, p, sw in opsx:
        if g == 'H':
            exp += [['RZ', p, sw, math.pi / 2], ['SX', p, sw], ['RZ', p, sw, math.pi / 2]]
        else:
            exp.append([g, p, sw])
    st4, last_rz = [], {}
    for o in exp:
        if o[0] == 'RZ':
            k = last_rz.get(o[1][0])
            if k is not None:
                st4[k][3] = (st4[k][3] + o[3]) % (2 * math.pi)
                continue
            last_rz[o[1][0]] = len(st4)
            st4.append(o[:])
            continue
        for q in o[1]:
            last_rz.pop(q, None)
        st4.append(o)
    st4 = [o for o in st4 if not (o[0] == 'RZ' and abs(math.sin(o[3] / 2)) < 1e-9)]
    # ⑤ 排程：每個閘盡早開始；同時進行的 CZ 不可以共用或相鄰（避免頻率碰撞）
    free, czs, sched = [0] * N, [], []
    for o in st4:
        g, p = o[0], o[1]
        t, d = max(free[q] for q in p), DUR[g]
        if g == 'CZ':
            ok = False
            while not ok:
                ok = True
                for zp, zt, zd in czs:
                    near = any(a == b or b in adj[a] for a in p for b in zp)
                    if near and t < zt + zd and zt < t + d:
                        t, ok = zt + zd, False
            czs.append((p, t, d))
        sched.append((o, t, d))
        for q in p:
            free[q] = t + d
    total = max(t + d for o, t, d in sched)
    return {'name': name, 'n': n, 'chip': cname, 'N': N, 'L0': L0, 'Lend': L, 'n_swap': n_swap, 'n_hh': n_hh,
            'ops0': ops0, 'st1': st1, 'cz_raw': sum(o[0] == 'CZ' for o in st1),
            'cz_routed': sum(o[0] == 'CZ' for o in st3), 'sx_routed': sum(o[0] in ('H', 'SX') for o in st3),
            'sx': sum(o[0] == 'SX' for o in st4), 'rz': sum(o[0] == 'RZ' for o in st4), 'cz': sum(o[0] == 'CZ' for o in st4),
            'st4': st4, 'total': total, 'gates_end': max(t + d for o, t, d in sched if o[0] != 'M'),
            'non_adj': sum(1 for o in st1 if o[0] == 'CZ' and dist[L0[o[1]]][L0[o[2]]] > 1)}


# ---------- 狀態向量模擬（驗算用） ----------
S2 = 2 ** -0.5
GATES1 = {'H': [[S2, S2], [S2, -S2]], 'X': [[0, 1], [1, 0]],
          'SX': [[(1 + 1j) / 2, (1 - 1j) / 2], [(1 - 1j) / 2, (1 + 1j) / 2]]}


def rz(th):
    return [[cmath.exp(-0.5j * th), 0], [0, cmath.exp(0.5j * th)]]


def apply1(psi, n, q, U):
    b = 1 << (n - 1 - q)
    for i in range(len(psi)):
        if not i & b:
            x, y = psi[i], psi[i | b]
            psi[i], psi[i | b] = U[0][0] * x + U[0][1] * y, U[1][0] * x + U[1][1] * y


def apply2(psi, n, g, c, t):
    bc, bt = 1 << (n - 1 - c), 1 << (n - 1 - t)
    for i in range(len(psi)):
        if g == 'CZ' and i & bc and i & bt:
            psi[i] = -psi[i]
        if g == 'CX' and i & bc and not i & bt:
            psi[i], psi[i | bt] = psi[i | bt], psi[i]


def probs(psi, n, qubits):
    """量 qubits（依序）得到每個位元串的機率"""
    out = {}
    for i, a in enumerate(psi):
        if abs(a) > 1e-12:
            k = ''.join(str((i >> (n - 1 - q)) & 1) for q in qubits)
            out[k] = out.get(k, 0) + abs(a) ** 2
    return {k: round(v, 6) for k, v in sorted(out.items()) if round(v, 6) > 0}


def ideal(ops, n):
    psi = [0j] * (1 << n)
    psi[0] = 1
    for o in ops:
        if o[0] in GATES1:
            apply1(psi, n, o[1], GATES1[o[0]])
        elif o[0] == 'CX':
            apply2(psi, n, 'CX', o[1], o[2])
    return probs(psi, n, [o for o in ops if o[0] == 'M'][0][1:])


def physical(r):
    """模擬編譯好的實體電路（只用 Rz、√X、CZ），量測位置照路由後的配置"""
    N = r['N']
    psi = [0j] * (1 << N)
    psi[0] = 1
    for o in r['st4']:
        if o[0] == 'RZ':
            apply1(psi, N, o[1][0], rz(o[3]))
        elif o[0] == 'SX':
            apply1(psi, N, o[1][0], GATES1['SX'])
        elif o[0] == 'CZ':
            apply2(psi, N, 'CZ', *o[1])
    m = [o for o in r['ops0'] if o[0] == 'M'][0][1:]
    return probs(psi, N, [r['Lend'][l] for l in m])


# ---------- 一、原生閘驗算 ----------
def mat(ops, n):
    """依序做 ops 的 2^n × 2^n 矩陣（每一欄 = 某個基底態送進去的結果）"""
    cols = []
    for k in range(1 << n):
        psi = [0j] * (1 << n)
        psi[k] = 1
        for o in ops:
            if o[0] == 'RZ':
                apply1(psi, n, o[1], rz(o[2]))
            elif o[0] in GATES1:
                apply1(psi, n, o[1], GATES1[o[0]])
            else:
                apply2(psi, n, o[0], o[1], o[2])
        cols.append(psi)
    return cols


def same_up_to_phase(A, B):
    ph = None
    for ca, cb in zip(A, B):
        for x, y in zip(ca, cb):
            if abs(y) > 1e-9:
                ph = ph or x / y
                if abs(x - ph * y) > 1e-9:
                    return False
            elif abs(x) > 1e-9:
                return False
    return abs(abs(ph) - 1) < 1e-9


def fmt_map(L):
    return '、'.join(f'q{l}→Q{p}' for l, p in enumerate(L))


if __name__ == '__main__':
    print('一、原生閘驗算（只差一個整體相位就算相同）')
    hp = math.pi / 2
    checks = [
        ('H = Rz(π/2)·√X·Rz(π/2)', mat([('H', 0)], 1), mat([('RZ', 0, hp), ('SX', 0), ('RZ', 0, hp)], 1)),
        ('X = √X·√X', mat([('X', 0)], 1), mat([('SX', 0), ('SX', 0)], 1)),
        ('CNOT = H·CZ·H（H 做在目標）', mat([('CX', 0, 1)], 2), mat([('H', 1), ('CZ', 0, 1), ('H', 1)], 2)),
        ('SWAP = 3 個 CNOT', mat([('CX', 0, 1), ('CX', 1, 0), ('CX', 0, 1)], 2),
         [[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]]),
    ]
    for name, A, B in checks:
        print(f'  {name}：{"相同 ✓" if same_up_to_phase(A, B) else "不同 ✗"}')
    print('二、效能競賽（總時間含讀取 600 ns；√X 32 ns、Rz 0 ns、CZ 48 ns）')
    for ck, chip in product(CIRCUITS, CHIPS):
        r = compile_circuit(ck, chip)
        ok = physical(r) == ideal(r['ops0'], r['n'])
        print(f'  {r["name"]} @ {r["chip"]}：SWAP {r["n_swap"]} 個，CZ {r["cz_raw"]} → {r["cz"]} 個，'
              f'√X {r["sx"]} 個，總時間 {r["total"]} ns，結果和原始電路{"相同 ✓" if ok else "不同 ✗"}')
    print('三、聰明一點的路由：BV 在直線晶片上，三個 CNOT 換順序')
    name, n, ops0 = CIRCUITS['bv']
    cxs = [o for o in ops0 if o[0] == 'CX']
    i0 = ops0.index(cxs[0])
    for order in permutations(cxs):
        ops = ops0[:i0] + list(order) + ops0[i0 + 3:]
        r = compile_circuit('bv', 'line', ops)
        ok = physical(r) == ideal(ops, n)
        tag = ' → '.join(f'CNOT({o[1]}→{o[2]})' for o in order)
        print(f'  {tag}：SWAP {r["n_swap"]} 個，CZ {r["cz"]} 個，總時間 {r["total"]} ns，結果{"相同 ✓" if ok else "不同 ✗"}')
    r = compile_circuit(MY_CIRCUIT, MY_CHIP)
    print(f'四、七層堆疊說明卡：{r["name"]} @ {r["chip"]}（MY_CIRCUIT、MY_CHIP）')
    gates = ' '.join(o[0] + '(' + ','.join(map(str, o[1:])) + ')' for o in r['ops0'])
    print(f'  ① 應用層：{gates}')
    print(f'  ② 電路 IR：{len(r["ops0"])} 個邏輯操作，還沒指定晶片')
    print(f'  ③ 編譯器：分解成 {r["cz_raw"]} 個 CZ；映射 {fmt_map(r["L0"])}；插 {r["n_swap"]} 個 SWAP；'
          f'抵消 {r["n_hh"]} 對 H·H；剩 √X {r["sx"]}、Rz {r["rz"]}、CZ {r["cz"]}')
    print(f'  ④ 脈衝層：√X 變成 32 ns 的微波脈衝、CZ 變成 48 ns 的磁通脈衝、Rz 只改相位（0 ns）；'
          f'閘在 {r["gates_end"]} ns 做完，讀取到 {r["total"]} ns')
    print('  ⑤ 即時控制：控制電子照時間軸同步播放、讀取；動態電路要在幾百 ns 內判斷並回饋')
    print('  ⑥ 類比硬體：數位波形 → 混頻 → 冷凍機 → 晶片 → 放大 → 數位化')
    print(f'  ⑦ 結果處理：理想機率 {ideal(r["ops0"], r["n"])}；實際要重跑數千次，再修正讀取誤差')
'''

# 七層堆疊說明卡（作品）：(層, 負責什麼, BV @ 直線 5 顆 的實例) — 解答用；列印包上只留第一欄
LAYERS = [
    ('① 應用／演算法', '用 Qiskit 等套件寫電路', 'X(3)、H×4、CNOT(0→3)、CNOT(1→3)、CNOT(2→3)、H×3、量測'),
    ('② 量子電路 IR', '轉成與硬體無關的 OpenQASM 3／QIR', '12 個邏輯操作，還沒指定晶片'),
    ('③ 編譯器', '分解 → 映射 → 路由 → 最佳化 → 排程', '映射 q0→Q0、q1→Q1、q2→Q3、q3→Q2；2 個 SWAP；CZ 3 → 9；抵消 4 對 H·H'),
    ('④ 脈衝層', '原生閘 → 校準好的波形', '√X 32 ns、CZ 48 ns 磁通脈衝、Rz 0 ns；閘做到 720 ns'),
    ('⑤ 即時控制', 'FPGA 同步播放、讀取、條件回饋', '讀取 600 ns → 判斷約 300 ns → 條件 π 脈衝'),
    ('⑥ 類比硬體', 'DAC → 混頻 → 冷凍機 → 晶片 → 放大 → ADC', '每顆位元 XY、Z、讀取三條線'),
    ('⑦ 結果處理', '判別 0/1、累積數千 shot、修正讀取誤差', '2000 shots，111 最多；總時間 1320 ns'),
]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q111：第 13 課 編譯與控制軟體堆疊（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。這是師生對話的最後一課：前十二課講過的晶片、脈衝、讀取、演算法和錯誤更正，今天用「軟體堆疊」串成一條生產線——一行演算法經過七層，變成某條線上某個奈秒的微波，讀回的訊號再翻回 0 和 1 的統計。課堂用「效能競賽」的方式：同一個電路放到「直線 5 顆」與「方格 3×3」兩種晶片，比 SWAP 數、CZ 數與總時間，最後把每一層做了什麼寫成「七層堆疊說明卡」。

## 需要準備

| 項目 | 說明 |
|---|---|
| 動畫 | 下載學程的 `animations/` 資料夾，用瀏覽器開 `transmon-3d.html#stack`（第 12 章軟體堆疊；步驟 1–8 自動播放，步驟「9」是自由實驗）與 `operation.html#workflow`（場景 12 完整流程）。免安裝、不需帳號 |
| 程式 | `stack_race.py`：只要有 Python 3 就能跑，不需安裝套件、不需帳號 |
| 列印 | `02_列印包_七層堆疊說明卡.pdf`（A4，共 4 頁） |
| 參考 | slides/transmon.pptx 第 26 頁（課綱寫 p27，實際內容在 p26）；slides/QC_Operation_Talk.pptx 第 26 頁「轉譯」；docs/超導量子電腦師生對話教學紀錄.md 第 13 課 |

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片；先猜「你寫的 qc.h(0) 到晶片上會變成什麼？」 | 影片、列印包第 1 頁 |
| 10–25 | 概念示範：七層與兩根支柱、分解、映射、路由、最佳化、排程與脈衝、即時回饋、結果處理與校準 | 影片第 3–9 段、`05_動畫導覽.md` |
| 25–65 | 效能競賽：在第 12 章自由實驗比較直線與方格晶片的 SWAP 數、CZ 數與總時間，填計分表 | `01_操作步驟.md`、列印包第 2 頁、`03_效能競賽計分表.csv` |
| 65–75 | 休息 | |
| 75–105 | 孩子獨立改造：選 Bell、GHZ、BV 其中一個，寫出每一層做了什麼；用程式對答案、改 MY_CIRCUIT 與 MY_CHIP | `stack_race.py`、列印包第 1 頁 |
| 105–115 | 角色互換：孩子教爸爸操作與原理，並指出一個限制 | 列印包第 3、4 頁 |
| 115–120 | 錄音總結、替七層堆疊說明卡命名、存檔 | |

## 課前準備（約 20 分鐘）

- 自己先打開 `transmon-3d.html#stack`，從步驟 1 看到步驟 8（自動接續，約 3 分鐘，左上方字幕逐句說明），再按步驟「9」進自由實驗。
- 在自由實驗選「BV」「直線 5 顆」，連按「下一階段 ▶」看五個階段；再按「方格 3×3」，比較面板的 SWAP 與總時間。
- 按「播放脈衝」看下方時間軸，再按「執行 2000 shots」看直方圖。
- 打開 `operation.html#workflow`，切換「主動重置（量測 + 條件 π 脈衝）」，看右下插圖的時間組成。
- 跑一次 `python stack_race.py`，確認「BV（s = 111） @ 直線 5 顆：SWAP 2 個……總時間 1320 ns」與「方格 3×3：SWAP 0 個……840 ns」。
- 讀一遍 `04_解答.md`。

## 裁判（爸爸）的原則

- 每一場都要說出「為什麼」：為什麼這個晶片要插 SWAP？為什麼 Rz 不算時間？說得出原因才算贏。
- 最重要的一句：晶片的連接方式會大幅改變 SWAP 數與錯誤；同一個電路，編譯得好不好可以差好幾倍的閘數。

## 誠實說明

- 動畫與 `stack_race.py` 的時間是示意值（√X 32 ns、CZ 48 ns、讀取 600 ns）；師生對話紀錄的範圍是 √X 20–40 ns、CZ 40–60 ns、讀取 0.3–1 μs，真實機器依平台與世代而不同。
- 校準資料（每顆位元與每條連線的錯誤率）是動畫裡寫死的範例數字，不是真實晶片的量測值。
- 動畫的路由是「照原順序、每次走一步」的簡單作法；`stack_race.py` 第三段換 CNOT 順序就能少一個 SWAP，真正的編譯器要搜尋這類空間（大電路找最少 SWAP 是 NP-hard，實務上用 SABRE 等啟發式）。
- 「執行 2000 shots」是動畫依理想機率抽樣，再加上每位元 2% 的讀取誤判，每次結果略有不同；`stack_race.py` 只算理想機率，不用亂數。
- `operation.html#workflow` 插圖的重置、閘、讀取時間是典型量級（插圖上寫「依系統而異」）。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：效能競賽（約 40 分鐘）

1. 用瀏覽器開 `animations/transmon-3d.html#stack`（第 12 章）。步驟 1 會自動播放並接續；左上方字幕逐句說明。
2. 步驟 1「全貌」：看板上七層依序亮起，右邊是「自動校準」「錯誤處理」兩根支柱。
3. 步驟 2–5：Bell 的分解與映射，BV 在直線晶片上插 SWAP（紫色）、最佳化（H·H 抵消、Rz 合併）。
4. 步驟 6–8：脈衝時間軸（白色游標）、即時回饋與 2000 shots、校準依賴圖（Ramsey 失敗退回 Rabi）。
5. 按步驟「9」自由實驗：選電路（Bell、GHZ、BV）和晶片（直線 5 顆、方格 3×3），用「◀ 上一階段」「下一階段 ▶」一步步看；每一場把右側面板的「SWAP」「原生閘（最佳化後）」「總時間」填進列印包第 2 頁。
6. 六場比完，圈出每個電路的冠軍晶片，並寫一句「為什麼」。

## 下半場：寫出每一層（約 30 分鐘）

1. 從 Bell、GHZ、BV 挑一個，在自由實驗走完五個階段，再按「播放脈衝」與「執行 2000 shots」。
2. 把每一層做了什麼寫進列印包第 1 頁「七層堆疊說明卡」。
3. 打開 `operation.html#workflow`，切換「主動重置（量測 + 條件 π 脈衝）」、拖「shots N」，看一次執行要多久，補在第 ⑤、⑦ 層。
4. 執行 `python stack_race.py`，對照「二、效能競賽」與「四、七層堆疊說明卡」。改 `MY_CIRCUIT = 'ghz'` 成你挑的電路、`MY_CHIP = 'line'` 成 `'grid'`，再跑一次。
5. 看「三、聰明一點的路由」：BV 的三個 CNOT 換順序，直線晶片最少要幾個 SWAP？
''',
}

FILES.update({
'stack_race.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n## 七層堆疊說明卡（以 BV @ 直線 5 顆為例）\n\n| 層 | 負責什麼 | BV @ 直線 5 顆 |\n|---|---|---|\n'
  + ''.join(f'| {a} | {b} | {c} |\n' for a, b, c in LAYERS)
  + '\n兩根支柱：自動校準（讀取腔頻譜 → 位元頻譜 → Rabi → Ramsey → T₁／T₂ → DRAG → 讀取最佳化 → 單位元 RB → CZ 校準 → 雙位元 RB → 頻率配置，失敗就退回上一步）；'
  '錯誤處理（現在是錯誤緩解，容錯時代是表面碼與即時解碼器）。\n'
  '\n## stack_race.py 實跑（Python 3.13.18）\n\n```\n' + RUN_OUTPUT + '```\n\n'
  '- Bell、GHZ 在兩種晶片上都不用 SWAP（GHZ 在直線上把 q0 放在中間的 Q2，兩個鄰居分別放 q1、q2）。\n'
  '- BV 的輔助位元要和 3 顆位元互動；直線晶片每顆最多 2 個鄰居，所以要插 SWAP：2 個 SWAP 讓 CZ 從 3 個變 9 個，總時間 1320 ns。\n'
  '- 方格晶片把輔助位元放在有 3 個鄰居的 Q1，0 個 SWAP，840 ns。\n'
  '- 換 CNOT 順序（同目標可交換）：直線晶片最少 1 個 SWAP、6 個 CZ、1080 ns。\n'
  '- 為什麼 Rz 不算時間？Rz 是虛擬 Z：只改後續脈衝的相位參考，不送任何波形。\n'
  '- 為什麼相鄰的 CZ 不能同時做？會頻率碰撞與串擾（師生對話第 4 課）。\n'
  '- 為什麼先把 CNOT 換成 H·CZ·H，卻等到最佳化才展開 H？保留 H 才看得出相鄰的 H·H 可以抵消。\n'
  '- operation.html#workflow：被動重置 250 μs，一個 shot 253.0 μs，1000 shots 約 253 ms；主動重置 2 μs，一個 shot 5.0 μs，1000 shots 5.0 ms、100,000 shots 500 ms；另加佇列、轉譯、波形載入、網路傳輸（秒～分鐘）。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載整個資料夾後用瀏覽器開啟，不需要網路、伺服器或帳號（transmon-3d 需連網載入 three.js）。

## `transmon-3d.html#stack`（第 12 章：編譯與控制軟體堆疊）

- 畫面：上方看板 A 是電路在每個編譯階段的樣子（青 = 單位元閘、金 = Rz（虛擬 Z，0 ns）、橘 = CZ、紅 = 兩端不相鄰、紫 = SWAP 展開、藍 = 量測）；下方看板 B 是編譯統計、脈衝時間軸或執行結果直方圖；地上是晶片（金色 = 被選中的實體位元，標籤附今天的單位元錯誤率）。
- 步驟 1～9：全貌、分解、映射、路由、最佳化、排程與脈衝、回饋與結果、校準、自由實驗。「◀ 上一步」「暫停」「重播」「下一步 ▶」與「自動接續」。
- 自由實驗：電路「Bell」「GHZ」「BV」；晶片「直線 5 顆」「方格 3×3」；「◀ 上一階段」「下一階段 ▶」「播放脈衝」「執行 2000 shots」。右側面板「電路 @ 晶片」「目前階段」「原生閘（最佳化後）」「SWAP」「總時間」。

## `operation.html#workflow`（場景 12：一次量子計算的完整流程）

- 發光的工作封包依序走過六站：① 寫程式、② 轉譯、③ 脈衝排程、④ 控制電子、⑤ 晶片執行 shots、⑥ 判別與結果。
- 控制項：「自動播放」「下一站 ▶」「shots N」「線路深度（層）」「主動重置（量測 + 條件 π 脈衝）」。
- 右下插圖：一個 shot 的時間組成（重置、閘、讀取）與整個工作的執行時間。

## 操作

滑鼠拖曳旋轉、滾輪縮放；transmon-3d 下方可切換十二章，左右方向鍵也能換章。
''',
})

SHEET_HEADER = ['電路', '晶片', '映射（q→Q）', 'SWAP 數', 'CZ 數（最佳化後）', '總時間（ns）', '冠軍？為什麼']
SHEET_ROWS = [['Bell', '直線 5 顆', '', '', '', '', ''], ['Bell', '方格 3×3', '', '', '', '', ''],
              ['GHZ', '直線 5 顆', '', '', '', '', ''], ['GHZ', '方格 3×3', '', '', '', '', ''],
              ['BV', '直線 5 顆', '', '', '', '', ''], ['BV', '方格 3×3', '', '', '', '', '']]

EXTRA_CSS = '''table.judge td{height:17mm;font-size:11pt}table.judge td.k{font-weight:bold;color:#0b2540}
table.rec td{height:11mm}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
pre.code{font-size:9pt;background:#f2f6fa;border:1pt solid #cfdde8;padding:3mm;margin:2mm 0;white-space:pre-wrap}'''


def check_program():
    """真的跑一次 stack_race.py（隔離模式），確認輸出和影片、教材寫的結果一致。"""
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / 'stack_race.py'
        p.write_text(PROGRAM, encoding='utf-8')
        out = subprocess.run([sys.executable, '-I', str(p)], capture_output=True, text=True, check=True,
                             env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}).stdout
    assert out == RUN_OUTPUT, out
    return out


def html():
    rows = ''.join(f'<tr><td class="k">{a}</td><td></td><td></td></tr>' for a, b, c in LAYERS)
    pages = [
        '<h2>七層堆疊說明卡</h2><p class="lead">挑一個電路（Bell、GHZ、BV）和一種晶片，在 transmon-3d.html#stack 自由實驗走完每個階段，寫出每一層做了什麼。</p>'
        '<p>我挑的電路：□ Bell　□ GHZ　□ BV　　晶片：□ 直線 5 顆　□ 方格 3×3</p>'
        '<table class="judge"><tr><th style="width:24%">層</th><th style="width:38%">這一層負責什麼</th><th style="width:38%">我的電路在這一層變成什麼</th></tr>'
        + rows + '</table>'
        '<p class="note">兩根支柱：自動校準＿＿＿＿＿＿＿＿＿＿　錯誤處理＿＿＿＿＿＿＿＿＿＿</p>',
        '<h2>效能競賽計分表</h2><p class="lead">在自由實驗選電路與晶片，連按「下一階段 ▶」到「⑤ 排程與脈衝」，抄下右側面板的數字。</p>'
        '<table class="rec"><tr>' + ''.join(f'<th>{h}</th>' for h in SHEET_HEADER) + '</tr>'
        + ''.join(f'<tr><td>{r[0]}</td><td>{r[1]}</td><td></td><td></td><td></td><td></td><td></td></tr>' for r in SHEET_ROWS) + '</table>'
        '<pre class="code">MY_CIRCUIT = &#39;ghz&#39;   # 改造區 1：選一個電路（&#39;bell&#39;、&#39;ghz&#39;、&#39;bv&#39;）\nMY_CHIP = &#39;line&#39;     # 改造區 2：選一種晶片（&#39;line&#39; 直線 5 顆、&#39;grid&#39; 方格 3×3）</pre>'
        '<p class="note">BV 在直線晶片上換 CNOT 的順序，最少要＿＿個 SWAP；總時間＿＿＿＿ ns。哪一場的讀取比所有閘加起來還久？＿＿＿＿＿＿</p>',
        '<h2>三個容易錯的地方</h2><div class="box"><ul class="chk">'
        '<li>以為電路寫好就能直接在晶片上跑：其實要經過分解、映射、路由、最佳化、排程、脈衝</li>'
        '<li>以為 Rz 也要花時間：Rz 是虛擬 Z，只改後續脈衝的相位參考，0 ns</li>'
        '<li>以為晶片怎麼連都一樣：連接方式會大幅改變 SWAP 數與錯誤</li></ul></div>'
        '<div class="box" style="margin-top:5mm"><h3>數一數</h3>'
        '<p>原生閘只有 ＿＿、＿＿、＿＿ 三種；一個 SWAP = ＿＿ 個 CNOT</p>'
        '<p>動畫的時間：√X ＿＿ ns、CZ ＿＿ ns、讀取約 ＿＿ ns</p>'
        '<p>回饋：讀取約 600 ns → FPGA 判斷約 ＿＿ ns → 條件 π 脈衝；所有儀器鎖在 ＿＿ MHz 參考時鐘</p>'
        '<p>我最容易搞錯的一點：</p><div class="line"></div><div class="line"></div></div>',
        '<h2>最後一關：說出七層</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 一行程式怎麼變成晶片上的微波？按順序說出七層。</p><div class="line"></div>'
        '<p>2. 為什麼 BV 在直線晶片上要插 SWAP，在方格晶片上不用？</p><div class="line"></div>'
        '<p>3. 校準和錯誤處理為什麼叫「支柱」？</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><ul class="chk">'
        '<li>不看稿說出：分解 → 映射 → 路由 → 最佳化 → 排程 → 脈衝 → 即時控制</li><li>在自由實驗示範直線與方格的差別，並解釋紫色的閘</li>'
        '<li>說出數字：BV 直線 2 個 SWAP、1320 ns；方格 0 個、840 ns</li><li>指出一個限制：晶片連接方式會大幅改變 SWAP 數與錯誤</li>'
        '<li>替七層堆疊說明卡取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q111 七層堆疊說明卡 列印包', '父子科技學院 量子電腦學程 Q111｜第 13 課：編譯與控制軟體堆疊', pages, EXTRA_CSS)


if __name__ == '__main__':
    check_program()
    classroom_pack.build(
        slug='q111-software-stack', folder='Q111_編譯與控制軟體堆疊', files=FILES,
        sheet=('03_效能競賽計分表.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_七層堆疊說明卡.pdf', pack_pages=4,
        pack_needles=('七層堆疊說明卡', '效能競賽', 'MY_CIRCUIT', 'MY_CHIP', '容易錯', 'SWAP', '最後一關'),
        authoring_dir=XINEW / 'authoring/q111', episode_dir='specials/q111-software-stack',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'no（瀏覽器開動畫；stack_race.py 只需 Python 3）',
               'program': 'stack_race.py', 'testedWith': 'Python 3.13.18 (standard library only)',
               'recordedRun': {'nativeGateIdentities': 4, 'nativeGateIdentitiesAllSame': True,
                               'swaps': {'bell@line': 0, 'bell@grid': 0, 'ghz@line': 0, 'ghz@grid': 0, 'bv@line': 2, 'bv@grid': 0},
                               'totalNs': {'bell': 712, 'ghz': 760, 'bv@line': 1320, 'bv@grid': 840},
                               'physicalCircuitMatchesIdeal': True, 'bvLineBestOrder': {'swaps': 1, 'cz': 6, 'totalNs': 1080}},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q111/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')
