# TỔNG KẾT VÒNG GIỐNG-THẬT V6 (P0–P3) + ĐỀ XUẤT VÒNG TIẾP
Ngày 07/11/2026. Chuẩn đánh giá: đối chiếu ảnh thật refs/ + ảnh mẫu theme
image-48, mọi kết luận có số đo hoặc render làm chứng. File chuẩn hiện tại:
layout_v8_p3.blend (grade mặc định = tông Sáng trong; chờ Chung Hy chốt tông).

## Đã thay đổi thật sau 6 đợt (V4 -> V10)
- Bề mặt: từ 100% màu phẳng -> PBR + HDRI + AO compositor; hốc vòm tối sâu
  -33% rồi thêm -24% ở P1; vật hết "trôi".
- Màu nhận diện: cột teal -> đỏ son (0% teal); vàng mặt tiền đo khớp #D9A441
  ±12; hồ cyan -> rêu + phản chiếu; trời phẳng -> cobalt 3 tông; bệ Phật nằm
  hết bị gán nhầm vàng, về đá xám + chữ vàng đọc đúng chiều cả 3 bảng.
- Cổng: cẩn sứ photo-texture từ ảnh cổng thật, hết vật lơ lửng.
- Đời sống: cây khối cầu -> cây lá card + cọ (11–14 tông xanh đo được),
  hoa giấy, bonsai, rào vàng kín chu vi, 14 người, lư hương S2,
  thùng công đức, biển Phương Tiện/Tịnh Độ.
- Phong hóa: chân tường tối hơn 12,6% theo vệt nước, thân tường không bẩn;
  decal rêu mép mái (V7, 2 vòng sửa).
- V7 (14:56 07/11): mật độ +1,0pp xanh lá flycam, hoa giấy ×2,1, cây tiền
  cảnh dày; mặt Di Lặc đạt một phần (bụng tròn hơn, vẫn ám xám-xanh).
- V8 (15:20 07/11): vòng rừng ngoài rào — xanh lá flycam toàn ảnh 6,9% ->
  11,5% (SW 17,0%), vượt chỉ tiêu; mặt Di Lặc hết ám xanh nhờ đèn fill ấm
  (B−R 31,7 -> −0,7), không đổi albedo.
- Web: bản nhẹ layout_v8_web.blend, -61% số mặt (2,41tr -> 932k), texture ≤1K.

## Thước đo thẳng thắn: giống thật đang ở đâu?
So với mốc V4 bị chê "cảm giác chân thật không có" (~20–25%): vòng V6–V8 đưa
mô hình lên khoảng **55–60%** theo cùng thang cảm nhận — đúng màu, đúng bố
cục, có bề mặt/sống thật, mật độ cây ngoài rào đã gần ảnh thật; nhưng chưa
tới mức "nhìn là chùa Vĩnh Tràng ngoài đời":
1. Mật độ trong sân vẫn thua flycam thật (khoảng trống trong khuôn viên, dù
   vòng rừng ngoài đã che phần lớn).
2. Mặt tượng (đặc biệt Di Lặc nhìn gần) vẫn là giới hạn điêu khắc tay — màu
   đã ấm, nét mặt vẫn đơn giản.
3. Cây card nhìn gần còn thưa ở trung cảnh; rêu mái ở góc mặt đất đọc thành
   mảng chữ nhật khá rõ; mặt đất xa ngoài rào vẫn phẳng (đã che phần lớn).

## Cập nhật V10 (09/11/2026) — file chuẩn: layout_v12_v10.blend
Mở vòng vì Chung Hy xem lại phán "vẫn thấy không giống". Xếp hạng lệch +
kết quả đầy đủ ở NOTES.md §V10. Tóm tắt: cổng có tháp + hốc tượng Phật
đứng trắng + chóp ngói (ĐẠT — sửa được lỗi nhận diện nặng nhất ở góc
cổng); nền ngoài rào hết hư vô (rừng 330 thân/1.880 mặt tán + đường nhựa
+ đất biến thiên — ĐẠT MỘT PHẦN, chưa thành biển dừa ref9); mái có biến
thiên mảng + bờ nóc (MỘT PHẦN, rêu vẫn vệt); hồ có lá sen + nước tối
(ĐẠT); tượng ấm màu về #EFE9DD (ĐẠT màu); diềm mặt tiền có hoa văn
lattice (MỘT PHẦN yếu — chưa thành tầng trang trí như ref1).
**Thước đo sau V10: ~65–68%** (từ ~60% sau V9).

