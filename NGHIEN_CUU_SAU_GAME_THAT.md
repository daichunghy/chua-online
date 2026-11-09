# NGHIÊN CỨU SÂU — CHÙA ONLINE (VĨNH TRÀNG) THEO CHUẨN "GAME THẬT"

**Ngày lập:** 06/11/2026. **Lệnh:** Chung Hy — bản hiện tại mới ~20% so với "game
thật", nghiên cứu sâu game thật + trải nghiệm đi chùa thật để nâng cấp, kèm cải
thiện model 3D về màu sắc.
**Nguồn nền:** `CAM_GIAC_DI_CHUA.md` (audit cảm giác đi chùa, cùng thư mục),
`THAM_KHAO_TRANG_KHAC.md` (đối thủ), `TRANG_PHUC_MAC_DINH_3_NHAN_VAT.md`,
`danh_muc_vat_pham.json` (21 món), kiểm chứng web 06/11/2026 (Sky wiki/review,
chuaminhduc.com.vn, tuvixemtuong.net, các bài kiến trúc Vĩnh Tràng:
tapchinghiencuuphathoc.vn, phatgiao.org.vn, langnghesondong.com.vn).
**Quy ước:** mục nào chưa kiểm chứng được ghi rõ — không bịa dữ kiện về chùa thật.

---

## 0. Tóm tắt + bảng chấm theo trục

Bản hiện tại mạnh ở *nội dung tu học* (niệm kinh 3 gói + giảng đường 4 lộ trình —
thứ cả 3 đối thủ đều yếu) và *model nhân vật đã fit*, nhưng yếu ở đúng phần làm
nên một "game": **không gian đi được, chuỗi hành vi lễ hoàn chỉnh, vòng lặp mùa/lịch**.
Đó là lý do cảm nhận tổng chỉ ~20%.

| Trục | % hiện tại | Một câu lý do |
|---|---|---|
| 1. Hành động nghi lễ | **25%** | Có bộ action (Thắp nhang/Vái/Quỳ) + niệm kinh, nhưng chuỗi thắp nhang trong cảnh = 1 toast; chưa chuông tương tác, chưa xăm, chưa dâng hoa quả |
| 2. Tham quan | **20%** | Bố cục khuôn viên 3D đang dựng ở tuyến layout, nhưng trải nghiệm web vẫn 1 phòng + nhảy góc máy; chưa đi được, chưa tuyến trạm sống |
| 3. Trang phục nhân vật | **35%** | 3 nhân vật mặc định + 5 vật phẩm đeo đã fit kiểm chứng đạt; nhưng trong trải nghiệm không chọn/đổi được áo, không pháp danh |
| 4. Vật phẩm & "mua sắm" | **20%** | Catalog 21 món thật có sẵn; shop hiện đặt sai chỗ + gắn giá vào UI lễ (audit K5); chưa có cơ chế thỉnh/dâng đúng nghĩa chùa |
| 5. Vòng lặp quay lại | **25%** | Có chuỗi ngày + thẻ an lạc theo ngày; chưa thời khóa giờ cố định, chưa lịch rằm/lễ, chưa ảnh Dấu ấn |
| 6. Model 3D & màu sắc | **30%** | Công trình/tượng đã qua kiểm chứng từng mục; grade còn sáng gắt (chưa áp D1/D2 của audit), palette chưa chuẩn hoá theo màu thật |
| **Tổng hợp** | **≈ 25%** | Khớp đánh giá ~20% của Chung Hy — phần người dùng *nhìn thấy* còn thấp hơn vì khuôn viên chưa vào trải nghiệm |

---

## RANH GIỚI BẮT BUỘC — phân loại mọi đề xuất trong báo cáo này

Giữ nguyên cảnh báo GHPGVN (02/11/2026, đã ghi trong dossier): tránh "tích điểm,
tranh thứ hạng, trả tiền đổi phước". Mọi ý tưởng dưới đây thuộc 1 trong 2 nhóm:

**NÊN LÀM** — tăng cảm giác đi lễ thật: chuỗi hành vi nghi lễ đầy đủ (châm–cắm
nhang, lạy đúng cách, thỉnh chuông, xin xăm để suy ngẫm), tuyến hành hương có
đường cong lắng dần, tương tác theo lịch lễ thật, sưu tầm mang tính *tưởng niệm*
(Dấu ấn hành trình, bộ thẻ trạm, vật phẩm đã thỉnh — chỉ ghi nhận bằng câu chữ,
không số đo), tiến trình *học* (được hướng dẫn thêm nghi thức, mở thêm bài giảng).

**KHÔNG NÊN LÀM** (có ở đối thủ, đã cân nhắc và loại):
- Điểm công đức hiển thị, EXP cho hành động lễ, cấp bậc trên đầu nhân vật/tượng,
  bảng xếp hạng, hệ số thưởng theo "thiền phái" (toàn bộ là của Niệm Phật Online).
- Vòng quay lộc/phần thưởng ngẫu nhiên gắn với lễ bái.
- Tiền ảo nạp tiền thật; bán đèn nguyện/vật phẩm tâm linh theo gói giá *ngay
  trong giao diện lễ* (v3 đang có — phải gỡ, xem trục 4).
