# NGHIÊN CỨU "GIỐNG THẬT" V5 — Vì sao model Vĩnh Tràng trông như đồ chơi, và đặc tả sửa

> Ngày: 07/11/2026 (00:0x). Người viết: tuyến nghiên cứu (theo lệnh sau khi Chung Hy bác verdict "đạt" của bố cục V4).
> Cách làm: mở trực tiếp 2 render V4 (`layout/layout_v4_flycam.png`, `layout/layout_v4_ground.png`) và 8 ảnh thật trong `~/workspace/vinh-trang-3d/refs/` (ref9, ref14, ref1, ref2, ref3, ref5, ref6, ref7); **đo màu bằng số** (trung bình vùng pixel, script PIL) trên cả ảnh thật lẫn render để bảng màu có căn cứ đo, không cảm tính.
> Tài liệu kế thừa, không viết lại: `CAM_GIAC_DI_CHUA.md` (audit trải nghiệm + grade D1/D2), `NGHIEN_CUU_SAU_GAME_THAT.md` trục 6 (palette chốt vòng trước), `layout/NOTES.md` (đính chính 00:03 07/11: bố cục đạt, GIỐNG THẬT chưa đạt ~20%).

---

## 0. Kết luận một câu

Render V4 đúng **bố cục** nhưng sai **bề mặt, ánh sáng và mật độ**: 100% bề mặt là màu phẳng đơn sắc không texture, không đổ bóng tiếp xúc (AO), bầu trời là màu nền phẳng, nước là mặt phẳng cyan, cây là khối cầu copy-paste, công trình bị "rửa trôi" màu (desaturate) so với ảnh thật — đó là đúng 5 dấu hiệu kinh điển khiến mắt người đọc cảnh 3D thành "đồ chơi / mô hình giấy". Không phải lỗi hình khối chính; là lỗi **vật liệu + ánh sáng + chi tiết**.

---

## A. BẢNG KHOẢNG CÁCH THEO HẠNG MỤC (render V4 vs ảnh thật)

Mức nghiêm trọng: **S1** = phá cảm giác thật ngay từ cái nhìn đầu · **S2** = nhìn kỹ là thấy giả · **S3** = bóng bẩy.

