/* 場景 10：IQ 平面與狀態判別 — 單發量測軌跡、高斯叢集、閾值、保真度 */
App.register({
  id: 'iq', num: 10, short: 'IQ 判別',
  title: '單發讀取：IQ 叢集與狀態判別',
  subtitle: '積分後的 (I, Q) 點落入兩團高斯分佈 → 以閾值判定 0 或 1',
  desc: `<p>每一次量測（single shot），數位化後的訊號經解調與<b>加權積分</b>得到一個 (I, Q) 點。圖中每條軌跡從上方（t = 0）落到 IQ 平面（t = τ_int）：一開始被雜訊淹沒，積分越久越收斂。</p>
<p>重複數千次，|0⟩ 與 |1⟩ 形成<b>兩團高斯雲</b>。以兩團中心的<b>垂直平分線</b>作為閾值即可判別。</p>
<p>• <b>放大器雜訊</b>決定雲的寬度（量子極限放大器 JPA/TWPA 可大幅縮小）<br>• <b>積分時間</b>越長 SNR 越好，但<b>T1 衰減</b>會讓 |1⟩ 在讀取途中掉到 |0⟩，形成兩團之間的「拖尾」<br>• 讀取保真度 F = 1 − [P(0|1) + P(1|0)] / 2</p>`,
  camera: { pos: [0, 5.8, 8.6], target: [0, 1.3, 0] },
  build(ctx) {
    const { scene, U, THREE, ui } = ctx;
    const HT = 4.2; // 時間軸高度
    // IQ 平面
    const plane = new THREE.Mesh(new THREE.PlaneGeometry(8, 8), new THREE.MeshStandardMaterial({ color: 0x101a2c, roughness: 0.9, side: THREE.DoubleSide }));
    plane.rotation.x = -Math.PI / 2; scene.add(plane);
    const grid = new THREE.GridHelper(8, 16, 0x34507a, 0x1d2b44); grid.position.y = 0.005; scene.add(grid);
    scene.add(U.line([[-4, 0.01, 0], [4, 0.01, 0]], 0x8ab4ff, 0.6), U.line([[0, 0.01, -4], [0, 0.01, 4]], 0x8ab4ff, 0.6));
    ctx.label('I', [4.3, 0, 0], 'plain big'); ctx.label('Q', [0, 0, -4.3], 'plain big');
    scene.add(U.line([[-4, 0, -4], [-4, HT, -4]], 0x9fb0c8, 0.6));
    ctx.label('時間 t = 0', [-4, HT, -4], 'small'); ctx.label('t = τ_int', [-4, 0.2, -4], 'small');
    const c0 = new THREE.Vector2(-1.4, 0.7), c1 = new THREE.Vector2(1.4, -0.7);
    ctx.label('|0⟩ 叢集', [c0.x - 0.4, 0.25, c0.y - 1.4], 'q0'); ctx.label('|1⟩ 叢集', [c1.x + 0.4, 0.25, c1.y + 1.5], 'q1');
    // 閾值線（垂直平分線）
    const n = c1.clone().sub(c0).normalize(); const perp = new THREE.Vector2(-n.y, n.x);
    const thr = U.line([[perp.x * -4, 0.02, perp.y * -4], [perp.x * 4, 0.02, perp.y * 4]], 0xe0a54a); scene.add(thr);
    ctx.label('判別閾值', [perp.x * 3.4, 0.3, perp.y * 3.4], 'gold small');

    // 點雲
    const MAXP = 1200;
    const pg = new THREE.BufferGeometry();
    pg.setAttribute('position', new THREE.BufferAttribute(new Float32Array(MAXP * 3), 3));
    pg.setAttribute('color', new THREE.BufferAttribute(new Float32Array(MAXP * 3), 3));
    pg.setDrawRange(0, 0);
    const pts = new THREE.Points(pg, new THREE.PointsMaterial({ size: 0.09, vertexColors: true, transparent: true, opacity: 0.9 }));
    pts.frustumCulled = false; scene.add(pts);
    const shots = []; // {prep, x, z}
    // 軌跡
    const NT = 10; const trails = [];
    for (let i = 0; i < NT; i++) { const l = U.dynLine(60, 0xffffff, 0.8); scene.add(l.obj); trails.push({ l, life: 0 }); }
    let ti = 0;
    const falling = [];

    let sigma0 = 1.0, tint = 1.0, T1 = 8, useT1 = true, amp = true, rate = 14;
    ui.toggle('量子極限放大器（JPA/TWPA）開啟', true, (on) => { amp = on; clear(); });
    ui.slider('積分時間 τ_int（相對）', 0.2, 3, 0.05, tint, (v) => { tint = v; clear(); }, (v) => v.toFixed(2));
    ui.toggle('包含讀取期間的 T1 衰減', true, (on) => { useT1 = on; clear(); });
    ui.slider('T1（與 τ_int 同單位，越大衰減越少）', 2, 40, 1, T1, (v) => { T1 = v; clear(); }, (v) => v.toFixed(0));
    ui.slider('每秒量測次數（動畫）', 2, 60, 1, rate, (v) => { rate = v; }, (v) => v.toFixed(0));
    ui.button('清除', () => clear());
    const ro = ui.readout();
    function clear() { shots.length = 0; pg.setDrawRange(0, 0); }

    function shoot() {
      const prep = Math.random() < 0.5 ? 0 : 1;
      const N = 50; const sig = (amp ? 0.33 : 1.25) * Math.sqrt(1 / tint);
      // 衰減時間（以積分時間為單位）
      const tDecay = prep === 1 && useT1 ? (-Math.log(Math.random()) * T1) / tint : Infinity; // 以積分時間比例表示
      let sx = 0, sz = 0; const path = [];
      for (let k = 1; k <= N; k++) {
        const tf = k / N; // 0..1（佔積分時間比例）
        const st = tf < tDecay ? prep : 0;
        const c = st ? c1 : c0;
        const ring = 1 - Math.exp(-tf * tint * 6); // 諧振腔充能
        const s = sig * Math.sqrt(N);
        sx += c.x * ring + s * U.gauss(); sz += c.y * ring + s * U.gauss();
        path.push([Math.max(-4, Math.min(4, sx / k)), HT * (1 - tf), Math.max(-4, Math.min(4, sz / k))]);
      }
      const end = path[path.length - 1];
      falling.push({ path, k: 0, prep, end });
    }
    function addShot(prep, x, z) {
      shots.push({ prep, x, z }); if (shots.length > MAXP) shots.shift();
      const P = pg.attributes.position.array, C = pg.attributes.color.array;
      shots.forEach((s, i) => { P.set([s.x, 0.03, s.z], 3 * i); C.set(s.prep ? [1, 0.36, 0.38] : [0.31, 0.55, 1], 3 * i); });
      pg.attributes.position.needsUpdate = true; pg.attributes.color.needsUpdate = true; pg.setDrawRange(0, shots.length);
    }
    const proj = (x, z) => (x - (c0.x + c1.x) / 2) * n.x + (z - (c0.y + c1.y) / 2) * n.y;

    ctx.inset('沿判別軸投影的直方圖（藍：製備 |0⟩，紅：製備 |1⟩）', (g, W, H, P) => {
      const NB = 48, lo = -4, hi = 4; const h0 = new Array(NB).fill(0), h1 = new Array(NB).fill(0);
      shots.forEach((s) => { const p = proj(s.x, s.z); const b = Math.floor(((p - lo) / (hi - lo)) * NB); if (b >= 0 && b < NB) (s.prep ? h1 : h0)[b]++; });
      const mx = Math.max(4, ...h0, ...h1);
      const { X, Y } = P.frame(g, W, H, [lo, hi], [0, mx * 1.1], { xlabel: '投影值（閾值 = 0）', ylabel: '次數', xticks: [[-3, '-3'], [0, '0'], [3, '3']] });
      const bw = (X(hi) - X(lo)) / NB;
      [[h0, 'rgba(79,140,255,.65)'], [h1, 'rgba(255,90,95,.65)']].forEach(([h, c]) => { g.fillStyle = c; h.forEach((v, i) => { g.fillRect(X(lo) + i * bw, Y(v), bw - 1, Y(0) - Y(v)); }); });
      g.strokeStyle = '#e0a54a'; g.lineWidth = 2; g.beginPath(); g.moveTo(X(0), Y(0)); g.lineTo(X(0), Y(mx * 1.1)); g.stroke();
    });

    let acc = 0;
    return {
      update(time, dt) {
        acc += dt * rate; while (acc > 1) { acc -= 1; shoot(); }
        for (let i = falling.length - 1; i >= 0; i--) {
          const f = falling[i]; f.k += dt * 60;
          const k = Math.min(f.path.length, Math.floor(f.k));
          const tr = trails[ti % NT];
          if (!f.tr) { f.tr = tr; ti++; tr.l.obj.material.color.setHex(f.prep ? 0xff7a7e : 0x7fb0ff); }
          f.tr.l.set(f.path.slice(0, Math.max(2, k)));
          f.tr.l.obj.material.opacity = 0.55;
          if (k >= f.path.length) { addShot(f.prep, f.end[0], f.end[2]); falling.splice(i, 1); }
        }
        trails.forEach((t) => { t.l.obj.material.opacity = Math.max(0.05, t.l.obj.material.opacity - dt * 0.5); });
        // 保真度
        let e01 = 0, e10 = 0, n0 = 0, n1 = 0;
        shots.forEach((s) => { const p = proj(s.x, s.z); if (s.prep) { n1++; if (p < 0) e10++; } else { n0++; if (p > 0) e01++; } });
        const P10 = n1 ? e10 / n1 : 0, P01 = n0 ? e01 / n0 : 0;
        const F = 1 - (P10 + P01) / 2;
        const sig = (amp ? 0.33 : 1.25) * Math.sqrt(1 / tint);
        const snr = c1.distanceTo(c0) / (2 * sig);
        ro.innerHTML = `累積量測：${shots.length} 次<br>P(判 1 | 備 0) = ${(P01 * 100).toFixed(1)} %　P(判 0 | 備 1) = ${(P10 * 100).toFixed(1)} %<br><b>讀取保真度 F ≈ ${(F * 100).toFixed(1)} %</b>　（SNR = 分離/2σ ≈ ${snr.toFixed(1)}）`;
      },
    };
  },
});
