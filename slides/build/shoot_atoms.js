/* 擷取「離子阱與中性原子」3D 場景截圖，供簡報使用，並自動計算裁切範圍。
 * 用法：node shoot_atoms.js [名稱 ...]   （需要 Playwright + Chromium）
 * 操作計畫：atoms_plan_ion.json（場景 1–6）、atoms_plan_atom.json（場景 7–13）
 *   格式 { "<名稱>": { "id": "<場景代號，預設同名稱>", "act": [{"click":"按鈕文字開頭"}, {"slider":["標籤片段", 值]}, {"wait": 毫秒}], "wait": 毫秒 } }
 * 輸出：../figures/3d_atoms/<名稱>.jpg（2560×1440）與 atoms_crops.json（去掉背景的裁切範圍）
 */
const path = require('path');
const fs = require('fs');
const sharp = require('sharp');
const { chromium } = require('playwright');
const OUT = path.resolve(__dirname, '..', 'figures', '3d_atoms');
const PAGE = 'file://' + path.resolve(__dirname, '..', '..', 'animations', 'atoms.html');
const CROPS = path.join(__dirname, 'atoms_crops.json');
fs.mkdirSync(OUT, { recursive: true });

const PLAN = {
  ...JSON.parse(fs.readFileSync(path.join(__dirname, 'atoms_plan_ion.json'), 'utf8')),
  ...JSON.parse(fs.readFileSync(path.join(__dirname, 'atoms_plan_atom.json'), 'utf8')),
};
const click = (t) => `(() => { const b = [...document.querySelectorAll('#controls button')].find((x) => x.textContent.trim().startsWith(${JSON.stringify(t)})); if (!b) throw new Error('找不到按鈕：' + ${JSON.stringify(t)}); b.click(); })()`;
const slide = (label, v) => `(() => { const l = [...document.querySelectorAll('#controls .slider')].find((x) => x.textContent.includes(${JSON.stringify(label)})); if (!l) throw new Error('找不到滑桿：' + ${JSON.stringify(label)}); const r = l.querySelector('input'); r.value = ${v}; r.dispatchEvent(new Event('input')); })()`;

/* 找出與背景色（#070c16）明顯不同的像素範圍，四周留白 */
async function autoCrop(file) {
  const { data, info } = await sharp(file).raw().toBuffer({ resolveWithObject: true });
  const { width: W, height: H, channels: C } = info;
  let x0 = W, y0 = H, x1 = 0, y1 = 0;
  for (let y = 0; y < H; y += 2) {
    for (let x = 0; x < W; x += 2) {
      const i = (y * W + x) * C;
      if (Math.abs(data[i] - 7) + Math.abs(data[i + 1] - 12) + Math.abs(data[i + 2] - 22) > 40) {
        if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y;
      }
    }
  }
  const pad = 30;
  const left = Math.max(0, x0 - pad), top = Math.max(0, y0 - pad);
  return { left, top, width: Math.min(W, x1 + pad) - left, height: Math.min(H, y1 + pad) - top };
}

(async () => {
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const p = await b.newPage({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 2 });
  const errors = [];
  p.on('pageerror', (e) => errors.push(e.message));
  const only = process.argv.slice(2);
  const crops = fs.existsSync(CROPS) ? JSON.parse(fs.readFileSync(CROPS, 'utf8')) : {};
  for (const [name, o] of Object.entries(PLAN)) {
    if (only.length && !only.includes(name)) continue;
    const id = o.id || name;
    await p.goto(`${PAGE}?noui=1&clean=1#${id}`);
    await p.waitForTimeout(1200);
    for (const a of o.act || []) {
      if (a.click || a.slider) await p.evaluate(a.click ? click(a.click) : slide(a.slider[0], a.slider[1]));
      await p.waitForTimeout(a.wait ?? a.pause ?? 250);
    }
    await p.waitForTimeout(o.wait ?? 1500);
    const file = path.join(OUT, name + '.jpg');
    await p.screenshot({ path: file, type: 'jpeg', quality: 90 });
    crops[name] = await autoCrop(file);
    console.log('saved', name, JSON.stringify(crops[name]));
  }
  fs.writeFileSync(CROPS, JSON.stringify(crops, null, 1) + '\n');
  await b.close();
  if (errors.length) { console.error('頁面錯誤：\n' + errors.join('\n')); process.exit(1); }
})();
