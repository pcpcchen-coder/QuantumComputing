"""Q001 開學任務：量子電腦不是更快的電腦 — production sources (12 scenes / 36 sentences).

製作用的是父子科技學院的可攜流程（pcpcchen-coder/XiNewVideoGPT 的 academy/）。量子電腦學程不在
父子學院的 192 堂課表裡，所以走它的「特別篇」路線（special_builder），集數資料夾建在
XiNewVideoGPT 的 academy/specials/q001-not-faster/；做完後把來源、教材與 QC 複製回本 repo 的
academy/episodes/q001-not-faster/。

    XINEW_ACADEMY=/path/to/XiNewVideoGPT/academy \
      $XINEW_ACADEMY/portable-runtime.sh python academy/authoring/q001/prepare_content.py
"""
from pathlib import Path
import json
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import special_builder  # noqa: E402

HERE = Path(__file__).resolve().parent
QREPO = HERE.parents[2]
LESSON, SLUG, CHECKED = 'Q001', 'q001-not-faster', '2026-11-07'
TITLE = '開學任務：量子電腦不是更快的電腦'
DISCLOSURE = '依課綱製作的課前教學版'
LESSON_JSON = json.loads((QREPO / 'academy/lessons/Q001/lesson.json').read_text(encoding='utf-8'))
assert LESSON_JSON['sourceRow']['課程主題'] == '開學任務：量子電腦不是「更快的電腦」'

SRC = {
    'curriculum': 'pcpcchen-coder/QuantumComputing academy/lessons/Q001/lesson.json',
    'op_talk': 'pcpcchen-coder/QuantumComputing slides/QC_Operation_Talk.pptx（第 3–4、8、36–37、42、45 頁）',
    'aaronson_limits': 'https://www.scottaaronson.com/papers/limitsam.pdf',
    'aaronson_qml': 'https://www.scottaaronson.com/papers/qml.pdf',
    'shor': 'https://arxiv.org/abs/quant-ph/9508027',
    'grover': 'https://arxiv.org/abs/quant-ph/9605043',
    'preskill': 'https://arxiv.org/abs/2106.10522',
    'workflow': 'pcpcchen-coder/QuantumComputing animations/operation.html#workflow',
}
SOURCE_RECORDS = [
    {'id': 'curriculum', 'title': '量子電腦學程 Q001 課綱', 'publisher': 'pcpcchen-coder/QuantumComputing', 'url': SRC['curriculum'],
     'usedFor': '主題、學習目標、動手任務、好玩機制、作品、120 分鐘流程、驗收'},
    {'id': 'op_talk', 'title': '如何操作量子電腦：設定、計算、讀取與加速原理', 'publisher': 'pcpcchen-coder/QuantumComputing（內部技術分享簡報）',
     'url': SRC['op_talk'], 'usedFor': '測量只得到一個結果、三個資源（疊加、干涉、糾纏）、常見誤解、加速等級、不會變快的事'},
    {'id': 'aaronson_limits', 'title': 'The Limits of Quantum Computers', 'publisher': 'Scott Aaronson, Scientific American (March 2008), author PDF',
     'url': SRC['aaronson_limits'], 'usedFor': '量子電腦不是同時試所有答案；加速靠干涉，只對特殊結構的問題'},
    {'id': 'aaronson_qml', 'title': 'Read the fine print', 'publisher': 'Scott Aaronson, Nature Physics 11, 291–293 (2015), author PDF',
     'url': SRC['aaronson_qml'], 'usedFor': '把大量古典資料載入量子態本身很花時間，可能吃掉加速'},
    {'id': 'shor', 'title': 'Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer',
     'publisher': 'Peter W. Shor, arXiv:quant-ph/9508027', 'url': SRC['shor'], 'usedFor': '量子電腦可在多項式時間分解大數；古典沒有已知的有效方法'},
    {'id': 'grover', 'title': 'A fast quantum mechanical algorithm for database search', 'publisher': 'Lov K. Grover, arXiv:quant-ph/9605043',
     'url': SRC['grover'], 'usedFor': '無序搜尋約 √N 步，古典平均約 N/2 步'},
    {'id': 'preskill', 'title': 'Quantum computing 40 years later', 'publisher': 'John Preskill, arXiv:2106.10522',
     'url': SRC['preskill'], 'usedFor': '費曼 1981 年演講提出用量子系統模擬量子物理'},
    {'id': 'workflow', 'title': '3D 場景 12：完整流程', 'publisher': 'pcpcchen-coder/QuantumComputing animations/operation.html',
     'url': SRC['workflow'], 'usedFor': '課後打開三維動畫，看一次量子計算從程式到結果'},
]

