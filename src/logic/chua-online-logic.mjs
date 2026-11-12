/**
 * Pure domain logic for Chùa Online | Chùa Vĩnh Tràng
 * Covers:
 * 1. 9-Zone Spatial Architecture across 14,000 m² Chùa Vĩnh Tràng grounds, D-Pad/WASD movement, collision & radar
 * 2. 3 Rigged 3D Characters (Phật tử Nữ 1.62m, Phật tử Nam 1.74m, Trẻ em 1.15m) & 3D Equipment fitting
 * 3. Spiritual Action State Machine (Lễ Phật, Dâng hương 4 bước, Dâng hoa, Niệm Phật 108 hạt, Thỉnh chuông, Quét lá)
 *    + Dấu Ấn Hành Trình (9 cánh hoa sen thanh tịnh, phi cạnh tranh)
 * 4. Souvenir & 3D Item Catalog (Quà lưu niệm, Đồ tu học, Vật phẩm 3D including 3D Shop Kiosk Model & Southern specialties)
 * 5. Deeply Researched Buddhist Dharma Curriculum (24 lessons + 10 canonical PDF textbooks from /Giáo trình phật học/)
 * 6. UGC Photo Check-in Studio ("Chụp ảnh Check-in Chùa Vĩnh Tràng như thật") & Community Gallery
 */

export const CHARACTER_PROFILES = [
  {
    key: 'nu',
    name: 'Phật tử Nữ (Diệu Tâm)',
    heightLabel: '1.62m',
    heightMeters: 1.62,
    outfitName: 'Áo tràng lam cổ tàu 5 nút (#9A8F99) & Túi vải sen',
    glb: '/Thiết kế giao diện/Nhân vật 3D/Bản chỉnh sửa/nu-phuc-hoi-mau-chuyen-dong.glb',
    previewImg: '/public/assets/aistudio/image_8f6004e3.png',
    fitPreviewImg: '/Thiết kế giao diện/Nhân vật 3D/render-items-nu.jpg',
    description: 'Phật tử nữ mặc áo lam tím khói 5 nút truyền thống, đeo túi tote hoa sen, tóc búi thấp trang nghiêm.'
  },
  {
    key: 'nam',
    name: 'Phật tử Nam (Minh Đức)',
    heightLabel: '1.74m',
    heightMeters: 1.74,
    outfitName: 'Pháp phục Áo tràng nâu / lam trầm & Tràng hạt gỗ',
    glb: '/Thiết kế giao diện/Nhân vật 3D/Chuyển động/nam-chuyen-dong.glb',
    previewImg: '/Thiết kế giao diện/Nhân vật 3D/anh-xem-truoc-3d-nam.png',
    fitPreviewImg: '/Thiết kế giao diện/Nhân vật 3D/render-items-nam-v2.jpg',
    description: 'Phật tử nam chững chạc, khoác pháp phục đi chùa truyền thống, bước đi điềm đạm chánh niệm.'
  },
  {
    key: 'tre_em',
    name: 'Em bé Phật tử (Bé An)',
    heightLabel: '1.15m',
    heightMeters: 1.15,
    outfitName: 'Áo lam thiếu nhi & Búp sen hồng cầm tay',
    glb: '/Thiết kế giao diện/Nhân vật 3D/Chuyển động/tre-em-chuyen-dong.glb',
    previewImg: '/Thiết kế giao diện/Nhân vật 3D/anh-xem-truoc-3d-tre_em.png',
    fitPreviewImg: '/Thiết kế giao diện/Nhân vật 3D/render-items-tre-em-v2.jpg',
    description: 'Em nhỏ Phật tử ngoan hiền theo cha mẹ về Chùa Vĩnh Tràng học lễ Phật, dâng hoa và rèn lòng hiếu thảo.'
  }
];

export const PILGRIMAGE_STATIONS = [
  {
    id: 0,
    key: 'cong_tam_quan',
    name: 'Cổng Tam Quan Ghép Sành Sứ',
    zoneCode: 'Khu 1 · Tiền Đường',
    pinLabel: '⛩️ Cổng Tam Quan',
    pos: { x: 23, z: 40.7 },
    standPos: { x: 23, z: 36.5 },
    via: [[23, 35]],
    mapCoord: { x: 50, y: 88 },
    lookAt: { x: 23, y: 4.2, z: 40.7 },
    audio: 's0_chao.mp3',
    subtitle: 'Nghệ thuật ghép mảnh sành sứ cổ năm 1933. Bước qua cửa Không – Vô Tướng – Vô Tác, buông nhẹ ưu phiền.',
    ritualType: 'welcome'
  },
  {
    id: 1,
    key: 'ho_sen_ca_koi',
    name: 'Hồ Sen Tịnh Thủy & Cầu Đá Cá Koi',
    zoneCode: 'Khu 2 · Song Liên Trì',
    pinLabel: '🪷 Hồ Sen & Cá Koi',
    pos: { x: 5, z: 16 },
    standPos: { x: 16.5, z: 16 },
    via: [[20, 22], [16.5, 16]],
    mapCoord: { x: 34, y: 62 },
    lookAt: { x: 5, y: 0.8, z: 16 },
    audio: 'day_di.mp3',
    subtitle: 'Hai hồ sen lớn tỏa hương thanh khiết trước sân Chánh điện, đàn cá Koi bơi lượn dưới lan can đá.',
    ritualType: 'dang_hoa'
  },
  {
    id: 2,
    key: 'phat_adida',
    name: 'Đại Tượng Phật A Di Đà Đứng (Cao 24m)',
    zoneCode: 'Khu 3 · Hoa Viên Tây',
    pinLabel: '🙏 Tượng Phật A Di Đà',
    pos: { x: -14, z: 28 },
    standPos: { x: -14, z: 14.8 },
    via: [[18, 22], [2, 18], [-10, 15]],
    mapCoord: { x: 18, y: 56 },
    lookAt: { x: -14, y: 9.5, z: 28 },
    audio: 's1_adida.mp3',
    subtitle: 'Đức Phật A Di Đà cao 24m đứng trên đài sen xanh dương phóng quang tiếp dẫn. Chắp tay niệm danh hiệu Ngài để nhiếp tâm.',
    ritualType: 'niem_phat'
  },
  {
    id: 3,
    key: 'phat_di_lac',
    name: 'Đại Tượng Phật Di Lặc Ngồi (Cao 20m)',
    zoneCode: 'Khu 4 · Hoa Viên Đông – Tây',
    pinLabel: '😊 Tượng Phật Di Lặc',
    pos: { x: -24.5, z: -4 },
    standPos: { x: -24.5, z: 9.8 },
    via: [[15, 14], [-8, 10], [-20, 9]],
    mapCoord: { x: 16, y: 38 },
    lookAt: { x: -24.5, y: 7.5, z: -4 },
    audio: 's4_dilac.mp3',
    subtitle: 'Đại tượng Phật Di Lặc cao 20m, nặng 250 tấn giữa hoa viên nhắc ta thực hành hạnh Nhẫn Nhục & Hỷ Xả.',
    ritualType: 'le_phat'
  },
  {
    id: 4,
    key: 'lu_huong_san',
    name: 'Lư Hương Đồng & Sân Chánh Điện',
    zoneCode: 'Khu 5 · Trung Tâm Sân Lễ',
    pinLabel: '🔥 Lư hương Chánh điện',
    pos: { x: 23, z: 11 },
    standPos: { x: 23, z: 16.5 },
    via: [[23, 18]],
    mapCoord: { x: 50, y: 54 },
    lookAt: { x: 23, y: 3.8, z: 2 },
    audio: 's2_thap_nhang.mp3',
    subtitle: 'Dâng ba nén tâm hương: Hương Giới — Hương Định — Hương Tuệ nguyện cầu quốc thái dân an.',
    ritualType: 'dang_huong'
  },
  {
    id: 5,
    key: 'chanh_dien',
    name: 'Chánh Điện Chùa Vĩnh Tràng & 18 La Hán',
    zoneCode: 'Khu 6 · Nội Điện Tam Bảo',
    pinLabel: '📍 Chánh điện',
    pos: { x: 23, z: -1 },
    standPos: { x: 23, z: 7.5 },
    via: [[23, 18], [23, 7.5]],
    mapCoord: { x: 50, y: 40 },
    lookAt: { x: 23, y: 5.2, z: -4 },
    audio: 's3_lay_phat.mp3',
    subtitle: 'Kiến trúc giao thoa Á – Âu độc đáo với 13 nhịp vòm, 7 bộ bao lam thếp vàng và thập bát La Hán gỗ mít năm 1907.',
    ritualType: 'le_phat'
  },
  {
    id: 6,
    key: 'cua_hang_luu_niem',
    name: 'Quầy Cửa Hàng Lưu Niệm Gỗ & Vật Phẩm 3D',
    zoneCode: 'Khu 7 · Hữu Vu Đông',
    pinLabel: '🏮 Cửa hàng lưu niệm',
    pos: { x: 40, z: 38 },
    standPos: { x: 36.5, z: 34.5 },
    via: [[28, 25], [35, 32]],
    mapCoord: { x: 78, y: 66 },
    lookAt: { x: 40, y: 2.4, z: 38 },
    audio: 'merit_box.mp3',
    subtitle: 'Quầy gỗ mái ngói cổ truyền trong sân chùa: chọn quà lưu niệm, pháp khí tu học và gắn vật phẩm 3D lên 3 nhân vật.',
    ritualType: 'shop'
  },
  {
    id: 7,
    key: 'giang_duong',
    name: 'Giảng Đường Phật Pháp & Phòng Kinh Sách',
    zoneCode: 'Khu 8 · Giảng Đường Huệ Đăng',
    pinLabel: '📖 Giảng đường',
    pos: { x: 44, z: -20 },
    standPos: { x: 36, z: -11 },
    via: [[28, 12], [35, 2], [36, -8]],
    mapCoord: { x: 80, y: 28 },
    lookAt: { x: 44, y: 3.5, z: -20 },
    audio: 's3_giang_duong.mp3',
    subtitle: 'Không gian gỗ lim trầm mặc: lắng nghe pháp âm, đọc 10 bộ giáo trình Phật học và học 24 bài thực hành.',
    ritualType: 'lecture'
  },
  {
    id: 8,
    key: 'phat_niet_ban',
    name: 'Đại Tượng Phật Niết Bàn (32m) & Bảo Tháp 7 Tầng',
    zoneCode: 'Khu 9 · Hậu Viên & Bảo Tháp',
    pinLabel: '🌸 Tượng Phật Niết Bàn & Bảo Tháp',
    pos: { x: 12, z: -47 },
    standPos: { x: 12, z: -32.0 },
    via: [[15, 8], [5, 5], [4, -18], [10, -31]],
    mapCoord: { x: 42, y: 16 },
    lookAt: { x: 12, y: 6.5, z: -47 },
    audio: 's5_nirvana.mp3',
    subtitle: 'Chiêm bái tôn tượng Đức Phật nhập Niết Bàn dài 32m và Bảo Tháp Thất Phật cao 35m (7 tầng) nơi hậu viên thanh tịnh.',
    ritualType: 'hoi_huong'
  }
];

export const WORLD_BOUNDS = {
  minX: -38,
  maxX: 53,
  minZ: -52,
  maxZ: 52
};

export function stepPlayerMovement(state, input, speed = 0.22, obstacles = []) {
  const dx = Number(input?.dx || 0);
  const dz = Number(input?.dz || 0);
  if (dx === 0 && dz === 0) {
    return { x: state.x, z: state.z, yaw: state.yaw, moving: false };
  }
  const len = Math.hypot(dx, dz) || 1;
  const nx = dx / len;
  const nz = dz / len;

  let nextX = Math.max(WORLD_BOUNDS.minX, Math.min(WORLD_BOUNDS.maxX, state.x + nx * speed));
  let nextZ = Math.max(WORLD_BOUNDS.minZ, Math.min(WORLD_BOUNDS.maxZ, state.z + nz * speed));

  for (const box of obstacles) {
    if (nextX > box.minX && nextX < box.maxX && nextZ > box.minZ && nextZ < box.maxZ) {
      const slideX = !(state.x > box.minX && state.x < box.maxX && nextZ > box.minZ && nextZ < box.maxZ);
      const slideZ = !(nextX > box.minX && nextX < box.maxX && state.z > box.minZ && state.z < box.maxZ);
      if (slideX) nextX = state.x;
      else if (slideZ) nextZ = state.z;
      else {
        nextX = state.x;
        nextZ = state.z;
      }
    }
  }

  const yaw = Math.atan2(nx, nz);
  return {
    x: Number(nextX.toFixed(4)),
    z: Number(nextZ.toFixed(4)),
    yaw: Number(yaw.toFixed(4)),
    moving: true
  };
}

export function findNearestStation(pos, stations = PILGRIMAGE_STATIONS) {
  let best = stations[0];
  let bestDist = Infinity;
  for (const st of stations) {
    const dPos = Math.hypot((pos?.x || 0) - st.pos.x, (pos?.z || 0) - st.pos.z);
    const dStand = st.standPos
      ? Math.hypot((pos?.x || 0) - st.standPos.x, (pos?.z || 0) - st.standPos.z)
      : Infinity;
    const d = Math.min(dPos, dStand);
    if (d < bestDist) {
      bestDist = d;
      best = st;
    }
  }
  return { station: best, distance: Number(bestDist.toFixed(2)) };
}

export function createSpiritualState(initial = {}) {
  return {
    bowCount: initial.bowCount || 0,
    incenseStep: initial.incenseStep || 0,
    incenseOfferings: initial.incenseOfferings || 0,
    lotusOfferings: initial.lotusOfferings || 0,
    malaBeads: initial.malaBeads || 0,
    malaCycles: initial.malaCycles || 0,
    bellRings: initial.bellRings || 0,
    leavesSwept: initial.leavesSwept || 0,
    visitedStations: Array.isArray(initial.visitedStations) ? [...initial.visitedStations] : [5],
    completedMilestones: Array.isArray(initial.completedMilestones) ? [...initial.completedMilestones] : [],
    lastUnlockedMilestone: initial.lastUnlockedMilestone || null,
    prayers: Array.isArray(initial.prayers) ? [...initial.prayers] : [],
    activeChant: initial.activeChant || 'Nam Mô A Di Đà Phật',
    equippedItems: {
      outfit: initial.equippedItems?.outfit || 'ao_trang_phat_tu',
      hat: initial.equippedItems?.hat || null,
      bag: initial.equippedItems?.bag || 'tui_vai_theu_sen',
      scarf: initial.equippedItems?.scarf || null,
      hand: initial.equippedItems?.hand || 'trang_hat_bo_de',
      altarItem: initial.equippedItems?.altarItem || null
    }
  };
}

