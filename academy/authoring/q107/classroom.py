"""Q107 課堂教材：四種黑盒判讀表、可執行的 deutsch_box.py、盲測紀錄表（自己當黑盒子）、容易錯的地方、教爸爸檢核表與解答。

不需要帳號，也不需要安裝套件：動畫用瀏覽器開 animations/transmon-3d.html#deutsch-lab；程式只要 Python 3。
建置時會真的執行一次 deutsch_box.py，確認輸出和影片、教材寫的結果一致。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q107/classroom.py
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
RUN_OUTPUT = '''輔助位元準備成 |−⟩（先翻轉再哈達瑪）
  f1（永遠 0，常數）問完後振幅 +0.50 −0.50 +0.50 −0.50｜量到 1 的機率 0%｜判讀 常數 ✓
  f2（永遠 1，常數）問完後振幅 −0.50 +0.50 −0.50 +0.50｜量到 1 的機率 0%｜判讀 常數 ✓
  f3（f(x) = x，平衡）問完後振幅 +0.50 −0.50 −0.50 +0.50｜量到 1 的機率 100%｜判讀 平衡 ✓
  f4（f(x) = NOT x，平衡）問完後振幅 −0.50 +0.50 +0.50 −0.50｜量到 1 的機率 100%｜判讀 平衡 ✓
忘了先翻轉：輔助位元變成 |+⟩
  f1（永遠 0，常數）問完後振幅 +0.50 +0.50 +0.50 +0.50｜量到 1 的機率 0%｜判讀 常數 ✓
  f2（永遠 1，常數）問完後振幅 +0.50 +0.50 +0.50 +0.50｜量到 1 的機率 0%｜判讀 常數 ✓
  f3（f(x) = x，平衡）問完後振幅 +0.50 +0.50 +0.50 +0.50｜量到 1 的機率 0%｜判讀 常數 ✗
  f4（f(x) = NOT x，平衡）問完後振幅 +0.50 +0.50 +0.50 +0.50｜量到 1 的機率 0%｜判讀 常數 ✗
古典電腦：要分別問 f(0)、f(1) 共 2 次；量子：只問 1 次
盲測：黑盒子 ？ 只問 1 次 → 輸入位元量到 1 → 平衡
'''

PROGRAM = r'''"""父子科技學院 量子電腦學程 Q107：Deutsch 演算法與相位回踢——四種黑盒子（純 Python，不需要安裝任何套件）

