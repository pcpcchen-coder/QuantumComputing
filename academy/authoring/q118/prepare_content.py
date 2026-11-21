"""Q118 範例 5：隱形傳態——四種 ψ — production sources (12 scenes / 36 sentences).

    cd $XINEW_ACADEMY && ./portable-runtime.sh python ~/QuantumComputing/academy/authoring/q118/prepare_content.py
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import qbuild  # noqa: E402

HERE = Path(__file__).resolve().parent
LESSON, SLUG, CHECKED = 'Q118', 'q118-teleport-four-psi', '2026-11-18'
TITLE = '範例 5：隱形傳態——四種 ψ'
TOPIC = '範例 5：隱形傳態——四種 ψ'
REPO = 'pcpcchen-coder/QuantumComputing'
SRC = {
    'curriculum': f'{REPO} academy/lessons/Q118/lesson.json',
    'bc_talk': f'{REPO} slides/output/basic-circuits.pptx（第 15、16、17 頁；原始稿 slides/reports/basic-circuits.js）',
    'scene': f'{REPO} animations/basic-circuits.html（#teleport：選項「要傳的狀態 ψ」√¾|0⟩+½|1⟩／|1⟩／|+⟩／|−⟩、四步電路、振幅柱子、「單看 q0」「單看 q2」Bloch 球、量測 q2）',
    'op': f'{REPO} animations/operation.html#circuit（animations/js/operation/06_circuit.js：「量子隱形傳態」線路 8 欄，延遲量測的受控閘修正）',
    'tele': 'https://en.wikipedia.org/wiki/Quantum_teleportation',
    'dmp': 'https://en.wikipedia.org/wiki/Deferred_measurement_principle',
    'noclone': 'https://en.wikipedia.org/wiki/No-cloning_theorem',
    'nocomm': 'https://en.wikipedia.org/wiki/No-communication_theorem',
    'run': f'{REPO} academy/authoring/q118/classroom.py（teleport_lab.py、qiskit_check.py 實跑紀錄）',
}
SOURCE_RECORDS = [
    {'id': 'curriculum', 'title': '量子電腦學程 Q118 課綱', 'publisher': REPO, 'url': SRC['curriculum'],
     'usedFor': '主題、學習目標（用延遲量測版看 Alice 量到什麼、Bob 怎麼修，以及狀態怎麼搬家）、動手任務（四種 ψ 各傳一次，用 Bloch 球確認 Bob 收到的狀態）、'
                '孩子獨立改造（拿掉修正步驟，看 Bob 的狀態變成什麼）、好玩機制（角色扮演：三人傳送）、作品（傳送流程表）、生活技能（通訊是不可少的一環）、'
                '120 分鐘流程、驗收與常見誤解（沒有古典通訊就無法完成，所以不能超光速）'},
    {'id': 'bc_talk', 'title': '量子電路入門：八個範例（簡報）第 15、16、17 頁', 'publisher': REPO, 'url': SRC['bc_talk'],
     'usedFor': '第 15 頁「範例 5｜隱形傳態：用糾纏把狀態送過去」：q0、q1 |0⟩（Alice）、q2 |0⟩（Bob）；① 準備 ψ（例 ψ = √¾|0⟩ + ½|1⟩，Alice 不必知道 ψ 是什麼）'
                '② 建立糾纏對（H + CNOT：q1、q2 成為 Bell 態；q2 交給遠方的 Bob）③ Alice：CNOT、H（Bell 量測的前半；量 q0、q1 得到 2 個位元）'
                '④ Bob：依結果修正（q1 = 1 做 X、q0 = 1 做 Z：q2 就變成 ψ）；備註「用一個 Ry 閘準備出來」「她把這兩個位元用電話告訴 Bob」「整個過程沒有搬動任何粒子」。'
                '第 16 頁「Alice 量到什麼、Bob 怎麼修」表格：q1 q0 = 00、01、10、11 各 ¼，Bob 的 q2 是 ψ、Zψ、Xψ、XZψ，修正：不用修、Z、X、先 X 再 Z，修正後都是 ψ；'
                '「收到 2 個位元之前，Bob 不知道是哪一種，q2 對他來說完全隨機：隱形傳態不能超光速」。'
                '第 17 頁「動畫：用 Bloch 球看狀態搬家」：② 之後 q2 縮到球心；④ 之後 q2 指向 ψ，q0 卻不再是 ψ（不可複製定理）；|+⟩ 和 |−⟩ 量起來都是 50/50，要看 Bloch 球才分得出來；'
                '動畫用受控閘代替「量測後再修正」（延遲量測原理），q2 的結果相同'},
    {'id': 'scene', 'title': '互動動畫：八個基礎量子電路（basic-circuits.html）#teleport', 'publisher': REPO, 'url': SRC['scene'],
     'usedFor': '選項「要傳的狀態 ψ」：√¾|0⟩+½|1⟩（預設，Ry(π/3)）、|1⟩（X）、|+⟩（H）、|−⟩（X、H）；四步：準備 ψ、建立糾纏對（H、CNOT q1→q2）、Alice（CNOT q0→q1、H q0）、'
                'Bob 修正（虛線框「修正（2 個古典位元）」：CNOT q1→q2、CZ q0、q2）；兩顆 Bloch 球「單看 q0」「單看 q2」（reducedBloch）；只量 q2；'
                '最後一步的判定「→ 對照 ψ：q2 的量測機率和 ψ 相同」；換選項時停在最後一步、量測清除；按鈕 #bFirst、#bNext、#m1000、#dots'},
    {'id': 'op', 'title': '互動動畫：如何操作量子電腦（operation.html）場景 6 量子線路：一步一步執行', 'publisher': REPO, 'url': SRC['op'],
     'usedFor': '「量子隱形傳態」線路 8 欄：Ry(2π/3) 準備 q0（P(1) = 0.75）、H、CNOT 做 Bell 對、Alice CNOT、H、「Bob 依 q1 的結果做 X（延遲量測：改成受控閘）」、'
                '「Bob 依 q0 的結果做 Z」、量測 q2：P(1) = 0.75（教材導覽選用；動畫展示段未選用）'},
    {'id': 'tele', 'title': 'Quantum teleportation', 'publisher': 'Wikipedia（2026-11-19 取得的 raw wikitext）', 'url': SRC['tele'],
     'usedFor': '只傳量子資訊、不傳物體；傳送者不必知道要傳的狀態；必須送古典資訊，所以不能比光快；需要能送兩個古典位元的通道、一對 Bell 態、Bell 量測；'
                '四種結果之一和原狀態相同，另外三種經修正（或不修）後相同；原本的資訊被「破壞」、不是複製，不可複製定理仍成立；1993 年理論提出、1997 年兩組實驗完成'},
    {'id': 'dmp', 'title': 'Deferred measurement principle', 'publisher': 'Wikipedia（2026-11-19 取得的 raw wikitext）', 'url': SRC['dmp'],
     'usedFor': '把量測延到最後不影響結果的機率分布；隱形傳態電路的兩種寫法（先量再用古典位元控制 X、Z，或把量測移到最後改用受控 X、Z）；'
                '延遲版需要兩顆位元靠近、能做兩位元閘，因而限制傳送距離'},
    {'id': 'noclone', 'title': 'No-cloning theorem', 'publisher': 'Wikipedia（2026-11-19 取得的 raw wikitext）', 'url': SRC['noclone'],
     'usedFor': '不可能為任意未知的量子態做出一份獨立且相同的複本'},
    {'id': 'nocomm', 'title': 'No-communication theorem', 'publisher': 'Wikipedia（2026-11-19 取得的 raw wikitext）', 'url': SRC['nocomm'],
     'usedFor': '量測糾纏態時，一方無法藉此把資訊傳給另一方，不論距離多遠；不違反狹義相對論的光速限制'},
    {'id': 'run', 'title': 'teleport_lab.py（純 Python）與 qiskit_check.py（Qiskit 2.6.2）實跑結果', 'publisher': REPO, 'url': SRC['run'],
     'usedFor': '四種 ψ 每一步單看 q0、q2 的 Bloch 向量：② 之後 q2 大小 0；④ 之後 q2 = ψ（四種都 True）、q0 四種都停在 (x +1, z 0)；'
                'ψ = √¾|0⟩+½|1⟩ 時 Alice 四種結果各 0.25，Bob 手上是 ψ、Zψ、Xψ、XZψ，修正後都是 ψ；先量再修各傳 1000 次（種子 1118），每次修完都等於 ψ；'
                '不修：四種 q2 都在球心、P(1) 0.50；只修 X：|1⟩ 對，|+⟩、|−⟩ 縮到球心（P(1) 仍 0.50），√¾|0⟩+½|1⟩ 大小 0.50（P(1) 仍 0.25）；'
                'Qiskit 相似度：兩個都修 1.000、不修 0.500'},
]

SCENES = [
 ('範例 5：隱形傳態，四種狀態', [
  '歡迎回到父子科技學院的量子電腦學程，我是陳犀牛，今天是量子第一百一十八堂，範例五，隱形傳態，這是依課綱製作的課前教學版，並非實際上課錄音。',
  '上一堂把受控反閘串成一條鏈，讓三顆位元一起糾纏；今天換個用途，拿一對糾纏的位元當通道，把一顆位元的狀態送到遠方。',
  '今天要記住一句話：隱形傳態搬的是狀態，不是粒子，而且一定要再打一通普通的電話，所以快不過光。'], ['curriculum', 'bc_talk', 'tele']),
 ('角色扮演：三人傳送', [
  '今天的玩法是三人傳送：一個人當愛麗絲，一個人當鮑伯，第三個人當信差，負責把兩個位元的消息送到鮑伯手上。',
  '家裡只有兩個人也沒關係，信差可以由一張小紙條來扮演，重點是紙條送到之前，鮑伯什麼都不能做。',
  '今天的作品是一張傳送流程表，四種狀態各傳一次，記下每一步誰做了什麼、鮑伯最後收到什麼。'], ['curriculum', 'bc_talk']),
 ('範例 5：四個步驟', [
  '先看簡報第十五頁的範例五：三條線都從零態出發，編號零和編號一在愛麗絲那邊，編號二在遠方的鮑伯手上。',
  '第一步在編號零準備要傳的狀態；第二步用哈達瑪閘加受控反閘，讓編號一和編號二變成一對貝爾態。',
  '第三步愛麗絲做受控反閘和哈達瑪閘，量出兩個位元；第四步鮑伯照這兩個位元修正，編號二就變成要傳的狀態。'], ['bc_talk', 'scene', 'tele']),
 ('愛麗絲量到什麼、鮑伯怎麼修', [
  '簡報第十六頁把愛麗絲的結果列成一張表：編號一和編號零兩個位元，零零、零一、一零、一一，各占四分之一。',
  '量到零零，鮑伯手上已經是要傳的狀態；零一要補一個相位翻轉閘，一零要補翻轉閘，一一兩個都要補。',
  '口訣是：編號一是一就做翻轉閘，編號零是一就做相位翻轉閘；不管是哪一種，修完都一樣。'], ['bc_talk', 'tele', 'run']),
 ('紙條送到之前：完全隨機', [
  '表格最下面那句最重要：紙條送到之前，鮑伯不知道是四種的哪一種，四種混在一起，他手上的位元完全隨機。',
  '這時候鮑伯自己去量，不管愛麗絲要傳的是哪一種狀態，都是一半零、一半一，看不出任何消息。',
  '所以隱形傳態不能超光速：消息一定要靠信差跑一趟，而信差再快，也快不過光。'], ['bc_talk', 'tele', 'nocomm', 'run']),
 ('延遲量測版：動畫怎麼做', [
  '動畫用的是延遲量測版：不在中間真的量測，而是把鮑伯的兩個修正，改成由編號一和編號零控制的受控閘。',
  '修翻轉的是受控反閘，修相位的是受控相位翻轉閘；鮑伯手上的結果，和先量再修完全一樣。',
  '好處是可以一步一步看振幅；但受控閘要三顆位元靠在一起，真的要傳到遠方，還是得先量，再打電話。'], ['bc_talk', 'scene', 'dmp']),
 ('四種狀態：鮑伯收到什麼', [
  '動畫可以換四種要傳的狀態：零態占四分之三的那一種、一態、正號疊加態，還有負號疊加態。',
  '第一種傳完，鮑伯量到零的機率是四分之三；一態傳完，鮑伯的箭頭指向南極，每次都量到一。',
  '正號和負號疊加態量起來都是一半一半，分不出來；要看布洛赫球，鮑伯的箭頭停在赤道上兩個相反的方向。'], ['bc_talk', 'scene', 'run']),
 ('常見誤解：複製、瞬移、超光速', [
  '第一個誤解是以為狀態被複製了一份；其實傳完以後，編號零的箭頭不管傳哪一種，都停在同一個方向，原來的資訊已經不在它身上。',
  '第二個誤解是以為有東西瞬間飛過去；其實沒有粒子移動，鮑伯的位元本來就在他手上，改變的只是它的狀態。',
  '第三個是以為比光快；沒有那兩個位元，鮑伯什麼都做不了，這也是今天驗收要你說出來的限制。'], ['bc_talk', 'tele', 'noclone', 'run']),
 ('父子共同實作：四種狀態各傳一次', [
  '上半場一起實作：打開線路入門動畫的範例五，上方選要傳的狀態，回到起點，四步一步一步按。',
  '每一步都看柱子下面的兩顆布洛赫球：左邊是愛麗絲的編號零，右邊是鮑伯的編號二，把箭頭的位置畫進流程表。',
  '四種都走到最後，按量測一千次，對照鮑伯量到的比例，和一開始要傳的狀態是不是一樣。'], ['curriculum', 'scene']),
 ('換你改造：拿掉修正', [
  '下半場換你出手：在教材的小程式裡，把鮑伯的修正拿掉，先猜他的位元會變成什麼，再執行。',
  '我們真的跑過：拿掉修正以後，四種狀態送過去，鮑伯的箭頭全部縮在球心，量起來都是一半一半。',
  '再試只修一半，只補翻轉閘：一態照樣傳對；正號疊加態量起來也還是一半一半，但箭頭縮進球心，其實傳錯了。'], ['curriculum', 'run']),
 ('兩小時的傳送流程表', [
  '兩小時的安排是：開場十分鐘，概念示範十五分鐘，接著四十分鐘，四種狀態各傳一次，用布洛赫球確認，然後休息十分鐘。',
  '下半場三十分鐘，拿掉修正步驟，看鮑伯的位元變成什麼；接著十分鐘角色互換，由你教爸爸操作和原理。',
  '最後五分鐘錄音總結、替流程表命名、存一個版本；今天的生活技能是通訊不可少，少了那通電話，什麼都傳不過去。'], ['curriculum']),
 ('最後一關：教爸爸傳送', [
  '最後一關請不看稿說出：愛麗絲要做哪些步驟，鮑伯又怎麼依照兩個位元修正？',
  '再指出一個限制：沒有普通的通訊就完成不了，所以隱形傳態不能超光速；而且傳完以後，原本那顆不再保有那個狀態。',
  '今天的作品是傳送流程表，下一堂是範例六，德意志演算法，用紅綠球搖獎機來猜黑盒子；我是陳犀牛，保持好奇，我們下次見！'], ['curriculum', 'bc_talk', 'tele']),
]

VISIBLE = [
 ['量子電腦學程 第一百一十八堂', '範例 5 隱形傳態：\n四種 ψ 各傳一次', '搬的是狀態，不是粒子', '量子第一百一十八堂  ·  依課綱製作的課前教學版'],
 ['角色扮演：三人傳送', 'Alice、信差、Bob，各演一角',
  '01 Alice', '手上有\n要傳的 ψ', '→', '02 信差', '送 2 個位元\n（古典通訊）', '→', '03 Bob', '照紙條修正\n收到 ψ',
  '今天的作品：傳送流程表'],
 ['範例 5：四個步驟', '簡報第 15 頁：q0、q1 在 Alice，q2 在遠方的 Bob',
  '01', '① 準備 ψ ＋ ② 糾纏對', 'q0 放 ψ；H + CNOT：q1、q2 成 Bell 態',
  '02', '③ Alice：CNOT、H', '量 q0、q1 → 得到 2 個位元',
  '03', '④ Bob：依結果修正', 'q1 = 1 做 X、q0 = 1 做 Z → q2 = ψ'],
 ['Alice 量到什麼、Bob 怎麼修', '簡報第 16 頁：q1 q0 四種結果，各 ¼', '此時 Bob 的 q2 → 修正',
  '00', 'ψ：不用修', '01', 'Zψ：做 Z', '10', 'Xψ：做 X', '11', 'XZψ：先 X、再 Z',
  '四種修完都是 ψ'],
 ['紙條送到之前：完全隨機', '隱形傳態不能超光速',
  '收到之前', 'q2 在球心：0、1 各半', '→', '收到 2 個位元', '修正後 q2 = ψ',
  '沒有古典通訊 → 什麼都傳不過去',
  '信差再快，也快不過光'],
 ['延遲量測版：動畫怎麼做', '用受控閘代替「量測後再修正」',
  '01 先量再修', '量完送紙條，再做 X、Z', '02 延遲量測', '改用受控 X、受控 Z', '03 結果', 'Bob 的 q2 完全相同',
  '受控閘要三顆靠近；傳遠要先量'],
 ['四種 ψ：Bob 收到什麼', '簡報第 17 頁：看「單看 q2」的 Bloch 球',
  'ψ（q0）  →  糾纏後 q2 在球心  →  修正後 q2 = ψ',
  '√¾|0⟩+½|1⟩', 'q2 量到 0：75%', '|1⟩', '指向南極：100% 是 1', '|+⟩、|−⟩', '都是 50/50，方向相反',
  '量測分不出 |+⟩、|−⟩：看 Bloch 球'],
 ['常見誤解：複製？瞬移？超光速？', '狀態搬家，不是影印',
  '一、不是複製：q0 不再有 ψ\n二、沒有粒子飛過去\n三、不能超光速',
  '正確說法', '1 對糾纏位元 ＋ 2 個古典位元', '沒有古典通訊\n就完成不了',
  '不可複製定理：搬過去，不是複製'],
 ['父子共同實作：四種 ψ 各傳一次', 'basic-circuits.html#teleport',
  'ψ：√¾|0⟩+½|1⟩、|1⟩', '起點 → 下一步 ×4\n看單看 q0、單看 q2',
  'ψ：|+⟩、|−⟩', '走完量 1,000 次\n對照 ψ 的機率',
  '箭頭位置畫進傳送流程表'],
 ['換你改造：拿掉修正', '先預測，再驗證',
  '01', '不修', 'teleport_lab.py：四種都縮在球心',
  '02', '只修 X', '|1⟩ 傳對，|+⟩ 卻縮進球心',
  '03', '先量再修', '真的量測、送紙條，各傳 1000 次'],
 ['兩小時的傳送流程表', '影片先引路，接下來傳、看、拆、教',
  '00–25', '開場＋範例 5 四步驟', '25–65', '四種 ψ 各傳一次', '65–75', '休息十分鐘',
  '75–105', '拿掉修正步驟', '105–115', '換你教爸爸', '115–120', '錄音總結＋保存',
  '今日生活技能：通訊不可少'],
 ['最後一關：教爸爸傳送', '暫停影片：不看稿說一次，再指出一個限制',
  '01', '說出步驟', '糾纏對 → Alice 做 CNOT、H → 量 2 個位元',
  '02', '說出修正', 'q1 = 1 做 X；q0 = 1 做 Z',
  '03', '指出限制', '沒有古典通訊就不行：不能超光速',
  '保持好奇，我們下次見！'],
]

BOARD = [
 ('開場：課前教學版揭露、範例 5、今天的一句話', '封面版型＋陳犀牛', '說出今天要做的作品'),
 ('角色扮演：Alice、信差、Bob', '三步流程卡＋黃字', '認識傳送流程表'),
 ('範例 5 的四個步驟（簡報第 15 頁）', '三點條列＋陳犀牛', '說出每一步誰做了什麼'),
 ('Alice 的四種結果與 Bob 的修正（簡報第 16 頁）', '面板四張卡＋黃字', '背出修正口訣'),
 ('收到之前完全隨機：不能超光速', '雙框對照＋白字＋黃字', '說明為什麼一定要古典通訊'),
 ('延遲量測版：受控閘代替先量再修', '三張步驟卡＋黃字', '比較兩種寫法'),
 ('四種 ψ 傳完的 Bloch 球（簡報第 17 頁）', '路徑一行＋三張卡＋黃字', '預測 Bob 的箭頭方向'),
 ('常見誤解：複製、瞬移、超光速', '左三行＋右欄＋黃字', '說出不可複製定理的意思'),
 ('父子共同實作：四種 ψ 各傳一次', '左右比較卡＋黃字', '在動畫逐步播放並量測'),
 ('獨立改造：拿掉修正、只修一半、先量再修', '三點條列＋陳犀牛', '跑 teleport_lab.py 驗證預測'),
 ('120 分鐘安排', '六列時間表＋黃字', '照時間表進行'),
 ('驗收與結尾：步驟、修正、限制；預告 Q119', '三點條列＋陳犀牛＋結尾語', '孩子教爸爸；錄音總結'),
]

if __name__ == '__main__':
    qbuild.build(
        here=HERE, lesson=LESSON, slug=SLUG, title=TITLE, topic=TOPIC, header_en='QUANTUM 101', checked=CHECKED,
        src=SRC, source_records=SOURCE_RECORDS, scenes=SCENES, visible=VISIBLE, board=BOARD,
        source_method='Quantum teleportation, Deferred measurement principle, No-cloning theorem and No-communication theorem claims from Wikipedia raw wikitext '
                      'fetched by the producing agent on 2026-11-19 (verbatim quotes in production/source-notes.md); repo slides (basic-circuits.pptx pages 15-17, read with '
                      'python-pptx, and their source slides/reports/basic-circuits.js) and animation source (basic-circuits.html #teleport, js/operation/06_circuit.js) read by '
                      'the producing agent and checked with Playwright screenshots; Bloch vectors, Alice outcome table, measure-then-correct runs and missing-correction '
                      'results from actually running teleport_lab.py (pure Python 3.13.18, random seed 1118) and qiskit_check.py (Qiskit 2.6.2, StatevectorSampler seed=2026).',
        not_verified=['「真的要傳到遠方還是得先量再打電話」依 Deferred measurement principle 條目的圖說（延遲版需兩顆位元靠近、限制傳送距離）；本課未另查特定實驗的實作細節',
                      '本課四種 ψ 的振幅都是實數，Bloch 向量只有 x、z 分量；複數振幅（y 方向）的 ψ 不在本課範圍',
                      '延遲量測版傳完後 q0 停在 |+⟩（單看 q0 的向量指向 +x）是這種寫法的結果；真實的「先量再修」版本 q0 會被量成 0 或 1',
                      '課綱的三組 YouTube 搜尋入口本次未挑選或觀看'],
        tts_date='2026-11-18')
