"""Q091 課堂教材：Shor 之後：後量子密碼 — 動畫操作步驟、家中加密盤點表、安全審查問題卡、NIST 標準查詢表、說明卡與解答。

免安裝、不需帳號：只用學程的 animations/operation.html#shor，用瀏覽器開啟；盤點與查詢用紙筆或試算表。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q091/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 7ˣ mod 15（學程簡報 p41、10_shor.js）：週期 4
POW7 = [pow(7, x, 15) for x in range(9)]
assert POW7[:5] == [1, 7, 4, 13, 1]
H = pow(7, 2, 15)                       # 4
assert (H - 1, H + 1) == (3, 5) and 15 % 3 == 0 and 15 % 5 == 0

# NIST 2024 年 8 月公布的三個後量子密碼標準（維基百科 NIST Post-Quantum Cryptography Standardization）
NIST = [('FIPS 203', 'ML-KEM', '交換金鑰（金鑰封裝）', '格（模組格上的帶誤差學習）', 'CRYSTALS-Kyber'),
        ('FIPS 204', 'ML-DSA', '數位簽章', '格', 'CRYSTALS-Dilithium'),
        ('FIPS 205', 'SLH-DSA', '數位簽章', '雜湊函數（無狀態雜湊簽章）', 'SPHINCS+')]

# 盤點表的預設列（課綱：網銀、密碼管理器、Wi-Fi），其餘由孩子自己加
ITEMS = ['網路銀行（網頁或 App）', '密碼管理器', '家裡的 Wi‑Fi', '手機通訊軟體', '電子郵件', '雲端相簿或硬碟', '', '']

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q091：Shor 之後：後量子密碼（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶出兩個問題：量子電腦夠大時，現在的哪些密碼會被打開？我們要怎麼提早換鎖？

只需要瀏覽器：下載學程的 `animations/` 資料夾，開 `operation.html#shor`。盤點表用列印包或 `03_家中加密盤點表.csv`。不需要帳號或安裝；下半場查標準要能上網。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 公開金鑰靠什麼保密、Shor 四步、資源估計 | 影片第 3–5 段、`05_動畫導覽.md` |
| 25–65 | 安全審查：一起盤點家中用到加密的地方 | `01_操作步驟.md`、列印包第 1–2 頁 |
| 65–75 | 休息 | |
| 75–105 | 孩子獨立查 NIST 後量子密碼標準名稱與用途 | 列印包第 3 頁 |
| 105–115 | 孩子教爸爸：為什麼 Shor 能破解、怎麼換鎖 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 先自己在 `#shor` 按「下一步 ▶」五次，看柱子從一根 → 64 根同高 → 四色 → 梳子 → 四根青色高峰 → 一根變白。
- 列出家裡用到加密的地方（至少網銀、密碼管理器、Wi‑Fi），印出 `02_列印包_後量子密碼.pdf`（A4，共 4 頁）。讀一遍 `04_解答.md`。

## 安全審查怎麼玩

爸爸是「受審者」，孩子是「審查員」。每一項由爸爸說明怎麼用，孩子用列印包第 2 頁的問題卡追問，最後在盤點表上標「會受影響／影響較小／還不確定」。不確定的不要硬猜，寫下要去查什麼。

## 誠實說明

- 盤點只看「用到哪一種鎖」，不登入、不截圖任何帳號，也不要把密碼寫在表上。
- 密碼管理器、Wi‑Fi（WPA2／WPA3）實際用哪種加密，依產品與設定而異；本課只教判斷原則，答案要查產品說明。
- 破解 RSA-2048 的資源估計（2019 約 2000 萬實體位元、2025 不到 100 萬）是研究估計，會隨研究變動。
- 「先存下來、以後再解密」是現在就存在的風險——這是本課最重要的注意事項。
''',

'01_操作步驟.md': '''# 操作步驟

## A. 看 Shor 怎麼找週期（`operation.html#shor`，約 10 分鐘）

1. 按「N = 15」，確認選的是「a = 7」，再按「重設」。右下小圖是 7ˣ mod 15：1、7、4、13 一直重複。
2. 按「下一步 ▶」：64 根柱子同高（x = 0…63 疊加）。
3. 再按：柱子依餘數上四種顏色。
4. 再按：量測第二暫存器，只剩同一種顏色、間隔 4 的「梳子」（哪一種顏色每次不同）。
5. 再按：QFT，四根青色高峰在 0、16、32、48。
6. 再按：量測，一根高峰變白。看左側讀數的連分數與 gcd，找出 15 = 3 × 5。
7. 進階：按「N = 21」再跑一次，高峰沒有那麼尖（教學用暫存器只有 64）。

## B. 安全審查：家中加密盤點（約 30 分鐘）

1. 在列印包第 1 頁列出用途（至少網銀、密碼管理器、Wi‑Fi）。
2. 每一項用第 2 頁的問題卡問三題：有沒有在交換鑰匙？有沒有在確認身分？還是用共用的鑰匙加密資料？
3. 標記「會受影響／影響較小／還不確定」，不確定的寫下要查什麼。

## C. 下半場：查 NIST 後量子密碼標準（約 30 分鐘）

在列印包第 3 頁寫下三個標準的編號、名稱、用途和數學基礎，再對回盤點表：哪一項的哪一步，可以換成哪一個標準。
''',

'04_解答.md': '# 解答（爸爸用）\n\n## Shor 的例子：N = 15、a = 7\n\n| x | ' + ' | '.join(str(x) for x in range(9)) + ' |\n|' + '---|' * 10 + '\n'
  '| 7ˣ mod 15 | ' + ' | '.join(str(v) for v in POW7) + ' |\n\n'
  f'週期 r = 4；7² mod 15 = {H}；gcd({H} − 1, 15) = 3、gcd({H} + 1, 15) = 5 → 15 = 3 × 5。\n'
  'QFT 後的高峰在 64k/4 = 0、16、32、48；量到 0 沒有資訊，要重跑。\n\n'
  '## NIST 後量子密碼標準（2024 年 8 月）\n\n| 編號 | 名稱 | 用途 | 數學基礎 | 原本的提案名 |\n|---|---|---|---|---|\n'
  + ''.join(f'| {a} | {b} | {c} | {d} | {e} |\n' for a, b, c, d, e in NIST)
  + '\n## 盤點表怎麼判斷（原則）\n\n'
  '- 連線一開始交換鑰匙、確認對方身分（憑證、數位簽章）多半用公開金鑰（RSA、ECC）→ **會受影響**，要換成 ML-KEM、ML-DSA 等。\n'
  '- 用一把共用的鑰匙加密資料（對稱加密，例如 AES）→ 只受 Grover 平方加速影響，**影響較小**，用 256 位元版本即可。\n'
  '- 網路銀行：網頁或 App 走加密連線，交換鑰匙與憑證那一步會受影響。\n'
  '- 密碼管理器：密碼庫通常以主密碼保護的對稱加密存放（影響較小），但同步、登入走的連線一樣有交換鑰匙那一步；以產品說明為準。\n'
  '- Wi‑Fi：依路由器設定（WPA2／WPA3）不同，答「還不確定、要查設定」是合格的。\n\n'
  '## 常見問題\n\n'
  '- 後量子密碼要用量子電腦嗎？不用，它在現在的電腦和手機上執行；和上一堂的量子金鑰分發是兩回事。\n'
  '- 量子電腦現在能破解 RSA 嗎？還不能。2025 年的估計約需不到 100 萬個錯誤率 0.1% 的實體量子位元、不到一週；目前最大系統約一千個量子位元。\n'
  '- 那為什麼現在就要換？因為「先存下來、以後再解密」：今天被攔下的資料，以後可能被解開；換鎖本身也要好幾年。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路或帳號。

## `operation.html#shor`（3D 場景 10：Shor 週期尋找）

- 按鈕：N = 15、N = 21；a = …（依 N 列出和 N 互質的數）；下一步 ▶、自動播放、重設。
- 64 根柱子是 x 暫存器 0–63；顏色代表 f(x) = aˣ mod N 的值，青色是 QFT 後的機率，白色是量到的 y。
- 右下插圖：f(x) 的週期圖，標出「a = 7，週期 r = 4」。
- 左側讀數：真正週期、第二暫存器量到的 f、峰值應在的位置、連分數與 gcd 的結果。

## 操作

`H` 隱藏面板；滑鼠拖曳旋轉、滾輪縮放。
''',
}

SHEET_HEADER = ['用途', '誰在用', '怎麼用（登入／連線／存檔）', '交換鑰匙或確認身分？', '共用鑰匙加密資料？', '判斷（會受影響／影響較小／還不確定）', '要去查什麼', '可換成的新標準']
SHEET_ROWS = [[it, '', '', '', '', '', '', ''] for it in ITEMS]

EXTRA_CSS = '''table.rec td{height:10mm}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.card{border:2pt solid #0b2540;border-radius:4mm;padding:5mm;margin-top:5mm}.card h3{margin-top:0}'''


def html():
    pages = [
        '<h2>家中加密盤點表（今天的作品）</h2><p class="lead">列出家裡用到加密的地方，逐項標出：會受影響／影響較小／還不確定。不要寫任何密碼。</p>'
        '<table class="rec"><tr><th>用途</th><th>怎麼用</th><th>交換鑰匙或<br>確認身分？</th><th>共用鑰匙<br>加密資料？</th><th>判斷</th><th>要去查什麼</th></tr>'
        + ''.join(f'<tr><td>{it}</td><td></td><td></td><td></td><td></td><td></td></tr>' for it in ITEMS) + '</table>'
        '<p>作品名稱：＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>',
        '<h2>安全審查：問題卡</h2><p class="lead">爸爸是受審者，你是審查員。每一項都問這幾題。</p>'
        '<div class="card"><h3>審查員的問題</h3><ul class="chk">'
        '<li>這一項是在交換鑰匙嗎？（連線一開始談好一把鑰匙）</li><li>這一項是在確認身分嗎？（憑證、數位簽章）</li>'
        '<li>還是用一把共用的鑰匙加密資料？（對稱加密）</li><li>這裡的資料要保密幾年？</li><li>如果不確定，要去哪裡查？</li></ul></div>'
        '<div class="card"><h3>判斷原則</h3><p>公開金鑰（RSA、ECC）→ 會受影響，要換鎖。</p><p>對稱加密（例如 AES）→ 影響較小，鑰匙位元數加倍即可。</p>'
        '<p>保密越久的資料，越要先換：先存下來、以後再解密。</p></div>',
        '<h2>換你改造：查 NIST 後量子密碼標準</h2><p class="lead">2024 年 8 月，美國國家標準與技術研究院（NIST）公布三個標準。查出來填好。</p>'
        '<table class="rec"><tr><th>編號</th><th>名稱</th><th>用途</th><th>建立在什麼數學上</th></tr>'
        + ''.join(f'<tr><td>{a}</td><td></td><td></td><td></td></tr>' for a, *_ in NIST) + '</table>'
        '<p>對回盤點表：＿＿＿＿＿＿ 的 ＿＿＿＿ 那一步，可以換成 ＿＿＿＿＿＿。</p>'
        '<p>Shor 練習：7ˣ mod 15 = 1、7、＿、＿、1 … 週期 r = ＿；gcd(7² mod 15 ± 1, 15) = ＿、＿</p>'
        '<p class="note">生活技能：提早準備，降低風險——你還想到哪件事最好提早準備？＿＿＿＿＿＿＿＿</p>',
        '<h2>說明卡與最後一關</h2><div class="box"><p>1. 公開金鑰密碼靠什麼數學難題保密？</p><div class="line"></div>'
        '<p>2. Shor 演算法怎麼把分解變簡單？</p><div class="line"></div><p>3. 後量子密碼是什麼？要不要量子電腦？</p><div class="line"></div>'
        '<p>4. 一個注意事項：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出：分解變找週期、QFT 找高峰、古典算 gcd</li><li>說出哪些會受影響：公開金鑰會，對稱加密影響較小</li>'
        '<li>說出三個 NIST 標準和用途</li><li>指出一個風險：先存下來、以後再解密</li>'
        '<li>替盤點表取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q091 Shor 之後：後量子密碼 列印包', '父子科技學院 量子電腦學程 Q091｜Shor 之後：後量子密碼', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q091-post-quantum-cryptography', folder='Q091_Shor之後後量子密碼', files=FILES,
        sheet=('03_家中加密盤點表.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_後量子密碼.pdf', pack_pages=4,
        pack_needles=('家中加密盤點表', '安全審查', '問題卡', 'NIST', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q091', episode_dir='specials/q091-post-quantum-cryptography',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'scenes': ['animations/operation.html#shor'],
               'nistStandards': {a: b for a, b, *_ in NIST}, 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q091/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')
