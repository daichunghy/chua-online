# BÁO CÁO V8 — TIỆM CẬN ẢNH THAM CHIẾU MỚI (THAM_CHIEU_V8.md)

**Bản dựng:** `trai-nghiem-vinh-trang-v7.html` — **17.260.812 byte** (V7.3d: 17.243.005).
Release `grep __v6ff` = 0 (đã kiểm). Kế hoạch: `KE_HOACH_V8.md`.
**Chuẩn giữ:** hành trình 9/9 · 0 lỗi JS · không tụt PASS so với V7.3
(48 PASS / 0 FAIL tự nhiên + tailA P12 4/4 + P13 3/3 + tailB 13 PASS + books 2/2).

## KẾT QUẢ KIỂM CHỨNG TỰ ĐỘNG
- **Lượt tự nhiên (natural run)** trên bản tiền-sửa-engine (17.257.925):
  **50 PASS / 0 FAIL tới hết P19** (vượt mốc nền V7.3 là P0–P18 = 48
  PASS; log `v8_verify_run.log`) — bị reboot VM cắt ở tiền đề P20.
  Hành trình 9/9 trong lượt này.
- **tailA trên bản có sửa engine (17.260.119): FULL PASS** — P12 4/4
  (gồm tới Niết Bàn + lặng + vái), P13 3/3, cổng 0 lỗi JS (log
  `v8f_tailA.log`). Hai sửa engine không làm tụt tuyến P12.
- **tailB trên bản sửa tư thế quỳ (17.260.549): verdicts 21/21 PASS,
  exceptions 0, console errors 0, cổng JS PASS** (log `v8f_tailB.log`)
  — chi tiết ở mục Lỗi thứ ba. Không tụt PASS nào so với nền V7.3
  (nền: P14–P18 13 PASS + books 2/2 + kẹp cột 4/4; bản này gộp cả cụm
  P20 vào cùng 21 verdict và đạt tất cả).
- **Bản cuối 17.260.812** chỉ khác bản đã chạy tailB ở MỘT thay đổi:
  vị trí sư đứng (34,5;−14) → (31;−11) + ghi chú code. Avatar không có
  collider và không nằm trên tuyến/kiểm tra nào của tailB nên kết quả
  mang sang nguyên vẹn; bản cuối đã được xác nhận trực tiếp bằng
  charsWorld (sư đứng đúng (31,−11)) + 2 ảnh cận sư 1000×2000.
- Lượt tự nhiên trọn vẹn trên bản nhị phân cuối: CHƯA chạy lại (xem Nợ).
- Bộ ảnh sau: `v8_shots/after/` — 9 ảnh 1000×2000 thật (spawn, mặt
  tiền, sân+lư, sư nam, sư tây, sư đông-nam, sư tây-nam, giảng đường,
  trong điện); đã tự soi tất cả các ảnh chốt (mặt tiền, sân+lư, trong
  điện, giảng đường, 3 ảnh sư).

## CÁC LỖI THẬT PHÁT HIỆN BẰNG ĐO ĐẠC (có sẵn từ trước V8, không phải V8 gây ra)
1. **6 khách quỳ trong điện vô hình:** module_5 ghi position (300+x, 300+z)
   cho group là CON của temple (+300,+300) → thế giới (600+x, 600+z).
   Bằng chứng: `v8_shots/before/chars.json` — chars 16–21 ở (595,5–604,5;
   596–602); ảnh `v8_5_trong_dien` (before): sàn điện trống trơn. Verify
   48 PASS của V7.3 không bắt được vì `__v7chars` chỉ báo tọa độ local.
   **Đã sửa:** position → (x, 0.32, z) + thêm 6 bồ đoàn module_3 khớp vị trí.
2. **Hai sư vô hình trong hộp đặc giảng đường:** nhà giảng đường là hộp đặc
   14×9 tại (44,−20) → x 37–51, z −24,5…−15,5; sư đứng (38,−18) nằm trong
   hộp, tuyến sư đi bộ xuyên hộp ở (44,−16)/(37,−23); waypoint cuối của
   NPC khách #5 (44,−16) cũng trong hộp. Bằng chứng: charsWorld before
   (sư đứng (38,−18)) + ảnh `v8_3_su` (before) chỉ thấy tường trơn.
   **Đã sửa:** sư đứng → (31;−11) hướng giảng đường (điểm trung gian
   34,5;−14 bị cây tại (34,−14) trong treeSpots che khuất ở cả 2 góc chụp —
   lỗi phát hiện khi soi ảnh v8_3_su/v8_3b_su_tay; điểm cuối cách thân cây
   4,24m, cách hộp giảng đường 6m); tuyến đi bộ →
   [[35,−12],[30,−18],[33,−24],[38,−9]] (đất trống, hở ≥2,4m với mọi vật
   trang trí mới); waypoint NPC #5 → (36,−11).
