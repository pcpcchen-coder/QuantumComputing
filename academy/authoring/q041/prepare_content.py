"""Q041 為什麼要 10 mK — production sources (12 scenes / 36 sentences).

    cd $XINEW_ACADEMY && ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q041/prepare_content.py
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import qbuild  # noqa: E402

HERE = Path(__file__).resolve().parent
LESSON, SLUG, CHECKED = 'Q041', 'q041-why-10mk', '2026-11-18'
TITLE = '為什麼要十毫克耳文'
TOPIC = '為什麼要 10 mK'
REPO = 'pcpcchen-coder/QuantumComputing'
SRC = {
    'curriculum': f'{REPO} academy/lessons/Q041/lesson.json',
    'pe_talk': f'{REPO} slides/QC_Peripheral_Systems_Talk.pptx（第 6–7 頁）',
    'kb': 'https://en.wikipedia.org/wiki/Boltzmann_constant',
    'planck': 'https://en.wikipedia.org/wiki/Planck_constant',
    'bdist': 'https://en.wikipedia.org/wiki/Boltzmann_distribution',
    'ln2': 'https://en.wikipedia.org/wiki/Liquid_nitrogen',
    'lhe': 'https://en.wikipedia.org/wiki/Liquid_helium',
    'al': 'https://en.wikipedia.org/wiki/Aluminium',
    'calc': f'{REPO} academy/authoring/q041/fact-check.md（製作代理的 Python 驗算）',
    'scene': f'{REPO} animations/peripherals.html#cooldown、animations/index.html#fridge、animations/transmon-3d.html#readout',
}
SOURCE_RECORDS = [
    {'id': 'curriculum', 'title': '量子電腦學程 Q041 課綱', 'publisher': REPO, 'url': SRC['curriculum'],
     'usedFor': '主題、學習目標、動手任務（5 GHz 換算、室溫／液氮／液氦／10 mK）、孩子獨立改造（3 GHz、8 GHz）、好玩機制（競速）、作品、120 分鐘流程、驗收與常見誤解'},
    {'id': 'pe_talk', 'title': '量子電腦的周邊系統（內部技術分享簡報）第 6–7 頁', 'publisher': REPO, 'url': SRC['pe_talk'],
     'usedFor': '5 GHz：hf ≈ 20 μeV ≈ 240 mK × kB；10 mK 時 kBT 只有 hf 的 1/24、熱激發 ≈ e⁻²⁴；溫度不夠低的四個後果；鋁 Tc ≈ 1.2 K；各溫層與基溫約 10 mK'},
    {'id': 'kb', 'title': 'Boltzmann constant', 'publisher': 'Wikipedia（2026-11-18 讀取）', 'url': SRC['kb'],
     'usedFor': 'k_B 定義為 1.380649×10⁻²³ J/K（精確值）'},
    {'id': 'planck', 'title': 'Planck constant', 'publisher': 'Wikipedia（2026-11-18 讀取）', 'url': SRC['planck'],
     'usedFor': 'h 定義為 6.62607015×10⁻³⁴ J·s（精確值）'},
    {'id': 'bdist', 'title': 'Boltzmann distribution', 'publisher': 'Wikipedia（2026-11-18 讀取）', 'url': SRC['bdist'],
     'usedFor': '兩個狀態機率的比值叫波茲曼因子，只和能量差有關：exp(−ΔE/kT)'},
    {'id': 'ln2', 'title': 'Liquid nitrogen', 'publisher': 'Wikipedia（2026-11-18 讀取）', 'url': SRC['ln2'],
     'usedFor': '液態氮在常壓下慢慢沸騰，溫度維持 77 K'},
    {'id': 'lhe', 'title': 'Liquid helium', 'publisher': 'Wikipedia（2026-11-18 讀取）', 'url': SRC['lhe'],
     'usedFor': '液態氦（氦四）常壓沸點 4.2 K'},
    {'id': 'al', 'title': 'Aluminium', 'publisher': 'Wikipedia（2026-11-18 讀取）', 'url': SRC['al'],
     'usedFor': '鋁的超導臨界溫度 1.2 K'},
    {'id': 'calc', 'title': '頻率→溫度、波茲曼因子的 Python 驗算', 'publisher': REPO, 'url': SRC['calc'],
     'usedFor': '5 GHz → 20.68 μeV → 0.240 K；300 K、77 K、4.2 K、10 mK、100 mK 的 hf/kT 與 exp(−hf/kT)；3 GHz、8 GHz；熱激發 < 1% 的溫度上限'},
    {'id': 'scene', 'title': '互動動畫：周邊系統 場景 4 降溫流程；JJ 與微波讀取 場景 11 低溫讀取鏈；transmon 3D 第 5 章 讀取', 'publisher': REPO,
     'url': SRC['scene'], 'usedFor': '各溫層從 300 K 降到約 10 mK；7 GHz 熱光子數 300 K ≈ 890、10 mK ≈ 10⁻¹⁵；22 μeV ≈ 0.25 K；位元等效溫度 40–60 mK'},
]

SCENES = [
 ('為什麼要十毫克耳文', [
  '歡迎回到父子科技學院的量子電腦學程，我是陳犀牛，今天是量子第四十一堂，為什麼要十毫克耳文，這是依課綱製作的課前教學版，並非實際上課錄音。',
  '上一堂我們發現，量子電腦不只是一顆晶片，晶片外面還圍著冷凍機、電子機櫃和一大堆設備。',
  '今天要回答其中最根本的問題：量子晶片為什麼要放在十毫克耳文，也就是比液態氦還冷四百多倍的地方？'], ['curriculum']),
 ('三步：比、算、排', [
  '今天分三步：先比較量子位元的能量和熱能，再把頻率換算成溫度，最後排出一張溫度換算表。',
  '實作的時候還要來一場競速，看誰換算得又快又對。',
  '今天的作品，就是這張從室溫一路排到十毫克耳文的溫度換算表。'], ['curriculum']),
 ('熱會把零踢成一', [
  '超導量子位元的零和一，是電路裡兩個能階，中間差的能量，等於普朗克常數乘上量子位元的頻率。',
  '周圍環境的熱，也會帶來一份一份隨機的能量，大小大約是波茲曼常數乘上溫度。',
  '如果熱能和量子位元的能量差不多大，零就會被熱隨機踢到一，我們還沒開始計算，資料就先亂了。'], ['pe_talk', 'bdist']),
 ('五吉赫換成溫度', [
  '開始換算：普朗克常數乘上五吉赫，得到大約三點三乘十的負二十四次方焦耳，也就是大約二十點七微電子伏特。',
  '再除以波茲曼常數，得到大約零點二四克耳文，也就是兩百四十毫克耳文。',
  '意思是：五吉赫量子位元的一份能量，只相當於零點二四克耳文的熱能，比液態氦的四點二克耳文還小得多。'], ['planck', 'kb', 'calc', 'pe_talk']),
 ('比一比：室溫和十毫克耳文', [
  '在三百克耳文的室溫，熱能大約是五吉赫量子位元能量的一千兩百五十倍，零和一被熱攪得幾乎一樣多。',
  '到了十毫克耳文，情況反過來，熱能只剩量子位元能量的二十四分之一。',
  '這時候熱激發的機率，大約只有千億分之四，熱雜訊幾乎不存在。'], ['calc', 'pe_talk']),
 ('熱激發機率怎麼算', [
  '熱激發的機率可以用波茲曼因子估算，分三步：先把量子位元的能量除以熱能，得到一個比值。',
  '第二步在比值前面加上負號，第三步算自然常數的這個次方，計算機上通常有一個指數鍵。',
  '比值是二十四的時候，答案大約是千億分之四；比值接近零的時候，答案接近一，代表激發態和基態幾乎一樣多。'], ['bdist', 'calc']),
 ('溫度換算表：四個溫度', [
  '把四個溫度排成一張表：室溫三百克耳文、液態氮七十七克耳文、液態氦四點二克耳文，還有十毫克耳文。',
  '液態氮的波茲曼因子大約零點九九七，液態氦大約零點九四，兩個都還接近一，熱雜訊仍然到處都是。',
  '只有到了十毫克耳文，數字才一口氣掉到千億分之四；表上的四個溫度，只有最後一個夠冷。'], ['ln2', 'lhe', 'calc']),
 ('不夠冷會怎樣', [
  '溫度不夠低，會出四種問題：量子位元一開始就有一部分在一，初始化出錯；讀取腔裡有熱光子，讓量子位元的相位亂掉。',
  '第三，超導體裡的準粒子變多，會穿過約瑟夫森接面帶走能量；第四，鋁大約在一點二克耳文以下才會超導，再熱一點，電路根本不會超導。',
  '暫停影片，自己算一算一百毫克耳文的波茲曼因子，看看它離千億分之四差多遠。'], ['pe_talk', 'al', 'calc']),
 ('溫度換算競速：計算員和裁判', [
  '實作的時候來場溫度換算競速：你是計算員，負責按計算機，把頻率換成溫度，再算出波茲曼因子。',
  '爸爸是裁判，負責計時、核對答案，記下每一題花了幾秒。',
  '訣竅是先估數量級：五吉赫大約零點二四克耳文，頻率加倍，溫度也加倍，心算就能先猜個大概。'], ['curriculum', 'calc']),
 ('換你改造：三吉赫和八吉赫', [
  '下半場換你改造：用同樣的方法，算出三吉赫和八吉赫的量子位元，各相當於多少克耳文。',
  '三吉赫大約零點一四克耳文，八吉赫大約零點三八克耳文；頻率越低，一份能量越小，就越怕熱。',
  '如果要熱激發低於百分之一，就把剛才換出的溫度再除以四點六：三吉赫要低於三十一毫克耳文，八吉赫要低於八十三毫克耳文。'], ['curriculum', 'calc']),
 ('兩小時的溫度實驗室', [
  '兩小時的安排是：開場十分鐘，用十五分鐘比較量子位元能量和熱能，接著四十分鐘把五吉赫換成溫度、排出換算表，然後休息十分鐘。',
  '下半場三十分鐘算三吉赫和八吉赫各需要多冷；接著十分鐘交換角色，由你教爸爸怎麼換算，為什麼要這麼冷。',
  '最後五分鐘錄音總結，替溫度換算表取名字，存一個版本。'], ['curriculum']),
 ('最後一關：教爸爸為什麼要十毫克耳文', [
  '最後一關，請不看稿說出：為什麼量子晶片要放在十毫克耳文？要拿來比的是哪兩種能量？',
  '再指出一個常見誤解：十毫克耳文不是為了讓電腦變快，而是為了讓熱雜訊幾乎不存在。',
  '今天的作品是溫度換算表，下一堂我們來看冷凍機的上半段，脈衝管與壓縮機，怎麼靠壓力波把溫度降到大約三克耳文；我是陳犀牛，保持好奇，我們下次見！'], ['curriculum', 'pe_talk']),
]

VISIBLE = [
 ['量子電腦學程 第四十一堂', '為什麼要\n10 mK', '比一比：量子位元能量和熱能', '量子第四十一堂  ·  依課綱製作的課前教學版'],
 ['三步：比、算、排', '今天來一場溫度換算競速',
  '01 比能量', '量子位元能量\n和熱能 kT', '→', '02 算溫度', '5 GHz\n換成克耳文', '→', '03 排表格', '室溫一路\n排到 10 mK',
  '今天的作品：溫度換算表'],
 ['熱會把零踢成一', '溫度太高，量子位元自己就亂了',
  '01', '零和一是兩個能階', '中間差一份 hf',
  '02', '熱能大約是 kT', '溫度越高，熱擾動越大',
  '03', 'kT 跟 hf 差不多', '零被熱踢到一'],
 ['五吉赫換成溫度', '把量子位元的能量寫成克耳文', '換算四步',
  '第一步', 'h × 5 GHz', '第二步', '≈ 20.7 μeV', '第三步', '÷ kB', '第四步', '≈ 0.24 K',
  '5 GHz ≈ 0.24 K ≈ 240 mK'],
 ['比一比：室溫和十毫克耳文', '同一顆 5 GHz 量子位元',
  '室溫 300 K', 'kT ≈ 1250 × hf', '→', '10 mK', 'kT ≈ hf ÷ 24',
  '熱激發：≈ 1  →  ≈ 4×10⁻¹¹',
  '溫度要遠低於量子位元能量'],
 ['熱激發機率怎麼算', '波茲曼因子：exp(−hf / kT)',
  '01 算比值', 'hf ÷ kT', '02 加負號', '−hf / kT', '03 按指數鍵', 'exp(−hf / kT)',
  '比值越大，熱激發越少'],
 ['溫度換算表：四個溫度', '同一顆 5 GHz 量子位元',
  '300 K  →  77 K  →  4.2 K  →  10 mK',
  '液氮 77 K', '≈ 0.997', '液氦 4.2 K', '≈ 0.94', '10 mK', '≈ 4×10⁻¹¹',
  '只有 10 mK 夠冷'],
 ['不夠冷會怎樣', '簡報第六頁列出的四個後果',
  '一、初始化出錯\n二、讀取腔有熱光子\n三、準粒子變多',
  '鋁的超導溫度', '約 1.2 K', '再熱一點\n根本不會超導',
  '暫停影片：算算 100 mK 夠不夠冷'],
 ['溫度換算競速：計算員和裁判', '你按計算機，爸爸計時',
  '計算員（你）', '頻率換成溫度\n算出波茲曼因子',
  '裁判（爸爸）', '計時、核對答案\n記下最快一題',
  '先估數量級，再按計算機'],
 ['換你改造：三吉赫和八吉赫', '頻率越低，越怕熱',
  '01', '3 GHz', '約 0.14 K',
  '02', '8 GHz', '約 0.38 K',
  '03', '熱激發 < 1%', '換出的溫度 ÷ 4.6'],
 ['兩小時的溫度實驗室', '影片先引路，接下來比、算、排、教',
  '00–25', '開場＋能量和熱能', '25–65', '5 GHz 換算競速', '65–75', '休息十分鐘',
  '75–105', '3 GHz 和 8 GHz', '105–115', '換你教爸爸', '115–120', '錄音總結＋保存',
  '今日生活技能：單位換算與數量級'],
 ['最後一關：教爸爸為什麼要 10 mK', '暫停影片：不看稿說一次，再指出一個誤解',
  '01', '說出原理', 'hf 和 kT 比一比',
  '02', '完成換算表', '四個溫度的熱激發',
  '03', '指出一個誤解', '冷不是為了變快',
  '保持好奇，我們下次見！'],
]

BOARD = [
 ('開場：課前教學版揭露、為什麼要 10 mK', '封面版型＋陳犀牛', '回想上一堂的周邊設備'),
 ('三步：比、算、排', '三步流程卡＋黃字', '認識今天的競速'),
 ('量子位元能量 hf 與熱能 kT', '三點條列＋陳犀牛', '說出熱激發是什麼'),
 ('5 GHz 換算成 0.24 K', '面板四張卡＋黃字', '跟著按計算機'),
 ('比較：室溫 vs 10 mK', '雙框對照＋白字＋黃字', '說出倍數'),
 ('波茲曼因子三步', '三張步驟卡＋黃字', '算出 exp(−24)'),
 ('溫度換算表：300 K、77 K、4.2 K、10 mK', '路徑一行＋三張卡＋黃字', '填換算表'),
 ('不夠冷的四個後果、鋁 Tc', '左三行＋右欄＋黃字', '算 100 mK'),
 ('遊戲：計算員與裁判', '左右比較卡＋黃字', '溫度換算競速'),
 ('獨立改造：3 GHz 與 8 GHz', '三點條列＋陳犀牛', '算出各需要多冷'),
 ('120 分鐘安排', '六列時間表＋黃字', '照時間表進行'),
 ('驗收與結尾：原理、換算表、誤解；預告 Q042', '三點條列＋陳犀牛＋結尾語', '孩子教爸爸；錄音總結'),
]

if __name__ == '__main__':
    qbuild.build(
        here=HERE, lesson=LESSON, slug=SLUG, title=TITLE, topic=TOPIC, header_en='QUANTUM 101', checked=CHECKED,
        src=SRC, source_records=SOURCE_RECORDS, scenes=SCENES, visible=VISIBLE, board=BOARD,
        source_method='Constants and temperatures from Wikipedia pages (Boltzmann constant, Planck constant, Boltzmann distribution, '
                      'Liquid nitrogen, Liquid helium, Aluminium) read by the producing agent on 2026-11-18 (quotes in production/source-notes.md); '
                      'repo slides p6–7 and animation source read by the producing agent; every number recomputed in Python (production/fact-check.md).',
        not_verified=['波茲曼因子 exp(−hf/kT) 是激發態對基態的機率比；本集把它當成「熱激發機率」的估算，高溫時真正的兩能階機率接近一半（見 fact-check.md）',
                      '簡報第 6 頁備註「100 mK 熱激發到百分之一量級」與驗算（5 GHz 約 9%）不符；本集不採用該句，改請觀眾自己算',
                      '實際晶片的等效溫度常高於冷凍機底板（動畫寫 40–60 mK），本集只在動畫段提及，不給通用數字',
                      '課綱的三組 YouTube 搜尋入口本次未挑選或觀看'],
        tts_date='2026-11-18')
