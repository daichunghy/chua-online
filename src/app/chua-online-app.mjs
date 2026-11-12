import {
  CHARACTER_PROFILES,
  PILGRIMAGE_STATIONS,
  SHOP_CATALOG,
  DHARMA_TEXTBOOKS,
  LECTURE_PATHS,
  LECTURE_LESSONS,
  UGC_BACKDROPS,
  UGC_POSES,
  INITIAL_UGC_GALLERY,
  stepPlayerMovement,
  findNearestStation,
  createSpiritualState,
  performSpiritualAction,
  recordSpiritualMilestone,
  checkUGCMilestoneUnlock,
  calculateJourneyImprint,
  filterShopCatalog,
  addToCart,
  updateCartQuantity,
  calculateCartSummary,
  validateOrderForm,
  getLessonsByPath,
  gradeLessonQuiz,
  createUGCPost
} from '/src/logic/chua-online-logic.mjs';
import { VinhTrang3DWorld } from '/src/app/vinh-trang-3d-world.mjs';

const STORAGE_KEY = 'chua_online_vinh_trang_state_v10';

const EIGHTEEN_ARHATS = [
  { id: 1, name: 'Tôn giả Tân Độ La Bạt La Đọa Xà', title: 'Tọa Lộc La Hán', meaning: 'Cưỡi hươu vào hoàng cung độ hóa vua quan, biểu trưng cho sự thanh cao và tinh tấn.' },
  { id: 2, name: 'Tôn giả Ca Nặc Ca Phạt Tha', title: 'Khánh Hỷ La Hán', meaning: 'Phân biệt rõ thiện ác, luôn mang niềm vui chánh pháp đến cho muôn người.' },
  { id: 3, name: 'Tôn giả Ca Nặc Ca Bạt Ly Đọa Xà', title: 'Cử Bát La Hán', meaning: 'Nâng bình bát xin ăn với tâm bình đẳng, gieo ruộng phước lành cho thí chủ.' },
  { id: 4, name: 'Tôn giả Tô Tần Đà', title: 'Thác Tháp La Hán', meaning: 'Nâng bảo tháp Phật trên tay, nhắc nhở luôn hộ trì Tam Bảo và giữ tâm sáng.' },
  { id: 5, name: 'Tôn giả Nặc Cự La', title: 'Tĩnh Tọa La Hán', meaning: 'Ngồi thiền định vững chãi như núi Thái Sơn, chiến thắng nội ma phiền não.' },
  { id: 6, name: 'Tôn giả Bạt Đà La', title: 'Quá Giang La Hán', meaning: 'Vượt biển truyền bá Phật pháp khắp các hải đảo Đông Nam Á.' },
  { id: 7, name: 'Tôn giả Ca Lý Ca', title: 'Kỵ Tượng La Hán', meaning: 'Cưỡi voi trắng biểu trưng cho sức mạnh đại thừa và tâm từ bi rộng lớn.' },
  { id: 8, name: 'Tôn giả Phạt Xà La Phất Đa La', title: 'Tiếu Sư La Hán', meaning: 'Chơi đùa cùng sư tử nhỏ, cảm hóa loài hung dữ bằng lòng từ ái.' },
  { id: 9, name: 'Tôn giả Thú Bác Ca', title: 'Khai Tâm La Hán', meaning: 'Mở vạt áo để lộ tâm Phật trong sáng, nhắc người đời ai cũng có Phật tính.' },
  { id: 10, name: 'Tôn giả Bán Thác Ca', title: 'Thám Thủ La Hán', meaning: 'Vươn tay ngáp nhẹ sau giờ thiền định, tự tại giữa muôn duyên.' },
  { id: 11, name: 'Tôn giả La Hầu La', title: 'Trầm Tư La Hán', meaning: 'Mật hạnh đệ nhất, luôn suy tư quán chiếu sâu sắc để tu sửa thân tâm.' },
  { id: 12, name: 'Tôn giả Na Già Tê Na', title: 'Khoái Nhĩ La Hán', meaning: 'Ngoáy tai thảnh thơi — nghe đủ mọi âm thanh đời thường mà tâm chẳng nhiễm ô.' },
  { id: 13, name: 'Tôn giả Nhân Yết Đà', title: 'Bố Đại La Hán', meaning: 'Mang túi vải bố thu nhiếp khổ đau thế gian và trao tặng niềm hoan hỷ.' },
  { id: 14, name: 'Tôn giả Phạt Na Bà Tư', title: 'Ba Tiêu La Hán', meaning: 'Ngồi dưới tán chuối xanh nghe mưa rơi mà ngộ lý vô thường.' },
  { id: 15, name: 'Tôn giả A Thị Đa', title: 'Trường Mi La Hán', meaning: 'Đôi lông mày dài bạc trắng biểu thị phước tướng từ bi trường thọ.' },
  { id: 16, name: 'Tôn giả Chú Trà Bán Thác Ca', title: 'Khán Môn La Hán', meaning: 'Cầm gậy tích trượng canh giữ cửa thiền, nhắc hành giả hộ trì sáu căn.' },
  { id: 17, name: 'Tôn giả Khánh Hữu (Nan Đề Mật Đa La)', title: 'Hàng Long La Hán', meaning: 'Hàng phục rồng dữ — biểu trưng cho trí tuệ chế ngự lòng sân hận.' },
  { id: 18, name: 'Tôn giả Tân Đầu Lư', title: 'Phục Hổ La Hán', meaning: 'Thuần phục hổ dữ bằng tâm từ — chế ngự lòng tham lam dữ tợn.' }
];

const AUDIO_LIBRARY = [
  { id: 's0_chao', title: 'Lời chào Cổng Tam Quan Chùa Vĩnh Tràng', file: 's0_chao.mp3', duration: '01:15' },
  { id: 's3_giang_duong', title: 'Pháp âm Giảng Đường: Hơi thở & Chánh niệm', file: 's3_giang_duong.mp3', duration: '03:20' },
  { id: 's1_adida', title: 'Chiêm bái Đại tượng Phật A Di Đà', file: 's1_adida.mp3', duration: '01:45' },
  { id: 's2_thap_nhang', title: 'Hướng dẫn Dâng ba nén tâm hương đúng pháp', file: 's2_thap_nhang.mp3', duration: '01:30' },
  { id: 's3_lay_phat', title: 'Nghi thức Lễ Phật Tam Bái tại Chánh Điện', file: 's3_lay_phat.mp3', duration: '01:50' },
  { id: 's4_dilac', title: 'Nụ cười Hỷ Xả của Đức Phật Di Lặc', file: 's4_dilac.mp3', duration: '01:40' },
  { id: 's5_nirvana', title: 'Quán niệm Tịch Tịnh trước Tượng Phật Niết Bàn', file: 's5_nirvana.mp3', duration: '02:05' },
  { id: 'niem_phat_xa', title: 'Tiếng niệm Phật A Di Đà & Chuông Mõ Đạo Tràng', file: 'niem_phat_xa.mp3', duration: '04:10' },
  { id: 's6_hoi_huong', title: 'Kệ Hồi Hướng Công Đức Viên Mãn', file: 's6_hoi_huong.mp3', duration: '02:15' }
];

export class ChuaOnlineApp {
  constructor() {
    this.saved = this.loadState();
    this.playerPos = { x: 0, z: 16.0, yaw: Math.PI, moving: false };
    this.spiritual = createSpiritualState(this.saved.spiritual);
    this.cart = Array.isArray(this.saved.cart)
      ? this.saved.cart
      : [
          {
            id: 'so_tay_hoa_sen',
            name: 'Sổ tay hoa sen',
            price: 125000,
            image: '/Thiết kế giao diện/Vật phẩm 3D/models/tham_khao_tui_sen.png',
            tab: 'souvenir',
            qty: 1
          }
        ];
    this.completedLessons = new Set(this.saved.completedLessons || ['A1']);
    this.orders = this.saved.orders || [];
    this.ugcGallery = Array.isArray(this.saved.ugcGallery)
      ? this.saved.ugcGallery
      : [...INITIAL_UGC_GALLERY];
    this.characterModelKey = this.saved.characterModelKey || 'nu'; // 'nu' | 'nam' | 'tre_em'
    this.uploadedUserPhotoDataUrl = this.saved.uploadedUserPhotoDataUrl || null;
    this.activeStationKey = 'chanh_dien';

    // Active screen & sub-views
    this.activeScreen = 'courtyard'; // 'courtyard' | 'shop' | 'lecture'
    this.shopTab = 'souvenir'; // 'souvenir' | 'study' | '3d'
    this.lectureTab = 'lesson'; // 'listen' | 'lesson' | 'package' (default 'lesson' per Giảng đường V2 spec)
    this.activePathId = 'A';
    this.activeLessonId = 'A1';
    this.selectedQuizOption = 0;
    this.quizFeedback = null;
    this.autoWalkObjective = null;

    // Audio & WebAudio
    this.audioEl = new Audio();
    this.audioPlaying = false;
    this.currentAudioFile = 's3_giang_duong.mp3';
    this.audioCtx = null;

    // 3D World & Canvas references
    this.world3d = null;
    this.backdropImg = null;
    this.particles = [];
    this.is3DWorldOpen = true;
    this.toastTimer = null;
    this.cachedGLBCharacters = {};
  }

