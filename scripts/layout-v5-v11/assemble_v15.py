# V15 ASSEMBLE (Buoc 4+5): ghep mat da sculpt vao ban sao cua V17 ->
# layout_v18_v15.blend. Gom: (1) thay cum mat 2 tuong chinh bang luoi
# Head_face tu file lam viec (toa do world, matrix Identity); (2) truyen
# sang 2 tuong cong bang Mc thu hoi tu cap skull (kiem chung tren 3 manh
# khac, lech <= 0,002 moi truyen); (3) Phat nam: 2 net ranh nhe (mi +
# moi, <= 0,003) tren manh canvas cua chinh no; (4) Light Linking cho
# den hoc cong (receiver = cac manh tuong cong); (5) checksum ngoai pham
# vi phai GIONG HET. Ra: layout_v18_v15.blend + v15_assemble.json
import bpy, bmesh, sys, json, re, hashlib
import numpy as np
sys.path.insert(0, "/home/hatch/workspace/chua-online-work/layout")
import v15_common as C
import v15_ops as O
from mathutils import Vector, Matrix

SRC = "/home/hatch/workspace/chua-online-work/layout_v17_v141.blend"
DST = "/home/hatch/workspace/chua-online-work/layout_v18_v15.blend"
WORK = "/home/hatch/workspace/chua-online-work/layout/v15_work"
OUTJ = "/home/hatch/workspace/chua-online-work/layout/v15_assemble.json"
GLBS = {
    "dilac": "/home/hatch/workspace/chua-online-work/statues/verified_v2/di-lac.glb",
    "adida": "/home/hatch/workspace/chua-online-work/statues/verified_v2/phat-dung-adida.glb",
    "nam": "/home/hatch/workspace/chua-online-work/statues/verified_v2/phat-nam.glb",
}
MERGE_SET = {
    "dilac": ["Head_skull", "Head_cheekL", "Head_cheekR", "Head_chin",
              "Head_mouth", "Head_nose", "Head_browL", "Head_browR",
              "Head_eyeL", "Head_eyeR", "Head_creaseL", "Head_creaseR",
              "Head_smile"],
    "adida": ["Head_skull", "Head_nose", "Head_browL", "Head_browR",
              "Head_eyeL", "Head_eyeR", "Head_lidL", "Head_lidR",
              "Head_mouth", "Head_urna"],
}
SCULPT_FILE = {"dilac": f"{WORK}/dilac_head_sculpt5.blend",
               "adida": f"{WORK}/adida_head_sculpt.blend"}
LOG = {"steps": []}
def log(*a):
    s = " ".join(str(x) for x in a)
    print("[ASM]", s, flush=True)
    LOG["steps"].append(s)

def base(n):
    return re.sub(r"\.\d{3}$", "", n)

def wbox(o):
    ws = [o.matrix_world @ Vector(c) for c in o.bound_box]
    return ([min(v[i] for v in ws) for i in range(3)],
            [max(v[i] for v in ws) for i in range(3)])

def wctr(o):
    mn, mx = wbox(o)
    return Vector([(mn[i] + mx[i]) / 2 for i in range(3)])


def wverts(o):
    """Dinh THE GIOI that (ap matrix_world) — khac O.world_verts chi dung
    cho file rieng matrix Identity."""
    V = np.empty(len(o.data.vertices) * 3)
    o.data.vertices.foreach_get("co", V)
    V = V.reshape(-1, 3)
    M = np.array(o.matrix_world)
    return V @ M[:3, :3].T + M[:3, 3]

def set_wverts(o, W):
    M = np.array(o.matrix_world)
    Minv = np.linalg.inv(M)
    L = W @ Minv[:3, :3].T + Minv[:3, 3]
    o.data.vertices.foreach_set("co", L.reshape(-1).astype(np.float32))
    o.data.update()

def wnormals(o):
    N = O.vert_normals(o)
    R = np.array(o.matrix_world)[:3, :3]
    NM = np.linalg.inv(R).T
    W = N @ NM.T
    return W / np.maximum(np.linalg.norm(W, axis=1, keepdims=True), 1e-9)

