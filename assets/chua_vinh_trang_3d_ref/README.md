# BỘ TƯ LIỆU HÌNH ẢNH THAM KHẢO DỰNG HÌNH 3D CHÙA VĨNH TRÀNG (MỸ THO - TIỀN GIANG)

Bộ dữ liệu này được thu thập và phân loại chuyên biệt nhằm phục vụ quy trình dựng hình 3D (3D Modeling), tái tạo quang trắc (Photogrammetry), Gaussian Splatting hoặc tạo Texture PBR cho dự án **Chùa Online**.

## 1. Thống Kê Tổng Quan
- **Tổng số hình ảnh thu thập được:** 165 files
- **Định dạng:** JPG, PNG, WEBP (Đã kiểm tra tính toàn vẹn và độ phân giải)
- **Nguồn:** Wikimedia Commons (Tư liệu gốc 4K - 6K Ultra HD) + Kho ảnh thực địa góc đa chiều

## 2. Phân Bổ Các Thư Mục Chuyên Môn
| Thư mục | Hạng mục | Số lượng ảnh | Mục đích ứng dụng 3D |
| :--- | :--- | :--- | :--- |
| `01_chanh_dien_mat_tien/` | Mặt tiền Chánh điện | 52 | Dựng khối nhà chính, vòm cong Phục Hưng, cột La Mã, hoa văn mái |
| `02_cong_tam_quan/` | Cổng Tam Quan | 18 | Dựng cổng tam quan, trích xuất texture khảm sành sứ (mosaic) |
| `03_dai_tuong_di_lac/` | Tượng Phật Di Lặc | 20 | Điêu khắc số (sculpting) tỷ lệ cơ thể, nét mặt hoan hỷ, bệ sen |
| `04_dai_tuong_a_di_da/` | Tượng Phật A Di Đà (24m) | 18 | Dựng tượng Phật đứng, nếp gấp áo cà sa, đài sen, vòng hào quang |
| `05_tuong_phat_nam/` | Tượng Phật Nhập Niết Bàn (35m) | 16 | Dựng tượng Phật nằm nghiêng, gối kê đầu, bệ nằm |
| `06_noi_dien_tam_bao/` | Nội điện & Bàn thờ | 23 | Dựng không gian nội thất, tượng gỗ cổ, bao lam chạm trổ, hoành phi dát vàng |
| `07_khuon_vien_thap_mo/` | Khuôn viên & Vườn tháp | 18 | Dựng environment, terrain, vườn tháp tổ, hồ sen, cây cảnh bonsai |
| `08_wikimedia_ultra_hd/` | Master Ultra HD (4K-6K) | 54 | File gốc độ phân giải cực cao (lên tới 6000x4000) để làm UV Mapping & PBR Texture |

## 3. Khuyến Nghị Kỹ Thuật Khi Dựng 3D
1. **Phong cách kiến trúc giao thoa:** Chùa Vĩnh Tràng kết hợp 5 nền văn hóa: Pháp (vòm cửa, cột tròn), La Mã (hàng hiên), Thái Lan (tháp nhọn chánh điện), Campuchia (chạm nổi Khmer) và Việt - Hoa (mái ngói âm dương, khảm sành sứ). Khi dựng mesh cần chia rõ phần khung Gothic/Renaissance và phần mái trang trí Đông phương.
2. **Nghệ thuật khảm sành sứ Cổng Tam Quan:** Không nên dựng polygon quá dày cho từng mảnh gốm; nên dựng mesh chuẩn hình khối rồi sử dụng Normal Map kết hợp Roughness Map tạo độ bóng men sứ.
3. **Bộ 3 Đại tượng Phật lộ thiên:**
   - **Tượng Phật Di Lặc:** Tượng thạch cao màu trắng ngà bóng mờ.
   - **Tượng Phật A Di Đà:** Tượng bê tông cốt thép sơn trắng, cao 24m (tính cả bệ).
   - **Tượng Phật Niết Bàn:** Dài 35m, bệ bê tông ốp đá trang trí.