SCENES = [
 ('開學任務：量子電腦不是更快的電腦', [
  '歡迎來到父子科技學院的量子電腦學程，我是陳犀牛，今天是量子第一堂，開學任務，這是依課綱製作的課前教學版，並非實際上課錄音。',
  '你一定聽過有人說：量子電腦超級快，以後什麼都能算。',
  '今天的任務，就是把這句話拆開來檢查：它哪裡對，哪裡說錯了。'], ['curriculum']),
 ('學程地圖：九十六堂', [
  '先看地圖：這個學程一共九十六堂，分成三個階段。',
  '第一階段用遊戲和三維動畫培養量子直覺，第二階段看硬體怎麼做，第三階段學操作、各種平台和未來的應用。',
  '今天的作品有兩個：一張宣稱分類卡，和一份屬於你自己的量子問題清單。'], ['curriculum']),
 ('最常聽到的說法', [
  '最常聽到的說法是：量子電腦會同時試所有的答案，所以比較快。',
  '問題是，量子電腦算完一定要測量，而每次測量只會得到一個結果，而且是隨機的。',
  '如果只是同時試、再隨便抽一個出來，那跟亂猜差不多，一點都不快。'], ['aaronson_limits', 'op_talk']),
 ('量子工具箱', [
  '那量子電腦真正的工具是什麼？我們先認識四樣：疊加、干涉、糾纏、測量。',
  '疊加讓很多種可能，各自帶著一個叫振幅的數字；干涉讓這些數字互相加強，或互相抵消。',
  '關鍵在設計：讓錯的答案互相抵消，對的答案互相加強，最後測量時，才容易得到對的那一個。'], ['aaronson_limits', 'op_talk']),
 ('比一比：普通電腦和量子電腦', [
  '所以量子電腦比較像一種專門工具，不是更快的筆電。',
  '你的電腦很擅長上網、打字、看影片；量子電腦只對某些有特殊數學結構的問題，才有機會大幅加速。',
  '大部分時候，兩種電腦會一起工作：普通電腦負責準備和整理，量子電腦負責最難的那一小段。'], ['aaronson_limits', 'op_talk']),
 ('有機會變快的三種問題', [
  '有哪些問題有機會變快？第一個是把很大的數字分解成質數；在夠大的量子電腦上，秀爾演算法可以比已知的古典方法快非常多。',
  '第二個是在一大堆沒有排好的資料裡找東西：一百萬筆資料，一筆一筆翻平均要五十萬次，格羅弗搜尋大約不到一千次，這是平方根的加速。',
  '第三個是模擬分子和材料；費曼在一九八一年的演講裡就提出，用量子系統來模擬量子世界。'], ['shor', 'grover', 'preskill']),
 ('不會變快的事', [
  '那哪些事不會變快？上網、打字、看影片、玩遊戲，這些事沒有讓干涉發揮的結構，用量子電腦不會更快。',
  '要把一大堆資料讀進量子電腦，本身就很花時間，常常把省下來的時間又吃掉了。',
  '而且現在的量子位元很怕熱、很怕雜訊，所以量子電腦不會取代你桌上的電腦。'], ['aaronson_qml', 'op_talk']),
 ('活動：宣稱卡分類', [
  '接下來是今天的活動：宣稱卡分類。',
  '列印包裡有十二張宣稱卡，請你把它們分成三堆：有機會變快、不會變快、說錯了。',
  '每放一張，都要說出理由；暫停影片，先猜猜「量子電腦會同時試所有答案」這張，應該放哪一堆。'], ['curriculum']),
 ('冒險任務', [
  '分類的時候玩冒險任務：你是探險家，爸爸是守門人。',
  '探險家每放一張卡，守門人就追問一次：你的證據是什麼？',
  '說得出理由就過關；說不出來，就把這張卡寫進問題清單，之後的課再回來解開。'], ['curriculum']),
 ('換你出題', [
  '下半場換你。第一，寫下十個你最想知道的量子問題，越奇怪越好。',
  '第二，從新聞或影片找一句講量子電腦的話，判斷它屬於哪一堆。',
  '第三，打開學程附的三維動畫，跟著一次量子計算，從寫程式一路走到拿到結果。'], ['curriculum', 'workflow']),
 ('兩小時的開學任務', [
  '兩小時的安排是：開場十分鐘，認識量子工具箱十五分鐘，接著四十分鐘玩宣稱卡分類，然後休息十分鐘。',
  '下半場三十分鐘寫問題清單、查一句新聞；接著十分鐘交換角色，由你教爸爸，量子電腦快在哪裡。',
  '最後五分鐘錄音總結，替兩件作品取名字，存一個版本。'], ['curriculum']),
 ('最後一關：教爸爸量子快在哪', [
  '最後一關，請不看稿說出：為什麼「同時試所有答案」這句話是錯的？',
  '再各舉一個例子：一件量子電腦有機會變快的事，和一件不會變快的事；也說出一個限制，例如格羅弗搜尋只快了平方根。',
  '今天的作品是宣稱分類卡和量子問題清單，下一堂我們要做一顆紙的布洛赫球，看看量子位元長什麼樣子；我是陳犀牛，保持好奇，我們下次見！'], ['curriculum', 'grover']),
]