export function checkUGCMilestoneUnlock(spiritual, completedLessonsCount = 0) {
  const s = createSpiritualState(spiritual);
  const reasons = [];
  if (s.bowCount >= 3) reasons.push('Đã đảnh lễ Tam Bảo (Tam Bái)');
  if (s.incenseOfferings >= 1) reasons.push('Đã dâng tâm hương tại Lư đồng');
  if (s.lotusOfferings >= 1) reasons.push('Đã dâng hoa sen thanh tịnh');
  if (s.malaCycles * 108 + s.malaBeads >= 3) reasons.push('Đã tịnh tâm lần chuỗi Niệm Phật');
  if (s.visitedStations.length >= 2) reasons.push(`Đã hành hương khám phá ${s.visitedStations.length} điểm trong chùa`);
  if (s.completedMilestones.length >= 1) reasons.push(...s.completedMilestones);
  if (completedLessonsCount >= 2) reasons.push('Đã hoàn thành bài học tại Giảng đường Phật pháp');

  const uniqueReasons = Array.from(new Set(reasons));
  const latest =
    s.lastUnlockedMilestone ||
    uniqueReasons[uniqueReasons.length - 1] ||
    'Hoàn thành 1 nghi lễ (Lễ Phật / Dâng hương / Dâng hoa / Khám phá Hồ sen & Tượng Phật) để mở khóa chụp ảnh Check-in';
  return {
    unlocked: uniqueReasons.length > 0,
    milestoneCount: uniqueReasons.length,
    completedCount: uniqueReasons.length,
    totalCompleted: uniqueReasons.length,
    latestAchievement: latest,
    latestMilestone: latest,
    achievements: uniqueReasons
  };
}

export function recordSpiritualMilestone(state, milestoneLabel) {
  const next = createSpiritualState(state);
  const label = String(milestoneLabel || '').trim();
  if (label && !next.completedMilestones.includes(label)) {
    next.completedMilestones.push(label);
  }
  if (label) {
    next.lastUnlockedMilestone = label;
  }
  return next;
}

export function performSpiritualAction(state, actionType, payload = {}) {
  let next = createSpiritualState(state);
  switch (actionType) {
    case 'LE_PHAT': {
      next.bowCount += 3;
      next = recordSpiritualMilestone(next, 'Đảnh lễ Tam Bảo trước Chánh Điện');
      return {
        state: next,
        animation: 'Vái',
        audioFile: 's3_lay_phat.mp3',
        milestoneUnlocked: true,
        milestoneTitle: 'Đảnh lễ Tam Bảo trước Chánh Điện',
        title: 'Đảnh lễ Tam Bảo (Tam Bái)',
        message: 'Chí tâm đảnh lễ: Nhất bái Phật Bảo — Nhị bái Pháp Bảo — Tam bái Tăng Bảo. Tâm thành kính lễ, thân tâm thanh tịnh.'
      };
    }
    case 'DANG_HUONG_STEP': {
      next.incenseStep = next.incenseStep >= 4 ? 1 : next.incenseStep + 1;
      const stepMessages = {
        1: 'Bước 1/4 — Xin ba nén tâm hương: Hương Giới, Hương Định, Hương Tuệ.',
        2: 'Bước 2/4 — Châm lửa thắp hương và phẩy nhẹ bằng tay (không thổi bằng miệng).',
        3: 'Bước 3/4 — Nâng hương ngang trán, thành tâm khấn nguyện bình an cho gia đạo và chúng sanh.',
        4: 'Bước 4/4 — Cắm hương ngay ngắn vào lư đồng. Khói trầm quyện tỏa trước Chánh điện.'
      };
      if (next.incenseStep === 4) {
        next.incenseOfferings += 1;
        next = recordSpiritualMilestone(next, 'Dâng ba nén tâm hương tại Lư đồng Chánh Điện');
      }
      return {
        state: next,
        animation: next.incenseStep === 4 ? 'Thắp nhang' : 'Chắp tay',
        audioFile: 's2_thap_nhang.mp3',
        milestoneUnlocked: next.incenseStep === 4,
        milestoneTitle: 'Dâng ba nén tâm hương tại Lư đồng Chánh Điện',
        title: `Dâng hương (Bước ${next.incenseStep}/4)`,
        message: stepMessages[next.incenseStep]
      };
    }
    case 'DANG_HUONG_COMPLETE': {
      next.incenseStep = 4;
      next.incenseOfferings += 1;
      next = recordSpiritualMilestone(next, 'Dâng ba nén tâm hương tại Lư đồng Chánh Điện');
      return {
        state: next,
        animation: 'Thắp nhang',
        audioFile: 's2_thap_nhang.mp3',
        milestoneUnlocked: true,
        milestoneTitle: 'Dâng ba nén tâm hương tại Lư đồng Chánh Điện',
        title: 'Dâng tâm hương hoàn mãn',
        message: 'Ba nén hương trầm đã được cắm trang nghiêm vào lư hương đồng trước Chánh điện.'
      };
    }
    case 'DANG_HOA': {
      next.lotusOfferings += 1;
      next.equippedItems.hand = 'hoa_sen_trang_nghiem';
      next = recordSpiritualMilestone(next, 'Dâng hoa sen thanh tịnh bên Hồ Sen Vĩnh Tràng');
      return {
        state: next,
        animation: 'Chắp tay',
        audioFile: 'merit_box.mp3',
        milestoneUnlocked: true,
        milestoneTitle: 'Dâng hoa sen thanh tịnh bên Hồ Sen Vĩnh Tràng',
        title: 'Dâng Hoa Sen Thanh Tịnh',
        message: 'Đạo hữu vừa dâng đóa sen hồng thơm ngát lên Phật đài — biểu trưng cho tâm Bồ Đề trong sáng giữa bụi trần.'
      };
    }
    case 'NIEM_PHAT_BEAD': {
      const increment = Math.max(1, Number(payload.count || 1));
      const total = next.malaBeads + increment;
      next.malaCycles += Math.floor(total / 108);
      next.malaBeads = total % 108;
      if (payload.chant) next.activeChant = payload.chant;
      next = recordSpiritualMilestone(next, `Niệm Phật định tâm (${next.activeChant})`);
      return {
        state: next,
        animation: 'Chắp tay',
        audioFile: 'niem_phat_xa.mp3',
        milestoneUnlocked: true,
        milestoneTitle: `Niệm Phật định tâm (${next.activeChant})`,
        title: `${next.activeChant} (${next.malaBeads}/108)`,
        message:
          total >= 108
            ? `Viên mãn ${next.malaCycles} tràng hạt 108 biến! Tâm niệm lắng trong, phước huệ song tu.`
            : `Từng hạt Bồ Đề lăn nhẹ theo hơi thở chánh niệm (${next.malaBeads}/108 hạt).`
      };
    }
    case 'RING_BELL': {
      next.bellRings += 1;
      next = recordSpiritualMilestone(next, 'Thỉnh chuông Đại Hồng Chung tỉnh thức');
      return {
        state: next,
        animation: 'Chắp tay',
        audioFile: 's6_dan.mp3',
        milestoneUnlocked: true,
        milestoneTitle: 'Thỉnh chuông Đại Hồng Chung tỉnh thức',
        title: 'Thỉnh Chuông Đại Hồng Chung',
        message: 'Nghe tiếng chuông phiền não nhẹ — Trí tuệ lớn, Bồ đề sanh.'
      };
    }
    case 'SWEEP_LEAVES': {
      next.leavesSwept += 1;
      next = recordSpiritualMilestone(next, 'Quét lá sân chùa — Công quả tịnh tâm');
      return {
        state: next,
        animation: 'Di bo',
        audioFile: 'day_di.mp3',
        milestoneUnlocked: true,
        milestoneTitle: 'Quét lá sân chùa — Công quả tịnh tâm',
        title: 'Quét Lá Sân Chùa — Quét Bụi Tâm',
        message: 'Sân chùa sạch bóng lá vàng rơi, lòng người cũng nhẹ bớt tạp niệm.'
      };
    }
    case 'EQUIP_ITEM': {
      const { slot, itemKey } = payload;
      if (slot && Object.prototype.hasOwnProperty.call(next.equippedItems, slot)) {
        next.equippedItems[slot] = next.equippedItems[slot] === itemKey ? null : itemKey;
      }
      return {
        state: next,
        animation: 'Dung',
        title: 'Cập nhật trang phục & pháp khí 3D',
        message: 'Đã cập nhật vật phẩm trên nhân vật Phật tử.'
      };
    }
    default:
      return { state: next, animation: 'Dung', title: '', message: '' };
  }
}

/**
 * Dấu Ấn Hành Trình (9 cánh hoa sen thanh tịnh ứng với 9 điểm hành hương trong chùa)
 * Không dùng thanh EXP, level, điểm số hay danh hiệu cạnh tranh.
 */
export function calculateJourneyImprint(spiritual) {
  const s = createSpiritualState(spiritual);
  const visitedSet = new Set(Array.isArray(s.visitedStations) ? s.visitedStations : [5]);
  const petals = PILGRIMAGE_STATIONS.map((st) => ({
    id: st.id,
    key: st.key,
    name: st.name,
    pinLabel: st.pinLabel,
    zoneCode: st.zoneCode,
    subtitle: st.subtitle,
    lit: visitedSet.has(st.id)
  }));
  const litCount = petals.filter((p) => p.lit).length;
  return {
    petals,
    litCount,
    totalPetals: PILGRIMAGE_STATIONS.length
  };
}

/**
 * Complete Souvenir & 3D Item Catalog matching Reference Image 2 (image_43ca3fb3.png)
 * + 3D Shop Kiosk Model + All 3 Character Fitting Items + Southern Cultural Specialties
 */
