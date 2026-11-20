"""Q022 量子諧振子：等距的梯子 — production sources (12 scenes / 36 sentences).

    cd $XINEW_ACADEMY && ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q022/prepare_content.py
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import qbuild  # noqa: E402

HERE = Path(__file__).resolve().parent
LESSON, SLUG, CHECKED = 'Q022', 'q022-equal-ladder', '2026-11-18'
TITLE = '量子諧振子：等距的梯子'
TOPIC = '量子諧振子：等距的梯子'
REPO = 'pcpcchen-coder/QuantumComputing'
SRC = {
    'curriculum': f'{REPO} academy/lessons/Q022/lesson.json',
    'neighbors': f'{REPO} academy/lessons/Q021/brief.md、academy/lessons/Q023/brief.md',
    'ep049_p7': f'{REPO} slides/output/ep049-superconducting-qubit.pptx p7（含講者備註）',
    'ep049_p10': f'{REPO} slides/output/ep049-superconducting-qubit.pptx p10（含講者備註）',
    'transmon_p14': f'{REPO} slides/transmon.pptx p14（含講者備註）',
    'wiki_qho': 'https://en.wikipedia.org/wiki/Quantum_harmonic_oscillator',
    'wiki_lc': 'https://en.wikipedia.org/wiki/LC_circuit',
    'wiki_transmon': 'https://en.wikipedia.org/wiki/Transmon',
    'wiki_scqc': 'https://en.wikipedia.org/wiki/Superconducting_quantum_computing',
    'jj_potential': f'{REPO} animations/index.html#potential（js/scenes/04_potential.js）',
    'lc_s3s4': f'{REPO} animations/lc-vs-jj.html#s3、#s4',
}
SOURCE_RECORDS = [
    {'id': 'curriculum', 'title': '量子電腦學程 Q022 課綱', 'publisher': REPO, 'url': SRC['curriculum'],
     'usedFor': '主題、學習目標（LC 電路的能階等距，所以無法只挑出兩個能階當量子位元）、動手任務（在場景切到 LC 模式，數能階間距；用梯子圖說明「一路往上爬」的問題）、'
                '孩子獨立改造（畫出不等距梯子，說明為什麼能只在 0 與 1 之間跳）、好玩機制（闖關）、作品（能階梯子圖）、家長課前準備（index.html#potential）、'
                '120 分鐘流程、驗收與常見誤解（「等距」才是問題所在，不是能量太高或太低）、生活技能支線（找出設計失敗的根本原因）'},
    {'id': 'neighbors', 'title': '量子電腦學程 Q021、Q023 課綱', 'publisher': REPO, 'url': SRC['neighbors'],
     'usedFor': '上一堂：彈簧、單擺與 LC 電路（質量↔電感、彈簧↔電容；1 nH、1 pF 約 5 GHz 的例子）；'
                '下一堂：約瑟夫森接面——超導三明治（SIS 結構）'},
    {'id': 'ep049_p7', 'title': '《量子超級英雄》#049 報告簡報 p7：量子諧振子——出現等距的能階', 'publisher': REPO, 'url': SRC['ep049_p7'],
     'usedFor': 'En = (n + ½) ħω；ΔE = ħω，相鄰能階的間距固定，像樓梯一樣「等距」；零點能：最低能量 ½ħω 不是零，不能完全靜止；'
                '要縮到夠小才有量子效應，還要極低溫'},
    {'id': 'ep049_p10', 'title': '《量子超級英雄》#049 報告簡報 p10：問題來了——二態系統在哪裡？', 'publisher': REPO, 'url': SRC['ep049_p10'],
     'usedFor': '超導 LC 電路給了一座樓梯，但不是兩個態；用微波激發；能階等距 → 同一個微波能把系統一路往上推，'
                '沒辦法只在 |0⟩ 和 |1⟩ 之間操作 → 必須讓能階不等距'},
    {'id': 'transmon_p14', 'title': 'Transmon 筆記簡報 p14：非諧性——能階不再等距', 'publisher': REPO, 'url': SRC['transmon_p14'],
     'usedFor': 'LC：每階間距相同，一個頻率會一路往上激發，挑不出兩個能階；Transmon 越上越密，E12 比 E01 低（簡報例子 283 MHz）；'
                '對準 E01 的微波只在 |0⟩、|1⟩ 之間來回；連到 lc-vs-jj.html#s3、#s4'},
    {'id': 'wiki_qho', 'title': 'Wikipedia: Quantum harmonic oscillator', 'publisher': 'Wikipedia', 'url': SRC['wiki_qho'],
     'usedFor': '能量只能是 ħω(n + ½)；「these discrete energy levels are equally spaced」；最低能量 ħω/2 高於位能最低點（零點能），'
                '基態的位置與動量不固定'},
    {'id': 'wiki_lc', 'title': 'Wikipedia: LC circuit', 'publisher': 'Wikipedia', 'url': SRC['wiki_lc'],
     'usedFor': 'ω₀ = 1/√(LC)：電感或電容換大，振盪頻率變低'},
    {'id': 'wiki_transmon', 'title': 'Wikipedia: Transmon', 'publisher': 'Wikipedia', 'url': SRC['wiki_transmon'],
     'usedFor': '非諧性（anharmonicity）定義為 E21 與 E10 的差；非諧性小時，對準 0→1 的共振脈衝也會激發更高的能階，'
                '不容易當成兩能階系統操作'},
    {'id': 'wiki_scqc', 'title': 'Wikipedia: Superconducting quantum computing', 'publisher': 'Wikipedia', 'url': SRC['wiki_scqc'],
     'usedFor': '「anharmonicity refers to the unequal spacing of energy levels in a superconducting circuit」；非諧性大有利於快速的微波控制'},
    {'id': 'jj_potential', 'title': 'JJ 與微波讀取 3D 場景 4：非線性——從 LC 諧振子到 Transmon', 'publisher': REPO, 'url': SRC['jj_potential'],
     'usedFor': '場景說明：LC 位勢是拋物線、能階等間距，用頻率 ω 的微波驅動時 0→1、1→2、2→3 全部同時共振；把電感換成 JJ，越往上越寬、間距縮小；'
                '「LC 諧振子（線性）」模式下三個間距都是 5.00 GHz、非諧性 0 MHz（等間距 → 無法單獨定址）；以同一程式重算 JJ 模式 4.74／4.45／4.13 GHz、−287 MHz'},
    {'id': 'lc_s3s4', 'title': 'LC 與約瑟夫森接面 圖解第 3、4 步', 'publisher': REPO, 'url': SRC['lc_s3s4'],
     'usedFor': '第 3 步：拋物線的能階等間距，餘弦的不是（E_C/h = 250 MHz、E_J/E_C 可調）；第 4 步：LC 的所有躍遷疊在同一個頻率上，驅動會一路往上爬，'
                'transmon 的躍遷錯開，驅動只打得到 0→1'},
]

SCENES = [
 ('量子諧振子：等距的梯子', [
  '歡迎回到父子科技學院的量子電腦學程，我是陳犀牛，今天是量子第二十二堂，量子諧振子：等距的梯子，這是依課綱製作的課前教學版，並非實際上課錄音。',
  '上一堂我們把彈簧和電感電容電路對了起來；今天把這個電路做得很小、冷到超導，看它變成量子之後是什麼樣子。',
  '答案是一把每一階一樣高的梯子，而這正是它不能直接當量子位元的原因。'], ['curriculum', 'neighbors', 'ep049_p7']),
 ('今天的三關', [
  '今天是闖關課，一共三關：第一關，認識量子諧振子的能量為什麼只能一階一階地變。',
  '第二關，看出電感電容電路的梯子每一階都等距，用微波一推就會一路往上爬；第三關，畫出一把不等距的梯子。',
  '今天的作品是一張能階梯子圖，上面要標出每一階的間距，還要寫出等距為什麼不能用。'], ['curriculum']),
 ('從彈簧到量子：能量分階', [
  '平常的彈簧可以振得大一點或小一點，能量要多少都行；可是做到夠小、夠冷，量子效應就出現了。',
  '這時能量只能是一階一階的固定值，叫做能階；最低的一階叫基態，標成零，往上是一、二、三。',
  '有趣的是，最低那一階並不在位能山谷的最底下，而是高出半階，這叫零點能，所以它永遠不會完全靜止。'], ['ep049_p7', 'wiki_qho']),
 ('等距的梯子', [
  '電感電容電路的位能，畫出來是一條拋物線形的山谷，能階就像架在山谷裡的梯子。',
  '解出來的答案很整齊：相鄰兩階的能量差都一樣，等於普朗克常數乘上電路的振盪頻率，像樓梯一樣等距。',
  '上一堂算過，一奈亨的電感配一皮法的電容大約是五吉赫；那麼這把梯子每往上一階，需要的微波頻率都是五吉赫。'], ['ep049_p7', 'wiki_qho', 'jj_potential', 'neighbors']),
 ('量子位元只要兩階', [
  '可是量子位元只要兩個狀態：最低的一階當零，第二階當一。',
  '我們用微波來控制它：微波的頻率對準零到一的間距，就能把零推到一，或停在兩者的疊加。',
  '理想的情況是，微波只在這兩階之間作用，上面的階梯完全不會被碰到。'], ['ep049_p10', 'transmon_p14']),
 ('一路往上爬', [
  '問題來了：等距的梯子，零到一、一到二、二到三的間距全部一樣。',
  '對準零到一的微波，也正好對準一到二、二到三，於是它推上一階之後，還會繼續往上推。',
  '狀態就一路往上爬，散到很多階上，沒辦法只停在零和一之間，這就不是一個量子位元了。'], ['ep049_p10', 'transmon_p14', 'jj_potential', 'wiki_transmon']),
 ('問題在等距，不在高低', [
  '很多人會以為，是能量太高或太低才不能用，其實不是。',
  '把電感或電容換大，振盪頻率變低，整把梯子的間距一起變小；換小，間距一起變大，可是每一階永遠一樣高。',
  '所以不管頻率是多少，微波還是會一路往上推；要解決的是等距，不是能量的高低。'], ['curriculum', 'wiki_lc', 'wiki_qho']),
 ('解法：讓梯子不等距', [
  '解法是讓梯子變得不等距：把電感換成約瑟夫森接面，山谷變成越往上越寬，梯子越往上越擠。',
  '例如零到一約四點七四吉赫，一到二約四點四五吉赫，兩者的差叫做非諧性，大約負兩百九十兆赫；微波對準零到一，就碰不到一到二。',
  '暫停影片想一想：如果每一階的間距都不一樣，微波要選哪一個頻率，才能只在零和一之間來回？'], ['transmon_p14', 'jj_potential', 'wiki_scqc', 'lc_s3s4']),
 ('實作：在場景裡看間距', [
  '實作的時候，爸爸打開能階場景，按下電感電容諧振子那一個按鈕，切到線性的模式。',
  '你負責記錄：每一階旁邊的數字是多少，一階一階抄下來，看看有沒有哪一階不一樣。',
  '接著在紙上畫一把梯子，標出每一階的間距，再用幾支箭頭畫出微波怎麼一路往上爬。'], ['curriculum', 'jj_potential']),
 ('換你改造：畫不等距梯子', [
  '下半場換你改造：畫一把不等距的梯子，越往上，每一階越窄。',
  '在每一階旁邊寫上間距，例如零到一寫四點七四，一到二寫四點四五，二到三寫四點一三。',
  '最後用你自己的話說明：為什麼微波對準零到一時，不會把狀態推到二？'], ['curriculum', 'jj_potential', 'lc_s3s4']),
 ('兩小時的闖關實驗室', [
  '兩小時的安排是：開場十分鐘，概念示範十五分鐘，接著四十分鐘在場景裡看間距、畫梯子圖，然後休息十分鐘。',
  '下半場三十分鐘，你自己畫不等距的梯子並寫出理由；接著十分鐘交換角色，由你教爸爸怎麼操作、為什麼等距不能用。',
  '最後五分鐘錄音總結，替你的能階梯子圖取個名字，再存一個版本。'], ['curriculum']),
 ('最後一關：教爸爸看梯子', [
  '最後一關，請不看稿說出：電感電容電路的能階梯子是什麼形狀？為什麼它不能直接當量子位元？',
  '再指出一個要注意的地方：問題出在等距，不是能量太高或太低。',
  '今天的作品是能階梯子圖，下一堂要認識讓梯子變得不等距的關鍵元件：約瑟夫森接面，一個超導的三明治；我是陳犀牛，保持好奇，我們下次見！'], ['curriculum', 'neighbors']),
]

VISIBLE = [
 ['量子電腦學程 第二十二堂', '量子諧振子：\n等距的梯子', 'LC 電路的能階，每一階一樣高', '量子第二十二堂  ·  依課綱製作的課前教學版'],
 ['今天的三關', '闖關：從能階到梯子圖',
  '01 第一關', '能量只能\n一階一階', '→', '02 第二關', '等距梯子\n一路往上爬', '→', '03 第三關', '畫出\n不等距梯子',
  '今天的作品：能階梯子圖'],
 ['從彈簧到量子：能量分階', '做得夠小、夠冷',
  '01', '經典彈簧', '能量要多少都行',
  '02', '量子諧振子', '能量一階一階：0、1、2、3',
  '03', '零點能', '最低一階高出谷底半階'],
 ['等距的梯子', '拋物線山谷裡的能階', '四個觀察',
  '第一點', '位能是拋物線', '第二點', 'E = (n + ½) hf', '第三點', '間距都一樣', '第四點', '每階約 5 GHz',
  '相鄰兩階相差 ΔE = hf'],
 ['量子位元只要兩階', '最低兩階當作 0 和 1',
  '|0⟩', '最低的一階', '⇄', '|1⟩', '第二階',
  '微波頻率對準 0 到 1 的間距',
  '上面的階梯不要碰到'],
 ['一路往上爬', '同一個微波頻率，每一階都吸收',
  '0 → 1', '5 GHz', '1 → 2', '也是 5 GHz', '2 → 3', '還是 5 GHz',
  '挑不出只有兩階的開關'],
 ['問題在等距，不在高低', '換元件只會改間距的大小',
  'ΔE = hf，f = 1 / (2π√(LC))',
  'L 或 C 換大', '間距一起變小', 'L 或 C 換小', '間距一起變大', '不管怎麼換', '每一階還是一樣高',
  '常見誤會：不是能量太高或太低'],
 ['解法：讓梯子不等距', '把電感換成約瑟夫森接面',
  '一、山谷變成餘弦形\n二、越往上越擠\n三、間距一階比一階小',
  '動畫的例子', '0→1 ≈ 4.74 GHz', '1→2 ≈ 4.45 GHz\n非諧性約 −290 MHz',
  '暫停影片：微波該選哪個頻率？'],
 ['實作：在場景裡看間距', '切到 LC 模式，一階一階看',
  '操作的人（爸爸）', '打開能階場景\n按 LC 諧振子',
  '記錄的人（你）', '抄下每階間距\n畫出梯子圖',
  '用箭頭畫出一路往上爬'],
 ['換你改造：畫不等距梯子', '下半場，越往上越窄',
  '01', '畫一把新梯子', '越往上，每階越窄',
  '02', '寫上每階間距', '4.74、4.45、4.13 GHz',
  '03', '說明為什麼', '只在 0 與 1 之間跳'],
 ['兩小時的闖關實驗室', '影片先引路，接下來看、畫、改、教',
  '00–25', '開場＋等距的梯子', '25–65', 'LC 模式＋畫梯子圖', '65–75', '休息十分鐘',
  '75–105', '畫不等距梯子', '105–115', '換你教爸爸', '115–120', '錄音總結＋保存',
  '今日生活技能：找出失敗的根本原因'],
 ['最後一關：教爸爸看梯子', '暫停影片：不看稿說一次，再指出一個注意事項',
  '01', '說出梯子的形狀', 'LC 的能階等距',
  '02', '為什麼不能用', '微波一路往上爬',
  '03', '指出一個注意事項', '等距才是問題',
  '保持好奇，我們下次見！'],
]

BOARD = [
 ('開場：課前教學版揭露、從上一堂的 LC 電路走到量子', '封面版型＋陳犀牛', '想一想電路變成量子會怎樣'),
 ('三關：能階、等距梯子與一路往上爬、不等距梯子', '三步流程卡＋黃字', '認識今天的作品'),
 ('從經典到量子：能量分階、基態、零點能', '三點條列＋陳犀牛', '說出能階是什麼'),
 ('等距的梯子：拋物線位能、E = (n + ½)hf、每階約 5 GHz', '面板四張卡＋黃字', '說出相鄰兩階差多少'),
 ('量子位元只要兩階：|0⟩、|1⟩，微波對準 0 到 1', '雙框對照＋白字＋黃字', '說出量子位元要什麼'),
 ('一路往上爬：同一個微波頻率每一階都吸收', '三張步驟卡＋黃字', '說出為什麼停不在兩階'),
 ('常見誤會：問題在等距，不在能量高低；f = 1/(2π√(LC))', '路徑一行＋三張卡＋黃字', '預測換元件後的間距'),
 ('解法：約瑟夫森接面讓梯子不等距；4.74／4.45 GHz、非諧性約 −290 MHz', '左三行＋右欄＋黃字', '暫停想微波該選哪個頻率'),
 ('實作：在能階場景切到 LC 模式，抄下間距、畫梯子圖', '左右比較卡＋黃字', '父子一起看間距、畫梯子'),
 ('獨立改造：畫不等距梯子並寫出理由', '三點條列＋陳犀牛', '畫、標間距、說明'),
 ('120 分鐘安排', '六列時間表＋黃字', '照時間表進行'),
 ('驗收與結尾：梯子的形狀、為什麼不能用、等距才是問題；預告 Q023', '三點條列＋陳犀牛＋結尾語', '孩子教爸爸；錄音總結'),
]

if __name__ == '__main__':
    qbuild.build(
        here=HERE, lesson=LESSON, slug=SLUG, title=TITLE, topic=TOPIC, header_en='QUANTUM 101', checked=CHECKED,
        src=SRC, source_records=SOURCE_RECORDS, scenes=SCENES, visible=VISIBLE, board=BOARD,
        source_method='Curriculum rows (Q021, Q022, Q023), the curriculum slide decks ep049-superconducting-qubit.pptx p7, p10 and '
                      'transmon.pptx p14 (slide text and speaker notes extracted with python-pptx), and the animation sources '
                      'animations/js/scenes/04_potential.js (index.html#potential) and animations/lc-vs-jj.html (#s3, #s4) read by the producing agent '
                      'on 2026-11-18; level spacings and anharmonicity recomputed by the producing agent in Node with the same code as the pages; '
                      'quantum harmonic oscillator, LC circuit and anharmonicity facts checked against the Wikipedia articles Quantum harmonic oscillator, '
                      'LC circuit, Transmon and Superconducting quantum computing (raw wikitext fetched 2026-11-18).',
        not_verified=['「普朗克常數乘上振盪頻率」是 ΔE = ħω = hf 的白話說法；旁白的「頻率」指每秒振盪次數 f，不是角頻率 ω',
                      '「每往上一階需要的微波頻率都是五吉赫」沿用上一堂 1 nH、1 pF 的整數例子（1/(2π√(LC)) = 5.03 GHz）；'
                      '能階場景 LC 模式的 5.00 GHz 是程式設定 E_J = 12.5 GHz、E_C = 0.25 GHz 時 √(8E_JE_C) 的值，兩者都不是某一顆量子位元的實際元件值',
                      '4.74／4.45／4.13 GHz 與 −287 MHz 是動畫以 E_J/E_C = 50、E_C/h = 250 MHz 對角化算出的例子（transmon 簡報 p14 的例子是 5.21／4.93 GHz、−283 MHz）；旁白說「大約負兩百九十兆赫」',
                      '「一路往上爬」是簡化說法：等距時同一頻率的微波對每一階都共振，狀態會擴散到多個能階（場景說明稱同調態）；本集不展開',
                      '「最低一階高出谷底半階」指 E₀ = ½hf；零點能與測不準原理的關係依簡報 p7 講者備註，本集不推導',
                      '課綱的三組 YouTube 搜尋入口本次未挑選或觀看',
                      '本集未錄影試拍；動畫段（index.html#potential 的面板捲動、按鈕入鏡；lc-vs-jj.html #s3、#s4 的捲動位置與滑桿以程式設定的時間點）待 v2 試錄確認'],
        tts_date='2026-11-18')
