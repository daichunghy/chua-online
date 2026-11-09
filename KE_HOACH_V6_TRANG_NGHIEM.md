# KẾ HOẠCH V6 — TRANG NGHIÊM (phản hồi Chung Hy + chị anh, 09:11 09/11/2026)
Phán quyết: "không có cảm giác đi chùa chút nào; nhân vật không có cảm nhận về
kiến thức Phật giáo; không nghiêm trang; làm chơi chơi; các thành phần lỗi hết,
lộn xộn". Chẩn đoán của coordinator (tự soi lại ảnh chụp v5): đúng cả 4 trục —
(1) bảng tên bay trên đầu NPC + tên ngẫu nhiên = ngôn ngữ game; (2) nút/toast
dính emoji, bong bóng thoại giọng vui nhộn kiểu hướng dẫn viên game; (3) NPC đi
lang thang vô định, không hành vi lễ; (4) nhãn chồng nhau ở mép màn hình, vài
luồng (nội điện, shop) chưa từng chạy kiểm thật nên lỗi tiềm ẩn.

## A. Khử tín hiệu game (bề mặt)
- XÓA bảng tên nổi trên đầu mọi NPC. Người đi chùa là khách vô danh như thật.
  Chú tiểu An chỉ nhận diện qua hộp thoại.
- XÓA emoji khỏi mọi nút/toast/thẻ (🚪🙏🌸…). Chữ thuần, giọng tĩnh.
- Hàng cánh sen: thu nhỏ, bỏ phát sáng/nhảy, tông kem tĩnh — chỉ là dấu vết
  hành trình, không phải thanh nhiệm vụ.
- Trong nhịp lễ (lạy, đứng lặng, hồi hướng): UI mờ xuống gần như biến mất;
  chỉ còn 1 nút "Tiếp" nhỏ khi thật cần. Chuông ngân ở nhịp mở đầu lạy và
  hồi hướng (WebAudio chuông đã có từ v4).

## B. Nhân vật có kiến thức + hành vi lễ (nội dung lấy từ nghiên cứu đã kiểm
chứng — NGHIEN_CUU_DI_CHUA_THAT.md, KHÔNG tự chế giáo lý)
- NPC: bỏ đi lang thang ngẫu nhiên. Hành vi đúng nếp: đi chậm trên lối đi,
  đứng chắp tay trước tượng, ngồi nghỉ ghế đá, một vị sư đi chậm qua sân.
  Tốc độ đi của avatar + NPC giảm; động tác lạy chậm lại và GIỮ một nhịp
  tĩnh sau khi lạy xong.
- Lời An viết lại: ít câu hơn, kính ngữ, bỏ giọng "nhé" vui nhộn. Mỗi trạm
  thêm 1 thẻ "Tìm hiểu thêm" tĩnh với dữ kiện ĐÃ kiểm chứng: vì sao 1 nén là
  tâm hương / 3 nén là Tam Bảo; vì sao không thổi tắt lửa; vì sao vào cửa bên;
  hữu nhiễu là gì; Bảo tháp Thất Phật thờ ai; hồi hướng nghĩa là gì. Nguồn
  ghi cuối thẻ (phatgiao.org.vn / tư liệu chùa) — thẻ nào không có nguồn thì
  không viết.

## C. Sửa lỗi + hết lộn xộn (chạy kiểm thật, không rà soát tĩnh)
- CDP chạy KHÔNG seed TOÀN TUYẾN: cổng → sạp → A Di Đà → Di Lặc → lư → nội
  điện trọn vòng (bỏ dép → lễ Tổ → lạy 3 → niệm kinh mở được → hữu nhiễu →
  ra) → Phật nằm → tháp → 2 điểm mua sắm (mở shop, mua 1 món, giỏ đúng) →
  bản đồ → khay Học Phật (Niệm kinh + Bài giảng bấm chạy) → Cài đặt. Lỗi JS
  nào lòi ra: sửa tại chỗ, chạy lại. Báo verdict từng luồng.
- Camera sạp: chỉnh góc/đích để mái + biển không choán tiền cảnh như ảnh
  2_sap.png.
- Độ sáng nội điện: rà lại đèn layer-1 (nợ v4 để lại), chụp ảnh nội điện
  nghiệm thu.

## D. Giới hạn nói thẳng
Cảnh 3D web vẫn là bản procedural cách điệu — V6 sửa CẢM GIÁC + nội dung +
lỗi, không biến cảnh thành giống thật. Giống thật nằm ở tuyến Blender (V10
đang chạy); khi model đạt, bước tích hợp model vào web mới là vòng sau.

## Nghiệm thu
Ảnh 5 trạng thái (spawn / trước tượng / giữa lễ lạy với UI đã mờ / nội điện /
shop) + log luồng CDP đủ + 0 lỗi JS. Coordinator tự soi ảnh đối chiếu tinh
thần "nghiêm trang" trước khi báo.
