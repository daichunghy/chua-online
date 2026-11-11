# PROMPT CHO ARGON (AI Studio) — V9: CẢI THIỆN TOÀN DIỆN CHẤT LIỆU CHÙA VĨNH TRÀNG

Bạn làm việc trên repo `chua-online`: trải nghiệm web 3D đi chùa Vĩnh Tràng
(Tiền Giang — chùa có thật, di tích quốc gia). Bản dựng web nằm ở
`Mô hình 3D Vĩnh Tràng/trai-nghiem-vinh-trang-v7.html`, được lắp từ các module
trong `Mô hình 3D Vĩnh Tràng/v7_parts/` (Three.js). Nhiệm vụ của bạn CHỈ MỘT
VIỆC: **nâng toàn diện CHẤT LIỆU của toàn cảnh** để cảnh đọc như vật liệu thật
thay vì khối màu phẳng. Bạn không có Blender và không dựng hình — xem luật.

## LUẬT CỨNG (vi phạm bất kỳ điều nào = bản bị loại toàn bộ)

1. **TƯỢNG PHẬT TUYỆT ĐỐI TRANG NGHIÊM:** với mọi tượng Phật trong cảnh, chất
   liệu CHỈ được làm giàu BỀ MẶT (vân đá, phong hóa, rêu kẽ). CẤM sửa hình
   khối, tỉ lệ, vị trí, nét mặt tượng dưới mọi hình thức — hình tượng vừa được
   khóa bằng đo đạc ở vòng V15, không ai được động vào nữa.
2. Mọi chất liệu phải đối chiếu **ảnh thật chùa Vĩnh Tràng** và bảng màu khóa
   ở mục 3. Không tự chế màu "cho đẹp".
3. Giữ nguyên 3 model nhân vật chuẩn (GLB đã nhúng), giữ nguyên toàn bộ tính
   năng đang chạy: hành trình 9 trạm, nghi lễ, âm thanh, cửa hàng, Học viện.
   Không phá journey, không đổi gameplay, không thêm cơ chế game hóa (điểm,
   EXP, level, vòng quay, tiền ảo — bị cấm tuyệt đối trong dự án này).
4. **Không texture/CDN/nguồn ngoài.** Mọi texture phải sinh thủ tục trong code
   (canvas 2D) hoặc tính bằng shader/vertex color ngay trong repo.
5. **Chỉ làm trên nhánh `argon-chat-lieu-v9`.** TUYỆT ĐỐI không commit vào
   `main`. Nếu công cụ của bạn không cho chọn nhánh, ghi rõ điều đó ở đầu
   changelog thay vì tự ý ghi đè main.
6. Changelog trung thực: mục nào chưa xong ghi **CHƯA XONG**, không mô tả việc
   chưa làm như đã làm. Không để lại code debug/rác (console.log thử nghiệm,
   khối code chết) trong bản giao.

## BẢNG MÀU KHÓA (đo từ ảnh thật — dùng làm màu nền của vật liệu)

- Đá tượng: trắng ấm `#EFE9DD`; bệ đá `#6E675C`, chữ vàng trên bệ `#D9A441`
- Mặt tiền điện: vàng nghệ `#D9A441` (vùng tối `#B9852F`); cột sơn son `#7E2A22`;
  vàng điểm xuyết `#C9A227`; nội thất son `#8E2323` + thếp vàng `#C9A227`/`#E8C766`
  (vàng KHÔNG phát sáng/emissive)
- Mái ngói: nâu đỏ `#7C4030` (biến thiên `#6E382A`–`#8A4A34`)
- Đài sen A Di Đà: xanh `#4E86A8`, đế `#8A4A3A`
- Tháp: thân `#C88A4A`, mái tầng `#A85A38`
- Cổng tam quan: nền `#C9962E` + mosaic cobalt `#2C4A8A` / ngọc `#3F7D5D` /
  đỏ `#A03A2A` / sứ trắng `#E8E2D4`
- Nước hồ: `#4E5F3A`; sân lát: `#8A7A63`; lá cây: `#3E6B34`–`#5C8446`;
  hoa giấy: `#C93B6E`/`#D94F3D`; hàng rào: `#C9962E`; trời: `#0155C9`–`#4F97F9`

## PHẠM VI CHẤT LIỆU (làm đủ 8 nhóm)

