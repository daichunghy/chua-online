# V13 INSPECT (read-only): mo layout_v14_v12.blend, xac dinh 3 nhom tuong +
# 2 nhom cong, do ti le tai/dau TRONG SCENE (chieu Z = doc), liet ke camera.
# Khong sua gi, khong luu file. Xuat JSON: /tmp/v13/scene_audit_v14.json
import bpy, re, json
import numpy as np
from mathutils import Vector

SRC = "/home/hatch/workspace/chua-online-work/layout_v14_v12.blend"
GLBS = {
    "dilac": "/home/hatch/workspace/chua-online-work/statues/verified_v2/di-lac.glb",
    "adida": "/home/hatch/workspace/chua-online-work/statues/verified_v2/phat-dung-adida.glb",
    "nam":   "/home/hatch/workspace/chua-online-work/statues/verified_v2/phat-nam.glb",
}
OUT = {"cameras": [], "groups": {}, "gates": {}}

def base(n):
    return re.sub(r"\.\d{3}$", "", n)

def wbox(o):
    ws = [o.matrix_world @ Vector(c) for c in o.bound_box]
    mn = [min(v[i] for v in ws) for i in range(3)]
    mx = [max(v[i] for v in ws) for i in range(3)]
    return mn, mx

def wctr(o):
    mn, mx = wbox(o)
    return Vector([(mn[i] + mx[i]) / 2 for i in range(3)])

bpy.ops.wm.open_mainfile(filepath=SRC)
for o in bpy.data.objects:
    if o.type == 'CAMERA':
        OUT["cameras"].append({"name": o.name, "loc": [round(v, 2) for v in o.location],
                               "lens": round(o.data.lens, 1)})

# ---- import tam 3 GLB, lap ban do manh ----
glb_maps = {}
for key, path in GLBS.items():
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=path)
    imported = [o for o in bpy.data.objects if o not in before]
    parts = {}
    for o in imported:
        if o.type == 'MESH':
            parts[base(o.name)] = o
    glb_maps[key] = {"parts": parts, "objects": imported}
    print(f"[INSPECT] imported {key}: {len(parts)} mesh parts", flush=True)

scene_meshes = [o for o in bpy.data.objects if o.type == 'MESH'
                and all(o not in glb_maps[k]["objects"] for k in glb_maps)]

def match_group(key, candidates):
    parts = glb_maps[key]["parts"]
    out = []
    for o in candidates:
        g = parts.get(base(o.name))
        if g is not None and len(g.data.vertices) == len(o.data.vertices):
            out.append((o, g))
    return out

def cluster(pairs, thresh=3.0):
    # union-find theo khoang cach XY cua tam manh
    n = len(pairs)
    parent = list(range(n))
    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]; i = parent[i]
        return i
    ctrs = [wctr(o) for o, _ in pairs]
    for i in range(n):
        for j in range(i + 1, n):
            d = (ctrs[i].x - ctrs[j].x) ** 2 + (ctrs[i].y - ctrs[j].y) ** 2
            if d < thresh * thresh:
                parent[find(i)] = find(j)
    groups = {}
    for i in range(n):
        groups.setdefault(find(i), []).append(pairs[i])
    return list(groups.values())

def group_report(pairs):
    # M do tu tat ca manh (tru tai), kiem nhat quan
    Ms = []
    for o, g in pairs:
        if base(o.name) in ("Head_earL", "Head_earR"):
            continue
        Ms.append(o.matrix_world @ g.matrix_world.inverted())
    M = Ms[0]
    maxdev = 0.0
    for Mx in Ms:
        for r in range(4):
            for c in range(4):
                maxdev = max(maxdev, abs(Mx[r][c] - M[r][c]))
    heads = [(o, g) for o, g in pairs if base(o.name).startswith("Head_")]
    hmn = [1e9] * 3; hmx = [-1e9] * 3
    for o, _ in heads:
        mn, mx = wbox(o)
        for i in range(3):
            hmn[i] = min(hmn[i], mn[i]); hmx[i] = max(hmx[i], mx[i])
    ears = {}
    for o, _ in pairs:
        bn = base(o.name)
        if bn in ("Head_earL", "Head_earR"):
            mn, mx = wbox(o)
            ears[bn] = {"obj": o.name, "top_z": round(mx[2], 4), "bot_z": round(mn[2], 4),
                        "h": round(mx[2] - mn[2], 4), "ctr": [round(v, 3) for v in wctr(o)]}
    head_h = hmx[2] - hmn[2]
    rep = {"parts": len(pairs), "M_translation": [round(v, 3) for v in M.translation],
           "M_maxdev": round(maxdev, 5),
           "head_top_z": round(hmx[2], 4), "head_bot_z": round(hmn[2], 4),
           "head_h": round(head_h, 4),
           "head_ctr_xy": [round((hmn[0] + hmx[0]) / 2, 3), round((hmn[1] + hmx[1]) / 2, 3)],
           "ears": ears}
    for bn, e in ears.items():
        rep[f"{bn}_ratio"] = round(e["h"] / head_h, 4)
        rep[f"{bn}_topfrac"] = round((hmx[2] - e["top_z"]) / head_h, 4)
        rep[f"{bn}_lobefrac"] = round((e["bot_z"] - hmn[2]) / head_h, 4)  # >0: day tai tren cam; <0: duoi cam
    return rep

