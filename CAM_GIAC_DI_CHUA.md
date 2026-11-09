# CẢM GIÁC ĐI CHÙA — phản hồi Chung Hy 18:51 ngày 06/11/2026 (lệnh nghiên cứu lại)

Chung Hy nói thẳng (nguyên ý): "Còn thiếu nhiều lắm luôn chứ không phải có mỗi cái đó đâu.
So với cái game á, bạn còn thua nhiều lắm. Di chuyển trong chùa này nọ, bạn đâu có
hoàn chỉnh được. Chưa có cảm giác được đi chùa luôn á. Bạn phải nghiên cứu lại nha.
Nhang khói đâu rồi, đường chùa như thế nào, chưa có cảm giác đi chùa luôn. Ánh sáng
của bạn hơi sáng á, bạn phải giảm sáng xíu nữa thì nó mới giống khung cảnh chùa."

## Các điểm phải xử lý (chốt từ phản hồi)
1. **Di chuyển trong chùa chưa hoàn chỉnh** — cần mô hình di chuyển rõ ràng qua khuôn
   viên (so với game/đối thủ: Chùa Sen, Niệm Phật Online, Sansa).
2. **Không có cảm giác đi chùa** — thiếu các yếu tố làm nên trải nghiệm thật:
   - **Nhang khói** (thắp nhang, khói bay) — hiện hoàn toàn không có.
   - **Đường chùa** — tuyến đường người đi lễ thật sự đi: cổng tam quan → sân →
     lư hương/thắp nhang → chánh điện lễ Phật → Di Lặc → Phật nằm → tháp → ra.
   - Âm thanh/hành vi đi kèm (đã có dossier âm thanh 5 vùng — phải gắn vào tuyến đường).
3. **Ánh sáng quá sáng** — giảm sáng, tông trầm ấm trang nghiêm cho cả render 3D lẫn
   bản trải nghiệm web. Render hiện tại dùng nắng mạnh + Standard transform nên
   phẳng và chói như trưa nắng gắt, không ra không khí chùa.
4. Chuẩn so sánh: "cái game" (Chợ Hòa Bình + đối thủ) — mức hoàn chỉnh phải ngang
   một trải nghiệm đi lại được, không phải vài cảnh tĩnh.

## Việc đã giao
- Tuyến nghiên cứu "cảm giác đi chùa": đối thủ (cách di chuyển, không khí) + tuyến
  đường lễ thật ở Vĩnh Tràng + đặc tả khói nhang + đặc tả giảm sáng → bản đặc tả
  trải nghiệm v4 (file này sẽ được bổ sung kết quả).
- Khi render bố cục chạy lại: áp grade trầm (giảm phơi sáng/nắng, tông ấm) vào cả
  hai góc flycam + mặt đất.

---

# ĐẶC TẢ "CẢM GIÁC ĐI CHÙA" — bản nghiên cứu lại (06/11/2026)

Phạm vi: kiểm toán bản trải nghiệm v3 hiện hành (file `trai-nghiem-vinh-trang-v3.html`,
2.487 dòng, Three.js) + đối thủ + tuyến đi lễ thật. Số liệu audit trích trực tiếp từ
code (ghi số dòng); số liệu chùa thật có nguồn ở mục F; mục nào chưa kiểm chứng được
ghi rõ "chưa kiểm chứng" — không bịa.

## A. Kiểm toán v3 so với 4 điểm phản hồi

### A1. Di chuyển — KHÔNG có di chuyển thật, chỉ có nhảy góc máy
- Toàn bộ "di chuyển" là `OrbitControls` (xoay/zoom quanh một tâm) + 5 nút góc máy
  đặt sẵn (`views`: altar / buddha / leftArhats / rightArhats / yard, dòng 946–953),
  chuyển cảnh bằng lerp vị trí camera (dòng 1955). Không WASD, không joystick,
  không chạm-sàn-để-đi, không nhân vật đi bộ trong cảnh 3D (avatar chibi chỉ cúi lạy
  tại chỗ khi bấm nút Lạy Phật).
- Cảnh 3D chỉ là **một nội thất chánh điện** 28×46 m (dòng 1208) + một góc máy "yard"
  nhìn ra. **Không tồn tại trong cảnh:** cổng tam quan, sân, đường đi, hồ, tượng
  Di Lặc, A Di Đà đứng, Phật nằm, tháp — tức là gần như toàn bộ khuôn viên thật.
- "Hành trình 5 chặng" (lớp V2) là checklist giao diện gắn vào nút công cụ: cả 5
  chặng hoàn thành được khi đứng yên một chỗ. Đây chính là gốc của nhận xét
  "di chuyển đâu có hoàn chỉnh" — người dùng không hề *đi* đâu cả.

### A2. Nhang khói — có một bát hương trang trí, không có hành vi thắp nhang
- Trong cảnh chỉ có **1 bát hương trên bàn thờ trong chánh điện** (dòng 1351) với 3
  que nhang tĩnh, đầu phát sáng. Không có lư hương sân (nơi khách thật thắp nhang).
- Khói hiện tại: 55 hạt `THREE.Points` trắng thuần, size 0,25, opacity 0,7 cố định,
  bốc thẳng 0,012/frame (≈0,72 m/giây) từ y=3,6 lên 7,5 rồi reset tức thì (dòng
  1717–1732, 1999–2007). Không lớn dần, không mờ dần, không trôi theo gió, luôn bật
  bất kể người dùng làm gì — đọc như đám mây hoạt hình, không phải khói nhang.