export const SHOP_CATALOG = [
  // === TAB 1: QUÀ LƯU NIỆM (First 3 match Reference Image 2 pixel-for-pixel!) ===
  {
    id: 'so_tay_hoa_sen',
    tab: 'souvenir',
    name: 'Sổ tay hoa sen',
    subtitle: 'Bìa vải bố đỏ thêu hoa sen ánh kim kèm dây kẹp vàng',
    price: 125000,
    badge: 'Giao tận nhà',
    deliveryText: 'Giao tận nhà',
    image: '/Thiết kế giao diện/Vật phẩm 3D/models/tham_khao_tui_sen.png',
    cropStyle: {
      bgImage: '/public/assets/aistudio/image_43ca3fb3.png',
      bgSize: '329.3% 489.2%',
      bgPos: '3.37% 67.02%'
    },
    illustrationType: 'lotus_notebook',
    procedural3dId: 'so_tay_hoa_sen',
    glb: '/Thiết kế giao diện/Vật phẩm 3D/Bản chỉnh sửa/tui-vai-sen.glb',
    zip: '/Thiết kế giao diện/Vật phẩm 3D/coohom_packages/coohom_tui_vai_theu_sen.zip',
    equipSlot: 'hand',
    dimensions: '14.5 × 21 × 1.8 cm',
    material: 'Bìa vải linen đỏ huyết dụ dập nổi hoa sen nhũ vàng, giấy kem 100gsm chống lóa',
    meaning: 'Dùng ghi chép lời Phật dạy, nhật ký chánh niệm và những điều biết ơn mỗi ngày sau chuyến hành hương Chùa Vĩnh Tràng.'
  },
  {
    id: 'trang_hat_go',
    tab: 'souvenir',
    name: 'Tràng hạt gỗ',
    subtitle: 'Vòng gỗ Bồ Đề & Hoàng Đàn 108 hạt kết tua rua đỏ truyền thống',
    price: 160000,
    badge: 'Giao tận nhà',
    deliveryText: 'Giao tận nhà',
    image: '/Thiết kế giao diện/Vật phẩm 3D/fixed/fixed_bo_doan_tron.png',
    cropStyle: {
      bgImage: '/public/assets/aistudio/image_43ca3fb3.png',
      bgSize: '329.3% 489.2%',
      bgPos: '50.35% 67.02%'
    },
    illustrationType: 'wooden_mala',
    procedural3dId: 'trang_hat_bo_de',
    glb: '/Thiết kế giao diện/Vật phẩm 3D/fixed/bo_doan_tron.glb',
    zip: '/Thiết kế giao diện/Vật phẩm 3D/coohom_packages/coohom_trang_hat_bo_de.zip',
    equipSlot: 'hand',
    dimensions: 'Đường kính hạt 10 mm · Chu vi 108 hạt',
    material: 'Gỗ Bồ Đề tự nhiên tiện tròn bóng mịn, hương gỗ dịu nhẹ, dây dù đỏ bền chắc',
    meaning: 'Mỗi hạt gỗ nhắc nhở người đeo giữ tâm bình hòa, lần hạt niệm Phật giúp chuyển hóa 108 phiền não.'
  },
  {
    id: 'buu_thiep_chua',
    tab: 'souvenir',
    name: 'Bưu thiếp chùa',
    subtitle: 'Bộ 6 bưu thiếp mỹ thuật Chánh điện Chùa Vĩnh Tràng & phong bì kraft',
    price: 65000,
    badge: 'Giao tận nhà',
    deliveryText: 'Giao tận nhà',
    image: '/Mô hình 3D Vĩnh Tràng/render_vinh_trang_facade.png',
    cropStyle: {
      bgImage: '/public/assets/aistudio/image_43ca3fb3.png',
      bgSize: '329.3% 489.2%',
      bgPos: '96.63% 67.02%'
    },
    illustrationType: 'pagoda_postcard',
    procedural3dId: 'buu_thiep_chua',
    glb: '/Mô hình 3D Vĩnh Tràng/Bản dựng mới/mat-tien-vinh-trang.glb',
    zip: '/Thiết kế giao diện/Vật phẩm 3D/coohom_all_vat_pham_chua_online.zip',
    equipSlot: 'altarItem',
    dimensions: '15 × 10.5 cm (Bộ 6 tấm + 6 phong bì giấy kraft)',
    material: 'Giấy mỹ thuật định lượng 350gsm in màu archival sắc nét mặt tiền Chùa Vĩnh Tràng',
    meaning: 'Gửi trao lời chúc bình an và lưu giữ kỷ niệm chuyến viếng thăm ngôi cổ tự trăm năm miền Tây.'
  },
  {
    id: 'tui_vai_theu_sen',
    tab: 'souvenir',
    name: 'Túi vải bố thêu hoa sen',
    subtitle: 'Túi tote canvas kem đeo vai chuẩn tạo hình 3 nhân vật Nam – Nữ – Trẻ em',
    price: 145000,
    badge: 'Giao tận nhà',
    deliveryText: 'Giao tận nhà',
    image: '/Thiết kế giao diện/Vật phẩm 3D/render-tui-vai-theu-sen-34.png',
    procedural3dId: 'tui_vai_di_chua',
    glb: '/Thiết kế giao diện/Vật phẩm 3D/Bản chỉnh sửa/tui-vai-sen.glb',
    zip: '/Thiết kế giao diện/Vật phẩm 3D/coohom_packages/coohom_tui_vai_theu_sen.zip',
    equipSlot: 'bag',
    dimensions: '34 × 38 × 8 cm',
    material: 'Vải bố canvas mộc dày dặn, thêu nổi hoa sen hồng chỉ lụa',
    meaning: 'Chiếc túi đồng hành cùng người Phật tử mỗi lần đi chùa, đựng kinh sách và vật dụng thanh lịch.'
  },
  {
    id: 'non_la_theu_sen',
    tab: 'souvenir',
    name: 'Nón lá lụa thêu hoa sen',
    subtitle: 'Nón lá miền Tây vành tre thanh thoát đội vừa vặn trên cả 3 nhân vật 3D',
    price: 135000,
    badge: 'Giao tận nhà',
    deliveryText: 'Giao tận nhà',
    image: '/Thiết kế giao diện/Vật phẩm 3D/blender-render-non-la.png',
    procedural3dId: 'non_la_theu_sen',
    glb: '/Thiết kế giao diện/Vật phẩm 3D/models/non_la_blender.glb',
    zip: '/Thiết kế giao diện/Vật phẩm 3D/coohom_packages/coohom_non_la_theu_sen.zip',
    equipSlot: 'hat',
    dimensions: 'Đường kính 41.6 cm × Cao 21 cm',
    material: 'Lá cọ non phơi sương lợp 2 lớp, thêu tay hoa sen hồng Mỹ Tho',
    meaning: 'Che nắng dịu dàng trên sân gạch Chùa Vĩnh Tràng, tôn nét duyên đằm thắm Nam Bộ.'
  },
  {
    id: 'khan_ran_nam_bo',
    tab: 'souvenir',
    name: 'Khăn rằn Nam Bộ thêu sen',
    subtitle: 'Khăn rằn dệt thủ công caro truyền thống điểm hoa sen hồng',
    price: 95000,
    badge: 'Giao tận nhà',
    deliveryText: 'Giao tận nhà',
    image: '/Thiết kế giao diện/Nhân vật 3D/render-items-nam-v2.jpg',
    procedural3dId: 'khan_ran_nam_bo',
    glb: '/Thiết kế giao diện/Vật phẩm 3D/models/ao_trang_phat_tu.glb',
    zip: '/Thiết kế giao diện/Vật phẩm 3D/coohom_packages/coohom_khan_ran_nam_bo.zip',
    equipSlot: 'scarf',
    dimensions: '125 × 55 cm',
    material: '100% sợi bông tự nhiên thấm hút, góc khăn thêu sen tinh tế',
    meaning: 'Biểu tượng nghĩa tình mộc mạc, hiếu khách của đất và người Tiền Giang.'
  },
  {
    id: 'combo_qua_que_mien_tay',
    tab: 'souvenir',
    name: 'Thức quà chay Mỹ Tho (Bánh bò · Bánh da lợn · Dừa xiêm)',
    subtitle: 'Đặc sản chay thanh vị miền Tây gói lá chuối tươi dâng lễ & thưởng thức',
    price: 110000,
    badge: 'Đặc sản chùa quê',
    deliveryText: 'Giao tận nhà',
    image: '/Thiết kế giao diện/Vật phẩm 3D/fixed/fixed_dia_banh_da_lon.png',
    procedural3dId: 'dia_banh_da_lon',
    glb: '/Thiết kế giao diện/Vật phẩm 3D/fixed/dia_banh_da_lon.glb',
    zip: '/Thiết kế giao diện/Vật phẩm 3D/coohom_packages/coohom_dia_banh_da_lon.zip',
    equipSlot: 'altarItem',
    dimensions: 'Khay 24 × 24 × 12 cm',
    material: 'Bột gạo nàng hương, lá dứa tươi, đậu xanh và dừa xiêm ngọt mát Tiền Giang',
    meaning: 'Hương vị quê hương mộc mạc giúp chuyến đi chùa thêm trọn vẹn niềm vui sum vầy.'
  },
  {
    id: 'quat_nan_gio_may',
    tab: 'souvenir',
    name: 'Quạt nan lá dừa & Giỏ mây tre đan thủ công',
    subtitle: 'Bộ đôi phụ kiện đi chùa xanh mát của nghệ nhân làng nghề Tiền Giang',
    price: 115000,
    badge: 'Thủ công xanh',
    deliveryText: 'Giao tận nhà',
    image: '/Thiết kế giao diện/Vật phẩm 3D/fixed/fixed_quat_nan_la_dua.png',
    procedural3dId: 'quat_nan_la_dua',
    glb: '/Thiết kế giao diện/Vật phẩm 3D/fixed/quat_nan_la_dua.glb',
    zip: '/Thiết kế giao diện/Vật phẩm 3D/coohom_packages/coohom_quat_nan_la_dua.zip',
    equipSlot: 'hand',
    dimensions: 'Quạt Ø 28 cm · Giỏ 32 × 26 cm',
    material: 'Lá dừa nước và mây tre tự nhiên đan tay bền đẹp',
    meaning: 'Gió lành mát rượi giữa trưa nắng miền Tây, khuyến khích lối sống xanh thân thiện môi trường.'
  },

  // === TAB 2: ĐỒ TU HỌC (Study & Practice Tools) ===
  {
    id: 'ao_trang_phat_tu',
    tab: 'study',
    name: 'Áo tràng lam Phật tử (Đủ cỡ Nam · Nữ · Trẻ em)',
    subtitle: 'Pháp phục áo lam cổ tàu 5 nút vải đũi tím khói trang nghiêm',
    price: 260000,
    badge: 'Giao tận nhà',
    deliveryText: 'Giao tận nhà',
    image: '/public/assets/aistudio/image_8f6004e3.png',
    procedural3dId: 'ao_trang_phat_tu',
    glb: '/Thiết kế giao diện/Vật phẩm 3D/models/ao_trang_phat_tu.glb',
    zip: '/Thiết kế giao diện/Vật phẩm 3D/coohom_packages/coohom_ao_trang_phat_tu.zip',
    equipSlot: 'outfit',
    dimensions: 'Đủ size Nam (1.74m) / Nữ (1.62m) / Trẻ em (1.15m)',
    material: 'Vải kate lụa & đũi lạnh màu lam tím khói (#9A8F99) thoáng mát, đứng phom',
    meaning: 'Màu lam khói tượng trưng cho hương trầm thanh tịnh, xóa nhòa khoảng cách để cùng hướng về sự giác ngộ.'
  },
  {
    id: 'bo_kinh_phap_cu',
    tab: 'study',
    name: 'Trọn bộ Giáo Trình Phật Học Phổ Thông & Kinh Pháp Cú',
    subtitle: 'Tuyển tập 10 quyển kinh sách căn bản (HT. Thích Thiện Hoa, Walpola Rahula, Ajahn Brahm)',
    price: 245000,
    badge: 'Giao tận nhà',
    deliveryText: 'Giao tận nhà',
    image: '/Thiết kế giao diện/giang-duong-bai-hoc-v2.png',
    procedural3dId: 'so_tay_hoa_sen',
    glb: '/Thiết kế giao diện/Vật phẩm 3D/fixed/mo_go_tung_kinh.glb',
    zip: '/Thiết kế giao diện/Vật phẩm 3D/coohom_all_vat_pham_chua_online.zip',
    equipSlot: 'hand',
    dimensions: 'Bộ hộp 15 × 22 × 8 cm',
    material: 'Bìa cứng bồi vải gấm, giấy kem chống mỏi mắt, tặng kèm bản đọc PDF trực tuyến',
    meaning: 'Kim chỉ nam tu tập Chánh kiến, hiểu thấu Tam Bảo, Tứ Diệu Đế, Nghiệp Báo và Thiền Chánh Niệm.'
  },
  {
    id: 'mo_go_mit_cham_rong',
    tab: 'study',
    name: 'Mõ gỗ mít chạm cá hóa rồng',
    subtitle: 'Mõ tụng kinh gỗ mít già kèm dùi và đệm gấm hoa sen',
    price: 340000,
    badge: 'Giao tận nhà',
    deliveryText: 'Giao tận nhà',
    image: '/Thiết kế giao diện/Vật phẩm 3D/fixed/fixed_mo_go_tung_kinh.png',
    procedural3dId: 'mo_go_tung_kinh',
    glb: '/Thiết kế giao diện/Vật phẩm 3D/fixed/mo_go_tung_kinh.glb',
    zip: '/Thiết kế giao diện/Vật phẩm 3D/coohom_packages/coohom_mo_go_tung_kinh.zip',
    equipSlot: 'altarItem',
    dimensions: '18 × 16 × 15 cm',
    material: 'Gỗ mít lõi già chạm thủ công, âm thanh trầm ấm vang đều',
    meaning: 'Nhắc người tu học luôn tỉnh thức ngày đêm như loài cá không bao giờ nhắm mắt.'
  },
  {
    id: 'chuong_dong_bat_nha',
    tab: 'study',
    name: 'Chuông gia trì đồng Bát Nhã',
    subtitle: 'Chuông đồng đỏ đúc thủ công đặt trên đệm sen gấm',
    price: 420000,
    badge: 'Giao tận nhà',
    deliveryText: 'Giao tận nhà',
    image: '/Thiết kế giao diện/Vật phẩm 3D/fixed/fixed_bat_nhang_tram.png',
    procedural3dId: 'chuong_dong_bat_nha',
    glb: '/Thiết kế giao diện/Vật phẩm 3D/fixed/bat_nhang_tram.glb',
    zip: '/Thiết kế giao diện/Vật phẩm 3D/coohom_packages/coohom_bat_nhang_tram.zip',
    equipSlot: 'altarItem',
    dimensions: 'Đường kính 16 cm × Cao 18 cm',
    material: 'Đồng đỏ pha thiếc theo tỷ lệ cổ truyền, ngân dài trên 18 giây',
    meaning: 'Mỗi tiếng chuông ngân giúp dừng lại dòng suy nghĩ phân tán, trở về hơi thở hiện tại.'
  },
  {
    id: 'toa_sen_ngoi_thien',
    tab: 'study',
    name: 'Bồ đoàn tọa thiền đài sen & Chiếu cói',
    subtitle: 'Đệm ngồi thiền vỏ đậu xanh êm ái như trong Giảng đường Phật pháp',
    price: 280000,
    badge: 'Giao tận nhà',
    deliveryText: 'Giao tận nhà',
    image: '/Thiết kế giao diện/Vật phẩm 3D/fixed/fixed_bo_doan_dai_sen.png',
    procedural3dId: 'bo_doan_dai_sen',
    glb: '/Thiết kế giao diện/Vật phẩm 3D/fixed/bo_doan_dai_sen.glb',
    zip: '/Thiết kế giao diện/Vật phẩm 3D/coohom_packages/coohom_bo_doan_dai_sen.zip',
    equipSlot: 'altarItem',
    dimensions: 'Đường kính 45 cm × Cao 11 cm',
    material: 'Vỏ vải bố gấm thêu cánh sen, ruột bông gòn tự nhiên & vỏ đậu xanh thoáng khí',
    meaning: 'Giúp giữ cột sống thẳng tự nhiên khi ngồi thiền, nghe giảng pháp hoặc tụng kinh tại gia.'
  },
  {
    id: 'bo_am_tra_sen_gom',
    tab: 'study',
    name: 'Bộ ấm trà đạo gốm men ngọc',
    subtitle: 'Ấm trà và 4 chén gốm men ngọc bích kèm khay tre thiền trà',
    price: 390000,
    badge: 'Giao tận nhà',
    deliveryText: 'Giao tận nhà',
    image: '/Thiết kế giao diện/Vật phẩm 3D/fixed/fixed_chum_sanh_hoa_sen.png',
    procedural3dId: 'bo_am_tra_sen_gom',
    glb: '/Thiết kế giao diện/Vật phẩm 3D/fixed/chum_sanh_hoa_sen.glb',
    zip: '/Thiết kế giao diện/Vật phẩm 3D/coohom_packages/coohom_chum_sanh_hoa_sen.zip',
    equipSlot: 'altarItem',
    dimensions: 'Khay 26 × 20 cm · Ấm 280 ml',
    material: 'Gốm nung 1280°C men ngọc lục bảo vẽ nổi cánh sen',
    meaning: 'Thưởng trà trong chánh niệm — nâng chén trà thơm cảm nhận đất trời và tình thân.'
  },

  // === TAB 3: VẬT PHẨM 3D (Includes 3D Shop Kiosk Model + Full 20-item 3D Collection) ===
  {
    id: 'mo_hinh_cua_hang_3d',
    tab: '3d',
    name: 'Mô Hình 3D Quầy Cửa Hàng Lưu Niệm Chùa Vĩnh Tràng',
    subtitle: 'Kiến trúc gỗ mái ngói âm dương, đèn lồng hồng, tượng Phật & kệ vật phẩm 3D',
    price: 680000,
    badge: 'Model Kiến Trúc 3D',
    deliveryText: 'Xem 3D & Tải gói Coohom',
    image: '/public/assets/aistudio/image_43ca3fb3.png',
    procedural3dId: 'kiosk_cua_hang_3d',
    glb: '/Mô hình 3D Vĩnh Tràng/Bản dựng mới/mat-tien-vinh-trang.glb',
    zip: '/Thiết kế giao diện/Vật phẩm 3D/coohom_all_vat_pham_chua_online.zip',
    equipSlot: 'altarItem',
    dimensions: '380 × 240 × 310 cm (Tỷ lệ 1:1 WebGL & Coohom)',
    material: 'Gỗ lim chạm khắc, mái ngói đất nung, đèn lồng lụa hồng & chậu hoa sen gốm men ngọc',
    meaning: 'Tái hiện trọn vẹn không gian Cửa hàng lưu niệm truyền thống bên hiên phải sân Chánh điện Chùa Vĩnh Tràng.'
  },
  {
    id: 'tuong_phat_di_lac_3d',
    tab: '3d',
    name: 'Tượng Phật Di Lặc Cát Tường (3D)',
    subtitle: 'Mô hình 3D GLB chuẩn PBR + gói Coohom & vật phẩm thỉnh về nhà',
    price: 480000,
    badge: '3D + Giao tận nhà',
    deliveryText: 'Thử 3D & Giao tận nhà',
    image: '/Mô hình 3D Vĩnh Tràng/Tượng/di-lac.png',
    procedural3dId: 'tuong_phat_di_lac_3d',
    glb: '/Mô hình 3D Vĩnh Tràng/Tượng/di-lac.glb',
    zip: '/Thiết kế giao diện/Vật phẩm 3D/coohom_all_vat_pham_chua_online.zip',
    equipSlot: 'altarItem',
    dimensions: '24 × 20 × 18 cm',
    material: 'Composite phủ nhũ vàng & gỗ hương chạm khắc dựa theo đại tượng Vĩnh Tràng',
    meaning: 'Biểu tượng của niềm vui hoan hỷ, buông bỏ sân giận và chiêu cảm bình an.'
  },
  {
    id: 'tuong_phat_adida_3d',
    tab: '3d',
    name: 'Tượng Phật A Di Đà Đứng Đài Sen (3D)',
    subtitle: 'Tôn tượng A Di Đà tay bắt ấn tiếp dẫn chuẩn tỷ lệ Vĩnh Tràng',
    price: 520000,
    badge: '3D + Giao tận nhà',
    deliveryText: 'Thử 3D & Giao tận nhà',
    image: '/Mô hình 3D Vĩnh Tràng/Tượng/phat-dung-adida.png',
    procedural3dId: 'tuong_phat_adida_3d',
    glb: '/Mô hình 3D Vĩnh Tràng/Tượng/phat-dung-adida.glb',
    zip: '/Thiết kế giao diện/Vật phẩm 3D/coohom_all_vat_pham_chua_online.zip',
    equipSlot: 'altarItem',
    dimensions: '12 × 12 × 38 cm',
    material: 'Đá cẩm thạch trắng nhân tạo & đế sen mạ vàng trang nghiêm',
    meaning: 'Ánh sáng Vô Lượng Quang — Vô Lượng Thọ soi đường cho người con Phật.'
  },
  {
    id: 'tuong_quan_am_3d',
    tab: '3d',
    name: 'Tượng Bồ Tát Quán Thế Âm (3D)',
    subtitle: 'Tôn tượng Quán Thế Âm cầm bình cam lộ trên đài sen',
    price: 490000,
    badge: '3D + Giao tận nhà',
    deliveryText: 'Thử 3D & Giao tận nhà',
    image: '/Mô hình 3D Vĩnh Tràng/Tượng/phat-ngoi-ban-tho.png',
    procedural3dId: 'tuong_quan_am_3d',
    glb: '/Mô hình 3D Vĩnh Tràng/Tượng/phat-ngoi-ban-tho.glb',
    zip: '/Thiết kế giao diện/Vật phẩm 3D/coohom_all_vat_pham_chua_online.zip',
    equipSlot: 'altarItem',
    dimensions: '12 × 12 × 36 cm',
    material: 'Gốm sứ Bạch Định men trắng ngà thanh khiết',
    meaning: 'Lắng nghe tiếng khổ của thế gian và rưới nước từ bi làm dịu mát tâm hồn.'
  },
  {
    id: 'lu_huong_dong_3d',
    tab: '3d',
    name: 'Lư Hương Đồng & Bát Nhang Trầm (3D)',
    subtitle: 'Lư hương đồng 3 chân quỳ chạm song long chầu nguyệt kèm 3 nén tâm hương',
    price: 450000,
    badge: '3D + Giao tận nhà',
    deliveryText: 'Thử 3D & Giao tận nhà',
    image: '/Thiết kế giao diện/Vật phẩm 3D/fixed/fixed_bat_nhang_tram.png',
    procedural3dId: 'bat_nhang_tram',
    glb: '/Thiết kế giao diện/Vật phẩm 3D/fixed/bat_nhang_tram.glb',
    zip: '/Thiết kế giao diện/Vật phẩm 3D/coohom_packages/coohom_bat_nhang_tram.zip',
    equipSlot: 'altarItem',
    dimensions: '22 × 18 × 24 cm',
    material: 'Đồng vàng giả cổ đúc nổi hoa văn truyền thống',
    meaning: 'Vật phẩm trung tâm của nghi thức dâng hương kết nối tâm nguyện với mười phương chư Phật.'
  },
  {
    id: 'den_hoa_sen_pha_le_3d',
    tab: '3d',
    name: 'Đèn Hoa Sen Pha Lê & Hoa Đăng Cầu An (3D)',
    subtitle: 'Đèn thờ hoa sen pha lê 7 tầng cánh tỏa ánh vàng ấm',
    price: 380000,
    badge: '3D + Giao tận nhà',
    deliveryText: 'Thử 3D & Giao tận nhà',
    image: '/Thiết kế giao diện/Vật phẩm 3D/fixed/fixed_den_hoa_dang.png',
    procedural3dId: 'den_hoa_dang',
    glb: '/Thiết kế giao diện/Vật phẩm 3D/fixed/den_hoa_dang.glb',
    zip: '/Thiết kế giao diện/Vật phẩm 3D/coohom_packages/coohom_den_hoa_dang.zip',
    equipSlot: 'hand',
    dimensions: '14 × 14 × 26 cm',
    material: 'Pha lê K9 tán sắc cao cấp kết hợp đế đồng mạ vàng',
    meaning: 'Dâng đăng cúng Phật tượng trưng cho ngọn đèn trí tuệ xua tan vô minh.'
  },
  {
    id: 'binh_gom_hoa_sen_3d',
    tab: '3d',
    name: 'Bình Gốm Hoa Sen Hồng & Búp Sen Cầm Tay (3D)',
    subtitle: 'Búp sen tươi 3 lớp cánh cầm tay lễ Phật & bình gốm men ngọc',
    price: 310000,
    badge: '3D + Giao tận nhà',
    deliveryText: 'Thử 3D & Giao tận nhà',
    image: '/Thiết kế giao diện/Vật phẩm 3D/fixed/fixed_chum_sanh_hoa_sen.png',
    procedural3dId: 'hoa_sen_tuoi',
    glb: '/Thiết kế giao diện/Vật phẩm 3D/fixed/chum_sanh_hoa_sen.glb',
    zip: '/Thiết kế giao diện/Vật phẩm 3D/coohom_packages/coohom_chum_sanh_hoa_sen.zip',
    equipSlot: 'hand',
    dimensions: '18 × 18 × 35 cm',
    material: 'Bình gốm thủ công và hoa sen lụa phủ sáp như thật',
    meaning: 'Dâng hoa cúng Phật gieo nhân lành tướng hảo, tâm hồn thơm ngát hương đức hạnh.'
  },
  {
    id: 'mam_ngu_qua_3d',
    tab: '3d',
    name: 'Mâm Bồng Ngũ Quả Miền Tây (3D)',
    subtitle: 'Mâm gỗ bày mãng cầu, dừa, đu đủ, xoài, sung dâng cúng Tam Bảo',
    price: 290000,
    badge: '3D + Giao tận nhà',
    deliveryText: 'Thử 3D & Giao tận nhà',
    image: '/Thiết kế giao diện/Vật phẩm 3D/fixed/fixed_mam_ngu_qua.png',
    procedural3dId: 'mam_ngu_qua',
    glb: '/Thiết kế giao diện/Vật phẩm 3D/fixed/mam_ngu_qua.glb',
    zip: '/Thiết kế giao diện/Vật phẩm 3D/coohom_packages/coohom_mam_ngu_qua.zip',
    equipSlot: 'altarItem',
    dimensions: 'Đường kính 28 cm × Cao 22 cm',
    material: 'Mâm gỗ tiện sơn mài và bộ trái cây mỹ thuật Nam Bộ',
    meaning: 'Biểu trưng cho luật Nhân Quả và tấm lòng hiếu kính dâng lên Tam Bảo, tổ tiên.'
  },
  {
    id: 'thac_khoi_tram_huong_3d',
    tab: '3d',
    name: 'Thác Khói Trầm Hương Lá Sen (3D)',
    subtitle: 'Tiểu cảnh thác trầm chảy ngược qua tầng lá sen xanh',
    price: 350000,
    badge: '3D + Giao tận nhà',
    deliveryText: 'Thử 3D & Giao tận nhà',
    image: '/Thiết kế giao diện/Vật phẩm 3D/fixed/fixed_nen_hoa_sen.png',
    procedural3dId: 'nen_hoa_sen',
    glb: '/Thiết kế giao diện/Vật phẩm 3D/fixed/nen_hoa_sen.glb',
    zip: '/Thiết kế giao diện/Vật phẩm 3D/coohom_packages/coohom_nen_hoa_sen.zip',
    equipSlot: 'altarItem',
    dimensions: '18 × 14 × 24 cm',
    material: 'Gốm men lưu ly xanh ngọc chế tác thủ công',
    meaning: 'Dòng khói trắng chảy nhẹ nhàng nhắc nhở sự vô thường và tĩnh lặng.'
  },
  {
    id: 'den_long_luc_giac_3d',
    tab: '3d',
    name: 'Đèn Lồng Gỗ Lục Giác Chùa Cổ (3D)',
    subtitle: 'Đèn lồng khung gỗ sáu cạnh lồng lụa vẽ sen hồng',
    price: 330000,
    badge: '3D + Giao tận nhà',
    deliveryText: 'Thử 3D & Giao tận nhà',
    image: '/Thiết kế giao diện/Vật phẩm 3D/fixed/fixed_den_long_luc_giac.png',
    procedural3dId: 'den_long_luc_giac',
    glb: '/Thiết kế giao diện/Vật phẩm 3D/fixed/den_long_luc_giac.glb',
    zip: '/Thiết kế giao diện/Vật phẩm 3D/coohom_packages/coohom_den_long_luc_giac.zip',
    equipSlot: 'altarItem',
    dimensions: '26 × 26 × 42 cm',
    material: 'Gỗ tràm chạm hoa văn cổ điển, vải lụa xuyên sáng ấm áp',
    meaning: 'Tái hiện vẻ đẹp kiến trúc truyền thống rực rỡ nơi hiên chùa và quầy lưu niệm.'
  },
  {
    id: 'the_go_cau_an_3d',
    tab: '3d',
    name: 'Thẻ Gỗ Cầu An Khắc Hoa Sen (3D)',
    subtitle: 'Thẻ gỗ thông khắc chữ Bình An treo dây kết Cát Tường đỏ',
    price: 75000,
    badge: '3D + Giao tận nhà',
    deliveryText: 'Thử 3D & Giao tận nhà',
    image: '/Thiết kế giao diện/Vật phẩm 3D/fixed/fixed_gio_may_tre.png',
    procedural3dId: 'the_go_cau_an_3d',
    glb: '/Thiết kế giao diện/Vật phẩm 3D/fixed/gio_may_tre.glb',
    zip: '/Thiết kế giao diện/Vật phẩm 3D/coohom_packages/coohom_gio_may_tre.zip',
    equipSlot: 'hand',
    dimensions: '9 × 14 × 0.8 cm',
    material: 'Gỗ thông khắc laser sắc nét, dây tết Cát Tường đỏ thắm',
    meaning: 'Ghi lời nguyện ước tốt lành gửi lại cây ước nguyện hoặc treo nơi góc học tập.'
  },
  {
    id: 'chau_bonsai_mai_chieu_thuy_3d',
    tab: '3d',
    name: 'Chậu Bonsai Mai Chiếu Thủy & Chum Sành Sen (3D)',
    subtitle: 'Cây cảnh bonsai dáng trực lắc và chum sành hoa sen sân Chùa Vĩnh Tràng',
    price: 550000,
    badge: '3D + Giao tận nhà',
    deliveryText: 'Thử 3D & Giao tận nhà',
    image: '/Thiết kế giao diện/Vật phẩm 3D/fixed/fixed_chum_sanh_hoa_sen.png',
    procedural3dId: 'chum_sanh_hoa_sen',
    glb: '/Thiết kế giao diện/Vật phẩm 3D/fixed/chum_sanh_hoa_sen.glb',
    zip: '/Thiết kế giao diện/Vật phẩm 3D/coohom_packages/coohom_chum_sanh_hoa_sen.zip',
    equipSlot: 'altarItem',
    dimensions: '32 × 26 × 38 cm',
    material: 'Chậu đất nung đỏ truyền thống & mô hình bonsai tỉ mỉ từng tán lá',
    meaning: 'Vẻ đẹp kiên cường, sum suê và thanh tao của vườn kiểng cổ tự miền Tây.'
  }
];

