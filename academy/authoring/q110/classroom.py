"""Q110 課堂教材：邏輯閘資源估算表、可執行的 magic_budget.py、蒸餾實驗紀錄表、容易錯的地方、工程答辯檢核表與解答。

不需要帳號，也不需要安裝套件：動畫用瀏覽器開 animations/transmon-3d.html#surgery（第 11 章）；程式只要 Python 3。
建置時會真的執行一次 magic_budget.py，確認輸出和影片、教材寫的結果一致。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q110/classroom.py
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
RUN_OUTPUT = '''一、T 閘傳送（資料 = 0.6|0⟩ + 0.8i|1⟩）
  Z⊗Z = +1、X = +1：機率 0.25 → 不必補 → 得到 T|ψ⟩ ✓
  Z⊗Z = +1、X = -1：機率 0.25 → 補相位翻轉 → 得到 T|ψ⟩ ✓
  Z⊗Z = -1、X = +1：機率 0.25 → 補 S → 得到 T|ψ⟩ ✓
  Z⊗Z = -1、X = -1：機率 0.25 → 補 S 和相位翻轉 → 得到 T|ψ⟩ ✓
二、15 顆輸入裡有幾顆出錯，騙得過 4 個檢查的排列有幾種
  1 顆出錯：  15 種排列中   0 種騙過檢查
  2 顆出錯： 105 種排列中   0 種騙過檢查
  3 顆出錯： 455 種排列中  35 種騙過檢查
  4 顆出錯：1365 種排列中 105 種騙過檢查
三、注入錯誤率 p → 一輪蒸餾的接受率與輸出錯誤率（35p³ 是近似公式）
  p =  1.0×10^-4  接受率  99.9%  輸出錯誤率 3.5×10^-11  35p³ = 3.5×10^-11
  p =  1.0×10^-3  接受率  98.5%  輸出錯誤率  3.5×10^-8  35p³ = 3.5×10^-8
  p =      0.010  接受率  86.0%  輸出錯誤率  3.7×10^-5  35p³ = 3.5×10^-5
  p =      0.050  接受率  46.6%  輸出錯誤率  5.9×10^-3  35p³ = 4.4×10^-3
  p =      0.100  接受率  22.0%  輸出錯誤率      0.063  35p³ = 0.035
  p =      0.040  接受率  54.4%  輸出錯誤率  2.9×10^-3  35p³ = 2.2×10^-3  ← 我的 p（MY_P）
四、邏輯閘資源估算表（1,000,000,000 個 T 閘，注入錯誤率 1.0×10^-3，目標：全部加起來出錯不到 0.01 次）
  蒸餾 0 輪：每顆魔術態錯誤率  1.0×10^-3，每顆約耗     1.0 顆注入態，全部 T 閘預計出錯 1.0e+06 次
  蒸餾 1 輪：每顆魔術態錯誤率  3.5×10^-8，每顆約耗    15.2 顆注入態，全部 T 閘預計出錯 3.5e+01 次
  蒸餾 2 輪：每顆魔術態錯誤率 1.5×10^-21，每顆約耗   228.4 顆注入態，全部 T 閘預計出錯 1.5e-12 次
  → 要蒸餾 2 輪；總共約 2.3e+11 顆注入態
'''

PROGRAM = r'''"""父子科技學院 量子電腦學程 Q110：lattice surgery 與魔術態蒸餾（純 Python，不需要安裝任何套件）