- **Không có tương tác thắp nhang:** chặng 1 của hành trình ghi "Thắp hương dâng lễ"
  nhưng nút của nó (`btn-offering`, dòng 1865) chỉ phát chuông + hiện chữ về dâng
  hoa sen. Người dùng không cầm nhang, không cắm nhang, khói không hề liên quan tới
  hành động của họ.

### A3. Đường chùa — không có
- Không có tuyến đường, không có trạm theo trình tự thật. Năm góc máy đều nằm trong
  một căn phòng; thứ tự bấm tùy ý. Âm thanh cũng chưa gắn theo khu vực: dossier âm
  thanh 5 zone đã có đặc tả (mục 1.4) nhưng **chưa được cài** — v3 chỉ có chuông/mõ
  synth sự kiện, không có lớp ambience nào.

### A4. Ánh sáng — sáng kiểu trưa nắng, đo được bằng số
Code tự đặt tên hệ thống là "CARTOON LIGHTING SYSTEM (BRIGHT & WARM)" (dòng 1148):
- HemisphereLight **3,4**; DirectionalLight (nắng) **2,4**; SpotLight chiếu Phật
  **14,0**; PointLight Phật **6,0**; hai đèn vách **4,5** mỗi bên; đèn nến 2,5;
  vật liệu phát sáng (emissive) tới 5–6.
- Renderer: ACESFilmic + `toneMappingExposure` **1,45**.
- Hệ quả: chủ thể bị "nướng" sáng phẳng như giữa trưa; phần trầm duy nhất là nền
  nâu tối (background/fog 0x35140b) — tương phản nền tối/chủ thể chói, không phải
  không khí trầm ấm. Phía Blender cũng cùng bệnh: nắng 3,2 + view transform
  Standard + trời 0,7 (đã ghi trong phần phản hồi ở đầu file).

### A5. Cái đang có, giữ lại cho v4 (không làm lại)
- Niệm kinh 3 gói + karaoke + mõ/chuông WebAudio; Giảng đường Huệ Đăng (bài giảng);
  chọn profile 3 nhân vật + chú tiểu An; hồi hướng cuối buổi niệm kinh.
- Bộ action của nhân vật GLB đã fit có sẵn **Thắp nhang / Vái / Quỳ / Đi bộ**
  (dossier mục profile) — v4 dùng chính các action này, không cần làm mới.
- Dossier âm thanh 5 zone (cổng / sân & hoa viên / chánh điện / giảng đường /
  khu tháp & tượng), ngân sách tải lần đầu ≤ 1,5 MB, crossfade 1,5–2 giây khi
  chuyển zone — dùng nguyên, chỉ cần *gắn vào tuyến đường* ở mục B.

## B. Đặc tả mô hình di chuyển — "đường chùa"

### B1. Mô hình: đi bộ tự do theo nhân vật + trạm dẫn đường (chuẩn đối thủ đã kiểm chứng)
Cả 3 đối thủ đều dùng **đi bộ tự do bằng avatar**, không ai dùng nhảy góc máy:
- Chùa Sen (hướng dẫn chính thức, cập nhật 04/11/2026): điện thoại = joystick nửa
  trái hoặc chạm sàn để nhân vật tự đi tới; máy tính = WASD/mũi tên hoặc nhấp/giữ
  chuột trên sàn; nút hành động **hiện theo ngữ cảnh khi đứng gần vật** (đến gần
  lư hương thì nút Thắp hương hiện; phím F tương tác); chạm vào vật đích (bồ đoàn,
  tượng, lư hương, chuông) thì nhân vật tự đi tới đó.
- Niệm Phật Online (hướng dẫn FPT): cùng khuôn — kéo nửa trái để đi, WASD/mũi tên,
  đến gần vị trí chức năng rồi chọn nút.
- Sansa (guide người dùng): WASD; bấm "lạy" thì nhân vật tự đi tới bồ đoàn trống;
  vào/ra nhà bằng nút tại cửa.

**Đặc tả v4 (bắt buộc đủ 4 kênh điều khiển):**
1. Máy tính: WASD + phím mũi tên; nhấp chuột lên sàn = đi tới điểm đó (pathfinding
   đơn giản theo polyline đường chùa, tránh vật cản bằng bounding circle).
2. Điện thoại: joystick ảo nửa trái; chạm sàn = đi tới; vuốt nửa phải = nhìn quanh.
3. Nút ngữ cảnh: trong bán kính 2,5 m của vật tương tác → hiện 1 nút lớn duy nhất
   (Thắp nhang / Lạy Phật / Ngồi bồ đoàn / Thỉnh chuông…); phím F/Enter trên máy tính.
4. Chế độ "Đi theo chú tiểu An" (cho cô chú lớn tuổi): bấm 1 nút, nhân vật tự đi
   hết tuyến trạm, dừng ở mỗi trạm và chờ người dùng bấm hành động chính. Thanh góc
   máy cũ giữ lại dưới tên "Xem nhanh" như chế độ hỗ trợ, không phải cách đi chính.
- Camera: bám sau vai nhân vật (third-person, khoảng cách 4–6 m, lerp mềm); khi vào
  chánh điện chuyển góc trong nhà; không cắt cảnh cứng giữa các trạm ngoài trời —
  nhân vật *đi* thật trên đường. Vào nhà: đi qua cửa + fade 0,4 giây.
