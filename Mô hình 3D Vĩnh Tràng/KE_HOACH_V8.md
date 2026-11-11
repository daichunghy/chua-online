# KẾ HOẠCH V8 — TIỆM CẬN ẢNH THAM CHIẾU MỚI (THAM_CHIEU_V8.md)

**Điểm xuất phát:** bản V7.3d — `trai-nghiem-vinh-trang-v7.html` 17.243.005 byte,
đã lên GitHub commit 20d9b11. Sao lưu tại `trai-nghiem-vinh-trang-v7-V73d-backup.html`.
**Chuẩn giữ nguyên (không được tụt):** hành trình 9/9, verify tự nhiên P0–P18 =
48 PASS / 0 FAIL, 0 exception JS, 0 console error, release `grep __v6ff` = 0,
ảnh chốt 1000×2000 thật. Luật tượng + luật nhân vật (3 GLB chuẩn) + danh sách
cấm trang nghiêm giữ tuyệt đối.

**Bằng chứng hiện trạng:** `v73_shots/` (10 ảnh 1000×2000 của V7.3d) +
`v8_shots/before/` (spawn / mặt tiền / sân+lư / cận sư / giảng đường / trong
điện + `measure.json` đo góc quay theo tick + `chars.json` vị trí thế giới) —
chụp bằng `shots_v8.mjs` qua driver `run_v8_driver.sh` (cổng load < 2,0 ×2).

---

## BẢNG CHÊNH LỆCH ĐO ĐƯỢC THEO 5 TRỤC

### Trục 1 — Cảnh / điện
| # | Mẫu | Hiện trạng (đo/đọc từ code + ảnh) | Cách làm trong giới hạn web | Tiêu chí đạt |
|---|---|---|---|---|
| 1.1 | Phông sau có **núi mờ + sương sớm**, trời sáng sớm | Sau chánh điện là hàng cây + trời cobalt phẳng; không có lớp phông xa (module_2 chỉ có cây ngoài rào bán kính ~62 m) | Thêm dãy núi mờ 4–5 khối nón/dãy thấp ở z ≈ −95…−120, màu xanh sương `0x8FB4D9` để FogExp2 (0,0028) tự làm mờ; không collider | Ảnh mặt tiền/spawn thấy dãy núi mờ sau điện; không che tháp/điện |
| 1.2 | Điện nhiều lớp **vàng + lam** (trang trí lam rõ) | Điện vàng + cột đỏ + phù điêu đỏ/xanh lá điểm xuyết; **không có dải lam nào trên điện** (lam chỉ ở mosaic cổng) | Thêm dải panel mosaic cobalt `#2C4A8A` (mã palette cổng) chạy trên băng kem + ô lam xen giữa hàng phù điêu — **KHÔNG đổi màu mái**: mái giữ đỏ nâu `#7C4030` theo ảnh thật Vĩnh Tràng + palette đã khóa (ghi rõ trong báo cáo — đây là điểm chủ động không theo mẫu vì mẫu là mockup, chùa thật mái đỏ nâu) | Ảnh mặt tiền thấy dải lam rõ; biển vẫn đọc trọn; mái giữ nguyên màu |
| 1.3 | **Cây hoa hồng/đào** bên hồ | Hoa giấy dạng bụi tròn rải rác; không có cây hoa thân cao cạnh hồ | Thêm 2 cây hoa đào: thân + 3–4 tán cầu phủ hoa hồng `#EE7FAE`/`#F2A0C4` ở (−2, 24) và (34, 27) cạnh hai hồ | Ảnh sân/hồ thấy cây hoa hồng rõ |
| 1.4 | Ánh sáng **buổi sáng** mềm | Sun từ phía tây (−30, 25, 18) — nắng chiều; grade tổng đã "Sáng trong" | Giữ nguyên hướng nắng (đổi hướng sẽ phá toàn bộ cân bằng mặt tiền đã nghiệm thu ở V7.3 + fill nam) — chỉ tăng nhẹ sương sớm: fog 0,0028 → 0,0032 và mây sớm sáng hơn. Ghi rõ đánh đổi trong báo cáo | Không tụt ảnh mặt tiền; phông xa mềm hơn |

