# V15 MERGE v3 (Buoc 1): hop nhat cum MAT cua mot tuong trong file lam viec.
# Lo A' (da kiem chung bang diag2/diag3): weld dinh trung tung manh ->
# manh KIN union bang solver MANIFOLD (EXACT vo im lang o cap chin+mouth);
# manh MO (tam cong brow/eye/crease/smile) chuan hoa phap tuyen huong ra
# ngoai -> Solidify 0,005 offset -1 -> MANIFOLD. Lo B du phong: Join +
# Voxel Remesh 0,0055. Do lai bang nhan BE MAT (BVH pristine) — KD theo
# dinh mau bi chay mau nhan (gate1 voxel da chung minh). Gate 1 = bang
# khoa ±0,01 + tai BB + deviation. Tao REF_merged khoa truoc khi tra.
# Chay: blender -b --python merge_v15.py -- <dilac|adida>
import bpy, bmesh, sys, json, re
import numpy as np
sys.path.insert(0, "/home/hatch/workspace/chua-online-work/layout")
import v15_common as C
import v15_ops as O
from mathutils import Vector

KEY = sys.argv[sys.argv.index("--") + 1]
WORK = "/home/hatch/workspace/chua-online-work/layout/v15_work"
SRCF = f"{WORK}/{KEY}_head.blend"
DSTF = f"{WORK}/{KEY}_head_merged.blend"
OUTJ = f"/home/hatch/workspace/chua-online-work/layout/v15_{KEY}_gate1.json"
MERGE_SET = {
    "dilac": ["Head_skull", "Head_cheekL", "Head_cheekR", "Head_chin",
              "Head_mouth", "Head_nose", "Head_browL", "Head_browR",
              "Head_eyeL", "Head_eyeR", "Head_creaseL", "Head_creaseR",
              "Head_smile"],
    "adida": ["Head_skull", "Head_nose", "Head_browL", "Head_browR",
              "Head_eyeL", "Head_eyeR", "Head_lidL", "Head_lidR",
              "Head_mouth", "Head_urna"],
}
LOG = {"key": KEY, "steps": []}
def log(*a):
    s = " ".join(str(x) for x in a)
    print("[MERGE]", s, flush=True)
    LOG["steps"].append(s)

def base(n):
    return re.sub(r"\.\d{3}$", "", n)

def open_work():
    bpy.ops.wm.open_mainfile(filepath=SRCF)
    for o in list(bpy.data.objects):
        b = base(o.name)
        if b != o.name and bpy.data.objects.get(b) is None:
            o.name = b
    return {base(o.name): o for o in bpy.data.objects if o.type == 'MESH'}

def weld(o):
    bm = bmesh.new(); bm.from_mesh(o.data)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.00005)
    bm.to_mesh(o.data); bm.free()
    o.data.update()

def classify(o):
    """(closed, signed_volume) sau weld."""
    bm = bmesh.new(); bm.from_mesh(o.data)
    closed = all(len(e.link_faces) == 2 for e in bm.edges)
    vol = bm.calc_volume() if closed else 0.0
    bm.free()
    return closed, vol

def flip(o):
    bm = bmesh.new(); bm.from_mesh(o.data)
    bmesh.ops.reverse_faces(bm, faces=list(bm.faces))
    bm.to_mesh(o.data); bm.free()
    o.data.update()

def nonmanifold_ratio(o):
    bm = bmesh.new(); bm.from_mesh(o.data)
    bad = sum(1 for e in bm.edges if len(e.link_faces) != 2)
    tot = len(bm.edges)
    bm.free()
    return bad, tot

def cleanup(o):
    bm = bmesh.new(); bm.from_mesh(o.data)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0001)
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    bm.to_mesh(o.data); bm.free()
    o.data.update()

def do_union(target, other, solver='MANIFOLD'):
    mod = target.modifiers.new("u", 'BOOLEAN')
    mod.operation = 'UNION'
    mod.solver = solver
    mod.object = other
    bpy.context.view_layer.objects.active = target
    target.select_set(True)
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(other, do_unlink=True)
    return len(target.data.vertices)

# ---- tham chieu pristine: BVH co nhan mat ----
ref = np.load(f"{WORK}/ref_{KEY}.npz", allow_pickle=True)
ref_pieces = []
for k in ref.files:
    if k.endswith("__verts"):
        lab = k[:-7]
        ref_pieces.append((lab, ref[f"{lab}__verts"], ref[f"{lab}__polys"]))
