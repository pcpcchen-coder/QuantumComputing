/* 原子場景 18：頻率基準 — 中性原子平台的「時鐘鏈」
 * 10 MHz 參考（氫邁射 / 銣鐘）→ 6.835 GHz 微波 → 原子陣列；光頻梳把 10 MHz 接到光頻；芮德堡雷射用 PDH 鎖到 ULE 參考腔
 * 右側：原子噴泉鐘（Ramsey 分離振盪場法的原型）
 * 插圖：類氫結構表、Ramsey 相位誤差 @ 6.835 GHz、雷射線寬 vs CZ 錯誤（粗估 ε ≈ π Δν t_gate）
 */
App.register({
  id: 'atomclock', num: 17, short: '頻率基準與原子鐘',
  title: '頻率基準：氫邁射、參考腔與光頻梳',
  subtitle: '中性原子要穩住兩種頻率：6.835 GHz 微波（鎖到 10 MHz 參考，例如氫邁射）與芮德堡雷射（鎖到超穩參考腔，再用光頻梳接回微波基準）',
  desc: `<p><b>同一個問題，放到中性原子</b>：⁸⁷Rb 量子位元相差 <b>6.835 GHz</b>，全域微波（或 Raman 雷射的頻差）同樣是「脈衝面積 = 角度、相位 = 旋轉軸」，所以微波源也要鎖到實驗室的 10 MHz 參考：氫邁射（場景 8）、銣鐘或 GPS 馴服振盪器。原子的 T₂ 約 1 秒以上，參考源越穩，長時間的 Ramsey / 自旋回波越不會被控制雜訊拖累。</p>
<p><b>類氫結構</b>：Rb、Cs、Yb⁺ 和氫一樣只有<b>一顆價電子</b>，電子自旋和核自旋耦合出兩個超精細能階——都是「21 公分線的親戚」：H（I=1/2，F=0/1，1.42 GHz）、⁸⁷Rb（I=3/2，F=1/2，6.835 GHz）、¹³³Cs（I=7/2，F=3/4，<b>9,192,631,770 Hz，定義國際單位「秒」</b>）、¹⁷¹Yb⁺（I=1/2，F=0/1，12.6 GHz）。有趣的是：商用<b>銣鐘</b>用的正是 ⁸⁷Rb 這條 6.835 GHz 躍遷——實驗室的時鐘和量子位元是同一種原子的同一條線。</p>
<p><b>中性原子多一道難題：芮德堡雷射</b>。CZ 閘要用 420 + 1013 nm 兩道光把原子激發到芮德堡態，<b>雷射的相位雜訊直接變成閘錯誤</b>。做法：<br>• 把雷射用 <b>Pound–Drever–Hall（PDH）</b>鎖到真空中的 <b>ULE 玻璃參考腔</b>（超低膨脹 Fabry–Pérot 腔），線寬從約 100 kHz 壓到 &lt; 1 kHz（最好的系統到 Hz 級），常再加一個濾波腔壓掉高頻相位雜訊。<br>• 參考腔長度會慢慢飄（玻璃老化），所以用<b>光頻梳</b>（鎖模雷射，梳齒 f<sub>n</sub> = f<sub>ceo</sub> + n·f<sub>rep</sub>，兩個頻率都鎖到 10 MHz）當「尺」，把數百 THz 的光頻接回氫邁射的微波基準，得到絕對頻率。</p>
<p><b>原子鐘本身就是中性原子</b>：國家時間標準的<b>銫噴泉鐘</b>把冷原子往上拋約 1 公尺，上升和落下各穿過同一個微波腔一次——這就是 Ramsey「分離振盪場法」最純粹的形式，自由演化約 0.5–1 秒。最準的<b>鍶光晶格鐘</b>、<b>光鑷原子鐘</b>和中性原子量子電腦用的是同一套硬體（冷原子 + 光鑷 / 光晶格 + 超穩雷射）。</p>
<p><b>三平台對照</b>：超導的微波源也鎖到 10 MHz（多半是銣鐘），但 T₂ 只有約 0.1 ms，參考源的長期穩定度不是瓶頸，短時間相位雜訊才是；離子阱的 12.6 GHz 微波 / Raman 頻差同樣鎖到 10 MHz，光學量子位元（⁴⁰Ca⁺ 729 nm）也要 ULE 參考腔；中性原子兩者都要：微波基準 + 芮德堡雷射穩頻。</p>
<p>插圖的數值是代表性的粗估模型，實際依機型與系統而異。</p>`,
  camera: { pos: [0.8, 4.6, 12.6], target: [0.8, 1.0, -0.4] },
  build(ctx) {
    const { scene, U, THREE, ui } = ctx;
    const QC = App.QC;
    const floor = new THREE.Mesh(new THREE.PlaneGeometry(16, 9), U.mat(0x161d2b, { roughness: 0.95 })); floor.rotation.x = -Math.PI / 2; floor.position.set(0.4, -0.02, -0.5); scene.add(floor);
    const D = (o) => App.device(ctx, o);

    /* ---------- 10 MHz 參考與分配 ---------- */
    D({ pos: [-5.6, 0, 0.4], w: 1.0, h: 2.2, d: 0.9, label: '氫邁射 / 銣鐘<br>10 MHz 參考', cls: 'small', leds: 3, ledColor: 0xd8ff6a, color: 0x2b3446 });
    D({ pos: [-3.6, 0, 0.4], w: 0.9, h: 0.5, d: 0.6, label: '10 MHz 分配放大器', cls: 'small', leds: 4, ledColor: 0x38c6d9 });
    const ATOM0 = new THREE.Vector3(2.6, 1.2, 0.4);
    D({ pos: [-1.4, 0, 1.6], w: 1.1, h: 0.45, d: 0.6, label: '微波合成器<br>10 MHz → 6.835 GHz', cls: 'small', leds: 2, ledColor: 0x38c6d9 });
    const flows = [];
    const F = (pts, c, o = {}) => { const f = App.Flow(scene, pts, c, Object.assign({ radius: 0.025, speed: 1.4, dot: 0.035, pipeOpacity: 0.4 }, o)); flows.push(f); return f; };
    F([[-5.1, 1.0, 0.4], [-4.4, 1.0, 0.4], [-4.4, 0.3, 0.4], [-4.05, 0.3, 0.4]], 0x38c6d9);
    const fMw = F([[-3.15, 0.25, 0.6], [-2.3, 0.25, 1.6], [-1.95, 0.25, 1.6]], 0x38c6d9);
    const HN = new THREE.Vector3(0.2, 0.35, 1.6);
    F([[-0.85, 0.22, 1.6], [HN.x - 0.25, HN.y, HN.z]], 0x38c6d9);
    const horn = new THREE.Mesh(new THREE.ConeGeometry(0.22, 0.45, 4, 1, true), U.metal(0xb7a46a, { side: THREE.DoubleSide }));
    horn.position.copy(HN); horn.lookAt(ATOM0); horn.rotateX(-Math.PI / 2); scene.add(horn);
    ctx.label('6.835 GHz 號角（全域單位元閘）', [HN.x + 0.3, HN.y - 0.4, HN.z + 0.3], 'small');

    /* ---------- 原子陣列 ---------- */
    const atoms = [];
    for (let i = 0; i < 4; i++) for (let j = 0; j < 3; j++) atoms.push(App.particle(scene, QC.atom, 0.07, [ATOM0.x - 0.6 + i * 0.4, ATOM0.y, ATOM0.z - 0.4 + j * 0.4]));
    const cell = new THREE.Mesh(new THREE.BoxGeometry(2.0, 1.2, 1.6), new THREE.MeshStandardMaterial({ color: 0xbfe6ff, transparent: true, opacity: 0.08, depthWrite: false })); cell.position.copy(ATOM0); scene.add(cell);
    ctx.label('⁸⁷Rb 原子陣列（玻璃真空腔）', [ATOM0.x, ATOM0.y - 0.9, ATOM0.z + 0.9], 'teal');

    /* ---------- 光頻梳、雷射、ULE 參考腔 ---------- */
    const COMB = new THREE.Vector3(-3.4, 1.2, -1.8);
    const ring = new THREE.Mesh(new THREE.TorusGeometry(0.45, 0.06, 12, 40), U.mat(0xff9ad8, { emissive: 0xc04090, emissiveIntensity: 0.5 })); ring.position.copy(COMB); scene.add(ring);
    F([[-3.6, 0.5, 0.15], [-3.6, 0.5, -1.2], [COMB.x, COMB.y - 0.5, COMB.z]], 0x38c6d9);
    ctx.label('光頻梳（f_rep、f_ceo 鎖到 10 MHz）', [COMB.x, COMB.y + 0.75, COMB.z], 'small');
    const teeth = [];
    for (let n = 0; n < 26; n++) { const b = U.box(0.03, 1, 0.03, U.glow(0xffb0e0, 0.85), COMB.x - 1.3 + n * 0.1, 0, COMB.z - 0.7); scene.add(b); teeth.push(b); }
    ctx.label('梳齒 f_n = f_ceo + n·f_rep：光頻的「尺」', [COMB.x, 2.75, COMB.z - 0.7], 'small');
    const L420 = new THREE.Vector3(-0.6, 0.0, -1.6), L1013 = new THREE.Vector3(-0.6, 0.0, -2.5);
    D({ pos: L420.toArray(), w: 1.0, h: 0.35, d: 0.42, label: '420 nm 雷射', cls: 'small', leds: 2, ledColor: App.wlColor(420) });
    D({ pos: L1013.toArray(), w: 1.0, h: 0.35, d: 0.42, label: '1013 nm 雷射', cls: 'small', labelDy: 0.8, leds: 2, ledColor: App.wlColor(1013) });
    const ULE = new THREE.Vector3(1.2, 1.5, -2.6);
    const can = new THREE.Mesh(new THREE.CylinderGeometry(0.45, 0.45, 1.6, 28), U.metal(0x9aa4b2, { transparent: true, opacity: 0.25, depthWrite: false })); can.rotation.z = Math.PI / 2; can.position.copy(ULE); scene.add(can);
    const spacer = new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.22, 1.1, 24), new THREE.MeshStandardMaterial({ color: 0xeaf6ff, transparent: true, opacity: 0.4 })); spacer.rotation.z = Math.PI / 2; spacer.position.copy(ULE); scene.add(spacer);
    [-0.56, 0.56].forEach((dx) => { const m = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.2, 0.04, 24), U.metal(0xe8ecf2, { roughness: 0.05 })); m.rotation.z = Math.PI / 2; m.position.set(ULE.x + dx, ULE.y, ULE.z); scene.add(m); });
    const bounce = U.dynLine(40, 0x9f8cff, 0.8); scene.add(bounce.obj);
    ctx.label('ULE 參考腔（真空中，PDH 鎖頻）', [ULE.x, ULE.y + 0.65, ULE.z], 'small');
    const fPdh1 = F([[L420.x + 0.5, 0.2, L420.z], [ULE.x - 0.9, 0.2, L420.z], [ULE.x - 0.9, ULE.y, ULE.z]], App.wlColor(420), { speed: 1.8 });
    const fPdh2 = F([[L1013.x + 0.5, 0.2, L1013.z], [ULE.x - 1.0, 0.2, L1013.z], [ULE.x - 1.0, ULE.y - 0.1, ULE.z]], App.wlColor(1013), { speed: 1.8 });
    const fBeat = F([[COMB.x + 0.45, COMB.y - 0.4, COMB.z], [-1.1, 0.5, -2.05]], 0xff9ad8, { speed: 1.2 });
    ctx.label('拍頻：雷射 ↔ 梳齒', [-2.0, 0.95, -1.95], 'small');
    const ryd = [App.beam(scene, [L420.x + 0.5, 0.18, L420.z], ATOM0, App.wlColor(420), 0.035, 0.6), App.beam(scene, [L1013.x + 0.5, 0.18, L1013.z], ATOM0, App.wlColor(1013), 0.035, 0.5)];
    ctx.label('芮德堡雷射 → 原子（CZ 閘）', [1.4, 0.45, -0.9], 'small');

    /* ---------- 原子噴泉鐘 ---------- */
    const FX = 6.0, fountain = new THREE.Group(); scene.add(fountain);
    const tube = new THREE.Mesh(new THREE.CylinderGeometry(0.28, 0.28, 3.6, 24, 1, true), new THREE.MeshStandardMaterial({ color: 0xbfe6ff, transparent: true, opacity: 0.12, side: THREE.DoubleSide, depthWrite: false })); tube.position.set(FX, 1.9, -0.4); fountain.add(tube);
    const mot = U.sphere(0.32, new THREE.MeshStandardMaterial({ color: 0x9aa4b2, transparent: true, opacity: 0.25 }), FX, 0.3, -0.4, 20); fountain.add(mot);
    const fcav = new THREE.Mesh(new THREE.CylinderGeometry(0.45, 0.45, 0.35, 28, 1, true), U.metal(0xd9894a, { transparent: true, opacity: 0.6, side: THREE.DoubleSide })); fcav.position.set(FX, 1.2, -0.4); fountain.add(fcav);
    const cloud = App.particle(scene, 0x7ee05a, 0.11, [FX, 0.3, -0.4]); fountain.add(cloud);
    const lbF = [ctx.label('原子噴泉鐘（Cs / Rb）', [FX, 3.95, -0.4], 'gold'), ctx.label('微波腔：上升、落下各穿過一次<br>→ Ramsey 的兩個 π/2', [FX - 0.4, 0.75, 0.7], 'small'), ctx.label('', [FX + 0.9, 2.6, -0.4], 'small')];
    const lbStat = ctx.label('', [0.4, -0.7, 1.9], 'big');

    /* ---------- 狀態與控制 ---------- */
    let ref = 'H', Tr = 1, locked = true, tab = 'hyd', showF = true;
    const F0 = 6.8347e9, TG = 0.25e-6;
    ui.radio([['Q', '石英 OCXO'], ['Rb', '銣鐘'], ['H', '氫邁射']], 'H', (v) => { ref = v; });
    ui.slider('Ramsey 自由演化時間 T', -3, 1.5, 0.1, 0, (v) => { Tr = Math.pow(10, v); }, (v) => { const t = Math.pow(10, v); return t < 1 ? `${(t * 1000).toPrecision(2)} ms` : `${t.toPrecision(2)} s`; });
    ui.toggle('芮德堡雷射鎖到 ULE 參考腔', true, (on) => { locked = on; });
    ui.toggle('顯示原子噴泉鐘', true, (on) => { showF = on; fountain.visible = on; lbF.forEach((l) => l.show(on)); });
    ui.radio([['hyd', '插圖：類氫結構'], ['mw', '插圖：微波相位誤差'], ['laser', '插圖：雷射線寬 vs CZ']], 'hyd', (v) => { tab = v; });
    const ro = ui.readout();
    const lw = () => (locked ? 1e3 : 1e5); // Hz（代表值）
    const czErr = (dnu) => Math.min(1, Math.PI * dnu * TG);

    ctx.inset('', (g, W, H, P) => {
      const t = document.getElementById('inset-title');
      if (tab === 'hyd') {
        t.textContent = '一顆價電子 + 核自旋 → 兩個超精細能階（21 公分線的親戚）';
        const rows = [['原子', '核自旋 I', '能階', '超精細頻率', '用途'], ['H', '1/2', 'F=0 / 1', '1.420 GHz', '氫邁射'], ['⁸⁷Rb', '3/2', 'F=1 / 2', '6.835 GHz', '量子位元・銣鐘'], ['¹³³Cs', '7/2', 'F=3 / 4', '9.193 GHz', '定義「秒」・噴泉鐘'], ['¹⁷¹Yb⁺', '1/2', 'F=0 / 1', '12.643 GHz', '離子量子位元']];
        const xs = [14, 74, 140, 214, 296];
        rows.forEach((r, i) => r.forEach((c, j) => P.text(g, c, xs[j], 26 + i * 34, i === 0 ? '#ffd28a' : j === 0 ? '#8ef0ff' : '#e8eef8', j === 4 ? 'left' : 'left')));
        g.strokeStyle = 'rgba(160,180,210,.3)'; g.beginPath(); g.moveTo(10, 36); g.lineTo(W - 10, 36); g.stroke();
        P.text(g, '原子核越重 → 電子在核附近的機率越大 → 分裂越大', W / 2, H - 10, '#9fb0c8', 'center');
        return;
      }
      if (tab === 'mw') {
        t.textContent = 'Ramsey 時間 T 內 6.835 GHz 微波累積的相位誤差（粗估）';
        const { X, Y } = P.frame(g, W, H, [-3, 1.5], [-5, 2], { xticks: [[-3, '1 ms'], [-2, '10 ms'], [-1, '0.1 s'], [0, '1 s'], [1, '10 s']], yticks: [[-4, '10⁻⁴'], [-2, '0.01'], [0, '1 rad'], [2, '100']], xlabel: '自由演化時間 T', m: { l: 52, b: 32, t: 8 } });
        ['Q', 'Rb', 'H'].forEach((k) => { g.save(); g.beginPath(); g.rect(X(-3), Y(2), X(1.5) - X(-3), Y(-5) - Y(2)); g.clip(); P.curve(g, (x) => Math.log10(App.ramseyPhase(k, F0, Math.pow(10, x))), -3, 1.5, X, Y, App.FREF[k].col, k === ref ? 3 : 1.4); g.restore(); });
        let ly = 18; ['Q', 'Rb', 'H'].forEach((k) => { P.text(g, App.FREF[k].name, W - 64, ly, App.FREF[k].col); ly += 15; });
        g.strokeStyle = '#ff8a8a'; g.setLineDash([4, 3]); g.beginPath(); g.moveTo(X(-3), Y(0)); g.lineTo(X(1.5), Y(0)); g.stroke(); g.setLineDash([]);
        P.text(g, '≈ 1 rad：相位糊掉', X(-2.9), Y(0) - 5, '#ff8a8a');
        const lx = Math.log10(Tr); g.strokeStyle = '#ffd28a'; g.beginPath(); g.moveTo(X(lx), Y(-5)); g.lineTo(X(lx), Y(2)); g.stroke();
        return;
      }
      t.textContent = '雷射線寬 → CZ 閘錯誤（粗估 ε ≈ π·Δν·t_gate，t_gate = 0.25 μs）';
      const { X, Y } = P.frame(g, W, H, [1, 6], [-6, 0], { xticks: [[1, '10 Hz'], [2, '100 Hz'], [3, '1 kHz'], [4, '10 kHz'], [5, '100 kHz'], [6, '1 MHz']], yticks: [[-6, '10⁻⁶'], [-4, '10⁻⁴'], [-2, '1 %'], [0, '100 %']], xlabel: '雷射線寬 Δν', m: { l: 52, b: 32, t: 8 } });
      P.curve(g, (x) => Math.log10(czErr(Math.pow(10, x))), 1, 6, X, Y, '#ff6ad5', 2.5);
      g.strokeStyle = '#8ef0a0'; g.setLineDash([4, 3]); g.beginPath(); g.moveTo(X(1), Y(Math.log10(0.005))); g.lineTo(X(6), Y(Math.log10(0.005))); g.stroke(); g.setLineDash([]);
      P.text(g, '目前最佳 CZ 的總錯誤 ≈ 0.5 %', X(1.1), Y(Math.log10(0.005)) - 5, '#8ef0a0');
      [[3, '鎖到 ULE 腔'], [5, '自由運轉']].forEach(([x, s]) => { const yy = Math.log10(czErr(Math.pow(10, x))); P.dot(g, X(x), Y(yy), x === Math.log10(lw()) ? 6 : 4, x === Math.log10(lw()) ? '#ffd28a' : '#9fb0c8'); P.text(g, s, X(x) + 8, Y(yy) + 14, '#cfd8e6'); });
    });

    return {
      update(time, dt) {
        flows.forEach((f) => f.update(dt));
        [fPdh1, fPdh2].forEach((f) => { f.group.visible = locked; });
        // 參考腔內來回反射的光
        const pts = []; for (let i = 0; i < 40; i++) { const zig = Math.abs(((i % 8) / 4) - 1); pts.push([ULE.x - 0.52 + 1.04 * zig, ULE.y + 0.12 * Math.sin(i * 0.9 + time * 3) * (locked ? 0.3 : 1), ULE.z + 0.06 * Math.cos(i * 1.3)]); }
        bounce.set(pts); bounce.obj.material.opacity = locked ? 0.9 : 0.25;
        // 梳齒閃爍
        teeth.forEach((b, n) => { const h = 0.25 + 0.75 * Math.exp(-Math.pow((n - 13) / 8, 2)); b.scale.y = h * (0.85 + 0.15 * Math.sin(time * 5 + n)); b.position.y = 1.9 + (b.scale.y) / 2; });
        ring.rotation.z = time * 0.8;
        // 雷射到原子：鎖住時穩定，沒鎖住時亮度抖動（相位雜訊示意）
        const jit = locked ? 0 : 0.25;
        ryd[0].on(true, 0.5 + jit * (Math.random() - 0.5)); ryd[1].on(true, 0.4 + jit * (Math.random() - 0.5));
        atoms.forEach((a, i) => a.glow(0.4 + 0.25 * Math.sin(time * 3 + i) + (locked ? 0 : 0.3 * Math.random())));
        // 噴泉：上拋 → 落下，週期 4 s；穿過微波腔時閃爍
        if (showF) {
          const T = 4, u = (time % T) / T;
          const y = 0.3 + 3.2 * 4 * u * (1 - u);
          cloud.position.set(FX, y, -0.4);
          const inCav = Math.abs(y - 1.2) < 0.2;
          fcav.material.emissive.setHex(inCav ? 0x664020 : 0x000000);
          cloud.glow(inCav ? 1 : 0.4);
          lbF[2].set(u < 0.5 ? (y > 1.4 ? '自由演化（只有原子自己的相位在走）' : '上升') : (y > 1.4 ? '自由演化' : '落下 → 偵測'));
          lbF[2].pos.set(FX + 1.1, Math.max(1.6, y), -0.4);
        }
        const ph = App.ramseyPhase(ref, F0, Tr), e = czErr(lw());
        lbStat.set(locked ? '雷射已鎖頻：線寬 ≈ 1 kHz' : '雷射自由運轉：線寬 ≈ 100 kHz');
        ro.innerHTML = `微波參考 <b>${App.FREF[ref].name}</b>：σ_y(${Tr < 1 ? (Tr * 1000).toPrecision(2) + ' ms' : Tr.toPrecision(2) + ' s'}) ≈ ${App.sciFmt(App.FREF[ref].s(Tr))} → 6.835 GHz 在 T 內相位誤差 ≈ <b style="color:${ph > 1 ? '#ff8a8a' : '#8ef0a0'}">${ph < 0.01 ? ph.toExponential(1) : ph.toFixed(2)} rad</b><br>`
          + `芮德堡雷射線寬 ≈ ${locked ? '1 kHz（PDH 鎖到 ULE 腔）' : '100 kHz（自由運轉）'} → 只算線寬的 CZ 錯誤 ≈ <b style="color:${e > 0.005 ? '#ff8a8a' : '#8ef0a0'}">${(e * 100).toFixed(e < 0.01 ? 2 : 1)} %</b>${e > 0.005 ? '（比整個閘的錯誤預算還大）' : ''}<br>`
          + '光頻梳把雷射頻率接回 10 MHz 基準：參考腔慢慢飄，靠梳子校正絕對頻率';
      },
    };
  },
});
