"""Q131 冷卻鏈不斷電與壓縮機驅動 — v2 動畫展示段（格式見 ../demos.py 的說明）。

power1000.html（pw）是 SVG 頁面，控制項是 .ctl 滑桿／select 與 label.tog 勾選框，不是 operation.html 的按鈕，
所以用 ('js', ...) 操作；下面的小函式產生那段程式碼。
"""
import json

LESSON = 'Q131'


def _pw_tog(label, on):
    return ('js', "(()=>{const l=[...document.querySelectorAll('#controls label.tog')].find(x=>x.textContent.includes(%s));"
                  "const i=l.querySelector('input');window.__flash(l);if(i.checked!==%s){i.checked=%s;i.dispatchEvent(new Event('change'));}})()"
            % (json.dumps(label), 'true' if on else 'false', 'true' if on else 'false'))


def _pw_sel(label, value):
    return ('js', "(()=>{const d=[...document.querySelectorAll('#controls .ctl')].find(x=>x.querySelector('label').textContent.includes(%s));"
                  "const s=d.querySelector('select');window.__flash(d);s.value=%s;s.dispatchEvent(new Event('change'));})()"
            % (json.dumps(label), json.dumps(value)))


def _pw_pp(n):  # 點全景場景的紅色痛點 n
    return ('js', "(()=>{const g=[...document.querySelectorAll('#svg g.pp')].find(x=>x.textContent.trim()===%s);"
                  "g.dispatchEvent(new MouseEvent('click',{bubbles:true}));window.__flash(document.getElementById('metrics'));})()" % json.dumps(str(n)))


_LIST = [
 dict(key='pulsetube', after=4, page='pe', hash='pulsetube', scene='周邊系統 3D 場景 2：脈衝管冷卻器＋氦壓縮機',
      title='動畫展示：冷卻鏈的第一棒', sub='三維動畫：脈衝管冷卻器與氦壓縮機',
      sentences=[
       '打開周邊系統動畫的脈衝管場景，左邊的箱子是氦氣壓縮機，標籤寫著電力大約十千瓦，而且要水冷。',
       '紅色管子把高壓氦氣送上冷頭，藍色管子把低壓氦氣送回壓縮機，冷頭上的旋轉閥負責切換高壓和低壓。',
       '右下角的小圖是冷頭裡的壓力，一高一低來回跳；壓縮機旁邊的冷卻水一進一出，把壓縮機的熱帶走。'],
      actions=[],
      points=[('氦壓縮機', '約十千瓦、要水冷'), ('旋轉閥', '高壓低壓來回切換'), ('冷卻水', '帶走壓縮機的熱')], shot=(1, 3.0)),
 dict(key='outage', pmap=[None, 0, 1, 2], after=5, page='pw', hash='outage', scene='1,000 位元供電互動動畫 場景 5：斷電時間軸',
      title='動畫展示：三種備援方案', sub='互動動畫：斷電時間軸',
      sentences=[
       '換到供電互動動畫的斷電時間軸，橫軸從一秒到十天，用的是對數刻度，曲線是混合腔的溫度。',
       '先看方案甲，只有控制電子接不斷電系統：白點走到兩分鐘附近，曲線就衝過紅色的一克耳文虛線，之後要好幾天才降回來。',
       '改選方案乙，冷卻鏈接不斷電系統，再由發電機接手，整條曲線平平地貼在十毫克耳文。',
       '方案丙是發電機沒起來，不斷電系統撐了十五分鐘就耗盡，曲線晚一點還是衝上去了。'],
      actions=[(1, 0.3, _pw_sel('備援方案', 'none')), (2, 0.4, _pw_sel('備援方案', 'full')), (3, 0.4, _pw_sel('備援方案', 'gen'))],
      points=[('方案甲', '兩分鐘衝過一克耳文'), ('方案乙', '溫度不動'), ('方案丙', '撐完十五分鐘才升溫')], shot=(1, 6.5)),
 dict(key='overview', pmap=[0, 1, 2, 2], after=7, page='pw', hash='overview', scene='1,000 位元供電互動動畫 場景 1：全景',
      title='動畫展示：分層保護的全景', sub='互動動畫：電從哪裡來、到哪裡去',
      sentences=[
       '最後看全景：電從左邊的中壓進線進來，經過分層不斷電系統，分成機電、乾淨、運算三條匯流排，粒子越密代表功率越大。',
       '勾選模擬斷電，進線的粒子停了，三條匯流排靠不斷電系統繼續流，右邊混合腔還是十毫克耳文。',
       '再取消冷卻鏈接不斷電系統，機電那一條停下來，混合腔溫度很快從綠色變黃、再變紅。',
       '點一號紅點，說明寫著：不斷電系統要為壓縮機這群馬達設計，因為它們的啟動電流決定了容量級距。'],
      actions=[(1, 0.3, _pw_tog('模擬斷電', True)), (2, 0.5, _pw_tog('冷卻鏈接 UPS', False)), (3, 0.2, _pw_pp(1))],
      points=[('三條匯流排', '機電、乾淨、運算'), ('模擬斷電', '靠不斷電系統繼續流'), ('冷卻鏈沒保護', '混合腔快速升溫')], shot=(2, 6.0)),
]


class _Demos(list):
    def __getitem__(self, k):
        return list(self) if k == LESSON else super().__getitem__(k)


DEMOS = _Demos(_LIST)
