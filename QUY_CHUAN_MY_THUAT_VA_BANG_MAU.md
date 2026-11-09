# QUY CHUẨN MỸ THUẬT & HỆ THỐNG MÀU SẮC (ART DIRECTION & COLOR SYSTEM)
## DỰ ÁN CHÙA ONLINE — CHÙA VĨNH TRÀNG 3D

> **Chuyên gia:** Art Director & Colorist  
> **Căn cứ nghiên cứu:**
> - Mockup thiết kế chuẩn: `chua-vinh-trang-3d-cartoon-de-xuat-01.png`, `cua-hang-luu-niem-de-xuat-02.png`, `giang-duong-phat-phap-de-xuat-01.png`, `giang-duong-bai-hoc-v2.png`
> - Hồ sơ thực tế 165 ảnh độ phân giải cao tại `assets/chua_vinh_trang_3d_ref/`
> - Văn kiện định hướng: `THEME_CHUA_ONLINE.md`, `THIET_KE_V5_CHOT.md`

---

## 1. NGUYÊN LÝ NGHỆ THUẬT CỐT LÕI (CORE ART DIRECTION)

1. **Khí chất tổng thể**: **SÁNG, ẤM, RỰC VỪA ĐỦ, THANH TỊNH**.
   - Tái hiện buổi sáng ngập tràn ánh nắng phương Nam tại Chùa Vĩnh Tràng (Mỹ Tho - Tiền Giang).
   - **Tuyệt đối loại bỏ** phong cách u tối, nâu đen rỉ sét, ánh sáng ma quái của các phiên bản cũ (v3).
2. **Quy luật tương phản hài hòa**:
   - Nền trời thiên thanh (`#74B4FA`) ôm trọn kiến trúc vàng hoàng thổ (`#E8C87A`) và mái ngói đất nung (`#B34728`).
   - Sắc hoa giấy hồng tím rực rỡ (`#E0367E`) và bonsai ngọc lục bảo (`#23532B`) tạo nên mật độ sinh khí dày dặn, ấm áp.
   - Các pho đại tượng mang sắc **Trắng ngà ấm (`#FAF6EE`)** từ bi thanh thoát, tương phản với nội điện dát **Vàng đồng cao quý (`#FFD166`)**.

---

## 2. BẢNG MÀU CHUẨN KHÔNG GIAN 3D (THREE.JS ENVIRONMENT & MATERIALS)

### 2.1. Bầu trời & Ánh sáng (Atmosphere & Lighting)

| Thành phần | Mã Hex | RGB | Three.js Hex | Ý nghĩa & Thông số kỹ thuật |
| :--- | :--- | :--- | :--- | :--- |
| **Zenith (Đỉnh trời)** | `#74B4FA` | `116, 180, 250` | `0x74b4fa` | Xanh thiên thanh trong trẻo, khoáng đạt |
| **Horizon (Chân trời)** | `#FFEDC7` | `255, 237, 199` | `0xffedc7` | Vàng kem ban mai, ấm áp, hòa sắc sương nắng |
| **Mặt trời (Sunlight)** | `#FFF1D0` | `255, 241, 208` | `0xfff1d0` | Nắng sớm ấm áp (~5200K), `intensity: 1.55` |
| **Bóng đổ (Shadow)** | `#362C24` | `54, 44, 36` | `0x362c24` | Bóng đổ ấm mềm (PCFSoft), không đen kịt |
| **Hemisphere Sky** | `#E8F4FC` | `232, 244, 252` | `0xe8f4fc` | Tán xạ ánh sáng vòm trời, `intensity: 1.15` |
| **Hemisphere Ground** | `#BBA590` | `187, 165, 144` | `0xbba590` | Phản xạ ấm từ gạch sân, thay thế màu bùn đen cũ |

---

### 2.2. Phân tích Chuyên sâu về Sương mù (Fog System)

#### Vấn đề của Fog hiện tại (`0x2a1a10`):
- **Bản chất màu sắc**: `0x2a1a10` là màu **nâu đen bùn tối (Dark Muddy Pitch Brown)**, RGB: `(42, 26, 16)`.
- **Lỗi kỹ thuật Three.js**: Shader Three.js hòa trộn màu vật thể xa về màu của Fog. Khi cự ly tăng lên, tường chùa vàng rực, hoa giấy hồng tươi, tượng trắng ngà... đều bị nuốt chửng thành những khối đen bẩn.
- **Xung đột thị giác**: Bầu trời nền là xanh sáng (`0x7fb2e5`), nhưng vật thể xa lại biến thành đen (`0x2a1a10`), tạo ra các viền silhouette nham nhở, biến cảnh chùa trang nghiêm thành bối cảnh game kinh dị/nghĩa địa u ám.

