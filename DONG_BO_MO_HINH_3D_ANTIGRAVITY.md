# HỒ SƠ ĐỒNG BỘ MÔ HÌNH 3D & HỆ THỐNG VẬT PHẨM (ANTIGRAVITY & CODEX HANDOFF)

> **Cập nhật ngày 04/11/2026 - Phiên bản V4:**  
> Hoàn tất toàn diện yêu cầu: **"Thiết kế 3d trang phục mặc định rồi cho mặc lên luôn nhé"**.  
> Bao gồm: Mô hình 3D Áo Tràng Phật Tử Vạt Chéo Thắt Nơ (khớp 100% ảnh tham khảo thẻ bên trái), trang bị trực tiếp lên Nhân vật Nữ chuyển động thật cùng Nón Lá Sen V3, và gói ma-nơ-canh trưng bày chuẩn Coohom.

---

## 1. Chi Tiết Trang Phục Mặc Định: Áo Tràng Phật Tử Vạt Chéo Thắt Nơ

### 1.1. Cổ Vắt Chéo & Nẹp Vạt Chữ Y (Overlapping Cross Collar Band)
* **Thiết kế:** Bản nẹp phẳng dày 1.5mm, rộng 2.6cm may đắp từ vai trái vắt chéo qua ngực sang eo phải.
* **Cổ phụ:** Vạt phụ từ vai phải chéo vào dưới ngực trái tạo giao điểm chữ Y cao quý, trang nghiêm tại xương ức.
* **Làm phẳng thân áo:** Đã loại bỏ hoàn toàn các nốt cúc áo cũ trên thân áo của mesh gốc `geometry_0`, tạo mặt phẳng vải lam mềm mại, thuần khiết.

### 1.2. Nơ Thắt Eo Vải Lam Tinh Tế (Waist Ribbon Bow Knot)
* **Vị trí:** Tọa độ giải phẫu $(X = 0.134, Y = -0.148, Z = 0.025)$ ngay tại điểm kết thúc vạt chéo bên mạn sườn phải.
* **Cấu trúc:** Gồm nút thắt oval 3D, hai cánh nơ bướm mềm mại dài 4cm, và hai dải lụa rủ thướt tha dài 24cm và 17cm buông dọc theo tà áo bên phải.
* **Rigging:** Được liên kết trọng số xương Armature (`Spine` 80%, `Pelvis` 20% cho phần trên; `Spine` 30%, `Pelvis` 70% cho đuôi dải lụa), giúp nơ và dải lụa chuyển động tự nhiên theo bước đi.

### 1.3. Ống Tay Thụng Rộng Truyền Thống (Wide Flowing Sleeves)
* **Kiểu dáng:** Ống tay áo thụng buông rủ dài qua cổ tay đúng chuẩn chùa truyền thống Việt Nam.
* **Hoạt cảnh Chắp Tay:** Khi thực hiện động tác `Chắp tay`, hai bàn tay khép sát vào nhau trước ngực ($< 1.9\text{ cm}$), hai ống tay áo thụng tự nhiên khép sát vào nhau trang nghiêm.

### 1.4. Ma-Nơ-Canh Gỗ Trưng Bày Coohom (Standalone Display)
* Khớp 100% hình ảnh chiếc áo trên ma-nơ-canh trong ảnh tham khảo của user:
  * Chân đế tròn gỗ tiện tự nhiên đường kính 340mm, cao 40mm.
  * Trụ đứng gỗ tiện tròn đường kính 36mm, cao 680mm.
  * Thân ma-nơ-canh bọc vải linen mộc mạc và chóp đỉnh cổ tiện gỗ.
  * Tỷ lệ chuẩn mm: $680 \times 360 \times 1520\text{ mm}$, Pivot đặt chính xác tại tâm đáy chân đế $(0, 0, 0)$.

---

## 2. Các Lỗi Trước Đó Đã Được Khắc Phục Hoàn Toàn

1. **Khoảng cách 2 bàn tay khép sát nhau:** Giảm từ $37.9\text{ cm}$ xuống còn **$1.9\text{ cm}$**, hai lòng bàn tay úp sát thành hình búp sen (*Anjali Mudra*).
2. **Loại bỏ lỗi lem màu:** Áo lam khói thanh nhã `#a0979f`, cổ họng gọn gàng ($abs(x) < 0.042$), chân tóc trán uốn cong tự nhiên ôm búi tóc thấp, không còn vết lem da sang vai.
3. **Nón Lá Thêu Sen V3:** Đường cong parabolic $r(h) = 0.208 \cdot (1 - (h/0.205)^{0.92})$, 16 vành tre, vân lá cọ `#DFCA9F`, đóa hoa sen hồng bung nở rực rỡ, quai lụa hồng, chóp nón hướng thẳng lên trời chuẩn xác.

