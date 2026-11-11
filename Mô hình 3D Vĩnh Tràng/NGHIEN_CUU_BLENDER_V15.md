# NGHIÊN CỨU BLENDER V15 — kỹ thuật trên mạng đối chiếu nợ của Chùa Vĩnh Tràng 3D

*Viết 11/11/2026 (tuyến nghiên cứu). Chỉ nghiên cứu — chưa thi công.*
*Bối cảnh: cảnh `layout_v17_v141.blend`, Blender 5.0.1, Cycles CPU, VM 8 GB RAM
(máy còn chia sẻ với các tuyến khác — cửa sổ chạy nặng thực tế cần
MemAvailable ≥ ~1.800 MB như các vòng V13–V14.1). Giống thật bố cục ~73%.*

## 0. Tóm tắt điều hành — 5 kết luận lớn

1. **Muốn sculpt mặt liền khối thì BẮT BUỘC hợp nhất các mảnh đầu thành MỘT
   lưới kín nước trước.** Tượng hiện tại là tập hợp mảnh nguyên khối rời
   (Di Lặc 94 mảnh, mặt gồm các mảnh Head_nose/brow/eye/crease/cheek/mouth
   riêng). Join thường (Ctrl+J) KHÔNG hàn mặt; đường chuẩn là Boolean Union
   (solver Exact) hoặc Voxel Remesh. Cả hai đều **làm lệch bề mặt so với số đo
   đã khóa** → vòng sculpt phải có bước "đo lại sau hợp nhất + nắn khối lớn về
   đúng bảng số V13/V14" trước khi chạm chi tiết. Đây là khác biệt cốt lõi so
   với V13–V14.1 (vốn chỉ biến đổi ma trận object, mesh checksum giữ nguyên).
2. **Photogrammetry từ 14 ảnh refs hiện có: KHÔNG khả thi** (cần tối thiểu
   ~30 ảnh vòng quanh, chồng lấp 60–80%; Meshroom bản đầy đủ cần GPU NVIDIA
   CUDA — VM không có). Ảnh refs chỉ dùng làm mốc đo + đối chiếu, như hiện tại.
3. **FaceBuilder/KeenFace (dựng đầu người từ ảnh): không dùng làm đường
   chính.** Công cụ này thay đầu bằng topology đầu NGƯỜI mẫu của hãng, không
   nhận mesh tự có làm base; tượng Phật (tai dài 0,664 chiều cao đầu, ushnisha,
   mắt khép) nằm ngoài mẫu người → rủi ro cao với luật tượng. Chỉ đáng thử
   nghiệm đối chứng nếu cần, và sản phẩm thử vẫn phải qua cùng bảng đo.
4. **Ba nợ phụ có kỹ thuật chuẩn, rẻ và an toàn:** tượng hốc cổng tối →
   **Light Linking** (Blender có sẵn từ 4.0, tài liệu 5.1 xác nhận) cho đèn
   fill chỉ chiếu vào tượng; rêu mái vệt → **mặt nạ shader theo AO/pointiness/
   hướng mặt + noise** (rêu tự nằm trong rãnh, hết vệt quẹt) hoặc bake mặt nạ
   về texture để render bằng 0 chi phí thêm; tán dừa góc cạnh → **tàu dừa
   hình học (geometry) cho cây gần** — có số đo Cycles cho thấy lá hình học
   render NHANH hơn lá alpha ~20% trên CPU vì khỏi trả giá transparent bounce.
5. **Tỉ lệ sơ đồ toàn cảnh (Di Lặc 11,3 m vs thật ~20 m) không có kỹ thuật
   nào sửa rẻ:** phóng toàn cảnh phá mọi mốc camera/số đo đã khóa và tính
   tương đương với bản web. Khuyến nghị giữ nguyên như một quyết định đã ghi,
   không đưa vào V15.

**Luật tượng áp dụng cho toàn bộ hồ sơ này:** mọi kỹ thuật dưới đây chỉ được
dùng để tiến VỀ PHÍA tượng thật trong ảnh, có số đo trước–sau; không có mục
nào được "tự do sáng tạo" trên tượng. File pristine `layout_v17_v141.blend`
không bao giờ bị ghi đè; mọi thử nghiệm trên bản sao, như tiền lệ V12–V14.1.

---

## 1. Nợ 1 — MẶT TƯỢNG GHÉP MẢNH (nợ lớn nhất)

Hiện trạng (từ NOTES §V13–§V14.1): tỉ lệ đã khóa đúng ảnh — tai Di Lặc 0,664 /
A Di Đà 0,507 (chiều cao đầu cằm→đỉnh), mũi/head_w 0,2500 / 0,2720, độ nổi
mày/mắt/nếp cười/má đã ép về ≤ đích. Còn lại là chất lượng BỀ MẶT: mắt là ống/
vạch nổi, mũi khối oval rời, miệng thanh ngang, má cầu dán, chưa có sống mũi/
lỗ mũi/rãnh âm. V14 §"Nợ còn lại" đã tự ghi 5 mục thuộc sculpt: hòa khối
má–mặt, rãnh âm nếp cười, cong môi, cánh mũi, (riêng) rộng đầu A Di Đà là nợ ĐO.

### 1.1 Pipeline sculpt chuẩn của cộng đồng (áp dụng nguyên khung)

- **Nguồn:** https://github.com/roble3/cc-blender-skill/blob/HEAD/knowledge/03-sculpting-retopo/00-overview.md
  (hồ sơ pipeline sculpt+retopo, cập nhật 2026-04-27, đã mở đọc trực tiếp);
  https://www.strayspark.studio/blog/how-to-make-a-3d-character-in-blender-2026
- **Cách làm:** 5 giai đoạn chuẩn: (1) blockout khóa tỉ lệ → (2) voxel remesh
  tăng dần độ mịn (mỗi bước ≤1,5×) → (3) dyntopo cho chi tiết bề mặt →
  (4) retopology lưới quad sạch phủ lên (Shrinkwrap bám mặt) → (5) multires
  trên lưới retopo + bake normal map từ cao xuống thấp. Thứ tự luôn: khối lớn
  (Grab/Clay Strips) → khối phụ (sống mũi, môi) → chi tiết (Crease/Draw Sharp)
  → cuối cùng mới bề mặt mịn.
