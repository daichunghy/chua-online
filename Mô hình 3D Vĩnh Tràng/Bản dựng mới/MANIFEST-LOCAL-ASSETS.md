# MANIFEST — tài sản còn ở máy local (chưa lên GitHub)

Cập nhật: 09/11/2026. Các mục dưới đây CHƯA có trên repo vì giới hạn kỹ thuật của đường truyền hiện có, không phải bị bỏ quên.

## 1. File .blend của layout (quá 25 MB/file)
- `layout_v13_v11.blend` (97,9 MB — bản layout mới nhất, vòng V11) và các bản cũ `layout_v12_v10.blend` (97,2 MB), `layout_v11_v9.blend`, ... — nằm ở máy local `~/workspace/chua-online-work/`, file V13 còn có bản ở thư mục gốc work.
- Vì sao chưa lên: giao diện web GitHub giới hạn 25 MB/file; connector GitHub chỉ truyền được file text (đẩy binary qua đó sẽ hỏng thành chuỗi base64 — đã từng xảy ra 06/11); máy ảo không có đường git SSH (proxy chặn) và không có git-lfs.
- Phương án: Chung Hy đẩy từ Mac bằng git thường (98 MB < giới hạn cứng 100 MB của GitHub), hoặc Muse cấp link lưu trữ riêng khi cần.
- Script dựng lại toàn bộ các vòng nằm trong `scripts/layout-v5-v11/` trên repo (build_p0 → build_v11 + patch/fix + NOTES.md), nên mở repo là dựng/sửa tiếp được kể cả khi chưa có .blend.

## 2. Textures PBR (56 MB, CC0)
- Thư mục local `~/workspace/chua-online-work/textures/` — tải lại được theo `SOURCES-textures.md` (Poly Haven / ambientCG, CC0).

## 3. Nhân vật fitted cho scene Blender (17–18 MB/file)
- `characters_fitted/nam.glb`, `nu.glb` (đã may áo tràng), `tre.glb` ở local — bản fitted tĩnh dùng trong scene Blender.
- Bản rigged gốc (có xương + hành động, bản dùng cho web) ĐÃ có trên repo: `Thiết kế giao diện/Nhân vật 3D/Chuyển động/`.

## 4. Bản web V7 (đang kiểm nghiệm thu)
- `trai-nghiem-vinh-trang-v7.html` (17,2 MB — nhúng sẵn 3 GLB nhân vật): vượt trần 16 MiB của snapshot text; sẽ đẩy qua giao diện web sau khi nghiệm thu xong. Nguồn của nó (`v7_parts/`) ĐÃ có trên repo ở `Mô hình 3D Vĩnh Tràng/v7_parts/`.
