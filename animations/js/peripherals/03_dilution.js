/* 周邊場景 3：稀釋冷凍單元 — ³He 在相分界面「溶入」⁴He 而吸熱 */
App.register({
  id: 'dilution', num: 3, short: '稀釋冷凍原理',
  title: '稀釋冷凍：從 4 K 到 10 mK',
  subtitle: '³He/⁴He 混合液在 0.87 K 以下相分離；³He 越過相界面時吸熱',
  desc: `<p>脈衝管只能到約 3 K。要再往下，靠的是 <b>³He/⁴He 混合液</b>：低於 0.87 K 時分成兩相 —— 上層<b>濃 ³He 相</b>、下層<b>稀相</b>（約 6.6 % ³He 溶在超流 ⁴He 中）。</p>
<p>③ 在 <b>Still</b>（~0.8 K）加熱，³He 比 ⁴He 更容易蒸發，被室溫的泵抽走 → 稀相中的 ³He 減少。<br>
④ <b>混合腔（MXC）</b>中的 ³He 便從濃相「溶入」稀相補充 —— 這像蒸發一樣需要能量，<b>從周圍吸熱</b>。<br>
① 被抽出的 ³He 經 <b>GHS</b> 淨化後送回，② 在 4 K 凝結、經流阻與<b>熱交換器</b>由回流的冷稀相預冷，再回到混合腔。</p>
<p>冷卻功率 <span class="eq">Q̇ ≈ 84 ṅ T²</span>（W；ṅ：³He 循環率 mol/s）。溫度越低，冷卻功率以 T² 下降。</p>
<p><b>量子晶片在哪？</b>不在混合腔裡。晶片裝在<b>樣品盒</b>內，經<b>銅支架</b>鎖在 <b>MXC 板</b>下方，外面套紅外與磁屏蔽；熱量經固體傳導：晶片 → 樣品盒 → 支架 → MXC 板 → 混合液（橘色粒子）。</p>`,
  camera: { pos: [9.5, 5.0, 16.5], target: [0, 3.2, 0] },
  build(ctx) {
    const { scene, U, THREE, ui } = ctx;
    const glassMat = (c, op = 0.2) => new THREE.MeshStandardMaterial({ color: c, transparent: true, opacity: op, side: THREE.DoubleSide, depthWrite: false, roughness: 0.3 });
    // 4 K 板與各級板（示意）
    const plate = (y, r, name) => { const m = new THREE.Mesh(new THREE.CylinderGeometry(r, r, 0.08, 40), U.metal(0xc98a4b, { transparent: true, opacity: 0.55 })); m.position.y = y; scene.add(m); ctx.label(name, [-r - 0.9, y, 0], 'small'); };
    plate(7.2, 1.6, '4 K 板'); plate(5.9, 1.4, 'Still 板'); plate(3.9, 1.25, 'Cold plate'); plate(-0.15, 1.1, 'MXC 板');
    // Still
    const still = new THREE.Mesh(new THREE.CylinderGeometry(0.75, 0.75, 1.2, 32, 1, true), glassMat(0x9fb7e0, 0.25)); still.position.set(0, 5.2, 0); scene.add(still);
    const stillLiq = new THREE.Mesh(new THREE.CylinderGeometry(0.72, 0.72, 0.5, 32), glassMat(0x4f8cff, 0.35)); stillLiq.position.set(0, 4.85, 0); scene.add(stillLiq);
    const heater = new THREE.Mesh(new THREE.TorusGeometry(0.5, 0.04, 8, 40), new THREE.MeshStandardMaterial({ color: 0xff7a59, emissive: 0xff5a2a, emissiveIntensity: 0.8 })); heater.rotation.x = Math.PI / 2; heater.position.set(0, 4.75, 0); scene.add(heater);
    ctx.label('③ Still ~0.8 K<br>加熱 → ³He 優先蒸發', [1.9, 5.3, 0], 'teal');
    // 混合腔
    const mxc = new THREE.Mesh(new THREE.CylinderGeometry(0.9, 0.9, 1.3, 36, 1, true), glassMat(0x9fb7e0, 0.25)); mxc.position.set(0, 0.6, 0); scene.add(mxc);
    const conc = new THREE.Mesh(new THREE.CylinderGeometry(0.87, 0.87, 0.35, 36), glassMat(0x8ef0ff, 0.35)); conc.position.set(0, 1.0, 0); scene.add(conc);
    const dil = new THREE.Mesh(new THREE.CylinderGeometry(0.87, 0.87, 0.85, 36), glassMat(0x3b6fd8, 0.3)); dil.position.set(0, 0.4, 0); scene.add(dil);
    const bnd = new THREE.Mesh(new THREE.CylinderGeometry(0.88, 0.88, 0.02, 36), new THREE.MeshBasicMaterial({ color: 0xffd28a, transparent: true, opacity: 0.8 })); bnd.position.set(0, 0.83, 0); scene.add(bnd);
    ctx.label('④ 混合腔 MXC ~10 mK', [2.1, 0.9, 0], 'gold');
    ctx.label('濃 ³He 相', [-1.6, 1.05, 0.4], 'small'); ctx.label('相界面：³He 溶入 → 吸熱', [0, 1.55, 0.95], 'gold small'); ctx.label('稀相（6.6 % ³He 溶於超流 ⁴He）', [-1.0, 0.25, 1.0], 'small');
    // 熱交換器（螺旋）
    const helix = []; for (let i = 0; i <= 260; i++) { const a = i * 0.16; helix.push([0.42 * Math.cos(a), 4.3 - (i / 260) * 2.6, 0.42 * Math.sin(a)]); }
    scene.add(U.smoothTube(helix, 0.05, U.metal(0xd8dee8), false, 600));
    for (let k = 0; k < 4; k++) scene.add(U.box(0.9, 0.1, 0.9, U.metal(0xb87333, { transparent: true, opacity: 0.45 }), 0, 1.45 + 0.17 * k, 0));
    ctx.label('② 熱交換器（連續 + 階梯式）', [1.9, 3.0, 0], 'small');
    // 流阻
    const imp = []; for (let i = 0; i <= 80; i++) { const a = i * 0.5; imp.push([-1.0 + 0.15 * Math.cos(a), 6.6 - i * 0.006, 0.15 * Math.sin(a)]); } scene.add(U.smoothTube(imp, 0.025, U.metal(0xe0a54a), false, 200));
    ctx.label('流阻（維持凝結壓力）', [-2.4, 6.5, 0], 'small');

    // ³He 循環路徑：室溫回流 → 4K 凝結 → 流阻 → 熱交換 → MXC 濃相 → 越過界面 → 稀相 → 經熱交換回 Still → 蒸發 → 抽氣
    const path = [
      [-1.0, 9.0, 0], [-1.0, 7.2, 0], [-1.0, 6.2, 0], [-1.0, 5.0, 0.6], [-0.5, 4.3, 0.42], [-0.42, 2.0, 0.2], [-0.3, 1.4, 0.2], [-0.3, 1.05, 0.2], // 往下到濃相
      [-0.1, 0.84, 0.1], // 越界面
      [0.2, 0.4, 0.0], [0.5, 0.2, -0.2], [0.55, 1.3, -0.3], [0.5, 2.2, -0.3], [0.45, 4.3, -0.3], [0.3, 4.75, -0.2], // 稀相往上回 Still
      [0.2, 5.2, 0.0], [0.4, 5.75, 0.1], [0.6, 7.2, 0.2], [0.6, 9.0, 0.2], // 蒸發、抽走
    ].map((p) => new THREE.Vector3(...p));
    const Tpts = [300, 4, 3, 1.2, 0.8, 0.1, 0.03, 0.015, 0.01, 0.01, 0.01, 0.02, 0.06, 0.4, 0.75, 0.8, 0.85, 4, 300];
    const lens = [0]; for (let i = 1; i < path.length; i++) lens.push(lens[i - 1] + path[i].distanceTo(path[i - 1]));
    const total = lens[lens.length - 1];
    const at = (s) => { for (let i = 1; i < lens.length; i++) if (s <= lens[i]) { const f = (s - lens[i - 1]) / (lens[i] - lens[i - 1]); return [path[i - 1].clone().lerp(path[i], f), Math.exp(Math.log(Tpts[i - 1]) + (Math.log(Tpts[i]) - Math.log(Tpts[i - 1])) * f), i]; } return [path[path.length - 1].clone(), 300, path.length - 1]; };
    scene.add(U.line(path, 0x8ef0ff, 0.25));
    ctx.label('① 自 GHS 回流的 ³He', [-1.0, 9.3, 0], 'small'); ctx.label('→ 抽往 GHS（渦輪泵）', [0.6, 9.3, 0.2], 'small');
    const NP = 90; const he3 = [];
    const g3 = new THREE.SphereGeometry(0.06, 10, 8);
    for (let i = 0; i < NP; i++) { const m = new THREE.Mesh(g3, new THREE.MeshBasicMaterial({ color: 0x8ef0ff })); scene.add(m); he3.push({ m, s: (i / NP) * total, jit: new THREE.Vector3(U.gauss(), U.gauss(), U.gauss()).multiplyScalar(0.05) }); }
    // ⁴He（稀相與 Still 液面中的背景原子）
    const he4 = []; const g4 = new THREE.SphereGeometry(0.045, 8, 6); const m4 = new THREE.MeshBasicMaterial({ color: 0x5b6f9a });
    for (let i = 0; i < 70; i++) {
      const inStill = i < 18; const a = Math.random() * 6.28, r = Math.sqrt(Math.random()) * (inStill ? 0.65 : 0.8);
      const m = new THREE.Mesh(g4, m4); const y = inStill ? 4.65 + Math.random() * 0.4 : 0.05 + Math.random() * 0.7;
      m.position.set(r * Math.cos(a), y, r * Math.sin(a)); scene.add(m); he4.push({ m, b: m.position.clone(), ph: Math.random() * 6.28 });
    }
    const flashes = []; for (let i = 0; i < 6; i++) { const f = U.sphere(0.12, new THREE.MeshBasicMaterial({ color: 0xffd28a, transparent: true, opacity: 0 })); scene.add(f); flashes.push(f); }
    let fi = 0;

    // ===== 樣品區：銅支架 + 樣品盒 + 晶片 + 屏蔽（位於 MXC 板下方）=====
    const cu = U.metal(0xd08a3a, { roughness: 0.3 });
    const finger = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.16, 1.35, 20), cu); finger.position.set(0, -0.9, 0); scene.add(finger);
    const flange = new THREE.Mesh(new THREE.CylinderGeometry(0.45, 0.45, 0.08, 28), cu); flange.position.set(0, -1.6, 0); scene.add(flange);
    const SB = { y: -2.05, w: 1.3, h: 0.7, d: 1.0 };
    const boxBase = U.box(SB.w, 0.12, SB.d, cu, 0, SB.y - SB.h / 2 + 0.06, 0); scene.add(boxBase);
    [[-SB.w / 2 + 0.05, 0.1, SB.d], [SB.w / 2 - 0.05, 0.1, SB.d]].forEach(([x, w, d]) => scene.add(U.box(w, SB.h, d, cu, x, SB.y, 0)));
    scene.add(U.box(SB.w, SB.h, 0.08, cu, 0, SB.y, -SB.d / 2 + 0.04));
    const lid = U.box(SB.w, 0.08, SB.d, U.metal(0xd08a3a, { transparent: true, opacity: 0.25, depthWrite: false }), 0, SB.y + SB.h / 2 - 0.04, 0); scene.add(lid);
    const pcb = U.box(1.05, 0.03, 0.8, U.mat(0x1f6b3a, { roughness: 0.7 }), 0, SB.y - SB.h / 2 + 0.135, 0); scene.add(pcb);
    const die = U.box(0.42, 0.04, 0.42, U.mat(0x2a3446, { roughness: 0.4, metalness: 0.2 }), 0, SB.y - SB.h / 2 + 0.17, 0); scene.add(die);
    const xm = U.mat(0xe6ecf5, { emissive: 0x4f8cff, emissiveIntensity: 0.6 });
    const cross = new THREE.Group();
    cross.add(U.box(0.26, 0.012, 0.04, xm), U.box(0.04, 0.012, 0.26, xm));
    cross.position.set(-0.07, SB.y - SB.h / 2 + 0.197, 0.04); scene.add(cross);
    const res = []; for (let k = 0; k < 7; k++) res.push([0.05 + (k % 2 ? 0.1 : 0), SB.y - SB.h / 2 + 0.196, -0.15 + k * 0.045]);
    scene.add(U.tube(res, 0.006, U.glow(0x8ef0ff)));
    // 打線（die → PCB）
    for (let k = 0; k < 6; k++) { const z = -0.15 + k * 0.06; scene.add(U.smoothTube([[0.21, SB.y - SB.h / 2 + 0.19, z], [0.27, SB.y - SB.h / 2 + 0.23, z], [0.33, SB.y - SB.h / 2 + 0.155, z]], 0.004, U.metal(0xffd28a), false, 12)); }
    // SMA 接頭與同軸線（往上接到各級）
    const coaxM = U.metal(0xc0c8d4);
    [-0.35, 0, 0.35].forEach((z, k) => {
      const sma = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 0.18, 12), U.metal(0xffd28a)); sma.rotation.z = Math.PI / 2; sma.position.set(SB.w / 2 + 0.09, SB.y, z); scene.add(sma);
      scene.add(U.tube([[SB.w / 2 + 0.18, SB.y, z], [SB.w / 2 + 0.45 + k * 0.08, SB.y, z], [SB.w / 2 + 0.45 + k * 0.08, -0.3, z], [0.85 + k * 0.08, -0.15, z * 0.5]], 0.02, coaxM));
    });
    // 屏蔽罐（紅外 + 磁屏蔽）
    const shield = new THREE.Mesh(new THREE.CylinderGeometry(1.25, 1.25, 1.9, 40, 1, true), new THREE.MeshStandardMaterial({ color: 0x8fb3d9, transparent: true, opacity: 0.12, side: THREE.DoubleSide, depthWrite: false, metalness: 0.4, roughness: 0.4 }));
    shield.position.set(0, -1.85, 0); scene.add(shield);
    ctx.label('樣品支架（無氧銅，鍍金）', [-2.0, -0.75, 0], 'small');
    ctx.label('樣品盒（銅／鋁）', [-1.9, SB.y + 0.2, 0], 'gold small');
    const chipLbl = ctx.label('量子晶片（transmon）', [1.8, SB.y - 0.3, 0.6], 'q0');
    ctx.label('紅外屏蔽 + 磁屏蔽', [-2.0, -2.6, 0], 'small');
    ctx.label('同軸線（SMA）→ 往上接到各級', [2.6, -0.9, 0], 'small');
    // 熱傳導路徑：晶片 → 樣品盒 → 支架 → MXC 板 → 混合液
    const heatPath = [[-0.07, SB.y - SB.h / 2 + 0.2, 0.04], [-0.2, SB.y - SB.h / 2 + 0.08, 0.2], [-0.55, SB.y - SB.h / 2 + 0.08, 0.2], [-0.6, SB.y + 0.3, 0.2], [-0.1, SB.y + 0.38, 0.1], [0, -1.6, 0], [0, -0.2, 0], [0, -0.1, 0], [0.1, 0.3, 0.1]].map((p) => new THREE.Vector3(...p));
    const hl = [0]; for (let i = 1; i < heatPath.length; i++) hl.push(hl[i - 1] + heatPath[i].distanceTo(heatPath[i - 1]));
    const hTot = hl[hl.length - 1];
    const hAt = (s) => { for (let i = 1; i < hl.length; i++) if (s <= hl[i]) return heatPath[i - 1].clone().lerp(heatPath[i], (s - hl[i - 1]) / (hl[i] - hl[i - 1])); return heatPath[heatPath.length - 1].clone(); };
    const heatDots = []; const hg = new THREE.SphereGeometry(0.045, 10, 8);
    for (let i = 0; i < 22; i++) { const m = new THREE.Mesh(hg, new THREE.MeshBasicMaterial({ color: 0xff9f43, transparent: true })); scene.add(m); heatDots.push({ m, s: (i / 22) * hTot }); }
    const heatLbl = ctx.label('熱流：晶片 → 樣品盒 → 支架 → MXC 板 → 混合液', [0, -3.3, 0.6], 'gold small');
    let showHeat = true;
    const rowV = ui.row();
    ui.button('視角：全景', () => ctx.app.orbit.reset(), rowV);
    ui.button('視角：樣品區（晶片位置）', () => ctx.app.orbit.flyTo([3.2, -0.2, 4.6], [0, -1.4, 0], 1.4), rowV);
    ui.toggle('顯示熱傳導路徑', true, (on) => { showHeat = on; heatDots.forEach((d) => (d.m.visible = on)); heatLbl.show(on); });
    let ndot = 0.5, qload = 10; // mmol/s, μW
    ui.slider('³He 循環率 ṅ (mmol/s)', 0.1, 1.5, 0.05, ndot, (v) => { ndot = v; }, (v) => v.toFixed(2));
    ui.slider('MXC 上的熱負載 (μW)', 0.5, 60, 0.5, qload, (v) => { qload = v; }, (v) => v.toFixed(1));
    const ro = ui.readout();
    ctx.inset('冷卻功率 Q̇ = 84 ṅ T² 與熱負載', (g, W, H, P) => {
      const { X, Y } = P.frame(g, W, H, [0, 50], [0, 80], { xlabel: 'MXC 溫度 (mK)', ylabel: 'μW', xticks: [[0, '0'], [10, '10'], [20, '20'], [30, '30'], [40, '40'], [50, '50']], yticks: [[0, '0'], [40, '40'], [80, '80']] });
      P.curve(g, (t) => 84 * ndot * 1e-3 * (t * 1e-3) ** 2 * 1e6, 0, 50, X, Y, '#38c6d9', 2.5);
      g.strokeStyle = '#ff7a59'; g.setLineDash([5, 4]); g.beginPath(); g.moveTo(X(0), Y(qload)); g.lineTo(X(50), Y(qload)); g.stroke(); g.setLineDash([]);
      const Tb = Math.sqrt((qload * 1e-6) / (84 * ndot * 1e-3)) * 1e3;
      if (Tb < 50) P.dot(g, X(Tb), Y(qload), 6, '#ffd28a');
      P.text(g, '冷卻功率', X(44), Y(84 * ndot * 1e-3 * (44e-3) ** 2 * 1e6) - 8, '#38c6d9', 'right');
      P.text(g, '熱負載', X(2), Y(qload) - 6, '#ff7a59');
    });
    return {
      update(time, dt) {
        const v = 0.55 + ndot * 0.9;
        he3.forEach((p) => {
          const prev = p.s; p.s = (p.s + dt * v) % total;
          const [pos, T, seg] = at(p.s);
          p.m.position.copy(pos).add(p.jit);
          p.m.material.color.copy(App.tempColor(T));
          if (prev < lens[8] && p.s >= lens[8]) { const f = flashes[fi++ % flashes.length]; f.position.copy(pos); f.material.opacity = 0.9; f.scale.setScalar(0.6); }
        });
        flashes.forEach((f) => { f.material.opacity = Math.max(0, f.material.opacity - dt * 1.8); f.scale.multiplyScalar(1 + dt * 2.5); });
        he4.forEach((a) => { a.ph += dt * 2; a.m.position.set(a.b.x + 0.02 * Math.sin(a.ph), a.b.y + 0.02 * Math.cos(a.ph * 1.3), a.b.z); });
        heater.material.emissiveIntensity = 0.5 + 0.4 * ndot + 0.2 * Math.sin(time * 6);
        if (showHeat) heatDots.forEach((d) => {
          d.s = (d.s + dt * 0.7) % hTot; d.m.position.copy(hAt(d.s));
          const f = d.s / hTot; d.m.material.color.setHSL(0.08 + 0.5 * f, 0.9, 0.6); d.m.material.opacity = f > 0.9 ? (1 - f) * 10 : 1;
        });
        xm.emissiveIntensity = 0.45 + 0.25 * Math.sin(time * 3);
        const Tb = Math.sqrt((qload * 1e-6) / (84 * ndot * 1e-3)) * 1e3;
        ro.innerHTML = `平衡溫度 T = √(Q̇ / 84ṅ) ≈ <b>${Tb.toFixed(1)} mK</b><br>20 mK 時冷卻功率 ≈ ${(84 * ndot * 1e-3 * 4e-4 * 1e6).toFixed(1)} μW；100 mK 時 ≈ ${(84 * ndot * 1e-3 * 1e-2 * 1e6).toFixed(0)} μW<br>（實際機台因熱交換器效率等因素低於理想值）`;
      },
    };
  },
});