| # | Hạng mục | Ảnh thật (nguồn) | Render V4 | Mức |
|---|---|---|---|---|
| A1 | **Vật liệu toàn cảnh** | Mọi bề mặt đều có vân: vữa phong hoá, gạch có mạch, ngói có gợn sóng + rêu, đá có vệt nước, sứ cẩn cổng lấp lánh đa sắc (ref1, ref6) | 100% vật liệu là **màu phẳng đơn sắc** (Principled chỉ có Base Color, không image texture, không normal/roughness map). Bề mặt nhẵn như nhựa → dấu hiệu "đồ chơi" số 1 | **S1** |
| A2 | **Đổ bóng / AO** | Bóng nắng gắt, ranh giới sáng–tối rõ; bóng tiếp xúc đậm dưới chân tượng, dưới mái hiên, trong hốc vòm (ref1, ref5) | Bóng rất nhạt, vật như "trôi" trên nền; không có AO bake/SSAO; hốc vòm chánh điện sáng đều như mặt phẳng → thiếu chiều sâu | **S1** |
| A3 | **Màu sắc tổng thể** | Bão hoà cao: trời xanh coban `#0155C9`–`#4F97F9` (đo ref6/ref5), vàng chùa rực, xanh cây đậm `#467542` (đo ref9) | Toàn cảnh **nhạt và xám** (AgX + màu gốc đã nhạt): cỏ đo `#899574` (nhạt, úa) so với cây thật `#467542` (đậm gấp ~2 lần độ bão hoà); trời = nền xám-xanh phẳng không mây | **S1** |
| A4 | **Chánh điện — mái** | Mái ngói **nâu đỏ sẫm, nhiều tầng lớp**, cong đầu đao, bờ nóc có tượng trang trí dày; nhìn flycam mái là mảng tối chủ đạo của khu (ref9, ref1) | Mái **nâu nhạt `#AD8367`** (đo) dạng sọc ngang phẳng, 1 lớp, đầu hông có vạt tam giác lỗi; sáng hơn thật rõ rệt | **S1** |
| A5 | **Chánh điện — mặt tiền** | Vàng **rực bão hoà**; cột tầng trệt **đỏ sẫm** có chạm vàng; song cửa sắt đen hoa văn dày đặc; dải ô thoáng trắng (lattice) chạy ngang; trang trí nổi chi chít 2 tầng (ref1, ref2) | Vàng pastel nhạt; cột lại là **xanh ngọc lam (teal) — sai màu thật**; song cửa vàng mảnh đều tăm tắp; thiếu dải lattice trắng; trang trí rút gọn thành khối hộp trơn | **S1** |
| A6 | **Cổng tam quan** | Tháp cổng cao hẹp, **cẩn sành sứ đa sắc** (rồng sứ, tượng trong hốc, câu đối), là tác phẩm trang trí dày đặc nhất chùa (ref6) | 2 khối be trơn, 1 vòm đơn, vài ô xanh — **không còn nhận ra là cổng Vĩnh Tràng** | **S1** |
| A7 | **Tượng Di Lặc** | **Khổng lồ** — điểm nhấn lớn nhất khuôn viên, ngồi trên bệ là một toà nhà có cầu thang; trắng, có chuỗi tràng hạt, nét mặt rõ (ref9, ref5) | Cục trắng tròn nhỏ trên bệ xám phẳng — **sai tỉ lệ ấn tượng** (dù số đo bệ có thể đúng, bệ bị rút gọn thành slab nên tượng mất vị thế) | **S1** |
| A8 | **Tượng A Di Đà đứng** | Cao ~18–22 m, **đứng trước hàng rào, sát đường**, trên đài sen xanh lớn + bệ đỏ nâu có biển chữ; là tiền cảnh áp đảo (ref14, ref3) | Nhỏ, lọt thỏm trong sân cạnh hồ; đài sen bé; thiếu bệ đỏ + biển | **S2** |
| A9 | **Tượng Phật nằm** | Dài ~32 m trên bệ đá xám cao có **chữ vàng lớn** "NAM MÔ BỔN SƯ…" (ref7, ref9) | Khối trắng trơn trên bệ be, không chữ, bệ thấp và nhạt | **S2** |
| A10 | **Tháp 7 tầng** | Cam đất/ochre, mái từng tầng đỏ cam, nổi bật trên nền trời (ref5, ref9) | Hồng kem nhạt `#9D9D8B` đo ra xám-oliu — **bị rửa màu**, mất chất cam đất | **S2** |
| A11 | **Hồ nước** | Nước **xanh rêu đục / nâu xanh** `#789164` (flycam) – `#5F552F` (mặt đất), có **phản chiếu** tượng/trời, bờ hồ có hàng rào + hoa (ref9, ref5) | Mặt phẳng **cyan-xám `#708F8F`**, không phản chiếu, không gợn — màu của bể bơi đồ chơi | **S1** |
| A12 | **Cây xanh** | Đa dạng nhiệt đới: **cọ/dừa cao** (thân mảnh, tàu lá), bonsai tạo dáng trong chậu lớn, bụi hoa giấy **hồng/đỏ rực**, cây cổ thụ tán bất đối xứng; bao quanh chùa là **rừng dừa đặc** (ref9, ref14, ref3) | ~40 cây **giống hệt nhau**: thân trụ + 1–3 khối cầu xanh nhạt, không cọ, không hoa, không chậu bonsai; ngoài khuôn viên là hư không | **S1** |
| A13 | **Sân / nền đất** | Phần lớn là **sân lát gạch + đất nâu xám** `#898361` (đo ref9), vườn hoa chia ô, hàng rào **vàng** bao quanh toàn khu, ngoài rào là đường + nhà dân + cây (ref9, ref14) | Một mặt phẳng **cỏ xanh nhạt khổng lồ** bao cả khuôn viên (thật gần như không có thảm cỏ lớn), không hàng rào, không đường, không bối cảnh xung quanh — cảnh "lơ lửng trên bàn" | **S1** |
| A14 | **Bầu trời / ánh sáng** | Trời xanh đậm có mây trắng; nắng nhiệt đới gắt (hoặc nắng chiều vàng); tương phản cao (ref1, ref5, ref6) | Nền `#A8B8C4`-ish xám phẳng, không trời, không mây; sáng đều kiểu studio → mất "không khí" | **S1** |
| A15 | **Mật độ chi tiết** | Chi chít: chậu cây, đèn đường, biển bảng, lư hương, người, xe, hàng rào, dây điện… mỗi mét vuông đều có vật (mọi ref) | Cả khuôn viên ~14.000 m² chỉ có ~10 loại vật, phần lớn mặt đất trống trơn; mật độ thấp hơn thật ước **5–10 lần** | **S1** |
| A16 | **Con người** | Khách lễ chùa đông, đủ tư thế (ref5, ref7 tiền cảnh) | 3–5 nhân vật đứng yên, mặt trơn, da/màu phẳng (đã biết từ audit G3) | **S2** |
| A17 | **Tỉ lệ khối phụ** | Nhà phụ, mái che, tường rào, cổng phụ chen nhau quanh chánh điện (ref9) | Thiếu gần hết khối phụ → khuôn viên "sạch" bất thường | **S2** |

