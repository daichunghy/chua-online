# KẾ HOẠCH CẢI THIỆN CHÙA ONLINE — CHÙA VĨNH TRÀNG 3D

Nguyên tắc xuyên suốt: **chân thật và khác biệt**. Các "chùa online" đang nổi phần lớn là chùa tưởng tượng (không có thật, bố cục tự bịa). Dự án này dựa trên một ngôi chùa thật — di tích cấp quốc gia, có địa chỉ, có lịch sử gần 200 năm — nên mọi cải thiện đều phải kiểm chứng được với chùa thật.

Người phụ trách mặc định: Muse thực thi, Logan duyệt ở các điểm chốt ghi rõ bên dưới.
Số liệu render đo thực tế trên máy Muse (không GPU): Eevee 1280×720, 64 samples ≈ 3,5–4 phút/frame. Mọi thời lượng dưới đây là ước lượng theo số đo này.

---

## PHẦN 0 — CHUẨN THAM CHIẾU (đã xong phần lớn)

- [x] 6 ảnh thật đã tải và kiểm chứng đúng chùa Vĩnh Tràng: toàn cảnh flycam, mặt tiền chánh điện, cổng tam quan, A Di Đà, Di Lặc + tháp, Phật nằm.
- [x] Đã đối chiếu và xác định các sai lệch của các bản dựng hiện có (xem Phần 1).
- [ ] Bổ sung 3 ảnh còn thiếu trước khi dựng sâu: nội điện Tam Bảo, chi tiết khảm sành cổng tam quan, tượng A Di Đà trong vườn bên phải (điểm hay bị bỏ sót).
- Điểm chốt 0: Logan duyệt bộ ảnh bổ sung — tiêu chí: mỗi hạng mục ở Phần 1 phải có ít nhất 1 ảnh thật đối chiếu trực tiếp.

## PHẦN 1 — MODEL ĐÚNG CHÙA THẬT (sửa trên bộ "Bản dựng mới", không dựng lại từ 0)

Bố cục tổng thể khóa theo ảnh flycam (đây là điểm khác biệt số 1 — không chùa online tưởng tượng nào có):
hai cổng tam quan ở hai đầu mặt tiền, hàng rào vàng, hồ nước chữ nhật ở giữa, chánh điện bên phải, Di Lặc bên trái, tháp 7 tầng và Phật nằm ở phía sau, A Di Đà trong vườn bên phải, bao quanh là vườn dừa.

| # | Hạng mục | Hiện trạng (đã kiểm chứng) | Việc phải làm | Nghiệm thu |
|---|----------|------------------------------|---------------|------------|
| 1.1 | Chánh điện | Render hiện tại màu kem/be, nền đen | Đổi vật liệu sang vàng rực theo ảnh mặt tiền; thêm nền trời xanh + sân gạch + bonsai | Đặt render cạnh ảnh thật: màu vàng chiếm đúng tông chủ đạo, không còn nền đen |
| 1.2 | Mái chánh điện | Dải phẳng hồng nhạt | Dựng khối mái ngói đỏ nâu lớn phía sau mặt tiền như ảnh flycam | Góc flycam thấy rõ khối mái đỏ nâu sau mặt tiền vàng |
| 1.3 | Cửa vòm | Bản cua-vom đã có song sắt vàng, cột xanh ngọc | Đếm lại số vòm từ ảnh thật và khóa con số; chỉnh cột về đỏ + xanh ngọc đúng ảnh | Số vòm trong model = số vòm đếm trên ảnh, có ghi nguồn ảnh |
| 1.4 | Cổng tam quan | Chưa có trong bản tổng thể | Dựng tháp cổng cao hẹp khảm sành, 1 vòm lớn, ô giữa có tượng Phật, đặt 2 cổng hai đầu | Đúng 3 đặc điểm: cao hẹp / 1 vòm / tượng ở ô giữa |
| 1.5 | Ba tượng lớn | Chưa ghép vào bản tổng thể | Di Lặc trắng ngồi trên bệ đá chữ vàng (trái); Phật nằm trắng trên bệ cao, dòng chữ "Nam Mô Bổn Sư Thích Ca Mâu Ni Phật" (sau); A Di Đà trắng trên đài sen xanh (vườn phải) | Đúng vị trí theo flycam, đúng màu trắng + bệ tương ứng |
| 1.6 | Tháp 7 tầng | Đã có trong bản bố cục, còn thô | Tinh chỉnh mái cam từng tầng, tỉ lệ so với Di Lặc | Đứng cạnh Di Lặc không lấn át, đúng ảnh Di Lặc + tháp |