piece_names = [lab for lab, _, _ in ref_pieces]
REF_DICT = {lab: v for lab, v, _ in ref_pieces}
bvh, face_labels = O.build_bvh_labeled([v for _, v, _ in ref_pieces],
                                       [p for _, _, p in ref_pieces])
log("ref pieces:", len(ref_pieces), "faces:", len(face_labels))

# Muc tieu protrusion "lo mat" (exposed): khoa V14 dem ca dinh bi chon
# trong skull (diag4: mat Di Lac chon 76-80%, protr lo mat pristine =
# 0,0040 khop so hop nhat 0,0034-0,0046). Tinh tren pristine: chi cac
# dinh nam NGOAI khoi skull moi co the lo tren be mat hop nhat.
_skull_polys = [p for lab, _, p in ref_pieces if lab == "Head_skull"][0]
_bvh_skull = O.build_bvh_from_arrays([REF_DICT["Head_skull"]], [_skull_polys])
_out = {}
for lab, V in REF_DICT.items():
    if lab == "Head_skull":
        continue
    keep = []
    for p in V:
        loc, nrm, _, _ = _bvh_skull.find_nearest(Vector(p))
        if loc is None or float((np.array(p) - np.array(loc)) @ np.array(nrm)) >= 0:
            keep.append(p)
    if keep:
        _out[lab] = np.array(keep)
EXPOSED_PROTR = C.measure_protr_ref(_out, REF_DICT)
log("exposed protr targets:", EXPOSED_PROTR)

def measure(merged):
    W = O.world_verts(merged)
    labs = O.label_by_surface(bvh, face_labels, piece_names, W)
    labeled = {}
    for p, lab in zip(W, labs):
        if lab is not None:
            labeled.setdefault(lab, []).append(p)
    labeled = {k: np.array(v) for k, v in labeled.items()}
    for o in bpy.data.objects:
        if o.type == 'MESH' and o is not merged and o.name.startswith("Head_") \
                and base(o.name) not in C.EAR_EXCLUDE \
                and base(o.name) not in C.NECK_EXCLUDE \
                and o.name != "REF_merged":
            labeled[base(o.name)] = O.world_verts(o)
    m = C.measure_surface(labeled)
    m["protr"] = C.measure_protr_ref(labeled, REF_DICT)
    return m

def gate(target):
    meas = measure(target)
    rows, ok = C.compare_table(KEY, meas, tol=0.01)
    # hang protr: muc tieu hieu dung = protr "lo mat" cua pristine (neu
    # khac khoa vi dinh bi chon); ghi ro nguon muc tieu vao tung hang.
    for r in rows:
        if r["name"].startswith("protr."):
            lab = r["name"][6:]
            exp = EXPOSED_PROTR.get(lab)
            if exp is not None and abs(exp - r["want"]) > 0.004:
                r["want_lock"] = r["want"]
                r["want"] = exp
                r["target_source"] = "exposed_pristine"
                r["delta"] = round(abs(r["got"] - exp), 4) if r["got"] is not None else None
                r["ok"] = r["got"] is not None and abs(r["got"] - exp) <= 0.01
    ok = all(r["ok"] for r in rows)
    dev = O.deviation_stats(target, bvh)
    ears = [o for o in bpy.data.objects if base(o.name) in C.EAR_EXCLUDE]
    ear_rows = C.measure_ears_bb(ears, meas["head_h"], meas["head_mn"][2],
                                 meas["head_mx"][2])
    tgt = C.LOCKS[KEY]["ear"]
    ear_ok = all(abs(r["ratio"] - tgt[0]) < 0.01 and abs(r["topf"] - tgt[1]) < 0.01
                 and abs(r["lobf"] - tgt[2]) < 0.012 for r in ear_rows)
    for r in rows:
        log(f"  {r['name']}: got={r['got']} want={r['want']} d={r['delta']} ok={r['ok']}")
    log(f"gate: table_ok={ok} ear_ok={ear_ok} dev max={dev[0]:.4f} "
        f"mean={dev[1]:.4f} p99={dev[2]:.4f} ears={ear_rows}")
    return meas, rows, ok, ear_ok, dev

