# KẾ HOẠCH V14 — NẮN MẶT TƯỢNG CHI TIẾT VỀ PHÍA ẢNH THẬT (GIAI ĐOẠN ĐO + KẾ HOẠCH)

**Trạng thái: ĐÃ ĐO XONG, CHƯA THI CÔNG.** File này là đầu ra của tuyến
song song V14 (10/11/2026): bảng đo chi tiết mặt 2 tượng + kế hoạch thao
tác gắn số đo đích + script nháp `build_v14.py` (chưa chạy build, chưa
render). File chuẩn vẫn là `layout_v15_v13.blend` — không ai được ghi đè
nó; bản thi công (khi được chạy) lưu riêng `layout_v16_v14.blend`.

**Luật cứng (không đổi):** tượng Phật phải trang nghiêm — TUYỆT ĐỐI không
stylize, không sửa theo cảm tính. Hướng duy nhất: đưa nét mặt VỀ PHÍA
tượng thật trong ảnh. Mọi thao tác phải gắn số đo đích dưới đây. Không
đụng tai (V13 đã đạt), không đụng thân/bệ/tỉ lệ tổng, không đụng Phật nằm.

---

## 1. Phương pháp đo (đo không đoán — ghi cách đo)

| Phía | Cách đo | Công cụ / nguồn |
|---|---|---|
| Ảnh thật | Crop mặt phóng 6× bằng PIL (LANCZOS) từ ref5 (Di Lặc), ref11 + ref3 (A Di Đà), lấy bbox landmarks bằng visual grounding, quy về tỉ lệ theo bbox đầu trong cùng ảnh | `v14_measure/crop_ref5_face.png`, `crop_ref11_face.png`, `crop_ref3_face.png` |
| Model | Parser GLB thuần Python: bbox từng mảnh `Head_*` từ accessor min/max + ma trận node (hệ GLB Y-up, mặt hướng −Z) | `v14_measure/glb_face_measure.py` → số thô ở mục 2 |
| Độ nổi (mới, V13 chưa đo) | Mặt trước của mảnh so với bề mặt ellipsoid sọ (tâm + 3 bán trục từ bbox `Head_skull`) tại (x,y) tâm mảnh; sai số xấp xỉ ±0,03 m | cùng script trên |
| Đối chiếu chéo | Số GLB khớp số Blender của V13 tại các mốc chung: head_h Di Lặc 1,8401 / A Di Đà 1,2388; tỉ lệ tai tiền-V13 0,486 / 0,407 — parser tin cậy được | NOTES §V13, `v13_audit.json` |

**Vì sao số GLB dùng thay số scene:** mảnh mặt trong `layout_v15_v13.blend`
là nguyên bản verified_v2 (V12 khôi phục nguyên bản; V13 chỉ đổi ma trận
tai — verify V13 độc lập: checksum mesh lệch = rỗng, ma trận lệch ngoài
nhóm tai = rỗng). Các tượng trong scene là bản sao qua phép đồng dạng đều
nên mọi tỉ lệ + tỉ số độ nổi/headH trong GLB giữ nguyên trong scene.
Script thi công vẫn phải chạy `measure_v14.py` (giai đoạn 0) để xác nhận
lại ngay trong scene trước khi sửa — xem mục 5.

**Giới hạn đo phải nói thẳng:**
- ref5 chụp 3/4 (mặt quay ~25–30°) từ dưới lên: tỉ lệ ngang phía xa bị
  nén phối cảnh ~15% → chỉ dùng mắt phía gần + các tỉ lệ dọc.
- ref11 gần chính diện nhưng mặt tượng chỉ ~90 px gốc → bbox landmark có
  sai số ±5–8% ở các mảnh nhỏ (mắt/miệng gồm cả bóng mí/môi).
- Ảnh không đo được độ sâu: kết luận "ống nổi vs rãnh/relief" chấm bằng
  đối chiếu render V15 (`layout_v15_face_*.png`) cạnh ảnh thật, còn số đo
  độ nổi lấy từ model (mục 2) — hai bằng chứng độc lập cùng chỉ một hướng.
- Ngưỡng quyết định: lệch > 7% (quy ước V13) mới đề xuất sửa.

