/* 周邊場景 1：系統全景 — 量子電腦機房的所有設備與連接 */
App.register({
  id: 'overview', num: 1, short: '系統全景',
  title: '量子電腦機房全景：設備與連接',
  subtitle: '晶片只佔一小部分；要讓它運作，需要低溫、真空、氣體、電子、時脈、電力、冷卻水與軟體協同',
  desc: `<p>中央是<b>稀釋冷凍機</b>（框架 + 真空罩 + 各溫層），量子晶片在最底部 10 mK。周圍的設備與它的連接：</p>
<p><span style="color:#5ee08a">■</span> <b>脈衝管氦氣</b>：壓縮機 ⇄ 冷頭（高壓/低壓兩條軟管）<br>
<span style="color:#4fa3ff">■</span> <b>冷卻水</b>：冷卻水機 ⇄ 壓縮機（帶走約 10 kW 熱）<br>
<span style="color:#c58bff">■</span> <b>混合氣循環</b>：氣體處理系統（GHS）⇄ Still 抽氣 / 凝結回流<br>
<span style="color:#aab4c4">■</span> <b>真空</b>：GHS 的泵 → 外真空罩（OVC）<br>
<span style="color:#ff9f43">■</span> <b>微波與直流線</b>：控制電子機櫃 → 冷凍機頂板密封接頭<br>
<span style="color:#38c6d9">■</span> <b>資料 / 時脈</b>：控制電腦 ⇄ 電子機櫃、GHS、溫控器；雲端使用者<br>
<span style="color:#ffd166">■</span> <b>電力</b>：市電 → UPS → 關鍵負載；大功率設備直接由配電盤供電</p>`,
  camera: { pos: [10, 11, 17], target: [-0.5, 1.0, 0] },
  build(ctx) {
    const { scene, U, THREE, ui, app } = ctx;
    const floor = new THREE.Mesh(new THREE.PlaneGeometry(18, 11), U.mat(0x1a2130, { roughness: 0.95 }));
    floor.rotation.x = -Math.PI / 2; scene.add(floor);
    const grid = new THREE.GridHelper(18, 18, 0x2b3a55, 0x1f2a3d); grid.position.y = 0.005; scene.add(grid);

    const fridge = App.buildFridge(ctx, { pos: [0, 0, 0], canOpacity: 0.28 });
    ctx.label('稀釋冷凍機<br>（量子晶片在 10 mK）', [0, 5.05, 0], 'gold');
    const D = (o) => App.device(ctx, o);
    D({ pos: [-3.2, 0, 0.3], w: 1.0, h: 2.1, d: 0.9, label: '控制電子機櫃', cls: 'teal', leds: 6, ledColor: 0x38c6d9 });
    D({ pos: [-5.3, 0, -1.7], w: 0.7, h: 1.6, d: 0.8, label: '控制電腦', labelDy: 0.15, leds: 3 });
    D({ pos: [-5.4, 0, 2.5], w: 1.0, h: 1.4, d: 0.8, label: 'UPS 不斷電', color: 0x3a3424, leds: 2, ledColor: 0xffd166 });
    D({ pos: [-7.0, 0, 0.6], w: 0.5, h: 1.8, d: 0.4, label: '配電盤', color: 0x404652, leds: 1, ledColor: 0xffd166 });
    D({ pos: [3.0, 0, -1.4], w: 1.2, h: 1.6, d: 0.8, label: '氣體處理系統 GHS<br>渦輪泵 · 乾式泵 · 閥 · 冷阱', color: 0x34304a, leds: 4, ledColor: 0xc58bff });
    D({ pos: [3.7, 0, 1.9], w: 0.75, h: 1.0, d: 0.75, label: '脈衝管壓縮機（~11 kW）', color: 0x2f4a3a, leds: 2 });
    D({ pos: [6.6, 0, 3.2], w: 1.1, h: 1.3, d: 0.9, label: '冷卻水機', color: 0x24384f, leds: 2, ledColor: 0x4fa3ff });
    D({ pos: [-1.0, 0, -3.4], w: 0.8, h: 1.2, d: 0.6, label: '溫控器 / 壓力監控', leds: 3, ledColor: 0xe0a54a });
    // 混合氣儲存槽、液氮杜瓦
    const tank = new THREE.Mesh(new THREE.CylinderGeometry(0.45, 0.45, 1.4, 28), U.metal(0xb7c0cc)); tank.position.set(4.9, 0.7, -2.6); scene.add(tank);
    ctx.label('混合氣儲存槽（³He/⁴He）', [4.9, 1.75, -2.6], 'small');
    const dewar = new THREE.Mesh(new THREE.CylinderGeometry(0.25, 0.25, 0.9, 24), U.metal(0xd8dee8)); dewar.position.set(1.9, 0.45, -3.0); scene.add(dewar);
    ctx.label('液氮冷阱（選配）', [1.9, 1.15, -3.0], 'small');
    // 雲端
    const cloud = new THREE.Group();
    [[0, 0, 0, 0.5], [0.5, 0.1, 0, 0.4], [-0.5, 0.05, 0, 0.38], [0.15, 0.35, 0, 0.38]].forEach(([x, y, z, r]) => cloud.add(U.sphere(r, U.mat(0xdfe8f5, { emissive: 0x223355, emissiveIntensity: 0.4 }), x, y, z)));
    cloud.position.set(-7.0, 4.2, -3.2); scene.add(cloud);
    ctx.label('使用者 / 雲端 API', [-7.0, 5.0, -3.2], 'teal');
    // 頂部線槽
    const tray = U.box(10.5, 0.06, 0.5, U.metal(0x4b5566), -1.0, 4.55, 0.3); scene.add(tray);

    const L = {};
    const add = (key, pts, color, o = {}) => { (L[key] ||= []).push(App.Flow(scene, pts, color, o)); };
    // 脈衝管氦氣（高壓、低壓）
    add('pt', [[3.55, 1.0, 1.9], [3.55, 4.35, 1.9], [0.62, 4.35, 0.2], [0.62, 4.05, 0.2]], 0x5ee08a, { speed: 1.4, radius: 0.04 });
    add('pt', [[0.48, 4.05, 0.2], [0.48, 4.25, 0.2], [3.85, 4.25, 1.9], [3.85, 1.0, 1.9]], 0x2f9e5b, { speed: 1.4, radius: 0.04 });
    // 冷卻水（供 / 回）
    add('water', [[6.2, 0.15, 3.2], [4.2, 0.15, 3.2], [4.2, 0.15, 1.9], [4.08, 0.4, 1.9]], 0x4fa3ff, { speed: 1.2, radius: 0.045 });
    add('water', [[4.08, 0.6, 2.2], [4.4, 0.25, 2.2], [4.4, 0.25, 3.5], [6.2, 0.25, 3.5]], 0x9fd0ff, { speed: 1.2, radius: 0.045 });
    // 混合氣循環：Still 抽氣（粗管）→ GHS → 凝結回流
    add('mix', [[0.2, 3.38, -0.4], [0.2, 4.15, -0.4], [2.7, 4.15, -1.4], [2.7, 1.6, -1.4]], 0xc58bff, { speed: 0.9, radius: 0.07 });
    add('mix', [[3.3, 1.6, -1.4], [3.3, 3.95, -1.4], [-0.25, 3.95, -0.6], [-0.25, 3.38, -0.6]], 0xe0b8ff, { speed: 0.9, radius: 0.035 });
    add('mix', [[3.6, 0.25, -1.4], [4.6, 0.25, -2.3]], 0xc58bff, { speed: 0.4, radius: 0.04 });
    add('mix', [[2.4, 0.3, -1.6], [1.9, 0.3, -2.8]], 0xc58bff, { speed: 0.4, radius: 0.03 });
    // 真空：GHS → OVC
    add('vac', [[2.4, 0.9, -1.2], [1.6, 0.9, -0.4], [1.12, 1.4, -0.2]], 0xaab4c4, { speed: 0.6, radius: 0.05 });
    // 微波 / DC 線：機櫃 → 線槽 → 頂板
    for (let k = 0; k < 4; k++) add('rf', [[-3.45 + k * 0.17, 2.1, 0.3], [-3.45 + k * 0.17, 4.5, 0.3 + k * 0.05], [-0.5 + k * 0.12, 4.5, 0.3 + k * 0.05], [-0.5 + k * 0.12, 3.38, 0.3]], k < 3 ? 0xff9f43 : 0xd9c39a, { speed: 1.6, radius: 0.025, density: 2 });
    // 資料 / 時脈
    add('data', [[-5.0, 0.6, -1.3], [-3.6, 0.6, -0.2]], 0x38c6d9, { speed: 1.5 });
    add('data', [[-5.0, 0.4, -1.5], [-1.0, 0.4, -2.9], [2.5, 0.4, -1.3]], 0x38c6d9, { speed: 1.5, radius: 0.02 });
    add('data', [[-5.3, 1.6, -1.7], [-7.0, 3.7, -3.2]], 0x38c6d9, { speed: 1.5, radius: 0.02 });
    add('data', [[-1.0, 0.8, -3.1], [-0.6, 1.0, -1.1]], 0x38c6d9, { speed: 1.0, radius: 0.02 });
    // 電力
    add('power', [[-6.75, 0.08, 0.6], [-6.75, 0.08, 2.5], [-5.9, 0.08, 2.5]], 0xffd166, { speed: 1.0, radius: 0.03 });
    add('power', [[-4.9, 0.08, 2.5], [-3.2, 0.08, 2.5], [-3.2, 0.08, 0.75]], 0xffd166, { speed: 1.0, radius: 0.03 });
    add('power', [[-5.4, 0.08, 2.1], [-5.4, 0.08, -1.3]], 0xffd166, { speed: 1.0, radius: 0.03 });
    add('power', [[-6.75, 0.12, 0.6], [-6.75, 0.12, 4.4], [6.6, 0.12, 4.4], [6.6, 0.12, 3.65]], 0xffd166, { speed: 1.0, radius: 0.03 });
    add('power', [[3.7, 0.12, 4.4], [3.7, 0.12, 2.3]], 0xffd166, { speed: 1.0, radius: 0.03 });
    add('power', [[-4.9, 0.12, 2.6], [1.0, 0.12, 2.6], [1.0, 0.12, -1.4], [2.4, 0.12, -1.4]], 0xffd166, { speed: 1.0, radius: 0.03 });

    const names = { pt: '脈衝管氦氣', water: '冷卻水', mix: '混合氣循環', vac: '真空', rf: '微波 / DC', data: '資料 / 時脈', power: '電力' };
    const on = Object.fromEntries(Object.keys(L).map((k) => [k, true]));
    const row = ui.row();
    const btns = {};
    Object.keys(L).forEach((k) => {
      const b = ui.button(names[k], () => { on[k] = !on[k]; b.classList.toggle('on', on[k]); L[k].forEach((f) => f.show(on[k])); }, row);
      b.classList.add('on'); btns[k] = b;
    });
    const r2 = ui.row();
    ui.button('全部顯示', () => Object.keys(L).forEach((k) => { on[k] = true; btns[k].classList.add('on'); L[k].forEach((f) => f.show(true)); }), r2);
    ui.button('只看冷卻相關', () => Object.keys(L).forEach((k) => { on[k] = ['pt', 'water', 'mix', 'vac'].includes(k); btns[k].classList.toggle('on', on[k]); L[k].forEach((f) => f.show(on[k])); }), r2);
    ui.button('只看訊號相關', () => Object.keys(L).forEach((k) => { on[k] = ['rf', 'data'].includes(k); btns[k].classList.toggle('on', on[k]); L[k].forEach((f) => f.show(on[k])); }), r2);
    const r3 = ui.row();
    ui.button('視角：全景', () => app.orbit.flyTo([10, 11, 17], [-0.5, 1.0, 0]), r3);
    ui.button('視角：冷凍機頂部', () => app.orbit.flyTo([3.5, 6.5, 5.5], [0.3, 3.8, 0]), r3);
    ui.button('視角：機櫃側', () => app.orbit.flyTo([-8, 4, 7], [-4, 1.2, 0]), r3);

    ctx.inset('典型用電分配（kW，示意）', (g, W, H, P) => {
      const cols = ['#5ee08a', '#4fa3ff', '#c58bff', '#38c6d9', '#9fb0c8'];
      App.bars(g, W, H, P, App.PD.power.map(([n, v], i) => [n, v, cols[i]]), { fmt: (v) => v.toFixed(1) + ' kW', l: 128, footer: `合計約 ${App.PD.power.reduce((a, b) => a + b[1], 0).toFixed(0)} kW（依機型與規模而異）` });
    });
    return { update(t, dt) { Object.values(L).flat().forEach((f) => f.update(dt)); } };
  },
});
