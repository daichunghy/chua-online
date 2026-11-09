
    // ---- 8. VÒNG LẶP CHÍNH ----
    const clock = new THREE.Clock();
    const camTmp = new THREE.Vector3();
    let zoneCheckT = 0;
    let stepAcc = 0;
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
          if (st) runStationAction(st);
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
        const step = (autoSpeed || player.speed) * dt;
        tryMove(player.pos.x + mx * step, player.pos.z + mz * step);
        // Quay mặt theo hướng đi
        const targetYaw = Math.atan2(mx, mz);
        let dy = targetYaw - player.yaw;
        while (dy > Math.PI) dy -= Math.PI * 2;
        while (dy < -Math.PI) dy += Math.PI * 2;
        player.yaw += dy * Math.min(1, dt * 10);
        player.walkPhase += dt * 6.2;
        player.moving = true;
        stepAcc += dt;
        if (stepAcc > 0.45) { stepAcc = 0; playStep(); }
      } else {
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
        g.rotation.y = Math.atan2(dx, dz);
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
        const dist = inside ? 3.2 : 4.7, height = inside ? 1.8 : 1.75;
        camTmp.set(
          player.pos.x + Math.sin(player.camYaw) * dist,
          height,
          player.pos.z + Math.cos(player.camYaw) * dist);
        camera.position.lerp(camTmp, Math.min(1, dt * 6));
        const lookAheadDist = inside ? 6.0 : 12.0;
        const lookHeight = inside ? 1.5 : 2.7;
        const lookX = player.pos.x - Math.sin(player.camYaw) * lookAheadDist;
        const lookZ = player.pos.z - Math.cos(player.camYaw) * lookAheadDist;
        camera.lookAt(lookX, lookHeight, lookZ);
      }
      // Cập nhật tọa độ chiếu 3D cho Pin "📍 Chánh điện"
      const pinEl = document.getElementById('pin-chanhdien');
      if (pinEl) {
        if (inside) {
          pinEl.style.display = 'none';
        } else {
          // Tọa độ vòm cửa chính Chánh điện (x: 23, y: 5.2, z: 4.2)
          const pinPos = new THREE.Vector3(23, 5.2, 4.2);
          const camToPin = pinPos.clone().sub(camera.position);
          const forward = new THREE.Vector3();
          camera.getWorldDirection(forward);
          if (camToPin.dot(forward) > 0) {
            pinPos.project(camera);
            if (pinPos.z > -1 && pinPos.z < 1) {
              const screenX = (pinPos.x * 0.5 + 0.5) * window.innerWidth;
              const screenY = (-(pinPos.y * 0.5) + 0.5) * window.innerHeight;
              pinEl.style.left = screenX + 'px';
              pinEl.style.top = screenY + 'px';
              pinEl.style.display = 'inline-flex';
            } else {
              pinEl.style.display = 'none';
            }
          } else {
            pinEl.style.display = 'none';
          }
        }
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
