// verify_v73 (gốc verify_v71.mjs — giữ nguyên 46 verdict V7 + thêm 10 check V7.1):
// (1) tới shop thì s7_tam_biet được gọi, (2) tới books thì s3_giang_duong được gọi,
// (3) bấm nút động từ lần đầu thì day_di được gọi đúng 1 lần (và vẫn 1 lần cuối tuyến),
// (4) trong điện, camera không còn nằm trong/xuyên cột đỏ (3 góc thử + 1 đối chứng).
// Bắt sự kiện phát giọng bằng spy HTMLAudioElement.prototype.play (ghi src), không nghe thật.
//
// Môi trường headless SwiftShader chỉ đạt ~0,6 fps nên thời gian game bị giãn ~33 lần.
// Vì vậy các chờ đợi theo khung hình dùng harness __v6ff CỦA BẢN TESTLOCAL: gọi thẳng
// module_7.tick(dt=0.05, render=false) — vẫn là 100% logic thật của game, chỉ tua nhanh
// tất định và bỏ qua render trung gian. Tương tác DOM/chuột vẫn là sự kiện thật.
import fs from 'node:fs';

const SHOTDIR = '/home/hatch/workspace/chua-online-work/v7_shots';
fs.mkdirSync(SHOTDIR, { recursive: true });

const sleep = ms => new Promise(r => setTimeout(r, ms));
const verdicts = [];
function verdict(name, ok, detail = '') {
  verdicts.push({ name, ok, detail });
  console.log(`[${ok ? 'PASS' : 'FAIL'}] ${name}${detail ? ' — ' + detail : ''}`);
}

