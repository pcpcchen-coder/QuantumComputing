"""Q129 課堂教材：用電清單（尋寶卡）、用電全景圖畫格、三平台用電大戶比較表、容易錯的地方、教爸爸檢核表與解答；
可執行的 power_inventory.py（純 Python：一套系統與 1,000 位元設施的用電加總、和 HPC 機櫃比、改造區自己的清單）。

不需要帳號，也不需要安裝套件：動畫用瀏覽器開 animations/power1000.html#overview、peripherals.html#overview；程式只要 Python 3。
建置時會真的執行一次 power_inventory.py，確認輸出和影片、教材寫的數字一致。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q129/classroom.py
"""
from pathlib import Path
import os
import subprocess
import sys
import tempfile

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 製作代理實跑紀錄：Python 3.13.18，無外部套件，結果固定（無亂數）
RUN_OUTPUT = '''一、一套超導量子電腦（peripherals.html#overview，示意）
  脈衝管壓縮機：10.7 kW（40.8%，冷凍）
  冷卻水系統：10.0 kW（38.2%，設施）
  控制電子機櫃：3.0 kW（11.5%，控制電子）
  氣體處理系統（泵）：1.5 kW（5.7%，冷凍）
  電腦 / 監控 / 網路：1.0 kW（3.8%，設施）
  合計 26.2 kW
  分三類：冷凍 12.2 kW（47%）、控制電子 3.0 kW（11%）、設施 11.0 kW（42%）
  為了保冷用的電（壓縮機＋冷卻水＋氣體處理）：22.2 kW，佔 85%
二、1,000 位元設施（power1000.html#overview，推論區間）
  機電匯流排：55.5–107.5 kW（壓縮機 ×3–5、冰水機與泵、氣體處理系統）
  乾淨匯流排：15–112 kW（控制電子、精密直流 ×110 台、時脈與網路）
  運算匯流排：10–100 kW（即時解碼、電子區空調）
  合計 80.5–319.5 kW，中點合計 200 kW
三、和一個 HPC 機櫃（約 140 kW）比
  一套超導量子電腦 26.2 kW ＝ 機櫃的 19%
  1,000 位元設施中點 200 kW ＝ 1.4 個機櫃
四、我的用電清單（MY_LIST）
  冷凍：10.7 kW
  控制電子：3.0 kW
  設施：10.0 kW
  已找到 3 項、合計 23.7 kW
'''

