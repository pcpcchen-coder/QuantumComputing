/* 離子阱場景 5：Mølmer–Sørensen 兩位元閘 — 自旋相依力、相空間迴圈、幾何相位與糾纏 */
App.register({
  id: 'ms', num: 5, short: 'Mølmer–Sørensen 閘',
  title: 'Mølmer–Sørensen 閘：讓振動在相空間繞一圈',
  subtitle: '雙色雷射推動離子的集體振動；振動繞完一個圓回到原點時，只留下兩顆離子之間的糾纏',
  desc: `<p><b>雙色雷射</b>：兩道光的頻率分別是 <span class="eq">ω₀ ± (ω_m + δ)</span>（ω₀：量子位元頻率，ω_m：振動模頻率，δ：小失諧）。合起來對每顆離子產生一個<b>自旋相依力</b>：自旋 σ<sub>x</sub> = +1 往一邊推、−1 往另一邊推。</p>
<p><b>相空間迴圈</b>：振動模態的狀態 α(t) = (ηΩ/δ)(e<sup>iδt</sup> − 1) 在相空間畫圓。兩顆離子自旋相同（S<sub>x</sub> = ±2）的分量往相反方向繞，自旋相反（S<sub>x</sub> = 0）的分量不動。</p>
<p><b>關鍵</b>：在 <b>t = 2πK/δ</b> 時所有迴圈都回到原點，振動回到原來的狀態（不管原本多熱），只留下和圓面積成正比的<b>幾何相位</b> → 等效於 <span class="eq">exp(−iπ/4 · σ<sub>x</sub>σ<sub>x</sub>)</span>。從 |00⟩ 出發得到 (|00⟩ − i|11⟩)/√2。</p>
<p><b>Lamb–Dicke 參數</b> η ≈ 0.1：光子動量能推動離子多少。閘時間由 δ 決定，代表值 10–200 μs；保真度 &gt; 99.9%（Quantinuum Helios 2025：99.921%）。若在迴圈還沒閉合時停下，自旋和振動仍然糾纏 → 錯誤。</p>
<p><b>其他做法</b>：Quantinuum 用 σ<sub>z</sub> 光位移的 <b>ZZ 閘</b>（原理相同，力改成依 σ<sub>z</sub>）；Oxford Ionics / IonQ 用<b>電子式控制</b>（微波 + 磁場梯度產生自旋相依力，不需要閘雷射）。</p>`,
  camera: { pos: [0, 2.2, 9.6], target: [0, 1.15, 0] },
  build(ctx) {
    const { scene, U, THREE, ui } = ctx;
    /* ---------- 左：兩顆離子與雙色雷射 ---------- */
    const I0 = new THREE.Vector3(-2.8, 1.2, 0), SEP = 0.9;
    [[1, 1], [-1, -1], [1, -1], [-1, 1]].forEach(([a, b], k) => {
      const m = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 3.4, 12), U.metal(k < 2 ? 0xd9a441 : 0x8a93a0, { transparent: true, opacity: 0.3 }));
      m.rotation.z = Math.PI / 2; m.position.set(I0.x, I0.y + a * 0.8, b * 0.8); scene.add(m);
    });
    const ions = [-1, 1].map((s) => App.particle(scene, App.QC.ion, 0.12, [I0.x + (s * SEP) / 2, I0.y, 0]));
    const gp = [-1, 1].map(() => U.sphere(0.12, new THREE.MeshBasicMaterial({ color: 0xff5a5f, transparent: true, opacity: 0.45, depthWrite: false }), 0, 0, 0, 16));
    const gm = [-1, 1].map(() => U.sphere(0.12, new THREE.MeshBasicMaterial({ color: 0x4f8cff, transparent: true, opacity: 0.45, depthWrite: false }), 0, 0, 0, 16));
    [...gp, ...gm].forEach((m) => scene.add(m));
    const bA = App.beam(scene, [I0.x - 1.6, -0.6, 0.4], I0, 0x7f5cff, 0.05, 0.5);
    const bB = App.beam(scene, [I0.x + 1.6, -0.6, 0.4], I0, 0xd46cff, 0.05, 0.5);
    ctx.label('ω₀ + (ω_m + δ)', [I0.x - 1.75, -0.35, 0.4], 'small');
    ctx.label('ω₀ − (ω_m + δ)', [I0.x + 1.75, -0.35, 0.4], 'small');
    ctx.label('離子 1　　離子 2', [I0.x, I0.y + 0.55, 0], 'gold');
    const lbForce = ctx.label('', [I0.x, I0.y - 0.95, 0], 'small');
    /* ---------- 右：相空間 ---------- */
    const C = new THREE.Vector3(2.4, 1.2, 0), HS = 1.75;
    const plane = new THREE.Mesh(new THREE.PlaneGeometry(2 * HS, 2 * HS), new THREE.MeshBasicMaterial({ color: 0x14203a, transparent: true, opacity: 0.7, side: THREE.DoubleSide }));
    plane.position.copy(C); plane.position.z = -0.02; scene.add(plane);
    const grid = new THREE.GridHelper(2 * HS, 10, 0x2b3a55, 0x22304a); grid.rotation.x = Math.PI / 2; grid.position.copy(C); grid.position.z = -0.01; scene.add(grid);
    scene.add(U.line([[C.x - HS, C.y, 0], [C.x + HS, C.y, 0]], 0x9fb0c8, 0.7));
    scene.add(U.line([[C.x, C.y - HS, 0], [C.x, C.y + HS, 0]], 0x9fb0c8, 0.7));
    ctx.label('位置 x', [C.x + HS - 0.3, C.y - 0.2, 0], 'small');
    ctx.label('動量 p', [C.x + 0.4, C.y + HS - 0.15, 0], 'small');
    ctx.label('振動模態的相空間', [C.x, C.y + HS + 0.3, 0], 'gold');
    const trP = U.dynLine(600, 0xff5a5f), trM = U.dynLine(600, 0x4f8cff);
    scene.add(trP.obj, trM.obj);
    const dP = App.particle(scene, 0xff5a5f, 0.07), dM = App.particle(scene, 0x4f8cff, 0.07), d0 = App.particle(scene, 0xffffff, 0.06, C.toArray());
    const lbP = ctx.label('S_x = +2（|++⟩）', [0, 0, 0], 'q1'), lbM = ctx.label('S_x = −2（|−−⟩）', [0, 0, 0], 'q0');
    ctx.label('S_x = 0 不動', [C.x - 0.85, C.y - 0.3, 0], 'small');
    const lbState = ctx.label('', [C.x, C.y - HS - 0.4, 0], 'big');

    /* ---------- 物理 ---------- */
    let fk = 10, K = 1, stopFrac = 1, s = 0, running = false;
    const sEnd = () => 2 * Math.PI * K * stopFrac;
    const A = () => 1 / (4 * Math.sqrt(K)); // ηΩ/δ（使 t = 2πK/δ 時 2Φ = π/4）
    const alpha = (ss) => [A() * (Math.cos(ss) - 1), A() * Math.sin(ss)];
    const Phi = (ss) => (A() * A()) * (ss - Math.sin(ss));
    const VS = 4.0 / Math.sqrt(1); // 相空間顯示比例
    const usOf = (ss) => (ss / (2 * Math.PI * fk)) * 1000;
    const ro = ui.readout();
    const traj = (sign) => { const pts = []; const n = 300; for (let i = 0; i <= n; i++) { const ss = (s * i) / n; const [x, p] = alpha(ss); pts.push([C.x + sign * x * VS, C.y + sign * p * VS, 0.01]); } return pts; };
    ui.button('▶ 執行閘', () => { s = 0; running = true; });
    ui.slider('失諧 δ/2π (kHz)', 5, 50, 1, fk, (v) => { fk = v; }, (v) => `${v} kHz → 閘時間 ${(1000 * K / v).toFixed(0)} μs`);
    ui.slider('停止時刻（迴圈比例）', 0.1, 1.0, 0.05, stopFrac, (v) => { stopFrac = v; s = Math.min(s, sEnd()); }, (v) => `${(v * 100).toFixed(0)}%`);
    ui.toggle('顯示 2 個迴圈（K=2）', false, (on) => { K = on ? 2 : 1; s = 0; running = true; });

    ctx.inset('布居數與運動位移 vs 時間', (g, W, H, P) => {
      const S = 2 * Math.PI * K;
      const { X, Y } = P.frame(g, W, H, [0, S], [0, 1.05], { xlabel: `時間 (μs)，閘時間 = ${usOf(S).toFixed(0)} μs`, xticks: [[0, '0'], [S / 2, usOf(S / 2).toFixed(0)], [S, usOf(S).toFixed(0)]], yticks: [[0, '0'], [0.5, '0.5'], [1, '1']], m: { l: 34 } });
      P.curve(g, (x) => Math.cos(2 * Phi(x)) ** 2, 0, S, X, Y, '#4f8cff', 2);
      P.curve(g, (x) => Math.sin(2 * Phi(x)) ** 2, 0, S, X, Y, '#ff5a5f', 2);
      g.setLineDash([4, 3]);
      P.curve(g, (x) => Math.hypot(...alpha(x)) / (2 * A()), 0, S, X, Y, '#9fb0c8', 1.5);
      g.setLineDash([]);
      P.curve(g, () => 0.005, 0, S, X, Y, '#c58bff', 1.5, 2);
      g.strokeStyle = '#ffd28a'; g.beginPath(); g.moveTo(X(s), Y(0)); g.lineTo(X(s), Y(1.05)); g.stroke();
      P.text(g, 'P(00)', X(S * 0.06), Y(0.9), '#a9c6ff');
      P.text(g, 'P(11)', X(S * 0.06), Y(0.14), '#ffb0b2');
      P.text(g, '|α|（運動位移，虛線）', X(S * 0.5), Y(1.0), '#cfd8e6', 'center');
      P.text(g, 'P(01)+P(10) = 0', X(S * 0.98), Y(0.06), '#d7b8ff', 'right');
    });

    return {
      update(time, dt) {
        if (running) { s += dt * ((2 * Math.PI * K) / 5); if (s >= sEnd()) { s = sEnd(); running = false; } }
        const [x, p] = alpha(s);
        trP.set(traj(1)); trM.set(traj(-1));
        dP.position.set(C.x + x * VS, C.y + p * VS, 0.02); dM.position.set(C.x - x * VS, C.y - p * VS, 0.02);
        lbP.pos.set(C.x + x * VS + 0.1, C.y + p * VS + 0.28, 0); lbM.pos.set(C.x - x * VS - 0.1, C.y - p * VS - 0.28, 0);
        const amp = Math.hypot(x, p);
        lbP.show(amp > 0.02); lbM.show(amp > 0.02);
        // 離子：σx 分量的「影子」往相反方向位移（位移 ∝ Re α）
        const osc = x * 2.2;
        [0, 1].forEach((i) => {
          const bx = I0.x + ((i ? 1 : -1) * SEP) / 2;
          gp[i].position.set(bx, I0.y + osc, 0); gm[i].position.set(bx, I0.y - osc, 0);
          gp[i].visible = gm[i].visible = amp > 0.005;
          ions[i].position.set(bx, I0.y, 0); ions[i].glow(running ? 0.9 : 0.5);
        });
        const on = running || (s > 0 && s < sEnd());
        bA.on(running, 0.6); bB.on(running, 0.6);
        lbForce.set(amp > 0.005 ? '紅影：σx=+1 分量　藍影：σx=−1 分量（自旋相依力推向相反方向）' : '');
        const P00 = Math.cos(2 * Phi(s)) ** 2, P11 = Math.sin(2 * Phi(s)) ** 2;
        const closed = amp < 1e-3 && s > 0.1;
        const atEnd = Math.abs(s - 2 * Math.PI * K) < 1e-6;
        lbState.set(s < 1e-6 ? '|00⟩' : atEnd ? '(|00⟩ − i|11⟩)/√2　最大糾纏' : `√${P00.toFixed(2)}|00⟩ − i√${P11.toFixed(2)}|11⟩` + (closed ? '' : '　⚠ 迴圈未閉合'));
        ro.innerHTML = `時間：${usOf(s).toFixed(1)} μs / 閘時間 ${usOf(2 * Math.PI * K).toFixed(0)} μs（δ/2π = ${fk} kHz，K = ${K}）<br>`
          + `P(00) = ${P00.toFixed(3)}，P(11) = ${P11.toFixed(3)}，幾何相位 2Φ = ${(2 * Phi(s) / Math.PI).toFixed(3)} π<br>`
          + (s < 1e-6 ? '按「▶ 執行閘」' : closed ? '<b style="color:#8ef0a0">迴圈閉合：振動回到原狀態，自旋和振動解開糾纏</b>' : `<b style="color:#ff8a8a">迴圈未閉合（|α| = ${amp.toFixed(3)}）：自旋與運動仍糾纏 → 錯誤</b>`)
          + (on ? '' : '');
      },
    };
  },
});
