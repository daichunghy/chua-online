# V13 VERIFY (doc lap, read-only): mo V15 + V14, doi chieu:
# 1) Ti le tai/dau cua 2 tuong chinh + 2 tuong cong trong V15 vs muc tieu anh.
# 2) Mc cong trong V15 van nhat quan (lech ~0 nhu V12).
# 3) Ngoai cac manh tai da sua (+ tai cong neu tao moi), MOI object cua V15
#    phai trung matrix_world + mesh checksum voi V14 (bang chung khong dung
#    vao than/canh). Mesh cua ca manh tai cung khong doi (chi doi matrix).
import bpy, re, json, hashlib
import numpy as np
from mathutils import Vector

V15 = "/home/hatch/workspace/chua-online-work/layout_v15_v13.blend"
V14 = "/home/hatch/workspace/chua-online-work/layout_v14_v12.blend"
GLBS = {
    "dilac": "/home/hatch/workspace/chua-online-work/statues/verified_v2/di-lac.glb",
    "adida": "/home/hatch/workspace/chua-online-work/statues/verified_v2/phat-dung-adida.glb",
}
TARGETS = {"dilac": {"f_len": 0.664, "f_top": 0.321},
           "adida": {"f_len": 0.507, "f_top": 0.632}}

def base(n):
    return re.sub(r"\.\d{3}$", "", n)

def wbox(o):
    ws = [o.matrix_world @ Vector(c) for c in o.bound_box]
    return ([min(v[i] for v in ws) for i in range(3)],
            [max(v[i] for v in ws) for i in range(3)])

def wctr(o):
    mn, mx = wbox(o)
    return Vector([(mn[i] + mx[i]) / 2 for i in range(3)])

def mesh_sig(o):
    vs = o.data.vertices
    h = hashlib.md5()
    h.update(str(len(vs)).encode())
    s = 0.0
    for i in range(0, len(vs), 7):
        s += vs[i].co.x + 3 * vs[i].co.y + 7 * vs[i].co.z
    h.update(f"{s:.3f}".encode())
    return h.hexdigest()[:12]

def dump_all(path):
    bpy.ops.wm.open_mainfile(filepath=path)
    d = {}
    for o in bpy.data.objects:
        if o.type != 'MESH':
            continue
        d[o.name] = {"mat": [round(v, 6) for row in o.matrix_world for v in row],
                     "sig": mesh_sig(o), "nv": len(o.data.vertices)}
    return d

# ---------- phan 1: ti le trong V15 ----------
bpy.ops.wm.open_mainfile(filepath=V15)
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
    return [(o, parts[base(o.name)]) for o in cands
            if base(o.name) in parts and len(o.data.vertices) == len(parts[base(o.name)].data.vertices)]

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
dl = [p for p in match("dilac", nongate) if -32 <= wctr(p[0]).x <= -15 and -9 <= wctr(p[0]).y <= 9]
ad = None
for cl in cluster(match("adida", nongate)):
    if "Head_ushnisha" in {base(o.name) for o, _ in cl} and len(cl) > 40:
        ad = cl

# DINH NGHIA DAU (nhu build_v13.py): chieu cao dau = CAM -> DINH DAU,
# khop dinh nghia do anh (Di Lac 1.840, A Di Da 1.2388). Head_neck /
# Head_neckring thap hon cam 0.19-0.22 m -> loai khoi mau so, neu khong
# se "xac nhan" sai tai dai thua 12-15%.
NECK_EXCLUDE = {"Head_neck", "Head_neckring0", "Head_neckring1"}
# Tay trai ban sao cong lech Mc san co tu V14 (tam khop Mc, chi xoay nho
# quanh tam) -> loai khoi kiem tra Mc, khong phai loi cua V13.
HAND_EXCLUDE = {"HandL", "FingerL0", "FingerL1", "FingerL2"}
# Loai tai khoi bbox dau: day tai A Di Da sau nan thap hon cam (dung nhu
# anh) -> neu tinh tai vao, day tai se tu dinh nghia lai day dau va ti le
# tu sai (verify chay dau bao A Di Da 0.4451 sai trong khi build dung
# 0.507). Mau so chi lay tu manh on dinh (so/cam/ushnisha/mat/mui/mieng).
EAR_EXCLUDE = {"Head_earL", "Head_earR"}

def ratios(pairs):
    hmn = [1e9] * 3; hmx = [-1e9] * 3
    for o, _ in pairs:
        if not base(o.name).startswith("Head_"):
            continue
        if base(o.name) in NECK_EXCLUDE or base(o.name) in EAR_EXCLUDE:
            continue
        mn, mx = wbox(o)
        for i in range(3):
            hmn[i] = min(hmn[i], mn[i]); hmx[i] = max(hmx[i], mx[i])
    hh = hmx[2] - hmn[2]
    out = {}
    for o, _ in pairs:
        if base(o.name) in ("Head_earL", "Head_earR"):
            mn, mx = wbox(o)
            out[o.name] = {"ratio": round((mx[2] - mn[2]) / hh, 4),
                           "topfrac": round((hmx[2] - mx[2]) / hh, 4),
                           "lobefrac": round((mn[2] - hmn[2]) / hh, 4)}
    return out