def groove_world(o, path, depth, width):
    W = wverts(o)
    N = wnormals(o)
    d = O.dist_to_polyline(W, np.array(path, dtype=np.float64))
    w = np.exp(-(d / width) ** 2)
    set_wverts(o, W - N * (depth * w)[:, None])
    return float((depth * w).max())

def checksum(o):
    vs = np.empty(len(o.data.vertices) * 3)
    o.data.vertices.foreach_get("co", vs)
    h = hashlib.md5(np.round(vs.reshape(-1, 3), 4).tobytes()).hexdigest()[:12]
    mt = tuple(round(float(x), 4) for row in o.matrix_world for x in row)
    return (len(o.data.vertices), h, mt)

bpy.ops.wm.open_mainfile(filepath=SRC)
BEFORE = {o.name: checksum(o) for o in bpy.data.objects if o.type == 'MESH'}
log(f"objects before: {len(BEFORE)}")

# ---------- tim nhom tuong ----------
glb_parts = {}
imported_all = []
for key, path in GLBS.items():
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=path)
    imp = [o for o in bpy.data.objects if o not in before]
    imported_all += imp
    glb_parts[key] = {base(o.name): o for o in imp if o.type == 'MESH'}
scene_meshes = [o for o in bpy.data.objects
                if o.type == 'MESH' and o not in imported_all]

def match(key, cands):
    parts = glb_parts[key]
    return [o for o in cands
            if parts.get(base(o.name)) is not None
            and len(parts[base(o.name)].data.vertices) == len(o.data.vertices)]

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
GROUPS = {}
GROUPS["dilac"] = [o for o in match("dilac", nongate)
                   if -32 <= wctr(o).x <= -15 and -9 <= wctr(o).y <= 9]
for cl in cluster(match("adida", nongate)):
    names = {base(o.name) for o in cl}
    if "Head_ushnisha" in names and len(cl) > 40:
        GROUPS["adida"] = cl
# Phat nam: manh Head_* con lai (khong thuoc 2 tuong chinh, khong cong)
# — GLB phat-nam khop dinh lech nen match() that bai; dung vi tri.
_known = set(GROUPS.get("dilac", [])) | set(GROUPS.get("adida", []))
GROUPS["nam"] = [o for o in scene_meshes
                 if base(o.name).startswith("Head_")
                 and not o.name.startswith("V10_GateBuddha_")
                 and o not in _known]
for k, g in GROUPS.items():
    log(f"group {k}: {len(g)} pieces")
assert len(GROUPS.get("dilac", [])) > 40 and len(GROUPS.get("adida", [])) > 40

def grp_obj(key, bname):
    for o in GROUPS[key]:
        if base(o.name) == bname:
            return o
    return None

CHANGED = set(o.name for o in imported_all)

# ---------- phan tich cong TRUOC khi xoa manh chinh ----------
GATES = {}
for o in scene_meshes:
    m = re.match(r"V10_GateBuddha_(PT|TD)_(.+)$", o.name)
    if m:
        GATES.setdefault(m.group(1), {})[base(m.group(2))] = o
log("gates:", {t: len(v) for t, v in GATES.items()})
GATE_PLAN = {}
for tag, pieces in GATES.items():
    gskull = pieces.get("Head_skull")
    if gskull is None:
        GATE_PLAN[tag] = {"error": "no skull"}
        continue
    src_key = None
    for key in ("adida", "dilac"):
        mskull = grp_obj(key, "Head_skull")
        if mskull is not None and mskull.data is gskull.data:
            src_key = key
    if src_key is None:
        GATE_PLAN[tag] = {"error": "source not identified"}
        continue
    gear = pieces.get("Head_earL")
    mear = grp_obj(src_key, "Head_earL")
    Mc = np.array(gear.matrix_world) @ np.linalg.inv(np.array(mear.matrix_world))
    devs = []
    for bn in ("Head_nose", "Head_ushnisha", "Head_neck", "Head_mouth"):
        g = pieces.get(bn)
        m_ = grp_obj(src_key, bn)
        if g is not None and m_ is not None:
            pred = (Mc[:3, :3] @ wverts(m_).T).T + Mc[:3, 3]
            devs.append(round(float(np.abs(pred - wverts(g)).max()), 5))
    GATE_PLAN[tag] = {"src": src_key, "Mc": Mc, "devs": devs}
    log(f"gate {tag}: src={src_key} Mc scale~{float(np.cbrt(abs(np.linalg.det(Mc[:3, :3])))):.4f} verify devs={devs}")


