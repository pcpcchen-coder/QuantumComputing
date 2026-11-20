"""Q011 課堂教材：三人傳送角色扮演（名牌、祕密狀態卡、鮑伯的四個信封、修正表）、六格傳送漫畫、說明卡與解答、動畫導覽。

不需要帳號，也不需要安裝；動畫路線只要瀏覽器打開 animations/basic-circuits.html#teleport。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q011/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 時鐘箭頭：把布洛赫球的一個大圓（只用實數振幅的狀態）畫成時鐘。12 點 = |0⟩、6 點 = |1⟩、3 點 = |+⟩、9 點 = |−⟩。
# 相位翻轉閘（Z）= 左右翻面：h → 12 − h；翻轉閘（X）= 上下翻面：h → 6 − h（都取 12 的餘數，0 寫成 12）。
# 依簡報 basic-circuits p16：Alice 量到（第二顆 q1, 第一顆 q0）= 00 → Bob 是 ψ；01 → Zψ；10 → Xψ；11 → XZψ（先 Z 後 X）。
# 修正：q1 = 1 先做翻轉閘，q0 = 1 再做相位翻轉閘。


def _h(h):
    h %= 12
    return 12 if h == 0 else h


def Z(h):
    return _h(12 - h)


def X(h):
    return _h(6 - h)


SECRETS = [  # (名稱, 動畫上的按鈕, 時鐘幾點鐘, 量到零的機率)
    ('A 斜斜的', '√¾|0⟩+½|1⟩', 2, '四分之三'),
    ('B 朝下', '|1⟩', 6, '零'),
    ('C 朝右', '|+⟩', 3, '一半'),
    ('D 朝左', '|−⟩', 9, '一半'),
]
# 鮑伯的四個信封：信封上寫「第一顆、第二顆」的硬幣結果（q0 q1），裡面是鮑伯那顆此刻的時鐘箭頭
OUTCOMES = [('0', '0'), ('1', '0'), ('0', '1'), ('1', '1')]  # (第一顆 q0, 第二顆 q1)


def bob_before(h, q0, q1):
    if q0 == '1':
        h = Z(h)
    if q1 == '1':
        h = X(h)
    return h


def fix(h, q0, q1):
    if q1 == '1':
        h = X(h)
    if q0 == '1':
        h = Z(h)
    return h


ENVELOPES = {name: [bob_before(h, a, b) for a, b in OUTCOMES] for name, _, h, _ in SECRETS}
for name, _, h, _ in SECRETS:
    assert all(fix(bob_before(h, a, b), a, b) == h for a, b in OUTCOMES), name
assert ENVELOPES['A 斜斜的'] == [2, 10, 4, 8]

FIX_TABLE = [  # (第一顆, 第二顆, 修正)
    ('0', '0', '不用修'),
    ('1', '0', '相位翻轉閘：左右翻面'),
    ('0', '1', '翻轉閘：上下翻面'),
    ('1', '1', '先翻轉閘（上下），再相位翻轉閘（左右）'),
]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q011：隱形傳態——傳狀態不傳東西（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶出今天的任務：用「一對糾纏＋兩個古典位元」把一顆量子位元的狀態送到遠方，並且分清楚哪一步一定要靠通訊（打電話）。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 三個角色、四步線路、為什麼要打電話 | 影片第 3–7 段、列印包第 2 頁 |
| 25–65 | 三人角色扮演：照線路一步一步傳送（至少 3 回合，換祕密卡），最後一回合「信差迷路」 | 列印包第 1、2 頁、`01_操作步驟.md`、`03_傳送紀錄.csv` |
| 65–75 | 休息 | |
| 75–105 | 畫六格傳送漫畫，圈出一定要打電話的那一格 | 列印包第 3 頁 |
| 105–115 | 孩子教爸爸：需要什麼、傳了什麼、限制在哪 | 列印包第 4 頁（說明卡） |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 20 分鐘）

- 列印 `02_列印包_隱形傳態.pdf`（A4，共 4 頁），剪下三張名牌與祕密狀態卡。
- 準備兩枚硬幣、一張小紙條、8 個小信封（或對折的紙）、紅筆。
- 照 `04_解答.md` 的「鮑伯的四個信封」，為今天要用的祕密卡各做一組 4 個信封：信封外寫硬幣結果，裡面畫時鐘箭頭。
- 用瀏覽器打開 `animations/basic-circuits.html#teleport`，先自己按一次「下一步 ▶」走完四步。

## 時鐘箭頭是什麼

把量子位元的箭頭（布洛赫球）只看一個圓圈，畫成時鐘：12 點是零、6 點是一、3 點和 9 點是一半一半的兩種疊加。
翻轉閘把箭頭「上下翻面」，相位翻轉閘把箭頭「左右翻面」。這只是教學模型，只適用於這四張祕密卡這類「實數」狀態。

## 誠實說明

- 擲兩枚硬幣代表愛麗絲的測量結果：真正的隱形傳態裡，四種結果的機率各是四分之一，所以用硬幣模擬是合理的；但硬幣本身不是量子測量。
- 信封是「事先算好的答案」，代表鮑伯那顆在愛麗絲測量後可能的四種狀態；真實世界裡沒有人事先寫好信封，是糾纏讓它成立。
- 爸爸做信封時會知道答案，所以最好讓孩子先當愛麗絲；第二輪再換孩子當鮑伯、玩偶當信差。
- 隱形傳態不能比光快：信差（電話）到之前，鮑伯拿到的四個信封都有可能，他無法知道哪一個才對。
''',

'01_操作步驟.md': '''# 操作步驟

## 角色扮演：三人傳送（約 40 分鐘，至少 3 回合）

角色：愛麗絲（寄件人）、鮑伯（收件人）、信差（電話；兩人時用玩偶）。每一步都在列印包第 2 頁的線路上放閘牌或打勾。

1. 第一步：準備狀態。愛麗絲抽一張祕密狀態卡，蓋著放在自己的第一條線上（她不用看，也不用知道是哪一張）。
2. 第二步：糾纏對。愛麗絲拿「糾纏卡」，鮑伯拿這張祕密卡對應的 4 個信封（他不知道祕密卡是哪張）。兩人分開，站到房間兩端。
3. 第三步：愛麗絲測量。在線路上放「受控反閘」「哈達瑪閘」閘牌，然後擲兩枚硬幣：第一枚是第一顆、第二枚是第二顆，正面記 1、反面記 0。
   接著把祕密卡翻面放進「不見了」盒子：原本的狀態已經被破壞了。
4. 第四步：打電話。愛麗絲把兩個位元寫在紙條上交給信差，信差用走的送給鮑伯（電話不會比光快）。
5. 鮑伯修正：打開寫著這兩個位元的信封，照修正表把箭頭翻面（翻轉閘＝上下翻面，相位翻轉閘＝左右翻面），畫在紀錄表上。
6. 對答案：打開「不見了」盒子，比一比鮑伯畫的箭頭和祕密卡。再打開 `basic-circuits.html#teleport`，上方選同一個狀態，看「單看 q2」那顆球的箭頭。

最後一回合「信差迷路」（用祕密卡 A 最清楚）：鮑伯拿不到紙條，只能隨便選一個信封。卡 A 的四個信封分別是 2、10、4、8 點，他沒辦法知道哪一個才對，這就是「沒有兩個古典位元，鮑伯只拿到隨機狀態」。

## 瀏覽器動畫（約 10 分鐘）

1. 打開 `animations/basic-circuits.html#teleport`，按「下一步 ▶」四次，看兩顆 Bloch 球：「單看 q0」是愛麗絲那顆、「單看 q2」是鮑伯那顆。
2. 第 2 步之後 q2 縮到球心（單看完全隨機）；第 4 步之後 q2 指向原本 q0 的方向，q0 卻變了（不可複製）。
3. 停在第 3 步按「量測 1,000 次」：0 和 1 各一半；再按「下一步 ▶」修正，重量 1,000 次：和要傳的狀態相同。

## 下半場：六格傳送漫畫（約 30 分鐘）

1. 在列印包第 3 頁畫六格：準備狀態、分糾纏對、兩人分開、愛麗絲測量、打電話、鮑伯修正（順序可以自己決定，但要合理）。
2. 用紅筆圈出一定要打電話的那一格，旁邊寫：「沒有這通電話，鮑伯只拿到隨機狀態」。
3. 替漫畫取名字。
''',

'04_解答.md': '# 解答（爸爸用）\n\n## 時鐘箭頭與動畫的對照\n\n| 祕密卡 | 動畫上方的按鈕 | 時鐘 | 量到零的機率 |\n|---|---|---|---|\n'
  + ''.join(f'| {n} | {b.replace("|", chr(92) + "|")} | {h} 點 | {p} |\n' for n, b, h, p in SECRETS)
  + '\n## 鮑伯的四個信封（信封外寫「第一顆、第二顆」的硬幣結果）\n\n| 祕密卡 | 00 | 10 | 01 | 11 |\n|---|---|---|---|---|\n'
  + ''.join(f'| {n} | ' + ' | '.join(f'{h} 點' for h in ENVELOPES[n]) + ' |\n' for n, *_ in SECRETS)
  + '\n（欄名是「第一顆、第二顆」：10 代表第一顆是 1、第二顆是 0。）\n\n## 修正表\n\n| 第一顆 | 第二顆 | 鮑伯要做 |\n|---|---|---|\n'
  + ''.join(f'| {a} | {b} | {f} |\n' for a, b, f in FIX_TABLE)
  + '\n照修正表做完，四個信封都會回到祕密卡的箭頭（本檔產生時已用程式逐一核對）。\n\n'
  '## 常見問題\n\n'
  '- 傳過去的是什麼？是狀態，不是粒子。鮑伯那顆一直在他手上，改變的是它的狀態。\n'
  '- 為什麼一定要打電話？愛麗絲量到四種結果之一，鮑伯那顆對應四種不同的箭頭；不知道是哪一種，就不知道怎麼修。\n'
  '- 可以比光快嗎？不行。電話（古典通訊）不會比光快；電話到之前，鮑伯那顆單看完全隨機。\n'
  '- 為什麼祕密卡要翻面？愛麗絲測量之後，她手上那顆不再是原本的狀態：狀態是搬過去，不是複製（不可複製定理）。\n'
  '- 愛麗絲要知道祕密狀態嗎？不用，這個方法對任何狀態都成立。\n',

'05_線路動畫導覽.md': '''# 線路動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路、伺服器或帳號。

## `animations/basic-circuits.html#teleport`（八個基礎量子電路：隱形傳態）

- 上方「要傳的狀態 ψ」：√¾|0⟩+½|1⟩、|1⟩、|+⟩、|−⟩ 四種。換選項時會直接跳到最後一步，按「⏮ 起點」從頭看。
- 「⏮ 起點」「◀ 上一步」「▶ 播放」「下一步 ▶」：四步依序是準備 ψ、建立糾纏對、Alice 做 CNOT 與 H、Bob 依 2 個位元修正。
- 兩顆 Bloch 球：「單看 q0」（愛麗絲）和「單看 q2」（鮑伯）；縮到球心代表單看完全隨機。
- 右邊「量測 1 次」「量測 1,000 次」「清除」：只量 q2；灰色是理論，綠色是實際次數。
- 動畫用受控閘代替「量測後再修正」（延遲量測原理），q2 的結果相同。

## `animations/operation.html#circuit`（場景 6：量子線路）

- 範例選「量子隱形傳態」，按「單步 ▶」八次，最後一格會跑 1000 次並在右下角畫直方圖（青線是理想機率）。
- 這裡準備的狀態量到 1 的機率是 0.75，和 basic-circuits 的預設狀態（量到 0 的機率 75%）不同，不要混在一起比。

## 操作

`H` 隱藏面板；滑鼠拖曳旋轉、滾輪縮放（operation.html）；左右方向鍵換步（basic-circuits.html）。
''',
}

SHEET_HEADER = ['回合', '祕密卡', '硬幣第一顆', '硬幣第二顆', '打開哪個信封', '信封裡幾點鐘', '鮑伯的修正', '修正後幾點鐘', '和祕密卡一樣嗎']
SHEET_ROWS = [[f'第 {i} 回合'] for i in (1, 2, 3)] + [['信差迷路', '', '', '', '（隨便選一個）']]

ROLES = [('愛麗絲', '寄件人', '手上有要傳的狀態；測量後祕密卡要翻面'),
         ('鮑伯', '收件人', '拿著四個信封；等電話才知道開哪一個'),
         ('信差', '電話', '只送兩個位元；用走的送過去')]

EXTRA_CSS = '''.roles{display:grid;grid-template-columns:repeat(3,1fr);gap:4mm;margin-top:3mm}
.role{border:1.6pt solid #0b2540;border-radius:4mm;padding:4mm;text-align:center;min-height:42mm}
.role b{display:block;font-size:22pt;margin:2mm 0}.role small{display:block;font-size:10pt;color:#4a6a88}
.clocks{display:grid;grid-template-columns:repeat(4,1fr);gap:4mm;margin-top:3mm}
.clock{border:1.2pt dashed #0b2540;border-radius:3mm;padding:3mm;text-align:center;font-size:11pt}
.dial{width:30mm;height:30mm;border:1.2pt solid #0b2540;border-radius:50%;margin:2mm auto;position:relative}
.dial i{position:absolute;left:50%;top:50%;width:1.2pt;height:13mm;background:#c0392b;transform-origin:top center}
.steps4{display:grid;grid-template-columns:repeat(4,1fr);gap:3mm;margin-top:3mm}
.steps4 div{border:1.2pt solid #0b2540;border-radius:3mm;padding:3mm;font-size:11pt;min-height:30mm}
.call{border:2pt solid #c0392b !important}
.comic{display:grid;grid-template-columns:repeat(2,1fr);gap:4mm;margin-top:3mm}
.comic div{border:1.4pt solid #0b2540;height:62mm;padding:2mm;font-size:10pt;color:#4a6a88}
.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}'''


def _dial(h):
    # 指針從圓心往下畫，旋轉 180° + 30° × 幾點鐘，指向該點鐘方向
    return f'<div class="dial"><i style="transform:rotate({180 + 30 * h}deg)"></i></div>'


def html():
    roles = ''.join(f'<div class="role"><small>名牌</small><b>{n}</b>{r}<small>{d}</small></div>' for n, r, d in ROLES)
    secrets = ''.join(f'<div class="clock">祕密卡 {n}{_dial(h)}{h} 點鐘</div>' for n, _, h, _ in SECRETS)
    fix_rows = ''.join(f'<tr><td>{a}</td><td>{b}</td><td>{f}</td></tr>' for a, b, f in FIX_TABLE)
    comic = ''.join(f'<div>第 {i} 格</div>' for i in range(1, 7))
    pages = [
        '<h2>名牌與祕密狀態卡</h2><p class="lead">剪下名牌掛在身上；祕密卡蓋著交給愛麗絲。</p>'
        f'<div class="roles">{roles}</div>'
        '<h3 style="margin-top:6mm">祕密狀態卡（時鐘箭頭：12 點＝零、6 點＝一）</h3>'
        f'<div class="clocks">{secrets}</div>'
        '<p class="note">翻轉閘＝上下翻面；相位翻轉閘＝左右翻面。這是教學模型，只用在這四張卡。</p>',
        '<h2>傳送任務板：照線路一步一步走</h2><p class="lead">每完成一步就打勾。紅框那一步一定要打電話。</p>'
        '<div class="steps4"><div><b>第一步 □</b><br>愛麗絲拿到祕密卡（蓋著）</div>'
        '<div><b>第二步 □</b><br>分糾纏對：愛麗絲拿糾纏卡、鮑伯拿四個信封，分開站遠</div>'
        '<div><b>第三步 □</b><br>愛麗絲放受控反閘、哈達瑪閘，擲兩枚硬幣；祕密卡翻面</div>'
        '<div class="call"><b>第四步 □</b><br>打電話：信差送兩個位元；鮑伯開信封、修正</div></div>'
        '<h3 style="margin-top:5mm">修正表（鮑伯用）</h3>'
        f'<table class="rec"><tr><th>第一顆</th><th>第二顆</th><th>鮑伯要做</th></tr>{fix_rows}</table>'
        '<p class="note">信差迷路的那一回合：鮑伯只能隨便開一個信封。信封裡的箭頭不只一種，他能確定自己對了嗎？＿＿＿＿＿＿</p>',
        '<h2>六格傳送漫畫</h2><p class="lead">畫出整個傳送流程；用紅筆圈出一定要打電話的那一格。</p>'
        f'<div class="comic">{comic}</div>'
        '<p class="note">在被圈起來的格子旁邊寫：沒有這通電話，鮑伯只拿到隨機狀態。漫畫名稱：＿＿＿＿＿＿＿＿＿＿</p>',
        '<h2>說明卡：我的傳送流程漫畫</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. 隱形傳態需要哪兩樣東西？</p><div class="line"></div><p>2. 傳過去的是什麼？不是什麼？</p><div class="line"></div>'
        '<p>3. 一個限制或容易錯的地方：</p><div class="line"></div><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出：一對糾纏＋兩個古典位元</li><li>說出傳的是狀態，不是東西</li>'
        '<li>說出為什麼祕密卡要翻面（不可複製）</li><li>指出一個限制：沒有那兩個位元，鮑伯只拿到隨機狀態；不能超光速</li>'
        '<li>替漫畫和說明卡取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q011 隱形傳態 列印包', '父子科技學院 量子電腦學程 Q011｜隱形傳態：傳狀態不傳東西', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q011-teleportation', folder='Q011_隱形傳態', files=FILES,
        sheet=('03_傳送紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_隱形傳態.pdf', pack_pages=4,
        pack_needles=('名牌', '祕密狀態卡', '傳送任務板', '修正表', '六格傳送漫畫', '打電話', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q011', episode_dir='specials/q011-teleportation',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'game': '三人角色扮演傳送（硬幣代表測量、信封代表鮑伯那顆的四種可能、時鐘箭頭代表實數狀態）',
               'envelopes': ENVELOPES, 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q011/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')