const list = await (await fetch('http://localhost:9222/json/list')).json();
const target = list.find(x => x.type === 'page');
if (!target) { console.log('NO PAGE TARGET'); process.exit(2); }
const ws = new WebSocket(target.webSocketDebuggerUrl);
await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });
let msgId = 0; const pending = new Map();
const exceptions = []; const consoleErrors = [];
ws.onmessage = ev => {
  const m = JSON.parse(ev.data);
  if (m.id && pending.has(m.id)) { pending.get(m.id)(m.result || {}); pending.delete(m.id); return; }
  if (m.method === 'Runtime.exceptionThrown') {
    const d = m.params.exceptionDetails;
    exceptions.push((d.exception && d.exception.description) || d.text || 'unknown');
  }
  if (m.method === 'Runtime.consoleAPICalled' && m.params.type === 'error') {
    consoleErrors.push(m.params.args.map(a => a.value || a.description || '').join(' '));
  }
};
const send = (method, params = {}) => new Promise(r => { const i = ++msgId; pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
const ev = async expr => { const r = await send('Runtime.evaluate', { expression: expr, returnByValue: true }); return r.result ? r.result.value : undefined; };
const state = () => ev(`window.__v6debug ? window.__v6debug.state() : null`);
// Chờ theo THỜI GIAN THẬT (sự kiện DOM đồng bộ / timer thật của trang)
async function waitFor(desc, fn, timeoutS = 60) {
  const t0 = Date.now();
  while (Date.now() - t0 < timeoutS * 1000) { if (await fn()) return true; await sleep(1200); }
  console.log('  TIMEOUT:', desc); return false;
}
// Chờ theo THỜI GIAN GAME: tua nhanh bằng harness tick() cho tới khi điều kiện đúng
async function ffUntil(desc, fn, maxGameSec = 360) {
  let used = 0;
  while (used <= maxGameSec) {
    if (await fn()) return true;
    await ev(`window.__v6ff && window.__v6ff(60)`);
    await sleep(150);
    used += 3;
  }
  if (await fn()) return true;
  console.log('  FF-TIMEOUT:', desc); return false;
}
const click = sel => ev(`(() => { const el = document.querySelector(${JSON.stringify(sel)}); if (!el) return false; el.scrollIntoView({block:'center'}); el.click(); return true; })()`);
const clickText = (scopeSel, text) => ev(`(() => { const scope = document.querySelector(${JSON.stringify(scopeSel)}) || document; const b = [...scope.querySelectorAll('button, .opt-card')].find(x => x.textContent.includes(${JSON.stringify(text)})); if (!b) return false; b.click(); return true; })()`);
async function shot(name, dsf = 1.5) {
  await send('Emulation.setDeviceMetricsOverride', { width: 420, height: 840, deviceScaleFactor: dsf, mobile: true });
  await sleep(3500);
  // V7: captureScreenshot từng treo cứng khi renderer quá tải (lượt chạy đầu
  // gãy ở 2c_thap_nhang) -> bọc timeout 45s + thử lại 3 lần.
  let data = null;
  for (let attempt = 1; attempt <= 1 && !data; attempt++) {
    try {
      const r = await Promise.race([
        send('Page.captureScreenshot', { format: 'png' }),
        sleep(40000).then(() => { throw new Error('shot timeout'); }),
      ]);
      data = r.data || null;
    } catch (e) { console.log('  shot retry', name, attempt, e.message); await sleep(3000); }
  }
  if (data) { fs.writeFileSync(`${SHOTDIR}/${name}.png`, Buffer.from(data, 'base64')); console.log('  shot:', name); }
  else console.log('  shot FAILED (bo qua):', name);
  await send('Emulation.setDeviceMetricsOverride', { width: 260, height: 520, deviceScaleFactor: 0.25, mobile: true });
}
const near = async (x, z, d = 1.6) => { const s = await state(); return s && Math.hypot(s.pos[0] - x, s.pos[1] - z) < d; };

await send('Page.enable'); await send('Runtime.enable');
await send('Emulation.setDeviceMetricsOverride', { width: 260, height: 520, deviceScaleFactor: 0.25, mobile: true });
// Chrome bản này chặn điều hướng thẳng tới 127.0.0.1 (LNA) — đi qua trang chuyển hướng file:// (local→local)
await send('Page.navigate', { url: 'file:///tmp/redir.html' });

// ---------- P0: tải trang + màn hình đầu ----------
const ready = await waitFor('module ready', async () => !!(await ev(`!!window.__v6ff && !!window.__v6debug`)), 300);
verdict('P0 tải trang + module + harness sẵn sàng', ready);
if (!ready) { console.log('ABORT'); process.exit(2); }
// Dọn sạch tiến trình đã lưu để lượt chạy thật sự KHÔNG seed
await ev(`localStorage.clear()`);
await ev(`location.reload()`);
await waitFor('module ready after reload', async () => !!(await ev(`!!window.__v6ff && !!window.__v6debug`)), 300);
await ev(`window.__v6debug.setSpeed(10); window.__v6debug.setAutoSpeed(10);`);
// V7.1: spy giọng — ghi lại mọi lần HTMLAudioElement.play() kèm src (playVoice dùng new Audio).
// Cài SAU reload để không bị trang mới xóa; lời chào đầu (sayAn 900ms, không voiceKey) không phát audio.
await ev(`window.__voiceLog = [];
(() => { const _play = HTMLAudioElement.prototype.play;
  HTMLAudioElement.prototype.play = function () { try { if (this.src) window.__voiceLog.push(this.src); } catch (e) {} return _play.call(this); }; })();`);
const voiceCount = async key => await ev(`(window.__voiceLog || []).filter(s => s.indexOf(${JSON.stringify(key + '.mp3')}) !== -1).length`);
const voiceSeen = async key => (await voiceCount(key)) > 0;
// V7: chờ 3 GLB nhân vật nạp + dựng xong hết (chỉ log kiểm, không tính verdict)
const charsOk = await waitFor('chars ready', async () => (await ev(`window.__charsReady === true`)) === true, 300);
const charsDump = await ev(`window.__v7chars ? window.__v7chars() : []`);
console.log('  [CHAR] charsReady =', charsOk, '| tổng nhân vật =', (charsDump || []).length,
  '| ready =', (charsDump || []).filter(c => c.ready).length,
  '| người chơi =', JSON.stringify((charsDump || [])[0]));
await sleep(1500);
const clickables = await ev(`[...document.querySelectorAll('button, a, input, [onclick], .opt-card, .menu-item, .nav-pill, .tray-btn')].filter(el => {
  const r = el.getBoundingClientRect();
  if (r.width < 2 || r.height < 2) return false;
  if (r.right <= 0 || r.bottom <= 0 || r.left >= innerWidth || r.top >= innerHeight) return false;
  for (let n = el; n; n = n.parentElement) {
    const cs = getComputedStyle(n);
    if (cs.display === 'none' || cs.visibility === 'hidden' || cs.opacity === '0') return false;
  }
  return true;
}).length`);
verdict('P0 màn hình đầu đúng 3 phần tử bấm được (thấy được thật)', clickables === 3, `count=${clickables}`);
const nametags = await ev(`document.querySelectorAll('.nametag').length`);
verdict('A1 không còn bảng tên nổi (.nametag = 0)', nametags === 0, `count=${nametags}`);
const s0 = await state();
verdict('P0 nút động từ đầu = “Vào cổng”', s0 && s0.verb === 'Vào cổng', `verb=${s0 && s0.verb}`);
await shot('1_spawn');

// ---------- P1: cổng ----------
await click('#btn-context');
const dayDiFirst = await voiceCount('day_di');
verdict('V7.1 day_di phát đúng 1 lần khi bấm nút động từ đầu tiên', dayDiFirst === 1, `count=${dayDiFirst}`);
verdict('P1 vào cổng (journey.gate)', await ffUntil('gate', async () => (await state())?.journey?.gate === true));

// ---------- P2: sạp nhang hoa ----------
await click('#btn-context');
verdict('P2 sạp mở', await ffUntil('stall open', async () => await ev(`document.getElementById('stall-panel').classList.contains('open')`)));
await sleep(2500);
await shot('2b_sap');
await click('#stall-opt3');
await sleep(400);
await click('#stall-buy');
verdict('P2 mua bó 3 nén (bought.sticks=3, journey.stall)', await waitFor('bought', async () => { const s = await state(); return s && s.bought && s.bought.sticks === 3 && s.journey.stall; }, 60));
// Thẻ Tìm hiểu thêm tại sạp (tâm hương)
const infoShown = await ev(`document.getElementById('btn-info').classList.contains('show')`);
if (infoShown) {
  await click('#btn-info');
  const okInfo = await waitFor('info modal', async () => await ev(`document.getElementById('info-modal').classList.contains('open') && document.getElementById('info-modal').textContent.includes('tâm hương')`), 30);
  verdict('B thẻ “Tìm hiểu thêm” tại sạp (tâm hương)', !!okInfo);
  await clickText('#info-modal', 'Đóng'); await sleep(600);
} else verdict('B thẻ “Tìm hiểu thêm” tại sạp (tâm hương)', false, 'btn-info không hiện tại sạp');

// ---------- P3: A Di Đà ----------
await click('#btn-context');
verdict('P3 vái A Di Đà (journey.adida)', await ffUntil('adida', async () => (await state())?.journey?.adida === true, 300));
await ev(`window.__v6ff(8)`); // vào giữa nhịp lạy đầu
await shot('2_truoc_tuong');
let dimSeen = false;
for (let i = 0; i < 30 && !dimSeen; i++) { const s = await state(); if (s && s.ritualDim) dimSeen = true; else { await ev(`window.__v6ff(10)`); await sleep(120); } }
verdict('A UI mờ trong nhịp lạy (ritual-dim)', dimSeen);

// ---------- P4: Di Lặc ----------
await click('#btn-context');
verdict('P4 vái Di Lặc (journey.dilac)', await ffUntil('dilac', async () => (await state())?.journey?.dilac === true, 300));

// ---------- P5: lư hương 4 nhịp ----------
await click('#btn-context');
verdict('P5 panel thắp nhang mở', await ffUntil('incense open', async () => await ev(`document.getElementById('incense-panel').classList.contains('open')`), 300));
verdict('P5 tới trạm lư (station=burner sau khi tới nơi)', (await state())?.station === 'burner', `station=${(await state())?.station}`);
const dimPanel = await ev(`document.body.classList.contains('ritual-dim')`);
verdict('A UI mờ khi panel nhang mở', dimPanel === true);
await clickText('#incense-actions', '3 nén');
await sleep(600);
await clickText('#incense-actions', 'Châm nhang vào đèn dầu');
await sleep(800);
// Giữ chuột thật trên nút phẩy (tiến độ tính theo thời gian giữ thật ≥900ms)
const holdRect = await ev(`(() => { const b = [...document.querySelectorAll('#incense-actions button')].find(x => x.textContent.includes('Phẩy')); if (!b) return null; const r = b.getBoundingClientRect(); return { x: r.x + r.width / 2, y: r.y + r.height / 2 }; })()`);
if (holdRect) {
  await send('Input.dispatchMouseEvent', { type: 'mousePressed', x: holdRect.x, y: holdRect.y, button: 'left', clickCount: 1 });
  await sleep(1500);
  await send('Input.dispatchMouseEvent', { type: 'mouseReleased', x: holdRect.x, y: holdRect.y, button: 'left', clickCount: 1 });
} else console.log('  KHÔNG THẤY nút phẩy');
verdict('P5 nhịp 2 phẩy tắt lửa → nhịp 3', await waitFor('beat3', async () => await ev(`document.getElementById('incense-text').textContent.includes('Nhịp 3')`), 60));
await clickText('#incense-actions', 'Vái một vái'); await sleep(900);
await ev(`window.__v6ff(20)`); // V7: giữa nhịp vái ở lư — action 'Vái' của model thật
await shot('2c_thap_nhang');
for (let i = 0; i < 2; i++) { await clickText('#incense-actions', 'Vái một vái'); await sleep(900); }
verdict('P5 nhịp 3 vái đủ 3 → nhịp 4', await waitFor('beat4', async () => await ev(`document.getElementById('incense-text').textContent.includes('Nhịp 4')`), 60));
await clickText('#incense-actions', 'Cắm nhang vào giữa lư');
verdict('P5 cắm nhang (lit.main + journey.burner)', await waitFor('lit', async () => { const s = await state(); return s && s.lit && s.lit.main && s.journey.burner; }, 60));
await clickText('#incense-actions', 'Đã xong — đóng');
await ev(`window.__v6ff(120)`); // 6 giây game: nhịp lạy cuối + giữ tĩnh chạy hết
await sleep(800);
const panelClosed = await ev(`!document.getElementById('incense-panel').classList.contains('open') && !document.body.classList.contains('ritual-dim')`);
verdict('P5 đóng panel, UI sáng lại', panelClosed === true);

// ---------- P6–P8: vào chánh điện, lễ Tổ, lạy 3 ----------
await click('#btn-context');
verdict('P6 vào nội điện (inside=true)', await ffUntil('inside', async () => (await state())?.inside === true, 300));
await click('#btn-context');
verdict('P7 lễ Tổ (journey.to)', await ffUntil('to', async () => (await state())?.journey?.to === true, 300));
await click('#btn-context');
let dimBow = false;
for (let i = 0; i < 60 && !dimBow; i++) {
  const s = await state();
  if (s && s.journey && s.journey.hall) break;
  if (s && s.ritualDim) dimBow = true;
  else { await ev(`window.__v6ff(30)`); await sleep(120); }
}
verdict('A UI mờ trong 3 lạy ở Tam Bảo', dimBow);
if (dimBow) await shot('3_lay_ui_mo');
verdict('P8 lạy Phật 3 lạy (journey.hall)', await ffUntil('hall', async () => (await state())?.journey?.hall === true, 120));
verdict('A UI sáng lại sau lạy + giữ tĩnh', await ffUntil('dim off', async () => !(await state())?.ritualDim, 120));
await ev(`window.__v6ff(20)`);
await shot('4_noi_dien');
const sIn = await state();
verdict('P8 nút động từ sau lạy = “Niệm kinh (không bắt buộc)”', sIn && sIn.verb === 'Niệm kinh (không bắt buộc)', `verb=${sIn && sIn.verb}`);
// Thẻ hữu nhiễu tại bàn Tam Bảo
const infoIn = await ev(`document.getElementById('btn-info').classList.contains('show')`);
if (infoIn) {
  await click('#btn-info');
  const okHN = await waitFor('huu nhieu card', async () => await ev(`document.getElementById('info-modal').classList.contains('open') && document.getElementById('info-modal').textContent.includes('Hữu nhiễu')`), 30);
  verdict('B thẻ “Tìm hiểu thêm” hữu nhiễu trong điện', !!okHN);
  await clickText('#info-modal', 'Đóng'); await sleep(600);
} else verdict('B thẻ “Tìm hiểu thêm” hữu nhiễu trong điện', false, 'btn-info không hiện tại trạm in');

// ---------- P9: Niệm kinh trong điện ----------
await click('#btn-context');
verdict('P9 modal Niệm kinh mở từ trạm Tam Bảo', await waitFor('chant modal', async () => await ev(`!!document.querySelector('.v3-modal') && document.querySelector('.v3-modal').textContent.includes('Niệm kinh')`), 60));
await ev(`(() => { const b = document.querySelector('[data-pack]'); if (b) b.click(); return !!b; })()`);
await sleep(600);
await click('#v3-start');
verdict('P9 thời kinh chạy (có câu .v3-sent)', await waitFor('chant lines', async () => (await ev(`document.querySelectorAll('.v3-sent').length`)) > 0, 90));
await click('.v3-close');
await sleep(800);

// ---------- P10–P11: hữu nhiễu + ra sân ----------
await ev(`window.__v6debug.walkTo(303, 310)`);
await ffUntil('near huunhieu 1', () => near(303, 310, 2), 120);
await ev(`window.__v6debug.walkTo(300.5, 317.5)`);
await ffUntil('near huunhieu 2', () => near(300.5, 317.5, 2), 120);
await click('#btn-context');
verdict('P10 hữu nhiễu (journey.huunhieu)', await ffUntil('huunhieu', async () => (await state())?.journey?.huunhieu === true, 120));
await click('#btn-context');
verdict('P11 ra sân (inside=false)', await ffUntil('outside', async () => (await state())?.inside === false, 300));

// ---------- P12: Phật nằm — đứng lặng ----------
await click('#btn-context');
verdict('P12 tới trạm Phật nằm', await ffUntil('station nirvana', async () => (await state())?.station === 'nirvana', 300));
verdict('P12 đứng lặng trọn 10s (silenceDone)', await ffUntil('silence done', async () => (await state())?.silenceDone === true, 120));
const quietShown = await ev(`document.getElementById('btn-quiet').classList.contains('show')`);
verdict('P12 nút “Tiếp” hiện sau đứng lặng', quietShown === true);
await click('#btn-quiet');
verdict('P12 vái Phật nằm sau đứng lặng (journey.nirvana)', await ffUntil('nirvana', async () => (await state())?.journey?.nirvana === true, 120));

// ---------- P13: tháp + hồi hướng ----------
await click('#btn-context');
verdict('P13 thẻ hồi hướng mở ở bảo tháp', await ffUntil('hoihuong modal', async () => await ev(`[...document.querySelectorAll('.modal-overlay')].some(o => o.textContent.includes('Hồi hướng'))`), 300));
verdict('P13 journey.tower', (await state())?.journey?.tower === true);
await ev(`(() => { const o = [...document.querySelectorAll('.modal-overlay')].find(x => x.textContent.includes('Hồi hướng')); const b = o && [...o.querySelectorAll('button')].find(x => x.textContent.trim() === 'Đóng'); if (b) b.click(); return !!b; })()`);
verdict('P13 khép tuyến (body.free)', await waitFor('free', async () => await ev(`document.body.classList.contains('free')`), 60));

// ---------- P14: quầy lưu niệm + giỏ ----------
for (const [hx, hz] of [[8, -32], [4, -20], [2, -2], [8, 3.6], [19, 8.5], [25.3, 13.7], [30, 22], [36, 28], [40, 34.3]]) {
  await ev(`window.__v6debug.walkTo(${hx}, ${hz})`);
  await ffUntil(`hop shop ${hx},${hz}`, () => near(hx, hz, 2.2), 120);
}
verdict('P14 tới trạm quầy lưu niệm', await ffUntil('station shop', async () => (await state())?.station === 'shop', 60));
verdict('V7.1 tới shop thì s7_tam_biet được gọi', await voiceSeen('s7_tam_biet'), `s7_tam_biet count=${await voiceCount('s7_tam_biet')}`);
await click('#btn-context');
verdict('P14 shop mở', await ffUntil('shop open', async () => await ev(`document.getElementById('shop-modal').classList.contains('open')`), 120));
const shopOpenNow = await ev(`document.getElementById('shop-modal').classList.contains('open')`);
if (shopOpenNow) await ev(`(() => { const b = document.querySelector('.shop-item .add'); if (b) b.click(); return !!b; })()`);
verdict('P14 thêm 1 món (cartQty=1)', !!shopOpenNow && await waitFor('cart 1', async () => (await state())?.cartQty === 1, 60));
await sleep(1000);
await shot('5_shop');
await click('#btn-view-cart');
const cartOk = await waitFor('cart modal', async () => await ev(`[...document.querySelectorAll('.modal-overlay')].some(o => o.textContent.includes('Giỏ hàng của bạn'))`), 60);
const cartText = cartOk ? await ev(`([...document.querySelectorAll('.modal-overlay')].find(o => o.textContent.includes('Giỏ hàng của bạn')) || {}).textContent || ''`) : '';
verdict('P14 giỏ đúng món + giá (Sổ tay hoa sen, 89.000đ)', cartText.includes('Sổ tay hoa sen') && cartText.includes('89.000đ'), cartText.slice(0, 80).replace(/\s+/g, ' '));
await ev(`(() => { const o = [...document.querySelectorAll('.modal-overlay')].find(x => x.textContent.includes('Giỏ hàng của bạn')); const b = o && o.querySelector('.modal-close'); if (b) b.click(); return !!b; })()`);
await sleep(600);
await click('#shop-modal .modal-close');
await sleep(600);

// ---------- P15: bản đồ ----------
await click('#btn-map');
verdict('P15 bản đồ mở (có #map-dot)', await waitFor('map', async () => await ev(`!!document.getElementById('map-dot')`), 60));
await ev(`(() => { const os = document.querySelectorAll('.dyn-overlay'); const o = os[os.length - 1]; const b = o && o.querySelector('.modal-close'); if (b) b.click(); return !!b; })()`);
await sleep(600);

// ---------- P16: khay Khám phá → Niệm kinh ----------
await click('#nav-explore');
await waitFor('tray open', async () => await ev(`document.getElementById('explore-tray').classList.contains('open')`), 30);
await click('#tray-chant');
verdict('P16 Niệm kinh qua khay Khám phá', await waitFor('chant via tray', async () => await ev(`!!document.querySelector('.v3-modal')`), 60));
await click('.v3-close');
await sleep(800);

// ---------- P17: Bài giảng ----------
await click('#nav-learn');
verdict('P17 Giảng đường (Bài giảng) mở', await waitFor('lessons', async () => await ev(`!!document.querySelector('.v3-modal') && document.querySelector('.v3-modal').textContent.includes('Giảng đường Huệ Đăng')`), 60));
await ev(`(() => { const b = document.querySelector('[data-lesson]'); if (b) b.click(); return !!b; })()`);
verdict('P17 vào bài học (có quiz)', await waitFor('quiz', async () => await ev(`!!document.querySelector('.v3-quiz')`), 60));
await click('.v3-close');
await sleep(800);

// ---------- P18: Cài đặt ----------
await click('#btn-settings');
verdict('P18 pop Cài đặt mở', await waitFor('settings', async () => await ev(`document.getElementById('settings-pop').classList.contains('open')`), 30));
const lblBefore = await ev(`document.getElementById('btn-audio-toggle').textContent`);
await click('#btn-audio-toggle');
await sleep(500);
const lblAfter = await ev(`document.getElementById('btn-audio-toggle').textContent`);
verdict('P18 nút Chuông Mõ đổi trạng thái', lblBefore !== lblAfter, `${lblBefore} → ${lblAfter}`);
await click('#btn-settings');

// ---------- P19 (V7.1): Phòng kinh sách — giọng Giảng đường ----------
// Từ shop đi men phía đông chánh điện (tránh rect chánh điện x 9..37, z -13..1.2) tới books.
for (const [hx, hz] of [[23, 30], [23, 16], [15, 8], [5, 5], [2, -2], [4, -20], [8, -32], [20, -24], [34, -17], [37, -14.4], [42, -7.6]]) { // v7.3c: phòng kinh sách dời (42,-10.5) + tuyến sau lưng điện (xem verify_v73_tailB.mjs)
  await ev(`window.__v6debug.walkTo(${hx}, ${hz})`);
  await ffUntil(`hop books ${hx},${hz}`, () => near(hx, hz, 2.5), 120);
}
verdict('V7.1 tới trạm Phòng kinh sách', await ffUntil('station books', async () => (await state())?.station === 'books', 60));
verdict('V7.1 tới books thì s3_giang_duong được gọi', await voiceSeen('s3_giang_duong'), `s3_giang_duong count=${await voiceCount('s3_giang_duong')}`);

// ---------- P20 (V7.1): camera trong điện không xuyên cột đỏ ----------
// Cột world: x = 291.5 / 308.5, z = 282, 290, 298, 306, 314, 320; trục r = 0,48; kẹp r = 0,8.
const PILLARS = []; for (const pz of [282, 290, 298, 306, 314, 320]) { PILLARS.push([291.5, pz], [308.5, pz]); }
const camMinDist = async () => {
  const s = await state(); if (!s || !s.cam) return -1;
  let m = 1e9;
  for (const [px, pz] of PILLARS) m = Math.min(m, Math.hypot(s.cam[0] - px, s.cam[1] - pz));
  return m;
};
const camCase = async (px, pz, yaw) => {
  await ev(`window.__v6debug.teleport(${px}, ${pz}); window.__v6debug.setCamYaw(${yaw});`);
  await ev(`window.__v6ff(60)`); await sleep(300);
  return camMinDist();
};
// Vào lại chánh điện: đi vòng phía nam (z ~ 6.8, ngoài rect chánh điện) tới trạm hall rồi bấm nút.
for (const [hx, hz] of [[38.5, -4], [38.5, 6], [30, 6], [17.5, 6.8]]) {
  await ev(`window.__v6debug.walkTo(${hx}, ${hz})`);
  await ffUntil(`hop hall ${hx},${hz}`, () => near(hx, hz, 2.5), 120);
}
verdict('V7.1 vào lại chánh điện (station=hall)', await ffUntil('station hall', async () => (await state())?.station === 'hall', 60));
await click('#btn-context');
verdict('V7.1 vào lại nội điện (inside=true)', await waitFor('inside again', async () => (await state())?.inside === true, 60));
// 3 góc từng xuyên cột: đặt người chơi sao cho camera chưa kẹp sẽ rơi đúng tâm cột.
let dA = await camCase(291.5, 286.5, 0);
verdict('V7.1 camera không xuyên cột — chính diện (291.5,286.5,yaw 0)', dA >= 0.78, `minDist=${dA.toFixed(2)} (kẹp r=0,8)`);
let dB = await camCase(308.5, 301.5, Math.PI);
verdict('V7.1 camera không xuyên cột — đối diện (308.5,301.5,yaw π)', dB >= 0.78, `minDist=${dB.toFixed(2)} (kẹp r=0,8)`);
let dC = await camCase(293.97, 292.47, 5 * Math.PI / 4);
verdict('V7.1 camera không xuyên cột — chéo (293.97,292.47,yaw 5π/4)', dC >= 0.78, `minDist=${dC.toFixed(2)} (kẹp r=0,8)`);
let dD = await camCase(300, 290.5, 0);
const sD = await state();
verdict('V7.1 camera xa cột giữ nguyên vị trí (đối chứng Tam Bảo)', dD > 3 && sD && Math.hypot(sD.cam[0] - 300, sD.cam[1] - 294) < 0.15, `minDist=${dD.toFixed(2)} cam=${JSON.stringify(sD && sD.cam)}`);
await ev(`window.__v6debug.teleport(300, 290.5); window.__v6debug.setCamYaw(0.5);`);
await ev(`window.__v6ff(40)`);
await shot('6_dien_cot');
// day_di phải VẪN đúng 1 lần sau toàn tuyến (mọi lần bấm nút động từ sau đó không phát lại).
const dayDiFinal = await voiceCount('day_di');
verdict('V7.1 day_di vẫn đúng 1 lần cuối tuyến (không phát lặp)', dayDiFinal === 1, `count=${dayDiFinal}`);
console.log('  [VOICE] log:', JSON.stringify(await ev(`window.__voiceLog || []`)));

// ---------- Tổng kết ---------- (in sớm — chốt cổng trước phần bonus NPC) ----------
const fin = await state();
console.log('\n===== TỔNG KẾT V6 =====');
console.log('journey:', JSON.stringify(fin && fin.journey));
console.log('exceptions:', exceptions.length, exceptions.slice(0, 5));
console.log('console errors:', consoleErrors.length, consoleErrors.slice(0, 5));
const fails = verdicts.filter(v => !v.ok);
console.log(`verdicts: ${verdicts.length - fails.length}/${verdicts.length} PASS`);
verdict('CỔNG 0 lỗi JS toàn tuyến', exceptions.length === 0 && consoleErrors.length === 0, `exc=${exceptions.length} consoleErr=${consoleErrors.length}`);


// ---------- V7: ảnh NPC vái/chắp tay trước tượng A Di Đà (trang riêng ?v5pos) ----------
await send('Page.navigate', { url: 'file:///tmp/redir_npc.html' });
await waitFor('module ready (npc page)', async () => !!(await ev(`!!window.__v6ff && !!window.__v6debug`)), 300);
await waitFor('chars ready (npc page)', async () => (await ev(`window.__charsReady === true`)) === true, 300);
let npcFound = false;
for (let i = 0; i < 200 && !npcFound; i++) {
  const cs = await ev(`window.__v7chars ? window.__v7chars() : []`);
  npcFound = (cs || []).some(c => Math.abs(c.x + 14) < 1.8 && Math.abs(c.z - 24) < 1.8 && (c.pose === 'Vái' || c.pose === 'Chắp tay'));
  if (!npcFound) { await ev(`window.__v6ff(50)`); await sleep(150); }
}
console.log('  [CHAR] NPC đang vái/chắp tay trước A Di Đà:', npcFound ? 'BẮT ĐƯỢC' : 'không bắt được trong thời gian chờ');
if (npcFound) await shot('2a_npc_adida');


// Addendum sau phần bonus NPC: đếm lại exceptions (trang NPC nạp cùng bản build)
verdict('CỔNG 0 lỗi JS (cả trang bonus NPC)', exceptions.length === 0, exceptions.length ? exceptions[0].slice(0, 160) : 'sạch');
console.log('===== KẾT THÚC: ' + verdicts.filter(v => v.ok).length + '/' + verdicts.length + ' PASS =====');
ws.close();
process.exit(verdicts.every(v => v.ok) && exceptions.length === 0 ? 0 : 1);
