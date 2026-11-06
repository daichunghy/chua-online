# Bốn tượng Phật trang nghiêm — Chùa Vĩnh Tràng (dựng tay bằng Blender, không Hunyuan/GPU)

Ngày dựng: 2026-11-05. Công cụ: Blender 5.0.1, Cycles CPU 32 samples, 900×900.
Kỹ thuật: loft theo vòng tiết diện elip (thân/áo), loft dọc đường cong (tay, thân Phật nằm),
ống cong (nếp áo, nét mặt), cánh sen instance theo vòng (đài sen), đầu tạo hình từ cầu biến dạng
(ushnisha, tai dài, vành cổ). Mọi tượng quay mặt về **+Y**, đơn vị = mét, gốc tọa độ tại tâm chân bệ.

Nguyên tắc đối chiếu: mỗi tượng render xong đều đặt cạnh ảnh thật (refs/) soi lại, sửa tối đa 3 vòng.

---

## 1. Phật đứng A Di Đà — `phat-dung-adida.blend / .glb / .png`
- **Ảnh mẫu:** ref3.jpg, ref11_adida.jpg.
- **Kích thước:** tổng cao ≈ **11,1 m** — bệ đỏ nâu 4,8×3,8×1,3 m + phiến đá 0,18 m;
  đài sen xanh cao 1,5 m (Ø tối đa ≈ 4,1 m, 3 tầng cánh: 14/12/10 cánh, 2 tông xanh lam);
  tượng cao ≈ 8,05 m.
- **Tư thế/thủ ấn:** đứng thẳng; tay trái (+X) nâng trước ngực, **ấn vitarka** (vòng ngón cái–trỏ + 3 ngón duỗi);
  tay phải buông dọc thân, bàn tay dài cầm mép áo. Áo cà sa có **5 nếp sóng lượn (scallop)** xếp tầng trước thân
  + 1 mép áo chéo vai trái→hông phải — đúng đặc điểm dễ nhận nhất trong ảnh thật.
  Đầu: ushnisha, tóc búi, tai dài tới hàm, 2 vành cổ, mắt khép, bạch hào (urna).
- **Bệ:** bảng vàng chữ "NAM MÔ A DI ĐÀ PHẬT" (texture vẽ bằng PIL — chữ phỏng theo lệ thường, ảnh thật chụp xa không đọc rõ từng chữ).
- **Verdict: ĐẠT.** Nhìn là nhận ra đúng tượng A Di Đà Vĩnh Tràng: trắng, đài sen xanh, tay ấn vitarka, nếp áo sóng.
  Hạn chế còn lại: cánh sen ở silhouette hơi nhọn; nét mặt tối giản (đúng tính chất tượng đá khổ lớn xem từ xa).

## 2. Di Lặc — `di-lac.blend / .glb / .png`
- **Ảnh mẫu:** ref5_maitreya.jpg.
- **Kích thước:** tổng cao ≈ **7,9 m** (≈ 2/3 tượng đứng) — bệ đá đen 10,6×6,6×1,7 m + phiến 0,14 m;
  tượng ngồi cao ≈ 6,05 m, rộng chân ≈ 8,6 m.
- **Tư thế:** ngồi xếp chân rộng trên bệ, **bụng phệ lộ**, áo mở hai bên ngực (2 mép áo cong ôm bụng);
  vòng **tràng hạt lớn** quanh cổ buông tới bụng (46 hạt + hạt chủ); tay phải (+X) đặt trên gối cầm
  **xâu hạt rủ** (12 hạt); tay trái đặt trên gối trái. Đầu hói tròn, má phệ, mắt cười khép,
  miệng cười hở (khoang miệng tối), tai dài.
- **Bệ:** mặt trước chữ Hán vàng "南無彌勒尊佛" (texture PIL/Noto Serif CJK — đọc phỏng theo ảnh, ảnh thật không đủ nét để chép chính xác từng chữ).
- **Verdict: ĐẠT.** Nhận ra ngay Di Lặc: cười, bụng lớn, tràng hạt, ngồi trên bệ chữ vàng.
  Hạn chế: tay còn hơi "ống" và thân là một khối mượt — độ chi tiết cơ bắp/nếp vải chưa bằng tượng thật; ở tỉ lệ sân chùa (xem từ 10 m+) thì đọc tốt.

