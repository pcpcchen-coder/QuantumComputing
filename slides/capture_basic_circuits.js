// 擷取「十個基礎量子電路」與「量子理論基礎」簡報用截圖 → slides/figures/basic_circuits/
// 用法：node slides/capture_basic_circuits.js（需 Playwright 與 Chromium；離線可用）
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const OUT = path.join(__dirname, 'figures/basic_circuits/');
const PAGE = 'file://' + path.resolve(__dirname, '../animations/basic-circuits.html');
const BASICS = 'file://' + path.resolve(__dirname, '../animations/quantum-basics.html');

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 1120, height: 1000 }, deviceScaleFactor: 1.5, colorScheme: 'light' });
  const p = await ctx.newPage();
  p.on('pageerror', e => console.log('ERR', e.message));
  // 固定亂數，讓量測次數每次擷取都一樣
  await p.addInitScript(() => { let s = 12345; Math.random = () => ((s = (s * 1103515245 + 12345) % 2147483648) / 2147483648); });

  // 從「電路」卡片上緣截到「量測」卡片下緣
  const shot = async (name) => {
    const box = await p.evaluate(() => {
      const a = document.querySelector('main > .card').getBoundingClientRect();
      const g = document.querySelector('.grid2').getBoundingClientRect();
      return { x: a.left - 12, y: a.top + scrollY - 12, width: a.width + 24, height: g.bottom - a.top + 24 };
    });
    await p.screenshot({ path: OUT + name + '.jpg', type: 'jpeg', quality: 88, clip: box, fullPage: true });
    console.log('saved', name);
  };
  const open = async (hash, step, opt) => {
    await p.goto(PAGE + '#' + hash); await p.waitForTimeout(300);
    if (opt) await p.evaluate((t) => [...document.querySelectorAll('#opts button')].find(x => x.textContent === t).click(), opt);
    await p.evaluate(() => document.getElementById('bFirst').click());
    for (let i = 0; i < step; i++) { await p.click('#bNext'); await p.waitForTimeout(120); }
    await p.waitForTimeout(900);
  };
  const measure = async () => { await p.click('#m1000'); await p.waitForTimeout(1600); };

  await open('interference', 2); await measure(); await shot('interf_z');   // Z 之後：機率仍各半，Bloch 指向 −x
  await open('bell', 2); await measure(); await shot('bell_final');         // Φ⁺：只有 00、11
  await open('deutsch', 3); await shot('deutsch_oracle');                   // 黑盒之後：q0 = 1 的兩根變號
  await open('bv', 4); await measure(); await shot('bv_final');             // 密碼 101
  await open('teleport', 4); await measure(); await shot('teleport_final');  // q2 = ψ，q0 不再是 ψ
  await open('grover', 4, '3 顆（N = 8）'); await shot('grover_oracle');     // 3 顆位元、第 2 輪標記後：答案變號、平均線
  await open('grover-sat', 4); await shot('grover_sat');                    // SAT 規則版 Oracle：CZ 剛變號，只有 1110 是負的
  await open('qft', 5); await shot('qft_basis');                            // x = 1：大小一樣、相位每格 45°
  await open('shor', 3); await p.click('#m1'); await p.click('#m1000'); await p.waitForTimeout(1600); await shot('shor_final'); // 尖峰 0、2、4、6

  // 理論基礎頁：第 2 課（相位）與第 6 課（干涉）的互動圖
  await p.goto(BASICS); await p.waitForTimeout(300);
  const setRange = (id, v) => p.$eval('#' + id, (e, v) => { e.value = v; e.dispatchEvent(new Event('input')); }, v);
  await setRange('q2p', 120); await setRange('q6p', 120);
  for (const [sel, name] of [['#phase .fig', 'basics_phase'], ['#interference .fig', 'basics_interference']]) {
    await p.locator(sel).screenshot({ path: OUT + name + '.jpg', type: 'jpeg', quality: 88 }); console.log('saved', name);
  }

  await b.close();
})();
