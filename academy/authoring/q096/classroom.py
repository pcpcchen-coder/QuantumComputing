"""Q096 課堂教材：畢業 Teach-back：換孩子教爸爸 — 十分鐘教學設計表、工作坊被問倒紀錄、錄影與公開前檢查表、說明卡與評分參考。

免安裝、不需帳號：教學示範可用學程的 animations/ 任一場景（範例：operation.html#interference），用瀏覽器開啟；錄影用家中手機或電腦即可。

    cd $XINEW_ACADEMY && XINEW_CHROME=/path/to/chrome-headless-shell \
      ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q096/classroom.py
"""
from pathlib import Path
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import classroom_pack  # noqa: E402
import printpack  # noqa: E402

HERE = Path(__file__).resolve().parent

# 本集建議的十分鐘教學骨架（教學建議，不是課綱規定）
OUTLINE = [('開場問題', 1, '丟出一個問題，讓爸爸好奇'), ('核心原理', 3, '用自己的話講清楚一個原理'),
           ('動畫示範', 4, '先讓爸爸預測，再操作場景對答案'), ('限制＋總結', 2, '一個常見錯誤或限制、總結、念出來源')]
TOTAL_MIN = sum(m for _, m, _ in OUTLINE)
assert TOTAL_MIN == 10

CHECKS = ['影片在十分鐘以內', '字幕逐句對齊、沒有錯字', '片尾列出所有來源（含學程動畫與簡報）',
          '畫面沒有姓名、學校、住址、制服等個資', '音樂、圖片都有授權或自己做的', '爸爸從頭看過一遍', '公開與否由爸媽決定']

