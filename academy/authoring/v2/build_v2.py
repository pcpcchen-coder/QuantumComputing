"""量子電腦學程 v2：在 v1 的 12 頁之間插入「動畫展示」段，產生新版影片與簡報。

    cd $XINEW_ACADEMY && .venv/bin/python ~/QuantumComputing/academy/authoring/v2/build_v2.py Q001 [audio|record|deck|assemble|all]

沿用 v1（父子科技學院可攜流程做的 specials/qxxx-*）已查核、已合成的 12 頁旁白與音訊；
新增段落的旁白用同一個 Edge TTS 合成函式、同一套暖聲處理與響度；影片規格同 v1（1080p30、0.55 秒淡化、
燒錄字幕樣式與 kinsoku 斷行、整體 −16 LUFS、無背景音樂）。輸出在 $XINEW_ACADEMY/specials/<v1 slug>-v2/。
"""
from pathlib import Path
import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
X = Path(os.environ.get('XINEW_ACADEMY', '/home/user/xinewvideogpt/academy')).resolve()
Q = HERE.parents[2]
sys.path.insert(0, str(HERE))
from demos import DEMOS, PAGES  # noqa: E402

LESSONS = {'Q001': 'q001-not-faster', 'Q002': 'q002-coin-and-arrow', 'Q003': 'q003-measure-and-shots',
           'Q004': 'q004-gates-rotate', 'Q005': 'q005-phase-hidden', 'Q006': 'q006-interference-waves',
           'Q007': 'q007-two-to-the-n', 'Q008': 'q008-entangled-dice', 'Q009': 'q009-circuit-score',
           'Q010': 'q010-first-program'}
# Q011 起不必改這裡：各課 authoring/qxxx/prepare_content.py 寫 LESSON, SLUG, ... = 'Qxxx', 'qxxx-slug', ... 就自動登記
import re as _re
for _pc in sorted(Path(__file__).resolve().parents[1].glob('q[0-9][0-9][0-9]/prepare_content.py')):
    _m = _re.search(r"LESSON, SLUG[^=]*=\s*'(Q\d{3})',\s*'([a-z0-9-]+)'", _pc.read_text(encoding='utf-8'))
    if _m:
        LESSONS.setdefault(_m.group(1), _m.group(2))
FPS, FADE = 30, 0.55
EMU = 12700  # per pt
PIC = (20, 72, 704, 396)            # pt：簡報上截圖／影片中錄影的位置
COL_X, COL_W = 740, 200             # pt：右欄
CARD_Y0, CARD_H, CARD_GAP = 190, 74, 84
OPENING = X / 'assets/opening/開場影片-v2.mp4'
STYLE = ("FontName=Noto Sans CJK TC,FontSize=16,Bold=1,PrimaryColour=&H00FFFFFF,"
         "OutlineColour=&H7A000000,BackColour=&H7A000000,BorderStyle=1,Outline=1.2,"
         "Shadow=0,Alignment=2,MarginV=20,MarginL=24,MarginR=24")


def run(cmd, **kw):
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True, **kw)
    if r.returncode:
        raise RuntimeError(' '.join(map(str, cmd[:4])) + '\n' + r.stderr[-2500:])
    return r.stdout.strip()


