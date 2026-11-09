// Nghiệm thu v5 KHÔNG seed: mở -> đếm phần tử bấm được màn hình đầu ->
// Vào cổng -> Chuẩn bị nhang hoa (mua) -> tới lư -> thắp đủ 4 nhịp -> kiểm localStorage.
// Chụp 4 ảnh: spawn / sạp / giữa lễ thắp nhang / chánh điện cửa bên.
import { writeFileSync, mkdirSync } from 'node:fs';
const PAGE = 'file:///home/hatch/workspace/chua-online-work/trai-nghiem-vinh-trang-v5-TESTLOCAL.html';
const SHOTS = '/home/hatch/workspace/chua-online-work/v5_shots';
mkdirSync(SHOTS, { recursive: true });
const list = await (await fetch('http://localhost:9222/json/list')).json();
const t = list.find(x => x.type === 'page' && x.url.startsWith('about:')) || list.find(x => x.type === 'page');
if (!t) throw new Error('no page target');
const ws = new WebSocket(t.webSocketDebuggerUrl);
await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });
let id = 0; const pending = new Map(); const errs = [];
const send = (m, p = {}) => new Promise((resolve) => { const i = ++id; pending.set(i, resolve); ws.send(JSON.stringify({ id: i, method: m, params: p })); });
ws.onmessage = (ev) => {
  const m = JSON.parse(ev.data);
  if (m.id && pending.has(m.id)) { pending.get(m.id)(m.result || {}); pending.delete(m.id); }
  if (m.method === 'Runtime.exceptionThrown') errs.push(m.params.exceptionDetails?.exception?.description || m.params.exceptionDetails?.text);
  if (m.method === 'Runtime.consoleAPICalled' && m.params.type === 'error') errs.push('console.error: ' + m.params.args.map(a => a.value || a.description || '').join(' '));
};
const ev = async (expr) => { const r = await send('Runtime.evaluate', { expression: expr, returnByValue: true }); if (r.exceptionDetails) throw new Error('EVAL FAIL: ' + JSON.stringify(r.exceptionDetails).slice(0, 300)); return r.result?.value; };
const sleep = ms => new Promise(r => setTimeout(r, ms));
async function setDSF(f) {
  await send('Emulation.setDeviceMetricsOverride', { width: 880, height: 560, deviceScaleFactor: f, mobile: false });
}
async function shot(name) {
  await setDSF(1.5); // nâng độ nét riêng cho khung hình nghiệm thu
  await sleep(3500);
  const s = await send('Page.captureScreenshot', { format: 'png' });
  writeFileSync(`${SHOTS}/${name}.png`, Buffer.from(s.data, 'base64'));
  console.log('SHOT', name);
  await setDSF(0.5);
}
async function waitFor(label, expr, timeout = 180000) {
  const t0 = Date.now();
  while (Date.now() - t0 < timeout) {
    const v = await ev(expr).catch(() => null);
    if (v) { console.log('OK  ', label, '=>', typeof v === 'object' ? JSON.stringify(v) : v); return v; }
    await sleep(700);
  }
  throw new Error('TIMEOUT: ' + label);
}
await send('Runtime.enable'); await send('Page.enable'); await send('Emulation.enable'); await send('Input.enable');
await setDSF(0.5); // render nhẹ để vòng lặp chạy nhanh trong lúc di chuyển
await send('Page.navigate', { url: PAGE });
await sleep(14000);

// 0) Trang đã chạy module chưa + đếm phần tử bấm được ở màn hình đầu
await waitFor('module ready', `!!(window.__v5debug && document.getElementById('btn-context'))`);
const clickables = await ev(`(() => {
  const out = [];
  document.querySelectorAll('button, a, input, [onclick], .opt-card, .menu-item, .nav-pill, .tray-btn').forEach(el => {
    const cs = getComputedStyle(el);
    const r = el.getBoundingClientRect();
    if (cs.display === 'none' || cs.visibility === 'hidden' || cs.pointerEvents === 'none') return;
    if (+cs.opacity < 0.5) return;
    if (r.width < 2 || r.height < 2) return;
    if (r.bottom < 0 || r.top > innerHeight || r.right < 0 || r.left > innerWidth) return;
    out.push(el.id || el.className || el.tagName);
  });
  return out;
})()`);
console.log('FIRST-SCREEN CLICKABLES:', JSON.stringify(clickables), 'COUNT =', clickables.length);
const state0 = await ev(`window.__v5debug.state()`);
console.log('SPAWN STATE:', JSON.stringify(state0));
await shot('1_spawn');
// Tăng tốc RIÊNG cho kiểm thử headless (máy đang tải nặng, rAF ~0.7fps) — logic không đổi
await ev(`window.__v5debug.setAutoSpeed(24); window.__v5debug.setSpeed(24); 'fast'`);

