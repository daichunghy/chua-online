
    // ---- 5. KHÓI NHANG (C3) — sprite mềm, chỉ cháy ở lư đã thắp ----
    function smokeTexture() {
      const cv = document.createElement('canvas'); cv.width = 128; cv.height = 128;
      const ctx = cv.getContext('2d');
      const g = ctx.createRadialGradient(64, 64, 4, 64, 64, 62);
      g.addColorStop(0, 'rgba(255,255,255,0.85)');
      g.addColorStop(0.45, 'rgba(255,255,255,0.38)');
      g.addColorStop(1, 'rgba(255,255,255,0)');
      ctx.fillStyle = g; ctx.fillRect(0, 0, 128, 128);
      const tex = new THREE.CanvasTexture(cv);
      return tex;
    }
    const smokeTex = smokeTexture();
    class SmokeColumn {
      constructor(origin, count, indoor) {
        this.origin = origin; this.count = count; this.active = false; this.fade = 0;
        this.parts = [];
        for (let i = 0; i < count; i++) {
          const m = new THREE.SpriteMaterial({ map: smokeTex, color: 0xcfc8bd, transparent: true, opacity: 0, depthWrite: false });
          const sp = new THREE.Sprite(m);
          if (indoor) sp.layers.set(1);
          sp.visible = false;
          scene.add(sp);
          this.parts.push({ sp, age: Math.random() * 8, life: 6 + Math.random() * 4, seed: Math.random() * 10, rise: 0.25 + Math.random() * 0.15 });
        }
      }
      setActive(on) { this.active = on; }
      update(dt, t) {
        const target = this.active ? 1 : 0;
        this.fade += (target - this.fade) * Math.min(1, dt / 3); // bật dần ~3s
        const show = this.fade > 0.02;
        for (const p of this.parts) {
          p.age += dt;
          if (p.age > p.life) { p.age = 0; p.life = 6 + Math.random() * 4; }
          const k = p.age / p.life;
          const y = this.origin.y + p.age * p.rise * (1 + p.age * 0.04);
          const x = this.origin.x + 0.08 * p.age + Math.sin(p.age * 1.4 + p.seed) * 0.12 * p.age;
          const z = this.origin.z + Math.cos(p.age * 1.1 + p.seed) * 0.06 * p.age;
          const size = 0.08 + k * 1.2;
          p.sp.position.set(x, y, z);
          p.sp.scale.set(size, size, 1);
          p.sp.material.opacity = this.fade * Math.sin(Math.PI * Math.min(1, k)) * 0.36;
          p.sp.visible = show && p.sp.material.opacity > 0.01;
        }
      }
    }
    const smokeMain = new SmokeColumn(new THREE.Vector3(23, 3.0, 11), 120, false);
    const smokeDiLac = new SmokeColumn(new THREE.Vector3(-24, 1.6, 2.2), 90, false);
    const smokeAdida = new SmokeColumn(new THREE.Vector3(-13, 1.6, 24.2), 90, false);
    const smokeAltar = new SmokeColumn(new THREE.Vector3(300, 4.6, 300 + altarZ + 1.8), 40, true);
    const smokeColumns = { main: smokeMain, dilac: smokeDiLac, adida: smokeAdida, altar: smokeAltar };

    // ---- Lá bồ đề rơi ngoài sân (G5) — trong điện KHÔNG có mưa cánh ----
    const leafFall = [];
    const leafGeo = new THREE.PlaneGeometry(0.16, 0.22);
    const leafFallMat = new THREE.MeshBasicMaterial({ color: 0x7A9B4E, side: THREE.DoubleSide, transparent: true, opacity: 0.9 });
    const leafTrees = [[15, 0], [31, 8], [-20, 28], [6, -34], [42, -38], [-34, 10], [50, 10]];
    for (let i = 0; i < 25; i++) {
      const m = new THREE.Mesh(leafGeo, leafFallMat);
      const t = leafTrees[i % leafTrees.length];
      m.position.set(t[0] + (Math.random() - 0.5) * 6, 2 + Math.random() * 5, t[1] + (Math.random() - 0.5) * 6);
      scene.add(m);
      leafFall.push({ m, seed: Math.random() * 10, speed: 0.25 + Math.random() * 0.2 });
    }

    // ---- Bồ câu sân chùa (G5) — đậu, mổ thóc, bay vụt khi đến gần <3m ----
    const pigeons = [];
    function makePigeon(x, z) {
      const g = new THREE.Group(); g.position.set(x, 0.12, z);
      const body = addBall(0, 0.12, 0, 0.14, mat(0x8A8A8A, 0.8), g); body.scale.set(1, 0.8, 1.4);
      addBall(0, 0.28, -0.16, 0.08, mat(0x5A5A5A, 0.8), g);
      const wL = addBox(-0.16, 0.16, 0, 0.04, 0.02, 0.28, mat(0x6E6E6E, 0.8), g);
      const wR = addBox(0.16, 0.16, 0, 0.04, 0.02, 0.28, mat(0x6E6E6E, 0.8), g);
      g.traverse(o => { o.castShadow = false; });
      scene.add(g);
      return { group: g, wL, wR, state: 'perch', tx: x, tz: z, seed: Math.random() * 10, peck: Math.random() * 2 };
    }
    [[20, 14], [26, 16], [18, 8], [28, 7], [22, 20], [16, 18], [30, 18], [24, 5]].forEach(([x, z]) => pigeons.push(makePigeon(x, z)));
