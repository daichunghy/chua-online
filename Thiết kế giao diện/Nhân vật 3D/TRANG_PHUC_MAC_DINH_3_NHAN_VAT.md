# TRANG PHỤC MẶC ĐỊNH — KIỂM CHỨNG VỪA VẶN 3 NHÂN VẬT ĐI CHÙA

Cập nhật: 2026-11-05. Phạm vi: nón lá + túi vải đeo chéo cho 3 nhân vật phụ nữ / đàn ông / trẻ em.
Phương pháp (script `fit_real.py`): MỌI kích thước suy từ số đo posed mesh của chính model đó —
không dùng hằng số gõ tay. Kiểm chứng bằng render mặt trước và soi bằng mắt từng tiêu chí.

## Công thức fit dùng chung (theo tỉ lệ chiều cao posed H của từng nhân vật)

| Hạng mục | Công thức |
|---|---|
| Nón — bán kính vành | R = 0,126 × H (đường kính vành = 0,252 × H ≈ tỉ lệ nón thật 41,6 cm / người 1,65 m) |
| Nón — cao vành (rim) | z = zmin + 0,895 × H (nữ, bản v1) / zmin + 0,885 × H (nam + trẻ em, bản v2); tâm nón: x/y của xương Head (v1) / centroid dải đầu đo từ posed mesh (v2) |
| Nón — chiều sâu chóp | 0,105 × H (v1) / 0,125 × H (v2); bán kính đỉnh chóp: 0,012 (v1, đỉnh nhọn) / 0,055 × H (v2, chóp cụt — tóc nam xuyên đỉnh nhọn, xem mục 2) |
| Túi — tâm thân túi | x = bề_rộng_hông/2 + 0,055 × H (ngoài hông trái), z = zmin + 0,47 × H |
| Túi — kích thước | 0,155 H × 0,05 H × 0,165 H |
| Quai đeo | Từ miệng túi lên vai ĐỐI DIỆN (xương upper arm phía ngược), chạy sát mặt trước thân; mặt trước thân (FRONT_Y) đo ở pose **Đứng** — KHÔNG đo ở pose Chắp tay vì hai tay chắp chắn trước ngực làm sai số đo. Bản v2 (nam + trẻ em): quai 3 đoạn ôm bề mặt thân (mẫu bề mặt lấy ở pose Đứng theo từng độ cao) vì quai thẳng 1 đoạn bị chìm vào bụng/ngực model nam |
| Màu model | Model không có material/UV — màu nằm ở vertex color tên `Color`; phải tạo material Vertex Color → Principled Base Color mới render đúng màu |

---

## 1. PHỤ NỮ — ✅ ĐÃ XONG, ĐẠT

- **Model nguồn:** file Logan tải lên `~/workspace/user/files/nu-phuc-hoi-mau-chuyen-dong.glb` (4.031.800 byte).
  Kích thước trùng khớp tuyệt đối với `Thiết kế giao diện/Nhân vật 3D/Chuyển động/nu-chuyen-dong.glb` trên repo → thư mục **Chuyển động** là nguồn chuẩn của dòng model này.
- **Cấu trúc:** 1 skinned mesh `geometry_0` (66.057 đỉnh), armature `world`, 15 xương (Pelvis, Spine, Head, L/R upper arm, forearm, hand, thigh, shin, foot), 8 action: Chắp tay, Di bo, Dung, Quỳ, Thắp nhang, Vái, Lên cầu thang, Xuống cầu thang (tên action trong file có hậu tố `_world`).

### Số đo (pose Chắp tay, frame 15 — đo lại và xác nhận 2026-11-05)

| Số đo | Giá trị |
|---|---|
| Chiều cao posed H (z −1,019 … 0,968) | 1,987 |
| Bề rộng đầu (dải z trên cùng 16% H) | 0,230 |
| Bề rộng hông (dải z = zmin + 0,52 H) | 0,463 |
| Vai trái (xương L upper arm, world) | (0,204; 0,031; 0,507) |
| Vai phải (xương R upper arm, world) | (−0,204; 0,031; 0,507) |
| Mặt trước thân FRONT_Y (đo ở pose Đứng) | −0,137 |

### Hằng số fit đã áp (suy từ số đo trên)