---

## 2. Bảng đo — DI LẶC (ref5 ↔ model GLB; mẫu số: head_h = 1,8401 m, head_w = 1,7148 m)

| # | Chỉ số | Ảnh thật | Model | Lệch | Kết luận |
|---|---|---|---|---|---|
| D1 | Rộng đầu / cao đầu | 0,962 | 0,932 | −3% | GIỮ — trong nhiễu |
| D2 | Mắt: rộng / head_w (mắt gần) | 0,220 | 0,220 | 0% | GIỮ kích thước |
| D3 | Mắt: khoảng cách 2 tâm / head_w | 0,360 | 0,381 | +6% | GIỮ — trong nhiễu (ảnh 3/4 nén ngang) |
| D4 | Mắt: tâm theo chiều dọc (từ đỉnh đầu) / head_h | 0,385 | 0,398 | +3% | GIỮ vị trí |
| D5 | Mắt: cao / head_h | 0,072 | 0,071 | −1% | GIỮ — nhưng xem D6 |
| D6 | **Mắt: DẠNG** — ảnh là rãnh cong khít mặt; model là ống cong tiết diện gần tròn (Y 0,130 × Z 0,119 m), nổi +0,017 m tại tâm nhưng hai đầu ống hở khỏi mặt cong → render thành 2 ống trắng nổi, có bóng tách | rãnh | ống | KHÁC DẠNG | **SỬA DẠNG: ép dẹt ống theo trục sâu (mục 4, op D-a)** |
| D7 | **Mày: độ nổi** — ảnh: dải relief mờ liền mặt, không bóng tách; model: ống Ø ~0,10–0,12 m, nổi **+0,119 m (+0,064 head_h)** khỏi ellipsoid sọ | ≈ liền mặt | +0,119 m | VƯỢT XA | **SỬA: ép dẹt + hạ chìm (op D-a)** |
| D8 | **Mũi: rộng / head_w** | 0,250 | 0,170 | **−32%** | **SỬA: nới rộng ngang mũi về 0,25 (op D-b)** |
| D9 | Mũi: cao / head_h | 0,240 | 0,215 | −10% | Theo dõi — nới ngang ở D-b không đổi cao; chấm lại sau render |
| D10 | Mũi: rộng/cao | 1,00 | 0,74 | −26% | Hệ quả của D8; đích sau sửa ≈ 0,97 |
| D11 | **Miệng: tâm dọc / head_h (từ đỉnh)** | 0,663 | smile 0,717 / mouth 0,780 | +8% / +18% | **CHƯA SỬA NGAY — cổng kiểm chứng:** ảnh chụp từ dưới + mặt cúi có thể bóp tỉ lệ dọc; phải render cùng góc chụp ref5 rồi đo lại trên render; chỉ sửa nếu lệch >7% vẫn đứng (op D-d, giai đoạn cổng) |
| D12 | Miệng: đáy miệng → cằm / head_h | 0,279 | 0,117 (mouth) | −58% | Cùng cổng với D11 — hai số này liên đới vị trí miệng |
| D13 | Miệng: rộng / head_w | 0,370 (phần miệng mở) | smile 0,508 / mouth 0,419 | — | GIỮ — mảnh model rộng hơn phần mở trong ảnh là bình thường (mảnh gồm cả viền môi/khóe); không có căn cứ thu hẹp |
| D14 | **Má: DẠNG** — ảnh: má phình liền khối, chuyển mặt liên tục; model: 2 cầu rời (Ø ~0,63×0,55×0,51 m) nổi **+0,203 m (+0,110 head_h)** khỏi ellipsoid sọ → render thấy 2 quả cầu dán lên mặt | liền khối | cầu rời | KHÁC DẠNG | **SỬA MỘT PHẦN bằng ma trận: ép dẹt trục sâu ×0,60 quanh pivot ở mặt sau mảnh (op D-c)** — giảm đọc "cầu dán"; hòa khối thật cần sculpt mesh, ngoài phạm vi bản nháp này (mục 6) |
| D15 | **Nếp cười (crease): DẠNG** — ảnh là **rãnh âm** (đường bóng chìm từ cánh mũi xuống khóe miệng); model là ống nổi (+0,092 m, tiết diện Z 0,098 m) | rãnh âm | ống nổi | NGƯỢC DẤU | **SỬA: ép dẹt + hạ chìm như D-a (op D-a)** — đích: đọc thành vệt relief sát mặt; biến thành rãnh âm thật cần can thiệp mesh (mục 6) |
| — | Cằm (chin): nổi +0,318 m | cằm đôi liền khối | khối cằm | — | GIỮ — cằm Di Lặc trong ảnh cũng phình mạnh; không có số đo ảnh đủ vững để sửa |

