"""Q087 課堂教材：變分演算法 — 本機兩位元 VQE 模擬器（只用 Python 標準函式庫）、能量曲線紀錄、程式對決、起點實驗、說明卡與解答。

免帳號：06_兩位元VQE模擬.py 只需要 Python 3（不用安裝套件）；動畫用學程的 animations/operation.html（#gates、#qubit）。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q087/classroom.py
"""
from pathlib import Path
import math
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 玩具題目：H = −Z₀Z₁ + 0.3(Z₀ + Z₁)；試探線路 Ry(a) ⊗ Ry(b) 作用在 |00⟩。
# 能量 E(a, b) = −cos a · cos b + 0.3(cos a + cos b)。兩個谷底：(0°, 0°) → −0.4（局部最小）、(180°, 180°) → −1.6（基態 |11⟩）。
J, HZ, LR, ITERS = 1.0, 0.3, 0.4, 40


def energy(a, b):
    ca, cb = math.cos(a), math.cos(b)
    return -J * ca * cb + HZ * (ca + cb)


def descend(a_deg, b_deg):
    a, b = math.radians(a_deg), math.radians(b_deg)
    out = []
    for _ in range(ITERS + 1):
        out.append(energy(a, b))
        ga = (energy(a + math.pi / 2, b) - energy(a - math.pi / 2, b)) / 2   # 參數平移規則
        gb = (energy(a, b + math.pi / 2) - energy(a, b - math.pi / 2)) / 2
        a, b = a - LR * ga, b - LR * gb
    return out


STARTS = [(20, 20), (60, 60), (100, 30), (90, 90), (120, 120), (45, 135), (160, 160)]
RESULTS = {s: descend(*s) for s in STARTS}
assert abs(RESULTS[(20, 20)][-1] + 0.4) < 1e-3 and abs(RESULTS[(160, 160)][-1] + 1.6) < 1e-3
assert abs(RESULTS[(90, 90)][-1] + 1.6) < 1e-3 and abs(RESULTS[(100, 30)][-1] + 0.4) < 1e-3
f3 = lambda v: f'{v:+.3f}'  # noqa: E731

SIM = '''"""兩位元變分量子特徵值求解器（VQE）的本機模擬器（父子科技學院 Q087）。
只用 Python 標準函式庫：python3 06_兩位元VQE模擬.py 20 20
（兩個數字是兩顆量子位元的起始角度，單位是度；不填就用 20 20）

玩具題目（教學用，不是真實分子）：
    能量算符 H = −Z0·Z1 + 0.3·(Z0 + Z1)
    試探線路：兩顆量子位元都從 |0⟩ 出發，各做一個 Ry(角度) 旋轉閘
迴圈：古典電腦給角度 → 「量子電腦」跑線路、量 SHOTS 次估計能量 → 用參數平移規則算斜率 → 角度往下坡走一步
"""
import math
import random
import sys

SHOTS = 1000      # 每次估計能量量幾次；改成 0 代表「無限多次」（直接算理論值，沒有統計誤差）
LR = 0.4          # 每一步走多大（學習率）
ITERS = 40        # 迭代次數
SEED = None       # 想讓每次結果一樣，就填一個整數


def probs(a, b):
    """兩顆位元各自 Ry 之後，量到 0 的機率（沒有糾纏，兩顆獨立）。"""
    return math.cos(a / 2) ** 2, math.cos(b / 2) ** 2


def energy(a, b, rng):
    p0, q0 = probs(a, b)
    if SHOTS == 0:
        z0, z1 = 2 * p0 - 1, 2 * q0 - 1
        return -z0 * z1 + 0.3 * (z0 + z1)
    total = 0.0
    for _ in range(SHOTS):
        z0 = 1 if rng.random() < p0 else -1     # 量到 0 記 +1，量到 1 記 −1
        z1 = 1 if rng.random() < q0 else -1
        total += -z0 * z1 + 0.3 * (z0 + z1)
    return total / SHOTS


def main():
    rng = random.Random(SEED)
    a_deg = float(sys.argv[1]) if len(sys.argv) > 1 else 20.0
    b_deg = float(sys.argv[2]) if len(sys.argv) > 2 else 20.0
    a, b = math.radians(a_deg), math.radians(b_deg)
    rows = []
    for it in range(ITERS + 1):
        e = energy(a, b, rng)
        rows.append((it, math.degrees(a), math.degrees(b), e))
        ga = (energy(a + math.pi / 2, b, rng) - energy(a - math.pi / 2, b, rng)) / 2
        gb = (energy(a, b + math.pi / 2, rng) - energy(a, b - math.pi / 2, rng)) / 2
        a, b = a - LR * ga, b - LR * gb
    print("迭代  角度一   角度二    能量    （每個 # 代表 0.05）")
    for it, x, y, e in rows:
        bar = "#" * max(0, round((e + 1.8) / 0.05))
        print(f"{it:4d} {x:7.1f} {y:7.1f} {e:+7.3f}  {bar}")
    with open("能量曲線.csv", "w", encoding="utf-8") as f:
        f.write("迭代,角度一,角度二,能量\\n")
        for it, x, y, e in rows:
            f.write(f"{it},{x:.1f},{y:.1f},{e:.4f}\\n")
    print("最後能量：%+.3f（真正最低是 −1.600）；已存成 能量曲線.csv，可以用試算表畫圖" % rows[-1][3])


if __name__ == "__main__":
    main()
'''

