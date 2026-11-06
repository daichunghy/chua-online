# Sửa 15 vật phẩm repo — FIX_NOTES

Ngày sửa: 2026-11-06 (đêm) · Script: `fix_props.py` · Đầu ra: `fixed/<item>.glb`
Đối chiếu: `VERIFY_NOTES.md` (chẩn đoán gốc, không sửa) + `danh_muc_vat_pham.json` (kích thước catalog)

## Trạng thái kiểm chứng — ĐỌC TRƯỚC

- **Đã làm & đã kiểm chứng ở mức HÌNH HỌC:** sửa normals, sửa hình học theo từng chẩn đoán, rescale về catalog, export GLB, và **đo lại trực tiếp trên file GLB đã export** (parse accessor POSITION, cả tổng thể lẫn từng node — không còn node phình/lỗi). Số đo trong bảng dưới là số đo thật từ GLB.
- **KIỂM CHỨNG BẰNG RENDER — ĐÃ XONG 2026-11-06 (đêm, sau khi CPU được mở):** chạy `fix_props.py` (không đặt `FIX_RENDER=0`) render Cycles 32 samples 720×720 từng món, soi từng hình. Kết quả cuối: **15/15 PASS** (4 món cần vòng sửa thêm sau render đầu: xem bảng verdict render bên dưới). Không món nào còn FAIL.
- **CHƯA push binary lên GitHub:** quy tắc đẩy file qua GitHub MCP — `create_or_update_file` / `push_files` chỉ lưu được TEXT; truyền base64 của GLB/PNG vào thì repo chứa nguyên văn chuỗi base64, file hỏng mà push vẫn báo thành công (bài học 06/11: 13 render JPG đã hỏng kiểu này). **15 GLB + 15 PNG kiểm chứng chỉ nằm LOCAL** tại `repo-items/fixed/` và `repo-items/fixed_<item>.png` — phải tải lên bằng giao diện web GitHub (Add file → Upload files). Chỉ file TEXT (FIX_NOTES.md, fix_props.py) được đẩy qua MCP.

## Bảng verdict render (Cycles 32, 720×720, soi từng hình)

| # | Vật phẩm | Verdict render | Ghi chú chính |
|---|----------|----------------|---------------|
| 1 | mo_go_tung_kinh | PASS (marginal) | Dùi ráp lại đúng; miệng mõ là dải tối khối, gỗ màu hồng nhạt |
| 2 | bat_nhang_tram | PASS | Đồng sâu màu, mặt tro sạch; nén thứ 3 khuất sau, chỉ 1 đầu than phát sáng |
| 3 | nen_hoa_sen | PASS | Nến + lửa + 8 cánh sen cong; lửa hơi nhỏ, cánh hơi thưa |
| 4 | den_hoa_dang | PASS (marginal) | Nến lộ giữa 2 vòng cánh; đế xanh là phiến vuông, đọc như gạch |
| 5 | mam_ngu_qua | PASS (sau 2 vòng sửa) | Vảy thanh long từng bay khỏi trái (xoay sau bake); chùm sung từng rớt dưới mâm — đã sửa, dims về đúng 360×360×160 |
| 6 | bo_doan_dai_sen | PASS (marginal, sau 1 vòng sửa) | Cánh sen xám-nâu chìm vào gối → đổi hồng + đặt lên mặt gối; vẫn hơi mỏng |
| 7 | bo_doan_tron | PASS | Gối tròn vải bố + gân + tag; sạch |
| 8 | chieu_coi_thien | PASS (marginal) | Đúng tỉ lệ; vân đan bump không đọc ở cự ly studio |
| 9 | dia_banh_bo | PASS | 5 bánh vòm + dừa sợi; mặt tổ ong đọc yếu |
| 10 | dia_banh_da_lon | PASS | 4 lát, đủ 5 lớp màu bóng |
| 11 | trai_dua_xiem | PASS | Dừa xanh + ống hút tre; ống hút đứng thẳng thay vì nghiêng |
| 12 | quat_nan_la_dua | PASS (marginal) | Quạt đọc đúng dáng; nan đan nhạt, cánh đọc như phiến trơn |
| 13 | gio_may_tre | PASS (sau 1 vòng sửa) | Quai từng đứt thành 15 vạch dọc — do bake() đọc matrix_world cũ, mất rotation; đã vá, quai liền mạch |
| 14 | chum_sanh_hoa_sen | PASS (sau 4 vòng sửa) | Xem chi tiết bên dưới — món khó nhất |
| 15 | den_long_luc_giac | PASS | Mặt lụa vàng hiện, móc treo có; tua rua chỉ là hạt đỏ, đáy hơi lệch |