FILES = {
'00_爸爸先讀.md': f'''# 父子科技學院 量子電腦學程 Q096：畢業 Teach-back：換孩子教爸爸（爸爸先讀）

這是依課綱製作的課前教學版，不是實際上課錄音。今天換孩子當老師：用上一堂（Q095）做好的專題和一個動畫場景，教爸爸一個量子主題，最後錄成十分鐘教學影片。

需要：瀏覽器（開學程的 `animations/` 場景）、手機或電腦錄影。不需要網路、帳號或安裝。

| 分鐘 | 做什麼 | 用到的教材 |
|---|---|---|
| 00–10 | 一起看影片 | 影片 |
| 10–25 | 十分鐘教學的四段骨架、唸稿和真的教的差別 | 影片第 3–6 段、列印包第 1 頁 |
| 25–65 | 畢業工作坊：孩子當老師，爸爸當學生發問 | 列印包第 1–2 頁 |
| 65–75 | 休息 | |
| 75–105 | 重錄成十分鐘短片，加字幕和來源 | `01_操作步驟.md`、列印包第 3 頁 |
| 105–115 | 孩子教爸爸操作與原理 | 列印包第 4 頁 |
| 115–120 | 錄音總結、作品命名、存檔 | |

## 爸爸的角色

- 當一個好學生：真的聽、真的問「為什麼」。每個被問倒的問題請孩子記在列印包第 2 頁。
- 可以故意說錯一次（例如「量子電腦就是同時試所有答案」），看孩子能不能發現並更正。
- 不要搶著講答案；孩子卡住時，只問「你可以換個說法嗎？」。

## 公開之前（本課最重要的注意事項）

- 影片要不要公開，由爸媽決定。公開前檢查：姓名、學校、住址、制服等個資；音樂、圖片的授權。
- 不確定能不能用的素材，就不要用。只給家人看的版本，就不要公開分享。

## 誠實說明

- 「一分、三分、四分、兩分」的十分鐘骨架是本集的建議，可以依主題調整。
- 課綱列的「發表模板」以列印包第 1 頁的教學設計表代替。
''',

'01_操作步驟.md': '''# 操作步驟

## A. 選主題（約 10 分鐘）

1. 拿出 Q095 的專題作品，挑一個你最有把握的原理（例如疊加、干涉、糾纏、錯誤更正）。
2. 挑一個能說明它的動畫場景，寫在列印包第 1 頁。範例：`animations/operation.html#interference`。

## B. 排十分鐘（約 15 分鐘）

照列印包第 1 頁的四段骨架，每段只寫三到五個關鍵字，不寫逐字稿。

## C. 畢業工作坊（約 40 分鐘）

1. 孩子站在螢幕前教，爸爸當學生，可以隨時舉手。
2. 示範段一定要「先讓爸爸預測，再按按鈕」。
3. 每被問倒一次，記在列印包第 2 頁。

## D. 錄成短片（約 30 分鐘）

1. 根據被問倒的問題修改，再重錄一次，控制在十分鐘以內。
2. 剪掉講錯和停頓太久的地方，加上字幕。
3. 片尾列出所有來源（學程動畫、簡報、別人的圖片或數字）。
4. 用列印包第 3 頁逐項檢查，交給爸爸從頭看一遍。
''',

'04_解答.md': '# 評分參考（爸爸用）\n\n## 十分鐘骨架（本集建議）\n\n| 段落 | 分鐘 | 重點 |\n|---|---|---|\n'
  + ''.join(f'| {n} | {m} | {d} |\n' for n, m, d in OUTLINE)
  + f'| 合計 | {TOTAL_MIN} | |\n\n'
  '## 驗收三件事（課綱）\n\n- 完成「10 分鐘教學影片」。\n- 能不用看稿說出核心原理。\n'
  '- 能指出至少一個錯誤、限制或注意事項（例如：公開影片前由家長審核個資與授權）。\n\n'
  '## 好的教學通常有\n\n- 開場是一個問題，而不是一個定義。\n- 示範前先讓學生預測。\n- 至少一個專題裡的測試或驗證當證據。\n'
  '- 說得出一個限制或常見誤解。\n- 片尾有來源。\n\n'
  '## 範例：用干涉場景教（operation.html#interference）\n\n'
  '- 相位 φ = 0：通往結果 |1⟩ 的兩支箭頭方向相反、抵消，結果一定是 0；φ = 180°：反過來，結果一定是 1。\n'
  '- 打開「A：中途偵測路徑（破壞干涉）」：干涉消失，結果變成 50/50。\n'
  '- 一句話解釋：振幅有方向，先相加再平方成機率，所以可以互相抵消。\n',

'05_動畫導覽.md': '''# 動畫導覽

學程的互動動畫在 pcpcchen-coder/QuantumComputing 的 `animations/` 資料夾，下載後用瀏覽器開啟，不需要網路或帳號。孩子可以從任一場景挑一個當教材，以下是範例。

## `operation.html#interference`（操作場景 8：干涉）

- 單選：單一量子位元：兩條路徑、3 位元：8 條路徑（Deutsch–Jozsa）。
- 滑桿「A：相位 φ」0–360°；開關「A：自動掃描 φ」「A：中途偵測路徑（破壞干涉）」。
- 右側兩個結果圓：藍、橙是兩條路徑的貢獻，白色是總和；插圖是 P(0) 與 φ 的干涉條紋，白點是目前的 φ。

## 操作

`H` 隱藏面板；滑鼠拖曳旋轉、滾輪縮放。錄影時先按 `H`，畫面比較乾淨。
''',
}

SHEET_HEADER = ['項目', '段落／問題', '分鐘', '關鍵字', '被問倒的問題', '我的補強', '完成']
SHEET_ROWS = ([[f'骨架', n, str(m), '', '', '', ''] for n, m, _ in OUTLINE]
              + [[f'被問倒第 {i} 題', '', '', '', '', '', ''] for i in range(1, 9)]
              + [['錄影檢查', c, '', '', '', '', ''] for c in CHECKS])

EXTRA_CSS = '''table.rec td{height:9mm}.chk li{margin:2.5mm 0;font-size:13pt;list-style:none}.chk li:before{content:"□ "}.chk{padding-left:2mm}
.card{border:2pt solid #0b2540;border-radius:4mm;padding:5mm;margin-top:5mm}.card h3{margin-top:0}'''


