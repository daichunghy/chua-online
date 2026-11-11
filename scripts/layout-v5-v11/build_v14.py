# V14 BUILD (NHAP — CHUA CHAY BUILD) — NAN MAT TUONG CHI TIET VE PHIA ANH THAT.
# Can cu do: layout/KE_HOACH_V14.md + v14_measure/v14_face_measure.json.
# Nguyen tac (ke thua V13): CHI ma tran object (z'=... tong quat hoa thanh
# A = T · B · T^-1 quanh tam manh, B = scale huong trong co so (side, facing,
# up)); KHONG cham mesh; KHONG dung tai/than/be/ti le tong; moi he so TINH
# TU SO DO trong file nay, khong hardcode so doan.
# DRY_RUN = True (mac dinh cua ban nhap): chi mo file, xac dinh nhom, tinh
# he so + du doan ti le sau sua tu bbox, in ra, KHONG ap, KHONG luu.
# Khi thi cong that: chay measure_v14.py truoc (giai doan 0), doi
# DRY_RUN = False, chay, roi chay verify_v14.py doc lap.
# DAU RA khi chay that: layout_v16_v14.blend (TUYET DOI khong ghi de
# layout_v15_v13.blend) + layout/v14_audit.json.
import bpy, re, json, math
import numpy as np
from mathutils import Matrix, Vector

DRY_RUN = False

SRC = "/home/hatch/workspace/chua-online-work/layout_v15_v13.blend"
DST = "/home/hatch/workspace/chua-online-work/layout_v16_v14.blend"
assert SRC != DST
GLBS = {
    "dilac": "/home/hatch/workspace/chua-online-work/statues/verified_v2/di-lac.glb",
    "adida": "/home/hatch/workspace/chua-online-work/statues/verified_v2/phat-dung-adida.glb",
}

# ---- MUC TIEU DO TU ANH THAT (v14_face_measure.json) ----
TARGETS = {
    # Di Lac: rong mui / head_w anh = 0.250 (model 0.170)
    "dilac_nose_w_frac": 0.250,
    # A Di Da: rong mui / head_w anh = 0.272 (model 0.154); tran an toan 1.60
    "adida_nose_w_frac": 0.272,
    "nose_widen_cap": 1.60,
    # Do noi dich cho cac manh dang ONG (may/mat/mi/crease/mieng A Di Da):
    # <= +0.020 head_h (relief sat mat nhu anh); he so ep det truc sau suy tu
    # do noi do duoc, tran duoi 0.35 de khong xep manh thanh phang.
    "protr_target_frac": 0.020,
    "flatten_min_k": 0.35,
}
LOG = {"steps": [], "ops": [], "dry_run": DRY_RUN}
def log(*a):
    s = " ".join(str(x) for x in a)
    print("[V14]", s, flush=True)
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

# ---- import tam + xac dinh nhom (cung phuong phap build_v13/inspect_v13) ----
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
dl_all = match("dilac", nongate)
dilac = [p for p in dl_all if -32 <= wctr(p[0]).x <= -15 and -9 <= wctr(p[0]).y <= 9]
adida = None
for cl in cluster(match("adida", nongate)):
    if "Head_ushnisha" in {base(o.name) for o, _ in cl} and len(cl) > 40:
        adida = cl
assert len(dilac) >= 90, f"dilac group too small: {len(dilac)}"
assert adida and len(adida) >= 70, f"adida group bad: {len(adida) if adida else 0}"
log("groups: dilac", len(dilac), "adida", len(adida))
GROUPS = {"dilac": dilac, "adida": adida}

# DINH NGHIA DAU: giong het V13 (cam -> dinh, loai co + tai khoi mau so).
NECK_EXCLUDE = {"Head_neck", "Head_neckring0", "Head_neckring1"}
EAR_EXCLUDE = {"Head_earL", "Head_earR"}
HAND_EXCLUDE = {"HandL", "FingerL0", "FingerL1", "FingerL2"}  # lech Mc san co tu V14/V12
FACE_PIECES = {
    "dilac": {"Head_browL", "Head_browR", "Head_eyeL", "Head_eyeR",
              "Head_nose", "Head_cheekL", "Head_cheekR",
              "Head_creaseL", "Head_creaseR", "Head_mouth", "Head_smile"},
    "adida": {"Head_browL", "Head_browR", "Head_eyeL", "Head_eyeR",
              "Head_lidL", "Head_lidR", "Head_nose", "Head_mouth", "Head_urna"},
}

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
    """Co so (side, facing, up) cua dau trong world: up = +Z the gioi;
    facing = huong ngang tu tam so toi tam mui (chuan hoa, bo thanh phan Z);
    side = up x facing."""
    skull = piece(pairs, "Head_skull")
    nose = piece(pairs, "Head_nose")
    sc, nc = wctr(skull), wctr(nose)
    f = Vector((nc.x - sc.x, nc.y - sc.y, 0.0))
    assert f.length > 1e-6, "facing degenerate"
    f.normalize()
    up = Vector((0, 0, 1))
    side = up.cross(f).normalized()
    return sc, side, f, up