1. **Đá trắng tượng** (chỉ bề mặt!): vân đá mịn (noise hạt nhỏ, tương phản
   thấp), vệt phong hóa chảy dọc rất nhẹ, rêu xanh xám ở kẽ/chân tượng, độ
   nhám cao (roughness 0,85–0,95), không bóng.
2. **Sơn son thếp vàng chánh điện:** son đỏ có chiều sâu (đậm ở khe, hơi mòn ở
   gờ), vàng thếp có vân lá vàng + biến thiên độ bóng (metalness vừa, roughness
   không đều theo mặt nạ), cột có vệt tay nắm mòn sáng ở tầm tay người.
3. **Vân gỗ** (cột kèo gỗ, nhà Tổ, cửa): vân gỗ thủ tục theo thớ dọc, mắt gỗ
   thưa, màu nâu gỗ cũ `#5A3D26` cho khu vực không thếp vàng; gỗ sơn son thì
   giữ đỏ theo bảng màu.
4. **Ngói âm dương + rêu mái:** từng hàng ngói đọc được (bump từ họa tiết
   hàng ngói), biến thiên màu giữa các viên, rêu xanh ở rãnh ngói và chân mái
   (đậm phía ít nắng), vệt nước chảy từ mép mái.
5. **Đồng** (chuông Pháp Bảo, lư hương sân, đỉnh đồng): đồng sẫm có patina
   xanh `#3F7D5D` loang ở kẽ và phần dưới, phần gờ hay chạm thì sáng hơn;
   metalness cao nhưng roughness biến thiên theo mặt nạ patina.
6. **Tường vôi cũ:** vôi vàng kem có vệt ố nước, chân tường sẫm + rêu nhẹ,
   nứt tóc rất thưa; không làm tường bẩn quá mức — chùa đang được chăm sóc.
7. **Gạch/đá sân mòn:** lát sân có mạch vữa đọc được, viên mòn bóng nhẹ ở lối
   đi chính (roughness thấp hơn theo dải đường đi), rêu ở mạch khu ít đi lại,
   vệt nước đọng sau mưa rất nhẹ ở vùng trũng.
8. **Nước hồ sen:** nước có gợn (normal thủ tục chuyển động chậm), phản chiếu
   trời theo góc nhìn (fresnel), mép nước sẫm, lá sen có vân lá + mặt trên/mặt
   dưới khác tông, hoa sen hồng `#EE7FAE` có chuyển sắc cánh.

## KỸ THUẬT ĐƯỢC PHÉP (môi trường code-only của bạn)

- Texture thủ tục bằng canvas 2D (vân đá, thớ gỗ, hàng ngói, patina, rêu,
  mạch lát) — sinh 1 lần lúc tải, dùng lại; kích thước vừa phải (≤1024) để
  không phình dung lượng bản dựng.
- Tinh chỉnh `roughness`/`metalness`/`bumpMap`/`roughnessMap` theo mặt nạ.
- Làm giàu vertex color ở những chỗ đang phẳng màu.
- Tinh chỉnh ánh sáng/môi trường nhẹ nếu giúp vật liệu đọc đúng hơn (không
  đổi tông tổng thể "sáng trong": trời cobalt, nắng sáng, exposure quanh 1,1).
- Mọi thay đổi nằm trong `v7_parts/` rồi lắp lại bản dựng bằng quy trình sẵn
  có của repo; bản dựng cuối phải là 1 file HTML tự chứa như hiện tại.

## KHÔNG LÀM

- Không nặn/sửa hình khối bất kỳ vật thể nào (đặc biệt là tượng — luật 1).
- Không đổi bố cục cảnh, vị trí trạm, tuyến di chuyển, nội dung bài học.
- Không thêm thư viện ngoài, không ảnh ngoài, không font ngoài.
- Không xóa hay viết lại tài liệu/báo cáo/checklist sẵn có trong repo.

## GIAO NỘP

- Nhánh `argon-chat-lieu-v9`, commit theo từng nhóm chất liệu (8 nhóm ở trên),
  mỗi commit ghi rõ nhóm nào.
- File `BAO_CAO_ARGON_V9.md` ở thư mục `Mô hình 3D Vĩnh Tràng/`: từng nhóm —
  đã làm gì, kỹ thuật nào, thông số chính; mục chưa đạt ghi CHƯA XONG + lý do.
- Bản dựng cuối phải mở chạy được ngay: hành trình đi đủ 9 trạm, không lỗi
  console, dung lượng không vượt quá ~19 MB.
