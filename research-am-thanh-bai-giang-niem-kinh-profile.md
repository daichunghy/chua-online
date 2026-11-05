# Hồ sơ nghiên cứu: Âm thanh – Bài giảng học viện – Niệm kinh – Profile nhân vật

**Dự án:** Chùa Online — Chùa Vĩnh Tràng (repo `daichunghy/chua-online`)
**Ngày nghiên cứu:** 2026-11-05
**Phạm vi:** 4 chủ đề Logan yêu cầu: (1) âm thanh, (2) bài giảng trong học viện, (3) niệm kinh, (4) profile nhân vật.

**Quy ước nhãn trong toàn văn:**

- ✅ **Đã kiểm chứng** — có nguồn web cụ thể, dẫn URL tại chỗ.
- ⚠️ **Chưa kiểm chứng** — không tìm thấy nguồn đáng tin; tuyệt đối không dùng làm dữ kiện trong sản phẩm cho tới khi xác minh.
- 🎨 **Đề xuất thiết kế** — ý tưởng của hồ sơ này, không phải dữ kiện về chùa thật.

---

## 0. Bối cảnh chung và nguyên tắc thiết kế

### 0.1 Dữ kiện nền về Chùa Vĩnh Tràng (✅ đã kiểm chứng)

| Dữ kiện | Nội dung | Nguồn |
|---|---|---|
| Vị trí | Ấp Mỹ An, xã Mỹ Phong, TP. Mỹ Tho (đường Nguyễn Trung Trực); khuôn viên khoảng 2 ha | pagoda.amazingvietnam.vn — http://pagoda.amazingvietnam.vn/2021/09/chua-vinh-trang.html |
| Hệ phái | Bắc tông (Đại thừa); là tổ đình dòng Lâm Tế – Trí Huệ | pagoda.amazingvietnam.vn (dẫn sách *Phật giáo Tiền Giang – Lược sử và những ngôi chùa*, HT. Thích Huệ Thông, 2002) |
| Lịch sử vắn tắt | Thảo am do Tri huyện Bùi Công Đạt xây đầu thế kỷ XIX; năm 1849 HT. Thích Huệ Đăng xây thành đại tự, đặt tên Vĩnh Tràng (từ cặp đối "Vĩnh cửu đối sơn hà / Trường tồn tề thiên địa") | pagoda.amazingvietnam.vn; dulichtiengiang.com.vn |
| Địa vị | Di tích kiến trúc nghệ thuật cấp quốc gia (công nhận 1984); đặt Văn phòng Ban Trị sự GHPGVN tỉnh từ 1983 đến nay; nơi tổ chức Đại hội Phật giáo tỉnh, Đại Giới đàn, khóa An cư, lễ Phật Đản | pagoda.amazingvietnam.vn; Nghiên cứu Tôn giáo số 2–2018 (timtailieu.vn) |
| Hạng mục trong khuôn viên (theo mô tả nguồn) | Sân kiểng, tượng Phật Thích Ca tham thiền dưới cội bồ đề, ao sen + tượng Quan Thế Âm bên phải, vườn tháp cổ, hội trường, phòng phát hành kinh sách | pagoda.amazingvietnam.vn |

⚠️ **Lưu ý hành chính:** sau đợt sáp nhập tỉnh 2025, một số báo Phật giáo năm 2026 đã ghi địa chỉ Mỹ Tho thuộc **tỉnh Đồng Tháp** (ví dụ phatsuonline.vn, bài họp mặt đầu năm 2026 của Trường TCPH Tiền Giang: "phường Mỹ Tho, tỉnh Đồng Tháp"). Sản phẩm cần Logan chốt cách ghi địa danh (Tiền Giang theo thói quen/di tích, hay Đồng Tháp theo hành chính hiện hành) — hồ sơ này không tự quyết.

### 0.2 Bối cảnh thị trường "đi chùa online" (✅ đã kiểm chứng)

