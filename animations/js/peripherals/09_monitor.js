/* 周邊場景 9：監控、聯鎖與故障情境 */
App.register({
  id: 'monitor', num: 9, short: '監控與聯鎖',
  title: '監控、聯鎖與故障處置',
  subtitle: '溫度、壓力、流量、冷卻水 24 小時監控；異常時自動進入安全狀態',
  desc: `<p><b>溫度計</b>：50 K 級用 PT100／矽二極體，4 K 與 Still 用 Cernox，Cold plate 與 MXC 用 RuO₂；由低溫溫控器以低激發電流讀取。</p>
<p><b>GHS 儀表</b>：多個壓力計（P1–P6：Still 抽氣、凝結壓力、儲存槽…）、³He 流量計、常閉氣動閥與過壓釋放閥。</p>
<p><b>聯鎖（interlock）</b>：冷卻水溫過高 → 壓縮機停機；停電或控制器異常 → 閥門關閉、混合氣經背壓閥回收至儲存槽，保護昂貴的 ³He。</p>
<p>選擇一種故障情境，觀察感測器數值、告警與自動處置。</p>`,
  camera: { pos: [6.5, 4.2, 8.5], target: [0.4, 2.0, 0] },
  build(ctx) {
    const { scene, U, THREE, ui } = ctx;
    const fr = App.buildFridge(ctx, { canOpacity: 0.18, frame: false });
    const st = App.PD.stages;
    const sensors = [
      { i: 1, type: 'PT100', T0: 40 }, { i: 2, type: 'Cernox', T0: 3.0 }, { i: 3, type: 'Cernox', T0: 0.88 }, { i: 4, type: 'RuO₂', T0: 0.09 }, { i: 5, type: 'RuO₂', T0: 0.010 },
    ].map((s) => {
      const y = st[s.i].y; const m = U.sphere(0.07, U.glow(0x2ecc71), st[s.i].r * 0.7, y + 0.06, 0.4); scene.add(m);
      return { ...s, m, T: s.T0, lbl: ctx.label('', [st[s.i].r + 1.15, y, 0], 'small') };
    });
    st.forEach((s) => ctx.label(s.name, [-s.r - 0.9, s.y, 0], 'small'));
    const panel = App.device(ctx, { pos: [-3.6, 0, -0.5], w: 1.2, h: 1.7, d: 0.6, label: 'GHS：壓力計 P1–P6 · 流量計 · 閥', color: 0x34304a, leds: 4, ledColor: 0xc58bff });
    const comp = App.device(ctx, { pos: [3.6, 0, -1.8], w: 0.8, h: 1.0, d: 0.8, label: '壓縮機（水溫聯鎖）', color: 0x2f4a3a, leds: 2 });
    const tank = new THREE.Mesh(new THREE.CylinderGeometry(0.35, 0.35, 1.1, 24), U.metal(0xb7c0cc)); tank.position.set(-3.6, 0.55, 1.4); scene.add(tank);
    ctx.label('混合氣儲存槽', [-3.6, 1.35, 1.4], 'small');
    const alarm = U.sphere(0.18, U.glow(0x2ecc71), -3.6, 2.25, -0.5); scene.add(alarm);
    const recov = App.Flow(scene, [[-0.2, 3.4, -0.4], [-0.2, 4.0, -0.4], [-3.6, 4.0, 1.4], [-3.6, 1.1, 1.4]], 0xc58bff, { radius: 0.04, speed: 1.2 });
    recov.show(false);
    const circ = App.Flow(scene, [[0.2, 3.4, -0.4], [0.2, 3.8, -0.6], [-3.2, 3.8, -0.5], [-3.2, 1.7, -0.5]], 0xc58bff, { radius: 0.05, speed: 0.9 });
    let fault = 'ok', tf = 0;
    ui.radio([['ok', '正常運轉'], ['water', '冷卻水中斷'], ['leak', '真空洩漏'], ['block', '流阻堵塞']], 'ok', (v) => { fault = v; tf = 0; hist.length = 0; });
    const ro = ui.readout();
    const hist = [];
    const qf = new URLSearchParams(location.search).get('fault');
    if (qf) { fault = qf; }
    const fmtT = (T) => (T >= 1 ? T.toFixed(T >= 10 ? 0 : 2) + ' K' : (T * 1000).toFixed(T < 0.1 ? 1 : 0) + ' mK');
    ctx.inset('監控曲線（最近 60 秒，時間加速）', (g, W, H, P) => {
      const { X, Y } = P.frame(g, W, H, [0, 60], [-2.2, 2], { xlabel: '時間 (s)', ylabel: '溫度', yticks: [[-2, '10 mK'], [-1, '100 mK'], [0, '1 K'], [1, '10 K']], m: { l: 54 } });
      const cols = ['#b07cff', '#4f8cff', '#38c6d9', '#2ecc71'];
      [4, 3, 2, 1].forEach((k, j) => { g.strokeStyle = cols[j]; g.lineWidth = 1.8; g.beginPath(); hist.forEach((h, i) => { const x = X(h[0] - Math.max(0, tt - 60)), y = Y(Math.log10(h[1][k])); i ? g.lineTo(x, y) : g.moveTo(x, y); }); g.stroke(); });
      P.text(g, 'MXC', W - 40, 24, '#b07cff'); P.text(g, 'CP', W - 40, 38, '#4f8cff'); P.text(g, 'Still', W - 40, 52, '#38c6d9'); P.text(g, '4 K', W - 40, 66, '#2ecc71');
    });
    let tt = 0;
    return {
      update(time, dt) {
        tf += dt; tt += dt;
        // 情境模型（tf 秒，時間加速）
        const T = sensors.map((s) => s.T0);
        let water = 18, pOVC = 1e-5, flow = 0.5, pCond = 500, comp_on = true, status = 'OK', action = '—';
        if (fault === 'water') {
          water = 18 + Math.min(30, tf * 2.2);
          comp_on = water < 32;
          const u = comp_on ? 0 : tf - (32 - 18) / 2.2;
          if (!comp_on) { T[0] = 40 + u * 6; T[1] = 3 + u * 1.2; T[2] = 0.88 + u * 0.4; T[3] = 0.09 * Math.exp(u / 4); T[4] = 0.01 * Math.exp(u / 3.2); flow = Math.max(0, 0.5 - u * 0.05); }
          status = water > 27 ? 'ALARM' : 'WARN';
          action = comp_on ? '冷卻水溫上升，發出警告' : '水溫超限 → 聯鎖停止壓縮機；GHS 準備回收混合氣';
        } else if (fault === 'leak') {
          pOVC = 1e-5 * Math.exp(Math.min(tf, 20) * 0.6);
          const h = Math.log10(pOVC / 1e-5);
          T[0] = 40 + h * 8; T[1] = 3 * (1 + h * 0.5); T[2] = 0.88 * (1 + h * 0.6); T[3] = 0.09 * Math.exp(h * 0.9); T[4] = 0.01 * Math.exp(h * 1.0);
          status = pOVC > 1e-3 ? 'ALARM' : 'WARN';
          action = pOVC > 1e-3 ? 'OVC 壓力過高：氣體導熱使各級升溫 → 停止循環、檢漏' : 'OVC 壓力上升';
        } else if (fault === 'block') {
          flow = Math.max(0, 0.5 * Math.exp(-tf / 3)); pCond = 500 + Math.min(600, tf * 60);
          T[4] = 0.01 / Math.sqrt(Math.max(flow, 0.004) / 0.5); T[3] = 0.09 * (1 + (0.5 - flow) * 3);
          status = flow < 0.2 ? 'ALARM' : 'WARN';
          action = flow < 0.2 ? '³He 流量歸零、凝結壓力升高 → 多為雜質在冷阱/流阻凍結；需升溫清理冷阱' : '流量下降';
        }
        T.forEach((v, i) => (T[i] = Math.min(v, 300)));
        sensors.forEach((s, i) => {
          s.T = T[i]; const ratio = s.T / s.T0;
          const col = ratio > 3 ? 0xff5a5f : ratio > 1.3 ? 0xe0a54a : 0x2ecc71;
          s.m.material.color.setHex(col); s.m.scale.setScalar(ratio > 1.3 ? 1 + 0.3 * Math.sin(time * 8) : 1);
          s.lbl.set(`${s.type}：${fmtT(s.T)}`);
        });
        fr.plates.forEach((p, i) => { if (i > 0) { p.material.emissive = App.tempColor(T[i - 1]); p.material.emissiveIntensity = 0.2; } });
        alarm.material.color.setHex(status === 'OK' ? 0x2ecc71 : status === 'WARN' ? 0xe0a54a : 0xff5a5f);
        alarm.scale.setScalar(status === 'ALARM' ? 1 + 0.4 * Math.abs(Math.sin(time * 6)) : 1);
        comp.body.material.emissive.setHex(comp_on ? 0x000000 : 0x440000);
        const recovering = status === 'ALARM' && (fault === 'water');
        recov.show(recovering); recov.update(dt);
        circ.show(flow > 0.05 && !recovering); circ.speed = 0.3 + flow * 1.5; circ.update(dt);
        hist.push([tt, T.slice()]); while (hist.length && hist[0][0] < tt - 60) hist.shift();
        ro.innerHTML = `狀態：<b style="color:${status === 'OK' ? '#7ef0a0' : status === 'WARN' ? '#ffd28a' : '#ff8a8a'}">${status}</b>　動作：${action}<br>` +
          `冷卻水入水 ${water.toFixed(1)} °C　OVC ${pOVC.toExponential(1)} mbar<br>³He 流量 ${flow.toFixed(2)} mmol/s　凝結壓力 ${pCond.toFixed(0)} mbar　壓縮機 ${comp_on ? '運轉' : '<b>停止</b>'}`;
      },
    };
  },
});