#### Giải pháp Chuẩn hóa:
1. **Màu sương mù thay thế**: **`#E6F0F8`** (Morning Atmospheric Sky Mist) hoặc **`#FDF5E6`** (Golden Sun Haze).
2. **Loại sương mù**: Chuyển sang **`THREE.Fog(color, near, far)`** tuyến tính thay vì hàm mũ:
   - `near = 45.0`: Giữ cho không gian tiền cảnh và trung cảnh (sân chùa, lư hương, hoa viên) sắc nét 100%.
   - `far = 180.0` (hoặc `250.0` cho view toàn cảnh): Làm dịu dần hậu cảnh vào đường chân trời.
3. Nếu dùng `THREE.FogExp2`: Color `0xe6f0f8`, mật độ `density = 0.0015` (giảm mạnh từ mức `0.007` cũ).

---

### 2.3. Vật liệu Kiến trúc & Cảnh quan (Architectural & Nature Materials)

| Đối tượng | Màu sắc | Mã Hex | Three.js Hex | Roughness / Metalness | Ghi chú mỹ thuật |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Sân gạch chính** | Paving Stone | `#D1BEB0` | `0xd1beb0` | R: 0.82, M: 0.05 | Đá lát xám kem ấm đón nắng |
| **Lối đi gạch tàu** | Terracotta Pave | `#B86548` | `0xb86548` | R: 0.78, M: 0.04 | Gạch nung đỏ truyền thống miền Tây |
| **Tường Chánh điện** | Colonial Ochre | `#E8C87A` | `0xe8c87a` | R: 0.65, M: 0.08 | Vàng hoàng thổ đặc trưng Nam Bộ |
| **Phào chỉ mosaic** | White Stucco | `#FAF8F2` | `0xfaf8f2` | R: 0.35, M: 0.15 | Khảm sành sứ trắng mờ phản quang |
| **Cột son hiên chùa** | Vermilion Red | `#8B251E` | `0x8b251e` | R: 0.40, M: 0.12 | Sơn son trầm ấm, không dùng đỏ cờ |
| **Mái ngói âm dương**| Terracotta Tile | `#B34728` | `0xb34728` | R: 0.75, M: 0.05 | Màu đất nung chín đỏ ấm |
| **Vệt rêu phong mái**| Ancient Moss | `#526046` | `0x526046` | R: 0.90, M: 0.02 | Rêu phong tự nhiên trên góc mái |
| **Cánh hoa giấy** | Bougainvillea Pink | `#E0367E` | `0xe0367e` | R: 0.45, M: 0.05 | Hồng tím rực rỡ, đón nắng |
| **Chồi hoa giấy non** | Young Pink | `#F285AC` | `0xf285ac` | R: 0.45, M: 0.05 | Hồng phớt ngọn cành |
| **Chậu cảnh đất nung**| Terracotta Pot | `#B85B35` | `0xb85b35` | R: 0.80, M: 0.05 | Chậu tròn đất nung Nam Bộ |
| **Tán cây đón nắng** | Sunlit Emerald | `#4F8534` | `0x4f8534` | R: 0.55, M: 0.05 | Xanh non tràn trề sinh khí |
| **Tán cây bóng râm** | Deep Moss Green | `#23532B` | `0x23532b` | R: 0.65, M: 0.05 | Xanh lục bảo trầm ấm của kiểng cổ |
| **Mặt nước hồ sen** | Serene Lake | `#2D6867` | `0x2d6867` | R: 0.15, M: 0.60 | Xanh ngọc bích tĩnh lặng |
| **Lá sen mặt hồ** | Lotus Leaf | `#3B7E48` | `0x3b7e48` | R: 0.60, M: 0.05 | Xanh ngọc diệp viền bèo |
| **Hoa sen hồng** | Sacred Lotus | `#EB6896` | `0xeb6896` | R: 0.35, M: 0.05 | Hồng sen thanh khiết |

---

### 2.4. Quy chuẩn Màu sắc Tượng Phật (Statues Palette)

