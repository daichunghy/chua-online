#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tạo trang web Chùa Vĩnh Tràng 3D Cartoon 100% HOÀN TOÀN GIỐNG ẢNH THAM KHẢO
(chua-vinh-trang-3d-cartoon-de-xuat-01.png - người phụ nữ 3D trong ngôi chùa 3D cartoon):
- Sử dụng trực tiếp ảnh gốc độ phân giải cao 1672x941 làm nền không gian 3D Cartoon chuẩn mực.
- Tích hợp lớp hiệu ứng thời gian thực (Real-time Canvas FX):
  * Cánh hoa sen / hoa sứ hồng bay lượn bồng bềnh trong gió.
  * Khói nhang trầm thơm uốn lượn bay lên trời khi dâng hương.
  * Hào quang hoa sen vàng rực rỡ tỏa sáng dưới chân người phụ nữ khi lễ Phật.
  * Hoa sen hồng bay dâng lên Tam Bảo khi dâng hoa.
  * Tiếng chuông gia trì, mõ trầm ấm, chuông gió WebAudio chuẩn xác.
- Tương tác di chuyển (Walk / Zoom):
  * Bấm D-Pad (▲, ▼, ◀, ▶) hoặc phím WASD / Mũi tên: Nhân vật tiến lại gần Chánh điện với âm thanh bước chân và hiệu ứng zoom chiều sâu.
- Các nút điều khiển chuẩn xác 100% theo vị trí ảnh gốc:
  * Top-left: Chùa Online | Chùa Vĩnh Tràng
  * Top-right: Khám phá, Học Phật, Tài khoản (+ Nút Cửa hàng & Âm thanh)
  * Pin: 📍 Chánh điện (nhấp vào để chiêm bái sâu vào nội điện bàn thờ Tam Bảo)
  * Bottom-left: D-Pad Di chuyển
  * Bottom-right: Lễ Phật, Dâng hương, Dâng hoa, Niệm Phật
- Toàn bộ Drawer / Modal thiết kế đồng bộ theo các ảnh đề xuất còn lại:
  * Giảng đường Phật pháp (giang-duong-phat-phap-de-xuat-01.png)
  * Cửa hàng lưu niệm (cua-hang-luu-niem-de-xuat-02.png)
  * Chứng nhận tu tập (Generated Audio November 03, 2026 - 10_16PM.png)
  * Khám phá 6 thắng cảnh Chùa Vĩnh Tràng
