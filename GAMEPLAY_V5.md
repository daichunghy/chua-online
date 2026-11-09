# THIẾT KẾ LẠI CÁCH CHƠI + PHONG CÁCH + ÂM THANH — web v5
Chung Hy phản hồi 07/11 22:44 về web v4: (1) vẫn chưa giống phong cách ảnh mẫu
image-48; (2) cách chơi vẫn khó hiểu — phải thiết kế lại cách chơi rồi mới làm;
(3) âm thanh thiếu giọng thật + độ chính xác — cải thiện RIÊNG một tuyến.
Tài liệu này là bản thiết kế; việc thực hiện bám đúng tài liệu này.

## A. Vì sao v4 khó hiểu (chẩn đoán thẳng)
- Mở vào là modal chọn người + chọn mục đích chắn hết cảnh — chưa thấy chùa đã
  phải trả lời 2 câu hỏi.
- Quá nhiều hệ cùng lúc: WASD + joystick + chạm sàn + nút ngữ cảnh + guided
  mode + "Xem nhanh" 5 góc + panel hành trình + thẻ an lạc + đèn nguyện + shop.
  Người mới không biết bắt đầu từ đâu, đi đâu, bấm gì.
- Không có "mục tiêu duy nhất" hiển thị: không vòng sáng đích, không mũi tên,
  không đường dẫn — người chơi tự đoán trạm tiếp theo ở đâu.
- HUD kiểu game (panel trái, nhiều nút nhỏ) trong khi ảnh mẫu là thẻ lớn, ít
  chữ, một hành động một thẻ.

## B. Cách chơi mới (nguyên tắc: MỘT VIỆC MỘT LÚC)
1. **Vào là thấy chùa.** Không modal chắn. Avatar đứng trước cổng Phương Tiện,
   camera sau vai. Chọn nhân vật/mục đích dời vào nút nhỏ góc phải (đổi lúc nào
   cũng được, mặc định Phật tử nữ như ảnh mẫu).
2. **Luôn có đúng 1 mục tiêu.** Đích hiện tại = vòng sen phát sáng + cột sáng
   nhẹ + thẻ lớn dưới cùng màn hình ghi đúng 1 câu: "Đi tới vòng sáng ở cổng"
   / "Bấm Nhận nhang" / "Đi tới lư hương giữa sân"... Hoàn thành thì mục tiêu
   tự chuyển trạm kế, không cần người chơi tự tìm.
3. **Đi lại = chạm là đi.** Chạm vòng sáng (hoặc nút "Đi tới đó" trên thẻ) thì
   avatar tự đi theo đường lát. WASD/joystick giữ làm tùy chọn phụ, không bắt
   buộc, không hướng dẫn dài — gợi ý 1 dòng nhỏ lần đầu.
4. **Hành động = 1 nút to duy nhất** khi tới nơi (Nhận nhang / Thắp nhang /
   Lạy Phật / Vái / Ngồi bồ đoàn / Thỉnh chuông), chữ lớn, giữa-dưới màn hình.
   Chuỗi thắp nhang chạy từng bước có thẻ hướng dẫn riêng từng nhịp (châm lửa →
   vái → cắm), mỗi nhịp 1 nút "Tiếp".
5. **Tiến trình = hàng hoa sen trên cùng**: 8 cánh sen = 8 trạm, cánh đang đi
   nhấp nháy, cánh xong tô hồng. Không panel chữ dài bên trái nữa.
6. **Header đúng ảnh mẫu**: pill trái "🪷 Chùa Online | Chùa Vĩnh Tràng"; pill
   phải: Khám phá / Học Phật / Tài khoản. Niệm kinh + Bài giảng nằm trong "Học
   Phật"; Thẻ an lạc + Đèn nguyện nằm trong "Khám phá" (không chen vào tuyến
   lễ); Shop chỉ mở ở S7 như cũ.
7. **Dẫn dắt bằng giọng An** (xem mục D): mỗi trạm An nói 1 câu ngắn (giọng
   thật) + hiện chữ. 10 giây đầu An dạy đi: "Chạm vào vòng sáng để đi tới nhé."

