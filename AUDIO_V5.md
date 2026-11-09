# AUDIO V5 — Giọng dẫn Chùa Online (bàn giao tuyến âm thanh)

**Ngày sản xuất:** 2026-11-07 · **Nguồn văn bản:** `NGHIEN_CUU_AM_THANH.md` mục 5
(cột "Bản thu đề xuất") — thu **đúng từng chữ**, không tự sửa. (Ngoại lệ: 3 file
thu lại cuối ngày 07/11 theo `THIET_KE_V5_CHOT` — xem mục ✅ ở cuối file.)
**Giọng:** `avocado_v2:MAI_03` (TTS tích hợp sẵn trong môi trường, tiếng Việt),
một giọng duy nhất cho mọi file. Tốc độ 92 cho câu dẫn, 80 cho 4 dòng Kệ Hồi Hướng.
FPT.AI/Vbee **không** dùng: cả hai đều cần tài khoản/API key mới — theo lệnh
tuyến, không tự tạo tài khoản/đăng nhập mới.
**Nhãn trung thực (bắt buộc hiển thị trong app, mục Giới thiệu/Nguồn âm thanh):**
"Giọng dẫn của An là **giọng đọc nhân tạo** (TTS), thu một lần thành file tĩnh."
**Xưng hô:** An gọi người nghe là "bạn"; tự xưng "An"/"mình" đúng nguyên văn đã duyệt.

## Cách nghe kiểm đã áp dụng
- Đo thời lượng từng file bằng ffprobe, đối chiếu ước lượng
  (số từ × 60 / (155 × tốc độ/100)); ngưỡng bất thường > 1,6 lần.
- Nghe kiểm bằng transcript ASR (faster-whisper, model small, ngôn ngữ vi) —
  phương pháp vòng kín bắt được: nuốt chữ, thay từ, đọc sai số liệu, sai tên riêng ở mức âm tiết.
- Giới hạn thành thật: whisper-small tự nó hay sai **thanh điệu** tiếng Việt
  (chùa→"chua", tượng→"tưởng", cổng→"khổng", trọn→"tróng", đệ→"để"… trong transcript
  đều là lỗi của ASR, khung từ khớp 100% nguyên văn). Ba điểm dưới đây cần **tai người
  nghe xác nhận thanh điệu lần cuối** trước khi phát hành: "rất riêng / rất hiền"
  (s3_bo_dep, s4_dilac — ASR nghe thành "đức", đã kiểm chéo: bản thu mẫu "đức" thật
  cho transcript gần như y hệt → kết luận đây là lỗi phân định của ASR, không phải
  giọng đọc sai), "lạy ngài" (s1_adida, s3_lay_phat), "Huệ Đăng" (s3_giang_duong —
  khung "…Đăng" đúng, âm "Huệ" ASR lúc "Hủy" lúc "Hội").

## Bảng key — câu dẫn (11 + 2)