1. **Bộ 3 Đại Tượng Lộ Thiên (Di Lặc, A Di Đà, Thích Ca Niết Bàn)**:
   - **Màu chủ đạo:** **Trắng ngà ấm (`#FAF6EE` / `0xfaf6ee`)** hoặc (`#F5EFEB`).
   - **Đặc tính quang học:** Phủ bóng mờ (`Roughness: 0.40`, `Metalness: 0.08`). Ánh sáng mặt trời phản quang tạo sắc ấm áp, thoát tục, tuyệt đối không dùng màu trắng bệch xi măng (`#FFFFFF`) gây chói gắt.
   - **Đài sen Tượng A Di Đà (cao 24m):** Cánh sen màu xanh ngọc bích (`#1F6B4F`) kết hợp viền cánh hồng (`#EB6896`) và nhụy vàng đồng (`#FFD166`).
2. **Hệ thống Tượng Nội Điện (Tam Bảo & 18 Vị La Hán)**:
   - **Màu chủ đạo:** **Vàng đồng cao quý (`#FFD166` / `0xffd166`)** kết hợp vàng hổ phách (`#E5A93C`).
   - **Đặc tính quang học:** Sơn son thếp vàng lộng lẫy (`Roughness: 0.22`, `Metalness: 0.88`, `Emissive: 0x332005` độ rực nhẹ), phản chiếu ánh nến và đèn pháp hoa lung linh.

---

## 3. QUY CHUẨN THIẾT KẾ GIAO DIỆN (UI DESIGN SYSTEM & TOKENS)

### 3.1. Phân bổ Màu sắc Thành phần UI

```
┌────────────────────────────────────────────────────────┐
│ HEADER PILL: Nền Xanh Ngọc Đậm (#1C5A34), Chữ Vàng Kem │
└────────────────────────────────────────────────────────┘

 [D-PAD ĐIỀU HƯỚNG]                    [4 NÚT HÀNH ĐỘNG]
  Vòng xanh rêu đậm (#1F402B)           Nâu hạt dẻ (#58321a)
  Viền vàng đồng (#C9962E)              Viền vàng đồng (#C9962E)
  Mũi tên vàng kem (#FCC86C)            Icon & Chữ vàng kem (#FCC86C)
                                        (Lễ Phật, Dâng hương,
                                         Dâng hoa, Niệm Phật)

┌────────────────────────────────────────────────────────┐
│ MODAL / SHEET PANEL:                                   │
│ Nền kem giấy dó (#FFFCF2), Viền vàng đồng (#C9962E)    │
│ Tiêu đề nâu gỗ (#4A3222), Nút chính Xanh ngọc (#1C5A34)│
│ Nút phụ / Giỏ hàng Cam đất nung (#C96F4A)              │
└────────────────────────────────────────────────────────┘
```

| Thành phần UI | Vai trò | Mã Hex | CSS Variable | Mô tả chi tiết |
| :--- | :--- | :--- | :--- | :--- |
| **Header Pill** | Khung đầu trang | `#1C5A34` | `--ui-header-bg` | Xanh ngọc đậm sang trọng, bo góc tròn viên thuốc |
| **D-pad Base** | Vòng xoay điều hướng | `#1F402B` | `--ui-dpad-bg` | Xanh rêu sẫm trong suốt (opacity 0.85) |
| **D-pad Arrow** | Mũi tên chỉ hướng | `#FCC86C` | `--ui-dpad-arrow` | Vàng kem tương phản rõ ràng |
| **4 Nút Hành Động** | Nền nút tròn góc phải | `#58321a` | `--ui-action-btn-bg` | Nâu hạt dẻ / chocolate bronze ấm áp |
| **Icon 4 Nút** | Biểu tượng thao tác | `#FCC86C` | `--ui-action-btn-icon`| Vàng kem ấm, khắc họa tinh xảo |
| **Viền 4 Nút** | Đường viền thanh lịch | `#C9962E` | `--ui-action-btn-border`| Vàng đồng 1.5px - 2px |
| **Modal / Sheet BG**| Nền thẻ & bảng nổi | `#FFFCF2` | `--ui-modal-bg` | Kem sáng trang nhã, phỏng giấy dó |
| **Modal Border** | Đường bo & phân cách | `#C9962E` | `--ui-gold-border` | Vàng đồng trang nghiêm |
| **Primary CTA** | Nút xác nhận chính | `#1C5A34` | `--ui-btn-primary` | Xanh ngọc đậm thảo mộc (chữ trắng/kem) |
| **Secondary CTA** | Nút giỏ hàng / phụ | `#C96F4A` | `--ui-btn-secondary` | Cam đất nung ấm áp |
| **Text Tiêu đề** | Font serif chính | `#4A3222` | `--ui-text-title` | Nâu gỗ ấm trang trọng |
| **Text Thân bài** | Nội dung mô tả | `#6B5E55` | `--ui-text-body` | Nâu xám mềm, dễ đọc |

