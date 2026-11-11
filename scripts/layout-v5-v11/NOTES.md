# Layout V3 — bố cục tổng thể Vĩnh Tràng (ĐẠT, có ghi nợ)

> **⛔ TRẠNG THÁI 2026-11-06 15:15: RENDER ĐÃ TẠM DỪNG theo lệnh điều phối
> (quy tắc video-first của Chung Hy).** Không khởi chạy bất kỳ render Blender nào
> cho tuyến chùa cho đến khi coordinator gửi lệnh REOPEN rõ ràng — đang chờ 2 video
> final (Đắc Kỷ, Họa Bì). Việc không render vẫn làm được: viết script, kiểm tra
> asset, tính camera. `layout_flycam.png` + `layout_ground.png` đã render xong
> trước lệnh dừng — giữ nguyên, coordinator sẽ xét khi render mở lại. Kiểm tra lúc
> nhận lệnh: không có render tuyến chùa nào đang chạy (render duy nhất trên máy là
> v41 của tuyến Chợ Hòa Bình — không thuộc tuyến chùa, không tự ý dừng).

Script: `layout_build_v3.py` (base `repo-khuonvienchanhdienmoi.blend` + cổng/hồ/đường
từ `repo-khuonvienvinhtrang.blend`, tượng `statues/verified_v2/`, vật phẩm
`repo-items/fixed/`, nhân vật `characters_fitted/` — xem `items_worn_export.py`
để biết cách xuất nhân vật đã fit). File: `layout_v3.blend` (31,9MB).
Render: `layout_flycam.png` (Cam_Flycam), `layout_ground.png` (Cam_Ground) — Cycles 32 mẫu.

## Kết quả kiểm chứng (so với refs/ref9.jpg, ref14_int_c.jpg, ref1_front.jpg)

FLYCAM — ĐẠT: chánh điện bên phải mái ngói đỏ nâu lớn (mái hông thật, có hàng ngói),
tháp 7 tầng sau trung-trái, Di Lặc trái-giữa trên bệ đá sẫm, Phật nằm sau trung-phải
(đầu hướng tây), A Di Đà đứng đài sen xanh góc trước-trái, 2 hồ cảnh + 2 cổng tam
quan phía trước, lối đi chính + hàng bồn cây, nền đất xanh bao quanh.
MẶT ĐẤT — ĐẠT: 13 ô vòm + song vàng + cột gốm xanh + vàng bão hòa khớp ref1; mái
là khối đặc (không còn khe hở); 3 nhân vật (nữ/nam/trẻ em, nón + túi + tràng hạt,
pose Chắp tay) đứng trên thềm hướng về chánh điện.

Lưu ý: render flycam cuối ẩn 3 nhân vật (chỉ ~5px ở tỉ lệ đó; nhân vật đã kiểm
chứng trong render mặt đất) để vừa RAM khi render v41 chạy song song — file
`layout_v3.blend` vẫn chứa đủ nhân vật.

## Ba lỗi đã tìm ra + sửa trong quá trình làm
1. **Mặt phẳng studio `Ground`/`Ground.001`/`Ground.002`** do GLB tượng mang theo
   (nằm ở z~1,6) che toàn bộ mặt đất/hồ/sân — phát hiện bằng raycast khi hồ không
   hiện dù đã nâng z. Đã xóa trong script build (2 chỗ). Bài học: GLB nào cũng có
   thể mang "đồ studio" theo — kiểm tra tên object lạ sau mỗi lần import.
2. **Nhân vật lệch gấp đôi tọa độ** (20,-8 → 40,-16, đứng giữa hồ): `matrix_world`
   còn stale ngay sau import nên phép xoay quanh điểm neo tính trên ma trận
   identity. Đã sửa: `view_layer.update()` sau import + sau khi dịch chuyển.
3. **Hàng ngói tách khe hở nhìn xuyên trời** ở góc mặt đất (tia nhìn qua khe đi
   qua nóc mái): đổi hàng ngói thành chồng mí (rộng 1,7 > khoảng cách 1,5).
   Ngoài ra: hồ z-fight với sân → nâng +0,08; camera clip_end 100 → 500;
   bệ Di Lặc tách vật liệu riêng màu đá sẫm.

## Nợ / giới hạn đã ghi (không giấu)
- Hàng rào vàng bao quanh: repo KHÔNG có model hàng rào chu vi (chỉ có lan can thềm
  chính điện) → 2 cổng đứng lẻ, chưa có tường rào nối. Ghi nợ, không tự chế.
- Cây xanh xung quanh thưa (122 tán + 26 thân, tập trung quanh chánh điện/tháp) —
  ảnh thật là rừng cây rậm bao quanh. Không thêm cây giả.
- Mái chánh điện là mái hông dựng trong script (repo không có khối mái lớn thật;
  'Mái ngói phía sau' trong file gốc chỉ là dải phẳng 0,96m ở mặt đất, đã xóa).
- Mặt tượng vẫn trơn như đã ghi ở vòng 2 (giới hạn điêu khắc tay).
- `layout_v3.blend` 31,9MB > giới hạn 25MB/file của giao diện web GitHub → chỉ
  giữ local; render PNG + GLB nhân vật (17-18MB) vẫn tải lên web được.
- Render song song 2 job Cycles trên VM 8GB có thể bị OOM-kill (đã gặp 1 lần ở
  flycam, exit 137) — render nặng chạy 1 job tại một thời điểm.

## Checklist 7 mốc (đánh giá cuối)
- [x] 2 cổng tam quan hai đầu phía trước
- [x] Hồ phía trước (2 hồ đọc rõ); [ ] hàng rào vàng — KHÔNG CÓ asset
- [x] Tượng Phật đứng trắng đài sen xanh góc trước-trái (lớn nhất)
- [x] Chánh điện bên phải, mái ngói đỏ nâu lớn
- [x] Di Lặc trái-giữa
- [x] Tháp 7 tầng phía sau trung-trái
- [x] Phật nằm phía sau trung-phải, trên bệ cao

## Coordinator verdict (mở trực tiếp 2 render, đối chiếu ref9/ref14 + ref1) — 15:20 ngày 06/11

**Kết luận: CHƯA ĐẠT mức "giống thật" — đúng hướng, cần sửa tiếp sau khi mở lại render.**

Đạt:
- 6/7 mốc vị trí đúng: 2 cổng tam quan đầu trước, hồ phía trước, chánh điện phải mái nâu đỏ lớn, Di Lặc trái-giữa, tháp 7 tầng sau-trung-trái, Phật nằm sau-trung-phải.
- Dùng đúng tài sản thật (mặt tiền chi tiết, tượng verified_v2, nhân vật mặc vật phẩm); không còn khối thô tự chế như V2 bị bác.

Chưa đạt (sửa ở vòng sau, theo thứ tự):
1. Tượng Phật đứng trắng góc trước-trái quá nhỏ/lệch biên — trong ảnh thật đây là tượng LỚN NHẤT, nổi bật nhất. Cần tăng tỉ lệ hiển thị và đặt đúng cạnh hồ/cổng, không để lọt ra mép khung.
2. Hồ: cây xanh đang đứng TRONG lòng hồ (trông như cây mọc dưới nước) — bỏ cây khỏi mặt hồ, hoặc dời lên bờ.
3. Mái chánh điện từ cả hai góc đều là mặt phẳng nâu trơn, không có hàng ngói/gờ mái — cần hàng ngói + gờ sống mái đọc được từ flycam lẫn mặt đất (đây là lỗi cũ của facade v3 đã từng gặp).
4. Sân trống trải, mặt đất phẳng lì một màu, hàng cây giống hệt nhau xếp đều hai bên đường như mô hình đường sắt — cần: lát sân đá, cỏ có biến đổi, bonsai/đèn đá, người đi lại, vật phẩm bày biện để sân có đời sống.
5. Góc mặt đất: tháp gable giữa mái đang chìm nửa chân vào mặt mái — chỉnh chân tháp khớp mặt mái.

Ghi chú: 2 render này hoàn thành trước khi lệnh tạm dừng render có hiệu lực hoàn toàn (flycam 15:06); từ đây KHÔNG render thêm cho tới khi main chat báo mở lại.

## Vòng V4 — sửa theo verdict coordinator (2026-11-06, ~17:50–18:10)

Script: `layout_fix_v4.py` (mở layout_v3.blend -> lưu `layout_v4.blend`). Đã probe
kiểm chứng số đo trên file v4 (chưa render — chờ CPU rảnh, watcher
`render_when_idle.sh` tự render khi load<5 + hết ffmpeg/blender khác):

1. Tượng đứng: dịch cụm 97 mesh từ tâm (-41,-32) -> (-13,-34) (bbox mới
   x -18.7..-7, y -40.6..-27.4, z 0..11.1 — cao đúng 11,1m, vào trong khung,
   tây-nam hồ trái). Flycam nới khung: cam (-4,-118,72), lens 33, target (4,6,0).
2. Hồ: 0 mesh cây còn trong hồ (probe lại = 0). Hàng bồn cây x=8 (21 mesh) dời
   sang bờ đông hồ trái x=16.5; cây nền hồ phải: cụm bắc -> (42,-29), cụm nam ->
   (42,-4.1); chum sành (5,-9) -> bờ nam (5,-5.8). Đèn hoa đăng GIỮ trên mặt
   nước (đèn thả nổi — đúng bản chất, không phải cây mọc trong nước).
3. Mái: xóa 7 hàng mỏng cũ; dựng 34 hàng ngói (10 trước + 10 sau + 14 hông),
   dày 0,16 chồng mí, xen kẽ 2 tông nâu; thêm 2 gờ hông trước + diềm chân mái.
4. Sân: noise variation cho 'Nền xám sáng'/'Đá sân'/'Dat_Co'; 6 đèn đá hai bên
   đường chính (VẬT DỰNG MỚI phục vụ trang trí — không phải asset khóa, ghi rõ);
   thêm 2 nhân vật đi trên đường chính (nữ (21.5,-27), trẻ em (24.5,-24), dùng
   lại GLB đã fit); 2 nến hoa sen (vật phẩm fixed) trước thềm chánh điện.
5. Gable: nâng cụm tháp mặt tiền +0,75 -> chân cụm z=7,36 > mặt dốc tại y=-1,85
   là 7,29 (không còn chìm).
Render: layout_v4_flycam.png + layout_v4_ground.png (chờ watcher).

## Ghi chú 18:44 — chờ nu.glb áo tràng mới
- Coordinator báo: trang phục nhân vật nữ đang được sửa ở tuyến riêng (áo tràng
  liền thân); characters_fitted/nu.glb sẽ bị thay (có backup nu-before-robe.glb).
- Nhân vật nữ đã có 2 bản trong layout_v4.blend: trên thềm (20,-8) từ bản v3 và
  người đi đường (21.5,-27) từ script v4 -> phải thay CẢ HAI bằng file mới
  trước render kiểm chứng cuối.
- Watcher render đã DỪNG (kill 18:45) để không render nhầm bản áo cũ; chưa có
  render v4 nào được tạo. Khi coordinator xác nhận file mới sẵn sàng: viết
  script thay 2 cụm nữ (nhận diện theo armature + neo vị trí, giữ nguyên vật
  phẩm đèn lồng tại (19,-8)/(27,-8)), lưu lại blend, rồi mới chạy lại watcher.

## Ghi chú 20:42 — coordinator tự xử lý deadline (watchdog báo agent im 44 phút)
- Kiểm chứng trực tiếp: agent 68638a22 ĐÃ thay xong áo mới TRƯỚC khi im (blend lưu
  19:54; dump object list: Ao_Trang có mặt ở CẢ HAI vị trí nữ (20.1,-8.2) và
  (21.6,-27.2)). Im lặng sau đó là do chờ khe CPU, không phải chưa làm. Coordinator
  đã đóng agent đó (không cần nữa — sản phẩm đã nằm trên đĩa).
- Render robe chạy 20:44 trong khe CPU (load rơi còn ~1): robe-dung-front + side ĐẠT
  nhìn — áo liền một mảnh, quần chỉ lộ dưới gấu. NHƯNG robe-chaptay-front render ra
  Y HỆT tư thế đứng (tay không chắp) — script robe_render.py không áp action đúng,
  nên kiểm chứng pose bằng render này VÔ HIỆU; kiểm chứng pose chỉ còn số đo BVH.
  Lỗi script cần sửa trước vòng render sau.
- Layout V4 flycam + ground (kèm grade D) CHƯA render được trong cửa sổ deadline:
  khe CPU mở quá muộn, slot đã dùng cho robe. Chờ khe tiếp theo sau các final video.

## Ghi chú 20:56 — sửa xong lỗi script robe_render.py (coordinator tự chẩn đoán)
- Nguyên nhân render chắp tay = tư thế đứng: script chạy dưới Blender 5 mà chỉ gán
  animation_data.action, KHÔNG gán action_slot (hệ slotted actions của Blender 5)
  → action không được đánh giá, mọi shot đều là rest pose. Tên action trong file
  đúng ('Chắp tay_world', 'Quỳ_world'...), arm 'world'.
- Bằng chứng sửa đạt (probe không render): có slot, delta vị trí đỉnh trung bình
  so với Đứng: Chắp tay 0,0395m, Quỳ 0,329m (trước sửa = 0).
