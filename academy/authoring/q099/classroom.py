"""Q099 課堂教材：第 1 課：SQUID 干涉之後能做什麼 — 動畫操作步驟、SQUID 調頻筆記、角色扮演對話卡、自己出題、說明卡與解答。

免安裝、不需帳號：只用學程的 animations/index.html（#squid）與 transmon-3d.html（#case），用瀏覽器開啟。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q099/classroom.py
"""
from pathlib import Path
import math
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 06_squid.js 的模型：E_JΣ/h = 20 GHz、E_C/h = 250 MHz；E_J(Φ) = E_JΣ √(cos² + d² sin²)；f₀₁ = max(0, √(8E_J E_C) − E_C)
EJS, EC = 20.0, 0.25


def ej(phi, d=0.0):
    c, s = math.cos(math.pi * phi), math.sin(math.pi * phi)
    return EJS * math.sqrt(c * c + d * d * s * s)


def f01(phi, d=0.0):
    return max(0.0, math.sqrt(8 * ej(phi, d) * EC) - EC)


PHIS = [0, 0.1, 0.2, 0.25, 0.3, 0.4, 0.5]
TABLE = [(p, round(f01(p), 2), round(f01(p, 0.5), 2), round(ej(p) / EC)) for p in PHIS]
assert TABLE[0][1] == 6.07 and TABLE[-1][1] == 0 and TABLE[-1][2] == 4.22

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q099：第 1 課：SQUID 干涉之後能做什麼（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。今天用「師生對話」的方式上課：一人當老師、一人當學生，讀學程的
《超導量子電腦師生對話教學紀錄》第 1 課，再到 3D 動畫裡調磁通。

只需要瀏覽器：下載學程的 `animations/` 資料夾，開 `index.html#squid` 和 `transmon-3d.html#case`；對話原文在 `docs/超導量子電腦師生對話教學紀錄.md`。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 旋鈕是磁通、四步因果、Φ = 0 與 Φ₀/2、甜蜜點 | 影片第 3–6 段、`05_動畫導覽.md` |
| 25–65 | 分角色讀對話第 1 課，再到動畫調磁通、填調頻筆記 | `01_操作步驟.md`、列印包第 1–2 頁 |
| 65–75 | 休息 | |
| 75–105 | 孩子自己出題：磁通調太多會怎樣？找線索回答 | 列印包第 3 頁、`03_調頻紀錄.csv` |
| 105–115 | 孩子教爸爸：操作與原理 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 讀一遍對話第 1 課（學生只問了一句話，老師先修正觀念，再列用途表）。
- 在 `index.html#squid` 拖「外加磁通 Φ / Φ₀」滑桿，看右下角小圖的青色圓點怎麼沿曲線移動。
- 列印 `02_列印包_SQUID調頻筆記.pdf`（A4，共 4 頁）。讀一遍 `04_解答.md`。

## 角色扮演怎麼玩

第一輪爸爸當老師、孩子當學生，照原文各讀一遍。第二輪交換：孩子當老師，爸爸故意問錯的問題
（「所以是直接改兩個 JJ 的相位嗎？」「甜蜜點就完全不怕雜訊了嗎？」），看孩子能不能修正。

## 誠實說明

- 動畫插圖用的是代表值（E_JΣ/h = 20 GHz、E_C/h = 250 MHz），不是某顆晶片的量測。
- 對稱 SQUID 在 Φ₀/2 時，動畫的頻率掉到 0，是公式取 max(0, …) 的結果；真實元件到那裡早已不是 transmon。
- 本課最重要的注意事項：可調頻率也會帶來磁通雜訊；甜蜜點只是一階不敏感。
''',

'01_操作步驟.md': '''# 操作步驟

## A. 讀對話（約 15 分鐘）

1. 打開 `docs/超導量子電腦師生對話教學紀錄.md` 第 1 課。
2. 學生念「🧑‍🎓 學生」那一句，老師念「👩‍🏫 老師」的回答；讀到用途表時，兩人輪流念一列。
3. 讀完，學生用自己的話說一次：老師修正了什麼觀念？

## B. 調磁通（`index.html#squid`，約 20 分鐘）

1. 把「接面不對稱度 d」拉到 0，「外加磁通 Φ / Φ₀」拉到 0。看：環中間沒有箭頭、兩個 JJ 最亮、小圖圓點在最高點（甜蜜點）。
2. 依序把磁通調到 0.1、0.2、0.25、0.3、0.4、0.5，每次在列印包第 1 頁記下小圖上圓點的高度（頻率，GHz）。
3. 再把 d 拉到 0.5，重做一次。比較金色曲線（現在的 d）和灰色曲線（d = 0）。
4. 在甜蜜點附近小小地來回拖，再到 0.25 附近小小地來回拖，比較圓點上下動的幅度。