3. **Khách "quỳ" mà như đứng:** buildCharModel ghim action 'Quỳ' ở t=5,15s.
   Đo đường cong Pelvis Y trong cả 3 GLB chuẩn (parser GLB thuần): đoạn
   GIỮ QUỲ là 2,09–3,13s (−0,570); t=5,15s là giữa đoạn ĐỨNG DẬY (−0,27).
   Bằng chứng số: `chars_probe.json` trước sửa — pose='Quỳ' nhưng chiều
   cao chỉ giảm ~0,1m (nữ 1,59 so đứng 1,71–1,75; nam/trẻ gần như không
   giảm). **Đã sửa:** ghim t=2,6 (giữa đoạn giữ quỳ). Sau sửa đo lại:
   nữ 1,59→1,28, nam 1,69→1,36, trẻ 1,23→1,00; đáy vẫn khớp mặt bồ đoàn
   (minY 0,18 sân / 0,32 điện). Ảnh façade + trong điện sau sửa: khách
   quỳ thật hai bên lư và trong điện.

## VERDICT THEO 5 TRỤC
### Trục 1 — Cảnh/điện: ĐẠT MỘT PHẦN
Đã thêm: dải mosaic cobalt + đinh vàng trên dải trán chánh điện và 2 tấm
cobalt ở tháp đầu hồi (đúng mã lam cổng chùa); dãy núi xa mờ sau chùa;
2 cây hoa hồng đào hai bên sân; sương nền 0,0028→0,0032 cho chiều sâu
sáng sớm; khu giảng đường có đèn đá + bonsai + bảng "LỊCH GIẢNG / HUỆ
ĐĂNG". Giới hạn thật: mặt tiền vẫn là procedural (khối hộp + vòm), không
thể đạt độ nhiều lớp chạm khắc như mockup; mái giữ đỏ nâu theo ảnh thật
(xem mục khai lệch mẫu). Ảnh đã soi: `v8_shots/after/v8_1_mat_tien.png`
(bảng hiệu đọc đủ, dải cobalt thấy rõ), `v8_0_spawn.png`, `v8_4_giang_duong.png`.

### Trục 2 — Đi đứng: ĐẠT (trong giới hạn đo được ở môi trường SwiftShader)
- NPC/sư: gán snap `rotation.y = atan2(...)` → lerp có bọc góc dt×4
  (module_7 stepNPC). Probe 29 mẫu × 10 tick (`npc_turn_quick.json`):
  26/29 khoảng |Δyaw| ≤ 0,13 rad; 3 khoảng lớn (≤2,615) khớp giới hạn
  hội tụ của lerp khi NPC quay đầu ~180° ở cuối tuyến (≤0,86π/10 tick) —
  không phải nhảy tức thời 1 tick như bản cũ.
- Người chơi: đo series yaw khi rẽ 90° (`v8_shots/after/measure.json`):
  tiến tiệm cận 4,516→4,712, bước tối đa 0,098 rad/tick, êm sau ~5 tick.
- Thêm moveBlend (tấn công 5/s, thả 7/s): bước chân + nhịp đi tăng/giảm
  dần thay vì bật/tắt tức thời.
- Tư thế quỳ sửa ở lỗi #3 — đây là thay đổi "đi đứng" thấy rõ nhất trong ảnh.

### Trục 3 — Cách chơi: ĐẠT
Thêm dòng mục tiêu `#obj-line` ("Đang tới: …") hiện khi tự đi, tắt khi
tới nơi/hủy — phản hồi thao tác rõ mà không thêm bất kỳ cơ chế bị cấm
nào (vẫn 1 hệ tiến trình duy nhất = hàng cánh sen). Nhịp 60 giây đầu giữ
nguyên (đã kiểm chứng ở các vòng trước + natural run V8 đạt 50 PASS /
0 FAIL tới P19). Hành trình 9/9 giữ nguyên (xem mục kiểm chứng).

