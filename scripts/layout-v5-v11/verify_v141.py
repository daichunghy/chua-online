# V14.1 VERIFY (doc lap, read-only): mo layout_v17_v141 (buoc 2) + layout_v16_v14:
# 1) Do lai tren V17: mui A Di Da phai = 0,272 ± 0,010 (dich KE_HOACH_V14 A5);
#    MOI so V14 khac phai giu nguyen nhu v14_verify.json (mui Di Lac 0,2500,
#    do noi cac manh ep det, ma, tai 2 tuong, head_h/head_w, Mc 2 cong).
# 2) Toan canh V17 vs V16: so object bang; mesh checksum lech RONG;
#    matrix lech CHI o dung 3 object: mui A Di Da chinh + 2 ban sao cong.
import bpy, re, json, math, hashlib
from mathutils import Vector

V17 = "/home/hatch/workspace/chua-online-work/layout_v17_v141.blend"
V16 = "/home/hatch/workspace/chua-online-work/layout_v16_v14.blend"
V14V = "/home/hatch/workspace/chua-online-work/layout/v14_verify.json"
OUT = "/home/hatch/workspace/chua-online-work/layout/v141_verify.json"
GLBS = {
    "dilac": "/home/hatch/workspace/chua-online-work/statues/verified_v2/di-lac.glb",
    "adida": "/home/hatch/workspace/chua-online-work/statues/verified_v2/phat-dung-adida.glb",
}
NECK_EXCLUDE = {"Head_neck", "Head_neckring0", "Head_neckring1"}
EAR_EXCLUDE = {"Head_earL", "Head_earR"}
HAND_EXCLUDE = {"HandL", "FingerL0", "FingerL1", "FingerL2"}
ALLOWED_CHANGED = {"Head_nose",  # mui A Di Da chinh (ten object trong scene)
                   "V10_GateBuddha_PT_Head_nose",
                   "V10_GateBuddha_TD_Head_nose"}
RES = {"checks": [], "groups": {}, "gates": {}}
def check(name, ok, detail=""):
    RES["checks"].append({"name": name, "ok": bool(ok), "detail": str(detail)})
    print(f"[VERIFY141] {'OK ' if ok else 'FAIL'} {name} {detail}", flush=True)

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

with open(V14V) as fp:
    V14 = json.load(fp)

# ---------- phan 1: do lai tren V17 ----------
bpy.ops.wm.open_mainfile(filepath=V17)
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
    assert len(got) == 1, f"piece {name}: {len(got)}"
    return got[0][0]

def head_frame(pairs):
    skull = piece(pairs, "Head_skull"); nose = piece(pairs, "Head_nose")
    sc, nc = wctr(skull), wctr(nose)
    f = Vector((nc.x - sc.x, nc.y - sc.y, 0.0)); f.normalize()
    up = Vector((0, 0, 1))
    return sc, up.cross(f).normalized(), f, up

def ellipsoid_protr(pairs, o):
    skull = piece(pairs, "Head_skull")
    smn, smx = wbox(skull)
    sc, side, f, up = head_frame(pairs)
    radii = Vector(((smx[0] - smn[0]) / 2, (smx[1] - smn[1]) / 2, (smx[2] - smn[2]) / 2))
    c = wctr(o); d = c - sc
    u = d.dot(side) / radii.x if radii.x else 0.0
    v = d.z / radii.z if radii.z else 0.0
    t = 1.0 - u * u - v * v
    corners = [o.matrix_world @ Vector(cc) for cc in o.bound_box]
    front = max((p - sc).dot(f) for p in corners)
    if t <= 0:
        return float("nan")
    return front - math.sqrt(t) * radii.y

EAR_TARGET = {"dilac": (0.664, 0.321, 0.015), "adida": (0.507, 0.632, -0.139)}
FLAT_PIECES = {"dilac": ["Head_browL", "Head_browR", "Head_eyeL", "Head_eyeR",
                         "Head_creaseL", "Head_creaseR"],
               "adida": ["Head_browL", "Head_browR", "Head_lidL", "Head_lidR",
                         "Head_eyeL", "Head_eyeR", "Head_mouth", "Head_urna"]}
