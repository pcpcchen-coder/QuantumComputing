/* 場景 7：JJ 製程 — Dolan bridge 雙角度陰影蒸鍍 */
App.register({
  id: 'fab', num: 7, short: 'JJ 製程',
  title: 'JJ 製程：Dolan bridge 雙角度蒸鍍',
  subtitle: '電子束微影 → +θ 蒸鍍 Al → 原位氧化 → −θ 蒸鍍 Al → Lift-off',
  desc: `<p>1. <b>雙層光阻</b>：上層 PMMA 定義圖形，下層 MMA 顯影較快形成<b>底切</b>，於是上層留下一座<b>懸空的光阻橋</b>。</p>
<p>2. <b>第一次斜角蒸鍍</b>（+θ）：Al 原子斜射，「影子」使沉積位置平移。</p>
<p>3. <b>原位氧化</b>：不破真空，通入 O₂，Al 表面長出 1–2 nm AlOx。氧化的<b>壓力 × 時間</b>決定穿隧電阻 R_n，也就決定 I<sub>c</sub> 與 E_J。</p>
<p>4. <b>第二次斜角蒸鍍</b>（−θ）：第二層 Al 往反方向平移，在<b>橋的正下方與第一層重疊</b> → 形成 JJ。</p>
<p>5. <b>Lift-off</b>：溶掉光阻，只留下兩層重疊的鋁線。接面面積約 100 × 200 nm²。</p>`,
  camera: { pos: [7, 6.5, 11], target: [0, 0.2, 0] },
  build(ctx) {
    const { scene, U, THREE, ui, app } = ctx;
    scene.add(U.box(11, 0.4, 6.5, U.mat(0x3a4150, { roughness: 0.85 }), 0, -0.2, 0));
    ctx.label('矽基板', [-4.8, -0.2, 3.3], 'small');
    const hb = 0.8, ht = 0.25, wz = 0.5, xb = 0.25, X0 = 3.2, wzB = 0.65, XB = 3.6;
    const resist = new THREE.Group(); scene.add(resist);
    const pmma = new THREE.MeshStandardMaterial({ color: 0xc58bff, transparent: true, opacity: 0.45, roughness: 0.6, depthWrite: false });
    const mma = new THREE.MeshStandardMaterial({ color: 0x7fb2ff, transparent: true, opacity: 0.22, roughness: 0.6, depthWrite: false });
    const slab = (x0, x1, z0, z1, y0, h, m) => U.box(x1 - x0, h, z1 - z0, m, (x0 + x1) / 2, y0 + h / 2, (z0 + z1) / 2);
    // 上層 PMMA（含懸空橋）
    const yT = hb;
    [slab(-5.5, 5.5, -3.25, -wz / 2, yT, ht, pmma), slab(-5.5, 5.5, wz / 2, 3.25, yT, ht, pmma),
      slab(-5.5, -X0, -wz / 2, wz / 2, yT, ht, pmma), slab(X0, 5.5, -wz / 2, wz / 2, yT, ht, pmma)].forEach((m) => resist.add(m));
    const bridge = slab(-xb, xb, -wz / 2, wz / 2, yT, ht, new THREE.MeshStandardMaterial({ color: 0xe0a0ff, emissive: 0x3a1050, emissiveIntensity: 0.6, transparent: true, opacity: 0.8 }));
    resist.add(bridge);
    // 下層 MMA（底切，開口較寬）
    [slab(-5.5, 5.5, -3.25, -wzB, 0, hb, mma), slab(-5.5, 5.5, wzB, 3.25, 0, hb, mma),
      slab(-5.5, -XB, -wzB, wzB, 0, hb, mma), slab(XB, 5.5, -wzB, wzB, 0, hb, mma)].forEach((m) => resist.add(m));
    // 頂部多餘金屬（lift-off 時移除）
    const topFilm = slab(-5.5, 5.5, -3.25, 3.25, yT + ht, 0.04, U.metal(0xc9d2e0, { transparent: true, opacity: 0 }));
    resist.add(topFilm);
    const lbls = {
      pmma: ctx.label('上層光阻 PMMA', [-3.9, yT + ht + 0.35, -1.6], 'small'),
      mma: ctx.label('下層光阻 MMA（底切）', [-4.2, 0.4, 2.0], 'small'),
      bridge: ctx.label('懸空光阻橋（Dolan bridge）', [0, yT + ht + 0.6, 0], 'gold'),
    };

    // 沉積層
    const s = 0.55, t1 = 0.07, tox = 0.025, t2 = 0.1;
    const al1 = U.metal(0xaeb9c9), al2 = U.metal(0xdfe6f0), oxM = new THREE.MeshStandardMaterial({ color: 0xff7a59, emissive: 0x5a1a00, emissiveIntensity: 0.7, transparent: true, opacity: 0 });
    const clipI = ([a, b]) => [Math.max(a, -XB), Math.min(b, XB)];
    const L1 = [clipI([-X0 + s, -xb + s]), clipI([xb + s, X0 + s])];
    const L2 = [clipI([-X0 - s, -xb - s]), clipI([xb - s, X0 - s])];
    const layer1 = new THREE.Group(), oxide = new THREE.Group(), layer2 = new THREE.Group();
    scene.add(layer1, oxide, layer2);
    L1.forEach(([a, b]) => {
      layer1.add(slab(a, b, -wz / 2, wz / 2, 0, t1, al1));
      oxide.add(slab(a, b, -wz / 2, wz / 2, t1, tox, oxM));
    });
    L2.forEach(([a, b]) => {
      // 依是否疊在第一層上拆段
      const cuts = [a, b]; L1.forEach(([c, d]) => { [c, d].forEach((v) => { if (v > a && v < b) cuts.push(v); }); });
      cuts.sort((p, q) => p - q);
      for (let i = 0; i < cuts.length - 1; i++) {
        const m = (cuts[i] + cuts[i + 1]) / 2;
        const on1 = L1.some(([c, d]) => m > c && m < d);
        const seg = slab(cuts[i], cuts[i + 1], -wz / 2, wz / 2, on1 ? t1 + tox : 0, t2, al2);
        layer2.add(seg);
      }
    });
    layer1.scale.y = 0.001; layer2.scale.y = 0.001;
    // JJ 高亮
    // JJ 高亮：重疊區 = [xb − s, s − xb]
    const jjHi = new THREE.Mesh(new THREE.BoxGeometry(2 * (s - xb), tox + 0.05, wz + 0.04), new THREE.MeshBasicMaterial({ color: 0xffd28a, transparent: true, opacity: 0 }));
    jjHi.position.set(0, t1 + tox / 2, 0);
    scene.add(jjHi);
    const jjLbl = ctx.label('JJ：Al / AlOx / Al 重疊區', [0, 0.9, 0.9], 'gold big'); jjLbl.show(false);
    const leadL = ctx.label('電極 A', [-2.6, 0.5, 0.6], 'q0 small'), leadR = ctx.label('電極 B', [2.6, 0.5, 0.6], 'q1 small');
    leadL.show(false); leadR.show(false);

    // 粒子（Al 原子 / O₂）
    const NP = 170; const atoms = [];
    const aGeo = new THREE.SphereGeometry(0.035, 8, 6);
    const aMat = U.glow(0xe6edf7), oMat = U.glow(0xff8a6a);
    for (let i = 0; i < NP; i++) { const m = new THREE.Mesh(aGeo, aMat); m.visible = false; scene.add(m); atoms.push({ m, v: new THREE.Vector3(), stopY: 0 }); }
    const theta = Math.atan(s / (hb + ht * 0.5));
    const inOpening = (x, z) => Math.abs(z) < wz / 2 && Math.abs(x) < X0 && Math.abs(x) > xb;
    function spawn(p, kind) {
      const dir = kind === 'ox' ? new THREE.Vector3(U.gauss() * 0.1, -1, U.gauss() * 0.1).normalize()
        : new THREE.Vector3(kind === 'e1' ? Math.sin(theta) : -Math.sin(theta), -Math.cos(theta), 0);
      // 目標點（擊中高度 yT+ht 的平面）
      const tx = (Math.random() * 2 - 1) * 4.2, tz = Math.random() < 0.6 ? (Math.random() - 0.5) * wz : (Math.random() - 0.5) * 4;
      const yTop = yT + ht;
      const startY = yTop + 3.2; const tt = (startY - yTop) / -dir.y;
      p.m.position.set(tx - dir.x * tt, startY, tz - dir.z * tt);
      p.v.copy(dir).multiplyScalar(kind === 'ox' ? 2.2 : 4.5);
      p.stopY = inOpening(tx, tz) ? 0.08 : yTop + 0.02;
      p.m.material = kind === 'ox' ? oMat : aMat; p.m.visible = true;
    }

    const STAGES = [
      { t: '① 電子束微影 + 顯影：雙層光阻與懸空橋', dur: 4 },
      { t: '② 第一次斜角蒸鍍 Al（+θ）', dur: 5 },
      { t: '③ 原位氧化：O₂ → AlOx（1–2 nm）', dur: 4 },
      { t: '④ 第二次斜角蒸鍍 Al（−θ）', dur: 5 },
      { t: '⑤ Lift-off：去除光阻 → 留下 JJ', dur: 6 },
    ];
    let stage = 0, st = 0, auto = true;
    const stageLbl = ctx.label('', [0, 2.6, -2.5], 'big teal');
    const r1 = ui.row();
    const btns = STAGES.map((S, i) => ui.button(`${i + 1}`, () => { go(i); auto = false; autoBtn.classList.remove('on'); }, r1));
    const autoBtn = ui.toggle('自動播放', true, (on) => { auto = on; });
    const ro = ui.readout();
    ro.innerHTML = `蒸鍍角 θ ≈ ${Math.round(theta * 180 / Math.PI)}°（影子平移 s = h·tanθ）<br>` + '接面面積 A ≈ 0.02 μm²，R_n ≈ 5–15 kΩ<br>I<sub>c</sub>R_n = πΔ/2e ≈ 280 μV（Ambegaokar–Baratoff）<br>→ I<sub>c</sub> ≈ 20–60 nA，E_J/h ≈ 10–30 GHz';
    function go(i) {
      stage = i; st = 0;
      btns.forEach((b, k) => b.classList.toggle('on', k === i));
      // 設定該階段之前的完成狀態
      layer1.scale.y = i > 1 ? 1 : 0.001; layer1.position.y = 0;
      oxide.children.forEach((m) => (m.material.opacity = i > 2 ? 0.9 : 0));
      layer2.scale.y = i > 3 ? 1 : 0.001;
      resist.position.y = 0; resist.visible = true;
      [...resist.children].forEach((m) => { m.userData.op ??= m.material.opacity; m.material.opacity = m.userData.op; });
      topFilm.material.opacity = i > 1 ? 0.7 : 0;
      jjHi.material.opacity = 0; jjLbl.show(false); leadL.show(false); leadR.show(false);
      Object.values(lbls).forEach((l) => l.show(true));
      atoms.forEach((a) => (a.m.visible = false));
      if (i === 4) app.orbit.flyTo([2.2, 2.4, 4.2], [0, 0.1, 0], 2.5); else if (i === 0) app.orbit.flyTo([7, 6.5, 11], [0, 0.2, 0], 1.5);
    }
    const qs = new URLSearchParams(location.search).get('stage');
    if (qs !== null) { auto = false; autoBtn.classList.remove('on'); go(+qs); } else go(0);

    return {
      update(time, dt) {
        const S = STAGES[stage]; st += dt; const k = Math.min(1, st / S.dur);
        stageLbl.set(S.t);
        if (stage === 0) { resist.children.forEach((m) => { if (m !== topFilm) m.material.opacity = m.userData.op * U.smooth(Math.min(1, st / 1.5)); }); }
        const kind = stage === 1 ? 'e1' : stage === 3 ? 'e2' : stage === 2 ? 'ox' : null;
        if (kind) {
          atoms.forEach((a) => {
            if (!a.m.visible && Math.random() < dt * 6 && k < 0.92) spawn(a, kind);
            if (a.m.visible) { a.m.position.addScaledVector(a.v, dt); if (a.m.position.y <= a.stopY) a.m.visible = false; }
          });
          if (stage === 1) { layer1.scale.y = Math.max(0.001, k); topFilm.material.opacity = 0.7 * k; }
          if (stage === 3) layer2.scale.y = Math.max(0.001, k);
          if (stage === 2) oxide.children.forEach((m) => (m.material.opacity = 0.9 * k));
        } else atoms.forEach((a) => (a.m.visible = false));
        if (stage === 4) {
          const e = U.smooth(Math.min(1, st / 3));
          resist.position.y = e * 3;
          resist.children.forEach((m) => (m.material.opacity = m.userData.op * (1 - e)));
          topFilm.material.opacity = 0.7 * (1 - e);
          if (e >= 1) resist.visible = false;
          Object.values(lbls).forEach((l) => l.show(e < 0.3));
          if (st > 3) { jjHi.material.opacity = 0.35 + 0.35 * Math.sin(time * 5); jjLbl.show(true); leadL.show(true); leadR.show(true); }
        }
        if (auto && st > S.dur + 1.2) go((stage + 1) % STAGES.length);
      },
    };
  },
});