- Streak có hình phạt mất chuỗi, vật phẩm "giữ chuỗi" bán tiền.
- Vật phẩm giả tưởng kiểu game (vũ khí, linh thú) — vật phẩm của Vĩnh Tràng là
  21 món thật trong catalog repo.
- Xin xăm đóng khung "phán tài lộc chắc chắn" (phải là lời nhắc suy ngẫm).
- "Phóng sinh" dạng tương tác game — nhạy cảm sinh thái, dễ thành thả sai loài;
  nếu nhắc chỉ ở dạng nội dung giáo dục trong bài giảng.
- Số người online giả, mạo nhận giờ công phu của chùa thật (chưa có nguồn công bố).

---

## TRỤC 1 — HÀNH ĐỘNG NGHI LỄ

### Tham khảo làm gì (cụ thể)
- **Sky: Children of the Light:** động từ cốt lõi của game là *thắp sáng cho
  nhau* — đốt nến/tượng để nhận "sáp" rồi nến; biểu cảm (emote) là ngôn ngữ
  chính: cúi chào (bow) có cấp độ, ngồi thiền cùng nhau trên ghế đá, nắm tay dẫn
  đường. Bài học: **một hành vi lễ nhỏ, làm chậm, có âm thanh và có người chứng
  kiến** đáng giá hơn 10 nút bấm.
- **Chùa Sen:** chuỗi cứng theo đúng lệ: qua tam quan → thắp hương ở lư hương →
  thỉnh chuông ở gác chuông (**người cùng phòng nghe được tiếng chuông của
  bạn**) → vào chánh điện lạy Phật → **ngồi xuống bồ đoàn thì bảng công phu mới
  mở** → khép buổi bằng Kệ Hồi Hướng.
- **Chùa Minh Đức online (VN, celefmedia):** mỗi hành động là nhân vật *tự đi
  tới nơi rồi làm*: Lễ Phật = quay về tượng gần nhất cúi lạy; Thắp hương = đi
  tới lư hương, **mỗi nén cháy 90 giây**; Rung chuông = đi tới tháp chuông, đánh
  1 hồi, nhận 1 lời chúc; Dâng hoa = **đi nhặt đủ 10 bông hoa quanh chùa** rồi
  mang dâng trước chánh điện; Thả hoa đăng = ra lan can thả xuống sông, **mọi
  người cùng sân đều thấy**; Lời nguyện hiện trên đầu nhân vật 30 giây.
- **Tuvixemtuong:** trong chánh điện: chọn **1 hoặc 3 nén**, chọn **vái hoặc lạy
  × 1/3/9 lượt**, hình quỳ cúi theo từng lượt; gõ mõ/thỉnh chuông bấm lúc nào
  cũng được; hoa đăng mang theo lời khấn bay lên.
- **Nghi lễ thật (có nguồn báo Giác Ngộ/phatgiao.org.vn + hướng dẫn xin xăm):**
  - *Thắp nhang:* 3 nén = Tam bảo (Phật–Pháp–Tăng) / giới–định–huệ hương; châm
    từ lửa sẵn (đèn dầu), cầm hai tay ngang trán khấn, vái, rồi cắm.
  - *Vái vs lạy:* vái = đứng chắp tay cúi người; lạy = quỳ, **ngũ thể đầu địa**
    (gối phải → gối trái → hai khuỷu tay chạm đất → hai bàn tay ngửa duỗi quá
    trán → đỉnh đầu chạm xuống, giữ một lúc). **3 lạy = kính Phật, Pháp, Tăng.**
  - *Xin xăm Quan Âm (bộ 100 quẻ):* tĩnh tâm, thắp nhang khấn rõ điều muốn hỏi
    → xóc ống xăm đến khi **đúng 1 thẻ rơi** → **gieo âm dương** (2 đồng/khối)
    để xác nhận, tối đa 3 lần gieo → nhận thẻ, nghe giải quẻ.
  - *Thỉnh chuông:* 3 tiếng, chậm, để tiếng chuông tắt hẳn mới thỉnh tiếp.
  - *Nghi thức ngưỡng cửa:* bỏ dép trước chánh điện, nhận nhang/hoa ở sạp cổng.
  - *Công quả:* quét sân, phụ chuẩn bị hoa — phần "làm" của một buổi đi chùa.

### Mình có gì
- Bộ action GLB đã fit sẵn: **Thắp nhang / Vái / Quỳ / Chắp tay / Đi bộ** (3 nhân
  vật) — đủ nguyên liệu cho hầu hết chuỗi trên, chưa được dùng trong cảnh.
- Niệm kinh 3 gói (karaoke + mõ/chuông WebAudio) + hồi hướng cuối buổi; bát
  hương bàn thờ chánh điện (tĩnh) + khói trang trí sai chuẩn (audit A2).
- Chuỗi thắp nhang đầy đủ **đã đặc tả xong ở audit mục C2** (5 nhịp: đến gần →
  rút nhang bén lửa → vái giữ nhang → cắm → khói lên dần + chuông nhỏ).

### Thiếu gì
1. **Chuỗi thắp nhang chưa cài** (audit C2) — đây là nhịp cảm xúc số 1 của buổi lễ.
2. **Lạy đúng cách:** chưa có hướng dẫn ngũ thể đầu địa; action Quỳ+Vái ghép
   nhịp chỉ là tạm — ghi nợ 1 action "Lạy" đầy đủ; mặc định **3 lạy**, cho chọn
   1/3/9 như lệ thật.
