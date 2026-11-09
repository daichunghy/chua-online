"""PATCH P2 v2: xoa 3 cum nam bi nhuom loi (S2-xam, path-lam + ban sao),
import lai tu GLB goc, nhuom theo luminance (giu gradient sang-toi cua vai),
dat lai dung cho. Mo layout_v7_p2.blend -> luu lai cung file."""
import bpy, math
from mathutils import Vector, Matrix
from collections import Counter

W = "/home/hatch/workspace/chua-online-work/"
CHAR_NAMES = ('geometry_0', 'Non_La', 'Tui_Vai', 'Quai_Deo', 'trang_hat', 'hoa_sen', 'khan_ran', 'Ao_Trang')

def bbox(o):
    ws = [o.matrix_world @ Vector(v) for v in o.bound_box]
    xs=[v.x for v in ws]; ys=[v.y for v in ws]; zs=[v.z for v in ws]
    return (min(xs),max(xs),min(ys),max(ys),min(zs),max(zs))

# 1. xoa 3 cum cu
targets = [(21.9, -12.7), (20.3, -33.5), (27.2, -28.3)]
removed = 0
for o in list(bpy.data.objects):
    if o.type != 'MESH' or not o.name.startswith(CHAR_NAMES):
        continue
    b = bbox(o); cx, cy = (b[0]+b[1])/2, (b[2]+b[3])/2
    if any(abs(cx-tx) < 1.3 and abs(cy-ty) < 1.3 for tx, ty in targets):
        bpy.data.objects.remove(o, do_unlink=True); removed += 1
print("removed old nam objects:", removed, flush=True)

def lum(c): return 0.2126*c[0] + 0.7152*c[1] + 0.0722*c[2]

def tint_lum(objs, target):
    for ob in objs:
        if not ob.name.startswith('geometry_0'):
            continue
        me = ob.data; ca = me.color_attributes[0]
        cols = [tuple(d.color[:3]) for d in ca.data]
        cnt = Counter(tuple(round(c/0.04) for c in col) for col in cols)
        modal = tuple(k*0.04 for k in cnt.most_common(1)[0][0])
        lm = lum(modal); changed = 0
        for d in ca.data:
            col = d.color
            cen = tuple(round(c/0.04)*0.04 for c in col[:3])
            if math.sqrt(sum((a-b)**2 for a, b in zip(cen, modal))) < 0.16 and lm > 0.01:
                f = lum(col[:3]) / lm
                d.color = (min(1, target[0]*f), min(1, target[1]*f), min(1, target[2]*f), col[3])
                changed += 1
        print(f"  tint {ob.name} modal {tuple(round(v,3) for v in modal)} -> {target}: {changed}/{len(cols)}", flush=True)

def ground_z(x, y):
    dg = bpy.context.evaluated_depsgraph_get()
    hit, loc, *_ = bpy.context.scene.ray_cast(dg, Vector((x, y, 60.0)), Vector((0, 0, -1)))
    return loc.z if (hit and loc.z < 3.0) else 0.0

def import_person(glb, target, facing, tint, tag):
    bpy.ops.import_scene.gltf(filepath=W + "characters_fitted/" + glb)
    bpy.context.view_layer.update()
    new = [o for o in bpy.context.selected_objects]
    for o in [o for o in new if o.name.lower().startswith(('ground','floor','backdrop','studio'))]:
        bpy.data.objects.remove(o, do_unlink=True); new.remove(o)
    if tint: tint_lum(new, tint)
    tops = [o for o in new if o.parent is None] or new
    ws = []
    for o in tops:
        for v in o.bound_box: ws.append(o.matrix_world @ Vector(v))
    xs=[v.x for v in ws]; ys=[v.y for v in ws]; zs=[v.z for v in ws]
    cx, cy, minz = (min(xs)+max(xs))/2, (min(ys)+max(ys))/2, min(zs)
    gz = ground_z(*target)
    delta = Vector((target[0]-cx, target[1]-cy, gz + 0.02 - minz))
    for o in tops: o.location += delta
    bpy.context.view_layer.update()
    if facing == 'N':
        C = Vector((target[0], target[1], 0))
        R = Matrix.Rotation(math.radians(180), 4, 'Z')
        for o in tops:
            o.matrix_world = (Matrix.Translation(C) @ R @ Matrix.Translation(-C)) @ o.matrix_world
    bpy.context.view_layer.update()
    print(f"person {tag} at {target} facing {facing}", flush=True)
    return tops

XAM = (0.42, 0.41, 0.40); LAM = (0.36, 0.40, 0.52)
import_person("nam.glb", (21.9, -12.7), 'N', XAM, "S2-nam-xam-v2")
master = import_person("nam.glb", (20.3, -33.5), 'S', LAM, "path-nam-lam-v2")

# ban sao linked cua nam-lam tai (27.2,-28.3), xoay them 180 -> huong N
ws = []
for o in master:
    for v in o.bound_box: ws.append(o.matrix_world @ Vector(v))
cx = (min(v.x for v in ws)+max(v.x for v in ws))/2
cy = (min(v.y for v in ws)+max(v.y for v in ws))/2
minz = min(v.z for v in ws)
T = (27.2, -28.3)
gz = ground_z(*T)
delta = Vector((T[0]-cx, T[1]-cy, gz + 0.02 - minz))
C = Vector((T[0], T[1], 0))
for o in master:
    cp = o.copy()
    bpy.context.collection.objects.link(cp)
    m = Matrix.Translation(delta) @ o.matrix_world
    m = (Matrix.Translation(C) @ Matrix.Rotation(math.radians(180), 4, 'Z') @ Matrix.Translation(-C)) @ m
    cp.matrix_world = m
bpy.context.view_layer.update()
bodies = [o for o in bpy.data.objects if o.type == 'MESH' and o.name.startswith('geometry_0')]
print("TOTAL people bodies:", len(bodies), flush=True)
bpy.ops.wm.save_as_mainfile(filepath=W + "layout_v7_p2.blend")
print("PATCH2 SAVED", flush=True)