| Key | Nguyên văn (đúng bản thu) | Thời lượng | Ước lượng | Nghe kiểm (ASR) |
|---|---|---|---|---|
| s0_chao | "An chào bạn. Mình đang đứng trước cổng Phương Tiện, chùa Vĩnh Tràng. An sẽ đi cùng bạn một vòng chùa, thong thả thôi nhé." | 9,00s | 12,2s | ĐẠT — "Phương Tiện" rõ từng âm; "Vĩnh Tràng" khung âm đúng (ASR mất dấu) |
| day_di | "Chạm vào vòng sáng để đi tới nhé." | 2,90s | 3,4s | ĐẠT — khớp từng chữ |
| s0_nhan_nhang | "Sạp nhang hoa ở ngoài cổng — nhang và hoa lễ đều mua ở đây." (THU LẠI 09/11 theo hiển thị v6 — câu `an:` của trạm stall, module_6b.js; trước đó đã thu lại 07/11 theo THIET_KE_V5_CHOT) | 4,56s | 5,9s | ĐẠT — khớp từng chữ (ASR ghi "nhan" thiếu phụ âm cuối là lỗi quen của ASR) |
| s1_adida | "Đây là tượng Phật A Di Đà, cao mười tám mét trên bệ cao bảy mét, khánh thành năm hai nghìn không trăm linh tám. Mình lạy ngài một lạy nhé." | 10,25s | 13,9s | ĐẠT về nội dung — số đọc thành chữ đúng (ASR quy về "18m / 2008"); "A Di Đà" nghe liền thành một cụm; đoạn "lạy ngài một lạy" chờ tai người xác nhận thanh điệu |
| s2_thap_nhang | "Lư hương giữa sân. Cả buổi lễ, nhang chỉ thắp ở đây một lần, châm từ đèn dầu bên cạnh lư." (THU LẠI 09/11 theo hiển thị v6 — câu mở của trạm burner, module_6b.js; 4 nhịp trong panel giữ toast chữ) | 7,08s | 8,8s | ĐẠT — đủ chữ, đúng thứ tự (ASR: lư→"lưu", thắp→"thấp", nhang→"nhan" là lỗi dấu/phụ âm của ASR) |
| s3_bo_dep | "Chánh điện Vĩnh Tràng. Cửa giữa dành cho chư Tăng — khách vào cửa bên phía tây, bỏ dép ở thềm." (THU LẠI 09/11 theo hiển thị v6 — câu `an:` của trạm hall, module_6b.js; lần thu đầu dùng nhầm câu `onEnterInterior` nên đã thu lại) | 7,34s | 8,4s | ĐẠT — khớp khung từng chữ (ASR: Tràng→"tràn", chư→"chưa", Tăng→"tăng", dép→"giép" là lỗi dấu/phụ âm của ASR) |
| s3_lay_phat | "Trước Kim Thân Đức Phật, mình lạy ba lạy. Hương mình đã thắp ở lư sân rồi, trong điện chỉ lễ Phật thôi nhé." (THU LẠI 07/11 theo THIET_KE_V5_CHOT — xem mục ✅ cuối file) | 8,54s | 10,1s | ĐẠT — ASR khớp cả 2 câu; thu 2 đoạn theo 2 câu ghép nghỉ 0,5s vì bản thu 1 lần bị lỗi backend (xem mục ✅) |
| s4_dilac | "Đây là tượng Phật Di Lặc, khánh thành năm hai nghìn không trăm mười, cao khoảng hai mươi mét. Ngài cười rất hiền. Mình vái ngài một vái nhé." | 8,95s | 12,6s | ĐẠT — số đúng (ASR quy về "2010 / 20 mét"); "Di Lặc" khung "…lạc" rõ (ASR ghi "ghi lạc"/"dây lạc"); "rất hiền" chờ tai người xác nhận |
| s5_nirvana | "Đây là tượng Phật nhập Niết Bàn, dài khoảng ba mươi hai mét. Mình đứng lặng một lát, rồi vái ngài nhé." | 7,13s | 10,1s | ĐẠT — "Niết Bàn" khung đúng (ASR ghi "niec bàn"), số 32 đúng |
| s6_hoi_huong | Dẫn (THU LẠI 09/11 theo hiển thị v6 — câu `an:` của trạm tower, module_6b.js): "Bảo tháp Thất Phật — dựng năm 2015, cao ba mươi lăm mét, bảy tầng thờ bảy vị Phật. Vườn tháp Tổ là khu riêng, ở phía sau." + Kệ 4 dòng GIỮ NGUYÊN (xem dưới) | 24,05s | ~25,2s | ĐẠT — dẫn khớp khung từng chữ, số 2015 / 35 mét / 7 tầng / 7 vị đọc đúng (ASR quy về số); "Thất Phật" vẫn chờ tai người xác nhận thanh điệu; 4 dòng kệ là file cũ nguyên vẹn, ASR bản ghép đủ 4 dòng đúng thứ tự |
| s7_tam_biet | "Mình đã đi trọn một vòng chùa rồi. Ghé cửa hàng lưu niệm ở đây nếu bạn muốn mang một món quà nhỏ về nhé. Cảm ơn bạn đã đến chùa Vĩnh Tràng." | 10,08s | 14,3s | ĐẠT — đủ chữ (ASR: trọn→"chọn", lưu→"lu", Tràng→"tràn" là lỗi dấu của ASR) |
| merit_box (phụ) | "Thùng công đức ở đây. Tùy tâm của bạn thôi, không có mức nào cả." | 4,51s | 6,3s | ĐẠT — đủ chữ (ASR: Thùng→"Khủng" là lỗi phụ âm đầu của ASR) |
| s3_giang_duong (phụ) | "Đây là Giảng đường Huệ Đăng. Chùa Vĩnh Tràng là nơi Trường Trung cấp Phật học Tiền Giang ra đời năm một nghìn chín trăm chín mươi, và lớp Cao đẳng Phật học của trường hiện vẫn đặt tại đây." | 12,65s | 18,1s | ĐẠT về nội dung — năm đọc thành chữ đúng (ASR quy về "1990"); "Huệ Đăng" chờ tai người xác nhận âm "Huệ" |

Không file nào vượt ngưỡng thời lượng bất thường (tỉ lệ thực tế/ước lượng 0,67–0,90,
nhịp giọng đều ~205–215 từ/phút ở tốc độ 92). Không file nào phải thu lại vì lỗi nội
dung; riêng phần kệ từng có 1 lần thu lỗi kỹ thuật (file rỗng do backend) đã thu lại ngay.

