# V12 verify (read-only): mo file V14 tren dia, doi chieu lai tu dau.
# 1) Di Lac: 94 manh — matrix phai bang M @ W_glb (tru PlatformSlab giu nguyen),
#    kich thuoc phai bang GLB (ti le 1.000), rieng 6 manh da khoi phuc kiem ky.
# 2) Cong: tim manh nguon theo MESH DATABLOCK DUNG CHUNG (V10: d.data = p.data),
#    kiem Mc = W_copy @ W_src^-1 nhat quan + scale deu (SV bang nhau).
import bpy, re
import numpy as np
from mathutils import Vector

V14 = "/home/hatch/workspace/chua-online-work/layout_v14_v12.blend"
GLB = "/home/hatch/workspace/chua-online-work/statues/verified_v2/di-lac.glb"

def base(n):
    return re.sub(r"\.\d{3}$", "", n)

def wctr(o):
    ws = [o.matrix_world @ Vector(c) for c in o.bound_box]
    return Vector(((min(v.x for v in ws)+max(v.x for v in ws))/2,
                   (min(v.y for v in ws)+max(v.y for v in ws))/2,
                   (min(v.z for v in ws)+max(v.z for v in ws))/2))

bpy.ops.wm.open_mainfile(filepath=V14)
before = set(bpy.data.objects)
bpy.ops.import_scene.gltf(filepath=GLB)
imported = [o for o in bpy.data.objects if o not in before]
glb_parts = {base(o.name): o for o in imported if o.type == 'MESH'}

BOX = (-32, -15, -9, 9)
TOUCHED = {"Head_earL", "Head_earR", "Head_smile", "Head_cheekL", "Head_cheekR", "Torso"}
group = []
for o in bpy.data.objects:
    if o.type != 'MESH' or o in imported: continue
    c = wctr(o)
    if not (BOX[0] <= c.x <= BOX[1] and BOX[2] <= c.y <= BOX[3]): continue
    g = glb_parts.get(base(o.name))
    if g is not None and len(g.data.vertices) == len(o.data.vertices):
        group.append((o, g))
print(f"[VERIFY] group parts: {len(group)}")

Ms = [o.matrix_world @ g.matrix_world.inverted() for o, g in group if base(o.name) not in TOUCHED and base(o.name) != "PlatformSlab"]
M = Ms[0]
worst = {}
for o, g in group:
    bn = base(o.name)
    Mi = o.matrix_world @ g.matrix_world.inverted()
    d = max(abs(Mi[r][c] - M[r][c]) for r in range(4) for c in range(4))
    worst[bn] = max(worst.get(bn, 0), d)
    dr = [o.dimensions[i] / g.dimensions[i] for i in range(3) if g.dimensions[i] > 0.01]
    if bn in TOUCHED or d > 0.01 or any(abs(r - 1) > 0.005 for r in dr):
        print(f"[VERIFY] {o.name:<18} matrixDev={d:.4f} dimRatios={[round(r,4) for r in dr]} scale={[round(s,3) for s in o.scale]}")
print(f"[VERIFY] max matrixDev among untouched (excl PlatformSlab): "
      f"{max(v for k, v in worst.items() if k not in TOUCHED and k != 'PlatformSlab'):.5f}")
print(f"[VERIFY] PlatformSlab matrixDev (giu nguyen co chu dich): {worst.get('PlatformSlab', 0):.3f}")

# mesh sharing cua 6 manh da khoi phuc: chi nhom Di Lac duoc dung mesh moi
for bn in TOUCHED:
    for o, g in group:
        if base(o.name) == bn:
            users = [u.name for u in bpy.data.objects if u.type == 'MESH' and u.data == o.data]
            print(f"[VERIFY] mesh cua {o.name}: users = {users}")

# ---------- cong: khop nguon theo datablock dung chung ----------
for tag in ('PT', 'TD'):
    parts = [o for o in bpy.data.objects if o.name.startswith(f'V10_GateBuddha_{tag}_')]
    Mcs, unmatched = [], []
    for p in parts:
        srcs = [o for o in bpy.data.objects
                if o.type == 'MESH' and o.data == p.data and o is not p
                and not o.name.startswith('V10_GateBuddha_')]
        if len(srcs) == 1:
            Mcs.append(p.matrix_world @ srcs[0].matrix_world.inverted())
        else:
            unmatched.append((p.name, len(srcs)))
    if Mcs:
        Mc0 = Mcs[0]
        mx = max(abs(Mc[r][c] - Mc0[r][c]) for Mc in Mcs for r in range(4) for c in range(4))
        sv = np.linalg.svd(np.array(Mc0)[:3, :3], compute_uv=False)
        print(f"[VERIFY] gate {tag}: {len(parts)} parts, khop nguon theo datablock: {len(Mcs)}, "
              f"max Mc dev = {mx:.5f}, SV = {[round(float(v), 4) for v in sv]}, unmatched = {unmatched}")
    else:
        print(f"[VERIFY] gate {tag}: NO datablock matches; unmatched = {unmatched}")
print("VERIFY V12 DONE", flush=True)
