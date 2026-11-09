# V12 — KHOI PHUC TUONG PHAT VE NGUYEN BAN TRANG NGHIEM
# Lenh cung cua Chung Hy (18:13 09/11): tuong Phat phai trang nghiem,
# TUYET DOI khong chinh sua/stylize ti le hay net mat tuong.
# Vong V7 (build_v7.py muc 4) da sculpt Di Lac: tai Z x1.4 (nam trong scale
# cua object), smile X x1.3 (matrix), ma +-0.06 (matrix), bung Torso day
# +0.14m (nau vao mesh). Vong nay hoan tra ca 4 bang ban goc verified_v2.
# Cach lam: voi moi manh cua nhom Di Lac trong scene, thay mesh data bang
# mesh goc tu di-lac.glb (ban sao doc lap), gan lai dung material scene cu;
# 6 manh bi cham thi reset matrix_world = M @ W_glb (M = phep dat ca nhom,
# da do: dich thuan (-24,-1,+3.2), scale dung 1.0, 87/88 manh khop tuyet doi).
# PlatformSlab lech M co chu dich tu truoc (giu nguyen vi tri, chi doi mesh).
# Giu nguyen: be V11 + V11_PlinthText, mau am, fill 1500W, moi thu khac cua V13.
import bpy, json, mathutils
from mathutils import Matrix, Vector

SRC = "/home/hatch/workspace/chua-online-work/layout_v13_v11.blend"
DST = "/home/hatch/workspace/chua-online-work/layout_v14_v12.blend"
GLB = "/home/hatch/workspace/chua-online-work/statues/verified_v2/di-lac.glb"
LOG = {"steps": [], "audit": {}}
def log(*a):
    s = " ".join(str(x) for x in a)
    print("[V12]", s, flush=True)
    LOG["steps"].append(s)

bpy.ops.wm.open_mainfile(filepath=SRC)
sc = bpy.context.scene

# ---------- xac dinh nhom Di Lac trong scene (hop + ten goc + so dinh) ----------
TMPG = bpy.ops.import_scene.gltf
before_objs = set(bpy.data.objects)
before_mats = set(bpy.data.materials)
before_meshes = set(bpy.data.meshes)
TMPG(filepath=GLB)
imported = [o for o in bpy.data.objects if o not in before_objs]

def base(n):
    import re
    return re.sub(r"\.\d{3}$", "", n)

glb_parts = {}   # base name -> obj (ban import, toa do goc)
for o in imported:
    if o.type == 'MESH':
        glb_parts[base(o.name)] = o
log("imported glb objects:", len(imported), "mesh parts:", len(glb_parts))

def wctr(o):
    ws = [o.matrix_world @ Vector(c) for c in o.bound_box]
    return Vector(((min(v.x for v in ws)+max(v.x for v in ws))/2,
                   (min(v.y for v in ws)+max(v.y for v in ws))/2,
                   (min(v.z for v in ws)+max(v.z for v in ws))/2))

BOX = (-32, -15, -9, 9)
group = []
for o in bpy.data.objects:
    if o.type != 'MESH' or o in imported:
        continue
    c = wctr(o)
    if not (BOX[0] <= c.x <= BOX[1] and BOX[2] <= c.y <= BOX[3]):
        continue
    g = glb_parts.get(base(o.name))
    if g is not None and len(g.data.vertices) == len(o.data.vertices):
        group.append((o, g))
log("di-lac group matched:", len(group), "parts")
assert len(group) >= 90, "group too small — dung lai"

# ---------- do M tu cac manh chua bi cham ----------
TOUCHED = {"Head_earL", "Head_earR", "Head_smile", "Head_cheekL", "Head_cheekR", "Torso"}
Ms = []
for o, g in group:
    if base(o.name) in TOUCHED:
        continue
    Ms.append(o.matrix_world @ g.matrix_world.inverted())
M0 = Ms[0]
maxdev = 0.0; dev_name = None
for (o, g), M in zip([p for p in group if base(p[0].name) not in TOUCHED], Ms):
    for r in range(4):
        for c in range(4):
            d = abs(M[r][c] - M0[r][c])
            if d > maxdev: maxdev, dev_name = d, o.name
log("M0 translation:", [round(v, 3) for v in M0.translation], "max dev giua cac manh:", round(maxdev, 4), "tai", dev_name)
M = M0

# ghi lai lech cua tung manh bi cham + PlatformSlab (bao cao)
for o, g in group:
    bn = base(o.name)
    if bn in TOUCHED or bn == "PlatformSlab":
        Mi = o.matrix_world @ g.matrix_world.inverted()
        dt = Mi.translation - M.translation
        log("pre-restore", o.name, "lech translation vs M:", [round(v, 3) for v in dt],
            "scale:", [round(v, 3) for v in o.scale])

