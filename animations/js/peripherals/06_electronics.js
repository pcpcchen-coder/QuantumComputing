/* 周邊場景 6：室溫控制電子學 — 波形產生、上/下變頻、數位化、即時回饋、時脈同步 */
App.register({
  id: 'electronics', num: 6, short: '控制電子學',
  title: '室溫控制電子學：產生與解讀每一個微波脈衝',
  subtitle: 'AWG/DAC · LO · IQ 混頻 · ADC · FPGA 即時回饋 · DC 源 · 10 MHz 參考時脈',
  desc: `<p>一次「量測—回饋」循環（動畫依序播放）：</p>
<p>① 控制電腦把編譯好的<b>脈衝序列</b>上傳到儀器，由<b>同步器</b>統一觸發。<br>
② <b>AWG/DAC</b> 產生中頻 I/Q 包絡，與 <b>LO</b> 在 IQ 混頻器上變頻到 4–8 GHz（或用<b>直接射頻合成</b>一步產生），送入冷凍機驅動量子位元。<br>
③ 讀取模組送出讀取脈衝，回來的訊號被下變頻、<b>ADC</b> 取樣、<b>FPGA</b> 解調判別。<br>
④ 判別結果在數百奈秒內<b>回饋</b>給 AWG（例如主動重置的 π 脈衝）。<br>
⑤ 結果回傳電腦。</p>
<p>所有儀器鎖在同一個 <b>10 MHz 參考時脈</b>（常用銣原子鐘）與觸發網路上，確保相位一致、時序精確。<b>DC 電流源</b>提供磁通偏壓；另有 HEMT 偏壓與 TWPA 泵浦源。</p>`,
  camera: { pos: [4.0, 3.8, 12], target: [0.3, 2.0, 0] },
  build(ctx) {
    const { scene, U, THREE, ui } = ctx;
    const floor = new THREE.Mesh(new THREE.PlaneGeometry(16, 8), U.mat(0x1a2130, { roughness: 0.95 })); floor.rotation.x = -Math.PI / 2; scene.add(floor);
    const RX = -1.6;
    scene.add(U.box(1.5, 4.3, 1.0, U.mat(0x202838, { roughness: 0.6 }), RX, 2.15, 0));
    const mods = [
      ['clock', '銣原子鐘 / 10 MHz 分配', 0xffd166],
      ['sync', '同步器 / 觸發分配', 0x38c6d9],
      ['awg', 'AWG / DAC（XY 驅動）', 0x4f8cff],
      ['lo', 'LO 合成器', 0x2ecc71],
      ['mix', 'IQ 混頻器（上變頻）', 0x6fb4ff],
      ['ro', '讀取模組：AWG + 下變頻 + ADC', 0xe0a54a],
      ['fpga', 'FPGA 即時處理 / 回饋', 0xff7a59],
      ['dc', 'DC 電流源（磁通偏壓）', 0x9ad1a0],
      ['bias', 'HEMT 偏壓 · TWPA 泵浦源', 0xb07cff],
    ];
    const M = {};
    mods.forEach(([k, name, col], i) => {
      const y = 3.95 - i * 0.43;
      const m = U.box(1.3, 0.34, 0.06, U.mat(0x111827, { emissive: col, emissiveIntensity: 0.12 }), RX, y, 0.52);
      scene.add(m);
      for (let j = 0; j < 4; j++) scene.add(U.sphere(0.022, U.glow(col), RX - 0.5 + j * 0.09, y + 0.08, 0.56, 8));
      M[k] = { m, y, col, base: 0.12 };
      ctx.label(name, [RX - 1.75, y, 0.5], 'small');
    });
    // 控制電腦
    App.device(ctx, { pos: [-5.6, 0, 0], w: 0.8, h: 1.6, d: 0.8, label: '控制電腦', leds: 2 });
    // 冷凍機頂板（示意）
    const top = new THREE.Mesh(new THREE.CylinderGeometry(1.1, 1.1, 0.12, 40), U.metal(0x9aa4b2)); top.position.set(3.4, 3.2, 0); scene.add(top);
    const can = new THREE.Mesh(new THREE.CylinderGeometry(1.0, 1.0, 3.1, 40, 1, true), new THREE.MeshStandardMaterial({ color: 0xaab6c8, transparent: true, opacity: 0.15, side: THREE.DoubleSide, depthWrite: false })); can.position.set(3.4, 1.6, 0); scene.add(can);
    ctx.label('冷凍機頂板（密封接頭）', [3.4, 3.65, 0], 'gold');
    const chip = U.box(0.3, 0.12, 0.3, U.metal(0xd08a3a, { emissive: 0x000000 }), 3.4, 0.4, 0); scene.add(chip);
    ctx.label('量子晶片 10 mK', [3.4, 0.05, 0.6], 'small');
    // 固定纜線
    const cab = (pts, col) => scene.add(U.tube(pts, 0.02, U.mat(col, { transparent: true, opacity: 0.45 })));
    const P = {
      pcSync: [[-5.2, 1.4, 0.4], [-3.0, 1.4, 0.4], [-3.0, M.sync.y, 0.6], [RX - 0.7, M.sync.y, 0.6]],
      syncAwg: [[RX + 0.66, M.sync.y, 0.6], [RX + 0.9, M.sync.y, 0.6], [RX + 0.9, M.awg.y, 0.6], [RX + 0.66, M.awg.y, 0.6]],
      syncRo: [[RX + 0.66, M.sync.y, 0.62], [RX + 1.0, M.sync.y, 0.62], [RX + 1.0, M.ro.y, 0.62], [RX + 0.66, M.ro.y, 0.62]],
      awgMix: [[RX + 0.66, M.awg.y, 0.5], [RX + 1.15, M.awg.y, 0.5], [RX + 1.15, M.mix.y, 0.5], [RX + 0.66, M.mix.y, 0.5]],
      loMix: [[RX + 0.66, M.lo.y, 0.45], [RX + 0.8, M.lo.y, 0.45], [RX + 0.8, M.mix.y, 0.45]],
      mixFr: [[RX + 0.66, M.mix.y, 0.3], [2.6, M.mix.y, 0.3], [2.6, 3.3, 0.3], [3.2, 3.3, 0.3], [3.2, 0.5, 0.1]],
      awgFr: [[RX + 0.66, M.awg.y, 0.25], [2.5, M.awg.y, 0.25], [2.5, 3.3, 0.25], [3.15, 3.3, 0.2], [3.15, 0.5, 0.1]],
      roFr: [[RX + 0.66, M.ro.y, 0.2], [2.4, M.ro.y, 0.2], [2.4, 3.3, 0.0], [3.3, 3.3, 0.0], [3.3, 0.5, 0.0]],
      frRo: [[3.55, 0.5, -0.1], [3.55, 3.3, -0.1], [2.3, 3.3, -0.2], [2.3, M.ro.y - 0.05, 0.2], [RX + 0.66, M.ro.y - 0.05, 0.2]],
      roFpga: [[RX + 0.66, M.ro.y - 0.08, 0.55], [RX + 1.1, M.ro.y - 0.08, 0.55], [RX + 1.1, M.fpga.y, 0.55], [RX + 0.66, M.fpga.y, 0.55]],
      fpgaAwg: [[RX + 0.66, M.fpga.y, 0.65], [RX + 1.3, M.fpga.y, 0.65], [RX + 1.3, M.awg.y, 0.65], [RX + 0.66, M.awg.y, 0.65]],
      fpgaPc: [[RX - 0.7, M.fpga.y, 0.6], [-3.2, M.fpga.y, 0.6], [-3.2, 1.2, 0.4], [-5.2, 1.2, 0.4]],
      dcFr: [[RX + 0.66, M.dc.y, 0.15], [2.7, M.dc.y, 0.15], [2.7, 3.3, -0.3], [3.6, 3.3, -0.3], [3.6, 0.5, -0.2]],
      biasFr: [[RX + 0.66, M.bias.y, 0.1], [2.8, M.bias.y, 0.1], [2.8, 3.3, -0.45], [3.7, 3.3, -0.45], [3.7, 2.0, -0.4]],
    };
    Object.entries(P).forEach(([k, pts]) => cab(pts, k.includes('Fr') || k === 'frRo' ? 0xff9f43 : 0x38c6d9));
    // 時脈分配
    const clkPts = mods.slice(1).map(([k]) => M[k].y);
    scene.add(U.tube([[RX - 0.75, M.clock.y, 0.45], [RX - 0.75, M.bias.y, 0.45]], 0.015, U.mat(0xffd166, { transparent: true, opacity: 0.5 })));
    const clkPulses = clkPts.map((y) => { const s = U.sphere(0.05, U.glow(0xffd166)); s.position.set(RX - 0.75, y, 0.45); scene.add(s); return s; });
    // 封包
    const pk = U.sphere(0.1, U.glow(0xffffff)); scene.add(pk); pk.visible = false;
    const pk2 = U.sphere(0.08, U.glow(0x9ad1a0)); scene.add(pk2);
    const lens = (pts) => { const v = pts.map((p) => new THREE.Vector3(...p)); const L = [0]; for (let i = 1; i < v.length; i++) L.push(L[i - 1] + v[i].distanceTo(v[i - 1])); return { v, L }; };
    const along = (pts, f) => { const { v, L } = lens(pts); const s = f * L[L.length - 1]; for (let i = 1; i < v.length; i++) if (s <= L[i]) return v[i - 1].clone().lerp(v[i], (s - L[i - 1]) / (L[i] - L[i - 1] || 1)); return v[v.length - 1].clone(); };
    let mode = 'iq';
    ui.radio([['iq', '外差 IQ 混頻架構'], ['direct', '直接射頻合成（RFSoC 等）']], 'iq', (m) => { mode = m; });
    let speed = 1;
    ui.slider('播放速度', 0.3, 2, 0.1, speed, (v) => { speed = v; }, (v) => v.toFixed(1) + '×');
    const ro = ui.readout();
    const stepLbl = ctx.label('', [0.8, 4.9, 0], 'big teal');
    let cyc = 0;
    const seq = () => {
      const s = [
        { d: 0.7, path: 'pcSync', col: 0x38c6d9, t: '① 上傳脈衝序列 → 同步器', glow: ['sync'] },
        { d: 0.6, path: 'syncAwg', col: 0x38c6d9, t: '② 同步觸發', glow: ['awg', 'ro'] },
      ];
      if (mode === 'iq') s.push({ d: 0.6, path: 'awgMix', col: 0x4f8cff, t: '② AWG 中頻 I/Q → 混頻器', glow: ['awg', 'lo', 'mix'] }, { d: 1.0, path: 'mixFr', col: 0x4f8cff, t: '② 上變頻 → XY 驅動脈衝進入冷凍機', glow: ['mix'] });
      else s.push({ d: 1.1, path: 'awgFr', col: 0x4f8cff, t: '② 直接合成 GHz 脈衝 → 冷凍機', glow: ['awg'] });
      s.push(
        { d: 1.0, path: 'roFr', col: 0xe0a54a, t: '③ 讀取脈衝 → 晶片', glow: ['ro'] },
        { d: 1.0, path: 'frRo', col: 0xffd28a, t: '③ 讀取訊號返回 → 下變頻 + ADC', glow: ['ro'] },
        { d: 0.5, path: 'roFpga', col: 0xff7a59, t: '③ FPGA 解調、判別 0 / 1', glow: ['fpga'] },
        { d: 0.6, path: 'fpgaAwg', col: 0xff7a59, t: '④ 即時回饋（~0.35–0.55 μs）→ AWG', glow: ['fpga', 'awg'] },
        { d: 1.0, path: mode === 'iq' ? 'mixFr' : 'awgFr', col: 0xff5a5f, t: '④ 條件式 π 脈衝（主動重置）', glow: ['awg'] },
        { d: 0.8, path: 'fpgaPc', col: 0x38c6d9, t: '⑤ 結果回傳電腦', glow: ['fpga'] },
      );
      return s;
    };
    ctx.inset('XY 驅動波形：中頻 I/Q 包絡 → 4–8 GHz 載波', (g, W, H, Pl) => {
      const { X, Y } = Pl.frame(g, W, H, [0, 1], [-1.2, 1.2], { xlabel: '時間（~40 ns 脈衝）', ylabel: '振幅', yticks: [[-1, '-1'], [0, '0'], [1, '1']] });
      const env = (t) => Math.exp(-(((t - 0.5) / 0.16) ** 2));
      const dr = (t) => (-(t - 0.5) / 0.0256) * env(t) * 0.05;
      Pl.curve(g, (t) => env(t) * Math.cos(2 * Math.PI * 22 * t) * 0.95, 0, 1, X, Y, 'rgba(79,140,255,.55)', 1, 600);
      Pl.curve(g, env, 0, 1, X, Y, '#e0a54a', 2.2);
      Pl.curve(g, dr, 0, 1, X, Y, '#38c6d9', 2.2);
      Pl.text(g, 'I：高斯包絡', X(0.68), Y(0.85), '#e0a54a'); Pl.text(g, 'Q：DRAG 修正', X(0.68), Y(0.35), '#38c6d9'); Pl.text(g, '上變頻後的 RF', X(0.02), Y(-1.0), '#6fb4ff');
    });
    let clkT = 0;
    return {
      update(time, dt) {
        const S = seq(); const total = S.reduce((a, b) => a + b.d, 0);
        cyc = (cyc + dt * speed) % (total + 0.6);
        let acc = 0, cur = null, f = 0;
        for (const s of S) { if (cyc < acc + s.d) { cur = s; f = (cyc - acc) / s.d; break; } acc += s.d; }
        Object.values(M).forEach((m) => (m.m.material.emissiveIntensity = m.base));
        ['lo', 'mix'].forEach((k) => (M[k].m.material.emissiveIntensity = mode === 'iq' ? 0.12 : 0.02));
        if (cur) {
          pk.visible = true; pk.position.copy(along(P[cur.path], f)); pk.material.color.setHex(cur.col);
          cur.glow.forEach((k) => (M[k].m.material.emissiveIntensity = 0.9));
          stepLbl.set(cur.t);
          chip.material.emissive.setHex(cur.path.endsWith('Fr') && f > 0.8 ? cur.col : 0x000000); chip.material.emissiveIntensity = 0.8;
        } else { pk.visible = false; stepLbl.set('（等待下一個循環）'); }
        // 磁通 DC（持續）
        pk2.position.copy(along(P.dcFr, (time * 0.25) % 1));
        // 10 MHz 時脈脈衝
        clkT += dt; const pulse = (clkT % 1) < 0.15;
        clkPulses.forEach((s) => s.scale.setScalar(pulse ? 1.6 : 0.8));
        M.clock.m.material.emissiveIntensity = pulse ? 0.9 : 0.25;
        ro.innerHTML = (mode === 'iq'
          ? '外差架構：AWG（~1–2 GSa/s）產生中頻，LO + IQ 混頻器上變頻；需校正 IQ 不平衡與 LO 洩漏'
          : '直接合成：高速 DAC（數 GSa/s）+ 數位上變頻，直接輸出 GHz 訊號；省去類比混頻器與校正') +
          '<br>回饋延遲（文獻/廠商值）：單機 ~350 ns，跨機櫃 < 550 ns';
      },
    };
  },
});
