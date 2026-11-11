# V15 COMMON — cong do MOI cho luoi hop nhat (ke thua dinh nghia do V13/V14):
# - Dau vao: nhom manh goc (chua hop nhat) HOAC luoi hop nhat + nhan manh
#   gan bang KDTree toi be mat manh goc pristine (cung vi tri scene).
# - Chi so khoa (bang V14.1): head_h, head_w, nose_w_frac, do noi ellipsoid
#   (brow/eye/crease/lid/mouth/urna/cheek), tai (ratio/topf/lobf).
# Dinh nghia truong do KHOP verify_v141.py: head_w/head_h tu bbox cac manh
# Head_* loai neck/neckring/tai; do noi ellipsoid theo skull (tam + ban kinh
# bbox), front = max (p - sc).f tren cac dinh cua manh, u/v chuan hoa.
# Che do "surface": bbox/front/center tinh tren DINH THAT thay vi 8 goc
# bound_box; lech he thong (neu co) duoc hieu chuan o Buoc 0 tren luoi goc.
import re, math, json
import numpy as np
from mathutils import Vector
from mathutils.kdtree import KDTree

NECK_EXCLUDE = {"Head_neck", "Head_neckring0", "Head_neckring1"}
EAR_EXCLUDE = {"Head_earL", "Head_earR"}

LOCKS = {
    "dilac": {"head_h": 1.8401, "head_w": 1.7148, "nose_w_frac": 0.2500,
              "ear": (0.664, 0.321, 0.015),
              "protr": {"Head_browL": 0.0063, "Head_browR": 0.0063,
                        "Head_eyeL": 0.0173, "Head_eyeR": 0.0173,
                        "Head_creaseL": 0.0092, "Head_creaseR": 0.0092,
                        "Head_cheekL": 0.1004, "Head_cheekR": 0.1004}},
    "adida": {"head_h": 1.2388, "head_w": 0.8419, "nose_w_frac": 0.2720,
              "ear": (0.507, 0.632, -0.139),
              "protr": {"Head_browL": 0.0076, "Head_browR": 0.0076,
                        "Head_lidL": 0.0096, "Head_lidR": 0.0096,
                        "Head_eyeL": 0.0053, "Head_eyeR": 0.0053,
                        "Head_mouth": 0.0200, "Head_urna": 0.0169}},
}
FLAT_LIST = {k: sorted(v["protr"].keys()) for k, v in LOCKS.items()}

def base(n):
    return re.sub(r"\.\d{3}$", "", n)

def obj_world_verts(o):
    vs = np.empty(len(o.data.vertices) * 3, dtype=np.float64)
    o.data.vertices.foreach_get("co", vs)
    vs = vs.reshape(-1, 3)
    M = np.array(o.matrix_world, dtype=np.float64)
    return vs @ M[:3, :3].T + M[:3, 3]

def wbox_bb(o):
    ws = [o.matrix_world @ Vector(c) for c in o.bound_box]
    return ([min(v[i] for v in ws) for i in range(3)],
            [max(v[i] for v in ws) for i in range(3)])

def build_ref_cloud(pieces):
    """pieces: list[(label, obj)] -> (KDTree, labels list, all verts array).
    KDTree tren dinh the gioi cua tung manh goc."""
    allv = []
    labels = []
    for lab, o in pieces:
        w = obj_world_verts(o)
        allv.append(w)
        labels += [lab] * len(w)
    V = np.vstack(allv)
    kd = KDTree(len(V))
    for i, co in enumerate(V):
        kd.insert(Vector(co), i)
    kd.balance()
    return kd, labels, V

def label_points(kd, labels, pts, max_dist=0.008):
    """Gan nhan manh goc cho mang diem (N,3). Tra ve list label|None."""
    out = []
    for p in pts:
        _, idx, dist = kd.find(Vector(p))
        out.append(labels[idx] if dist <= max_dist else None)
    return out

def head_frame_from(skull_ctr, nose_ctr):
    f = Vector((nose_ctr[0] - skull_ctr[0], nose_ctr[1] - skull_ctr[1], 0.0))
    f.normalize()
    up = Vector((0, 0, 1))
    side = up.cross(f).normalized()
    return Vector(skull_ctr), side, f, up

