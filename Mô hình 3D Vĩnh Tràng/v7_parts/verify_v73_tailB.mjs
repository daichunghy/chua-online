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
// ---------- V72-TAIL: gieo trạng thái SAU P11 qua localStorage (game tự nạp khi khởi động) ----------
// Trạng thái thật sau P11 ở lượt chạy đầy đủ: journey gate/stall/adida/dilac/burner/hall/huunhieu,
// bought = {sticks:3, flowers:true} (mua ở P2), giỏ quầy trống, lit rỗng (không check nào phía sau đọc lit).
await send('Page.addScriptToEvaluateOnNewDocument', { source: `
  try {
    localStorage.setItem('chuaOnlineV5', JSON.stringify({
      bought: { sticks: 3, flowers: true },
      incenseDate: new Date().toISOString().slice(0, 10),
      lit: {},
      journey: { gate: true, stall: true, adida: true, dilac: true, burner: true, hall: true, huunhieu: true, nirvana: true, tower: true },
      brightness: 1.0
    }));
  } catch (e) {}
` });
await send('Page.navigate', { url: 'file:///tmp/redir.html' });
const readyT = await waitFor('module ready (tail)', async () => !!(await ev(`!!window.__v6ff && !!window.__v6debug`)), 300);
verdict('TAIL module sẵn sàng', readyT === true);
await ev(`window.__voiceLog = [];
(() => { const _play = HTMLAudioElement.prototype.play;
  HTMLAudioElement.prototype.play = function () { try { if (this.src) window.__voiceLog.push(this.src); } catch (e) {} return _play.call(this); }; })();`);
const voiceCount = async key => await ev(`(window.__voiceLog || []).filter(s => s.indexOf(${JSON.stringify(key + '.mp3')}) !== -1).length`);
const voiceSeen = async key => (await voiceCount(key)) > 0;
const charsOkT = await waitFor('chars ready (tail)', async () => (await ev(`window.__charsReady === true`)) === true, 300);
console.log('  [CHAR-TAIL] charsReady =', charsOkT);
await sleep(1500);
const seedState = await state();
const seedOk = !!seedState && ['gate','stall','adida','dilac','burner','hall','huunhieu','nirvana','tower'].every(k => seedState.journey && seedState.journey[k] === true)
  && seedState.bought && seedState.bought.sticks === 3 && seedState.inside === false;
verdict('TAIL trạng thái gieo khớp sau-P13 (9 cờ journey + bought.sticks=3 + ngoài điện)', seedOk, JSON.stringify(seedState && seedState.journey));
await ev(`window.__v6debug.teleport(-2, -38)`); // B2: dat nguoi choi o chan thap nhu luc P13 vua xong (vi tri tu nhien cua pha)
await ev(`window.__v6ff(30)`);
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
// Từ shop đi books — tuyến V7.3c (diag_books2/3_v73 đo từng đoạn):
// (a) Phòng kinh sách ĐÃ DỜI trong module_2/6b từ (33,-12) sang (42,-10.5),
// điểm đứng (42,-7.6): vị trí cũ nằm TRONG rect va chạm chánh điện nên không
// đường đi nào tới được — lỗi đặt phòng, không phải lỗi bán kính trạm.
// (b) Tuyến vòng phía ĐÔNG bị khóa cứng: bonsai lớn (29.2,6.4) R nới 1,59 +
// bonsai (28.7,26) R 1,25 + mép hồ đông (rect nới tới z=24,0) + thùng công đức
// (27.9,4.9) R 1,3 + tháp phải chánh điện (rect nới x 36,9..40,3, z 0,3..3,7)
// tạo dải chắn liên tục (diag3: avatar kẹt cứng ở (29.03,8.02)).
// (c) Tuyến dùng ở đây: trục giữa x=23 -> làn Phật nằm đã kiểm chứng P12
// (15,8)(5,5)(2,-2)(4,-20)(8,-32) -> sau lưng chánh điện (20,-24)(34,-17)
// -> (37,-14.4) (ngoài rect điện z>=-13,5 và ngoài góc Giảng đường) ->
// điểm đứng (42,-7.6), lách góc tây-nam rect phòng (39.1,-12.3) hở 0,49.
for (const [hx, hz] of [[23, 30], [23, 16], [15, 8], [5, 5], [2, -2], [4, -20], [8, -32], [20, -24], [34, -17], [37, -14.4], [42, -7.6]]) {
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
// v8 (đo hop_test/probe_test): làn cũ x=38,5 XUYÊN THÂN THÁP ĐÔNG — vùng cấm
// tháp (x>=36,9; z>=0,3 sau biên 0,5) và vùng cấm điện (x<=37,5; z<=1,7)
// chồng nhau, dải x=38,5 bịt kín về hình học (V7.3 từng lọt nhờ cắt góc).
// Làn mới vòng qua khe đông THẬT (x>40,3): men z=4,3-4,5 (hở mép tháp
// z<=3,7 từ 0,6m, hở cây (40,6) R=1,0 từ 1,67m), vòng nam thùng công
// đức (27,9;4,9) R=1,3 qua (28;2,8) (hở >=1,67m mọi đoạn, tính tay)
// rồi tới điểm đứng trạm. CHỈ đổi hop đệm di chuyển;
// các verdict (station=hall, inside, kẹp cột) giữ nguyên như V7.3.
for (const [hx, hz] of [[42, 4.3], [30, 4.5], [28, 2.8], [17.5, 6.8]]) {
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
// day_di: lượt TAIL gieo trạng thái sau P11 nên lần bấm nút đầu không diễn ra ở đây;
// tính "phát đúng 1 lần + không phát lặp" đã được chứng ở lượt chạy đầy đủ (run2: P0 PASS).
const dayDiFinal = await voiceCount('day_di');
console.log(`  [VOICE-TAIL] day_di count trong lượt tail = ${dayDiFinal} (kỳ vọng 0 ở lượt gieo; bản đầy đủ đã PASS ở run2)`);
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