執行：  python magic_budget.py
一、T 閘傳送：用一顆魔術態 |T⟩ 加上 Z⊗Z、X 兩次量測，把 T 作用到資料位元上（四種量測結果逐一驗算）。
二、15-to-1 蒸餾的檢查：15 顆輸入編號 1～15，工廠量 4 個檢查值（第 k 個檢查看編號二進位第 k 位是 1 的那 8 顆）。
三、注入錯誤率 p → 接受率、輸出錯誤率（32768 種錯誤排列全部加總，不用亂數）。
四、邏輯閘資源估算表：要跑 MY_T_COUNT 個 T 閘，需要幾輪蒸餾、消耗多少顆注入態。
"""
import cmath
from itertools import combinations

# 改造區 1：注入錯誤率（調高看看接受率怎麼變；動畫滑桿最右邊約 0.05）
MY_P = 0.04
# 改造區 2：資源估算——演算法要用幾個 T 閘
MY_T_COUNT = 10 ** 9


def fmt(x):
    return f'{x:.1e}'.replace('e-0', 'e-').replace('e-', '×10^-') if x < 0.01 else f'{x:.3f}'


# ---------- 一、T 閘傳送 ----------
W = cmath.exp(1j * cmath.pi / 4)            # T = diag(1, e^{iπ/4})


def teleport_T(a, b):
    """資料 a|0⟩+b|1⟩，魔術態 (|0⟩+W|1⟩)/√2；回傳四種結果 (ZZ, X) → 機率、資料位元的狀態"""
    s = 2 ** -0.5
    amp = {(0, 0): a * s, (0, 1): a * W * s, (1, 0): b * s, (1, 1): b * W * s}   # (資料, 魔術態)
    out = {}
    for zz in (+1, -1):
        keep = {k: v for k, v in amp.items() if (1 if k[0] == k[1] else -1) == zz}      # 量 Z⊗Z
        for x in (+1, -1):
            # 量魔術態的 X：投影到 |+⟩ 或 |−⟩，剩下資料位元的狀態
            d0 = sum(v * (1 if k[1] == 0 else x) for k, v in keep.items() if k[0] == 0) * s
            d1 = sum(v * (1 if k[1] == 0 else x) for k, v in keep.items() if k[0] == 1) * s
            out[(zz, x)] = (abs(d0) ** 2 + abs(d1) ** 2, d0, d1)
    return out


def same_state(u0, u1, v0, v1):
    """兩個單一位元狀態是否只差一個整體相位"""
    n = (abs(u0) ** 2 + abs(u1) ** 2) ** 0.5 * (abs(v0) ** 2 + abs(v1) ** 2) ** 0.5
    return abs(abs(u0.conjugate() * v0 + u1.conjugate() * v1) - n) < 1e-12


# ---------- 二、15-to-1 的 4 個檢查 ----------
def syndrome(bad):
    """bad = 出錯輸入的編號集合；第 k 個檢查 = 編號二進位第 k 位是 1 的輸入裡，出錯的個數是奇數"""
    return tuple(sum((q >> k) & 1 for q in bad) % 2 for k in range(4))


# 32768 種錯誤排列裡，哪些騙得過 4 個檢查：依出錯顆數分類
SNEAKY = [0] * 16
for w in range(16):
    SNEAKY[w] = sum(1 for bad in combinations(range(1, 16), w) if syndrome(bad) == (0, 0, 0, 0))


def distill(p):
    """一輪 15-to-1：接受率、輸出錯誤率（騙過檢查又不是零個錯誤的，一律算成輸出有錯）"""
    acc = sum(SNEAKY[w] * p ** w * (1 - p) ** (15 - w) for w in range(16))
    bad = sum(SNEAKY[w] * p ** w * (1 - p) ** (15 - w) for w in range(1, 16))
    return acc, bad / acc


if __name__ == '__main__':
    print('一、T 閘傳送（資料 = 0.6|0⟩ + 0.8i|1⟩）')
    a, b = 0.6, 0.8j
    target = (a, b * W)                        # T|ψ⟩
    fixes = {'不必補': lambda d0, d1: (d0, d1), '補相位翻轉': lambda d0, d1: (d0, -d1),
             '補 S': lambda d0, d1: (d0, 1j * d1), '補 S 和相位翻轉': lambda d0, d1: (d0, -1j * d1)}
    for (zz, x), (prob, d0, d1) in teleport_T(a, b).items():
        fix = next(n for n, f in fixes.items() if same_state(*f(d0, d1), *target))
        print(f'  Z⊗Z = {zz:+d}、X = {x:+d}：機率 {prob:.2f} → {fix} → 得到 T|ψ⟩ ✓')
    print('二、15 顆輸入裡有幾顆出錯，騙得過 4 個檢查的排列有幾種')
    for w in (1, 2, 3, 4):
        print(f'  {w} 顆出錯：{len(list(combinations(range(15), w))):4d} 種排列中 {SNEAKY[w]:3d} 種騙過檢查')
    print('三、注入錯誤率 p → 一輪蒸餾的接受率與輸出錯誤率（35p³ 是近似公式）')
    for p in (1e-4, 1e-3, 1e-2, 0.05, 0.1, MY_P):
        acc, out = distill(p)
        print(f'  p = {fmt(p):>10}  接受率 {acc * 100:5.1f}%  輸出錯誤率 {fmt(out):>10}  35p³ = {fmt(35 * p ** 3)}'
              + ('  ← 我的 p（MY_P）' if p is MY_P else ''))
    print(f'四、邏輯閘資源估算表（{MY_T_COUNT:,} 個 T 閘，注入錯誤率 1.0×10^-3，目標：全部加起來出錯不到 0.01 次）')
    p_in, cost, rounds = 1e-3, 1.0, 0
    while True:
        total_fail = MY_T_COUNT * p_in
        print(f'  蒸餾 {rounds} 輪：每顆魔術態錯誤率 {fmt(p_in):>10}，每顆約耗 {cost:7.1f} 顆注入態，'
              f'全部 T 閘預計出錯 {total_fail:.1e} 次')
        if total_fail < 0.01:
            break
        acc, p_in = distill(p_in)
        cost, rounds = cost * 15 / acc, rounds + 1
    print(f'  → 要蒸餾 {rounds} 輪；總共約 {MY_T_COUNT * cost:.1e} 顆注入態')
'''

# 邏輯閘資源估算表（作品）：(邏輯運算, 做法, 時間或代價) — 解答用；列印包上只留第一欄
COSTS = [
    ('X、Z（Pauli）', '只在軟體裡記帳（Pauli frame）', '幾乎免費'),
    ('聯合 Pauli 量測（X_A·X_B）', 'lattice surgery：準備接縫 → 合併量 d 輪 → 拆開', '約 d μs（d = 3 約 3 μs）'),
    ('CNOT', '輔助補丁 |+⟩ + 三次聯合量測 + Pauli 修正', '約 2～3d 輪（十幾到幾十 μs）'),
    ('T', '消耗 1 顆魔術態 + 閘傳送（一半補 S）', '最貴：每顆魔術態要蒸餾'),
]

FILES = {
'00_爸爸先讀.md': '''# 父子科技學院 量子電腦學程 Q110：第 12 課 lattice surgery 與魔術態蒸餾（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。影片帶出今天的任務：表面碼負責「存」，要「算」還得做邏輯閘。Clifford 運算用 lattice surgery（縫合兩塊表面碼補丁、量出聯合奇偶、再拆開）；真正帶來量子優勢的 T 閘，要消耗事先蒸餾好的魔術態。課堂用「工程答辯」的方式：孩子當工程師，爸爸當評審，追問每一種邏輯閘要花多少時間、多少資源，答出來就填進「邏輯閘資源估算表」。

## 需要準備

| 項目 | 說明 |
|---|---|
| 動畫 | 下載學程的 `animations/` 資料夾，用瀏覽器開 `transmon-3d.html#surgery`（第 11 章邏輯閘；步驟 1–7 自動播放，步驟「8」是自由實驗）。免安裝、不需帳號 |
| 程式 | `magic_budget.py`：只要有 Python 3 就能跑，不需安裝套件、不需帳號 |
| 列印 | `02_列印包_邏輯閘資源估算表.pdf`（A4，共 4 頁） |
| 參考 | slides/transmon.pptx 第 25 頁（課綱寫 p26，實際內容在 p25）；docs/超導量子電腦師生對話教學紀錄.md 第 12 課 |

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片；先猜「表面碼把位元保護好了，那要怎麼對它做運算？」 | 影片、列印包第 1 頁 |
| 10–25 | 概念示範：橫向閘的限制、Clifford 與 T、合併與拆開、三步 CNOT、T 閘傳送、15-to-1 蒸餾 | 影片第 3–9 段、`05_動畫導覽.md` |
| 25–65 | 在第 11 章依序播放合併、拆開、CNOT（步驟 2–4），再到自由實驗跑蒸餾統計；填估算表 | `01_操作步驟.md`、列印包第 1 頁 |
| 65–75 | 休息 | |
| 75–105 | 孩子獨立改造：調高注入錯誤率，記錄接受率怎麼變；用程式對答案、改 MY_P 與 MY_T_COUNT | `magic_budget.py`、列印包第 2 頁、`03_蒸餾實驗紀錄.csv` |
| 105–115 | 角色互換：孩子教爸爸操作與原理，並指出一個限制 | 列印包第 3、4 頁 |
| 115–120 | 錄音總結、替邏輯閘資源估算表命名、存檔 | |

## 課前準備（約 20 分鐘）

- 自己先打開 `transmon-3d.html#surgery`，從步驟 1 看到步驟 7（自動接續，約 3 分鐘，左上方字幕逐句說明），再按步驟「8」進自由實驗。
- 在自由實驗依序按「準備接縫」→「合併（量 X_A·X_B）」→ 等看板量滿 3 輪 →「拆開」。
- 按「看魔術態工廠」→「跑一輪」；再把「注入錯誤率 p」拉到最右邊（約 0.050），按「跑 2000 次統計」。
- 跑一次 `python magic_budget.py`，確認「3 顆出錯：455 種排列中 35 種騙過檢查」與「要蒸餾 2 輪」。
- 讀一遍 `04_解答.md`。

## 評審（爸爸）的原則

- 每一格都追問「這個數字從哪裡來？」：從動畫看板、影片，還是程式？說得出來源才算答對。
- 最重要的一句：容錯量子電腦的成本主要在 T 閘與魔術態工廠；Pauli 幾乎免費，Clifford 用 lattice surgery，T 要消耗魔術態。

## 誠實說明

- 動畫的蒸餾抽樣是簡化模型（1、2 個輸入出錯必被抓到，3 個出錯有 35/455 的組合漏網，更多時當作隨機）；「跑 2000 次統計」每次結果略有不同。
- `magic_budget.py` 的 4 個檢查是 15-to-1 偵測錯誤的計數模型：每顆輸入編號 1～15，第 k 個檢查看編號二進位第 k 位是 1 的那 8 顆；騙過檢查的排列一律算成「輸出有錯」（保守估計）。它不是完整的量子電路模擬，但 p 小時輸出錯誤率和 35p³ 一致。
- 35p³、兩輪約 10⁻²¹、注入約 10⁻³、合併約 d μs、CNOT 約 2～3d 輪，依學程師生對話紀錄與動畫；T 閘傳送四種結果由程式逐一驗算。
- 「十億個 T 閘」只是估算練習的數量級（動畫寫「破解 RSA-2048 的 Toffoli 閘以十億計」），不是某個演算法的精確閘數。
''',

'01_操作步驟.md': '''# 操作步驟

## 上半場：合併、拆開、CNOT（約 40 分鐘）

1. 用瀏覽器開 `animations/transmon-3d.html#surgery`（第 11 章）。步驟 1 會自動播放並接續；左上方字幕逐句說明。
2. 步驟 2「合併」：看接縫位元準備在 |0⟩、新穩定子打開、看板「第 1 輪」到「第 3 輪」，以及金色標籤「X_A · X_B = ±1」。
3. 步驟 3「拆開」：接縫位元閃白光（「量 Z」），兩塊補丁恢復獨立。
4. 步驟 4「CNOT」：看板依序亮起 ① 量 Z_C ⊗ Z_A、② 量 X_A ⊗ X_T、③ 單獨量 A 的 Z、④ 補 Pauli 修正。
5. 步驟 5「T 閘傳送」：看板最後一行寫這次要不要補 S（隨機）。
6. 按步驟「8」自由實驗，自己按「準備接縫」→「合併（量 X_A·X_B）」→「拆開」；按「重設」再做一次，看個別的 ±1 有沒有變、乘積有沒有變。
7. 每做完一項，就填列印包第 1 頁「邏輯閘資源估算表」的一列。

## 下半場：調高注入錯誤率（約 30 分鐘）

1. 自由實驗按「看魔術態工廠」，先在 p = 1.0×10⁻³ 按「跑一輪」，看 15 顆球飛進工廠、4 盞燈、金色球。
2. 按「跑 2000 次統計」，把接受率填進列印包第 2 頁。
3. 把「注入錯誤率 p」滑桿往右拉（例如 10⁻²、0.020、0.040、0.050），每一格都跑一次統計，記錄接受率與「接受中出錯」。
4. 按「2 輪」，看第一輪的輸出變成第二輪的輸入，記下輸出錯誤率與消耗（15 × 15 = 225 顆）。
5. 執行 `python magic_budget.py`，對照「三、注入錯誤率 p → 接受率」。改 `MY_P = 0.04` 成你在動畫試的 p，再跑一次。
6. 改 `MY_T_COUNT`（例如 `10 ** 6`、`10 ** 12`），看要蒸幾輪、總共耗多少注入態，填進估算表最後一列。
''',
}

FILES.update({
'magic_budget.py': PROGRAM,

'04_解答.md': '# 解答（爸爸用）\n\n## 邏輯閘資源估算表\n\n| 邏輯運算 | 做法 | 時間或代價 |\n|---|---|---|\n'
  + ''.join(f'| {a} | {b} | {c} |\n' for a, b, c in COSTS)
  + '\n- 合併時新 X 穩定子的個別結果是隨機的 ±1，乘積才是 X_A ⊗ X_B；量 d 輪是因為量測本身也會錯，要讓解碼器在時間方向上抓錯。\n'
  '- 拆開後，個別結果只需要 Pauli 修正，記在軟體裡（Pauli frame）。\n'
  '- 為什麼第 7～9 章的演算法都能被古典電腦模擬？它們只用 Clifford 閘（H、X、Z、CZ、CNOT），依 Gottesman–Knill 定理可有效模擬。\n'
  '\n## magic_budget.py 實跑（Python 3.13.18）\n\n```\n' + RUN_OUTPUT + '```\n\n'
  '- T 閘傳送：Z⊗Z = −1 的那一半要補 S（S = T²，所以 S·T† = T）；X = −1 只要補相位翻轉（Pauli，記帳就好）。\n'
  '- 1、2 顆出錯一定被 4 個檢查抓到；3 顆出錯的 455 種排列裡有 35 種騙過，這就是 35p³ 的 35。\n'
  '- 注入錯誤率 10⁻⁴ 蒸一輪：35 × (10⁻⁴)³ = 3.5×10⁻¹¹。\n'
  '- 調高 p：接受率從 98.5%（10⁻³）掉到約 46.6%（5%）、22%（10%）；輸出仍比輸入乾淨，但丟掉的原料越來越多。動畫看板的接受率用 (1 − p)¹⁵ 近似（p = 0.050 時 46.2%）。\n'
  '- 十億個 T 閘：一輪後每顆 3.5×10⁻⁸，全部加起來還會錯約 35 次；兩輪後 1.5×10⁻²¹，每顆魔術態平均約耗 228 顆注入態（15 × 15 再除以接受率）。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載整個資料夾後用瀏覽器開啟，不需要網路、伺服器或帳號。

## `transmon-3d.html#surgery`（第 11 章：Lattice surgery 與魔術態蒸餾）

- 圖例：圓球 = 資料位元（中間一行是接縫）；青色格子 = Z 穩定子、琥珀色格子 = X 穩定子，亮框是合併時新打開的穩定子，亮起 = 量到 −1；工廠裡橘色球 = 注入的髒魔術態、金色球 = 蒸餾後的乾淨魔術態、紅色 = 有錯。
- 步驟 1～8：為什麼、合併、拆開、CNOT、T 閘傳送、蒸餾、第二輪與工廠、自由實驗。「◀ 上一步」「暫停」「重播」「下一步 ▶」與「自動接續」。
- 自由實驗：「看 lattice surgery」「看魔術態工廠」；「準備接縫」「合併（量 X_A·X_B）」「拆開」「重設」；「注入錯誤率 p」滑桿（10⁻⁴ 到約 0.050）；輪數「1 輪」「2 輪」；「跑一輪」「跑 2000 次統計」。面板「補丁狀態」「量到的 X_A·X_B」「蒸餾」。
- 上方看板：lattice surgery 視角顯示每一輪的個別結果與乘積；工廠視角顯示輸入 → 輸出（35p³）、接受率 (1 − p)¹⁵、消耗，以及「注入／1 輪／2 輪／Shor 需要」四根錯誤率柱子（對數，越矮越乾淨）。

## 操作

滑鼠拖曳旋轉、滾輪縮放；transmon-3d 下方可切換十二章，左右方向鍵也能換章。
''',
})

SHEET_HEADER = ['注入錯誤率 p', '輪數', '看板的輸出錯誤率', '2000 批中接受幾批', '接受率', '接受中出錯幾批', '我的觀察']
SHEET_ROWS = [['1.0×10⁻³', '1', '', '', '', '', ''], ['1.0×10⁻²', '1', '', '', '', '', ''], ['0.020', '1', '', '', '', '', ''],
              ['0.040', '1', '', '', '', '', ''], ['0.050', '1', '', '', '', '', ''], ['0.050', '2', '', '', '', '', '']]

EXTRA_CSS = '''table.judge td{height:17mm;font-size:11pt}table.judge td.k{font-weight:bold;color:#0b2540}
table.rec td{height:9mm}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
pre.code{font-size:9pt;background:#f2f6fa;border:1pt solid #cfdde8;padding:3mm;margin:2mm 0;white-space:pre-wrap}'''


def check_program():
    """真的跑一次 magic_budget.py（隔離模式），確認輸出和影片、教材寫的結果一致。"""
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / 'magic_budget.py'
        p.write_text(PROGRAM, encoding='utf-8')
        out = subprocess.run([sys.executable, '-I', str(p)], capture_output=True, text=True, check=True,
                             env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}).stdout
    assert out == RUN_OUTPUT, out
    return out


def html():
    rows = ''.join(f'<tr><td class="k">{a}</td><td></td><td></td><td></td></tr>' for a, b, c in COSTS)
    pages = [
        '<h2>邏輯閘資源估算表</h2><p class="lead">在 transmon-3d.html#surgery 依序看合併、拆開、CNOT、T 閘傳送與蒸餾；每答出一格，就說出數字從哪裡來。</p>'
        '<p>開場先猜：表面碼把位元保護好了，要怎麼對它做運算？＿＿＿＿＿＿＿＿＿＿＿＿＿＿</p>'
        '<table class="judge"><tr><th style="width:22%">邏輯運算</th><th style="width:34%">做法</th><th style="width:22%">時間或代價</th>'
        '<th style="width:22%">數字從哪裡來</th></tr>'
        + rows + '<tr><td class="k">MY_T_COUNT 個 T 閘</td><td></td><td></td><td></td></tr></table>'
        '<p class="note">合併時量到的是什麼？ □ 每顆位元的 0／1　□ 兩顆邏輯位元的聯合奇偶 X_A·X_B　　合併要量幾輪？＿＿ 輪</p>',
        '<h2>工程答辯：注入越髒會怎樣？</h2><p class="lead">在自由實驗「看魔術態工廠」，調「注入錯誤率 p」，每一格按「跑 2000 次統計」。</p>'
        '<table class="rec"><tr>' + ''.join(f'<th>{h}</th>' for h in SHEET_HEADER) + '</tr>'
        + ''.join(f'<tr><td>{r[0]}</td><td>{r[1]}</td><td></td><td></td><td></td><td></td><td></td></tr>' for r in SHEET_ROWS) + '</table>'
        '<pre class="code">MY_P = 0.04            # 改造區 1：注入錯誤率（調高看看接受率怎麼變）\nMY_T_COUNT = 10 ** 9   # 改造區 2：資源估算——演算法要用幾個 T 閘</pre>'
        '<p class="note">p 變大時，接受率 □ 變高　□ 變低；輸出還比輸入乾淨嗎？＿＿＿＿　程式說 3 顆出錯的 455 種排列裡有＿＿＿種騙過檢查。</p>',
        '<h2>三個容易錯的地方</h2><div class="box"><ul class="chk">'
        '<li>以為 lattice surgery 會搬動位元：其實只改變「這一輪量哪些穩定子」</li>'
        '<li>以為合併時每個新穩定子的結果有意義：個別結果隨機，乘積才是 X_A·X_B</li>'
        '<li>以為所有邏輯閘一樣貴：成本主要在 T 閘與魔術態工廠</li></ul></div>'
        '<div class="box" style="margin-top:5mm"><h3>數一數</h3>'
        '<p>15-to-1：＿＿ 顆髒的進、＿＿ 顆乾淨的出；工廠頂上有 ＿＿ 盞檢查燈</p>'
        '<p>輸出錯誤率約 35p³：p = 10⁻³ → ＿＿＿＿＿＿；p = 10⁻⁴ → ＿＿＿＿＿＿</p>'
        '<p>CNOT = 一塊輔助補丁 + ＿＿ 次聯合量測；T 閘 = ＿＿ 顆魔術態 + Clifford 運算</p>'
        '<p>我最容易搞錯的一點：</p><div class="line"></div><div class="line"></div></div>',
        '<h2>最後一關：答辯邏輯閘成本</h2><div class="box"><p>作品名稱：＿＿＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p>'
        '<p>1. lattice surgery 怎麼量出兩顆邏輯位元的聯合奇偶？</p><div class="line"></div>'
        '<p>2. 為什麼 T 閘要靠魔術態？為什麼魔術態要蒸餾？</p><div class="line"></div>'
        '<p>3. 容錯量子電腦的成本主要花在哪裡？</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><ul class="chk">'
        '<li>不看稿說出：合併 → 量 d 輪 → 拆開；T 閘 = 魔術態 + 閘傳送</li><li>在自由實驗示範合併與拆開，並解釋看板上的乘積</li>'
        '<li>說出數字：15 顆換 1 顆、35p³、兩輪耗 225 顆</li><li>指出一個限制：成本主要在 T 閘與魔術態工廠</li>'
        '<li>替邏輯閘資源估算表取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q110 邏輯閘資源估算表 列印包', '父子科技學院 量子電腦學程 Q110｜第 12 課：lattice surgery 與魔術態蒸餾', pages, EXTRA_CSS)


if __name__ == '__main__':
    check_program()
    classroom_pack.build(
        slug='q110-lattice-surgery', folder='Q110_lattice_surgery與魔術態蒸餾', files=FILES,
        sheet=('03_蒸餾實驗紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_邏輯閘資源估算表.pdf', pack_pages=4,
        pack_needles=('邏輯閘資源估算表', '工程答辯', 'MY_P', 'MY_T_COUNT', '容易錯', '魔術態', '最後一關'),
        authoring_dir=XINEW / 'authoring/q110', episode_dir='specials/q110-lattice-surgery',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': 'no（瀏覽器開動畫；magic_budget.py 只需 Python 3）',
               'program': 'magic_budget.py', 'testedWith': 'Python 3.13.18 (standard library only)',
               'recordedRun': {'tGateTeleportOutcomes': 4, 'tGateTeleportAllCorrect': True,
                               'sneakyPatterns': {'1': 0, '2': 0, '3': 35, '4': 105},
                               'acceptPercent': {'1e-4': 99.9, '1e-3': 98.5, '1e-2': 86.0, '0.05': 46.6, '0.1': 22.0, '0.04': 54.4},
                               'distillRoundsFor1e9T': 2, 'injectedPerMagicState': 228.4},
               'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q110/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')