VISIBLE = [
 ['量子電腦學程 第一堂', '開學任務：\n量子電腦不是更快的電腦', '同時試所有答案？我們來檢查', '量子第一堂  ·  依課綱製作的課前教學版'],
 ['學程地圖：九十六堂', '三個階段，由淺到深',
  '01 量子直覺', '遊戲和三維動畫\n不用公式', '→', '02 硬體怎麼做', '超導、讀取\n冷凍機', '→', '03 操作與未來', '演算法、平台\n錯誤更正',
  '今天的作品：宣稱分類卡＋量子問題清單'],
 ['最常聽到的說法', '「同時試所有答案」哪裡不對',
  '01', '常見說法', '同時試所有答案，所以快',
  '02', '但是測量', '每次只得到一個隨機結果',
  '03', '所以', '只是同時試，跟亂猜差不多'],
 ['量子工具箱', '四樣工具，一起用才有用', '工具箱',
  '疊加', '很多可能帶著振幅', '干涉', '振幅加強或抵消', '糾纏', '結果之間有關聯', '測量', '只得到一個結果',
  '讓錯的抵消，讓對的加強'],
 ['比一比：普通電腦和量子電腦', '專門工具，不是更快的筆電',
  '普通電腦', '上網、打字、看影片', '→', '量子電腦', '特殊結構的難題',
  '兩種電腦一起工作',
  '量子電腦負責最難的一小段'],
 ['有機會變快的三種問題', '加速的大小不一樣',
  '01 分解大數', '秀爾演算法，快非常多', '02 無序搜尋', '格羅弗搜尋，平方根', '03 模擬分子', '費曼的點子',
  '要有特殊結構，才有加速'],
 ['不會變快的事', '你的電腦還是最好用',
  '上網  →  打字  →  看影片  →  玩遊戲',
  '不需要', '干涉的結構', '大量資料', '讀進來就很慢', '還很嬌貴', '怕熱，也怕雜訊',
  '量子電腦不會取代你的電腦'],
 ['活動：宣稱卡分類', '十二張卡，分成三堆',
  '一、有機會變快\n二、不會變快\n三、說錯了',
  '每張卡', '都要說出理由', '先猜\n再對答案',
  '暫停影片：這張卡放哪一堆？'],
 ['冒險任務', '你找答案，爸爸把關',
  '探險家（你）', '放一張卡\n說一個理由',
  '守門人（爸爸）', '追問證據\n決定過關',
  '說不出來？寫進問題清單'],
 ['換你出題', '下半場，自己找、自己判斷',
  '01', '我的量子問題清單', '寫下十個問題',
  '02', '找一句新聞說法', '判斷屬於哪一堆',
  '03', '打開三維動畫', '跟著一次量子計算走'],
 ['兩小時的開學任務', '影片先引路，接下來分、寫、查、教',
  '00–25', '開場十分＋工具箱十五分', '25–65', '宣稱卡分類', '65–75', '休息十分鐘',
  '75–105', '問題清單＋查一句新聞', '105–115', '換你教爸爸', '115–120', '錄音總結＋保存',
  '今日生活技能：查證，先問證據'],
 ['最後一關：教爸爸量子快在哪', '暫停影片：不看稿說一次，再指出一個限制',
  '01', '說出迷思錯在哪', '測量只得到一個結果',
  '02', '各舉一個例子', '會變快、不會變快',
  '03', '指出一個限制', '格羅弗只快平方根',
  '保持好奇，我們下次見！'],
]