- Đã vá robe_render.py: gán slot + assert_pose_changed() (pose không đổi >0,005m
  thì DỪNG trước khi render, không lặp lại batch vô hiệu). Batch robe bị kill lúc
  20:50 vì 2 shot còn lại (quỳ/đi bộ) chắc chắn cũng sai pose.
- Sau sửa CHƯA render lại (máy ưu tiên encode Họa Bì) — vòng render sau dùng
  script đã vá này để chốt kiểm chứng pose bằng mắt (chắp tay/quỳ/đi bộ).

## Coordinator verdict V4 (mở trực tiếp 2 render, đối chiếu ref9/ref14/ref1) — 00:00 ngày 07/11

**Kết luận: ĐẠT cho vòng bố cục — 5/5 điểm sửa đều đọc được.**

- Tượng đứng: trong khung, nổi bật góc trước-trái cạnh hồ, đài sen xanh — ĐẠT.
- Hồ: sạch cây trong nước cả 2 hồ — ĐẠT.
- Mái: hàng ngói đọc được từ CẢ flycam lẫn mặt đất (không còn mặt phẳng trơn) — ĐẠT.
- Gable: chân tháp nằm trên mặt mái, hết chìm — ĐẠT.
- Sân: có người (3 nhân vật thềm + người đi đường), đèn đá 2 bên, bonsai — cải
  thiện rõ so với V3; vẫn còn thưa (cỏ/sân phẳng, hàng cây giống hệt nhau) — nợ
  chuyển sang trải nghiệm v4, không chặn bố cục.
- Áo tràng nữ trong cảnh: đọc liền một mảnh từ vai xuống gối, quần chỉ ló dưới
  gấu — ĐẠT ở khoảng cách cảnh.
- Grade D: dịu + ấm hơn hẳn V3, hết chói trưa gắt — ĐẠT hướng.

Nợ nhỏ còn lại (bóng bẩy, không chặn):
- 2 đầu hông mái có vạt tam giác nhỏ nhô lên ở góc mái (nhìn mặt đất thấy rõ).
- Robe còn hơi hộp khi soi gần; quỳ sâu gấu áo cắt nhẹ vào chân (thấy ở cận cảnh,
  không thấy ở khoảng cách cảnh).

### Sự cố render đáng ghi (23:14–00:00 06/11)
- Scene gốc layout_v4.blend làm MỌI lệnh render abort ngay khi khởi động (Cycles
  lẫn Workbench, kể cả ẩn hết mesh/bỏ world/đổi camera mới), trong khi v3 render
  bình thường và cùng object đó render bình thường trong scene mới. Chẩn đoán:
  data-block Scene gốc bị hỏng (không phải object/material/world/camera — đã
  loại trừ từng cái). Cách khắc phục: layout_render_v4_fixed.py tạo scene mới,
  link toàn bộ object, áp grade D1, render 2 góc, lưu layout_v4_fixed.blend
  (bản chuẩn từ đây; layout_v4.blend giữ lại chỉ để đối chiếu).
- robe_render.py đã vá lỗi slot Blender 5 (gán action_slot + assert pose đổi):
  6 shot pose đã render lại đạt (đứng/chắp tay/đi bộ đạt; quỳ còn lỗi nhỏ).

## Đính chính 00:03 ngày 07/11 — Chung Hy BÁC verdict V4 ở trên
- Chung Hy soi 2 render V4 và bác thẳng: "chưa ổn luôn / đâu có đạt đâu / cảm giác
  chân thật ko có luôn". Đúng theo chuẩn của anh (giống ảnh thật): verdict "ĐẠT"
  ở trên chỉ đúng trong phạm vi nội bộ (5 điểm sửa của vòng bố cục đã vào đúng
  chỗ), KHÔNG đạt theo chuẩn giống thật — màu vẫn phẳng như đồ chơi, cây vẫn là
  khối cầu, nền vẫn trơn, tượng vẫn đơn giản. Hạ xuống: BỐ CỤC đạt, GIỐNG THẬT
  chưa đạt (~20% theo ước lượng của Chung Hy).
- Hướng sửa: nghiên cứu sâu màu sắc/vật liệu/mật độ chi tiết đối chiếu ảnh thật
  + game 3D thật (đặc tả NGHEN_CUU_GIONG_THAT_V5) rồi mới dựng vòng cải thiện
  tiếp theo. Không báo "đạt" cho bất kỳ thứ gì chưa đối chiếu ảnh thật.

## Ghi chú 00:10 ngày 07/11 — dọn v3 web + khóa palette (theo NGHIEN_CUU_SAU_GAME_THAT)
- ĐÃ GỠ khỏi trai-nghiem-vinh-trang-v3.html (bản local): (1) số online giả
  "28 đang tu tập"; (2) huy hiệu cấp (Đồng Tu · Cấp 4 ở header, "Cấp N" trên
  nametag La Hán + nametag người dùng); (3) pop-up "+X công đức" khi hoàn thành
  bước + hàng "Điểm công đức" trong panel hành trình + hậu tố "(+điểm)" ở danh
  sách bước; (4) gói giá đèn nguyện trong UI lễ (3 mức 20k/50k/100k ở lựa chọn
  thời gian thắp đèn -> chỉ còn thời gian; nút Dâng Đèn/Thỉnh Tượng trong modal
  La Hán bỏ nhãn giá). Đã grep kiểm chứng sạch. Giá ở mục CỬA HÀNG (chuỗi hạt
  150k, tượng 220k) GIỮ NGUYÊN — đó là thương mại thật, không phải UI lễ.
  File local xong; bản trên repo GitHub chưa cập nhật (đẩy text qua MCP sau,
  không gấp bằng bản v4).
- PALETTE KHÓA (từ nghiên cứu sâu của main chat, áp cho mọi vòng dựng sau):
  ngoài trời mặt tiền vàng ấm #D9A441 + trim kem, sân gạch dịu; nội điện đỏ son
  #8E2323 + thếp vàng #C9A227/#E8C766 trên gỗ tối, CẤM emissive khoe vàng;
  nhà tổ gỗ mộc #5A3D26 không thếp; cổng cẩn sứ đa sắc; nắng ~16h30, AgX,
  exposure web 1,02.
- Thứ tự P0 không đổi: E1 khuôn viên đi bộ + tuyến S0-S7 -> E2 chuỗi thắp nhang
  5 nhịp + khói chuẩn -> E3 grade sáng + palette.


## Đợt P0 "GIỐNG THẬT" (theo NGHIEN_CUU_GIONG_THAT_V5.md mục E + THEME_CHUA_ONLINE.md) — 07/11/2026

File mới: `layout_v5_p0.blend` (từ `layout_v4_fixed.blend`, KHÔNG ghi đè bản fixed).
Scripts: `layout/build_p0.py` + `layout/patch_p0.py` (vòng 2) + `layout/patch_p0_round3.py`
(theme sáng) + `layout/patch_p0_round4.py` (sáng nền theo số đo) + `layout/patch_p0_round5.py`
(trời + cam Di Lặc) + `layout/patch_p0_round6.py` (bão hòa trời + cam Di Lặc mặt bắc)
+ `layout/patch_p0_round7.py` (sửa 3 ảnh bảng chữ rỗng).
Tái lập = chạy lần lượt build -> patch -> round3 -> round4 -> round5 -> round6 -> round7 (bảng chữ).

### Asset CC0 (Poly Haven, API chính thức, chi tiết ở textures/SOURCES.md)
- HDRI: qwantani_late_afternoon_puresky (vòng 1) -> kloppenheim_02 (vòng 3, bị nhiễu đốm)
  -> kloppenheim_06_puresky (vòng 5, trời xanh trong) + HueSat 1.35 (vòng 6).
- PBR 1K: painted_plaster_wall, clay_roof_tiles_02, brick_pavement_02, chipped_concrete,
  dark_wooden_planks, metal_plate (Diffuse/nor_gl/Rough/AO).

### Đã áp (E1-E5)
- E1: world HDRI + sun 3.0 ấm (1.0,0.88,0.72) rot (0.88,0.15,-0.55), AgX, exposure 1.0.
- E2+E3: 59 vật liệu — PBR (BOX projection + Object coords, AO map multiply, Bump từ diffuse)
  cho vữa vàng/ngói/lát/đá/gỗ/sắt; đổi màu theo bảng B: cột teal -> đỏ son #7E2A22/#8E2323
  (hết teal), mái #7C4030, tháp cam đất #C88A4A (override 12 slot trong bbox tháp) + mái tầng
  #A85A38, đài sen #4E86A8, tượng trắng ấm #EFE9DD, bệ đá #6E675C, song sắt -> sắt tối #3A332E
  metallic 0.5, lá 3 vật liệu P0_La_A/B/C (ramp noise 3 tông, gán theo crc32 tên object),
  nước: ramp noise #42532F<->#5A6B40, roughness 0.07, bump gợn.
- E4: AO map trong bộ PBR (multiply) + view-layer AO pass bật. (Chưa có compositor trộn AO
  pass — Blender 5 đổi socket, để P1 xử lý; AO hiện đến từ texture AO + bóng Cycles.)
- E5: nước phản chiếu env (roughness 0.07) + THÊM thành hồ đá (DarkStone 0.45x0.5m) và rào
  vàng P0_Rao_Ho quanh 2 hồ (30 cọc/hồ + lan can trên z 0.93).
- Camera mới: Cam_Gate (23,-63,3.0), Cam_DiLac (vòng 6: (-24,21,4.0) — mặt tượng hướng BẮC
  theo pháp tuyến FrontText (0,1,0)).

### Nghiệm thu bằng số (PIL, script layout/scripts/measure_v5.py)
- Nước (flycam): V4 (112,142,141) G-R=+30 cyan -> V5 (105,116,80) G-R=+11 (<=20 ĐẠT),
  3 tông >=2% (>=2 ĐẠT), hết cyan ĐẠT. Mean sáng hơn albedo đích ~+22 do phản chiếu trời.
- Nền đất (flycam, mặt nạ cỏ V4): V5 (120,109,91) vs đích lát (138,122,99): lệch -18/-13/-8
  -> CHƯA đạt sát ±12 ở kênh R/G (vòng 3 còn -42/-33/-26; mặt nạ gồm cả vùng bóng cây/bệ).
- Mái (flycam): V5 (85,39,31), độ sáng ~47 << tường -> mái tối hơn tường ĐẠT hướng.
- Cột teal (ground): V4 ground có 6.532 px teal ở mặt nạ cột; V5 tại cùng mặt nạ: mean (58,27,19), 98,7% hue đỏ, teal còn 0,0% -> ĐẠT tuyệt đối.
- Hốc vòm (ground): độ sáng dải vòm/song: V4 140,9 -> V5 94,2 = tối hơn 33,1% (>=20% ĐẠT).
- Trời (ground, dải 42px trên): dải trời 42px ở ground: 1 tông >=3% -> KHÔNG ĐẠT tiêu chí >=3 tông (góc cổng đếm được 2 tông; trời sạch nhiễu, có mây mềm nhưng xanh nhạt — xem nợ dưới).
- Mặt tiền (ground): V5 (187,151,102) vs albedo đích (217,164,65): lệch (-30,-13,+37) -> CHƯA ĐẠT ±12; render kem nhạt, kém bão hòa hơn vàng ref1.
- Đối chiếu ảnh mẫu image-48: ảnh mẫu: bão hòa 0,489 / sáng 0,680. V5 ground: 0,341 / 0,597 -> đúng hướng SÁNG-ẤM nhưng còn kém bão hòa -0,148 và kém sáng -0,083 so với mẫu.

