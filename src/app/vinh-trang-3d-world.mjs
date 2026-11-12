/**
 * VinhTrang3DWorld V8 ("Sáng Trong" Master Edition) — Full-Featured Interactive 3D Temple Grounds
 * Built directly from the 5-Section Master Specification & Reference V8 Modules:
 * 1. SỬA MÀU SẮC & ÁNH SÁNG ("Sáng trong"):
 *    - Cobalt blue sky (0x2B7DE1, gradient #0155C9 -> #4F97F9), warm sunlight ~16:30 (0xffd9a3, intensity 1.7)
 *      + south front-fill (0xfff6e0, intensity 0.55), hemisphere (0xfff2d9 / 0x5e4a35, intensity 1.3),
 *      ACESFilmicToneMapping exposure 1.12.
 *    - Locked real-photo hex palette: Chánh điện gold #D9A441 (#B9852F shaded), cream #E8E2D4, red columns #7E2A22,
 *      dark wood openings #1E1410 / #2B2320, terracotta brown-red roof tiles #7C4030 (#6E382A-#8A4A34),
 *      warm white statues #EFE9DD, A Di Đà blue lotus throne #4E86A8 on #8A4A3A base, stone pedestals #6E675C,
 *      7-tier stupa #C88A4A / #A85A38, Tam Quan gates #C9962E + mosaic cobalt #2C4A8A / jade #3F7D5D / red #A03A2A,
 *      stone-paved courtyard #8A7A63 / #B4A68C, pond water #4E5F3A, foliage #3E6B34-#5C8446, bougainvillea #EE7FAE.
 *    - Self-generated procedural canvas textures (<=1024px): stone paving with mortar lines, terracotta roof tiles,
 *      leaf clusters, Buddhist 5-stripe flag, and high-DPI plaques ("CHÙA VĨNH TRÀNG").
 * 2. SỬA MẶT TIỀN & TƯỢNG:
 *    - 13-arch Chánh Điện at (23, 0, -1) with red columns, golden lattice grilles, upper cream frieze,
 *      cobalt mosaic band, 2-tier #7C4030 roof, 5-step staircase, two bell/drum towers, and bonsai pots.
 *    - Real sculpted GLB Buddha statues from /Mô hình 3D Vĩnh Tràng/Tượng/ (NEVER primitive spheres/cones):
 *      phat-dung-adida.glb, di-lac.glb, phat-nam.glb, phat-ngoi-ban-tho.glb (with 300x300 "Ground" removed).
 * 3. SỬA DI CHUYỂN & SANSA AUTO-WALK:
 *    - Crossfade (0.22s), speed-blend (moveBlend), smooth yaw lerp, hysteresis obstacle escape in tryMove,
 *      click-to-walk along waypoints with golden trail & objective callback ("Đang tới: <tên trạm>").
 *    - Monks in grey robes with orange diagonal sash (recolorMonkRobe), kneeling worshippers on red-gold cushions,
 *      and SmokeColumn rising from the bronze incense burner.
 * 4. LÀM ĐẦY ĐỦ KHUÔN VIÊN (~14,000 m²):
 *    - 2 Tam Quan gates, golden fence, 2 Lotus Ponds with stone balusters & Koi fish, 8 stone lanterns,
 *      coconut palms, Buddhist flag strings, distant mountains, blossom trees, Sạp nhang hoa, Phòng kinh sách,
 *      Giảng đường Huệ Đăng, Bảo tháp 7 tầng, Quầy lưu niệm, pigeons, and 4-section Interior Hall.
 */

import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import * as SkeletonUtils from 'three/addons/utils/SkeletonUtils.js';
import {
  PILGRIMAGE_STATIONS,
  WORLD_BOUNDS,
  shiftOklch,
  VINH_TRANG_OKLCH_PALETTE
} from '../logic/chua-online-logic.mjs';

const CHAR_GLB_PATHS = {
  nu: '/Thiết kế giao diện/Nhân vật 3D/Bản chỉnh sửa/nu-phuc-hoi-mau-chuyen-dong.glb',
  nam: '/Thiết kế giao diện/Nhân vật 3D/Chuyển động/nam-chuyen-dong.glb',
  tre_em: '/Thiết kế giao diện/Nhân vật 3D/Chuyển động/tre-em-chuyen-dong.glb'
};

const CHAR_HEIGHTS = {
  nu: 1.64,
  nam: 1.75,
  tre_em: 1.18
};

const STATUE_GLB_PATHS = {
  adida: '/Mô hình 3D Vĩnh Tràng/Tượng/phat-dung-adida.glb',
  dilac: '/Mô hình 3D Vĩnh Tràng/Tượng/di-lac.glb',
  phatnam: '/Mô hình 3D Vĩnh Tràng/Tượng/phat-nam.glb',
  bantho: '/Mô hình 3D Vĩnh Tràng/Tượng/phat-ngoi-ban-tho.glb'
};

const PROP_GLB_PATHS = {
  ban_tho: '/Thiết kế giao diện/Vật phẩm 3D/fixed/bat_nhang_tram.glb',
  non_la: '/Thiết kế giao diện/Vật phẩm 3D/models/non_la_theu_sen_v3.glb',
  tui_sen: '/Thiết kế giao diện/Vật phẩm 3D/models/tui_vai_theu_sen.glb',
  ao_trang: '/Thiết kế giao diện/Vật phẩm 3D/models/ao_trang_phat_tu.glb',
  bo_doan: '/Thiết kế giao diện/Vật phẩm 3D/fixed/bo_doan_dai_sen.glb',
  hoa_sen: '/Thiết kế giao diện/Vật phẩm 3D/fixed/nen_hoa_sen.glb',
  den_long: '/Thiết kế giao diện/Vật phẩm 3D/fixed/den_long_luc_giac.glb',
  chum_sen: '/Thiết kế giao diện/Vật phẩm 3D/fixed/chum_sanh_hoa_sen.glb',
  mam_ngu_qua: '/Thiết kế giao diện/Vật phẩm 3D/fixed/mam_ngu_qua.glb',
  mo_go: '/Thiết kế giao diện/Vật phẩm 3D/fixed/mo_go_tung_kinh.glb'
};

function makeCanvasTex(draw, w = 512, h = 512, repeatX = 1, repeatY = 1, isColor = true) {
  const c = document.createElement('canvas');
  c.width = w;
  c.height = h;
  draw(c.getContext('2d'), w, h);
  const t = new THREE.CanvasTexture(c);
  t.wrapS = t.wrapT = THREE.RepeatWrapping;
  t.repeat.set(repeatX, repeatY);
  if (isColor) t.colorSpace = THREE.SRGBColorSpace;
  return t;
}

function makeTextTex(text, opts = {}) {
  const w = opts.w || 1024;
  const h = opts.h || 256;
  const c = document.createElement('canvas');
  c.width = w;
  c.height = h;
  const g = c.getContext('2d');
  g.fillStyle = opts.bg || '#5C1B12';
  g.fillRect(0, 0, w, h);
  g.strokeStyle = opts.border || '#D9A441';
  g.lineWidth = Math.max(8, h * 0.05);
  g.strokeRect(10, 10, w - 20, h - 20);
  g.strokeRect(22, 22, w - 44, h - 44);
  g.fillStyle = opts.color || '#FFD875';
  g.font = `bold ${opts.size || Math.floor(h * 0.44)}px "Noto Serif", "Times New Roman", Georgia, serif`;
  g.textAlign = 'center';
  g.textBaseline = 'middle';
  g.shadowColor = 'rgba(0,0,0,0.65)';
  g.shadowBlur = 8;
  g.fillText(text, w / 2, h / 2);
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  t.anisotropy = 8;
  return t;
}

class SmokeColumn {
  constructor(origin, count = 42, spread = 0.25, height = 3.2) {
    this.origin = origin.clone();
    this.count = count;
    this.spread = spread;
    this.height = height;
    const geom = new THREE.BufferGeometry();
    this.positions = new Float32Array(count * 3);
    this.ages = new Float32Array(count);
    for (let i = 0; i < count; i++) {
      this.ages[i] = Math.random();
      this.resetParticle(i, this.ages[i]);
    }
    geom.setAttribute('position', new THREE.BufferAttribute(this.positions, 3));
    const c = document.createElement('canvas');
    c.width = c.height = 64;
    const g = c.getContext('2d');
    const grd = g.createRadialGradient(32, 32, 2, 32, 32, 30);
    grd.addColorStop(0, 'rgba(255,250,240,0.75)');
    grd.addColorStop(0.5, 'rgba(235,230,225,0.35)');
    grd.addColorStop(1, 'rgba(220,220,225,0)');
    g.fillStyle = grd;
    g.fillRect(0, 0, 64, 64);
    const tex = new THREE.CanvasTexture(c);
    const mat = new THREE.PointsMaterial({
      map: tex,
      size: 0.72,
      transparent: true,
      depthWrite: false,
      opacity: 0.78
    });
    this.points = new THREE.Points(geom, mat);
  }

  resetParticle(i, age = 0) {
    this.ages[i] = age;
    this.positions[i * 3] = this.origin.x + (Math.random() - 0.5) * this.spread * 0.5;
    this.positions[i * 3 + 1] = this.origin.y + age * this.height;
    this.positions[i * 3 + 2] = this.origin.z + (Math.random() - 0.5) * this.spread * 0.5;
  }

  update(dt, time) {
    for (let i = 0; i < this.count; i++) {
      this.ages[i] += (dt * 0.28) / (this.height / 3);
      if (this.ages[i] >= 1) {
        this.resetParticle(i, 0);
      } else {
        const a = this.ages[i];
        this.positions[i * 3] =
          this.origin.x + Math.sin(time * 1.4 + i) * this.spread * a + a * 0.25;
        this.positions[i * 3 + 1] = this.origin.y + a * this.height;
        this.positions[i * 3 + 2] =
          this.origin.z + Math.cos(time * 1.1 + i * 0.7) * this.spread * a;
      }
    }
    this.points.geometry.attributes.position.needsUpdate = true;
  }
}

export class VinhTrang3DWorld {
  constructor(canvas, callbacks = {}) {
    this.canvas = canvas;
    this.onStationProximity = callbacks.onStationProximity || callbacks.onStationArrive || (() => {});
    this.onStationArrive = callbacks.onStationArrive || callbacks.onStationProximity || (() => {});
    this.onPinScreenUpdate = callbacks.onPinScreenUpdate || (() => {});
    this.onUpdateProjectedPins = callbacks.onUpdateProjectedPins || (() => {});
    this.onObjectClick = callbacks.onObjectClick || (() => {});
    this.onLoaded = callbacks.onLoaded || (() => {});
    this.onAutoWalkArrival = callbacks.onAutoWalkArrival || callbacks.onStationArrive || (() => {});
    this.onAutoWalkTargetChange = callbacks.onAutoWalkTargetChange || (() => {});

    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(0x2B7DE1);
    this.scene.fog = new THREE.FogExp2(0xBDD7F2, 0.0032);

    this.camera = new THREE.PerspectiveCamera(48, 16 / 9, 0.2, 420);

    this.isSoftwareGl = (() => {
      const gl = document.createElement('canvas').getContext('webgl2');
      if (!gl) return true;
      const ext = gl.getExtension('WEBGL_debug_renderer_info');
      const param = ext ? ext.UNMASKED_RENDERER_WEBGL : gl.RENDERER;
      const gpu = String(gl.getParameter(param));
      gl.getExtension('WEBGL_lose_context')?.loseContext();
      return /SwiftShader|llvmpipe|softpipe|Software|Basic Render/i.test(gpu);
    })();

    this.renderer = new THREE.WebGLRenderer({
      canvas: this.canvas,
      antialias: !this.isSoftwareGl,
      preserveDrawingBuffer: true,
      powerPreference: 'high-performance'
    });
    this.renderer.setPixelRatio(this.isSoftwareGl ? 1 : Math.min(window.devicePixelRatio || 1, 2));
    this.renderer.shadowMap.enabled = !this.isSoftwareGl;
    this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    this.renderer.outputColorSpace = THREE.SRGBColorSpace;
    this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
    this.renderer.toneMappingExposure = 1.12;

    this.clock = new THREE.Clock();
    this.gltfLoader = new GLTFLoader();

    this.playerState = {
      x: 23.0,
      z: 21.5,
      yaw: Math.PI,
      moving: false,
      charKey: callbacks.initialCharKey || 'nu',
      pose: 'Dung',
      moveBlend: 0
    };
    this.heldDirs = new Set();
    this.currentStationId = 5;
    this.inInterior = false;
    this.cameraBaseYaw = Math.PI;
    this.cameraAzimuthOffset = 0;

    this.charDataCache = {};
    this.propMeshCache = {};
    this.playerContainer = new THREE.Group();
    this.scene.add(this.playerContainer);
    this.anCompanion = null;
    this.activePlayerRecord = null;
    this.npcRecords = [];
    this.kneelingRecords = [];
    this.koiList = [];
    this.pigeons = [];
    this.smokeColumns = [];
    this.incenseSticksGroup = new THREE.Group();
    this.offeredLotusesGroup = new THREE.Group();

    this.stationMarkers = [];
    this.autoWalkWaypoints = [];
    this.autoWalkCallback = null;
    this.autoWalkStation = null;
    this.walkTargetRing = null;
    this.walkPathLine = null;

    this.obstacles = [];
    this.rectObstacles = [];
    this.interiorObstacles = [];
    this.interiorRectObstacles = [];

    this.exteriorGroup = new THREE.Group();
    this.interiorGroup = new THREE.Group();
    this.interiorGroup.visible = false;
    this.scene.add(this.exteriorGroup);
    this.scene.add(this.interiorGroup);

    this.initTexturesAndMaterials();
    this.initLights();
    this.buildSkyDomeAndMountains();
    this.buildTempleGroundsV8();
    this.buildInteriorChanhDienV8();
    this.buildStationBeacons();
    this.initPointerAndWheelControls();
    this.handleResize();
    window.addEventListener('resize', () => this.handleResize());

    this.loadAllGLBAssets();
    this.animate();
  }

  // Compatibility getters & methods for ChuaOnlineApp
  init() {
    this.handleResize();
    this.syncPlayerTransform();
  }

  get playerPos() {
    return { x: this.playerState.x, z: this.playerState.z };
  }

  get playerYaw() {
    return this.playerState.yaw;
  }

  get playerMoving() {
    return this.playerState.moving;
  }

  get insideInterior() {
    return this.inInterior;
  }

  enterInteriorHall() {
    this.toggleInterior(true);
  }

  exitInteriorHall() {
    this.toggleInterior(false);
  }

  switchCharacter(charKey) {
    this.setCharacter(charKey);
  }

  playPlayerBowAnimation() {
    this.triggerActionAnimation('Vái');
  }

  setIncenseBoost() {
    this.addIncenseStickVisual();
    this.triggerActionAnimation('Thắp nhang');
  }

  placeLotusOfferingIn3D() {
    this.addLotusOfferingVisual();
    this.triggerActionAnimation('Chắp tay');
  }

  captureSnapshotDataURL() {
    try {
      this.renderer.render(this.scene, this.camera);
      return this.canvas.toDataURL('image/png');
    } catch {
      return null;
    }
  }

  setHeldDirection(dir, active) {
    if (!dir) return;
    if (active) {
      this.heldDirs.add(dir);
      this.cancelAutoWalk();
    } else {
      this.heldDirs.delete(dir);
      if (this.heldDirs.size === 0 && this.autoWalkWaypoints.length === 0) {
        this.playerState.moving = false;
      }
    }
  }

  clearHeldDirections() {
    this.heldDirs.clear();
    if (this.autoWalkWaypoints.length === 0) {
      this.playerState.moving = false;
    }
  }

  nudgeDirection(dir, dist = 1.35) {
    const dirMap = {
      up: { dx: 0, dz: -1 },
      down: { dx: 0, dz: 1 },
      left: { dx: -1, dz: 0 },
      right: { dx: 1, dz: 0 }
    };
    const v = dirMap[dir];
    if (!v) return;
    const angle = this.cameraBaseYaw + this.cameraAzimuthOffset;
    const forwardX = Math.sin(angle);
    const forwardZ = Math.cos(angle);
    const rightX = -forwardZ;
    const rightZ = forwardX;
    const worldDx = forwardX * (-v.dz) + rightX * v.dx;
    const worldDz = forwardZ * (-v.dz) + rightZ * v.dx;
    this.moveStep(worldDx, worldDz, dist * 0.55);
  }

  stepSimulation(dt = 0.016) {
    this.updateHeldMovement(dt);
    this.updateAutoWalk(dt);
  }

  renderFrame() {
    this.renderer.render(this.scene, this.camera);
  }

