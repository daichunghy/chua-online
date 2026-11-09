# V10 FIX4 — tượng hốc cổng đang quay LƯNG ra đường (tượng gốc hướng bắc —
# mặt trước + biển quay vào trong chùa). Xoay 180° quanh trục đứng qua tâm
# tượng để mặt hướng nam như tượng cổng thật (ref6). Đèn fill dời lệch bên
# để tạo khối cho nếp áo.
import bpy
from mathutils import Matrix

bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/chua-online-work/layout_v12_v10.blend")
sc = bpy.context.scene
for gx, tag in ((23.0, 'PT'), (45.0, 'TD')):
    c = (gx, -39.55, 0.0)
    M = Matrix.Translation(c) @ Matrix.Rotation(3.14159265, 4, 'Z') @ Matrix.Translation((-c[0], -c[1], 0.0))
    cnt = 0
    for o in bpy.data.objects:
        if o.name.startswith(f'V10_GateBuddha_{tag}_'):
            o.matrix_world = M @ o.matrix_world
            cnt += 1
    print("rotated", tag, cnt)
    fl = bpy.data.objects.get(f'V10_NicheFill_{tag}')
    if fl:
        fl.location = (gx - 1.3, -41.3, 9.4)
        fl.data.energy = 70
        print("fill moved", tag)
bpy.ops.wm.save_as_mainfile(filepath="/home/hatch/workspace/chua-online-work/layout_v12_v10.blend")
print("FIX4 SAVED")
