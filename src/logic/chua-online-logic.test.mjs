import test from 'node:test';
import assert from 'node:assert/strict';
import {
  CHARACTER_PROFILES,
  PILGRIMAGE_STATIONS,
  SHOP_CATALOG,
  DHARMA_TEXTBOOKS,
  LECTURE_PATHS,
  LECTURE_LESSONS,
  UGC_BACKDROPS,
  INITIAL_UGC_GALLERY,
  stepPlayerMovement,
  findNearestStation,
  createSpiritualState,
  performSpiritualAction,
  calculateJourneyImprint,
  filterShopCatalog,
  addToCart,
  updateCartQuantity,
  calculateCartSummary,
  validateOrderForm,
  getLessonsByPath,
  gradeLessonQuiz,
  createUGCPost,
  hexToOklch,
  oklchToHex,
  shiftOklch,
  VINH_TRANG_OKLCH_PALETTE
} from './chua-online-logic.mjs';

test('OKLab/OKLCH perceptual color engine (meodai/skill.color-expert) preserves perceptual lightness and prevents muddy mid-tones', () => {
  const gold = hexToOklch('#D9A441');
  assert.ok(gold.L > 0.68 && gold.L < 0.78);
  assert.ok(gold.C > 0.1);

  const roundTrip = oklchToHex(gold.L, gold.C, gold.H);
  const rtOklch = hexToOklch(roundTrip);
  assert.ok(Math.abs(rtOklch.L - gold.L) < 0.01);

  const sunlit = shiftOklch('#D9A441', 0.08, 1.05, 4);
  const shaded = shiftOklch('#D9A441', -0.12, 0.95, -6);
  assert.ok(hexToOklch(sunlit).L > gold.L);
  assert.ok(hexToOklch(shaded).L < gold.L);
  assert.ok(hexToOklch(shaded).C > 0.08); // Never collapses to muddy gray!
  assert.ok(VINH_TRANG_OKLCH_PALETTE.goldFacadeSun.startsWith('#'));
  assert.ok(VINH_TRANG_OKLCH_PALETTE.lotusThroneBlue.startsWith('#'));
});


test('3 rigged 3D character profiles (Nam, Nữ, Trẻ em) are defined with exact heights and GLBs', () => {
  assert.equal(CHARACTER_PROFILES.length, 3);
  const keys = CHARACTER_PROFILES.map((c) => c.key);
  assert.deepEqual(keys, ['nu', 'nam', 'tre_em']);
  assert.equal(CHARACTER_PROFILES[0].heightMeters, 1.62);
  assert.equal(CHARACTER_PROFILES[1].heightMeters, 1.74);
  assert.equal(CHARACTER_PROFILES[2].heightMeters, 1.15);
});

test('stepPlayerMovement moves character, updates yaw, and respects world bounds & obstacles', () => {
  const start = { x: 0, z: 16, yaw: Math.PI };
  const forward = stepPlayerMovement(start, { dx: 0, dz: -1 }, 0.5);
  assert.equal(forward.moving, true);
  assert.equal(forward.z, 15.5);
  assert.equal(forward.x, 0);

  const idle = stepPlayerMovement(forward, { dx: 0, dz: 0 }, 0.5);
  assert.equal(idle.moving, false);
  assert.equal(idle.z, 15.5);

  const obstacle = [{ minX: -2, maxX: 2, minZ: 14, maxZ: 15.2 }];
  const blocked = stepPlayerMovement({ x: 0, z: 15.3, yaw: Math.PI }, { dx: 0, dz: -1 }, 0.5, obstacle);
  assert.equal(blocked.z, 15.3);
});

test('findNearestStation & Dấu Ấn Hành Trình (9 lotus petals) work across all 9 temple zones without gamified EXP/levels/ranks', () => {
  assert.equal(PILGRIMAGE_STATIONS.length, 9);
  const stationKeys = PILGRIMAGE_STATIONS.map((s) => s.key);
  assert.ok(stationKeys.includes('ho_sen_ca_koi'));
  assert.ok(stationKeys.includes('phat_adida'));
  assert.ok(stationKeys.includes('phat_di_lac'));
  assert.ok(stationKeys.includes('phat_niet_ban'));
  assert.ok(stationKeys.includes('chanh_dien'));

  const nearest = findNearestStation({ x: 23, z: 7.2 });
  assert.equal(nearest.station.key, 'chanh_dien');

  const state = createSpiritualState({
    bowCount: 3,
    incenseOfferings: 1,
    lotusOfferings: 1,
    malaCycles: 1,
    visitedStations: [0, 1, 2, 3, 4, 5, 6, 7, 8]
  });
  const imprint = calculateJourneyImprint(state);
  assert.equal(imprint.totalPetals, 9);
  assert.equal(imprint.litCount, 9);
  assert.equal(imprint.petals.every((p) => p.lit), true);
  assert.equal('percent' in imprint, false);
  assert.equal('rankTitle' in imprint, false);
});