## 3. Phật nằm — `phat-nam.blend / .glb / .png`
- **Ảnh mẫu:** ref7_reclining.jpg.
- **Kích thước:** bệ đá đen 17,6×5,4×2,4 m + phiến 0,16 m; thân dài ≈ **15,5 m** (x −6,9 → 8,55, cộng đầu tới ≈ −8,6),
  cao tối đa ≈ 5,3 m tính từ mặt đất (thân nằm trên gối xanh, đỉnh vai ≈ 5,33 m so với nền).
- **Tư thế:** nằm nghiêng phải (niết-bàn), đầu tựa lên **tay phải chống** (cẳng tay dựng, bàn tay dưới má),
  mặt hướng ra trước hơi ngước; tay trái buông dọc theo thân; hai bàn chân khép ở cuối thân.
  Gối nằm xanh lục nhạt có gờ cuộn tròn phía trước (đúng chi tiết mép gối lượn trong ảnh).
  3 nếp áo cong dài chạy dọc thân.
- **Bệ:** chữ vàng đúng nguyên văn ảnh thật: **"NAM MÔ BỔN SƯ THÍCH CA MÂU NI PHẬT"** (texture PIL, DejaVu Bold).
- **Verdict: ĐẠT.** Đọc đúng Phật nằm Vĩnh Tràng: thân dài trắng, đầu tựa tay ở đầu bệ, bệ chữ vàng.
  Hạn chế: đầu hơi nhỏ và áp sát vai hơn ảnh thật (trong ảnh đầu lớn và nhô cao rõ hơn); nếp áo còn ít.

## 4. Phật ngồi bàn thờ (chánh điện) — `phat-ngoi-ban-tho.blend / .glb / .png`
- **Ảnh mẫu:** KHÔNG có ảnh nội điện thật — dựng theo quy ước tượng thờ chánh điện Vĩnh Tràng
  và tông vàng nâu của render bàn thờ hiện có trong repo.
- **Kích thước:** tổng cao **2,86 m** (đo bbox thực tế, tính cả đỉnh vòng hào quang) — đài sen vàng cao 0,42 m (Ø ≈ 1,76 m, 2 tầng cánh);
  tượng ngồi ≈ 2,0 m; hào quang: đĩa Ø 0,88 m + vòng Ø 1,0 m sau đầu.
  Lưu ý đặt tượng: chân đài sen chìm 0,04 m dưới mặt z=0 (mép dưới cánh sen) — khi đặt lên bàn thờ nâng +0,05 m.
- **Tư thế/thủ ấn:** ngồi kiết già trên đài sen, **ấn thiền (dhyana)** — hai bàn tay xếp chồng trong lòng, đầu ngón cái chạm nhau;
  mắt khép, ushnisha + tóc vàng sẫm, tai dài; vật liệu vàng đồng (metallic 0.85, roughness 0.35).
- **Verdict: ĐẠT ở khoảng cách bàn thờ.** Trang nghiêm, đúng quy ước tượng thờ; thay thế hẳn "khối cầu" vô hồn trong model cũ.
  Hạn chế thành thật: nét mặt tối giản (đã bỏ vòng cung lông mày vì ở cự ly gần trông hoạt hình);
  nếu sau này có ảnh nội điện thật cần đối chiếu lại màu vàng và kiểu hào quang.

---

## Vòng 2 — cải tiến theo lệnh xuyên đêm 06/11 (chưa render kiểm chứng đầy đủ)

Theo điều phối 02:12 (CPU ưu tiên cho video Na Tra + Hoa Mộc Lan tới 06:12), vòng 2 chỉ sửa hình học +
kiểm tra nhẹ (preview Cycles 6 mẫu 480px + đo bbox), **chưa** chạy render kiểm chứng 32 mẫu.
Bộ file đã kiểm chứng đầy đủ ở vòng 1 được giữ nguyên tại `verified_v1/` (push-ready).
Khi CPU rảnh: chạy lại 4 script `build_*.py` (đã chứa sẵn sửa đổi vòng 2) để lấy render 900×900/32 mẫu,
soi lại với ảnh thật rồi mới thay verdict.

