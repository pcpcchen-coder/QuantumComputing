"""Q085 課堂教材：低於門檻 — 動畫操作步驟、門檻曲線紀錄、效能競賽紀錄、解讀實驗圖（算 Λ）、說明卡與解答。

免安裝、不需帳號：只用學程的 animations/operation.html#qec 與 transmon-3d.html#surface，用瀏覽器開啟。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q085/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 以 js/operation/11_qec.js 自己的解碼器與 trial() 重算（Node 移植，每點 20000 次；只有資料 X 錯誤、量測完美）
# (實體錯誤率 %, d=3, d=5, d=7 邏輯錯誤率 %)
MC = [(1, 0.17, 0.03, 0.00), (2, 0.69, 0.20, 0.06), (3, 1.58, 0.65, 0.31), (5, 3.67, 2.44, 1.67),
      (8, 8.43, 7.66, 7.42), (9, 9.95, 9.90, 9.90), (10, 12.08, 12.55, 12.88), (12, 15.63, 17.90, 18.87),
      (20, 30.45, 36.78, 41.45)]
PTS = [p for p, *_ in MC]
QUBITS = {d: 2 * d * d - 1 for d in (3, 5, 7)}
assert QUBITS == {3: 17, 5: 49, 7: 97}


def lam(a, b):
    return round(a / b, 2)


# 練習用：同一個錯誤率下，相鄰碼距相除得到 Λ
LAM = [(p, lam(a, b), lam(b, c)) for p, a, b, c in MC if p in (3, 5, 12)]   # 3%：2.43、2.1；5%：1.5、1.46；12%：0.87、0.95

FILES = {
'00_爸爸先讀.md': f'''# 父子科技學院 量子電腦學程 Q085：低於門檻（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶出一個問題：把表面碼做得更大，邏輯錯誤一定會變少嗎？答案：只有實體錯誤率低於門檻時才會。

只需要瀏覽器：下載學程的 `animations/` 資料夾，開 `operation.html#qec`（主要）和 `transmon-3d.html#surface`（第 7 步）。不需要網路、帳號或安裝。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 碼距與門檻、門檻定理、Λ | 影片第 3–6 段、`05_動畫導覽.md` |
| 25–65 | 用「跑 2000 輪」量不同 d、p 的邏輯錯誤率，畫門檻曲線；玩效能競賽 | `01_操作步驟.md`、列印包第 1–2 頁 |
| 65–75 | 休息 | |
| 75–105 | 解讀一份公開的低於門檻實驗圖，算 Λ | 列印包第 3 頁 |
| 105–115 | 孩子教爸爸：門檻是什麼、為什麼低於門檻碼越大越好 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 先自己在 `#qec` 試一次：按「d = 3」、把「實體錯誤率 p」拉到 5%、按「跑 2000 輪（只統計）」，在左側面板下方讀出「邏輯錯誤率 ≈ …%」（面板可往下捲）。
- 列印 `02_列印包_低於門檻.pdf`（A4，共 4 頁）。讀一遍 `04_解答.md`。

## 效能競賽怎麼玩

爸爸設定一個實體錯誤率，挑一個碼距，跑 2000 輪，記下邏輯錯誤率；孩子在同一個錯誤率換另一個碼距再跑。邏輯錯誤率低的人得一分。至少要有一回合把錯誤率設在 15% 以上——這時小碼距會贏。

## 誠實說明

- 動畫的模型只有資料位元的 X 錯誤、量測完美，所以門檻約 9–10%；真實電路（閘與量測也會錯）的表面碼門檻約 1%。
- 每次「跑 2000 輪」都是隨機的，結果會和解答差一點；在錯誤率很低時，邏輯錯誤可能一次都沒有。
- 高於門檻時，碼距越大反而越糟——這是本課最重要的注意事項。
''',

'01_操作步驟.md': '''# 操作步驟

## A. 量一個點（`operation.html#qec`，約 5 分鐘）

1. 按「d = 3」（或 d = 5、d = 7）選碼距。
2. 拉「實體錯誤率 p（每個資料量子位元）」滑桿到想要的值（0.5%–20%）。改錯誤率或碼距都會把統計清零。
3. 按「跑 2000 輪（只統計）」，在面板下方讀出「邏輯錯誤率 ≈ …%」。想更準可以多按幾次（輪數會累加）。

## B. 畫門檻曲線（約 25 分鐘）

1. 用列印包第 1 頁的表，對 p = 2%、5%、8%、10%、12%、20% 各量 d = 3、5、7。
2. 把點畫在第 1 頁的方格上，同一個碼距連成一條線（藍 d=3、黃 d=5、紅 d=7，和動畫右下角小圖的顏色一樣）。
3. 找出三條線交叉的地方，寫下「我量到的門檻約 ＿＿%」。
4. 和右下角小圖（場景自己算的曲線）比一比。

## C. 效能競賽（約 10 分鐘）

照「00_爸爸先讀」的規則玩，記在列印包第 2 頁。

## D. 看真實電路的閾值（`transmon-3d.html#surface`，約 5 分鐘）

1. 取消勾選「自動接續」，按步驟按鈕「7」（碼距與閾值）。
2. 看後方看板右邊：d = 3、5、7、11 四條線，紅色虛線是閾值約 1%。
3. 等看板左邊多出 Willow 那一行（Λ ≈ 2.1）。

## E. 下半場：解讀一份低於門檻實驗圖（約 30 分鐘）

用列印包第 3 頁：讀出 d = 3、5、7 三個點、相鄰相除算 Λ、判斷是不是低於門檻。
''',

'04_解答.md': '# 解答（爸爸用）\n\n## 邏輯錯誤率（以動畫自己的解碼器重算，每點 2 萬次）\n\n'
  '| 實體錯誤率 | d = 3 | d = 5 | d = 7 |\n|---|---|---|---|\n'
  + ''.join(f'| {p}% | {a:.2f}% | {b:.2f}% | {c:.2f}% |\n' for p, a, b, c in MC)
  + '\n- 交叉在約 9–10%：低於它，d = 7 最好；高於它，d = 7 最差。\n'
  '- 動畫右下角小圖每點只跑 1000 次，低錯誤率時可能 0 次失敗（畫在最下面）；孩子自己跑 2000 輪也會和表格差一點。\n\n'
  '## 用場景數字練習算 Λ（相鄰碼距相除）\n\n| 實體錯誤率 | Λ（d3 ÷ d5） | Λ（d5 ÷ d7） | 判斷 |\n|---|---|---|---|\n'
  + ''.join(f'| {p}% | {x} | {y} | {"低於門檻" if min(x, y) > 1 else "高於門檻"} |\n' for p, x, y in LAM)
  + '\n## 真實硬體：Google Willow（學程簡報第 50 頁）\n\n'
  '- d = 3 → 5 → 7，每加 2 邏輯錯誤率約減半，Λ ≈ 2.14；第一次在硬體上清楚看到低於門檻。\n'
  '- d = 7 用 101 個量子位元，每輪邏輯錯誤約 0.143%，邏輯位元壽命約是最好實體位元的 2.4 倍。\n'
  '- 照 Λ 外推到 10⁻⁶：d ≈ 27，約 1,500 顆實體位元／邏輯位元（2 × 27² − 1 = 1457）。\n\n'
  '## 實體位元數（2d² − 1）\n\n' + '、'.join(f'd = {d}：{n} 顆' for d, n in QUBITS.items()) + '\n\n'
  '## 常見問題\n\n'
  '- 為什麼高於門檻碼越大越糟？位元越多，同時出錯的機會增加得比能修的錯還快。\n'
  '- 為什麼動畫的門檻是 9–10%，真實的是 1%？動畫只讓資料位元出錯、量測完美；真實電路的閘、量測、重設都會錯。\n'
  '- 縱軸為什麼用對數？每加 2 是「乘上同一個倍數」，在對數座標上就是等間隔，趨勢一眼看出。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路或帳號。

## `operation.html#qec`（操作場景 11：雜訊與量子錯誤更正：表面碼）

- 碼距按鈕：d = 3、d = 5、d = 7（預設 5）。棋盤上方金色字寫出資料、量測、實體量子位元數。
- 滑桿「實體錯誤率 p（每個資料量子位元）」：0.5%–20%，預設 5%。
- 「自動循環」：一輪一輪自動跑；紅球＝錯誤、橘色柱子＝症狀、綠線＝解碼器推測的錯誤鏈。
- 「下一步」：手動一步一步；「跑 2000 輪（只統計）」：只算統計，結果在面板下方。
- 右下角小圖：邏輯錯誤率 vs 實體錯誤率（即時蒙地卡羅），藍 d=3、黃 d=5、紅 d=7；白線＝目前的 p；虛線＝不編碼。

## `transmon-3d.html#surface`（第 10 章：表面碼）

- 步驟 7「碼距與閾值」：看板右邊 d = 3、5、7、11 四條線與閾值約 1% 的紅色虛線；左邊算式會加上 Willow 與資源估計。
- 步驟 8「自由實驗」：可點位元注入錯誤、跑 300 次統計（這個模型的閾值約 10–15%，因為包含 X、Y、Z 三種錯誤）。

## 操作

`H` 隱藏面板；滑鼠拖曳旋轉、滾輪縮放。
''',
}

SHEET_HEADER = ['項目', '碼距 d', '實體錯誤率（%）', '跑了幾輪', '邏輯錯誤次數', '邏輯錯誤率（%）', '誰贏', '備註']
SHEET_ROWS = ([['門檻曲線', str(d), str(p), '', '', '', '', ''] for p in (2, 5, 8, 10, 12, 20) for d in (3, 5, 7)]
              + [[f'效能競賽第 {i} 回合', '', '', '', '', '', '', ''] for i in range(1, 7)])

EXTRA_CSS = '''table.rec td{height:8mm}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.card{border:2pt solid #0b2540;border-radius:4mm;padding:5mm;margin-top:4mm}.card h3{margin-top:0}
.grid{height:62mm;border:1pt solid #0b2540;background-image:linear-gradient(#ccd 1px,transparent 1px),linear-gradient(90deg,#ccd 1px,transparent 1px);background-size:10mm 10mm}'''


def html():
    pages = [
        '<h2>實驗一：畫門檻曲線（今天的作品）</h2><p class="lead">在 operation.html#qec：選 d → 設 p → 跑 2000 輪 → 讀邏輯錯誤率。</p>'
        '<table class="rec"><tr><th>實體錯誤率 p</th><th>d = 3</th><th>d = 5</th><th>d = 7</th><th>誰最低</th></tr>'
        + ''.join(f'<tr><td>{p}%</td><td></td><td></td><td></td><td></td></tr>' for p in (2, 5, 8, 10, 12, 20)) + '</table>'
        '<div class="card"><h3>門檻曲線</h3><p>橫軸：實體錯誤率　縱軸：邏輯錯誤率（三條線：d = 3、5、7）</p><div class="grid"></div>'
        '<p>我量到的門檻約：＿＿＿%　作品名稱：＿＿＿＿＿＿＿＿　日期：＿＿＿＿</p></div>',
        '<h2>效能競賽：誰的邏輯錯誤少</h2><p class="lead">同一個錯誤率，各挑一個碼距跑 2000 輪；邏輯錯誤率低的人得一分。</p>'
        '<table class="rec"><tr><th>回合</th><th>錯誤率 p</th><th>爸爸的 d</th><th>爸爸的結果</th><th>我的 d</th><th>我的結果</th><th>誰贏</th></tr>'
        + ''.join(f'<tr><td>{i}</td><td></td><td></td><td></td><td></td><td></td><td></td></tr>' for i in range(1, 7)) + '</table>'
        '<p class="note">小碼距在什麼錯誤率會贏？＿＿＿＿　為什麼？＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p>',
        '<h2>換你改造：解讀低於門檻實驗圖</h2><p class="lead">找一張公開的結果圖（例如 Google Willow），讀點、相除、判斷。</p>'
        '<table class="rec"><tr><th>碼距</th><th>讀到的邏輯錯誤率</th><th>和下一個相除（Λ）</th></tr>'
        '<tr><td>d = 3</td><td></td><td>d3 ÷ d5 =</td></tr><tr><td>d = 5</td><td></td><td>d5 ÷ d7 =</td></tr><tr><td>d = 7</td><td></td><td>—</td></tr></table>'
        '<p>Λ 大於 1 嗎？＿＿　所以是（低於／高於）門檻。</p><p>縱軸是對數刻度嗎？＿＿　每一格代表乘上幾倍？＿＿＿</p>'
        '<p>簡報上的答案：Willow 的 Λ ≈ 2.14。我算的和它差多少？＿＿＿＿</p>'
        '<p class="note">生活技能：看懂趨勢圖——先看座標軸，再看線往哪裡走。你還在哪裡看過對數座標？＿＿＿＿＿＿</p>',
        '<h2>說明卡與最後一關</h2><div class="box"><p>1. 門檻是什麼？</p><div class="line"></div>'
        '<p>2. 低於門檻時，碼距加大會怎樣？</p><div class="line"></div><p>3. Λ 是什麼？怎麼算？</p><div class="line"></div>'
        '<p>4. 一個限制或注意事項：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出門檻：兩股力量打平的錯誤率</li><li>說出低於門檻：碼距越大，邏輯錯誤越少</li>'
        '<li>說出動畫模型（約 9–10%）和真實電路（約 1%）為什麼不同</li><li>指出一個限制：高於門檻，碼距越大越糟</li>'
        '<li>替門檻曲線取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q085 低於門檻 列印包', '父子科技學院 量子電腦學程 Q085｜低於門檻', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q085-below-threshold', folder='Q085_低於門檻', files=FILES,
        sheet=('03_門檻曲線與競賽紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_低於門檻.pdf', pack_pages=4,
        pack_needles=('門檻曲線', '效能競賽', '解讀低於門檻實驗圖', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q085', episode_dir='specials/q085-below-threshold',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'scenes': ['animations/operation.html#qec', 'animations/transmon-3d.html#surface'],
               'logicalErrorPct': {f'{p}%': {'d3': a, 'd5': b, 'd7': c} for p, a, b, c in MC},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q085/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')