---

## 4. CODE MẪU ÁP DỤNG NGAY (READY-TO-USE CODE SNIPPETS)

### 4.1. Cấu hình Three.js (Thay thế hoàn toàn mã v6/v7)

```javascript
// ========================================================
// CHÙA ONLINE — CẤU HÌNH THREE.JS LIGHTING & ATMOSPHERE CHUẨN
// ========================================================

// 1. Scene & Sky Background
scene.background = new THREE.Color(0x74b4fa); // Xanh thiên thanh trong trẻo

// 2. Fog Chuẩn (Thay thế hoàn toàn 0x2a1a10)
// Hòa sắc vào chân trời nắng ấm, giữ tiền cảnh 0-45m trong vắt
scene.fog = new THREE.Fog(0xe6f0f8, 45, 200);

// 3. Renderer Color Space & Tone Mapping
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.05;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;

// 4. Ánh sáng Bầu trời & Mặt đất (HemisphereLight)
// Trời xanh dịu (0xe8f4fc) + Đất gạch nung ấm (0xbba590)
const hemiLight = new THREE.HemisphereLight(0xe8f4fc, 0xbba590, 1.15);
hemiLight.position.set(0, 50, 0);
scene.add(hemiLight);

// 5. Ánh sáng Mặt trời Ban mai (DirectionalLight)
// Nắng vàng ấm 5200K, góc xiên Tây Nam tạo bóng đổ tự nhiên
const sunLight = new THREE.DirectionalLight(0xfff1d0, 1.55);
sunLight.position.set(-35, 30, 22);
sunLight.castShadow = true;
sunLight.shadow.mapSize.width = 2048;
sunLight.shadow.mapSize.height = 2048;
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 150;
sunLight.shadow.camera.left = -50;
sunLight.shadow.camera.right = 50;
sunLight.shadow.camera.top = 50;
sunLight.shadow.camera.bottom = -50;
sunLight.shadow.bias = -0.0005;
scene.add(sunLight);

// 6. Materials Chuẩn
const matStatueIvory = new THREE.MeshStandardMaterial({
  color: 0xfaf6ee, // Trắng ngà ấm cho 3 đại tượng
  roughness: 0.40,
  metalness: 0.08
});

const matBuddhaGold = new THREE.MeshStandardMaterial({
  color: 0xffd166, // Vàng đồng cao quý cho tượng Tam Bảo & La Hán
  roughness: 0.22,
  metalness: 0.88,
  emissive: 0x332005
});

const matPaving = new THREE.MeshStandardMaterial({
  color: 0xd1beb0, // Đá lát sân xám kem ấm
  roughness: 0.82,
  metalness: 0.05
});

const matFacadeOchre = new THREE.MeshStandardMaterial({
  color: 0xe8c87a, // Vàng hoàng thổ Chánh điện
  roughness: 0.65,
  metalness: 0.08
});

const matVermilionCol = new THREE.MeshStandardMaterial({
  color: 0x8b251e, // Cột son đỏ chu sa
  roughness: 0.40,
  metalness: 0.12
});

const matBougainvillea = new THREE.MeshStandardMaterial({
  color: 0xe0367e, // Hoa giấy hồng magenta
  roughness: 0.45,
  metalness: 0.05
});

const matBonsaiGreen = new THREE.MeshStandardMaterial({
  color: 0x23532b, // Tán bonsai xanh ngọc lục bảo ấm
  roughness: 0.65,
  metalness: 0.05
});
```

---

### 4.2. Hệ thống Biến CSS Tokens (UI Design Variables)

