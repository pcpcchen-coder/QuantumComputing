"""Q023 約瑟夫森接面：超導三明治 — production sources (12 scenes / 36 sentences).

    cd $XINEW_ACADEMY && ./portable-runtime.sh python /home/user/QuantumComputing/academy/authoring/q023/prepare_content.py
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import qbuild  # noqa: E402

HERE = Path(__file__).resolve().parent
LESSON, SLUG, CHECKED = 'Q023', 'q023-josephson-junction-sandwich', '2026-11-18'
TITLE = '約瑟夫森接面：超導三明治'
TOPIC = '約瑟夫森接面：超導三明治'
REPO = 'pcpcchen-coder/QuantumComputing'
SRC = {
    'curriculum': f'{REPO} academy/lessons/Q023/lesson.json',
    'neighbors': f'{REPO} academy/lessons/Q022/brief.md、academy/lessons/Q024/brief.md',
    'jj_talk_p12': f'{REPO} slides/JJ_Microwave_Readout_Talk.pptx p12（含講者備註）',
    'jj_talk_p13': f'{REPO} slides/JJ_Microwave_Readout_Talk.pptx p13（含講者備註）',
    'ep049_p5': f'{REPO} slides/output/ep049-superconducting-qubit.pptx p5（含講者備註）',
    'jj_notes': f'{REPO} notes/josephson-junction-wave-and-tunneling.md',
    'jj_scene': f'{REPO} animations/index.html#jj（animations/js/scenes/03_jj.js）',
    'wiki_je': 'https://en.wikipedia.org/wiki/Josephson_effect',
    'wiki_bj': 'https://en.wikipedia.org/wiki/Brian_Josephson',
    'wiki_tunnel': 'https://en.wikipedia.org/wiki/Quantum_tunnelling',
    'wiki_jvs': 'https://en.wikipedia.org/wiki/Josephson_voltage_standard',
}
SOURCE_RECORDS = [
    {'id': 'curriculum', 'title': '量子電腦學程 Q023 課綱', 'publisher': REPO, 'url': SRC['curriculum'],
     'usedFor': '主題、學習目標（認識 SIS 結構、Cooper pair 穿隧與 DC／AC Josephson 效應）、動手任務（用兩片吐司夾一層薄紙做 JJ 模型，標出超導、絕緣、相位差）、'
                '孩子獨立改造（寫一段 30 秒說明，解釋「穿隧」不是挖洞穿過去）、好玩機制（Maker 挑戰：紙模型）、作品（JJ 紙模型＋標註）、家長課前準備（紙材或食物模型）、'
                '120 分鐘流程、驗收與常見誤解（絕緣層只有約 1–2 奈米；穿隧是波的性質，不是粒子打洞）、生活技能支線（用模型說明結構）'},
    {'id': 'neighbors', 'title': '量子電腦學程 Q022、Q024 課綱', 'publisher': REPO, 'url': SRC['neighbors'],
     'usedFor': '上一堂：量子諧振子——等距的梯子（LC 電路的能階等距，所以無法只挑出兩個能階當量子位元）；'
                '下一堂：JJ 是非線性電感（JJ 的電感會隨電流改變，這個非線性是做出量子位元的關鍵）'},
    {'id': 'jj_talk_p12', 'title': '超導量子電腦的核心：JJ 與微波讀取（簡報）p12：JJ 的結構：超導–絕緣–超導', 'publisher': REPO, 'url': SRC['jj_talk_p12'],
     'usedFor': '材料 Al / AlOx / Al；氧化層厚度 1–2 nm（備註：幾個原子層）；接面面積 ~0.01–0.05 μm²；臨界電流 Ic 20–60 nA；'
                '絕緣層夠薄 → Cooper pair 可整對量子穿隧；兩側超導體各有相位 φ1、φ2，一切由相位差 φ 決定'},
    {'id': 'jj_talk_p13', 'title': '超導量子電腦的核心：JJ 與微波讀取（簡報）p13：Josephson 的兩大關係式', 'publisher': REPO, 'url': SRC['jj_talk_p13'],
     'usedFor': 'DC：I = Ic sin φ，零電壓下就能有超電流，電流大小由相位差決定，最大值 Ic，超過就進入電壓態；'
                'AC：dφ/dt = 2eV/ħ，加電壓 → 相位持續旋轉，電流以 f = V/Φ0 振盪，483.6 GHz/mV，電壓標準的基礎；備註：1962 年 Josephson 預測、後來得諾貝爾獎'},
    {'id': 'ep049_p5', 'title': '《量子超級英雄》#049 報告簡報 p5：回顧：JJ 是什麼', 'publisher': REPO, 'url': SRC['ep049_p5'],
     'usedFor': '結構：超導體｜絕緣體｜超導體；庫柏電子對（2e）成對穿隧 → 超導電流；和一般穿隧不同，不是單顆電子，而是兩個兩個成對過去'},
    {'id': 'jj_notes', 'title': '筆記：約瑟夫森結——巨觀量子波、相位差與「穿隧」的真正意義', 'publisher': REPO, 'url': SRC['jj_notes'],
     'usedFor': '超導體裡庫柏對凝聚成同一個巨觀波函數、共用同一個相位（像踩著同一個節拍）；絕緣層把大波切成兩個波，各有相位 φ₁、φ₂；'
                '穿隧用波定義：波函數進入絕緣層後指數衰減但不立刻消失，夠薄時與另一邊重疊；I_c ∝ e^(−2κd)；V = 0 直流超電流、V ≠ 0 交流（約 483.6 GHz/mV）；'
                'JJ 提供非線性，讓能階不等距（Q022、Q024 的銜接）'},
    {'id': 'jj_scene', 'title': 'JJ 與微波讀取 3D 場景 3：約瑟夫森接面（JJ）的結構與穿隧', 'publisher': REPO, 'url': SRC['jj_scene'],
     'usedFor': '動畫段：兩塊鋁電極（右側半透明）、橘紅色 AlOx 穿隧阻障、相位鐘、Cooper pair 穿過阻障時閃光；偏壓電流按鈕 0.5 Ic／≈ Ic／1.4 Ic、讀數與右下小圖'},
    {'id': 'wiki_je', 'title': 'Wikipedia: Josephson effect', 'publisher': 'Wikipedia', 'url': SRC['wiki_je'],
     'usedFor': '超電流在沒有施加電壓時持續流過約瑟夫森接面；弱連結可以是薄絕緣層（S-I-S）；1962 年 Brian Josephson 預測電流與電壓的關係'},
    {'id': 'wiki_bj', 'title': 'Wikipedia: Brian Josephson', 'publisher': 'Wikipedia', 'url': SRC['wiki_bj'],
     'usedFor': '1962 年在劍橋讀博士期間做出預測（1964 年取得博士）；1973 年諾貝爾物理獎'},
    {'id': 'wiki_tunnel', 'title': 'Wikipedia: Quantum tunnelling', 'publisher': 'Wikipedia', 'url': SRC['wiki_tunnel'],
     'usedFor': '位障內的解是指數衰減的漸逝波；穿透機率隨位障寬度指數下降（厚一倍不是剩一半，而是小很多）'},
    {'id': 'wiki_jvs', 'title': 'Wikipedia: Josephson voltage standard', 'publisher': 'Wikipedia', 'url': SRC['wiki_jvs'],
     'usedFor': '自 1990 年國際協議起是全世界電壓標準的基礎；K_J-90 = 483597.9 GHz/V（約 483.6 GHz/mV）'},
]

SCENES = [
 ('約瑟夫森接面：超導三明治', [
  '歡迎回到父子科技學院的量子電腦學程，我是陳犀牛，今天是量子第二十三堂，約瑟夫森接面：超導三明治，這是依課綱製作的課前教學版，並非實際上課錄音。',
  '上一堂看到電感電容電路的能階像一把間距相等的梯子，沒辦法只挑出兩階來用；要打破這個等距，需要一個特別的超導元件。',
  '這個元件就是約瑟夫森接面，今天先拆開它的結構，看看電子對怎麼穿過去，再認識兩個以約瑟夫森命名的效應。'], ['curriculum', 'neighbors', 'jj_notes']),
 ('三個重點', [
  '今天有三個重點：第一，約瑟夫森接面像一個三明治，兩片超導體中間夾一層非常薄的絕緣體。',
  '第二，超導體裡的電子兩兩成對，可以整對穿過絕緣層，這叫穿隧；第三，兩個效應：不加電壓也有電流，加了電壓電流就會振盪。',
  '今天的作品是一個約瑟夫森接面的紙模型，用兩片吐司夾一張薄紙，再把每一層標清楚。'], ['curriculum', 'jj_talk_p13']),
 ('超導三明治：三層結構', [
  '先看結構：兩片超導體夾一層絕緣體，超導、絕緣、超導，所以常被叫做超導三明治。',
  '量子電腦裡最常見的做法是鋁、氧化鋁、鋁；中間的氧化鋁只有一到兩奈米，大約只有幾個原子層。',
  '這種接面非常小，面積大約只有零點零幾平方微米，能通過的最大超電流大約是幾十奈安培。'], ['jj_talk_p12', 'ep049_p5', 'wiki_je']),
 ('庫柏電子對的穿隧', [
  '超導體裡的電子會兩兩配成一對，叫做庫柏電子對，所有電子對都踩著同一個節拍一起運動。',
  '絕緣層照理會擋住電流，但它夠薄，電子對可以整對穿過去，這叫穿隧；和一般一次只過一顆電子的穿隧不同，這裡是兩個兩個成對過去。',
  '穿隧是波的性質：電子對的波進到絕緣層裡會很快變弱，但不會一下子變成零；牆夠薄，另一邊還剩一點，兩邊的波就接上了。'], ['ep049_p5', 'jj_notes', 'jj_talk_p12', 'wiki_tunnel']),
 ('相位與相位差', [
  '因為所有電子對踩同一個節拍，每一塊超導體都可以用一個相位來描述，就像一個時鐘指針指著的方向。',
  '兩片超導體被絕緣層隔開，各有自己的相位，兩根指針可以指向不同的方向。',
  '兩個相位的差叫做相位差；接下來的兩個效應，都是由這個相位差來決定。'], ['jj_notes', 'jj_talk_p12']),
 ('直流約瑟夫森效應', [
  '第一個效應叫直流約瑟夫森效應：接面兩端不加電壓，也能有電流穿過去，這叫做超電流。',
  '電流的大小等於臨界電流乘上相位差的正弦，相位差九十度時最大，這個最大值就是臨界電流。',
  '如果硬推比臨界電流更大的電流，相位差就鎖不住，接面兩端出現電壓，這時就輪到第二個效應。'], ['jj_talk_p13', 'wiki_je', 'jj_notes']),
 ('交流約瑟夫森效應', [
  '第二個效應叫交流約瑟夫森效應：接面兩端一旦有電壓，相位差就不再固定，而是一直轉下去。',
  '相位差一直轉，電流就跟著來回振盪，頻率和電壓成正比，每一毫伏特大約對應四百八十三點六吉赫。',
  '這個關係非常準，從一九九零年起，世界各地的電壓標準都以它為基礎；約瑟夫森在一九六二年讀研究所時就預測了這些效應，後來得到諾貝爾物理獎。'],
  ['jj_talk_p13', 'jj_notes', 'wiki_jvs', 'wiki_je', 'wiki_bj']),
 ('穿隧不是挖洞', [
  '最常見的誤解是：穿隧好像在牆上挖一個洞鑽過去；其實絕緣層上沒有任何洞，穿隧之後它也完好如初。',
  '真正的原因是波：波在絕緣層裡越來越弱，但絕緣層只有一到兩奈米，到了另一邊還剩一點，所以牆越薄，穿過去的電流就越多。',
  '暫停影片想一想：如果絕緣層變厚一倍，穿過去的電流會剛好變成一半嗎？'], ['curriculum', 'jj_notes', 'wiki_tunnel']),
 ('實作：吐司紙模型', [
  '實作的時候，父子一起做模型：兩片吐司代表兩片超導的鋁，中間夾一張薄紙代表絕緣層。',
  '用便利貼標出超導體和絕緣層，再在兩片吐司上各畫一個時鐘，指針指向不同方向，中間寫上相位差。',
  '最後在模型旁邊寫一個限制：紙其實太厚了，真正的絕緣層只有一到兩奈米，而且穿隧不會在紙上留下洞。'], ['curriculum', 'jj_talk_p12']),
 ('換你改造：三十秒說明', [
  '下半場換你：寫一段三十秒的說明，解釋為什麼穿隧不是挖洞穿過去。',
  '可以分三步：先指著模型說出三明治的三層，再用波說明電子對怎麼過去，最後說出模型和真實接面哪裡不一樣。',
  '寫好以後用碼錶計時念一次，超過三十秒就刪掉多餘的字，不到就補一個例子，念到剛好為止。'], ['curriculum', 'jj_notes']),
 ('兩小時的超導三明治工坊', [
  '兩小時的安排是：開場十分鐘，概念示範十五分鐘，接著四十分鐘一起做吐司紙模型、貼上標註，然後休息十分鐘。',
  '下半場三十分鐘，你寫三十秒的穿隧說明並計時；接著十分鐘交換角色，由你教爸爸這個接面的結構和原理。',
  '最後五分鐘錄音總結，替你的模型取個名字，再存一個版本。'], ['curriculum']),
 ('最後一關：教爸爸認識接面', [
  '最後一關，請不看稿說出：約瑟夫森接面是哪三層？電子對怎麼過去？兩個效應各是什麼？',
  '再指出一個要注意的地方：絕緣層只有一到兩奈米，穿隧是波的性質，不是粒子在牆上打洞。',
  '今天的作品是約瑟夫森接面紙模型，下一堂要看這個接面為什麼像一個非線性電感：它的電感會隨電流改變，這正是做出量子位元的關鍵；我是陳犀牛，保持好奇，我們下次見！'], ['curriculum', 'neighbors']),
]

VISIBLE = [
 ['量子電腦學程 第二十三堂', '約瑟夫森接面\n超導三明治', '兩片超導體，夾一層薄薄的絕緣體', '量子第二十三堂  ·  依課綱製作的課前教學版'],
 ['三個重點', '從結構到兩個效應',
  '01 三層結構', '兩片超導\n夾一層絕緣', '→', '02 電子對穿隧', '兩個一組\n整對過去', '→', '03 兩個效應', '零電壓有電流\n有電壓就振盪',
  '今天的作品：JJ 紙模型＋標註'],
 ['超導三明治：三層結構', '超導｜絕緣｜超導（SIS）',
  '01', '兩片超導體', '量子電路常用鋁',
  '02', '中間夾絕緣層', '氧化鋁，約 1–2 nm',
  '03', '非常小的元件', 'Ic 約 20–60 nA'],
 ['庫柏電子對的穿隧', '兩個一組，整對過去', '四個觀察',
  '第一點', '電子兩兩成對', '第二點', '電荷是 2e', '第三點', '波滲進絕緣層', '第四點', '夠薄才接得上',
  '穿隧靠的是波，不是挖洞'],
 ['相位與相位差', '一塊超導體，一個節拍',
  '超導體 1', '相位 φ₁', '⇄', '超導體 2', '相位 φ₂',
  '相位差 φ = φ₂ − φ₁',
  '兩個效應都由相位差決定'],
 ['直流約瑟夫森效應', '零電壓，也有電流',
  'I = Ic sin φ', '電流跟著相位差', '零電壓', '照樣有超電流', '最大值 Ic', '超過就出現電壓',
  '電流大小由相位差決定'],
 ['交流約瑟夫森效應', '有電壓，相位就一直轉',
  'dφ/dt = 2eV/ħ  →  f = 2eV/h',
  '加電壓 V', '相位差一直轉', '電流', '來回振盪', '每 1 mV', '約 483.6 GHz',
  '各國電壓標準的基礎'],
 ['穿隧不是挖洞', '絕緣層完好如初',
  '一、牆上沒有洞\n二、波在牆裡變弱\n三、夠薄才接得上',
  '絕緣層厚度', '只有約 1–2 nm', '大約\n幾個原子層',
  '暫停影片：厚一倍，電流剩一半嗎？'],
 ['實作：吐司紙模型', '兩片吐司，夾一張薄紙',
  '做模型的人（爸爸）', '兩片吐司\n夾一張薄紙',
  '標註的人（你）', '超導、絕緣\n畫相位時鐘',
  '再寫一個模型的限制'],
 ['換你改造：三十秒說明', '下半場，說清楚「穿隧」',
  '01', '先說結構', '超導｜絕緣｜超導',
  '02', '再說穿隧', '波滲過薄牆，不是挖洞',
  '03', '最後說限制', '模型的紙太厚了'],
 ['兩小時的超導三明治工坊', '影片先引路，接下來做、標、寫、教',
  '00–25', '開場＋接面概念', '25–65', '做模型＋標註', '65–75', '休息十分鐘',
  '75–105', '寫三十秒說明', '105–115', '換你教爸爸', '115–120', '錄音總結＋保存',
  '今日生活技能：用模型說明結構'],
 ['最後一關：教爸爸認識接面', '暫停影片：不看稿說一次，再指出一個注意事項',
  '01', '說出三層結構', '超導｜絕緣｜超導',
  '02', '說出兩個效應', '零電壓有電流、有電壓就振盪',
  '03', '指出一個注意事項', '穿隧是波，不是打洞',
  '保持好奇，我們下次見！'],
]

BOARD = [
 ('開場：課前教學版揭露、從上一堂等距的梯子接到約瑟夫森接面', '封面版型＋陳犀牛', '想一想為什麼需要特別的超導元件'),
 ('三個重點：三層結構、電子對穿隧、兩個效應', '三步流程卡＋黃字', '認識今天的作品'),
 ('三層結構：鋁／氧化鋁／鋁、1–2 nm、面積與 Ic 典型值', '三點條列＋陳犀牛', '說出三明治的三層'),
 ('庫柏電子對穿隧：兩兩成對、2e、波滲進絕緣層、夠薄才接得上', '面板四張卡＋黃字', '說出穿隧靠的是波'),
 ('相位與相位差：兩片超導體各有相位，相位差決定效應', '雙框對照＋白字＋黃字', '用時鐘指針說明相位差'),
 ('直流效應：I = Ic sin φ、零電壓有超電流、超過 Ic 出現電壓', '三張步驟卡＋黃字', '說出零電壓也有電流'),
 ('交流效應：dφ/dt = 2eV/ħ、483.6 GHz/mV、電壓標準、1962 年預測', '路徑一行＋三張卡＋黃字', '說出電壓讓相位一直轉'),
 ('穿隧不是挖洞：牆完好如初、波變弱、絕緣層 1–2 nm', '左三行＋右欄＋黃字', '暫停想厚一倍電流剩一半嗎'),
 ('實作：吐司紙模型，標出超導、絕緣、相位時鐘與相位差', '左右比較卡＋黃字', '父子一起做模型、貼標註'),
 ('獨立改造：三十秒穿隧說明（結構、穿隧、限制）', '三點條列＋陳犀牛', '寫稿、計時、修到剛好'),
 ('120 分鐘安排', '六列時間表＋黃字', '照時間表進行'),
 ('驗收與結尾：三層結構、兩個效應、注意事項；預告 Q024', '三點條列＋陳犀牛＋結尾語', '孩子教爸爸；錄音總結'),
]

if __name__ == '__main__':
    qbuild.build(
        here=HERE, lesson=LESSON, slug=SLUG, title=TITLE, topic=TOPIC, header_en='QUANTUM 101', checked=CHECKED,
        src=SRC, source_records=SOURCE_RECORDS, scenes=SCENES, visible=VISIBLE, board=BOARD,
        source_method='Curriculum rows (Q022, Q023, Q024), the curriculum slide decks JJ_Microwave_Readout_Talk.pptx p12–13 and '
                      'ep049-superconducting-qubit.pptx p5 (slide text, tables and speaker notes extracted with python-pptx), '
                      'notes/josephson-junction-wave-and-tunneling.md, and animations/index.html#jj (js/scenes/03_jj.js) read by the producing '
                      'agent on 2026-11-18; history, tunnelling and voltage-standard facts checked against the Wikipedia articles Josephson effect, '
                      'Brian Josephson, Quantum tunnelling and Josephson voltage standard (raw wikitext fetched 2026-11-18); the tunnelling '
                      'thickness example recomputed by the producing agent with tunnel_check.py.',
        not_verified=['「接面面積約零點零幾平方微米、臨界電流幾十奈安培」取自學程簡報 JJ_Microwave_Readout_Talk p12 的典型值表，不是某一顆晶片的實測值；'
                      '不同實驗室與設計會有差異',
                      '「每一毫伏特約四百八十三點六吉赫」由 2e/h 算出（Josephson voltage standard 條目 K_J-90 = 483597.9 GHz/V）；旁白不展開 2019 年 SI 改制的細節',
                      '「厚一倍電流不是剩一半」只依穿透機率隨位障寬度指數下降的一般性質（Quantum tunnelling 條目、筆記 I_c ∝ e^(−2κd)）；'
                      '教材裡的 κ 是示意值，不是真實氧化鋁的量測值，只用來說明「指數」和「成正比」的差別',
                      '「所有電子對踩著同一個節拍」與「相位像時鐘指針」是筆記中的比喻（同一個巨觀波函數、同一個相位），不是嚴格的物理描述',
                      '吐司紙模型只表示三層的順序，不按比例；本集不估算紙張與真實絕緣層的厚度比',
                      '課綱的三組 YouTube 搜尋入口本次未挑選或觀看',
                      '本集未錄影試拍；動畫段（index.html#jj 面板捲動、按鈕位置與換行、右側青色電壓標籤是否被右下小圖蓋住、低畫格率下相位收斂速度）待 v2 試錄確認'],
        tts_date='2026-11-18')