**5 khoảng cách lớn nhất (theo thứ tự phá cảm giác thật):**
1. **A1 — Không có texture thật nào**: mọi bề mặt phẳng nhựa. Đây là nguyên nhân gốc của chữ "đồ chơi".
2. **A14+A2 — Ánh sáng/bầu trời phẳng**: không HDRI, không mây, bóng nhạt, không AO → vật không "ngồi" xuống đất.
3. **A3+A13 — Sai bảng màu nền**: cỏ xanh nhạt thay cho sân gạch/đất nâu + cây bị rửa màu → sai "chất Nam Bộ" ngay từ flycam.
4. **A11+A12 — Nước cyan + cây khối cầu copy-paste**: hai thứ đập vào mắt nhất ở flycam đều đang ở dạng placeholder.
5. **A5+A6 — Chánh điện và cổng mất chi tiết trang trí + sai màu cột (teal thay vì đỏ)**: hai công trình nhận diện nhất của chùa bị rút gọn + sai màu.

---

## B. BẢNG MÀU ĐỀ XUẤT (đo từ ảnh thật + chốt vòng trước)

Cách dùng: cột "Albedo đích" là màu bề mặt (sRGB) TRƯỚC khi chiếu sáng — render cuối sẽ tối/sáng theo nắng. Các giá trị "ĐO" là trung bình pixel vùng sạch trong ảnh thật (ảnh đã qua nắng nên chỉ dùng làm mốc bão hoà/tông, không copy nguyên). Đối chiếu render hiện tại đo cùng phương pháp.