| Hạng mục | Giá trị |
|---|---|
| Nón: R vành / Ø vành | 0,250 / 0,501 |
| Nón: rim_z / sâu chóp | 0,759 / 0,209 |
| Túi: tâm (x, z) | (0,341; −0,085) |
| Túi: kích thước | 0,308 × 0,099 × 0,328 |
| Quai | miệng túi → vai phải (đối diện), sát FRONT_Y = −0,137 |

### Kiểm chứng bằng render — `fit_real_nu4.png` (bản JPG đã đẩy repo: `Thiết kế giao diện/Nhân vật 3D/render-fit-model-that-v1.jpg`)

- ✅ Nón ngồi trên đầu, tỉ lệ vành hợp lý so với đầu/thân
- ✅ Túi nằm ở hông trái, không lơ lửng ngang cẳng tay (lỗi bản cũ), không chìm vào thân
- ✅ Quai chạy chéo qua thân lên vai đối diện
- ✅ Màu render đúng: áo tràng xám xanh, da ấm, tóc đen (nhờ material vertex color)
- ⚠️ Ghi chú thẩm mỹ nhỏ: búi tóc hơi nhô trên đỉnh nón (nón hơi nông so với bản Logan tự làm) — không phải lỗi vừa vặn, để nguyên chờ Logan duyệt

---

## 2. ĐÀN ÔNG — ✅ ĐÃ XONG, ĐẠT (2026-11-05, sau khi Logan tải file lên)

- **Model nguồn:** file Logan tải lên `~/workspace/user/files/nam-chuyen-dong.glb` (4.356.216 byte — trùng kích thước với bản `Chuyển động/nam-chuyen-dong.glb` trên repo).
- **Cấu trúc (kiểm kê):** 1 skinned mesh `geometry_0` (71.464 đỉnh), armature `world`, 15 xương cùng tên như bản nữ, **đủ 8 action, không khác biệt**: Chắp tay, Di bo, Dung, Quỳ, Thắp nhang, Vái, Lên cầu thang, Xuống cầu thang (hậu tố `_world`). Có 1 mesh thừa `Icosphere` (42 đỉnh) giống file nữ — đã loại khi fit. Không material/UV, màu ở vertex color `Color`.
- **Script:** `fit_nam.py` (cùng thư mục). Render kiểm chứng bằng Cycles 32 mẫu, 960×540 (Eevee không dùng được trên máy này — thiếu libEGL).

### Số đo (pose Chắp tay, frame 15)

| Số đo | Giá trị |
|---|---|
| Chiều cao posed H (z −1,020 … 0,966) | 1,985 |
| Bề rộng đầu (dải z trên cùng 16% H) | 0,252 |
| Bề rộng hông (dải z = zmin + 0,52 H) | 0,460 |
| Centroid dải đầu (tâm nón) | (0,001; −0,008) |
| Vai trái / phải (xương upper arm, world) | (0,22; 0,03; 0,51) / (−0,22; 0,03; 0,51) |
| Xương Head (world) | head (0,0; 0,02; 0,64), tail (0,0; 0,01; 1,04) |
| Mặt trước thân FRONT_Y (đo ở pose Đứng) | −0,132 |

### Hằng số fit đã áp (công thức v2, suy từ số đo trên)

| Hạng mục | Giá trị |
|---|---|
| Nón: R vành / Ø vành | 0,250 / 0,500 |
| Nón: rim_z / sâu chóp / bán kính đỉnh | 0,737 / 0,248 / 0,109 |
| Túi: tâm (x, z) | (0,34; −0,09) |
| Túi: kích thước | 0,308 × 0,099 × 0,327 |
| Quai | 3 đoạn ôm bề mặt thân: (0,32; −0,10; 0,08) → vai phải (−0,21; −0,13; 0,50) |

### Kiểm chứng bằng render — `fit-nam.png`

