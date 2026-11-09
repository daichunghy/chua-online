# THAM KHẢO CÁC TRANG CHÙA ONLINE KHÁC — Brief áp dụng cho Chùa Vĩnh Tràng 3D

**Ngày lập:** 05/11/2026 (kiểm chứng live tối 05/11/2026)
**Nguồn:** file nghiên cứu trong repo (`Tìm trend đi chùa online.txt`, `Nghiên cứu Chùa Online - Vibe, UGC và Phân tích Đối thủ.txt` — hai file này có nội dung trùng nhau, `Giai_ma_thiet_ke_tinh_nang_va_tam_ly_marketing_Niem_Phat_Online.txt`, RESOURCES.md, NOTES.md, hồ sơ `research-am-thanh-bai-giang-niem-kinh-profile.md`) + kiểm tra trực tiếp niemphat.online (gồm API công khai /api/meta), chuasen.com (gồm trang hướng dẫn chính thức), sansatemple.com.
**Nguyên tắc dự án giữ nguyên:** chùa THẬT (Vĩnh Tràng, tên thật, số liệu có nguồn), không game-hóa công đức, không bán phước.

---

## 1. Hồ sơ từng site

### 1.1. Niệm Phật Online — niemphat.online (Việt Nam)
*Mô hình:* game nhập vai chùa 3D trên trình duyệt — đối thủ trực tiếp và giàu tính năng nhất. *(Nguồn: file giải mã 03/11/2026 + API /api/meta kiểm tra live 05/11/2026.)*
- **20 không gian chùa hư cấu "lấy cảm hứng" chùa thật** (vd chùa "Vô Lượng" ← Khai Nguyên, "Trấn Hồ" ← Trấn Quốc): dựng procedural bằng Three.js (đổi tham số kiến trúc/màu/tượng), KHÔNG dùng tên chùa thật. → Đây là điểm Vĩnh Tràng thắng ngược: chùa thật, tên thật, model từ tư liệu thật.
- **Game-hóa sâu:** 100 cấp độ, EXP cho từng hành động (lạy = 3, đủ vòng tràng hạt = 20…), nhiệm vụ ngày/tuần, điểm danh + streak, bảng xếp hạng, 4 "thiền phái" có hệ số thưởng ×1,3–1,5 theo hành động, 71+ vật phẩm, 2 tiền ảo Sen/Ngọc.
- **Thương mại:** nạp Ngọc qua SePay/VietQR (gói 20k–500k), vật phẩm hiếm giới hạn số lượng (Nón Thần 1.680 Ngọc, giới hạn 5 món), quỹ ủng hộ mở máy chủ có thanh tiến độ — số site tự báo cáo tại 05/11/2026 vẫn là **2.213.960đ / mục tiêu 3.000.000đ** (trùng số nghiên cứu 03/11; lưu ý trường `payOff: true` trong cấu hình live — kênh nạp có thể đang tắt). Doanh thu bán Ngọc: **chưa xác minh được**.
- **Thời khóa chung theo giờ:** cấu hình live có 2 phiên cố định — sáng 05:00 (20 phút), tối 20:00 (30 phút). Đây là cơ chế "cùng tu một giờ" không cần công nghệ multiplayer nặng.
- **Vận hành cộng đồng là gánh nặng thật:** đã phải tắt tạo đạo tràng/chat/nhắn tin, tạm ngừng đổi tên + avatar vì nội dung không phù hợp; có ticker nội quy + giới hạn trẻ em dưới 18 tuổi tối đa 60 phút/ngày; đồng thời có dòng disclaimer đáng học: *"chỉ là phương tiện nhắc nhở tu tập, không thay thế việc đến chùa"*.
- **Lan truyền:** ảnh thành tích có nhân vật + cảnh chùa, chia sẻ Facebook/Zalo kèm link giới thiệu, thưởng hai chiều khi mời bạn; thu thập UTM đầy đủ. Meme tự phát ("hết chỗ ngồi", "nạp VIP lên trụ trì") là động cơ viral chính theo báo Tuổi Trẻ/Znews.