## PHẦN 2 — TRẢI NGHIỆM ĐI CHÙA THÚ VỊ (gắn lên trai-nghiem-chua-vinh-trang-3d.html sẵn có)

Hiện trạng đã kiểm chứng trong file gốc: đã có lạy Phật, tràng hạt, tụng kinh, thả đèn nguyện, chuông mõ WebAudio, shop. Thiếu toàn bộ cơ chế **giữ chân và quay lại** (localStorage = 0, không lưu gì cả).

| # | Tính năng | Cách làm cụ thể | Nghiệm thu |
|---|-----------|------------------|------------|
| 2.1 | Hành trình 1 mạch | Checklist 5 chặng theo đúng trình tự đi chùa thật: thắp hương → lạy Phật → lần tràng hạt → thả đèn nguyện → rút thẻ an lạc. Hoàn thành chặng nào sáng chặng đó | Người mới vào tự đi hết 5 chặng không cần hướng dẫn ngoài, ≤ 5 phút |
| 2.2 | Thẻ an lạc mỗi ngày | 12 thẻ lời chúc/kệ ngắn; seed theo ngày — mỗi ngày 1 thẻ duy nhất, qua ngày mới có thẻ mới; lưu thẻ đã rút | Rút 2 lần trong ngày ra cùng 1 thẻ; hôm sau khác thẻ |
| 2.3 | Điểm công đức + chuỗi ngày | Cộng điểm theo hành động có sẵn (lạy +5, tràng hạt đủ vòng +20, thả đèn +10…), lưu localStorage, hiển thị chuỗi ngày liên tiếp | Tải lại trang không mất điểm; ngắt 1 ngày thì chuỗi reset đúng |
| 2.4 | Chú tiểu dẫn đường | Bong bóng thoại ngắn ở từng chặng, kể 1 chi tiết thật về chùa (năm xây, tượng cao bao nhiêu — chỉ dùng số liệu có nguồn) | Mỗi chặng 1 câu ≤ 25 chữ, không câu nào không có nguồn |
| 2.5 | Âm thanh | Giữ WebAudio chuông/mõ sẵn có; bổ sung tiếng chuông gió + chim nền, tắt mặc định, bật bằng 1 nút | Bật/tắt hoạt động, không tự phát khi chưa bấm |

## PHẦN 3 — NHÂN VẬT & VẬT PHẨM (khác biệt số 2: người đi chùa Việt thật)

- Hiện trạng: render nữ Phật tử đội nón lá bị washed-out (trắng xám, mất mặt) — lỗi sáng/vật liệu, không phải lỗi model.
- Việc làm: chỉnh lại đèn + tông da + áo tràng xám đúng ảnh người đi chùa thật; nón lá giữ chi tiết nan như bản PBR đã có.
- Nghiệm thu: render nhân vật đặt cạnh ảnh chụp người đi lễ thật — nhận ra được nón lá, áo tràng, khuôn mặt; không còn trắng xám.

## PHẦN 4 — PHÁT HÀNH & ĐO LƯỜNG

- Đẩy mọi thay đổi lên repo `daichunghy/chua-online`, cập nhật Gallery README bằng render mới (thay ảnh nền đen).
- Mỗi hạng mục chỉ tính là xong khi có ảnh render đối chiếu trước/sau đính kèm trong commit.
- Chỉ số theo dõi duy nhất sau phát hành (1 lagging): lượt mở trang trải nghiệm; tối đa 3 leading: tỉ lệ hoàn thành 5 chặng, tỉ lệ rút thẻ, tỉ lệ quay lại ngày hôm sau. Không thêm chỉ số khác.

## RỦI RO / GIỚI HẠN ĐÃ BIẾT

