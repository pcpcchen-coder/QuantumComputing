"""Q004 課堂教材：三種閘的旋轉表、六關闖關紀錄表、自出兩關、解答（不需帳號、不需安裝）。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q004/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 四個位置：北極 |0⟩、南極 |1⟩、赤道前方 |+⟩、赤道後方 |−⟩；三種閘都是轉半圈
POS = ['北極', '南極', '赤道前方', '赤道後方']
TABLE = {
    'X': {'北極': '南極', '南極': '北極', '赤道前方': '赤道前方', '赤道後方': '赤道後方'},
    'H': {'北極': '赤道前方', '赤道前方': '北極', '南極': '赤道後方', '赤道後方': '南極'},
    'Z': {'北極': '北極', '南極': '南極', '赤道前方': '赤道後方', '赤道後方': '赤道前方'},
}
NAME = {'X': 'X 翻轉閘（繞前後軸）', 'H': 'H 哈達瑪閘（繞斜軸）', 'Z': 'Z 相位翻轉閘（繞直立軸）'}


def run(seq, start='北極'):
    p = start
    for g in seq:
        p = TABLE[g][p]
    return p


def reachable(gates, start='北極'):
    seen, todo = {start}, [start]
    while todo:
        p = todo.pop()
        for g in gates:
            q = TABLE[g][p]
            if q not in seen:
                seen.add(q); todo.append(q)
    return seen


# 每個閘轉兩次回原狀
assert all(run(g + g, p) == p for g in 'XHZ' for p in POS)
LEVELS = [
    ('第一關', '到南極', '全部可用', 'X', 1),
    ('第二關', '到赤道前方', '全部可用', 'H', 1),
    ('第三關', '到赤道後方', '全部可用', 'X → H（或 H → Z）', 2),
    ('第四關', '到南極', '不准用 X', 'H → Z → H', 3),
    ('第五關', '預測：依序按 X、H、Z、H，箭頭停在哪？', '照順序按', '回到北極', 4),
    ('陷阱關', '到赤道前方', '只准用 X 和 Z', '過不了：X、Z 只在兩極之間搬', None),
]
assert run('X') == '南極' and run('H') == '赤道前方' and run('XH') == run('HZ') == '赤道後方'
assert run('HZH') == '南極' and run('XHZH') == '北極'
assert '赤道前方' not in reachable('XZ') and '赤道後方' not in {run(g) for g in 'XHZ'}

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q004：量子閘就是轉箭頭（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片約五分鐘，帶出今天的問題：怎麼把箭頭轉到想要的方向？

## 這份教材在做什麼

三種量子閘都是「繞一條軸轉半圈」。孩子先在紙上預測，再到 3D 場景按按鈕驗證，闖六關；下半場孩子當關主，出兩關給爸爸破。
不需要帳號；3D 場景見 `05_三維動畫導覽.md`。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 量子閘就是旋轉；X、H、Z 三條軸；閘可逆、測量不可逆 | 影片第 3–6 段、列印包第 1 頁 |
| 25–65 | 六關闖關（爸爸當關主、孩子當挑戰者） | `01_闖關說明.md`、列印包第 2 頁 |
| 65–75 | 休息 | |
| 75–105 | 孩子出兩關給爸爸破，寫參考解 | 列印包第 3 頁 |
| 105–115 | 孩子教爸爸：三種閘怎麼轉 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名 | |

## 課前準備（約 5 分鐘）

- 列印 `02_列印包_量子閘就是轉箭頭.pdf`（A4，共 4 頁）、鉛筆、色筆；可用一顆橘子或球插一根筷子當箭頭。
- 電腦打開 `animations/operation.html#gates`；讀一遍 `04_解答與旋轉表.md`。

## 關主的原則

- 先要孩子「說出預測」，再按按鈕；猜錯時請孩子找出是哪一顆閘轉錯。
- 第六關是陷阱關，答案是「過不了」；說得出理由就算過關。
- 驗收的兩個注意事項：同一個閘做兩次會回到原狀（例如 H 做兩次）；量子閘可以倒回去，測量不行。

## 誠實說明

- 「正前方」指 3D 場景預設視角下 x 軸朝向你的那一端（|+⟩）；轉動視角後前後會跟著變。
- 「翻轉閘」「相位翻轉閘」是英文 bit-flip、phase-flip 的意譯，按鈕上寫 X、Z。
- Z 閘改變的是相位，測量機率看不出來；為什麼它重要，下一堂（Q005 相位）再說。
''',

'01_闖關說明.md': '''# 闖關說明

## 規則

1. 每一關都從北極（|0⟩）出發。
2. 先在列印包第 2 頁寫下路線和顆數，再到 3D 場景按「重設 |0⟩」後依序按閘驗證。
3. 用的閘越少越厲害；過關後在表上打勾。
4. 每一關開始前按「清除軌跡」和「重設 |0⟩」。

## 六關

''' + ''.join(f'- **{n}**：{goal}（{rule}）\n' for n, goal, rule, _, _ in LEVELS) + '''
## 下半場：自己出兩關

1. 寫下目標位置（北極、南極、赤道前方、赤道後方之一）和可以用的閘。
2. 寫出你的參考解和最少顆數，先用 3D 場景自己試一次。
3. 給爸爸破；爸爸用的顆數比你的參考解少？那你的參考解還不是最少。
''',

'04_解答與旋轉表.md': '# 解答與旋轉表（爸爸用）\n\n## 三種閘的旋轉表（都轉半圈）\n\n'
  + '| 起點 | ' + ' | '.join(NAME[g] for g in 'XHZ') + ' |\n|---|---|---|---|\n'
  + ''.join(f'| {p} | ' + ' | '.join(TABLE[g][p] for g in 'XHZ') + ' |\n' for p in POS)
  + '\n## 六關解答\n\n| 關卡 | 目標 | 限制 | 參考解 | 最少顆數 |\n|---|---|---|---|---|\n'
  + ''.join(f'| {n} | {goal} | {rule} | {ans} | {k if k else "無解"} |\n' for n, goal, rule, ans, k in LEVELS)
  + '\n## 常見問題\n\n'
  '- 第三關為什麼不能一顆？三種閘從北極出發，只會到南極、赤道前方或留在北極。\n'
  '- 第四關的 H → Z → H 和 X 效果一樣：3D 場景有「示範：H → Z → H = X」按鈕可以對照。\n'
  '- 第六關：X 把北極和南極對調，Z 讓兩極不動，所以箭頭永遠離不開兩極。\n'
  '- 倒回去：一串 X、H、Z，從最後一顆開始倒著再按一次，就回到起點；測量之後就回不去了。\n',

'05_三維動畫導覽.md': '''# 三維動畫導覽

學程的三維動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路或伺服器。

## 今天要看的場景：`animations/operation.html#gates`（場景 2：單位元閘）

- 「X」「H」「Z」：按一下，箭頭繞粉紅色的旋轉軸轉半圈。
- 「重設 |0⟩」：箭頭回到北極；每一關開始前先按。
- 「清除軌跡」：擦掉箭頭走過的線。
- 下方讀數：測量機率 P(0)、P(1)；右下插圖：最後一個閘的矩陣與線路紀錄。
- 「示範：H → Z → H = X」：第四關做完再按來對照。
- 今天只用 X、H、Z；Y、S、T、√X、Rx/Ry/Rz 是延伸，之後的課會用到。

## 操作

滑鼠拖曳旋轉、滾輪縮放；`H` 隱藏面板；`R` 重設視角。
''',
}

SHEET_HEADER = ['關卡', '目標', '限制', '我預測的路線', '顆數', '動畫驗證結果', '過關']
SHEET_ROWS = ([[n, goal, rule, '', '', '', ''] for n, goal, rule, _, _ in LEVELS]
              + [['我出的第一關', '', '', '', '', '', ''], ['我出的第二關', '', '', '', '', '', '']])

EXTRA_CSS = '''table.rec td{height:13mm}table.rec td:nth-child(4){width:42mm}table.rot td,table.rot th{text-align:center}
.globe{display:flex;gap:8mm;align-items:center;margin-top:4mm}
.ball{width:62mm;height:62mm;border:1.4pt solid #0b2540;border-radius:50%;position:relative;flex:none;margin:6mm 26mm 6mm 24mm}
.ball:before{content:"";position:absolute;left:0;right:0;top:50%;border-top:1pt dashed #4a6a88}
.ball span{position:absolute;font-size:10pt;color:#0b2540;white-space:nowrap}
.chk li{margin:3mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}'''


def ball():
    return ('<div class="ball"><span style="top:-6mm;left:22mm">北極 |0⟩</span><span style="bottom:-6mm;left:22mm">南極 |1⟩</span>'
            '<span style="top:32mm;right:calc(100% + 2mm)">赤道前方 |+⟩</span><span style="top:24mm;left:calc(100% + 2mm)">赤道後方 |−⟩</span></div>')


def html():
    pages = [
        '<h2>三種閘，三條軸</h2><p class="lead">每一種閘都是繞著自己的軸轉半圈。軸上的箭頭不會動。</p>'
        '<div class="globe">' + ball() + '<div><p><b>X 翻轉閘</b>：繞前後軸（穿過赤道前方和後方）</p>'
        '<p><b>H 哈達瑪閘</b>：繞斜軸（北極和赤道前方的正中間）</p><p><b>Z 相位翻轉閘</b>：繞直立軸（穿過南北極）</p></div></div>'
        '<h3 style="margin-top:8mm">先預測，再用動畫對答案：箭頭會轉到哪裡？</h3>'
        '<table class="rot"><tr><th>起點</th><th>按 X</th><th>按 H</th><th>按 Z</th></tr>'
        + ''.join(f'<tr><td>{p}</td><td></td><td></td><td></td></tr>' for p in POS) + '</table>'
        '<p class="note">寫完以後檢查：哪些格子「轉了也不動」？那個點就在旋轉軸上。</p>',
        '<h2>闖關紀錄表：六關</h2><p class="lead">每一關都從北極出發。先寫路線和顆數，再按「重設 |0⟩」驗證。</p>'
        '<table class="rec"><tr><th>關卡</th><th>目標</th><th>限制</th><th>我的路線</th><th>顆數</th><th>過關</th></tr>'
        + ''.join(f'<tr><td>{n}</td><td>{goal}</td><td>{rule}</td><td></td><td></td><td>□</td></tr>' for n, goal, rule, _, _ in LEVELS)
        + '</table><p class="note">陷阱關如果過不了，寫下理由也算過關：＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p>',
        '<h2>下半場：換你當關主</h2><p class="lead">出兩關給爸爸破，先寫好參考解，用動畫試一次。</p>'
        + ''.join(f'<div class="box" style="margin-top:5mm"><h3>我出的第{c}關</h3>'
                  '<p>目標位置：＿＿＿＿＿＿　可以用的閘：□ X　□ H　□ Z</p>'
                  '<p>我的參考解：＿＿＿＿＿＿＿＿＿＿　最少顆數：＿＿＿</p>'
                  '<p>爸爸的解法：＿＿＿＿＿＿＿＿＿＿　爸爸用了幾顆：＿＿＿</p>'
                  '<p>動畫驗證：□ 真的過得了</p></div>' for c in '一二')
        + '<p class="note">爸爸比你用得少？那就再想一想，你的參考解是不是最少。</p>',
        '<h2>最後一關：教爸爸轉箭頭</h2><div class="box"><ul class="chk">'
        '<li>說出量子閘就是繞一條軸轉動箭頭</li><li>說出 X、H、Z 各繞哪一條軸</li>'
        '<li>從北極出發，預測連按兩顆閘之後箭頭在哪裡</li><li>說出同一個閘做兩次會回到原狀</li>'
        '<li>指出一個限制：量子閘可以倒回去，測量不行</li><li>替闖關紀錄表取名字、存檔</li></ul></div>'
        '<div class="box" style="margin-top:6mm"><h3>三句學習日誌</h3><p>我做了什麼：</p><div class="line"></div>'
        '<p>哪裡卡住：</p><div class="line"></div><p>下次想加什麼：</p><div class="line"></div></div>',
    ]
    return printpack.document('Q004 量子閘就是轉箭頭 列印包', '父子科技學院 量子電腦學程 Q004｜量子閘就是轉箭頭', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q004-gates-rotate', folder='Q004_量子閘就是轉箭頭', files=FILES,
        sheet=('03_闖關紀錄表.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_量子閘就是轉箭頭.pdf', pack_pages=4,
        pack_needles=('三種閘，三條軸', '闖關紀錄表', '陷阱關', '換你當關主', '最後一關'),
        authoring_dir=XINEW / 'authoring/q004', episode_dir='specials/q004-gates-rotate',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'levels': [{'name': n, 'goal': g, 'rule': r, 'answer': a, 'minGates': k} for n, g, r, a, k in LEVELS],
               'rotationTable': TABLE, 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q004/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')