PROGRAM = '''"""父子科技學院 量子電腦學程 Q129：電從哪裡來、到哪裡去——用電清單（純 Python，不需要安裝任何套件，沒有亂數）

執行：  python power_inventory.py
一、一套超導量子電腦（約 20 位元級）的用電清單：數字取自學程動畫 peripherals.html#overview 右下的「典型用電分配（示意）」。
二、1,000 位元設施的用電清單：數字取自 power1000.html#overview（設計文件第 4 章的推論區間）。
三、和一個超級電腦（HPC）機櫃比一比（約 140 kW，供電簡報第 6 頁）。
四、改造區：把你自己找到的設備寫進 MY_LIST，程式會幫你分類加總。
"""

# 一、一套超導量子電腦：(設備, kW, 類別)
ONE_SYSTEM = [
    ('脈衝管壓縮機', 10.7, '冷凍'),
    ('冷卻水系統', 10.0, '設施'),
    ('控制電子機櫃', 3.0, '控制電子'),
    ('氣體處理系統（泵）', 1.5, '冷凍'),
    ('電腦 / 監控 / 網路', 1.0, '設施'),
]
# 為了讓晶片保持低溫而用的電：壓縮機、冷卻水（帶走壓縮機的熱）、氣體處理系統
KEEP_COLD = ('脈衝管壓縮機', '冷卻水系統', '氣體處理系統（泵）')

# 二、1,000 位元設施：(負載, 低 kW, 高 kW, 匯流排)
FACILITY = [
    ('壓縮機 ×3–5', 37.5, 62.5, '機電'),
    ('冰水機與泵', 15, 40, '機電'),
    ('氣體處理系統', 3, 5, '機電'),
    ('控制電子', 10, 100, '乾淨'),
    ('精密直流 ×110 台', 3, 7, '乾淨'),
    ('時脈與網路', 2, 5, '乾淨'),
    ('即時解碼', 5, 50, '運算'),
    ('電子區空調', 5, 50, '運算'),
]

GROUPS = ('冷凍', '控制電子', '設施')
HPC_RACK = 140.0  # kW，一個 HPC 機櫃（Cray EX4000，供電簡報第 6 頁）

# 四、改造區：你在動畫裡找到的設備（設備, kW, 類別：冷凍／控制電子／設施）
MY_LIST = [
    ('脈衝管壓縮機', 10.7, '冷凍'),
    ('冷卻水系統', 10.0, '設施'),
    ('控制電子機櫃', 3.0, '控制電子'),
]


def by_group(items):
    out = {}
    for name, kw, g in items:
        out[g] = out.get(g, 0) + kw
    return out


def show_list(title, items):
    total = sum(kw for _, kw, _ in items)
    print(title)
    for name, kw, g in items:
        print(f'  {name}：{kw:.1f} kW（{kw / total * 100:.1f}%，{g}）')
    print(f'  合計 {total:.1f} kW')
    groups = by_group(items)
    print('  分三類：' + '、'.join(f'{g} {groups[g]:.1f} kW（{groups[g] / total * 100:.0f}%）' for g in GROUPS if g in groups))
    return total


if __name__ == '__main__':
    total = show_list('一、一套超導量子電腦（peripherals.html#overview，示意）', ONE_SYSTEM)
    cold = sum(kw for n, kw, _ in ONE_SYSTEM if n in KEEP_COLD)
    print(f'  為了保冷用的電（壓縮機＋冷卻水＋氣體處理）：{cold:.1f} kW，佔 {cold / total * 100:.0f}%')
    print('二、1,000 位元設施（power1000.html#overview，推論區間）')
    lo = sum(x[1] for x in FACILITY)
    hi = sum(x[2] for x in FACILITY)
    mid = sum((x[1] + x[2]) / 2 for x in FACILITY)
    for bus in ('機電', '乾淨', '運算'):
        rows = [x for x in FACILITY if x[3] == bus]
        print(f'  {bus}匯流排：{sum(r[1] for r in rows):g}–{sum(r[2] for r in rows):g} kW（'
              + '、'.join(r[0] for r in rows) + '）')
    print(f'  合計 {lo:g}–{hi:g} kW，中點合計 {mid:g} kW')
    print('三、和一個 HPC 機櫃（約 140 kW）比')
    print(f'  一套超導量子電腦 {total:.1f} kW ＝ 機櫃的 {total / HPC_RACK * 100:.0f}%')
    print(f'  1,000 位元設施中點 {mid:g} kW ＝ {mid / HPC_RACK:.1f} 個機櫃')
    print('四、我的用電清單（MY_LIST）')
    mine = by_group(MY_LIST)
    for g in GROUPS:
        print(f'  {g}：{mine.get(g, 0):.1f} kW' + ('' if g in mine else '  ← 還沒找到這一類'))
    print(f'  已找到 {len(MY_LIST)} 項、合計 {sum(kw for _, kw, _ in MY_LIST):.1f} kW')
'''

