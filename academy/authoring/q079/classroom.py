"""Q079 課堂教材：拓樸量子位元與 NV 色心 — 繩子編辮子紀錄、工程答辯問題卡、進展與爭議整理表、平台卡、說明卡與解答。

免安裝、不需帳號：三條繩子（或鞋帶、毛線）；表面碼動畫 animations/operation.html#qec 用瀏覽器開啟（選用）。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q079/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 繩子編辮子：繩子由左到右編號 1、2、3；「A」= 左邊那條跨到中間那條上面，「B」= 中間那條跨到右邊那條上面
BRAIDS = [('A 再 B', '先左跨中，再中跨右'), ('B 再 A', '先中跨右，再左跨中'), ('A 再 A', '左跨中兩次'), ('A 再 A⁻¹', '左跨中，再從下面跨回來')]

# 實驗現況時間線（依 Wikipedia：Topological quantum computer、Majorana 1，2026-11-18 讀取）
TIMELINE = [('1997', 'Kitaev 提出拓樸量子計算構想', '理論'),
            ('2018', '有團隊宣稱看到孤立的馬約拉納粒子', '宣稱'),
            ('2021', '上述說法被撤回', '撤回'),
            ('2025', '微軟發表 Majorana 1；論文作者寫明量測本身不能確定是拓樸態', '爭議中')]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q079：拓樸量子位元與 NV 色心（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶出兩個問題：有沒有天生不怕雜訊的量子位元？鑽石裡的缺陷怎麼變成量子位元？

需要準備：三條繩子（鞋帶、毛線、跳繩都可以，最好三種顏色）、膠帶。選用：瀏覽器開學程的 `animations/operation.html#qec`。不需要網路、帳號或安裝。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 資訊放在哪裡、拓樸與編織、實驗現況、NV 色心 | 影片第 3–7 段 |
| 25–65 | 繩子編辮子（順序對調比一比）、練習工程答辯 | `01_操作步驟.md`、列印包第 1–2 頁 |
| 65–75 | 休息 | |
| 75–105 | 整理拓樸與 NV 色心的最新進展與爭議 | 列印包第 3 頁、`03_編辮子與消息整理紀錄.csv` |
| 105–115 | 孩子答辯給爸爸聽：拓樸原理、NV 讀取、一個限制 | 列印包第 4 頁 |
| 115–120 | 錄音總結、平台卡命名、存檔 | |

## 課前準備（約 10 分鐘）

- 把三條繩子的上端用膠帶黏在桌邊，自己先編一次「A 再 B」和「B 再 A」，確認兩條辮子看起來不一樣。
- 列印 `02_列印包_拓樸量子位元與NV色心.pdf`（A4，共 4 頁）。讀一遍 `04_解答.md`。

## 工程答辯怎麼玩

孩子選一個平台（拓樸量子位元或 NV 色心）當「工程師」替它辯護；爸爸當審查委員，對每一句宣稱追問三個問題：有沒有同行審查？別的團隊重做過嗎？是理論上可以，還是實驗上已經做到？答不出來的句子，就移到平台卡的「理論承諾」欄。

## 誠實說明

- 拓樸量子位元還在研究階段：拓樸量子計算需要的非阿貝爾任意子，至今還沒有在實驗上被確認。
- 繩子辮子是經典的類比；真正的任意子編織還和交換方向有關，量子力學細節不在本課範圍。
- 本課事實取自維基百科（Topological quantum computer、Majorana 1、Toric code、Nitrogen-vacancy center），學程目前沒有這兩個平台的簡報。
''',

'01_操作步驟.md': '''# 操作步驟

## A. 繩子編辮子（約 20 分鐘）

1. 三條繩子上端黏在桌邊，由左到右編號 1、2、3。
2. 定義兩個動作：「A」= 左邊位置的繩子跨到中間位置那條的上面（交換位置）；「B」= 中間位置的繩子跨到右邊位置那條的上面。
3. 爸爸編「A 再 B」，下端用膠帶固定；拉一拉、抖一抖、讓繩子彎來彎去，但不准讓繩子穿過彼此。辮子變了嗎？
4. 孩子用另外三條繩子編「B 再 A」，兩條並排比一比：下端的顏色順序一樣嗎？交叉長相一樣嗎？
5. 再試「A 再 A」和「A 再從下面跨回來」：後者拉直後會怎樣？把結果記在列印包第 1 頁。

## B. 工程答辯練習（約 15 分鐘）

用列印包第 2 頁的問題卡。孩子先替拓樸量子位元辯護一次，再替 NV 色心辯護一次；爸爸每次只問卡上的三個問題。

## C. 選用：表面碼動畫（`operation.html#qec`，約 5 分鐘）

關掉「自動循環」，按「d = 7」，把實體錯誤率拉到 8%，按「下一步」四次：紅球（錯誤）→ 橘柱（症狀）→ 綠線（解碼）→ 修正。只有貫穿上下邊界的鏈才會變成邏輯錯誤——這就是「只看整體連法」的拓樸想法。

## D. 下半場：整理進展與爭議（約 30 分鐘）

每個平台至少找一則最新消息，填進列印包第 3 頁：一欄寫理論承諾、一欄寫實驗現況、再勾有沒有同行審查。最後寫平台卡。
''',

'04_解答.md': '# 解答（爸爸用）\n\n## 繩子編辮子\n\n| 編法 | 說明 | 結果 |\n|---|---|---|\n'
  '| A 再 B | 先左跨中，再中跨右 | 下端顏色順序變成 2、3、1 |\n'
  '| B 再 A | 先中跨右，再左跨中 | 下端顏色順序變成 3、1、2，和上一條不同 |\n'
  '| A 再 A | 左跨中兩次 | 下端回到 1、2、3，但繩子纏了一圈，拉不直——和沒編過不一樣 |\n'
  '| A 再 A⁻¹ | 左跨中，再從下面跨回來 | 拉直後解開，和沒編過一樣 |\n\n'
  '重點：拉一拉、抖一抖（不讓繩子互相穿過）不會改變辮子；交叉的順序與上下方向才會改變。'
  '「A 再 A」說明了：只看兩端的位置還不夠，怎麼繞也算數——這就是拓樸。\n\n'
  '## 實驗現況時間線（維基百科）\n\n| 年 | 事件 | 性質 |\n|---|---|---|\n'
  + ''.join(f'| {y} | {e} | {k} |\n' for y, e, k in TIMELINE)
  + '\n## 常見問題\n\n'
  '- 拓樸量子位元已經做出來了嗎？還沒有被確認。拓樸量子計算需要的非阿貝爾任意子尚未在實驗上確認；2025 年 Majorana 1 的論文作者也寫明，量測本身不能確定那些狀態是拓樸的。\n'
  '- 為什麼可能天生抗雜訊？資訊存在好幾顆任意子共同的狀態裡，運算只取決於編織的拓樸，路徑上的小誤差改不了結果。\n'
  '- NV 色心是什麼？鑽石裡一個氮原子取代碳、旁邊有一個空位。綠光照射會發紅光，亮度和自旋有關，可用來讀取和初始化；室溫下自旋相干最多可達毫秒。\n'
  '- NV 色心最常用在哪？奈米尺度的磁場與電場量測（量子感測），也被拿來研究量子網路與量子計算。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程目前沒有拓樸量子位元、編織或 NV 色心的動畫（課綱標為「需新增」）。可以借用的相關場景：

## `operation.html#qec`（3D 場景 11：雜訊與量子錯誤更正：表面碼）

- 單選「d = 3／5／7」：碼距；按下會重新開始。
- 滑桿「實體錯誤率 p（每個資料量子位元）」：0.5%–20%。
- 開關「自動循環」；按鈕「下一步」、「跑 2000 輪（只統計）」。
- 白球是資料量子位元；青色方塊檢查 X 錯誤的奇偶；亮橘色 = 症狀；綠線 = 解碼器猜的錯誤鏈。
- 只有貫穿上下邊界的鏈才是邏輯錯誤。表面碼本身就是一種拓樸量子錯誤更正碼。

## 操作

`H` 隱藏面板；滑鼠拖曳旋轉、滾輪縮放。
''',
}

SHEET_HEADER = ['項目', '編法或平台', '結果／消息', '理論承諾', '實驗現況', '同行審查（有／無／不知道）', '來源', '備註']
SHEET_ROWS = ([['編辮子', b, '', '', '', '', '', ''] for b, _ in BRAIDS]
              + [['消息', p, '', '', '', '', '', ''] for p in ('拓樸量子位元', '拓樸量子位元', 'NV 色心', 'NV 色心')])

EXTRA_CSS = '''table.rec td{height:10mm}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.card{border:2pt solid #0b2540;border-radius:4mm;padding:5mm;margin-top:5mm}.card h3{margin-top:0}'''


def html():
    pages = [
        '<h2>實作：繩子編辮子</h2><p class="lead">繩子由左到右 1、2、3。A = 左跨過中；B = 中跨過右。編好後拉一拉、抖一抖，但不准讓繩子互相穿過。</p>'
        '<table class="rec"><tr><th>編法</th><th>怎麼做</th><th>下端顏色順序</th><th>抖一抖後變了嗎</th><th>和別條一樣嗎</th></tr>'
        + ''.join(f'<tr><td>{b}</td><td>{h}</td><td></td><td></td><td></td></tr>' for b, h in BRAIDS) + '</table>'
        '<p class="note">結論：辮子只和＿＿＿＿＿＿有關，和＿＿＿＿＿＿無關。</p>',
        '<h2>工程答辯問題卡</h2><p class="lead">你當工程師替平台辯護；爸爸當審查委員，對每一句宣稱問這三個問題。</p>'
        '<div class="box"><p>1. 有沒有經過同行審查？</p><p>2. 別的團隊重做過嗎？</p><p>3. 這是理論上可以做到，還是實驗上已經做到？</p></div>'
        '<table class="rec"><tr><th>平台</th><th>我的宣稱</th><th>問 1</th><th>問 2</th><th>問 3：理論／實驗</th></tr>'
        + ''.join(f'<tr><td>{p}</td><td></td><td></td><td></td><td></td></tr>' for p in ('拓樸量子位元', '拓樸量子位元', 'NV 色心', 'NV 色心')) + '</table>'
        '<p class="note">答不出來的宣稱，移到平台卡的「理論承諾」欄。</p>',
        '<h2>換你改造：整理進展與爭議</h2><p class="lead">每個平台至少找一則最新消息，拆成兩欄。</p>'
        '<table class="rec"><tr><th>平台</th><th>消息（日期、來源）</th><th>理論承諾</th><th>實驗現況</th><th>同行審查？</th></tr>'
        + ''.join(f'<tr><td>{p}</td><td></td><td></td><td></td><td></td></tr>' for p in ('拓樸', '拓樸', 'NV 色心', 'NV 色心')) + '</table>'
        '<p class="note">生活技能：分辨「理論承諾」與「實驗現況」。廣告或新聞裡你看過類似的例子嗎？＿＿＿＿＿＿＿＿</p>',
        '<div class="card"><h3>平台卡（今天的作品）</h3><table class="rec"><tr><th></th><th>拓樸量子位元</th><th>NV 色心</th></tr>'
        '<tr><td>核心原理</td><td></td><td></td></tr><tr><td>一個優點</td><td></td><td></td></tr>'
        '<tr><td>一個限制</td><td></td><td></td></tr><tr><td>證據從哪裡來</td><td></td><td></td></tr></table>'
        '<p>作品名稱：＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：答辯給爸爸聽</h3><ul class="chk">'
        '<li>不看稿說出拓樸為什麼可能抗雜訊：資訊分散、靠編織</li><li>說出 NV 色心怎麼讀：綠光照、看紅光亮暗</li>'
        '<li>指出一個限制：需要的任意子還沒被確認</li><li>對一則消息問出三個答辯問題</li>'
        '<li>替平台卡取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q079 拓樸量子位元與 NV 色心 列印包', '父子科技學院 量子電腦學程 Q079｜拓樸量子位元與 NV 色心', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q079-topological-nv', folder='Q079_拓樸量子位元與NV色心', files=FILES,
        sheet=('03_編辮子與消息整理紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_拓樸量子位元與NV色心.pdf', pack_pages=4,
        pack_needles=('繩子編辮子', '工程答辯問題卡', '整理進展與爭議', '平台卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q079', episode_dir='specials/q079-topological-nv',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'materials': ['三條繩子', '膠帶'], 'scenes': ['animations/operation.html#qec'],
               'timeline': [list(t) for t in TIMELINE], 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q079/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')
