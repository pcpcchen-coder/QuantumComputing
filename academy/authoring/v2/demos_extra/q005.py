"""Q005 相位：看不見卻最重要 — v2 動畫展示段。

格式同 demos.py。場景程式：
- animations/js/operation/01_qubit.js（#qubit：按鈕「|+⟩」「清除統計」「一次跑 1000 shots」；滑桿「φ（相位）」只改相位、不改理論機率）
- animations/js/operation/02_gates.js（#gates：按鈕 H、Z、S、「重設 |0⟩」「示範：H → Z → H = X」；
  180° 的閘約 1.3 秒、90° 的閘約 0.9 秒轉完，連按會排隊依序執行；
  錄影時 swiftshader 每秒格數低、dt 上限 0.05 秒，實際約慢 4–5 倍，所以先把「動畫速度」調到 3×）
"""

LESSON = 'Q005'

_LIST = [
 dict(key='hidden', after=3, page='op', hash='qubit', scene='3D 場景 1：量子位元的狀態與測量',
      title='動畫展示：相位轉了，測量看不出來', sub='三維動畫：量子位元的狀態與測量',
      sentences=[
       '打開量子位元場景，先按加號那一顆，把箭頭放到赤道，再一次跑一千次測量。',
       '零和一大約各五百次；接著把相位滑桿拖到一百八十度，箭頭轉到赤道的另一邊。',
       '清除統計再跑一千次，結果還是各五百次左右，直接測量完全看不出相位轉過了。'],
      actions=[(0, 0.5, ('click', '|+⟩')), (0, 5.6, ('click', '一次跑 1000 shots')),
               (1, 3.4, ('sweep', 'φ（相位）', 0, 180, 3.5)),
               (2, 0.3, ('click', '清除統計')), (2, 1.6, ('click', '一次跑 1000 shots'))],
      points=[('箭頭在赤道', '零和一各約五百次'), ('相位轉半圈', '箭頭到另一邊'), ('再跑一千次', '還是各約五百次')], shot=(2, 5.0)),
 dict(key='blindtest', after=6, page='op', hash='gates', scene='3D 場景 2：單位元量子閘',
      title='動畫展示：盲測的兩種答案', sub='三維動畫：單位元量子閘',
      sentences=[
       '換到單位元閘場景，按重設回到北極，再按哈達瑪閘，箭頭躺到赤道上。',
       '假設爸爸沒有加相位翻轉，再按一次哈達瑪閘，箭頭轉回北極，得到零的機率是百分之百。',
       '再試一次有加的情況：哈達瑪、相位翻轉、哈達瑪，箭頭最後停在南極，一定得到一。'],
      actions=[(0, 0.1, ('slider', '動畫速度', 3)), (0, 1.5, ('click', '重設 |0⟩')), (0, 3.5, ('click', 'H')),
               (1, 3.0, ('click', 'H')),
               (2, 0.2, ('click', '示範：H → Z → H = X'))],
      points=[('沒加相位翻轉', '回到北極，得到零'), ('加了相位翻轉', '停在南極，得到一'), ('哈達瑪閘', '把相位差轉出來')], shot=(2, 7.8)),
 dict(key='twostep', after=10, page='op', hash='gates', scene='3D 場景 2：單位元量子閘',
      title='動畫展示：兩步的關卡', sub='三維動畫：單位元量子閘',
      sentences=[
       '再看兩步的關卡：重設之後按哈達瑪，接著只按一次四分之一圈的相位閘，再按哈達瑪。',
       '箭頭停在赤道上，讀數顯示零和一各佔一半，偵探沒辦法確定爸爸做了什麼。',
       '重設再來一次，這回連按兩次四分之一圈的相位閘，最後的哈達瑪把箭頭送到南極。',
       '兩個四分之一圈合起來，效果就和一個相位翻轉閘一樣。'],
      actions=[(0, 0.1, ('slider', '動畫速度', 3)), (0, 1.0, ('click', '重設 |0⟩')), (0, 2.0, ('click', 'H')),
               (0, 4.5, ('click', 'S')), (0, 6.3, ('click', 'H')),
               (2, 0.3, ('click', '重設 |0⟩')), (2, 0.5, ('click', 'H')), (2, 2.4, ('click', 'S')),
               (2, 3.4, ('click', 'S')), (2, 4.6, ('click', 'H'))],
      points=[('只加一步', '零和一各一半'), ('加滿兩步', '相位差半圈'), ('最後的哈達瑪', '一定得到一')], shot=(3, 3.0)),
]


class _Demos(list):
    """清單（demos.py 的載入方式：DEMOS[LESSON] = 本模組.DEMOS），同時也能用 DEMOS['Q005'] 取用。"""

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