def finish(target, route):
    refcopy = target.copy()
    refcopy.data = target.data.copy()
    refcopy.name = "REF_merged"
    bpy.context.scene.collection.objects.link(refcopy)
    refcopy.hide_set(True)
    refcopy.hide_render = True
    meas, rows, ok, ear_ok, dev = gate(target)
    LOG.update({"route": route, "verts_merged": len(target.data.vertices),
                "meas": meas, "rows": rows, "gate1_ok": bool(ok),
                "ear_ok": bool(ear_ok),
                "dev_vs_pristine": {"max": round(dev[0], 4),
                                    "mean": round(dev[1], 4),
                                    "p99": round(dev[2], 4)}})
    bpy.ops.wm.save_as_mainfile(filepath=DSTF)
    with open(OUTJ, "w") as fp:
        json.dump(LOG, fp, indent=1, ensure_ascii=False, default=str)
    return ok and ear_ok

# ================= LO A': MANIFOLD + SOLIDIFY =================
objs = open_work()
for nm in MERGE_SET[KEY]:
    assert nm in objs, f"thieu manh {nm} trong {SRCF}"
skull = objs["Head_skull"]
sW = O.world_verts(skull)
sc = (sW.min(0) + sW.max(0)) / 2
closed_set, open_set = [], []
for nm in MERGE_SET[KEY][1:]:
    o = objs[nm]
    weld(o)
    closed, vol = classify(o)
    if closed and vol < 0:
        flip(o)
        vol = -vol
    log(f"piece {nm}: closed={closed} vol={vol:+.4f}")
    (closed_set if closed else open_set).append(nm)
weld(skull)
target = skull
target.name = "Head_face"
route = "manifold_solidify"
broken = False
for nm in closed_set:
    nv = do_union(target, objs[nm])
    log(f"union(M) + {nm}: verts={nv}")
    if nv == 0:
        broken = True
        break
if not broken:
    for nm in open_set:
        o = objs[nm]
        # phap tuyen tam phai huong RA XA tam skull, neu khong thi dao mat
        W = O.world_verts(o)
        N = O.vert_normals(o)
        outward = W.mean(0) - sc
        if float((N.mean(0) * outward).sum()) < 0:
            flip(o)
            log(f"open {nm}: dao phap tuyen ra ngoai")
        sm = o.modifiers.new("s", 'SOLIDIFY')
        sm.thickness = 0.005
        sm.offset = -1.0
        bpy.context.view_layer.objects.active = o
        o.select_set(True)
        bpy.ops.object.modifier_apply(modifier=sm.name)
        nv = do_union(target, o)
        log(f"union(S+M) + {nm}: verts={nv}")
        if nv == 0:
            broken = True
            break
if not broken:
    cleanup(target)
    bad, tot = nonmanifold_ratio(target)
    log(f"non-manifold sau lo A': {bad}/{tot}")
    if tot and bad / tot > 0.02:
        broken = True
if not broken:
    if finish(target, route):
        print(f"V15 MERGE {KEY} DONE", flush=True)
        sys.exit(0)
    log("Gate 1 lo A' KHONG dat -> thu lo Voxel")

# ================= LO B: JOIN + VOXEL =================
log("=== LO B: join + voxel remesh 0.0055 ===")
objs = open_work()
pieces = [objs[nm] for nm in MERGE_SET[KEY]]
for p in pieces:
    weld(p)
    closed, vol = classify(p)
    if closed and vol < 0:
        flip(p)
bpy.ops.object.select_all(action='DESELECT')
for p in pieces:
    p.select_set(True)
bpy.context.view_layer.objects.active = pieces[0]
bpy.ops.object.join()
target = pieces[0]
target.name = "Head_face"
target.data.remesh_voxel_size = 0.0055
target.data.remesh_voxel_adaptivity = 0.0
bpy.ops.object.voxel_remesh()
cleanup(target)
bad, tot = nonmanifold_ratio(target)
log(f"voxel: verts={len(target.data.vertices)} non-manifold {bad}/{tot}")
if finish(target, "voxel_fallback"):
    print(f"V15 MERGE {KEY} DONE", flush=True)
else:
    print(f"V15 MERGE {KEY} GATE FAIL", flush=True)
    sys.exit(1)
