
    // ================================================================
    // V5 — GAMEPLAY THEO BẢN CHỐT (THIET_KE_V5_CHOT.md)
    // · Nút động từ = LỆNH DI CHUYỂN: bấm -> avatar tự đi tới điểm đứng
    //   chuẩn của trạm -> mở nhịp hành động. Thao tác tay hủy tự đi.
    // · Tiến trình DUY NHẤT: hàng cánh sen (V4.journey theo ROUTE).
    // · Thắp nhang: người chơi tự chạm TỪNG nhịp, không setTimeout tự chạy.
    // ================================================================
    const BOW_DUR = 2.3; // giây cho mỗi lạy (v6: chậm rãi, trang nghiêm)
    let bowAnim = 0, bowTotal = 0, bowHoldT = 0;
    function startBow(n) {
      bowAnim = BOW_DUR * n; bowTotal = n;
      ritualDimAdd('bow');
      if (n >= 3) playBell(); // chuông ngân mở nhịp lạy
    }
    let silenceLeft = 0, silenceDone = false;
    let currentStation = null;
    const ctxBtn = document.getElementById('btn-context');

    // ---- V6: UI mờ gần hết trong nhịp lễ (lạy / đứng lặng / hồi hướng / thắp nhang) ----
    const ritualReasons = new Set();
    function ritualDimAdd(r) { ritualReasons.add(r); document.body.classList.add('ritual-dim'); }
    function ritualDimRemove(r) { ritualReasons.delete(r); if (!ritualReasons.size) document.body.classList.remove('ritual-dim'); }
    function showQuiet() { document.getElementById('btn-quiet').classList.add('show'); }
    function hideQuiet() { document.getElementById('btn-quiet').classList.remove('show'); }
    document.getElementById('btn-quiet').addEventListener('click', () => {
      hideQuiet();
      ritualDimRemove('silence');
      if (currentStation) runStationAction(currentStation);
    });

    // ---- Lời của An (bong bóng, không bấm được) + giọng thu sẵn ----
    let anTimer = null;
    function sayAn(text, voiceKey) {
      const b = document.getElementById('an-bubble');
      document.getElementById('an-text').textContent = text;
      b.classList.add('show');
      if (voiceKey) playVoice(voiceKey);
      clearTimeout(anTimer);
      anTimer = setTimeout(() => b.classList.remove('show'), 8000);
    }

    // ---- Tiến trình: hàng cánh sen ----
    const ROUTE = ['gate', 'stall', 'adida', 'dilac', 'burner', 'hall', 'nirvana', 'tower'];
    function renderPetals() {
      document.querySelectorAll('#lotus-progress .petal').forEach(p => {
        const id = p.dataset.p;
        p.classList.toggle('done', !!V4.journey[id]);
        p.classList.toggle('next', !V4.journey[id] && ROUTE.find(x => !V4.journey[x]) === id);
      });
    }
    function routeComplete() { return ROUTE.every(id => V4.journey[id]); }
    function markStation(id) {
      if (V4.journey[id]) return;
      V4.journey[id] = true; saveV4(); renderPetals(); refreshVerb();
      if (routeComplete()) {
        document.body.classList.add('free');
        showToast('Đã đi trọn một vòng chùa. Từ đây, bạn cứ thong thả dạo sân chùa.');
      }
    }

    // ---- Tự đi (auto-walk) + vệt sen chỉ đường + vòng đích ----
    let autoWalk = null;
    let autoSpeedBase = 1.15; // tốc độ tự đi chuẩn (v6: đi chậm); kiểm thử headless tăng qua __v6debug
    let camOverride = null; // góc máy riêng cho sạp nhang (module_7 dùng)
    const trailMat = new THREE.LineBasicMaterial({ color: 0xC9962E, transparent: true, opacity: 0.55 });
    let trailLine = null, destRing = null;
    function showTrail(pts) {
      hideTrail();
      const v = pts.map(p => new THREE.Vector3(p[0], 0.22, p[1]));
      trailLine = new THREE.Line(new THREE.BufferGeometry().setFromPoints(v), trailMat);
      scene.add(trailLine);
      const last = pts[pts.length - 1];
      destRing = new THREE.Mesh(new THREE.RingGeometry(0.68, 0.95, 36),
        new THREE.MeshBasicMaterial({ color: 0xC9962E, transparent: true, opacity: 0.9, side: THREE.DoubleSide }));
      destRing.rotation.x = -Math.PI / 2;
      destRing.position.set(last[0], 0.07, last[1]);
      scene.add(destRing);
    }
    function hideTrail() {
      if (trailLine) { scene.remove(trailLine); trailLine.geometry.dispose(); trailLine = null; }
      if (destRing) { scene.remove(destRing); destRing.geometry.dispose(); destRing = null; }
    }
    function startAutoWalk(station) {
      const path = [];
      (station.via || []).forEach(p => path.push({ x: p[0], z: p[1] }));
      path.push({ x: station.pos[0], z: station.pos[1] });
      autoWalk = { path, station };
      player.target = null;
      showTrail([[player.pos.x, player.pos.z]].concat(path.map(p => [p.x, p.z])));
    }
    function cancelAutoWalk() { if (autoWalk) { autoWalk = null; hideTrail(); } }

    // ---- Trạm (thứ tự MỚI theo nghiên cứu đi chùa thật) ----
    const STATIONS = [
      { id: 'gate', route: true, name: 'Cổng Tam Quan — Phương Tiện', verb: 'Vào cổng',
        an: 'Cổng Phương Tiện — một trong hai cổng tam quan của chùa. Theo phép, khách đi cửa bên; cửa giữa dành cho chư Tăng.',
        pos: [28, 44.6], r: 3.5, via: [],
        action: () => {
          sayAn('An chào bạn. An đang đứng trước cổng Phương Tiện, chùa Vĩnh Tràng. An sẽ đi cùng bạn một vòng chùa, thong thả.', 's0_chao');
          markStation('gate');
        } },
      { id: 'stall', route: true, name: 'Sạp nhang hoa (ngoài cổng)', verb: 'Chuẩn bị nhang hoa',
        an: 'Sạp nhang hoa ở ngoài cổng — nhang và hoa lễ đều mua ở đây.',
        pos: [31.6, 45.4], r: 3.2, via: [[29.8, 45.8]],
        action: () => openStall() },
      { id: 'adida', route: true, name: 'Phật A Di Đà', verb: 'Vái A Di Đà', voice: 's1_adida',
        an: 'Tượng Phật A Di Đà, cao mười tám mét trên bệ cao bảy mét, khánh thành năm 2008. Trước tượng chỉ vái; nhang chỉ thắp ở lư giữa sân.',
        pos: [-14, 23.2], r: 3.5, via: [[28, 40.6], [28, 36.5], [8, 31], [-6, 27.5]],
        action: () => { startBow(1); playMokugyo(); showToast('Nam mô A Di Đà Phật.'); markStation('adida'); } },
      { id: 'dilac', route: true, name: 'Phật Di Lặc', verb: 'Vái Di Lặc', voice: 's4_dilac',
        an: 'Tượng Phật Di Lặc, khánh thành năm 2010, cao khoảng hai mươi mét, nặng hơn hai trăm năm mươi tấn.',
        pos: [-24, 6], r: 3.5, via: [[-19, 16], [-22, 9]],
        action: () => { startBow(1); playMokugyo(); showToast('Nam mô Di Lặc Tôn Phật.'); markStation('dilac'); } },
      { id: 'quanam', route: false, name: 'Đài Quan Âm', verb: 'Vái Quan Âm',
        an: 'Đài Quan Thế Âm Bồ Tát trong hoa viên, bên ao sen.',
        pos: [-26, 25.6], r: 3, via: [],
        action: () => { startBow(1); playMokugyo(); showToast('Nam mô Quan Thế Âm Bồ Tát.'); V4.journey.quanam = true; saveV4(); } },
      { id: 'burner', route: true, name: 'Lư hương giữa sân', verb: 'Tới thắp nhang',
        an: 'Lư hương giữa sân. Cả buổi lễ, nhang chỉ thắp ở đây một lần, châm từ đèn dầu bên cạnh lư.',
        pos: [25.3, 13.7], r: 5.2, via: [[-16, 3.6], [8, 3.6], [19, 8.5], [22.5, 16.5]],
        action: () => openIncense() },
      { id: 'hall', route: true, name: 'Chánh điện Vĩnh Tràng', verb: 'Vào chánh điện',
        an: 'Chánh điện Vĩnh Tràng. Cửa giữa dành cho chư Tăng — khách vào cửa bên phía tây, bỏ dép ở thềm.',
        pos: [17.5, 6.8], r: 3, via: [[21, 9.5]],
        action: () => {
          sayAn('Vào cửa bên. Dép để ở thềm. Trong điện đi nhẹ, nói khẽ.');
          enterInterior();
        } },
      { id: 'to', route: false, inside: true, name: 'Điện thờ Tổ', verb: 'Lễ Tổ',
        an: 'Điện thờ Tổ. Theo phép, vào điện lễ Tổ trước, rồi mới lạy Phật.',
        pos: [290.8, 304], r: 3.2, via: [],
        action: () => {
          startBow(1); playMokugyo();
          V4.journey.to = true; saveV4();
          sayAn('Đã lễ Tổ. Mời ra trước bàn Tam Bảo, lạy Phật ba lạy.');
          refreshVerb();
        } },
      { id: 'in', route: false, inside: true, name: 'Bàn Tam Bảo', verb: 'Lạy Phật — 3 lạy',
        an: 'Bàn Tam Bảo. Lạy ở bồ đoàn chếch phía trước, không đứng chắn giữa lối đi. Trên trần là những khoanh nhang treo đang cháy.',
        pos: [300, 290.5], r: 4, via: [],
        action: () => {
          if (V4.journey.hall) { if (window.openChant) window.openChant(); return; }
          startBow(3); playMokugyo();
          playVoice('s3_lay_phat');
          showToast('Đã lạy Phật ba lạy.');
          markStation('hall');
          sayAn('Lạy xong. Có thể nán lại niệm kinh một thời ngắn, hoặc đi vòng hữu nhiễu quanh điện.');
        } },
      { id: 'huunhieu', route: false, inside: true, name: 'Hữu nhiễu quanh điện', verb: 'Đi vòng hữu nhiễu',
        an: 'Hữu nhiễu: đi vòng quanh điện theo phía tay phải, chậm rãi, không đi ngang qua trước người đang lạy.',
        pos: [300.5, 317.5], r: 3, via: [[306.5, 289], [307.5, 297], [303, 310]],
        action: () => {
          V4.journey.huunhieu = true; saveV4();
          sayAn('Bên phải là chuông Pháp Bảo — cao một mét hai, nặng một trăm năm mươi ký. Chuông chỉ thỉnh trong đại lễ.');
          refreshVerb();
        } },
      { id: 'inexit', route: false, inside: true, name: 'Cửa ra sân', verb: 'Ra sân chùa',
        an: 'Cửa ra sân. Phía sau là Phật nằm và bảo tháp.',
        pos: [300, 319.8], r: 2.5, via: [],
        action: () => exitInterior() },
      { id: 'nirvana', route: true, name: 'Phật Niết Bàn', verb: 'Vái Phật nằm', voice: 's5_nirvana',
        an: 'Tượng Phật nhập Niết Bàn, dài khoảng ba mươi hai mét, dựng năm 2013. Nơi đây tĩnh lặng — đứng yên một lát rồi mới vái.',
        pos: [12, -39.3], r: 7.5, via: [[2, -2], [4, -20], [8, -32]],
        action: () => {
          if (silenceLeft > 0) { showToast('Đang trong phút đứng lặng.'); return; }
          startBow(1); playMokugyo(); showToast('Nam mô Bổn Sư Thích Ca Mâu Ni Phật.'); markStation('nirvana');
        } },
      { id: 'tower', route: true, name: 'Bảo tháp Thất Phật', verb: 'Lên bảo tháp',
        an: 'Bảo tháp Thất Phật — dựng năm 2015, cao ba mươi lăm mét, bảy tầng thờ bảy vị Phật. Vườn tháp Tổ là khu riêng, ở phía sau.',
        pos: [-2, -35.3], r: 3.5, via: [[2, -34]],
        action: () => { playVoice('s6_hoi_huong'); doHoiHuong(); markStation('tower'); } },
      { id: 'merit', route: false, name: 'Thùng công đức', verb: 'Tùy tâm công đức',
        an: 'Thùng công đức. Tấm lòng tùy tâm, không có mức nào cả.',
        pos: [27.9, 7.0], r: 2.2, via: [],
        action: () => { playBell(); playVoice('merit_box'); showToast('Đã ghi nhận tấm lòng tùy tâm.'); } },
      { id: 'books', route: false, name: 'Phòng kinh sách', verb: 'Xem kinh sách',
        an: 'Phòng kinh sách ở phía sau, gần Giảng đường Huệ Đăng.',
        pos: [33, -8.4], r: 3, via: [],
        action: () => openBooks() },
      { id: 'shop', route: false, name: 'Quầy lưu niệm', verb: 'Xem quà lưu niệm',
        an: 'Quầy lưu niệm ở hông phải chùa, trên đường ra.',
        pos: [40, 34.3], r: 3.5, via: [],
        action: () => openModal('shop-modal') },
    ];
    function stationById(id) { return STATIONS.find(s => s.id === id); }
    function nextRouteStation() { const id = ROUTE.find(x => !V4.journey[x]); return id ? stationById(id) : null; }
    function interiorTarget() {
      if (!V4.journey.to) return stationById('to');
      if (!V4.journey.hall) return stationById('in');
      // Vừa lạy xong, còn đứng ở bàn Tam Bảo: nút mời Niệm kinh (không bắt buộc).
      // Rời trạm này để đi vòng hữu nhiễu thì nút chuyển theo trạm đích.
      if (currentStation && currentStation.id === 'in') return stationById('in');
      if (!V4.journey.huunhieu) return stationById('huunhieu');
      return stationById('inexit');
    }
    function pickVerbStation() {
      if (inside) return interiorTarget();
      const cs = currentStation;
      if (cs && !cs.inside && (!cs.route || !V4.journey[cs.id])) return cs;
      return nextRouteStation() || cs || null;
    }
    function refreshVerb() {
      const st = pickVerbStation();
      if (!st) { ctxBtn.textContent = 'Dạo sân chùa'; }
      else ctxBtn.textContent = (st.id === 'in' && V4.journey.hall) ? 'Niệm kinh (không bắt buộc)' : st.verb;
      refreshInfoBtn();
    }
    function runStationAction(st) { if (st && st.action) st.action(); }
    function doContextAction() {
      if (document.body.classList.contains('panel-open')) return;
      const st = pickVerbStation();
      if (!st) { showToast('Đã đi trọn một vòng chùa.'); return; }
      const d = Math.hypot(player.pos.x - st.pos[0], player.pos.z - st.pos[1]);
      if (d > 1.8) startAutoWalk(st);
      else { cancelAutoWalk(); runStationAction(st); }
    }
    ctxBtn.addEventListener('click', doContextAction);

    // ---- Thẻ "Tìm hiểu thêm" (v6) — CHỈ dùng dữ kiện đã kiểm chứng trong
    // NGHIEN_CUU_DI_CHUA_THAT.md / NGHIEN_CUU_AM_THANH.md; nguồn ghi cuối thẻ.
    // Thẻ nào không có nguồn thì không viết. ----
    const INFO_CARDS = {
      'cua-ben': { t: 'Vì sao vào chùa bằng cửa bên',
        b: 'Theo truyền thống, cửa giữa của tam quan — gọi là Cửa Không — dành cho Phật và các bậc tôn quý; người đi lễ vào bằng hai cửa bên. Tại chánh điện Vĩnh Tràng, cửa giữa hiện cũng đóng, khách vào ra bằng hai cửa tả hữu ở hai bên.',
        s: 'Nguồn: phatgiao.org.vn (“8 điều kiêng kỵ khi đi lễ chùa”); hướng dẫn tham quan chùa Vĩnh Tràng (bazantravel, travelmart).' },
      'tam-huong': { t: 'Một nén tâm hương, ba nén Tam Bảo',
        b: 'Một nén hương gọi là tâm hương: một nén nhưng bao hàm Ngũ Phần Hương — Giới hương, Định hương, Tuệ hương, Giải thoát hương và Giải thoát tri kiến hương. Ba nén tượng trưng Tam Bảo: Phật, Pháp, Tăng. Hướng dẫn của Giáo hội khuyên chỉ cần thắp một nén, nhiều nhất là ba nén; cá nhân đi lễ không thắp năm nén.',
        s: 'Nguồn: phatgiao.org.vn (“Vào chùa thắp hương như thế nào cho phù hợp”, “Ý nghĩa 3 nén hương”).' },
      'khong-thoi': { t: 'Vì sao không thổi tắt lửa',
        b: 'Khi lửa trên đầu nén hương bén lớn, không dùng miệng thổi tắt. Theo hướng dẫn trên phatgiao.org.vn: “vẩy nhẹ cho lửa nhỏ dần chứ không nên thổi tắt” — phẩy nhẹ cho lửa tắt dần, để hương cháy âm ỉ dâng lên Tam Bảo.',
        s: 'Nguồn: phatgiao.org.vn; bài giảng của Đại đức Thích Trúc Thái Minh (chuahanhduc.com).' },
      'huu-nhieu': { t: 'Hữu nhiễu là gì',
        b: 'Hữu nhiễu là phép di chuyển trong điện: đi giữ phía tay mặt của mình hướng về chánh điện, chậm rãi, và không đi ngang qua trước đầu người đang quỳ lạy.',
        s: 'Nguồn: “Tu Phật Nghi Thức Yếu Lược” (HT. Thích Từ Quang), dẫn tại daotrangtuphat.com.' },
      'le-to': { t: 'Vì sao lễ Tổ trước',
        b: 'Theo nghi thức lễ Phật, khi vào điện, Phật tử bỏ giày dép ở ngoài, lễ Tổ ở điện thờ Tổ trước, rồi mới lên chánh điện lễ Phật ba lạy.',
        s: 'Nguồn: “Tu Phật Nghi Thức Yếu Lược” (HT. Thích Từ Quang), dẫn tại daotrangtuphat.com.' },
      'that-phat': { t: 'Bảo tháp Thất Phật',
        b: 'Bảo tháp xây năm 2015, cao 35 mét, gồm một tầng trệt và bảy lầu. Tầng trệt thờ Thích Ca và Bồ Tát; mỗi lầu thờ một vị Phật cùng ba vị La Hán; tầng bảy tôn trí 15 bộ kinh Diệu Pháp Liên Hoa. Vườn tháp Tổ — nơi an trí tháp của chư vị hòa thượng tiền bối — là một khu riêng, yên tĩnh ở phía sau.',
        s: 'Nguồn: tư liệu giới thiệu chùa Vĩnh Tràng (pagoda.amazingvietnam.vn).' },
      'hoi-huong': { t: 'Hồi hướng là gì',
        b: 'Hồi hướng là hướng công đức của việc lành vừa làm về khắp tất cả chúng sanh — như bốn câu kệ vẫn đọc khi khép buổi lễ: “Nguyện đem công đức này, hướng về khắp tất cả, đệ tử và chúng sanh, đều trọn thành Phật đạo.”',
        s: 'Nguồn: phatgiao.org.vn (bài giải thích hồi hướng); kệ theo Nghi thức lễ Phật.' },
      'adida': { t: 'Tượng Phật A Di Đà',
        b: 'Tượng cao 18 mét, khánh thành năm 2008, đứng trên đài sen trong hoa viên. Trước tượng chỉ vái — nhang chỉ thắp một lần ở lư giữa sân, các nơi khác không thắp thêm.',
        s: 'Nguồn: tư liệu chùa Vĩnh Tràng; phatgiao.org.vn (quy tắc thắp hương).' },
      'dilac': { t: 'Tượng Phật Di Lặc',
        b: 'Tượng khánh thành năm 2010, cao khoảng 20 mét, nặng hơn 250 tấn. Dân gian có nếp xoa bụng tượng cầu lộc, nhưng theo các điều kiêng kỵ khi đi lễ chùa, không chỉ trỏ và không sờ vào tượng — tới trước tượng chỉ vái.',
        s: 'Nguồn: tư liệu chùa Vĩnh Tràng; phatgiao.org.vn (“8 điều kiêng kỵ khi đi lễ chùa”).' },
      'quanam': { t: 'Đài Quan Thế Âm',
        b: 'Trong hoa viên của chùa có đài Quan Thế Âm Bồ Tát, bên ao sen — một điểm dừng yên tĩnh trên đường vào chánh điện.',
        s: 'Nguồn: tư liệu giới thiệu chùa Vĩnh Tràng (travelmart; anphat.org).' },
      'nirvana': { t: 'Tượng Phật nhập Niết Bàn',
        b: 'Tượng dài khoảng 32 mét, khánh thành năm 2013. Du khách thường mô tả khu phía sau chùa là khoảng lặng yên tĩnh nhất trong khuôn viên — khách tới đây thường đứng lặng một lát trước khi vái.',
        s: 'Nguồn: tư liệu chùa Vĩnh Tràng; ghi nhận của du khách trên TripAdvisor.' },
    };
    const STATION_INFO = {
      gate: ['cua-ben'], stall: ['tam-huong'], adida: ['adida'], dilac: ['dilac'],
      quanam: ['quanam'], burner: ['tam-huong', 'khong-thoi'], hall: ['cua-ben'],
      to: ['le-to'], in: ['huu-nhieu'], huunhieu: ['huu-nhieu'],
      nirvana: ['nirvana'], tower: ['that-phat', 'hoi-huong'],
    };
    function refreshInfoBtn() {
      const btn = document.getElementById('btn-info');
      if (!btn) return;
      const ids = currentStation ? STATION_INFO[currentStation.id] : null;
      btn.classList.toggle('show', !!ids);
    }
    function openInfo() {
      const ids = currentStation ? STATION_INFO[currentStation.id] : null;
      if (!ids) return;
      const old = document.getElementById('info-modal'); if (old) old.remove();
      const secs = ids.map(id => { const c = INFO_CARDS[id]; return `<div class="info-sec"><h4>${c.t}</h4><p>${c.b}</p><div class="src">${c.s}</div></div>`; }).join('');
      const m = document.createElement('div');
      m.className = 'modal-overlay open'; m.id = 'info-modal'; m.style.zIndex = 57;
      m.innerHTML = `<div class="modal"><button class="modal-close">✕</button><div class="modal-title">Tìm hiểu thêm</div>${secs}<button class="btn-submit">Đóng</button></div>`;
      document.body.appendChild(m);
      const close = () => m.remove();
      m.querySelector('.modal-close').onclick = close;
      m.querySelector('.btn-submit').onclick = close;
      m.addEventListener('click', e => { if (e.target === m) close(); });
    }
    document.getElementById('btn-info').addEventListener('click', openInfo);
    function onEnterInterior() {
      sayAn('Vào điện bằng cửa bên, dép để ở thềm. Trong điện đi nhẹ, nói khẽ. Trước tiên, lễ Tổ ở điện thờ Tổ phía tây.');
      refreshVerb();
    }
    function onExitInterior() {
      if (!V4.journey.hall) sayAn('Chưa lạy Phật trong điện. Khi sẵn sàng, mời quay lại cửa bên phía tây.');
      else sayAn('Ra sân. Đi tiếp ra phía sau: Phật nằm, rồi Bảo tháp Thất Phật.');
      refreshVerb();
    }

    // ---- An đồng hành + vòng đích (gọi mỗi frame từ vòng lặp chính) ----
    function updateCompanion(dt, t) {
      const fwdX = Math.sin(player.yaw), fwdZ = Math.cos(player.yaw);
      const sideX = fwdZ, sideZ = -fwdX;
      let tx, tz;
      if (autoWalk) { tx = player.pos.x + fwdX * 0.6 + sideX * 1.25; tz = player.pos.z + fwdZ * 0.6 + sideZ * 1.25; }
      else { tx = player.pos.x - fwdX * 1.35 + sideX * 1.05; tz = player.pos.z - fwdZ * 1.35 + sideZ * 1.05; }
      const dx = tx - anState.pos.x, dz = tz - anState.pos.z;
      const d = Math.hypot(dx, dz);
      if (d > 0.12) {
        const sp = Math.min(d, 2.4 * dt * Math.max(1, d));
        anState.pos.x += (dx / d) * sp; anState.pos.z += (dz / d) * sp;
        const ty = Math.atan2(dx, dz);
        let dy = ty - anState.yaw;
        while (dy > Math.PI) dy -= Math.PI * 2;
        while (dy < -Math.PI) dy += Math.PI * 2;
        anState.yaw += dy * Math.min(1, dt * 10);
        anAv.setPose('Di bo'); // V7: model thật — đi bộ bằng action 'Di bo'
      } else {
        // Đứng yên: An quay mặt về trạm hiện tại (chỉ tay dẫn hướng)
        const st = pickVerbStation();
        if (st && !inside) anState.yaw = Math.atan2(st.pos[0] - anState.pos.x, st.pos[1] - anState.pos.z);
        anAv.setPose('Dung'); // V7: đứng chờ bằng action 'Dung'
      }
      anAv.group.position.x = anState.pos.x;
      anAv.group.position.z = anState.pos.z;
      anAv.group.rotation.y = anState.yaw;
      if (destRing) { const s = 1 + 0.13 * Math.sin(t * 3.2); destRing.scale.set(s, s, 1); }
      if (typeof lampFlame !== 'undefined' && lampFlame) { const f = 1 + 0.18 * Math.sin(t * 11); lampFlame.scale.set(f, f * 1.15, f); }
    }

    // ---- Sạp nhang hoa (MUA) ----
    let stallChoice = 0;
    function openStall() {
      if (V4.bought) { showToast('Đã có nhang và hoa rồi. Mời tới lư giữa sân thắp.'); return; }
      document.getElementById('stall-panel').classList.add('open');
      document.body.classList.add('panel-open');
      // V6: góc máy riêng cho sạp — đặt máy phía trước sạp để mái + biển không choán tiền cảnh
      camOverride = { x: 26.4, y: 2.1, z: 40.0, lx: 33.8, ly: 1.5, lz: 47.0 };
    }
    function closeStall() {
      document.getElementById('stall-panel').classList.remove('open');
      document.body.classList.remove('panel-open');
      camOverride = null;
    }
    function stallPick(n) {
      stallChoice = n;
      document.getElementById('stall-opt1').classList.toggle('sel', n === 1);
      document.getElementById('stall-opt3').classList.toggle('sel', n === 3);
      document.getElementById('stall-buy').disabled = false;
    }
    document.getElementById('stall-opt1').addEventListener('click', () => stallPick(1));
    document.getElementById('stall-opt3').addEventListener('click', () => stallPick(3));
    document.getElementById('stall-close').addEventListener('click', closeStall);
    document.getElementById('stall-buy').addEventListener('click', () => {
      if (!stallChoice) return;
      V4.bought = { sticks: stallChoice, flowers: true }; saveV4();
      playBell();
      playVoice('s0_nhan_nhang');
      showToast(`Đã mua bó ${stallChoice} nén nhang và hoa sen. Vào vái A Di Đà, Di Lặc, rồi thắp nhang ở lư sân.`);
      markStation('stall');
      closeStall();
    });

    // ---- Lễ thắp nhang: 4 NHỊP, người chơi tự chạm từng nhịp ----
    const incenseState = { step: 0, chosen: 0, bows: 0 };
    function openIncense() {
      if (V4.lit.main) { showToast('Lư sân đã có nhang đang cháy.'); return; }
      if (!V4.bought) {
        showToast('Chưa có nhang. Mời ghé sạp nhang hoa ngoài cổng mua trước.');
        startAutoWalk(stationById('stall'));
        return;
      }
      incenseState.step = 0; incenseState.chosen = 0; incenseState.bows = 0;
      document.getElementById('incense-panel').classList.add('open');
      document.body.classList.add('panel-open');
      ritualDimAdd('panel'); // nhịp lễ: UI xung quanh mờ đi
      playVoice('s2_thap_nhang');
      renderIncense();
    }
    function closeIncense() {
      document.getElementById('incense-panel').classList.remove('open');
      document.body.classList.remove('panel-open');
      ritualDimRemove('panel');
    }
    document.getElementById('incense-close').addEventListener('click', closeIncense);
    function incenseDots(step) {
      document.querySelectorAll('#incense-dots span').forEach((s, i) => {
        s.className = i < step ? 'done' : (i === step ? 'now' : '');
      });
    }
    function renderIncense() {
      const st = incenseState;
      const txt = document.getElementById('incense-text');
      const act = document.getElementById('incense-actions');
      const flame = document.getElementById('incense-flame');
      incenseDots(Math.min(st.step, 3));
      act.innerHTML = '';
      const mkBtn = (label, cls) => {
        const b = document.createElement('button');
        b.className = 'big-btn' + (cls ? ' ' + cls : '');
        b.textContent = label;
        act.appendChild(b);
        return b;
      };
      if (st.step === 0) {
        flame.innerHTML = '';
        txt.innerHTML = '<b>Nhịp 1 — Chọn số nén.</b> Một nén là <b>tâm hương</b>: tượng trưng tấm lòng, vẫn trọn lễ. Ba nén là <b>Tam Bảo</b>: Phật — Pháp — Tăng. (Cá nhân đi lễ chỉ thắp 1 hoặc 3 nén.)';
        const wrap = document.createElement('div'); wrap.className = 'opt-cards'; act.appendChild(wrap);
        const o1 = document.createElement('div'); o1.className = 'opt-card';
        o1.innerHTML = '<b>1 nén</b><small>Tâm hương</small>';
        o1.onclick = () => { incenseState.chosen = 1; incenseState.step = 1; renderIncense(); };
        wrap.appendChild(o1);
        const o3 = document.createElement('div'); o3.className = 'opt-card';
        if (V4.bought.sticks >= 3) {
          o3.innerHTML = '<b>3 nén</b><small>Tam Bảo</small>';
          o3.onclick = () => { incenseState.chosen = 3; incenseState.step = 1; renderIncense(); };
        } else {
          o3.style.opacity = '.45';
          o3.innerHTML = '<b>3 nén</b><small>Bó đã mua chỉ có một nén</small>';
        }
        wrap.appendChild(o3);
      } else if (st.step === 1) {
        flame.innerHTML = '<span class="flame-dot dim"></span>';
        txt.innerHTML = '<b>Nhịp 2 — Châm nhang từ đèn dầu</b> bên cạnh lư (không dùng bật lửa, không châm từ nhang người khác).';
        mkBtn('Châm nhang vào đèn dầu').onclick = () => {
          playFire();
          flame.innerHTML = '<span class="flame-dot"></span>';
          txt.innerHTML = 'Lửa bùng lên đầu nhang — <b>không thổi</b>. Phẩy nhẹ tay cho lửa tắt, chỉ để khói thơm. <b>Giữ nhẹ nút dưới đây</b> như đang phẩy tay.';
          act.innerHTML = '';
          const hold = mkBtn('Phẩy nhẹ cho tắt lửa (giữ nhẹ)', 'gold');
          const ring = document.createElement('div'); ring.className = 'hold-ring';
          ring.innerHTML = '<i></i>'; ring.style.display = 'block'; act.appendChild(ring);
          const bar = ring.querySelector('i');
          // Tiến độ tính theo THỜI GIAN GIỮ THẬT (không đếm tick) — bền với máy chậm/fps thấp
          let iv = null, holdT0 = 0;
          const curProg = () => holdT0 ? Math.min(1, (performance.now() - holdT0) / 900) : 0;
          const stop = () => {
            if (iv) { clearInterval(iv); iv = null; }
            const prog = curProg();
            holdT0 = 0;
            if (prog >= 0.95) { incenseState.step = 2; renderIncense(); return; }
            if (prog > 0.05 && prog < 0.4) showToast('Đó là thổi mạnh. Phẩy nhẹ thôi, giữ đều tay.');
            bar.style.width = '0%';
          };
          hold.addEventListener('pointerdown', e => {
            e.preventDefault();
            if (iv) return;
            holdT0 = performance.now();
            iv = setInterval(() => { bar.style.width = (curProg() * 100) + '%'; if (curProg() >= 1) stop(); }, 40);
          });
          hold.addEventListener('pointerup', stop);
          hold.addEventListener('pointerleave', stop);
        };
      } else if (st.step === 2) {
        flame.innerHTML = '<span class="flame-dot"></span>';
        txt.innerHTML = `<b>Nhịp 3 — Cầm nhang bằng hai tay, vái 3 vái.</b> Đã vái: <b>${st.bows}/3</b>`;
        mkBtn('Vái một vái').onclick = () => {
          startBow(1); playMokugyo();
          incenseState.bows++;
          if (incenseState.bows >= 3) { incenseState.step = 3; }
          renderIncense();
        };
      } else if (st.step === 3) {
        flame.innerHTML = '<span class="flame-dot"></span>';
        txt.innerHTML = '<b>Nhịp 4 — Cắm nhang vào giữa lư</b> bằng hai tay. Bạn đang đứng chếch sang một bên — đúng phép, không đứng chắn giữa lư.';
        mkBtn('Cắm nhang vào giữa lư').onclick = () => {
          playerAv.playOnce('Thắp nhang'); // V7: action cắm nhang của model thật
          burnerSticks.visible = true;
          if (incenseState.chosen === 1) {
            burnerSticks.children.forEach((c, i) => { c.visible = (i === 2 || i === 3); });
          } else {
            burnerSticks.children.forEach(c => { c.visible = true; });
          }
          smokeMain.setActive(true);
          V4.lit.main = true; saveV4();
          playBell();
          incenseState.step = 4;
          markStation('burner');
          renderIncense();
        };
      } else {
        document.querySelectorAll('#incense-dots span').forEach(s => s.className = 'done');
        flame.innerHTML = '<span class="flame-dot"></span>';
        txt.innerHTML = 'Đã thắp nhang — khói hương bay lên. Lư sẽ cháy suốt buổi hôm nay. Giờ vào chánh điện, cửa bên phía tây.';
        mkBtn('Đã xong — đóng').onclick = closeIncense;
      }
    }

    // ---- Hồi hướng ở bảo tháp + ảnh Dấu ấn hành trình ----
    function doHoiHuong() {
      playBell();
      ritualDimAdd('hoihuong'); // nhịp khép buổi: UI mờ, chỉ còn tấm thẻ kệ
      const cv = document.createElement('canvas'); cv.width = 640; cv.height = 800;
      const ctx = cv.getContext('2d');
      ctx.fillStyle = '#FFF6E5'; ctx.fillRect(0, 0, 640, 800);
      ctx.strokeStyle = '#C9962E'; ctx.lineWidth = 8; ctx.strokeRect(20, 20, 600, 760);
      ctx.fillStyle = '#1C5A34'; ctx.font = 'bold 44px Georgia, serif'; ctx.textAlign = 'center';
      ctx.fillText('DẤU ẤN HÀNH TRÌNH', 320, 170);
      ctx.font = '28px Georgia, serif'; ctx.fillStyle = '#4A3222';
      ctx.fillText('Chùa Vĩnh Tràng — ' + new Date().toLocaleDateString('vi-VN'), 320, 230);
      const names = { gate: 'Vào cổng Phương Tiện', stall: 'Chuẩn bị nhang hoa', adida: 'Vái A Di Đà', dilac: 'Vái Di Lặc', burner: 'Thắp nhang lư sân', hall: 'Lạy Phật chánh điện', nirvana: 'Vái Phật nằm', tower: 'Hồi hướng ở bảo tháp' };
      let y = 300;
      ROUTE.forEach(k => {
        ctx.fillStyle = V4.journey[k] ? '#1C5A34' : '#B9A98F';
        ctx.fillText((V4.journey[k] ? '✓ ' : '▢ ') + names[k], 320, y); y += 48;
      });
      ctx.font = 'italic 24px Georgia, serif'; ctx.fillStyle = '#6B4226';
      ctx.fillText('Nguyện đem công đức này, hướng về khắp tất cả,', 320, 700);
      ctx.fillText('đệ tử và chúng sanh, đều trọn thành Phật đạo.', 320, 736);
      const url = cv.toDataURL('image/png');
      const m = document.createElement('div');
      m.className = 'modal-overlay open'; m.style.zIndex = 55;
      m.innerHTML = `<div class="modal" style="text-align:center">
        <div class="modal-title">Hồi hướng</div>
        <div class="modal-desc">Nguyện đem công đức này,<br>Hướng về khắp tất cả,<br>Đệ tử và chúng sanh,<br>Đều trọn thành Phật đạo.</div>
        <img src="${url}" style="width:100%;border-radius:12px;border:1.5px solid var(--gold)">
        <a href="${url}" download="dau-an-hanh-trinh.png" class="btn-submit" style="display:block;text-decoration:none;text-align:center;margin-top:10px">Lưu ảnh Dấu ấn mang về</a>
        <button class="btn-submit alt" style="margin-top:8px">Đóng</button></div>`;
      const closeHH = () => { ritualDimRemove('hoihuong'); m.remove(); };
      m.querySelector('.btn-submit.alt').onclick = closeHH;
      m.addEventListener('click', e => { if (e.target === m) closeHH(); });
      document.body.appendChild(m);
    }

    // ---- Phòng kinh sách (điểm dừng riêng ở phía sau) ----
    function openBooks() {
      const m = document.createElement('div');
      m.className = 'modal-overlay open'; m.style.zIndex = 55;
      m.innerHTML = `<div class="modal"><button class="modal-close">✕</button>
        <div class="modal-title">Phòng kinh sách</div>
        <div class="modal-desc">Phòng kinh sách ở phía sau khuôn viên, gần giảng đường Huệ Đăng. Kinh sách ở đây để <b>gieo duyên</b> — ai cần thì thỉnh về đọc, không buôn bán trong điện.</div>
        <div class="book-item"><span class="thumb">Phổ</span><div><b>Kinh Phổ Môn</b><small>Phẩm Quan Thế Âm — gieo duyên</small></div></div>
        <div class="book-item"><span class="thumb">Bi</span><div><b>Chú Đại Bi</b><small>Bản in chữ lớn, dễ đọc — gieo duyên</small></div></div>
        <div class="book-item"><span class="thumb">Đà</span><div><b>Kinh A Di Đà</b><small>Kèm phần sớ lược Tịnh Độ — gieo duyên</small></div></div>
        <div class="modal-desc" style="margin-top:8px">Muốn học sâu thêm, mở mục <b>Bài giảng Huệ Đăng</b> trong Khám phá.</div>
      </div>`;
      m.querySelector('.modal-close').onclick = () => m.remove();
      m.addEventListener('click', e => { if (e.target === m) m.remove(); });
      document.body.appendChild(m);
    }

    // ---- Bản đồ tĩnh (KHÔNG nhảy camera — chỉ xem vị trí) ----
    let mapTimer = null;
    function buildMap() {
      const old = document.getElementById('map-modal'); if (old) old.remove();
      const SX = x => (x + 38) / 92 * 460, SY = z => (z + 42) / 95 * 380;
      const dot = (x, z, label, col) =>
        `<circle cx="${SX(x)}" cy="${SY(z)}" r="6" fill="${col || '#C9962E'}" stroke="#fff" stroke-width="2"/>` +
        `<text x="${SX(x)}" y="${SY(z) - 10}" font-size="11" font-weight="bold" fill="#4A3222" text-anchor="middle">${label}</text>`;
      const svg = `<svg viewBox="0 0 460 380" style="width:100%;display:block">
        <rect x="2" y="2" width="456" height="376" rx="14" fill="#EFE8CE" stroke="#C9962E" stroke-width="2"/>
        <rect x="${SX(-4.9)}" y="${SY(8.5)}" width="${SX(14.9) - SX(-4.9)}" height="${SY(23.5) - SY(8.5)}" fill="#7A9B6E" rx="6"/>
        <rect x="${SX(31.1)}" y="${SY(8.5)}" width="${SX(50.9) - SX(31.1)}" height="${SY(23.5) - SY(8.5)}" fill="#7A9B6E" rx="6"/>
        <rect x="${SX(9)}" y="${SY(-13)}" width="${SX(37) - SX(9)}" height="${SY(1.2) - SY(-13)}" fill="#D9A441" rx="4"/>
        <text x="${SX(23)}" y="${SY(-4)}" font-size="12" font-weight="bold" fill="#7E2A22" text-anchor="middle">CHÁNH ĐIỆN</text>
        <rect x="${SX(18.5)}" y="${SY(-1)}" width="${SX(27.5) - SX(18.5)}" height="${SY(42) - SY(-1)}" fill="#D8C9A3"/>
        ${dot(-14, 27, 'A Di Đà')} ${dot(-24.5, -3, 'Di Lặc')} ${dot(-27, 21, 'Quan Âm')}
        ${dot(23, 11, 'Lư sân', '#C0392B')} ${dot(12, -47, 'Phật nằm')} ${dot(-2, -41, 'Bảo tháp')}
        ${dot(44, -20, 'Giảng đường')} ${dot(33, -12, 'Kinh sách')} ${dot(40, 38, 'Lưu niệm')}
        ${dot(34, 47, 'Sạp nhang')} ${dot(23, 40.7, 'Cổng Phương Tiện', '#1C5A34')} ${dot(45, 40.7, 'Cổng Tịnh Độ', '#1C5A34')}
      </svg>`;
      const m = document.createElement('div');
      m.className = 'modal-overlay open'; m.id = 'map-modal'; m.style.zIndex = 56;
      m.innerHTML = `<div class="modal"><button class="modal-close">✕</button>
        <div class="modal-title">Sơ đồ chùa Vĩnh Tràng</div>
        <div class="modal-desc">Chấm vàng là chỗ bạn đang đứng. Cứ đi theo nút động từ — An dẫn đường.</div>
        <div id="map-wrap">${svg}<div id="map-dot"></div></div></div>`;
      document.body.appendChild(m);
      const upd = () => {
        const d = document.getElementById('map-dot'); if (!d) return;
        const wrap = document.getElementById('map-wrap');
        d.style.left = (SX(player.pos.x) / 460 * 100) + '%';
        d.style.top = (SY(player.pos.z) / 380 * 100) + '%';
        if (wrap) wrap.style.position = 'relative';
      };
      upd();
      mapTimer = setInterval(upd, 500);
      const close = () => { clearInterval(mapTimer); m.remove(); };
      m.querySelector('.modal-close').onclick = close;
      m.addEventListener('click', e => { if (e.target === m) close(); });
    }
    document.getElementById('btn-map').addEventListener('click', buildMap);

    // ---- Cửa hàng lưu niệm (3 nhóm — giá CHỈ ở đây) ----
    const SHOP_PRODUCTS = [
      { id: 'sotay', cat: 'souvenir', name: 'Sổ tay hoa sen', desc: 'Bìa cứng, giấy láng, 120 trang', price: 89000 },
      { id: 'buuthiep', cat: 'souvenir', name: 'Bưu thiếp chùa (bộ 5)', desc: 'Ảnh chùa Vĩnh Tràng in đẹp', price: 45000 },
      { id: 'tranh', cat: 'souvenir', name: 'Tranh chùa Vĩnh Tràng', desc: 'Khổ A4, giấy mỹ thuật', price: 120000 },
      { id: 'tranghat', cat: 'study', name: 'Tràng hạt gỗ', desc: 'Gỗ trầm, 108 hạt', price: 150000 },
      { id: 'chuoihat', cat: 'study', name: 'Chuỗi hạt', desc: 'Đeo tay, gỗ đàn hương', price: 150000 },
      { id: 'kinhsach', cat: 'study', name: 'Kinh sách (bộ)', desc: 'Kinh Phổ Môn + Chú Đại Bi', price: 99000 },
      { id: 'tuong3d', cat: '3d', name: 'Tượng Phật 3D', desc: 'In 3D, cao 15cm', price: 220000 },
      { id: 'mohinh', cat: '3d', name: 'Mô hình chùa mini', desc: 'Chùa Vĩnh Tràng thu nhỏ', price: 350000 },
      { id: 'mo3d', cat: '3d', name: 'Mõ gỗ 3D', desc: 'Mõ tụng kinh mini', price: 180000 },
    ];
    const CART_KEY = 'chuaOnlineV5Cart';
    let cart = [];
    try { const raw = localStorage.getItem(CART_KEY); if (raw) cart = JSON.parse(raw); } catch (e) {}
    function saveCart() { try { localStorage.setItem(CART_KEY, JSON.stringify(cart)); } catch (e) {} updateCartBadge(); }
    function updateCartBadge() {
      const n = cart.reduce((a, c) => a + c.qty, 0);
      const el = document.getElementById('cart-count'); if (el) el.textContent = n;
    }
    function fmtVND(n) { return n.toLocaleString('vi-VN') + 'đ'; }
    let shopCat = 'souvenir';
    function renderShop() {
      const list = document.getElementById('shop-list'); if (!list) return;
      list.innerHTML = '';
      SHOP_PRODUCTS.filter(p => p.cat === shopCat).forEach(p => {
        const div = document.createElement('div');
        div.className = 'shop-item';
        div.innerHTML = `<div class="thumb">${p.name.charAt(0)}</div><div class="info"><b>${p.name}</b><small>${p.desc}</small></div><div class="price">${fmtVND(p.price)}</div>`;
        const btn = document.createElement('button');
        btn.className = 'add'; btn.textContent = 'Thêm';
        btn.onclick = () => {
          const it = cart.find(c => c.id === p.id);
          if (it) it.qty++; else cart.push({ id: p.id, qty: 1 });
          saveCart(); showToast(`Đã thêm “${p.name}” vào giỏ.`);
        };
        div.appendChild(btn);
        list.appendChild(div);
      });
    }
    document.querySelectorAll('.shop-tab').forEach(t => t.addEventListener('click', () => {
      shopCat = t.dataset.cat;
      document.querySelectorAll('.shop-tab').forEach(x => x.classList.toggle('active', x === t));
      renderShop();
    }));
    renderShop(); updateCartBadge();
    document.getElementById('btn-view-cart').addEventListener('click', () => {
      if (!cart.length) { showToast('Giỏ hàng đang trống — chọn món rồi bấm “Thêm”.'); return; }
      const lines = cart.map(c => {
        const p = SHOP_PRODUCTS.find(x => x.id === c.id);
        return `• ${p.name} × ${c.qty} — ${fmtVND(p.price * c.qty)}`;
      });
      const total = cart.reduce((a, c) => a + SHOP_PRODUCTS.find(x => x.id === c.id).price * c.qty, 0);
      const m = document.createElement('div');
      m.className = 'modal-overlay open'; m.style.zIndex = 55;
      m.innerHTML = `<div class="modal"><button class="modal-close">✕</button>
        <div class="modal-title">Giỏ hàng của bạn</div>
        <div class="modal-desc">${lines.join('<br>')}<br><b>Tổng: ${fmtVND(total)}</b><br>Giao tận nhà, kiểm tra rồi thanh toán (COD).</div>
        <button class="btn-submit">Đặt hàng ngay</button></div>`;
      m.querySelector('.modal-close').onclick = () => m.remove();
      m.querySelector('.btn-submit').onclick = () => { m.remove(); openCheckout(); };
      m.addEventListener('click', e => { if (e.target === m) m.remove(); });
      document.body.appendChild(m);
    });
    function openCheckout() {
      const total = cart.reduce((a, c) => a + SHOP_PRODUCTS.find(x => x.id === c.id).price * c.qty, 0);
      document.getElementById('order-item-title').textContent = 'Đặt hàng giỏ lưu niệm';
      document.getElementById('order-item-desc').textContent =
        cart.map(c => `${SHOP_PRODUCTS.find(x => x.id === c.id).name} × ${c.qty}`).join(', ') +
        ` — Tổng ${fmtVND(total)}. Giao tận nhà, kiểm tra rồi thanh toán (COD).`;
      openModal('order-modal');
    }
    document.getElementById('btn-checkout').addEventListener('click', () => {
      if (!cart.length) { showToast('Giỏ hàng đang trống — chọn món rồi bấm “Thêm”.'); return; }
      openCheckout();
    });
    document.getElementById('btn-submit-order').addEventListener('click', () => {
      const name = document.getElementById('order-name').value.trim();
      const phone = document.getElementById('order-phone').value.trim();
      const addr = document.getElementById('order-address').value.trim();
      if (name && phone && addr && cart.length) { cart = []; saveCart(); }
    });

    // ---- Cài đặt + nav + khay khám phá ----
    const brightnessSlider = document.getElementById('brightness-slider');
    brightnessSlider.value = V4.brightness || 1.0;
    renderer.toneMappingExposure = 1.02 * (V4.brightness || 1.0);
    brightnessSlider.addEventListener('input', () => {
      V4.brightness = parseFloat(brightnessSlider.value); saveV4();
      renderer.toneMappingExposure = 1.02 * V4.brightness;
    });
    document.getElementById('btn-settings').addEventListener('click', () => {
      document.getElementById('settings-pop').classList.toggle('open');
    });
    document.getElementById('btn-profile-change').addEventListener('click', () => {
      document.getElementById('settings-pop').classList.remove('open');
      if (window.openProfiles) window.openProfiles();
    });
    const tray = document.getElementById('explore-tray');
    document.getElementById('nav-explore').addEventListener('click', () => tray.classList.toggle('open'));
    document.getElementById('nav-learn').addEventListener('click', () => { tray.classList.remove('open'); if (window.openLessons) window.openLessons(); });
    document.getElementById('nav-account').addEventListener('click', () => { tray.classList.remove('open'); if (window.openProfiles) window.openProfiles(); });
    document.getElementById('tray-chant').addEventListener('click', () => { tray.classList.remove('open'); if (window.openChant) window.openChant(); });
    document.getElementById('tray-lessons').addEventListener('click', () => { tray.classList.remove('open'); if (window.openLessons) window.openLessons(); });
    document.getElementById('tray-fortune').addEventListener('click', () => { tray.classList.remove('open'); if (window.__openFortune) window.__openFortune(); });
    document.getElementById('tray-books').addEventListener('click', () => { tray.classList.remove('open'); openBooks(); });
    document.getElementById('tray-shop').addEventListener('click', () => { tray.classList.remove('open'); openModal('shop-modal'); });
    document.getElementById('tray-so').addEventListener('click', () => { tray.classList.remove('open'); openModal('so-modal'); });

    // ---- Khởi tạo ----
    renderPetals();
    if (routeComplete()) document.body.classList.add('free');
    refreshVerb();
    setTimeout(() => sayAn('Nam mô A Di Đà Phật. An sẽ đi cùng bạn một vòng chùa. Mời bấm nút “Vào cổng”.'), 900);

    // Debug/kiem thu (chi doc trang thai + di bo thu cong)
    window.__v6debug = {
      state: () => ({ pos: [player.pos.x, player.pos.z], inside, journey: V4.journey, lit: V4.lit, bought: V4.bought, verb: ctxBtn.textContent, station: currentStation ? currentStation.id : null, cartQty: cart.reduce((a, c) => a + c.qty, 0), silenceLeft, silenceDone, ritualDim: document.body.classList.contains('ritual-dim') }),
      walkTo: (x, z) => { cancelAutoWalk(); player.target = { x, z }; },
      setSpeed: s => { player.speed = s; },
      setAutoSpeed: s => { autoSpeedBase = s; },
      station: st => currentStation === st,
    };
    window.__v5debug = window.__v6debug; // tương thích ngược
