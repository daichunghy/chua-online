
    // ---- 3. KHUÔN VIÊN CHÙA VĨNH TRÀNG (procedural, theo bố cục layout_v10_v8 + ref9) ----
    // Tọa độ Three.js: x = Blender x, z = -Blender y (đã đối chiếu probe_v4)
    const grounds = new THREE.Group();
    scene.add(grounds);
    const colRects = [], colCircles = [];
    function colRect(x0, z0, x1, z1) { colRects.push([x0, z0, x1, z1]); }
    function colCircle(x, z, r) { colCircles.push([x, z, r]); }
    const fishes = [];

    const stoneMat = mat(0x8A7A63, 0.85);
    const stoneDark = mat(0x6E675C, 0.9);
    const fenceGoldMat = mat(0xC9962E, 0.5, 0.3);
    const woodSignMat = mat(0x5A3D26, 0.7);
    const roofMat = new THREE.MeshStandardMaterial({ map: roofTex, roughness: 0.7 });
    roofTex.repeat.set(3, 2);
    // v7.2: texture cờ Phật giáo 5 sọc (xanh dương · vàng · đỏ · trắng · cam)
    function buddhistFlagTexture72() {
      const cv = document.createElement('canvas'); cv.width = 100; cv.height = 64;
      const ctx = cv.getContext('2d');
      ['#3A6BC5', '#F2C230', '#D94F3D', '#F5F0E6', '#E8852A'].forEach((c, i) => {
        ctx.fillStyle = c; ctx.fillRect(i * 20, 0, 20, 64);
      });
      const tex = new THREE.CanvasTexture(cv);
      tex.colorSpace = THREE.SRGBColorSpace;
      return tex;
    }
    const flagTex72 = buddhistFlagTexture72();
    const flagMat72 = new THREE.MeshBasicMaterial({ map: flagTex72, side: THREE.DoubleSide });
    const wallGoldMat = mat(0xD9A441, 0.6);
    const pillarRedMat = mat(0x7E2A22, 0.45);
    const grilleMat = mat(0x2B2320, 0.6, 0.4);
    const waterMat = new THREE.MeshStandardMaterial({ color: 0x4E5F3A, roughness: 0.15, metalness: 0.35, transparent: true, opacity: 0.92 });
    const flowerPinkMat = mat(0xEE7FAE, 0.5);
    const flowerRedMat = mat(0xD94F3D, 0.5);

    // --- Nền đất ngoài rào + sân lát gạch trong khuôn viên ---
    const outerGround = new THREE.Mesh(new THREE.PlaneGeometry(260, 260),
      new THREE.MeshStandardMaterial({ color: 0x7A8A5A, roughness: 1 }));
    outerGround.rotation.x = -Math.PI / 2; outerGround.position.set(7, -0.05, 0);
    outerGround.receiveShadow = true; grounds.add(outerGround);
    const slab = new THREE.Mesh(new THREE.PlaneGeometry(93, 95),
      new THREE.MeshStandardMaterial({ map: pavingTex, roughness: 0.95 }));
    pavingTex.repeat.set(24, 24);
    slab.rotation.x = -Math.PI / 2; slab.position.set(7.7, 0, 5.5);
    slab.receiveShadow = true; grounds.add(slab);
    // Đường chính từ cổng vào chánh điện
    const road = new THREE.Mesh(new THREE.PlaneGeometry(9, 43),
      new THREE.MeshStandardMaterial({ color: 0xBFAE8E, roughness: 0.95 })); // v7.2: đá sáng ấm
    road.rotation.x = -Math.PI / 2; road.position.set(23, 0.02, 20);
    road.receiveShadow = true; grounds.add(road);

    // --- Hồ nước (xanh rêu + cá + sen) ---
    function makePond(cx, cz) {
      const g = new THREE.Group(); g.position.set(cx, 0, cz); grounds.add(g);
      const water = new THREE.Mesh(new THREE.PlaneGeometry(18.4, 14.4), waterMat);
      water.rotation.x = -Math.PI / 2; water.position.y = 0.12; water.receiveShadow = true; g.add(water);
      addBox(0, 0.25, -7.5, 19.9, 0.5, 0.45, stoneMat, g);
      addBox(0, 0.25, 7.5, 19.9, 0.5, 0.45, stoneMat, g);
      addBox(-9.7, 0.25, 0, 0.45, 0.5, 15.4, stoneMat, g);
      addBox(9.7, 0.25, 0, 0.45, 0.5, 15.4, stoneMat, g);
      // v7.2: Lan can ĐÁ chạm quanh hồ (như ảnh mẫu) — trụ đá + tay vịn đá + chỉ vàng dưới tay vịn
      for (let i = -9; i <= 9; i += 2.25) {
        addCyl(i, 0.72, -7.5, 0.07, 0.55, stoneMat, g);
        addCyl(i, 0.72, 7.5, 0.07, 0.55, stoneMat, g);
      }
      addBox(0, 1.02, -7.5, 19.9, 0.14, 0.34, stoneDark, g);
      addBox(0, 1.02, 7.5, 19.9, 0.14, 0.34, stoneDark, g);
      addBox(0, 0.88, -7.5, 19.9, 0.05, 0.36, fenceGoldMat, g);
      addBox(0, 0.88, 7.5, 19.9, 0.05, 0.36, fenceGoldMat, g);
      // v7.2: Lá sen + hoa sen hồng NỞ + nụ (trước chỉ là bóng hồng tròn)
      const leafMat72 = mat(0x3E6B34, 0.8);
      const leafSpots72 = [[-7, -4], [-3.5, 3.5], [0, -4.5], [3.5, 4], [7, -3.5], [-6, 4.5], [6, 3], [0.5, 0.5]];
      leafSpots72.forEach(([lx, lz], li) => {
        const leaf = addBall(lx, 0.17, lz, 0.5 + (li % 3) * 0.12, leafMat72, g); leaf.scale.set(1, 0.14, 1); leaf.castShadow = false;
      });
      function lotusFlower72(lx, lz, s) {
        const fg = new THREE.Group(); fg.position.set(lx, 0.16, lz); g.add(fg);
        for (let p = 0; p < 6; p++) {
          const a = (p / 6) * Math.PI * 2;
          const petal = addBall(Math.cos(a) * 0.16 * s, 0.16 * s, Math.sin(a) * 0.16 * s, 0.17 * s, flowerPinkMat, fg);
          petal.scale.set(1, 1.25, 0.55); petal.rotation.set(Math.sin(a) * 0.7, 0, -Math.cos(a) * 0.7);
          petal.castShadow = false;
        }
        const core = addBall(0, 0.2 * s, 0, 0.09 * s, mat(0xF2C230, 0.6), fg); core.castShadow = false;
        addCyl(0, 0.02, 0, 0.025, 0.2, leafMat72, fg).castShadow = false;
      }
      lotusFlower72(-5.2, -1.5, 1.15); lotusFlower72(2.2, 2.2, 1.0); lotusFlower72(5.8, -4.6, 1.25); lotusFlower72(-1.8, -5.2, 0.9);
      [[-3.9, -0.8], [4.4, 5.4]].forEach(([bx, bz]) => { // nụ sen
        const bud = addBall(bx, 0.42, bz, 0.16, flowerPinkMat, g); bud.scale.set(0.8, 1.5, 0.8); bud.castShadow = false;
        addCyl(bx, 0.2, bz, 0.025, 0.3, leafMat72, g).castShadow = false;
      });
      for (let i = 0; i < 4; i++) {
        const f = addBall(0, 0.05, 0, 0.16, mat(i % 2 ? 0xE8A33D : 0xE8E2D4, 0.5), g);
        f.scale.set(1.8, 0.6, 0.7);
        fishes.push({ mesh: f, cx, cz, ang: i * 1.7, r: 3 + i * 1.2, sp: 0.12 + i * 0.03 });
      }
      colRect(cx - 9.9, cz - 7.5, cx + 9.9, cz + 7.5);
    }
    makePond(5, 16);
    makePond(41, 16);

    // --- Rào vàng kín chu vi (chừa 2 cổng phía nam) ---
    function fenceRun(x0, z0, x1, z1) {
      const len = Math.hypot(x1 - x0, z1 - z0);
      const n = Math.floor(len / 2.2);
      for (let i = 0; i <= n; i++) {
        const t = i / n;
        addCyl(x0 + (x1 - x0) * t, 0.7, z0 + (z1 - z0) * t, 0.07, 1.4, fenceGoldMat, grounds);
      }
      const bar = addBox((x0 + x1) / 2, 1.25, (z0 + z1) / 2, len, 0.08, 0.08, fenceGoldMat, grounds);
      bar.rotation.y = -Math.atan2(z1 - z0, x1 - x0);
      const base = addBox((x0 + x1) / 2, 0.2, (z0 + z1) / 2, len, 0.4, 0.3, stoneMat, grounds);
      base.rotation.y = -Math.atan2(z1 - z0, x1 - x0);
    }
    fenceRun(-38.6, -42.1, 54.1, -42.1);          // bắc
    fenceRun(-38.6, 53.1, 14, 53.1);              // nam (trừ cổng 1)
    fenceRun(32, 53.1, 36, 53.1);                 // nam giữa 2 cổng
    fenceRun(54, 53.1, 54.1, 53.1);               // nam (trừ cổng 2)
    fenceRun(-38.6, -42.1, -38.6, 53.1);          // tây
    fenceRun(54.1, -42.1, 54.1, 53.1);            // đông

    // --- Cổng tam quan (mosaic, 1 vòm lớn, tượng Phật trắng ở hốc trên) ---
    function makeGate(x, z, name, name2) {
      const g = new THREE.Group(); g.position.set(x, 0, z); grounds.add(g);
      addBox(-3.4, 2.2, 0, 1.6, 4.4, 1.4, mat(0xC9962E, 0.6), g); // trụ trái
      addBox(3.4, 2.2, 0, 1.6, 4.4, 1.4, mat(0xC9962E, 0.6), g); // trụ phải
      // Vòm lớn giữa
      const arch = new THREE.Mesh(new THREE.TorusGeometry(2.2, 0.55, 10, 20, Math.PI), mat(0xC9962E, 0.6));
      arch.position.set(0, 4.4, 0); arch.castShadow = true; g.add(arch);
      addBox(0, 6.2, 0, 9.2, 1.2, 1.6, mat(0x2C4A8A, 0.5), g); // tầng mosaic cobalt
      addBox(0, 7.4, 0, 7.4, 1.0, 1.4, mat(0x3F7D5D, 0.5), g); // tầng mosaic ngọc
      addBox(0, 8.6, 0, 5.6, 0.9, 1.2, mat(0xA03A2A, 0.5), g); // tầng mosaic đỏ
      const roof = addBox(0, 9.6, 0, 8.4, 0.5, 2.2, roofMat, g);
      roof.rotation.z = 0;
      // Tượng Phật trắng ở hốc giữa tầng trên
      const niche = addBox(0, 6.2, 0.85, 1.8, 2.2, 0.2, mat(0xE8E2D4, 0.6), g);
      const bBody = addBall(0, 6.0, 1.0, 0.55, mat(0xEFE9DD, 0.4), g); bBody.scale.set(1, 1.4, 0.7);
      addBall(0, 7.0, 1.0, 0.3, mat(0xEFE9DD, 0.4), g);
      // Bảng tên cổng
      const sign = plaque([name, name2], 4.4, 1.1, { w: 512, h: 128, bg: '#1C5A34', fg: '#FFD166', font: 'bold 56px Georgia, serif' });
      sign.position.set(0, 5.0, 0.95); g.add(sign);
      // Hai cửa BÊN (khách vào cửa phụ hai bên, cửa giữa dành cho chư Tăng)
      [-1, 1].forEach(s => {
        addBox(s * 6.6, 1.9, 0, 1.5, 3.8, 1.3, mat(0xC9962E, 0.6), g); // trụ ngoài
        const sArch = new THREE.Mesh(new THREE.TorusGeometry(1.05, 0.34, 8, 16, Math.PI), mat(0xC9962E, 0.6));
        sArch.position.set(s * 5.1, 3.8, 0); sArch.castShadow = true; g.add(sArch);
        addBox(s * 5.1, 4.6, 0, 4.4, 0.55, 1.3, mat(0x2C4A8A, 0.5), g); // dầm mosaic trên cửa bên
      });
      colRect(x - 4.2, z - 1, x - 2.6, z + 1);
      colRect(x + 2.6, z - 1, x + 4.2, z + 1);
      colRect(x - 7.4, z - 1, x - 5.8, z + 1);
      colRect(x + 5.8, z - 1, x + 7.4, z + 1);
      return g;
    }
    makeGate(23, 40.7, 'PHƯƠNG TIỆN', 'CỔNG CHÍNH');
    makeGate(45, 40.7, 'TỊNH ĐỘ', 'CỔNG PHỤ');

    // --- Chánh điện (mặt tiền vàng, 13 vòm, cột đỏ, mái đỏ 2 tầng) ---
    const hall = new THREE.Group(); hall.position.set(23, 0, -1); grounds.add(hall);
    addBox(0, 2.7, 0, 28, 5.4, 10, wallGoldMat, hall); // thân điện
    addBox(0, 0.4, 5.1, 28.6, 0.8, 0.6, mat(0xE8E2D4, 0.6), hall); // gờ chân tường
    // 13 vòm cửa (mở tối) + cột đỏ giữa các vòm
    for (let i = 0; i < 13; i++) {
      const x = -12 + i * 2;
      const archTrim = new THREE.Mesh(new THREE.TorusGeometry(0.85, 0.17, 8, 16, Math.PI), wallGoldMat); // v7.3: viền vòm dày hơn cho có lớp
      archTrim.position.set(x, 2.4, 5.12); archTrim.castShadow = true; hall.add(archTrim);
      const dark = addBox(x, 1.6, 5.06, 1.5, 3.2, 0.1, mat(0x1E1410, 0.9), hall);
      dark.castShadow = false;
      if (i < 12) {
        addCyl(x + 1, 2.2, 5.15, 0.22, 4.4, pillarRedMat, hall); // cột đỏ
        addBox(x + 1, 4.48, 5.15, 0.58, 0.32, 0.58, fenceGoldMat, hall); // v7.2: đầu cột vàng
        addBox(x + 1, 0.32, 5.15, 0.56, 0.5, 0.56, fenceGoldMat, hall); // v7.2: chân cột vàng
      }
    }
    addCyl(-13, 2.2, 5.15, 0.22, 4.4, pillarRedMat, hall);
    addCyl(13, 2.2, 5.15, 0.22, 4.4, pillarRedMat, hall);
    addBox(-13, 4.48, 5.15, 0.58, 0.32, 0.58, fenceGoldMat, hall);
    addBox(13, 4.48, 5.15, 0.58, 0.32, 0.58, fenceGoldMat, hall);
    // Song sắt vàng trước vòm (lattice)
    for (let i = 0; i < 13; i++) {
      const x = -12 + i * 2;
      for (let j = 0; j < 3; j++) addBox(x - 0.5 + j * 0.5, 1.6, 5.3, 0.05, 3.2, 0.05, fenceGoldMat, hall);
    }
    // v7.2 — TẦNG TRANG TRÍ MẶT TIỀN như ảnh mẫu 67/68 + ref1: dải frieze kem,
    // BIỂN LỚN "CHÙA VĨNH TRÀNG" đọc được từ sân, ô phù điêu màu xen kẽ.
    // v7.3 — CHẨN ĐOÁN V7.2 biển không đọc được: (1) biển 9,6×1,45 quá nhỏ ở
    // khoảng cách sân ~35m; (2) mái tầng 1 (sâu 13, tâm y6,2, nghiêng 0,18) nhô
    // ra z≈6,4 và hạ xuống y≈4,7 ở mép trước -> che + đổ bóng lên băng biển;
    // (3) vật liệu biển MeshStandard bị nắng tây làm tối. Sửa: biển 13,4×2,05
    // vật liệu Basic (giữ nguyên độ sáng như biển sơn nắng), băng kem cao 2,15
    // nhô hẳn ra trước, mái tầng 1 nâng lên 6,5 + rút sâu còn 11,6.
    const creamMat72 = mat(0xE8E2D4, 0.6);
    addBox(0, 3.38, 5.14, 28.6, 0.14, 0.26, creamMat72, hall); // v7.3: chỉ kem trên hàng vòm
    addBox(0, 3.55, 5.18, 28.6, 0.2, 0.3, fenceGoldMat, hall); // v7.3: chỉ vàng phân lớp
    addBox(0, 4.78, 5.22, 28.6, 2.15, 0.34, creamMat72, hall); // băng kem NHÔ (mặt trước z=5,39)
    addBox(0, 5.93, 5.26, 28.8, 0.16, 0.36, fenceGoldMat, hall); // chỉ vàng trên băng
    addBox(0, 3.66, 5.26, 28.8, 0.14, 0.36, fenceGoldMat, hall); // chỉ vàng dưới băng
    const hallSign = plaque(['CHÙA VĨNH TRÀNG'], 13.4, 2.05, { w: 3072, h: 512, bg: '#6E1420', fg: '#FFE066', font: 'bold 296px Georgia, serif' }); // v7.3d: texture x2 (3072x512, font 296) — bản 1536/148px vẽ dấu ĐÚNG (đã kiểm chứng canvas riêng) nhưng mip-map ở khoảng cách sân ~30m làm dấu (vài texel) nhòe biến mất, ảnh chụp đọc thành "CHUA VINH TRANG"; tăng độ phân giải + anisotropy để dấu sống qua minification
    hallSign.material = new THREE.MeshBasicMaterial({ map: hallSign.material.map }); // v7.3: biển giữ độ sáng/ tương phản ở mọi góc nắng
    hallSign.material.map.anisotropy = 8;
    hallSign.position.set(0, 4.78, 5.48); hall.add(hallSign);
    for (let i = 0; i < 4; i++) { // ô phù điêu màu hai bên biển — v7.3: to + sâu + lõi vàng cho có chiều sâu thật
      const rx = 7.9 + i * 1.7;
      [-1, 1].forEach(sd => {
        addBox(sd * rx, 4.78, 5.32, 1.35, 1.5, 0.24, mat(i % 2 ? 0x3F7D5D : 0xA03A2A, 0.55), hall);
        addBox(sd * rx, 4.78, 5.47, 0.8, 0.95, 0.06, fenceGoldMat, hall);
      });
    }
    for (let fx = -13; fx <= 13.01; fx += 2) addBall(fx, 6.12, 5.3, 0.11, fenceGoldMat, hall).castShadow = false; // v7.3: hàng chóp vàng nhỏ dưới mép mái (silhouette như mẫu)
    // v8: DẢI MOSAIC COBALT dưới mép mái tầng 1 — tiệm cận tông vàng+lam của
    // ảnh tham chiếu V8 bằng đúng mã lam mosaic của cổng (#2C4A8A, palette đã
    // khóa). Mái giữ đỏ nâu theo ảnh thật Vĩnh Tràng, KHÔNG đổi theo mockup.
    addBox(0, 6.30, 5.28, 28.6, 0.30, 0.30, mat(0x2C4A8A, 0.55), hall);
    for (let fx = -12.5; fx <= 12.51; fx += 2.5) addBox(fx, 6.30, 5.45, 0.5, 0.34, 0.06, fenceGoldMat, hall); // ô vàng xen trên dải lam
    // Mái 2 tầng cong + rêu
    const roof1 = addBox(0, 6.5, 0, 31, 0.7, 11.6, roofMat, hall); roof1.rotation.x = 0.18; // v7.3: nâng + rút sâu, hết che biển
    const roof2 = addBox(0, 8.6, 0, 26, 0.6, 11, roofMat, hall); roof2.rotation.x = 0.18;
    // v7.3: cụm trang trí nóc TRƯỚC (trên sườn mái, giữa mặt tiền) — phá silhouette phẳng
    addBox(0, 6.75, 3.2, 4.6, 0.9, 0.8, fenceGoldMat, hall);
    addBox(0, 7.5, 3.2, 3.0, 0.8, 0.7, fenceGoldMat, hall);
    addBall(0, 8.05, 3.2, 0.3, fenceGoldMat, hall);
    addCyl(0, 8.6, 3.2, 0.06, 0.7, fenceGoldMat, hall);
    addBall(0, 9.05, 3.2, 0.16, mat(0xFFAA00, 0.2, 0, 1, 1.6), hall);
    addBox(0, 9.4, 0, 26.5, 0.5, 0.5, fenceGoldMat, hall); // sống mái
    // v7.2: trang trí nóc nhiều lớp như ảnh mẫu — gờm trung tâm + chóp hai đầu hồi + cờ Phật giáo
    addBox(0, 10.05, 0, 3.6, 0.85, 0.6, fenceGoldMat, hall);
    addBox(0, 10.75, 0, 2.3, 0.7, 0.5, fenceGoldMat, hall);
    addBall(0, 11.45, 0, 0.42, fenceGoldMat, hall);
    addBall(0, 11.95, 0, 0.2, mat(0xFFAA00, 0.2, 0, 1, 1.6), hall);
    [-11.8, 11.8].forEach(sx => {
      addBox(sx, 9.95, 0, 1.1, 0.6, 0.55, fenceGoldMat, hall);
      addBall(sx, 10.5, 0, 0.3, fenceGoldMat, hall);
    });
    addCyl(13.6, 10.6, 0, 0.045, 2.6, stoneDark, hall); // cột cờ đầu hồi phải
    const hallFlag = new THREE.Mesh(new THREE.PlaneGeometry(1.15, 0.75), flagMat72);
    hallFlag.position.set(14.2, 11.55, 0); hall.add(hallFlag);
    [[-13, 1.2, 2.8], [-10, 1.8, 3.6], [-7.5, 1.0, 3.0], [-4, 1.5, 4.0], [-1, 2.0, 3.2],
     [2.5, 1.1, 3.8], [6, 1.6, 2.9], [9.5, 1.3, 3.5], [12.5, 1.0, 3.1]].forEach(([mx, mw, mz]) => {
      const moss = addBox(mx, 6.87 - mz * 0.182, mz, mw, 0.08, 2.6, mat(0x55663A, 0.95), hall); // v7.3: y bám mặt mái tầng 1 đã nâng (6,5)
      moss.rotation.x = 0.18; moss.castShadow = false;
    });
    // Bậc thềm 5 bậc + đèn đá 2 bên
    for (let i = 0; i < 5; i++) addBox(0, 0.12 + i * 0.12, 5.9 + i * 0.55, 16 - i * 1.2, 0.24, 0.6, stoneMat, hall);
    [[-9, 6.5], [9, 6.5]].forEach(([x, z]) => {
      addBox(x, 0.7, z, 0.5, 1.4, 0.5, stoneDark, hall);
      addBox(x, 1.55, z, 0.7, 0.3, 0.7, stoneDark, hall);
      addBall(x, 1.85, z, 0.22, mat(0xFFAA00, 0.2, 0, 1, 1.6), hall);
    });
    // v7.2: hai tháp nhỏ hai đầu mặt tiền (như ảnh mẫu 67/68 — tháp chuông/trống thu nhỏ)
    [-15.6, 15.6].forEach(tx => {
      addBox(tx, 2.5, 3, 2.4, 5.0, 2.4, wallGoldMat, hall);
      addBox(tx, 5.25, 3, 2.8, 0.5, 2.8, creamMat72, hall);
      const cap = new THREE.Mesh(new THREE.ConeGeometry(2.0, 1.5, 4), roofMat);
      cap.position.set(tx, 6.25, 3); cap.rotation.y = Math.PI / 4; cap.castShadow = true; hall.add(cap);
      addBall(tx, 7.25, 3, 0.26, fenceGoldMat, hall);
      addBox(tx, 3.1, 4.25, 1.1, 2.2, 0.12, mat(0x1E1410, 0.9), hall); // ô cửa tối mặt trước tháp
      addBox(tx, 4.62, 4.26, 1.2, 0.55, 0.1, mat(0x2C4A8A, 0.55), hall); // v8: ô mosaic cobalt trên mặt tháp (cùng dải lam mặt tiền)
    });
    colRect(23 - 14, -1 - 12, 23 + 14, -1 + 2.2);
    colRect(23 - 16.8, -1 + 1.8, 23 - 14.4, -1 + 4.2); // tháp trái (world)
    colRect(23 + 14.4, -1 + 1.8, 23 + 16.8, -1 + 4.2); // tháp phải (world)

    // --- Tượng A Di Đà trắng, đài sen xanh (S1) ---
    function makeStandingBuddha(x, z, plaqueLines) {
      const g = new THREE.Group(); g.position.set(x, 0, z); grounds.add(g);
      addCyl(0, 0.35, 0, 2.2, 0.7, mat(0x8A4A3A, 0.8), g); // bệ đỏ nâu
      // v7.3: đài sen dùng vật liệu riêng có emissive nhẹ đúng mã #4E86A8 — bản
      // V7.2 chung mat() bị grade/ACES làm bợt, nhìn từ sân không đọc được xanh.
      const lotusMat73 = new THREE.MeshStandardMaterial({ color: 0x4E86A8, roughness: 0.55, emissive: 0x1E4258, emissiveIntensity: 0.5 });
      const lotus = addBall(0, 0.9, 0, 1.7, lotusMat73, g); lotus.scale.set(1, 0.45, 1); // đài sen xanh
      for (let i = 0; i < 10; i++) {
        const a = (i / 10) * Math.PI * 2;
        const petal = addBall(Math.cos(a) * 1.55, 0.85, Math.sin(a) * 1.55, 0.4, lotusMat73, g);
        petal.scale.set(1, 0.5, 0.6); petal.rotation.y = -a;
      }
      const body = addBall(0, 2.6, 0, 0.95, mat(0xEFE9DD, 0.4), g); body.scale.set(1, 1.7, 0.75);
      addBall(0, 4.5, 0, 0.45, mat(0xEFE9DD, 0.4), g);
      addCyl(0, 4.85, 0, 0.16, 0.3, mat(0xEFE9DD, 0.4), g); // nhục kế
      const sign = plaque(plaqueLines, 3.4, 1.0, { w: 512, h: 160, bg: '#5A3D26', fg: '#FFD166', font: 'bold 44px Georgia, serif' });
      sign.position.set(0, 1.1, 2.35); g.add(sign);
      // v7.2 — ĐO THẬT (nợ "tượng web nhỏ hơn thật"): chiều cao tượng+bệ hiện tại
      // ≈ 5,00 đv (đỉnh nhục kế: trụ y4.85 + h0.3/2 = 5,00); chánh điện tới nóc
      // chính ≈ 9,65 đv (sống mái y9.4 + h0.5/2) -> tỉ lệ 0,52. Tượng thật 18m
      // trên bệ 7m (tổng ~25m, lớn nhất khuôn viên); ảnh mẫu 67/68: tượng+bệ
      // ≈ 2/3 chiều cao mặt tiền tới nóc chính -> cần 6,43 đv -> scale ĐỒNG
      // DẠNG 1.29 (chỉ kích thước tổng thể, tuyệt đối không đổi hình/nét tượng).
      const ADIDA_SCALE = 1.29;
      g.scale.setScalar(ADIDA_SCALE);
      colCircle(x, z, 3.2 * ADIDA_SCALE);
      return g;
    }
    makeStandingBuddha(-14, 27, ['NAM MÔ A DI ĐÀ PHẬT']);
    // v7.3: phông lá xanh đậm phía sau tượng (bắc + tây) cho silhouette trắng
    // nổi hẳn — ảnh V7.2 tượng trắng chìm vào trời/cây sáng cùng tông.
    [[-19.5, 20.5, 2.7, 3.4], [-20.5, 26, 2.2, 4.4], [-8.5, 19.5, 2.4, 3.8]].forEach(([bx, bz, br, by]) => {
      const bk = addBall(bx, by, bz, br, mat(0x2F5527, 0.95), grounds); bk.scale.set(1.15, 0.95, 1.15); bk.castShadow = false;
    });
    // v7.2: hoa giấy hồng/đỏ ôm chân bệ A Di Đà (như ref3 + ảnh mẫu)
    [[-17.9, 24.0], [-10.1, 24.0], [-18.3, 30.5]].forEach(([fx, fz], fi) => {
      const sk = addBall(fx, 0.45, fz, 0.9, mat(0x3E6B34, 0.9), grounds); sk.scale.set(1.2, 0.7, 1.2);
      const fl = addBall(fx, 0.98, fz, 0.55, fi % 2 ? flowerRedMat : flowerPinkMat, grounds); fl.scale.set(1.25, 0.55, 1.25);
    });
    // Đài Quan Âm (trạm phụ trong vườn hoa, phía tây — chỉ vái, không thắp nhang)
    const qaGarden = new THREE.Group(); qaGarden.position.set(-27, 0, 21); grounds.add(qaGarden);
    addCyl(0, 0.3, 0, 1.9, 0.6, stoneDark, qaGarden);
    addCyl(0, 0.75, 0, 1.5, 0.3, stoneMat, qaGarden);
    const qaLotus = addBall(0, 1.0, 0, 1.05, mat(0x4E86A8, 0.5), qaGarden); qaLotus.scale.set(1, 0.4, 1);
    const qaBody = addBall(0, 2.1, 0, 0.55, mat(0xEFE9DD, 0.4), qaGarden); qaBody.scale.set(0.85, 1.6, 0.7);
    addBall(0, 3.35, 0, 0.3, mat(0xEFE9DD, 0.4), qaGarden);
    addCyl(0.42, 1.9, 0.3, 0.05, 0.55, mat(0xEFE9DD, 0.4), qaGarden); // tay cầm bình cam lồ
    addBall(0.42, 2.25, 0.3, 0.11, mat(0xEFE9DD, 0.4), qaGarden);
    const qaSign = plaque(['ĐÀI QUAN ÂM'], 2.6, 0.8, { w: 512, h: 160, bg: '#5A3D26', fg: '#FFD166', font: 'bold 52px Georgia, serif' });
    qaSign.position.set(0, 0.75, 1.75); qaGarden.add(qaSign);
    colCircle(-27, 21, 2.1);
    // Bệ đá + chữ Hán cho Di Lặc (S4)
    const dilac = new THREE.Group(); dilac.position.set(-24.5, 0, -3); grounds.add(dilac);
    addBox(0, 0.6, 0, 8, 1.2, 7, stoneDark, dilac);
    addBox(0, 1.3, 0, 6.5, 0.6, 5.5, stoneMat, dilac);
    const dBody = addBall(0, 3.0, 0, 1.9, mat(0xEFE9DD, 0.4), dilac); dBody.scale.set(1.15, 1.15, 0.9);
    addBall(0, 4.9, 0, 0.75, mat(0xEFE9DD, 0.4), dilac);
    addBall(0, 2.1, 0, 0.9, mat(0xEFE9DD, 0.4), dilac); // bụng tròn
    // Chuỗi hạt đeo cổ
    for (let i = 0; i < 12; i++) {
      const a = Math.PI * (0.15 + 0.7 * i / 11);
      addBall(Math.sin(a) * 0.9, 4.1 - Math.cos(a) * 0.9, 0.85, 0.09, mat(0x6B4226, 0.5), dilac);
    }
    const dSign = plaque(['南無彌勒尊佛'], 3.6, 1.0, { w: 512, h: 160, bg: '#5A3D26', fg: '#FFD166', font: 'bold 56px Georgia, serif' });
    dSign.position.set(0, 0.9, 4.1); dilac.add(dSign);
    for (let i = 0; i < 4; i++) addBox(-3.4 + i * 0.7, 1.75, 3.6, 0.5, 0.22, 0.3, stoneMat, dilac); // bậc lên bệ
    colRect(-24.5 - 4, -3 - 3.5, -24.5 + 4, -3 + 3.5);
    // Phật nằm bệ đá (S5)
    const recl = new THREE.Group(); recl.position.set(12, 0, -47); grounds.add(recl);
    addBox(0, 0.8, 0, 12, 1.6, 5, stoneDark, recl);
    addBox(0, 1.7, 0, 10.5, 0.5, 4, stoneMat, recl);
    const rBody = addBall(0, 2.5, 0, 1.1, mat(0xEFE9DD, 0.4), recl); rBody.scale.set(3.2, 1.0, 0.9);
    addBall(-3.9, 2.9, 0, 0.55, mat(0xEFE9DD, 0.4), recl);
    const rSign = plaque(['NAM MÔ BỔN SƯ', 'THÍCH CA MÂU NI PHẬT'], 5.2, 1.3, { w: 512, h: 128, bg: '#5A3D26', fg: '#FFD166', font: 'bold 40px Georgia, serif' });
    rSign.position.set(0, 1.0, 2.6); recl.add(rSign);
    colRect(12 - 6, -47 - 2.5, 12 + 6, -47 + 2.5);
    // Bảo tháp 7 tầng (S6)
    const tower = new THREE.Group(); tower.position.set(-2, 0, -41); grounds.add(tower);
    addBox(0, 1.0, 0, 7, 2, 7, mat(0xC88A4A, 0.6), tower);
    for (let i = 0; i < 7; i++) {
      const w = 6.4 - i * 0.7;
      addBox(0, 2.6 + i * 1.9, 0, w, 1.5, w, mat(0xC88A4A, 0.6), tower);
      const tr = addBox(0, 3.45 + i * 1.9, 0, w + 1.2, 0.35, w + 1.2, mat(0xA85A38, 0.6), tower);
      tr.rotation.y = 0;
    }
    addCyl(0, 16.6, 0, 0.12, 2.4, fenceGoldMat, tower);
    addBall(0, 17.9, 0, 0.35, fenceGoldMat, tower);
    colCircle(-2, -41, 4.5);
    // Giảng đường Huệ Đăng
    const lecture = new THREE.Group(); lecture.position.set(44, 0, -20); grounds.add(lecture);
    addBox(0, 2.2, 0, 14, 4.4, 9, mat(0xE8D8A0, 0.6), lecture);
    const lRoof = addBox(0, 5.0, 0, 16, 0.6, 11, roofMat, lecture); lRoof.rotation.x = 0.15;
    const lSign = plaque(['GIẢNG ĐƯỜNG', 'HUỆ ĐĂNG'], 5.0, 1.4, { w: 512, h: 160, bg: '#1C5A34', fg: '#FFF6E5', font: 'bold 48px Georgia, serif' });
    lSign.position.set(0, 3.2, 4.6); lecture.add(lSign);
    colRect(44 - 7, -20 - 4.5, 44 + 7, -20 + 4.5);
    // v8: trang trí trước Giảng đường (trục 4 — học viện phải là một nơi tử
    // tế trong cảnh): 2 tháp đèn đá + cặp bonsai chầu cửa + bảng gỗ lịch
    // giảng. Đã đo khoảng hở với tuyến đi của sư (44,-16)->(37,-23) và
    // (39,-7)->(44,-16): mọi vật cách tuyến >= 1,75m, không chồng hình.
    makeStoneLantern72(39, -13.8); makeStoneLantern72(49, -13.8);
    makeBonsai72(41, -14.2, 1); makeBonsai72(47, -14.2, 1);
    const lecBoard = plaque(['LỊCH GIẢNG', 'HUỆ ĐĂNG'], 2.6, 1.0, { w: 512, h: 192, bg: '#5A3D26', fg: '#FFD166', font: 'bold 52px Georgia, serif' });
    lecBoard.position.set(44, 1.7, -13.0); grounds.add(lecBoard);
    addBox(43.2, 0.8, -13.05, 0.14, 1.6, 0.14, woodSignMat, grounds);
    addBox(44.8, 0.8, -13.05, 0.14, 1.6, 0.14, woodSignMat, grounds);

    // --- Cây + hoa giấy + bonsai ---
    function makeTree(x, z, s, leafTex) {
      const g = new THREE.Group(); g.position.set(x, 0, z); grounds.add(g);
      const trunk = addCyl(0, 1.6 * s, 0, 0.22 * s, 3.2 * s, mat(0x5A3D26, 0.9), g);
      trunk.scale.set(1, 1, 1);
      const canopy = new THREE.Mesh(new THREE.SphereGeometry(2.4 * s, 12, 10),
        new THREE.MeshStandardMaterial({ map: leafTex, roughness: 0.9, transparent: true, alphaTest: 0.35 }));
      canopy.position.y = 3.9 * s; canopy.scale.set(1.25, 1.05, 1.25);
      canopy.castShadow = true; g.add(canopy);
      const c2 = new THREE.Mesh(new THREE.SphereGeometry(1.6 * s, 10, 8),
        new THREE.MeshStandardMaterial({ map: leafTex, roughness: 0.9, transparent: true, alphaTest: 0.35 }));
      c2.position.set(1.1 * s, 4.6 * s, 0.5 * s); c2.castShadow = true; g.add(c2);
      colCircle(x, z, 0.5 * s);
      return g;
    }
    const treeSpots = [
      [-30, 30, 1.1], [-32, 8, 1.3], [-34, -20, 1.0], [-28, -34, 1.2], [-10, -32, 0.9],
      [6, -34, 1.1], [14, -30, 1.0], [30, -32, 1.2], [38, -36, 1.0], [50, -30, 1.1],
      [52, -8, 1.2], [50, 8, 1.0], [36, 28, 1.1], [30, 8, 0.9], [16, -28, 1.0],
      [-8, 8, 1.0], [-18, -28, 1.1], [0, 30, 1.0], [-6, -12, 0.9], [48, -38, 1.2],
      [20, -28, 1.0], [-36, 22, 1.1], [34, -14, 0.9], [-14, 38, 1.0], [52, 26, 1.1],
      [-30, -8, 1.0], [10, 8, 0.9], [-4, 34, 1.1], [40, 6, 1.0], [-20, -38, 1.2],
    ];
    const leafTexs = [leafTexA, leafTexB, leafTexC];
    treeSpots.forEach(([x, z, s], i) => makeTree(x, z, s, leafTexs[i % 3]));
    // Vòng cây ngoài rào
    for (let i = 0; i < 23; i++) {
      const a = (i / 23) * Math.PI * 2;
      const x = 7.7 + Math.cos(a) * 62, z = 5.5 + Math.sin(a) * 58;
      if (z > 44 && x > 10 && x < 56) continue; // chừa lối cổng nam
      makeTree(x, z, 1.3 + Math.random() * 0.4, leafTexs[i % 3]);
    }
    // Cọ 12 cây
    for (let i = 0; i < 12; i++) {
      const spots = [[-36, 40], [-10, 44], [8, 44], [52, 44], [-36, -38], [52, -38], [0, -38], [20, 44], [34, 44], [-20, 44], [48, 20], [-34, -28]];
      const [x, z] = spots[i];
      const g = new THREE.Group(); g.position.set(x, 0, z); grounds.add(g);
      addCyl(0, 2.2, 0, 0.14, 4.4, mat(0x6B4226, 0.9), g);
      for (let k = 0; k < 7; k++) {
        const a = (k / 7) * Math.PI * 2;
        const leaf = addBox(Math.cos(a) * 1.1, 4.6, Math.sin(a) * 1.1, 0.5, 2.4, 0.18, mat(0x3E6B34, 0.85), g);
        leaf.rotation.z = Math.cos(a) * 0.9; leaf.rotation.x = -Math.sin(a) * 0.9;
      }
      colCircle(x, z, 0.4);
    }
    // Hoa giấy hồng + bonsai
    for (let i = 0; i < 14; i++) {
      const spots = [[16, 34], [30, 34], [-8, 20], [36, 10], [-30, 16], [50, 30], [10, -8], [-16, 8], [44, 30], [14, 26], [-36, -12], [52, -16], [4, -24], [-24, 30]];
      const [x, z] = spots[i];
      const skirt = addBall(x, 0.45, z, 0.85, mat(0x3E6B34, 0.9), grounds); skirt.scale.set(1.2, 0.7, 1.2);
      const b = addBall(x, 0.95, z, 0.5, i % 2 ? flowerRedMat : flowerPinkMat, grounds);
      b.scale.set(1.2, 0.55, 1.2);
      addCyl(x, 0.5, z, 0.12, 1.0, mat(0x5A3D26, 0.9), grounds);
    }
    [[20, 6.2], [26, 6.2], [18, 30], [28, 30]].forEach(([x, z]) => {
      addCyl(x, 0.35, z, 0.55, 0.7, mat(0x8A4A3A, 0.8), grounds);
      const bonsai = addBall(x, 1.0, z, 0.7, mat(0x3E6B34, 0.85), grounds); bonsai.scale.set(1, 0.7, 1);
      colCircle(x, z, 0.7);
    });
    // v7.2 — BONSAI CHẬU TRANG TRÍ dọc lối đi + cặp lớn chầu thềm điện (ref1 + ảnh mẫu)
    function makeBonsai72(x, z, s) {
      const g = new THREE.Group(); g.position.set(x, 0, z); grounds.add(g);
      addCyl(0, 0.38 * s, 0, 0.62 * s, 0.76 * s, mat(0x8A4A3A, 0.8), g); // chậu đất nung
      addCyl(0, 0.72 * s, 0, 0.65 * s, 0.1 * s, fenceGoldMat, g); // viền miệng chậu vàng
      addCyl(0, 0.95 * s, 0, 0.09 * s, 0.45 * s, mat(0x5A3D26, 0.9), g); // thân
      const t1 = addBall(0, 1.35 * s, 0, 0.85 * s, mat(0x3E6B34, 0.85), g); t1.scale.set(1.15, 0.5, 1.15);
      const t2 = addBall(0.18 * s, 1.78 * s, 0.1 * s, 0.58 * s, mat(0x4E7A3A, 0.85), g); t2.scale.set(1.1, 0.5, 1.1);
      colCircle(x, z, 0.75 * s);
      return g;
    }
    [[17.3, 30], [28.7, 30], [17.3, 26], [28.7, 26], [17.3, 14.5], [28.7, 14.5]].forEach(([x, z]) => makeBonsai72(x, z, 1));
    makeBonsai72(16.8, 6.4, 1.45); makeBonsai72(29.2, 6.4, 1.45); // cặp lớn hai bên thềm chánh điện
    // v7.2 — THÁP ĐÈN ĐÁ dọc lối (như ảnh mẫu)
    function makeStoneLantern72(x, z) {
      const g = new THREE.Group(); g.position.set(x, 0, z); grounds.add(g);
      addBox(0, 0.14, 0, 0.62, 0.28, 0.62, stoneDark, g);
      addCyl(0, 0.6, 0, 0.09, 0.65, stoneMat, g);
      addBox(0, 1.05, 0, 0.46, 0.42, 0.46, stoneMat, g);
      addBall(0, 1.05, 0, 0.15, mat(0xFFC46B, 0.25, 0, 1, 1.5), g).castShadow = false; // tim đèn ấm
      const cap = new THREE.Mesh(new THREE.ConeGeometry(0.44, 0.3, 4), stoneDark);
      cap.position.set(0, 1.42, 0); cap.rotation.y = Math.PI / 4; cap.castShadow = true; g.add(cap);
      addBall(0, 1.62, 0, 0.07, stoneDark, g);
      colCircle(x, z, 0.42);
      return g;
    }
    [[19.6, 26], [26.4, 26], [19.6, 17.5], [26.4, 17.5],
     [19.6, 34], [26.4, 34], [19.6, 9.5], [26.4, 9.5]].forEach(([x, z]) => makeStoneLantern72(x, z)); // v8: thêm 2 cặp -> hai hàng đèn đá dọc lối chính như ảnh tham chiếu
    // v7.2 — DỪA CAO cạnh chánh điện + sau tượng (cọ cũ chỉ cao 4,4 — mẫu/ref3 dừa vút cao)
    function makeTallPalm72(x, z, h, lean) {
      const g = new THREE.Group(); g.position.set(x, 0, z); g.rotation.z = lean || 0; grounds.add(g);
      addCyl(0, h / 2, 0, 0.15, h, mat(0x6B4226, 0.9), g);
      for (let k = 0; k < 8; k++) {
        const a = (k / 8) * Math.PI * 2;
        const leaf = addBox(Math.cos(a) * 1.5, h + 0.5, Math.sin(a) * 1.5, 0.42, 3.1, 0.15, mat(0x3E6B34, 0.85), g);
        leaf.rotation.z = Math.cos(a) * 1.05; leaf.rotation.x = -Math.sin(a) * 1.05;
      }
      addBall(0.25, h - 0.25, 0.15, 0.17, mat(0x5C8446, 0.8), g);
      addBall(-0.22, h - 0.3, -0.1, 0.15, mat(0x5C8446, 0.8), g);
      colCircle(x, z, 0.45);
      return g;
    }
    makeTallPalm72(-8.5, 31.5, 8.2, 0.04);
    makeTallPalm72(33, -5.5, 7.6, -0.05);
    makeTallPalm72(-3.5, 34.5, 7.2, 0.02);
    // v7.2 — DÂY CỜ PHẬT GIÁO giăng ngang lối chính (cờ sọc 5 màu, dây võng)
    function makeFlagString72(x0, z0, x1, z1, h, sag) {
      const N = 11;
      const pts = [];
      for (let i = 0; i <= N; i++) {
        const t = i / N;
        pts.push(new THREE.Vector3(x0 + (x1 - x0) * t, h - Math.sin(t * Math.PI) * sag, z0 + (z1 - z0) * t));
      }
      const line = new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts),
        new THREE.LineBasicMaterial({ color: 0x5A3D26 }));
      grounds.add(line);
      const yaw = Math.atan2(x1 - x0, z1 - z0);
      for (let i = 0; i < N; i++) {
        const mid = pts[i].clone().add(pts[i + 1]).multiplyScalar(0.5);
        const flag = new THREE.Mesh(new THREE.PlaneGeometry(0.85, 0.55), flagMat72); // v7.3: cờ to hơn — bản 0,62×0,42 mất hút ở cỡ ảnh sân
        flag.position.copy(mid); flag.position.y -= 0.3;
        flag.rotation.y = yaw + Math.PI / 2;
        grounds.add(flag);
      }
      addCyl(x0, h / 2, z0, 0.055, h, mat(0x5A3D26, 0.85), grounds);
      addCyl(x1, h / 2, z1, 0.055, h, mat(0x5A3D26, 0.85), grounds);
    }
    makeFlagString72(16.2, 33, 29.8, 33, 7.0, 0.6); // v7.3b: nâng dây cờ lên 7,0 (sag 0,6) — ở 4,8 dây z=21 treo đúng tầm biển "CHÙA VĨNH TRÀNG" (băng y3,75–5,8), ảnh sân chụp thật cho thấy cờ che mất chữ; đường ngắm từ sân (cam y~2) qua đáy cờ ~6,1 tại z=21 tới biển đạt y~8,9 > đỉnh biển -> hết che (đo hình học trong BAO_CAO_V73)
    makeFlagString72(16.2, 21, 29.8, 21, 7.0, 0.6);
    // Đèn lồng GIẤY ấm (v7.2: hết khối hồng — cầu giấy dẹt, nắp đỏ, phát sáng ấm)
    // v7.3c: BỎ 2 cột giữa (i=3 x=22/z=30, i=4 x=24/z=34) — ảnh sân V7.3 chụp
    // thật: cầu trắng của 2 cột này chiếu đúng vào băng biển, che chữ "ÙA"/"NG"
    // của "CHÙA VĨNH TRÀNG". Hành lang trục giữa phải trống như ảnh mẫu.
    for (let i = 0; i < 8; i++) {
      if (i === 3 || i === 4) continue;
      const x = 16 + i * 2, z = 34 - (i % 2) * 4;
      const pole = addCyl(x, 2.2, z, 0.1, 4.4, mat(0x5A3D26, 0.8), grounds);
      const lamp = addBall(x, 3.6, z, 0.36, mat(0xF7C8D3, 0.35, 0, 1, 0.85), grounds);
      lamp.scale.set(1, 0.82, 1);
      addCyl(x, 3.92, z, 0.13, 0.07, mat(0xA03A2A, 0.6), grounds).castShadow = false;
      addCyl(x, 3.28, z, 0.13, 0.07, mat(0xA03A2A, 0.6), grounds).castShadow = false;
    }

    // Lư hương chính S2 (23, 11) + 2 lư nhỏ
    const burnerMain = new THREE.Group(); burnerMain.position.set(23, 0, 11); burnerMain.scale.setScalar(1.35); grounds.add(burnerMain);
    addCyl(0, 0.5, 0, 0.9, 1.0, mat(0x8C5E32, 0.35, 0.8), burnerMain);
    addCyl(0, 1.05, 0, 1.05, 0.25, mat(0x8C5E32, 0.35, 0.8), burnerMain);
    addCyl(0, 1.15, 0, 0.8, 0.12, mat(0xB8B0A0, 0.9), burnerMain); // lớp tro sáng
    addCyl(0, 1.2, 0, 1.08, 0.08, fenceGoldMat, burnerMain); // vành vàng
    const burnerSticks = new THREE.Group(); burnerSticks.position.set(0, 1.2, 0); burnerSticks.visible = false;
    for (let i = -1; i <= 1; i++) {
      const st = addCyl(i * 0.14, 0.5, 0, 0.02, 1.0, mat(0xE63946, 0.6), burnerSticks);
      st.rotation.z = i * 0.08;
      addBall(i * 0.14, 1.02, 0, 0.035, mat(0xFFAA00, 0.2, 0, 1, 2.0), burnerSticks);
    }
    burnerMain.add(burnerSticks);
    colCircle(23, 11, 1.8);
    // Đèn dầu cạnh lư (châm nhang từ đèn dầu — vật tương tác màu vàng đồng)
    const oilLamp = new THREE.Group(); oilLamp.position.set(24.7, 0, 12.1); grounds.add(oilLamp);
    addCyl(0, 0.45, 0, 0.09, 0.9, fenceGoldMat, oilLamp);
    addCyl(0, 0.95, 0, 0.3, 0.1, fenceGoldMat, oilLamp);
    const lampGlass = addBall(0, 1.2, 0, 0.17, mat(0xFFD9A0, 0.2, 0, 1, 0.7), oilLamp); lampGlass.scale.set(1, 1.25, 1);
    const lampFlame = addBall(0, 1.22, 0, 0.07, mat(0xFFAA00, 0.1, 0, 1, 2.2), oilLamp);
    colCircle(24.7, 12.1, 0.45);
    function makeSmallBurner(x, z) {
      const b = new THREE.Group(); b.position.set(x, 0, z); grounds.add(b);
      addCyl(0, 0.4, 0, 0.45, 0.8, mat(0x8C5E32, 0.35, 0.8), b);
      addCyl(0, 0.85, 0, 0.55, 0.15, mat(0x8C5E32, 0.35, 0.8), b);
      const sticks = new THREE.Group(); sticks.position.set(0, 0.9, 0); sticks.visible = false;
      for (let i = -1; i <= 1; i++) addCyl(i * 0.1, 0.35, 0, 0.015, 0.7, mat(0xE63946, 0.6), sticks);
      b.add(sticks);
      colCircle(x, z, 0.8);
      return { group: b, sticks };
    }
    const burnerDiLac = makeSmallBurner(-24, 2.2); // ngay trước bệ Di Lặc (v4 đặt lạc ra z=16.3)
    const burnerAdida = makeSmallBurner(-12.4, 22.4); // v7.2: dời ra trước bệ tượng đã phóng 1.29 (tránh lẹm vào bệ)

    // --- Lá rụng + sỏi rải sân (phá mặt sân trống) ---
    const scatterSpots = [];
    let seed = 7;
    const rnd = () => { seed = (seed * 16807) % 2147483647; return seed / 2147483647; };
    for (let i = 0; i < 90; i++) {
      const x = -36 + rnd() * 88, z = -40 + rnd() * 88;
      if (Math.abs(x - 23) < 5.5 && z > -2 && z < 42) continue; // chừa đường chính
      if (x > -5 && x < 15 && z > 8 && z < 24) continue; // chừa hồ trái
      if (x > 31 && x < 51 && z > 8 && z < 24) continue; // chừa hồ phải
      scatterSpots.push([x, z, rnd()]);
    }
    scatterSpots.forEach(([x, z, r], i) => {
      if (i % 3 === 0) {
        const peb = addBall(x, 0.06, z, 0.09 + r * 0.06, mat(0x8A7A63, 0.95), grounds);
        peb.scale.set(1, 0.5, 1); peb.castShadow = false;
      } else {
        const lf = new THREE.Mesh(new THREE.PlaneGeometry(0.16, 0.22),
          new THREE.MeshBasicMaterial({ color: i % 2 ? 0x7A9B4E : 0xC9962E, side: THREE.DoubleSide, transparent: true, opacity: 0.85 }));
        lf.rotation.x = -Math.PI / 2; lf.rotation.z = r * 6.28;
        lf.position.set(x, 0.03, z); lf.receiveShadow = false;
        grounds.add(lf);
      }
    });

    // --- Biển nội quy ở cổng + biển chỉ đường ---
    const rules = plaque(['NỘI QUY', 'Giữ im lặng · Ăn mặc kín đáo', 'Không quay phim trong điện'], 4.6, 1.6, { w: 512, h: 192, bg: '#5A3D26', fg: '#FFF6E5', font: 'bold 36px Georgia, serif' });
    rules.position.set(15.3, 1.6, 42.5); rules.rotation.y = 0.15; grounds.add(rules);
    addBox(15.3, 0.8, 42.5, 0.15, 1.6, 0.15, woodSignMat, grounds);
    const dir1 = plaque(['→ CHÁNH ĐIỆN'], 2.6, 0.7, { w: 384, h: 96, bg: '#1C5A34', fg: '#FFF6E5', font: 'bold 44px Georgia, serif' });
    dir1.position.set(19, 1.8, 32); dir1.rotation.y = -0.4; grounds.add(dir1);
    const dir2 = plaque(['← DI LẶC · THÁP'], 2.8, 0.7, { w: 384, h: 96, bg: '#1C5A34', fg: '#FFF6E5', font: 'bold 40px Georgia, serif' });
    dir2.position.set(12, 1.8, 8); dir2.rotation.y = 0.5; grounds.add(dir2);

    // --- Sạp nhang + hoa NGOÀI cổng (khu tiền sảnh, phía đông cổng Phương Tiện) — MUA, không miễn phí ---
    const stall = new THREE.Group(); stall.position.set(34, 0, 47); stall.rotation.y = -0.45; grounds.add(stall);
    addBox(0, 1.0, 0, 4.6, 0.3, 2.4, woodSignMat, stall);
    addBox(-2.1, 0.5, 0, 0.2, 1.0, 2.4, woodSignMat, stall);
    addBox(2.1, 0.5, 0, 0.2, 1.0, 2.4, woodSignMat, stall);
    const stallRoof = addBox(0, 2.6, 0, 5.4, 0.25, 3.2, roofMat, stall); stallRoof.rotation.x = 0.12;
    for (let i = 0; i < 8; i++) addCyl(-1.2 + i * 0.12, 1.5, -0.4, 0.015, 0.9, mat(0xE63946, 0.6), stall); // bó nhang
    addBall(1.2, 1.25, 0.3, 0.35, flowerPinkMat, stall);
    addBall(0.6, 1.25, 0.5, 0.3, flowerRedMat, stall);
    const stallSign = plaque(['SẠP NHANG · HOA', 'Nhang thơm · hoa tươi'], 2.6, 1.0, { w: 512, h: 192, bg: '#1C5A34', fg: '#FFF6E5', font: 'bold 52px Georgia, serif' });
    stallSign.position.set(0, 2.0, 1.05); stall.add(stallSign);
    colRect(34 - 2.3, 47 - 1.4, 34 + 2.3, 47 + 1.4);

    // --- Phòng kinh sách (gần giảng đường, phía sau — điểm dừng riêng, tách quầy lưu niệm) ---
    const bookRoom = new THREE.Group(); bookRoom.position.set(42, 0, -10.5); grounds.add(bookRoom); // v7.3c: dời từ (33,-12) — vị trí cũ NẰM TRONG rect va chạm chánh điện (9..37, -13..1.2) nên không đường đi nào tới được điểm đứng (33,-8.4); vị trí mới sau điện, cạnh Giảng đường, đúng nghiên cứu "phòng kinh sách ở phía sau gần chánh điện"
    addBox(0, 1.0, 0, 4.8, 0.3, 2.2, woodSignMat, bookRoom);
    addBox(-2.2, 0.5, 0, 0.2, 1.0, 2.2, woodSignMat, bookRoom);
    addBox(2.2, 0.5, 0, 0.2, 1.0, 2.2, woodSignMat, bookRoom);
    const brRoof = addBox(0, 2.7, 0, 5.6, 0.25, 3.0, roofMat, bookRoom); brRoof.rotation.x = 0.12;
    [[-1.5, 0x8E2323], [-0.5, 0x1C5A34], [0.5, 0xC9962E], [1.5, 0x5A3D26]].forEach(([bx, bc]) => {
      addBox(bx, 1.35, 0, 0.7, 0.4, 1.1, mat(bc, 0.6), bookRoom); // chồng kinh sách bìa màu
    });
    const brSign = plaque(['PHÒNG KINH SÁCH', 'Thỉnh kinh · gieo duyên'], 3.0, 1.0, { w: 512, h: 192, bg: '#1C5A34', fg: '#FFF6E5', font: 'bold 48px Georgia, serif' });
    brSign.position.set(0, 2.05, 1.05); bookRoom.add(brSign);
    colRect(42 - 2.4, -10.5 - 1.3, 42 + 2.4, -10.5 + 1.3); // v7.3c: theo vị trí bookRoom mới (42,-10.5)

    // --- Quầy lưu niệm S7 (gần cổng 2) — v7.2: dựng lại theo image-48 (mái cong, biển gỗ, đèn giấy) ---
    const shopKiosk = new THREE.Group(); shopKiosk.position.set(40, 0, 38); grounds.add(shopKiosk);
    const woodLight72 = mat(0x8A5A33, 0.7);
    [[-3.2, -2.2], [3.2, -2.2], [-3.2, 2.2], [3.2, 2.2]].forEach(([px, pz]) => addBox(px, 1.9, pz, 0.28, 3.8, 0.28, woodSignMat, shopKiosk)); // 4 cột gỗ
    addBox(0, 1.9, -2.3, 7, 3.8, 0.22, woodLight72, shopKiosk); // vách sau
    addBox(-3.4, 1.9, 0, 0.22, 3.8, 4.6, woodLight72, shopKiosk); // vách hông trái
    addBox(3.4, 1.9, 0, 0.22, 3.8, 4.6, woodLight72, shopKiosk); // vách hông phải
    addBox(0, 0.95, 2.0, 6.8, 1.1, 0.5, woodSignMat, shopKiosk); // quầy trước
    addBox(0, 1.55, 2.0, 7.0, 0.14, 0.7, woodLight72, shopKiosk); // mặt quầy
    [1.9, 2.6].forEach(sy => { // kệ + hàng lưu niệm (hộp quà màu)
      addBox(0, sy, -1.9, 6.2, 0.1, 0.7, woodSignMat, shopKiosk);
      for (let gi = 0; gi < 5; gi++) addBox(-2.4 + gi * 1.2, sy + 0.28, -1.9, 0.55, 0.45, 0.5, mat([0xC93B6E, 0xC9962E, 0x3F7D5D, 0xA03A2A, 0xE8E2D4][gi], 0.55), shopKiosk);
    });
    const shopBuddha = addBall(0, 2.35, -1.85, 0.3, mat(0xEFE9DD, 0.4), shopKiosk); shopBuddha.scale.set(1, 1.35, 0.8); // tượng nhỏ trên kệ
    for (let k = -2; k <= 2; k++) { // mái cong 5 phiến ngói (faceted curve như image-48)
      const slab72 = addBox(0, 4.42 - k * k * 0.13, k * 1.28, 8.2, 0.16, 1.55, roofMat, shopKiosk);
      slab72.rotation.x = k * 0.21;
    }
    addBox(0, 4.5, 0, 8.3, 0.22, 0.4, woodSignMat, shopKiosk); // sống mái
    const shopSign = plaque(['CỬA HÀNG', 'LƯU NIỆM'], 4.5, 1.4, { w: 512, h: 192, bg: '#5A3D26', fg: '#FFD166', font: 'bold 60px Georgia, serif' });
    shopSign.position.set(0, 3.15, 2.42); shopKiosk.add(shopSign);
    [-2.9, 2.9].forEach(lx => { // đèn giấy treo hai góc quầy
      const ll = addBall(lx, 3.35, 2.35, 0.27, mat(0xF7C8D3, 0.35, 0, 1, 0.9), shopKiosk); ll.scale.set(1, 0.85, 1); ll.castShadow = false;
    });
    colRect(40 - 3.5, 38 - 2.5, 40 + 3.5, 38 + 2.5);

    // --- Thùng công đức (27.9, 4.9) ---
    const meritBox = new THREE.Group(); meritBox.position.set(27.9, 0, 4.9); grounds.add(meritBox);
    addBox(0, 0.6, 0, 0.72, 1.2, 0.62, woodSignMat, meritBox);
    addBox(0, 1.25, 0, 0.8, 0.12, 0.7, fenceGoldMat, meritBox);
    addBox(0, 1.32, 0, 0.3, 0.04, 0.1, stoneDark, meritBox);
    const meritSign = plaque(['TÙY TÂM', 'CÔNG ĐỨC'], 0.9, 0.6, { w: 256, h: 160, bg: '#5A3D26', fg: '#FFD166', font: 'bold 40px Georgia, serif' });
    meritSign.position.set(0, 0.6, 0.36); meritBox.add(meritSign);
    colCircle(27.9, 4.9, 0.8);

    // --- Dép bỏ ở thềm (xuất hiện sau nhịp bỏ dép) ---
    const shoePairs = new THREE.Group(); shoePairs.position.set(0, 0, 0); shoePairs.visible = false; grounds.add(shoePairs);
    [[20.5, 5.6], [25.5, 5.6]].forEach(([x, z]) => {
      addBox(x, 0.05, z, 0.28, 0.08, 0.7, mat(0x2B2320, 0.8), shoePairs);
      addBox(x + 0.35, 0.05, z, 0.28, 0.08, 0.7, mat(0x2B2320, 0.8), shoePairs);
    });

    // v8 — BỒ ĐOÀN sân (ảnh tham chiếu: người quỳ lễ hai bên lư hương): đĩa
    // trụ đỏ sẫm viền vàng; 2 cái có khách quỳ (avatar ở module_5, cùng tọa
    // độ), 2 cái trống hai bên; thêm 1 trước Di Lặc. Collider nhỏ r 0,45 —
    // đã đo không chạm điểm đứng trạm lư (25,3; 13,7) và các via tuyến.
    const cushionMat8 = mat(0x7A1F1F, 0.75);
    function makeCushion8(x, z) {
      const g = new THREE.Group(); g.position.set(x, 0, z); grounds.add(g);
      addCyl(0, 0.09, 0, 0.55, 0.18, cushionMat8, g);
      addCyl(0, 0.20, 0, 0.47, 0.05, mat(0x9D0208, 0.7), g);
      addCyl(0, 0.02, 0, 0.58, 0.04, fenceGoldMat, g);
      colCircle(x, z, 0.45);
      return g;
    }
    makeCushion8(20.4, 15.6); makeCushion8(24.8, 14.8);
    // ^ Vị trí tây (20,4; 15,6): bản đầu (21,2; 14,8) bị dời vì đường chéo
    // (23,16)->(15,8) của tuyến books (verify tailB) đi qua cách tâm nó
    // 0,42m — kẹp giữa bồ đoàn và lư sân (r 1,8) gây FF-TIMEOUT hop books
    // 15,8 ở lượt tailB đầu. Vị trí mới hở 1,56m với tuyến đó.
    makeCushion8(19.8, 15.2);
    // Bồ đoàn trống thứ 4 đặt ở (28,5; 12,5) phía đông-nam lư — vị trí đầu
    // tiên dự kiến (26,2; 15,2) bị LOẠI vì đường thẳng lư -> quầy lưu niệm
    // (tuyến verify tailB) đi qua cách tâm nó 0,04m: avatar đâm trực diện
    // collider tròn và kẹt (FF-TIMEOUT hop shop 30,22 đo được ở lượt tailB
    // đầu). Vị trí mới hở 3,4m với tuyến đó và với điểm đứng trạm lư.
    makeCushion8(28.5, 12.5);
    makeCushion8(-24, 4.2);

    // v8 — NÚI MỜ sau chùa (phông xa của ảnh tham chiếu: núi + sương sớm).
    // Khối nón thấp màu xanh sương nhạt; FogExp2 của cảnh tự làm mềm thêm.
    [[-45, -108, 34, 26], [0, -118, 42, 32], [48, -110, 36, 27], [-85, -96, 30, 21], [88, -100, 32, 23]].forEach(([mx, mz, mr, mh]) => {
      const mt = new THREE.Mesh(new THREE.ConeGeometry(mr, mh, 7), new THREE.MeshStandardMaterial({ color: 0xA8C4E4, roughness: 1, flatShading: true }));
      mt.position.set(mx, mh / 2 - 0.5, mz); mt.castShadow = false; mt.receiveShadow = false;
      grounds.add(mt);
    });

    // v8 — CÂY HOA ĐÀO/HỒNG cạnh hai hồ (ảnh tham chiếu: cây hoa hồng bên hồ
    // sen): thân nâu + 3 tán cầu phủ hoa hồng hai tông của theme.
    function makeBlossom8(x, z, s) {
      const g = new THREE.Group(); g.position.set(x, 0, z); grounds.add(g);
      addCyl(0, 1.5 * s, 0, 0.16 * s, 3.0 * s, mat(0x5A3D26, 0.9), g);
      const c1 = addBall(0, 3.6 * s, 0, 1.5 * s, mat(0xEE7FAE, 0.65), g); c1.scale.set(1.2, 0.75, 1.2);
      const c2 = addBall(0.9 * s, 4.3 * s, 0.3 * s, 1.0 * s, mat(0xF2A0C4, 0.65), g); c2.scale.set(1.15, 0.7, 1.15);
      const c3 = addBall(-0.9 * s, 4.1 * s, -0.3 * s, 0.9 * s, mat(0xE86A9C, 0.65), g); c3.scale.set(1.1, 0.7, 1.1);
      colCircle(x, z, 0.5 * s);
      return g;
    }
    makeBlossom8(-2, 24.5, 1.0);
    makeBlossom8(34, 27, 1.1);

    // --- Ghế đá nghỉ chân (v6: khách ngồi nghỉ — hành vi lễ tĩnh) ---
    // BENCH_SEATS được module_5 dùng để đặt khách ngồi: [x, z, yaw mặt hướng]
    const BENCH_SEATS = [[-9, 20, -0.56], [30, 25.5, 2.28]];
    BENCH_SEATS.forEach(([bx, bz, byaw]) => {
      const bg = new THREE.Group(); bg.position.set(bx, 0, bz); bg.rotation.y = byaw; grounds.add(bg);
      addBox(0, 0.48, 0, 1.9, 0.16, 0.55, stoneDark, bg);
      addBox(-0.7, 0.2, 0, 0.28, 0.4, 0.45, stoneDark, bg);
      addBox(0.7, 0.2, 0, 0.28, 0.4, 0.45, stoneDark, bg);
      colRect(bx - 1.0, bz - 0.45, bx + 1.0, bz + 0.45);
    });