**Chốt Di Lặc:** kích thước/vị trí mắt–mày–miệng (trừ cổng D11/D12) và má
đều trong nhiễu đo — V13 kết luận "mắt/mũi/miệng/má lệch ≤7%" chỉ đúng ở
lớp TỈ LỆ. Lớp lệch thật nằm ở (1) **DẠNG ống nổi thay vì rãnh/relief**
(mày, mắt, nếp cười), (2) **rộng mũi −32%**, (3) **má dạng cầu rời**.
Đây là căn cứ đo được, không phải cảm tính.
---

## 3. Bảng đo — A DI ĐÀ (ref11 chính, ref3 đối chiếu; head_h = 1,2388 m, head_w = 0,8419 m)

| # | Chỉ số | Ảnh thật | Model | Lệch | Kết luận |
|---|---|---|---|---|---|
| A1 | Rộng đầu / cao đầu (gồm ushnisha) | 0,565 | 0,680 | +20% | **NỢ ĐO — KHÔNG SỬA Ở V14:** V13 từng ghi số đầu/thân A Di Đà mâu thuẫn giữa các lần đo; sửa rộng đầu = đụng toàn bộ đầu, vượt phạm vi "chỉ nét mặt". Cần ảnh chính diện phân giải cao hơn mới quyết được |
| A2 | Mắt: khoảng cách 2 tâm / head_w | 0,441 | 0,437 | −1% | GIỮ |
| A3 | Mắt: rộng / head_w | 0,324 (bbox gồm bóng mí+mày) | eye 0,219 / lid 0,235 | — | GIỮ — bbox ảnh phóng đại, không đủ căn cứ đổi rộng mắt |
| A4 | **Cụm mắt: DẠNG** — ảnh: 1 đường mí cong liền khối/trên mắt; model: **3 ống xếp chồng** (mày + mí + mắt), từng ống nổi +0,064…+0,090 m → render thành 3 ống trắng song song. Tổng bề cao cụm: ảnh ≈ 0,142 head_h, model 0,149 head_h (khớp!) — lệch ở độ nổi từng ống, không ở kích thước cụm | 1 relief | 3 ống nổi | KHÁC DẠNG | **SỬA: ép dẹt cả 3 lớp về độ nổi đích ≤ +0,020 head_h (op A-a)** để cụm đọc liền thành một dải mí như ảnh |
| A5 | **Mũi: rộng / head_w** | 0,272 | 0,154 | **−43%** | **SỬA: nới rộng ngang (op A-b)** — hệ số cần 1,77 vượt trần an toàn 1,60 cho một lần nắn ma trận → kế hoạch 2 bước: nắn ×1,60 → render → đo lại → nắn tiếp phần còn lại nếu render xác nhận |
| A6 | Mũi: rộng/cao | 0,92 | 0,35 | −62% | Hệ quả A5; đích sau 2 bước ≈ 0,85–0,92 |
| A7 | Mũi: đáy mũi từ đỉnh đầu / head_h | 0,726 | 0,726 | 0% | GIỮ vị trí dọc — chỉ nới ngang |
| A8 | Miệng: rộng/mũi | 1,35 | 1,30 | −4% | GIỮ rộng miệng (tỉ lệ tương đối khớp; số tuyệt đối lệch vì A5) |
| A9 | **Miệng: DẠNG** — ảnh: môi cong nhẹ, sát mặt; model: thanh ống thẳng (Y 0,046 × Z 0,046 m) nổi +0,034 m → render như một gạch trắng ngang | môi cong sát | thanh ống | KHÁC DẠNG | **SỬA: ép dẹt + hạ chìm (op A-a)**; độ cong môi thật cần sculpt — ngoài phạm vi nháp (mục 6) |
| A10 | Miệng: tâm dọc / head_h | 0,802 | 0,753 | −6% | GIỮ — trong nhiễu (ảnh chụp từ dưới) |
| A11 | Urna: nổi +0,058 m, Ø 0,045 m | chấm nhỏ sát trán | khối nhỏ nổi | nhẹ | Ép dẹt cùng op A-a cho đồng nhất; không xóa (urna là dấu hiệu đúng của tượng) |

