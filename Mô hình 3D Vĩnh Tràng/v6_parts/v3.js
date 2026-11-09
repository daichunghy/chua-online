/* ============================================================
   CHÙA ONLINE V3 — lớp tính năng bổ sung trên V2:
   1) Chọn profile nhân vật (nữ / nam / trẻ em) + Chú tiểu An chào theo mục đích
   2) NIỆM KINH: karaoke chữ theo câu, mõ/chuông WebAudio, 3 gói 5/10/20 phút
      (cấu trúc theo Thiền môn nhật tụng — hồ sơ research mục 3)
   3) BÀI GIẢNG Giảng đường Huệ Đăng: 4 lộ trình, bài mẫu đủ 6 phần
      (nghe/tóm tắt/thí dụ/quiz/suy ngẫm/hành trì) — hồ sơ research mục 2
   Lưu trữ: khóa riêng 'chuaOnlineV3' (không đụng khóa V2).
   Thuật ngữ hiển thị dùng "dấu ấn" theo khuyến nghị hồ sơ mục 0.3.
   ============================================================ */
(function () {
  'use strict';
  var KEY = 'chuaOnlineV3';
  var S = { profile: null, purpose: '', chantDone: 0, chantMinutes: 0, lessonsDone: {}, reflections: {} };
  try { var raw = localStorage.getItem(KEY); if (raw) S = Object.assign(S, JSON.parse(raw)); } catch (e) {}
  function save() { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) {} }

  /* ---------- WebAudio: chuông + mõ (tổng hợp, không cần file) ---------- */
  var AC = null;
  function ctx() { if (!AC) { try { AC = new (window.AudioContext || window.webkitAudioContext)(); } catch (e) {} } if (AC && AC.state === 'suspended') AC.resume(); return AC; }
  function bell(vol) {
    var ac = ctx(); if (!ac) return; var t = ac.currentTime;
    [523.25, 783.99, 1046.5].forEach(function (f, i) {
      var o = ac.createOscillator(), g = ac.createGain();
      o.type = 'sine'; o.frequency.value = f;
      g.gain.setValueAtTime((vol || 0.15) / (i + 1), t);
      g.gain.exponentialRampToValueAtTime(0.0001, t + 2.2);
      o.connect(g); g.connect(ac.destination); o.start(t); o.stop(t + 2.3);
    });
  }
  function mo() {
    var ac = ctx(); if (!ac) return; var t = ac.currentTime;
    var o = ac.createOscillator(), g = ac.createGain();
    o.type = 'triangle'; o.frequency.setValueAtTime(720, t);
    o.frequency.exponentialRampToValueAtTime(320, t + 0.09);
    g.gain.setValueAtTime(0.22, t); g.gain.exponentialRampToValueAtTime(0.0001, t + 0.13);
    o.connect(g); g.connect(ac.destination); o.start(t); o.stop(t + 0.14);
  }

  /* ---------- CSS ---------- */
  var css = document.createElement('style');
  css.textContent = [
    '.v3-bar{position:fixed;left:12px;bottom:12px;z-index:60;display:flex;gap:8px;flex-wrap:wrap}',
    '.v3-btn{cursor:pointer;border:none;border-radius:999px;padding:10px 16px;font-size:14px;font-weight:600;background:#7a4a21;color:#ffe9bd;box-shadow:0 4px 14px rgba(0,0,0,.35)}',
    '.v3-btn.alt{background:#f3e3bb;color:#5b3a17}',
    '.v3-modal{position:fixed;inset:0;z-index:80;background:rgba(20,12,4,.66);display:flex;align-items:center;justify-content:center;padding:14px}',
    '.v3-card{background:#fffaf0;border-radius:18px;max-width:760px;width:100%;max-height:88vh;overflow:auto;padding:22px;color:#33241a;font-family:inherit}',
    '.v3-card h2{margin:0 0 6px;color:#7a4a21}.v3-card h3{color:#7a4a21;margin:16px 0 6px}',
    '.v3-profiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin-top:12px}',
    '.v3-prof{border:2px solid #e5d3a8;border-radius:14px;padding:14px;cursor:pointer;background:#fff}',
    '.v3-prof.sel{border-color:#b07d2b;background:#fdf3d7}',
    '.v3-prof .emoji{font-size:40px}.v3-prof small{color:#7a6a55}',
    '.v3-close{float:right;cursor:pointer;border:none;background:#e8dcc0;border-radius:999px;width:32px;height:32px;font-size:16px}',
    '.v3-sent{padding:7px 10px;border-radius:10px;margin:4px 0;line-height:1.55;transition:all .3s}',
    '.v3-sent.on{background:#f7d774;font-weight:700;box-shadow:0 2px 8px rgba(176,125,43,.35)}',
    '.v3-sent.done{color:#8a7a5f}',
    '.v3-prog{height:8px;background:#eee0bd;border-radius:99px;overflow:hidden;margin:10px 0}',
    '.v3-prog i{display:block;height:100%;background:#b07d2b;width:0%}',
    '.v3-pack{display:flex;gap:10px;flex-wrap:wrap}.v3-pack button{flex:1;min-width:150px}',
    '.v3-lesson{border:1px solid #e5d3a8;border-radius:12px;padding:12px;margin:8px 0;background:#fff}',
    '.v3-quiz label{display:block;padding:6px 8px;border-radius:8px;cursor:pointer}.v3-quiz label:hover{background:#f7ecd2}',
    '.v3-note{font-size:12.5px;color:#8a7a5f}',
    'textarea.v3-refl{width:100%;min-height:64px;border:1px solid #d9c491;border-radius:10px;padding:8px;font-family:inherit}'
  ].join('');
  document.head.appendChild(css);

  function el(html) { var d = document.createElement('div'); d.innerHTML = html; return d.firstElementChild; }
  function modal(html) {
    closeModal();
    var m = el('<div class="v3-modal"><div class="v3-card"><button class="v3-close" title="Đóng">✕</button>' + html + '</div></div>');
    m.querySelector('.v3-close').onclick = closeModal;
    m.addEventListener('click', function (e) { if (e.target === m) closeModal(); });
    document.body.appendChild(m); return m;
  }
  function closeModal() { var m = document.querySelector('.v3-modal'); if (m) m.remove(); if (chant.timer) { clearInterval(chant.timer); chant.timer = null; } }

  /* ---------- 1) PROFILE NHÂN VẬT ---------- */
  var PROFILES = [
    { id: 'nu', name: 'Phật tử nữ', outfit: 'Áo tràng xám–xanh lam, nón lá vẽ sen, túi vải thêu sen',
      purposes: ['Cầu an cho gia đình', 'Tìm phút tĩnh tâm', 'Học Phật pháp'] },
    { id: 'nam', name: 'Phật tử nam', outfit: 'Áo tràng, nón lá, túi vải',
      purposes: ['Cầu an cho gia đình', 'Tìm phút tĩnh tâm', 'Học Phật pháp'] },
    { id: 'tre', name: 'Trẻ em đi chùa', outfit: 'Áo lam Phật tử nhỏ, nón lá nhỏ',
      purposes: ['Đi chùa cùng gia đình', 'Nghe kể chuyện Phật', 'Xem tượng Phật lớn'] }
  ];
  function openProfiles() {
    var h = '<h2>Chọn người đi chùa</h2><div class="v3-note">Chú tiểu An sẽ dẫn đường theo đúng mục đích bạn chọn. Đổi lại bất cứ lúc nào bằng nút “Hồ sơ”.</div><div class="v3-profiles">';
    PROFILES.forEach(function (p) {
      h += '<div class="v3-prof' + (S.profile === p.id ? ' sel' : '') + '" data-id="' + p.id + '"><b>' + p.name + '</b><br><small>' + p.outfit + '</small></div>';
    });
    h += '</div><h3>Mục đích chuyến đi</h3><div class="v3-pack" id="v3-purposes"></div>';
    var m = modal(h);
    var pur = m.querySelector('#v3-purposes');
    function drawPurposes(pid) {
      var p = PROFILES.filter(function (x) { return x.id === pid; })[0]; pur.innerHTML = '';
      p.purposes.forEach(function (t) {
        var b = el('<button class="v3-btn alt">' + t + '</button>');
        b.onclick = function () { S.profile = pid; S.purpose = t; save(); closeModal(); greet(); if (window.__onProfile) window.__onProfile(pid); };
        pur.appendChild(b);
      });
    }
    m.querySelectorAll('.v3-prof').forEach(function (card) {
      card.onclick = function () {
        m.querySelectorAll('.v3-prof').forEach(function (c) { c.classList.remove('sel'); });
        card.classList.add('sel'); drawPurposes(card.getAttribute('data-id'));
      };
    });
    drawPurposes(S.profile || 'nu');
  }
  function greet() {
    var p = PROFILES.filter(function (x) { return x.id === S.profile; })[0];
    if (!p) return;
    var m = modal('<h2>Chú tiểu An chào bạn</h2><p>Bạn đi chùa với mục đích <b>' + (S.purpose || 'vãng cảnh chùa') + '</b>. ' +
      (S.purpose.indexOf('Học') >= 0 ? 'Mời bạn ghé <b>Giảng đường Huệ Đăng</b> — nơi chùa dành cho việc học Phật pháp, có bài giảng theo lộ trình.' :
       S.purpose.indexOf('tĩnh tâm') >= 0 ? 'Mời bạn vào chánh điện <b>niệm kinh</b> một thời ngắn cho lòng lắng lại.' :
       'Mình cùng đi một vòng cho đúng phép: vào cổng, mua nhang hoa ở sạp ngoài cổng, vái Phật, thắp nén hương ở lư sân, rồi vào chánh điện.') +
      '</p><p class="v3-note">Trải nghiệm hỗ trợ tại nhà — không thay thế một chuyến đi chùa thật khi bạn có dịp.</p>');
    setTimeout(function () { if (document.body.contains(m)) closeModal(); }, 9000);
  }

  /* ---------- 2) NIỆM KINH ---------- */
  var TAM_KINH = [
    'Quán Tự Tại Bồ Tát, hành thâm Bát Nhã Ba La Mật Đa thời, chiếu kiến ngũ uẩn giai không, độ nhất thiết khổ ách.',
    'Xá Lợi Tử! Sắc bất dị không, không bất dị sắc; sắc tức thị không, không tức thị sắc. Thọ, tưởng, hành, thức, diệc phục như thị.',
    'Xá Lợi Tử! Thị chư pháp không tướng: bất sanh, bất diệt; bất cấu, bất tịnh; bất tăng, bất giảm.',
    'Thị cố không trung vô sắc, vô thọ, tưởng, hành, thức; vô nhãn, nhĩ, tỷ, thiệt, thân, ý; vô sắc, thanh, hương, vị, xúc, pháp.',
    'Vô nhãn giới, nãi chí vô ý thức giới; vô vô minh, diệc vô vô minh tận; nãi chí vô lão tử, diệc vô lão tử tận.',
    'Vô khổ, tập, diệt, đạo; vô trí, diệc vô đắc.',
    'Dĩ vô sở đắc cố, Bồ Đề Tát Đỏa y Bát Nhã Ba La Mật Đa cố, tâm vô quái ngại; vô quái ngại cố, vô hữu khủng bố, viễn ly điên đảo mộng tưởng, cứu cánh Niết Bàn.',
    'Tam thế chư Phật y Bát Nhã Ba La Mật Đa cố, đắc A Nậu Đa La Tam Miệu Tam Bồ Đề.',
    'Cố tri Bát Nhã Ba La Mật Đa, thị đại thần chú, thị đại minh chú, thị vô thượng chú, thị vô đẳng đẳng chú, năng trừ nhất thiết khổ, chân thiệt bất hư.',
    'Cố thuyết Bát Nhã Ba La Mật Đa chú, tức thuyết chú viết: Yết đế, yết đế, ba la yết đế, ba la tăng yết đế, bồ đề tát bà ha.'
  ];
  var DAI_BI_OPEN = [
    'Nam mô Đại Bi Hội Thượng Phật Bồ Tát. (ba lần)',
    'Thiên thủ thiên nhãn vô ngại Đại Bi tâm đà la ni.',
    'Nam mô hắc ra đát na đa ra dạ da. Nam mô a rị da, bà lô yết đế thước bát ra da, Bồ Đề Tát Đỏa bà da, Ma ha Tát Đỏa bà da, Ma ha ca lô ni ca da.',
    'Án, tát bàn ra phạt duệ, số đát na đát tỏa.',
    'Nam mô tất kiết lật đỏa y mông a rị da, bà lô kiết đế thất Phật ra lăng đà bà.',
    'Nam mô na ra cẩn trì, hê rị ma ha bàn đa sa mế, tát bà a tha đậu du bằng, a thệ dựng.'
  ];
  var PACKS = [
    { id: 'tamkinh', name: 'Gói 5 phút — Tâm Kinh tĩnh tâm', desc: 'Trọn Bát Nhã Tâm Kinh, nhịp chậm. Chuông mở và kết thời.',
      sections: [{ title: 'Bát Nhã Tâm Kinh', lines: TAM_KINH }] },
    { id: 'daibi', name: 'Gói 10 phút — Đại Bi (phần mở đầu)', desc: 'Phần khai kinh và những câu đầu của Chú Đại Bi. Phần tiếp theo sẽ bổ sung từ bản Thiền môn nhật tụng sau kiểm duyệt.',
      sections: [{ title: 'Khai kinh — Chú Đại Bi', lines: DAI_BI_OPEN }, { title: 'Bát Nhã Tâm Kinh', lines: TAM_KINH }] },
    { id: 'congphu', name: 'Gói 20 phút — Công phu tối rút gọn', desc: 'Theo thứ tự thời công phu tối: Đại Bi → Tâm Kinh → niệm Phật 108 lần (đếm hạt).',
      sections: [{ title: 'Khai kinh — Chú Đại Bi', lines: DAI_BI_OPEN }, { title: 'Bát Nhã Tâm Kinh', lines: TAM_KINH }, { title: 'Niệm Phật — 108 lần', lines: [], beads: 108 }] }
  ];
  var chant = { pack: null, flat: [], idx: 0, timer: null, playing: false, beadsLeft: 0 };
  function openChant() {
    var h = '<h2>Niệm kinh</h2><p class="v3-note">Chữ sáng theo từng câu, mõ gõ theo nhịp, chuông ở đầu và cuối mỗi phần. Đã hoàn thành: <b>' + S.chantDone + ' thời</b> · tổng <b>' + S.chantMinutes + ' phút</b>.</p><div class="v3-pack">';
    PACKS.forEach(function (p) { h += '<button class="v3-btn" data-pack="' + p.id + '">' + p.name + '</button>'; });
    h += '</div><div id="v3-pack-desc" style="margin-top:10px"></div><div id="v3-chant-body"></div>';
    var m = modal(h);
    m.querySelectorAll('[data-pack]').forEach(function (b) {
      b.onclick = function () {
        var p = PACKS.filter(function (x) { return x.id === b.getAttribute('data-pack'); })[0];
        m.querySelector('#v3-pack-desc').innerHTML = '<p>' + p.desc + '</p><button class="v3-btn" id="v3-start">Bắt đầu thời kinh</button>';
        m.querySelector('#v3-start').onclick = function () { startChant(p, m); };
      };
    });
  }
  function startChant(pack, m) {
    chant.pack = pack; chant.flat = []; chant.idx = 0; chant.playing = true;
    pack.sections.forEach(function (sec) {
      if (sec.beads) { chant.flat.push({ section: sec.title, beadStart: sec.beads }); }
      sec.lines.forEach(function (ln, i) { chant.flat.push({ section: sec.title, text: ln, first: i === 0 }); });
    });
    var body = m.querySelector('#v3-chant-body');
    body.innerHTML = '<div class="v3-prog"><i id="v3-bar"></i></div><div id="v3-lines"></div>' +
      '<div id="v3-beads" style="display:none;text-align:center"><div style="font-size:44px" id="v3-bead-n"></div>' +
      '<button class="v3-btn" id="v3-bead-btn">Niệm một hạt (phím Space)</button></div>' +
      '<div style="margin-top:10px;display:flex;gap:8px"><button class="v3-btn alt" id="v3-pause">Tạm dừng</button></div>';
    var linesBox = body.querySelector('#v3-lines');
    chant.flat.forEach(function (it, i) {
      if (it.text) { var d = el('<div class="v3-sent" data-i="' + i + '">' + it.text + '</div>'); linesBox.appendChild(d); }
    });
    bell(0.18);
    body.querySelector('#v3-pause').onclick = function () {
      chant.playing = !chant.playing;
      this.textContent = chant.playing ? 'Tạm dừng' : 'Tụng tiếp';
    };
    body.querySelector('#v3-bead-btn').onclick = beadHit;
    chant._key = function (e) { if (e.code === 'Space' && chant.beadsLeft > 0) { e.preventDefault(); beadHit(); } };
    document.addEventListener('keydown', chant._key);
    step(m);
  }
  function beadHit() {
    if (chant.beadsLeft <= 0) return;
    mo(); chant.beadsLeft--;
    var n = document.querySelector('#v3-bead-n'); if (n) n.textContent = 'Còn ' + chant.beadsLeft + ' hạt';
    if (chant.beadsLeft === 0) { chant.idx++; var m = document.querySelector('.v3-modal'); if (m) step(m); }
  }
  function step(m) {
    if (!document.body.contains(m)) { document.removeEventListener('keydown', chant._key); return; }
    if (chant.idx >= chant.flat.length) { finishChant(m); return; }
    var it = chant.flat[chant.idx];
    var bar = m.querySelector('#v3-bar'); if (bar) bar.style.width = Math.round(100 * chant.idx / chant.flat.length) + '%';
    if (it.beadStart) {
      chant.beadsLeft = it.beadStart;
      var bz = m.querySelector('#v3-beads'); bz.style.display = 'block';
      m.querySelector('#v3-bead-n').textContent = 'Còn ' + chant.beadsLeft + ' hạt';
      bell(0.12); return; // chờ người dùng đếm hạt
    }
    var bz2 = m.querySelector('#v3-beads'); if (bz2) bz2.style.display = 'none';
    m.querySelectorAll('.v3-sent').forEach(function (d) {
      var i = +d.getAttribute('data-i');
      d.classList.toggle('on', i === chant.idx);
      if (i < chant.idx) d.classList.add('done');
      if (i === chant.idx) d.scrollIntoView({ block: 'center', behavior: 'smooth' });
    });
    if (it.first) bell(0.10); else mo();
    var words = it.text.split(/\s+/).length;
    var ms = Math.max(2600, words * 620); // nhịp tụng ~ chậm, rõ chữ
    var t0 = Date.now();
    clearInterval(chant.timer);
    chant.timer = setInterval(function () {
      if (!chant.playing) { t0 += 200; return; }
      if (Date.now() - t0 >= ms) { clearInterval(chant.timer); chant.idx++; step(m); }
    }, 200);
  }
  function finishChant(m) {
    bell(0.2);
    S.chantDone++; S.chantMinutes += chant.pack.id === 'tamkinh' ? 5 : chant.pack.id === 'daibi' ? 10 : 20; save();
    document.removeEventListener('keydown', chant._key);
    m.querySelector('#v3-chant-body').innerHTML = '<h3>Hồi hướng</h3><p>Nguyện đem công đức này, hướng về khắp tất cả, đệ tử và chúng sanh, đều trọn thành Phật đạo.</p><p class="v3-note">Bạn vừa hoàn thành một thời kinh — dấu ấn đã lưu vào hồ sơ. Tổng: ' + S.chantDone + ' thời · ' + S.chantMinutes + ' phút.</p>';
  }

  /* ---------- 3) BÀI GIẢNG — GIẢNG ĐƯỜNG HUỆ ĐĂNG ---------- */
  var PATHS = [
    { id: 'A', name: 'A. Nhập môn Phật pháp', lessons: ['Tam Bảo là gì?', 'Đức Phật — bậc thầy, không phải thần linh', 'Chắp tay, xá chào, lễ Phật đúng phép', 'Đi chùa thế nào cho đúng?', 'Nghi lễ căn bản ở chánh điện', 'Ăn chay và giữ giới cho người mới'] },
    { id: 'B', name: 'B. Kinh điển nhập môn', lessons: ['Tâm Kinh — “sắc tức thị không” hiểu sao?', 'Chú Đại Bi và hạnh nguyện Quan Âm', 'Kinh A Di Đà và pháp môn niệm Phật', 'Bát Đại Nhân Giác — tám điều giác ngộ', 'Kinh Vu Lan và đạo hiếu', 'Sám hối trong kinh điển', 'Nhân quả — hiểu đúng, sống đúng', 'Vô thường — bài học từ đời sống'] },
    { id: 'C', name: 'C. Sống an trong đời thường', lessons: ['Khi giận — dừng lại thế nào', 'Khi lo âu — quay về hơi thở', 'Sám hối là gì, bắt đầu từ đâu', 'Hồi hướng và phát nguyện mỗi ngày', 'Bồ đề tâm trong công việc', 'Gia đình hòa thuận theo lời Phật dạy'] },
    { id: 'D', name: 'D. Hiểu về chùa Vĩnh Tràng', lessons: ['Lịch sử Tổ đình Vĩnh Tràng', 'Kiến trúc Á–Âu của chánh điện', 'Trường Phật học Tiền Giang — khởi nguồn 1990 tại Vĩnh Tràng', 'Các tượng lớn trong khuôn viên chùa'] }
  ];
  var SAMPLE_LESSON = {
    path: 'A', idx: 0, title: 'Tam Bảo là gì?',
    summary: 'Tam Bảo là ba ngôi báu của người Phật tử: Phật — bậc đã giác ngộ và chỉ đường; Pháp — lời dạy và con đường thực hành; Tăng — đoàn thể những người cùng tu học và gìn giữ con đường ấy. Quy y Tam Bảo không phải là “theo đạo” theo nghĩa hình thức, mà là chọn một hướng đi: khi lạc lối thì quay về nương tựa nơi ba ngôi báu này. (Bản tóm tắt mẫu của dự án — nội dung giáo lý sẽ được người có chuyên môn kiểm duyệt trước khi phát hành chính thức.)',
    example: 'Thí dụ: như người đi biển cần hải đăng (Phật), hải đồ (Pháp) và thủy thủ đoàn cùng thuyền (Tăng). Thiếu một trong ba, chuyến đi đều khó trọn vẹn.',
    quiz: [
      { q: 'Tam Bảo gồm những gì?', opts: ['Phật — Pháp — Tăng', 'Trời — Đất — Người', 'Chùa — Chuông — Mõ'], ans: 0, why: 'Đúng: Phật, Pháp, Tăng là ba ngôi báu.' },
      { q: '“Pháp” trong Tam Bảo nghĩa là gì?', opts: ['Pháp luật nhà nước', 'Lời Phật dạy và con đường thực hành', 'Phép thuật nhiệm màu'], ans: 1, why: 'Pháp là giáo pháp — lời dạy và phương pháp tu tập, không phải phép thuật.' },
      { q: 'Quy y Tam Bảo hiểu đúng nhất là…', opts: ['Xin một danh xưng mới', 'Nương tựa và hướng đời sống theo Phật — Pháp — Tăng', 'Phải ăn chay trường ngay'], ans: 1, why: 'Quy y là chọn hướng nương tựa để sống và thực hành.' }
    ],
    reflect: 'Lần gần nhất bạn thấy lòng mình “lạc hướng”, điều gì đã giúp bạn bình tĩnh lại?',
    practice: 'Mở mục Niệm kinh và tụng một thời Tâm Kinh 5 phút.'
  };
  function openLessons() {
    var h = '<h2>Giảng đường Huệ Đăng</h2><p class="v3-note">Nơi chùa Vĩnh Tràng tổ chức các lễ khai giảng, tốt nghiệp của Trường Phật học Tiền Giang. Trong trải nghiệm này, đây là lớp học Phật pháp cho cư sĩ: 4 lộ trình, mỗi bài theo 6 phần — nghe giảng, tóm tắt, thí dụ, quiz, suy ngẫm, hành trì. Bài giảng âm thanh sẽ bổ sung khi có nguồn được phép phổ biến.</p>';
    PATHS.forEach(function (p) {
      h += '<h3>' + p.name + '</h3>';
      p.lessons.forEach(function (t, i) {
        var done = S.lessonsDone[p.id + i];
        var isSample = (p.id === SAMPLE_LESSON.path && i === SAMPLE_LESSON.idx);
        h += '<div class="v3-lesson"><b>' + (done ? '✓ ' : '') + t + '</b>' +
          (isSample ? ' <button class="v3-btn" data-lesson="' + p.id + i + '">Vào học</button>' : ' <span class="v3-note">— sắp mở</span>') + '</div>';
      });
    });
    var m = modal(h);
    m.querySelectorAll('[data-lesson]').forEach(function (b) { b.onclick = function () { openSampleLesson(m); }; });
  }
  function openSampleLesson(m) {
    var L = SAMPLE_LESSON;
    var h = '<h2>' + L.title + '</h2><p class="v3-note">Lộ trình A · Bài 1 · Thầy giảng sư thỉnh chuông mở lớp (bấm “Vào học” là chuông đã thỉnh ở lớp học chính).</p>' +
      '<h3>2) Tóm tắt</h3><p>' + L.summary + '</p>' +
      '<h3>3) Thí dụ</h3><p>' + L.example + '</p>' +
      '<h3>4) Quiz — 3 câu</h3><div class="v3-quiz" id="v3-quiz"></div>' +
      '<h3>5) Suy ngẫm</h3><p>' + L.reflect + '</p><textarea class="v3-refl" id="v3-refl" placeholder="Viết 1–3 dòng của bạn (chỉ lưu trên máy này)…">' + (S.reflections['A0'] || '') + '</textarea>' +
      '<h3>6) Hành trì gợi ý</h3><p>' + L.practice + '</p>' +
      '<div style="margin-top:12px"><button class="v3-btn" id="v3-done">Hoàn thành bài học</button></div><div id="v3-quiz-msg"></div>';
    m.querySelector('.v3-card').innerHTML = '<button class="v3-close" title="Đóng">✕</button>' + h;
    m.querySelector('.v3-close').onclick = closeModal;
    bell(0.15);
    var qz = m.querySelector('#v3-quiz'); var score = {};
    L.quiz.forEach(function (q, qi) {
      var box = el('<div style="margin:10px 0"><b>' + (qi + 1) + '. ' + q.q + '</b></div>');
      q.opts.forEach(function (o, oi) {
        var lab = el('<label><input type="radio" name="q' + qi + '"> ' + o + '</label>');
        lab.querySelector('input').onchange = function () {
          score[qi] = (oi === q.ans);
          m.querySelector('#v3-quiz-msg').innerHTML = '<p class="v3-note">' + q.why + '</p>';
        };
        box.appendChild(lab);
      });
      qz.appendChild(box);
    });
    m.querySelector('#v3-done').onclick = function () {
      var answered = Object.keys(score).length, right = Object.values(score).filter(Boolean).length;
      if (answered < 3) { m.querySelector('#v3-quiz-msg').innerHTML = '<p>Bạn trả lời đủ 3 câu quiz trước khi hoàn thành (' + answered + '/3).</p>'; return; }
      S.reflections['A0'] = m.querySelector('#v3-refl').value; S.lessonsDone['A0'] = true; save();
      m.querySelector('#v3-quiz-msg').innerHTML = '<p>Hoàn thành. Quiz đúng ' + right + '/3. Dấu ấn bài học đã lưu vào hồ sơ.</p>';
    };
  }

  /* ---------- Xuất hàm dùng chung (v5: KHÔNG còn thanh nút nổi .v3-bar —
     Niệm kinh / Bài giảng / Hồ sơ mở qua khay Khám phá, Cài đặt và trạm) ---------- */
  window.openChant = openChant; window.openLessons = openLessons; window.openProfiles = openProfiles;
  window.getProfile = function () { return S.profile; }; // module chính đọc profile hiện tại
  // v5: KHÔNG tự bật modal chọn nhân vật — mặc định Phật tử nữ (đúng ảnh mẫu),
  // người dùng đổi trong Cài đặt khi muốn.
  if (!S.profile) { S.profile = 'nu'; save(); }
})();

