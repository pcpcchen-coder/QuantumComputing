// 擷取「八個基礎量子電路」簡報用截圖 → slides/figures/basic_circuits/
// 用法：node slides/capture_basic_circuits.js（需 Playwright 與 Chromium；離線可用）
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const OUT = path.join(__dirname, 'figures/basic_circuits/');
const PAGE = 'file://' + path.resolve(__dirname, '../animations/basic-circuits.html');

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

  await b.close();
})();
