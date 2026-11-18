"""Q078 課堂教材：半導體自旋量子位元 — 紙上量子點模型、偵探辦案、自旋與超導比較表、平台卡、說明卡與解答。

學程還沒有量子點場景（課綱標為需新增），本課實作用紙、筆和硬幣；比較時參考學程的 animations/atoms.html#compare 與 index.html#chip。
免安裝、不需帳號。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q078/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 偵探辦案範例題（遊戲用的虛構數字，不是真實元件的量測）：放進第一顆電子需要的閘電壓（mV）
CASE = [('A', 512), ('B', 498), ('C', 621), ('D', 505)]
SUSPECT = max(CASE, key=lambda kv: abs(kv[1] - sorted(v for _, v in CASE)[len(CASE) // 2]))[0]
assert SUSPECT == 'C'

# 比較表的參考值（來源見 fact-check.md）
COMPARE = [
    ('量子位元是什麼', '量子點裡一顆電子的自旋', '超導電路（人造原子）'),
    ('尺寸', '量子點約 20–100 nm', '讀取諧振腔約 4 mm（學程動畫 #chip）'),
    ('工作溫度', '多在低溫冷凍機；部分矽元件可在幾 K', '10 mK 稀釋冷凍機（學程動畫 #compare）'),
    ('製程', '可在業界標準矽晶圓廠製作', '微影＋鋁蒸鍍做約瑟夫森接面'),
    ('挑戰', '每顆量子點都不一樣，要逐顆校準', '要極低溫與大量佈線、相干時間短'),
]
SIZE_RATIO = (4e-3 / 100e-9, 4e-3 / 20e-9)  # 4 萬～20 萬倍
assert round(SIZE_RATIO[0]) == 40000 and round(SIZE_RATIO[1]) == 200000

FILES = {
'00_爸爸先讀.md': f'''# 父子科技學院 量子電腦學程 Q078：半導體自旋量子位元（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶出三件事：量子點怎麼關住一顆電子、電子的自旋怎麼當零和一、為什麼這個平台能借用半導體製程。

學程還沒有量子點的互動場景，所以今天的實作用紙、筆和硬幣；比較超導時，可以開學程 `animations/atoms.html#compare`（三平台比較）和 `animations/index.html#chip`（超導晶片）。不需要網路、帳號或安裝。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 量子點、自旋、交換閘、晶圓廠 | 影片第 3–7 段 |
| 25–65 | 紙上量子點模型放電子、偵探辦案 | `01_操作步驟.md`、列印包第 1–2 頁 |
| 65–75 | 休息 | |
| 75–105 | 自旋與超導比較表、平台卡 | 列印包第 3 頁、`03_偵探與比較紀錄.csv` |
| 105–115 | 孩子教爸爸：量子點和自旋怎麼運作 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 準備 8–10 枚硬幣（正面＝自旋朝上＝0、反面＝朝下＝1）、一張白紙畫四個量子點和一排電極。
- 先想好偵探題：替四個量子點寫下「放進第一顆電子要多少電壓」，其中一顆和其他差很多。範例：{', '.join(f'{k} {v} mV' for k, v in CASE)}（嫌犯是 {SUSPECT}）。這些是遊戲用的虛構數字。
- 列印 `02_列印包_半導體自旋量子位元.pdf`（A4，共 4 頁）。讀一遍 `04_解答.md`。

## 誠實說明

- 本課的平台事實取自維基百科（Spin qubit quantum computer、Quantum dot、Electron paramagnetic resonance）與學程動畫原始碼；學程沒有自旋平台的簡報。
- 偵探題的電壓是虛構的，只用來體會「每顆量子點都不一樣」。
- 尺寸比較用的是超導讀取諧振腔（約 4 mm），不是 transmon 本體。
''',

'01_操作步驟.md': '''# 操作步驟

## A. 紙上量子點模型（約 15 分鐘）

1. 在紙上畫一排電極（長條方塊），中間圍出四個圓圈當量子點，相鄰兩個量子點之間畫一扇「門」（中間的閘電極）。
2. 爸爸說「電壓往上調」，孩子就往一個量子點放一枚硬幣；說「再調」，再放一枚。目標：每個量子點只留一顆電子。
3. 硬幣正面＝自旋朝上＝0、反面＝朝下＝1。爸爸說「打微波」，孩子把指定的硬幣翻面——這就是單位元閘。
4. 爸爸說「打開中間的門」，孩子把相鄰兩枚硬幣交換位置——這就是交換；只打一半時間是交換閘的平方根（紙上模型無法真的做出疊加，只用說的）。

## B. 偵探辦案（約 15 分鐘）

1. 爸爸把四個量子點的「放進第一顆電子要多少電壓」寫在卡片背面，一張一張翻開當線索。
2. 孩子記在列印包第 2 頁，找出和其他差最多的那顆（嫌犯），說出推理。
3. 討論：如果晶片上有一百萬顆量子點，每顆都要這樣調，會怎樣？

## C. 看比較的對手（約 10 分鐘，可選）

1. 開 `atoms.html#compare`：最左邊藍色是超導，旁邊標著「10 mK 稀釋冷凍機」。
2. 按「閘速度」「相干時間」，看超導和其他平台的差異。
3. 開 `index.html#chip`，看超導晶片上彎曲的讀取諧振腔（約 4 mm）。

## D. 下半場：自旋與超導比較表（約 30 分鐘）

用列印包第 3 頁，比尺寸、比工作溫度、寫挑戰，最後把重點抄到平台卡。
''',

'04_解答.md': '# 解答（爸爸用）\n\n## 偵探辦案範例（虛構數字）\n\n| 量子點 | 電壓（mV） |\n|---|---|\n'
  + ''.join(f'| {k} | {v} |\n' for k, v in CASE)
  + f'\n嫌犯：{SUSPECT}。其他三顆都在 500 mV 左右，{SUSPECT} 差了一百多 mV。重點：每顆量子點都不一樣，量子點越多，校準越花工夫。\n\n'
  '## 自旋與超導比較表（參考）\n\n| 項目 | 半導體自旋 | 超導 |\n|---|---|---|\n'
  + ''.join(f'| {a} | {b} | {c} |\n' for a, b, c in COMPARE)
  + f'\n尺寸差：4 mm ÷ 100 nm ≈ {round(SIZE_RATIO[0]):,} 倍；4 mm ÷ 20 nm ≈ {round(SIZE_RATIO[1]):,} 倍（諧振腔對量子點）。\n\n'
  '## 常見問題\n\n'
  '- 量子點為什麼叫人造原子？電子在裡面只能待在幾個固定的能階，像原子一樣。\n'
  '- 自旋怎麼當零和一？在磁場裡朝上和朝下的能量不同；打入能量剛好相符的微波就能翻轉。\n'
  '- 兩顆電子怎麼做閘？兩點之間的閘電極打電壓脈衝，自旋會交換；半個脈衝是交換閘的平方根，再配單位元閘組成受控反閘。\n'
  '- 為什麼和 CMOS 有關？矽自旋量子位元可以在業界標準的矽晶圓廠製作；英特爾等公司投入。\n'
  '- 熱量子位元？部分矽元件可在幾 K 工作，比 10 mK 暖一百倍以上，但仍然非常冷。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路或帳號。學程目前沒有量子點場景。

## `atoms.html#compare`（原子場景 13：三平台比較）

- 按鈕：連接性、閘速度、相干時間、規模、↻ 重播。
- 最左邊藍色是超導（旁邊是 10 mK 稀釋冷凍機），中間金色是離子阱，右邊青色是中性原子。
- 右下插圖：兩位元閘、讀取、T₂ 的時間尺度（代表值）。

## `index.html#chip`（場景 8：電路 QED 晶片）

- 超導量子位元做在矽基板上；每個量子位元配一條彎曲的讀取諧振腔，約 4 mm。

## 操作

`H` 隱藏面板；滑鼠拖曳旋轉、滾輪縮放。
''',
}

SHEET_HEADER = ['項目', '量子點', '電壓（mV）', '和中位數差多少', '是嫌犯嗎', '半導體自旋', '超導', '備註']
SHEET_ROWS = ([['偵探線索', k, '', '', '', '', '', ''] for k, _ in CASE]
              + [['比較表', '', '', '', '', '', '', a] for a, *_ in COMPARE])

EXTRA_CSS = '''table.rec td{height:9mm}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.card{border:2pt solid #0b2540;border-radius:4mm;padding:5mm;margin-top:5mm}.card h3{margin-top:0}'''


def html():
    pages = [
        '<h2>紙上量子點：一顆一顆放電子</h2><p class="lead">畫一排電極、四個量子點。硬幣當電子：正面＝朝上＝0，反面＝朝下＝1。</p>'
        '<table class="rec"><tr><th>動作</th><th>爸爸說</th><th>你做了什麼</th><th>結果</th></tr>'
        + ''.join(f'<tr><td>{a}</td><td>{b}</td><td></td><td></td></tr>' for a, b in [
            ('放電子', '電壓往上調'), ('只留一顆', '再調一次'), ('單位元閘', '打微波'), ('交換', '打開中間的門'), ('交換閘的平方根', '只打一半時間')])
        + '</table>'
        '<div class="card"><h3>平台卡（今天的作品）：半導體自旋量子位元</h3><p>量子位元是：＿＿＿＿＿＿＿＿　零和一是：＿＿＿＿＿＿＿＿</p>'
        '<p>怎麼做閘：＿＿＿＿＿＿＿＿＿＿＿＿　工作溫度：＿＿＿＿＿＿</p><p>優點：</p><div class="line"></div><p>挑戰：</p><div class="line"></div>'
        '<p>作品名稱：＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p></div>',
        '<h2>偵探辦案：找出不聽話的量子點</h2><p class="lead">線索：每顆量子點放進第一顆電子要多少電壓。找出差最多的那顆。</p>'
        '<table class="rec"><tr><th>量子點</th><th>電壓（mV）</th><th>和其他差多少</th><th>可疑嗎</th></tr>'
        + ''.join(f'<tr><td>{k}</td><td></td><td></td><td></td></tr>' for k, _ in CASE) + '</table>'
        '<p>嫌犯是：＿＿＿　我的推理：</p><div class="line"></div><div class="line"></div>'
        '<p class="note">如果晶片上有一百萬顆量子點，每顆都要這樣調，會怎樣？＿＿＿＿＿＿＿＿＿＿</p>',
        '<h2>換你改造：自旋和超導比一比</h2><p class="lead">參考影片與 atoms.html#compare、index.html#chip。</p>'
        '<table class="rec"><tr><th>項目</th><th>半導體自旋</th><th>超導</th></tr>'
        + ''.join(f'<tr><td>{a}</td><td></td><td></td></tr>' for a, *_ in COMPARE) + '</table>'
        '<p>尺寸差幾倍：4 mm ÷ ＿＿＿ nm ≈ ＿＿＿＿＿ 倍</p><p>溫度差幾倍：＿＿ K ÷ 10 mK ≈ ＿＿＿ 倍</p>'
        '<p class="note">生活技能：連結既有產業能力——新點子借用現成的晶片工廠。你還想到哪個例子？＿＿＿＿＿＿＿＿</p>',
        '<h2>說明卡與最後一關</h2><div class="box"><p>1. 量子點怎麼關住一顆電子？</p><div class="line"></div>'
        '<p>2. 電子的自旋怎麼當成零和一？怎麼翻轉？</p><div class="line"></div><p>3. 為什麼這個平台能借用半導體製程？</p><div class="line"></div>'
        '<p>4. 一個限制或注意事項：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出：電極加電壓圍出量子點，只留一顆電子</li><li>說出：自旋朝上、朝下是零和一，微波翻轉</li>'
        '<li>說出：中間的閘電極讓兩顆電子交換</li><li>指出一個限制：每顆量子點都不一樣，要逐顆校準</li>'
        '<li>替平台卡取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q078 半導體自旋量子位元 列印包', '父子科技學院 量子電腦學程 Q078｜半導體自旋量子位元', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q078-semiconductor-spin-qubits', folder='Q078_半導體自旋量子位元', files=FILES,
        sheet=('03_偵探與比較紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_半導體自旋量子位元.pdf', pack_pages=4,
        pack_needles=('紙上量子點', '平台卡', '偵探辦案', '自旋和超導比一比', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q078', episode_dir='specials/q078-semiconductor-spin-qubits',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'scenes': ['animations/atoms.html#compare', 'animations/index.html#chip'],
               'detectiveCaseMv': dict(CASE), 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q078/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')
