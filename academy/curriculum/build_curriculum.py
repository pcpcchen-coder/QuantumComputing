"""由 lessons_data.py 產生量子電腦學程的課綱檔案。

    python3 academy/curriculum/build_curriculum.py

輸出（全部可重複產生，不要手改）：
  academy/curriculum/catalog.json        96 堂完整欄位（欄位名稱同父子科技學院 V2 課表）
  academy/lessons/Qxxx/lesson.json       每堂一份
  academy/lessons/Qxxx/brief.md          每堂的 120 分鐘教案摘要
  academy/CURRICULUM_INDEX.md            96 堂索引
  academy/curriculum/production-status.json、academy/PRODUCTION_STATUS.md
    狀態表：既有狀態會保留，只補上新課次
"""
from pathlib import Path
from urllib.parse import quote_plus
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
ACADEMY = HERE.parent
REPO = ACADEMY.parent
sys.path.insert(0, str(HERE))
from lessons_data import DECKS, L, MODULES, SCENE_PAGES  # noqa: E402

CN = '零一二三四五六七八九'
FLOW_MINUTES = '10／15／40／10／30／10／5'


def ordinal(n):
    """1 → 一、16 → 十六、96 → 九十六。"""
    if n < 10:
        return CN[n]
    t, o = divmod(n, 10)
    return (CN[t] if t > 1 else '') + '十' + (CN[o] if o else '')


def scene_link(code, depth):
    page, _, scene = code.partition(':')
    path = SCENE_PAGES['t3d' if page == 't3d' else page]
    return ('../' * depth) + path + (f'#{scene}' if scene else '')


def deck_text(ref):
    key, _, pages = ref.partition(' ')
    return f'{DECKS[key][1]}（{DECKS[key][0]}）{pages}'


def flow(row):
    return '\n'.join([
        f'00–10 任務開場：{row["t"]}',
        f'10–25 概念示範：{row["g"]}',
        f'25–65 父子共同實作：{row["task"]}',
        '65–75 休息／走動／聊天',
        f'75–105 孩子獨立改造：{row["mod"]}',
        '105–115 角色互換：孩子教爸爸操作與原理',
        '115–120 錄音總結、作品命名、版本存檔',
    ])


def search(row, n):
    words = {
        1: f'{row["t"]} quantum computing explained beginner',
        2: f'{row["t"]} {row["g"][:20]} hands on demo',
        3: f'{row["t"]} quantum computing lecture visualization',
    }[n]
    return words, 'https://www.youtube.com/results?search_query=' + quote_plus(words)