  initTexturesAndMaterials() {
    // 1. Worn Courtyard Stone Slabs + Mortar & Subtle Moss (PROMPT_ARGON_CHAT_LIEU #7)
    this.pavingTex = makeCanvasTex(
      (g, w, h) => {
        g.fillStyle = '#9C8D76';
        g.fillRect(0, 0, w, h);
        const step = 64;
        for (let y = 0; y < h; y += step) {
          for (let x = 0; x < w; x += step) {
            const seed = ((Math.sin(x * 12.9898 + y * 78.233) * 43758.5453) % 1 + 1) % 1;
            const v = seed * 22 - 11;
            g.fillStyle = `rgb(${Math.round(176 + v)}, ${Math.round(162 + v)}, ${Math.round(138 + v)})`;
            g.fillRect(x + 2, y + 2, step - 4, step - 4);
            // Subtle stone grain speckles
            g.fillStyle = seed > 0.5 ? 'rgba(255,248,235,0.12)' : 'rgba(70,58,42,0.12)';
            g.fillRect(x + 10, y + 12, step - 20, step - 24);
          }
        }
        g.strokeStyle = '#685B48';
        g.lineWidth = 3;
        for (let i = 0; i <= w; i += step) {
          g.beginPath();
          g.moveTo(i, 0);
          g.lineTo(i, h);
          g.stroke();
          g.beginPath();
          g.moveTo(0, i);
          g.lineTo(w, i);
          g.stroke();
        }
        // Subtle green moss spots in mortar intersections
        g.fillStyle = 'rgba(72, 102, 54, 0.28)';
        for (let y = 0; y <= h; y += step) {
          for (let x = 0; x <= w; x += step) {
            if ((x + y) % 128 === 0) {
              g.beginPath();
              g.arc(x, y, 5, 0, Math.PI * 2);
              g.fill();
            }
          }
        }
      },
      512,
      512,
      28,
      28
    );

    // 2. Yin-Yang Terracotta Roof Tiles + Moss Patches (PROMPT_ARGON_CHAT_LIEU #4)
    this.roofTex = makeCanvasTex(
      (g, w, h) => {
        g.fillStyle = '#7C4030';
        g.fillRect(0, 0, w, h);
        for (let y = 0; y < h; y += 24) {
          g.fillStyle = y % 48 === 0 ? '#8E4C36' : '#6E382A';
          g.fillRect(0, y, w, 20);
          g.fillStyle = '#472117';
          g.fillRect(0, y + 20, w, 4);
        }
        for (let x = 0; x < w; x += 28) {
          g.fillStyle = 'rgba(255,215,180,0.12)';
          g.fillRect(x + 4, 0, 8, h);
          g.strokeStyle = 'rgba(38,14,8,0.48)';
          g.lineWidth = 2.5;
          g.beginPath();
          g.moveTo(x, 0);
          g.lineTo(x, h);
          g.stroke();
        }
        // Subtle moss along tile grooves
        g.fillStyle = 'rgba(65, 92, 48, 0.18)';
        for (let i = 0; i < 18; i++) {
          g.beginPath();
          g.arc((i * 53) % w, (i * 41) % h, 10 + (i % 7), 0, Math.PI * 2);
          g.fill();
        }
      },
      256,
      256,
      12,
      5
    );

    // 3. Aged Warm Lime Wall Texture (#D9A441 / #E2B352) (PROMPT_ARGON_CHAT_LIEU #6)
    this.limeWallTex = makeCanvasTex(
      (g, w, h) => {
        g.fillStyle = '#DFAC48';
        g.fillRect(0, 0, w, h);
        for (let i = 0; i < 160; i++) {
          const x = (i * 79) % w;
          const y = (i * 43) % h;
          g.fillStyle = i % 2 === 0 ? 'rgba(255,244,210,0.12)' : 'rgba(155,105,32,0.10)';
          g.beginPath();
          g.arc(x, y, 18 + (i % 20), 0, Math.PI * 2);
          g.fill();
        }
      },
      256,
      256,
      4,
      2
    );

    // 4. Weathered Statue Stone Bump Texture (PROMPT_ARGON_CHAT_LIEU #1)
    this.stoneBumpTex = makeCanvasTex(
      (g, w, h) => {
        g.fillStyle = '#808080';
        g.fillRect(0, 0, w, h);
        for (let i = 0; i < 600; i++) {
          const v = 110 + ((i * 29) % 36);
          g.fillStyle = `rgb(${v},${v},${v})`;
          g.fillRect((i * 47) % w, (i * 83) % h, 3, 3);
        }
      },
      256,
      256,
      6,
      6,
      false
    );

    // 5. Vertical Wood Grain Texture (PROMPT_ARGON_CHAT_LIEU #3)
    this.woodGrainTex = makeCanvasTex(
      (g, w, h) => {
        g.fillStyle = '#5A3D26';
        g.fillRect(0, 0, w, h);
        for (let x = 0; x < w; x += 4) {
          g.fillStyle = x % 8 === 0 ? 'rgba(40,22,10,0.22)' : 'rgba(120,82,48,0.16)';
          g.fillRect(x, 0, 2, h);
        }
      },
      256,
      256,
      2,
      2
    );

    // 6. Rippled Lotus Pond Water Texture (PROMPT_ARGON_CHAT_LIEU #8)
    this.waterTex = makeCanvasTex(
      (g, w, h) => {
        const grd = g.createRadialGradient(w / 2, h / 2, 20, w / 2, h / 2, w * 0.65);
        grd.addColorStop(0, '#3D6B4C');
        grd.addColorStop(0.6, '#2F573D');
        grd.addColorStop(1, '#23422E');
        g.fillStyle = grd;
        g.fillRect(0, 0, w, h);
        g.strokeStyle = 'rgba(190, 230, 205, 0.16)';
        g.lineWidth = 1.5;
        for (let i = 0; i < 28; i++) {
          g.beginPath();
          g.arc((i * 67) % w, (i * 53) % h, 14 + (i % 18), 0, Math.PI * 2);
          g.stroke();
        }
      },
      256,
      256,
      3,
      3
    );

    // Perceptually uniform OKLCH foliage textures (meodai/skill.color-expert: warm sunlit shift + cool sky-bounce shade)
    this.leafTexA = this.makeLeafTexture(
      '#4E7A3E',
      shiftOklch('#4E7A3E', 0.11, 1.08, -6),
      shiftOklch('#4E7A3E', -0.11, 0.92, 8)
    );
    this.leafTexB = this.makeLeafTexture(
      VINH_TRANG_OKLCH_PALETTE.jadeFoliageDeep,
      shiftOklch(VINH_TRANG_OKLCH_PALETTE.jadeFoliageDeep, 0.12, 1.08, -6),
      shiftOklch(VINH_TRANG_OKLCH_PALETTE.jadeFoliageDeep, -0.1, 0.92, 8)
    );
    this.leafTexC = this.makeLeafTexture(
      VINH_TRANG_OKLCH_PALETTE.jadeFoliageSun,
      shiftOklch(VINH_TRANG_OKLCH_PALETTE.jadeFoliageSun, 0.11, 1.06, -5),
      shiftOklch(VINH_TRANG_OKLCH_PALETTE.jadeFoliageSun, -0.11, 0.94, 7)
    );
    this.flagTex72 = this.makeBuddhistFlagTexture();

    this.MAT = {
      goldWall: new THREE.MeshStandardMaterial({
        color: new THREE.Color(VINH_TRANG_OKLCH_PALETTE.goldFacadeSun),
        map: this.limeWallTex,
        bumpMap: this.stoneBumpTex,
        bumpScale: 0.015,
        roughness: 0.58
      }),
      goldLight: new THREE.MeshStandardMaterial({
        color: new THREE.Color(shiftOklch(VINH_TRANG_OKLCH_PALETTE.goldFacadeSun, 0.07, 1.02, 3)),
        map: this.limeWallTex,
        roughness: 0.52
      }),
      goldAccent: new THREE.MeshStandardMaterial({
        color: 0xD8A436,
        metalness: 0.58,
        roughness: 0.28
      }),
      creamTrim: new THREE.MeshStandardMaterial({
        color: 0xF2ECE0,
        bumpMap: this.stoneBumpTex,
        bumpScale: 0.01,
        roughness: 0.65
      }),
      redColumn: new THREE.MeshStandardMaterial({
        color: 0x862820,
        roughness: 0.42,
        metalness: 0.08
      }),
      darkWood: new THREE.MeshStandardMaterial({
        color: 0x5A3D26,
        map: this.woodGrainTex,
        roughness: 0.65
      }),
      darkOpening: new THREE.MeshStandardMaterial({ color: 0x221712, roughness: 0.88 }),
      roofTile: new THREE.MeshStandardMaterial({
        map: this.roofTex,
        bumpMap: this.roofTex,
        bumpScale: 0.04,
        roughness: 0.68
      }),
      statueWhite: new THREE.MeshStandardMaterial({
        color: 0xF4EFE6,
        bumpMap: this.stoneBumpTex,
        bumpScale: 0.012,
        roughness: 0.46,
        metalness: 0.03
      }),
      lotusBlue: new THREE.MeshStandardMaterial({ color: 0x4E86A8, roughness: 0.5 }),
      pedestalRed: new THREE.MeshStandardMaterial({ color: 0x8A4A3A, roughness: 0.62 }),
      stoneDark: new THREE.MeshStandardMaterial({
        color: 0x6E675C,
        bumpMap: this.stoneBumpTex,
        bumpScale: 0.025,
        roughness: 0.84
      }),
      stoneLight: new THREE.MeshStandardMaterial({
        color: 0xA89E8E,
        bumpMap: this.stoneBumpTex,
        bumpScale: 0.02,
        roughness: 0.78
      }),
      stupaBody: new THREE.MeshStandardMaterial({
        color: 0xD2924E,
        map: this.limeWallTex,
        roughness: 0.6
      }),
      stupaRoof: new THREE.MeshStandardMaterial({
        color: 0xA85A38,
        map: this.roofTex,
        roughness: 0.64
      }),
      mosaicBlue: new THREE.MeshStandardMaterial({
        color: 0x2C4A8A,
        roughness: 0.3,
        metalness: 0.18
      }),
      mosaicGreen: new THREE.MeshStandardMaterial({
        color: 0x3F7D5D,
        roughness: 0.3,
        metalness: 0.18
      }),
      mosaicRed: new THREE.MeshStandardMaterial({
        color: 0xA83828,
        roughness: 0.36,
        metalness: 0.12
      }),
      terracottaPot: new THREE.MeshStandardMaterial({ color: 0xA45236, roughness: 0.68 }),
      trunk: new THREE.MeshStandardMaterial({
        color: 0x5A402C,
        map: this.woodGrainTex,
        roughness: 0.88
      }),
      foliageDark: new THREE.MeshStandardMaterial({
        color: 0x3E6B34,
        map: this.leafTexB,
        roughness: 0.8,
        bumpMap: this.leafTexB,
        bumpScale: 0.08
      }),
      foliageMid: new THREE.MeshStandardMaterial({
        color: 0x4E7A3E,
        map: this.leafTexA,
        roughness: 0.78,
        bumpMap: this.leafTexA,
        bumpScale: 0.08
      }),
      foliageLight: new THREE.MeshStandardMaterial({
        color: 0x5C8446,
        map: this.leafTexC,
        roughness: 0.75,
        bumpMap: this.leafTexC,
        bumpScale: 0.08
      }),
      bougainvilleaPink: new THREE.MeshStandardMaterial({ color: 0xF078AA, roughness: 0.58 }),
      bougainvilleaRed: new THREE.MeshStandardMaterial({ color: 0xD94F3D, roughness: 0.6 }),
      marigold: new THREE.MeshStandardMaterial({ color: 0xF0AE2E, roughness: 0.6 }),
      lotusLeaf: new THREE.MeshStandardMaterial({ color: 0x3E6E36, roughness: 0.72 }),
      pondWater: new THREE.MeshStandardMaterial({
        map: this.waterTex,
        color: 0x5C8568,
        roughness: 0.18,
        metalness: 0.38
      }),
      bronzeBurner: new THREE.MeshStandardMaterial({
        color: 0x487A5E,
        roughness: 0.38,
        metalness: 0.62
      }),
      lanternGlow: new THREE.MeshStandardMaterial({
        color: 0xFFE8AD,
        emissive: 0xFFB84D,
        emissiveIntensity: 0.92
      })
    };
  }

  makeLeafTexture(baseHex, lightHex, darkHex) {
    const c = document.createElement('canvas');
    c.width = c.height = 128;
    const g = c.getContext('2d');
    g.fillStyle = baseHex;
    g.fillRect(0, 0, 128, 128);
    for (let i = 0; i < 220; i++) {
      const r = Math.random();
      g.fillStyle = r < 0.45 ? lightHex : r < 0.82 ? baseHex : darkHex;
      const x = Math.random() * 128;
      const y = Math.random() * 128;
      g.beginPath();
      g.ellipse(
        x,
        y,
        3 + Math.random() * 4,
        2 + Math.random() * 3,
        Math.random() * Math.PI,
        0,
        Math.PI * 2
      );
      g.fill();
    }
    const t = new THREE.CanvasTexture(c);
    t.wrapS = t.wrapT = THREE.RepeatWrapping;
    t.repeat.set(3, 3);
    t.colorSpace = THREE.SRGBColorSpace;
    return t;
  }

  makeBuddhistFlagTexture() {
    const c = document.createElement('canvas');
    c.width = 120;
    c.height = 80;
    const g = c.getContext('2d');
    const cols = ['#1E4FA3', '#F2C12E', '#C9382B', '#F5F2EB', '#E87425'];
    for (let i = 0; i < 5; i++) {
      g.fillStyle = cols[i];
      g.fillRect(i * 20, 0, 20, 80);
    }
    for (let i = 0; i < 5; i++) {
      g.fillStyle = cols[i];
      g.fillRect(100, i * 16, 20, 16);
    }
    const t = new THREE.CanvasTexture(c);
    t.colorSpace = THREE.SRGBColorSpace;
    return t;
  }

  initLights() {
    const hemi = new THREE.HemisphereLight(0xfff2d9, 0x5e4a35, 1.3);
    this.scene.add(hemi);

    const sun = new THREE.DirectionalLight(0xffd9a3, 1.7);
    sun.position.set(-30, 25, 18);
    sun.castShadow = true;
    sun.shadow.mapSize.set(1024, 1024);
    sun.shadow.camera.left = -65;
    sun.shadow.camera.right = 65;
    sun.shadow.camera.top = 65;
    sun.shadow.camera.bottom = -65;
    sun.shadow.camera.near = 5;
    sun.shadow.camera.far = 150;
    sun.shadow.bias = -0.0004;
    this.scene.add(sun);

    const frontFill = new THREE.DirectionalLight(0xfff6e0, 0.55);
    frontFill.position.set(25, 20, 55);
    this.scene.add(frontFill);
  }

  buildSkyDomeAndMountains() {
    const skyCanvas = document.createElement('canvas');
    skyCanvas.width = 512;
    skyCanvas.height = 256;
    const sctx = skyCanvas.getContext('2d');
    const grad = sctx.createLinearGradient(0, 0, 0, 256);
    grad.addColorStop(0.0, '#0155C9');
    grad.addColorStop(0.55, '#4F97F9');
    grad.addColorStop(0.88, '#9CC9FA');
    grad.addColorStop(1.0, '#E7F0FA');
    sctx.fillStyle = grad;
    sctx.fillRect(0, 0, 512, 256);
    sctx.fillStyle = 'rgba(255,252,245,0.58)';
    for (let i = 0; i < 20; i++) {
      const cx = (i * 73) % 500;
      const cy = 65 + (i % 4) * 26;
      for (let j = 0; j < 4; j++) {
        sctx.beginPath();
        sctx.arc(cx + j * 14, cy + (j % 2) * 5, 16 - j * 2, 0, Math.PI * 2);
        sctx.fill();
      }
    }
    const skyTex = new THREE.CanvasTexture(skyCanvas);
    skyTex.colorSpace = THREE.SRGBColorSpace;
    const skyDome = new THREE.Mesh(
      new THREE.SphereGeometry(240, 32, 18),
      new THREE.MeshBasicMaterial({ map: skyTex, side: THREE.BackSide, fog: false })
    );
    this.scene.add(skyDome);

    const mMat = new THREE.MeshStandardMaterial({
      color: 0x7A9BB8,
      roughness: 0.95,
      fog: true
    });
    const peaks = [
      [-90, -135, 55, 28],
      [-35, -145, 65, 34],
      [25, -140, 60, 30],
      [85, -135, 52, 26],
      [-115, 30, 50, 22],
      [125, 25, 50, 22],
      [-60, 140, 62, 24],
      [15, 148, 70, 28],
      [80, 138, 56, 22]
    ];
    for (const [mx, mz, r, h] of peaks) {
      const m = new THREE.Mesh(new THREE.ConeGeometry(r, h, 7), mMat);
      m.position.set(mx, h / 2 - 2, mz);
      m.rotation.y = (mx * 0.13) % Math.PI;
      this.exteriorGroup.add(m);
    }
  }

  addObstacle(x, z, r) {
    this.obstacles.push({ x, z, r });
  }

  addRectObstacle(minX, maxX, minZ, maxZ) {
    this.rectObstacles.push({ minX, maxX, minZ, maxZ });
  }