- **Áp vào nợ:** đây là khung quy trình cho §6 (đề xuất V15) — nhưng dự án
  mình KHÔNG bắt đầu từ blockout: điểm bắt đầu là lưới đã đúng tỉ lệ, nên giai
  đoạn 1–2 được thay bằng "hợp nhất + đo lại + nắn khối lớn về bảng số khóa".
- **Khả thi trên máy này:** có, với điều kiện sculpt trong FILE RIÊNG chỉ có
  đầu tượng (xem §5). Multires: mỗi level ×4 mặt; tài liệu cảnh báo level 5+
  trên base 10K mặt = 10M+ mặt, hiệu năng tụt mạnh; khuyến nghị base ≤5K,
  ≤4 level cho nhân vật game — mình render tĩnh, có thể lên level 5 ở bước
  render nhưng sculpt tương tác nên giữ ≤4.
- **Rủi ro luật tượng:** thấp nếu giữ kỷ luật đo (xem 1.4). Rủi ro thật nằm ở
  bàn tay sculpt tự do — hồ sơ này khóa bằng cổng số, không khóa bằng cảm tính.
- **Công sức:** là khung cho toàn bộ mục 1; chi tiết từng bước ở 1.2–1.5.

### 1.2 Hợp nhất mảnh → một lưới kín nước (bước cửa bắt buộc)

- **Nguồn:** https://copyprogramming.com/howto/how-to-join-multiple-objects
  (Join vs Boolean vs Merge — đã đối chiếu 2 bài cùng trang);
  https://docs.blender.org/manual/zh-hans/3.6/sculpt_paint/sculpting/introduction/adaptive.html
  (Blender Manual: voxel remesh "loại bỏ hình học chồng lấp và tạo thể tích
  manifold"); https://3d-agent.com/blender-ai/3d-printing (voxel remesh cho
  vỏ kín nước theo cấu trúc, đánh đổi: chi tiết nhỏ hơn voxel bị mất, UV bị bỏ).
- **Cách làm:**
  - *Join (Ctrl+J)*: chỉ gom vào một object, hình học vẫn rời và chồng lấp
    bên trong — KHÔNG sculpt liền khối được. Loại.
  - *Boolean Union (solver Exact của Blender 5)*: tính hợp thể tích thật, cho
    bề mặt ngoài liên tục, giữ chi tiết sắc nét tốt hơn voxel; chậm và dễ lỗi
    trên lưới nhiều mảnh giao nhau phức tạp (94 mảnh Di Lặc — nhưng chỉ cần
    hợp nhất cụm ĐẦU, khoảng 15–20 mảnh).
  - *Voxel Remesh*: bọc lại thành vỏ kín đều; voxel càng nhỏ càng giữ form
    nhưng mặt phình nhanh; quy tắc cộng đồng: giảm voxel theo bước ≤1,5× và
    chỉ giảm khi form ở độ phân giải hiện tại đã xong.
  - Đường thực tế cho dự án: **Boolean Union trước** (giữ form gốc tối đa) →
    nếu còn mảnh lỗi/non-manifold thì **Voxel Remesh ở voxel đủ mịn** làm
    lưới clay → đo lại.
- **Áp vào nợ:** áp cho cụm đầu Di Lặc + A Di Đà (+ 2 bản cổng là bản sao tỉ
  lệ — xử lý riêng ở §6 bước 4; Phật nằm: đầu liền thân dài, chỉ xử lý vùng
  mặt bằng mask, xem 1.3).
- **Khả thi:** có. Boolean trên ~20 mảnh + remesh một đầu tượng (~1,2–1,8 m)
  là việc nhẹ so với render toàn cảnh; chạy trong file riêng thì RAM thoải mái.
- **Rủi ro luật tượng:** **TRUNG BÌNH — điểm rủi ro chính của cả vòng V15.**
  Cả Boolean lẫn voxel đều dời bề mặt (voxel: tới ~cỡ voxel ở vùng cong gắt).
  Bắt buộc: đo lại TOÀN BỘ bảng số khóa ngay sau hợp nhất (tai/head, đỉnh/đáy
  tai, nose frac, độ nổi quy về mốc mặt) và nắn khối lớn (Grab ở multires thấp
  / voxel thô) về trong ±0,01 như dung sai V13/V14 trước khi đi tiếp. Nếu sau
  hợp nhất có chỉ số lệch >0,02 mà không nắn về được → DỪNG, báo cáo, không
  sculpt tiếp trên nền sai.
- **Công sức:** 0,5–1 ngày chạy máy (viết script hợp nhất + harness đo bề mặt
  mới + 1–2 lượt thử/sửa), cho cả hai tượng chính.

### 1.3 Sculpt chi tiết mặt: rãnh thay ống nổi, sống mũi/lỗ mũi, mí liền khối

- **Nguồn:** https://kitchendemy.com/how-to-make-a-face-in-blender/
  (Crease "xuất sắc cho môi và mí mắt"; Draw Sharp cho chi tiết sắc; mũi:
  sống → chóp → lỗ mũi/cánh bằng Clay/Draw rồi Crease mở lỗ mũi);
  https://yelzkizi.org/realistic-character-creation-process-in-blender/
  (Crease+Pinch cho nếp và mép môi; lỗ mũi phải có độ dày và hình giọt nước);
  https://github.com/roble3/cc-blender-skill/blob/HEAD/knowledge/03-sculpting-retopo/00-overview.md
  (bảng brush: Crease Shift+C, Pinch, Snake Hook, Mask…);
  https://corpsephageblog.blogspot.com/2024/12/sculpting-head-in-blender.html
  (Draw Ctrl+click khoét lỗ mũi; Draw Sharp vẽ miệng — nó đẩy mặt vào trong
  theo mặc định).