- ✅ Nón ngồi trên đầu, vành ngang trán trên tai, phủ hết tóc (đã phóng to soi vùng đầu)
- ✅ Quai chạy chéo qua thân lên vai đối diện, nằm trên bề mặt thân
- ✅ Túi ở hông trái, không lơ lửng, không chìm
- ✅ Màu render đúng: áo tràng nâu, quần nâu sẫm, da ấm (vertex color)
- 🔧 Quá trình sửa (3 vòng render): vòng 1 quai thẳng bị **chìm vào bụng/ngực** → đổi quai 3 đoạn ôm bề mặt; tóc **xuyên đỉnh nón nhọn** (đo bằng script: 24 đỉnh, lệch tối đa +7 mm ở chỏm tóc trán z≈0,914) và búi tóc lòi trên chóp → tâm nón theo centroid dải đầu, rim hạ 0,885 H, chóp sâu 0,125 H, đỉnh cụt 0,055 H → đạt

---

## 3. TRẺ EM — ✅ ĐÃ XONG, ĐẠT (2026-11-05, sau khi Logan tải file lên)

- **Model nguồn:** file Logan tải lên `~/workspace/user/files/tre-em-chuyen-dong.glb` (4.365.804 byte — trùng kích thước với bản `Chuyển động/tre-em-chuyen-dong.glb` trên repo).
- **Cấu trúc (kiểm kê):** 1 skinned mesh `geometry_0` (71.617 đỉnh), armature `world`, 15 xương cùng tên, **đủ 8 action, không khác biệt** so với bản nữ/nam. Có mesh thừa `Icosphere` — đã loại khi fit. Màu ở vertex color `Color`.
- **Script:** `fit_tre_em.py`. Render Cycles 32 mẫu, 960×540. Áp ngay công thức v2 đã sửa ở nhân vật nam — đạt từ vòng render đầu tiên.

### Số đo (pose Chắp tay, frame 15)

| Số đo | Giá trị |
|---|---|
| Chiều cao posed H (z −1,019 … 0,965) | 1,984 |
| Bề rộng đầu (dải z trên cùng 16% H) | 0,300 (lớn hơn hẳn người lớn — đúng tỉ lệ trẻ em) |
| Bề rộng hông (dải z = zmin + 0,52 H) | 0,460 |
| Vai trái / phải (xương upper arm, world) | (0,19; 0,03; 0,43) / (−0,19; 0,03; 0,43) |
| Xương Head (world) | head (0,0; 0,02; 0,56), tail (0,0; 0,01; 0,87) |
| Mặt trước thân FRONT_Y (đo ở pose Đứng) | −0,104 |

### Hằng số fit đã áp (công thức v2)

| Hạng mục | Giá trị |
|---|---|
| Nón: R vành / Ø vành | 0,250 / 0,500 |
| Nón: rim_z / sâu chóp / bán kính đỉnh | 0,737 / 0,248 / 0,109 |
| Túi: tâm (x, z) | (0,34; −0,09) |
| Túi: kích thước | 0,308 × 0,099 × 0,327 |
| Quai | 3 đoạn ôm bề mặt thân: (0,32; −0,07; 0,08) → vai phải (−0,18; −0,10; 0,42) |

### Kiểm chứng bằng render — `fit-tre-em.png`

- ✅ Nón ngồi trên đầu, không tóc xuyên nón (đã phóng to soi); tóc mai xõa dưới vành là tóc thật của model, tự nhiên
- ✅ Quai chạy chéo qua thân lên vai đối diện, nằm trên bề mặt thân
- ✅ Túi ở hông trái, treo bằng quai đúng vị trí hông (áo trẻ em suông thẳng nên túi có khe hở nhỏ với đùi — chấp nhận được, không lơ lửng/không chìm)
- ✅ Màu render đúng: áo lam xám–tím nhạt, da ấm (vertex color)

---

## Tổng kết trạng thái

| Nhân vật | Trạng thái | Render kiểm chứng |
|---|---|---|
| Phụ nữ | ✅ Đạt (1 ghi chú thẩm mỹ nhỏ về búi tóc) | `fit_real_nu4.png` + JPG trên repo |
| Đàn ông | ✅ Đạt (sau 3 vòng sửa: quai ôm bề mặt + nón chóp cụt) | `fit-nam.png` |
| Trẻ em | ✅ Đạt (áp công thức v2, đạt ngay vòng đầu) | `fit-tre-em.png` |

Cả 3 nhân vật đã fit xong trang phục mặc định trên đúng model thật của từng nhân vật, mọi hằng số đều suy từ số đo posed mesh của chính model đó. Script: `fit_real.py` (nữ), `fit_nam.py`, `fit_tre_em.py`.