for key, pairs in GROUPS.items():
    hmn, hmx = head_bbox(pairs)
    head_h = hmx[2] - hmn[2]; head_w = hmx[0] - hmn[0]
    g14 = V14["groups"][key]
    g = {"head_h": round(head_h, 4), "head_w": round(head_w, 4), "protr": {}}
    check(f"{key} head_h giu V14", abs(head_h - g14["head_h"]) <= 0.0015,
          f"{head_h:.4f} vs {g14['head_h']}")
    check(f"{key} head_w giu V14", abs(head_w - g14["head_w"]) <= 0.0015,
          f"{head_w:.4f} vs {g14['head_w']}")
    nose = piece(pairs, "Head_nose")
    nmn, nmx = wbox(nose)
    frac = (nmx[0] - nmn[0]) / head_w
    g["nose_w_frac"] = round(frac, 4)
    if key == "adida":
        check("adida nose frac -> 0.272 (buoc 2)", abs(frac - 0.272) <= 0.010,
              f"frac={frac:.4f} (V14 buoc 1: 0.2463)")
    else:
        check("dilac nose frac giu 0.2500", abs(frac - g14["nose_w_frac"]) <= 0.003,
              f"frac={frac:.4f} vs {g14['nose_w_frac']}")
    for nm in FLAT_PIECES[key]:
        pr = ellipsoid_protr(pairs, piece(pairs, nm))
        g["protr"][nm] = round(pr, 4)
        check(f"{key} {nm} protr giu V14", abs(pr - g14["protr"][nm]) <= 0.004,
              f"protr={pr:.4f} vs {g14['protr'][nm]}")
    if key == "dilac":
        for nm in ("Head_cheekL", "Head_cheekR"):
            pr = ellipsoid_protr(pairs, piece(pairs, nm))
            g["protr"][nm] = round(pr, 4)
            check(f"dilac {nm} protr giu V14", abs(pr - g14["protr"][nm]) <= 0.006,
                  f"protr={pr:.4f} vs {g14['protr'][nm]}")
    for o, _ in pairs:
        if base(o.name) in EAR_EXCLUDE:
            mn, mx = wbox(o)
            ratio = (mx[2] - mn[2]) / head_h
            topf = (hmx[2] - mx[2]) / head_h
            lobf = (mn[2] - hmn[2]) / head_h
            t = EAR_TARGET[key]
            ok = abs(ratio - t[0]) < 0.01 and abs(topf - t[1]) < 0.01 and abs(lobf - t[2]) < 0.012
            check(f"{key} tai {o.name} giu V13", ok,
                  f"ratio={ratio:.4f} top={topf:.4f} lobe={lobf:.4f}")
    RES["groups"][key] = g

# cong: Mc nhat quan (loai tay)
for tag in ("PT", "TD"):
    pairs_g = []
    for o in bpy.data.objects:
        if not o.name.startswith(f"V10_GateBuddha_{tag}_"):
            continue
        s = bpy.data.objects.get(o.name[len(f"V10_GateBuddha_{tag}_"):])
        if s is not None:
            pairs_g.append((o, s))
    ref = [p for p in pairs_g if base(p[1].name) == "Head_ushnisha"]
    assert ref, f"gate {tag}: khong co Head_ushnisha"
    Mc = ref[0][0].matrix_world @ ref[0][1].matrix_world.inverted()
    mx = 0.0
    for o, s in pairs_g:
        if base(s.name) in HAND_EXCLUDE:
            continue
        Mi = o.matrix_world @ s.matrix_world.inverted()
        mx = max(mx, max(abs(Mi[r][c] - Mc[r][c]) for r in range(4) for c in range(4)))
    RES["gates"][tag] = {"parts": len(pairs_g), "Mc_maxdev": round(float(mx), 6)}
    check(f"gate {tag} Mc <= 0.002", mx <= 0.002, f"maxdev={mx:.6f} parts={len(pairs_g)}")

# ---------- phan 2: toan canh V17 vs V16 ----------
d17 = dump_all(V17)
d16 = dump_all(V16)
only17 = sorted(set(d17) - set(d16)); only16 = sorted(set(d16) - set(d17))
check("so object bang nhau", not only17 and not only16,
      f"v17={len(d17)} v16={len(d16)} only17={only17} only16={only16}")
bad_sig = [nm for nm in set(d17) & set(d16)
           if d17[nm]["sig"] != d16[nm]["sig"] or d17[nm]["nv"] != d16[nm]["nv"]]
check("mesh checksum lech rong", not bad_sig, f"{bad_sig[:10]}")
changed, bad_mat, ear_changed = [], [], []
for nm in set(d17) & set(d16):
    dev = max(abs(a - b) for a, b in zip(d17[nm]["mat"], d16[nm]["mat"]))
    if dev <= 1e-6:
        continue
    changed.append(nm)
    if base(nm) in EAR_EXCLUDE:
        ear_changed.append((nm, round(dev, 5)))
    if nm not in ALLOWED_CHANGED:
        bad_mat.append((nm, round(dev, 5)))
check("matrix lech chi o mui A Di Da (chinh + 2 cong)",
      not bad_mat and "Head_nose" in changed and len(changed) == 3,
      f"changed={sorted(changed)} bad={bad_mat[:8]}")
check("tai (chinh + cong) khong doi matrix", not ear_changed, f"{ear_changed[:6]}")
RES["changed"] = sorted(changed)
fails = [c for c in RES["checks"] if not c["ok"]]
RES["verdict"] = "PASS" if not fails else f"FAIL {len(fails)}"
RES["n_pass"] = sum(1 for c in RES["checks"] if c["ok"])
RES["n_total"] = len(RES["checks"])
with open(OUT, "w") as fp:
    json.dump(RES, fp, indent=1, ensure_ascii=False)
print(f"VERIFY V141 {RES['verdict']} {RES['n_pass']}/{RES['n_total']}", flush=True)
