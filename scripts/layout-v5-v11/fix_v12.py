# V12 FIX — hoan tra "noi ngang x1.35" tuong hoc cong (build_v10_fix3).
# FIX3 (09/11) da premultiply Mx = T(gx) @ Scale(1.35 theo X) @ T(-gx) len ca
# 64 manh V10_GateBuddha_* de "hoc cong de doc hon" — do la chinh ti le tuong
# Phat, cung mot loi voi sculpt Di Lac o V7. Vong V12 hoan tra bang phep
# nghich dao. FIX2 (dich Y) va FIX4 (xoay 180 do huong mat ra duong nhu ref6)
# la phep dat/xoay cung — GIU NGUYEN. Mx^-1 giao hoan voi FIX4 (chung truc
# x=gx) nen ap truc tiep len matrix hien tai la dung.
import bpy
import numpy as np
from mathutils import Matrix, Vector

F = "/home/hatch/workspace/chua-online-work/layout_v14_v12.blend"
bpy.ops.wm.open_mainfile(filepath=F)

for gx, tag in ((23.0, 'PT'), (45.0, 'TD')):
    Mx_inv = (Matrix.Translation((gx, 0, 0)) @ Matrix.Scale(1.0 / 1.35, 4, (1, 0, 0))
              @ Matrix.Translation((-gx, 0, 0)))
    cnt = 0
    for o in bpy.data.objects:
        if o.name.startswith(f'V10_GateBuddha_{tag}_'):
            o.matrix_world = Mx_inv @ o.matrix_world
            cnt += 1
    print(f"[V12FIX] unwidened {tag}: {cnt} parts", flush=True)
bpy.context.view_layer.update()

# kiem chung ngay: Mc phai la phep dong dang (3 SV bang nhau ~0.1953)
def wbb(o):
    ws = [o.matrix_world @ Vector(c) for c in o.bound_box]
    return (min(v.x for v in ws), max(v.x for v in ws),
            min(v.y for v in ws), max(v.y for v in ws),
            min(v.z for v in ws), max(v.z for v in ws))

for tag in ('PT', 'TD'):
    parts = [o for o in bpy.data.objects if o.name.startswith(f'V10_GateBuddha_{tag}_')]
    Mcs = []
    for p in parts:
        srcs = [o for o in bpy.data.objects
                if o.type == 'MESH' and o.data == p.data and o is not p
                and not o.name.startswith('V10_GateBuddha_')]
        if len(srcs) == 1:
            Mcs.append(np.array(p.matrix_world @ srcs[0].matrix_world.inverted()))
    Mc0 = Mcs[0]
    mx = max(float(np.abs(Mc - Mc0).max()) for Mc in Mcs)
    sv = np.linalg.svd(Mc0[:3, :3], compute_uv=False)
    los = [wbb(p) for p in parts]
    dims = (max(b[1] for b in los) - min(b[0] for b in los),
            max(b[3] for b in los) - min(b[2] for b in los),
            max(b[5] for b in los) - min(b[4] for b in los))
    print(f"[V12FIX] gate {tag}: parts={len(parts)} Mc max dev={mx:.5f} "
          f"SV={[round(float(v), 4) for v in sv]} group dims={[round(d, 2) for d in dims]}", flush=True)

bpy.ops.wm.save_as_mainfile(filepath=F)
print("FIX V12 SAVED", flush=True)