# 1,000 位元設施的八個負載（power1000.html#overview）：(負載, 區間, 匯流排, 類別, 尋寶提示)
LOADS = [
    ('壓縮機 ×3–5', '37.5–62.5 kW', '機電', '冷凍', '最大的單一負載（痛點 2）'),
    ('冰水機與泵', '15–40 kW', '機電', '設施', '帶走壓縮機的熱'),
    ('GHS（氣體處理系統）', '3–5 kW', '機電', '冷凍', '混合氣循環'),
    ('控制電子', '10–100 kW', '乾淨', '控制電子', '區間最寬'),
    ('精密直流 ×110 台', '3–7 kW', '乾淨', '控制電子', '2,500–3,000 路（痛點 4）'),
    ('時脈與網路', '2–5 kW', '乾淨', '控制電子', '10 MHz 參考、網路'),
    ('即時解碼', '5–50 kW', '運算', '控制電子', '要緊鄰機台（痛點 7）'),
    ('電子區空調', '5–50 kW', '運算', '設施', '把電子的熱帶走'),
]

# 三平台用電大戶（供電簡報 p6；文獻回顧 §7.1、§12、§17）
PLATFORMS = [
    ('超導', '約 20–30 kW', '稀釋冷凍機的壓縮機（每台 10–15 kW）＋冷卻水', '要 10 mK，冷卻鏈最耗電'),
    ('離子阱', 'Helios 官方 < 40 kW', '精密空調與雷射冷卻水、雷射、控制電子', '讓光路和雷射穩定的環境設備是大宗（推論）'),
    ('中性原子', '約 3–10 kW', '精密空調與冷卻水、雷射（光纖放大器）、控制電子', '不需要稀釋冷凍機'),
]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q129：電從哪裡來、到哪裡去（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶出今天的任務：把量子電腦當成一個要供電、要備援的工程系統，跟著電走一圈——從市電進門、經過配電和不斷電系統、到每台設備，最後變成熱被帶走。課堂用「尋寶」的方式，在動畫的全景場景裡找出每一條電路，填成一張用電清單，再畫成用電全景圖。

## 需要準備

| 項目 | 說明 |
|---|---|
| 動畫 | 下載學程的 `animations/` 資料夾，用瀏覽器開 `power1000.html#overview`（主場景）；加映 `peripherals.html#overview`、`peripherals.html#pulsetube`。免安裝、不需帳號 |
| 程式 | `power_inventory.py`：只要有 Python 3 就能跑，不需安裝套件、不需帳號 |
| 列印 | `02_列印包_電從哪裡來到哪裡去.pdf`（A4，共 4 頁）；三種顏色的筆（冷凍、控制電子、設施各一色） |

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片；先猜「量子電腦最耗電的是晶片嗎？」 | 影片、列印包第 1 頁 |
| 10–25 | 概念示範：用電三大類、電的路線、一套約 26 kW、壓縮機是電老虎 | 影片第 3–8 段、`05_動畫導覽.md` |
| 25–65 | 尋寶：在 power1000.html#overview 找出每一條電路，填用電清單，跑 power_inventory.py | `01_操作步驟.md`、列印包第 1 頁、`03_用電清單.csv` |
| 65–75 | 休息 | |
| 75–105 | 比較超導、離子阱、中性原子的用電大戶；畫用電全景圖 | 列印包第 2、3 頁 |
| 105–115 | 孩子教爸爸：操作與原理，指出一個注意事項 | 列印包第 4 頁 |
| 115–120 | 錄音總結、替用電全景圖命名、存檔 | |

## 課前準備（約 20 分鐘）

- 自己先打開 `power1000.html#overview`，從左邊「中壓進線」順著粒子看到右邊的冷凍機；點紅色編號 2、4、7 看痛點說明。
- 跑一次 `python power_inventory.py`，確認第一段最後一行是「保冷用的電……22.2 kW，佔 85%」，第二段是「中點合計 200 kW」。
- 讀一遍 `04_解答.md`（用電清單、三平台比較的參考答案）。

## 主持尋寶的原則

- 一個負載算一件寶物：找到方塊、說出它屬於哪條匯流排、哪一類（冷凍／控制電子／設施），才算找到。
- 數字一律抄動畫上寫的區間，不要自己估；清單上另外標「能不能斷」「怕不怕雜訊」。
- 最重要的一句：耗電量本身不是最難的問題，難的是不能斷電與低干擾。