  buildTempleGroundsV8() {
    const M = this.MAT;

    const grass = new THREE.Mesh(
      new THREE.PlaneGeometry(320, 320),
      new THREE.MeshStandardMaterial({ color: 0x3E6832, roughness: 0.95 })
    );
    grass.rotation.x = -Math.PI / 2;
    grass.position.y = -0.05;
    grass.receiveShadow = true;
    this.exteriorGroup.add(grass);

    const courtyard = new THREE.Mesh(
      new THREE.BoxGeometry(93, 0.1, 95),
      new THREE.MeshStandardMaterial({ map: this.pavingTex, color: 0xB4A68C, roughness: 0.85 })
    );
    courtyard.position.set(7.5, -0.04, 5);
    courtyard.receiveShadow = true;
    this.exteriorGroup.add(courtyard);

    const mainRoad = new THREE.Mesh(
      new THREE.BoxGeometry(10.5, 0.12, 38),
      new THREE.MeshStandardMaterial({ map: this.pavingTex, color: 0xBFAE8E, roughness: 0.78 })
    );
    mainRoad.position.set(23, 0.0, 23);
    mainRoad.receiveShadow = true;
    this.exteriorGroup.add(mainRoad);

    this.buildFenceAndGateWall();
    const road = new THREE.Mesh(
      new THREE.BoxGeometry(118, 0.08, 10),
      new THREE.MeshStandardMaterial({ color: 0x4A4A4E, roughness: 0.9 })
    );
    road.position.set(7.5, -0.02, 58);
    road.receiveShadow = true;
    this.exteriorGroup.add(road);

    const gateEast = this.buildTamQuanGate('CHÙA VĨNH TRÀNG');
    gateEast.position.set(23, 0, 40.7);
    this.exteriorGroup.add(gateEast);

    const gateWest = this.buildTamQuanGate('VĨNH TRÀNG ĐẠI PHẬT TỰ');
    gateWest.position.set(3, 0, 41.3);
    this.exteriorGroup.add(gateWest);

    const chanhDien = this.buildChanhDien13Arches();
    chanhDien.position.set(23, 0, -1);
    this.exteriorGroup.add(chanhDien);

    const leftHall = this.buildSideHall(8.3, 18.8, 5.2, M.goldWall);
    leftHall.position.set(9.8, 0, -2.1);
    this.exteriorGroup.add(leftHall);
    this.addRectObstacle(5.6, 14.0, -11.5, 7.3);

    const rightHall = this.buildSideHall(7.7, 17.6, 5.2, M.goldWall);
    rightHall.position.set(36.2, 0, -0.9);
    this.exteriorGroup.add(rightHall);
    this.addRectObstacle(32.3, 40.1, -9.7, 7.9);

    this.buildIncenseStallAndBookRoom();

    const giangDuong = this.buildGiangDuong();
    giangDuong.position.set(44, 0, -20);
    this.exteriorGroup.add(giangDuong);
    this.addRectObstacle(39, 49, -30, -10);

    const stupa = this.buildSevenTierStupa();
    stupa.position.set(23, 0, -39);
    this.exteriorGroup.add(stupa);
    this.addObstacle(23, -39, 4.2);

    const rearRight = this.buildSideHall(17.9, 13.7, 5.0, M.creamTrim);
    rearRight.position.set(32.6, 0, -24.1);
    this.exteriorGroup.add(rearRight);
    this.addRectObstacle(23.6, 41.6, -31.0, -17.2);

    const rearLeft = this.buildSideHall(12.2, 7.8, 4.6, M.creamTrim);
    rearLeft.position.set(7.5, 0, -31.7);
    this.exteriorGroup.add(rearLeft);
    this.addRectObstacle(1.4, 13.6, -35.6, -27.8);

    this.buildStatuePedestals();

    const pond1 = this.buildLotusPond(17.4, 11.4, 12);
    pond1.position.set(5.0, 0, 16.0);
    this.exteriorGroup.add(pond1);
    this.addRectObstacle(-4.0, 14.0, 10.0, 22.0);

    const pond2 = this.buildLotusPond(12.0, 8.6, 8);
    pond2.position.set(5.0, 0, -16.0);
    this.exteriorGroup.add(pond2);
    this.addRectObstacle(-1.2, 11.2, -20.5, -11.5);

    const mainBurner = this.buildIncenseBurner(1.1);
    mainBurner.position.set(23, 0, 11);
    this.exteriorGroup.add(mainBurner);
    this.addObstacle(23, 11, 1.3);
    this.incenseSticksGroup.position.set(23, 1.48, 11);
    this.exteriorGroup.add(this.incenseSticksGroup);
    this.offeredLotusesGroup.position.set(13.2, 0.45, 16.0);
    this.exteriorGroup.add(this.offeredLotusesGroup);

    const burnerAdida = this.buildIncenseBurner(0.75);
    burnerAdida.position.set(-14, 0, 19.2);
    this.exteriorGroup.add(burnerAdida);
    this.addObstacle(-14, 19.2, 0.9);

    const burnerDiLac = this.buildIncenseBurner(0.8);
    burnerDiLac.position.set(-24.5, 0, 3.8);
    this.exteriorGroup.add(burnerDiLac);
    this.addObstacle(-24.5, 3.8, 0.9);

    const cushionCoords = [
      [21.6, 12.6, Math.PI],
      [24.4, 12.6, Math.PI],
      [23.0, 13.4, Math.PI],
      [-14.0, 17.5, 0],
      [-24.5, 5.2, Math.PI]
    ];
    for (const [kx, kz, kyaw] of cushionCoords) {
      const c = this.makeKneelingCushion();
      c.position.set(kx, 0, kz);
      c.rotation.y = kyaw;
      this.exteriorGroup.add(c);
    }

    const lanternZ = [15, 21, 27, 33];
    for (const z of lanternZ) {
      for (const x of [17.8, 28.2]) {
        const l = this.makeStoneLantern();
        l.position.set(x, 0, z);
        this.exteriorGroup.add(l);
        this.addObstacle(x, z, 0.65);
      }
    }

    this.buildGardensTreesAndFlags();

    this.shopKioskAnchor = new THREE.Group();
    this.shopKioskAnchor.position.set(40, 0, 38);
    this.shopKioskAnchor.rotation.y = -Math.PI * 0.25;
    this.exteriorGroup.add(this.shopKioskAnchor);
    this.buildProceduralShopPavilion();
    this.addObstacle(40, 38, 3.2);

    this.buildCourtyardPigeons();
  }

