# V15 GATE 0 — xac thuc cong do MOI (v15_common.measure_surface) tren luoi
# GOC V17 (chua hop nhat): phai tai lap bang khoa V14.1 trong <= 0,005.
# Kiem ca 2 duong: (a) do truc tiep tren tung manh; (b) do tren luoi JOIN tam
# voi nhan gan bang KDTree (dung he may se dung cho luoi hop nhat sau nay).
# Tai: do BB nhu verify cu (tai khong bao gio hop nhat).
# Dau ra: layout/v15_gate0.json. Sentinel: GATE0 V15 PASS / FAIL.
import bpy, re, sys, json
import numpy as np
sys.path.insert(0, "/home/hatch/workspace/chua-online-work/layout")
import v15_common as C
from mathutils import Vector

SRC = "/home/hatch/workspace/chua-online-work/layout_v17_v141.blend"
OUT = "/home/hatch/workspace/chua-online-work/layout/v15_gate0.json"
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
            out.append((o, g))
    return out

def cluster(pairs, thresh=3.0):
    n = len(pairs); parent = list(range(n))
    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]; i = parent[i]
        return i
    ctrs = [wctr(o) for o, _ in pairs]
    for i in range(n):
        for j in range(i + 1, n):
            if (ctrs[i].x - ctrs[j].x) ** 2 + (ctrs[i].y - ctrs[j].y) ** 2 < thresh * thresh:
                parent[find(i)] = find(j)
    groups = {}
    for i in range(n):
        groups.setdefault(find(i), []).append(pairs[i])
    return list(groups.values())

nongate = [o for o in scene_meshes if not o.name.startswith("V10_GateBuddha_")]
dilac = [p for p in match("dilac", nongate) if -32 <= wctr(p[0]).x <= -15 and -9 <= wctr(p[0]).y <= 9]
adida = None
for cl in cluster(match("adida", nongate)):
    if "Head_ushnisha" in {base(o.name) for o, _ in cl} and len(cl) > 40:
        adida = cl
GROUPS = {"dilac": dilac, "adida": adida}
print("[GATE0] groups:", {k: len(v) for k, v in GROUPS.items()}, flush=True)

RES = {"src": SRC, "groups": {}}
all_ok = True
for key, pairs in GROUPS.items():
    objs = [o for o, _ in pairs]
    head_objs = [o for o in objs if base(o.name).startswith("Head_")]
    # (a) do truc tiep: label = base name cua chinh manh
    labeled = {}
    for o in head_objs:
        lab = base(o.name)
        w = C.obj_world_verts(o)
        labeled[lab] = np.vstack([labeled[lab], w]) if lab in labeled else w
    meas_a = C.measure_surface(labeled)
    rows_a, ok_a = C.compare_table(key, meas_a, tol=0.005)
    # (b) JOIN tam + gan nhan KDTree
    kd, labels, _ = C.build_ref_cloud([(base(o.name), o) for o in head_objs])
    joined = np.vstack([C.obj_world_verts(o) for o in head_objs])
    labs = C.label_points(kd, labels, joined, max_dist=0.008)
    labeled_b = {}
    n_unlab = 0
    for p, lab in zip(joined, labs):
        if lab is None:
            n_unlab += 1
            continue
        labeled_b.setdefault(lab, []).append(p)
    labeled_b = {k: np.array(v) for k, v in labeled_b.items()}
    meas_b = C.measure_surface(labeled_b)
    rows_b, ok_b = C.compare_table(key, meas_b, tol=0.005)
    # tai BB (dinh nghia cu)
    ears = [o for o in objs if base(o.name) in C.EAR_EXCLUDE]
    head_labels = [l for l in labeled if l.startswith("Head_")
                   and l not in C.NECK_EXCLUDE and l not in C.EAR_EXCLUDE]
    allv = np.vstack([labeled[l] for l in head_labels])
    ear_rows = C.measure_ears_bb(ears, meas_a["head_h"],
                                 float(allv[:, 2].min()), float(allv[:, 2].max()))
    tgt = C.LOCKS[key]["ear"]
    ear_ok = all(abs(r["ratio"] - tgt[0]) < 0.01 and abs(r["topf"] - tgt[1]) < 0.01
                 and abs(r["lobf"] - tgt[2]) < 0.012 for r in ear_rows)
    # hieu chuan de xuat: khoa - do duong (a)
    calib = {}
    for r in rows_a:
        if r["delta"] is not None and r["delta"] > 0.005:
            calib[r["name"]] = round(r["want"] - r["got"], 4)
    g = {"n_head_pieces": len(head_objs),
         "head_pieces": sorted({base(o.name) for o in head_objs}),
         "meas_direct": meas_a, "rows_direct": rows_a, "ok_direct": ok_a,
         "meas_kdtree": meas_b, "rows_kdtree": rows_b, "ok_kdtree": ok_b,
         "unlabeled_verts": n_unlab, "n_joined_verts": int(len(joined)),
         "ears": ear_rows, "ear_ok": ear_ok,
         "calibration_needed": calib}
    RES["groups"][key] = g
    print(f"[GATE0] {key}: direct ok={ok_a} kdtree ok={ok_b} ear ok={ear_ok} "
          f"unlab={n_unlab}/{len(joined)} calib={calib}", flush=True)
    for r in rows_a:
        if not r["ok"]:
            print(f"[GATE0]   LECH(a) {r['name']}: got={r['got']} want={r['want']} d={r['delta']}", flush=True)
    for r in rows_b:
        if not r["ok"]:
            print(f"[GATE0]   LECH(b) {r['name']}: got={r['got']} want={r['want']} d={r['delta']}", flush=True)
    all_ok = all_ok and ok_a and ok_b and ear_ok and not calib

RES["verdict"] = "PASS" if all_ok else "FAIL"
with open(OUT, "w") as fp:
    json.dump(RES, fp, indent=1, ensure_ascii=False)
print(f"GATE0 V15 {RES['verdict']}", flush=True)
