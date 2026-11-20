"""Q081 課堂教材：錯誤預算：線路能跑多深 — 計算步驟、錯誤預算表、基準測試紀錄、模擬器驗證、說明卡與解答。

免安裝、不需帳號：計算機加上學程的 animations/operation.html#circuit（用瀏覽器開啟，當作本機模擬器）。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q081/classroom.py
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

# 錯誤預算：成功率掉到底線 B 之前能跑幾個閘 G = ln(B) / ln(F)（取整數）
FIDS = [0.99, 0.999, 0.9999]
BASES = [0.9, 0.5]
BUDGET = {(f, b): int(math.log(b) / math.log(f)) for f in FIDS for b in BASES}
assert BUDGET[(0.99, 0.5)] == 68 and round(math.log(0.5) / math.log(0.99)) == 69
HALF = {f: round(math.log(0.5) / math.log(f)) for f in FIDS}   # 69、693、6931（四捨五入，影片用）
assert HALF == {0.99: 69, 0.999: 693, 0.9999: 6931}
P100 = {f: round(100 * f ** 100, 1) for f in FIDS}             # 36.6、90.5、99.0
EX_SLIDE = round(math.log(0.5) / math.log(0.997))              # 簡報例子：0.3% → 約 231（簡報寫約 230）
GATES_PER_LAYER = 10

# 06_circuit.js 的雜訊模型：每閘 1%（出錯就輸出均勻隨機結果）、每個量測位元 3% 翻轉
CIRCS = [('Bell 態', 2, 2, ['00', '11']), ('干涉：H–Z–H', 3, 1, ['1']), ('Grover 搜尋', 12, 2, ['11'])]


def budget(g, m):
    return 0.99 ** g * 0.97 ** m


def expected(g, m, good):
    """以動畫自己的模型算期望的「理想答案」比例（含隨機落回正確、讀取翻轉）。"""
    K = 1 << m
    pg = 1 - 0.99 ** g
    ideal = [0.0] * K
    for s in good:
        ideal[int(s, 2)] = 1 / len(good)
    pre = [(1 - pg) * ideal[k] + pg / K for k in range(K)]
    out = [0.0] * K
    for k in range(K):
        for j in range(K):
            flips = bin(k ^ j).count('1')
            out[j] += pre[k] * 0.03 ** flips * 0.97 ** (m - flips)
    return sum(out[int(s, 2)] for s in good)


SIM = [(n, g, m, round(100 * budget(g, m), 1), round(100 * expected(g, m, good), 1)) for n, g, m, good in CIRCS]

FILES = {
'00_爸爸先讀.md': f'''# 父子科技學院 量子電腦學程 Q081：錯誤預算：線路能跑多深（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶出一個問題：每個閘都有一點點出錯的機會，一條線路最多能跑多深？

需要：計算機（手機也可以）和瀏覽器。下載學程的 `animations/` 資料夾，開 `operation.html#circuit` 當本機模擬器。不需要網路、帳號或安裝。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 保真度、錯誤率、連乘公式、0.69 ÷ ε 估法 | 影片第 3–7 段 |
| 25–65 | 算 99%、99.9%、99.99% 能跑幾個閘、幾層，填錯誤預算表 | `01_操作步驟.md`、列印包第 1 頁 |
| 65–75 | 休息 | |
| 75–105 | 基準測試：先估再用模擬器跑，比較預算和實測 | 列印包第 2–3 頁、`03_預算與實測紀錄.csv` |
| 105–115 | 孩子教爸爸：為什麼連乘、多一個九差多少 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 先自己在 `#circuit` 走一次：選「Grover 搜尋」→ 按「播放」→ 看右下直方圖；再打開「加入雜訊（每閘 1%、讀取 3%）」，看 11 那根柱子變矮。
- 列印 `02_列印包_錯誤預算.pdf`（A4，共 4 頁）。讀一遍 `04_解答.md`。

## 誠實說明

- 連乘假設每個錯誤彼此獨立，是粗估。真實的錯誤可能好幾個一起發生（相關錯誤），也可能漏到 0 和 1 以外的能階（洩漏）。
- 動畫的雜訊是簡化模型：出錯就輸出隨機結果，所以有時會剛好落回正確答案，實測常比預算高一點。
- 「一層 {GATES_PER_LAYER} 個閘」只是方便換算的假設。
''',

'01_操作步驟.md': f'''# 操作步驟

## A. 錯誤預算表（計算機，約 25 分鐘）

1. 錯誤率 ε = 1 − 保真度 F。
2. 跑 G 個閘全部做對的機會 ≈ F^G。先算 F = 0.99、0.999、0.9999 各跑 100 個閘的成功率。
3. 定一條底線（例如 50% 或 90%），找出能跑幾個閘：G = log(底線) ÷ log(F)；好記的估法：剩一半時 G ≈ 0.69 ÷ ε。
4. 假設一層有 {GATES_PER_LAYER} 個閘，把閘數除以 {GATES_PER_LAYER} 得到層數，填進列印包第 1 頁。

## B. 基準測試（`operation.html#circuit`，約 30 分鐘）

1. 爸爸選一個範例線路（Bell 態、干涉：H–Z–H、Grover 搜尋），孩子數出有幾個閘、量幾個位元。
2. 孩子算預算：0.99^閘數 × 0.97^量測位元數，寫在列印包第 2 頁。
3. 爸爸打開「加入雜訊（每閘 1%、讀取 3%）」，按「播放」跑到測量欄，記下理想答案出現幾次（下方讀數或直方圖）。
4. 比一比：預算和實測差多少？想想為什麼。
''',

'04_解答.md': '# 解答（爸爸用）\n\n## 跑 100 個閘全部做對的機會\n\n| 保真度 | 成功率 |\n|---|---|\n'
  + ''.join(f'| {f * 100:g}% | 約 {P100[f]}% |\n' for f in FIDS)
  + '\n## 錯誤預算表（成功率掉到底線前能跑幾個閘，取整數；一層 10 個閘）\n\n'
  '| 保真度 | 底線 90%：閘數 | 層數 | 底線 50%：閘數 | 層數 |\n|---|---|---|---|---|\n'
  + ''.join(f'| {f * 100:g}% | {BUDGET[(f, 0.9)]} | {BUDGET[(f, 0.9)] // GATES_PER_LAYER} | {BUDGET[(f, 0.5)]} | {BUDGET[(f, 0.5)] // GATES_PER_LAYER} |\n' for f in FIDS)
  + f'\n影片用四捨五入說「約 69、693、6931 個閘」（ln 0.5 ÷ ln F = {", ".join(f"{math.log(0.5) / math.log(f):.1f}" for f in FIDS)}）。'
  f'估法 0.69 ÷ ε 得 69、690、6900，錯誤率越小越準。簡報例子：錯誤率 0.3% → ln 0.5 ÷ ln 0.997 ≈ {EX_SLIDE}（簡報寫約 230）。\n\n'
  '## 模擬器驗證（以 06_circuit.js 的雜訊模型計算）\n\n| 線路 | 閘數 | 量測位元 | 預算 0.99^G × 0.97^m | 理想答案的期望比例 |\n|---|---|---|---|---|\n'
  + ''.join(f'| {n} | {g} | {m} | 約 {b}% | 約 {e}% |\n' for n, g, m, b, e in SIM)
  + '\n實測（1000 次）會在期望值上下差約 1 個百分點。期望比預算高，是因為動畫裡做錯的那幾次會隨機輸出結果，有時剛好落回正確答案。\n\n'
  '## 常見問題\n\n'
  '- 為什麼用乘的？每一步都要做對，整條才算對；獨立事件同時發生的機率要相乘。\n'
  '- 為什麼多一個九，深度約十倍？剩一半的閘數約 0.69 ÷ ε，ε 變成十分之一，閘數就變十倍。\n'
  '- 連乘的限制？假設錯誤彼此獨立；實際上錯誤可能相關（一起發生），也可能洩漏到 |2⟩ 等計算空間以外的能階。\n'
  '- 那要跑數十億個閘怎麼辦？硬體錯誤率約 10⁻³–10⁻⁴，離 10⁻¹⁰ 太遠，要靠量子錯誤更正（簡報第 47 頁）。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路或帳號。

## `operation.html#circuit`（操作場景 6：量子線路——一步一步執行）

- 範例按鈕：Bell 態、GHZ 態、干涉：H–Z–H、Deutsch–Jozsa、Bernstein–Vazirani、Grover 搜尋、量子隱形傳態、QFT。
- 「⏮ 重設」「單步 ▶」「播放」：播放每 1.3 秒走一欄；走到最後的量測欄會跑 1000 shots。
- 開關「加入雜訊（每閘 1%、讀取 3%）」：出錯機會 = 1 − 0.99^閘數，出錯時輸出隨機結果；每個量測位元再有 3% 被讀錯。
- 右下直方圖：柱子是 1000 次的結果，青線是理想機率。

## 操作

`H` 隱藏面板；滑鼠拖曳旋轉、滾輪縮放。
''',
}

SHEET_HEADER = ['項目', '保真度或線路', '閘數', '量測位元', '預算成功率（%）', '實測理想答案次數（/1000）', '差多少', '備註']
SHEET_ROWS = ([['錯誤預算', f'{f * 100:g}%', '', '', '', '', '', ''] for f in FIDS]
              + [['模擬器驗證', n, str(g), str(m), '', '', '', ''] for n, g, m, *_ in SIM]
              + [[f'基準測試第 {i} 回合', '', '', '', '', '', '', ''] for i in range(1, 7)])

EXTRA_CSS = '''table.rec td{height:9mm}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.card{border:2pt solid #0b2540;border-radius:4mm;padding:5mm;margin-top:5mm}.card h3{margin-top:0}'''


def html():
    pages = [
        '<h2>錯誤預算表（今天的作品）</h2><p class="lead">成功率 ≈ 保真度 F 的閘數次方。能跑幾個閘：G = log(底線) ÷ log(F)；剩一半時 G ≈ 0.69 ÷ 錯誤率。一層算 10 個閘。</p>'
        '<table class="rec"><tr><th>保真度</th><th>跑 100 個閘的成功率</th><th>底線 90%：閘數／層數</th><th>底線 50%：閘數／層數</th></tr>'
        + ''.join(f'<tr><td>{f * 100:g}%</td><td></td><td></td><td></td></tr>' for f in FIDS) + '</table>'
        '<div class="card"><h3>我的發現</h3><p>保真度每多一個九，能跑的閘數大約變成＿＿＿倍。</p>'
        '<div class="line"></div><p>作品名稱：＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p></div>',
        '<h2>基準測試：先估再跑</h2><p class="lead">爸爸選線路，你先算預算：0.99^閘數 × 0.97^量測位元數；爸爸打開雜訊跑 1000 次，公布理想答案出現幾次。</p>'
        '<table class="rec"><tr><th>回合</th><th>線路</th><th>閘數</th><th>量測位元</th><th>我的預算</th><th>實測（/1000）</th><th>差多少</th></tr>'
        + ''.join(f'<tr><td>{i}</td><td></td><td></td><td></td><td></td><td></td><td></td></tr>' for i in range(1, 7)) + '</table>'
        '<p class="note">差很多的那一回，漏算了什麼？＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p>',
        '<h2>換你改造：用模擬器驗證</h2><p class="lead">operation.html#circuit 的雜訊：每閘 1%、讀取 3%。三條線路各跑兩次，比較預算和實測。</p>'
        '<table class="rec"><tr><th>線路</th><th>閘數</th><th>量測位元</th><th>預算</th><th>第一次</th><th>第二次</th></tr>'
        + ''.join(f'<tr><td>{n}</td><td>{g}</td><td>{m}</td><td></td><td></td><td></td></tr>' for n, g, m, *_ in SIM) + '</table>'
        '<p>實測比預算高還是低？＿＿＿　為什麼？＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p>'
        '<p class="note">生活技能：小錯累積成大錯——一件事有很多步，每步都要做對。你想到哪個例子？＿＿＿＿＿＿＿＿</p>',
        '<h2>說明卡與最後一關</h2><div class="box"><p>1. 為什麼要把保真度連乘？</p><div class="line"></div>'
        '<p>2. 保真度 99% 和 99.9%，跑 100 個閘差多少？</p><div class="line"></div><p>3. 數十億個閘的演算法要怎麼辦？</p><div class="line"></div>'
        '<p>4. 一個限制或注意事項：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出連乘：每一步都要做對</li><li>說出多一個九，能跑的閘數約十倍</li>'
        '<li>用 0.69 ÷ 錯誤率估一次閘數</li><li>指出一個限制：連乘是粗估，還有相關錯誤與洩漏</li>'
        '<li>替錯誤預算表取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q081 錯誤預算列印包', '父子科技學院 量子電腦學程 Q081｜錯誤預算：線路能跑多深', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q081-error-budget', folder='Q081_錯誤預算', files=FILES,
        sheet=('03_預算與實測紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_錯誤預算.pdf', pack_pages=4,
        pack_needles=('錯誤預算表', '基準測試', '用模擬器驗證', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q081', episode_dir='specials/q081-error-budget',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'scenes': ['animations/operation.html#circuit'],
               'gatesToHalf': {f'{f * 100:g}%': HALF[f] for f in FIDS},
               'simulatorNoise': {'perGate': 0.01, 'readoutPerBit': 0.03}, 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q081/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')
