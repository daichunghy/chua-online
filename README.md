# Chùa Online (Online Pagoda)

> Hệ thống không gian 3D Chùa Vĩnh Tràng, mô hình vật phẩm chuẩn Coohom, nhân vật Phật tử và giáo trình Phật học trực tuyến.

---

## 🏛️ Tổng Quan Dự Án

Dự án **Chùa Online** được xây dựng nhằm mang lại trải nghiệm chiêm bái, tu học và tiếp cận giáo lý Phật giáo một cách trực quan, khoa học và chánh niệm trên nền tảng kỹ thuật số:

1. **Không gian 3D Chùa Vĩnh Tràng (Mỹ Tho - Tiền Giang):**
   - Mô phỏng kiến trúc giao thoa Đông - Tây độc đáo (5 vòm cuốn La Mã, hàng hiên Phục Hưng, mái đao và tháp Angkor).
   - Tái hiện Chánh điện, Cổng Tam quan, các cụm tượng Phật lộ thiên (Phật Di Lặc, Phật A Di Đà, Phật Niết Bàn) và không gian nội điện.
   - Hỗ trợ tương tác dâng hương, lạy Phật, thắp đèn Dược Sư và thỉnh pháp bảo.

2. **Hệ thống nhân vật & vật phẩm 3D:**
   - 3 tạo hình nhân vật Phật tử (Nam 1.74m, Nữ 1.62m, Trẻ em 1.15m) trong trang phục áo tràng, nón lá, túi sen.
   - Chuyển động thiền hành, dâng hương và tương tác sân chùa.
   - Bộ 20 vật phẩm thờ cúng chuẩn xuất Coohom (.obj, .mtl, .glb).

3. **Giáo trình Phật học tương tác:**
   - Nội dung học chánh kiến, Tam Bảo, Ngũ Giới, Tứ Diệu Đế, Bát Chánh Đạo.
   - Giao diện bài học thanh nhã, tối giản, quy chuẩn font Calibri sắc nét.

---

## 📂 Cấu Trúc Thư Mục

```text
├── index.html                       # Hub điều hướng toàn bộ không gian & mô hình 3D
├── Mô hình 3D Vĩnh Tràng/           # Dự án 3D kiến trúc chùa (Blender, Three.js, Vite)
│   ├── trai-nghiem-chua-vinh-trang-3d.html
│   ├── chua_vinh_trang_blender.glb
│   └── Bản dựng mới/
├── Thiết kế giao diện/              # Thiết kế UI & hệ thống mô hình 3D
│   ├── Nhân vật 3D/                 # Mô hình GLB nhân vật nam, nữ, trẻ em & hoạt ảnh
│   ├── Vật phẩm 3D/                 # 20 vật phẩm thờ cúng & gói Coohom
│   └── Giảng đường 3D/              # Không gian lớp học Phật pháp
├── Giáo trình phật học/             # Tài liệu, PDF giáo trình nền tảng
├── Định hướng sản phẩm/             # Biên bản nghiên cứu & định hướng tính năng
├── assets/                          # Kho tư liệu ảnh thực địa & Ultra HD tham khảo
└── scripts/                         # Các script tự động hóa Blender Python
```

---

## 🚀 Trải Nghiệm Nhanh

Mở trực tiếp file `index.html` trên trình duyệt web hoặc chạy máy chủ tĩnh (Live Server / Vite) để trải nghiệm toàn bộ hệ thống.
