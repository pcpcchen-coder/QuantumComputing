/* 周邊場景 10：系統啟動與校準流程 — 降溫完成後到「可以跑量子程式」 */
App.register({
  id: 'bringup', num: 10, short: '啟動與校準',
  title: '從基溫到上線：啟動與校準流程',
  subtitle: '硬體連接完成、降到基溫後，還要一連串量測把每顆量子位元「調好」',
  desc: `<p>每一步都由控制軟體自動執行並把結果寫入<b>校準資料庫</b>（右下角為該步的典型量測圖）：</p>
<p>① 系統檢查（溫度、放大器偏壓、線路穿透）→ ② 讀取腔頻譜 → ③ Punch-out（確認有耦合到量子位元）→ ④ 量子位元頻譜 → ⑤ Rabi（找 π 脈衝振幅）→ ⑥ Ramsey（精修頻率、T₂*）→ ⑦ T₁ → ⑧ 讀取最佳化（頻率、功率、積分權重、閾值）→ ⑨ DRAG / 閘微調 → ⑩ 隨機基準測試（RB）→ ⑪ 上線。</p>
<p>雙量子位元閘還需額外校準（耦合器偏壓、條件相位…）。參數會漂移，所以校準會<b>定期重跑</b>。</p>`,
  camera: { pos: [0.5, 4.5, 12.5], target: [0, 2.0, 0] },
  build(ctx) {
    const { scene, U, THREE, ui } = ctx;
    const steps = [
      ['系統檢查', 'check'], ['讀取腔頻譜', 'res'], ['Punch-out', 'punch'], ['量子位元頻譜', 'qspec'], ['Rabi', 'rabi'], ['Ramsey', 'ramsey'],
      ['T₁ 量測', 't1'], ['讀取最佳化', 'iq'], ['DRAG / 閘微調', 'drag'], ['隨機基準測試', 'rb'], ['上線 ✓', 'done'],
    ];
    const blocks = steps.map(([n], i) => {
      const x = -6 + i * 1.2, z = 0, y = 0.3 + i * 0.36;
      const m = U.box(1.1, 0.3, 0.8, U.mat(0x2a3446, { emissive: 0x38c6d9, emissiveIntensity: 0.0 }), x, y, z);
      scene.add(m); ctx.label(`${i + 1}. ${n}`, [x, y + (i % 2 ? 0.5 : -0.45), z], 'small');
      return m;
    });
    for (let i = 0; i < blocks.length - 1; i++) scene.add(U.line([blocks[i].position, blocks[i + 1].position], 0x5b7aa8, 0.6));
    const runner = U.sphere(0.18, U.glow(0xffd28a)); scene.add(runner);
    const core = App.buildFridge(ctx, { pos: [-4.5, 0, -3], scale: 0.7, frame: false, canOpacity: 0.2 });
    ctx.label('基溫 10 mK', [-4.5, 2.9, -3], 'gold small');
    let cur = 0, auto = true, tStep = 0;
    const r = ui.row();
    ui.button('◀ 上一步', () => { cur = Math.max(0, cur - 1); auto = false; ab.classList.remove('on'); tStep = 0; }, r);
    ui.button('下一步 ▶', () => { cur = Math.min(steps.length - 1, cur + 1); auto = false; ab.classList.remove('on'); tStep = 0; }, r);
    const ab = ui.toggle('自動播放', true, (on) => { auto = on; });
    const ro = ui.readout();
    const info = {
      check: '確認各級溫度、HEMT/TWPA 偏壓、每條線的穿透與衰減符合預期（室溫與低溫各量一次）',
      res: '掃頻找出每個讀取腔的共振凹陷（多工饋線上一次看到全部）',
      punch: '提高讀取功率：低功率時腔頻受量子位元推移，高功率時回到裸頻 → 證明耦合存在',
      qspec: '固定讀取、掃量子位元驅動頻率，找到 f₀₁（高功率時也看到 f₀₂/2 → 非諧性）',
      rabi: '掃驅動振幅，P(1) 呈餘弦振盪 → 取第一個峰為 π 脈衝振幅',
      ramsey: '兩個 π/2 之間等待時間 τ，條紋頻率 = 失諧量 → 修正頻率；包絡給出 T₂*',
      t1: 'π 脈衝後等待 τ 再讀取，指數衰減給出 T₁',
      iq: '最佳化讀取頻率、功率、時長與積分權重；設定判別閾值，得到讀取保真度',
      drag: '調整 DRAG 係數抑制洩漏與相位誤差；精修 π、π/2 振幅（重複脈衝放大誤差）',
      rb: '隨機 Clifford 序列長度 m 的存活機率 A·p^m + B → 每閘平均錯誤率',
      done: '參數寫入資料庫，開放給編譯器與使用者；之後定期自動重新校準',
    };
    ctx.inset('', (g, W, H, P) => {
      const key = steps[cur][1]; const R = (a, b) => a + (b - a) * Math.random();
      const fr = (xr, yr, xl, yl) => P.frame(g, W, H, xr, yr, { xlabel: xl, ylabel: yl });
      if (key === 'check') { App.bars(g, W, H, P, [['50 K', 40], ['4 K', 3], ['Still', 0.9], ['CP', 0.09], ['MXC', 0.01]].map(([n, v]) => [n, Math.log10(v) + 2.2, '#2ecc71']), { fmt: (v) => '✓', l: 60, footer: '各級溫度正常（對數長度）' }); return; }
      if (key === 'res') { const { X, Y } = fr([-5, 5], [0, 1.1], '頻率 − 7.1 GHz (MHz)', '|S21|'); P.curve(g, (f) => 1 - 0.8 / (1 + 4 * f * f), -5, 5, X, Y, '#e0a54a', 2); return; }
      if (key === 'punch') { const { X, Y } = fr([-4, 4], [0, 1], '頻率偏移 (MHz)', '讀取功率'); for (let k = 0; k < 20; k++) { const p = k / 19; const f0 = p < 0.55 ? -1.5 : 0.5; for (let j = 0; j < 40; j++) { const f = -4 + j * 0.2; const v = 1 - 0.8 / (1 + 6 * (f - f0) ** 2); g.fillStyle = `rgba(56,198,217,${1 - v})`; g.fillRect(X(f), Y(p + 0.05), (X(4) - X(-4)) / 40 + 1, (Y(0) - Y(0.05)) + 1); } } P.text(g, '低功率：腔頻被推移', X(-3.8), Y(0.3), '#ffd28a'); P.text(g, '高功率：回到裸頻', X(-3.8), Y(0.85), '#ffd28a'); return; }
      if (key === 'qspec') { const { X, Y } = fr([4.2, 5.0], [0, 1.1], '驅動頻率 (GHz)', 'P(1)'); P.curve(g, (f) => 0.9 / (1 + ((f - 4.74) / 0.006) ** 2) + 0.35 / (1 + ((f - 4.596) / 0.004) ** 2), 4.2, 5.0, X, Y, '#4f8cff', 2, 800); P.text(g, 'f₀₁', X(4.74), Y(0.98), '#fff', 'center'); P.text(g, 'f₀₂/2', X(4.596), Y(0.45), '#fff', 'center'); return; }
      if (key === 'rabi') { const { X, Y } = fr([0, 1], [0, 1.05], '驅動振幅（任意單位）', 'P(1)'); P.curve(g, (a) => 0.5 - 0.5 * Math.cos(2 * Math.PI * a * 1.6), 0, 1, X, Y, '#ff5a5f', 2); P.dot(g, X(1 / 3.2), Y(1), 5, '#ffd28a'); P.text(g, 'π 振幅', X(1 / 3.2) + 6, Y(0.95), '#ffd28a'); return; }
      if (key === 'ramsey') { const { X, Y } = fr([0, 10], [0, 1], '等待時間 τ (μs)', 'P(1)'); P.curve(g, (t) => 0.5 + 0.45 * Math.exp(-t / 6) * Math.cos(2 * Math.PI * 0.6 * t), 0, 10, X, Y, '#38c6d9', 2, 500); return; }
      if (key === 't1') { const { X, Y } = fr([0, 300], [0, 1], '等待時間 τ (μs)', 'P(1)'); P.curve(g, (t) => Math.exp(-t / 90), 0, 300, X, Y, '#ff5a5f', 2); P.text(g, 'T₁ ≈ 90 μs', X(150), Y(0.6), '#ffd28a'); return; }
      if (key === 'iq') { const { X, Y } = fr([-3, 3], [-2.2, 2.2], 'I', 'Q'); for (let k = 0; k < 260; k++) { P.dot(g, X(-1.2 + 0.4 * U.gauss()), Y(0.5 + 0.4 * U.gauss()), 1.6, 'rgba(79,140,255,.7)'); P.dot(g, X(1.2 + 0.4 * U.gauss()), Y(-0.5 + 0.4 * U.gauss()), 1.6, 'rgba(255,90,95,.7)'); } return; }
      if (key === 'drag') { const { X, Y } = fr([-1, 1], [-1, 1], 'DRAG 係數 β', '相位誤差'); P.curve(g, (b) => 0.9 * (b - 0.2), -1, 1, X, Y, '#4f8cff', 2); P.curve(g, (b) => -0.9 * (b - 0.2), -1, 1, X, Y, '#ff5a5f', 2); P.dot(g, X(0.2), Y(0), 5, '#ffd28a'); P.text(g, '兩條線交點 = 最佳 β', X(0.25), Y(0.15), '#ffd28a'); return; }
      if (key === 'rb') { const { X, Y } = fr([0, 500], [0.4, 1.0], 'Clifford 序列長度 m', '存活機率'); P.curve(g, (m) => 0.5 + 0.5 * Math.pow(0.998, m), 0, 500, X, Y, '#2ecc71', 2); P.text(g, '每閘錯誤率 ≈ 0.1 %', X(250), Y(0.92), '#ffd28a'); return; }
      P.text(g, '✓ 校準完成，量子處理器上線', W / 2, H / 2, '#7ef0a0', 'center');
    });
    const qs = new URLSearchParams(location.search).get('step');
    if (qs !== null) { cur = +qs; auto = false; ab.classList.remove('on'); }
    let lastKey = '';
    return {
      update(time, dt) {
        tStep += dt;
        if (auto && tStep > 3.2) { cur = (cur + 1) % steps.length; tStep = 0; }
        blocks.forEach((b, i) => { b.material.emissive.setHex(i < cur ? 0x2ecc71 : i === cur ? 0xffd28a : 0x38c6d9); b.material.emissiveIntensity = i < cur ? 0.45 : i === cur ? 0.6 + 0.3 * Math.sin(time * 6) : 0.0; });
        runner.position.copy(blocks[cur].position).add(new THREE.Vector3(0, 0.45 + 0.08 * Math.sin(time * 5), 0));
        if (lastKey !== steps[cur][1]) { lastKey = steps[cur][1]; document.getElementById('inset-title').textContent = `第 ${cur + 1} 步：${steps[cur][0]}`; }
        ro.innerHTML = `<b>第 ${cur + 1} 步：${steps[cur][0]}</b><br>${info[steps[cur][1]]}`;
      },
    };
  },
});
