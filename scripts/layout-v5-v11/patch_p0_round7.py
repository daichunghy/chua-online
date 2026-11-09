# -*- coding: utf-8 -*-
"""P0 patch round 7 — sửa 3 ảnh bảng chữ bị rỗng trong cảnh layout
(di_lac_front / adida_plaque / phat_nam_front: filepath trống, size 0x0
-> render ra màu magenta). Trỏ lại vào statues/tex/*.png có thật + pack."""
import bpy, os

BLEND = os.path.expanduser("~/workspace/chua-online-work/layout_v5_p0.blend")
TEXD = os.path.expanduser("~/workspace/chua-online-work/statues/tex")
MAP = {
    'di_lac_front': 'di_lac_front.png',
    'adida_plaque': 'adida_plaque.png',
    'phat_nam_front': 'phat_nam_front.png',
}
for img_name, fname in MAP.items():
    im = bpy.data.images.get(img_name)
    path = os.path.join(TEXD, fname)
    assert os.path.exists(path), path
    if im is None:
        im = bpy.data.images.load(path)
        im.name = img_name
    else:
        im.filepath = path
        im.reload()
    im.pack()
    print("FIXED", img_name, "->", path, "size:", tuple(im.size),
          "packed:", bool(im.packed_file))

bpy.ops.wm.save_as_mainfile(filepath=BLEND)
print(f"SAVED {BLEND} size={os.path.getsize(BLEND)}")
print("PATCH7 DONE")
