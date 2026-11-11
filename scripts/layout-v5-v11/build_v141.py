# V14.1 BUILD — MUI A DI DA BUOC 2 (KE_HOACH_V14 muc 3 A5 + muc 4 A-b):
# buoc 1 (V14) da chan tran 1.60 -> rong mui/head_w = 0,2463 (verify V14).
# Buoc 2: noi them phan con lai ve DICH 0,272 (so do anh ref11/ref3).
# He so TINH TU SO DO TRONG SCENE: k = (0,272 * head_w) / cur_w, du kien
# ~ 0,272/0,2463 = 1,104. Cung manh, cung pivot/truc voi buoc 1 trong
# build_v14.py widen_op: A = T(pivot) · B · diag(k_side,1,1) · B^-1 ·
# T(-pivot), pivot = tam manh (pivot_back=0), co so (side, facing, up)
# cua dau. CHI ma tran object, KHONG cham mesh. CHI op mui nay: khong
# dung tai/mat/ma/mieng Di Lac (cong D-d DA DONG: khong sua mieng),
# khong dung bat ky manh nao khac. Truyen lien hop Mc sang 2 tuong hoc
# cong PT/TD nhu V13/V14.
# Cach chay: blender -b --python build_v141.py -- DRY   (chi tinh, khong ap)
#            blender -b --python build_v141.py -- BUILD (ap + luu file moi)
# Dau ra BUILD: layout_v17_v141.blend (KHONG ghi de layout_v16_v14.blend)
#               + layout/v141_audit.json
import bpy, re, json, sys
import numpy as np
from mathutils import Matrix, Vector

MODE = "DRY"
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
if argv:
    MODE = argv[0]
assert MODE in ("DRY", "BUILD"), MODE
DRY_RUN = (MODE == "DRY")

SRC = "/home/hatch/workspace/chua-online-work/layout_v16_v14.blend"
DST = "/home/hatch/workspace/chua-online-work/layout_v17_v141.blend"
assert SRC != DST
TARGET_FRAC = 0.272          # rong mui / head_w — anh ref11/ref3 (KE_HOACH_V14 A5)
PRE_FRAC_EXPECTED = 0.2463   # sau buoc 1 (verify V14 doc lap)
K_EXPECTED_RANGE = (1.05, 1.16)   # du kien ~1,104; ngoai khoang -> DUNG
NOSE_CAP = 1.60              # tran an toan thua ke (khong cham o buoc 2)
GLB_ADIDA = "/home/hatch/workspace/chua-online-work/statues/verified_v2/phat-dung-adida.glb"
GLB_DILAC = "/home/hatch/workspace/chua-online-work/statues/verified_v2/di-lac.glb"

LOG = {"steps": [], "ops": [], "mode": MODE,
       "src": SRC, "dst": DST, "target_frac": TARGET_FRAC}
def log(*a):
    s = " ".join(str(x) for x in a)
    print("[V141]", s, flush=True)
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

bpy.ops.wm.open_mainfile(filepath=SRC)

# ---- xac dinh nhom (cung phuong phap build_v14/verify_v14) ----
glb_parts = {}
imported_all = []
for key, path in {"dilac": GLB_DILAC, "adida": GLB_ADIDA}.items():
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
dilac = [p for p in match("dilac", nongate)
         if -32 <= wctr(p[0]).x <= -15 and -9 <= wctr(p[0]).y <= 9]
adida = None
for cl in cluster(match("adida", nongate)):
    if "Head_ushnisha" in {base(o.name) for o, _ in cl} and len(cl) > 40:
        adida = cl
assert len(dilac) >= 90, f"dilac group too small: {len(dilac)}"
assert adida and len(adida) >= 70, f"adida group bad: {len(adida) if adida else 0}"
log("groups: dilac", len(dilac), "adida", len(adida))
GROUPS = {"dilac": dilac, "adida": adida}

NECK_EXCLUDE = {"Head_neck", "Head_neckring0", "Head_neckring1"}
EAR_EXCLUDE = {"Head_earL", "Head_earR"}
HAND_EXCLUDE = {"HandL", "FingerL0", "FingerL1", "FingerL2"}
TARGET_PIECE = "Head_nose"

def head_bbox(pairs):
    hmn = [1e9] * 3; hmx = [-1e9] * 3
    for o, _ in pairs:
        bn = base(o.name)
        if not bn.startswith("Head_") or bn in NECK_EXCLUDE or bn in EAR_EXCLUDE:
            continue
        mn, mx = wbox(o)
        for i in range(3):
            hmn[i] = min(hmn[i], mn[i]); hmx[i] = max(hmx[i], mx[i])
    return hmn, hmx