| Vật liệu | Ảnh thật (đo) | Render V4 (đo) | **Albedo đích** | Roughness | Ghi chú vật liệu |
|---|---|---|---|---|---|
| Vàng tường chánh điện | rực, bão hoà cao (ref1/ref6 `#B89B5A` vùng cổng) | pastel, xám | **`#D9A441`**, vùng khuất `#B9852F` | 0.75–0.85 | Sơn vữa: noise variation ±8% + vệt phong hoá chân tường |
| Cột tầng trệt + chi tiết sơn son | đỏ sẫm (ref1, ref2) | **teal `#7FB3B0` — SAI** | **`#7E2A22`** điểm chạm vàng `#C9A227` | 0.5 | Cột đỏ là dấu nhận diện; bỏ hẳn teal ở cột (teal chỉ đúng cho… không đâu trong chánh điện thật) |
| Song/cửa sắt chánh điện | đen nâu, hoa văn dày | vàng mảnh | **`#2B2320`** sắt, hoa văn bằng normal/alpha | 0.6, metal 0.4 | Mật độ hoa văn quan trọng hơn màu |
| Mái ngói chánh điện + tháp cổng | nâu đỏ sẫm (flycam mảng tối; ref1) | `#AD8367` nâu nhạt | **`#7C4030`**, biến thiên mảng `#6E382A`–`#8A4A34` | 0.85 | Ngói phải TỐI hơn tường rõ rệt; thêm sóng ngói bằng normal map + rêu mép |
| Đài sen A Di Đà | xanh dương sen (ref3) | xanh nhỏ, nhạt | **`#4E86A8`** cánh sen, đế bệ đỏ nâu `#8A4A3A` | 0.6 | ref3 cho thấy đài sen là xanh dương (không phải xanh lá như chốt cũ theo bố cục khoá — **ghi nhận khác biệt, cần Chung Hy chốt khi dựng**) |
| Tượng trắng (cả 3 tượng lớn) | trắng ấm `#EFE9DD` | trắng xám phẳng | **`#EFE9DD`** + vệt thời tiết rất nhẹ | 0.55 | Bê tông/sơn trắng: roughness map vệt dọc, AO trong nếp áo |
| Bệ đá tượng (Di Lặc, Phật nằm) | đá xám tối có chữ vàng (ref7) | be nhạt trơn | **`#6E675C`** đá, chữ `#D9A441` | 0.9 | Chữ vàng trên bệ là chi tiết nhận diện — phải có (decal) |
| Tháp 7 tầng | cam đất/ochre | `#9D9D8B` xám-oliu | **thân `#C88A4A`**, mái tầng `#A85A38` | 0.8 | Tăng bão hoà mạnh so với hiện tại |
| Cổng tam quan (nền) | vàng đất + sứ đa sắc (ref6) | be trơn | nền **`#C9962E`**, mảnh sứ: cobalt `#2C4A8A`, ngọc `#3F7D5D`, đỏ `#A03A2A`, trắng sứ `#E8E2D4` | 0.45 (sứ bóng hơn nền) | Không texture được hết chi tiết sứ → dùng photo-texture chụp từ ref6 cho mặt cổng (mục D) |
| Nước hồ | `#789164` flycam / `#5F552F` mặt đất (đo) | `#708F8F` cyan | **`#4E5F3A`** + phản chiếu trời/tượng | 0.05–0.15 | Nước đục xanh rêu; bắt buộc có reflection (planar/env) + gợn normal động |
| Sân lát gạch (mặt đất chính) | `#898361` nâu xám (đo ref9) | xám nhạt + cỏ | **`#8A7A63`** gạch/đất, mạch gạch tối hơn 15% | 0.95 | Thay thảm cỏ lớn bằng sân gạch + ô vườn; cỏ chỉ còn dải hẹp |
| Cây lá (tán) | `#467542` đậm (đo ref9) | `#899574` nhạt úa | dải **`#3E6B34` – `#5C8446`** theo cây | 0.9 | Ít nhất 3 tông xanh khác nhau + variation theo instance |
| Hoa giấy / điểm hoa | hồng–đỏ rực (ref3, ref5) | không có | **`#C93B6E`** / `#D94F3D` | 0.8 | Điểm màu bắt buộc quanh tượng + cổng |
| Hàng rào | vàng đồng bộ chùa (ref9, ref14) | không có | **`#C9962E`** | 0.7 | Rào + trụ + song hoa văn đơn giản, chạy kín chu vi |
| Trời (nền + HDRI) | `#0155C9`–`#4F97F9` + mây trắng | xám phẳng | HDRI trời nhiệt đới xanh (mục D) | — | Không dùng màu nền phẳng nữa |

---

## C. KỸ THUẬT GAME 3D THẬT ÁP DỤNG ĐƯỢC (tham chiếu đã kiểm chứng qua web)

Nguyên lý chung rút ra từ tài liệu PBR/game-art (tripo3d.ai — "diffuse-only models look like plastic toys"; rapidpipeline — PBR map set):

