"""Q102 頻率配置與頻率碰撞 — v2 動畫展示段（格式見 ../demos.py 的說明）。

三段都在 transmon-3d.html#case（第 6 章 案例）的「⑥ 自由實驗」裡操作：
自由實驗的控制項全由我們按，不靠章節自動播放的時間軸（錄影幀率偏低時，自動時間軸會比牆鐘慢）。
進入自由實驗後，面板內容比視窗高；用 js 每半秒把面板捲到底，讓滑桿、按鈕、Q1–Q3 數值與碰撞清單同時入鏡。
"""

LESSON = 'Q102'

# 進入第 6 步「自由實驗」（步驟按鈕由程式動態產生，沒有 id）
_FREE = ('sel', '#c6steps button:nth-child(6)')
# 面板捲到底並保持（碰撞清單行數變動時也不會被切掉）
_PIN = ('js', "(()=>{const pn=document.getElementById('panel');const f=()=>{pn.scrollTop=pn.scrollHeight;};f();"
              "clearInterval(window.__pin);window.__pin=setInterval(f,500);})()")


def _set_phi(k, v):
    """把 Q(k+1) 的 Φ 滑桿設成 v（觸發 input，與手動拖動相同）。"""
    return ('js', f"(()=>{{const s=document.getElementById('c6phi{k}');s.value={v};"
                  f"s.dispatchEvent(new Event('input'));window.__flash(s.closest('label'));}})()")


def _sweep_phi(k, a, b, ms):
    """在頁面裡用計時器把 Q(k+1) 的 Φ 滑桿從 a 慢慢拖到 b（ms 毫秒）。"""
    return ('js', f"(()=>{{const s=document.getElementById('c6phi{k}'),l=s.closest('label'),t0=performance.now();"
                  f"l.classList.add('qflash');const id=setInterval(()=>{{const u=Math.min(1,(performance.now()-t0)/{ms});"
                  f"s.value=({a}+({b}-{a})*u).toFixed(3);s.dispatchEvent(new Event('input'));"
                  f"if(u>=1){{clearInterval(id);l.classList.remove('qflash');}}}},80);}})()")


_LIST = [
 dict(key='hidden', after=4, page='tr', hash='case', scene='transmon 3D 第 6 章：案例——自由實驗（隱藏的頻率線）',
      title='動畫展示：撞上隱藏的頻率', sub='三維動畫：二號的一到二與雙光子',
      sentences=[
       '打開超導晶片動畫的案例章，進入第六步自由實驗，三顆位元先停在配置好的位置，面板顯示無碰撞。',
       '看二號的金色記號：高的實線是零到一，往左最遠那條淡淡的細線是一到二，兩者中間的金色菱形是雙光子。',
       '把一號的磁通調小，青色實線往右移到四點九六，正好碰上二號的菱形，一號和二號外圍亮起紅圈，面板寫著一號驅動撞上二號的雙光子。',
       '再把磁通加大，青色線離開菱形一路往左，停在四點八二，碰上二號那條淡淡的細線，紅圈又亮起來，這是零到一撞一到二。'],
      actions=[(0, 0.3, _FREE), (0, 0.6, _PIN),
               (2, 1.2, _set_phi(0, 0.110)), (3, 1.0, _set_phi(0, 0.150))],
      points=[('二號的三條線', '實線、細線、菱形'), ('碰上菱形', '雙光子碰撞'), ('碰上細線', '零到一撞一到二')], shot=(3, 8.0)),
 dict(key='address', after=5, page='tr', hash='case', scene='transmon 3D 第 6 章：案例——自由實驗（禁區與棋盤格）',
      title='動畫展示：禁區和旁觀者', sub='三維動畫：二號鄰居的禁區與棋盤格',
      sentences=[
       '再開一次自由實驗，這時三顆已經在配置好的位置；勾選顯示二號鄰居的禁區，頻率尺上多出五條淡紅色的帶子。',
       '由左到右依序是一到二、雙光子、同頻、雙光子、一到二，一號和三號的實線都落在禁區外面。',
       '現在用滑桿把三號的磁通拉大，讓它也降到四點九，和一號一樣，排成棋盤格；兩顆都沒踩進禁區，紅字卻寫著旁觀者碰撞。',
       '按回到配置，三號回到五點三，紅字變成青色的無碰撞，三顆位元又各有自己的地址。'],
      actions=[(0, 0.3, _FREE), (0, 0.6, _PIN), (0, 7.0, ('id', 'c6zones')),
               (2, 1.5, _set_phi(2, 0.186)), (3, 0.5, ('id', 'c6alloc'))],
      points=[('五條禁區', '二號的鄰居不能去'), ('棋盤格', '旁觀者碰撞'), ('回到配置', '各有地址')], shot=(2, 10.5)),
 dict(key='hunt', after=7, page='tr', hash='case', scene='transmon 3D 第 6 章：案例——自由實驗（找第二個空位）',
      title='動畫展示：找第二個空位', sub='三維動畫：慢慢移動三號的頻率',
      sentences=[
       '最後來找第二個空位：一樣進入自由實驗，準備用滑桿把三號的頻率慢慢往下拉。',
       '三號從五點三往下走，紅圈和面板的紅字一個接一個冒出又消失：先是三號的雙光子撞上二號，再來三號的一到二撞上一號，接著和二號同頻。',
       '停在五點零的時候，紅圈全部熄滅，面板又出現無碰撞，這是三號的第二個空位，和小程式算出來的一樣。',
       '按送給二號的派脈衝驗收：只有中間的二號亮起來，兩邊的激發機率都還是零。'],
      actions=[(0, 0.3, _FREE), (0, 0.6, _PIN), (1, 0.5, _sweep_phi(2, 0.080, 0.166, 12000)),
               (3, 0.8, ('sel', '[data-pi="1"]'))],
      points=[('往下拉三號', '碰撞輪流出現'), ('五點零', '第二個空位'), ('打二號', '只有二號亮')], shot=(3, 5.0)),
]


class _Demos(list):
    """清單（demos.py 的載入方式：DEMOS[LESSON] = 本模組.DEMOS），同時也能用 DEMOS['Q102'] 取用。"""

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
