/* 場景 2：超導與 Cooper pair — 溫度低於 Tc 時電子配對、集體無散射流動 */
App.register({
  id: 'cooper', num: 2, short: 'Cooper pair',
  title: '超導體：Cooper pair 與零電阻',
  subtitle: 'BCS 理論：電子–聲子交互作用 → 電子配對 → 能隙 Δ',
  desc: `<p>電子經過時會吸引帶正電的晶格離子，留下短暫的「正電荷尾跡」（聲子），進而吸引另一顆電子 — 兩顆<b>自旋相反、動量相反</b>的電子形成 <b>Cooper pair</b>。</p>
<p>低於臨界溫度 <b>T<sub>c</sub></b>（鋁約 1.2 K）時，所有 Cooper pair 凝聚為同一個<b>巨觀量子態</b> ψ = √n·e<sup>iφ</sup>，整體同步移動，不再被晶格散射 → <b>直流電阻為零</b>。</p>
<p>拆散一對需要 2Δ 的能量（鋁 2Δ/h ≈ 90 GHz），遠高於量子位元 ~5 GHz 的能量尺度，所以超導電路幾乎無耗散。</p>`,
  camera: { pos: [0, 4.6, 12.5], target: [0, -0.3, 0] },
  build(ctx) {
    const { scene, U, THREE, ui } = ctx;
    const NX = 11, NY = 3, NZ = 4, a = 1;
    const ionMat = U.mat(0xe0a54a, { roughness: 0.35, metalness: 0.4, emissive: 0x3a2400, emissiveIntensity: 0.4 });
    const ions = [];
    const ionGeo = new THREE.SphereGeometry(0.12, 16, 12);
    for (let i = 0; i < NX; i++) for (let j = 0; j < NY; j++) for (let k = 0; k < NZ; k++) {
      const base = new THREE.Vector3((i - (NX - 1) / 2) * a, (j - (NY - 1) / 2) * a, (k - (NZ - 1) / 2) * a);
      const m = new THREE.Mesh(ionGeo, ionMat); m.position.copy(base); scene.add(m);
      ions.push({ m, base, ph: Math.random() * 6.28, f: 4 + Math.random() * 3 });
    }
    // 外框
    const frame = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(NX * a, NY * a + 0.4, NZ * a)),
      new THREE.LineBasicMaterial({ color: 0x5b7aa8, transparent: true, opacity: 0.4 }));
    scene.add(frame);
    const XL = (NX * a) / 2;

    const NP = 10; // 電子對數
    const eGeo = new THREE.SphereGeometry(0.13, 14, 10);
    const eMatUp = U.glow(0x6fb4ff), eMatDn = U.glow(0x9d7bff);
    const pairs = [];
    for (let p = 0; p < NP; p++) {
      const c = new THREE.Vector3((Math.random() * 2 - 1) * XL, (Math.random() - 0.5) * 2, (Math.random() - 0.5) * 3);
      const e1 = new THREE.Mesh(eGeo, eMatUp), e2 = new THREE.Mesh(eGeo, eMatDn);
      const bond = U.dynLine(2, 0x8ef0ff, 0.6);
      scene.add(e1, e2, bond.obj);
      pairs.push({ c, e1, e2, bond, ph: Math.random() * 6.28, axis: new THREE.Vector3(Math.random() - 0.5, Math.random() - 0.5, Math.random() - 0.5).normalize(),
        v1: new THREE.Vector3(1, 0, 0), v2: new THREE.Vector3(1, 0, 0), p1: c.clone(), p2: c.clone().add(new THREE.Vector3(0.9, 0, 0)), flash: 0 });
    }
    const pairLabel = ctx.labelOn(pairs[0].e1, 'Cooper pair（↑↓ 電子對）', [0, 0.45, 0], 'teal small');
    ctx.label('正離子晶格（Al）', [XL - 1, NY / 2 + 0.6, 0], 'gold small');
    const stateLbl = ctx.label('', [0, -NY / 2 - 0.9, NZ / 2], 'big');

    let T = 0.3; const Tc = 1.2;
    const tS = ui.slider('溫度 T (K)', 0.05, 3, 0.05, T, (v) => { T = v; }, (v) => v.toFixed(2) + ' K');
    ui.radio([[0.3, '超導態 0.3 K'], [2.5, '正常態 2.5 K']], 0.3, (v) => tS.set(v));
    const ro = ui.readout();

    ctx.inset('電阻 R 對溫度 T（鋁，Tc ≈ 1.2 K）', (g, W, H, P) => {
      const R = (t) => (t < Tc ? 0 : 1 + 0.08 * (t - Tc));
      const { X, Y } = P.frame(g, W, H, [0, 3], [0, 1.3], { xlabel: '溫度 T (K)', ylabel: '電阻 R（正規化）', xticks: [[0, '0'], [1.2, 'Tc'], [2, '2'], [3, '3']], yticks: [[0, '0'], [1, '1']] });
      P.curve(g, R, 0, 3, X, Y, '#e0a54a', 2.5, 600);
      P.dot(g, X(T), Y(R(T)), 6, '#38c6d9');
    });

    const tmp = new THREE.Vector3();
    return {
      update(time, dt) {
        const sc = T < Tc;
        const frac = sc ? 1 - Math.pow(T / Tc, 4) : 0; // 超流體比例（示意）
        const nPaired = Math.round(frac * NP);
        stateLbl.set(sc ? '超導態：Cooper pair 同步流動，無散射' : '正常態：電子被晶格振動散射 → 有電阻');
        stateLbl.el.style.color = sc ? '#8ef0ff' : '#ffb0b2';
        const vd = 1.4;
        pairs.forEach((p, idx) => {
          const paired = idx < nPaired;
          if (paired) {
            p.c.x += vd * dt; if (p.c.x > XL) p.c.x -= 2 * XL;
            p.ph += dt * 2.2;
            const r = 0.55;
            const perp = new THREE.Vector3(0, Math.cos(p.ph), Math.sin(p.ph)).multiplyScalar(r);
            const along = new THREE.Vector3(Math.sin(p.ph * 0.7) * 0.3, 0, 0);
            p.p1.copy(p.c).add(perp).add(along); p.p2.copy(p.c).sub(perp).sub(along);
            p.bond.obj.visible = true; p.bond.set([[p.p1.x, p.p1.y, p.p1.z], [p.p2.x, p.p2.y, p.p2.z]]);
            p.v1.set(vd, 0, 0); p.v2.set(vd, 0, 0);
          } else {
            p.bond.obj.visible = false;
            [[p.p1, p.v1], [p.p2, p.v2]].forEach(([pos, v]) => {
              // 隨機散射（頻率隨溫度上升）
              if (Math.random() < dt * (2 + 3 * T)) {
                v.set(U.gauss(), U.gauss(), U.gauss()).normalize().multiplyScalar(2.2);
                v.x += 0.6; p.flash = 0.15;
              }
              pos.addScaledVector(v, dt);
              if (pos.x > XL) pos.x -= 2 * XL; if (pos.x < -XL) pos.x += 2 * XL;
              if (Math.abs(pos.y) > NY / 2) { v.y *= -1; pos.y = Math.sign(pos.y) * NY / 2; }
              if (Math.abs(pos.z) > NZ / 2) { v.z *= -1; pos.z = Math.sign(pos.z) * NZ / 2; }
            });
            p.c.copy(p.p1).add(p.p2).multiplyScalar(0.5);
          }
          p.e1.position.copy(p.p1); p.e2.position.copy(p.p2);
        });
        pairLabel.show(nPaired > 0);
        // 離子：熱振動 + 被電子吸引的晶格扭曲（聲子尾跡）
        const amp = 0.02 + 0.05 * T;
        ions.forEach((ion) => {
          tmp.set(Math.sin(time * ion.f + ion.ph), Math.cos(time * ion.f * 1.3 + ion.ph), Math.sin(time * ion.f * 0.8 + 2 * ion.ph)).multiplyScalar(amp);
          ion.m.position.copy(ion.base).add(tmp);
          if (sc) {
            pairs.forEach((p, idx) => {
              if (idx >= nPaired) return;
              const d = p.p1.clone().sub(ion.base); const L2 = d.lengthSq();
              if (L2 < 2.5) ion.m.position.addScaledVector(d, 0.12 * Math.exp(-L2 * 1.2));
            });
          }
        });
        ro.innerHTML = `T / T<sub>c</sub> = ${(T / Tc).toFixed(2)}　配對比例 ≈ ${(frac * 100).toFixed(0)} %<br>${sc ? '能隙 Δ 打開：小擾動無法散射 Cooper pair' : '無能隙：電子與聲子碰撞 → 焦耳熱'}`;
      },
    };
  },
});
