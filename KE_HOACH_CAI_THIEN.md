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