- Máy Muse không có GPU: render Eevee chậm (đo ở trên). Khắc phục: render kiểm tra ở 720p, bản cuối 1080p chạy nền qua đêm hoặc render trên máy Logan bằng chính file .blend đã đẩy lên repo.
- Số liệu lịch sử/kích thước tượng dùng trong lời dẫn (2.4) bắt buộc có nguồn; chưa có nguồn thì để trống, không bịa.
- Âm thanh chuông/mõ hiện là tổng hợp WebAudio. Muốn "thật" hơn nữa cần file ghi âm chuông thật — điểm chốt 4: Logan quyết định dùng bản ghi âm (cần nguồn file) hay giữ tổng hợp.


### NHẬT KÝ ĐỐI CHIẾU — bổ sung 2026-11-05 (tối)

- **Vòng 3 — Nội điện: ĐẠT.** Nguyên nhân cháy sáng không nằm ở hệ màu mà ở năng lượng đèn trong script gốc (đèn bàn thờ 3200, đèn rọi tượng 1800, đèn nến 350). Đã hạ về 1200 / 700 / 120, hào quang emission 5.5 → 2.8, giữ AgX cho nội thất (Standard chỉ dùng mặt tiền). Kết quả: hết cháy trắng, giữ được hơi ấm bản gốc. Script: scripts/blender_build_vinh_trang_cai_tien_v3.py; preview: render_noi_dien_v2.jpg. Nợ còn lại: tượng trong model gốc là khối cầu đơn giản — muốn đọc ra tượng Phật ngồi cần điêu khắc lại (cùng loại nợ với tượng Di Lặc / Phật nằm).
- **Vòng 4 — Bố cục tổng thể V2: ĐẠT (khối lượng).** Bổ sung vào bo-cuc-theo-anh.blend: hồ nước chữ nhật, tượng Phật đứng đài sen xanh góc trước–trái (theo đính chính ref14), 2 cổng tam quan hai đầu mặt tiền (theo ref10), hàng rào vàng. Script: scripts/dung_bo_cuc_v2.py; render: render_bo_cuc_v2.jpg. Di Lặc + Phật nằm vẫn là bệ chờ tượng điêu khắc — giữ trạng thái trung thực, không bịa tượng thô. Lưu ý kỹ thuật: file .blend của repo được lưu bằng Blender 5.0.2 (nén zstd) — phải mở bằng Blender 5, bản 4.2 không đọc được.
- **Phần 2 bổ sung — Trải nghiệm V3: XONG.** trai-nghiem-vinh-trang-v3.html: chọn profile nhân vật, niệm kinh (3 gói 5/10/20 phút, karaoke theo câu, mõ/chuông WebAudio, đếm 108 hạt), bài giảng Giảng đường Huệ Đăng (4 lộ trình theo hồ sơ nghiên cứu, 1 bài mẫu đủ 6 phần). Hồ sơ: research-am-thanh-bai-giang-niem-kinh-profile.md.
- **Phần 3 — Trang phục mặc định: ĐỦ 3/3 ĐẠT.** Nữ (fit_real.py), nam + trẻ em (fit_nam.py, fit_tre_em.py — công thức v2: vành 0,885 H, chóp sâu 0,125 H có đỉnh cụt, quai 3 đoạn ôm bề mặt thân). Tài liệu: Nhân vật 3D/TRANG_PHUC_MAC_DINH_3_NHAN_VAT.md + render-fit-nam.jpg, render-fit-tre-em.jpg. Ghi chú: thân túi là mesh túi vải trơn sẵn có, chưa có hoa văn thêu sen.

- **ĐÍNH CHÍNH 22:52 cùng ngày — Vòng 4 bị bác:** Chung Hy xem render bố cục V2 và chê sản phẩm nhìn ghê, "ngượng gạo" — ĐÚNG: bản đó chỉ đạt checklist vị trí/khối lượng, hình ảnh vẫn là khối thô + tượng nón tự chế, không đạt chuẩn "giống thật" của dự án. Thu hồi đánh giá ĐẠT. Hướng làm lại: tượng phải là model có texture tạo từ ảnh thật (pipeline Hunyuan3D như nhân vật), mặt tiền dùng model chi tiết sẵn có (cua-vom / mat-tien), bỏ hẳn tượng/khối tự chế bằng hình cơ bản.

