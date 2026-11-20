"""Q093 課堂教材：產業地圖與發展路線 — 路線圖模板、公開里程碑卡、家庭投票紀錄、說明卡與解答。

免安裝、不需帳號：只用學程的 animations/（atoms.html#compare、operation.html#qec、peripherals.html#wiring），用瀏覽器開啟。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q093/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 三個階段（slides/QC_Operation_Talk.pptx 第 51 頁）
STAGES = [('NISQ（現在）', '數十～上千實體位元', '錯誤緩解＋淺層線路；物理模擬、演算法研究、基準測試'),
          ('早期容錯（研發中）', '數十～數百邏輯位元', '邏輯錯誤 10⁻⁶～10⁻⁹；中等規模化學、物理模擬'),
          ('大規模容錯（目標）', '數千邏輯位元以上（百萬實體位元等級）', 'Shor、大型分子、材料設計；需解決佈線、低溫電子、即時解碼')]

# 公開里程碑卡（只收學程簡報與動畫標示的代表值；剪下來貼到路線圖上）
MILESTONES = [
    ('超導', 'Google Willow（2024）105 顆量子位元', 'QC_Operation_Talk p15；13_compare.js'),
    ('超導', 'Willow 表面碼 d = 3→5→7，Λ ≈ 2.14；d = 7 用 101 個量子位元（Nature, 2025）', 'QC_Operation_Talk p50'),
    ('超導', 'IBM Condor 1121 顆量子位元', '13_compare.js'),
    ('離子阱', 'Quantinuum H2 56 位元 → Helios 98 位元（2025）', 'Ion_NeutralAtom_Talk p45'),
    ('中性原子', 'QuEra Aquila 類比 256 顆', 'Ion_NeutralAtom_Talk p45'),
    ('中性原子', 'Caltech 原子陣列 6100 顆', '13_compare.js'),
    ('離子阱＋中性原子', '已有雲端可用的機器；提出 2028–2030 年容錯運算路線圖（目標，不是成績）', 'Ion_NeutralAtom_Talk p45'),
]

# 低溫佈線熱負載（以 05_wiring.js 的 App.PD.wiring 重算；% = 熱負載 ÷ 該級冷卻功率；示意估算）
WIRING = [(20, [8, 5, 0, 11, 4]), (100, [38, 22, 2, 52, 21]), (200, [75, 45, 4, 103, 42])]
WIRING_STAGES = ['50 K', '4 K', 'Still', 'Cold plate', 'MXC']

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q093：產業地圖與發展路線（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶出三個問題：量子電腦現在走到哪裡？接下來要經過哪幾個階段？各家選了哪些平台路線？

只需要瀏覽器與紙筆：下載學程的 `animations/` 資料夾，開 `atoms.html#compare`、`operation.html#qec`、`peripherals.html#wiring`。不需要網路、帳號或安裝。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 三個階段、實體位元 vs 邏輯位元、三條平台路線 | 影片第 3–7 段、`05_動畫導覽.md` |
| 25–65 | 把里程碑卡貼到路線圖上（已發表＝實線、公司目標＝虛線） | `01_操作步驟.md`、列印包第 1–2 頁 |
| 65–75 | 休息 | |
| 75–105 | 家庭投票：哪一年會出現真正有用的量子電腦？寫理由 | 列印包第 3 頁、`03_投票與里程碑紀錄.csv` |
| 105–115 | 孩子教爸爸：三個階段、三條路線、目標和證據 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 15 分鐘）

- 列印 `02_列印包_產業地圖與發展路線.pdf`（A4，共 4 頁），把第 2 頁的里程碑卡剪開。
- 讀一遍 `04_解答.md`。路線圖模板每年更新：把今年新發表的實驗加進里程碑卡。

## 家庭投票怎麼玩

每個人寫下一個年份和一個理由，理由必須指向地圖上的一張里程碑卡（例如「已經做出低於門檻的邏輯位元」）。爸爸收好，明年更新路線圖時再拿出來對答案。沒有標準答案，理由比年份重要。

## 誠實說明

- 各平台的規模數字是學程簡報與動畫標示的 2024–2026 年代表值，各家差異很大。
- 公司路線圖是目標，不是保證；判斷進度要看已發表、能被重現的實驗——這是本課最重要的注意事項。
- 本課不替任何公司排名，也不對「哪一年」下結論。
''',

'01_操作步驟.md': '''# 操作步驟

## A. 三平台比規模（`atoms.html#compare`，約 10 分鐘）

1. 預設是「連接性」：看超導只連鄰居、離子全連接、原子被光鑷搬動。
2. 按「規模」：柱子用對數畫已展示的量子位元／原子數，讀三個標籤，抄到列印包第 1 頁。
3. 再按「閘速度」「相干時間」：規模最大的平台，不一定在每一項都領先。

## B. 一個邏輯位元的代價（`operation.html#qec`，約 10 分鐘）

1. 按「d = 3」「d = 5」「d = 7」，讀上方金色字的實體量子位元數（17、49、97）。
2. 把「實體錯誤率」滑桿拉到 2%，再拉到 20%，看右下小圖三條線的順序怎麼變。

## C. 位元一多，線就塞爆（`peripherals.html#wiring`，約 5 分鐘）

把「量子位元數（線束示意）」從 20 拉到 200，看右下熱負載哪一列先變紅。

## D. 畫路線圖（約 15 分鐘）

在列印包第 1 頁的時間軸上分三段；把里程碑卡貼上去：已發表的實驗用實線框，公司目標用虛線框。
''',

'04_解答.md': '# 解答（爸爸用）\n\n## 三個階段（簡報 QC_Operation_Talk 第 51 頁）\n\n| 階段 | 規模 | 能做什麼 |\n|---|---|---|\n'
  + ''.join(f'| {a} | {b} | {c} |\n' for a, b, c in STAGES)
  + '\n## 里程碑卡的出處\n\n| 平台 | 里程碑 | 出處 |\n|---|---|---|\n'
  + ''.join(f'| {a} | {b} | {c} |\n' for a, b, c in MILESTONES)
  + '\n## 低溫佈線熱負載（動畫示意估算，熱負載 ÷ 冷卻功率）\n\n| 量子位元數 | ' + ' | '.join(WIRING_STAGES) + ' |\n|---|---|---|---|---|---|\n'
  + ''.join(f'| {n} | ' + ' | '.join(f'{v}%' for v in vs) + ' |\n' for n, vs in WIRING)
  + '\n200 顆時 Cold plate 一級超過 100%（紅色），這只是示意模型，但說明了大規模容錯為什麼需要低溫控制電子、高密度佈線與模組化互連。\n\n'
  '## 常見問題\n\n'
  '- 位元數最多就最強嗎？不一定。還要看錯誤率、連接性、閘速度，以及能不能做出低於門檻的邏輯位元。\n'
  '- 一個邏輯位元要多少實體位元？表面碼 d = 7 是 97 個（動畫），Willow 實驗則用了 101 個（簡報數字）；要到 10⁻⁶ 約需 d ≈ 27、約 1,500 個（簡報估算）。\n'
  '- 路線圖寫 2028–2030 年容錯，可以當真嗎？那是目標；要看之後有沒有已發表、能被重現的實驗。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路或帳號。

## `atoms.html#compare`（離子阱與中性原子場景 13：三平台比較）

- 單選：連接性、閘速度、相干時間、規模；按鈕「↻ 重播」。
- 藍色超導、金色離子阱、青色中性原子；右下小圖把閘、讀取、T₂ 畫在同一把對數尺上。

## `operation.html#qec`（操作場景 11：表面碼）

- 單選 d = 3／5／7；滑桿「實體錯誤率」；開關「自動循環」；按鈕「下一步」「跑 2000 輪（只統計）」。
- 右下小圖：藍、黃、紅三條線是碼距 3、5、7；白色直線是目前的實體錯誤率；灰虛線是不編碼。

## `peripherals.html#wiring`（周邊系統場景 5：低溫佈線）

- 滑桿「量子位元數（線束示意）」1–200；單選可聚焦單一線路。
- 右下小圖：各級熱負載 ÷ 冷卻功率，綠 < 50%、橘 50–100%、紅 > 100%。

## 操作

`H` 隱藏面板；滑鼠拖曳旋轉、滾輪縮放。
''',
}

SHEET_HEADER = ['項目', '平台', '里程碑或年份', '已發表／目標', '出處或理由', '備註']
SHEET_ROWS = ([[f'里程碑 {i}', a, b, '目標' if '路線圖' in b else '已發表／已展示', c, ''] for i, (a, b, c) in enumerate(MILESTONES, 1)]
              + [[f'投票 {i}', '', '', '', '', ''] for i in range(1, 6)])

EXTRA_CSS = '''table.rec td{height:9mm}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.card{border:2pt solid #0b2540;border-radius:4mm;padding:5mm;margin-top:5mm}.card h3{margin-top:0}
.cut{border:1.5pt dashed #0b2540;border-radius:2mm;padding:2.5mm;margin:2mm 0;font-size:11pt}'''


def html():
    pages = [
        '<h2>發展路線圖（今天的作品）</h2><p class="lead">三段時間軸：把第 2 頁的里程碑卡貼上去。已發表＝實線框，公司目標＝虛線框。</p>'
        '<table class="rec"><tr><th>平台</th><th>NISQ（現在）</th><th>早期容錯（研發中）</th><th>大規模容錯（目標）</th></tr>'
        + ''.join(f'<tr><td>{p}</td><td></td><td></td><td></td></tr>' for p in ('超導', '離子阱', '中性原子', '其他')) + '</table>'
        '<p>atoms.html#compare 按「規模」：超導＿＿＿＿　離子阱＿＿＿＿　中性原子＿＿＿＿</p>'
        '<div class="card"><h3>作品資訊</h3><p>作品名稱：＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿（明年這天再更新）</p></div>',
        '<h2>公開里程碑卡（剪下來貼）</h2><p class="lead">只收學程簡報與動畫標示的代表值。最後一張是目標，請用虛線框。</p>'
        + ''.join(f'<div class="cut"><b>{a}</b>　{b}<br><small>出處：{c}</small></div>' for a, b, c in MILESTONES)
        + '<div class="cut"><b>空白卡</b>　今年新發表的實驗：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</div>',
        '<h2>家庭投票：哪一年會有用</h2><p class="lead">先寫理由，再投票。理由要指向地圖上的一張里程碑卡。</p>'
        '<table class="rec"><tr><th>投票的人</th><th>年份</th><th>理由（指向哪張卡）</th><th>明年對答案</th></tr>'
        + ''.join('<tr><td></td><td></td><td></td><td></td></tr>' for _ in range(5)) + '</table>'
        '<p class="note">生活技能：對未來做有根據的預測——就像天氣預報，預測要有根據，也要隨新資料修正。</p>',
        '<h2>說明卡與最後一關</h2><div class="box"><p>1. 發展分成哪三個階段？各有多少位元？</p><div class="line"></div>'
        '<p>2. 三條平台路線各自的強項？</p><div class="line"></div><p>3. 為什麼一個邏輯位元要很多實體位元？</p><div class="line"></div>'
        '<p>4. 一個限制或注意事項：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出三個階段：現在、早期容錯、大規模容錯</li><li>說出三條路線：超導速度、離子品質、原子規模</li>'
        '<li>說出為什麼不能只看位元數</li><li>指出一個限制：公司路線圖是目標，不是保證</li>'
        '<li>替發展路線圖取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q093 產業地圖與發展路線 列印包', '父子科技學院 量子電腦學程 Q093｜產業地圖與發展路線', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q093-industry-roadmap', folder='Q093_產業地圖與發展路線', files=FILES,
        sheet=('03_投票與里程碑紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_產業地圖與發展路線.pdf', pack_pages=4,
        pack_needles=('發展路線圖', '里程碑卡', '家庭投票', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q093', episode_dir='specials/q093-industry-roadmap',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'scenes': ['animations/atoms.html#compare', 'animations/operation.html#qec', 'animations/peripherals.html#wiring'],
               'stages': [s[0] for s in STAGES], 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q093/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')
