"""父子科技學院 量子電腦學程 Q101：迷思修正——Z 線不是把位元調成一樣

用和 transmon-3d.html 第 6 章（案例）相同的公式與數值，算三顆可調 transmon 的頻率與碰撞。
只用 Python 標準函式庫，不需要安裝任何套件：  python freq_case.py
碰撞判定窗是動畫的示意值，不是真實晶片的規格。
"""
import math

EC, ALPHA, D = 0.25, -0.283, 0.013          # GHz：充電能、非諧性、修正項（同動畫）
EJMAX = [14.49, 14.381, 15.978]             # GHz：三顆的 E_J,max（製程誤差讓它們不同）
WIN = {'same': 0.03, 'x12': 0.025, 'tp': 0.012}   # GHz：碰撞判定窗（示意）


def freq(k, phi):
    """第 k 顆在磁通 phi（單位 Φ₀）時的 f01（GHz）：E_J(Φ) = E_J,max|cos(πΦ/Φ₀)|，f01 ≈ √(8 E_J E_C) − E_C。"""
    ej = EJMAX[k] * abs(math.cos(math.pi * phi))
    return max(0.0, math.sqrt(8 * ej * EC) - EC - D)


def phi_for(k, f):
    """要讓第 k 顆停在頻率 f，Z 線要給多少磁通（只能往下調；f 比最高頻率還高時回傳 None）。"""
    ej = (f + EC + D) ** 2 / (8 * EC)
    r = ej / EJMAX[k]
    return None if r > 1 else math.acos(r) / math.pi


def collisions(f):
    out = []

    def pair(i, j, bystander):
        n, m = f'Q{i + 1}', f'Q{j + 1}'
        if abs(f[i] - f[j]) < WIN['same']:
            out.append(f'旁觀者：{n} ≈ {m}' if bystander else f'{n}–{m} 同頻（差 {round(abs(f[i] - f[j]) * 1000)} MHz）')
        if abs(f[i] - (f[j] + ALPHA)) < WIN['x12']:
            out.append(f'{"旁觀者：" if bystander else ""}{n} 0→1 ≈ {m} 1→2')
        if abs(f[j] - (f[i] + ALPHA)) < WIN['x12']:
            out.append(f'{"旁觀者：" if bystander else ""}{m} 0→1 ≈ {n} 1→2')
        if not bystander:
            if abs(f[i] - (f[j] + ALPHA / 2)) < WIN['tp']:
                out.append(f'{n} 驅動 ≈ {m} 雙光子 0→2')
            if abs(f[j] - (f[i] + ALPHA / 2)) < WIN['tp']:
                out.append(f'{m} 驅動 ≈ {n} 雙光子 0→2')

    pair(0, 1, False)   # Q1–Q2 相鄰
    pair(1, 2, False)   # Q2–Q3 相鄰
    pair(0, 2, True)    # Q1、Q3 都是 Q2 的鄰居
    return out


def show(name, phis):
    f = [freq(k, p) for k, p in enumerate(phis)]
    c = collisions(f)
    print(f'{name}：' + '  '.join(f'Q{k + 1} {x:.3f} GHz' for k, x in enumerate(f)))
    print('    ' + ('；'.join(c) if c else '無碰撞'))


if __name__ == '__main__':
    show('製程原貌（三顆都在 Φ = 0）', [0, 0, 0])
    # 迷思：把三顆都調成一樣（Q3 調到和 Q2 相同；Q1 也調到 5.100）
    show('迷思：全部調成 5.100', [phi_for(0, 5.100), 0, phi_for(2, 5.100)])
    show('棋盤格（Q1 = Q3 = 4.90）', [phi_for(0, 4.90), 0, phi_for(2, 4.90)])
    show('頻率配置（4.90／5.10／5.30）', [phi_for(0, 4.90), 0, phi_for(2, 5.30)])
    print('Q2 想往上調到 5.20 GHz：', phi_for(1, 5.20), '（None = 做不到，只能往下調）')
    print('調近再調開：Q2、Q3 固定在配置，Q1 從 4.90 慢慢往上')
    for f1 in (4.90, 4.95, 5.00, 5.05, 5.08, 5.10):
        p = phi_for(0, f1)
        c = collisions([freq(0, p), freq(1, 0), freq(2, phi_for(2, 5.30))])
        print(f'    Q1 = {f1:.2f} GHz（Φ = {p:.3f} Φ₀）：' + ('；'.join(c) if c else '無碰撞'))