  loadState() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      return raw ? JSON.parse(raw) : {};
    } catch {
      return {};
    }
  }

  saveState() {
    try {
      localStorage.setItem(
        STORAGE_KEY,
        JSON.stringify({
          spiritual: this.spiritual,
          cart: this.cart,
          completedLessons: Array.from(this.completedLessons),
          orders: this.orders,
          ugcGallery: this.ugcGallery.slice(0, 12),
          characterModelKey: this.characterModelKey,
          uploadedUserPhotoDataUrl: this.uploadedUserPhotoDataUrl
        })
      );
    } catch {}
  }

  init() {
    this.mountDOM();
    this.initLive3DWorld();
    this.initParticleFX();
    this.bindEvents();
    this.renderShopProducts();
    this.renderLectureStage();
    this.updateActionBadges();
    this.updateEquippedTags();
    this.updateUGCMilestoneHUD();
    this.updateAnCompanionCard();

    window.__CHUA_ONLINE_APP__ = this;
    window.advanceTime = (ms = 16) => {
      const dt = ms / 1000;
      this.stepParticles(dt);
      if (this.world3d) {
        this.world3d.stepSimulation(dt);
        this.world3d.renderFrame();
      }
    };
    window.render_game_to_text = () =>
      JSON.stringify({
        screen: this.activeScreen,
        is3DWalkableWorld: true,
        insideInteriorHall: Boolean(this.world3d?.insideInterior),
        activeStationKey: this.activeStationKey,
        shopTab: this.shopTab,
        lectureTab: this.lectureTab,
        activeLessonId: this.activeLessonId,
        characterModelKey: this.characterModelKey,
        playerPos: this.world3d
          ? {
              x: Number(this.world3d.playerPos.x.toFixed(2)),
              z: Number(this.world3d.playerPos.z.toFixed(2)),
              yaw: Number(this.world3d.playerYaw.toFixed(2)),
              moving: this.world3d.playerMoving
            }
          : this.playerPos,
        ugcMilestone: checkUGCMilestoneUnlock(this.spiritual, this.completedLessons.size),
        hasUploadedUserPhoto: Boolean(this.uploadedUserPhotoDataUrl),
        spiritual: this.spiritual,
        journeyImprint: calculateJourneyImprint(this.spiritual),
        autoWalkObjective: this.autoWalkObjective ? this.autoWalkObjective.name : null,
        cartSummary: calculateCartSummary(this.cart)
      });
  }

  /* ========================================================================
     DOM MOUNTING — Live Walkable 3D World + Reference HUDs 1, 2, 3, 4
     ======================================================================== */
  mountDOM() {
    const root = document.getElementById('app-root');
    if (!root) return;

    root.innerHTML = `
      <!-- ================= 1. LIVE WALKABLE 3D COURTYARD & TEMPLE GROUNDS ================= -->
      <div id="scene-stage">
        <canvas id="courtyard-backdrop"></canvas>

        <!-- Primary Live 3D WebGL Walkable Temple World -->
        <div id="world3d-container" class="active">
          <canvas id="world3d-canvas"></canvas>
        </div>

        <canvas id="fx-canvas"></canvas>

        <!-- Quick-Walk 3D Landmark Bar: Walk freely to Lotus Pond, Great Buddhas, Main Hall, Interior, Shop, Lecture -->
        <nav class="quick-walk-bar" id="quick-walk-bar" aria-label="Đi bộ khám phá các điểm trong khuôn viên 3D">
          <button class="walk-chip-btn" id="btn-open-2d-map" style="background:#C9962E;color:#241409;font-weight:800;" title="Mở Sơ đồ kiến trúc Chùa Vĩnh Tràng 2D & Vị trí của bạn">🗺️ Sơ đồ Chùa 2D</button>
          <button class="walk-chip-btn" data-walk-station="cong_tam_quan" title="Đi bộ ra Cổng Tam Quan Nghệ Thuật">⛩️ Cổng Tam Quan</button>
          <button class="walk-chip-btn" data-walk-station="ho_sen_ca_koi" title="Đi bộ dạo Hồ Sen & Cá Koi">🪷 Hồ Sen & Cá Koi</button>
          <button class="walk-chip-btn" data-walk-station="phat_adida" title="Đi bộ chiêm bái Đại Tượng Phật A Di Đà">🙏 Phật A Di Đà</button>
          <button class="walk-chip-btn" data-walk-station="phat_di_lac" title="Đi bộ chiêm bái Đại Tượng Phật Di Lặc">😊 Phật Di Lặc</button>
          <button class="walk-chip-btn" data-walk-station="lu_huong_san" title="Đi bộ đến Lư Hương Đồng Sân Chùa">🔥 Lư Hương</button>
          <button class="walk-chip-btn active" data-walk-station="chanh_dien" title="Đi bộ về Mặt Tiền Chánh Điện">📍 Chánh Điện</button>
          <button class="walk-chip-btn" id="btn-toggle-interior-hall" title="Bước vào Nội Điện Tam Bảo & 18 Vị La Hán">🏛️ Nội Điện 18 La Hán</button>
          <button class="walk-chip-btn" data-walk-station="phat_niet_ban" title="Đi bộ đến Tượng Phật Niết Bàn & Bảo Tháp 7 Tầng">🌸 Phật Niết Bàn</button>
          <button class="walk-chip-btn" data-walk-station="cua_hang_luu_niem" title="Đi bộ đến Quầy Cửa Hàng Lưu Niệm 3D">🏮 Quầy Lưu Niệm 3D</button>
          <button class="walk-chip-btn" data-walk-station="giang_duong" title="Đi bộ đến Giảng Đường Phật Pháp">📖 Giảng Đường</button>
        </nav>

        <!-- 3D Projected Floating Scene Pins -->
        <div id="scene-pins-layer">
          <button id="pin-chanh-dien" class="scene-pin" style="left:50%;top:37.2%;" title="Đi bộ tới Chánh điện lễ Phật & vào Nội điện 18 La Hán">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
              <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5a2.5 2.5 0 0 1 0-5 2.5 2.5 0 0 1 0 5z"/>
            </svg>
            <span>Chánh điện</span>
          </button>

          <button id="pin-ho-sen" class="scene-pin secondary-pin" style="left:26%;top:56%;" title="Đi bộ ra Hồ Sen & Cá Koi">
            <span>🪷 Hồ Sen & Cá Koi</span>
          </button>

          <button id="pin-phat-adida" class="scene-pin secondary-pin" style="left:19%;top:38%;" title="Đi bộ chiêm bái Đại Tượng Phật A Di Đà">
            <span>🙏 Tượng Phật A Di Đà</span>
          </button>

          <button id="pin-phat-dilac" class="scene-pin secondary-pin" style="left:79%;top:38%;" title="Đi bộ chiêm bái Đại Tượng Phật Di Lặc">
            <span>😊 Tượng Phật Di Lặc</span>
          </button>

          <button id="pin-cua-hang" class="scene-pin secondary-pin" style="left:82%;top:52%;" title="Đi bộ tới Quầy Cửa hàng lưu niệm 3D">
            <span>🏮 Cửa hàng lưu niệm</span>
          </button>

          <button id="pin-giang-duong" class="scene-pin secondary-pin" style="left:18%;top:49%;" title="Đi bộ tới Giảng đường Phật pháp">
            <span>📖 Giảng đường</span>
          </button>
        </div>

        <!-- Milestone-Unlocked UGC Check-in Pill & Dấu Ấn Hành Trình (9 Cánh Sen) in Courtyard HUD -->
        <button id="btn-ugc-milestone-hud" class="ugc-milestone-pill locked" title="Hoàn thành 1 nghi lễ hoặc khám phá điểm đến rồi đưa ảnh của bạn vào để nhận ảnh Check-in Chùa Vĩnh Tràng">
          <span id="ugc-hud-icon">🔒</span>
          <span id="ugc-hud-text">Check-in UGC (Hoàn thành 1 hoạt động để mở khóa)</span>
        </button>

        <div id="auto-walk-objective-banner" style="display:none;position:fixed;top:114px;left:50%;transform:translateX(-50%);z-index:26;background:rgba(28,90,52,0.92);color:#FFF6E5;border:1.5px solid #C9962E;border-radius:999px;padding:6px 18px;font-size:13.5px;font-weight:800;box-shadow:0 6px 18px rgba(0,0,0,0.28);pointer-events:none;">
          🚶 Đang tới: Chánh điện
        </div>

        <!-- Protagonist Hotspot in Courtyard -->
        <div id="protagonist-hotspot" title="Bấm để mở Tủ đồ 3 Nhân vật (Nam · Nữ · Trẻ em) & Gắn vật phẩm 3D">
          <div id="equipped-tags" class="equipped-floating-tags"></div>
        </div>

        <!-- Top Navigation Bar (Always visible on Courtyard & Shop) -->
        <header class="top-hud-bar" id="main-top-hud">
          <button class="brand-pill" id="btn-brand-home" title="Về sân Chánh điện Chùa Vĩnh Tràng">
            <svg class="lotus-logo" viewBox="0 0 64 46" fill="none">
              <path d="M32 4C27 13 24 22 32 34C40 22 37 13 32 4Z" stroke="white" stroke-width="3.2" stroke-linejoin="round"/>
              <path d="M32 34C22 28 15 19 16 10C23 13 28 20 32 34Z" stroke="white" stroke-width="3.2" stroke-linejoin="round"/>
              <path d="M32 34C42 28 49 19 48 10C41 13 36 20 32 34Z" stroke="white" stroke-width="3.2" stroke-linejoin="round"/>
              <path d="M32 35C18 35 8 28 5 19C14 19 23 25 32 35Z" stroke="white" stroke-width="3.2" stroke-linejoin="round"/>
              <path d="M32 35C46 35 56 28 59 19C50 19 41 25 32 35Z" stroke="white" stroke-width="3.2" stroke-linejoin="round"/>
              <path d="M12 40H52" stroke="white" stroke-width="3.2" stroke-linecap="round"/>
            </svg>
            <span class="brand-main">Chùa Online</span>
            <span class="brand-divider"></span>
            <span class="brand-sub">Chùa Vĩnh Tràng</span>
          </button>

          <nav class="top-nav-group" aria-label="Điều hướng chính">
            <button class="nav-pill-btn" id="nav-btn-explore">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
                <circle cx="12" cy="12" r="9"/>
                <polygon points="15.5,8.5 13.5,13.5 8.5,15.5 10.5,10.5" fill="currentColor" stroke="none"/>
              </svg>
              <span>Khám phá</span>
            </button>

            <button class="nav-pill-btn" id="nav-btn-lecture">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M2 4h7a4 4 0 0 1 4 4v13a3 3 0 0 0-3-3H2z"/>
                <path d="M22 4h-7a4 4 0 0 0-4 4v13a3 3 0 0 1 3-3h8z"/>
              </svg>
              <span>Học Phật</span>
            </button>

            <button class="nav-pill-btn" id="nav-btn-account">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round">
                <circle cx="12" cy="8" r="4"/>
                <path d="M4 20c1.5-4 5-6 8-6s6.5 2 8 6"/>
              </svg>
              <span>Tài khoản</span>
            </button>
          </nav>
        </header>

        <!-- Chú Tiểu An Contextual Companion & Station Ritual Card -->
        <aside id="an-companion-card" style="position:fixed;left:22px;bottom:192px;z-index:24;width:276px;background:rgba(255,246,229,0.97);border:2px solid #C9962E;border-radius:20px;padding:10px 13px;box-shadow:0 10px 26px rgba(24,42,28,0.28);color:#4A3222;">
          <div style="display:flex;align-items:center;justify-content:space-between;gap:6px;">
            <span style="font-size:12px;font-weight:800;color:#1C5A34;" id="an-card-station">📍 Sân Chánh Điện</span>
            <button id="btn-an-mini-map" style="background:#1C5A34;color:#FFF6E5;border:none;border-radius:999px;padding:3px 9px;font-size:11px;font-weight:700;cursor:pointer;">🗺️ Bản đồ</button>
          </div>
          <p id="an-card-quote" style="font-size:12px;line-height:1.38;margin:5px 0 8px;color:#4A3222;">
            Chú tiểu An: "Mời đạo hữu giữ phím mũi tên / WASD hoặc bấm mặt đất để dạo bước chiêm bái!"
          </p>
          <div style="display:flex;gap:6px;">
            <button id="btn-an-station-action" style="flex:1;background:linear-gradient(180deg,#C96F4A 0%,#A65230 100%);color:#FFF6E5;border:none;border-radius:999px;padding:6px 10px;font-size:12px;font-weight:800;cursor:pointer;">
              🏛️ Vào Nội Điện 18 La Hán
            </button>
            <button id="btn-an-teleport-here" style="background:#FFFdf8;color:#1C5A34;border:1.5px solid #1C5A34;border-radius:999px;padding:6px 9px;font-size:11.5px;font-weight:800;cursor:pointer;" title="Dịch chuyển nhanh đến trạm đang chọn">
              ⚡ Đến ngay
            </button>
          </div>
        </aside>

        <!-- Bottom-Left D-Pad Card ("Di chuyển" — Matches Reference Image 1) -->
        <aside class="dpad-card" id="dpad-card" aria-label="Bộ điều khiển di chuyển">
          <div class="dpad-title">Di chuyển (Giữ để đi)</div>
          <div class="dpad-grid">
            <button class="dpad-btn dpad-up" data-dir="up" aria-label="Tiến lên">
              <svg viewBox="0 0 24 24"><polygon points="12,5 20,18 4,18"/></svg>
            </button>
            <button class="dpad-btn dpad-left" data-dir="left" aria-label="Sang trái">
              <svg viewBox="0 0 24 24"><polygon points="5,12 18,4 18,20"/></svg>
            </button>
            <button class="dpad-btn dpad-right" data-dir="right" aria-label="Sang phải">
              <svg viewBox="0 0 24 24"><polygon points="19,12 6,4 6,20"/></svg>
            </button>
            <button class="dpad-btn dpad-down" data-dir="down" aria-label="Lùi lại">
              <svg viewBox="0 0 24 24"><polygon points="12,19 4,6 20,6"/></svg>
            </button>
          </div>
        </aside>

        <!-- Bottom-Right 4 Spiritual Action Buttons (Matches Reference Image 1) -->
        <section class="spiritual-actions-bar" id="spiritual-actions-bar" aria-label="Nghi thức tâm linh">
          <button class="action-square-btn" id="act-le-phat">
            <span class="action-badge-count" id="badge-le-phat" style="display:none;">0</span>
            <div class="action-icon">
              <svg viewBox="0 0 64 52" width="48" height="42" fill="#FFF3DC">
                <path d="M32 6C27 16 25 25 32 37C39 25 37 16 32 6Z"/>
                <path d="M29 38C20 31 15 22 17 13C23 17 27 25 29 38Z"/>
                <path d="M35 38C44 31 49 22 47 13C41 17 37 25 35 38Z"/>
                <path d="M26 42C14 39 7 31 6 22C14 23 21 30 26 42Z"/>
                <path d="M38 42C50 39 57 31 58 22C50 23 43 30 38 42Z"/>
              </svg>
            </div>
            <span class="action-label">Lễ Phật</span>
          </button>

          <button class="action-square-btn" id="act-dang-huong">
            <span class="action-badge-count" id="badge-dang-huong" style="display:none;">0</span>
            <div class="action-icon">
              <svg viewBox="0 0 64 56" width="46" height="42" fill="none">
                <path d="M24 20C22 14 26 10 24 4" stroke="#FFF3DC" stroke-width="3" stroke-linecap="round"/>
                <path d="M32 18C30 12 34 8 32 2" stroke="#FFF3DC" stroke-width="3" stroke-linecap="round"/>
                <path d="M40 20C38 14 42 10 40 4" stroke="#FFF3DC" stroke-width="3" stroke-linecap="round"/>
                <rect x="16" y="24" width="32" height="5" rx="2.5" fill="#FFF3DC"/>
                <path d="M18 30H46L43 44C42 47 38 49 32 49C26 49 22 47 21 44L18 30Z" fill="#FFF3DC"/>
                <path d="M23 48L20 54M41 48L44 54M32 49V54" stroke="#FFF3DC" stroke-width="3.2" stroke-linecap="round"/>
              </svg>
            </div>
            <span class="action-label">Dâng hương</span>
          </button>

          <button class="action-square-btn" id="act-dang-hoa">
            <span class="action-badge-count" id="badge-dang-hoa" style="display:none;">0</span>
            <div class="action-icon">
              <svg viewBox="0 0 64 56" width="46" height="42" fill="#FFF3DC">
                <path d="M32 6C28 14 27 22 32 30C37 22 36 14 32 6Z"/>
                <path d="M30 30C22 26 17 18 19 11C24 14 28 20 30 30Z"/>
                <path d="M34 30C42 26 47 18 45 11C40 14 36 20 34 30Z"/>
                <path d="M28 32C18 32 11 26 10 19C17 20 23 24 28 32Z"/>
                <path d="M36 32C46 32 53 26 54 19C47 20 41 24 36 32Z"/>
                <path d="M32 33V50M22 42C26 42 30 45 32 49M42 42C38 42 34 45 32 49" stroke="#FFF3DC" stroke-width="3.2" stroke-linecap="round" fill="none"/>
              </svg>
            </div>
            <span class="action-label">Dâng hoa</span>
          </button>

          <button class="action-square-btn" id="act-niem-phat">
            <span class="action-badge-count" id="badge-niem-phat" style="display:none;">0</span>
            <div class="action-icon">
              <svg viewBox="0 0 64 56" width="46" height="42" fill="#FFF3DC">
                <circle cx="32" cy="8" r="3.4"/>
                <circle cx="41" cy="10" r="3.4"/>
                <circle cx="47" cy="17" r="3.4"/>
                <circle cx="48" cy="26" r="3.4"/>
                <circle cx="43" cy="34" r="3.4"/>
                <circle cx="35" cy="39" r="3.4"/>
                <circle cx="27" cy="39" r="3.4"/>
                <circle cx="19" cy="34" r="3.4"/>
                <circle cx="16" cy="25" r="3.4"/>
                <circle cx="18" cy="16" r="3.4"/>
                <circle cx="24" cy="10" r="3.4"/>
                <path d="M26 42L21 53M28 43L26 54" stroke="#FFF3DC" stroke-width="2.8" stroke-linecap="round"/>
              </svg>
            </div>
            <span class="action-label">Niệm Phật</span>
          </button>
        </section>

        <!-- Ritual / Narration Toast -->
        <div id="ritual-toast" role="status" aria-live="polite">
          <div class="toast-title" id="toast-title">Chùa Vĩnh Tràng</div>
          <div class="toast-desc" id="toast-desc">Chào mừng đạo hữu về chiêm bái ngôi cổ tự miền Tây.</div>
        </div>
      </div>

      <!-- ================= 2. CỬA HÀNG LƯU NIỆM & VẬT PHẨM 3D (Reference Image 2) ================= -->
      <section id="shop-screen" aria-label="Cửa hàng lưu niệm">
        <div class="shop-kiosk-hero">
          <div class="top-hud-bar">
            <button class="brand-pill" id="btn-shop-back-home">
              <svg class="lotus-logo" viewBox="0 0 64 46" fill="none">
                <path d="M32 4C27 13 24 22 32 34C40 22 37 13 32 4Z" stroke="white" stroke-width="3.2"/>
                <path d="M32 34C22 28 15 19 16 10C23 13 28 20 32 34Z" stroke="white" stroke-width="3.2"/>
                <path d="M32 34C42 28 49 19 48 10C41 13 36 20 32 34Z" stroke="white" stroke-width="3.2"/>
                <path d="M12 40H52" stroke="white" stroke-width="3.2" stroke-linecap="round"/>
              </svg>
              <span class="brand-main">Chùa Online</span>
              <span class="brand-divider"></span>
              <span class="brand-sub">Chùa Vĩnh Tràng</span>
            </button>

            <div class="top-nav-group">
              <button class="nav-pill-btn" id="shop-nav-kiosk3d" style="background:#7a481d;"><span>🏮 Xem Mô Hình Quầy 3D</span></button>
              <button class="nav-pill-btn" id="shop-nav-explore"><span>Khám phá</span></button>
              <button class="nav-pill-btn" id="shop-nav-lecture"><span>Học Phật</span></button>
              <button class="nav-pill-btn" id="shop-nav-account"><span>Tài khoản</span></button>
            </div>
          </div>
        </div>

        <div class="shop-sheet-body">
          <div class="shop-lotus-crest" aria-hidden="true">
            <svg viewBox="0 0 180 68" width="165" height="60">
              <path d="M22 50C40 42 54 44 68 52" stroke="#3D8854" stroke-width="5" stroke-linecap="round" fill="none"/>
              <path d="M158 50C140 42 126 44 112 52" stroke="#3D8854" stroke-width="5" stroke-linecap="round" fill="none"/>
              <path d="M90 8C81 22 79 38 90 54C101 38 99 22 90 8Z" fill="#F78FB3" stroke="#E05A8B" stroke-width="1.5"/>
              <path d="M88 54C72 45 64 31 67 17C77 22 84 34 88 54Z" fill="#F8A5C2" stroke="#E05A8B" stroke-width="1.5"/>
              <path d="M92 54C108 45 116 31 113 17C103 22 96 34 92 54Z" fill="#F8A5C2" stroke="#E05A8B" stroke-width="1.5"/>
              <path d="M85 56C66 55 53 45 49 32C62 33 74 42 85 56Z" fill="#FBC3D8" stroke="#E05A8B" stroke-width="1.5"/>
              <path d="M95 56C114 55 127 45 131 32C118 33 106 42 95 56Z" fill="#FBC3D8" stroke="#E05A8B" stroke-width="1.5"/>
            </svg>
          </div>

          <h1 class="shop-main-title">Cửa hàng lưu niệm</h1>
          <p class="shop-main-subtitle">Chọn món quà gợi nhớ chuyến đi chùa</p>

          <!-- 3 Category Pill Tabs -->
          <div class="shop-tabs-row" role="tablist">
            <button class="shop-tab-pill active" data-shop-tab="souvenir" role="tab">
              <span>🪷</span>
              <span>Quà lưu niệm</span>
            </button>
            <button class="shop-tab-pill" data-shop-tab="study" role="tab">
              <span>📖</span>
              <span>Đồ tu học</span>
            </button>
            <button class="shop-tab-pill" data-shop-tab="3d" role="tab">
              <span>📦</span>
              <span>Vật phẩm 3D</span>
            </button>
          </div>

          <!-- 3-Column Product Card Grid -->
          <div class="shop-products-grid" id="shop-products-grid"></div>

          <!-- Footer Bar: Cần hỗ trợ? + Large Terracotta Giỏ hàng -->
          <div class="shop-footer-bar">
            <button class="shop-support-btn" id="btn-shop-support">
              <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2.2">
                <path d="M3 18v-6a9 9 0 0 1 18 0v6"/>
                <path d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3zM3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z"/>
              </svg>
              <span>Cần hỗ trợ?</span>
            </button>

            <button class="shop-cart-cta" id="btn-open-cart">
              <svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="9" cy="21" r="1.5"/>
                <circle cx="20" cy="21" r="1.5"/>
                <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/>
              </svg>
              <span id="shop-cart-label">Giỏ hàng (1)</span>
            </button>

            <button class="shop-close-pill" id="btn-shop-return-courtyard">
              ← Về sân Chánh điện
            </button>
          </div>
        </div>
      </section>

      <!-- ================= 3. GIẢNG ĐƯỜNG PHẬT PHÁP (Reference Image 3 & Lesson Cards) ================= -->
      <section id="lecture-screen" aria-label="Giảng đường Phật pháp">
        <header class="lecture-top-bar">
          <div class="lecture-top-left">
            <button class="lecture-back-courtyard" id="btn-lecture-back">← Sân chùa</button>
            <h1 class="lecture-hall-heading">Giảng đường Phật pháp</h1>
          </div>
          <div style="display:flex;gap:10px;align-items:center;">
            <button class="lecture-back-courtyard" id="btn-lecture-textbooks" style="background:rgba(230,174,71,0.22);border-color:rgba(230,174,71,0.55);color:#ffe8b3;">
              📚 10 Giáo trình PDF
            </button>
            <button class="lecture-audio-gold-btn" id="btn-lecture-recordings">Bài thu âm</button>
          </div>
        </header>

        <main class="lecture-center-stage" id="lecture-center-stage"></main>

        <footer class="lecture-bottom-dock" role="tablist">
          <button class="lecture-dock-tab active" data-lecture-tab="listen" role="tab">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
              <path d="M3 18v-6a9 9 0 0 1 18 0v6"/>
              <path d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3zM3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z"/>
            </svg>
            <span>Nghe giảng</span>
          </button>

          <button class="lecture-dock-tab" data-lecture-tab="lesson" role="tab">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
              <path d="M2 4h7a4 4 0 0 1 4 4v13a3 3 0 0 0-3-3H2z"/>
              <path d="M22 4h-7a4 4 0 0 0-4 4v13a3 3 0 0 1 3-3h8z"/>
            </svg>
            <span>Bài học</span>
          </button>

          <button class="lecture-dock-tab" data-lecture-tab="package" role="tab">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
              <polygon points="12 2 2 7 12 12 22 7 12 2"/>
              <polyline points="2 12 12 17 22 12"/>
              <polyline points="2 17 12 22 22 17"/>
            </svg>
            <span>Gói học</span>
          </button>
        </footer>
      </section>

      <!-- ================= 4. UNIVERSAL MODAL OVERLAY ================= -->
      <div class="modal-backdrop" id="universal-modal" role="dialog" aria-modal="true">
        <div class="modal-card">
          <div class="modal-header">
            <h3 id="modal-title">Chi tiết</h3>
            <button class="modal-close-x" id="modal-close-btn" aria-label="Đóng">✕</button>
          </div>
          <div class="modal-body" id="modal-body"></div>
        </div>
      </div>
    `;
  }

  /* ========================================================================
     LIVE WALKABLE 3D WORLD INITIALIZATION (Default Viewport)
     ======================================================================== */
  initLive3DWorld() {
    const canvas = document.getElementById('world3d-canvas');
    if (!canvas) return;

    this.world3d = new VinhTrang3DWorld(canvas, {
      initialCharKey: this.characterModelKey,
      onAutoWalkTargetChange: (targetStation) => {
        this.autoWalkObjective = targetStation || null;
        const banner = document.getElementById('auto-walk-objective-banner');
        if (banner) {
          if (targetStation) {
            banner.style.display = 'inline-flex';
            banner.textContent = `🚶 Đang tới: ${targetStation.name}`;
          } else {
            banner.style.display = 'none';
          }
        }
      },
      onStationArrive: (station) => {
        if (!station) return;
        this.activeStationKey = station.key;
        if (!this.spiritual.visitedStations.includes(station.id)) {
          this.spiritual.visitedStations.push(station.id);
        }
        this.spiritual = recordSpiritualMilestone(
          this.spiritual,
          `Khám phá ${station.name}`
        );
        this.saveState();
        this.updateUGCMilestoneHUD();
        this.highlightActiveWalkChip(station.key);
        this.updateAnCompanionCard();
        this.playVoiceAudio(station.audio);
        this.showToast(
          `📍 Đã tới: ${station.name}`,
          `${station.subtitle}`,
          5200,
          true
        );
      },
      onUpdateProjectedPins: (projected) => {
        const pinMap = {
          chanh_dien: 'pin-chanh-dien',
          ho_sen_ca_koi: 'pin-ho-sen',
          phat_adida: 'pin-phat-adida',
          phat_di_lac: 'pin-phat-dilac',
          cua_hang_luu_niem: 'pin-cua-hang',
          giang_duong: 'pin-giang-duong'
        };
        projected.forEach((p) => {
          const domId = pinMap[p.key];
          if (!domId) return;
          const el = document.getElementById(domId);
          if (!el) return;
          if (!p.visible || p.y < 118 || p.y > window.innerHeight - 130) {
            el.style.display = 'none';
          } else {
            el.style.display = 'inline-flex';
            el.style.left = `${Math.round(p.x)}px`;
            el.style.top = `${Math.round(p.y)}px`;
          }
        });
      },
      onObjectClick: (action, payload) => {
        if (action === 'ENTER_INTERIOR') {
          this.toggleInteriorHallIn3D(true);
        } else if (action === 'OPEN_ARHAT') {
          this.openExploreModal('arhats');
        } else if (action === 'LE_PHAT') {
          this.triggerLePhat();
        } else if (action === 'DANG_HUONG') {
          this.triggerDangHuong();
        } else if (action === 'DANG_HOA') {
          this.triggerDangHoa();
        } else if (action === 'OPEN_SHOP') {
          this.switchScreen('shop');
        } else if (action === 'OPEN_LECTURE') {
          this.switchScreen('lecture');
        } else if (action === 'TOAST' && payload) {
          this.spiritual = recordSpiritualMilestone(this.spiritual, payload.title || 'Chiêm bái khuôn viên chùa');
          this.saveState();
          this.updateUGCMilestoneHUD();
          this.showToast(payload.title, payload.desc, 4800, true);
        }
      }
    });

    this.world3d.init();

    window.addEventListener('resize', () => {
      this.resizeFXCanvas();
    });
  }

  updateAnCompanionCard() {
    const st =
      PILGRIMAGE_STATIONS.find((s) => s.key === this.activeStationKey) || PILGRIMAGE_STATIONS[5];
    const stEl = document.getElementById('an-card-station');
    const quoteEl = document.getElementById('an-card-quote');
    const actBtn = document.getElementById('btn-an-station-action');
    if (!stEl || !quoteEl || !actBtn) return;

    const companionGuides = {
      cong_tam_quan: {
        quote: 'Chú tiểu An: "Cổng Tam Quan ghép mảnh sành sứ cổ lấp lánh dưới nắng. Bước qua cửa Không để lòng nhẹ tênh!"',
        btnLabel: '🎧 Nghe thuyết minh Cổng Tam Quan'
      },
      ho_sen_ca_koi: {
        quote: 'Chú tiểu An: "Song Liên Trì nước biếc sen hồng, đàn cá Koi vàng cam đang bơi lượn quanh Đài Quan Âm!"',
        btnLabel: '🐟 Cho cá Koi ăn & Thả hoa sen'
      },
      phat_adida: {
        quote: 'Chú tiểu An: "Đại tượng Phật A Di Đà cao sừng sững giữa vòm cây xanh, tay kết ấn Tiếp Dẫn từ bi."',
        btnLabel: '🙏 Chiêm bái & Lễ Phật A Di Đà'
      },
      phat_di_lac: {
        quote: 'Chú tiểu An: "Đức Phật Di Lặc nở nụ cười hoan hỷ bao dung, nhắc ta buông xả mọi phiền muộn."',
        btnLabel: '😊 Lễ Phật Di Lặc & Cầu Hoan Hỷ'
      },
      lu_huong_san: {
        quote: 'Chú tiểu An: "Trước Lư Hương đồng có đèn dầu thắp hương. Mời đạo hữu châm 3 nén tâm hương Giới - Định - Tuệ."',
        btnLabel: '🔥 Thắp nhang từ đèn dầu (4 bước)'
      },
      chanh_dien: {
        quote: 'Chú tiểu An: "Mặt tiền Chánh Điện 13 nhịp vòm vàng rực rỡ. Mời đạo hữu cởi giày bước vào Nội Điện 18 La Hán!"',
        btnLabel: this.world3d?.insideInterior ? '🙏 Chiêm bái 18 Vị La Hán' : '🏛️ Vào Nội Điện 18 La Hán'
      },
      cua_hang_luu_niem: {
        quote: 'Chú tiểu An: "Quầy Lưu Niệm có nón lá thêu sen, áo tràng, tràng hạt bồ đề và 20 pháp khí 3D để thử gắn!"',
        btnLabel: '🏮 Mở Cửa Hàng Lưu Niệm 3D'
      },
      giang_duong: {
        quote: 'Chú tiểu An: "Giảng đường gỗ lim trang nghiêm có 24 bài học Phật pháp và 10 giáo trình PDF gốc."',
        btnLabel: '📖 Vào Giảng Đường Học Phật'
      },
      phat_niet_ban: {
        quote: 'Chú tiểu An: "Sau Chánh Điện là Đại Tượng Phật Niết Bàn dài 28m và Bảo Tháp Xá Lợi 7 tầng uy nghiêm."',
        btnLabel: '🔔 Thỉnh Chuông & Đọc Kệ Hồi Hướng'
      }
    };

    const g = companionGuides[st.key] || companionGuides.chanh_dien;
    stEl.textContent = st.pinLabel;
    quoteEl.textContent = g.quote;
    actBtn.textContent = g.btnLabel;
  }

  triggerAnStationAction() {
    const key = this.activeStationKey;
    if (key === 'cong_tam_quan') {
      this.playBellTone(216, 2.4);
      this.playVoiceAudio('s0_chao.mp3');
      this.showToast('⛩️ Cổng Tam Quan Nghệ Thuật Khảm Sành Sứ', 'Ba cửa Không — Vô Tướng — Vô Tác dẫn vào cõi thiền Vĩnh Tràng.', 4800, true);
    } else if (key === 'ho_sen_ca_koi') {
      this.world3d?.placeLotusOfferingIn3D();
      this.playBellTone(324, 2.2);
      this.spiritual = recordSpiritualMilestone(this.spiritual, 'Cho cá Koi ăn & Thả sen tại Song Liên Trì');
      this.saveState();
      this.updateUGCMilestoneHUD();
      this.showToast('🐟 Đã rải thức ăn cho đàn cá Koi & Thả sen', 'Đàn cá Koi quẫy đuôi bơi lại gần mặt hồ sen trong vắt!', 4800, true);
    } else if (key === 'phat_adida') {
      this.playVoiceAudio('s1_adida.mp3');
      this.triggerLePhat();
    } else if (key === 'phat_di_lac') {
      this.playVoiceAudio('s4_dilac.mp3');
      this.triggerLePhat();
    } else if (key === 'lu_huong_san') {
      this.triggerDangHuong();
    } else if (key === 'chanh_dien') {
      if (this.world3d?.insideInterior) {
        this.openExploreModal('arhats');
      } else {
        this.toggleInteriorHallIn3D(true);
      }
    } else if (key === 'cua_hang_luu_niem') {
      this.switchScreen('shop');
    } else if (key === 'giang_duong') {
      this.switchScreen('lecture');
    } else if (key === 'phat_niet_ban') {
      this.playBellTone(196, 3.2);
      this.playVoiceAudio('s6_hoi_huong.mp3');
      this.spiritual = recordSpiritualMilestone(this.spiritual, 'Hồi hướng tại Đại Tượng Phật Niết Bàn & Bảo Tháp 7 Tầng');
      this.saveState();
      this.updateUGCMilestoneHUD();
      this.showToast('🔔 Nguyện Đem Công Đức Này — Hồi Hướng Khắp Tất Cả', 'Tiếng Đại Hồng Chung ngân vang từ Bảo Tháp 7 Tầng và Vườn Phật Niết Bàn.', 5200, true);
    }
  }

  highlightActiveWalkChip(stationKey) {
    document.querySelectorAll('[data-walk-station]').forEach((btn) => {
      btn.classList.toggle('active', btn.getAttribute('data-walk-station') === stationKey);
    });
  }

  teleportToStationIn3D(stationKey) {
    this.activeStationKey = stationKey;
    this.highlightActiveWalkChip(stationKey);
    const st =
      PILGRIMAGE_STATIONS.find((s) => s.key === stationKey) || PILGRIMAGE_STATIONS[5];
    if (!this.spiritual.visitedStations.includes(st.id)) {
      this.spiritual.visitedStations.push(st.id);
    }
    this.spiritual = recordSpiritualMilestone(this.spiritual, `Đến chiêm bái ${st.name}`);
    this.saveState();
    this.updateUGCMilestoneHUD();
    if (this.world3d) {
      if (this.world3d.insideInterior) {
        this.toggleInteriorHallIn3D(false);
      }
      this.world3d.teleportToStation(stationKey);
      this.playerPos = {
        x: Number(this.world3d.playerPos.x.toFixed(2)),
        z: Number(this.world3d.playerPos.z.toFixed(2)),
        yaw: Number(this.world3d.playerYaw.toFixed(2)),
        moving: false
      };
    }
    this.updateAnCompanionCard();
    this.playVoiceAudio(st.audio);
    this.showToast(`📍 Đã đến: ${st.name}`, st.subtitle, 4500, true);
  }

  walkToStationIn3D(stationKey) {
    this.activeStationKey = stationKey;
    this.highlightActiveWalkChip(stationKey);
    const st =
      PILGRIMAGE_STATIONS.find((s) => s.key === stationKey) || PILGRIMAGE_STATIONS[5];

    if (!this.spiritual.visitedStations.includes(st.id)) {
      this.spiritual.visitedStations.push(st.id);
    }
    this.spiritual = recordSpiritualMilestone(this.spiritual, `Hành hương tới ${st.name}`);
    this.saveState();
    this.updateUGCMilestoneHUD();

    if (this.world3d) {
      const pinsLayer = document.getElementById('scene-pins-layer');
      if (pinsLayer) pinsLayer.style.display = 'block';
      const intBtn = document.getElementById('btn-toggle-interior-hall');
      if (intBtn) {
        intBtn.classList.remove('active');
        intBtn.innerHTML = '🏛️ Nội Điện 18 La Hán';
      }
      this.world3d.walkToStation(stationKey);
      this.playerPos = {
        x: st.standPos?.x ?? st.pos.x,
        z: st.standPos?.z ?? st.pos.z,
        yaw: st.lookYaw ?? Math.PI,
        moving: true
      };
    }
    this.updateAnCompanionCard();

    this.showToast(
      `🚶 Đang đi bộ tới: ${st.name}`,
      `Chú tiểu An đang dẫn đường trên lối sen vàng tới ${st.name}...`,
      3800,
      true
    );
  }

  toggleInteriorHallIn3D(forceEnter = null) {
    if (!this.world3d) return;
    const entering = forceEnter !== null ? forceEnter : !this.world3d.insideInterior;
    const btn = document.getElementById('btn-toggle-interior-hall');
    const pinsLayer = document.getElementById('scene-pins-layer');
    if (entering) {
      this.world3d.enterInteriorHall();
      if (pinsLayer) pinsLayer.style.display = 'none';
      if (btn) {
        btn.classList.add('active');
        btn.innerHTML = '← Ra Sân Chánh Điện 3D';
      }
      this.spiritual = recordSpiritualMilestone(
        this.spiritual,
        'Chiêm bái Nội Điện Tam Bảo & 18 Vị La Hán'
      );
      this.saveState();
      this.updateUGCMilestoneHUD();
      this.playBellTone(216, 2.6);
      this.showToast(
        '🏛️ Nội Điện Chánh Điện & 18 Vị La Hán',
        'Bạn đang ở trong Nội Điện. Dùng phím di chuyển / chuột để chiêm bái bàn thờ Tam Bảo và 18 pho tượng La Hán dọc hai hành lang.',
        5200,
        true
      );
    } else {
      this.world3d.exitInteriorHall();
      if (pinsLayer) pinsLayer.style.display = 'block';
      if (btn) {
        btn.classList.remove('active');
        btn.innerHTML = '🏛️ Nội Điện 18 La Hán';
      }
      this.showToast(
        '🌿 Đã bước ra Sân Chánh Điện 3D',
        'Tiếp tục đi bộ khám phá Hồ Sen, Đại Tượng Phật A Di Đà, Phật Di Lặc và Phật Niết Bàn.',
        4000
      );
    }
  }

  updateUGCMilestoneHUD() {
    const status = checkUGCMilestoneUnlock(this.spiritual, this.completedLessons.size);
    const hudBtn = document.getElementById('btn-ugc-milestone-hud');
    const iconEl = document.getElementById('ugc-hud-icon');
    const textEl = document.getElementById('ugc-hud-text');
    if (!hudBtn || !iconEl || !textEl) return;

    if (status.unlocked) {
      hudBtn.classList.remove('locked');
      hudBtn.classList.add('unlocked');
      iconEl.textContent = '📸';
      textEl.textContent = `Check-in UGC: ${status.latestMilestone} (Đưa ảnh vào!)`;
    } else {
      hudBtn.classList.remove('unlocked');
      hudBtn.classList.add('locked');
      iconEl.textContent = '🔒';
      textEl.textContent = 'Check-in UGC (Hoàn thành 1 nghi lễ để mở khóa)';
    }
  }

  /* ========================================================================
     AMBIENT INCENSE SMOKE & LOTUS PETAL PARTICLE FX
     ======================================================================== */
  initParticleFX() {
    this.resizeFXCanvas();
    for (let i = 0; i < 28; i++) {
      this.particles.push(this.createParticle(i));
    }
    const loop = () => {
      this.stepParticles(0.016);
      setTimeout(loop, 95);
    };
    setTimeout(loop, 95);
  }

  resizeFXCanvas() {
    const fx = document.getElementById('fx-canvas');
    if (!fx) return;
    fx.width = window.innerWidth;
    fx.height = window.innerHeight;
  }

  createParticle(idx = 0) {
    const isSmoke = idx < 16;
    return {
      type: isSmoke ? 'smoke' : 'petal',
      x: isSmoke ? 0.5 + (Math.random() - 0.5) * 0.03 : Math.random(),
      y: isSmoke ? 0.52 - Math.random() * 0.14 : Math.random() * 0.6,
      vx: isSmoke ? (Math.random() - 0.5) * 0.004 : (Math.random() - 0.3) * 0.015,
      vy: isSmoke ? -0.015 - Math.random() * 0.012 : 0.012 + Math.random() * 0.015,
      size: isSmoke ? 8 + Math.random() * 14 : 4 + Math.random() * 5,
      alpha: isSmoke ? 0.18 + Math.random() * 0.22 : 0.45 + Math.random() * 0.35,
      phase: Math.random() * Math.PI * 2
    };
  }

  stepParticles(dt) {
    if (this.activeScreen !== 'courtyard') return;
    const fx = document.getElementById('fx-canvas');
    if (!fx) return;
    const ctx = fx.getContext('2d');
    const w = fx.width;
    const h = fx.height;
    ctx.clearRect(0, 0, w, h);

    const smokeMultiplier = this.spiritual.incenseOfferings > 0 ? 1.65 : 1.0;

    for (const p of this.particles) {
      p.phase += dt * 2.2;
      p.x += (p.vx + Math.sin(p.phase) * 0.003) * dt;
      p.y += p.vy * dt;

      if (p.type === 'smoke') {
        if (p.y < 0.34) {
          p.y = 0.53;
          p.x = 0.5 + (Math.random() - 0.5) * 0.02;
        }
        const px = p.x * w;
        const py = p.y * h;
        const grad = ctx.createRadialGradient(px, py, 1, px, py, p.size * smokeMultiplier);
        grad.addColorStop(0, `rgba(255, 248, 235, ${p.alpha * smokeMultiplier})`);
        grad.addColorStop(1, 'rgba(255, 248, 235, 0)');
        ctx.fillStyle = grad;
        ctx.beginPath();
        ctx.arc(px, py, p.size * smokeMultiplier, 0, Math.PI * 2);
        ctx.fill();
      } else {
        if (p.y > 0.95 || p.x < 0 || p.x > 1) {
          p.y = 0.05;
          p.x = Math.random();
        }
        const px = p.x * w;
        const py = p.y * h;
        ctx.save();
        ctx.translate(px, py);
        ctx.rotate(p.phase);
        ctx.fillStyle = `rgba(247, 143, 179, ${p.alpha})`;
        ctx.beginPath();
        ctx.ellipse(0, 0, p.size, p.size * 0.55, 0, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
      }
    }
  }

  /* ========================================================================
     SOUND & VOICEOVER ENGINE (WebAudio Bell/Mokugyo + audio_v5 MP3s)
     ======================================================================== */
  ensureAudioContext() {
    if (!this.audioCtx) {
      const AC = window.AudioContext || window.webkitAudioContext;
      if (AC) this.audioCtx = new AC();
    }
    if (this.audioCtx && this.audioCtx.state === 'suspended') {
      this.audioCtx.resume().catch(() => {});
    }
  }

  playBellTone(freq = 216, duration = 2.6) {
    try {
      this.ensureAudioContext();
      if (!this.audioCtx) return;
      const now = this.audioCtx.currentTime;
      const osc1 = this.audioCtx.createOscillator();
      const osc2 = this.audioCtx.createOscillator();
      const gain = this.audioCtx.createGain();
      osc1.type = 'sine';
      osc2.type = 'sine';
      osc1.frequency.setValueAtTime(freq, now);
      osc2.frequency.setValueAtTime(freq * 2.756, now);
      gain.gain.setValueAtTime(0.24, now);
      gain.gain.exponentialRampToValueAtTime(0.0008, now + duration);
      osc1.connect(gain);
      osc2.connect(gain);
      gain.connect(this.audioCtx.destination);
      osc1.start(now);
      osc2.start(now);
      osc1.stop(now + duration);
      osc2.stop(now + duration);
    } catch {}
  }

  playMokugyoTap() {
    try {
      this.ensureAudioContext();
      if (!this.audioCtx) return;
      const now = this.audioCtx.currentTime;
      const osc = this.audioCtx.createOscillator();
      const gain = this.audioCtx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(390, now);
      osc.frequency.exponentialRampToValueAtTime(250, now + 0.09);
      gain.gain.setValueAtTime(0.28, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.11);
      osc.connect(gain);
      gain.connect(this.audioCtx.destination);
      osc.start(now);
      osc.stop(now + 0.12);
    } catch {}
  }

  playVoiceAudio(fileName) {
    if (!fileName) return;
    this.currentAudioFile = fileName;
    this.audioEl.src = `/Mô hình 3D Vĩnh Tràng/audio_v5/${fileName}`;
    this.audioEl.volume = 0.85;
    this.audioEl
      .play()
      .then(() => {
        this.audioPlaying = true;
      })
      .catch(() => {
        this.audioPlaying = false;
      });
  }

  showToast(title, desc, durationMs = 4500, showCheckinBtn = false) {
    const toast = document.getElementById('ritual-toast');
    const tTitle = document.getElementById('toast-title');
    const tDesc = document.getElementById('toast-desc');
    if (!toast || !tTitle || !tDesc) return;
    tTitle.textContent = title;
    const status = checkUGCMilestoneUnlock(this.spiritual, this.completedLessons.size);
    if (showCheckinBtn || status.unlocked) {
      tDesc.innerHTML = `
        <div>${desc}</div>
        <button id="btn-toast-open-ugc" style="margin-top:8px;padding:6px 14px;border-radius:999px;border:1.5px solid #fbe09c;background:linear-gradient(180deg,#d96b27 0%,#9e3810 100%);color:#fff;font-size:12.5px;font-weight:800;cursor:pointer;">
          📸 Đưa ảnh của bạn vào nhận ảnh Check-in Chùa Vĩnh Tràng →
        </button>
      `;
      document.getElementById('btn-toast-open-ugc')?.addEventListener('click', () => {
        toast.classList.remove('visible');
        this.openUGCStudioModal();
      });
    } else {
      tDesc.textContent = desc;
    }
    toast.classList.add('visible');
    if (this.toastTimer) clearTimeout(this.toastTimer);
    this.toastTimer = setTimeout(() => {
      toast.classList.remove('visible');
    }, durationMs);
  }

  /* ========================================================================
     REAL-TIME 3D MOVEMENT & NAVIGATION (D-Pad + Keyboard WASD/Arrows)
     ======================================================================== */
  handleMoveDirection(dir) {
    const dirMap = {
      up: { dx: 0, dz: -1 },
      down: { dx: 0, dz: 1 },
      left: { dx: -1, dz: 0 },
      right: { dx: 1, dz: 0 }
    };
    const vec = dirMap[dir];
    if (!vec) return;

    if (this.world3d) {
      this.world3d.nudgeDirection(dir, 1.55);
      this.playerPos = {
        x: Number(this.world3d.playerPos.x.toFixed(2)),
        z: Number(this.world3d.playerPos.z.toFixed(2)),
        yaw: Number(this.world3d.playerYaw.toFixed(2)),
        moving: true
      };
    } else {
      this.playerPos = stepPlayerMovement(this.playerPos, vec, 1.2);
    }

    const nearest = findNearestStation(this.playerPos);
    if (nearest.distance < 4.8) {
      this.activeStationKey = nearest.station.key;
      this.highlightActiveWalkChip(nearest.station.key);
      if (!this.spiritual.visitedStations.includes(nearest.station.id)) {
        this.spiritual.visitedStations.push(nearest.station.id);
        this.spiritual = recordSpiritualMilestone(
          this.spiritual,
          `Khám phá ${nearest.station.name}`
        );
        this.saveState();
        this.updateUGCMilestoneHUD();
        this.showToast(
          `📍 ${nearest.station.name}`,
          `${nearest.station.subtitle} — Đã mở khóa chụp ảnh Check-in!`,
          4200,
          true
        );
      }
    }
  }

  switchScreen(screenName) {
    this.activeScreen = screenName;
    const shopEl = document.getElementById('shop-screen');
    const lectureEl = document.getElementById('lecture-screen');
    if (shopEl) shopEl.classList.toggle('open', screenName === 'shop');
    if (lectureEl) lectureEl.classList.toggle('open', screenName === 'lecture');

    if (screenName === 'shop') {
      this.renderShopProducts();
    } else if (screenName === 'lecture') {
      this.renderLectureStage();
    }
  }

  updateActionBadges() {
    const map = [
      ['badge-le-phat', this.spiritual.bowCount],
      ['badge-dang-huong', this.spiritual.incenseOfferings],
      ['badge-dang-hoa', this.spiritual.lotusOfferings],
      ['badge-niem-phat', this.spiritual.malaCycles * 108 + this.spiritual.malaBeads]
    ];
    for (const [id, val] of map) {
      const el = document.getElementById(id);
      if (!el) continue;
      if (val > 0) {
        el.style.display = 'inline-block';
        el.textContent = String(val);
      } else {
        el.style.display = 'none';
      }
    }

    const cartSummary = calculateCartSummary(this.cart);
    const cartLabel = document.getElementById('shop-cart-label');
    if (cartLabel) {
      cartLabel.textContent =
        cartSummary.totalCount > 0 ? `Giỏ hàng (${cartSummary.totalCount})` : 'Giỏ hàng';
    }
    this.updateUGCMilestoneHUD();
  }

  updateEquippedTags() {
    const container = document.getElementById('equipped-tags');
    if (!container) return;
    const eq = this.spiritual.equippedItems;
    const charProf = CHARACTER_PROFILES.find((c) => c.key === this.characterModelKey) || CHARACTER_PROFILES[0];
    const chips = [`🙏 ${charProf.name} (${charProf.heightLabel})`];
    if (eq.hat) {
      const item = SHOP_CATALOG.find((p) => p.id === eq.hat);
      if (item) chips.push(`👒 ${item.name}`);
    }
    if (eq.scarf) {
      const item = SHOP_CATALOG.find((p) => p.id === eq.scarf);
      if (item) chips.push(`🧣 ${item.name}`);
    }
    if (eq.hand && eq.hand !== 'trang_hat_bo_de') {
      const item = SHOP_CATALOG.find((p) => p.id === eq.hand);
      chips.push(`🪷 ${item ? item.name : 'Hoa sen thanh tịnh'}`);
    }
    container.innerHTML = chips.map((c) => `<span class="equip-tag-chip">${c}</span>`).join('');
  }

  /* ========================================================================
     THREE.JS 3D PROCEDURAL BUILDERS (3D Shop Kiosk + 20 3D Items + 3 Rigged GLBs)
     ======================================================================== */
  build3DShopKiosk(THREE) {
    const kiosk = new THREE.Group();
    kiosk.name = 'kiosk_cua_hang_3d';

    const woodDark = new THREE.MeshStandardMaterial({ color: 0x6b3e1e, roughness: 0.65 });
    const woodWarm = new THREE.MeshStandardMaterial({ color: 0x9c5e2c, roughness: 0.55 });
    const tileTerracotta = new THREE.MeshStandardMaterial({ color: 0xc85a28, roughness: 0.5 });
    const goldMat = new THREE.MeshStandardMaterial({ color: 0xe6b84c, roughness: 0.3, metalness: 0.65 });
    const pinkLanternMat = new THREE.MeshStandardMaterial({
      color: 0xf78fb3,
      roughness: 0.4,
      emissive: 0xff6b9d,
      emissiveIntensity: 0.45
    });

    // Base platform & wooden counter
    const base = new THREE.Mesh(new THREE.BoxGeometry(1.5, 0.08, 0.9), woodDark);
    base.position.y = 0.04;
    kiosk.add(base);

    const counter = new THREE.Mesh(new THREE.BoxGeometry(1.32, 0.38, 0.48), woodWarm);
    counter.position.set(0, 0.25, 0.14);
    kiosk.add(counter);

    // 4 Timber Columns
    [
      [-0.62, 0.34],
      [0.62, 0.34],
      [-0.62, -0.32],
      [0.62, -0.32]
    ].forEach(([cx, cz]) => {
      const col = new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.05, 1.05, 16), woodDark);
      col.position.set(cx, 0.56, cz);
      kiosk.add(col);
    });

    // Back display shelves with items & central Golden Buddha statue
    const backWall = new THREE.Mesh(new THREE.BoxGeometry(1.24, 0.68, 0.12), woodDark);
    backWall.position.set(0, 0.68, -0.28);
    kiosk.add(backWall);

    const buddha = new THREE.Mesh(new THREE.ConeGeometry(0.11, 0.26, 16), goldMat);
    buddha.position.set(0, 0.72, -0.18);
    kiosk.add(buddha);
    const buddhaHead = new THREE.Mesh(new THREE.SphereGeometry(0.055, 14, 14), goldMat);
    buddhaHead.position.set(0, 0.88, -0.18);
    kiosk.add(buddhaHead);

    // Curved Terracotta Roof + Signboard "Cửa hàng lưu niệm"
    const roof = new THREE.Mesh(new THREE.ConeGeometry(1.18, 0.42, 4), tileTerracotta);
    roof.position.set(0, 1.28, 0);
    roof.rotation.y = Math.PI / 4;
    roof.scale.set(1.25, 1, 0.88);
    kiosk.add(roof);

    const signBoard = new THREE.Mesh(new THREE.BoxGeometry(0.72, 0.24, 0.05), woodDark);
    signBoard.position.set(0, 1.02, 0.36);
    kiosk.add(signBoard);

    // 2 Hanging Pink Lotus Lanterns on Left & Right
    [-0.52, 0.52].forEach((lx) => {
      const lantern = new THREE.Mesh(new THREE.SphereGeometry(0.095, 16, 12), pinkLanternMat);
      lantern.scale.set(1, 0.82, 1);
      lantern.position.set(lx, 0.92, 0.36);
      kiosk.add(lantern);
    });

    // Emerald Glazed Lotus Urn beside the kiosk
    const urn = new THREE.Mesh(
      new THREE.CylinderGeometry(0.14, 0.1, 0.26, 20),
      new THREE.MeshStandardMaterial({ color: 0x2b6e46, roughness: 0.25, metalness: 0.2 })
    );
    urn.position.set(0.82, 0.17, 0.22);
    kiosk.add(urn);

    return kiosk;
  }

  build3DItemMesh(THREE, itemId) {
    if (itemId === 'kiosk_cua_hang_3d' || itemId === 'mo_hinh_cua_hang_3d') {
      const k = this.build3DShopKiosk(THREE);
      k.scale.setScalar(0.55);
      return k;
    }

    const g = new THREE.Group();
    if (itemId === 'non_la_theu_sen') {
      const cone = new THREE.Mesh(
        new THREE.ConeGeometry(0.24, 0.24, 32, 1, true),
        new THREE.MeshStandardMaterial({ color: 0xe8d9b5, roughness: 0.82, side: THREE.DoubleSide })
      );
      cone.position.y = 0.12;
      g.add(cone);
      const lotusDecal = new THREE.Mesh(
        new THREE.SphereGeometry(0.038, 12, 10),
        new THREE.MeshStandardMaterial({ color: 0xf48fb1, roughness: 0.5 })
      );
      lotusDecal.scale.set(1.2, 0.5, 1);
      lotusDecal.position.set(0, 0.12, 0.13);
      g.add(lotusDecal);
    } else if (itemId === 'trang_hat_bo_de' || itemId === 'trang_hat_go') {
      const beadMat = new THREE.MeshStandardMaterial({ color: 0x6b3a1e, roughness: 0.35 });
      const count = 36;
      for (let i = 0; i < count; i++) {
        const a = (2 * Math.PI * i) / count;
        const b = new THREE.Mesh(new THREE.SphereGeometry(0.016, 10, 8), beadMat);
        b.position.set(0.18 * Math.cos(a), 0.18 + 0.18 * Math.sin(a), 0);
        g.add(b);
      }
      const tassel = new THREE.Mesh(
        new THREE.CylinderGeometry(0.008, 0.022, 0.12, 12),
        new THREE.MeshStandardMaterial({ color: 0xc0392b, roughness: 0.8 })
      );
      tassel.position.set(0, -0.05, 0);
      g.add(tassel);
    } else if (itemId === 'so_tay_hoa_sen' || itemId === 'bo_kinh_phap_cu') {
      const book = new THREE.Mesh(
        new THREE.BoxGeometry(0.26, 0.36, 0.045),
        new THREE.MeshStandardMaterial({ color: 0x9b2c2c, roughness: 0.6 })
      );
      book.position.y = 0.2;
      g.add(book);
      const goldBand = new THREE.Mesh(
        new THREE.BoxGeometry(0.015, 0.365, 0.05),
        new THREE.MeshStandardMaterial({ color: 0xe6b84c, metalness: 0.6, roughness: 0.3 })
      );
      goldBand.position.set(0.09, 0.2, 0);
      g.add(goldBand);
      const lotus = new THREE.Mesh(
        new THREE.SphereGeometry(0.055, 14, 12),
        new THREE.MeshStandardMaterial({ color: 0xf78fb3, roughness: 0.4 })
      );
      lotus.scale.set(1.1, 0.9, 0.3);
      lotus.position.set(-0.01, 0.22, 0.025);
      g.add(lotus);
    } else if (itemId === 'hoa_sen_tuoi' || itemId === 'binh_gom_hoa_sen_3d') {
      const vase = new THREE.Mesh(
        new THREE.CylinderGeometry(0.09, 0.07, 0.22, 20),
        new THREE.MeshStandardMaterial({ color: 0x529471, roughness: 0.3 })
      );
      vase.position.y = 0.11;
      g.add(vase);
      const bud = new THREE.Mesh(
        new THREE.ConeGeometry(0.075, 0.16, 16),
        new THREE.MeshStandardMaterial({ color: 0xf48fb1, roughness: 0.45 })
      );
      bud.position.y = 0.3;
      g.add(bud);
    } else {
      // Ornate Golden Lotus Pedestal & Temple Relic
      const relic = new THREE.Mesh(
        new THREE.CylinderGeometry(0.14, 0.18, 0.28, 24),
        new THREE.MeshStandardMaterial({ color: 0xd49b38, roughness: 0.35, metalness: 0.6 })
      );
      relic.position.y = 0.15;
      g.add(relic);
    }
    return g;
  }

  async loadRiggedCharacterGLB(THREE, charKey = 'nu') {
    if (this.cachedGLBCharacters[charKey]) {
      return this.cachedGLBCharacters[charKey].clone();
    }
    const profile = CHARACTER_PROFILES.find((c) => c.key === charKey) || CHARACTER_PROFILES[0];
    try {
      const { GLTFLoader } = await import('three/addons/loaders/GLTFLoader.js');
      const loader = new GLTFLoader();
      const gltf = await loader.loadAsync(profile.glb);
      const model = gltf.scene;
      let bbox = null;
      model.traverse((o) => {
        if (o.isMesh || o.isSkinnedMesh) {
          o.geometry.computeVertexNormals();
          o.geometry.computeBoundingBox();
          bbox = o.geometry.boundingBox;
          o.material = new THREE.MeshStandardMaterial({
            vertexColors: true,
            roughness: 0.85
          });
          o.frustumCulled = false;
        }
      });
      if (bbox) {
        const h = profile.heightMeters || 1.62;
        const scale = h / Math.max(0.1, bbox.max.y - bbox.min.y);
        model.scale.setScalar(scale * 0.72);
        model.position.y = -bbox.min.y * scale * 0.72 - 0.35;
      }
      this.cachedGLBCharacters[charKey] = model;
      return model.clone();
    } catch {
      return null;
    }
  }

  /* ========================================================================
     4 SPIRITUAL ACTION MODALS & INTERACTIONS (Lễ Phật, Dâng hương, Dâng hoa, Niệm Phật)
     ======================================================================== */
  triggerLePhat() {
    const res = performSpiritualAction(this.spiritual, 'LE_PHAT');
    this.spiritual = res.state;
    this.saveState();
    this.updateActionBadges();
    this.world3d?.playPlayerBowAnimation();
    this.playBellTone(216, 3.0);
    this.playVoiceAudio(res.audioFile);
    this.showToast(res.title, res.message, 5200, true);

    const charProf = CHARACTER_PROFILES.find((c) => c.key === this.characterModelKey) || CHARACTER_PROFILES[0];

    this.openModal(
      '🙏 Nghi Thức Lễ Phật Tam Bái — Chánh Điện Vĩnh Tràng',
      `
      <div style="display:grid;grid-template-columns:240px 1fr;gap:18px;align-items:center;">
        <div style="background:#173925;color:#fff8ea;padding:16px;border-radius:20px;text-align:center;">
          <img src="${charProf.previewImg}" alt="${charProf.name}" style="width:130px;height:175px;object-fit:cover;border-radius:14px;border:2px solid rgba(255,215,140,0.45);margin-bottom:8px;" />
          <div style="font-size:16px;font-weight:800;color:#f6cd72;">${charProf.name}</div>
          <div style="font-size:13px;opacity:0.9;margin-top:3px;">Đã lễ: <strong>${this.spiritual.bowCount} lạy</strong></div>
          <div style="margin-top:6px;padding:4px 8px;border-radius:999px;background:rgba(230,178,74,0.25);color:#ffe9b5;font-size:11.5px;font-weight:800;">✓ Đã mở khóa Check-in UGC!</div>
        </div>
        <div style="display:flex;flex-direction:column;gap:10px;">
          <div style="background:#fffdf8;border:1px solid rgba(150,110,60,0.25);padding:11px 15px;border-radius:14px;">
            <strong style="color:#154c2b;">Nhất bái Phật Bảo:</strong>
            <p style="font-size:13.5px;color:#4a2f18;margin-top:3px;">Con xin quy y Phật — Đấng Phúc Trí Viên Mãn, đạo sư chỉ đường sáng suốt.</p>
          </div>
          <div style="background:#fffdf8;border:1px solid rgba(150,110,60,0.25);padding:11px 15px;border-radius:14px;">
            <strong style="color:#154c2b;">Nhị bái Pháp Bảo:</strong>
            <p style="font-size:13.5px;color:#4a2f18;margin-top:3px;">Con xin quy y Pháp — Phương thuốc nhiệm mầu chuyển hóa khổ đau thành an lạc.</p>
          </div>
          <div style="background:#fffdf8;border:1px solid rgba(150,110,60,0.25);padding:11px 15px;border-radius:14px;">
            <strong style="color:#154c2b;">Tam bái Tăng Bảo:</strong>
            <p style="font-size:13.5px;color:#4a2f18;margin-top:3px;">Con xin quy y Tăng — Đoàn thể thanh tịnh hòa hợp cùng tiến tu giải thoát.</p>
          </div>
          <div style="display:flex;gap:10px;margin-top:4px;flex-wrap:wrap;">
            <button id="btn-bow-again" class="product-detail-btn" style="flex:1;">🔔 Lạy thêm 3 lạy (+Thỉnh chuông)</button>
            <button id="btn-open-arhats-from-bow" class="product-detail-btn" style="flex:1;background:#784820;">🏛️ Vào Nội Điện 18 La Hán</button>
            <button id="btn-open-ugc-from-bow" class="product-detail-btn" style="flex:1.2;background:linear-gradient(180deg,#d96b27 0%,#9e3810 100%);">📸 Đưa ảnh vào nhận Check-in</button>
          </div>
        </div>
      </div>
      `
    );

    document.getElementById('btn-bow-again')?.addEventListener('click', () => {
      this.triggerLePhat();
    });
    document.getElementById('btn-open-arhats-from-bow')?.addEventListener('click', () => {
      this.closeModal();
      this.toggleInteriorHallIn3D(true);
    });
    document.getElementById('btn-open-ugc-from-bow')?.addEventListener('click', () => {
      this.openUGCStudioModal();
    });
  }

  triggerDangHuong() {
    const res = performSpiritualAction(this.spiritual, 'DANG_HUONG_STEP');
    this.spiritual = res.state;
    this.saveState();
    this.updateActionBadges();
    this.world3d?.setIncenseBoost(true);
    this.playBellTone(288, 2.0);
    this.playVoiceAudio('s2_thap_nhang.mp3');
    this.renderDangHuongModal();
  }

  renderDangHuongModal() {
    const step = this.spiritual.incenseStep || 1;
    const steps = [
      { n: 1, title: 'Xin 3 nén tâm hương', desc: 'Hương Giới — Hương Định — Hương Tuệ (không thắp quá nhiều gây khói ngạt).' },
      { n: 2, title: 'Châm lửa & Phẩy nhẹ bằng tay', desc: 'Dùng bàn tay phẩy nhẹ cho tắt ngọn lửa, tuyệt đối không dùng miệng thổi.' },
      { n: 3, title: 'Nâng hương ngang trán khấn nguyện', desc: 'Chắp tay nâng hương ngang mày, gửi tâm từ bi cầu quốc thái dân an, gia đạo bình yên.' },
      { n: 4, title: 'Cắm hương ngay ngắn vào lư đồng', desc: 'Cắm ba nén hương thẳng đứng vào lư hương sân Chánh điện và xá 3 xá.' }
    ];

    this.openModal(
      '🔥 Nghi Thức Dâng Hương 4 Bước Chuẩn Oai Nghi',
      `
      <div style="display:flex;flex-direction:column;gap:14px;">
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;">
          ${steps
            .map(
              (s) => `
            <div style="padding:12px;border-radius:16px;border:2px solid ${
              s.n <= step ? '#185832' : 'rgba(140,100,60,0.25)'
            };background:${s.n === step ? '#e5f5eb' : '#fffdf8'};">
              <div style="font-size:13px;font-weight:800;color:${s.n <= step ? '#185832' : '#7a5838'};">Bước ${s.n}/4</div>
              <div style="font-size:15px;font-weight:800;margin:4px 0;">${s.title}</div>
              <div style="font-size:13px;color:#52361c;line-height:1.4;">${s.desc}</div>
            </div>
          `
            )
            .join('')}
        </div>

        <div style="background:#1c3d29;color:#fff8ea;padding:16px 20px;border-radius:18px;display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;">
          <div>
            <div style="font-size:16px;font-weight:800;color:#f6cd72;">Số lần dâng hương viên mãn: ${this.spiritual.incenseOfferings} lần</div>
            <div style="font-size:14px;opacity:0.92;margin-top:3px;">Khói trầm hương đang tỏa nhẹ trước lư đồng sân Chánh điện 3D.</div>
          </div>
          <div style="display:flex;gap:10px;flex-wrap:wrap;">
            <button id="btn-incense-next-step" class="product-detail-btn" style="width:auto;padding:0 22px;background:#d96d38;">
              ${step < 4 ? `Thực hiện Bước ${step + 1}/4 →` : '✨ Dâng hương hoàn mãn (Làm lại)'}
            </button>
            <button id="btn-incense-complete-now" class="product-detail-btn" style="width:auto;padding:0 20px;">
              Cắm hương ngay
            </button>
            <button id="btn-open-ugc-from-incense" class="product-detail-btn" style="width:auto;padding:0 18px;background:#8c4b1e;">
              📸 Chụp ảnh Check-in
            </button>
          </div>
        </div>
      </div>
      `
    );

    document.getElementById('btn-incense-next-step')?.addEventListener('click', () => {
      const r = performSpiritualAction(this.spiritual, 'DANG_HUONG_STEP');
      this.spiritual = r.state;
      this.saveState();
      this.updateActionBadges();
      this.world3d?.setIncenseBoost(true);
      this.playBellTone(288, 1.8);
      this.renderDangHuongModal();
    });

    document.getElementById('btn-incense-complete-now')?.addEventListener('click', () => {
      const r = performSpiritualAction(this.spiritual, 'DANG_HUONG_COMPLETE');
      this.spiritual = r.state;
      this.saveState();
      this.updateActionBadges();
      this.world3d?.setIncenseBoost(true);
      this.playBellTone(216, 2.8);
      this.closeModal();
      this.showToast(r.title, r.message, 5200, true);
    });

    document.getElementById('btn-open-ugc-from-incense')?.addEventListener('click', () => {
      const r = performSpiritualAction(this.spiritual, 'DANG_HUONG_COMPLETE');
      this.spiritual = r.state;
      this.saveState();
      this.updateActionBadges();
      this.openUGCStudioModal();
    });
  }

  triggerDangHoa() {
    const res = performSpiritualAction(this.spiritual, 'DANG_HOA');
    this.spiritual = res.state;
    this.saveState();
    this.updateActionBadges();
    this.updateEquippedTags();
    this.world3d?.placeLotusOfferingIn3D();
    this.playBellTone(324, 2.4);
    this.playVoiceAudio(res.audioFile);
    this.showToast(res.title, res.message, 5200, true);

    this.openModal(
      '🪷 Dâng Hoa Sen Thanh Tịnh & Gửi Lời Nguyện Cầu An',
      `
      <div style="display:grid;grid-template-columns:240px 1fr;gap:18px;align-items:center;">
        <div style="background:#fffdf8;border:1.5px solid rgba(150,110,60,0.28);border-radius:20px;padding:14px;text-align:center;">
          <img src="/Thiết kế giao diện/Vật phẩm 3D/fixed/fixed_binh_gom_hoa_sen.png" alt="Bình gốm hoa sen" style="width:100%;height:170px;object-fit:contain;border-radius:12px;" />
          <div style="font-weight:800;color:#154c2b;margin-top:8px;">Đã dâng: ${this.spiritual.lotusOfferings} bình sen</div>
          <div style="margin-top:6px;padding:4px 8px;border-radius:999px;background:#dcfce7;color:#15803d;font-size:11.5px;font-weight:800;">✓ Đã mở khóa Check-in UGC!</div>
        </div>
        <div style="display:flex;flex-direction:column;gap:10px;">
          <p style="font-size:15px;line-height:1.5;color:#3d2410;">
            Hoa sen mọc từ bùn lầy mà vẫn tinh khôi thơm ngát — tượng trưng cho nhân lành và quả giác ngộ. Xin chọn lời nguyện lành đi kèm đóa sen dâng Phật:
          </p>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
            ${[
              'Nguyện cầu cha mẹ tăng long phước thọ, thân tâm an khang',
              'Nguyện cầu gia đình hòa thuận, con cháu hiếu thảo học hành sáng suốt',
              'Nguyện cầu công việc hanh thông, gặp nhiều thiện duyên lành',
              'Nguyện cầu thế giới hòa bình, muôn loài chúng sanh vơi bớt khổ đau'
            ]
              .map(
                (wish, idx) => `
              <button class="wish-choice-btn" data-wish="${wish}" style="padding:11px 14px;border-radius:14px;border:1.5px solid rgba(24,88,50,0.35);background:${
                idx === 0 ? '#e6f5ec' : '#fffdf8'
              };color:#1b3b26;font-size:13.5px;font-weight:700;text-align:left;cursor:pointer;">
                🪷 ${wish}
              </button>
            `
              )
              .join('')}
          </div>
          <div style="display:flex;gap:10px;margin-top:6px;flex-wrap:wrap;">
            <input id="custom-prayer-input" type="text" placeholder="Hoặc tự viết lời cầu nguyện riêng của bạn..." style="flex:1;min-width:220px;padding:11px 14px;border-radius:12px;border:1.5px solid rgba(140,100,60,0.35);font-size:14px;" />
            <button id="btn-submit-prayer" class="product-detail-btn" style="width:auto;padding:0 22px;">Gửi lên Phật đài</button>
            <button id="btn-open-ugc-from-flower" class="product-detail-btn" style="width:auto;padding:0 18px;background:linear-gradient(180deg,#d96b27 0%,#9e3810 100%);">📸 Đưa ảnh vào nhận Check-in</button>
          </div>
        </div>
      </div>
      `
    );

    document.querySelectorAll('.wish-choice-btn').forEach((btn) => {
      btn.addEventListener('click', () => {
        const w = btn.getAttribute('data-wish');
        const inp = document.getElementById('custom-prayer-input');
        if (inp && w) inp.value = w;
      });
    });

    document.getElementById('btn-submit-prayer')?.addEventListener('click', () => {
      const inp = document.getElementById('custom-prayer-input');
      const text = (inp?.value || 'Nguyện cầu bình an và trí tuệ cho gia quyến').trim();
      this.spiritual.prayers.unshift({ text, time: new Date().toLocaleDateString('vi-VN') });
      this.saveState();
      this.playBellTone(324, 2.5);
      this.closeModal();
      this.showToast('🪷 Đã dâng hoa & lời nguyện', `"${text}"`, 5000, true);
    });

    document.getElementById('btn-open-ugc-from-flower')?.addEventListener('click', () => {
      this.openUGCStudioModal();
    });
  }

  triggerNiemPhat() {
    this.playMokugyoTap();
    this.renderNiemPhatModal();
  }

  renderNiemPhatModal() {
    const chants = [
      'Nam Mô A Di Đà Phật',
      'Nam Mô Quán Thế Âm Bồ Tát',
      'Nam Mô Bổn Sư Thích Ca Mâu Ni Phật',
      'Án Ma Ni Bát Di Hồng'
    ];

    this.openModal(
      '📿 Niệm Phật Lần Chuỗi 108 Hạt Bồ Đề & Chuông Mõ',
      `
      <div style="display:grid;grid-template-columns:280px 1fr;gap:20px;align-items:center;">
        <div class="mala-ring-box">
          <button class="mala-counter-circle" id="btn-pull-bead" title="Bấm để lần từng hạt chuỗi">
            <span class="mala-big-num" id="mala-bead-num">${this.spiritual.malaBeads}/108</span>
            <span class="mala-sub-label">Bấm để lần hạt (+Gõ mõ)</span>
            <span style="font-size:12px;color:#f6cd72;margin-top:4px;">Đã viên mãn: ${this.spiritual.malaCycles} chuỗi</span>
          </button>
          <div style="display:flex;gap:8px;width:100%;">
            <button id="btn-strike-bell" class="product-detail-btn" style="flex:1;height:40px;font-size:14px;background:#8c4b1e;">🔔 Thỉnh chuông</button>
            <button id="btn-auto-108" class="product-detail-btn" style="flex:1;height:40px;font-size:14px;">✨ +10 Hạt nhanh</button>
          </div>
        </div>

        <div style="display:flex;flex-direction:column;gap:12px;">
          <div>
            <div style="font-size:14px;font-weight:700;color:#5c3a1d;margin-bottom:6px;">Chọn hồng danh chư Phật / Bồ Tát:</div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
              ${chants
                .map(
                  (c) => `
                <button class="chant-select-btn" data-chant="${c}" style="padding:10px 12px;border-radius:12px;border:1.5px solid ${
                    this.spiritual.activeChant === c ? '#175631' : 'rgba(130,90,50,0.28)'
                  };background:${
                    this.spiritual.activeChant === c ? '#175631' : '#fffdf8'
                  };color:${this.spiritual.activeChant === c ? '#fff' : '#241409'};font-weight:700;font-size:13.5px;cursor:pointer;">
                  🙏 ${c}
                </button>
              `
                )
                .join('')}
            </div>
          </div>

          <div style="background:#fffdf8;border:1px solid rgba(150,110,60,0.25);padding:14px 16px;border-radius:16px;">
            <div style="font-size:15px;font-weight:800;color:#154c2b;margin-bottom:4px;">Kệ Niệm Phật & Hồi Hướng</div>
            <p style="font-size:14px;line-height:1.55;color:#4a2f18;">
              "A Di Đà Phật thân sắc vàng, tướng tốt không gì sánh ngang. Hào quang chiếu khắp mười phương cõi, nhiếp thụ chúng sanh niệm danh Ngài."
            </p>
          </div>

          <div style="display:flex;gap:10px;">
            <button id="btn-play-chant-audio" class="product-detail-btn" style="flex:1;background:#6e3c16;">
              🎧 Bật/Tắt tiếng niệm Phật đạo tràng
            </button>
          </div>
        </div>
      </div>
      `
    );

    document.getElementById('btn-pull-bead')?.addEventListener('click', () => {
      const r = performSpiritualAction(this.spiritual, 'NIEM_PHAT_BEAD', { count: 1 });
      this.spiritual = r.state;
      this.saveState();
      this.updateActionBadges();
      this.playMokugyoTap();
      if (this.spiritual.malaBeads === 0 || this.spiritual.malaBeads % 27 === 0) {
        this.playBellTone(216, 2.5);
      }
      this.renderNiemPhatModal();
    });

    document.getElementById('btn-auto-108')?.addEventListener('click', () => {
      const r = performSpiritualAction(this.spiritual, 'NIEM_PHAT_BEAD', { count: 10 });
      this.spiritual = r.state;
      this.saveState();
      this.updateActionBadges();
      this.playBellTone(260, 2.2);
      this.renderNiemPhatModal();
    });

    document.getElementById('btn-strike-bell')?.addEventListener('click', () => {
      const r = performSpiritualAction(this.spiritual, 'RING_BELL');
      this.spiritual = r.state;
      this.saveState();
      this.playBellTone(196, 3.4);
    });

    document.querySelectorAll('.chant-select-btn').forEach((btn) => {
      btn.addEventListener('click', () => {
        const chant = btn.getAttribute('data-chant');
        if (chant) {
          this.spiritual.activeChant = chant;
          this.saveState();
          this.renderNiemPhatModal();
        }
      });
    });

    document.getElementById('btn-play-chant-audio')?.addEventListener('click', () => {
      if (this.audioPlaying) {
        this.audioEl.pause();
        this.audioPlaying = false;
      } else {
        this.playVoiceAudio('niem_phat_xa.mp3');
      }
    });
  }

  /* ========================================================================
     CỬA HÀNG LƯU NIỆM & VẬT PHẨM 3D RENDERING (Reference Image 2)
     ======================================================================== */
  renderShopProducts() {
    const grid = document.getElementById('shop-products-grid');
    if (!grid) return;

    document.querySelectorAll('.shop-tab-pill').forEach((tabBtn) => {
      tabBtn.classList.toggle('active', tabBtn.getAttribute('data-shop-tab') === this.shopTab);
    });

    const items = filterShopCatalog(this.shopTab);
    grid.innerHTML = items
      .map((item) => {
        const thumbHTML = item.cropStyle
          ? `<div class="product-thumb-crop" style="background-image:url('${item.cropStyle.bgImage}');background-size:${item.cropStyle.bgSize};background-position:${item.cropStyle.bgPos};"></div>`
          : `<img class="product-thumb-img" src="${item.image}" alt="${item.name}" />`;

        return `
        <article class="shop-product-card" data-product-id="${item.id}">
          <div class="product-thumb-box">
            ${thumbHTML}
            <span class="product-price-tag">${item.price.toLocaleString('vi-VN')}đ</span>
          </div>
          <h2 class="product-card-title">${item.name}</h2>
          <div class="product-delivery-row">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="1" y="4" width="15" height="12" rx="1"/>
              <polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/>
              <circle cx="5.5" cy="18.5" r="2.5"/>
              <circle cx="18.5" cy="18.5" r="2.5"/>
            </svg>
            <span>${item.deliveryText}</span>
          </div>
          <button class="product-detail-btn" data-detail-id="${item.id}">Xem chi tiết</button>
        </article>
      `;
      })
      .join('');

    grid.querySelectorAll('[data-detail-id]').forEach((btn) => {
      btn.addEventListener('click', () => {
        const id = btn.getAttribute('data-detail-id');
        if (id) this.openProductDetailModal(id);
      });
    });

    this.updateActionBadges();
  }

  openProductDetailModal(productId, previewCharKey = null) {
    const item = SHOP_CATALOG.find((p) => p.id === productId);
    if (!item) return;

    const activeChar = previewCharKey || this.characterModelKey;
    const isEquipped = Object.values(this.spiritual.equippedItems).includes(item.id);

    this.openModal(
      `🪷 ${item.name} — Xem Mô Hình 3D & Thử Lên 3 Nhân Vật (Nam · Nữ · Trẻ Em)`,
      `
      <div style="display:grid;grid-template-columns:1.1fr 1fr;gap:20px;align-items:start;">
        <div>
          <div class="viewer3d-stage" id="product-3d-stage" style="height:300px;">
            <canvas class="viewer3d-canvas" id="product-3d-canvas"></canvas>
            <div style="position:absolute;top:8px;left:10px;display:flex;gap:6px;">
              ${CHARACTER_PROFILES.map(
                (c) => `
                <button class="tryon-char-btn" data-char="${c.key}" style="padding:4px 10px;border-radius:999px;border:1px solid #165632;background:${
                  activeChar === c.key ? '#165632' : 'rgba(255,255,255,0.92)'
                };color:${
                  activeChar === c.key ? '#fff' : '#165632'
                };font-size:11.5px;font-weight:800;cursor:pointer;">
                  Thử: ${c.name.split('(')[0].trim()} (${c.heightLabel})
                </button>
              `
              ).join('')}
            </div>
            <div style="position:absolute;bottom:8px;left:10px;right:10px;display:flex;justify-content:space-between;align-items:center;pointer-events:none;">
              <span style="background:rgba(22,68,40,0.9);color:#fff;font-size:11.5px;font-weight:700;padding:4px 10px;border-radius:999px;">
                Xoay 360° trực tiếp · Khớp tỷ lệ nhân vật GLB
              </span>
              <span style="background:rgba(90,52,20,0.88);color:#ffe9c2;font-size:11.5px;font-weight:700;padding:4px 10px;border-radius:999px;">
                ${item.price.toLocaleString('vi-VN')} VNĐ
              </span>
            </div>
          </div>
          <div style="display:flex;gap:8px;margin-top:10px;">
            <button id="btn-equip-3d-item" class="product-detail-btn" style="flex:1;height:42px;font-size:14px;background:${
              isEquipped ? '#8a3918' : '#185832'
            };">
              ${isEquipped ? '✓ Đang gắn trên nhân vật / Bàn thờ' : '✨ Gắn 3D lên nhân vật / Dâng lễ'}
            </button>
            <a href="${item.zip}" download style="display:inline-flex;align-items:center;justify-content:center;padding:0 14px;height:42px;border-radius:999px;background:#f0dbc0;color:#4e3016;font-size:13px;font-weight:700;text-decoration:none;">
              📦 Tải Coohom .zip
            </a>
          </div>
        </div>

        <div style="display:flex;flex-direction:column;gap:10px;">
          <div style="font-size:22px;font-weight:800;color:#144929;">${item.name}</div>
          <div style="font-size:14.5px;color:#5b3b1e;font-weight:600;">${item.subtitle}</div>
          <div style="font-size:20px;font-weight:800;color:#b84518;">${item.price.toLocaleString('vi-VN')} VNĐ <span style="font-size:13px;font-weight:600;color:#175832;">(🚚 Giao tận nhà toàn quốc)</span></div>

          <div style="background:#fffdf8;border:1px solid rgba(150,110,60,0.25);border-radius:14px;padding:12px 14px;font-size:13.5px;line-height:1.5;">
            <div><strong>Kích thước chuẩn Coohom:</strong> ${item.dimensions}</div>
            <div style="margin-top:4px;"><strong>Chất liệu:</strong> ${item.material}</div>
            <div style="margin-top:6px;color:#3d2410;"><strong>Ý nghĩa tâm linh & văn hóa:</strong> ${item.meaning}</div>
          </div>

          <div style="display:flex;gap:10px;margin-top:6px;">
            <button id="btn-add-to-cart-modal" class="shop-cart-cta" style="margin:0;height:48px;font-size:17px;">
              🛒 Thêm vào giỏ hàng (Thỉnh về nhà)
            </button>
          </div>
        </div>
      </div>
      `
    );

    this.mountInteractive3DStage('product-3d-canvas', {
      item,
      charKey: previewCharKey
    });

    document.querySelectorAll('.tryon-char-btn').forEach((btn) => {
      btn.addEventListener('click', () => {
        const ck = btn.getAttribute('data-char') || 'nu';
        this.characterModelKey = ck;
        this.saveState();
        this.updateEquippedTags();
        this.openProductDetailModal(productId, ck);
      });
    });

    document.getElementById('btn-equip-3d-item')?.addEventListener('click', () => {
      const r = performSpiritualAction(this.spiritual, 'EQUIP_ITEM', {
        slot: item.equipSlot || 'hand',
        itemKey: item.id
      });
      this.spiritual = r.state;
      this.saveState();
      this.updateEquippedTags();
      this.playBellTone(320, 1.5);
      this.openProductDetailModal(productId, activeChar);
      this.showToast('✨ Đã cập nhật vật phẩm 3D', `Đã gắn "${item.name}" lên nhân vật Phật tử.`, 3600);
    });

    document.getElementById('btn-add-to-cart-modal')?.addEventListener('click', () => {
      this.cart = addToCart(this.cart, item.id, 1);
      this.saveState();
      this.updateActionBadges();
      this.closeModal();
      this.openCartModal();
    });
  }

  openCartModal() {
    const summary = calculateCartSummary(this.cart);

    this.openModal(
      '🛒 Giỏ Hàng Lưu Niệm & Đặt Giao Tận Nhà (COD)',
      `
      <div style="display:grid;grid-template-columns:1.1fr 1fr;gap:20px;align-items:start;">
        <div style="display:flex;flex-direction:column;gap:10px;">
          <div style="font-size:16px;font-weight:800;color:#144929;">Danh sách vật phẩm đã chọn (${summary.totalCount})</div>
          ${
            this.cart.length === 0
              ? `<div style="padding:24px;background:#fffdf8;border-radius:16px;text-align:center;color:#6b4a2b;">Giỏ hàng đang trống. Mời đạo hữu chọn món quà lưu niệm tại cửa hàng.</div>`
              : this.cart
                  .map(
                    (c) => `
                <div style="display:flex;align-items:center;justify-content:space-between;background:#fffdf8;border:1px solid rgba(150,110,60,0.25);padding:10px 14px;border-radius:14px;gap:10px;">
                  <div>
                    <div style="font-weight:800;font-size:15px;">${c.name}</div>
                    <div style="font-size:13px;color:#7a4e25;">${c.price.toLocaleString('vi-VN')}đ × ${c.qty}</div>
                  </div>
                  <div style="display:flex;align-items:center;gap:6px;">
                    <button class="cart-qty-btn" data-id="${c.id}" data-delta="-1" style="width:28px;height:28px;border-radius:8px;border:1px solid #8a623c;background:#f5e6cf;cursor:pointer;font-weight:800;">-</button>
                    <span style="min-width:22px;text-align:center;font-weight:800;">${c.qty}</span>
                    <button class="cart-qty-btn" data-id="${c.id}" data-delta="1" style="width:28px;height:28px;border-radius:8px;border:1px solid #8a623c;background:#f5e6cf;cursor:pointer;font-weight:800;">+</button>
                  </div>
                </div>
              `
                  )
                  .join('')
          }

          <div style="background:#f3e3c9;padding:12px 16px;border-radius:14px;font-size:14px;">
            <div style="display:flex;justify-content:space-between;"><span>Tạm tính:</span><strong>${summary.subtotal.toLocaleString('vi-VN')}đ</strong></div>
            <div style="display:flex;justify-content:space-between;margin-top:4px;"><span>Phí vận chuyển (Miễn phí đơn từ 300k):</span><strong>${summary.shippingFee.toLocaleString('vi-VN')}đ</strong></div>
            <div style="display:flex;justify-content:space-between;margin-top:6px;font-size:17px;color:#a53b16;"><span>Tổng thanh toán khi nhận hàng:</span><strong>${summary.grandTotal.toLocaleString('vi-VN')}đ</strong></div>
          </div>
        </div>

        <form id="checkout-order-form" style="background:#fffdf8;border:1px solid rgba(150,110,60,0.28);padding:16px;border-radius:18px;display:flex;flex-direction:column;gap:10px;">
          <div style="font-size:16px;font-weight:800;color:#144929;">Thông tin nhận quà tận nhà</div>
          <input id="order-name" type="text" placeholder="Họ và tên người nhận *" required style="padding:10px 12px;border-radius:10px;border:1px solid #bfa07a;font-size:14px;" />
          <input id="order-phone" type="tel" placeholder="Số điện thoại liên hệ (VD: 0912345678) *" required style="padding:10px 12px;border-radius:10px;border:1px solid #bfa07a;font-size:14px;" />
          <textarea id="order-address" rows="2" placeholder="Địa chỉ giao hàng chi tiết (Số nhà, Phường/Xã, Quận/Huyện, Tỉnh/TP) *" required style="padding:10px 12px;border-radius:10px;border:1px solid #bfa07a;font-size:14px;"></textarea>
          <input id="order-note" type="text" placeholder="Lời chúc / Ghi chú gói quà (tùy chọn)" style="padding:10px 12px;border-radius:10px;border:1px solid #bfa07a;font-size:14px;" />
          <div id="order-error-msg" style="color:#b91c1c;font-size:13px;font-weight:700;display:none;"></div>
          <button type="submit" class="shop-cart-cta" style="margin:4px 0 0;height:48px;font-size:17px;max-width:none;">
            🚚 Xác nhận đặt giao tận nhà
          </button>
        </form>
      </div>
      `
    );

    document.querySelectorAll('.cart-qty-btn').forEach((btn) => {
      btn.addEventListener('click', () => {
        const id = btn.getAttribute('data-id');
        const delta = Number(btn.getAttribute('data-delta') || 0);
        if (id) {
          this.cart = updateCartQuantity(this.cart, id, delta);
          this.saveState();
          this.updateActionBadges();
          this.openCartModal();
        }
      });
    });

    document.getElementById('checkout-order-form')?.addEventListener('submit', (e) => {
      e.preventDefault();
      if (this.cart.length === 0) return;
      const form = {
        name: document.getElementById('order-name')?.value,
        phone: document.getElementById('order-phone')?.value,
        address: document.getElementById('order-address')?.value,
        note: document.getElementById('order-note')?.value
      };
      const check = validateOrderForm(form);
      const errEl = document.getElementById('order-error-msg');
      if (!check.valid) {
        if (errEl) {
          errEl.style.display = 'block';
          errEl.textContent = Object.values(check.errors).join(' ');
        }
        return;
      }
      const orderCode = `VT-${Date.now().toString().slice(-6)}`;
      this.orders.unshift({
        code: orderCode,
        ...form,
        items: [...this.cart],
        total: calculateCartSummary(this.cart).grandTotal,
        createdAt: new Date().toLocaleString('vi-VN')
      });
      this.cart = [];
      this.saveState();
      this.updateActionBadges();
      this.playBellTone(288, 2.5);
      this.openModal(
        '🎉 Đặt Quà Lưu Niệm Thành Công',
        `
        <div style="text-align:center;padding:14px;">
          <div style="font-size:22px;font-weight:800;color:#144929;margin-bottom:8px;">Mã đơn thỉnh: ${orderCode}</div>
          <p style="font-size:15px;color:#4a2f18;line-height:1.5;max-width:520px;margin:0 auto 16px;">
            Cửa hàng lưu niệm Chùa Vĩnh Tràng đã ghi nhận đơn quà của đạo hữu <strong>${form.name}</strong> (${form.phone}). Quà sẽ được đóng gói trang trọng và giao tận nhà tại: <em>${form.address}</em>.
          </p>
          <button id="btn-done-order" class="product-detail-btn" style="max-width:260px;">Hoan hỷ trở về</button>
        </div>
        `
      );
      document.getElementById('btn-done-order')?.addEventListener('click', () => this.closeModal());
    });
  }

  /* ========================================================================
     GIẢNG ĐƯỜNG PHẬT PHÁP RENDERING (Reference Image 3 & Lesson Study Stack)
     ======================================================================== */
  renderLectureStage() {
    const stage = document.getElementById('lecture-center-stage');
    if (!stage) return;

    document.querySelectorAll('.lecture-dock-tab').forEach((btn) => {
      btn.classList.toggle('active', btn.getAttribute('data-lecture-tab') === this.lectureTab);
    });

    const lesson =
      LECTURE_LESSONS.find((l) => l.id === this.activeLessonId) || LECTURE_LESSONS[0];

    if (this.lectureTab === 'listen') {
      stage.innerHTML = `
        <div class="lesson-study-stack" style="max-width:680px;margin-top:auto;margin-bottom:14px;">
          <div class="lesson-cream-card" style="background:rgba(255,246,229,0.95);border:2px solid #C9962E;">
            <div style="display:flex;justify-content:space-between;align-items:center;gap:14px;flex-wrap:wrap;">
              <div>
                <div style="font-size:12.5px;font-weight:800;color:#1C5A34;text-transform:uppercase;letter-spacing:0.04em;">🎧 Pháp Âm Giảng Đường Vĩnh Tràng</div>
                <div style="font-size:20px;font-weight:800;color:#4A3222;margin-top:3px;">${lesson.title}</div>
                <div style="font-size:13.5px;color:#6b4c32;margin-top:2px;">Nguồn: ${lesson.sourceBook} · Thời lượng: ${lesson.duration}</div>
              </div>
              <button id="btn-toggle-lecture-listen" class="product-detail-btn" style="width:auto;padding:0 22px;height:44px;background:${this.audioPlaying ? '#C96F4A' : '#1C5A34'};">
                ${this.audioPlaying ? '❚❚ Tạm dừng pháp âm' : '▶ Nghe giảng ngay'}
              </button>
            </div>
            <p style="font-size:14.5px;color:#4A3222;margin-top:10px;line-height:1.55;">
              "${lesson.summary[0]}"
            </p>
          </div>
        </div>
      `;

      document.getElementById('btn-toggle-lecture-listen')?.addEventListener('click', () => {
        if (this.audioPlaying) {
          this.audioEl.pause();
          this.audioPlaying = false;
        } else {
          this.playVoiceAudio(lesson.audio);
          this.audioPlaying = true;
        }
        this.renderLectureStage();
      });
      return;
    }

    if (this.lectureTab === 'lesson') {
      stage.innerHTML = `
        <div class="lesson-study-stack">
          <div class="lesson-cream-card lesson-header-card">
            <div class="lesson-card-big-title">${lesson.title}</div>
            <div class="lesson-card-meta">Bài ${lesson.id} · ${lesson.duration} · Nguồn: ${lesson.sourceBook}</div>
            <button class="lesson-listen-btn" id="btn-lesson-play-audio">
              <span style="display:inline-flex;align-items:center;gap:10px;">
                <span>🎧</span>
                <span>${this.audioPlaying ? 'Đang nghe bài học (Bấm để dừng)' : 'Nghe bài học'}</span>
              </span>
              <span class="play-circle">${this.audioPlaying ? '❚❚' : '▶'}</span>
            </button>
          </div>

          <div class="lesson-cream-card">
            <div class="lesson-summary-lead">${lesson.summary[0]}</div>
            <ul class="lesson-bullet-list">
              ${lesson.summary.slice(1).map((s) => `<li>${s}</li>`).join('')}
            </ul>
            <div class="lesson-example-box">
              <strong>Ứng dụng tại Chùa Vĩnh Tràng:</strong> ${lesson.example}
            </div>
          </div>

          <div class="lesson-cream-card">
            <div class="lesson-quiz-heading">${lesson.quiz.question}</div>
            <div class="lesson-quiz-options">
              ${lesson.quiz.options
                .map(
                  (opt, idx) => `
                <button class="lesson-quiz-option ${this.selectedQuizOption === idx ? 'selected' : ''}" data-quiz-idx="${idx}">
                  <span class="radio-dot"></span>
                  <span>${opt}</span>
                </button>
              `
                )
                .join('')}
            </div>
            ${
              this.quizFeedback
                ? `<div style="margin-top:10px;padding:10px 14px;border-radius:12px;background:${
                    this.quizFeedback.correct ? '#dff3e5' : '#fce8e6'
                  };color:${
                    this.quizFeedback.correct ? '#14532d' : '#991b1b'
                  };font-size:14px;font-weight:700;">
                    ${this.quizFeedback.correct ? '✓ Chính xác! ' : '💡 Giải thích: '}${this.quizFeedback.explanation}
                  </div>`
                : ''
            }
          </div>

          <button class="lesson-next-green-btn" id="btn-lesson-continue">
            <span>Tiếp tục</span>
            <span>→</span>
          </button>
        </div>
      `;

      document.getElementById('btn-lesson-play-audio')?.addEventListener('click', () => {
        if (this.audioPlaying) {
          this.audioEl.pause();
          this.audioPlaying = false;
        } else {
          this.playVoiceAudio(lesson.audio);
          this.audioPlaying = true;
        }
        this.renderLectureStage();
      });

      stage.querySelectorAll('[data-quiz-idx]').forEach((btn) => {
        btn.addEventListener('click', () => {
          this.selectedQuizOption = Number(btn.getAttribute('data-quiz-idx') || 0);
          this.quizFeedback = gradeLessonQuiz(lesson.id, this.selectedQuizOption);
          if (this.quizFeedback.correct) {
            this.completedLessons.add(lesson.id);
            this.saveState();
            this.playBellTone(324, 1.8);
          }
          this.renderLectureStage();
        });
      });

      document.getElementById('btn-lesson-continue')?.addEventListener('click', () => {
        this.completedLessons.add(lesson.id);
        this.saveState();
        const idx = LECTURE_LESSONS.findIndex((l) => l.id === lesson.id);
        const nextLesson = LECTURE_LESSONS[(idx + 1) % LECTURE_LESSONS.length];
        this.activeLessonId = nextLesson.id;
        this.activePathId = nextLesson.pathId;
        this.selectedQuizOption = nextLesson.quiz.correctIndex;
        this.quizFeedback = null;
        this.playBellTone(288, 2.0);
        this.renderLectureStage();
      });
      return;
    }

    if (this.lectureTab === 'package') {
      const lessonsInPath = getLessonsByPath(this.activePathId);
      stage.innerHTML = `
        <div class="lesson-study-stack" style="max-width:860px;">
          <div class="lesson-cream-card">
            <div style="display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:6px;">
              <div style="font-size:23px;font-weight:800;color:#144929;">
                4 Gói Học · 24 Bài Học Phật Pháp & 10 Giáo Trình Kinh Điển
              </div>
              <button id="btn-open-pdf-library-inline" class="product-detail-btn" style="width:auto;padding:0 16px;height:36px;font-size:13.5px;background:#8c4b1e;">
                📚 Mở 10 sách Giáo trình Phật học (.PDF)
              </button>
            </div>
            <p style="font-size:14px;color:#5b3a1d;margin-bottom:12px;">
              Đã hoàn thành: <strong>${this.completedLessons.size}/24 bài học</strong> — Biên soạn sát theo <em>Phật Học Phổ Thông</em> (HT. Thích Thiện Hoa), <em>Đức Phật Dạy Những Gì</em> (HT. Walpola Rahula), <em>Phương Pháp Thiền Căn Bản</em> (Ajahn Brahm) & <em>Tích Truyện Pháp Cú</em>.
            </p>
            <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:14px;">
              ${LECTURE_PATHS.map(
                (p) => `
                <button class="path-tab-btn" data-path-id="${p.id}" style="padding:11px;border-radius:16px;border:2px solid ${
                  this.activePathId === p.id ? '#165632' : 'rgba(130,90,50,0.25)'
                };background:${
                  this.activePathId === p.id ? '#165632' : '#fffdf8'
                };color:${
                  this.activePathId === p.id ? '#fff' : '#241409'
                };text-align:left;cursor:pointer;">
                  <div style="font-size:12px;font-weight:800;opacity:0.85;">${p.code}</div>
                  <div style="font-size:14px;font-weight:800;margin-top:3px;">${p.title}</div>
                </button>
              `
              ).join('')}
            </div>

            <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:10px;">
              ${lessonsInPath
                .map((l) => {
                  const done = this.completedLessons.has(l.id);
                  return `
                  <button class="select-lesson-card" data-lesson-id="${l.id}" style="padding:11px 14px;border-radius:14px;border:1.5px solid ${
                    this.activeLessonId === l.id ? '#165632' : 'rgba(130,90,50,0.25)'
                  };background:#fffdf8;color:#241409;text-align:left;cursor:pointer;display:flex;justify-content:space-between;align-items:center;gap:10px;">
                    <div>
                      <div style="font-size:12px;font-weight:800;color:#7a4e25;">Bài ${l.id} · ${l.sourceBook}</div>
                      <div style="font-size:14.5px;font-weight:800;margin-top:2px;">${l.title}</div>
                    </div>
                    <span style="padding:4px 10px;border-radius:999px;background:${
                      done ? '#dcfce7' : '#f3e4cb'
                    };color:${done ? '#15803d' : '#6b4522'};font-size:12px;font-weight:800;flex-shrink:0;">
                      ${done ? '✓ Đã học' : 'Học ngay'}
                    </span>
                  </button>
                `;
                })
                .join('')}
            </div>
          </div>
        </div>
      `;

      document.getElementById('btn-open-pdf-library-inline')?.addEventListener('click', () => {
        this.openTextbooksModal();
      });

      stage.querySelectorAll('.path-tab-btn').forEach((btn) => {
        btn.addEventListener('click', () => {
          const pid = btn.getAttribute('data-path-id');
          if (pid) {
            this.activePathId = pid;
            this.renderLectureStage();
          }
        });
      });

      stage.querySelectorAll('.select-lesson-card').forEach((btn) => {
        btn.addEventListener('click', () => {
          const lid = btn.getAttribute('data-lesson-id');
          if (lid) {
            this.activeLessonId = lid;
            this.lectureTab = 'lesson';
            this.quizFeedback = null;
            this.renderLectureStage();
          }
        });
      });
    }
  }

  openTextbooksModal() {
    this.openModal(
      '📚 Tủ Sách Giáo Trình Phật Học Kinh Điển (10 Ấn Bản PDF Nguyên Bản)',
      `
      <div style="display:flex;flex-direction:column;gap:10px;">
        <p style="font-size:14px;color:#4a2f18;">
          Toàn bộ 24 bài học trong Giảng đường Phật pháp được nghiên cứu và trích lục từ 10 bộ giáo trình Phật học kinh điển dưới đây:
        </p>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
          ${DHARMA_TEXTBOOKS.map(
            (b) => `
            <div style="background:#fffdf8;border:1.5px solid rgba(140,100,60,0.28);border-radius:14px;padding:12px 14px;display:flex;flex-direction:column;justify-content:space-between;gap:8px;">
              <div>
                <div style="font-size:15px;font-weight:800;color:#144929;">${b.title}</div>
                <div style="font-size:12.5px;font-weight:700;color:#8c4b1e;margin-top:2px;">Tác giả / Dịch giả: ${b.author}</div>
                <p style="font-size:13px;color:#4a2f18;margin-top:5px;line-height:1.42;">${b.coreTeachings}</p>
              </div>
              <a href="${b.pdfPath}" target="_blank" download style="display:inline-flex;align-items:center;justify-content:center;height:36px;border-radius:999px;background:#165632;color:#fff;font-size:13px;font-weight:700;text-decoration:none;">
                📖 Đọc / Tải sách PDF nguyên bản
              </a>
            </div>
          `
          ).join('')}
        </div>
      </div>
      `
    );
  }

  openAudioRecordingsModal() {
    this.openModal(
      '🎧 Thư Viện Bài Thu Âm Pháp Âm & Kệ Tụng Chùa Vĩnh Tràng',
      `
      <div style="display:flex;flex-direction:column;gap:10px;">
        <p style="font-size:14.5px;color:#4a2f18;">
          Chọn bài thu âm thuyết minh hành hương hoặc pháp âm tụng niệm để lắng nghe:
        </p>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
          ${AUDIO_LIBRARY.map(
            (track) => `
            <button class="audio-track-btn" data-file="${track.file}" style="padding:12px 16px;border-radius:14px;border:1.5px solid ${
              this.currentAudioFile === track.file && this.audioPlaying
                ? '#165632'
                : 'rgba(140,100,60,0.28)'
            };background:#fffdf8;color:#241409;text-align:left;cursor:pointer;display:flex;align-items:center;justify-content:space-between;gap:10px;">
              <div>
                <div style="font-weight:800;font-size:14.5px;">${track.title}</div>
                <div style="font-size:12.5px;color:#7a5229;margin-top:2px;">Thời lượng: ${track.duration}</div>
              </div>
              <span style="width:34px;height:34px;border-radius:50%;background:#165632;color:#fff;display:flex;align-items:center;justify-content:center;font-size:13px;flex-shrink:0;">▶</span>
            </button>
          `
          ).join('')}
        </div>
      </div>
      `
    );

    document.querySelectorAll('.audio-track-btn').forEach((btn) => {
      btn.addEventListener('click', () => {
        const file = btn.getAttribute('data-file');
        if (file) {
          this.playVoiceAudio(file);
          this.closeModal();
          this.renderLectureStage();
          this.showToast('🎧 Đang phát bài thu âm', btn.textContent?.trim() || file, 3800);
        }
      });
    });
  }

  /* ========================================================================
     MILESTONE-UNLOCKED USER-PHOTO UPLOAD UGC CHECK-IN STUDIO
     ("Ảnh UGC chỉ chụp khi hoàn thành gì đó, người dùng đưa ảnh vào rồi hệ thống đẩy ảnh check-in với Chùa Vĩnh Tràng")
     ======================================================================== */
  openUGCStudioModal() {
    const milestoneStatus = checkUGCMilestoneUnlock(this.spiritual, this.completedLessons.size);
    let selectedCharMode = 'family_3'; // 'family_3' | 'nu' | 'nam' | 'tre_em'
    let selectedBackdropId = 'live_3d_view'; // 'live_3d_view' or any UGC_BACKDROPS.id
    let selectedPoseId = 'chap_tay_le_phat';

    const live3DSnapshot = this.world3d?.captureSnapshotDataURL?.() || null;

    this.openModal(
      '📸 Check-in Chùa Vĩnh Tràng — Đưa Ảnh Của Bạn Vào Nhận Ảnh Check-in Kỷ Niệm',
      `
      <div style="display:flex;flex-direction:column;gap:14px;">
        <!-- Milestone Unlock Status Banner -->
        <div id="ugc-milestone-banner" style="padding:12px 16px;border-radius:16px;border:2px solid ${
          milestoneStatus.unlocked ? '#165632' : '#d97706'
        };background:${
          milestoneStatus.unlocked
            ? 'linear-gradient(90deg,#dcfce7 0%,#f0fdf4 100%)'
            : 'linear-gradient(90deg,#fef3c7 0%,#fffbeb 100%)'
        };display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;">
          <div>
            <div style="font-size:15px;font-weight:800;color:${
              milestoneStatus.unlocked ? '#14532d' : '#92400e'
            };">
              ${
                milestoneStatus.unlocked
                  ? `✅ ĐÃ MỞ KHÓA CHECK-IN UGC! Thành tựu vừa hoàn thành: "${milestoneStatus.latestMilestone}" (${milestoneStatus.totalCompleted} hoạt động)`
                  : '🔒 CHƯA MỞ KHÓA CHECK-IN: Ảnh UGC chỉ chụp khi bạn hoàn thành ít nhất 1 nghi lễ hoặc khám phá điểm đến tại chùa!'
              }
            </div>
            <div style="font-size:13px;color:#4a2f18;margin-top:2px;">
              ${
                milestoneStatus.unlocked
                  ? 'Hãy tải ảnh cá nhân / gia đình của bạn lên ở mục 1 bên phải — hệ thống sẽ tự động ghép và đẩy ảnh Check-in Chùa Vĩnh Tràng cho bạn.'
                  : 'Bấm 1 trong các hoạt động tâm linh bên cạnh để hoàn thành ngay và mở khóa ghép ảnh Check-in:'
              }
            </div>
          </div>
          ${
            !milestoneStatus.unlocked
              ? `
            <div style="display:flex;gap:8px;flex-wrap:wrap;">
              <button id="btn-ugc-quick-bow" class="product-detail-btn" style="width:auto;padding:0 14px;height:36px;font-size:12.5px;">🙏 Lễ Phật mở khóa ngay</button>
              <button id="btn-ugc-quick-lotus" class="product-detail-btn" style="width:auto;padding:0 14px;height:36px;font-size:12.5px;background:#8c4b1e;">🪷 Dâng hoa sen mở khóa</button>
            </div>
          `
              : `<span style="padding:5px 12px;border-radius:999px;background:#165632;color:#fff;font-size:12px;font-weight:800;">🌟 Sẵn sàng xuất ảnh Check-in</span>`
          }
        </div>

        <div style="display:grid;grid-template-columns:1.15fr 1fr;gap:18px;align-items:start;">
          <!-- Left: System Output Check-in Composite Canvas -->
          <div>
            <div style="position:relative;">
              <canvas id="ugc-composite-canvas" width="760" height="500" style="width:100%;height:auto;border-radius:18px;border:2.5px solid #c8963e;box-shadow:0 12px 30px rgba(0,0,0,0.32);background:#1b3b26;"></canvas>
              <div id="ugc-output-status-badge" style="position:absolute;top:12px;right:12px;background:rgba(22,86,50,0.92);color:#fff;padding:5px 12px;border-radius:999px;font-size:12px;font-weight:800;border:1px solid #f6cd72;">
                ${
                  this.uploadedUserPhotoDataUrl
                    ? '✓ Đã ghép ảnh của bạn vào Chùa Vĩnh Tràng'
                    : '📷 Chờ đưa ảnh của bạn vào...'
                }
              </div>
            </div>

            <div style="display:flex;gap:10px;margin-top:10px;">
              <button id="btn-ugc-download" class="product-detail-btn" style="flex:1;height:44px;font-size:14.5px;background:#165632;">
                💾 Nhận & Tải ảnh Check-in (.PNG)
              </button>
              <button id="btn-ugc-publish" class="shop-cart-cta" style="flex:1;margin:0;height:44px;font-size:15px;">
                🌟 Đăng lên Lưu Bút Chùa Vĩnh Tràng
              </button>
            </div>
          </div>

          <!-- Right: Step 1 Upload User Photo + Step 2 Backdrop + Step 3 Companion & Blessing -->
          <div style="display:flex;flex-direction:column;gap:10px;">
            <!-- STEP 1: USER UPLOADS THEIR PHOTO -->
            <div class="ugc-upload-dropzone" id="ugc-upload-dropzone">
              <div style="font-size:14px;font-weight:800;color:#144929;">
                1. 📤 Đưa ảnh của bạn vào để hệ thống đẩy ảnh Check-in Chùa Vĩnh Tràng
              </div>
              <p style="font-size:12.5px;color:#3d2410;margin:4px 0 8px;">
                Chọn ảnh chân dung / selfie từ máy của bạn (JPG, PNG, WEBP) để ghép vào khung sen vàng trước Chùa Vĩnh Tràng:
              </p>
              <div style="display:flex;gap:8px;justify-content:center;align-items:center;flex-wrap:wrap;">
                <label for="ugc-user-photo-input" style="display:inline-flex;align-items:center;gap:6px;padding:8px 16px;border-radius:999px;background:#165632;color:#fff;font-size:13px;font-weight:800;cursor:pointer;box-shadow:0 4px 12px rgba(22,86,50,0.3);">
                  📁 Chọn ảnh từ thiết bị của bạn
                </label>
                <input id="ugc-user-photo-input" type="file" accept="image/*" style="display:none;" />
                <button type="button" id="btn-ugc-sample-user-1" style="padding:7px 11px;border-radius:999px;border:1.5px solid #8c4b1e;background:#fffdf8;color:#5c3412;font-size:12px;font-weight:700;cursor:pointer;">
                  👩 Dùng ảnh mẫu Phật tử Nữ
                </button>
                <button type="button" id="btn-ugc-sample-user-2" style="padding:7px 11px;border-radius:999px;border:1.5px solid #8c4b1e;background:#fffdf8;color:#5c3412;font-size:12px;font-weight:700;cursor:pointer;">
                  👨‍👩‍👧 Dùng ảnh mẫu Gia đình
                </button>
              </div>
              <div id="ugc-upload-filename" style="margin-top:6px;font-size:12px;font-weight:700;color:#15803d;">
                ${
                  this.uploadedUserPhotoDataUrl
                    ? '✓ Ảnh người dùng đã sẵn sàng trên khung Check-in'
                    : 'Chưa tải ảnh cá nhân (đang hiển thị nhân vật 3D mặc định)'
                }
              </div>
            </div>

            <!-- STEP 2: SELECT TEMPLE SCENE (LIVE 3D WORLD SNAPSHOT OR ARCHITECTURAL BACKDROP) -->
            <div>
              <div style="font-size:13.5px;font-weight:800;color:#144929;margin-bottom:5px;">
                2. Chọn Bối cảnh Chùa Vĩnh Tràng (Góc 3D thực tế hoặc Kiến trúc):
              </div>
              <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;">
                <button class="ugc-bg-btn" data-bg="live_3d_view" style="padding:8px 10px;border-radius:10px;border:1.5px solid #165632;background:#e5f5eb;font-size:12.5px;font-weight:800;text-align:left;cursor:pointer;">
                  🌐 Góc nhìn 3D hiện tại (Hồ Sen / Tượng Phật / Chánh Điện)
                </button>
                ${UGC_BACKDROPS.map(
                  (b) => `
                  <button class="ugc-bg-btn" data-bg="${b.id}" style="padding:8px 10px;border-radius:10px;border:1.5px solid rgba(130,90,50,0.28);background:#fffdf8;font-size:12.5px;font-weight:700;text-align:left;cursor:pointer;">
                    ${b.name}
                  </button>
                `
                ).join('')}
              </div>
            </div>

            <!-- STEP 3: COMPANION 3D AVATAR & POSE -->
            <div>
              <div style="font-size:13.5px;font-weight:800;color:#144929;margin-bottom:5px;">
                3. Chọn Nhân vật 3D đồng hành & Nghi thức kỷ niệm:
              </div>
              <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;">
                ${[
                  { id: 'family_3', label: '👨‍👩‍👧 Gia đình 3 nhân vật (Nam · Nữ · Trẻ em)' },
                  { id: 'nu', label: '👩 Phật tử Nữ (Áo lam 1.62m)' },
                  { id: 'nam', label: '👨 Phật tử Nam (Áo tràng 1.74m)' },
                  { id: 'tre_em', label: '🧒 Em bé Phật tử (1.15m)' }
                ]
                  .map(
                    (m, i) => `
                  <button class="ugc-char-btn" data-cmode="${m.id}" style="padding:7px 10px;border-radius:10px;border:1.5px solid ${
                      i === 0 ? '#165632' : 'rgba(130,90,50,0.28)'
                    };background:${i === 0 ? '#e5f5eb' : '#fffdf8'};font-size:12px;font-weight:700;text-align:left;cursor:pointer;">
                    ${m.label}
                  </button>
                `
                  )
                  .join('')}
              </div>
            </div>

            <div style="display:flex;gap:8px;">
              <input id="ugc-author-input" type="text" placeholder="Tên Phật tử / Gia đình" value="Phật tử Tâm An" style="width:40%;padding:9px 11px;border-radius:10px;border:1px solid #bfa07a;font-size:13px;" />
              <input id="ugc-wish-input" type="text" placeholder="Lời nguyện cầu trên ảnh Check-in..." value="Check-in Chùa Vĩnh Tràng — Nguyện cầu gia đạo bình an, tâm thanh tịnh!" style="flex:1;padding:9px 11px;border-radius:10px;border:1px solid #bfa07a;font-size:13px;" />
            </div>
          </div>
        </div>

        <div style="margin-top:8px;border-top:1.5px solid rgba(140,100,60,0.25);padding-top:12px;">
          <div style="font-size:15.5px;font-weight:800;color:#144929;margin-bottom:8px;">
            🌟 Bức Tường Lưu Bút Check-in Cộng Đồng Phật Tử (${this.ugcGallery.length} bức ảnh kỷ niệm)
          </div>
          <div id="ugc-gallery-feed" style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;"></div>
        </div>
      </div>
      `
    );

    // Quick unlock ritual buttons if user opened modal before completing a milestone
    document.getElementById('btn-ugc-quick-bow')?.addEventListener('click', () => {
      const r = performSpiritualAction(this.spiritual, 'LE_PHAT');
      this.spiritual = r.state;
      this.saveState();
      this.updateActionBadges();
      this.world3d?.playPlayerBowAnimation();
      this.playBellTone(216, 2.5);
      this.openUGCStudioModal();
    });

    document.getElementById('btn-ugc-quick-lotus')?.addEventListener('click', () => {
      const r = performSpiritualAction(this.spiritual, 'DANG_HOA');
      this.spiritual = r.state;
      this.saveState();
      this.updateActionBadges();
      this.world3d?.placeLotusOfferingIn3D();
      this.playBellTone(324, 2.2);
      this.openUGCStudioModal();
    });

    const renderGalleryFeed = () => {
      const feed = document.getElementById('ugc-gallery-feed');
      if (!feed) return;
      feed.innerHTML = this.ugcGallery
        .slice(0, 6)
        .map(
          (post) => `
          <div style="background:#fffdf8;border:1px solid rgba(140,100,60,0.28);border-radius:14px;padding:10px 12px;display:flex;flex-direction:column;justify-content:space-between;gap:6px;">
            <div>
              <div style="display:flex;justify-content:space-between;align-items:center;gap:6px;">
                <span style="font-size:13px;font-weight:800;color:#165632;">${post.author}</span>
                <span style="font-size:11px;font-weight:700;color:#8c4b1e;background:#fef3db;padding:2px 7px;border-radius:999px;">✓ ${
                  post.milestoneBadge || 'Lễ Phật'
                }</span>
              </div>
              <div style="font-size:11.5px;color:#8c4b1e;margin-top:2px;">${post.createdAt}</div>
              <p style="font-size:12.5px;color:#3d2410;margin-top:4px;line-height:1.4;">"${post.wishText}"</p>
            </div>
            <div style="display:flex;justify-content:space-between;align-items:center;margin-top:4px;">
              <span style="font-size:11.5px;font-weight:700;color:#6b4522;">${
                post.userPhotoUploaded ? '📸 Ảnh thật Check-in' : '🙏 Check-in 3D'
              }</span>
              <button class="ugc-like-btn" data-post-id="${post.id}" style="padding:3px 9px;border-radius:999px;border:1px solid #c8963e;background:#fef3db;color:#7a4414;font-size:11.5px;font-weight:800;cursor:pointer;">
                🙏 Tùy hỷ (${post.likes})
              </button>
            </div>
          </div>
        `
        )
        .join('');

      feed.querySelectorAll('.ugc-like-btn').forEach((btn) => {
        btn.addEventListener('click', () => {
          const pid = btn.getAttribute('data-post-id');
          const found = this.ugcGallery.find((p) => p.id === pid);
          if (found) {
            found.likes += 1;
            this.saveState();
            this.playBellTone(360, 1.2);
            renderGalleryFeed();
          }
        });
      });
    };

    const drawComposite = () => {
      const canvas = document.getElementById('ugc-composite-canvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      const w = canvas.width;
      const h = canvas.height;

      const curMilestone = checkUGCMilestoneUnlock(this.spiritual, this.completedLessons.size);
      const backdropObj =
        UGC_BACKDROPS.find((b) => b.id === selectedBackdropId) || UGC_BACKDROPS[0];
      const poseObj = UGC_POSES.find((p) => p.id === selectedPoseId) || UGC_POSES[0];
      const authorText =
        document.getElementById('ugc-author-input')?.value || 'Phật tử Tâm An';
      const wishText =
        document.getElementById('ugc-wish-input')?.value ||
        'Kính lễ Phật tại Chùa Vĩnh Tràng';

      const bgSrc =
        selectedBackdropId === 'live_3d_view' && live3DSnapshot
          ? live3DSnapshot
          : backdropObj.src;

      const bgImg = new Image();
      bgImg.src = bgSrc;
      bgImg.onload = () => {
        ctx.clearRect(0, 0, w, h);
        // Draw temple background scene
        if (selectedBackdropId === 'live_3d_view' && live3DSnapshot) {
          ctx.drawImage(bgImg, 0, 0, w, h);
        } else {
          ctx.drawImage(bgImg, 0, 65, bgImg.width, bgImg.height * 0.62, 0, 0, w, h);
        }

        // Warm golden temple atmosphere vignette
        const grad = ctx.createLinearGradient(0, h * 0.48, 0, h);
        grad.addColorStop(0, 'rgba(20, 42, 28, 0)');
        grad.addColorStop(1, 'rgba(14, 34, 22, 0.94)');
        ctx.fillStyle = grad;
        ctx.fillRect(0, 0, w, h);

        // Draw Ornate Golden Border Around Check-in Postcard
        ctx.strokeStyle = 'rgba(236, 192, 91, 0.85)';
        ctx.lineWidth = 4;
        ctx.strokeRect(10, 10, w - 20, h - 20);

        // Top Golden Temple Stamp + Completed Milestone Badge
        ctx.fillStyle = 'rgba(20, 58, 35, 0.94)';
        ctx.strokeStyle = '#f3c65f';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.roundRect(22, 20, 495, 42, 21);
        ctx.fill();
        ctx.stroke();

        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 15px "Be Vietnam Pro", sans-serif';
        ctx.fillText('🪷 CHÙA VĨNH TRÀNG · ẢNH CHECK-IN CHỨNG NHẬN CÔNG ĐỨC', 36, 46);

        // Milestone Achievement Ribbon under header
        const milestoneLabel = curMilestone.unlocked
          ? `✨ Đã hoàn thành: ${curMilestone.latestMilestone}`
          : '🙏 Hành hương Chùa Vĩnh Tràng Mỹ Tho';
        ctx.fillStyle = 'rgba(158, 56, 16, 0.92)';
        ctx.strokeStyle = '#fbe09c';
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.roundRect(22, 70, 380, 32, 16);
        ctx.fill();
        ctx.stroke();

        ctx.fillStyle = '#fff7df';
        ctx.font = 'bold 13px "Be Vietnam Pro", sans-serif';
        ctx.fillText(milestoneLabel.slice(0, 48), 36, 91);

        // Foreground Portrait: User's Uploaded Photo (Primary) + 3D Companion Badge
        const primaryPortraitSrc =
          this.uploadedUserPhotoDataUrl ||
          (selectedCharMode === 'family_3'
            ? '/Thiết kế giao diện/Nhân vật 3D/anh-xem-truoc-3d-all-nguoi-that.png'
            : (
                CHARACTER_PROFILES.find((c) => c.key === selectedCharMode) ||
                CHARACTER_PROFILES[0]
              ).previewImg);

        const userImg = new Image();
        userImg.src = primaryPortraitSrc;
        userImg.onload = () => {
          // Large Golden Lotus Arch Portrait Frame on Right Foreground
          const pw = 230;
          const ph = 265;
          const px = w - pw - 28;
          const py = h - ph - 86;

          ctx.save();
          // Outer golden glow frame
          ctx.fillStyle = '#fff9ed';
          ctx.strokeStyle = '#e5b24c';
          ctx.lineWidth = 5;
          ctx.beginPath();
          ctx.roundRect(px - 6, py - 6, pw + 12, ph + 12, 24);
          ctx.fill();
          ctx.stroke();

          ctx.beginPath();
          ctx.roundRect(px, py, pw, ph, 18);
          ctx.clip();

          // Aspect-fill user photo cleanly inside portrait frame
          const imgRatio = userImg.width / Math.max(1, userImg.height);
          const boxRatio = pw / ph;
          let sx = 0,
            sy = 0,
            sw = userImg.width,
            sh = userImg.height;
          if (imgRatio > boxRatio) {
            sw = userImg.height * boxRatio;
            sx = (userImg.width - sw) * 0.5;
          } else {
            sh = userImg.width / boxRatio;
            sy = (userImg.height - sh) * 0.2;
          }
          ctx.drawImage(userImg, sx, sy, sw, sh, px, py, pw, ph);
          ctx.restore();

          // Label badge below portrait frame ("Ảnh Check-in của bạn tại Chùa Vĩnh Tràng")
          ctx.fillStyle = '#165632';
          ctx.strokeStyle = '#f6cd72';
          ctx.lineWidth = 2;
          ctx.beginPath();
          ctx.roundRect(px + 10, py + ph - 18, pw - 20, 28, 14);
          ctx.fill();
          ctx.stroke();

          ctx.fillStyle = '#ffffff';
          ctx.font = 'bold 12px "Be Vietnam Pro", sans-serif';
          ctx.textAlign = 'center';
          ctx.fillText(
            this.uploadedUserPhotoDataUrl
              ? '📸 Ảnh Check-in Phật Tử'
              : '🙏 Nhân vật 3D Chùa Vĩnh Tràng',
            px + pw / 2,
            py + ph
          );
          ctx.textAlign = 'left';

          // Bottom Calligraphy Blessing Banner
          ctx.fillStyle = '#f8d278';
          ctx.font = 'bold 17px "Be Vietnam Pro", sans-serif';
          ctx.fillText(`${authorText} · ${poseObj.label}`, 26, h - 52);

          ctx.fillStyle = '#fff9ee';
          ctx.font = '500 14.5px "Be Vietnam Pro", sans-serif';
          ctx.fillText(`"${wishText.slice(0, 74)}"`, 26, h - 26);
        };
      };
    };

    const handleUserImageDataUrl = (dataUrl, labelText) => {
      this.uploadedUserPhotoDataUrl = dataUrl;
      // Ensure at least 1 milestone is recorded when user uploads photo
      if (!checkUGCMilestoneUnlock(this.spiritual, this.completedLessons.size).unlocked) {
        this.spiritual = recordSpiritualMilestone(
          this.spiritual,
          'Hoàn thành Check-in Hành Hương Chùa Vĩnh Tràng'
        );
      }
      this.saveState();
      this.updateUGCMilestoneHUD();

      const statusBadge = document.getElementById('ugc-output-status-badge');
      if (statusBadge) {
        statusBadge.textContent = '✓ Đã ghép ảnh của bạn vào Chùa Vĩnh Tràng!';
        statusBadge.style.background = '#b84518';
      }
      const fnEl = document.getElementById('ugc-upload-filename');
      if (fnEl) {
        fnEl.textContent = `✓ Đã nhận ảnh: ${labelText} — Hệ thống đã đẩy ảnh Check-in bên trái!`;
      }
      this.playBellTone(324, 2.0);
      drawComposite();
      this.showToast(
        '📸 Hệ thống đã đẩy ảnh Check-in Chùa Vĩnh Tràng!',
        'Ảnh của bạn đã được ghép vào khung cảnh Chùa Vĩnh Tràng kèm dấu ấn công đức.',
        4500
      );
    };

    // File input upload handler
    document.getElementById('ugc-user-photo-input')?.addEventListener('change', (e) => {
      const file = e.target?.files?.[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = () => {
        if (typeof reader.result === 'string') {
          handleUserImageDataUrl(reader.result, file.name);
        }
      };
      reader.readAsDataURL(file);
    });

    // Quick sample portrait buttons (for 1-click user testing)
    document.getElementById('btn-ugc-sample-user-1')?.addEventListener('click', () => {
      handleUserImageDataUrl(
        '/public/assets/aistudio/image_8f6004e3.png',
        'Ảnh chân dung Phật tử áo lam'
      );
    });

    document.getElementById('btn-ugc-sample-user-2')?.addEventListener('click', () => {
      handleUserImageDataUrl(
        '/Thiết kế giao diện/Nhân vật 3D/anh-xem-truoc-3d-all-nguoi-that.png',
        'Ảnh gia đình 3 người hành hương'
      );
    });

    drawComposite();
    renderGalleryFeed();

    document.querySelectorAll('.ugc-char-btn').forEach((btn) => {
      btn.addEventListener('click', () => {
        selectedCharMode = btn.getAttribute('data-cmode') || 'family_3';
        document.querySelectorAll('.ugc-char-btn').forEach((b) => {
          const act = b.getAttribute('data-cmode') === selectedCharMode;
          b.style.background = act ? '#e5f5eb' : '#fffdf8';
          b.style.borderColor = act ? '#165632' : 'rgba(130,90,50,0.28)';
        });
        drawComposite();
      });
    });

    document.querySelectorAll('.ugc-bg-btn').forEach((btn) => {
      btn.addEventListener('click', () => {
        selectedBackdropId = btn.getAttribute('data-bg') || 'live_3d_view';
        document.querySelectorAll('.ugc-bg-btn').forEach((b) => {
          const act = b.getAttribute('data-bg') === selectedBackdropId;
          b.style.background = act ? '#e5f5eb' : '#fffdf8';
          b.style.borderColor = act ? '#165632' : 'rgba(130,90,50,0.28)';
        });
        drawComposite();
      });
    });

    document.getElementById('ugc-author-input')?.addEventListener('input', drawComposite);
    document.getElementById('ugc-wish-input')?.addEventListener('input', drawComposite);

    document.getElementById('btn-ugc-download')?.addEventListener('click', () => {
      const canvas = document.getElementById('ugc-composite-canvas');
      if (!canvas) return;
      const link = document.createElement('a');
      link.download = `checkin-chua-vinh-trang-${Date.now()}.png`;
      link.href = canvas.toDataURL('image/png');
      link.click();
      this.showToast(
        '📸 Đã tải ảnh Check-in Chùa Vĩnh Tràng',
        'Ảnh kỷ niệm của bạn với Chùa Vĩnh Tràng đã được lưu về máy.',
        3600
      );
    });

    document.getElementById('btn-ugc-publish')?.addEventListener('click', () => {
      const curM = checkUGCMilestoneUnlock(this.spiritual, this.completedLessons.size);
      const post = createUGCPost({
        author: document.getElementById('ugc-author-input')?.value,
        charMode: selectedCharMode,
        backdropId: selectedBackdropId,
        poseId: selectedPoseId,
        milestoneBadge: curM.latestMilestone || 'Lễ Phật Tam Bái',
        userPhotoUploaded: Boolean(this.uploadedUserPhotoDataUrl),
        wishText: document.getElementById('ugc-wish-input')?.value
      });
      this.ugcGallery.unshift(post);
      this.saveState();
      this.playBellTone(324, 2.0);
      renderGalleryFeed();
      this.showToast(
        '🌟 Đã đăng ảnh Check-in lên Lưu Bút Chùa Vĩnh Tràng',
        `Cảm ơn ${post.author} đã chia sẻ khoảnh khắc hành hương!`,
        4200
      );
    });
  }

  /* ========================================================================
     KHÁM PHÁ MODAL (9 Walkable 3D Zones + Dấu Ấn Hành Trình 9 Cánh Sen + 18 La Hán)
     ======================================================================== */
  openExploreModal(initialSubTab = 'stations') {
    const imprint = calculateJourneyImprint(this.spiritual);

    this.openModal(
      `🧭 Bản Đồ Khuôn Viên Chùa Vĩnh Tràng & Dấu Ấn Hành Trình (${imprint.litCount}/9 Cánh Sen)`,
      `
      <div style="display:flex;flex-direction:column;gap:14px;">
        <div style="display:flex;gap:8px;flex-wrap:wrap;">
          <button class="explore-sub-btn product-detail-btn" data-sub="stations" style="width:auto;padding:0 16px;height:38px;font-size:13.5px;">🗺️ Đi Bộ 9 Khu Vực 3D</button>
          <button class="explore-sub-btn product-detail-btn" data-sub="imprint" style="width:auto;padding:0 16px;height:38px;font-size:13.5px;background:#1C5A34;">🪷 Dấu Ấn Hành Trình (${imprint.litCount}/9)</button>
          <button class="explore-sub-btn product-detail-btn" data-sub="arhats" style="width:auto;padding:0 16px;height:38px;font-size:13.5px;background:#6d4422;">🙏 18 Vị La Hán</button>
          <button class="explore-sub-btn product-detail-btn" data-sub="sweep" style="width:auto;padding:0 16px;height:38px;font-size:13.5px;background:#3a5c28;">🍂 Quét Lá Sân Chùa</button>
          <button id="btn-explore-open-interior" class="product-detail-btn" style="width:auto;padding:0 16px;height:38px;font-size:13.5px;background:#784820;">🏛️ Vào Nội Điện 18 La Hán 3D</button>
          <button id="btn-explore-open-ugc" class="product-detail-btn" style="width:auto;padding:0 16px;height:38px;font-size:13.5px;background:#C96F4A;">📸 Lưu Ảnh Kỷ Niệm Chùa</button>
        </div>

        <div id="explore-sub-content"></div>
      </div>
      `
    );

    const renderSub = (sub) => {
      const box = document.getElementById('explore-sub-content');
      if (!box) return;

      if (sub === 'stations') {
        const curX = this.world3d ? this.world3d.playerPos.x : this.playerPos.x;
        const curZ = this.world3d ? this.world3d.playerPos.z : this.playerPos.z;
        // Map world (x in [-36, 52], z in [-55, 45]) to SVG viewBox (0..760, 0..340)
        const mapX = (x) => Math.round(((x + 36) / 88) * 660 + 50);
        const mapY = (z) => Math.round(((z + 55) / 100) * 280 + 30);
        const px = mapX(curX);
        const py = mapY(curZ);
        const axisX = mapX(23); // 493

        box.innerHTML = `
          <!-- Interactive 2D Architectural Map of Chùa Vĩnh Tràng -->
          <div style="background:#f6ebd6;border:2px solid #C9962E;border-radius:18px;padding:12px 14px;margin-bottom:12px;box-shadow:inset 0 2px 10px rgba(74,50,34,0.1);">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;flex-wrap:wrap;gap:8px;">
              <div>
                <strong style="font-size:15px;color:#1C5A34;">🗺️ Tổng Mặt Bằng Kiến Trúc Chùa Vĩnh Tràng (2 Hecta)</strong>
                <span style="font-size:12px;color:#6E5034;margin-left:8px;">Bấm vào bất kỳ công trình nào trên bản đồ để Đi bộ hoặc Đến ngay</span>
              </div>
              <div style="font-size:12px;font-weight:800;color:#B84518;background:#fffdf8;padding:4px 10px;border-radius:999px;border:1px solid #C9962E;">
                📍 Vị trí của bạn: (X: ${curX.toFixed(1)}m, Z: ${curZ.toFixed(1)}m)
              </div>
            </div>

            <svg viewBox="0 0 760 340" style="width:100%;height:245px;background:linear-gradient(in oklab 180deg,#dcecd5 0%,#efe4ca 55%,#e5d5b5 100%);border-radius:14px;border:1.5px solid rgba(120,85,45,0.35);display:block;">
              <!-- North-South Central Sacred Axis (x = 23) & Stone Pathways -->
              <rect x="${axisX - 48}" y="25" width="96" height="295" rx="8" fill="#d8ccb8" stroke="#b5a48b" stroke-width="1.5"/>
              <line x1="${axisX}" y1="25" x2="${axisX}" y2="318" stroke="#C9962E" stroke-width="2" stroke-dasharray="5,5"/>
              <path d="M ${mapX(-24.5)} ${mapY(16)} L ${mapX(40)} ${mapY(16)} M ${mapX(-24.5)} ${mapY(-4)} L ${mapX(44)} ${mapY(-4)} M ${mapX(-14)} ${mapY(28)} L ${axisX} ${mapY(28)}" stroke="#d8ccb8" stroke-width="14" stroke-linecap="round"/>

              <!-- Rear Nirvana Park & 7-Tier Stupa (North / Top of Map, x=12, z=-47) -->
              <rect x="${mapX(12) - 95}" y="${mapY(-47) - 18}" width="190" height="40" rx="10" fill="#f7efe0" stroke="#C9962E" stroke-width="2"/>
              <text x="${mapX(12)}" y="${mapY(-47) + 16}" text-anchor="middle" fill="#4A3222" font-size="11" font-weight="800">🌸 Đại Tượng Phật Niết Bàn (32m)</text>
              <circle cx="${mapX(-10)}" cy="${mapY(-44)}" r="22" fill="#e6b84c" stroke="#7E2A22" stroke-width="2"/>
              <text x="${mapX(-10)}" y="${mapY(-44) + 4}" text-anchor="middle" fill="#241409" font-size="10" font-weight="800">Bảo Tháp 7 Tầng</text>

              <!-- Chánh Điện 13 Nhịp Vòm & Nội Điện 18 La Hán (x=23, z=-1) -->
              <rect x="${axisX - 88}" y="${mapY(-1) - 32}" width="176" height="64" rx="8" fill="#D9A441" stroke="#7E2A22" stroke-width="3"/>
              <text x="${axisX}" y="${mapY(-1) - 6}" text-anchor="middle" fill="#241409" font-size="12.5" font-weight="900">🏛️ CHÁNH ĐIỆN VĨNH TRÀNG</text>
              <text x="${axisX}" y="${mapY(-1) + 22}" text-anchor="middle" fill="#4A3222" font-size="10.5" font-weight="700">(Tam Bảo & 18 Vị La Hán)</text>

              <!-- Đại Tượng Phật Di Lặc (West-Central, x=-24.5, z=-4) -->
              <circle cx="${mapX(-24.5)}" cy="${mapY(-4)}" r="34" fill="#fffdf8" stroke="#1C5A34" stroke-width="2.5"/>
              <text x="${mapX(-24.5)}" y="${mapY(-4) + 20}" text-anchor="middle" fill="#1C5A34" font-size="10.5" font-weight="800">😊 Phật Di Lặc (20m)</text>

              <!-- Giảng Đường (x=44, z=-20) & Quầy Lưu Niệm (x=40, z=38) -->
              <rect x="${mapX(44) - 64}" y="${mapY(-20) - 22}" width="128" height="44" rx="8" fill="#8A4A34" stroke="#f6cd72" stroke-width="2"/>
              <text x="${mapX(44)}" y="${mapY(-20) + 17}" text-anchor="middle" fill="#FFF6E5" font-size="11" font-weight="800">📖 Giảng Đường</text>
              <rect x="${mapX(40) - 64}" y="${mapY(38) - 22}" width="128" height="42" rx="8" fill="#C96F4A" stroke="#fff" stroke-width="2"/>
              <text x="${mapX(40)}" y="${mapY(38) + 16}" text-anchor="middle" fill="#FFF6E5" font-size="11" font-weight="800">🏮 Quầy Lưu Niệm 3D</text>

              <!-- Song Liên Trì (Lotus Pond & Koi Bridge, x=5, z=16) -->
              <ellipse cx="${mapX(5)}" cy="${mapY(16)}" rx="56" ry="24" fill="#3B6E5C" stroke="#8fc9b3" stroke-width="2"/>
              <text x="${mapX(5)}" y="${mapY(16) + 18}" text-anchor="middle" fill="#FFF6E5" font-size="10.5" font-weight="800">🪷 Hồ Sen & Cá Koi</text>

              <!-- Đại Tượng Phật A Di Đà (West-Front Park, x=-14, z=28) -->
              <circle cx="${mapX(-14)}" cy="${mapY(28)}" r="34" fill="#fffdf8" stroke="#4E86A8" stroke-width="3"/>
              <text x="${mapX(-14)}" y="${mapY(28) + 22}" text-anchor="middle" fill="#1C5A34" font-size="10.5" font-weight="900">🙏 Phật A Di Đà (24m)</text>

              <!-- Cổng Tam Quan & Đường Nguyễn Trung Trực (South Entrance, x=23, z=40.7) -->
              <rect x="${axisX - 85}" y="${mapY(40.7) - 14}" width="170" height="28" rx="6" fill="#7E2A22" stroke="#FFD875" stroke-width="2"/>
              <text x="${axisX}" y="${mapY(40.7) + 11}" text-anchor="middle" fill="#FFD875" font-size="10.5" font-weight="800">⛩️ 2 CỔNG TAM QUAN</text>

              <!-- Interactive Station Pins on 2D Map -->
              ${PILGRIMAGE_STATIONS.map((st) => {
                const sx = mapX(st.pos.x);
                const sy = mapY(st.pos.z);
                const isAct = this.activeStationKey === st.key;
                return `
                  <g class="map2d-station-pin" data-station-key="${st.key}" style="cursor:pointer;">
                    <circle cx="${sx}" cy="${sy}" r="${isAct ? 12 : 9}" fill="${isAct ? '#C96F4A' : '#1C5A34'}" stroke="#FFF6E5" stroke-width="2.5"/>
                    <text x="${sx}" y="${sy + 3.5}" text-anchor="middle" fill="#FFF6E5" font-size="9.5" font-weight="900">${st.id}</text>
                  </g>
                `;
              }).join('')}

              <!-- Live Pulsing Player Dot -->
              <g transform="translate(${px}, ${py})">
                <circle r="13" fill="rgba(255, 196, 46, 0.38)"/>
                <circle r="7" fill="#FFD875" stroke="#7E2A22" stroke-width="2.5"/>
              </g>
            </svg>
          </div>

          <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;">
            ${PILGRIMAGE_STATIONS.map((st) => {
              const visited = this.spiritual.visitedStations.includes(st.id);
              return `
              <div style="background:#fffdf8;border:1.5px solid ${
                visited ? '#1C5A34' : 'rgba(140,100,60,0.28)'
              };border-radius:16px;padding:12px 14px;display:flex;flex-direction:column;justify-content:space-between;gap:8px;">
                <div>
                  <div style="display:flex;justify-content:space-between;align-items:center;">
                    <span style="font-size:11.5px;font-weight:800;color:#1C5A34;">Trạm ${st.id} · ${st.zoneCode}</span>
                    <span style="font-size:11px;font-weight:800;color:${visited ? '#15803d' : '#8a623c'};">${
                      visited ? '🪷 Đã chiêm bái' : 'Chưa đến'
                    }</span>
                  </div>
                  <div style="font-size:15px;font-weight:800;margin-top:3px;">${st.name}</div>
                  <p style="font-size:12.5px;color:#52361c;margin-top:4px;line-height:1.4;">${st.subtitle}</p>
                </div>
                <div style="display:flex;gap:6px;">
                  <button class="visit-station-btn product-detail-btn" data-station-key="${st.key}" style="flex:1;height:36px;font-size:12.5px;">
                    🚶 Đi bộ tới
                  </button>
                  <button class="teleport-station-btn product-detail-btn" data-station-key="${st.key}" style="width:auto;padding:0 12px;height:36px;font-size:12.5px;background:#C96F4A;">
                    ⚡ Đến ngay
                  </button>
                </div>
              </div>
            `;
            }).join('')}
          </div>
        `;
        box.querySelectorAll('.visit-station-btn, .map2d-station-pin').forEach((b) => {
          b.addEventListener('click', () => {
            const key = b.getAttribute('data-station-key') || 'chanh_dien';
            this.closeModal();
            this.switchScreen('courtyard');
            this.walkToStationIn3D(key);
          });
        });
        box.querySelectorAll('.teleport-station-btn').forEach((b) => {
          b.addEventListener('click', () => {
            const key = b.getAttribute('data-station-key') || 'chanh_dien';
            this.closeModal();
            this.switchScreen('courtyard');
            this.teleportToStationIn3D(key);
          });
        });
      } else if (sub === 'imprint') {
        const curImprint = calculateJourneyImprint(this.spiritual);
        box.innerHTML = `
          <div style="background:#1C5A34;color:#FFF6E5;padding:16px 20px;border-radius:18px;margin-bottom:12px;display:flex;justify-content:space-between;align-items:center;gap:14px;flex-wrap:wrap;">
            <div>
              <div style="font-size:18px;font-weight:800;color:#FFD875;">🪷 Dấu Ấn Hành Trình Chánh Niệm</div>
              <div style="font-size:13.5px;opacity:0.92;margin-top:3px;">Mỗi cánh sen sáng lên khi đạo hữu thong thả dạo bước đến chiêm bái một điểm trong khuôn viên Chùa Vĩnh Tràng — không điểm số, không cấp bậc, chỉ có sự bình yên.</div>
            </div>
            <div style="display:flex;gap:6px;align-items:center;">
              ${curImprint.petals
                .map(
                  (p) =>
                    `<span title="${p.name}" style="font-size:22px;filter:${
                      p.lit ? 'none' : 'grayscale(1) opacity(0.38)'
                    };">🪷</span>`
                )
                .join('')}
            </div>
          </div>
          <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;">
            ${curImprint.petals
              .map(
                (p) => `
              <div style="background:#fffdf8;border:1.5px solid ${
                p.lit ? '#C9962E' : 'rgba(140,100,60,0.25)'
              };border-radius:14px;padding:12px 14px;">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                  <strong style="font-size:14px;color:#1C5A34;">${p.pinLabel}</strong>
                  <span style="font-size:12px;font-weight:800;color:${p.lit ? '#C9962E' : '#8a623c'};">
                    ${p.lit ? '🪷 Cánh sen đã nở' : '○ Chưa ghé'}
                  </span>
                </div>
                <p style="font-size:12.5px;color:#4A3222;margin-top:5px;line-height:1.4;">${p.subtitle}</p>
              </div>
            `
              )
              .join('')}
          </div>
        `;
      } else if (sub === 'arhats') {
        box.innerHTML = `
          <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;max-height:52vh;overflow-y:auto;padding-right:4px;">
            ${EIGHTEEN_ARHATS.map(
              (a) => `
              <div style="background:#fffdf8;border:1px solid rgba(140,100,60,0.28);border-radius:14px;padding:11px 13px;">
                <div style="font-size:12px;font-weight:800;color:#8c4b1e;">Vị thứ ${a.id}/18 · ${a.title}</div>
                <div style="font-size:14.5px;font-weight:800;color:#144929;margin:3px 0;">${a.name}</div>
                <p style="font-size:12.5px;color:#4a2f18;line-height:1.4;">${a.meaning}</p>
              </div>
            `
            ).join('')}
          </div>
        `;
      } else if (sub === 'sweep') {
        box.innerHTML = `
          <div style="background:#fffdf8;border:1.5px solid rgba(140,100,60,0.28);border-radius:18px;padding:18px;text-align:center;">
            <div style="font-size:19px;font-weight:800;color:#144929;">🍂 Quét Lá Sân Chùa — Quét Sạch Bụi Tâm</div>
            <p style="font-size:14px;color:#4a2f18;margin:6px auto 14px;max-width:520px;">
              "Chổi tre quét sạch lá vàng, Lòng ta quét sạch muôn ngàn sân si." Đạo hữu đã quét sạch <strong>${this.spiritual.leavesSwept}</strong> đợt lá rụng trên sân Chánh điện.
            </p>
            <button id="btn-do-sweep" class="product-detail-btn" style="max-width:280px;">🧹 Quét lá sân chùa trong chánh niệm</button>
          </div>
        `;
        document.getElementById('btn-do-sweep')?.addEventListener('click', () => {
          const r = performSpiritualAction(this.spiritual, 'SWEEP_LEAVES');
          this.spiritual = r.state;
          this.saveState();
          this.updateUGCMilestoneHUD();
          this.playMokugyoTap();
          renderSub('sweep');
        });
      }
    };

    renderSub(initialSubTab);

    document.querySelectorAll('.explore-sub-btn').forEach((btn) => {
      btn.addEventListener('click', () => {
        const sub = btn.getAttribute('data-sub') || 'stations';
        renderSub(sub);
      });
    });

    document.getElementById('btn-explore-open-ugc')?.addEventListener('click', () => {
      this.openUGCStudioModal();
    });

    document.getElementById('btn-explore-open-interior')?.addEventListener('click', () => {
      this.closeModal();
      this.switchScreen('courtyard');
      this.toggleInteriorHallIn3D(true);
    });
  }

  /* ========================================================================
     TÀI KHOẢN & TỦ ĐỒ 3 NHÂN VẬT 3D (Nam · Nữ · Trẻ em)
     ======================================================================== */
  openAccountModal() {
    const wearableItems = SHOP_CATALOG.filter((item) =>
      [
        'ao_trang_phat_tu',
        'tui_vai_theu_sen',
        'non_la_theu_sen',
        'khan_ran_nam_bo',
        'trang_hat_go',
        'so_tay_hoa_sen',
        'quat_nan_gio_may',
        'den_hoa_sen_pha_le_3d'
      ].includes(item.id)
    );

    const activeProf =
      CHARACTER_PROFILES.find((c) => c.key === this.characterModelKey) || CHARACTER_PROFILES[0];

    this.openModal(
      '👤 Hồ Sơ Phật Tử & Tủ Đồ 3 Nhân Vật 3D (Phật Tử Nữ · Phật Tử Nam · Trẻ Em)',
      `
      <div style="display:grid;grid-template-columns:300px 1fr;gap:20px;align-items:start;">
        <div style="background:#fffdf8;border:1.5px solid rgba(140,100,60,0.28);border-radius:20px;padding:12px;text-align:center;">
          <div class="viewer3d-stage" style="height:260px;">
            <canvas class="viewer3d-canvas" id="character-3d-canvas"></canvas>
            <img src="${activeProf.fitPreviewImg}" alt="${activeProf.name}" style="position:absolute;top:8px;right:8px;width:58px;height:74px;object-fit:cover;border-radius:10px;border:1.5px solid #165632;box-shadow:0 4px 10px rgba(0,0,0,0.2);" title="Kiểm chứng fit 3D" />
          </div>
          <div style="font-size:15px;font-weight:800;color:#144929;margin-top:8px;">${activeProf.name} (${activeProf.heightLabel})</div>
          <div style="font-size:12px;color:#5b3a1d;margin-top:2px;">${activeProf.outfitName}</div>
          <div style="display:flex;gap:6px;justify-content:center;margin-top:10px;">
            ${CHARACTER_PROFILES.map(
              (c) => `
              <button class="char-switch-btn" data-char="${c.key}" style="padding:6px 10px;border-radius:999px;border:1.5px solid #165632;background:${
                this.characterModelKey === c.key ? '#165632' : '#fff'
              };color:${
                this.characterModelKey === c.key ? '#fff' : '#165632'
              };font-size:12px;font-weight:700;cursor:pointer;">
                ${c.name.split('(')[0].trim()} (${c.heightLabel})
              </button>
            `
            ).join('')}
          </div>
        </div>

        <div style="display:flex;flex-direction:column;gap:12px;">
          <div style="background:#173d26;color:#fff8ea;padding:14px 18px;border-radius:16px;display:grid;grid-template-columns:repeat(4,1fr);gap:10px;text-align:center;">
            <div><div style="font-size:20px;font-weight:800;color:#f6cd72;">${this.spiritual.bowCount}</div><div style="font-size:12px;">Lạy Phật</div></div>
            <div><div style="font-size:20px;font-weight:800;color:#f6cd72;">${this.spiritual.incenseOfferings}</div><div style="font-size:12px;">Lần dâng hương</div></div>
            <div><div style="font-size:20px;font-weight:800;color:#f6cd72;">${this.spiritual.malaCycles * 108 + this.spiritual.malaBeads}</div><div style="font-size:12px;">Biến niệm Phật</div></div>
            <div><div style="font-size:20px;font-weight:800;color:#f6cd72;">${this.completedLessons.size}/24</div><div style="font-size:12px;">Bài học Phật</div></div>
          </div>

          <div>
            <div style="font-size:15px;font-weight:800;color:#144929;margin-bottom:8px;">Trang phục & Pháp khí 3D gắn trên 3 nhân vật:</div>
            <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:8px;">
              ${wearableItems
                .map((item) => {
                  const active = Object.values(this.spiritual.equippedItems).includes(item.id);
                  return `
                  <button class="wardrobe-toggle-btn" data-slot="${item.equipSlot}" data-id="${item.id}" style="padding:10px 12px;border-radius:12px;border:1.5px solid ${
                    active ? '#165632' : 'rgba(130,90,50,0.28)'
                  };background:${active ? '#e5f5eb' : '#fffdf8'};color:#241409;text-align:left;cursor:pointer;display:flex;justify-content:space-between;align-items:center;">
                    <span style="font-size:13px;font-weight:700;">${item.name}</span>
                    <span style="font-size:11.5px;font-weight:800;color:${active ? '#165632' : '#8a623c'};">${active ? '✓ Đang mang' : 'Thử gắn'}</span>
                  </button>
                `;
                })
                .join('')}
            </div>
          </div>

          <div style="display:flex;gap:10px;flex-wrap:wrap;">
            <button id="btn-account-open-ugc" class="product-detail-btn" style="flex:1;background:#9c4119;">📸 Đưa ảnh nhận Check-in Chùa Vĩnh Tràng</button>
            <button id="btn-account-open-shop" class="product-detail-btn" style="flex:1;">🪷 Cửa hàng lưu niệm & 20 Vật phẩm 3D</button>
          </div>
        </div>
      </div>
      `
    );

    this.mountInteractive3DStage('character-3d-canvas', {
      item: SHOP_CATALOG.find((p) => p.id === (this.spiritual.equippedItems.hat || 'non_la_theu_sen')),
      charKey: this.characterModelKey
    });

    document.querySelectorAll('.char-switch-btn').forEach((btn) => {
      btn.addEventListener('click', () => {
        const key = btn.getAttribute('data-char') || 'nu';
        this.characterModelKey = key;
        this.world3d?.switchCharacter(key);
        this.saveState();
        this.updateEquippedTags();
        this.openAccountModal();
      });
    });

    document.querySelectorAll('.wardrobe-toggle-btn').forEach((btn) => {
      btn.addEventListener('click', () => {
        const slot = btn.getAttribute('data-slot') || 'hand';
        const itemKey = btn.getAttribute('data-id');
        const r = performSpiritualAction(this.spiritual, 'EQUIP_ITEM', { slot, itemKey });
        this.spiritual = r.state;
        this.saveState();
        this.updateEquippedTags();
        this.openAccountModal();
      });
    });

    document.getElementById('btn-account-open-ugc')?.addEventListener('click', () => {
      this.openUGCStudioModal();
    });

    document.getElementById('btn-account-open-shop')?.addEventListener('click', () => {
      this.closeModal();
      this.switchScreen('shop');
    });
  }

  /* ========================================================================
     THREE.JS INTERACTIVE 3D STAGE (Loads Real Rigged GLBs + 3D Shop Kiosk + 3D Items)
     ======================================================================== */
  async mountInteractive3DStage(canvasId, { item, charKey }) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;

    try {
      const THREE = await import('three');
      const rect = canvas.parentElement.getBoundingClientRect();
      const w = Math.max(240, rect.width || 320);
      const h = Math.max(220, rect.height || 260);

      const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
      renderer.setSize(w, h, false);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));

      const scene = new THREE.Scene();
      const camera = new THREE.PerspectiveCamera(40, w / h, 0.1, 100);
      camera.position.set(0, 0.65, 2.25);
      camera.lookAt(0, 0.25, 0);

      scene.add(new THREE.AmbientLight(0xfff6e5, 1.45));
      const dir = new THREE.DirectionalLight(0xffdf9e, 1.7);
      dir.position.set(3, 5, 4);
      scene.add(dir);

      const ped = new THREE.Mesh(
        new THREE.CylinderGeometry(0.65, 0.72, 0.08, 32),
        new THREE.MeshStandardMaterial({ color: 0xc8963e, roughness: 0.4, metalness: 0.4 })
      );
      ped.position.y = -0.38;
      scene.add(ped);

      const stageGroup = new THREE.Group();
      scene.add(stageGroup);

      // Build procedural 3D mesh for item or 3D Shop Kiosk
      const mesh3d = this.build3DItemMesh(THREE, item?.procedural3dId || item?.id || 'non_la_theu_sen');
      if (charKey) {
        mesh3d.position.set(0.32, -0.15, 0.18);
      } else {
        mesh3d.position.set(0, -0.15, 0);
        mesh3d.scale.setScalar(1.35);
      }
      stageGroup.add(mesh3d);

      // Load rigged 3D character GLB if charKey specified
      if (charKey) {
        this.loadRiggedCharacterGLB(THREE, charKey).then((charMesh) => {
          if (charMesh) {
            stageGroup.add(charMesh);
          }
        });
      }

      let dragging = false;
      let prevX = 0;
      canvas.addEventListener('pointerdown', (e) => {
        dragging = true;
        prevX = e.clientX;
      });
      window.addEventListener('pointerup', () => {
        dragging = false;
      });
      canvas.addEventListener('pointermove', (e) => {
        if (!dragging) return;
        stageGroup.rotation.y += (e.clientX - prevX) * 0.012;
        prevX = e.clientX;
      });

      const animate = () => {
        if (!document.body.contains(canvas)) {
          renderer.dispose();
          return;
        }
        if (!dragging) stageGroup.rotation.y += 0.01;
        renderer.render(scene, camera);
        setTimeout(() => requestAnimationFrame(animate), 33);
      };
      animate();
    } catch {}
  }

  /* ========================================================================
     MODAL HELPERS & GLOBAL EVENT BINDINGS
     ======================================================================== */
  openModal(title, htmlContent) {
    const modal = document.getElementById('universal-modal');
    const titleEl = document.getElementById('modal-title');
    const bodyEl = document.getElementById('modal-body');
    if (!modal || !titleEl || !bodyEl) return;
    titleEl.textContent = title;
    bodyEl.innerHTML = htmlContent;
    modal.classList.add('open');
  }

  closeModal() {
    const modal = document.getElementById('universal-modal');
    if (modal) modal.classList.remove('open');
  }

  bindEvents() {
    document.getElementById('btn-brand-home')?.addEventListener('click', () => {
      this.switchScreen('courtyard');
      if (this.world3d?.insideInterior) {
        this.toggleInteriorHallIn3D(false);
      }
      this.walkToStationIn3D('chanh_dien');
    });

    document.getElementById('nav-btn-explore')?.addEventListener('click', () => {
      this.openExploreModal('stations');
    });
    document.getElementById('nav-btn-lecture')?.addEventListener('click', () => {
      this.switchScreen('lecture');
    });
    document.getElementById('nav-btn-account')?.addEventListener('click', () => {
      this.openAccountModal();
    });

    // Quick-Walk 3D Landmark Bar
    document.querySelectorAll('[data-walk-station]').forEach((btn) => {
      btn.addEventListener('click', () => {
        const stKey = btn.getAttribute('data-walk-station');
        if (!stKey) return;
        if (this.world3d?.insideInterior) {
          this.toggleInteriorHallIn3D(false);
        }
        this.walkToStationIn3D(stKey);
      });
    });

    document.getElementById('btn-toggle-interior-hall')?.addEventListener('click', () => {
      this.toggleInteriorHallIn3D();
    });

    // Scene Pins in 3D Courtyard
    document.getElementById('pin-chanh-dien')?.addEventListener('click', () => {
      this.walkToStationIn3D('chanh_dien');
    });
    document.getElementById('pin-ho-sen')?.addEventListener('click', () => {
      this.walkToStationIn3D('ho_sen_ca_koi');
    });
    document.getElementById('pin-phat-adida')?.addEventListener('click', () => {
      this.walkToStationIn3D('phat_adida');
    });
    document.getElementById('pin-phat-dilac')?.addEventListener('click', () => {
      this.walkToStationIn3D('phat_di_lac');
    });
    document.getElementById('pin-cua-hang')?.addEventListener('click', () => {
      this.switchScreen('shop');
    });
    document.getElementById('pin-giang-duong')?.addEventListener('click', () => {
      this.switchScreen('lecture');
    });
    document.getElementById('btn-ugc-milestone-hud')?.addEventListener('click', () => {
      this.openUGCStudioModal();
    });
    document.getElementById('protagonist-hotspot')?.addEventListener('click', () => {
      this.openAccountModal();
    });

    document.getElementById('btn-open-2d-map')?.addEventListener('click', () => {
      this.openExploreModal('stations');
    });
    document.getElementById('btn-an-mini-map')?.addEventListener('click', () => {
      this.openExploreModal('stations');
    });
    document.getElementById('btn-an-station-action')?.addEventListener('click', () => {
      this.triggerAnStationAction();
    });
    document.getElementById('btn-an-teleport-here')?.addEventListener('click', () => {
      this.teleportToStationIn3D(this.activeStationKey || 'chanh_dien');
    });

    // Bottom-Left D-Pad ("Di chuyển" — Supports both continuous hold and single tap)
    document.querySelectorAll('.dpad-btn').forEach((btn) => {
      const dir = btn.getAttribute('data-dir');
      if (!dir) return;
      btn.addEventListener('pointerdown', (e) => {
        e.preventDefault();
        this.world3d?.setHeldDirection(dir, true);
        this.handleMoveDirection(dir);
      });
      const stopHold = () => {
        this.world3d?.setHeldDirection(dir, false);
      };
      btn.addEventListener('pointerup', stopHold);
      btn.addEventListener('pointerleave', stopHold);
      btn.addEventListener('pointercancel', stopHold);
      btn.addEventListener('click', () => {
        this.handleMoveDirection(dir);
      });
    });

    const keyMap = {
      ArrowUp: 'up',
      KeyW: 'up',
      ArrowDown: 'down',
      KeyS: 'down',
      ArrowLeft: 'left',
      KeyA: 'left',
      ArrowRight: 'right',
      KeyD: 'right'
    };

    window.addEventListener('keydown', (e) => {
      if (['INPUT', 'TEXTAREA'].includes(document.activeElement?.tagName || '')) return;
      const dir = keyMap[e.code];
      if (dir && this.activeScreen === 'courtyard') {
        e.preventDefault();
        this.world3d?.setHeldDirection(dir, true);
        if (!e.repeat) {
          this.handleMoveDirection(dir);
        }
      } else if (e.code === 'Escape') {
        this.closeModal();
      }
    });

    window.addEventListener('keyup', (e) => {
      const dir = keyMap[e.code];
      if (dir) {
        this.world3d?.setHeldDirection(dir, false);
      }
    });

    window.addEventListener('blur', () => {
      this.world3d?.clearHeldDirections();
    });

    // Bottom-Right 4 Spiritual Action Buttons
    document.getElementById('act-le-phat')?.addEventListener('click', () => this.triggerLePhat());
    document.getElementById('act-dang-huong')?.addEventListener('click', () => this.triggerDangHuong());
    document.getElementById('act-dang-hoa')?.addEventListener('click', () => this.triggerDangHoa());
    document.getElementById('act-niem-phat')?.addEventListener('click', () => this.triggerNiemPhat());

    // Shop Screen Controls
    document.querySelectorAll('[data-shop-tab]').forEach((btn) => {
      btn.addEventListener('click', () => {
        const tab = btn.getAttribute('data-shop-tab');
        if (tab) {
          this.shopTab = tab;
          this.renderShopProducts();
        }
      });
    });
    document.getElementById('shop-nav-kiosk3d')?.addEventListener('click', () => {
      this.openProductDetailModal('mo_hinh_cua_hang_3d');
    });
    document.getElementById('btn-open-cart')?.addEventListener('click', () => this.openCartModal());
    document.getElementById('btn-shop-support')?.addEventListener('click', () => {
      this.openModal(
        '🎧 Hỗ Trợ Phật Tử & Hướng Dẫn Thỉnh Vật Phẩm 3D',
        `
        <div style="display:flex;flex-direction:column;gap:10px;font-size:15px;line-height:1.55;color:#3d2410;">
          <p><strong>1. Quà lưu niệm & Đồ tu học giao tận nhà:</strong> Mọi vật phẩm tại Cửa hàng lưu niệm Chùa Vĩnh Tràng đều được đóng gói trang nghiêm và giao tận nhà toàn quốc (miễn phí vận chuyển cho đơn từ 300.000đ).</p>
          <p><strong>2. Mô hình Quầy Cửa hàng 3D & 3 Nhân vật (Nam · Nữ · Trẻ em):</strong> Bấm <em>Xem chi tiết</em> ở bất kỳ vật phẩm nào để xoay mô hình 3D trực tiếp, thử gắn lên cả 3 nhân vật (Nam 1.74m, Nữ 1.62m, Trẻ em 1.15m) hoặc tải gói <code>.zip</code> chuẩn Coohom.</p>
          <p><strong>3. Liên hệ Ban Quản Tự & Hỗ Trợ:</strong> Đường dây nóng hỗ trợ Phật tử: <strong>1900 6868</strong> (07:00 – 20:00 hàng ngày).</p>
        </div>
        `
      );
    });
    document.getElementById('btn-shop-back-home')?.addEventListener('click', () => this.switchScreen('courtyard'));
    document.getElementById('btn-shop-return-courtyard')?.addEventListener('click', () => this.switchScreen('courtyard'));
    document.getElementById('shop-nav-explore')?.addEventListener('click', () => this.openExploreModal('stations'));
    document.getElementById('shop-nav-lecture')?.addEventListener('click', () => this.switchScreen('lecture'));
    document.getElementById('shop-nav-account')?.addEventListener('click', () => this.openAccountModal());

    // Lecture Screen Controls
    document.getElementById('btn-lecture-back')?.addEventListener('click', () => this.switchScreen('courtyard'));
    document.getElementById('btn-lecture-textbooks')?.addEventListener('click', () => this.openTextbooksModal());
    document.getElementById('btn-lecture-recordings')?.addEventListener('click', () => this.openAudioRecordingsModal());
    document.querySelectorAll('[data-lecture-tab]').forEach((btn) => {
      btn.addEventListener('click', () => {
        const tab = btn.getAttribute('data-lecture-tab');
        if (tab) {
          this.lectureTab = tab;
          this.renderLectureStage();
        }
      });
    });

    // Modal close events
    document.getElementById('modal-close-btn')?.addEventListener('click', () => this.closeModal());
    document.getElementById('universal-modal')?.addEventListener('click', (e) => {
      if (e.target && e.target.id === 'universal-modal') {
        this.closeModal();
      }
    });
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const app = new ChuaOnlineApp();
  app.init();
});
