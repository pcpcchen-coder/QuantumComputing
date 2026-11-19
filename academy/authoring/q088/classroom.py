"""Q088 課堂教材：量子化學與材料 — H₂ 能量表、先猜再算紀錄、單參數變分掃描、規模估計、說明卡與解答。

免安裝、不需帳號：能量表已預先算好（課綱的「新簡報＋notebook」尚未存在）；動畫只用學程的 animations/operation.html#register。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q088/classroom.py
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

# 製作代理以最小基底 STO-3G（ζ=1.24，解析高斯積分）自行計算的 H₂ 能量（單位：哈特里 Ha，含原子核排斥）
# (原子核距離 Å, Hartree–Fock, 完整計算 FCI 2×2)
CURVE = [(0.3, -0.594, -0.602), (0.4, -0.904, -0.914), (0.5, -1.043, -1.055), (0.6, -1.101, -1.116),
         (0.7, -1.117, -1.136), (0.74, -1.117, -1.137), (0.8, -1.111, -1.134), (0.9, -1.092, -1.121),
         (1.0, -1.066, -1.101), (1.2, -1.005, -1.057), (1.5, -0.911, -0.998), (2.0, -0.784, -0.949),
         (2.5, -0.703, -0.936), (3.0, -0.656, -0.934)]
R_MIN, E_MIN, E_FAR = 0.735, -1.1373, -0.9332          # 最低點與拉到很遠（兩個氫原子）的能量
HA_KJMOL = 2625.5
DEPTH_KJ = round((E_FAR - E_MIN) * HA_KJMOL)            # ≈ 536（簡化模型）
WIKI_KJ = 435.7                                         # 維基百科 Hydrogen：鍵解離能
assert min(CURVE, key=lambda r: r[2])[0] == 0.74 and DEPTH_KJ == 536

# 0.74 Å 的單參數試探態 cosθ|雙佔成鍵⟩ − sinθ|雙佔反鍵⟩：E(θ) = cos²θ·E1 + sin²θ·E2 − 2·sinθ·cosθ·K + 1/R
E1, E2, K, NN = -1.83186, -0.25249, 0.18121, 0.71510


def e_theta(deg):
    t = math.radians(deg)
    return round(math.cos(t) ** 2 * E1 + math.sin(t) ** 2 * E2 - 2 * math.sin(t) * math.cos(t) * K + NN, 4)


SCAN = [(d, e_theta(d)) for d in (0, 5, 10, 15, 20, 30)]
THETA_BEST = round(math.degrees(0.5 * math.atan2(2 * K, E2 - E1)), 1)   # ≈ 6.5°
assert SCAN[0][1] == -1.1168 and abs(e_theta(THETA_BEST) - E_MIN) < 2e-4

FILES = {
'00_爸爸先讀.md': f'''# 父子科技學院 量子電腦學程 Q088：量子化學與材料（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶出兩個問題：為什麼模擬分子適合量子電腦？H₂ 的能量曲線怎麼算？

課綱列的「新簡報＋notebook」還沒有做好，所以今天的「模擬器」用教材附的能量表代替：這張表是用最小基底（STO-3G）把 H₂ 在每個距離的 2×2 問題直接算出來的。只需要紙筆、方格紙、瀏覽器。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 為什麼分子難算、變分迴圈四步、曲線怎麼算 | 影片第 3–7 段、`operation.html#register` |
| 25–65 | 先猜曲線、再描點畫出 H₂ 能量曲線；單參數變分掃描 | 列印包第 1–2 頁、`03_能量與估計紀錄.csv` |
| 65–75 | 休息 | |
| 75–105 | 查一個真實的材料或藥物題目，估計要多大的量子電腦 | 列印包第 3 頁 |
| 105–115 | 孩子教爸爸：為什麼適合、曲線怎麼算 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 誠實說明

- 能量表是簡化模型（最小基底）的結果：最低點約 {R_MIN} Å；它算出的井深約 {DEPTH_KJ} kJ/mol，比維基百科的實際鍵解離能 {WIKI_KJ} kJ/mol 大。模型越簡單，數字越不準——這本身就是一個「注意事項」。
- 像 H₂ 這樣的小分子，古典電腦早就算得很準；量子優勢只可能在大型、強關聯的系統出現，目前化學上還沒有確立的量子優勢。
- 「工業級分子需數百萬實體位元等級」取自學程簡報第 44 頁，是會隨技術進展變動的估計。
''',

'01_操作步驟.md': f'''# 操作步驟

## A. 看那道牆（`operation.html#register`，約 5 分鐘）

1. 把「量子位元數 n」從 1 拉到 4，柱子從 2 根變 16 根；按「均勻疊加 H⊗ⁿ」。
2. 看右下插圖：30 個位元 16 GB、40 個 16 TB、50 個 18 PB，紅色虛線是頂級超級電腦的總記憶體。

## B. 先猜再算（約 20 分鐘）

1. 在列印包第 1 頁的方格上，先用鉛筆畫出你猜的曲線，標出你猜的最低點。
2. 用列印包附的表，把「完整計算」那一欄一個點一個點描上去，用另一種顏色連起來。
3. 再用第三種顏色描「最簡單近似（HF）」那一欄。拉遠的時候，兩條線差多少？

## C. 單參數變分掃描（約 15 分鐘）

在 0.74 Å，試探狀態只有一個角度 θ。照列印包第 2 頁的表，找出能量最低的 θ（提示：在 0° 和 15° 之間）。這就是上一堂變分演算法的「古典電腦調參數」。

## D. 下半場：估規模（約 30 分鐘）

挑一個題目（新材料、催化劑、高溫超導、固氮酶活性中心……），查它大概需要多少量子位元，和現在的機器（數十～上千實體位元）比一比。
''',

'04_解答.md': '# 解答（爸爸用）\n\n## H₂ 能量表（最小基底，單位 Ha）\n\n'
  '| 距離（Å） | 最簡單近似 HF | 完整計算 |\n|---|---|---|\n'
  + ''.join(f'| {r} | {h} | {f} |\n' for r, h, f in CURVE)
  + f'\n- 最低點約 {R_MIN} Å，能量約 {E_MIN} Ha。\n- 拉到很遠（兩個氫原子）約 {E_FAR} Ha；井深約 {E_FAR - E_MIN:.3f} Ha ≈ {DEPTH_KJ} kJ/mol（簡化模型；維基百科實際值 {WIKI_KJ} kJ/mol）。\n'
  '- 拉遠時 HF 一路往上（3 Å 差了約 0.28 Ha），因為它把兩個電子綁在同一個軌域裡；完整計算讓兩個電子一起考慮，曲線才會變平。\n\n'
  '## 單參數變分掃描（0.74 Å）\n\n| θ | 能量（Ha） |\n|---|---|\n'
  + ''.join(f'| {d}° | {e} |\n' for d, e in SCAN)
  + f'\n最低在 θ ≈ {THETA_BEST}°，能量 ≈ {E_MIN} Ha，等於完整計算的答案；θ = 0° 就是 HF。\n\n'
  '## 規模估計範例\n\n- 工業級分子：數百萬實體位元等級（簡報第 44 頁）。\n- 現在：數十～上千實體位元（簡報第 51 頁）。\n- 一千 → 一百萬：差一千倍；還要佈線、低溫電子、即時解碼（簡報第 51 頁）。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路或帳號。學程目前沒有分子或化學專用場景。

## `operation.html#register`（操作場景 4：多位元與糾纏）

- 滑桿「量子位元數 n」：1–4，下方柱子是 2ⁿ 個振幅（高度＝機率，金＝正相位、藍＝負相位）。
- 按鈕：均勻疊加 H⊗ⁿ、Bell 態、GHZ 態、測量全部、重設 |0…0⟩。
- 右下插圖：精確模擬 n 個量子位元所需記憶體（2ⁿ × 16 bytes）。

## 操作

`H` 隱藏面板；滑鼠拖曳旋轉、滾輪縮放。
''',
}

SHEET_HEADER = ['項目', '距離（Å）', '我猜的能量', '完整計算（Ha）', 'HF（Ha）', 'θ（度）', '變分能量（Ha）', '題目', '需要位元數', '備註']
SHEET_ROWS = ([['能量曲線', str(r), '', '', '', '', '', '', '', ''] for r, *_ in CURVE]
              + [['變分掃描', '0.74', '', '', '', str(d), '', '', '', ''] for d, _ in SCAN]
              + [['規模估計', '', '', '', '', '', '', '', '', ''] for _ in range(3)])

EXTRA_CSS = '''table.rec td{height:7mm}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.card{border:2pt solid #0b2540;border-radius:4mm;padding:4mm;margin-top:4mm}.card h3{margin-top:0}
.grid{height:80mm;border:1pt solid #888;background-image:linear-gradient(#ddd 1px,transparent 1px),linear-gradient(90deg,#ddd 1px,transparent 1px);background-size:5mm 5mm}'''


def html():
    pages = [
        '<h2>科學實驗：H₂ 能量曲線</h2><p class="lead">先用鉛筆畫你猜的曲線，再描「完整計算」，最後描「HF」。橫軸：距離 0–3 Å；縱軸：能量 −1.2 到 −0.5 Ha。</p>'
        '<div class="grid"></div>'
        '<table class="rec"><tr><th>距離（Å）</th>' + ''.join(f'<td>{r}</td>' for r, *_ in CURVE[::2]) + '</tr>'
        '<tr><th>完整計算</th>' + ''.join(f'<td>{f}</td>' for *_, f in CURVE[::2]) + '</tr>'
        '<tr><th>HF</th>' + ''.join(f'<td>{h}</td>' for _, h, _f in CURVE[::2]) + '</tr></table>'
        '<p class="note">完整表格見 04_解答.md／CSV。我猜的最低點：＿＿＿ Å　算出的最低點：＿＿＿ Å</p>',
        '<h2>變分迴圈：只調一個角度</h2><p class="lead">在 0.74 Å，試探狀態只有一個角度 θ。把能量填進表格，找出最低的 θ。</p>'
        '<table class="rec"><tr><th>θ</th><th>能量（Ha）</th><th>比上一個高還是低</th></tr>'
        + ''.join(f'<tr><td>{d}°</td><td></td><td></td></tr>' for d, _ in SCAN) + '</table>'
        '<div class="card"><h3>H₂ 能量曲線（今天的作品）</h3><p>最低點：＿＿＿ Å　斷成兩個原子的平台：約＿＿＿ Ha</p>'
        '<p>我猜錯的地方和原因：</p><div class="line"></div><div class="line"></div><p>作品名稱：＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p></div>',
        '<h2>換你改造：它要多大的量子電腦</h2><p class="lead">挑一個真實的材料或藥物題目，和現在的機器比一比。</p>'
        '<table class="rec"><tr><th>題目</th><th>為什麼難算</th><th>估計需要的實體位元</th><th>和一千個位元差幾倍</th></tr>'
        + '<tr><td></td><td></td><td></td><td></td></tr>' * 3 + '</table>'
        '<p>參考：工業級分子約數百萬實體位元等級（簡報第 44 頁）；現在的機器約數十～上千實體位元（第 51 頁）。</p>'
        '<p>要先解決哪些工程問題？＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p>'
        '<p class="note">生活技能：從簡單案例理解大問題——先把 H₂ 算懂，才知道大分子難在哪裡。</p>',
        '<h2>說明卡與最後一關</h2><div class="box"><p>1. 為什麼模擬分子適合量子電腦？</p><div class="line"></div>'
        '<p>2. H₂ 的能量曲線怎麼算？</p><div class="line"></div><p>3. 曲線的最低點和平台代表什麼？</p><div class="line"></div>'
        '<p>4. 一個限制或注意事項：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出：用量子模擬量子，位元數隨軌域成比例</li><li>說出曲線怎麼算：固定距離、找最低能量、換距離重複</li>'
        '<li>說出拉遠時最簡單近似為什麼不準</li><li>指出一個限制：小分子古典就算得準，量子優勢要在大型強關聯系統才可能出現</li>'
        '<li>替能量曲線圖取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q088 量子化學與材料 列印包', '父子科技學院 量子電腦學程 Q088｜量子化學與材料', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q088-quantum-chemistry-materials', folder='Q088_量子化學與材料', files=FILES,
        sheet=('03_能量與估計紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_量子化學與材料.pdf', pack_pages=4,
        pack_needles=('H₂ 能量曲線', '變分迴圈', '多大的量子電腦', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q088', episode_dir='specials/q088-quantum-chemistry-materials',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'scenes': ['animations/operation.html#register'],
               'h2CurveHa': [list(r) for r in CURVE], 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q088/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')
