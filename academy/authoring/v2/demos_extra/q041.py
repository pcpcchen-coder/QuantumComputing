"""Q041 為什麼要 10 mK — v2 動畫展示段（格式見 ../demos.py 的說明）。

場景與控制項（皆已讀原始碼確認）：
- tr#readout：animations/transmon-3d.html 第 5 章「讀取」。步驟按鈕由 bindChapter(4) 動態建在 #g5steps（無 id），
  用 ('sel', '#g5steps button:nth-child(k)') 點；步驟 1 面板寫「h × 5.21 GHz ≈ 22 μeV（約相當於 0.25 K 的熱能）」，
  步驟 7 看板寫「稀釋冷凍機：全程維持 ~10 mK」「位元等效溫度常為 40–60 mK：靜置時仍有約 0.1–1% 在 |1⟩」。
- pe#cooldown：animations/js/peripherals/04_cooldown.js。按鈕「⏸ 暫停」、滑桿「時間 (小時)」（0–36）。
  TMODEL：t=0 全部 300 K；t=24 h 50 K 板 50 K；t=36 h 混合腔 10.2 mK、相位標籤「✓ 基溫穩定，可開始量測」。
- jj#fridge：animations/js/scenes/11_fridge.js。滑桿「動畫速度」、按鈕「放大混合腔」；
  readout 第二行「熱光子數 n_th = 1/(e^{hf/kT} − 1)：7 GHz 時 300 K ≈ 890，10 mK ≈ 10⁻¹⁵」。
"""

LESSON = 'Q041'


class _Demos(list):
    """清單（demos.py 的載入方式），同時也能用 DEMOS['Q041'] 取用。"""

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


_STEP = '#g5steps button:nth-child({})'

DEMOS = _Demos([
 dict(key='energy', after=4, page='tr', hash='readout', scene='transmon 3D 第 5 章：色散讀取',
      title='動畫展示：一份能量相當幾度', sub='三維動畫：超導量子位元的讀取章',
      sentences=[
       '打開超導量子位元的三維動畫，切到讀取這一章的第一步。',
       '右邊面板寫著，五點二一吉赫的量子位元，一個激發只有大約二十二微電子伏特，大約相當於零點二五克耳文的熱能。',
       '跳到第七步，中間圖表右上角的方框寫著：稀釋冷凍機全程維持大約十毫克耳文，重新降溫一次要好幾天。',
       '看板最下面一行還提醒，量子位元自己的等效溫度常常是四十到六十毫克耳文，所以靜置時仍有大約千分之一到百分之一停在一。'],
      actions=[(0, 0.1, ('id', 'g5auto')), (0, 0.3, ('sel', _STEP.format(1))), (2, 0.3, ('sel', _STEP.format(7)))],
      points=[('五點二一吉赫', '約零點二五克耳文'), ('冷凍機', '全程約十毫克耳文'), ('等效溫度', '仍有少量停在一')], shot=(3, 2.0)),
 dict(key='cooldown', after=7, page='pe', hash='cooldown', scene='周邊系統 3D 場景 4：降溫流程',
      title='動畫展示：一層一層降到十毫克耳文', sub='三維動畫：稀釋冷凍機的降溫流程',
      sentences=[
       '打開周邊系統動畫的降溫流程場景，先暫停，把時間拉回零，右邊金色的數字顯示每一層都是三百克耳文。',
       '往後拖動時間，脈衝管預冷開始，五十克耳文那層降到五十克耳文左右，下面幾層也一路掉到二、三十克耳文。',
       '繼續往後拉，混合氣凝結、稀釋循環啟動，最下面三層在幾個小時內陡降，混合腔停在十點二毫克耳文，上方顯示基溫穩定。',
       '從頂板的三百克耳文到混合腔的十毫克耳文，差了大約三萬倍，插圖裡對數座標的六條曲線一層比一層低，最下面三條在最後幾個小時陡降。'],
      actions=[(0, 4.4, ('click', '⏸')), (0, 6.2, ('slider', '時間', 0)),
               (1, 0.6, ('sweep', '時間', 0, 24, 8.0)),
               (2, 1.0, ('sweep', '時間', 24, 36, 10.0))],
      points=[('起點', '每一層三百克耳文'), ('脈衝管預冷', '上面兩層先降'), ('稀釋循環', '混合腔約十毫克耳文')], shot=(3, 2.0)),
 dict(key='photons', after=8, page='jj', hash='fridge', scene='JJ 與微波讀取 3D 場景 11：低溫讀取鏈',
      title='動畫展示：熱光子被壓到幾乎沒有', sub='三維動畫：稀釋冷凍機中的微波讀取鏈',
      sentences=[
       '換到微波讀取動畫的低溫讀取鏈場景，冷凍機一樣分成六層，最下面金色字的混合腔，大約十毫克耳文。',
       '往下送的輸入線上，四克耳文、冷板和混合腔各有一個衰減器，標籤都寫著負二十分貝，把室溫帶下來的熱雜訊一層一層壓低。',
       '控制面板的說明一直寫著：七吉赫的微波，在室溫平均有大約八百九十個熱光子，到了十毫克耳文，只剩十的負十五次方個。',
       '只有底層夠冷，讀取腔裡才幾乎沒有熱光子；按下放大混合腔，就能近看裝著量子晶片的樣品盒。'],
      actions=[(0, 0.5, ('slider', '動畫速度', 1.5)), (3, 4.2, ('click', '放大混合腔'))],
      points=[('衰減器', '一層一層壓低熱雜訊'), ('室溫', '約八百九十個熱光子'), ('十毫克耳文', '只剩十的負十五次方')], shot=(2, 3.0)),
])
