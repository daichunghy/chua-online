
    // ---- 7. ĐI BỘ + TƯƠNG TÁC (tuyến v5) ----
    // Trạng thái v5 (localStorage theo ngày) — khóa RIÊNG, không đụng dữ liệu v4
    const V4KEY = 'chuaOnlineV5';
    const TODAY4 = new Date().toISOString().slice(0, 10);
    let V4 = { bought: null, incenseDate: '', lit: {}, journey: {}, brightness: 1.0 };
    try { const raw = localStorage.getItem(V4KEY); if (raw) V4 = Object.assign(V4, JSON.parse(raw)); } catch (e) {}
    if (V4.incenseDate !== TODAY4) { V4.lit = {}; V4.incenseDate = TODAY4; }
    function saveV4() { try { localStorage.setItem(V4KEY, JSON.stringify(V4)); } catch (e) {} }
    saveV4();

    // Khôi phục nhang lư sân đã thắp hôm nay (cháy tới hết phiên).
    // Lư nhỏ trước tượng + bàn thờ trong điện: chỉ vái, KHÔNG thắp (đúng phép chùa thật).
    if (V4.lit.main) { burnerSticks.visible = true; smokeMain.setActive(true); }

    // ---- Va chạm (bounding circle 0,5m; trượt theo từng trục) ----
    const interiorRects = [
      [-7, -19, 7, -14],        // bàn Tam Bảo
      [-13.7, -15, -11.9, 12],  // dãy La Hán trái
      [11.9, -15, 13.7, 12],    // dãy La Hán phải
      [-13.8, -1.6, -12.4, 1.6], // điện Quan Âm
      [12.4, -1.6, 13.8, 1.6],  // điện Địa Tạng
    ];
    function pointBlocked(x, z) {
      if (inside) {
        x -= 300; z -= 300; // player.pos là world; trong điện đổi sang local
        if (x < -13 || x > 13 || z < -22 || z > 22.4) return true;
        for (const r of interiorRects) if (x > r[0] - 0.5 && x < r[2] + 0.5 && z > r[1] - 0.5 && z < r[3] + 0.5) return true;
        return false;
      }
      if (x < -38 || x > 53 || z < -41 || z > 52) return true;
      for (const r of colRects) if (x > r[0] - 0.5 && x < r[2] + 0.5 && z > r[1] - 0.5 && z < r[3] + 0.5) return true;
      for (const c of colCircles) { const dx = x - c[0], dz = z - c[1]; if (dx * dx + dz * dz < (c[2] + 0.5) * (c[2] + 0.5)) return true; }
      return false;
    }
    // Độ lún vào vùng cấm (>0 = đang bị chặn, giá trị = mức lún sâu nhất).
    // Dùng để THOÁT NÊM: trượt theo từng trục có thể lọt vào góc lõm của collider
    // (mỗi bước đơn trục hợp lệ nhưng vị trí tổng hợp đã vào trong vùng cấm) —
    // khi đó cả hai trục đều bị chặn và nhân vật kẹt cứng. Gặp trường hợp đó,
    // cho phép di chuyển theo hướng giảm độ lún cho tới khi thoát hẳn.
    function blockDepth(x, z) {
      let d = 0;
      const rectDepth = (r, grow) => {
        const x0 = r[0] - grow, z0 = r[1] - grow, x1 = r[2] + grow, z1 = r[3] + grow;
        if (x > x0 && x < x1 && z > z0 && z < z1) return Math.min(x - x0, x1 - x, z - z0, z1 - z);
        return 0;
      };
      if (inside) {
        const lx = x - 300, lz = z - 300;
        d = Math.max(d, -13 - lx, lx - 13, -22 - lz, lz - 22.4);
        for (const r of interiorRects) d = Math.max(d, rectDepth([r[0] + 300, r[1] + 300, r[2] + 300, r[3] + 300], 0.5));
        return d;
      }
      d = Math.max(d, -38 - x, x - 53, -41 - z, z - 52);
      for (const r of colRects) d = Math.max(d, rectDepth(r, 0.5));
      for (const c of colCircles) {
        const R = c[2] + 0.5, dist = Math.hypot(x - c[0], z - c[1]);
        if (dist < R) d = Math.max(d, R - dist);
      }
      return d;
    }
    function tryMove(nx, nz) {
      const px = player.pos.x, pz = player.pos.z;
      const cur = blockDepth(px, pz);
      if (cur > 0) {
        // Đang bị nêm: ưu tiên bước giảm độ lún nhất trong các hướng quanh mình
        const stepLen = Math.max(0.05, Math.hypot(nx - px, nz - pz));
        let bx = px, bz = pz, bd = cur;
        for (let k = 0; k < 8; k++) {
          const a = (k / 8) * Math.PI * 2;
          const cx = px + Math.cos(a) * stepLen, cz = pz + Math.sin(a) * stepLen;
          const cd = blockDepth(cx, cz);
          if (cd < bd) { bd = cd; bx = cx; bz = cz; }
        }
        // Cả hướng định đi lẫn hướng thoát tốt nhất đều được xét
        const fd = blockDepth(nx, nz);
        if (fd < bd) { bx = nx; bz = nz; bd = fd; }
        if (bd < cur) { player.pos.x = bx; player.pos.z = bz; }
        return;
      }
      if (!pointBlocked(nx, pz)) player.pos.x = nx;
      if (!pointBlocked(px, nz)) player.pos.z = nz;
    }
    // Tọa độ trong điện: world (300+x, 300+z) <-> local (x, z)
    function toLocal() { return { x: player.pos.x - 300, z: player.pos.z - 300 }; }

    // ---- Nhập liệu: WASD/mũi tên + nhấp sàn + joystick + vuốt nhìn quanh ----
    const keys = {};
    window.addEventListener('keydown', e => {
      keys[e.code] = true;
      if (e.code === 'KeyF') doContextAction();
      if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'Space'].includes(e.code)) e.preventDefault();
    });
    window.addEventListener('keyup', e => { keys[e.code] = false; });
    const raycaster = new THREE.Raycaster();
    const groundPlane = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0);
    const clickPoint = new THREE.Vector3();
    let downX = 0, downY = 0, downT = 0;
    renderer.domElement.addEventListener('pointerdown', e => { downX = e.clientX; downY = e.clientY; downT = performance.now(); });
    renderer.domElement.addEventListener('pointerup', e => {
      if (e.pointerType === 'touch') return;
      if (Math.hypot(e.clientX - downX, e.clientY - downY) > 6 || performance.now() - downT > 300) return; // kéo xoay, không phải nhấp
      const r = renderer.domElement.getBoundingClientRect();
      const nx = ((e.clientX - r.left) / r.width) * 2 - 1;
      const ny = -((e.clientY - r.top) / r.height) * 2 + 1;
      raycaster.setFromCamera({ x: nx, y: ny }, camera);
      if (raycaster.ray.intersectPlane(groundPlane, clickPoint)) {
        player.target = { x: clickPoint.x, z: clickPoint.z };
        cancelAutoWalk(); // thao tác tay luôn thắng — hủy tự đi của nút động từ
      }
    });
    // Vuốt nửa phải để xoay camera (chuột kéo cũng xoay)
    let dragging = false, lastX = 0, lastY = 0;
    renderer.domElement.addEventListener('pointerdown', e => { dragging = true; lastX = e.clientX; lastY = e.clientY; });
    window.addEventListener('pointermove', e => {
      if (!dragging || viewMode !== 'walk') return;
      player.camYaw -= (e.clientX - lastX) * 0.005;
      lastX = e.clientX; lastY = e.clientY;
    });
    window.addEventListener('pointerup', () => { dragging = false; });
    // Joystick ảo (nửa trái)
    const joy = document.getElementById('joystick'), knob = document.getElementById('joy-knob');
    let joyVec = { x: 0, y: 0 }, joyActive = false;
    joy.addEventListener('pointerdown', e => { joyActive = true; joy.setPointerCapture(e.pointerId); moveJoy(e); });
    joy.addEventListener('pointermove', e => { if (joyActive) moveJoy(e); });
    joy.addEventListener('pointerup', () => { joyActive = false; joyVec = { x: 0, y: 0 }; knob.style.transform = 'translate(-50%,-50%)'; });
    function moveJoy(e) {
      const r = joy.getBoundingClientRect();
      let dx = (e.clientX - r.left - r.width / 2) / (r.width / 2);
      let dy = (e.clientY - r.top - r.height / 2) / (r.height / 2);
      const l = Math.hypot(dx, dy); if (l > 1) { dx /= l; dy /= l; }
      joyVec = { x: dx, y: dy };
      knob.style.transform = `translate(calc(-50% + ${dx * 28}px), calc(-50% + ${dy * 28}px))`;
    }

    // ---- Camera: bám sau vai 4–6m (v5: ĐÃ XÓA "Xem nhanh"/OrbitControls theo bản chốt —
    // thay bằng nút Bản đồ tĩnh, không nhảy camera) ----
    let viewMode = 'walk';

    // ---- Ra / vào chánh điện (fade 0,4s) ----
    let inside = false;
    let fadeTimer = null;
    function fadeSwap(mid) {
      const f = document.getElementById('fade-overlay');
      f.style.transition = 'opacity .4s'; f.style.opacity = '1';
      clearTimeout(fadeTimer);
      fadeTimer = setTimeout(() => { mid(); f.style.opacity = '0'; }, 420);
    }
    function enterInterior() {
      fadeSwap(() => {
        inside = true;
        player.pos.set(300, 0, 300 + 20);
        player.yaw = Math.PI; player.camYaw = 0;
        setLayerRecursive(playerAv.group, 1);
        setLayerRecursive(anAv.group, 1);
        anState.pos.set(298.6, 0, 300 + 21);
        playBell();
        showToast('Vào chánh điện — bỏ dép ở thềm, giữ tâm thanh tịnh.');
        playVoice('s3_bo_dep');
        window.__setHallChant(true); // chỉ phát nếu có bản tụng THẬT (niem_phat_xa.mp3)
        shoePairs.visible = true;
        setZone('dien');
        onEnterInterior();
      });
    }
    function exitInterior() {
      fadeSwap(() => {
        inside = false;
        player.pos.set(17.5, 0, 7.5); // ra đúng cửa BÊN phía tây chánh điện
        player.yaw = Math.PI; player.camYaw = 0; // quay mặt về chánh điện, camera ở sân
        setLayerRecursive(playerAv.group, 0);
        setLayerRecursive(anAv.group, 0);
        anState.pos.set(16.1, 0, 8.6);
        window.__setHallChant(false);
        setZone('san');
        onExitInterior();
      });
    }