## Kệ Hồi Hướng (key s6_hoi_huong)
- Ghép từ 5 phần thu riêng: câu dẫn (tốc độ 92) + nghỉ 1,0s + 4 dòng kệ thu **tách
  riêng từng dòng** ở tốc độ 80, nghỉ 0,9s giữa các dòng. Tổng hiện tại **24,05s**
  (bản đầu 22,71s; dẫn thu lại 07/11 → tổng 21,63s; dẫn thu lại lần nữa 09/11 theo
  hiển thị v6 — dẫn mới 10,25s thay vào `ke_parts/s6_dan.mp3`, 4 phần kệ giữ
  nguyên vẹn; bản ghép đo đúng tổng tính tay 24,052s).
- Nguyên văn kệ (đã đối chiếu ở NGHIEN_CUU_AM_THANH mục 1, giữ chữ "sanh"):
  "Nguyện đem công đức này. / Hướng về khắp tất cả. / Đệ tử và chúng sanh. /
  Đều trọn thành Phật đạo."
- Các phần lẻ lưu ở `audio_v5/ke_parts/` (s6_dan.mp3, s6_ke_1..4.mp3) để tuyến web
  dùng lại nếu cần phát theo dòng.
- **Không** thu TTS Chú Đại Bi / phần Hán âm (theo chốt) — phần đó giữ karaoke chữ + mõ.

## Tiếng tụng xa — niem_phat_xa.mp3
- File: bản MP3 xem trước (HQ) của Freesound #345028 "Temple chanting interior"
  (tác giả 3bagbrew) — tăng chúng tụng trong chánh điện chùa Gakwonsa, Cheonan,
  Hàn Quốc. Thời lượng 402,0s (6:42, khớp metadata trang nguồn), 8.504.606 byte.
- Giấy phép: **CC0** (đã kiểm trên trang nguồn:
  https://freesound.org/people/3bagbrew/sounds/345028/).
- Điều kiện dùng (theo nghiên cứu mục 3.3): CHỈ làm âm cảnh "tiếng tụng xa" ở mức
  âm lượng rất nhỏ; đây là tiếng tụng tiếng Hàn/Phạn — **tuyệt đối không giới thiệu
  là tiếng tụng của chùa Vĩnh Tràng**. Bản gốc WAV 101,6 MB cần đăng nhập Freesound
  mới tải được — theo lệnh tuyến không đăng nhập mới, nên dùng bản xem trước HQ cùng
  một bản ghi (đủ cho lớp nền âm lượng nhỏ; khi cắt 60–90s cho web nên transcode
  Opus mono ~48 kbps theo ngân sách dossier).

## Để trống có chủ ý
- **Vòng niệm Phật "Nam Mô A Di Đà Phật" bằng giọng người thật: ĐỂ TRỐNG** (theo
  chốt THIET_KE_V5_CHOT mục 5) — không thu TTS giả tụng. Chờ giọng người thật
  tình nguyện thu theo đặc tả nhịp ở NGHIEN_CUU_AM_THANH mục 2.3 (8–10 câu/phút,
  6 chữ liền, nhóm 3–3–4, mõ cuối câu).

## ✅ Ba mâu thuẫn nội dung — ĐÃ XỬ LÝ (thu lại 07/11/2026 theo THIET_KE_V5_CHOT)
Bản thu đầu làm đúng cột nguyên văn của NGHIEN_CUU_AM_THANH mục 5, nhưng 3 chỗ
trong nguyên văn đó **mâu thuẫn với THIET_KE_V5_CHOT**. Coordinator đã chốt
THIET_KE thắng; cả 3 file đã thu lại đúng từng chữ theo câu mới và kiểm đủ
ffprobe + ASR theo quy trình ở đầu file:
1. `s0_nhan_nhang` (cũ nói "nhận… không tốn gì đâu" — sai chốt MUA ở sạp,
   THIET_KE mục 3.2) → bản mới **6,34s**: "Ngay bên cổng có sạp nhang hoa của
   chùa. Mình ghé mua nhang và một bó hoa sen mang theo nhé." (Lần thu đầu ra
   file rỗng 0 byte — lỗi backend thoáng qua; thu lại lần 2 đạt.)
2. `s3_lay_phat` (cũ nói "thắp hương ở bát hương trong điện" — sai chốt trong
   điện không thắp, THIET_KE mục 4) → bản mới **8,54s**: "Trước Kim Thân Đức
   Phật, mình lạy ba lạy. Hương mình đã thắp ở lư sân rồi, trong điện chỉ lễ
   Phật thôi nhé." **Sự cố kỹ thuật:** bản thu 1 lần đầu bị lỗi backend —
   giọng thoái hóa thành vòng lặp vô nghĩa ("chăm đức điện thổ…" lặp ~20 lần),
   tổng 48,53s ≈ 4,8 lần ước lượng; đã thu lại thành 2 đoạn theo 2 câu
   (3,26s + 4,78s), ghép nghỉ 0,5s — ASR khớp cả 2 câu.