- **Sansa (Hàn Quốc):** chùa ảo 3D do Park Jin-won xây bằng "vibe coding", đạt 600.000 lượt truy cập sau 3 ngày, chạm 1 triệu lượt vào 1/11; người dùng hóa thân chú tiểu, làm 108 lễ bái, lần tràng hạt, tụng kinh, gõ mõ trong không gian 3D có tiếng tụng phát sẵn; không có chat. (blogtamsu.vn dẫn VnExpress/Korea Herald — https://blogtamsu.vn/p/di-chua-online-140985)
- **Niệm Phật Online (Việt Nam):** game trình duyệt 3D (niemphat.online) với lạy Phật, tụng kinh, lần tràng hạt, thiền, thắp hương, kèm cơ chế game: nhiệm vụ, cấp độ, vật phẩm, bảng xếp hạng. (fpt.vn — https://fpt.vn/tin-tuc/game-di-chua-online-15777.html)
- **Chanmi (Hàn Quốc, mô phỏng nhà thờ Công giáo):** chuông kinh Truyền tin vang **3 lần/ngày vào 6h, 12h, 18h** — mẫu "âm thanh theo lịch cố định" đáng học. (twaslnews1.twaslnews.com — https://twaslnews1.twaslnews.com/6969811/)

### 0.3 Quan điểm của Giáo hội — ràng buộc thiết kế bắt buộc (✅ đã kiểm chứng)

Ngày 2/11/2026, đại diện GHPGVN trao đổi về trào lưu "đi chùa online" (báo Tin tức và Dân tộc, đăng lại trên kenh14.vn — https://kenh14.vn/giao-hoi-phat-giao-viet-nam-noi-gi-ve-trao-luu-di-chua-online-215261103142543026.chn):

- HT. Thích Huệ Thông: công nghệ mở thêm kênh tiếp cận Phật giáo (nghe thuyết pháp, theo dõi tụng kinh, thiền định trực tuyến) — vai trò **hỗ trợ**, đáng khuyến khích trong khuôn khổ hướng dẫn đúng.
- TT. Thích Minh Nhẫn (phụ trách chuyển đổi số, Ban Thông tin – Truyền thông TW): thực hành online **không thay thế hoàn toàn** trải nghiệm tại tự viện; cần phân biệt vai trò hỗ trợ của công nghệ với thực hành tôn giáo thật.
- Bài viết trên website Giáo hội (được dẫn lại) cảnh báo thiết kế "kích thích người dùng bấm liên tục, tích điểm, tranh thứ hạng hoặc trả tiền để nhận lời hứa về phước báo".
- Luật Tín ngưỡng, tôn giáo 2026 (hiệu lực 1/1/2027) bổ sung quy định về hoạt động tín ngưỡng, tôn giáo trên không gian mạng.

🎨 **Suy ra 4 quy tắc cứng cho sản phẩm của mình:**

1. Mọi màn hình đều có dòng định vị: *"Trải nghiệm hỗ trợ tìm hiểu và thực hành tại nhà — không thay thế việc đến chùa."*
2. Điểm "công đức" của bản V2 giữ nguyên vai trò **dấu ấn hành trình cá nhân** (ghi nhận mình đã làm gì), không bảng xếp hạng, không đổi điểm lấy "phước", không bán vật phẩm bằng tiền thật kèm hứa hẹn tâm linh.
3. Nội dung kinh/giảng chỉ dùng bản được phép phổ biến; ghi rõ xuất xứ trong ứng dụng.
4. Âm thanh tụng niệm dùng giọng người thật khi có phép; giọng máy (TTS) không giả danh là tiếng tụng của quý thầy.

---

## 1. ÂM THANH (Soundscape)

### 1.1 Hiện trạng trong repo (✅ đã kiểm chứng từ mã nguồn)

File trải nghiệm hiện tại (`trai-nghiem-goc.html`, bản V2 tại `trai-nghiem-vinh-trang-v2.html`) **không dùng file audio nào** — toàn bộ âm thanh được tổng hợp bằng WebAudio:

- `playBell()`: oscillator sine quét tần 587,33 Hz (D5) → 293,66 Hz, decay 3,8 giây — mô phỏng tiếng chuông.
- `playMokugyo()`: oscillator triangle 340 → 140 Hz trong 0,15 giây — mô phỏng tiếng mõ.
- Nút bật/tắt duy nhất: `#btn-audio-toggle` ("🔔 Chuông Mõ: Bật/Tắt").
- Bản V2 overlay chưa có lớp âm thanh riêng; điểm công đức + chuỗi ngày lưu ở localStorage khóa `chuaOnlineV2`.

**Đánh giá:** cách tổng hợp (synth) cho chuông/mõ sự kiện là đúng hướng cho web (0 KB tải thêm, không lo bản quyền), nhưng âm sắc còn "điện tử": chuông thật có phổ harmonic không nguyên (inharmonic partials) và decay dài hơn; mõ thật là tiếng gõ gỗ có nhiễu (noise burst) chứ không phải sóng triangle thuần. Lớp **ambience** (gió, chim, nước, tiếng người xa) và **tiếng tụng** hiện chưa có.

### 1.2 Bài học từ các sản phẩm dẫn đầu (✅ đã kiểm chứng)

| Sản phẩm | Cách làm âm thanh | Bài học rút ra |
|---|---|---|
| **Plum Village App** (plumvillage.org — https://plumvillage.org/mindfulness/mindful-apps) | "Bell of mindfulness": chuông chánh niệm kêu theo khoảng thời gian người dùng đặt (mặc định gợi ý mỗi 15 phút) để dừng lại thở 3 hơi; thư viện tụng niệm, thiền hướng dẫn, **tiếng thiên nhiên thu tại tu viện**; tải offline; 300+ bài pháp thoại dạng podcast | (a) Chuông theo lịch/khoảng là tính năng giữ chân cốt lõi; (b) âm thanh thu tại chính tu viện tạo tính chân thực khác biệt; (c) mọi nội dung nghe được đều tải offline |
| **Sansa** (Hàn Quốc) | Tiếng tụng phát sẵn trong không gian 3D; thao tác gõ mõ/lần hạt có phản hồi âm thanh | Âm thanh là "linh hồn" của cảnh 3D; thiếu âm thanh thì cảnh chết |
| **Chanmi** | Chuông kêu đúng 6h/12h/18h mỗi ngày | Âm thanh gắn **mốc giờ cố định trong ngày** tạo thói quen quay lại |
| **RESONANCE / các web soundscape thuần WebAudio** (resonance.craig-45c.workers.dev) | Toàn bộ soundscape (mưa, gió, chuông gió…) **tổng hợp thời gian thực bằng Web Audio API — zero file**; nhiều lớp chạy đồng thời, mỗi lớp có volume riêng | Với lớp thiên nhiên đơn giản (gió, mưa, chuông gió), synth giúp dung lượng = 0 và trộn lớp linh hoạt |

### 1.3 Âm thanh thật của Chùa Vĩnh Tràng — những gì biết và chưa biết

✅ **Biết:** chùa Bắc tông có hai thời công phu sáng/chiều theo truyền thống Thiền môn (xem mục 3), có chuông, mõ, khánh trong chánh điện như mọi chùa Bắc tông Việt Nam; khuôn viên có ao sen, vườn cây — âm cảnh thiên nhiên miền Tây sông nước (gió, chim, nước).

⚠️ **Chưa kiểm chứng (không tìm thấy nguồn công bố chính thức):**

- **Thời khóa tụng niệm chính thức hằng ngày của chùa Vĩnh Tràng** — tìm trên phatgiao.org.vn, phatsuonline.vn và các trang giới thiệu chùa không thấy công bố giờ công phu. **Không được bịa giờ**; trong sản phẩm chỉ ghi "giờ gợi ý theo thông lệ" (mục 3.4).
- **Giờ mở cửa chính thức:** các trang du lịch ghi **không thống nhất** — 5h30–21h00 (dulichbinhminh.com), 6h00–23h00 (nucuoimekong.com), 6h30–18h30 (tourdulichbentre.com, tiphay.vn), 7h00–21h00 (saigonstartravel.com, vietsensetravel.com), 7h30–18h00 (trip.com). Đây đều là nguồn du lịch không chính thức → ⚠️ chưa kiểm chứng; chỉ dùng được làm khoảng tham khảo "sáng sớm đến tối" cho chế độ ngày/đêm trong cảnh 3D.

🎨 **Hướng chân thực nhất (khớp luật "đối chiếu thật" của dự án):** xin phép chùa ghi âm thực địa 1 buổi công phu + âm cảnh sân chùa (30–60 phút, máy ghi âm phổ thông cũng đủ cho web sau khi nén). Đây là tài sản âm thanh không đối thủ nào có — đúng định vị "chùa thật" của dự án. Việc xin phép thuộc về Logan; hồ sơ chỉ đề xuất.

### 1.4 Đặc tả âm thanh theo zone (🎨 đề xuất thiết kế)

Mỗi zone có 3 lớp: **(A) ambience nền** (loop, luôn chạy khi ở zone), **(B) âm sự kiện** (one-shot khi có hoạt động), **(C) âm tương tác** (phản hồi thao tác của người dùng). Chuyển zone = crossfade 1,5–2 giây, không cắt đột ngột.

| Zone | (A) Ambience nền | (B) Âm sự kiện | (C) Tương tác |
|---|---|---|---|
| **Cổng tam quan** | Gió nhẹ qua cây, chim xa, tiếng đường phố rất xa và nhỏ (đặc trưng chùa sát đường Nguyễn Trung Trực) | Chuông gió dưới mái cổng (synth hoặc sample) khi gió "thổi" ngẫu nhiên 20–40s/lần | Tiếng bước chân trên gạch khi nhân vật di chuyển |
| **Sân & hoa viên** | Chim buổi sáng (theo giờ thật của máy người dùng: sáng = chim + gió; tối = dế/ếch miền Tây, rất nhẹ) | Tiếng chổi quét sân vào khung "giờ quét sân" buổi sáng (one-shot khi vào zone lần đầu) | Tiếng nước khi tương tác hồ sen; lá xào xạc khi chạm cây |
| **Chánh điện** | Rất tĩnh: tiếng tụng xa nhỏ (nếu người dùng bật "chế độ khóa lễ" thì rõ dần theo mục 3), tiếng mõ nhịp đều ở chế độ niệm kinh | Chuông lớn (sample thật, decay 8–12s) khi bắt đầu/kết thúc hành lễ; khánh khi lạy | Mõ theo từng lần click lần hạt (giữ synth hiện tại, nâng cấp âm sắc); chuông nhỏ khi thắp nhang xong |
| **Giảng đường** | Tĩnh, hơi vang phòng (reverb nhẹ) | Giọng giảng sư (mục 2) — âm thanh chính của zone, các lớp khác duck xuống −12 dB | Tiếng lật trang/phím khi mở tài liệu; chuông thỉnh giảng đầu buổi |
| **Khu tháp & tượng** | Gió cao, chim, yên tĩnh nhất toàn cảnh | Chuông gió treo tháp (nếu có tương tác chạm) | Tiếng bước chân chậm trên sỏi |

**Chế độ ngày/đêm:** lấy giờ thật từ máy người dùng — 5h–18h dùng bộ ambience ngày, 18h–5h dùng bộ đêm + đèn lồng trong cảnh 3D; đúng các mốc 6h/12h/18h phát 1 tiếng chuông lớn toàn cảnh (học Chanmi) nếu người dùng đang mở trang và đã bật âm thanh.

### 1.5 Nguồn âm thanh miễn phí / có phép

| Nguồn | Điều kiện | Đánh giá cho dự án |
|---|---|---|
| **Freesound.org** (✅ đã kiểm chứng cơ chế giấy phép) | 3 loại Creative Commons: **CC0** (dùng tự do, kể cả thương mại, không cần ghi công), **CC-BY** (phải ghi công tác giả), **CC-BY-NC** (ghi công + **cấm thương mại**). Phải kiểm tra giấy phép **từng file** | Dùng được nếu chỉ chọn CC0/CC-BY và lập bảng ghi công trong app. Ví dụ đã tìm thấy: "Temple chanting interior" thu tại chùa Gakwonsa, Hàn Quốc — CC0 (https://freesound.org/people/3bagbrew/sounds/345028/); bản tụng + tiếng xu cúng dường tại chùa Tokyo — CC0 (https://freesound.org/people/timothyd4y/sounds/473789/); có cả sample mõ (mokugyo/wooden fish), chuông bát (singing bowl), thậm chí bản ghi "máy niệm Phật" trong chùa Việt Nam (mục tìm kiếm tag buddhism+temple: https://freesound.org/browse/tags/?f=tag%3A%22buddhism%22+tag%3A%22temple%22) |
| **Thu âm thực địa tại Vĩnh Tràng** (🎨 đề xuất) | Cần xin phép chùa; là tài sản riêng của dự án | Ưu tiên số 1 về lâu dài — đúng chất "chùa thật" |
| **Thu âm studio tình nguyện** (🎨 đề xuất) | Quý thầy/Phật tử tụng mẫu, ký đồng ý phổ biến | Cho mục niệm kinh (mục 3) và bài giảng (mục 2) |
| **Synth bằng WebAudio** | Không bản quyền, 0 KB | Chuông/mõ sự kiện + gió/mưa nền đơn giản; giữ và nâng cấp code hiện tại |

⚠️ **Cảnh báo kỹ thuật:** file gốc trên Freesound thường là WAV/FLAC rất nặng (bản "Temple chanting interior" dài 6:42 nặng **101,6 MB**). Tuyệt đối không nhúng nguyên bản — phải chuyển mã (transcode) theo ngân sách ở mục 1.6.

### 1.6 Đặc tả triển khai — Âm thanh

**Kiến trúc:**

- Một `AudioEngine` duy nhất (mở rộng code WebAudio hiện có trong file trải nghiệm), gồm: `masterGain` → các bus `ambience`, `ritual` (chuông/mõ/tụng), `voice` (giảng), `ui`. Ducking: khi `voice` hoặc phiên tụng đang phát, `ambience` tự hạ −9 đến −12 dB (dùng `GainNode.gain` ramp 300 ms).
- Khởi tạo `AudioContext` **chỉ sau thao tác chạm đầu tiên** của người dùng (nút "Vào chùa") — chính sách autoplay của trình duyệt chặn âm thanh trước tương tác; đây cũng là lý do nút toggle hiện tại hoạt động đúng.
- Trạng thái bật/tắt + âm lượng từng lớp lưu vào localStorage (bổ sung vào khóa `chuaOnlineV2` hiện có: `audio: {master, ambience, ritual}`), mặc định: ambience BẬT nhỏ (0,35), ritual BẬT, voice BẬT.

**Nâng cấp synth chuông/mõ (thay 2 hàm hiện tại):**

- Chuông: cộng 4–5 partial không nguyên (ví dụ tỉ lệ 1 : 2,02 : 2,74 : 3,76 : 5,4 so với tần fundamental), mỗi partial một gain decay riêng (partial cao tắt nhanh hơn) → hết cảm giác "chuông điện tử". Chuông lớn chánh điện: fundamental ~196–262 Hz, decay tổng 8–12 giây. Chuông nhỏ: ~587 Hz như hiện tại.
- Mõ: thay sóng triangle bằng noise burst qua bandpass filter (trung tâm ~900–1.200 Hz) + 1 oscillator gõ ngắn → gần tiếng gỗ thật hơn; giữ độ dài ~0,15 giây.

**Định dạng & ngân sách dung lượng (toàn bộ lớp audio):**

| Loại | Định dạng | Thông số | Ngân sách |
|---|---|---|---|
| Ambience loop mỗi zone | Opus (fallback AAC) | stereo 48–64 kbps, loop 60–120 giây, crossfade loop liền mạch | 0,4–0,9 MB/file; tổng 5 zone ≤ 4 MB, **tải lười theo zone** (chỉ tải zone đang đứng + preload zone kề) |
| Chuông/mõ/khánh sample (nếu dùng sample thay synth) | Opus/MP3 | mono 64 kbps | ≤ 250 KB/file |
| Tiếng tụng (mục 3) | Opus | **mono** 40–48 kbps (giọng người) | ~0,35 MB/phút → phiên 20 phút ≈ 7 MB, **stream, không preload** |
| Bài giảng (mục 2) | Opus | mono 32–48 kbps | 10 phút ≈ 2,4–3,6 MB, stream + cho tải offline |
| **Tổng tải lần đầu vào trang** | | | **≤ 1,5 MB** (chỉ ambience zone cổng + UI); phần còn lại tải theo nhu cầu |

**Quy tắc vận hành:**

- Trang ẩn (tab không active) quá 60 giây → tự pause ambience (tiết kiệm pin/CPU), resume khi quay lại.
- Tôn trọng `prefers-reduced-motion`/cài đặt im lặng của hệ điều hành di động: không tự phát khi máy đang ở chế độ im lặng nếu chưa có tương tác.
- Mọi file lấy từ Freesound phải ghi vào `credits` trong app: tên file, tác giả, giấy phép, URL — chỉ nhận CC0 và CC-BY.

---

## 2. BÀI GIẢNG TRONG HỌC VIỆN (Giảng đường)

### 2.1 Kiểm chứng: quan hệ giữa Chùa Vĩnh Tràng và Trường Trung cấp Phật học Tiền Giang

Giả định ban đầu "chùa Vĩnh Tràng là nơi đặt Trường TCPH Tiền Giang" — kết quả kiểm chứng: **đúng về gốc gác và đúng một phần ở hiện tại**, cần diễn đạt chính xác như sau:

| Mốc | Dữ kiện (✅ đã kiểm chứng) | Nguồn |
|---|---|---|
| 1985 | Ban Trị sự GHPGVN tỉnh Tiền Giang thành lập (tháng 1/1985) | phatgiaodongthap.org |
| 1990 | Theo Quyết định 101/QĐ-HĐTS và Công văn 48/CV-UB (15/5/1990), **Trường Cơ bản Phật học tỉnh Tiền Giang được thành lập và đặt tại chùa Vĩnh Tràng** | phatgiaodongthap.org — https://phatgiaodongthap.org/tien-giang-truong-trung-cap-phat-hoc-tiep-doan-thanh-tra-ban-giao-duc-phat-giao-trung-uong-den-tham-va-lam-viec-d2878.html |
| 1998 | Trường (sau đổi tên Trường Trung cấp Phật học) **dời trụ sở về chùa Phật Ân** (số 5 Ngô Quyền, phường 7, TP. Mỹ Tho) — trụ sở chính hiện nay ở đây | phatgiaodongthap.org (bài trên) |
| 2019 | Thông báo chiêu sinh Lớp **Cao đẳng Phật học** Khóa III trực thuộc Trường TCPH: văn phòng lớp đặt tại chùa Vĩnh Tràng; **Tăng sinh nội trú tại chùa Vĩnh Tràng**, Ni sinh nội trú tại chùa Phổ Đức; học phí và chỗ ở miễn phí | phatgiao.org.vn — https://phatgiao.org.vn/tien-giang-thong-bao-chieu-sinh-cao-dang-phat-hoc-khoa-iii-2019-2021-d34655.html |
| 2023 | Trường tiếp đoàn Học viện Viên Quang (Đài Loan) **tại trụ sở Lớp Cao đẳng Phật học — chùa Vĩnh Tràng**; ký kết hợp tác giáo dục với Đại học Hoa Phạm (Đài Loan) cũng diễn ra tại đây (2024) | phatsuonline.vn — https://www.phatsuonline.vn/tags/truong-trung-cap-phat-hoc-tien-giang |
| 2024 | Lễ Tốt nghiệp Lớp Cao đẳng Phật học Khóa V và tổng Khai giảng năm học 2024–2025 của Trường TCPH Tiền Giang tổ chức **tại Giảng đường Huệ Đăng — Tổ đình Vĩnh Tràng** | phatsuonline.vn (trang thẻ trên) |
| Tổng kết | Qua 32 năm, trường đã đào tạo 8 khóa với gần 1.000 Tăng Ni sinh | phatgiaodongthap.org |

✅ **Kết luận dùng cho sản phẩm:** Vĩnh Tràng là **cái nôi của Trường TCPH Tiền Giang (1990)**, hiện là **trụ sở Lớp Cao đẳng Phật học** của trường và là nơi tổ chức các lễ lớn của trường tại **Giảng đường Huệ Đăng**. Tránh ghi "trụ sở Trường TCPH Tiền Giang đặt tại chùa Vĩnh Tràng" (đã dời về chùa Phật Ân từ 1998).

🎨 Đây là lợi thế nội dung có thật và rất riêng: khu "Học viện" trong trải nghiệm online có thể kể đúng câu chuyện này — một ngôi chùa cổ vừa là di tích quốc gia vừa là nơi đào tạo Tăng Ni hơn ba thập kỷ.

### 2.2 Trường Phật học dạy những gì (✅ đã kiểm chứng — chương trình hệ Trung cấp toàn quốc)

- Hệ Trung cấp Phật học đào tạo **4 năm**, do Ban Giáo dục Tăng Ni Trung ương hướng dẫn khung; chương trình gồm **nội điển** và **ngoại điển**. (phatgiao.org.vn — https://phatgiao.org.vn/giao-duc-va-dao-tao-tang-ni-sinh-he-trung-cap-phat-hoc-thach-thuc-va-giai-phap-d43917.html)
- **Nội điển** (giáo lý): các bộ môn **Kinh, Luật, Luận**, sử học và văn học Phật giáo.
- **Ngoại điển** (kiến thức xã hội bổ trợ): văn học, lịch sử, triết học, xã hội học, ngoại ngữ; học viên chưa đủ văn hóa phải học bổ túc theo chương trình Bộ GD&ĐT.
- Bộ giáo trình thống nhất của Ban Giáo dục Tăng Ni TW gồm **35 cuốn, 6 nhóm: Kinh, Luật, Luận, văn học, sử học, ngôn ngữ**; mỗi bài Kinh/Luật/Luận có 6 phần: phiên âm–dịch nghĩa, giải thích thuật ngữ, phân tích nội dung, ứng dụng thực tiễn, câu hỏi–thảo luận, đọc thêm. (Quỹ Đạo Phật Ngày Nay — https://quydaophatngaynay.org/thu-ngo-tro-duyen-an-tong-sach-giao-khoa-cho-33-truong-trung-cap-phat-hoc-gd6-c84-6/)
- Ví dụ danh mục môn thật của một cơ sở TCPH (thi học kỳ, phatsuonline.vn — https://phatsuonline.vn/vinh-long-co-so-iii-truong-trung-cap-phat-hoc-tinh-to-chuc-thi-hoc-ky-ii-nam-thu-i-khoa-v-2025-2026-53): Kinh Bát Đại Nhân Giác, Nhị Khóa Hiệp Giải, Kinh Hiền Nhân, luật Tỳ-ni (Trường Hàng Luật), Ý nghĩa và Thực hành Căn bản Nghi lễ Phật giáo, Đức Phật và Thánh Chúng, Khuyến Phát Bồ Đề Tâm Văn, Sơ Đẳng Phật Học Giáo Khoa Thư, Phật Học Danh Số, Hán văn, Anh văn, Việt văn.
- Hình thức học truyền thống trong trường: **thuyết giảng** của giáo thọ, **vấn đáp/thảo luận** theo bài, thi tự luận + trắc nghiệm. (phatsuonline.vn, bài thi học kỳ trên)

⚠️ Chương trình chi tiết riêng của Trường TCPH Tiền Giang (thời khóa biểu từng khóa, danh sách giáo thọ hiện tại) không công bố đầy đủ trên web — không suy diễn; phần dưới đây là thiết kế chuyển thể cho cư sĩ, không phải sao chép chương trình của trường.

### 2.3 Thiết kế "Học viện online" trong giảng đường (🎨 đề xuất thiết kế)

**Định vị:** thư viện bài giảng cho **cư sĩ tại gia** (không phải đào tạo Tăng Ni), học theo lộ trình, mỗi bài ngắn, có kiểm tra nhẹ và một câu suy ngẫm. Giảng đường trong cảnh 3D là "cửa vào" của tính năng; nhân vật giảng sư (mục 4) đứng lớp.

**Cấu trúc thư viện — 4 lộ trình (map từ chương trình nội/ngoại điển của trường Phật học, giản lược cho cư sĩ):**

| Lộ trình | Nội dung | Map từ chương trình thật |
|---|---|---|
| **A. Nhập môn Phật pháp** (6 bài) | Đức Phật và thánh chúng; Tam bảo; cách lễ Phật, chắp tay, xá chào đúng phép; nghi lễ căn bản khi đến chùa | "Đức Phật và Thánh Chúng", "Ý nghĩa và Thực hành Căn bản Nghi lễ Phật giáo" |
| **B. Kinh điển nhập môn** (8 bài) | Tâm Kinh (ý nghĩa từng đoạn); Chú Đại Bi và hạnh nguyện Quan Âm; Kinh A Di Đà và pháp môn niệm Phật; Bát Đại Nhân Giác | Môn Kinh + Nhị Khóa Hiệp Giải |
| **C. Sống an trong đời thường** (6 bài) | Khuyến phát Bồ đề tâm (ứng dụng); sám hối là gì; chánh niệm khi giận, khi lo; hồi hướng và phát nguyện | "Khuyến Phát Bồ Đề Tâm Văn" + phần "ứng dụng thực tiễn" trong cấu trúc bài học của bộ giáo trình |
| **D. Hiểu về chùa Vĩnh Tràng** (4 bài) | Lịch sử tổ đình (theo dữ kiện ✅ ở mục 0.1 và 2.1); kiến trúc Á–Âu của chánh điện; câu chuyện Trường Phật học 1990; các tượng lớn trong khuôn viên | Ngoại điển: sử học — nội dung riêng của dự án, mọi dữ kiện phải qua kiểm chứng như hồ sơ này |

**Định dạng mỗi bài học (theo đúng 6 phần của bài học Kinh/Luật/Luận trong giáo trình thống nhất, rút gọn):**

1. **Nghe giảng** — audio 10–20 phút (hoặc video nếu có nguồn được phép).
2. **Tóm tắt chữ** — 300–500 chữ + thuật ngữ Phật học có chú thích (học theo phần "giải thích thuật ngữ").
3. **Câu chuyện/thí dụ** — 1 tình huống đời thường (học theo phần "ứng dụng thực tiễn").
4. **Quiz** — 3 câu trắc nghiệm, chấm ngay, giải thích đáp án.
5. **Suy ngẫm (reflection)** — 1 câu hỏi mở, người dùng tự viết 1–3 dòng, lưu local (không gửi đi đâu).
6. **Hành trì gợi ý** — 1 việc nhỏ gắn với các tính năng khác (tụng 1 biến Tâm Kinh ở mục 3, thả 1 hoa đăng…).

**Hình thức buổi học:**

- **Thuyết giảng:** phát audio, transcript chạy đồng bộ highlight theo đoạn (dạng karaoke thu nhỏ, dùng chung engine đồng bộ với mục 3.3).
- **Vấn đáp:** sau mỗi bài có mục "Hỏi đáp thường gặp" dạng văn bản (câu hỏi cư sĩ hay hỏi + trả lời ngắn, có nguồn) — mô phỏng truyền thống vấn đáp trong trường Phật học; ⚠️ nội dung trả lời phải được kiểm duyệt bởi người có chuyên môn trước khi phát hành, không để mô hình AI tự trả lời giáo lý trong sản phẩm.
- **Lịch lớp:** 🎨 đề xuất 2 buổi cố định/tuần trong app (ví dụ tối thứ Năm 20h và sáng Chủ nhật 8h — mở "lớp trực tiếp": bài giảng mới phát hành + nhắc nhở). Đây là **lịch của ứng dụng, không phải lịch của Trường TCPH** — ghi nhãn rõ để không gây hiểu nhầm.
- **Chuỗi học tập:** hoàn thành 1 bài = 1 dấu ấn vào hồ sơ (mục 4); đủ 1 lộ trình = huy hiệu + mở khóa bộ thẻ an lạc đặc biệt. Không xếp hạng giữa người dùng (theo quy tắc mục 0.3).

**Nguồn nội dung bài giảng — thứ tự ưu tiên:**

1. Bài giảng ghi âm/ghi hình được **xin phép phổ biến** từ quý thầy từng giảng tại Vĩnh Tràng/giảng đường Huệ Đăng (nếu Logan xin được) — giá trị chân thực cao nhất.
2. Bài giảng công khai của các giảng sư uy tín có điều khoản cho phép nhúng (ví dụ nhúng YouTube chính chủ qua trình phát chính thức — tôn trọng điều khoản nền tảng, không tải về phát lại).
3. Nội dung chữ tự biên soạn theo giáo trình thống nhất 35 cuốn (dẫn nguồn), đọc thu âm bởi tình nguyện viên — ghi rõ "bài đọc tóm lược", không mạo danh bài giảng của quý thầy.

⚠️ Không scrape/tải lại audio pháp thoại từ YouTube hay website chùa khác để phát trong app khi chưa có phép — rủi ro bản quyền và sai lệch tôn nghiêm.

### 2.4 Đặc tả triển khai — Bài giảng

**Mô hình dữ liệu (JSON tĩnh, không cần backend ở giai đoạn 1):**

```json
{
  "courseId": "kinh-dien-nhap-mon",
  "title": "Kinh điển nhập môn",
  "lessons": [{
    "id": "tam-kinh-01",
    "title": "Tâm Kinh — 'Không' không phải là hư vô",
    "audioUrl": "audio/lectures/tam-kinh-01.opus",
    "durationSec": 780,
    "transcriptUrl": "data/transcripts/tam-kinh-01.json",
    "summary": "…",
    "terms": [{"term": "Ngũ uẩn", "note": "…"}],
    "quiz": [{"q": "…", "options": ["…"], "answer": 0, "explain": "…"}],
    "reflection": "Hôm nay, điều gì bạn đang nắm chặt nhất?",
    "practice": {"type": "chant", "ref": "tam-kinh", "label": "Tụng Tâm Kinh 1 biến"}
  }]
}
```

**Thông số media:** audio giọng nói mono Opus 32–48 kbps (13 phút ≈ 2,5–3,9 MB); transcript dạng mảng `{start, end, text}` theo câu để highlight; ảnh bìa bài học tái dùng ảnh render 3D giảng đường (không tải ảnh ngoài).

**Tiến độ:** lưu trong localStorage cùng khóa `chuaOnlineV2`, bổ sung `lessonsDone: []`, `reflections: {lessonId: text}`, `quizBest: {lessonId: score}`; đồng bộ huy hiệu sang profile nhân vật (mục 4.5).

**Điều kiện nghiệm thu nội dung:** mỗi bài phát hành phải có (a) nguồn ghi dưới bài, (b) người kiểm duyệt chuyên môn ký duyệt trong file dữ liệu (`reviewedBy`), (c) quiz có giải thích — thiếu một trong ba thì không publish.

---

## 3. NIỆM KINH (Sutra chanting)

### 3.1 Cấu trúc thời khóa tụng niệm — ✅ đã kiểm chứng

Truyền thống chùa Bắc tông Việt Nam theo *Thiền môn nhật tụng* / *Hai thời công phu* (bản dịch giải của Trí Quang Thượng nhân), được phân tích tại phatgiao.org.vn — https://phatgiao.org.vn/yeu-to-mat-giao-trong-hai-thoi-cong-phu-d55947.html:

**Thời khóa buổi sáng (công phu khuya):**

1. Thần chú Lăng Nghiêm
2. Thần chú Đại Bi Tâm (Chú Đại Bi)
3. Tâm Kinh Bát Nhã

**Thời khóa buổi chiều (công phu chiều/tối):**

1. Thần chú Đại Bi Tâm + Tâm Kinh Bát Nhã
2. Kinh A Di Đà
3. Thần chú Vãng Sanh Tịnh Độ
4. Sám Hồng Danh, gồm các bước: tán dương chư Phật → quy y Tam bảo (cả tánh và tướng) → phát Bồ đề tâm → đảnh lễ Tam bảo → lạy Phật → sám hối → phát lộ → hướng nguyện theo hạnh Phổ Hiền → hồi hướng
5. Văn thí thực (Mông Sơn thí thực)
6. Niệm Phật
7. Tán Phật
8. Nguyện sanh Cực Lạc
9. Tán lễ Bổn Tôn
10. Cảnh sách
11. Tự quy y Tam bảo (Tam tự quy y)

Nhận xét của nguồn: ngoài các phần tán/niệm/lạy/sám/nguyện/hồi hướng/Tam tự quy, phần lớn hai thời công phu là thần chú — tức thời khóa đầy đủ của chư Tăng **dài và nặng**, không thể bê nguyên vào trải nghiệm cho cư sĩ tại nhà; cần rút gọn có cấu trúc (mục 3.2).

**Khung giờ tham chiếu:** một nghiên cứu về sinh hoạt tịnh xá (Nghiên cứu Tôn giáo, scholar.dlu.edu.vn) ghi nhận mẫu phổ biến: khóa khuya khoảng **4h00** (nhiều nơi 3h45), khóa chiều khoảng **18h30**. ⚠️ Đây là số liệu của tịnh xá Ngọc Phương (hệ Khất sĩ), **không phải của chùa Vĩnh Tràng** — chỉ dùng làm mốc thiết kế "giờ gợi ý", ghi nhãn rõ trong app.

**Thực hành tại gia phổ biến** (tham khảo trang hướng dẫn niệm kinh tại gia, sites.google.com/view/huongdanniemkinh — nguồn không chính thống, chỉ để tham khảo thói quen cư sĩ): bộ bài tập hằng ngày thường bắt đầu bằng Chú Đại Bi, kèm Tâm Kinh, Lễ Phật Đại Sám Hối Văn, Chú Vãng Sanh; biến số Đại Bi thường đặt mục tiêu 21/49 biến — cho thấy nhu cầu "đếm biến" là có thật ở người dùng mục tiêu.

### 3.2 Thiết kế phiên tụng cho cư sĩ tại nhà (🎨 đề xuất thiết kế)

Ba gói thời lượng **5 / 10 / 20 phút**, cắt từ đúng thứ tự thời khóa chiều (thời khóa phổ biến hơn với cư sĩ đi làm), mỗi gói giữ khung: **Khai kinh (chuông) → thân bài → niệm Phật → hồi hướng → kết (chuông)**.

| Phần | Gói 5 phút "Tâm Kinh" | Gói 10 phút "Chiều An" | Gói 20 phút "Thời Khóa Tối Thu Nhỏ" |
|---|---|---|---|
| Khai kinh | Chuông ×1, kệ khai kinh ngắn | Chuông ×1, hương tán + kệ khai kinh | Chuông ×3, hương tán + kệ khai kinh |
| Thân bài 1 | — | Chú Đại Bi ×1 biến | Chú Đại Bi ×1 biến |
| Thân bài 2 | Tâm Kinh ×1 | Tâm Kinh ×1 | Tâm Kinh ×1 |
| Thân bài 3 | — | — | Kinh A Di Đà (trích đoạn chính) |
| Thân bài 4 | — | — | Sám hối (trích Sám Hồng Danh: phần sám hối + phát lộ) |
| Niệm Phật | 1 phút theo nhịp mõ | 2 phút theo nhịp mõ, đếm số câu | 3 phút theo nhịp mõ, đếm số câu |
| Hồi hướng | Văn hồi hướng ngắn + Tam tự quy y | Văn hồi hướng + Tam tự quy y | Văn hồi hướng đầy đủ + Tam tự quy y |
| Ghi chú thời lượng | Tâm Kinh tụng chậm ≈ 3–4 phút | Đại Bi 1 biến ≈ 5–6 phút | Tổng các phần ≈ 19–21 phút |

Cùng một khung, thêm 2 biến thể theo ngày (🎨): **"Công phu khuya thu nhỏ"** (Lăng Nghiêm rút gọn thay bằng Đại Bi mở đầu theo thời sáng — vì chú Lăng Nghiêm rất dài, chỉ đưa bản trích) và **"Sám hối 14/29 âm lịch"** (nhấn phần Sám Hồng Danh đầy đủ hơn, theo thông lệ sám hối định kỳ bán nguyệt của cư sĩ — thông lệ này phổ biến trong chùa Bắc tông Việt Nam; khi đưa vào app ghi là "theo thông lệ", không khẳng định là lịch riêng của Vĩnh Tràng ⚠️).

### 3.3 Luồng tương tác trong phiên tụng (🎨 đề xuất thiết kế)

1. **Chuẩn bị:** chọn gói (5/10/20) → chọn chế độ **"Tụng theo"** (có chữ chạy) hoặc **"Chỉ nghe"** (màn hình tối giản, nhân vật 3D quỳ chắp tay đồng hành) → chuông khai kinh.
2. **Trong phiên:**
   - Chữ kinh hiển thị từng câu, **highlight karaoke theo câu** đang tụng (không cần chính xác từng chữ — nhịp tụng đều nên đồng bộ theo câu là đủ và ổn định hơn).
   - **Mõ tự động** gõ theo nhịp câu (tái dùng `playMokugyo()` đã nâng cấp ở mục 1.6); người dùng có thể tự gõ mõ bằng cách chạm — mỗi chạm là 1 tiếng mõ + rung nhẹ (haptic trên di động).
   - **Chuông tự động** tại các mốc chuyển phần (khai kinh ×1, trước hồi hướng ×1, kết thúc ×3) — đúng vai trò "tín hiệu chuyển đoạn" của chuông/khánh trong khóa lễ thật.
   - **Bộ đếm:** biến Đại Bi (mục tiêu tự đặt 1/3/7/21), số câu niệm Phật (vòng 108 hạt ảo chạy quanh viền màn hình — nối tiếp tính năng lần tràng hạt 21 hạt đã có ở V2).
   - Nhân vật 3D: quỳ + chắp tay suốt phiên; đến phần lạy trong sám hối thì nhân vật thực hiện animation **Vái/Lạy** theo nhịp (dùng action "Vái", "Quỳ" đã có — mục 4).
3. **Kết phiên:** chuông ×3 → hiện văn hồi hướng → nút "Hoàn thành thời khóa" → cộng dấu ấn vào hồ sơ + chuỗi ngày (nếu là phiên đầu tiên trong ngày), gợi ý 1 bài giảng liên quan (mục 2) hoặc thẻ an lạc.
4. **An toàn trải nghiệm:** nút tạm dừng luôn hiện; thoát giữa chừng vẫn lưu vị trí (tiếp tục sau); quá 22h app tự gợi ý giảm âm lượng và dùng gói ngắn.

### 3.4 Lịch hằng ngày trong app (🎨 đề xuất thiết kế)

| Mốc | Tính năng | Ghi nhãn bắt buộc |
|---|---|---|
| 4h00 | Nhắc "Công phu khuya" (opt-in, tắt mặc định) + gói khuya thu nhỏ | "Giờ gợi ý theo thông lệ chùa Bắc tông — không phải giờ công phu công bố của chùa Vĩnh Tràng" |
| 18h30 | Nhắc "Công phu chiều" (opt-in) + 3 gói 5/10/20 phút | Như trên |
| Rằm & mùng 1 âm lịch | Mở gói "Sám hối" mở rộng + trang trí hoa đăng trong cảnh | Theo lịch âm tích hợp sẵn |
| Phật Đản, Vu Lan | Phiên tụng đặc biệt + bài giảng chuyên đề ở mục 2 | Gắn với dữ kiện lễ lớn của chùa (✅ chùa có tổ chức Đại lễ Phật Đản — pagoda.amazingvietnam.vn) |

⚠️ **Không khẳng định** các mốc giờ trên là thời khóa thật của chùa Vĩnh Tràng (chưa kiểm chứng, mục 1.3). Nếu sau này Logan xin được thời khóa chính thức của chùa, chỉ cần thay bảng giờ và bỏ ghi nhãn "gợi ý".

### 3.5 Văn bản kinh — nguồn và bản quyền

- Văn bản Hán–Việt truyền thống của Chú Đại Bi, Tâm Kinh, Kinh A Di Đà, Sám Hồng Danh thuộc lớp văn bản cổ truyền lưu hành công khai trong các bản *Nhật tụng*/*Kinh tụng hằng ngày* của nhiều chùa; khi tích hợp phải **ghi xuất xứ bản dùng** (tên sách/bản in) dưới mỗi bài kinh trong app và đối chiếu chính tả với ít nhất 2 bản phổ biến khác nhau trước khi phát hành.
- Phần dịch nghĩa/giải thích (nếu có) là tác phẩm có tác giả (ví dụ bản dịch giải *Hai thời công phu* của Trí Quang Thượng nhân) — **không sao chép** nếu chưa có phép; chỉ dùng phần văn kinh gốc.

### 3.6 Đặc tả triển khai — Niệm kinh

**Dữ liệu bài kinh (JSON theo câu, dùng chung cho highlight + đếm biến):**

```json
{
  "id": "thoi-chieu-10",
  "title": "Thời chiều — gói 10 phút",
  "sections": [{
    "id": "dai-bi", "title": "Chú Đại Bi", "bellAtStart": 1,
    "audioUrl": "audio/chant/dai-bi-1bien.opus",
    "lines": [{ "t": 0.0, "text": "Nam mô hắc ra đát na đá ra dạ da…" }],
    "moPattern": "per-line"
  }]
}
```

**Đồng bộ:** vòng lặp `requestAnimationFrame` đọc `audio.currentTime`, tra câu hiện tại bằng tìm kiếm nhị phân trên mảng `lines[].t`; highlight bằng CSS class — không dùng `setInterval` rời rạc (tránh lệch nhịp khi tab chậm). Khi tab bị ẩn, audio vẫn chạy (WebAudio/`Audio` element), highlight tiếp tục đúng theo đồng hồ audio khi quay lại.

**Âm thanh phiên:** giọng tụng thu âm thật (mono Opus 40–48 kbps, xem ngân sách mục 1.6); mõ/chuông là lớp riêng tổng hợp bằng WebAudio (không trộn cứng vào file tụng) để người dùng tắt/bật mõ độc lập và để nhịp mõ khớp highlight.

**Trạng thái lưu:** bổ sung vào `chuaOnlineV2`: `chant: { lastSessionId, resumeAt, totalMinutes, dailyDone: {date: true} }`; hoàn thành phiên = điều kiện cộng chuỗi ngày thay cho chỉ "mở trang" như V2 hiện tại (chặt chẽ hơn, đúng tinh thần chống tích điểm hình thức ở mục 0.3).

**Nghiệm thu:** (a) highlight lệch audio ≤ 0,5 giây trên toàn phiên; (b) chuông/mõ không chồng lấn gây giật khi chuyển phần; (c) phiên 20 phút chạy trọn trên điện thoại tầm trung không nóng máy (giới hạn animation nền trong lúc tụng).

---

## 4. PROFILE NHÂN VẬT

### 4.1 Tài sản nhân vật hiện có (✅ đã kiểm chứng từ công việc trước trong dự án)

| Nhân vật | Tài sản 3D | Trạng thái |
|---|---|---|
| **Phật tử nữ** | Model Hunyuan3D có màu qua vertex-color (file chuẩn Logan cung cấp: `nu-phuc-hoi-mau-chuyen-dong.glb`, 1 mesh skinned 66.057 verts, armature 15 xương) | ✅ Đã đo đạc trên tư thế thật và fit vật phẩm: nón lá (vành = 0,252 × chiều cao nhân vật, vành ở 0,895 × chiều cao), túi đeo tại hông, quai chéo tới vai đối diện — script `scripts/fit_model_that.py` đã đẩy lên repo. **8 action có sẵn: Chắp tay, Đi bộ, Đứng, Quỳ, Thắp nhang, Vái, Lên cầu thang, Xuống cầu thang** |
| **Phật tử nam** | Có model tĩnh có màu trong repo (`Hunyuan3D/nam-chua-co-mau.glb`) và bản blocky `nam-di-chua.glb` (cao 1,76, vai 0,56 — số đo của bản blocky, không dùng cho bản thật) | ⚠️ File **animated** của nam nằm trong thư mục `Chuyển động/` của repo (4–26 MB) — chưa tải về workspace được; chưa đo đạc/fit trên model thật |
| **Trẻ em** | Có model tĩnh có màu (`tre-em-chua-co-mau.glb`) và bản blocky | ⚠️ Tương tự nam: chưa có file animated trong workspace, chưa đo đạc |
| **Chú tiểu dẫn đường** | Đã tồn tại dạng **bong bóng thoại hướng dẫn** trong overlay V2 (nói dữ kiện đã kiểm chứng từ ảnh thật) | Chưa có model 3D riêng được chốt; đang là lớp UI |
| **Giảng sư** | Chưa có | Nhân vật mới, phục vụ mục 2 |

**Bài học kỹ thuật đã trả giá (ghi vào hồ sơ để không lặp lại):** model nữ **không có material/UV — màu nằm ở vertex color tên `Color`**; pipeline nào không đọc vertex color sẽ render nhân vật trắng xóa. Mọi profile dưới đây phải kèm ghi chú này cho dev xử lý model.

### 4.2 Bộ trường (fields) của một profile (🎨 đề xuất thiết kế)

| Nhóm | Trường | Ghi chú |
|---|---|---|
| Định danh | `id`, `tenHienThi`, `loai` (khách chọn được / NPC dẫn đường / NPC giảng sư) | Tên của 3 nhân vật khách do **người dùng tự đặt** khi bắt đầu (mặc định gợi ý tên trung tính); tên NPC là hư cấu, ghi rõ là nhân vật của trải nghiệm |
| Thông tin | `nhomTuoi` (thanh niên / trung niên / trẻ em…), `mucDichDiChua` (chọn 1–3: cầu an gia đạo, học Phật pháp, tìm bình yên, lễ Phật rằm/mùng 1, đi cùng gia đình, vãng cảnh di tích) | `mucDichDiChua` dùng để cá nhân hóa gợi ý: chọn "học Phật pháp" → chú tiểu gợi ý giảng đường trước; chọn "tìm bình yên" → gợi ý gói niệm kinh 10 phút |
| Ngoại hình | `modelUrl`, `trangPhucMacDinh` (mô tả + mã màu), `vatPhamMacDinh` (nón, túi…), `fitProfile` (bộ hằng số fit theo từng model — như bộ đã chốt cho nữ) | Mỗi model một `fitProfile` riêng; **cấm dùng chung hằng số giữa các model** (bài học từ audit: 3 script gắn nón cho ra 3 vị trí khác nhau vì hằng số gõ tay) |
| Hành động | `actions`: map tên action trong file ↔ hành động trong trải nghiệm | Xem bảng 4.3 |
| Tiến trình | `congDuc` (điểm dấu ấn), `chuoiNgay`, `changHanhTrinh` (5 chặng V2), `baiGiangDaHoc`, `phienKinhDaHoanThanh`, `huyHieu` | Dữ liệu nằm ở localStorage của người dùng, profile chỉ là "khung hiển thị + cấu hình" — xem 4.5 |
| Âm thanh | `giongNoi` (NPC: tập câu thoại cố định; khách: không có) | NPC không dùng giọng AI ứng khẩu cho nội dung giáo lý (mục 2.3) |

### 4.3 Bảng map action ↔ tính năng

| Action trong file 3D | Dùng ở | Trạng thái kiểm chứng |
|---|---|---|
| Đứng | Trạng thái chờ ở mọi zone | ✅ Có ở model nữ |
| Đi bộ | Di chuyển giữa các zone | ✅ Có ở model nữ |
| Lên cầu thang / Xuống cầu thang | Lên chánh điện, lên tháp | ✅ Có ở model nữ |
| Chắp tay | Chào chú tiểu/NPC khác, đứng trước bàn thờ, trong phiên niệm kinh | ✅ Có ở model nữ |
| Thắp nhang | Chặng dâng hương của hành trình V2 | ✅ Có ở model nữ |
| Quỳ | Niệm kinh (mục 3), lễ Phật | ✅ Có ở model nữ |
| Vái | Lễ bái trong chánh điện, phần lạy của sám hối (mục 3.3) | ✅ Có ở model nữ (action "Vái" là vái đứng; lạy quỳ sâu chưa có action riêng — ⚠️ nếu muốn lạy ngũ thể đầu địa phải làm thêm animation) |
| (Chưa có) Lần tràng hạt ngồi | Phiên niệm Phật dài | 🎨 Đề xuất bổ sung sau; tạm dùng Quỳ + Chắp tay |

⚠️ Bộ action của nam và trẻ em **chưa kiểm chứng** (chưa có file animated trong workspace). Khi Logan cung cấp file (như đã làm với model nữ), việc đầu tiên là liệt kê action + đo đạc lại toàn bộ, không suy từ model nữ.

### 4.4 Profile cụ thể cho 5 nhân vật (🎨 đề xuất thiết kế — phần tiểu sử NPC là hư cấu phục vụ trải nghiệm)

**A. Ba nhân vật khách (người dùng chọn 1 làm nhân vật đại diện):**

| | Phật tử nữ | Phật tử nam | Trẻ em |
|---|---|---|---|
| Vai trò | Nhân vật đại diện mặc định (đã sẵn sàng kỹ thuật) | Nhân vật đại diện | Nhân vật đại diện cho người dùng nhỏ tuổi / gia đình đi cùng con |
| Trang phục mặc định | Áo tràng xám–xanh lam (đúng màu vertex-color của model thật), tóc búi | Áo tràng xám/nâu (⚠️ chốt màu theo model thật khi có file) | Áo lam Phật tử trẻ em, kích thước nhỏ (⚠️ chốt theo model thật) |
| Vật phẩm mặc định | Nón lá vẽ sen + túi vải thêu sen (đã fit xong) | Nón lá + túi vải (chờ fit) | Nón lá nhỏ (chờ fit) |
| Đối tượng người dùng | Mặc định chung | Người dùng nam | Trẻ em đi cùng gia đình; nội dung gợi ý rút gọn, không quiz khó |
| Ghi chú | Là nhân vật duy nhất đã đạt chuẩn "đối chiếu model thật" | Cần file animated để hoàn thiện | Cần file animated để hoàn thiện |

**B. Chú tiểu dẫn đường (NPC, không chọn được):**

- **Tên hiển thị (hư cấu):** "Chú tiểu An" — chữ "An" nối với thẻ an lạc theo ngày của V2.
- **Vai trò:** người dẫn đường duy nhất trong cảnh: chào ở cổng, giới thiệu từng zone bằng **dữ kiện đã kiểm chứng** (đúng nguyên tắc overlay V2 đang làm), nhắc giờ gợi ý công phu, dẫn vào giảng đường và phòng niệm kinh.
- **Tính cách biên tập:** nói ngắn, ấm, không giảng đạo dài dòng; câu hỏi về giáo lý thì hướng người dùng vào bài giảng ở giảng đường thay vì tự trả lời.
- **Hiện diện:** bong bóng thoại (hiện tại) → 🎨 nâng cấp: model 3D nhỏ đứng tại các điểm dừng của hành trình khi có tài sản model phù hợp; không tự chế model chú tiểu thô (luật đối chiếu thật của dự án).

**C. Giảng sư (NPC, chỉ xuất hiện ở giảng đường):**

- **Tên hiển thị:** ghi chức danh trung tính "Thầy giảng sư" (không đặt pháp danh cụ thể — tránh vô tình trùng/ám chỉ một vị thầy thật; mọi bài giảng đều ghi nguồn và người kiểm duyệt riêng ở mục 2.4).
- **Vai trò:** "chủ nhiệm lớp" của Học viện online: mở đầu buổi học bằng 1 tiếng chuông thỉnh giảng, giới thiệu bài, đặt câu hỏi suy ngẫm cuối bài.
- **Ranh giới:** giảng sư là nhân vật giao diện; nội dung giảng là nội dung có nguồn/kiểm duyệt (mục 2.3), nhân vật không "tự thuyết pháp".

### 4.5 Cách profile xuất hiện trong UI (🎨 đề xuất thiết kế)

1. **Màn hình mở đầu "Chọn người đi chùa":** 3 thẻ nhân vật (render từ chính model 3D, không dùng ảnh minh họa ngoài) — chọn xong mới vào cổng; cho đổi lại bất cứ lúc nào trong Hồ sơ.
2. **HUD thường trực:** avatar tròn (ảnh chụp từ model), tên người dùng đặt, chuỗi ngày 🔥, điểm dấu ấn — kế thừa thanh trạng thái của overlay V2, bổ sung avatar + tên.
3. **Trang Hồ sơ (mở từ HUD):** ảnh nhân vật toàn thân với trang phục/vật phẩm đang mang; danh sách huy hiệu (hành trình 5 chặng, lộ trình bài giảng, số phiên kinh); nút đổi nhân vật / đổi vật phẩm đã mở khóa; trường `mucDichDiChua` sửa được — sửa xong gợi ý của chú tiểu thay đổi theo.
4. **Trong cảnh 3D:** nhân vật đại diện là người thực hiện mọi animation (lên cầu thang vào chánh điện, quỳ niệm kinh, thắp nhang…); chú tiểu xuất hiện dạng bong bóng thoại tại điểm dừng; giảng sư chỉ ở giảng đường.
5. **Nguyên tắc riêng tư:** toàn bộ profile + tiến trình ở **localStorage trên máy người dùng** (như V2), không tài khoản, không gửi máy chủ ở giai đoạn này; trang Hồ sơ có nút "Xóa dữ liệu của tôi".

### 4.6 Tiến trình gắn với profile (🎨 đề xuất thiết kế — mở rộng V2, tuân thủ mục 0.3)

- **Điểm "công đức" → đổi tên hiển thị thành "Dấu ấn hành trình"** trong UI (giữ nguyên cơ chế điểm của V2: lạy +5, lần hạt +20, thắp đèn +10…), kèm chú thích cố định: *"Dấu ấn ghi nhận hoạt động của bạn trong trải nghiệm này."* — tránh ngôn ngữ hứa hẹn phước báo.
- **Chuỗi ngày:** từ V3, một ngày được tính khi hoàn thành **ít nhất 1 hoạt động trọn vẹn** (1 phiên kinh, 1 bài giảng, hoặc đủ 5 chặng hành trình) thay vì chỉ mở trang — chặt chẽ và ý nghĩa hơn.
- **Huy hiệu:** theo chặng (5), theo lộ trình giảng (4), theo niệm kinh (tổng 10/50/100 phiên; chuỗi 7/30 ngày). Huy hiệu chỉ hiển thị trong hồ sơ cá nhân, **không** bảng xếp hạng công khai.

### 4.7 Đặc tả triển khai — Profile nhân vật

**Schema (JSON cấu hình tĩnh cho nhân vật + localStorage cho tiến trình):**

```json
{
  "characters": [{
    "id": "nu", "loai": "khach",
    "tenMacDinh": "Phật tử nữ",
    "modelUrl": "models/nu-phuc-hoi-mau-chuyen-dong.glb",
    "vertexColorLayer": "Color",
    "trangPhucMacDinh": { "ten": "Áo tràng xám xanh", "nguon": "vertex-color của model" },
    "vatPhamMacDinh": ["non-la-sen", "tui-vai-sen"],
    "fitProfile": "fit/nu.json",
    "actions": ["Đứng","Đi bộ","Chắp tay","Quỳ","Thắp nhang","Vái","Lên cầu thang","Xuống cầu thang"]
  }]
}
```

**Mở rộng khóa lưu trữ `chuaOnlineV2` (giữ tương thích ngược, không mất dữ liệu cũ):**

```json
{ "points": 0, "streak": 0, "characterId": "nu", "displayName": "",
  "purposes": [], "outfit": {}, "lessonsDone": [], "chant": {},
  "audio": { "master": true, "ambience": 0.35, "ritual": true } }
```

**Checklist nghiệm thu cho mỗi nhân vật mới (nam/trẻ em) trước khi đưa vào chọn nhân vật:**

1. Có file animated gốc (không suy từ bản blocky/tĩnh).
2. Liệt kê đủ action trong file; map vào bảng 4.3; thiếu action nào thì khóa tính năng tương ứng cho nhân vật đó.
3. Đo đạc trên tư thế đã pose (không đo ở T-pose) và fit nón/túi bằng script riêng — theo đúng quy trình đã làm cho nữ (`fit_model_that.py`), render kiểm chứng đặt cạnh ảnh render mẫu của Logan.
4. Kiểm tra material vertex-color (lớp `Color`) — render thử 1 frame xác nhận không trắng xóa.

---

## 5. Danh mục nguồn đã dùng

**Về Chùa Vĩnh Tràng và Trường TCPH Tiền Giang:**

- phatgiaodongthap.org — Trường TCPH Tiền Giang tiếp đoàn Thanh tra Ban Giáo dục Phật giáo TW (lịch sử trường: thành lập 1990 tại chùa Vĩnh Tràng, dời về chùa Phật Ân 1998): https://phatgiaodongthap.org/tien-giang-truong-trung-cap-phat-hoc-tiep-doan-thanh-tra-ban-giao-duc-phat-giao-trung-uong-den-tham-va-lam-viec-d2878.html
- phatgiao.org.vn — Thông báo chiêu sinh Cao đẳng Phật học Khóa III (2019–2021): https://phatgiao.org.vn/tien-giang-thong-bao-chieu-sinh-cao-dang-phat-hoc-khoa-iii-2019-2021-d34655.html
- phatsuonline.vn — Trang thẻ Trường TCPH Tiền Giang (lễ tốt nghiệp tại Giảng đường Huệ Đăng 2024; trụ sở Lớp Cao đẳng tại chùa Vĩnh Tràng): https://www.phatsuonline.vn/tags/truong-trung-cap-phat-hoc-tien-giang
- phatsuonline.vn — Lễ ký kết hợp tác giáo dục với Đại học Hoa Phạm tại trụ sở Lớp CĐ, chùa Vĩnh Tràng: https://phatsuonline.vn/tien-giang-le-ky-ket-ghi-nho-hop-tac-giao-duc-giua-truong-trung-cap-phat-hoc-tien-giang-va-dai-hoc-hoa-pham-dai-loan-11
- pagoda.amazingvietnam.vn — Hồ sơ Chùa Vĩnh Tràng (lịch sử, hệ phái, di tích quốc gia): http://pagoda.amazingvietnam.vn/2021/09/chua-vinh-trang.html
- Nghiên cứu Tôn giáo số 2–2018 (timtailieu.vn) — khảo sát chùa Bắc truyền Tiền Giang: https://timtailieu.vn/tai-lieu/su-dung-hop-giua-phat-giao-bac-truyen-voi-tin-nguong-truyen-thong-o-tien-giang-qua-khao-sat-mot-so-ngoi-chua-70458/
- Giờ mở cửa (nguồn du lịch, không thống nhất — chỉ để chứng minh "chưa kiểm chứng"): dulichbinhminh.com, nucuoimekong.com, tourdulichbentre.com, saigonstartravel.com, vietsensetravel.com, trip.com

**Về chương trình Phật học và thời khóa:**

- phatgiao.org.vn — Giáo dục và đào tạo Tăng Ni sinh hệ Trung cấp Phật học: https://phatgiao.org.vn/giao-duc-va-dao-tao-tang-ni-sinh-he-trung-cap-phat-hoc-thach-thuc-va-giai-phap-d43917.html
- Quỹ Đạo Phật Ngày Nay — Bộ giáo trình 35 cuốn cho 33 trường TCPH: https://quydaophatngaynay.org/thu-ngo-tro-duyen-an-tong-sach-giao-khoa-cho-33-truong-trung-cap-phat-hoc-gd6-c84-6/
- phatsuonline.vn — Môn thi học kỳ của một cơ sở TCPH: https://phatsuonline.vn/vinh-long-co-so-iii-truong-trung-cap-phat-hoc-tinh-to-chuc-thi-hoc-ky-ii-nam-thu-i-khoa-v-2025-2026-53
- phatgiao.org.vn — "Yếu tố Mật giáo trong hai thời công phu" (cấu trúc hai thời theo *Thiền môn nhật tụng*): https://phatgiao.org.vn/yeu-to-mat-giao-trong-hai-thoi-cong-phu-d55947.html
- Nghiên cứu Tôn giáo (scholar.dlu.edu.vn) — giờ khóa lễ tham chiếu tại tịnh xá: https://scholar.dlu.edu.vn/thuvienso/bitstream/DLU123456789/218492/1/48693-37-152432-1-10-20200626.pdf

**Về thị trường và âm thanh:**

- kenh14.vn — GHPGVN nói về trào lưu "đi chùa online": https://kenh14.vn/giao-hoi-phat-giao-viet-nam-noi-gi-ve-trao-luu-di-chua-online-215261103142543026.chn
- blogtamsu.vn (dẫn VnExpress) — Trào lưu đi chùa online, Sansa: https://blogtamsu.vn/p/di-chua-online-140985
- fpt.vn — Game Niệm Phật Online: https://fpt.vn/tin-tuc/game-di-chua-online-15777.html
- plumvillage.org — Mindfulness Apps / Plum Village App (bell of mindfulness, chanting, nature sounds): https://plumvillage.org/mindfulness/mindful-apps
- Freesound.org — cơ chế giấy phép CC0/CC-BY/CC-BY-NC và các bản ghi mẫu: https://freesound.org/people/3bagbrew/sounds/345028/ ; https://freesound.org/people/timothyd4y/sounds/473789/ ; https://freesound.org/browse/tags/?f=tag%3A%22buddhism%22+tag%3A%22temple%22

---

## 6. Việc chưa kiểm chứng & câu hỏi mở cần Logan xử lý

1. **Thời khóa công phu chính thức của Chùa Vĩnh Tràng** — ⚠️ chưa tìm thấy công bố. Nếu muốn app ghi "giờ công phu của chùa", cần hỏi trực tiếp văn phòng chùa. Hiện tại app chỉ được ghi "giờ gợi ý theo thông lệ".
2. **Giờ mở cửa chính thức** — các nguồn du lịch lệch nhau tới vài giờ (mở 5h30–7h30, đóng 18h00–23h00). Cần 1 nguồn chính thức nếu muốn hiển thị.
3. **Ghi âm thực địa tại chùa** (âm cảnh + 1 buổi công phu) — cần Logan xin phép chùa; đây là nâng cấp giá trị nhất cho mục Âm thanh.
4. **Bài giảng có phép phổ biến** — cần Logan quyết định kênh: xin phép quý thầy giảng tại Huệ Đăng, hay nhúng nguồn chính chủ, hay tự biên soạn + thu âm tình nguyện viên.
5. **File animated của nhân vật nam và trẻ em** — cần Logan cung cấp (như đã cung cấp file nữ) để đo đạc, liệt kê action và fit vật phẩm; hiện cả hai chưa đạt chuẩn kiểm chứng.
6. **Cách ghi địa danh hành chính** (Tiền Giang / Đồng Tháp sau sáp nhập 2025) trên các màn hình giới thiệu chùa.
7. **Người kiểm duyệt chuyên môn** cho nội dung bài giảng và phần giải thích kinh — điều kiện publish bắt buộc ở mục 2.4, cần Logan chỉ định nguồn nhân sự (ví dụ liên hệ qua Trường TCPH / Ban Trị sự tỉnh nếu có quan hệ).

*Hết hồ sơ.*
