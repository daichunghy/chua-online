# TRANG PHỤC MẶC ĐỊNH — KIỂM CHỨNG VỪA VẶN 3 NHÂN VẬT ĐI CHÙA

Cập nhật: 2026-11-05. Phạm vi: nón lá + túi vải đeo chéo cho 3 nhân vật phụ nữ / đàn ông / trẻ em.
Phương pháp (script `fit_real.py`): MỌI kích thước suy từ số đo posed mesh của chính model đó —
không dùng hằng số gõ tay. Kiểm chứng bằng render mặt trước và soi bằng mắt từng tiêu chí.

## Công thức fit dùng chung (theo tỉ lệ chiều cao posed H của từng nhân vật)

| Hạng mục | Công thức |
|---|---|
| Nón — bán kính vành | R = 0,126 × H (đường kính vành = 0,252 × H ≈ tỉ lệ nón thật 41,6 cm / người 1,65 m) |
| Nón — cao vành (rim) | z = zmin + 0,895 × H, tâm nón tại x/y của xương Head |
| Nón — chiều sâu chóp | 0,105 × H |
| Túi — tâm thân túi | x = bề_rộng_hông/2 + 0,055 × H (ngoài hông trái), z = zmin + 0,47 × H |
| Túi — kích thước | 0,155 H × 0,05 H × 0,165 H |
| Quai đeo | Từ miệng túi lên vai ĐỐI DIỆN (xương upper arm phía ngược), chạy sát mặt trước thân; mặt trước thân (FRONT_Y) đo ở pose **Đứng** — KHÔNG đo ở pose Chắp tay vì hai tay chắp chắn trước ngực làm sai số đo |
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

## 2. ĐÀN ÔNG — ⛔ CHƯA LÀM ĐƯỢC: THIẾU FILE MODEL THẬT

### Đã thử tải (2026-11-05) — đều bị chặn bởi giới hạn connector GitHub

Connector GitHub MCP chỉ trả nội dung file ≤ ~1 MB; file lớn hơn chỉ trả "too large to display" + URL tải có token bị che (không dùng được). Đã thử cả đường vòng theo blob SHA — API yêu cầu SHA của commit/tree, không nhận blob SHA. Kết quả:

| File trên repo | Dung lượng | Kết quả |
|---|---|---|
| `Thiết kế giao diện/Nhân vật 3D/Hunyuan3D/nam-chua-co-mau.glb` | 2.573.924 byte (SHA 74df75a0bdd6a825b78d247e47c81f34cab10bcc) | ❌ Quá giới hạn |
| `Thiết kế giao diện/Nhân vật 3D/Chuyển động/nam-chuyen-dong.glb` | 4.356.216 byte (SHA 674144fe2b47240fe80b2197378bad65c07c4bc7) | ❌ Quá giới hạn |

### File cần Logan tải lên (đúng 1 file)

> **`Thiết kế giao diện/Nhân vật 3D/Chuyển động/nam-chuyen-dong.glb`** — 4.356.216 byte (~4,16 MB)
>
> Đây là bản có chuyển động cùng dòng với file nữ Logan đã cấp (đã kiểm chứng: file nữ tải lên trùng kích thước với `nu-chuyen-dong.glb` trên repo). Bản Hunyuan3D tĩnh (`nam-chua-co-mau.glb`, 2.573.924 byte) chỉ cần khi bản chuyển động có vấn đề — phương pháp fit cần armature + action Chắp tay/Đứng để đo, nên ưu tiên bản Chuyển động.

### KHÔNG dùng model thay thế

Các file `nam-di-chua.glb` (233 KB) trong Thư mục Nhân vật 3D là model khối hộp lắp ghép — Logan đã xác nhận "model đâu phải này đâu". Số đo của chúng (cao 1,76; đầu 0,29; vai 0,56) KHÔNG áp được cho model thật, nên không fit thay thế.

### Việc sẽ làm ngay khi có file (đo giống hệt quy trình nữ)

1. Kiểm kê: tên mesh chính, armature, danh sách xương, danh sách action (kỳ vọng cùng khung 15 xương / 8 action như bản nữ).
2. Đo ở pose Đứng: FRONT_Y (mặt trước thân tại 0,78 H, dải |x| < 0,16 H).
3. Đo ở pose Chắp tay (frame giữa): H (zmin…zmax), bề rộng đầu (16% H trên cùng), bề rộng hông (zmin + 0,52 H), vị trí world của xương Head và 2 xương upper arm.
4. Áp công thức fit ở bảng đầu tài liệu → render kiểm chứng `fit-nam.png` → soi 4 tiêu chí: nón ngồi đúng đầu/tỉ lệ; quai chéo sát thân lên vai đối diện; túi ở hông không lơ lửng/không chìm; màu đúng qua vertex color. Sai tiêu chí nào thì sửa và render lại.

---

## 3. TRẺ EM — ⛔ CHƯA LÀM ĐƯỢC: THIẾU FILE MODEL THẬT

### Đã thử tải (2026-11-05) — cùng giới hạn như trên

| File trên repo | Dung lượng | Kết quả |
|---|---|---|
| `Thiết kế giao diện/Nhân vật 3D/Hunyuan3D/tre-em-chua-co-mau.glb` | 2.579.764 byte | ❌ Quá giới hạn |
| `Thiết kế giao diện/Nhân vật 3D/Chuyển động/tre-em-chuyen-dong.glb` | 4.365.804 byte (SHA 968219ff28ff123d361cf6c02ad403de13f48564) | ❌ Quá giới hạn |

### File cần Logan tải lên (đúng 1 file)

> **`Thiết kế giao diện/Nhân vật 3D/Chuyển động/tre-em-chuyen-dong.glb`** — 4.365.804 byte (~4,16 MB)
>
> (Dự phòng: `Thiết kế giao diện/Nhân vật 3D/Hunyuan3D/tre-em-chua-co-mau.glb` — 2.579.764 byte.)

Không dùng `tre-em-di-chua.glb` (234 KB, model khối hộp) thay thế — cùng lý do như nhân vật nam.
Quy trình đo + fit + render kiểm chứng `fit-tre-em.png` giống hệt mục 2 sau khi có file. Lưu ý riêng cho trẻ em: tỉ lệ đầu/thân lớn hơn người lớn, nên bề rộng đầu và vị trí rim nón PHẢI đo từ mesh của chính model trẻ em — công thức theo H tự co giãn theo tỉ lệ đó, không mượn hằng số của người lớn.

---

## Tổng kết trạng thái

| Nhân vật | Trạng thái | Render kiểm chứng |
|---|---|---|
| Phụ nữ | ✅ Đạt (1 ghi chú thẩm mỹ nhỏ về búi tóc) | `fit_real_nu4.png` + JPG trên repo |
| Đàn ông | ⛔ Chờ Logan tải lên `nam-chuyen-dong.glb` (4.356.216 byte) | — |
| Trẻ em | ⛔ Chờ Logan tải lên `tre-em-chuyen-dong.glb` (4.365.804 byte) | — |

Chặn duy nhất: connector GitHub không tải được file > ~1 MB. Chỉ cần Logan tải lên 2 file trên (như đã làm với file nữ) là fit + render kiểm chứng cho cả hai nhân vật còn lại làm được ngay bằng đúng quy trình đã đạt ở nhân vật nữ.