## Nợ còn lại sau V10
1. Rừng ngoài rào: mật độ/bão hòa chưa bằng ref9 — cần kỹ thuật khác
   (tán 3D dày hoặc texture rừng), sương grade khóa làm xa nhạt.
2. Mặt tiền chánh điện thiếu hẳn tầng trang trí trên của ref1 (dải
   lattice cao + pediment giữa + bờ nóc trang trí) — cần dựng thêm vào
   model mặt tiền, việc kiến trúc riêng.
3. Rêu mép mái đọc vệt chữ nhật ở góc mặt đất (V9_ReuMai mesh gộp).
4. Di Lặc: tỷ lệ tượng/bệ (bệ 22×20 phẳng; thật là khối nhà có mái +
   thang, tượng choán bệ) + nét mặt sculpt đơn giản.
5. Người trong scene Blender tĩnh/chắp tay (để cho web GLB có xương).

## Đề xuất vòng V7 (chờ Chung Hy gật đầu mới chạy)
Ưu tiên theo tác động thị giác / công sức:
1. **Mật độ sâu theo ref9**: phủ cây + bụi hoa vào các khoảng trống (tây-nam,
   quanh tháp, dọc rào), nâng hoa giấy lên mật độ ảnh mẫu. Tác động lớn nhất.
2. **Decal rêu mái + vệt nước cổng** cho dứt điểm weathering.
3. **Chất lượng gần**: thay tán cây card bằng cụm lá dày hơn ở các cây tiền
   cảnh (chỉ vùng camera hay tới, giữ nhẹ máy).
4. **Mặt tượng**: chỉ làm khi có hướng đi mới (thử sculpt lại Di Lặc theo
   ref5 ở mức khối lớn: bụng, vành tai, nụ cười) — không hứa "như thật".
Song song (không thuộc vòng 3D): dựng trải nghiệm web v4 vẫn chờ duyệt danh
sách "cảm giác đi chùa"; bản web nhẹ đã sẵn sàng làm nền.


---

## V11 — đóng 5 nợ lớn nhất của V10 (09/11/2026, layout_v13_v11.blend)

Chung Hy duyệt chạy tiếp. Kết quả từng mục (chi tiết + số đo ở
layout/NOTES.md §V11; render: layout/layout_v13_{flycam,ground,gate,
facade,dilac}.png):

1. **Tầng trang trí mặt tiền — ĐẠT:** dựng đủ tầng trên hàng vòm theo đo
   ref1 (tường vàng + dải lattice trắng + relief vàng + cornice + pediment
   bảng 永長 + 2 tháp đầu hồi 福/壽). Tự bắt 2 lỗi texture (UV atlas của
   cube Blender 5; nét lattice quá mảnh) và sửa tận gốc trong vòng.
2. **Bệ Di Lặc — ĐẠT cấu trúc/tỉ lệ:** bỏ phiến phẳng 22×20; bệ khối có
   diềm ngói + mặt đá sẫm + 1 dải chữ vàng đúng chiều; tỉ lệ tượng:bệ 2,77
   so với 2,85 đo từ ref5. Nợ: tổng cao 11,3m vs thật ~20m (tỉ lệ sơ đồ
   toàn khuôn viên).
3. **Vành đai dừa — ĐẠT:** 340 cây ngoài rào (dừa + tán khối vertex-color),
   flycam thành thảm xanh liền; xanh toàn khung 22,86% → 32,93%; giữ 2
   hành lang cổng Nam.
4. **Rêu mái — ĐẠT:** 99 mảng nhỏ rời thay dải liền; hết vệt chữ nhật ở
   góc đất + flycam.
5. **Sương nhạt — ĐẠT:** mist start 85/depth 560 + ×0,45 riêng nhánh sương
   (AO không đụng); sương hiệu dụng tại chánh điện ở flycam ≈ 0,003; bão
   hòa vùng chánh điện 46,6 → 84,2; grade "Sáng trong" giữ nguyên.

**Thước đo sau V11: ~73%** (từ ~65–68% sau V10). Nợ còn: mặt tượng
(sculpt), nội thất (chưa có ảnh thật), tỉ lệ tuyệt đối sơ đồ, chi tiết
gốm mặt tiền giản lược, người tĩnh trong scene Blender, tán vành đai
nhìn gần còn faceted.
