# BÁO CÁO V7.3 "GIỐNG THAM CHIẾU" — Web Chùa Online (trai-nghiem-vinh-trang-v7.html)

**Bản dựng cuối: V7.3d — 17.243.005 byte** (assemble từ `v7_parts/` bằng `assemble_v7.py`; release `grep __v6ff` = **0**, hook test chỉ có ở bản TESTLOCAL). Nhân vật giữ nguyên 3 GLB chuẩn rigged; luồng trang nghiêm 10 trạm, wiring giọng V7.1 (day_di đúng 1 lần, s3_giang_duong, s7_tam_biet) và camera kẹp cột chánh điện giữ nguyên. KHÔNG đẩy GitHub ở tuyến này — coordinator soi lại rồi tự đẩy qua web UI + đọc lại blob SHA.

Mốc phụ: V7.3 (17.241.465 B) → V7.3b (17.241.815 B, nâng dây cờ) → V7.3c (17.242.638 B, dời Phòng kinh sách + bỏ 2 cột đèn giữa) → V7.3d (17.243.005 B, texture biển ×2).

---

## 1. VIỆC 1 — MẶT TIỀN + BIỂN (gap lớn nhất của V7.2)

### Chẩn đoán bằng đo (không đoán)
1. **Bug phơi sáng tận gốc:** `module_1.js` đặt exposure 1.12 nhưng `module_6b.js` (init + handler slider độ sáng) ghi đè bằng base **1.02** — mức nâng sáng của V7.2 chưa bao giờ có hiệu lực lúc chạy. Đã sửa cả 2 chỗ về 1.12.
2. Biển V7.2 không đọc được vì 3 lớp nguyên nhân: biển 9,6×1,45 quá nhỏ ở ~35 m; mái tầng 1 (sâu 13, tâm y6,2) nhô tới z≈6,4 hạ xuống y≈4,7 che + đổ bóng lên băng biển; vật liệu MeshStandard bị nắng tây làm tối.
3. Sau khi biển đã lớn (13,4×2,05, MeshBasicMaterial, chữ #FFE066 trên nền #6E1420), ảnh chụp thật cho thấy 2 che khuất mới: **dây cờ z=21 treo đúng tầm băng biển** (treo 4,8, võng 0,75) và **2 cột đèn lồng giấy giữa trục** (x=22/z=30, x=24/z=34) chiếu cầu trắng đúng vào chữ "ÙA"/"NG".

### Sửa
- Biển 13,4×2,05, canvas tăng gấp đôi **3072×512, font 296px, anisotropy 8** (bản 1536/148 vẽ dấu đúng — đã kiểm chứng bằng trang canvas riêng — nhưng ở ~35 m dấu chỉ còn vài pixel màn hình theo phối cảnh; tăng độ phân giải giữ nét chữ qua mip-map).
- Băng kem nhô (28,6×2,15×0,34, mặt trước z=5,39) + chỉ vàng trên/dưới; 8 ô phù điêu sâu 0,24 có lõi vàng; hàng chóp vàng r0,11 dưới mép mái; mái tầng 1 nâng y 6,2→6,5 và rút sâu 13→11,6; cụm chóp trang trí trước trên sườn mái (3 lớp + cầu phát sáng ở đỉnh y9,05).
- Đèn tiền cảnh `frontFill73` (DirectionalLight 0xfff6e0, 0.55, từ (25,20,55)) nâng mặt nam của chánh điện + mặt tượng (nắng chính từ phía tây để mặt nam tối đỏ nâu).
- **Dây cờ nâng 4,8 → 7,0 (võng 0,6):** đo hình học đường ngắm từ camera sân (y≈2) qua đáy cờ ≈6,1 tại z=21 tới biển đạt y≈8,9 > đỉnh biển 5,93 → hết cắt qua băng biển.
- **Bỏ 2 cột đèn lồng giữa trục** (i=3, i=4 trong vòng lặp đèn giấy) — hành lang trục giữa trống như ảnh mẫu; 6 cột còn lại giữ nguyên.

### Nghiệm thu bằng ảnh (1000×2000 thật — xem §4 về bài học độ phân giải)
- `v73_1_mat_tien.png` (từ (23,36)) + `v73_0_spawn.png` (từ spawn (23,50)): mặt tiền vàng sáng nhiều lớp, hàng vòm + cột đỏ + phù điêu rõ; **biển đọc trọn "CHÙA VĨNH TRÀNG"** — coordinator đã chấm **ĐẠT** (22:55 10/11). Nit duy nhất: chữ G cuối hơi chạm một khối lá tiền cảnh ở mép phải khung tại góc (23,36) — lỗi khung hình, không phải lỗi cảnh.
- `v73_3_co_phat_giao.png` (từ (23,24.5)): 2 dây cờ lớn, cờ 5 màu rõ, treo phía trên băng biển.

**Verdict mặt tiền/biển: ĐẠT.**

## 2. VIỆC 2 — HIỆN DIỆN TƯỢNG + CÁC MỤC CHƯA XÁC NHẬN Ở V7.2

| Mục | Bằng chứng | Verdict |
|---|---|---|
| A Di Đà trước–trái | `v73_2b_tuong_adida_tay.png` (góc SE (−6,39)): **trọn tượng trong khung** từ búi tóc (nhục kế) → thân → **đài sen xanh #4E86A8** → bệ đỏ nâu; bảng **"NAM MÔ A DI ĐÀ PHẬT" đủ chữ** | **ĐẠT** |
| Đài sen xanh | Vật liệu riêng `lotusMat73` (color 0x4E86A8, emissive 0x1E4258 ×0,5) cho đài + 10 cánh; phông lá xanh đậm 0x2F5527 sau tượng cho silhouette trắng nổi. Ảnh 2 góc chéo đều đọc rõ dải sen xanh ôm chân tượng | **ĐẠT** |
| Dây cờ Phật giáo ×2 | `v73_3_co_phat_giao.png` + `v73_1_mat_tien.png`: cờ 0,85×0,55 (to hơn bản 0,62×0,42 của V7.2), 2 dây z=33/z=21 | **ĐẠT** |
| Bonsai dọc lối | `v73_4_bonsai.png`: chậu bonsai 2 hàng dọc trục + cặp lớn 2 bên thềm điện | **ĐẠT** |
| NPC áo dài pastel | `v73_5_npc_pastel.png`: NPC nữ áo dài hồng phấn + nón lá (nhuộm lại vertex-color: NPC 0 hồng, 2 tím, 5 kem, 8 đào) | **ĐẠT** |
| Quầy lưu niệm | `v73_5_shop.png`: biển **"CỬA HÀNG / LƯU NIỆM"** (dấu đầy đủ, đọc rõ ở cự ly gần) + quầy + kệ hàng, nhìn qua cổng; hai mép biển bị trụ cổng cắt nhẹ = lỗi khung hình. Chức năng shop đã PASS ở tail-B (mở shop, thêm món, giỏ 89.000đ) | **ĐẠT** |

**Luật tượng được giữ tuyệt đối:** mesh tượng không sửa nét/tỉ lệ; A Di Đà giữ scale đồng dạng ×1,29 của V7.2 (tỉ lệ tượng+bệ ≈ 0,668 chiều cao chánh điện); chỉ thay vật liệu đài sen, phông nền, ánh sáng. Ghi nhận trung thực: tượng web là khối trơn đơn giản (không có nét mặt chạm khắc) — đó là giới hạn mô hình thủ tục từ các vòng trước, thuộc phạm vi tượng Blender/quyết định vòng nắn mặt đang chờ Chung Hy, không thuộc V7.3.

## 3. VIỆC 3 — P12 (FAIL tái lập ở V7.2): ĐÃ TÌM GỐC + SỬA + PASS

### Chẩn đoán (diag_p12_v73, log từng 5 game-giây)
Đường gieo trạng thái sau-P11, teleport (23,10) như tail-A: avatar **kẹt cứng tại (20,31; 7,36)** — đúng biên (khoảng cách 1,20 = R nới) của collider tròn chậu bonsai nhỏ tại (20; 6,2). Cả 2 bước tách trục đều bị chặn, vị trí KHÔNG nằm trong collider (blockDepth = 0) nên cơ chế thoát-kẹt (wedge-escape) không kích hoạt → autoStuck bỏ qua cả 4 waypoint → đường đi rỗng → **hành động trạm kích hoạt từ xa**: journey.nirvana = true từ cách 38 m trong khi station vẫn "hall", silenceDone = false. Đây là toàn bộ chuỗi FAIL "vái PASS nhưng trạm/im lặng/Tiếp FAIL". Lượt tự nhiên qua được vì điểm rời điện thật (17.5; 7.5) tiếp cận từ phía tây chậu, không rơi vào bẫy.

### Sửa (3 lớp, không nới bán kính che lỗi)
1. `module_6a.js` `tryMove`: thêm **trượt xoay** — khi cả 2 bước tách trục bị chặn mà vị trí không nằm trong collider, thử các bước xoay [35,−35,70,−70,110,−110,150,−150]° quanh hướng định đi; mọi ứng viên vẫn qua `pointBlocked` nên không bao giờ xuyên vật.
2. `module_7.js`: auto-walk chỉ chạy hành động trạm khi avatar **thật sự ở trong max(2.5, r) của trạm** — hết kích hoạt từ xa.
3. Via trạm Phật nằm đổi tuyến tránh góc lõm bị niêm phong (tháp trái nới (x≤9,1; z 0,3–3,7) ∩ điện nới (x≥8,5; z≤1,7)): via cuối `[[15,8],[5,5],[2,-2],[4,-20],[8,-32]]`, mọi đoạn đã đo khoảng hở collider.

### Kết quả
- Diag sau vá (bản cuối): avatar đi trơn 55 game-giây tới **station=nirvana**, stuckRounds = 0 suốt đường, **silenceDone = true**, 0 exception.
- **Tail-A: P12 4/4 PASS + P13 3/3 PASS** (tới trạm / đứng lặng 10s / nút Tiếp / vái; thẻ hồi hướng / journey.tower / khép tuyến). Tổng tail-A 8/9 — FAIL duy nhất là check "TAIL module sẵn sàng" timeout lúc nạp module trên SwiftShader chậm; ngay sau đó charsReady = true và mọi check chức năng đều PASS (tail-B đã PASS lại check này — không phải lỗi thật, theo đúng nhận định của coordinator).
- **Lượt tự nhiên: P12 + P13 PASS** trong chuỗi P0–P18 (48 PASS, 0 FAIL — xem §5).

**Verdict P12: ĐẠT (đã đóng).**

## 4. PHÁT HIỆN PHỤ — HỒ ĐÔNG + PHÒNG KINH SÁCH (từ chẩn đoán books)

Tail-B chết ở hop "books" qua 2 lượt. Diag (diag_books2/3) đo được avatar kẹt ở 2 lớp chắn:
- **Hồ đông** `colRect(31.1; 8.5)–(50.9; 23.5)`, nới tới z=24,0 — avatar bám mép nam hồ không qua được.
- **Bonsai (28.7; 26) R nới 1,25** — đâm trực diện: kẹt cứng tại (29,90; 26,47); cộng bonsai lớn (29.2; 6,4) R nới 1,59 + thùng công đức (27.9; 4,9) R 1,3 + tháp phải điện tạo **dải chắn liên tục** phía đông (diag3: kẹt tại (29,03; 8,02)).

Đào sâu hơn: **Phòng kinh sách đặt tại (33,−12) nằm TRONG rect va chạm chánh điện (9..37; −13..1,2)** và điểm đứng (33;−8,4) cũng ở trong rect — không đường đi nào tới được. Đây là lỗi đặt phòng từ các vòng trước, chỉ lộ ra khi V7.1 nối giọng s3_giang_duong cho trạm này.

**Sửa tận gốc:** dời Phòng kinh sách sang **(42;−10,5)** (sau chánh điện, cạnh Giảng đường — đúng nghiên cứu "phòng kinh sách ở phía sau, gần chánh điện"), rect va chạm và điểm đứng trạm → **(42;−7,6)** theo cùng. Tuyến kiểm chứng đổi sang **làn sau lưng điện** (dùng lại các đoạn đã kiểm chứng của tuyến Phật nằm): (23,30)→(23,16)→(15,8)→(5,5)→(2,−2)→(4,−20)→(8,−32)→(20,−24)→(34,−17)→(37,−14,4)→(42,−7,6) — diag4: **11/11 hop REACHED, station=books**.

**Bài học độ phân giải ảnh (đo, không đoán):** bộ ảnh V7.3 đầu chỉ đạt **125×250 px** (thậm chí 65×130) dù script đặt viewport 500×1000 × DSF 2 — vì renderer chốt `setPixelRatio` ngay lúc init theo DSF 0,25 của chế độ verify nhỏ. Đã sửa quy trình chụp: đặt metrics 500×1000 @ DSF 2 **trước** khi navigate và log kích thước canvas từng ảnh; toàn bộ ảnh chốt là **1000×2000 thật** (~0,6–1,3 MB/ảnh).

## 5. KẾT QUẢ VERIFY TỔNG HỢP (bản V7.3c/V7.3d)

| Lượt | Kết quả |
|---|---|
| Diag P12 sau vá | station=nirvana @55gs, silenceDone=true, 0 exception — **PASS** |
| Tail-A (gieo sau-P11) | **P12 4/4 + P13 3/3 PASS**; tổng 8/9 (FAIL = timeout nạp module, không phải chức năng) |
| Lượt tự nhiên (verify_v73_run) | **P0–P18: 48 PASS, 0 FAIL** (gồm day_di đúng 1 lần, P12, P13, shop + s7_tam_biet, bản đồ, niệm kinh, giảng đường, cài đặt); bị VM reboot cắt ở hop books tuyến CŨ — books đã được đóng ở tail-B bên dưới |
| Tail-B lượt 1 (bản V7.2) | 21/23 — books FAIL ×2 (mầm của §4), còn lại PASS gồm 4/4 verdict cột (minDist 0,80/0,80/0,81, đối chứng cam=[300,294]) + trang NPC 0 lỗi |
| Tail-B bản V7.3c | **P14–P18: 13 PASS, 0 FAIL + books 2/2 PASS** ("tới trạm Phòng kinh sách", "s3_giang_duong count=1"); VM reboot giết lượt ở đoạn quay lại điện |
| Mini-pillar (phần còn thiếu của tail-B, logic chép nguyên) | Kẹp cột **3/3 góc tấn công PASS** (minDist 1,50 ≥ 0,78); cổng 0 lỗi JS 2/2 PASS; **NPC vái/chắp tay trước A Di Đà: BẮT ĐƯỢC**. 3 FAIL là giả tạo của lượt rút gọn: vào-lại-điện timeout dưới load cực cao (đã PASS ở 2 lượt tail-B đầy đủ) và ca đối chứng lệch offset camera vì lượt rút gọn không vào được trạng thái inside (ở lượt đầy đủ: cam=[300,294] PASS) |
| Hành trình | **journey 9/9** ở mọi lượt chốt; **0 exception JS, 0 console error** toàn tuyến |

Coordinator đã tuyên bố khép verify về chức năng (23:50 10/11) trên cơ sở trên.

## 6. ĐỐI CHIẾU TỔNG THỂ VỚI ẢNH MẪU 67/68 + THEME 48

| Hạng mục mẫu | V7.2 | V7.3d |
|---|---|---|
| Trời cobalt / grade sáng | ĐẠT | ĐẠT (giữ + sửa bug exposure) |
| Mặt tiền vàng nhiều lớp | CHƯA (tối, phẳng) | **ĐẠT** (`v73_1_mat_tien`) |
| Biển đọc được từ sân | CHƯA | **ĐẠT** (coordinator chấm; nit: G chạm lá tiền cảnh) |
| Tượng trắng nổi + đài sen xanh | CHƯA (khối trắng, sen bợt) | **ĐẠT** (`v73_2b_tuong_adida_tay`) |
| Dây cờ Phật giáo | Chưa xác nhận | **ĐẠT** (`v73_3_co_phat_giao`) |
| Bonsai / tháp đèn đá | Chưa xác nhận | **ĐẠT** (`v73_4_bonsai`, `v73_1`) |
| NPC áo dài pastel | Chưa xác nhận | **ĐẠT** (`v73_5_npc_pastel`) |
| Quầy lưu niệm mái cong (image-48) | Có, chưa có ảnh | **ĐẠT** (`v73_5_shop`) |
| Hồ sen + lan can đá | ĐẠT | ĐẠT (giữ nguyên) |
| UI game của mẫu (Lv/EXP/quest) | Không chép | Không chép (đúng luật trang nghiêm) |

## 7. NỢ / GHI CHÚ CÒN LẠI
- **Động cơ di chuyển:** va chạm đâm trực diện vào collider tròn vẫn có thể kẹt tại chỗ (đã gặp ở bonsai (28.7;26) và (29.2;6,4)); mọi tuyến auto-walk hiện dùng via qua làn trống đã đo nên không chạm, người dùng thật tự lái vòng qua được. Nếu sau này thêm trạm mới, phải đo tuyến như diag books/P12 trước khi nối.
- Tượng web không có nét mặt chạm khắc (xem §2) — ngoài phạm vi V7.3.
- Ảnh `2a_npc_adida` theo format của harness verify vẫn không chụp được (Page.captureScreenshot timeout trên SwiftShader); hành vi NPC vái trước tượng đã xác nhận bằng state dump ở mini-pillar ("BẮT ĐƯỢC").
- Quá trình: VM reboot/SIGTERM giết tiến trình verify **ít nhất 5 lần** trong ngày 10/11 và load có lúc lên 24 (tuyến khác) — các lượt verify dài phải chạy bằng driver tự chờ + log tăng dần như đã làm; số liệu trong báo cáo này đều đọc lại từ log trên đĩa.

## 8. FILE LIÊN QUAN
- Bản dựng: `trai-nghiem-vinh-trang-v7.html` (17.243.005 B) + `trai-nghiem-vinh-trang-v7-TESTLOCAL.html` (bản test, có hook — KHÔNG phát hành).
- Nguồn: `v7_parts/module_1.js / module_2.js / module_6a.js / module_6b.js / module_7.js`, `v7_parts/assemble_v7.py`.
- Ảnh: `v73_shots/` (10 ảnh 1000×2000: spawn, mặt tiền, tượng ×3, cờ, bonsai, NPC pastel, shop ×2).
- Log: `diag_p12_v73_fix.log`, `verify_v73_tailA.log`, `verify_v73_run.log`, `verify_v73_tailB.log`, `verify_v73_pillar.log`, `diag_books2_v73.log`, `diag_books3_v73.log`, `diag_books4_v73.log`.
- Script chẩn đoán/chụp: `diag_p12_v73.mjs`, `diag_books{,2,3,4}_v73.mjs`, `mini_pillar_v73.mjs`, `shots_v73{c..j}.mjs`, driver `run_*_v73.sh`.
