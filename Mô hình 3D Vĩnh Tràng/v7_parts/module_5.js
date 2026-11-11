    // ---- 6. NHÂN VẬT THẬT (V7) — GLB rigged CHUẨN của dự án ----
    // Chung Hy chốt 09/11: web phải dùng đúng 3 model đã dựng + kiểm chứng
    // (user/files: nu-phuc-hoi-mau / nam / tre-em — bản "-chuyen-dong", rigged),
    // KHÔNG dùng avatar khối tự chế nữa. Màu nằm ở vertex color (GLB không có
    // material/UV) -> bắt buộc bật vertexColors khi nạp.
    // Mapping action (đo trực tiếp từ cả 3 GLB — mỗi file đủ 8 action, 15 xương):
    //   'Dung'       2.80s -> đứng chờ (idle)
    //   'Di bo'      1.24s -> đang di chuyển
    //   'Chắp tay'   3.20s -> đứng chắp tay lặng (NPC trước tượng; người chơi trong nhịp lễ)
    //   'Vái'        3.80s -> vái/lạy — CÓ action riêng, dùng cho mọi nhịp startBow
    //   'Quỳ'        5.80s -> giữ khung gần cuối cho khách ngồi thiền trong điện
    //   'Thắp nhang' 4.70s -> nhịp 4 cắm nhang ở lư sân (playOnce)
    //   'Lên/Xuống cầu thang' -> không dùng (khuôn viên bằng phẳng)
    const CHAR_HEIGHT = { nu: 1.62, nam: 1.72, tre: 1.26 }; // chiều cao hiển thị (m)
    const charTemplates = {}; // kind -> { root, clips, height, minY }
    const charRegistry = [];
    window.__charsReady = false;

    function b64ToBuf(b64) {
      const bin = atob(b64);
      const buf = new Uint8Array(bin.length);
      for (let i = 0; i < bin.length; i++) buf[i] = bin.charCodeAt(i);
      return buf.buffer;
    }
    function loadCharTemplate(kind, b64) {
      return new Promise((resolve) => {
        new GLTFLoader().parse(b64ToBuf(b64), '', (gltf) => {
          const root = gltf.scene;
          root.traverse(o => {
            if (o.isMesh) {
              o.castShadow = true; o.frustumCulled = false;
              if (o.material) {
                o.material.vertexColors = true;
                // GLB KHÔNG khai material -> GLTFLoader cấp material mặc định
                // theo spec glTF: metalness = 1, roughness = 1. Kim loại không
                // có env map thì diffuse chết -> nhân vật ĐEN THUI dù đèn đủ
                // (đo + đối chiếu A/B thật 09/11). Ép về vải: metal 0, rough .92.
                o.material.metalness = 0;
                o.material.roughness = 0.92;
              }
              // GLB xuất thiếu thuộc tính normal -> MeshStandardMaterial ra đen
              // tuyệt đối (đo thật 09/11: attrs chỉ có position/skinIndex/
              // skinWeight/color). Tự tính normal mượt từ bind pose.
              if (!o.geometry.getAttribute('normal')) o.geometry.computeVertexNormals();
            }
          });
          const clips = {};
          gltf.animations.forEach(c => { clips[c.name.replace(/_world$/, '')] = c; });
          // ĐO THẬT chiều cao khi ĐÃ DIỄN action 'Dung': Box3 trên bind pose
          // nhỏ hơn hẳn (nút armature mang scale của Blender — đo 0,771 so với
          // 1,112 khi diễn, lệch ~1,44 lần). Probe bằng 1 bản clone + mixer riêng.
          let animH = 0, animMinY = 0;
          try {
            const probe = skeletonClone(root);
            const pg = new THREE.Group(); pg.add(probe);
            const pm = new THREE.AnimationMixer(probe);
            const dung = clips['Dung'];
            if (dung) { pm.clipAction(dung).play(); pm.update(0.3); }
            pg.updateMatrixWorld(true);
            probe.traverse(o => { if (o.isSkinnedMesh && o.skeleton) o.skeleton.update(); });
            const pb = new THREE.Box3().setFromObject(pg);
            animH = Math.max(0.01, pb.max.y - pb.min.y); animMinY = pb.min.y;
          } catch (e) { console.error('V7: probe chiều cao lỗi', kind, e); }
          if (!(animH > 0.05)) { const b2 = new THREE.Box3().setFromObject(root); animH = Math.max(0.01, b2.max.y - b2.min.y); animMinY = b2.min.y; }
          const scale = CHAR_HEIGHT[kind] / animH;
          charTemplates[kind] = { root, clips, scale, footOff: -animMinY * scale };
          resolve(true);
        }, (err) => { console.error('V7: parse GLB lỗi', kind, err); resolve(false); });
      });
    }
    // Biến thể áo chư Tăng: nhuộm lại cụm vertex-color áo tràng của model nam.
    // Số đo từ GLB nam: áo = (43,20,20) 62% + (20,0,0) 22% đỉnh; da (191,128,84),
    // tóc (0,0,0), giày (171,171,148) đều nằm ngoài ngưỡng dưới đây -> không lem.
    function recolorMonkRobe(model, tone) {
      model.traverse(o => {
        if (!o.isMesh) return;
        o.geometry = o.geometry.clone();
        const col = o.geometry.getAttribute('color');
        if (!col || !col.array || col.itemSize < 3) return;
        const a = col.array, st = col.itemSize;
        for (let i = 0; i < col.count; i++) {
          const r = a[i * st], g = a[i * st + 1], b = a[i * st + 2];
          if (r >= 12 && r <= 78 && g <= 38 && b <= 38 && r > g + 5) {
            const dark = r < 30;
            a[i * st] = Math.round((dark ? 96 : 138) * tone);
            a[i * st + 1] = Math.round((dark ? 58 : 86) * tone);
            a[i * st + 2] = Math.round((dark ? 22 : 34) * tone);
          }
        }
        col.needsUpdate = true;
      });
    }
    // v7.2: biến thể ÁO DÀI PASTEL cho NPC nữ — nhuộm vertex-color như sư áo nâu.
    // Số đo từ GLB nữ: cụm áo tràng xám = (96,87,100) chiếm 82,4% đỉnh; da
    // (198,124,85), giày be (179,161,139), tóc (4,3,2) đều ngoài ngưỡng -> không lem.
    function recolorPastelDress(model, rgb) {
      model.traverse(o => {
        if (!o.isMesh) return;
        o.geometry = o.geometry.clone();
        const col = o.geometry.getAttribute('color');
        if (!col || !col.array || col.itemSize < 3) return;
        const a = col.array, st = col.itemSize;
        for (let i = 0; i < col.count; i++) {
          const r = a[i * st], g = a[i * st + 1], b = a[i * st + 2];
          if (r >= 78 && r <= 114 && g >= 68 && g <= 106 && b >= 82 && b <= 118 && (r - g) >= 0 && (r - g) <= 20) {
            a[i * st] = rgb[0]; a[i * st + 1] = rgb[1]; a[i * st + 2] = rgb[2];
          }
        }
        col.needsUpdate = true;
      });
    }
    const DRESS_PASTEL = {
      hong: [240, 186, 203], tim: [206, 186, 233], trang: [244, 239, 230], dao: [246, 205, 190],
    };
    // Nón lá: phụ kiện fit theo công thức ĐÃ KIỂM CHỨNG của dự án
    // (TRANG_PHUC_MAC_DINH_3_NHAN_VAT: vành R = 0.126 x H, chóp cụt) — gắn vào
    // xương Head bằng attach() để nón đi theo đầu qua mọi action.
    function attachHat(av) {
      const head = av.model.getObjectByName('Head');
      if (!head) return;
      const H = CHAR_HEIGHT[av.kind];
      // Kích thước nón tính theo ĐƠN VỊ THẾ GIỚI: nón được add vào scene ở
      // scale 1 rồi head.attach() giữ nguyên world transform (bản trước chia
      // thêm hệ số scale của model nên nón nhỏ hẳn, lọt trong đầu — không thấy).
      const geo = new THREE.CylinderGeometry(0.05 * H, 0.126 * H, 0.115 * H, 20, 1, true);
      const hat = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ color: 0xE8D8A0, roughness: 0.85, side: THREE.DoubleSide }));
      hat.castShadow = true;
      av.group.updateMatrixWorld(true);
      const hp = new THREE.Vector3(); head.getWorldPosition(hp);
      // Đặt vành theo ĐỈNH ĐẦU đo thật (= group.y + H), KHÔNG theo gốc xương
      // Head: gốc xương nằm ở cổ/hàm nên cộng theo xương làm nón sụp xuống
      // ngang cằm, che hết mặt (đo từ ảnh nghiệm thu 09/11). Tâm nón cao hơn
      // đỉnh đầu 0.02H -> vành ôm trán, mặt lộ rõ dưới vành.
      const gy = av.group.getWorldPosition(new THREE.Vector3()).y;
      hat.position.set(hp.x, gy + H * 1.02, hp.z);
      scene.add(hat);
      head.attach(hat);
    }
    function applyCharPose(av, instant) {
      if (!av.mixer || av.kneel) return;
      const next = av.actions[av._want];
      if (!next || av.pose === av._want) return;
      const prev = av.pose ? av.actions[av.pose] : null;
      next.reset(); next.enabled = true; next.setLoop(THREE.LoopRepeat, Infinity); next.timeScale = 1;
      if (prev && prev !== next && !instant) { next.fadeIn(0.22); prev.fadeOut(0.22); }
      else if (prev && prev !== next) prev.stop();
      next.play();
      av.pose = av._want;
    }
    function buildCharModel(av) {
      const tpl = charTemplates[av.kind];
      if (!tpl || av.model) return;
      const model = skeletonClone(tpl.root);
      if (av.robeVariant) recolorMonkRobe(model, av.robeVariant);
      if (av.dressVariant) recolorPastelDress(model, av.dressVariant);
      model.scale.setScalar(tpl.scale);
      model.position.y = tpl.footOff;
      // Layer của group có thể đã set trước khi model nạp xong (khách trong điện)
      const mask = av.group.layers.mask;
      model.traverse(o => { o.layers.mask = mask; if (o.isMesh) { o.castShadow = true; o.frustumCulled = false; } });
      av.group.add(model);
      av.model = model;
      av.mixer = new THREE.AnimationMixer(model);
      av.actions = {};
      Object.keys(tpl.clips).forEach(n => { av.actions[n] = av.mixer.clipAction(tpl.clips[n]); });
      if (av.kneel) {
        const a = av.actions['Quỳ'];
        if (a) {
          a.reset().play(); a.time = 5.15;
          av.mixer.update(0.01); // áp pose quỳ trước khi đo
          a.paused = true; av.pose = 'Quỳ';
          // Căn đáy pose quỳ (gối/shin) chạm đúng mặt group: đo box thật rồi
          // dịch model — footOff của pose đứng không áp được cho tư thế quỳ.
          try {
            av.group.updateMatrixWorld(true);
            model.traverse(o => { if (o.isSkinnedMesh && o.skeleton) o.skeleton.update(); });
            const kb = new THREE.Box3().setFromObject(av.group);
            model.position.y += av.group.position.y - kb.min.y;
          } catch (e) { console.error('V7: căn pose quỳ lỗi', e); }
        }
      } else applyCharPose(av, true);
      if (av.hat) attachHat(av);
    }
    function makeAvatar(opt) {
      const g = new THREE.Group();
      const av = {
        group: g, kind: opt.kind || 'nu',
        hat: !!opt.hat, kneel: !!opt.kneel, robeVariant: opt.robeVariant || 0,
        dressVariant: opt.dressVariant || null,
        mixer: null, actions: {}, model: null, pose: null, _want: opt.initPose || 'Dung',
        onceName: null, onceT: 0,
        setPose(name) { if (this._want !== name) { this._want = name; if (!this.onceName) applyCharPose(this); } },
        playOnce(name) {
          const a = this.actions[name]; if (!a || !this.mixer) return;
          const cur = this.pose ? this.actions[this.pose] : null;
          a.reset(); a.setLoop(THREE.LoopOnce, 1); a.clampWhenFinished = false; a.enabled = true; a.fadeIn(0.15); a.play();
          if (cur && cur !== a) cur.fadeOut(0.15);
          this.onceName = name; this.onceT = a.getClip().duration; this.pose = name;
        },
      };
      charRegistry.push(av);
      if (charTemplates[av.kind]) buildCharModel(av);
      return av;
    }
    function updateCharMixers(dt) {
      for (const av of charRegistry) {
        if (!av.mixer) continue;
        if (av.onceName) {
          av.onceT -= dt;
          if (av.onceT <= 0) { av.onceName = null; av.pose = null; applyCharPose(av); }
        }
        av.mixer.update(dt);
      }
    }
    if (window.__GLB_B64) {
      Promise.all(['nu', 'nam', 'tre'].map(k => loadCharTemplate(k, window.__GLB_B64[k]))).then(() => {
        for (const av of charRegistry) buildCharModel(av);
        window.__charsReady = true;
      });
    }
    // Debug/kiem thu: đọc trạng thái nhân vật (kind + pose + vị trí + chiều cao
    // đo thật từ world box — gồm cả nón nếu có, nên avatar có nón cao hơn ~0,29)
    window.__v7chars = () => charRegistry.map((av, i) => {
      let h = 0, minY = 0;
      if (av.model) {
        try {
          av.group.updateMatrixWorld(true);
          const b = new THREE.Box3().setFromObject(av.group);
          h = +(b.max.y - b.min.y).toFixed(2); minY = +b.min.y.toFixed(2);
        } catch (e) { /* bỏ qua */ }
      }
      return {
        i, kind: av.kind, pose: av.pose, want: av._want, ready: !!av.model, h, minY,
        x: +av.group.position.x.toFixed(1), z: +av.group.position.z.toFixed(1),
      };
    });

    // Người chơi — model theo profile đã chọn (mặc định nữ như ảnh mẫu)
    let S_profile = (window.getProfile && window.getProfile()) || 'nu';
    const playerAv = makeAvatar({ kind: CHAR_HEIGHT[S_profile] ? S_profile : 'nu', hat: true });
    scene.add(playerAv.group);
    const player = {
      pos: new THREE.Vector3(23, 0, 50), yaw: Math.PI, camYaw: 0, speed: 1.05,
      target: null, moving: false, walkPhase: 0, layer: 0,
    };
    playerAv.group.position.copy(player.pos);
    playerAv.group.rotation.y = player.yaw;

    // NPC khách lễ (v6 — HÀNH VI LỄ, không còn đi lang thang vô định):
    // đi chậm trên lối; tới waypoint trước tượng/lư thì đứng chắp tay, vái một
    // vái chậm rồi lặng yên một lúc; hai khách đứng nghỉ trước ghế đá.
    const NPC_KINDS = ['nu', 'nam', 'nu', 'tre', 'nam', 'nu', 'nam', 'tre', 'nu', 'nam'];
    const NPC_ROUTES = [
      [[23, 38], [23, 14], [23, 7], [-10, 10], [-24, 8], [-14, 22.6]],
      [[23, 40], [30, 30], [23, 14], [23, 7]],
      [[45, 40], [40, 30], [23, 14], [-24, 8], [23, 38]],
      [[-14, 30], [-14, 22.6], [23, 14], [23, 7], [12, -38]],
      [[23, 38], [23, 14], [12, -40], [-2, -34], [23, 38]],
      [[45, 40], [23, 30], [23, 14], [23, 7], [44, -16]],
      [[23, 38], [-24, 8], [-24, -16], [23, 14]],
      [[23, 40], [23, 14], [23, 7], [-14, 22.6]],
      [[-14, 30], [23, 14], [23, 7], [23, 38]],
      [[45, 40], [30, 20], [23, 14], [-2, -34]],
    ];
    // Waypoint đứng trước tượng/bàn lễ: key "x,z" -> [điểm nhìn về, số giây đứng lặng]
    const NPC_FOCUS = {
      '-14,22.6': [[-14, 27], 11],   // trước A Di Đà
      '-24,8': [[-24, 0], 11],       // trước Di Lặc
      '23,14': [[25.3, 13.7], 9],    // trước lư sân
      '23,7': [[23, -4], 8],         // trước thềm chánh điện
    };
    const NPC_DRESS = { 0: 'hong', 2: 'tim', 5: 'trang', 8: 'dao' }; // v7.2: NPC nữ mặc áo dài pastel
    const npcs = [];
    for (let i = 0; i < 10; i++) {
      const av = makeAvatar({ kind: NPC_KINDS[i], hat: i % 2 === 0, dressVariant: DRESS_PASTEL[NPC_DRESS[i]] || null });
      scene.add(av.group);
      const route = NPC_ROUTES[i % NPC_ROUTES.length];
      const start = route[i % route.length];
      av.group.position.set(start[0], 0, start[1]);
      npcs.push({
        av, route, wp: (i + 1) % route.length,
        speed: 0.55 + (i % 3) * 0.07, pause: 0, bowT: 0, faceYaw: null, walkPhase: i * 1.7,
      });
    }
    // Hai khách đứng chắp tay nghỉ trước ghế đá (module_2 dựng BENCH_SEATS)
    BENCH_SEATS.forEach(([bx, bz, byaw], i) => {
      const av = makeAvatar({ kind: i ? 'nam' : 'nu', hat: false, initPose: 'Chắp tay', dressVariant: i ? null : DRESS_PASTEL.tim });
      av.group.position.set(bx - Math.sin(byaw) * 0.55, 0, bz - Math.cos(byaw) * 0.55);
      av.group.rotation.y = byaw;
      scene.add(av.group);
    });
    // Chư Tăng: model nam với áo nhuộm nâu vàng từ vertex color (xem recolorMonkRobe);
    // một vị đi chậm qua sân khu giảng đường, một vị đứng lặng chắp tay
    const monks = [];
    {
      const avA = makeAvatar({ kind: 'nam', hat: false, robeVariant: 1.0 });
      scene.add(avA.group);
      avA.group.position.set(44, 0, -16);
      monks.push({ av: avA, route: [[44, -16], [37, -23], [31, -13], [39, -7]], wp: 1, speed: 0.45, pause: 0, faceYaw: null, walkPhase: 0, pauseBase: 3.5 });
      const avB = makeAvatar({ kind: 'nam', hat: false, robeVariant: 0.72, initPose: 'Chắp tay' });
      scene.add(avB.group);
      avB.group.position.set(38, 0, -18);
      avB.group.rotation.y = Math.atan2(44 - 38, -20 + 18); // mặt hướng giảng đường
      monks.push({ av: avB, still: true });
    }
    const sweeper = makeAvatar({ kind: 'nam', hat: true });
    scene.add(sweeper.group);
    sweeper.group.position.set(19, 0, 8);
    const broom = addCyl(-0.42, 0.72, 0.3, 0.03, 1.25, mat(0x8A6D3B, 0.8), sweeper.group);
    broom.rotation.z = 0.5; broom.rotation.x = 0.4;

    // Khách quỳ thiền trong điện (layer 1) — 6 người, 2 hàng; model giữ khung quỳ của action 'Quỳ'
    const seatedNPCs = [];
    [[-4.5, -4], [0, -4], [4.5, -4], [-4.5, 2], [0, 2], [4.5, 2]].forEach(([x, z], i) => {
      const av = makeAvatar({ kind: ['nu', 'nam', 'nu', 'nam', 'tre', 'nu'][i], hat: false, kneel: true });
      av.group.position.set(300 + x, 0.32, 300 + z);
      av.group.rotation.y = Math.PI; // quay mặt về bàn Tam Bảo (-Z)
      setLayerRecursive(av.group, 1);
      temple.add(av.group);
      seatedNPCs.push(av);
    });

    // V6: KHÔNG còn bảng tên nổi trên đầu bất kỳ nhân vật nào.
    // Đổi profile trong Cài đặt -> thay cả model người chơi (nữ/nam/trẻ em).
    window.__onProfile = function (pid) {
      S_profile = pid;
      const kind = CHAR_HEIGHT[pid] ? pid : 'nu';
      if (playerAv.kind !== kind) {
        playerAv.kind = kind;
        if (playerAv.model) {
          playerAv.group.remove(playerAv.model);
          playerAv.model = null; playerAv.mixer = null; playerAv.actions = {}; playerAv.pose = null; playerAv.onceName = null;
        }
        buildCharModel(playerAv);
      }
    };

    // ---- Chú tiểu An (v5): bạn đồng hành — model trẻ em; đi theo người chơi, dẫn tới trạm ----
    const anAv = makeAvatar({ kind: 'tre', hat: false });
    anAv.group.position.set(21.4, 0, 51.6);
    scene.add(anAv.group);
    const anState = { pos: new THREE.Vector3(21.4, 0, 51.6), yaw: Math.PI, walkPhase: 0 };
