/* 場景 12：操作量子電腦的完整流程 — 寫程式 → 轉譯 → 排程/脈衝 → 執行 shots → 讀取判別 → 結果 */
App.register({
  id: 'workflow', num: 12, short: '完整流程',
  title: '一次量子計算的完整流程',
  subtitle: '程式 → 轉譯 → 脈衝排程 → 控制電子 → 晶片重複執行 N 次 → 判別 → 直方圖',
  desc: `<p>跟著發光的「工作封包」走一遍：</p>
<p>① <b>寫程式</b>：用 Qiskit / Cirq 等描述線路，指定 shots。</p>
<p>② <b>轉譯（transpile）</b>：把閘拆成硬體的原生閘（如 RZ、√X、CZ），把邏輯量子位元對應到實體量子位元，不相鄰的要插入 SWAP，並最佳化。</p>
<p>③ <b>排程與脈衝</b>：每個閘換成校準好的微波/磁通脈衝，排到奈秒級的時間軸上。</p>
<p>④ <b>控制電子</b>把波形載入 AWG，觸發後送進冷凍機。</p>
<p>⑤ <b>每個 shot</b> = 重置 → 閘 → 讀取，重複 N 次。</p>
<p>⑥ 讀取訊號在 FPGA 判別成位元，累積成直方圖回傳給使用者。</p>
<p>右下插圖：一個 shot 的時間組成與整個工作的執行時間 —— 常常是<b>重置</b>而非計算本身佔最多時間。</p>`,
  camera: { pos: [0, 5.5, 12.5], target: [0, 0.2, 0] },
  build(ctx) {
    const { scene, U, THREE, ui } = ctx;
    const ST = [
      { x: -6.0, z: 0.0, name: '① 寫程式', col: 0x2e9e5b },
      { x: -3.6, z: -1.2, name: '② 轉譯', col: 0x1c9db0 },
      { x: -1.2, z: -1.8, name: '③ 脈衝排程', col: 0x8a5cd0 },
      { x: 1.2, z: -1.8, name: '④ 控制電子', col: 0xc8862a },
      { x: 3.6, z: -1.2, name: '⑤ 晶片執行 shots', col: 0x3b6fd8 },
      { x: 6.0, z: 0.0, name: '⑥ 判別與結果', col: 0xd9534f },
    ];
    const pads = ST.map((s, i) => {
      const m = U.box(2.0, 0.1, 1.6, U.mat(s.col, { emissive: s.col, emissiveIntensity: 0.1 }), s.x, -1.0, s.z); scene.add(m);
      ctx.label(s.name, [s.x, -1.0, s.z + 1.15], 'gold small');
      return m;
    });
    const path = ST.map((s) => [s.x, -0.75, s.z]);
    scene.add(U.smoothTube(path, 0.03, U.glow(0x6f8fbf, 0.6), false, 200));
    const curve = new THREE.CatmullRomCurve3(path.map((p) => new THREE.Vector3(...p)));
    const pkt = U.box(0.35, 0.35, 0.35, U.mat(0xffd28a, { emissive: 0xffd28a, emissiveIntensity: 0.9 })); scene.add(pkt);
    // ① 程式螢幕
    scene.add(U.box(1.6, 1.1, 0.08, U.mat(0x1a1f2b), -6.0, 0.0, -0.3));
    const code = ctx.label('<pre style="margin:0;font:11px Consolas,monospace;color:#bff6ff;text-align:left">qc = QuantumCircuit(2)\nqc.h(0)\nqc.cx(0, 1)\nqc.measure_all()\nsampler.run([qc], shots=N)</pre>', [-6.0, 0.0, -0.2], '');
    // ② 耦合圖（5 個實體量子位元，T 形）
    const cp = [[-4.2, -0.2, -1.6], [-3.6, -0.2, -1.6], [-3.0, -0.2, -1.6], [-3.6, -0.2, -1.0], [-3.6, -0.2, -0.4]];
    [[0, 1], [1, 2], [1, 3], [3, 4]].forEach(([a, b]) => scene.add(U.tube([cp[a], cp[b]], 0.02, U.mat(0x9fb7e0))));
    const cq = cp.map((p, i) => { const m = U.sphere(0.12, U.mat(0xe8eef8, { emissive: 0x1c9db0, emissiveIntensity: 0 }), ...p); scene.add(m); return m; });
    const mapL = [ctx.label('q0→Q3', [cp[3][0] + 0.45, cp[3][1] + 0.25, cp[3][2]], 'teal small'), ctx.label('q1→Q1', [cp[1][0], cp[1][1] + 0.35, cp[1][2]], 'teal small')];
    // ③ 時間軸
    const tl = new THREE.Group(); tl.position.set(-1.2, -0.3, -1.8); scene.add(tl);
    const chans = ['D0', 'D1', 'Z', 'M0', 'M1'];
    chans.forEach((c, i) => { tl.add(U.line([[-0.8, 0.6 - i * 0.25, 0], [0.85, 0.6 - i * 0.25, 0]], 0x6f8fbf, 0.6)); });
    const blocks = [[0, -0.6, 0.18, 0xe0a54a], [1, -0.6, 0.18, 0xe0a54a], [0, -0.3, 0.18, 0xe0a54a], [2, 0.0, 0.3, 0x38c6d9], [0, 0.35, 0.18, 0xe0a54a], [3, 0.65, 0.35, 0xff5a5f], [4, 0.65, 0.35, 0xff5a5f]];
    const bms = blocks.map(([ch, x, w, c]) => { const m = U.box(w, 0.16, 0.06, U.mat(c, { emissive: c, emissiveIntensity: 0.2 }), x, 0.6 - ch * 0.25, 0); tl.add(m); return m; });
    ctx.label('D=驅動 Z=磁通 M=讀取', [-1.2, 0.55, -1.8], 'small');
    // ④ 控制電子機櫃
    scene.add(U.box(1.1, 1.6, 0.8, U.mat(0x2a3346, { metalness: 0.4 }), 1.2, -0.15, -2.0));
    const leds = []; for (let k = 0; k < 6; k++) { const m = U.sphere(0.04, U.glow(0x2ecc71), 0.8 + k * 0.15, 0.45, -1.58); scene.add(m); leds.push(m); }
    ctx.label('AWG / LO / ADC / FPGA', [1.2, 0.95, -2.0], 'small');
    // ⑤ 冷凍機 + 晶片
    const fr = new THREE.Group(); fr.position.set(3.6, -0.9, -1.2); scene.add(fr);
    [0.55, 0.47, 0.4, 0.33].forEach((r, k) => fr.add(U.box(r * 2, 0.06, r * 2, U.metal(0xd4a24c), 0, 0.3 + k * 0.45, 0)));
    fr.add(U.box(0.5, 0.05, 0.5, U.mat(0x8c96a8), 0, 0.15, 0));
    const chipGlow = U.box(0.3, 0.06, 0.3, U.mat(0x4f8cff, { emissive: 0x4f8cff, emissiveIntensity: 0.2 }), 0, 0.2, 0); fr.add(chipGlow);
    const shotL = ctx.label('', [3.6, 1.35, -1.2], 'teal small');
    // ⑥ 直方圖
    const hb = [0, 1, 2, 3].map((k) => { const m = U.box(0.3, 1, 0.3, U.mat(k === 0 || k === 3 ? 0xe0a54a : 0x4a5468), 5.4 + k * 0.4, -0.95, 0); m.scale.y = 1e-3; scene.add(m); return m; });
    ['00', '01', '10', '11'].forEach((s, k) => ctx.label(s, [5.4 + k * 0.4, -1.15, 0.45], 'plain small'));

    let stage = 0, k = 0, autoRun = true, shots = 1000, active = false, depth = 20, done = 0, counts = [0, 0, 0, 0];
    const NOTES = [
      '使用者在筆電上寫線路、指定 shots，透過雲端 API 送出工作，進入佇列。',
      '轉譯器：H → RZ(π/2)·√X·RZ(π/2)；CNOT → H·CZ·H；選出錯誤率最低的實體量子位元（q0→Q3、q1→Q1），必要時插入 SWAP。',
      '每個原生閘換成「校準資料庫」裡的脈衝（振幅、頻率、DRAG、長度），排上奈秒級時間軸；RZ 只改相位（虛擬 Z）。',
      '波形與序列下載到 AWG/FPGA；所有儀器鎖在同一個 10 MHz 參考時脈，觸發後同步輸出。',
      '晶片上每個 shot：重置 → 執行閘 → 讀取，重複 N 次。量子態只活幾十～幾百 μs，所以每次都要重來。',
      'FPGA 把每個讀取訊號積分、判別成 0/1，累積成計數，回傳給使用者（可再做誤差緩解）。',
    ];
    const r = ui.row();
    ui.toggle('自動播放', autoRun, (v) => { autoRun = v; });
    ui.button('下一站 ▶', () => { autoRun = false; stage = (stage + 1) % 6; k = 0; if (stage === 0) { done = 0; counts = [0, 0, 0, 0]; } }, r);
    ui.slider('shots N', 2, 5, 0.1, Math.log10(shots), (v) => { shots = Math.round(10 ** v); }, (v) => Math.round(10 ** v).toLocaleString());
    ui.slider('線路深度（層）', 1, 1000, 1, depth, (v) => { depth = v; });
    ui.toggle('主動重置（量測 + 條件 π 脈衝）', active, (v) => { active = v; });
    const ro = ui.readout();
    const times = () => { const reset = active ? 2.0 : 250, gates = depth * 0.1, meas = 1.0; return { reset, gates, meas, shot: reset + gates + meas }; };

    ctx.inset('一個 shot 的時間組成（μs）與總執行時間', (g, W, H, P) => {
      const T = times();
      const x0 = 20, w = W - 40, tot = T.shot;
      const seg = [['重置', T.reset, '#8a5cd0'], ['閘', T.gates, '#e0a54a'], ['讀取', T.meas, '#ff5a5f']];
      let x = x0;
      seg.forEach(([n, v, c]) => { const ww = Math.max(2, (v / tot) * w); g.fillStyle = c; g.fillRect(x, 40, ww, 34); x += ww; });
      let y = 100;
      seg.forEach(([n, v, c]) => { g.fillStyle = c; g.fillRect(x0, y - 10, 12, 12); P.text(g, `${n}：${v < 10 ? v.toFixed(1) : v.toFixed(0)} μs（${((100 * v) / tot).toFixed(1)}%）`, x0 + 20, y, '#e8eef8'); y += 20; });
      const job = (T.shot * shots) / 1e6;
      P.text(g, `每 shot ${tot.toFixed(1)} μs × ${shots.toLocaleString()} shots = ${job < 1 ? (job * 1000).toFixed(1) + ' ms' : job.toFixed(2) + ' s'}`, x0, 178, '#ffd28a');
      P.text(g, '另加：佇列、轉譯、波形載入、網路傳輸（秒～分鐘）', x0, 200, '#9fb0c8');
      P.text(g, '數值為典型量級（依系統而異）', x0, 220, '#7f90a8');
    });

    return {
      update(t, dt) {
        k += dt / (stage === 4 ? 3.5 : 2.2);
        if (k >= 1 && autoRun) { k = 0; stage = (stage + 1) % 6; if (stage === 0) { done = 0; counts = [0, 0, 0, 0]; } }
        const kk = Math.min(1, k);
        const u0 = Math.max(0, (stage - 1) / 5), u1 = stage / 5;
        const u = u0 + (u1 - u0) * U.smooth(Math.min(1, kk / 0.4));
        pkt.position.copy(curve.getPoint(Math.min(1, u))).add(new THREE.Vector3(0, 0.35 + 0.08 * Math.sin(t * 6), 0));
        pkt.rotation.y += dt * 2;
        pads.forEach((m, i) => { m.material.emissiveIntensity = i === stage ? 0.6 : 0.08; });
        cq.forEach((m, i) => { m.material.emissiveIntensity = stage === 1 && (i === 1 || i === 3) ? 1 : 0; });
        mapL.forEach((L) => L.show(stage >= 1));
        bms.forEach((m, i) => { m.material.emissiveIntensity = stage === 2 && kk * blocks.length > i ? 0.9 : 0.15; });
        leds.forEach((m, i) => { m.visible = stage !== 3 || Math.sin(t * 20 + i) > 0; });
        if (stage === 4) {
          const target = Math.min(shots, Math.round(kk * shots)); while (done < target) { const b = Math.random() < 0.5 ? 0 : 3; const e = Math.random() < 0.04 ? [1, 2][Math.floor(Math.random() * 2)] : b; counts[e]++; done++; }
          chipGlow.material.emissiveIntensity = 0.3 + 0.7 * Math.abs(Math.sin(t * 25));
          shotL.set(`shot ${done.toLocaleString()} / ${shots.toLocaleString()}`); shotL.show(true);
        } else { chipGlow.material.emissiveIntensity = 0.2; shotL.show(stage === 5); }
        const tot = counts.reduce((a, b) => a + b, 0) || 1;
        hb.forEach((m, i) => { const h = stage >= 4 ? (counts[i] / tot) * 2.2 : 0; m.scale.y += (Math.max(1e-3, h) - m.scale.y) * 0.1; m.position.y = -0.95 + m.scale.y / 2; });
        const T = times();
        ro.innerHTML = `<b>${ST[stage].name}</b>：${NOTES[stage]}<br>每 shot ≈ ${T.shot.toFixed(1)} μs（${active ? '主動重置' : '被動等待 ~5T₁'}）` + (stage >= 4 ? `<br>目前計數：00 ${counts[0]}，01 ${counts[1]}，10 ${counts[2]}，11 ${counts[3]}` : '');
      },
    };
  },
});