export function filterShopCatalog(tab = 'souvenir', searchQuery = '') {
  const q = String(searchQuery || '').trim().toLowerCase();
  return SHOP_CATALOG.filter((item) => {
    const matchTab = tab === 'all' ? true : item.tab === tab;
    if (!matchTab) return false;
    if (!q) return true;
    return (
      item.name.toLowerCase().includes(q) ||
      item.subtitle.toLowerCase().includes(q) ||
      item.meaning.toLowerCase().includes(q)
    );
  });
}

export function addToCart(cart, productId, qty = 1) {
  const product = SHOP_CATALOG.find((p) => p.id === productId);
  if (!product) return [...cart];
  const next = cart.map((entry) => ({ ...entry }));
  const existing = next.find((entry) => entry.id === productId);
  if (existing) {
    existing.qty = Math.min(99, existing.qty + Math.max(1, qty));
  } else {
    next.push({
      id: product.id,
      name: product.name,
      price: product.price,
      image: product.image,
      tab: product.tab,
      qty: Math.max(1, qty)
    });
  }
  return next;
}

export function updateCartQuantity(cart, productId, delta) {
  const next = [];
  for (const item of cart) {
    if (item.id === productId) {
      const updatedQty = item.qty + delta;
      if (updatedQty > 0) {
        next.push({ ...item, qty: Math.min(99, updatedQty) });
      }
    } else {
      next.push({ ...item });
    }
  }
  return next;
}

export function calculateCartSummary(cart) {
  const totalCount = cart.reduce((sum, item) => sum + (item.qty || 0), 0);
  const subtotal = cart.reduce((sum, item) => sum + (item.price || 0) * (item.qty || 0), 0);
  const shippingFee = totalCount === 0 ? 0 : subtotal >= 300000 ? 0 : 25000;
  return {
    totalCount,
    subtotal,
    shippingFee,
    grandTotal: subtotal + shippingFee
  };
}

export function validateOrderForm(form) {
  const name = String(form?.name || '').trim();
  const phone = String(form?.phone || '').replace(/\s+/g, '');
  const address = String(form?.address || '').trim();
  const errors = {};
  if (name.length < 2) errors.name = 'Vui lòng nhập họ tên người nhận.';
  if (!/^(0|\+84)[0-9]{8,10}$/.test(phone)) {
    errors.phone = 'Số điện thoại chưa hợp lệ (gồm 9–11 chữ số).';
  }
  if (address.length < 6) errors.address = 'Vui lòng nhập địa chỉ giao hàng chi tiết.';
  return {
    valid: Object.keys(errors).length === 0,
    errors
  };
}

/**
 * 10 Canonical Buddhist Textbooks available in /Giáo trình phật học/
 */