3. `s6_hoi_huong` câu dẫn (cũ nói tháp là "nơi lưu tro cốt chư Tăng và Phật
   tử" — sai chốt **Bảo tháp Thất Phật**, THIET_KE mục 3.8) → dẫn mới **7,82s**:
   "Đây là Bảo tháp Thất Phật, bảy tầng thờ bảy vị Phật. Mình cùng đọc bài kệ
   hồi hướng để khép lại vòng chùa nhé." — đã thay vào `ke_parts/s6_dan.mp3`
   rồi ghép lại với 4 phần kệ CŨ NGUYÊN VẸN (nghỉ 1,0s sau dẫn, 0,9s giữa
   các dòng): tổng mới **21,63s**.
Điểm chờ tai người xác nhận thanh điệu (bổ sung): "Thất Phật" ở câu dẫn s6 mới
— ASR nghe thành "thức Phật", cùng lớp mơ hồ thanh điệu như các điểm đã ghi ở
đầu file, khung từ khớp nguyên văn.

## ✅ Lệch giọng/chữ với lời hiển thị v6 — ĐÃ XỬ LÝ (thu lại 09/11/2026)
Web v6 ("Trang nghiêm") viết lại lời An theo kính ngữ làm 4 key lệch giữa giọng
đã thu và chữ hiển thị. Cả 4 đã thu lại **đúng nguyên văn hiển thị** trích từ
`v6_parts/` (giọng `avocado_v2:MAI_03`, tốc độ 92; kiểm đủ ffprobe + ASR từng
file; không file nào vượt ngưỡng bất thường 1,6× ước lượng — tỉ lệ thực
tế/ước lượng 0,77–0,96):
1. `s0_nhan_nhang` → **4,56s**: "Sạp nhang hoa ở ngoài cổng — nhang và hoa lễ
   đều mua ở đây." (câu `an:` của trạm stall, module_6b.js — playVoice phát
   lúc bấm mua ở sạp; toast mua chứa số nén biến thiên nên không thu.)
2. `s2_thap_nhang` → **7,08s**: "Lư hương giữa sân. Cả buổi lễ, nhang chỉ
   thắp ở đây một lần, châm từ đèn dầu bên cạnh lư." (câu mở của trạm burner;
   4 nhịp trong panel giữ nguyên toast chữ theo thiết kế.)
3. `s3_bo_dep` → **7,34s**: "Chánh điện Vĩnh Tràng. Cửa giữa dành cho chư
   Tăng — khách vào cửa bên phía tây, bỏ dép ở thềm." (câu `an:` của trạm
   hall, module_6b.js. **Sửa sai:** lần thu đầu dùng nhầm câu trong
   `onEnterInterior` ("Vào điện bằng cửa bên, dép để ở thềm…") — coordinator
   đã chốt đúng câu trạm hall; đã thu lại với đúng câu này, ASR khớp khung
   từng chữ, thời lượng 7,34s so với ước lượng 8,4s.)
4. `s6_hoi_huong` → dẫn mới **10,25s** thay vào `ke_parts/s6_dan.mp3`: "Bảo
   tháp Thất Phật — dựng năm 2015, cao ba mươi lăm mét, bảy tầng thờ bảy vị
   Phật. Vườn tháp Tổ là khu riêng, ở phía sau." (câu `an:` của trạm tower.)
   4 phần kệ `s6_ke_1..4.mp3` GIỮ NGUYÊN bản thu cũ đã kiểm khớp từng chữ;
   ghép lại đúng công thức cũ (nghỉ 1,0s sau dẫn, 0,9s giữa các dòng) → tổng
   mới **24,05s**. ASR bản ghép: dẫn + đủ 4 dòng kệ, đúng thứ tự; các số
   2015 / 35 mét / 7 tầng / 7 vị trong dẫn đọc đúng.
Điểm chờ tai người (giữ nguyên các lượt trước): thanh điệu "Thất Phật" ở dẫn
s6 — ASR nghe "thức Phật", cùng lớp mơ hồ thanh điệu đã ghi nhận, khung từ
khớp nguyên văn.
Sự cố quy trình (không ảnh hưởng sản phẩm): lượt ghép s6 đầu bị treo ở câu
hỏi ghi đè file của ffmpeg (thiếu cờ `-y`) tới khi hệ thống dừng tiến trình;
đã ghép lại với `-y` ra file tạm, đo thời lượng khớp đúng tổng tính tay
24,052s rồi mới đặt vào chỗ — file đích không bị hỏng ở lượt treo (ffmpeg
thoát mà không ghi).