- **Đêm 05–06/11 (sau 23:00) — kiểm kê + dùng model repo có sẵn, soi thật, sửa theo verdict:**
  - **Vật phẩm:** phát hiện catalog 21 món đã có sẵn model trong repo (`Thiết kế giao diện/Vật phẩm 3D/models/` — GLB/OBJ kèm texture) nhưng chưa bao giờ được kiểm kê/fit. Kiểm chứng 15 OBJ: **không món nào dùng ngay được** — tất cả dính lỗi normals export (mở lên đen gần hoàn toàn), 0 texture, quạt hỏng hẳn (đĩa tròn trên cọc), giỏ quai gãy + bịt miệng, chum bịt miệng, đèn lồng mặt lụa không hiện, cánh sen là hộp chữ nhật. Đã sửa xong hình học 15/15 (normals + vật liệu + dựng lại quạt, kích thước về đúng catalog 0–3%), GLB sạch trong `repo-items/fixed/`; render kiểm chứng + push đang chạy theo điều phối (nhường CPU cho final video tới 06:12 rồi mở lại).
  - **Fit lên 3 nhân vật (V2 — model repo có texture):** nón thêu sen v3 GLB, túi thêu sen GLB, tràng hạt, hoa sen tươi, khăn rằn — ĐÃ PUSH (scripts/items_worn.py + 3 render + tài liệu trang phục V2). Đạt: túi/nón/tràng hạt ở cả 3; nữ có hoa sen đọc đúng. **Chưa đạt (Muse tự soi bác verdict của tuyến con):** hoa sen cầm tay nam + trẻ em — búp thành cụm bóng hồng, lá thành đĩa xanh nằm ngang giữa thân như cái khay; đang sửa lại, xếp sau mốc 06:12. Khăn rằn đọc thành vành xám trơn vì file repo không có texture caro (giới hạn file gốc, đã ghi rõ).
  - **Tượng điêu khắc (vòng 1 đã soi):** A Di Đà đứng đài sen xanh, Di Lặc, Phật nằm, Phật bàn thờ — đúng dáng/bố cục theo ảnh thật, thay được khối thô. **Chưa đạt mức "như thật":** mặt tượng còn trơn (Di Lặc không đọc ra nụ cười); biển A Di Đà bị **ngược chữ** — phải sửa. Vòng 2 đang sửa (tay A Di Đà, đầu Phật nằm, tay Di Lặc, chữ biển), render kiểm chứng sau mốc 06:12.
  - **Mặt tiền chánh điện V3e — ĐẠT:** dùng model cửa vòm chi tiết của repo (13 ô vòm, song vàng, cột gốm xanh), nhuộm vàng bão hòa theo ảnh thật (Standard, vàng 1.0/0.60/0.02), bỏ khối mái giả (bản v3/v3b/v3c đều sai thành dải phiến lơ lửng) — khung chỉ lấy mặt tiền + đường mái trang trí + trời. Script: scripts/facade_v3.py; render: Mô hình 3D Vĩnh Tràng/render_mat_tien_v3.jpg. Mái lớn làm trong cảnh tổng thể, không ghép khối giả vào khung mặt tiền nữa.
  - **Tham khảo trang khác:** hồ sơ THAM_KHAO_TRANG_KHAC.md (so sánh Niệm Phật Online / Chùa Sen / Sansa): Vĩnh Tràng thắng ở chùa thật + model từ tư liệu thật; không sao chép game-hóa sâu (cảnh báo GHPGVN); học được: ngồi bồ đoàn mới mở công phu, hồi hướng khép buổi, ảnh "Dấu ấn hành trình" để chia sẻ, thời khóa chung dùng gói niệm kinh V3.
  - **Chuẩn judgement chốt 02:00 06/11:** mọi kết quả qua kiểm chứng thực nghiệm có bằng chứng (mở file, đo thật, render soi) và báo verdict thẳng — đạt / cần sửa / hỏng kèm lý do; không báo đạt theo cảm tính hay theo lời tuyến con chưa tự kiểm chứng. Áp dụng mọi dự án, lâu dài.

