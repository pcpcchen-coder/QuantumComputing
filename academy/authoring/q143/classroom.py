"""Q143 課堂教材：11 張項目卡、項目依賴圖底稿、時間機器檢查卡、完成判準工作單、說明卡與解答。

不需要帳號或安裝；只要紙筆（或瀏覽器打開 animations/power1000.html#devplan 對照）。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q143/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 項目卡：(編號, 名稱, 階段, 第一步, 完成判準) — 依 docs/我們量子供電產品開發計畫.md（規劃建議，非既有計畫）
ITEMS = [
    ('①', '分層 UPS＋精密空調參考設計', '0–1 年', '取得場地規劃文件；量一次壓縮機啟動波形', '示範場域經過一次市電中斷，冷凍機溫度不離開運轉範圍'),
    ('②', '現場勘查服務', '0–1 年', '買齊儀器，先量自己的 UPS、變頻器、變壓器', '報告格式定案；累積 3 個場域的數據'),
    ('③', '量子等級電源規格（QGP）與量測台', '0–1 年', '先定量測方法，門檻值後補', '同一顆電源重複量測一致；一家儀器廠採用'),
    ('④', '壓縮機變頻驅動', '1–3 年', '借一台壓縮機做外掛驗證', '啟動電流下降、冷卻功率無退化；一家 OEM 簽共同開發'),
    ('⑤', '量子等級隔離 DC-DC 與 AC-DC', '1–3 年', '用 QGP 量測台量現有醫療級模組', 'QGP 量測優於醫療級；一家儀器廠裝機回報改善'),
    ('⑥', '集中供電＋接地電流監測 PDU', '1–3 年', 'PDU 先做（不需儀器廠配合）', '抓到一次「接地電流變化 ↔ 量測異常」的時間對應'),
    ('⑦', '精密線圈電流源', '1–3 年', '做 20 A 原型交給原子物理實驗室', '實驗室量到同調時間改善；一家系統廠索樣'),
    ('⑧', '4 K 低溫電源轉換', '3–7 年', '和學研合作量元件的低溫特性', '小功率原型在 4 K 恆溫器中展示'),
    ('⑨', '高通道數直流供電', '3–7 年', '作為 ⑥ 的第二代，不單獨立項', '與一家儀器廠完成共同設計'),
    ('⑩', '模組化量子資料中心配電', '3–7 年', '把 ① 每個案子的設計模組化', '需求出現時已有可複製的設計'),
    ('⑪', '解碼機櫃供電與液冷', '3–7 年（可提前）', '量現有 AI 機櫃電源的磁場與漏電流', '定出與量子機台的最小距離與應用指南'),
]
EDGES = [  # (提供成果, 靠它的項目, 提供什麼) — 開發計畫 §0、簡報 p61、動畫 FEEDS
    ('②', '①', '實測數據'), ('②', '⑩', '實測數據'), ('②', '⑪', '量測方法'),
    ('③', '⑤', '規格與驗證'), ('③', '⑥', '規格與驗證'), ('③', '⑦', '規格與驗證'), ('③', '⑨', '規格與驗證'),
    ('①', '⑩', '可複製的設計'), ('④', '①', '群控、UPS 容量'), ('④', '⑩', '群控'),
    ('⑤', '⑥', '模組入口隔離'), ('⑤', '⑨', '隔離電源'), ('⑥', '⑨', '背板架構'), ('⑧', '⑨', '低溫化介面'), ('⑧', '⑩', '成果回饋'),
]
CHECKS = [  # (時間機器撥到, 檢查的問題, 答案否定時) — 開發計畫 §13
    ('第 6 個月', '取得至少一家廠商的場地規劃文件了嗎？QGP 量測台量得出產品差異嗎？', '調整夥伴策略；量測台雜訊底不夠就先解決它'),
    ('第 12 個月', '示範場域運轉了嗎？勘查找到可對應到產品的問題嗎？', '若找不到問題，重新評估 ⑤、⑥ 的必要性'),
    ('第 18 個月', '有儀器廠或冷凍機廠願意共同開發嗎？', '第二階段縮小到只做 PDU 與參考設計'),
    ('第 36 個月', 'OEM 有設計導入嗎？低溫 CMOS 與模組化冷凍機進度如何？', '決定第三階段各項的投入規模'),
]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q143：三階段路線圖與 11 個開發項目（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。今天的好玩機制是「時間機器」：孩子當規劃師，用 11 張項目卡排出項目依賴圖；你操作時間機器，撥到第幾個月、宣布檢查結果。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 三階段路線圖、依賴關係、啟動順序、檢查點 | 影片第 3–8 段、列印包第 1 頁 |
| 25–65 | 排項目依賴圖；爸爸撥時間機器、宣布檢查結果 | 列印包第 1、2 頁、`03_時間機器紀錄.csv` |
| 65–75 | 休息 | |
| 75–105 | 挑一個項目，寫出完成判準 | 列印包第 3 頁 |
| 105–115 | 孩子教爸爸：為什麼 ②③ 最先做、路線圖為什麼不是承諾 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 列印 `02_列印包_項目依賴圖.pdf`（A4，共 4 頁），剪下第 1 頁的 11 張項目卡；準備色筆兩支（建議：黑＝依賴箭頭、紅＝檢查點）。
- 讀一遍 `04_解答.md`。想看動畫的話，用瀏覽器開 `animations/power1000.html#roadmap` 與 `#devplan`。

## 時間機器的原則

- 撥時間要具體：「現在是第 12 個月」，再宣布一個結果（例如示範場域還沒蓋好、沒有廠商願意合作）。
- 請孩子在圖上指出：哪些箭頭斷了、哪些項目要往後挪或縮小。答不出來的地方，就是依賴圖要補畫的地方。
- 結果是遊戲情境，不是實際進度。

## 誠實說明

- 11 個項目與檢查點來自學程文件「我們量子供電產品開發計畫」，作者明寫是**規劃建議，不是既有計畫**；時程是量級估計，規格是假設值。
- 依賴箭頭以文件 §0、簡報第 61 頁與動畫的金框／綠框為準；文件與動畫在個別箭頭上略有差異（例如 ② → ⑪），解答已註明。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：項目依賴圖（約 40 分鐘）

1. 剪下列印包第 1 頁的 11 張項目卡，依階段排成三欄：0–1 年、1–3 年、3–7 年。
2. 在第 2 頁底稿上把卡片貼好，用黑筆畫箭頭：**從提供成果的項目，指向需要它的項目**。至少畫出：② → ①、③ → ⑤⑥⑦⑨、④ → ①⑩、⑥ → ⑨。
3. 依建議啟動順序替卡片標號：②③ → ① → ⑥⑤ → ④⑦ → 第三階段小規模並行（⑪ 可提前）。
4. 用紅筆在時間軸上標出四個檢查點：第 6、12、18、36 個月。
5. 爸爸撥時間機器（第 2 頁的檢查卡），孩子在圖上回答；結果記在 `03_時間機器紀錄.csv`。

## 下半場：寫完成判準（約 30 分鐘）

1. 挑一個項目（建議先挑第一階段的 ①②③ 以外的項目，自己想）。
2. 在第 3 頁寫：要做出什麼、第一步、完成判準。
3. 判準檢查：量得出來嗎？有沒有「誰認可」？下一個靠它的項目能不能接得上？
4. 對照 `04_解答.md` 裡文件寫的判準，比較差在哪裡。

## 動畫對照（選做）

- `animations/power1000.html#devplan`：點項目卡看第一步、困難、完成判準；綠框是需要先有，金框是靠它提供成果；勾「自動導覽」依建議順序播放；拉「時間」看檢查點。
- `animations/power1000.html#roadmap`：三欄路線圖；點卡片跳到對應的痛點場景。
''',

'04_解答.md': '# 解答（爸爸用）\n\n## 11 個項目（規劃建議）\n\n| # | 項目 | 階段 | 第一步 | 完成判準 |\n|---|---|---|---|---|\n'
  + ''.join(f'| {a} | {b} | {c} | {d} | {e} |\n' for a, b, c, d, e in ITEMS)
  + '\n## 依賴箭頭\n\n| 提供成果 | → 靠它的項目 | 提供什麼 |\n|---|---|---|\n'
  + ''.join(f'| {a} | {b} | {c} |\n' for a, b, c in EDGES)
  + '\n說明：② → ⑪ 來自動畫 FEEDS 與文件 §11（用 ② 的方法量 AI 機櫃）；文件 §0 的依賴圖只畫 ② → ①、⑩。\n\n'
  + '## 建議啟動順序\n\n②③（投入最小，大家靠它們的數據）→ ① → ⑥ 的 PDU 與 ⑤ → ④、⑦ → 第三階段小規模合作並行（⑪ 投入很小，可提前到第一階段）。\n\n'
  + '## 四個檢查點\n\n| 時間 | 問題 | 答案否定時 |\n|---|---|---|\n'
  + ''.join(f'| {a} | {b} | {c} |\n' for a, b, c in CHECKS)
  + '\n## 常見誤解\n\n'
  '- 「路線圖寫了 3 年就一定 3 年做完」：路線圖是計畫，不是承諾；時程是量級估計，每個檢查點都要重新評估。\n'
  '- 「同一階段的項目誰先都可以」：要看依賴；②③ 提供數據給其他項目，所以先做。\n'
  '- 「完成判準就是做完原型」：判準要量得出來，最好還有一位外部的人認可（廠商引用、簽約、採用）。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路、伺服器或帳號。

## `animations/power1000.html#roadmap`（三階段路線圖）

- 三欄：0–1 年建立案例與規格、1–3 年進入供應鏈、3–7 年下一代架構；每張卡片下方「→ 看痛點：…」，點卡片跳到對應場景。
- 左邊面板下方：三個先建立的能力（QGP 規格與量測、驗證平台、夥伴生態）。

## `animations/power1000.html#devplan`（開發計畫：11 個項目）

- 點項目卡：右側顯示要做出什麼、第一步、困難與解法、完成判準；白框＝選中，綠框＝需要先有，金框＝靠它提供成果。
- 「自動導覽（依建議啟動順序）」：每 6 秒換一項，順序 ② ③ ① ⑥ ⑤ ④ ⑦ ⑪ ⑧ ⑨ ⑩。
- 「時間」滑桿 0–84 個月：第 12 個月第二階段亮起、第 36 個月第三階段亮起；面板顯示第 6、12、18、36 個月的檢查點問題。

## 操作

`H` 隱藏面板；左右方向鍵換場景；空白鍵暫停。
''',
}

SHEET_HEADER = ['時間機器撥到', '檢查的問題', '爸爸宣布的結果', '哪些箭頭斷了／哪些項目要調整', '答得出來嗎']
SHEET_ROWS = [[a, b] for a, b, _ in CHECKS] + [['自訂 1', ''], ['自訂 2', '']]

EXTRA_CSS = '''.cards{display:grid;grid-template-columns:1fr 1fr 1fr;gap:3mm;margin-top:3mm}
.card{border:1.3pt dashed #0b2540;border-radius:3mm;padding:2mm 3mm;font-size:10.5pt;min-height:22mm}.card b{font-size:13pt;color:#35a9d6}
.lanes{display:grid;grid-template-columns:1fr 1fr 1fr;gap:4mm;margin-top:3mm;height:105mm}
.lane{border:1.3pt dashed #0b2540;border-radius:3mm;padding:2mm 3mm;font-size:11pt;color:#4a6a88}.lane b{color:#0b2540}
.axis{margin-top:4mm;font-size:11pt;color:#0b2540;border-top:1.5pt solid #0b2540;padding-top:2mm;display:flex;justify-content:space-between}
.quiz{display:grid;grid-template-columns:1fr 1fr;gap:3mm;margin-top:3mm}
.qc{border:1.4pt dashed #0b2540;border-radius:3mm;padding:2mm 4mm;min-height:30mm;font-size:11pt}.qc b{color:#35a9d6}
.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}'''


def html():
    cards = ''.join(f'<div class="card"><b>{a}</b> {b}<br><small>{c}</small></div>' for a, b, c, *_ in ITEMS)
    checks = ''.join(f'<div class="qc"><b>撥到{a}</b><br>{b}<br>爸爸宣布：<div class="line"></div>斷掉的箭頭／要調整的項目：<div class="line"></div></div>'
                     for a, b, _ in CHECKS)
    pages = [
        '<h2>項目卡（剪下來）</h2><p class="lead">11 張項目卡；這是學程文件的規劃建議，不是既有計畫。</p>'
        f'<div class="cards">{cards}</div>'
        '<p class="note">提示：同一階段裡誰先做，要看誰提供成果給誰。</p>',
        '<h2>項目依賴圖（底稿）</h2><p class="lead">把卡片貼進三欄，畫箭頭：從提供成果的項目，指向需要它的項目。</p>'
        '<div class="lanes"><div class="lane"><b>0–1 年</b> 建立案例與規格</div><div class="lane"><b>1–3 年</b> 進入供應鏈</div>'
        '<div class="lane"><b>3–7 年</b> 下一代架構</div></div>'
        '<div class="axis"><span>啟動</span><span>第 6 個月</span><span>第 12 個月</span><span>第 18 個月</span><span>第 36 個月</span></div>'
        f'<h3 style="margin-top:3mm">時間機器檢查卡</h3><div class="quiz">{checks}</div>',
        '<h2>換你改造：寫完成判準</h2><p class="lead">挑一個項目，寫出「做完」的樣子。</p>'
        '<div class="box"><p>我挑的項目：＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p><p>要做出什麼：</p><div class="line"></div>'
        '<p>第一步：</p><div class="line"></div><p>完成判準（量得出來）：</p><div class="line"></div><div class="line"></div>'
        '<p>誰會認可（廠商、儀器廠、實驗室）：</p><div class="line"></div>'
        '<p>完成後，哪個項目可以接手？</p><div class="line"></div></div>'
        '<p class="note">檢查：判準量得出來嗎？有人認可嗎？下一個項目接得上嗎？</p>',
        '<h2>說明卡：我的項目依賴圖</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 三個階段各在做什麼？</p><div class="line"></div><p>2. 為什麼 ②③ 最先做？</p><div class="line"></div><div class="line"></div>'
        '<p>3. 一個限制或容易錯的地方：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出三階段：建立案例與規格、進入供應鏈、下一代架構</li><li>解釋依賴：② 提供數據、③ 是電源產品的驗證依據</li>'
        '<li>說出四個檢查點的時間</li><li>指出一個限制：路線圖是計畫，不是承諾，每個檢查點都要重新評估</li>'
        '<li>替依賴圖取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q143 項目依賴圖 列印包', '父子科技學院 量子電腦學程 Q143｜三階段路線圖與 11 個開發項目', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q143-roadmap-11-projects', folder='Q143_三階段路線圖', files=FILES,
        sheet=('03_時間機器紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_項目依賴圖.pdf', pack_pages=4,
        pack_needles=('項目卡', '依賴圖', '時間機器檢查卡', '完成判準', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q143', episode_dir='specials/q143-roadmap-11-projects',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'items': len(ITEMS), 'edges': len(EDGES), 'checkCards': len(CHECKS), 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q143/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')
