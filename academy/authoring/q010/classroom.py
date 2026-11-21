"""Q010 課堂教材：可執行的貝爾態模擬器程式、瀏覽器動畫替代路線、成就卡、直方圖格、四種貝爾態改造表、說明卡與解答。

不需要帳號；模擬器路線需要在自己的電腦安裝開源套件（pip install qiskit qiskit-aer），瀏覽器路線免安裝。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q010/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 製作代理實跑紀錄：Python 3.13、qiskit 2.6.2、qiskit-aer 0.18.4、shots=1024、seed_simulator=2026
RUN = {'00': 516, '11': 508}
VARIANTS = [  # (名稱, 線路最前面加的閘, 理論結果, 實跑 seed=2026)
    ('Φ⁺（今天做的）', '不加', '00、11 各一半', {'00': 516, '11': 508}),
    ('Φ⁻', 'qc.x(0)', '00、11 各一半（差在負號）', {'00': 524, '11': 500}),
    ('Ψ⁺', 'qc.x(1)', '01、10 各一半', {'01': 508, '10': 516}),
    ('Ψ⁻', 'qc.x([0, 1])', '01、10 各一半（差在負號）', {'01': 524, '10': 500}),
]
assert sum(RUN.values()) == 1024 and all(sum(v.values()) == 1024 for *_, v in VARIANTS)

PROGRAM = '''"""父子科技學院 量子電腦學程 Q010：第一個量子程式——貝爾態（本機模擬器，不需要帳號）