# ---------- (1) thay mat tuong chinh ----------
def append_face(key):
    path = SCULPT_FILE[key]
    with bpy.data.libraries.load(path, link=False) as (src, dst):
        dst.objects = ["Head_face"]
    o = dst.objects[0]
    bpy.context.scene.collection.objects.link(o)
    o.matrix_world = Matrix.Identity(4)
    return o

new_faces = {}
for key in ("dilac", "adida"):
    face = append_face(key)
    face.name = f"V15_HeadFace_{key}"
    # gan lai vat lieu trung ten voi canh (neu co) cho sach
    scene_mats = {m.name: m for m in bpy.data.materials}
    for i, m in enumerate(list(face.data.materials)):
        if m and m.name in scene_mats and scene_mats[m.name] is not m:
            face.data.materials[i] = scene_mats[m.name]
    new_faces[key] = face
    CHANGED.add(face.name)
    targets = [grp_obj(key, bname) for bname in MERGE_SET[key]]
    n_rm = 0
    for o in targets:
        if o is not None:
            CHANGED.add(o.name)
            bpy.data.objects.remove(o, do_unlink=True)
            n_rm += 1
    log(f"{key}: face appended ({len(face.data.vertices)} verts), "
        f"removed {n_rm} old pieces")

# ---------- (2) truyen cong ----------
gate_results = {}
for tag, pieces in GATES.items():
    plan = GATE_PLAN.get(tag, {})
    if "error" in plan or not plan.get("devs") or max(plan["devs"]) > 0.002:
        gate_results[tag] = f"PLAN FAIL {plan.get('error', plan.get('devs'))}"
        log(f"gate {tag}: bo qua — {gate_results[tag]}")
        continue
    src_key = plan["src"]
    Mc = plan["Mc"]
    src_face = new_faces[src_key]
    me = src_face.data.copy()
    me.transform(Matrix(Mc.tolist()))
    go = bpy.data.objects.new(f"V10_GateBuddha_{tag}_Head_face", me)
    bpy.context.scene.collection.objects.link(go)
    CHANGED.add(go.name)
    targets = [pieces.get(bname) for bname in MERGE_SET[src_key]]
    n_rm = 0
    for o in targets:
        if o is not None:
            CHANGED.add(o.name)
            bpy.data.objects.remove(o, do_unlink=True)
            n_rm += 1
    gate_results[tag] = {"src": src_key, "removed": n_rm,
                         "face_verts": len(me.vertices),
                         "mc_dev": plan["devs"]}
    log(f"gate {tag}: face propagated ({len(me.vertices)} verts), "
        f"removed {n_rm}")

