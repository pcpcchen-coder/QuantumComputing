/* 原子場景 7：中性原子量子電腦系統全景 — 玻璃真空腔、MOT、光鑷（SLM + AOD）、芮德堡雷射、相機、控制電子與設施 */
App.register({
  id: 'atomsys', num: 7, short: '中性原子系統全景',
  title: '中性原子量子電腦：系統全景',
  subtitle: '不需要稀釋冷凍機：原子本身用雷射冷到 μK，被光鑷「夾」在超高真空的玻璃腔裡',
  desc: `<p>一套中性原子系統的核心是<b>光學桌</b>：</p>
<p><b>真空與原子源</b>：Rb 原子源（dispenser）→ 2D MOT → 玻璃真空腔（glass cell，< 10⁻¹¹ mbar）。<br>
<b>MOT</b>：6 道 <span style="color:#ff6060">780 nm</span> 冷卻光 + 反亥姆霍茲線圈，把原子冷到約 10–100 μK。<br>
<b>光鑷</b>：高功率 <span style="color:#d04090">852 / 1064 nm</span> 雷射 → <b>SLM</b>（空間光調變器，產生靜態陣列）+ <b>2D AOD</b>（聲光偏轉器，移動光鑷）→ 高 NA 物鏡 → 腔內原子陣列。<br>
<b>量子操作</b>：<span style="color:#7f5cff">420 nm</span> + <span style="color:#d04090">1013 nm</span> 芮德堡雷射（鎖在 ULE 參考腔）做兩位元閘；6.8 GHz 微波 / Raman 光做單位元閘；局部定址光束選擇個別原子。<br>
<b>讀取</b>：原子螢光經物鏡 → sCMOS / EMCCD 相機。</p>
<p><b>電子與運算</b>：多音 RF 任意波形產生器驅動 AOD、FPGA 即時規劃重排路徑、GPU / 控制電腦。<b>設施</b>：雷射冷卻水、恆溫空調（光路對溫度敏感）、UPS。</p>`,
  camera: { pos: [1.5, 9.0, 10.5], target: [0.8, 0.6, -1.2] },
  build(ctx) {
    const { scene, U, THREE, ui, app } = ctx;
    const floor = new THREE.Mesh(new THREE.PlaneGeometry(22, 16), U.mat(0x1a2130, { roughness: 0.95 }));
    floor.rotation.x = -Math.PI / 2; scene.add(floor);
    const grid = new THREE.GridHelper(22, 22, 0x2b3a55, 0x1f2a3d); grid.position.y = 0.005; scene.add(grid);
    App.opticalTable(ctx, { w: 13, d: 6.4, y: 0.9, pos: [0, 0, 0] });
    const TOP = 0.9, H = 1.6; // 光路高度
    const post = (x, z, y = H) => scene.add(U.box(0.06, y - 0.25 - TOP, 0.06, U.metal(0xc0c6d0), x, TOP + (y - 0.25 - TOP) / 2, z));
    const opt = (type, p, o) => { post(p[0], p[2], p[1]); return App.optic(ctx, type, p, o); };
    const D = (o) => App.device(ctx, o);
    const wl = App.wlColor;

    /* ---- 真空腔與原子源 ---- */
    const cell = new THREE.Mesh(new THREE.BoxGeometry(1.1, 0.7, 0.7), new THREE.MeshStandardMaterial({ color: 0xbfe2ff, transparent: true, opacity: 0.16, roughness: 0.05, metalness: 0.1, depthWrite: false }));
    cell.position.set(0, H, 0); scene.add(cell);
    const edges = new THREE.LineSegments(new THREE.EdgesGeometry(cell.geometry), new THREE.LineBasicMaterial({ color: 0x9cc8ee, transparent: true, opacity: 0.6 }));
    edges.position.copy(cell.position); scene.add(edges);
    ctx.label('玻璃真空腔（glass cell）', [1.5, H + 0.75, 0.4], 'gold');
    const steel = new THREE.Mesh(new THREE.CylinderGeometry(0.42, 0.42, 1.2, 8), U.metal(0xc4ccd6, { roughness: 0.35 }));
    steel.rotation.z = Math.PI / 2; steel.position.set(-1.15, H, 0); scene.add(steel);
    scene.add(U.box(0.5, 0.5, 0.5, U.mat(0x5b6474, { metalness: 0.5 }), -1.5, TOP + 0.25, 0.9));
    scene.add(U.tube([[-1.5, TOP + 0.5, 0.9], [-1.5, H, 0.4]], 0.08, U.metal(0xc4ccd6)));
    ctx.label('離子泵 / NEG', [-1.9, TOP + 0.6, 1.5], 'small');
    const disp = U.box(0.35, 0.35, 0.35, U.mat(0x7a5c3a, { metalness: 0.4 }), -2.0, H, 0); scene.add(disp);
    ctx.label('Rb 原子源 + 2D MOT', [-2.6, H + 0.5, -0.4], 'small');
    [H + 0.5, H - 0.5].forEach((y) => { const c = new THREE.Mesh(new THREE.TorusGeometry(0.42, 0.06, 10, 36), U.metal(0xc98a4b)); c.rotation.x = Math.PI / 2; c.position.set(0, y, 0); scene.add(c); });
    ctx.label('MOT 線圈', [0.95, H - 0.5, 0.6], 'small');
    // 原子陣列（腔內）
    const atoms = [];
    for (let i = 0; i < 6; i++) for (let j = 0; j < 6; j++) {
      const a = U.sphere(0.022, U.glow(0x8ef4ff), (i - 2.5) * 0.07, H + (j - 2.5) * 0.07, 0, 8); scene.add(a); atoms.push(a);
    }

    /* ---- 雷射光路 ---- */
    const beams = [];
    const B = (pts, nm, r = 0.025, op = 0.55) => { for (let k = 0; k < pts.length - 1; k++) beams.push(App.beam(scene, pts[k], pts[k + 1], wl(nm), r, op)); };
    // 光鑷：光纖放大器 → SLM → AOD → 二向色鏡 → 物鏡 → 原子
    D({ pos: [-5.6, TOP, -2.4], w: 1.0, h: 0.5, d: 0.7, label: '光鑷雷射 852/1064 nm<br>（數十 W 光纖放大器）', cls: 'small', color: 0x3a2a40, leds: 2, ledColor: 0xd04090 });
    const slm = U.box(0.12, 0.5, 0.5, U.mat(0x203048, { emissive: 0x3050a0, emissiveIntensity: 0.4 }), -3.6, H, -2.4); scene.add(slm); post(-3.6, -2.4);
    ctx.label('SLM（靜態陣列）', [-3.6, H + 0.55, -2.4], 'small');
    opt('aom', [-2.2, H, -2.4], { label: '2D AOD（移動光鑷）', dy: 0.4 });
    opt('mirror', [0, H, -2.4], { label: '二向色鏡', rot: -Math.PI / 4, dy: 0.42 });
    const obj = new THREE.Mesh(new THREE.CylinderGeometry(0.25, 0.32, 0.8, 24), U.metal(0x2a2f38, { roughness: 0.4 }));
    obj.rotation.x = Math.PI / 2; obj.position.set(0, H, -1.0); scene.add(obj); post(0, -1.0);
    ctx.label('高 NA 物鏡', [-0.8, H + 0.35, -1.0], 'small');
    B([[-5.1, H, -2.4], [-3.6, H, -2.4], [-2.2, H, -2.4], [0, H, -2.4], [0, H, -1.4]], 1064, 0.035, 0.5);
    B([[0, H, -0.6], [0, H, 0]], 1064, 0.012, 0.75);
    // 相機
    D({ pos: [0, TOP, -3.4], w: 0.6, h: 0.45, d: 0.45, label: 'sCMOS / EMCCD 相機', cls: 'small', color: 0x2b3446, leds: 1, ledColor: 0x38c6d9 });
    const fl = App.beam(scene, [0, H, -1.4], [0, H, -3.17], wl(780), 0.02, 0.0);
    // MOT 光束（780 nm，6 道：水平兩組對角 + 垂直）
    D({ pos: [-5.6, TOP, 0.9], w: 1.0, h: 0.45, d: 0.7, label: '冷卻 / 成像雷射 780 nm', cls: 'small', color: 0x402828, leds: 2, ledColor: 0xff4040 });
    const mot = [];
    [[1, 0, 1], [1, 0, -1], [0, 1, 0]].forEach((d) => {
      const v = new THREE.Vector3(...d).normalize().multiplyScalar(1.1);
      const c = new THREE.Vector3(0, H, 0);
      mot.push(App.beam(scene, c.clone().sub(v), c.clone().add(v), wl(780), 0.09, 0.18));
    });
    // 芮德堡雷射 420 + 1013（對打）
    D({ pos: [4.9, TOP, -2.4], w: 1.0, h: 0.45, d: 0.7, label: '芮德堡雷射 420 nm', cls: 'small', color: 0x30284a, leds: 2, ledColor: 0x7f5cff });
    D({ pos: [-4.4, TOP, 2.4], w: 1.0, h: 0.45, d: 0.7, label: '芮德堡雷射 1013 nm', cls: 'small', color: 0x3a2a40, leds: 2, ledColor: 0xd04090 });
    D({ pos: [5.6, TOP, 0.3], w: 0.7, h: 0.5, d: 0.9, label: 'ULE 參考腔（窄線寬鎖頻）', cls: 'small', color: 0x3a4250, leds: 1, ledColor: 0xe0a54a });
    opt('mirror', [2.6, H, -2.4], { rot: Math.PI / 4 });
    opt('mirror', [-2.6, H, 2.4], { rot: Math.PI / 4 });
    B([[4.4, H, -2.4], [2.6, H, -2.4], [2.6, H, 0], [0.4, H, 0]], 420, 0.02, 0.7);
    B([[-3.9, H, 2.4], [-2.6, H, 2.4], [-2.6, H, 0], [-0.4, H, 0]], 1013, 0.02, 0.6);
    // Raman / 局部定址
    D({ pos: [3.6, TOP, 2.4], w: 1.0, h: 0.45, d: 0.7, label: 'Raman / 局部定址雷射 + AOD', cls: 'small', color: 0x2a3440, leds: 2, ledColor: 0xff8a3d });
    opt('mirror', [1.6, H, 2.4], { rot: -Math.PI / 4 });
    B([[3.1, H, 2.4], [1.6, H, 2.4], [0.05, H + 0.05, 0.05]], 795, 0.015, 0.6);
    // 微波號角
    const horn = new THREE.Mesh(new THREE.ConeGeometry(0.22, 0.5, 4, 1, true), U.metal(0xd4a050, { side: THREE.DoubleSide }));
    horn.position.set(1.3, H + 0.75, 0.9); horn.lookAt(0, H, 0); horn.rotateX(Math.PI / 2); scene.add(horn);
    ctx.label('6.8 GHz 微波號角', [2.0, H + 0.95, 1.1], 'small');
    const laserBeams = [...beams, ...mot];

    /* ---- 機櫃與設施（地面） ---- */
    D({ pos: [-4.5, 0, -5.3], w: 1.0, h: 2.0, d: 0.8, label: '雷射控制 / 鎖頻', cls: 'small', labelDy: 0.15, leds: 5, ledColor: 0xff8a3d });
    D({ pos: [-2.6, 0, -5.3], w: 1.0, h: 2.0, d: 0.8, label: '多音 RF AWG<br>（驅動 AOD）', cls: 'teal small', labelDy: 0.35, leds: 6, ledColor: 0x38c6d9 });
    D({ pos: [-0.7, 0, -5.3], w: 1.0, h: 2.0, d: 0.8, label: 'FPGA<br>（即時重排）', cls: 'teal small', labelDy: 0.15, leds: 6, ledColor: 0x38c6d9 });
    D({ pos: [1.2, 0, -5.3], w: 1.0, h: 2.0, d: 0.8, label: 'GPU / 控制電腦', cls: 'teal small', labelDy: 0.35, leds: 4, ledColor: 0x38c6d9 });
    D({ pos: [3.3, 0, -5.3], w: 1.0, h: 1.4, d: 0.8, label: '微波源 / 線圈電源', cls: 'small', leds: 3, ledColor: 0xe0a54a });
    D({ pos: [8.6, 0, -4.6], w: 1.2, h: 1.3, d: 0.9, label: '冷卻水機（雷射）', color: 0x24384f, leds: 2, ledColor: 0x4fa3ff });
    D({ pos: [8.6, 0, -1.9], w: 1.0, h: 1.4, d: 0.8, label: 'UPS + 配電', color: 0x3a3424, leds: 2, ledColor: 0xffd166 });
    D({ pos: [8.6, 0, 0.9], w: 1.6, h: 0.9, d: 0.7, label: '恆溫空調（±0.1 °C）', color: 0x2b3446, leds: 2 });

    const L = {};
    const add = (key, pts, color, o = {}) => { (L[key] ||= []).push(App.Flow(scene, pts, color, o)); };
    // RF：AWG → AOD；微波源 → 號角；線圈電源 → 線圈
    add('rf', [[-2.6, 2.0, -4.9], [-2.6, 2.4, -3.6], [-2.2, 2.0, -2.4], [-2.2, H + 0.1, -2.4]], 0xff9f43, { speed: 1.4, radius: 0.025 });
    add('rf', [[3.3, 1.4, -4.9], [3.3, 2.6, -1.0], [1.4, 2.6, 0.6], [1.3, H + 0.75, 0.9]], 0xff9f43, { speed: 1.4, radius: 0.025 });
    add('rf', [[3.0, 1.0, -4.9], [3.0, TOP + 0.05, -3.2], [0.6, TOP + 0.05, -0.6], [0.4, H - 0.5, 0]], 0xd9c39a, { speed: 1.0, radius: 0.02 });
    // 資料：相機 → FPGA → AWG；電腦 ⇄ FPGA；鎖頻
    add('data', [[0, TOP + 0.3, -3.65], [0, TOP + 0.3, -4.5], [-0.7, 1.3, -4.9]], 0x38c6d9, { speed: 1.6, radius: 0.025 });
    add('data', [[-0.7, 1.7, -4.9], [-1.6, 2.2, -4.9], [-2.6, 1.7, -4.9]], 0x38c6d9, { speed: 1.6, radius: 0.025 });
    add('data', [[1.2, 1.5, -4.9], [0.3, 1.9, -4.9], [-0.7, 1.5, -4.9]], 0x38c6d9, { speed: 1.6, radius: 0.02 });
    add('data', [[5.6, TOP + 0.5, 0.3], [5.0, TOP + 0.5, -1.0], [4.9, TOP + 0.45, -2.05]], 0xe0a54a, { speed: 1.0, radius: 0.02 });
    add('data', [[5.6, TOP + 0.5, 0.75], [5.6, TOP + 0.08, 3.1], [-4.4, TOP + 0.08, 3.1], [-4.4, TOP + 0.45, 2.75]], 0xe0a54a, { speed: 1.0, radius: 0.02 });
    add('data', [[-4.5, 1.6, -4.9], [-5.6, 1.6, -3.4], [-5.6, TOP + 0.45, -2.75]], 0xe0a54a, { speed: 1.0, radius: 0.02 });
    // 電力
    add('power', [[8.1, 0.08, -1.9], [7.2, 0.08, -1.9], [7.2, 0.08, -6.3], [-4.5, 0.08, -6.3], [-4.5, 0.08, -5.7]], 0xffd166, { speed: 1.0, radius: 0.03 });
    [-2.6, -0.7, 1.2, 3.3].forEach((x) => add('power', [[x, 0.1, -6.3], [x, 0.1, -5.7]], 0xffd166, { speed: 1.0, radius: 0.025 }));
    add('power', [[8.6, 0.12, -1.5], [8.6, 0.12, 0.55]], 0xffd166, { speed: 1.0, radius: 0.025 });
    // 冷卻水：冷卻水機 → 雷射（光纖放大器、芮德堡）
    add('water', [[8.0, 0.25, -4.6], [6.9, 0.25, -4.6], [6.9, 0.25, -4.0], [-6.6, 0.25, -4.0], [-6.6, 0.6, -2.4], [-6.1, TOP + 0.2, -2.4]], 0x4fa3ff, { speed: 1.2, radius: 0.04 });
    add('water', [[8.0, 0.35, -4.3], [6.6, 0.35, -4.3], [6.6, 0.6, -2.4], [5.4, TOP + 0.2, -2.4]], 0x4fa3ff, { speed: 1.2, radius: 0.035 });

    let mode = 'all';
    const apply = () => {
      const vis = { laser: mode === 'all' || mode === 'laser', rf: mode === 'all' || mode === 'elec', data: mode === 'all' || mode === 'elec', power: mode === 'all' || mode === 'fac', water: mode === 'all' || mode === 'fac' };
      laserBeams.forEach((b) => (b.visible = vis.laser));
      fl.visible = vis.laser;
      Object.entries(L).forEach(([k, arr]) => arr.forEach((f) => f.show(vis[k])));
      ro.innerHTML = {
        all: '全部連接：雷射光路（彩色光束）、RF / 微波（橘）、資料 / 鎖頻（青、金）、電力（黃）、冷卻水（藍）',
        laser: '<b>雷射</b>：780 nm 冷卻與成像、852/1064 nm 光鑷、420 + 1013 nm 芮德堡、Raman / 局部定址。<br>同一顆原子要被 5–7 種波長的雷射照射，全部要鎖頻、對準、功率穩定。',
        elec: '<b>電子訊號</b>：AWG 產生多音 RF 驅動 AOD（每個頻率 = 一支移動光鑷）；相機影像 → FPGA 算出重排路徑 → AWG（毫秒內完成）；微波源驅動 6.8 GHz 號角；雷射鎖頻迴路。',
        fac: '<b>設施</b>：沒有稀釋冷凍機與氦壓縮機；主要負載是雷射（含光纖放大器）與其冷卻水、恆溫空調、控制電子。光路對溫度與振動敏感 → 空調穩定度與防振桌很重要。',
      }[mode];
    };
    ui.radio([['all', '全部'], ['laser', '只看雷射'], ['elec', '只看電子訊號'], ['fac', '只看設施']], 'all', (v) => { mode = v; apply(); });
    const r3 = ui.row();
    ui.button('視角：全景', () => app.orbit.flyTo([1.8, 10.2, 12.0], [1.2, 0.6, -1.4]), r3);
    ui.button('視角：真空腔特寫', () => app.orbit.flyTo([2.6, 3.0, 3.4], [0, H, 0]), r3);
    ui.button('視角：機櫃側', () => app.orbit.flyTo([2, 5, 3], [-0.5, 1.0, -5.3]), r3);
    const ro = ui.readout();
    apply();

    ctx.inset('典型用電分配（kW，示意，非官方數字）', (g, W, H2, P) => {
      const items = [['雷射（含光纖放大器）', 3.0, '#d04090'], ['雷射冷卻水機', 2.5, '#4fa3ff'], ['控制電子 / FPGA / GPU', 2.5, '#38c6d9'], ['真空、線圈、微波', 0.6, '#9fb0c8'], ['恆溫空調（機房分攤）', 2.0, '#e0a54a']];
      App.bars(g, W, H2, P, items, { fmt: (v) => v.toFixed(1) + ' kW', l: 140, footer: '合計約 10 kW 等級；不需稀釋冷凍機（依系統而異）' });
    });

    return {
      update(t, dt) {
        Object.values(L).flat().forEach((f) => f.update(dt));
        atoms.forEach((a, i) => { a.material.color.setHSL(0.52, 0.9, 0.55 + 0.25 * Math.sin(t * 3 + i)); });
        mot.forEach((b, i) => { if (b.visible) b.material.opacity = 0.12 + 0.06 * Math.sin(t * 2 + i); });
        if (fl.visible) fl.material.opacity = 0.25 + 0.2 * Math.max(0, Math.sin(t * 1.5));
      },
    };
  },
});
