// 擷取 Deutsch 簡報用 3D 截圖 → slides/figures/3d_deutsch/
// 用法：node slides/capture_3d_deutsch.js（需 Playwright 與 Chromium；transmon-3d 需連網載入 three.js）
const { chromium } = require('playwright');
const path = require('path');
const OUT = path.join(__dirname, 'figures/3d_deutsch/');
const ANI = 'file://' + path.resolve(__dirname, '../animations') + '/';
(async () => {
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-webgl', '--ignore-gpu-blocklist'] });
  const ctx = await b.newContext({ viewport: { width: 1600, height: 900 }, deviceScaleFactor: 1.5 });
  const p = await ctx.newPage();
  p.on('pageerror', e => console.log('ERR', e.message));
  const hideT = () => p.addStyleTag({ content: '#panel,.hint,#rail,.rail{display:none!important}' });
  const clipT = { x: 0, y: 0, width: 1160, height: 840 };
  const shot = async (name, clip = clipT) => { await p.screenshot({ path: OUT + name + '.jpg', type: 'jpeg', quality: 88, ...(clip ? { clip } : {}) }); console.log('saved', name); };

  // 1) 步驟 7：Deutsch（f₃(x) = x）
  await p.goto(ANI + 'transmon-3d.html#deutsch'); await hideT();
  const t0 = Date.now(); const at = async (s) => { const w = s * 1000 - (Date.now() - t0); if (w > 0) await p.waitForTimeout(w); };
  await at(9.5); await shot('deu_start');
  await at(15.5); await shot('deu_hh');
  await at(27); await shot('deu_uf');
  await at(38.5); await shot('deu_h');
  await at(45.8); await shot('deu_meas');

  // 2) 步驟 8：自由實驗，隱藏黑盒子（固定抽到 f₂ 常數 1）
  await p.goto(ANI + 'transmon-3d.html#deutsch-lab'); await p.waitForTimeout(2500);
  await p.evaluate(() => { const r = Math.random; Math.random = () => 0.3; document.querySelector('[data-fn="hide"]').click(); Math.random = r; });
  await p.evaluate(() => document.getElementById('g7deu').click());
  await hideT();
  await p.waitForTimeout(5200); await shot('lab_hidden');
  await p.waitForTimeout(5500); await shot('lab_reveal');

  // 3) 操作篇場景 8：干涉
  await p.goto(ANI + 'operation.html#interference'); await p.waitForTimeout(2500);
  await p.evaluate(() => document.body.classList.add('hide-ui'));
  await p.waitForTimeout(1500); await shot('interf_two_paths', null);
  await p.evaluate(() => document.body.classList.remove('hide-ui'));
  const clickTxt = (t) => p.evaluate((t) => { const el = [...document.querySelectorAll('button')].find(x => x.textContent.trim() === t); if (!el) throw new Error('no ' + t); el.click(); }, t);
  await clickTxt('3 位元：8 條路徑（Deutsch–Jozsa）');
  await clickTxt('常數 f = 0');
  await p.evaluate(() => document.body.classList.add('hide-ui'));
  await p.waitForTimeout(2500); await shot('interf_dj_const', null);
  await p.evaluate(() => document.body.classList.remove('hide-ui'));
  await clickTxt('平衡 f = x₀');
  await p.evaluate(() => document.body.classList.add('hide-ui'));
  await p.waitForTimeout(2500); await shot('interf_dj_bal', null);
  await b.close();
})();
