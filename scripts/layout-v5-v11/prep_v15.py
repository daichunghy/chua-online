# V15 PREP: tu V17 trich cum dau Di Lac + A Di Da ra 2 file lam viec rieng
# (bake world transform -> toa do scene, matrix = Identity, ten = base name),
# dong thoi dump may diem + polygon pristine ra npz lam tham chieu do/deviation.
# Dau ra: layout/v15_work/{dilac_head.blend, adida_head.blend, ref_dilac.npz,
# ref_adida.npz}. Sentinel: V15 PREP DONE
import bpy, re, json, sys
import numpy as np
sys.path.insert(0, "/home/hatch/workspace/chua-online-work/layout")
import v15_common as C
from mathutils import Vector

SRC = "/home/hatch/workspace/chua-online-work/layout_v17_v141.blend"
WORK = "/home/hatch/workspace/chua-online-work/layout/v15_work"
GLBS = {
    "dilac": "/home/hatch/workspace/chua-online-work/statues/verified_v2/di-lac.glb",
    "adida": "/home/hatch/workspace/chua-online-work/statues/verified_v2/phat-dung-adida.glb",
}

def base(n):
    return re.sub(r"\.\d{3}$", "", n)

def wbox(o):
    ws = [o.matrix_world @ Vector(c) for c in o.bound_box]
    return ([min(v[i] for v in ws) for i in range(3)],
            [max(v[i] for v in ws) for i in range(3)])

def wctr(o):
    mn, mx = wbox(o)
    return Vector([(mn[i] + mx[i]) / 2 for i in range(3)])

bpy.ops.wm.open_mainfile(filepath=SRC)
glb_parts = {}
imported_all = []
for key, path in GLBS.items():
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=path)
    imp = [o for o in bpy.data.objects if o not in before]
    imported_all += imp
    glb_parts[key] = {base(o.name): o for o in imp if o.type == 'MESH'}
scene_meshes = [o for o in bpy.data.objects if o.type == 'MESH' and o not in imported_all]

def match(key, cands):
    parts = glb_parts[key]
    out = []
    for o in cands:
        g = parts.get(base(o.name))
        if g is not None and len(g.data.vertices) == len(o.data.vertices):
            out.append(o)
    return out

def cluster(objs, thresh=3.0):
    n = len(objs); parent = list(range(n))
    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]; i = parent[i]
        return i
    ctrs = [wctr(o) for o in objs]
    for i in range(n):
        for j in range(i + 1, n):
            if (ctrs[i].x - ctrs[j].x) ** 2 + (ctrs[i].y - ctrs[j].y) ** 2 < thresh * thresh:
                parent[find(i)] = find(j)
    groups = {}
    for i in range(n):
        groups.setdefault(find(i), []).append(objs[i])
    return list(groups.values())

nongate = [o for o in scene_meshes if not o.name.startswith("V10_GateBuddha_")]
dilac = [o for o in match("dilac", nongate) if -32 <= wctr(o).x <= -15 and -9 <= wctr(o).y <= 9]
adida = None
for cl in cluster(match("adida", nongate)):
    if "Head_ushnisha" in {base(o.name) for o in cl} and len(cl) > 40:
        adida = cl
GROUPS = {"dilac": dilac, "adida": adida}

for key, objs in GROUPS.items():
    head = [o for o in objs if base(o.name).startswith("Head_")]
    assert len(head) >= 15, f"{key}: chi {len(head)} manh dau"
    # --- dump npz tham chieu (label -> verts the gioi + polys) ---
    store = {}
    for o in head:
        lab = base(o.name)
        W = C.obj_world_verts(o)
        polys = [tuple(p.vertices) for p in o.data.polygons]
        if f"{lab}__verts" in store:
            # trung base name: noi them (polys offset)
            off = len(store[f"{lab}__verts"])
            store[f"{lab}__verts"] = np.vstack([store[f"{lab}__verts"], W])
            store[f"{lab}__polys"] = np.array(
                list(store[f"{lab}__polys"]) + [tuple(i + off for i in p) for p in polys],
                dtype=object)
        else:
            store[f"{lab}__verts"] = W
            store[f"{lab}__polys"] = np.array(polys, dtype=object)
    np.savez_compressed(f"{WORK}/ref_{key}.npz", **store)
    print(f"[PREP] ref_{key}.npz: {len(head)} manh, "
          f"{sum(len(v) for k2, v in store.items() if k2.endswith('__verts'))} dinh", flush=True)
    # --- tao file lam viec: copy tung manh dau, bake world transform ---
    new_objs = []
    for o in head:
        me = o.data.copy()
        me.transform(o.matrix_world)
        no = bpy.data.objects.new(base(o.name), me)
        bpy.context.scene.collection.objects.link(no)
        new_objs.append(no)
    keep = set(new_objs)
    for o in list(bpy.data.objects):
        if o not in keep:
            bpy.data.objects.remove(o, do_unlink=True)
    out = f"{WORK}/{key}_head.blend"
    bpy.ops.wm.save_as_mainfile(filepath=out)
    print(f"[PREP] saved {out} ({len(new_objs)} objects)", flush=True)
    # mo lai V17 cho tuong tiep theo
    if key == "dilac":
        bpy.ops.wm.open_mainfile(filepath=SRC)
        # phai tim lai nhom adida trong file vua mo lai: don gian hoa bang
        # cach dung lai logic — nhung objects da thay; chay lai tu dau:
        glb_parts2 = {}
        imported2 = []
        for k2, path in GLBS.items():
            before = set(bpy.data.objects)
            bpy.ops.import_scene.gltf(filepath=path)
            imp = [o for o in bpy.data.objects if o not in before]
            imported2 += imp
            glb_parts2[k2] = {base(o.name): o for o in imp if o.type == 'MESH'}
        sm = [o for o in bpy.data.objects if o.type == 'MESH' and o not in imported2]
        ng = [o for o in sm if not o.name.startswith("V10_GateBuddha_")]
        def match2(key2, cands):
            parts = glb_parts2[key2]
            return [o for o in cands if parts.get(base(o.name)) is not None
                    and len(parts[base(o.name)].data.vertices) == len(o.data.vertices)]
        adida2 = None
        for cl in cluster(match2("adida", ng)):
            if "Head_ushnisha" in {base(o.name) for o in cl} and len(cl) > 40:
                adida2 = cl
        GROUPS["adida"] = adida2
print("V15 PREP DONE", flush=True)
