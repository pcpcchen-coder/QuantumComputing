"""量子電腦學程每集共用的建置程式（Q002 起使用；Q001 的 prepare_content.py 是同樣做法的展開版）。

各集的 authoring/qxxx/prepare_content.py 只放該集文字，呼叫 build()。這裡負責：
- 指向父子科技學院可攜流程的 special_builder（XINEW_ACADEMY 環境變數）
- 核對課綱 lesson.json 的主題
- 固定的揭露字樣、結尾句、渲染選項、TTS 授權說明
- 建置後把 manifest 的副標與頁首改成量子電腦學程
"""
from pathlib import Path
import json
import os
import sys

XINEW = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
sys.path.insert(0, str(XINEW / 'authoring'))
import special_builder  # noqa: E402

QREPO = Path(__file__).resolve().parents[2]
DISCLOSURE = '依課綱製作的課前教學版'
CN = '零一二三四五六七八九'


def ordinal(n):
    if n >= 100:  # Q100 起：一百、一百零一、一百一十、一百二十三
        h, r = divmod(n, 100)
        if r == 0:
            return CN[h] + '百'
        return CN[h] + '百' + ('零' + CN[r] if r < 10 else ('一' + ordinal(r) if r < 20 else ordinal(r)))
    if n < 10:
        return CN[n]
    if n >= 100:
        h, r = divmod(n, 100)
        if r == 0:
            return CN[h] + '百'
        return CN[h] + '百' + ('零' + CN[r] if r < 10 else ('一' + ordinal(r) if r < 20 else ordinal(r)))
    t, o = divmod(n, 10)
    return (CN[t] if t > 1 else '') + '十' + (CN[o] if o else '')


def readme(lesson, title):
    return (f'# 父子科技學院 量子電腦學程 {lesson}\n\n依量子電腦學程課綱製作的課前教學版，主題「{title}」。\n'
            '製作流程借用父子科技學院的可攜流程（特別篇路線）；來源、旁白、PPTX、教材與 QC 都留在本集資料夾，先讀 `production/START_HERE.md`。\n'
            '大型成品（MP4、交付 ZIP）不進 Git；檔名、大小、SHA-256 與取得方式見 `delivery.json`，檢視方法與限制見 `qc/manual-review.md`。\n'
            '不含課堂私人錄音，也沒有偽造逐字稿。YouTube 由使用者自行上傳。\n')


def build(*, here, lesson, slug, title, topic, header_en, checked, src, source_records, scenes, visible, board,
          source_method, not_verified, tts_date):
    here = Path(here)
    rec = json.loads((QREPO / f'academy/lessons/{lesson}/lesson.json').read_text(encoding='utf-8'))
    assert rec['sourceRow']['課程主題'] == topic, (rec['sourceRow']['課程主題'], topic)
    n = int(lesson[1:])
    docs = {name: (here / name).read_text(encoding='utf-8')
            for name in ('fact-check.md', 'plan.md', 'delivery-summary.md', 'source-notes.md')}
    E = special_builder.build(
        special=lesson, slug=slug, title=title, header_en=header_en, cover_disclosure=DISCLOSURE,
        first_sentence_needles=(DISCLOSURE, '並非實際上課錄音'), summary_prefix='這是依課綱製作的課前教學版，不是實際上課錄音',
        checked=checked, src=src, scenes=scenes, visible=visible, board=board,
        render_options={'asianLatinAutoSpace': False, 'captionLineBreak': 'kinsoku'},
        tts_basis=f'On {tts_date} the user asked to produce quantum track lessons (this one: {lesson}) with the academy opening and voice; '
                  'the public narration script goes to Edge TTS on the same basis as Q001.',
        source_records=source_records, source_method=source_method, not_verified=not_verified,
        documents=docs, readme=readme(lesson, title), content_mode='curriculum-based-preclass',
        delivery_label='量子電腦學程・依課綱製作的課前教學版（無課堂錄音）',
        classroom_note=f'classroom.zip 是 {lesson} 的課堂教材。課堂 120 分鐘與影片片長分開。')
    m = json.loads((E / 'production/manifest.json').read_text(encoding='utf-8'))
    m['subtitle'] = f'父子科技學院 量子電腦學程 第{ordinal(n)}堂｜{DISCLOSURE}'
    m['seriesHeader'] = f'父子科技學院 量子電腦學程  ·  {header_en}'
    m['program'] = {'name': '量子電腦學程', 'lessonId': lesson, 'repo': 'pcpcchen-coder/QuantumComputing',
                    'lessonRecord': f'academy/lessons/{lesson}/lesson.json'}
    (E / 'production/manifest.json').write_text(json.dumps(m, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('episode:', E)
    return E
