// 擷取 transmon.pptx 用的 2D 圖解截圖（animations/lc-vs-jj.html）→ slides/figures/2d_lcjj/
// 用法：node slides/capture_2d_lcjj.js（需 Playwright 與 Chromium；離線時字型改用系統字型）
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const OUT = path.join(__dirname, 'figures/2d_lcjj/');
const PAGE = 'file://' + path.resolve(__dirname, '../animations/lc-vs-jj.html');
fs.mkdirSync(OUT, { recursive: true });
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: 1100, height: 900 }, deviceScaleFactor: 2, colorScheme: 'light' });
  const p = await ctx.newPage();
  p.on('pageerror', e => console.log('ERR', e.message));
  await p.goto(PAGE, { waitUntil: 'networkidle' }).catch(() => {});
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(500);
  // 依多個元素的外框取聯集截圖
  const shot = async (name, sels, pad = 8) => {
    const box = await p.evaluate((sels) => {
      const rs = sels.map(s => document.querySelector(s).getBoundingClientRect());
      const x0 = Math.min(...rs.map(r => r.left)), y0 = Math.min(...rs.map(r => r.top));
      const x1 = Math.max(...rs.map(r => r.right)), y1 = Math.max(...rs.map(r => r.bottom));
      return { x: x0 + scrollX, y: y0 + scrollY, width: x1 - x0, height: y1 - y0 };
    }, sels);
    await p.screenshot({ path: OUT + name + '.jpg', type: 'jpeg', quality: 90, fullPage: true,
      clip: { x: box.x - pad, y: box.y - pad, width: box.width + 2 * pad, height: box.height + 2 * pad } });
    console.log('saved', name, Math.round(box.width + 2 * pad) + 'x' + Math.round(box.height + 2 * pad));
  };
  await shot('step1_iphi', ['#s1 .legend', '#fig1']);
  await shot('step3_levels', ['#s3 .twin']);
  await shot('step6_drag', ['#s6drag .quad', '#s6drag .legend']);
  await b.close();
})();
