"""Q075 課堂教材：分區架構與成像讀取 — 動畫操作步驟、分區排程表、相機影像判讀紀錄、中途量測改造、說明卡與解答。

免安裝、不需帳號：只用學程的 animations/atoms.html（#zoned、#imaging），用瀏覽器開啟。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q075/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 動畫 11_zoned.js 插圖「一層的時間組成（代表值）」（μs）
LAYER = [('抓取＋搬運到糾纏區', 250), ('芮德堡 CZ（所有配對並行）', 0.3), ('搬回儲存區', 250)]
LAYER_US = sum(v for _, v in LAYER)                 # 500.3
MID_READ_US = 1000                                  # 插圖「中途讀取（選用）」1 ms
N_LAYERS = 3
TOTAL_PLAIN = round(N_LAYERS * LAYER_US, 1)         # 1500.9
TOTAL_MID = round(TOTAL_PLAIN + MID_READ_US, 1)     # 2500.9
PCT_GATE_PLAIN = round(100 * N_LAYERS * 0.3 / TOTAL_PLAIN, 2)   # 0.06
PCT_GATE_MID = round(100 * N_LAYERS * 0.3 / TOTAL_MID, 2)       # 0.04
PCT_READ_MID = round(100 * MID_READ_US / TOTAL_MID, 1)          # 40.0
assert abs(LAYER_US - 500.3) < 1e-9 and TOTAL_PLAIN == 1500.9 and TOTAL_MID == 2500.9

# 以 12_imaging.js 的模型重算（亮 = 3 × 曝光 ms、暗 = 0.12 × 曝光 + 0.6，卜瓦松；閾值取兩種錯誤平均最小）
EXPO = [(1, 3, 0.72, 2, '81.90'), (2, 6, 0.84, 3, '94.23'), (3, 9, 0.96, 4, '98.11'),
        (5, 15, 1.2, 6, '99.79'), (10, 30, 1.8, 11, '100.00'), (20, 60, 3.0, 20, '100.00')]

FILES = {
'00_爸爸先讀.md': f'''# 父子科技學院 量子電腦學程 Q075：分區架構與成像讀取（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶出兩個問題：上百顆中性原子要在哪裡等待、在哪裡做閘？算完之後怎麼用一張照片讀出每一顆？

只需要瀏覽器：下載學程的 `animations/` 資料夾，開 `atoms.html#zoned` 和 `atoms.html#imaging`。不需要網路、帳號或安裝。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 三個區、一層線路四步、讀取三步 | 影片第 3–8 段、`05_動畫導覽.md` |
| 25–65 | 排出三層線路的分區時程；判讀相機影像 | `01_操作步驟.md`、列印包第 1–2 頁 |
| 65–75 | 休息 | |
| 75–105 | 加入中途量測，重新排時程 | 列印包第 3 頁、`03_排程與判讀紀錄.csv` |
| 105–115 | 孩子教爸爸：三個區的用途、讀取三步 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 先自己在 `#zoned` 按「▶ 執行一層」兩次、「中途量測」一次，看下方讀數「已執行 N 層 · 累計 M 個 CZ」。
- 在 `#imaging` 走一次：準備隨機態 → ① 推出 |1⟩ → ② 成像，看右邊的相機影像與綠框／紅框。
- 列印 `02_列印包_分區架構與成像讀取.pdf`（A4，共 4 頁）。讀一遍 `04_解答.md`。

## 真實任務怎麼玩

把孩子當成實驗室的排程工程師：給他一條三層的線路，他要寫出每一步在哪一區、做什麼、花多久，最後加總。爸爸扮演「主管」，問：哪一步最花時間？能不能更快？

## 誠實說明

- 一層的時間組成（抓取＋搬運 250、CZ 0.3、搬回 250 μs、中途讀取 1 ms）是動畫標示的示意代表值，不是特定機器的量測。
- 成像場景的光子數、閾值與保真度是用示意模型算的；每次「準備隨機態」的結果不同，正確幾顆也會不同。
- 推出 |1⟩ 的讀取方式會失去原子，量完要重新裝載——這是本課最重要的注意事項。
''',

'01_操作步驟.md': '''# 操作步驟

## A. 看一層線路（`atoms.html#zoned`，約 10 分鐘）

1. 按「重置」，再按「▶ 執行一層」。看四步：光錐抓起兩列原子 → 搬到糾纏區 → 粉紅色光片一閃（全域芮德堡脈衝）→ 搬回儲存區。
2. 讀下方讀數：已執行幾層、累計幾個 CZ。
3. 把「並行對數」拉到 8，再按一次「▶ 執行一層」。累計多了幾個？脈衝多了幾道？
4. 看右下插圖「一層的時間組成（代表值）」。

## B. 排出分區時程（約 15 分鐘）

用列印包第 1 頁，替「三層線路」寫下每一步：區域、動作、時間（μs），最後加總。

## C. 判讀相機影像（`atoms.html#imaging`，約 15 分鐘）

1. 按「準備隨機態」：藍色是 |0⟩、紅色是 |1⟩。先在列印包第 2 頁的 5×5 格子畫下哪幾格是紅色。
2. 按「① 推出 |1⟩」：紅色原子飛出光鑷。
3. 按「② 成像」：看相機影像，每一格亮就判 0、暗就判 1。和你畫的答案對照；讀數會寫出「正確 N / 25」。
4. 把「曝光時間 (ms)」改成 1、2、5、10，記下讀數上的閾值和判別保真度。

## D. 下半場：加入中途量測（約 30 分鐘）

1. 在 `#zoned` 按「中途量測」：第四列原子被搬到讀取區拍照，再補上新原子。
2. 在第二層和第三層之間插入一次中途讀取（約 1 ms），用列印包第 3 頁重算總時間與比例。
3. 加分題：開啟 `#imaging` 的「非破壞讀取（另一種做法）」，再走一次，看看哪一種原子發光、原子有沒有被推走。
''',

'04_解答.md': '# 解答（爸爸用）\n\n## 一層的時間組成（動畫示意代表值）\n\n| 項目 | 時間（μs） |\n|---|---|\n'
  + ''.join(f'| {n} | {v} |\n' for n, v in LAYER)
  + f'| 一層合計 | {LAYER_US} |\n\n'
  f'## 三層線路\n\n- 不加中途量測：{N_LAYERS} × {LAYER_US} = {TOTAL_PLAIN} μs；做閘只占 0.9 ÷ {TOTAL_PLAIN} ≈ {PCT_GATE_PLAIN}%\n'
  f'- 加一次中途讀取（1 ms）：{TOTAL_PLAIN} + {MID_READ_US} = {TOTAL_MID} μs；讀取占 ≈ {PCT_READ_MID}%，做閘只占 ≈ {PCT_GATE_MID}%\n'
  '- 一次中途讀取（1000 μs）差不多等於兩層（2 × 500.3 μs）。\n- 動畫的中途量測還要先把原子搬到讀取區，量完補新原子；本表把它們簡化成「中途讀取 1 ms」一行。\n\n'
  '## 曝光時間與判別保真度（以動畫自己的模型重算）\n\n| 曝光 | 亮平均光子 | 暗平均光子 | 閾值（≥ 幾個判為有原子） | 判別保真度 |\n|---|---|---|---|---|\n'
  + ''.join(f'| {e} ms | {b} | {d} | {th} | {f}% |\n' for e, b, d, th, f in EXPO)
  + '\n曝光太短，亮和暗的光子數擠在一起；曝光愈久愈準，但讀取也愈慢。\n\n'
  '## 常見問題\n\n'
  '- 為什麼亮的是 |0⟩？標準做法先用共振光把 |1⟩ 推出光鑷，剩下會發光的都是 |0⟩。\n'
  '- 原子在中途掉了會怎樣？沒有亮點，會被誤判成 |1⟩。\n'
  '- 為什麼要讀取區？把要量的原子搬過去拍照，螢光不會干擾還在儲存區的原子。\n'
  '- 為什麼要補原子？推出讀取是破壞性的，|1⟩ 的原子被打走，量完要重新裝載。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路或帳號。

## `atoms.html#zoned`（中性原子場景 11：分區架構與並行閘）

- 按鈕：▶ 執行一層、中途量測、重置。一段動作還沒跑完時，再按會被忽略。
- 滑桿「並行對數」：2–8 對（預設 6）。
- 三塊底板：儲存區、糾纏區、讀取區；四種顏色代表四個邏輯位元 A、B、C、D。配對依序輪流：第 1、3 列 → 第 2、4 列 → 第 1、2 列 → 第 3、4 列。
- 右下插圖：一層的時間組成（代表值）。

## `atoms.html#imaging`（中性原子場景 12：螢光成像讀取）

- 按鈕：準備隨機態、① 推出 |1⟩、② 成像、重置。
- 滑桿「曝光時間 (ms)」：1–20（預設 10）。開關「非破壞讀取（另一種做法）」：切換時會重置。
- 相機影像：綠框＝判為有原子、紅框＝判為沒有；右下插圖是有原子／無原子的光子數分佈與閾值。

## 操作

`H` 隱藏面板；滑鼠拖曳旋轉、滾輪縮放。
''',
}

SHEET_HEADER = ['項目', '區域', '動作', '時間（μs）', '曝光（ms）', '閾值', '保真度（%）', '正確幾顆／25', '備註']
SHEET_ROWS = ([[f'第 {k} 層', '', '', '', '', '', '', '', ''] for k in range(1, N_LAYERS + 1)]
              + [['中途量測', '讀取區', '', '', '', '', '', '', '']]
              + [[f'成像 {e} ms', '', '', '', str(e), '', '', '', ''] for e in (1, 2, 5, 10)])

EXTRA_CSS = '''table.rec td{height:9mm}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.card{border:2pt solid #0b2540;border-radius:4mm;padding:5mm;margin-top:5mm}.card h3{margin-top:0}
table.grid td{width:12mm;height:12mm;text-align:center}'''


def html():
    rows = ''.join(f'<tr><td>第 {k} 層</td><td>{n}</td><td></td><td></td></tr>'
                   for k in range(1, N_LAYERS + 1) for n, _ in LAYER)
    grid = '<table class="grid">' + ''.join('<tr>' + '<td></td>' * 5 + '</tr>' for _ in range(5)) + '</table>'
    pages = [
        '<h2>分區排程表（今天的作品）</h2><p class="lead">在 atoms.html#zoned 按「▶ 執行一層」，看右下插圖，替三層線路排出每一步。</p>'
        '<table class="rec"><tr><th>層</th><th>動作</th><th>區域</th><th>時間（μs）</th></tr>' + rows + '</table>'
        '<p>三層合計：＿＿＿＿ μs　做閘一共：＿＿＿ μs，占 ≈ ＿＿＿%</p>'
        '<p>作品名稱：＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>',
        '<h2>判讀相機影像</h2><p class="lead">在 atoms.html#imaging：準備隨機態 → 先畫下哪幾格是紅色（|1⟩）→ ① 推出 → ② 成像。</p>'
        '<div style="display:flex;gap:10mm"><div><p>我畫的答案（紅色打 ×）</p>' + grid + '</div>'
        '<div><p>相機影像判讀（亮寫 0、暗寫 1）</p>' + grid + '</div></div>'
        '<table class="rec"><tr><th>曝光時間</th><th>閾值</th><th>判別保真度</th><th>正確幾顆／25</th></tr>'
        + ''.join(f'<tr><td>{e} ms</td><td></td><td></td><td></td></tr>' for e in (1, 2, 5, 10)) + '</table>',
        '<h2>換你改造：加入中途量測</h2><p class="lead">在第二層和第三層之間插入一次中途讀取（插圖代表值約 1 ms＝1000 μs）。</p>'
        '<table class="rec"><tr><th>順序</th><th>做什麼</th><th>區域</th><th>時間（μs）</th></tr>'
        + ''.join(f'<tr><td>{i}</td><td></td><td></td><td></td></tr>' for i in range(1, 6)) + '<tr><td>合計</td><td></td><td></td><td></td></tr></table>'
        '<p>讀取占：1000 ÷ ＿＿＿ ≈ ＿＿＿%</p><p>做閘占：＿＿＿ ÷ ＿＿＿ ≈ ＿＿＿%</p>'
        '<p>量完的原子怎麼辦？＿＿＿＿＿＿＿＿＿＿＿＿</p>'
        '<p class="note">生活技能：依功能分區提高效率——廚房、書桌、工具箱也分區嗎？你想到的例子：＿＿＿＿＿＿＿＿</p>',
        '<h2>說明卡與最後一關</h2><div class="box"><p>1. 儲存區、糾纏區、讀取區各做什麼？</p><div class="line"></div>'
        '<p>2. 一層線路的四步是什麼？哪一步最花時間？</p><div class="line"></div><p>3. 讀取三步：推出、成像、判別，亮代表什麼？</p><div class="line"></div>'
        '<p>4. 一個限制或注意事項：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出三個區的用途</li><li>說出一層線路大部分時間花在搬運</li>'
        '<li>說出讀取三步，亮是 |0⟩、暗是 |1⟩</li><li>指出一個限制：推出 |1⟩ 會失去原子，要重新裝載</li>'
        '<li>替分區排程表取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q075 分區架構與成像讀取 列印包', '父子科技學院 量子電腦學程 Q075｜分區架構與成像讀取', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q075-zoned-imaging', folder='Q075_分區架構與成像讀取', files=FILES,
        sheet=('03_排程與判讀紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_分區架構與成像讀取.pdf', pack_pages=4,
        pack_needles=('分區排程表', '判讀相機影像', '加入中途量測', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q075', episode_dir='specials/q075-zoned-imaging',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'scenes': ['animations/atoms.html#zoned', 'animations/atoms.html#imaging'],
               'layerTimesUs': dict(LAYER), 'midReadUs': MID_READ_US, 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q075/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')
