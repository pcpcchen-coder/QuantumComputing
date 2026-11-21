"""Q074 課堂教材：芮德堡阻斷與 CZ — 動畫操作步驟、阻斷距離表、闖關紀錄、|00⟩ 負號推導、說明卡與解答。

免安裝、不需帳號：只用學程的 animations/atoms.html（#rydberg、#atomqubit），用瀏覽器開啟。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q074/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 動畫 10_rydberg.js 的代表值：Ω/2π = 2 MHz、C₆/2π = 858 GHz·μm⁶ → R_b = (C₆/Ω)^(1/6)
RB_UM = round((858000 / 2) ** (1 / 6), 1)
assert RB_UM == 8.7
# 以場景自己的雙原子哈密頓量重算 0–1 μs 內 P(rr) 的最大值（製作代理，numpy 對角化）
LEVELS = [(3, 0.000), (5, 0.001), (7, 0.051), (8, 0.279), (8.5, 0.489), (9, 0.676), (10, 0.889), (12, 0.987), (15, 0.999)]
# Levine 協定讀數（RK4 重算，與動畫相同參數）
PHI01, PHI11 = -2.379, -1.618
DIFF = 3.139
# 三脈衝（π、2π、π）協定真值表（維基百科 Neutral atom quantum computer）
JAKSCH = [('|00⟩', '+1', '兩顆都在 0，雷射碰不到'), ('|01⟩', '−1', '第二顆繞一整圈'),
          ('|10⟩', '−1', '第一顆上去又回來'), ('|11⟩', '−1', '第一顆上去又回來，第二顆被阻斷')]

FILES = {
'00_爸爸先讀.md': f'''# 父子科技學院 量子電腦學程 Q074：芮德堡阻斷與 CZ（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶出一個問題：中性原子之間幾乎沒有交互作用，怎麼做兩位元閘？答案是把原子激發到芮德堡態，靠「阻斷」得到條件相位。

只需要瀏覽器：下載學程的 `animations/` 資料夾，開 `atoms.html#rydberg` 和 `atoms.html#atomqubit`。不需要網路、帳號或安裝。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 芮德堡原子、阻斷、阻斷半徑 | 影片第 3–5 段、`05_動畫導覽.md` |
| 25–65 | 改原子間距闖關、填阻斷距離表、再走一次 CZ 協定 | `01_操作步驟.md`、列印包第 1–2 頁 |
| 65–75 | 休息 | |
| 75–105 | 孩子獨立改造：解釋 \\|00⟩ 為什麼多一個負號 | 列印包第 3 頁 |
| 105–115 | 孩子教爸爸：阻斷是什麼、怎麼變 CZ | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 課前準備（約 10 分鐘）

- 先自己在 `#rydberg` 把「原子間距 r (μm)」從 5 拉到 12，看綠色阻斷球變灰、粉紅色 P(rr) 曲線從貼在 0 變成接近 1。
- 列印 `02_列印包_芮德堡阻斷與CZ.pdf`（A4，共 4 頁）。讀一遍 `04_解答.md`。

## 闖關怎麼玩

爸爸是關主，每一關指定一個間距（建議 3、5、8、10、12 μm，加分關 8.5、9）。孩子先預測「阻斷／不阻斷」，再拉滑桿、按「▶ 雷射脈衝」，讀畫面下方的標示與粉紅色曲線的最高點，填進阻斷距離表。

## 誠實說明

- 動畫的阻斷半徑約 {RB_UM} μm，是用代表值（Ω/2π = 2 MHz、C₆）算的，不是某台機器的量測；簡報寫典型 5–10 μm。
- 壽命 100–150 μs、閘時間約 0.3 μs 是簡報的代表值（n≈70）。
- 芮德堡態壽命有限，閘要夠快——這是本課最重要的注意事項。
''',

'01_操作步驟.md': '''# 操作步驟

## A. 看阻斷（`atoms.html#rydberg`，約 10 分鐘）

1. 預設間距 5 μm。按「▶ 雷射脈衝」，看曲線圖：藍色 P(gg)、紫色 P(單激發)、粉紅色 P(rr)。
2. 讀畫面下方的金色標示：「間距 r = … < R_b → 阻斷」或「> R_b → 不阻斷」。
3. 看右側雙原子能階：阻斷時 |rr⟩ 被推高，箭頭變紅、寫著「✗ 被推離共振」。

## B. 闖關：填阻斷距離表（約 20 分鐘）

1. 爸爸指定間距，孩子先在列印包第 1 頁寫預測。
2. 拉「原子間距 r (μm)」滑桿到指定值，按「▶ 雷射脈衝」。
3. 記下標示（阻斷／不阻斷）與粉紅色曲線的最高點（大約幾成）。

## C. 走一次 CZ 協定（約 10 分鐘）

1. 按「CZ 協定（Levine 2019）」：曲線圖換成兩個脈衝的示意。
2. 讀控制面板的讀數：|00⟩ 相位 0；|01⟩、|11⟩ 回到原態的機率與相位；最後一行 φ₁₁ − 2φ₀₁ ≈ π。
3. 想回到阻斷畫面，按「阻斷動力學（數值演化）」或「▶ 雷射脈衝」。

## D. 選做：單位元相位修正（`atoms.html#atomqubit`）

按「全域微波 π/2」→「局部定址 Z(π)（選中的原子）」→「全域微波 π/2」：只有洋紅色圈住的原子回到 |0⟩。
''',

'04_解答.md': '# 解答（爸爸用）\n\n'
  f'## 阻斷距離表（以動畫自己的模型重算；R_b ≈ {RB_UM} μm）\n\n'
  '| 間距 | 標示 | P(rr) 最高約 |\n|---|---|---|\n'
  + ''.join(f'| {r} μm | {"阻斷" if r < RB_UM else "不阻斷"} | {p:.2f} |\n' for r, p in LEVELS)
  + '\n重點：阻斷半徑不是一刀切；8–10 μm 之間 P(rr) 從約三成慢慢升到約九成。\n\n'
  f'## CZ 協定讀數（Levine 2019，動畫參數）\n\n- φ₀₁ ≈ {PHI01}、φ₁₁ ≈ {PHI11}\n- φ₁₁ − 2φ₀₁ ≈ {DIFF} ≈ π → 加上單位元 Z 修正就是 CZ\n\n'
  '## |00⟩ 為什麼多一個負號（三脈衝 π、2π、π 版本）\n\n| 初始態 | 結果的正負號 | 理由 |\n|---|---|---|\n'
  + ''.join(f'| {s.replace("|", chr(92) + "|")} | {g} | {w} |\n' for s, g, w in JAKSCH)
  + '\n四個狀態一起乘上 −1（整體相位，量不到）後，變成只有 |00⟩ 帶負號；這和 CZ 只差每顆原子的單位元修正。\n\n'
  '## 常見問題\n\n'
  '- 為什麼要吹大原子？基態原子幾乎沒有交互作用；芮德堡態的交互作用增加 10¹² 倍以上，而且只在做閘時打開。\n'
  '- 為什麼間距要小於 R_b？交互作用 V = C₆/r⁶ 要遠大於雷射驅動，|rr⟩ 才會被推離共振。\n'
  '- 為什麼閘要夠快？芮德堡態壽命約 100–150 μs，閘約 0.3 μs，衰變錯誤才壓在約 0.1%。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路或帳號。

## `atoms.html#rydberg`（中性原子場景 10：芮德堡阻斷與 CZ 閘）

- 滑桿「原子間距 r (μm)」：2–15，步進 0.5，預設 5。
- 按鈕：▶ 雷射脈衝、⏸ 停止；單選：阻斷動力學（數值演化）、CZ 協定（Levine 2019）。
- 綠色球＝阻斷範圍（阻斷時綠、不阻斷時灰）；右側是雙原子能階 |gg⟩、(|gr⟩+|rg⟩)/√2、|rr⟩。
- 曲線圖：藍 P(gg)、紫 P(單激發)、粉紅 P(rr)，時間軸 0–1 μs。

## `atoms.html#atomqubit`（中性原子場景 9：原子量子位元）

- 左邊 ⁸⁷Rb 能階：|0⟩、|1⟩ 相差 6.835 GHz；|1⟩ 經 420 nm、1013 nm 到芮德堡態。
- 按鈕：全域微波 π/2、全域 π、局部定址 Z(π)（選中的原子）、示範：只翻轉未定址的原子、重置。

## 操作

`H` 隱藏面板；滑鼠拖曳旋轉、滾輪縮放。
''',
}

SHEET_HEADER = ['關卡', '間距（μm）', '我的預測', '畫面標示', 'P(rr) 最高約', '對嗎', '備註']
SHEET_ROWS = [[f'第 {i} 關', str(r), '', '', '', '', ''] for i, r in enumerate([3, 5, 8, 10, 12, 8.5, 9], 1)]

EXTRA_CSS = '''table.rec td{height:9mm}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.card{border:2pt solid #0b2540;border-radius:4mm;padding:5mm;margin-top:5mm}.card h3{margin-top:0}'''


def html():
    pages = [
        '<h2>阻斷距離表（今天的作品）</h2><p class="lead">在 atoms.html#rydberg：關主指定間距 → 你先預測 → 拉滑桿、按 ▶ 雷射脈衝 → 讀標示和粉紅色曲線最高點。</p>'
        '<table class="rec"><tr><th>關卡</th><th>間距</th><th>我的預測</th><th>畫面標示</th><th>P(rr) 最高約</th><th>對嗎</th></tr>'
        + ''.join(f'<tr><td>{i}</td><td>{r} μm</td><td></td><td></td><td></td><td></td></tr>' for i, r in enumerate([3, 5, 8, 10, 12, 8.5, 9], 1)) + '</table>'
        '<p>作品名稱：＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>',
        '<h2>走一次 CZ 協定</h2><p class="lead">按「CZ 協定（Levine 2019）」，抄下控制面板的讀數。</p>'
        '<table class="rec"><tr><th>初始態</th><th>回到原態的機率</th><th>相位</th></tr>'
        '<tr><td>|00⟩</td><td>—</td><td></td></tr><tr><td>|01⟩、|10⟩</td><td></td><td>φ₀₁ =</td></tr><tr><td>|11⟩</td><td></td><td>φ₁₁ =</td></tr></table>'
        '<p>φ₁₁ − 2φ₀₁ = ＿＿＿＿　接近哪個數？＿＿＿＿</p>'
        '<div class="card"><h3>想一想</h3><p>為什麼只有 |11⟩ 的相位和別人不一樣？</p><div class="line"></div><div class="line"></div></div>',
        '<h2>換你改造：|00⟩ 為什麼多一個負號</h2><p class="lead">三脈衝版本：第一顆打 π（送上芮德堡態）→ 第二顆打 2π（繞一整圈）→ 第一顆再打 π（送回來）。雷射只碰得到 |1⟩。</p>'
        '<table class="rec"><tr><th>初始態</th><th>誰被激發？</th><th>有沒有被阻斷？</th><th>正負號</th></tr>'
        + ''.join(f'<tr><td>{s}</td><td></td><td></td><td></td></tr>' for s, *_ in JAKSCH) + '</table>'
        '<p>提示：一顆原子上去又回來（共 2π），會多一個負號。</p>'
        '<p>四個狀態一起乘上 −1 之後：＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p>'
        '<p class="note">生活技能：一個人的狀態影響另一個人——一顆原子被激發，旁邊的原子就被擋住。你想到哪個例子？＿＿＿＿＿＿＿＿</p>',
        '<h2>說明卡與最後一關</h2><div class="box"><p>1. 什麼是芮德堡阻斷？</p><div class="line"></div>'
        '<p>2. 阻斷半徑大約多大？光鑷間距呢？</p><div class="line"></div><p>3. 阻斷怎麼變成 CZ？</p><div class="line"></div>'
        '<p>4. 一個限制或注意事項：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：教爸爸</h3><ul class="chk">'
        '<li>不看稿說出阻斷：靠得夠近，兩顆不能同時被激發</li><li>說出只有 |11⟩ 的相位不一樣</li>'
        '<li>說出 |00⟩ 負號的理由</li><li>指出一個限制：芮德堡態壽命有限，閘要夠快</li>'
        '<li>替阻斷距離表取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q074 芮德堡阻斷與 CZ 列印包', '父子科技學院 量子電腦學程 Q074｜芮德堡阻斷與 CZ', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q074-rydberg-blockade-cz', folder='Q074_芮德堡阻斷與CZ', files=FILES,
        sheet=('03_阻斷距離表.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_芮德堡阻斷與CZ.pdf', pack_pages=4,
        pack_needles=('阻斷距離表', 'CZ 協定', '負號', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q074', episode_dir='specials/q074-rydberg-blockade-cz',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'scenes': ['animations/atoms.html#rydberg', 'animations/atoms.html#atomqubit'],
               'blockadeRadiusUm': RB_UM, 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q074/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')