執行：  python deutsch_box.py
兩顆位元：q0 是輸入位元 x，q1 是輔助位元 y。狀態用 4 個振幅表示，順序是 |x y⟩ = |00⟩、|01⟩、|10⟩、|11⟩
（和 transmon-3d.html 第 7 章的四根長條相同）。
"""
import math

R = 1 / math.sqrt(2)
PREP = True     # 改造區 1：輔助位元要不要先翻成 1？（True = 照課本；False = 忘了準備，看看會怎樣）
SECRET = 'f3'   # 改造區 2（盲測）：孩子偷偷改成 f1、f2、f3 或 f4，只讓爸爸看最後一行

BOXES = [
    ('f1', '永遠 0', '常數', lambda x: 0),
    ('f2', '永遠 1', '常數', lambda x: 1),
    ('f3', 'f(x) = x', '平衡', lambda x: x),
    ('f4', 'f(x) = NOT x', '平衡', lambda x: 1 - x),
]


def hadamard(s, q):
    """對第 q 顆做哈達瑪閘（q = 0 是輸入位元，q = 1 是輔助位元）"""
    bit = 2 if q == 0 else 1
    out = s[:]
    for i in range(4):
        if not i & bit:
            a, b = s[i], s[i | bit]
            out[i], out[i | bit] = R * (a + b), R * (a - b)
    return out


def flip(s, q):
    """對第 q 顆做翻轉閘"""
    bit = 2 if q == 0 else 1
    return [s[i ^ bit] for i in range(4)]


def oracle(s, f):
    """量子黑盒子：|x y⟩ → |x, y ⊕ f(x)⟩（只查詢這一次）"""
    out = [0.0] * 4
    for x in (0, 1):
        for y in (0, 1):
            out[2 * x + (y ^ f(x))] += s[2 * x + y]
    return out


def deutsch(f, prep=True):
    s = [1.0, 0.0, 0.0, 0.0]          # |00⟩
    if prep:
        s = flip(s, 1)                 # 輔助位元翻成 1
    s = hadamard(hadamard(s, 0), 1)    # 兩顆都做哈達瑪閘
    s = oracle(s, f)                   # 問黑盒子一次
    after = s
    s = hadamard(s, 0)                 # 輸入位元再做一次哈達瑪閘
    p1 = s[2] ** 2 + s[3] ** 2         # 量到輸入位元 = 1 的機率
    return after, p1


def sign(v):
    return ('+' if v > 1e-9 else '−' if v < -1e-9 else ' ') + f'{abs(v):.2f}'


if __name__ == '__main__':
    for prep in (PREP, not PREP):
        print('輔助位元準備成 |−⟩（先翻轉再哈達瑪）' if prep else '忘了先翻轉：輔助位元變成 |+⟩')
        for name, rule, kind, f in BOXES:
            after, p1 = deutsch(f, prep)
            guess = '平衡' if p1 > 0.5 else '常數'
            print(f'  {name}（{rule}，{kind}）問完後振幅 ' + ' '.join(sign(v) for v in after)
                  + f'｜量到 1 的機率 {p1 * 100:.0f}%｜判讀 {guess} ' + ('✓' if guess == kind else '✗'))
    print('古典電腦：要分別問 f(0)、f(1) 共 2 次；量子：只問 1 次')
    box = next(b for b in BOXES if b[0] == SECRET)
    _, p1 = deutsch(box[3], PREP)
    print(f'盲測：黑盒子 ？ 只問 1 次 → 輸入位元量到 {round(p1)} → {"平衡" if p1 > 0.5 else "常數"}')
'''

# 四種黑盒子：(代號, 規則, 紅綠球, 類型, 黑盒裡的閘, 問完後的輸入位元, 量到)
BOXES = [
    ('f₁', '永遠 0', '兩顆都紅', '常數', '什麼都不做', '+|+⟩', '0'),
    ('f₂', '永遠 1', '兩顆都綠', '常數', '對輔助位元 X', '−|+⟩', '0'),
    ('f₃', 'f(x) = x', '一紅一綠', '平衡', 'CNOT（= H–CZ–H）', '+|−⟩', '1'),
    ('f₄', 'f(x) = NOT x', '一綠一紅', '平衡', 'CNOT 再 X', '−|−⟩', '1'),
]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q107：第 9 課 Deutsch 演算法與相位回踢（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶出今天的任務：黑盒子只准問一次，怎麼判斷它是常數還是平衡；課堂用「盲測」的方式，先在 3D 動畫把四種黑盒子都跑一次，再讓孩子當黑盒子考爸爸。

## 需要準備

| 項目 | 說明 |
|---|---|
| 動畫 | 下載學程的 `animations/` 資料夾，用瀏覽器開 `transmon-3d.html#deutsch-lab`（第 7 章自由實驗）；加映 `transmon-3d.html#deutsch`（第 7 章 Deutsch 步驟，自動播放約 47 秒）、`basic-circuits.html#deutsch`（範例 6）。免安裝、不需帳號 |
| 程式 | `deutsch_box.py`：只要有 Python 3 就能跑，不需安裝套件、不需帳號 |
| 列印 | `02_列印包_Deutsch演算法與相位回踢.pdf`（A4，共 4 頁）；四張小紙卡寫 f₁、f₂、f₃、f₄（盲測用） |
| 參考 | 《量子金魚》008 Deutsch 演算法報告簡報（紅綠球搖獎機比喻） |

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片；先猜「只准問一次，能分出常數和平衡嗎？」 | 影片、列印包第 1 頁 |
| 10–25 | 概念示範：紅綠球、可逆黑盒子、相位回踢、疊加→查詢→干涉 | 影片第 3–7 段、`05_動畫導覽.md` |
| 25–65 | 在 deutsch-lab 跑四種黑盒子（先一鍵、再單步），對照紅綠球，填四種黑盒判讀表 | `01_操作步驟.md`、列印包第 1 頁 |
| 65–75 | 休息 | |
| 75–105 | 孩子當黑盒子：偷偷選紙卡、改程式的 SECRET，爸爸只問一次猜類型；再改 PREP 看忘了準備會怎樣 | `deutsch_box.py`、列印包第 2 頁、`03_盲測紀錄.csv` |
| 105–115 | 孩子教爸爸：操作與原理，指出一個限制 | 列印包第 3、4 頁 |
| 115–120 | 錄音總結、替四種黑盒判讀表命名、存檔 | |

## 課前準備（約 20 分鐘）

- 自己先打開 `transmon-3d.html#deutsch`，看完第 7 步 Deutsch（約 47 秒，左上方字幕逐句說明），再按步驟「8」進自由實驗。
- 在自由實驗依序試 f₁～f₄ 各按一次「一鍵 Deutsch」，再按「隨機（隱藏）」玩一回。
- 跑一次 `python deutsch_box.py`，確認最後一行是「盲測：黑盒子 ？ 只問 1 次 → 輸入位元量到 1 → 平衡」。
- 讀一遍 `04_解答.md`。

## 解碼者（爸爸）的原則

- 只准問一次：程式只看最後一行、動畫只按一次「一鍵 Deutsch」。
- 說出常數或平衡之後，要能解釋負號怎麼跑到輸入位元上（相位回踢）。
- 最重要的一句：輔助位元一定要在 |−⟩；忘了準備（少了 X），相位回踢不會發生，平衡也會被誤判成常數。

## 誠實說明

- Deutsch 在 1985 年最早提出這個問題的量子解法；當年的原始版本成功機率只有一半，今天這個只問一次、100% 確定的電路，是 1998 年 Cleve 等人改良後的版本（維基百科 Deutsch–Jozsa algorithm）。
- 量子優勢是「查詢次數 2 → 1」，不是速度，也沒有實用價值；價值在觀念：只回答全域性質（f(0) 和 f(1) 是否相同），而且相位回踢後來一路用到 Shor。
- Deutsch 不需要糾纏：輔助位元從頭到尾停在 |−⟩，全程是乘積態。
- 動畫的「隨機（隱藏）」每次抽到哪一個黑盒子不一定；量測次數是模擬抽樣。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：四種黑盒子（約 40 分鐘）

1. 用瀏覽器開 `animations/transmon-3d.html#deutsch-lab`（第 7 章 ⑧ 自由實驗）。右邊面板往下捲，找到「黑盒子」那一列。
2. 選「f₁：常數 0」，按「一鍵 Deutsch」。它會依序做 X(q1) → H⊗H → U_f → H(q0) → 量測 30 次。看面板「量測結果」的「第一位 q0」，填進列印包第 1 頁。
3. 換 f₂、f₃、f₄ 各做一次。每次都注意：U_f 之後，紅色（負的）長條在哪幾根？
4. 單步再做一次 f₃：按「重設 |00⟩」→「X₂」→「H₁」→「H₂」→「U_f」→「H₁」→「量測 50 次」。每按一下，說出長條怎麼變；右上的判定是不是一直寫「乘積態」？
5. 對照紅綠球：f₁ 兩顆都紅、f₂ 兩顆都綠、f₃ 一紅一綠、f₄ 一綠一紅。
6. 盲測一回：按「隨機（隱藏）」，先猜，再按「一鍵 Deutsch」，看左上字幕揭曉。

## 加映：另一個動畫（約 10 分鐘，可選）

- `animations/basic-circuits.html#deutsch`：選「f(x)=1-x」，按「⏮ 起點」再一步一步按「下一步 ▶」，看「單看 q0」的布洛赫球在黑盒那一步翻面；最後按「量測 1,000 次」。
- 再選「f(x)=1」：所有項一起變號（整體相位），q0 的布洛赫球不動，最後全是 0。

## 下半場：你當黑盒子（約 30 分鐘）

1. 孩子偷偷抽一張紙卡（f₁～f₄），打開 `deutsch_box.py`，把 `SECRET = 'f3'` 改成抽到的那一個（例如 `'f1'`）。
2. 執行 `python deutsch_box.py`，只讓爸爸看最後一行「盲測：…」。爸爸說出常數或平衡，填進列印包第 2 頁。
3. 換角色再玩幾回；每回都記錄「猜對了嗎」。爸爸能從最後一行分出 f₁ 和 f₂ 嗎？為什麼？
4. 改造：把 `PREP = True` 改成 `False` 再跑一次，看前四列和後四列的位置互換、平衡的兩種被判成常數 ✗。說出原因。
'''
}

FILES.update({
'deutsch_box.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n## 四種黑盒判讀表\n\n| 黑盒子 | 規則 | 紅綠球 | 類型 | 黑盒裡的閘 | 問完後的輸入位元 | 最後量 q0 |\n|---|---|---|---|---|---|---|\n'
  + ''.join(f'| {a} | {b} | {c} | {d} | {e} | {f} | {g}（100%） |\n' for a, b, c, d, e, f, g in BOXES)
  + '\n## deutsch_box.py 實跑（Python 3.13.18）\n\n```\n' + RUN_OUTPUT + '```\n\n'
  '- 振幅順序是 |x y⟩ = |00⟩、|01⟩、|10⟩、|11⟩（x 是輸入位元 q0，y 是輔助位元 q1），和 transmon-3d 第 7 章的四根長條相同。\n'
  '- 準備成 |−⟩：問完後 f₃ 的負號從 |11⟩ 搬到 |10⟩（相位回踢）；f₂ 四根一起變號（整體相位），所以和 f₁ 一樣量到 0。\n'
  '- 忘了先翻轉（PREP = False）：輔助位元是 |+⟩，翻轉它不會多出負號，四種問完後的振幅全是 +0.50，輸入位元一律量到 0，f₃、f₄ 被誤判成常數。\n'
  '- PREP 改成 False 再跑：程式先印「忘了先翻轉」那段，再印「準備成 |−⟩」那段；最後一行盲測也用 PREP，所以 SECRET = f3 時會誤判成常數。\n'
  '- 爸爸分不出 f₁ 和 f₂：兩者只差整體相位，量不到；Deutsch 本來就只回答「常數還是平衡」（f(0) ⊕ f(1)）。\n'
  '- 古典做法：問 f(0)、再問 f(1)，共 2 次；量子只問 1 次。優勢是查詢次數，不是速度。\n'
  '- 為什麼不需要糾纏：輔助位元從頭到尾停在 |−⟩（CNOT 目標的特徵態），動畫右上判定一直是「乘積態」。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載整個資料夾後用瀏覽器開啟，不需要網路、伺服器或帳號。

## `transmon-3d.html#deutsch`（第 7 章步驟 ⑦ Deutsch）

- 自動播放約 47 秒，左上方字幕逐句說明；上方電路圖金色高亮的是正在送的閘。
- 示範 f(x) = x：準備 q1 = |1⟩ → 兩顆 H → 查詢一次（CNOT = H–CZ–H）→ 負號移到 |10⟩ → q0 再 H → 量測 30 次，第一位永遠是 1。
- 「◀ 上一步」「暫停」「重播」「下一步 ▶」與「自動接續」核取方塊；步驟按鈕 1–8。

## `transmon-3d.html#deutsch-lab`（第 7 章步驟 ⑧ 自由實驗）

- 長條高度是振幅，負的是紅色；左邊那位是 Q1／q0（輸入位元），右邊是 Q2／q1（輔助位元）。
- 黑盒子：「f₁：常數 0」「f₂：常數 1」「f₃：f(x) = x」「f₄：f(x) = NOT x」「隨機（隱藏）」。
- 「一鍵 Deutsch」：X(q1) → H⊗H → U_f → H(q0) → 量測 30 次，量完字幕顯示判斷；隱藏時電路方塊寫「U_f ?」，量完揭曉。
- 單步：「X₂」「H₁」「H₂」「U_f」；「量測 50 次」「重設 |00⟩」。面板「判定」顯示乘積態或糾纏；「量測結果」列出第一位 q0 是 0、1 各幾次。

## `basic-circuits.html#deutsch`（範例 6：Deutsch 演算法）

- 「黑盒裡的函數」選 f(x)=0、f(x)=1、f(x)=x、f(x)=1-x；換選項會直接跳到最後一步，按「⏮ 起點」從頭走。
- 振幅柱子：藍色正、橙色負；兩顆布洛赫球「單看 q0」「單看 q1」。
- 「量測 1,000 次」後顯示「→ 常數函數」或「→ 平衡函數」。

## 操作

滑鼠拖曳旋轉、滾輪縮放；transmon-3d 下方可切換十二章，左右方向鍵也能換章。
''',
})

SHEET_HEADER = ['回合', '黑盒主人', '祕密黑盒（翻開前不看）', '解碼者只問一次的結果（q0）', '解碼者猜', '翻開後', '猜對了嗎']
SHEET_ROWS = [['1', '孩子', '', '', '', '', ''], ['2', '孩子', '', '', '', '', ''], ['3', '孩子', '', '', '', '', ''],
              ['4', '爸爸', '', '', '', '', ''], ['5', '爸爸', '', '', '', '', ''], ['6（PREP = False）', '孩子', '', '', '', '', '']]

EXTRA_CSS = '''table.judge td{height:24mm;font-size:11pt}table.judge td.k{font-weight:bold;color:#0b2540}
table.rec td{height:9mm}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
pre.code{font-size:9pt;background:#f2f6fa;border:1pt solid #cfdde8;padding:3mm;margin:2mm 0;white-space:pre-wrap}
.balls{font-size:11pt;color:#4a6a88;margin:1mm 0 3mm}'''


def check_program():
    """真的跑一次 deutsch_box.py（隔離模式），確認輸出和影片、教材寫的結果一致。"""
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / 'deutsch_box.py'
        p.write_text(PROGRAM, encoding='utf-8')
        out = subprocess.run([sys.executable, '-I', str(p)], capture_output=True, text=True, check=True,
                             env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}).stdout
    assert out == RUN_OUTPUT, out
    return out


def html():
    judge = ''.join(f'<tr><td class="k">{a}</td><td>{b}<br><span class="note">{c}</span></td><td></td><td></td><td></td><td></td><td></td></tr>'
                    for a, b, c, d, e, f, g in BOXES)
    pages = [
        '<h2>四種黑盒判讀表</h2><p class="lead">在 transmon-3d.html#deutsch-lab 選黑盒子，按「一鍵 Deutsch」，只看第一位 q0。</p>'
        '<p>開場先猜：黑盒子只准問一次，能分出常數和平衡嗎？ □ 能　□ 不能　因為＿＿＿＿＿</p>'
        '<p class="balls">紅綠球：第一次搖 = 輸入 0、第二次搖 = 輸入 1；紅 = 0、綠 = 1。兩顆同色 = 常數，一紅一綠 = 平衡。</p>'
        '<table class="judge"><tr><th style="width:9%">黑盒</th><th style="width:19%">規則／紅綠球</th><th style="width:14%">我猜</th><th style="width:24%">U_f 後紅色長條</th><th style="width:16%">問完後 q0<br>（±|+⟩／±|−⟩）</th><th style="width:8%">量到 q0</th><th style="width:10%">判讀</th></tr>'
        + judge + '</table>'
        '<p class="note">q0：0 = 常數、1 = 平衡。右上判定是不是一直寫「乘積態」？ □ 是　□ 不是</p>'
        '<p>f₁ 和 f₂ 的 q0 只差一個整體負號，量得出來嗎？ □ 量得出來　□ 量不出來</p>',
        '<h2>換你當黑盒子：盲測紀錄</h2><p class="lead">黑盒主人偷偷選 f₁～f₄，改 deutsch_box.py 的 SECRET；解碼者只看最後一行，只准問一次。</p>'
        '<table class="rec"><tr><th>回合</th><th>黑盒主人</th><th>祕密黑盒</th><th>q0 結果</th><th>解碼者猜</th><th>翻開後</th><th>猜對？</th></tr>'
        + ''.join(f'<tr><td>{r[0]}</td><td>{r[1]}</td><td></td><td></td><td></td><td></td><td></td></tr>' for r in SHEET_ROWS) + '</table>'
        '<pre class="code">PREP = True     # 改造區 1：輔助位元要不要先翻成 1？（False = 忘了準備）\nSECRET = \'f3\'   # 改造區 2（盲測）：偷偷改成 f1、f2、f3 或 f4</pre>'
        '<p class="note">爸爸分得出 f₁ 和 f₂ 嗎？為什麼？＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p>',
        '<h2>三個容易錯的地方</h2><div class="box"><ul class="chk">'
        '<li>輔助位元沒準備成 |−⟩：少了 X，相位回踢不會發生，平衡被誤判成常數</li>'
        '<li>少了最後的 H：|+⟩ 和 |−⟩ 直接量都是一半一半，分不出來</li>'
        '<li>Deutsch 不需要糾纏：輔助位元從頭到尾停在 |−⟩，全程乘積態</li></ul></div>'
        '<div class="box" style="margin-top:5mm"><h3>相位回踢</h3>'
        '<p>U_f|x⟩|−⟩ = (−1)<sup>f(x)</sup>|x⟩|−⟩：負號跑到＿＿＿＿＿位元上。</p>'
        '<p>前面的整體負號（例如 f₂ 的 −|+⟩）：□ 量得到　□ 量不到</p>'
        '<p>量子優勢：□ 跑得更快　□ 查詢次數 2 → 1</p>'
        '<p>我最容易搞錯的一點：</p><div class="line"></div><div class="line"></div></div>',
        '<h2>最後一關：教爸爸相位回踢</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 答案怎麼寫進相位？輔助位元為什麼要在 |−⟩？</p><div class="line"></div>'
        '<p>2. 為什麼最後還要一個 H？</p><div class="line"></div>'
        '<p>3. 古典要問幾次？量子問幾次？優勢是什麼？</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><ul class="chk">'
        '<li>不看稿說出三步：疊加、相位回踢、干涉</li><li>在 deutsch-lab 示範一鍵 Deutsch 和單步 f₃，並解釋長條</li>'
        '<li>說出判讀：q0 = 0 常數、q0 = 1 平衡</li><li>指出一個限制：輔助位元要在 |−⟩；整體相位量不到</li>'
        '<li>替四種黑盒判讀表取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q107 Deutsch 演算法與相位回踢 列印包', '父子科技學院 量子電腦學程 Q107｜第 9 課：Deutsch 演算法與相位回踢', pages, EXTRA_CSS)


if __name__ == '__main__':
    check_program()
    classroom_pack.build(
        slug='q107-deutsch-kickback', folder='Q107_Deutsch演算法與相位回踢', files=FILES,
        sheet=('03_盲測紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_Deutsch演算法與相位回踢.pdf', pack_pages=4,
        pack_needles=('四種黑盒判讀表', '一鍵 Deutsch', '盲測紀錄', 'SECRET', '容易錯', '相位回踢', '最後一關'),
        authoring_dir=XINEW / 'authoring/q107', episode_dir='specials/q107-deutsch-kickback',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'no（瀏覽器開動畫；deutsch_box.py 只需 Python 3）',
               'program': 'deutsch_box.py', 'testedWith': 'Python 3.13.18 (standard library only)',
               'recordedRun': {'prepMinus_p1': [0, 0, 100, 100], 'prepMinus_allCorrect': True,
                               'forgotX_p1': [0, 0, 0, 0], 'forgotX_misjudged': ['f3', 'f4'], 'secretF3': '平衡'},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q107/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')
