# Checklist ghép bố cục tổng thể Vĩnh Tràng bằng tài sản thật

Nguyên tắc: chỉ dùng tài sản đã kiểm chứng; không khối thô tự chế (bản V2 khối thô đã bị Chung Hy bác 22:52 ngày 05/11). Render chỉ tính đạt khi đặt cạnh ảnh flycam thật (refs/ref9.jpg, refs/ref14_int_c.jpg) mà đọc ra đúng chùa.

## Tài sản đầu vào (đã kiểm chứng)
- Chánh điện: model cửa vòm chi tiết nhuộm vàng — output của scripts/facade_v3.py (local facade-v3e.blend), 13 ô vòm, cột gốm xanh, song vàng.
- Tượng (statues/verified_v2/, GLB): phat-dung-adida (11,03m cả bệ), di-lac (7,89m), phat-nam (5,33m), phat-ngoi-ban-tho (2,86m — đặt trong nội điện, không ra sân).
- Nhân vật mặc vật phẩm: scripts/items_worn.py (3 nhân vật, đã đạt).
- Vật phẩm tĩnh đã sửa: repo-items/fixed/*.glb — CHỈ dùng món đã qua render kiểm chứng của tuyến vật phẩm.
- Cổng tam quan, tháp 7 tầng, hồ, hàng rào vàng: TRÍCH từ model tổng có sẵn của repo (bo-cuc-theo-anh.blend / chua_vinh_trang_full.blend), không dựng mới bằng hình cơ bản. Nếu trích không sạch thì ghi nợ rõ ràng, không thay bằng khối thô.

## Vị trí khóa theo ảnh flycam thật
- [ ] 2 cổng tam quan ở hai đầu phía trước
- [ ] Hồ phía trước, hàng rào vàng bao quanh
- [ ] Tượng Phật đứng trắng khổng lồ đài sen XANH ở góc trước–trái, cạnh hồ/cổng (tượng lớn nhất cảnh)
- [ ] Chánh điện bên PHẢI, mái ngói đỏ nâu lớn phía sau mặt tiền vàng
- [ ] Di Lặc ở trái–giữa
- [ ] Tháp 7 tầng phía sau, trung–trái
- [ ] Phật nằm phía sau, trung–phải, trên bệ đá cao

## Kiểm chứng trước khi báo đạt
- [ ] Render Cycles góc flycam tương đương ref9 + một góc mặt đất tương đương ref1
- [ ] Đặt cạnh ref9/ref14: đủ 7 mốc vị trí trên, không thừa khối lạ
- [ ] Mái chánh điện là khối mái thật (hồi/đỉnh + hàng ngói đọc được), không phải dải phẳng
- [ ] Màu: vàng bão hòa của chánh điện, trắng tượng, xanh đài sen — khớp ảnh thật
- [ ] Đẩy repo: file chữ qua MCP; file nhị phân (render/GLB) qua giao diện web GitHub — TUYỆT ĐỐI không đẩy nhị phân qua MCP (bài học 06/11)