### Trục 4 — Học viện/Giảng đường: ĐẠT MỘT PHẦN
Đã sửa: chấm bản đồ "Kinh sách" từ tọa độ cũ (33,−12 — TRONG tường điện)
về đúng (42,−10,5); modal Phòng kinh sách có nút mở Bài giảng hoạt động;
v3.js tổng quát hóa để mở được nhiều bài full; **thêm 1 bài full MỚI:
D3 "Các tượng lớn trong khuôn viên chùa"** — lắp 100% từ số liệu đã có
nguồn trong thẻ "Tìm hiểu thêm" (A Di Đà 18m/2008/bệ 7m; Di Lặc 2010
~20m >250 tấn; Niết Bàn ~32m/2013; Bảo tháp 2015/35m/7 tầng/15 bộ Pháp
Hoa; quy tắc thắp nhang 1 lần ở lư sân, không chỉ tay/sờ tượng), gồm tóm
tắt + ví dụ + 3 câu trắc nghiệm + suy ngẫm + thực hành. Khu vực được
trang trí thêm (đèn đá, bonsai, bảng lịch giảng). **Chưa đạt phần còn
lại:** 22/24 bài vẫn "sắp mở" — không bịa giáo lý để lấp đầy.
### Trục 5 — Trang phục + đồ lễ: ĐẠT
- **Sư:** áo tràng XÁM + dải vai CAM sơn theo đỉnh (vertex) ngay trên GLB
  chuẩn — không đổi model/mesh/tỉ lệ. Đã soi cận trên BẢN CUỐI
  (`v8_shots/after/v8_3c_su_dongnam.png` + bản phóng to): dải cam chạy
  chéo từ cổ xuống ngực rõ ràng, áo xám, hai tay chắp. Sư đứng ở (31,−11)
  (charsWorld trên bản cuối xác nhận), sư đi bộ chạy tuyến ngoài hộp.
- **Đồ lễ:** bồ đoàn đỏ viền vàng ×5 ở sân (3 chiếc có khách quỳ thật sau
  sửa lỗi #3 — ảnh façade: khách quỳ hai bên lư hương đúng bố cục mẫu) +
  ×6 trong điện khớp 6 khách thiền; đèn đá nâng lên 8 cây thành 2 hàng;
  khói lư đưa lên trần spec đã khóa (opacity đỉnh 0,36→0,38, sprite lớn
  hơn) và chỉ hiện khi lư đã thắp; đồ thờ trong điện giữ nguyên V7.3.

## ĐIỂM CHỦ ĐỘNG KHÔNG THEO MẪU (khai rõ)
- **Mái điện giữ đỏ nâu** theo ảnh thật Vĩnh Tràng + palette đã khóa; mẫu là
  mockup vẽ mái lam. Tiệm cận tông lam bằng dải mosaic cobalt trên mặt tiền
  (đúng mã lam của cổng chùa) thay cho đổi màu mái.
- **Khói lư chỉ hiện khi lư đã thắp** (nghiên cứu nghi lễ đã khóa: thắp một
  lần ở lư sân) — không để khói ambient vô điều kiện như mockup.
- **Người chơi vẫn là khách nữ mặc định** (hệ profile + theme image-48);
  sư trong mẫu là NPC — hai sư trong bản là NPC, nay mặc đúng áo xám + dải cam.

## LỖI THỨ BA — KẸT ĐƯỜNG SÁCH → ĐIỆN, ĐÃ SỬA TẬN GỐC (engine di chuyển)
Đoạn đi từ Phòng kinh sách vòng qua tháp đông chánh điện về trạm điện:
verify (cả lượt tự nhiên lẫn tailB) kẹt cứng ở (38,5; ~0,28) — 3 hop
timeout, verdict "vào lại chánh điện / vào lại nội điện" FAIL (tailB
18/21, 3 FAIL cùng một cụm). Chuỗi chẩn đoán bằng số (hop_test A/B/C/D):
- Lượt A/B (bản V8 có hòa tốc / bản tắt hòa tốc blendK=1): kẹt Y HỆT
  (38,51; 0,25–0,29) → **hòa tốc vô tội**.
- Đọc code: vùng cấm tháp đông = colRect (37,4; 0,8)–(39,8; 3,2), biên
  va chạm 0,5 → cấm z ≥ 0,30; avatar dừng z ≈ 0,28.
- **Gốc rễ:** nhánh thoát chéo trong `tryMove` (module_6a) chỉ chạy khi
  `pos.x === px && pos.z === pz` (bằng tuyệt đối). Hướng đi tới (38,5; 6)
  từ (38,51; ·) có thành phần x ≈ −0,002 → bước đơn trục x "thành công"
  ~0,0001 m/tick, điều kiện bằng không bao giờ đúng → nhánh thoát không
  bao giờ chạy; avatar bò 0,1 mm/tick (đo: +0,01 m/30 game-giây). V7.3
  từng qua đoạn này là nhờ may mắn vi-hướng (pos.x khớp đúng 38,5).
- **Sửa 1:** điều kiện vào nhánh thoát → tiến độ thật < 25% bước định đi.
  Hop D: avatar trượt tây được (38,51 → 37,87 ở 30 game-giây) nhưng dao
  động đông–tây triệt tiêu dần (37,87 → 37,78 ở 600 tick tiếp) vì góc
  thoát thắng thay đổi từng tick ở mép biên 1 cm.
- **Sửa 2 (hysteresis):** nhớ dấu hướng thoát thành công gần nhất
  (escSign), thử các góc cùng phía trước; quên khi đi thông hẳn. Kèm
  góc ±90 (trượt ngang thuần) đã thêm ở bản trước. Mọi đích thoát vẫn
  qua pointBlocked — không bao giờ xuyên vật.
- **Sửa 3 (làn verify — phần đệm, không đổi verdict):** probe vi mô
  (mẫu mỗi 2 tick) cho thấy avatar trượt tây TỐC ĐỘ TỐI ĐA tới x=37,50
  rồi bật ngược đông — vì tại đó vùng cấm điện (x ≤ 37,5; z ≤ 1,7) nối
  liền vùng cấm tháp: dải x=38,5 mà làn hop cũ ép đi là **xuyên thân
  tháp, bịt kín về hình học**; khe qua duy nhất là x > 40,3 (đông tháp)
  hoặc x < 5,7 (tây tháp). Đường tự đi THẬT của game (trạm điện via
  (21; 9,5)) trượt góc đông-nam của điện được vì trục nam tự do — người
  chơi thật không kẹt; chỉ làn hop kiểm thử sai. Làn đệm 1 —
  (42;4,0) → (28;3,3) → (17,5;6,8) — vẫn timeout ở (28;3,3) vì dải
  z 3,3–4,0 cưỡi lên mép vùng cấm tháp (z ≤ 3,7) (log
  `v8f_tailB_lane1.log`; các phần P14–P18 + books của lượt đó vẫn PASS).
  **Làn đệm 2 (bản chốt, đã sửa trong verify_v73_tailB.mjs +
  verify_v73_run.mjs): (42;−7,6) → (42;4,3) → (30;4,5) → (28;2,8) →
  (17,5;6,8)** — khoảng hở tính tay: mép tháp (z ≤ 3,7) hở ≥ 0,6m; cây
  (40,6) R=1,0 hở ≥ 1,67m; thùng công đức (27,9;4,9) R=1,3 hở ≥ 1,67m
  trên mọi đoạn (nhờ điểm võng nam (28;2,8)); bonsai (29,2;6,4) và hồ
  đông (z ≥ 8,5) tránh hẳn. Các verdict P20 giữ nguyên từng chữ như V7.3.
- Kiểm chứng sau sửa: **tailB trên làn 2 (log `v8f_tailB.log`): verdicts
  21/21 PASS, exceptions 0, console errors 0** — vào lại chánh điện
  (station=hall) PASS, vào lại nội điện (inside=true) PASS, kẹp camera
  cột 3/3 PASS (minDist 0,80/0,80/0,81 = đúng bán kính kẹp), đối chứng
  xa cột cam=[300,294] PASS (khớp giá trị V7.3), books 2/2 PASS và
  **toàn lượt không có FF-TIMEOUT nào**. (Hai dòng "shot FAILED (bo
  qua)" trong log là ảnh chụp phụ tùy chọn của chính script verify —
  nó tự bỏ qua khi timeout; không phải verdict.)

