/* 周邊場景 2：脈衝管冷卻器與氦壓縮機 — 提供 50 K 與 4 K 的「預冷」 */
App.register({
  id: 'pulsetube', num: 2, short: '脈衝管冷卻',
  title: '脈衝管冷卻器 + 氦壓縮機',
  subtitle: '「乾式」冷凍機的心臟：不需液氦，持續提供 ~45 K 與 ~3 K',
  desc: `<p><b>壓縮機</b>把氦氣壓縮到高壓（約 2 MPa），熱量交給<b>冷卻水</b>帶走。</p>
<p><b>旋轉閥</b>以約 1–1.4 Hz 交替接通高壓與低壓，使冷頭內的氦氣週期性<b>壓縮–膨脹</b>。</p>
<p><b>蓄冷器（regenerator）</b>是填滿金屬網／稀土合金的管子：氣體往下流時把熱留在填料，往上流時再取回，形成溫度梯度。</p>
<p><b>脈衝管 + 緩衝槽/孔口</b>調整壓力與流量的相位，使膨脹發生在冷端 → <b>冷端吸熱</b>。冷端<b>沒有活動零件</b>，振動小、可靠度高。</p>
<p>兩級設計：一級約 40–50 K（冷卻輻射屏蔽、熱錨定纜線），二級約 3–4 K（冷卻 4 K 板並凝結混合氣）。</p>`,
  camera: { pos: [6.5, 4.8, 14], target: [-1.6, 2.9, 0] },
  build(ctx) {
    const { scene, U, THREE, ui } = ctx;
    // 壓縮機
    const comp = App.device(ctx, { pos: [-5, 0, 0], w: 1.6, h: 1.8, d: 1.4, color: 0x2f4a3a, label: '氦壓縮機<br>電力 ~10 kW · 水冷', leds: 3 });
    const floor = new THREE.Mesh(new THREE.PlaneGeometry(16, 8), U.mat(0x1a2130, { roughness: 0.95 })); floor.rotation.x = -Math.PI / 2; scene.add(floor);
    // 冷頭
    const valve = new THREE.Mesh(new THREE.CylinderGeometry(0.45, 0.45, 0.6, 28), U.metal(0xd8dee8)); valve.position.set(0, 5.3, 0); scene.add(valve);
    const motor = U.box(0.5, 0.4, 0.5, U.mat(0x3a4456), 0, 5.8, 0); scene.add(motor);
    ctx.label('旋轉閥 + 馬達（~1.4 Hz）', [1.6, 5.6, 0], 'small');
    const glass = (r, y0, y1, x, z = 0) => {
      const m = new THREE.Mesh(new THREE.CylinderGeometry(r, r, y0 - y1, 24, 1, true), new THREE.MeshStandardMaterial({ color: 0xbfd0e6, transparent: true, opacity: 0.22, side: THREE.DoubleSide, depthWrite: false }));
      m.position.set(x, (y0 + y1) / 2, z); scene.add(m); return m;
    };
    // 一級：蓄冷器 + 脈衝管
    glass(0.32, 5.0, 2.7, -0.35); glass(0.17, 5.0, 2.7, 0.45);
    // 二級：蓄冷器（一級冷端 → 二級冷端）+ 脈衝管（二級冷端 → 室溫端）
    glass(0.22, 2.55, 0.65, -0.35); glass(0.12, 5.0, 0.65, 0.95);
    const fl1 = new THREE.Mesh(new THREE.CylinderGeometry(0.85, 0.85, 0.12, 40), U.metal(0xc98a4b)); fl1.position.set(0.2, 2.62, 0); scene.add(fl1);
    const fl2 = new THREE.Mesh(new THREE.CylinderGeometry(0.75, 0.75, 0.12, 40), U.metal(0xc98a4b)); fl2.position.set(0.3, 0.6, 0); scene.add(fl2);
    ctx.label('一級冷端 ~45 K<br>（~40 W）', [2.0, 2.62, 0], 'gold');
    ctx.label('二級冷端 ~3 K<br>（~1.5 W @ 4.2 K）', [2.0, 0.6, 0], 'gold');
    ctx.label('蓄冷器', [-1.25, 3.9, 0], 'small'); ctx.label('一級脈衝管', [0.45, 5.15, 0.6], 'small');
    ctx.label('二級蓄冷器', [-1.35, 1.6, 0], 'small'); ctx.label('二級脈衝管', [1.75, 3.9, 0], 'small');
    // 緩衝槽 + 孔口
    const buf = new THREE.Mesh(new THREE.CylinderGeometry(0.35, 0.35, 0.7, 24), U.metal(0x9aa4b2)); buf.position.set(2.2, 5.3, -0.6); scene.add(buf);
    scene.add(U.tube([[0.45, 5.0, 0], [0.45, 5.35, -0.3], [1.85, 5.35, -0.6]], 0.04, U.metal(0x9aa4b2)), U.tube([[0.95, 5.0, 0], [0.95, 5.2, -0.6], [1.85, 5.2, -0.6]], 0.03, U.metal(0x9aa4b2)));
    ctx.label('緩衝槽 + 孔口（相位調節）', [2.4, 6.0, -0.6], 'small');
    // 軟管與流動
    const hi = App.Flow(scene, [[-4.4, 1.8, 0.2], [-4.4, 4.6, 0.2], [-0.4, 4.6, 0.2], [-0.4, 5.3, 0.25]], 0xff7a59, { speed: 1.6, radius: 0.06 });
    const lo = App.Flow(scene, [[0.4, 5.3, 0.25], [0.4, 4.4, -0.3], [-5.6, 4.4, -0.3], [-5.6, 1.8, -0.3]], 0x4fa3ff, { speed: 1.6, radius: 0.06 });
    ctx.label('高壓氦（~2 MPa）', [-2.4, 4.85, 0.2], 'small'); ctx.label('低壓氦（~0.8 MPa）', [-2.4, 4.1, -0.3], 'small');
    const wIn = App.Flow(scene, [[-7.5, 0.3, 0.4], [-5.8, 0.3, 0.4]], 0x4fa3ff, { speed: 1.0, radius: 0.05 });
    const wOut = App.Flow(scene, [[-5.8, 0.6, -0.4], [-7.5, 0.6, -0.4]], 0xff9f43, { speed: 1.0, radius: 0.05 });
    ctx.label('冷卻水 進 / 出', [-7.2, 1.1, 0], 'small');

    // 冷頭內的氣體粒子（顏色依高度代表溫度）
    const tubes = [
      { x: -0.35, y0: 4.95, y1: 2.75, r: 0.26, n: 70, amp: 0.25 },
      { x: 0.45, y0: 4.95, y1: 2.75, r: 0.12, n: 30, amp: 0.6 },
      { x: -0.35, y0: 2.5, y1: 0.7, r: 0.17, n: 45, amp: 0.18 },
      { x: 0.95, y0: 4.95, y1: 0.7, r: 0.08, n: 35, amp: 0.5 },
    ];
    const Ty = (y) => (y > 2.62 ? 45 + ((y - 2.62) / (5.0 - 2.62)) * 255 : 3 + ((y - 0.6) / (2.62 - 0.6)) * 42);
    const parts = [];
    const pg = new THREE.SphereGeometry(0.035, 8, 6);
    tubes.forEach((tb, ti) => {
      for (let i = 0; i < tb.n; i++) {
        const m = new THREE.Mesh(pg, new THREE.MeshBasicMaterial({ color: 0xffffff }));
        const a = Math.random() * 6.28, rr = Math.sqrt(Math.random()) * tb.r * 0.85;
        const y = tb.y1 + Math.random() * (tb.y0 - tb.y1);
        m.position.set(tb.x + rr * Math.cos(a), y, rr * Math.sin(a)); scene.add(m);
        parts.push({ m, tb, base: y, ph: ti });
      }
    });
    let speed = 1.0;
    ui.slider('顯示速度（實際約 1.4 Hz）', 0.2, 2, 0.05, speed, (v) => { speed = v; }, (v) => v.toFixed(2) + '×');
    const ro = ui.readout();
    const hist = [];
    ctx.inset('冷頭內壓力（旋轉閥切換高/低壓）', (g, W, H, P) => {
      const { X, Y } = P.frame(g, W, H, [0, 3], [0.6, 2.2], { xlabel: '時間（週期）', ylabel: '壓力 (MPa)', xticks: [[0, '0'], [1, '1'], [2, '2'], [3, '3']], yticks: [[0.8, '0.8'], [2.0, '2.0']] });
      g.strokeStyle = '#ffd28a'; g.lineWidth = 2; g.beginPath();
      hist.forEach(([t, p], i) => (i ? g.lineTo(X(t), Y(p)) : g.moveTo(X(t), Y(p)))); g.stroke();
    });
    let ph = 0;
    return {
      update(time, dt) {
        ph += dt * speed * 2 * Math.PI * 0.7;
        const cyc = (ph / (2 * Math.PI)) % 3;
        const pr = 1.4 + 0.6 * Math.tanh(3 * Math.sin(ph));
        if (hist.length && cyc < hist[hist.length - 1][0]) hist.length = 0;
        hist.push([cyc, pr]);
        valve.rotation.y = ph;
        hi.speed = 1.6 * speed; lo.speed = 1.6 * speed; hi.update(dt); lo.update(dt); wIn.update(dt); wOut.update(dt);
        parts.forEach((p) => {
          const lag = p.tb.r < 0.15 ? 0.9 : 0; // 脈衝管與蓄冷器的相位差
          const y = U.clamp(p.base + p.tb.amp * Math.sin(ph - lag) * 0.5, p.tb.y1, p.tb.y0);
          p.m.position.y = y;
          p.m.material.color.copy(App.tempColor(Ty(y)));
        });
        fl1.material.emissive = App.tempColor(45); fl1.material.emissiveIntensity = 0.25;
        fl2.material.emissive = App.tempColor(3); fl2.material.emissiveIntensity = 0.35;
        ro.innerHTML = `冷頭壓力 ≈ ${pr.toFixed(2)} MPa（${Math.sin(ph) > 0 ? '高壓相：氣體壓縮' : '低壓相：氣體膨脹 → 冷端吸熱'}）<br>粒子顏色 = 溫度（紅 300 K → 藍 3 K）`;
      },
    };
  },
});
