"""Q019 課堂教材：人肉晶格劇本與觀察紀錄、能隙示意圖（列印）、能量尺度卡、說明卡、解答、gap_scale.py、動畫導覽。

不需要帳號，也不需要安裝套件（gap_scale.py 只要 Python 3）；動畫用瀏覽器開啟 animations/index.html#cooper。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q019/classroom.py
"""
from pathlib import Path
import contextlib
import io
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

PROGRAM = '''"""父子科技學院 量子電腦學程 Q019：鋁的能隙有多大？——熱能、量子位元、能隙比一比。

不用安裝任何套件，只要 Python 3。執行：  python gap_scale.py
能隙用 BCS 理論的關係 Δ(0) ≈ 1.764 k_B T_c（維基百科 BCS theory），鋁的臨界溫度 T_c ≈ 1.2 K（學程簡報 p7）。
最後一段的配對比例用學程動畫 animations/index.html#cooper（js/scenes/02_cooper.js）裡的示意公式 1 − (T/T_c)⁴，不是真實材料的曲線。
"""
H = 6.62607015e-34    # 普朗克常數（J·s）
KB = 1.380649e-23     # 波茲曼常數（J/K）
E = 1.602176634e-19   # 基本電荷（C），用來把焦耳換成電子伏特

TC = 1.2              # 鋁的臨界溫度（K）
T_CHIP = 0.010        # 量子晶片工作溫度（K），約 10 mK
F_QUBIT = 5e9         # 量子位元頻率（Hz），約 5 GHz

gap = 2 * 1.764 * KB * TC          # 拆散一對需要的能量 2Δ（J）
GAP_GHZ = gap / H / 1e9
QUBIT_GHZ = F_QUBIT / 1e9
THERMAL_GHZ = KB * T_CHIP / H / 1e9

print(f'能隙 2Δ        ≈ {GAP_GHZ:6.1f} GHz（{gap / E * 1e6:.0f} μeV）')
print(f'量子位元 f01   ≈ {QUBIT_GHZ:6.1f} GHz（{H * F_QUBIT / E * 1e6:.0f} μeV）')
print(f'熱能 k_B T（10 mK）≈ {THERMAL_GHZ:6.2f} GHz（{KB * T_CHIP / E * 1e6:.2f} μeV）')
RATIO_GAP_QUBIT = GAP_GHZ / QUBIT_GHZ
RATIO_QUBIT_THERMAL = QUBIT_GHZ / THERMAL_GHZ
RATIO_TC_CHIP = TC / T_CHIP
print(f'能隙 ÷ 量子位元 ≈ {RATIO_GAP_QUBIT:.1f} 倍；量子位元 ÷ 熱能 ≈ {RATIO_QUBIT_THERMAL:.0f} 倍；臨界溫度 ÷ 晶片溫度 = {RATIO_TC_CHIP:.0f} 倍')
print('結論：微波（量子位元）和熱都跨不過能隙，拆不散電子對。')

print()
print('動畫的示意公式：配對比例 = 1 − (T / Tc)⁴（只在 T < Tc 時；10 對電子）')
TABLE = []
for t in (2.5, 1.2, 1.1, 1.0, 0.8, 0.6, 0.3):
    frac = 1 - (t / TC) ** 4 if t < TC else 0.0
    TABLE.append((t, round(frac * 100), round(frac * 10)))
    print(f'  T = {t:4.2f} K  配對比例 ≈ {frac * 100:3.0f} %  成對的有 {round(frac * 10):2d} 對')
'''

R = {}
with contextlib.redirect_stdout(io.StringIO()) as _out:
    exec(compile(PROGRAM, 'gap_scale.py', 'exec'), R)  # noqa: S102 — 實跑本檔附的程式
RUN_LOG = _out.getvalue()
# 製作代理實跑（Python 3）：與簡報 p8（88 GHz、5 GHz、0.2 GHz）、旁白（十幾倍、一百多倍）、動畫讀數相同
assert round(R['GAP_GHZ']) == 88 and round(R['THERMAL_GHZ'], 1) == 0.2
assert 10 < R['RATIO_GAP_QUBIT'] < 20 and round(R['RATIO_TC_CHIP']) == 120
assert [p for _, p, _ in R['TABLE']] == [0, 0, 29, 52, 80, 94, 100]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q019：Cooper pair 與能隙（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。這一堂接著上一堂的「電阻消失、磁鐵懸浮」往裡看：
電子明明互相排斥，為什麼在超導體裡會兩兩成對（Cooper pair，庫柏對）？成對以後，「能隙」又保護了什麼？

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 晶格扭曲、Cooper pair、能隙、能量尺度；看動畫裡的電子對 | 影片第 3–8 段、`05_動畫導覽.md` |
| 25–65 | 角色扮演：全家當人肉晶格，一人走過時大家靠近，讓第二個人被「吸」過來 | 列印包第 1 頁、`01_操作步驟.md` |
| 65–75 | 休息 | |
| 75–105 | 孩子畫能隙示意圖：有能隙和沒能隙時，小擾動造成的差別 | 列印包第 2、3 頁 |
| 105–115 | 孩子教爸爸：電子為什麼成對、能隙保護什麼 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、替示意圖取名字、存檔 | |

