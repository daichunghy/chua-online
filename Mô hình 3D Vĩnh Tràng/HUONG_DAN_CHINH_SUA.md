# HƯỚNG DẪN CHỈNH SỬA — Chùa Online (dành cho Antigravity / người sửa trên repo)

Repo: `daichunghy/chua-online`. Thư mục này (`Mô hình 3D Vĩnh Tràng/`) là bản web
trải nghiệm + model layout chùa Vĩnh Tràng (Mỹ Tho).
Ngày viết: 09/11/2026. Trạng thái lúc viết: web v7 đạt **46/46 verify + 0 lỗi JS**;
layout V13 nắn tai xong, **chưa render nghiệm thu** (driver đang chờ khe CPU).

## 1. Bản đồ file

- `trai-nghiem-vinh-trang-v7.html` — file phát hành (mở double-click được).
  **KHÔNG sửa trực tiếp**: sửa trong `v7_parts/` rồi chạy `assemble_v7.py` để dựng lại.
- `v7_parts/assemble_v7.py` — lắp HTML từ `head_css.html` + `modal_*.html` +
  `module_1..7.js` (module 6 tách `6a`/`6b`) + `v2.js` + `v3.js`; nhúng base64 3 GLB;
  đồng thời xuất bản `*-TESTLOCAL.html` (importmap → `vendor/three.module.js` local
  + hook `__v6ff` tua nhanh để verify). `modal_lamp.html` + `modal_arhat.html`
  KHÔNG được include (như v5/v6).
- `v7_parts/verify_v7.mjs` — bộ verify v7 (46 check). Chạy sau MỌI sửa web;
  chuẩn đạt: **46/46 + 0 lỗi JS**. Log chuẩn: `verify_v7_run2_46pass.log`.
- **3 GLB chuẩn** (nhân vật Phật tử rigged, có chuyển động — xem §3.2):
  `~/workspace/user/files/nu-phuc-hoi-mau-chuyen-dong.glb`,
  `nam-chuyen-dong.glb`, `tre-em-chuyen-dong.glb`
  (~12,8 MB → base64 ~17 MB nhúng trong HTML). `assemble_v7.py` dừng nếu thiếu file.
- `audio_v5/` — giọng dẫn thu sẵn, đặt cùng cấp với file HTML khi phát hành;
  code nạp theo đường dẫn tương đối `audio_v5/<key>.mp3`
  (`module_1.js` → `playVoice`). Bản làm việc: `~/workspace/chua-online-work/audio_v5/`
  (14 file mp3: s0/s1/s2/s3/s4/s5/s6/s7, `day_di`, `niem_phat_xa`, `merit_box`…).
- **Layout Blender** — `~/workspace/chua-online-work/layout/`:
  `build_v*.py` (script dựng từng vòng), `NOTES.md` (nhật ký từng vòng V10–V13 +
  verdict từng tượng), `scripts/render_v13.py`, `pixeldiff_v13.py`,
  `verify_v13.py`, `render_v13_driver.sh` (chờ khe CPU rồi render).
  File layout mới nhất: `~/workspace/chua-online-work/layout_v15_v13.blend`
  (97.698.093 byte; V14: 97.679.559 byte).
- **Tượng Phật** — `~/workspace/chua-online-work/statues/`:
  `verified_v2/NOTES.md` (4 tượng: A Di Đà đứng ~11,1 m — ref3;
  Di Lặc ~7,9 m — ref5; Phật nằm; 2 tượng hốc cổng).
  Dựng tay bằng Blender 5.0.1, Cycles CPU 32 samples, 900×900.
  Mọi tượng quay mặt về **+Y**, đơn vị = mét, gốc tọa độ tại tâm chân bệ.
- **Theme** — `~/workspace/chua-online-work/THEME_CHUA_ONLINE.md`
  (khóa 07/11 theo ảnh mẫu Chung Hy gửi).

## 2. Cách dựng lại file phát hành

1. Sửa file trong `v7_parts/` (không sửa trực tiếp file HTML phát hành).
2. Chạy: `python3 "Mô hình 3D Vĩnh Tràng/v7_parts/assemble_v7.py"`
   (cần đủ 3 file GLB ở `~/workspace/user/files/` — thiếu là script dừng).
3. Mở bản TESTLOCAL, chạy `verify_v7.mjs` — phải **46/46 + 0 lỗi JS** mới đẩy.
4. Đẩy file **text** lên repo bằng `github push-files` từ staging
   `~/workspace/chua-online-push/`. File **nhị phân** (PNG/JPG/GLB) CHỈ đẩy bằng
   giao diện web GitHub (Add file → Upload files): MCP `push_files` lưu chuỗi
   UTF-8 nên file nhị phân sẽ hỏng (bài học 06/11: 13 render JPG hỏng kiểu này).