1. **PBR texture set thay màu phẳng** — mỗi vật liệu chính cần tối thiểu: albedo (ảnh) + roughness map + normal map. Chỉ riêng việc bề mặt hết "phẳng tuyệt đối" đã loại bỏ dấu hiệu đồ chơi số 1. (Blender: Principled BSDF đủ cổng; Three.js: MeshStandardMaterial đủ cổng.)
2. **HDRI environment** — game/tour 3D dùng HDRI trời thật để lấy phản xạ + sáng môi trường đúng tông; thay world màu phẳng. Cả Blender (World = Environment Texture) lẫn Three.js (PMREM từ HDRI) đều hỗ trợ sẵn.
3. **Ambient Occlusion** — bake AO trong Blender cho công trình/tượng, hoặc SSAO post-process trên web; tạo bóng tiếp xúc ở chân tường, hốc vòm, nếp áo tượng.
4. **Variation chống copy-paste** — cùng 1 asset cây nhưng random hue/scale/rotation theo instance (game dùng instancing + per-instance color); con người cũng vậy. Mắt bắt "giống hệt nhau" rất nhanh.
5. **Weathering/grunge overlay** — lớp bẩn, vệt nước, rêu ở chân tường/mép mái bằng noise mask trộn vào roughness + albedo (kỹ thuật chuẩn trong tutorial texturing Blender): bề mặt "đã qua thời gian" mới thật.
6. **Fog + vignette + color grade cuối** — sương khí quyển nhẹ làm xa mờ dần (Three.js FogExp2 đã có trong đặc tả D2 của audit), grade ấm ở post.
7. **Photo-texture cho chi tiết không dựng nổi** — cổng cẩn sứ và mặt tiền: chụp/cắt từ ảnh thật (ref6, ref1) làm texture/decal lên khối đơn giản — cách các tour 3D ngân sách thấp vẫn đạt nhận diện. (Lưu ý pháp lý ở mục D.)
8. **Mật độ theo lớp** — tiền cảnh chi tiết cao, trung cảnh vừa, hậu cảnh là "rừng" đơn giản + billboard; game không bao giờ để mặt đất trống trơn: scatter (đá, chậu, lá rụng, bụi) bằng Geometry Nodes (Blender) / InstancedMesh (web).

---

## D. NGUỒN ASSET MIỄN PHÍ HỢP LỆ (CC0, tải trực tiếp không cần tài khoản trả phí)

| Nhu cầu | Nguồn | Giấy phép | Ghi chú áp dụng |
|---|---|---|---|
| PBR texture: vữa/plaster, gạch lát sân, đá, bê tông, gỗ, ngói | **Poly Haven** (polyhaven.com/textures) + **ambientCG** (ambientcg.com) | **CC0** toàn catalog (đã kiểm chứng qua web) | Tải bản 1K–2K JPG (Color/NormalGL/Roughness/AO). ambientCG có sẵn bộ "PavingStones", "Plaster", "Concrete", "RoofingTiles" — khớp nhu cầu |
| HDRI trời nhiệt đới / nắng chiều | **Poly Haven HDRIs** | CC0 | Chọn sky nắng gắt (vd nhóm "kloppenheim / noon grass" — chốt tên file khi tải); dùng cho cả Blender world lẫn web PMREM |
| Cây cọ / cây nhiệt đới (model) | Poly Haven models (ít), **Quaternius / Kenney** (CC0, nhưng stylized) | CC0 | Cọ thật dạng scan hiếm ở CC0; phương án chắc: tự dựng cọ đơn giản (thân cong + tàu lá alpha texture từ Poly Haven "leaves" atlas) — alpha lá là chìa khoá hết "khối cầu" |
| Texture lá (alpha) cho cây/billboard | Poly Haven textures (foliage), ambientCG "Atlas" | CC0 | Dùng cho tán cây dạng card chéo — rẻ mà hết đặc |
| Ảnh thật chùa (ref1/ref6…) làm photo-texture cổng/mặt tiền | Ảnh trong `refs/` của dự án | **Chưa rõ nguồn/tác quyền từng ảnh** | CHỈ dùng nội bộ dựng hình; nếu phát hành công khai phải thay bằng ảnh tự chụp hoặc ảnh CC — **ghi nợ pháp lý, cần Chung Hy chốt** (anh đã lệnh bỏ qua điều kiện pháp lý cho việc cúng dường/thu tiền, nhưng tác quyền ảnh bên thứ ba là chuyện khác — nêu để biết, không chặn) |
| Font chữ Hán/Nôm cho biển, câu đối, chữ bệ tượng | Google Fonts (Noto Serif TC/SC) | OFL | Decal chữ vàng: bệ Phật nằm, biển cổng Phương Tiện/Tịnh Độ, biển A Di Đà |

---

## E. KẾ HOẠCH DỰNG THEO ƯU TIÊN + TIÊU CHÍ NGHIỆM THU (đo/nhìn được)

