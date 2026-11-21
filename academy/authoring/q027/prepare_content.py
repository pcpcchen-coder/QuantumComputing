"""Q027 SQUID：用磁場轉頻率 — production sources (12 scenes / 36 sentences).

    cd $XINEW_ACADEMY && ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q027/prepare_content.py
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import qbuild  # noqa: E402

HERE = Path(__file__).resolve().parent
LESSON, SLUG, CHECKED = 'Q027', 'q027-squid-flux-tuning', '2026-11-18'
TITLE = 'SQUID：用磁場轉頻率'
TOPIC = 'SQUID：用磁場轉頻率'
REPO = 'pcpcchen-coder/QuantumComputing'
SRC = {
    'curriculum': f'{REPO} academy/lessons/Q027/lesson.json',
    'neighbors': f'{REPO} academy/lessons/Q026/brief.md、academy/lessons/Q028/brief.md',
    'jj_talk_p15': f'{REPO} slides/JJ_Microwave_Readout_Talk.pptx p15（兩個能量尺度的表格）',
    'jj_talk_p17': f'{REPO} slides/JJ_Microwave_Readout_Talk.pptx p17（含講者備註）',
    'transmon_p20': f'{REPO} slides/transmon.pptx p20（含講者備註；課綱寫 p21，但 p21 是第 7 章振幅長條，SQUID 調頻的案例在 p20）',
    'squid_scene': f'{REPO} animations/index.html#squid（animations/js/scenes/06_squid.js）',
    'tr_case': f'{REPO} animations/transmon-3d.html#case（第 6 章「三顆可調 transmon 的頻率配置」）',
    'dlg': f'{REPO} docs/超導量子電腦師生對話教學紀錄.md 第 1–3 課',
    'wiki_squid': 'https://en.wikipedia.org/wiki/SQUID',
}
SOURCE_RECORDS = [
    {'id': 'curriculum', 'title': '量子電腦學程 Q027 課綱', 'publisher': REPO, 'url': SRC['curriculum'],
     'usedFor': '主題、學習目標（知道兩個 JJ 並聯成環可以用磁通調整頻率，認識甜蜜點）、動手任務（在場景把量子位元調到指定頻率，並找出對磁通雜訊最不敏感的點）、'
                '孩子獨立改造（比較對稱與不對稱 SQUID 的調頻範圍）、好玩機制（闖關：調到指定頻率）、作品（調頻曲線）、家長課前準備（index.html#squid）、'
                '120 分鐘流程、驗收與常見誤解（可調 = 多一個雜訊入口；甜蜜點是一階不敏感，不是完全不受影響）、生活技能支線（在可調性與穩定性之間取捨）'},
    {'id': 'neighbors', 'title': '量子電腦學程 Q026、Q028 課綱', 'publisher': REPO, 'url': SRC['neighbors'],
     'usedFor': '上一堂：傾斜洗衣板（在場景加大偏壓電流，記錄粒子何時從井中滑出）；'
                '下一堂：量子位元家族圖鑑（比較 transmon、fluxonium、電荷與相位量子位元的結構與優缺點）'},
    {'id': 'jj_talk_p15', 'title': '超導量子電腦的核心：JJ 與微波讀取（簡報）p15：兩個能量尺度：EJ 與 EC', 'publisher': REPO, 'url': SRC['jj_talk_p15'],
     'usedFor': '表「約瑟夫森能 EJ｜EJ = Φ0 Ic / 2π = ħ Ic / 2e」（與臨界電流成正比）、「充電能 EC｜EC = e² / 2CΣ｜總電容 CΣ（含大電容板）」（由電容決定）'},
    {'id': 'jj_talk_p17', 'title': '超導量子電腦的核心：JJ 與微波讀取（簡報）p17：SQUID：用磁通調整的 JJ', 'publisher': REPO, 'url': SRC['jj_talk_p17'],
     'usedFor': 'EJ(Φ) = EJΣ |cos(πΦ/Φ0)| √(1 + d² tan²(πΦ/Φ0))；兩個 JJ 並聯成環 = 一個臨界電流可調的 JJ；用晶片上的 Z 線通電流產生磁通 → 即時調頻；'
                '甜蜜點 Φ = 0：df/dΦ = 0，對磁通雜訊一階免疫；不對稱 SQUID 縮小調頻範圍、降低雜訊敏感度；備註：週期剛好是一個 Φ0、奈秒尺度內調整頻率、'
                '用來做雙量子位元閘或避開有缺陷的頻率、對稱 SQUID 在半個 Φ0 處頻率掉到零、通常讓量子位元停在甜蜜點'},
    {'id': 'transmon_p20', 'title': 'Transmon 筆記簡報 p20：案例：三顆可調 transmon 的頻率配置', 'publisher': REPO, 'url': SRC['transmon_p20'],
     'usedFor': '② SQUID 調頻：E_J(Φ) = E_J,max |cos(πΦ/Φ₀)|，用 Z 線磁通把頻率往下調；③ Q2 留在 sweet spot；備註：用 SQUID 加 Z 線磁通把頻率調開，給每顆位元一個地址'},
    {'id': 'squid_scene', 'title': 'JJ 與微波讀取 3D 場景 6：DC SQUID：可用磁通調整的 JJ', 'publisher': REPO, 'url': SRC['squid_scene'],
     'usedFor': '動畫段三段與實作：滑桿「外加磁通 Φ / Φ₀」−1～1（初值 0.25）、「接面不對稱度 d」0～0.8；讀數（等效 E_J/h、f₀₁、磁通敏感度 df/dΦ、甜蜜點字樣）；'
                '右下小圖「量子位元頻率 f₀₁ 與外加磁通」（E_JΣ/h = 20 GHz、E_C/h = 250 MHz）；文中頻率數值都以同一段公式重算'},
    {'id': 'tr_case', 'title': 'Transmon 3D 第 6 章：案例：三顆可調 transmon 的頻率配置（#case）', 'publisher': REPO, 'url': SRC['tr_case'],
     'usedFor': '步驟 ② 字幕「最高點 Φ = 0 就是 sweet spot，所以頻率只能往下調」「離開 sweet spot 時，磁通雜訊讓頻率抖動（dephasing）」；教材動畫導覽'},
    {'id': 'dlg', 'title': '超導量子電腦師生對話教學紀錄 第 1–3 課', 'publisher': REPO, 'url': SRC['dlg'],
     'usedFor': '第 1 課：電流分兩條路各穿過一個 JJ 再匯合，很像雙狹縫干涉；I_c(Φ) = 2I_c₀|cos(πΦ/Φ₀)|；可調 transmon 的代價是磁通雜訊變成頻率抖動，對策是待在 sweet spot 或用不對稱 SQUID；'
                '第 2 課：Z 線磁通讓 E_J(Φ) = E_J,max|cos(πΦ/Φ₀)|；第 3 課：SQUID 只能往下調（最高在 Φ = 0），所以 E_J 要刻意做大一點；用途包括閃避缺陷、做 CZ'},
    {'id': 'wiki_squid', 'title': 'Wikipedia: SQUID', 'publisher': 'Wikipedia', 'url': SRC['wiki_squid'],
     'usedFor': 'superconducting quantum interference device，是非常靈敏的磁力計；DC SQUID 於 1964 年由 Ford Research Labs 的 Jaklevic、Lambe、Mercereau、Silver 發明；'
                '兩個約瑟夫森接面並聯在一個超導環上；響應以一個磁通量子為週期'},
]

SCENES = [
 ('SQUID：用磁場轉頻率', [
  '歡迎回到父子科技學院的量子電腦學程，我是陳犀牛，今天是量子第二十七堂，超導量子干涉元件：用磁場轉頻率，這是依課綱製作的課前教學版，並非實際上課錄音。',
  '上一堂在傾斜的洗衣板上看到，偏壓電流一加大，相位小球就會滑出山谷；今天換一個旋鈕，改用磁場來調約瑟夫森接面。',
  '我們會把兩個接面並聯成一個環，用穿過環的磁通，把量子位元的頻率調高調低，還要找出最不怕磁通雜訊的那個點。'], ['curriculum', 'neighbors', 'jj_talk_p17']),
 ('三個重點', [
  '今天有三個重點：第一，兩個約瑟夫森接面並聯成環，就像一個臨界電流可以調的接面。',
  '第二，穿過環的磁通會改變約瑟夫森能量，頻率跟著變，每隔一個磁通量子重複一次；第三，曲線最高的甜蜜點，斜率是零，對磁通雜訊最不敏感。',
  '今天的作品是一條調頻曲線，還要玩一個闖關遊戲：把量子位元調到指定的頻率。'], ['curriculum', 'jj_talk_p17']),
 ('兩個接面並聯成環', [
  '超導量子干涉元件的英文縮寫，拼起來剛好是魷魚這個英文字；它本身是一種極靈敏的磁場感測器。',
  '它的結構很簡單：一個超導環，左右各夾一個約瑟夫森接面，兩個接面是並聯的。',
  '一九六四年，美國福特公司研究實驗室的科學家發明了這種直流的超導量子干涉元件；放進量子位元裡，它就是一個可以調的接面。'], ['wiki_squid', 'jj_talk_p17', 'dlg']),
 ('兩條路的干涉', [
  '電流從環的一邊進來，分成兩條路，各穿過一個接面，再在另一邊會合，很像光的雙狹縫干涉。',
  '穿過環的磁通，會讓兩條路的相位錯開；兩路超導電流合在一起，能通過的最大電流，就隨著磁通變大變小。',
  '磁通是零，兩路完全同步，臨界電流最大；磁通加到半個磁通量子，兩個一樣的接面剛好互相抵消，臨界電流變成零。'], ['dlg', 'jj_talk_p17', 'wiki_squid']),
 ('磁通 → 能量 → 頻率', [
  '約瑟夫森能量和臨界電流成正比，所以磁通一改變，約瑟夫森能量就跟著變。',
  '充電能量由電容決定，磁通調不動它；頻率大約等於八倍約瑟夫森能量乘上充電能量，再開根號，減掉充電能量。',
  '動畫用的數字是：兩個接面合起來的約瑟夫森能量二十吉赫、充電能量兩百五十兆赫；磁通是零時頻率約六點零七吉赫，四分之一個磁通量子時約五點零七吉赫。'],
  ['jj_talk_p15', 'jj_talk_p17', 'dlg', 'squid_scene']),
 ('晶片上的磁通控制線', [
  '真正的晶片上，每顆可調的量子位元旁邊，都有一條磁通控制線，通一點電流，就能改變穿過小環的磁通。',
  '頻率可以在奈秒的時間內調好，用來把兩顆量子位元調到共振做雙量子位元閘，或是避開有缺陷的頻率。',
  '要注意，頻率最高的地方在磁通是零，所以只能往下調；設計時會刻意把約瑟夫森能量做大一點，留出往下調的空間。'], ['jj_talk_p17', 'transmon_p20', 'dlg', 'tr_case']),
 ('甜蜜點', [
  '調頻曲線最高的地方叫甜蜜點：在那裡，頻率對磁通的斜率剛好是零，動畫面板叫它磁通敏感度。',
  '斜率是零，代表磁通抖一點點，頻率幾乎不動，這叫對磁通雜訊一階不敏感，所以通常讓量子位元停在這裡。',
  '用動畫的公式算：同樣抖百分之一個磁通量子，在甜蜜點頻率只差一點六兆赫，在四分之一個磁通量子的地方，卻差了八十六兆赫。'], ['jj_talk_p17', 'squid_scene', 'tr_case']),
 ('可調也有代價', [
  '第一個要注意的地方：可以調，就多了一個雜訊的入口，磁通一抖，頻率跟著抖，量子位元的相位就慢慢亂掉。',
  '第二，甜蜜點只是一階不敏感，不是完全不受影響：從零拉到百分之二個磁通量子，頻率還是降了大約六兆赫。',
  '暫停影片想一想：如果一定要把量子位元停在甜蜜點以外的地方，有什麼辦法讓它比較不怕磁通雜訊？'], ['curriculum', 'dlg', 'tr_case', 'squid_scene']),
 ('實作：調頻闖關', [
  '實作的時候，父子一起打開超導量子干涉元件的動畫場景，左邊面板有外加磁通的滑桿，下面的讀數會寫出頻率。',
  '爸爸出題，例如五點五吉赫，孩子拉滑桿，讓讀數落在目標上下零點零五吉赫以內就算過關，每過一關記下磁通和頻率。',
  '最後把所有點畫成調頻曲線，再找出磁通敏感度等於零的那一格，那就是甜蜜點。'], ['curriculum', 'squid_scene']),
 ('換你改造：不對稱的環', [
  '下半場換你：比較對稱和不對稱的超導量子干涉元件，看看調頻範圍差多少。',
  '把接面不對稱度從零拉到零點六，最高頻率還是六點零七吉赫，但半個磁通量子的地方不再掉到零，只降到四點六五吉赫。',
  '調頻範圍從六吉赫多縮小到一點四吉赫左右，換來整條曲線比較平、比較不怕雜訊；這就是可調性和穩定性的取捨。'], ['curriculum', 'squid_scene', 'jj_talk_p17', 'dlg']),
 ('兩小時的調頻闖關工坊', [
  '兩小時的安排是：開場十分鐘，概念示範十五分鐘，接著四十分鐘一起闖關調頻、畫出調頻曲線並找甜蜜點，然後休息十分鐘。',
  '下半場三十分鐘，你比較對稱和不對稱的環；接著十分鐘交換角色，由你教爸爸操作和原理。',
  '最後五分鐘錄音總結，替你的調頻曲線取個名字，再存一個版本。'], ['curriculum']),
 ('最後一關：教爸爸調頻率', [
  '最後一關，請不看稿說出：兩個接面並聯成環，為什麼能用磁通調頻率？甜蜜點在哪裡、為什麼特別？',
  '再指出一個要注意的地方：可以調就多一個雜訊入口；甜蜜點只是一階不敏感，不是完全不受影響。',
  '今天的作品是調頻曲線，下一堂要做量子位元家族圖鑑，比較幾種超導量子位元的結構和優缺點；我是陳犀牛，保持好奇，我們下次見！'], ['curriculum', 'neighbors']),
]

VISIBLE = [
 ['量子電腦學程 第二十七堂', 'SQUID\n用磁場轉頻率', '兩個接面圍成環，磁通就是頻率旋鈕', '量子第二十七堂  ·  依課綱製作的課前教學版'],
 ['三個重點', '一個環、一個旋鈕、一個甜蜜點',
  '01 可調的接面', '兩個 JJ\n並聯成環', '→', '02 磁通調頻', '週期一個 Φ₀\n只能往下調', '→', '03 甜蜜點', '斜率為零\n一階不敏感',
  '今天的作品：調頻曲線'],
 ['兩個接面並聯成環', '超導量子干涉元件（DC SQUID）',
  '01', '本身是磁場感測器', '極靈敏的磁力計',
  '02', '環上夾兩個 JJ', '兩個接面並聯',
  '03', '1964 年發明', '福特公司研究實驗室'],
 ['兩條路的干涉', '磁通讓兩路的相位錯開', '四個觀察',
  '第一點', '電流分成兩路', '第二點', '像雙狹縫干涉', '第三點', 'Φ = 0 電流最大', '第四點', 'Φ₀/2 時變成零',
  'I_c(Φ) = 2I_c0 |cos(πΦ/Φ₀)|'],
 ['磁通 → 能量 → 頻率', '磁通調得動 E_J，調不動 E_C',
  'E_J(Φ)', 'E_JΣ |cos(πΦ/Φ₀)|', '→', '頻率 f₀₁', '≈ √(8E_J E_C) − E_C',
  'Φ = 0：6.07 GHz　Φ = 0.25 Φ₀：5.07 GHz',
  '動畫設定：E_JΣ = 20 GHz、E_C = 250 MHz'],
 ['晶片上的磁通控制線', 'Z 線：通電流，產生磁通',
  'Z 控制線', '每顆位元一條', '奈秒調頻', '做閘、避開缺陷', '只能往下', '最高點在 Φ = 0',
  'E_J 刻意做大，留出往下調的空間'],
 ['甜蜜點', '斜率為零：一階不敏感',
  '同樣抖 0.01 Φ₀（依動畫的公式計算）',
  '甜蜜點 Φ = 0', '只差 1.6 MHz', '約 55 倍', '差距', 'Φ = 0.25 Φ₀', '差 86 MHz',
  '通常讓量子位元停在甜蜜點'],
 ['可調也有代價', '多一個旋鈕，多一個雜訊入口',
  '一、磁通抖，頻率抖\n二、甜蜜點也會動\n三、偏 0.02 Φ₀ 降 6 MHz',
  '停在甜蜜點外', '怎麼辦？', '提示：\n讓曲線變平',
  '暫停影片：怎麼讓它比較不怕磁通雜訊？'],
 ['實作：調頻闖關', '爸爸出題，孩子拉滑桿',
  '出題的人（爸爸）', '目標頻率\n例如 5.5 GHz',
  '拉滑桿的人（你）', '誤差 ±0.05 GHz\n記下 Φ 和 f₀₁',
  '把每一關的點連成調頻曲線'],
 ['換你改造：不對稱的環', '可調性和穩定性的取捨',
  '01', '拉不對稱度', 'd 從 0 拉到 0.6',
  '02', '看谷底', 'Φ₀/2 只降到 4.65 GHz',
  '03', '比調頻範圍', '範圍 6.07 → 1.43 GHz'],
 ['兩小時的調頻闖關工坊', '影片先引路，接下來調、畫、比、教',
  '00–25', '開場＋兩個接面成環', '25–65', '闖關調頻＋畫曲線', '65–75', '休息十分鐘',
  '75–105', '對稱與不對稱比較', '105–115', '換你教爸爸', '115–120', '錄音總結＋保存',
  '今日生活技能：在可調性與穩定性之間取捨'],
 ['最後一關：教爸爸調頻率', '暫停影片：不看稿說一次，再指出一個注意事項',
  '01', '說出環為何可調', '磁通讓兩路干涉',
  '02', '說出甜蜜點', '斜率為零，一階不敏感',
  '03', '指出一個注意事項', '可調 = 多一個雜訊入口',
  '保持好奇，我們下次見！'],
]

BOARD = [
 ('開場：課前教學版揭露、從上一堂洗衣板的偏壓電流接到磁場這個新旋鈕', '封面版型＋陳犀牛', '想一想還有什麼方法能調接面'),
 ('三個重點：可調的接面、磁通調頻（週期 Φ₀）、甜蜜點斜率為零', '三步流程卡＋黃字', '認識今天的作品：調頻曲線'),
 ('兩個接面並聯成環：磁場感測器、環上夾兩個 JJ、1964 年發明', '三點條列＋陳犀牛', '說出 SQUID 的結構'),
 ('兩條路的干涉：電流分兩路、像雙狹縫、Φ = 0 最大、Φ₀/2 變零', '面板四張卡＋黃字', '說出磁通怎麼改變臨界電流'),
 ('磁通 → E_J → 頻率：E_J(Φ)、f₀₁ ≈ √(8E_JE_C) − E_C、動畫數值', '雙框對照＋白字＋黃字', '說出 E_C 為什麼不受磁通影響'),
 ('晶片上的 Z 線：每顆位元一條、奈秒調頻、只能往下調', '三張步驟卡＋黃字', '說出 Z 線拿來做什麼'),
 ('甜蜜點：df/dΦ = 0、一階不敏感；抖 0.01 Φ₀ 時 1.6 MHz 對 86 MHz', '路徑一行＋三張卡＋黃字', '說出為什麼量子位元停在甜蜜點'),
 ('可調也有代價：雜訊入口、甜蜜點也會動（0.02 Φ₀ 降約 6 MHz）', '左三行＋右欄＋黃字', '暫停想怎麼讓曲線變平'),
 ('實作：index.html#squid 拉外加磁通，闖關調到目標頻率 ±0.05 GHz，記點畫曲線', '左右比較卡＋黃字', '父子闖關、畫調頻曲線、找甜蜜點'),
 ('獨立改造：不對稱度 0 → 0.6，比較谷底與調頻範圍', '三點條列＋陳犀牛', '寫下可調性與穩定性的取捨'),
 ('120 分鐘安排', '六列時間表＋黃字', '照時間表進行'),
 ('驗收與結尾：環為何可調、甜蜜點、可調 = 多一個雜訊入口；預告 Q028', '三點條列＋陳犀牛＋結尾語', '孩子教爸爸；錄音總結'),
]

if __name__ == '__main__':
    qbuild.build(
        here=HERE, lesson=LESSON, slug=SLUG, title=TITLE, topic=TOPIC, header_en='QUANTUM 101', checked=CHECKED,
        src=SRC, source_records=SOURCE_RECORDS, scenes=SCENES, visible=VISIBLE, board=BOARD,
        source_method='Curriculum rows (Q026, Q027, Q028), the curriculum slide decks JJ_Microwave_Readout_Talk.pptx p17 (plus the p15 energy-scale table) and transmon.pptx p20 '
                      '(slide text and speaker notes extracted with python-pptx; the curriculum cites transmon.pptx p21, whose content is chapter 7, '
                      'so the SQUID tuning case on p20 was used instead), the animation sources animations/js/scenes/06_squid.js (index.html#squid) '
                      'and animations/transmon-3d.html (chapter 6 #case step scripts) read by the producing agent on 2026-11-18, the repo document '
                      'docs/超導量子電腦師生對話教學紀錄.md lessons 1–3, and the Wikipedia article SQUID (raw wikitext fetched 2026-11-18); all frequency '
                      'and sensitivity numbers were recomputed in Node with the scene\'s own f01 formula and again in Python by squid_tuning.py.',
        not_verified=['「每顆可調的量子位元旁邊都有一條磁通控制線」「奈秒的時間內調好」取自學程簡報 JJ_Microwave_Readout_Talk p17 的講者備註；固定頻率的量子位元（例如課程文件提到的 IBM 路線）沒有這條線',
                      '動畫的 E_JΣ/h = 20 GHz、E_C/h = 250 MHz 是場景設定的示意值，不是某一顆晶片的實測值；文中 6.07、5.07、1.6 MHz、86 MHz、6 MHz、4.65 GHz 都是依這組設定以場景公式計算',
                      '「兩個一樣的接面在半個磁通量子剛好互相抵消、臨界電流變成零」是理想對稱 SQUID 的結果（課程文件 I_c(Φ) = 2I_c₀|cos(πΦ/Φ₀)|）；真實元件兩個接面不可能完全一樣',
                      '「設計時會刻意把約瑟夫森能量做大一點」取自課程文件第 3 課的說明，本集不估算實際設計值',
                      '課綱素材寫 transmon.pptx p21，但該頁是第 7 章振幅長條；本集改用 p20（第 6 章案例：SQUID 調頻），已在來源中註明',
                      '課綱的三組 YouTube 搜尋入口本次未挑選或觀看',
                      '本集未錄影試拍；動畫段（index.html#squid 面板捲到底後兩根滑桿與讀數是否同時入鏡、右下小圖灰色對稱曲線在不對稱度 0.6 時是否看得清楚）待 v2 試錄確認'],
        tts_date='2026-11-18')