- **Sáng 06/11 — sự cố file nhị phân trên repo + đã sửa xong toàn bộ:** phát hiện đường đẩy GitHub qua connector (create_or_update_file / push_files) chỉ lưu được file TEXT — truyền base64 của ảnh/model vào thì repo chứa nguyên văn chuỗi base64, file hỏng nhưng thao tác vẫn báo thành công. Tổng cộng **13 render JPG bị hỏng kiểu này** (gồm cả các file trước đây được báo "đã đẩy + đọc kiểm chứng"). Đã sửa dứt điểm qua giao diện web GitHub và ĐỌC LẠI TỪNG FILE xác nhận (magic bytes JPEG + dung lượng khớp byte-exact với bản local): tải lại thật 11 file (render mặt tiền v3, nội điện v2, mặt tiền v2, bố cục v2, 7 render nhân vật/fit) + bộ tượng verified_v2 gồm 4 GLB + 4 render (thư mục Mô hình 3D Vĩnh Tràng/Tượng); xoá 2 file hỏng không còn bản gốc (render-fit-model-that-v1.jpg, render-kiem-chung-vua-van.jpg — lịch sử git vẫn giữ). Hai PNG lớn (render_vinh_trang_facade.png, render_vinh_trang_altar.png) kiểm tra trực tiếp trên web: hiển thị bình thường, không dính lỗi. **Quy tắc cứng từ nay: file nhị phân chỉ tải lên bằng web GitHub; đẩy xong bắt buộc đọc lại bytes thật mới tính là đã lên.** Kiểm chứng buổi sáng: hoa sen cầm tay nam/trẻ em ĐẠT (đã soi render v2); tượng vòng 2 đạt ở dáng/bố cục/chữ bệ (cả 3 bảng chữ từng bị gương do texture lật + mặt bảng quay ngược — đã sửa cả hai lớp), mặt tượng có nét hơn nhưng vẫn trơn — nợ chất lượng ghi công khai; kiểm chứng 15 vật phẩm đang chạy (quạt đạt mức tối thiểu, giỏ mây đạt hẳn, chum sành bị bác làm lại: chum đọc thành khối cầu trơn, búp sen chưa có cánh).
## Nhật ký 2026-11-06 (sáng) — LAYOUT V3 ĐẠT (còn nợ hàng rào)

Bố cục tổng thể lắp từ tài sản đã kiểm chứng: chánh điện = facade cua-vom đã tô lại vàng (13 ô vòm) + mái hông dựng trong script (repo không có khối mái lớn thật), tượng verified_v2 (A Di Đà đài sen xanh góc trước-trái, Di Lặc bệ đá sẫm trái-giữa, Phật nằm đầu hướng tây sau trung-phải), 2 cổng tam quan + 2 hồ cảnh + đường chính lấy từ model khuôn viên repo, 15 vật phẩm fixed, 3 nhân vật đã fit (nón/túi/tràng hạt/hoa sen, pose Chắp tay). Script `scripts/layout_v3.py`, NOTES `Mô hình 3D Vĩnh Tràng/Bố cục/NOTES.md`. Render Cycles 32 mẫu 1280×720: **flycam ĐẠT 6,5/7 mốc** (so ref9/ref14), **mặt đất ĐẠT** (so ref1: 13 vòm, song vàng, cột gốm xanh, mái đặc, 3 nhân vật trên thềm). 3 lỗi đã sửa: mặt phẳng studio `Ground` của GLB tượng che mất hồ/sân; `matrix_world` stale sau import làm nhân vật lệch gấp đôi vào hồ; hàng ngói tách khe nhìn xuyên trời → chồng mí. **Nợ: hàng rào vàng chu vi KHÔNG có asset (2 cổng đứng lẻ); cây thưa; mặt tượng còn trơn.** File `layout_v3.blend` 31,9MB > giới hạn 25MB của web GitHub → chỉ giữ local; render PNG + GLB nhân vật tải web được.
