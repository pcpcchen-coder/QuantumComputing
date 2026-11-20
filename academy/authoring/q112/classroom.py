"""Q112 課堂教材：自編對話模板、可執行的 teach_helper.py、十三課選課表、三題練習出題卡、錄音四問、最後一關檢核表與解答。

不需要帳號，也不需要安裝套件：動畫用瀏覽器開 animations/transmon-3d.html（第 1 章 #chip、#capacitor 與章節列）；程式只要 Python 3。
建置時會真的執行一次 teach_helper.py，確認輸出和影片、教材寫的結果一致。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q112/classroom.py
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
RUN_OUTPUT = '''一、對答案：第 1 章「大十字電容的作用」面板（E_J/h = 15 GHz）
  C_Σ 20.0 fF：E_C 969 MHz，E_J/E_C 15.5，f₀₁ 9.69 GHz，α −1.33 GHz，電荷色散 53.1 MHz，判斷：電荷雜訊主導（接近 Cooper pair box）
  C_Σ 77.5 fF：E_C 250 MHz，E_J/E_C 60.0，f₀₁ 5.21 GHz，α −283 MHz，電荷色散 1.9 kHz，判斷：transmon 區間
  C_Σ 200.0 fF：E_C 96.8 MHz，E_J/E_C 154.9，f₀₁ 3.31 GHz，α −104 MHz，電荷色散 < 0.1 Hz，判斷：非諧性偏小，閘需放慢
  滑桿每格 0.5 fF：判斷是「transmon 區間」的範圍是 26.0–154.5 fF
二、出題小幫手（MY_C = 40）
  題目：如果十字電容是 40 fF，E_J/E_C 是多少？位元頻率 f₀₁ 會比 77.5 fF 時的 5.21 GHz 高還是低？落在哪個區間？
  解答：E_J/E_C = 31.0；f₀₁ = 7.10 GHz（比 5.21 GHz 高）；transmon 區間
  C_Σ 40.0 fF：E_C 484 MHz，E_J/E_C 31.0，f₀₁ 7.10 GHz，α −586 MHz，電荷色散 706.7 kHz，判斷：transmon 區間
三、對話稿檢查（MY_LESSON）
  ✓ 有「課名」
  ✓ 有「學習目標」
  ✓ 有「重點整理」
  ✓ 有「動畫演示」
  ✓ 師生對話：老師 3 句、學生 3 句（兩邊都要有）
  ✓ 動畫註明出處（檔名＋#代號＋章名）
  ✓ 課後練習 3 題、解答 3 個（要剛好三題、每題都有解答）
  結果：7/7 項通過
'''

PROGRAM = '''"""父子科技學院 量子電腦學程 Q112：模組發表——換你當老師（純 Python，不需要安裝任何套件）

執行：  python teach_helper.py
一、對答案：transmon-3d.html 第 1 章「大十字電容的作用」分頁的面板數字，照動畫的程式重算一次
    （電荷基底哈密頓量 + 二分法求能階；E_J/h 固定 15 GHz、E_C/h = 19.37 / C[fF] GHz）。
二、出題小幫手：把 MY_C 改成你想考爸爸的電容值，印出一題計算題和它的解答。
三、對話稿檢查：檢查 MY_LESSON 是否有一課該有的五個部分、老師和學生是否都有說話、
    動畫有沒有註明出處（章名與網址後面的 #代號）、課後練習是不是剛好三題而且都有解答。
