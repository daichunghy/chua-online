/* ===== CHÙA ONLINE V5 — Thẻ an lạc mỗi ngày (Dấu ấn mang về) =====
   Bản v5 đã GỠ khỏi file này: panel "Dấu ấn hành trình" dạng checklist thứ hai,
   chuỗi 5 chặng cũ (có thả đèn nguyện — không có ở chùa thật), chú tiểu dạng hộp thoại cố định.
   Tiến trình duy nhất của v5 là hàng cánh sen ở module chính.
   Thẻ an lạc sống trong mục Khám phá — NGOÀI tuyến lễ. */
(function () {
  'use strict';
  var KEY = 'chuaOnlineV2';
  var today = new Date();
  function dstr(d) { return d.getFullYear() + '-' + (d.getMonth() + 1) + '-' + d.getDate(); }
  var TODAY = dstr(today);
  var S = { fortuneDate: '', fortuneIdx: -1 };
  try { var raw = localStorage.getItem(KEY); if (raw) S = Object.assign(S, JSON.parse(raw)); } catch (e) {}
  function save() { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) {} }

  var CARDS = [
    { t: 'An nhiên', v: 'Tâm an thì cảnh an. Hôm nay cứ đi chậm một chút.' },
    { t: 'Buông nhẹ', v: 'Việc gì không đổi được, học cách mỉm cười mà qua.' },
    { t: 'Biết ơn', v: 'Nhớ ơn người đã giúp mình, dù chỉ một lần rất nhỏ.' },
    { t: 'Lắng nghe', v: 'Nghe hết câu chuyện của người khác trước khi phán xét.' },
    { t: 'Hiếu thuận', v: 'Một cuộc gọi về nhà hôm nay đáng hơn ngàn lời hẹn.' },
    { t: 'Kiên nhẫn', v: 'Cây sen cũng phải chờ bùn lặng mới nở hoa.' },
    { t: 'Cho đi', v: 'Giúp người không cần đợi lúc mình dư dả.' },
    { t: 'Tỉnh thức', v: 'Ăn biết ngon, ngủ biết yên — đó đã là phúc.' },
    { t: 'Từ bi', v: 'Nói một lời làm người khác nhẹ lòng, phước ở ngay đó.' },
    { t: 'Đủ đầy', v: 'Biết đủ là giàu. Hôm nay bạn đã có rất nhiều rồi.' },
    { t: 'Bình an', v: 'Đi chùa không cầu hết khổ, chỉ cầu lòng vững giữa khổ vui.' },
    { t: 'Khởi đầu', v: 'Ngày mới như nén hương mới thắp — bắt đầu lại lúc nào cũng được.' }
  ];
  function dailyCardIdx() {
    var h = 0; for (var i = 0; i < TODAY.length; i++) h = (h * 31 + TODAY.charCodeAt(i)) >>> 0;
    return h % CARDS.length;
  }

  var css = document.createElement('style');
  css.textContent =
    '#co-card-modal{position:fixed;inset:0;z-index:9999;background:rgba(20,10,0,.55);display:none;align-items:center;justify-content:center}' +
    '#co-card{background:linear-gradient(165deg,#fff8e1,#ffe9a8);border:3px solid #c8871a;border-radius:24px;width:min(320px,86vw);' +
    'padding:26px 22px;text-align:center;color:#5b3a06;box-shadow:0 12px 40px rgba(0,0,0,.5)}' +
    '#co-card .ttl{font-size:24px;font-weight:800;color:#a86e00;letter-spacing:1px} #co-card .verse{font-size:16px;margin:12px 0;line-height:1.6}' +
    '#co-card button{background:#1C5A34;color:#FFF6E5;border:none;border-radius:999px;padding:9px 22px;font-weight:700;cursor:pointer;font-family:inherit}';
  document.head.appendChild(css);

  var modal = document.createElement('div'); modal.id = 'co-card-modal';
  modal.innerHTML = '<div id="co-card"><div class="ttl"></div>' +
    '<div class="verse"></div><div style="font-size:12px;opacity:.7" class="day"></div>' +
    '<button id="co-card-close">Con cảm ơn</button></div>';
  document.body.appendChild(modal);
  document.getElementById('co-card-close').addEventListener('click', function () { modal.style.display = 'none'; });
  modal.addEventListener('click', function (e) { if (e.target === modal) modal.style.display = 'none'; });

  window.__openFortune = function () {
    if (S.fortuneDate !== TODAY) { S.fortuneDate = TODAY; S.fortuneIdx = dailyCardIdx(); save(); }
    var c = CARDS[S.fortuneIdx >= 0 ? S.fortuneIdx : dailyCardIdx()];
    modal.querySelector('.ttl').textContent = '「 ' + c.t + ' 」';
    modal.querySelector('.verse').textContent = c.v;
    modal.querySelector('.day').textContent = 'Thẻ ngày ' + today.getDate() + '/' + (today.getMonth() + 1) + '/' + today.getFullYear() + ' — Chùa Vĩnh Tràng Online';
    modal.style.display = 'flex';
  };
})();
