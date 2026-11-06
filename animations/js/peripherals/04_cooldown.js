/* 周邊場景 4：降溫流程 — 抽真空 → 脈衝管預冷 → 凝結混合氣 → 循環至基溫 */
App.register({
  id: 'cooldown', num: 4, short: '降溫流程',
  title: '降溫流程：從室溫到 10 mK',
  subtitle: '乾式稀釋冷凍機一次完整降溫約 1–2 天；升溫回室溫也需約 1 天',
  desc: `<p><b>① 抽真空</b>：外真空罩（OVC）以泵抽到高真空，避免氣體對流導熱；同時檢漏。</p>
<p><b>② 脈衝管預冷</b>：50 K、4 K 板由脈衝管冷卻；下方各級靠預冷迴路／熱開關跟著降到約 4 K。這是最耗時的階段（受各級熱容量影響）。</p>
<p><b>③ 凝結混合氣</b>：GHS 把 ³He/⁴He 混合氣送入，在 4 K 與流阻處凝結成液體填入混合腔與 Still。</p>
<p><b>④ 循環</b>：啟動渦輪泵抽 Still、開 Still 加熱，稀釋循環開始 → MXC 在數小時內降到 ~10 mK。</p>
<p>樣品若要更換，需整機升溫、開罐、再降溫 —— 所以晶片更換週期通常以「天」計。</p>`,
  camera: { pos: [6.5, 4.0, 8], target: [0, 2.0, 0] },
  build(ctx) {
    const { scene, U, THREE, ui } = ctx;
    const fr = App.buildFridge(ctx, { canOpacity: 0.16 });
    const st = App.PD.stages;
    st.forEach((s) => ctx.label(s.name, [-s.r - 1.0, s.y, 0], 'small'));
    const tLbls = st.map((s) => ctx.label('', [s.r + 0.9, s.y, 0], 'gold small'));
    const phaseLbl = ctx.label('', [0, 5.3, 0], 'big teal');
    // 凝結的混合液滴
    const drops = []; for (let i = 0; i < 30; i++) { const m = U.sphere(0.035, U.glow(0x8ef0ff)); m.visible = false; scene.add(m); drops.push({ m, y: 3.3 - Math.random() * 2.6, x: (Math.random() - 0.5) * 0.3, z: (Math.random() - 0.5) * 0.3 }); }
    const TMODEL = (t) => {
      // 回傳各級溫度（K）
      const pre = (tau, Tend, t0 = 2) => (t < t0 ? 300 : Tend + (300 - Tend) * Math.exp(-(t - t0) / tau));
      const T50 = pre(5.5, 45), T4 = pre(7.5, 3.4, 2.3);
      let Tl = pre(8.5, 4.2, 3);
      const Tlow = [Tl, Tl, Tl];
      if (t > 25) {
        const k = Math.min(1, (t - 25) / 2.5); // 凝結：降到 ~1 K
        Tlow.fill(Math.exp(Math.log(Tl) + (Math.log(1.0) - Math.log(Tl)) * k));
      }
      if (t > 27.5) {
        const u = t - 27.5;
        Tlow[0] = 0.8 + 0.2 * Math.exp(-u / 0.6);
        Tlow[1] = 0.1 + 0.9 * Math.exp(-u / 1.2);
        Tlow[2] = 0.01 + 0.99 * Math.exp(-u / 1.0);
      }
      return [300, T50, T4, ...Tlow];
    };
    const phase = (t) => (t < 2 ? '① 抽真空 / 檢漏' : t < 25 ? '② 脈衝管預冷' : t < 27.5 ? '③ 凝結混合氣' : t < 33 ? '④ 稀釋循環 → 基溫' : '✓ 基溫穩定，可開始量測');
    let t = 0, play = true, rate = 1.0; // 小時 / 秒
    const sl = ui.slider('時間 (小時)', 0, 36, 0.1, t, (v) => { t = v; }, (v) => v.toFixed(1) + ' h');
    const r = ui.row();
    const pb = ui.button('⏸ 暫停', () => { play = !play; pb.textContent = play ? '⏸ 暫停' : '▶ 播放'; }, r);
    ui.button('⟲ 重新開始', () => { t = 0; play = true; pb.textContent = '⏸ 暫停'; }, r);
    ui.slider('播放速度（小時/秒）', 0.2, 4, 0.1, rate, (v) => { rate = v; }, (v) => v.toFixed(1));
    const ro = ui.readout();
    const qt = new URLSearchParams(location.search).get('t');
    if (qt !== null) { t = +qt; play = false; pb.textContent = '▶ 播放'; sl.show(t); }
    const curves = st.map(() => []);
    for (let k = 0; k <= 360; k++) { const tt = k / 10; TMODEL(tt).forEach((T, i) => curves[i].push([tt, T])); }
    const cols = ['#ff7a59', '#e0a54a', '#2ecc71', '#38c6d9', '#4f8cff', '#b07cff'];
    ctx.inset('各級溫度隨時間（對數座標）', (g, W, H, P) => {
      const { X, Y } = P.frame(g, W, H, [0, 36], [-2.2, 2.6], { xlabel: '時間 (h)', ylabel: '溫度', xticks: [[0, '0'], [12, '12'], [24, '24'], [36, '36']], yticks: [[-2, '10 mK'], [-1, '100 mK'], [0, '1 K'], [1, '10 K'], [2, '100 K']], m: { l: 54 } });
      curves.forEach((c, i) => { g.strokeStyle = cols[i]; g.lineWidth = 1.8; g.beginPath(); c.forEach(([x, T], k) => (k ? g.lineTo(X(x), Y(Math.log10(T))) : g.moveTo(X(x), Y(Math.log10(T))))); g.stroke(); });
      g.strokeStyle = 'rgba(255,255,255,.6)'; g.beginPath(); g.moveTo(X(t), Y(-2.2)); g.lineTo(X(t), Y(2.6)); g.stroke();
    });
    const fmtT = (T) => (T >= 1 ? T.toFixed(T >= 10 ? 0 : 1) + ' K' : (T * 1000).toFixed(T < 0.1 ? 1 : 0) + ' mK');
    return {
      update(time, dt) {
        if (play) { t = Math.min(36, t + dt * rate); sl.show(t); }
        const T = TMODEL(t);
        fr.plates.forEach((p, i) => { p.material.color.copy(App.tempColor(T[i])); p.material.emissive = App.tempColor(T[i]); p.material.emissiveIntensity = 0.25; tLbls[i].set(fmtT(T[i])); });
        fr.box.material.emissive = App.tempColor(T[5]); fr.box.material.emissiveIntensity = 0.3;
        phaseLbl.set(phase(t));
        const cond = t > 25 && t < 28;
        drops.forEach((d) => { d.m.visible = cond; if (cond) { d.y -= dt * 0.8; if (d.y < 0.6) d.y = 3.3; d.m.position.set(d.x, d.y, d.z); } });
        const pOVC = t < 2 ? 1e5 * Math.pow(1e-9, t / 2) : 1e-4 * Math.exp(-(t - 2) / 10) + 1e-7;
        ro.innerHTML = `${phase(t)}<br>OVC 壓力 ≈ ${pOVC.toExponential(1)} Pa<br>MXC = <b>${fmtT(T[5])}</b>　4 K 板 = ${fmtT(T[2])}　50 K 板 = ${fmtT(T[1])}<br><span style="color:#9fb0c8">時間尺度為典型示意，依機型與負載而異</span>`;
      },
    };
  },
});