- **Cách làm theo từng chi tiết của mình:**
  - *Mắt khép thanh thản (cả 3 tượng):* không khoét hốc mắt kiểu người mở mắt.
    Sculpt mí thành một mặt lồi nhẵn liền khối, rồi dùng **Crease/Pinch** rạch
    MỘT rãnh mảnh đúng vị trí đường mi (thay 3 ống trắng xếp chồng hiện tại).
    Rãnh là hình học ÂM nên bắt sáng/tối như ảnh thật, không còn "vạch dán".
  - *Nếp cười Di Lặc:* bỏ ống nổi; dùng Crease + Draw (trừ) khắc rãnh âm cong
    từ cánh mũi xuống khóe miệng, độ sâu nông (đích độ nổi V14 đã khóa tương
    đương: chi tiết phải nằm TRONG biên ±0,01–0,02 m quanh bề mặt đích).
  - *Mũi:* từ khối oval hiện tại, Clay Strips dựng SỐNG mũi nối trán→chóp,
    Draw (trừ, Ctrl) khoét 2 lỗ mũi nhỏ ở mặt dưới chóp + Pinch tạo cánh mũi.
    Rộng mũi bị khóa ở 0,2500/0,2720 — sculpt chỉ thêm cấu trúc TRONG biên đó.
  - *Miệng:* bỏ thanh ngang; môi là hai gờ mềm (Clay) với rãnh Crease ở đường
    giữa; cong môi theo ảnh (mục V14 đã ghi "cong môi" thuộc sculpt).
  - *Má Di Lặc:* Smooth + Clay hòa cầu má vào mặt (hết đường biên "cầu dán"),
    giữ độ phình tương đương độ nổi +0,100 đã khóa.
  - *Tóc xoắn A Di Đà (ốc xoắn trên đầu):* ảnh ref3 có các cuộn xoắn nhỏ đều.
    Hai đường: (a) sculpt từng cuộn ở multires cao — chậm, khó đều; (b) mô-đun
    cuộn xoắn nhỏ instance bằng Geometry Nodes lên vùng da đầu của lưới đã
    sculpt — đều và rẻ, nhưng là hình học gắn thêm (giống cách dự án từng gắn
    mảnh). Khuyến nghị thử (b) sau khi mặt xong; nếu render cận vẫn giả thì
    ghi nợ, không chặn cả vòng vì tóc.
  - *Mask/Face Sets:* khoanh vùng sculpt (mặt / tai / tóc) để không lan sang
    vùng đã khóa — tương đương kỷ luật "checksum ngoài phạm vi rỗng" của
    V13/V14 nhưng ở cấp độ vùng trên cùng một lưới.
- **Khả thi:** có — đây là sculpt mức "khối phụ + rãnh nông", không phải
  chi tiết lỗ chân lông; độ phân giải cần thiết vừa phải (multires 4 là đủ
  cho rãnh mi/nếp cười ở khoảng cách render hiện tại).
- **Rủi ro luật tượng:** CAO nếu làm bằng tay tự do; hạ xuống THẤP bằng quy
  trình: mỗi pass sculpt chỉ xử lý ĐÚNG danh sách chi tiết đã liệt kê từ ảnh,
  sau mỗi pass chạy cổng đo §1.4 + render cùng camera đặt cạnh ảnh thật,
  coordinator soi mới qua pass sau. Tuyệt đối không "nắn cho đẹp" ngoài danh
  sách. *Lưu ý trung thực: sculpt qua script bpy thuần túy (không có tay người
  cầm bút) cho chất lượng thấp hơn sculpt thủ công nhiều; kỳ vọng đúng mức là
  "hết mảnh ghép rời, rãnh đọc đúng ở khoảng cách toàn cảnh/bán cận" — không
  hứa chất lượng chân dung cận như nghệ sĩ sculpt.*
- **Công sức:** Di Lặc 2–4 ngày (tượng mặt to, cười, nhiều chi tiết nhất);
  A Di Đà 2–3 ngày (mặt thanh, ít chi tiết hơn, cộng phần tóc xoắn);
  Phật nằm 0,5–1 ngày (chỉ đường mi khép + môi, mặt nhìn nghiêng).

### 1.4 Khóa tỉ lệ khi sculpt — cổng đo MỚI cho lưới đã hợp nhất

Đây là phần dự án phải tự chế, vì cổng V13/V14 đo trên ma trận OBJECT
(từng mảnh) — sau hợp nhất các mảnh không còn tồn tại.

- **Nguồn kỹ thuật:** https://www.blenderstudio.cn/en/training/realistic-character-workflow/chapter/3-shapes-and-wrinkles/
  (Blender Studio: sculpt trên shape key thay vì sculpt layer; dùng Geometry
  Nodes so sánh vị trí đỉnh với bản gốc nhân đôi, tô màu độ lệch để theo dõi
  biến dạng); https://superhivemarket.com/products/retopoproof--prove-your-retopology-still-is-the-sculpt?search_id=50431512
  (nguyên tắc đo HAI CHIỀU khi đối chiếu lưới mới với bề mặt cũ: đo một chiều
  sẽ mù trước chi tiết bị MẤT — ví dụ thiếu tai vẫn ra số "sạch").
- **Cách làm (đề xuất cổng V15, kế thừa tinh thần verify_v13/v14):**
  1. **Basis khóa:** trước khi sculpt, lưu shape key "Basis_V17" = lưới hợp
     nhất nguyên trạng + một bản sao object ẩn làm mốc. Sculpt chỉ trên key
     mới; Basis không bao giờ bị sửa (đúng vai trò file pristine ở cấp object).
  2. **Bảng mốc bề mặt:** tái dùng đúng định nghĩa đo V13 (chiều cao đầu =
     cằm→đỉnh, loại cổ/tai khỏi mẫu số) và bảng đích V13/V14/V14.1 (tai 0,664/
     0,507; nose frac 0,2500/0,2720; các độ nổi đích). Đo trên lưới mới bằng:
     (a) bbox theo cụm đỉnh phân vùng (tai/mũi theo vùng không gian đã biết);
     (b) **render cùng camera đã khớp ảnh** (xem 1.6) rồi đo landmark trên
     ảnh render bằng cùng pipeline PIL + visual grounding đã dùng ở V14 —
     đây là cổng chính, vì nó đo đúng cái mắt người thấy.
  3. **Bản đồ lệch (deviation map):** Geometry Nodes so đỉnh lưới sculpt với
     bản sao mốc → vùng nào lệch > ngưỡng (đề xuất 0,02 m ngoài vùng chi tiết
     cho phép) sẽ hiện màu; vùng tai/thân/bệ phải ~0 tuyệt đối như chuẩn
     "worst dev 0,0" của V14.1.
  4. **Pixel-diff khoanh vùng:** như V14 (diff V15↔V16 chỉ 3,4%/1,4% đúng
     vùng mặt) — render trước/sau cùng camera, diff phải nằm trong bbox mặt,
     ngoài mặt ≈ 0.
