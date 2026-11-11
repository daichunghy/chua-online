    import * as THREE from 'three';
    import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
    import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
    import { clone as skeletonClone } from 'three/addons/utils/SkeletonUtils.js';


    // 1. AUDIO SYNTHESIZER
    let audioCtx = null;
    let isAudioOn = true;

    function initAudio() {
      if (!audioCtx) {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      }
    }

    function playBell() {
      if (!isAudioOn) return;
      initAudio();
      if (audioCtx.state === 'suspended') audioCtx.resume();
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(587.33, audioCtx.currentTime); // D5
      osc.frequency.exponentialRampToValueAtTime(293.66, audioCtx.currentTime + 3.5);
      gain.gain.setValueAtTime(0.55, audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 3.8);
      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start();
      osc.stop(audioCtx.currentTime + 3.8);
    }

    function playMokugyo() {
      if (!isAudioOn) return;
      initAudio();
      if (audioCtx.state === 'suspended') audioCtx.resume();
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(340, audioCtx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(140, audioCtx.currentTime + 0.12);
      gain.gain.setValueAtTime(0.85, audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.14);
      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start();
      osc.stop(audioCtx.currentTime + 0.15);
    }

    document.getElementById('btn-audio-toggle').onclick = () => {
      isAudioOn = !isAudioOn;
      document.getElementById('btn-audio-toggle').textContent = isAudioOn ? 'Chuông Mõ: Bật' : 'Chuông Mõ: Tắt';
      if (isAudioOn) playBell();
    };

    // 3. PROCEDURAL CARTOON TEXTURES
    // Mặt Chibi cười tươi má hồng
    function createChibiFaceTexture(type = 'happy') {
      const cv = document.createElement('canvas');
      cv.width = 512;
      cv.height = 512;
      const ctx = cv.getContext('2d');

      // Nền da hồng đào mềm mại
      ctx.fillStyle = '#ffdfba';
      ctx.fillRect(0, 0, 512, 512);

      if (type === 'happy' || type === 'user') {
        // Đôi mắt cười hình trăng lưỡi liềm cong dễ thương
        ctx.strokeStyle = '#381607';
        ctx.lineWidth = 18;
        ctx.lineCap = 'round';

        ctx.beginPath();
        ctx.arc(160, 230, 52, Math.PI * 1.15, Math.PI * 1.85, false);
        ctx.stroke();

        ctx.beginPath();
        ctx.arc(352, 230, 52, Math.PI * 1.15, Math.PI * 1.85, false);
        ctx.stroke();

        // Má hồng đào phúng phính (Blush)
        ctx.fillStyle = 'rgba(255, 99, 132, 0.6)';
        ctx.beginPath();
        ctx.arc(120, 285, 45, 0, Math.PI * 2);
        ctx.fill();

        ctx.beginPath();
        ctx.arc(392, 285, 45, 0, Math.PI * 2);
        ctx.fill();

        // Nụ cười hoan hỷ
        ctx.beginPath();
        ctx.arc(256, 290, 32, 0.2, Math.PI - 0.2, false);
        ctx.stroke();

        // Chấm đỏ bindi giữa trán
        ctx.fillStyle = '#d62828';
        ctx.beginPath();
        ctx.arc(256, 140, 14, 0, Math.PI * 2);
        ctx.fill();
      } else if (type === 'buddha') {
        // Mặt Đức Phật Chibi từ bi
        ctx.fillStyle = '#ffe699';
        ctx.fillRect(0, 0, 512, 512);

        ctx.strokeStyle = '#5c3300';
        ctx.lineWidth = 14;
        ctx.lineCap = 'round';

        // Đôi mắt khép hờ tĩnh lặng
        ctx.beginPath();
        ctx.arc(165, 235, 55, Math.PI * 0.1, Math.PI * 0.9, false);
        ctx.stroke();
        ctx.beginPath();
        ctx.arc(347, 235, 55, Math.PI * 0.1, Math.PI * 0.9, false);
        ctx.stroke();

        // Nụ cười từ bi
        ctx.beginPath();
        ctx.arc(256, 305, 36, 0.2, Math.PI - 0.2, false);
        ctx.stroke();

        // Bạch hào ngọc trắng
        ctx.fillStyle = '#ffffff';
        ctx.beginPath();
        ctx.arc(256, 150, 18, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = '#ffb703';
        ctx.lineWidth = 6;
        ctx.stroke();
      }

      const tex = new THREE.CanvasTexture(cv);
      return tex;
    }

    const faceUserTex = createChibiFaceTexture('user');
    const faceMonkTex = createChibiFaceTexture('happy');
    const faceBuddhaTex = createChibiFaceTexture('buddha');

    // Sàn gạch đỏ men nung Cartoon bóng bẩy
    function createCartoonFloorTexture() {
      const cv = document.createElement('canvas');
      cv.width = 512;
      cv.height = 512;
      const ctx = cv.getContext('2d');
      const size = 128;
      for (let y = 0; y < 4; y++) {
        for (let x = 0; x < 4; x++) {
          const px = x * size;
          const py = y * size;
          ctx.fillStyle = '#3a1106';
          ctx.fillRect(px, py, size, size);

          ctx.fillStyle = '#b8381d';
          ctx.beginPath();
          ctx.roundRect(px + 4, py + 4, size - 8, size - 8, 14);
          ctx.fill();

          const grad = ctx.createRadialGradient(px + size/2, py + size/2, 5, px + size/2, py + size/2, size/2);
          grad.addColorStop(0, '#f2542d');
          grad.addColorStop(0.7, '#cc3b1b');
          grad.addColorStop(1, '#94260f');
          ctx.fillStyle = grad;
          ctx.beginPath();
          ctx.roundRect(px + 8, py + 8, size - 16, size - 16, 10);
          ctx.fill();

          ctx.strokeStyle = 'rgba(255, 209, 102, 0.55)';
          ctx.lineWidth = 2;
          ctx.beginPath();
          ctx.roundRect(px + 10, py + 10, size - 20, size - 20, 8);
          ctx.stroke();
        }
      }
      const tex = new THREE.CanvasTexture(cv);
      tex.wrapS = THREE.RepeatWrapping;
      tex.wrapT = THREE.RepeatWrapping;
      tex.repeat.set(16, 26);
      return tex;
    }

    const floorTexture = createCartoonFloorTexture();

    // 4. CARTOON VIBRANT MATERIALS
    const mat = (c, r=0.45, m=0.0, e=0, ei=0) => new THREE.MeshStandardMaterial({
      color: c, roughness: r, metalness: m,
      emissive: e ? c : 0, emissiveIntensity: Math.min(ei, 2.2) // v4: trần emissive D2
    });

    const floorMat = new THREE.MeshStandardMaterial({
      map: floorTexture,
      roughness: 0.2,
      metalness: 0.15,
    });

    const pillarMat = mat(0xd90429, 0.3, 0.05); // Cột sơn son đỏ tươi bóng
    const wallMat = mat(0xfff3bf, 0.65, 0.0); // Tường vàng kem ấm
    const goldMat = mat(0xffd166, 0.22, 0.88); // Vàng hoàng kim tươi sáng
    const buddhaMat = mat(0xffb703, 0.2, 0.9); // Kim thân Phật dát vàng óng ánh
    const arhatMat = mat(0xffc300, 0.22, 0.88); // 18 La Hán Chibi vàng óng
    const lotusPinkMat = mat(0xff5d8f, 0.4); // Cánh hoa sen hồng tươi
    const lotusWhiteMat = mat(0xffffff, 0.35); // Đầu cánh sen trắng
    const woodDark = mat(0x4a1e13, 0.6); // Gỗ mun ấm
    const matRug = mat(0x9d0208, 0.65); // Thảm đỏ tươi
    const cushionMat = mat(0x7209b7, 0.55); // Bồ đoàn tím sen
    const haloMat = mat(0xffe066, 0.1, 0, 1, 2.2);

    // Materials cho các chú thú cưng Chibi
    const deerMat = mat(0xddb892, 0.45, 0.1);
    const tigerMat = mat(0xf77f00, 0.35, 0.15);
    const dragonMat = mat(0x06d6a0, 0.3, 0.25);
    const elephantMat = mat(0xfdf0d5, 0.35, 0.1);
    const lionMat = mat(0xffb703, 0.4, 0.2);


    // ---- Scene + grade D2 (audit) ----
    const canvas = document.getElementById('three-canvas');
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x2B7DE1); // v7.2: trời xanh cobalt như ảnh mẫu (palette #0155C9–#4F97F9)
    scene.fog = new THREE.FogExp2(0xBDD7F2, 0.0032); // v8: 0,0028 -> 0,0032 — phông xa mềm sương sớm như ảnh tham chiếu (giữ nguyên cobalt sky + exposure 1,12 đã nghiệm thu) // v7.2: sương sáng xanh — bỏ sương nâu 0x2a1a10 làm xỉn/tối toàn cảnh
    const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.1, 600);
    camera.position.set(23, 4.5, 52);
    camera.lookAt(23, 2, 38);
    const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, powerPreference: 'high-performance' });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.12; // v7.2: nâng sáng tổng thể theo tông "Sáng trong" của ảnh mẫu
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    // Layered lights: layer 0 ngoài sân / layer 1 nội điện (tối hơn một bậc)
    const hemi = new THREE.HemisphereLight(0xfff2d9, 0x5e4a35, 1.3);
    hemi.layers.set(0);
    scene.add(hemi);
    const sun = new THREE.DirectionalLight(0xffd9a3, 1.7);
    sun.position.set(-30, 25, 18); // nắng thấp phía tây
    sun.castShadow = true;
    sun.shadow.mapSize.width = 2048; sun.shadow.mapSize.height = 2048;
    sun.shadow.camera.left = -60; sun.shadow.camera.right = 60;
    sun.shadow.camera.top = 60; sun.shadow.camera.bottom = -60;
    sun.shadow.camera.far = 120;
    sun.layers.set(0);
    scene.add(sun);
    // v7.3: đèn fill frontal từ phía nam (phía sân/người xem) — nắng chính từ tây
    // làm mặt tiền + mặt tượng (hướng nam) tối/đỏ nâu trong ảnh V7.2; fill mềm
    // không đổ bóng chỉ nâng các bề mặt hướng nam cho sáng như ảnh mẫu.
    const frontFill73 = new THREE.DirectionalLight(0xfff6e0, 0.55);
    frontFill73.position.set(25, 20, 55);
    frontFill73.castShadow = false;
    frontFill73.layers.set(0);
    scene.add(frontFill73);
    const hemiIn = new THREE.HemisphereLight(0xffe9c4, 0x3a2418, 0.55);
    hemiIn.layers.set(1);
    scene.add(hemiIn);
    camera.layers.enable(1); // camera thấy cả 2 layer
    function setLayerRecursive(obj, layer) {
      obj.traverse(o => { o.layers.set(layer); });
    }
    // Mây trắng mềm
    const cloudTex = (() => {
      const cv = document.createElement('canvas'); cv.width = 256; cv.height = 128;
      const ctx = cv.getContext('2d');
      for (let i = 0; i < 14; i++) {
        const x = 30 + Math.random() * 196, y = 40 + Math.random() * 48, r = 18 + Math.random() * 26;
        const g = ctx.createRadialGradient(x, y, 2, x, y, r);
        g.addColorStop(0, 'rgba(255,255,255,0.85)'); g.addColorStop(1, 'rgba(255,255,255,0)');
        ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, r, 0, 7); ctx.fill();
      }
      return new THREE.CanvasTexture(cv);
    })();
    for (let i = 0; i < 7; i++) {
      const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: cloudTex, transparent: true, opacity: 0.85, depthWrite: false }));
      sp.position.set(-60 + i * 22 + Math.random() * 8, 42 + Math.random() * 14, -50 + Math.random() * 90);
      sp.scale.set(34, 16, 1);
      scene.add(sp);
    }

    // ---- Âm thanh 5 zone (procedural WebAudio, không file ngoài) ----
    const ZONES = {
      cong:  { wind: 0.16, birds: 0.25, chime: 0 },   // cổng: gió + chim xa
      san:   { wind: 0.10, birds: 0.5,  chime: 0.3 }, // sân: chim gần + lá
      dien:  { wind: 0.02, birds: 0,    chime: 0.6 }, // điện: tĩnh + chuông/mõ
      dilac: { wind: 0.08, birds: 0.35, chime: 0.4 },
      thap:  { wind: 0.05, birds: 0.1,  chime: 0.8 }, // tháp: tĩnh nhất
    };
    let amb = null, curZone = 'cong';
    function initAmbience() {
      if (amb) return;
      initAudio();
      const ctx = audioCtx;
      const master = ctx.createGain(); master.gain.value = 0.9; master.connect(ctx.destination);
      // Gió: noise loop qua lowpass
      const len = ctx.sampleRate * 2;
      const buf = ctx.createBuffer(1, len, ctx.sampleRate);
      const d = buf.getChannelData(0);
      for (let i = 0; i < len; i++) d[i] = Math.random() * 2 - 1;
      const noise = ctx.createBufferSource(); noise.buffer = buf; noise.loop = true;
      const lp = ctx.createBiquadFilter(); lp.type = 'lowpass'; lp.frequency.value = 420;
      const windGain = ctx.createGain(); windGain.gain.value = 0;
      noise.connect(lp); lp.connect(windGain); windGain.connect(master); noise.start();
      const birdGain = ctx.createGain(); birdGain.gain.value = 0; birdGain.connect(master);
      const chimeGain = ctx.createGain(); chimeGain.gain.value = 0; chimeGain.connect(master);
      amb = { ctx, master, windGain, birdGain, chimeGain };
      applyZone('cong', 0.1);
      scheduleBird(); scheduleChime();
    }
    function applyZone(name, fadeSec) {
      if (!amb) return;
      const z = ZONES[name] || ZONES.san;
      const t = amb.ctx.currentTime;
      amb.windGain.gain.linearRampToValueAtTime(z.wind, t + fadeSec);
      amb.birdGain.gain.linearRampToValueAtTime(z.birds, t + fadeSec);
      amb.chimeGain.gain.linearRampToValueAtTime(z.chime * 0.5, t + fadeSec);
    }
    function setZone(name) {
      if (name === curZone) return;
      curZone = name;
      if (amb) applyZone(name, 1.75); // crossfade 1,5–2s
    }
    window.__setZone = setZone;
    function birdChirp() {
      if (!amb || !isAudioOn) return;
      const ctx = amb.ctx, t = ctx.currentTime;
      const o = ctx.createOscillator(); o.type = 'sine';
      const g = ctx.createGain(); g.gain.value = 0;
      o.connect(g); g.connect(amb.birdGain);
      const f0 = 2400 + Math.random() * 900;
      o.frequency.setValueAtTime(f0, t);
      o.frequency.exponentialRampToValueAtTime(f0 * 1.3, t + 0.09);
      o.frequency.exponentialRampToValueAtTime(f0 * 0.9, t + 0.18);
      g.gain.linearRampToValueAtTime(0.5, t + 0.03);
      g.gain.exponentialRampToValueAtTime(0.001, t + 0.22);
      o.start(t); o.stop(t + 0.25);
    }
    function scheduleBird() {
      setTimeout(() => {
        if (Math.random() < 0.8) { birdChirp(); if (Math.random() < 0.5) setTimeout(birdChirp, 180); }
        scheduleBird();
      }, 3000 + Math.random() * 6000);
    }
    function chimeRing() {
      if (!amb || !isAudioOn) return;
      const ctx = amb.ctx, t = ctx.currentTime;
      [880, 1174.7, 1568].forEach((f, i) => {
        const o = ctx.createOscillator(); o.type = 'sine'; o.frequency.value = f;
        const g = ctx.createGain();
        g.gain.setValueAtTime(0, t + i * 0.12);
        g.gain.linearRampToValueAtTime(0.22, t + i * 0.12 + 0.02);
        g.gain.exponentialRampToValueAtTime(0.001, t + i * 0.12 + 2.2);
        o.connect(g); g.connect(amb.chimeGain);
        o.start(t + i * 0.12); o.stop(t + i * 0.12 + 2.4);
      });
    }
    function scheduleChime() {
      setTimeout(() => { chimeRing(); scheduleChime(); }, 20000 + Math.random() * 20000); // chuông gió 20–40s
    }
    function playStep() {
      if (!amb || !isAudioOn) return;
      const ctx = amb.ctx, t = ctx.currentTime;
      const len = Math.floor(ctx.sampleRate * 0.09);
      const buf = ctx.createBuffer(1, len, ctx.sampleRate);
      const dd = buf.getChannelData(0);
      for (let i = 0; i < len; i++) dd[i] = (Math.random() * 2 - 1) * (1 - i / len);
      const src = ctx.createBufferSource(); src.buffer = buf;
      const lp = ctx.createBiquadFilter(); lp.type = 'lowpass'; lp.frequency.value = 320;
      const g = ctx.createGain(); g.gain.value = curZone === 'dien' ? 0.06 : 0.14;
      src.connect(lp); lp.connect(g); g.connect(ctx.destination); src.start(t);
    }
    function playFire() {
      if (!isAudioOn) return;
      initAudio();
      const ctx = audioCtx, t = ctx.currentTime;
      const len = Math.floor(ctx.sampleRate * 0.8);
      const buf = ctx.createBuffer(1, len, ctx.sampleRate);
      const dd = buf.getChannelData(0);
      for (let i = 0; i < len; i++) dd[i] = (Math.random() * 2 - 1) * (1 - i / len) * 0.7;
      const src = ctx.createBufferSource(); src.buffer = buf;
      const bp = ctx.createBiquadFilter(); bp.type = 'bandpass'; bp.frequency.value = 900; bp.Q.value = 0.8;
      const g = ctx.createGain(); g.gain.value = 0.5;
      src.connect(bp); bp.connect(g); g.connect(ctx.destination); src.start(t);
    }
    // ---- Giọng dẫn thu sẵn (v5): audio_v5/<key>.mp3 — thiếu file/lỗi thì IM LẶNG ----
    let voiceEl = null;
    function playVoice(key) {
      try {
        if (voiceEl) { voiceEl.pause(); voiceEl = null; }
        const a = new Audio('audio_v5/' + key + '.mp3');
        a.onerror = () => {};
        voiceEl = a;
        const p = a.play();
        if (p && p.catch) p.catch(() => {});
      } catch (e) {}
    }
    window.playVoice = playVoice;
    // Khe vòng niệm Phật chánh điện: CHỈ phát khi có bản ghi THẬT được phép dùng
    // (audio_v5/niem_phat_xa.mp3). Chưa có file -> giữ tĩnh lặng, không thay bằng TTS/tổng hợp.
    let hallChantEl = null, hallChantOk = false;
    window.__setHallChant = function (on) {
      try {
        if (on) {
          if (!hallChantEl) {
            hallChantEl = new Audio('audio_v5/niem_phat_xa.mp3');
            hallChantEl.loop = true; hallChantEl.volume = 0.12; // tiếng tụng xa, rất nhỏ
            hallChantEl.addEventListener('canplaythrough', () => { hallChantOk = true; });
            hallChantEl.onerror = () => { hallChantEl = null; };
          }
          const p = hallChantEl.play();
          if (p && p.catch) p.catch(() => {});
        } else if (hallChantEl) { hallChantEl.pause(); }
      } catch (e) {}
    };
    window.addEventListener('pointerdown', () => { if (isAudioOn) initAmbience(); }, { once: true });

    // ---- Helpers dựng cảnh ----
    function addBox(x, y, z, w, h, d, m, parent) {
      const o = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), m);
      o.position.set(x, y, z);
      o.castShadow = true; o.receiveShadow = true;
      (parent || scene).add(o);
      return o;
    }
    function addCyl(x, y, z, r, h, m, parent, seg) {
      const o = new THREE.Mesh(new THREE.CylinderGeometry(r, r, h, seg || 18), m);
      o.position.set(x, y, z);
      o.castShadow = true; o.receiveShadow = true;
      (parent || scene).add(o);
      return o;
    }
    function addBall(x, y, z, r, m, parent) {
      const o = new THREE.Mesh(new THREE.SphereGeometry(r, 20, 16), m);
      o.position.set(x, y, z);
      o.castShadow = true; o.receiveShadow = true;
      (parent || scene).add(o);
      return o;
    }
    function textTexture(lines, opts) {
      const o = Object.assign({ w: 512, h: 256, bg: '#5A3D26', fg: '#FFD166', font: 'bold 64px Georgia, serif' }, opts || {});
      const cv = document.createElement('canvas'); cv.width = o.w; cv.height = o.h;
      const ctx = cv.getContext('2d');
      ctx.fillStyle = o.bg; ctx.fillRect(0, 0, o.w, o.h);
      ctx.strokeStyle = o.fg; ctx.lineWidth = 6; ctx.strokeRect(10, 10, o.w - 20, o.h - 20);
      ctx.fillStyle = o.fg; ctx.font = o.font; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      const n = lines.length;
      lines.forEach((ln, i) => ctx.fillText(ln, o.w / 2, o.h * (i + 1) / (n + 1)));
      const tex = new THREE.CanvasTexture(cv);
      tex.colorSpace = THREE.SRGBColorSpace;
      return tex;
    }
    function plaque(lines, w, h, opts) {
      const tex = textTexture(lines, opts);
      const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h),
        new THREE.MeshStandardMaterial({ map: tex, roughness: 0.6 }));
      return m;
    }
    function leafTexture(base) {
      const cv = document.createElement('canvas'); cv.width = 256; cv.height = 256;
      const ctx = cv.getContext('2d');
      ctx.clearRect(0, 0, 256, 256);
      for (let i = 0; i < 90; i++) {
        const x = Math.random() * 256, y = Math.random() * 256, r = 8 + Math.random() * 22;
        ctx.fillStyle = base;
        ctx.globalAlpha = 0.55 + Math.random() * 0.45;
        ctx.beginPath(); ctx.ellipse(x, y, r, r * 0.6, Math.random() * 3, 0, 7); ctx.fill();
      }
      ctx.globalAlpha = 1;
      const tex = new THREE.CanvasTexture(cv);
      tex.colorSpace = THREE.SRGBColorSpace;
      return tex;
    }
    const leafTexA = leafTexture('#3E6B34'), leafTexB = leafTexture('#5C8446'), leafTexC = leafTexture('#4E7A3A');
    function roofTexture() {
      const cv = document.createElement('canvas'); cv.width = 256; cv.height = 256;
      const ctx = cv.getContext('2d');
      ctx.fillStyle = '#7C4030'; ctx.fillRect(0, 0, 256, 256);
      for (let y = 0; y < 16; y++) {
        for (let x = 0; x < 16; x++) {
          const v = 0.85 + Math.random() * 0.3;
          ctx.fillStyle = `rgb(${Math.floor(124 * v)},${Math.floor(64 * v)},${Math.floor(48 * v)})`;
          ctx.fillRect(x * 16, y * 16, 15, 15);
        }
      }
      const tex = new THREE.CanvasTexture(cv);
      tex.wrapS = tex.wrapT = THREE.RepeatWrapping; tex.colorSpace = THREE.SRGBColorSpace;
      return tex;
    }
    const roofTex = roofTexture();
    function pavingTexture() {
      const cv = document.createElement('canvas'); cv.width = 256; cv.height = 256;
      const ctx = cv.getContext('2d');
      ctx.fillStyle = '#B4A68C'; ctx.fillRect(0, 0, 256, 256);
      for (let y = 0; y < 8; y++) for (let x = 0; x < 8; x++) {
        const v = 0.88 + Math.random() * 0.24;
        ctx.fillStyle = `rgb(${Math.floor(186 * v)},${Math.floor(170 * v)},${Math.floor(140 * v)})`;
        ctx.fillRect(x * 32 + 1, y * 32 + 1, 30, 30);
      }
      const tex = new THREE.CanvasTexture(cv);
      tex.wrapS = tex.wrapT = THREE.RepeatWrapping; tex.colorSpace = THREE.SRGBColorSpace;
      return tex;
    }
    const pavingTex = pavingTexture();