def ellipsoid_protr(pairs, o):
    """Do noi cua manh o so voi ellipsoid so (bbox Head_skull), do doc
    truc facing qua tam manh. Tra (protr_m, front_pt, skull_ctr)."""
    skull = piece(pairs, "Head_skull")
    smn, smx = wbox(skull)
    sc, side, f, up = head_frame(pairs)
    radii = Vector(((smx[0] - smn[0]) / 2, (smx[1] - smn[1]) / 2, (smx[2] - smn[2]) / 2))
    # ban kinh ellipsoid theo 3 truc world xap xi tu bbox (so doi xung truc)
    c = wctr(o)
    d = c - sc
    # toa do tam manh trong co so (side, facing, up) tu tam so
    u = d.dot(side) / radii.x if radii.x else 0.0
    v = d.z / radii.z if radii.z else 0.0
    t = 1.0 - u * u - v * v
    mn, mx = wbox(o)
    # diem truoc nhat cua manh doc facing: chieu bbox len facing
    corners = [o.matrix_world @ Vector(cc) for cc in o.bound_box]
    front = max((p - sc).dot(f) for p in corners)
    if t <= 0:
        return float("nan"), front, sc
    surf = math.sqrt(t) * radii.y  # ban kinh facing cua ellipsoid ~ radii.y
    return front - surf, front, sc

def basis_matrix(side, f, up):
    B = Matrix.Identity(4)
    B.col[0][:3] = side
    B.col[1][:3] = f
    B.col[2][:3] = up
    return B

def make_A(pairs, o, k_side=1.0, k_face=1.0, sink=0.0, pivot_back=0.0):
    """A = T(-sink*f) · T(pivot) · B · diag(k_side,k_face,1) · B^-1 · T(-pivot).
    pivot = tam manh lui pivot_back doc -facing (pivot_back=0.5*depth
    -> pivot o mat sau manh, mat truoc co ve phia mat)."""
    _, side, f, up = head_frame(pairs)
    c = wctr(o)
    mn, mx = wbox(o)
    depth = max((Vector(cc) - c).dot(f) * 2 for cc in
                [o.matrix_world @ Vector(x) for x in o.bound_box])
    pivot = c - f * (pivot_back * depth)
    B = basis_matrix(side, f, up)
    S = Matrix.Diagonal((k_side, k_face, 1.0, 1.0))
    A = (Matrix.Translation(-sink * f) @ Matrix.Translation(pivot) @ B @ S
         @ B.inverted() @ Matrix.Translation(-pivot))
    return A

def predict_box(o, A):
    ws = [A @ o.matrix_world @ Vector(c) for c in o.bound_box]
    return ([min(v[i] for v in ws) for i in range(3)],
            [max(v[i] for v in ws) for i in range(3)])

# ---- ghi ma tran tai goc de assert khong dung (ca chinh + cong) ----
ear_snapshot = {}
for o in bpy.data.objects:
    if o.type == 'MESH' and base(o.name) in EAR_EXCLUDE:
        ear_snapshot[o.name] = np.array(o.matrix_world)
nonface_snapshot = {}
for key, pairs in GROUPS.items():
    for o, _ in pairs:
        if base(o.name) not in FACE_PIECES[key]:
            nonface_snapshot[o.name] = np.array(o.matrix_world)

ADJ = {"dilac": {}, "adida": {}}   # base_name -> A (world, tuong chinh)
OPS = []

def register_op(key, name, A, why):
    pairs = GROUPS[key]
    o = piece(pairs, name)
    mn0, mx0 = wbox(o)
    mn1, mx1 = predict_box(o, A)
    rec = {"statue": key, "piece": o.name, "why": why,
           "size_pre": [round(mx0[i] - mn0[i], 4) for i in range(3)],
           "size_pred": [round(mx1[i] - mn1[i], 4) for i in range(3)],
           "A": [[round(A[r][c], 5) for c in range(4)] for r in range(4)]}
    OPS.append(rec)
    ADJ[key][name] = A
    log("OP", key, o.name, why)
    if not DRY_RUN:
        o.matrix_world = A @ o.matrix_world

