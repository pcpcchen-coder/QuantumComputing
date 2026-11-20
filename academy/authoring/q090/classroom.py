"""Q090 課堂教材：量子密碼：BB84 — 遊戲規則、三人金鑰遊戲紀錄（無 Eve／有 Eve）、錯誤率計算、說明卡與解答。

免安裝、不需帳號：只要硬幣與方向卡（＋／×）；選用學程的 animations/operation.html（#qubit、#readout），用瀏覽器開啟。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q090/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent
ROUNDS = 20

# 攔截重送：Eve 猜錯基底 1/2 × Bob 因此讀錯 1/2 = 1/4（Wikipedia: Quantum key distribution, Intercept and resend）
QBER_EVE = 0.25
# 抽查 n 位、至少抓到一個錯的機率 P_d = 1 − (3/4)^n（同上；n = 72 → 0.999999999）
CHECK = [(n, 1 - 0.75 ** n) for n in (1, 2, 5, 10, 20, 72)]
assert abs(CHECK[3][1] - 0.9437) < 1e-4 and CHECK[-1][1] > 0.999999998
# Eve 只攔截比例 f 的光子 → 錯誤率約 f/4（由上式推得，教學用）
PARTIAL = [(f, f / 4) for f in (1.0, 0.5, 0.2)]

FILES = {
'00_爸爸先讀.md': f'''# 父子科技學院 量子電腦學程 Q090：量子密碼：BB84（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶出一個問題：兩個人要共用一把秘密鑰匙，怎麼確定途中沒人偷看？

只需要硬幣三枚、方向卡（每人一組「＋」「×」各一張，或用一枚硬幣決定）與列印包。動畫是選用的：下載學程的 `animations/` 資料夾，開 `operation.html#qubit` 和 `operation.html#readout`。不需要網路、帳號或安裝。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 兩種基底、量錯基底一半一半、量測擾動 | 影片第 3–6 段、`05_動畫導覽.md` |
| 25–65 | 三人金鑰遊戲：先 {ROUNDS} 回合沒有 Eve，再 {ROUNDS} 回合有 Eve | `01_操作步驟.md`、列印包第 1–2 頁 |
| 65–75 | 休息 | |
| 75–105 | 算出 Eve 造成的錯誤率，和遊戲紀錄比較 | 列印包第 3 頁、`03_金鑰遊戲紀錄.csv` |
| 105–115 | 孩子教爸爸：協定怎麼運作、為什麼抓得到偷聽 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 角色

- Alice（愛麗絲）：送出的人。Bob（鮑伯）：接收的人。Eve（伊芙）：偷聽的人。只有兩個人時，爸爸兼任 Alice 和 Eve，但 Eve 的動作要在孩子看不到時做。

## 誠實說明

- 硬幣＋方向卡是依 BB84 規則設計的教學模擬：「基底不同就擲硬幣當結果」模擬的是量子力學的隨機，不是實際的光學實驗。
- 25% 只適用於 Eve 攔截每一顆光子、照量到的結果重送（攔截重送攻擊）；只攔截一部分，錯誤率會比較低。
- 驗收要說出的限制：QKD 保護的是金鑰交換這一步；公開通道要能認證；實際設備仍可能有漏洞。
''',

'01_操作步驟.md': f'''# 操作步驟

## A. 一回合怎麼玩（沒有 Eve）

1. Alice 擲硬幣決定位元（正面 = 0、反面 = 1），再抽方向卡決定基底（＋ 直線、× 斜線），寫在小紙條上交給 Bob，不讓 Bob 看基底。
2. Bob 抽自己的方向卡選基底。Alice 在旁邊對答案：基底一樣，Bob 就照實讀出位元；不一樣，Bob 擲硬幣當結果（隨機）。
3. Bob 把自己的基底和結果記在列印包第 1 頁。
4. 玩完 {ROUNDS} 回合，兩人公開說出每一回合的基底（不說結果），基底不同的那一列打叉丟掉。
5. 從留下的位元裡選一半公開比對，記下有幾個對不上；剩下沒公開的，就是你們的金鑰。

## B. 加入 Eve（再玩 {ROUNDS} 回合）

1. 紙條先交給 Eve。Eve 抽方向卡猜基底：猜對就照實讀出位元；猜錯就擲硬幣當結果。
2. Eve 用「自己猜的基底」和「自己讀到的位元」重寫一張紙條交給 Bob（原本的紙條收走）。
3. Bob 照 A 的規則讀這張新紙條（比對的是 Eve 寫的基底）。
4. 最後一樣公開比基底、丟掉不同的、抽查一半，記在列印包第 2 頁。

## C. 選用：在動畫裡看「對的基底、錯的基底」

1. `operation.html#qubit`：按 |0⟩ → 一次跑 1000 shots（全部是 0）；按 |+⟩ → 一次跑 1000 shots（約一半一半）；按「測量一次」看箭頭跳到極點。
2. `operation.html#readout`：準備狀態 θ 拉到 0，基底按「量 Z」→ 幾乎全藍；按「量 X（先 H）」→ 藍紅各半。

## D. 下半場：算 Eve 造成的錯誤率（約 30 分鐘）

用列印包第 3 頁一步一步算，再和 A、B 兩段的抽查錯誤率比較。
''',

'04_解答.md': '# 解答（爸爸用）\n\n## Eve 攔截每一顆光子時的錯誤率\n\n'
  '- Eve 猜錯基底的機率：1/2\n- 猜錯後 Bob（用和 Alice 一樣的基底）讀錯的機率：1/2\n'
  f'- 相乘：1/2 × 1/2 = 1/4 = {QBER_EVE:.0%}\n\n'
  '遊戲只有約十個留下的位元、抽查一半約五個，數字會跳動很大；把全家幾輪的紀錄加起來比較接近 25%。沒有 Eve 的那一段，抽查應該完全對得上（硬幣模擬沒有雜訊）。\n\n'
  '## 抽查 n 位，至少抓到一個錯（Eve 攔截每一顆）\n\n| 抽查位數 n | 抓到 Eve 的機率 1 − (3/4)^n |\n|---|---|\n'
  + ''.join(f'| {n} | {p:.9f} |\n' if n == 72 else f'| {n} | {p:.1%} |\n' for n, p in CHECK)
  + '\n（n = 72 的數字與維基百科 Quantum key distribution 頁一致：0.999999999。）\n\n'
  '## 延伸：Eve 只攔截一部分\n\n| 攔截比例 | 預期錯誤率 |\n|---|---|\n'
  + ''.join(f'| {f:.0%} | {q:.1%} |\n' for f, q in PARTIAL)
  + '\n## 常見問題\n\n'
  '- 為什麼要公開基底？基底不是秘密，結果才是；基底不同的那幾次，Bob 的結果是隨機的，沒有用。\n'
  '- 為什麼 Eve 不能先複製？不可複製定理：無法完美複製一個未知的量子狀態。\n'
  '- 抽查過的位元還能用嗎？不能，已經公開了。\n'
  '- 錯誤一定是 Eve 造成的嗎？不一定，雜訊也會造成錯誤；但分不出來，所以全部當成被偷聽處理。\n'
  '- QKD 安全嗎？原理上，攔截會留下錯誤；但它只保護金鑰交換，公開通道要能認證，實際設備也可能有漏洞（例如旁通道攻擊）。\n',

'05_動畫導覽.md': '''# 動畫導覽（選用）

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路或帳號。學程目前還沒有 BB84 專用場景，以下兩個場景用來看「對的基底、錯的基底」。

## `operation.html#qubit`（3D 場景 1：量子位元的狀態與測量）

- 預設按鈕：|0⟩、|1⟩、|+⟩、|+i⟩、θ=60°；測量一次、連續 shots、清除統計、一次跑 1000 shots。
- |0⟩ 像直線基底的 0；|+⟩ 像斜線基底的 0。動畫只用直線基底（Z）量。
- 「測量一次」後箭頭跳到北極或南極，約 1.4 秒後動畫自動重新準備狀態（真實的光子不會）。

## `operation.html#readout`（3D 場景 7：讀取與統計）

- 基底單選：量 Z（直接量）、量 X（先 H）、量 Y（先 S†H）。量 X 等於先做哈達瑪閘再量 Z。
- 滑桿「準備狀態 θ」：0 是 |0⟩；90 接近 |+⟩。
- 下方平面每個點是一次讀取，粉紅線右邊判為 1（紅）、左邊判為 0（藍）。

## 操作

`H` 隱藏面板；滑鼠拖曳旋轉、滾輪縮放。
''',
}

SHEET_HEADER = ['段落', '回合', 'Alice 位元', 'Alice 基底', 'Eve 基底', 'Eve 讀到', 'Bob 基底', 'Bob 讀到', '基底相同？', '抽查？', '對得上？']
SHEET_ROWS = ([['沒有 Eve', str(i), '', '', '—', '—', '', '', '', '', ''] for i in range(1, ROUNDS + 1)]
              + [['有 Eve', str(i), '', '', '', '', '', '', '', '', ''] for i in range(1, ROUNDS + 1)])

EXTRA_CSS = '''table.rec td{height:7.2mm}table.rec{font-size:11pt}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.card{border:2pt solid #0b2540;border-radius:4mm;padding:4mm;margin-top:4mm}.card h3{margin-top:0}'''


def _rows(cols):
    return ''.join('<tr><td>' + str(i) + '</td>' + '<td></td>' * cols + '</tr>' for i in range(1, ROUNDS + 1))


def html():
    pages = [
        '<h2>金鑰遊戲一：沒有 Eve</h2><p class="lead">正面 = 0、反面 = 1；＋ 直線、× 斜線。基底相同照實讀，不同就擲硬幣。</p>'
        '<table class="rec"><tr><th>回合</th><th>Alice 位元</th><th>Alice 基底</th><th>Bob 基底</th><th>Bob 讀到</th><th>基底相同？</th><th>抽查／留下</th></tr>'
        + _rows(6) + '</table>'
        '<p class="note">基底相同：＿＿ 回合　抽查：＿＿ 位，對不上：＿＿ 位　留下的金鑰：＿＿＿＿＿＿＿＿</p>',
        '<h2>金鑰遊戲二：Eve 在中間</h2><p class="lead">Eve 猜一個基底偷量，照自己讀到的結果重寫紙條交給 Bob。</p>'
        '<table class="rec"><tr><th>回合</th><th>Alice 位元</th><th>Alice 基底</th><th>Eve 基底</th><th>Eve 讀到</th><th>Bob 基底</th><th>Bob 讀到</th><th>抽查對得上？</th></tr>'
        + _rows(7) + '</table>'
        '<p class="note">基底相同：＿＿ 回合　抽查：＿＿ 位，對不上：＿＿ 位　錯誤率：＿＿＿%</p>',
        '<h2>換你改造：Eve 造成的錯誤率</h2><p class="lead">假設 Eve 攔截每一顆光子，只看 Alice 和 Bob 基底相同的位元。</p>'
        '<div class="box"><p>1. Eve 猜錯基底的機率：＿＿＿</p><p>2. 猜錯之後，Bob 讀錯的機率：＿＿＿</p>'
        '<p>3. 相乘：＿＿＿ × ＿＿＿ ＝ ＿＿＿ ＝ ＿＿＿%</p><p>4. 我的遊戲二錯誤率：＿＿＿%　接近嗎？為什麼會差？</p><div class="line"></div></div>'
        '<table class="rec"><tr><th>抽查位數</th><th>抓到 Eve 的機率 1 − (3/4)ⁿ</th></tr>'
        + ''.join(f'<tr><td>{n}</td><td></td></tr>' for n, _ in CHECK[:4]) + '</table>'
        '<div class="card"><h3>BB84 遊戲紀錄（今天的作品）</h3><p>作品名稱：＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>生活技能：資訊安全意識——家裡最需要保護的一把「鑰匙」是：＿＿＿＿＿＿＿＿</p></div>',
        '<h2>說明卡與最後一關</h2><div class="box"><p>1. 為什麼量了就會改變狀態？</p><div class="line"></div>'
        '<p>2. Alice 和 Bob 怎麼靠抽查發現 Eve？</p><div class="line"></div><p>3. 為什麼要公開基底、卻不能公開結果？</p><div class="line"></div>'
        '<p>4. 一個限制或注意事項：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出：量錯基底，結果隨機、狀態被改掉</li><li>說出協定四步：送、量、比基底、抽查</li>'
        '<li>算出 Eve 造成的錯誤率：½ × ½ ＝ 25%</li><li>指出一個限制：只保護金鑰交換；設備可能有漏洞</li>'
        '<li>替 BB84 遊戲紀錄取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q090 量子密碼：BB84 列印包', '父子科技學院 量子電腦學程 Q090｜量子密碼：BB84', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q090-bb84-quantum-key-distribution', folder='Q090_量子密碼BB84', files=FILES,
        sheet=('03_金鑰遊戲紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_量子密碼BB84.pdf', pack_pages=4,
        pack_needles=('沒有 Eve', 'Eve 在中間', '錯誤率', 'BB84 遊戲紀錄', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q090', episode_dir='specials/q090-bb84-quantum-key-distribution',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'scenes': ['animations/operation.html#qubit', 'animations/operation.html#readout'],
               'interceptResendErrorRate': QBER_EVE, 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q090/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')