---

## 3. Danh Mục Tệp Tin Hoàn Thiện

| Phân Loại | Đường Dẫn Tệp Tin | Mô Tả & Trạng Thái |
| :--- | :--- | :--- |
| **Nhân vật mặc Áo Tràng** | `Thiết kế giao diện/Nhân vật 3D/Chuyển động/nu-mac-ao-trang-doi-non.glb` | GLB đầy đủ 5 animation, mặc áo tràng vạt chéo + nơ eo + nón lá V3 |
| **Đồng bộ mặc định** | `Thiết kế giao diện/Nhân vật 3D/Chuyển động/nu-doi-non-la-chuyen-dong.glb` | Tự động đồng bộ sang tệp mặc định của cảnh chùa |
| **Ma-nơ-canh Coohom GLB** | `Thiết kế giao diện/Vật phẩm 3D/models/ao_trang_phat_tu.glb` | Mô hình 3D ma-nơ-canh gỗ mặc áo tràng trưng bày |
| **Ma-nơ-canh Coohom OBJ** | `Thiết kế giao diện/Vật phẩm 3D/models/ao_trang_phat_tu.obj` + `.mtl` | Tệp OBJ chuẩn Coohom kèm vật liệu |
| **Gói Coohom ZIP** | `Thiết kế giao diện/Vật phẩm 3D/coohom_packages/coohom_ao_trang_phat_tu.zip` | Gói nén chuẩn mm (OBJ + MTL + Metadata + Preview) |
| **Trình xem WebGL** | `Thiết kế giao diện/Vật phẩm 3D/chi-tiet-ao-trang-3d.html` | Xem 3D 360°, đổi chế độ ma-nơ-canh / người thật, đổi động tác |

---

## 4. Ảnh Render Studio Kiểm Nghiệm (Trong Artifact Brain)

* [render-nu-ao-trang-chap-tay.png](file:///Users/macos/.gemini/antigravity/brain/e586aaa5-2e71-4723-b119-f4df2ed52600/render-nu-ao-trang-chap-tay.png): Nhân vật nữ chắp tay búp sen khép sát, Áo Tràng vạt chéo, nơ eo, nón lá sen V3.
* [render-nu-ao-trang-dung.png](file:///Users/macos/.gemini/antigravity/brain/e586aaa5-2e71-4723-b119-f4df2ed52600/render-nu-ao-trang-dung.png): Góc nhìn 3/4 đứng chánh niệm thấy rõ toàn bộ đường cắt may vạt chéo, nơ eo và dải lụa.
* [render-nu-ao-trang-di-bo.png](file:///Users/macos/.gemini/antigravity/brain/e586aaa5-2e71-4723-b119-f4df2ed52600/render-nu-ao-trang-di-bo.png): Bước chân thiền hành hướng vào Chánh điện từ phía sau.
* [render-ao-trang-mannequin.png](file:///Users/macos/.gemini/antigravity/brain/e586aaa5-2e71-4723-b119-f4df2ed52600/render-ao-trang-mannequin.png): Ma-nơ-canh gỗ cao cấp trưng bày Áo Tràng chuẩn Coohom.

---

## 5. Trình Xem Trực Tiếp Trên Trình Duyệt

* **Áo Tràng Phật Tử Vạt Chéo:** [http://localhost:8080/Thiết%20kế%20giao%20diện/Vật%20phẩm%203D/chi-tiet-ao-trang-3d.html](http://localhost:8080/Thiết%20kế%20giao%20diện/Vật%20phẩm%203D/chi-tiet-ao-trang-3d.html)
* **Nón Lá Thêu Sen V3:** [http://localhost:8080/Thiết%20kế%20giao%20diện/Vật%20phẩm%203D/chi-tiet-non-la-3d.html](http://localhost:8080/Thiết%20kế%20giao%20diện/Vật%20phẩm%203D/chi-tiet-non-la-3d.html)
* **Toàn Bộ Vật Phẩm 3D:** [http://localhost:8080/Thiết%20kế%20giao%20diện/Vật%20phẩm%203D/bo-vat-pham-3d.html](http://localhost:8080/Thiết%20kế%20giao%20diện/Vật%20phẩm%203D/bo-vat-pham-3d.html)