export const DHARMA_TEXTBOOKS = [
  {
    id: 'phpt_1',
    title: 'Phật Học Phổ Thông — Quyển 1 (Khóa I, II, III)',
    author: 'Hòa thượng Thích Thiện Hoa',
    pdfPath: '/Giáo trình phật học/Phật học phổ thông 1.pdf',
    coreTeachings: 'Trình bày hệ thống từ Quy Y Tam Bảo, Ngũ Giới, Thập Thiện, Tứ Nhiếp Pháp đến Nhân Quả, Luân Hồi và Tứ Diệu Đế theo phương pháp sư phạm dễ hiểu cho Phật tử tại gia.'
  },
  {
    id: 'phpt_3',
    title: 'Phật Học Phổ Thông — Quyển 3 (Lục Độ & Đại Thừa)',
    author: 'Hòa thượng Thích Thiện Hoa',
    pdfPath: '/Giáo trình phật học/Phật học phổ thông 3.pdf',
    coreTeachings: 'Đi sâu vào Tứ Vô Lượng Tâm (Từ, Bi, Hỷ, Xả), Lục Độ Ba La Mật và tinh thần Bồ Tát Đạo nhập thế cứu khổ.'
  },
  {
    id: 'duc_phat_day_nhung_gi',
    title: 'Đức Phật Dạy Những Gì (What the Buddha Taught)',
    author: 'HT. Walpola Rahula · Ni sư Trí Hải dịch',
    pdfPath: '/Giáo trình phật học/duc-phat-day-nhung-gi-ht-walpola-rahula-ns-tri-hai-dich.pdf',
    coreTeachings: 'Kiệt tác Phật học thế giới giải thích chuẩn xác thái độ tâm thức Phật giáo, Tứ Diệu Đế, thuyết Vô Ngã (Anatta), Duyên Khởi và Thiền Chánh Niệm.'
  },
  {
    id: 'nen_tang_1_tam_bao',
    title: 'Nền Tảng Phật Giáo — Quyển 1: Tam Bảo',
    author: 'Tỳ kheo Giác Giới',
    pdfPath: '/Giáo trình phật học/nen-tang-phat-giao-quyen-1-tam-bao.pdf',
    coreTeachings: 'Giải thích rõ ân đức của Phật Bảo (Tự giác, Giác tha, Giác hạnh viên mãn), Pháp Bảo (Thiết thực hiện tại, vượt thời gian) và Tăng Bảo.'
  },
  {
    id: 'nen_tang_2_quy_y',
    title: 'Nền Tảng Phật Giáo — Quyển 2: Quy Y Tam Bảo',
    author: 'Tỳ kheo Giác Giới',
    pdfPath: '/Giáo trình phật học/nen-tang-phat-giao-quyen-2-quy-y-tam-bao.pdf',
    coreTeachings: 'Làm sáng tỏ ý nghĩa Quy y nội tâm (quay về tự tính giác ngộ) và Quy y ngoại tướng, cùng các điều làm thành tựu hay đứt mẻ giới quy y.'
  },
  {
    id: 'nen_tang_4_nghiep',
    title: 'Nền Tảng Phật Giáo — Quyển 4: Nghiệp và Quả của Nghiệp',
    author: 'Tỳ kheo Giác Giới',
    pdfPath: '/Giáo trình phật học/nen-tang-phat-giao-quyen-4-nghiep-va-qua-cua-nghiep.pdf',
    coreTeachings: 'Phân tích Cố ý (Tác ý - Cetanā) chính là Nghiệp, 10 bất thiện nghiệp, 10 thiện nghiệp và phương pháp chuyển hóa trọng nghiệp bằng tu tâm.'
  },
  {
    id: 'nen_tang_5_phuoc',
    title: 'Nền Tảng Phật Giáo — Quyển 5: Phước Thiện (Puñña)',
    author: 'Tỳ kheo Giác Giới',
    pdfPath: '/Giáo trình phật học/nen-tang-phat-giao-quyen-quyen-5-phuoc-thien.pdf',
    coreTeachings: 'Mười cội phước thiện (Thập phúc nghiệp sự): Bố thí, Trì giới, Tham thiền, Cung kính, Phục vụ, Hồi hướng phước, Tùy hỷ phước, Thính pháp, Thuyết pháp và Chánh kiến.'
  },
  {
    id: 'thien_ajahn_brahm',
    title: 'Phương Pháp Thiền Căn Bản (Basic Method of Meditation)',
    author: 'Thiền sư Ajahn Brahm',
    pdfPath: '/Giáo trình phật học/phuong-phap-thien-can-ban-ajahn-brahm-tieng-viet.pdf',
    coreTeachings: 'Hướng dẫn từng bước buông xả quá khứ và tương lai, an trú trong hiện tại tĩnh lặng và theo dõi hơi thở êm dịu dẫn vào định.'
  },
  {
    id: 'tich_truyen_phap_cu',
    title: 'Tích Truyện Pháp Cú (Dhammapada Commentary)',
    author: 'Bản dịch Việt ngữ',
    pdfPath: '/Giáo trình phật học/tichtruyenphapcu.pdf',
    coreTeachings: 'Những câu chuyện lịch sử sinh động thời Đức Phật gắn liền với 423 bài kệ Kinh Pháp Cú — bài học nhân sinh sâu sắc.'
  },
  {
    id: 'tu_duong_tam_tu',
    title: 'Tu Dưỡng Tâm Từ Bằng Thiền Chánh Niệm',
    author: 'Giáo trình Thiền Tứ Niệm Xứ & Tâm Từ',
    pdfPath: '/Giáo trình phật học/tu-duong-tam-tu-bang-thien-chanh-niem.pdf',
    coreTeachings: 'Kết hợp Quán thân thọ tâm pháp (Satipatthana) với thiền Rải Tâm Từ (Metta Bhavana) để chữa lành tổn thương và nuôi dưỡng lòng bi mẫn.'
  }
];

export const LECTURE_PATHS = [
  {
    id: 'A',
    code: 'Gói A',
    title: 'Nhập môn Phật pháp căn bản',
    subtitle: 'Theo Phật Học Phổ Thông (HT. Thích Thiện Hoa) & Nền Tảng Phật Giáo: Tam Bảo, Ngũ Giới, Nhân Quả',
    duration: '6 bài học · 75 phút',
    audioTrack: 's3_giang_duong.mp3'
  },
  {
    id: 'B',
    code: 'Gói B',
    title: 'Kinh điển & Lời Phật dạy tinh yếu',
    subtitle: 'Theo Đức Phật Dạy Những Gì (Walpola Rahula) & Tích Truyện Pháp Cú: Tâm Kinh, Từ Bi, Niệm Phật',
    duration: '6 bài học · 80 phút',
    audioTrack: 'niem_phat_xa.mp3'
  },
  {
    id: 'C',
    code: 'Gói C',
    title: 'Thiền chánh niệm & Sống an đời thường',
    subtitle: 'Theo Phương Pháp Thiền Căn Bản (Ajahn Brahm) & Tu Dưỡng Tâm Từ: Hơi thở, Lắng nghe, Hiếu đạo',
    duration: '6 bài học · 70 phút',
    audioTrack: 's6_dan.mp3'
  },
  {
    id: 'D',
    code: 'Gói D',
    title: 'Di sản & Nghi lễ Chùa Vĩnh Tràng',
    subtitle: 'Lịch sử cổ tự Vĩnh Tràng 1849, kiến trúc Á – Âu, 18 vị La Hán và nghi thức đi chùa đúng pháp',
    duration: '6 bài học · 65 phút',
    audioTrack: 's0_chao.mp3'
  }
];

