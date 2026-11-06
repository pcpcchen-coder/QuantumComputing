/* 周邊場景 8：機房基礎設施 — 電力、UPS、冷卻水、空調、接地、防振；停電情境 */
App.register({
  id: 'infra', num: 8, short: '機房基礎設施',
  title: '機房基礎設施：電力 · 冷卻水 · 環境 · 防振',
  subtitle: '一套稀釋冷凍機系統約 20–30 kW；壓縮機與冷卻水是最大負載',
  desc: `<p><b>電力</b>：三相市電 → 配電盤。<b>壓縮機與冷卻水機</b>直接由配電盤供電（功率大）；<b>控制電子、電腦、GHS 控制器與閥門</b>接 UPS，停電時才能安全處置。</p>
<p><b>冷卻水</b>：壓縮機約 10 kW 的熱要由冷卻水帶走（PT415：~11.5 L/min、入水 ≤ 27 °C）。冷卻水中斷 → 壓縮機過溫停機 → 冷凍機開始升溫。</p>
<p><b>環境</b>：恆溫空調、濕度控制；另需壓縮空氣（氣動閥）。<b>接地</b>採單點（星形）接地、隔離變壓器，避免接地迴路引入雜訊。</p>
<p><b>防振</b>：脈衝管 1.4 Hz 的振動會經由纜線摩擦電效應變成雜訊；以遠端馬達、軟管固定、纜線綁紮與避震座降低。</p>
<p>按「模擬停電」看系統如何反應。</p>`,
  camera: { pos: [11, 11, 16], target: [0.6, 1, 0] },
  build(ctx) {
    const { scene, U, THREE, ui } = ctx;
    const floor = new THREE.Mesh(new THREE.PlaneGeometry(20, 11), U.mat(0x1a2130, { roughness: 0.95 })); floor.rotation.x = -Math.PI / 2; scene.add(floor);
    // 牆（室內 / 室外分界）
    scene.add(U.box(0.15, 3.2, 11, U.mat(0x2a3140, { transparent: true, opacity: 0.35 }), 5.6, 1.6, 0));
    ctx.label('室外', [7.6, 3.6, -4.5], 'small'); ctx.label('機房（恆溫恆濕）', [-1, 4.3, -4.5], 'small');
    const fr = App.buildFridge(ctx, { pos: [0, 0, 0], canOpacity: 0.25 });
    // 避震座
    [[-1.6, -1.6], [1.6, -1.6], [-1.6, 1.6], [1.6, 1.6]].forEach(([x, z]) => scene.add(U.box(0.35, 0.12, 0.35, U.mat(0x111111), x, 0.06, z)));
    ctx.label('避震座 + 剛性框架', [1.9, 0.2, 2.2], 'small');
    const D = (o) => App.device(ctx, o);
    const tr = D({ pos: [8.2, 0, -2.5], w: 1.2, h: 1.6, d: 1.0, label: '市電變壓器（三相）', color: 0x3a3a3a, leds: 1, ledColor: 0xffd166 });
    const panel = D({ pos: [-6.5, 0, -2.8], w: 0.6, h: 1.9, d: 0.45, label: '配電盤', color: 0x404652, leds: 2, ledColor: 0xffd166 });
    const ups = D({ pos: [-6.5, 0, 0.2], w: 1.0, h: 1.4, d: 0.8, label: 'UPS + 電池', color: 0x3a3424, leds: 3, ledColor: 0xffd166 });
    const iso = D({ pos: [-6.5, 0, 2.4], w: 0.6, h: 0.8, d: 0.6, label: '隔離變壓器', color: 0x3a3424, leds: 1 });
    const rack = D({ pos: [-3.4, 0, 1.8], w: 1.0, h: 2.1, d: 0.9, label: '控制電子 + 電腦', cls: 'teal', leds: 6, ledColor: 0x38c6d9 });
    const ghs = D({ pos: [2.9, 0, -2.6], w: 1.2, h: 1.6, d: 0.8, label: 'GHS（泵 · 閥 · 控制器）', color: 0x34304a, leds: 4, ledColor: 0xc58bff });
    const comp = D({ pos: [3.8, 0, 2.2], w: 0.8, h: 1.0, d: 0.8, label: '壓縮機 ~10.7 kW', color: 0x2f4a3a, leds: 2 });
    const chill = D({ pos: [8.0, 0, 2.6], w: 1.3, h: 1.4, d: 1.0, label: '冷卻水機（≤27 °C）', color: 0x24384f, leds: 2, ledColor: 0x4fa3ff });
    const air = D({ pos: [-2.0, 0, -4.3], w: 2.2, h: 0.9, d: 0.6, label: '恆溫空調 / 壓縮空氣', color: 0x2b3446, leds: 2 });
    // 接地
    const gnd = U.box(0.5, 0.05, 0.5, U.metal(0x9ad11a), -1.6, 0.03, 3.8); scene.add(gnd);
    ctx.label('單點接地', [-1.6, 0.35, 4.3], 'small');
    [[-3.4, 0.05, 2.25], [0, 0.05, 1.6], [3.8, 0.05, 2.6], [-6.5, 0.05, 2.7]].forEach((p) => scene.add(U.tube([p, [-1.6, 0.05, 3.8]], 0.02, U.mat(0x9ad11a))));
    const F = (pts, c, o) => App.Flow(scene, pts, c, o);
    const grid = [
      F([[7.6, 0.1, -2.5], [-6.2, 0.1, -2.5]], 0xffd166, { radius: 0.04 }),
      F([[-6.5, 0.15, -2.3], [-6.5, 0.15, -0.2]], 0xffd166, { radius: 0.04 }),
      F([[-6.2, 0.1, -2.6], [-6.2, 0.1, -3.6], [3.8, 0.1, -3.6], [3.8, 0.1, -3.0]], 0xffd166, { radius: 0.03 }),
      F([[-6.0, 0.12, -2.4], [4.5, 0.12, -2.4], [4.5, 0.12, 2.2], [4.2, 0.12, 2.2]], 0xffd166, { radius: 0.04 }),
      F([[4.5, 0.12, 0.6], [7.4, 0.12, 0.6], [7.4, 0.12, 2.6]], 0xffd166, { radius: 0.04 }),
      F([[-6.2, 0.1, -3.0], [-2.0, 0.1, -3.9]], 0xffd166, { radius: 0.03 }),
    ];
    const upsF = [
      F([[-6.5, 0.18, 0.6], [-6.5, 0.18, 2.1]], 0xfff2a8, { radius: 0.035 }),
      F([[-6.2, 0.18, 2.4], [-3.4, 0.18, 2.4], [-3.4, 0.18, 2.25]], 0xfff2a8, { radius: 0.035 }),
      F([[-6.0, 0.2, 0.2], [2.4, 0.2, 0.2], [2.4, 0.2, -2.2]], 0xfff2a8, { radius: 0.03 }),
    ];
    const water = [
      F([[7.4, 0.3, 2.9], [4.25, 0.3, 2.9], [4.25, 0.5, 2.5]], 0x4fa3ff, { radius: 0.05, speed: 1.2 }),
      F([[4.25, 0.7, 2.0], [4.6, 0.45, 1.8], [7.4, 0.45, 1.8], [7.4, 0.45, 2.3]], 0xff9f43, { radius: 0.05, speed: 1.2 }),
    ];
    ctx.label('冷水 → 壓縮機', [6.0, 0.8, 3.3], 'small'); ctx.label('回水（帶走 ~10 kW）', [6.0, 0.9, 1.4], 'small');
    const ptF = [F([[3.6, 1.0, 2.2], [3.6, 4.3, 2.2], [0.62, 4.3, 0.2], [0.62, 4.05, 0.2]], 0x5ee08a, { radius: 0.04, speed: 1.4 })];
    // 空調氣流
    const airF = [F([[-2.0, 1.0, -4.0], [-2.0, 2.5, -2.0], [-1.0, 2.0, 0.5]], 0xcfe8ff, { radius: 0.01, speed: 0.6, pipeOpacity: 0.05 })];
    // 振動示意
    const vib = U.dynLine(120, 0xff7a59); scene.add(vib.obj);
    const vib2 = U.dynLine(120, 0x2ecc71); scene.add(vib2.obj);
    const vL = ctx.label('', [1.8, 4.6, 0.2], 'small');

    let outage = false, tOut = 0, remoteMotor = true;
    const ob = ui.toggle('⚡ 模擬停電', false, (on) => { outage = on; tOut = 0; });
    ui.toggle('脈衝管遠端馬達 + 纜線固定（降振）', true, (on) => { remoteMotor = on; });
    const ro = ui.readout();
    const hist = [];
    ctx.inset('停電後的變化（示意）', (g, W, H, P) => {
      const { X, Y } = P.frame(g, W, H, [0, 120], [-2.2, 1.0], { xlabel: '停電後時間 (分鐘)', ylabel: 'MXC 溫度', xticks: [[0, '0'], [30, '30'], [60, '60'], [90, '90'], [120, '120']], yticks: [[-2, '10 mK'], [-1, '100 mK'], [0, '1 K'], [1, '10 K']], m: { l: 54 } });
      P.curve(g, (m) => Math.log10(Tm(m)), 0, 120, X, Y, 'rgba(159,176,200,.4)', 1.5);
      if (outage) P.dot(g, X(Math.min(120, tOut)), Y(Math.log10(Tm(Math.min(120, tOut)))), 6, '#ff5a5f');
      P.text(g, '~10 分鐘：混合液開始蒸發 → 回收至儲存槽', X(12), Y(-1.7), '#ffd28a');
    });
    const Tm = (m) => (m < 8 ? 0.01 + 0.003 * m : m < 40 ? 0.034 * Math.exp((m - 8) / 6.5) : Math.min(8, 4.5 + (m - 40) * 0.04));
    return {
      update(time, dt) {
        if (outage) tOut += dt * 6; // 1 秒 = 6 分鐘
        const mains = !outage;
        grid.forEach((f) => { f.on = mains; f.mat.color.setHex(mains ? 0xffd166 : 0x444444); f.update(dt); });
        upsF.forEach((f) => f.update(dt));
        water.forEach((f) => { f.on = mains; f.update(dt); });
        ptF.forEach((f) => { f.on = mains; f.update(dt); });
        airF.forEach((f) => { f.on = mains; f.update(dt); });
        [tr, panel, comp, chill, air].forEach((d) => d.body.material.emissive.setHex(mains ? 0x000000 : 0x330000));
        // 振動波形
        const A = mains ? 0.25 : 0; const damp = remoteMotor ? 0.12 : 0.6;
        const pts = [], pts2 = [];
        for (let i = 0; i < 120; i++) { const x = 0.9 + i * 0.02; pts.push([x, 4.35 + A * Math.sin(time * 9 + i * 0.3), 0.2]); pts2.push([x, 0.55 + A * damp * Math.sin(time * 9 + i * 0.3), 0.6]); }
        vib.set(pts); vib2.set(pts2);
        vL.set(mains ? `冷頭振動 → 樣品處振動（${remoteMotor ? '已隔離' : '未隔離'}）` : '脈衝管停止');
        const T = Tm(Math.min(120, tOut));
        ro.innerHTML = outage
          ? `<b style="color:#ff8a8a">停電 ${tOut.toFixed(0)} 分鐘</b>：壓縮機、冷卻水機停止；UPS 供電給電子、電腦、GHS 閥門控制<br>GHS 關閉閥門、混合氣經背壓閥回收至儲存槽（避免損失 ³He）<br>MXC ≈ ${T < 1 ? (T * 1000).toFixed(0) + ' mK' : T.toFixed(1) + ' K'} — 復電後需重新降溫（數小時～一天）`
          : '正常運轉：市電供應所有設備；UPS 待機（建議可撐 ≥ 1–2 小時給關鍵負載）<br>典型用電：壓縮機 ~10.7 kW、冷卻水 ~10 kW、電子 ~3 kW，合計 ~25 kW';
      },
    };
  },
});