def flatten_op(key, name):
    """Op D-a/A-a: ep det truc sau + ha chim de do noi ve <= muc tieu.
    He so suy tu do noi do duoc (ellipsoid), khong doan."""
    pairs = GROUPS[key]
    o = piece(pairs, name)
    hmn, hmx = head_bbox(pairs)
    head_h = hmx[2] - hmn[2]
    protr, front, sc = ellipsoid_protr(pairs, o)
    assert protr == protr, f"{key} {name}: tam manh ngoai ellipsoid, khong do duoc do noi"
    tgt = TARGETS["protr_target_frac"] * head_h
    if protr <= tgt:
        log("SKIP flatten", key, name, "protr da dat", round(protr, 4))
        return
    # do sau manh doc facing (tu bbox chieu len facing)
    _, side, f, up = head_frame(pairs)
    corners = [o.matrix_world @ Vector(x) for x in o.bound_box]
    c = wctr(o)
    depth = max((p - c).dot(f) for p in corners) - min((p - c).dot(f) for p in corners)
    k = max(TARGETS["flatten_min_k"], 1.0 - (protr - tgt) / max(depth, 1e-6))
    sink = max(0.0, (protr - tgt) - (1.0 - k) * depth / 2)
    A = make_A(pairs, o, k_face=k, sink=sink, pivot_back=0.5)
    register_op(key, name, A, f"flatten protr {protr:.3f}->{tgt:.3f} k={k:.3f} sink={sink:.3f}")

def widen_op(key, name, target_frac):
    """Op D-b/A-b: nong rong ngang mui ve ti le anh. He so = (ti le dich x
    head_w) / rong do duoc; chan tren boi nose_widen_cap (an toan)."""
    pairs = GROUPS[key]
    o = piece(pairs, name)
    hmn, hmx = head_bbox(pairs)
    head_w = hmx[0] - hmn[0]
    mn, mx = wbox(o)
    cur_w = mx[0] - mn[0]
    k = (target_frac * head_w) / cur_w
    k = min(k, TARGETS["nose_widen_cap"])
    log("widen", key, name, "cur_w", round(cur_w, 4), "k", round(k, 4))
    A = make_A(pairs, o, k_side=k, pivot_back=0.0)
    register_op(key, name, A, f"nose widen k={k:.3f} -> frac {target_frac}")

# ================= CAC OP THEO KE HOACH (muc 4) =================
# Di Lac
for nm in ("Head_browL", "Head_browR", "Head_eyeL", "Head_eyeR",
           "Head_creaseL", "Head_creaseR"):
    flatten_op("dilac", nm)
widen_op("dilac", "Head_nose", TARGETS["dilac_nose_w_frac"])
# Ma Di Lac: chi ep det truc sau quanh pivot mat sau, KHONG sink, KHONG scale ngang/doc
# HIEU CHINH VONG 2 (do lai sau vong 1, xem NOTES V14): k=0.60 quanh pivot
# o MAT SAU manh lam mat truoc lui (1-k)*depth = 0,4*0,5137 = 0,205 m ->
# do noi sau ep -0,0023 (qua dich +0,10 cua ke hoach). Dich lui 0,103 m
# -> (1-k) = 0,103/0,5137 = 0,20 -> k = 0,80; do noi du doan ~ +0,100.
for nm in ("Head_cheekL", "Head_cheekR"):
    pairs = GROUPS["dilac"]
    o = piece(pairs, nm)
    A = make_A(pairs, o, k_face=0.80, sink=0.0, pivot_back=0.5)
    register_op("dilac", nm, A, "cheek deflate k_face=0.80 pivot sau (hieu chinh vong 2)")

# A Di Da
for nm in ("Head_browL", "Head_browR", "Head_lidL", "Head_lidR",
           "Head_eyeL", "Head_eyeR", "Head_mouth", "Head_urna"):
    flatten_op("adida", nm)
widen_op("adida", "Head_nose", TARGETS["adida_nose_w_frac"])

# ===== CONG D-d (V14.1, MAC DINH TAT): dich mieng Di Lac theo chieu doc.
# Chi mo khi render goc chup ref5 + do lai tren render xac nhan lech > 7%
# (xem KE_HOACH_V14 muc 4 D-d). Cach tinh khi mo: dz = (frac_anh - frac_model)
# * head_h tren truc Z the gioi, ap cho ca Head_mouth + Head_smile.
# if False:
#     dz = ...
#     A = Matrix.Translation((0, 0, dz))
#     for nm in ("Head_mouth", "Head_smile"):
#         register_op("dilac", nm, A, "gate D-d: mouth vertical shift")