5. Sau khi đẩy, **đọc lại bytes thật trên repo (magic bytes)** mới tính là đã lên.

## 3. LUẬT CỨNG (không được phá)

1. **Tượng Phật chỉ nắn VỀ PHÍA ẢNH THẬT, cấm stylize/cách điệu thêm.**
   Mắt/mũi/miệng giữ tối giản theo bản gốc; tai nắn theo số đo từ ref
   (ref3 = A Di Đà, ref5 = Di Lặc). Mọi lần nắn phải có số đo + ảnh render
   đặt cạnh ref; không nắn bằng cảm giác.
2. **Nhân vật web phải là 3 GLB chuẩn** (nữ / nam / trẻ em, rigged, có chuyển động)
   — cấm nhân vật khối tự chế (v7 đã thay toàn bộ khối tự chế bằng 3 GLB này).
3. **Theme sáng**: nền `#FFF6E5` / `#FDF3DC`, xanh đậm `#1C5A34` / `#14532D`,
   vàng đồng `#C9962E`, chữ nâu `#4A3222` / `#6B4226`, hồng sen `#F2A0C4`.
   Cấm theme tối đỏ/nâu kiểu game (v3 cũ đã bị loại vì sai theme hoàn toàn).
4. **Trang nghiêm**: KHÔNG điểm công đức, KHÔNG EXP, không cơ chế game hóa việc
   lễ Phật. Chuông mõ / chắp tay chỉ là tương tác tĩnh lặng.
5. **Giọng dẫn chỉ dùng bản ghi thật đã thu** (`audio_v5/*.mp3`) — thiếu file thì
   im lặng, cấm thay bằng TTS/tổng hợp (xem `playVoice` + `__setHallChant`
   trong `module_1.js`; khe niệm Phật chánh điện chỉ phát khi có
   `audio_v5/niem_phat_xa.mp3` thật).
6. **Luật CPU của dự án**: render Blender chỉ chạy khi máy rỗi
   (ffmpeg = 0, không Blender lạ, load < 7, MemAvailable ≥ 2200 MB) —
   xem `layout/render_v13_driver.sh`. Không ép render khi máy đang tải nặng.

## 4. Nợ kỹ thuật đã biết (chưa sửa — đừng tưởng là xong)

- **Camera xuyên cột đỏ trong chánh điện**: chưa có va chạm camera trong điện
  (vòng V7.1 đang làm: thêm va chạm để camera không xuyên cột).
- **3 key giọng đã thu nhưng CHƯA được gọi ở đâu**:
  `s7_tam_biet` (trạm ra về), `s3_giang_duong` (giảng đường Huệ Đăng), `day_di`.
  File mp3 có trong `audio_v5/`, chưa có `playVoice('...')` nào gọi chúng trong
  `v7_parts/` (các key đang được gọi: s0_nhan_nhang, s2_thap_nhang,
  s3_bo_dep, s3_lay_phat, s6_hoi_huong, merit_box). V7.1 nối 3 key này vào
  đúng điểm hành trình, qua `sayAn(text, voiceKey)` ở `module_6b.js`.
- **A Di Đà bản web nhỏ hơn tượng thật** (thật cao ~11,1 m) — tỉ lệ web chưa
  khớp thật, cần đo lại khi chỉnh layout.
- **V13 chưa render nghiệm thu**: tai Di Lặc đã nắn khớp ảnh
  (0,664 / 0,321 / +0,015, cả 3 số khớp mục tiêu trong ±0,01),
  tai A Di Đà khớp (0,507 / 0,632 / −0,139), 2 tượng hốc cổng đã truyền tai
  khớp 0,5070 (Mc 0,000004); Phật nằm KHÔNG nắn (lệch trong sai số đo).
  Driver render (`layout/render_v13_driver.sh`) đang chờ khe CPU — xem
  `layout/render_v13_driver.log`; render xong mới soi cận mặt đối chiếu
  ref5/ref3 + chạy `pixeldiff_v13.py` rồi chốt V13.

## 5. Quy trình một vòng cải thiện (chuẩn các vòng trước)

1. Đo từ ảnh thật → sửa bằng **script build** (không sửa tay trong Blender rồi quên ghi).
2. Verify bằng script (`verify_v7.mjs` cho web, `verify_v13.py` cho layout).
3. Render đối chiếu ref (cận mặt + toàn cảnh), ghi verdict bằng số đo.
4. Ghi `NOTES.md`: số đo + verdict + tên file + script đã dùng.
5. Đẩy text qua `push-files`, nhị phân qua web UI, rồi **đọc lại kiểm chứng**.
6. Log + script chẩn đoán ghi vào `workspace/layout/`, **KHÔNG để /tmp**
   (VM restart xóa /tmp — đã mất toàn bộ `/tmp/v13` ngày 09/11).