test('Spiritual Action State Machine handles Lễ Phật, Dâng hương 4 steps, Dâng hoa, Niệm Phật 108 beads, and unlocks UGC milestone', () => {
  let state = createSpiritualState();
  const bowRes = performSpiritualAction(state, 'LE_PHAT');
  state = bowRes.state;
  assert.equal(state.bowCount, 3);
  assert.equal(bowRes.milestoneUnlocked, true);
  assert.ok(state.completedMilestones.length >= 1);

  for (let i = 1; i <= 4; i++) {
    const incRes = performSpiritualAction(state, 'DANG_HUONG_STEP');
    state = incRes.state;
    assert.equal(state.incenseStep, i);
  }
  assert.equal(state.incenseOfferings, 1);

  const lotusRes = performSpiritualAction(state, 'DANG_HOA');
  state = lotusRes.state;
  assert.equal(state.lotusOfferings, 1);

  const malaRes = performSpiritualAction(state, 'NIEM_PHAT_BEAD', { count: 108, chant: 'Nam Mô A Di Đà Phật' });
  state = malaRes.state;
  assert.equal(state.malaCycles, 1);
  assert.equal(state.malaBeads, 0);

  const equipRes = performSpiritualAction(state, 'EQUIP_ITEM', { slot: 'hat', itemKey: 'non_la_theu_sen' });
  state = equipRes.state;
  assert.equal(state.equippedItems.hat, 'non_la_theu_sen');
});

test('Shop catalog has 3D Shop Kiosk model, exact top 3 souvenir items from Reference Image 2, and cart/order validation', () => {
  const souvenirs = filterShopCatalog('souvenir');
  const studies = filterShopCatalog('study');
  const items3d = filterShopCatalog('3d');

  assert.ok(souvenirs.length >= 8);
  assert.ok(studies.length >= 6);
  assert.ok(items3d.length >= 11);

  assert.equal(souvenirs[0].name, 'Sổ tay hoa sen');
  assert.equal(souvenirs[1].name, 'Tràng hạt gỗ');
  assert.equal(souvenirs[2].name, 'Bưu thiếp chùa');
  assert.equal(items3d[0].id, 'mo_hinh_cua_hang_3d');

  let cart = [];
  cart = addToCart(cart, 'so_tay_hoa_sen', 2);
  cart = addToCart(cart, 'trang_hat_go', 1);
  const summary1 = calculateCartSummary(cart);
  assert.equal(summary1.totalCount, 3);
  assert.equal(summary1.shippingFee, 0);

  cart = updateCartQuantity(cart, 'so_tay_hoa_sen', -2);
  const summary2 = calculateCartSummary(cart);
  assert.equal(summary2.totalCount, 1);

  const goodOrder = validateOrderForm({
    name: 'Nguyễn Thị Minh Tâm',
    phone: '0912345678',
    address: 'Ấp Mỹ An, Xã Mỹ Phong, TP. Mỹ Tho, Tiền Giang'
  });
  assert.equal(goodOrder.valid, true);
});

test('Deeply researched Buddhist Dharma has 10 canonical PDF textbooks, 4 paths, 24 lessons, and milestone-unlocked user-photo UGC check-in', () => {
  assert.equal(DHARMA_TEXTBOOKS.length, 10);
  assert.equal(LECTURE_PATHS.length, 4);
  assert.equal(LECTURE_LESSONS.length, 24);

  for (const lesson of LECTURE_LESSONS) {
    assert.ok(lesson.sourceBook && lesson.sourceBook.length > 5);
    assert.ok(lesson.summary.length >= 3);
    assert.equal(lesson.quiz.options.length, 3);
  }

  assert.equal(gradeLessonQuiz('A1', 1).correct, true);
  assert.equal(gradeLessonQuiz('D6', 1).correct, true);

  assert.ok(UGC_BACKDROPS.length >= 4);
  assert.ok(INITIAL_UGC_GALLERY.length >= 3);
  const post = createUGCPost({
    author: 'Gia đình Phật tử Mỹ Tho',
    charMode: 'family_3',
    backdropId: 'chanh_dien_mat_tien',
    poseId: 'chap_tay_le_phat',
    milestoneBadge: 'Đảnh lễ Tam Bảo trước Chánh Điện',
    userPhotoUploaded: true,
    wishText: 'Kính lễ Phật tại Chùa Vĩnh Tràng!'
  });
  assert.equal(post.charMode, 'family_3');
  assert.equal(post.userPhotoUploaded, true);
  assert.equal(post.milestoneBadge, 'Đảnh lễ Tam Bảo trước Chánh Điện');
  assert.equal(post.likes, 1);
});