### chum_sanh_hoa_sen — 4 vòng render mới đạt
1. Vòm đất trong miệng chum (thân chum tự lồi, đỉnh z 0.48) chôn đĩa nước — chỉ lộ viền xanh + chấm hồng.
2. San phẳng vòm, sen nới 1.9× — thành bánh hồng dẹt, đĩa nước trồi khỏi vai chum như nắp.
3. Sen 1.5×/1.2z, nước thu 0.88× — búp đỡ dẹt nhưng vẫn là vòm trơn không cánh; đĩa nước vẫn trồi.
4. (Theo lệnh coordinator) cổ trụ đặc bịt miệng lại + lá xoay sau bake bay ra ngoài (dims 579×712) — 2 lỗi mới trong 1 vòng.
5. Bỏ cổ trụ (chỉ giữ vành torus), lá nghiêng đặt trong operator, búp dựng lại bằng vòng cánh nón của búp sen nhân vật (5@32°/4@18°/3@8° + đài xanh) — **PASS**: chum đất + vành miệng + mặt nước xanh + sen hồng có cánh + lá nghiêng. Dims 480×480×494.

## Lỗi chung phát hiện thêm trong lúc render (đã vá trong fix_props.py)

- **bake() đọc matrix_world cũ:** ở background mode, rotation đặt trên object chưa cập nhật vào matrix_world cho tới khi view layer update — `bake()` biến mọi tube thành trụ đứng (quai giỏ thành 15 vạch). Đã vá: `bake()` gọi `view_layer.update()` trước.
- **Xoay SAU khi bake = xoay quanh gốc thế giới:** `cone()`/`disc()` bake ngay trong hàm; gán `rotation_quaternion`/`rotation_euler` sau đó xoay vật quanh (0,0,0) — vảy thanh long bay khỏi trái, lá sen chum bay ra hông chum. Quy tắc: rotation phải đặt trong operator call hoặc trước `bake()`.

## Lỗi chung đã xử lý (cả 15 món)

- Xoá custom split normals hỏng, tính lại shading từ hình học (smooth-by-angle) — hết lỗi render đen.
- Gán lại Principled materials sane từ màu Kd phẳng của MTL (roughness 0.62 mặc định); thêm emission nơi vật phẩm có lửa/ánh sáng: lửa nến sen (2.5), lõi đèn hoa đăng (2.2) + cánh giấy (0.22), mặt lụa đèn lồng (0.55), điểm than bát nhang (1.6); đồng cổ bát nhang sâu màu (0.45, 0.30, 0.15) metallic 0.7; chỉ thêu vàng bồ đoàn + viền vàng mâm ngũ quả metallic 0.8–0.85.

## Bảng kết quả (số đo từ GLB đã export, mm)

| # | Vật phẩm | Catalog | GLB thực tế | Lệch | Verdict |
|---|----------|---------|-------------|-------|---------|
| 1 | mo_go_tung_kinh | 240×240×200 | 240×240×200 | 0% | Đạt hình học — chờ render |
| 2 | bat_nhang_tram | 180×180×320 | 180×180×320 | 0% | Đạt hình học — chờ render |
| 3 | nen_hoa_sen | 140×140×100 | 139×139×100 | −0.7% | Đạt hình học — chờ render |
| 4 | den_hoa_dang | 200×200×80 | 200×200×80 | 0% | Đạt hình học — chờ render |
| 5 | mam_ngu_qua | 360×360×160 | 360×360×160 | 0% | Đạt hình học — chờ render |
| 6 | bo_doan_dai_sen | 450×450×120 | 452×452×117 | +0.4/−2.5% | Đạt hình học — chờ render |
| 7 | bo_doan_tron | 400×400×100 | 441×402×100 | x +10%* | Đạt hình học — chờ render |
| 8 | chieu_coi_thien | 800×1600×14 | 810×1610×14 | ≈+1% | Đạt hình học — chờ render |
| 9 | dia_banh_bo | 280×280×70 | 280×280×73 | cao +4.3% | Đạt hình học — chờ render |
| 10 | dia_banh_da_lon | 280×280×60 | 280×280×59 | −1.7% | Đạt hình học — chờ render |
| 11 | trai_dua_xiem | 180×180×260 | 180×180×257 | −1.2% | Đạt hình học — chờ render |
| 12 | quat_nan_la_dua | 280×20×380 | 280×21×380 | dày +5% | Đạt hình học — chờ render (dựng lại từ đầu) |
| 13 | gio_may_tre | 340×280×360 | 346×290×360 | +1.8/+3.6% | Đạt hình học — chờ render |
| 14 | chum_sanh_hoa_sen | 480×480×500 | 480×480×500 | 0% | Đạt hình học — chờ render |
| 15 | den_long_luc_giac | 440×440×520 | 440×417×540 | sâu −5.2%**, cao +3.8% | Đạt hình học — chờ render |

\* bo_doan_tron: phần nở +10% ở trục x là mẩu tag vải thò bên hông (có trong file gốc); thân gối đúng Ø400.
\** den_long: 417 là khoảng cách hai mặt phẳng đối diện của lục giác — file gốc cũng 416; 440 của catalog ứng với khoảng cách hai đỉnh đối diện (trục x đạt đúng 440).

## Đã sửa gì từng món

