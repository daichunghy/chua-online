# KẾ HOẠCH TOÀN DIỆN V6 — Chùa Vĩnh Tràng tiến tới "giống thật"
Lập 07/11 sau đợt P0 (coordinator tự lập + tự duyệt theo ủy quyền của Chung Hy
03:27 ngày 07/11: "bạn tự duyệt plan mới rồi chạy thêm"). Chuẩn nghiệm thu duy
nhất: đối chiếu ảnh thật (refs/) + ảnh mẫu theme (image-48.png), đo bằng số —
không tự phong đạt theo cảm tính.

## Hiện trạng sau P0 (đã nghiệm thu bằng số + coordinator tự soi render)
ĐẠT: cột hết teal -> đỏ son (0% teal) · nước hồ hết cyan -> xanh rêu + phản
chiếu · mái tối hơn tường (0,71) · hốc vòm có AO (-33%) · 59 vật liệu PBR, hết
màu phẳng tuyệt đối · bảng chữ Di Lặc đọc đúng chiều.
CHƯA ĐẠT: vàng mặt tiền nhạt/kém bão hòa so với ref1 · trời xanh nhạt, chưa
cobalt, <3 tông · tán cây pastel bạc hà (gốc: model cây khối cầu) · nền ngoài
khuôn viên texture bẩn loang ở flycam · cổng còn 2 chốt trang trí lơ lửng + ô
gốm phẳng · nhân vật bị ám hồng theme lên nón + túi (LỖI MỚI do P0 — phải sửa
trước tiên).

## P1 — Sửa lỗi + nhận diện (chạy ngay sau P0)
1. FIX ám hồng: nón/túi 3 nhân vật về đúng màu gốc (nón rơm/trắng thêu sen, túi
   vải be) — kiểm vật liệu nào bị gán #EE7FAE nhầm, tách riêng vật liệu cánh
   hoa giấy. Nghiệm thu: render ground, nón/túi không còn pixel hồng bão hòa
   (đo vùng nón: hue ngoài vùng hồng), hoa giấy (nếu có trong khung) vẫn hồng.
2. Vàng mặt tiền: sâu albedo tường về #D9A441 (giữ PBR vữa + variation), nghiệm
   thu đo lại: lệch ≤ ±12/kênh so với đích ở vùng tường nắng.
3. Trời cobalt: thay HDRI bằng trời nắng cao nhiệt đới thuần (hoặc vòm trời
   gradient + mây), sửa luôn ám hoàng hôn hướng nam ở góc Di Lặc. Nghiệm thu:
   vùng trời ≥3 tông + hue xanh dương rõ (đo histogram), không còn tông ấm ở
   góc Di Lặc.
4. Cổng tam quan: photo-texture/decal cẩn sứ từ ref6 cho mặt cổng + gắn lại 2
   chốt trang trí đang lơ lửng trên xà. Nghiệm thu: render góc cổng đặt cạnh
   ref6 — đọc được mảng sứ đa sắc, không vật thể bay.
5. Nền đất: chỉnh scale tiling + giảm loang bẩn của texture nền ngoài khuôn
   viên; sân trong về gần đích #8A7A63 (lệch ≤ ±12). Nghiệm thu: đo lại vùng
   sân như bảng B đặc tả V5 + flycam không còn loang nâu xám chiếm khung.
6. AO pass qua compositor (khắc phục socket Blender 5) hoặc tăng AO texture —
   nghiệm thu: hốc vòm/chân tượng tối bền ở cả 4 góc render.
7. Render kiểm chứng bảng chữ A Di Đà + Phật nằm (dữ liệu đã sửa ở P0, chưa có
   render riêng): chữ đọc đúng chiều, không magenta.

## P2 — Mật độ & đời sống (sau P1 đạt)
1. Thay cây khối cầu: cây lá card alpha (tàu lá/cọ + tán lá texture CC0), ≥3
   tông xanh, variation theo instance; thêm hoa giấy hồng leo quanh cổng +
   chánh điện + quanh tượng (điểm màu bắt buộc theo đặc tả), bonsai đúng vị trí
   ref1.
2. Hàng rào vàng chạy kín chu vi khuôn viên (ref9/ref14); bờ hồ đá hoàn chỉnh.
3. Scatter chi tiết sân: chậu cây, lá rụng, đá, ghế đá, biển chỉ dẫn (Phương
   Tiện/Tịnh Độ), thùng công đức ở đúng vị trí audit.
4. Người: tăng số khách hành hương trong sân (dùng 3 nhân vật đã fit + biến thể
   màu áo), vài người chắp tay/quỳ đúng trạm S2/S3.
5. Nền ngoài khuôn viên: hàng cây xa + đường vào + cổng phụ thứ hai rõ hơn.

## P3 — Bóng bẩy (sau P2 đạt)
1. Weathering: vệt nước chân tường, rêu mép mái/hồ bằng mask noise.
2. Grade cuối: fog nhẹ + vignette ấm theo audit D; bản render "16h30" và bản
   "sáng trong" để Chung Hy chọn tông chính.
3. Chuẩn bị đưa sang web: xuất bản nhẹ (decimate + texture 1K) cho scene web v4
   dùng cùng palette; theme UI theo THEME_CHUA_ONLINE.md.

## Nguyên tắc xuyên suốt
- Mỗi đợt: render đúng các góc chuẩn (flycam/ground/cổng/Di Lặc) + đo số theo
  tiêu chí của đợt; coordinator tự soi trước khi báo; mục chưa đạt ghi rõ, sửa
  tiếp trong đợt sau — không giấu, không báo đạt sớm.
- Chỉ render khi máy rảnh (ưu tiên video final), một render một lúc.
- File chuẩn: layout_v5_p0.blend -> P1 lưu layout_v6_p1.blend (không ghi đè).
