/* 場景 8：量子晶片 — Xmon 量子位元、λ/4 讀取諧振腔、共用饋線、頻率多工讀取 */
App.register({
  id: 'chip', num: 8, short: '晶片與多工讀取',
  title: '電路 QED 晶片：量子位元 + 讀取諧振腔',
  subtitle: '每個量子位元配一個不同頻率的 λ/4 共平面波導諧振腔，共用一條饋線',
  desc: `<p><b>Xmon（十字形 transmon）</b>：十字形電容板 + 一端的 SQUID/JJ 接地。十字的四臂分別耦合到讀取諧振腔、XY 驅動線、Z 磁通線與鄰近量子位元。</p>
<p><b>λ/4 讀取諧振腔</b>：一段彎曲的共平面波導（CPW），長度約 4 mm → 共振頻率約 6–8 GHz。一端靠近量子位元（電容耦合 g），另一端靠近饋線（耦合率 κ）。</p>
<p><b>頻率多工</b>：每個諧振腔長度略有不同（頻率差數十 MHz），所以一條饋線送入「頻率梳」就能<b>同時讀取多個量子位元</b>。</p>
<p>點選各量子位元切換 |0⟩/|1⟩，再送出讀取脈衝，觀察右下角穿透頻譜的變化。</p>`,
  camera: { pos: [0, 10.5, 9.5], target: [0, 0, 0.3] },
  build(ctx) {
    const { scene, U, THREE, ui, app } = ctx;
    const Y = 0.16;
    scene.add(U.box(13, 0.3, 9, U.mat(0x1d2533, { roughness: 0.8 }), 0, -0.15 + 0.0, 0));
    scene.add(U.box(12.6, 0.02, 8.6, U.metal(0x8f9bb0, { roughness: 0.55, metalness: 0.7 }), 0, 0.01 + 0.0, 0));
    ctx.label('超導接地面（Al / Nb / Ta 薄膜）on 矽基板', [-4.4, 0.1, 4.6], 'small');
    const gapMat = new THREE.MeshBasicMaterial({ color: 0x0b0f18 });
    const cpw = (pts, mat, r = 0.045) => {
      const g = new THREE.Group();
      const gp = U.tube(pts.map(([x, z]) => [x, Y - 0.12, z]), r * 2.4, gapMat); gp.scale.y = 0.3; gp.position.y = 0.06;
      g.add(gp, U.tube(pts.map(([x, z]) => [x, Y - 0.08, z]), r, mat));
      return g;
    };
    // 饋線
    const feedZ = -2.7;
    const feedMat = U.metal(0xd6dde8, { emissive: 0x0a2a33, emissiveIntensity: 0.2 });
    scene.add(cpw([[-6.0, feedZ], [6.0, feedZ]], feedMat, 0.07));
    scene.add(U.box(0.6, 0.04, 0.6, U.metal(0xe0a54a), -6.1, 0.04, feedZ), U.box(0.6, 0.04, 0.6, U.metal(0xe0a54a), 6.1, 0.04, feedZ));
    ctx.label('讀取饋線 IN', [-6.0, 0.4, feedZ - 0.7], 'teal');
    ctx.label('OUT → 放大器', [6.0, 0.4, feedZ - 0.7], 'teal');

    const QX = [-4.5, -1.5, 1.5, 4.5];
    const FR = [6.82, 6.97, 7.11, 7.26]; // 諧振腔頻率 GHz
    const qColor = (s) => (s ? 0xff5a5f : 0x4f8cff);
    const qubits = [];
    QX.forEach((xq, i) => {
      // 諧振腔：耦合肘（平行饋線）+ 蜿蜒線，legs 越多 → 越長 → 頻率越低（此處僅示意）
      const legs = 6 + i; const z0 = feedZ + 0.75, z1 = 0.75; const dz = (z1 - z0) / legs;
      const P = [[xq - 0.9, feedZ + 0.35], [xq + 0.5, feedZ + 0.35], [xq + 0.5, z0]];
      for (let k = 0; k < legs; k++) {
        const z = z0 + dz * k, zn = z0 + dz * (k + 1);
        const x = k % 2 === 0 ? -0.5 : 0.5;
        P.push([xq + x, z], [xq + x, zn]);
      }
      P.push([xq, z1], [xq, 1.2]);
      const resMat = U.metal(0xd6dde8, { emissive: 0x38c6d9, emissiveIntensity: 0 });
      const res = cpw(P, resMat, 0.04); scene.add(res);
      // Xmon 十字
      const xm = U.metal(0xe6ecf5, { emissive: qColor(0), emissiveIntensity: 0.15 });
      const cz = 2.3, arm = 0.95, w = 0.2;
      const cross = new THREE.Group();
      cross.add(U.box(2 * arm, 0.05, w, xm, 0, 0, 0), U.box(w, 0.05, 2 * arm, xm, 0, 0, 0));
      cross.position.set(xq, Y - 0.04, cz); scene.add(cross);
      const halo = U.box(2 * arm + 0.25, 0.01, w + 0.25, gapMat, xq, Y - 0.07, cz); const halo2 = U.box(w + 0.25, 0.01, 2 * arm + 0.25, gapMat, xq, Y - 0.07, cz);
      scene.add(halo, halo2);
      // 耦合爪
      scene.add(U.tube([[xq - 0.35, Y - 0.05, 1.2], [xq + 0.35, Y - 0.05, 1.2]], 0.05, resMat));
      // SQUID（上端）
      const sq = new THREE.Mesh(new THREE.TorusGeometry(0.16, 0.035, 8, 24), new THREE.MeshStandardMaterial({ color: 0xff7a59, emissive: 0xff7a59, emissiveIntensity: 0.6 }));
      sq.rotation.x = Math.PI / 2; sq.position.set(xq, Y, cz + arm + 0.2); scene.add(sq);
      // XY / Z 控制線
      scene.add(cpw([[xq + 1.5, 4.3], [xq + 1.5, cz], [xq + arm + 0.35, cz]], U.metal(0xc8a46a), 0.035));
      scene.add(cpw([[xq - 0.6, 4.3], [xq - 0.6, cz + arm + 0.55], [xq - 0.05, cz + arm + 0.55]], U.metal(0x9ad1a0), 0.035));
      ctx.label(`Q${i + 1}`, [xq - 0.7, 0.5, cz - 0.6], 'big');
      qubits.push({ xq, res, resMat, xm, state: 0, amp: 0, f: FR[i] });
    });
    ctx.label('Xmon 量子位元', [QX[0] + 0.95, 0.45, 3.35], 'gold small');
    ctx.label('SQUID / JJ', [QX[1] + 0.55, 0.45, 3.65], 'gold small');
    ctx.label('XY 驅動線', [QX[2] + 1.55, 0.45, 3.9], 'small');
    ctx.label('Z 磁通線', [QX[3] - 0.6, 0.45, 4.0], 'small');
    ctx.label('λ/4 讀取諧振腔', [QX[0] + 0.9, 0.45, -0.8], 'teal small');

    // 讀取脈衝封包
    const packets = [];
    const pcol = [0x6fb4ff, 0x8ef0ff, 0xb2ff9e, 0xffd28a];
    function sendPulse(mask) {
      mask.forEach((on, i) => {
        if (!on) return;
        const g = new THREE.Group();
        for (let k = 0; k < 7; k++) { const s = U.sphere(0.08 + 0.02 * Math.sin((k / 6) * Math.PI), U.glow(pcol[i], 0.9)); s.position.x = -k * 0.13; g.add(s); }
        g.position.set(-6.2 - i * 0.05, Y + 0.12 + i * 0.05, feedZ);
        scene.add(g); packets.push({ g, i, x: -6.2 - i * 0.25 });
      });
    }
    const r = ui.row();
    const qBtns = qubits.map((q, i) => ui.button(`Q${i + 1}: |0⟩`, (b) => { q.state ^= 1; b.textContent = `Q${i + 1}: |${q.state}⟩`; b.classList.toggle('on', !!q.state); }, r));
    const r2 = ui.row();
    ui.button('▶ 多工讀取（4 個頻率同時）', () => sendPulse([1, 1, 1, 1]), r2);
    ui.button('只讀 Q2', () => sendPulse([0, 1, 0, 0]), r2);
    let autoSend = true;
    ui.toggle('自動重複讀取', true, (on) => { autoSend = on; });
    const r3 = ui.row();
    ui.button('視角：全晶片', () => app.orbit.flyTo([0, 10.5, 9.5], [0, 0, 0.3]), r3);
    ui.button('放大 Xmon', () => app.orbit.flyTo([-0.6, 3.2, 4.8], [-1.5, 0, 2.4]), r3);
    ui.button('放大饋線耦合', () => app.orbit.flyTo([-3.6, 2.6, -0.4], [-4.3, 0, -2.4]), r3);
    const ro = ui.readout();
    const chi = 0.004, kap = 0.006; // GHz（示意放大）

    ctx.inset('饋線穿透 |S21| 頻譜（4 個諧振腔的吸收凹陷）', (g, W, H, P) => {
      const { X, Y: Yp } = P.frame(g, W, H, [6.7, 7.38], [0, 1.08], { xlabel: '頻率 (GHz)', ylabel: '|S21|', xticks: [[6.8, '6.8'], [7.0, '7.0'], [7.2, '7.2']], yticks: [[0, '0'], [1, '1']] });
      const s21 = (f) => { let v = 1; qubits.forEach((q) => { const fr = q.f + (q.state ? chi * 6 : -chi * 6); const d = (f - fr) / (kap * 2); v *= 1 - 0.85 / (1 + 4 * d * d); }); return v; };
      P.curve(g, s21, 6.7, 7.38, X, Yp, '#e0a54a', 2, 800);
      qubits.forEach((q, i) => {
        g.strokeStyle = '#' + pcol[i].toString(16).padStart(6, '0'); g.setLineDash([3, 3]); g.beginPath(); g.moveTo(X(q.f), Yp(0)); g.lineTo(X(q.f), Yp(1.05)); g.stroke(); g.setLineDash([]);
        P.text(g, `Q${i + 1}:|${q.state}⟩`, X(q.f), Yp(0.12), q.state ? '#ffb0b2' : '#a9c6ff', 'center');
      });
    });

    let tSend = 0;
    return {
      update(time, dt) {
        tSend -= dt;
        if (autoSend && tSend <= 0) { sendPulse([1, 1, 1, 1]); tSend = 4.5; }
        for (let k = packets.length - 1; k >= 0; k--) {
          const p = packets[k]; p.x += dt * 3.2; p.g.position.x = p.x;
          const q = qubits[p.i];
          if (Math.abs(p.x - (q.xq - 0.3)) < 0.5) q.amp = Math.min(1, q.amp + dt * 4);
          if (p.x > 6.6) { scene.remove(p.g); p.g.traverse((o) => o.geometry && o.geometry.dispose()); packets.splice(k, 1); }
        }
        qubits.forEach((q) => {
          q.amp = Math.max(0, q.amp - dt * 0.6);
          q.resMat.emissiveIntensity = q.amp * (0.6 + 0.4 * Math.sin(time * 18));
          q.xm.emissive.setHex(qColor(q.state)); q.xm.emissiveIntensity = 0.25 + 0.5 * q.amp;
        });
        ro.innerHTML = qubits.map((q, i) => `Q${i + 1}：f_r = ${q.f.toFixed(2)} GHz，狀態 |${q.state}⟩ → 腔頻 ${q.state ? '+' : '−'}χ`).join('<br>') +
          '<br>典型 κ/2π ≈ 1–5 MHz，2χ/2π ≈ 1–5 MHz';
      },
    };
  },
});