1. **mo_go_tung_kinh** — Dùi rời rạc đã ráp lại: đầu nỉ đỏ gắn vào đầu cán, thu ngắn 0.88×, đặt nằm trên gối phía trước mõ (ma trận xoay dựng từ vị trí cán gốc). Toàn bộ về đúng 240×240×200 (trước +22/+30/+21%).
2. **bat_nhang_tram** — Xoá mặt tro lỗi sao, thay đĩa tro tròn sạch; phát hiện 1 cán hương bị gán nhầm material than cháy (DiemThanRuc cho cả cán) → gán lại ChanHuongDo, chỉ chừa đầu than phát sáng; đồng cổ sâu màu metallic 0.7; scale (0.918, 0.918, 0.988) về đúng catalog.
3. **nen_hoa_sen** — Xoá 8 "cánh" hộp chữ nhật, thay vòng 8 cánh sen cong (petal builder: cánh thuôn, cup, cong đầu, solidify) quanh nến; lửa có emission; scale về 139×139×100.
4. **den_hoa_dang** — Xoá 12 cánh hộp đứng, thay 2 vòng cánh cong xoè thấp (8 cánh ngoài lean 68°, 6 cánh trong lean 38°) để lộ nến giữa; nến/lửa kéo cao về đúng 80; lửa + cánh giấy có emission ấm.
5. **mam_ngu_qua** — Xoá 4 trái cầu/nón trơn (đu đủ, mãng cầu, dừa, xoài), dựng lại: bưởi xếp chồng 2 tầng (chiều cao đủ 160), mãng cầu gai (icosphere jitter), thanh long hồng + 16 vảy xanh, cam có núm, chùm chuối 6 nải cong (cầu xếp theo cung), chùm sung giữ nguyên nhưng dời ra trước. Đĩa + viền vàng scale về 360.
6. **bo_doan_dai_sen** — Xoá 8 khối hộp thò quanh thân, thay 8 cánh sen cong ôm sườn; vòng chỉ thêu hở chữ C → torus vàng metallic khép kín trên mặt; thân scale về Ø~430 để tổng cả cánh = 452.
7. **bo_doan_tron** — Chỉ sửa normals (món sạch nhất, đúng chẩn đoán).
8. **chieu_coi_thien** — Thêm vân đan bằng bump checker thủ tục (ảnh 256² tự sinh, mapping lặp 7×14) trên mặt cói qua UV smart-project; kích thước giữ nguyên (≈chuẩn từ gốc).
9. **dia_banh_bo** — Jitter đỉnh vòm bánh (gợi mặt tổ ong) + 35 sợi dừa trắng mỏng rải trên mặt 5 bánh.
10. **dia_banh_da_lon** — Xoá khối 3 lớp/2 màu, dựng 4 lát bánh, mỗi lát đủ 5 lớp màu (lá dứa, dừa trắng, đậu xanh, tím, hồng), glossy roughness 0.25, xếp quạt trên đĩa.
11. **trai_dua_xiem** — Cắt đáy cầu, gắn đĩa đáy phẳng (đứng vững, không lăn); kéo chiều cao 300 → 257 (catalog 260).
12. **quat_nan_la_dua** — HỎNG ở bản gốc → dựng lại từ đầu: thân quạt hình elip 280×260 có gợn sóng nhẹ + solidify, 11 nan toả từ cán, 2 sợi đan ngang, cán tre thuôn; đúng catalog 280×20×380.
13. **gio_may_tre** — Xoá toàn bộ cụm vành + đĩa bịt miệng + quai gãy (island nổi phía trên); thêm vành torus, đĩa tối bên trong (giỏ rỗng thật), quai mới = cung 15 đoạn ống nối cả hai bên vành; scale oval 340×280, chiều cao ép đúng 360 (trước −36%).
14. **chum_sanh_hoa_sen** — Xoá đảo vòm đất bịt miệng (320 mặt); hoa sen có sẵn trong file được nâng +25mm để nổi rõ trên mặt nước (đỉnh hoa = 500 đúng catalog); thêm 2 lá sen nổi trên mặt nước.
15. **den_long_luc_giac** — Thân đặc một khối → dựng lại khung lục giác thật: 6 cột góc + 6 mặt lụa vàng phát sáng nhẹ lọt giữa khung, vành trên/dưới; thêm dây treo + móc; tua rua trụ trơn → bead + chùm nón sợi; gốc toạ độ hết chìm −140mm (min z = 0).

## Ghi chú kỹ thuật cho lần render sau

- `fix_props.py` chạy được từng món: `blender -b --factory-startup -noaudio --python fix_props.py -- <item>`; đặt `FIX_RENDER=0` để bỏ qua render. Render dùng đúng studio setup của `verify_one.py` (Cycles 32, 720×720) và ghi `fixed_<item>.png`.
- Bài học đã vá trong script: KHÔNG dùng `ob.dimensions =` trong background mode (bound box chưa cập nhật → hộp ở lại 1×1×1 m; phát hiện nhờ parse GLB theo node). `box()` nay dựng từ from_pydata. Đo chiều cao giỏ phải đo từ đỉnh thật (vert_bbox), bound_box của ống cong báo sai.
- File gốc OBJ/MTL không bị đụng vào; mọi sửa chữa nằm trong `fix_props.py` + GLB ở `fixed/`.
