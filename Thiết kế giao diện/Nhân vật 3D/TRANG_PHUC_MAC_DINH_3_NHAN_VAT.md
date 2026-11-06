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

---

## Vật phẩm đeo/cầm theo catalog (bổ sung 2026-11-05) — `items_worn.py`

Script tham số hoá `items_worn.py` (chạy: `blender -b --python items_worn.py -- <nu|nam|tre>`) mở rộng đúng bộ fit ở trên (nón + túi giữ nguyên công thức từng nhân vật: nữ v1, nam/trẻ em v2) và thêm 5 vật phẩm từ `danh_muc_vat_pham.json`. Mọi vị trí vẫn suy từ posed mesh/xương của chính nhân vật (thân ở pose Đứng, tay ở pose Chắp tay frame 15). Render kiểm chứng: `items-nu.png`, `items-nam.png`, `items-tre-em.png` (Cycles 32 mẫu, 960×960).

### 1. `non_la_theu_sen` — sen thêu trên nón ✅ cả 3
Huy hiệu sen phẳng 5 cánh (hồng sen 0.87/0.50/0.58 + tâm vàng kim) đặt tại tham số t=0,42 trên sườn trước của côn nón, offset ra ngoài đúng 0,042×bề rộng huy hiệu theo pháp tuyến côn (pháp tuyến suy từ độ dốc sườn (R2−R)/D của chính chiếc nón đã fit), rồi quay cùng góc nghiêng 3° của nón. Bề rộng huy hiệu 0,085H. Kiểm chứng: sen nằm áp sườn côn mặt trước, không lơ lửng, không chìm — đạt ở cả 3.

### 2. `tui_vai_di_chua` — sen trên túi ✅ cả 3 (chỉ sen, không chữ)
Cùng huy hiệu sen (bề rộng 0,095H) áp phẳng mặt trước túi, offset = nửa sâu túi + 0,042×bề rộng huy hiệu, quay theo góc Z −4° của túi. **Chữ thư pháp: bỏ qua có chủ đích** — chữ dựng bằng hình học nguyên thủy không đọc được sạch ở cỡ này; chỉ ghi nhận, không làm ẩu. Kiểm chứng: sen rõ trên mặt túi cả 3 nhân vật.

### 3. `trang_hat_bo_de` — tràng hạt 108 hạt ✅ cả 3
Vòng Catmull-Rom kín đi qua đúng vị trí xương L/R hand ở pose Chắp tay; điểm treo hai bên chuyển dần từ lòng bàn tay về bề mặt thân (trọng số w = min(1, f/0,35) theo các mốc f = 0,10…0,92), bề mặt thân lấy từ pose Đứng với dải z ±0,03H và khoảng hở 0,020. Độ sâu thả được giải bằng chia đôi (bisection) để chu vi vòng khớp 108 × Ø hạt; Ø hạt đạt 0,0110H ở cả 3 (nữ 0,0219; nam/trẻ em 0,0218; chu vi ≈ 2,36). Hạt chủ (Ø ×1,7) + chùm tua chỉ đỏ 5 sợi tại điểm thấp nhất của vòng. Vì 108 hạt × 0,011H ≈ 2,36 m, vòng thả dài tới gần cổ chân (đáy vòng: nữ z=−0,528; nam −0,532; trẻ em −0,599) — đúng bản chất tràng 108 cầm tay khi niệm.
- Hai lỗi đã bắt được khi soi render và đã sửa: (a) khoảng hở 0,012 + điểm khống chế thưa khiến hạt **chìm vào eo áo trẻ em** (đứt đoạn giữa chừng) → tăng khoảng hở/dải đo + dày điểm khống chế; (b) điểm trượt khỏi tay cùng cao độ với điểm mặt áo đầu tiên tạo **"thanh ngang" hạt** ngang thân ở nữ → chuyển dần y theo trọng số w như trên. Bản cuối: vòng võng mượt liên tục từ hai tay xuống trước áo ở cả 3.

### 4. `hoa_sen_tuoi` — búp sen cầm tay ✅ cả 3
Cuống xanh (Ø 0,011H) từ dưới lòng bàn tay 0,20H đi lên tâm hai bàn tay (tâm = trung điểm 2 xương hand, pose Chắp tay); búp 3 lớp cánh côn dẹt (5 ngoài nghiêng 30° hồng nhạt / 4 giữa 17° / 3 trong 7° hồng đậm) + 3 đài xanh ôm gốc, gốc búp ở +0,045H trên tâm bàn tay. Kiểm chứng: búp đứng thẳng giữa hai lòng bàn tay, cuống xuyên qua tay xuống dưới — đạt cả 3.