### 1.2. Chùa Sen — chuasen.com (Việt Nam)
*Mô hình:* chùa 3D miễn phí, **không cần đăng ký**, vào nhanh — do một nhà phát triển độc lập xây bằng AI (theo video tự thuật của tác giả, chi phí API "hơn 5.400$" — số liệu tự công bố, chưa kiểm chứng). *(Nguồn: trang chủ + trang hướng dẫn chính thức của site, cập nhật 04/11/2026.)*
- **Luồng đi chùa từng bước rất rõ:** chọn nhân vật (pháp danh tự nhập, giới tính, kiểu + màu áo) → qua cổng tam quan → thắp hương ở lư hương → thỉnh chuông ở gác chuông (**người cùng phòng nghe được tiếng chuông của bạn**) → vào chánh điện lạy Phật → **ngồi xuống bồ đoàn thì bảng công phu mới mở** (Tràng hạt / Tụng kinh / Thiền) → kết buổi bằng **Kệ Hồi Hướng 4 câu**.
- **Mở khóa mềm theo "Hành trình":** Thỉnh chuông và Dâng hoa mở từ cấp 2 — nhưng có công tắc trong Cài đặt "Hiện đủ mọi tính năng" cho người không muốn bị chặn. Mẫu thiết kế đáng học: dẫn dắt người mới mà không khóa cứng.
- **Giữ trạng thái không cần tài khoản:** đóng tab, lần sau vào nhân vật và công phu vẫn được giữ (lưu cục bộ). Có hướng dẫn cài lên màn hình chính (PWA).
- Không thấy cơ chế nạp tiền/trả phí trên trang công khai ("miễn phí", giá 0 VND theo metadata) — mô hình tiền tệ **chưa rõ**.

### 1.3. Sansa — sansatemple.com (Hàn Quốc)
*Mô hình:* tối giản cực đoan — vào nhanh không tài khoản, hóa thân chú tiểu, cùng ngồi yên trong chính điện, gần như không chat, không game-hóa. *(Nguồn: file nghiên cứu trong repo + báo Hàn/Tuổi Trẻ dẫn lại; site live chỉ hiển thị màn hình chờ bằng tiếng Hàn khi fetch text — không kiểm chứng thêm được tính năng.)*
- Số liệu lan truyền được báo chí ghi: ~600.000 lượt truy cập trong 3 ngày, hơn 1 triệu trong tuần đầu (ra mắt 26/10/2026) — **số do báo chí nhà sáng lập cung cấp, chưa kiểm chứng độc lập**.
- Bài học cốt lõi: **viral nhờ một nhu cầu rõ (một chỗ ngồi yên, có người ngồi cùng) + hình ảnh dễ chụp/chia sẻ**, không nhờ số lượng tính năng. Ban đầu chỉ 20 chỗ ngồi trong chánh điện — sự "hết chỗ" tự nó thành nội dung lan truyền.

### 1.4. Các tham chiếu phụ (từ file nghiên cứu)
- **Mô hình Trung Quốc:** thắp hương ảo, gõ mõ điện tử, đèn cầu an, livestream tụng kinh — tương tác nhanh trên điện thoại, không có không gian 3D khám phá. Ít phù hợp hướng "giống thật" của Vĩnh Tràng.
- **Plum Village App:** tham chiếu cho mảng HỌC/nghe pháp — nội dung có nguồn, chuông chánh niệm, trải nghiệm nhẹ. Khớp chuẩn biên soạn trong NOTES.md của repo (bài học có: khởi tâm → chánh pháp cốt lõi có trích nguồn → quán chiếu → trắc nghiệm → "pháp hành trong ngày").
- **Vinamilk "est. 1976, còn bạn?" (2023)** — không phải site chùa, là mẫu UGC: người dùng nhập tên/năm sinh → nhận ngay ảnh cá nhân hóa trong bộ nhận diện → tự chia sẻ. Đây là khuôn mẫu cho ý tưởng "Dấu ấn hành trình / bưu thiếp từ chùa" mà dự án đã chọn hướng trong file nghiên cứu.

---

## 2. Bảng so sánh: pattern × site × Vĩnh Tràng V3