Nguyên tắc nghiệm thu chung cho mọi mục: render lại ĐÚNG 2 góc máy V4 (flycam + ground) + 1 góc cổng + 1 góc Di Lặc, đặt cạnh ảnh thật tương ứng (ref9/ref1/ref6/ref5); mục chỉ "đạt" khi tiêu chí số của nó đạt — **không nghiệm thu bằng cảm tính, không tự báo đạt như vòng V4**.

### P0 — Bề mặt & ánh sáng (tác động lớn nhất, làm trước)

| # | Việc | Tiêu chí nghiệm thu kiểm chứng được |
|---|---|---|
| E1 | **HDRI world + nắng gắt có hướng**: thay nền phẳng bằng HDRI trời xanh; sun theo audit D1 nhưng tăng tương phản (giữ AgX, exposure 0.9–1.0) | Render ground: đo vùng trời trong hình phải có gradient/mây (không còn 1 màu phẳng — kiểm bằng histogram vùng trời ≥ 3 tông); bóng chánh điện xuống sân nhìn rõ ở 100% zoom |
| E2 | **PBR cho 6 vật liệu chủ đạo**: tường vàng, mái ngói, sân gạch, đá bệ, gỗ, sắt — mỗi cái đủ albedo + roughness + normal từ CC0 (mục D) | Zoom 200% ở render ground: nhìn thấy vân bề mặt ở cả 6 vật liệu (checklist tick từng cái); không còn bề mặt nào là màu phẳng tuyệt đối ngoài tượng trắng |
| E3 | **Đổi bảng màu theo mục B** (cột→đỏ son, mái→nâu đỏ sẫm, tháp→cam đất, nước→xanh rêu, cỏ→xanh đậm) | Đo lại bằng script PIL cùng vùng như bảng B: màu render sau grade lệch ≤ ±12 (mỗi kênh RGB) so với "Albedo đích" đã chiếu sáng tương đương ở ảnh thật — hoặc tối thiểu: cột hết teal (đo hue thuộc vùng đỏ), nước hết cyan (G ≤ R+20), mái tối hơn tường ≥ 15% độ sáng |
| E4 | **AO bake** cho chánh điện + 3 tượng lớn + cổng; bật AO pass/SSAO | Render ground: có bóng tiếp xúc tối rõ dưới hiên, chân cột, chân tượng (so sánh trước/sau bằng ảnh đặt cạnh — vùng hốc vòm tối hơn bản V4 ≥ 20% độ sáng đo được) |
| E5 | **Nước hồ thật**: mặt nước có reflection (reflector/envmap) + normal gợn + màu xanh rêu; bờ hồ thêm thành đá + hàng rào thấp | Flycam: hồ phản chiếu thấy bóng trời/cây (có ít nhất 2 tông trên mặt nước, không còn 1 màu); ground góc Di Lặc: mặt nước có điểm sáng nắng (specular) |

### P1 — Nhận diện công trình (sau P0)

| # | Việc | Tiêu chí nghiệm thu |
|---|---|---|
| E6 | **Cổng tam quan**: dựng lại theo ref6 (tháp cao hẹp, 2 tầng mái, hốc tượng giữa) + photo-texture mặt trước từ ref6 + câu đối; làm cả 2 cổng | Đặt cạnh ref6 ở góc cổng: nhận ra đúng cổng Vĩnh Tràng (kiểm bằng mắt theo checklist: có hốc tượng giữa ✓, mái 2 tầng ✓, texture sứ đa sắc ✓, câu đối 2 bên ✓) |
| E7 | **Mặt tiền chánh điện**: thêm dải lattice trắng, dày song cửa + hoa văn (normal/alpha), gờ trang trí nổi 2 tầng, chậu bonsai lớn trước thềm | Đặt cạnh ref1: đếm được ≥ 5/6 lớp chi tiết của ref1 (lattice, cột đỏ, song đen dày, gờ nổi, bonsai chậu, lan can thềm đá) |
| E8 | **Tượng đúng vị thế**: Di Lặc — bệ thành toà nhà có cầu thang + chữ; A Di Đà — đưa ra trước rào sát trục cổng, bệ đỏ + biển; Phật nằm — chữ vàng trên bệ (decal) | Flycam đặt cạnh ref9/ref14: thứ tự kích thước thị giác Di Lặc ≥ chánh điện về độ nổi bật tiền cảnh; chữ trên bệ Phật nằm đọc được ở render ground/góc gần |
| E9 | **Tháp 7 tầng**: sơn lại cam đất + mái tầng đỏ cam + chi tiết lan can từng tầng | Đo màu render theo bảng B (hue vùng cam); đặt cạnh ref5 nhận đúng tháp |

