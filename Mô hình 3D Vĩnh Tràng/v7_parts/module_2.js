
    // ---- 3. KHUÔN VIÊN CHÙA VĨNH TRÀNG (procedural, theo bố cục layout_v10_v8 + ref9) ----
    // Tọa độ Three.js: x = Blender x, z = -Blender y (đã đối chiếu probe_v4)
    const grounds = new THREE.Group();
    scene.add(grounds);
    const colRects = [], colCircles = [];
    function colRect(x0, z0, x1, z1) { colRects.push([x0, z0, x1, z1]); }
    function colCircle(x, z, r) { colCircles.push([x, z, r]); }
    const fishes = [];

    const stoneMat = mat(0xDFD6C7, 0.82);
    const stoneDark = mat(0x9E9385, 0.88);
    const fenceGoldMat = mat(0xE0A832, 0.45, 0.35);
    const woodSignMat = mat(0x6E4426, 0.65);
    const roofMat = new THREE.MeshStandardMaterial({ map: roofTex, roughness: 0.65 });
    roofTex.repeat.set(3, 2);
    const wallGoldMat = mat(0xF2C357, 0.55); // Vàng chùa Vĩnh Tràng tươi sáng
    const pillarRedMat = mat(0xBA3524, 0.38, 0.08); // Đỏ son bóng mịn
    const grilleMat = mat(0x3D2E26, 0.5, 0.3);
    const waterMat = new THREE.MeshStandardMaterial({ color: 0x328A80, roughness: 0.08, metalness: 0.42, transparent: true, opacity: 0.85 });
    const flowerPinkMat = mat(0xFF4388, 0.45); // Hoa giấy hồng rực rỡ
    const flowerRedMat = mat(0xE63946, 0.45);
    const statueMat = mat(0xFAF6EE, 0.38, 0.06); // Đá cẩm thạch trắng ngà ấm trang nghiêm

    // --- Nền đất ngoài rào + sân lát gạch trong khuôn viên ---
    const outerGround = new THREE.Mesh(new THREE.PlaneGeometry(260, 260),
      new THREE.MeshStandardMaterial({ color: 0x6FA83B, roughness: 0.95 }));
    outerGround.rotation.x = -Math.PI / 2; outerGround.position.set(7, -0.05, 0);
    outerGround.receiveShadow = true; grounds.add(outerGround);
    const slab = new THREE.Mesh(new THREE.PlaneGeometry(93, 95),
      new THREE.MeshStandardMaterial({ map: pavingTex, roughness: 0.85 }));
    pavingTex.repeat.set(24, 24);
    slab.rotation.x = -Math.PI / 2; slab.position.set(7.7, 0, 5.5);
    slab.receiveShadow = true; grounds.add(slab);
    // Đường chính từ cổng vào chánh điện
    const road = new THREE.Mesh(new THREE.PlaneGeometry(9, 43),
      new THREE.MeshStandardMaterial({ color: 0xD8CFBF, roughness: 0.85 }));
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
      // Lan can vàng quanh hồ
      for (let i = -9; i <= 9; i += 3) {
        addCyl(i, 0.75, -7.5, 0.05, 0.6, fenceGoldMat, g);
        addCyl(i, 0.75, 7.5, 0.05, 0.6, fenceGoldMat, g);
      }
      addBox(0, 1.0, -7.5, 19.9, 0.06, 0.06, fenceGoldMat, g);
      addBox(0, 1.0, 7.5, 19.9, 0.06, 0.06, fenceGoldMat, g);
      // Hoa sen + cá lượn dưới mặt nước
      for (let i = 0; i < 5; i++) {
        const lx = -7 + i * 3.5, lz = -4 + (i % 2) * 7;
        const leaf = addBall(lx, 0.18, lz, 0.55, mat(0x3E6B34, 0.8), g); leaf.scale.set(1, 0.18, 1);
        addBall(lx + 0.3, 0.35, lz, 0.28, flowerPinkMat, g);
      }
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
    // 13 vòm cửa (cửa giữa i=6 mở rộng hiển lộ bàn thờ Tam Bảo) + cột đỏ giữa các vòm
    for (let i = 0; i < 13; i++) {
      const x = -12 + i * 2;
      const archTrim = new THREE.Mesh(new THREE.TorusGeometry(0.85, 0.12, 8, 16, Math.PI), wallGoldMat);
      archTrim.position.set(x, 2.4, 5.12); archTrim.castShadow = true; hall.add(archTrim);
      if (i !== 6) {
        // Cửa phụ: nền tối sau vòm
        const dark = addBox(x, 1.6, 5.06, 1.5, 3.2, 0.1, mat(0x1E1410, 0.9), hall);
        dark.castShadow = false;
        // Song sắt vàng trước vòm (lattice)
        for (let j = 0; j < 3; j++) addBox(x - 0.5 + j * 0.5, 1.6, 5.3, 0.05, 3.2, 0.05, fenceGoldMat, hall);
      }
      // Cột Corinthian/Romanesque vàng đất nung thạch cao theo ảnh tham khảo
      const colGoldMat = mat(0xDCA74A, 0.45);
      const colPlasterMat = mat(0xF6F0DC, 0.5);
      if (i < 12) {
        addBox(x + 1, 0.35, 5.15, 0.52, 0.7, 0.52, colPlasterMat, hall);
        addCyl(x + 1, 2.3, 5.15, 0.20, 3.2, colGoldMat, hall);
        addBox(x + 1, 4.05, 5.15, 0.52, 0.35, 0.52, colPlasterMat, hall);
      }
    }
    const colGoldMat = mat(0xDCA74A, 0.45);
    const colPlasterMat = mat(0xF6F0DC, 0.5);
    addBox(-13, 0.35, 5.15, 0.52, 0.7, 0.52, colPlasterMat, hall);
    addCyl(-13, 2.3, 5.15, 0.20, 3.2, colGoldMat, hall);
    addBox(-13, 4.05, 5.15, 0.52, 0.35, 0.52, colPlasterMat, hall);
    addBox(13, 0.35, 5.15, 0.52, 0.7, 0.52, colPlasterMat, hall);
    addCyl(13, 2.3, 5.15, 0.20, 3.2, colGoldMat, hall);
    addBox(13, 4.05, 5.15, 0.52, 0.35, 0.52, colPlasterMat, hall);

    // Lan can phù điêu thạch cao chạy dọc bờ mái Chánh điện
    addBox(0, 5.5, 5.1, 28.4, 0.75, 0.3, colPlasterMat, hall);
    for (let bx = -13.2; bx <= 13.2; bx += 0.88) {
      addCyl(bx, 5.5, 5.18, 0.08, 0.55, colPlasterMat, hall);
    }
    for (let px = -13.2; px <= 13.2; px += 2.64) {
      addBall(px, 6.0, 5.18, 0.16, fenceGoldMat, hall);
    }

    // Bàn thờ & Tượng Phật thếp vàng hiển lộ bên trong cửa vòm chính (i=6)
    const altar = new THREE.Group(); altar.position.set(0, 0.4, 2.8); hall.add(altar);
    addBox(0, 0.6, 0, 3.2, 1.2, 1.6, mat(0x5c1d18, 0.4), altar);
    addBox(0, 1.22, 0, 3.4, 0.08, 1.8, fenceGoldMat, altar);
    const altarLotus = addBall(0, 1.45, 0, 0.9, mat(0x1F6B4F, 0.45), altar); altarLotus.scale.set(1, 0.35, 1);
    for (let k = 0; k < 8; k++) {
      const a = (k / 8) * Math.PI * 2;
      const p = addBall(Math.cos(a) * 0.8, 1.45, Math.sin(a) * 0.8, 0.22, flowerPinkMat, altar);
      p.scale.set(1, 0.4, 0.6);
    }
    const altBuddhaBody = addBall(0, 2.15, 0, 0.6, mat(0xffd166, 0.22, 0.85, 1, 0.35), altar);
    altBuddhaBody.scale.set(0.95, 1.35, 0.7);
    addBall(0, 2.95, 0, 0.32, mat(0xffd166, 0.22, 0.85, 1, 0.35), altar);
    addCyl(0, 3.22, 0, 0.1, 0.22, mat(0xffd166, 0.22, 0.85, 1, 0.35), altar);
    const altHalo = addBall(0, 2.7, -0.25, 0.75, mat(0xffe066, 0.1, 0, 1, 2.0), altar);
    altHalo.scale.set(1.2, 1.2, 0.1);
    [[-1.1, 0.4], [1.1, 0.4]].forEach(([cx, cz]) => {
      addCyl(cx, 1.4, cz, 0.06, 0.32, fenceGoldMat, altar);
      addBall(cx, 1.6, cz, 0.045, mat(0xffaa00, 0.1, 0, 1, 2.5), altar);
    });
    const altarLight = new THREE.PointLight(0xffe29a, 2.8, 12);
    altarLight.position.set(0, 2.4, 2.5); hall.add(altarLight);

    // Tầng trán pediment & tháp Angkor trang trí nóc Chánh điện
    const pediment = new THREE.Group(); pediment.position.set(0, 5.4, 4.8); hall.add(pediment);
    addBox(0, 1.2, 0, 10.4, 2.4, 0.6, colPlasterMat, pediment);
    addBox(0, 2.5, 0, 9.8, 0.25, 0.8, wallGoldMat, pediment);
    addBox(0, 3.4, 0, 5.4, 1.6, 0.7, colPlasterMat, pediment);
    addBox(0, 4.3, 0, 3.2, 1.0, 0.8, wallGoldMat, pediment);
    addCyl(0, 5.4, 0, 0.22, 1.4, fenceGoldMat, pediment);
    addBall(0, 6.2, 0, 0.26, fenceGoldMat, pediment);
    const hallSign = plaque(['CHÙA VĨNH TRÀNG', '永長寺'], 3.6, 1.0, { w: 512, h: 160, bg: '#1C5A34', fg: '#FFD166', font: 'bold 44px Georgia, serif' });
    hallSign.position.set(0, 1.1, 0.35); pediment.add(hallSign);
    [-9.5, 9.5].forEach(tx => {
      addBox(tx, 1.5, 0, 3.2, 2.4, 0.6, colPlasterMat, pediment);
      addBox(tx, 2.8, 0, 2.6, 0.8, 0.7, wallGoldMat, pediment);
      addCyl(tx, 3.7, 0, 0.18, 1.0, fenceGoldMat, pediment);
      addBall(tx, 4.3, 0, 0.22, fenceGoldMat, pediment);
    });

    // Mái 2 tầng cong + rêu
    const roof1 = addBox(0, 6.2, 0, 31, 0.7, 13, roofMat, hall); roof1.rotation.x = 0.18;
    const roof2 = addBox(0, 8.6, 0, 26, 0.6, 11, roofMat, hall); roof2.rotation.x = 0.18;
    addBox(0, 9.4, 0, 26.5, 0.5, 0.5, fenceGoldMat, hall); // sống mái
    [[-13, 1.2, 2.8], [-10, 1.8, 3.6], [-7.5, 1.0, 3.0], [-4, 1.5, 4.0], [-1, 2.0, 3.2],
     [2.5, 1.1, 3.8], [6, 1.6, 2.9], [9.5, 1.3, 3.5], [12.5, 1.0, 3.1]].forEach(([mx, mw, mz]) => {
      const moss = addBox(mx, 6.55, mz, mw, 0.08, 2.6, mat(0x55663A, 0.95), hall);
      moss.rotation.x = 0.18; moss.castShadow = false;
    });

    // Bậc thềm tam cấp 7 bậc + Lan can uốn lượn màu vàng
    for (let i = 0; i < 7; i++) {
      addBox(0, 0.12 + i * 0.14, 5.2 + i * 0.52, 9.6, 0.26, 0.58, stoneMat, hall);
    }
    [-5.1, 5.1].forEach(lx => {
      for (let k = 0; k < 6; k++) {
        const bz = 5.3 + k * 0.52, by = 0.55 + k * 0.14;
        addCyl(lx, by, bz, 0.08, 0.7, wallGoldMat, hall);
      }
      const rail = addBox(lx, 1.05, 6.6, 0.22, 0.16, 3.4, wallGoldMat, hall);
      rail.rotation.x = 0.26;
      addBox(lx, 0.55, 8.4, 0.45, 1.1, 0.45, wallGoldMat, hall);
      addBall(lx, 1.25, 8.4, 0.22, fenceGoldMat, hall);
    });
    colRect(23 - 14, -1 - 12, 23 + 14, -1 + 2.2);

    // --- Tượng A Di Đà trắng, đài sen xanh (S1) ---
    function makeStandingBuddha(x, z, plaqueLines) {
      const g = new THREE.Group(); g.position.set(x, 0, z); grounds.add(g);
      addCyl(0, 0.35, 0, 2.2, 0.7, mat(0x8A4A3A, 0.8), g); // bệ đỏ nâu
      const lotus = addBall(0, 0.9, 0, 1.7, mat(0x1F6B4F, 0.45), g); lotus.scale.set(1, 0.45, 1); // đài sen xanh
      for (let i = 0; i < 10; i++) {
        const a = (i / 10) * Math.PI * 2;
        const petal = addBall(Math.cos(a) * 1.55, 0.85, Math.sin(a) * 1.55, 0.4, flowerPinkMat, g);
        petal.scale.set(1, 0.5, 0.6); petal.rotation.y = -a;
      }
      const body = addBall(0, 2.6, 0, 0.95, statueMat, g); body.scale.set(1, 1.7, 0.75);
      addBall(0, 4.5, 0, 0.45, statueMat, g);
      addCyl(0, 4.85, 0, 0.16, 0.3, statueMat, g); // nhục kế
      const sign = plaque(plaqueLines, 3.4, 1.0, { w: 512, h: 160, bg: '#5A3D26', fg: '#FFD166', font: 'bold 44px Georgia, serif' });
      sign.position.set(0, 1.1, 2.35); g.add(sign);
      colCircle(x, z, 3.2);
      return g;
    }
    makeStandingBuddha(-14, 27, ['NAM MÔ A DI ĐÀ PHẬT']);
    // Đài Quan Âm (trạm phụ trong vườn hoa, phía tây — chỉ vái, không thắp nhang)
    const qaGarden = new THREE.Group(); qaGarden.position.set(-27, 0, 21); grounds.add(qaGarden);
    addCyl(0, 0.3, 0, 1.9, 0.6, stoneDark, qaGarden);
    addCyl(0, 0.75, 0, 1.5, 0.3, stoneMat, qaGarden);
    const qaLotus = addBall(0, 1.0, 0, 1.05, mat(0x1F6B4F, 0.45), qaGarden); qaLotus.scale.set(1, 0.4, 1);
    const qaBody = addBall(0, 2.1, 0, 0.55, statueMat, qaGarden); qaBody.scale.set(0.85, 1.6, 0.7);
    addBall(0, 3.35, 0, 0.3, statueMat, qaGarden);
    addCyl(0.42, 1.9, 0.3, 0.05, 0.55, statueMat, qaGarden); // tay cầm bình cam lồ
    addBall(0.42, 2.25, 0.3, 0.11, statueMat, qaGarden);
    const qaSign = plaque(['ĐÀI QUAN ÂM'], 2.6, 0.8, { w: 512, h: 160, bg: '#5A3D26', fg: '#FFD166', font: 'bold 52px Georgia, serif' });
    qaSign.position.set(0, 0.75, 1.75); qaGarden.add(qaSign);
    colCircle(-27, 21, 2.1);
    // Bệ đá + chữ Hán cho Di Lặc (S4)
    const dilac = new THREE.Group(); dilac.position.set(-24.5, 0, -3); grounds.add(dilac);
    addBox(0, 0.6, 0, 8, 1.2, 7, stoneDark, dilac);
    addBox(0, 1.3, 0, 6.5, 0.6, 5.5, stoneMat, dilac);
    const dBody = addBall(0, 3.0, 0, 1.9, statueMat, dilac); dBody.scale.set(1.15, 1.15, 0.9);
    addBall(0, 4.9, 0, 0.75, statueMat, dilac);
    addBall(0, 2.1, 0, 0.9, statueMat, dilac); // bụng tròn
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
    const rBody = addBall(0, 2.5, 0, 1.1, statueMat, recl); rBody.scale.set(3.2, 1.0, 0.9);
    addBall(-3.9, 2.9, 0, 0.55, statueMat, recl);
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
    // --- Hai hàng chậu kiểng đất nung & bonsai / hoa giấy dọc sân Chánh điện (chuẩn 100% ảnh tham khảo) ---
    const potMat = mat(0xA64A28, 0.75); // Đất nung đỏ Nam Bộ
    function makeCourtyardPlanter(x, z, isFlower = false) {
      const g = new THREE.Group(); g.position.set(x, 0, z); grounds.add(g);
      addCyl(0, 0.22, 0, 0.75, 0.44, potMat, g); // đôn tròn
      addCyl(0, 0.55, 0, 0.95, 0.35, potMat, g); // chậu miệng xòe
      addCyl(0, 0.70, 0, 0.88, 0.08, mat(0x3B2518, 0.9), g); // đất
      if (isFlower) {
        // Cây hoa giấy / hoa sứ tán tròn hoa hồng rực rỡ
        addCyl(0, 1.1, 0, 0.12, 0.8, mat(0x5A3D26, 0.9), g);
        const bush = addBall(0, 1.7, 0, 0.95, mat(0x2E6B38, 0.85), g);
        bush.scale.set(1.15, 0.85, 1.15);
        for (let k = 0; k < 14; k++) {
          const a = (k / 14) * Math.PI * 2 + (k % 3);
          const r = 0.55 + (k % 4) * 0.12;
          const fl = addBall(Math.cos(a) * r, 1.6 + Math.sin(k * 2) * 0.35, Math.sin(a) * r, 0.22, flowerPinkMat, g);
          fl.scale.set(1.2, 0.6, 1.2);
        }
      } else {
        // Cây kiểng Bonsai thế cổ Nam Bộ nhiều tầng tán
        const trunk = addCyl(0.08, 1.15, 0, 0.16, 0.9, mat(0x543722, 0.9), g);
        trunk.rotation.z = -0.12;
        const b1 = addBall(-0.25, 1.45, 0.1, 0.65, mat(0x1F5428, 0.85), g); b1.scale.set(1.1, 0.45, 1.0);
        const b2 = addBall(0.35, 1.75, -0.1, 0.58, mat(0x235E2D, 0.85), g); b2.scale.set(1.05, 0.42, 1.05);
        const b3 = addBall(0.05, 2.15, 0, 0.72, mat(0x2A6F35, 0.85), g); b3.scale.set(1.15, 0.5, 1.15);
      }
      colCircle(x, z, 0.95);
      return g;
    }

    // 5 cặp chậu đối xứng hai bên lối đi chính (x = 17.5 và x = 28.5)
    [10.5, 14.5, 18.5, 22.5, 26.5].forEach((z, idx) => {
      makeCourtyardPlanter(17.5, z, idx % 2 === 1);
      makeCourtyardPlanter(28.5, z, idx % 2 === 0);
    });

    // Ghế đá cong nghỉ chân dọc mép hoa viên
    const benchMat = mat(0xD8CFBF, 0.85);
    function makeCourtyardBench(x, z, yaw) {
      const g = new THREE.Group(); g.position.set(x, 0, z); g.rotation.y = yaw; grounds.add(g);
      addBox(0, 0.48, 0, 2.2, 0.14, 0.6, benchMat, g);
      addBox(-0.85, 0.22, 0, 0.28, 0.44, 0.5, stoneDark, g);
      addBox(0.85, 0.22, 0, 0.28, 0.44, 0.5, stoneDark, g);
      addBox(0, 0.85, -0.25, 2.2, 0.65, 0.12, benchMat, g);
      colRect(x - 1.1, z - 0.5, x + 1.1, z + 0.5);
    }
    makeCourtyardBench(14.0, 16.5, 0.15);
    makeCourtyardBench(14.0, 22.5, 0.15);
    makeCourtyardBench(32.0, 22.5, -0.15);

    // Bồn hoa thấp viền vàng ngăn khuôn viên hai bên
    [-1, 1].forEach(side => {
      const bx = 23 + side * 9.6;
      addBox(bx, 0.25, 18.5, 0.45, 0.5, 18.0, wallGoldMat, grounds);
      for (let k = 0; k < 7; k++) {
        const hz = 10.5 + k * 2.6;
        const hedge = addBall(bx + side * 0.9, 0.55, hz, 0.85, mat(0x286334, 0.9), grounds);
        hedge.scale.set(1.2, 0.75, 1.2);
        const hf = addBall(bx + side * 0.8, 0.9, hz, 0.35, flowerPinkMat, grounds);
        hf.scale.set(1.1, 0.5, 1.1);
      }
    });

    // Cành hoa giấy rủ tiền cảnh ở góc trên bên phải khung hình (đúng ảnh mẫu)
    const bougainvilleaCanopy = new THREE.Group();
    bougainvilleaCanopy.position.set(25.8, 3.2, 21.2); grounds.add(bougainvilleaCanopy);
    const cBranch = addCyl(0, 0, 0, 0.08, 2.6, mat(0x5A3D26, 0.9), bougainvilleaCanopy);
    cBranch.rotation.z = 0.85; cBranch.rotation.x = -0.3;
    for (let k = 0; k < 12; k++) {
      const a = (k / 12) * Math.PI * 2;
      const lx = Math.cos(a) * 0.7 + (k * 0.08);
      const ly = -0.3 - (k * 0.06);
      const lz = Math.sin(a) * 0.6;
      const lf = addBall(lx, ly, lz, 0.38, mat(0x2E6B38, 0.85), bougainvilleaCanopy); lf.scale.set(1.1, 0.5, 1.0);
      const fl = addBall(lx + 0.1, ly - 0.15, lz, 0.28, flowerPinkMat, bougainvilleaCanopy); fl.scale.set(1.2, 0.7, 1.2);
    }

    // Lư hương chính S2 trên thềm trước Chánh điện
    const burnerMain = new THREE.Group(); burnerMain.position.set(23, 0.7, 5.4); burnerMain.scale.setScalar(1.2); grounds.add(burnerMain);
    addCyl(0, 0.5, 0, 0.9, 1.0, mat(0x8C5E32, 0.35, 0.8), burnerMain);
    addCyl(0, 1.05, 0, 1.05, 0.25, mat(0x8C5E32, 0.35, 0.8), burnerMain);
    addCyl(0, 1.15, 0, 0.8, 0.12, mat(0xB8B0A0, 0.9), burnerMain);
    addCyl(0, 1.2, 0, 1.08, 0.08, fenceGoldMat, burnerMain);
    const burnerSticks = new THREE.Group(); burnerSticks.position.set(0, 1.2, 0); burnerSticks.visible = false;
    for (let i = -1; i <= 1; i++) {
      const st = addCyl(i * 0.14, 0.5, 0, 0.02, 1.0, mat(0xE63946, 0.6), burnerSticks);
      st.rotation.z = i * 0.08;
      addBall(i * 0.14, 1.02, 0, 0.035, mat(0xFFAA00, 0.2, 0, 1, 2.0), burnerSticks);
    }
    burnerMain.add(burnerSticks);
    colCircle(23, 5.4, 1.2);
    // Đèn dầu cạnh lư
    const oilLamp = new THREE.Group(); oilLamp.position.set(24.5, 0.7, 5.4); grounds.add(oilLamp);
    addCyl(0, 0.45, 0, 0.09, 0.9, fenceGoldMat, oilLamp);
    addCyl(0, 0.95, 0, 0.3, 0.1, fenceGoldMat, oilLamp);
    const lampGlass = addBall(0, 1.2, 0, 0.17, mat(0xFFD9A0, 0.2, 0, 1, 0.7), oilLamp); lampGlass.scale.set(1, 1.25, 1);
    const lampFlame = addBall(0, 1.22, 0, 0.07, mat(0xFFAA00, 0.1, 0, 1, 2.2), oilLamp);
    colCircle(24.5, 5.4, 0.45);
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
    const burnerAdida = makeSmallBurner(-13, 24.2);

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
    const bookRoom = new THREE.Group(); bookRoom.position.set(33, 0, -12); grounds.add(bookRoom);
    addBox(0, 1.0, 0, 4.8, 0.3, 2.2, woodSignMat, bookRoom);
    addBox(-2.2, 0.5, 0, 0.2, 1.0, 2.2, woodSignMat, bookRoom);
    addBox(2.2, 0.5, 0, 0.2, 1.0, 2.2, woodSignMat, bookRoom);
    const brRoof = addBox(0, 2.7, 0, 5.6, 0.25, 3.0, roofMat, bookRoom); brRoof.rotation.x = 0.12;
    [[-1.5, 0x8E2323], [-0.5, 0x1C5A34], [0.5, 0xC9962E], [1.5, 0x5A3D26]].forEach(([bx, bc]) => {
      addBox(bx, 1.35, 0, 0.7, 0.4, 1.1, mat(bc, 0.6), bookRoom); // chồng kinh sách bìa màu
    });
    const brSign = plaque(['PHÒNG KINH SÁCH', 'Thỉnh kinh · gieo duyên'], 3.0, 1.0, { w: 512, h: 192, bg: '#1C5A34', fg: '#FFF6E5', font: 'bold 48px Georgia, serif' });
    brSign.position.set(0, 2.05, 1.05); bookRoom.add(brSign);
    colRect(33 - 2.4, -12 - 1.3, 33 + 2.4, -12 + 1.3);

    // --- Quầy lưu niệm S7 (đặt trong hoa viên bên phải Chánh điện theo ảnh mẫu) ---
    const shopKiosk = new THREE.Group(); shopKiosk.position.set(35, 0, 16); grounds.add(shopKiosk);
    addBox(0, 1.8, 0, 5.4, 3.6, 4.2, woodSignMat, shopKiosk);
    const skRoof = addBox(0, 3.8, 0, 6.2, 0.35, 5.0, roofMat, shopKiosk); skRoof.rotation.x = 0;
    const shopSign = plaque(['CỬA HÀNG', 'LƯU NIỆM'], 3.8, 1.2, { w: 512, h: 256, bg: '#1C5A34', fg: '#FFD166', font: 'bold 64px Georgia, serif' });
    shopSign.position.set(0, 2.5, 2.15); shopKiosk.add(shopSign);
    colRect(35 - 2.8, 16 - 2.2, 35 + 2.8, 16 + 2.2);

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