### 5. `khan_ran_nam_bo` — khăn rằn quấn cổ ✅ cả 3
Không dùng bán kính cổ gõ tay: quét z dưới xương Head tìm cao độ "eo cổ" (bề ngang thân hẹp nhất: nữ z=0,633; nam 0,635; trẻ em 0,553), rồi lấy bán kính bề mặt theo từng góc từ chính posed mesh (r trong khoảng 0,05–0,19 tuỳ hướng — tiết diện cổ+vạt vai không tròn). Vòng khăn = 18 segment/hàng × 2 hàng, caro xen kẽ trắng ngà (0.92/0.90/0.84) / chàm (0.16/0.18/0.30), hàng dưới lệch nửa segment. Hai vạt thả trước ngực (mỗi vạt 3 đoạn caro ôm bề mặt thân, dài 0,11H) + tua trắng ở cuối vạt. Kiểm chứng: vòng khăn ôm sát cổ, không lơ lửng, không thít vào cổ; vạt nằm trên ngực — đạt cả 3.

### Ghi chú kỹ thuật
- Blender 4.2.3 chạy nền: `bpy.ops.object.transform_apply(scale=True)` **xoá luôn location** của object (đã kiểm chứng) — các cánh sen/búp sen giữ scale ở object, không apply.
- Render phải chạy **tuần tự từng nhân vật**: nhiều tiến trình Blender song song trên máy này chết lặng do RAM (đã mất 1 lượt render nam vì việc này).

---

## BẢN V2 — FIT MODEL REPO CÓ TEXTURE (2026-11-06) — THAY THẾ bản dựng nguyên thủy ở mục trên

Theo lệnh đổi hướng của Chung Hy: không dựng vật phẩm bằng nguyên thủy nữa — repo đã có sẵn model hoàn chỉnh có texture (pipeline Coohom). `items_worn.py` đã viết lại thành script import-and-fit (bản nguyên thủy lưu ở `items_worn_v1_primitives.py`, chỉ còn giá trị tham khảo). Model tải từ chính repo về `repo-items/`: `non_la_theu_sen_v3.glb`, `tui_vai_theu_sen.glb`, `trang_hat_bo_de.obj/.mtl`, `hoa_sen_tuoi.obj/.mtl`, `khan_ran_nam_bo.obj/.mtl`. Mọi scale/vị trí vẫn suy từ số đo posed mesh của từng nhân vật như các mục trước. Render kiểm chứng: `render-items-nu.jpg`, `render-items-nam.jpg`, `render-items-tre-em.jpg` (Cycles 32 mẫu, 960×960) — **đạt 4/5 vật phẩm cho cả 3 nhân vật; hoa sen chỉ đạt ở nữ, lỗi ở nam + trẻ em (xem mục 4 + V2 fix bên dưới)**, kèm các ghi chú trung thực dưới đây.

### 1. Nón `non_la_theu_sen_v3.glb` (PBR) ✅ cả 3
Vành model Ø 0,416 → scale về đúng vành đã fit 0,252H: nữ ×1,204 (rim_z 0,759), nam ×1,203 (rim_z 0,737), trẻ em ×1,202 (rim_z 0,737); đặt tại tâm vành đã đo, nghiêng 3° như bản fit. Texture PBR tự mang trong GLB — họa tiết sen thêu đọc rõ trên sườn nón (rõ nhất ở bản nam).
- **Đã loại mesh quai lụa `Quai_Lua_Hong`** ở cả 3: vòng quai nằm trong mặt phẳng XZ qua trục đầu nên khi đội lên đầu thật, cung dưới của nó cắt ngang mặt (đã soi render vòng đầu, có bằng chứng ảnh). Chỉ loại phần quai, thân nón + texture giữ nguyên.

### 2. Túi `tui_vai_theu_sen.glb` (PBR) ✅ cả 3
Scale theo bề ngang thân túi đã fit (0,155H): ×0,865 (nữ) / ×0,864 (nam, trẻ em) → chiều cao thân đạt 0,328–0,329 so với chuẩn 0,327–0,328. Model repo chỉ có quai xách → **giữ nguyên quai đeo vai 3 đoạn ôm bề mặt** của bản fit đã đạt, neo từ miệng túi lên vai đối diện. Họa in sen trên texture PBR đọc rất rõ ở cả 3 render (bản này có cả chữ/họa tiết in của model gốc, hơn hẳn huy hiệu sen nguyên thủy của v1).