## C. Phong cách theo ảnh mẫu (đối chiếu trực tiếp image-48)
- UI: thẻ kem #FFF6E5 bo góc ≥24px, bóng mềm, tiêu đề serif xanh đậm
  #1C5A34 lớn, nút pill xanh đậm chữ trắng, điểm hồng sen + vàng đồng. Ít chữ,
  chữ to. Mọi panel cũ của v4 phải vẽ lại theo ngôn ngữ này (không panel tối,
  không viền mảnh kiểu game).
- Cảnh 3D sáng và rực vừa như ảnh mẫu: trời xanh có mây trắng, hoa giấy hồng
  dày dọc đường đi + quanh cổng/kiosk, bonsai xanh đậm hai bên trục, sen hồng
  ở hồ. Mật độ hoa dọc tuyến chính là tiêu chí nghiệm thu bằng ảnh chụp.
- Kiosk lưu niệm ở S7 vẽ giống ảnh mẫu (mái ngói cam, biển gỗ "Cửa hàng lưu
  niệm", đèn lồng hồng) — v4 đang là kiosk trơn.

## D. Âm thanh — tuyến riêng "giọng thật + chính xác"
Hiện trạng v4: ambience tổng hợp WebAudio + chuông/mõ synth, KHÔNG có giọng
người — Chung Hy chốt là thiếu giọng thật và thiếu chính xác.
Kế hoạch:
1. **Giọng An thật (TTS tiếng Việt)**: thu sẵn thành file MP3 cho từng câu dẫn
   trạm + dạy đi + câu bỏ dép + Kệ Hồi Hướng đọc chậm rõ. Danh sách khóa câu
   (key) cố định để v5 gắn: s0_chao, day_di, s0_nhan_nhang, s1_adida,
   s2_thap_nhang, s3_bo_dep, s3_lay_phat, s4_dilac, s5_niết_bàn (tĩnh lặng —
   chỉ 1 câu khẽ), s6_hoi_huong, s7_tam_biet. Nội dung câu lấy từ đặc tả audit
   (dữ kiện đã kiểm chứng ở mục F của CAM_GIAC_DI_CHUA.md) — KHÔNG bịa dữ kiện
   mới; câu nào chưa có nguồn thì chỉ dẫn hành động, không nêu số liệu.
2. **Niệm Phật có giọng**: 1 vòng "Nam Mô A Di Đà Phật" đọc/ tụng chậm có
   giọng thật làm lớp nền ở zone chánh điện + trong màn Niệm kinh (tùy chọn
   bật), thay cảm giác synth. Kiểm tra thời lượng từng file sau khi thu (bài
   học TTS: tên riêng lạ làm file dài bất thường → thu lại).
3. **Chính xác**: phát âm tên riêng (Vĩnh Tràng, Di Lặc, A Di Đà, Huệ Đăng)
   phải nghe rõ đúng; tốc độ chậm; mỗi file nghe kiểm lại 1 lượt trước khi
   gắn; ghi bảng kiểm vào AUDIO_V5.md.
4. Ambience synth cũ giữ làm nền (gió/chim/chuông gió) nhưng hạ dưới giọng;
   chuông/mõ giữ. Nút tắt tiếng + tắt giọng riêng.
Định dạng bàn giao của tuyến âm thanh: thư mục audio_v5/ (MP3 theo key) +
AUDIO_V5.md (bảng câu, nguồn dữ kiện, thời lượng, kết quả nghe kiểm). v5 gắn
theo key, file nào chưa có thì fallback về chữ (không lỗi).

## E. Thứ tự thực hiện
1. Tuyến A (v5): dựng lại cách chơi + phong cách theo mục B + C trên nền v4
   (giữ scene, khói, NPC, shop, niệm kinh/bài giảng), gắn hook giọng theo key
   của mục D (phát file nếu có, chưa có thì chỉ hiện chữ).
2. Tuyến B (âm thanh): sản xuất audio_v5/ theo mục D song song.
3. Coordinator ráp: kiểm file giọng có đủ key không, mở v5 kiểm chứng bằng
   ảnh chụp (S0 lúc mở, thẻ mục tiêu, 1 trạm giữa, S7 kiosk) + nghe thử ít
   nhất 2 file giọng, rồi báo Chung Hy.