# ---- cong: truyen A cua A Di Da qua phep dong dang Mc (giong V13) ----
# CHI chay khi DRY_RUN = False. Ban nhap chi kiem tra cau truc: liet ke
# manh cong + manh mat co mat trong ADJ["adida"].
for tag in ("PT", "TD"):
    pairs_g = []
    for o in bpy.data.objects:
        if not o.name.startswith(f"V10_GateBuddha_{tag}_"):
            continue
        s = bpy.data.objects.get(o.name[len(f"V10_GateBuddha_{tag}_"):])
        if s is not None:
            pairs_g.append((o, s))
    assert pairs_g, f"gate {tag} rong"
    face_here = [base(s.name) for _, s in pairs_g if base(s.name) in ADJ["adida"]]
    log(f"gate {tag}: parts={len(pairs_g)} face pieces se truyen: {sorted(face_here)}")
    if DRY_RUN:
        continue
    ref = [p for p in pairs_g if base(p[1].name) == "Head_ushnisha"]
    assert ref, f"gate {tag}: khong co Head_ushnisha"
    Mc = ref[0][0].matrix_world @ ref[0][1].matrix_world.inverted()
    devs_pre = {}
    for o, s in pairs_g:
        if base(s.name) in FACE_PIECES["adida"] or base(s.name) in HAND_EXCLUDE:
            continue  # manh mat se doi co chu dich; tay lech san co
        Mi = o.matrix_world @ s.matrix_world.inverted()
        devs_pre[s.name] = max(abs(Mi[r][c] - Mc[r][c]) for r in range(4) for c in range(4))
    mx = max(devs_pre.values())
    sv = np.linalg.svd(np.array(Mc)[:3, :3], compute_uv=False)
    log(f"gate {tag}: Mc_maxdev(non-face,non-hand)={mx:.6f} sv={[round(float(v), 4) for v in sv]}")
    assert mx < 0.002, f"gate {tag} Mc khong nhat quan"
    assert abs(sv[0] - sv[2]) < 0.001, f"gate {tag} Mc khong phai dong dang deu"
    for o, s in pairs_g:
        bn = base(s.name)
        if bn in ADJ["adida"]:
            Aprime = Mc @ ADJ["adida"][bn] @ Mc.inverted()
            o.matrix_world = Aprime @ o.matrix_world
    bpy.context.view_layer.update()
    # kiem chung sau truyen: manh mat cong phai khop Mc o trang thai moi
    mx2 = 0.0
    for o in bpy.data.objects:
        if not o.name.startswith(f"V10_GateBuddha_{tag}_"):
            continue
        s = bpy.data.objects.get(o.name[len(f"V10_GateBuddha_{tag}_"):])
        if s is None or base(s.name) in HAND_EXCLUDE:
            continue
        Mc_i = o.matrix_world @ s.matrix_world.inverted()
        mx2 = max(mx2, max(abs(Mc_i[r][c] - Mc[r][c]) for r in range(4) for c in range(4)))
    log(f"gate {tag}: Mc_maxdev SAU truyen (tru tay) = {mx2:.6f}")
    assert mx2 < 0.002, f"gate {tag} Mc vo sau truyen"
    LOG.setdefault("gates", {})[tag] = {"parts": len(pairs_g),
                                        "Mc_maxdev_pre": round(float(mx), 6),
                                        "Mc_maxdev_post": round(float(mx2), 6),
                                        "face_propagated": sorted(face_here)}

# ---- assert an toan: tai + manh ngoai pham vi khong doi ----
if not DRY_RUN:
    bpy.context.view_layer.update()
    for name, M0 in ear_snapshot.items():
        dev = float(np.abs(np.array(bpy.data.objects[name].matrix_world) - M0).max())
        assert dev < 1e-6, f"TAI BI DUNG: {name} dev {dev}"
    for name, M0 in nonface_snapshot.items():
        dev = float(np.abs(np.array(bpy.data.objects[name].matrix_world) - M0).max())
        assert dev < 1e-6, f"MANH NGOAI PHAM VI BI DUNG: {name} dev {dev}"
    log("assert tai + ngoai pham vi: KHONG DOI")

# ---- don import tam ----
for o in imported_all:
    bpy.data.objects.remove(o, do_unlink=True)
log("cleanup done")

LOG["ops"] = OPS
if DRY_RUN:
    log("DRY_RUN: khong ap ma tran, khong luu file. Tong op du kien:", len(OPS))
else:
    bpy.ops.wm.save_as_mainfile(filepath=DST)
    log("SAVED", DST)
    with open("/home/hatch/workspace/chua-online-work/layout/v14_audit.json", "w") as fp:
        json.dump(LOG, fp, indent=1, ensure_ascii=False)
print("BUILD V14", "DRY-RUN" if DRY_RUN else "", "DONE", flush=True)