Sửa đổi vòng 2:
- **A Di Đà:** bàn tay trái trước đây đặt theo tọa độ cứng, lệch cổ tay ~4 cm (lơ lửng) — nay suy ra từ
  điểm cuối + hướng của loft cẳng tay, palm áp đúng cổ tay, vòng vitarka và ngón bám theo palm.
  Cánh sen nới rộng tiết diện (0,185→0,21) cho bớt nhọn. Bbox sau sửa: 5,20×4,20×11,03 ✓.
- **Di Lặc:** tay thon lại (bán kính ×0,85), thêm nếp gấp khuỷu + cổ tay 2 bên. Bbox: 11,20×7,20×7,89 ✓.
  Đã kiểm tra riêng: chữ Hán trên bệ giữ nguyên hướng như bản vòng 1 (cắt phóng to đối chiếu 2 bản — trùng khớp).
- **Phật nằm:** đầu to lên (h 1,55→1,85) và nâng cao/thoát ra khỏi khối vai (tâm đầu −7,70/4,22),
  tay chống + bàn tay đỡ dời theo má. Preview cho thấy đầu nổi rõ trên đường thân — đúng điểm yếu vòng 1.
  Bbox: 18,22×6,00×5,33 ✓ (đầu tới sát mép bệ như ảnh thật).
- **Bàn thờ:** cẳng tay thêm điểm cong trung gian, không còn gập chữ V cứng khi về lòng. Bbox: 2,16×2,20×2,86 ✓.

## Vòng 2 — KẾT QUẢ KIỂM CHỨNG ĐẦY ĐỦ (06/11, sau khi gỡ giới hạn CPU)

Render Cycles 32 mẫu 900×900 cho cả 4 tượng (chạy tuần tự, 1 Blender/lần), soi cạnh ảnh thật
ref3/ref11 (A Di Đà), ref5 (Di Lặc), ref7 (Phật nằm). Bộ đã kiểm chứng nằm tại `verified_v2/`
(.glb + .png + NOTES này) và đã đẩy GitHub `Mô hình 3D Vĩnh Tràng/Tượng/`.

### Khuyết điểm vòng 1 phát hiện thêm (kiểm tra độc lập) và cách sửa
1. **Chữ trên bệ bị GƯƠNG (mirror) ở cả 3 tượng có bảng chữ** — không chỉ A Di Đà.
   Nguyên nhân gốc: file texture PNG trong `tex/` bản thân đã bị lật ngang (kiểm chứng: vẽ lại
   bằng cùng `make_tex.py` cho ra chữ đúng; file cũ trên đĩa đọc ngược), và mặt phẳng bảng
   dùng rotation (-90°, 0, 180°) khiến mặt trước quay ra sau. Sửa cả hai lớp:
   - Chạy lại `make_tex.py` → cả 3 PNG đọc đúng chiều (đã soi file PNG trực tiếp).
   - Thêm `plaque_plane()` trong `lib_statues.py`: đặt mặt bảng bằng ma trận cơ sở tường minh
     (local +X → world −X = phải màn hình khi nhìn từ +Y; local +Y → +Z; normal → +Y),
     thay cho rotation Euler mơ hồ. Cả 3 script dựng bảng chữ chuyển sang dùng hàm này.
   - Kiểm chứng: cắt phóng to vùng bảng chữ từ render 900×900 cả 3 tượng — đều đọc đúng:
     "NAM MÔ A DI ĐÀ PHẬT" / "南無彌勒尊佛" / "NAM MÔ BỔN SƯ THÍCH CA MÂU NI PHẬT".