### 3. Tràng hạt `trang_hat_bo_de.obj` ✅ cả 3
Model gốc là vòng oval nằm phẳng (0,296 × 0,416; hạt chủ ở đầu −Y, tua rủ −Z). Fit: cộng thêm Rx +85° vào rotation +90° mà `obj_import` đặt sẵn (tổng 175°) để trục dài thành trục đứng, hạt chủ xuống đáy, đáy vòng ngả trước 5°; scale bề ngang ×1,18 (vòng rộng ≈ 0,35), scale trục dài ×2,35 → đỉnh vòng tại lòng bàn tay +0,03, đáy vòng: nữ −0,521 / nam −0,518 / trẻ em −0,604. Hệ quả của kéo trục dài: hạt thành hình oval dọc (giống hạt bồ đề oval tự nhiên) — chấp nhận được, đã soi render. Vòng qua đúng hai lòng bàn tay pose Chắp tay, hạt chủ + tua đỏ ở điểm thấp nhất — đạt cả 3.

### 4. Hoa sen `hoa_sen_tuoi.obj` ✅ nữ / ❌ nam + trẻ em (đã sửa — V2 fix, xem dưới)
Scale ×1,15 (chuẩn hoá theo H): gốc cuống tại lòng bàn tay −0,10H, đỉnh búp: nữ z=0,642 / nam 0,644 / trẻ em 0,557. **Lỗi đã bắt được khi tự soi render (không phải do người khác chỉ):** model repo là bó sen cắm trưng, không phải sen cầm tay — đo thật từng bộ phận: cuống z 0..0,300; gương sen z 0,300..0,325; cánh búp hồng z 0,284..0,346 (rộng 0,122 × cao chỉ 0,062 → đọc như chùm bóng); lá sen là đĩa phẳng 0,28×0,276 tại z≈0,053, lệch +X 0,08. Đặt gốc tại palm.z − 0,10H khiến búp lơ lửng ~0,13 trên đầu ngón tay và lá nằm ngang giữa thân như **khay bay** — ở nữ tay cao hơn nên búp chạm gần đầu ngón tay, đọc tạm được; ở nam + trẻ em lỗi hiện rõ. Ghi chú cũ "giữ nguyên vì đó là thiết kế của model repo" là **sai** — đã thu hồi.

#### V2 fix — hoa sen cầm tay (nam + trẻ em, 2026-11-06; nữ giữ nguyên)
Tách model theo material, **xoá hẳn lá sen phẳng**; thu hẹp búp ngang ×0,72 + kéo cao ×1,5 (búp cao ~0,107 × rộng ~0,101 — một búp đứng, không còn chùm bóng); đo đỉnh ngón tay từ chính posed mesh pose Chắp tay (nam hand_top_z=0,568 / trẻ em 0,453) và đặt đáy búp ngay trên đầu ngón tay +0,01; cuống co lại chỉ còn đoạn ngắn từ đáy búp xuyên tay xuống palm.z − 0,08 (nam stem_len=0,213 / trẻ em 0,184). Render kiểm chứng mới: `render-items-nam-v2.jpg`, `render-items-tre-em-v2.jpg` — **đạt cả 2**: một búp sen đứng ngay trên hai lòng bàn tay, cuống ngắn xuyên qua tay, không còn khay. Nón/túi/tràng hạt/khăn rằn không đổi (đã đạt từ trước).

### 5. Khăn rằn `khan_ran_nam_bo.obj` ✅ cả 3 (có ghi chú)
Vành model Ø 0,35 → scale ×0,86 (Ø ≈ 0,30), giữ rotation nền +90° của obj_import trừ 15° cho vạt ngả áp ngực, tâm vành hạ 0,018 dưới "eo cổ" đã đo (nữ 0,633 / nam 0,635 / trẻ em 0,553). Vành ôm cổ áo, 2 vạt trắng thả trước ngực + tua ở cuối vạt — đạt cả 3.
- **Ghi chú trung thực:** bản OBJ/MTL tải về chỉ có màu phẳng (MTL không kèm texture caro) nên vành đọc thành dải xám đậm trơn, không thấy họa caro như tên vật phẩm; vạt khăn của model vốn cứng phẳng nên nhìn hơi "giấy" ở cự ly gần. Đây là giới hạn của chính file repo, không phải lỗi fit.

### Chuẩn hoá bắt buộc khi dùng OBJ của repo
Các OBJ mang **custom split normals hỏng** (tham chiếu vn vượt mảng vn) → shade gần đen trong mọi importer chuẩn (búp sen và cuống từng render đen tím vì lỗi này). Script áp đúng quy trình mà `verify_one.py` của chính repo dùng: xoá custom split normals + `shade_smooth_by_angle` sau khi import. GLB không bị lỗi này.
Thêm: `obj_import` đặt sẵn rotation X +90° trên object — mọi rotation fit cho OBJ phải cộng dồn trên nền +90° đó (bản nháp đầu quên điều này khiến vòng hạt nằm ngang như đĩa ở hông và khăn bị lật ngược; đã bắt được khi soi render và sửa).