// 1) Vào cổng (nút động từ = lệnh di chuyển)
await ev(`document.getElementById('btn-context').click(); 'clicked'`);
await waitFor('gate done', `window.__v5debug.state().journey.gate === true`);
const v1 = await ev(`window.__v5debug.state().verb`);
console.log('VERB AFTER GATE:', v1);

// 2) Chuẩn bị nhang hoa -> tự đi tới sạp -> panel mở
await ev(`document.getElementById('btn-context').click(); 'clicked'`);
await waitFor('stall panel open', `document.getElementById('stall-panel').classList.contains('open')`);
await shot('2_sap');
await ev(`document.getElementById('stall-opt3').click(); 'opt3'`);
await ev(`document.getElementById('stall-buy').click(); 'buy'`);
await waitFor('bought 3 sticks', `JSON.stringify(window.__v5debug.state().bought)`, 8000);
const st2 = await ev(`window.__v5debug.state()`);
console.log('AFTER BUY:', JSON.stringify({ bought: st2.bought, journey: st2.journey }));

// 3) Tới lư (đi bộ tay bằng debug walkTo — tương đương nhấp sàn) rồi bấm nút ngữ cảnh của trạm lư
await ev(`window.__v5debug.walkTo(28, 36); 'hop1'`); // qua cửa bên vào sân trước
await waitFor('inside grounds', `(() => { const p = window.__v5debug.state().pos; return Math.hypot(p[0] - 28, p[1] - 36) < 2.5; })()`, 240000);
await ev(`window.__v5debug.walkTo(25.3, 13.7); 'walk'`);
await waitFor('at burner station', `window.__v5debug.state().station === 'burner'`, 240000);
const v3 = await ev(`window.__v5debug.state().verb`);
console.log('VERB AT BURNER:', v3);
await ev(`document.getElementById('btn-context').click(); 'clicked'`);
await waitFor('incense panel open', `document.getElementById('incense-panel').classList.contains('open')`);
// Nhịp 1: chọn 3 nén
await ev(`(() => { const c = document.querySelectorAll('#incense-actions .opt-card'); c[1].click(); return c.length; })()`);
await sleep(600);
// Nhịp 2a: châm từ đèn dầu
await ev(`(() => { const b = [...document.querySelectorAll('#incense-actions .big-btn')][0]; b.click(); return b.textContent; })()`);
await sleep(600);
// Nhịp 2b: GIỮ nút phẩy nhẹ ~1.6s bằng sự kiện chuột CDP thật (đúng đường input của người dùng)
const holdXY = await ev(`(() => { const b = document.querySelector('#incense-actions .big-btn'); const rc = b.getBoundingClientRect(); return { x: rc.x + rc.width / 2, y: rc.y + rc.height / 2 }; })()`);
await send('Input.dispatchMouseEvent', { type: 'mousePressed', x: holdXY.x, y: holdXY.y, button: 'left', clickCount: 1 });
await sleep(1600);
await send('Input.dispatchMouseEvent', { type: 'mouseReleased', x: holdXY.x, y: holdXY.y, button: 'left', clickCount: 1 });
await waitFor('beat 3 reached', `document.getElementById('incense-text').textContent.includes('Nhịp 3')`, 8000);
// Nhịp 3: vái 3 lần (chụp ảnh giữa lễ ở nhịp này)
await shot('3_thapnhang');
for (let i = 0; i < 3; i++) {
  await ev(`(() => { const b = [...document.querySelectorAll('#incense-actions .big-btn')][0]; b.click(); return b.textContent; })()`);
  await sleep(500);
}
await waitFor('beat 4 reached', `document.getElementById('incense-text').textContent.includes('Nhịp 4')`, 8000);
// Nhịp 4: cắm nhang vào giữa lư
await ev(`(() => { const b = [...document.querySelectorAll('#incense-actions .big-btn')][0]; b.click(); return b.textContent; })()`);
await sleep(800);
const lsState = await ev(`localStorage.getItem('chuaOnlineV5')`);
console.log('LOCALSTORAGE chuaOnlineV5:', lsState);
const parsed = JSON.parse(lsState);
console.log('CHECK lit.main =', parsed.lit && parsed.lit.main, '| journey.burner =', parsed.journey && parsed.journey.burner);
await ev(`(() => { const b = [...document.querySelectorAll('#incense-actions .big-btn')][0]; if (b) b.click(); return 'closed'; })()`);

// 4) Chánh điện cửa bên (phía tây)
await ev(`window.__v5debug.walkTo(17.5, 6.8); 'walk'`);
await waitFor('at hall station', `window.__v5debug.state().station === 'hall'`, 240000);
await sleep(1500);
await shot('4_chanhdien_cuaben');
const v4label = await ev(`window.__v5debug.state().verb`);
console.log('VERB AT HALL:', v4label);

console.log('EXCEPTIONS:', errs.length ? JSON.stringify(errs.slice(0, 6)) : 'none');
ws.close(); process.exit(0);
