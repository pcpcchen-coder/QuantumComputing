/* 離子阱場景 1：系統全景 — 光學桌、雷射、真空腔、阱、成像、控制電子與設施 */
App.register({
  id: 'ionsys', num: 1, short: '離子阱系統全景',
  title: '離子阱量子電腦：系統全景',
  subtitle: '用電場「抓住」單顆離子，用雷射與微波操作它，再用相機看它發不發光',
  desc: `<p>中央是<b>超高真空腔</b>（&lt; 10⁻¹¹ mbar），裡面有一片<b>表面電極阱晶片</b>，一串離子懸浮在晶片上方約 50–100 μm。周圍的子系統：</p>
<p><span style="color:#b46cff">■</span> <b>雷射</b>（以 ¹⁷¹Yb⁺ 為例）：369 nm 冷卻 / 初始化 / 偵測、935 nm 回泵、399 nm 光游離（裝載）、355 nm 脈衝雷射（Raman 量子閘）。每道光經 <b>AOM</b> 開關與調頻，再經光纖送到真空腔。<br>
<span style="color:#ff5a5f">■</span> <b>RF</b>：RF 源 → 螺旋共振器升壓（約 100–300 V、數十 MHz）→ 阱的 RF 電極，產生囚禁位勢。<br>
<span style="color:#ff9f43">■</span> <b>DC</b>：多通道 DAC（數十到數百通道）→ 分段電極，決定離子位置、搬運離子。<br>
<span style="color:#b388ff">■</span> <b>微波</b>：12.6 GHz 號角，直接驅動量子位元（單位元閘）。<br>
<span style="color:#38c6d9">■</span> <b>資料 / 時脈</b>：FPGA 時序控制（ARTIQ 類）以奈秒精度指揮所有 AOM、DAC、RF；PMT / 相機計數回傳；銣鐘 10 MHz 同步。<br>
<span style="color:#ffd166">■</span> <b>電力</b>、<span style="color:#4fa3ff">■</span> <b>冷卻水</b>：雷射與電子的散熱、恆溫空調（光學桌要 ±0.1 °C 等級）。</p>
<p>數值為代表值，實際依系統而異。</p>`,
  camera: { pos: [1.4, 10.2, 10.6], target: [0.9, 0.9, -1.1] },
  build(ctx) {
    const { scene, U, THREE, ui } = ctx;
    const floor = new THREE.Mesh(new THREE.PlaneGeometry(22, 14), U.mat(0x1a2130, { roughness: 0.95 }));
    floor.rotation.x = -Math.PI / 2; floor.position.set(0.8, 0, -0.8); scene.add(floor);
    App.opticalTable(ctx, { w: 10, d: 5, y: 0.9 });
    const TOP = 0.9;
    const D = (o) => App.device(ctx, o);
    const cat = { laser: [], elec: [], fac: [] };
    const flows = [];
    const F = (key, pts, c, o) => { const f = App.Flow(scene, pts, c, o); flows.push(f); cat[key].push(f); return f; };

    /* ---- 雷射與光路 ---- */
    const lasers = [
      [369, -1.7, '369 nm 冷卻 / 偵測'], [935, -0.85, '935 nm 回泵'], [399, 0.0, '399 nm 光游離'], [355, 0.85, '355 nm 脈衝雷射（Raman 閘）'],
    ];
    const C0 = new THREE.Vector3(1.8, 1.75, 0); // 離子位置（真空腔中心）
    lasers.forEach(([nm, z, name]) => {
      const col = App.wlColor(nm);
      D({ pos: [-4.0, TOP, z], w: 1.0, h: 0.35, d: 0.42, label: name, cls: 'small', labelDy: 0.12, color: 0x2b3446, leds: 2, ledColor: col });
      App.optic(ctx, 'aom', [-2.85, 1.12, z]);
      App.optic(ctx, 'fiber', [-2.1, 1.12, z]);
      cat.laser.push(App.beam(scene, [-3.5, 1.1, z], [-2.95, 1.1, z], col, 0.025, 0.7));
      cat.laser.push(App.beam(scene, [-2.75, 1.1, z], [-2.2, 1.1, z], col, 0.025, 0.7));
    });
    ctx.label('AOM（開關 · 調頻）→ 光纖', [-2.45, 1.35, 1.75], 'small');
    // 光纖到真空腔
    const outs = [[369, -1.7, [0.7, 1.75, -0.35]], [935, -0.85, [0.65, 1.75, 0.0]], [399, 0.0, [0.7, 1.75, 0.35]]];
    outs.forEach(([nm, z, o]) => {
      const col = App.wlColor(nm);
      F('laser', [[-2.0, 1.12, z], [-1.2, 1.05, z], [0.1, 1.05, o[2]], [0.45, 1.75, o[2]], [o[0], o[1], o[2]]], col, { radius: 0.02, speed: 2.2, pipeOpacity: 0.5, dot: 0.03 });
      App.optic(ctx, 'fiber', o);
      cat.laser.push(App.beam(scene, o, C0, col, 0.018, 0.6));
    });
    // 355 nm：兩道交叉 Raman 光束由前方射入
    const col355 = App.wlColor(355);
    F('laser', [[-2.0, 1.12, 0.85], [-1.0, 1.05, 1.7], [1.8, 1.05, 1.7], [1.8, 1.75, 1.7]], col355, { radius: 0.022, speed: 2.2, pipeOpacity: 0.5, dot: 0.03 });
    App.optic(ctx, 'fiber', [1.8, 1.75, 1.7]);
    cat.laser.push(App.beam(scene, [1.8, 1.75, 1.7], [1.35, 1.75, 1.45], col355, 0.02, 0.6));
    cat.laser.push(App.beam(scene, [1.8, 1.75, 1.7], [2.25, 1.75, 1.45], col355, 0.02, 0.6));
    cat.laser.push(App.beam(scene, [1.35, 1.75, 1.45], C0, col355, 0.022, 0.75));
    cat.laser.push(App.beam(scene, [2.25, 1.75, 1.45], C0, col355, 0.022, 0.75));
    ctx.label('兩道 355 nm 交叉 → Raman 閘', [0.1, 1.25, 2.05], 'small');

    /* ---- 真空腔、阱、離子 ---- */
    scene.add(U.box(0.35, 1.4 - TOP, 0.35, U.metal(0x8a93a0), 1.8, (1.4 + TOP) / 2, 0));
    App.chamber(ctx, { pos: [1.8, 1.75, 0], r: 0.85, h: 0.7, pump: false });
    const chip = U.box(0.7, 0.04, 0.35, U.metal(0xc9a24a, { roughness: 0.35 }), 1.8, 1.66, 0); scene.add(chip);
    const ions = [];
    for (let i = 0; i < 5; i++) ions.push(App.particle(scene, App.QC.ion, 0.022, [1.8 + (i - 2) * 0.09, C0.y, 0]));
    ctx.label('超高真空腔（表面電極阱 + 離子鏈）', [3.4, 0.95, 2.15], 'gold');
    // 離子泵
    scene.add(U.tube([[2.5, 1.6, -0.5], [3.1, 1.3, -1.2]], 0.08, U.metal(0xd0d6de)));
    scene.add(U.box(0.55, 0.4, 0.45, U.mat(0x5b6474, { metalness: 0.5 }), 3.2, 1.12, -1.35));
    ctx.label('離子泵 + NEG', [4.3, 1.15, -1.45], 'small');
    // 成像
    const obj = new THREE.Mesh(new THREE.CylinderGeometry(0.17, 0.2, 0.5, 24), U.metal(0x2a2f38)); obj.position.set(1.8, 2.45, 0); scene.add(obj);
    scene.add(U.box(0.45, 0.4, 0.45, U.mat(0x1f2633, { metalness: 0.4 }), 1.8, 3.0, 0));
    ctx.label('成像物鏡 → PMT / 相機', [2.9, 3.05, 0.2], 'small');
    // 磁場線圈（3 對）
    const coilMat = U.metal(0xc98a4b, { roughness: 0.4, transparent: true, opacity: 0.75 });
    const torus = () => new THREE.Mesh(new THREE.TorusGeometry(1.0, 0.035, 8, 48), coilMat);
    [-0.6, 0.6].forEach((d) => {
      const a = torus(); a.position.set(1.8, 1.75, d); scene.add(a);
      const b = torus(); b.rotation.y = Math.PI / 2; b.position.set(1.8 + d, 1.75, 0); scene.add(b);
      const c = torus(); c.rotation.x = Math.PI / 2; c.position.set(1.8, 1.75 + d * 0.75, 0); scene.add(c);
    });
    ctx.label('磁場線圈（3 對，定量子化軸）', [-0.1, 2.15, 0.9], 'small');
    // 螺旋共振器
    const hr = new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.22, 0.7, 24), U.metal(0xc98a4b)); hr.position.set(3.6, 1.25, 0.15); scene.add(hr);
    ctx.label('螺旋共振器（RF 升壓）', [4.75, 1.45, 0.35], 'small');
    // 微波號角
    const horn = new THREE.Mesh(new THREE.ConeGeometry(0.24, 0.5, 4, 1, true), U.metal(0xb7a46a, { side: THREE.DoubleSide }));
    horn.rotation.x = -Math.PI / 2; horn.position.set(1.8, 1.75, -1.25); scene.add(horn);
    ctx.label('微波號角 12.6 GHz', [0.3, 1.35, -1.6], 'small');

    /* ---- 控制電子（後方機櫃） ---- */
    const RZ = -4.6;
    D({ pos: [-5.6, 0, RZ], w: 0.7, h: 1.5, d: 0.7, label: '控制電腦', labelDy: 0.7, leds: 3 });
    D({ pos: [-3.9, 0, RZ], w: 1.0, h: 2.0, d: 0.8, label: 'FPGA 時序控制<br>（ARTIQ 類）', cls: 'teal', leds: 6, ledColor: 0x38c6d9 });
    D({ pos: [-2.4, 0, RZ], w: 0.6, h: 0.9, d: 0.6, label: '銣鐘 10 MHz', labelDy: 0.15, leds: 1, ledColor: 0x9fe8ff });
    D({ pos: [-0.8, 0, RZ], w: 1.0, h: 2.0, d: 0.8, label: 'AOM 驅動<br>DDS', labelDy: 0.7, leds: 5, ledColor: 0xff5a5f });
    D({ pos: [1.0, 0, RZ], w: 1.0, h: 2.0, d: 0.8, label: '多通道 DAC<br>（阱電極 DC）', leds: 6, ledColor: 0xff9f43 });
    D({ pos: [2.8, 0, RZ], w: 0.9, h: 1.6, d: 0.8, label: 'RF 源<br>+ 放大器', labelDy: 1.0, leds: 3, ledColor: 0xff5a5f });
    D({ pos: [4.5, 0, RZ], w: 0.8, h: 1.4, d: 0.8, label: '微波<br>合成器', labelDy: 0.5, leds: 3, ledColor: 0xb388ff });
    /* ---- 設施 ---- */
    D({ pos: [7.0, 0, -3.0], w: 1.0, h: 1.4, d: 0.8, label: 'UPS / 配電盤', color: 0x3a3424, leds: 3, ledColor: 0xffd166 });
    D({ pos: [7.0, 0, 0.6], w: 1.2, h: 1.3, d: 0.9, label: '冷卻水機（雷射散熱）', color: 0x24384f, leds: 2, ledColor: 0x4fa3ff });
    D({ pos: [7.0, 0, 2.9], w: 1.4, h: 0.9, d: 0.6, label: '恆溫空調（±0.1 °C）', leds: 2 });

    /* ---- 電子連線 ---- */
    const DATA = 0x38c6d9, RF = 0xff5a5f, DC = 0xff9f43, MW = 0xb388ff;
    F('elec', [[-3.9, 2.05, RZ], [-3.9, 2.5, RZ], [4.5, 2.5, RZ], [4.5, 1.45, RZ]], DATA, { radius: 0.025, speed: 1.6 });
    F('elec', [[-5.3, 1.0, RZ], [-4.4, 1.0, RZ]], DATA, { radius: 0.025, speed: 1.2 });
    F('elec', [[-2.4, 0.95, RZ + 0.3], [-2.4, 0.95, RZ + 0.55], [-3.9, 0.95, RZ + 0.55], [-3.9, 0.95, RZ + 0.4]], 0x9fe8ff, { radius: 0.02, speed: 1.0 });
    F('elec', [[1.8, 3.2, 0], [1.8, 3.7, 0], [1.8, 3.7, -3.6], [-3.9, 3.7, -3.6], [-3.9, 2.05, -3.95]], DATA, { radius: 0.025, speed: 1.8 });
    ctx.label('光子計數 → FPGA', [-1.0, 3.95, -3.6], 'small');
    [-1.7, -0.85, 0.0, 0.85].forEach((z, i) => F('elec', [[-0.8 + (i - 1.5) * 0.15, 1.0, RZ + 0.4], [-0.8 + (i - 1.5) * 0.15, 1.05, -2.7], [-2.85, 1.05, -2.7], [-2.85, 1.25, z]], RF, { radius: 0.015, speed: 1.2, pipeOpacity: 0.25 }));
    [-0.12, 0, 0.12].forEach((d) => F('elec', [[1.0 + d, 1.9, RZ + 0.4], [1.0 + d, 1.9, -1.4], [1.6 + d, 1.75, -0.75]], DC, { radius: 0.018, speed: 1.0 }));
    F('elec', [[2.8, 1.0, RZ + 0.4], [2.8, 1.05, -2.0], [3.6, 1.05, -0.3], [3.6, 1.05, 0.0]], RF, { radius: 0.03, speed: 1.2 });
    F('elec', [[3.45, 1.45, 0.1], [2.62, 1.72, 0.05]], RF, { radius: 0.03, speed: 1.2 });
    F('elec', [[4.5, 1.0, RZ + 0.4], [4.5, 1.05, -1.9], [1.8, 1.75, -1.9], [1.8, 1.75, -1.5]], MW, { radius: 0.03, speed: 1.4 });
    /* ---- 設施連線 ---- */
    const PW = 0xffd166, W1 = 0x4fa3ff, W2 = 0x9fd0ff;
    F('fac', [[6.5, 0.1, -3.0], [6.1, 0.1, -3.0], [6.1, 0.1, -5.4], [-5.6, 0.1, -5.4], [-5.6, 0.1, RZ - 0.35]], PW, { radius: 0.04 });
    F('fac', [[6.1, 0.12, -3.2], [5.8, 0.12, -3.2], [5.8, 0.12, 2.8], [-4.0, 0.12, 2.8], [-4.0, 0.6, 2.4]], PW, { radius: 0.035 });
    F('fac', [[6.4, 0.35, 0.5], [5.4, 0.35, 0.5], [5.4, 0.35, 3.1], [-4.4, 0.35, 3.1], [-4.4, 0.85, 2.4], [-4.4, 0.85, -1.7]], W1, { radius: 0.04, speed: 1.2 });
    F('fac', [[-3.7, 0.85, -1.7], [-3.7, 0.85, 2.4], [-3.7, 0.5, 3.3], [5.6, 0.5, 3.3], [5.6, 0.5, 0.8], [6.4, 0.5, 0.8]], W2, { radius: 0.04, speed: 1.2 });

    /* ---- 偵測光子 ---- */
    const ph = App.photons(scene, App.wlColor(369), 60, { size: 0.022 });

    /* ---- UI ---- */
    const INFO = {
      all: '<b>全部子系統</b>：雷射與光學、真空與阱、RF/DC/微波電子、FPGA 時序、成像、設施。<br>典型一輪：冷卻 → 初始化 → 閘（雷射或微波）→ 偵測螢光。',
      laser: '<b>雷射</b>：每個波長一台雷射（常需鎖頻到波長計或參考腔），經 AOM 在 μs 內開關、調頻調相，再經光纖送入真空腔。369 nm 同時負責冷卻、初始化與偵測；355 nm 脈衝雷射的兩道光頻差 = 12.6 GHz，做 Raman 閘。',
      elec: '<b>電子訊號</b>：RF（數十 MHz、數百 V）產生囚禁位勢；DAC 控制數十～數百片 DC 電極（搬運離子）；微波直接驅動量子位元；FPGA 以奈秒精度排程所有脈衝，並即時讀取 PMT 光子計數。',
      fac: '<b>設施</b>：沒有稀釋冷凍機；主要負載是雷射、電子與它們的散熱。光學桌與雷射要恆溫（±0.1 °C 等級）、防振；部分系統另有 4–20 K 低溫恆溫器改善真空。',
    };
    const ro = ui.readout();
    let mode = 'all';
    const setMode = (m) => {
      mode = m;
      const vis = { laser: m === 'all' || m === 'laser', elec: m === 'all' || m === 'elec', fac: m === 'all' || m === 'fac' };
      Object.entries(cat).forEach(([k, arr]) => arr.forEach((o) => (o.show ? o.show(vis[k]) : (o.visible = vis[k]))));
      ro.innerHTML = INFO[m];
    };
    ui.radio([['all', '全部'], ['laser', '只看雷射'], ['elec', '只看電子訊號'], ['fac', '只看設施']], 'all', setMode);
    setMode('all');
    ctx.inset('典型用電（示意；Quantinuum Helios 官方 < 40 kW）', (g, W, H, P) => {
      App.bars(g, W, H, P, [['空調 / 冷卻水', 10, '#4fa3ff'], ['雷射與光學', 6, '#b46cff'], ['控制電子（RF/DAC/FPGA）', 5, '#38c6d9'], ['低溫恆溫器（選配）', 7, '#7a8699'], ['真空泵', 0.2, '#e0a54a']],
        { l: 150, max: 12, fmt: (v) => '~' + v + ' kW', footer: '無稀釋冷凍機；雷射與散熱是主要負載' });
    });
    let acc = 0;
    return {
      update(time, dt) {
        flows.forEach((f) => f.update(dt));
        ph.update(dt);
        const lv = mode === 'all' || mode === 'laser';
        ions.forEach((p, i) => p.glow(lv ? 0.6 + 0.4 * Math.sin(time * 6 + i) : 0.2));
        if (lv) {
          acc += dt;
          while (acc > 0.06) {
            acc -= 0.06;
            const p = ions[(Math.random() * 5) | 0].position;
            const up = Math.random() < 0.6;
            ph.emit(p, up ? [U.gauss() * 0.12, 1, U.gauss() * 0.12] : null, 1.6, up ? 0.45 : 0.35);
          }
        }
      },
    };
  },
});
