"""Q071 課堂教材：螢光讀取與 QCCD — 動畫操作步驟、閾值選擇卡、盲測紀錄、搬運時間占比計算、說明卡與解答。

免安裝、不需帳號：只用學程的 animations/atoms.html（#ionqubit、#qccd），用瀏覽器開啟。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q071/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 動畫 06_qccd.js 標示的一層線路時間組成（示意代表值，μs）
LAYER = [('搬運＋分離／合併', 400), ('共冷（重新冷卻）', 300), ('偵測', 150), ('兩位元閘', 50), ('單位元閘', 10)]
TOTAL = sum(v for _, v in LAYER)
assert TOTAL == 910
PCT_MOVE = round(100 * 400 / TOTAL, 1)            # 44.0
PCT_MOVE_COOL = round(100 * 700 / TOTAL, 1)       # 76.9
PCT_GATES = round(100 * 60 / TOTAL, 1)            # 6.6

# 以 03_ionqubit.js 的光子模型重算（R=0.1/μs、BG=0.0005/μs、τ₁=10 ms、τ₀=100 ms；20 萬次）
DET = [(50, 0, 98.4), (100, 1, 99.8), (200, 2, 99.8), (300, 2, 99.7), (500, 3, 99.6)]

FILES = {
'00_爸爸先讀.md': f'''# 父子科技學院 量子電腦學程 Q071：螢光讀取與 QCCD（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶出兩個問題：離子算完之後怎麼讀出零或一？離子變多了怎麼搬？

只需要瀏覽器：下載學程的 `animations/` 資料夾，開 `atoms.html#ionqubit` 和 `atoms.html#qccd`。不需要網路、帳號或安裝。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 狀態相依螢光、讀取四步、亮暗光子數 | 影片第 3–5 段、`05_動畫導覽.md` |
| 25–65 | 改偵測時間看閾值、玩盲測十回合、看離子搬運 | `01_操作步驟.md`、列印包第 1–2 頁 |
| 65–75 | 休息 | |
| 75–105 | 算搬運時間占一層線路的比例 | 列印包第 3 頁、`03_盲測與計算紀錄.csv` |
| 105–115 | 孩子教爸爸：怎麼讀取、為什麼要搬 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 先自己在 `#ionqubit` 走一次：① 冷卻 → ② 光泵浦 → ④ 微波 π → ⑤ 偵測，看下方讀數出現「上一次偵測：N 個光子 → 判為 |1⟩」。
- 列印 `02_列印包_螢光讀取與QCCD.pdf`（A4，共 4 頁）。讀一遍 `04_解答.md`。

## 盲測怎麼玩

孩子背對螢幕。爸爸按 ② 光泵浦（得到 0），想出 1 就再按 ④ 微波 π，然後按 ⑤ 偵測，只念出讀數上的光子數。孩子用自己寫在選擇卡上的閾值說出 0 或 1，爸爸公布答案。

## 誠實說明

- 動畫的光子數、閾值與保真度是用代表值的模型算的（亮態每微秒 0.1 個、背景很小），不是某台機器的量測。
- 一層線路的時間組成（400／300／150／50／10 μs）是動畫標示的示意代表值。
- 搬運會加熱離子，搬完要再冷卻——這是本課最重要的注意事項。
''',

'01_操作步驟.md': '''# 操作步驟

## A. 偵測時間與閾值（`atoms.html#ionqubit`，約 15 分鐘）

1. 按「重置」，再按「② 光泵浦初始化 |0⟩」、「③ 微波 π/2」：離子變成一半 0、一半 1。
2. 按「一次跑 1000 shots」。看直方圖：藍色（真值 0）、紅色（真值 1），右上角寫著閾值與判別保真度。
3. 把「偵測時間 (μs)」拉到 50，再按一次 1000 shots；再試 100、300、500。每次把閾值和保真度記在列印包第 1 頁。
4. 選一個你覺得最好的偵測時間與閾值，寫在「讀取閾值選擇卡」上，並寫下理由。

## B. 盲測（約 15 分鐘，十回合）

爸爸照「00_爸爸先讀」出題，孩子只聽光子數判讀，記在列印包第 2 頁。

## C. 看離子搬運（`atoms.html#qccd`，約 10 分鐘）

1. 按「單步」七次，每一步讀畫面上方的步驟名稱：分離搬運、合併、共冷、兩位元閘、經接面轉向偵測區、偵測、搬回。
2. 看右側插圖「一層線路的時間組成」，哪一列亮起來，就是現在在做的事。
3. 再按「▶ 執行一段線路」一口氣看完。

## D. 下半場：算搬運時間占比（約 30 分鐘）

用列印包第 3 頁的表，把五項時間加起來，算出搬運占多少、搬運加冷卻占多少、閘占多少。
''',

'04_解答.md': '# 解答（爸爸用）\n\n## 偵測時間與閾值（以動畫自己的光子模型重算，20 萬次）\n\n'
  '| 偵測時間 | 亮態平均光子數 | 閾值（> 幾個判為 1） | 判別保真度 |\n|---|---|---|---|\n'
  + ''.join(f'| {t} μs | {t // 10} | > {th} | 約 {f}% |\n' for t, th, f in DET)
  + '\n動畫每次只用 3000 次校準，畫面上的保真度會和表格差 0.1–0.2 個百分點。重點：太短（50 μs）光子太少、兩堆重疊；拉到很長也沒有更好，因為亮態在偵測中途可能被打成暗態。100–200 μs 附近最好。\n\n'
  '## 一層線路的時間組成（動畫示意代表值）\n\n| 項目 | 時間（μs） |\n|---|---|\n'
  + ''.join(f'| {n} | {v} |\n' for n, v in LAYER)
  + f'| 合計 | {TOTAL} |\n\n- 搬運占：400 ÷ {TOTAL} ≈ {PCT_MOVE}%\n- 搬運＋冷卻占：700 ÷ {TOTAL} ≈ {PCT_MOVE_COOL}%\n- 兩種閘合計：60 ÷ {TOTAL} ≈ {PCT_GATES}%\n\n'
  '## 常見問題\n\n'
  '- 為什麼 |1⟩ 亮、|0⟩ 暗？偵測光只和 |1⟩ 的循環躍遷共振；|0⟩ 差了 14.7 GHz，幾乎不吸光。\n'
  '- 為什麼收到的光子不多？離子每秒散射數百萬個光子，但物鏡只收集約 1–5%。\n'
  '- 為什麼要配共冷離子？搬運會加熱離子；用另一種元素冷卻，雷射不會碰到量子位元的狀態。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路或帳號。

## `atoms.html#ionqubit`（離子阱場景 3：離子量子位元）

- 按鈕：① Doppler 冷卻、② 光泵浦初始化 |0⟩、③ 微波 π/2、④ 微波 π、⑤ 偵測（螢光）、一次跑 1000 shots、重置。
- 滑桿「偵測時間 (μs)」：50–500。改動後直方圖清空、閾值重新校準。
- 右下直方圖：藍色是真值 |0⟩、紅色是真值 |1⟩；右上角是閾值、判別保真度、亮態平均。

## `atoms.html#qccd`（離子阱場景 6：QCCD 搬運架構）

- 「▶ 執行一段線路」：七步一口氣跑完；「單步」：一次一步。
- 金色是量子位元離子 ¹³⁷Ba⁺、紫色是共冷離子 ¹⁷¹Yb⁺；載入區、記憶區、閘區、偵測區、儲存區與 X 接面。
- 開關「顯示 DC 電極電壓」：離子附近的電極會亮，示意電壓波形推動位能井。

## 操作

`H` 隱藏面板；滑鼠拖曳旋轉、滾輪縮放。
''',
}

SHEET_HEADER = ['項目', '偵測時間（μs）', '閾值', '保真度（%）', '爸爸準備的答案', '光子數', '我的判讀', '對嗎', '備註']
SHEET_ROWS = ([['偵測時間實驗', str(t), '', '', '', '', '', '', ''] for t, *_ in DET]
              + [[f'盲測第 {i} 回合', '', '', '', '', '', '', '', ''] for i in range(1, 11)])

EXTRA_CSS = '''table.rec td{height:9mm}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.card{border:2pt solid #0b2540;border-radius:4mm;padding:5mm;margin-top:5mm}.card h3{margin-top:0}'''


def html():
    pages = [
        '<h2>實驗一：偵測時間和閾值</h2><p class="lead">在 atoms.html#ionqubit：② 光泵浦 → ③ 微波 π/2 → 一次跑 1000 shots。改偵測時間，記下右上角的數字。</p>'
        '<table class="rec"><tr><th>偵測時間</th><th>亮態平均</th><th>閾值（&gt; 幾個）</th><th>判別保真度</th><th>兩堆分得開嗎</th></tr>'
        + ''.join(f'<tr><td>{t} μs</td><td></td><td></td><td></td><td></td></tr>' for t, *_ in DET) + '</table>'
        '<div class="card"><h3>讀取閾值選擇卡（今天的作品）</h3><p>我選的偵測時間：＿＿＿＿ μs　閾值：超過＿＿＿個光子判為 1</p>'
        '<p>理由：</p><div class="line"></div><div class="line"></div><p>作品名稱：＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p></div>',
        '<h2>盲測：爸爸出題、你判讀</h2><p class="lead">你背對螢幕，只聽光子數。用選擇卡上的閾值說出 0 或 1。</p>'
        '<table class="rec"><tr><th>回合</th><th>光子數</th><th>我的判讀</th><th>答案</th><th>對嗎</th><th>錯的話：亮判暗／暗判亮</th></tr>'
        + ''.join(f'<tr><td>{i}</td><td></td><td></td><td></td><td></td><td></td></tr>' for i in range(1, 11)) + '</table>'
        '<p class="note">猜錯幾次？＿＿　想一想：要改閾值，還是改偵測時間？＿＿＿＿＿＿＿＿＿＿</p>',
        '<h2>換你改造：搬運占了多少時間</h2><p class="lead">atoms.html#qccd 右側插圖：一層線路的時間組成（示意代表值）。</p>'
        '<table class="rec"><tr><th>項目</th><th>時間（μs）</th></tr>'
        + ''.join(f'<tr><td>{n}</td><td>{v}</td></tr>' for n, v in LAYER) + '<tr><td>合計</td><td></td></tr></table>'
        '<p>搬運占：400 ÷ ＿＿＿ ≈ ＿＿＿%</p><p>搬運＋冷卻占：＿＿＿ ÷ ＿＿＿ ≈ ＿＿＿%</p><p>兩種閘合計占：＿＿＿ ÷ ＿＿＿ ≈ ＿＿＿%</p>'
        '<p class="note">生活技能：物流也是系統效能——貨車再快，倉庫搬貨慢，整體還是慢。你想到哪個例子？＿＿＿＿＿＿＿＿</p>',
        '<h2>說明卡與最後一關</h2><div class="box"><p>1. 離子的 0 和 1 怎麼用螢光分辨？</p><div class="line"></div>'
        '<p>2. 閾值要怎麼選？</p><div class="line"></div><p>3. 為什麼要把離子搬來搬去？</p><div class="line"></div>'
        '<p>4. 一個限制或注意事項：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出讀取原理：1 亮、0 暗、數光子</li><li>說出閾值怎麼選：兩種錯誤加起來最少</li>'
        '<li>說出偵測時間太短會怎樣</li><li>指出一個限制：搬運會加熱離子，搬完要再冷卻</li>'
        '<li>替閾值選擇卡取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q071 螢光讀取與 QCCD 列印包', '父子科技學院 量子電腦學程 Q071｜螢光讀取與 QCCD', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q071-fluorescence-qccd', folder='Q071_螢光讀取與QCCD', files=FILES,
        sheet=('03_盲測與計算紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_螢光讀取與QCCD.pdf', pack_pages=4,
        pack_needles=('偵測時間', '閾值選擇卡', '盲測', '搬運占了多少時間', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q071', episode_dir='specials/q071-fluorescence-qccd',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'scenes': ['animations/atoms.html#ionqubit', 'animations/atoms.html#qccd'],
               'layerTimesUs': dict(LAYER), 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q071/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')
