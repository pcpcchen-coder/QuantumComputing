"""Q056 課堂教材：耦合圖紙板、題卡、路由比賽紀錄、可執行的 routing_lab.py、說明卡與解答。

不需要帳號、不需要安裝套件（routing_lab.py 只用 Python 標準函式庫；也可以只用紙板與代幣）。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q056/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

PROGRAM = r'''"""父子科技學院 量子電腦學程 Q056：轉譯：邏輯線路到硬體 的路由裁判（只用 Python 標準函式庫）

執行：python routing_lab.py
對每一張題卡、每一張耦合圖，窮舉所有擺法與交換順序，找出「最少要插幾個 SWAP」，
並印出一組做法：一開始代幣怎麼擺、在哪裡交換。用來當效能競賽的裁判。
規則（和紙板遊戲相同）：
  - 題卡上的 CNOT 照順序做；做每個 CNOT 時，兩枚代幣必須在有連線的兩個圓點上。
  - 一次 SWAP = 把一條連線兩端的代幣（或代幣與空位）互換，記 1 分；1 個 SWAP = 3 個 CNOT。
改造區：在 BOARDS 加你自己的耦合圖、在CARDS 加你自己的題卡。
"""
from collections import deque
from itertools import permutations

BOARDS = {   # 圓點編號 → 連線
    '線形 5 顆': (5, [(0, 1), (1, 2), (2, 3), (3, 4)]),
    '方格 3×3': (9, [(0, 1), (1, 2), (3, 4), (4, 5), (6, 7), (7, 8), (0, 3), (3, 6), (1, 4), (4, 7), (2, 5), (5, 8)]),
    '重六角小片 7 顆': (7, [(0, 1), (1, 2), (1, 3), (3, 5), (4, 5), (5, 6)]),
}

CARDS = {    # 題卡：邏輯位元數、CNOT 順序（控制, 目標）
    'A 兩人組': (2, [(0, 1)]),
    'B 一拖二': (3, [(0, 1), (0, 2)]),
    'C 接力鏈': (4, [(0, 1), (1, 2), (2, 3)]),
    'D 一拖三': (4, [(0, 1), (0, 2), (0, 3)]),
    'E 三角形': (3, [(0, 1), (1, 2), (2, 0)]),
    'F 一拖四': (5, [(0, 1), (0, 2), (0, 3), (0, 4)]),
}


def solve(board, card):
    n, edges = BOARDS[board]
    k, gates = CARDS[card]
    if k > n:
        return None
    adj = {i: set() for i in range(n)}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    start = {}
    dist, back, dq = {}, {}, deque()
    for pl in permutations(range(n), k):          # pl[q] = 邏輯位元 q 所在的圓點
        s = (pl, 0)
        dist[s], back[s] = 0, None
        dq.append(s)
    while dq:                                     # 0-1 BFS：做 CNOT 不花分，SWAP 花 1 分
        s = dq.popleft()
        pl, g = s
        if g == len(gates):
            steps, cur = [], s
            while back[cur] is not None:
                prev, move = back[cur]
                if move:
                    steps.append(move)
                cur = prev
            return dist[s], cur[0], steps[::-1]
        a, b = gates[g]
        if pl[b] in adj[pl[a]]:
            t = (pl, g + 1)
            if t not in dist or dist[t] > dist[s]:
                dist[t], back[t] = dist[s], (s, None)
                dq.appendleft(t)
            continue
        for u, v in edges:
            npl = tuple(v if p == u else u if p == v else p for p in pl)
            if npl == pl:
                continue
            t = (npl, g)
            if t not in dist:
                dist[t], back[t] = dist[s] + 1, (s, f'SWAP 圓點{u}–{v}（在第 {g + 1} 個 CNOT 之前）')
                dq.append(t)


if __name__ == '__main__':
    for card, (k, gates) in CARDS.items():
        print(f'題卡 {card}：' + '、'.join(f'CNOT(q{a},q{b})' for a, b in gates))
        for board in BOARDS:
            r = solve(board, card)
            if r is None:
                print(f'  {board}：位元不夠')
                continue
            cnt, pl, steps = r
            place = '、'.join(f'q{q}→{p}' for q, p in enumerate(pl))
            print(f'  {board}：最少 {cnt} 個 SWAP（多 {3 * cnt} 個 CNOT）；擺法 {place}' + (f'；{"；".join(steps)}' if steps else ''))
    print('\n粗估：每個 CNOT 錯 1% 時，全部不出錯的機會 = 0.99 的 CNOT 數次方')
    for m in (1, 3, 4, 9):
        print(f'  {m} 個 CNOT：{0.99 ** m:.1%}')
'''

ns = {}
exec(compile(PROGRAM, 'routing_lab.py', 'exec'), ns)  # 用同一份程式算解答，避免手抄錯
SOL = {(c, b): ns['solve'](b, c) for c in ns['CARDS'] for b in ns['BOARDS']}
BOARDS = list(ns['BOARDS'])
CARDS = ns['CARDS']


def ans_cell(card, board):
    r = SOL[(card, board)]
    if r is None:
        return '—'
    cnt, pl, steps = r
    return f'{cnt}（擺法 ' + '、'.join(f'q{q}→{p}' for q, p in enumerate(pl)) + '）'


CARD_TEXT = {
    'A 兩人組': '熱身：兩顆位元做一次 CNOT。',
    'B 一拖二': 'q0 要和 q1、q2 各做一次（像三顆一起糾纏的線路）。',
    'C 接力鏈': '一個接一個傳下去。',
    'D 一拖三': '影片裡的例題：一顆要碰三顆。',
    'E 三角形': '三顆兩兩都要碰一次。',
    'F 一拖四': '挑戰題：一顆要碰四顆。',
}

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q056：轉譯：邏輯線路到硬體（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。今天的核心一句：**我們寫的線路不能直接上晶片，要經過轉譯：① 分解成原生閘、② 配置到實體位元、③ 路由（兩端不相鄰就插 SWAP）、④ 最佳化（抵消、合併）。** 一個 SWAP 等於三個 CNOT，會大幅增加錯誤，所以好的轉譯要盡量少插 SWAP。好玩機制是效能競賽：同一張題卡、同一張耦合圖，比誰插的 SWAP 最少。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 打開動畫第 12 章第 9 步，看 Bell、BV 在直線晶片上的轉譯結果 | `transmon-3d.html#stack` |
| 25–65 | 效能競賽：在線形紙板上做題卡 A–E，各自擺、交換核對 | 列印包第 1、2、3 頁 |
| 65–75 | 休息 | |
| 75–105 | 改造：同一張題卡換方格、重六角小片，比較 SWAP 數；挑戰題 F | 列印包第 1、3 頁、`routing_lab.py` |
| 105–115 | 孩子教爸爸：四道工序、怎麼路由、一個限制 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 15 分鐘）

- 列印 `02_列印包_轉譯邏輯線路到硬體.pdf`（A4，共 4 頁）。第 1 頁是耦合圖紙板（可貼在厚紙板上），第 2 頁題卡沿虛線剪開。
- 代幣：準備 5 枚可以寫字的代幣（硬幣貼紙、瓶蓋、圓形便利貼都可以），分別寫 q0～q4。
- 下載學程的 `animations/` 資料夾，用瀏覽器開 `transmon-3d.html#stack`（需連網載入 three.js；不需要帳號）。
- 讀一遍 `04_解答.md`。

## 遊戲規則（給孩子）

1. 抽一張題卡，把需要的代幣擺到紙板的圓點上（一個圓點最多一枚）。
2. 照題卡順序做每個 CNOT：兩枚代幣之間有連線 → 打勾；沒有 → 先 SWAP。
3. SWAP：選一條連線，把兩端的代幣（或代幣和空位）互換，記 1 分。
4. 全部做完，分數最低的人贏；交換紀錄互相核對，有一步不相鄰就不算。

## 誠實說明

- 「重六角小片」是七顆位元的教學用簡化圖（每顆最多 2–3 個鄰居），不是任何一台機器的完整耦合圖。
- 動畫裡的轉譯器是教學用的簡化版本：BV 在直線上插了 2 個 SWAP，但最少只要 1 個（`routing_lab.py` 可驗證）。真正的轉譯器也用近似方法，不保證最少。
- 解答的「最少 SWAP」是 `routing_lab.py` 窮舉所有擺法與交換順序得到的；擺法可能不只一種。
''',

'01_操作步驟.md': '''# 操作步驟

## 先看動畫（約 15 分鐘）

1. 打開 `animations/transmon-3d.html#stack`，取消「自動接續」，按步驟按鈕「9」進入自由實驗。
2. 電路按「Bell」，晶片「直線 5 顆」，一直按「下一階段 ▶」：看 CNOT 怎麼變成 H、CZ、H，最佳化後 H 又展開成 Rz、√X、Rz。
3. 電路按「BV」，按到「③ 路由」：左上角寫著插了幾個 SWAP、CZ 從幾個變成幾個？紫色的閘就是 SWAP 拆開後的閘。
4. 晶片按「方格 3×3」，再按「◀ 上一階段」「下一階段 ▶」刷新說明：SWAP 變成幾個？再按到「⑤ 排程與脈衝」比較總時間。

## 效能競賽（約 40 分鐘）

1. 兩人各拿一套代幣，用同一張線形紙板（或各畫一張）。
2. 抽題卡 A～E，各自擺代幣、照順序走，在列印包第 3 頁記下擺法與 SWAP 數。
3. 交換紀錄核對：每個 CNOT 時兩枚代幣真的相鄰嗎？每次互換都算分了嗎？
4. 分數較低者贏；平手時比誰先完成。

## 改造：換耦合圖（約 30 分鐘）

1. 同一張題卡分別放到線形、方格、重六角小片，記錄三種 SWAP 數。
2. 挑戰題 F（一拖四）：哪一種耦合圖可以 0 個 SWAP？為什麼？
3. 執行 `python routing_lab.py`，看看你們的分數是不是最少。
''',

'routing_lab.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n'
  '以下由 `routing_lab.py` 窮舉算出：「最少 SWAP 數（一種起始擺法，q→圓點編號）」。圓點編號見列印包第 1 頁。擺法可能不只一種。\n\n'
  '| 題卡 | ' + ' | '.join(BOARDS) + ' |\n|---|' + '---|' * len(BOARDS) + '\n'
  + ''.join(f'| {c} | ' + ' | '.join(ans_cell(c, b) for b in BOARDS) + ' |\n' for c in CARDS)
  + '\n## 重點\n\n'
  '- B 一拖二：在線形上把 q0 放中間，兩個鄰居放 q1、q2，0 個 SWAP。\n'
  '- D 一拖三：線形每顆最多 2 個鄰居，至少 1 個 SWAP；方格與重六角小片有 3 個鄰居的點，0 個。動畫裡的簡單轉譯器在線形上插了 2 個。\n'
  '- E 三角形：三種紙板都沒有三角形的連線，至少要 1 個 SWAP。\n'
  '- F 一拖四：只有方格正中間（圓點 4）有 4 個鄰居，所以方格 0 個；重六角小片 1 個；線形 2 個。\n'
  '- 代價：1 個 SWAP = 3 個 CNOT。每個 CNOT 錯 1% 時，3 個 CNOT 全對約 97.0%，9 個約 91.4%。\n\n'
  '## 動畫裡會看到（第 12 章第 9 步）\n\n'
  '- Bell @ 直線：分解後 q1 為 H、CZ、H；最佳化：√X 3、Rz 6（0 ns）、CZ 1。\n'
  '- BV @ 直線：映射 q3→Q2，有 1 個 CZ 兩端不相鄰（紅色）；路由插 2 個 SWAP，CZ 3 → 9；總時間 1320 ns。\n'
  '- BV @ 方格：q3→Q1（後排中間，鄰居 Q0、Q2、Q4），0 個 SWAP，CZ 3；總時間 840 ns。\n\n'
  '## 常見誤解\n\n'
  '- 「SWAP 只是換位置，很便宜」：1 個 SWAP = 3 個 CNOT，而兩位元閘是最容易出錯的閘。\n'
  '- 「轉譯器一定找到最少 SWAP」：大型線路找最少 SWAP 非常困難（NP-hard），實務用啟發式；動畫的 BV 就多插了一個。\n'
  '- 「鄰居越多的晶片一定越好」：鄰居多，頻率互相干擾的機會也多；重六角就是用較少鄰居換較少干擾，代價是多 SWAP。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟（transmon-3d.html 需連網載入 three.js，不需要帳號）。

## `animations/transmon-3d.html#stack`（第 12 章：編譯與控制軟體堆疊，課綱指定）

- 右邊面板有步驟按鈕 1～9；先取消「自動接續」，否則會自己跳步。
- 第 2 步分解、第 3 步映射、第 4 步路由、第 5 步最佳化、第 6 步排程與脈衝；第 9 步是自由實驗。
- 自由實驗：電路「Bell／GHZ／BV」、晶片「直線 5 顆／方格 3×3」、「◀ 上一階段」「下一階段 ▶」「播放脈衝」「執行 2000 shots」。
- 上方看板是電路（青＝單位元閘、金＝Rz、橘＝CZ、紅＝兩端不相鄰、紫＝SWAP 展開、藍＝量測），下方看板是統計或脈衝時間軸，地上是晶片（金色＝被選中的實體位元）。
- 左上角字幕在按「下一階段」時更新；換晶片後按一次「上一階段」再「下一階段」刷新。

## 操作

滑鼠拖曳旋轉、滾輪縮放；左右方向鍵切換章節。
''',
}

SHEET_HEADER = ['題卡', '耦合圖', '起始擺法', '我的 SWAP 數', '爸爸的 SWAP 數', '最少（裁判）', '核對 □']
SHEET_ROWS = [[c, b] for c in CARDS for b in BOARDS]

EXTRA_CSS = '''svg.bd{display:block;margin:0 auto}.bd circle{fill:#fff;stroke:#0b2540;stroke-width:1.4}
.bd line{stroke:#35a9d6;stroke-width:3.2}.bd text{font-size:7px;fill:#4a6a88;font-family:sans-serif}
.bds{display:grid;grid-template-columns:1fr 1fr;gap:4mm;margin-top:3mm}.bds h3,.bl h3{font-size:12.5pt;margin:0 0 1mm}
.cards{display:grid;grid-template-columns:1fr 1fr;gap:4mm}.cards .cut{padding:3.5mm 4.5mm;height:74mm}
.cards h3{font-size:15pt;margin:0 0 1.5mm}.cards p{margin:1.2mm 0;font-size:11.5pt}.cards .g{font-size:13pt;font-weight:700;color:#0b2540}
table.rc td{height:9.5mm;text-align:center}table.rc th{text-align:center;font-size:10pt}
.chk li{margin:2mm 0;font-size:12.5pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}'''

LAYOUT = {   # 圓點座標（mm）
    '線形 5 顆': [(12 + 34 * i, 12) for i in range(5)],
    '方格 3×3': [(12 + 30 * (i % 3), 12 + 30 * (i // 3)) for i in range(9)],
    '重六角小片 7 顆': [(12, 12), (42, 12), (72, 12), (42, 42), (12, 72), (42, 72), (72, 72)],
}


def svg(board):
    n, edges = ns['BOARDS'][board]
    pts = LAYOUT[board]
    w = max(x for x, _ in pts) + 12
    h = max(y for _, y in pts) + 12
    lines = ''.join(f'<line x1="{pts[a][0]}" y1="{pts[a][1]}" x2="{pts[b][0]}" y2="{pts[b][1]}"/>' for a, b in edges)
    dots = ''.join(f'<circle cx="{x}" cy="{y}" r="10"/><text x="{x + 7}" y="{y - 8}">{i}</text>' for i, (x, y) in enumerate(pts))
    return f'<svg class="bd" width="{w}mm" height="{h}mm" viewBox="0 0 {w} {h}">{lines}{dots}</svg>'


def html():
    cards = ''.join(f'<div class="cut"><h3>題卡 {c}</h3><p>{CARD_TEXT[c]}</p>'
                    f'<p class="g">' + '　'.join(f'{i}. CNOT(q{a}, q{b})' for i, (a, b) in enumerate(g, 1)) + '</p>'
                    f'<p>需要代幣：' + '、'.join(f'q{q}' for q in range(k)) + '</p>'
                    '<p>我的 SWAP：＿＿＿　爸爸的 SWAP：＿＿＿</p></div>' for c, (k, g) in CARDS.items())
    rows = ''.join(f'<tr><td>{k}</td><td></td><td></td><td></td><td></td><td></td><td>□</td></tr>' for k in range(1, 10))
    pages = [
        '<h2>耦合圖紙板</h2><p class="lead">圓點＝實體位元（旁邊的小字是編號），藍線＝可以直接做兩位元閘的連線。代幣寫 q0～q4，一個圓點最多放一枚。</p>'
        f'<div class="bl"><h3>線形 5 顆（每顆最多 2 個鄰居）</h3>{svg("線形 5 顆")}</div>'
        f'<div class="bds"><div><h3>方格 3×3（正中間 4 個鄰居）</h3>{svg("方格 3×3")}</div>'
        f'<div><h3>重六角小片 7 顆（每顆最多 3 個鄰居）</h3>{svg("重六角小片 7 顆")}</div></div>'
        '<p class="note">重六角小片是教學用的簡化圖，不是任何一台機器的完整耦合圖。</p>',
        '<h2>題卡</h2><p class="lead">沿虛線剪開。照順序做 CNOT；兩枚代幣不相鄰就先 SWAP（互換一條連線兩端），每次記 1 分。</p>'
        f'<div class="cards">{cards}</div>',
        '<h2>路由比賽紀錄</h2><p class="lead">效能競賽：同一張題卡、同一張耦合圖，SWAP 最少且核對全對的人贏。1 個 SWAP = 3 個 CNOT。</p>'
        '<table class="rc"><tr><th>局</th><th>題卡</th><th>耦合圖</th><th>起始擺法</th><th>我的<br>SWAP</th><th>爸爸的<br>SWAP</th><th>核對</th></tr>'
        f'{rows}</table>'
        '<div class="box" style="margin-top:4mm"><p>1. 同一張題卡在三種耦合圖上的 SWAP 數：線形＿＿　方格＿＿　重六角＿＿</p>'
        '<p>2. 哪一種耦合圖最省 SWAP？為什麼有人還是選鄰居少的？</p><div class="line"></div>'
        '<p>3. 我的妙招（怎麼擺最省）：</p><div class="line"></div></div>',
        '<h2>說明卡：我的路由比賽紀錄</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 轉譯：邏輯線路到硬體在解決什麼？</p><div class="line"></div><p>2. 我怎麼做？</p><div class="line"></div>'
        '<p>3. 哪裡容易錯？真實的量子電腦哪裡會用到？</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:4mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出四道工序：分解、配置、路由、最佳化</li>'
        '<li>示範：兩端不相鄰的 CNOT，用 SWAP 搬到隔壁再做</li>'
        '<li>說出擺代幣的妙招：互動多的位元放在鄰居多的位置</li>'
        '<li>指出限制：1 個 SWAP ＝ 3 個 CNOT，會大幅增加錯誤</li>'
        '<li>替路由比賽紀錄取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q056 轉譯：邏輯線路到硬體 列印包', '父子科技學院 量子電腦學程 Q056｜轉譯：邏輯線路到硬體', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q056-transpile-routing', folder='Q056_轉譯邏輯線路到硬體', files=FILES,
        sheet=('03_路由比賽紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_轉譯邏輯線路到硬體.pdf', pack_pages=4,
        pack_needles=('耦合圖紙板', '題卡', '路由比賽紀錄', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q056', episode_dir='specials/q056-transpile-routing',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'program': 'routing_lab.py', 'puzzleCards': list(CARDS), 'boards': BOARDS,
               'transpileFrom': 'slides/QC_Operation_Talk.pptx p26', 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q056/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')