def measure_surface(labeled, frame=None):
    """labeled: dict label -> (N,3) world verts (chi cac manh Head_* lien
    quan; tai do rieng bang BB nhu cu — xem measure_ears).
    frame: (sc, side, f, up); neu None tu tinh tu skull/nose.
    Tra ve dict chi so theo dinh nghia khoa."""
    def bb(v):
        return v.min(axis=0), v.max(axis=0)
    head_labels = [l for l in labeled
                   if l.startswith("Head_") and l not in NECK_EXCLUDE
                   and l not in EAR_EXCLUDE]
    allv = np.vstack([labeled[l] for l in head_labels])
    hmn, hmx = bb(allv)
    head_h = float(hmx[2] - hmn[2]); head_w = float(hmx[0] - hmn[0])
    smn, smx = bb(labeled["Head_skull"])
    sc = (smn + smx) / 2.0
    nmn_c, nmx_c = bb(labeled["Head_nose"])
    nose_ctr = (nmn_c + nmx_c) / 2.0
    if frame is None:
        frame = head_frame_from(sc, nose_ctr)
    scv, side, f, up = frame
    sc_np = np.array(scv)
    side_np = np.array(side); f_np = np.array(f)
    radii = (smx - smn) / 2.0
    out = {"head_h": round(head_h, 4), "head_w": round(head_w, 4),
           "head_mn": [round(float(v), 4) for v in hmn],
           "head_mx": [round(float(v), 4) for v in hmx],
           "nose_w_frac": round(float((nmx_c[0] - nmn_c[0]) / head_w), 4),
           "protr": {}}
    for lab, v in labeled.items():
        if lab == "Head_skull":
            continue
        vmn, vmx = bb(v)
        c = (vmn + vmx) / 2.0
        d = c - sc_np
        u = float(d @ side_np) / radii[0] if radii[0] else 0.0
        vv = float(d[2]) / radii[2] if radii[2] else 0.0
        t = 1.0 - u * u - vv * vv
        front = float(((v - sc_np) @ f_np).max())
        protr = front - math.sqrt(t) * radii[1] if t > 0 else float("nan")
        out["protr"][lab] = round(float(protr), 4)
    if "Head_mouth" in labeled:
        mmn, mmx = bb(labeled["Head_mouth"])
        mctr_z = float((mmn[2] + mmx[2]) / 2.0)
        out["mouth_frac_from_top"] = round((float(hmx[2]) - mctr_z) / head_h, 4)
        out["mouth_frac_from_bottom"] = round((mctr_z - float(hmn[2])) / head_h, 4)
    if "Head_smile" in labeled:
        smn2, smx2 = bb(labeled["Head_smile"])
        out["smile_frac_from_bottom"] = round(
            (float((smn2[2] + smx2[2]) / 2.0) - float(hmn[2])) / head_h, 4)
    return out

def measure_protr_ref(labeled, ref_labeled):
    """Protrusion on dinh nghia V14 nhung on dinh sau hop nhat: (u, v) va
    ellipsoid chuan (tam skull sc + radii) lay tu PRISTINE (hang so chuan
    cua dac trung), front = do sau lon nhat cua cum dinh gan nhan tren
    luoi dang do. Tren luoi pristine cho ket qua trung V14 (gate0 da
    chung minh front theo dinh ~ front theo goc BB <= 0,005)."""
    def bb(v):
        return v.min(axis=0), v.max(axis=0)
    smn, smx = bb(ref_labeled["Head_skull"])
    sc = (smn + smx) / 2.0
    nmn, nmx = bb(ref_labeled["Head_nose"])
    frame = head_frame_from(sc, (nmn + nmx) / 2.0)
    scv, side, f, up = frame
    sc_np = np.array(scv); side_np = np.array(side); f_np = np.array(f)
    radii = (smx - smn) / 2.0
    out = {}
    for lab, v in labeled.items():
        if lab == "Head_skull" or lab not in ref_labeled:
            continue
        rmn, rmx = bb(ref_labeled[lab])
        c = (rmn + rmx) / 2.0
        d = c - sc_np
        u = float(d @ side_np) / radii[0] if radii[0] else 0.0
        vv = float(d[2]) / radii[2] if radii[2] else 0.0
        t = 1.0 - u * u - vv * vv
        if t <= 0:
            continue
        front = float(((v - sc_np) @ f_np).max())
        out[lab] = round(front - math.sqrt(t) * float(radii[1]), 4)
    return out

def measure_ears_bb(pairs, head_h, head_mn_z, head_mx_z):
    """pairs: list[obj] tai (BB mode — giong verify cu). Tra ve list dict."""
    res = []
    for o in pairs:
        mn, mx = wbox_bb(o)
        res.append({"name": o.name,
                    "ratio": round((mx[2] - mn[2]) / head_h, 4),
                    "topf": round((head_mx_z - mx[2]) / head_h, 4),
                    "lobf": round((mn[2] - head_mn_z) / head_h, 4)})
    return res

def compare_table(key, meas, locks=None, tol=0.005):
    """So bang do voi bang khoa. Tra ve (list[dict], all_ok)."""
    L = (locks or LOCKS)[key]
    rows = []
    def row(name, got, want):
        d = None if got is None else round(abs(got - want), 4)
        rows.append({"name": name, "got": got, "want": want, "delta": d,
                     "ok": d is not None and d <= tol})
    row("head_h", meas.get("head_h"), L["head_h"])
    row("head_w", meas.get("head_w"), L["head_w"])
    row("nose_w_frac", meas.get("nose_w_frac"), L["nose_w_frac"])
    for lab, want in L["protr"].items():
        row(f"protr.{lab}", meas.get("protr", {}).get(lab), want)
    return rows, all(r["ok"] for r in rows)