## 誠實說明

- 一套系統的 26 kW 是周邊動畫的「典型用電分配（示意）」，Google 公開的最壞情況也約 26 kW；實際依機型與規模而異。
- 1,000 位元設施的 80–320 kW 是學程設計文件第 4 章的推論區間，不是實測。動畫三條匯流排上的「約 80／70／30 kW」是頁面的取整數字，和八個負載的中點相加不完全一樣，教材以八個負載的區間為準。
- 斷電後要多久才能恢復，是下一課（Q130）的主題；本課只標「能不能斷」，不展開。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：電路尋寶（約 40 分鐘）

1. 用瀏覽器開 `animations/power1000.html#overview`（場景 1：全景：電從哪裡來、到哪裡去）。不要勾「模擬斷電」（那是下一課的內容）。
2. 從最左邊的「中壓進線」出發，順著粒子走到「分層 UPS」，再分成三條：橘色＝機電匯流排、青色＝乾淨匯流排、紫色＝運算匯流排。
3. 每找到一個負載方塊，就在列印包第 1 頁的用電清單填上：區間、匯流排、類別（冷凍／控制電子／設施）。
4. 點紅色編號 2、4、7，把面板上的痛點說明各抄一句。
5. 打開 `power_inventory.py`，先預測：一套系統裡保冷用的電佔幾成？千位元設施的中點是多少？再執行 `python power_inventory.py` 對答案。
6. 加映（可選）：開 `peripherals.html#overview`，按「只看訊號相關」→「微波 / DC」→「資料 / 時脈」→「電力」，只留黃色電力線；再按「只看冷卻相關」，看右下的典型用電分配。

## 下半場：三平台用電大戶（約 30 分鐘）

