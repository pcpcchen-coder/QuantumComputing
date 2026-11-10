// 擷取 transmon.pptx 用 3D 截圖 → slides/figures/3d_transmon/
// 用法：node slides/capture_3d_transmon.js（需 Playwright 與 Chromium；transmon-3d 需連網載入 three.js）
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
  const shot = async (name) => { await p.screenshot({ path: OUT + name + '.jpg', type: 'jpeg', quality: 88, clip }); console.log('saved', name); };
  const click = (id) => p.evaluate((id) => document.getElementById(id).click(), id);
  const step = (box, n) => p.evaluate(([box, n]) => document.querySelectorAll('#' + box + ' button')[n].click(), [box, n]);
  const open = async (hash) => { await p.goto(ANI + 'transmon-3d.html#' + hash); await p.waitForTimeout(2500); };

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
  await b.close();
})();
