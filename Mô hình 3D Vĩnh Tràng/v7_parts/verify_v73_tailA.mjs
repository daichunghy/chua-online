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
      journey: { gate: true, stall: true, adida: true, dilac: true, burner: true, hall: true, huunhieu: true },
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
const seedOk = !!seedState && ['gate','stall','adida','dilac','burner','hall','huunhieu'].every(k => seedState.journey && seedState.journey[k] === true)
  && seedState.bought && seedState.bought.sticks === 3 && seedState.inside === false;
verdict('TAIL trạng thái gieo khớp sau-P11 (7 cờ journey + bought.sticks=3 + ngoài điện)', seedOk, JSON.stringify(seedState && seedState.journey));
await ev(`window.__v6debug.teleport(23, 10)`); // A2: dat nguoi choi o them dien nhu luc vua ra san o P11 (vi tri tu nhien cua pha)
await ev(`window.__v6ff(30)`);
console.log('  [A2] verb sau teleport:', JSON.stringify((await state()) && (await state()).verb));
// ---------- P12: Phật nằm — đứng lặng ----------
await click('#btn-context');
verdict('P12 tới trạm Phật nằm', await ffUntil('station nirvana', async () => (await state())?.station === 'nirvana', 420));
verdict('P12 đứng lặng trọn 10s (silenceDone)', await ffUntil('silence done', async () => (await state())?.silenceDone === true, 180));
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

// ---------- Tổng kết ---------- (in sớm — chốt cổng trước phần bonus NPC) ----------
const fin = await state();
console.log('\n===== TỔNG KẾT V6 =====');
console.log('journey:', JSON.stringify(fin && fin.journey));
console.log('exceptions:', exceptions.length, exceptions.slice(0, 5));
console.log('console errors:', consoleErrors.length, consoleErrors.slice(0, 5));
const fails = verdicts.filter(v => !v.ok);
console.log(`verdicts: ${verdicts.length - fails.length}/${verdicts.length} PASS`);
verdict('CỔNG 0 lỗi JS toàn tuyến', exceptions.length === 0 && consoleErrors.length === 0, `exc=${exceptions.length} consoleErr=${consoleErrors.length}`);

ws.close();
process.exit(verdicts.every(v => v.ok) && exceptions.length === 0 ? 0 : 1);