### P2 — Mật độ & bối cảnh (làm sau, chia nhỏ được)

| # | Việc | Tiêu chí nghiệm thu |
|---|---|---|
| E10 | **Hàng rào vàng kín chu vi + cổng phụ + đường nhựa trước chùa** | Flycam: rào chạy kín 4 cạnh khuôn viên, có đường + vỉa trước cổng như ref14 |
| E11 | **Thảm thực vật 3 lớp**: cọ cao (≥ 12 cây), cây tán đa dạng ≥ 5 loại hình (không còn khối cầu đơn), bụi hoa giấy quanh tượng/cổng, bonsai chậu lớn dọc trục | Flycam đặt cạnh ref9: không còn vùng đất trống > 15×15 m không có vật; đếm ≥ 5 dáng cây khác nhau; có ≥ 6 điểm hoa hồng/đỏ |
| E12 | **Nền đất đúng thật**: thay thảm cỏ lớn bằng sân gạch + ô vườn + dải cỏ hẹp; scatter chi tiết nhỏ (chậu, đèn đường, biển, lá rụng) bằng instancing | Đo màu nền flycam: tông chủ đạo thuộc nâu xám `#8A7A63`±15, không còn mảng xanh nhạt > 30% diện tích khuôn viên |
| E13 | **Khối phụ + bối cảnh xa**: nhà phụ/mái che quanh chánh điện (theo ref9), vành đai cây dày quanh rào (billboard/card), vài mái nhà dân xa | Flycam: khuôn viên không còn "lơ lửng" — có vành đai xanh + khối phụ ≥ 4 cụm như ref9 |
| E14 | **Người có đời sống**: ≥ 10 nhân vật, variation màu áo, ≥ 3 đang lễ/đi (nối audit G3/N3) | Đếm trên render flycam + ground: ≥ 10 người, không 2 người giống hệt nhau kề nhau |

### P3 — Bóng bẩy (chỉ khi P0–P2 đạt)

- E15: Weathering pass — vệt nước dưới mái, rêu chân tường, bụi sân (mask noise vào roughness/albedo). Nghiệm thu: zoom 200% chân tường chánh điện thấy vệt tối dọc + rêu xanh ở mép sân.
- E16: Khói nhang + chim + lá rơi theo audit (C/G5) — thuộc trải nghiệm, không tính vào "giống thật" tĩnh.

**Thứ tự bắt buộc: P0 trước** — chỉ riêng P0 (texture + HDRI + đúng màu + AO + nước) đã xử lý 5 khoảng cách lớn nhất và là phần duy nhất có thể nâng cảm giác thật từ ~20% lên vùng "nhìn là chùa thật" mà không cần dựng lại hình khối. P1/P2 là nâng tiếp; **không đảo P2 lên trước P0** (thêm cây/chi tiết lên nền vật liệu phẳng chỉ làm cảnh đông hơn, không thật hơn).

---

## F. NHỮNG GÌ ĐẶC TẢ NÀY KHÔNG LÀM

- Không sửa model, không render — chỉ nghiên cứu + đặc tả (theo lệnh phân công).
- Không thay đặc tả trải nghiệm (đi bộ/nghi lễ/âm thanh) của `CAM_GIAC_DI_CHUA.md` — file đó vẫn là chuẩn cho v4 trải nghiệm; file này là chuẩn cho **vòng vật liệu/bề mặt V5**.
- Hai điểm cần Chung Hy chốt khi dựng: (1) màu đài sen A Di Đà — ảnh ref3 cho **xanh dương**, chốt cũ của bố cục ghi xanh lá theo "bố cục đã khoá"; (2) dùng ảnh ref (chưa rõ tác quyền) làm photo-texture cổng — nội bộ thì được, phát hành cần ảnh thay thế.