def piece(pairs, name):
    got = [(o, g) for o, g in pairs if base(o.name) == name]
    assert len(got) == 1, f"piece {name}: found {len(got)}"
    return got[0][0]

def head_frame(pairs):
    skull = piece(pairs, "Head_skull")
    nose = piece(pairs, "Head_nose")
    sc, nc = wctr(skull), wctr(nose)
    f = Vector((nc.x - sc.x, nc.y - sc.y, 0.0))
    assert f.length > 1e-6, "facing degenerate"
    f.normalize()
    up = Vector((0, 0, 1))
    side = up.cross(f).normalized()
    return sc, side, f, up

def basis_matrix(side, f, up):
    B = Matrix.Identity(4)
    B.col[0][:3] = side
    B.col[1][:3] = f
    B.col[2][:3] = up
    return B

def make_A(pairs, o, k_side):
    """GIONG HET widen_op build_v14.py: pivot = tam manh (pivot_back=0),
    scale truc side trong co so dau."""
    _, side, f, up = head_frame(pairs)
    c = wctr(o)
    pivot = c.copy()
    B = basis_matrix(side, f, up)
    S = Matrix.Diagonal((k_side, 1.0, 1.0, 1.0))
    return (Matrix.Translation(pivot) @ B @ S @ B.inverted()
            @ Matrix.Translation(-pivot))

def predict_box(o, A):
    ws = [A @ o.matrix_world @ Vector(c) for c in o.bound_box]
    return ([min(v[i] for v in ws) for i in range(3)],
            [max(v[i] for v in ws) for i in range(3)])

# ---- snapshot an toan: tai (toan canh) + moi manh khong phai mui A Di Da ----
ear_snapshot = {}
for o in bpy.data.objects:
    if o.type == 'MESH' and base(o.name) in EAR_EXCLUDE:
        ear_snapshot[o.name] = np.array(o.matrix_world)
nose_obj = piece(adida, TARGET_PIECE)
gate_nose_names = {f"V10_GateBuddha_{t}_Head_nose" for t in ("PT", "TD")}
protected_snapshot = {}
for key, pairs in GROUPS.items():
    for o, _ in pairs:
        if o is nose_obj:
            continue
        protected_snapshot[o.name] = np.array(o.matrix_world)
for o in bpy.data.objects:
    if o.type == 'MESH' and o.name.startswith("V10_GateBuddha_") \
            and o.name not in gate_nose_names:
        protected_snapshot[o.name] = np.array(o.matrix_world)
log("protected objects (phai khong doi):", len(protected_snapshot),
    "| ears:", len(ear_snapshot))

# ---- DO + TINH HE SO (tu so do scene, khong hardcode) ----
hmn, hmx = head_bbox(adida)
head_w = hmx[0] - hmn[0]
head_h = hmx[2] - hmn[2]
mn, mx = wbox(nose_obj)
cur_w = mx[0] - mn[0]
cur_frac = cur_w / head_w
log("adida head_w", round(head_w, 4), "head_h", round(head_h, 4),
    "nose_w", round(cur_w, 4), "frac_hien_tai", round(cur_frac, 4))
assert abs(cur_frac - PRE_FRAC_EXPECTED) <= 0.006, \
    f"frac hien tai {cur_frac:.4f} lech xa sau-buoc-1 {PRE_FRAC_EXPECTED} — DUNG"
k = (TARGET_FRAC * head_w) / cur_w
assert k <= NOSE_CAP, f"k={k:.4f} vuot tran an toan"
assert K_EXPECTED_RANGE[0] <= k <= K_EXPECTED_RANGE[1], \
    f"k={k:.4f} ngoai khoang du kien {K_EXPECTED_RANGE} — DUNG, bao coordinator"
log("k buoc 2 =", round(k, 4), "(du kien ~1,104)")

A = make_A(adida, nose_obj, k)
mn1, mx1 = predict_box(nose_obj, A)
pred_frac = (mx1[0] - mn1[0]) / head_w
log("frac du doan sau buoc 2 =", round(pred_frac, 4), "dich", TARGET_FRAC)
assert abs(pred_frac - TARGET_FRAC) <= 0.004, f"du doan lech dich: {pred_frac:.4f}"
LOG["op"] = {"statue": "adida", "piece": nose_obj.name,
              "why": f"nose widen STEP2 k={k:.4f} frac {cur_frac:.4f}->{TARGET_FRAC}",
              "k": round(float(k), 5),
              "frac_pre": round(float(cur_frac), 4),
              "frac_pred": round(float(pred_frac), 4),
              "head_w": round(float(head_w), 4), "head_h": round(float(head_h), 4),
              "size_pre": [round(mx[i] - mn[i], 4) for i in range(3)],
              "size_pred": [round(mx1[i] - mn1[i], 4) for i in range(3)],
              "A": [[round(A[r][c], 5) for c in range(4)] for r in range(4)]}