# ---------- thay mesh + reset matrix cho manh bi cham ----------
restored_matrix = []
for o, g in group:
    old_mesh = o.data
    old_mats = [ms.material.name if ms.material else None for ms in o.material_slots]
    if not old_mats:
        old_mats = [m.name if m else None for m in old_mesh.materials]
    new_mesh = g.data.copy()
    o.data = new_mesh
    # gan lai material scene cu theo tung slot
    mats_now = list(new_mesh.materials)
    for i, mname in enumerate(old_mats):
        if mname is None:
            continue
        mat = bpy.data.materials.get(mname)
        if mat is None:
            log("WARN material missing:", mname); continue
        if i < len(new_mesh.materials):
            new_mesh.materials[i] = mat
        else:
            new_mesh.materials.append(mat)
    if old_mesh.users == 0:
        nm = old_mesh.name
        bpy.data.meshes.remove(old_mesh)
        new_mesh.name = nm
    # xac minh material hieu luc sau swap; sai thi gan lai qua material_slots
    eff = [ms.material.name if ms.material else None for ms in o.material_slots]
    if eff != old_mats:
        for i, mname in enumerate(old_mats):
            if mname and i < len(o.material_slots):
                mat = bpy.data.materials.get(mname)
                if mat: o.material_slots[i].material = mat
        eff2 = [ms.material.name if ms.material else None for ms in o.material_slots]
        if eff2 != old_mats:
            log("WARN material mismatch sau swap:", o.name, "cu:", old_mats, "moi:", eff2)
    if base(o.name) in TOUCHED:
        o.matrix_world = M @ g.matrix_world
        restored_matrix.append(o.name)
bpy.context.view_layer.update()
log("mesh swapped for all", len(group), "parts; matrix restored:", restored_matrix)

# chup lai so lieu GLB can cho audit truoc khi xoa object tam
GLB_DIMS = {base(g.name): list(g.dimensions) for _, g in group}
GLB_CHEEK_DIST = None
_gcl, _gcr = glb_parts.get('Head_cheekL'), glb_parts.get('Head_cheekR')
if _gcl and _gcr:
    GLB_CHEEK_DIST = (wctr(_gcl) - wctr(_gcr)).length

# ---------- don cac object/material/mesh tam tu import ----------
for o in imported:
    bpy.data.objects.remove(o, do_unlink=True)
for m in list(bpy.data.materials):
    if m not in before_mats and m.users == 0:
        bpy.data.materials.remove(m)
for me in list(bpy.data.meshes):
    if me not in before_meshes and me.users == 0:
        bpy.data.meshes.remove(me)
log("cleanup done")

# ---------- kiem chung sau khoi phuc (trong bo nho) ----------
bad = []
for o, g in group:
    gd = GLB_DIMS[base(o.name)]
    for i in range(3):
        if gd[i] > 0.01:
            r = o.dimensions[i] / gd[i]
            if abs(r - 1.0) > 0.005:
                bad.append((o.name, i, round(r, 4)))
log("post-restore dim deviations >0.5%:", bad)
# khoang cach 2 ma (phai bang ban goc)
def get(n):
    return bpy.data.objects.get(n)
cl, cr = get('Head_cheekL'), get('Head_cheekR')
d_scene = (wctr(cl) - wctr(cr)).length if cl and cr else None
log("cheek center dist: scene =", round(d_scene, 4) if d_scene else None,
    "| glb =", round(GLB_CHEEK_DIST, 4) if GLB_CHEEK_DIST else None)
LOG["audit"]["cheek_dist_scene"] = d_scene
LOG["audit"]["cheek_dist_glb"] = GLB_CHEEK_DIST
# cac doi tuong phai giu nguyen
fl = bpy.data.objects.get('V8_FillDiLac')
LOG["audit"]["fill"] = {"energy": fl.data.energy, "color": list(fl.data.color)} if fl else None
pt = bpy.data.objects.get('V11_PlinthText')
LOG["audit"]["plinth_text"] = {"exists": pt is not None, "hide_render": bool(pt.hide_render)} if pt else None
ft = bpy.data.objects.get('FrontText')
LOG["audit"]["front_text"] = {"hide_render": bool(ft.hide_render), "loc": list(ft.location)} if ft else None
log("fill:", LOG["audit"]["fill"], "| plinth_text:", LOG["audit"]["plinth_text"], "| front_text:", LOG["audit"]["front_text"])

# ---------- ra soat 2 tuong cong: ma tran sao chep nhat quan + scale deu ----------
gate_audit = {}
for tag in ('PT', 'TD'):
    devs = []; svs = []
    for o in bpy.data.objects:
        if not o.name.startswith(f'V10_GateBuddha_{tag}_'):
            continue
        srcname = o.name[len(f'V10_GateBuddha_{tag}_'):]
        s = bpy.data.objects.get(srcname)
        if s is None: continue
        Mc = o.matrix_world @ s.matrix_world.inverted()
        devs.append((o.name, Mc))
    if devs:
        Mc0 = devs[0][1]
        mx = max(abs(Mc[r][c] - Mc0[r][c]) for _, Mc in devs for r in range(4) for c in range(4))
        import numpy as np
        sv = np.linalg.svd(np.array(Mc0)[:3, :3], compute_uv=False)
        gate_audit[tag] = {"parts": len(devs), "max_matrix_dev": round(float(mx), 5),
                           "singular_values": [round(float(v), 4) for v in sv]}
log("gate audit:", gate_audit)
LOG["audit"]["gates"] = gate_audit
LOG["audit"]["dim_deviations"] = bad
LOG["audit"]["group_parts"] = len(group)
LOG["audit"]["matrix_restored"] = restored_matrix

bpy.ops.wm.save_as_mainfile(filepath=DST)
log("SAVED", DST)
with open("/home/hatch/workspace/chua-online-work/layout/v12_audit.json", "w") as f:
    json.dump(LOG, f, indent=1, ensure_ascii=False)
print("BUILD V12 DONE", flush=True)