2. **Mặt quá trơn/không đọc được nét** (A Di Đà + Di Lặc): ống nét mặt dùng cùng vật liệu trắng
   với da nên chỉ đọc bằng bóng đổ, ở cự ly sân chùa biến mất. Sửa trong `lib_statues.py`:
   - Thêm vật liệu `FeatureShadow` (0.78, 0.76, 0.71) cho mọi ống nét (mắt, mày, miệng, nếp cười,
     nếp mũi-má) ở cả `head_serene` và `head_maitreya`; thêm nếp mí trên cho đầu serene;
     vòng ushnisha thêm nhẫn mỏng ở chân; khoang miệng cười Di Lặc to lên (0.185h→0.21h),
     ống cười dày hơn. Đầu bàn thờ dùng GDARK làm feature tone (vàng sẫm trên nền vàng).

### Verdict vòng 2 (thành thật, từng tượng)
- **A Di Đà — ĐẠT.** Bảng chữ đọc đúng (đã soi phóng to). Tay trái ấn vitarka áp đúng cổ tay,
  không còn lơ lửng. Mặt: mày/mắt khép/miệng đã đọc được ở cự ly render — vẫn tối giản
  (không có tóc xoắn ốc như tượng thật, nét mũi chỉ gợi), nhưng đúng tính chất tượng đá 11 m
  xem từ sân chùa. Nếp áo sóng + đài sen xanh + bệ đỏ nâu khớp ref11.
- **Di Lặc — ĐẠT, cải thiện rõ nhất.** Cười ĐÃ ĐỌC ĐƯỢC: khoang miệng tối + nếp cười + mắt cười
  khép nhìn là nhận ra Di Lặc đang cười, không còn "đầu vòm trơn" như vòng 1. Tay thon + nếp
  khuỷu/cổ tay phá được cảm giác "ống". Chữ Hán trên bệ đọc đúng chiều. Hạn chế còn lại:
  tay phải cầm xâu hạt đặt trên gối (ảnh thật xâu hạt vắt cao hơn qua vai); thân vẫn là khối
  mượt, nếp vải ít — chấp nhận được ở tỉ lệ sân chùa.
- **Phật nằm — ĐẠT.** Đầu to + nhô cao khỏi vai đúng điểm yếu vòng 1; mặt nghiêng đọc được
  (mắt khép, miệng). Chữ vàng trên bệ đọc đúng, đủ nguyên văn ref7. Hạn chế: nếp áo dọc thân
  vẫn ít (3 đường) so với tượng thật; mặt ở khung toàn thân còn nhỏ — ở cự ly sân chùa vẫn
  nhận ra đúng Phật nằm.
- **Bàn thờ — ĐẠT ở khoảng cách bàn thờ.** Mặt đọc rõ nhất trong 4 tượng: mắt khép, mí, mũi,
  miệng đều hiện trên nền vàng (feature tone vàng sẫm). Ấn thiền, hào quang, đài sen vàng giữ
  nguyên. Hạn chế: tay vẫn hơi "ống" ở hai bên thân; không có ảnh nội điện thật để đối chiếu
  màu vàng và kiểu hào quang — vẫn là điểm nợ như vòng 1.

## Ghi chú tích hợp vào bố cục
- Cả 4 file .glb export với apply modifiers + Y-up; khi đưa vào scene tổng thể chỉ cần scale/rotate —
  không cần sửa hình. Mặt trước tượng = +Y (cổng/hồ trong bố cục đang ở phía −Y, nhớ xoay 180° khi đặt).
- Texture chữ trên bệ nằm trong thư mục `tex/` (đã nhúng vào .glb; .blend trỏ tới file trong `tex/` —
  giữ nguyên cấu trúc thư mục khi di chuyển).
- File script dựng lại: `build_adida.py`, `build_dilac.py`, `build_phatnam.py`, `build_bantho.py`,
  thư viện chung `lib_statues.py`, sinh texture `make_tex.py` — sửa thông số trong script rồi chạy lại là ra bản mới.
- GitHub: Chung Hy đã duyệt trước (pre-approved 02:04) cho bản nào qua kiểm chứng render-vs-ảnh thật.
  Hiện trạng: bộ vòng 1 đã kiểm chứng nằm ở `verified_v1/` — sẵn sàng đẩy. Bộ vòng 2 (file ở thư mục gốc)
  mới kiểm tra nhẹ, chờ render đầy đủ sau 06:12 mới đẩy, tránh ghi đè bản đã kiểm chứng bằng bản chưa soi kỹ.