if DRY_RUN:
    log("DRY: khong ap, khong luu. k =", round(k, 4), "pred frac =", round(pred_frac, 4))
    print("BUILD V141 DRY-RUN DONE", flush=True)
    sys.exit(0)

# ---- AP BUOC 2 cho tuong chinh ----
nose_obj.matrix_world = A @ nose_obj.matrix_world
bpy.context.view_layer.update()
log("da ap A cho", nose_obj.name)

# ---- Truyen lien hop Mc sang 2 cong (nhu build_v14) ----
LOG["gates"] = {}
for tag in ("PT", "TD"):
    pairs_g = []
    for o in bpy.data.objects:
        if not o.name.startswith(f"V10_GateBuddha_{tag}_"):
            continue
        s = bpy.data.objects.get(o.name[len(f"V10_GateBuddha_{tag}_"):])
        if s is not None:
            pairs_g.append((o, s))
    assert pairs_g, f"gate {tag} rong"
    ref = [p for p in pairs_g if base(p[1].name) == "Head_ushnisha"]
    assert ref, f"gate {tag}: khong co Head_ushnisha"
    Mc = ref[0][0].matrix_world @ ref[0][1].matrix_world.inverted()
    devs_pre = {}
    for o, s in pairs_g:
        if base(s.name) == TARGET_PIECE or base(s.name) in HAND_EXCLUDE:
            continue
        Mi = o.matrix_world @ s.matrix_world.inverted()
        devs_pre[s.name] = max(abs(Mi[r][c] - Mc[r][c]) for r in range(4) for c in range(4))
    mxdev = max(devs_pre.values())
    sv = np.linalg.svd(np.array(Mc)[:3, :3], compute_uv=False)
    log(f"gate {tag}: Mc_maxdev(non-nose,non-hand)={mxdev:.6f} sv={[round(float(v), 4) for v in sv]}")
    assert mxdev < 0.002, f"gate {tag} Mc khong nhat quan"
    assert abs(sv[0] - sv[2]) < 0.001, f"gate {tag} Mc khong phai dong dang deu"
    g_nose = [o for o, s in pairs_g if base(s.name) == TARGET_PIECE]
    assert len(g_nose) == 1, f"gate {tag}: nose copies = {len(g_nose)}"
    Aprime = Mc @ A @ Mc.inverted()
    g_nose[0].matrix_world = Aprime @ g_nose[0].matrix_world
    bpy.context.view_layer.update()
    mx2 = 0.0
    for o in bpy.data.objects:
        if not o.name.startswith(f"V10_GateBuddha_{tag}_"):
            continue
        s = bpy.data.objects.get(o.name[len(f"V10_GateBuddha_{tag}_"):])
        if s is None or base(s.name) in HAND_EXCLUDE:
            continue
        Mi = o.matrix_world @ s.matrix_world.inverted()
        mx2 = max(mx2, max(abs(Mi[r][c] - Mc[r][c]) for r in range(4) for c in range(4)))
    log(f"gate {tag}: Mc_maxdev SAU truyen (tru tay) = {mx2:.6f}")
    assert mx2 < 0.002, f"gate {tag} Mc vo sau truyen"
    LOG["gates"][tag] = {"parts": len(pairs_g),
                         "Mc_maxdev_pre": round(float(mxdev), 6),
                         "Mc_maxdev_post": round(float(mx2), 6),
                         "nose_propagated": g_nose[0].name}

# ---- assert an toan ----
bpy.context.view_layer.update()
for name, M0 in ear_snapshot.items():
    dev = float(np.abs(np.array(bpy.data.objects[name].matrix_world) - M0).max())
    assert dev < 1e-6, f"TAI BI DUNG: {name} dev {dev}"
worst = 0.0
for name, M0 in protected_snapshot.items():
    dev = float(np.abs(np.array(bpy.data.objects[name].matrix_world) - M0).max())
    worst = max(worst, dev)
    assert dev < 1e-6, f"MANH DUOC BAO VE BI DUNG: {name} dev {dev}"
log("assert tai + protected: KHONG DOI (worst dev", worst, ")")

# ---- don import tam + luu ----
for o in imported_all:
    bpy.data.objects.remove(o, do_unlink=True)
log("cleanup done")
bpy.ops.wm.save_as_mainfile(filepath=DST)
log("SAVED", DST)
with open("/home/hatch/workspace/chua-online-work/layout/v141_audit.json", "w") as fp:
    json.dump(LOG, fp, indent=1, ensure_ascii=False)
print("BUILD V141 DONE", flush=True)