def dur(p):
    return float(run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=nw=1:nk=1', p]))


def srt_time(s):
    ms = max(0, round(s * 1000)); h, r = divmod(ms, 3600000); m, r = divmod(r, 60000); sec, r = divmod(r, 1000)
    return f'{h:02d}:{m:02d}:{sec:02d},{r:03d}'


def dump(p, d):
    Path(p).write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


class Lesson:
    def __init__(self, lid):
        self.lid, self.slug = lid, LESSONS[lid]
        self.v1 = X / 'specials' / self.slug
        self.name = self.slug + '-v2'
        self.E = X / 'specials' / self.name
        for d in ('production/presentation', 'assets/slides', 'assets/visuals', 'audio', 'subtitles', 'output', 'qc', 'work'):
            (self.E / d).mkdir(parents=True, exist_ok=True)
        self.demos = DEMOS[lid]
        self.v1timing = json.loads((self.v1 / 'production/timing.json').read_text(encoding='utf-8'))
        self.v1narr = json.loads((self.v1 / 'production/narration.json').read_text(encoding='utf-8'))
        self.v1man = json.loads((self.v1 / 'production/manifest.json').read_text(encoding='utf-8'))
        # 播出順序：('slide', n) 或 ('demo', key)
        self.order = []
        for n in range(1, 13):
            self.order.append(('slide', n))
            self.order += [('demo', d['key']) for d in self.demos if d['after'] == n]
        self.total = len(self.order)
        self.page_of = {item: i + 1 for i, item in enumerate(self.order)}

    def demo(self, key):
        return next(d for d in self.demos if d['key'] == key)

    # ── 1. 旁白 ────────────────────────────────────────────────
    def audio(self):
        sys.argv = [sys.argv[0], '--episode', f'specials/{self.slug}']
        sys.path.insert(0, str(X / 'pipeline/scripts'))
        import synthesize_narration as sn
        W = self.E / 'work'
        timing = {}
        for d in self.demos:
            files, sents, t = [], [], 0.0
            for i, s in enumerate(d['sentences']):
                raw = W / f"{d['key']}-{i + 1:02d}-raw.mp3"
                warm = W / f"{d['key']}-{i + 1:02d}.wav"
                if os.environ.get('QV2_DRY'):  # 試跑：用靜音代替，長度依字數估計；正式輸出前必須拿掉
                    run(['ffmpeg', '-y', '-v', 'error', '-f', 'lavfi', '-i', 'anullsrc=r=24000:cl=mono', '-t', f'{len(s) / 4.5:.2f}', raw.with_suffix('.dry.mp3')])
                    raw = raw.with_suffix('.dry.mp3')
                elif not raw.exists():
                    sn.synthesize(s, raw)
                run(['ffmpeg', '-y', '-v', 'error', '-i', raw, '-af',
                     'adelay=140,highpass=f=85,lowpass=f=8800,'
                     'equalizer=f=170:t=q:w=1:g=2.5,equalizer=f=2600:t=q:w=1.2:g=1.2,'
                     'aecho=0.8:0.35:28:0.035,acompressor=threshold=0.16:ratio=2.3:attack=18:release=180,'
                     'alimiter=limit=0.92,apad=pad_dur=0.34', '-ar', '44100', '-ac', '1', warm])
                dd = dur(warm)
                files.append(warm); sents.append({'text': s, 'start': t, 'end': t + dd - 0.18}); t += dd
            lst = W / f"{d['key']}.txt"; lst.write_text(''.join(f"file '{f}'\n" for f in files))
            out = self.E / 'audio' / f"demo_{d['key']}.mp3"
            run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-af', 'loudnorm=I=-18:TP=-2:LRA=7',
                 '-c:a', 'libmp3lame', '-b:a', '160k', out])
            timing[d['key']] = {'duration': dur(out), 'sentences': sents, 'audio': f"audio/demo_{d['key']}.mp3"}
            print(f"demo {d['key']}: {timing[d['key']]['duration']:.2f}s", flush=True)
        dump(self.E / 'production/demo-timing.json', timing)

    # ── 2. 錄影 ────────────────────────────────────────────────
    def record(self):
        timing = json.loads((self.E / 'production/demo-timing.json').read_text(encoding='utf-8'))
        for d in self.demos:
            tm = timing[d['key']]
            st = [s['start'] for s in tm['sentences']]
            acts = []
            for si, off, a in d['actions']:
                t = st[si] + off
                kind = a[0]
                if kind == 'click': acts.append({'t': t, 'kind': 'click', 'label': a[1]})
                elif kind == 'id': acts.append({'t': t, 'kind': 'id', 'id': a[1]})
                elif kind == 'slider': acts.append({'t': t, 'kind': 'slider', 'label': a[1], 'value': a[2]})
                elif kind == 'toggle': acts.append({'t': t, 'kind': 'toggle', 'label': a[1], 'value': a[2]})
                elif kind == 'sel': acts.append({'t': t, 'kind': 'sel', 'sel': a[1]})
                elif kind == 'js': acts.append({'t': t, 'kind': 'js', 'code': a[1]})
                elif kind == 'sweep': acts.append({'t': t, 'kind': 'sweep', 'label': a[1], 'from': a[2], 'to': a[3], 'secs': a[4]})
            page = Q / PAGES[d['page']][0]
            spec = {'url': page.as_uri() + '#' + d['hash'], 'duration': tm['duration'], 'actions': acts,
                    'shot_t': st[d['shot'][0]] + d['shot'][1], 'settle': d.get('settle', 2500 if d['page'] == 'op' else 4000),
                    'video_out': str(self.E / 'assets/visuals' / f"demo_{d['key']}.webm"),
                    'shot_out': str(self.E / 'assets/visuals' / f"demo_{d['key']}.png")}
            sp = self.E / 'work' / f"spec_{d['key']}.json"; dump(sp, spec)
            print(run(['node', HERE / 'record_demo.js', sp], cwd=str(HERE)), flush=True)

    # ── 3. 簡報 ────────────────────────────────────────────────
    def deck(self):
        from pptx import Presentation
        from pptx.util import Emu, Pt
        src = self.v1 / 'production/presentation' / f'{self.slug}.pptx'
        prs = Presentation(src)
        base = prs.slides[4]  # v1 第 5 頁：雙框比較版型，借它的頁首、頁尾、標題與卡片樣式
        sid = lambda n: next(s for s in base.shapes if s.shape_id == n)
        keep = [20, 2, 3, 4, 5, 6, 7, 8]
        lst = prs.slides._sldIdLst
        for d in sorted(self.demos, key=lambda d: -d['after']):
            new = prs.slides.add_slide(base.slide_layout)
            for sh in list(new.shapes):
                sh._element.getparent().remove(sh._element)
            cs = new._element.cSld
            if cs.bg is not None:
                cs.remove(cs.bg)
            cs.insert(0, copy.deepcopy(base._element.cSld.bg))
            tree = new.shapes._spTree
            for n in keep:
                tree.append(copy.deepcopy(sid(n)._element))

            def clone(n, x, y, w, h, text=None, size=None):
                el = copy.deepcopy(sid(n)._element); tree.append(el)
                sh = new.shapes[-1]
                sh.left, sh.top, sh.width, sh.height = Emu(x * EMU), Emu(y * EMU), Emu(w * EMU), Emu(h * EMU)
                if text is not None:
                    tf = sh.text_frame; p = tf.paragraphs[0]
                    for extra in tf.paragraphs[1:]:
                        extra._p.getparent().remove(extra._p)
                    runs = p.runs; runs[0].text = text
                    for r in runs[1:]:
                        r._r.getparent().remove(r._r)
                    if size:
                        runs[0].font.size = Pt(size)
                return sh
            x, y, w, h = PIC
            clone(11, x - 2, y - 2, w + 4, h + 4)  # 外框
            new.shapes.add_picture(str(self.E / 'assets/visuals' / f"demo_{d['key']}.png"), Emu(x * EMU), Emu(y * EMU), Emu(w * EMU), Emu(h * EMU))
            clone(9, COL_X, 74, COL_W, 74, d['title'], 21)
            clone(10, COL_X, 150, COL_W, 34, d['scene'], 11)
            for i, (hd, body) in enumerate(d['points']):
                cy = CARD_Y0 + i * CARD_GAP
                clone(11, COL_X, cy, COL_W - 4, CARD_H)
                clone(12, COL_X + 12, cy + 8, COL_W - 28, 26, f'{i + 1:02d} {hd}', 15)
                clone(13, COL_X + 12, cy + 38, COL_W - 28, 30, body, 13)
            link = clone(19, COL_X, 448, COL_W, 22, '▶ 開啟 3D 動畫（線上版）', 13)
            link.text_frame.paragraphs[0].runs[0].hyperlink.address = PAGES[d['page']][1] + '#' + d['hash']
            notes = d['sentences'] + ['[Sources]', f"{PAGES[d['page']][1]}#{d['hash']}（{d['scene']}，pcpcchen-coder/QuantumComputing）"]
            new.notes_slide.notes_text_frame.text = '\n'.join(notes)
            el = lst[-1]; lst.remove(el); lst.insert(d['after'], el)
        # 頁碼重編
        for i, s in enumerate(prs.slides, 1):
            for sh in s.shapes:
                if sh.has_text_frame and sh.text_frame.text.startswith(f'{self.lid} · '):
                    sh.text_frame.paragraphs[0].runs[0].text = f'{self.lid} · {i:02d}/{len(prs.slides):02d}'
        assert len(prs.slides) == self.total
        out = self.E / 'production/presentation' / f'{self.name}.pptx'
        prs.save(out)
        self.render(out)
        print('deck', out, len(prs.slides), 'slides', flush=True)

    def render(self, deck):
        sys.path.insert(0, str(X / 'pipeline'))
        import academy
        with tempfile.TemporaryDirectory(prefix='qv2-render-') as t:
            t = Path(t)
            office = ['soffice', f"-env:UserInstallation={(t / 'profile').as_uri()}", '--headless']
            run([*office, '--convert-to', 'odp', '--outdir', t / 'odp', deck])
            (t / 'fixed').mkdir()
            academy.disable_asian_latin_autospace(t / 'odp' / f'{self.name}.odp', t / 'fixed' / f'{self.name}.odp')
            run([*office, '--convert-to', 'pdf', '--outdir', t, t / 'fixed' / f'{self.name}.odp'])
            run(['pdftoppm', '-png', '-scale-to-x', '1920', '-scale-to-y', '1080', t / f'{self.name}.pdf', t / 'slide'])
            imgs = sorted(t.glob('slide-*.png'), key=lambda p: int(p.stem.split('-')[-1]))
            assert len(imgs) == self.total, len(imgs)
            for f in (self.E / 'assets/slides').glob('*.png'):
                f.unlink()
            for i, p in enumerate(imgs, 1):
                shutil.copy2(p, self.E / f'assets/slides/page_{i:02d}.png')

    # ── 4. 組裝 ────────────────────────────────────────────────
    def highlight_pngs(self, d):
        from PIL import Image, ImageDraw
        outs = []
        for i in range(3):
            im = Image.new('RGBA', (1920, 1080), (0, 0, 0, 0)); dr = ImageDraw.Draw(im)
            cy = CARD_Y0 + i * CARD_GAP
            dr.rounded_rectangle([COL_X * 2 - 4, cy * 2 - 4, (COL_X + COL_W - 4) * 2 + 4, (cy + CARD_H) * 2 + 4],
                                 radius=14, outline=(255, 193, 47, 255), width=5)
            p = self.E / 'work' / f"hl_{d['key']}_{i}.png"; im.save(p); outs.append(p)
        return outs

    def assemble(self):
        W = self.E / 'work'
        timing = json.loads((self.E / 'production/demo-timing.json').read_text(encoding='utf-8'))
        v1sc = {s['slide']: s for s in self.v1timing['scenes']}
        vf_static = ('scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,format=yuv420p,setsar=1,'
                     'eq=contrast=1.015:brightness=0.003:saturation=1.03,vignette=angle=PI/4.8:dither=0')
        intro = W / 'clip-00.mp4'
        if not intro.exists():
            run(['ffmpeg', '-y', '-v', 'error', '-i', OPENING, '-vf', 'scale=1920:1080:flags=lanczos,fps=30,format=yuv420p,setsar=1',
                 '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', '-ar', '48000', '-ac', '2', '-c:a', 'aac', '-b:a', '192k', intro])
        clips, durs, audios, scenes = [intro], [dur(intro)], [intro], []
        for k, (kind, ref) in enumerate(self.order, 1):
            png = self.E / f'assets/slides/page_{k:02d}.png'
            out = W / f'clip-{k:02d}.mp4'
            if kind == 'slide':
                s = v1sc[ref]; d_ = s['duration']
                run(['ffmpeg', '-y', '-v', 'error', '-loop', '1', '-i', png, '-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=48000',
                     '-vf', vf_static, '-t', f'{d_:.3f}', '-r', str(FPS), '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17',
                     '-c:a', 'aac', '-shortest', out])
                audios.append(self.v1 / s['audio'])
                scenes.append({'page': k, 'kind': 'slide', 'v1slide': ref, 'title': s['title'], 'duration': d_,
                               'sentences': s['sentences'], 'audio': str(self.v1 / s['audio'])})
            else:
                d = self.demo(ref); tm = timing[ref]; d_ = tm['duration']
                meta = json.loads(Path(str(self.E / 'assets/visuals' / f'demo_{ref}.webm') + '.json').read_text())
                hl = self.highlight_pngs(d)
                n = len(d['sentences'])
                pmap = [min(i, 2) for i in range(n)] if n == 3 else [0, 1, 1, 2]
                st = [s['start'] for s in tm['sentences']] + [d_]
                x, y, w, h = [v * 2 for v in PIC]
                fc = [f'[1:v]fps={FPS},scale={w}:{h}:flags=lanczos,setpts=PTS-STARTPTS[rec]',
                      f'[0:v][rec]overlay={x}:{y}:shortest=0[b0]']
                last = 'b0'
                for i in range(n):
                    a, b = st[i], st[i + 1]
                    fc.append(f'[{last}][{2 + pmap[i]}:v]overlay=0:0:enable=\'between(t,{a:.3f},{b:.3f})\'[b{i + 1}]'); last = f'b{i + 1}'
                fc.append(f'[{last}]format=yuv420p,setsar=1,eq=contrast=1.015:brightness=0.003:saturation=1.03,vignette=angle=PI/4.8:dither=0[v]')
                run(['ffmpeg', '-y', '-v', 'error', '-loop', '1', '-t', f'{d_:.3f}', '-i', png,
                     '-ss', f"{meta['trimStart']:.3f}", '-i', self.E / 'assets/visuals' / f'demo_{ref}.webm',
                     *sum([['-loop', '1', '-t', f'{d_:.3f}', '-i', p] for p in hl], []),
                     '-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=48000',
                     '-filter_complex', ';'.join(fc), '-map', '[v]', '-map', f'{2 + len(hl)}:a',
                     '-t', f'{d_:.3f}', '-r', str(FPS), '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', '-c:a', 'aac', out])
                audios.append(self.E / tm['audio'])
                scenes.append({'page': k, 'kind': 'demo', 'demo': ref, 'title': d['title'], 'duration': d_,
                               'sentences': tm['sentences'], 'audio': tm['audio'], 'animation': f"{PAGES[d['page']][1]}#{d['hash']}"})
            clips.append(out); durs.append(d_)
            print(f'clip {k:02d}/{self.total} {kind} {d_:.2f}s', flush=True)
        # 淡化串接（同 v1：每段尾端凍結 FADE 秒，再以 fade 轉場）
        padded = []
        for i, c in enumerate(clips):
            o = W / f'pad-{i:02d}.mp4'
            if i < len(clips) - 1:
                run(['ffmpeg', '-y', '-v', 'error', '-i', c, '-vf', f'tpad=stop_mode=clone:stop_duration={FADE}', '-c:v', 'libx264',
                     '-preset', 'veryfast', '-crf', '17', '-c:a', 'copy', o])
            else:
                shutil.copyfile(c, o)
            padded.append(o)
        fc, last, el = [], '0:v', 0.0
        for i in range(len(padded) - 1):
            off = durs[i] if i == 0 else el + durs[i]
            fc.append(f'[{last}][{i + 1}:v]xfade=transition=fade:duration={FADE}:offset={off:.3f}[v{i + 1}]'); last = f'v{i + 1}'; el = off
        fc.append(f'[{last}]format=yuv420p,setsar=1[vout]')
        video = W / 'video.mp4'
        run(['ffmpeg', '-y', '-v', 'error', *sum([['-i', c] for c in padded], []), '-filter_complex', ';'.join(fc),
             '-map', '[vout]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', video])
        # 旁白：片頭原音＋各段旁白（無背景音樂），量測後定增益到 −16 LUFS
        base = W / 'base-audio.m4a'
        ins = sum([['-i', p] for p in audios], [])
        fa = ''.join(f'[{i}:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,apad,atrim=duration={durs[i]:.9f},asetpts=PTS-STARTPTS[a{i}];'
                     for i in range(len(audios)))
        fa += ''.join(f'[a{i}]' for i in range(len(audios))) + f'concat=n={len(audios)}:v=0:a=1[aout]'
        run(['ffmpeg', '-y', '-v', 'error', *ins, '-filter_complex', fa, '-map', '[aout]', '-c:a', 'aac', '-b:a', '192k', base])
        an = subprocess.run(['ffmpeg', '-hide_banner', '-i', str(base), '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'],
                            capture_output=True, text=True, check=True)
        stt = json.loads(an.stderr[an.stderr.rfind('{'):])
        gain = min(-16 - float(stt['input_i']), -1.5 - float(stt['input_tp']) - .1)
        normed = W / 'normed.wav'
        run(['ffmpeg', '-y', '-v', 'error', '-i', base, '-af', f'volume={gain:.6f}dB', '-c:a', 'pcm_s16le', normed])
        master = self.E / 'output' / f'{self.name}-master.mp4'
        run(['ffmpeg', '-y', '-v', 'error', '-i', video, '-i', normed, '-map', '0:v', '-map', '1:a', '-ar', '48000', '-ac', '2',
             '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', master])
        # 字幕
        sys.path.insert(0, str(X / 'pipeline/scripts'))
        from caption_wrap import wrap_caption
        cues, burn, t0 = [], [], durs[0]
        for sc, dd in zip(scenes, durs[1:]):
            for s in sc['sentences']:
                rng = f"{srt_time(t0 + s['start'])} --> {srt_time(t0 + s['end'])}"
                n = len(cues) + 1
                cues.append(f"{n}\n{rng}\n{s['text']}\n")
                burn.append(f"{n}\n{rng}\n" + '\n'.join(wrap_caption(s['text'])) + '\n')
            t0 += dd
        (self.E / 'subtitles/zh-TW.srt').write_text('\n'.join(cues) + '\n', encoding='utf-8')
        bsrt = W / 'burn.srt'; bsrt.write_text('\n'.join(burn) + '\n', encoding='utf-8')
        zh = self.E / 'output' / f'{self.name}-zh-TW.mp4'
        run(['ffmpeg', '-y', '-v', 'error', '-i', master, '-vf', f"subtitles='{bsrt}':fontsdir='{X}/assets/fonts':force_style='{STYLE}'",
             '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-c:a', 'copy', zh])
        shutil.copyfile(self.E / 'assets/slides/page_01.png', self.E / 'output/thumbnail.png')
        dump(self.E / 'production/timing.json', {'version': 2, 'opening': durs[0], 'scenes': scenes})
        dump(self.E / 'qc/assembly.json', {'masterDuration': dur(master), 'zhDuration': dur(zh), 'opening': {'file': str(OPENING), 'seconds': durs[0]},
                                           'pages': self.total, 'demos': len(self.demos), 'cues': len(cues), 'fadeSeconds': FADE, 'fps': FPS,
                                           'loudness': {'analysis': stt, 'gainDb': gain, 'predictedIntegratedLUFS': float(stt['input_i']) + gain},
                                           'backgroundMusic': 'none', 'subtitleStyle': STYLE, 'captionLineBreak': 'kinsoku'})
        print('master', master, f'{dur(master):.2f}s; cues', len(cues), flush=True)


if __name__ == '__main__':
    lid = sys.argv[1]; step = sys.argv[2] if len(sys.argv) > 2 else 'all'
    L = Lesson(lid)
    for s in (['audio', 'record', 'deck', 'assemble'] if step == 'all' else [step]):
        getattr(L, s)()