安裝（只要一次）：  pip install qiskit qiskit-aer
執行：              python bell_simulator.py
"""
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# 第一段：建立線路——兩顆量子位元、兩格紀錄
qc = QuantumCircuit(2, 2)

# 改造區：想做另外三種貝爾態，把下面其中一行前面的 # 拿掉
# qc.x(0)        # Φ⁻：直方圖和原本一樣，差在負號
# qc.x(1)        # Ψ⁺：變成 01 和 10
# qc.x([0, 1])   # Ψ⁻：01 和 10，差在負號

# 第二段：照著樂譜加動作
qc.h(0)                         # 哈達瑪閘：第一顆（q0）進入疊加
qc.cx(0, 1)                     # 受控反閘：q0 是 1 時，翻轉 q1
qc.measure([0, 1], [0, 1])      # 把兩顆的結果寫進紀錄
print(qc.draw())

# 第三段：交給模擬器，重複 1024 次，數出每種結果
sim = AerSimulator()
counts = sim.run(transpile(qc, sim), shots=1024).result().get_counts()
print(counts)   # 位元字串的最右邊是 q0（第一顆）

# 想每次都得到同一組數字（例如和影片比對），可以改成：
# counts = sim.run(transpile(qc, sim), shots=1024, seed_simulator=2026).result().get_counts()
# 影片中的結果就是這樣跑出來的：{'00': 516, '11': 508}
'''

FILES = {
'00_爸爸先讀.md': f'''# 父子科技學院 量子電腦學程 Q010：第一個量子程式——貝爾態（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶出今天的任務：把一份兩顆量子位元的線路寫成程式，交給模擬器跑，讀懂直方圖。

## 兩條路線，選一條就好

| 路線 | 需要 | 適合 |
|---|---|---|
| A 本機模擬器 | 一台可裝 Python 的電腦；`pip install qiskit qiskit-aer`；不需要帳號 | 想真的打程式 |
| B 瀏覽器動畫 | 只要瀏覽器，打開 `animations/basic-circuits.html#bell`；免安裝、不需帳號 | 還沒準備好寫程式的電腦 |

課綱寫的「免安裝線路編輯器」學程尚未新增；路線 B 用現有的互動動畫替代（可逐步播放、量測 1,000 次、切換四種貝爾態），但不能拖拉自己的閘。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 模擬器是什麼、貝爾態線路四格、寫下預測 | 影片第 3–5 段、列印包第 1 頁 |
| 25–65 | 打程式（或開動畫）、跑 1024 次（動畫是 1,000 次）、截圖、畫直方圖並解釋 | `bell_simulator.py`、`01_操作步驟.md`、列印包第 2 頁 |
| 65–75 | 休息 | |
| 75–105 | 改出另一種貝爾態，記錄直方圖差異 | 列印包第 3 頁、`03_直方圖紀錄.csv` |
| 105–115 | 孩子教爸爸：怎麼操作、為什麼只有兩種結果 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（路線 A 約 15 分鐘，路線 B 約 2 分鐘）

- 路線 A：先自己跑一次 `bell_simulator.py`，確定會印出線路圖和像 `{{'00': 5xx, '11': 5xx}}` 的結果。
- 路線 B：下載學程的 `animations/` 資料夾，用瀏覽器開 `basic-circuits.html#bell`。
- 列印 `02_列印包_第一個量子程式.pdf`（A4，共 4 頁）；準備印章或貼紙當成就章。讀一遍 `04_解答.md`。

## 成就官的原則

- 先預測再執行：孩子沒寫預測就按執行，這一關先不蓋章。
- 516 和 508 不一樣高是正常的：次數有限，數字本來就會上下跳；1024 次大約上下差 16 次。
- 程式出錯時，先一起讀錯誤訊息最後一行，找出是哪一行；看懂錯誤訊息是一枚隱藏成就。

## 誠實說明

- 模擬器算的是理想的量子規則，沒有雜訊；真的量子電腦會多出少量 01、10，多少依機器而定，本課不給數字。
- 影片中的 516／508 是用固定亂數種子（seed_simulator=2026）跑的，你們跑出來的數字多半不同。
- 程式介面依套件版本會調整；本程式在 qiskit 2.6.2、qiskit-aer 0.18.4 測試過。
''',

'01_操作步驟.md': '''# 操作步驟

## 路線 A：本機模擬器（約 40 分鐘）

1. 安裝（只要一次）：在終端機輸入 `pip install qiskit qiskit-aer`。
2. 先在列印包第 1 頁寫預測：會量到哪些結果？各大約幾次？
3. 打開 `bell_simulator.py`，和孩子一起找出三段：建線路、加動作、交給模擬器。
4. 執行 `python bell_simulator.py`。畫面先印出線路圖，再印出像 `{'00': 516, '11': 508}` 的次數表。
5. 截圖（線路圖＋次數表）。把兩個數字畫在列印包第 2 頁的直方圖格。
6. 再執行兩次，記下三次的數字，看看差多少。

## 路線 B：瀏覽器動畫（約 40 分鐘）

1. 打開 `animations/basic-circuits.html#bell`，上方選「Φ⁺」。
2. 按「下一步 ▶」兩次：先看 H 之後，再看 CNOT 之後，振幅柱子怎麼變。
3. 按「量測 1,000 次」，右邊出現灰色（理論）和綠色（實際次數）。截圖。
4. 按「清除」，再量一次 1,000 次，記下兩次的數字。
5. 頁面下方「Qiskit 程式碼」可以展開，看看同一個線路寫成程式長什麼樣。

## 下半場：另外三種貝爾態（約 30 分鐘）

1. 路線 A：把程式「改造區」其中一行前面的 `#` 拿掉；路線 B：上方改選 Φ⁻、Ψ⁺ 或 Ψ⁻。
2. 先在列印包第 3 頁寫預測，再跑。
3. 把新的直方圖和原本的並排，寫下差在哪裡。
''',

'bell_simulator.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n## 影片中的實跑（qiskit 2.6.2、qiskit-aer 0.18.4、shots=1024、seed_simulator=2026）\n\n'
  + '| 結果 | 次數 |\n|---|---|\n' + ''.join(f'| {k} | {v} |\n' for k, v in sorted(RUN.items()))
  + '| 01 | 0 |\n| 10 | 0 |\n\n不固定種子時另跑三次：518／506、494／530、510／514（00／11）。1024 次的一半是 512，大約上下差 16 次都常見。\n\n'
  + '## 四種貝爾態\n\n| 名稱 | 線路最前面加 | 理論結果 | 實跑（seed=2026） |\n|---|---|---|---|\n'
  + ''.join(f'| {n} | `{g}` | {t} | ' + '、'.join(f'{k}：{v}' for k, v in sorted(c.items())) + ' |\n' for n, g, t, c in VARIANTS)
  + '\n## 常見問題\n\n'
  '- 為什麼沒有 01、10？受控反閘讓第二顆跟著第一顆：第一顆是 0 時第二顆維持 0，第一顆是 1 時第二顆翻成 1。\n'
  '- 為什麼 Φ⁻ 和原本一樣？差別在正負號，只量零和一看不出來，要再經過干涉才分得出來。\n'
  '- 位元字串怎麼讀？最右邊是 q0（第一顆）。只做 `qc.x(0)` 再量測，會得到 `01`。\n'
  '- 真的量子電腦呢？閘和讀取會出錯，會多出少量 01、10；模擬器沒有雜訊。動畫 `operation.html#circuit` 的「加入雜訊」開關可以模擬看看（每閘 1%、讀取 3%，只是示意）。\n',

'05_線路動畫導覽.md': '''# 線路動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路、伺服器或帳號。

## `animations/basic-circuits.html#bell`（八個基礎量子電路：Bell 態）

- 上方「目標 Bell 態」：Φ⁺、Φ⁻、Ψ⁺、Ψ⁻ 四種。
- 「⏮ 起點」「◀ 上一步」「▶ 播放」「下一步 ▶」：一步一步看振幅柱子怎麼變。
- 右下「量測 1 次」「量測 1,000 次」「清除」：灰色是理論，綠色是實際次數。
- 最下面「Qiskit 程式碼」：展開後是同一個線路的程式，會隨上方選項改變。

## `animations/operation.html#circuit`（場景 6：量子線路）

- 範例選「Bell 態」，按「單步 ▶」三次，最後一步會跑 1000 次並畫直方圖。
- 「加入雜訊（每閘 1%、讀取 3%）」：打開後會冒出少量 01、10，示意真機的雜訊。

## 操作

`H` 隱藏面板；滑鼠拖曳旋轉、滾輪縮放（operation.html）；左右方向鍵換步（basic-circuits.html）。
''',
}

SHEET_HEADER = ['實驗', '路線（模擬器／動畫）', '改了什麼', '預測', '重複次數', '00', '01', '10', '11', '和預測一樣嗎']
SHEET_ROWS = ([['貝爾態 Φ⁺ 第 1 次', '', '不改', '', '1024'], ['貝爾態 Φ⁺ 第 2 次', '', '不改', '', '1024'],
               ['貝爾態 Φ⁺ 第 3 次', '', '不改', '', '1024']]
              + [[f'改造 {n}', '', g, '', '1024'] for n, g, *_ in VARIANTS[1:]])

BADGES = ['寫好預測', '跑出結果', '讀懂直方圖', '解釋為什麼沒有 01、10', '改出新的貝爾態']

EXTRA_CSS = '''.badges{display:grid;grid-template-columns:repeat(3,1fr);gap:5mm;margin-top:4mm}
.badge{border:1.4pt solid #0b2540;border-radius:50%;aspect-ratio:1;display:flex;flex-direction:column;align-items:center;justify-content:center;
text-align:center;font-size:12pt;padding:4mm}.badge b{font-size:10pt;color:#4a6a88}.badge.hidden{border-style:dashed}
.hgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:6mm;height:78mm;border-left:1.2pt solid #0b2540;border-bottom:1.2pt solid #0b2540;
margin:3mm 0 0 12mm;position:relative;background-image:linear-gradient(#cfdde8 .6pt,transparent .6pt);background-size:100% 7.8mm}
.ylab{position:absolute;left:-12mm;font-size:9pt;color:#4a6a88}.xlab{display:grid;grid-template-columns:repeat(4,1fr);gap:6mm;margin-left:12mm;
font-size:11pt;text-align:center}table.rec td{height:10mm}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
pre.code{font-size:9.5pt;background:#f2f6fa;border:1pt solid #cfdde8;padding:3mm;margin:2mm 0;white-space:pre-wrap}'''


def html():
    badge = ''.join(f'<div class="badge"><b>成就 {i}</b>{t}<br>□</div>' for i, t in enumerate(BADGES, 1))
    pages = [
        '<h2>成就卡：第一個量子程式</h2><p class="lead">每完成一關，成就官（爸爸）蓋一個章。</p>'
        f'<div class="badges">{badge}<div class="badge hidden"><b>隱藏成就</b>看懂一則錯誤訊息<br>□</div></div>'
        '<div class="box" style="margin-top:6mm"><h3>成就 1：先預測</h3><p>線路：兩顆都是 0 → 第一顆做 H → 受控反閘 → 一起量。跑 1024 次：</p>'
        '<p>00 大約＿＿次　01 大約＿＿次　10 大約＿＿次　11 大約＿＿次</p><p>我為什麼這樣猜：</p><div class="line"></div></div>',
        '<h2>成就 2、3：跑出結果，讀懂直方圖</h2><p class="lead">路線 A 跑 bell_simulator.py（1024 次）；路線 B 用 basic-circuits.html#bell（1,000 次）。</p>'
        '<table class="rec"><tr><th>第幾次</th><th>00</th><th>01</th><th>10</th><th>11</th></tr>'
        + ''.join(f'<tr><td>第 {i} 次</td><td></td><td></td><td></td><td></td></tr>' for i in (1, 2, 3)) + '</table>'
        '<h3 style="margin-top:4mm">直方圖（第 1 次；每格約 100 次）</h3>'
        '<div class="hgrid"><span class="ylab" style="top:-2mm">1000</span><span class="ylab" style="top:37mm">500</span>'
        '<span class="ylab" style="bottom:-2mm">0</span></div><div class="xlab"><span>00</span><span>01</span><span>10</span><span>11</span></div>'
        '<p class="note">位元字串的最右邊是第一顆（q0）。兩根柱子為什麼不一樣高？＿＿＿＿＿＿＿＿＿＿＿＿</p>',
        '<h2>成就 5：另外三種貝爾態</h2><p class="lead">在線路最前面加一個 X 閘（翻轉閘）。先預測，再跑，和原本並排比較。</p>'
        '<table class="rec"><tr><th>名稱</th><th>線路最前面加</th><th>我的預測</th><th>實際結果</th><th>和原本差在哪</th></tr>'
        + ''.join(f'<tr><td>{n}</td><td>{g}</td><td></td><td></td><td></td></tr>' for n, g, *_ in VARIANTS) + '</table>'
        '<pre class="code"># 程式的改造區：拿掉其中一行前面的 #\n# qc.x(0)\n# qc.x(1)\n# qc.x([0, 1])\nqc.h(0)\nqc.cx(0, 1)\nqc.measure([0, 1], [0, 1])</pre>'
        '<p class="note">有兩種量起來和原本一模一樣，你覺得差別藏在哪裡？＿＿＿＿＿＿＿＿＿＿＿＿</p>',
        '<h2>說明卡：我的貝爾態</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 線路有哪幾步？</p><div class="line"></div><p>2. 為什麼只有 00 和 11？</p><div class="line"></div><div class="line"></div>'
        '<p>3. 一個限制或容易錯的地方：</p><div class="line"></div><p>（截圖貼在背面）</p></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出線路的步驟：疊加、受控反閘、測量</li><li>解釋為什麼直方圖只有 00 和 11</li>'
        '<li>說出為什麼兩次的數字不一樣</li><li>指出一個限制：模擬器沒有雜訊，真機會多出少量 01、10</li>'
        '<li>替截圖和說明卡取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q010 第一個量子程式 列印包', '父子科技學院 量子電腦學程 Q010｜第一個量子程式：貝爾態', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q010-first-program', folder='Q010_第一個量子程式', files=FILES,
        sheet=('03_直方圖紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_第一個量子程式.pdf', pack_pages=4,
        pack_needles=('成就卡', '先預測', '跑出結果', '直方圖', '另外三種貝爾態', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q010', episode_dir='specials/q010-first-program',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'optional（路線 A：pip install qiskit qiskit-aer；路線 B 免安裝）',
               'program': 'bell_simulator.py', 'testedWith': 'qiskit 2.6.2, qiskit-aer 0.18.4',
               'recordedRun': RUN, 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q010/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')
