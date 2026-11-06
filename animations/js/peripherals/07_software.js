/* 周邊場景 7：軟體堆疊 — 從量子程式到微波脈衝，再把量測結果送回 */
App.register({
  id: 'software', num: 7, short: '軟體堆疊',
  title: '軟體堆疊：量子程式如何變成微波',
  subtitle: '雲端 API → 編譯器 → 脈衝層 → 控制韌體 → 硬體；校準資料庫貫穿其中',
  desc: `<p><b>使用者層</b>：以 Qiskit、Cirq 等寫量子電路，經排程佇列送到機器。</p>
<p><b>編譯器</b>：把任意閘分解為硬體的<b>原生閘</b>，依晶片連接關係做<b>量子位元映射與路由</b>（插入 SWAP），並最佳化深度。</p>
<p><b>脈衝層</b>：每個原生閘查<b>校準資料庫</b>（頻率、振幅、DRAG 係數、讀取參數…）轉成具體脈衝，排出時間表。</p>
<p><b>控制韌體</b>：序列器在 FPGA 上以奈秒精度播放波形、處理即時分支。</p>
<p>結果（IQ → 0/1 → 統計）沿原路回傳。<b>自動校準服務</b>定期量測並更新資料庫，因為量子位元參數會隨時間漂移。</p>`,
  camera: { pos: [6.5, 4.5, 10], target: [0.6, 2.6, 0] },
  build(ctx) {
    const { scene, U, THREE, ui } = ctx;
    const layers = [
      ['使用者程式 / 雲端 API', 'Qiskit · Cirq · OpenQASM', 0x8ef0ff],
      ['編譯器', '原生閘分解 · 映射 · 路由 · 最佳化', 0x4f8cff],
      ['脈衝層', '閘 → 脈衝（查校準資料）· 排程', 0xe0a54a],
      ['控制韌體 / 序列器', 'FPGA · 波形記憶體 · 即時分支', 0xff7a59],
      ['硬體', '電子學 · 冷凍機 · 量子晶片', 0x2ecc71],
    ];
    const LY = (i) => 4.6 - i * 1.0;
    const slabs = layers.map(([n, d, c], i) => {
      const m = U.box(4.2, 0.18, 2.4, new THREE.MeshStandardMaterial({ color: c, transparent: true, opacity: 0.28, roughness: 0.4, emissive: c, emissiveIntensity: 0.05 }), 0, LY(i), 0);
      scene.add(m);
      m.add(new THREE.LineSegments(new THREE.EdgesGeometry(m.geometry), new THREE.LineBasicMaterial({ color: c, transparent: true, opacity: 0.8 })));
      ctx.label(`<b>${n}</b><br><span style="color:#9fb0c8">${d}</span>`, [-3.6, LY(i), 1.2], 'small');
      return m;
    });
    // 側邊服務
    const db = new THREE.Mesh(new THREE.CylinderGeometry(0.55, 0.55, 0.9, 28), U.mat(0xe0a54a, { emissive: 0x3a2400, emissiveIntensity: 0.5 })); db.position.set(3.6, LY(2), 0); scene.add(db);
    ctx.label('校準資料庫', [3.6, LY(2) + 0.75, 0], 'gold');
    const cal = U.box(1.1, 0.6, 0.8, U.mat(0x2a3446, { emissive: 0x38c6d9, emissiveIntensity: 0.2 }), 3.6, LY(4) + 0.3, 0); scene.add(cal);
    ctx.label('自動校準服務', [3.6, LY(4) + 0.95, 0], 'teal small');
    const qq = U.box(1.1, 0.5, 0.8, U.mat(0x2a3446), 3.6, LY(0), 0); scene.add(qq);
    ctx.label('工作佇列 / 排程器', [3.6, LY(0) + 0.6, 0], 'small');
    const mon = U.box(1.1, 0.5, 0.8, U.mat(0x2a3446), -3.6, LY(4) - 0.9, -1.0); scene.add(mon);
    ctx.label('監控 / 日誌', [-3.6, LY(4) - 0.4, -1.0], 'small');
    const f1 = App.Flow(scene, [[2.2, LY(2), 0], [3.05, LY(2), 0]], 0xe0a54a, { speed: 0.8, radius: 0.03 });
    const f2 = App.Flow(scene, [[3.6, LY(4) + 0.6, 0], [3.6, LY(2) - 0.45, 0]], 0x38c6d9, { speed: 0.6, radius: 0.03 });
    const f3 = App.Flow(scene, [[3.1, LY(4) + 0.3, 0], [2.2, LY(4), 0]], 0x38c6d9, { speed: 0.6, radius: 0.03 });
    const f4 = App.Flow(scene, [[3.05, LY(0), 0], [2.2, LY(0), 0]], 0x8ef0ff, { speed: 0.6, radius: 0.03 });
    const f5 = App.Flow(scene, [[-1.5, LY(4), -0.9], [-3.05, LY(4) - 0.9, -1.0]], 0x9aa4b2, { speed: 0.5, radius: 0.02 });
    // 下行 / 上行封包
    const down = U.box(0.35, 0.35, 0.35, U.mat(0xffffff, { emissive: 0xffffff, emissiveIntensity: 0.5 })); scene.add(down);
    const up = U.sphere(0.2, U.glow(0x2ecc71)); scene.add(up);
    const dl = ctx.labelOn(down, '', [0.9, 0.3, 0], 'gold small');
    const ul = ctx.labelOn(up, '', [-1.0, 0.3, 0], 'q0 small');
    const dTxt = ['量子電路（H、CNOT…）', '原生閘 + 實體量子位元', '脈衝序列（含時間表）', '波形 + 指令', '微波脈衝'];
    const uTxt = ['IQ 原始資料', '0 / 1 位元串', '位元串', '直方圖 / 期望值', '結果回到使用者'];
    let speed = 1;
    ui.slider('播放速度', 0.3, 2, 0.1, speed, (v) => { speed = v; }, (v) => v.toFixed(1) + '×');
    const ro = ui.readout();
    let cur = 0;
    ctx.inset('同一個程式在不同層的樣子', (g, W, H, P) => {
      P.text(g, '電路層', 8, 18, cur <= 1 ? '#ffd28a' : '#9fb0c8');
      // 電路
      for (let q = 0; q < 2; q++) { g.strokeStyle = '#9fb0c8'; g.beginPath(); g.moveTo(60, 30 + q * 30); g.lineTo(370, 30 + q * 30); g.stroke(); P.text(g, `q${q}`, 40, 34 + q * 30, '#cfd8e6'); }
      g.fillStyle = '#4f8cff'; g.fillRect(90, 18, 26, 24); P.text(g, 'H', 98, 35, '#fff');
      g.strokeStyle = '#4f8cff'; g.beginPath(); g.moveTo(170, 30); g.lineTo(170, 60); g.stroke(); P.dot(g, 170, 30, 5, '#4f8cff'); g.beginPath(); g.arc(170, 60, 9, 0, 6.3); g.stroke();
      g.fillStyle = '#e0a54a'; g.fillRect(250, 18, 26, 54); P.text(g, 'M', 257, 50, '#1a1206');
      P.text(g, '脈衝層（時間 →）', 8, 108, cur >= 2 ? '#ffd28a' : '#9fb0c8');
      const lane = (y, name) => { g.strokeStyle = 'rgba(160,180,210,.3)'; g.beginPath(); g.moveTo(80, y); g.lineTo(370, y); g.stroke(); P.text(g, name, 8, y + 4, '#9fb0c8'); };
      lane(130, 'q0 XY'); lane(155, 'q1 XY'); lane(180, 'CR / Z'); lane(205, '讀取');
      const gp = (x0, w, y, c) => { g.fillStyle = c; g.beginPath(); for (let i = 0; i <= 30; i++) { const x = x0 + (w * i) / 30; const a = Math.exp(-((((i / 30) - 0.5) / 0.2) ** 2)) * 9; i ? g.lineTo(x, y - a) : g.moveTo(x, y); } g.lineTo(x0 + w, y); g.fill(); };
      gp(90, 26, 130, '#4f8cff'); gp(90, 26, 155, '#4f8cff'); g.fillStyle = '#2ecc71'; g.fillRect(130, 172, 90, 8); gp(130, 30, 130, '#6fb4ff'); gp(190, 30, 130, '#6fb4ff');
      g.fillStyle = '#e0a54a'; g.fillRect(240, 197, 110, 8);
    });
    let tt = 0;
    return {
      update(time, dt) {
        tt += dt * speed * 0.55; const ph = tt % 2; // 0–1 下行，1–2 上行
        if (ph < 1) {
          const y = LY(0) + 0.5 - ph * (LY(0) - LY(4) + 0.5); down.position.set(-0.4, y, 0); down.visible = true; up.visible = false;
          cur = U.clamp(Math.floor(ph * 5), 0, 4); dl.set(dTxt[cur]); down.rotation.y += dt;
        } else {
          const p = ph - 1; const y = LY(4) + p * (LY(0) - LY(4) + 0.4); up.position.set(0.8, y, 0); up.visible = true; down.visible = false;
          cur = 4 - U.clamp(Math.floor(p * 5), 0, 4); ul.set(uTxt[4 - cur]);
        }
        slabs.forEach((s, i) => (s.material.emissiveIntensity = i === cur ? 0.6 : 0.05));
        [f1, f2, f3, f4, f5].forEach((f) => f.update(dt));
        ro.innerHTML = `目前所在：<b>${layers[cur][0]}</b><br>${ph < 1 ? '↓ 編譯與下傳' : '↑ 量測結果回傳'}<br>校準參數每隔數小時～數天需重新量測（頻率、振幅、讀取閾值會漂移）`;
      },
    };
  },
});
