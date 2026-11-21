"""Q005 課堂教材：盲測（爸爸偷偷加或不加 Z，孩子只用 H 加測量破案）、兩步關卡、解答與閘對照表（不需帳號、不需安裝）。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q005/classroom.py
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

# 單一量子位元的閘（2×2 矩陣），用來重算解答表，避免手算出錯
R = 1 / math.sqrt(2)
GATES = {'H': [[R, R], [R, -R]], 'Z': [[1, 0], [0, -1]], 'S': [[1, 0], [0, 1j]], 'X': [[0, 1], [1, 0]]}


def run(seq):
    """從 |0⟩ 依序作用 seq 裡的閘，回傳得到 0 的機率。"""
    a, b = 1 + 0j, 0j
    for g in seq:
        m = GATES[g]
        a, b = m[0][0] * a + m[0][1] * b, m[1][0] * a + m[1][1] * b
    return abs(a) ** 2


LEVELS = [
    ('直接量（沒加）', ['H']), ('直接量（加了 Z）', ['H', 'Z']),
    ('盲測（沒加）', ['H', 'H']), ('盲測（加了 Z）', ['H', 'Z', 'H']),
    ('Z 加兩次', ['H', 'Z', 'Z', 'H']), ('只加一個 S', ['H', 'S', 'H']), ('加兩個 S', ['H', 'S', 'S', 'H']),
]
assert abs(run(['H', 'H']) - 1) < 1e-9 and abs(run(['H', 'Z', 'H'])) < 1e-9
assert abs(run(['H', 'S', 'H']) - 0.5) < 1e-9 and abs(run(['H', 'S', 'S', 'H'])) < 1e-9
assert abs(run(['H']) - 0.5) < 1e-9 and abs(run(['H', 'Z']) - 0.5) < 1e-9


def pct(p):
    return f'{p * 100:.0f}%'


FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q005：相位（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片約五分鐘，帶出今天的問題：兩支測量起來一模一樣的箭頭，差在哪裡？

## 這份教材在做什麼

盲測遊戲：箭頭先用 H 放到赤道，爸爸偷偷決定加不加 Z，孩子只能用 H 加測量判斷。下半場孩子自己設計「兩步才看得出相位差」的關卡（把 Z 拆成兩個 S）。
不需要帳號；3D 場景見 `05_三維動畫導覽.md`。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 同樣機率不同相位、Z 只改相位、先轉再量 | 影片第 3–6 段 |
| 25–65 | 盲測：先試「直接量就猜」5 回，再試「H 再量」10 回 | `01_盲測步驟.md`、列印包第 1、2 頁 |
| 65–75 | 休息 | |
| 75–105 | 設計兩步的關卡，拿去考爸爸 | 列印包第 3 頁 |
| 105–115 | 孩子教爸爸：為什麼直接測量看不到相位 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名 | |

## 課前準備（約 5 分鐘）

- 電腦或平板打開 `animations/operation.html#gates`；一張紙或資料夾用來遮螢幕；鉛筆。
- 列印 `02_列印包_相位猜猜看.pdf`（A4，共 4 頁），讀一遍 `04_解答與閘對照表.md`。

## 出題者的原則

- 出題時孩子轉身或閉眼；用丟硬幣決定加不加 Z，避免孩子從爸爸的習慣猜到答案。
- 3D 場景沒有「測量一次」按鈕：盲測時看讀數的 P(0)。P(0)=1 代表測量一定得 0，P(0)=0 代表一定得 1。孩子破案前請先遮住讀數以外的線路紀錄（右下小圖會列出按過的閘）。
- 如果孩子直接看 H 之後的 P(0) 就猜，讓他發現兩種情況都是 0.5，這正是今天的重點。

## 誠實說明

- 「沒加得零，有加得一」是理想閘的結果；真實量子電腦有少量錯誤，結果偶爾會錯。
- 「朝前／朝後」是比喻，指赤道上方向相反的兩個點（|+⟩ 與 |−⟩）。
- 只加一個 S 時，H 之後一半一半：一步的相位差（四分之一圈）不可能被一次測量百分之百分辨。
''',

'01_盲測步驟.md': '''# 盲測步驟

## 熱身：直接量就猜（5 回，約 10 分鐘）

1. 爸爸按「重設 |0⟩」，再按 H。孩子轉身。
2. 爸爸丟硬幣：正面就按 Z，反面不按。
3. 孩子轉回來，只能看讀數的 P(0)，猜有沒有加 Z，寫進列印包第 1 頁。
4. 你會發現 P(0) 永遠是 0.500，只能碰運氣。

## 正式盲測：先轉再量（10 回，約 25 分鐘）

1. 同樣：重設 |0⟩ → H → 爸爸偷偷決定加不加 Z。
2. 孩子按一次 H，再看 P(0)。
3. P(0)=1（箭頭回到北極）→ 猜「沒加」；P(0)=0（箭頭在南極）→ 猜「有加」。
4. 爸爸公布答案，猜對記一分。玩完交換角色。

## 下半場：兩步的關卡（約 30 分鐘）

1. 先試：重設 |0⟩ → H → S → H，看 P(0)。（一半一半，偵探沒法確定）
2. 再試：重設 |0⟩ → H → S → S → H。（一定得 1，和加一個 Z 一樣）
3. 自己設計一關：例如「爸爸偷偷加 0 個或 2 個 S」，寫下參考解，拿去考爸爸。
''',

'04_解答與閘對照表.md': '# 解答與閘對照表（爸爸用）\n\n從 |0⟩ 開始，依序作用下列閘，理想情況下測量得到 0 的機率（由矩陣計算）：\n\n'
  + '| 情況 | 閘的順序 | 得到 0 | 得到 1 |\n|---|---|---|---|\n'
  + ''.join(f'| {name} | {" → ".join(seq)} | {pct(run(seq))} | {pct(1 - run(seq))} |\n' for name, seq in LEVELS)
  + '\n## 為什麼\n\n'
  '- H 把北極的箭頭放到赤道「前方」（|+⟩）。Z 繞直立軸轉半圈，把它轉到「後方」（|−⟩）。兩者直接量都是一半一半。\n'
  '- 第二個 H 把前方送回北極、後方送到南極，相位差就變成 0 和 1 的差別。\n'
  '- S 只轉四分之一圈，兩個 S 等於一個 Z（S·S = Z）。只加一個 S，H 之後是一半一半。\n'
  '- Z 加兩次等於沒加（Z·Z = I）。\n\n'
  '## 常見問題\n\n'
  '- 孩子說「Z 沒有用」：如果箭頭在北極就按 Z，箭頭真的不會動，因為 Z 不改 |0⟩。要先 H 放到赤道。\n'
  '- 孩子只看 P(0) 就猜：直接量看不出相位，這是今天要指出的限制。\n',

'05_三維動畫導覽.md': '''# 三維動畫導覽

學程的三維動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路或伺服器。

## 今天的場景：`animations/operation.html#gates`（場景 2：單位元閘）

- 按鈕 X、Y、Z、H、S……：每按一個，箭頭就繞粉紅色的軸轉動。
- 「重設 |0⟩」：箭頭回到北極，線路紀錄清空。
- 「示範：H → Z → H = X」：一次看完盲測「有加 Z」的情況。
- 讀數：測量機率 P(0)、P(1)。
- 右下小圖：最後一個閘的矩陣和按過的閘（出題時要遮住）。

## 補充：`animations/operation.html#qubit`（場景 1）

- 按「|+⟩」，再拖「φ（相位）」滑桿：箭頭繞赤道轉，但理論機率不變。

## 操作

滑鼠拖曳旋轉、滾輪縮放；`H` 隱藏面板；`R` 重設視角。
''',
}

SHEET_HEADER = ['回合', '方法', '我的猜測（有加／沒加）', '看到的 P(0) 或結果', '爸爸公布', '對或錯']
SHEET_ROWS = ([[str(i), '直接量'] for i in range(1, 6)] + [[str(i), '先 H 再量'] for i in range(6, 16)])

EXTRA_CSS = '''table.rec td{height:9.5mm}table.big td{height:13mm}
.chk li{margin:3mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.flow{font-size:14pt;font-weight:bold;color:#0b2540;margin:3mm 0}'''


def html():
    rows5 = ''.join(f'<tr><td>{i}</td><td></td><td></td><td></td><td></td></tr>' for i in range(1, 6))
    rows10 = ''.join(f'<tr><td>{i}</td><td></td><td></td><td></td><td></td></tr>' for i in range(1, 11))
    pages = [
        '<h2>盲測熱身：直接量就猜</h2><p class="lead">重設 |0⟩ → H → 爸爸偷偷加或不加 Z → 你只看 P(0) 就猜。</p>'
        '<table class="big"><tr><th>回合</th><th>看到的 P(0)</th><th>我猜（有加／沒加）</th><th>爸爸公布</th><th>對或錯</th></tr>'
        + rows5 + '</table>'
        '<p style="margin-top:5mm">五回猜對：＿＿回。　P(0) 每次都是多少？＿＿＿＿</p>'
        '<div class="box" style="margin-top:5mm"><h3>想一想</h3><p>為什麼只看 P(0) 沒辦法破案？</p>'
        '<div class="line"></div><div class="line"></div></div>',
        '<h2>相位猜猜看紀錄：先轉再量</h2>'
        '<p class="flow">重設 |0⟩ → H → 爸爸偷偷：Z 或不加 → 你按 H → 看 P(0)</p>'
        '<table class="rec"><tr><th>回合</th><th>我按 H 後的 P(0)</th><th>我猜（有加／沒加）</th><th>爸爸公布</th><th>對或錯</th></tr>'
        + rows10 + '</table>'
        '<p style="margin-top:4mm">十回猜對：＿＿回。　P(0)=1 代表＿＿＿＿；P(0)=0 代表＿＿＿＿</p>'
        '<div class="box" style="margin-top:4mm"><h3>交換角色</h3><p>換我出題，爸爸猜對：＿＿回／＿＿回</p></div>',
        '<h2>下半場：設計兩步的關卡</h2><p class="lead">S 只轉四分之一圈。先試試，再自己出一關。</p>'
        '<table class="big"><tr><th>試一試</th><th>閘的順序</th><th>我猜 P(0)</th><th>場景顯示 P(0)</th></tr>'
        '<tr><td>一個 S</td><td>H → S → H</td><td></td><td></td></tr>'
        '<tr><td>兩個 S</td><td>H → S → S → H</td><td></td><td></td></tr>'
        '<tr><td>Z 兩次</td><td>H → Z → Z → H</td><td></td><td></td></tr></table>'
        '<div class="box" style="margin-top:6mm"><h3>我的關卡</h3><p>關卡名稱：＿＿＿＿＿＿＿＿</p>'
        '<p>爸爸可以偷偷加的閘：＿＿＿＿＿＿＿＿＿＿</p><p>偵探要怎麼做才看得出來（參考解）：</p>'
        '<div class="line"></div><div class="line"></div><p>爸爸有沒有破案？＿＿＿＿</p></div>',
        '<h2>最後一關：教爸爸看見相位</h2><div class="box"><ul class="chk">'
        '<li>說出什麼是相位（繞赤道轉圈的角度）</li><li>說出兩支赤道箭頭機率一樣、相位不一樣</li>'
        '<li>說出 Z 只改相位、不改機率</li><li>說出怎麼看見相位：先按 H，再測量</li>'
        '<li>指出一個限制：直接測量看不出相位</li><li>替相位猜猜看紀錄取名字、存檔</li></ul></div>'
        '<div class="box" style="margin-top:6mm"><h3>閘對照表（理想情況）</h3>'
        '<table><tr><th>閘的順序</th><th>得到 0</th></tr>'
        + ''.join(f'<tr><td>{" → ".join(seq)}</td><td>{pct(run(seq))}</td></tr>' for _, seq in LEVELS[:4])
        + '</table></div>',
    ]
    return printpack.document('Q005 相位猜猜看 列印包', '父子科技學院 量子電腦學程 Q005｜相位猜猜看', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q005-phase-hidden', folder='Q005_相位猜猜看', files=FILES,
        sheet=('03_相位猜猜看紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_相位猜猜看.pdf', pack_pages=4,
        pack_needles=('直接量就猜', '相位猜猜看紀錄', '先轉再量', '兩步的關卡', '最後一關', '閘對照表'),
        authoring_dir=XINEW / 'authoring/q005', episode_dir='specials/q005-phase-hidden',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'gateTable': {' '.join(seq): round(run(seq), 4) for _, seq in LEVELS}, 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q005/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')
