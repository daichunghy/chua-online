# V15 VERIFY FINAL tren layout_v18_v15.blend (doc lap, chi doc):
# - dem object, kiem cac object moi ton tai, tai/kept pieces nguyen ven
# - do lai 2 dau tuong chinh NGAY trong canh (nhan be mat tu npz goc)
#   so voi bang khoa (mat Di Lac dung muc tieu lo mat 0,0040)
# - cong: bbox mat cong = ti le Mc 0,1953 cua mat chinh ±0,01; tai cong
#   giu nguyen ti le V13
# - Light Linking doc lai tu file
# Sentinel: V15 FINAL VERIFY PASS
import bpy, sys, json, re
import numpy as np
sys.path.insert(0, "/home/hatch/workspace/chua-online-work/layout")
import v15_common as C
import v15_ops as O
from mathutils import Vector

DST = "/home/hatch/workspace/chua-online-work/layout_v18_v15.blend"
WORK = "/home/hatch/workspace/chua-online-work/layout/v15_work"
OUTJ = "/home/hatch/workspace/chua-online-work/layout/v15_final_verify.json"
RES = {"checks": []}
def check(name, ok, detail=""):
    RES["checks"].append({"name": name, "ok": bool(ok), "detail": detail})
    print(f"[VF] {'PASS' if ok else 'FAIL'} {name} {detail}", flush=True)

def base(n):
    return re.sub(r"\.\d{3}$", "", n)

def wverts(o):
    V = np.empty(len(o.data.vertices) * 3)
    o.data.vertices.foreach_get("co", V)
    V = V.reshape(-1, 3)
    M = np.array(o.matrix_world)
    return V @ M[:3, :3].T + M[:3, 3]

def wbox(o):
    ws = [o.matrix_world @ Vector(c) for c in o.bound_box]
    return ([min(v[i] for v in ws) for i in range(3)],
            [max(v[i] for v in ws) for i in range(3)])

bpy.ops.wm.open_mainfile(filepath=DST)
meshes = [o for o in bpy.data.objects if o.type == 'MESH']
check("object count 2568-43+4=2529", len(meshes) == 2529, f"got {len(meshes)}")
for nm in ("V15_HeadFace_dilac", "V15_HeadFace_adida",
           "V10_GateBuddha_PT_Head_face", "V10_GateBuddha_TD_Head_face"):
    check(f"exists {nm}", bpy.data.objects.get(nm) is not None)
check("no Head_curls", bpy.data.objects.get("Head_curls") is None)
check("no REF_merged in scene",
      all(not o.name.startswith("REF_merged") for o in meshes))

def head_measure(key, face_name, extra_names):
    ref = np.load(f"{WORK}/ref_{key}.npz", allow_pickle=True)
    pieces = []
    pristine = {}
    for k in ref.files:
        if k.endswith("__verts"):
            pieces.append((k[:-7], ref[k], ref[f"{k[:-7]}__polys"]))
            pristine[k[:-7]] = ref[k]
    bvh, fl = O.build_bvh_labeled([v for _, v, _ in pieces],
                                  [p for _, _, p in pieces])
    names = [lab for lab, _, _ in pieces]
    face = bpy.data.objects[face_name]
    W = wverts(face)
    labs = O.label_by_surface(bvh, fl, names, W)
    labeled = {}
    for p, lab in zip(W, labs):
        if lab is not None:
            labeled.setdefault(lab, []).append(p)
    labeled = {k: np.array(v) for k, v in labeled.items()}
    for en in extra_names:
        o = bpy.data.objects.get(en)
        if o is not None:
            labeled[base(en)] = wverts(o)
    m = C.measure_surface(labeled)
    m["protr"] = C.measure_protr_ref(labeled, pristine)
    return m

def find_group_head_extras(key):
    # tai + (adida: ushnisha/hair/ring) cua tuong chinh trong canh V18:
    # xac dinh theo vi tri tuong doi tam dau pristine
    return []

# Di Lac: extras = tai (tim theo vi tri canh dau)
def extras_near(center, radius, want_bases, exclude_names):
    out = []
    for o in meshes:
        if base(o.name) in want_bases and o.name not in exclude_names:
            mn, mx = wbox(o)
            c = np.array([(mn[i] + mx[i]) / 2 for i in range(3)])
            if np.linalg.norm(c - np.array(center)) < radius:
                out.append(o.name)
    return out

dilac_extras = extras_near((-24, -0.9, 10.2), 2.2,
                           ("Head_earL", "Head_earR"), ())