1. 在列印包第 3 頁的比較表，寫下超導、離子阱、中性原子各自的用電大戶（看 `04_解答.md` 之前先自己猜）。
2. 改造：把你在動畫裡找到的設備寫進 `power_inventory.py` 的 `MY_LIST`（設備、kW、類別），再跑一次，看三類各找到多少。
3. 在列印包第 2 頁畫用電全景圖：左邊進門、中間分配、右邊設備，最後畫出熱往哪裡去；三類設備用三種顏色。
4. 想一想：哪一類用電最多？哪一類用電不多但最怕雜訊？
''',

'power_inventory.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n## 用電清單（power1000.html#overview 的八個負載）\n\n| 負載 | 區間 | 匯流排 | 類別 | 提示 |\n|---|---|---|---|---|\n'
  + ''.join(f'| {a} | {b} | {c} | {d} | {e} |\n' for a, b, c, d, e in LOADS)
  + '\n類別是本課的分法（冷凍＝讓晶片變冷的機器；控制電子＝產生、量測、處理訊號；設施＝冷卻水、空調等支援環境），匯流排是動畫的分法，兩者不必一一對應。\n'
  + '\n## 三平台的用電大戶\n\n| 平台 | 單套功率 | 用電大戶 | 備註 |\n|---|---|---|---|\n'
  + ''.join(f'| {a} | {b} | {c} | {d} |\n' for a, b, c, d in PLATFORMS)
  + '\n## power_inventory.py 實跑（Python 3.13.18）\n\n```\n' + RUN_OUTPUT + '```\n\n'
  '- 一套系統：壓縮機 10.7＋冷卻水 10.0＋氣體處理 1.5 = 22.2 kW，佔 26.2 kW 的 85%——大部分的電都花在保冷。\n'
  '- 壓縮機約 10 kW 的電，在 4 K 那一層只換到約 1.5 W 的冷卻（peripherals.html#pulsetube 的標籤）；其餘幾乎都變成熱，由冷卻水帶走。\n'
  '- 千位元設施：八個負載的低值相加 80.5 kW、高值相加 319.5 kW、中點相加 200 kW，約 1.4 個 HPC 機櫃（約 140 kW）。\n'
  '- 常見誤解：耗電量本身不是最難的問題（一套超導量子電腦約 20–30 kW，比一個 HPC 機櫃還小）；難的是不能斷電與低干擾（偏壓要 µV 級、上百台儀器的漏電流加起來會變成地電位雜訊）。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載整個資料夾後用瀏覽器開啟，不需要網路、伺服器或帳號。

## `power1000.html#overview`（場景 1：全景：電從哪裡來、到哪裡去）

- 左到右：中壓進線（雙迴路＋發電機）→ 分層 UPS（80–270 kW）→ 機電、乾淨、運算三條匯流排 → 八個負載 → 稀釋冷凍機。
- 粒子密度代表功率；橘色＝機電、青色＝乾淨、紫色＝運算。
- 紅色編號 1–7 是痛點，點擊後說明出現在左邊面板；本課看 2（壓縮機）、4（精密直流）、7（即時解碼）。1 號與「模擬斷電」留給下一課。

## `peripherals.html#overview`（場景 1：機房全景）

- 七個連接按鈕可以各自開關：脈衝管氦氣、冷卻水、混合氣循環、真空、微波 / DC、資料 / 時脈、電力；另有「全部顯示」「只看冷卻相關」「只看訊號相關」。
- 右下「典型用電分配（kW，示意）」：脈衝管壓縮機 10.7、冷卻水系統 10.0、控制電子機櫃 3.0、氣體處理系統 1.5、電腦／監控／網路 1.0，合計約 26 kW。

## `peripherals.html#pulsetube`（場景 2：脈衝管冷卻器＋氦壓縮機）

- 「氦壓縮機 電力 ~10 kW · 水冷」；紅色高壓氦、藍色低壓氦兩條軟管；冷卻水一進一出。
- 「一級冷端 ~45 K（~40 W）」「二級冷端 ~3 K（~1.5 W @ 4.2 K）」：一萬瓦的電換來的低溫冷卻只有幾瓦。

## 操作

power1000.html：左右方向鍵換場景、空白鍵暫停、H 隱藏面板。peripherals.html：滑鼠拖曳旋轉、滾輪縮放、R 重設視角。
''',
}

SHEET_HEADER = ['負載', '動畫上的區間', '匯流排（機電／乾淨／運算）', '類別（冷凍／控制電子／設施）', '能不能斷', '怕不怕雜訊', '找到了嗎']
SHEET_ROWS = [[a] for a, *_ in LOADS] + [['自己找的：'], ['自己找的：']]

EXTRA_CSS = '''table.rec td{height:8.5mm}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.frame{border:1.2pt dashed #4a6a88;border-radius:3mm;height:120mm;margin-top:3mm;position:relative}
.frame span{position:absolute;top:2mm;font-size:10pt;color:#4a6a88}
pre.code{font-size:9pt;background:#f2f6fa;border:1pt solid #cfdde8;padding:3mm;margin:2mm 0;white-space:pre-wrap}'''


def check_program():
    """真的跑一次 power_inventory.py（隔離模式），確認輸出和影片、教材寫的數字一致。"""
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / 'power_inventory.py'
        p.write_text(PROGRAM, encoding='utf-8')
        out = subprocess.run([sys.executable, '-I', str(p)], capture_output=True, text=True, check=True,
                             env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}).stdout
    assert out == RUN_OUTPUT, out
    return out