- Font chữ: 100% Calibri quy chuẩn.
"""

import os

def generate_perfect_html():
    return '''<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>Chùa Online — Chùa Vĩnh Tràng 3D Cartoon</title>
  <style>
    /* ==========================================================================
       QUY CHUẨN FONT CHỮ CALIBRI & GIAO DIỆN CHÙA ONLINE (CHUẨN 3D CARTOON)
       ========================================================================== */
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-tap-highlight-color: transparent;
    }
    html, body {
      width: 100%;
      height: 100%;
      overflow: hidden;
      font-family: Calibri, 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
      font-size: 11pt;
      line-height: 1.5;
      color: #2c2523;
      background: #1a2634;
      display: flex;
      align-items: center;
      justify-content: center;
      user-select: none;
    }

    /* Khung hiển thị khớp chuẩn tỷ lệ 1672 x 941 của ảnh tham khảo gốc */
    #stage-container {
      position: relative;
      width: 100vw;
      height: 100vh;
      max-width: calc(100vh * 1672 / 941);
      max-height: calc(100vw * 941 / 1672);
      margin: auto;
      overflow: hidden;
      background: #000;
      box-shadow: 0 0 50px rgba(0, 0, 0, 0.6);
    }

    /* ẢNH THAM KHẢO GỐC: NGƯỜI PHỤ NỮ 3D TRONG NGÔI CHÙA 3D CARTOON */
    #main-backdrop {
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
      pointer-events: none;
      transform-origin: 50% 65%;
      transition: transform 0.45s cubic-bezier(0.2, 0.85, 0.25, 1);
    }

    /* Lớp Canvas hiệu ứng hạt thời gian thực (Cánh hoa bay, khói nhang, hào quang) */
    #fx-canvas {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      z-index: 5;
    }

    /* ==========================================================================
       CÁC VÙNG TƯƠNG TÁC (INTERACTIVE HOTSPOTS) ĐẶT KHỚP 100% VỚI NÚT TRÊN ẢNH GỐC
       ========================================================================== */
    .hotspot {
      position: absolute;
      cursor: pointer;
      z-index: 10;
      border-radius: 20px;
      transition: all 0.2s cubic-bezier(0.2, 0.8, 0.2, 1);
    }

    .hotspot:hover {
      box-shadow: 0 0 16px rgba(245, 206, 88, 0.7), inset 0 0 10px rgba(255, 255, 255, 0.35);
      border: 1.5px solid rgba(245, 206, 88, 0.85);
    }

    .hotspot:active {
      transform: scale(0.95);
      box-shadow: 0 0 8px rgba(245, 206, 88, 0.9);
    }

    /* Top Left: Logo Chùa Online */
    #spot-logo {
      left: 1.5%;
      top: 1.8%;
      width: 31.5%;
      height: 7.2%;
      border-radius: 30px;
    }

    /* Top Right: Khám phá, Học Phật, Tài khoản */
    #spot-kham-pha {
      left: 68.0%;
      top: 1.8%;
      width: 10.6%;
      height: 7.2%;
      border-radius: 30px;
    }

    #spot-hoc-phat {
      left: 79.4%;
      top: 1.8%;
      width: 9.8%;
      height: 7.2%;
      border-radius: 30px;
    }

    #spot-tai-khoan {
      left: 89.6%;
      top: 1.8%;
      width: 9.6%;
      height: 7.2%;
      border-radius: 30px;
    }

    /* Floating Pin: 📍 Chánh điện */
    #spot-pin-chanh-dien {
      left: 45.4%;
      top: 35.5%;
      width: 9.3%;
      height: 5.6%;
      border-radius: 24px;
      animation: pinPulse 2.4s ease-in-out infinite;
    }

    @keyframes pinPulse {
      0%, 100% { transform: translateY(0); }
      50% { transform: translateY(-4px); }
    }

    /* D-Pad Di chuyển */
    #spot-dpad-up {
      left: 5.0%;
      top: 79.5%;
      width: 3.5%;
      height: 5.6%;
      border-radius: 8px;
    }
    #spot-dpad-left {
      left: 1.8%;
      top: 85.0%;
      width: 3.2%;
      height: 5.6%;
      border-radius: 8px;
    }
    #spot-dpad-right {
      left: 8.2%;
      top: 85.0%;
      width: 3.2%;
      height: 5.6%;
      border-radius: 8px;
    }
    #spot-dpad-down {
      left: 5.0%;
      top: 90.5%;
      width: 3.5%;
      height: 5.6%;
      border-radius: 8px;
    }

    /* 4 Nút hành trình tâm linh góc dưới phải */
    #spot-le-phat {
      left: 64.5%;
      top: 82.0%;
      width: 8.2%;
      height: 14.0%;
      border-radius: 16px;
    }
    #spot-dang-huong {
      left: 73.2%;
      top: 82.0%;
      width: 8.2%;
      height: 14.0%;
      border-radius: 16px;
    }
    #spot-dang-hoa {
      left: 81.9%;
      top: 82.0%;
      width: 8.2%;
      height: 14.0%;
      border-radius: 16px;
    }
    #spot-niem-phat {
      left: 90.5%;
      top: 82.0%;
      width: 8.2%;
      height: 14.0%;
      border-radius: 16px;
    }

    /* Phụ trợ: Nút Cửa Hàng & Âm Thanh nổi nhỏ nhắn, tinh tế */
    .extra-action-bar {
      position: absolute;
      top: 9.8%;
      right: 2.2%;
      display: flex;
      gap: 8px;
      z-index: 15;
    }

    .mini-pill {
      background: rgba(22, 54, 38, 0.88);
      backdrop-filter: blur(10px);
      -webkit-backdrop-filter: blur(10px);
      border: 1px solid rgba(255, 255, 255, 0.25);
      border-radius: 20px;
      color: #ffffff;
      display: flex;
      align-items: center;
      gap: 6px;
      padding: 6px 14px;
      font-size: 10pt;
      font-weight: 600;
      cursor: pointer;
      box-shadow: 0 4px 14px rgba(0,0,0,0.2);
      transition: all 0.2s ease;
    }

    .mini-pill:hover {
      background: rgba(30, 75, 52, 0.95);
      border-color: #f5ce58;
      transform: translateY(-1px);
    }

    /* ==========================================================================
       TOAST THÔNG BÁO TÂM LINH
       ========================================================================== */
    #spiritual-toast {
      position: absolute;
      top: 86px;
      left: 50%;
      transform: translateX(-50%) translateY(-20px);
      background: rgba(36, 21, 13, 0.94);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      border: 1.5px solid rgba(245, 206, 88, 0.65);
      border-radius: 30px;
      color: #fff8eb;
      padding: 10px 24px;
      font-size: 11.5pt;
      font-weight: 500;
      box-shadow: 0 8px 30px rgba(0, 0, 0, 0.35);
      display: flex;
      align-items: center;
      gap: 10px;
      z-index: 100;
      opacity: 0;
      pointer-events: none;
      transition: all 0.35s cubic-bezier(0.2, 0.9, 0.3, 1);
    }

    #spiritual-toast.show {
      opacity: 1;
      transform: translateX(-50%) translateY(0);
    }

    /* ==========================================================================
       MODALS & DRAWERS (CHUẨN ẢNH ĐỀ XUẤT)
       ========================================================================== */
    .modal-overlay {
      position: fixed;
      inset: 0;
      background: rgba(14, 10, 8, 0.58);
      backdrop-filter: blur(6px);
      -webkit-backdrop-filter: blur(6px);
      z-index: 200;
      display: flex;
      justify-content: center;
      align-items: flex-end;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.28s ease;
    }

    .modal-overlay.open {
      opacity: 1;
      pointer-events: auto;
    }

    .modal-card {
      background: #fdfbf7;
      border-radius: 28px 28px 0 0;
      width: 100%;
      max-width: 640px;
      max-height: 88vh;
      overflow-y: auto;
      padding: 24px 28px 36px;
      box-shadow: 0 -8px 40px rgba(0, 0, 0, 0.28);
      transform: translateY(100%);
      transition: transform 0.35s cubic-bezier(0.18, 0.89, 0.32, 1);
      display: flex;
      flex-direction: column;
      gap: 18px;
    }

    .modal-overlay.open .modal-card {
      transform: translateY(0);
    }

    .modal-drag-bar {
      width: 44px;
      height: 5px;
      background: #dfd7cc;
      border-radius: 3px;
      align-self: center;
      margin-bottom: 4px;
    }

    .modal-header-wrap {
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      gap: 6px;
      position: relative;
    }

    .modal-close-btn {
      position: absolute;
      top: 0;
      right: 0;
      background: #eee8de;
      border: none;
      width: 32px;
      height: 32px;
      border-radius: 50%;
      font-size: 14pt;
      color: #61564f;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.15s ease;
    }

    .modal-close-btn:hover {
      background: #e2dacd;
      color: #2c2523;
    }

    .modal-lotus-icon {
      font-size: 26pt;
      line-height: 1;
    }

    .modal-title {
      font-size: 16pt;
      font-weight: 700;
      color: #1b4931;
    }

    .modal-subtitle {
      font-size: 11pt;
      color: #6d6259;
    }

    .filter-tabs {
      display: flex;
      gap: 8px;
      background: #f1ebdE;
      padding: 4px;
      border-radius: 14px;
      overflow-x: auto;
    }

    .filter-tab {
      flex: 1;
      padding: 8px 12px;
      background: transparent;
      border: none;
      border-radius: 10px;
      font-family: inherit;
      font-size: 10.5pt;
      font-weight: 600;
      color: #655a52;
      cursor: pointer;
      transition: all 0.2s ease;
      white-space: nowrap;
    }

    .filter-tab.active {
      background: #1b4931;
      color: #ffffff;
      box-shadow: 0 2px 8px rgba(27, 73, 49, 0.25);
    }

    .item-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
      gap: 14px;
    }

    .item-card {
      background: #ffffff;
      border: 1px solid #ebd9c8;
      border-radius: 16px;
      padding: 14px;
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      gap: 8px;
      box-shadow: 0 2px 10px rgba(0,0,0,0.03);
    }

    .item-img-box {
      width: 100%;
      height: 100px;
      background: #fcf8f2;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 32pt;
    }

    .item-name {
      font-size: 11pt;
      font-weight: 600;
      color: #3b2f27;
    }

    .item-badge {
      font-size: 9.5pt;
      color: #8b5e3c;
      background: #fbf0e4;
      padding: 2px 8px;
      border-radius: 8px;
    }

    .btn-green {
      background: #1b4931;
      color: #ffffff;
      border: none;
      border-radius: 12px;
      padding: 8px 14px;
      font-family: inherit;
      font-size: 10pt;
      font-weight: 600;
      cursor: pointer;
      width: 100%;
      transition: all 0.15s ease;
    }

    .btn-green:hover {
      background: #256343;
    }

    .lecture-card {
      background: #ffffff;
      border: 1px solid #e7decb;
      border-radius: 16px;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      box-shadow: 0 2px 10px rgba(0,0,0,0.02);
    }

    .lecture-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .lecture-title {
      font-size: 12pt;
      font-weight: 600;
      color: #235237;
    }

    .audio-player-bar {
      display: flex;
      align-items: center;
      gap: 12px;
      background: #f7f1e6;
      border-radius: 12px;
      padding: 10px 14px;
      margin-top: 6px;
    }

    .play-btn-circle {
      width: 38px;
      height: 38px;
      border-radius: 50%;
      background: #1b4931;
      color: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      border: none;
      cursor: pointer;
      font-size: 12pt;
    }

    /* Hiệu ứng hào quang sen vàng dưới chân người phụ nữ */
    #aura-lotus {
      position: absolute;
      left: 33%;
      top: 86%;
      transform: translate(-50%, -50%) scale(0);
      width: 220px;
      height: 80px;
      background: radial-gradient(ellipse at center, rgba(255, 215, 64, 0.85) 0%, rgba(255, 179, 0, 0.4) 50%, rgba(255, 238, 88, 0) 80%);
      border-radius: 50%;
      pointer-events: none;
      z-index: 6;
      opacity: 0;
      transition: all 0.5s cubic-bezier(0.18, 0.89, 0.32, 1.28);
    }

    #aura-lotus.active {
      transform: translate(-50%, -50%) scale(1);
      opacity: 1;
    }
  </style>
</head>
<body>

  <!-- STAGE CHÍNH KHỚP CHUẨN 100% ẢNH THAM KHẢO -->
  <div id="stage-container">
    
    <!-- ẢNH GỐC THIẾT KẾ ĐỀ XUẤT 3D CARTOON (NGƯỜI PHỤ NỮ 3D TRONG CHÙA VĨNH TRÀNG 3D CARTOON) -->
    <img id="main-backdrop" src="../Thiết%20kế%20giao%20diện/chua-vinh-trang-3d-cartoon-de-xuat-01.png" alt="Chùa Vĩnh Tràng 3D Cartoon">

    <!-- CANVAS HIỆU ỨNG HẠT THỜI GIAN THỰC -->
    <canvas id="fx-canvas"></canvas>

    <!-- HÀO QUANG SEN DƯỚI CHÂN NGƯỜI PHỤ NỮ -->
    <div id="aura-lotus"></div>

    <!-- CÁC ĐIỂM TƯƠNG TÁC KHỚP CHUẨN XÁC NÚT TRÊN ẢNH GỐC -->
    <div class="hotspot" id="spot-logo" title="Chùa Online — Chùa Vĩnh Tràng"></div>

    <div class="hotspot" id="spot-kham-pha" title="Khám phá thắng cảnh Chùa Vĩnh Tràng"></div>
    <div class="hotspot" id="spot-hoc-phat" title="Giảng đường Phật pháp — Cùng nghe giảng, học từng bài"></div>
    <div class="hotspot" id="spot-tai-khoan" title="Tài khoản Phật tử & Chứng nhận tu tập"></div>

    <div class="hotspot" id="spot-pin-chanh-dien" title="📍 Chánh điện — Nhấp để chiêm ngưỡng nội điện Tam Bảo"></div>

    <!-- D-Pad Di chuyển -->
    <div class="hotspot" id="spot-dpad-up" title="Tiến tới sân Chánh điện (Phím W hoặc ▲)"></div>
    <div class="hotspot" id="spot-dpad-left" title="Nghiêng góc nhìn trái (Phím A hoặc ◀)"></div>
    <div class="hotspot" id="spot-dpad-right" title="Nghiêng góc nhìn phải (Phím D hoặc ▶)"></div>
    <div class="hotspot" id="spot-dpad-down" title="Lùi lại góc nhìn rộng (Phím S hoặc ▼)"></div>

    <!-- 4 Nút hành trình tâm linh -->
    <div class="hotspot" id="spot-le-phat" title="Lễ Phật — Đảnh lễ Đức Bổn Sư"></div>
    <div class="hotspot" id="spot-dang-huong" title="Dâng hương — Thắp tâm nhang thanh tịnh"></div>
    <div class="hotspot" id="spot-dang-hoa" title="Dâng hoa — Dâng đóa sen hồng"></div>
    <div class="hotspot" id="spot-niem-phat" title="Niệm Phật — Gõ mõ & lần 108 hạt"></div>

    <!-- Thanh tiện ích nhỏ gọn góc trên: Cửa hàng & Âm thanh -->
    <div class="extra-action-bar">
      <button class="mini-pill" id="btn-open-shop">
        <span>🛍️</span> <span>Cửa hàng</span>
      </button>
      <button class="mini-pill" id="btn-toggle-sound">
        <span id="sound-icon">🔔</span> <span id="sound-text">Âm thanh: Bật</span>
      </button>
    </div>

    <!-- SPIRITUAL TOAST -->
    <div id="spiritual-toast">
      <span id="toast-icon">🪷</span>
      <span id="toast-text">Tâm thành kính chiêm bái Đức Phật...</span>
    </div>

  </div>

  <!-- ==========================================================================
       MODAL 1: GIẢNG ĐƯỜNG PHẬT PHÁP (CHUẨN giang-duong-phat-phap-de-xuat-01.png)
       ========================================================================== -->
  <div class="modal-overlay" id="modal-hoc-phat">
    <div class="modal-card">
      <div class="modal-drag-bar"></div>
      <div class="modal-header-wrap">
        <button class="modal-close-btn" data-close="modal-hoc-phat">&times;</button>
        <span class="modal-lotus-icon">🪷</span>
        <h2 class="modal-title">Giảng đường Phật pháp</h2>
        <p class="modal-subtitle">Cùng nghe giảng, học từng bài — Nơi nuôi dưỡng tâm từ bi & trí tuệ</p>
      </div>

      <div class="filter-tabs">
        <button class="filter-tab active">Tất cả bài học</button>
        <button class="filter-tab">Căn bản Phật học</button>
        <button class="filter-tab">Thiền & Chánh niệm</button>
      </div>

      <div class="lecture-card">
        <div class="lecture-row">
          <span class="lecture-title">Bài 1: Đạo Phật là gì? — Nguồn gốc & Tinh thần giải thoát</span>
          <span class="item-badge">Bài mở đầu</span>
        </div>
        <p style="font-size:10pt; color:#6b5f56;">Tìm hiểu về cuộc đời Đức Phật Thích Ca Mâu Ni và con đường đưa đến an lạc nội tâm giữa đời thường.</p>
        <div class="audio-player-bar">
          <button class="play-btn-circle" id="btn-play-lecture-1">▶</button>
          <div style="flex:1;">
            <div style="font-size:10pt; font-weight:600; color:#235237;" id="lecture-status-1">Giảng đường Huệ Đăng — Thời lượng: 12 phút</div>
            <div style="height:4px; background:#e1d8c8; border-radius:2px; margin-top:4px; overflow:hidden;">
              <div id="lecture-prog-1" style="width:0%; height:100%; background:#1b4931; transition:width 0.3s;"></div>
            </div>
          </div>
        </div>
      </div>

      <div class="lecture-card">
        <div class="lecture-row">
          <span class="lecture-title">Bài 2: Tam Bảo — Ba ngôi báu nương tựa vững chãi</span>
          <span class="item-badge">Phật học căn bản</span>
        </div>
        <p style="font-size:10pt; color:#6b5f56;">Ý nghĩa sâu xa của Phật bảo, Pháp bảo và Tăng bảo đối với người Phật tử tại gia.</p>
        <button class="btn-green" style="margin-top:6px;" onclick="triggerToast('📿 Đã mở bài học Tam Bảo vào hành trang tu học!', 3000)">Nghe bài học</button>
      </div>

      <div class="lecture-card">
        <div class="lecture-row">
          <span class="lecture-title">Bài 3: Ngũ Giới & Bát Chánh Đạo — Con đường an lạc</span>
          <span class="item-badge">Thực hành hằng ngày</span>
        </div>
        <p style="font-size:10pt; color:#6b5f56;">Năm điều răn gìn giữ phẩm hạnh và tám con đường chân chính để diệt trừ phiền não.</p>
        <button class="btn-green" style="margin-top:6px;" onclick="triggerToast('🌸 Đã chọn bài học Ngũ Giới & Bát Chánh Đạo!', 3000)">Nghe bài học</button>
      </div>
    </div>
  </div>

  <!-- ==========================================================================
       MODAL 2: CỬA HÀNG LƯU NIỆM (CHUẨN cua-hang-luu-niem-de-xuat-02.png)
       ========================================================================== -->
  <div class="modal-overlay" id="modal-cua-hang">
    <div class="modal-card">
      <div class="modal-drag-bar"></div>
      <div class="modal-header-wrap">
        <button class="modal-close-btn" data-close="modal-cua-hang">&times;</button>
        <span class="modal-lotus-icon">🛍️</span>
        <h2 class="modal-title">Cửa hàng lưu niệm</h2>
        <p class="modal-subtitle">Chọn món quà gợi nhớ chuyến đi chùa — Thỉnh pháp bảo gieo duyên lành</p>
      </div>

      <div class="filter-tabs">
        <button class="filter-tab active">Quà lưu niệm</button>
        <button class="filter-tab">Đồ tu học</button>
        <button class="filter-tab">Vật phẩm 3D</button>
      </div>

      <div class="item-grid">
        <div class="item-card">
          <div class="item-img-box">📔</div>
          <span class="item-name">Sổ tay hoa sen</span>
          <span class="item-badge">Bìa da dập nhũ vàng</span>
          <button class="btn-green" onclick="triggerToast('📔 Đã thỉnh Sổ tay hoa sen — Lưu giữ lời Phật dạy!', 3000)">Thỉnh vật phẩm</button>
        </div>

        <div class="item-card">
          <div class="item-img-box">📿</div>
          <span class="item-name">Tràng hạt gỗ</span>
          <span class="item-badge">108 hạt gỗ trầm hương</span>
          <button class="btn-green" onclick="triggerToast('📿 Đã thỉnh Tràng hạt 108 hạt tâm niệm an lạc!', 3000)">Thỉnh vật phẩm</button>
        </div>

        <div class="item-card">
          <div class="item-img-box">🖼️</div>
          <span class="item-name">Bưu thiếp chùa</span>
          <span class="item-badge">Bộ ảnh 3D Vĩnh Tràng</span>
          <button class="btn-green" onclick="triggerToast('🖼️ Đã lưu bưu thiếp kỷ niệm chuyến viếng Chùa Vĩnh Tràng!', 3000)">Thỉnh vật phẩm</button>
        </div>

        <div class="item-card">
          <div class="item-img-box">👒</div>
          <span class="item-name">Nón lá thêu sen</span>
          <span class="item-badge">Truyền thống Nam Bộ</span>
          <button class="btn-green" onclick="triggerToast('👒 Đã thỉnh Nón lá thêu sen trang nghiêm!', 3000)">Thỉnh vật phẩm</button>
        </div>

        <div class="item-card">
          <div class="item-img-box">👜</div>
          <span class="item-name">Túi vải sen</span>
          <span class="item-badge">Vải bố mộc thêu sen</span>
          <button class="btn-green" onclick="triggerToast('👜 Đã mang túi vải sen đồng hành cùng bạn!', 3000)">Thỉnh vật phẩm</button>
        </div>

        <div class="item-card">
          <div class="item-img-box">👘</div>
          <span class="item-name">Áo tràng Phật tử</span>
          <span class="item-badge">Áo tràng lam trang nghiêm</span>
          <button class="btn-green" onclick="triggerToast('👘 Áo tràng lam đã sẵn sàng cho buổi chiêm bái!', 3000)">Thỉnh vật phẩm</button>
        </div>
      </div>
    </div>
  </div>

  <!-- ==========================================================================
       MODAL 3: KHÁM PHÁ CÁC ĐIỂM THẮNG CẢNH CHÙA VĨNH TRÀNG
       ========================================================================== -->
  <div class="modal-overlay" id="modal-kham-pha">
    <div class="modal-card">
      <div class="modal-drag-bar"></div>
      <div class="modal-header-wrap">
        <button class="modal-close-btn" data-close="modal-kham-pha">&times;</button>
        <span class="modal-lotus-icon">🧭</span>
        <h2 class="modal-title">Khám phá Chùa Vĩnh Tràng</h2>
        <p class="modal-subtitle">Di tích kiến trúc nghệ thuật cấp quốc gia gần 200 năm tuổi tại Mỹ Tho</p>
      </div>

      <div class="lecture-card" style="cursor:pointer;" onclick="closeModal(); triggerToast('🏛️ Đang chiêm bái: Mặt tiền Chánh điện Chùa Vĩnh Tràng', 3000);">
        <div class="lecture-row">
          <span class="lecture-title">🏛️ Mặt tiền Chánh điện</span>
          <span class="item-badge">Góc nhìn chính</span>
        </div>
        <p style="font-size:10pt; color:#6b5f56;">Kiến trúc giao thoa Đông — Tây độc nhất vô nhị: 13 cửa vòm cuốn La Mã, cột gốm xanh mosaic, tháp mái Angkor chạm phù điêu khảm sành sứ tinh xảo.</p>
      </div>

      <div class="lecture-card" style="cursor:pointer;" onclick="closeModal(); zoomToAltar();">
        <div class="lecture-row">
          <span class="lecture-title">🪷 Nội điện Tam Bảo</span>
          <span class="item-badge">Tôn nghiêm</span>
        </div>
        <p style="font-size:10pt; color:#6b5f56;">Nơi tôn trí kim thân Đức Phật Thích Ca Mâu Ni dát vàng trên đài sen cùng bộ tượng 18 vị La Hán bằng gỗ mít chạm khắc sống động từ năm 1907.</p>
      </div>

      <div class="lecture-card" style="cursor:pointer;" onclick="closeModal(); triggerToast('😃 Đại tượng Phật Di Lặc nụ cười hoan hỷ cao 20m, nặng 250 tấn ngự trong khuôn viên dừa xanh.', 4000);">
        <div class="lecture-row">
          <span class="lecture-title">😃 Đại tượng Phật Di Lặc</span>
          <span class="item-badge">Hoa sen an lạc</span>
        </div>
        <p style="font-size:10pt; color:#6b5f56;">Pho tượng màu trắng tuyết ngự trên đài hoa sen, nụ cười hoan hỷ cao 20m, nặng 250 tấn ngự trong khuôn viên vườn dừa xanh ngát.</p>
      </div>

      <div class="lecture-card" style="cursor:pointer;" onclick="closeModal(); triggerToast('🌸 Đại tượng Phật A Di Đà uy nghi cao 24m trên đài sen xanh tiếp dẫn chúng sanh.', 4000);">
        <div class="lecture-row">
          <span class="lecture-title">🌸 Đại tượng Phật A Di Đà</span>
          <span class="item-badge">Đài sen xanh</span>
        </div>
        <p style="font-size:10pt; color:#6b5f56;">Tượng đứng uy nghi cao 24m trên đài sen xanh, tay chỉ trời tay chỉ đất tiếp dẫn chúng sanh về cõi Cực Lạc bình an.</p>
      </div>

      <div class="lecture-card" style="cursor:pointer;" onclick="closeModal(); triggerToast('🛏️ Đại tượng Đức Phật Thích Ca Niết Bàn an nhiên dài 35m.', 4000);">
        <div class="lecture-row">
          <span class="lecture-title">🛏️ Đại tượng Phật Thích Ca Niết Bàn</span>
          <span class="item-badge">Thanh thản vô ưu</span>
        </div>
        <p style="font-size:10pt; color:#6b5f56;">Pho tượng Phật nhập Niết Bàn an nhiên dài 35m, bệ đá khắc dòng chữ "Nam Mô Bổn Sư Thích Ca Mâu Ni Phật" tôn kính.</p>
      </div>
    </div>
  </div>

  <!-- ==========================================================================
       MODAL 4: TÀI KHOẢN & CHỨNG NHẬN TU TẬP (CHUẨN Generated Audio November 03...)
       ========================================================================== -->
  <div class="modal-overlay" id="modal-tai-khoan">
    <div class="modal-card">
      <div class="modal-drag-bar"></div>
      <div class="modal-header-wrap">
        <button class="modal-close-btn" data-close="modal-tai-khoan">&times;</button>
        <span class="modal-lotus-icon">👤</span>
        <h2 class="modal-title">Chứng Nhận Tu Tập</h2>
        <p class="modal-subtitle">Chùa Online — Không gian tu học Phật pháp số</p>
      </div>

      <div class="lecture-card" style="background:#fffcf5; border:1.5px solid #d8be8d; text-align:center;">
        <div style="font-size:10.5pt; color:#856404; text-transform:uppercase; letter-spacing:1px; margin-bottom:4px;">Phật tử</div>
        <div style="font-size:16pt; font-weight:700; color:#5c3a21;" id="devotee-name">Diệu An</div>
        <div style="font-size:11pt; color:#7d6f66; margin-top:2px;">Đang tu tập tại <strong>Chùa Vĩnh Tràng</strong> (Mỹ Tho, Tiền Giang)</div>

        <div style="display:flex; justify-content:space-around; margin-top:14px; background:#f7f1e4; padding:12px; border-radius:14px;">
          <div>
            <div style="font-size:16pt; font-weight:700; color:#8b5e3c;" id="stat-streak">21</div>
            <div style="font-size:9.5pt; color:#6b5f56;">Ngày liên tục</div>
          </div>
          <div style="border-left:1px solid #e2d7c5;"></div>
          <div>
            <div style="font-size:16pt; font-weight:700; color:#8b5e3c;" id="stat-hours">10h 30m</div>
            <div style="font-size:9.5pt; color:#6b5f56;">Tổng thời gian tu tập</div>
          </div>
        </div>

        <p style="font-size:10pt; font-style:italic; color:#6b5f56; margin-top:12px;">"Nguyện tinh tấn tu học, giữ tâm an lạc, vun bồi thiện lành."</p>
      </div>

      <div style="font-size:11.5pt; font-weight:700; color:#1b4931;">Ghi nhận công đức buổi viếng chùa:</div>
      <div style="display:flex; justify-content:space-between; background:#ffffff; border:1px solid #ebd9c8; border-radius:12px; padding:12px 18px;">
        <span>Số lần đảnh lễ Tam Bảo:</span>
        <strong style="color:#8b5e3c;" id="stat-bows">12 lần</strong>
      </div>
      <div style="display:flex; justify-content:space-between; background:#ffffff; border:1px solid #ebd9c8; border-radius:12px; padding:12px 18px;">
        <span>Hạt chuỗi niệm Phật:</span>
        <strong style="color:#8b5e3c;" id="stat-chants">108 hạt</strong>
      </div>
    </div>
  </div>

  <!-- ==========================================================================
       JAVASCRIPT: HIỆU ỨNG TƯƠNG TÁC THỜI GIAN THỰC & ÂM THANH CHÙA
       ========================================================================== -->
  <script>
    // 1. ÂM THANH WEBAUDIO (CHUÔNG GIA TRÌ, MÕ TRẦM, CHUÔNG GIÓ)
    let audioCtx = null;
    let isAudioOn = true;

    function getAudioContext() {
      if (!audioCtx) {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      }
      if (audioCtx.state === 'suspended') {
        audioCtx.resume();
      }
      return audioCtx;
    }

    function playBell() {
      if (!isAudioOn) return;
      const ctx = getAudioContext();
      const now = ctx.currentTime;
      const freqs = [587.33, 1174.66, 1760.0, 2349.32];
      const gains = [0.65, 0.25, 0.12, 0.05];

      freqs.forEach((f, i) => {
        const osc = ctx.createOscillator();
        const g = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(f, now);
        osc.frequency.exponentialRampToValueAtTime(f * 0.995, now + 4.5);

        g.gain.setValueAtTime(gains[i], now);
        g.gain.exponentialRampToValueAtTime(0.0001, now + 4.5);

        osc.connect(g);
        g.connect(ctx.destination);
        osc.start(now);
        osc.stop(now + 4.5);
      });
    }

    function playMokugyo() {
      if (!isAudioOn) return;
      const ctx = getAudioContext();
      const now = ctx.currentTime;

      const osc = ctx.createOscillator();
      const g = ctx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(320, now);
      osc.frequency.exponentialRampToValueAtTime(130, now + 0.14);

      g.gain.setValueAtTime(0.9, now);
      g.gain.exponentialRampToValueAtTime(0.001, now + 0.16);

      osc.connect(g);
      g.connect(ctx.destination);
      osc.start(now);
      osc.stop(now + 0.17);
    }

    function playFootstep() {
      if (!isAudioOn) return;
      const ctx = getAudioContext();
      const now = ctx.currentTime;
      const osc = ctx.createOscillator();
      const g = ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(90, now);
      osc.frequency.exponentialRampToValueAtTime(40, now + 0.06);
      g.gain.setValueAtTime(0.15, now);
      g.gain.exponentialRampToValueAtTime(0.001, now + 0.07);
      osc.connect(g);
      g.connect(ctx.destination);
      osc.start(now);
      osc.stop(now + 0.08);
    }

    function playWindChime() {
      if (!isAudioOn) return;
      const ctx = getAudioContext();
      const now = ctx.currentTime;
      const notes = [1318.5, 1479.98, 1760.0, 1975.5, 2349.3];
      const pitch = notes[Math.floor(Math.random() * notes.length)];

      const osc = ctx.createOscillator();
      const g = ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(pitch, now);
      g.gain.setValueAtTime(0.18, now);
      g.gain.exponentialRampToValueAtTime(0.0001, now + 2.2);

      osc.connect(g);
      g.connect(ctx.destination);
      osc.start(now);
      osc.stop(now + 2.2);
    }

    setInterval(() => {
      if (isAudioOn && Math.random() < 0.35) {
        playWindChime();
      }
    }, 6000);

    // 2. CANVAS HIỆU ỨNG THỜI GIAN THỰC (CÁNH HOA SEN BAY, KHÓI NHANG, HẠT VÀNG)
    const fxCanvas = document.getElementById('fx-canvas');
    const ctx = fxCanvas.getContext('2d');
    let width, height;

    function resizeCanvas() {
      const rect = fxCanvas.getBoundingClientRect();
      width = fxCanvas.width = rect.width;
      height = fxCanvas.height = rect.height;
    }
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    // Hệ thống hạt cánh hoa rơi bồng bềnh
    const petals = [];
    for (let i = 0; i < 28; i++) {
      petals.push({
        x: Math.random() * 1600,
        y: Math.random() * 900,
        size: 5 + Math.random() * 8,
        speedY: 0.6 + Math.random() * 1.1,
        speedX: 0.3 + Math.random() * 0.8,
        angle: Math.random() * Math.PI * 2,
        angularSpeed: (Math.random() - 0.5) * 0.04,
        opacity: 0.5 + Math.random() * 0.45,
        color: Math.random() > 0.4 ? '#ff69b4' : '#ff1493'
      });
    }

    // Hạt khói nhang
    const smokes = [];
    function emitSmoke(x, y) {
      for (let i = 0; i < 6; i++) {
        smokes.push({
          x: x + (Math.random() - 0.5) * 12,
          y: y,
          vx: (Math.random() - 0.5) * 0.6,
          vy: -1.2 - Math.random() * 1.0,
          radius: 3 + Math.random() * 4,
          maxRadius: 28 + Math.random() * 15,
          opacity: 0.65,
          life: 0,
          maxLife: 90 + Math.random() * 40
        });
      }
    }

    // Vòng lặp vẽ hiệu ứng
    function fxLoop() {
      ctx.clearRect(0, 0, width, height);
      const scaleX = width / 1672;
      const scaleY = height / 941;

      // Vẽ cánh hoa bay
      petals.forEach(p => {
        p.y += p.speedY;
        p.x += p.speedX;
        p.angle += p.angularSpeed;

        if (p.y > 960) p.y = -20;
        if (p.x > 1700) p.x = -20;

        ctx.save();
        ctx.translate(p.x * scaleX, p.y * scaleY);
        ctx.rotate(p.angle);
        ctx.globalAlpha = p.opacity;
        ctx.fillStyle = p.color;

        // Vẽ hình cánh hoa sen
        ctx.beginPath();
        ctx.ellipse(0, 0, p.size * scaleX, (p.size * 0.55) * scaleY, 0, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
      });

      // Vẽ khói nhang
      for (let i = smokes.length - 1; i >= 0; i--) {
        const s = smokes[i];
        s.life++;
        s.x += s.vx;
        s.y += s.vy;
        const progress = s.life / s.maxLife;
        const currentR = s.radius + (s.maxRadius - s.radius) * progress;
        const currentAlpha = s.opacity * (1 - progress);

        ctx.save();
        ctx.globalAlpha = Math.max(0, currentAlpha);
        const grad = ctx.createRadialGradient(
          s.x * scaleX, s.y * scaleY, 0,
          s.x * scaleX, s.y * scaleY, currentR * scaleX
        );
        grad.addColorStop(0, 'rgba(255, 250, 240, 0.7)');
        grad.addColorStop(0.6, 'rgba(240, 230, 215, 0.3)');
        grad.addColorStop(1, 'rgba(235, 225, 210, 0)');
        ctx.fillStyle = grad;
        ctx.beginPath();
        ctx.arc(s.x * scaleX, s.y * scaleY, currentR * scaleX, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();

        if (s.life >= s.maxLife) {
          smokes.splice(i, 1);
        }
      }

      requestAnimationFrame(fxLoop);
    }
    fxLoop();

    // 3. TƯƠNG TÁC DI CHUYỂN / ZOOM CHIỀU SÂU (WALK INTO PAGODA)
    const backdrop = document.getElementById('main-backdrop');
    let currentZoom = 1.0;
    let currentPanX = 0;
    let currentPanY = 0;

    function updateTransform() {
      backdrop.style.transform = `scale(${currentZoom}) translate(${currentPanX}%, ${currentPanY}%)`;
    }

    function walkForward() {
      playFootstep();
      currentZoom = Math.min(1.45, currentZoom + 0.08);
      updateTransform();
      triggerToast('👣 Bạn đang bước tiến vào sân Chùa Vĩnh Tràng...', 1500, '🌿');
    }

    function walkBackward() {
      playFootstep();
      currentZoom = Math.max(1.0, currentZoom - 0.08);
      if (currentZoom === 1.0) {
        currentPanX = 0;
        currentPanY = 0;
      }
      updateTransform();
    }

    function panLeft() {
      playFootstep();
      currentPanX = Math.min(6, currentPanX + 1.5);
      updateTransform();
    }

    function panRight() {
      playFootstep();
      currentPanX = Math.max(-6, currentPanX - 1.5);
      updateTransform();
    }

    document.getElementById('spot-dpad-up').onclick = walkForward;
    document.getElementById('spot-dpad-down').onclick = walkBackward;
    document.getElementById('spot-dpad-left').onclick = panLeft;
    document.getElementById('spot-dpad-right').onclick = panRight;

    window.addEventListener('keydown', e => {
      switch (e.code) {
        case 'KeyW': case 'ArrowUp': walkForward(); break;
        case 'KeyS': case 'ArrowDown': walkBackward(); break;
        case 'KeyA': case 'ArrowLeft': panLeft(); break;
        case 'KeyD': case 'ArrowRight': panRight(); break;
      }
    });

    // 4. TOAST THÔNG BÁO TÂM LINH
    const toast = document.getElementById('spiritual-toast');
    const toastIcon = document.getElementById('toast-icon');
    const toastText = document.getElementById('toast-text');
    let toastTimeout = null;

    window.triggerToast = function(msg, duration = 3000, icon = '🪷') {
      toastText.textContent = msg;
      toastIcon.textContent = icon;
      toast.classList.add('show');
      if (toastTimeout) clearTimeout(toastTimeout);
      toastTimeout = setTimeout(() => {
        toast.classList.remove('show');
      }, duration);
    };

    // 5. CÁC HÀNH ĐỘNG TÂM LINH
    const auraLotus = document.getElementById('aura-lotus');
    let bowCount = 12;
    let chantCount = 108;

    // LỄ PHẬT: Chuông ngân vang, hoa sen vàng tỏa sáng dưới chân người phụ nữ
    document.getElementById('spot-le-phat').onclick = () => {
      playBell();
      bowCount++;
      document.getElementById('stat-bows').textContent = `${bowCount} lần`;

      auraLotus.classList.add('active');
      triggerToast('Nam Mô Bổn Sư Thích Ca Mâu Ni Phật — Con chí tâm đảnh lễ Tam Bảo!', 4000, '🪷');

      setTimeout(() => {
        auraLotus.classList.remove('active');
      }, 3500);
    };

    // DÂNG HƯƠNG: Thắp nhang trầm thơm ngát, khói bay lên trời
    document.getElementById('spot-dang-huong').onclick = () => {
      playBell();
      triggerToast('Khói trầm xông ngát mười phương — Nguyện cầu quốc thái dân an, gia đạo cát tường!', 4200, '♨️');

      // Tỏa khói nhang tại vị trí lư hương sân chùa (x: 836, y: 520)
      for (let k = 0; k < 4; k++) {
        setTimeout(() => emitSmoke(836, 520), k * 250);
      }
    };

    // DÂNG HOA: Dâng đóa sen hồng tươi thắm
    document.getElementById('spot-dang-hoa').onclick = () => {
      playBell();
      triggerToast('Dâng đóa sen hồng tươi thắm — Tâm thanh tịnh, nở hoa trí tuệ an vui!', 3800, '🌸');

      // Tăng cường mưa cánh hoa sen
      for (let i = 0; i < 20; i++) {
        petals.push({
          x: 400 + Math.random() * 800,
          y: -20 - Math.random() * 100,
          size: 7 + Math.random() * 9,
          speedY: 1.2 + Math.random() * 1.5,
          speedX: (Math.random() - 0.5) * 1.2,
          angle: Math.random() * Math.PI * 2,
          angularSpeed: (Math.random() - 0.5) * 0.06,
          opacity: 0.85,
          color: '#ff4081'
        });
      }
    };

    // NIỆM PHẬT: Gõ mõ & lần chuỗi hạt
    document.getElementById('spot-niem-phat').onclick = () => {
      playMokugyo();
      chantCount++;
      document.getElementById('stat-chants').textContent = `${chantCount} hạt`;

      const mantras = [
        'Nam Mô A Di Đà Phật',
        'Nam Mô Bổn Sư Thích Ca Mâu Ni Phật',
        'Nam Mô Quán Thế Âm Bồ Tát'
      ];
      const mText = mantras[chantCount % mantras.length];
      triggerToast(`${mText} (Hạt thứ ${chantCount % 108 || 108}/108)`, 2400, '📿');
    };

    // NHẤP VÀO PIN "📍 Chánh điện": Phóng tầm mắt vào chiêm bái nội điện Tam Bảo
    window.zoomToAltar = function() {
      playBell();
      currentZoom = 1.45;
      currentPanX = 0;
      currentPanY = -8;
      updateTransform();
      triggerToast('🏛️ Đang chiêm ngưỡng Kim thân Đức Phật Thích Ca dát vàng toạ thiền nội điện!', 4000, '📍');
    };
    document.getElementById('spot-pin-chanh-dien').onclick = window.zoomToAltar;

    // 6. MODALS
    function openModal(id) {
      document.querySelectorAll('.modal-overlay').forEach(m => m.classList.remove('open'));
      const target = document.getElementById(id);
      if (target) target.classList.add('open');
    }

    function closeModal() {
      document.querySelectorAll('.modal-overlay').forEach(m => m.classList.remove('open'));
    }
    window.closeModal = closeModal;

    document.querySelectorAll('[data-close]').forEach(btn => {
      btn.onclick = () => closeModal();
    });

    document.querySelectorAll('.modal-overlay').forEach(overlay => {
      overlay.onclick = e => {
        if (e.target === overlay) closeModal();
      };
    });

    document.getElementById('spot-kham-pha').onclick = () => openModal('modal-kham-pha');
    document.getElementById('spot-hoc-phat').onclick = () => openModal('modal-hoc-phat');
    document.getElementById('spot-tai-khoan').onclick = () => openModal('modal-tai-khoan');
    document.getElementById('btn-open-shop').onclick = () => openModal('modal-cua-hang');

    // Bật tắt âm thanh
    const btnSound = document.getElementById('btn-toggle-sound');
    const soundIcon = document.getElementById('sound-icon');
    const soundText = document.getElementById('sound-text');

    btnSound.onclick = () => {
      isAudioOn = !isAudioOn;
      if (isAudioOn) {
        soundIcon.textContent = '🔔';
        soundText.textContent = 'Âm thanh: Bật';
        playBell();
        triggerToast('🔔 Đã bật âm thanh chuông mõ thanh tịnh', 2000);
      } else {
        soundIcon.textContent = '🔕';
        soundText.textContent = 'Âm thanh: Tắt';
        triggerToast('🔕 Đã tắt âm thanh', 2000);
      }
    };

    // Nghe bài giảng 1
    let isLecturePlaying = false;
    let lectureTimer = null;
    const btnPlayLec1 = document.getElementById('btn-play-lecture-1');
    const progLec1 = document.getElementById('lecture-prog-1');
    const statusLec1 = document.getElementById('lecture-status-1');

    btnPlayLec1.onclick = () => {
      isLecturePlaying = !isLecturePlaying;
      if (isLecturePlaying) {
        btnPlayLec1.textContent = '⏸';
        playBell();
        statusLec1.textContent = 'Đang phát: Đạo Phật là gì? — Thầy Thích Thiện Hoa';
        let p = 0;
        lectureTimer = setInterval(() => {
          p += 1;
          progLec1.style.width = p + '%';
          if (p >= 100) {
            clearInterval(lectureTimer);
            btnPlayLec1.textContent = '▶';
            statusLec1.textContent = 'Đã hoàn thành bài học 1';
          }
        }, 300);
      } else {
        btnPlayLec1.textContent = '▶';
        statusLec1.textContent = 'Tạm dừng bài học';
        if (lectureTimer) clearInterval(lectureTimer);
      }
    };
  </script>
</body>
</html>
'''

def main():
    base_dir = "/Users/macos/Desktop/Chùa online"
    html_content = generate_perfect_html()
    
    target_files = [
        os.path.join(base_dir, "Mô hình 3D Vĩnh Tràng", "trai-nghiem-chua-vinh-trang-3d.html"),
        os.path.join(base_dir, "Mô hình 3D Vĩnh Tràng", "trai-nghiem-vinh-trang-v3.html")
    ]
    
    for path in target_files:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"Generated: {path} ({len(html_content)} bytes)")

if __name__ == "__main__":
    main()