def html():
    pages = [
        '<h2>十分鐘教學設計表</h2><p class="lead">主題：＿＿＿＿＿＿＿＿＿＿　用到的場景：＿＿＿＿＿＿＿＿＿＿。每段只寫關鍵字，不寫逐字稿。</p>'
        '<table class="rec"><tr><th>段落</th><th>分鐘</th><th>要做的事</th><th>我的關鍵字</th></tr>'
        + ''.join(f'<tr><td>{n}</td><td>{m}</td><td>{d}</td><td></td></tr>' for n, m, d in OUTLINE) + '</table>'
        '<div class="card"><h3>開場問題（第一分鐘）</h3><div class="line"></div>'
        '<h3>我的證據：專題裡的測試或驗證</h3><div class="line"></div>'
        '<p>作品名稱：＿＿＿＿＿＿＿＿＿＿　日期：＿＿＿＿＿＿</p></div>',
        '<h2>畢業工作坊：被問倒紀錄</h2><p class="lead">你當老師，爸爸當學生。每被問倒一次就記下來，這些就是下一版要補強的地方。</p>'
        '<table class="rec"><tr><th>#</th><th>爸爸問了什麼</th><th>我當時怎麼回答</th><th>下一版怎麼補強</th></tr>'
        + ''.join(f'<tr><td>{i}</td><td></td><td></td><td></td></tr>' for i in range(1, 9)) + '</table>'
        '<p class="note">爸爸故意說錯的那一句是：＿＿＿＿＿＿＿＿　我有發現嗎？□ 有　□ 沒有</p>',
        '<h2>錄影與公開前檢查表</h2><p class="lead">重錄成十分鐘短片之後，逐項打勾，再交給爸爸從頭看一遍。</p>'
        '<ul class="chk">' + ''.join(f'<li>{c}</li>' for c in CHECKS) + '</ul>'
        '<div class="card"><h3>片尾來源清單</h3><div class="line"></div><div class="line"></div><div class="line"></div></div>'
        '<p class="note">生活技能：教學相長與傳承——教的人也在學。你想把今天學到的教給誰？＿＿＿＿＿＿＿＿</p>',
        '<h2>說明卡與最後一關</h2><div class="box"><p>1. 我教的主題，核心原理是什麼？</p><div class="line"></div>'
        '<p>2. 十分鐘的教學分成哪四段？</p><div class="line"></div><p>3. 為什麼示範前要先讓學生預測？</p><div class="line"></div>'
        '<p>4. 一個限制或注意事項：</p><div class="line"></div></div>'
        '<div class="box" style="margin-top:5mm"><h3>最後一關：畢業驗收</h3><ul class="chk">'
        '<li>完成十分鐘教學影片</li><li>不看稿說出核心原理</li>'
        '<li>說出四段骨架：問題、原理、示範、總結</li><li>指出一個注意事項：公開前由爸媽審核個資與授權</li>'
        '<li>替教學影片取名字、存檔</li></ul></div>',
    ]
    return printpack.document('Q096 畢業 Teach-back 列印包', '父子科技學院 量子電腦學程 Q096｜畢業 Teach-back：換孩子教爸爸', pages, EXTRA_CSS)


if __name__ == '__main__':
    classroom_pack.build(
        slug='q096-graduation-teach-back', folder='Q096_畢業TeachBack', files=FILES,
        sheet=('03_教學設計與檢查紀錄.csv', SHEET_HEADER, SHEET_ROWS),
        pack_html=html(), pack_pdf='02_列印包_畢業TeachBack.pdf', pack_pages=4,
        pack_needles=('十分鐘教學設計表', '被問倒紀錄', '公開前檢查表', '說明卡', '最後一關'),
        authoring_dir=XINEW / 'authoring/q096', episode_dir='specials/q096-graduation-teach-back',
        extra={'activityMinutes': 120, 'needsAccount': False, 'needsInstall': False,
               'scenes': ['animations/operation.html#interference'],
               'outlineMinutes': {n: m for n, m, _ in OUTLINE}, 'factsFrom': 'production/fact-check.md'})
    (HERE / 'print').mkdir(exist_ok=True)
    (HERE / 'print/print-pack.html').write_text((XINEW / 'authoring/q096/print/print-pack.html').read_text(encoding='utf-8'), encoding='utf-8')