FILES = {
'00_爸爸先讀.md': f'''# 父子科技學院 量子電腦學程 Q087：變分演算法：VQE 與 QAOA（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶出一個問題：容錯量子電腦還沒來之前，有雜訊、位元不多的機器能做什麼？其中一個答案是「量子線路＋古典最佳化」的變分迴圈。

需要：Python 3（不用安裝套件）跑 `06_兩位元VQE模擬.py`；瀏覽器開學程的 `animations/operation.html#gates` 和 `#qubit`。不需要網路或帳號。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 變分原理、迴圈四步、VQE 與 QAOA | 影片第 3–7 段、`05_動畫導覽.md` |
| 25–65 | 跑兩位元 VQE、畫能量曲線、程式對決 | `01_操作步驟.md`、列印包第 1–2 頁 |
| 65–75 | 休息 | |
| 75–105 | 換五組起點，看會不會卡在局部最小值 | 列印包第 3 頁、`03_能量與起點紀錄.csv` |
| 105–115 | 孩子教爸爸：分工、變分原理、限制 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 15 分鐘）

- 在終端機跑 `python3 06_兩位元VQE模擬.py 20 20` 和 `python3 06_兩位元VQE模擬.py 160 160`，看最後能量分別停在約 −0.4 和約 −1.6。
- 列印 `02_列印包_變分演算法.pdf`（A4，共 4 頁）。讀一遍 `04_解答.md`。

## 程式對決怎麼玩

爸爸和孩子各寫下一組起始角度（0–180 度），輪流執行模擬器，把每次的能量畫在列印包第 2 頁。最後能量比較低的人贏；輸的人說出自己的曲線卡在哪裡。

## 誠實說明

- 模擬器的題目是本課自訂的玩具題目（兩個谷底 −1.6、−0.4），不是任何分子的真實能量；它的答案剛好不需要糾纏，所以試探線路只有兩個旋轉閘。
- 變分演算法是啟發式方法，不保證找到真正的最低能量，目前也沒有被證明的普遍加速；線路選得不好還會遇到「貧瘠高原」。
- 預設每次估計量 1000 次，所以能量會有一點點抖動；把 `SHOTS` 改成 0 就是沒有統計誤差的理論值。
''',

'01_操作步驟.md': '''# 操作步驟

## A. 先看「旋鈕」（`operation.html#gates`，約 5 分鐘）

1. 按「重設 |0⟩」，把「旋轉角 θ」拉到 45°。
2. 連按四次「Ry(θ)」：箭頭每次往下轉 45°，第四次停在南極。右下角的線路紀錄排出四個方塊。
3. 想一想：如果角度是一顆旋鈕，誰來決定要轉多少？

## B. 手動跑一圈變分迴圈（`operation.html#qubit`，約 10 分鐘）

1. 假裝「能量 = 得到 0 的比例」。按「θ=60°」，再按「一次跑 1000 shots」，記下藍柱大約多高。
2. 把「θ（極角）」拉到 120°，再跑 1000 次；最後拉到 180°，再跑一次。
3. 你剛剛就是「古典電腦」：看結果、調角度、再量一次。

## C. 跑兩位元 VQE（約 20 分鐘）

1. 終端機輸入 `python3 06_兩位元VQE模擬.py 20 20`。
2. 看每一列的能量：它隨著迭代往下掉，最後停住。程式也存了 `能量曲線.csv`。
3. 把第 0、5、10、20、40 次的能量抄到列印包第 1 頁，畫成一條曲線。

## D. 程式對決與換起點（下半場約 30 分鐘）

1. 程式對決：照「00_爸爸先讀」的規則，各挑一組起點，比最後能量。
2. 換起點：至少試五組，記在列印包第 3 頁，寫下每一組停在 −0.4 還是 −1.6。
3. 進階：把 `SHOTS` 改成 100，曲線變得比較抖；改成 0，曲線變得很平滑。
''',

'04_解答.md': '# 解答（爸爸用）\n\n## 玩具題目的理論能量曲線（`SHOTS = 0`，學習率 0.4）\n\n'
  '| 起始角度 | 第 0 次 | 第 5 次 | 第 10 次 | 第 20 次 | 第 40 次 | 停在 |\n|---|---|---|---|---|---|---|\n'
  + ''.join(f'| ({a}°, {b}°) | ' + ' | '.join(f3(r[k]) for k in (0, 5, 10, 20, 40)) + f" | {'局部最小 −0.4' if r[-1] > -1 else '最低點 −1.6'} |\n"
            for (a, b), r in RESULTS.items())
  + '\n預設 `SHOTS = 1000` 時，在山坡上的能量會在理論值附近抖動，一個標準差約 0.03（谷底附近幾乎不抖）；起點剛好在 (90°, 90°) 這種「分水嶺」附近時，雜訊可能讓它掉進任一個山谷。\n\n'
  '## 為什麼有兩個山谷？\n\n能量 E = −cos a·cos b + 0.3(cos a + cos b)。兩顆都在 |0⟩（a = b = 0°）時 E = −1 + 0.6 = −0.4；兩顆都在 |1⟩（180°）時 E = −1 − 0.6 = −1.6。'
  '從 (0°, 0°) 往任何方向走一小步，能量都會變高，所以梯度下降停在那裡：這就是局部最小值。\n\n'
  '## 常見問題\n\n'
  '- 量子電腦負責什麼？跑帶角度的線路、量很多次，估計能量。古典電腦負責什麼？看能量、決定角度怎麼調。\n'
  '- 變分原理：任何試探狀態量到的平均能量都不會低於基態能量，所以越低越接近答案。\n'
  '- 為什麼要量那麼多次？能量是統計估出來的，誤差約和次數的平方根成反比：誤差小十倍要多一百倍次數。\n'
  '- QAOA 和 VQE 差在哪？骨架相同；QAOA 的線路是「問題層＋混合層」輪流疊 p 層（2p 個角度），用來解組合最佳化，例如 MaxCut。\n'
  '- 限制：局部最小值、貧瘠高原（地形一片平、找不到下坡）、量測次數多、雜訊；目前沒有被證明的普遍加速。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路或帳號。課綱規劃的「變分能量地形場景」尚未製作，本課用以下兩個現有場景。

## `operation.html#gates`（操作場景 2：單位元量子閘）

- 滑桿「旋轉角 θ（給 Rx / Ry / Rz）」：−180°～180°；按鈕 Rx(θ)、Ry(θ)、Rz(θ)。
- 粉紅線是旋轉軸；右下插圖是最後一個閘的矩陣與線路紀錄。
- 變分演算法裡，這些可調角度就是古典電腦要調的參數。

## `operation.html#qubit`（操作場景 1：量子位元的狀態與測量）

- 滑桿「θ（極角）」：0°～180°，改動會清空統計；按鈕「一次跑 1000 shots」。
- 右側藍柱 = 得到 0、紅柱 = 得到 1；青色橫線 = 理論機率 cos²(θ/2)。
- 右下插圖：估計值隨 shots 數收斂，灰帶是 ±1σ，次數越多越窄。

## 操作

`H` 隱藏面板；滑鼠拖曳旋轉、滾輪縮放。
''',

'06_兩位元VQE模擬.py': SIM,
}

SHEET_HEADER = ['項目', '玩家', '起始角度一', '起始角度二', '第0次能量', '第10次能量', '第40次能量', '停在哪個谷底', '備註']
SHEET_ROWS = ([['程式對決', p, '', '', '', '', '', '', ''] for p in ('爸爸', '孩子')]
              + [[f'換起點第 {i} 組', '', '', '', '', '', '', '', ''] for i in range(1, 6)])

EXTRA_CSS = '''table.rec td{height:9mm}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.card{border:2pt solid #0b2540;border-radius:4mm;padding:5mm;margin-top:5mm}.card h3{margin-top:0}'''


def html():
    pages = [
        '<h2>實驗一：能量隨迭代往下掉</h2><p class="lead">執行 python3 06_兩位元VQE模擬.py 20 20，把能量抄下來，畫成曲線。</p>'
        '<table class="rec"><tr><th>迭代次數</th><th>0</th><th>5</th><th>10</th><th>20</th><th>40</th></tr>'
        '<tr><td>能量</td><td></td><td></td><td></td><td></td><td></td></tr></table>'
        '<div class="card"><h3>VQE notebook（今天的作品）</h3><p>我的能量曲線（橫軸：迭代次數；縱軸：能量）：</p>'
        '<div style="height:60mm;border:1pt solid #9fb0c8"></div>'
        '<p>作品名稱：＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p></div>',
        '<h2>程式對決：誰的能量最低</h2><p class="lead">各挑一組起始角度（0–180 度），跑四十次迭代，比最後的能量。</p>'
        '<table class="rec"><tr><th>玩家</th><th>起始角度</th><th>第 0 次</th><th>第 10 次</th><th>第 40 次</th><th>贏了嗎</th></tr>'
        '<tr><td>爸爸</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>你</td><td></td><td></td><td></td><td></td><td></td></tr></table>'
        '<p class="note">輸的人說說看：我的曲線卡在哪裡？為什麼？</p><div class="line"></div><div class="line"></div>',
        '<h2>換你改造：會不會卡住</h2><p class="lead">試五組不同的起點，記下每一組停在 −0.4 還是 −1.6。</p>'
        '<table class="rec"><tr><th>組</th><th>角度一</th><th>角度二</th><th>最後能量</th><th>停在哪個谷底</th></tr>'
        + ''.join(f'<tr><td>{i}</td><td></td><td></td><td></td><td></td></tr>' for i in range(1, 6)) + '</table>'
        '<p>哪些起點會卡在 −0.4？＿＿＿＿＿＿＿＿＿＿＿＿</p>'
        '<p class="note">生活技能：反覆試錯逼近答案——蒙著眼睛下山，每一步先踩踩看哪邊比較低。大題目不知道起點，你會怎麼辦？＿＿＿＿＿＿＿＿</p>',
        '<h2>說明卡與最後一關</h2><div class="box"><p>1. 變分迴圈裡，量子電腦負責什麼？古典電腦負責什麼？</p><div class="line"></div>'
        '<p>2. 變分原理是什麼？</p><div class="line"></div><p>3. VQE 和 QAOA 哪裡一樣、哪裡不一樣？</p><div class="line"></div>'
        '<p>4. 一個限制或注意事項：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出分工：量子量能量、古典調角度</li><li>說出變分原理：猜的能量不會低於基態</li>'
        '<li>說出為什麼要量很多次</li><li>指出一個限制：局部最小值、貧瘠高原、沒有被證明的普遍加速</li>'
        '<li>替 VQE notebook 取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q087 變分演算法 列印包', '父子科技學院 量子電腦學程 Q087｜變分演算法：VQE 與 QAOA', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q087-vqe-qaoa', folder='Q087_變分演算法', files=FILES,
        sheet=('03_能量與起點紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_變分演算法.pdf', pack_pages=4,
        pack_needles=('能量隨迭代', 'VQE notebook', '程式對決', '會不會卡住', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q087', episode_dir='specials/q087-vqe-qaoa',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'scenes': ['animations/operation.html#gates', 'animations/operation.html#qubit'],
               'toyModel': 'H = -Z0Z1 + 0.3(Z0+Z1), Ry⊗Ry ansatz; minima -1.6 (global) and -0.4 (local)',
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q087/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')