- **Khả thi:** có; (2b) dùng lại hạ tầng đo ảnh sẵn có của dự án.
- **Rủi ro luật tượng:** đây là cơ chế GIẢM rủi ro — không có nó thì không
  được mở vòng sculpt.
- **Công sức:** gộp trong 1.2 (harness đo) + ~0,5 ngày viết cổng render-đo.

### 1.5 Retopology + multires + bake (có cần cho dự án này không?)

- **Nguồn:** https://github.com/roble3/cc-blender-skill/blob/HEAD/knowledge/03-sculpting-retopo/00-overview.md;
  https://cada-edu.com/guides/3d-character-modelling-for-games-how-to-model-in-blender
- **Đánh giá riêng cho dự án:** tượng là vật TĨNH, render tĩnh, không rig/
  không biến dạng → **retopology sạch kiểu nhân vật game là KHÔNG cần thiết
  ở mức đầy đủ.** Chỉ cần: lưới hợp nhất → (voxel/QuadriFlow remesh vừa đủ
  đều để sculpt không bị kéo méo) → multires sculpt. Bake normal map chỉ cần
  nếu muốn trả tượng về độ phân giải thấp cho nhẹ cảnh — tùy chọn tối ưu sau,
  không phải điều kiện đạt. Bỏ qua retopo thủ công tiết kiệm phần việc đắt
  nhất (trường hợp tham chiếu: một dự án sculpt Phật trên YouTube tốn tổng
  ~42 giờ mà "phần lớn thời gian là retopology" —
  https://www.youtube.com/watch?v=2zwhL7nRljI).
- **Khả thi:** QuadriFlow remesh có sẵn trong Blender (bpy.ops.object.
  quadriflow_remesh) — chạy được bằng script trên VM.
- **Rủi ro:** QuadriFlow cũng dời bề mặt nhẹ → vẫn qua cổng 1.4.
- **Công sức:** tránh được 3–5 ngày so với pipeline nhân vật đầy đủ.

### 1.6 Khớp camera vào ảnh thật (fSpy / Perspective Plotter)

- **Nguồn:** https://www.motionmaster3d.com/blog/fspy-alternative-blender
  (trạng thái fSpy trên Blender 5: bản chính thức 1.0.3 từ 2019 không còn bảo
  trì, có báo cáo chạy được trên 5.0/5.1 qua fork cộng đồng; lựa chọn trong
  Blender: Perspective Plotter ~$18, Simple Camera Match miễn phí);
  https://blendervisualinvestigation.com/knowledge-base/docs/tools/fspy/
  (cách solve: kéo đường song song → điểm tụ → tiêu cự/vị trí camera; ảnh
  không có kích thước tuyệt đối, phải đặt Reference Distance theo vật đo được).
- **Áp vào dự án:** cổng D-d miệng Di Lặc ở V14 bị treo vì "mẫu số bbox ảnh
  chưa chứng minh được" — một phần do camera render so với ảnh chưa khớp
  hình học chặt. fSpy solve camera từ các đường kiến trúc CHÙA trong ảnh
  (cạnh điện, bậc thềm — ref5/ref3 đều có kiến trúc phía sau) rồi render
  tượng bằng đúng camera đó → số đo trên render và trên ảnh cùng hệ quy
  chiếu, cổng đo 1.4(2b) đáng tin hơn hẳn.
- **Giới hạn trung thực:** fSpy cần đường thẳng song song rõ — đầu tượng tự
  nó không có; phải solve từ kiến trúc nền rồi cắt khung vào mặt. Ảnh bị cắt
  cúp (crop) làm principal point lệch tâm → kết quả solve có sai số; vẫn tốt
  hơn ước lượng tay (V14 dùng lens 85 + azimut 30° ước lượng).
- **Khả thi:** fSpy standalone miễn phí, chạy ngoài Blender; rủi ro tương
  thích importer trên Blender 5.0.1 — có đường vòng: nhập tay thông số camera
  (tiêu cự/vị trí/quay) từ fSpy vào Blender bằng script, không phụ thuộc addon.
- **Rủi ro luật tượng:** không (chỉ là công cụ đo).
- **Công sức:** 0,25–0,5 ngày cho ref5 + ref3.

### 1.7 FaceBuilder / KeenFace — đánh giá và KHUYẾN NGHỊ KHÔNG dùng làm đường chính

- **Nguồn (đã mở đọc trực tiếp):** https://keentools.io/products/facebuilder-for-blender
  — FaceBuilder: gắn lưới đầu người mẫu của hãng vào ảnh bằng pins/landmark
  (bản 2024.1 tự nhận diện mặt, 70+ landmark), chạy được với vài ảnh, kể cả
  1 ảnh; thuê bao Freelancer $19,99/tháng (hoặc $15,99/tháng trả năm), dùng
  thử 15 ngày miễn phí. FAQ của hãng ghi rõ: **"Có dùng mesh tự có thay đầu
  mẫu được không? — Hiện tại không. Cách vòng: wrap lưới FaceBuilder bằng
  topology khác."** KeenFace (dịch vụ cloud mới): 1–15 ảnh, trả theo đầu,
  xuất topology MetaHuman —
  https://www.awn.com/news/keentools-keenface-turns-photos-metahuman-ready-3d-heads
- **Vì sao không hợp:** (1) sản phẩm là ĐẦU NGƯỜI mẫu — tai người không thể
  đạt tỉ lệ tai/đầu 0,664 đã khóa nếu không kéo giãn ngoài thiết kế của
  công cụ; ushnisha/mắt khép thanh thản không thuộc hệ biểu cảm người của
  nó; (2) thay đầu mẫu vào tượng = thay đổi danh tính hình học của tượng,
  ngược tinh thần luật tượng hơn cả sculpt trên lưới gốc (sculpt giữ 100%
  hình khối gốc làm nền); (3) KeenFace phải tải ảnh di sản lên cloud của
  bên thứ ba và trả tiền theo đầu — dự án ưu tiên công cụ miễn phí;
  (4) FaceBuilder cần đăng ký thuê bao Core Library sau 15 ngày thử.
- **Dùng được ở đâu:** nếu muốn, chỉ như THÍ NGHIỆM đối chứng trong 15 ngày
  thử miễn phí: dựng thử đầu Di Lặc từ ref5, đo bằng cổng 1.4 — nếu (như dự
  đoán) tai/tỉ lệ không đạt bảng khóa thì loại hẳn, có số mà kết luận.
- **Công sức nếu thử:** 0,5 ngày. **Khuyến nghị: không thử ở V15** — để sau
  khi đường sculpt chính cho kết quả, tránh phân tán.

---

## 2. Photogrammetry / quét 3D từ ảnh refs hiện có — KHÔNG khả thi

- **Nguồn:** https://33d.ch/en/blog/meshroom (Meshroom: vật nhỏ cần ~70–150
  ảnh vòng quanh có chủ đích; bản 2025.1 dùng CUDA 12, cần GPU compute
  capability ≥5.0 cho bản đầy đủ); https://dappcdn.com/download/graphic-apps/meshroom
  ("ít nhất 50 ảnh, tối thiểu 30, chồng lấp 60–70%"; không GPU NVIDIA thì chỉ
  còn Draft Meshing chậm và kém); https://kimono-oyaji.com/en/photogrammetry-smartphone-01-en/
  (bảng đo thực tế: 10 ảnh ≈180° → méo + lỗ lớn; 30–40 ảnh 360° mới "thực
  dụng"; xử lý trên GPU RTX 3090 đã 8–15 phút cho 30–40 ảnh);
  https://3dx.info/beyond-your-smartphone-budget-friendly-camera-setups-for-high-quality-photogrammetry/
  (Meshroom yêu cầu chồng lấp ≥80% mặt trước / 60% mặt bên; lưới quét có tỉ
  lệ tùy ý nếu không neo bằng kích thước đo thật).
- **Đối chiếu kho refs của mình:** 14 ảnh (`~/workspace/vinh-trang-3d/refs/`)
  là ảnh du lịch: ít góc, không vòng quanh tượng nào đủ 360°, chồng lấp không
  có hệ thống, tiêu cự/độ cao máy khác nhau, tượng trắng đơn sắc ít đặc trưng
  bề mặt (SfM ghép điểm dựa vào texture — mặt tượng trắng trơn là ca khó
  kinh điển). Kết quả chắc chắn: solve thiếu camera hoặc lưới lỗ/méo — tệ hơn
  lưới hiện tại vốn đã đúng số đo.
- **Kết luận:** KHÔNG chạy photogrammetry ở V15. Lộ trình duy nhất để nó khả
  thi là Chung Hy (hoặc người tại chỗ) chụp MỚI tại chùa: mỗi tượng 80–150
  ảnh, 2–3 vòng (ngang tầm / cao / thấp), chồng lấp ≥70%, ánh sáng tản đều,
  kèm 1 kích thước neo thật (chiều cao bệ đo bằng thước). Đó là việc của
  người tại hiện trường, không phải việc VM; và xử lý Meshroom bản đầy đủ
  vẫn cần máy có GPU NVIDIA (máy Mac của Chung Hy hoặc dịch vụ ngoài) —
  VM này chỉ chạy được draft CPU rất chậm. Ghi nhận là phương án "nếu có
  chuyến đi chùa" chứ không lên kế hoạch.
- **Rủi ro luật tượng (nếu sau này làm):** lưới quét là dữ liệu đo trực tiếp
  từ tượng thật — về nguyên tắc PHÙ HỢP luật tượng nhất trong mọi kỹ thuật;
  rủi ro nằm ở bước dọn lưới (lấp lỗ = bịa hình) — vùng lấp phải được đánh
  dấu và đối chiếu ảnh như cổng 1.4.

---

## 3. Nợ 2 — Tán dừa góc cạnh khi nhìn gần (alpha-card)

- **Nguồn (có số đo):** https://blog.michelanders.nl/2018/01/blender-transparent-particles-vs.html?m=1
  — thí nghiệm Cycles có kiểm soát: cùng hệ hạt lá, bản lá HÌNH HỌC render
  nhanh hơn bản alpha-card ~20% trên CPU (tới ~50% trên GPU ở mật độ cao),
  vì alpha phải trả transparent bounces (để mặc định 8; lá hình học thì số
  bounce này không ảnh hưởng). https://blenderartists.org/t/game-foliage-alpha-cards-vs-geo/1656216
  — đồng thuận cộng đồng kiểu LOD: xa dùng card, gần dùng hình học.
- **Cách làm áp vào mình:** giữ nguyên vành đai 340 cây ở xa (cards, rẻ,
  flycam đã đạt 32,93% xanh). Chỉ dựng lại ~8–12 cây "hero" gần đường đi/
  cổng/sân bằng tàu dừa HÌNH HỌC: mỗi tàu là dải lưới cong có gân giữa, lá
  chét là các dải con hoặc texture opaque không alpha (cắt silhouette bằng
  hình học ở mép tàu), instance bằng Geometry Nodes để RAM không phình
  (instance dùng chung dữ liệu lưới). Thân dừa giữ nguyên.
- **Khả thi:** có — số cây ít, làm bằng script (sinh tàu theo tham số cong/
  dài/góc rủ, random hạt giống cố định để tái lập). Render còn có lợi về
  thời gian theo số đo ở trên.
- **Rủi ro luật tượng:** không liên quan tượng. Rủi ro thẩm mỹ: tàu hình học
  xấu hơn card nếu cong/chét làm ẩu → cổng: render cận 2 cây mẫu, coordinator
  soi cạnh ảnh thật trước khi nhân ra cả nhóm hero.
- **Công sức:** 1–2 ngày (script sinh tàu + thay cây hero + render đối chiếu).

## 4. Nợ 3 — Rêu mái còn vệt

- **Nguồn:** https://80.lv/articles/building-a-game-ready-nordic-village-scene-with-day-night-lighting-setups
  (pipeline sản xuất thật: mid-poly + SƠN VERTEX nhiều lớp — bùn/rêu/mài mòn —
  trên cùng vật liệu lát lặp, cộng mặt nạ thủ tục theo góc pháp tuyến);
  https://superhivemarket.com/products/realmaterials?search_id=50431515
  (SuperMaterials: mặt nạ AO "bùn trong góc" BAKE ra ảnh một lần → chi phí
  render bằng 0; rêu chảy theo Flow Gradient từ mép chọn trước);
  https://www.instagram.com/reel/Da5At2pzmD-/ (quy trình scatter rêu trên mái
  bằng particle + weight paint mật độ).