# ---------- (3) Phat nam: 2 net ----------
nam_info = "skipped"
nam = GROUPS.get("nam")
if nam:
    bymap = {base(o.name): o for o in nam}
    head_pieces = {b: o for b, o in bymap.items() if b.startswith("Head_")}
    canvas = None
    for cand in ("Head_skull", "Head_face"):
        if cand in head_pieces:
            canvas = head_pieces[cand]
    if canvas is None and head_pieces:
        canvas = max(head_pieces.values(),
                     key=lambda o: len(o.data.vertices))
    if canvas is not None:
        CHANGED.add(canvas.name)
        Minv = np.array(canvas.matrix_world).copy()
        scale_loc = float(np.cbrt(abs(np.linalg.det(Minv[:3, :3]))))
        # chia nho cuc bo quanh mat + mieng (toa do local)
        zones = []
        for bn in ("Head_eyeL", "Head_eyeR", "Head_mouth"):
            if bn in head_pieces:
                c = wctr(head_pieces[bn])
                lc = np.array(canvas.matrix_world.inverted() @ c)
                zones.append((lc, 0.30 / max(scale_loc, 1e-6)))
        if zones:
            bm = bmesh.new(); bm.from_mesh(canvas.data)
            for _ in range(2):
                esel = set()
                for fc in bm.faces:
                    cc = np.array(fc.calc_center_median())
                    if any(np.linalg.norm(cc - zc) < zr for zc, zr in zones):
                        for e in fc.edges:
                            esel.add(e)
                if esel:
                    bmesh.ops.subdivide_edges(bm, edges=list(esel), cuts=1)
            bm.to_mesh(canvas.data); bm.free()
            canvas.data.update()
        _cp = [tuple(p.vertices) for p in canvas.data.polygons]
        bvh_canvas = O.build_bvh_from_arrays([wverts(canvas)], [_cp])
        done = []
        def centerline3d(V, nbins=6):
            c = V.mean(0)
            Q = V - c
            _, _, vt = np.linalg.svd(Q, full_matrices=False)
            t = Q @ vt[0]
            order = np.argsort(t)
            bins = np.array_split(order, nbins)
            return np.array([V[b].mean(0) for b in bins if len(b)])
        for bn, depth, width in (("Head_eyeL", 0.003, 0.007),
                                 ("Head_mouth", 0.0025, 0.007)):
            if bn not in head_pieces:
                continue
            path = []
            for p in centerline3d(wverts(head_pieces[bn])):
                loc, _, _, _ = bvh_canvas.find_nearest(Vector(p))
                path.append(np.array(loc))
            groove_world(canvas, np.array(path), depth, width)
            done.append(bn)
        nam_info = {"canvas": canvas.name, "grooves": done,
                    "verts": len(canvas.data.vertices)}
        log(f"nam: {nam_info}")
LOG["nam"] = nam_info
LOG["gates"] = gate_results

# ---------- (4) Light Linking hoc cong ----------
ll_info = {}
for tag in ("PT", "TD"):
    light = bpy.data.objects.get(f"V10_NicheFill_{tag}")
    if light is None:
        ll_info[tag] = "no light"
        continue
    members = [o for o in bpy.data.objects
               if o.name.startswith(f"V10_GateBuddha_{tag}_")]
    coll = bpy.data.collections.new(f"LL_Niche_{tag}")
    for o in members:
        coll.objects.link(o)
    try:
        light.light_linking.receiver_collection = coll
        back = light.light_linking.receiver_collection
        ll_info[tag] = {"receivers": len(members),
                        "collection": back.name if back else None}
    except Exception as e:
        ll_info[tag] = f"ERROR {e}"
    log(f"light linking {tag}: {ll_info[tag]}")
LOG["light_linking"] = ll_info

# don cac object import GLB tam
for o in imported_all:
    if o.name in bpy.data.objects:
        bpy.data.objects.remove(o, do_unlink=True)

# ---------- (5) checksum ngoai pham vi ----------
AFTER = {o.name: checksum(o) for o in bpy.data.objects if o.type == 'MESH'}
diff = []
for name, cs in BEFORE.items():
    if name in CHANGED:
        continue
    if name not in AFTER:
        diff.append((name, "MISSING"))
    elif AFTER[name] != cs:
        diff.append((name, "CHANGED"))
LOG["out_of_scope_diff"] = diff
log(f"out-of-scope diff: {len(diff)} {diff[:5]}")

bpy.ops.wm.save_as_mainfile(filepath=DST)
with open(OUTJ, "w") as fp:
    json.dump(LOG, fp, indent=1, ensure_ascii=False, default=str)
ok = len(diff) == 0 and all(
    isinstance(v, dict) for v in gate_results.values()) and nam_info != "skipped"
print("V15 ASSEMBLE " + ("DONE" if ok else "PARTIAL"), flush=True)
if not ok:
    print("V15 ASSEMBLE issues:", gate_results, nam_info, "diff:", len(diff),
          flush=True)
    sys.exit(1)