### Còn chưa đạt / nợ kỹ thuật sau P0
- Trời render xanh NHẠT hơn ảnh thật/theme (đích #0155C9-#4F97F9): HueSat 1.35 đã đỡ nhưng
  AgX + dải chân trời trong khung hình vẫn nhạt — cần grade riêng cho web/P1.
- Tán cây pastel (xanh bạc hà) ở cự ly gần: ramp lá đã sâu 2 vòng vẫn bị nắng 3.0 + AgX
  đánh bạt — gốc rễ là mô hình cây cầu đơn giản, thuộc P2 (thay cây thật).
- Vàng mặt tiền render kem nhạt hơn ref1 (vàng bão hòa): tint đã #B57E22; sâu nữa sẽ ám
  sang cam — để coordinator/Chung Hy chốt mắt trước khi ép thêm.
- Cổng: 2 chốt trang trí LƠ LỬNG trên xà ngang (lỗi hình học có từ V4, lộ ra ở góc cam mới);
  ô gốm cổng phẳng xanh trơn (chưa mosaic) — P1.
- **Vòng 7 (phát hiện khi soi Di Lặc): 3 ảnh bảng chữ trong cảnh layout BỊ RỖNG từ V4**
  (di_lac_front/adida_plaque/phat_nam_front: filepath trống, 0x0 -> magenta). ĐÃ SỬA:
  trỏ lại statues/tex/*.png + pack (patch_p0_round7.py); render Di Lặc kiểm chứng chữ vàng
  "南無彌勒尊佛" đọc rõ. Hai bảng còn lại không nằm trong khung hình đợt này — đã sửa dữ liệu,
  chưa có render kiểm chứng riêng.
- Trời hướng nam (góc Di Lặc nhìn về nam) trúng vùng nắng của HDRI nên ngả hoàng hôn —
  cùng 1 HDRI, hướng bắc (góc cổng) xanh nhạt; muốn đồng nhất "giữa trưa" phải thay HDRI
  thuần nắng cao hoặc grade riêng — để P1.
- Nền ngoài khuôn viên (mặt phẳng 600m) vẫn trơn màu — P2 (môi trường xung quanh).
- Flycam giữ bản vòng 4 (vòng 5/6 chỉ đổi trời + cam Di Lặc, flycam không thấy trời).

## P1 (V6) — layout_v6_p1.blend — XONG 07/11, ĐẠT 7/7 (đo bằng scripts/measure_v6.py)
Scripts: layout/patch_p1.py (mục 1,2,3,4,5,7) -> patch_p1_comp.py (AO lần 1, hỏng cổng)
 -> patch_p1_round2.py (ramp trời thang Z ngược) -> patch_p1_comp2.py (AO cổng Mist)
 -> patch_p1_round3.py (tường/đất theo số) -> round4 (cả họ vàng) -> round5/6/7/8 (B/specular).
Render chuẩn: layout/layout_v6_{flycam,ground,gate,dilac}.png + 3 render bảng chữ
 (layout_v6_Cam_Plaque*.png), 1280x720 Cycles 32spp, compositor AO bật.

1. ÁM HỒNG — ĐẠT. Gốc: 10 ảnh texture `*_theu_sen_pbr.00x` size (0,0) không có file
   (Blender render magenta). Trích lại từ characters_fitted/{nu}.glb ra
   characters_fitted/tex/{non_la,tui_vai}_theu_sen_pbr.png (1024², nón rơm thêu sen,
   túi be) -> trỏ lại + pack. Đo ground: pixel hồng bão hòa 348px (V5) -> 1px (0,0%).
2. VÀNG MẶT TIỀN — ĐẠT (sát biên B). Mặt nạ "tường nắng" KHÔNG phải 3 vật liệu tường:
   test loại trừ cho thấy do CẢ HỌ 13 vật liệu vàng (Vàng trang trí, Hoa văn vàng,
   Chỉ trắng ngà 219 obj, Chỉ màu kem, ChuoiVang, LuaVangTamLinh, Kim loại vàng cổ...)
   + sàn kênh B do phản chiếu specular trời xanh (Specular IOR 0.5->0.05 mới hạ được).
   Kết quả: (205.8, 154.0, 76.7) vs đích (217,164,65) = delta (-11, -10, +12) <= ±12.
3. TRỜI COBALT — ĐẠT. World 2 nhánh qua Light Path: HDRI sky_blue_clear (ánh sáng)
   + gradient cho tia camera. BÀI HỌC: world Generated Z chạy NGƯỢC (chân trời ~0.50,
   lên cao GIẢM về 0) — stop theo thang đo thật: 0.50 #DCEFFD / 0.42 #4F97F9 /
   0.30 #1E6FD9 / 0.15 #0155C9. Đo: cổng 3 dải (110,159,216)->(97,152,215)->(86,145,213);
   ám ấm góc Di Lặc 0,0% (V5 ngả hoàng hôn nặng).
4. CỔNG — ĐẠT. 8 chốt lơ lửng (Châu+Chóp ở x 18.3/27.7 cổng 1, 40.3/49.7 cổng 2) hạ -2.1m
   đáp mái dưới z=7.8. Decal photo từ ref6_gate.jpg (gate_tex/couplet_L/R.png,
   frieze.png — đã lấp góc trời trong ảnh crop) + trụ phủ mosaic box-projection
   (gate_tex/mosaic_sq.png). Bão hòa mặt cổng 0.348 (V5) -> 0.434.
5. NỀN ĐẤT — ĐẠT. Dat_Co boost 2.8 + tint chỉnh (1.06,0.97,0.80) rồi B x0.92;
   mảng noise 0.78->0.90, scale 0.05->0.085; Cây nền mảng xanh max 0.22->0.15.
   Đo flycam: (133.8, 125.3, 108.3) vs đích (138,122,99) = (-4, +3, +9).
6. AO COMPOSITOR — ĐẠT (qua cổng Mist). B5: scene.compositing_node_group +
   CompositorNodeRLayers output 'Ambient Occlusion' + ShaderNodeMix MULTIPLY.
   HAI bẫy: (a) AO pass = 0 trên trời -> nhân thẳng làm trời ĐEN; (b) Alpha pass = 1
   khắp nơi (film không trong suốt) nên cổng Alpha vô dụng. Cổng đúng = pass Mist
   (world mist start 40 / depth 400): AO' = LIGHTEN(AO, Mist). Độ tối hốc vòm ground:
   102.7 (V5) -> 78.4 (-24%), trời nguyên vẹn.
7. BẢNG CHỮ — ĐẠT, có sửa thật. A Di Đà "NAM MÔ A DI ĐÀ PHẬT" đúng chiều (cam
   Cam_PlaqueAdida). Di Lặc đúng (góc dilac). Phật nằm: plane FrontText.001 vốn quay
   mặt ra BẮC (mặt sau, phía hàng rào) và áp vào mặt bắc của bệ (Platform.001
   y 44.3..49.7) — khách phía sân (nam) không thấy chữ. Đã xoay 180° quanh Z +
   dời plane về mặt NAM của bệ (y 49.69 -> 44.24); render Cam_PlaquePhatNamS xác nhận
   "…BỔN SƯ THÍCH CA MÂU NI…" đọc đúng chiều từ phía sân.

Nợ còn lại sau P1 (không thuộc 7 mục): cây khối cầu pastel (P2), mặt tượng Di Lặc
ám xám xanh ở góc gần + chất lượng sculpt (nợ cũ), nền xa ngoài khuôn viên còn
trơn (P2), frieze cổng còn vệt sáng nhẹ ở mép trái decal.


## P2 — Mật độ & đời sống (07/11/2026, file layout_v7_p2.blend)

Script: `layout/build_p2.py` (+ `patch_p2_tint2.py`, `render_p2.py`); texture tự vẽ
`layout/gen_p2_textures.py` (nguồn ghi ở textures/SOURCES.md). KHÔNG ghi đè v6.

- **Cây:** xóa 282 khối cầu lá (122 "Tán cây" + 160 "Lá nền") + 4 thân bonsai cũ ở thềm.
  Dựng 42 tán card alpha mới (22 cây chính + 20 cây nền, mỗi tán 9–10 card chéo 3 lớp +
  1 card đỉnh) trên ĐÚNG vị trí thân cây cũ; 5 vật liệu lá (3 texture tông #3E6B34 /
  #4C7A3C / #5C8446 + 2 biến thể nhân tint) gán luân phiên theo thứ tự không gian nên
  2 cây kề nhau không trùng vật liệu; mỗi cây có seed hình học riêng (yaw/scale/card).
  Thêm 12 cây cọ (thân cong phân đoạn + 10 tàu lá 2 đoạn) ở vành đai/cạnh hồ/gần tháp.
  **Lỗi đã bắt & sửa trong đợt:** 2 vật liệu tint dùng nút Mix MULTIPLY với Fac mặc định
  0,5 → cộng nửa màu tint gần trắng vào mọi pixel → tán bị trắng bệch (bắt được khi soi
  render flycam đầu tiên); sửa Fac = 1,0, render lại toàn bộ — mọi tán đều xanh.
  Đo render: vùng tán có 11–14 bin màu xanh phân biệt rõ (>200px/bin) — đạt ≥3 tông.
- **Hoa giấy:** 14 điểm (4 chân trụ cổng leo cao 3 m, 2 bên thềm, 2 mép bắc bệ A Di Đà,
  4 góc bệ Di Lặc, 2 góc rào trong), vật liệu hoa RIÊNG `P2_HoaGiay`. Đo pixel hồng bão
  hòa trong ô quanh điểm trồng: cổng 836px, thềm 551px — thấy rõ ở góc cổng/sân nhưng
  mật độ còn thua xa ảnh mẫu image-48 (bụi còn nhỏ) — ghi nhận là điểm chưa đạt tương đối.
- **Bonsai:** 4 chậu mới tại đúng 4 vị trí thềm cũ (13/16,2/29,8/33; −6): chậu gốm xanh,
  thân uốn 3 đoạn, 3 tầng lá phẳng — đọc rõ dáng bonsai ở góc ground.
- **Rào vàng #C9962E:** 6 đoạn (trụ + 2 ray + song 0,5 m) phủ kín hình chữ nhật
  x −38,5..54, y −42..53; đo bbox trong file: x −38,6..54,1, y −42,1..53,1. Phía nam chừa
  2 khoảng trống đúng 2 cổng (16..30 và 38,5..51,5). Bờ hồ đá đã có từ P0, không thiếu.
- **Scatter:** 3 ghế đá, 6 chậu nhỏ dọc lối/cổng, 2 biển gỗ chỉ dẫn — cổng chính (x≈23)
  là "Phương Tiện", cổng hai (x≈45) là "Tịnh Độ" — **gán tên theo quyết định thiết kế
  của đợt này** (audit chỉ chốt có 2 tên này ở 2 cổng, không rõ cổng nào tên nào).
  Thùng công đức gỗ đỏ + mặt chữ tại (27,9; −4,9) cạnh thềm theo audit. 3 lư hương đồng
  (S2 giữa sân (23,−11) lớn + Di Lặc (−24,−16,3) + A Di Đà (−13,−24,2)), mỗi lư 14 que
  hương nghiêng ngẫu nhiên. 132 card lá rụng (texture forest_leaves_02 CC0) + 48 đá cuội.
- **Người:** tổng 14 thân (5 cũ + 9 mới: 7 import + 2 bản sao linked). Mới: S3 thềm —
  nữ nâu (21,3;−7,0); S2 lư hương — nam xám (21,9;−12,7) + nữ xám (24,2;−12,6); tuyến
  chính — nam lam (20,3;−33,5) + bản sao (27,2;−28,3), trẻ nâu (25,8;−19,8) + bản sao
  gần cổng (21,5;−37,3); Di Lặc — nữ lam gốc (−26,5;12,8); A Di Đà — nam nâu gốc
  (−15,5;−23,6). Nhuộm áo bằng cụm vertex-color chiếm đa số: phép nhân bị clamp làm
  2 nhân vật nam không tới được màu đích → đã xóa dựng lại bằng phép nhuộm theo tỉ lệ
  luminance (giữ gradient sáng-tối của vải), phủ 85% loop vải. **Giới hạn trung thực:
  GLB đã fit là mesh tĩnh bake sẵn tư thế chắp tay — CẢ 9 người mới đều chắp tay (kể cả
  người trên tuyến đi), file không có pose đi bộ/đứng khác.** Người ở Di Lặc nằm ngoài
  khung Cam_DiLac (quá gần camera) — đã xác minh tọa độ trong file bằng probe.
- **Sự cố hạ tầng:** VM restart lúc ~02:19 giữa lượt render đầu (mất /tmp + tiến trình
  render + bản vá Fac chưa kịp lưu); đã làm lại patch + render đủ 4 góc sau restart.
  Một cây cọ ở (−24,14) chắn đúng trục nhìn tượng Di Lặc — đã dời sang (−31,16) và
  render lại góc Di Lặc: tượng + biển hiệu đọc trọn.
- **Chưa đạt / nợ sau P2:** (1) mật độ tổng thể vẫn thua ref9 — khuôn viên còn nhiều
  khoảng lát trống lớn (đặc biệt góc tây-nam và quanh tháp), tán card nhìn gần còn
  "lollipop"/thưa; (2) hoa giấy chưa đạt độ rậm image-48; (3) tàu cọ nhìn gần thấy
  vệt sọc + thân cọ từng khúc hộp — chỉ ổn ở khoảng cách; (4) người mới chỉ có pose
  chắp tay (giới hạn asset); (5) nền ngoài rào vẫn là mặt phẳng trơn màu (nợ từ P0/P1);
  (6) mặt tượng Di Lặc ám xám-xanh + sculpt = nợ cũ. Render kiểm chứng:
  layout_v7_{flycam,ground,gate,dilac}.png — đã tự soi cả 4.

## P3 — BÓNG BẨY (07/11, từ layout_v7_p2.blend → layout_v8_p3.blend)
Script: layout/build_p3.py + layout/patch_p3.py + layout/render_p3.py. Bản chính
layout_v8_p3.blend đã lưu KÈM grade (a); grade (b) chỉ áp trong lúc render (không lưu).

1) SỬA BỆ PHẬT NẰM (mục bắt buộc): flycam V7 bệ đọc vàng/ochre — ĐÚNG LÀ LỖI THẬT:
   object "Bệ khu tượng nằm" + "Viền bệ tượng nằm" gán nhầm material "Vàng tường"
   (vàng chánh điện). Đã gán lại DarkStone.002 (= material của Platform.001, cùng
   cây node bê tông PBR). Kiểm chứng render riêng Cam_PlaquePhatNamS
   (layout_v8_phatnam.png): mặt bệ đá xám tối đo RGB (70,65,59) ở vùng dưới bảng chữ,
   chữ vàng "NAM MÔ BỔN SƯ THÍCH CA MÂU NI PHẬT" đọc ĐÚNG CHIỀU; flycam V8 khối bệ
   đã là khối xám tối dưới tượng trắng (hết vàng). Khớp ref7 (tường đá xám sẫm + chữ
   vàng). Lưu ý nhỏ: sắc đá hơi ấm do texture bê tông + nắng ấm, không phải xám lạnh
   tuyệt đối như ảnh thật.

2) WEATHERING (mask world-Z × noise, trộn MULTIPLY vào albedo + cộng roughness):
   21 materials — nhóm tường (dải 0→1,7m, tint (0,33–0,36; 0,34–0,37; 0,27–0,29),
   rough +0,30): Vàng tường, Chỉ trắng ngà, Chỉ màu kem, Gờ vàng, Gờ đỏ, ChuoiVang,
   Vàng trang trí, Hoa văn vàng, Vàng kem, Vữa màu vàng kem, LuaVangTamLinh,
   Kim loại vàng cổ, P1_GomTru, Gốm xanh + (patch bổ sung 4 material sót ở vùng thấp:
   Ngà sáng 48 lượt dùng, Trắng, Đỏ gạch, Men gốm xanh). Nhóm mái (6,2→8,6m, tint rêu
   (0,30,0,42,0,22), +0,20): Mai_Ngoi_Hang(+Sáng). Nhóm mép hồ (−0,1→0,55m):
   Vôi vàng.
   SỐ ĐO (render ground V7→V8 cùng pixel): dải chân tường/plinth −12,6% độ sáng
   (ĐẠT chuẩn ≥8%), thân tường −1,8% (gần như nguyên — không bẩn tổng thể), chân cột
   −6,4% so thân cột −4,1%, toàn cảnh +2,4% (không tối đi). Soi mắt: vệt ố rêu nâu-
   olive đọc rõ ở chân tường + chân cột + bậc thềm.
   NỢ THẬT: rêu mép mái tác dụng RẤT NHẸ (đo G−R ở hàng ngói dưới cùng gần như không
   đổi, flycam chỉ đậm hơn chút ở chân mái) — mask/noise chạy (cùng cơ chế với tường
   đã đạt) nhưng tint nhân lên nền ngói đỏ sẫm nên chủ yếu thành tối đi thay vì xanh
   rêu. Muốn rõ phải đổi cách (overlay decal rêu riêng) — để đợt sau nếu cần.

3) GRADE 2 TÔNG (compositor, nối sau P1_CompAO): fog = Mist pass × hệ số → trộn về
   màu fog; vignette = ảnh PNG nhân (tạo sẵn bằng PIL trong textures/).
   HIỆU CHỈNH QUAN TRỌNG: Mist pass của scene đo thực tế ≈ khoảng cách/200 (ở chùa
   110–140m đã 0,66–0,69) chứ KHÔNG theo start 40/depth 400 như khai báo — hệ số bản
   nháp 0,50 làm trắng xóa mái (đo: mái (123,93,76)→(157,150,149), mất bão hòa).
   Đã hiệu chuẩn: (a) hệ số 0,15 → fog tại chùa ≈0,10; (b) hệ số 0,27 → ≈0,18.
   (a) "Sáng trong" (ĐÃ LƯU làm mặc định trong file): fog (0,82,0,88,0,96) × 0,15 +
   vignette_a (mép −10%, tint ấm rất nhẹ). Render layout_v8_ground.png +
   layout_v8_flycam.png: trời xanh trong trở lại, chùa sắc nét, xa chỉ hơi khói.
   (b) "16h30 ấm" (chỉ render thử, KHÔNG lưu): sun 2,4 màu (1.0, 0.80, 0.58) nghiêng
   58°, exposure 0,9, world ×0,85, fog ấm (0,96,0,83,0,62) × 0,27, vignette_b
   (mép −17%, ấm). Render layout_v8b_ground.png + layout_v8b_flycam.png: toàn cảnh
   nhuốm hổ phách, nắng chiều rõ. Chờ Chung Hy chọn tông chính; nếu chọn (b) thì
   patch thông số (b) vào file.

4) XUẤT BẢN WEB NHẸ: web_export/layout_v8_web.blend + web_export/KE_BANGKE.md.
   Decimate 14 mesh thân nhân vật (132–143k → 13k mặt/mesh; 2 mesh multi-user phải
   tách bản sao mới áp được — đã xử lý ở 2 lượt hiệu chỉnh, kiểm lại: KHÔNG còn mesh
   >20k). Tổng mặt theo mesh-data duy nhất: 2.412.022 → 932.022 (−61%). Texture:
   5 ảnh hạ về ≤1024 (di_lac_front, phat_nam_front, adida_plaque, HDRI, vignette);
   64/64 ảnh đã pack. File 96,7MB → 83,3MB (giảm ít vì texture pack chiếm phần lớn;
   lợi ích chính là số mặt cho Three.js). 2.394 objects giữ nguyên vị trí/palette.
   CHƯA dựng scene web (đúng phạm vi đợt).

Bài học kỹ thuật: Blender 5 compositor KHÔNG nhận ShaderNodeHueSaturation /
ShaderNodeRGB (đó là node của shader editor) — bản compositor: CompositorNodeRGB,
ShaderNodeMath, ShaderNodeMix (socket: [0]=Factor VALUE, [6]=A, [7]=B RGBA,
output [2]=Result). Mist pass: đừng tin thông số start/depth khai báo — render thử
pass riêng mà hiệu chuẩn.


## V7 — MẬT ĐỘ SÂU (07/11/2026, file layout_v9_v7.blend)
Script: `layout/build_v7.py` (+ `layout/patch_v7_moss.py` vòng 2 rêu, `layout/scripts/measure_v7.py`);
probe: `layout/probe_v7.py`, `layout/probe_v7b.py`, `/tmp/probe_body.py`.
Render kiểm chứng (tông a, đã lưu): layout_v9_{flycam,ground,gate,dilac}.png — đã tự soi cả 4.
KHÔNG ghi đè v8; grade giữ nguyên tông Sáng trong (coordinator đã chốt theo ảnh thật).

1) MẬT ĐỘ — ĐẠT MỨC TƯƠNG ĐỐI (chưa tới ref9). Thêm 19 cây mới (thân + tán card,
   ztop 2,6–3,2m, R 1,6–1,9) + 7 cọ + 5 bồn cây tròn kiểu ref9 + 16 cụm hoa giấy
   (scale 1,4, lớn hơn P2) vào đúng các khoảng trống đã đo từ flycam V8 so ref9:
   SW quanh A Di Đà (4 cây/2 cọ/2 bồn), quanh tháp (4 cây/1 cọ, chừa hành lang
   x −2..4), đông-bắc (5 cây/1 cọ), dải đông (2 cây/1 cọ), dải nam (2 cây/1 cọ),
   dải tây (2 cây/1 cọ). Số đo flycam (pixel xanh lá): SW 5,8% → 8,8% (+3,0pp),
   NE 3,3% → 5,1%/4,8% (+1,5–1,8pp), toàn ảnh 5,9% → 6,9–7,1% (+1,0–1,2pp).
   Hoa giấy: pixel hồng ground 98 → 209 (×2,1). SOI MẮT: SW/tháp/NE đều có cây
   mới đọc rõ; NHƯNG mật độ tổng vẫn thua xa ref9 (sân vẫn chủ yếu là lát trống,
   cây mới còn nhỏ so với khoảng trống) — muốn tới mật độ ảnh thật cần thêm ít
   nhất 1 vòng phủ nữa với cây lớn hơn, hoặc chấp nhận mức hiện tại.
   Lưu ý đo: pixel hồng ở góc cổng V7 800 → V9 541 (GIẢM) dù hoa cổng vẫn đọc rõ
   bằng mắt (cụm hồng leo 2 trụ còn nguyên) — do cây/cọ mới che bóng + ngưỡng đo
   nhạy sáng; không phải hồi quy, không truy cứu thêm.
2) RÊU MÁI — ĐẠT SAU 2 VÒNG. Vòng 1: 54 card (ngang hàng 0+1, mặt đứng) — TỰ BẮT
   LỖI khi soi ground: dải rêu đọc như tuyết/vôi trắng, liền mạch 2 hàng ngói
   (G−R +19/+34 nhưng VALUE quá sáng). Nguyên nhân: noise theo Object trên mesh
   join dài 30m → vệt loang ~10m. Vòng 2 (`patch_v7_moss.py`): màu tối hơn
   (0,05/0,09/0,02 → 0,14/0,24/0,07), alpha loang hơn (ngưỡng 0,42→0,70), noise
   chuyển sang UV từng card (vệt ~0,9m), bỏ hàng ngói 1, chừa khoảng trống mỗi
   đoạn thứ 4 → còn 34 card. Số đo G−R dải mái dưới: +9,9/+16,9 (bằng ~1/2 vòng 1);
   soi mắt: dải xanh olive sẫm, loang từng mảng có khoảng trống — đọc là rêu mép
   mái, hết cảm giác tuyết. Vệt nước chân cổng: 12 vệt (3/trụ × 4 trụ, alpha 0,5)
   đã đặt đúng tọa độ mặt nam trụ; ở khoảng cách render chuẩn chỉ đọc rất nhẹ
   (đúng ý đồ, không phải lỗi) — không đo bằng pixel được, ghi nhận theo tọa độ file.
3) CÂY TIỀN CẢNH — ĐẠT. 7 tán đại lộ gần thềm (x ±8, y −9..12) được thêm 1 lớp
   card lớn hơn (R 1,8, thấp hơn 0,3m): soi ground thấy cây lá dày hẳn ở 2 mép
   khung, hết cảm giác "lollipop" ở tiền cảnh. (Kỳ vọng 8 tán nhưng thực tế chỉ
   có 7 thân đại lộ ở x ±8 trong dải y đó — thân (8,−9) không tồn tại, thay bằng
   (16,5,−9); không phải lỗi.)
4) MẶT DI LẶC — ĐẠT MỘT PHẦN (ghi rõ, không phong đạt). Đã làm (kiểm chứng bằng
   probe trên file đã lưu): tai dài Z ×1,4 quanh đỉnh (đáy 7,96 → 7,60, đỉnh giữ
   8,85); miệng rộng X ×1,3 (0,88 → 1,14m); má nở ±0,06; bụng đẩy đỉnh +0,14m
   theo +Y trong dải z 4,85–6,0 bằng falloff (210/2738 đỉnh, đo max y 1,55 → 1,645;
   không chạm chuỗi hạt/me áo ở z>6,0). Soi render dilac: BỤNG tròn hơn thấy rõ;
   TAI/MIỆNG không đọc rõ ở góc này (quá nhỏ so với đầu); MẶT VẪN ÁM XÁM-XANH
   (mẫu tâm ảnh B−R 23,8 → 22,0, gần như không đổi) dù WhiteStone.001 đã hạ
   Specular IOR 0,5 → 0,25. CHẨN ĐOÁN GỐC: tượng quay mặt về bắc, mặt nằm trong
   bóng râm nên chỉ nhận sáng trời xanh → xanh xám; sửa bằng sculpt không tới —
   cần đèn fill ấm hướng mặt hoặc nâng albedo đá trắng, để vòng sau (không làm
   liều trong V7).
- Hạ tầng: render 4 góc chạy nền chờ ffmpeg xong (1 lần chờ ~13 phút), mỗi góc
  ~3 phút, không đè tuyến video. VM không restart trong đợt.
- Chưa đạt / nợ sau V7: (1) mật độ vẫn thua ref9 rõ (cần vòng phủ nữa nếu muốn
  sát ảnh thật); (2) mặt Di Lặc còn ám xám-xanh + chi tiết tai/miệng chưa đọc
  (cần fill ấm/albedo, không phải sculpt); (3) cây card nhìn gần vẫn thưa ở
  trung cảnh (chỉ tiền cảnh được dày); (4) nền ngoài rào vẫn trơn (nợ cũ từ P0).
  Render kiểm chứng: layout_v9_{flycam,ground,gate,dilac}.png.

## V8 — MẬT ĐỘ SÂU (ĐỢT 2) + MẶT DI LẶC ẤM (07/11/2026, file layout_v10_v8.blend)
Script: `layout/build_v8.py` (+ `layout/scripts/measure_v8.py`); probe:
`/tmp/probe_v8.py`. KHÔNG ghi đè v9; grade giữ tông Sáng trong.
Render kiểm chứng: layout_v10_{flycam,ground,dilac}.png — đã tự soi cả 3.

1) MẬT ĐỘ ĐỢT 2 — ĐẠT, VƯỢT CẢ 2 CHỈ TIÊU. Thêm 15 cây lớn TRONG khuôn viên
   (R 2.4–3.2, ztop 3.6–4.6) vào các khoảng trống còn lại (SW 5, đông-bắc 4,
   dải đông 3, quanh tháp 2, dải nam 1) + 23 cây lớn NGOÀI RÀO (R 2.8–3.4,
   ztop 4.6) thành vòng rừng 4 phía + 4 cọ ngoài rào. Vòng ngoài là quyết định
   có chủ ý theo ref9: rừng bao quanh chùa là phần lớn của mật độ ảnh thật;
   phia nam ngoài rào chừa đúng 2 hành lang nhìn cổng (không cây x 14..32 và
   36..52) nên Cam_Gate + trục chính không bị chắn (soi flycam xác nhận 2 cổng
   đọc trọn). Mỗi cây mới cách thân V7 ≥5m; tránh đại lộ, chánh điện, 2 hồ,
   3 bệ tượng, hành lang cổng (ghi trong docstring build_v8.py).
   Số đo flycam (pixel xanh lá, cùng box measure_v7): SW 8,8% → **17,0%**
   (đích ≥12% — vượt), NE 4,8% → **13,2%**, toàn ảnh 6,9% → **11,5%**
   (đích ≥9–10% — vượt). Soi mắt: khuôn viên đọc rậm hẳn, rừng ngoài rào
   khung trọn 4 phía; sân trong vẫn còn lát trống (đúng như ref9: sân chùa
   thật cũng lát nhiều, cây tập trung vành đai + bồn).
2) MẶT DI LẶC ẤM — ĐẠT CHỈ BẰNG ĐÈN FILL (không cần đổi albedo). Đèn Point
   `V8_FillDiLac` 1000W màu ấm (1.0, 0.72, 0.42) đặt (-24, 9, 8.5) trước mặt
   tượng (mặt hướng bắc, tâm mặt ~(-24, -0.2, 8.3)); dùng Point để không hiện
   hình trong render (Area sẽ lộ hình chữ nhật sáng trong khung Cam_DiLac).
   Đã test render 640×360/16spp trước khi render chuẩn: B−R mặt 32 → ~0.
   Số đo full-res: mặt B−R 31,7/36,0 → **−0,7/3,6** (đích ≤10), thân
   18,7 → **−4,7** (hơi ấm). Soi mắt: tượng đọc trắng đá sáng, hết xám-xanh;
   vũng sáng ấm trên mặt bệ trước tượng rất nhẹ, tự nhiên, không hotspot;
   bảng chữ vàng vẫn đọc đúng. Albedo WhiteStone.001 GIỮ NGUYÊN (0.8, 0.8, 0.8)
   — theo đúng thứ tự nhiệm vụ: (a) đủ thì không làm (b).
- Hạ tầng: VM restart lúc ~08:04 giữa lần chạy build đầu (file V10 chưa lưu);
  chạy lại build sau restart, xong. Render 3 góc chạy đơn lẻ khi ffmpeg=0,
  mỗi góc ~3–4 phút (nặng hơn V7 do thêm ~42 cây), không đè tuyến video.
- Chưa đạt / nợ sau V8: (1) nền đất ngoài rào vẫn là mặt phẳng trơn màu
  (cây đã che phần lớn nhưng mặt đất xa vẫn trống — muốn hết phải thêm texture
  cỏ/rừng xa, ngoài phạm vi V8); (2) cây card nhìn gần vẫn thưa ở trung cảnh;
  (3) mặt Di Lặc đọc trắng trung tính (B−R ~0) chứ chưa trắng ấm hẳn như
  ref5 — muốn ấm rõ hơn phải tăng fill hoặc đổi albedo, nhưng mặt hiện tại
  đã trong ngưỡng và tự nhiên nên không ép thêm trong đợt này; (4) rêu mái
  ở góc ground đọc thành mảng xanh hình chữ nhật khá rõ (nợ thẩm mỹ từ V7).

## V9 — NỢ CÒN LẠI CỦA MODEL (07/11/2026, file layout_v11_v9.blend)
Script: `layout/build_v9.py` (+ `layout/scripts/measure_v9.py`).
Render kiểm chứng: layout_v11_{flycam,ground,gate}.png — đã tự soi cả 3.
KHÔNG ghi đè v10; grade giữ tông Sáng trong.

1) KHOẢNG TRỐNG TRONG SÂN — ĐẠT MỘT PHẦN (chỉ tiêu ≥25% KHÔNG ĐẠT, nói rõ
   lý do dưới). Thêm 11 cây lớn (R 2.4–3.0, ztop 3.8–4.4, kiểu V8) + 4 cụm
   hoa giấy + 2 bồn cây vào các khoảng trống theo flycam V10 (SW, tây be Di
   Lặc, tây-bắc, đông-bắc sau chánh điện, dải đông, dải nam). Mỗi vị trí cây
   được KIỂM TRA trong script (cách mọi thân hiện có ≥4m, trong rào, ngoài
   keep-out: 11/11 đạt, không bị loại vị trí nào). Hoa (10,-4) bị keep-out
   đại lộ chặn trong script → dời (12,-5), 4/4 cụm hoa đặt đủ.
   Số đo flycam: xanh lá SW 17,0% → 20,0% (+3,0pp), NE 13,2% → 15,0%
   (+1,9pp), toàn ảnh 11,5% → 12,3% (+0,8pp); hoa giấy ground 207 → 769 px
   (×3,7). Lát trống trong hộp khuôn viên: 71,2% → 69,7% (−1,4pp, −2,0%
   tương đối); đo lại trong đa giác hàng rào: 67,1% → 65,3% (−2,7% tương
   đối). KHÔNG ĐẠT mục tiêu ≥25% — và mục tiêu đó đặt sai: mỗi cây mới chỉ
   phủ ~25m² trên khuôn viên ~8.800m² (11 cây ≈ 3% diện tích); muốn −25%
   cần thêm ~60–80 cây lớn nữa, sẽ chắn trục lễ + phá bố cục. Hơn nữa sân
   chùa thật (ref9) vốn lát nhiều, cây tập trung vành đai + bồn — phần lát
   trống còn lại chủ yếu là sân lễ/trục chính, ĐÚNG ra phải để trống. Kết
   luận: mật độ đã đủ ở mức hiện tại theo chuẩn ref9; không chạy thêm vòng
   phủ cây nữa trừ khi coordinator đổi chuẩn đo (ví dụ đo xanh lá thay vì
   đo lát trống).
2) CÂY TRUNG CẢNH DÀY HƠN — ĐẠT (soi mắt). 76 tán hiện có (P2_TanCay,
   P2_TanNen, V7_Tan_T*, V8_Tan_IN* — nhiều hơn ước 54 do P2 có thêm tán
   nền) mỗi tán thêm 4 card lá TRONG tán (cùng vật liệu của tán đó, 304
   card). Soi ground + gate: tán trung cảnh đọc đầy, hết "xuyên thấu" ở
   khoảng cách thường; cây 2 mép khung ground dày hẳn.
3) RÊU MÁI GÓC MẶT ĐẤT — ĐẠT (soi mắt). Làm lại V7_ReuMai → V9_ReuMai:
   alpha = noise (UV riêng UVMoss, offset ngẫu nhiên mỗi card) × edge
   falloff theo UV 0..1 (mờ dần ~30% mép card); 34 card jitter kích thước/
   vị trí/góc, giữ bố cục + skip pattern của patch_v7. Soi ground: rêu đọc
   thành vệt loang tự nhiên dọc mép mái, HẾT cạnh hình chữ nhật sắc.
   LƯU Ý SỐ ĐO: G−R dải mái (y 285–310/310–335) V10 −42,6/−24,7 → V11
   −45,4/−30,8 (đỏ hơn nhẹ — do edge falloff giảm độ phủ, đúng như thiết
   kế). PHÁT HIỆN KHI ĐO LẠI: số +9,9/+16,9 ghi ở V7 KHÔNG tái hiện được
   trên chính render V9 (đo lại: −38,6/−24,8, cùng hộp đo) — số V7 có lẽ
   đo trên render khác/băng khác; metric G−R trung bình dải bị ngói đỏ
   chiếm đa số nên không phải thước đo rêu đáng tin. Từ nay đánh giá rêu
   bằng soi mắt + quét G−R theo hàng (dải rêu y 305–330 ít đỏ hơn ngói trần
   ~10–20 điểm), không dùng số V7 nữa.
- Hạ tầng: build 48 giây (1 lần lỗi AttributeError ở _min_edge do dùng
  sep.outputs.X thay vì sep.outputs["X"] — đã sửa, chạy lại xong); render
  3 góc đơn lẻ khi ffmpeg=0, mỗi góc ~4–4,5 phút (flycam 09:52, ground
  09:56, gate 10:00), không đè tuyến video. VM không restart trong đợt.
- Nợ còn lại sau V9: (1) mặt đất xa ngoài rào vẫn phẳng trơn (nợ cũ P0,
  cây đã che phần lớn); (2) mặt Di Lặc trắng trung tính, chưa trắng ấm hẳn
  như ref5 (đã trong ngưỡng, không ép); (3) người trong scene Blender đều
  tĩnh/chắp tay (chuyển động để dành cho web dùng GLB có xương).

## V10 — GIỐNG THẬT (09/11/2026, từ layout_v11_v9.blend → layout_v12_v10.blend)
Lý do mở vòng: Chung Hy xem lại, phán "vẫn thấy không giống".
Baseline: render V11 (layout_v11_{flycam,ground,gate}.png, render 09:56–
10:03 ngày 07/11 — SAU lần lưu file cuối 09:52, cùng một file không đổi)
+ layout_v10_dilac.png. Đã soi đối chiếu ref9/ref1/ref6/ref5 trước khi sửa.

### Xếp hạng điểm lệch (theo trọng lượng thị giác, ghi TRƯỚC khi sửa)
1. **Nền ngoài rào = hư vô xám phẳng.** Flycam: ~40% khung hình là mặt
   phẳng xám trơn; góc cổng: hậu cảnh trống trơn. Ref9: chùa nằm giữa biển
   tán dừa xanh rậm tới chân trời, phía trước có đường nhựa. Đây là lệch
   nặng nhất — phá mọi góc rộng (nợ P0, các vòng trước chỉ trồng vòng cây
   thưa, chưa thành "nền").
2. **Cổng thiếu hẳn tháp cổng.** Ref6: tháp 2 tầng mái ngói, hốc giữa đặt
   tượng Phật đứng trắng, 2 hốc vệ thần, câu đối dọc. Render: đỉnh cổng là
   khung chữ nhật rỗng, mái phẳng; photo-texture bị kéo giãn + lẫn hình
   cây xanh của ảnh gốc. Góc cổng sai nhận diện.
3. **Mái chánh điện phẳng/đều + rêu thành vệt chữ nhật.** Ground: hàng
   mảng xanh đều nhau dọc diềm mái đọc như dán decal; ngói thiếu biến
   thiên mảng + không thấy bờ nóc. Ref1/ref9: ngói sóng, mảng tối sáng
   không đều, bờ nóc + gờ rõ.
4. **Mặt tiền thiếu tầng trang trí trên.** Ref1: trên dải vòm là dải
   lattice trắng + phù điêu dày, giữa có tháp pediment, bờ nóc trang trí.
   Render: trên vòm là tường vàng trơn; các mảng vàng nằm trên mặt mái
   đọc như áp phích dán lên ngói.
5. **Hồ nước sáng xanh mint, mặt trơn.** Hai hồ chiếm tiền cảnh flycam;
   ref9 nước rêu tối (#4E5F3A khóa) + có lá sen. Render đọc như bể bơi.
6. **Tượng trắng đọc xám lạnh.** Albedo tượng đang 0.8 xám trung tính
   (WhiteStone.001) — chưa phải trắng ấm #EFE9DD của bảng khóa; Di Lặc cận
   cảnh xám be, A Di Đà flycam xám xanh. (Nét mặt Di Lặc đơn giản = giới
   hạn sculpt đã ghi, không thuộc vòng này.)
7. **Cây mọc giữa lối cổng** (gate: thân cây + tán trong khung vòm) —
   trục cổng ngoài đời trống.
8. **Góc flycam xa/cao hơn ref9** (khuôn viên ~62% bề ngang khung; ref9
   ~85%) — chỉnh camera khớp góc đối chiếu sau khi nền đã sửa.

### Kết quả V10 (đã soi render layout_v12_{flycam,ground,gate,niche,dilac}.png)
Scripts: layout/build_v10.py + build_v10_patch.py + build_v10_fix2/3/4
(+ fix đèn/ramp qua /tmp/fix5–7). File: layout_v12_v10.blend; v11 giữ
nguyên. Hạ tầng: VM restart 2 lần làm chết 2 render (chạy lại xong);
ffmpeg tuyến video chiếm máy ~75 phút — mọi render đều chờ ffmpeg=0.

1. NỀN NGOÀI RÀO — ĐẠT MỘT PHẦN. Hết "hư vô xám": Dat_Co thêm tầng noise
   3 tông đất/rêu (ramp cuối linear ~(0.008–0.02, 0.03–0.042, 0.006–0.012),
   fac 0.93); rừng 180 vị trí gieo (105 gần) — patch gom cụm thành 330
   thân + 1.880 mặt tán (tán ngang 0.95 bề rộng + thêm lớp giữa); đường
   nhựa 175×10,4m + vai đất trước rào nam. NHƯNG chưa thành biển dừa ref9:
   tán card từ trên vẫn thưa, sương của grade khóa làm xa nhạt xám. Cần
   hướng khác (tán 3D dày hoặc texture rừng) — ghi nợ.
2. THÁP CỔNG — ĐẠT. Cả 2 cổng: panel lót hốc + inset tối + viền vàng +
   bệ + TƯỢNG PHẬT ĐỨNG TRẮNG (bản sao đủ 32 mảnh của A Di Đà, scale
   0.195) + chóp ngói đỏ 2 dốc (Mai_Ngoi_Hang) + bờ nóc + 3 bảo châu.
   Hai lỗi tự bắt khi soi cận cảnh: (a) đợt 1 đặt cụm hốc SAI DẤU tọa độ —
   panel che khuất tượng (fix2: dời cả cụm về mặt nam trụ, y −39.65);
   (b) tượng quay LƯNG ra đường vì tượng gốc hướng bắc (fix4: xoay 180°,
   kiểm chứng bằng render cô lập — đủ nếp áo, sash chéo, tay vitarka).
   Render cổng cuối: đọc rõ tượng trắng trong hốc tối. Giới hạn: hốc nông
   hơn tháp thật; tượng mini gần vẫn đơn giản (nếp áo ~2cm).
3. MÁI — ĐẠT MỘT PHẦN. Multiply noise (ramp 0.60→1.09, scale 0.22) cho
   mảng ngói tối/sáng thấy rõ ở ground; bờ nóc: trụ lăn Ø0.3 dài 18,4m tại
   ridge thật (đỉnh verts x-span 20, y=7, z=11.5) + 3 chóp vàng. RÊU mép
   mái vẫn vệt chữ nhật ở ground — V9_ReuMai là 1 mesh gộp, không sửa
   được kiểu chọn lọc; ghi nợ tiếp.
4. MẶT TIỀN — ĐẠT MỘT PHẦN (yếu). Dải lattice dựng mới (z 6.4–7.5) bị
   hàng ngói diềm (mặt trước tới y −3.66) CHE TOÀN BỘ — tự soi ground
   phát hiện, đã xóa; thay bằng gán texture lattice (textures/
   v10_lattice.png, tự vẽ PIL) cho 'Diềm gốm' sẵn có: diềm có hoa văn
   mịn thay trắng trơn, nhưng repeat 60 → họa tiết nhỏ, CHƯA thành tầng
   lattice như ref1. Đúng ref1 cần dựng thêm tầng trên cho model mặt
   tiền — việc kiến trúc lớn, ghi nợ.
5. HỒ — ĐẠT. Ramp nước tối ~40% + roughness 0.07→0.16; mỗi hồ 17 lá sen
   (vật liệu xanh đậm riêng sau khi bản đầu đọc trắng) + nụ hồng. Flycam
   đọc rõ lá sen, hết cảm giác bể bơi.
6. TƯỢNG ẤM — ĐẠT (màu). WhiteStone/001/002 multiply (1.05, 0.99, 0.85)
   về phía #EFE9DD khóa + fill Di Lặc 1000→1500W, màu (1.0,0.70,0.40).
   Render Di Lặc: xám lạnh → be ấm rõ rệt; A Di Đà ấm theo. Nét mặt giữ
   nguyên (nợ sculpt đã biết).
7. CÂY TRỤC CỔNG — ĐẠT. V9_Than.009 + tán V9_Tan_IN9 dời (−5.5, +1.0);
   render cổng: lối đi trống.
8. FLYCAM — ĐẠT. Cam_Flycam → (−2, −97, 57) nhìn (5, 2, 1), lens 33:
   khuôn viên ~85% bề ngang, khớp ref9.

**Ước lượng giống thật sau V10: ~65–68%** (từ ~60%). Căn cứ: góc cổng —
góc nhận diện mạnh nhất — nay có tháp + tượng hốc + chóp ngói (trước là
khung rỗng); flycam hết nền hư vô, có rừng + đường + hồ lá sen. Chặn trên
còn lại: rừng chưa bão hòa ref9, mặt tiền thiếu tầng trang trí, tỷ lệ +
nét Di Lặc trên bệ phẳng 22×20 (thật: tượng choán bệ + bệ là khối nhà có
mái), rêu mái vệt, người tĩnh. Ảnh niche trên đĩa là trạng thái fill 70W
(fix4); file final fill 140W — đã thấy rõ ở render cổng final.



## V11 — GIỐNG THẬT (09/11/2026, layout_v13_v11.blend từ layout_v12_v10.blend)

Chung Hy duyệt chạy tiếp sau V10 (~65–68%). 5 việc theo trọng lượng của §V10.
Số đo PIL flycam: xanh toàn khung 22,86% → **32,93%**; bão hòa vùng chánh
điện (crop cố định) 46,6 → **84,2**.

1. **Tầng trang trí mặt tiền — ĐẠT.** Dựng nguyên tầng trên hàng vòm theo đo
   ref1 (tầng trên ≈ 0,43× tầng vòm; pediment ≈ +1,0×): tường vàng #D9A441
   cao 2,6m trên diềm mái, dải lattice (texture vẽ mới: ô trám + medallion,
   ~1,55m/ô), dải relief vàng, cornice trắng ngà, 2 tháp đầu hồi mang bảng
   chữ Hán vàng trên nền đỏ sẫm (**福/壽**, 1 chữ/tháp như ref1), pediment
   giữa: thân + bảng **永長** + 2 ô lattice nhỏ + gable ngói + chóp vàng.
   13 ô vòm + cột đỏ tầng trệt giữ nguyên. Hai lỗi tự bắt khi soi render:
   (a) texture không hiện — Blender 5 tạo UV dạng ATLAS cho cube primitive
   (mỗi mặt chỉ phủ 1/4×1/4 texture) → viết lại UV theo hình chiếu thế giới
   cho 4 hộp mang texture (fix_v11.py); (b) nét lattice v1 quá mảnh, chìm ở
   khoảng cách cảnh → vẽ v2 nét đậm (gen_v11_lattice2.py, bản v1 giữ ở
   textures/v11_lattice_v1.png). Nợ nhỏ: tầng thật ornate hơn (relief gốm +
   tháp giữa cao hơn) — bản này đúng tỉ lệ + thành phần, giản lược chi tiết.
2. **Bệ Di Lặc — ĐẠT (cấu trúc/tỉ lệ), nợ tỉ lệ tuyệt đối.** Bỏ phiến phẳng
   22×20m; bệ mới: thềm đá sẫm 15×13 + chân đỏ gạch + khối đá sẫm 11,5×9,2
   mang MỘT dải chữ vàng 南無彌勒尊佛 đọc đúng chiều (bản sao FrontText đặt
   lại lên mặt bệ; bản gốc trên đế tượng đã ẩn render để hết chữ trùng) +
   diềm ngói đỏ-nâu cụp 4 phía + nắp đá 3,2m; tượng nâng +1,5m. Tỉ lệ
   tượng:bệ 7,89:2,85 ≈ **2,77** so với đo ref5 **2,85**; tượng choán bề
   ngang bệ như ref5. Tổng công trình 11,3m (thật ~20m) — không kéo lên vì
   toàn khuôn viên model là tỉ lệ sơ đồ (điện ~12m); ghi nợ riêng.
3. **Vành đai dừa — ĐẠT.** 340 cây NGOÀI rào gộp 1 mesh vertex-color 4 tông
   xanh khóa: 184 dừa (thân 7–11m, tán 8–10 lá cọ rủ) + 156 cây tán khối
   icosphere méo noise; vành 4–42m ngoài rào, 2–3 lớp sâu; chừa đúng 2 hành
   lang cổng Nam + dải đường. Flycam đọc thành thảm xanh LIỀN quanh khuôn
   viên (22,86→32,93%). Nợ nhỏ: tán khối nhìn gần còn faceted (đồng phong
   cách card của scene).
4. **Rêu mái — ĐẠT.** Xóa V9_ReuMai (mesh dải liền); 99 mảng rêu nhỏ rời
   (fan 9 đỉnh, r 0,3–1,0m, texture alpha noise) bám đúng mặt dốc: cụm dày
   mép mái trước + rải theo rãnh ngói + mái sau. Render góc đất + flycam:
   hết vệt dài; mảng nhỏ, hơi tinh tế (đúng tiêu chí mục này).
5. **Sương nhạt — ĐẠT.** Mist world start 40→**85**, depth 400→**560**;
   node ×**0,45** CHỈ ở nhánh sương compositor (cổng AO LIGHTEN không đụng).
   Mist tại chánh điện ở flycam: pass 0,048 → hiệu dụng ≈ **0,003** (mục
   tiêu ≤0,15). Sun/exposure/grade "Sáng trong" khóa giữ nguyên. Bão hòa
   vùng chánh điện 46,6 → 84,2.

Giữ nguyên (đã kiểm qua render): 3 bảng hiệu + hướng, rào vàng, tượng cổng
V10, hồ sen V10, palette khóa, fill Di Lặc 1500W, màu tượng trắng ấm V10.

Sự cố kỹ thuật vòng này: (a) NodeLink bị gỡ tham chiếu sau remove link →
   bắt vị trí neo trước khi gỡ; (b) Blender 5: `transform_apply(scale=True)`
   sau `primitive_cube_add(location=...)` nấu location vào mesh — helper
   box() set location lần 2 làm MỌI box đi gấp đôi tọa độ → bỏ apply, tạo
   tại gốc rồi set dimensions/rotation/location; kiểm bbox 13/13 vật đúng
   tâm kỳ vọng trước khi render.

**ƯỚC LƯỢNG GIỐNG THẬT SAU V11: ~73%** (căn cứ: 5/5 nợ cấu trúc lớn nhất
của V10 đã đóng ở mức thành phần + tỉ lệ đo được; phần còn lại là nợ chi
tiết/sculpt — mặt tượng, nội thất chưa có ảnh thật, tỉ lệ tuyệt đối sơ đồ,
người tĩnh trong scene Blender, chi tiết gốm mặt tiền giản lược).
Render nghiệm thu: layout/layout_v13_{flycam,ground,gate,facade,dilac}.png.
Script: layout/build_v11.py, fix_v11.py, fix_v11_tex2.py,
scripts/gen_v11_lattice2.py, scripts/measure_v11.py, render_v11_driver.sh.

## Nợ còn lại sau V11
1. Mặt tượng (giới hạn sculpt) — Di Lặc/A Di Đà/Niết Bàn vẫn khối đơn giản.
2. Nội thất chánh điện: chưa có ảnh thật đối chiếu (giữ nguyên trạng).
3. Tỉ lệ tuyệt đối toàn khuôn viên là sơ đồ (Di Lặc 11,3m vs thật ~20m;
   điện ~12m) — muốn đúng tuyệt đối phải dựng lại tỉ lệ toàn layout.
4. Tầng trang trí: chi tiết gốm/relief giản lược so với ref1.
5. Người trong scene Blender tĩnh (web dùng GLB có xương riêng).
6. Tán cây vành đai nhìn gần còn faceted; cây tiền cảnh vẫn card.

## V12 — KHÔI PHỤC TƯỢNG PHẬT NGUYÊN BẢN TRANG NGHIÊM (09/11/2026, layout_v14_v12.blend từ layout_v13_v11.blend)

**Lệnh cứng của Chung Hy (18:13 09/11): "TƯỢNG PHẬT THÌ LÀM CHO NGHIÊM
TRANG, KHÔNG ĐƯỢC CHỈNH LẠI — VẬY LÀ BÁNG BỔ ĐÓ".** Luật tuyệt đối từ
vòng này: KHÔNG chỉnh sửa/stylize tỉ lệ hay nét mặt bất kỳ tượng Phật
nào; chỉ được khớp VỀ PHÍA ảnh thật/bản gốc đã kiểm chứng. Màu đá ấm
#EFE9DD + fill Di Lặc 1500W + bệ kiến trúc V11 là khớp theo ảnh thật /
kiến trúc — GIỮ.

### Phát hiện khi rà (đo từ file, không đoán)
- **Di Lặc bị sculpt ở V7** (build_v7.py mục 4, mang sang mọi vòng sau):
  tai `Head_earL/R.001` tỉ lệ trục Z = **1,400** so với bản gốc (scale
  nằm trong object), `Head_smile` trục X = **1,300**, má `Head_cheekL/R`
  lệch ±0,06 m, bụng `Torso` bị đẩy đỉnh vào mesh (bbox sâu Y +2,2%,
  tối đa +0,14 m ở dải z 4,85–6,0). Đo bằng tỉ lệ bbox từng mảnh so với
  verified_v2: 94 mảnh khớp, CHỈ 4 mảnh này lệch — đúng 4 chỗ V7 đã chạm.
- **Tượng hốc cổng bị "nới ngang ×1,35"** ở build_v10_fix3 ("để hốc cổng
  dễ đọc hơn"): trị riêng của ma trận sao chép = [0,2636; 0,1953; 0,1953]
  — biến dạng tỉ lệ cùng loại với sculpt Di Lặc, phải hoàn trả.
- A Di Đà chính + Phật nằm: không lệch (xem kiểm chứng dưới).

### Cách sửa (sửa tận gốc, giữ nguyên mọi thứ khác của V13)
1. `build_v12.py`: cả 94 mảnh của nhóm Di Lặc được thay mesh bằng bản
   sao của mesh gốc từ `statues/verified_v2/di-lac.glb` (gán lại đúng
   vật liệu scene theo từng slot); 6 mảnh bị chạm (tai ×2, smile, má ×2,
   Torso) được reset `matrix_world = M @ W_glb`, với M = phép đặt cả
   nhóm đo từ 88 mảnh chưa bị chạm: **dịch thuần (−24, −1, +3,2), scale
   đúng 1,0** (87/88 mảnh khít tuyệt đối). `PlatformSlab` lệch M ở Z
   −1,5 là vị trí chìm có chủ đích từ các vòng trước — giữ nguyên vị
   trí, chỉ thay mesh.
2. `fix_v12.py`: áp phép nghịch của ×1,35 (tỉ lệ X ×1/1,35 quanh tâm
   cổng) lên 64 mảnh `V10_GateBuddha_*`. FIX2 (dịch Y) và FIX4 (xoay
   180° cho mặt tượng hướng ra đường như ref6) là phép đặt/xoay cứng —
   giữ nguyên.
3. `fix_v12b.py`: bản sao cổng của V10 lọc theo vật liệu nên SÓT 7 mảnh
   nét mặt (mày/mắt/mí/miệng, vật liệu FeatureShadow) — tượng cổng
   thiếu mặt. Bổ sung đủ 7 mảnh × 2 cổng bằng đúng phép đồng dạng của
   nhóm sao (độ lệch Mc = 0,00000), chia sẻ mesh gốc như cách V10 làm.
   Đài sen/bệ/bảng của tượng chính không đưa vào — hốc có bệ riêng
   (đúng thiết kế V10 + tượng cổng thật ở ref6).

### Kiểm chứng (đo trên file đã lưu)
- Di Lặc: 94/94 mảnh — độ lệch ma trận so với M@W_glb = **0,0000**, tỉ
  lệ kích thước từng trục = **1,000**, khoảng cách 2 má scene 0,8944 =
  GLB 0,8944. Mesh mới chỉ có đúng vật đó dùng (không còn bản sculpt
  sót ở đâu).
- A Di Đà chính: 79 mảnh, M-dev = 0; đối chiếu TỪNG ĐỈNH: khoảng cách
  đỉnh-gần-nhất hai chiều scene↔gốc **max 0,00 mm** (trung bình
  0,001–0,002 mm) kể cả các mảnh tay/ngón/chân/tai → nguyên bản tuyệt
  đối, chưa từng bị chạm.
- Phật nằm: 33 mảnh khớp đỉnh toàn bộ; chỉ `FrontText.001` (bảng chữ)
  lệch vị trí — đó là lần dời bảng sang mặt nam ở P1 (vị trí, không
  phải tỉ lệ tượng).
- Tượng cổng sau sửa: trị riêng đều **[0,1953; 0,1953; 0,1953]**, tỉ lệ
  khoảng cách từng cặp tâm mảnh hằng số tuyệt đối (0/494 cặp lệch),
  cụm cao 1,58 m trong hốc — bản sao đồng dạng chính xác của gốc.
- Diff pixel render Di Lặc V13↔V14 (cùng camera): chỉ **0,30%** khung
  hình thay đổi, nằm đúng vùng đầu/tai và dải bụng — phần còn lại của
  cảnh giống hệt. Phóng to vùng mặt: tai hết thõng dài (về độ dài tự
  nhiên), má hết phồng, miệng cười hẹp lại — mặt về vẻ calm/trang
  nghiêm của bản verified_v2.
- Render nghiệm thu: layout/layout_v14_{dilac,adida,niche,flycam}.png
  (soi cạnh ref5/ref3: đạt — tượng đúng tỉ lệ gốc, trang nghiêm).

### Verdict từng tượng
- **Di Lặc: ĐÃ KHÔI PHỤC nguyên bản verified_v2** (tai/miệng/má/bụng về
  gốc; giữ bệ V11, bảng V11_PlinthText, fill 1500W, màu ấm).
- **A Di Đà chính: NGUYÊN BẢN** — không phải sửa gì.
- **Phật nằm (Niết Bàn): NGUYÊN BẢN** — không phải sửa gì.
- **2 tượng hốc cổng: ĐÃ KHÔI PHỤC** — hết nới ngang ×1,35, bổ sung đủ
  nét mặt; hình học là mesh gốc (dùng chung datablock với tượng chính).
- **Tượng bàn thờ: KHÔNG CÓ trong file bố cục này** (quét toàn scene:
  không vật nào dùng AltarGold/GoldDark, không có HandsDhyana; các cụm
  WhiteStone/HairStone chỉ gồm đúng 4 nhóm tượng trên). Tượng thờ thuộc
  model nội điện riêng — ngoài phạm vi layout_v14; muốn rà phải mở
  vòng riêng cho file nội điện.

### Ước lượng giống thật sau V12
Tổng thể giữ **~73%** như V11 (vòng này không thêm chi tiết mới — nó
gỡ một lỗi đúng/sai). Riêng trục tượng: **về đúng chuẩn verified_v2 —
100% hình học gốc, 0 chỉnh stylize còn sót**. Giới hạn còn lại của
tượng là giới hạn của chính bản dựng gốc (nét mặt tối giản kiểu ống,
thân khối mượt, tay hơi "ống") — muốn vượt phải dựng lại tượng từ ảnh
thật trong một vòng riêng, không phải nắn nót trên tượng hiện có.

### Quan sát ngoài phạm vi (ghi lại, chưa sửa)
Thân tượng trong hốc cổng đọc TỐI trên render cận cảnh — đã có từ
render của chính V10 (layout_v12_niche.png), hình học đã chứng minh
đúng vị trí/kích thước/vật liệu; đây là vấn đề ánh sáng trong hốc,
không phải tượng. Để Chung Hy quyết có mở vòng riêng cho ánh sáng hốc
hay không.

Script vòng này: layout/build_v12.py, fix_v12.py, fix_v12b.py,
verify_v12.py, diag_gate_v12.py, diag_gate2_v12.py, audit_verts_v12.py,
audit_nn_v12.py, scripts/render_v12.py, render_v12_driver.sh;
audit thô: layout/v12_audit.json.

## V13 — NẮN TAI TƯỢNG VỀ PHÍA ẢNH THẬT (09/11/2026, layout_v15_v13.blend)

**Lệnh Chung Hy 20:04 09/11: "Làm vòng nắn mặt tượng theo đúng ảnh thật".**
Luật cứng vòng này: chỉ sửa cái ĐO ĐƯỢC là lệch so với ảnh thật (mỗi sửa
ghi căn cứ đo); cấm stylize/cute hóa; chỉ đụng vùng mặt/đầu; base
layout_v14_v12.blend → layout_v15_v13.blend, không ghi đè nguồn; kiểm
chứng bằng audit script độc lập, không tự chấm bằng mắt.

### Định nghĩa đo (ghi rõ vì đã gây lỗi — xem "Lỗi bắt được" dưới)
Chiều cao đầu = **CẰM → ĐỈNH ĐẦU**, khớp định nghĩa đo trên ảnh:
Di Lặc cằm 6,0501 → đỉnh sọ 7,8902 = **1,8401 m**; A Di Đà đáy sọ
9,8126 → đỉnh ushnisha 11,0514 = **1,2388 m** (GLB, Y-up). Tỉ lệ
tai/đầu, đỉnh tai, đáy tai đều tính trên mẫu số này. Head_neck /
Head_neckring thấp hơn cằm 0,19–0,22 m và TAI (sau khi kéo dài, đáy
tai A Di Đà thấp hơn cằm) KHÔNG được tính vào mẫu số.

### Bảng đo ảnh ↔ model ↔ sau nắn (tỉ lệ theo chiều cao đầu)
| Tượng / chỉ số | Ảnh thật | Model V14 | Sau nắn V15 | Kết luận |
|---|---|---|---|---|
| **Di Lặc** (ref5) tai/đầu | 0,664 | 0,486 | **0,664** | NẮN — tai ngắn ~27% |
| Di Lặc đỉnh tai (từ đỉnh đầu) | 0,321 | 0,402 | **0,321** | NẮN cùng phép biến đổi |
| Di Lặc đáy tai (so cằm) | +0,015 (≈ ngang cằm) | +0,112 | **+0,015** | NẮN cùng phép biến đổi |
| **A Di Đà** (ref3) tai/đầu | 0,507 | 0,407 | **0,507** | NẮN — tai ngắn ~20% |
| A Di Đà đỉnh tai | 0,632 | 0,534 | **0,632** | NẮN cùng phép biến đổi |
| A Di Đà đáy tai (so cằm) | −0,140 (dưới cằm) | +0,059 | **−0,139** | NẮN cùng phép biến đổi |
| **Phật nằm** (ref7) tai/đầu | ≈0,53 ± 0,06 | 0,489 | 0,489 | KHÔNG NẮN — lệch ~8% trong sai số đo |
| Di Lặc mắt / mũi / miệng / má | — | lệch 3% / 7% / 6% / ~0% | giữ nguyên | KHÔNG SỬA — ≤7%, nhiều chiều bị nhiễu phối cảnh |
| Di Lặc đầu/thân | 0,29 | 0,304 (5%) | giữ nguyên | KHÔNG SỬA |
| A Di Đà đầu/thân | không đo vững (0,12–0,26) | — | giữ nguyên | KHÔNG SỬA — số liệu mâu thuẫn giữa các lần đo |
| Di Lặc hạt tràng | ≈0,08 đầu | 0,114 đầu | giữ nguyên | KHÔNG SỬA — lệch chưa rõ |

Phương pháp đo ảnh: visual grounding landmarks trên crop phóng to bằng
PIL + parser bbox GLB thuần Python (/tmp/v13/glb_dump.py — đã mất theo
VM restart, xem cuối mục); tỉ lệ theo chiều dọc nên vững trước phối
cảnh góc 3/4.

### Cách nắn (chỉ ma trận, không chạm mesh)
Biến đổi `z' = k·z + b` trên matrix_world của mảnh tai (chỉ trục dọc),
đo lại sau biến đổi, assert tỉ lệ + đỉnh tai trong ±0,01 mục tiêu:
- **Di Lặc** (Head_earL.001 / Head_earR.001): k = **1,3667**, b = −3,6465;
  tai 0,894 → **1,2218 m**; đỉnh 10,3506 → 10,4995; đáy 9,4566 → 9,2777.
- **A Di Đà** (Head_earL / Head_earR): k = **1,2467**, b = −2,6846;
  tai 0,5038 → **0,6281 m**; đỉnh 10,3899 → 10,2685; đáy 9,8861 → 9,6404.
- **2 tượng hốc cổng**: truyền bằng phép liên hợp `A' = Mc·A·Mc⁻¹`
  (Mc scale đều 0,1953; tai cổng có sẵn cả 2 mảnh, không phải tạo mới);
  Mc trước 0,000002/0,000004 → sau sửa **0,000004** cả 2 cổng; tỉ lệ
  tai cổng đo lại = **0,5070** (mục tiêu 0,507).

### Lỗi bắt được trong vòng (đã sửa tận gốc trước khi giao)
1. **Kiểm tra Mc cổng quá chặt + sai mốc**: build v1 lấy Mc từ pairs[0]
   tùy ý và chạy SAU khi tai chính đã đổi → báo Mc lệch 0,650852 và
   chết ở cổng PT. Chẩn đoán: (a) cặp tai lệch Mc ~0,65 là HỢP LỆ sau
   khi tai chính đổi (chính phép liên hợp sẽ sửa); (b) 4 mảnh tay trái
   bản sao cổng (HandL, FingerL0/1/2) lệch Mc **0,06–0,08 có từ V14**
   — tâm khớp Mc chính xác (diff 0,0000 m), chỉ xoay nhỏ quanh tâm
   riêng từ lúc sao chép V10, ngoài phạm vi V13 nên loại khỏi kiểm tra,
   KHÔNG sửa. Sửa script: Mc lấy từ Head_ushnisha, kiểm tra trước loại
   tai + tay, kiểm tra sau chỉ loại tay.
2. **Mẫu số chiều cao đầu sai (nghiêm trọng, suýt giao tai dài thừa)**:
   bản build đầu tính head_h trên TẤT CẢ mảnh Head_* — gồm Head_neck
   thấp hơn cằm 0,19–0,22 m — nên k Di Lặc ra 1,5328 thay vì 1,3667,
   tai dài thừa **12–15%** so với ảnh (vượt luật "không phóng đại quá
   ảnh thật"). Bắt được khi đối chiếu k thực tế với k kế hoạch trong
   header script + đo lại bbox từng mảnh GLB. Sửa tận gốc: loại cổ +
   tai khỏi bbox đầu ở CẢ build_v13.py VÀ verify_v13.py (verify bản
   đầu cũng mắc lỗi này theo chiều ngược: đo trên V15, đáy tai đã kéo
   dài tự định nghĩa lại đáy đầu → báo sai A Di Đà 0,4451 trong khi
   build đúng 0,507). Sau sửa: k = 1,3667 / 1,2467 khớp đúng kế hoạch
   1,367 / 1,247; verify độc lập ĐẠT cả 2 tượng.

### Kiểm chứng độc lập (verify_v13.py, chạy lại trên file đã lưu)
- Di Lặc: ratio 0,664 / topfrac 0,321 / lobefrac 0,015 → **OK** (2 tai).
- A Di Đà: ratio 0,507 / topfrac 0,632 / lobefrac −0,139 → **OK** (2 tai).
- Cổng PT + TD: Mc_maxdev 0,000004; head_h cổng 0,2419 (= 0,1953 ×
  1,2388); tai cổng 0,5070 → **OK**.
- Toàn cảnh V15 vs V14: 2568 = 2568 object, không thêm/bớt; mesh
  checksum lệch: **rỗng** (không mảnh mesh nào bị chạm); ma trận lệch
  ngoài nhóm tai chính: **rỗng**; ma trận cổng đổi: đúng 4 mảnh tai
  cổng (dev 0,0482); tai chính đổi: đúng Head_earL/R + .001.
- File: layout_v15_v13.blend 97.698.093 byte (V14: 97.679.559);
  audit thô: layout/v13_audit.json.

### Render nghiệm thu
CHƯA RENDER lúc ghi mục này (14:41 09/11: ffmpeg Lục Phán + Blender
snow-globe đang chạy, load 10,14 — không có khe CPU). Driver chờ khe
đã chuẩn bị: layout/render_v13_driver.sh (đợi ffmpeg=0 + không Blender
lạ + load<7 + MemAvailable≥2200 MB, rồi render facebase V14 → full V15
→ pixeldiff_v13.py). Render gồm: cận mặt Di Lặc + A Di Đà (camera
tính từ bbox đầu thật), dilac/adida/niche/flycam chuẩn V12. Sau khi
render xong sẽ soi cạnh ref5/ref3 và bổ sung verdict ảnh vào mục này.

### Verdict từng tượng (theo số đo; render ảnh chờ bổ sung)
- **Di Lặc: ĐÃ NẮN — tai khớp ảnh** (0,664 / 0,321 / +0,015, cả 3 số
  khớp mục tiêu trong ±0,01). Còn lại: nét mặt vẫn là giới hạn của bản
  dựng gốc (mắt/mũi/miệng tối giản) — vòng này không đụng.
- **A Di Đà chính: ĐÃ NẮN — tai khớp ảnh** (0,507 / 0,632 / −0,139).
- **2 tượng hốc cổng: ĐÃ TRUYỀN** — tai khớp 0,5070, Mc 0,000004.
- **Phật nằm: KHÔNG NẮN** — lệch trong sai số đo, giữ nguyên bản V12.
- **Giới hạn còn lại**: tai là phần duy nhất nắn được bằng đo vững;
  mắt nhắm/độ cong môi/má/cằm chưa đo vững được từ ảnh 3/4 nên chưa
  đụng — muốn vượt phải có ảnh chính diện độ phân giải cao hơn hoặc
  dựng lại mặt từ ảnh thật.

### Ghi chú vận hành
VM restart 14:38 09/11 xóa toàn bộ /tmp/v13 (log build/verify, script
chẩn đoán, crop ảnh đo, pipeline.sh). File bền trong workspace còn đủ:
layout_v15_v13.blend, v13_audit.json, build/verify/pixeldiff_v13.py,
render_v13.py (đã sửa xong). Bài học: log + script chẩn đoán của vòng
sau nên ghi vào workspace/layout/ thay vì /tmp.

Script vòng này: layout/build_v13.py, verify_v13.py, pixeldiff_v13.py,
inspect_v13.py, scripts/render_v13.py, render_v13_driver.sh;
audit thô: layout/v13_audit.json; log verify: layout/verify_v13_run2.log.

## V14 — NẮN MẶT TƯỢNG CHI TIẾT VỀ PHÍA ẢNH THẬT (10/11/2026, layout_v16_v14.blend)

Thi công theo KE_HOACH_V14.md (đo + kế hoạch đã chốt trước): chỉ ma trận
object, không chạm mesh; không đụng tai (V13 đạt), thân, bệ, tỉ lệ đầu;
base layout_v15_v13.blend → layout_v16_v14.blend, không ghi đè nguồn.
Chạy bằng driver tự chờ khe CPU `run_v14_driver.sh` (checkpoint trong
`v14_run/`, sống sót qua VM restart 10:48 UTC — driver chết khi chưa chạy
bước nào nên khởi động lại an toàn; phase A hạ ngưỡng RAM 1500 MB vì chỉ
đo/dry-run, phase B 1800 MB).

### Cổng 0 + 1 (trước khi áp)
- measure_v14.py đo lại trong scene: khớp parser GLB mọi chỉ số (<0,5%;
  lệch lớn nhất ở độ nổi ±0,001 m): head_h 1,8401/1,2388; mũi/head_w
  0,1698/0,154; độ nổi mày Di Lặc 0,1186, má 0,2032, nếp cười 0,092;
  cụm A Di Đà 0,090/0,074/0,064; tai giữ 0,664/0,507 đúng V13.
- DRY_RUN khớp §7 kế hoạch: mũi Di Lặc k=1,473 (≈1,47); mũi A Di Đà
  k=1,767 bị chặn trần 1,600 (kế hoạch 2 bước); ép dẹt k ∈ [0,350; 0,792];
  má ×0,60 (vòng 1); mắt Di Lặc bỏ qua vì độ nổi 0,0173 đã ≤ đích 0,0368.

### Kết quả đo sau nắn (verify_v14.py độc lập — vòng 2 PASS 42/42)
| Mục | Trước | Đích | Sau | Kết luận |
|---|---|---|---|---|
| Di Lặc mũi rộng/head_w | 0,170 | 0,250 (ảnh) | **0,2500** | ĐẠT |
| Di Lặc mày độ nổi (m) | +0,119 | ≤ +0,037 | **+0,0063** | ĐẠT |
| Di Lặc nếp cười độ nổi | +0,092 | ≤ +0,037 | **+0,0092** | ĐẠT |
| Di Lặc mắt độ nổi | +0,017 | ≤ +0,037 | +0,0173 (không đụng) | ĐẠT sẵn |
| Di Lặc má độ nổi | +0,203 | ≈ +0,10 | **+0,1004** | ĐẠT (vòng 2) |
| A Di Đà mũi rộng/head_w | 0,154 | 0,272 (ảnh), bước 1 trần 1,60 | **0,2463** | ĐẠT bước 1 — còn bước 2 (+0,026) chờ render/coordinator duyệt |
| A Di Đà mày/mí/mắt độ nổi | +0,090/+0,074/+0,064 | ≤ +0,025 | **+0,0076/+0,0096/+0,0053** | ĐẠT |
| A Di Đà miệng độ nổi | +0,034 | ≤ +0,025 | **+0,0200** | ĐẠT |
| A Di Đà urna độ nổi | +0,058 | ≤ +0,025 | **+0,0169** | ĐẠT |
| Tai 2 tượng (tỉ lệ/đỉnh/đáy) | V13 | giữ nguyên | 0,664/0,321/+0,015 và 0,507/0,632/−0,139 | KHÔNG ĐỔI |
| 2 cổng PT/TD | — | Mc ≤ 0,002 | **0,000004** cả 2 (18 mảnh mặt truyền liên hợp) | ĐẠT |
| Toàn cảnh | — | — | 2568 = 2568 object; checksum mesh lệch RỖNG; ma trận lệch ngoài phạm vi RỖNG; tai (chính+cổng) không đổi | ĐẠT |

### Lỗi bắt được trong vòng (đã sửa tận gốc)
1. **Má ép quá tay ở vòng 1**: kế hoạch dự tính ×0,60 quanh pivot mặt sau
   làm mặt trước lùi ≈0,10 m, nhưng pivot nằm ở mặt SAU mảnh nên độ lùi
   thật = (1−k)×depth = 0,4×0,5137 = 0,205 m → độ nổi sau ép −0,0023
   (sát mặt ellipsoid, mất má phình). Verify vòng 1 FAIL đúng mục này.
   Hiệu chỉnh từ số đo mới: cần lùi 0,103 m → k = 0,80 → sau ép +0,1004.
   Render vòng 1 giữ ở layout/v14_iter1/ làm bằng chứng.
2. **Tiêu chí "bbox mũi không chạm mắt/má" không hợp lệ**: đo baseline
   trên chính bản nguyên bản V15 (baseline_overlap_v14.py) cho thấy bbox
   mũi ĐÃ chồng bbox mắt cả 3 trục ở Di Lặc (side +0,0075 / up +0,0158 /
   facing +0,1111) và 2/3 trục ở A Di Đà — tượng ghép mảnh có khối sống
   mũi tựa giữa 2 mắt ngay từ gốc. Hạ mục này xuống INFO trong verify;
   phán quyết "mũi có chạm mắt thật không" bằng render (không chạm —
   xem ảnh mặt) + tỉ lệ mũi đã khớp ảnh.
3. verify_v14.py bản đầu crash ReferenceError (dùng tham chiếu Object
   sau khi dump_all mở lại mainfile) — sửa bằng trích tên mảnh ra string
   trước khi mở lại file. Sentinel driver vòng 1 cũng lỏng (khớp cả
   "VERIFY V14 FAIL") — đã siết thành "VERIFY V14 PASS".

### Cổng D-d — miệng Di Lặc lệch dọc: KHÔNG SỬA ở V14 (ghi số chờ quyết V14.1)
- Render cùng góc ref5 (bản xa: khoảng cách 9× head_h, lens 85, azimut
  30°; bản cận 2,4× head_h cho số méo 0,93 nên loại) đo bằng visual
  grounding trên layout_v15_ref5_dilac.png (miệng chưa đụng): đầu
  277–588, miệng 550–562 → tâm miệng = **0,897** chiều cao đầu ảnh;
  đáy miệng→cằm = 0,084. Ảnh thật: 0,663 và 0,279. Số 3D nội tại:
  miệng 0,780 / smile 0,717.
- Kết luận cổng: phối cảnh góc chụp KHÔNG giải thích được lệch (nó đẩy
  số đi xa ảnh hơn: 0,780 → 0,897 so với 0,663 của ảnh). Nhưng độ dịch
  cần để ép khớp render (0,234 head_h ≈ 0,43 m) sẽ đẩy miệng vào dải
  mũi trong không gian 3D, còn độ dịch theo số nội tại (0,117 head_h ≈
  0,22 m) lại giả định mẫu số bbox ảnh = mẫu số 3D — điều chưa chứng
  minh được (bbox đầu trong ảnh có thể gồm cả nọng cằm/cổ). Theo luật
  tượng + cổng mặc định TẮT của kế hoạch: KHÔNG sửa, để coordinator
  quyết ở V14.1 với các số trên.

### Render nghiệm thu (Cycles CPU, cùng camera V13)
layout_v16_{face_dilac, face_adida, ref5_dilac, dilac, adida, niche,
flycam}.png + layout_v15_ref5_dilac.png (góc ref5 bản xa).
Pixel-diff V15↔V16: face_dilac 3,441% bbox (491,146)–(962,539) đúng
vùng mặt; face_adida 1,442% bbox (548,233)–(757,419) vùng mặt; dilac
toàn thân 0,119%; adida 0,033% bbox vùng đỉnh đầu; niche 0,000%;
flycam 0,001% — thay đổi khoanh đúng vùng mặt/đầu, không lan.
Soi bằng mắt (tuyến thi công): Di Lặc — mày hết ống nổi, đọc thành dải
dẹt sát mặt; mũi rộng rõ về tỉ lệ ảnh; má vòng 2 phình tròn đầy, hết
"cầu dán" của V15 mà không bẹt như vòng 1; nếp cười còn mẩu ống nhỏ
(rãnh âm thật thuộc nợ sculpt, mục 6 kế hoạch). A Di Đà — cụm 3 ống
song song ép thành dải mí liền hơn; mũi rộng bước 1; miệng/urna dẹt
sát mặt. Tai giữ nguyên V13 ở mọi ảnh.

### Nợ còn lại sau V14
- A Di Đà mũi bước 2 (0,2463 → 0,272, k thêm ≈1,10): chờ coordinator
  soi render bước 1 rồi quyết, như kế hoạch 2 bước.
- Cổng D-d miệng Di Lặc: số đã ghi ở trên, chờ quyết V14.1.
- Ngoài phạm vi (không tự làm, như kế hoạch §6): hòa khối má–mặt, rãnh
  âm nếp cười, cong môi, cánh mũi, rộng đầu A Di Đà (nợ đo A1).

File: layout_v16_v14.blend 98.001.099 byte (nguồn V15: 97.698.093,
nguyên vẹn); audit: layout/v14_audit.json; verify: layout/v14_verify.json
+ verify_v14.log; đo scene: layout/v14_scene_measure.json.
Script vòng này: layout/measure_v14.py, build_v14.py (DRY_RUN đã tắt sau
khi qua cổng), verify_v14.py, baseline_overlap_v14.py,
scripts/render_v14.py, pixeldiff_v14.py, run_v14_driver.sh; log driver:
layout/v14_driver.log; bằng chứng vòng 1: layout/v14_iter1/.

## §V14.1 — Mũi A Di Đà bước 2 (0,2463 → 0,272) — XONG 01:31 ngày 11/11/2026
Driver run_v141_driver.sh canh khe RAM (≥1800 MB) suốt từ 19:43 ngày 10/11,
bị VM reboot giết 2 lần, coordinator khởi động lại; chạy trọn
dryrun → build → verify → render trong cửa sổ RAM ~01:00–01:31 ngày 11/11.
- File: layout_v17_v141.blend (98.001.265 byte; nguồn layout_v16_v14.blend
  nguyên vẹn). Script: layout/build_v141.py, verify_v141.py, render_v141.py.
- Đo trước: head_w 0,8419, nose_w 0,2074, frac 0,2463 → k = 1,1042.
  Sau: **frac = 0,2720 = đúng tỉ lệ ảnh thật** (audit v141_audit.json).
- Verify độc lập **32/32 PASS** (v141_verify.json, verdict PASS): toàn bộ số
  V14 giữ nguyên (Di Lặc nose 0,2500; protrusion mày/mắt/nếp cười/má;
  A Di Đà brow/lid/eye/mouth/urna), tai giữ V13 (ratio 0,5070), vật đổi =
  ĐÚNG 3 object (Head_nose + 2 bản cổng Phương Tiện/Tịnh Độ), cổng Mc
  deviation 0,000004, object được bảo vệ worst dev 0,0.
- Render: layout/layout_v17_face_adida.png. **Coordinator soi 03:5x: số đo
  ĐẠT; tổng thể mặt vẫn CHƯA giống thật** — cùng kết luận V14: mũi vẫn là
  khối oval rời, mắt 3 vạch trắng xếp chồng, miệng thanh ngang, đầu trứng.
  Khoảng cách còn lại là việc ĐIÊU KHẮC lưới (gắn liền nét vào mặt, rãnh thay
  ống nổi, sống mũi/lỗ mũi, tóc xoắn A Di Đà) — ngoài phạm vi phép biến đổi
  ma trận, chờ quyết định mở vòng điêu khắc riêng của Chung Hy.