def build():
    lessons = []
    for idx, row in enumerate(L, 1):
        lid = f'Q{idx:03d}'
        m_idx = (idx - 1) // 16
        mid, mname, stage, audience = MODULES[m_idx]
        accept = (f'完成「{row["work"]}」；能不用看稿說出核心原理；'
                  f'能指出至少一個錯誤、限制或注意事項（例如：{row["safe"]}）。')
        record_q = (f'請孩子回答：1. {row["t"]}在解決什麼？2. 我怎麼做？'
                    '3. 哪裡容易錯？4. 生活中或真實的量子電腦哪裡會用到？')
        source = {
            '總課次': idx, '學程': '量子電腦學程', '階段': stage, '模組': f'{mid} {mname}',
            '模組內課次': (idx - 1) % 16 + 1, '課程主題': row['t'], '對象與上課方式': audience,
            '學習目標': row['g'], '2 小時課程流程': flow(row), '動手任務': row['task'],
            '孩子獨立改造': row['mod'], '好玩機制': row['fun'], '作品／交付': row['work'],
            '生活技能支線': row['life'], '家長課前準備': row['prep'],
            '課後延伸': '15–30 分鐘自由改造；寫三句學習日誌：我做了什麼、哪裡卡住、下次想加什麼。',
            '驗收標準': accept, '常見誤解與安全提醒': row['safe'], '錄音重點': record_q,
            '建議 YouTube 標題': f'父子科技課 量子電腦學程 #{lid}｜{row["t"]}',
            '難度 1–5': row['d'],
            '沿用簡報頁': [deck_text(x) for x in row['deck']],
            '沿用 3D 場景': row['scn'],
            '需新增素材': row['new'],
        }
        for n in (1, 2, 3):
            words, url = search(row, n)
            source[f'YouTube 關鍵字 {n}'] = words
            source[f'YouTube 連結 {n}'] = url
            source[f'影片用途 {n}'] = {1: '課前暖身', 2: '課中實作參考', 3: '課後延伸'}[n]
        lessons.append({'lessonId': lid, 'sourceRow': source})

    catalog = {
        'schemaVersion': 1,
        'source': 'academy/curriculum/lessons_data.py（由 build_curriculum.py 產生，不要手改）',
        'program': '父子科技學院 量子電腦學程',
        'lessonCount': len(lessons),
        'modules': [{'id': m[0], 'name': m[1], 'stage': m[2], 'audience': m[3],
                     'lessons': f'Q{i * 16 + 1:03d}–Q{i * 16 + 16:03d}'} for i, m in enumerate(MODULES)],
        'classMinutes': FLOW_MINUTES,
        'youtubeSearchNote': '每堂三組 YouTube 連結是動態搜尋入口，尚未挑選或觀看任何影片。',
        'lessons': lessons,
    }
    text = json.dumps(catalog, ensure_ascii=False, indent=2) + '\n'
    (HERE / 'catalog.json').write_text(text, encoding='utf-8')
    sha = hashlib.sha256(text.encode('utf-8')).hexdigest()

    status_path = HERE / 'production-status.json'
    status = json.loads(status_path.read_text(encoding='utf-8')) if status_path.exists() else {'schemaVersion': 1, 'lessons': {}}
    for les in lessons:
        status['lessons'].setdefault(les['lessonId'], {'status': 'planned', 'episodePath': None, 'evidence': None})
    status_path.write_text(json.dumps(status, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    for les in lessons:
        lid, s = les['lessonId'], les['sourceRow']
        d = ACADEMY / 'lessons' / lid
        d.mkdir(parents=True, exist_ok=True)
        st = status['lessons'][lid]
        (d / 'lesson.json').write_text(json.dumps({
            'lessonId': lid, 'sourceRow': s, 'curriculumSha256': sha,
            'episodePaths': ([st['episodePath']] if st.get('episodePath') else []) + ([st['v2']['episodePath']] if st.get('v2') else []),
            'minutes': 120, 'status': st['status']}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        reuse = [f'- 簡報：{x}' for x in s['沿用簡報頁']] + \
                [f'- 3D 場景：[`{c}`]({scene_link(c, 3)})' for c in s['沿用 3D 場景']]
        brief = [
            f'# {lid} {s["課程主題"]}', '',
            f'{s["模組"]}｜{s["階段"]}｜難度 {s["難度 1–5"]}／5｜好玩機制：{s["好玩機制"]}', '',
            f'**學習目標**：{s["學習目標"]}', '',
            '## 120 分鐘流程', '', '```', s['2 小時課程流程'], '```', '',
            '## 當堂作品', '', s['作品／交付'], '',
            '## 家長課前準備', '', s['家長課前準備'], '',
            '## 驗收', '', s['驗收標準'], '',
            '## 錄音提問', '', s['錄音重點'], '',
            '## 素材', '',
            *(reuse or ['- 沒有可直接沿用的現有頁面或場景。']),
            *[f'- 需新增：{x}' for x in s['需新增素材']], '',
            f'生活技能支線：{s["生活技能支線"]}。課後延伸：{s["課後延伸"]}', '',
            '課前教學影片與兩小時課堂分開管理；影片長度依實測旁白，不等於 120 分鐘。', '',
        ]
        (d / 'brief.md').write_text('\n'.join(brief), encoding='utf-8')

    idx = ['# 量子電腦學程課表索引', '',
           '父子科技學院的量子電腦學程，共 96 堂（6 模組 × 16 堂）。每堂 120 分鐘，'
           f'分段 {FLOW_MINUTES} 分鐘。詳細欄位見 `curriculum/catalog.json` 與 `lessons/Qxxx/brief.md`。', '']
    for i, m in enumerate(MODULES):
        idx += [f'## {m[0]} {m[1]}（Q{i * 16 + 1:03d}–Q{i * 16 + 16:03d}）', '',
                f'{m[2]}；{m[3]}。', '',
                '| 課次 | 主題 | 學習目標 | 好玩機制 | 作品 | 難度 |', '|---|---|---|---|---|---|']
        for les in lessons[i * 16:(i + 1) * 16]:
            s = les['sourceRow']
            idx.append(f'| [{les["lessonId"]}](lessons/{les["lessonId"]}/brief.md) | {s["課程主題"]} | {s["學習目標"]} '
                       f'| {s["好玩機制"]} | {s["作品／交付"]} | {s["難度 1–5"]} |')
        idx.append('')
    (ACADEMY / 'CURRICULUM_INDEX.md').write_text('\n'.join(idx), encoding='utf-8')

    label = {'planned': '規劃完成', 'verified': '已製作並驗收', 'awaiting_user_upload': '待使用者上傳'}
    rows = ['# 量子電腦學程製作狀態', '',
            '由 `curriculum/production-status.json` 產生。狀態：planned＝課綱完成、尚未製作；'
            'verified＝課前教學版已製作並通過驗收。YouTube 一律由使用者自己上傳。', '',
            '| 課次 | 主題 | 狀態 | 製作資料夾 |', '|---|---|---|---|']
    for les in lessons:
        st = status['lessons'][les['lessonId']]
        ep = f'`{st["episodePath"]}`' if st.get('episodePath') else '—'
        if st.get('v2'):
            ep += f'<br>v2 動畫展示版：`{st["v2"]["episodePath"]}`'
        state = label.get(st['status'], st['status'])
        if st.get('publication'):
            state += f'／{label.get(st["publication"], st["publication"])}'
        if st.get('v2'):
            state += '；v2 動畫展示版已製作並驗收'
        rows.append(f'| {les["lessonId"]} | {les["sourceRow"]["課程主題"]} | {state} | {ep} |')
    (ACADEMY / 'PRODUCTION_STATUS.md').write_text('\n'.join(rows) + '\n', encoding='utf-8')
    print(f'{len(lessons)} lessons; catalog sha256 {sha[:12]}')


if __name__ == '__main__':
    build()
