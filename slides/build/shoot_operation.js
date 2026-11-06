/* 擷取「如何操作量子電腦」3D 場景截圖，供簡報使用。
 * 用法：node shoot_operation.js   （需要 Playwright + Chromium）
 * 輸出：../figures/3d_op/<場景>.jpg（2560×1440）
 */
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');
const OUT = path.resolve(__dirname, '..', 'figures', '3d_op');
const PAGE = 'file://' + path.resolve(__dirname, '..', '..', 'animations', 'operation.html');
fs.mkdirSync(OUT, { recursive: true });

// 每個場景：拍照前的操作（依按鈕文字點擊、設定滑桿），以及等待時間
const click = (t) => `[...document.querySelectorAll('#controls button')].find((b) => b.textContent.trim().startsWith(${JSON.stringify(t)})).click()`;
const slide = (label, v) => `(() => { const l = [...document.querySelectorAll('#controls .slider')].find((x) => x.textContent.includes(${JSON.stringify(label)})); const r = l.querySelector('input'); r.value = ${v}; r.dispatchEvent(new Event('input')); })()`;
const PLAN = {
  qubit: { act: [click('一次跑 1000 shots')], wait: 1500 },
  gates: { act: [click('H'), click('T')], wait: 4500 },
  pulse: { act: [slide('閘長度', 40), click('▶ 送出脈衝')], wait: 2600 },
  register: { act: [slide('量子位元數', 3), click('GHZ 態')], wait: 2000 },
  twoqubit: { act: [click('▶ 執行')], wait: 3000 },
  circuit: { act: [click('Grover'), ...Array(8).fill(click('單步'))], wait: 2500 },
  readout: { act: [], wait: 6000 },
  interference: { act: [slide('相位 φ', 60)], wait: 1500 },
  grover: { act: [click('自動跑到最佳次數')], wait: 6500 },
  shor: { act: [click('下一步'), click('下一步'), click('下一步'), click('下一步')], wait: 2500 },
  qec: { act: [click('d = 7'), slide('實體錯誤率', 0.07), click('下一步'), click('下一步'), click('下一步')], wait: 1500 },
  workflow: { act: [], wait: 10500 },
};
const EXTRA = { // 同一場景的第二張圖
  shor_comb: { id: 'shor', act: [click('下一步'), click('下一步'), click('下一步')], wait: 2500 },
  register_bell: { id: 'register', act: [click('Bell 態')], wait: 2000 },
  twoqubit_cr: { id: 'twoqubit', act: [click('交叉共振'), click('▶ 執行')], wait: 3200 },
  circuit_bv: { id: 'circuit', act: [click('Bernstein'), ...Array(5).fill(click('單步'))], wait: 2500 },
  interference_dj: { id: 'interference', act: [click('3 位元'), click('平衡 f = 奇偶')], wait: 1500 },
};

(async () => {
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const p = await b.newPage({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 2 });
  p.on('pageerror', (e) => console.error('pageerror', e.message));
  const only = process.argv.slice(2);
  const jobs = [...Object.entries(PLAN).map(([id, o]) => [id, { id, ...o }]), ...Object.entries(EXTRA)].filter(([n]) => !only.length || only.includes(n));
  for (const [name, o] of jobs) {
    await p.goto(`${PAGE}?noui=1&clean=1#${o.id}`);
    await p.waitForTimeout(1200);
    // 用 UI 操作需要面板存在（隱藏時按鈕仍可點擊）
    for (const a of o.act) { await p.evaluate(a); await p.waitForTimeout(250); }
    await p.waitForTimeout(o.wait);
    await p.screenshot({ path: path.join(OUT, name + '.jpg'), type: 'jpeg', quality: 90 });
    console.log('saved', name);
  }
  await b.close();
})();
