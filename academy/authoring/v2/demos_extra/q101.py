"""Q101 迷思修正：Z 線不是把位元調成一樣 — v2 動畫展示段（格式見 ../demos.py 的說明）。

三段都用 transmon-3d.html 第 6 章（#case）。該章的步驟 1–5 依頁面內部時間軸播放，錄影機負載高時會變慢
（實測約 12–18 fps，dt 上限 0.05 s，時間軸約為實際時間的 0.6–0.9 倍），所以旁白不依賴內部時間軸的字幕或自動脈衝：
需要「發生某件事」的地方一律改成在步驟 6（自由實驗）直接按按鈕或設定滑桿，立即生效。
"""

LESSON = 'Q101'

_STEP1 = '#c6steps button:nth-child(1)'
_STEP6 = '#c6steps button:nth-child(6)'


def _q1(v):
    """設定自由實驗 Q1 的 Φ 滑桿（#c6phi0，範圍 0–0.3 Φ₀）並觸發 input，外框閃一下。"""
    return ("(()=>{const s=document.getElementById('c6phi0');s.value=%s;"
            "s.dispatchEvent(new Event('input'));window.__flash(s.closest('label'));})()" % v)


_LIST = [
 dict(key='squid', after=4, page='tr', hash='case', scene='transmon 3D 第 6 章：案例——自由實驗',
      title='動畫展示：磁通線只能往下調', sub='三維動畫：三顆可調超導量子位元的頻率',
      sentences=[
       '打開晶片動畫的案例章，進入自由實驗，按回到製程原貌，三顆的磁通都歸零，左邊小圖上的點都疊在曲線最高點。',
       '現在把第一顆的磁通慢慢加大，它的點沿著曲線往下滑，頻率尺上的青色線也往左移，頻率一路往下掉。',
       '第一顆移開之後，它身上的紅圈消失了，只剩第二、三顆之間還有碰撞；離開最高點，青色線還會微微抖動，代表磁通雜訊開始有影響。',
       '把滑桿拉回零，青色線回到最高點，再也上不去，所以磁通線只能把頻率往下調。'],
      actions=[(0, 2.6, ('sel', _STEP6)), (0, 4.8, ('id', 'c6raw')),
               (1, 0.6, ('js', _q1(0.04))), (1, 1.4, ('js', _q1(0.08))), (1, 2.2, ('js', _q1(0.12))),
               (1, 3.0, ('js', _q1(0.16))), (1, 3.8, ('js', _q1(0.2))),
               (3, 0.6, ('js', _q1(0)))],
      points=[('磁通歸零', '三顆都在最高點'), ('加大磁通', '頻率往下掉'), ('拉回零', '再也上不去')], shot=(2, 3.0)),
 dict(key='crosstalk', after=6, page='tr', hash='case', scene='transmon 3D 第 6 章：案例——製程誤差與串擾',
      title='動畫展示：頻率太近就串擾', sub='三維動畫：製程誤差讓頻率擠在一起',
      sentences=[
       '回到案例章的第一步：三顆可調的超導量子位元排成一列，剛做好的時候，磁通都是零。',
       '看上方的頻率尺，第一顆和第二顆的線幾乎疊在一起，被紅色帶子罩住，三顆外面也都亮起紅圈，右邊面板寫著碰撞三處。',
       '接著換到自由實驗，按回到製程原貌，只對第一顆送一道翻轉脈衝。',
       '第一顆亮起青光，可是隔壁的第二顆也跟著微微發亮，頻率太近，脈衝分不清目標，這就是串擾。'],
      actions=[(0, 0.1, ('id', 'c6auto')), (0, 0.3, ('sel', _STEP1)), (1, 0.2, ('id', 'c6play')),
               (2, 1.6, ('sel', _STEP6)), (2, 1.8, ('id', 'c6raw')), (2, 5.0, ('sel', '[data-pi="0"]'))],
      points=[('製程原貌', '第一、二顆擠在一起'), ('紅色帶子', '代表碰撞'), ('只打第一顆', '第二顆也被激發')], shot=(3, 1.5)),
 dict(key='coupling', after=7, page='tr', hash='case', scene='transmon 3D 第 6 章：案例——自由實驗',
      title='動畫展示：調開，需要時才對上', sub='三維動畫：頻率配置與受控相位翻轉閘',
      sentences=[
       '最後一段，在自由實驗先按回到製程原貌，第一、二顆擠在一起，紅色帶子和紅圈都冒出來。',
       '再按回到配置，三顆各自搬到相隔大約兩億赫茲的位置，紅色全部消失，這就是頻率配置。',
       '想讓第二顆和第三顆合作，就按受控相位翻轉閘，第三顆被短暫往上推，兩顆中間的耦合電容亮起青光，紅圈也刻意亮起來。',
       '幾秒後第三顆回到原本的位置，青光熄滅，耦合又關上；右邊面板的相位累積到一百八十度，閘就完成了。'],
      actions=[(0, 1.8, ('sel', _STEP6)), (0, 3.8, ('id', 'c6raw')),
               (1, 0.4, ('id', 'c6alloc')), (2, 2.4, ('id', 'c6cz'))],
      points=[('製程原貌', '紅色碰撞帶'), ('回到配置', '各有地址、零碰撞'), ('受控相位翻轉閘', '短暫對上再分開')], shot=(2, 5.0)),
]


class _Demos(list):
    """清單（demos.py 的載入方式：DEMOS[LESSON] = 本模組.DEMOS），同時也能用 DEMOS['Q101'] 取用。"""

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
