import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { clone as skeletonClone } from 'three/addons/utils/SkeletonUtils.js';
import { PILGRIMAGE_STATIONS, CHARACTER_PROFILES } from '/src/logic/chua-online-logic.mjs';

export class VinhTrang3DWorld {
  constructor(canvas, callbacks = {}) {
    this.canvas = canvas;
    this.callbacks = callbacks; // { onStationReached, onStationArrive, onStationProximity, onPinClick }
    this.isSoftwareGl = this.detectSoftwareGl();

    this.scene = null;
    this.camera = null;
    this.renderer = null;
    this.clock = new THREE.Clock();

    // World groups
    this.grounds = new THREE.Group();
    this.interiorGroup = new THREE.Group();
    this.insideInterior = false;

    // Colliders
    this.colRects = [];
    this.colCircles = [];

    // Animated elements
    this.fishes = [];
    this.lotusFlowers = [];
    this.smokeParticles = [];
    this.leafParticles = [];
    this.npcs = [];
    this.charTemplates = {};
    this.charRegistry = [];

    // Player & Companion state (Spawn on main courtyard avenue facing Chánh Điện, with Lotus Pond visible)
    this.player = {
      pos: new THREE.Vector3(23, 0, 22),
      yaw: Math.PI,
      camYaw: 0,
      camPitch: 0.24,
      camDist: 6.4,
      speed: 4.2,
      target: null,
      moving: false,
      profileKey: callbacks.initialCharKey || 'nu',
      hatEquipped: false,
      bowTimer: 0,
      incenseLit: false
    };
    this.playerAv = null;
    this.companionAv = null;
    this.companionPos = new THREE.Vector3(21.4, 0, 23.4);
    this.companionYaw = Math.PI;

    // Auto-walk pathing
    this.autoWalk = null;
    this.trailLine = null;
    this.destRing = null;

    // Input state
    this.keys = {};
    this.dpadDir = { dx: 0, dz: 0 };
    this.dragging = false;
    this.pointerDownPos = { x: 0, y: 0, t: 0 };
    this.lastPointer = { x: 0, y: 0 };

    // Reusable scratch vectors (Zero-GC loop)
    this._projVec = new THREE.Vector3();
    this._camTarget = new THREE.Vector3();
    this._lookTarget = new THREE.Vector3();
    this._raycaster = new THREE.Raycaster();
    this._groundPlane = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0);
    this._clickPt = new THREE.Vector3();