## C. 晶片上的樣子（`transmon-3d.html#case`，約 5 分鐘）

1. 按步驟按鈕「2」（SQUID 調頻）。看最左邊 Q1 的 SQUID 冒出銅色箭頭、看板小圖的圓點下滑、頻率尺上的實線左移並微微抖動。
2. 想一想：為什麼頻率只能往下調？

## D. 下半場：自己出題（約 30 分鐘）

用列印包第 3 頁，寫下你要問老師的題目「磁通調太多會怎樣？」，再到動畫裡找三個線索回答。
''',

'04_解答.md': '# 解答（爸爸用）\n\n## 調頻紀錄（以動畫 06_squid.js 的模型重算：E_JΣ/h = 20 GHz、E_C/h = 250 MHz）\n\n'
  '| Φ / Φ₀ | f₀₁（d = 0） | f₀₁（d = 0.5） | E_J/E_C（d = 0） |\n|---|---|---|---|\n'
  + ''.join(f'| {p} | {a} GHz | {b} GHz | {r} |\n' for p, a, b, r in TABLE)
  + '\n動畫小圖只能目測，讀到 ±0.2 GHz 以內就算對。重點：d = 0 時頻率從 6.07 GHz 一路掉到 0；d = 0.5 時最低只到約 4.22 GHz。\n\n'
  '## 磁通調太多會怎樣（三個線索）\n\n'
  '1. 對稱 SQUID 靠近 Φ₀/2，等效 E_J 趨近 0，頻率掉到底（動畫取 max(0, …)）。\n'
  '2. E_J/E_C 比值一路變小；transmon-3d 第 1 章把比值小於 20 判為「電荷雜訊主導」，表格裡 Φ = 0.4 時已只剩約 25。\n'
  '3. 離甜蜜點越遠，曲線越陡，同樣的磁通雜訊造成越大的頻率抖動；調過一整個 Φ₀，頻率又繞回來（週期性）。\n\n'
  '## 常見問題\n\n'
  '- 是不是直接改兩個 JJ 的電流相位？不是。能控制的是穿過環的磁通 Φ，它把兩個 JJ 的相位差綁成 2πΦ/Φ₀。\n'
  '- 為什麼只能往下調？E_J(Φ) 的最大值在 Φ = 0，任何磁通都讓 E_J 變小、頻率變低。\n'
  '- 甜蜜點就完全不怕雜訊嗎？不是，只是一階不敏感（df/dΦ = 0），二階效應還在。\n'
  '- 不對稱 SQUID 換到什麼？調頻範圍變小，換來整段曲線對磁通雜訊比較不敏感。\n'
  '- SQUID 會寫入狀態嗎？不會。它只決定頻率；寫入靠 XY 線的微波脈衝（下一課）。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路或帳號。

## `index.html#squid`（超導場景 6：DC SQUID）

- 滑桿「外加磁通 Φ / Φ₀」：-1 到 1。環中間的淺藍色箭頭代表穿過環的磁通，環上的光點代表屏蔽電流（示意）。
- 滑桿「接面不對稱度 d」：0 到 0.8。d 越大，金色曲線越平緩。
- 開關「自動掃描磁通」：磁通自動來回掃。
- 右下小圖：灰色是 d = 0 的曲線，金色是目前 d 的曲線，青色圓點是目前的磁通；曲線頂端標著「甜蜜點」。
- 兩個橘紅色 JJ 的亮度代表等效 E_J 的大小。

## `transmon-3d.html#case`（第 6 章：三顆可調 transmon 的頻率配置）

- 步驟 1–6；步驟 2「SQUID 調頻」示範 Q1 的 Z 線送電流、磁通穿過 SQUID、頻率往下調再回來。
- 看板左邊是 E_J(Φ)/E_J,max = |cos(πΦ/Φ₀)| 小圖，右邊是頻率尺（往右頻率越高）。
- 「自動接續」打勾時，每一步播完會自動進下一步。

## 操作

`H` 隱藏面板；滑鼠拖曳旋轉、滾輪縮放。
''',
}

SHEET_HEADER = ['項目', 'Φ / Φ₀', 'd', '我讀到的 f₀₁（GHz）', '接面亮不亮', '光點有沒有繞圈', '備註']
SHEET_ROWS = ([['調頻紀錄', str(p), '0', '', '', '', ''] for p in PHIS]
              + [['調頻紀錄', str(p), '0.5', '', '', '', ''] for p in PHIS]
              + [['自己出題', '', '', '', '', '', '線索 1'], ['自己出題', '', '', '', '', '', '線索 2'], ['自己出題', '', '', '', '', '', '線索 3']])

