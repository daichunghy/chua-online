# Chùa Online (Online Pagoda)

> Hệ thống không gian 3D Chùa Vĩnh Tràng, mô hình vật phẩm chuẩn Coohom, nhân vật Phật tử và giáo trình Phật học trực tuyến.

---

## 📸 Thư Viện Hình Ảnh Mô Hình 3D (Gallery)

### 🏛️ Không Gian Kiến Trúc Chùa Vĩnh Tràng
<p align="center">
  <img src="./Mô%20hình%203D%20Vĩnh%20Tràng/render_vinh_trang_facade.png" width="49%" alt="Mặt tiền Chùa Vĩnh Tràng" />
  <img src="./Mô%20hình%203D%20Vĩnh%20Tràng/render_vinh_trang_altar.png" width="49%" alt="Nội điện Tam Bảo" />
</p>
<p align="center">
  <img src="./Mô%20hình%203D%20Vĩnh%20Tràng/Bản%20dựng%20mới/khuon-vien-chanh-dien-moi.png" width="49%" alt="Khuôn viên chánh điện mới" />
  <img src="./Mô%20hình%203D%20Vĩnh%20Tràng/Bản%20dựng%20mới/chanh-dien-cua-vom.png" width="49%" alt="Chi tiết cửa vòm La Mã" />
</p>

### 🧘 Hệ Thống Nhân Vật Phật Tử 3D & Hoạt Ảnh
<p align="center">
  <img src="./Thiết%20kế%20giao%20diện/Nhân%20vật%203D/anh-xem-truoc-3d-all.png" width="49%" alt="Ba nhân vật Phật tử" />
  <img src="./Thiết%20kế%20giao%20diện/Nhân%20vật%203D/Chuyển%20động/render-nu-that-doi-non-front.png" width="49%" alt="Nữ Phật tử đội nón lá" />
</p>
<p align="center">
  <img src="./Thiết%20kế%20giao%20diện/Nhân%20vật%203D/Chuyển%20động/render-nu-deo-tui-chap-tay.png" width="49%" alt="Chắp tay niệm Phật" />
  <img src="./Thiết%20kế%20giao%20diện/Nhân%20vật%203D/Chuyển%20động/san-chua-xem-truoc.png" width="49%" alt="Thiền hành sân chùa" />
</p>

### 🪷 Vật Phẩm 3D & Chuẩn Xuất Coohom
<p align="center">
  <img src="./Thiết%20kế%20giao%20diện/Vật%20phẩm%203D/render-ao-trang-mannequin.png" width="32%" alt="Áo tràng Phật tử" />
  <img src="./Thiết%20kế%20giao%20diện/Vật%20phẩm%203D/render-tui-vai-theu-sen-34.png" width="32%" alt="Túi vải thêu hoa sen" />
  <img src="./Thiết%20kế%20giao%20diện/Vật%20phẩm%203D/blender-render-non-la.png" width="32%" alt="Nón lá thêu sen PBR" />
</p>

### 📖 Giảng Đường Phật Pháp 3D
<p align="center">
  <img src="./Thiết%20kế%20giao%20diện/Giảng%20đường%203D/giang-duong-phat-phap.png" width="49%" alt="Không gian giảng đường Phật pháp" />
  <img src="./Thiết%20kế%20giao%20diện/Giảng%20đường%203D/giang-duong-co-canh-quan.png" width="49%" alt="Cảnh quan ngoài giảng đường" />
</p>

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
