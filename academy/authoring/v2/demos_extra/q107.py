"""Q107 第 9 課：Deutsch 演算法與相位回踢 — v2 動畫展示段（格式見 ../demos.py 的說明）。

tr = animations/transmon-3d.html#deutsch-lab（HASH_ALIAS 直接進第 7 章步驟 8「自由實驗」）。
  控制項（第 7 章 extra）：黑盒子 [data-fn="0"～"3"]、[data-fn="hide"]「隨機（隱藏）」；[data-op="X1"] X₂、[data-op="H0"] H₁、
  [data-op="H1"] H₂、[data-op="UF"] U_f；#g7deu「一鍵 Deutsch」；#g7meas「量測 50 次」；#g7reset「重設 |00⟩」。
  自由實驗預設 answer = 2，振幅長條下方會掛「★ 答案」；先用 js（不加黃框）按一次一鍵 Deutsch 再按重設，把 answer 清成 −1、佇列清空，
  畫面回到 |00⟩、電路圖清空，旁白不提這一步。面板比視窗高，用 js 每半秒把面板捲到底，讓按鈕、乘積態判定與量測結果同時入鏡。
  閘動畫由畫面幀推進（dt 上限 0.05 s），錄影幀率低時會比牆鐘慢，動作之間留足間隔。
bc = animations/basic-circuits.html#deutsch（範例 6）：一般網頁，用 sel 點按鈕；縮放並捲到範例標題，讓電路、柱子、布洛赫球與量測卡同時入鏡。
  換選項時 rebuild(false) 會直接跳到最後一步，所以選完函數要按「⏮ 起點」再一步一步走。
"""

LESSON = 'Q107'

# 第 7 章自由實驗：面板捲到底並保持
_PIN = ('js', "(()=>{const pn=document.getElementById('panel');const f=()=>{pn.scrollTop=pn.scrollHeight;};f();"
              "clearInterval(window.__pin);window.__pin=setInterval(f,500);})()")
# 清掉預設的「★ 答案」記號：一鍵 Deutsch 會把 answer 設成 −1，緊接著重設 |00⟩ 清空佇列與電路圖（不加黃框）
_CLEAR = ('js', "(()=>{document.getElementById('g7deu').click();setTimeout(()=>document.getElementById('g7reset').click(),150);})()")
_FN3 = ('sel', '[data-fn="2"]')   # f₃：f(x) = x
# basic-circuits.html：縮放並捲到範例標題
_BC_FIT = ('js', "document.body.style.zoom='0.74';"
                 "document.querySelector('#sceneTitle').scrollIntoView({block:'start'});"
                 "window.scrollBy(0,-6);")

_LIST = [
 dict(key='kick', after=5, page='tr', hash='deutsch-lab', scene='transmon 3D 第 7 章：振幅長條——自由實驗（單步跑 f₃）',
      title='動畫展示：負號搬了家', sub='三維動畫：一個閘一個閘跑德意志演算法',
      sentences=[
       '打開超導晶片動畫第七章的自由實驗，選第三種黑盒子，也就是輸出等於輸入的平衡函數，這次不按一鍵，我們自己一個閘一個閘按。',
       '先對輔助位元按翻轉閘，四根柱子只剩零一那一根，再對兩顆各按一次哈達瑪閘，四根都變成正負二分之一，輔助位元是一的那兩根變成紅色的負值。',
       '按下黑盒子，只問這一次：四個機率都還是百分之二十五，可是負號從一一搬到了一零，右邊的判定照樣寫著乘積態。',
       '最後對輸入位元再按一次哈達瑪閘，只剩一零和一一兩根，按量測五十次，面板上第一位每次都是一，所以是平衡。'],
      actions=[(0, 0.3, _PIN), (0, 0.6, _CLEAR), (0, 4.0, _FN3),
               (1, 0.6, ('sel', '[data-op="X1"]')), (1, 5.6, ('sel', '[data-op="H0"]')), (1, 7.2, ('sel', '[data-op="H1"]')),
               (2, 0.8, ('sel', '[data-op="UF"]')),
               (3, 0.6, ('sel', '[data-op="H0"]')), (3, 5.2, ('id', 'g7meas'))],
      points=[('先翻轉再哈達瑪', '輔助位元變成減態'), ('問一次黑盒子', '負號搬到一零'), ('最後的哈達瑪閘', '第一位每次都是一')], shot=(3, 9.5)),
 dict(key='bloch', after=7, page='bc', hash='deutsch', scene='量子電路入門互動動畫：範例 6 Deutsch 演算法（f(x) = 1 − x）',
      title='動畫展示：輸入位元的箭頭翻面', sub='三維動畫：量子電路入門——第四種黑盒子與布洛赫球',
      sentences=[
       '換到線路入門動畫的德意志範例，上方選最右邊的函數，也就是一減輸入的第四種黑盒子，再按起點從頭走。',
       '按兩次下一步，輔助位元先翻成一，兩顆再做哈達瑪閘；下方兩顆布洛赫球，左邊單看輸入位元，箭頭指向左下，右邊的輔助位元指向反方向。',
       '再按下一步問黑盒子：四根柱子的機率都還是四分之一，正負號卻換了位置，左邊那顆的箭頭一下子翻到右上，和輔助位元指向同一邊。',
       '最後一步對輸入位元做哈達瑪閘，左邊的箭頭轉到正下方的一態；按量測一千次，一千次全部是一，旁邊寫著平衡函數。'],
      actions=[(0, 0.2, _BC_FIT), (0, 3.6, ('sel', '#opts .seg button:nth-child(4)')), (0, 9.2, ('sel', '#bFirst')),
               (1, 0.5, ('sel', '#bNext')), (1, 3.5, ('sel', '#bNext')),
               (2, 0.6, ('sel', '#bNext')),
               (3, 0.5, ('sel', '#bNext')), (3, 6.6, ('sel', '#m1000'))],
      points=[('第四種黑盒子', '輸出等於一減輸入'), ('問完黑盒子', '輸入位元的箭頭翻面'), ('量測一千次', '全部是一，平衡')], shot=(3, 9.6)),
 dict(key='blind', after=9, page='tr', hash='deutsch-lab', scene='transmon 3D 第 7 章：振幅長條——自由實驗（隨機隱藏的黑盒子）',
      title='動畫展示：盲測一回合', sub='三維動畫：隨機隱藏的黑盒子，只問一次',
      sentences=[
       '回到超導晶片動畫的自由實驗玩一回盲測：按隨機隱藏，左上角的字幕說，已經偷偷選好一個黑盒子。',
       '先猜猜看是常數還是平衡，再按一鍵德意志：電路依序送出翻轉閘、兩個哈達瑪閘、問一次寫著問號的黑盒子，再一個哈達瑪閘，最後量三十次。',
       '量完之後只看第一位：零代表常數、一代表平衡，字幕接著揭曉抽到的是哪一個黑盒子，判斷正確就打勾。',
       '不管抽到哪一種，黑盒子都只被問了一次；古典的做法，至少要分別問零和一兩次才能比較。'],
      actions=[(0, 0.3, _PIN), (0, 0.6, _CLEAR), (0, 4.0, ('sel', '[data-fn="hide"]')),
               (1, 3.6, ('id', 'g7deu'))],
      points=[('隨機隱藏', '黑盒子變成問號'), ('一鍵德意志', '只問一次'), ('字幕揭曉', '判斷正確打勾')], shot=(3, 5.0)),
]


class _Demos(list):
    """清單（demos.py 的載入方式：DEMOS[LESSON] = 本模組.DEMOS），同時也能用 DEMOS['Q107'] 取用。"""

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
