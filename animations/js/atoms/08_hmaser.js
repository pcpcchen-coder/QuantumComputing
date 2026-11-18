/* 離子阱場景 8：氫邁射（Hydrogen maser）— 控制微波的頻率基準
 * 3D：H₂ 氣瓶 → 射頻放電解離器 → 六極磁鐵選態 → 鐵氟龍儲存泡 + 銅色 TE₀₁₁ 共振腔 → 接收機鎖相 → 10 MHz → 12.6 GHz → ¹⁷¹Yb⁺
 * 振盪模型（示意、可調）：腔內場能 W，上能階原子以 βW 受激輻射（W += 1），下能階原子以 βW 吸收（W −= 1），腔損耗 W/τ。
 * 有粒子數反轉且 β(N↑ − N↓)τ > 1 時才會起振。
 * 插圖的 Allan 偏差與 Ramsey 相位誤差用代表性的經驗模型（量級正確，實際依機型而異）。
 */
App.register({
  id: 'hmaser', num: 8, short: '氫邁射：頻率基準',
  title: '氫邁射：控制微波的「節拍器」',
  subtitle: '把上能階的氫原子關在鐵氟龍泡裡，放進 1.42 GHz 銅腔，讓它們自己同調放出微波——再用它鎖住 12.6 GHz 的閘微波',
  desc: `<p><b>為什麼需要它</b>：單位元閘就是打 12.6 GHz 微波（場景 3、7），<b>脈衝面積 = 角度、微波相位 = 旋轉軸</b>。微波源只要有一點頻率飄移或相位雜訊，量子位元就會累積 Z 誤差（等於 dephasing）。離子的 T₂ 可以到秒級以上，<b>控制微波反而變成限制</b>，所以實驗室把所有 RF / 微波 / FPGA 鎖到同一個超穩定的 10 MHz 參考；氫邁射是短中期（1 秒～1 天）最穩定的微波頻率源之一。</p>
<p><b>21 公分線</b>：氫原子基態的電子自旋與質子自旋平行（F=1）或反平行（F=0），相差 <span class="eq">1,420,405,751.77 Hz</span>。用的是 |F=1, m=0⟩ ↔ |F=0, m=0⟩「時鐘躍遷」，對磁場一階不敏感——和 ¹⁷¹Yb⁺ 量子位元選時鐘態的理由完全一樣。</p>
<p><b>運作四步</b>：<br>① <b>解離</b>：H₂ 經射頻放電拆成 H 原子，形成原子束。<br>② <b>選態</b>：六極磁鐵（類似 Stern–Gerlach）把 F=1（m=+1、0，「弱場尋求者」）聚焦進管子，F=0 與 m=−1 被甩開 → 泡裡形成<b>粒子數反轉</b>。<br>③ <b>儲存</b>：原子在內壁塗<b>鐵氟龍</b>的石英泡裡亂彈約 1 秒、撞牆上萬次而相位幾乎不被破壞 → 譜線寬約 1 Hz，<span class="eq">Q ≈ 10⁹</span>。<br>④ <b>受激輻射</b>：腔內 1.42 GHz 場刺激上能階原子放出同頻同相的光子，場變強又刺激更多原子；增益超過腔損耗就<b>自我維持振盪</b>（maser = Microwave Amplification by Stimulated Emission of Radiation）。輸出只有約 −100 dBm，再把一顆石英振盪器鎖相到它，輸出 10 MHz / 100 MHz / 1 PPS。</p>
<p><b>Cavity pulling</b>：腔頻偏 Δf<sub>腔</sub> 會把振盪頻率拉動約 (Q<sub>腔</sub>/Q<sub>原子</sub>)·Δf<sub>腔</sub>，所以腔體溫度要精密控制，外面再包好幾層 μ-metal 磁屏蔽。</p>
<p><b>歷史</b>：1960 年哈佛的 Norman Ramsey 與學生 Daniel Kleppner、H. M. Goldenberg 做出第一台。Ramsey 的「分離振盪場法」就是你在量子位元上量 T₂* 的 Ramsey 實驗。<b>1989 年諾貝爾物理獎</b>：Ramsey（分離振盪場法與氫邁射）＋ Paul 與 Dehmelt（離子阱技術）——Paul 阱（場景 2）、電子擱置讀取（場景 3）與這台時鐘出自同一屆。</p>
<p><b>實務</b>：不是每個離子阱實驗室都配氫邁射，很多用銣鐘或 GPS 馴服振盪器就夠；做長時間相干實驗或精密量測時才需要這個等級。氫邁射也用在 VLBI 電波天文（例如事件視界望遠鏡各站）、衛星導航地面站與國家時間標準。光學原子鐘已經超越它好幾個數量級，其中之一正是離子阱（Al⁺ 量子邏輯鐘）。</p>
<p>拿掉選態器（沒有粒子數反轉）或把原子流量調低（低於閾值），腔內就不會起振。</p>`,
  camera: { pos: [0.9, 3.9, 11.9], target: [0.9, 1.15, 0] },
  build(ctx) {
    const { scene, U, THREE, ui } = ctx;
    const AY = 1.5; // 原子束高度
    const BC = new THREE.Vector3(0.6, AY, 0), BRAD = 0.72; // 儲存泡中心與半徑

    /* ---------- 氣瓶、解離器 ---------- */
    const bottle = new THREE.Mesh(new THREE.CylinderGeometry(0.28, 0.28, 1.3, 24), U.metal(0x8a93a0)); bottle.position.set(-5.4, 0.85, 0); scene.add(bottle);
    scene.add(U.sphere(0.28, U.metal(0x8a93a0), -5.4, 1.5, 0, 20));
    ctx.label('H₂ 氣瓶', [-5.4, 0.05, 0], 'small');
    scene.add(U.tube([[-5.4, 1.75, 0], [-5.4, 2.0, 0], [-4.4, 2.0, 0], [-4.4, AY + 0.35, 0]], 0.03, U.metal(0xc0c6d0)));
    const diss = U.sphere(0.36, new THREE.MeshStandardMaterial({ color: 0xff8ad8, emissive: 0xc040b0, emissiveIntensity: 0.9, transparent: true, opacity: 0.55 }), -4.4, AY, 0, 24); scene.add(diss);
    for (let k = 0; k < 4; k++) { const c = new THREE.Mesh(new THREE.TorusGeometry(0.42, 0.018, 6, 28), U.metal(0xd4a050)); c.rotation.y = Math.PI / 2; c.position.set(-4.62 + k * 0.15, AY, 0); scene.add(c); }
    ctx.label('① 射頻放電解離器：H₂ → 2H', [-4.4, AY + 0.75, 0], 'small');

    /* ---------- 六極磁鐵 ---------- */
    const HX0 = -3.0, HX1 = -1.5, HR = 0.24;
    for (let k = 0; k < 6; k++) {
      const a = (k / 6) * Math.PI * 2;
      const m = new THREE.Mesh(new THREE.CylinderGeometry(0.055, 0.055, HX1 - HX0, 12), U.mat(k % 2 ? 0x4f8cff : 0xff5a5f, { metalness: 0.4 }));
      m.rotation.z = Math.PI / 2; m.position.set((HX0 + HX1) / 2, AY + HR * Math.cos(a), HR * Math.sin(a)); scene.add(m);
    }
    const lbHex = ctx.label('② 六極磁鐵選態器', [(HX0 + HX1) / 2, AY - 0.55, 0.3], 'small');
    scene.add(U.tube([[-1.45, AY, 0], [BC.x - BRAD - 0.02, AY, 0]], 0.07, new THREE.MeshStandardMaterial({ color: 0xcfe6ff, transparent: true, opacity: 0.35 })));
    ctx.label('準直管', [-0.8, AY - 0.3, 0], 'small');

    /* ---------- 儲存泡、共振腔、C 場線圈、磁屏蔽 ---------- */
    const bulb = new THREE.Mesh(new THREE.SphereGeometry(BRAD, 32, 20), new THREE.MeshStandardMaterial({ color: 0xe8f4ff, transparent: true, opacity: 0.16, roughness: 0.1, depthWrite: false }));
    bulb.position.copy(BC); scene.add(bulb);
    const bulbRim = new THREE.Mesh(new THREE.SphereGeometry(BRAD + 0.01, 24, 14), new THREE.MeshBasicMaterial({ color: 0xffffff, wireframe: true, transparent: true, opacity: 0.08 }));
    bulbRim.position.copy(BC); scene.add(bulbRim);
    const cav = new THREE.Mesh(new THREE.CylinderGeometry(1.2, 1.2, 2.1, 40, 1, true), new THREE.MeshStandardMaterial({ color: 0xd9894a, metalness: 0.8, roughness: 0.3, transparent: true, opacity: 0.28, side: THREE.DoubleSide, depthWrite: false }));
    cav.position.copy(BC); scene.add(cav);
    [1.05, -1.05].forEach((dy) => { const c = new THREE.Mesh(new THREE.CylinderGeometry(1.2, 1.2, 0.04, 40), new THREE.MeshStandardMaterial({ color: 0xd9894a, metalness: 0.8, roughness: 0.3, transparent: true, opacity: 0.22, depthWrite: false })); c.position.set(BC.x, BC.y + dy, 0); scene.add(c); });
    const field = new THREE.Mesh(new THREE.CylinderGeometry(1.12, 1.12, 1.95, 40, 1, true), new THREE.MeshBasicMaterial({ color: 0xd8ff6a, transparent: true, opacity: 0, side: THREE.DoubleSide, depthWrite: false, blending: THREE.AdditiveBlending }));
    field.position.copy(BC); scene.add(field);
    ctx.label('③ 鐵氟龍內襯石英儲存泡', [BC.x, BC.y - BRAD - 0.25, 0.8], 'small');
    ctx.label('④ 銅色微波共振腔（TE₀₁₁，1.42 GHz）', [BC.x, BC.y + 1.35, 0], 'gold');
    for (let k = 0; k < 7; k++) { const c = new THREE.Mesh(new THREE.TorusGeometry(1.3, 0.012, 6, 48), U.metal(0xd4a050)); c.rotation.x = Math.PI / 2; c.position.set(BC.x, BC.y - 0.9 + k * 0.3, 0); scene.add(c); }
    const shields = [1.55, 1.8].map((r) => { const s = new THREE.Mesh(new THREE.CylinderGeometry(r, r, 2.6 + (r - 1.55) * 0.8, 40, 1, true), new THREE.MeshStandardMaterial({ color: 0xaab4c4, metalness: 0.6, roughness: 0.4, transparent: true, opacity: 0.12, side: THREE.DoubleSide, depthWrite: false })); s.position.copy(BC); scene.add(s); return s; });
    const lbShield = ctx.label('μ-metal 磁屏蔽 × 多層 + C 場線圈', [BC.x - 1.6, BC.y - 1.4, 1.0], 'small');

    /* ---------- 輸出：耦合環 → 接收機 → 10 MHz → 合成器 → 號角 → 離子 ---------- */
    const loop = new THREE.Mesh(new THREE.TorusGeometry(0.12, 0.02, 6, 20), U.metal(0xd4a050)); loop.position.set(BC.x + 1.1, BC.y + 0.4, 0); loop.rotation.y = Math.PI / 2; scene.add(loop);
    const RX = [3.4, 1.3, 0];
    const rx = App.device(ctx, { pos: RX, w: 1.2, h: 0.6, d: 0.7, label: '接收機 + 鎖相迴路<br>（石英 VCXO 鎖到 1.42 GHz）', cls: 'small', leds: 3, ledColor: 0x666666 });
    const SY = [3.4, 0.0, 1.6];
    App.device(ctx, { pos: SY, w: 1.2, h: 0.45, d: 0.6, label: '微波合成器（PLL）<br>10 MHz → 12.6428 GHz', cls: 'small', leds: 2, ledColor: 0x38c6d9 });
    const fOut = App.Flow(scene, [[BC.x + 1.25, BC.y + 0.4, 0], [2.3, BC.y + 0.4, 0], [2.3, RX[1] + 0.3, 0], [RX[0] - 0.6, RX[1] + 0.3, 0]], 0xd8ff6a, { radius: 0.025, speed: 1.6, dot: 0.035, pipeOpacity: 0.4 });
    const f10 = App.Flow(scene, [[RX[0], RX[1], 0.35], [RX[0], RX[1] - 0.25, 0.9], [SY[0], SY[1] + 0.45, SY[2] - 0.3]], 0x38c6d9, { radius: 0.025, speed: 1.2, dot: 0.035, pipeOpacity: 0.4 });
    ctx.label('10 MHz 參考', [RX[0] + 0.75, RX[1] - 0.05, 0.9], 'teal');
    const HN = new THREE.Vector3(4.55, 0.25, 1.6), ION = new THREE.Vector3(5.6, 0.45, 1.6);
    const fSyn = App.Flow(scene, [[SY[0] + 0.6, SY[1] + 0.22, SY[2]], [HN.x - 0.25, HN.y, HN.z]], 0x38c6d9, { radius: 0.025, speed: 1.5, dot: 0.035, pipeOpacity: 0.4 });
    const horn = new THREE.Mesh(new THREE.ConeGeometry(0.2, 0.4, 4, 1, true), U.metal(0xb7a46a, { side: THREE.DoubleSide }));
    horn.position.copy(HN); horn.lookAt(ION); horn.rotateX(-Math.PI / 2); scene.add(horn);
    const ion = App.particle(scene, App.QC.ion, 0.1, ION.toArray());
    [[1, 1], [-1, -1], [1, -1], [-1, 1]].forEach(([a, b], k) => { const m = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 0.9, 10), U.metal(k < 2 ? 0xd9a441 : 0x8a93a0, { transparent: true, opacity: 0.45 })); m.rotation.z = Math.PI / 2; m.position.set(ION.x, ION.y + a * 0.18, ION.z + b * 0.18); scene.add(m); });
    ctx.label('¹⁷¹Yb⁺：12.6 GHz 單位元閘', [ION.x, ION.y + 0.45, ION.z], 'gold');
    const phMw = App.photons(scene, 0x38c6d9, 40, { size: 0.025 });
    const phE = App.photons(scene, 0xd8ff6a, 120, { size: 0.03 });
    const lbState = ctx.label('', [BC.x, -0.6, 1.4], 'big');

    /* ---------- 原子 ---------- */
    const NP = 280;
    const geoA = new THREE.SphereGeometry(0.045, 10, 8);
    const matUp = new THREE.MeshBasicMaterial({ color: 0xff5a5f }), matLo = new THREE.MeshBasicMaterial({ color: 0x4f8cff });
    const pool = [];
    for (let i = 0; i < NP; i++) { const m = new THREE.Mesh(geoA, matUp); m.visible = false; scene.add(m); pool.push({ m, v: new THREE.Vector3(), mode: 'off', up: true, ttl: 0, lost: 0 }); }
    let selector = true, flux = 0.7, W = 0, spawnAcc = 0;
    const BETA = 0.1, TAU = 0.5, SEED = 0.01, TSTORE = 4.0;
    let Ws = 0, osc = false; // 平滑後的場能（顯示用）與是否起振（含遲滯）
    const spawn = () => {
      const p = pool.find((q) => q.mode === 'off'); if (!p) return;
      p.mode = 'beam'; p.up = Math.random() < 0.5; p.m.material = p.up ? matUp : matLo; p.m.visible = true;
      p.m.position.set(-4.05, AY + U.gauss() * 0.03, U.gauss() * 0.03);
      p.v.set(1.9 + Math.random() * 0.4, U.gauss() * 0.04, U.gauss() * 0.04);
    };
    const kill = (p) => { p.mode = 'off'; p.m.visible = false; };

    /* ---------- 控制 ---------- */
    ui.toggle('② 六極磁鐵選態器', true, (on) => { selector = on; });
    ui.slider('原子流量', 0, 1, 0.05, flux, (v) => { flux = v; }, (v) => `${(v * 100).toFixed(0)} %`);
    ui.toggle('顯示磁屏蔽', true, (on) => { shields.forEach((s) => { s.visible = on; }); lbShield.show(on); });
    let tab = 'level', ref = 'H', Tr = 10;
    ui.radio([['level', '插圖：能階'], ['allan', '插圖：Allan 穩定度'], ['ramsey', '插圖：對量子位元的影響']], 'level', (v) => { tab = v; });
    ui.radio([['Q', '石英 OCXO'], ['Rb', '銣鐘'], ['Cs', '銫鐘'], ['H', '氫邁射']], 'H', (v) => { ref = v; });
    ui.slider('Ramsey 自由演化時間 T', -3, 2, 0.1, Math.log10(Tr), (v) => { Tr = Math.pow(10, v); }, (v) => { const t = Math.pow(10, v); return t < 1 ? `${(t * 1000).toPrecision(2)} ms` : `${t.toPrecision(2)} s`; });
    const ro = ui.readout();

    const REF = App.FREF, F0 = 12.6428e9;
    const dphi = (k, T) => App.ramseyPhase(k, F0, T);
    const sciFmt = App.sciFmt;

    ctx.inset('', (g, W2, H, P) => {
      const t = document.getElementById('inset-title');
      if (tab === 'level') {
        t.textContent = '氫原子基態的超精細分裂（21 公分線）';
        const L = (x0, x1, y, col) => { g.strokeStyle = col; g.lineWidth = 3; g.beginPath(); g.moveTo(x0, y); g.lineTo(x1, y); g.stroke(); g.lineWidth = 1; };
        L(40, 110, 50, '#ff8a8a'); L(40, 110, 64, '#ff5a5f'); L(40, 110, 78, '#ff8a8a'); L(40, 110, 186, '#4f8cff');
        P.text(g, 'F=1', 116, 68, '#ffb0b2'); P.text(g, 'm = +1 / 0 / −1', 150, 52, '#cfd8e6'); P.text(g, 'F=0, m=0', 116, 190, '#a9c6ff');
        g.strokeStyle = '#d8ff6a'; g.lineWidth = 2; g.beginPath(); g.moveTo(75, 68); g.lineTo(75, 180); g.stroke(); g.beginPath(); g.moveTo(69, 172); g.lineTo(75, 182); g.lineTo(81, 172); g.stroke(); g.lineWidth = 1;
        P.text(g, '1,420,405,751.77 Hz', 150, 120, '#d8ff6a'); P.text(g, '（m=0 ↔ m=0 時鐘躍遷）', 150, 138, '#cfd8e6');
        P.text(g, '電子自旋 ↑↑ 質子自旋', 150, 82, '#ffb0b2'); P.text(g, '電子自旋 ↑↓ 質子自旋', 150, 206, '#a9c6ff');
        P.text(g, '選態器只放行 F=1 的 m=+1、0 → 粒子數反轉', 190, 222, '#ffd28a', 'center');
        P.text(g, '¹⁷¹Yb⁺ 量子位元是同一種結構（12.6 GHz）', 190, 18, '#ffd28a', 'center');
        return;
      }
      const xr = tab === 'allan' ? [0, 5] : [-3, 2];
      const yr = tab === 'allan' ? [-16, -10] : [-5, 2];
      const xt = tab === 'allan' ? [[0, '1 s'], [1, '10 s'], [2, '100 s'], [3, '10³ s'], [4, '10⁴ s'], [5, '10⁵ s']] : [[-3, '1 ms'], [-2, '10 ms'], [-1, '0.1 s'], [0, '1 s'], [1, '10 s'], [2, '100 s']];
      const yt = tab === 'allan' ? [[-16, '10⁻¹⁶'], [-14, '10⁻¹⁴'], [-12, '10⁻¹²'], [-10, '10⁻¹⁰']] : [[-4, '10⁻⁴'], [-2, '0.01'], [0, '1 rad'], [2, '100']];
      t.textContent = tab === 'allan' ? 'Allan 偏差 σ_y(τ)：頻率在 τ 秒內平均的相對抖動（代表值）' : `Ramsey 時間 T 內累積的相位誤差 @ 12.6 GHz（粗估）`;
      const { X, Y } = P.frame(g, W2, H, xr, yr, { xticks: xt, yticks: yt, xlabel: tab === 'allan' ? '平均時間 τ' : '自由演化時間 T', m: { l: 52, b: 32, t: 8 } });
      Object.entries(REF).forEach(([k, r]) => {
        const f = tab === 'allan' ? (x) => Math.log10(r.s(Math.pow(10, x))) : (x) => Math.log10(dphi(k, Math.pow(10, x)));
        g.save(); g.beginPath(); g.rect(X(xr[0]), Y(yr[1]), X(xr[1]) - X(xr[0]), Y(yr[0]) - Y(yr[1])); g.clip();
        P.curve(g, f, xr[0], xr[1], X, Y, r.col, k === ref ? 3 : 1.4); g.restore();
      });
      let ly = 18; Object.entries(REF).forEach(([k, r]) => { P.text(g, r.name, W2 - 64, ly, r.col); ly += 15; });
      if (tab === 'ramsey') {
        g.strokeStyle = '#ff8a8a'; g.setLineDash([4, 3]); g.beginPath(); g.moveTo(X(xr[0]), Y(0)); g.lineTo(X(xr[1]), Y(0)); g.stroke(); g.setLineDash([]);
        P.text(g, '≈ 1 rad：相位糊掉', X(-2.9), Y(0) - 5, '#ff8a8a');
        const lx = Math.log10(Tr); g.strokeStyle = '#ffd28a'; g.beginPath(); g.moveTo(X(lx), Y(yr[0])); g.lineTo(X(lx), Y(yr[1])); g.stroke();
      }
    });

    return {
      update(time, dt) {
        // 產生原子
        spawnAcc += dt * 70 * flux;
        while (spawnAcc >= 1) { spawnAcc -= 1; spawn(); }
        let nUp = 0, nLo = 0;
        const rate = BETA * W;
        pool.forEach((p) => {
          if (p.mode === 'off') return;
          const pos = p.m.position;
          if (p.mode === 'beam') {
            if (pos.x > HX0 && pos.x < HX1 && selector) {
              const ry = pos.y - AY, rz = pos.z;
              const k = p.up ? -9 : 9; // 弱場尋求者聚焦、強場尋求者散焦
              p.v.y += k * ry * dt; p.v.z += k * rz * dt;
            }
            pos.addScaledVector(p.v, dt);
            const r = Math.hypot(pos.y - AY, pos.z);
            if (pos.x > HX0 && pos.x < HX1 && r > HR - 0.04) { p.mode = 'lost'; p.lost = 0.6; }
            else if (pos.x > -1.45 && r > 0.12) { p.mode = 'lost'; p.lost = 0.4; }
            else if (pos.distanceTo(BC) < BRAD) { p.mode = 'bulb'; p.ttl = TSTORE * (0.6 + 0.8 * Math.random()); const d = new THREE.Vector3(U.gauss(), U.gauss(), U.gauss()).normalize(); p.v.copy(d).multiplyScalar(1.1); }
          } else if (p.mode === 'lost') {
            pos.addScaledVector(p.v, dt); p.lost -= dt; if (p.lost <= 0) kill(p);
          } else if (p.mode === 'bulb') {
            pos.addScaledVector(p.v, dt);
            const d = pos.clone().sub(BC);
            if (d.length() > BRAD - 0.05) { const n = d.normalize(); p.v.addScaledVector(n, -2 * p.v.dot(n)); p.v.add(new THREE.Vector3(U.gauss(), U.gauss(), U.gauss()).multiplyScalar(0.15)).setLength(1.1); pos.copy(BC).addScaledVector(n, BRAD - 0.06); }
            // 受激輻射 / 吸收
            if (p.up) {
              if (Math.random() < (rate + SEED) * dt) { p.up = false; p.m.material = matLo; W += 1; phE.emit(pos, null, 1.4, 0.35); }
            } else if (Math.random() < rate * dt) { p.up = true; p.m.material = matUp; W = Math.max(0, W - 1); }
            if (p.up) nUp++; else nLo++;
            p.ttl -= dt; if (p.ttl <= 0) kill(p);
          }
        });
        W = Math.max(0, W - (W / TAU) * dt);
        phE.update(dt); phMw.update(dt);
        Ws += (W - Ws) * Math.min(1, dt / 1.5);
        osc = osc ? Ws > 0.5 : Ws > 1.5;
        const amp = Math.min(1, Ws / 4);
        field.material.opacity = (0.04 + 0.4 * amp) * (0.65 + 0.35 * Math.sin(time * 2 * Math.PI * 2.5));
        diss.material.emissiveIntensity = 0.6 + 0.4 * Math.sin(time * 9);
        ion.glow(osc ? 0.6 + 0.3 * Math.sin(time * 6) : 0.3);
        [fOut, f10, fSyn].forEach((f) => { f.on = osc; f.update(dt); });
        fOut.mat.color.setHex(osc ? 0xd8ff6a : 0x444444); f10.mat.color.setHex(osc ? 0x38c6d9 : 0x444444); fSyn.mat.color.setHex(osc ? 0x38c6d9 : 0x444444);
        if (osc && Math.random() < dt * 14) phMw.emit(HN, ION.clone().sub(HN), 1.6, 0.65);
        rx.children.forEach((c) => { if (c.geometry && c.geometry.type === 'SphereGeometry') c.material.color.setHex(osc ? 0x2ecc71 : 0x666666); });
        const thr = Math.ceil(1 / (BETA * TAU));
        const status = osc ? '振盪中：輸出 1.42 GHz' : !selector ? '沒有粒子數反轉 → 不會起振' : nUp - nLo < thr ? '低於起振閾值' : '起振中…';
        lbState.set(status);
        lbHex.set(selector ? '② 六極磁鐵選態器：紅 = F=1（聚焦）、藍 = F=0 / m=−1（甩開）' : '② 選態器關閉：兩種原子都進泡');
        const s = REF[ref].s(Tr), ph = dphi(ref, Tr);
        ro.innerHTML = `泡內原子：<b style="color:#ffb0b2">上能階 ${nUp}</b>、<b style="color:#a9c6ff">下能階 ${nLo}</b>（起振需要 N↑ − N↓ ≳ ${thr}）<br>`
          + `腔內場能（示意，平滑）：${Ws.toFixed(1)}　${osc ? '<b style="color:#8ef0a0">接收機已鎖定 → 10 MHz 輸出</b>' : '<b style="color:#ff8a8a">接收機未鎖定</b>'}<br>`
          + `參考源 <b>${REF[ref].name}</b>：σ_y(${Tr < 1 ? (Tr * 1000).toPrecision(2) + ' ms' : Tr.toPrecision(2) + ' s'}) ≈ ${sciFmt(s)} → 12.6 GHz 微波在 T 內相位誤差 ≈ <b style="color:${ph > 1 ? '#ff8a8a' : '#8ef0a0'}">${ph < 0.01 ? ph.toExponential(1) : ph.toFixed(2)} rad</b>${ph > 1 ? '（量子位元相位糊掉）' : ''}`;
      },
    };
  },
});
