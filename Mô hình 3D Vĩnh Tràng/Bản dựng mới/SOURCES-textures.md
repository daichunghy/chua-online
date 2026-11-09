# NGUỒN ASSET — thư mục textures/ (đợt P0 "giống thật", 07/11/2026)

Tất cả asset tải từ **Poly Haven** (polyhaven.com) — giấy phép **CC0 1.0** (public domain,
dùng thương mại không cần ghi công; vẫn ghi ở đây để truy vết). Tải qua API chính thức
`api.polyhaven.com`, độ phân giải 1K JPG cho texture, 2K HDR cho HDRI. File gốc tải về
nằm ở `dl/` (kèm `dl/hdris.json`, `dl/textures.json` là metadata API tại thời điểm tải);
bản dùng trong Blender đã chép ra thư mục này với tên ngắn.

| File trong textures/ | Asset Poly Haven | Loại |
|---|---|---|
| sky_late_afternoon_2k.hdr | `qwantani_late_afternoon_puresky` | HDRI trời nắng chiều (world E1) |
| plaster_diff/nor/rough/ao.jpg | `painted_plaster_wall` | Vữa sơn — tường vàng, trim, cột đỏ, tượng trắng |
| rooftiles_diff/nor/rough/ao.jpg | `clay_roof_tiles_02` | Ngói đất — mái chánh điện, mái tháp, viền đỏ |
| paving_diff/nor/rough/ao.jpg | `brick_pavement_02` | Gạch lát — sân, nền đất lớn |
| concrete_diff/nor/rough/ao.jpg | `chipped_concrete` | Bê tông/đá sứt — bệ tượng, thành hồ, đá xám |
| wood_diff/nor/rough/ao.jpg | `dark_wooden_planks` | Gỗ tối — cửa, khung, thân cây |
| metal_diff/nor/rough/ao.jpg | `metal_plate` | Kim loại — song sắt cửa (tô tối #2B2320) |

Ghi chú kỹ thuật: trong Blender các map được chiếu **BOX projection theo Object
coordinates** (không phụ thuộc UV của mesh dựng thủ công), normal map được dùng qua
**Bump** (lấy từ diffuse) để tránh lỗi tangent khi không có UV chuẩn — xem script
`layout/build_p0.py`. Màu đích theo bảng B của `NGHIEN_CUU_GIONG_THAT_V5.md` đạt bằng
cách nhân (multiply) tint sRGB lên albedo texture.
| sky_bright_day_2k.hdr | `kloppenheim_02` | HDRI ban ngày sáng, trời xanh có mây (art direction THEME_CHUA_ONLINE.md, chốt 04:42 07/11) |
| sky_blue_clear_2k.hdr | `kloppenheim_06_puresky` | HDRI trời xanh trong (vá vòng 5: thay kloppenheim_02 bị nhiễu đốm + xám ở góc cổng) |
| forest_leaves_diff.jpg | `forest_leaves_02` (Poly Haven, CC0) | Lá rụng phủ đất — card scatter P2 (diffuse 1K) |

**Texture tự tạo bằng PIL (đợt P2, 07/11/2026 — tài sản của dự án, không phải của bên thứ ba):**
`leaf_cluster_A/B/C.png` (cụm lá alpha cho tán cây card — 3 tông #3E6B34/#4C7A3C/#5C8446),
`palm_frond_A/B.png` (tàu lá cọ alpha), `bougainvillea.png` (cụm hoa giấy hồng #EE7FAE/#C93B6E),
`sign_phuong_tien.png`, `sign_tinh_do.png`, `cong_duc_front.png` (chữ vàng trên gỗ sẫm, DejaVu Serif Bold).
Sinh bởi `layout/gen_p2_textures.py`. Poly Haven không có atlas lá alpha (chỉ có texture mặt đất
không trong suốt) nên tán cây dùng texture tự vẽ theo thủ tục — đây là lựa chọn kỹ thuật của đợt P2.
