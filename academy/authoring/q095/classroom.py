"""Q095 課堂教材：畢業專題製作 — 每日版本紀錄、先預測再對答案的驗證表、展示日評審卡、說明卡與解答。

免安裝、不需帳號：專題用到什麼工具由提案決定；示範驗證只用學程的 animations/operation.html#workflow，用瀏覽器開啟。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q095/classroom.py
"""
from pathlib import Path
from math import comb, sqrt
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 貝爾線路（哈達瑪閘 → 受控反閘 → 量測）重複 N 次，理想情況每次 00 或 11 各一半：二項分布
N = 1000
SIGMA = sqrt(N * 0.25)                       # ≈ 15.8
LO, HI = round(N / 2 - 2 * SIGMA), round(N / 2 + 2 * SIGMA)   # 468–532（約 ±2σ）
P_IN = sum(comb(N, k) for k in range(LO, HI + 1)) / 2 ** N    # ≈ 0.960
assert (LO, HI) == (468, 532) and 0.95 < P_IN < 0.97
# 動畫 12_workflow.js 模擬約 4% 落到 01／10：00 的期望值約 480
ERR = 0.04
E00 = round(N * (1 - ERR) / 2)               # 480
DAYS = 10                                    # 兩週約十個工作天

FILES = {
'00_爸爸先讀.md': f'''# 父子科技學院 量子電腦學程 Q095：畢業專題製作（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。上一堂孩子寫好一頁提案，範圍縮到兩週做得完；今天開始動手做，原則是「每天都留一個能展示的版本」，並替作品加上一個測試或驗證。

需要的工具由提案決定（程式、動畫場景、簡報或短片）。示範驗證只需要瀏覽器：下載學程的 `animations/` 資料夾，開 `operation.html#workflow`。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 每天交付、一天四步、先預測再對答案 | 影片第 3–7 段、`05_動畫導覽.md` |
| 25–65 | 依提案製作，收工前留下能展示的版本 | 列印包第 1 頁、`03_每日版本與驗證紀錄.csv` |
| 65–75 | 休息 | |
| 75–105 | 加一個測試或驗證，故意弄錯一次看測試抓不抓得到 | 列印包第 2 頁 |
| 105–115 | 展示日：孩子實機展示、教爸爸操作與原理 | 列印包第 3–4 頁 |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 和孩子一起把提案拆成約 {DAYS} 個一天做得完的小任務，寫在列印包第 1 頁。
- 準備專題所需工具；列印 `02_列印包_畢業專題製作.pdf`（A4，共 4 頁）。讀一遍 `04_解答.md`。

## 展示日怎麼玩

每天收工前，孩子用三分鐘實際打開作品操作一次，說出完成了什麼、下一步要做什麼。爸爸當評審：只問一個問題，給一個讚美、一個建議，建議寫進明天的任務清單。不能只用嘴巴說「會動」。

## 誠實說明

- 「每天三分鐘」「一個問題、一個讚美、一個建議」是本課的建議做法，可依家裡情況調整。
- 引用他人素材（圖片、音樂、程式、影片）要註明來源與授權；不確定能不能用就不要用——這是本課最重要的注意事項。
''',

'01_操作步驟.md': f'''# 操作步驟

## A. 拆任務（約 10 分鐘）

1. 拿出上一堂的提案，把要做的東西拆成約 {DAYS} 個小任務，每個一天做得完。
2. 排順序：第一天要做出「從頭到尾走得通」的最簡單版本，之後每天加一點。

## B. 今天的一輪（約 40 分鐘）

1. 挑一小塊 → 2. 動手做 → 3. 馬上測試（昨天的功能還正常嗎？）→ 4. 展示＋存版本。
2. 存檔：檔名寫日期與版本號（例如 `專題_v03_日期`），在紀錄表寫一句「今天改了什麼」。

## C. 示範驗證：先預測再對答案（`operation.html#workflow`，約 10 分鐘）

1. 先在列印包第 2 頁寫下預測：線路先做哈達瑪閘、再做受控反閘，重複 {N} 次，00、01、10、11 各大約幾次？
2. 關掉「自動播放」，按「下一站 ▶」一站一站走到「⑤ 晶片執行 shots」，看計數跑到 {N}。
3. 再按一次到「⑥ 判別與結果」，看右邊直方圖，和預測比較。注意：從第六站再按「下一站」會回到第一站並清空。

## D. 下半場：替自己的作品加一個測試（約 30 分鐘）

1. 找一個事先就知道答案的情況（手算、理論、已知特例）。
2. 寫清楚：輸入、預期結果、可以接受的誤差。
3. 故意把作品改錯一個地方，再跑測試；抓得到才算有用。改回來，存一個版本。
''',

'04_解答.md': '# 解答（爸爸用）\n\n## 貝爾線路重複一千次\n\n'
  f'- 理想情況：每次只會得到 00 或 11，機率各一半；01、10 不會出現。\n'
  f'- 重複 {N} 次，00 的次數像擲 {N} 次公正硬幣的正面數：平均 {N // 2}，標準差約 {SIGMA:.1f}。\n'
  f'- 「平均 ± 兩個標準差」約 {LO}–{HI} 次，理想情況下大約 {P_IN * 100:.0f}% 的機會落在裡面——所以偶爾落在外面也不代表作品錯了，可以再跑一次。\n'
  f'- 動畫（和真實機器）有錯誤：動畫約 {ERR * 100:.0f}% 的結果改記成 01 或 10，所以 00 的期望約 {E00} 次。'
  '測試範圍要把錯誤算進去，例如「00 和 11 各在 440–530 之間，01 加 10 不超過 80」，而不是要求 01、10 剛好是零。\n\n'
  '## 三種作品的驗證例子\n\n| 作品 | 已知答案的情況 | 故意弄錯的方式 |\n|---|---|---|\n'
  '| 程式 | 只有一個量子位元、做哈達瑪閘：0 和 1 各一半 | 把哈達瑪閘換成翻轉閘，結果應該變成全部是 1 |\n'
  '| 動畫場景 | 連做兩次翻轉閘，箭頭回到原位 | 只做一次，測試應該報錯 |\n'
  '| 簡報或短片 | 每個事實都有來源欄位 | 拿掉一個來源，檢查表應該抓到 |\n\n'
  '## 常見問題\n\n'
  '- 為什麼不等最後一天再組裝？問題會全擠在同一天；每天都有能動的版本，壞了只要查昨天到今天改了什麼。\n'
  '- 預測可以事後改嗎？不行。先寫下預測與範圍，才是真正的驗證。\n'
  '- 網路上找到的圖可以直接用嗎？要看授權條款，並註明來源；不確定就自己畫。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路或帳號。

## `operation.html#workflow`（操作場景 12：一次量子計算的完整流程）

- 六站：① 寫程式 → ② 轉譯 → ③ 脈衝排程 → ④ 控制電子 → ⑤ 晶片執行 shots → ⑥ 判別與結果。
- 開關「自動播放」：預設開，每站自動前進；按鈕「下一站 ▶」：一次走一站（同時關掉自動前進）。
- 滑桿「shots N」：100–100,000，預設 1000；「線路深度（層）」與開關「主動重置」會改變右下插圖的時間組成。
- 範例程式：`qc.h(0)`、`qc.cx(0, 1)`、`measure_all()`——就是哈達瑪閘加受控反閘的貝爾線路。
- 右邊直方圖：00、11 是金色，01、10 是灰色。

## 操作

`H` 隱藏面板；滑鼠拖曳旋轉、滾輪縮放。
''',
}

SHEET_HEADER = ['日期', '版本號', '今天的一小塊', '測試結果', '展示日：評審的問題', '讚美', '建議（寫進明天）', '今天改了什麼', '用到的外部素材與來源']
SHEET_ROWS = [[f'第 {i} 天', f'v{i:02d}', '', '', '', '', '', '', ''] for i in range(1, DAYS + 1)]

EXTRA_CSS = '''table.rec td{height:9mm}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.card{border:2pt solid #0b2540;border-radius:4mm;padding:5mm;margin-top:5mm}.card h3{margin-top:0}'''


def html():
    pages = [
        '<h2>每日版本紀錄</h2><p class="lead">每天收工前：能打開、能操作，存一個版本，寫一句今天改了什麼。</p>'
        '<table class="rec"><tr><th>天</th><th>版本號</th><th>今天的一小塊</th><th>測試過了嗎</th><th>今天改了什麼</th></tr>'
        + ''.join(f'<tr><td>{i}</td><td>v{i:02d}</td><td></td><td></td><td></td></tr>' for i in range(1, DAYS + 1)) + '</table>'
        '<div class="card"><h3>專題作品（今天的作品）</h3><p>作品名稱：＿＿＿＿＿＿＿＿＿＿　類型：程式／動畫場景／簡報／短片</p>'
        '<p>第一天「走得通」的最簡單版本是：</p><div class="line"></div></div>',
        '<h2>驗證：先預測再對答案</h2><p class="lead">在 operation.html#workflow：哈達瑪閘 → 受控反閘 → 量測，重複 1000 次。先寫預測，再看直方圖。</p>'
        '<table class="rec"><tr><th>結果</th><th>我的預測（次）</th><th>可接受範圍</th><th>動畫的結果</th><th>通過嗎</th></tr>'
        + ''.join(f'<tr><td>{s}</td><td></td><td></td><td></td><td></td></tr>' for s in ('00', '01', '10', '11')) + '</table>'
        '<div class="card"><h3>替我的作品加一個測試</h3><p>已知答案的情況：</p><div class="line"></div>'
        '<p>輸入：＿＿＿＿＿＿　預期結果：＿＿＿＿＿＿　可接受誤差：＿＿＿＿</p>'
        '<p>我故意弄錯的地方：＿＿＿＿＿＿＿＿　測試有抓到嗎？□ 有　□ 沒有</p></div>',
        '<h2>展示日評審卡</h2><p class="lead">每天收工前三分鐘：你實際操作作品，爸爸當評審。</p>'
        '<table class="rec"><tr><th>天</th><th>評審的一個問題</th><th>一個讚美</th><th>一個建議（寫進明天）</th></tr>'
        + ''.join(f'<tr><td>{i}</td><td></td><td></td><td></td></tr>' for i in range(1, 6)) + '</table>'
        '<h3>素材來源表</h3><table class="rec"><tr><th>素材</th><th>來源（網址或作者）</th><th>授權</th></tr>'
        + '<tr><td></td><td></td><td></td></tr>' * 3 + '</table>'
        '<p class="note">生活技能：持續交付——每天砌好一層，比最後一天一口氣堆起來穩當。</p>',
        '<h2>說明卡與最後一關</h2><div class="box"><p>1. 我的專題在解決什麼問題？給誰用？</p><div class="line"></div>'
        '<p>2. 我用到的核心原理：</p><div class="line"></div><p>3. 我怎麼證明成果是對的？</p><div class="line"></div>'
        '<p>4. 一個錯誤、限制或注意事項：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出專題要解決的問題</li><li>不看稿說出核心原理</li>'
        '<li>實際操作今天的版本給爸爸看</li><li>指出一個限制：引用他人素材要註明來源與授權</li>'
        '<li>替專題作品取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q095 畢業專題製作 列印包', '父子科技學院 量子電腦學程 Q095｜畢業專題製作', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q095-capstone-build', folder='Q095_畢業專題製作', files=FILES,
        sheet=('03_每日版本與驗證紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_畢業專題製作.pdf', pack_pages=4,
        pack_needles=('每日版本紀錄', '專題作品', '先預測再對答案', '展示日評審卡', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q095', episode_dir='specials/q095-capstone-build',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'scenes': ['animations/operation.html#workflow'],
               'bellShots': N, 'bellRange2Sigma': [LO, HI], 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q095/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')