## 課前準備（約 20 分鐘）

- 客廳清出一塊空地（至少能站 3×3 個人的格子；人不夠可以用椅子、抱枕代替晶格原子）。
- 列印 `02_列印包_能隙.pdf`（A4，共 4 頁）；讀一遍 `04_解答.md`。
- 下載學程的 `animations/` 資料夾，用瀏覽器先點一次 `index.html#cooper`（見 `05_動畫導覽.md`）。
- 有電腦可以跑 Python 3 的話，執行一次 `gap_scale.py`（不需要安裝套件），看熱能、量子位元和能隙差多少。

## 驗收重點

1. 說得出晶格扭曲的四步：電子經過 → 正離子靠近 → 留下正電的尾巴 → 吸來第二顆電子。
2. 說得出能隙保護了什麼：拆散一對要一整筆能量，小擾動（晶格輕微振動、雜質、量子位元的微波、10 mK 的熱）跨不過，電子對不會被撞散，所以沒有電阻、幾乎不耗損能量。
3. 指出至少一個注意事項：這是簡化圖像；嚴格的 BCS 理論要到大學物理才會完整推導。

## 誠實說明

- 人肉晶格與「正電的尾巴」都是簡化圖像。真的電子對中的兩顆電子可能相隔好幾百奈米，中間穿插著許多別的電子對；角色扮演只演出「透過晶格互相吸引」這一件事。
- 能隙 88 GHz、量子位元 5 GHz、熱能 0.2 GHz 是學程簡報 p8 的鋁代表值；`gap_scale.py` 用 BCS 關係重算得到相同的數量級。
- 動畫裡配對比例隨溫度變化的曲線是示意公式，不是真實鋁的量測曲線。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：角色扮演——人肉晶格（約 40 分鐘）

1. 排晶格：家人（或椅子、抱枕）站成整齊的格子，每人之間隔一步，當帶正電的「正離子」。雙手放身側。
2. 第一顆電子：孩子當電子，從格子中間慢慢走過去。規則：電子走到你旁邊時，晶格原子往電子的方向靠近半步、伸出手（被負電吸過來）；
   電子走遠後，數到三再慢慢退回原位（尾巴不會馬上消失）。
3. 第二顆電子：爸爸當第二顆電子，跟在後面隔幾步走。規則：哪裡的晶格原子還靠得比較近（正電比較多），就往哪裡走——你會發現自己被「吸」進第一顆電子留下的通道。
4. 互換角色再演一次；這次讓兩顆電子從相反的方向出發，討論「兩顆電子沒有直接拉手，為什麼會被綁在一起」。
5. 加一個「小擾動」：有人輕輕推一下晶格原子（晶格振動）。先演「沒有能隙」：被推的地方電子就被撞歪、走散；
   再演「有能隙」：規定要一次推滿三下（一整筆能量）才能把兩顆電子分開，輕輕一推不算數——兩顆電子繼續一起走。
6. 在列印包第 1 頁記錄：誰當什麼、看到什麼、哪一步最難演。
7. 最後一起說一次注意事項：這是簡化圖像，真的電子對可能隔得很遠，詳細理論在大學物理。

## 下半場：孩子改造——能隙示意圖（約 30 分鐘）

