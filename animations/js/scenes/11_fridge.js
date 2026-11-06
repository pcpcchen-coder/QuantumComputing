/* 場景 11：稀釋冷凍機中的讀取鏈 — 輸入線衰減、樣品、環行器、TWPA、HEMT、室溫解調 */
App.register({
  id: 'fridge', num: 11, short: '低溫讀取鏈',
  title: '稀釋冷凍機中的微波讀取鏈',
  subtitle: '室溫 → 50 K → 4 K → 0.8 K → 100 mK → 10 mK → 量子晶片 → 放大回到室溫',
  desc: `<p><b>輸入線（往下）</b>：各溫層放置<b>衰減器</b>（共約 −60 dB），把室溫 300 K 的熱雜訊（7 GHz 約上千個光子）壓到 10⁻³ 光子以下；最後在晶片端只剩約 −120 dBm（腔內數個光子）。</p>
<p><b>輸出線（往上）</b>：訊號極弱，必須先經過<b>環行器/隔離器</b>（阻擋反向雜訊），再由<b>量子極限放大器（JPA / TWPA，~20 dB）</b>在 10 mK 先放大，接著 4 K 的 <b>HEMT（~40 dB）</b>，最後室溫放大。</p>
<p>依 <b>Friis 公式</b>，整條鏈的雜訊幾乎由第一級放大器決定 — 這就是 TWPA 讓單發讀取成為可能的原因。</p>
<p>室溫端：AWG 產生脈衝 → IQ 混頻器上變頻 → … → 下變頻 → ADC → FPGA 數位解調與判別。</p>`,
  camera: { pos: [14, 7, 18], target: [0, 5.6, 0] },
  build(ctx) {
    const { scene, U, THREE, ui } = ctx;
    const plates = [
      { y: 9.0, r: 3.2, name: '300 K 室溫頂板', c: 0x9aa4b2 },
      { y: 7.6, r: 3.0, name: '50 K', c: 0xc98a4b },
      { y: 6.2, r: 2.8, name: '4 K（脈衝管冷頭）', c: 0xc98a4b },
      { y: 4.8, r: 2.5, name: 'Still ~0.8 K', c: 0xd29a52 },
      { y: 3.5, r: 2.3, name: 'Cold plate ~100 mK', c: 0xd8a85e },
      { y: 2.2, r: 2.1, name: 'Mixing chamber ~10 mK', c: 0xe6b86a },
    ];
    plates.forEach((p, i) => {
      const m = new THREE.Mesh(new THREE.CylinderGeometry(p.r, p.r, 0.16, 64), U.metal(p.c, { roughness: 0.35 }));
      m.position.y = p.y; scene.add(m);
      ctx.label(p.name, [-p.r - 1.6, p.y, 0], i === 5 ? 'gold' : 'small');
      if (i < plates.length - 1) {
        const q = plates[i + 1];
        for (let k = 0; k < 4; k++) {
          const a = (k / 4) * Math.PI * 2 + 0.4; const rr = q.r - 0.25;
          const rod = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, p.y - q.y, 8), U.metal(0xb0b8c4));
          rod.position.set(rr * Math.cos(a), (p.y + q.y) / 2, rr * Math.sin(a)); scene.add(rod);
        }
      }
    });
    // 樣品盒 + 磁屏蔽
    const sb = U.box(1.4, 0.5, 1.0, U.metal(0xd08a3a), 0, 1.0, 0); scene.add(sb);
    const shield = new THREE.Mesh(new THREE.CylinderGeometry(1.05, 1.05, 1.4, 40, 1, true), new THREE.MeshStandardMaterial({ color: 0x8fb3d9, transparent: true, opacity: 0.18, side: THREE.DoubleSide, depthWrite: false }));
    shield.position.y = 1.1; scene.add(shield);
    scene.add(new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 1.0, 8), U.metal(0xb0b8c4)).translateY(1.7));
    ctx.label('量子晶片（樣品盒 + 磁屏蔽）', [0, 0.35, 1.1], 'gold');

    // 線路
    const xin = -1.1, xout = 1.1;
    const coaxIn = U.tube([[xin, 10.6, 0], [xin, 1.25, 0], [-0.7, 1.25, 0]], 0.045, U.metal(0x9fd3ff, { roughness: 0.3 }));
    const coaxOut = U.tube([[0.7, 1.25, 0], [xout, 1.25, 0], [xout, 10.6, 0]], 0.045, U.metal(0xffd28a, { roughness: 0.3 }));
    scene.add(coaxIn, coaxOut);
    const comp = (x, y, w, h, color, text, cls = 'small', side = -1) => {
      const m = U.box(w, h, 0.36, U.mat(color, { emissive: color, emissiveIntensity: 0.25 }), x, y, 0); scene.add(m);
      ctx.label(text, [x + side * (w / 2 + (side < 0 ? -1.15 : 1.6)), y + (side < 0 ? 0.25 : 0), 0.3], cls); return m;
    };
    comp(xin, 6.45, 0.32, 0.3, 0x6c8db8, '衰減器 −20 dB');
    comp(xin, 3.75, 0.32, 0.3, 0x6c8db8, '衰減器 −20 dB');
    comp(xin, 2.45, 0.32, 0.3, 0x6c8db8, '衰減器 −20 dB');
    comp(xin, 1.85, 0.32, 0.3, 0x4f6f9a, '低通 / Eccosorb 濾波');
    const circ = new THREE.Mesh(new THREE.CylinderGeometry(0.28, 0.28, 0.2, 24), U.metal(0xb04a4a)); circ.rotation.z = Math.PI / 2; circ.position.set(xout, 1.75, 0); scene.add(circ);
    ctx.label('環行器 / 隔離器', [xout + 1.5, 1.75, 0.3], 'small');
    const twpa = comp(xout, 2.75, 0.42, 0.42, 0x38c6d9, 'TWPA / JPA（~20 dB）', 'teal', 1);
    const hemt = comp(xout, 6.45, 0.42, 0.42, 0x2ecc71, 'HEMT（~40 dB，T_N ≈ 2–4 K）', 'small', 1);
    const rtamp = comp(xout, 9.75, 0.42, 0.42, 0x8a9bb0, '室溫放大器', 'small', 1);
    // 室溫電子學
    const rt = [[-2.6, 'AWG / DAC'], [-0.9, 'IQ 混頻器 + LO'], [0.9, '下變頻 + ADC'], [2.6, 'FPGA 解調 / 判別']];
    rt.forEach(([x, t]) => { scene.add(U.box(1.4, 0.55, 0.9, U.mat(0x263248), x, 11.2, 0)); ctx.label(t, [x, 11.75, 0], 'small'); });
    scene.add(U.tube([[-2.6, 11.2, 0.5], [xin, 11.2, 0.5], [xin, 10.6, 0]], 0.03, U.metal(0x9fd3ff)));
    scene.add(U.tube([[xout, 10.6, 0], [xout, 11.2, 0.5], [2.6, 11.2, 0.5]], 0.03, U.metal(0xffd28a)));

    // 訊號封包
    const pkt = U.sphere(0.2, U.glow(0x9fd3ff)); scene.add(pkt);
    const halo = U.sphere(0.45, new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.15, depthWrite: false })); scene.add(halo);
    const pathPts = [[-2.6, 11.2, 0.5], [xin, 11.2, 0.5], [xin, 10.6, 0], [xin, 1.25, 0], [-0.7, 1.25, 0], [0, 1.0, 0], [0.7, 1.25, 0], [xout, 1.25, 0], [xout, 10.6, 0], [xout, 11.2, 0.5], [2.6, 11.2, 0.5]].map((p) => new THREE.Vector3(...p));
    const lens = [0]; for (let i = 1; i < pathPts.length; i++) lens.push(lens[i - 1] + pathPts[i].distanceTo(pathPts[i - 1]));
    const total = lens[lens.length - 1];
    const at = (s) => { for (let i = 1; i < lens.length; i++) if (s <= lens[i]) return pathPts[i - 1].clone().lerp(pathPts[i], (s - lens[i - 1]) / (lens[i] - lens[i - 1])); return pathPts[pathPts.length - 1].clone(); };
    const ro = ui.readout();
    let speed = 1;
    ui.slider('動畫速度', 0.3, 2.5, 0.1, speed, (v) => { speed = v; }, (v) => v.toFixed(1) + '×');
    const r = ui.row();
    ui.button('視角：整體', () => ctx.app.orbit.flyTo([14, 7, 18], [0, 5.6, 0]), r);
    ui.button('放大混合腔', () => ctx.app.orbit.flyTo([4.2, 2.6, 4.8], [0, 1.8, 0]), r);

    ctx.inset('訊號功率沿讀取鏈的變化（dBm）', (g, W, H, P) => {
      const pts = [['AWG', -50], ['4K', -70], ['CP', -90], ['MXC', -110], ['晶片', -120], ['TWPA', -101], ['HEMT', -63], ['RT', -33], ['ADC', -33]];
      const { X, Y } = P.frame(g, W, H, [0, pts.length - 1], [-130, -20], { ylabel: 'dBm', yticks: [[-120, '-120'], [-80, '-80'], [-40, '-40']], m: { b: 34 } });
      g.strokeStyle = '#e0a54a'; g.lineWidth = 2; g.beginPath(); pts.forEach(([, v], i) => (i ? g.lineTo(X(i), Y(v)) : g.moveTo(X(i), Y(v)))); g.stroke();
      pts.forEach(([n, v], i) => { P.dot(g, X(i), Y(v), 3.5, i <= 4 ? '#9fd3ff' : '#ffd28a'); P.text(g, n, X(i), H - 18, '#9fb0c8', 'center'); });
      const k = Math.min(pts.length - 1, (s / total) * (pts.length - 1));
      g.strokeStyle = 'rgba(56,198,217,.6)'; g.beginPath(); g.moveTo(X(k), Y(-130)); g.lineTo(X(k), Y(-20)); g.stroke();
    });

    let s = 0;
    return {
      update(time, dt) {
        s += dt * 1.6 * speed; if (s > total + 2) s = 0;
        const p = at(Math.min(s, total)); pkt.position.copy(p); halo.position.copy(p);
        const up = p.x > 0.6 && p.y > 1.2;
        let size = 0.2, noise = 0.15, txt = '';
        if (s < lens[3] + 0.01 && p.x < -0.5) {
          // 往下：逐級衰減
          const y = p.y; size = y > 6.45 ? 0.24 : y > 3.75 ? 0.18 : y > 2.45 ? 0.13 : 0.09;
          noise = y > 6.45 ? 0.5 : y > 3.75 ? 0.25 : y > 2.45 ? 0.12 : 0.05;
          txt = y > 6.45 ? '室溫脈衝 −50 dBm，伴隨 300 K 熱雜訊' : y > 3.75 ? '經 4 K 衰減器 −20 dB：熱雜訊被等比例壓低' : y > 2.45 ? '經 100 mK 衰減器 −20 dB' : '經 10 mK 衰減器 −20 dB → 抵達晶片 ≈ −120 dBm';
          pkt.material.color.setHex(0x9fd3ff);
        } else if (p.x > -0.7 && p.x < 0.7 && p.y < 1.4) {
          size = 0.09; noise = 0.05; txt = '探測微波與諧振腔作用：攜帶量子位元狀態資訊（相位）';
          pkt.material.color.setHex(0xffffff);
        } else if (up) {
          const y = p.y; size = y < 2.75 ? 0.09 : y < 6.45 ? 0.17 : y < 9.75 ? 0.25 : 0.3;
          noise = y < 2.75 ? 0.05 : y < 6.45 ? 0.08 : 0.12;
          txt = y < 2.75 ? '經環行器 → 進入 TWPA' : y < 6.45 ? 'TWPA 放大 ~20 dB（只加入 ~½ 光子雜訊）' : y < 9.75 ? 'HEMT 放大 ~40 dB（雜訊已被前級訊號壓過）' : '室溫放大 → 下變頻 → ADC → FPGA 判別 0 / 1';
          pkt.material.color.setHex(0xffd28a);
        } else txt = 'AWG 產生讀取脈衝（例如 7 GHz，數百 ns）';
        pkt.scale.setScalar(size / 0.2); halo.scale.setScalar((size + noise) / 0.45);
        halo.material.opacity = 0.08 + noise * 0.4;
        twpa.material.emissiveIntensity = up && Math.abs(p.y - 2.75) < 0.4 ? 1.2 : 0.25;
        hemt.material.emissiveIntensity = up && Math.abs(p.y - 6.45) < 0.4 ? 1.2 : 0.25;
        rtamp.material.emissiveIntensity = up && Math.abs(p.y - 9.75) < 0.4 ? 1.2 : 0.25;
        ro.innerHTML = `<b>${txt}</b><br>熱光子數 n_th = 1/(e^{hf/kT} − 1)：7 GHz 時 300 K ≈ 890，10 mK ≈ 10⁻¹⁵`;
      },
    };
  },
});