- Tốc độ đi bộ 1,2–1,4 m/giây (đi lễ là đi chậm); không cho chạy ở khu tháp/tượng.

### B2. Tuyến trạm = tuyến đi lễ thật ở Vĩnh Tràng
Thứ tự đối chiếu nguồn ở mục F (blog hướng dẫn tham quan + bài của Giáo hội):
cổng → hoa viên (A Di Đà, Di Lặc) → chánh điện → Phật Niết Bàn → bảo tháp → về cổng.
Chánh điện đặt trước Di Lặc trong tuyến trải nghiệm vì trạm thắp nhang (S2) phải
xảy ra trước khi vào lễ — đúng thói quen đi lễ thật (thắp nhang ở sân rồi mới vào
chánh điện lạy Phật).

| Trạm | Nơi chốn (khớp bố cục 3D đã khóa) | Người dùng LÀM gì | Âm thanh (zone dossier) |
|---|---|---|---|
| S0 | Cổng tam quan (2 cổng ở hai đầu trước) | Qua cổng, chú tiểu An chào + 1 câu giới thiệu cổng ghép sành sứ; chọn "Tự đi" hoặc "Đi theo An" | Zone Cổng tam quan: gió, chim xa, chuông gió ngẫu nhiên |
| S1 | Hoa viên — tượng A Di Đà đứng trên đài sen xanh (góc trước-trái) | Chiêm bái: bấm Vái (action Vái), điểm chụp hình gợi ý | Zone Sân & hoa viên |
| S2 | **Lư hương lớn giữa sân, trên trục trước thềm chánh điện** | **THẮP NHANG** — toàn bộ tương tác ở mục C; xong thì Vái 1 vái | Zone Sân; chuông nhỏ khi cắm nhang xong |
| S3 | Chánh điện (vào cửa, fade) | Lạy Phật 3 lạy trước bàn thờ; ngồi bồ đoàn → mở niệm kinh; hai dãy La Hán = 2 điểm xem có chú thích | Zone Chánh điện: rất tĩnh, chuông lớn đầu/cuối buổi lễ |
| S4 | Tượng Di Lặc (trái-giữa, trên bệ đá) | Vái; An kể 1 câu về tượng (khánh thành 2010, cao ~20 m — nguồn mục F); điểm chụp hình | Zone Sân & hoa viên |
| S5 | Phật Thích Ca nhập Niết Bàn (sau-trung-phải, trên bệ cao) | Đứng lặng 10 giây (không nút bấm — thiết kế có chủ ý), rồi Vái | Zone Khu tháp & tượng (yên tĩnh nhất) |
| S6 | Bảo tháp 7 tầng (sau tượng Phật nằm) | Khép buổi: Kệ Hồi Hướng (dùng bản đã có ở niệm kinh) + xuất ảnh "Dấu ấn hành trình" | Zone Khu tháp & tượng; 1 tiếng chuông lớn khép buổi |
| S7 | Đường về cổng | Tự đi hoặc An dẫn về; kết thúc mở khóa đi tự do toàn khuôn viên | Crossfade về zone Cổng |

- Mỗi trạm: đúng 1 hành động chính + tối đa 1–2 dòng dữ kiện đã kiểm chứng từ An.
  Không nhiệm vụ phụ, không điểm số hiển thị (giữ nguyên tắc dự án + cảnh báo
  GHPGVN đã ghi trong dossier).
- Giảng đường Huệ Đăng gắn như trạm nhánh từ sân (vào nghe bài giảng) — không nằm
  trên tuyến chính để tuyến chính giữ đúng nhịp đi lễ thật (~10–15 phút online,
  so với 90–120 phút tham quan thật).

## C. Đặc tả khói nhang

### C1. Vị trí lư hương (trong bố cục 3D)
- **Lư hương chính:** giữa sân, trên trục trung tâm, ngay trước thềm chánh điện —
  vị trí khách thật đứng thắp nhang trước khi vào lễ (thông lệ chùa Nam Bộ; ảnh
  ref1 cho thấy trục sân + thềm trống đúng vị trí này). ⚠️ Chưa có ảnh/nguồn nào
  trong tay chụp rõ lư hương sân của Vĩnh Tràng — khi dựng phải đối chiếu lại ảnh
  flycam/toàn cảnh, sai thì dời, không khẳng định đây là vị trí đã kiểm chứng.
- **Hai lư nhỏ:** trước bệ Di Lặc và trước đài A Di Đà (cùng cảnh báo kiểm chứng).
- Trong nhà: giữ bát hương bàn thờ chánh điện như hiện có, thay hệ khói mới.

### C2. Luồng tương tác (web) — "thắp nhang" phải là một hành vi, không phải nút bấm lấy điểm
1. Đến trong 2,5 m của lư hương → nút ngữ cảnh "Thắp nhang" hiện.
2. Bấm → avatar rút 3 que nhang, chơi action **Thắp nhang** (đã có trong GLB);
   đầu nhang bén lửa (chấm sáng cam nhấp nháy 0,8 giây) kèm tiếng lửa rất nhỏ.
3. Avatar **Vái** 1 vái với nhang trên tay (action Vái), giữ 1,5 giây.
4. Nhang được cắm vào lư; cột khói **bật dần trong ~3 giây** (không phụt lên ngay);
   1 tiếng chuông nhỏ (theo dossier: "chuông nhỏ khi thắp nhang xong").
