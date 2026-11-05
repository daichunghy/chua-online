#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script tạo file trai-nghiem-chua-vinh-trang-3d.html hoàn chỉnh với:
1. Không gian Chánh Điện (Đại Hùng Bửu Điện) Chùa Vĩnh Tràng đồ sộ, tráng lệ.
2. Hai dãy tường Tả - Hữu có ĐỦ 18 vị Thập Bát La Hán gỗ mít thếp vàng cưỡi linh thú.
3. Hai Đại Khám Thờ Bồ Tát Quán Thế Âm Chuẩn Đề & Bồ Tát Địa Tạng Vương ở giữa 2 vách.
4. Tượng Hộ Pháp Vi Đà & Tiêu Diện Đại Sĩ ở tiền điện.
5. Sàn gạch đỏ bóng loáng phản chiếu ánh nến và hào quang Phật (procedural terracotta tile texture).
6. 3 Đèn chùm pha lê Pháp buông từ xà gồ gỗ trên trần (biểu tượng độc nhất Vĩnh Tràng).
7. Hai cột rồng thếp vàng và hoành phi 「黃金寶殿」, 「勅賜 永長寺」, câu đối chữ Hán vàng.
8. Floating nametags 3D trên đầu avatar các đồng tu (Tự Phong Hiếu Hạnh, Thích Từ Quang...).
9. Đầy đủ tính năng tương tác cúng bái (Lạy Phật gật camera, tràng hạt 108, tụng kinh, dâng lễ).
10. Tối ưu hóa chuyển đổi mua hàng: Thả Đèn Nguyện Cầu An, Thỉnh Pháp Bảo Thật ship tận nhà, Thỉnh Tượng La Hán Hộ Mệnh.
11. Tuân thủ 100% font Calibri và UI thanh tịnh, trang nghiêm.
"""

import os

html_code = """<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>Đại Hùng Bửu Điện — Chùa Vĩnh Tràng 3D</title>
  <script type="importmap">
    {
      "imports": {
        "three": "https://unpkg.com/three@0.160.0/build/three.module.js",
        "three/addons/": "https://unpkg.com/three@0.160.0/examples/jsm/"
      }
    }
  </script>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: Calibri, 'Segoe UI', -apple-system, sans-serif;
      font-size: 11pt;
      line-height: 1.5;
      background: #140804;
      color: #fcefdc;
      overflow: hidden;
      height: 100vh;
      width: 100vw;
      user-select: none;
    }
    #canvas-container {
      position: absolute;
      inset: 0;
      z-index: 1;
    }
    #three-canvas {
      width: 100%;
      height: 100%;
      display: block;
    }

    /* 3D FLOATING NAMETAGS OVERLAY */
    #nametags-container {
      position: absolute;
      inset: 0;
      pointer-events: none;
      z-index: 8;
      overflow: hidden;
    }
    .nametag {
      position: absolute;
      top: 0;
      left: 0;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 3px;
      pointer-events: none;
      transition: opacity 0.2s;
      white-space: nowrap;
    }
    .nametag-badge {
      background: rgba(36, 17, 10, 0.88);
      border: 1px solid rgba(230, 184, 92, 0.65);
      border-radius: 12px;
      padding: 3px 9px;
      font-size: 9pt;
      font-weight: 600;
      color: #ffd88a;
      box-shadow: 0 4px 12px rgba(0,0,0,0.6);
      display: flex;
      align-items: center;
      gap: 5px;
    }
    .nametag-level {
      background: #7a2817;
      color: #fff0d6;
      font-size: 7.5pt;
      padding: 1px 5px;
      border-radius: 8px;
    }
    .nametag.is-user .nametag-badge {
      background: rgba(94, 27, 14, 0.95);
      border: 1.5px solid #ffcc44;
      color: #ffffff;
      box-shadow: 0 0 16px rgba(255, 204, 68, 0.7);
    }
    .nametag-pointer {
      width: 0;
      height: 0;
      border-left: 6px solid transparent;
      border-right: 6px solid transparent;
      border-top: 7px solid #ffd88a;
      animation: floatPointer 1.5s ease-in-out infinite alternate;
    }
    @keyframes floatPointer {
      from { transform: translateY(0); }
      to { transform: translateY(-4px); }
    }

    /* TOP BAR */
    header {
      position: absolute;
      top: 14px;
      left: 18px;
      right: 18px;
      z-index: 10;
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      pointer-events: none;
    }
    .user-profile-badge {
      pointer-events: auto;
      background: rgba(43, 20, 13, 0.92);
      backdrop-filter: blur(14px);
      border: 1px solid rgba(230, 184, 92, 0.5);
      border-radius: 14px;
      padding: 10px 16px;
      display: flex;
      align-items: center;
      gap: 12px;
      box-shadow: 0 8px 30px rgba(0,0,0,0.65);
    }
    .avatar-circle {
      width: 44px;
      height: 44px;
      background: radial-gradient(circle, #e6b85c, #855316);
      border: 2px solid #f7d58b;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 20pt;
      box-shadow: 0 0 14px rgba(230, 184, 92, 0.6);
    }
    .profile-info h1 {
      font-size: 13pt;
      font-weight: 600;
      color: #ffd88a;
      margin: 0;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .level-tag {
      background: #7a2817;
      color: #ffe6cf;
      font-size: 9pt;
      padding: 2px 8px;
      border-radius: 10px;
      border: 1px solid #c95138;
    }
    .temple-location {
      font-size: 10pt;
      color: #dfcdbd;
      margin-top: 2px;
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .btn-toggle-view {
      background: linear-gradient(135deg, #a83d24, #732210);
      border: 1px solid #e86d54;
      color: #fff;
      font-family: Calibri, sans-serif;
      font-size: 9.5pt;
      font-weight: 600;
      padding: 3px 10px;
      border-radius: 12px;
      cursor: pointer;
      pointer-events: auto;
      transition: all 0.2s;
    }
    .btn-toggle-view:hover {
      background: #c2472b;
      box-shadow: 0 2px 10px rgba(194, 71, 43, 0.4);
    }
    .online-count {
      color: #72e28a;
      font-size: 9.5pt;
      display: flex;
      align-items: center;
      gap: 4px;
    }
    .online-dot {
      width: 7px;
      height: 7px;
      background: #44db63;
      border-radius: 50%;
      box-shadow: 0 0 8px #44db63;
    }

    /* TOP NOTIFICATION BANNER */
    .top-banner {
      position: absolute;
      top: 16px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(38, 18, 12, 0.9);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(220, 180, 110, 0.4);
      border-radius: 20px;
      padding: 7px 22px;
      font-size: 10pt;
      color: #ffeedb;
      z-index: 10;
      pointer-events: auto;
      display: flex;
      align-items: center;
      gap: 8px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }

    /* TOP RIGHT BUTTONS */
    .top-right-group {
      pointer-events: auto;
      display: flex;
      gap: 8px;
    }
    .btn-nav-top {
      background: rgba(43, 20, 13, 0.88);
      backdrop-filter: blur(10px);
      border: 1px solid rgba(220, 180, 110, 0.35);
      color: #f7e6d2;
      padding: 8px 14px;
      border-radius: 18px;
      font-family: Calibri, sans-serif;
      font-size: 10.5pt;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }
    .btn-nav-top:hover {
      background: #733c1a;
      border-color: #ffd88a;
      color: #fff;
    }

    /* RIGHT SIDEBAR: ĐÈN NGUYỆN */
    .prayer-lamp-sidebar {
      position: absolute;
      top: 76px;
      right: 18px;
      width: 315px;
      max-height: calc(100vh - 180px);
      background: rgba(36, 17, 10, 0.94);
      backdrop-filter: blur(16px);
      border: 1px solid rgba(230, 184, 92, 0.45);
      border-radius: 16px;
      z-index: 12;
      display: flex;
      flex-direction: column;
      box-shadow: -6px 8px 30px rgba(0,0,0,0.65);
      transition: transform 0.3s ease;
    }
    .prayer-header {
      padding: 12px 16px;
      border-bottom: 1px solid rgba(220, 180, 110, 0.25);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .prayer-title {
      font-size: 11.5pt;
      font-weight: 600;
      color: #ffd88a;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .prayer-tabs {
      display: flex;
      gap: 4px;
      background: rgba(20, 9, 5, 0.7);
      padding: 3px;
      border-radius: 12px;
      font-size: 9pt;
    }
    .prayer-tab {
      padding: 3px 9px;
      border-radius: 10px;
      color: #c4b3a3;
      cursor: pointer;
    }
    .prayer-tab.active {
      background: #943b22;
      color: #fff;
      font-weight: 600;
    }
    .prayer-list {
      flex: 1;
      overflow-y: auto;
      padding: 10px 14px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      max-height: 330px;
    }
    .prayer-card {
      background: rgba(56, 28, 17, 0.75);
      border: 1px solid rgba(200, 160, 100, 0.22);
      border-radius: 10px;
      padding: 10px 12px;
      transition: border-color 0.2s;
    }
    .prayer-card:hover {
      border-color: #f7d58b;
    }
    .prayer-text {
      font-size: 10pt;
      color: #ffeedb;
      margin-bottom: 6px;
      font-style: italic;
      line-height: 1.4;
    }
    .prayer-meta {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 8.5pt;
      color: #bda897;
    }
    .prayer-user {
      color: #f2cb73;
      font-weight: 600;
    }
    .prayer-bottom-action {
      padding: 12px 16px;
      border-top: 1px solid rgba(220, 180, 110, 0.25);
      background: rgba(26, 12, 7, 0.95);
      border-radius: 0 0 16px 16px;
    }
    .btn-release-lamp {
      width: 100%;
      background: linear-gradient(135deg, #d4982f, #945f13);
      border: 1px solid #ffd88a;
      color: #1a0c04;
      font-family: Calibri, sans-serif;
      font-size: 11.5pt;
      font-weight: 600;
      padding: 10px;
      border-radius: 12px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      box-shadow: 0 4px 18px rgba(212, 152, 47, 0.45);
      transition: all 0.2s;
    }
    .btn-release-lamp:hover {
      background: #e6a735;
      transform: translateY(-1px);
    }

    /* BOTTOM RIGHT RITUAL TOOLBAR */
    .ritual-toolbar {
      position: absolute;
      bottom: 20px;
      right: 20px;
      z-index: 12;
      display: flex;
      gap: 10px;
    }
    .ritual-btn {
      background: rgba(45, 21, 13, 0.92);
      backdrop-filter: blur(14px);
      border: 1px solid rgba(230, 184, 92, 0.4);
      border-radius: 16px;
      color: #fcefdc;
      padding: 9px 13px;
      font-family: Calibri, sans-serif;
      font-size: 10.5pt;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 3px;
      min-width: 68px;
      box-shadow: 0 6px 22px rgba(0,0,0,0.5);
      transition: all 0.2s cubic-bezier(0.2, 0.8, 0.2, 1);
    }
    .ritual-btn .r-icon {
      font-size: 17pt;
    }
    .ritual-btn:hover {
      background: #7a3a18;
      border-color: #ffd88a;
      transform: translateY(-2px);
      color: #fff;
    }
    .ritual-btn.highlight {
      background: linear-gradient(135deg, #a63820, #731e0f);
      border-color: #f07b65;
    }
    .ritual-btn.highlight:hover {
      background: #c24327;
      box-shadow: 0 4px 18px rgba(194, 67, 39, 0.5);
    }

    /* BOTTOM LEFT MENU BAR */
    .bottom-menu {
      position: absolute;
      bottom: 20px;
      left: 20px;
      z-index: 12;
      background: rgba(36, 17, 10, 0.88);
      backdrop-filter: blur(14px);
      border: 1px solid rgba(220, 180, 110, 0.3);
      border-radius: 18px;
      padding: 6px 12px;
      display: flex;
      gap: 12px;
    }
    .menu-item {
      color: #d1c1b2;
      font-size: 9.5pt;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 5px;
      padding: 6px 8px;
      border-radius: 8px;
      transition: all 0.2s;
    }
    .menu-item:hover {
      color: #ffd88a;
      background: rgba(255,255,255,0.08);
    }

    /* MODAL SYSTEM */
    .modal-overlay {
      position: absolute;
      inset: 0;
      background: rgba(0,0,0,0.75);
      backdrop-filter: blur(10px);
      z-index: 40;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 20px;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.25s ease;
    }
    .modal-overlay.open {
      opacity: 1;
      pointer-events: auto;
    }
    .modal-box {
      background: #26130b;
      border: 1px solid #d4a755;
      border-radius: 18px;
      width: 100%;
      max-width: 480px;
      padding: 24px;
      box-shadow: 0 20px 50px rgba(0,0,0,0.85);
      position: relative;
    }
    .modal-title {
      font-size: 15pt;
      font-weight: 600;
      color: #f7d58b;
      margin-bottom: 6px;
      text-align: center;
    }
    .modal-desc {
      font-size: 10.5pt;
      color: #c9bbae;
      margin-bottom: 18px;
      text-align: center;
    }
    .form-group {
      margin-bottom: 14px;
    }
    .form-group label {
      display: block;
      font-size: 10pt;
      font-weight: 600;
      color: #dfcfbd;
      margin-bottom: 4px;
    }
    .form-group input, .form-group textarea, .form-group select {
      width: 100%;
      background: #170b06;
      border: 1px solid #5c3b24;
      border-radius: 8px;
      padding: 9px 12px;
      color: #fff;
      font-family: Calibri, sans-serif;
      font-size: 11pt;
    }
    .form-group input:focus, .form-group textarea:focus, .form-group select:focus {
      outline: none;
      border-color: #d4a755;
    }
    .btn-submit {
      width: 100%;
      background: linear-gradient(135deg, #c78f2d, #8f5f14);
      border: 1px solid #f2ca77;
      color: #1a0f05;
      font-family: Calibri, sans-serif;
      font-size: 12pt;
      font-weight: 600;
      padding: 11px;
      border-radius: 10px;
      cursor: pointer;
      margin-top: 10px;
      transition: all 0.2s;
    }
    .btn-submit:hover {
      background: #d89e35;
      box-shadow: 0 4px 15px rgba(216, 158, 53, 0.4);
    }

    /* TOAST */
    .toast-msg {
      position: absolute;
      top: 90px;
      left: 50%;
      transform: translateX(-50%) translateY(-20px);
      background: rgba(43, 20, 13, 0.95);
      border: 1px solid #ffd88a;
      color: #fff2e0;
      padding: 10px 24px;
      border-radius: 25px;
      font-size: 11pt;
      font-weight: 600;
      box-shadow: 0 8px 30px rgba(0,0,0,0.6);
      z-index: 50;
      opacity: 0;
      pointer-events: none;
      transition: all 0.3s ease;
    }
    .toast-msg.show {
      transform: translateX(-50%) translateY(0);
      opacity: 1;
    }
  </style>
</head>
<body>

  <!-- 3D Canvas -->
  <div id="canvas-container">
    <canvas id="three-canvas"></canvas>
  </div>

  <!-- 3D Nametags Overlay -->
  <div id="nametags-container"></div>

  <!-- Header -->
  <header>
    <div class="user-profile-badge">
      <div class="avatar-circle">☸</div>
      <div class="profile-info">
        <h1>
          <span>Tự Phong Hiếu Hạnh</span>
          <span class="level-tag">Đồng Tu · Cấp 4</span>
        </h1>
        <div class="temple-location">
          <span>🏛 Chùa Vĩnh Tràng</span>
          <button class="btn-toggle-view" id="btn-toggle-view">🌳 Ra sân ngắm cảnh</button>
          <div class="online-count">
            <span class="online-dot"></span>
            <span>28 đang online</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Top Center Banner -->
    <div class="top-banner">
      <span>✨ Hai bên Chánh Điện là 18 vị Thập Bát La Hán gỗ mít thếp vàng cưỡi linh thú. Nhấp vào tượng để chiêm bái!</span>
    </div>

    <!-- Top Right Group -->
    <div class="top-right-group">
      <button class="btn-nav-top" id="btn-audio-toggle">🔔 Chuông Mõ: Bật</button>
      <button class="btn-nav-top" id="btn-open-so" style="background:#8f2d19; border-color:#e6644e;">📜 Sớ Cầu An</button>
    </div>
  </header>

  <!-- Right Sidebar: Đèn Nguyện -->
  <aside class="prayer-lamp-sidebar" id="prayer-sidebar">
    <div class="prayer-header">
      <div class="prayer-title">
        <span>🏮 Đèn Nguyện</span>
        <span style="font-size:9.5pt; color:#c7b3a0; font-weight:normal;">(32 ngọn đèn)</span>
      </div>
      <div class="prayer-tabs">
        <span class="prayer-tab active">Chùa này</span>
        <span class="prayer-tab">Tất cả</span>
      </div>
    </div>

    <div class="prayer-list" id="prayer-list">
      <div class="prayer-card">
        <div class="prayer-text">"Nguyện cho Gia đình luôn luôn bình An, cha mẹ sống đời với con cháu."</div>
        <div class="prayer-meta">
          <span class="prayer-user">Quý Lĩnh Như Trầm</span>
          <span>5 phút trước · 8 kính bái</span>
        </div>
      </div>
      <div class="prayer-card">
        <div class="prayer-text">"Nguyện cầu công việc thuận lợi, tai qua nạn khỏi, lòng được thanh tịnh an yên."</div>
        <div class="prayer-meta">
          <span class="prayer-user">Ngưng Ái Kim</span>
          <span>12 phút trước · 14 kính bái</span>
        </div>
      </div>
      <div class="prayer-card">
        <div class="prayer-text">"Chúc bách gia trăm họ vạn sự an khang, tai ương tiêu trừ, phúc thọ tăng long."</div>
        <div class="prayer-meta">
          <span class="prayer-user">Nhãn Vạn Linh</span>
          <span>35 phút trước · 21 kính bái</span>
        </div>
      </div>
      <div class="prayer-card">
        <div class="prayer-text">"Cầu xin Đức Phật chứng minh cho tâm thành hướng thiện, sớm trả hết nợ đời."</div>
        <div class="prayer-meta">
          <span class="prayer-user">Thích Từ Quang</span>
          <span>47 phút trước · 30 kính bái</span>
        </div>
      </div>
    </div>

    <div class="prayer-bottom-action">
      <button class="btn-release-lamp" id="btn-release-lamp">
        <span>🏮</span>
        <span>Thả Đèn Nguyện Cầu An</span>
      </button>
    </div>
  </aside>

  <!-- Bottom Left Menu -->
  <div class="bottom-menu">
    <div class="menu-item" onclick="showToast('Nhiệm vụ: Lạy Phật 3 lạy & chiêm bái các vị La Hán để tích lũy công đức!')">📋 Nhiệm vụ</div>
    <div class="menu-item" onclick="openModal('shop-modal')">🎁 Cửa hàng</div>
    <div class="menu-item" onclick="showToast('Đạo tràng Vĩnh Tràng: 28 đồng tu đang cùng niệm Phật.')">👥 Đạo tràng</div>
    <div class="menu-item" onclick="openModal('so-modal')">📜 Tấm Sớ</div>
  </div>

  <!-- Bottom Right Ritual Toolbar -->
  <div class="ritual-toolbar">
    <button class="ritual-btn" id="btn-bow">
      <span class="r-icon">🙏</span>
      <span>Lạy Phật</span>
    </button>
    <button class="ritual-btn" id="btn-beads">
      <span class="r-icon">📿</span>
      <span>Tràng Hạt</span>
    </button>
    <button class="ritual-btn" id="btn-chant">
      <span class="r-icon">📖</span>
      <span>Tụng Kinh</span>
    </button>
    <button class="ritual-btn" id="btn-meditate">
      <span class="r-icon">🧘</span>
      <span>Thiền Định</span>
    </button>
    <button class="ritual-btn" id="btn-offering">
      <span class="r-icon">🌸</span>
      <span>Dâng Lễ</span>
    </button>
    <button class="ritual-btn highlight" id="btn-open-shop">
      <span class="r-icon">🏮</span>
      <span>Thỉnh Pháp Bảo</span>
    </button>
  </div>

  <!-- Toast Message -->
  <div class="toast-msg" id="toast">Thành tâm kính Phật</div>

  <!-- Modal: Thả Đèn Nguyện Cầu An -->
  <div class="modal-overlay" id="lamp-modal">
    <div class="modal-box">
      <div class="modal-title">🏮 Thả Đèn Nguyện Cầu An</div>
      <div class="modal-desc">Đèn Dược Sư bản mệnh tượng trưng cho ánh sáng trí tuệ xua tan u tối, cầu bình an cho gia đạo và người thân tại Chùa Vĩnh Tràng.</div>

      <div class="form-group">
        <label>Tên người được cầu an</label>
        <input type="text" id="lamp-user-name" placeholder="Ví dụ: Cầu an cho Mẹ: Trần Thị Mai (Năm sinh 1958)">
      </div>
      <div class="form-group">
        <label>Lời khấn nguyện thành tâm</label>
        <textarea id="lamp-prayer-text" rows="3" placeholder="Nguyện cầu chư Phật mười phương gia hộ cho cha mẹ thân tâm an lạc, tai qua nạn khỏi..."></textarea>
      </div>
      <div class="form-group">
        <label>Thời gian thắp sáng ngọn đèn trên Chánh Điện</label>
        <select id="lamp-duration">
          <option value="7">Thắp sáng 7 ngày (Gieo duyên tùy tâm 20.000 đ)</option>
          <option value="49">Thắp sáng 49 ngày (Gieo duyên cúng dường 50.000 đ)</option>
          <option value="100">Thắp sáng trọn năm (Cầu an niên biểu 100.000 đ)</option>
        </select>
      </div>

      <button class="btn-submit" id="btn-confirm-lamp">Dâng Đèn Lên Bàn Tam Bảo</button>
      <button style="width:100%; background:transparent; border:none; color:#a39281; margin-top:10px; cursor:pointer;" onclick="closeModal('lamp-modal')">Đóng</button>
    </div>
  </div>

  <!-- Modal: Chiêm Bái Tôn Giả La Hán / Bồ Tát -->
  <div class="modal-overlay" id="arhat-modal">
    <div class="modal-box" style="max-width:500px;">
      <div class="modal-title" id="arhat-modal-title">🙏 Chiêm Bái Tôn Giả</div>
      <div style="text-align:center; margin:10px 0;">
        <span id="arhat-modal-mount" style="background:#5e2416; color:#ffe3c2; padding:3px 12px; border-radius:12px; font-size:10pt; border:1px solid #c48858;"></span>
      </div>
      <div class="modal-desc" id="arhat-modal-desc" style="text-align:justify; line-height:1.6; background:rgba(40,18,10,0.6); padding:12px; border-radius:10px; border:1px solid rgba(212,167,85,0.3);">
      </div>
      <div style="display:flex; gap:10px; margin-top:16px;">
        <button class="btn-submit" id="btn-arhat-lamp" style="margin-top:0; flex:1; background:linear-gradient(135deg, #a63820, #731e0f);">🏮 Dâng Đèn (20k)</button>
        <button class="btn-submit" id="btn-arhat-statue" style="margin-top:0; flex:1;">🎁 Thỉnh Tượng Gỗ (220k)</button>
      </div>
      <button style="width:100%; background:transparent; border:none; color:#a39281; margin-top:12px; cursor:pointer;" onclick="closeModal('arhat-modal')">Thoát</button>
    </div>
  </div>

  <!-- Modal: Cửa Hàng Thỉnh Pháp Bảo Thật Ship Tận Nhà -->
  <div class="modal-overlay" id="shop-modal">
    <div class="modal-box" style="max-width:520px;">
      <div class="modal-title">🎁 Thỉnh Pháp Bảo Chùa Vĩnh Tràng</div>
      <div class="modal-desc">Vật phẩm tâm linh đã được chú nguyện bình an tại Chùa Vĩnh Tràng, đóng gói cẩn thận giao tận tư gia toàn quốc.</div>

      <div style="max-height:360px; overflow-y:auto; display:flex; flex-direction:column; gap:12px; margin-bottom:14px;">
        <div style="background:rgba(54,28,17,0.7); border:1px solid #73482a; border-radius:10px; padding:12px; display:flex; gap:12px; align-items:center;">
          <div style="font-size:32pt;">📿</div>
          <div style="flex:1;">
            <div style="font-size:11.5pt; font-weight:600; color:#fed98e;">Vòng Tay Trầm Hương Tự Nhiên Vĩnh Tràng</div>
            <div style="font-size:9.5pt; color:#c7b3a0;">Gỗ trầm hương thơm dịu, trừ tà khí, an thần dưỡng khí.</div>
            <div style="font-size:11pt; color:#f0a85d; font-weight:600; margin-top:2px;">290.000 đ</div>
          </div>
          <button onclick="orderItem('Vòng Tay Trầm Hương', '290.000 đ')" style="background:#8f2d19; border:1px solid #f07b65; color:#fff; padding:6px 14px; border-radius:8px; cursor:pointer; font-weight:600;">Thỉnh</button>
        </div>

        <div style="background:rgba(54,28,17,0.7); border:1px solid #73482a; border-radius:10px; padding:12px; display:flex; gap:12px; align-items:center;">
          <div style="font-size:32pt;">🪷</div>
          <div style="flex:1;">
            <div style="font-size:11.5pt; font-weight:600; color:#fed98e;">Chuỗi Hạt Bồ Đề 108 Hạt Niệm Phật</div>
            <div style="font-size:9.5pt; color:#c7b3a0;">Chất gỗ Bồ Đề kim cang, bóng đẹp, thích hợp tu trì công phu.</div>
            <div style="font-size:11pt; color:#f0a85d; font-weight:600; margin-top:2px;">150.000 đ</div>
          </div>
          <button onclick="orderItem('Chuỗi Hạt Bồ Đề 108', '150.000 đ')" style="background:#8f2d19; border:1px solid #f07b65; color:#fff; padding:6px 14px; border-radius:8px; cursor:pointer; font-weight:600;">Thỉnh</button>
        </div>

        <div style="background:rgba(54,28,17,0.7); border:1px solid #73482a; border-radius:10px; padding:12px; display:flex; gap:12px; align-items:center;">
          <div style="font-size:32pt;">🏮</div>
          <div style="flex:1;">
            <div style="font-size:11.5pt; font-weight:600; color:#fed98e;">Đèn Sen Pha Lê Đổi Màu Dược Sư</div>
            <div style="font-size:9.5pt; color:#c7b3a0;">Đèn hoa sen sạc điện, ánh sáng ấm cúng thờ Tam Bảo tại tư gia.</div>
            <div style="font-size:11pt; color:#f0a85d; font-weight:600; margin-top:2px;">180.000 đ</div>
          </div>
          <button onclick="orderItem('Đèn Sen Pha Lê', '180.000 đ')" style="background:#8f2d19; border:1px solid #f07b65; color:#fff; padding:6px 14px; border-radius:8px; cursor:pointer; font-weight:600;">Thỉnh</button>
        </div>

        <div style="background:rgba(54,28,17,0.7); border:1px solid #73482a; border-radius:10px; padding:12px; display:flex; gap:12px; align-items:center;">
          <div style="font-size:32pt;">🪵</div>
          <div style="flex:1;">
            <div style="font-size:11.5pt; font-weight:600; color:#fed98e;">Tượng La Hán Hộ Mệnh Gỗ Bách Xanh</div>
            <div style="font-size:9.5pt; color:#c7b3a0;">Tạc thủ công theo diện tượng 18 La Hán Vĩnh Tràng, bỏ túi hộ thân.</div>
            <div style="font-size:11pt; color:#f0a85d; font-weight:600; margin-top:2px;">220.000 đ</div>
          </div>
          <button onclick="orderItem('Tượng La Hán Gỗ Bách Xanh', '220.000 đ')" style="background:#8f2d19; border:1px solid #f07b65; color:#fff; padding:6px 14px; border-radius:8px; cursor:pointer; font-weight:600;">Thỉnh</button>
        </div>
      </div>

      <button style="width:100%; background:transparent; border:none; color:#a39281; cursor:pointer;" onclick="closeModal('shop-modal')">Đóng Cửa Hàng</button>
    </div>
  </div>

  <!-- Modal: Đặt Hàng Thỉnh Vật Phẩm -->
  <div class="modal-overlay" id="order-modal">
    <div class="modal-box">
      <div class="modal-title" id="order-item-title">Thỉnh Pháp Bảo</div>
      <div class="modal-desc" id="order-item-desc">Vui lòng để lại địa chỉ để nhà chùa gửi chuyển phát tận nhà (Kiểm tra hàng rồi thanh toán COD).</div>

      <div class="form-group">
        <label>Họ và tên người nhận</label>
        <input type="text" id="order-name" placeholder="Nguyễn Văn A">
      </div>
      <div class="form-group">
        <label>Số điện thoại nhận hàng</label>
        <input type="tel" id="order-phone" placeholder="0908 123 456">
      </div>
      <div class="form-group">
        <label>Địa chỉ nhận bưu phẩm</label>
        <input type="text" id="order-address" placeholder="Số nhà, đường, phường/xã, quận/huyện, tỉnh/thành">
      </div>
      <div class="form-group">
        <label>Ghi chú cầu an (để in lên sớ kẹp theo kiện hàng)</label>
        <input type="text" id="order-note" placeholder="Cầu an cho gia đình mạnh khỏe">
      </div>

      <button class="btn-submit" id="btn-submit-order">Xác Nhận Đặt Thỉnh (Giao Tận Nơi)</button>
      <button style="width:100%; background:transparent; border:none; color:#a39281; margin-top:10px; cursor:pointer;" onclick="closeModal('order-modal')">Quay Lại</button>
    </div>
  </div>

  <!-- Modal: Sớ Cầu An Thư Pháp Mạ Vàng -->
  <div class="modal-overlay" id="so-modal">
    <div class="modal-box" style="max-width:540px; background:#47190f; border:2px solid #f0c36b; color:#ffe8cb;">
      <div style="border:1px dashed #d4a755; padding:20px; border-radius:12px; text-align:center;">
        <div style="font-size:10pt; letter-spacing:3px; color:#f0c36b;">TIỀN GIANG TỈNH · MỸ THO THÀNH PHỐ</div>
        <div style="font-size:18pt; font-weight:bold; color:#ffd88a; margin:8px 0 16px 0;">SẮC TỨ VĨNH TRÀNG CỔ TỰ CẦU AN SỚ</div>
        <div style="font-size:11pt; line-height:1.8; text-align:justify; margin-bottom:16px;">
          Phục dĩ: Nam mô Thập phương Thường trụ Tam Bảo tác đại chứng minh. Nay có đệ tử Phật môn hiệu là: <b id="so-user" style="color:#ffd88a;">Tự Phong Hiếu Hạnh</b>, phát tâm bồ đề, dâng hương hoa đăng trà quả, kính lễ Tam Bảo Chùa Vĩnh Tràng.<br><br>
          Cúi xin Đức Phật Từ Bi, Chư Tôn Bồ Tát, Thập Bát La Hán phóng ngọc hào quang gia trì: Thân tâm an lạc, tai tiêu nạn tán, tật bệnh tiêu trừ, sở cầu như ý, gia đạo hưng long, vạn niên phúc đức.
        </div>
        <div style="display:flex; justify-content:space-between; font-size:10pt; color:#deb785; margin-top:20px;">
          <div>Chứng Minh Sư: Hòa Thượng Viện Chủ</div>
          <div>Bính Ngọ Niên · Cát Nhật</div>
        </div>
      </div>
      <button class="btn-submit" style="margin-top:16px;" onclick="closeModal('so-modal'); showToast('🙏 Đã ghi nhận tấm sớ thành tâm của quý Phật tử!')">Lưu Giữ Phước Điền</button>
    </div>
  </div>

  <!-- Three.js Logic -->
  <script type="module">
    import * as THREE from 'three';
    import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

    // 1. AUDIO SYNTHESIZER (Bell & Wooden Fish)
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
      osc.frequency.setValueAtTime(320, audioCtx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(120, audioCtx.currentTime + 0.12);
      gain.gain.setValueAtTime(0.8, audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.14);
      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start();
      osc.stop(audioCtx.currentTime + 0.15);
    }

    document.getElementById('btn-audio-toggle').onclick = () => {
      isAudioOn = !isAudioOn;
      document.getElementById('btn-audio-toggle').textContent = isAudioOn ? '🔔 Chuông Mõ: Bật' : '🔕 Chuông Mõ: Tắt';
      if (isAudioOn) playBell();
    };

    // 2. THREE.JS SCENE SETUP
    const canvas = document.getElementById('three-canvas');
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x1a0a05);
    scene.fog = new THREE.FogExp2(0x190b07, 0.012);

    const camera = new THREE.PerspectiveCamera(46, window.innerWidth / window.innerHeight, 0.1, 150);
    const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, powerPreference: "high-performance" });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.35;
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.06;
    controls.maxPolarAngle = Math.PI / 2 - 0.02;
    controls.minDistance = 3;
    controls.maxDistance = 60;

    // Camera Views: Chánh Điện (Third-person view qua vai avatar) vs Sân tiền đường
    const views = {
      altar: { pos: new THREE.Vector3(0, 3.6, 16.5), target: new THREE.Vector3(0, 4.8, -14.0) },
      yard: { pos: new THREE.Vector3(0, 6.5, 33.0), target: new THREE.Vector3(0, 5.0, 4.0) }
    };

    let currentViewMode = 'altar';
    camera.position.copy(views.altar.pos);
    controls.target.copy(views.altar.target);
    controls.update();

    let isTransitioning = false;
    let transitionProgress = 0;
    const startPos = new THREE.Vector3(), startTarget = new THREE.Vector3();
    const endPos = new THREE.Vector3(), endTarget = new THREE.Vector3();

    function setView(mode) {
      currentViewMode = mode;
      isTransitioning = true;
      transitionProgress = 0;
      startPos.copy(camera.position);
      startTarget.copy(controls.target);
      endPos.copy(views[mode].pos);
      endTarget.copy(views[mode].target);

      document.getElementById('btn-toggle-view').textContent = mode === 'altar' ? '🌳 Ra sân ngắm cảnh' : '🏛 Vào Chánh Điện';
      document.getElementById('prayer-sidebar').style.display = mode === 'altar' ? 'flex' : 'none';
    }

    document.getElementById('btn-toggle-view').onclick = () => {
      setView(currentViewMode === 'altar' ? 'yard' : 'altar');
    };

    // 3. LIGHTING SYSTEM (WARM, RADIANT & EXPANSIVE)
    const ambient = new THREE.HemisphereLight(0xffecd1, 0x471d11, 2.2);
    scene.add(ambient);

    // Warm Altar Spotlights (chiếu rực rỡ tượng Phật Thích Ca dát vàng)
    const altarLight = new THREE.SpotLight(0xffc25c, 7.5, 50, Math.PI / 3, 0.45);
    altarLight.position.set(0, 11, -4);
    altarLight.target.position.set(0, 5.5, -16.5);
    altarLight.castShadow = true;
    scene.add(altarLight);
    scene.add(altarLight.target);

    // Điểm sáng chiếu hai hàng tượng Thập Bát La Hán ở hai bên vách
    const leftWallLight = new THREE.PointLight(0xffa142, 3.2, 35);
    leftWallLight.position.set(-10, 6.0, 0);
    scene.add(leftWallLight);

    const rightWallLight = new THREE.PointLight(0xffa142, 3.2, 35);
    rightWallLight.position.set(10, 6.0, 0);
    scene.add(rightWallLight);

    // 4. PROCEDURAL TEXTURES & MATERIALS
    function createTerracottaFloorTexture() {
      const cv = document.createElement('canvas');
      cv.width = 512;
      cv.height = 512;
      const ctx = cv.getContext('2d');
      const size = 128;
      for (let y = 0; y < 4; y++) {
        for (let x = 0; x < 4; x++) {
          const px = x * size;
          const py = y * size;
          // Mạch vữa sẫm
          ctx.fillStyle = '#220b06';
          ctx.fillRect(px, py, size, size);
          // Gờ gạch
          ctx.fillStyle = '#632014';
          ctx.fillRect(px + 3, py + 3, size - 6, size - 6);
          // Mặt gạch men nung chuyển sắc ấm
          const grad = ctx.createRadialGradient(px + size/2, py + size/2, 10, px + size/2, py + size/2, size/2);
          grad.addColorStop(0, '#943622');
          grad.addColorStop(0.65, '#732415');
          grad.addColorStop(1, '#52170d');
          ctx.fillStyle = grad;
          ctx.fillRect(px + 7, py + 7, size - 14, size - 14);
          // Viền chỉ trang nhã
          ctx.strokeStyle = '#b86637';
          ctx.lineWidth = 1;
          ctx.strokeRect(px + 9, py + 9, size - 18, size - 18);
        }
      }
      const tex = new THREE.CanvasTexture(cv);
      tex.wrapS = THREE.RepeatWrapping;
      tex.wrapT = THREE.RepeatWrapping;
      tex.repeat.set(16, 26);
      return tex;
    }

    const floorTexture = createTerracottaFloorTexture();
    const floorMat = new THREE.MeshStandardMaterial({
      map: floorTexture,
      roughness: 0.24,
      metalness: 0.12,
    });

    const mat = (c, r=0.7, m=0.0, e=0, ei=0) => new THREE.MeshStandardMaterial({
      color: c, roughness: r, metalness: m,
      emissive: e ? c : 0, emissiveIntensity: ei
    });

    const pillarMat = mat(0x57190e, 0.55, 0.08); // Lacquer red ironwood pillars
    const stoneMat = mat(0x6e655d, 0.85); // Grey stone column bases
    const goldMat = mat(0xdfab35, 0.3, 0.88); // Gilded dragon & ornaments
    const buddhaMat = mat(0xf7c83e, 0.22, 0.92); // Radiant 24K Golden Buddha
    const arhatMat = mat(0xdfab35, 0.32, 0.85); // Antique gilded wood 18 Arhats
    const beastMat = mat(0xb87930, 0.45, 0.65); // Sacred animals under Arhats
    const lotusMat = mat(0xe85a82, 0.5); // Pink lotus
    const woodDark = mat(0x2b1309, 0.75); // Dark mahogany rafters
    const matRug = mat(0x5e2015, 0.8); // Golden embroidered carpet mats
    const cushionMat = mat(0x733722, 0.75); // Brown bồ đoàn
    const haloMat = mat(0xffcc44, 0.1, 0, 1, 1.4); // Radiant Halo

    // 5. BUILD THE GRAND CHÁNH ĐIỆN (ĐẠI HÙNG BỬU ĐIỆN)
    const temple = new THREE.Group();
    scene.add(temple);

    function addBox(x, y, z, w, h, d, m, parent=temple) {
      const o = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), m);
      o.position.set(x, y, z);
      o.castShadow = true; o.receiveShadow = true;
      parent.add(o);
      return o;
    }

    function addCyl(x, y, z, r, h, m, parent=temple, r2=r) {
      const o = new THREE.Mesh(new THREE.CylinderGeometry(r2, r, h, 24), m);
      o.position.set(x, y, z);
      o.castShadow = true; o.receiveShadow = true;
      parent.add(o);
      return o;
    }

    function addBall(x, y, z, r, m, parent=temple) {
      const o = new THREE.Mesh(new THREE.SphereGeometry(r, 20, 16), m);
      o.position.set(x, y, z);
      o.castShadow = true; o.receiveShadow = true;
      parent.add(o);
      return o;
    }

    // GRAND HALL SHELL (Rộng 28m, Dài 46m, Cao 10m)
    // Sàn gạch đỏ bóng loáng
    addBox(0, 0, 0, 28, 0.2, 46, floorMat);
    // Tường hậu phía sau bàn thờ
    addBox(0, 5, -23, 28, 10, 0.8, pillarMat);
    // Tường 2 bên vách Chánh Điện
    addBox(-14, 5, 0, 0.8, 10, 46, pillarMat);
    addBox(14, 5, 0, 0.8, 10, 46, pillarMat);
    // Trần nhà xà gồ gỗ chạm lộng
    addBox(0, 10, 0, 28, 0.4, 46, woodDark);

    // HÀNG CỘT LIM ĐỎ SƠN THẾP VÀNG DỌC THEO LÒNG CHÁNH ĐIỆN (2 hàng cột 12 cây)
    const pillarZ = [-18, -10, -2, 6, 14, 20];
    pillarZ.forEach(pz => {
      [-8.5, 8.5].forEach(px => {
        // Chân tảng đá
        addBox(px, 0.35, pz, 1.4, 0.5, 1.4, stoneMat);
        // Thân cột tròn gỗ lim đỏ
        addCyl(px, 5.2, pz, 0.48, 9.4, pillarMat);
        // Đầu cột hoa văn thếp vàng
        addBox(px, 9.8, pz, 1.2, 0.4, 1.2, goldMat);
      });
    });

    // HAI CỘT RỒNG THẾP VÀNG NGAY CẬN BÀN TAM BẢO (ĐẶC TRƯNG CHÙA VĨNH TRÀNG)
    [-8.5, 8.5].forEach(px => {
      // Rồng vàng cuộn tròn quanh cột
      for (let y = 1.8; y <= 8.5; y += 1.4) {
        addCyl(px, y, -10, 0.58, 0.3, goldMat);
      }
      // Câu đối chữ Hán vàng ốp lòng máng
      addBox(px + (px > 0 ? -0.45 : 0.45), 5.2, -10, 0.12, 6.2, 0.55, goldMat);
    });

    // 3 ĐÈN CHÙM PHA LÊ KIỂU PHÁP BUÔNG TỪ TRẦN (castShadow = false)
    [-10, 0, 10].forEach(cz => {
      const chGroup = new THREE.Group();
      temple.add(chGroup);
      const c1 = addCyl(0, 9.2, cz, 0.03, 1.6, goldMat, chGroup);
      c1.castShadow = false;
      const c2 = addCyl(0, 8.2, cz, 1.2, 0.1, goldMat, chGroup);
      c2.castShadow = false;
      const c3 = addCyl(0, 7.8, cz, 0.8, 0.1, goldMat, chGroup);
      c3.castShadow = false;
      const c4 = addCyl(0, 7.4, cz, 0.4, 0.1, goldMat, chGroup);
      c4.castShadow = false;
      for (let a = 0; a < Math.PI * 2; a += Math.PI / 4) {
        const cx = Math.cos(a) * 1.1;
        const cy = Math.sin(a) * 1.1;
        const b = addBall(cx, 8.1, cz + cy, 0.08, mat(0xffeedd, 0.1, 0, 1, 3.0), chGroup);
        b.castShadow = false;
      }
      const clight = new THREE.PointLight(0xffb84d, 2.2, 18);
      clight.position.set(0, 7.6, cz);
      scene.add(clight);
    });

    // ĐÈN SPOTLIGHT CHIẾU TRỰC TIẾP TƯỢNG PHẬT THÍCH CA DÁT VÀNG
    const buddhaDirectLight = new THREE.SpotLight(0xffdf88, 10.0, 32, Math.PI / 4, 0.35);
    buddhaDirectLight.position.set(0, 9.5, -9.0);
    buddhaDirectLight.target.position.set(0, 7.4, -18.7);
    scene.add(buddhaDirectLight);
    scene.add(buddhaDirectLight.target);

    const buddhaGlow = new THREE.PointLight(0xffd866, 4.5, 14);
    buddhaGlow.position.set(0, 8.2, -16.5);
    scene.add(buddhaGlow);

    // HOÀNH PHI 「黃金寶殿」 (HOÀNG KIM BỬU ĐIỆN) & 「勅賜 永長寺」 TREO CAO
    addBox(0, 9.0, -13, 8.8, 1.4, 0.25, goldMat);
    addBox(0, 9.0, -12.85, 8.2, 1.0, 0.1, pillarMat);

    // BÀN THỜ TAM BẢO ĐỒ SỘ (3 CẤP SƠN SON THẾP VÀNG)
    const altarZ = -16.5;
    addBox(0, 1.2, altarZ, 14.0, 2.2, 5.0, woodDark);
    addBox(0, 2.35, altarZ, 14.2, 0.15, 5.2, goldMat);
    // Cấp 2
    addBox(0, 3.0, altarZ - 1.2, 11.0, 1.6, 3.2, woodDark);
    addBox(0, 3.85, altarZ - 1.2, 11.2, 0.12, 3.4, goldMat);
    // Cấp 3: Tòa sen Phật
    addBox(0, 4.5, altarZ - 2.2, 8.0, 1.4, 2.4, goldMat);

    // ĐẠI TƯỢNG PHẬT THÍCH CA / A DI ĐÀ DÁT VÀNG TỌA TRÊN ĐÀI SEN KHỔNG LỒ
    const bZ = altarZ - 2.2;
    // Đài sen nở rộ 2 tầng
    addCyl(0, 5.5, bZ, 2.2, 0.8, goldMat);
    addCyl(0, 6.1, bZ, 1.8, 0.6, lotusMat);
    // Thân Phật ngồi kiết già trang nghiêm
    const buddhaBody = addBall(0, 7.4, bZ, 1.4, buddhaMat);
    buddhaBody.scale.set(1.3, 1.4, 0.9);
    // Đầu Phật & Nhục kế
    addBall(0, 9.1, bZ, 0.65, buddhaMat);
    addBall(0, 9.8, bZ, 0.22, buddhaMat);

    // HÀO QUANG NGŨ SẮC TOẢ SÁNG PHÍA SAU PHẬT (Radiant Aureole)
    const haloGroup = new THREE.Group();
    haloGroup.position.set(0, 8.8, bZ - 0.4);
    temple.add(haloGroup);

    const haloRing1 = addCyl(0, 0, 0, 2.6, 0.05, mat(0xffffff, 0.1, 0, 1, 2.5), haloGroup);
    haloRing1.rotation.x = Math.PI / 2;
    const haloRing2 = addCyl(0, 0, -0.04, 3.3, 0.04, mat(0xfbbf24, 0.1, 0, 1, 2.2), haloGroup);
    haloRing2.rotation.x = Math.PI / 2;
    const haloRing3 = addCyl(0, 0, -0.08, 4.0, 0.04, mat(0x06b6d4, 0.1, 0, 1, 2.0), haloGroup);
    haloRing3.rotation.x = Math.PI / 2;
    const haloRing4 = addCyl(0, 0, -0.12, 4.8, 0.03, mat(0xef4444, 0.1, 0, 1, 1.8), haloGroup);
    haloRing4.rotation.x = Math.PI / 2;

    // HAI VỊ THỊ GIẢ A NAN - CA DIẾP HAI BÊN
    [-4.5, 4.5].forEach((ax) => {
      addCyl(ax, 3.8, altarZ - 1.2, 0.8, 0.6, goldMat);
      addCyl(ax, 5.2, altarZ - 1.2, 0.45, 2.2, goldMat);
      addBall(ax, 6.6, altarZ - 1.2, 0.35, goldMat);
    });

    // BẢNG VÀNG CÔNG ĐỨC & PHÁP NGỮ PHẬT DẠY HAI BÊN
    addBox(-7.5, 4.5, altarZ + 0.5, 2.4, 4.0, 0.2, goldMat);
    addBox(-7.5, 4.5, altarZ + 0.62, 2.1, 3.7, pillarMat);
    addBox(7.5, 4.5, altarZ + 0.5, 2.4, 4.0, 0.2, goldMat);
    addBox(7.5, 4.5, altarZ + 0.62, 2.1, 3.7, pillarMat);

    // NGHI TRƯỢNG THỜ TỰ TRÊN BÀN LỄ
    addCyl(0, 2.8, altarZ + 1.8, 0.6, 0.7, mat(0x5a462f, 0.45, 0.85));
    for (let h = -0.12; h <= 0.12; h += 0.12) {
      addCyl(h, 3.7, altarZ + 1.8, 0.02, 1.2, mat(0xba2525, 0.7));
      addBall(h, 4.35, altarZ + 1.8, 0.04, mat(0xffaa33, 0.1, 0, 1, 4.0));
    }

    // Đôi Đèn Dược Sư tỏa sáng vàng ấm
    [-4.8, 4.8].forEach(dx => {
      addCyl(dx, 3.2, altarZ + 1.5, 0.25, 1.4, goldMat);
      addBall(dx, 4.1, altarZ + 1.5, 0.35, lotusMat);
      addBall(dx, 4.25, altarZ + 1.5, 0.12, mat(0xffa834, 0.1, 0, 1, 6.0));
    });

    // Cặp Lộc Bình men hoa lam cắm sen
    addCyl(-2.4, 2.8, altarZ + 1.6, 0.25, 0.7, mat(0x5a462f, 0.5, 0.8));
    addBall(-2.4, 3.4, altarZ + 1.6, 0.35, lotusMat);
    addCyl(2.4, 2.8, altarZ + 1.6, 0.25, 0.7, mat(0x5a462f, 0.5, 0.8));
    addBall(2.4, 3.4, altarZ + 1.6, 0.35, lotusMat);

    // =========================================================================
    // 6. HAI DÃY TƯỢNG THẬP BÁT LA HÁN & ĐẠI KHÁM THỜ BỒ TÁT DỌC 2 BÊN VÁCH
    // =========================================================================
    const interactiveObjects = [];

    // Danh sách 18 vị Thập Bát La Hán Chùa Vĩnh Tràng
    const arhatsLeft = [
      { id: 1, name: "Tọa Lộc La Hán (Tân Đầu Lô Tôn Giả)", mount: "Cưỡi Hươu Linh", desc: "Ngài Tân-đầu-lô ngự trên lưng hươu tiên, biểu trưng cho sự thanh cao, an nhiên tự tại và trường thọ." },
      { id: 2, name: "Hoan Hỷ La Hán (Ca Nặc Ca Phạt Tha)", mount: "Tọa Sen Vàng", desc: "Tôn giả mang tâm hoan hỷ bất biến, đem niềm vui an lạc và nụ cười từ bi gieo rắc khắp muôn nơi." },
      { id: 3, name: "Cử Bát La Hán (Ca Nặc Ca Bạt Ly Đọa)", mount: "Nâng Bát Vàng", desc: "Tôn giả giơ cao bình bát khất thực giáo hóa chúng sinh, trừ bỏ tham lam xan xỉ, huân tu đức nhẫn nhục." },
      { id: 4, name: "Thác Tháp La Hán (Tô Tần Đà Tôn Giả)", mount: "Cầm Tháp Bảo", desc: "Tay nâng bảo tháp Phật xá lợi, biểu thị cho chính pháp trường tồn, hào quang trí tuệ chiếu sáng mười phương." },
      { id: 5, name: "Tĩnh Tọa La Hán (Nặc Cự La Tôn Giả)", mount: "Tọa Phiến Thạch", desc: "Thiền định bất động như núi cao, giúp tâm phật tử lắng đọng mọi tạp niệm, tiêu trừ lo âu phiền muộn." },
      { id: 6, name: "Quá Giang La Hán (Bạt Đà La Tôn Giả)", mount: "Cưỡi Cá Kình", desc: "Vượt qua biển sinh tử luân hồi, tiếp độ chúng sinh qua bến bờ giác ngộ an vui." },
      { id: 7, name: "Kỵ Tượng La Hán (Ca Lý Ca Tôn Giả)", mount: "Cưỡi Voi Trắng", desc: "Ngự trên thớt voi trắng dũng mãnh kiên nhẫn, tượng trưng cho hạnh nguyện đại bi không lay chuyển." },
      { id: 8, name: "Tiếu Sư La Hán (Phạt Xà La Phất Đa)", mount: "Cưỡi Sư Tử Vàng", desc: "Dũng lực như chúa sơn lâm sư tử hống, xua tan mọi tà ma ám chướng và sợ hãi trong tâm." },
      { id: 9, name: "Khai Tâm La Hán (Tuất Bác Ca Tôn Giả)", mount: "Vạch Ngực Thấy Phật", desc: "Vạch tâm can hiện rõ Phật tính, dạy rằng Phật tại tâm mỗi người, chỉ cần sống từ bi và lương thiện." }
    ];

    const arhatsRight = [
      { id: 10, name: "Thám Thủ La Hán (Bán Thác Ca Tôn Giả)", mount: "Vươn Tay Thư Thái", desc: "Sau giờ thiền định vươn tay thư thái, thức tỉnh bản tánh thanh tịnh, thấu suốt vạn pháp duyên sinh." },
      { id: 11, name: "Trầm Tư La Hán (La Hầu La Tôn Giả)", mount: "Tọa Đài Trầm Mặc", desc: "Con của Đức Phật Thích Ca, mật hạnh đệ nhất, nêu gương khiêm cung, nhẫn nại và tinh tấn." },
      { id: 12, name: "Trầm Tĩnh La Hán (Na Già Tư Na Tôn Giả)", mount: "Thủ Ấn Tĩnh Tâm", desc: "Tâm thức sáng trong như trăng rằm, hóa giải mọi tranh chấp thị phi, mang lại hòa khí cho gia đạo." },
      { id: 13, name: "Phục Hổ La Hán (Phục Hổ Tôn Giả)", mount: "Cưỡi Bạch Hổ", desc: "Hàng phục chúa sơn lâm cọp dữ bằng lòng từ bi vô lượng, chế ngự tâm sân hận nóng giận của con người." },
      { id: 14, name: "Hàng Long La Hán (Hàng Long Tôn Giả)", mount: "Cưỡi Kim Long", desc: "Thu phục rồng thiêng bảo hộ kinh điển, biểu thị đại trí đại dũng, ban phúc tài lộc hanh thông." },
      { id: 15, name: "Bố Đại La Hán (Nhân Yết Đà Tôn Giả)", mount: "Mang Túi Vải Càn Khôn", desc: "Túi vải thu nạp mọi muộn phiền nhân gian và ban phát muôn điều may mắn, no đủ, hoan hỷ." },
      { id: 16, name: "Ba Tiêu La Hán (Phạt Na Bà Tư Tôn Giả)", mount: "Tọa Gốc Ba Tiêu", desc: "Ngồi dưới gốc chuối thanh tịnh quán sát vô thường, dứt trừ phiền não ái dục thế gian." },
      { id: 17, name: "Trường Mi La Hán (A Thị Đa Tôn Giả)", mount: "Lông Mày Dài Trắng", desc: "Lông mày rủ dài biểu thị phúc tướng diên thọ, ban lời chúc trường thọ khang ninh cho cha mẹ bách lão." },
      { id: 18, name: "Khán Môn La Hán (Chú Đồ Bán Thác Ca)", mount: "Cầm Tích Trượng", desc: "Tay rung trượng đồng thức tỉnh nhân tâm, giữ gìn cửa đạo chánh pháp thanh tịnh." }
    ];

    // Kệ thờ gỗ sơn son thếp vàng chạy dọc vách Tả & Hữu
    addBox(-13.0, 0.7, 0, 1.6, 1.4, 34, woodDark);
    addBox(-13.0, 1.45, 0, 1.7, 0.1, 34.2, goldMat);

    addBox(13.0, 0.7, 0, 1.6, 1.4, 34, woodDark);
    addBox(13.0, 1.45, 0, 1.7, 0.1, 34.2, goldMat);

    // Hàm dựng một pho tượng La Hán cưỡi thú linh
    function createArhatStatue(x, z, data, isLeft) {
      const g = new THREE.Group();
      g.position.set(x, 1.5, z);
      g.rotation.y = isLeft ? Math.PI / 2 : -Math.PI / 2;
      temple.add(g);

      // Bệ sen con
      addCyl(0, 0.15, 0, 0.55, 0.25, goldMat, g);
      // Linh thú bên dưới
      addBox(0, 0.45, 0, 0.75, 0.4, 0.45, beastMat, g);
      addBall(0.35, 0.65, 0, 0.22, beastMat, g);

      // Tượng Tôn Giả La Hán bằng gỗ mít thếp vàng
      addCyl(0, 0.95, 0, 0.32, 0.75, arhatMat, g);
      addBall(0, 1.45, 0, 0.2, arhatMat, g);
      // Vòng hào quang nhỏ sau đầu
      const aHalo = addCyl(0, 1.45, -0.1, 0.28, 0.02, mat(0xffd88a, 0.2, 0, 1, 1.2), g);
      aHalo.rotation.x = Math.PI / 2;

      // Đèn hoa sen phát sáng ấm áp
      addBall(0, 0.32, 0.4, 0.1, lotusMat, g);
      addBall(0, 0.42, 0.4, 0.04, mat(0xffa834, 0.1, 0, 1, 5.0), g);

      // Điểm sáng nhẹ cho mỗi cụm tượng
      const pt = new THREE.PointLight(0xffa834, 0.8, 4);
      pt.position.set(0, 0.6, 0.4);
      g.add(pt);

      // Gắn dữ liệu tương tác
      g.userData = {
        isArhat: true,
        data: data,
        worldPos: new THREE.Vector3(x, 2.5, z)
      };
      interactiveObjects.push(g);
      return g;
    }

    // Đặt 9 vị La Hán bên vách Tả (X = -12.8)
    arhatsLeft.forEach((arh, idx) => {
      const zPos = -15.0 + idx * 3.4;
      createArhatStatue(-12.8, zPos, arh, true);
    });

    // Đặt 9 vị La Hán bên vách Hữu (X = +12.8)
    arhatsRight.forEach((arh, idx) => {
      const zPos = -15.0 + idx * 3.4;
      createArhatStatue(12.8, zPos, arh, false);
    });

    // HAI ĐẠI KHÁM THỜ BỒ TÁT Ở GIỮA HAI VÁCH (Z = 0)
    // 1. Vách Tả: Bồ Tát Quán Thế Âm Chuẩn Đề (X = -13.2, Z = 0)
    const quanAmGroup = new THREE.Group();
    quanAmGroup.position.set(-13.1, 0, 0);
    quanAmGroup.rotation.y = Math.PI / 2;
    temple.add(quanAmGroup);

    addBox(0, 3.2, -0.4, 3.2, 6.4, 0.6, goldMat, quanAmGroup);
    addBox(0, 3.2, -0.2, 2.8, 5.8, 0.4, pillarMat, quanAmGroup);
    addCyl(0, 1.8, 0, 1.1, 0.6, lotusMat, quanAmGroup);
    addCyl(0, 2.8, 0, 0.45, 1.4, buddhaMat, quanAmGroup);
    addBall(0, 3.7, 0, 0.32, buddhaMat, quanAmGroup);
    const qaHalo = addCyl(0, 3.7, -0.15, 1.2, 0.04, mat(0x5eead4, 0.2, 0, 1, 1.6), quanAmGroup);
    qaHalo.rotation.x = Math.PI / 2;
    [-1.0, 1.0].forEach(lx => {
      addCyl(lx, 1.6, 0.4, 0.15, 0.8, goldMat, quanAmGroup);
      addBall(lx, 2.1, 0.4, 0.2, lotusMat, quanAmGroup);
    });
    quanAmGroup.userData = {
      isArhat: true,
      data: {
        name: "Đại Bi Quán Thế Âm Bồ Tát (Chuẩn Đề)",
        mount: "Tòa Sen Thất Bảo",
        desc: "Đức Mẹ từ bi tầm thanh cứu khổ, lắng nghe tiếng kêu than của muôn loài, ban sự an lành, chở che tai ương và hộ trì phụ nữ, trẻ nhỏ."
      },
      worldPos: new THREE.Vector3(-12.0, 4.0, 0)
    };
    interactiveObjects.push(quanAmGroup);

    // 2. Vách Hữu: Bồ Tát Địa Tạng Vương (X = +13.2, Z = 0)
    const diaTangGroup = new THREE.Group();
    diaTangGroup.position.set(13.1, 0, 0);
    diaTangGroup.rotation.y = -Math.PI / 2;
    temple.add(diaTangGroup);

    addBox(0, 3.2, -0.4, 3.2, 6.4, 0.6, goldMat, diaTangGroup);
    addBox(0, 3.2, -0.2, 2.8, 5.8, 0.4, pillarMat, diaTangGroup);
    addCyl(0, 1.8, 0, 1.1, 0.6, lotusMat, diaTangGroup);
    addCyl(0, 2.8, 0, 0.45, 1.4, buddhaMat, diaTangGroup);
    addBall(0, 3.7, 0, 0.32, buddhaMat, diaTangGroup);
    addCyl(0.4, 3.2, 0.2, 0.03, 2.2, goldMat, diaTangGroup);
    const dtHalo = addCyl(0, 3.7, -0.15, 1.2, 0.04, mat(0xf59e0b, 0.2, 0, 1, 1.6), diaTangGroup);
    dtHalo.rotation.x = Math.PI / 2;
    [-1.0, 1.0].forEach(lx => {
      addCyl(lx, 1.6, 0.4, 0.15, 0.8, goldMat, diaTangGroup);
      addBall(lx, 2.1, 0.4, 0.2, lotusMat, diaTangGroup);
    });
    diaTangGroup.userData = {
      isArhat: true,
      data: {
        name: "Đại Nguyện Địa Tạng Vương Bồ Tát",
        mount: "Đế Thính Linh Thú",
        desc: "Đại nguyện 'Địa ngục vị không, thệ bất thành Phật', cứu vớt cửu huyền thất tổ, siêu độ tiên linh quá vãng, phù hộ gia quyến bình an, phúc lộc trường cửu."
      },
      worldPos: new THREE.Vector3(12.0, 4.0, 0)
    };
    interactiveObjects.push(diaTangGroup);

    // 3. TƯỢNG HỘ PHÁP VI ĐÀ & TIÊU DIỆN ĐẠI SĨ TẠI TIỀN ĐIỆN (Z = 16.5m)
    [-9.5, 9.5].forEach((hx, idx) => {
      const hp = new THREE.Group();
      hp.position.set(hx, 0, 16.5);
      hp.rotation.y = idx === 0 ? Math.PI / 3 : -Math.PI / 3;
      temple.add(hp);
      addBox(0, 1.0, 0, 1.8, 2.0, 1.8, woodDark, hp);
      addCyl(0, 2.8, 0, 0.5, 1.8, idx === 0 ? goldMat : mat(0x942b1a, 0.4, 0.6), hp);
      addBall(0, 4.0, 0, 0.35, goldMat, hp);
      addCyl(0.4, 3.2, 0.2, 0.04, 2.4, goldMat, hp);

      hp.userData = {
        isArhat: true,
        data: idx === 0 ? {
          name: "Vi Đà Tôn Thiên Bồ Tát (Hộ Pháp)",
          mount: "Kim Cang Giáp Trụ",
          desc: "Bảo hộ đạo tràng thanh tịnh, ủng hộ Phật pháp trường tồn, bảo vệ người thiện lương khỏi tai ương chướng ngại."
        } : {
          name: "Tiêu Diện Đại Sĩ (Diện Nhiên Quỷ Vương)",
          mount: "Lưỡi Lửa Tam Muội",
          desc: "Hóa thân từ bi của Bồ Tát Quán Thế Âm để giáo hóa u hồn tà quỷ, trừ sạch ác niệm, mang lại sự bình yên tuyệt đối cho đạo tràng."
        },
        worldPos: new THREE.Vector3(hx, 4.5, 16.5)
      };
      interactiveObjects.push(hp);
    });

    // =========================================================================
    // 7. MÂM BỒ ĐOÀN & AVATAR ĐỒNG TU PHẬT TỬ (LƯỚI 4 CỘT x 5 HÀNG)
    // =========================================================================
    const avatars = [];
    const avatarDataList = [
      { name: "Thích Từ Quang", level: 20, col: -5.2, row: 0 },
      { name: "Diệu Tâm", level: 8, col: -1.8, row: 0 },
      { name: "Viên Thông", level: 12, col: 1.8, row: 0 },
      { name: "Thiện Duyên", level: 6, col: 5.2, row: 0 },

      { name: "Quý Lĩnh Như Trầm", level: 5, col: -5.2, row: 1 },
      { name: "Hải Đăng", level: 9, col: -1.8, row: 1 },
      { name: "Quảng Đức", level: 15, col: 1.8, row: 1 },
      { name: "Tâm An", level: 4, col: 5.2, row: 1 },

      { name: "An Nhiên", level: 7, col: -5.2, row: 2 },
      { name: "Minh Triết", level: 11, col: -1.8, row: 2 },
      { name: "Ngọc Liên", level: 5, col: 1.8, row: 2 },
      { name: "Bảo Trân", level: 8, col: 5.2, row: 2 },

      { name: "Tuệ Mẫn", level: 14, col: -5.2, row: 3 },
      { name: "Điền Lực Thạch", level: 3, col: -1.8, row: 3 },
      { name: "Giang Nghi Hạ", level: 14, col: 1.8, row: 3 },
      { name: "Phúc Lộc", level: 6, col: 5.2, row: 3 },

      { name: "Nhãn Vạn Linh", level: 8, col: -5.2, row: 4 },
      // CHÍNH NGƯỜI DÙNG Ở ĐÂY: col: -1.8, row: 4
      { name: "Hinh Tài Hiên Bình", level: 5, col: 1.8, row: 4 },
      { name: "Kim Cương", level: 10, col: 5.2, row: 4 }
    ];

    const nametagsContainer = document.getElementById('nametags-container');

    avatarDataList.forEach(item => {
      const zPos = -6.0 + item.row * 4.2;
      const xPos = item.col;

      addBox(xPos, 0.12, zPos, 1.8, 0.04, 1.8, matRug);
      addBox(xPos, 0.15, zPos, 1.7, 0.02, 1.7, goldMat);
      addCyl(xPos, 0.26, zPos, 0.65, 0.22, cushionMat);

      const pGroup = new THREE.Group();
      pGroup.position.set(xPos, 0.38, zPos);
      temple.add(pGroup);

      const robeColors = [0x543826, 0x8a552b, 0x3d4e61, 0x6e4e37];
      const rColor = robeColors[Math.floor(Math.random() * robeColors.length)];

      addCyl(0, 0.65, 0, 0.4, 1.05, mat(rColor, 0.8), pGroup);
      addBall(0, 1.45, 0, 0.3, mat(0xd9a882, 0.8), pGroup);
      const pHalo = addCyl(0, 1.45, -0.12, 0.52, 0.03, mat(0xffd88a, 0.2, 0, 1, 1.2), pGroup);
      pHalo.rotation.x = Math.PI / 2;

      const tagDiv = document.createElement('div');
      tagDiv.className = 'nametag';
      tagDiv.innerHTML = `
        <div class="nametag-badge">
          <span>${item.name}</span>
          <span class="nametag-level">Cấp ${item.level}</span>
        </div>
      `;
      nametagsContainer.appendChild(tagDiv);

      avatars.push({
        group: pGroup,
        tagEl: tagDiv,
        worldHeadPos: new THREE.Vector3(xPos, 2.3, zPos),
        origY: 0.38,
        seed: Math.random() * 10
      });
    });

    // VỊ TRÍ CỦA CHÍNH NGƯỜI DÙNG: "Tự Phong Hiếu Hạnh" (Cấp 4) - Đặt ở Z = 9.2 để camera nhìn thấy trọn vẹn
    const userZ = 9.2;
    const userX = -1.5;
    addBox(userX, 0.12, userZ, 1.8, 0.04, 1.8, matRug);
    addBox(userX, 0.15, userZ, 1.7, 0.02, 1.7, goldMat);
    addCyl(userX, 0.26, userZ, 0.65, 0.22, cushionMat);

    const userGroup = new THREE.Group();
    userGroup.position.set(userX, 0.38, userZ);
    temple.add(userGroup);

    addCyl(0, 0.7, 0, 0.42, 1.1, mat(0x38557a, 0.8), userGroup);
    addBox(0, 0.7, 0.2, 0.15, 1.0, 0.3, goldMat, userGroup);
    addBall(0, 1.5, 0, 0.32, mat(0xd49f7b, 0.8), userGroup);
    const uHalo = addCyl(0, 1.5, -0.15, 0.6, 0.04, mat(0xffcc44, 0.1, 0, 1, 1.8), userGroup);
    uHalo.rotation.x = Math.PI / 2;

    const userTagDiv = document.createElement('div');
    userTagDiv.className = 'nametag is-user';
    userTagDiv.innerHTML = `
      <div class="nametag-pointer"></div>
      <div class="nametag-badge">
        <span>Tự Phong Hiếu Hạnh</span>
        <span class="nametag-level" style="background:#b83a1b;">Cấp 4</span>
      </div>
    `;
    nametagsContainer.appendChild(userTagDiv);

    avatars.push({
      group: userGroup,
      tagEl: userTagDiv,
      worldHeadPos: new THREE.Vector3(userX, 2.45, userZ),
      origY: 0.38,
      seed: 0
    });

    // Dynamic Smoke Particles in Altar
    const particleCount = 85;
    const pGeo = new THREE.BufferGeometry();
    const pPos = new Float32Array(particleCount * 3);
    for (let i = 0; i < particleCount; i++) {
      pPos[i*3] = (Math.random() - 0.5) * 0.3;
      pPos[i*3+1] = 3.6 + Math.random() * 4.0;
      pPos[i*3+2] = altarZ + 1.8 + (Math.random() - 0.5) * 0.3;
    }
    pGeo.setAttribute('position', new THREE.BufferAttribute(pPos, 3));
    const smokeParticles = new THREE.Points(pGeo, new THREE.PointsMaterial({
      color: 0xe0d2c3,
      size: 0.18,
      transparent: true,
      opacity: 0.55
    }));
    scene.add(smokeParticles);

    // =========================================================================
    // 8. TƯƠNG TÁC CLICK CHIÊM BÁI TƯỢNG LA HÁN & BỒ TÁT (RAYCASTER)
    // =========================================================================
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();

    window.addEventListener('click', (e) => {
      if (e.target.closest('header, aside, .ritual-toolbar, .bottom-menu, .modal-overlay, .nametag')) return;

      mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
      mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
      raycaster.setFromCamera(mouse, camera);

      const intersects = raycaster.intersectObjects(temple.children, true);
      if (intersects.length > 0) {
        let hit = intersects[0].object;
        let root = null;
        while (hit && hit !== temple) {
          if (hit.userData && hit.userData.isArhat) {
            root = hit;
            break;
          }
          hit = hit.parent;
        }

        if (root && root.userData && root.userData.data) {
          const d = root.userData.data;
          playBell();
          document.getElementById('arhat-modal-title').textContent = `🙏 ${d.name}`;
          document.getElementById('arhat-modal-mount').textContent = d.mount;
          document.getElementById('arhat-modal-desc').innerHTML = `
            <p style="margin-bottom:8px;">${d.desc}</p>
            <p style="color:#f7d58b; font-size:9.5pt; font-style:italic;">* Một trong 18 vị Thập Bát La Hán gỗ mít thếp vàng độc nhất vô nhị chế tác năm 1907 tại Chùa Vĩnh Tràng.</p>
          `;
          document.getElementById('btn-arhat-lamp').onclick = () => {
            closeModal('arhat-modal');
            openModal('lamp-modal');
            document.getElementById('lamp-prayer-text').value = `Con thành tâm đảnh lễ trước ${d.name}, cầu xin ngài gia hộ bình an, thân tâm thanh tịnh...`;
          };
          document.getElementById('btn-arhat-statue').onclick = () => {
            closeModal('arhat-modal');
            orderItem(`Tượng ${d.name} Gỗ Bách Xanh`, '220.000 đ');
          };
          openModal('arhat-modal');
        }
      }
    });

    // 9. TOAST & RITUALS
    let toastTimer;
    function showToast(msg) {
      const t = document.getElementById('toast');
      t.textContent = msg;
      t.classList.add('show');
      clearTimeout(toastTimer);
      toastTimer = setTimeout(() => t.classList.remove('show'), 2800);
    }
    window.showToast = showToast;

    // Lạy Phật (Bow 3 times with bell and camera nod)
    document.getElementById('btn-bow').onclick = () => {
      playBell();
      showToast('🙏 Một lòng đảnh lễ Tam Bảo: Nam Mô Bổn Sư Thích Ca Mâu Ni Phật');
      let count = 0;
      const interval = setInterval(() => {
        playMokugyo();
        count++;
        camera.position.y -= 0.35;
        setTimeout(() => camera.position.y += 0.35, 450);
        if (count >= 3) clearInterval(interval);
      }, 1000);
    };

    // Tràng Hạt 108 biến
    let beadCount = 0;
    document.getElementById('btn-beads').onclick = () => {
      playMokugyo();
      beadCount++;
      if (beadCount >= 108) {
        playBell();
        showToast('🌟 Công đức viên mãn! Bạn đã hoàn thành 1 tràng hạt 108 biến niệm Phật.');
        beadCount = 0;
      } else {
        showToast(`📿 Niệm Phật câu thứ ${beadCount}/108: Nam Mô A Di Đà Phật`);
      }
    };

    // Tụng Kinh
    document.getElementById('btn-chant').onclick = () => {
      playBell();
      showToast('📖 Đang mở kinh nhật tụng: Chú Đại Bi & Bát Nhã Ba La Mật Đa Tâm Kinh...');
      let beats = 0;
      const chInterval = setInterval(() => {
        playMokugyo();
        beats++;
        if (beats >= 8) clearInterval(chInterval);
      }, 700);
    };

    // Thiền Định
    document.getElementById('btn-meditate').onclick = () => {
      playBell();
      showToast('🧘 Bắt đầu thời khóa thiền định quán niệm hơi thở. Hít vào tâm tĩnh lặng, thở ra miệng mỉm cười.');
    };

    // Dâng Lễ
    document.getElementById('btn-offering').onclick = () => {
      playBell();
      showToast('🌸 Kính dâng hoa sen thơm và đăng trà quả phẩm thanh tịnh lên mười phương chư Phật.');
    };

    // MODAL HANDLERS
    window.openModal = function(id) {
      document.getElementById(id).classList.add('open');
    };
    window.closeModal = function(id) {
      document.getElementById(id).classList.remove('open');
    };

    document.getElementById('btn-release-lamp').onclick = () => openModal('lamp-modal');
    document.getElementById('btn-open-shop').onclick = () => openModal('shop-modal');
    document.getElementById('btn-open-so').onclick = () => openModal('so-modal');

    // Thả Đèn Nguyện Cầu An
    document.getElementById('btn-confirm-lamp').onclick = () => {
      const name = document.getElementById('lamp-user-name').value.trim() || 'Phật tử ẩn danh';
      const text = document.getElementById('lamp-prayer-text').value.trim() || 'Nguyện cầu gia đạo an khang thịnh vượng, vạn sự hanh thông';

      playBell();
      closeModal('lamp-modal');

      const list = document.getElementById('prayer-list');
      const card = document.createElement('div');
      card.className = 'prayer-card';
      card.style.borderColor = '#ffd88a';
      card.innerHTML = `
        <div class="prayer-text">"${text}"</div>
        <div class="prayer-meta">
          <span class="prayer-user">✨ ${name}</span>
          <span>Vừa thắp · 1 kính bái</span>
        </div>
      `;
      list.prepend(card);

      showToast(`🏮 Ngọn đèn cầu an của ${name} đã được thắp sáng trên Chánh Điện!`);
    };

    // Đặt Hàng Pháp Bảo
    window.orderItem = function(name, price) {
      closeModal('shop-modal');
      closeModal('arhat-modal');
      document.getElementById('order-item-title').textContent = `Thỉnh: ${name}`;
      document.getElementById('order-item-desc').textContent = `Giá gieo duyên: ${price} · Đóng gói cẩn thận, chuyển phát COD tận nhà.`;
      openModal('order-modal');
    };

    document.getElementById('btn-submit-order').onclick = () => {
      const name = document.getElementById('order-name').value.trim();
      const phone = document.getElementById('order-phone').value.trim();
      const addr = document.getElementById('order-address').value.trim();
      if (!name || !phone || !addr) {
        alert('Vui lòng điền đủ Họ tên, Số điện thoại và Địa chỉ nhận hàng.');
        return;
      }
      playBell();
      closeModal('order-modal');
      showToast('🎉 Đã ghi nhận đơn thỉnh pháp bảo! Nhà chùa sẽ liên hệ sớm nhất.');
      document.getElementById('so-user').textContent = name;
      setTimeout(() => openModal('so-modal'), 1200);
    };

    // 10. ANIMATION LOOP & 3D NAMETAGS PROJECTION
    window.addEventListener('resize', () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    });

    let clock = new THREE.Clock();
    const tempVec = new THREE.Vector3();

    function animate() {
      requestAnimationFrame(animate);
      const time = clock.getElapsedTime();

      // Smooth camera transition between altar and yard
      if (isTransitioning) {
        transitionProgress += 0.035;
        if (transitionProgress >= 1) {
          transitionProgress = 1;
          isTransitioning = false;
        }
        const t = transitionProgress < 0.5 ? 2 * transitionProgress * transitionProgress : -1 + (4 - 2 * transitionProgress) * transitionProgress;
        camera.position.lerpVectors(startPos, endPos, t);
        controls.target.lerpVectors(startTarget, endTarget, t);
      }
      controls.update();

      // Rotate radiant halo slightly
      haloRing1.rotation.z = time * 0.15;
      haloRing2.rotation.z = -time * 0.12;
      haloRing3.rotation.z = time * 0.08;\n      haloRing4.rotation.z = -time * 0.05;

      // Gentle breathing animation for meditating avatars
      avatars.forEach(av => {
        av.group.position.y = av.origY + Math.sin(time * 2.0 + av.seed) * 0.025;

        // Cập nhật vị trí thẻ tên trên màn hình
        if (currentViewMode === 'altar') {
          tempVec.copy(av.worldHeadPos);
          tempVec.project(camera);
          if (tempVec.z < 1) {
            const x = (tempVec.x * 0.5 + 0.5) * window.innerWidth;
            const y = (-(tempVec.y * 0.5) + 0.5) * window.innerHeight;
            av.tagEl.style.transform = `translate(-50%, -100%) translate(${x}px, ${y}px)`;
            av.tagEl.style.opacity = '1';
          } else {
            av.tagEl.style.opacity = '0';
          }
        } else {
          av.tagEl.style.opacity = '0';
        }
      });

      // Rising incense smoke
      const pos = smokeParticles.geometry.attributes.position.array;
      for (let i = 0; i < particleCount; i++) {
        pos[i*3 + 1] += 0.009;
        if (pos[i*3 + 1] > 7.5) {
          pos[i*3 + 1] = 3.6;
        }
      }
      smokeParticles.geometry.attributes.position.needsUpdate = true;

      renderer.render(scene, camera);
    }
    animate();
  </script>
</body>
</html>
"""

output_path = "/Users/macos/Desktop/Chùa online/Mô hình 3D Vĩnh Tràng/trai-nghiem-chua-vinh-trang-3d.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_code)

print(f"Đã ghi thành công file: {output_path} ({len(html_code)} bytes)")
