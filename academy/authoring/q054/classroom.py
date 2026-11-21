"""Q054 課堂教材：分解練習單、對決記錄表、對決題卡、可執行的 zyz_lab.py、說明卡與解答。

不需要帳號、不需要安裝套件（zyz_lab.py 只用 Python 標準函式庫；也可以只用動畫）。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q054/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

PROGRAM = r'''"""父子科技學院 量子電腦學程 Q054：任意旋轉 = 三個旋轉 的小實驗室（只用 Python 標準函式庫）

執行：python zyz_lab.py
一、把常見的單位元閘拆成「繞 z、繞 y、再繞 z」三個旋轉（U = e^(iγ)·Rz(φ)·Ry(θ)·Rz(λ)），
    印出在 operation.html#gates 要「依序按」的三個按鈕：Rz(λ) → Ry(θ) → Rz(φ)，並用矩陣相乘驗證。
二、比較受控 T 和受控 Rz(45°)：單獨一顆只差整體相位，做成受控版本就不一樣。
改造區：在 QUIZ 裡加入你自己的題目（可以把幾個閘相乘）。
"""
import cmath
import math

S2 = 1 / math.sqrt(2)


def mul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def RZ(deg):
    t = math.radians(deg)
    return [[cmath.exp(-1j * t / 2), 0], [0, cmath.exp(1j * t / 2)]]


def RY(deg):
    t = math.radians(deg)
    c, s = math.cos(t / 2), math.sin(t / 2)
    return [[c, -s], [s, c]]


def RX(deg):
    t = math.radians(deg)
    c, s = math.cos(t / 2), math.sin(t / 2)
    return [[c, -1j * s], [-1j * s, c]]


GATES = {
    'H': [[S2, S2], [S2, -S2]],
    'X': [[0, 1], [1, 0]],
    'Y': [[0, -1j], [1j, 0]],
    'Z': [[1, 0], [0, -1]],
    'S': [[1, 0], [0, 1j]],
    'S†': [[1, 0], [0, -1j]],
    'T': [[1, 0], [0, cmath.exp(1j * math.pi / 4)]],
    'T†': [[1, 0], [0, cmath.exp(-1j * math.pi / 4)]],
    '√X': [[0.5 + 0.5j, 0.5 - 0.5j], [0.5 - 0.5j, 0.5 + 0.5j]],
}


def norm180(a):
    a = (a + 180) % 360 - 180
    return 180.0 if abs(a + 180) < 1e-6 else a


def same_up_to_phase(A, B):
    """A = e^(iγ)·B？回傳 (是否相同, γ 度數)"""
    k = sum(complex(B[i][j]).conjugate() * complex(A[i][j]) for i in range(2) for j in range(2))
    k /= abs(k)
    ok = all(abs(complex(A[i][j]) - k * complex(B[i][j])) < 1e-9 for i in range(2) for j in range(2))
    return ok, math.degrees(cmath.phase(k)) % 360


def zyz(U):
    """U = e^(iγ)·Rz(φ)·Ry(θ)·Rz(λ)；回傳 (λ, θ, φ, γ)，單位是度。"""
    a, b = complex(U[0][0]), complex(U[0][1])
    c, d = complex(U[1][0]), complex(U[1][1])
    g = cmath.phase(a * d - b * c) / 2
    e = cmath.exp(-1j * g)
    a, c, d = a * e, c * e, d * e
    th = 2 * math.atan2(abs(c), abs(a))
    s = cmath.phase(d) if abs(d) > 1e-9 else 0.0   # (φ + λ) / 2
    t = cmath.phase(c) if abs(c) > 1e-9 else 0.0   # (φ − λ) / 2
    phi, lam = math.degrees(s + t), math.degrees(s - t)
    th = math.degrees(th)
    if th < 1e-6:                      # 中間那一步是 0：兩個 Rz 合成一個
        lam, phi = lam + phi, 0.0
    lam, phi = norm180(lam), norm180(phi)
    ok, gamma = same_up_to_phase(U, mul(RZ(phi), mul(RY(th), RZ(lam))))
    assert ok
    return lam, th, phi, gamma


def fmt(x):
    return f'{x:g}°' if abs(x - round(x)) > 1e-6 else f'{round(x)}°'


def plan(U):
    lam, th, phi, gamma = zyz(U)
    steps = [f'Rz({fmt(lam)})', f'Ry({fmt(th)})', f'Rz({fmt(phi)})']
    keep = [s for s, v in zip(steps, (lam, th, phi)) if abs(v) > 1e-6]
    return lam, th, phi, gamma, ' → '.join(keep) if keep else '（什麼都不用按）'


QUIZ = [   # (題目, 矩陣)；改造區：加你自己的題目
    ('H', GATES['H']), ('S', GATES['S']), ('T', GATES['T']), ('Z', GATES['Z']), ('X', GATES['X']),
    ('Y', GATES['Y']), ('√X', GATES['√X']), ('S†', GATES['S†']), ('T†', GATES['T†']),
    ('Rx(60°)', RX(60)), ('H 接 T', mul(GATES['T'], GATES['H'])), ('H 接 S', mul(GATES['S'], GATES['H'])),
]

if __name__ == '__main__':
    print('一、拆成三個旋轉（按鈕依序按；角度為 0 的那一步省略）')
    print(f'  {"題目":<8}{"λ":>8}{"θ":>8}{"φ":>8}{"整體相位":>10}   依序按')
    for name, U in QUIZ:
        lam, th, phi, gamma, order = plan(U)
        print(f'  {name:<8}{fmt(lam):>8}{fmt(th):>8}{fmt(phi):>8}{fmt(gamma):>10}   {order}')

    print('\n二、受控版本：整體相位會被看見')
    CT = [1, 1, 1, cmath.exp(1j * math.pi / 4)]                       # 受控 T 的對角線
    CR = [1, 1, cmath.exp(-1j * math.pi / 8), cmath.exp(1j * math.pi / 8)]  # 受控 Rz(45°)
    for name, D in (('受控 T', CT), ('受控 Rz(45°)', CR)):
        # 控制位元 |+⟩、目標位元 |1⟩：狀態 (|0⟩|1⟩ + |1⟩|1⟩)/√2，只看 |01⟩ 和 |11⟩ 的振幅
        a01, a11 = D[1] * S2, D[3] * S2
        ang = math.degrees(cmath.phase(a11 / a01))
        print(f'  {name:<12} 控制位元的相對相位 = {ang:.1f}°')
    print('  兩者差 22.5°：單獨一顆時看不見的整體相位，受控時變成控制位元上的相位。')
'''

ns = {}
exec(compile(PROGRAM, 'zyz_lab.py', 'exec'), ns)  # 用同一份程式算解答，避免手抄錯
ANS = {name: ns['plan'](U) for name, U in ns['QUIZ']}
FMT = ns['fmt']

PRACTICE = ['H', 'S', 'T', 'Z', 'X', '√X']        # 分解練習單（課綱：H、S、T 必做）
DUEL = [  # (題卡名, 題目, 動畫裡出題者怎麼按)
    ('半個翻轉', '√X', '按「√X」'),
    ('翻轉', 'X', '按「X」'),
    ('繞左右軸', 'Y', '按「Y」'),
    ('前後軸 60°', 'Rx(60°)', '滑桿 60°，按「Rx(θ)」'),
    ('兩顆一起', 'H 接 T', '依序按「H」「T」'),
    ('倒退的相位', 'T†', '按「T†」'),
]


def ans_row(name):
    lam, th, phi, gamma, order = ANS[name]
    return FMT(lam), FMT(th), FMT(phi), FMT(gamma), order


FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q054：任意旋轉 = 三個旋轉（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。今天的核心一句：**任何單一量子位元的操作，都能拆成「繞 z 軸、繞 y 軸、再繞 z 軸」三個旋轉，外加一個整體相位：U = e^(iγ)·Rz(φ)·Ry(θ)·Rz(λ)。** 矩陣由右往左作用，所以在動畫裡依序按 Rz(λ) → Ry(θ) → Rz(φ)。好玩機制是程式對決：一個人偷按一顆閘，另一個人只能用 Rz、Ry 按鈕追上，換一個起點也相同才算贏。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 打開動畫，認識 Rx／Ry／Rz 按鈕與「旋轉角 θ」滑桿 | `operation.html#gates` |
| 25–65 | 把 H、S、T（加碼 Z、X、√X）拆成三個角度，北極與赤道兩個起點都驗證 | 列印包第 1 頁 |
| 65–75 | 休息 | |
| 75–105 | 程式對決：孩子出題、爸爸解題，再交換；記錄誰先拆出來 | 列印包第 2、3 頁、`zyz_lab.py` |
| 105–115 | 孩子教爸爸：三個旋轉的原理、怎麼拆、一個限制 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 下載學程的 `animations/` 資料夾，用瀏覽器開 `operation.html#gates`（課綱指定；不需要網路、伺服器或帳號）。
- 列印 `02_列印包_任意旋轉三個旋轉.pdf`（A4，共 4 頁），第 3 頁的題卡沿虛線剪開。
- 讀一遍 `04_解答.md`。

## 拆閘三步（給孩子的口訣）

1. **看北極**：從 |0⟩ 出發按下這顆閘，箭頭往下倒的角度就是 θ，停在赤道的哪個方位就是 φ。
2. **看赤道**：北極在 z 軸上，第一個 Rz(λ) 對它沒作用；要看赤道上的一點（例如先按 H 到前方）被送到哪，才決定 λ。
3. **換起點**：北極、赤道各驗證一次，箭頭都停在同一點才算拆對。

## 誠實說明

- 拆法不只一種（角度可加減 360°，也可以讓 θ 取負值）；解答只列一組，孩子的答案只要每個起點都對就算對。
- 動畫左邊面板的 |ψ⟩ 係數和原本的閘可能差一個共同的相位因子（整體相位），測量機率一樣。
- 「旋轉角 θ」滑桿每格 5°；本課所有題目的角度都是 5° 的倍數。
- 方向說明：動畫中 x 軸（橘）指向左前方、y 軸（綠）指向右、z 軸直立；轉動視角後左右會跟著改變。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：分解練習單（約 40 分鐘）

1. 打開 `animations/operation.html#gates`，按「重設 |0⟩」。
2. 按「H」，記下箭頭停在哪裡（前方）。
3. 按「重設 |0⟩」，把「旋轉角 θ」設成 180，按「Rz(θ)」；設成 90，按「Ry(θ)」。箭頭也停在前方嗎？左邊面板的機率一樣嗎？|ψ⟩ 的係數差了什麼？
4. 換起點：按「重設 |1⟩」再做一次第 2、3 步，比較兩種做法。
5. 照同樣方法拆 S、T（提示：中間那一步是 0），加碼拆 Z、X、√X，填列印包第 1 頁。
6. 執行 `python zyz_lab.py` 對答案。

## 下半場：程式對決（約 30 分鐘）

1. 出題者抽一張題卡，照卡上的方法在動畫裡按，記下箭頭位置（不要讓解題者看到按了什麼）。
2. 解題者先在紙上寫出三個角度，再按「重設 |0⟩」，依序按 Rz(λ)、Ry(θ)、Rz(φ)。
3. 換起點：兩人都先按「H」（或「重設 |1⟩」）再做一次；兩次都停在同一點才算贏。
4. 在列印包第 2 頁記錄每一局的用時與勝負，再交換角色。
''',

'zyz_lab.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n'
  '公式 U = e^(iγ)·Rz(φ)·Ry(θ)·Rz(λ)；在動畫裡依序按 Rz(λ) → Ry(θ) → Rz(φ)（角度 0 的步驟可省略）。以下由 `zyz_lab.py` 算出，拆法不唯一。\n\n'
  '| 閘 | λ（第一步） | θ（第二步） | φ（第三步） | 整體相位 γ | 依序按 |\n|---|---|---|---|---|---|\n'
  + ''.join(f'| {n} | ' + ' | '.join(ans_row(n)) + ' |\n' for n, _ in ns['QUIZ'])
  + '\n## 其他正確拆法（舉例）\n\n'
  '- H：先 Ry(−90°) 再 Rz(180°)（Z·Ry(−π/2) = H），整體相位 90°。從 |0⟩ 出發，箭頭先倒到後方，再沿赤道轉半圈到前方；|ψ⟩ 顯示 (−0.71i)|0⟩ + (−0.71i)|1⟩。\n'
  '- Rx(θ)：Rz(90°) → Ry(θ) → Rz(−90°)，對任何 θ 都成立。\n\n'
  '## 動畫驗證時會看到\n\n'
  '- H 之後按 T：箭頭沿赤道往右轉 45°；再按 Rz(−45°)：回到前方，|ψ⟩ = (0.65+0.27i)|0⟩ + (0.65+0.27i)|1⟩（只差整體相位 22.5°）。\n'
  '- √X 從 |0⟩：箭頭到左邊；Rz(90°) → Ry(90°) → Rz(−90°)：第一下不動、第二下到前方、第三下到左邊。\n'
  '- 起點改成「H 之後」：√X 讓箭頭不動；三步解法是往右、不動、轉回前方。\n\n'
  '## 常見誤解\n\n'
  '- 「整體相位永遠可以丟」：單獨一顆量測不到；但受控版本只在控制位元為 1 時作用，整體相位變成控制位元的相對相位。'
  '受控 T 與受控 Rz(45°) 相比，控制位元多了 22.5° 的相位（`zyz_lab.py` 第二部分）。\n'
  '- 「拆法只有一種」：角度可以差 360°，也有 θ 取負的拆法；每個起點都對就算對。\n'
  '- 「從北極驗證一次就夠」：第一個 Rz(λ) 對北極沒作用，只驗北極會漏掉 λ 錯誤。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路、伺服器或帳號。

## `animations/operation.html#gates`（如何操作量子電腦 場景 2：單位元閘，課綱指定）

- 閘按鈕：X、Y、Z、H／S、S†、T、T†、√X。
- 滑桿「旋轉角 θ（給 Rx / Ry / Rz）」：−180°～180°，每格 5°；按鈕「Rx(θ)」「Ry(θ)」「Rz(θ)」按下時讀取當時的角度。
- 「重設 |0⟩」「重設 |1⟩」「清除軌跡」；連按的閘會排隊依序執行。
- 粉紅色直線是這一次的旋轉軸；右下插圖顯示最後一個閘的矩陣、線路紀錄與「目前：…」的狀態；左邊面板顯示布洛赫向量、|ψ⟩ 與測量機率。
- 「動畫速度」滑桿可以放慢或加快。

## 操作

滑鼠拖曳旋轉、滾輪縮放；可用左右方向鍵切換場景、`H` 隱藏面板。
''',
}

SHEET_HEADER = ['閘', '第一步 Rz(λ)', '第二步 Ry(θ)', '第三步 Rz(φ)', '整體相位', '北極驗證', '赤道驗證']
SHEET_ROWS = [[g] for g in PRACTICE]

EXTRA_CSS = '''table.dz td{height:13mm;text-align:center;font-size:12pt}table.dz th{font-size:10.5pt;text-align:center}
table.du td{height:11mm;text-align:center}table.du th{text-align:center;font-size:10.5pt}
.chk li{margin:2mm 0;font-size:12.5pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.cards{display:grid;grid-template-columns:1fr 1fr;gap:4mm}.cards .cut{padding:3.5mm 4.5mm;height:72mm}
.cards h3{font-size:14pt;margin:0 0 1.5mm}.cards p{margin:1.2mm 0;font-size:11.5pt}.cards .rx{border-top:.8pt dotted #7f9bb3;padding-top:1.5mm;margin-top:2mm;color:#35506b}
.fx{font-size:15pt;text-align:center;margin:2mm 0 3mm;font-weight:700;color:#0b2540}'''


def html():
    rows = ''.join(f'<tr><td style="width:18mm"><b>{g}</b></td><td></td><td></td><td></td><td></td><td>□</td><td>□</td></tr>'
                   for g in PRACTICE)
    duel_rows = ''.join(f'<tr><td>{k}</td><td></td><td></td><td></td><td></td><td></td></tr>' for k in range(1, 7))
    cards = ''.join(f'<div class="cut"><h3>題卡 {i}：{a}</h3><p><b>出題者：</b>{c}，記下箭頭位置。</p>'
                    f'<div class="rx"><p><b>解題者的三個角度：</b></p><p>Rz(＿＿＿) → Ry(＿＿＿) → Rz(＿＿＿)</p>'
                    f'<p>北極起點 □ 相同　換起點 □ 相同</p></div></div>' for i, (a, b, c) in enumerate(DUEL, 1))
    pages = [
        '<h2>分解練習單</h2><p class="fx">U ＝ e^(iγ) · Rz(φ) · Ry(θ) · Rz(λ)</p>'
        '<p class="lead">在 operation.html#gates 依序按 Rz(λ) → Ry(θ) → Rz(φ)。先從 |0⟩ 驗證，再換一個起點（先按 H，或重設 |1⟩）驗證。H、S、T 必做，其他加碼。</p>'
        '<table class="dz"><tr><th>閘</th><th>第一步<br>Rz(λ)</th><th>第二步<br>Ry(θ)</th><th>第三步<br>Rz(φ)</th>'
        f'<th>整體相位</th><th>北極<br>驗證</th><th>換起點<br>驗證</th></tr>{rows}</table>'
        '<div class="box" style="margin-top:4mm"><p>我發現：相位閘拆完，中間那一步都是＿＿＿；第一個 Rz 對北極＿＿＿＿，所以要換起點驗證。</p>'
        '<p class="note">作品名稱：＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p></div>',
        '<h2>對決記錄表</h2><p class="lead">程式對決：出題者偷按一顆閘，解題者只能用 Rz、Ry 追上。北極和換起點都相同才算贏。</p>'
        '<table class="du"><tr><th>局</th><th>出題者</th><th>題卡</th><th>解題者的三個角度</th><th>用時</th><th>勝負</th></tr>'
        f'{duel_rows}</table>'
        '<div class="box" style="margin-top:4mm"><p>1. 哪一題最難？為什麼？</p><div class="line"></div>'
        '<p>2. 換你出一題（寫下要按的閘或旋轉）：</p><div class="line"></div>'
        '<p>3. 有沒有兩組不同的角度都對？寫下來：</p><div class="line"></div></div>',
        '<h2>對決題卡</h2><p class="lead">沿虛線剪開。出題者抽卡、照卡上的方法按；解題者寫下三個角度後再按。</p>'
        f'<div class="cards">{cards}</div>',
        '<h2>說明卡：我的分解練習單</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 任意旋轉 = 三個旋轉在解決什麼？</p><div class="line"></div><p>2. 我怎麼做？</p><div class="line"></div>'
        '<p>3. 哪裡容易錯？真實的量子電腦哪裡會用到？</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:4mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出：任何單位元操作＝繞 z、繞 y、再繞 z，加一個整體相位</li>'
        '<li>示範：H 和 Ry(−90°)、Rz(180°) 停在同一點，只差整體相位</li>'
        '<li>說出拆閘三步：看北極、看赤道、換起點</li>'
        '<li>指出限制：整體相位單獨一顆看不見，受控版本會變成看得見的相對相位</li>'
        '<li>替分解練習單取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q054 任意旋轉 = 三個旋轉 列印包', '父子科技學院 量子電腦學程 Q054｜任意旋轉 = 三個旋轉', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q054-zyz-decomposition', folder='Q054_任意旋轉三個旋轉', files=FILES,
        sheet=('03_分解練習表.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_任意旋轉三個旋轉.pdf', pack_pages=4,
        pack_needles=('分解練習單', '對決記錄表', '對決題卡', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q054', episode_dir='specials/q054-zyz-decomposition',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'program': 'zyz_lab.py', 'duelCards': [a for a, *_ in DUEL],
               'decompositionFrom': 'slides/QC_Operation_Talk.pptx p19', 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q054/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')