5. Khói ở lư đó **cháy tiếp tới hết phiên**; lư chưa thắp thì không khói. Vào lại
   chùa phiên sau: trạng thái giữ theo localStorage (nhang của "hôm nay").
6. Ở chánh điện, thắp nhang bàn thờ dùng lại đúng luồng này ở bát hương trong nhà.

### C3. Thông số hình ảnh khói
Web (Three.js — thay hệ 55 Points hiện tại bằng sprite mềm):
- Hạt: 90–140 hạt/lư đang cháy (trong nhà: 40), sprite radial-gradient tự vẽ trên
  canvas 128 px, `depthWrite: false`, blending thường (cấm additive — sẽ chói).
- Sinh tại đầu que nhang (bán kính 0,06 m); vận tốc bốc đầu 0,25–0,40 m/giây, tăng
  nhẹ theo chiều cao; tuổi thọ 6–10 giây (trong nhà 8–12 giây, không khí tĩnh).
- Kích thước lớn dần 0,08 m → 0,9–1,4 m; opacity theo đường cong 0 → đỉnh 0,32–0,38
  → 0 (khói nhang thật mỏng — không bao giờ vượt 0,4); màu xám ấm #cfc8bd, nhuốm
  sáng ấm theo nắng.
- Trôi ngang: gió nền 0,05–0,12 m/giây theo +X cộng nhiễu sin tăng dần theo chiều
  cao (cột khói nghiêng và tan, không phải ống khói thẳng đứng).
- Tiêu chuẩn nghiệm thu: nhìn xuyên qua cột khói vẫn thấy tượng phía sau; khói đọc
  được ở khoảng cách 10 m nhưng không che chủ thể ở 3 m.

Render Blender (Cycles, cho tuyến bố cục):
- Ưu tiên: **thẻ billboard khói** — 5–7 mặt phẳng luôn hướng camera, texture khói
  alpha (cùng sprite mềm như web, vẽ lớn 512 px), xếp thành cột hơi nghiêng trên
  lư hương chính + lư Di Lặc. Rẻ, kiểm soát được, không mô phỏng.
- Không dùng mô phỏng thể tích (volume sim) trên máy này: Cycles CPU quá nặng cho
  kết quả không cần thiết ở ảnh tĩnh. Chỉ cân nhắc cho 1 ảnh hero nếu sau này có
  máy mạnh hơn — ghi nợ, không hứa.

## D. Đặc tả giảm sáng / grade "trầm, ấm, trang nghiêm"

Mẫu tham chiếu: ảnh Vĩnh Tràng chụp cuối chiều — vàng mặt tiền bão hòa dưới nắng
xiên ấm, sân đá xám dịu, bóng dài; nội điện trầm, ánh sáng gom thành từng vùng ấm
quanh bàn thờ/nến. Mục tiêu cảm giác: **khoảng 16h30–17h00**, không phải 12h trưa.

### D1. Blender (Cycles) — thay bộ số hiện tại (nắng 3,2 / trời 0,7 / Standard)
| Hạng mục | Hiện tại | Đặc tả mới |
|---|---|---|
| View transform | Standard | **AgX** (ngoại cảnh tuyệt đối không dùng Standard) |
| Exposure (film) | — | 0,85–1,0 |
| Sun energy | 3,2 | **2,2–2,6** |
| Góc nắng | cao, gần đỉnh đầu | hạ thấp, cao độ ~28–35°, hướng tây–tây nam (nắng xiên, bóng dài qua sân) |
| Màu nắng | trắng | ấm: RGB ≈ (1,00 / 0,82 / 0,62) |
| World strength | 0,7 | **0,35–0,45** |
| Hậu kỳ | — | saturation 0,92–0,97; cân bằng trắng lệch ấm nhẹ |
| Nội điện | đã sửa: altar 1200 / key 700 / nến 120, hào quang 2,8 | **giữ nguyên trần này** (đã kiểm chứng hết cháy sáng), không tăng thêm nguồn nào |

### D2. Web (Three.js v4) — thay bộ số đo ở A4
| Hạng mục | v3 hiện tại | Đặc tả v4 |
|---|---|---|
| toneMappingExposure | 1,45 | **1,02** (khoảng cho phép 0,95–1,08) |
| HemisphereLight | 3,4 | **1,15** (trời 0xffe8c4 / đất 0x4a2c17) |
| DirectionalLight nắng | 2,4, gần trắng | **1,5**, màu 0xffd9a3, đặt thấp phía tây |
| SpotLight Phật | 14,0 | **6,5**, penumbra 0,6 |
| PointLight Phật / vách | 6,0 / 4,5×2 | **2,6 / 1,6** mỗi bên |
| Đèn nến/đèn hoa | 2,5 / 1,4 | ≤ **1,2** |
| Emissive vật liệu | tới 5–6 | trần **2,2** |
| Fog | FogExp2 0x35140b, 0,009 | giữ, đổi 0x2a1a10, mật độ 0,007 |
| Lớp phủ CSS trên canvas | không có | vignette ấm: trong suốt ở tâm → rgba(43,20,4,0,28) ở rìa; wash ấm #ffb46b opacity 6–8% (overlay); filter saturate(0,94) contrast(1,03) |
| Nội điện so với ngoài trời | cùng một ngân sách sáng | tối hơn có chủ ý: ánh sáng gom vùng ấm quanh bàn thờ, gỗ tối — đạt bằng ngân sách đèn theo zone, không bằng giảm exposure toàn cục |