**Chốt A Di Đà:** vị trí/kích thước cụm mắt và miệng khớp ảnh; lệch thật =
mũi hẹp −43% + toàn bộ nét mặt là ống/thanh nổi thay vì relief liền khối.

---

## 4. Thao tác dự kiến (chỉ ma trận object — như V13; hệ số tính từ số đo, ghi trong script)

| Op | Mảnh | Phép biến đổi | Số đích |
|---|---|---|---|
| D-a | Di Lặc: browL/R, eyeL/R, creaseL/R | Scale trục sâu quanh pivot tại mặt sau mảnh (`k_face` suy từ độ nổi đo được) + tịnh tiến chìm (`sink`) dọc −facing | Độ nổi sau ≤ **+0,020 head_h** (≈ +0,037 m); `k_face` bị chặn dưới 0,35 |
| D-b | Di Lặc: nose | Scale ngang (trục side) `k = 0,250 / 0,170 ≈ 1,47` (script tự tính từ số đo thực trong scene) | Rộng mũi/head_w = **0,250 ± 0,01** |
| D-c | Di Lặc: cheekL/R | Scale trục sâu **×0,60** quanh pivot mặt sau, không sink, không đổi ngang/dọc | Mặt trước má lùi ≈ 0,10 m; vẫn nhô hơn mặt sọ tại má ≈ +0,10 m (má thật vẫn phình) |
| D-d | Di Lặc: mouth + smile | **CỔNG (V14.1, mặc định TẮT trong script):** tịnh tiến dọc theo delta đo lại từ render cùng góc ref5 | Chỉ khi lệch dọc > 7% sau kiểm chứng góc khớp |
| A-a | A Di Đà: browL/R, lidL/R, eyeL/R, mouth, urna | Như D-a | Độ nổi sau ≤ **+0,020 head_h** (≈ +0,025 m) |
| A-b | A Di Đà: nose | Scale ngang bước 1 `k = min(1,77; trần 1,60)` | Sau bước 1: rộng/head_w ≈ 0,246; bước 2 (nếu render duyệt): về **0,272 ± 0,01** |
| PROP | 2 tượng hốc cổng (A Di Đà) | Truyền mọi A của A Di Đà qua liên hợp `A' = Mc·A·Mc⁻¹` (Mc từ Head_ushnisha, như V13) | Mc sau ≤ 0,002; tai cổng giữ nguyên của V13 |

**Rủi ro chính & cách chặn:**
- Ép dẹt ống cong quanh trục thế giới có thể làm đầu ống hở khỏi mặt cong
  → pivot đặt ở mặt sau mảnh + sink tính từ độ nổi; verify bằng render
  cận mặt 2 góc (thẳng + 3/4) trước khi coi là đạt.
- Nới ngang mũi làm mũi bè chạm vào mắt/má → assert khoảng hở bbox sau
  biến đổi trong verify; A-b có trần 1,60 + kế hoạch 2 bước vì lý do này.
- Ép dẹt má quá tay làm mặt bẹt mất má phình Di Lặc → D-c chỉ ×0,60 và
  cấm sink; đích còn nhô ≈ +0,10 m.
- Mọi op đều có `predict_box` trong DRY_RUN: chạy khô trước, đối chiếu
  tỉ lệ dự đoán với bảng đo rồi mới cho áp thật.

---

## 5. Quy trình thi công + kiểm chứng (khi vòng thi công được mở)

0. Viết `measure_v14.py` (theo mẫu inspect_v13.py, mở `layout_v15_v13.blend`):
   in lại toàn bộ số mục 2–3 ngay trong scene + hướng facing từng tượng.
   Lệch parser GLB > 2% ở bất kỳ chỉ số nào → DỪNG, báo coordinator.