## NỢ CÒN LẠI SAU V8
- Lượt tự nhiên (natural run) chưa chạy lại trọn vẹn đầu–cuối trên bản
  nhị phân cuối 17.260.812 (bằng chứng thay thế: natural 50/0 tới P19 +
  tailA full PASS + tailB 21/21 — cả ba trên các bản chỉ khác bản cuối
  ở các thay đổi đã khai từng mục).
- Cổng bonus-NPC của bộ verify chưa từng chạy hoàn tất trên bất kỳ bản
  V8 nào (trang phụ chết vì reboot VM) — nợ mang từ V7.3 sang.
- 22/24 bài giảng vẫn "sắp mở" (chỉ A0 + D3 là bài full) — chờ nguồn
  giáo lý có kiểm chứng, không bịa.
- Tượng Phật bản web vẫn là khối trơn không nét mặt (nợ điêu khắc;
  luật tượng cấm chỉnh tùy tiện — ngoài phạm vi V8).
- Chữ G cuối bảng hiệu còn chạm lá cây ở mép khung khi chụp (nợ khung
  hình từ V7.3, không phải lỗi cảnh).
- Kẹt khi đâm thẳng vào collider tròn vẫn là LỚP nợ của engine: V8 đã
  giảm nhẹ tận gốc cho các trường hợp đo được (điều kiện vào nhánh
  thoát theo tiến độ + hysteresis + góc ±90) và dời 2 bồ đoàn chắn
  tuyến; không tuyên bố diệt hết lớp lỗi này.
- Đo quay NPC dạng mẫu-mịn (150 mẫu × 2 tick) bị cắt vì môi trường
  SwiftShader quá chậm (~40 phút không xong phần B) — đã thay bằng
  probe 29 mẫu × 10 tick + series rẽ của người chơi (mục Trục 2).
- Bảng "LỊCH GIẢNG / HUỆ ĐĂNG" bị mái quầy kinh sách che một phần ở
  góc chụp cao từ tây-nam; nhìn từ sân phía nam thì đọc được.