  buildFenceAndGateWall() {
    const M = this.MAT;
    const g = new THREE.Group();
    const baseMat = M.goldWall;
    const barMat = M.goldAccent;

    const addWallSeg = (x1, z1, x2, z2) => {
      const len = Math.hypot(x2 - x1, z2 - z1);
      const ang = Math.atan2(x2 - x1, z2 - z1);
      const seg = new THREE.Group();
      const base = new THREE.Mesh(new THREE.BoxGeometry(0.45, 0.85, len), baseMat);
      base.position.y = 0.425;
      seg.add(base);
      const topRail = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.12, len), barMat);
      topRail.position.y = 2.05;
      seg.add(topRail);
      const posts = Math.max(2, Math.floor(len / 4));
      for (let i = 0; i <= posts; i++) {
        const pz = -len / 2 + (i / posts) * len;
        const post = new THREE.Mesh(new THREE.BoxGeometry(0.55, 2.35, 0.55), baseMat);
        post.position.set(0, 1.175, pz);
        seg.add(post);
        const cap = new THREE.Mesh(new THREE.SphereGeometry(0.24, 8, 8), M.lotusBlue);
        cap.position.set(0, 2.48, pz);
        seg.add(cap);
      }
      seg.position.set((x1 + x2) / 2, 0, (z1 + z2) / 2);
      seg.rotation.y = ang;
      g.add(seg);
    };

    addWallSeg(-39, 41, -3, 41);
    addWallSeg(9, 41, 16, 41);
    addWallSeg(30, 41, 54, 41);
    addWallSeg(-39, -45, -39, 41);
    addWallSeg(54, -45, 54, 41);
    addWallSeg(-39, -45, 54, -45);
    this.exteriorGroup.add(g);
  }

  buildTamQuanGate(signText = 'CHÙA VĨNH TRÀNG') {
    const M = this.MAT;
    const g = new THREE.Group();
    const pillarPositions = [-5.8, -2.5, 2.5, 5.8];
    const pillarHeights = [6.2, 8.2, 8.2, 6.2];

    pillarPositions.forEach((px, i) => {
      const h = pillarHeights[i];
      const p = new THREE.Mesh(new THREE.BoxGeometry(1.15, h, 1.15), M.goldWall);
      p.position.set(px, h / 2, 0);
      p.castShadow = true;
      g.add(p);

      const strip = new THREE.Mesh(new THREE.BoxGeometry(0.75, h - 1.2, 1.2), M.mosaicBlue);
      strip.position.set(px, h / 2, 0);
      g.add(strip);

      const finial = new THREE.Mesh(new THREE.ConeGeometry(0.55, 1.3, 8), M.mosaicRed);
      finial.position.set(px, h + 0.65, 0);
      g.add(finial);
    });

    const beam = new THREE.Mesh(new THREE.BoxGeometry(6.4, 1.5, 1.35), M.goldWall);
    beam.position.set(0, 6.4, 0);
    g.add(beam);

    const signTex = makeTextTex(signText, {
      w: 1024,
      h: 220,
      bg: '#2C4A8A',
      border: '#D9A441',
      color: '#FFD875',
      size: 68
    });
    const sign = new THREE.Mesh(
      new THREE.BoxGeometry(4.8, 1.0, 1.42),
      new THREE.MeshStandardMaterial({ map: signTex, roughness: 0.4 })
    );
    sign.position.set(0, 6.4, 0);
    g.add(sign);

    for (let t = 0; t < 2; t++) {
      const w = 7.4 - t * 2.0;
      const roof = new THREE.Mesh(new THREE.ConeGeometry(w * 0.72, 1.35, 4), M.mosaicGreen);
      roof.rotation.y = Math.PI / 4;
      roof.scale.set(1.3, 1, 0.55);
      roof.position.set(0, 7.7 + t * 1.35, 0);
      g.add(roof);
    }

    for (const sx of [-4.15, 4.15]) {
      const sb = new THREE.Mesh(new THREE.BoxGeometry(3.4, 1.0, 1.15), M.goldWall);
      sb.position.set(sx, 4.7, 0);
      g.add(sb);
      const sr = new THREE.Mesh(new THREE.ConeGeometry(2.5, 1.1, 4), M.mosaicGreen);
      sr.rotation.y = Math.PI / 4;
      sr.scale.set(1.2, 1, 0.55);
      sr.position.set(sx, 5.7, 0);
      g.add(sr);
    }
    return g;
  }

  buildChanhDien13Arches() {
    const M = this.MAT;
    const g = new THREE.Group();
    const W = 26.9;
    const D = 14.3;

    const plinth = new THREE.Mesh(new THREE.BoxGeometry(W + 1.2, 1.25, D + 1.6), M.stoneLight);
    plinth.position.set(0, 0.625, 0);
    plinth.receiveShadow = true;
    plinth.castShadow = true;
    g.add(plinth);

    for (let s = 0; s < 5; s++) {
      const step = new THREE.Mesh(
        new THREE.BoxGeometry(8.6, 0.25, 0.55),
        s % 2 === 0 ? M.stoneLight : M.stoneDark
      );
      step.position.set(0, 0.125 + s * 0.25, D / 2 + 0.8 + (4 - s) * 0.48);
      step.receiveShadow = true;
      g.add(step);
    }
    for (const sx of [-4.5, 4.5]) {
      const rail = new THREE.Mesh(new THREE.BoxGeometry(0.42, 1.45, 2.8), M.goldWall);
      rail.position.set(sx, 0.85, D / 2 + 1.6);
      g.add(rail);
      const post = new THREE.Mesh(new THREE.BoxGeometry(0.58, 1.85, 0.58), M.creamTrim);
      post.position.set(sx, 1.0, D / 2 + 2.9);
      g.add(post);
      const ball = new THREE.Mesh(new THREE.SphereGeometry(0.28, 12, 10), M.goldAccent);
      ball.position.set(sx, 2.05, D / 2 + 2.9);
      g.add(ball);
    }

    const bodyH = 6.2;
    const body = new THREE.Mesh(new THREE.BoxGeometry(W, bodyH, D), M.goldWall);
    body.position.set(0, 1.25 + bodyH / 2, 0);
    body.castShadow = true;
    body.receiveShadow = true;
    g.add(body);

    const upperCream = new THREE.Mesh(new THREE.BoxGeometry(W + 0.25, 1.65, 0.85), M.creamTrim);
    upperCream.position.set(0, 1.25 + bodyH - 0.82, D / 2 - 0.1);
    g.add(upperCream);

    const fz = D / 2 + 0.35;
    for (let x = -12; x <= 12; x += 2) {
      const col = new THREE.Mesh(new THREE.CylinderGeometry(0.24, 0.27, 4.3, 14), M.redColumn);
      col.position.set(x, 3.4, fz);
      col.castShadow = true;
      g.add(col);

      const base = new THREE.Mesh(new THREE.BoxGeometry(0.68, 0.55, 0.68), M.goldAccent);
      base.position.set(x, 1.52, fz);
      g.add(base);

      const cap = new THREE.Mesh(new THREE.BoxGeometry(0.7, 0.42, 0.7), M.goldAccent);
      cap.position.set(x, 5.55, fz);
      g.add(cap);

      const pil = new THREE.Mesh(new THREE.BoxGeometry(0.32, 1.5, 0.32), M.goldWall);
      pil.position.set(x, 6.62, fz - 0.15);
      g.add(pil);

      if (x < 12) {
        const cx = x + 1;
        const archOuter = new THREE.Mesh(
          new THREE.TorusGeometry(0.95, 0.16, 10, 20, Math.PI),
          M.creamTrim
        );
        archOuter.position.set(cx, 4.65, fz);
        g.add(archOuter);

        const archInner = new THREE.Mesh(
          new THREE.TorusGeometry(0.78, 0.1, 8, 18, Math.PI),
          M.redColumn
        );
        archInner.position.set(cx, 4.65, fz + 0.04);
        g.add(archInner);

        const isCenterDoor = Math.abs(cx) <= 2.5;
        const recess = new THREE.Mesh(
          new THREE.BoxGeometry(1.65, isCenterDoor ? 3.85 : 3.2, 0.25),
          M.darkOpening
        );
        recess.position.set(cx, isCenterDoor ? 3.25 : 3.55, fz - 0.35);
        g.add(recess);

        if (!isCenterDoor) {
          const bal = new THREE.Mesh(new THREE.BoxGeometry(1.75, 0.95, 0.32), M.goldLight);
          bal.position.set(cx, 1.78, fz - 0.05);
          g.add(bal);
          for (let gIdx = -0.55; gIdx <= 0.55; gIdx += 0.275) {
            const bar = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.025, 2.3, 6), M.goldAccent);
            bar.position.set(cx + gIdx, 3.5, fz - 0.18);
            g.add(bar);
          }
        }

        const panel = new THREE.Mesh(new THREE.BoxGeometry(1.55, 0.85, 0.18), M.mosaicBlue);
        panel.position.set(cx, 6.62, fz - 0.08);
        g.add(panel);
        const rosette = new THREE.Mesh(new THREE.CylinderGeometry(0.26, 0.26, 0.22, 12), M.goldAccent);
        rosette.rotation.x = Math.PI / 2;
        rosette.position.set(cx, 6.62, fz - 0.05);
        g.add(rosette);
      }
    }

    const innerGlow = new THREE.Mesh(
      new THREE.PlaneGeometry(3.4, 3.8),
      new THREE.MeshBasicMaterial({ color: 0x3A1E0E })
    );
    innerGlow.position.set(0, 3.3, fz - 0.42);
    g.add(innerGlow);
    const miniAltarBuddha = new THREE.Mesh(
      new THREE.SphereGeometry(0.55, 14, 12),
      new THREE.MeshStandardMaterial({
        color: 0xFFD25A,
        emissive: 0xC98A1E,
        emissiveIntensity: 0.7,
        metalness: 0.6,
        roughness: 0.25
      })
    );
    miniAltarBuddha.scale.set(1, 1.45, 0.7);
    miniAltarBuddha.position.set(0, 3.35, fz - 0.32);
    g.add(miniAltarBuddha);

    const cornice1 = new THREE.Mesh(new THREE.BoxGeometry(W + 1.0, 0.45, D + 1.2), M.goldLight);
    cornice1.position.set(0, 5.85, 0);
    g.add(cornice1);

    const mosaicBand = new THREE.Mesh(new THREE.BoxGeometry(W + 0.6, 0.55, D + 0.6), M.mosaicBlue);
    mosaicBand.position.set(0, 7.55, 0);
    g.add(mosaicBand);

    const cornice2 = new THREE.Mesh(new THREE.BoxGeometry(W + 1.3, 0.5, D + 1.4), M.creamTrim);
    cornice2.position.set(0, 7.95, 0);
    g.add(cornice2);

    // Ornate Ceramic Mosaic Relief Panels across the 7 bays (matching real Chùa Vĩnh Tràng & Reference Image 1)
    for (let bi = -3; bi <= 3; bi++) {
      const bx = bi * 3.1;
      const frame = new THREE.Mesh(new THREE.BoxGeometry(2.45, 0.88, 0.34), M.creamTrim);
      frame.position.set(bx, 6.65, fz + 0.25);
      g.add(frame);
      const inlay = new THREE.Mesh(new THREE.BoxGeometry(2.15, 0.62, 0.38), M.mosaicBlue);
      inlay.position.set(bx, 6.65, fz + 0.27);
      g.add(inlay);
      const floral = new THREE.Mesh(new THREE.BoxGeometry(1.1, 0.28, 0.42), M.goldAccent);
      floral.position.set(bx, 6.65, fz + 0.29);
      g.add(floral);
    }

    // Refined traditional gold-on-crimson plaque tucked above central archway
    const mainSignTex = makeTextTex('CHÙA VĨNH TRÀNG', {
      w: 1536,
      h: 320,
      bg: '#5C1610',
      border: '#FFD86B',
      color: '#FFF2B2',
      size: 130
    });
    const mainSign = new THREE.Mesh(
      new THREE.BoxGeometry(3.4, 0.72, 0.36),
      new THREE.MeshStandardMaterial({
        map: mainSignTex,
        roughness: 0.28,
        emissive: 0x3A1808,
        emissiveIntensity: 0.22
      })
    );
    mainSign.position.set(0, 5.38, fz + 0.36);
    g.add(mainSign);

    // 3 Stepped Baroque-Khmer Pediment Towers (Left [-8.5], Center [0], Right [8.5])
    for (const [gx, gw, gh, tiers] of [
      [-8.5, 5.4, 2.8, 2],
      [0, 7.8, 4.2, 3],
      [8.5, 5.4, 2.8, 2]
    ]) {
      for (let t = 0; t < tiers; t++) {
        const tw = gw * (1 - t * 0.24);
        const th = (gh / tiers) * 1.05;
        const ty = 8.2 + t * (gh / tiers) + th / 2;
        const ped = new THREE.Mesh(new THREE.BoxGeometry(tw, th, 1.15 - t * 0.12), M.goldLight);
        ped.position.set(gx, ty, D / 2 - 0.3);
        g.add(ped);

        const trim = new THREE.Mesh(
          new THREE.BoxGeometry(tw + 0.45, 0.26, 1.28 - t * 0.1),
          M.creamTrim
        );
        trim.position.set(gx, ty + th / 2, D / 2 - 0.3);
        g.add(trim);

        const inl = new THREE.Mesh(
          new THREE.BoxGeometry(tw * 0.56, th * 0.48, 1.22 - t * 0.1),
          M.mosaicBlue
        );
        inl.position.set(gx, ty, D / 2 - 0.28);
        g.add(inl);
      }

      const spire = new THREE.Mesh(new THREE.ConeGeometry(0.42, 1.45, 8), M.goldAccent);
      spire.position.set(gx, 8.2 + gh + 0.75, D / 2 - 0.3);
      g.add(spire);
    }

    const roof1 = new THREE.Mesh(new THREE.ConeGeometry(18.5, 2.8, 4), M.roofTile);
    roof1.rotation.y = Math.PI / 4;
    roof1.scale.set(1.12, 1, 0.58);
    roof1.position.set(0, 9.2, -0.6);
    roof1.castShadow = true;
    g.add(roof1);

    const roof2 = new THREE.Mesh(new THREE.ConeGeometry(13.5, 2.5, 4), M.roofTile);
    roof2.rotation.y = Math.PI / 4;
    roof2.scale.set(1.1, 1, 0.55);
    roof2.position.set(0, 11.1, -0.8);
    roof2.castShadow = true;
    g.add(roof2);

    for (const tx of [-15.6, 15.6]) {
      const tBase = new THREE.Mesh(new THREE.BoxGeometry(3.6, 7.6, 3.6), M.goldWall);
      tBase.position.set(tx, 3.8, D / 2 - 1.4);
      tBase.castShadow = true;
      g.add(tBase);

      const tTop = new THREE.Mesh(new THREE.BoxGeometry(3.0, 2.8, 3.0), M.goldLight);
      tTop.position.set(tx, 9.0, D / 2 - 1.4);
      g.add(tTop);

      const tRoof = new THREE.Mesh(new THREE.ConeGeometry(2.6, 1.8, 4), M.roofTile);
      tRoof.rotation.y = Math.PI / 4;
      tRoof.position.set(tx, 11.3, D / 2 - 1.4);
      g.add(tRoof);
    }

    for (const bx of [-5.8, 5.8]) {
      const b = this.makeBonsai72(1.18);
      b.position.set(bx, 0, D / 2 + 2.1);
      g.add(b);
    }
    for (const bx of [-8.8, 8.8]) {
      const b = this.makeBonsai72(0.82);
      b.position.set(bx, 0, D / 2 + 1.9);
      g.add(b);
    }

    this.addRectObstacle(9.5, 19.2, -8.5, 6.2);
    this.addRectObstacle(26.8, 36.5, -8.5, 6.2);
    this.addRectObstacle(9.5, 36.5, -8.5, -1.5);
    return g;
  }

  makeBonsai72(scale = 1) {
    const M = this.MAT;
    const g = new THREE.Group();
    const stand = new THREE.Mesh(new THREE.CylinderGeometry(0.42, 0.52, 0.45, 12), M.stoneDark);
    stand.position.y = 0.225;
    g.add(stand);
    const pot = new THREE.Mesh(
      new THREE.CylinderGeometry(0.78, 0.52, 0.68, 16),
      M.terracottaPot
    );
    pot.position.y = 0.78;
    pot.castShadow = true;
    g.add(pot);
    const rim = new THREE.Mesh(
      new THREE.TorusGeometry(0.78, 0.07, 8, 18),
      M.terracottaPot
    );
    rim.rotation.x = Math.PI / 2;
    rim.position.y = 1.12;
    g.add(rim);
    const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.24, 1.9, 10), M.trunk);
    trunk.position.y = 1.95;
    trunk.rotation.z = 0.08;
    g.add(trunk);
    const pads = [
      [0, 1.55, 0, 0.85],
      [-0.58, 1.95, 0.15, 0.68],
      [0.58, 2.15, -0.1, 0.68],
      [-0.38, 2.55, -0.1, 0.56],
      [0.35, 2.7, 0.12, 0.54],
      [0, 3.05, 0, 0.52]
    ];
    for (const [px, py, pz, r] of pads) {
      const pad = new THREE.Mesh(new THREE.SphereGeometry(r, 12, 10), M.foliageMid);
      pad.scale.set(1.35, 0.42, 1.15);
      pad.position.set(px, py, pz);
      pad.castShadow = true;
      g.add(pad);
    }
    g.scale.setScalar(scale);
    return g;
  }

  buildSideHall(w, d, h, wallMat) {
    const M = this.MAT;
    const g = new THREE.Group();
    const body = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), wallMat);
    body.position.y = h / 2;
    body.castShadow = true;
    body.receiveShadow = true;
    g.add(body);
    const roof = new THREE.Mesh(
      new THREE.ConeGeometry(Math.max(w, d) * 0.76, 2.2, 4),
      M.roofTile
    );
    roof.rotation.y = Math.PI / 4;
    roof.scale.set(w / Math.max(w, d), 1, d / Math.max(w, d));
    roof.position.y = h + 1.05;
    roof.castShadow = true;
    g.add(roof);
    return g;
  }

  buildIncenseStallAndBookRoom() {
    const M = this.MAT;
    const stall = new THREE.Group();
    const counter = new THREE.Mesh(
      new THREE.BoxGeometry(3.6, 0.95, 1.6),
      new THREE.MeshStandardMaterial({ color: 0x6E3B22, roughness: 0.7 })
    );
    counter.position.y = 0.475;
    counter.castShadow = true;
    stall.add(counter);
    for (const [px, pz] of [
      [-1.65, -0.65],
      [1.65, -0.65],
      [-1.65, 0.65],
      [1.65, 0.65]
    ]) {
      const p = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 2.5, 8), M.redColumn);
      p.position.set(px, 1.25, pz);
      stall.add(p);
    }
    const roof = new THREE.Mesh(new THREE.ConeGeometry(2.8, 0.95, 4), M.roofTile);
    roof.rotation.y = Math.PI / 4;
    roof.scale.set(1.15, 1, 0.65);
    roof.position.y = 2.85;
    stall.add(roof);
    const sign = new THREE.Mesh(
      new THREE.BoxGeometry(2.6, 0.48, 0.08),
      new THREE.MeshStandardMaterial({
        map: makeTextTex('QUẦY HƯƠNG HOA · LỘC PHẬT', { w: 768, h: 160, size: 54 })
      })
    );
    sign.position.set(0, 2.35, 0.75);
    stall.add(sign);
    stall.position.set(12.2, 0, 28.5);
    this.exteriorGroup.add(stall);
    this.addObstacle(12.2, 28.5, 2.0);
  }

  buildGiangDuong() {
    const M = this.MAT;
    const g = new THREE.Group();
    const f1 = new THREE.Mesh(new THREE.BoxGeometry(9.6, 4.2, 18.8), M.goldWall);
    f1.position.y = 2.1;
    f1.castShadow = true;
    f1.receiveShadow = true;
    g.add(f1);
    const f2 = new THREE.Mesh(new THREE.BoxGeometry(9.2, 3.8, 18.2), M.creamTrim);
    f2.position.y = 6.1;
    f2.castShadow = true;
    g.add(f2);
    const roof = new THREE.Mesh(new THREE.ConeGeometry(13.8, 2.8, 4), M.roofTile);
    roof.rotation.y = Math.PI / 4;
    roof.scale.set(0.56, 1, 1.05);
    roof.position.y = 9.3;
    roof.castShadow = true;
    g.add(roof);
    const sign = new THREE.Mesh(
      new THREE.BoxGeometry(5.8, 0.95, 0.18),
      new THREE.MeshStandardMaterial({
        map: makeTextTex('GIẢNG ĐƯỜNG PHẬT PHÁP', { w: 1024, h: 200, size: 68 })
      })
    );
    sign.rotation.y = -Math.PI / 2;
    sign.position.set(-4.85, 4.2, 0);
    g.add(sign);
    return g;
  }

  buildSevenTierStupa() {
    const M = this.MAT;
    const g = new THREE.Group();
    const base = new THREE.Mesh(new THREE.CylinderGeometry(4.2, 4.6, 1.4, 8), M.stoneDark);
    base.position.y = 0.7;
    base.receiveShadow = true;
    g.add(base);
    let y = 1.4;
    for (let i = 0; i < 7; i++) {
      const r = 3.0 - i * 0.28;
      const h = 2.2 - i * 0.1;
      const body = new THREE.Mesh(new THREE.CylinderGeometry(r * 0.88, r, h, 8), M.stupaBody);
      body.position.y = y + h / 2;
      body.castShadow = true;
      g.add(body);
      const roof = new THREE.Mesh(new THREE.ConeGeometry(r * 1.32, 0.78, 8), M.stupaRoof);
      roof.position.y = y + h + 0.35;
      roof.castShadow = true;
      g.add(roof);
      y += h + 0.45;
    }
    const spire = new THREE.Mesh(new THREE.ConeGeometry(0.38, 2.8, 12), M.goldAccent);
    spire.position.y = y + 1.4;
    g.add(spire);
    return g;
  }

  buildStatuePedestals() {
    const M = this.MAT;

    // 1. Đại Tượng Phật A Di Đà (Monumental statue with sculpted lotus throne & pedestal)
    this.adidaGroup = new THREE.Group();
    this.adidaGroup.position.set(-14, 0, 28);
    const adidaTerrace = new THREE.Mesh(
      new THREE.CylinderGeometry(6.8, 7.4, 0.36, 16),
      M.stoneLight
    );
    adidaTerrace.position.y = 0.18;
    adidaTerrace.receiveShadow = true;
    this.adidaGroup.add(adidaTerrace);

    const adidaFrontSign = new THREE.Mesh(
      new THREE.BoxGeometry(4.2, 0.85, 0.16),
      new THREE.MeshStandardMaterial({
        map: makeTextTex('ĐẠI TƯỢNG PHẬT A DI ĐÀ (CAO 24M)', { w: 1024, h: 200, size: 54 })
      })
    );
    adidaFrontSign.position.set(0, 0.85, -5.2);
    adidaFrontSign.rotation.y = Math.PI;
    this.adidaGroup.add(adidaFrontSign);

    // Semi-circular dark green foliage backdrop BEHIND A Di Đà (+Z side, z = 36.5) so front view is 100% unobstructed
    for (let i = -3; i <= 3; i++) {
      const ang = i * 0.32;
      const tx = Math.sin(ang) * 9.5;
      const tz = Math.cos(ang) * 8.5;
      const t = new THREE.Group();
      const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.32, 0.48, 5.2, 8), M.trunk);
      trunk.position.y = 2.6;
      t.add(trunk);
      const crown = new THREE.Mesh(new THREE.SphereGeometry(2.8, 12, 10), M.foliageDark);
      crown.position.y = 5.8;
      crown.scale.set(1.15, 1.1, 1.15);
      t.add(crown);
      t.position.set(tx, 0, tz);
      this.adidaGroup.add(t);
    }
    this.exteriorGroup.add(this.adidaGroup);
    this.addObstacle(-14, 28, 4.8);

    // 2. Đại Tượng Phật Di Lặc (Monumental seated statue with sculpted pedestal & plaque)
    this.dilacGroup = new THREE.Group();
    this.dilacGroup.position.set(-24.5, 0, -4);
    const dilacTerrace = new THREE.Mesh(new THREE.BoxGeometry(15.5, 0.36, 12.2), M.stoneLight);
    dilacTerrace.position.y = 0.18;
    dilacTerrace.receiveShadow = true;
    this.dilacGroup.add(dilacTerrace);

    const dilacSign = new THREE.Mesh(
      new THREE.BoxGeometry(5.2, 0.92, 0.16),
      new THREE.MeshStandardMaterial({
        map: makeTextTex('南無彌勒尊佛 · ĐẠI TƯỢNG PHẬT DI LẶC', { w: 1024, h: 200, size: 54 })
      })
    );
    dilacSign.position.set(0, 0.95, 6.2);
    this.dilacGroup.add(dilacSign);
    this.exteriorGroup.add(this.dilacGroup);
    this.addRectObstacle(-31.5, -17.5, -8.5, 2.5);

    // 3. Đại Tượng Phật Niết Bàn (Total GLB length 28.0m — already includes its sculpted pedestal!)
    this.nietBanGroup = new THREE.Group();
    this.nietBanGroup.position.set(12, 0, -47);
    const nbTerrace = new THREE.Mesh(new THREE.BoxGeometry(29.5, 0.36, 11.2), M.stoneLight);
    nbTerrace.position.y = 0.18;
    nbTerrace.receiveShadow = true;
    this.nietBanGroup.add(nbTerrace);

    const nbSign = new THREE.Mesh(
      new THREE.BoxGeometry(7.2, 0.9, 0.16),
      new THREE.MeshStandardMaterial({
        map: makeTextTex('ĐẠI TƯỢNG PHẬT THÍCH CA NHẬP NIẾT BÀN (32M)', { w: 1024, h: 180, size: 44 })
      })
    );
    nbSign.position.set(0, 0.95, 5.7);
    this.nietBanGroup.add(nbSign);
    this.exteriorGroup.add(this.nietBanGroup);
    this.addRectObstacle(-2.0, 26.0, -52.0, -42.0);

    // 4. Đài Quan Âm Nam Hải (West Lotus Garden at (-26, 0, 14))
    this.quanAmGroup = new THREE.Group();
    this.quanAmGroup.position.set(-26, 0, 14);
    const qaPool = new THREE.Mesh(new THREE.CylinderGeometry(3.8, 4.1, 0.55, 16), M.stoneLight);
    qaPool.position.y = 0.275;
    this.quanAmGroup.add(qaPool);
    const qaWater = new THREE.Mesh(new THREE.CylinderGeometry(3.4, 3.4, 0.48, 16), M.pondWater);
    qaWater.position.y = 0.3;
    this.quanAmGroup.add(qaWater);
    this.exteriorGroup.add(this.quanAmGroup);
    this.addObstacle(-26, 14, 3.9);
  }

  makeLotusFlower3D(isWhite = false) {
    const g = new THREE.Group();
    const petalMat = isWhite
      ? this.MAT.statueWhite
      : new THREE.MeshStandardMaterial({ color: 0xF57CA8, roughness: 0.45 });
    const centerMat = new THREE.MeshStandardMaterial({ color: 0xF4C430, roughness: 0.5 });
    const center = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.05, 0.09, 10), centerMat);
    center.position.y = 0.06;
    g.add(center);
    for (let i = 0; i < 8; i++) {
      const a = (i / 8) * Math.PI * 2;
      const p = new THREE.Mesh(new THREE.ConeGeometry(0.07, 0.22, 6), petalMat);
      p.position.set(Math.cos(a) * 0.11, 0.08, Math.sin(a) * 0.11);
      p.rotation.z = -Math.cos(a) * 0.55;
      p.rotation.x = Math.sin(a) * 0.55;
      g.add(p);
    }
    return g;
  }

  buildLotusPond(w, d, koiCount = 12) {
    const M = this.MAT;
    const g = new THREE.Group();
    const wallH = 0.64;
    const rim = new THREE.Mesh(new THREE.BoxGeometry(w + 0.75, wallH, d + 0.75), M.stoneLight);
    rim.position.y = wallH / 2;
    rim.receiveShadow = true;
    g.add(rim);

    const water = new THREE.Mesh(new THREE.BoxGeometry(w, wallH - 0.08, d), M.pondWater);
    water.position.y = (wallH - 0.08) / 2 + 0.05;
    g.add(water);

    const step = 1.6;
    for (let x = -w / 2; x <= w / 2; x += step) {
      for (const z of [-d / 2 - 0.2, d / 2 + 0.2]) {
        const post = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.58, 0.18), M.creamTrim);
        post.position.set(x, wallH + 0.29, z);
        g.add(post);
        const cap = new THREE.Mesh(new THREE.SphereGeometry(0.12, 8, 8), M.goldAccent);
        cap.position.set(x, wallH + 0.62, z);
        g.add(cap);
      }
    }

    for (let i = 0; i < 28; i++) {
      const lx = (Math.random() - 0.5) * (w - 2.0);
      const lz = (Math.random() - 0.5) * (d - 1.8);
      const pad = new THREE.Mesh(
        new THREE.CylinderGeometry(0.45, 0.45, 0.03, 14),
        M.lotusLeaf
      );
      pad.position.set(lx, wallH + 0.02, lz);
      g.add(pad);
      if (i % 2 === 0) {
        const fl = this.makeLotusFlower3D(i % 6 === 0);
        fl.position.set(lx, wallH + 0.04, lz);
        fl.scale.setScalar(1.25);
        g.add(fl);
      }
    }

    const koiColors = [0xFF5722, 0xFF9800, 0xFFF8E1, 0xE53935, 0xFFB300];
    for (let i = 0; i < koiCount; i++) {
      const fishGroup = new THREE.Group();
      const body = new THREE.Mesh(
        new THREE.ConeGeometry(0.12, 0.46, 8),
        new THREE.MeshStandardMaterial({ color: koiColors[i % koiColors.length], roughness: 0.25 })
      );
      body.rotation.x = Math.PI / 2;
      fishGroup.add(body);
      const tail = new THREE.Mesh(
        new THREE.ConeGeometry(0.09, 0.18, 4),
        new THREE.MeshStandardMaterial({ color: 0xFFF8E1, roughness: 0.3 })
      );
      tail.rotation.x = -Math.PI / 2;
      tail.position.z = -0.26;
      fishGroup.add(tail);
      g.add(fishGroup);
      this.koiList.push({
        mesh: fishGroup,
        tail,
        rx: (w * 0.38) * (0.4 + Math.random() * 0.55),
        rz: (d * 0.38) * (0.4 + Math.random() * 0.55),
        speed: 0.48 + Math.random() * 0.45,
        phase: Math.random() * Math.PI * 2,
        y: wallH - 0.01
      });
    }
    return g;
  }

  buildIncenseBurner(scale = 1) {
    const M = this.MAT;
    const g = new THREE.Group();
    const base = new THREE.Mesh(new THREE.CylinderGeometry(1.05, 1.22, 0.38, 12), M.stoneDark);
    base.position.y = 0.19;
    g.add(base);
    // 3 Bronze tripod legs
    for (let i = 0; i < 3; i++) {
      const a = (i / 3) * Math.PI * 2;
      const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.09, 0.55, 8), M.bronzeBurner);
      leg.position.set(Math.cos(a) * 0.55, 0.52, Math.sin(a) * 0.55);
      g.add(leg);
    }
    const body = new THREE.Mesh(new THREE.CylinderGeometry(0.82, 0.64, 0.96, 20), M.bronzeBurner);
    body.position.y = 1.02;
    body.castShadow = true;
    g.add(body);
    const rim = new THREE.Mesh(new THREE.TorusGeometry(0.83, 0.09, 10, 24), M.goldAccent);
    rim.rotation.x = Math.PI / 2;
    rim.position.y = 1.48;
    g.add(rim);
    // Dragon handles on left and right of burner
    for (const sx of [-0.92, 0.92]) {
      const ear = new THREE.Mesh(new THREE.TorusGeometry(0.22, 0.05, 8, 14), M.goldAccent);
      ear.position.set(sx, 1.22, 0);
      g.add(ear);
    }
    // Oil lamp on small ritual table beside main burner
    const lampStand = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.22, 0.95, 10), M.stoneDark);
    lampStand.position.set(1.28, 0.475, 0.35);
    g.add(lampStand);
    const oilFlame = new THREE.Mesh(
      new THREE.ConeGeometry(0.08, 0.22, 8),
      new THREE.MeshBasicMaterial({ color: 0xFF9800 })
    );
    oilFlame.position.set(1.28, 1.06, 0.35);
    g.add(oilFlame);

    const ash = new THREE.Mesh(
      new THREE.CylinderGeometry(0.74, 0.74, 0.1, 16),
      new THREE.MeshStandardMaterial({ color: 0xC9BD9F, roughness: 0.95 })
    );
    ash.position.y = 1.44;
    g.add(ash);
    g.scale.setScalar(scale);
    return g;
  }

  makeKneelingCushion() {
    const g = new THREE.Group();
    const mat = new THREE.MeshStandardMaterial({ color: 0x9E241C, roughness: 0.72 });
    const trim = this.MAT.goldAccent;
    const pad = new THREE.Mesh(new THREE.CylinderGeometry(0.46, 0.5, 0.14, 16), mat);
    pad.position.y = 0.07;
    pad.receiveShadow = true;
    g.add(pad);
    const ring = new THREE.Mesh(new THREE.TorusGeometry(0.46, 0.03, 8, 18), trim);
    ring.rotation.x = Math.PI / 2;
    ring.position.y = 0.13;
    g.add(ring);
    return g;
  }

  makeStoneLantern() {
    const M = this.MAT;
    const g = new THREE.Group();
    const base = new THREE.Mesh(new THREE.BoxGeometry(0.78, 0.35, 0.78), M.stoneDark);
    base.position.y = 0.175;
    g.add(base);
    const shaft = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.22, 1.25, 8), M.stoneLight);
    shaft.position.y = 0.95;
    shaft.castShadow = true;
    g.add(shaft);
    const lamp = new THREE.Mesh(new THREE.BoxGeometry(0.46, 0.42, 0.46), M.lanternGlow);
    lamp.position.y = 1.78;
    g.add(lamp);
    const roof = new THREE.Mesh(new THREE.ConeGeometry(0.58, 0.42, 4), M.stoneDark);
    roof.rotation.y = Math.PI / 4;
    roof.position.y = 2.18;
    g.add(roof);
    return g;
  }

  buildGardensTreesAndFlags() {
    const M = this.MAT;
    const bougCoords = [
      [16.2, 24.5],
      [16.2, 18.5],
      [29.8, 24.5],
      [29.8, 18.5],
      [15.0, 10.2],
      [31.0, 10.2],
      [-8.5, 22.0],
      [-19.5, 22.0]
    ];
    for (const [bx, bz] of bougCoords) {
      const pot = new THREE.Group();
      const pMesh = new THREE.Mesh(
        new THREE.CylinderGeometry(0.68, 0.46, 0.65, 14),
        M.terracottaPot
      );
      pMesh.position.y = 0.325;
      pMesh.castShadow = true;
      pot.add(pMesh);
      const st = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.15, 1.35, 8), M.trunk);
      st.position.y = 1.1;
      pot.add(st);
      for (const [ox, oy, oz, r] of [
        [0, 1.85, 0, 0.72],
        [-0.42, 1.65, 0.22, 0.55],
        [0.42, 1.7, -0.2, 0.55]
      ]) {
        const crown = new THREE.Mesh(new THREE.SphereGeometry(r, 10, 8), M.foliageMid);
        crown.position.set(ox, oy, oz);
        pot.add(crown);
        const fl = new THREE.Mesh(
          new THREE.SphereGeometry(r * 0.92, 10, 8),
          M.bougainvilleaPink
        );
        fl.position.set(ox, oy + 0.12, oz);
        pot.add(fl);
      }
      pot.position.set(bx, 0, bz);
      this.exteriorGroup.add(pot);
      this.addObstacle(bx, bz, 0.72);
    }

    for (const [sx, sz, rotY] of [
      [16.2, 21.5, Math.PI / 2],
      [16.2, 14.5, Math.PI / 2],
      [29.8, 21.5, -Math.PI / 2],
      [29.8, 14.5, -Math.PI / 2]
    ]) {
      const bench = new THREE.Group();
      const seat = new THREE.Mesh(new THREE.BoxGeometry(1.85, 0.12, 0.55), M.stoneLight);
      seat.position.y = 0.48;
      seat.castShadow = true;
      bench.add(seat);
      const back = new THREE.Mesh(new THREE.BoxGeometry(1.85, 0.45, 0.1), M.stoneLight);
      back.position.set(0, 0.72, -0.22);
      bench.add(back);
      for (const lx of [-0.72, 0.72]) {
        const leg = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.48, 0.48), M.stoneDark);
        leg.position.set(lx, 0.24, 0);
        bench.add(leg);
      }
      bench.position.set(sx, 0, sz);
      bench.rotation.y = rotY;
      this.exteriorGroup.add(bench);
    }

    const treePositions = [
      [-5, 33, 1.3],
      [-23, 35, 1.4],
      [-31, 14, 1.35],
      [-33, -16, 1.4],
      [-14, -26, 1.3],
      [44, 24, 1.3],
      [46, 8, 1.35],
      [48, -36, 1.4],
      [34, 34, 1.15]
    ];
    for (const [tx, tz, sc] of treePositions) {
      const tree = new THREE.Group();
      const tr = new THREE.Mesh(new THREE.CylinderGeometry(0.26, 0.42, 3.6, 10), M.trunk);
      tr.position.y = 1.8;
      tr.castShadow = true;
      tree.add(tr);
      for (const [cx, cy, cz, r] of [
        [0, 4.2, 0, 1.85],
        [-1.1, 3.6, 0.6, 1.35],
        [1.1, 3.7, -0.5, 1.35],
        [0, 5.2, 0, 1.4]
      ]) {
        const cr = new THREE.Mesh(new THREE.SphereGeometry(r, 12, 10), M.foliageLight);
        cr.position.set(cx, cy, cz);
        cr.castShadow = true;
        tree.add(cr);
      }
      tree.position.set(tx, 0, tz);
      tree.scale.setScalar(sc);
      this.exteriorGroup.add(tree);
      this.addObstacle(tx, tz, 0.8);
    }

    const flagSpans = [
      [10, 5.8, 38, 36, 5.8, 38, 14],
      [-22, 5.5, 32, -4, 5.5, 22, 12]
    ];
    const flagMat = new THREE.MeshBasicMaterial({ map: this.flagTex72, side: THREE.DoubleSide });
    for (const [x1, y1, z1, x2, y2, z2, n] of flagSpans) {
      for (let i = 1; i < n; i++) {
        const t = i / n;
        const fx = x1 + (x2 - x1) * t;
        const fz = z1 + (z2 - z1) * t;
        const fy = y1 + (y2 - y1) * t - Math.sin(t * Math.PI) * 0.65;
        const f = new THREE.Mesh(new THREE.PlaneGeometry(0.55, 0.38), flagMat);
        f.position.set(fx, fy, fz);
        this.exteriorGroup.add(f);
      }
    }
  }

  buildProceduralShopPavilion() {
    const M = this.MAT;
    const g = new THREE.Group();
    const base = new THREE.Mesh(
      new THREE.BoxGeometry(5.8, 0.26, 4.4),
      M.darkWood
    );
    base.position.y = 0.13;
    g.add(base);
    const counter = new THREE.Mesh(
      new THREE.BoxGeometry(4.9, 1.02, 1.35),
      new THREE.MeshStandardMaterial({ color: 0x8C5532, map: this.woodGrainTex, roughness: 0.58 })
    );
    counter.position.set(0, 0.72, 1.0);
    counter.castShadow = true;
    g.add(counter);
    for (const [px, pz] of [
      [-2.35, -1.65],
      [2.35, -1.65],
      [-2.35, 1.65],
      [2.35, 1.65]
    ]) {
      const col = new THREE.Mesh(new THREE.CylinderGeometry(0.15, 0.17, 3.1, 12), M.redColumn);
      col.position.set(px, 1.65, pz);
      col.castShadow = true;
      g.add(col);
    }
    const roof = new THREE.Mesh(new THREE.ConeGeometry(4.6, 1.5, 4), M.roofTile);
    roof.rotation.y = Math.PI / 4;
    roof.scale.set(1.15, 1, 0.88);
    roof.position.y = 3.72;
    roof.castShadow = true;
    g.add(roof);
    const sign = new THREE.Mesh(
      new THREE.BoxGeometry(3.6, 0.78, 0.15),
      new THREE.MeshStandardMaterial({
        map: makeTextTex('CỬA HÀNG LƯU NIỆM', { w: 1024, h: 220, size: 74 })
      })
    );
    sign.position.set(0, 2.9, 1.75);
    g.add(sign);
    this.proceduralShopGroup = g;
    this.shopKioskAnchor.add(g);
  }

  buildCourtyardPigeons() {
    const bodyMat = new THREE.MeshStandardMaterial({ color: 0xDCE0E6, roughness: 0.55 });
    const wingMat = new THREE.MeshStandardMaterial({ color: 0x9BA4B0, roughness: 0.6 });
    const spots = [
      [20.2, 23.5],
      [21.0, 24.1],
      [25.5, 19.2],
      [26.1, 18.7],
      [19.4, 14.2],
      [22.4, 25.0],
      [24.0, 24.6],
      [18.2, 19.5]
    ];
    for (const [px, pz] of spots) {
      const bird = new THREE.Group();
      const b = new THREE.Mesh(new THREE.SphereGeometry(0.14, 8, 8), bodyMat);
      b.scale.set(1, 0.8, 1.45);
      b.position.y = 0.14;
      bird.add(b);
      const h = new THREE.Mesh(new THREE.SphereGeometry(0.08, 8, 8), bodyMat);
      h.position.set(0, 0.24, 0.14);
      bird.add(h);
      const wL = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.03, 0.16), wingMat);
      wL.position.set(-0.12, 0.16, 0);
      bird.add(wL);
      const wR = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.03, 0.16), wingMat);
      wR.position.set(0.12, 0.16, 0);
      bird.add(wR);
      bird.position.set(px, 0, pz);
      this.exteriorGroup.add(bird);
      this.pigeons.push({
        group: bird,
        wL,
        wR,
        baseX: px,
        baseZ: pz,
        phase: Math.random() * 6.28,
        flying: false,
        flyTimer: 0
      });
    }
  }

  buildInteriorChanhDienV8() {
    const M = this.MAT;
    const g = this.interiorGroup;

    const floor = new THREE.Mesh(
      new THREE.BoxGeometry(24, 0.2, 36),
      new THREE.MeshStandardMaterial({ map: this.pavingTex, color: 0xA87454, roughness: 0.48 })
    );
    floor.position.set(0, -0.1, -6);
    floor.receiveShadow = true;
    g.add(floor);

    const wallMat = new THREE.MeshStandardMaterial({
      color: 0x5A2E1B,
      map: this.woodGrainTex,
      roughness: 0.7
    });
    const backWall = new THREE.Mesh(new THREE.BoxGeometry(24, 8.8, 0.5), wallMat);
    backWall.position.set(0, 4.4, -23.5);
    g.add(backWall);
    for (const wx of [-11.6, 11.6]) {
      const sw = new THREE.Mesh(new THREE.BoxGeometry(0.5, 8.8, 36), wallMat);
      sw.position.set(wx, 4.4, -6);
      g.add(sw);
    }

    // Warm interior golden lighting
    const intPoint1 = new THREE.PointLight(0xFFD584, 1.4, 28);
    intPoint1.position.set(0, 6.8, -14);
    g.add(intPoint1);
    const intPoint2 = new THREE.PointLight(0xFFE0A3, 1.1, 24);
    intPoint2.position.set(0, 6.5, -2);
    g.add(intPoint2);

    for (let z = 6; z >= -20; z -= 5.2) {
      for (const x of [-4.8, 4.8]) {
        const col = new THREE.Mesh(new THREE.CylinderGeometry(0.34, 0.38, 8.5, 16), M.redColumn);
        col.position.set(x, 4.25, z);
        g.add(col);
        const ring = new THREE.Mesh(new THREE.CylinderGeometry(0.4, 0.4, 0.4, 16), M.goldAccent);
        ring.position.set(x, 6.8, z);
        g.add(ring);
        this.interiorObstacles.push({ x, z, r: 0.55 });
      }
    }

    // Hanging spiral incense coils (nhang khoanh treo trần) + red silk lanterns
    for (const [ix, iz] of [
      [-2.6, -4],
      [2.6, -4],
      [-2.6, -11],
      [2.6, -11]
    ]) {
      const coil = new THREE.Mesh(
        new THREE.ConeGeometry(0.55, 0.95, 16, 1, true),
        new THREE.MeshStandardMaterial({ color: 0xC8963E, side: THREE.DoubleSide, wireframe: true })
      );
      coil.position.set(ix, 6.4, iz);
      g.add(coil);
    }

    // Chuông Pháp Bảo (Great Bronze Bell inside Hall on right)
    const bellStand = new THREE.Group();
    bellStand.position.set(6.8, 0, -10.5);
    const bFrame = new THREE.Mesh(new THREE.BoxGeometry(1.8, 3.2, 0.8), M.darkWood);
    bFrame.position.y = 1.6;
    bellStand.add(bFrame);
    const bell = new THREE.Mesh(
      new THREE.CylinderGeometry(0.38, 0.62, 1.35, 18),
      M.bronzeBurner
    );
    bell.position.y = 1.85;
    bellStand.add(bell);
    g.add(bellStand);
    this.interiorObstacles.push({ x: 6.8, z: -10.5, r: 1.1 });

    this.tamBaoAltarGroup = new THREE.Group();
    this.tamBaoAltarGroup.position.set(0, 0, -18.7);
    const tier1 = new THREE.Mesh(new THREE.BoxGeometry(9.2, 1.4, 4.0), M.redColumn);
    tier1.position.y = 0.7;
    this.tamBaoAltarGroup.add(tier1);
    const tier2 = new THREE.Mesh(new THREE.BoxGeometry(6.8, 1.45, 2.9), M.goldAccent);
    tier2.position.y = 2.12;
    this.tamBaoAltarGroup.add(tier2);
    const plaque = new THREE.Mesh(
      new THREE.BoxGeometry(6.6, 1.15, 0.18),
      new THREE.MeshStandardMaterial({
        map: makeTextTex('ĐẠI HÙNG BẢO ĐIỆN', { w: 1024, h: 220, size: 78 })
      })
    );
    plaque.position.set(0, 6.7, 1.8);
    this.tamBaoAltarGroup.add(plaque);
    g.add(this.tamBaoAltarGroup);
    this.interiorRectObstacles.push({ minX: -5.0, maxX: 5.0, minZ: -21.5, maxZ: -16.0 });

    // 18 La Hán statues sculpted along the left and right walls
    this.arhatGroups = [];
    for (let i = 0; i < 9; i++) {
      const az = 4.5 - i * 2.85;
      for (const ax of [-9.8, 9.8]) {
        const ped = new THREE.Mesh(new THREE.BoxGeometry(1.25, 1.15, 1.25), M.redColumn);
        ped.position.set(ax, 0.575, az);
        g.add(ped);
        const trim = new THREE.Mesh(new THREE.BoxGeometry(1.32, 0.14, 1.32), M.goldAccent);
        trim.position.set(ax, 1.16, az);
        g.add(trim);
        const arhatGroup = new THREE.Group();
        arhatGroup.position.set(ax, 1.22, az);
        arhatGroup.rotation.y = ax < 0 ? Math.PI / 2 : -Math.PI / 2;
        // Sculpted golden wood Arhat figure on spirit mount
        const mount = new THREE.Mesh(
          new THREE.BoxGeometry(0.75, 0.42, 0.52),
          new THREE.MeshStandardMaterial({ color: 0x8C5828, roughness: 0.45, metalness: 0.25 })
        );
        mount.position.y = 0.21;
        arhatGroup.add(mount);
        const torso = new THREE.Mesh(
          new THREE.CylinderGeometry(0.22, 0.28, 0.78, 12),
          M.goldAccent
        );
        torso.position.y = 0.78;
        arhatGroup.add(torso);
        const head = new THREE.Mesh(new THREE.SphereGeometry(0.17, 12, 12), M.goldAccent);
        head.position.y = 1.32;
        arhatGroup.add(head);
        const halo = new THREE.Mesh(
          new THREE.RingGeometry(0.22, 0.28, 18),
          new THREE.MeshBasicMaterial({ color: 0xFFD875, side: THREE.DoubleSide })
        );
        halo.position.set(0, 1.34, -0.1);
        arhatGroup.add(halo);
        g.add(arhatGroup);
        this.arhatGroups.push(arhatGroup);
      }
    }
  }

  buildStationBeacons() {
    this.stationMarkers = [];
    for (const st of PILGRIMAGE_STATIONS) {
      const ring = new THREE.Mesh(
        new THREE.RingGeometry(0.65, 0.92, 32),
        new THREE.MeshBasicMaterial({
          color: 0xFFD166,
          side: THREE.DoubleSide,
          transparent: true,
          opacity: 0.82
        })
      );
      ring.rotation.x = -Math.PI / 2;
      const sx = st.standPos ? st.standPos.x : st.pos.x;
      const sz = st.standPos ? st.standPos.z : st.pos.z;
      ring.position.set(sx, 0.05, sz);
      this.exteriorGroup.add(ring);
      this.stationMarkers.push({ station: st, ring });
    }

    this.walkTargetRing = new THREE.Mesh(
      new THREE.RingGeometry(0.35, 0.58, 24),
      new THREE.MeshBasicMaterial({
        color: 0xFFE066,
        side: THREE.DoubleSide,
        transparent: true,
        opacity: 0.92
      })
    );
    this.walkTargetRing.rotation.x = -Math.PI / 2;
    this.walkTargetRing.visible = false;
    this.scene.add(this.walkTargetRing);
  }

  loadGLB(url) {
    return new Promise((resolve) => {
      this.gltfLoader.load(
        encodeURI(url),
        (gltf) => resolve(gltf),
        undefined,
        () => resolve(null)
      );
    });
  }

  cleanStatueScene(gltfScene, matOverride = null) {
    const root = gltfScene.clone(true);
    const toRemove = [];
    root.traverse((o) => {
      if (/ground|plane|floor|shadow/i.test(o.name || '')) {
        toRemove.push(o);
        return;
      }
      if (o.isMesh && o.geometry) {
        if (!o.geometry.getAttribute('normal')) {
          o.geometry.computeVertexNormals();
        }
        o.geometry.computeBoundingBox();
        const bb = o.geometry.boundingBox;
        if (bb && (bb.max.x - bb.min.x > 120 || bb.max.z - bb.min.z > 120)) {
          toRemove.push(o);
          return;
        }
        o.castShadow = true;
        o.receiveShadow = true;
        if (matOverride) {
          o.material = matOverride;
        } else if (o.material) {
          o.material = o.material.clone();
          if (o.geometry.getAttribute('color')) {
            o.material.vertexColors = true;
          }
          // Preserve embedded FeatureShadow, lotus blue, pedestal, and gold plaque colors while adding stone bump
          const matName = (o.material.name || '').toLowerCase();
          if (/white|statue|body|robe|skin/i.test(matName) || !matName) {
            o.material.bumpMap = this.stoneBumpTex;
            o.material.bumpScale = 0.01;
          }
          o.material.roughness = Math.min(0.58, Math.max(0.28, o.material.roughness ?? 0.45));
        }
      }
    });
    for (const r of toRemove) {
      if (r.parent) r.parent.remove(r);
    }
    return root;
  }

  async loadAllGLBAssets() {
    const [adidaGltf, dilacGltf, phatNamGltf, banThoGltf] = await Promise.all([
      this.loadGLB(STATUE_GLB_PATHS.adida),
      this.loadGLB(STATUE_GLB_PATHS.dilac),
      this.loadGLB(STATUE_GLB_PATHS.phatnam),
      this.loadGLB(STATUE_GLB_PATHS.bantho)
    ]);

    // 1. Đại Tượng Phật A Di Đà (Monumental 15.6m height facing -Z toward the player at z = 14.8)
    if (adidaGltf?.scene) {
      const s = this.cleanStatueScene(adidaGltf.scene, null);
      const box = new THREE.Box3().setFromObject(s);
      const h = Math.max(0.1, box.max.y - box.min.y);
      const scale = 15.6 / h;
      s.scale.setScalar(scale);
      const box2 = new THREE.Box3().setFromObject(s);
      s.position.set(
        -(box2.min.x + box2.max.x) / 2,
        0.32 - box2.min.y,
        -(box2.min.z + box2.max.z) / 2
      );
      s.rotation.y = Math.PI;
      this.adidaGroup.add(s);

      // Also place serene Quan Thế Âm statue (7.8m) in the West Lotus Garden
      if (this.quanAmGroup) {
        const qa = this.cleanStatueScene(adidaGltf.scene, null);
        qa.scale.setScalar(7.8 / h);
        const qaBox = new THREE.Box3().setFromObject(qa);
        qa.position.set(
          -(qaBox.min.x + qaBox.max.x) / 2,
          0.45 - qaBox.min.y,
          -(qaBox.min.z + qaBox.max.z) / 2
        );
        qa.rotation.y = 0.48;
        this.quanAmGroup.add(qa);
      }
    }

    // 2. Đại Tượng Phật Di Lặc (Monumental 12.6m height facing +Z toward the player at z = 9.8)
    if (dilacGltf?.scene) {
      const s = this.cleanStatueScene(dilacGltf.scene, null);
      const box = new THREE.Box3().setFromObject(s);
      const h = Math.max(0.1, box.max.y - box.min.y);
      const scale = 12.6 / h;
      s.scale.setScalar(scale);
      const box2 = new THREE.Box3().setFromObject(s);
      s.position.set(
        -(box2.min.x + box2.max.x) / 2,
        0.32 - box2.min.y,
        -(box2.min.z + box2.max.z) / 2
      );
      s.rotation.y = 0;
      this.dilacGroup.add(s);
    }

    // 3. Đại Tượng Phật Niết Bàn (Monumental 28.0m length, original sculpted details preserved!)
    if (phatNamGltf?.scene) {
      const s = this.cleanStatueScene(phatNamGltf.scene, null);
      const box = new THREE.Box3().setFromObject(s);
      const w = Math.max(0.1, box.max.x - box.min.x, box.max.z - box.min.z);
      const scale = 28.0 / w;
      s.scale.setScalar(scale);
      const box2 = new THREE.Box3().setFromObject(s);
      s.position.set(
        -(box2.min.x + box2.max.x) / 2,
        0.32 - box2.min.y,
        -(box2.min.z + box2.max.z) / 2
      );
      this.nietBanGroup.add(s);
    }

    // 4. Tượng Phật Bàn Thờ Tam Bảo (4.6m tall on main altar + visible through exterior doorway!)
    if (banThoGltf?.scene) {
      const s = this.cleanStatueScene(banThoGltf.scene, null);
      const box = new THREE.Box3().setFromObject(s);
      const h = Math.max(0.1, box.max.y - box.min.y);
      const scale = 4.6 / h;
      s.scale.setScalar(scale);
      const box2 = new THREE.Box3().setFromObject(s);
      s.position.set(
        -(box2.min.x + box2.max.x) / 2,
        2.82 - box2.min.y,
        -(box2.min.z + box2.max.z) / 2
      );
      this.tamBaoAltarGroup.add(s);
    }

    const initialKey = this.playerState.charKey || 'nu';
    const [initialCharGltf, denLongGltf, chumSenGltf, mamNguQuaGltf, moGoGltf, banThoPropGltf] =
      await Promise.all([
        this.loadGLB(CHAR_GLB_PATHS[initialKey]),
        this.loadGLB(PROP_GLB_PATHS.den_long),
        this.loadGLB(PROP_GLB_PATHS.chum_sen),
        this.loadGLB(PROP_GLB_PATHS.mam_ngu_qua),
        this.loadGLB(PROP_GLB_PATHS.mo_go),
        this.loadGLB(PROP_GLB_PATHS.ban_tho)
      ]);

    if (initialCharGltf?.scene) {
      this.charDataCache[initialKey] = initialCharGltf;
    }
    if (denLongGltf?.scene) this.propMeshCache.den_long = denLongGltf.scene;
    if (chumSenGltf?.scene) this.propMeshCache.chum_sen = chumSenGltf.scene;
    if (mamNguQuaGltf?.scene) this.propMeshCache.mam_ngu_qua = mamNguQuaGltf.scene;
    if (moGoGltf?.scene) this.propMeshCache.mo_go = moGoGltf.scene;
    if (banThoPropGltf?.scene) this.propMeshCache.ban_tho = banThoPropGltf.scene;

    this.placeLoaded3DPropsInWorld();
    this.setCharacter(initialKey);
    this.spawnMonksAndPilgrimsV8();
    this.initSmokeColumns();
    this.onLoaded();

    // Load remaining alternate character GLBs in background for instant character switching
    for (const key of ['nu', 'nam', 'tre_em']) {
      if (key === initialKey) continue;
      this.loadGLB(CHAR_GLB_PATHS[key]).then((gltf) => {
        if (gltf?.scene) this.charDataCache[key] = gltf;
      });
    }
  }

  placeLoaded3DPropsInWorld() {
    const fitProp = (sceneObj, targetSize) => {
      const clone = sceneObj.clone(true);
      clone.traverse((o) => {
        if (o.isMesh) {
          o.castShadow = true;
          o.receiveShadow = true;
          if (o.geometry && !o.geometry.getAttribute('normal')) {
            o.geometry.computeVertexNormals();
          }
        }
      });
      const box = new THREE.Box3().setFromObject(clone);
      const sz = new THREE.Vector3();
      box.getSize(sz);
      const maxDim = Math.max(0.05, sz.x, sz.y, sz.z);
      clone.scale.setScalar(targetSize / maxDim);
      const box2 = new THREE.Box3().setFromObject(clone);
      clone.position.y = -box2.min.y;
      return clone;
    };

    // Place hexagonal lanterns at Chánh Điện porch & Shop Pavilion
    if (this.propMeshCache.den_long) {
      for (const lx of [19.8, 26.2]) {
        const l = fitProp(this.propMeshCache.den_long, 0.85);
        l.position.set(lx, 4.8, 6.6);
        this.exteriorGroup.add(l);
      }
      if (this.proceduralShopGroup) {
        for (const sx of [-1.85, 1.85]) {
          const l = fitProp(this.propMeshCache.den_long, 0.68);
          l.position.set(sx, 2.35, 1.65);
          this.proceduralShopGroup.add(l);
        }
      }
    }

    // Place lotus urns (chum_sanh_hoa_sen) beside Chánh Điện stairs & Shop Pavilion
    if (this.propMeshCache.chum_sen) {
      for (const ux of [17.8, 28.2]) {
        const urn = fitProp(this.propMeshCache.chum_sen, 1.15);
        urn.position.set(ux, 0, 8.8);
        this.exteriorGroup.add(urn);
      }
      if (this.proceduralShopGroup) {
        const urn = fitProp(this.propMeshCache.chum_sen, 1.1);
        urn.position.set(2.85, 0, 1.5);
        this.proceduralShopGroup.add(urn);
      }
    }

    // Place five-fruit tray (mam_ngu_qua), wooden fish (mo_go), and incense bowl (ban_tho) on Tam Bảo Altar & Shop counter
    if (this.propMeshCache.mam_ngu_qua && this.tamBaoAltarGroup) {
      const tray = fitProp(this.propMeshCache.mam_ngu_qua, 0.78);
      tray.position.set(-1.4, 1.4, 1.2);
      this.tamBaoAltarGroup.add(tray);
    }
    if (this.propMeshCache.mo_go && this.tamBaoAltarGroup) {
      const mogo = fitProp(this.propMeshCache.mo_go, 0.62);
      mogo.position.set(1.4, 1.4, 1.2);
      this.tamBaoAltarGroup.add(mogo);
    }
    if (this.propMeshCache.ban_tho && this.tamBaoAltarGroup) {
      const bowl = fitProp(this.propMeshCache.ban_tho, 0.75);
      bowl.position.set(0, 1.4, 1.35);
      this.tamBaoAltarGroup.add(bowl);
    }
  }

  initSmokeColumns() {
    const origins = [
      new THREE.Vector3(23, 1.55, 11),
      new THREE.Vector3(-14, 1.15, 22.2),
      new THREE.Vector3(-24.5, 1.2, 3.8)
    ];
    for (const orig of origins) {
      const sc = new SmokeColumn(orig, 42, 0.26, 3.4);
      this.exteriorGroup.add(sc.points);
      this.smokeColumns.push(sc);
    }
  }

  // Exact vertex-color monk robe & orange diagonal sash from module_5.js
  recolorMonkRobe(model, tone = 0) {
    const robePalette = [
      [0.46, 0.45, 0.43],
      [0.54, 0.48, 0.4],
      [0.42, 0.36, 0.3]
    ];
    const robe = robePalette[tone % robePalette.length];
    const sash = [0.9, 0.48, 0.14];
    model.traverse((o) => {
      if (!o.isMesh || !o.geometry) return;
      const col = o.geometry.getAttribute('color');
      const pos = o.geometry.getAttribute('position');
      if (!col || !pos) return;
      o.geometry = o.geometry.clone();
      const c = o.geometry.getAttribute('color');
      const p = o.geometry.getAttribute('position');
      o.geometry.computeBoundingBox();
      const bb = o.geometry.boundingBox;
      const yMin = bb.min.y;
      const ySpan = Math.max(0.001, bb.max.y - yMin);
      const xSpan = Math.max(0.001, bb.max.x - bb.min.x);
      for (let i = 0; i < c.count; i++) {
        const r = c.getX(i);
        const g = c.getY(i);
        const b = c.getZ(i);
        const maxC = Math.max(r, g, b);
        const minC = Math.min(r, g, b);
        const sat = maxC > 0 ? (maxC - minC) / maxC : 0;
        const isSkin = r > g && g > b && r - b > 0.12 && r > 0.42;
        const ny = (p.getY(i) - yMin) / ySpan;
        if (ny > 0.85 && maxC < 0.25) {
          c.setXYZ(i, 0.72, 0.58, 0.46);
          continue;
        }
        if (!isSkin && sat < 0.32 && maxC > 0.18 && maxC < 0.92 && ny > 0.12 && ny < 0.86) {
          const nx = (p.getX(i) - bb.min.x) / xSpan;
          const diag = nx * 0.85 + (ny - 0.42);
          const onSash = ny > 0.46 && ny < 0.83 && diag > 0.58 && diag < 0.88;
          const shade = 0.75 + 0.35 * maxC;
          if (onSash) {
            c.setXYZ(
              i,
              Math.min(1, sash[0] * shade),
              Math.min(1, sash[1] * shade),
              Math.min(1, sash[2] * shade)
            );
          } else {
            c.setXYZ(
              i,
              Math.min(1, robe[0] * shade),
              Math.min(1, robe[1] * shade),
              Math.min(1, robe[2] * shade)
            );
          }
        }
      }
      c.needsUpdate = true;
    });
  }

  recolorPastelDress(model, rgb) {
    model.traverse((o) => {
      if (!o.isMesh || !o.geometry) return;
      const col = o.geometry.getAttribute('color');
      const pos = o.geometry.getAttribute('position');
      if (!col || !pos) return;
      o.geometry = o.geometry.clone();
      const c = o.geometry.getAttribute('color');
      const p = o.geometry.getAttribute('position');
      o.geometry.computeBoundingBox();
      const bb = o.geometry.boundingBox;
      const yMin = bb.min.y;
      const ySpan = Math.max(0.001, bb.max.y - yMin);
      for (let i = 0; i < c.count; i++) {
        const r = c.getX(i);
        const g = c.getY(i);
        const b = c.getZ(i);
        const maxC = Math.max(r, g, b);
        const minC = Math.min(r, g, b);
        const sat = maxC > 0 ? (maxC - minC) / maxC : 0;
        const isSkin = r > g && g > b && r - b > 0.12 && r > 0.42;
        const ny = (p.getY(i) - yMin) / ySpan;
        if (!isSkin && sat < 0.28 && maxC > 0.22 && maxC < 0.9 && ny > 0.18 && ny < 0.84) {
          const shade = 0.72 + 0.38 * maxC;
          c.setXYZ(
            i,
            Math.min(1, rgb[0] * shade),
            Math.min(1, rgb[1] * shade),
            Math.min(1, rgb[2] * shade)
          );
        }
      }
      c.needsUpdate = true;
    });
  }

  attachConicalHat(record, heightMeters = 1.62) {
    if (!record?.root) return;
    const hatMat = new THREE.MeshStandardMaterial({
      color: 0xDFC99B,
      roughness: 0.75,
      side: THREE.DoubleSide
    });
    const cone = new THREE.Mesh(new THREE.ConeGeometry(0.24, 0.16, 20, 1, true), hatMat);
    cone.castShadow = true;
    let headBone = null;
    record.root.traverse((b) => {
      if (b.isBone && b.name === 'Head') headBone = b;
    });
    if (headBone) {
      const s = record.root.scale.x || 1;
      cone.scale.setScalar(1 / s);
      cone.position.set(0, 0.14 / s, 0);
      cone.rotation.x = -0.08;
      headBone.add(cone);
    } else {
      cone.position.set(0, heightMeters * 1.02, 0);
      record.root.add(cone);
    }
  }

  cloneAnimatedCharacter(charKey, targetHeight) {
    const gltf = this.charDataCache[charKey];
    if (!gltf?.scene) return null;
    const cloned = SkeletonUtils.clone(gltf.scene);
    let geomBox = null;
    cloned.traverse((o) => {
      if (o.isMesh || o.isSkinnedMesh) {
        o.castShadow = true;
        o.receiveShadow = true;
        o.frustumCulled = false;
        if (o.geometry) {
          if (!o.geometry.getAttribute('normal')) {
            o.geometry.computeVertexNormals();
          }
          o.geometry.computeBoundingBox();
          if (o.isSkinnedMesh && o.geometry.boundingBox) {
            geomBox = o.geometry.boundingBox;
          }
        }
        if (o.material) {
          o.material = o.material.clone();
          if (o.geometry && o.geometry.getAttribute('color')) {
            o.material.vertexColors = true;
          }
          o.material.metalness = 0.0;
          o.material.roughness = 0.88;
        }
      }
    });
    if (!geomBox) {
      geomBox = new THREE.Box3().setFromObject(cloned);
    }
    const rawH = Math.max(0.2, geomBox.max.y - geomBox.min.y);
    const scale = targetHeight / rawH;
    cloned.scale.setScalar(scale);
    cloned.position.y = -geomBox.min.y * scale;

    const mixer = new THREE.AnimationMixer(cloned);
    const actions = {};
    for (const clip of gltf.animations || []) {
      const cleanName = clip.name.replace(/_world$/, '');
      const act = mixer.clipAction(clip);
      actions[cleanName] = act;
      actions[clip.name] = act;
    }
    if (actions['Di bo'] && !actions['Đi bộ']) actions['Đi bộ'] = actions['Di bo'];
    if (actions['Đi bộ'] && !actions['Di bo']) actions['Di bo'] = actions['Đi bộ'];

    return {
      root: cloned,
      mixer,
      actions,
      activeAction: null,
      activeClipName: '',
      baseY: cloned.position.y
    };
  }

  playClipCrossfade(record, clipName, fadeDuration = 0.22, loopOnce = false) {
    if (!record || !record.actions) return;
    const target =
      record.actions[clipName] ||
      (clipName === 'Đi bộ' ? record.actions['Di bo'] : null) ||
      (clipName === 'Di bo' ? record.actions['Đi bộ'] : null) ||
      record.actions['Dung'] ||
      Object.values(record.actions)[0];
    if (!target) return;
    if (record.activeAction === target && !loopOnce) {
      target.paused = false;
      return;
    }

    if (record.activeAction && record.activeAction !== target) {
      record.activeAction.fadeOut(fadeDuration);
    }
    target.reset();
    target.paused = false;
    target.setLoop(loopOnce ? THREE.LoopOnce : THREE.LoopRepeat, loopOnce ? 1 : Infinity);
    target.clampWhenFinished = loopOnce;
    target.fadeIn(fadeDuration).play();
    record.activeAction = target;
    record.activeClipName = clipName;
  }

  setCharacter(charKey = 'nu') {
    if (!['nu', 'nam', 'tre_em'].includes(charKey)) charKey = 'nu';
    this.playerState.charKey = charKey;
    while (this.playerContainer.children.length > 0) {
      this.playerContainer.remove(this.playerContainer.children[0]);
    }
    const h = CHAR_HEIGHTS[charKey] || 1.62;
    const rec = this.cloneAnimatedCharacter(charKey, h);
    if (!rec) return;
    this.activePlayerRecord = rec;
    this.playerContainer.add(rec.root);

    // Add soft contact shadow under protagonist
    const shadow = new THREE.Mesh(
      new THREE.CircleGeometry(0.36, 20),
      new THREE.MeshBasicMaterial({ color: 0x1A140E, transparent: true, opacity: 0.26 })
    );
    shadow.rotation.x = -Math.PI / 2;
    shadow.position.y = 0.015;
    this.playerContainer.add(shadow);

    // Default cream shoulder tote bag for female protagonist on left shoulder when viewed from behind (matching Reference Image 1)
    if (charKey === 'nu') {
      const bagGroup = new THREE.Group();
      const bagMat = new THREE.MeshStandardMaterial({ color: 0xF3E6CE, roughness: 0.78 });
      const pouch = new THREE.Mesh(new THREE.BoxGeometry(0.11, 0.24, 0.22), bagMat);
      pouch.position.set(0.21, h * 0.54, -0.03);
      pouch.rotation.z = -0.12;
      bagGroup.add(pouch);
      const strap = new THREE.Mesh(
        new THREE.TorusGeometry(0.14, 0.016, 8, 16, Math.PI),
        bagMat
      );
      strap.position.set(0.18, h * 0.67, -0.02);
      strap.rotation.y = Math.PI / 2;
      bagGroup.add(strap);
      this.playerContainer.add(bagGroup);
    }

    this.equipmentGroup = new THREE.Group();
    this.playerContainer.add(this.equipmentGroup);

    // Start in natural mid-stride walking posture (arms relaxed at sides, not T/A-pose)
    this.playClipCrossfade(rec, 'Di bo', 0.05);
    if (rec.activeAction) {
      rec.mixer.setTime(0.28);
      rec.mixer.update(0);
      rec.activeAction.paused = true;
    }

    this.syncPlayerTransform();
    if (this.lastEquippedState) {
      this.updateEquippedItems(this.lastEquippedState);
    }
  }

  makeArticulatedFigure({
    height = 1.65,
    robeHex = 0x7A746E,
    sashHex = null,
    hairType = 'bun',
    hat = false,
    kneeling = false
  }) {
    const root = new THREE.Group();
    const s = height / 1.65;

    const skinMat = new THREE.MeshStandardMaterial({ color: 0xF2C8A6, roughness: 0.75 });
    const robeMat = new THREE.MeshStandardMaterial({ color: robeHex, roughness: 0.82 });
    const pantsMat = new THREE.MeshStandardMaterial({ color: 0x4A443F, roughness: 0.85 });
    const hairMat = new THREE.MeshStandardMaterial({ color: 0x221B18, roughness: 0.8 });

    // Soft ground contact shadow disc
    const shadowDisc = new THREE.Mesh(
      new THREE.CircleGeometry(0.36 * s, 16),
      new THREE.MeshBasicMaterial({ color: 0x1A140E, transparent: true, opacity: 0.28 })
    );
    shadowDisc.rotation.x = -Math.PI / 2;
    shadowDisc.position.y = 0.015;
    root.add(shadowDisc);

    const bodyGroup = new THREE.Group();
    root.add(bodyGroup);

    // Legs
    const legL = new THREE.Mesh(new THREE.CylinderGeometry(0.085 * s, 0.075 * s, 0.62 * s, 10), pantsMat);
    const legR = new THREE.Mesh(new THREE.CylinderGeometry(0.085 * s, 0.075 * s, 0.62 * s, 10), pantsMat);
    if (kneeling) {
      legL.scale.y = 0.45;
      legR.scale.y = 0.45;
      legL.position.set(-0.11 * s, 0.16 * s, 0.06 * s);
      legR.position.set(0.11 * s, 0.16 * s, 0.06 * s);
      bodyGroup.position.y = -0.28 * s;
    } else {
      legL.position.set(-0.11 * s, 0.31 * s, 0);
      legR.position.set(0.11 * s, 0.31 * s, 0);
    }
    root.add(legL, legR);

    // Robe / Torso
    const torso = new THREE.Mesh(
      new THREE.CylinderGeometry(0.18 * s, 0.24 * s, 0.68 * s, 14),
      robeMat
    );
    torso.position.y = 0.88 * s;
    bodyGroup.add(torso);

    // Optional Monk Diagonal Saffron Sash (Huỳnh Y / Dải Cam)
    if (sashHex !== null) {
      const sashMat = new THREE.MeshStandardMaterial({ color: sashHex, roughness: 0.7 });
      const sash = new THREE.Mesh(
        new THREE.TorusGeometry(0.205 * s, 0.048 * s, 8, 18),
        sashMat
      );
      sash.position.set(0, 0.94 * s, 0);
      sash.rotation.set(Math.PI / 2.6, 0.42, 0);
      bodyGroup.add(sash);
    }

    // Arms (articulated for walking or Chắp tay prayer)
    const armL = new THREE.Mesh(
      new THREE.CylinderGeometry(0.058 * s, 0.05 * s, 0.48 * s, 10),
      robeMat
    );
    const armR = new THREE.Mesh(
      new THREE.CylinderGeometry(0.058 * s, 0.05 * s, 0.48 * s, 10),
      robeMat
    );
    armL.position.set(-0.23 * s, 0.92 * s, 0.06 * s);
    armR.position.set(0.23 * s, 0.92 * s, 0.06 * s);
    bodyGroup.add(armL, armR);

    // Head
    const head = new THREE.Mesh(new THREE.SphereGeometry(0.145 * s, 14, 12), skinMat);
    head.position.y = 1.38 * s;
    bodyGroup.add(head);

    if (hairType === 'tuft') {
      // Chú tiểu An top-knot tuft
      const tuft = new THREE.Mesh(new THREE.SphereGeometry(0.055 * s, 10, 8), hairMat);
      tuft.position.set(0, 1.53 * s, 0.02 * s);
      bodyGroup.add(tuft);
    } else if (hairType === 'bun') {
      const cap = new THREE.Mesh(
        new THREE.SphereGeometry(0.15 * s, 12, 10, 0, Math.PI * 2, 0, Math.PI * 0.58),
        hairMat
      );
      cap.position.y = 1.39 * s;
      bodyGroup.add(cap);
      const bun = new THREE.Mesh(new THREE.SphereGeometry(0.065 * s, 10, 8), hairMat);
      bun.position.set(0, 1.36 * s, -0.14 * s);
      bodyGroup.add(bun);
    }

    if (hat) {
      const cone = new THREE.Mesh(
        new THREE.ConeGeometry(0.28 * s, 0.18 * s, 20),
        new THREE.MeshStandardMaterial({ color: 0xE6D3A7, roughness: 0.75 })
      );
      cone.position.set(0, 1.54 * s, 0);
      bodyGroup.add(cone);
    }

    return { root, legL, legR, armL, armR, bodyGroup, s };
  }

  animateArticulatedFigure(fig, elapsed, walking = false, speed = 1.0) {
    if (!fig) return;
    if (walking) {
      const swing = Math.sin(elapsed * 7.5 * speed) * 0.35;
      fig.legL.rotation.x = swing;
      fig.legR.rotation.x = -swing;
      fig.armL.rotation.x = -swing * 0.7;
      fig.armR.rotation.x = swing * 0.7;
      fig.armL.rotation.z = 0.08;
      fig.armR.rotation.z = -0.08;
    } else {
      // Chắp tay (Prayer pose)
      fig.legL.rotation.x = 0;
      fig.legR.rotation.x = 0;
      fig.armL.rotation.x = -0.65;
      fig.armR.rotation.x = -0.65;
      fig.armL.rotation.z = -0.35;
      fig.armR.rotation.z = 0.35;
    }
  }

  spawnMonksAndPilgrimsV8() {
    // 1. Spawn Chú tiểu An companion walking alongside the player
    if (!this.anCompanion) {
      const anFig = this.makeArticulatedFigure({
        height: 1.18,
        robeHex: 0x8A7B6A,
        sashHex: 0xE67E22,
        hairType: 'tuft'
      });
      anFig.root.position.set(this.playerState.x + 1.35, 0, this.playerState.z + 0.55);
      anFig.root.rotation.y = this.playerState.yaw;
      this.exteriorGroup.add(anFig.root);
      this.anCompanion = {
        fig: anFig,
        x: this.playerState.x + 1.35,
        z: this.playerState.z + 0.55,
        yaw: this.playerState.yaw,
        moving: false
      };
    }

    // 2. Kneeling worshippers on lotus cushions
    const kneelSpots = [
      { x: 21.6, z: 12.6, yaw: Math.PI, robeHex: 0xB89AA8, hairType: 'bun' },
      { x: 24.4, z: 12.6, yaw: Math.PI, robeHex: 0x7A746E, hairType: 'shaved' },
      { x: -14.0, z: 17.5, yaw: 0, robeHex: 0xC9B49C, hairType: 'bun' },
      { x: -24.5, z: 5.2, yaw: Math.PI, robeHex: 0x6E7B8B, hairType: 'shaved' }
    ];
    for (const ks of kneelSpots) {
      const fig = this.makeArticulatedFigure({
        height: 1.62,
        robeHex: ks.robeHex,
        hairType: ks.hairType,
        kneeling: true
      });
      this.animateArticulatedFigure(fig, 0, false);
      fig.root.position.set(ks.x, 0.12, ks.z);
      fig.root.rotation.y = ks.yaw;
      this.exteriorGroup.add(fig.root);
      this.kneelingRecords.push(fig);
    }

    // 3. Walking Monks & Pilgrims on courtyard routes
    const routes = [
      {
        height: 1.72,
        robeHex: 0x787570,
        sashHex: 0xE67E22,
        hairType: 'shaved',
        hat: false,
        pts: [
          [20.2, 32],
          [20.2, 13.5],
          [15.2, 13.5],
          [15.2, 32]
        ],
        speed: 1.1
      },
      {
        height: 1.7,
        robeHex: 0x8A7B68,
        sashHex: 0xE67E22,
        hairType: 'shaved',
        hat: false,
        pts: [
          [26.2, 14],
          [26.2, 31],
          [32.5, 31],
          [32.5, 14]
        ],
        speed: 1.02
      },
      {
        height: 1.62,
        robeHex: 0xD89CB2,
        sashHex: null,
        hairType: 'bun',
        hat: true,
        pts: [
          [-7, 23],
          [-16, 22],
          [-21, 6],
          [-9, 9]
        ],
        speed: 1.18
      },
      {
        height: 1.15,
        robeHex: 0x8CA6C2,
        sashHex: null,
        hairType: 'tuft',
        hat: false,
        pts: [
          [-6.2, 23.8],
          [-15.2, 22.8],
          [-20.2, 6.8],
          [-8.2, 9.8]
        ],
        speed: 1.18
      },
      {
        height: 1.62,
        robeHex: 0xA89EC4,
        sashHex: null,
        hairType: 'bun',
        hat: true,
        pts: [
          [34, 34],
          [24, 24],
          [24, 15],
          [35, 22]
        ],
        speed: 1.12
      }
    ];

    for (const rt of routes) {
      const fig = this.makeArticulatedFigure(rt);
      fig.root.position.set(rt.pts[0][0], 0, rt.pts[0][1]);
      this.exteriorGroup.add(fig.root);
      this.npcRecords.push({
        fig,
        pts: rt.pts,
        idx: 1,
        speed: rt.speed,
        pauseTimer: 0,
        yaw: 0
      });
    }
  }

  tryMove(nx, nz, radius = 0.42) {
    const curX = this.playerState.x;
    const curZ = this.playerState.z;
    const bounds = this.inInterior
      ? { minX: -9.8, maxX: 9.8, minZ: -15.5, maxZ: 7.5 }
      : WORLD_BOUNDS;
    let x = Math.max(bounds.minX, Math.min(bounds.maxX, nx));
    let z = Math.max(bounds.minZ, Math.min(bounds.maxZ, nz));

    const circles = this.inInterior ? this.interiorObstacles : this.obstacles;
    const rects = this.inInterior ? this.interiorRectObstacles : this.rectObstacles;

    for (const c of circles) {
      const dx = x - c.x;
      const dz = z - c.z;
      const dist = Math.hypot(dx, dz);
      const minD = c.r + radius;
      if (dist < minD) {
        const prevDist = Math.hypot(curX - c.x, curZ - c.z);
        if (prevDist < minD && dist > prevDist) {
          continue;
        }
        const nLen = dist || 0.001;
        x = c.x + (dx / nLen) * minD;
        z = c.z + (dz / nLen) * minD;
      }
    }

    for (const b of rects) {
      if (
        x > b.minX - radius &&
        x < b.maxX + radius &&
        z > b.minZ - radius &&
        z < b.maxZ + radius
      ) {
        const prevInside =
          curX > b.minX - radius &&
          curX < b.maxX + radius &&
          curZ > b.minZ - radius &&
          curZ < b.maxZ + radius;
        if (prevInside) continue;
        const canX = !(
          x > b.minX - radius &&
          x < b.maxX + radius &&
          curZ > b.minZ - radius &&
          curZ < b.maxZ + radius
        );
        const canZ = !(
          curX > b.minX - radius &&
          curX < b.maxX + radius &&
          z > b.minZ - radius &&
          z < b.maxZ + radius
        );
        if (canX) z = curZ;
        else if (canZ) x = curX;
        else {
          x = curX;
          z = curZ;
        }
      }
    }

    return { x, z };
  }

  lerpAngle(a, b, t) {
    let diff = ((b - a + Math.PI) % (Math.PI * 2)) - Math.PI;
    if (diff < -Math.PI) diff += Math.PI * 2;
    return a + diff * Math.min(1, t);
  }

  walkToStation(stationOrId, onArrival = null) {
    const st =
      typeof stationOrId === 'object'
        ? stationOrId
        : PILGRIMAGE_STATIONS.find((s) => s.id === Number(stationOrId) || s.key === stationOrId);
    if (!st) return;

    if (this.inInterior) {
      this.toggleInterior(false);
    }

    const pts = [];
    if (Array.isArray(st.via)) {
      for (const [vx, vz] of st.via) {
        if (Math.hypot(vx - this.playerState.x, vz - this.playerState.z) > 2.2) {
          pts.push({ x: vx, z: vz });
        }
      }
    }
    const tx = st.standPos ? st.standPos.x : st.pos.x;
    const tz = st.standPos ? st.standPos.z : st.pos.z;
    pts.push({ x: tx, z: tz, lookAt: st.lookAt });

    this.autoWalkWaypoints = pts;
    this.autoWalkCallback = onArrival;
    this.autoWalkStation = st;
    this.walkTargetRing.position.set(tx, 0.06, tz);
    this.walkTargetRing.visible = true;
    this.updateWalkPathLine();
    this.onAutoWalkTargetChange(st);
  }

  cancelAutoWalk() {
    if (this.autoWalkWaypoints.length > 0 || this.autoWalkStation) {
      this.autoWalkWaypoints = [];
      this.autoWalkCallback = null;
      this.autoWalkStation = null;
      if (this.walkTargetRing) this.walkTargetRing.visible = false;
      if (this.walkPathLine) this.walkPathLine.visible = false;
      this.onAutoWalkTargetChange(null);
    }
  }

  updateWalkPathLine() {
    if (this.walkPathLine) {
      this.scene.remove(this.walkPathLine);
      this.walkPathLine.geometry.dispose();
      this.walkPathLine = null;
    }
    if (!this.autoWalkWaypoints.length) return;
    const points = [new THREE.Vector3(this.playerState.x, 0.08, this.playerState.z)];
    for (const wp of this.autoWalkWaypoints) {
      points.push(new THREE.Vector3(wp.x, 0.08, wp.z));
    }
    const geom = new THREE.BufferGeometry().setFromPoints(points);
    const mat = new THREE.LineBasicMaterial({ color: 0xFFD166, transparent: true, opacity: 0.85 });
    this.walkPathLine = new THREE.Line(geom, mat);
    this.scene.add(this.walkPathLine);
  }

  moveStep(dx, dz, speed = 0.22) {
    if (dx !== 0 || dz !== 0) {
      this.cancelAutoWalk();
    }
    const len = Math.hypot(dx, dz);
    if (len < 0.001) {
      this.playerState.moving = false;
      return this.playerState;
    }
    const nx = dx / len;
    const nz = dz / len;
    const targetX = this.playerState.x + nx * speed;
    const targetZ = this.playerState.z + nz * speed;
    const moved = this.tryMove(targetX, targetZ);
    this.playerState.x = moved.x;
    this.playerState.z = moved.z;
    const targetYaw = Math.atan2(nx, nz);
    this.playerState.yaw = this.lerpAngle(this.playerState.yaw, targetYaw, 0.32);
    this.playerState.moving = true;
    clearTimeout(this._nudgeStopTimer);
    this._nudgeStopTimer = setTimeout(() => {
      if (this.heldDirs.size === 0 && this.autoWalkWaypoints.length === 0) {
        this.playerState.moving = false;
      }
    }, 360);
    this.syncPlayerTransform();
    this.checkStationProximity();
    return this.playerState;
  }

  updateHeldMovement(dt) {
    if (!this.heldDirs || this.heldDirs.size === 0) return;
    let ix = 0;
    let iz = 0;
    if (this.heldDirs.has('up')) iz -= 1;
    if (this.heldDirs.has('down')) iz += 1;
    if (this.heldDirs.has('left')) ix -= 1;
    if (this.heldDirs.has('right')) ix += 1;
    if (ix === 0 && iz === 0) return;

    const len = Math.hypot(ix, iz) || 1;
    ix /= len;
    iz /= len;

    const angle = this.cameraBaseYaw + this.cameraAzimuthOffset;
    const forwardX = Math.sin(angle);
    const forwardZ = Math.cos(angle);
    const rightX = -forwardZ;
    const rightZ = forwardX;

    const worldDx = forwardX * (-iz) + rightX * ix;
    const worldDz = forwardZ * (-iz) + rightZ * ix;
    const speed = 5.4 * dt;
    const moved = this.tryMove(
      this.playerState.x + worldDx * speed,
      this.playerState.z + worldDz * speed
    );
    this.playerState.x = moved.x;
    this.playerState.z = moved.z;
    this.playerState.yaw = this.lerpAngle(
      this.playerState.yaw,
      Math.atan2(worldDx, worldDz),
      Math.min(1, dt * 12)
    );
    this.playerState.moving = true;
    this.syncPlayerTransform();
    this.checkStationProximity();
  }

  stopMoving() {
    if (this.autoWalkWaypoints.length === 0 && this.heldDirs.size === 0) {
      this.playerState.moving = false;
    }
  }

  teleportToStation(stationId) {
    const st = PILGRIMAGE_STATIONS.find((s) => s.id === Number(stationId) || s.key === stationId);
    if (!st) return;
    this.cancelAutoWalk();
    if (this.inInterior) this.toggleInterior(false);
    const sx = st.standPos ? st.standPos.x : st.pos.x;
    const sz = st.standPos ? st.standPos.z : st.pos.z;
    this.playerState.x = sx;
    this.playerState.z = sz;
    if (st.lookAt) {
      this.playerState.yaw = Math.atan2(st.lookAt.x - sx, st.lookAt.z - sz);
      this.cameraBaseYaw = this.playerState.yaw;
      this.cameraAzimuthOffset = 0;
    }
    this.playerState.moving = false;
    this.currentStationId = st.id;
    this.syncPlayerTransform();
    this.onStationProximity(st, 0);
  }

  toggleInterior(enter) {
    this.inInterior = Boolean(enter ?? !this.inInterior);
    this.exteriorGroup.visible = !this.inInterior;
    this.interiorGroup.visible = this.inInterior;
    if (this.inInterior) {
      this.playerState.x = 0;
      this.playerState.z = 5.5;
      this.playerState.yaw = Math.PI;
    } else {
      this.playerState.x = 23;
      this.playerState.z = 7.5;
      this.playerState.yaw = Math.PI;
    }
    this.cameraBaseYaw = Math.PI;
    this.cameraAzimuthOffset = 0;
    this.syncPlayerTransform();
    return this.inInterior;
  }

  triggerActionAnimation(clipName = 'Vái') {
    const mapName = {
      Vai: 'Vái',
      Vái: 'Vái',
      'Chap tay': 'Chắp tay',
      'Chắp tay': 'Chắp tay',
      'Thap nhang': 'Thắp nhang',
      'Thắp nhang': 'Thắp nhang',
      Quy: 'Quỳ',
      Quỳ: 'Quỳ',
      'Di bo': 'Di bo',
      'Đi bộ': 'Di bo',
      Dung: 'Dung'
    };
    const resolved = mapName[clipName] || 'Vái';
    this.playerState.pose = resolved;
    if (this.activePlayerRecord) {
      this.playClipCrossfade(this.activePlayerRecord, resolved, 0.22, true);
      clearTimeout(this._poseReturnTimer);
      this._poseReturnTimer = setTimeout(() => {
        if (!this.playerState.moving && this.activePlayerRecord) {
          this.playerState.pose = 'Dung';
          this.playClipCrossfade(this.activePlayerRecord, 'Dung', 0.25, false);
        }
      }, 2800);
    }
  }

  addIncenseStickVisual() {
    const stick = new THREE.Group();
    const stem = new THREE.Mesh(
      new THREE.CylinderGeometry(0.012, 0.012, 0.45, 6),
      new THREE.MeshStandardMaterial({ color: 0xA8241C })
    );
    stem.position.y = 0.22;
    stick.add(stem);
    const tip = new THREE.Mesh(
      new THREE.SphereGeometry(0.022, 6, 6),
      new THREE.MeshBasicMaterial({ color: 0xFF5722 })
    );
    tip.position.y = 0.45;
    stick.add(tip);
    const count = this.incenseSticksGroup.children.length;
    stick.position.set(((count % 5) - 2) * 0.06, 0, Math.floor(count / 5) * 0.05);
    this.incenseSticksGroup.add(stick);
  }

  addLotusOfferingVisual() {
    const fl = this.makeLotusFlower3D(false);
    fl.scale.setScalar(1.4);
    const c = this.offeredLotusesGroup.children.length;
    fl.position.set((c % 6) * 0.34, 0, Math.floor(c / 6) * 0.34);
    this.offeredLotusesGroup.add(fl);
  }

  updateEquippedItems(equipped = {}) {
    this.lastEquippedState = equipped;
    if (!this.equipmentGroup) return;
    while (this.equipmentGroup.children.length > 0) {
      this.equipmentGroup.remove(this.equipmentGroup.children[0]);
    }
    const h = CHAR_HEIGHTS[this.playerState.charKey] || 1.64;
    if (equipped.hat && this.propMeshCache.non_la) {
      const hat = this.propMeshCache.non_la.clone(true);
      hat.scale.setScalar(0.38);
      hat.position.set(0, h + 0.02, 0);
      this.equipmentGroup.add(hat);
    }
    if (equipped.bag && this.propMeshCache.tui_sen) {
      const bag = this.propMeshCache.tui_sen.clone(true);
      bag.scale.setScalar(0.28);
      bag.position.set(-0.22, h * 0.56, 0.04);
      this.equipmentGroup.add(bag);
    }
    if (equipped.hand === 'hoa_sen_trang_nghiem' && this.propMeshCache.hoa_sen) {
      const lotus = this.propMeshCache.hoa_sen.clone(true);
      lotus.scale.setScalar(0.26);
      lotus.position.set(0.22, h * 0.62, 0.24);
      this.equipmentGroup.add(lotus);
    }
  }

  syncPlayerTransform() {
    this.playerContainer.position.set(this.playerState.x, 0, this.playerState.z);
    // Character GLBs face +Z in local coordinates, so rotation.y = yaw faces movement direction
    this.playerContainer.rotation.y = this.playerState.yaw;

    const isMonumental =
      !this.inInterior &&
      ([2, 3, 8].includes(this.currentStationId) ||
        Math.hypot(this.playerState.x - -14, this.playerState.z - 14.8) < 5.5 ||
        Math.hypot(this.playerState.x - -24.5, this.playerState.z - 9.8) < 5.5 ||
        Math.hypot(this.playerState.x - 12, this.playerState.z - -32) < 6.5);

    const camDist = this.inInterior ? 4.2 : isMonumental ? 9.4 : 7.0;
    const camHeight = this.inInterior ? 2.05 : isMonumental ? 2.4 : 2.05;
    const lookY = this.inInterior ? 2.45 : isMonumental ? 6.8 : 3.55;
    const lookAngle = this.cameraBaseYaw + this.cameraAzimuthOffset;
    // Slight right-shoulder offset so the protagonist stands slightly left of center as in Reference Image 1
    const sideOffset = this.inInterior ? 0 : 0.62;
    const cx =
      this.playerState.x - Math.sin(lookAngle) * camDist - Math.cos(lookAngle) * sideOffset;
    const cz =
      this.playerState.z - Math.cos(lookAngle) * camDist + Math.sin(lookAngle) * sideOffset;
    this.camera.position.set(cx, camHeight, cz);
    this.camera.lookAt(
      this.playerState.x + Math.sin(lookAngle) * 11,
      lookY,
      this.playerState.z + Math.cos(lookAngle) * 11
    );
  }

  checkStationProximity() {
    if (this.inInterior) return;
    let best = PILGRIMAGE_STATIONS[0];
    let bestDist = Infinity;
    for (const st of PILGRIMAGE_STATIONS) {
      const tx = st.standPos ? st.standPos.x : st.pos.x;
      const tz = st.standPos ? st.standPos.z : st.pos.z;
      const d = Math.hypot(this.playerState.x - tx, this.playerState.z - tz);
      if (d < bestDist) {
        bestDist = d;
        best = st;
      }
    }
    if (best.id !== this.currentStationId || bestDist < 4.5) {
      this.currentStationId = best.id;
      this.onStationProximity(best, bestDist);
    }
  }

  initPointerAndWheelControls() {
    let dragging = false;
    let downX = 0;
    let downY = 0;
    let movedDrag = false;

    this.canvas.addEventListener('pointerdown', (e) => {
      dragging = true;
      movedDrag = false;
      downX = e.clientX;
      downY = e.clientY;
    });

    window.addEventListener('pointermove', (e) => {
      if (!dragging) return;
      const dx = e.clientX - downX;
      const dy = e.clientY - downY;
      if (Math.hypot(dx, dy) > 6) {
        movedDrag = true;
        this.cameraAzimuthOffset -= dx * 0.0045;
        downX = e.clientX;
        downY = e.clientY;
        this.syncPlayerTransform();
      }
    });

    window.addEventListener('pointerup', (e) => {
      if (!dragging) return;
      dragging = false;
      if (!movedDrag && e.target === this.canvas) {
        this.handleCanvasTapToWalk(e);
      }
    });
  }

  handleCanvasTapToWalk(e) {
    const rect = this.canvas.getBoundingClientRect();
    const ndc = new THREE.Vector2(
      ((e.clientX - rect.left) / rect.width) * 2 - 1,
      -((e.clientY - rect.top) / rect.height) * 2 + 1
    );
    const raycaster = new THREE.Raycaster();
    raycaster.setFromCamera(ndc, this.camera);

    // If inside interior hall and user clicks an Arhat or Tam Bảo altar, trigger interactive inspect
    if (this.inInterior) {
      if (this.arhatGroups?.length) {
        const hits = raycaster.intersectObjects(this.arhatGroups, true);
        if (hits.length > 0) {
          this.onObjectClick('OPEN_ARHAT');
          return;
        }
      }
      if (this.tamBaoAltarGroup) {
        const hits = raycaster.intersectObjects([this.tamBaoAltarGroup], true);
        if (hits.length > 0) {
          this.onObjectClick('LE_PHAT');
          return;
        }
      }
    }

    const groundPlane = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0);
    const hit = new THREE.Vector3();
    if (raycaster.ray.intersectPlane(groundPlane, hit)) {
      // Check if click is near any Pilgrimage Station landmark first
      if (!this.inInterior) {
        for (const st of PILGRIMAGE_STATIONS) {
          const dPos = Math.hypot(hit.x - st.pos.x, hit.z - st.pos.z);
          const dStand = st.standPos
            ? Math.hypot(hit.x - st.standPos.x, hit.z - st.standPos.z)
            : Infinity;
          if (Math.min(dPos, dStand) < 4.2) {
            this.walkToStation(st);
            return;
          }
        }
      }
      const clamped = this.tryMove(hit.x, hit.z);
      this.autoWalkWaypoints = [{ x: clamped.x, z: clamped.z }];
      this.autoWalkCallback = null;
      this.autoWalkStation = null;
      this.walkTargetRing.position.set(clamped.x, 0.06, clamped.z);
      this.walkTargetRing.visible = true;
      this.updateWalkPathLine();
    }
  }

  handleResize() {
    const w = this.canvas.clientWidth || window.innerWidth || 1280;
    const h = this.canvas.clientHeight || window.innerHeight || 720;
    this.camera.aspect = w / h;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(w, h, false);
  }

  updateAutoWalk(dt) {
    if (!this.autoWalkWaypoints.length) return;
    const wp = this.autoWalkWaypoints[0];
    const dx = wp.x - this.playerState.x;
    const dz = wp.z - this.playerState.z;
    const dist = Math.hypot(dx, dz);
    if (dist < 0.45) {
      this.autoWalkWaypoints.shift();
      if (this.autoWalkWaypoints.length === 0) {
        this.playerState.moving = false;
        if (wp.lookAt) {
          this.playerState.yaw = Math.atan2(
            wp.lookAt.x - this.playerState.x,
            wp.lookAt.z - this.playerState.z
          );
          this.cameraBaseYaw = this.playerState.yaw;
          this.cameraAzimuthOffset = 0;
        }
        if (this.walkTargetRing) this.walkTargetRing.visible = false;
        if (this.walkPathLine) this.walkPathLine.visible = false;
        const arrivedSt = this.autoWalkStation;
        const cb = this.autoWalkCallback;
        this.autoWalkStation = null;
        this.autoWalkCallback = null;
        this.syncPlayerTransform();
        this.checkStationProximity();
        this.onAutoWalkTargetChange(null);
        if (cb) cb(arrivedSt);
        this.onAutoWalkArrival(arrivedSt);
        return;
      }
      this.updateWalkPathLine();
      return;
    }

    const stepSpeed = Math.min(dist, dt * 5.2);
    const nx = dx / dist;
    const nz = dz / dist;
    const moved = this.tryMove(
      this.playerState.x + nx * stepSpeed,
      this.playerState.z + nz * stepSpeed
    );
    this.playerState.x = moved.x;
    this.playerState.z = moved.z;
    this.playerState.yaw = this.lerpAngle(this.playerState.yaw, Math.atan2(nx, nz), dt * 10);
    this.playerState.moving = true;
    this.syncPlayerTransform();
    this.checkStationProximity();
  }

  animate() {
    const dt = Math.min(this.clock.getDelta(), 0.05);
    const elapsed = this.clock.elapsedTime;

    this.updateHeldMovement(dt);
    this.updateAutoWalk(dt);

    if (this.activePlayerRecord) {
      if (this.playerState.moving) {
        this.playerState.moveBlend = Math.min(1, this.playerState.moveBlend + dt * 6);
        this.playClipCrossfade(this.activePlayerRecord, 'Di bo', 0.15, false);
        if (this.activePlayerRecord.activeAction) {
          this.activePlayerRecord.activeAction.paused = false;
          this.activePlayerRecord.activeAction.timeScale =
            0.55 + 0.65 * this.playerState.moveBlend;
        }
        this.activePlayerRecord.mixer.update(dt);
      } else {
        this.playerState.moveBlend = Math.max(0, this.playerState.moveBlend - dt * 7);
        if (
          this.activePlayerRecord.activeClipName === 'Di bo' ||
          this.activePlayerRecord.activeClipName === 'Đi bộ'
        ) {
          if (this.activePlayerRecord.activeAction) {
            this.activePlayerRecord.activeAction.paused = true;
          }
        } else {
          this.activePlayerRecord.mixer.update(dt);
        }
      }
    }

    // Update companion Chú tiểu An walking gently beside the player
    if (this.anCompanion && !this.inInterior) {
      const targetX = this.playerState.x + Math.cos(this.playerState.yaw) * 1.35;
      const targetZ = this.playerState.z - Math.sin(this.playerState.yaw) * 1.35 + 0.45;
      const adx = targetX - this.anCompanion.x;
      const adz = targetZ - this.anCompanion.z;
      const adist = Math.hypot(adx, adz);
      if (adist > 0.35) {
        const astep = Math.min(adist, dt * 4.8);
        this.anCompanion.x += (adx / adist) * astep;
        this.anCompanion.z += (adz / adist) * astep;
        this.anCompanion.yaw = this.lerpAngle(
          this.anCompanion.yaw,
          Math.atan2(adx, adz),
          dt * 8
        );
        this.animateArticulatedFigure(this.anCompanion.fig, elapsed, true, 1.2);
      } else {
        this.animateArticulatedFigure(this.anCompanion.fig, elapsed, false);
      }
      this.anCompanion.fig.root.position.set(this.anCompanion.x, 0, this.anCompanion.z);
      this.anCompanion.fig.root.rotation.y = this.anCompanion.yaw;
    }

    for (const npc of this.npcRecords) {
      if (npc.pauseTimer > 0) {
        npc.pauseTimer -= dt;
        this.animateArticulatedFigure(npc.fig, elapsed, false);
        continue;
      }
      const target = npc.pts[npc.idx];
      const dx = target[0] - npc.fig.root.position.x;
      const dz = target[1] - npc.fig.root.position.z;
      const d = Math.hypot(dx, dz);
      if (d < 0.35) {
        npc.idx = (npc.idx + 1) % npc.pts.length;
        npc.pauseTimer = 2.4;
        this.animateArticulatedFigure(npc.fig, elapsed, false);
      } else {
        const step = Math.min(d, dt * npc.speed);
        npc.fig.root.position.x += (dx / d) * step;
        npc.fig.root.position.z += (dz / d) * step;
        const targetYaw = Math.atan2(dx, dz);
        npc.yaw = this.lerpAngle(npc.yaw, targetYaw, dt * 6);
        npc.fig.root.rotation.y = npc.yaw;
        this.animateArticulatedFigure(npc.fig, elapsed, true, npc.speed);
      }
    }

    for (const sc of this.smokeColumns) {
      sc.update(dt, elapsed);
    }
    for (const k of this.koiList) {
      const a = elapsed * k.speed + k.phase;
      k.mesh.position.set(Math.cos(a) * k.rx, k.y, Math.sin(a) * k.rz);
      k.mesh.rotation.y = -a;
      if (k.tail) {
        k.tail.rotation.y = Math.sin(elapsed * 9 + k.phase) * 0.35;
      }
    }
    for (const p of this.pigeons) {
      const distToPlayer = Math.hypot(
        this.playerState.x - p.group.position.x,
        this.playerState.z - p.group.position.z
      );
      if (distToPlayer < 3.2 && !p.flying) {
        p.flying = true;
        p.flyTimer = 0;
      }
      if (p.flying) {
        p.flyTimer += dt;
        p.group.position.y = Math.min(5.5, p.flyTimer * 2.8);
        p.group.position.x += Math.sin(p.phase) * dt * 2.4;
        p.group.position.z -= Math.cos(p.phase) * dt * 2.4;
        if (p.wL && p.wR) {
          const flap = Math.sin(elapsed * 26) * 0.65;
          p.wL.rotation.z = flap;
          p.wR.rotation.z = -flap;
        }
        if (p.flyTimer > 4.5) {
          p.flying = false;
          p.group.position.set(p.baseX, 0, p.baseZ);
          if (p.wL && p.wR) {
            p.wL.rotation.z = 0;
            p.wR.rotation.z = 0;
          }
        }
      } else {
        p.group.position.y = Math.abs(Math.sin(elapsed * 3.2 + p.phase)) * 0.04;
        p.group.rotation.y = Math.sin(elapsed * 0.7 + p.phase) * 0.6;
      }
    }

    // Project 3D Station Pins to 2D Screen
    const w = this.canvas.clientWidth || window.innerWidth || 1280;
    const h = this.canvas.clientHeight || window.innerHeight || 720;
    const projectedList = [];
    for (const st of PILGRIMAGE_STATIONS) {
      const v = new THREE.Vector3(
        st.lookAt?.x ?? st.pos.x,
        (st.lookAt?.y ?? 3.8) + 1.1,
        st.lookAt?.z ?? st.pos.z
      );
      v.project(this.camera);
      const visible = v.z < 1 && v.z > -1;
      const px = (v.x * 0.5 + 0.5) * w;
      const py = (-v.y * 0.5 + 0.5) * h;
      projectedList.push({
        key: st.key,
        visible,
        x: px,
        y: py,
        label: st.pinLabel
      });
    }
    this.onUpdateProjectedPins(projectedList);

    this.renderer.render(this.scene, this.camera);
    if (this.isSoftwareGl) {
      this.afterDraw(() => this.animate());
    } else {
      requestAnimationFrame(() => this.animate());
    }
  }

  afterDraw(cb) {
    const gl = this.renderer.getContext();
    if (!gl || typeof gl.fenceSync !== 'function') {
      window.setTimeout(cb, 80);
      return;
    }
    const sync = gl.fenceSync(gl.SYNC_GPU_COMMANDS_COMPLETE, 0);
    gl.flush();
    const poll = () => {
      const state = sync && gl.getSyncParameter(sync, gl.SYNC_STATUS);
      if (state === gl.UNSIGNALED) {
        window.setTimeout(poll, 5);
      } else {
        if (sync) gl.deleteSync(sync);
        window.setTimeout(cb, 80);
      }
    };
    window.setTimeout(poll, 5);
  }
}
