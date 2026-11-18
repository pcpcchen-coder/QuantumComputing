/* 原子場景 15：分區架構（儲存區 / 糾纏區 / 讀取區）與並行 CZ 閘 */
App.register({
  id: 'zoned', num: 14, short: '分區架構與並行閘',
  title: '分區架構：搬運原子 → 並行糾纏 → 中途量測',
  subtitle: '連接性由「移動」決定：AOD 整排抓起原子送進糾纏區，一道全域芮德堡雷射同時完成所有 CZ',
  desc: `<p>大型中性原子處理器把晶片分成三個區域：</p>
<p><b>儲存區</b>：大多數原子在這裡等待，不受芮德堡雷射照射，保持相干。<br>
<b>糾纏區</b>：成對的光鑷位置。被送進來的原子兩兩靠近（< R_b），<b>一道全域芮德堡脈衝</b>同時對所有對做 CZ。<br>
<b>讀取區</b>：把要量測的原子（例如錯誤更正的輔助位元）搬到這裡成像，避免螢光干擾其他原子。</p>
<p><b>搬運</b>：AOD 用多個 RF 頻率產生一整排移動光鑷，整列（或整個子陣列）平移，原子在搬運中<b>保持量子態</b>。因為可以把任意兩顆原子搬到一起，連接性不受固定佈線限制。</p>
<p>顏色代表 4 個<b>邏輯位元</b>區塊。把兩個區塊對應位置的原子一對一做 CZ，就是<b>橫向（transversal）邏輯閘</b>，一層就完成。Bluvstein et al., Nature 2024（Harvard / MIT / QuEra）用這種架構以 280 顆原子操作最多 48 個邏輯位元。</p>
<p>代價是<b>速度</b>：搬運約數百 μs，CZ 本身只要約 0.3 μs。</p>`,
  camera: { pos: [0.4, 7.2, 6.6], target: [0, -0.4, 0.3] },
  build(ctx) {
    const { scene, U, THREE, ui } = ctx;
    const COLS = 8, ROWS = 4;
    const BCOL = [0x38d6e9, 0xffc04a, 0x5ee08a, 0xc58bff];
    const xs = (i) => -3.5 + i * 1.0;
    const zStore = (j) => -3.0 + j * 0.6, zEnt = 1.3, zRead = 3.3;
    // 區域底板
    const zone = (z0, z1, col, name) => {
      const m = new THREE.Mesh(new THREE.PlaneGeometry(8.8, z1 - z0), new THREE.MeshBasicMaterial({ color: col, transparent: true, opacity: 0.12, depthWrite: false }));
      m.rotation.x = -Math.PI / 2; m.position.set(0, -0.12, (z0 + z1) / 2); scene.add(m);
      scene.add(U.line([[-4.4, -0.11, z0], [4.4, -0.11, z0], [4.4, -0.11, z1], [-4.4, -0.11, z1], [-4.4, -0.11, z0]], col, 0.6));
      ctx.label(name, [-5.4, 0, (z0 + z1) / 2], 'small');
      return m;
    };
    zone(-3.35, -0.85, 0x4f8cff, '儲存區');
    const entZone = zone(0.75, 1.85, 0xff6ad5, '糾纏區');
    zone(2.8, 3.8, 0x38c6d9, '讀取區');
    // 糾纏區成對光鑷位置、讀取區位置
    for (let i = 0; i < COLS; i++) {
      [-0.16, 0.16].forEach((dx) => { const r = new THREE.Mesh(new THREE.TorusGeometry(0.1, 0.01, 6, 20), U.glow(0xff6ad5, 0.5)); r.rotation.x = Math.PI / 2; r.position.set(xs(i) + dx, -0.05, zEnt); scene.add(r); });
      const r2 = new THREE.Mesh(new THREE.TorusGeometry(0.1, 0.01, 6, 20), U.glow(0x38c6d9, 0.5)); r2.rotation.x = Math.PI / 2; r2.position.set(xs(i), -0.05, zRead); scene.add(r2);
    }
    // 芮德堡全域光片
    const sheet = new THREE.Mesh(new THREE.BoxGeometry(8.6, 0.35, 0.9), new THREE.MeshBasicMaterial({ color: 0xff6ad5, transparent: true, opacity: 0, depthWrite: false, blending: THREE.AdditiveBlending }));
    sheet.position.set(0, 0, zEnt); scene.add(sheet);
    const readGlow = new THREE.Mesh(new THREE.BoxGeometry(8.6, 0.3, 0.8), new THREE.MeshBasicMaterial({ color: 0x38c6d9, transparent: true, opacity: 0, depthWrite: false, blending: THREE.AdditiveBlending }));
    readGlow.position.set(0, 0, zRead); scene.add(readGlow);

    // 原子
    const geo = new THREE.SphereGeometry(0.11, 16, 10);
    const atoms = [];
    for (let j = 0; j < ROWS; j++) for (let i = 0; i < COLS; i++) {
      const b = (j < 2 ? 0 : 2) + (i < 4 ? 0 : 1);
      const m = new THREE.Mesh(geo, U.mat(BCOL[b], { emissive: BCOL[b], emissiveIntensity: 0.5 }));
      const home = new THREE.Vector3(xs(i), 0, zStore(j)); m.position.copy(home); scene.add(m);
      atoms.push({ i, j, b, m, home, from: home.clone(), to: home.clone() });
    }
    const at = (i, j) => atoms[j * COLS + i];
    ['邏輯位元 A', '邏輯位元 B', '邏輯位元 C', '邏輯位元 D'].forEach((n, b) => ctx.label(n, [b % 2 ? 2.0 : -2.0, 0.35, b < 2 ? -3.75 : -1.95 + 1.55], 'small'));
    // AOD 光錐
    const coneGeo = new THREE.ConeGeometry(0.13, 1.2, 14, 1, true);
    const cones = atoms.map(() => { const c = new THREE.Mesh(coneGeo, new THREE.MeshBasicMaterial({ color: 0xff4fd8, transparent: true, opacity: 0.35, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide })); c.rotation.x = Math.PI; c.visible = false; scene.add(c); return c; });
    const links = []; for (let i = 0; i < COLS; i++) { const l = U.dynLine(2, 0xffffff); l.obj.visible = false; scene.add(l.obj); links.push(l); }
    const ph = App.photons(scene, 0x8ef4ff, 120, { size: 0.025 });

    const LAYERS = [[0, 2, '橫向 CZ：A⊗C、B⊗D'], [1, 3, '橫向 CZ：A⊗C、B⊗D'], [0, 1, '區塊內 CZ（A、B 內部）'], [2, 3, '區塊內 CZ（C、D 內部）']];
    let li = 0, npairs = 6, step = null, stepT = 0, sel = [], nLayers = 0, nCZ = 0, info = '按「▶ 執行一層」';
    const seqLayer = () => {
      const [ra, rb, name] = LAYERS[li % LAYERS.length]; li++;
      sel = [];
      for (let i = 0; i < npairs; i++) { const a = at(i, ra), b = at(i, rb); a.to = new THREE.Vector3(xs(i) - 0.16, 0, zEnt); b.to = new THREE.Vector3(xs(i) + 0.16, 0, zEnt); sel.push(a, b); }
      return [
        { k: 'pick', d: 0.6, msg: `AOD 抓起第 ${ra + 1}、${rb + 1} 列的前 ${npairs} 顆原子` },
        { k: 'move', d: 1.6, msg: '整排平移到糾纏區（原子保持相干，約 100–500 μs）' },
        { k: 'gate', d: 1.6, msg: `全域芮德堡脈衝：${npairs} 對同時做 CZ（約 0.3 μs）— ${name}` },
        { k: 'back', d: 1.6, msg: '搬回儲存區' },
      ];
    };
    const seqMeasure = () => {
      sel = []; const j = 3;
      for (let i = 0; i < npairs; i++) { const a = at(i, j); a.to = new THREE.Vector3(xs(i), 0, zRead); sel.push(a); }
      return [
        { k: 'pick', d: 0.6, msg: `抓起第 4 列（例如錯誤更正的輔助位元）` },
        { k: 'move', d: 1.8, msg: '搬到讀取區，遠離其他原子' },
        { k: 'read', d: 3.0, msg: '螢光成像（約 1–10 ms），不干擾儲存區的原子' },
        { k: 'refill', d: 1.2, msg: '量測後的原子已加熱 / 丟失 → 從儲備位置補充新原子' },
      ];
    };
    let queue = [];
    const start = (seq) => { if (queue.length || step) return; queue = seq; };

    ui.button('▶ 執行一層', () => start(seqLayer()));
    ui.button('中途量測', () => start(seqMeasure()));
    ui.button('重置', () => { queue = []; step = null; atoms.forEach((a) => { a.m.position.copy(a.home); a.m.visible = true; a.m.scale.setScalar(1); }); cones.forEach((c) => (c.visible = false)); links.forEach((l) => (l.obj.visible = false)); nLayers = 0; nCZ = 0; li = 0; info = '按「▶ 執行一層」'; });
    ui.slider('並行對數', 2, 8, 1, npairs, (v) => { npairs = v; }, (v) => `${v} 對`);
    const ro = ui.readout();

    ctx.inset('一層的時間組成（代表值）', (g, W, H, P) => {
      App.bars(g, W, H, P, [['抓取 + 搬運', 250, '#ff4fd8'], ['芮德堡 CZ（並行）', 0.3, '#ff6ad5'], ['搬回', 250, '#c58bff'], ['中途讀取（選用）', 1000, '#38c6d9']], { fmt: (v) => (v < 1 ? v + ' μs' : v >= 1000 ? (v / 1000) + ' ms' : v + ' μs'), l: 130, max: 1150, footer: '閘本身只佔極小比例；整體速度由搬運與讀取決定' });
    });

    return {
      update(t, dt) {
        if (!step && queue.length) { step = queue.shift(); stepT = 0; info = step.msg; sel.forEach((a) => (a.from = a.m.position.clone())); }
        if (step) {
          stepT += dt; const u = U.clamp(stepT / step.d, 0, 1), e = U.smooth(u);
          if (step.k === 'pick') sel.forEach((a) => { const c = cones[atoms.indexOf(a)]; c.visible = true; c.position.copy(a.m.position).add(new THREE.Vector3(0, 0.6, 0)); c.material.opacity = 0.35 * e; });
          if (step.k === 'move') sel.forEach((a) => { a.m.position.lerpVectors(a.from, a.to, e); cones[atoms.indexOf(a)].position.copy(a.m.position).add(new THREE.Vector3(0, 0.6, 0)); });
          if (step.k === 'gate') {
            cones.forEach((c) => (c.visible = false));
            sheet.material.opacity = 0.45 * Math.sin(Math.PI * u);
            for (let k = 0; k < sel.length / 2; k++) { const a = sel[2 * k], b = sel[2 * k + 1]; links[k].obj.visible = true; links[k].set([a.m.position.toArray(), b.m.position.toArray()]); links[k].obj.material.opacity = 1; }
            sel.forEach((a) => a.m.scale.setScalar(1 + 0.5 * Math.sin(Math.PI * u)));
          }
          if (step.k === 'back') {
            sheet.material.opacity = 0; links.forEach((l) => (l.obj.visible = false));
            sel.forEach((a) => { const c = cones[atoms.indexOf(a)]; c.visible = true; a.m.position.lerpVectors(a.from, a.home, e); c.position.copy(a.m.position).add(new THREE.Vector3(0, 0.6, 0)); });
          }
          if (step.k === 'read') {
            cones.forEach((c) => (c.visible = false));
            readGlow.material.opacity = 0.35 * Math.sin(Math.PI * u);
            if (Math.random() < 0.7) { const a = sel[Math.floor(Math.random() * sel.length)]; ph.emit(a.m.position, [U.gauss() * 0.3, 1, U.gauss() * 0.3], 2.5, 0.8); }
          }
          if (step.k === 'refill') {
            readGlow.material.opacity = 0;
            sel.forEach((a) => { if (u < 0.5) { a.m.scale.setScalar(Math.max(0.01, 1 - 2 * u)); } else { a.m.position.copy(a.home); a.m.scale.setScalar(Math.max(0.01, 2 * u - 1)); } });
          }
          if (u >= 1) {
            if (step.k === 'gate') { nCZ += sel.length / 2; sel.forEach((a) => a.m.scale.setScalar(1)); }
            if (step.k === 'back') { nLayers++; cones.forEach((c) => (c.visible = false)); }
            if (step.k === 'refill') { sel.forEach((a) => { a.m.position.copy(a.home); a.m.scale.setScalar(1); }); }
            step = null;
            if (!queue.length) info = '完成。可再執行下一層（四種配對輪流）';
          }
        }
        ph.update(dt);
        ro.innerHTML = `${info}<br>已執行 ${nLayers} 層 · 累計 ${nCZ} 個 CZ（每層只需一道芮德堡脈衝）`;
      },
    };
  },
});