adida_extras = extras_near((-14, -31, 10.34), 1.6,
                           ("Head_earL", "Head_earR", "Head_ushnisha",
                            "Head_hair", "Head_ushnisha_ring"), ())
print("[VF] dilac extras:", dilac_extras, flush=True)
print("[VF] adida extras:", adida_extras, flush=True)

m_d = head_measure("dilac", "V15_HeadFace_dilac", dilac_extras)
dk = C.LOCKS["dilac"]
check("dilac head_h", abs(m_d["head_h"] - dk["head_h"]) <= 0.01,
      f"{m_d['head_h']} vs {dk['head_h']}")
check("dilac head_w", abs(m_d["head_w"] - dk["head_w"]) <= 0.01,
      f"{m_d['head_w']} vs {dk['head_w']}")
check("dilac nose", abs(m_d["nose_w_frac"] - dk["nose_w_frac"]) <= 0.01,
      f"{m_d['nose_w_frac']} vs {dk['nose_w_frac']}")
check("dilac cheek protr", abs(m_d["protr"].get("Head_cheekL", 9) - 0.1004) <= 0.02,
      f"{m_d['protr'].get('Head_cheekL')}")
check("dilac eye protr (exposed)", abs(m_d["protr"].get("Head_eyeL", 9) - 0.0040) <= 0.01,
      f"{m_d['protr'].get('Head_eyeL')}")
ears_d = [bpy.data.objects[n] for n in dilac_extras if "ear" in n]
er = C.measure_ears_bb(ears_d, m_d["head_h"], m_d["head_mn"][2], m_d["head_mx"][2])
check("dilac ears V13", all(abs(r["ratio"] - 0.664) < 0.01
                            and abs(r["topf"] - 0.321) < 0.01
                            and abs(r["lobf"] - 0.015) < 0.012 for r in er),
      f"{er}")

m_a = head_measure("adida", "V15_HeadFace_adida", adida_extras)
ak = C.LOCKS["adida"]
for nm, got, want in (("head_h", m_a["head_h"], ak["head_h"]),
                      ("head_w", m_a["head_w"], ak["head_w"]),
                      ("nose", m_a["nose_w_frac"], ak["nose_w_frac"]),
                      ("mouth protr", m_a["protr"].get("Head_mouth", 9), 0.0200),
                      ("urna protr", m_a["protr"].get("Head_urna", 9), 0.0169)):
    check(f"adida {nm}", abs(got - want) <= 0.01, f"{got} vs {want}")
ears_a = [bpy.data.objects[n] for n in adida_extras if "ear" in n]
er = C.measure_ears_bb(ears_a, m_a["head_h"], m_a["head_mn"][2], m_a["head_mx"][2])
check("adida ears V13", all(abs(r["ratio"] - 0.507) < 0.01
                            and abs(r["topf"] - 0.632) < 0.01
                            and abs(r["lobf"] + 0.139) < 0.012 for r in er),
      f"{er}")

# cong: ti le bbox mat cong / mat chinh ~ 0,1953
fm = wverts(bpy.data.objects["V15_HeadFace_adida"])
fmn, fmx = fm.min(0), fm.max(0)
for tag in ("PT", "TD"):
    g = wverts(bpy.data.objects[f"V10_GateBuddha_{tag}_Head_face"])
    gmn, gmx = g.min(0), g.max(0)
    ratios = (gmx - gmn) / (fmx - fmn)
    check(f"gate {tag} face scale", np.all(np.abs(ratios - 0.1953) < 0.01),
          f"ratios={np.round(ratios, 4)}")

# Light Linking doc lai
for tag in ("PT", "TD"):
    light = bpy.data.objects.get(f"V10_NicheFill_{tag}")
    rc = light.light_linking.receiver_collection if light else None
    check(f"lightlink {tag}", rc is not None and len(rc.objects) == 30,
          f"{rc.name if rc else None} n={len(rc.objects) if rc else 0}")

RES["dilac_meas"] = m_d
RES["adida_meas"] = m_a
n_ok = sum(1 for c in RES["checks"] if c["ok"])
RES["summary"] = f"{n_ok}/{len(RES['checks'])}"
with open(OUTJ, "w") as fp:
    json.dump(RES, fp, indent=1, ensure_ascii=False, default=str)
allok = n_ok == len(RES["checks"])
print(f"V15 FINAL VERIFY {'PASS' if allok else 'FAIL'} "
      f"({RES['summary']})", flush=True)
sys.exit(0 if allok else 1)
