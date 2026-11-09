
    // ---- Scene + grade D2 (audit) ----
    const canvas = document.getElementById('three-canvas');
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x7fb2e5);
    scene.fog = new THREE.FogExp2(0x2a1a10, 0.007);
    const camera = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 0.1, 600);
    camera.position.set(23, 4.5, 52);
    camera.lookAt(23, 2, 38);
    const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, powerPreference: 'high-performance' });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.02;
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    // Layered lights: layer 0 ngoài sân / layer 1 nội điện (tối hơn một bậc)
    const hemi = new THREE.HemisphereLight(0xfff2d9, 0x5e4a35, 1.15);
    hemi.layers.set(0);
    scene.add(hemi);
    const sun = new THREE.DirectionalLight(0xffd9a3, 1.5);
    sun.position.set(-30, 25, 18); // nắng thấp phía tây
    sun.castShadow = true;
    sun.shadow.mapSize.width = 2048; sun.shadow.mapSize.height = 2048;
    sun.shadow.camera.left = -60; sun.shadow.camera.right = 60;
    sun.shadow.camera.top = 60; sun.shadow.camera.bottom = -60;
    sun.shadow.camera.far = 120;
    sun.layers.set(0);
    scene.add(sun);
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
      ctx.fillStyle = '#8A7A63'; ctx.fillRect(0, 0, 256, 256);
      for (let y = 0; y < 8; y++) for (let x = 0; x < 8; x++) {
        const v = 0.88 + Math.random() * 0.24;
        ctx.fillStyle = `rgb(${Math.floor(138 * v)},${Math.floor(122 * v)},${Math.floor(99 * v)})`;
        ctx.fillRect(x * 32 + 1, y * 32 + 1, 30, 30);
      }
      const tex = new THREE.CanvasTexture(cv);
      tex.wrapS = tex.wrapT = THREE.RepeatWrapping; tex.colorSpace = THREE.SRGBColorSpace;
      return tex;
    }
    const pavingTex = pavingTexture();