1. `build_v14.py` chạy **DRY_RUN** (mặc định): soát hệ số từng op in ra
   so với mục 4. Hệ số ngoài khoảng dự kiến → DỪNG.
2. Tắt DRY_RUN, chạy build → `layout_v16_v14.blend` + `v14_audit.json`.
   Script tự assert: tai không đổi (< 1e-6), mọi mảnh ngoài danh sách mặt
   không đổi, Mc 2 cổng ≤ 0,002 sau truyền.
3. Viết `verify_v14.py` độc lập (theo mẫu verify_v13.py): đo lại toàn bộ
   chỉ số mục 2–3 trên file đã lưu (kể cả độ nổi bằng ellipsoid như
   script đo GLB) + checksum mesh toàn scene phải rỗng + số object không đổi.
4. Render (chỉ khi có khe CPU — driver tự chờ như `render_v13_driver.sh`):
   Cycles CPU, camera mặt thẳng + 3/4 cho 2 tượng (cùng cách đặt camera
   của render V13) + render Di Lặc cùng góc ref5 cho cổng D-d + flycam
   đối chứng toàn cảnh. Pixel-diff V15↔V16 phải khoanh đúng vùng mặt 2
   tượng chính + 2 hốc cổng, ngoài vùng đó ≈ 0.
5. Coordinator soi render cạnh ref5/ref11/ref3 và chấm từng mục
   ĐẠT / CHƯA ĐẠT. Chưa đạt ở op nào thì lặp lại op đó với hệ số hiệu
   chỉnh từ số đo mới — không nắn tay tự do.

---

## 6. Ngoài phạm vi bản nháp này (ghi nợ rõ ràng, không tự làm)

- **Hòa khối má–mặt / biến nếp cười thành rãnh âm / tạo cong môi thật /
  cánh mũi cho A Di Đà:** cần sculpt cấp mesh hoặc boolean — thay đổi
  hình học gốc của tượng, rủi ro cao với luật trang nghiêm. Chỉ làm khi
  có quyết định riêng sau khi thấy kết quả bản ma trận (V14).
- **Rộng đầu A Di Đà (A1):** nợ đo — cần ảnh chính diện rõ hơn.
- **Mắt Di Lặc trong render trông như "gốc ống cụt":** một phần do ống
  mắt cong bị camera từ dưới rút ngắn; sau op D-a phải chấm lại bằng
  render 2 góc trước khi kết luận thêm.

---

## 7. Trạng thái bàn giao của giai đoạn đo + kế hoạch (10/11/2026)

- Bảng đo: mục 2–3 của file này + bản máy đọc được
  `v14_measure/v14_face_measure.json`; script đo `v14_measure/glb_face_measure.py`
  (chạy lại được, không cần Blender); crop đo giữ trong `v14_measure/`.
- Script nháp `layout/build_v14.py` (375 dòng): đã qua `py_compile` —
  syntax OK; cấu trúc theo build_v13 (matching nhom, head_bbox loai co+tai,
  snapshot/assert tai + ngoai pham vi, truyen lien hop Mc cho 2 cong,
  cleanup import tam, audit JSON). `DRY_RUN = True` mac dinh.
- **Chua chay DRY_RUN trong Blender**: tai thoi diem ban giao, 2 tien
  trinh ffmpeg dang chay + load ~15 (tuyen video uu tien) — theo luat
  CPU chi chay Blender khi ffmpeg=0. Nguoi thi cong chay DRY_RUN truoc
  tien (buoc 0/1 muc 5) va doi chieu he so tinh duoc voi bang du doan:
  mui Di Lac k~1.47, mui A Di Da bi chan 1.60 (ke hoach 2 buoc),
  cac op ep det k nam trong [0.35, 1.0). Lech lon hon phai dung lai bao cao.
- Khong tao file TEST o giai doan nay (khong chay Blender); file
  layout_v16_v14_TEST.blend chi xuat hien khi thi cong chay DRY_RUN/
  build thu theo muc 5. layout_v15_v13.blend nguyen ven, khong ghi de.