for key, pairs in (("dilac", dl), ("adida", ad)):
    r = ratios(pairs)
    t = TARGETS[key]
    print(f"[VERIFY] {key}: target ratio={t['f_len']} topfrac={t['f_top']}")
    for nm, v in r.items():
        ok = abs(v["ratio"] - t["f_len"]) < 0.01 and abs(v["topfrac"] - t["f_top"]) < 0.01
        print(f"[VERIFY]   {nm}: {v} -> {'OK' if ok else 'LECH!'}")

# cong: Mc + ti le tai trong khung cong
for tag in ("PT", "TD"):
    pairs = []
    for o in bpy.data.objects:
        if o.name.startswith(f"V10_GateBuddha_{tag}_"):
            s = bpy.data.objects.get(o.name[len(f"V10_GateBuddha_{tag}_"):])
            if s is not None:
                pairs.append((o, s))
    ref = [p for p in pairs if base(p[1].name) == "Head_ushnisha"]
    assert ref, f"gate {tag}: khong co Head_ushnisha"
    Mc = ref[0][0].matrix_world @ ref[0][1].matrix_world.inverted()
    mx = 0.0
    for o, s in pairs:
        if base(s.name) in HAND_EXCLUDE:
            continue
        Mi = o.matrix_world @ s.matrix_world.inverted()
        mx = max(mx, max(abs(Mi[r][c] - Mc[r][c]) for r in range(4) for c in range(4)))
    heads = [o for o, s in pairs if base(s.name).startswith("Head_")
             and base(s.name) not in NECK_EXCLUDE
             and base(s.name) not in EAR_EXCLUDE]
    hmn = [1e9] * 3; hmx = [-1e9] * 3
    for o in heads:
        mn, mx2 = wbox(o)
        for i in range(3):
            hmn[i] = min(hmn[i], mn[i]); hmx[i] = max(hmx[i], mx2[i])
    hh = hmx[2] - hmn[2]
    print(f"[VERIFY] gate {tag}: parts={len(pairs)} Mc_maxdev={mx:.6f} head_h={hh:.4f}")
    for o, s in pairs:
        if base(s.name) in ("Head_earL", "Head_earR"):
            mn, mx2 = wbox(o)
            print(f"[VERIFY]   {o.name}: ear ratio={(mx2[2]-mn[2])/hh:.4f} (target 0.507)")

ADJUSTED = set()
for key, pairs in (("dilac", dl), ("adida", ad)):
    for o, _ in pairs:
        if base(o.name) in ("Head_earL", "Head_earR"):
            ADJUSTED.add(o.name)
print(f"[VERIFY] manh tai chinh se doi chieu: {sorted(ADJUSTED)}")

# ---------- phan 2: doi chieu toan canh V15 vs V14 ----------
d15 = dump_all(V15)
d14 = dump_all(V14)
only15 = sorted(set(d15) - set(d14))
only14 = sorted(set(d14) - set(d15))
print(f"[VERIFY] objects: v15={len(d15)} v14={len(d14)} only15={only15} only14={only14}")
bad_mat, bad_sig = [], []
for nm in set(d15) & set(d14):
    if d15[nm]["sig"] != d14[nm]["sig"] or d15[nm]["nv"] != d14[nm]["nv"]:
        bad_sig.append(nm)
    dev = max(abs(a - b) for a, b in zip(d15[nm]["mat"], d14[nm]["mat"]))
    if dev > 1e-6 and nm not in ADJUSTED and not nm.startswith("V10_GateBuddha_"):
        bad_mat.append((nm, dev))
gate_dev = []
for nm in set(d15) & set(d14):
    if nm.startswith("V10_GateBuddha_"):
        dev = max(abs(a - b) for a, b in zip(d15[nm]["mat"], d14[nm]["mat"]))
        if dev > 1e-6:
            gate_dev.append((nm, round(dev, 4)))
print(f"[VERIFY] mesh sig lech (phai rong): {bad_sig}")
print(f"[VERIFY] matrix lech NGOAI nhom tai chinh (phai rong): {bad_mat}")
print(f"[VERIFY] matrix cong da doi (chi tai cong duoc phep): {gate_dev}")
print(f"[VERIFY] manh tai chinh da sua: {sorted(ADJUSTED)}")
print("VERIFY V13 DONE", flush=True)
