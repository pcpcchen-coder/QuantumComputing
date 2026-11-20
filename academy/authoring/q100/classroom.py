"""Q100 課堂教材：第 2 課：transmon 怎麼寫入狀態 — 動畫操作步驟、闖關紀錄、XY／Z 線分工圖（接線圖）、說明卡與解答。

免安裝、不需帳號：只用學程的 animations/transmon-3d.html（#chip、#control、#case），用瀏覽器開啟。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q100/classroom.py
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

# transmon-3d.html 第 6 章的模型（Q1）：E_J,max = 14.49、E_C = 0.25、d = 0.013 GHz；f₀₁ = √(8 E_J E_C) − E_C − d
EJMAX_Q1, EC, D = 14.49, 0.25, 0.013


def f_q1(phi):
    return max(0.0, math.sqrt(8 * EJMAX_Q1 * abs(math.cos(math.pi * phi)) * EC) - EC - D)


PHIS = [0.0, 0.05, 0.1, 0.129, 0.15, 0.2]
TABLE = [(p, round(f_q1(p), 2)) for p in PHIS]
assert TABLE[0][1] == 5.12 and TABLE[3][1] == 4.90 and TABLE[-1][1] == 4.58

# 師生對話紀錄第 2 課的代表值（E_J,max/h = 15 GHz）
DOC_Z = [('Φ = 0（sweet spot）', '15 GHz', '5.21 GHz'), ('0.1 Φ₀', '14.3 GHz', '降約 130 MHz'), ('0.25 Φ₀', '10.6 GHz', '約 4.4 GHz')]

LINES = [('XY 驅動線', '左下', 'f₀₁ 的微波脈衝（約 5 GHz）', '電容（電場）', '狀態：寫入'),
         ('Z 磁通線', '右下', '電流 → 磁通穿過 SQUID', '電感（磁場）', '頻率：調頻'),
         ('讀取共振腔＋饋線', '上方', '約 7 GHz 探測微波', '耦合 g（本課不細談）', '讀出結果')]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q100：第 2 課：transmon 怎麼寫入狀態（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片接續師生對話第 2 課：學生問「transmon 怎麼寫入狀態？SQUID 的作用是什麼？」

只需要瀏覽器：下載學程的 `animations/` 資料夾，開 `transmon-3d.html#chip`、`#control`、`#case`。不需要網路、帳號或安裝。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 晶片分工、寫入四步、脈衝三個旋鈕、SQUID 兩個身分 | 影片第 3–8 段、`05_動畫導覽.md` |
| 25–65 | 送 π 脈衝、比較 π 與 π/2、拖 Z 線磁通；玩闖關 | `01_操作步驟.md`、列印包第 1–2 頁 |
| 65–75 | 休息 | |
| 75–105 | 畫「哪條線做什麼」的接線圖（XY／Z 線分工圖） | 列印包第 3 頁 |
| 105–115 | 孩子教爸爸：怎麼寫入、Z 線做什麼 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 先自己在 `#chip` 按「送出 π 脈衝」，再到 `#case` 點步驟 6「自由實驗」，拖「Q1 Φ」滑桿、按「π → Q1」。
- 列印 `02_列印包_transmon寫入.pdf`（A4，共 4 頁）。讀一遍 `04_解答.md`。

## 闖關怎麼玩

爸爸當關主，每關問一題（見列印包第 2 頁），孩子答對才過關；答錯就回動畫再看一次。

## 誠實說明

- 動畫的頻率、磁通與激發機率是用代表值的模型算的，不是某顆晶片的量測；第 6 章的 T₁ 衰減刻意放慢以便觀察。
- 對話紀錄裡的「0.25 Φ₀ → 約 4.4 GHz」是代表值。
- 本課最重要的注意事項：寫入用的是 XY 線的微波脈衝；Z 線只改頻率，本身不會把 |0⟩ 變成 |1⟩。
''',

'01_操作步驟.md': '''# 操作步驟

## 第一關：認線（`transmon-3d.html#chip`，約 10 分鐘）

1. 勾選「顯示標籤」，找出十字電容板、SQUID（兩個約瑟夫森結）、XY 驅動線、Z 磁通線、讀取共振腔、饋線。
2. 按「送出 π 脈衝」：青綠色小點沿 XY 驅動線跑到十字板，十字板發金光（|1⟩），之後慢慢變暗（T₁ 衰減）。
3. 回答：哪一條線在工作？Z 磁通線有沒有動？

## 第二關：寫入（`transmon-3d.html#control`，約 15 分鐘）

1. 按「重設 |0⟩」→「X 軸 π」：箭頭從北極轉到南極，能階梯上 |1⟩ 變粗。
2. 按「重設 |0⟩」→「X 軸 π/2」：箭頭停在赤道。再「重設 |0⟩」→「Y 軸 π/2」：也停在赤道，但方向不同。
3. 按「持續驅動（Rabi 振盪）」看箭頭連續轉，再按「停止驅動」。把觀察記在列印包第 1 頁。

## 第三關：調頻（`transmon-3d.html#case`，約 15 分鐘）

1. 取消「自動接續」，點步驟按鈕 6（自由實驗）。
2. 拖「Q1 Φ」滑桿，從約 0.13 拖到 0.2：頻率尺上 Q1 的線往左移（頻率變低），Q1 的十字板不會亮。
3. 按「π → Q1」：小點沿 XY 線跑到 Q1，十字板亮起來。
4. 按「回到配置」。把 Φ 與頻率記在列印包第 1 頁（面板上的 Q1 欄依序是 f₀₁、Φ、P(|1⟩)）。

## 下半場：畫接線圖（約 30 分鐘）

用列印包第 3 頁：畫十字、SQUID、三條線，每條線寫「送什麼、怎麼耦合、改什麼」。
''',

'04_解答.md': '# 解答（爸爸用）\n\n## 晶片上的分工（師生對話紀錄第 2 課、簡報第 11 頁）\n\n'
  '| 線 | 位置 | 送什麼 | 耦合方式 | 改變什麼 |\n|---|---|---|---|---|\n'
  + ''.join(f'| {a} | {b} | {c} | {d} | {e} |\n' for a, b, c, d, e in LINES)
  + '\n十字電容 C_Σ ≈ 77.5 fF；SQUID 是非線性電感，也是頻率旋鈕。**SQUID 不負責寫入，XY 線才負責寫入。**\n\n'
  '## 脈衝的三個旋鈕\n\n| 參數 | 控制 | 例子 |\n|---|---|---|\n'
  '| 振幅 × 時間（面積） | 旋轉角度 | π：\\|0⟩→\\|1⟩；π/2：停在赤道 |\n| 微波相位 | 繞哪一軸 | 0° 繞 X、90° 繞 Y |\n| 頻率 | 哪一對能階 | 5.21 GHz 只驅動 0↔1（1→2 低 283 MHz） |\n\n'
  '## Z 線磁通與頻率\n\n對話紀錄的代表值（E_J,max/h = 15 GHz）：\n\n| Z 線磁通 | E_J/h | f₀₁ |\n|---|---|---|\n'
  + ''.join(f'| {a} | {b} | {c} |\n' for a, b, c in DOC_Z)
  + '\n動畫第 6 章 Q1 的模型值：\n\n| Φ / Φ₀ | f₀₁（GHz） |\n|---|---|\n'
  + ''.join(f'| {p:.3f} | {f:.2f} |\n' for p, f in TABLE)
  + '\n## 常見問題\n\n'
  '- Z 線調頻會不會順便把 |0⟩ 變成 |1⟩？不會。它只改頻率；要改狀態，得送對準新頻率的 XY 微波脈衝。\n'
  '- 為什麼寫入一律從 |0⟩ 開始？晶片在 10–20 mK，熱能約 0.2–0.4 GHz，遠小於 5.21 GHz，靜置後 > 99% 在 |0⟩；不想等就量一次、量到 1 補一個 π 脈衝（主動重設）。\n'
  '- XY 線為什麼不直接接到十字上？耦合太強，位元的能量會反過來漏進 XY 線，T₁ 變短。\n'
  '- 沒有 SQUID 可以嗎？可以。單一 JJ 就能提供非線性電感，只是頻率固定、不能調（固定頻率位元）。\n'
  '- Z 旋轉一定要靠 Z 線嗎？實務上多用虛擬 Z：軟體改後續脈衝的相位，約 0 ns。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路或帳號。

## `transmon-3d.html#chip`（第 1 章：晶片）

- 分頁「晶片總覽」：按鈕「送出 π 脈衝」、核取「顯示標籤」。十字板發金光代表 |1⟩，依 T₁ 衰減。
- 分頁「大十字電容的作用」：C_Σ 滑桿、電場線、手臂用途。

## `transmon-3d.html#control`（第 4 章：操控）

- 按鈕：X 軸 π、X 軸 π/2、Y 軸 π/2、持續驅動（Rabi 振盪）、重設 |0⟩；上方可切換「有 JJ（transmon）」與「沒有 JJ（線性 LC）」。
- 左邊能階梯：長條粗細代表佔據機率；驅動時 0–1 之間出現青色微波。

## `transmon-3d.html#case`（第 6 章：案例）

- 步驟 1–6：製程誤差、SQUID 調頻、頻率配置、XY 寫入、CZ 閘、自由實驗；「自動接續」會自動播下一步。
- 自由實驗：Q1／Q2／Q3 Φ 滑桿（0–0.3）、π → Q1／Q2／Q3、CZ（Q2–Q3）、回到配置、回到製程原貌、顯示 Q2 鄰居的禁區。
- 頻率尺：實線是 0→1、細線是 1→2、◆ 是雙光子；紅色帶代表碰撞（下一課的主題）。

## 操作

滑鼠拖曳旋轉、滾輪縮放；← → 切換章節。
''',
}

SHEET_HEADER = ['關卡／實驗', '操作', 'Φ / Φ₀', 'f₀₁（GHz）', '十字板有沒有亮', '我的觀察', '過關了嗎', '備註']
SHEET_ROWS = ([['第一關 認線', '送出 π 脈衝', '', '', '', '', '', ''],
               ['第二關 寫入', 'X 軸 π', '', '', '', '', '', ''],
               ['第二關 寫入', 'X 軸 π/2', '', '', '', '', '', ''],
               ['第二關 寫入', 'Y 軸 π/2', '', '', '', '', '', '']]
              + [['第三關 調頻', '拖 Q1 Φ', f'{p:.3f}', '', '', '', '', ''] for p in PHIS]
              + [['第三關 調頻', 'π → Q1', '', '', '', '', '', '']])

EXTRA_CSS = '''table.rec td{height:9mm}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.card{border:2pt solid #0b2540;border-radius:4mm;padding:5mm;margin-top:5mm}.card h3{margin-top:0}.draw{border:1.5pt dashed #0b2540;height:95mm;margin-top:4mm}'''


def html():
    pages = [
        '<h2>實驗紀錄：送脈衝和調磁通</h2><p class="lead">#control：比較 π、π/2 與不同軸；#case 步驟 6：拖 Q1 Φ、再按 π → Q1。</p>'
        '<table class="rec"><tr><th>操作</th><th>箭頭停在哪裡</th><th>能階梯哪一階變粗</th></tr>'
        + ''.join(f'<tr><td>{x}</td><td></td><td></td></tr>' for x in ('X 軸 π', 'X 軸 π/2', 'Y 軸 π/2')) + '</table>'
        '<table class="rec" style="margin-top:4mm"><tr><th>Q1 Φ / Φ₀</th><th>f₀₁（GHz）</th><th>十字板亮了嗎</th></tr>'
        + ''.join(f'<tr><td>{p:.3f}</td><td></td><td></td></tr>' for p in PHIS) + '<tr><td>按 π → Q1 之後</td><td></td><td></td></tr></table>',
        '<h2>闖關：爸爸出題、你過關</h2><p class="lead">每關說對才過關；答錯就回動畫再看一次。</p>'
        '<table class="rec"><tr><th>關卡</th><th>題目</th><th>我的答案</th><th>過關</th></tr>'
        '<tr><td>一</td><td>按送出脈衝時，哪一條線在工作？十字板為什麼發光？</td><td></td><td></td></tr>'
        '<tr><td>二</td><td>π 和 π/2 差在哪？X 軸和 Y 軸差在哪？</td><td></td><td></td></tr>'
        '<tr><td>三</td><td>拖 Z 線磁通，改變了什麼？沒改變什麼？</td><td></td><td></td></tr>'
        '<tr><td>四</td><td>為什麼 5.21 GHz 的微波不會把狀態推上 |2⟩？</td><td></td><td></td></tr>'
        '<tr><td>五</td><td>SQUID 的兩個身分是什麼？</td><td></td><td></td></tr></table>',
        '<h2>換你改造：XY／Z 線分工圖</h2><p class="lead">畫十字電容、SQUID、XY 驅動線、Z 磁通線、讀取共振腔。每條線旁寫：送什麼、電場還是磁場耦合、改狀態還是改頻率。</p>'
        '<div class="draw"></div>'
        '<p>從 |0⟩ 寫到 |1⟩ 靠：＿＿＿＿＿＿　把頻率從 5.21 GHz 調到約 4.4 GHz 靠：＿＿＿＿＿＿</p>'
        '<p>作品名稱：＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p class="note">生活技能：分清楚每個控制鈕的功能——你家裡哪個遙控器的按鈕最容易按錯？＿＿＿＿＿＿＿＿</p>',
        '<h2>說明卡與最後一關</h2><div class="box"><p>1. transmon 怎麼從 |0⟩ 寫成 |1⟩？</p><div class="line"></div>'
        '<p>2. 脈衝的面積、相位、頻率各管什麼？</p><div class="line"></div><p>3. SQUID 的兩個身分：</p><div class="line"></div>'
        '<p>4. 一個注意事項：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出寫入原理：從 |0⟩ 出發，XY 送 f₀₁ 脈衝轉動狀態</li><li>說出三個旋鈕：面積、相位、頻率</li>'
        '<li>說出為什麼只停在 |1⟩：1→2 低 283 MHz</li><li>指出注意事項：Z 線只改頻率，不會把 |0⟩ 變 |1⟩</li>'
        '<li>替分工圖取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q100 transmon 怎麼寫入狀態 列印包', '父子科技學院 量子電腦學程 Q100｜第 2 課：transmon 怎麼寫入狀態', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q100-transmon-write-xy-z', folder='Q100_transmon怎麼寫入狀態', files=FILES,
        sheet=('03_闖關與實驗紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_transmon寫入.pdf', pack_pages=4,
        pack_needles=('實驗紀錄', '闖關', '分工圖', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q100', episode_dir='specials/q100-transmon-write-xy-z',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'scenes': ['animations/transmon-3d.html#chip', 'animations/transmon-3d.html#control', 'animations/transmon-3d.html#case'],
               'q1FreqGHz': {f'{p:.3f}': f for p, f in TABLE}, 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q100/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')
