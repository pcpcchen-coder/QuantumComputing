"""Q017 課堂教材：五條件檢核卡、五條件卡（列印）、生活二態系統改造、說明卡、解答、ladder_check.py、動畫導覽。

不需要帳號，也不需要安裝套件（ladder_check.py 只要 Python 3）；動畫用瀏覽器開啟 animations/index.html 與 atoms.html。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q017/classroom.py
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

PROGRAM = '''"""父子科技學院 量子電腦學程 Q017：樓梯等不等高？——LC 電路和約瑟夫森接面電路的能階。

不用安裝任何套件，只要 Python 3。執行：  python ladder_check.py
和學程動畫 animations/index.html#potential（js/scenes/04_potential.js）用同樣的數字與算法：
充電能 E_C = 0.25 GHz、E_J / E_C = 50，電荷基底 n = -14 … 14。
"""
import math

EC = 0.25            # 充電能（GHz）
EJ = 50 * EC         # 約瑟夫森能（GHz）
N = 14


def jacobi_eigenvalues(a, sweeps=60):
    """對稱矩陣的 Jacobi 對角化（只用標準函式庫），回傳由小到大的特徵值。"""
    n = len(a)
    a = [row[:] for row in a]
    for _ in range(sweeps):
        off = sum(a[i][j] ** 2 for i in range(n) for j in range(n) if i != j)
        if off < 1e-22:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if abs(a[p][q]) < 1e-15:
                    continue
                theta = (a[q][q] - a[p][p]) / (2 * a[p][q])
                t = (1 if theta >= 0 else -1) / (abs(theta) + math.sqrt(theta * theta + 1))
                c = 1 / math.sqrt(t * t + 1)
                s = t * c
                for k in range(n):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p], a[k][q] = c * akp - s * akq, s * akp + c * akq
                for k in range(n):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k], a[q][k] = c * apk - s * aqk, s * apk + c * aqk
    return sorted(a[i][i] for i in range(n))


# LC 電路（線性）：能階 E_n = ω(n + 1/2)，ω = √(8 E_J E_C)
w = math.sqrt(8 * EJ * EC)
LC = [w * (n + 0.5) for n in range(5)]
LC_GAPS = [LC[k + 1] - LC[k] for k in range(3)]
print('LC 電路（線性）    相鄰兩階的間距（GHz）：', [round(g, 3) for g in LC_GAPS])

# 約瑟夫森接面電路（transmon）：H = 4 E_C n² − (E_J / 2)(|n⟩⟨n+1| + h.c.)
dim = 2 * N + 1
H = [[0.0] * dim for _ in range(dim)]
for i in range(dim):
    n = i - N
    H[i][i] = 4 * EC * n * n
    if i + 1 < dim:
        H[i][i + 1] = H[i + 1][i] = -EJ / 2
E = jacobi_eigenvalues(H)
JJ_GAPS = [E[k + 1] - E[k] for k in range(3)]
ALPHA_MHZ = (JJ_GAPS[1] - JJ_GAPS[0]) * 1000
print('約瑟夫森接面（非線性）相鄰兩階的間距（GHz）：', [round(g, 3) for g in JJ_GAPS])
print(f'非諧性 = (1→2 間距) − (0→1 間距) = {ALPHA_MHZ:.0f} MHz；LC 電路是 {(LC_GAPS[1] - LC_GAPS[0]) * 1000:.0f} MHz')
print('結論：LC 電路每一階一樣高，微波會一路往上推；換成約瑟夫森接面，0→1 和 1→2 的頻率不同，微波就能只推 0 和 1。')
'''

R = {}
with contextlib.redirect_stdout(io.StringIO()) as _out:
    exec(compile(PROGRAM, 'ladder_check.py', 'exec'), R)  # noqa: S102 — 實跑本檔附的程式
RUN_LOG = _out.getvalue()
# 製作代理實跑（Python 3）：與 source-notes.md 的紀錄、動畫標籤相同
assert [round(g, 2) for g in R['LC_GAPS']] == [5.0, 5.0, 5.0]
assert [round(g, 2) for g in R['JJ_GAPS']] == [4.74, 4.45, 4.13]
assert round(R['ALPHA_MHZ']) == -287

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q017：為什麼要做「人造原子」（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。這一堂是第二階段「硬體怎麼做」的第一堂：量子位元需要一個可以控制的二態系統，
再用迪文森佐（DiVincenzo）五條件當檢查清單，逐條檢核一枚硬幣、一顆燈泡、一個原子和一顆 transmon（超導量子位元，也就是「人造原子」）。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 二態系統的三個要求、五條件；看動畫裡的離子和能階 | 影片第 3–8 段、列印包第 2 頁（五條件卡） |
| 25–65 | 冒險任務：孩子當檢核員、爸爸當考官，逐條檢核四位候選人 | 列印包第 1 頁、`03_五條件檢核卡.csv`、`01_操作步驟.md` |
| 65–75 | 休息 | |
| 75–105 | 孩子自己找一個生活中的二態系統，檢核它缺哪一條、要補什麼 | 列印包第 3 頁 |
| 105–115 | 孩子教爸爸：五條件是什麼、為什麼超導要做人造原子 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、替檢核卡取名字、存檔 | |

## 課前準備（約 20 分鐘）

- 列印 `02_列印包_人造原子.pdf`（A4，共 4 頁）；第 2 頁是「五條件卡」，可以剪下來當書籤。讀一遍 `04_解答.md`。
- 下載學程的 `animations/` 資料夾，用瀏覽器先點一次 `index.html#potential`、`atoms.html#ionqubit`、`atoms.html#compare`（見 `05_動畫導覽.md`）。
- 有電腦可以跑 Python 3 的話，執行一次 `ladder_check.py`（不需要安裝套件），看「樓梯等不等高」的數字。

## 考官的追問（驗收重點）

1. 「有兩個狀態」還不夠：還要能疊加、能初始化、能操控、能讀取，而且維持得夠久。
2. 每打一個勾都要說得出理由；說不出理由的勾先擦掉，查完再補。
3. 硬幣和燈泡的問題不在「兩個狀態」，而在它們不能疊加——它們是古典位元。

## 誠實說明

- 檢核卡上的數字（維持時間、閘時間、能做幾個閘）都是學程簡報與動畫標示的代表值，各實驗室差異很大。
- 「原子五條全過」指的是離子阱、中性原子等實驗平台已經分別做到五個條件；單一顆原子本身還不是一台量子電腦。
- 硬幣、燈泡的判定是本堂課的教學判斷：五條件要的是量子位元，古典的兩個狀態不算。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：冒險任務——五條件檢核（約 40 分鐘）

1. 孩子當檢核員、爸爸當考官。拿出列印包第 1 頁「五條件檢核卡」和第 2 頁「五條件卡」。
2. 依序檢核四位候選人：一枚硬幣 → 一顆燈泡 → 一個原子 → 一顆 transmon。每一格寫 ✓、✗ 或「不適用」，再寫一句理由。
3. 硬幣、燈泡可以真的拿在手上試：翻一翻、開一開，問自己「它能不能同時是兩種的組合（疊加）？」
4. 原子：開 `atoms.html#ionqubit`，依序按「① Doppler 冷卻」「② 光泵浦初始化 |0⟩」「④ 微波 π」「⑤ 偵測（螢光）」，對照第 2、4、5 條。
5. transmon：開 `index.html#potential`，按「LC 諧振子（線性）」和「JJ / Transmon（非線性）」比一比樓梯等不等高（第 1 條）；
   再開 `atoms.html#compare` 按「相干時間」，看它在量子狀態消失前能做幾個閘（第 3 條）。
6. 考官每看到一個勾就追問「真的嗎？為什麼？」；說不出理由就先擦掉。四位都檢核完，對照 `04_解答.md`。

## 下半場：孩子改造——生活裡的二態系統（約 30 分鐘）

1. 在家裡或路上找一個「二態系統」：電燈開關、紅綠燈的紅和綠、門的開和關、手機的靜音開關……
2. 用列印包第 3 頁逐條檢核，五條都問一次，特別注意「能不能疊加」「能不能維持夠久」。
3. 寫下它缺哪一條（可能不只一條），再想：如果真要把它變成量子位元，要補上什麼？
4. 拿去考爸爸：讓爸爸檢核同一個東西，看兩個人的答案哪裡不一樣，討論到有共識。
''',

'ladder_check.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n'
  '## 五條件檢核卡參考答案\n\n'
  '| 條件 | 一枚硬幣 | 一顆燈泡 | 一個原子（離子、中性原子） | 一顆 transmon（人造原子） |\n|---|---|---|---|---|\n'
  '| ① 定義清楚、可擴充的量子位元 | ✗ 正反兩面，但不能疊加（古典位元） | ✗ 亮暗兩種，但不能疊加 | ✓ 挑兩個超精細能階（例：鐿-171 離子相差 12.6 GHz）；陣列可放大 | ✓ 約瑟夫森接面讓能階不等距，只挑 0 和 1；晶片製程大量製作 |\n'
  '| ② 能初始化成 0 | ✓ 放成正面（古典） | ✓ 關掉（古典） | ✓ 雷射冷卻＋光泵浦，> 99.9% | ✓ 在約 10 mK 的冷凍機裡待在 0；讀完可重設，最快幾 μs |\n'
  '| ③ 維持得比一個閘久很多 | 不適用（沒有量子狀態） | 不適用 | ✓ T₂ 約 1 秒到更久；離子約可做 10⁴ 個閘以上 | ✓ 但較短：T₂ 約 0.1 ms，閘約 50 ns，約 2000 個閘 |\n'
  '| ④ 能做量子閘 | ✗ 只能翻面，轉不到疊加 | ✗ 只有開和關 | ✓ 微波或雷射；雙位元靠共用振動或芮德堡態 | ✓ 微波脈衝（奈秒級） |\n'
  '| ⑤ 能讀出每一顆 | ✓ 看一眼（古典） | ✓ 看一眼（古典） | ✓ 狀態相依螢光：1 亮、0 暗 | ✓ 色散微波讀取（微秒級） |\n'
  '| 結論 | 古典位元，卡在第 1 條 | 古典位元，卡在第 1 條 | 五條全過；代價：要用電場或雷射一顆顆抓住、大量雷射 | 五條全過；代價：要冷到 10 mK、維持時間較短、每顆有製程差異 |\n\n'
  '## ladder_check.py 實跑輸出\n\n```\n' + RUN_LOG + '```\n\n'
  '## 暫停題：超導量子位元和原子各贏在哪裡？\n\n'
  '- 原子贏在：每一顆完全相同（大自然保證）、量子狀態維持得久。\n'
  '- 超導贏在：做在晶片上、不用一顆顆抓住、閘很快（奈秒級），可以用晶片製程大量製作。\n'
  '- 這就是為什麼兩種路線都有人做：沒有一種在五條件上全面領先。\n\n'
  '## 常見問題\n\n'
  '- 旋轉中的硬幣不就是一半正、一半反嗎？不是。它在每一刻都有確定的朝向，只是我們還不知道；疊加是量子狀態本身就是 0 和 1 的組合，之後還能干涉。\n'
  '- 為什麼不直接用 LC 電路？它的能階等間距，送進去的微波會同時把 0 推到 1、1 推到 2，沒辦法只操作兩個能階（`ladder_check.py` 的非諧性是 0）。\n'
  '- 「人造原子」是什麼意思？用鋁和約瑟夫森接面做出的電路，能階不等距、看起來像原子的能階，所以可以挑兩階當 0 和 1。\n'
  '- 動畫的數字是真機的數字嗎？是代表值：簡報和動畫都標明各家差異很大。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路、伺服器或帳號。網址後面的 `#` 名稱可以直接跳到場景。

## `index.html#potential`（JJ 與微波讀取 場景 4：非線性——從 LC 諧振子到 Transmon）

- 「LC 諧振子（線性）」：拋物線山谷、能階等間距；右邊金色標籤三個都是 5.00 GHz，面板寫「非諧性 0 MHz（等間距 → 無法單獨定址）」。
- 「JJ / Transmon（非線性）」：餘弦形狀的山谷，間距 4.74、4.45、4.13 GHz，非諧性約 −287 MHz。
- 「E_J / E_C」滑桿和「CPB」「10」「Transmon：50」按鈕可以改比值；右下小圖是能階對背景電荷的敏感度。

## `atoms.html#ionqubit`（離子阱 場景 3：離子量子位元）

- 依序按「① Doppler 冷卻」「② 光泵浦初始化 |0⟩」「③ 微波 π/2」或「④ 微波 π」「⑤ 偵測（螢光）」。
- 右邊布洛赫球顯示狀態；偵測時 1 會發亮、0 是暗的，面板寫出數到幾個光子、判為 0 或 1。「一次跑 1000 shots」畫出光子數直方圖。

## `atoms.html#compare`（場景 13：三平台比較）

- 超導（左）、離子阱（中）、中性原子（右）。按「相干時間」看量子狀態消失前大約能做幾個閘；也可以按「閘速度」「連接性」「規模」。

## 操作

`H` 隱藏面板；滑鼠拖曳旋轉、滾輪縮放；← → 切換場景。
''',
}

SHEET_HEADER = ['條件', '一枚硬幣', '理由', '一顆燈泡', '理由', '一個原子', '理由', '一顆 transmon', '理由', '我的生活二態系統', '理由']
SHEET_ROWS = [['① 定義清楚、可擴充的量子位元（能疊加的兩個狀態）'], ['② 能初始化成 0'], ['③ 維持得比一個閘久很多'],
              ['④ 能做量子閘'], ['⑤ 能讀出每一顆'], ['結論：缺哪一條？代價是什麼？']]

EXTRA_CSS = '''table.rec td{height:24mm;font-size:10.5pt}table.rec th:first-child{width:30mm}
.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
table.demo td{font-size:10.5pt;height:auto}table.demo th:first-child{width:34mm}'''

CONDS = ['① 定義清楚、可擴充的量子位元', '② 能初始化成 0', '③ 維持得比一個閘久很多', '④ 能做量子閘', '⑤ 能讀出每一顆']


def html():
    rows = ''.join(f'<tr><td>{c}</td><td></td><td></td><td></td><td></td></tr>' for c in CONDS)
    pages = [
        '<h2>五條件檢核卡</h2><p class="lead">每一格寫 ✓、✗ 或「不適用」，再寫一句理由。說不出理由的勾，考官可以擦掉。</p>'
        '<p>檢核員：＿＿＿＿＿＿　考官：＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<table class="rec"><tr><th>條件</th><th>一枚硬幣</th><th>一顆燈泡</th><th>一個原子</th><th>一顆 transmon</th></tr>'
        + rows + '<tr><td>結論：缺哪一條？代價？</td><td></td><td></td><td></td><td></td></tr></table>',
        '<h2>五條件卡</h2><p class="lead">迪文森佐（DiVincenzo）整理的量子電腦條件：五條都要有，才算合格。</p>'
        '<div class="box"><h3>先找一個二態系統</h3><p>兩個清楚的基本狀態（當作 0 和 1）・可以疊加・能控制。有兩個狀態還不夠！</p></div>'
        '<table class="demo" style="margin-top:4mm"><tr><th>條件</th><th>白話</th><th>考官會問</th></tr>'
        '<tr><td>① 定義清楚、可擴充</td><td>有能疊加的兩個狀態，而且能做很多顆</td><td>它能同時是 0 和 1 的組合嗎？</td></tr>'
        '<tr><td>② 能初始化</td><td>每次開始前都能放回 0</td><td>你怎麼確定它從 0 開始？</td></tr>'
        '<tr><td>③ 維持得夠久</td><td>量子狀態維持的時間，比做一個閘久很多</td><td>狀態消失前能做幾個閘？</td></tr>'
        '<tr><td>④ 能做量子閘</td><td>想轉多少就轉多少，兩顆之間也能互相影響</td><td>用什麼工具轉它？</td></tr>'
        '<tr><td>⑤ 能讀出每一顆</td><td>能單獨讀出每一顆是 0 還是 1</td><td>怎麼看出結果？</td></tr></table>'
        '<div class="box" style="margin-top:4mm"><h3>人造原子 vs 真的原子</h3>'
        '<p>真的原子：每一顆都一樣、維持得久；但太小，要用電場或雷射一顆顆抓住。</p>'
        '<p>人造原子（transmon）：做在晶片上、閘很快；把電感換成約瑟夫森接面，能階不等距，才能只挑 0 和 1；要冷到 10 mK。</p></div>',
        '<h2>換你改造：生活裡的二態系統</h2><p class="lead">找一個生活中的二態系統，用五條件逐條檢核，寫出它缺哪一條。</p>'
        '<div class="box"><p>我找到的二態系統：＿＿＿＿＿＿＿＿　它的兩個狀態：＿＿＿＿＿＿ 和 ＿＿＿＿＿＿</p></div>'
        '<table class="rec" style="margin-top:3mm"><tr><th>條件</th><th>✓ / ✗ / 不適用</th><th>理由</th></tr>'
        + ''.join(f'<tr><td>{c}</td><td></td><td></td></tr>' for c in CONDS) + '</table>'
        '<div class="box" style="margin-top:3mm"><p>它缺哪一條：</p><div class="line"></div>'
        '<p>如果真要把它變成量子位元，要補上什麼：</p><div class="line"></div></div>',
        '<h2>說明卡：我的五條件檢核卡</h2><div class="box"><p>檢核卡名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 為什麼要做「人造原子」？它在解決什麼？</p><div class="line"></div><p>2. 我怎麼做（怎麼檢核）？</p><div class="line"></div>'
        '<p>3. 哪裡容易錯？</p><div class="line"></div><p>4. 真實的量子電腦哪裡會用到？</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出：量子位元為什麼需要可以控制的二態系統</li><li>說出五個條件</li>'
        '<li>說出硬幣和燈泡卡在哪一條、為什麼</li><li>說出為什麼要把電感換成約瑟夫森接面</li>'
        '<li>指出一個注意事項：有兩個狀態還不夠，還要能初始化、操控、讀取並維持夠久</li><li>替檢核卡取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q017 人造原子 列印包', '父子科技學院 量子電腦學程 Q017｜為什麼要做「人造原子」', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q017-artificial-atom', folder='Q017_為什麼要做人造原子', files=FILES,
        sheet=('03_五條件檢核卡.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_人造原子.pdf', pack_pages=4,
        pack_needles=('五條件檢核卡', '五條件卡', '換你改造', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q017', episode_dir='specials/q017-artificial-atom',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'none（ladder_check.py 只要 Python 3；動畫用瀏覽器）',
               'program': 'ladder_check.py',
               'recordedRun': {'lc_gaps_GHz': [round(g, 3) for g in R['LC_GAPS']], 'jj_gaps_GHz': [round(g, 3) for g in R['JJ_GAPS']],
                               'anharmonicity_MHz': round(R['ALPHA_MHZ'])},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q017/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')