Thêm 1 thanh trượt sáng ± trong Cài đặt (phục vụ người lớn tuổi nhìn kém) — rẻ và
tránh tranh cãi hai chiều về độ sáng; mặc định ở đúng grade trên.

## E. Thứ tự xây dựng

**Trải nghiệm v4 (theo thứ tự, effort là ước lượng):**
1. **[L — 3–5 ngày]** Cảnh khuôn viên + avatar đi bộ tự do + khung trạm S0–S7:
   nạp cảnh bố cục 3D (GLB xuất từ tuyến layout) + nhân vật đã fit; 4 kênh điều
   khiển ở B1; va chạm đơn giản + polyline đường chùa. Đây là nền — mọi thứ khác
   gắn lên nó.
2. **[M — 1–2 ngày]** Hệ khói nhang + luồng thắp nhang (mục C) tại lư sân chính và
   bát hương chánh điện; trạng thái cháy theo phiên.
3. **[S — nửa ngày]** Grade ánh sáng D2 cho cả cảnh sân mới lẫn nội điện cũ
   (thuần đổi số + lớp phủ CSS) — làm sớm vì rẻ và chữa đúng phàn nàn trực tiếp.
4. **[M — 1–2 ngày]** Gắn ambience 5 zone của dossier vào tuyến trạm (crossfade
   khi đổi trạm, tải lười, lần đầu ≤ 1,5 MB); tiếng bước chân trên gạch/sỏi theo zone.
5. **[M — 1–2 ngày]** Chế độ "Đi theo chú tiểu An" (tự đi hết tuyến + lời dẫn đã
   kiểm chứng) + khép buổi hồi hướng ở tháp + ảnh Dấu ấn hành trình.

**Gắn vào tuyến render bố cục 3D (khi render mở lại):**
- Áp ngay bộ số D1 cho cả hai góc flycam + mặt đất (đợt render tới).
- Đặt lư hương chính + 2 lư nhỏ theo C1 (dùng model bát nhang/lư trong bộ vật phẩm
  đã kiểm chứng nếu có, thiếu thì ghi nợ model riêng); thẻ khói billboard C3.
- Nhân vật đã fit đứng/đi trên đường chùa, ít nhất 1 nhân vật ở tư thế Thắp nhang
  trước lư chính — ảnh bố cục phải *kể được hành vi đi lễ*, không chỉ xếp công trình.

## F. Nguồn & mức kiểm chứng

**Tuyến đi lễ + dữ kiện chùa (đã đối chiếu ≥ 2 nguồn trừ khi ghi khác):**
- Thứ tự tham quan 5 bước (cổng tam quan → hoa viên A Di Đà/Di Lặc → tiền đường,
  chánh điện → Phật Niết Bàn → bảo tháp → về cổng); khuôn viên ~14.000 m²; Di Lặc
  khánh thành 2010 cao ~20 m; A Di Đà 2008, tượng 18 m trên bệ 7 m; Niết Bàn 2013
  dài ~32 m; bảo tháp 7 tầng sau khu Phật nằm, lưu tro cốt chư tăng/Phật tử:
  https://nucuoimekong.com/chua-vinh-trang (nguồn dẫn lại Cổng thông tin du lịch
  tỉnh Đồng Tháp) + https://didodidays.com/kinh-nghiem-du-lich-chua-vinh-trang-tai-tien-giang/
  + https://dulichvietnam.com.vn/chua-vinh-trang-tien-giang.html
- Hai cổng xây 1930 tên **Phương Tiện** và **Tịnh Độ**; trước chánh điện là sân
  cảnh; Giảng đường Huệ Đăng; chùa hiện là nơi đặt lớp Phật học (khớp dossier):
  https://phatgiao.org.vn/chua-vinh-trang-co-tu-tren-dat-dinh-tuong-xua-d97275.html