- **Cách làm áp vào mình:** rêu V9–V11 hiện là các patch card đặt tay (đạt ở
  mức "có rêu đúng chỗ") nhưng vệt vì cạnh patch lộ. Nâng cấp 2 lớp:
  (1) **Rêu shader:** trong material mái, trộn màu rêu bằng mặt nạ =
  AO/Pointiness (rãnh giữa các hàng ngói) × hướng mặt hướng lên × Noise
  Texture vỡ vụn (hết vệt thẳng) — rêu tự sinh trong rãnh ngói đúng vật lý
  ẩm; trên VM Cycles CPU, noise thủ tục rẻ; nếu muốn chắc ăn thì bake mặt
  nạ này ra texture 2K một lần rồi dùng như ảnh (chi phí render ~0).
  (2) giữ lại ít patch 3D ở mép mái/rãnh chính làm "rêu dày" như V11.
  KHÔNG khuyến nghị dựng lại ngói hình học hàng loạt (Array/Lattice kiểu
  tutorial mái châu Á — https://www.instagram.com/reel/DeMulf5Mxid/ — đó là
  kỹ thuật dựng mái MỚI từ đầu; mái của mình đã có và đã khóa số đo, dựng
  lại là phá việc đã đạt để đổi lấy nợ khác).
- **Khả thi:** có, thuần shader/script, nhẹ máy.
- **Rủi ro:** không liên quan tượng. Rủi ro màu: rêu shader dễ "xanh đều"
  giả → cổng màu bằng dải đo G−R như các vòng trước + soi mắt.
