
    // ---- 6. AVATAR + NPC (G3) — áo tràng + nón lá, procedural theo nhân vật đã fit ----
    function makeAvatar(opt) {
      const robe = opt.robe || 0x8A9BA8;
      const g = new THREE.Group();
      const body = addBall(0, 0.85, 0, 0.52, mat(robe, 0.5), g); body.scale.set(1.05, 1.35, 0.9);
      const armL = addCyl(-0.48, 0.85, 0, 0.11, 0.75, mat(robe, 0.5), g); armL.rotation.z = 0.18;
      const armR = addCyl(0.48, 0.85, 0, 0.11, 0.75, mat(robe, 0.5), g); armR.rotation.z = -0.18;
      const hands = addBall(0, 0.88, 0.48, 0.15, mat(0xFFDFBA, 0.5), g); // chắp tay phía TRƯỚC ngực
      const head = new THREE.Mesh(new THREE.SphereGeometry(0.34, 20, 16), new THREE.MeshStandardMaterial({ map: faceMonkTex, roughness: 0.3 }));
      head.position.set(0, 1.62, 0); head.rotation.y = -Math.PI / 2; // mặt nhìn về +Z (hướng đi)
      g.add(head);
      let hat = null;
      if (opt.hat !== false) {
        hat = new THREE.Mesh(new THREE.ConeGeometry(0.55, 0.3, 20), mat(0xE8D8A0, 0.7));
        hat.position.set(0, 1.88, 0); hat.castShadow = true; g.add(hat);
      }
      if (opt.bag) addBox(0.58, 0.75, 0.12, 0.26, 0.36, 0.1, mat(0x8A6D3B, 0.8), g);
      g.traverse(o => { o.castShadow = true; });
      return { group: g, head, armL, armR, hands, body, hat };
    }

    // Người chơi — màu áo theo profile đã chọn
    const PROFILE_ROBE = { nu: 0x8A9BA8, nam: 0x6B4A2E, tre: 0x7A9BC4 };
    const PROFILE_SCALE = { nu: 1.0, nam: 1.05, tre: 0.72 };
    // S của v3 nằm trong IIFE — module đọc qua window.getProfile()
    let S_profile = (window.getProfile && window.getProfile()) || 'nu';
    function playerRobe() { return PROFILE_ROBE[S_profile] || 0x8A9BA8; }
    function playerScale() { return PROFILE_SCALE[S_profile] || 1.0; }
    const playerAv = makeAvatar({ robe: playerRobe(), hat: true, bag: true });
    playerAv.group.scale.setScalar(playerScale());
    scene.add(playerAv.group);
    const player = {
      pos: new THREE.Vector3(23, 0, 50), yaw: Math.PI, camYaw: 0, speed: 1.05,
      target: null, moving: false, walkPhase: 0, layer: 0,
    };
    playerAv.group.position.copy(player.pos);
    playerAv.group.rotation.y = player.yaw;

    // NPC khách lễ (v6 — HÀNH VI LỄ, không còn đi lang thang vô định):
    // đi chậm trên lối; tới waypoint trước tượng/lư thì đứng chắp tay, vái một
    // vái chậm rồi lặng yên một lúc; hai khách ngồi nghỉ trên ghế đá.
    const NPC_ROBES = [0x543826, 0x8A552B, 0x1D3557, 0x6E4E37, 0xF4A261, 0x8A9BA8, 0x6B4A2E, 0x3E6B34];
    const NPC_ROUTES = [
      [[23, 38], [23, 14], [23, 7], [-10, 10], [-24, 8], [-14, 24]],
      [[23, 40], [30, 30], [23, 14], [23, 7]],
      [[45, 40], [40, 30], [23, 14], [-24, 8], [23, 38]],
      [[-14, 30], [-14, 24], [23, 14], [23, 7], [12, -38]],
      [[23, 38], [23, 14], [12, -40], [-2, -34], [23, 38]],
      [[45, 40], [23, 30], [23, 14], [23, 7], [44, -16]],
      [[23, 38], [-24, 8], [-24, -16], [23, 14]],
      [[23, 40], [23, 14], [23, 7], [-14, 24]],
      [[-14, 30], [23, 14], [23, 7], [23, 38]],
      [[45, 40], [30, 20], [23, 14], [-2, -34]],
    ];
    // Waypoint đứng trước tượng/bàn lễ: key "x,z" -> [điểm nhìn về, số giây đứng lặng]
    const NPC_FOCUS = {
      '-14,24': [[-14, 28.5], 11],   // trước A Di Đà
      '-24,8': [[-24, 0], 11],       // trước Di Lặc
      '23,14': [[25.3, 13.7], 9],    // trước lư sân
      '23,7': [[23, -4], 8],         // trước thềm chánh điện
    };
    const npcs = [];
    for (let i = 0; i < 10; i++) {
      const av = makeAvatar({ robe: NPC_ROBES[i % NPC_ROBES.length], hat: i % 2 === 0, bag: i % 3 === 0 });
      scene.add(av.group);
      const route = NPC_ROUTES[i % NPC_ROUTES.length];
      const start = route[i % route.length];
      av.group.position.set(start[0], 0, start[1]);
      npcs.push({
        av, route, wp: (i + 1) % route.length,
        speed: 0.55 + (i % 3) * 0.07, pause: 0, bowT: 0, faceYaw: null, walkPhase: i * 1.7,
      });
    }
    // Hai khách ngồi nghỉ trên ghế đá (module_2 dựng BENCH_SEATS)
    BENCH_SEATS.forEach(([bx, bz, byaw], i) => {
      const av = makeAvatar({ robe: NPC_ROBES[(5 + i) % NPC_ROBES.length], hat: false, bag: false });
      av.group.scale.set(0.95, 0.6, 0.95);
      av.group.position.set(bx, 0.42, bz);
      av.group.rotation.y = byaw;
      scene.add(av.group);
    });
    // Chư Tăng: một vị đi chậm qua sân khu giảng đường, một vị đứng lặng
    const monks = [];
    {
      const avA = makeAvatar({ robe: 0x8A552B, hat: false, bag: false });
      scene.add(avA.group);
      avA.group.position.set(44, 0, -16);
      monks.push({ av: avA, route: [[44, -16], [37, -23], [31, -13], [39, -7]], wp: 1, speed: 0.45, pause: 0, faceYaw: null, walkPhase: 0, pauseBase: 3.5 });
      const avB = makeAvatar({ robe: 0x543826, hat: false, bag: false });
      scene.add(avB.group);
      avB.group.position.set(38, 0, -18);
      avB.group.rotation.y = Math.atan2(44 - 38, -20 + 18); // mặt hướng giảng đường
      monks.push({ av: avB, still: true });
    }
    const sweeper = makeAvatar({ robe: 0x3E6B34, hat: true, bag: false });
    scene.add(sweeper.group);
    sweeper.group.position.set(19, 0, 8);
    const broom = addCyl(-0.6, 0.7, -0.3, 0.03, 1.2, mat(0x8A6D3B, 0.8), sweeper.group);
    broom.rotation.z = 0.5; broom.rotation.x = 0.4;

    // Khách ngồi thiền trong điện (layer 1) — 6 người, 2 hàng
    const seatedNPCs = [];
    [[-4.5, -4], [0, -4], [4.5, -4], [-4.5, 2], [0, 2], [4.5, 2]].forEach(([x, z], i) => {
      const av = makeAvatar({ robe: NPC_ROBES[i % NPC_ROBES.length], hat: false, bag: false });
      av.group.scale.set(0.9, 0.62, 0.9);
      av.group.position.set(300 + x, 0.55, 300 + z);
      av.group.rotation.y = Math.PI; // quay mặt về bàn Tam Bảo (-Z)
      setLayerRecursive(av.group, 1);
      temple.add(av.group);
      seatedNPCs.push(av);
    });

    // V6: KHÔNG còn bảng tên nổi trên đầu bất kỳ nhân vật nào.
    // Đổi profile trong v3 -> đổi màu áo + tỉ lệ avatar.
    window.__onProfile = function (pid) {
      S_profile = pid;
      playerAv.body.material.color.setHex(playerRobe());
      playerAv.group.scale.setScalar(playerScale());
    };

    // ---- Chú tiểu An (v5): bạn đồng hành — đi theo người chơi, dẫn tới trạm, chỉ tay khi tới nơi ----
    const anAv = makeAvatar({ robe: 0x3E6B34, hat: false, bag: false });
    anAv.group.scale.setScalar(0.78);
    anAv.group.position.set(21.4, 0, 51.6);
    scene.add(anAv.group);
    const anState = { pos: new THREE.Vector3(21.4, 0, 51.6), yaw: Math.PI, walkPhase: 0 };