### Trục 2 — Đi đứng
| # | Mẫu | Hiện trạng (đo bằng state dump, `v8_shots/before/measure.json`) | Cách làm | Tiêu chí đạt |
|---|---|---|---|---|
| 2.1 | NPC rẽ hướng mượt | NPC **snap góc tức thì**: `g.rotation.y = Math.atan2(dx, dz)` mỗi tick (module_7 `stepNPC`) — snap theo cấu trúc code (Δyaw tùy ý trong 1 tick). Lượt đo số before KHÔNG lấy được mẫu (render 1000×2000 quá chậm — xem v8_progress.md) nên mốc before = chính dòng code này | Rẽ giảm chấn như người chơi: lerp góc theo `dt * 4` kèm wrap ±π | Đo after: worst bước rẽ NPC ≤ 0,35 rad/tick (mẫu 2-tick ≤ 0,7); NPC vẫn tới waypoint và dừng vái đúng (verify NPC PASS giữ nguyên) |
| 2.2 | Người chơi chuyển động có gia tốc mềm | Người chơi đi/dừng **tức thì** theo input (step = speed × dt trực tiếp — bằng chứng code); rẽ đã lerp `dt*10` | Thêm hệ số hòa tốc `moveBlend` (tăng ~5/s khi có input, giảm ~7/s khi thả) nhân vào bước đi + nhịp bước chân | Kiểm chứng: verify hành trình 9/9 + auto-walk tới đích giữ nguyên (blend có sàn 0,35 nên không kẹt); đối chiếu code before/after |
| 2.3 | Chuyển tư thế không giật | Đã có fadeIn/fadeOut 0,22 s ở `applyCharPose` (module_5) | Giữ nguyên — không đụng | — |

### Trục 3 — Cách chơi
| # | Mẫu | Hiện trạng | Cách làm | Tiêu chí đạt |
|---|---|---|---|---|
| 3.1 | Có cảm giác "đang được dẫn đi làm một việc" | Bấm nút động từ → auto-walk + vệt sáng đã có; nhưng **không có dòng mục tiêu** cho biết đang đi đâu/vì sao cho tới khi tới nơi (chỉ có lời An khi tới trạm) | Thêm dòng mục tiêu nhỏ dưới nút động từ: khi auto-walk chạy hiện "Đang tới: <tên trạm>", tới nơi/cancel thì ẩn. **Không** điểm/EXP — chỉ là chỉ đường (đúng vai trò breadcrumb của bản chốt V5) | Ảnh chụp giữa đường thấy dòng mục tiêu; verify journey 9/9 giữ nguyên |
| 3.2 | Nhịp 60 giây đầu | Đã đúng bản chốt V5 (spawn ngoài cổng, ≤3 nút, An chào) — V7.3 verify P0 PASS | Giữ nguyên; chỉ rà lại bằng lượt verify tự nhiên | P0–P2 PASS như V7.3 |

### Trục 4 — Học viện / Giảng đường
| # | Mẫu | Hiện trạng (đo từ code) | Cách làm | Tiêu chí đạt |
|---|---|---|---|---|
| 4.1 | Giảng đường là một nơi tử tế trong cảnh | Nhà giảng đường chỉ là hộp + biển; **không đèn đá/bonsai/bảng tin** phía trước; monk đứng gần đó nhưng khung cảnh trống | Thêm trước giảng đường: 2 tháp đèn đá + cặp bonsai (dùng lại `makeStoneLantern72`/`makeBonsai72`) + bảng gỗ "LỊCH GIẢNG · HUỆ ĐĂNG" | Ảnh giảng đường thấy đủ bộ; không chặn tuyến monk (route (44,−16)… giữ nguyên khoảng hở) |
| 4.2 | Nội dung học | 4 lộ trình, 24 bài nhưng **chỉ 1 bài (A0) có nội dung**, 23 bài "sắp mở"; modal Phòng kinh sách không nối sang bài giảng | (a) Viết thêm **1 bài đầy đủ D3 "Các tượng lớn trong khuôn viên chùa"** — nội dung CHỈ lắp từ INFO_CARDS đã có nguồn trong module_6b (A Di Đà 18 m/2008, Di Lặc 2010 ~20 m, Niết Bàn ~32 m/2013, tháp 2015/35 m) + tổng quát hoá `openSampleLesson` thành bảng LESSON_CONTENT {A0, D3}, quiz 3 câu từ đúng các dữ kiện đó; (b) modal Phòng kinh sách thêm nút mở thẳng Bài giảng | Bài D3 mở được từ danh sách (nút "Vào học"), quiz chấm đúng/sai chạy, hoàn thành lưu `lessonsDone['D3']`; verify P17 (giảng đường có quiz) PASS giữ nguyên |
| 4.3 | Bản đồ đúng vị trí | Bản đồ tĩnh vẫn chấm **Kinh sách ở (33,−12)** — vị trí cũ đã bỏ từ V7.3c (nay (42,−10,5)) | Sửa chấm bản đồ → (42, −10,5) | Mở bản đồ thấy chấm đúng cạnh Giảng đường |