    this.frameId = 0;
    this.simTime = 0;
    this.lastPinSync = 0;
    this.nearestStationId = 5;
  }

  get playerPos() {
    return this.player.pos;
  }

  get playerYaw() {
    return this.player.yaw;
  }

  get playerMoving() {
    return this.player.moving;
  }

  detectSoftwareGl() {
    try {
      const probeCanvas = document.createElement('canvas');
      const gl = probeCanvas.getContext('webgl2') || probeCanvas.getContext('webgl');
      if (!gl) return true;
      const ext = gl.getExtension('WEBGL_debug_renderer_info');
      const param = ext ? ext.UNMASKED_RENDERER_WEBGL : gl.RENDERER;
      const gpu = String(gl.getParameter(param) || '');
      gl.getExtension('WEBGL_lose_context')?.loseContext();
      return /SwiftShader|llvmpipe|softpipe|Software|Basic Render/i.test(gpu);
    } catch {
      return true;
    }
  }

  init() {
    if (!this.canvas) return;

    this.renderer = new THREE.WebGLRenderer({
      canvas: this.canvas,
      antialias: !this.isSoftwareGl,
      powerPreference: 'high-performance',
      preserveDrawingBuffer: true
    });
    this.renderer.outputColorSpace = THREE.SRGBColorSpace;
    this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
    this.renderer.toneMappingExposure = 1.12;
    this.renderer.setPixelRatio(this.isSoftwareGl ? 1 : Math.min(window.devicePixelRatio || 1, 2));
    this.renderer.setSize(window.innerWidth, window.innerHeight);
    this.renderer.shadowMap.enabled = !this.isSoftwareGl;
    this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;

    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(0x78b9eb);
    this.scene.fog = new THREE.FogExp2(0xd6ebfa, 0.0065);

    this.camera = new THREE.PerspectiveCamera(48, window.innerWidth / window.innerHeight, 0.25, 260);

    // Warm/Cool Lighting Rig
    const hemi = new THREE.HemisphereLight(0xdff2ff, 0x8f7e62, 1.15);
    this.scene.add(hemi);

    const sun = new THREE.DirectionalLight(0xffe6b8, 1.85);
    sun.position.set(28, 46, 32);
    if (!this.isSoftwareGl) {
      sun.castShadow = true;
      sun.shadow.mapSize.set(1024, 1024);
      sun.shadow.camera.near = 2;
      sun.shadow.camera.far = 140;
      const d = 55;
      sun.shadow.camera.left = -d;
      sun.shadow.camera.right = d;
      sun.shadow.camera.top = d;
      sun.shadow.camera.bottom = -d;
      sun.shadow.bias = -0.0005;
    }
    this.scene.add(sun);

    this.scene.add(this.grounds);
    this.interiorGroup.position.set(300, 0, 300);
    this.interiorGroup.visible = false;
    this.scene.add(this.interiorGroup);

    this.buildTempleGrounds();
    this.buildInteriorHall();
    this.setupAvatarsAndNPCs();
    this.loadAllGLBAssets();
    this.bindInputs();

    this.snapCamera();
    this.startLoop();
  }

  mat(color, roughness = 0.72, metalness = 0.06, extra = {}) {
    return new THREE.MeshStandardMaterial({ color, roughness, metalness, ...extra });
  }

  createPlaqueTexture(text, subText = '', bg = '#5b1912', fg = '#f7d274') {
    const cv = document.createElement('canvas');
    cv.width = 512;
    cv.height = 160;
    const ctx = cv.getContext('2d');
    ctx.fillStyle = bg;
    ctx.fillRect(0, 0, 512, 160);
    ctx.strokeStyle = fg;
    ctx.lineWidth = 8;
    ctx.strokeRect(8, 8, 496, 144);
    ctx.fillStyle = fg;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.font = 'bold 42px "Be Vietnam Pro", Georgia, serif';
    ctx.fillText(text, 256, subText ? 64 : 80);
    if (subText) {
      ctx.font = '600 24px "Be Vietnam Pro", Georgia, serif';
      ctx.fillText(subText, 256, 114);
    }
    const tex = new THREE.CanvasTexture(cv);
    tex.colorSpace = THREE.SRGBColorSpace;
    return tex;
  }

  /* ========================================================================
     1. BUILD WALKABLE 3D CHÙA VĨNH TRÀNG GROUNDS
     ======================================================================== */
  buildTempleGrounds() {
    // 1. Extended lush grass terrain & stone courtyard avenue
    const grass = new THREE.Mesh(
      new THREE.PlaneGeometry(240, 240),
      this.mat(0x6f9459, 0.92, 0.02)
    );
    grass.rotation.x = -Math.PI / 2;
    grass.position.y = -0.02;
    grass.receiveShadow = true;
    this.grounds.add(grass);

    // Main Stone Courtyard & Paving Avenue (Matches grey-warm granite slabs in Ref Image 1)
    const mainPaving = new THREE.Mesh(
      new THREE.PlaneGeometry(34, 56),
      this.mat(0xb8b2aa, 0.82, 0.05)
    );
    mainPaving.rotation.x = -Math.PI / 2;
    mainPaving.position.set(23, 0.01, 18);
    mainPaving.receiveShadow = true;
    this.grounds.add(mainPaving);

    // Subtle stone tile grid lines on courtyard
    const gridHelper = new THREE.GridHelper(34, 17, 0x999289, 0xa39c93);
    gridHelper.position.set(23, 0.018, 18);
    this.grounds.add(gridHelper);

    // Western & Eastern Garden Paths connecting to A Di Đà, Di Lặc, Niết Bàn, Bảo Tháp, Giảng Đường
    const westPath = new THREE.Mesh(
      new THREE.PlaneGeometry(46, 7),
      this.mat(0xc4b89f, 0.85, 0.04)
    );
    westPath.rotation.x = -Math.PI / 2;
    westPath.position.set(-4, 0.012, 22);
    this.grounds.add(westPath);

    const dilacPath = new THREE.Mesh(
      new THREE.PlaneGeometry(8, 32),
      this.mat(0xc4b89f, 0.85, 0.04)
    );
    dilacPath.rotation.x = -Math.PI / 2;
    dilacPath.position.set(-22, 0.012, 10);
    this.grounds.add(dilacPath);

    const northPath = new THREE.Mesh(
      new THREE.PlaneGeometry(9, 48),
      this.mat(0xc4b89f, 0.85, 0.04)
    );
    northPath.rotation.x = -Math.PI / 2;
    northPath.position.set(8, 0.012, -20);
    this.grounds.add(northPath);

    // 2. Two Walkable Lotus Ponds with Koi Fish, Blooming Lotuses & Stone Bridges
    this.buildLotusPond(5, 16, 15.5, 13.5, 'Hồ Sen Tây (Liên Trì)');
    this.buildLotusPond(41, 16, 15.5, 13.5, 'Hồ Sen Đông (Bạch Liên)');

    // 3. 13-Arch Chánh Điện Chùa Vĩnh Tràng (Iconic East-West Yellow Facade from Ref Image 1)
    this.buildMainHallFacade();

    // 4. Bronze Incense Burner (`Lư Hương Sân Chánh Điện`) & Kneeling Cushions
    this.buildCourtyardBurner();

    // 5. Cổng Tam Quan Ghép Sành Sứ & Sạp Nhang Hoa
    this.buildTamQuanGate(23, 43, 'CỔNG PHƯƠNG TIỆN');
    this.buildIncenseStall(33.5, 44.5);

    // 6. Quầy Cửa Hàng Lưu Niệm Gỗ 3D (`image_43ca3fb3.png`)
    this.buildSouvenirShopKiosk3D(40, 35.5);

    // 7. Giảng Đường Phật Pháp Huệ Đăng & Phòng Kinh Sách
    this.buildLectureHall3D(43, -16);

    // 8. Great Buddha Statues & 7-Story Stupa (Procedural + GLB Loaded)
    this.buildStandingAdidaMonument(-14, 27);
    this.buildSeatedDiLacMonument(-24, -2);
    this.buildQuanAmPavilion(-26, 21);
    this.buildRecliningNirvanaMonument(12, -43);
    this.buildSevenTierStupa(-4, -39);

    // 9. Bougainvillea Pots, Trimmed Cloud Bonsai & Stone Benches flanking the Courtyard (Matches Ref Image 1)
    this.buildCourtyardFloraAndBenches();

    // 10. Falling Golden Leaves
    const leafGeo = new THREE.PlaneGeometry(0.14, 0.09);
    const leafMat = this.mat(0xe6b44c, 0.7, 0.05, { side: THREE.DoubleSide });
    for (let i = 0; i < 28; i++) {
      const m = new THREE.Mesh(leafGeo, leafMat);
      m.position.set(10 + Math.random() * 26, 1 + Math.random() * 5, 4 + Math.random() * 30);
      this.grounds.add(m);
      this.leafParticles.push({
        mesh: m,
        speed: 0.35 + Math.random() * 0.35,
        seed: Math.random() * 10
      });
    }
  }

  buildLotusPond(cx, cz, w, d, labelText) {
    const pond = new THREE.Group();
    pond.position.set(cx, 0, cz);

    const wallMat = this.mat(0xd7c59f, 0.75);
    const trimMat = this.mat(0xc8963e, 0.45, 0.3);
    const waterMat = this.mat(0x286e5e, 0.18, 0.15);

    // Pond stone walls
    const wallN = new THREE.Mesh(new THREE.BoxGeometry(w + 0.6, 0.55, 0.42), wallMat);
    wallN.position.set(0, 0.26, -d / 2);
    const wallS = wallN.clone();
    wallS.position.z = d / 2;
    const wallW = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.55, d + 0.6), wallMat);
    wallW.position.set(-w / 2, 0.26, 0);
    const wallE = wallW.clone();
    wallE.position.x = w / 2;
    pond.add(wallN, wallS, wallW, wallE);

    // Water surface
    const water = new THREE.Mesh(new THREE.PlaneGeometry(w - 0.3, d - 0.3), waterMat);
    water.rotation.x = -Math.PI / 2;
    water.position.y = 0.16;
    pond.add(water);

    // Center miniature rockery & fountain lotus
    const rock = new THREE.Mesh(new THREE.DodecahedronGeometry(0.95, 1), this.mat(0x6d685f, 0.88));
    rock.position.set(0, 0.55, 0);
    rock.scale.set(1.2, 0.9, 1.1);
    pond.add(rock);

    // Arched viewing bridge on courtyard edge
    const bridgeDeck = new THREE.Mesh(new THREE.BoxGeometry(3.2, 0.18, 2.2), this.mat(0xd9c29c, 0.7));
    bridgeDeck.position.set(cx < 23 ? w / 2 - 0.8 : -w / 2 + 0.8, 0.48, 0);
    pond.add(bridgeDeck);

    // 28 Lotus Pads & 18 Blooming Pink Lotus Flowers
    const padMat = this.mat(0x2e6f3e, 0.75);
    const petalPink = this.mat(0xf78fb3, 0.45);
    const petalLight = this.mat(0xfbc3d8, 0.45);
    const pistilGold = this.mat(0xf5c842, 0.4, 0.3);

    for (let i = 0; i < 24; i++) {
      const ang = (i / 24) * Math.PI * 2 + (i % 3) * 0.2;
      const rad = 1.6 + (i % 5) * 0.95;
      const lx = Math.cos(ang) * rad * 1.15;
      const lz = Math.sin(ang) * rad * 0.95;

      const pad = new THREE.Mesh(new THREE.CylinderGeometry(0.38, 0.38, 0.02, 14), padMat);
      pad.position.set(lx, 0.19, lz);
      pond.add(pad);

      if (i % 3 !== 0) {
        const flower = new THREE.Group();
        flower.position.set(lx, 0.24, lz);
        for (let p = 0; p < 6; p++) {
          const pa = (p / 6) * Math.PI * 2;
          const petal = new THREE.Mesh(
            new THREE.ConeGeometry(0.09, 0.22, 6),
            p % 2 === 0 ? petalPink : petalLight
          );
          petal.position.set(Math.cos(pa) * 0.08, 0.06, Math.sin(pa) * 0.08);
          petal.rotation.z = -Math.cos(pa) * 0.45;
          petal.rotation.x = Math.sin(pa) * 0.45;
          flower.add(petal);
        }
        const center = new THREE.Mesh(new THREE.SphereGeometry(0.055, 8, 8), pistilGold);
        center.position.y = 0.08;
        flower.add(center);
        pond.add(flower);
        this.lotusFlowers.push({ group: flower, baseY: 0.24, seed: i * 0.7 });
      }
    }

    // 10 Swimming Koi Fish per pond
    const koiColors = [0xff5722, 0xff9800, 0xf5f5f5, 0xe63946, 0xffb703];
    for (let k = 0; k < 10; k++) {
      const fishGroup = new THREE.Group();
      const body = new THREE.Mesh(
        new THREE.ConeGeometry(0.08, 0.34, 8),
        this.mat(koiColors[k % koiColors.length], 0.35)
      );
      body.rotation.x = Math.PI / 2;
      fishGroup.add(body);
      const tail = new THREE.Mesh(
        new THREE.ConeGeometry(0.06, 0.14, 4),
        this.mat(0xffffff, 0.4)
      );
      tail.rotation.x = -Math.PI / 2;
      tail.position.z = -0.2;
      fishGroup.add(tail);
      fishGroup.position.y = 0.14;
      pond.add(fishGroup);
      this.fishes.push({
        mesh: fishGroup,
        ang: k * 0.65,
        r: 1.8 + (k % 4) * 1.1,
        sp: (0.42 + (k % 3) * 0.14) * (k % 2 ? 1 : -1)
      });
    }

    // Wooden sign by the pond
    const signBoard = new THREE.Mesh(
      new THREE.BoxGeometry(2.1, 0.52, 0.08),
      new THREE.MeshBasicMaterial({ map: this.createPlaqueTexture(labelText, 'Dạo bước ngắm sen & cá Koi') })
    );
    signBoard.position.set(cx < 23 ? w / 2 + 0.4 : -w / 2 - 0.4, 1.15, d / 2 - 1.2);
    pond.add(signBoard);

    this.grounds.add(pond);
    this.colRects.push([cx - w / 2, cz - d / 2, cx + w / 2, cz + d / 2]);
  }

  buildMainHallFacade() {
    const hall = new THREE.Group();
    hall.position.set(23, 0, -6);

    const yellowWall = this.mat(0xf5c869, 0.55, 0.08);
    const creamTrim = this.mat(0xfff3d6, 0.5, 0.05);
    const bluePorcelain = this.mat(0x4b83a8, 0.4, 0.15);
    const terracottaRoof = this.mat(0xc85a28, 0.52, 0.08);
    const darkWood = this.mat(0x4e2b15, 0.65);
    const goldMat = this.mat(0xeab646, 0.28, 0.68);

    // Stepped Stone Platform (`Thềm Tam Cấp Chánh Điện`)
    const basePlatform = new THREE.Mesh(new THREE.BoxGeometry(28.5, 1.1, 14.5), this.mat(0xd7c8ad, 0.75));
    basePlatform.position.set(0, 0.55, 0);
    basePlatform.receiveShadow = true;
    hall.add(basePlatform);

    // Central Granite Staircase (7 steps with golden balustrades as in Ref Image 1)
    for (let s = 0; s < 6; s++) {
      const step = new THREE.Mesh(
        new THREE.BoxGeometry(5.6, 0.18, 0.42),
        this.mat(0x9ca3af, 0.72)
      );
      step.position.set(0, 0.09 + s * 0.18, 9.4 - s * 0.4);
      hall.add(step);
    }
    [-2.9, 2.9].forEach((bx) => {
      const rail = new THREE.Mesh(new THREE.BoxGeometry(0.28, 0.85, 2.8), yellowWall);
      rail.position.set(bx, 0.75, 8.3);
      hall.add(rail);
    });

    // Main Hall Body
    const mainBody = new THREE.Mesh(new THREE.BoxGeometry(26.5, 6.2, 11.5), yellowWall);
    mainBody.position.set(0, 4.1, -0.5);
    mainBody.castShadow = true;
    mainBody.receiveShadow = true;
    hall.add(mainBody);

    // 11 Front Roman Columns & Arches along Veranda
    for (let i = -5; i <= 5; i++) {
      const cx = i * 2.35;
      const col = new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.25, 4.8, 14), yellowWall);
      col.position.set(cx, 3.5, 6.4);
      hall.add(col);

      const cap = new THREE.Mesh(new THREE.BoxGeometry(0.62, 0.28, 0.62), creamTrim);
      cap.position.set(cx, 5.95, 6.4);
      hall.add(cap);

      if (i < 5) {
        const archBeam = new THREE.Mesh(new THREE.BoxGeometry(2.35, 0.9, 0.48), yellowWall);
        archBeam.position.set(cx + 1.175, 5.8, 6.4);
        hall.add(archBeam);

        const frieze = new THREE.Mesh(new THREE.BoxGeometry(1.85, 0.46, 0.54), bluePorcelain);
        frieze.position.set(cx + 1.175, 6.55, 6.42);
        hall.add(frieze);
      }
    }

    // 3 Elaborate Front Pediments / Towers (Central + Left + Right matching Ref Image 1)
    const towers = [
      { x: 0, w: 7.4, h: 4.8 },
      { x: -9.4, w: 4.8, h: 3.2 },
      { x: 9.4, w: 4.8, h: 3.2 }
    ];
    towers.forEach((tw) => {
      const ped = new THREE.Mesh(new THREE.BoxGeometry(tw.w, tw.h, 2.6), yellowWall);
      ped.position.set(tw.x, 7.2 + tw.h * 0.4, 5.6);
      hall.add(ped);

      const spire = new THREE.Mesh(new THREE.ConeGeometry(tw.w * 0.58, 2.2, 4), terracottaRoof);
      spire.rotation.y = Math.PI / 4;
      spire.position.set(tw.x, 7.2 + tw.h * 0.88, 5.6);
      hall.add(spire);

      const finial = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.24, 1.1, 10), goldMat);
      finial.position.set(tw.x, 8.4 + tw.h * 0.88, 5.6);
      hall.add(finial);
    });

    // Plaque "CHÙA VĨNH TRÀNG"
    const plaque = new THREE.Mesh(
      new THREE.PlaneGeometry(4.6, 1.15),
      new THREE.MeshBasicMaterial({
        map: this.createPlaqueTexture('CHÙA VĨNH TRÀNG', 'Di Tích Lịch Sử Văn Hóa Quốc Gia')
      })
    );
    plaque.position.set(0, 6.65, 6.72);
    hall.add(plaque);

    // Glowing Golden Buddha visible inside the central doorway arch (just like Ref Image 1!)
    const doorwayRecess = new THREE.Mesh(new THREE.BoxGeometry(2.8, 3.8, 0.8), darkWood);
    doorwayRecess.position.set(0, 3.0, 5.2);
    hall.add(doorwayRecess);

    const innerBuddha = new THREE.Group();
    innerBuddha.position.set(0, 2.3, 5.45);
    const lotusBase = new THREE.Mesh(new THREE.CylinderGeometry(0.55, 0.68, 0.35, 16), goldMat);
    const torso = new THREE.Mesh(new THREE.ConeGeometry(0.42, 1.05, 14), goldMat);
    torso.position.y = 0.65;
    const head = new THREE.Mesh(new THREE.SphereGeometry(0.22, 14, 14), goldMat);
    head.position.y = 1.32;
    const halo = new THREE.Mesh(
      new THREE.RingGeometry(0.32, 0.48, 24),
      new THREE.MeshBasicMaterial({ color: 0xffe484, side: THREE.DoubleSide })
    );
    halo.position.set(0, 1.32, -0.15);
    innerBuddha.add(lotusBase, torso, head, halo);
    hall.add(innerBuddha);

    this.grounds.add(hall);
    this.colRects.push([9, -13, 37, 5.8]);
  }

  buildCourtyardBurner() {
    const burner = new THREE.Group();
    burner.position.set(23, 0, 11);

    const bronze = this.mat(0x5e4934, 0.42, 0.55);
    const gold = this.mat(0xd8a33e, 0.32, 0.65);

    const ped = new THREE.Mesh(new THREE.BoxGeometry(1.8, 0.26, 1.4), this.mat(0x9e9589, 0.8));
    ped.position.y = 0.13;
    burner.add(ped);

    const body = new THREE.Mesh(new THREE.CylinderGeometry(0.62, 0.52, 0.92, 20), bronze);
    body.position.y = 0.82;
    burner.add(body);

    const rim = new THREE.Mesh(new THREE.TorusGeometry(0.62, 0.06, 10, 24), gold);
    rim.rotation.x = Math.PI / 2;
    rim.position.y = 1.28;
    burner.add(rim);

    // 3 Glowing Incense Sticks
    this.incenseSticksGroup = new THREE.Group();
    [-0.12, 0, 0.12].forEach((ix) => {
      const stick = new THREE.Mesh(new THREE.CylinderGeometry(0.014, 0.014, 0.55, 6), this.mat(0xb8332a, 0.7));
      stick.position.set(ix, 1.48, 0);
      const tip = new THREE.Mesh(
        new THREE.SphereGeometry(0.025, 8, 8),
        new THREE.MeshBasicMaterial({ color: 0xff5722 })
      );
      tip.position.set(ix, 1.76, 0);
      this.incenseSticksGroup.add(stick, tip);
    });
    burner.add(this.incenseSticksGroup);

    // Smoke Particles above Burner
    const smokeGeo = new THREE.SphereGeometry(0.14, 8, 8);
    const smokeMat = new THREE.MeshBasicMaterial({
      color: 0xfff8eb,
      transparent: true,
      opacity: 0.28,
      depthWrite: false
    });
    for (let i = 0; i < 14; i++) {
      const sp = new THREE.Mesh(smokeGeo, smokeMat.clone());
      sp.position.set(23 + (Math.random() - 0.5) * 0.25, 1.8 + (i / 14) * 2.2, 11 + (Math.random() - 0.5) * 0.25);
      this.grounds.add(sp);
      this.smokeParticles.push({ mesh: sp, offset: i * 0.45 });
    }

    // 2 Kneeling Lotus Cushions (`Bồ đoàn lễ Phật`) beside the burner
    [-1.8, 1.8].forEach((kx) => {
      const cushion = new THREE.Mesh(new THREE.CylinderGeometry(0.45, 0.48, 0.16, 18), this.mat(0x8c2d19, 0.75));
      cushion.position.set(kx, 0.08, 1.8);
      burner.add(cushion);
    });

    this.grounds.add(burner);
    this.colCircles.push([23, 11, 1.1]);
  }

  buildTamQuanGate(gx, gz, title) {
    const gate = new THREE.Group();
    gate.position.set(gx, 0, gz);

    const mosaicMat = this.mat(0xe5c168, 0.48, 0.15);
    const roofMat = this.mat(0xc04a22, 0.55);

    [-4.6, -1.8, 1.8, 4.6].forEach((px, idx) => {
      const h = idx === 1 || idx === 2 ? 6.2 : 4.8;
      const pillar = new THREE.Mesh(new THREE.BoxGeometry(0.72, h, 0.72), mosaicMat);
      pillar.position.set(px, h / 2, 0);
      pillar.castShadow = true;
      gate.add(pillar);
    });

    const mainBeam = new THREE.Mesh(new THREE.BoxGeometry(10.6, 0.95, 1.1), mosaicMat);
    mainBeam.position.set(0, 5.2, 0);
    gate.add(mainBeam);

    const upperRoof = new THREE.Mesh(new THREE.ConeGeometry(4.2, 1.8, 4), roofMat);
    upperRoof.rotation.y = Math.PI / 4;
    upperRoof.scale.set(1.3, 1, 0.65);
    upperRoof.position.set(0, 6.9, 0);
    gate.add(upperRoof);

    const sign = new THREE.Mesh(
      new THREE.PlaneGeometry(3.8, 0.85),
      new THREE.MeshBasicMaterial({ map: this.createPlaqueTexture(title, 'Chùa Vĩnh Tràng · 1849') })
    );
    sign.position.set(0, 5.25, -0.58);
    sign.rotation.y = Math.PI;
    gate.add(sign);

    this.grounds.add(gate);
  }

  buildIncenseStall(sx, sz) {
    const stall = new THREE.Group();
    stall.position.set(sx, 0, sz);
    const table = new THREE.Mesh(new THREE.BoxGeometry(2.6, 0.85, 1.4), this.mat(0x7c4d25, 0.7));
    table.position.y = 0.425;
    stall.add(table);
    const roof = new THREE.Mesh(new THREE.ConeGeometry(2.3, 0.9, 4), this.mat(0xb84a24, 0.6));
    roof.rotation.y = Math.PI / 4;
    roof.position.y = 2.4;
    stall.add(roof);
    this.grounds.add(stall);
    this.colRects.push([sx - 1.4, sz - 0.8, sx + 1.4, sz + 0.8]);
  }

  buildSouvenirShopKiosk3D(kx, kz) {
    const kiosk = new THREE.Group();
    kiosk.position.set(kx, 0, kz);
    kiosk.rotation.y = -Math.PI / 6;

    const woodDark = this.mat(0x6b3e1e, 0.65);
    const woodWarm = this.mat(0x9c5e2c, 0.55);
    const tileTerracotta = this.mat(0xc85a28, 0.5);
    const goldMat = this.mat(0xe6b84c, 0.3, 0.65);
    const pinkLantern = this.mat(0xf78fb3, 0.4, 0.1, { emissive: 0xff6b9d, emissiveIntensity: 0.4 });

    const base = new THREE.Mesh(new THREE.BoxGeometry(4.6, 0.22, 3.0), woodDark);
    base.position.y = 0.11;
    kiosk.add(base);

    const counter = new THREE.Mesh(new THREE.BoxGeometry(4.0, 1.05, 1.25), woodWarm);
    counter.position.set(0, 0.64, 0.55);
    kiosk.add(counter);

    [
      [-1.9, 1.1],
      [1.9, 1.1],
      [-1.9, -1.0],
      [1.9, -1.0]
    ].forEach(([cx, cz]) => {
      const col = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.16, 3.2, 14), woodDark);
      col.position.set(cx, 1.7, cz);
      kiosk.add(col);
    });

    const roof = new THREE.Mesh(new THREE.ConeGeometry(3.8, 1.35, 4), tileTerracotta);
    roof.position.set(0, 3.85, 0);
    roof.rotation.y = Math.PI / 4;
    roof.scale.set(1.25, 1, 0.9);
    kiosk.add(roof);

    const sign = new THREE.Mesh(
      new THREE.PlaneGeometry(2.8, 0.78),
      new THREE.MeshBasicMaterial({
        map: this.createPlaqueTexture('CỬA HÀNG LƯU NIỆM', 'Quà lưu niệm · Đồ tu học · Vật phẩm 3D')
      })
    );
    sign.position.set(0, 2.95, 1.22);
    kiosk.add(sign);

    [-1.6, 1.6].forEach((lx) => {
      const lantern = new THREE.Mesh(new THREE.SphereGeometry(0.28, 14, 12), pinkLantern);
      lantern.scale.set(1, 0.82, 1);
      lantern.position.set(lx, 2.65, 1.18);
      kiosk.add(lantern);
    });

    const miniBuddha = new THREE.Mesh(new THREE.ConeGeometry(0.28, 0.7, 14), goldMat);
    miniBuddha.position.set(0, 1.65, -0.4);
    kiosk.add(miniBuddha);

    this.grounds.add(kiosk);
    this.colRects.push([kx - 2.4, kz - 1.8, kx + 2.4, kz + 1.8]);
  }

  buildLectureHall3D(lx, lz) {
    const hall = new THREE.Group();
    hall.position.set(lx, 0, lz);

    const wall = new THREE.Mesh(new THREE.BoxGeometry(12, 4.8, 8.5), this.mat(0xf2d399, 0.65));
    wall.position.y = 2.4;
    hall.add(wall);

    const roof = new THREE.Mesh(new THREE.ConeGeometry(9.2, 2.6, 4), this.mat(0xb84a24, 0.55));
    roof.rotation.y = Math.PI / 4;
    roof.scale.set(1.25, 1, 0.92);
    roof.position.y = 6.1;
    hall.add(roof);

    const sign = new THREE.Mesh(
      new THREE.PlaneGeometry(4.2, 0.95),
      new THREE.MeshBasicMaterial({
        map: this.createPlaqueTexture('GIẢNG ĐƯỜNG PHẬT PHÁP', '24 Bài Học & 10 Giáo Trình Kinh Điển')
      })
    );
    sign.position.set(0, 3.8, 4.32);
    hall.add(sign);

    this.grounds.add(hall);
    this.colRects.push([lx - 6.2, lz - 4.4, lx + 6.2, lz + 4.4]);
  }

  buildStandingAdidaMonument(x, z) {
    const g = new THREE.Group();
    g.position.set(x, 0, z);
    const whiteMarble = this.mat(0xfbfaf7, 0.35, 0.05);
    const pinkLotus = this.mat(0xf2a6be, 0.48);

    // Fallback procedural statue + pedestal (replaced seamlessly when phat-dung-adida.glb finishes loading)
    this.adidaFallback = new THREE.Group();
    const baseOct = new THREE.Mesh(new THREE.CylinderGeometry(3.6, 4.4, 2.6, 8), this.mat(0xe5dec9, 0.7));
    baseOct.position.y = 1.3;
    const lotusThrone = new THREE.Mesh(new THREE.CylinderGeometry(2.4, 1.9, 1.1, 16), pinkLotus);
    lotusThrone.position.y = 3.15;
    const robe = new THREE.Mesh(new THREE.CylinderGeometry(0.95, 1.45, 7.2, 18), whiteMarble);
    robe.position.y = 7.2;
    const head = new THREE.Mesh(new THREE.SphereGeometry(0.78, 16, 16), whiteMarble);
    head.position.y = 11.4;
    this.adidaFallback.add(baseOct, lotusThrone, robe, head);
    g.add(this.adidaFallback);

    this.adidaMount = g;
    this.grounds.add(g);
    this.colCircles.push([x, z, 4.2]);
  }

  buildSeatedDiLacMonument(x, z) {
    const g = new THREE.Group();
    g.position.set(x, 0, z);
    const whiteMarble = this.mat(0xfbfaf7, 0.35, 0.05);

    this.dilacFallback = new THREE.Group();
    const ped = new THREE.Mesh(new THREE.BoxGeometry(8.5, 2.2, 6.8), this.mat(0xe3d8be, 0.72));
    ped.position.y = 1.1;
    const belly = new THREE.Mesh(new THREE.SphereGeometry(2.6, 18, 16), whiteMarble);
    belly.scale.set(1.25, 0.95, 1.1);
    belly.position.y = 4.2;
    const head = new THREE.Mesh(new THREE.SphereGeometry(1.05, 16, 16), whiteMarble);
    head.position.y = 6.9;
    this.dilacFallback.add(ped, belly, head);
    g.add(this.dilacFallback);

    this.dilacMount = g;
    this.grounds.add(g);
    this.colRects.push([x - 4.5, z - 3.6, x + 4.5, z + 3.6]);
  }

  buildQuanAmPavilion(x, z) {
    const g = new THREE.Group();
    g.position.set(x, 0, z);
    const whiteMat = this.mat(0xfaf8f2, 0.35);
    const base = new THREE.Mesh(new THREE.CylinderGeometry(1.5, 1.9, 1.4, 12), this.mat(0xd7c8ad, 0.7));
    base.position.y = 0.7;
    const body = new THREE.Mesh(new THREE.CylinderGeometry(0.45, 0.7, 3.2, 14), whiteMat);
    body.position.y = 2.9;
    const head = new THREE.Mesh(new THREE.SphereGeometry(0.35, 12, 12), whiteMat);
    head.position.y = 4.75;
    g.add(base, body, head);
    this.grounds.add(g);
    this.colCircles.push([x, z, 2.0]);
  }

  buildRecliningNirvanaMonument(x, z) {
    const g = new THREE.Group();
    g.position.set(x, 0, z);
    const whiteMarble = this.mat(0xfbfaf7, 0.36, 0.05);

    this.nirvanaFallback = new THREE.Group();
    const platform = new THREE.Mesh(new THREE.BoxGeometry(16.5, 2.0, 5.6), this.mat(0xe5dbc4, 0.72));
    platform.position.y = 1.0;
    const body = new THREE.Mesh(new THREE.CylinderGeometry(1.1, 1.35, 11.5, 16), whiteMarble);
    body.rotation.z = Math.PI / 2;
    body.position.set(0.5, 3.1, 0);
    const head = new THREE.Mesh(new THREE.SphereGeometry(0.95, 16, 16), whiteMarble);
    head.position.set(-5.6, 3.6, 0);
    this.nirvanaFallback.add(platform, body, head);
    g.add(this.nirvanaFallback);

    this.nirvanaMount = g;
    this.grounds.add(g);
    this.colRects.push([x - 8.5, z - 3.2, x + 8.5, z + 3.2]);
  }

  buildSevenTierStupa(x, z) {
    const stupa = new THREE.Group();
    stupa.position.set(x, 0, z);
    const wallMat = this.mat(0xf3d48c, 0.55);
    const roofMat = this.mat(0xc44d24, 0.52);
    const goldMat = this.mat(0xe6b84c, 0.3, 0.7);

    let curY = 0;
    for (let t = 0; t < 7; t++) {
      const r = 3.2 - t * 0.32;
      const h = 1.65 - t * 0.08;
      const tierBody = new THREE.Mesh(new THREE.CylinderGeometry(r * 0.88, r, h, 8), wallMat);
      tierBody.position.y = curY + h / 2;
      stupa.add(tierBody);

      const eaves = new THREE.Mesh(new THREE.ConeGeometry(r * 1.28, 0.65, 8), roofMat);
      eaves.position.y = curY + h + 0.25;
      stupa.add(eaves);
      curY += h + 0.38;
    }
    const spire = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.28, 2.2, 12), goldMat);
    spire.position.y = curY + 1.1;
    stupa.add(spire);

    this.grounds.add(stupa);
    this.colCircles.push([x, z, 3.6]);
  }

  buildCourtyardFloraAndBenches() {
    const potMat = this.mat(0xa84b2b, 0.65);
    const trunkMat = this.mat(0x6e4f35, 0.85);
    const leafGreen = this.mat(0x3a7d34, 0.72);
    const bougainvilleaPink = this.mat(0xf05492, 0.55);

    // Potted Bougainvillea & Cloud Bonsai flanking the main courtyard (Matches Ref Image 1)
    const potCoords = [
      [15.5, 24, true],
      [15.5, 14, false],
      [17.2, 6.5, false],
      [30.5, 24, true],
      [30.5, 14, false],
      [28.8, 6.5, false]
    ];
    potCoords.forEach(([px, pz, hasFlowers]) => {
      const potGroup = new THREE.Group();
      potGroup.position.set(px, 0, pz);
      const pot = new THREE.Mesh(new THREE.CylinderGeometry(0.68, 0.48, 0.65, 16), potMat);
      pot.position.y = 0.325;
      const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.22, 1.45, 10), trunkMat);
      trunk.position.y = 1.1;
      potGroup.add(pot, trunk);

      [
        [0, 1.95, 0, 0.78],
        [-0.45, 1.65, 0.25, 0.58],
        [0.45, 1.72, -0.2, 0.62]
      ].forEach(([cx, cy, cz, r]) => {
        const canopy = new THREE.Mesh(
          new THREE.SphereGeometry(r, 12, 10),
          hasFlowers ? bougainvilleaPink : leafGreen
        );
        canopy.scale.set(1.2, 0.65, 1.1);
        canopy.position.set(cx, cy, cz);
        potGroup.add(canopy);
      });
      this.grounds.add(potGroup);
      this.colCircles.push([px, pz, 0.85]);
    });

    // Stone benches on courtyard sides
    [
      [16.2, 19.2, Math.PI / 2],
      [29.8, 19.2, -Math.PI / 2]
    ].forEach(([bx, bz, rotY]) => {
      const bench = new THREE.Mesh(new THREE.BoxGeometry(1.8, 0.48, 0.58), this.mat(0xd5cfc4, 0.8));
      bench.position.set(bx, 0.24, bz);
      bench.rotation.y = rotY;
      this.grounds.add(bench);
    });
  }

  /* ========================================================================
     2. BUILD INTERIOR CHÁNH ĐIỆN & 18 VỊ LA HÁN (At (300, 0, 300))
     ======================================================================== */
  buildInteriorHall() {
    const floor = new THREE.Mesh(
      new THREE.PlaneGeometry(28, 36),
      this.mat(0x8c3b20, 0.55)
    );
    floor.rotation.x = -Math.PI / 2;
    this.interiorGroup.add(floor);

    // Red ceremonial carpet leading to Tam Bảo Altar
    const carpet = new THREE.Mesh(
      new THREE.PlaneGeometry(5.6, 26),
      this.mat(0x9b1b1b, 0.72)
    );
    carpet.rotation.x = -Math.PI / 2;
    carpet.position.set(0, 0.02, 1);
    this.interiorGroup.add(carpet);

    const wallMat = this.mat(0x522114, 0.75);
    const goldMat = this.mat(0xeab646, 0.25, 0.78);
    const woodRed = this.mat(0x6e1d14, 0.48);
    const pillarRed = this.mat(0x881c14, 0.42);
    const lanternMat = this.mat(0xffd269, 0.3, 0.1, { emissive: 0xffaa2b, emissiveIntensity: 0.75 });

    // Enclosing Walls & Dark Timber Ceiling
    const backWall = new THREE.Mesh(new THREE.BoxGeometry(28, 9.5, 0.6), wallMat);
    backWall.position.set(0, 4.75, -15);
    const leftWall = new THREE.Mesh(new THREE.BoxGeometry(0.6, 9.5, 36), wallMat);
    leftWall.position.set(-13.8, 4.75, 0);
    const rightWall = new THREE.Mesh(new THREE.BoxGeometry(0.6, 9.5, 36), wallMat);
    rightWall.position.set(13.8, 4.75, 0);
    const ceiling = new THREE.Mesh(new THREE.BoxGeometry(28.4, 0.5, 36), this.mat(0x3b180e, 0.8));
    ceiling.position.set(0, 9.5, 0);
    this.interiorGroup.add(backWall, leftWall, rightWall, ceiling);

    // Warm Interior PointLight
    const warmLight = new THREE.PointLight(0xffd896, 2.2, 38);
    warmLight.position.set(0, 7.2, -3);
    this.interiorGroup.add(warmLight);

    // 10 Towering Red-and-Gold Columns & Hanging Lanterns along the Nave
    [-9, -4, 1, 6, 11].forEach((pz) => {
      [-4.8, 4.8].forEach((px) => {
        const col = new THREE.Mesh(new THREE.CylinderGeometry(0.36, 0.4, 9.2, 16), pillarRed);
        col.position.set(px, 4.6, pz);
        const baseRing = new THREE.Mesh(new THREE.CylinderGeometry(0.5, 0.56, 0.35, 16), goldMat);
        baseRing.position.set(px, 0.18, pz);
        const lantern = new THREE.Mesh(new THREE.SphereGeometry(0.32, 12, 10), lanternMat);
        lantern.position.set(px * 0.72, 6.8, pz);
        this.interiorGroup.add(col, baseRing, lantern);
      });
    });

    // Overhead Plaque "ĐẠI HÙNG BẢO ĐIỆN"
    const baoDienPlaque = new THREE.Mesh(
      new THREE.PlaneGeometry(5.6, 1.25),
      new THREE.MeshBasicMaterial({
        map: this.createPlaqueTexture('ĐẠI HÙNG BẢO ĐIỆN', 'Tam Bảo Trang Nghiêm · Thập Bát La Hán')
      })
    );
    baoDienPlaque.position.set(0, 6.9, -8.5);
    this.interiorGroup.add(baoDienPlaque);

    // Tam Bảo Altar & Three Golden Buddhas (Di Đà - Thích Ca - Di Lặc)
    const altar = new THREE.Mesh(new THREE.BoxGeometry(10.5, 1.85, 3.8), woodRed);
    altar.position.set(0, 0.925, -11);
    const altarTrim = new THREE.Mesh(new THREE.BoxGeometry(10.7, 0.22, 4.0), goldMat);
    altarTrim.position.set(0, 1.86, -11);
    this.interiorGroup.add(altar, altarTrim);

    [-2.8, 0, 2.8].forEach((bx, idx) => {
      const s = idx === 1 ? 1.0 : 0.78;
      const lotusPed = new THREE.Mesh(new THREE.CylinderGeometry(0.85 * s, 1.05 * s, 0.45, 18), goldMat);
      lotusPed.position.set(bx, 2.1, -11);
      const mainBuddha = new THREE.Mesh(new THREE.ConeGeometry(1.05 * s, 2.6 * s, 18), goldMat);
      mainBuddha.position.set(bx, 3.4 * s + 0.6, -11);
      const head = new THREE.Mesh(new THREE.SphereGeometry(0.52 * s, 16, 16), goldMat);
      head.position.set(bx, 4.95 * s + 0.5, -11);
      const halo = new THREE.Mesh(
        new THREE.RingGeometry(0.75 * s, 1.08 * s, 28),
        new THREE.MeshBasicMaterial({ color: 0xffe484, side: THREE.DoubleSide })
      );
      halo.position.set(bx, 4.85 * s + 0.5, -11.45);
      this.interiorGroup.add(lotusPed, mainBuddha, head, halo);
    });

    // Kneeling Cushions in Front of Tam Bảo Altar
    [-1.6, 0, 1.6].forEach((cx) => {
      const cush = new THREE.Mesh(new THREE.CylinderGeometry(0.45, 0.48, 0.16, 18), this.mat(0x8c2d19, 0.7));
      cush.position.set(cx, 0.08, -6.8);
      this.interiorGroup.add(cush);
    });

    // 18 Golden Arhat Statues (`Thập Bát La Hán`) along Left & Right Walls
    for (let i = 0; i < 9; i++) {
      const az = -9.5 + i * 2.35;
      [-11.2, 11.2].forEach((ax) => {
        const ped = new THREE.Mesh(new THREE.BoxGeometry(1.1, 1.05, 1.1), woodRed);
        ped.position.set(ax, 0.525, az);
        const arhat = new THREE.Mesh(new THREE.CylinderGeometry(0.3, 0.38, 1.15, 14), goldMat);
        arhat.position.set(ax, 1.6, az);
        const aHead = new THREE.Mesh(new THREE.SphereGeometry(0.22, 12, 12), goldMat);
        aHead.position.set(ax, 2.35, az);
        this.interiorGroup.add(ped, arhat, aHead);
      });
    }
  }

  /* ========================================================================
     3. RIGGED 3D CHARACTERS (Nữ, Nam, Trẻ em) + COMPANION AN + NPCs
     ======================================================================== */
  makeAvatar(kind = 'nu', options = {}) {
    const group = new THREE.Group();
    // Procedural fallback figure while GLB loads
    const fallback = new THREE.Group();
    const h = kind === 'nam' ? 1.74 : kind === 'tre_em' ? 1.15 : 1.62;
    const robeColor = kind === 'nam' ? 0x6d5849 : kind === 'tre_em' ? 0x8fa89b : 0x9a8f99;
    const body = new THREE.Mesh(
      new THREE.CylinderGeometry(0.16 * (h / 1.62), 0.22 * (h / 1.62), h * 0.68, 14),
      this.mat(robeColor, 0.82)
    );
    body.position.y = h * 0.36;
    const head = new THREE.Mesh(
      new THREE.SphereGeometry(0.12 * (h / 1.62), 14, 12),
      this.mat(0xe8be9e, 0.65)
    );
    head.position.y = h * 0.82;
    const hair = new THREE.Mesh(
      new THREE.SphereGeometry(0.125 * (h / 1.62), 12, 10),
      this.mat(0x1f1a17, 0.85)
    );
    hair.position.set(0, h * 0.85, -0.02);
    fallback.add(body, head, hair);
    group.add(fallback);

    // Optional Non La hat mesh
    const hatMesh = new THREE.Mesh(
      new THREE.ConeGeometry(0.24 * (h / 1.62), 0.16 * (h / 1.62), 20, 1, true),
      this.mat(0xe8d8a0, 0.82, 0.05, { side: THREE.DoubleSide })
    );
    hatMesh.position.y = h * 0.96;
    hatMesh.visible = Boolean(options.hat);
    group.add(hatMesh);

    const av = {
      group,
      fallback,
      hatMesh,
      kind,
      model: null,
      mixer: null,
      actions: {},
      pose: null,
      wantPose: options.initPose || 'Dung',
      setPose(name) {
        this.wantPose = name;
        if (!this.mixer || this.pose === name) return;
        const next = this.actions[name] || this.actions['Dung'];
        if (!next) return;
        const prev = this.pose ? this.actions[this.pose] : null;
        next.reset();
        next.enabled = true;
        next.play();
        if (prev && prev !== next) {
          next.fadeIn(0.2);
          prev.fadeOut(0.2);
        }
        this.pose = name;
      }
    };

    this.charRegistry.push(av);
    if (this.charTemplates[kind]) {
      this.HydrateAvatarWithGLB(av);
    }
    return av;
  }

  HydrateAvatarWithGLB(av) {
    const tpl = this.charTemplates[av.kind];
    if (!tpl || av.model) return;
    try {
      const cloned = skeletonClone(tpl.root);
      cloned.scale.setScalar(tpl.scale);
      cloned.position.y = tpl.footOffset;
      cloned.traverse((o) => {
        if (o.isMesh) {
          o.castShadow = !this.isSoftwareGl;
          o.frustumCulled = false;
        }
      });
      av.fallback.visible = false;
      av.group.add(cloned);
      av.model = cloned;
      av.mixer = new THREE.AnimationMixer(cloned);
      Object.keys(tpl.clips).forEach((k) => {
        av.actions[k] = av.mixer.clipAction(tpl.clips[k]);
      });
      av.pose = null;
      av.setPose(av.wantPose);
      av.mixer.update(0.05);
      av.group.updateMatrixWorld(true);
      cloned.traverse((o) => {
        if (o.isSkinnedMesh && o.skeleton) o.skeleton.update();
      });
      const b = new THREE.Box3().setFromObject(cloned);
      if (Number.isFinite(b.min.y)) {
        cloned.position.y += av.group.position.y - b.min.y;
      }
    } catch {}
  }

  setupAvatarsAndNPCs() {
    this.playerAv = this.makeAvatar(this.player.profileKey, { hat: this.player.hatEquipped });
    this.playerAv.group.position.copy(this.player.pos);
    this.playerAv.group.rotation.y = this.player.yaw;
    this.scene.add(this.playerAv.group);

    // Chú tiểu An (Companion child guide)
    this.companionAv = this.makeAvatar('tre_em', { hat: false });
    this.companionAv.group.position.copy(this.companionPos);
    this.scene.add(this.companionAv.group);

    // 4 Peaceful Temple NPCs strolling & bowing at the Lotus Pond, Burner, A Di Đà & Di Lặc
    const npcConfigs = [
      { kind: 'nam', route: [[20, 26], [15, 16], [20, 13], [26, 18]], hat: false },
      { kind: 'nu', route: [[27, 25], [31, 16], [26, 12], [27, 25]], hat: true },
      { kind: 'nam', route: [[-10, 22], [-14, 21.5], [-18, 12], [-22, 6]], hat: false },
      { kind: 'tre_em', route: [[34, 32], [37, 33], [30, 26], [34, 32]], hat: true }
    ];
    npcConfigs.forEach((cfg, idx) => {
      const av = this.makeAvatar(cfg.kind, { hat: cfg.hat });
      av.group.position.set(cfg.route[0][0], 0, cfg.route[0][1]);
      this.grounds.add(av.group);
      this.npcs.push({
        av,
        route: cfg.route,
        wp: 1,
        speed: 1.15 + (idx % 2) * 0.2,
        pause: 0
      });
    });
  }

  loadAllGLBAssets() {
    const loader = new GLTFLoader();

    // 1. Load 3 Rigged Animated Characters (Nữ, Nam, Trẻ em)
    CHARACTER_PROFILES.forEach((prof) => {
      loader.load(
        prof.glb,
        (gltf) => {
          const root = gltf.scene;
          root.traverse((o) => {
            if (o.isMesh) {
              if (o.material) {
                o.material.vertexColors = true;
                o.material.metalness = 0;
                o.material.roughness = 0.9;
              }
              if (!o.geometry.getAttribute('normal')) {
                o.geometry.computeVertexNormals();
              }
            }
          });
          const clips = {};
          (gltf.animations || []).forEach((c) => {
            clips[c.name.replace(/_world$/, '')] = c;
          });
          let animH = 0;
          let animMinY = 0;
          try {
            const probe = skeletonClone(root);
            const pg = new THREE.Group();
            pg.add(probe);
            const pm = new THREE.AnimationMixer(probe);
            const dung = clips['Dung'];
            if (dung) {
              pm.clipAction(dung).play();
              pm.update(0.3);
            }
            pg.updateMatrixWorld(true);
            probe.traverse((o) => {
              if (o.isSkinnedMesh && o.skeleton) o.skeleton.update();
            });
            const pb = new THREE.Box3().setFromObject(pg);
            animH = Math.max(0.01, pb.max.y - pb.min.y);
            animMinY = pb.min.y;
          } catch {}
          if (!(animH > 0.05)) {
            const box = new THREE.Box3().setFromObject(root);
            animH = Math.max(0.1, box.max.y - box.min.y);
            animMinY = box.min.y;
          }
          const scale = (prof.heightMeters || 1.62) / animH;
          this.charTemplates[prof.key] = {
            root,
            clips,
            scale,
            footOffset: -animMinY * scale
          };
          this.charRegistry
            .filter((av) => av.kind === prof.key)
            .forEach((av) => this.HydrateAvatarWithGLB(av));
        },
        undefined,
        () => {}
      );
    });

    // 2. Load Sculpted Buddha Statue GLBs into the 3D Monuments
    const statueJobs = [
      {
        url: '/Mô hình 3D Vĩnh Tràng/Tượng/phat-dung-adida.glb',
        mount: () => this.adidaMount,
        fallback: () => this.adidaFallback,
        targetHeight: 12.2,
        baseY: 0,
        color: 0xfbfaf7
      },
      {
        url: '/Mô hình 3D Vĩnh Tràng/Tượng/di-lac.glb',
        mount: () => this.dilacMount,
        fallback: () => this.dilacFallback,
        targetHeight: 8.2,
        baseY: 0,
        color: 0xfbfaf7
      },
      {
        url: '/Mô hình 3D Vĩnh Tràng/Tượng/phat-nam.glb',
        mount: () => this.nirvanaMount,
        fallback: () => this.nirvanaFallback,
        targetHeight: 5.4,
        baseY: 0,
        color: 0xfbfaf7
      }
    ];

    statueJobs.forEach((job) => {
      loader.load(
        job.url,
        (gltf) => {
          const root = gltf.scene;
          const fallbackMat = this.mat(job.color, 0.35, 0.06);
          const toRemove = [];
          root.traverse((o) => {
            if (/ground/i.test(o.name || '')) {
              toRemove.push(o);
              return;
            }
            if (o.isMesh) {
              if (!o.geometry.getAttribute('normal')) o.geometry.computeVertexNormals();
              if (o.material) {
                o.material.roughness = 0.42;
                o.material.metalness = 0.05;
              } else {
                o.material = fallbackMat;
              }
            }
          });
          toRemove.forEach((o) => o.parent?.remove(o));
          const b = new THREE.Box3().setFromObject(root);
          const h = Math.max(0.1, b.max.y - b.min.y);
          const s = job.targetHeight / h;
          root.scale.setScalar(s);
          const b2 = new THREE.Box3().setFromObject(root);
          root.position.set(
            -(b2.min.x + b2.max.x) / 2,
            job.baseY - b2.min.y,
            -(b2.min.z + b2.max.z) / 2
          );
          const m = job.mount();
          const fb = job.fallback();
          if (m) {
            if (fb) fb.visible = false;
            m.add(root);
          }
        },
        undefined,
        () => {}
      );
    });
  }

  /* ========================================================================
     4. MOVEMENT, COLLISION, AUTO-WALK TRAIL & CAMERA CONTROLS
     ======================================================================== */
  isBlocked(x, z) {
    if (this.insideInterior) {
      return x < 288 || x > 312 || z < 289 || z > 316;
    }
    if (x < -36 || x > 51 || z < -41 || z > 50) return true;
    for (const r of this.colRects) {
      if (x > r[0] - 0.55 && x < r[2] + 0.55 && z > r[1] - 0.55 && z < r[3] + 0.55) {
        return true;
      }
    }
    for (const c of this.colCircles) {
      if (Math.hypot(x - c[0], z - c[1]) < c[2] + 0.55) return true;
    }
    return false;
  }

  tryMove(nx, nz) {
    const px = this.player.pos.x;
    const pz = this.player.pos.z;
    if (!this.isBlocked(nx, pz)) this.player.pos.x = nx;
    if (!this.isBlocked(this.player.pos.x, nz)) this.player.pos.z = nz;
  }

  walkToStation(stationKeyOrId) {
    const st =
      PILGRIMAGE_STATIONS.find(
        (s) => s.id === stationKeyOrId || s.key === stationKeyOrId
      ) || PILGRIMAGE_STATIONS[5];

    if (this.insideInterior) {
      this.exitInteriorHall();
    }

    const destX = st.standPos ? st.standPos.x : st.pos.x;
    const destZ = st.standPos ? st.standPos.z : st.pos.z;
    const path = [];
    if (Array.isArray(st.via)) {
      st.via.forEach(([vx, vz]) => {
        if (Math.hypot(vx - this.player.pos.x, vz - this.player.pos.z) > 2.5) {
          path.push({ x: vx, z: vz });
        }
      });
    }
    path.push({ x: destX, z: destZ });

    this.autoWalk = {
      station: st,
      path
    };
    this.player.target = null;
    this.showGoldenTrail([[this.player.pos.x, this.player.pos.z], ...path.map((p) => [p.x, p.z])]);
    return st;
  }

  teleportToStation(stationKeyOrId) {
    const st =
      PILGRIMAGE_STATIONS.find(
        (s) => s.id === stationKeyOrId || s.key === stationKeyOrId
      ) || PILGRIMAGE_STATIONS[5];
    if (this.insideInterior) this.exitInteriorHall();
    const destX = st.standPos ? st.standPos.x : st.pos.x;
    const destZ = st.standPos ? st.standPos.z : st.pos.z;
    this.player.pos.set(destX, 0, destZ);
    const lookX = st.lookAt ? st.lookAt.x : st.pos.x;
    const lookZ = st.lookAt ? st.lookAt.z : st.pos.z;
    const dx = lookX - destX;
    const dz = lookZ - destZ;
    this.player.yaw = Math.atan2(dx, dz);
    this.player.camYaw = Math.atan2(-dx, -dz);
    this.companionPos.set(destX - 1.3, 0, destZ + 1.1);
    if (this.playerAv) {
      this.playerAv.group.position.copy(this.player.pos);
      this.playerAv.group.rotation.y = this.player.yaw;
    }
    this.hideGoldenTrail();
    this.autoWalk = null;
    this.snapCamera();
    if (this.callbacks.onStationReached) {
      this.callbacks.onStationReached(st);
    }
    if (this.callbacks.onStationArrive) {
      this.callbacks.onStationArrive(st);
    }
    return st;
  }

  enterInteriorHall() {
    this.insideInterior = true;
    this.grounds.visible = false;
    this.interiorGroup.visible = true;
    this.player.pos.set(300, 0, 304.5);
    this.player.yaw = Math.PI;
    this.player.camYaw = 0;
    this.companionPos.set(298.6, 0, 305.8);
    if (this.playerAv) {
      this.playerAv.group.position.copy(this.player.pos);
      this.playerAv.group.rotation.y = this.player.yaw;
    }
    this.hideGoldenTrail();
    this.snapCamera();
  }

  exitInteriorHall() {
    this.insideInterior = false;
    this.interiorGroup.visible = false;
    this.grounds.visible = true;
    this.player.pos.set(23, 0, 14.5);
    this.player.yaw = Math.PI;
    this.player.camYaw = 0;
    this.companionPos.set(21.5, 0, 15.8);
    if (this.playerAv) {
      this.playerAv.group.position.copy(this.player.pos);
      this.playerAv.group.rotation.y = this.player.yaw;
    }
    this.snapCamera();
  }

  showGoldenTrail(pts) {
    this.hideGoldenTrail();
    const vecs = pts.map(([x, z]) => new THREE.Vector3(x, 0.16, z));
    this.trailLine = new THREE.Line(
      new THREE.BufferGeometry().setFromPoints(vecs),
      new THREE.LineBasicMaterial({ color: 0xf4c44e, linewidth: 2 })
    );
    this.scene.add(this.trailLine);

    const last = pts[pts.length - 1];
    this.destRing = new THREE.Mesh(
      new THREE.RingGeometry(0.65, 0.95, 32),
      new THREE.MeshBasicMaterial({ color: 0xf4c44e, side: THREE.DoubleSide })
    );
    this.destRing.rotation.x = -Math.PI / 2;
    this.destRing.position.set(last[0], 0.08, last[1]);
    this.scene.add(this.destRing);
  }

  hideGoldenTrail() {
    if (this.trailLine) {
      this.scene.remove(this.trailLine);
      this.trailLine.geometry.dispose();
      this.trailLine = null;
    }
    if (this.destRing) {
      this.scene.remove(this.destRing);
      this.destRing.geometry.dispose();
      this.destRing = null;
    }
  }

  setCharacterProfile(profileKey, hatEquipped = false) {
    this.player.profileKey = profileKey;
    this.player.hatEquipped = Boolean(hatEquipped);
    if (this.playerAv) {
      this.scene.remove(this.playerAv.group);
      const idx = this.charRegistry.indexOf(this.playerAv);
      if (idx >= 0) this.charRegistry.splice(idx, 1);
    }
    this.playerAv = this.makeAvatar(profileKey, { hat: this.player.hatEquipped });
    this.playerAv.group.position.copy(this.player.pos);
    this.playerAv.group.rotation.y = this.player.yaw;
    this.scene.add(this.playerAv.group);
  }

  switchCharacter(profileKey, hatEquipped = this.player.hatEquipped) {
    this.setCharacterProfile(profileKey, hatEquipped);
  }

  triggerBowAnimation(durationSec = 2.6) {
    this.player.bowTimer = durationSec;
    if (this.playerAv) {
      this.playerAv.setPose('Vái');
    }
  }

  playPlayerBowAnimation(durationSec = 2.6) {
    this.triggerBowAnimation(durationSec);
  }

  setIncenseBoost() {
    this.player.incenseLit = true;
    for (const sp of this.smokeParticles) {
      if (sp.mesh && sp.mesh.material) {
        sp.mesh.material.opacity = 0.45;
      }
    }
  }

  placeLotusOfferingIn3D() {
    if (!this.grounds) return;
    const lotus = new THREE.Group();
    const ox = this.player.pos.x - Math.sin(this.player.yaw) * 1.1;
    const oz = this.player.pos.z - Math.cos(this.player.yaw) * 1.1;
    lotus.position.set(ox, 0.22, oz);
    const petalMat = this.mat(0xf78fb3, 0.45);
    for (let p = 0; p < 6; p++) {
      const a = (p / 6) * Math.PI * 2;
      const cone = new THREE.Mesh(new THREE.ConeGeometry(0.08, 0.2, 6), petalMat);
      cone.position.set(Math.cos(a) * 0.08, 0.06, Math.sin(a) * 0.08);
      lotus.add(cone);
    }
    this.grounds.add(lotus);
  }

  setDpadInput(dx, dz) {
    this.dpadDir = { dx, dz };
    if (dx !== 0 || dz !== 0) {
      this.autoWalk = null;
      this.hideGoldenTrail();
    }
  }

  nudgeDirection(dir, stepMeters = 2.1) {
    this.nudgeMove(dir, stepMeters);
  }

  nudgeMove(dir, stepMeters = 2.1) {
    this.autoWalk = null;
    this.hideGoldenTrail();
    const fwdX = -Math.sin(this.player.camYaw);
    const fwdZ = -Math.cos(this.player.camYaw);
    const rightX = -fwdZ;
    const rightZ = fwdX;
    let mx = 0;
    let mz = 0;
    if (dir === 'up') {
      mx = fwdX;
      mz = fwdZ;
    } else if (dir === 'down') {
      mx = -fwdX;
      mz = -fwdZ;
    } else if (dir === 'left') {
      mx = -rightX;
      mz = -rightZ;
    } else if (dir === 'right') {
      mx = rightX;
      mz = rightZ;
    }
    const len = Math.hypot(mx, mz) || 1;
    mx /= len;
    mz /= len;
    this.tryMove(this.player.pos.x + mx * stepMeters, this.player.pos.z + mz * stepMeters);
    this.player.yaw = Math.atan2(mx, mz);
    this.playerAv.group.position.copy(this.player.pos);
    this.playerAv.group.rotation.y = this.player.yaw;
    this.checkStationProximity();
  }

  bindInputs() {
    window.addEventListener('keydown', (e) => {
      if (['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement?.tagName || '')) return;
      this.keys[e.code] = true;
    });
    window.addEventListener('keyup', (e) => {
      this.keys[e.code] = false;
    });
    window.addEventListener('blur', () => {
      this.keys = {};
      this.dpadDir = { dx: 0, dz: 0 };
      this.dragging = false;
    });

    this.canvas.addEventListener('pointerdown', (e) => {
      this.dragging = true;
      this.pointerDownPos = { x: e.clientX, y: e.clientY, t: performance.now() };
      this.lastPointer = { x: e.clientX, y: e.clientY };
    });

    window.addEventListener('pointermove', (e) => {
      if (!this.dragging) return;
      const dx = e.clientX - this.lastPointer.x;
      const dy = e.clientY - this.lastPointer.y;
      this.player.camYaw -= dx * 0.0055;
      this.player.camPitch = THREE.MathUtils.clamp(this.player.camPitch + dy * 0.0035, 0.08, 0.68);
      this.lastPointer = { x: e.clientX, y: e.clientY };
    });

    window.addEventListener('pointerup', (e) => {
      if (!this.dragging) return;
      this.dragging = false;
      const dist = Math.hypot(e.clientX - this.pointerDownPos.x, e.clientY - this.pointerDownPos.y);
      const elapsed = performance.now() - this.pointerDownPos.t;
      if (dist < 7 && elapsed < 320 && e.target === this.canvas) {
        const rect = this.canvas.getBoundingClientRect();
        const nx = ((e.clientX - rect.left) / rect.width) * 2 - 1;
        const ny = -((e.clientY - rect.top) / rect.height) * 2 + 1;
        this._raycaster.setFromCamera({ x: nx, y: ny }, this.camera);
        if (this._raycaster.ray.intersectPlane(this._groundPlane, this._clickPt)) {
          this.autoWalk = null;
          this.player.target = { x: this._clickPt.x, z: this._clickPt.z };
          this.showGoldenTrail([
            [this.player.pos.x, this.player.pos.z],
            [this._clickPt.x, this._clickPt.z]
          ]);
        }
      }
    });

    this.canvas.addEventListener(
      'wheel',
      (e) => {
        this.player.camDist = THREE.MathUtils.clamp(this.player.camDist + e.deltaY * 0.004, 3.8, 13.5);
      },
      { passive: true }
    );

    window.addEventListener('resize', () => {
      if (!this.renderer || !this.camera) return;
      this.camera.aspect = window.innerWidth / window.innerHeight;
      this.camera.updateProjectionMatrix();
      this.renderer.setSize(window.innerWidth, window.innerHeight);
    });
  }

  checkStationProximity() {
    if (this.insideInterior) return;
    let best = null;
    let bestD = Infinity;
    for (const st of PILGRIMAGE_STATIONS) {
      const tx = st.standPos ? st.standPos.x : st.pos.x;
      const tz = st.standPos ? st.standPos.z : st.pos.z;
      const d = Math.hypot(this.player.pos.x - tx, this.player.pos.z - tz);
      if (d < bestD) {
        bestD = d;
        best = st;
      }
    }
    if (best && best.id !== this.nearestStationId && bestD < 5.2) {
      this.nearestStationId = best.id;
      if (this.callbacks.onStationProximity) {
        this.callbacks.onStationProximity(best, bestD);
      }
    }
  }

  /* ========================================================================
     5. SIMULATION TICK & SOFTWARE-WEBGL PACED RENDER LOOP
     ======================================================================== */
  tick(dt) {
    this.simTime += dt;
    const t = this.simTime;

    // 1. Update skeletal animation mixers
    for (const av of this.charRegistry) {
      if (av.mixer) av.mixer.update(dt);
    }

    // 2. Player movement (WASD / Arrows / D-Pad / AutoWalk / Click-to-Walk)
    const fwdX = -Math.sin(this.player.camYaw);
    const fwdZ = -Math.cos(this.player.camYaw);
    const rightX = -fwdZ;
    const rightZ = fwdX;

    let mx = 0;
    let mz = 0;
    let manual = false;

    if (this.keys['KeyW'] || this.keys['ArrowUp']) {
      mx += fwdX;
      mz += fwdZ;
      manual = true;
    }
    if (this.keys['KeyS'] || this.keys['ArrowDown']) {
      mx -= fwdX;
      mz -= fwdZ;
      manual = true;
    }
    if (this.keys['KeyA'] || this.keys['ArrowLeft']) {
      mx -= rightX;
      mz -= rightZ;
      manual = true;
    }
    if (this.keys['KeyD'] || this.keys['ArrowRight']) {
      mx += rightX;
      mz += rightZ;
      manual = true;
    }
    if (this.dpadDir.dx || this.dpadDir.dz) {
      mx += fwdX * -this.dpadDir.dz + rightX * this.dpadDir.dx;
      mz += fwdZ * -this.dpadDir.dz + rightZ * this.dpadDir.dx;
      manual = true;
    }

    if (manual) {
      this.autoWalk = null;
      this.player.target = null;
      this.hideGoldenTrail();
    }

    if (this.autoWalk && !manual) {
      const wp = this.autoWalk.path[0];
      if (!wp) {
        const reached = this.autoWalk.station;
        this.autoWalk = null;
        this.hideGoldenTrail();
        if (reached && this.callbacks.onStationReached) {
          this.callbacks.onStationReached(reached);
        }
        if (reached && this.callbacks.onStationArrive) {
          this.callbacks.onStationArrive(reached);
        }
      } else {
        const dx = wp.x - this.player.pos.x;
        const dz = wp.z - this.player.pos.z;
        const d = Math.hypot(dx, dz);
        if (d < 0.65) {
          this.autoWalk.path.shift();
        } else {
          mx = dx / d;
          mz = dz / d;
        }
      }
    } else if (this.player.target && !manual) {
      const dx = this.player.target.x - this.player.pos.x;
      const dz = this.player.target.z - this.player.pos.z;
      const d = Math.hypot(dx, dz);
      if (d < 0.5) {
        this.player.target = null;
        this.hideGoldenTrail();
      } else {
        mx = dx / d;
        mz = dz / d;
      }
    }

    const moveLen = Math.hypot(mx, mz);
    if (moveLen > 0.01) {
      mx /= moveLen;
      mz /= moveLen;
      const step = this.player.speed * dt;
      this.tryMove(this.player.pos.x + mx * step, this.player.pos.z + mz * step);
      const wantYaw = Math.atan2(mx, mz);
      let dyaw = wantYaw - this.player.yaw;
      while (dyaw > Math.PI) dyaw -= Math.PI * 2;
      while (dyaw < -Math.PI) dyaw += Math.PI * 2;
      this.player.yaw += dyaw * Math.min(1, dt * 10);
      this.player.moving = true;
      this.checkStationProximity();
    } else {
      this.player.moving = false;
    }

    if (this.playerAv) {
      this.playerAv.group.position.copy(this.player.pos);
      this.playerAv.group.rotation.y = this.player.yaw;
      if (this.player.bowTimer > 0) {
        this.player.bowTimer -= dt;
        this.playerAv.setPose('Vái');
      } else if (this.player.moving) {
        this.playerAv.setPose('Di bo');
      } else {
        this.playerAv.setPose('Dung');
      }
    }

    // 3. Companion Chú tiểu An follows smoothly beside player
    if (this.companionAv) {
      const sideX = Math.cos(this.player.yaw);
      const sideZ = -Math.sin(this.player.yaw);
      const tx = this.player.pos.x - Math.sin(this.player.yaw) * 1.15 + sideX * 1.1;
      const tz = this.player.pos.z - Math.cos(this.player.yaw) * 1.15 + sideZ * 1.1;
      const cdx = tx - this.companionPos.x;
      const cdz = tz - this.companionPos.z;
      const cd = Math.hypot(cdx, cdz);
      if (cd > 0.18) {
        const sp = Math.min(cd, 3.6 * dt);
        this.companionPos.x += (cdx / cd) * sp;
        this.companionPos.z += (cdz / cd) * sp;
        this.companionYaw = Math.atan2(cdx, cdz);
        this.companionAv.setPose('Di bo');
      } else {
        this.companionAv.setPose('Dung');
      }
      this.companionAv.group.position.copy(this.companionPos);
      this.companionAv.group.rotation.y = this.companionYaw;
    }

    // 4. Animate Koi fish, lotus flowers, incense smoke, falling leaves & NPCs
    for (const f of this.fishes) {
      f.ang += f.sp * dt;
      f.mesh.position.x = Math.cos(f.ang) * f.r;
      f.mesh.position.z = Math.sin(f.ang) * f.r * 0.78;
      f.mesh.rotation.y = Math.atan2(-Math.cos(f.ang) * 0.78, -Math.sin(f.ang));
    }

    for (const lf of this.lotusFlowers) {
      lf.group.position.y = lf.baseY + Math.sin(t * 1.8 + lf.seed) * 0.015;
    }

    for (const sp of this.smokeParticles) {
      const cycle = ((t * 0.55 + sp.offset) % 2.4) / 2.4;
      sp.mesh.position.y = 1.75 + cycle * 2.4;
      sp.mesh.position.x = 23 + Math.sin(t * 1.5 + sp.offset) * 0.22 * cycle;
      sp.mesh.material.opacity = (1 - cycle) * 0.32;
      sp.mesh.scale.setScalar(0.7 + cycle * 1.4);
    }

    for (const leaf of this.leafParticles) {
      leaf.mesh.position.y -= leaf.speed * dt;
      leaf.mesh.position.x += Math.sin(t * 1.4 + leaf.seed) * 0.25 * dt;
      leaf.mesh.rotation.z += dt * 0.9;
      if (leaf.mesh.position.y < 0.08) {
        leaf.mesh.position.y = 4.5 + Math.random() * 2.0;
      }
    }

    for (const n of this.npcs) {
      if (n.pause > 0) {
        n.pause -= dt;
        n.av.setPose('Chắp tay');
        continue;
      }
      const wp = n.route[n.wp];
      const dx = wp[0] - n.av.group.position.x;
      const dz = wp[1] - n.av.group.position.z;
      const d = Math.hypot(dx, dz);
      if (d < 0.45) {
        n.wp = (n.wp + 1) % n.route.length;
        n.pause = 2.8;
      } else {
        n.av.group.position.x += (dx / d) * n.speed * dt;
        n.av.group.position.z += (dz / d) * n.speed * dt;
        n.av.group.rotation.y = Math.atan2(dx, dz);
        n.av.setPose('Di bo');
      }
    }

    // 5. Update Camera & Project 3D Floating Pins
    this.updateCamera(dt);
    this.project3DPinsToHUD();
  }

  computeCameraTargets() {
    const dist = this.insideInterior ? 4.8 : this.player.camDist;
    const height = this.insideInterior ? 2.4 : 1.65 + Math.sin(this.player.camPitch) * dist;
    const horizDist = Math.cos(this.player.camPitch) * dist;

    this._camTarget.set(
      this.player.pos.x + Math.sin(this.player.camYaw) * horizDist,
      Math.max(1.3, height),
      this.player.pos.z + Math.cos(this.player.camYaw) * horizDist
    );

    const lookAhead = this.insideInterior ? 3.8 : 3.2;
    this._lookTarget.set(
      this.player.pos.x - Math.sin(this.player.camYaw) * lookAhead,
      this.insideInterior ? 1.85 : 1.75,
      this.player.pos.z - Math.cos(this.player.camYaw) * lookAhead
    );
  }

  snapCamera() {
    if (!this.camera) return;
    this.computeCameraTargets();
    this.camera.position.copy(this._camTarget);
    this.camera.lookAt(this._lookTarget);
  }

  updateCamera(dt) {
    this.computeCameraTargets();
    const alpha = 1 - Math.exp(-8 * dt);
    this.camera.position.lerp(this._camTarget, alpha);
    this.camera.lookAt(this._lookTarget);
  }

  project3DPinsToHUD() {
    if (!this.callbacks.onUpdateProjectedPins || this.insideInterior) return;
    const w = window.innerWidth;
    const h = window.innerHeight;
    const projected = [];

    for (const st of PILGRIMAGE_STATIONS) {
      const py = st.key === 'chanh_dien' ? 5.2 : st.key === 'ho_sen_ca_koi' ? 1.5 : 3.8;
      this._projVec.set(st.pos.x, py, st.pos.z);
      this._projVec.project(this.camera);
      const visible =
        this._projVec.z >= -1 &&
        this._projVec.z <= 1 &&
        this._projVec.x >= -0.95 &&
        this._projVec.x <= 0.95 &&
        this._projVec.y >= -0.85 &&
        this._projVec.y <= 0.88;

      const sx = (this._projVec.x * 0.5 + 0.5) * w;
      const sy = (-this._projVec.y * 0.5 + 0.5) * h;
      const dist = Math.round(Math.hypot(this.player.pos.x - st.pos.x, this.player.pos.z - st.pos.z));
      projected.push({
        id: st.id,
        key: st.key,
        pinLabel: st.pinLabel,
        visible,
        x: sx,
        y: sy,
        dist
      });
    }
    this.callbacks.onUpdateProjectedPins(projected);
  }

  captureSnapshotDataURL() {
    if (!this.renderer || !this.scene || !this.camera) return null;
    this.renderer.render(this.scene, this.camera);
    try {
      return this.canvas.toDataURL('image/png');
    } catch {
      return null;
    }
  }

  stepSimulation(dt) {
    this.tick(dt);
  }

  renderFrame() {
    if (this.renderer && this.scene && this.camera) {
      this.renderer.render(this.scene, this.camera);
    }
  }

  startLoop() {
    const afterDraw = (cb) => {
      const gl = this.renderer.getContext();
      if (gl && gl.fenceSync) {
        const sync = gl.fenceSync(gl.SYNC_GPU_COMMANDS_COMPLETE, 0);
        gl.flush();
        const poll = () => {
          const state = sync && gl.getSyncParameter(sync, gl.SYNC_STATUS);
          if (state === gl.UNSIGNALED) {
            this.frameId = window.setTimeout(poll, 5);
          } else {
            gl.deleteSync(sync);
            this.frameId = window.setTimeout(cb, 80);
          }
        };
        this.frameId = window.setTimeout(poll, 5);
      } else {
        this.frameId = window.setTimeout(cb, 80);
      }
    };

    const loop = () => {
      const dt = Math.min(this.clock.getDelta(), 0.05);
      this.tick(dt);
      this.renderer.render(this.scene, this.camera);
      if (this.isSoftwareGl) {
        afterDraw(loop);
      } else {
        this.frameId = requestAnimationFrame(loop);
      }
    };
    loop();
  }
}