1. 用列印包第 2 頁：左半邊畫「有能隙」，右半邊畫「沒能隙」。
2. 兩邊都畫同樣大小的小擾動箭頭（例如晶格的輕微振動）。有能隙的那邊畫一道高門檻，箭頭撞上去彈回來、電子對還在；沒能隙的那邊，箭頭直接把電子撞偏。
3. 用第 3 頁的能量尺度卡，在示意圖旁邊標出三個能量：熱能（10 mK）、量子位元的微波、能隙；看看誰跨得過門檻。
4. 替示意圖取名字，拿去考爸爸：「如果把冷凍機關掉、溫度回到室溫，圖會變成哪一邊？」
''',

'gap_scale.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n'
  '## 晶格扭曲四步\n\n'
  '1. 一顆電子跑過晶格。\n2. 帶正電的離子被它吸引，稍微靠向電子（晶格扭曲）。\n'
  '3. 那一小塊地方的正電變多，像電子留下的一條短暫尾巴；晶格的這種振動叫做聲子。\n'
  '4. 正電的尾巴吸引第二顆電子；在夠遠的距離上，這股吸引勝過兩顆電子的排斥，兩顆電子成對（Cooper pair）。\n\n'
  '## Cooper pair 的特徵\n\n'
  '- 兩顆電子自旋相反、動量（跑的方向）相反；一對帶兩倍電荷（2e）。\n'
  '- 兩顆可能相隔好幾百奈米，中間穿插著許多別的電子對。\n'
  '- 所有電子對進入同一個量子狀態，整塊超導體只需要一個相位 φ 描述（之後的約瑟夫森接面就是兩塊超導體的相位差）。\n\n'
  '## 能隙示意圖參考答案\n\n'
  '| | 有能隙（超導態） | 沒能隙（正常態） |\n|---|---|---|\n'
  '| 小擾動（晶格輕微振動、雜質） | 跨不過門檻，電子對不被撞散 | 直接把電子撞偏 |\n'
  '| 結果 | 電子對同步流動、零電阻 | 電子亂跑、有電阻，能量變成熱 |\n'
  '| 量子位元的微波（約 5 GHz） | 比能隙（約 88 GHz）小十幾倍，拆不散 | — |\n'
  '| 10 mK 的熱（約 0.2 GHz） | 遠小於能隙，拆不散 | — |\n\n'
  '## gap_scale.py 實跑輸出\n\n```\n' + RUN_LOG + '```\n\n'
  '## 暫停題：已經比臨界溫度低了，為什麼還要冷到 10 mK？\n\n'
  '- 學程簡報 p8 的答案：熱能要遠小於量子位元的能量（0.2 GHz ≪ 5 GHz），量子位元才能穩定待在 0，熱激發的機率極低。\n'
  '- 1.2 K 的熱能約 25 GHz，比 5 GHz 的量子位元還大；只冷到剛好超導，量子位元會一直被熱擾動。\n\n'
  '## 常見問題\n\n'
  '- 電子不是互相排斥嗎？是。成對靠的不是兩顆電子直接互相吸引，而是透過晶格：第一顆電子讓晶格扭曲，扭曲處的正電再吸引第二顆。\n'
  '- 成對的兩顆電子是黏在一起的嗎？不是，可能相隔好幾百奈米；人肉晶格只是簡化圖像。\n'
  '- 能隙是一個洞嗎？不是。「隙」指能量上的一段空隙：拆散一對至少要 2Δ 的能量，比這小的擾動沒有辦法把它拆開。\n'
  '- 動畫裡的配對比例曲線是真的嗎？是示意公式 1 − (T/Tc)⁴，讓「越冷配得越多」看得見，不是真實鋁的量測曲線。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路、伺服器或帳號。網址後面的 `#` 名稱可以直接跳到場景。

## `index.html#cooper`（JJ 與微波讀取 場景 2：超導體——Cooper pair 與零電阻）

- 金色小球是鋁的正離子晶格；藍色、紫色小球是電子，配對時用青色的線連成一對。
- 「超導態 0.3 K」：10 對電子一邊繞轉、一邊一起往右前進；晶格下面的字是「超導態：Cooper pair 同步流動，無散射」，面板寫「能隙 Δ 打開：小擾動無法散射 Cooper pair」。
- 「正常態 2.5 K」：連線消失，電子亂跑、常常突然轉向（被晶格振動散射）；字變成粉紅色「正常態：電子被晶格振動散射 → 有電阻」，面板寫「無能隙：電子與聲子碰撞 → 焦耳熱」。
- 「溫度 T (K)」滑桿：慢慢從 2.5 拉到 0.3，看面板的配對比例（1.0 K 約 52 %）和右下角電阻對溫度的小圖：低於 1.2 K 時電阻掉到零。
- 晶格扭曲在這個動畫裡畫得很小，主要看電子怎麼成對、怎麼一起走。

## 操作

`H` 隱藏面板；滑鼠拖曳旋轉、滾輪縮放；← → 切換場景（場景 3 是約瑟夫森接面，之後的課會用到）。
''',
}

SHEET_HEADER = ['回合', '晶格原子（誰）', '第一顆電子（誰）', '第二顆電子（誰）', '有沒有被吸過去', '小擾動：有能隙／沒能隙', '看到什麼', '最難演的地方']
SHEET_ROWS = [['第 1 回'], ['第 2 回（互換角色）'], ['第 3 回（相反方向）'], ['第 4 回（加小擾動）']]

EXTRA_CSS = '''table.rec td{height:22mm;font-size:10.5pt}table.rec th:first-child{width:30mm}
.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
table.demo td{font-size:10.5pt;height:auto}table.demo th:first-child{width:34mm}
.split{display:flex;gap:4mm;margin-top:3mm}.split .box{flex:1;height:120mm}'''


