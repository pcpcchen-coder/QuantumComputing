/* 依時間表操作 3D 動畫並錄影（Playwright + Chromium，1600×900）。
 * 用法：node record_demo.js spec.json
 * spec = { url, duration, actions: [{t, kind, label|id, value, from, to, secs}], shot_t, video_out, shot_out }
 * 輸出：video_out（webm，已記錄要裁掉的開頭秒數於 video_out + '.json'）、shot_out（png）
 * 被按的按鈕會短暫加上黃色外框，讓觀眾看得出按了哪裡。
 */
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const spec = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const dir = fs.mkdtempSync(path.join(path.dirname(spec.video_out), 'rec-'));
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const ctx = await b.newContext({ viewport: { width: 1600, height: 900 }, recordVideo: { dir, size: { width: 1600, height: 900 } } });
  const tCtx = Date.now();
  const p = await ctx.newPage();
  p.on('pageerror', (e) => console.error('pageerror', e.message));
  await p.goto(spec.url);
  await p.waitForTimeout(spec.settle || 2500);
  await p.evaluate(() => {
    const st = document.createElement('style');
    st.textContent = '.qflash{outline:3px solid #f5c242 !important; outline-offset:2px; box-shadow:0 0 14px #f5c242 !important;}';
    document.head.appendChild(st);
    window.__flash = (el) => { if (!el) return; el.classList.add('qflash'); setTimeout(() => el.classList.remove('qflash'), 700); };
    window.__btn = (t) => [...document.querySelectorAll('#controls button')].find((x) => x.textContent.trim().startsWith(t));
    window.__sl = (t) => [...document.querySelectorAll('#controls .slider')].find((x) => x.textContent.includes(t));
    window.__setSlider = (t, v) => { const l = window.__sl(t); const r = l.querySelector('input'); r.value = v; r.dispatchEvent(new Event('input')); return l; };
  });
  const t0 = Date.now();
  const at = (sec) => t0 + sec * 1000;
  const sleepUntil = async (ms) => { const d = ms - Date.now(); if (d > 0) await p.waitForTimeout(d); };
  const acts = [...spec.actions].sort((a, b2) => a.t - b2.t);
  let shotDone = false;
  const maybeShot = async () => {
    if (!shotDone && Date.now() >= at(spec.shot_t)) { await p.screenshot({ path: spec.shot_out }); shotDone = true; }
  };
  for (const a of acts) {
    if (!shotDone && at(spec.shot_t) < at(a.t)) { await sleepUntil(at(spec.shot_t)); await maybeShot(); }
    await sleepUntil(at(a.t));
    if (a.kind === 'click') {
      const ok = await p.evaluate((t) => { const el = window.__btn(t); if (!el) return false; window.__flash(el); el.click(); return true; }, a.label);
      if (!ok) throw new Error('button not found: ' + a.label);
    } else if (a.kind === 'id') {
      const ok = await p.evaluate((id) => { const el = document.getElementById(id); if (!el) return false; window.__flash(el); el.click(); return true; }, a.id);
      if (!ok) throw new Error('id not found: ' + a.id);
    } else if (a.kind === 'slider') {
      await p.evaluate(([t, v]) => window.__flash(window.__setSlider(t, v)), [a.label, a.value]);
    } else if (a.kind === 'toggle') {
      const ok = await p.evaluate(([t, v]) => {
        const el = window.__btn(t); if (!el) return false;
        window.__flash(el); if (el.classList.contains('on') !== v) el.click(); return true;
      }, [a.label, a.value]);
      if (!ok) throw new Error('toggle not found: ' + a.label);
    } else if (a.kind === 'sweep') {
      const steps = Math.max(2, Math.round(a.secs * 12));
      for (let k = 0; k <= steps; k++) {
        const v = a.from + (a.to - a.from) * k / steps;
        await sleepUntil(at(a.t + a.secs * k / steps));
        await p.evaluate(([t, v2]) => { const l = window.__setSlider(t, Math.round(v2)); if (l) l.classList.add('qflash'); }, [a.label, v]);
        await maybeShot();
      }
      await p.evaluate((t) => { const l = window.__sl(t); if (l) l.classList.remove('qflash'); }, a.label);
    }
    await maybeShot();
  }
  if (!shotDone) { await sleepUntil(at(spec.shot_t)); await maybeShot(); }
  await sleepUntil(at(spec.duration + 0.4));
  const video = p.video();
  await ctx.close();
  await b.close();
  fs.renameSync(await video.path(), spec.video_out);
  fs.rmSync(dir, { recursive: true, force: true });
  fs.writeFileSync(spec.video_out + '.json', JSON.stringify({ trimStart: (t0 - tCtx) / 1000, duration: spec.duration }));
  console.log('recorded', spec.video_out, ((t0 - tCtx) / 1000).toFixed(2));
})();
