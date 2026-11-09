# V12 vertex audit (read-only): A Di Da + Phat Nam — doi chieu tung DINH.
# Gia dinh kiem chung: ca nhom tuong duoc dat bang MOT phep bien doi cung
# (M) — da chung minh voi Di Lac (88 manh khop tuyet doi). Neu M-dev cua
# moi manh ~0 ma tap dinh the gioi (GLB dich qua M) trung tap dinh scene
# thi mesh chua tung bi sua. Manh nao lech dinh se bi liet ke.
import bpy, re
import numpy as np
from mathutils import Vector, Matrix

F = "/home/hatch/workspace/chua-online-work/layout_v14_v12.blend"

def base(n):
    return re.sub(r"\.\d{3}$", "", n)

def wctr(o):
    ws = [o.matrix_world @ Vector(c) for c in o.bound_box]
    return ((min(v.x for v in ws)+max(v.x for v in ws))/2,
            (min(v.y for v in ws)+max(v.y for v in ws))/2)

def rounded_set(mat, verts):
    return sorted((round(v.x, 3), round(v.y, 3), round(v.z, 3))
                  for v in (mat @ v.co for v in verts))

bpy.ops.wm.open_mainfile(filepath=F)

CASES = [
    ("ADIDA", "/home/hatch/workspace/chua-online-work/statues/verified_v2/phat-dung-adida.glb", (-21, -7, -39, -23)),
    ("PHATNAM", "/home/hatch/workspace/chua-online-work/statues/verified_v2/phat-nam.glb", (-8, 22, 39, 56)),
]
for label, glbpath, box in CASES:
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=glbpath)
    imported = [o for o in bpy.data.objects if o not in before]
    glb_parts = {base(o.name): o for o in imported if o.type == 'MESH'}
    group = []
    for o in bpy.data.objects:
        if o.type != 'MESH' or o in imported: continue
        cx, cy = wctr(o)
        if not (box[0] <= cx <= box[1] and box[2] <= cy <= box[3]): continue
        g = glb_parts.get(base(o.name))
        if g is not None and len(g.data.vertices) == len(o.data.vertices):
            group.append((o, g))
    Ms = np.array([np.array(o.matrix_world @ g.matrix_world.inverted()) for o, g in group])
    med = np.median(Ms, axis=0)
    mdev = sorted(((float(np.abs(M - med).max()), o.name) for M, (o, g) in zip(Ms, group)), reverse=True)
    Mmed = Matrix(med.tolist())
    mism = []
    for o, g in group:
        vs = rounded_set(o.matrix_world, o.data.vertices)
        vg = rounded_set(Mmed @ g.matrix_world, g.data.vertices)
        if vs != vg:
            nd = sum(1 for a, b in zip(vs, vg) if a != b)
            mism.append((o.name, len(vs), nd))
    print(f"[VAUDIT {label}] parts={len(group)} M-dev top3: {[(n, round(d, 5)) for d, n in mdev[:3]]}")
    print(f"[VAUDIT {label}] vertex mismatches: {mism}")
    for o in imported:
        bpy.data.objects.remove(o, do_unlink=True)
print("VERTEX AUDIT DONE", flush=True)