- **Công sức:** 0,5–1 ngày.

## 5. Nợ 4 — Tượng trong hốc cổng bị tối

- **Nguồn:** https://docs.blender.org/manual/nl/latest/render/lights/light_linking.html
  (Blender Manual 5.1: Light Linking — đèn chỉ chiếu vào object/collection
  được chỉ định; Shadow Linking — kiểm soát vật nào chắn sáng; lấy mẫu hiệu
  quả nhất khi bật Light Tree); https://jsabbott.artstation.com/blog/Bdd6z/how-to-use-light-and-shadow-linking-in-blender-4-0
  (thao tác từng bước từ Blender 4.0, Cycles).
- **Cách làm áp vào mình:** dự án đã có tiền lệ đèn fill tay (Di Lặc: Point
  1500 W ấm). Chuẩn hóa thành rig: mỗi hốc cổng 1 Area/Point fill nhỏ đặt
  trong hốc, **Light Linking Include = chỉ 39 mảnh tượng của hốc đó** (đèn
  không rò ra tường/cổng), Shadow Linking loại chính tượng khỏi tự chắn.
  Đèn linked không làm sáng phần còn lại của cảnh → giữ nguyên grade
  "Sáng trong" đã khóa và các số Mist/bão hòa V11.
- **Khả thi:** có sẵn trong Blender 5.0.1 (tính năng từ 4.0), script bpy đặt
  linking collection được; chi phí render tăng không đáng kể với Light Tree.
- **Rủi ro luật tượng:** không — chỉ chiếu sáng, không đụng hình. (Đây là
  mục "chờ Chung Hy quyết" từ V12: hồ sơ này xác nhận kỹ thuật sạch và rẻ;
  quyết vẫn ở coordinator/Chung Hy.)
- **Công sức:** 0,25–0,5 ngày gồm render đối chiếu hốc trước/sau.

## 6. Nợ 5 — Tỉ lệ sơ đồ toàn cảnh (Di Lặc 11,3 m vs thật ~20 m)

Không có kỹ thuật Blender nào "sửa" việc này ngoài phóng tỷ lệ toàn bộ tổ
hợp ×~1,77 — tức dựng lại vị trí/camera/điểm đứng của mọi vòng đo V5–V14.1
và phá tương đương với cảnh web. **Khuyến nghị: giữ nguyên, không đưa vào
V15**; nếu sau này Chung Hy muốn "đúng tỉ lệ thật" thì đó là một dự án riêng
(layout V-mới từ đầu trên nền asset hiện có), không phải vòng cải tiến.

---

## 7. Giới hạn máy này (VM 8 GB RAM, Cycles CPU, Eevee hỏng) — kỹ thuật nào sống được

- **Nguồn:** https://github.com/roble3/cc-blender-skill/blob/HEAD/knowledge/03-sculpting-retopo/00-overview.md
  (multires level 5+ trên base 10K = 10M+ mặt, hiệu năng tụt; dyntopo detail
  <3 px làm máy bò và phình bộ nhớ); https://docs.blender.org/manual/zh-hans/3.6/sculpt_paint/sculpting/introduction/adaptive.html
  (manual: chuyển level >5 làm chậm chuyển mức rõ rệt);
  https://geturna.com/en/guides/render-faster-blender-cycles (Noise Threshold
  0,02–0,05 + OpenImageDenoise giữ chi tiết; giảm Max Bounces; Clamp Indirect
  1–5 dập firefly; Persistent Data giữ cảnh trong RAM giữa các frame);
  https://www.renderjuice.com/blog/how-to-render-faster-in-blender
  (adaptive sampling; bộ nhớ quyết bởi texture/subdivision/instance;
  tiling để chặn đỉnh RAM ở render lớn).
- **Bảng khả thi trên máy này:**