export const LECTURE_LESSONS = [
  {
    id: 'A1',
    pathId: 'A',
    order: 1,
    title: 'Tam Bảo là gì? Ý nghĩa Phật – Pháp – Tăng',
    duration: '12 phút',
    audio: 's3_giang_duong.mp3',
    sourceBook: 'Nền Tảng Phật Giáo Quyển 1: Tam Bảo & Phật Học Phổ Thông Q.1',
    summary: [
      'Phật Bảo (Buddha) là Đấng Tự Giác, Giác Tha, Giác Hạnh Viên Mãn — bậc Đạo sư chỉ đường sáng suốt.',
      'Pháp Bảo (Dhamma) là phương thuốc nhiệm mầu gồm Giáo pháp và Chứng pháp có công năng diệt trừ phiền não.',
      'Tăng Bảo (Sangha) là đoàn thể thanh tịnh cùng tu tập, giữ gìn và truyền trao mạng mạch Chánh pháp.'
    ],
    example: 'Khi vào Chánh điện Chùa Vĩnh Tràng lạy 3 lạy (Tam Bái), mỗi lạy là sự trở về nương tựa nơi Phật (Tỉnh thức), Pháp (Chánh kiến) và Tăng (Hòa hợp thanh tịnh).',
    practice: 'Hôm nay khi chắp tay trước ngực, hãy thở vào thật sâu và thầm nhủ: "Con về nương tựa Phật, người đưa đường chỉ lối cho con trong cuộc đời."',
    quiz: {
      question: 'Trong giáo lý Tam Bảo (Phật Học Phổ Thông), yếu tố nào được ví như "phương thuốc lành" trực tiếp chữa lành bệnh khổ đau trong tâm?',
      options: ['Phật Bảo (Vị lương y)', 'Pháp Bảo (Phương thuốc lành)', 'Tăng Bảo (Người chăm sóc hướng dẫn)'],
      correctIndex: 1,
      explanation: 'HT. Thích Thiện Hoa giảng: Đức Phật như vị lương y giỏi, Pháp Bảo là phương thuốc nhiệm mầu, Tăng Bảo là y tá tận tâm hướng dẫn bệnh nhân uống thuốc.'
    }
  },
  {
    id: 'A2',
    pathId: 'A',
    order: 2,
    title: 'Quy Y Tam Bảo & Năm Giới quý báu của người tại gia',
    duration: '13 phút',
    audio: 's0_nhan_nhang.mp3',
    sourceBook: 'Nền Tảng Phật Giáo Quyển 2: Quy Y Tam Bảo',
    summary: [
      'Quy (quay về) Y (nương tựa): Quay từ bờ mê lầm về nương tựa ánh sáng Giác – Chánh – Tịnh.',
      'Năm giới gồm: Không sát sanh, Không trộm cắp, Không tà hạnh, Không nói dối/lời ác, Không say sưa nghiện ngập.',
      'Giữ 5 giới là 5 món quà bình an (Ngũ đại thí) hiến tặng cho gia đình và xã hội.'
    ],
    example: 'Trước khi nói lời nóng giận với người thân, người Phật tử nhớ đến giới thứ tư (Chánh ngữ & Ái ngữ) để chọn lời nói ôn hòa.',
    practice: 'Chọn 1 trong 5 giới để thực hành trọn vẹn trong 24 giờ tới, bắt đầu từ lời nói chân thật và dịu dàng.',
    quiz: {
      question: 'Bản chất thực sự của Năm Giới (Ngũ Giới) trong đạo Phật là gì?',
      options: [
        'Những hình phạt bắt buộc của nhà chùa',
        'Năm nguyên tắc đạo đức tự nguyện giúp bảo vệ tự do và bình an cho mình và muôn loài',
        'Chỉ dành riêng cho người xuất gia'
      ],
      correctIndex: 1,
      explanation: 'Ngũ giới là hàng rào đạo đức tự nguyện bảo vệ hạnh phúc gia đình, giúp hành giả sống không hối hận (vô tác hối).'
    }
  },
  {
    id: 'A3',
    pathId: 'A',
    order: 3,
    title: 'Tứ Diệu Đế: Bốn sự thật nhiệm mầu (Đức Phật Dạy Những Gì)',
    duration: '14 phút',
    audio: 's3_giang_duong.mp3',
    sourceBook: 'Đức Phật Dạy Những Gì — HT. Walpola Rahula (NS. Trí Hải dịch)',
    summary: [
      'Khổ Đế (Dukkha): Nhận diện trung thực tính bất toàn, vô thường của thế gian mà không bi quan.',
      'Tập Đế (Samudaya): Thấy rõ gốc rễ của khổ là Ái dục (Tanha) đi kèm chấp thủ và vô minh.',
      'Diệt Đế (Nirodha) & Đạo Đế (Magga): Niết Bàn tịch tịnh có thể chứng nghiệm ngay trong hiện tại nhờ Bát Chánh Đạo.'
    ],
    example: 'Khi gặp chuyện buồn, thay vì trách hoàn cảnh, ta dùng Tứ Diệu Đế như bác sĩ bắt mạch: biết rõ nỗi khổ (Tri khổ), buông nguyên nhân chấp trước (Đoạn tập), và thở chánh niệm (Tu đạo).',
    practice: 'Ghi nhận một điều đang làm bạn căng thẳng hôm nay và tìm xem sự đòi hỏi quá mức nào phía sau đang tạo nên áp lực đó.',
    quiz: {
      question: 'Theo tác phẩm "Đức Phật Dạy Những Gì" của HT. Walpola Rahula, thái độ của đạo Phật khi nói về Khổ Đế là gì?',
      options: [
        'Bi quan chán đời',
        'Hiện thực và sáng suốt như vị y sĩ chẩn đoán đúng bệnh để chữa lành dứt điểm',
        'Lạc quan giả tạo'
      ],
      correctIndex: 1,
      explanation: 'Đức Phật không bi quan cũng không lạc quan mù quáng, mà là bậc Hiện Thực (Yathābhūta) nhìn thẳng sự thật để giải thoát.'
    }
  },
  {
    id: 'A4',
    pathId: 'A',
    order: 4,
    title: 'Nghiệp (Kamma) & Mười Cội Phước Thiện (Puñña)',
    duration: '12 phút',
    audio: 's6_dan.mp3',
    sourceBook: 'Nền Tảng Phật Giáo Quyển 4 & Quyển 5 (Nghiệp & Phước Thiện)',
    summary: [
      'Đức Phật định nghĩa: "Này các Tỳ kheo, Tác ý (Cetanā - sự cố ý) chính là Nghiệp".',
      'Mười cội phước thiện gồm: Bố thí, Trì giới, Tham thiền, Cung kính, Phục vụ, Hồi hướng, Tùy hỷ, Thính pháp, Thuyết pháp, Chánh kiến.',
      'Nhân quả không phải thuyết định mệnh; gieo thiện nghiệp hiện tại sẽ chuyển hóa tương lai.'
    ],
    example: 'Khi bạn bấm "Hồi hướng công đức" hoặc vui mừng trước ảnh đi chùa của Phật tử khác (Tùy hỷ phước), bạn đã thành tựu cội phước thiện thanh cao.',
    practice: 'Thực hiện 3 cội phước không tốn tiền hôm nay: Cung kính người lớn, Phục vụ giúp đỡ việc nhỏ, và Tùy hỷ niềm vui của người khác.',
    quiz: {
      question: 'Theo Kinh Tăng Chi Bộ (được trích trong Nền Tảng Phật Giáo Q.4), yếu tố cốt lõi nào quyết định một hành động trở thành Nghiệp (Kamma)?',
      options: [
        'Sự ngẫu nhiên vô tình',
        'Tác ý (Cetanā — Ý chí chủ tâm thiện hoặc bất thiện khi tạo tác bằng Thân, Khẩu, Ý)',
        'Sự phán xét của người ngoài'
      ],
      correctIndex: 1,
      explanation: '"Cetanāhaṃ bhikkhave kammaṃ vadāmi" — Chính Tác ý (ý chủ tâm) là hạt nhân tạo thành Nghiệp.'
    }
  },
  {
    id: 'A5',
    pathId: 'A',
    order: 5,
    title: 'Bát Chánh Đạo & Tam Vô Lậu Học (Giới – Định – Tuệ)',
    duration: '13 phút',
    audio: 's3_giang_duong.mp3',
    sourceBook: 'Phật Học Phổ Thông Quyển 1 & Đức Phật Dạy Những Gì',
    summary: [
      'Tám chi phần chân chánh gom vào 3 môn học giải thoát (Tam vô lậu học): Giới học, Định học và Tuệ học.',
      'Tuệ học: Chánh kiến & Chánh tư duy. Giới học: Chánh ngữ, Chánh nghiệp, Chánh mạng. Định học: Chánh tinh tấn, Chánh niệm, Chánh định.',
      'Giữ Giới giúp tâm không loạn (sinh Định); tâm Định tĩnh như mặt hồ phẳng lặng sẽ chiếu sáng Trí Tuệ.'
    ],
    example: 'Khi điều khiển nhân vật đi từng bước trên sân gạch Chùa Vĩnh Tràng, sự chú tâm lắng nghe tiếng bước chân và chuông chùa chính là thực tập Chánh niệm.',
    practice: 'Dành 5 phút đi bộ chậm rãi mà không nhìn điện thoại, cảm nhận rõ từng bước chân chạm đất.',
    quiz: {
      question: 'Ba trụ cột chính (Tam vô lậu học) bao trùm toàn bộ 8 chi phần Bát Chánh Đạo là gì?',
      options: ['Giới – Định – Tuệ', 'Phước – Lộc – Thọ', 'Danh – Lợi – Quyền'],
      correctIndex: 0,
      explanation: 'Tám nhánh Bát Chánh Đạo kết tinh thành Giới – Định – Tuệ, ba trụ cột nâng đỡ toàn bộ tòa nhà Phật pháp.'
    }
  },
  {
    id: 'A6',
    pathId: 'A',
    order: 6,
    title: 'Lục Độ Ba La Mật & Tứ Vô Lượng Tâm (Từ – Bi – Hỷ – Xả)',
    duration: '11 phút',
    audio: 's6_hoi_huong.mp3',
    sourceBook: 'Phật Học Phổ Thông Quyển 3 — HT. Thích Thiện Hoa',
    summary: [
      'Sáu phép thực hành đưa sang bờ giác: Bố thí, Trì giới, Nhẫn nhục, Tinh tấn, Thiền định, Trí tuệ.',
      'Tứ Vô Lượng Tâm: Từ (ban vui), Bi (cứu khổ), Hỷ (vui theo điều lành của người), Xả (buông bỏ thành kiến phân biệt).',
      'Nhẫn nhục và Hỷ xả là sức mạnh nội tâm lớn nhất trước nghịch cảnh.'
    ],
    example: 'Chiêm ngưỡng nụ cười của Đại tượng Phật Di Lặc tại Chùa Vĩnh Tràng giúp ta học hạnh Nhẫn nhục và Hỷ xả.',
    practice: 'Hoàn thành cả 6 nhiệm vụ trong bảng "Hành Trình Lục Độ Ba La Mật" của ứng dụng Chùa Online.',
    quiz: {
      question: 'Trong Lục Độ Ba La Mật, hạnh nào giúp bảo hộ rừng công đức không bị ngọn lửa sân giận thiêu rụi?',
      options: ['Bố thí', 'Nhẫn nhục Ba La Mật', 'Tinh tấn'],
      correctIndex: 1,
      explanation: 'Kinh dạy "Nhất niệm sân tâm khởi, bách vạn chướng môn khai", nên Nhẫn nhục giúp giữ trọn công đức lành.'
    }
  },

  // === GÓI B (6 bài) ===
  {
    id: 'B1',
    pathId: 'B',
    order: 1,
    title: 'Kinh Pháp Cú & Tích Truyện: Tâm dẫn đầu các pháp',
    duration: '14 phút',
    audio: 's6_ke_1.mp3',
    sourceBook: 'Tích Truyện Pháp Cú (Phẩm Song Yếu — Kệ số 1 & 2)',
    summary: [
      'Kệ số 1 (Tích thầy Tỳ kheo Cakkhupāla): "Ý dẫn đầu các pháp, Ý làm chủ, ý tạo".',
      'Nói hay làm với tâm ô nhiễm thì khổ đau theo sau như bánh xe theo chân con bò kéo.',
      'Kệ số 2 (Tích chàng Matthakundalī): Nói hay làm với tâm thanh tịnh thì an lạc theo sau như bóng không rời hình.'
    ],
    example: 'Chàng thanh niên Matthakundalī chỉ khởi tâm thành kính hướng về Đức Phật trên giường bệnh mà được sinh cảnh giới an lành — chứng minh sức mạnh của một niệm tâm thanh tịnh.',
    practice: 'Mỗi sáng thức dậy, khởi một ý niệm thiện lành đầu tiên chúc bình an cho gia đình và muôn loài.',
    quiz: {
      question: 'Theo tích truyện kệ số 1 & 2 Kinh Pháp Cú, yếu tố nào dẫn đầu và quyết định tính chất thiện/ác của mọi hành động?',
      options: ['Hoàn cảnh bên ngoài', 'Tâm ý (Ý làm chủ, ý tạo)', 'Tiền tài danh vọng'],
      correctIndex: 1,
      explanation: '"Ý dẫn đầu các pháp, ý làm chủ, ý tạo" — giữ tâm trong sáng là gốc của mọi an vui.'
    }
  },
  {
    id: 'B2',
    pathId: 'B',
    order: 2,
    title: 'Bát Nhã Tâm Kinh: Quán chiếu Duyên Khởi & Vô Ngã',
    duration: '15 phút',
    audio: 'niem_phat_xa.mp3',
    sourceBook: 'Bát Nhã Tâm Kinh & Đức Phật Dạy Những Gì (Chương Vô Ngã)',
    summary: [
      '"Chiếu kiến ngũ uẩn giai không, độ nhất thiết khổ ách": Thấy rõ 5 uẩn (Sắc, Thọ, Tưởng, Hành, Thức) do duyên hợp nên vượt qua khổ đau.',
      'Tính Không (Śūnyatā) không phải là hư vô, mà là vạn pháp tương tức, không có cái tôi biệt lập bất biến.',
      'Nhờ vô thường và duyên khởi mà nỗi khổ có thể chuyển hóa và hạt giống tốt có thể nảy nở.'
    ],
    example: 'Đóa hoa sen dâng Phật có mặt nhờ ánh nắng, bùn nước, đám mây và bàn tay người trồng — nhìn sâu vào đóa sen ta thấy cả vũ trụ.',
    practice: 'Khi gặp một cơn giận hay nỗi buồn, hãy quán sát nó như đám mây hợp rồi tan trên bầu trời tâm thức.',
    quiz: {
      question: 'Nhờ quán chiếu điều gì mà Bồ Tát Quán Tự Tại vượt qua hết thảy khổ ách trong Tâm Kinh?',
      options: [
        'Quán chiếu năm uẩn đều nương duyên mà thành, không có tự tính riêng biệt (Ngũ uẩn giai không)',
        'Tìm kiếm phép thuật thần thông',
        'Tránh xa cuộc đời'
      ],
      correctIndex: 0,
      explanation: 'Thấy rõ thân tâm và hoàn cảnh đều do duyên sinh, vô thường nên buông xả được chấp ngã nặng nề.'
    }
  },
  {
    id: 'B3',
    pathId: 'B',
    order: 3,
    title: 'Kinh Từ Bi (Karaniya Metta Sutta) & Thiền Tâm Từ',
    duration: '13 phút',
    audio: 's6_ke_2.mp3',
    sourceBook: 'Tu Dưỡng Tâm Từ Bằng Thiền Chánh Niệm',
    summary: [
      'Người thực hành Từ Bi sống hiền hòa, tri túc, dễ nuôi, lục căn thanh tịnh, khiêm cung.',
      'Rải tâm từ tuần tự từ chính mình -> người thương -> người trung dung -> người gây khó dễ -> khắp muôn loài.',
      'Tâm từ như mẹ hiền đem cả mạng sống che chở đứa con duy nhất của mình.'
    ],
    example: 'Sau mỗi thời niệm Phật hoặc dâng hương, ta đọc bài kệ Hồi hướng để gửi năng lượng từ bi đến cha mẹ, bà con và hết thảy chúng sanh.',
    practice: 'Gửi lời chúc thầm lặng "Mong bạn không có oan trái, không có khổ đau, thân tâm an lạc" đến 3 người hôm nay.',
    quiz: {
      question: 'Theo sách "Tu Dưỡng Tâm Từ Bằng Thiền Chánh Niệm", vì sao ta cần khởi đầu rải tâm từ cho chính mình trước?',
      options: [
        'Vì ích kỷ chỉ nghĩ cho mình',
        'Vì khi mình biết thương yêu và làm lắng dịu nội tâm mình, ta mới có nguồn năng lượng bình an chân thật để truyền trao cho người khác',
        'Vì không cần thương người ngoài'
      ],
      correctIndex: 1,
      explanation: 'Lấy chính mình làm chứng: mình muốn an vui không khổ đau thế nào thì muôn loài cũng ước mong như thế.'
    }
  },
  {
    id: 'B4',
    pathId: 'B',
    order: 4,
    title: 'Ý nghĩa Niệm Phật & Chuỗi hạt 108 biến Bồ Đề',
    duration: '13 phút',
    audio: 's1_adida.mp3',
    sourceBook: 'Giáo Trình Phật Học & Pháp Môn Tịnh Độ',
    summary: [
      'Nam Mô A Di Đà Phật nghĩa là quay về nương tựa Đấng Vô Lượng Quang (Ánh sáng trí tuệ) và Vô Lượng Thọ (Sự sống từ bi).',
      'Chuỗi 108 hạt biểu trưng cho việc chuyển hóa 108 phiền não sinh khởi khi 6 căn tiếp xúc 6 trần.',
      'Mỗi tiếng niệm Phật nhiếp cả 3 nghiệp: Tay lần chuỗi (Thân), Miệng niệm danh hiệu (Khẩu), Tâm nhớ nghĩ công đức Phật (Ý).'
    ],
    example: 'Khi bấm nút "Niệm Phật" ở góc phải màn hình, mỗi hạt chuỗi dịch chuyển cùng tiếng mõ trầm đều giúp nhịp tim và hơi thở chậm lại.',
    practice: 'Dành 3 phút lần chuỗi niệm Phật 21 hoặc 108 biến trước khi đi ngủ.',
    quiz: {
      question: 'Pháp môn Niệm Phật đạt hiệu quả "Nhất tâm bất loạn" khi hành giả kết hợp ba yếu tố nào?',
      options: [
        'Chỉ đọc bằng miệng thật to mà tâm nghĩ việc khác',
        'Ba nghiệp Thân – Khẩu – Ý hợp nhất trong chánh niệm (Miệng niệm rõ ràng, tai lắng nghe rõ ràng, tâm ghi nhớ từng câu Phật hiệu)',
        'Đếm cho thật nhanh'
      ],
      correctIndex: 1,
      explanation: 'Tổ Ấn Quang dạy: Niệm từ tâm khởi, tiếng từ miệng ra, âm vào tai nghe rõ ràng thì vọng tưởng tự lặng.'
    }
  },
  {
    id: 'B5',
    pathId: 'B',
    order: 5,
    title: 'Kinh Phước Đức (Mangala Sutta): 38 nấc thang hạnh phúc',
    duration: '12 phút',
    audio: 's6_ke_3.mp3',
    sourceBook: 'Kinh Tập (Sutta Nipāta) & Nền Tảng Phật Giáo Q.5',
    summary: [
      'Phước lành tối thượng bắt đầu từ việc không gần kẻ ác, thân cận người hiền trí, sống ở môi trường thiện lành.',
      'Đa văn học rộng, khéo nghề nghiệp chân chính, nói lời chân thật hòa ái.',
      'Phụng dưỡng cha mẹ, yêu thương vợ con, tâm không sầu muộn nhiễm ô trước 8 ngọn gió đời (Bát phong).'
    ],
    example: 'Đưa cả gia đình 3 thế hệ (Ông bà/Cha mẹ và Trẻ em) cùng đi chùa, chụp bức ảnh kỷ niệm hiếu hạnh là hình ảnh đẹp nhất của Kinh Phước Đức.',
    practice: 'Gọi điện hỏi thăm hoặc rót một tách trà ấm mời cha mẹ trong ngày hôm nay.',
    quiz: {
      question: 'Theo Kinh Phước Đức, đỉnh cao của người có phước đức giữa cuộc đời biến động là gì?',
      options: [
        'Khi xúc chạm việc đời (được/mất, hơn/thua), tâm không dao động, không sầu, trong sạch và an ổn',
        'Không bao giờ gặp thử thách',
        'Trúng số may mắn'
      ],
      correctIndex: 0,
      explanation: '"Phuṭṭhassa lokadhammehi, cittaṃ yassa na kampati" — Khi chạm việc đời mà tâm không lay động là phước đức lớn nhất.'
    }
  },
  {
    id: 'B6',
    pathId: 'B',
    order: 6,
    title: 'Bốn bài Kệ Hồi Hướng & Tâm nguyện Bồ Đề rộng lớn',
    duration: '13 phút',
    audio: 's6_ke_4.mp3',
    sourceBook: 'Nền Tảng Phật Giáo Quyển 5 (Hồi hướng phước - Pattidāna)',
    summary: [
      'Hồi hướng (Pattidāna) là đem công đức tu tập chia sẻ cho ông bà cha mẹ và khắp pháp giới chúng sanh.',
      'Kinh điển ví sự hồi hướng phước như lấy một ngọn đuốc mồi cho hàng trăm ngọn đuốc khác: ngọn đuốc đầu chẳng hề vơi đi mà cả gian phòng càng rực sáng.',
      'Kết thúc mỗi chuyến hành hương bằng lời kệ hồi hướng giúp phá trừ tâm ích kỷ nhỏ hẹp.'
    ],
    example: 'Tại trạm số 8 (Bảo Tháp Thất Phật), bốn câu kệ hồi hướng vang lên khép lại hành trình đi chùa trong niềm hoan hỷ.',
    practice: 'Thuộc lòng 4 câu: "Nguyện đem công đức này, Hướng về khắp tất cả, Đệ tử và chúng sanh, Đều trọn thành Phật đạo."',
    quiz: {
      question: 'Theo giáo lý Phước Thiện (Quyển 5), khi ta hồi hướng công đức lành cho mọi người thì phước của ta thay đổi thế nào?',
      options: [
        'Bị giảm đi một nửa',
        'Không hề hao tổn mà còn sinh thêm một cội phước mới gọi là "Phước Hồi Hướng" (Pattidāna-maya)',
        'Biến mất hoàn toàn'
      ],
      correctIndex: 1,
      explanation: 'Hồi hướng là một trong 10 cội phước thiện; càng chia sẻ bằng tâm hoan hỷ, phước báu càng tăng trưởng.'
    }
  },

  // === GÓI C (6 bài) ===
  {
    id: 'C1',
    pathId: 'C',
    order: 1,
    title: 'Phương pháp Thiền căn bản (Ajahn Brahm): An trú hiện tại',
    duration: '12 phút',
    audio: 's6_dan.mp3',
    sourceBook: 'Phương Pháp Thiền Căn Bản — Thiền sư Ajahn Brahm',
    summary: [
      'Giai đoạn 1: Buông bỏ gánh nặng quá khứ (đã qua) và tương lai (chưa tới) để bước vào căn phòng tĩnh lặng của Giây Phút Hiện Tại.',
      'Giai đoạn 2: Trở về nhận biết hơi thở tự nhiên với thái độ nâng niu, không kiểm soát hay gồng ép.',
      'Khi tâm tĩnh lặng và hỷ lạc, hơi thở trở nên êm dịu, mở cánh cửa đi vào định tĩnh sâu sắc.'
    ],
    example: 'Ngồi trên bồ đoàn trong Giảng đường Phật pháp Chùa Vĩnh Tràng, nhìn ánh nắng xuyên qua khung cửa gỗ và buông thư đôi vai theo đúng hướng dẫn của Thiền sư Ajahn Brahm.',
    practice: 'Thực hành 3 phút "Tĩnh lặng trong hiện tại": mỗi khi tâm nhớ việc cũ hay lo việc mai, nhẹ nhàng mỉm cười quay về hơi thở.',
    quiz: {
      question: 'Trong sách "Phương Pháp Thiền Căn Bản", Thiền sư Ajahn Brahm ví quá khứ và tương lai như điều gì cần buông xuống khi vào thiền?',
      options: [
        'Hai chiếc va-li nặng trĩu trên hai tay cần đặt xuống đất để được thảnh thơi trong giây phút hiện tại',
        'Hai món trang sức cần mang theo mãi',
        'Điều quan trọng hơn hiện tại'
      ],
      correctIndex: 0,
      explanation: 'Buông hai chiếc túi quá khứ và tương lai xuống giúp tâm nghỉ ngơi trọn vẹn trong hiện tại nhiệm mầu.'
    }
  },
  {
    id: 'C2',
    pathId: 'C',
    order: 2,
    title: 'Chuyển hóa cơn giận & Nghệ thuật Lắng nghe sâu',
    duration: '12 phút',
    audio: 's3_giang_duong.mp3',
    sourceBook: 'Tích Truyện Pháp Cú (Phẩm Phẫn Nộ) & Tu Dưỡng Tâm Từ',
    summary: [
      'Kinh Pháp Cú dạy: "Lấy không giận thắng giận, lấy thiện thắng không thiện".',
      'Khi cơn giận khởi lên, đừng vội nói hay hành động; hãy quay về ôm ấp và làm dịu hơi thở của chính mình trước.',
      'Lắng nghe sâu bằng tâm từ bi giúp tháo gỡ hiểu lầm trong gia đình.'
    ],
    example: 'Khi có bất đồng, nhớ lại hình ảnh tôn giả Hàng Long La Hán tại Chánh điện Vĩnh Tràng — hàng phục con rồng sân hận bằng trí tuệ tĩnh lặng.',
    practice: 'Hôm nay hãy lắng nghe một người thân tâm sự trọn vẹn 5 phút mà không ngắt lời hay phán xét.',
    quiz: {
      question: 'Theo Kinh Pháp Cú (kệ 223), phương pháp tối thắng để hóa giải lòng sân giận và oán hận là gì?',
      options: [
        'Đáp trả mạnh mẽ hơn',
        'Lấy tâm Không Giận (Từ nhẫn) để cảm hóa cái giận, lấy điều lành thắng điều chưa lành',
        'Im lặng thù ghét trong lòng'
      ],
      correctIndex: 1,
      explanation: '"Hận thù diệt hận thù, đời này không thể có; Từ bi diệt hận thù, là định luật ngàn thu."'
    }
  },
  {
    id: 'C3',
    pathId: 'C',
    order: 3,
    title: 'Đạo Hiếu trong Phật giáo: Cha mẹ là hai vị Phật tại gia',
    duration: '12 phút',
    audio: 's6_ke_1.mp3',
    sourceBook: 'Phật Học Phổ Thông Quyển 1 & Kinh Báo Hiếu Công Đức Phụ Mẫu Ân',
    summary: [
      'Đức Phật dạy: "Tâm hiếu là tâm Phật, hạnh hiếu là hạnh Phật".',
      'Thờ Phật ở xa không bằng hiếu kính, phụng dưỡng cha mẹ hiện tiền ngay trong gia đình.',
      'Đại hiếu trọn vẹn nhất là vừa chăm sóc thân cha mẹ ấm êm, vừa hướng dẫn cha mẹ biết quy y Tam Bảo, giữ giới, làm lành.'
    ],
    example: 'Trong tính năng Chụp ảnh UGC Chùa Vĩnh Tràng, bạn có thể chọn chế độ "Gia đình 3 thế hệ (Nam + Nữ + Trẻ em)" để lưu giữ khoảnh khắc hiếu hạnh sum vầy.',
    practice: 'Nói một lời biết ơn hoặc đỡ đần cha mẹ một công việc nhỏ trong hôm nay.',
    quiz: {
      question: 'Trong Kinh Tăng Chi Bộ, Đức Phật dạy cách báo đáp trọn vẹn nhất công ơn sinh thành dưỡng dục của cha mẹ là gì?',
      options: [
        'Chỉ chu cấp tiền bạc là đủ',
        'Vừa phụng dưỡng chu đáo bằng lòng kính yêu, vừa khuyến hóa cha mẹ có niềm tin nơi Tam Bảo, giữ giới, bố thí và trí tuệ',
        'Đợi đến rằm tháng Bảy mới nhớ tới'
      ],
      correctIndex: 1,
      explanation: 'Giúp cha mẹ an vui cả đời này lẫn gieo nhân lành giải thoát nhiều đời sau là đại hiếu viên mãn.'
    }
  },
  {
    id: 'C4',
    pathId: 'C',
    order: 4,
    title: 'Thiền hành & Thiền trà trong đời sống bận rộn',
    duration: '11 phút',
    audio: 'day_di.mp3',
    sourceBook: 'Tu Dưỡng Tâm Từ Bằng Thiền Chánh Niệm (Tứ Oai Nghi Đi – Đứng – Nằm – Ngồi)',
    summary: [
      'Chánh niệm không chỉ giới hạn lúc ngồi xếp bằng mà tiếp nối trong cả 4 oai nghi: Đi, Đứng, Nằm, Ngồi.',
      'Khi bước đi trên sân chùa, biết rõ từng bước chân chạm mặt đá mát lành.',
      'Khi nâng chén trà sen, tâm hoàn toàn có mặt với hương trà và người đối diện.'
    ],
    example: 'Tản bộ quanh vườn bonsai Mai Chiếu Thủy và hoa giấy hồng ở sân chùa Vĩnh Tràng với tâm thư thái.',
    practice: 'Khi uống ly nước hoặc tách trà chiều nay, hãy dừng mọi việc khác trong 1 phút để cảm nhận hơi ấm nơi lòng bàn tay.',
    quiz: {
      question: 'Mục đích chính của Thiền hành (đi bộ trong chánh niệm) là gì?',
      options: [
        'Đi thật nhanh cho kịp giờ',
        'Đưa tâm trở về hợp nhất với thân trong từng bước chân bình an nơi hiện tại',
        'Vừa đi vừa suy tính công việc'
      ],
      correctIndex: 1,
      explanation: 'Thiền hành giúp thân và tâm cùng có mặt ở đây và bây giờ, mỗi bước chân đều nở hoa sen.'
    }
  },
  {
    id: 'C5',
    pathId: 'C',
    order: 5,
    title: 'Buông xả lo âu & Giấc ngủ an lành của người có Tâm Từ',
    duration: '11 phút',
    audio: 's5_nirvana.mp3',
    sourceBook: 'Tu Dưỡng Tâm Từ Bằng Thiền Chánh Niệm (11 Phước Báu Của Tâm Từ)',
    summary: [
      'Kinh Tăng Chi nêu 11 lợi ích của người tu tập Tâm Từ: Ngủ an lành, Thức dậy an lành, Không ác mộng, Được người và chư thiên quý mến, Sắc mặt hiền hòa, Tâm dễ định tĩnh...',
      'Thực tập buông thư toàn thân từ đỉnh đầu xuống bàn chân trước khi ngủ.',
      'Thầm gửi lời tha thứ cho mình và cho mọi người trước khi khép mắt.'
    ],
    example: 'Tư thế Cát Tường an nhiên của tôn tượng Phật Niết Bàn dài 32m tại Vĩnh Tràng nhắc ta biết buông xuống những gánh nặng không cần thiết.',
    practice: 'Trước khi ngủ tối nay, thực tập tha thứ và rải tâm từ trong 2 phút để đón nhận giấc ngủ sâu bình yên.',
    quiz: {
      question: 'Theo Kinh điển Pali (trích trong sách Tu Dưỡng Tâm Từ), người thường xuyên thực hành rải Tâm Từ trước khi ngủ sẽ nhận được phước lành nào ngay trong đêm?',
      options: [
        'Ngủ an lành, thức dậy an lành, không gặp ác mộng và gương mặt tươi sáng',
        'Thức trắng đêm suy nghĩ',
        'Mơ thấy tranh đấu'
      ],
      correctIndex: 0,
      explanation: 'Đức Phật dạy 11 phước báu hiện tiền của Tâm Từ, đứng đầu là "Ngủ an lạc, thức dậy an lạc, không thấy ác mộng".'
    }
  },
  {
    id: 'C6',
    pathId: 'C',
    order: 6,
    title: 'Hạnh Tri Ân, Báo Ân & Tri Túc Thường Lạc',
    duration: '12 phút',
    audio: 's7_tam_biet.mp3',
    sourceBook: 'Phật Học Phổ Thông Quyển 1 & Kinh Di Giáo',
    summary: [
      'Đức Phật dạy người biết ơn và đền ơn (Tri ân – Báo ân) là biểu hiện của bậc thiện nhân giữa cuộc đời.',
      'Tứ trọng ân: Ân cha mẹ, Ân Tam Bảo – thầy tổ, Ân quốc gia xã hội, Ân chúng sanh vạn loại.',
      'Kinh Di Giáo dạy: "Người biết đủ (Tri túc) tuy nằm trên đất vẫn thấy an vui; người không biết đủ dù ở thiên đường cũng chưa vừa ý."'
    ],
    example: 'Viết 3 điều biết ơn vào cuốn Sổ tay hoa sen lưu niệm mỗi tối giúp tâm hồn luôn ấm áp.',
    practice: 'Viết ra 3 điều giản dị mà bạn cảm thấy biết ơn trong ngày hôm nay.',
    quiz: {
      question: 'Lời dạy cuối cùng của Đức Phật trong Kinh Di Giáo về hạnh "Tri túc" (Biết đủ) mang ý nghĩa gì?',
      options: [
        'Lười biếng không làm việc',
        'Biết đủ và trân trọng những gì mình đang có bằng chánh mạng, không để lòng tham lam bất tận làm khổ tâm',
        'Đòi hỏi thật nhiều'
      ],
      correctIndex: 1,
      explanation: '"Tri túc chi pháp, tức thị phú lạc an ổn chi xứ" — Hạnh biết đủ chính là nơi giàu có, an vui và bình ổn nhất.'
    }
  },

  // === GÓI D (6 bài) ===
  {
    id: 'D1',
    pathId: 'D',
    order: 1,
    title: 'Lịch sử Chùa Vĩnh Tràng — Cổ tự trăm năm miền Tây',
    duration: '11 phút',
    audio: 's0_chao.mp3',
    sourceBook: 'Biên Niên Sử Danh Lam Chùa Vĩnh Tràng (Mỹ Tho · Tiền Giang)',
    summary: [
      'Khởi dựng từ đầu thế kỷ XIX tại làng Mỹ Hóa (nay thuộc TP. Mỹ Tho, Tiền Giang) bởi ông bà Tri huyện Bùi Công Đạt.',
      'Năm 1849, Hòa thượng Thích Huệ Đăng từ chùa Giác Lâm (Gia Định) về trụ trì, đại trùng tu và đặt tên chùa Vĩnh Tràng ("Vĩnh cửu đối sơn trang").',
      'Trải qua các đợt trùng tu lớn năm 1907 và 1933, chùa được công nhận Di tích lịch sử – văn hóa cấp Quốc gia năm 1984.'
    ],
    example: 'Ngay từ cổng Tam Quan ghép mảnh sành sứ năm 1933 bởi nghệ nhân Huế, du khách đã cảm nhận được bề dày lịch sử gần 200 năm.',
    practice: 'Quan sát kỹ các bức phù điêu sành sứ và hàng cột vòm trước mặt tiền Chánh điện.',
    quiz: {
      question: 'Tên gọi "Vĩnh Tràng" do Hòa thượng Thích Huệ Đăng đặt năm 1849 bắt nguồn từ câu đối mang ý nghĩa gì?',
      options: [
        'Vĩnh cửu đối sơn trang, Tràng nghiêm quy hải tạng (Mãi mãi trang nghiêm bền vững cùng non sông biển rộng)',
        'Ngôi chùa nhỏ bên sông',
        'Nơi buôn bán sầm uất'
      ],
      correctIndex: 0,
      explanation: 'Tên chùa lấy hai chữ đầu của câu đối "Vĩnh cửu đối sơn trang, Tràng nghiêm quy hải tạng".'
    }
  },
  {
    id: 'D2',
    pathId: 'D',
    order: 2,
    title: 'Kiến trúc giao thoa Á – Âu độc đáo của Chánh Điện',
    duration: '11 phút',
    audio: 's3_lay_phat.mp3',
    sourceBook: 'Nghiên Cứu Kiến Trúc Mỹ Thuật Cổ Tự Nam Bộ',
    summary: [
      'Mặt tiền kết hợp hài hòa vòm cửa La Mã, thức cột Corinth/Phục Hưng, bông sắt Pháp với mái chùa cổ truyền Việt Nam và hoa văn Khmer.',
      'Bên trong nội điện giữ trọn cấu trúc gỗ truyền thống kiểu chữ Quốc (國) gồm Tiền đường, Chánh điện, Nhà tổ và Nhà hậu với 7 bộ bao lam chạm thếp vàng.',
      'Hàng hiên gạch bông và phù điêu gốm sứ màu lam – vàng tạo nên vẻ đẹp độc nhất vô nhị.'
    ],
    example: 'Trong cảnh 3D chính của ứng dụng, bạn thấy rõ 7 vòm cửa uốn cong vàng ấm cùng phù điêu gốm xanh trắng đặc trưng Vĩnh Tràng.',
    practice: 'Di chuyển nhân vật lại gần bậc thềm Chánh điện hoặc chụp một tấm ảnh UGC trước mặt tiền Á – Âu.',
    quiz: {
      question: 'Nét đặc sắc nổi bật nhất về mặt kiến trúc của mặt tiền Chánh điện Chùa Vĩnh Tràng là gì?',
      options: [
        'Hoàn toàn bằng bê tông hiện đại',
        'Sự kết hợp nhuần nhuyễn giữa nghệ thuật kiến trúc Á Đông cổ truyền (mái ngói, tứ linh) và nét trang trí Phục Hưng – La Mã phương Tây',
        'Xây dựng hoàn toàn bằng đá xanh'
      ],
      correctIndex: 1,
      explanation: 'Chùa Vĩnh Tràng nổi tiếng khắp Đông Nam Á nhờ sự giao thoa kiến trúc Đông – Tây đầy thẩm mỹ.'
    }
  },
  {
    id: 'D3',
    pathId: 'D',
    order: 3,
    title: 'Bộ tượng Thập Bát La Hán gỗ mít trăm tuổi (1907)',
    duration: '11 phút',
    audio: 's3_lay_phat.mp3',
    sourceBook: 'Di Sản Điêu Khắc Cổ Chùa Vĩnh Tràng',
    summary: [
      'Gồm 18 pho tượng La Hán tạc bằng gỗ mít cổ thụ từ năm 1907 đặt dọc hai tường bên nội điện.',
      'Mỗi vị cao khoảng 0.8m–1m, cưỡi linh thú hoặc cầm pháp khí riêng: Tọa Lộc, Khánh Hỷ, Cử Bát, Thác Tháp, Tĩnh Tọa, Quá Giang, Kỵ Tượng, Tiếu Sư, Khai Tâm, Hàng Long, Phục Hổ...',
      'Thể hiện đỉnh cao nghệ thuật điêu khắc gỗ tâm linh Nam Bộ đầu thế kỷ XX.'
    ],
    example: 'Mỗi vị La Hán tuy diện mạo khác nhau nhưng đều biểu thị trí tuệ đã chiến thắng phiền não nội tâm.',
    practice: 'Vào mục Khám phá -> Thập Bát La Hán để xem chi tiết ý nghĩa từng vị trong 18 vị La Hán Chùa Vĩnh Tràng.',
    quiz: {
      question: 'Bộ tượng 18 vị La Hán nổi tiếng tại Chùa Vĩnh Tràng được chế tác năm 1907 từ chất liệu gì?',
      options: ['Đá hoa cương', 'Gỗ mít cổ thụ chạm khắc thủ công sơn thếp vàng', 'Thạch cao'],
      correctIndex: 1,
      explanation: 'Các nghệ nhân miền Nam xưa đã dùng gỗ mít già bền chắc để chạm khắc sống động 18 vị La Hán.'
    }
  },
  {
    id: 'D4',
    pathId: 'D',
    order: 4,
    title: 'Ba pho Đại Tượng lộ thiên: Di Lặc – A Di Đà – Niết Bàn',
    duration: '11 phút',
    audio: 's4_dilac.mp3',
    sourceBook: 'Quy Hoạch Khuôn Viên 2 Hecta Chùa Vĩnh Tràng',
    summary: [
      'Đại tượng Phật A Di Đà đứng cao 18m (tính cả bệ 24m) biểu trưng cho từ bi tiếp dẫn.',
      'Đại tượng Phật Di Lặc ngồi cao 20m, rộng 18m với nụ cười hoan hỷ bao dung.',
      'Đại tượng Phật Thích Ca Niết Bàn dài 32m an nhiên giữa vườn cây xanh mát.'
    ],
    example: 'Ba pho đại tượng tạo thành thế Tam Tôn lộ thiên hùng vĩ giữa khuôn viên 2 hecta của nhà chùa.',
    practice: 'Bấm vào Bản đồ Khuôn viên 9 Khu vực để di chuyển đến chiêm bái lần lượt cả 3 pho đại tượng.',
    quiz: {
      question: 'Ba pho đại tượng trắng lộ thiên nổi tiếng trong khuôn viên Chùa Vĩnh Tràng gồm những tôn tượng nào?',
      options: [
        'Phật A Di Đà đứng, Phật Di Lặc ngồi và Phật Thích Ca nhập Niết Bàn',
        'Ba tượng Hộ Pháp',
        'Ba tượng Quan Công'
      ],
      correctIndex: 0,
      explanation: 'Đây là 3 công trình điêu khắc Phật giáo quy mô lớn tạo điểm nhấn tâm linh cho toàn khuôn viên.'
    }
  },
  {
    id: 'D5',
    pathId: 'D',
    order: 5,
    title: 'Nghi thức đi chùa đúng pháp: Trang phục, Đi đứng & Thắp hương',
    duration: '11 phút',
    audio: 's3_bo_dep.mp3',
    sourceBook: 'Cẩm Nang Oai Nghi Phật Tử Tại Gia',
    summary: [
      'Trang phục kín đáo, trang nhã (như bộ áo tràng lam Phật tử 5 nút cổ tàu cho Nữ, Nam và Trẻ em).',
      'Vào chùa đi cửa bên (Giả quan / Không quan), không dẫm lên bậu cửa gỗ, bỏ dép trước khi vào nội điện.',
      'Chỉ thắp 1 đến 3 nén hương tại lư hương ngoài sân, phẩy tắt lửa bằng tay chứ không thổi bằng miệng.'
    ],
    example: 'Ba nhân vật Phật tử (Nam, Nữ, Trẻ em) trong Chùa Online đều mặc pháp phục kín đáo, thực hiện đúng 4 bước dâng hương ngoài sân trước khi vào lễ Phật.',
    practice: 'Thực hành trọn vẹn quy trình 4 bước Dâng hương và 3 lạy Lễ Phật ngay trên giao diện chính.',
    quiz: {
      question: 'Khi nén hương bốc lửa lúc châm, người đi chùa nên làm gì cho đúng oai nghi?',
      options: [
        'Dùng miệng thổi mạnh cho tắt',
        'Cầm hương phẩy nhẹ bằng tay cho tắt lửa rồi mới nâng ngang trán khấn nguyện',
        'Cắm ngay khi lửa còn cháy to'
      ],
      correctIndex: 1,
      explanation: 'Theo truyền thống Phật giáo, hơi thở từ miệng được xem là bất tịnh đối với hương dâng Phật nên ta dùng tay phẩy nhẹ.'
    }
  },
  {
    id: 'D6',
    pathId: 'D',
    order: 6,
    title: 'Ý nghĩa Dâng Hoa Sen, Chuông Chùa & Lưu Bút Hành Hương Chánh Tín',
    duration: '10 phút',
    audio: 'merit_box.mp3',
    sourceBook: 'Phật Học Phổ Thông & Văn Hóa Đi Chùa Việt Nam',
    summary: [
      'Dâng hoa sen tượng trưng cho việc tu nhân thiện lành (hoa) để kết thành quả giác ngộ (gương sen) ngay trong hiện tại.',
      'Thỉnh chuông chùa và dạo bước chánh niệm quanh 9 điểm hành hương giúp buông xả căng thẳng, nuôi dưỡng tâm từ bi.',
      'Lưu giữ bức ảnh kỷ niệm cùng Chùa Vĩnh Tràng sau khi lễ Phật là cách nhắc nhở bản thân và gia đình giữ gìn nếp sống hướng thiện.'
    ],
    example: 'Bạn có thể vào mục "📸 Chụp ảnh UGC" sau khi hoàn thành một nghi lễ để lưu giữ kỷ niệm gia đình 3 nhân vật trước Chùa Vĩnh Tràng.',
    practice: 'Dâng hoa sen bên Hồ Sen và lưu giữ một bức ảnh kỷ niệm trang nghiêm cùng Chùa Vĩnh Tràng.',
    quiz: {
      question: 'Trong truyền thống Phật giáo, hoa sen dâng Phật mang biểu trưng đặc biệt nào?',
      options: [
        'Chỉ có hoa mà không có quả',
        'Hoa và gương sen (nhân và quả) cùng hiện hữu một lúc, mọc từ bùn nhưng chẳng hôi tanh mùi bùn',
        'Chỉ nở vào ban đêm'
      ],
      correctIndex: 1,
      explanation: 'Hoa sen là loài hoa duy nhất vừa nở hoa vừa kết gương sen cùng lúc, tượng trưng cho lý Nhân Quả đồng thời và sự thanh tịnh giữa cuộc đời.'
    }
  }
];