"""

# 改造區 1：你想考爸爸的電容值（fF；動畫滑桿範圍 5–200，每格 0.5）
MY_C = 40

# 改造區 2：你的自編對話（照模板寫；每一行用「標記：內容」）
MY_LESSON = \'\'\'
課名：第 2 課 Transmon 怎麼寫入狀態
學習目標：對照晶片圖說出十字電容、SQUID、XY 線、Z 線、讀取腔各自的工作
學生：transmon 是怎麼寫入狀態的？SQUID 的作用是什麼？
老師：先猜猜看，五個零件裡，哪一個負責寫入？
學生：SQUID？
老師：很多人這樣猜。其實 SQUID 不負責寫入，XY 線送 5.21 GHz 的微波脈衝才是寫入。
學生：那 SQUID 做什麼？
老師：它有兩個身分：非線性電感，讓能階不等距；也是頻率旋鈕，Z 線的磁通靠它調頻率。
重點整理：XY 線寫入、Z 線經由 SQUID 調頻率、讀取共振腔讀出；SQUID 不負責寫入
動畫演示：transmon-3d.html#chip 第 1 章 晶片：按「送出 π 脈衝」，十字板發光代表進入 |1⟩
練習 1：要把 |0⟩ 寫成一半一半的疊加，要改脈衝的哪個參數？
解答 1：脈衝面積（振幅 × 時間）做成 π/2
練習 2：XY 線和 Z 線分別用電場還是磁場耦合到位元？
解答 2：XY 用電場（電容耦合）；Z 用磁場（磁通穿過 SQUID 迴路）
練習 3：改錯：「SQUID 負責把狀態寫進位元。」
解答 3：寫入靠 XY 線的微波脈衝；SQUID 是非線性電感和頻率旋鈕
\'\'\'

from decimal import Decimal, ROUND_HALF_UP

EJ = 15.0          # E_J/h（GHz），和動畫相同
EC_PER_FF = 19.37  # E_C/h [GHz] = 19.37 / C[fF]，和動畫相同


def transmon_levels(ej, ec, ng, k=3, n=25):
    """電荷基底三對角哈密頓量，用 Sturm 序列二分法求最低 k 個能階（照動畫 transmonLevels 改寫）"""
    d = [4 * ec * (m - ng) ** 2 for m in range(-n, n + 1)]
    e2 = (ej / 2) ** 2

    def count(x):
        q = d[0] - x
        c = 1 if q < 0 else 0
        for i in range(1, len(d)):
            q = d[i] - x - e2 / (1e-300 if q == 0 else q)
            if q < 0:
                c += 1
        return c
    out = []
    for j in range(k):
        lo, hi = -ej - 1, 4 * ec * (n + 1) ** 2 + ej + 1
        for _ in range(90):
            m = (lo + hi) / 2
            if count(m) > j:
                hi = m
            else:
                lo = m
        out.append((lo + hi) / 2)
    return out


def cap_stats(c):
    ec = EC_PER_FF / c
    a, b = transmon_levels(EJ, ec, 0), transmon_levels(EJ, ec, 0.5)
    fa, fb = a[1] - a[0], b[1] - b[0]
    return {'EC': ec, 'f01': (fa + fb) / 2, 'alpha': ((a[2] - 2 * a[1] + a[0]) + (b[2] - 2 * b[1] + b[0])) / 2,
            'disp': abs(fa - fb), 'ratio': EJ / ec}


def fixed(x, n):
    """和 JavaScript 的 toFixed 一樣：剛好一半時進位"""
    return str(Decimal(x).quantize(Decimal(1).scaleb(-n), rounding=ROUND_HALF_UP))


def fmt_f(g):
    """和動畫一樣的頻率格式（輸入單位 GHz）"""
    v = g * 1e9
    if v >= 1e9:
        return fixed(g, 2) + ' GHz'
    if v >= 1e6:
        return fixed(v / 1e6, 0 if v >= 1e8 else 1) + ' MHz'
    if v >= 1e3:
        return fixed(v / 1e3, 1) + ' kHz'
    return fixed(v, 1) + ' Hz'


def verdict(ratio):
    return '電荷雜訊主導（接近 Cooper pair box）' if ratio < 20 else 'transmon 區間' if ratio <= 120 else '非諧性偏小，閘需放慢'


def row(c):
    r = cap_stats(c)
    disp = '< 0.1 Hz' if r['disp'] * 1e9 < 0.1 else fmt_f(r['disp'])
    sign = '−' if r['alpha'] < 0 else '+'
    return (f'C_Σ {c:.1f} fF：E_C {fmt_f(r["EC"])}，E_J/E_C {fixed(r["ratio"], 1)}，f₀₁ {fmt_f(r["f01"])}，'
            f'α {sign}{fmt_f(abs(r["alpha"]))}，電荷色散 {disp}，判斷：{verdict(r["ratio"])}')


SECTIONS = ['課名', '學習目標', '重點整理', '動畫演示']


def check_lesson(text):
    lines = [s.strip() for s in text.strip().splitlines() if s.strip()]
    tags = [s.split('：', 1)[0] for s in lines]
    res = []
    for s in SECTIONS:
        res.append((f'有「{s}」', s in tags))
    t, st = tags.count('老師'), tags.count('學生')
    res.append((f'師生對話：老師 {t} 句、學生 {st} 句（兩邊都要有）', t > 0 and st > 0))
    anim = [s for s in lines if s.startswith('動畫演示')]
    res.append(('動畫註明出處（檔名＋#代號＋章名）', any('.html#' in s and '章' in s for s in anim)))
    q = [s for s in tags if s.startswith('練習')]
    a = [s for s in tags if s.startswith('解答')]
    res.append((f'課後練習 {len(q)} 題、解答 {len(a)} 個（要剛好三題、每題都有解答）', len(q) == 3 and len(a) == 3))
    return res


if __name__ == '__main__':
    print('一、對答案：第 1 章「大十字電容的作用」面板（E_J/h = 15 GHz）')
    for c in (20, 77.5, 200):
        print('  ' + row(c))
    lo = next(x / 2 for x in range(10, 401) if 20 <= cap_stats(x / 2)['ratio'] <= 120)
    hi = max(x / 2 for x in range(10, 401) if 20 <= cap_stats(x / 2)['ratio'] <= 120)
    print(f'  滑桿每格 0.5 fF：判斷是「transmon 區間」的範圍是 {lo:.1f}–{hi:.1f} fF')
    print(f'二、出題小幫手（MY_C = {MY_C}）')
    r = cap_stats(MY_C)
    print(f'  題目：如果十字電容是 {MY_C} fF，E_J/E_C 是多少？位元頻率 f₀₁ 會比 77.5 fF 時的 5.21 GHz 高還是低？落在哪個區間？')
    print(f'  解答：E_J/E_C = {fixed(r["ratio"], 1)}；f₀₁ = {fmt_f(r["f01"])}（比 5.21 GHz {"高" if r["f01"] > cap_stats(77.5)["f01"] else "低"}）；{verdict(r["ratio"])}')
    print('  ' + row(MY_C))
    print('三、對話稿檢查（MY_LESSON）')
    res = check_lesson(MY_LESSON)
    for name, ok in res:
        print(f'  {"✓" if ok else "✗"} {name}')
    print(f'  結果：{sum(ok for _, ok in res)}/{len(res)} 項通過')
'''

# 十三課選課表（師生對話教學紀錄「課程地圖」與附錄 A）
LESSONS13 = [
    ('1', 'SQUID 干涉', '第 1 章 晶片（#chip）'), ('2', '寫入與 SQUID', '第 1、4 章（#chip、#control）'),
    ('3', '迷思修正：Z 線', '第 6 章 案例（#case）'), ('4', '頻率配置', '第 6 章 案例（#case）'),
    ('5', '能階與 Rabi', '第 3、4 章（#potential、#control）'), ('6', '讀取與重設', '第 5 章 讀取（#readout）'),
    ('7', '疊加與 BV', '第 9 章 BV 密碼（#bv）'), ('8', '糾纏與 Grover', '第 7 章 振幅長條（#grover）'),
    ('9', 'Deutsch', '第 7 章（#deutsch）'), ('10', 'Shor', '第 8 章 Shor（#shor）'),
    ('11', '表面碼', '第 10 章 表面碼（#surface）'), ('12', 'Lattice surgery 與魔術態', '第 11 章 邏輯閘（#surgery）'),
    ('13', '軟體堆疊', '第 12 章 軟體堆疊（#stack）'),
]

TEMPLATE_MD = '''# 自編對話模板（照教學紀錄「每一課的固定結構」）

> 寫法：每一行用「標記：內容」，貼進 teach_helper.py 的 MY_LESSON 就能自動檢查。

課名：第＿課 ＿＿＿＿＿＿＿＿
學習目標：（說得出的 2–3 件事）
學生：（保留學生原本的問法）
老師：（先讓學生猜／先修正一個小觀念）
學生：
老師：（一步一步解釋；可以用一個比喻）
重點整理：（一段話收尾）
動畫演示：transmon-3d.html#＿＿＿ 第＿章 ＿＿＿：按「＿＿＿」，看到＿＿＿
練習 1：（計算題）
解答 1：
練習 2：（為什麼題）
解答 2：
練習 3：（改錯題：從附錄 D 的迷思改寫）
解答 3：

注意事項：引用動畫畫面時要註明出處（檔名＋#代號＋章名）；動畫上的數字多半是範例或示意值，不能當成實測。
'''

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q112：模組發表——換你當老師（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。QM07「超導量子電腦深入：師生對話十三課」走完了，今天是模組發表：角色交換，孩子當老師、爸爸當學生。孩子從十三課挑一課，照教學紀錄「每一課的固定結構」（學習目標、師生對話、重點整理、動畫演示、課後練習）改寫成自己的師生對話、錄音，用 transmon 3D 動畫示範，再替這課出三題課後練習與解答。

## 需要準備

| 項目 | 說明 |
|---|---|
| 文件 | docs/超導量子電腦師生對話教學紀錄.md（全篇；課程地圖、附錄 A 章節對照、附錄 D 學生迷思最好用） |
| 動畫 | 下載學程的 `animations/` 資料夾，用瀏覽器開 `transmon-3d.html`（需連網載入 three.js；資料夾內附 lib/three-r128.min.js 時可離線）。免安裝、不需帳號 |
| 程式 | `teach_helper.py`：只要有 Python 3 就能跑，不需安裝套件、不需帳號 |
| 錄音 | 手機或電腦的錄音程式即可 |
| 列印 | `02_列印包_自編對話一課.pdf`（A4，共 4 頁）；`06_自編對話模板.md` 可直接複製 |

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片；孩子先說「十三課裡我最想教哪一課？為什麼？」 | 影片、`03_十三課選課表.csv` |
| 10–25 | 概念示範：一課五個部分、以第 2 課示範、好老師三招、三種題型、註明出處 | 影片第 3–8 段、`05_動畫導覽.md` |
| 25–65 | 父子共同實作：挑一課，照模板改寫成自己的師生對話並錄音（孩子當老師、爸爸當學生） | 列印包第 1 頁、`06_自編對話模板.md` |
| 65–75 | 休息 | |
| 75–105 | 孩子獨立改造：替這課加三題課後練習與解答；用 teach_helper.py 出題、檢查對話稿 | 列印包第 2 頁、`teach_helper.py` |
| 105–115 | 角色互換：孩子不看稿教爸爸操作與原理 | 列印包第 3、4 頁 |
| 115–120 | 錄音總結（錄音四問）、作品命名、版本存檔 | 列印包第 3 頁 |

## 課前準備（約 20 分鐘）

- 讀一遍教學紀錄的「怎麼使用這份紀錄」與「課程地圖」，再讀第 2 課（影片示範用的那一課）。
- 打開 `transmon-3d.html#chip`：按「送出 π 脈衝」，看青色光點沿 XY 驅動線前進、十字板發光再慢慢變暗；取消「顯示標籤」。
- 按「大十字電容的作用」分頁（或開 `#capacitor`），把 C_Σ 滑桿拖到 20 和 200 fF，看面板的判斷改變。
- 跑一次 `python teach_helper.py`，確認「一、對答案」三列和動畫面板一樣，「三、對話稿檢查」7/7。
- 讀一遍 `04_解答.md`。

## 學生（爸爸）的原則

- 認真當學生：可以問「為什麼？」「如果……會怎樣？」，也可以故意說出附錄 D 的一條迷思，讓老師修正。
- 驗收三件事：孩子能不用看稿說出核心原理；能用動畫示範並說出出處（檔名、#代號、章名）；能指出至少一個錯誤、限制或注意事項。

## 誠實說明

- 動畫第 1 章的數字（C_Σ 約 77.5 fF、E_J/h 15 GHz、f₀₁ 5.21 GHz）是學程的範例參數；面板寫明「實際尺寸 數百 μm（示意，未按比例）」。
- 十字板發光後變暗的速度是示意放慢（動畫時間常數 6 秒）；真實 T₁ 約 100 μs（師生對話紀錄的範例值）。
- teach_helper.py 照動畫的程式重算面板數字，結果和動畫一樣，但它檢查的是同一個簡化模型（E_J 固定 15 GHz），不是某台真實晶片。
- 「對話稿檢查」只檢查格式（五個部分、出處、三題解答），不會判斷內容對不對；內容要爸爸和孩子對照教學紀錄。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：挑一課、改寫、錄音（約 40 分鐘）

1. 打開 `03_十三課選課表.csv`（或列印包第 1 頁下方），挑一課；在教學紀錄找到那一課，讀完「學習目標」「師生對話」「重點整理」。
2. 用瀏覽器開 `animations/transmon-3d.html`，在畫面最下方的章節列點選對應的章（例如第 6 課讀取 → 第 5 章；第 7 課 BV → 第 9 章）。
3. 照 `06_自編對話模板.md` 寫：課名、學習目標、四到八句師生對話（保留學生原本的問法；老師先讓學生猜、再修正觀念）、重點整理、動畫演示（寫出檔名＋#代號＋章名與要按的按鈕）。
4. 排練一次再錄音：孩子當老師、爸爸當學生，邊講邊操作動畫。

## 下半場：出三題、上台（約 30 分鐘＋10 分鐘）

1. 出三題：一題計算、一題為什麼、一題改錯（從附錄 D 挑一條迷思改寫），每題都寫解答。
2. 想出「如果改掉一個數字會怎樣？」的題目：開 `transmon-3d.html#capacitor`，拖 C_Σ 滑桿；或改 `teach_helper.py` 的 `MY_C`，跑程式拿題目和解答。
3. 把整份對話貼進 `teach_helper.py` 的 `MY_LESSON`，執行 `python teach_helper.py`，看「三、對話稿檢查」是不是 7/7。
4. 角色互換：孩子不看稿，教爸爸怎麼操作動畫、背後的原理是什麼。
5. 錄音總結：回答列印包第 3 頁的錄音四問；替作品取名字、存一個版本（例如「v1」）。
''',
}

FILES.update({
'teach_helper.py': PROGRAM,
'06_自編對話模板.md': TEMPLATE_MD,

'04_解答.md': '# 解答（爸爸用）\n\n## 示範：第 2 課（Transmon 怎麼寫入狀態）\n\n'
  '- 五個零件：十字電容板（約 77.5 fF）、SQUID（兩個約瑟夫森結圍成迴路）、XY 驅動線、Z 磁通線、讀取共振腔（約 7 GHz）＋饋線。\n'
  '- 關鍵句：SQUID 不負責寫入，XY 線送 f₀₁（5.21 GHz）的微波脈衝才是寫入；SQUID 的兩個身分是非線性電感與頻率旋鈕。\n'
  '- 三題練習範例：① 計算：|0⟩ 寫成 (|0⟩+|1⟩)/√2 → 脈衝面積做成 π/2（轉 90°）。'
  '② 為什麼：十字電容為什麼不能太小也不能太大？→ 太小 E_J/E_C 低、怕電荷雜訊；太大非諧性變小、脈衝容易漏到 |2⟩，閘要放慢。'
  '③ 改錯：「SQUID 負責把狀態寫進位元」→ 寫入靠 XY 線的微波脈衝。\n'
  '\n## 十三課對照（課程地圖與附錄 A）\n\n| 課 | 主題 | 動畫 |\n|---|---|---|\n'
  + ''.join(f'| {a} | {b} | {c} |\n' for a, b, c in LESSONS13)
  + '\n## teach_helper.py 實跑（Python 3.13.18）\n\n```\n' + RUN_OUTPUT + '```\n\n'
  '- 「一」三列和 transmon-3d.html#capacitor 面板一模一樣（製作時用瀏覽器實際讀過面板）。\n'
  '- 電容越小，E_C 越大、E_J/E_C 越小：位元頻率變高，但電荷色散（對電荷雜訊的敏感度）急速變大；電容越大則非諧性變小。\n'
  '- 滑桿每格 0.5 fF，判斷是「transmon 區間」（20 ≤ E_J/E_C ≤ 120）的範圍是 26.0–154.5 fF。\n'
  '- 改 MY_C 時，記得題目要寫「動畫的範例模型」，不是真實晶片的規格。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載整個資料夾後用瀏覽器開啟，不需要伺服器或帳號（transmon-3d 需 three.js：資料夾內附 lib/three-r128.min.js，沒有時會連網下載）。

## `transmon-3d.html`：十二章章節列

- 畫面最下方是十二章的章節按鈕（01 晶片 … 012 軟體堆疊）；左右方向鍵也能換章。網址後加 `#代號`（例如 `#readout`）可直接開到那一章。
- 第 5 章起，左上角有字幕跟著導覽步驟逐句說明；多數章節最後一步是「自由實驗」。

## 第 1 章 `#chip`：晶片總覽

- 標籤：十字電容板 C_Σ、SQUID：兩個約瑟夫森結、讀取共振腔 ~7 GHz、饋線、XY 驅動線、Z 磁通線、接地面（Al）、基板（矽 / 藍寶石）。
- 「送出 π 脈衝」：青色光點沿 XY 線送到十字板，十字板發光代表 |1⟩，再慢慢衰減回 |0⟩（示意放慢）。「顯示標籤」可以關掉標籤，用來考爸爸。

## 第 1 章 `#capacitor`：大十字電容的作用

- C_Σ 滑桿（5–200 fF）：十字板粗細跟著變；面板顯示 E_C、E_J/E_C、f₀₁、非諧性 α、電荷色散與判斷。「回到 77.5 fF」按鈕；「電場線」「手臂用途」勾選框。

## 操作

滑鼠拖曳旋轉、滾輪縮放。引用畫面時，請寫出檔名、#代號與章名，例如「transmon-3d.html#chip 第 1 章 晶片」。
''',
})

SHEET_HEADER = ['課', '主題', '對應動畫章', '我想教？（○）', '我要用的比喻', '我要考的迷思（附錄 D）']
SHEET_ROWS = [[a, b, c, '', '', ''] for a, b, c in LESSONS13]

EXTRA_CSS = '''table.judge td{height:13mm;font-size:11pt}table.judge td.k{font-weight:bold;color:#0b2540;width:22%}
table.rec td{height:8mm;font-size:10pt}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
pre.code{font-size:9pt;background:#f2f6fa;border:1pt solid #cfdde8;padding:3mm;margin:2mm 0;white-space:pre-wrap}'''


def check_program():
    """真的跑一次 teach_helper.py（隔離模式），確認輸出和影片、教材寫的結果一致。"""
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / 'teach_helper.py'
        p.write_text(PROGRAM, encoding='utf-8')
        out = subprocess.run([sys.executable, '-I', str(p)], capture_output=True, text=True, check=True,
                             env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}).stdout
    assert out == RUN_OUTPUT, out
    return out


def html():
    tpl_rows = [('課名', '第＿課'), ('學習目標', ''), ('學生問', ''), ('老師答', '（先讓學生猜）'), ('學生問', ''), ('老師答', '（用一個比喻）'),
                ('重點整理', ''), ('動畫演示', '檔名＋#代號＋章名：')]
    pages = [
        '<h2>自編對話模板</h2><p class="lead">挑十三課其中一課，照教學紀錄「每一課的固定結構」寫成自己的師生對話；你當老師，爸爸當學生。</p>'
        '<table class="judge">' + ''.join(f'<tr><td class="k">{a}</td><td>{b}</td></tr>' for a, b in tpl_rows) + '</table>'
        '<p class="note">十三課對照：1–2 課 → 第 1 章；3–4 課 → 第 6 章；5 課 → 第 3、4 章；6 課 → 第 5 章；7 課 → 第 9 章；8–9 課 → 第 7 章；'
        '10 課 → 第 8 章；11 課 → 第 10 章；12 課 → 第 11 章；13 課 → 第 12 章</p>',
        '<h2>三題課後練習出題卡</h2><p class="lead">三種題型各一題，每題都要寫解答；解答先摺起來，讓爸爸先想。</p>'
        '<table class="judge"><tr><th style="width:18%">題型</th><th style="width:44%">題目</th><th style="width:38%">解答</th></tr>'
        '<tr><td class="k">計算</td><td></td><td></td></tr><tr><td class="k">為什麼</td><td></td><td></td></tr>'
        '<tr><td class="k">改錯（附錄 D）</td><td></td><td></td></tr></table>'
        '<pre class="code">MY_C = 40          # 改造區 1：你想考爸爸的電容值（fF；動畫滑桿 5–200，每格 0.5）\nMY_LESSON = &#39;&#39;&#39; ... &#39;&#39;&#39;   # 改造區 2：貼上你的自編對話（每行「標記：內容」）</pre>'
        '<p class="note">「如果改掉一個數字會怎樣？」在 transmon-3d.html#capacitor 拖 C_Σ：20 fF 時判斷＿＿＿＿＿＿＿＿；200 fF 時判斷＿＿＿＿＿＿＿＿</p>',
        '<h2>錄音四問與三個容易錯的地方</h2><div class="box"><p>1. 這一課在解決什麼？</p><div class="line"></div>'
        '<p>2. 我怎麼做？</p><div class="line"></div><p>3. 哪裡容易錯？</p><div class="line"></div>'
        '<p>4. 生活中或真實的量子電腦哪裡會用到？</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><ul class="chk">'
        '<li>引用動畫畫面卻沒寫出處：要寫檔名、#代號、章名</li>'
        '<li>把動畫的範例或示意數字當成真實晶片的實測</li>'
        '<li>只照念原文：要保留學生的問法，再用自己的話和比喻解釋</li></ul></div>',
        '<h2>最後一關：換你上台</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　版本：＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 我教的是第＿＿課，核心原理一句話：</p><div class="line"></div>'
        '<p>2. 我用的動畫（檔名＋#代號＋章名）：</p><div class="line"></div>'
        '<p>3. 一個錯誤、限制或注意事項：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><ul class="chk">'
        '<li>完成自編師生對話一課（五個部分都有）</li><li>不看稿說出核心原理</li>'
        '<li>用動畫示範，並說出出處</li><li>三題練習都有解答；teach_helper.py 對話稿檢查 7/7</li>'
        '<li>錄音總結、替作品命名、存一個版本</li></ul></div>',
    ]
    return printpack.document('Q112 自編對話一課 列印包', '父子科技學院 量子電腦學程 Q112｜模組發表：換你當老師', pages, EXTRA_CSS)


if __name__ == '__main__':
    check_program()
    classroom_pack.build(
        slug='q112-teach-back', folder='Q112_模組發表_換你當老師', files=FILES,
        sheet=('03_十三課選課表.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_自編對話一課.pdf', pack_pages=4,
        pack_needles=('自編對話模板', '出題卡', 'MY_C', 'MY_LESSON', '錄音四問', '容易錯', '最後一關'),
        authoring_dir=XINEW / 'authoring/q112', episode_dir='specials/q112-teach-back',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'no（瀏覽器開動畫；teach_helper.py 只需 Python 3）',
               'program': 'teach_helper.py', 'testedWith': 'Python 3.13.18 (standard library only)',
               'recordedRun': {'capacitorPanel': {'20fF': {'EC': '969 MHz', 'ratio': 15.5, 'f01': '9.69 GHz', 'alpha': '−1.33 GHz'},
                                                  '77.5fF': {'EC': '250 MHz', 'ratio': 60.0, 'f01': '5.21 GHz', 'alpha': '−283 MHz'},
                                                  '200fF': {'EC': '96.8 MHz', 'ratio': 154.9, 'f01': '3.31 GHz', 'alpha': '−104 MHz'}},
                               'matchesAnimationPanel': True, 'transmonRangeFF': [26.0, 154.5],
                               'myC40': {'ratio': 31.0, 'f01': '7.10 GHz'}, 'lessonCheck': '7/7'},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q112/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')
