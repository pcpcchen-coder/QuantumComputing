// 擷取 transmon.pptx 用 3D 截圖 → slides/figures/3d_transmon/
// 用法：node slides/capture_3d_transmon.js [9-12]（需 Playwright 與 Chromium；加 9-12 只擷取第 9–12 章）
const { chromium } = require('playwright');
const path = require('path');
const OUT = path.join(__dirname, 'figures/3d_transmon/');
const ANI = 'file://' + path.resolve(__dirname, '../animations') + '/';
(async () => {
  const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-webgl', '--ignore-gpu-blocklist'] });
  const ctx = await b.newContext({ viewport: { width: 1600, height: 900 }, deviceScaleFactor: 1.5 });
  const p = await ctx.newPage();
  p.on('pageerror', e => console.log('ERR', e.message));
  const clip = { x: 0, y: 0, width: 1160, height: 840 };
  const hide = () => p.addStyleTag({ content: '#panel,.hint,#rail,.rail{display:none!important}' });
  const shot = async (name, c = clip) => { await p.screenshot({ path: OUT + name + '.jpg', type: 'jpeg', quality: 88, ...(c ? { clip: c } : {}) }); console.log('saved', name); };
  const click = (id) => p.evaluate((id) => document.getElementById(id).click(), id);
  const step = (box, n) => p.evaluate(([box, n]) => document.querySelectorAll('#' + box + ' button')[n].click(), [box, n]);
  const open = async (hash) => { await p.goto(ANI + 'transmon-3d.html#' + hash); await p.waitForTimeout(2500); };

  const auto = (id) => p.evaluate((id) => { const c = document.getElementById(id); c.checked = false; c.dispatchEvent(new Event('change')); }, id);
  const ONLY_NEW = process.argv[2] === '9-12';
  if (!ONLY_NEW) {
  await open('chip'); await click('c1pulse'); await hide(); await p.waitForTimeout(1200); await shot('ch1_chip');
  await open('junction'); await hide(); await p.waitForTimeout(1500); await shot('ch2_junction');
  await open('potential'); await hide(); await p.waitForTimeout(1500); await shot('ch3_potential');
  await open('control'); await click('c4xh'); await hide(); await p.waitForTimeout(3000); await shot('ch4_control');
  await open('readout'); await click('c5m20'); await hide(); await p.waitForTimeout(6000); await shot('ch5_readout');
  await open('case'); await p.evaluate(() => { document.getElementById('c6auto').checked = false; document.getElementById('c6auto').dispatchEvent(new Event('change')); });
  await step('c6steps', 2); await hide(); await p.waitForTimeout(9000); await shot('ch6_case_plan');
  await step('c6steps', 4); await p.waitForTimeout(9000); await shot('ch6_case_cz');
  await open('grover'); await p.evaluate(() => { document.getElementById('g7auto').checked = false; document.getElementById('g7auto').dispatchEvent(new Event('change')); });
  await step('g7steps', 0); await hide(); await p.waitForTimeout(10000); await shot('ch7_bell');
  await step('g7steps', 3); await p.waitForTimeout(10000); await shot('ch7_grover');
  await open('shor'); await p.evaluate(() => { document.getElementById('g8auto').checked = false; document.getElementById('g8auto').dispatchEvent(new Event('change')); });
  await step('g8steps', 3); await hide(); await p.waitForTimeout(9000); await shot('ch8_comb');
  await step('g8steps', 4); await p.waitForTimeout(10000); await shot('ch8_qft');
  }
  // 第 9–12 章（看板較寬，擷取整個畫面）
  await open('bv'); await auto('g9auto');
  await step('g9steps', 2); await hide(); await p.waitForTimeout(10000); await shot('ch9_bv_query', null);
  await step('g9steps', 4); await p.waitForTimeout(10000); await shot('ch9_bv_measure', null);
  await open('surface'); await auto('g10auto');
  await step('g10steps', 0); await hide(); await p.waitForTimeout(9000); await shot('ch10_surface_layout', null);
  await step('g10steps', 2); await p.waitForTimeout(12000); await shot('ch10_surface_error', null);
  await open('surgery'); await auto('g11auto');
  await step('g11steps', 1); await hide(); await p.waitForTimeout(16000); await shot('ch11_merge', null);
  await step('g11steps', 5); await p.waitForTimeout(30000); await shot('ch11_distill', null);
  await open('stack'); await auto('g12auto');
  await step('g12steps', 3); await hide(); await p.waitForTimeout(10000); await shot('ch12_route', null);
  await step('g12steps', 5); await p.waitForTimeout(12000); await shot('ch12_pulse', null);
  await b.close();
})();