```css
:root {
  /* ========================================================
     BẢNG MÃ MÀU CHÙA ONLINE (THEME CHUẨN BAN NGÀY NẮNG ẤM)
     ======================================================== */
  /* Màu chủ đạo */
  --co-primary-green: #1C5A34;     /* Xanh ngọc đậm */
  --co-primary-green-dark: #154527;/* Xanh rêu sẫm */
  --co-gold-accent: #C9962E;       /* Vàng đồng cao quý */
  --co-gold-light: #FFD166;        /* Vàng kim tươi sáng */
  --co-gold-cream: #FCC86C;        /* Vàng kem ánh nến */
  
  /* Nền trang & Panel */
  --co-bg-cream: #FFFCF2;          /* Nền kem sáng mềm mại */
  --co-bg-parchment: #FFF6E5;      /* Nền kem giấy dó */
  --co-card-bg: #FFFFFF;           /* Nền thẻ trắng ngà */

  /* Chữ & Biển hiệu */
  --co-text-title: #4A3222;        /* Nâu gỗ ấm cho tiêu đề */
  --co-text-body: #6B5E55;         /* Nâu xám trầm dễ đọc */
  --co-text-muted: #8F8278;        /* Xám be phụ trợ */

  /* 4 Nút Hành Động (Lễ Phật, Dâng hương, Dâng hoa, Niệm Phật) */
  --co-action-bronze: #58321A;     /* Nâu hạt dẻ / Chocolate Bronze */
  --co-action-bronze-hover: #6E3F21;
  --co-action-icon: #FCC86C;       /* Vàng kem ấm */
  --co-action-border: #C9962E;     /* Viền vàng đồng */

  /* Điểm nhấn phụ */
  --co-accent-terracotta: #C96F4A; /* Cam đất nung (Giỏ hàng, badge) */
  --co-accent-lotus: #EB6896;      /* Hồng sen thanh khiết */
  --co-sky-zenith: #74B4FA;        /* Xanh đỉnh trời */
  --co-sky-horizon: #FFEDC7;       /* Vàng chân trời */

  /* Hiệu ứng bóng & Bo góc */
  --co-radius-pill: 9999px;
  --co-radius-card: 20px;
  --co-radius-modal: 28px;
  --co-shadow-soft: 0 4px 20px rgba(74, 50, 34, 0.08);
  --co-shadow-gold: 0 4px 16px rgba(201, 150, 46, 0.28);
}

/* ========================================================
   STYLING CÁC THÀNH PHẦN UI CỐT LÕI
   ======================================================== */

/* 1. Header Pill */
.chua-header-pill {
  background: var(--co-primary-green);
  border: 1.5px solid rgba(201, 150, 46, 0.45);
  border-radius: var(--co-radius-pill);
  color: var(--co-bg-cream);
  box-shadow: 0 4px 14px rgba(28, 90, 52, 0.25);
  padding: 8px 20px;
  display: flex;
  align-items: center;
  gap: 12px;
}

/* 2. D-pad Controller (Góc dưới trái) */
.chua-dpad-container {
  background: rgba(31, 64, 43, 0.88);
  border: 2px solid var(--co-gold-accent);
  border-radius: 50%;
  backdrop-filter: blur(8px);
  box-shadow: var(--co-shadow-gold);
}
.chua-dpad-btn {
  color: var(--co-gold-cream);
}

/* 3. Bốn Nút Hành Động (Góc dưới phải) */
.chua-action-btn {
  background: var(--co-action-bronze);
  border: 2px solid var(--co-action-border);
  border-radius: var(--co-radius-pill);
  color: var(--co-action-icon);
  box-shadow: 0 4px 14px rgba(88, 50, 26, 0.35);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}
.chua-action-btn:hover {
  background: var(--co-action-bronze-hover);
  border-color: var(--co-gold-light);
  transform: translateY(-2px);
  box-shadow: var(--co-shadow-gold);
}
.chua-action-btn .btn-icon {
  fill: var(--co-action-icon);
}

/* 4. Modal Sheet (Cửa hàng / Giảng đường / Hồi hướng) */
.chua-sheet-modal {
  background: var(--co-bg-cream);
  border: 1.5px solid var(--co-gold-accent);
  border-radius: var(--co-radius-modal);
  box-shadow: 0 12px 36px rgba(74, 50, 34, 0.16);
  color: var(--co-text-body);
}
.chua-sheet-title {
  font-family: 'Playfair Display', Georgia, serif;
  color: var(--co-text-title);
  font-weight: 700;
}
.chua-btn-primary {
  background: var(--co-primary-green);
  color: #FFFFFF;
  border: none;
  border-radius: var(--co-radius-pill);
  font-weight: 600;
}
.chua-btn-secondary {
  background: var(--co-accent-terracotta);
  color: #FFFFFF;
  border: none;
  border-radius: var(--co-radius-pill);
  font-weight: 600;
}
```
