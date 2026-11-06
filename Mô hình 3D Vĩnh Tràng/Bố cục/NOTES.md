# Layout V3 — bố cục tổng thể Vĩnh Tràng (ĐẠT, có ghi nợ)

Script: `layout_build_v3.py` (base `repo-khuonvienchanhdienmoi.blend` + cổng/hồ/đường
từ `repo-khuonvienvinhtrang.blend`, tượng `statues/verified_v2/`, vật phẩm
`repo-items/fixed/`, nhân vật `characters_fitted/` — xem `items_worn_export.py`
để biết cách xuất nhân vật đã fit). File: `layout_v3.blend` (31,9MB).
Render: `layout_flycam.png` (Cam_Flycam), `layout_ground.png` (Cam_Ground) — Cycles 32 mẫu.

## Kết quả kiểm chứng (so với refs/ref9.jpg, ref14_int_c.jpg, ref1_front.jpg)

FLYCAM — ĐẠT: chánh điện bên phải mái ngói đỏ nâu lớn (mái hông thật, có hàng ngói),
tháp 7 tầng sau trung-trái, Di Lặc trái-giữa trên bệ đá sẫm, Phật nằm sau trung-phải
(đầu hướng tây), A Di Đà đứng đài sen xanh góc trước-trái, 2 hồ cảnh + 2 cổng tam
quan phía trước, lối đi chính + hàng bồn cây, nền đất xanh bao quanh.
MẶT ĐẤT — ĐẠT: 13 ô vòm + song vàng + cột gốm xanh + vàng bão hòa khớp ref1; mái
là khối đặc (không còn khe hở); 3 nhân vật (nữ/nam/trẻ em, nón + túi + tràng hạt,
pose Chắp tay) đứng trên thềm hướng về chánh điện.

Lưu ý: render flycam cuối ẩn 3 nhân vật (chỉ ~5px ở tỉ lệ đó; nhân vật đã kiểm
chứng trong render mặt đất) để vừa RAM khi render v41 chạy song song — file
`layout_v3.blend` vẫn chứa đủ nhân vật.

## Ba lỗi đã tìm ra + sửa trong quá trình làm
1. **Mặt phẳng studio `Ground`/`Ground.001`/`Ground.002`** do GLB tượng mang theo
   (nằm ở z~1,6) che toàn bộ mặt đất/hồ/sân — phát hiện bằng raycast khi hồ không
   hiện dù đã nâng z. Đã xóa trong script build (2 chỗ). Bài học: GLB nào cũng có
   thể mang "đồ studio" theo — kiểm tra tên object lạ sau mỗi lần import.
2. **Nhân vật lệch gấp đôi tọa độ** (20,-8 → 40,-16, đứng giữa hồ): `matrix_world`
   còn stale ngay sau import nên phép xoay quanh điểm neo tính trên ma trận
   identity. Đã sửa: `view_layer.update()` sau import + sau khi dịch chuyển.
3. **Hàng ngói tách khe hở nhìn xuyên trời** ở góc mặt đất (tia nhìn qua khe đi
   qua nóc mái): đổi hàng ngói thành chồng mí (rộng 1,7 > khoảng cách 1,5).
   Ngoài ra: hồ z-fight với sân → nâng +0,08; camera clip_end 100 → 500;
   bệ Di Lặc tách vật liệu riêng màu đá sẫm.

## Nợ / giới hạn đã ghi (không giấu)
- Hàng rào vàng bao quanh: repo KHÔNG có model hàng rào chu vi (chỉ có lan can thềm
  chính điện) → 2 cổng đứng lẻ, chưa có tường rào nối. Ghi nợ, không tự chế.
- Cây xanh xung quanh thưa (122 tán + 26 thân, tập trung quanh chánh điện/tháp) —
  ảnh thật là rừng cây rậm bao quanh. Không thêm cây giả.
- Mái chánh điện là mái hông dựng trong script (repo không có khối mái lớn thật;
  'Mái ngói phía sau' trong file gốc chỉ là dải phẳng 0,96m ở mặt đất, đã xóa).
- Mặt tượng vẫn trơn như đã ghi ở vòng 2 (giới hạn điêu khắc tay).
- `layout_v3.blend` 31,9MB > giới hạn 25MB/file của giao diện web GitHub → chỉ
  giữ local; render PNG + GLB nhân vật (17-18MB) vẫn tải lên web được.
- Render song song 2 job Cycles trên VM 8GB có thể bị OOM-kill (đã gặp 1 lần ở
  flycam, exit 137) — render nặng chạy 1 job tại một thời điểm.

## Checklist 7 mốc (đánh giá cuối)
- [x] 2 cổng tam quan hai đầu phía trước
- [x] Hồ phía trước (2 hồ đọc rõ); [ ] hàng rào vàng — KHÔNG CÓ asset
- [x] Tượng Phật đứng trắng đài sen xanh góc trước-trái (lớn nhất)
- [x] Chánh điện bên phải, mái ngói đỏ nâu lớn
- [x] Di Lặc trái-giữa
- [x] Tháp 7 tầng phía sau trung-trái
- [x] Phật nằm phía sau trung-phải, trên bệ cao
