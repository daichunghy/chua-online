# V12 NN-distance check (read-only): cac manh A Di Da bi co dinh lech —
# do khoang cach dinh-gan-nhat hai chieu giua scene va GLB (qua M nhom).
# Jitter so hoc: max <= ~2mm. Sua that: co dinh lech hang cm.
import bpy, re
import numpy as np
from mathutils import Vector, Matrix, kdtree

F = "/home/hatch/workspace/chua-online-work/layout_v14_v12.blend"
GLB = "/home/hatch/workspace/chua-online-work/statues/verified_v2/phat-dung-adida.glb"
TARGETS = ['FingerL0', 'FingerL2', 'HandL', 'HandR', 'FootL', 'FootR',
           'Head_earL', 'Head_earR', 'Head_skull', 'Lotus_t2_1']

def base(n):
    return re.sub(r"\.\d{3}$", "", n)

def wverts(o, mat=None):
    m = mat or o.matrix_world
    return [m @ v.co for v in o.data.vertices]

bpy.ops.wm.open_mainfile(filepath=F)
before = set(bpy.data.objects)
bpy.ops.import_scene.gltf(filepath=GLB)
imported = [o for o in bpy.data.objects if o not in before]
glb_parts = {base(o.name): o for o in imported if o.type == 'MESH'}

# M nhom tu 5 manh lon bat ky trong cum adida
refs = []
for o in bpy.data.objects:
    if o.type != 'MESH' or o in imported: continue
    g = glb_parts.get(base(o.name))
    if g is None: continue
    ws = [o.matrix_world @ Vector(c) for c in o.bound_box]
    cx = (min(v.x for v in ws) + max(v.x for v in ws)) / 2
    cy = (min(v.y for v in ws) + max(v.y for v in ws)) / 2
    if -21 <= cx <= -7 and -39 <= cy <= -23 and len(o.data.vertices) == len(g.data.vertices):
        refs.append(o.matrix_world @ g.matrix_world.inverted())
M = refs[0]
print("[NN] group parts referenced:", len(refs))

def nn_stats(a_pts, b_pts):
    kd = kdtree.KDTree(len(b_pts))
    for i, p in enumerate(b_pts):
        kd.insert(p, i)
    kd.balance()
    ds = [kd.find(p)[2] for p in a_pts]
    ds = np.array(ds)
    return ds.max(), ds.mean()

for t in TARGETS:
    so = next((o for o in bpy.data.objects
               if o.type == 'MESH' and o not in imported and base(o.name) == t
               and -21 <= (lambda ws: (min(v.x for v in ws) + max(v.x for v in ws)) / 2)([o.matrix_world @ Vector(c) for c in o.bound_box]) <= -7), None)
    g = glb_parts.get(t)
    if so is None or g is None:
        print(f"[NN] {t}: not found"); continue
    sp = wverts(so)
    gp = wverts(g, M @ g.matrix_world)
    mx1, mn1 = nn_stats(sp, gp)
    mx2, mn2 = nn_stats(gp, sp)
    print(f"[NN] {t:<12} scene->glb max={mx1*1000:.2f}mm mean={mn1*1000:.3f}mm | glb->scene max={mx2*1000:.2f}mm mean={mn2*1000:.3f}mm")
print("NN CHECK DONE", flush=True)
