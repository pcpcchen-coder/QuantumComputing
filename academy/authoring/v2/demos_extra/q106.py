"""Q106 第 8 課：糾纏與兩位元 Grover — v2 動畫展示段（格式見 ../demos.py 的說明）。

tr = animations/transmon-3d.html 第 7 章 #grover：步驟按鈕在 #g7steps，「暫停／播放」是 #g7play，「自動接續」是 #g7auto。
進場時第 7 章會自動從步驟 1 開始播，所以每段一開頭先取消自動接續、按要用的步驟（setup 會重設振幅），
再立刻按暫停（步驟時間停在約 0.1 秒），等旁白說到時按播放，讓步驟腳本裡固定的 cue 時間對上旁白。
步驟 1 cue：4.5 秒 H⊗H、13.5 秒 CZ、23 秒 H(Q2)、27.5 秒量 40 次（每秒 20 次）。
步驟 3 cue：0.3 秒 X(Q2)、5 秒 CZ、9.5 秒 X(Q2)；步驟 4：0.3 秒平均線、5 秒擴散（先 0.7 秒讓平均線出現，2.4 秒完成）；
步驟 5：0.3 秒量 50 次。
bc = animations/basic-circuits.html#grover：#opts 裡依序是「位元數」「答案」「重複輪數」三組 .seg；改選項後停在最後一步、量測清零。
"""

LESSON = 'Q106'

# transmon-3d 第 7 章：把右側讀數（a₀₀·a₁₁、a₀₁·a₁₀、判定）與量測結果捲到面板頂端
_G7_STATS = "document.getElementById('g7p1').closest('dl').scrollIntoView({block:'start'});"
# basic-circuits.html 是一般網頁：縮小並捲到範例標題，讓選項、電路、振幅與量測卡同時入鏡（同 q010）
_BC_FIT = ("document.body.style.zoom='0.62';"
           "document.querySelector('#sceneTitle').scrollIntoView({block:'start'});"
           "window.scrollBy(0,-8);")

_LIST = [
 dict(key='bell', after=4, page='tr', hash='grover', scene='transmon 3D 第 7 章：振幅長條——步驟 1 糾纏',
      title='動畫展示：一個負號做出貝爾態', sub='三維動畫：振幅長條——乘積態變成糾纏',
      sentences=[
       '按下超導晶片動畫第七章的第一步，一開始只有零零那根柱子頂到一；接著兩顆都做哈達瑪閘，四根變得一樣高。',
       '柱子右邊的兩個乘積都是正零點二五，判定是乘積態；接著送受控相位翻轉閘，一一那根翻到下面變成紅色，判定立刻變成糾纏。',
       '第二顆再做一次哈達瑪閘，只剩零零和一一兩根，各是零點七一；動畫接著量四十次，右邊面板的結果只有零零和一一。'],
      actions=[(0, 0.1, ('id', 'g7auto')), (0, 0.3, ('sel', '#g7steps button:nth-child(1)')),
               (0, 0.8, ('js', _G7_STATS))],
      points=[('H⊗H', '四根都是 +½，乘積態'), ('CZ', '|11⟩ 變紅，判定變糾纏'), ('H(Q2)', '只剩 00 和 11')], shot=(2, 10.0)),
 dict(key='grover', after=7, page='tr', hash='grover', scene='transmon 3D 第 7 章：振幅長條——步驟 3–5 Grover',
      title='動畫展示：標記、擴散、一次找到', sub='三維動畫：振幅長條——兩位元 Grover（答案 10）',
      sentences=[
       '接著按第三步，看寶藏一零怎麼被標記，柱子下方的金色星號標出寶藏的位置；先對第二顆做翻轉閘，一零和一一對調，看起來沒變。',
       '然後送受控相位翻轉閘，一一翻成紅色的負二分之一；再對第二顆做一次翻轉閘換回來，紅色就搬到寶藏一零，四個機率仍然各四分之一。',
       '按第四步，金色橫線就是平均，停在四分之一的高度；擴散開始，每根柱子以這條線當鏡子翻過去，三根變成零，寶藏衝到一。',
       '最後按第五步量五十次，每一次都是一零，寶藏只開一次就找到了。'],
      actions=[(0, 0.1, ('id', 'g7auto')), (0, 0.3, ('sel', '#g7steps button:nth-child(3)')), (0, 0.4, ('id', 'g7play')),
               (0, 8.1, ('id', 'g7play')),
               (2, 0.3, ('sel', '#g7steps button:nth-child(4)')),
               (3, 0.3, ('sel', '#g7steps button:nth-child(5)'))],
      points=[('標記', '10 翻成紅色 −½'), ('金色平均線', '停在 +¼'), ('擴散之後', '10 = 1，量 50 次都是 10')], shot=(2, 10.0)),
 dict(key='more', after=10, page='bc', hash='grover', scene='量子電路入門互動動畫：Grover 搜尋',
      title='動畫展示：換答案、加位元', sub='三維動畫：量子電路入門——Grover 的位元數與輪數',
      sentences=[
       '打開線路入門動畫的格羅弗範例，上方可以選位元數、答案和重複輪數，預設是兩顆位元、答案一一。',
       '把右邊那一位切成零，答案換成一零，畫面直接跳到最後一步，一零那根頂到一；按量測一千次，全部都是一零。',
       '改成三顆位元，選項變成八個，動畫照最佳輪數做兩輪，答案一零一的機率是百分之九十四點五，不是百分之百；量一千次，還會冒出少數別的結果。',
       '再把輪數改成三輪，答案那根反而變矮，機率掉到百分之三十三，這就是轉過頭。'],
      actions=[(0, 0.2, ('js', _BC_FIT)),
               (1, 1.5, ('sel', '#opts div.seg:nth-of-type(2) button:nth-child(2)')), (1, 8.3, ('sel', '#m1000')),
               (2, 0.6, ('sel', '#opts div.seg:nth-of-type(1) button:nth-child(2)')), (2, 11.3, ('sel', '#m1000')),
               (3, 1.4, ('sel', '#opts div.seg:nth-of-type(3) button:nth-child(4)'))],
      points=[('兩顆位元', '換答案也是一輪 100%'), ('三顆位元', '最佳兩輪約 94.5%'), ('做三輪', '掉到 33%，轉過頭')], shot=(2, 13.5)),
]


class _Demos(list):
    """清單（demos.py 的載入方式：DEMOS[LESSON] = 本模組.DEMOS），同時也能用 DEMOS['Q106'] 取用。"""

    def __getitem__(self, k):
        return list(self) if k == LESSON else super().__getitem__(k)

    def get(self, k, default=None):
        return list(self) if k == LESSON else default

    def keys(self):
        return [LESSON]

    def values(self):
        return [list(self)]

    def items(self):
        return [(LESSON, list(self))]


DEMOS = _Demos(_LIST)