# ---- Di Lac: phuong phap hop V12 ----
dilac_pairs = match_group("dilac", [o for o in scene_meshes
                                    if not o.name.startswith("V10_GateBuddha_")])
dl = [p for p in dilac_pairs if -32 <= wctr(p[0]).x <= -15 and -9 <= wctr(p[0]).y <= 9]
OUT["groups"]["dilac"] = group_report(dl)
print("[INSPECT] dilac:", json.dumps(OUT["groups"]["dilac"]), flush=True)

# ---- A Di Da: cluster cac ung vien ----
ad = match_group("adida", [o for o in scene_meshes if not o.name.startswith("V10_GateBuddha_")])
for cl in cluster(ad):
    names = {base(o.name) for o, _ in cl}
    if "Head_ushnisha" in names and len(cl) > 40:
        OUT["groups"]["adida"] = group_report(cl)
        print("[INSPECT] adida cluster parts:", len(cl), flush=True)
print("[INSPECT] adida:", json.dumps(OUT["groups"].get("adida")), flush=True)

# ---- Phat nam: chi ghi so lieu dau/tai de doi chieu ----
nm = match_group("nam", [o for o in scene_meshes if not o.name.startswith("V10_GateBuddha_")])
for cl in cluster(nm, thresh=4.0):
    names = {base(o.name) for o, _ in cl}
    if "Head_ushnisha" in names and len(cl) > 20:
        OUT["groups"]["nam"] = group_report(cl)
        print("[INSPECT] nam cluster parts:", len(cl), flush=True)
print("[INSPECT] nam:", json.dumps(OUT["groups"].get("nam")), flush=True)

# ---- Cong: Mc + tai ----
for tag in ("PT", "TD"):
    devs = []
    ear_objs = []
    head_objs = []
    for o in bpy.data.objects:
        if not o.name.startswith(f"V10_GateBuddha_{tag}_"):
            continue
        srcname = o.name[len(f"V10_GateBuddha_{tag}_"):]
        s = bpy.data.objects.get(srcname)
        if s is None:
            continue
        devs.append((o, s))
        if base(srcname) in ("Head_earL", "Head_earR"):
            ear_objs.append((o, s))
        if base(srcname).startswith("Head_"):
            head_objs.append(o)
    Mc = devs[0][0].matrix_world @ devs[0][1].matrix_world.inverted()
    mx = max(abs((o.matrix_world @ s.matrix_world.inverted())[r][c] - Mc[r][c])
             for o, s in devs for r in range(4) for c in range(4))
    sv = np.linalg.svd(np.array(Mc)[:3, :3], compute_uv=False)
    g = {"parts": len(devs), "Mc_maxdev": round(float(mx), 6),
         "singular": [round(float(v), 4) for v in sv],
         "ear_objs": [o.name for o, _ in ear_objs]}
    if head_objs:
        hmn = [1e9] * 3; hmx = [-1e9] * 3
        for o in head_objs:
            mn, mx2 = wbox(o)
            for i in range(3):
                hmn[i] = min(hmn[i], mn[i]); hmx[i] = max(hmx[i], mx2[i])
        g["gate_head_h"] = round(hmx[2] - hmn[2], 4)
        g["gate_head_top_z"] = round(hmx[2], 4)
        g["gate_head_bot_z"] = round(hmn[2], 4)
        for o, s in ear_objs:
            mn, mx2 = wbox(o)
            g[f"ear_{base(s.name)}_h"] = round(mx2[2] - mn[2], 4)
            g[f"ear_{base(s.name)}_top_z"] = round(mx2[2], 4)
            g[f"ear_{base(s.name)}_bot_z"] = round(mn[2], 4)
    OUT["gates"][tag] = g
    print(f"[INSPECT] gate {tag}:", json.dumps(g), flush=True)

with open("/tmp/v13/scene_audit_v14.json", "w") as f:
    json.dump(OUT, f, indent=1, ensure_ascii=False)
print("INSPECT DONE", flush=True)