### Trục 5 — Trang phục + đồ lễ
| # | Mẫu | Hiện trạng (đo từ GLB + code) | Cách làm | Tiêu chí đạt |
|---|---|---|---|---|
| 5.1 | Sư **áo tràng XÁM + dải vai CAM** vắt chéo | Sư đang nhuộm **nâu vàng** (138,86,34)/(96,58,22) bởi `recolorMonkRobe`; không có dải vai. Đo GLB nam: cụm áo = 60.519/71.464 đỉnh, ngực (35% trên của áo) 17.095 đỉnh — đủ mật độ nhuộm dải chéo theo tọa độ bind-pose (mặt = +Z, đã đo: tâm da đầu Z = +0,074) | (a) `recolorMonkRobe` → tông xám (138,138,142)/(96,96,100) × tone; (b) trong cùng lượt nhuộm: đỉnh áo ở mặt trước (Z > 0,04), Y ∈ [0,02; 0,80] và nằm trong dải chéo từ vai (Y 0,78; X −0,20) xuống hông (Y 0,05; X +0,25), bề rộng 0,15 → nhuộm cam (240,130,32)/(214,104,22). Nhuộm theo đỉnh nên dải đi theo MỌI action, không gắn xương, không đổi mesh | Ảnh cận sư: áo xám + dải cam chéo rõ qua ngực; `__v7chars` sư vẫn ready, pose đúng; luật nhân vật giữ (vẫn GLB nam chuẩn) |
| 5.2 | **Người quỳ trên bồ đoàn hai bên lư sân** | Sân **không có bồ đoàn, không có người quỳ** — chỉ NPC đứng vái ở (23,14) | Thêm 4 bồ đoàn (đĩa trụ r 0,55 h 0,18, đỏ sẫm viền vàng) hai bên lư tại (21,2; 14,8), (24,8; 14,8) có người quỳ + (19,8; 15,2), (26,2; 15,2) trống; 2 avatar `kneel` (1 nữ, 1 nam) quay mặt về lư; thêm 1 bồ đoàn + 1 khách quỳ trước Di Lặc (−24; 4,2). Collider nhỏ r 0,45 cho bồ đoàn có người | Ảnh sân+lư thấy người quỳ trên bồ đoàn hai bên lư; trạm lư (điểm đứng 25,3; 13,7, r 5,2) và tuyến verify không bị chặn (P_lư PASS giữ nguyên) |
| 5.3 | Đồ thờ trong điện đầy đặn | Bàn Tam Bảo đã có lư đồng + đèn sen + lộc bình; nhưng **6 khách quỳ trong điện ngồi thẳng trên sàn** (không bồ đoàn — grep module_3: không có cushion nào) | Thêm 6 bồ đoàn dưới đúng 6 vị khách quỳ (tọa độ local temple (−4,5/0/4,5; −4 và 2), đĩa r 0,55 h 0,18) | Ảnh trong điện thấy khách quỳ trên bồ đoàn |
| 5.4 | Khói lư sân **bay rõ** như mẫu | Khói đã đúng spec đã khóa (120 sprite, opacity đỉnh 0,36, rise 0,25–0,40, life 6–10 s — module_4) nhưng sprite nhỏ (size tối đa 1,28) nên ở cỡ ảnh sân khó thấy | Trong spec: size 0,08+k·1,2 → 0,10+k·1,5; opacity đỉnh 0,36 → 0,38 (trần spec) | Ảnh sân (lư đã thắp) thấy cột khói rõ; thông số vẫn trong spec khói đã khóa |
| 5.5 | Hai hàng đèn đá dọc sân | Đèn đá mới 4 cái dọc đường + 2 bên thềm | Thêm 4 tháp đèn đá (2 cặp tại z = 30 và z = 9,5, x = 19,6/26,4) → thành 2 hàng dọc lối chính | Ảnh spawn/mặt tiền thấy 2 hàng đèn đá |

