"""Q028 課堂教材：圖鑑卡模板、家族比較表、理想量子位元卡、說明卡（列印）、解答、動畫導覽。

不需要帳號，也不需要安裝任何程式；動畫用瀏覽器開啟 animations/index.html#potential、#washboard 與 animations/transmon-3d.html#capacitor。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q028/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 學程簡報 JJ_Microwave_Readout_Talk p18 家族表（典型範圍，實際依設計而異）＋維基百科補充；給爸爸念、給孩子填卡用。
FAMILY = [
    {'name': '電荷型', 'en': 'Charge qubit／Cooper pair box', 'structure': '小超導島＋1 個 JJ', 'ratio': '約 1', 'ratio_sort': 1,
     'freq': '5–10 GHz', 'alpha': '大', 'pro': '最早的超導量子位元（1999 年首次看到振盪）；非諧性大',
     'con': '對背景電荷極敏感（電荷色散大）；T2 約 1–2 μs'},
    {'name': '大電容型', 'en': 'Transmon', 'structure': 'JJ（或 SQUID）並聯大電容', 'ratio': '50–100', 'ratio_sort': 3,
     'freq': '4–6 GHz', 'alpha': '−200～−300 MHz', 'pro': '幾乎不怕背景電荷、結構簡單、業界主流；最佳 T1 約 0.1–1 ms',
     'con': '非諧性小，脈衝太快會漏到更高能階'},
    {'name': '超電感型', 'en': 'Fluxonium', 'structure': '1 個小 JJ 並聯超電感（上百個大 JJ 串成）', 'ratio': '約 1–10', 'ratio_sort': 2,
     'freq': '0.1–1 GHz', 'alpha': '極大', 'pro': '不怕背景電荷、非諧性極大；T1 可到毫秒；停在半個磁通量子對磁通雜訊一階不敏感',
     'con': '製作複雜、難大量擴充；頻率低，閘通常較慢'},
    {'name': '相位型', 'en': 'Phase qubit', 'structure': '電流偏壓的 1 個 JJ（傾斜洗衣板）', 'ratio': '遠大於 1', 'ratio_sort': 4,
     'freq': '5–10 GHz', 'alpha': '中', 'pro': '改偏壓電流就能調頻率；1985 年在這種接面量到能階（2025 年諾貝爾物理學獎）',
     'con': '電流一抖頻率就抖，狀態慢慢亂掉；現在較少使用'},
]
ORDER = [f['name'] for f in sorted(FAMILY, key=lambda f: f['ratio_sort'])]
assert ORDER == ['電荷型', '超電感型', '大電容型', '相位型']


def _table_md():
    rows = ['| 類型 | 結構 | E_J／E_C | 頻率 | 非諧性 | 優點 | 弱點 |', '|---|---|---|---|---|---|---|']
    rows += [f"| {f['name']}（{f['en']}） | {f['structure']} | {f['ratio']} | {f['freq']} | {f['alpha']} | {f['pro']} | {f['con']} |" for f in FAMILY]
    return '\n'.join(rows)


FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q028：量子位元家族圖鑑（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。這一堂比較四種超導量子位元：電荷型（Cooper pair box）、大電容型（transmon）、超電感型（fluxonium）、相位型（phase qubit）。
重點是：四種都靠約瑟夫森接面提供不耗損能量的非線性，差別在旁邊接了什麼、E_J／E_C 比值多少；每一種都有拿手的地方和怕的雜訊，沒有一種在所有指標都最好。下一堂 Q029 看晶片怎麼做：雙角度蒸鍍。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 共同點、看結構與比值、四種量子位元；看 3D 動畫 | 影片第 3–8 段、`05_動畫導覽.md` |
| 25–65 | 為四種量子位元各填一張圖鑑卡，每完成一張蓋一個解鎖章，照比值排序 | 列印包第 1、2 頁、`01_操作步驟.md` |
| 65–75 | 休息 | |
| 75–105 | 孩子改造：設計一張理想量子位元卡，寫出每個優點跟誰借、代價是什麼 | 列印包第 3 頁 |
| 105–115 | 孩子教爸爸：操作與原理 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、替圖鑑取名字、存檔 | |

## 課前準備（約 20 分鐘）

- 列印 `02_列印包_量子位元圖鑑.pdf`（A4，共 4 頁）；第 1 頁圖鑑卡模板可以多印一張，沿虛線剪成四張卡。
- 鉛筆、色筆、剪刀；一個印章或貼紙當「解鎖章」（沒有的話畫一顆星也可以）。
- 讀一遍 `04_解答.md`；有電腦的話，用瀏覽器先點一次 `index.html#potential`、`index.html#washboard`、`transmon-3d.html#capacitor`（見 `05_動畫導覽.md`）。

## 驗收重點

1. 完成「量子位元圖鑑卡」：四張卡都有結構、頻率、優點、弱點，右上角寫比值，並蓋上解鎖章。
2. 不看稿說出核心原理：四種都靠約瑟夫森接面的非線性；電荷型怕背景電荷、大電容型並聯大電容變得不怕但非諧性小、超電感型非諧性極大但難做、相位型可調但怕電流雜訊。
3. 指出至少一個注意事項：沒有一種量子位元在所有指標都最好；廠商選擇各有考量。

## 誠實說明

- 比值、頻率、非諧性是學程簡報 p18 的典型範圍，簡報註明「實際依設計而異」，不是某一顆晶片的量測。
- 年份、獎項與公司方向取自維基百科（Charge qubit、Transmon、Fluxonium、Phase qubit），未另查原始論文；影片不評論各公司的現況或優劣。
- 「電荷型、大電容型、超電感型、相位型」是本課為了好記取的小名；英文名字寫在卡片標題旁。
- 簡報表格還有一種「磁通量子位元」（超導環＋3–4 個 JJ），本課不做卡，可當課後延伸。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：四張圖鑑卡（約 40 分鐘）

1. 把列印包第 1 頁沿虛線剪成四張卡，第 2 頁的家族比較表放在中間。
2. 爸爸一次念比較表的一列（電荷型 → 大電容型 → 超電感型 → 相位型），孩子把重點用自己的話填進一張卡的四格：結構、頻率、優點、弱點。
3. 在「結構」格畫簡單的電路圖：
   - 電荷型：一個小方塊（小島）＋一個 ✕（接面）接到外面。
   - 大電容型：✕ 旁邊並聯一個很大的電容（兩條粗線）。
   - 超電感型：一個小 ✕ 並聯一大串 ✕✕✕✕（超電感）。
   - 相位型：一個 ✕ 接上電流源（畫一個圓圈加箭頭）。
4. 在每張卡右上角寫 E_J／E_C 比值；填完一張就蓋一個解鎖章。
5. 四張都蓋滿後，照比值從小排到大，拍照存檔。
6. 有電腦的話，一起看 `05_動畫導覽.md` 的三個場景，把看到的現象補進卡片的優點或弱點格。

## 下半場：孩子改造——理想量子位元卡（約 30 分鐘）

1. 用列印包第 3 頁。替你的理想量子位元取名字，畫出想像的結構。
2. 寫出三個優點，每一個都要寫「跟誰借」（例如向大電容型借結構簡單、向超電感型借很大的非諧性）。
3. 誠實寫下代價：借來的優點會不會互相打架？會不會更難做、或怕另一種雜訊？
4. 加分題：比較表裡有沒有哪兩個優點，在同一個設計裡很難同時拿到？（提示：大電容型的比值和非諧性）
''',

'04_解答.md': '# 解答（爸爸用）\n\n'
  '## 家族比較表（學程簡報 p18 典型範圍＋維基百科補充）\n\n' + _table_md() + '\n\n'
  '照比值從小排到大：' + ' → '.join(ORDER) + '（電荷型約 1、超電感型約 1–10、大電容型 50–100、相位型遠大於 1）。\n\n'
  '## 暫停題：想要不怕背景電荷，又要很大的非諧性，先看哪一張卡？\n\n'
  '- 超電感型（fluxonium）：維基百科寫它對 offset charge noise 不敏感、非諧性高；學程簡報 p18 寫非諧性「極大」。'
  '代價是那一大串接面讓製作複雜、難大量擴充，頻率低、閘通常較慢——這正是「沒有全能冠軍」。\n\n'
  '## 理想量子位元卡範例\n\n'
  '> 我的「穩穩號」：向大電容型借結構簡單和不怕背景電荷，向超電感型借很大的非諧性，向相位型借可以調頻率。'
  '代價：要可調就多一個雜訊入口（Q027 學過）；要非諧性大又不怕電荷，可能得用一大串接面，製作就變難。\n\n'
  '## 常見問題\n\n'
  '- 為什麼大家都說「沒有全能冠軍」？頻率、非諧性、相干時間、怕哪種雜訊、好不好製作常常互相拉扯；例如大電容型把電容加大換到不怕背景電荷，非諧性就跟著變小（Q025）。\n'
  '- 為什麼業界主流是大電容型？學程簡報 p18：抗電荷雜訊、結構簡單；講者備註提到幾家大公司都用它的變形。\n'
  '- 超電感型為什麼也有人做？維基百科：相干時間可到毫秒、非諧性高，有公司專門發展它。\n'
  '- 相位型為什麼少用了？學程簡報 p18「已較少使用」；維基百科：電流起伏會讓頻率跟著起伏、量子態失相。\n'
  '- 磁通量子位元呢？簡報表上第三列：超導環＋3–4 個 JJ，以環流方向編碼、對磁通雜訊敏感；可以當課後延伸自己補一張卡。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的 3D 動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要伺服器或帳號。網址後面的 `#…` 會直接跳到那個場景。

## `index.html#potential`（JJ 與微波讀取 3D 場景 4：能階與非諧性）——電荷型 vs 大電容型

- 打開時比值 E_J/E_C = 50（大電容型）。左邊面板下排三顆按鈕「CPB：E_J/E_C = 1」「10」「Transmon：50」。
- 右下角小圖「電荷色散：能階隨背景電荷 n_g 的變化」：藍、紅、綠三條線是最低三個能階。
  - 比值 50：三條都是平的直線 → 不怕背景電荷。
  - 比值 1（電荷型）：藍線和紅線上下起伏（紅線超出上緣的部分被截平）→ 背景電荷一變，能階就跟著動。

## `index.html#washboard`（JJ 與微波讀取 3D 場景 5：傾斜洗衣板）——相位型

- 金色小球是相位粒子；打開時偏壓電流 0.30，小球右邊的位障標著 1.15。
- 把「偏壓電流」滑桿慢慢加到 0.90：洗衣板越來越斜，位障降到 0.06；讀數第二行的 ω_p 從 0.98 降到 0.66 倍。相位型就是在這種很淺的山谷裡用最低兩個能階。
- 一次拉太快，小球可能滑出山谷（讀數變電壓態），這時按「重設」或把電流調小。

## `transmon-3d.html#capacitor`（Transmon 3D 第 1 章：大十字電容的作用）——大電容型的取捨

- 中間的十字金屬板就是並聯的大電容；「C_Σ」滑桿 5–200 fF（E_J/h 固定 15 GHz）。
  - 77.5 fF（預設）：比值 60.0、非諧性 −283 MHz、電荷色散 1.9 kHz、判斷「transmon 區間」。
  - 20 fF：比值 15.5、非諧性 −1.33 GHz、電荷色散 53.1 MHz、判斷「電荷雜訊主導（接近 Cooper pair box）」。
- 「回到 77.5 fF」按鈕回到預設值。電容拉小，非諧性變大，但電荷色散也變大——同一種設計裡也要取捨。

## 之後的課

Q029「晶片怎麼做：雙角度蒸鍍」會用 `index.html#fab` 看兩次斜角蒸鍍怎麼讓兩層鋁重疊出約瑟夫森接面。
''',
}

SHEET_HEADER = ['類型', '英文名字', '結構', 'E_J／E_C', '頻率', '非諧性', '優點', '弱點', '解鎖章']
SHEET_ROWS = [[f['name'], f['en']] for f in FAMILY]

EXTRA_CSS = '''.cards{display:grid;grid-template-columns:1fr 1fr;gap:5mm}
.card{border:1.6pt dashed #0b2540;border-radius:4mm;padding:3mm 4mm;height:116mm;position:relative}
.card h3{font-size:14pt;margin:0 0 1.5mm}.card .ratio{position:absolute;right:4mm;top:3mm;font-size:10pt;color:#4a6a88}
.cell{border:.8pt solid #7f9bb3;border-radius:2mm;padding:1mm 2mm;margin-top:1.8mm;font-size:10.5pt;color:#4a6a88}
.cell.big{height:30mm}.cell.mid{height:15mm}
.stamp{position:absolute;right:4mm;bottom:3mm;width:17mm;height:17mm;border:1.2pt dashed #c58a1a;border-radius:50%;font-size:8.5pt;color:#c58a1a;
display:flex;align-items:center;justify-content:center;text-align:center;line-height:1.2}
table.fam td,table.fam th{font-size:9.6pt;padding:1.2mm 1.8mm}table.fam{table-layout:fixed}table.fam th{white-space:nowrap}table.fam td:first-child{font-weight:700}
table.rank td{height:11mm}
.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.ideal .cell.big{height:75mm}'''


def _card(title):
    return (f'<div class="card"><h3>{title}</h3><span class="ratio">E_J／E_C：＿＿＿＿</span>'
            '<div class="cell big">結構（畫電路圖）</div><div class="cell mid">頻率</div>'
            '<div class="cell mid">優點</div><div class="cell mid">弱點</div><div class="stamp">解鎖章</div></div>')


def html():
    fam = ('<table class="fam"><tr><th style="width:15%">類型</th><th style="width:15%">結構</th><th style="width:9%">比值<br>E_J／E_C</th><th style="width:9%">頻率</th><th style="width:10%">非諧性</th><th>優點</th><th style="width:18%">弱點</th></tr>'
           + ''.join(f"<tr><td>{f['name']}<br><small style='margin:0'>{f['en']}</small></td><td>{f['structure']}</td><td>{f['ratio']}</td>"
                     f"<td>{f['freq']}</td><td>{f['alpha']}</td><td>{f['pro']}</td><td>{f['con']}</td></tr>" for f in FAMILY) + '</table>')
    pages = [
        '<h2>圖鑑卡模板</h2><p class="lead">沿虛線剪成四張卡。每張填四格、右上角寫比值；填完一張，蓋一個解鎖章。</p>'
        '<div class="cards">' + ''.join(_card(t) for t in ['電荷型', '大電容型', '超電感型', '相位型']) + '</div>',
        '<h2>家族比較表</h2><p class="lead">爸爸一次念一列，孩子用自己的話填進圖鑑卡。數值是學程簡報 p18 的典型範圍，實際依設計而異。</p>'
        + fam +
        '<h3 style="margin-top:5mm">整理比較表：照比值從小排到大</h3><table class="rank"><tr><th style="width:18%">名次</th><th>類型</th><th>E_J／E_C</th><th>它最怕什麼？</th></tr>'
        + ''.join(f'<tr><td>{i}</td><td></td><td></td><td></td></tr>' for i in range(1, 5)) + '</table>'
        '<div class="box" style="margin-top:4mm"><p>想要「不怕背景電荷，又要很大的非諧性」，該先看哪一張卡？為什麼？</p><div class="line"></div></div>',
        '<h2>理想量子位元卡</h2><p class="lead">設計一張你心中的理想量子位元：每個優點都要寫出跟誰借，最後誠實寫代價。</p>'
        '<div class="box ideal"><p>名字：＿＿＿＿＿＿＿＿＿＿　設計者：＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<div class="cell big">我想像的結構（畫電路圖）</div>'
        '<p style="margin:3mm 0 0">優點 1：＿＿＿＿＿＿＿＿＿＿＿＿＿＿　跟誰借：＿＿＿＿＿＿</p>'
        '<p style="margin:2mm 0 0">優點 2：＿＿＿＿＿＿＿＿＿＿＿＿＿＿　跟誰借：＿＿＿＿＿＿</p>'
        '<p style="margin:2mm 0 0">優點 3：＿＿＿＿＿＿＿＿＿＿＿＿＿＿　跟誰借：＿＿＿＿＿＿</p>'
        '<p style="margin:4mm 0 0">代價：借來的優點會不會互相打架？會不會更難做、或怕另一種雜訊？</p><div class="line"></div><div class="line"></div>'
        '<p style="margin:3mm 0 0">它最像哪一張圖鑑卡？為什麼？</p><div class="line"></div></div>',
        '<h2>說明卡：我的量子位元圖鑑</h2><div class="box"><p>圖鑑名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 量子位元家族圖鑑在解決什麼？</p><div class="line"></div><p>2. 我怎麼做（怎麼填卡、怎麼排）？</p><div class="line"></div>'
        '<p>3. 哪裡容易錯？</p><div class="line"></div><p>4. 生活中或真實的量子電腦哪裡會用到？</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出四種量子位元的共同點：都靠約瑟夫森接面的非線性</li><li>說出四種各自的結構</li>'
        '<li>說出每一種拿手的地方和怕的雜訊</li><li>說出理想量子位元卡的優點跟誰借、代價是什麼</li>'
        '<li>指出一個注意事項：沒有一種量子位元在所有指標都最好</li><li>替圖鑑取名字、拍照存檔</li></ul></div>',
    ]
    return printpack.document('Q028 量子位元圖鑑 列印包', '父子科技學院 量子電腦學程 Q028｜量子位元家族圖鑑', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q028-qubit-family-cards', folder='Q028_量子位元家族圖鑑', files=FILES,
        sheet=('03_圖鑑卡紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_量子位元圖鑑.pdf', pack_pages=4,
        pack_needles=('圖鑑卡模板', '家族比較表', '理想量子位元卡', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q028', episode_dir='specials/q028-qubit-family-cards',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'none（紙本；動畫用瀏覽器）',
               'family': {f['name']: {'en': f['en'], 'ratio': f['ratio'], 'freq': f['freq'], 'alpha': f['alpha']} for f in FAMILY},
               'rankByRatio': ORDER, 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q028/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')
