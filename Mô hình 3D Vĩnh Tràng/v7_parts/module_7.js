
    // ---- 8. VÒNG LẶP CHÍNH ----
    const clock = new THREE.Clock();
    const camTmp = new THREE.Vector3();
    let zoneCheckT = 0;
    let stepAcc = 0;
    let moveBlend = 0; // v8: hệ số hòa tốc người chơi (0 = đứng yên, 1 = đủ tốc)
    let autoStuck = 0, autoLastD = 1e9;

    function updatePlayer(dt, t) {
      let mx = 0, mz = 0;
      const fwdX = -Math.sin(player.camYaw), fwdZ = -Math.cos(player.camYaw);
      const rightX = -fwdZ, rightZ = fwdX;
      let manual = false;
      if (keys['KeyW'] || keys['ArrowUp']) { mx += fwdX; mz += fwdZ; manual = true; }
      if (keys['KeyS'] || keys['ArrowDown']) { mx -= fwdX; mz -= fwdZ; manual = true; }
      if (keys['KeyA'] || keys['ArrowLeft']) { mx -= rightX; mz -= rightZ; manual = true; }
      if (keys['KeyD'] || keys['ArrowRight']) { mx += rightX; mz += rightZ; manual = true; }
      if (joyVec.x || joyVec.y) {
        mx += fwdX * (-joyVec.y) + rightX * joyVec.x;
        mz += fwdZ * (-joyVec.y) + rightZ * joyVec.x;
        manual = true;
      }
      // Thao tác tay LUÔN thắng: hủy tự đi của nút động từ ngay
      if (manual) cancelAutoWalk();
      // Tự đi theo nút động từ: bám các điểm via -> điểm đứng chuẩn -> mở hành động
      let autoSpeed = 0;
      if (autoWalk && !manual) {
        const wp = autoWalk.path[0];
        if (!wp) {
          const st = autoWalk.station; autoWalk = null; hideTrail();
          // v7.3 (chẩn đoán P12): path rỗng cũng có thể do autoStuck bỏ qua hết
          // waypoint khi avatar bị kẹt — khi đó TUYỆT ĐỐI không chạy hành động
          // trạm từ xa (V7.2 từng ghi nhận "vái Phật nằm" PASS từ cách trạm
          // 38m). Chỉ chạy hành động khi avatar thật sự đứng trong vùng trạm.
          if (st) {
            const dd = Math.hypot(player.pos.x - st.pos[0], player.pos.z - st.pos[1]);
            if (dd <= Math.max(2.5, st.r || 0)) runStationAction(st);
          }
        } else {
          const dx = wp.x - player.pos.x, dz = wp.z - player.pos.z;
          const d = Math.hypot(dx, dz);
          const isLast = autoWalk.path.length === 1;
          if (d < (isLast ? 0.5 : 0.7)) { autoWalk.path.shift(); autoLastD = 1e9; autoStuck = 0; }
          else {
            mx += dx / d; mz += dz / d; autoSpeed = autoSpeedBase;
            if (d > autoLastD - 0.01) { autoStuck += dt; if (autoStuck > 2.5) { autoWalk.path.shift(); autoStuck = 0; autoLastD = 1e9; } }
            else autoStuck = 0;
            autoLastD = d;
          }
        }
      }
      // Nhấp sàn để đi (thao tác tay)
      if (player.target && !autoWalk) {
        const dx = player.target.x - player.pos.x, dz = player.target.z - player.pos.z;
        const d = Math.hypot(dx, dz);
        if (d < 0.4) { player.target = null; }
        else { mx += dx / d; mz += dz / d; }
      }
      const len = Math.hypot(mx, mz);
      if (len > 0.01) {
        mx /= len; mz /= len;
        // v8: hòa tốc — bước đi nhân hệ số blend tăng dần (đạt đủ tốc sau
        // ~0,2s game) thay cho đạt tốc tối đa ngay tick đầu; sàn 0,35 giữ
        // cho auto-walk không bao giờ đứng chờ blend ở cuối chặng.
        moveBlend = Math.min(1, moveBlend + dt * 5);
        const blendK = 0.35 + 0.65 * moveBlend;
        const step = (autoSpeed || player.speed) * dt * blendK;
        tryMove(player.pos.x + mx * step, player.pos.z + mz * step);
        // Quay mặt theo hướng đi
        const targetYaw = Math.atan2(mx, mz);
        let dy = targetYaw - player.yaw;
        while (dy > Math.PI) dy -= Math.PI * 2;
        while (dy < -Math.PI) dy += Math.PI * 2;
        player.yaw += dy * Math.min(1, dt * 10);
        player.walkPhase += dt * 6.2 * blendK;
        player.moving = true;
        stepAcc += dt;
        if (stepAcc > 0.45) { stepAcc = 0; playStep(); }
      } else {
        moveBlend = Math.max(0, moveBlend - dt * 7);
        player.moving = false;
      }
      playerAv.group.position.x = player.pos.x;
      playerAv.group.position.z = player.pos.z;
      playerAv.group.rotation.y = player.yaw;
      // V7: chọn action cho model thật theo trạng thái (nhịp thời gian giữ nguyên v6)
      if (bowAnim > 0) playerAv.setPose('Vái');
      else if (playerAv.onceName) { /* đang cắm nhang — playOnce tự chạy hết */ }
      else if (player.moving) playerAv.setPose('Di bo');
      else if (silenceLeft > 0 || silenceDone || document.body.classList.contains('ritual-dim')) playerAv.setPose('Chắp tay');
      else playerAv.setPose('Dung');
      // Vái/lạy (v6: mỗi lạy 2,3 giây — chậm rãi; xong giữ một nhịp tĩnh)
      if (bowAnim > 0) {
        bowAnim -= dt;
        if (bowAnim <= 0) { bowHoldT = 1.5; }
      } else if (bowHoldT > 0) {
        bowHoldT -= dt;
        if (bowHoldT <= 0) ritualDimRemove('bow');
      }
      // Ra khỏi điện khi đi tới cửa phía nam
      if (inside && player.pos.z - 300 > 22.3) exitInterior();
    }

    function detectZone() {
      if (inside) return 'dien';
      const { x, z } = player.pos;
      if (z > 34) return 'cong';
      if (x < -18 && z < -30) return 'thap';
      if (x < -18) return 'dilac';
      return 'san';
    }

    const saidVoice = {};
    function detectStation() {
      let best = null, bestD = 1e9;
      for (const st of STATIONS) {
        if (!!st.inside !== inside) continue;
        const d = Math.hypot(player.pos.x - st.pos[0], player.pos.z - st.pos[1]);
        if (d < st.r && d < bestD) { best = st; bestD = d; }
      }
      if (best !== currentStation) {
        currentStation = best;
        if (best) {
          let v = null;
          if (best.voice && !saidVoice[best.id]) { saidVoice[best.id] = true; v = best.voice; }
          sayAn(best.an, v);
        }
        refreshVerb();
      }
      // Phật nằm: đứng lặng 10s trước khi vái (UI mờ; hết lặng mới hiện nút Tiếp)
      if (currentStation && currentStation.id === 'nirvana' && !V4.journey.nirvana) {
        if (silenceLeft <= 0 && !silenceDone) { silenceLeft = 10; ritualDimAdd('silence'); }
      } else if (!currentStation || currentStation.id !== 'nirvana') {
        silenceLeft = 0; silenceDone = false;
        ritualDimRemove('silence'); hideQuiet();
      }
    }

    // NPC (v6): đi chậm trên lối; trước tượng/lư thì dừng, quay mặt về tượng,
    // vái một vái chậm (2,4s) rồi đứng lặng chắp tay; sư đi chậm qua sân.
    function updateNPCs(dt, t) {
      const stepNPC = (n) => {
        const g = n.av.group;
        if (n.pause > 0) {
          n.pause -= dt;
          if (n.faceYaw !== null && n.faceYaw !== undefined) {
            let dy = n.faceYaw - g.rotation.y;
            while (dy > Math.PI) dy -= Math.PI * 2;
            while (dy < -Math.PI) dy += Math.PI * 2;
            g.rotation.y += dy * Math.min(1, dt * 2.5);
          }
          if (n.bowT > 0) { n.bowT -= dt; n.av.setPose('Vái'); }
          else n.av.setPose(n.faceYaw !== null && n.faceYaw !== undefined ? 'Chắp tay' : 'Dung');
          return;
        }
        const wp = n.route[n.wp];
        const dx = wp[0] - g.position.x, dz = wp[1] - g.position.z;
        const d = Math.hypot(dx, dz);
        if (d < 0.5) {
          const foc = (typeof NPC_FOCUS !== 'undefined') ? NPC_FOCUS[wp[0] + ',' + wp[1]] : null;
          n.wp = (n.wp + 1) % n.route.length;
          if (foc) {
            n.pause = foc[1]; n.bowT = 2.4;
            n.faceYaw = Math.atan2(foc[0][0] - g.position.x, foc[0][1] - g.position.z);
          } else { n.pause = (n.pauseBase || 1.5) + (n.wp % 3); n.bowT = 0; n.faceYaw = null; }
          return;
        }
        g.position.x += (dx / d) * n.speed * dt;
        g.position.z += (dz / d) * n.speed * dt;
        // v8: rẽ GIẢM CHẤN thay cho snap tức thì — bản cũ gán thẳng
        // rotation.y = atan2 mỗi tick nên NPC giật cục khi đổi hướng ở
        // waypoint (đo ở v8_shots/before/measure.json). Lerp dt*4 như nhịp
        // rẽ của người chơi, bọc wrap ±π.
        const wantYaw = Math.atan2(dx, dz);
        let dyaw = wantYaw - g.rotation.y;
        while (dyaw > Math.PI) dyaw -= Math.PI * 2;
        while (dyaw < -Math.PI) dyaw += Math.PI * 2;
        g.rotation.y += dyaw * Math.min(1, dt * 4);
        n.av.setPose('Di bo'); // V7: model thật đi bằng action 'Di bo'
      };
      for (const n of npcs) stepNPC(n);
      for (const m of monks) { if (!m.still) stepNPC(m); }
      sweeper.group.rotation.y = Math.sin(t * 0.5) * 0.18; // V7: giảm biên độ — model thật không lắc cả thân như khối
      broom.rotation.x = 0.4 + Math.sin(t * 2) * 0.15;
    }

    function updatePigeons(dt, t) {
      for (const p of pigeons) {
        const d = Math.hypot(player.pos.x - p.group.position.x, player.pos.z - p.group.position.z);
        if (p.state === 'perch') {
          p.peck += dt;
          p.group.rotation.y = Math.sin(t * 0.7 + p.seed) * 0.8;
          p.group.position.y = 0.12 + (Math.sin(p.peck * 6) > 0.7 ? -0.05 : 0);
          if (d < 3 && !inside) {
            p.state = 'fly';
            const a = Math.random() * Math.PI * 2;
            p.tx = Math.max(-35, Math.min(52, p.group.position.x + Math.cos(a) * 8));
            p.tz = Math.max(-40, Math.min(50, p.group.position.z + Math.sin(a) * 8));
          }
        } else {
          const dx = p.tx - p.group.position.x, dz = p.tz - p.group.position.z;
          const dd = Math.hypot(dx, dz);
          if (dd < 0.5) { p.state = 'perch'; p.group.position.y = 0.12; p.wL.rotation.z = 0; p.wR.rotation.z = 0; continue; }
          p.group.position.x += (dx / dd) * 6 * dt;
          p.group.position.z += (dz / dd) * 6 * dt;
          p.group.position.y = 1.2 + Math.sin(t * 5) * 0.5;
          p.group.rotation.y = Math.atan2(dx, dz);
          p.wL.rotation.z = Math.sin(t * 18) * 0.7;
          p.wR.rotation.z = -Math.sin(t * 18) * 0.7;
        }
      }
    }

    // tick(dt, render): MỘT bước mô phỏng — toàn bộ logic từng khung hình nằm ở đây.
    // Vòng rAF thật gọi tick với dt thật; bản kiểm thử (TESTLOCAL) có thể gọi tick
    // trực tiếp với dt cố định và render=false để tua nhanh tất định (xem assemble_v6.py).
    // V7.1: chặn camera xuyên cột đỏ trong điện — cột trong interior.js: trục
    // r=0,48 tại local x=±8,5, z=-18,-10,-2,6,14,20; temple đặt tại world (300,300)
    // -> cột world x=291,5/308,5, z=282,290,298,306,314,320. Kẹp camera ngoài hình
    // trụ r=0,8 (trục + biên 0,32). Chỉ áp khi đang ở trong điện.
    const HALL_PILLARS = [];
    for (const pz of [282, 290, 298, 306, 314, 320]) { HALL_PILLARS.push([291.5, pz], [308.5, pz]); }
    const PILLAR_R = 0.8;
    function clampCamOutOfPillars(v) {
      for (const [px, pz] of HALL_PILLARS) {
        let dx = v.x - px, dz = v.z - pz;
        let d = Math.hypot(dx, dz);
        if (d >= PILLAR_R) continue;
        if (d < 1e-4) { // camera đúng tâm cột: đẩy theo hướng từ người chơi tới camera
          dx = v.x - player.pos.x; dz = v.z - player.pos.z; d = Math.hypot(dx, dz);
          if (d < 1e-4) { dx = 1; dz = 0; d = 1; }
        }
        const s = PILLAR_R / d;
        v.x = px + dx * s; v.z = pz + dz * s;
      }
      return v;
    }
    let simT = 0;
    function tick(dt, render = true) {
      simT += dt;
      const t = simT;
      updateCharMixers(dt); // V7: tiến các AnimationMixer của nhân vật thật
      updatePlayer(dt, t);
      updateCompanion(dt, t);
      detectStation();
      if (currentStation && currentStation.id === 'nirvana' && silenceLeft > 0) {
        silenceLeft -= dt;
        if (silenceLeft <= 0) { silenceLeft = 0; silenceDone = true; showQuiet(); }
      }
      zoneCheckT += dt;
      if (zoneCheckT > 1) { zoneCheckT = 0; setZone(detectZone()); }
      updateNPCs(dt, t);
      updatePigeons(dt, t);
      // Lá rơi
      for (const l of leafFall) {
        l.m.position.y -= l.speed * dt;
        l.m.position.x += Math.sin(t * 1.2 + l.seed) * 0.2 * dt;
        l.m.rotation.z += dt * 0.8; l.m.rotation.x += dt * 0.5;
        if (l.m.position.y < 0.1) l.m.position.y = 5 + Math.random() * 2;
      }
      // Cá lượn
      for (const f of fishes) {
        f.ang += f.sp * dt;
        f.mesh.position.x = Math.cos(f.ang) * f.r;
        f.mesh.position.z = Math.sin(f.ang) * f.r * 0.7;
        f.mesh.rotation.y = Math.atan2(-Math.cos(f.ang) * 0.7, -Math.sin(f.ang));
      }
      // Khói nhang
      smokeMain.update(dt, t); smokeDiLac.update(dt, t);
      smokeAdida.update(dt, t); smokeAltar.update(dt, t);
      // Nến flicker ±15% ~7Hz
      candleLights.forEach((cl, i) => { cl.intensity = 1.0 * (1 + 0.15 * Math.sin(t * 44 + i * 2.1)); });
      // Hào quang xoay chậm
      if (typeof haloRing1 !== 'undefined') { haloRing1.rotation.z += dt * 0.2; haloRing2.rotation.z -= dt * 0.15; }
      // Camera bám sau vai; riêng sạp nhang có góc máy riêng (camOverride ở module_6b)
      if (camOverride) {
        camTmp.set(camOverride.x, camOverride.y, camOverride.z);
        camera.position.lerp(camTmp, Math.min(1, dt * 3));
        camera.lookAt(camOverride.lx, camOverride.ly, camOverride.lz);
      } else {
        const dist = inside ? 3.5 : 5, height = inside ? 2.3 : 3.0;
        camTmp.set(
          player.pos.x + Math.sin(player.camYaw) * dist,
          height,
          player.pos.z + Math.cos(player.camYaw) * dist);
        if (inside) clampCamOutOfPillars(camTmp); // V7.1: đích camera không nằm trong cột
        camera.position.lerp(camTmp, Math.min(1, dt * 6));
        if (inside) clampCamOutOfPillars(camera.position); // V7.1: kẹp cả vị trí sau lerp
        camera.lookAt(player.pos.x, 1.4, player.pos.z);
      }
      if (render) renderer.render(scene, camera);
    }
    function animate() {
      requestAnimationFrame(animate);
      const dt = Math.min(clock.getDelta(), 0.05);
      tick(dt, true);
    }

    window.addEventListener('resize', () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    });

    // Nhang cháy ngắn dần theo phiên (que thu nhỏ dần) — chỉ lư sân còn thắp được
    const sessionStart = Date.now();
    setInterval(() => {
      const k = Math.max(0.3, 1 - (Date.now() - sessionStart) / 1800000);
      [burnerSticks, burnerDiLac.sticks, burnerAdida.sticks].forEach(sg => {
        if (sg) sg.scale.y = k;
      });
    }, 5000);

    // Debug qua URL: ?v5pos=x,z (đặt người chơi)
    try {
      const q = new URLSearchParams(location.search);
      const pp = q.get('v5pos') || q.get('v4pos');
      if (pp) {
        const [px, pz] = pp.split(',').map(Number);
        if (isFinite(px) && isFinite(pz)) { player.pos.set(px, 0, pz); player.target = null; anState.pos.set(px - 1.5, 0, pz + 1.5); }
      }
    } catch (e) {}

    animate();