export function getLessonsByPath(pathId = 'A') {
  return LECTURE_LESSONS.filter((l) => l.pathId === pathId).sort((a, b) => a.order - b.order);
}

export function gradeLessonQuiz(lessonId, selectedIndex) {
  const lesson = LECTURE_LESSONS.find((l) => l.id === lessonId);
  if (!lesson) {
    return { found: false, correct: false, explanation: '' };
  }
  const correct = Number(selectedIndex) === lesson.quiz.correctIndex;
  return {
    found: true,
    correct,
    correctIndex: lesson.quiz.correctIndex,
    explanation: lesson.quiz.explanation
  };
}

/**
 * UGC Photo Check-in Studio ("Chụp ảnh Check-in với Chùa Vĩnh Tràng như ở đó thật")
 */
export const UGC_BACKDROPS = [
  {
    id: 'chanh_dien_mat_tien',
    name: 'Mặt tiền Chánh điện Á – Âu rực rỡ',
    src: '/public/assets/aistudio/image_dbddfac8.png',
    captionTag: '📍 Chánh điện Chùa Vĩnh Tràng · Mỹ Tho, Tiền Giang'
  },
  {
    id: 'cua_hang_luu_niem_go',
    name: 'Quầy gỗ Cửa hàng lưu niệm & Đèn lồng sen',
    src: '/public/assets/aistudio/image_43ca3fb3.png',
    captionTag: '🪷 Cửa hàng lưu niệm Chùa Vĩnh Tràng'
  },
  {
    id: 'giang_duong_phat_phap',
    name: 'Nội điện Giảng đường Phật pháp trầm mặc',
    src: '/public/assets/aistudio/image_dc0ddf04.png',
    captionTag: '📖 Giảng đường Phật pháp Chùa Vĩnh Tràng'
  },
  {
    id: 'khuon_vien_3_nhan_vat',
    name: 'Sân chùa & Gia đình 3 nhân vật Phật tử',
    src: '/Thiết kế giao diện/Nhân vật 3D/anh-xem-truoc-3d-all-nguoi-that.png',
    captionTag: '🙏 Gia đình Phật tử hành hương Chùa Vĩnh Tràng'
  }
];

