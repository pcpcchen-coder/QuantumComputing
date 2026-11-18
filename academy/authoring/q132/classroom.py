"""Q132 課堂教材：雜訊預算表底稿、分貝換算、基準測試題卡、濾波器擋不住的雜訊比較表、說明卡與解答。

不需要帳號或安裝；只要紙筆和計算機（或瀏覽器打開 animations/power1000.html#ground 對照）。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q132/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 供電鏈（文獻回顧 §3.1.2）：(級, 這一級做什麼, 主要的雜訊問題)
STAGES = [
    ('1 市電＋雙轉換 UPS', '不能中斷、不能驟降', '中斷與驟降：偏壓一跳就要重新校準'),
    ('2 AC-DC 前端', '交流變直流（PFC 切換）', 'Y 電容漏電流 → 地電位差'),
    ('3 隔離 DC-DC（數位、類比各一顆）', '隔離、降壓', '數十 mV 漣波（數百 kHz–MHz）；隔離電容 → 共模電流'),
    ('4 線性穩壓 LDO', '壓低差模漣波', 'PSRR：1 kHz 約 60–80 dB，1 MHz 常只剩 20–40 dB（典型值）'),
    ('5 電壓基準＋20-bit DAC＋放大器', '產生精密電壓', '電壓基準溫漂（LTZ1000 0.05 ppm/°C）'),
    ('6 π 型 100 Hz 低通濾波 → 冷凍機', '最後一道濾波', '只擋差模；擋不住共模、近場、熱漂移'),
]
DB = [(6, '約 1/2'), (10, '約 1/3.16'), (20, '1/10'), (30, '約 1/31.6'), (40, '1/100'), (60, '1/1,000'), (80, '1/10,000')]
QUIZ = [  # (裁判的題目, 參考答案)
    ('漣波 20 mVpp，經過一級 LDO（30 dB），剩多少？過關嗎？', '20 mV ÷ 31.6 ≈ 632 µVpp，超過 500 µVpp，不過關（文獻回顧的推論例子）。'),
    ('上一題再加一級 20 dB 的濾波，剩多少？', '632 ÷ 10 ≈ 63 µVpp，過關（20 dB 這一級是練習假設）。'),
    ('漣波改成 50 mVpp，同一顆 LDO（30 dB），還要再加多少 dB？', '50 ÷ 31.6 ≈ 1.58 mVpp；要壓到 500 µVpp 以下，至少再多 10 dB 以上。'),
    ('同一顆 LDO 在 1 kHz 有 60 dB，20 mVpp 剩多少？', '60 dB = 1/1,000 → 20 µVpp，過關。所以頻率越高越難擋。'),
    ('隔離電容 100 pF、48 V 在 20 ns 內切換，共模尖峰多大？輸出端濾波器擋得住嗎？', 'I = C·dV/dt ≈ 0.24 A（推論估算）；擋不住，它走地線與屏蔽層。'),
    ('換成隔離電容 10 pF 的模組，尖峰變多少？', '約 0.024 A，變成十分之一（電流和電容成正比）。'),
]
NOISE = [  # (雜訊, 怎麼來, 後端濾得掉嗎, 要靠什麼)
    ('差模漣波', '交換式電源輸出數十 mV', '可以，但要算預算', '多一級濾波或穩壓'),
    ('共模電流', '隔離電容 × 電壓變化率（100 pF × 48 V／20 ns ≈ 0.24 A，推論）', '不行：走地線與屏蔽層', '低隔離電容的隔離 DC-DC'),
    ('近場耦合', 'DC-DC 電感離電壓基準只有數公分；切換頻率會飄', '不行', '低漏磁、屏蔽、鎖 10 MHz 參考時脈'),
    ('熱漂移', '前級損耗改變機箱溫度；熱電動勢 µV/°C 等級', '不行：低於 0.1 Hz', '效率、散熱位置、恆溫'),
    ('中斷與驟降', '市電斷、電壓掉', '不是濾波問題', '保持時間＋雙轉換 UPS'),
    ('漏電流', 'AC-DC 前端的 Y 電容漏到地線，上百台加總', '不是濾波問題', '低漏電流設計、集中供電'),
]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q132：精密 DC 源與雜訊預算（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。今天是「基準測試」：孩子當計算員，沿供電鏈填一張雜訊預算表；你當裁判，拿基準規格（< 500 µVpp）判定過關或超標，還可以改題目。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 精密直流源的規格、供電鏈四關、差模漣波逐級衰減 | 影片第 3–7 段、列印包第 1 頁 |
| 25–65 | 填雜訊預算表；裁判出題、判定 | 列印包第 1、2 頁、`03_雜訊預算表.csv` |
| 65–75 | 休息 | |
| 75–105 | 找出濾波器擋不住的雜訊 | 列印包第 3 頁 |
| 105–115 | 孩子教爸爸：差模漣波怎麼逐級衰減 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 列印 `02_列印包_雜訊預算.pdf`（A4，共 4 頁），準備計算機。
- 讀一遍 `04_解答.md`。想看動畫的話，用瀏覽器開 `animations/power1000.html#ground` 與 `animations/peripherals.html#electronics`。

## 裁判的原則

- 基準只有一個：最後一級的差模漣波 < 500 µVpp（QPower 論文的漣波規格）。
- 改題時一次只改一個數字（漣波大小、PSRR、多加的那一級），讓孩子看出是哪個數字讓結果過關或超標。
- 超標不扣分：請孩子在預算表上標出「哪一級要加強」。

## 誠實說明

- QPower 規格來自學程文獻回顧摘錄的論文數字（arXiv:2505.00297），原文本次未重新開啟。
- 論文沒有公開前級規格。「20 mVpp × 30 dB ≈ 632 µVpp」「PSRR 典型值」「共模尖峰 0.24 A」都是學程文件依架構推論的估算，不是量測。
- 本課的「再加一級 20 dB」是練習用的假設數字。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：沿供電鏈填雜訊預算表（約 40 分鐘）

1. 看列印包第 1 頁的供電鏈六級，先說出每一級在做什麼。
2. 從「隔離 DC-DC 輸出 20 mVpp 漣波」開始，往下一級一級填：上一級送進來多少、這一級衰減幾 dB、這一級自己加多少、輸出多少。
3. 用分貝換算表：每 20 dB，電壓變十分之一。30 dB 約是 1/31.6。
4. 最後一級的輸出和基準（< 500 µVpp）比，過關打勾、超標打叉。
5. 裁判出題（列印包第 2 頁），孩子算完寫在 `03_雜訊預算表.csv`。

## 下半場：找出濾波器擋不住的雜訊（約 30 分鐘）

1. 在列印包第 3 頁的表格，為每一種雜訊寫：怎麼來、輸出端濾波器擋得住嗎、要靠什麼。
2. 算一次共模尖峰：I = C × 電壓變化 ÷ 時間。100 pF、48 V、20 ns。
3. 想一想：為什麼這些雜訊要在「前一級電源」就處理？

## 動畫對照（選做）

- `animations/power1000.html#ground`：勾「量子等級隔離 DC-DC」看共模尖峰；勾「機櫃集中供電」看地電位差。
- `animations/power1000.html#overview`：點紅色 4 號痛點（精密直流）。
- `animations/peripherals.html#electronics`：控制電子機櫃裡的 DC 電流源（磁通偏壓）。
''',

'04_解答.md': '# 解答（爸爸用）\n\n## 供電鏈六級\n\n| 級 | 做什麼 | 主要的雜訊問題 |\n|---|---|---|\n'
  + ''.join(f'| {a} | {b} | {c} |\n' for a, b, c in STAGES)
  + '\n## 差模漣波預算（推論例子）\n\n| 級 | 進來 | 衰減 | 輸出 | 和基準比 |\n|---|---|---|---|---|\n'
  '| 隔離 DC-DC | — | — | 20 mVpp | — |\n'
  '| LDO（約 1 MHz 處 30 dB） | 20 mVpp | 30 dB（÷31.6） | 約 632 µVpp | 超標 |\n'
  '| 再加一級濾波（練習假設 20 dB） | 632 µVpp | 20 dB（÷10） | 約 63 µVpp | 過關 |\n'
  '\n各級「自己加多少」本課不給數字（論文沒有公開前級規格），填「未知」並說明即可。\n\n'
  + '## 分貝換算（電壓）\n\n' + ''.join(f'- {d} dB → {r}\n' for d, r in DB)
  + '\n## 基準測試題卡參考答案\n\n' + ''.join(f'- **{q}** {a}\n' for q, a in QUIZ)
  + '\n## 濾波器擋不住的雜訊\n\n| 雜訊 | 怎麼來 | 後端濾得掉嗎 | 要靠什麼 |\n|---|---|---|---|\n'
  + ''.join('| ' + ' | '.join(r) + ' |\n' for r in NOISE)
  + '\n## 常見誤解\n\n'
  '- 「最後加一個濾波器就好」：差模漣波可以，但共模電流、近場耦合、熱漂移會繞過或低於濾波器的頻段。\n'
  '- 「每台儀器都合規格，整套就合格」：QPower 論文自己提醒，串擾和接地迴路會讓整體變差。\n'
  '- 「前級電源只要便宜可用」：前級電源的規格（隔離電容、切換頻率、漏電流、熱）會影響後面所有精密儀器。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路、伺服器或帳號。

## `animations/power1000.html#ground`（接地與共模）

- 滑桿：交流入口（儀器台數）、每台漏電流、接地阻抗、隔離 DC-DC 的隔離電容。
- 勾選：機櫃集中供電（每櫃一個交流入口）、量子等級隔離 DC-DC（隔離電容 ≤ 10 pF）。
- 中間黑框：地線電流、地電位差、每顆 DC-DC 的共模尖峰（I = C·dV/dt，48 V／20 ns 估算）。

## `animations/power1000.html#overview`（全景）

- 乾淨匯流排接控制電子、精密直流 ×110 台、時脈與網路。點紅色 4 號看「2,500–3,000 路精密直流」的說明。

## `animations/peripherals.html#electronics`（控制電子學）

- 機櫃九個模組；「DC 電流源（磁通偏壓）」的淡綠色小球持續流進冷凍機；最上面是 10 MHz 參考時脈。

## 操作

`H` 隱藏面板；左右方向鍵換場景；空白鍵暫停。
''',
}

SHEET_HEADER = ['題目', '起始漣波（mVpp）', '各級衰減（dB）', '最後輸出（µVpp）', '基準 < 500 µVpp：過關／超標', '要加強哪一級']
SHEET_ROWS = [[f'題目 {i}', q] for i, (q, _) in enumerate(QUIZ, 1)] + [['自訂題目 1', ''], ['自訂題目 2', '']]

EXTRA_CSS = '''table.bud td{height:12mm}table.bud th,table.bud td{font-size:10.5pt}
.dbt{display:grid;grid-template-columns:repeat(7,1fr);gap:2mm;margin-top:3mm;font-size:11pt;text-align:center}
.dbt div{border:1.2pt solid #0b2540;border-radius:2mm;padding:1.5mm}.dbt b{display:block;color:#35a9d6}
.quiz{display:grid;grid-template-columns:1fr 1fr;gap:4mm;margin-top:3mm}
.qc{border:1.4pt dashed #0b2540;border-radius:3mm;padding:3mm 4mm;min-height:52mm;font-size:12pt}.qc b{color:#35a9d6}
table.rec td{height:17mm}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}'''


def html():
    rows = ''.join(f'<tr><td>{a}</td><td></td><td></td><td></td><td></td></tr>' for a, *_ in STAGES)
    dbt = ''.join(f'<div><b>{d} dB</b>{r}</div>' for d, r in DB)
    quiz = ''.join(f'<div class="qc"><b>題目 {i}</b><br>{q}<br><br>我的答案：<div class="line"></div><div class="line"></div>過關 □　超標 □</div>'
                   for i, (q, _) in enumerate(QUIZ, 1))
    pages = [
        '<h2>雜訊預算表（底稿）</h2><p class="lead">沿供電鏈一級一級填。從隔離 DC-DC 輸出 20 mVpp 開始，最後和基準 &lt; 500 µVpp 比。</p>'
        '<table class="bud"><tr><th>級</th><th>上一級送進來</th><th>這一級衰減（dB）</th><th>這一級自己加</th><th>輸出</th></tr>'
        f'{rows}</table>'
        f'<h3 style="margin-top:4mm">分貝換算（電壓）</h3><div class="dbt">{dbt}</div>'
        '<p class="note">口訣：每 20 dB，電壓變十分之一。論文沒有公開前級規格，「自己加多少」不知道就寫「未知」。</p>',
        f'<h2>基準測試題卡</h2><p class="lead">裁判（爸爸）讀題目，計算員（你）算出最後輸出，再和基準比。</p><div class="quiz">{quiz}</div>',
        '<h2>換你改造：濾波器擋不住的雜訊</h2><p class="lead">每一種雜訊寫：怎麼來、輸出端濾波器擋得住嗎、要靠什麼。</p>'
        '<table class="rec"><tr><th>雜訊</th><th>怎麼來</th><th>濾波器擋得住嗎</th><th>要靠什麼</th></tr>'
        + ''.join(f'<tr><td>{r[0]}</td><td></td><td></td><td></td></tr>' for r in NOISE) + '</table>'
        '<p class="note" style="margin-top:4mm">算一算共模尖峰：I = C × 電壓變化 ÷ 時間 = 100 pF × 48 V ÷ 20 ns ＝ ＿＿＿＿＿ A</p>',
        '<h2>說明卡：我的雜訊預算表</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 精密直流源要多安靜？（寫出一個規格）</p><div class="line"></div><p>2. 差模漣波怎麼一級一級變小？</p><div class="line"></div><div class="line"></div>'
        '<p>3. 一個限制或容易錯的地方：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出精密直流源的一個規格（例如漣波 &lt; 500 µVpp）</li><li>解釋 PSRR 為什麼頻率越高越小</li>'
        '<li>用口訣算一次：20 mVpp 經過 30 dB 剩多少</li><li>說出一種濾波器擋不住的雜訊，以及它怎麼繞過去</li>'
        '<li>替預算表取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q132 雜訊預算 列印包', '父子科技學院 量子電腦學程 Q132｜精密 DC 源與雜訊預算', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q132-dc-noise-budget', folder='Q132_雜訊預算', files=FILES,
        sheet=('03_雜訊預算表.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_雜訊預算.pdf', pack_pages=4,
        pack_needles=('雜訊預算表', '分貝換算', '基準測試題卡', '擋不住', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q132', episode_dir='specials/q132-dc-noise-budget',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'stages': len(STAGES), 'quizCards': len(QUIZ), 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q132/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')