3. **Thỉnh chuông chưa là tương tác trong cảnh:** cần trạm gác chuông — avatar
   đi tới, thỉnh 3 tiếng, chuông synth decay 8–12 giây (dossier âm thanh), khép
   bằng 1 dòng chúc tĩnh. (Bản nhiều người "nghe chuông của nhau" = để dành
   multiplayer, trục 5.)
4. **Xin xăm chưa có.** Đặc tả nên làm: gian Quan Âm → khấn (ô nhập điều muốn
   hỏi, *chỉ lưu máy người dùng*) → animation xóc ống → 1 thẻ rơi → gieo âm
   dương (1 sấp 1 ngửa = thánh quẻ, tối đa 3 lần) → thẻ hiện số + thơ quẻ +
   **lời giải viết theo hướng suy ngẫm, cấm phán định mệnh/tài lộc chắc chắn**
   (mẫu văn phong: Chùa Minh Đức ghi "lời nhắc để suy ngẫm, không phải lời tiên
   đoán") → lưu vào Dấu ấn của ngày; **1 lần/ngày** (đúng lệ + chống cày).
   ⚠️ Chưa kiểm chứng được Vĩnh Tràng thật có gian xin xăm hay không — trình bày
   là tính năng văn hoá chung, không khẳng định là nghi thức tại chùa.
5. **Dâng hoa quả chưa có:** học pattern Chùa Minh Đức — nhặt hoa sen quanh
   hồ/sân (hoặc nhận mâm ngũ quả ở trạm cổng, audit G2) → avatar cầm mang đi →
   dâng trước chánh điện. Vật phẩm đã có sẵn model: `hoa_sen_tuoi`,
   `mam_ngu_qua`.
6. **Nhịp ngưỡng cửa:** nhận 3 que nhang + hoa ở cổng (S0), bỏ dép ở cửa chánh
   điện (audit G2) — rẻ, đúng lễ, người đi chùa thật nhận ra ngay.

---

## TRỤC 2 — THAM QUAN

### Tham khảo làm gì
- **Sky:** 7 cõi đi bộ/bay liền mạch, mỗi cõi có "điểm dừng có nội dung" (tượng
  linh hồn kể 1 mẩu chuyện bằng hành động), cổng chuyển cảnh không cắt cứng;
  Aviary Village có chu trình sáng/tối theo giờ. Bài học: tham quan = *đi qua
  một tuyến có nhịp*, không phải mở menu bản đồ.
- **Chùa Sen / Niệm Phật:** đi bộ tự do bằng avatar, nút hành động hiện theo ngữ
  cảnh trong bán kính gần (chuẩn đã chép ở audit B1).
- **Sansa:** bài học ngược — chỉ 1 không gian ngồi yên cũng đủ lan truyền *nếu*
  một nhu cầu được làm trọn; Vĩnh Tràng không nên sao chép sự tối giản này vì
  lợi thế của mình là khuôn viên thật 14.000 m².

### Mình có gì
- Tuyến trạm **S0–S7 đã đặc tả khớp tuyến đi lễ thật** (audit B2): cổng Phương
  Tiện/Tịnh Độ → hoa viên A Di Đà → lư hương sân (thắp nhang) → chánh điện →
  Di Lặc → Phật Niết Bàn (đứng lặng 10 giây, không nút bấm) → bảo tháp (hồi
  hướng + Dấu ấn) → về cổng; giảng đường là trạm nhánh.
- Bố cục khuôn viên 3D (tuyến layout): công trình + 3 tượng lớn + tháp đã dựng
  và kiểm chứng từng mục; đường cong cảm xúc ồn → tĩnh đã đặc tả (audit G6).
- Dossier âm thanh 5 zone khớp đúng 5 đoạn của tuyến.

### Thiếu gì
1. **Khuôn viên chưa vào được trải nghiệm** — web v3 vẫn là 1 phòng 28×46 m +
   OrbitControls (audit A1/K1, lỗ hổng chết cảm giác số 1). Đây là P0 tuyệt đối.
2. **Điểm dừng chưa có nội dung sống:** mỗi trạm mới có "1 hành động + 1–2 dòng
   dữ kiện của An" trên giấy; cần thêm lớp khám phá nhẹ: bảng tên nơi chốn bằng
   bảng gỗ/đá trong cảnh (audit G7), điểm chụp hình gợi ý ở S1/S4 (gắn với Dấu
   ấn, trục 5), chi tiết sống quanh tuyến (bồ câu sân, lá bồ đề rơi, hồ cá —
   audit G5).
3. **Hồ chưa tồn tại trong cảnh web** dù chùa thật có ao cá và đèn hoa đăng cần
   mặt nước — hồ + cá + sen 3 trạng thái là 1 trạm tham quan độc lập nên có
   (giữa sân và khu tượng), đồng thời là nơi thả hoa đăng (trục 1/5).
4. **Chế độ ngày/chiều chưa có:** dossier đã đặc tả ngày/đêm; tối thiểu cần
   biến thể "hoàng hôn" của toàn tuyến (grade chiều ở trục 6) trước khi làm
   chu trình giờ đầy đủ.

---

## TRỤC 3 — TRANG PHỤC NHÂN VẬT

### Tham khảo làm gì
- **Chùa Sen:** ngay màn đầu: nhập **pháp danh**, chọn giới tính, **kiểu áo +
  màu áo** — nhân vật là "mình đi chùa", không phải avatar game chung chung.
- **Sky:** trang phục là lớp tiến trình *biểu cảm* duy nhất được bán/đổi bằng
  nến: áo choàng, mặt nạ, kiểu tóc, nhạc cụ — không một món nào cho sức mạnh.
  Bài học chuyển ngữ: ở chùa, "sưu tầm trang phục" = đổi sang bộ trang phục của
  *dịp lễ khác*, không phải khoe hiếm.
- **Trang phục đi chùa thật (VN):** **bộ lam/pháp phục** (lam, nâu, xám — màu
  của khiêm nhường); **áo tràng** (dài rộng, chỉ lam hoặc nâu sòng, mặc dịp lễ
  lớn/khoá tu); **áo bà ba Nam Bộ** (2 tà + quần ống suông đen, màu trắng/xanh/
  lam/vàng — rất hợp Vĩnh Tràng miền Tây, và khăn rằn đã có sẵn model);
  **áo dài** nhã nhặn (trắng, pastel, lam, nâu, vàng nhạt — nữ, dịp lễ). Quy tắc
  bất biến: kín đáo, qua gối, không màu loè loẹt/phản quang.

### Mình có gì
- 3 nhân vật (nữ/nam/trẻ em) đã fit trang phục mặc định **kiểm chứng đạt**:
  áo tràng một mảnh (nữ xám xanh, nam nâu, trẻ em lam xám–tím nhạt — đã sửa lỗi
  hai mảnh ngày 06/11), nón lá thêu sen, túi vải đeo chéo.
- 5 vật phẩm đeo/cầm từ model repo có texture đã fit đạt cả 3 nhân vật:
  nón lá thêu sen, túi vải thêu sen, **tràng hạt bồ đề 108 hạt**, búp sen cầm
  tay, khăn rằn Nam Bộ (`TRANG_PHUC_MAC_DINH_3_NHAN_VAT.md` bản V2).
- Hồ sơ nhân vật V3: chọn 1 trong 3 nhân vật + mục đích đi chùa (lưu local).

### Thiếu gì
1. **Không đổi được trang phục trong trải nghiệm:** đề xuất "tủ áo đi chùa" mở
   tại trạm cổng/nhà tổ, gồm đúng các bộ có thật: bộ lam (lam/nâu/xám), áo
   tràng lam + nâu sòng, áo bà ba (trắng/xanh) + khăn rằn cho nữ, áo dài trắng/
   pastel cho nữ dịp lễ, bộ chú tiểu cho trẻ em. Đổi áo = đổi vertex-color/
   material trên cùng model đã fit (kỹ thuật đã có), không cần model mới ngoài
   áo bà ba + áo dài (ghi nợ model, ưu tiên sau).
2. **Chưa có pháp danh:** thêm ô nhập pháp danh/tên gọi ở onboarding, hiện trên
   ảnh Dấu ấn (trục 5) — không hiện thành nametag bay trên đầu trong cảnh
   (audit G7 cấm nhãn kiểu game trong không gian 3D).
3. **Trang phục theo mùa lễ:** Vu Lan thêm **bông hồng cài áo** (đỏ/trắng — vật
   phẩm nhỏ, ý nghĩa lớn, gắn sự kiện trục 5); Phật đản thêm khăn/áo trắng.
   Đây là cách "cosmetic theo mùa" của Sky dịch sang ngữ cảnh chùa mà vẫn tôn
   nghiêm.

---

## TRỤC 4 — VẬT PHẨM & "MUA SẮM" THEO NGHĨA CHÙA

### Tham khảo làm gì
- **Đi chùa thật:** "mua sắm" ở chùa gồm 3 việc khác hẳn nhau: (1) mua/nhận
  **lễ vật để dâng** ở sạp gần cổng (nhang, hoa, quả) — mua xong là *cho đi*;
  (2) bỏ **thùng công đức** tùy tâm ở cửa chánh điện — không giá, không nhận lại
  gì ngoài sự nhẹ lòng; (3) ghé **phòng phát hành kinh sách/quầy lưu niệm gần
  lối ra** thỉnh sách, chuỗi hạt, vật phẩm mang về. Thứ tự và vị trí là một
  phần của nghi thức — thương mại ở chùa thật *lặng lẽ và ở rìa tuyến*.
- **Niệm Phật Online (mẫu KHÔNG chép):** 2 tiền ảo Sen/Ngọc, nạp Ngọc 20k–500k,
  vật phẩm hiếm giới hạn số lượng bán trong game — toàn bộ thuộc nhóm cấm theo
  cảnh báo GHPGVN và nguyên tắc dự án ("không bán phước").
- **Sky (mẫu chép được một nửa):** mọi thứ mua được đều là biểu cảm/trang trí,
  không lợi thế — nhưng tiền tệ của Sky vẫn là "cày + nạp"; Vĩnh Tràng chỉ chép
  nguyên tắc "không bán lợi thế", không chép tiền tệ.

### Mình có gì
- **Catalog 21 món thật** (`danh_muc_vat_pham.json`), nhiều món đã có model 3D:
  áo tràng, nón lá thêu sen, khăn rằn, tràng hạt 108, bộ mõ gỗ, bát nhang & 3
  nén hương trầm, búp sen tươi, nến hoa sen, đèn hoa đăng, mâm ngũ quả, 2 loại
  bồ đoàn, chiếu cói thiền, bánh bò thốt nốt, bánh da lợn, dừa xiêm, túi vải,
  quạt nan lá dừa, giỏ mây tre, chum sành hoa sen, đèn lồng lục giác.
- Shop trưng bày trong scene gốc (kế thừa) — nhưng audit K5/G2 đã kết luận:
  **đang bán vòng trầm 290.000đ + đèn nguyện theo gói 20k/50k/100k ngay trong
  UI lễ** — sai cả vị trí lẫn bản chất, phải gỡ khỏi mọi tương tác lễ.

### Thiếu gì — mô hình đề xuất (không tiền tệ, không điểm)
1. **Lễ vật = nhận, không mua.** Ở trạm cổng S0: "nhận 3 que nhang + bó hoa"
   (miễn phí, như phát tâm; audit G2). Lễ vật nằm trong tay avatar suốt tuyến
   và được *tiêu thụ* đúng nghi thức (cắm nhang S2, dâng hoa S3). Hết buổi là
   hết — không tồn kho, không kinh tế.
2. **Thùng công đức = vật trong cảnh, tương tác không số.** Đặt cạnh cửa chánh
   điện (3D); bấm vào: avatar cúi nhẹ, 1 dòng chữ tĩnh "Tuỳ tâm — chùa ghi
   nhận tấm lòng" — không nhập số tiền, không cộng gì, không lưu thành tích.
3. **Thỉnh vật phẩm = trạm cuối, mở theo hành trình.** Quầy lưu niệm dời về S7
   cạnh cổng (audit G2). 21 món chia 3 nhóm theo *cách nhận*:
   - *Mang theo khi lễ* (nhang, hoa, nến sen, đèn hoa đăng, mâm ngũ quả): nhận
     ở cổng/đúng trạm dùng.
   - *Dụng cụ tu tập* (tràng hạt, mõ, bồ đoàn, chiếu cói): "thỉnh" sau khi đã
     hoàn thành buổi thực hành tương ứng đầu tiên (đeo tràng hạt sau buổi niệm
    kinh đầu, bồ đoàn sau buổi thiền đầu) — ghi vào Dấu ấn như một dấu mốc học
     tập, không phải phần thưởng điểm.
   - *Lưu niệm miền Tây* (khăn rằn, quạt lá dừa, giỏ mây, bánh thốt nốt…):
     thỉnh tự do ở quầy cuối tuyến — sưu tầm mang tính tưởng niệm, hiện trong
     "Tủ dấu ấn" ở hồ sơ cá nhân, không hiện trong cảnh, không cấp độ.
4. **Nếu sau này cần doanh thu:** tách *hoàn toàn* khỏi trải nghiệm lễ — hoặc
   bán hàng lưu niệm thật ngoài đời (kênh riêng), hoặc quỹ ủng hộ minh bạch có
   pháp nhân + mục tiêu cụ thể (mục chờ #8 của `THAM_KHAO_TRANG_KHAC.md`, chưa
   khuyến nghị ở giai đoạn này). Tuyệt đối không bán vật phẩm tâm linh lấy lợi
   thế trong app, không "nạp".

---

## TRỤC 5 — VÒNG LẶP QUAY LẠI

### Tham khảo làm gì
- **Sky:** mùa (season) ~77 ngày = 1 bản đồ + 1 câu chuyện + bộ biểu cảm mới;
  nhiệm vụ ngày nhẹ; "Traveling Spirit" 2 tuần/lần mang đồ cũ quay lại. Dịch
  sang chùa: **lịch âm là "season" có sẵn** — không cần bịa sự kiện.
- **Niệm Phật Online (chép pattern, bỏ game-hóa):** thời khóa chung cố định
  05:00 (20') và 20:00 (30') — cơ chế "cùng tu một giờ" không cần multiplayer;
  kèm dòng disclaimer đáng chép nguyên ý: *"chỉ là phương tiện nhắc nhở tu tập,
  không thay thế việc đến chùa"*.
- **Chùa Sen:** khép buổi bằng hồi hướng khiến mỗi lần vào có *đầu–cuối trọn
  vẹn*; trạng thái giữ bằng localStorage, vào lại là tiếp nối.
- **Lịch lễ thật (VN):** mùng 1 + rằm hằng tháng; 5 rằm lớn —
  **Rằm tháng Giêng** (Thượng Nguyên/Nguyên Tiêu: cầu an đầu năm, hội hoa
  đăng, hái lộc), **Rằm tháng Tư — Phật Đản** (tắm Phật, rước đèn, thả hoa
  đăng), **Rằm tháng Bảy — Vu Lan** (bông hồng cài áo, tụng kinh báo hiếu, hoa
  đăng), Rằm tháng Tám (Trung Thu), Rằm tháng Mười (Hạ Nguyên). Tết: đi chùa
  đầu năm, hái lộc (nhận cành lộc/lộc chùa phát).

### Mình có gì
- Chuỗi ngày + thẻ an lạc theo ngày (đang chờ quyết định đổi tên "Dấu ấn hành
  trình", bỏ điểm hiển thị — hướng đã đúng, chưa chốt triển khai).
- Niệm kinh 3 gói là nội dung buổi sẵn có cho thời khóa chung; hồi hướng đã có.
- Ý tưởng **ảnh "Dấu ấn hành trình"** đã được chọn hướng ở nghiên cứu đối thủ
  (mẫu Vinamilk: ảnh cá nhân hoá dễ chia sẻ, không ghi điểm/cấp).

### Thiếu gì
1. **Thời khóa chung theo giờ cố định** (áp dụng #2 của THAM_KHAO): gợi ý 2
   phiên sáng/tối của *nền tảng* (giờ công phu thật của Vĩnh Tràng chưa có
   nguồn công bố — không mạo nhận): đếm ngược trước giờ → chuông khai buổi →
   gói niệm kinh/thiền có sẵn → hồi hướng → dòng ghi nhận "hôm nay có N người
   cùng dự" *chỉ khi có số thật*. Effort S–M, tạo thói quen theo GIỜ thay vì
   streak gây áp lực.
2. **Chế độ ngày lễ theo lịch âm** (P2 nhưng là vòng lặp mạnh nhất):
   - *Rằm/mùng 1 thường:* sân đông NPC hơn, hoa tươi mới, lư hương nhiều khói
     nền (của "khách trước"), mở thả hoa đăng buổi tối ở hồ.
   - *Phật Đản:* trạm **tắm Phật** (tượng Phật đản sinh trong chậu hoa ở sân —
     avatar múc gáo nước thơm rưới tượng, nghi lễ thật đặc trưng của mùa),
     treo đèn lồng lục giác (đã có model), rước đèn quanh sân.
   - *Vu Lan:* **bông hồng cài áo** đỏ/trắng cho nhân vật (trục 3), buổi niệm
     kinh Vu Lan, hoa đăng tưởng niệm ở hồ.
   - *Nguyên Tiêu/Tết:* **hái lộc ở cổng** — nhận 1 cành lộc/lá bồ đề ghi lời
     chúc đầu năm, lưu vào Tủ dấu ấn theo năm; hoa đăng đêm ở hồ.
3. **Dấu ấn hành trình thành sản phẩm:** sau mỗi buổi (đi hết tuyến / dự thời
   khóa / học 1 bài), xuất ảnh dọc: cảnh 3D Vĩnh Tràng + pháp danh + 1 dòng câu
   chữ của buổi + ngày âm lịch. Đây là động cơ chia sẻ Facebook/Zalo cho đúng
   phân khúc 45–70 tuổi mà nghiên cứu UGC đã chỉ ra — thay cho mọi ảnh "khoe
   cấp" của đối thủ.
4. **Đồng hiện diện (sau cùng, cân nhắc kỹ):** Niệm Phật đã phải tắt chat/đổi
   tên vì lạm dụng — multiplayer kéo theo kiểm duyệt là tính năng bắt buộc.
   Giai đoạn này: NPC đúng nhịp (audit G3) + hoa đăng/nến của "người khác" là
   các vật tĩnh có sẵn trong cảnh là đủ cảm giác có người; multiplayer thật để
   P2 cuối, kèm nội quy hiển thị (học cả disclaimer của Niệm Phật).

---

## TRỤC 6 — MODEL 3D & MÀU SẮC

### Màu thật của Vĩnh Tràng (có nguồn — cơ sở của palette chốt)
- **Cổng tam quan:** nghệ thuật **cẩn/gép mảnh sành sứ đa sắc** — tranh sự tích
  Phật, tứ linh, tứ quý bằng mảnh sứ nhiều màu (xanh, đỏ, vàng, trắng sứ) trên
  nền cổng cổ lầu (xây 1930, tên hai cổng Phương Tiện / Tịnh Độ).
- **Tiền đường (mặt tiền):** kiến trúc Âu–Á như dinh thự Pháp thuộc **sơn màu
  vàng**, hàng cột thanh mảnh, vòm Roman/Phục Hưng; nhìn từ tam quan thấy bóng
  **5 ngọn tháp kiểu Angkor** trên mái.
- **Nội thất chánh điện:** **sơn son thếp vàng rực** — tượng Phật tổ lớn và toàn
  bộ ~60 tượng (gỗ/đồng/đất nung) sơn son thếp vàng; 7 bộ bao lam thếp vàng
  (1907–1908) chạm Bát tiên cưỡi thú, thần Mặt trời/Mặt trăng; hoành phi **khảm
  ốc xà cừ** "Đại hùng bảo điện"; bộ 18 La Hán gỗ mít 1907.
- **Nhà tổ:** ngược hẳn — cột gỗ, cửa võng, đối liễn **để nguyên màu gỗ, không
  sơn thếp**: vẻ mộc trầm là một phần của bảng màu thật, không phải thiếu sót.
- **Tượng lớn ngoài trời:** A Di Đà đứng **trắng tinh** 18 m (2008) trên đài
  sen; Di Lặc **bê tông** ~20 m (khánh thành 2010) trên bệ đá; Phật Niết Bàn
  (2013) trên đế dài ~32–35 m sau khuôn viên.
- **Sân & vườn:** sân lát gạch rộng, hoa viên cây xanh Nam Bộ, ao cá (được tu
  sửa 2002) — xanh lá + xám gạch là nền, không phải vàng.

### Chuẩn palette + vật liệu CHỐT (áp cho cả Blender lẫn web)
| Nhóm | Màu chốt (sRGB tham chiếu) | Vật liệu/ghi chú |
|---|---|---|
| Vàng mặt tiền tiền đường | `#D9A441`, vùng bóng `#B9852F` | Sơn mờ (roughness 0,8), tróc nhẹ ở chân tường; trim vòm/cột kem `#F2E8D5` |
| Đỏ sơn son (nội điện) | `#8E2323` (bóng trong `#6E1A1A`) | Lacquer: roughness 0,35, clearcoat nhẹ nếu web chịu được |
| Vàng thếp (tượng, bao lam, chạm) | nền `#C9A227`, điểm sáng `#E8C766` | Metalness 0,85 / roughness 0,35; **cấm emissive** để khoe vàng (lỗi v3) |
| Khảm ốc hoành phi | nền gỗ đen `#2E2019`, ánh xà cừ `#CFC4A8` iridescent nhẹ | Chỉ 1–2 chi tiết điểm xuyết, không phủ rộng |
| Gỗ nhà tổ / cửa võng | `#5A3D26` – `#6E4F30` | Để mộc, roughness 0,7, **không thếp vàng** |
| Sứ cẩn cổng tam quan | cobalt `#2C4A8A`, ngọc `#3F7D5D`, đỏ gạch `#A03A2A`, vàng đất `#C9962E`, trắng sứ `#E8E2D4` | Mảnh nhỏ đa sắc trên nền xám ấm `#8B7D6B`; độ bóng sứ vừa |
| Tượng trắng / bê tông ngoài trời | A Di Đà `#EFE9DD`; Di Lặc + đế `#DDD6C8` | Bê tông có vệt thời tiết rất nhẹ; đài sen A Di Đà xanh `#4A7A5E` (theo bố cục đã khoá) |
| Mái ngói + tháp | ngói `#8A4A34` (phong hoá không đều), tháp tone đá `#9A8B74` | Ngói cũ: biến thiên ±10% sáng giữa các mảng |
| Sân gạch | `#9C6B52` dịu, mép rêu `#5C6E46` | Gạch là nền trung tính cho chủ thể vàng/trắng nổi lên |
| Vườn & hồ | lá `#4D7038`–`#6A8F4A`, sen hồng `#D77A9A`, mặt hồ `#33513F` | Xanh bão hoà vừa; hồ có gợn + bóng cá (audit G5) |
| Nhân vật | lam `#7D8AA0`, nâu sòng `#6B4A33`, xám `#8A8578`; bà ba trắng `#EDEAE2`/xanh `#7FA3B8`; áo dài trắng/pastel | Muted toàn bộ — nhân vật không được chói hơn tượng |

### Ánh sáng — giữ nguyên đặc tả của audit, không thương lượng lại
- Blender: AgX, exposure 0,85–1,0, nắng 2,2–2,6 màu (1,00/0,82/0,62) cao độ
  28–35° hướng tây, world 0,35–0,45, saturation 0,92–0,97 (audit D1) — cảm
  giác **16h30–17h00**, không phải trưa.
- Web: exposure 1,02, Hemisphere 1,15 (trời `#FFE8C4`/đất `#4A2C17`), nắng 1,5
  `#FFD9A3`, Spot Phật 6,5, emissive trần 2,2, fog `#2A1A10` 0,007, vignette ấm
  + wash `#FFB46B` 6–8% (audit D2). Nội điện tối hơn ngoài trời *có chủ ý* bằng
  ngân sách đèn theo zone.
- Nguyên tắc màu tổng: **ngoài trời = vàng ấm + xanh dịu; trong điện = đỏ son +
  vàng thếp trên nền gỗ tối; nhà tổ = gỗ mộc.** Ba "phòng màu" này phân biệt rõ
  là dấu hiệu nhận diện Vĩnh Tràng — model nào sơn một tông vàng đồng nhất từ
  cổng vào điện là sai màu thật.

### Thiếu gì ở model (ngoài màu)
1. Lư hương chính + 2 lư nhỏ chưa có trong cảnh render (audit C1 — vị trí theo
   thông lệ, **phải đối chiếu ảnh thật khi dựng**, chưa kiểm chứng).
2. Thùng công đức, sạp/quầy cổng, bảng nội quy + tên cổng Phương Tiện/Tịnh Độ
   bằng chữ trong cảnh (audit G7) chưa có model.
3. Hồ + mặt nước động, bồ câu, cây bồ đề có lá rơi (audit G5) chưa có.
4. Nhân vật trong render bố cục còn thưa và đứng yên (audit N3/G3): tối thiểu
   8 nhân vật, ≥2 đang ở tư thế lễ/thắp nhang.

---

## BACKLOG ƯU TIÊN — nối đúng thứ tự dựng của audit (mục E + G8), không đảo lộn

### P0 — Nền "đi được + lễ được + đúng sáng" (= audit E1–E3 + chèn G8)
1. **Cảnh khuôn viên + đi bộ tự do + tuyến trạm S0–S7** [L] — 4 kênh điều
   khiển (audit B1), polyline đường chùa, camera sau vai; **chèn ngay trong
   bước này:** NPC khách + nhà sư đúng nhịp (G3), đường cong ồn→tĩnh (G6), và
   **xoá ngay** số online giả + huy hiệu "Cấp" + pop-up "+5 công đức" + gói giá
   đèn nguyện khỏi UI lễ (K3/K5 — làm ngay, độc lập, nửa giờ).
2. **Chuỗi thắp nhang hoàn chỉnh** [M] — audit C2 đủ 5 nhịp tại lư sân chính +
   bát hương chánh điện, khói theo C3 (sprite mềm, opacity ≤ 0,4, cháy tới hết
   phiên); **chèn G2:** trạm nhận nhang/hoa ở cổng S0, nhịp bỏ dép ở cửa S3,
   thùng công đức (tương tác không số) cạnh cửa chánh điện.
3. **Grade ánh sáng + palette** [S] — áp D1 (Blender) + D2 (web) và bảng palette
   chốt ở trục 6 cho toàn cảnh; thanh trượt sáng ± trong Cài đặt giữ như audit.

### P1 — Không gian sống + nghi lễ mở rộng (sau khi P0 chạy được)
4. **Ambience 5 zone theo dossier** [M] — audit E4/G4 đủ bảng, crossfade theo
   trạm, bước chân theo zone, tải lười ≤ 1,5 MB.
5. **"Đi theo chú tiểu An" + khép buổi ở tháp + ảnh Dấu ấn hành trình** [M] —
   audit E5; ảnh xuất được để chia sẻ (pháp danh + câu chữ buổi + ngày âm).
6. **Gói chi tiết sống** [S–M] — audit G5: bồ câu sân, lá bồ đề rơi ngoài sân
   (bỏ mưa cánh sen trong nhà), hồ + cá + sen 3 trạng thái, flicker nến, nhang
   cháy ngắn dần + tro.
7. **Nghi lễ mở rộng** [M] — thỉnh chuông ở gác chuông (decay 8–12 s); lạy 3
   lạy có hướng dẫn ngũ thể của An (ghi nợ action Lạy đầy đủ); xin xăm Quan Âm
   theo đặc tả trục 1 (1 lần/ngày, khung suy ngẫm); dâng hoa quả (nhặt hoa quanh
   hồ → dâng chánh điện); thả hoa đăng trên hồ của bước 6.
8. **Trang phục trong trải nghiệm + thỉnh vật phẩm** [M] — tủ áo ở trạm cổng
   (lam/nâu/xám, áo tràng 2 màu, bà ba + khăn rằn; áo dài ghi nợ model), ô pháp
   danh; quầy thỉnh vật phẩm ở S7 theo mô hình trục 4 (không giá, không điểm).

### P2 — Vòng lặp lịch lễ + dài hạn
9. **Thời khóa chung 2 phiên/ngày của nền tảng** [S–M] — đếm ngược + chuông
   khai buổi + niệm kinh có sẵn + hồi hướng; ghi rõ giờ của nền tảng, không
   mạo nhận giờ chùa.
10. **Mùa lễ theo lịch âm** [M mỗi mùa] — rằm/mùng 1 (đông hơn, hoa đăng tối);
    Phật Đản (tắm Phật + đèn lồng + rước đèn); Vu Lan (bông hồng cài áo + hoa
    đăng tưởng niệm); Nguyên Tiêu/Tết (hái lộc ở cổng + hoa đăng đêm).
11. **Công quả nhẹ** [S] — "giờ công quả" buổi sáng: quét sân cùng NPC, dọn hoa
    tàn — ghi vào Dấu ấn bằng câu chữ, không điểm.
12. **Onboarding 30 giây + PWA** [S] — vào thẳng sân với nhân vật mặc định, tuỳ
    biến để sau; cài màn hình chính cho cô chú.
13. **Đồng hiện diện thật** [L + kiểm duyệt] — chỉ làm khi có nội quy hiển thị +
    cơ chế kiểm duyệt sẵn sàng (bài học Niệm Phật phải tắt chat); trước đó giữ
    NPC + vật tĩnh của "người khác".

---

## Ghi chú kiểm chứng (kế thừa audit mục F, bổ sung)
- Vị trí lư hương sân, giờ mở cửa, việc Vĩnh Tràng có gian xin xăm: **chưa kiểm
  chứng** — khi dựng phải đối chiếu ảnh/nguồn thật, không khẳng định.
- Giờ công phu chính thức của Vĩnh Tràng: chưa có nguồn công bố — thời khóa
  trong app là giờ của nền tảng.
- Số liệu Sansa/Niệm Phật trong `THAM_KHAO_TRANG_KHAC.md` là số tự báo cáo của
  các site/báo chí — chỉ dùng làm bài học pattern, không dùng làm dữ kiện thị
  trường.
- Tên gọi hành chính (tỉnh Tiền Giang/Đồng Tháp sau sáp nhập 01/07/2025) là
  quyết định của Chung Hy — báo cáo này giữ cách gọi hiện hành của dự án.
