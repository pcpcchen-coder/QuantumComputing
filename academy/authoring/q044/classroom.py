"""Q044 課堂教材：時間機器任務卡、降溫時間軸格（0–36 小時）、換樣品時程規劃表、停電加碼題、說明卡與解答。

不需要帳號、不需要安裝；只要瀏覽器打開學程的 animations/peripherals.html#cooldown（與 power1000.html#outage）。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q044/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 學程簡報 QC_Peripheral_Systems_Talk.pptx 第 12 頁的典型時間（小時）；實際依機型與負載而異
STEPS = [  # (步驟, 最少, 最多, 在等什麼)
    ('① 抽真空／檢漏', 2, 2, '等外真空罩的空氣抽乾，免得氣體把熱帶進來；檢查有沒有漏氣'),
    ('② 脈衝管預冷', 20, 20, '等脈衝管把 50 K、4 K 板冷下來，下面各層跟著降到約 4 K；銅和線越多越久'),
    ('③ 凝結混合氣', 2, 3, '等氦三／氦四混合氣在 4 K 凝結成液體，填進混合腔'),
    ('④ 稀釋循環到基溫', 3, 5, '等稀釋循環把混合腔從約 1 K 拉到約 10 mK'),
]
LO, HI = sum(s[1] for s in STEPS), sum(s[2] for s in STEPS)
assert (LO, HI) == (27, 30)
# 動畫 04_cooldown.js 的階段切點（小時）：①0–2、②2–25、③25–27.5、④27.5–33、33 起基溫穩定（典型示意）
ANIM = [('① 抽真空／檢漏', '0–2'), ('② 脈衝管預冷', '2–25'), ('③ 凝結混合氣', '25–27.5'), ('④ 稀釋循環 → 基溫', '27.5–33'), ('✓ 基溫穩定', '33 以後')]
STOPS = [1, 12, 26, 30, 36]  # 時間機器的五個停靠站（小時）
STOP_ANS = {  # 依動畫模型重算（fact-check.md 的表）
    1: ('① 抽真空／檢漏', '各層都還是 300 K', '空氣抽乾、檢漏'),
    12: ('② 脈衝管預冷', '50 K 板約 86 K、4 K 板約 85 K、下面三層約 107 K', '銅和線的熱被抽走'),
    26: ('③ 凝結混合氣', '下面三層約 6.7 K；畫面有往下落的小亮點', '混合氣凝結成液體'),
    30: ('④ 稀釋循環 → 基溫', '混合腔約 91 mK', '循環把混合腔往下拉'),
    36: ('✓ 基溫穩定，可開始量測', '混合腔約 10 mK', '不用再等，可以量測'),
}
SWAP = [  # 換一次樣品（指南第 7 節＋第 4 節）
    ('停止循環、回收混合氣到儲存槽', '幾小時內（依機型）'),
    ('停壓縮機，升溫回室溫', '1–2 天'),
    ('乾燥氮氣破真空、開罐換晶片、裝回屏蔽', '依實驗室，通常半天內（自己估）'),
    ('抽真空＋預冷＋凝結＋循環', f'{LO}–{HI} 小時（1–2 天）'),
    ('電子學上線、重新校準', '依系統而定（自己估）'),
]

FILES = {
'00_爸爸先讀.md': f'''# 父子科技學院 量子電腦學程 Q044：降溫一次要幾天（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶出今天的任務：稀釋冷凍機從室溫降到約 10 mK 要分四步，各要等多久、在等什麼；再規劃換一次樣品要幾天。

## 只需要瀏覽器

- `animations/peripherals.html#cooldown`（周邊系統 3D 場景 4：降溫流程）：「時間 (小時)」滑桿 0–36、「⏸ 暫停／▶ 播放」、「播放速度」。這就是今天的**時間機器**。
- 加碼：`animations/power1000.html#outage`（斷電時間軸），上方「備援方案」選單。
- 不需要帳號、不需要安裝；下載學程的 `animations/` 資料夾後直接用瀏覽器開啟。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 降溫四步與典型時間；為什麼不能馬上冷 | 影片第 3–7 段、列印包第 1 頁 |
| 25–65 | 時間機器：撥到五個停靠站，讀溫度、說出在等什麼；畫出降溫時間軸 | 動畫、`01_操作步驟.md`、列印包第 1–2 頁 |
| 65–75 | 休息 | |
| 75–105 | 規劃換一次樣品的完整時程（升溫＋降溫）；加碼：停電情境 | 列印包第 3 頁、`03_時程規劃.csv` |
| 105–115 | 孩子教爸爸：四步、為什麼預冷最久、一個限制 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 自己先開一次降溫動畫：按「⏸ 暫停」，把時間滑桿拖到 1、12、26、30、36 小時，看上方階段標籤與右下角曲線。
- 列印 `02_列印包_降溫時間軸.pdf`（A4，共 4 頁）；準備彩色筆（紅、橘、黃、藍）。讀一遍 `04_解答.md`。

## 值班工程師（爸爸）的原則

- 孩子撥到一個時間，先讓他說「現在在等什麼」，再一起看溫度核對。
- 說錯就「倒回去」：把滑桿拉回前一站再看一次，不扣分。
- 動畫的時間尺度是典型示意（面板最下面有寫），真正多久依機型、負載與佈線多寡而定。

## 誠實說明

- 四步的時間（約 2、20、2–3、3–5 小時）取自學程簡報〈量子電腦的周邊系統〉第 12 頁的典型值；動畫的切點略有不同（預冷 2–25 小時），兩者都是示意。
- 升溫回室溫約 1–2 天，依學程《周邊系統連接與啟動指南》第 7 節；動畫副標寫約 1 天。
- 停電數據（約 2 分鐘超過 1 K、重新降溫 2–5 天、最壞約 10 天）由學程供電簡報轉引德國 LRZ 的公開論文，本課未另讀原文。
- 重新校準要多久依系統而定，本課不給數字，請孩子自己估一個並寫下理由。
''',

'01_操作步驟.md': '''# 操作步驟

## 時間機器（約 40 分鐘）

1. 打開 `animations/peripherals.html#cooldown`。場景一打開就會自己播放，先按「⏸ 暫停」。
2. 時光旅人（孩子）把「時間 (小時)」滑桿拖到第一站：1 小時。先說出「現在在第幾步、在等什麼」。
3. 值班工程師（爸爸）讀出面板上的溫度：MXC（混合腔）、4 K 板、50 K 板，也可以看冷凍機右邊每一層的金色溫度標籤。
4. 寫進列印包第 1 頁的停靠站表，再撥到下一站：12、26、30、36 小時。
5. 在列印包第 2 頁的時間軸格上，用顏色把四步塗出來，並在每一段寫一句「在等什麼」。
6. 想看整段播放：按「⟲ 重新開始」，把「播放速度」調到 2（每秒 2 小時），約 18 秒跑完 36 小時。

## 下半場：換一次樣品（約 30 分鐘）

1. 照列印包第 3 頁，依序排出：回收混合氣 → 升溫 → 破真空開罐換晶片 → 降溫 → 校準。
2. 每一段寫下最少、最多要多久；不知道的（例如校準）自己估一個，寫下理由。
3. 算出最快和最慢共幾天，把它畫成一條時間軸，標出哪幾天實驗室「只能等」。

## 加碼：停電（約 5 分鐘）

1. 打開 `animations/power1000.html#outage`。
2. 備援方案選「A：只有控制電子接 UPS」：看金色曲線在「2 分」附近衝過 1 K 的紅色虛線，面板停機時間寫「約 3–5 天」。
3. 改選「B：冷卻鏈 UPS＋發電機接手」：曲線平貼 10 mK，停機時間 0。
''',

'04_解答.md': '# 解答（爸爸用）\n\n## 降溫四步（學程簡報第 12 頁典型值）\n\n| 步驟 | 約多久 | 在等什麼 |\n|---|---|---|\n'
  + ''.join(f'| {n} | ' + (f'{a} 小時' if a == b else f'{a}–{b} 小時') + f' | {w} |\n' for n, a, b, w in STEPS)
  + f'\n加起來：最快 {LO} 小時、最慢 {HI} 小時（約 {LO/24:.2f}–{HI/24:.2f} 天）。簡報備註：空機規格 24 小時內到基溫；大型機台或線多的系統通常一天半到兩天。最久的是預冷，因為要冷的銅和線最多（熱容量大）。\n\n'
  + '## 時間機器停靠站（降溫動畫的模型值，典型示意）\n\n| 時間 | 階段標籤 | 讀到的溫度 | 在等什麼 |\n|---|---|---|---|\n'
  + ''.join(f'| {t} 小時 | {STOP_ANS[t][0]} | {STOP_ANS[t][1]} | {STOP_ANS[t][2]} |\n' for t in STOPS)
  + '\n動畫的階段切點：' + '、'.join(f'{n} {h} 小時' for n, h in ANIM) + '。\n\n'
  + '## 換一次樣品\n\n| 段落 | 約多久 |\n|---|---|\n' + ''.join(f'| {a} | {b} |\n' for a, b in SWAP)
  + '\n只算升溫（1–2 天）＋降溫（1–2 天）就要 2–4 天，再加開罐與校準，所以「換一次樣品常要好幾天」。大型系統會用多台冷凍機輪流測試，就是為了不讓研究整個停下來。\n\n'
  + '## 停電加碼題\n\n- 冷卻中斷約 2 分鐘，晶片就超過 1 K；超過 1 K 校準要整套重做；重新降溫 2–5 天，最壞約 10 天（供電簡報第 7 頁，轉引 LRZ）。\n'
  '- 冷下來要一兩天，熱上去只要幾分鐘：所以 UPS 要涵蓋整條冷卻鏈（壓縮機、氣體處理系統、冰水機泵浦），撐到發電機接手（供電簡報第 8 頁，推論）。\n\n'
  '## 常見錯誤\n\n- 以為冷凍機像冰箱，插電幾分鐘就冷：其實要一到兩天。\n- 只算降溫、忘了升溫：換樣品兩頭都要等。\n- 把動畫的時間當成精確值：動畫面板寫明「時間尺度為典型示意」。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路、伺服器或帳號。

## `animations/peripherals.html#cooldown`（周邊系統 3D 場景 4：降溫流程）

- 「時間 (小時)」滑桿：0–36 小時；「⏸ 暫停／▶ 播放」「⟲ 重新開始」「播放速度（小時/秒）」。
- 冷凍機上方的大字是目前階段：① 抽真空 / 檢漏、② 脈衝管預冷、③ 凝結混合氣、④ 稀釋循環 → 基溫、✓ 基溫穩定，可開始量測。
- 每一層右邊的金色標籤是溫度；顏色從紅（熱）到藍（冷）。凝結階段（25–28 小時）會看到往下落的淡藍色小亮點。
- 右下角小圖：各層溫度隨時間（對數座標），白色直線是現在的時間。
- 面板讀數：外真空罩（OVC）壓力、MXC、4 K 板、50 K 板溫度；最下面註明「時間尺度為典型示意，依機型與負載而異」。

## `animations/power1000.html#outage`（1,000 位元供電設計 場景 5：斷電時間軸）

- 橫軸是對數時間（1 秒到 10 天），金色曲線是混合腔溫度，紅色虛線是 1 K。
- 「備援方案」選單：A 只有控制電子接 UPS、B 冷卻鏈 UPS＋發電機接手、C 冷卻鏈 UPS 但發電機沒起來（可調 UPS 撐幾分鐘）。
- 面板「停機時間（示意）」：A 約 3–5 天、B 0。曲線為教學示意，非實測。

## 操作

`H` 隱藏面板；左右方向鍵換場景；空白鍵暫停；滑鼠拖曳旋轉、滾輪縮放（peripherals.html）。
''',
}

SHEET_HEADER = ['段落', '在等什麼', '最少（小時）', '最多（小時）', '我的估計', '理由', '累計最少', '累計最多']
SHEET_ROWS = ([[n, w, str(a), str(b)] for n, a, b, w in STEPS]
              + [['停止循環、回收混合氣', '', '', ''], ['升溫回室溫', '', '24', '48'], ['破真空、開罐換晶片', '', '', ''],
                 ['再降溫（四步）', '', str(LO), str(HI)], ['重新校準', '', '', '']])

EXTRA_CSS = '''table.rec td{height:10mm}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.tl{position:relative;height:58mm;margin:4mm 0 0 0;border-left:1.2pt solid #0b2540;border-bottom:1.2pt solid #0b2540;
background-image:linear-gradient(90deg,#cfdde8 .6pt,transparent .6pt);background-size:calc(100%/12) 100%}
.tl .lane{position:absolute;left:0;right:0;border-top:.6pt dashed #9fb3c6;font-size:9pt;color:#4a6a88;padding-left:2mm}
.tx{display:flex;justify-content:space-between;font-size:9.5pt;margin:0 -2mm;color:#35506b}
.steps{display:grid;grid-template-columns:repeat(4,1fr);gap:3mm;margin-top:3mm}.steps .box{font-size:11pt;padding:2.5mm 3mm}
.steps b{display:block;font-size:12pt;margin-bottom:1mm}'''


def html():
    steps = ''.join(f'<div class="box"><b>{n}</b>約 ' + (f'{a}' if a == b else f'{a}–{b}') + ' 小時<br>在等：＿＿＿＿＿＿</div>'
                    for n, a, b, _ in STEPS)
    stops = ''.join(f'<tr><td>{t} 小時</td><td></td><td></td><td></td></tr>' for t in STOPS)
    ticks = ''.join(f'<span>{h}</span>' for h in range(0, 37, 3))
    lanes = ''.join(f'<div class="lane" style="top:{y}mm">{t}</div>' for y, t in ((12, '50 K 板'), (26, '4 K 板'), (40, '混合腔')))
    swap = ''.join(f'<tr><td>{i}. {a}</td><td></td><td></td><td></td></tr>' for i, (a, _) in enumerate(SWAP, 1))
    pages = [
        '<h2>時間機器任務卡</h2><p class="lead">打開 peripherals.html#cooldown，先按「⏸ 暫停」，再把「時間 (小時)」撥到每一站。先說「在等什麼」，再讀溫度。</p>'
        f'<div class="steps">{steps}</div>'
        '<h3 style="margin-top:5mm">五個停靠站</h3><table class="rec"><tr><th>撥到</th><th>上方寫第幾步</th><th>混合腔溫度</th><th>現在在等什麼</th></tr>'
        f'{stops}</table><p class="note">時光旅人（你）撥時間、說答案；值班工程師（爸爸）讀溫度、核對。說錯了就倒回去再看一次。</p>',
        '<h2>我的降溫時間軸</h2><p class="lead">用顏色把四步塗在下面的格子上（0–36 小時，每格 3 小時），再畫出三層的溫度大概怎麼往下走。</p>'
        f'<div class="tl">{lanes}</div><div class="tx">{ticks}</div><p class="note" style="text-align:right">時間（小時）</p>'
        '<table class="rec" style="margin-top:3mm"><tr><th>步驟</th><th>從第幾小時</th><th>到第幾小時</th><th>在等什麼（一句話）</th></tr>'
        + ''.join(f'<tr><td>{n}</td><td></td><td></td><td></td></tr>' for n, *_ in STEPS) + '</table>'
        f'<p class="note">加起來：2 ＋ 20 ＋ 2–3 ＋ 3–5 ＝ ＿＿＿ 到 ＿＿＿ 小時。最久的是哪一步？為什麼？＿＿＿＿＿＿＿＿</p>',
        '<h2>換你規劃：換一次樣品</h2><p class="lead">排出完整時程：先升溫、再開罐，最後再降溫。不知道的段落自己估，寫下理由。</p>'
        '<table class="rec"><tr><th>段落</th><th>最少</th><th>最多</th><th>理由</th></tr>' + swap + '</table>'
        '<p style="margin-top:3mm">合計：最快＿＿＿天，最慢＿＿＿天。哪幾天實驗室「只能等」？＿＿＿＿＿＿＿＿</p>'
        '<div class="box" style="margin-top:4mm"><h3>加碼：停電了</h3><p>打開 power1000.html#outage。方案 A：曲線在＿＿＿附近超過 1 K；停機時間約＿＿＿天。方案 B：＿＿＿＿＿＿。</p>'
        '<p>為什麼不斷電系統要顧到整條冷卻鏈？</p><div class="line"></div></div>',
        '<h2>說明卡：我的降溫時間軸</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 降溫有哪四步？</p><div class="line"></div><p>2. 為什麼預冷最久？</p><div class="line"></div><div class="line"></div>'
        '<p>3. 一個限制或容易錯的地方：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出降溫四步：抽真空、預冷、凝結、循環</li><li>說出每一步在等什麼，以及哪一步最久</li>'
        '<li>算出整趟降溫大約幾小時</li><li>指出一個限制：升溫和降溫都要時間，換一次樣品常要好幾天</li>'
        '<li>替時間軸取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q044 降溫一次要幾天 列印包', '父子科技學院 量子電腦學程 Q044｜降溫一次要幾天', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q044-cooldown-days', folder='Q044_降溫一次要幾天', files=FILES,
        sheet=('03_時程規劃.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_降溫時間軸.pdf', pack_pages=4,
        pack_needles=('時間機器任務卡', '五個停靠站', '我的降溫時間軸', '換一次樣品', '停電', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q044', episode_dir='specials/q044-cooldown-days',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'animations': ['animations/peripherals.html#cooldown', 'animations/power1000.html#outage'],
               'cooldownHours': [LO, HI], 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q044/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')
