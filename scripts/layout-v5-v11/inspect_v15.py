# V15 INSPECT (read-only): kiem ke manh dau 2 tuong chinh + Phat nam + cong,
# bbox dinh-that vs bound_box (chot thiet ke cong do V15), camera, den, mai/reu,
# cay gan dien. Dau ra: layout/v15_inspect.json
import bpy, re, json
import numpy as np
from mathutils import Vector

SRC = "/home/hatch/workspace/chua-online-work/layout_v17_v141.blend"
OUT = "/home/hatch/workspace/chua-online-work/layout/v15_inspect.json"
GLBS = {
    "dilac": "/home/hatch/workspace/chua-online-work/statues/verified_v2/di-lac.glb",
    "adida": "/home/hatch/workspace/chua-online-work/statues/verified_v2/phat-dung-adida.glb",
    "nam": "/home/hatch/workspace/chua-online-work/statues/verified_v2/phat-nam.glb",
}

def base(n):
    return re.sub(r"\.\d{3}$", "", n)

def wbox_bb(o):
    ws = [o.matrix_world @ Vector(c) for c in o.bound_box]
    return ([min(v[i] for v in ws) for i in range(3)],
            [max(v[i] for v in ws) for i in range(3)])

def wbox_vx(o):
    vs = np.empty(len(o.data.vertices) * 3)
    o.data.vertices.foreach_get("co", vs)
    vs = vs.reshape(-1, 3)
    M = np.array(o.matrix_world)
    w = vs @ M[:3, :3].T + M[:3, 3]
    return w.min(axis=0).tolist(), w.max(axis=0).tolist()

def wctr(o):
    mn, mx = wbox_bb(o)
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
nam = None
for cl in cluster(match("nam", nongate)):
    if len(cl) >= 25:
        nam = cl if nam is None or len(cl) > len(nam) else nam
print("[INSP] groups: dilac", len(dilac), "adida", len(adida or []),
      "nam", len(nam or []), flush=True)

RES = {"groups": {}}
def dump_group(key, objs):
    items = []
    for o in sorted(objs, key=lambda x: x.name):
        bmn, bmx = wbox_bb(o)
        vmn, vmx = wbox_vx(o)
        delta = max(max(abs(bmn[i] - vmn[i]), abs(bmx[i] - vmx[i])) for i in range(3))
        items.append({
            "name": o.name, "base": base(o.name), "nv": len(o.data.vertices),
            "mesh": o.data.name,
            "bb": [[round(v, 4) for v in bmn], [round(v, 4) for v in bmx]],
            "vx": [[round(v, 4) for v in vmn], [round(v, 4) for v in vmx]],
            "bb_vx_delta": round(float(delta), 5),
            "ctr": [round(v, 3) for v in wctr(o)],
            "mats": [m.name if m else None for m in o.data.materials],
        })
    RES["groups"][key] = items

dump_group("dilac", dilac)
dump_group("adida", adida)
if nam:
    dump_group("nam", nam)

# cong PT/TD: ten manh + co dung chung mesh voi tuong chinh khong
gates = {}
main_mesh_names = {o.data.name for o in dilac} | {o.data.name for o in adida}
for tag in ("PT", "TD"):
    gs = [o for o in bpy.data.objects if o.name.startswith(f"V10_GateBuddha_{tag}_")]
    gates[tag] = {"n": len(gs),
                  "head_pieces": sorted(base(o.name) for o in gs
                                        if base(o.name).startswith("Head_")),
                  "shared_mesh_with_main": sum(1 for o in gs if o.data.name in main_mesh_names)}
RES["gates"] = gates

RES["cameras"] = [{"name": o.name, "lens": round(o.data.lens, 1),
                   "loc": [round(v, 2) for v in o.location]}
                  for o in bpy.data.objects if o.type == 'CAMERA']
sc = bpy.context.scene
RES["render"] = {"engine": sc.render.engine,
                 "res": [sc.render.resolution_x, sc.render.resolution_y,
                         sc.render.resolution_percentage],
                 "samples": getattr(sc.cycles, "samples", None)}
RES["lights"] = [{"name": o.name, "type": o.data.type,
                  "loc": [round(v, 2) for v in o.location],
                  "energy": getattr(o.data, "energy", None)}
                 for o in bpy.data.objects if o.type == 'LIGHT']

# mai + reu + cay: quet ten
kw = {}
for pat in ("Roof", "Mai", "Reu", "Moss", "Palm", "Dua", "Coconut", "Tree", "Cay"):
    hits = [o.name for o in bpy.data.objects
            if pat.lower() in o.name.lower() and o.type == 'MESH']
    if hits:
        kw[pat] = hits[:40]
RES["name_scan"] = kw
RES["n_objects"] = len(bpy.data.objects)
with open(OUT, "w") as fp:
    json.dump(RES, fp, indent=1, ensure_ascii=False)
print("[INSP] cameras:", [c["name"] for c in RES["cameras"]], flush=True)
print("[INSP] lights:", len(RES["lights"]), "kw:", {k: len(v) for k, v in kw.items()}, flush=True)
print("INSPECT V15 DONE", flush=True)
