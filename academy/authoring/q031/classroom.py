"""Q031 課堂教材：嫌犯卡模板、雜訊來源關係圖、量測實驗設計單、說明卡（列印）、解答、suspect_check.py、動畫導覽。

不需要帳號，也不需要安裝套件（suspect_check.py 只要 Python 3）；動畫用瀏覽器開啟 animations/index.html#bloch。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q031/classroom.py
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

PROGRAM = '''"""父子科技學院 量子電腦學程 Q031：退相干偵探小工具（和動畫 index.html#bloch 同一套公式）。

不用安裝任何套件，只要 Python 3。執行：  python suspect_check.py
- 一、鐵律檢查：T2 不會大於 2*T1；超過就先懷疑量測或計算。
- 二、從證據配對嫌犯（學程簡報 JJ_Microwave_Readout_Talk p24 的整理）。
- 三、動畫的衰減曲線：T1 模式 P(1) = e^(-t/5)；Ramsey 模式 |r| = e^(-t/6)、P(1) 固定 0.5
  （animations/js/scenes/01_bloch.js 第 50、80–84 行；時間是動畫的相對單位）。
"""
import math

SUSPECTS = {
    'TLS 二能階缺陷': ('T1 變短（還會讓頻率漂移）', '表面處理、Ta/Nb 電容板、藍寶石或高電阻率矽基板、加大電容板間距'),
    '準粒子（紅外線、宇宙射線）': ('T1 變短', '紅外屏蔽、濾波器、準粒子陷阱'),
    '磁通雜訊': ('T2 變短（可調頻量子位元）', '停在甜蜜點、不對稱 SQUID、磁屏蔽'),
    '讀取腔熱光子': ('T2 變短', '輸入線衰減器、良好接地與封裝'),
    'Purcell 效應': ('T1 變短（能量經讀取腔漏出）', 'Purcell 濾波器'),
}


def believable(t1, t2):
    """T2 <= 2*T1 才可信。"""
    return t2 <= 2 * t1


def suspects_for(t1_short, t2_short):
    if t1_short:
        return [k for k, v in SUSPECTS.items() if v[0].startswith('T1')]
    if t2_short:
        return [k for k, v in SUSPECTS.items() if v[0].startswith('T2')]
    return []


print('一、鐵律檢查（單位：微秒）')
CASES = [(50, 80), (50, 100), (50, 150), (100, 120)]
CHECK = {}
for t1, t2 in CASES:
    ok = believable(t1, t2)
    CHECK[(t1, t2)] = ok
    print(f'  T1 = {t1:3d}、T2 = {t2:3d}：2*T1 = {2 * t1:3d} → ' + ('可信' if ok else '不可能，先懷疑量測或計算'))

print()
print('二、從證據配對嫌犯')
for label, a, b in (('T1 變短', True, False), ('T1 沒變、只有 T2 變短', False, True)):
    print(f'  {label}：' + '、'.join(suspects_for(a, b)))
print('  嫌犯檔案：')
for k, (ev, fix) in SUSPECTS.items():
    print(f'    {k}｜證據：{ev}｜對策：{fix}')

print()
print('三、動畫 index.html#bloch 的衰減（相對單位，T1 = 5、T2 = 6）')
CURVE = {}
for t in (0, 2, 3.47, 5, 8, 12):
    p1 = math.exp(-t / 5)
    r = math.exp(-t / 6)
    CURVE[t] = (p1, 1 - 2 * p1, r)
    print(f'  t = {t:5.2f}：T1 模式 P(1) = {p1:.2f}、z = {1 - 2 * p1:+.2f}｜Ramsey 模式 |r| = {r:.2f}、P(1) = 0.50')
print('  T1 模式在 t = 5 ln2 ≈ 3.47 時箭頭經過球心；12 時重來一次')
'''

R = {}
with contextlib.redirect_stdout(io.StringIO()) as _out:
    exec(compile(PROGRAM, 'suspect_check.py', 'exec'), R)  # noqa: S102 — 實跑本檔附的程式
RUN_LOG = _out.getvalue()
# 製作代理實跑（Python 3）：與旁白、動畫段、01_bloch.js 公式相同
assert R['CHECK'][(50, 150)] is False and R['CHECK'][(50, 100)] is True
assert abs(R['CURVE'][3.47][1]) < 0.01 and round(R['CURVE'][12][1], 2) == 0.82 and round(R['CURVE'][12][2], 2) == 0.14
assert R['suspects_for'](True, False) == ['TLS 二能階缺陷', '準粒子（紅外線、宇宙射線）', 'Purcell 效應']
assert R['suspects_for'](False, True) == ['磁通雜訊', '讀取腔熱光子']

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q031：退相干：敵人在哪裡（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。這一堂用「偵探辦案」認識超導量子位元的退相干來源：
兩個證據是 T₁（能量弛豫時間）和 T₂（相位相干時間）；四個嫌犯是 TLS 二能階缺陷、準粒子（紅外線、宇宙射線打散庫柏對）、磁通雜訊、
讀取腔的熱光子與 Purcell 效應。看哪一個時間變短，就能縮小嫌犯範圍，再配上對策。下一堂 Q032 是模組發表：設計我的 transmon。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 兩個證據、四個嫌犯、線索配對、T₂ ≤ 2T₁；看 3D 動畫 | 影片第 3–8 段、`05_動畫導覽.md` |
| 25–65 | 做四張嫌犯卡，依證據配對對策，貼成雜訊來源關係圖 | 列印包第 1、2 頁、`01_操作步驟.md` |
| 65–75 | 休息 | |
| 75–105 | 孩子改造：替一個嫌犯設計量測實驗 | 列印包第 3 頁 |
| 105–115 | 孩子教爸爸：操作與原理 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、替關係圖取名字、存檔 | |

## 課前準備（約 20 分鐘）

- 列印 `02_列印包_嫌犯卡.pdf`（A4，共 4 頁）；第 1 頁的四張嫌犯卡可以剪開。另備一張大紙（A3 或海報紙）、膠帶、彩色筆。
- 讀一遍 `04_解答.md`。
- 下載學程的 `animations/` 資料夾，用瀏覽器先點一次 `index.html#bloch`（見 `05_動畫導覽.md`）。
- 有電腦可以跑 Python 3 的話，執行一次 `suspect_check.py`（不需要安裝套件）。

## 驗收重點

1. 完成「雜訊來源關係圖」：四個嫌犯、兩個證據（T₁、T₂）、對策都在圖上，用箭頭連起來。
2. 不看稿說出核心原理：T₁ 是 |1⟩ 掉回 |0⟩ 的時間；T₂ 是疊加相位能保持多久；T₁ 變短先懷疑 TLS、準粒子、Purcell，只有 T₂ 變短先查磁通雜訊與熱光子。
3. 指出至少一個注意事項：T₂ 永遠不會大於 2T₁；看到這種數據要先懷疑量測。

## 誠實說明

- 嫌犯與對策取自學程簡報 p24 的整理，不是所有退相干來源（例如電荷雜訊只在 p6 帶過），也不代表哪個嫌犯在某顆晶片上最嚴重。
- 量測實驗是「設計」：家裡沒有量子位元可以量，作品寫的是步驟、要改的條件和預期結果，不要編造量測數據。
- 動畫的 T₁、T₂ 是相對單位，畫面把時間放慢了；真實最好的 transmon，T₁ 約 0.1–1 ms（簡報 p6）。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：嫌犯卡與關係圖（約 40 分鐘）

1. 剪開列印包第 1 頁的四張嫌犯卡：TLS 二能階缺陷、準粒子、磁通雜訊、讀取腔熱光子（Purcell 效應寫在熱光子卡的背面當「共犯」）。
2. 爸爸念影片第 4–7 段的線索，孩子在卡片正面填：躲在哪裡、做了什麼、留下的證據（只能寫「T₁ 變短」或「T₂ 變短」）。
3. 卡片背面寫對策，並寫一句「怎麼確認是它」。
4. 在大紙中間畫兩個圓：「證據 T₁ 變短」「證據 T₂ 變短」；把四張卡貼在四周，用箭頭從證據連到嫌犯，再從嫌犯連到對策（列印包第 2 頁有草圖格）。
5. 用動畫對照：`index.html#bloch` 按「T1 能量弛豫」看 T₁ 的畫面，按「Ramsey 進動 + T2」看 T₂ 的畫面。

## 下半場：孩子改造——設計量測實驗（約 30 分鐘）

1. 用列印包第 3 頁，挑一個嫌犯。
2. 寫下要量哪一個時間（T₁：翻到 |1⟩、等一段時間再量；T₂：拉姆齊實驗，先做成疊加態、讓它自己轉一段時間再量）。
3. 寫下「只改一個條件」：例如調離甜蜜點（磁通雜訊）、加不加紅外屏蔽（準粒子）。
4. 寫下預期：如果真的是它，哪一個時間會變短？如果另一個時間也跟著變，要怎麼解釋？
5. 檢查自己的數字有沒有違反 T₂ ≤ 2T₁（可以跑 `suspect_check.py`）。
''',

'suspect_check.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n'
  '## suspect_check.py 實跑輸出\n\n```\n' + RUN_LOG + '```\n\n'
  '## 嫌犯卡參考答案\n\n'
  '| 嫌犯 | 躲在哪 | 證據 | 對策 |\n|---|---|---|---|\n'
  '| TLS 二能階缺陷 | 金屬與基板介面、表面氧化層、接面絕緣層 | T₁ 變短、頻率漂移 | 表面處理、Ta/Nb 電容板、藍寶石或高電阻率矽、加大電容板間距 |\n'
  '| 準粒子 | 紅外線、宇宙射線打散庫柏對 | T₁ 變短 | 紅外屏蔽、濾波器、準粒子陷阱 |\n'
  '| 磁通雜訊 | 晶片表面的自旋 | T₂ 變短（可調頻量子位元） | 甜蜜點、不對稱 SQUID、磁屏蔽 |\n'
  '| 熱光子與 Purcell | 讀取腔 | 熱光子：T₂ 變短；Purcell：T₁ 變短 | 輸入線衰減器、Purcell 濾波器、接地與封裝 |\n\n'
  '（簡報 JJ_Microwave_Readout_Talk p24；周邊系統簡報 p6。）\n\n'
  '## 暫停題：T₁ = 50 μs、T₂ = 150 μs 可信嗎？\n\n'
  '- 不可信。2T₁ = 100 μs，T₂ 不可能超過它；先懷疑量測或計算（例如兩個時間不是同一顆、同一個條件下量的，或擬合出錯）。\n\n'
  '## 量測實驗範例\n\n'
  '> 嫌犯：磁通雜訊。我先在甜蜜點用拉姆齊實驗量 T₂，再只把量子位元調離甜蜜點、其他都不改，再量一次 T₂。'
  '如果真的是磁通雜訊，離開甜蜜點後 T₂ 會明顯變短，T₁ 應該差不多。\n\n'
  '（這是設計，不是真的量到的數據。）\n\n'
  '## 常見問題\n\n'
  '- 為什麼 T₂ 不會大於 2T₁？能量漏掉時相位資訊也跟著沒了；只有能量弛豫是唯一來源時，T₂ 才剛好等於 2T₁（維基百科 Quantum decoherence）。\n'
  '- 動畫的 Ramsey 模式為什麼 P(1) 一直是 0.5？箭頭一直在赤道上，只是變短；相位亂掉，直接量 0 和 1 看不出來，要用拉姆齊實驗把相位資訊轉成機率才看得到。\n'
  '- 輻射跟準粒子有什麼關係？紅外線、宇宙射線的能量會打散庫柏對，被打散的電子就是準粒子（簡報 p24）。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的 3D 動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要伺服器或帳號。網址後面的 `#…` 會直接跳到那個場景。

## `index.html#bloch`（JJ 與微波讀取 3D 場景 1：量子位元與 Bloch 球）

- 左邊面板往下捲，有一排模式按鈕：「Rabi 振盪」「Ramsey 進動 + T2」「T1 能量弛豫」「手動 θ / φ」。每按一次都從頭開始；每個模式 12 秒自動重來一次。
- 「T1 能量弛豫」＝證據一：金色箭頭從南極 |1⟩ 沿縱軸往上縮、穿過球心、指向 |0⟩；尖端小字 P(1) 往下掉，右下小圖曲線從 1 往下滑。
- 「Ramsey 進動 + T2」＝證據二：箭頭在赤道上邊轉邊縮，畫出往內捲的螺旋；右下小圖平平停在 0.5；讀數 |r| 變小，括號寫「混態：失去相干性」。
- 「Rabi 振盪」＝對照組：動畫沒有加雜訊，箭頭沿球面一圈一圈轉，讀數「純態」，小圖曲線一次又一次回到 1。
- 動畫裡的時間是相對單位，比真實晶片慢很多。

## 之後的課

Q032「模組發表：設計我的 transmon」會選定頻率、非諧性、E_J／E_C，替每個數字說出取捨。
''',
}

SHEET_HEADER = ['嫌犯', '躲在哪', '證據（T₁ 或 T₂ 變短）', '對策', '怎麼確認是它']
SHEET_ROWS = [['TLS 二能階缺陷'], ['準粒子'], ['磁通雜訊'], ['讀取腔熱光子／Purcell']]

EXTRA_CSS = '''table.rec td{height:13mm;font-size:11pt;text-align:center}table.rec th{font-size:10.5pt}
.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.cards{display:grid;grid-template-columns:1fr 1fr;gap:4mm}.card{border:2px dashed #0b2540;border-radius:3mm;padding:3mm 4mm;min-height:52mm}
.card h3{margin:0 0 2mm;font-size:13pt}.card p{margin:1.5mm 0;font-size:11pt}
.map{border:2px solid #0b2540;border-radius:3mm;height:150mm;position:relative;margin-top:3mm}
.ev{position:absolute;width:52mm;height:24mm;border:2px solid #b07a20;border-radius:12mm;text-align:center;line-height:24mm;font-size:12pt;font-weight:bold}'''


def _card(name):
    return (f'<div class="card"><h3>嫌犯：{name}</h3><p>躲在哪：＿＿＿＿＿＿＿＿＿＿＿＿</p><p>做了什麼：＿＿＿＿＿＿＿＿＿＿</p>'
            '<p>證據：□ T₁ 變短　□ T₂ 變短</p><p>（背面）對策：＿＿＿＿＿＿＿＿＿</p><p>怎麼確認是它：＿＿＿＿＿＿＿</p></div>')


def html():
    pages = [
        '<h2>嫌犯卡模板</h2><p class="lead">沿虛線剪開，正面填線索，背面寫對策。證據只能勾一個：T₁ 變短或 T₂ 變短。</p>'
        '<div class="cards">' + ''.join(_card(n) for n in ('TLS 二能階缺陷', '準粒子', '磁通雜訊', '讀取腔熱光子')) + '</div>'
        '<p style="font-size:10.5pt;color:#35506b">提示：Purcell 效應（能量經讀取腔漏出）寫在熱光子卡的背面當「共犯」，它留下的證據是 T₁ 變短。</p>',
        '<h2>雜訊來源關係圖（草圖格）</h2><p class="lead">中間兩個證據，四周貼嫌犯卡，用箭頭連到對策。</p>'
        '<div class="map"><div class="ev" style="left:20mm;top:60mm">證據：T₁ 變短</div>'
        '<div class="ev" style="right:20mm;top:60mm">證據：T₂ 變短</div></div>'
        '<p style="font-size:10.5pt;color:#35506b">畫好後檢查：每個嫌犯至少一條箭頭連到證據、一條連到對策。</p>',
        '<h2>量測實驗設計單</h2><p class="lead">挑一個嫌犯，設計實驗證明真的是它：只改一個條件，比較前後。</p>'
        '<div class="box"><p>我懷疑的嫌犯：＿＿＿＿＿＿＿＿　要量的時間：□ T₁　□ T₂</p>'
        '<p>量法（T₁：翻到 |1⟩ 等一下再量；T₂：拉姆齊實驗）：</p><div class="line"></div></div>'
        '<table class="rec" style="margin-top:3mm"><tr><th></th><th>改了什麼條件</th><th>預期 T₁</th><th>預期 T₂</th></tr>'
        '<tr><td>對照</td><td>不改</td><td></td><td></td></tr><tr><td>實驗</td><td></td><td></td><td></td></tr></table>'
        '<div class="box" style="margin-top:4mm"><p>如果真的是它，結果會怎樣？</p><div class="line"></div>'
        '<p>檢查：預期的 T₂ 有沒有大於 2T₁？</p><div class="line"></div>'
        '<p>還有哪個嫌犯也可能造成一樣的結果？</p><div class="line"></div></div>',
        '<h2>說明卡：我的雜訊來源關係圖</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 退相干：敵人在哪裡在解決什麼？</p><div class="line"></div><p>2. 我怎麼做？</p><div class="line"></div>'
        '<p>3. 哪裡容易錯？</p><div class="line"></div><p>4. 生活中或真實的量子電腦哪裡會用到？</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出 T₁、T₂ 各代表什麼</li><li>說出四個嫌犯各讓哪個時間變短</li>'
        '<li>說出每個嫌犯的一個對策</li><li>說出 T₂ 不會大於 2T₁，看到這種數據先懷疑量測</li>'
        '<li>講解自己設計的量測實驗</li><li>替關係圖取名字、拍照存檔</li></ul></div>',
    ]
    return printpack.document('Q031 嫌犯卡 列印包', '父子科技學院 量子電腦學程 Q031｜退相干：敵人在哪裡', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q031-decoherence-suspects', folder='Q031_退相干敵人在哪裡', files=FILES,
        sheet=('03_嫌犯卡紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_嫌犯卡.pdf', pack_pages=4,
        pack_needles=('嫌犯卡模板', '雜訊來源關係圖', '量測實驗設計單', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q031', episode_dir='specials/q031-decoherence-suspects',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'none（suspect_check.py 只要 Python 3；動畫用瀏覽器）',
               'program': 'suspect_check.py',
               'recordedRun': {'t2_le_2t1': {f'{a}/{b}': v for (a, b), v in R['CHECK'].items()},
                               'scene_t1_z_at_12': round(R['CURVE'][12][1], 2), 'scene_ramsey_r_at_12': round(R['CURVE'][12][2], 2)},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q031/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')