def html():
    rows = ''.join(f'<tr><td>{a}</td><td></td><td></td><td></td><td></td></tr>' for a, *_ in LOADS)
    plat = ''.join(f'<tr><td>{a}</td><td></td><td></td></tr>' for a, *_ in PLATFORMS)
    pages = [
        '<h2>用電清單：電路尋寶卡</h2><p class="lead">開 power1000.html#overview，從「中壓進線」順著粒子找。不要勾「模擬斷電」。</p>'
        '<p>開場先猜：量子電腦最耗電的是晶片嗎？ □ 是　□ 不是　我猜最耗電的是＿＿＿＿＿＿＿＿＿＿</p>'
        '<table class="rec"><tr><th>負載</th><th>區間（kW）</th><th>匯流排</th><th>類別</th><th>能不能斷／怕不怕雜訊</th></tr>' + rows + '</table>'
        '<p class="note">紅色編號 2、4、7 的痛點各抄一句：</p><div class="line"></div><div class="line"></div><div class="line"></div>',
        '<h2>用電全景圖</h2><p class="lead">左邊進門、中間分配、右邊設備，最後畫出熱往哪裡去。冷凍、控制電子、設施各用一種顏色。</p>'
        '<div class="frame"><span>進門（市電）→ 分配（配電盤、UPS）→ 設備 → 熱（冷卻水、空調）</span></div>'
        '<p>作品名稱：＿＿＿＿＿＿＿＿　用電最多的一類：＿＿＿＿　保冷約佔＿＿%</p>',
        '<h2>換你改造：三平台的用電大戶</h2><p class="lead">先自己猜，再看解答。單套功率填數字，大戶寫設備。</p>'
        '<table class="rec"><tr><th>平台</th><th>單套功率</th><th>用電大戶</th></tr>' + plat + '</table>'
        '<pre class="code">MY_LIST = [\n    (\'脈衝管壓縮機\', 10.7, \'冷凍\'),\n    (\'冷卻水系統\', 10.0, \'設施\'),\n    (\'控制電子機櫃\', 3.0, \'控制電子\'),\n    # 改造區：加上你找到的設備\n]</pre>'
        '<div class="box"><h3>三個容易錯的地方</h3><ul class="chk">'
        '<li>最耗電的不是晶片，而是讓晶片保持低溫的壓縮機和冷卻水</li>'
        '<li>耗電量本身不是最難的問題：一套約 20–30 kW，比一個 HPC 機櫃還小</li>'
        '<li>用電少不代表不重要：精密直流只有幾十瓦，卻要 µV 級的穩定</li></ul></div>',
        '<h2>最後一關：教爸爸用電全景</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 電從哪裡來、到哪裡去？</p><div class="line"></div>'
        '<p>2. 哪一類設備用電最多？為什麼？</p><div class="line"></div>'
        '<p>3. 一個注意事項（錯誤、限制或提醒）：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><ul class="chk">'
        '<li>不看稿說出電的路線：進門、分配、設備、變成熱</li><li>示範 power1000.html#overview：點一個紅色編號並解釋</li>'
        '<li>說出一套系統約 26 kW、保冷約 85%</li><li>指出一個注意事項：難的是不能斷電與低干擾</li>'
        '<li>替用電全景圖取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q129 電從哪裡來、到哪裡去 列印包', '父子科技學院 量子電腦學程 Q129｜電從哪裡來、到哪裡去', pages, EXTRA_CSS)


if __name__ == '__main__':
    check_program()
    classroom_pack.build(
        slug='q129-power-panorama', folder='Q129_電從哪裡來到哪裡去', files=FILES,
        sheet=('03_用電清單.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_電從哪裡來到哪裡去.pdf', pack_pages=4,
        pack_needles=('用電清單', '用電全景圖', '三平台', '容易錯', '最後一關'),
        authoring_dir=XINEW / 'authoring/q129', episode_dir='specials/q129-power-panorama',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'no（瀏覽器開動畫；power_inventory.py 只需 Python 3）',
               'program': 'power_inventory.py', 'testedWith': 'Python 3.13.18 (standard library only)',
               'recordedRun': {'oneSystem_kW': 26.2, 'keepCold_kW': 22.2, 'keepCold_share': 0.85,
                               'facilityLow_kW': 80.5, 'facilityHigh_kW': 319.5, 'facilityMid_kW': 200, 'hpcRacks': 1.4},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q129/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')