- Khách/đoàn đến chùa **thắp hương tại chánh điện**; không khí chùa gắn với hương
  khói khắp nơi (review du khách): https://phatsuonline.vn/tien-giang-phai-doan-trung-uong-mat-tran-to-quoc-viet-nam-tham-truong-ha-chua-vinh-trang/
  và https://www.tripadvisor.co.nz/Attraction_Review-g469417-d6224355-Reviews-Vinh_Trang_Temple-My_Tho_Tien_Giang_Province_Mekong_Delta.html
  (mẹo "mua một bó nhang để dâng" — Trip.com moments:
  https://www.trip.com/moments/detail/my-tho-24763-141386912/)

**Đối thủ — mô hình di chuyển:**
- Chùa Sen, trang hướng dẫn chính thức (cập nhật 04/11/2026): chuasen.com (trang
  hướng dẫn đi chùa online từng bước). Lưu ý thời sự: trang chủ chuasen.com ngày
  06/11/2026 đăng **thông báo tạm dừng hoạt động** — mô hình vẫn là chuẩn tham chiếu,
  nhưng đối thủ này hiện không còn live.
- Niệm Phật Online: https://fpt.vn/tin-tuc/game-di-chua-online-15777.html
- Sansa: guide của cộng đồng người dùng (không phải trang chính thức):
  https://sansatempleweb.com/

**Chưa kiểm chứng — không được dùng làm dữ kiện:**
- **Vị trí chính xác của lư hương sân Vĩnh Tràng:** không nguồn/ảnh nào trong tay
  nêu rõ; vị trí ở C1 là quyết định thiết kế theo thông lệ, phải đối chiếu ảnh
  thật khi dựng.
- **Giờ mở cửa:** các nguồn mâu thuẫn nhau (06:00–23:00 / 07:30–21:00 /
  07:30–18:00) — giữ trạng thái chưa chốt như dossier đã ghi.
- "Hiện cửa giữa chánh điện không mở, khách vào bằng hai cửa bên": 1 nguồn duy
  nhất (bazantravel.com) — chưa dùng.
- "Tụng kinh sáng trước 10h": 1 nguồn duy nhất (anywhere.com) — chưa dùng.
- Địa giới hành chính sau sáp nhập 01/07/2025: nhiều nguồn 2026 ghi chùa thuộc
  phường Mỹ Phong, **tỉnh Đồng Tháp** (không còn Tiền Giang) — có nguồn rõ ràng
  nhưng cách gọi tên trong sản phẩm là quyết định của Chung Hy, chưa tự đổi.

## G. Kiểm toán toàn phổ — cảm giác đi chùa (bổ sung 06/11/2026 theo lệnh mở rộng)

Khói nhang chỉ là một ví dụ. Mục này rà toàn bộ trải nghiệm (web v3 + cảnh/render
3D) đối chiếu một chuyến đi chùa thật. Mức độ: **CHẾT CẢM GIÁC** (không sửa thì
không thể thấy "đang đi chùa") / **NHẬN RA RÕ** / **TINH CHỈNH**.

### G1. Bảng xếp hạng toàn bộ lỗ hổng

| # | Lỗ hổng | Mức | Bằng chứng | Cách sửa (chi tiết ở) |
|---|---|---|---|---|
| K1 | Không có khuôn viên đi được, không có tuyến đường — chỉ nhảy góc máy trong 1 phòng | CHẾT | A1: OrbitControls + 5 view; cảnh = 1 chánh điện 28×46 m | B1–B2 |
| K2 | Chuỗi hành lễ gãy ở lõi: không mua/cầm/châm/cắm nhang; "thắp hương" là 1 dòng toast | CHẾT | A2: btn-offering chỉ phát chuông + chữ dâng hoa | C2 + G2 |
| K3 | Chùa trống người: không khách khác, không sư; thay bằng số giả "28 đang tu tập" + huy hiệu "Cấp 4" | CHẾT | HTML dòng ~608–610: số online **cứng trong code**; nametag tượng cũng có "Cấp" (dòng 1631) | G3 |
| K4 | Không có âm thanh không gian: 0 lớp ambience dù dossier đã đặc tả đủ 5 zone | CHẾT | v3 chỉ có chuông/mõ synth sự kiện; dossier mục 1.4 chưa cài dòng nào | G4 |
| K5 | Lớp game-hóa phủ lên thờ tự: "+5 công đức" bay lên, nhiệm vụ tích điểm, đèn nguyện bán theo gói 20k/50k/100k trong UI lễ | CHẾT | dòng 686, 740–742, 2061–2071, 2143 | G2 |
| K6 | Ánh sáng trưa gắt ở mọi cảnh (web + Blender) | CHẾT | A4 + mục D | D1–D2 |
| K7 | Cung bậc cảm xúc bị đảo: mở màn đã đứng trước bàn thờ (cao trào trước), không có đường vào | CHẾT | camera mở ở view `altar`; không có phố/cổng/sân | G6 |
| N1 | Khói hoạt hình: chấm trắng đặc, luôn bật, không nguồn | NHẬN RA | A2 | C3 |
| N2 | Cánh sen hồng mưa *trong nhà* khắp chánh điện (kỳ ảo), trong khi sân thật không có lá rơi/chim | NHẬN RA | 50 hạt petal rải x ±12, z ±18 trong nội điện (dòng 1700–1715) | G5 |
| N3 | Render bố cục 3D quá thưa người: 3–5 nhân vật / 14.000 m², đứng đông cứng, không ai đang lễ | NHẬN RA | các render layout đã kiểm chứng ở tuyến bố cục | G3 |
| N4 | Thiếu các nghi thức "ngưỡng cửa": cởi dép trước chánh điện, thùng công đức, sạp hoa/nhang ở cổng | NHẬN RA | không tồn tại object/tương tác nào trong v3 | G2 |
| N5 | Hồ chết: nước phẳng đứng yên, không cá (chùa thật có ao cá), đèn nguyện nhắc tới một cái hồ không có trong cảnh web | NHẬN RA | web v3 không có hồ; layout: mặt nước phẳng | G5 |
| N6 | Lửa nến = cầu phát sáng tĩnh, không lay; nhang không cháy ngắn lại, không tro | NHẬN RA | emissive tĩnh, không code flicker | G5 |
| N7 | Biển bảng: trong 3D không có bảng nội quy/chỉ đường; tên cổng chưa kiểm chứng chữ; web thì toàn HUD game | NHẬN RA | A1/G7 | G7 |
| N8 | Thời gian đông cứng ở "trưa vĩnh cửu": không có chế độ chiều tối/đèn lồng như dossier đã đặc tả | NHẬN RA | dossier mục 1.4 (ngày/đêm) chưa cài | D + G4 |

### G2. Chuỗi hành lễ thật vs v3 — từng bước
Trình tự thật (nguồn mục F + thông lệ được các blog/review mô tả): đến nơi (phố
Nguyễn Trung Trực) → mua nhang/hoa ở sạp gần cổng → qua cổng → **thắp nhang ở lư
sân: châm từ đèn dầu/lửa sẵn, cầm nhang khấn, vái, cắm** → bỏ dép, vào chánh điện
lạy Phật → vòng ngắm La Hán → ra sân đi các tượng lớn → ghé thùng công đức (tùy
tâm, theo hướng dẫn tại chùa) → phòng phát hành kinh sách/quầy lưu niệm → ra cổng.

| Bước thật | v3 có không | Nhận xét |
|---|---|---|
| Mua nhang/hoa ở cổng | **Không** | Người dùng không bao giờ *có* nhang trong tay. Sửa: trạm sạp nhỏ ở S0 — "nhận 3 que nhang + bó hoa" (không bán bằng tiền thật; nhận miễn phí như phát tâm) để hành vi cầm nhang tồn tại từ đầu tuyến |
| Châm lửa | **Không** | Không nguồn lửa, không khoảnh khắc bén lửa. Sửa: trong luồng C2, châm tại đèn dầu cạnh lư (hiệu ứng 0,8 giây đã đặc tả) |
| Cầm nhang khấn/vái rồi cắm | **Không** (toast thay thế) | Sửa: C2 đủ 5 nhịp — đây là nhịp cảm xúc quan trọng nhất của chuyến đi |
| Bỏ dép vào chánh điện | **Không** | Sửa rẻ: ở cửa S3, avatar dừng 0,5 giây, dép xuất hiện ngay ngắn bên thềm + dòng An: "Mình bỏ dép ở đây nhé" — chi tiết nhỏ, đúng lễ, người đi chùa thật nhận ra ngay |
| Lạy Phật / ngồi bồ đoàn | Có (tại chỗ, không cần đi tới) | Giữ, nhưng phải *đi tới nơi* mới mở (theo B1) |
| Thùng công đức | **Không có vật này** | Sửa: đặt thùng công đức cạnh cửa chánh điện trong 3D; tương tác = "tùy tâm" không số tiền, không cộng điểm (đúng cảnh báo GHPGVN; khác hẳn đèn nguyện bán theo gói — xem dưới) |
| Phòng kinh sách / lưu niệm | Có shop — nhưng bán vòng trầm 290.000đ + đèn theo gói tiền ngay trong UI lễ | **Đảo vị trí thương mại:** thật thì quầy ở gần cổng/lối ra và lặng lẽ; v3 thì giá tiền nằm giữa không gian thờ. Sửa: shop dời thành trạm cuối S7 cạnh cổng, bỏ mọi gói giá khỏi các tương tác lễ |
| Rút thẻ/xin xăm làm "chặng lễ" | Có (chặng 5) | Thẻ an lạc là cơ chế giữ chân của app, không phải nghi thức đã kiểm chứng ở Vĩnh Tràng — giữ tính năng nhưng đổi khung: gọi là "Dấu ấn mang về", không trình bày như một bước đi lễ |

### G3. Con người — chùa vắng là chùa chết
- Web v3: ngoài avatar người dùng chỉ có tượng. Số "28 đang tu tập" là **chữ cứng**
  — vừa giả vừa phản tác dụng khi người dùng nhìn quanh thấy không một bóng người.
  Xóa ngay; nếu chưa có multiplayer thật thì không hiển thị số người.
- Đặc tả người cho v4 (không cần multiplayer): **NPC khách đi lễ dùng chính 3 GLB
  nhân vật đã fit** (+ biến thể màu áo lam/nâu/xám): 8–14 người trong khuôn viên
  tại mọi thời điểm — vài người đi chậm trên tuyến đường, 2–3 người đứng vái trước
  Di Lặc/A Di Đà (có khói nhang từ lư nhỏ), 1–2 người ngồi bồ đoàn trong chánh
  điện, 1 người quét sân buổi sáng (khớp âm sự kiện "tiếng chổi" trong dossier).
  1–2 **nhà sư áo nâu/vàng** đi chậm ở khu nhà tổ/giảng đường — chỉ đi lại, không
  tương tác, không nói thay chùa điều gì.
- Render bố cục 3D: áp cùng mật độ (tối thiểu 8 nhân vật, ít nhất 2 đang ở tư thế
  lễ/Thắp nhang) — ảnh khuôn viên 14.000 m² mà 3 người đứng rải rác là ảnh "khu
  đất trống có tượng", không phải chùa đang sống.
- Hành vi phải *chậm và có đích*: đi theo tuyến, dừng ở trạm, vái, rồi đi tiếp.
  Cấm NPC đứng xoay vòng/đi xuyên vật — thà ít người mà đúng nhịp.

### G4. Âm thanh theo zone — đối chiếu dossier (mục 1.4 của dossier là chuẩn, mục này chỉ chấm hiện trạng)
| Âm dossier đã đặc tả | v3 hiện tại |
|---|---|
| 5 zone ambience loop + crossfade 1,5–2 s | **0/5** — không có file/loop nào |
| Tiếng đường phố rất xa ở zone cổng, mờ dần vào trong | Không |
| Chim sáng / dế-ếch đêm theo giờ thật; chuông lớn ở mốc 6h/12h/18h | Không |
| Chuông gió cổng + tháp (ngẫu nhiên 20–40 s/lần) | Không |
| Tiếng bước chân trên gạch/sỏi theo zone | Không |
| Chuông lớn decay 8–12 s đầu/cuối buổi; mõ theo hạt | Có synth chuông/mõ (âm sắc còn "điện tử" — nâng cấp partial/noise-burst như dossier mục 1.6) |
| Tiếng tụng xa nhỏ ở chánh điện | Không (karaoke niệm kinh là chữ + mõ, chưa có giọng) |
Kết luận: phần âm thanh đang ở mức "hiệu ứng nút bấm", chưa phải "không gian".
Đây là nửa còn lại của cảm giác đi chùa sau hình ảnh — ưu tiên ngang mục khói.

### G5. Chi tiết sống
- **Chim bồ câu sân chùa:** chưa có ở bất kỳ cảnh nào. Sửa rẻ: 6–10 sprite/model
  chim đơn giản ở sân trước chánh điện — đậu, mổ thóc, bay vụt lên khi avatar đến
  gần (< 3 m) rồi đáp lại chỗ khác. Đây là chi tiết "sân chùa thật" rẻ nhất.
- **Lá bồ đề rơi:** thay mưa cánh sen trong nhà (N2) bằng lá rơi *ngoài sân*:
  20–30 lá sprite rơi xoáy chậm quanh gốc cây lớn; trong chánh điện bỏ hẳn mưa cánh.
- **Hồ & cá:** chùa thật có ao cá (HT. Huệ Minh cho tu sửa ao cá năm 2002 —
  phatgiao.org.vn). Đặc tả: mặt nước có gợn (shader/normal động nhẹ), đàn cá lượn
  dưới mặt nước hồ trước chánh điện (bóng cá đơn giản di chuyển), sen có 3 trạng
  thái (nụ/nở/tàn) đổi theo ngày trong localStorage. Đèn hoa đăng thả ở S-khác
  phải trôi thật trên mặt hồ này, khép vòng với trạm đèn nguyện.
- **Lửa nến:** flicker bằng nhiễu cường độ ±15% ở ~7 Hz + chấm lửa co giãn nhẹ —
  3 dòng code, hết cảm giác "bóng đèn nhựa".
- **Nhang cháy tiếp:** que nhang của người dùng cháy ngắn dần theo thời gian phiên
  (scale Y theo phút), tro cong ở đầu que; lư có lớp tro xám (texture) và luôn có
  vài que của "khách trước" đang cháy — lư hương sống là lư không bao giờ trống.
- **Hoa cúng đổi trạng thái:** bó hoa người dùng dâng ở S2/S3 còn tươi trong ngày,
  hôm sau vào lại đã thay bó mới (ghi theo ngày) — chi tiết "chùa được chăm mỗi
  ngày".

### G6. Cung bậc cảm xúc — đường vào phải là một hành trình lắng dần
Thiết kế tuyến B2 phải kèm **đường cong ồn → tĩnh** đo được:
phố/cổng (tiếng đường xa, gió, chim — sáng nhất, động nhất) → sân hoa viên (chim
gần, lá xào xạc) → trước chánh điện (khói, tiếng người xa rất nhỏ) → trong chánh
điện (gần như tĩnh, chuông/mõ/tụng xa) → khu tháp (tĩnh nhất, chỉ gió cao).
Ánh sáng đi cùng đường cong này: ngoài trời grade chiều ấm (mục D), vào chánh
điện tối hơn một bậc rõ rệt. v3 hiện bắt đầu ở cuối đường cong (bàn thờ) rồi
không đi đâu — sửa bằng S0→S7 + quy tắc "lần đầu vào bắt buộc đi từ cổng".

### G7. Biển bảng — thứ người đi chùa thật nhìn thấy
- Đã có và đúng: bảng tên trên bệ tượng (NAM MÔ A DI ĐÀ PHẬT / NAM MÔ BỔN SƯ
  THÍCH CA MÂU NI PHẬT / chữ Hán Di Lặc) — tuyến điêu khắc đã sửa lỗi ngược chữ
  và kiểm chứng.
- Thiếu: **tên hai cổng Phương Tiện / Tịnh Độ** (có nguồn phatgiao.org.vn) trên
  cổng tam quan trong cảnh; **bảng nội quy** ở cổng (trang phục kín đáo, nói khẽ,
  không chụp ảnh trong chánh điện — nội dung theo các lưu ý đã có nguồn ở mục F,
  trình bày như bảng thật trong sân, không phải popup); **biển chỉ đường** nhỏ ở
  các ngã rẽ sân (theo chi tiết "trở lại cổng theo lối chỉ dẫn" trong nguồn).
- Web v4: mọi nhãn kiểu game (cấp độ, điểm, nametag "Cấp" trên tượng) phải biến
  mất khỏi không gian 3D; nhãn duy nhất trong cảnh là nhãn *của chùa* (tên nơi
  chốn bằng bảng gỗ/đá nhỏ khi đến gần trạm).

### G8. Bổ sung vào thứ tự xây dựng (chèn vào mục E)
- Vào bước 1 (nền): NPC khách + sư theo G3; quy tắc đường cong G6; xóa số online
  giả + huy hiệu cấp + nametag cấp (làm ngay, độc lập, nửa giờ).
- Vào bước 2: trạm nhận nhang/hoa ở cổng + thùng công đức + nhịp bỏ dép (G2).
- Vào bước 4 (âm thanh): đủ bảng G4 theo dossier, không cắt xén.
- Bước 6 mới [S–M]: gói chi tiết sống G5 (bồ câu, lá rơi, cá, flicker nến, tro) —
  rẻ, hiệu quả cảm giác cao, làm sau khi nền chạy được.
- Shop: dời ra trạm cuối cạnh cổng, gỡ mọi mức giá khỏi tương tác lễ (G2).