BOARD = [
 ('開場：學程與課前教學版揭露、今天要檢查的說法', '封面版型＋陳犀牛', '聽一句常見說法'),
 ('學程地圖：96 堂、三階段', '三步流程卡＋黃字', '認識學程'),
 ('迷思：同時試所有答案', '三點條列＋陳犀牛', '找出說法的漏洞'),
 ('概念：量子工具箱四樣', '面板四張卡＋黃字', '說出四樣工具'),
 ('比較：普通電腦與量子電腦', '雙框對照＋白字＋黃字', '說出專門工具的意思'),
 ('例子：有機會變快的三種問題', '三張步驟卡＋黃字', '比較加速大小'),
 ('例子：不會變快的事', '路徑一行＋三張卡＋黃字', '說出三個原因'),
 ('活動：宣稱卡分類', '左三行＋右欄＋黃字', '分三堆、說理由'),
 ('遊戲：冒險任務', '左右比較卡＋黃字', '探險家與守門人'),
 ('獨立改造：換你出題', '三點條列＋陳犀牛', '寫問題清單、查新聞、看動畫'),
 ('120 分鐘安排', '六列時間表＋黃字', '照時間表進行'),
 ('驗收與結尾：迷思、例子、限制；預告 Q002', '三點條列＋陳犀牛＋結尾語', '孩子教爸爸；錄音總結'),
]


def doc(name):
    return (HERE / name).read_text(encoding='utf-8')


README = '''# 父子科技學院 量子電腦學程 Q001

依量子電腦學程課綱製作的課前教學版，主題「開學任務：量子電腦不是更快的電腦」。
製作流程借用父子科技學院的可攜流程（特別篇路線）；來源、旁白、PPTX、教材與 QC 都留在本集資料夾，先讀 `production/START_HERE.md`。
大型成品（MP4、交付 ZIP）不進 Git；檔名、大小、SHA-256 與取得方式見 `delivery.json`，檢視方法與限制見 `qc/manual-review.md`。
不含課堂私人錄音，也沒有偽造逐字稿。YouTube 由使用者自行上傳。
'''

if __name__ == '__main__':
    E = special_builder.build(
        special=LESSON, slug=SLUG, title=TITLE, header_en='QUANTUM 101', cover_disclosure=DISCLOSURE,
        first_sentence_needles=(DISCLOSURE, '並非實際上課錄音'), summary_prefix='這是依課綱製作的課前教學版，不是實際上課錄音',
        checked=CHECKED, src=SRC, scenes=SCENES, visible=VISIBLE, board=BOARD,
        render_options={'asianLatinAutoSpace': False, 'captionLineBreak': 'kinsoku'},
        tts_basis='On 2026-11-07 the user asked to make one episode of the new quantum computing track with the academy opening and voice; '
                  'the public narration script goes to Edge TTS on the same basis as the academy lessons.',
        source_records=SOURCE_RECORDS,
        source_method='Claims mapped to primary papers and the author PDFs of two Scott Aaronson articles; a research sub-agent fetched the pages '
                      'and returned verbatim quotes (production/source-notes.md). Repo slides were read by the producing agent.',
        not_verified=['「一百萬筆約不到一千次」由 (π/4)√N ≈ 785 推算，Grover 原文寫的是 O(√N)',
                      '「快非常多」是對超多項式差距的口語說法，沒有給具體倍數',
                      '課綱的三組 YouTube 搜尋入口本次未挑選或觀看'],
        documents={'fact-check.md': doc('fact-check.md'), 'plan.md': doc('plan.md'),
                   'delivery-summary.md': doc('delivery-summary.md'), 'source-notes.md': doc('source-notes.md')},
        readme=README, content_mode='curriculum-based-preclass',
        delivery_label='量子電腦學程・依課綱製作的課前教學版（無課堂錄音）',
        classroom_note='classroom.zip 是 Q001 的課堂教材（宣稱卡、分類板、問題清單、解答）。課堂 120 分鐘與影片片長分開。')
    m = json.loads((E / 'production/manifest.json').read_text(encoding='utf-8'))
    m['subtitle'] = '父子科技學院 量子電腦學程 第一堂｜依課綱製作的課前教學版'
    m['seriesHeader'] = '父子科技學院 量子電腦學程  ·  QUANTUM 101'
    m['program'] = {'name': '量子電腦學程', 'lessonId': LESSON, 'repo': 'pcpcchen-coder/QuantumComputing',
                    'lessonRecord': 'academy/lessons/Q001/lesson.json'}
    (E / 'production/manifest.json').write_text(json.dumps(m, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('episode:', E)