export const UGC_POSES = [
  { id: 'chap_tay_le_phat', label: '🙏 Chắp tay lễ Phật Tam Bảo', propLabel: 'Tràng hạt Bồ Đề 108 hạt' },
  { id: 'dang_hoa_sen', label: '🪷 Dâng búp sen hồng thanh tịnh', propLabel: 'Hoa sen tươi Mỹ Tho' },
  { id: 'doi_non_deo_tui', label: '👒 Đội nón lá thêu sen & Túi vải', propLabel: 'Nón lá lụa + Túi tote sen' },
  { id: 'cam_den_hoa_dang', label: '🕯️ Nâng đèn hoa đăng cầu quốc thái dân an', propLabel: 'Đèn hoa sen pha lê' }
];

export const INITIAL_UGC_GALLERY = [
  {
    id: 'ugc_seed_1',
    author: 'Gia đình Phật tử Minh Đức – Diệu Tâm – Bé An',
    charMode: 'family_3',
    backdropId: 'chanh_dien_mat_tien',
    poseId: 'chap_tay_le_phat',
    wishText: 'Gia đình 3 thế hệ chúng con thành tâm kính lễ Phật tại Chùa Vĩnh Tràng. Nguyện cầu ông bà cha mẹ trường thọ, con cháu hiếu thảo!',
    likes: 108,
    createdAt: 'Hôm nay · Mỹ Tho, Tiền Giang'
  },
  {
    id: 'ugc_seed_2',
    author: 'Phật tử Diệu Liên (TP.HCM)',
    charMode: 'nu',
    backdropId: 'cua_hang_luu_niem_go',
    poseId: 'doi_non_deo_tui',
    wishText: 'Đã thỉnh Sổ tay hoa sen, Tràng hạt gỗ và Nón lá thêu sen tại Cửa hàng lưu niệm. Đẹp và trang nghiêm như đang đứng giữa sân chùa thật!',
    likes: 84,
    createdAt: 'Hôm nay · Chùa Vĩnh Tràng'
  },
  {
    id: 'ugc_seed_3',
    author: 'Đạo hữu Tâm Minh (Cần Thơ)',
    charMode: 'nam',
    backdropId: 'giang_duong_phat_phap',
    poseId: 'dang_hoa_sen',
    wishText: 'Nghe giảng Phật Học Phổ Thông và Phương Pháp Thiền Căn Bản của Thiền sư Ajahn Brahm trong Giảng đường gỗ thật an lạc.',
    likes: 69,
    createdAt: 'Hôm qua · Giảng đường Phật pháp'
  }
];

export function createUGCPost(payload = {}) {
  const author = String(payload.author || 'Phật tử Tâm An').trim() || 'Phật tử Tâm An';
  const charMode = payload.charMode || 'family_3'; // 'nu' | 'nam' | 'tre_em' | 'family_3'
  const backdropId = payload.backdropId || 'chanh_dien_mat_tien';
  const poseId = payload.poseId || 'chap_tay_le_phat';
  const milestoneBadge =
    String(payload.milestoneBadge || 'Hoàn thành nghi lễ Chiêm bái Chùa Vĩnh Tràng').trim();
  const userPhotoUploaded = Boolean(payload.userPhotoUploaded);
  const frameStyle = payload.frameStyle || 'lotus_arch';
  const wishText =
    String(payload.wishText || '').trim() ||
    'Thành tâm kính lễ Tam Bảo tại Chùa Vĩnh Tràng — Nguyện cầu gia đạo bình an, tâm từ rộng mở.';

  return {
    id: `ugc_${Date.now()}`,
    author,
    charMode,
    backdropId,
    poseId,
    milestoneBadge,
    userPhotoUploaded,
    frameStyle,
    wishText,
    dataUrl: payload.dataUrl || null,
    likes: 1,
    createdAt: 'Vừa xong · Chùa Vĩnh Tràng'
  };
}

/**
 * Perceptual OKLab / OKLCH Color Engine (inspired by meodai/skill.color-expert)
 * Ensures perceptually uniform Lightness (L), Chroma (C), and Hue (H) transformations
 * with Bezold-Brücke sunlit warmth & cool sky-bounce shadow compensation (zero muddy mid-tones).
 */
function srgbToLinear(c) {
  return c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
}

function linearToSrgb(c) {
  const clamped = Math.max(0, Math.min(1, c));
  return clamped <= 0.0031308 ? 12.92 * clamped : 1.055 * Math.pow(clamped, 1 / 2.4) - 0.055;
}

export function hexToOklch(hexStr) {
  const clean = String(hexStr || '#000000').replace(/^#/, '');
  const num = parseInt(clean.length === 3 ? clean.replace(/(.)/g, '$1$1') : clean, 16) || 0;
  const r = srgbToLinear(((num >> 16) & 255) / 255);
  const g = srgbToLinear(((num >> 8) & 255) / 255);
  const b = srgbToLinear((num & 255) / 255);

  const l = Math.cbrt(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b);
  const m = Math.cbrt(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b);
  const s = Math.cbrt(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b);

  const L = 0.2104542553 * l + 0.793617785 * m - 0.0040720468 * s;
  const A = 1.9779984951 * l - 2.428592205 * m + 0.4505937099 * s;
  const B = 0.0259040371 * l + 0.7827717662 * m - 0.808675766 * s;

  const C = Math.hypot(A, B);
  let H = (Math.atan2(B, A) * 180) / Math.PI;
  if (H < 0) H += 360;
  return { L: Number(L.toFixed(4)), C: Number(C.toFixed(4)), H: Number(H.toFixed(2)) };
}

export function oklchToHex(L, C, H) {
  const hRad = ((H || 0) * Math.PI) / 180;
  const A = C * Math.cos(hRad);
  const B = C * Math.sin(hRad);

  const l_ = L + 0.3963377774 * A + 0.2158037573 * B;
  const m_ = L - 0.1055613458 * A - 0.0638541728 * B;
  const s_ = L - 0.0894841775 * A - 1.291485548 * B;

  const l = l_ * l_ * l_;
  const m = m_ * m_ * m_;
  const s = s_ * s_ * s_;

  const r = linearToSrgb(+4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s);
  const g = linearToSrgb(-1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s);
  const b = linearToSrgb(-0.0041960863 * l - 0.7034186147 * m + 1.707614701 * s);

  const toByte = (v) =>
    Math.round(Math.max(0, Math.min(255, v * 255)))
      .toString(16)
      .padStart(2, '0');
  return `#${toByte(r)}${toByte(g)}${toByte(b)}`.toUpperCase();
}

export function shiftOklch(hexStr, dL = 0, scaleC = 1.0, dH = 0) {
  const { L, C, H } = hexToOklch(hexStr);
  const nextL = Math.max(0.08, Math.min(0.98, L + dL));
  // Gamut cusp protection: reduce chroma near extreme lightness (L < 0.2 or L > 0.92)
  const cuspFactor = nextL > 0.9 ? (1 - nextL) / 0.1 : nextL < 0.18 ? nextL / 0.18 : 1;
  const nextC = Math.max(0, Math.min(0.32, C * scaleC * Math.max(0.35, cuspFactor)));
  const nextH = (H + dH + 360) % 360;
  return oklchToHex(nextL, nextC, nextH);
}

export const VINH_TRANG_OKLCH_PALETTE = {
  skyZenith: oklchToHex(0.49, 0.195, 256),       // Cobalt sky zenith (#0155C9 perceptual lock)
  skyHorizon: oklchToHex(0.68, 0.145, 250),      // Luminous horizon blue (#4F97F9)
  goldFacadeSun: oklchToHex(0.76, 0.128, 78),    // Warm sunlit Chánh điện ochre-gold (#E0AA42)
  goldFacadeShade: oklchToHex(0.64, 0.112, 72),  // Perceptually rich warm shade (#B9852F, never gray!)
  vermilionColumn: oklchToHex(0.42, 0.138, 28),  // Lacquered vermilion red column (#862820)
  terracottaTile: oklchToHex(0.48, 0.098, 38),   // Southern clay roof tile (#834332)
  lotusThroneBlue: oklchToHex(0.59, 0.078, 232), // A Di Đà lotus throne azure (#4E86A8)
  jadeFoliageSun: oklchToHex(0.58, 0.115, 136),  // Sunlit bonsai crown (#5C8A46)
  jadeFoliageDeep: oklchToHex(0.44, 0.095, 142), // Shaded foliage (#365E2E, shifted cool-green)
  lotusPink: oklchToHex(0.73, 0.148, 352)        // Sacred lotus petal pink (#EE7FAE)
};