EXTRA_CSS = '''table.rec td{height:9mm}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.card{border:2pt solid #0b2540;border-radius:4mm;padding:5mm;margin-top:5mm}.card h3{margin-top:0}'''


def html():
    pages = [
        '<h2>SQUID 調頻筆記（今天的作品）</h2><p class="lead">在 index.html#squid：拖「外加磁通 Φ / Φ₀」，讀右下小圖青色圓點的高度。</p>'
        '<table class="rec"><tr><th>Φ / Φ₀</th><th>f₀₁（d = 0）</th><th>f₀₁（d = 0.5）</th><th>JJ 亮不亮</th><th>光點繞圈嗎</th></tr>'
        + ''.join(f'<tr><td>{p}</td><td></td><td></td><td></td><td></td></tr>' for p in PHIS) + '</table>'
        '<div class="card"><h3>我的觀察</h3><p>甜蜜點在 Φ = ＿＿＿，因為：</p><div class="line"></div>'
        '<p>d 變大，曲線變得：＿＿＿＿＿＿　作品名稱：＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p></div>',
        '<h2>角色扮演：老師與學生</h2><p class="lead">照師生對話第 1 課讀一遍，再交換角色。</p>'
        '<div class="box"><p><b>學生：</b>用 SQUID 架構改變兩個 JJ 的電流相位後，兩個電流產生干涉，然後可以做啥？</p>'
        '<p><b>老師要先修正的觀念：</b></p><div class="line"></div>'
        '<p><b>干涉之後得到什麼：</b></p><div class="line"></div></div>'
        '<table class="rec"><tr><th>用途</th><th>怎麼用干涉</th><th>例子</th></tr>'
        '<tr><td>量磁場</td><td></td><td></td></tr><tr><td>調參數</td><td></td><td></td></tr><tr><td>當位元本身</td><td></td><td></td></tr></table>'
        '<p class="note">交換後，爸爸故意問錯：「所以是直接改相位嗎？」「甜蜜點完全不怕雜訊嗎？」你怎麼修正？＿＿＿＿＿＿＿＿</p>',
        '<h2>換你出題：磁通調太多會怎樣</h2><p class="lead">先寫下你的題目，再到動畫裡找三個線索。</p>'
        '<div class="box"><p>我的題目：</p><div class="line"></div></div>'
        '<table class="rec"><tr><th>線索</th><th>我在動畫裡看到什麼</th><th>這代表什麼</th></tr>'
        '<tr><td>1. 頻率</td><td></td><td></td></tr><tr><td>2. E_J/E_C 比值</td><td></td><td></td></tr><tr><td>3. 曲線斜率</td><td></td><td></td></tr></table>'
        '<p class="note">生活技能：用提問推進理解——一個好問題，常常比十個答案更有用。你下一個想問的問題：＿＿＿＿＿＿＿＿</p>',
        '<h2>說明卡與最後一關</h2><div class="box"><p>1. SQUID 是什麼？控制旋鈕是什麼？</p><div class="line"></div>'
        '<p>2. 磁通 → E_J → 頻率，怎麼連起來？</p><div class="line"></div><p>3. 甜蜜點在哪裡？為什麼要停在那裡？</p><div class="line"></div>'
        '<p>4. 一個限制或注意事項：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出：兩個 JJ 並聯成環，用磁通調等效 E_J 與頻率</li><li>說出週期是一個磁通量子 Φ₀</li>'
        '<li>說出甜蜜點 Φ = 0：曲線是平的，一階不敏感</li><li>指出一個限制：可調頻率也帶來磁通雜訊</li>'
        '<li>替 SQUID 調頻筆記取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q099 SQUID 調頻筆記列印包', '父子科技學院 量子電腦學程 Q099｜第 1 課：SQUID 干涉之後能做什麼', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q099-squid-flux-tuning', folder='Q099_SQUID干涉之後能做什麼', files=FILES,
        sheet=('03_調頻紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_SQUID調頻筆記.pdf', pack_pages=4,
        pack_needles=('SQUID 調頻筆記', '角色扮演', '磁通調太多會怎樣', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q099', episode_dir='specials/q099-squid-flux-tuning',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'scenes': ['animations/index.html#squid', 'animations/transmon-3d.html#case'],
               'f01TableGHz': {str(p): {'d0': a, 'd0.5': b} for p, a, b, _ in TABLE}, 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q099/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')