| Kỹ thuật | Khả thi? | Điều kiện |
|---|---|---|
| Sculpt 1 đầu tượng trong file riêng, multires ≤4 (≈0,3–1,3M mặt ở level cao nhất tùy base) | ✅ | File chỉ chứa đầu + mốc; sculpt từng tượng một |
| Sculpt trong file toàn cảnh 98 MB (2568 object) | ❌ | RAM + độ trễ; mọi vòng trước đã phải canh MemAvailable ≥1.800 MB chỉ để BUILD ma trận |
| Boolean Union ~20 mảnh đầu / QuadriFlow 1 đầu | ✅ | Chạy trong file riêng, một lần |
| Voxel Remesh đầu ở voxel mịn (≤0,01 m) | ⚠️ | Mặt phình rất nhanh ở vật 1,2–1,8 m; chỉ dùng khi Boolean lỗi, và đo lại sau |
| Dyntopo chi tiết mịn toàn đầu | ⚠️ | Chỉ vùng nhỏ (quanh mắt/mũi) với detail 5–12 px; toàn đầu sẽ phình RAM |
| Bake normal/displacement từ multires | ✅ | Một lần, trong file riêng |
| Render kiểm chứng Cycles CPU (khuôn mặt, crop vùng) | ✅ | Render region/crop quanh đầu + adaptive sampling + OIDN; giữ driver canh khe CPU như V13/V14 |
| Render toàn cảnh sau khi thay đầu | ✅ | Như hiện tại (đã là quy trình chuẩn của dự án) |
| Photogrammetry Meshroom đầy đủ | ❌ | Cần GPU NVIDIA CUDA; CPU draft chậm/kém — và thiếu ảnh đầu vào (xem §2) |
| FaceBuilder chạy trong Blender trên VM | ⚠️ | Addon nhẹ, chạy được; nhưng không khuyến nghị vì lý do ở §1.7, không phải vì máy |
| Geometry Nodes sinh tàu dừa/tóc xoắn instance | ✅ | Instance dùng chung lưới — RAM rẻ |
| Rêu shader (noise/AO/pointiness) hoặc bake mặt nạ | ✅ | Bake một lần → render ~0 chi phí thêm |

- **Quy tắc vận hành giữ nguyên từ các vòng trước:** driver tự chờ khe
  (ffmpeg=0, không Blender lạ, load thấp, MemAvailable đủ), checkpoint từng
  bước ra workspace (không /tmp), render nghiệm thu cùng camera để diff được.

---

## 8. ĐỀ XUẤT THỨ TỰ VÒNG V15 (điêu khắc mặt tượng)

Nguyên tắc xuyên suốt: **một tượng một vòng nhỏ; qua cổng mới đi tiếp; file
pristine V17 không đụng; mọi thay đổi đều có cặp số trước–sau.** Thứ tự ưu
tiên theo "lợi ích nhìn thấy / rủi ro": Di Lặc trước (mặt to nhất, ref5 rõ
nhất, lỗi ghép mảnh lộ nhất), A Di Đà sau (áp lại quy trình đã chứng minh),
cổng + Phật nằm cuối (cơ học).

### Bước 0 — Hạ tầng cổng đo cho lưới hợp nhất (làm trước mọi sculpt)
1. Trích cụm đầu Di Lặc + A Di Đà ra file riêng từ `layout_v17_v141.blend`
   (bản sao); giữ nguyên mọi mảnh ngoài đầu.
2. Viết harness đo bề mặt (§1.4): bảng đích khóa từ V13/V14/V14.1 sao nguyên
   văn; đo bằng bbox vùng + render-khớp-camera (dùng fSpy §1.6 cho ref5/ref3
   nếu solve được, không thì giữ camera ước lượng V14 và ghi rõ).
3. Chạy harness lên lưới GỐC chưa hợp nhất → phải tái lập đúng các số V14.1
   (sai lệch ≤0,005) thì harness mới được tin. **Cổng 0 không qua = dừng.**

### Bước 1 — Hợp nhất + nắn nền (Di Lặc)
1. Boolean Union cụm đầu → (dự phòng) voxel remesh; đo lại toàn bảng.
2. Nắn khối lớn (Grab/Smooth ở mức thấp) về ±0,01 của bảng khóa; tai không
   được lệch khỏi 0,664/0,321/+0,015 — nếu tai bị remesh làm tròn cạnh thì
   xử lý riêng: giữ tai là mảnh RIÊNG ngoài lưới sculpt (tai đã đạt từ V13,
   không có lý do hợp nhất tai vào vùng sculpt mặt) — **kiến nghị: hợp nhất
   chỉ vùng MẶT (trán–mũi–má–miệng–cằm), tai + ushnisha + cổ giữ nguyên mảnh
   gốc.** Việc này giảm rủi ro nhất mà vẫn đạt mục tiêu liền khối của mặt.
3. **Cổng 1:** mọi chỉ số trong ±0,01; deviation map ngoài vùng mặt = 0;
   render diff với V17 chỉ trong bbox mặt.

### Bước 2 — Chi tiết mặt Di Lặc (theo danh sách đóng, từ ảnh ref5)
Theo thứ tự: hòa má → sống mũi + lỗ mũi/cánh mũi → rãnh nếp cười (âm) →
môi cong + rãnh giữa môi → rãnh mí mắt. Sau MỖI chi tiết: render cùng
camera + đo lại chỉ số liên quan (rộng mũi không rời 0,2500 ±0,01; độ nổi
má tương đương +0,100 ±0,02; tâm miệng KHÔNG di chuyển — cổng D-d của V14
vẫn đóng, sculpt không được lén mở lại cổng đó).
**Cổng 2:** coordinator soi render cạnh ref5 — verdict như chuẩn cũ:
số đo đạt / giống thật tổng thể chấm riêng, không trộn.

### Bước 3 — A Di Đà (lặp lại bước 1–2 với bảng số của tượng này)
Cộng mục riêng: tóc xoắn bằng instance Geometry Nodes (§1.3) — cổng phụ
riêng, hỏng thì bỏ mục này, không chặn mặt. Rộng đầu A Di Đà (nợ đo A1 của
V14) vẫn KHÔNG tự sửa: chỉ sculpt trong biên đầu hiện tại.

### Bước 4 — Truyền sang 2 tượng hốc cổng + Phật nằm
- Cổng: thay cụm mặt của bản sao cổng bằng bản sao thu nhỏ đều (0,1953) của
  lưới mặt đã sculpt (thay vì liên hợp từng mảnh như V13/V14 — lưới mới là
  một khối nên nhân bản theo tỉ lệ là chính xác tuyệt đối); kiểm chứng:
  tỉ lệ tai/mũi của bản cổng khi đo lại phải bằng bản chính ±0,005.