def html():
    rounds = ['第 1 回', '第 2 回（互換角色）', '第 3 回（相反方向）', '第 4 回（加小擾動）']
    pages = [
        '<h2>人肉晶格：劇本與觀察紀錄</h2><p class="lead">晶格原子：電子走到旁邊就靠近半步，電子走遠數到三再退回。第二顆電子：往晶格靠得近的地方走。</p>'
        '<p>日期：＿＿＿＿＿＿　參加的人：＿＿＿＿＿＿＿＿＿＿＿＿</p>'
        '<table class="rec"><tr><th>回合</th><th>誰當晶格？誰當電子？</th><th>第二顆有沒有被吸過去？</th><th>看到什麼</th></tr>'
        + ''.join(f'<tr><td>{r}</td><td></td><td></td><td></td></tr>' for r in rounds) + '</table>'
        '<div class="box" style="margin-top:3mm"><p>兩顆電子沒有直接拉手，為什麼會被綁在一起？</p><div class="line"></div>'
        '<p>注意事項：這是簡化圖像，真的電子對可能隔得很遠。</p></div>',
        '<h2>能隙示意圖</h2><p class="lead">左邊畫有能隙、右邊畫沒能隙；兩邊畫一樣大的小擾動箭頭，看看會怎樣。</p>'
        '<p>示意圖名稱：＿＿＿＿＿＿＿＿＿＿＿＿　畫的人：＿＿＿＿＿＿</p>'
        '<div class="split"><div class="box"><h3>有能隙（超導態）</h3></div><div class="box"><h3>沒能隙（正常態）</h3></div></div>'
        '<div class="box" style="margin-top:3mm"><p>我發現的差別：</p><div class="line"></div></div>',
        '<h2>能量尺度卡（鋁）</h2><p class="lead">用頻率比一比能量：誰跨得過能隙的門檻？</p>'
        '<table class="demo"><tr><th>能量</th><th>大約多少</th><th>跨得過能隙嗎？</th></tr>'
        '<tr><td>熱能（10 mK）</td><td>0.2 GHz</td><td></td></tr>'
        '<tr><td>量子位元的微波</td><td>5 GHz</td><td></td></tr>'
        '<tr><td>能隙 2Δ（拆散一對）</td><td>88 GHz</td><td>（門檻本身）</td></tr></table>'
        '<div class="box" style="margin-top:4mm"><h3>算一算</h3>'
        '<p>能隙 ÷ 量子位元 ≈ ＿＿＿ 倍　　量子位元 ÷ 熱能 ≈ ＿＿＿ 倍</p>'
        '<p>鋁的臨界溫度 1.2 K ÷ 晶片溫度 0.01 K = ＿＿＿ 倍</p></div>'
        '<div class="box" style="margin-top:4mm"><h3>晶格扭曲四步</h3>'
        '<p>① 電子經過　② 正離子靠近　③ 留下正電的尾巴（聲子）　④ 吸來第二顆電子</p>'
        '<p>成對以後：自旋相反、方向相反、電荷 2e；所有電子對進入同一個量子狀態。</p></div>',
        '<h2>說明卡：我的能隙示意圖</h2><div class="box"><p>示意圖名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. Cooper pair 與能隙在解決什麼？</p><div class="line"></div><p>2. 我怎麼做（怎麼演、怎麼畫）？</p><div class="line"></div>'
        '<p>3. 哪裡容易錯？</p><div class="line"></div><p>4. 真實的量子電腦哪裡會用到？</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出：電子互相排斥，為什麼會透過晶格成對</li><li>說出能隙保護了什麼</li>'
        '<li>比一比熱能、量子位元、能隙三個能量</li><li>說出為什麼晶片要冷到 10 mK</li>'
        '<li>指出一個注意事項：這是簡化圖像，BCS 理論要到大學物理才完整推導</li><li>替示意圖取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q019 能隙 列印包', '父子科技學院 量子電腦學程 Q019｜Cooper pair 與能隙', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q019-cooper-pair-gap', folder='Q019_Cooper_pair與能隙', files=FILES,
        sheet=('03_人肉晶格紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_能隙.pdf', pack_pages=4,
        pack_needles=('人肉晶格', '能隙示意圖', '能量尺度卡', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q019', episode_dir='specials/q019-cooper-pair-gap',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'none（gap_scale.py 只要 Python 3；動畫用瀏覽器）',
               'program': 'gap_scale.py',
               'recordedRun': {'gap_GHz': round(R['GAP_GHZ'], 1), 'qubit_GHz': R['QUBIT_GHZ'], 'thermal_10mK_GHz': round(R['THERMAL_GHZ'], 3),
                               'gap_over_qubit': round(R['RATIO_GAP_QUBIT'], 1), 'tc_over_chip': round(R['RATIO_TC_CHIP']),
                               'scene_pairing_percent': {str(t): p for t, p, _ in R['TABLE']}},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q019/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')