| Pattern | Niệm Phật Online | Chùa Sen | Sansa | Vĩnh Tràng V3 hiện tại |
|---|---|---|---|---|
| Chùa theo nguyên mẫu thật, dùng tên thật | Không (tên hư cấu "lấy cảm hứng") | Không rõ nguyên mẫu | Chùa hư cấu | **CÓ — Vĩnh Tràng thật (lợi thế độc nhất)** |
| Vào ngay, không đăng ký | Có (chọn máy chủ) | **Có, rất mượt** | Có | Có (profile lưu local, không tài khoản) |
| Nhân vật tùy biến (giới tính/áo/pháp danh) | Có, sâu | Có, vừa | Chú tiểu cố định | Có một phần (3 nhân vật có sẵn + mục đích đi chùa; chưa có pháp danh/đổi áo) |
| Đồng hiện diện nhiều người (multiplayer) | Có (WebSocket, chia phòng/máy chủ) | Có (cùng phòng, nghe chuông của nhau) | Có (ngồi cùng, ít tương tác) | **Chưa có** |
| Thời khóa chung theo giờ cố định | **Có (5:00 & 20:00)** | Không thấy | Không thấy | Chưa có |
| Niệm kinh/tụng kinh có hướng dẫn | Có (giọng đọc AI) | Có | Có (nghe kinh) | **Có** (3 gói 5/10/20', karaoke từng câu, mõ/chuông WebAudio) |
| Học Phật pháp có cấu trúc (khóa học + quiz) | Yếu (pháp ngữ ngắn) | Không thấy | Không | **Có — Giảng đường Huệ Đăng, 4 lộ trình (lợi thế riêng)** |
| Thiền có hướng dẫn | Có (5–30') | Có (trong công phu) | Là trọng tâm | Có (thừa hưởng scene gốc; chưa thành module riêng trong V3) |
| Tràng hạt 108 + thỉnh chuông + thắp hương + hoa đăng | Có, đủ bộ | Có, đủ bộ | Một phần | Có (scene gốc + bộ đếm 108 hạt ở gói 20') |
| Khép buổi bằng hồi hướng | Có | **Có (Kệ Hồi Hướng 4 câu)** | Không rõ | Có trong niệm kinh; chưa áp cho mọi loại buổi |
| Ghi nhận hành trình / thẻ chia sẻ được | Ảnh thành tích game (khoe cấp/vật phẩm) | Không rõ | Ảnh chụp màn hình tự phát | Có thẻ an lạc theo ngày; **chưa có ảnh "Dấu ấn hành trình" cá nhân hóa để chia sẻ** |
| Chuỗi ngày / điểm danh | Có (streak + vật phẩm giữ chuỗi) | Không thấy | Không | Có chuỗi ngày + điểm (đang chờ quyết định đổi tên "Dấu ấn hành trình", bỏ điểm hiển thị) |
| Cấp độ / nhiệm vụ / bảng xếp hạng | Có, rất sâu | Có nhẹ (mở khóa theo Hành trình) | Không | Chưa có — **và không nên làm theo hướng đua hạng** |
| Cửa hàng / nạp tiền / quỹ ủng hộ | Có (Ngọc + quỹ tiến độ) | Không thấy | Không | Có shop trưng bày trong scene gốc; không nạp tiền thật; chưa có quỹ ủng hộ |
| Kiểm duyệt/nội quy là tính năng hiển thị | Có (ticker, khóa tính năng khi bị lạm dụng) | Có trang nội quy riêng | Không rõ | Chưa có trang nội quy/disclaimer trong trải nghiệm |

---

## 3. Top ý tưởng NÊN ÁP DỤNG cho Vĩnh Tràng (xếp theo tác động × khả thi)

**1. "Dấu ấn hành trình" — ảnh cá nhân hóa xuất được để chia sẻ (kiểu Vinamilk, không phải ảnh thành tích game)**
- Làm gì: sau hành trình 5 chặng hoặc một buổi niệm kinh/bài giảng, xuất 1 ảnh dọc: cảnh 3D Vĩnh Tràng thật (góc đẹp cố định) + tên người dùng/pháp danh tự nhập + dòng "Hành trình tại Chùa Vĩnh Tràng — Chùa Online" + ngày. Có biến thể khung avatar dịp lễ (Phật đản, Vu Lan — hành vi đã có bằng chứng từ khung avatar của Báo Giác Ngộ/các chùa). Tuyệt đối không ghi cấp độ/điểm công đức lên ảnh, không tự nhận là chứng nhận của chùa thật.
- Tài sản sẵn: profile V3 (đã có tên/mục đích), thẻ an lạc theo ngày (đã có cơ chế seed theo ngày), render 3D Vĩnh Tràng.
- Effort: **M**. Đây là động cơ lan truyền chính mà file nghiên cứu của dự án đã chọn hướng — và là thứ cả 3 đối thủ đều làm dở (ảnh khoe thành tích game) hoặc không làm (Sansa).

**2. Thời khóa chung theo giờ cố định (học Niệm Phật, bỏ multiplayer)**
- Làm gì: 2 khung giờ mỗi ngày (gợi ý sáng 5:30, tối 20:00 — cần đối chiếu giờ công phu thật của Vĩnh Tràng, hiện **chưa có nguồn công bố**, không tự chốt số) mở "buổi chung": đếm ngược trước giờ, vào buổi là gói niệm kinh/thiền có sẵn, chuông khai buổi, cuối buổi hồi hướng + cho biết "hôm nay có N người cùng dự" — chỉ hiển thị khi có số liệu thật từ server; giai đoạn đầu chạy bản không đếm người vẫn trọn vẹn.
- Tài sản sẵn: 3 gói niệm kinh V3 + chuông/mõ WebAudio + cấu trúc hồi hướng.
- Effort: **S–M**. Tạo thói quen quay lại theo GIỜ thay vì theo streak gây áp lực.

**3. Ngồi vào bồ đoàn mới mở công phu (học Chùa Sen)**
- Làm gì: trong scene 3D, các điểm thực hành (bồ đoàn chánh điện, ghế giảng đường) là nơi mở module tương ứng — niệm kinh mở khi nhân vật đã "ngồi", bài giảng mở ở giảng đường. Menu tổng vẫn giữ cho người lớn tuổi dễ tìm.
- Tài sản sẵn: scene 3D + 8 action nhân vật (có Quỳ/Thắp nhang/Vái) + module niệm kinh/bài giảng V3.
- Effort: **S**. Tăng cảm giác "đang ở trong chùa thật" thay vì bấm menu web.

**4. Khép mọi buổi bằng hồi hướng + một dòng ghi nhận tĩnh (học Chùa Sen, mở rộng cái V3 đã có)**
- Làm gì: thiền, nghe giảng, niệm kinh — buổi nào kết thúc cũng qua màn hồi hướng ngắn (Kệ Hồi Hướng) rồi ghi vào "Dấu ấn hành trình" của ngày (không cộng điểm hiển thị). 
- Tài sản sẵn: phần hồi hướng đã có trong niệm kinh V3 + localStorage V3.
- Effort: **S**.

**5. Âm thanh gắn hành động + không gian theo khu vực (học cả hai đối thủ, theo spec dossier đã có)**
- Làm gì: chuông/mõ phát đúng lúc hành động diễn ra trong scene (thỉnh chuông ở gác chuông, mõ theo câu kinh), ambience 5 vùng tải lười (≤1,5MB lần đầu) như spec trong hồ sơ âm thanh; về dài hạn thay bằng ghi âm thật có phép.
- Tài sản sẵn: hồ sơ nghiên cứu âm thanh (đã có spec + nguồn Freesound CC0/CC-BY), WebAudio chuông/mõ hiện tại.
- Effort: **M**.

**6. Onboarding "vào chùa trong 30 giây" + cài PWA (học Chùa Sen/Sansa)**
- Làm gì: màn đầu chỉ 1 chạm để vào sân chùa với nhân vật mặc định; chọn nhân vật/mục đích (đã có ở V3) chuyển thành bước tùy chọn sau khi đã vào; thêm manifest để cài lên màn hình chính; nút to, chữ lớn cho cô chú (đúng phân khúc UGC avatar mà nghiên cứu đã chỉ ra: nhóm 45–70 tuổi trên Facebook/Zalo).
- Tài sản sẵn: profile picker V3 (đảo thứ tự), trang HTML tĩnh (thêm manifest là đủ).
- Effort: **S**.

**7. Mở rộng thư viện bài giảng theo chuẩn NOTES.md từ giáo trình đã có sẵn trong repo**
- Làm gì: mỗi bài theo đúng khung: khởi tâm → trích chánh pháp có nguồn → quán chiếu → quiz 2–3 câu → "pháp hành trong ngày". Nguồn nội dung đã nằm trong repo (`Giáo trình Phật học/`: Phật Học Phổ Thông, Nền Tảng Phật Giáo…) — không phải viết giáo lý tự do. V3 mới có 1 bài mẫu đầy đủ (A1) + khung 4 lộ trình; đây là việc lấp đầy nội dung theo mẫu.
- Tài sản sẵn: giáo trình PDF trong repo + mẫu bài A1 của V3 + chuẩn biên soạn NOTES.md.
- Effort: **M–L** (nặng ở biên soạn/kiểm duyệt nội dung, nhẹ ở kỹ thuật). Cần người duyệt giáo lý — câu hỏi mở đã ghi trong dossier.

**8. (Cân nhắc sau, không làm ngay) Quỹ ủng hộ minh bạch theo mục tiêu vận hành cụ thể**
- Niệm Phật chứng minh được cơ chế thanh tiến độ + mục tiêu cụ thể tạo niềm tin. Nhưng với Vĩnh Tràng chỉ nên làm khi có pháp nhân/đối tác rõ ràng và tách bạch hoàn toàn khỏi mọi hoạt động tu tập trong app; **không** gắn ủng hộ với điểm, vật phẩm hay "phước". Effort: **L + pháp lý**. Để trong danh sách chờ quyết định, không khuyến nghị triển khai ở giai đoạn này.

### Không nên sao chép (đã cân nhắc và loại)
- **Vòng quay lộc / phần thưởng ngẫu nhiên** — biến thực hành thành may rủi.
- **Bảng xếp hạng công đức, EXP cho hành động lễ bái, hệ số thưởng theo thiền phái** — gắn số đo vào tu tập và tông phái; trái cảnh báo của GHPGVN (02/11/2026) về "tích điểm, tranh thứ hạng, trả tiền đổi phước" đã ghi trong dossier.
- **Vật phẩm giả tưởng kiểu game** (vũ khí Tây Du Ký, linh thú bay…) — Niệm Phật đang bán; trái định vị "giống thật" của Vĩnh Tràng. Vật phẩm của Vĩnh Tràng nên là 21 món thật trong catalog repo.
- **Chùa hư cấu mượn cảm hứng chùa thật** — hướng ngược lại lợi thế cốt lõi của dự án.
- **Streak có hình phạt mất chuỗi / vật phẩm giữ chuỗi bán tiền** — giữ chuỗi ngày dạng ghi nhận nhẹ như V3 hiện tại là đủ.

---

## 4. Chưa kiểm chứng & nhạy cảm — đọc trước khi dùng số liệu

- **Số lượt truy cập Sansa (600k/3 ngày, 1 triệu/tuần):** từ báo chí + nhà sáng lập; chưa có nguồn độc lập. Chỉ dùng như "báo chí ghi nhận".
- **Quỹ ủng hộ Niệm Phật 2.213.960đ:** số do chính site trả về qua API công khai (kiểm tra lại 05/11/2026 vẫn nguyên số này) — không phải sao kê kiểm toán; không suy ra được doanh thu hay lợi nhuận. Doanh thu bán Ngọc: không có dữ liệu công khai đáng tin.
- **Chùa Sen "làm bằng AI, tốn 5.400$ API":** lời tự thuật của tác giả trên YouTube, chưa kiểm chứng; chỉ nên rút bài học về tốc độ làm sản phẩm, không trích như dữ kiện.
- **Hai file nghiên cứu trong repo** (`Tìm trend…` và `Nghiên cứu Chùa Online - Vibe, UGC…`) có nội dung **trùng nhau** — thực chất là một bản nghiên cứu, tránh đếm thành 2 nguồn độc lập.
- **Giờ công phu chính thức của chùa Vĩnh Tràng:** chưa tìm thấy nguồn công bố (đã ghi trong dossier) — mọi "thời khóa chung" trong app phải ghi là giờ của nền tảng, không mạo nhận lịch của chùa.
- **Pháp lý/hình ảnh:** tái hiện 3D chùa thật + dùng tên chùa thật cần cơ sở đồng ý của tự viện khi thương mại hóa; ảnh cá nhân hóa có mặt người dùng cần xin phép xử lý ảnh và cho xóa (điểm đã nêu trong file nghiên cứu UGC).
- **Tuyên bố của GHPGVN (02/11/2026):** công nghệ hỗ trợ học hỏi, không thay thế tu học tại chùa; tránh tích điểm/tranh hạng/trả tiền đổi phước. Mọi tính năng giữ chân của Vĩnh Tràng phải đối chiếu điều này — đây cũng là lý do V3 còn chờ quyết định đổi "điểm công đức" thành "Dấu ấn hành trình".

---

*Brief này chỉ dùng nguồn repo + kiểm tra live ngày 05/11/2026 như ghi ở từng mục; không đẩy lên GitHub theo yêu cầu.*