- Phật nằm: chỉ 2 nét (rãnh mí khép, môi) bằng mask vùng mặt trên lưới thân
  hiện tại, không hợp nhất toàn thân.
- Kèm rig Light Linking cho 2 hốc (§5) để mặt mới không chìm trong tối.

### Bước 5 — Ghép trả vào cảnh + nghiệm thu toàn cảnh
Thay cụm đầu trong bản sao của layout_v17 → file V15 mới; verify toàn cảnh
kiểu V14: số object ngoài phạm vi thay đổi = 0, checksum phần còn lại rỗng;
render bộ chuẩn (face_dilac, face_adida, niche, flycam + ref5_dilac cùng
góc) + pixel-diff khoanh vùng; coordinator soi cạnh ref5/ref3/ref11 rồi
mới kết luận giống thật.

### Việc KHÔNG làm ở V15 (ghi rõ để khỏi trôi phạm vi)
- Photogrammetry (thiếu ảnh + thiếu GPU — §2).
- FaceBuilder/KeenFace (§1.7).
- Phóng tỉ lệ toàn cảnh về 20 m (§6).
- Mở lại cổng D-d miệng Di Lặc (số chưa đủ chứng minh — V14 đã kết luận).
- Retopology thủ công đầy đủ + rig (tượng tĩnh, không cần — §1.5).
- Các nợ phụ (tàu dừa hero §3, rêu shader §4, đèn hốc §5) là các vòng NHỎ
  độc lập, chạy song song được với V15 vì không đụng tượng; riêng đèn hốc
  nên về đích cùng bước 4.

### Ước lượng tổng V15 (chỉ phần tượng, theo ngày chạy máy có canh khe CPU)
Bước 0: 0,5–1 · Bước 1: 0,5–1 · Bước 2: 2–4 · Bước 3: 2–3 · Bước 4: 0,5–1 ·
Bước 5: 0,5–1 → **tổng ~6–11 ngày** (chưa tính thời gian chờ khe CPU như
các vòng trước vẫn gặp). Nợ phụ song song: đèn hốc 0,25–0,5 · rêu 0,5–1 ·
dừa hero 1–2.

---

## 9. Danh mục nguồn đã dùng (toàn bộ đã truy cập được qua tìm kiếm/mở trang)

Sculpt & pipeline:
- https://github.com/roble3/cc-blender-skill/blob/HEAD/knowledge/03-sculpting-retopo/00-overview.md (đã mở đọc)
- https://www.strayspark.studio/blog/how-to-make-a-3d-character-in-blender-2026
- https://cada-edu.com/guides/3d-character-modelling-for-games-how-to-model-in-blender
- https://yelzkizi.org/realistic-character-creation-process-in-blender/
- https://kitchendemy.com/how-to-make-a-face-in-blender/
- https://corpsephageblog.blogspot.com/2024/12/sculpting-head-in-blender.html
- https://www.youtube.com/watch?v=2zwhL7nRljI (dự án sculpt Phật — số 42 giờ/retopo là chính, lấy từ mô tả kết quả tìm kiếm)

Hợp nhất lưới / remesh:
- https://copyprogramming.com/howto/how-to-join-multiple-objects
- https://docs.blender.org/manual/zh-hans/3.6/sculpt_paint/sculpting/introduction/adaptive.html (trang manual bản zh-hans do tìm kiếm trả về; nội dung tương ứng mục Adaptive Resolution của Blender Manual)
- https://3d-agent.com/blender-ai/3d-printing

Khóa tỉ lệ / đối chiếu lưới:
- https://www.blenderstudio.cn/en/training/realistic-character-workflow/chapter/3-shapes-and-wrinkles/
- https://superhivemarket.com/products/retopoproof--prove-your-retopology-still-is-the-sculpt?search_id=50431512

Dựng mặt từ ảnh / khớp camera:
- https://keentools.io/products/facebuilder-for-blender (đã mở đọc, gồm giá + FAQ)
- https://superrendersfarm.com/article/keentools-facebuilder-2024-1-blender-update
- https://www.awn.com/news/keentools-keenface-turns-photos-metahuman-ready-3d-heads
- https://www.motionmaster3d.com/blog/fspy-alternative-blender
- https://blendervisualinvestigation.com/knowledge-base/docs/tools/fspy/

Photogrammetry:
- https://33d.ch/en/blog/meshroom
- https://dappcdn.com/download/graphic-apps/meshroom
- https://kimono-oyaji.com/en/photogrammetry-smartphone-01-en/
- https://3dx.info/beyond-your-smartphone-budget-friendly-camera-setups-for-high-quality-photogrammetry/

Tán lá / rêu / kiến trúc:
- https://blog.michelanders.nl/2018/01/blender-transparent-particles-vs.html?m=1
- https://blenderartists.org/t/game-foliage-alpha-cards-vs-geo/1656216
- https://80.lv/articles/building-a-game-ready-nordic-village-scene-with-day-night-lighting-setups
- https://superhivemarket.com/products/realmaterials?search_id=50431515
- https://www.instagram.com/reel/Da5At2pzmD-/ (scatter rêu bằng weight paint — chỉ đọc được qua tóm tắt kết quả tìm kiếm)
- https://www.instagram.com/reel/DeMulf5Mxid/ (tutorial mái cong châu Á: Array + Boolean + Lattice — chỉ đọc được qua tóm tắt kết quả tìm kiếm)

Ánh sáng hốc:
- https://docs.blender.org/manual/nl/latest/render/lights/light_linking.html (trang manual bản nl do tìm kiếm trả về; nội dung là mục Light Linking của Blender Manual 5.1)
- https://jsabbott.artstation.com/blog/Bdd6z/how-to-use-light-and-shadow-linking-in-blender-4-0

Hiệu năng Cycles CPU:
- https://geturna.com/en/guides/render-faster-blender-cycles
- https://www.renderjuice.com/blog/how-to-render-faster-in-blender

*Không có nguồn nào trong hồ sơ này bị bịa: mọi URL đều lấy nguyên văn từ
kết quả tìm kiếm/mở trang trong phiên nghiên cứu 11/11/2026. Hai nguồn
Instagram chỉ xem được qua bản tóm tắt của công cụ tìm kiếm — đã ghi rõ ở
trên thay vì giả vờ đã xem video.*
