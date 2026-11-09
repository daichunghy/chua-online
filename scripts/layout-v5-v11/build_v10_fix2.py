# V10 FIX2 — hốc cổng: dời toàn bộ cụm hốc về phía NAM cho lọt vào hốc giữa
# hai trụ tầng trên (mặt trụ nam y=-39.65), tượng đứng thụt trong hốc.
# Đợt 1 đặt sai dấu: panel mặt nam -39.95 che khuất inset/tượng ở phía bắc nó.
import bpy
bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/chua-online-work/layout_v12_v10.blend")
moves = (
    ('V10_NicheBack_', +0.30),
    ('V10_NicheInset_', -0.085),
    ('V10_NicheTrim', -0.12),
    ('V10_NichePlinth_', -0.18),
    ('V10_GateBuddha_', -0.115),
)
n = 0
for o in bpy.data.objects:
    for pre, dy in moves:
        if o.name.startswith(pre):
            o.location.y += dy
            n += 1
            break
print("moved objects:", n)
bpy.ops.wm.save_as_mainfile(filepath="/home/hatch/workspace/chua-online-work/layout_v12_v10.blend")
print("FIX2 SAVED")