### Lỗi phụ phát hiện khi đo — ĐÃ KHẲNG ĐỊNH BẰNG SỐ (before, 2026-11-11)
- **Khách quỳ trong điện lệch thế giới — ĐÚNG LÀ LỖI THẬT:** `charsWorld`
  trong `v8_shots/before/chars.json`: 6 khách quỳ (chars 16–21) ở thế giới
  (595,5–604,5 ; 596–602) thay vì (295,5–304,5 ; 296–302) — module_5 ghi
  position (300+x, 300+z) cho group vốn là con của `temple` (+300,+300)
  → **trong điện không hề có người quỳ ở bản V7.3d** (đúng họ lỗi V6 đã sửa
  cho đèn nội điện; verify 48 PASS không bắt được vì `__v7chars` chỉ báo
  tọa độ local). **Đã sửa ở B1:** position → (x, 0.32, z), khớp đúng 6 bồ
  đoàn mới thêm ở module_3. Tiêu chí nghiệm thu: charsWorld after của 6
  khách quỳ ∈ (295..305, 296..302) + ảnh trong điện thấy người quỳ trên
  bồ đoàn.

---

## THỨ TỰ THI CÔNG (mỗi mục xong → ghi checkpoint vào v8_progress.md)
- **B1 — Trục 5:** 5.1 áo sư + dải cam (module_5) → 5.2 bồ đoàn sân + khách
  quỳ (module_2 + module_5) → 5.3 bồ đoàn điện (module_3) → 5.5 đèn đá
  (module_2) → 5.4 khói (module_4). Dựng lại + soi nhanh ảnh sân/sư.
- **B2 — Trục 1:** 1.1 núi mờ → 1.2 dải lam điện → 1.3 cây hoa đào → 1.4 sương.
- **B3 — Trục 2:** 2.1 rẽ NPC giảm chấn → 2.2 hòa tốc người chơi (module_7/6a).
- **B4 — Trục 4:** 4.1 trang trí giảng đường → 4.3 chấm bản đồ → 4.2 bài D3 +
  nối modal kinh sách (v3.js + module_6b).
- **B5 — Trục 3:** 3.1 dòng mục tiêu (head_css + module_6b/7).
- **C — Kiểm chứng:** assemble (release grep `__v6ff` = 0) → driver chạy
  verify_v73_run + tailA + tailB → shots_v8 after + measure after → soi từng
  ảnh cạnh THAM_CHIEU_V8.md → BAO_CAO_V8.md verdict từng trục.

## RỦI RO / GIỚI HẠN KHAI THẬT TRƯỚC
- Mái xanh lam của mẫu: **không làm theo** — mâu thuẫn ảnh thật + palette khóa;
  tiệm cận bằng dải lam mosaic (1.2). Nêu rõ trong BAO_CAO_V8.
- Nhuộm dải chéo theo đỉnh phụ thuộc mật độ đỉnh vùng ngực (đã đo 17.095 đỉnh
  cho 35% trên của áo — đủ mịn); mép dải là mép đỉnh, không phải đường cắt
  mesh — chấp nhận ở cỡ ảnh web.
- Bài giảng: chỉ thêm được bài lắp từ dữ kiện đã có nguồn trong repo (D3);
  22 bài còn lại vẫn "sắp mở" — không bịa nội dung giáo lý.
