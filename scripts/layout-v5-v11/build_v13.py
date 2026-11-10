# V13 BUILD — NAN MAT TUONG VE PHIA ANH THAT (chi tai, theo so do anh).
# Lenh Chung Hy 20:04 09/11: "Lam vong nan mat tuong theo dung anh that".
# LUAT: chi sua cai DO DUOC la lech so voi anh that; moi sua deu co can cu do.
# Ket qua do (xem NOTES.md S.V13):
#  - Di Lac (ref5): tai/dau anh = 0.664, model = 0.486 -> tai ngan ~27%.
#    Dinh tai: anh 0.321 (tu dinh dau), model 0.402. Day tai ~ ngang cam (anh
#    +0.015) vs model +0.112. -> keo dai tai x1.367 + nang dinh tai +0.148 (GLB).
#  - A Di Da (ref3): tai/dau anh = 0.507, model = 0.407 -> tai ngan ~20%.
#    Dinh tai: anh 0.632, model 0.534. Day tai DUOI cam 0.140 (anh) vs tren cam
#    0.059 (model). -> keo dai x1.247 + ha dinh tai -0.122 (GLB).
#  - Phat nam (ref7): lech ~8% trong sai so do -> KHONG nan.
#  - Mat/mui/mieng/ma/trang cua 2 tuong: lech <=7% (nhieu chieu bi nhieu phoi
#    canh) -> KHONG sua. Dau/than: Di Lac 0.304 vs 0.29 (5%); A Di Da so lieu
#    mau thuan giua cac lan do -> KHONG sua.
# Cach sua: bien doi z' = k*z + b tren matrix_world cua manh tai (chi truc doc),
# giong ky luat V7/V12 (object matrix, kiem chung duoc). Cong: A' = Mc A Mc^-1.
import bpy, re, json
import numpy as np
from mathutils import Matrix, Vector

SRC = "/home/hatch/workspace/chua-online-work/layout_v14_v12.blend"
DST = "/home/hatch/workspace/chua-online-work/layout_v15_v13.blend"
GLBS = {
    "dilac": "/home/hatch/workspace/chua-online-work/statues/verified_v2/di-lac.glb",
    "adida": "/home/hatch/workspace/chua-online-work/statues/verified_v2/phat-dung-adida.glb",
}
TARGETS = {  # phan so do tu anh that
    "dilac": {"f_len": 0.664, "f_top": 0.321},
    "adida": {"f_len": 0.507, "f_top": 0.632},
}
LOG = {"steps": [], "statues": {}, "gates": {}}
def log(*a):
    s = " ".join(str(x) for x in a)
    print("[V13]", s, flush=True)
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

# ---- import tam + xac dinh nhom (cung phuong phap inspect_v13) ----
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

# DINH NGHIA DAU: chieu cao dau = CAM -> DINH DAU (khop dinh nghia do anh:
# ref5/ref3 do tu cam len dinh; GLB: Di Lac cam 6.0501 -> dinh so 7.8902
# = 1.840; A Di Da day so 9.8126 -> dinh ushnisha 11.0514 = 1.2388).
# Head_neck / Head_neckring THAP HON cam 0.19-0.22 m -> NEU TINH VAO
# mau so se phong dai tai 12-15% (loi gap o ban build dau: k Di Lac
# 1.5328 thay vi 1.3667 dung). Loai khoi bbox dau. CUNG LOAI TAI:
# sau khi keo dai, day tai A Di Da thap hon cam (dung nhu anh that) ->
# neu tinh tai vao bbox, day tai se tu dinh nghia lai day dau (mau so
# phu thuoc vao chinh thu no do) -> mau so phai lay tu cac manh on
# dinh (so, cam, ushnisha, mat/mui/mieng), khong lay tai.
NECK_EXCLUDE = {"Head_neck", "Head_neckring0", "Head_neckring1"}
EAR_EXCLUDE = {"Head_earL", "Head_earR"}

def head_bbox(pairs):
    hmn = [1e9] * 3; hmx = [-1e9] * 3
    for o, _ in pairs:
        if not base(o.name).startswith("Head_"):
            continue
        if base(o.name) in NECK_EXCLUDE or base(o.name) in EAR_EXCLUDE:
            continue
        mn, mx = wbox(o)
        for i in range(3):
            hmn[i] = min(hmn[i], mn[i]); hmx[i] = max(hmx[i], mx[i])
    return hmn, hmx

# Cac manh tay trai cua ban sao cong lech Mc san co tu V14 (diag 09/11):
# tam the gioi khop Mc chinh xac (diff 0.0000 m) nhung ma tran lech
# 0.06-0.08 = xoay nho quanh tam rieng (co tu luc sao chep V10).
# Ngoai pham vi V13 (chi tai) -> loai khoi kiem tra Mc, KHONG sua.
HAND_EXCLUDE = {"HandL", "FingerL0", "FingerL1", "FingerL2"}

ADJ = {}  # key -> Matrix A (world)
for key, pairs in GROUPS.items():
    hmn, hmx = head_bbox(pairs)
    head_h = hmx[2] - hmn[2]
    tgt = TARGETS[key]
    ears = [(o, g) for o, g in pairs if base(o.name) in ("Head_earL", "Head_earR")]
    assert len(ears) == 2, f"{key}: ears found {len(ears)}"
    rep = {"head_h": round(head_h, 4), "head_top_z": round(hmx[2], 4), "ears": {}}
    A_by_ear = {}
    for o, _ in ears:
        mn, mx = wbox(o)
        cur_h = mx[2] - mn[2]
        k = tgt["f_len"] * head_h / cur_h
        top_new = hmx[2] - tgt["f_top"] * head_h
        b = top_new - k * mx[2]
        A = Matrix.Identity(4); A[2][2] = k; A[2][3] = b
        prev = A_by_ear.get(base(o.name))
        if prev is not None:
            dev = max(abs(A[r][c] - prev[r][c]) for r in range(4) for c in range(4))
            assert dev < 0.02, f"{key}: hai tai lech A qua lon {dev}"
        A_by_ear[base(o.name)] = A
        rep["ears"][o.name] = {"pre_h": round(cur_h, 4), "pre_top_z": round(mx[2], 4),
                              "pre_bot_z": round(mn[2], 4), "k": round(k, 4), "b": round(b, 4)}
        o.matrix_world = A @ o.matrix_world
        bpy.context.view_layer.update()
        mn2, mx2 = wbox(o)
        rep["ears"][o.name].update({"post_h": round(mx2[2] - mn2[2], 4),
                                    "post_top_z": round(mx2[2], 4), "post_bot_z": round(mn2[2], 4),
                                    "post_ratio": round((mx2[2] - mn2[2]) / head_h, 4),
                                    "post_topfrac": round((hmx[2] - mx2[2]) / head_h, 4),
                                    "post_lobefrac": round((mn2[2] - hmn[2]) / head_h, 4)})
        log(key, o.name, "k=", round(k, 4), "post_ratio=", rep["ears"][o.name]["post_ratio"],
            "post_topfrac=", rep["ears"][o.name]["post_topfrac"],
            "post_lobefrac=", rep["ears"][o.name]["post_lobefrac"])
    # assert muc tieu
    for nm, e in rep["ears"].items():
        assert abs(e["post_ratio"] - tgt["f_len"]) < 0.01, f"{key} {nm} ratio off"
        assert abs(e["post_topfrac"] - tgt["f_top"]) < 0.01, f"{key} {nm} topfrac off"
    ADJ[key] = A_by_ear
    LOG["statues"][key] = rep

# ---- cong: truyen A cua A Di Da qua phep dong dang Mc ----
ADJ_AD = ADJ["adida"]
for tag in ("PT", "TD"):
    pairs = []
    for o in bpy.data.objects:
        if not o.name.startswith(f"V10_GateBuddha_{tag}_"):
            continue
        s = bpy.data.objects.get(o.name[len(f"V10_GateBuddha_{tag}_"):])
        if s is not None:
            pairs.append((o, s))
    assert pairs, f"gate {tag} rong"
    # Mc lay tu manh on dinh Head_ushnisha (khong phai pairs[0] tuy y).
    # LUU Y THU TU: tai chinh da bi dieu chinh o tren, nen cap tai se lech
    # Mc ~0.65 mot cach HOP LE (chinh cai lech do phep lien hop se sua) ->
    # loai cap tai khoi kiem tra TRUOC; chi kiem tra cac cap con lai
    # (tru 4 manh tay lech san co).
    ref = [p for p in pairs if base(p[1].name) == "Head_ushnisha"]
    assert ref, f"gate {tag}: khong co Head_ushnisha"
    Mc = ref[0][0].matrix_world @ ref[0][1].matrix_world.inverted()
    devs_pre = {}
    for o, s in pairs:
        if base(s.name) in ("Head_earL", "Head_earR") or base(s.name) in HAND_EXCLUDE:
            continue
        Mi = o.matrix_world @ s.matrix_world.inverted()
        devs_pre[s.name] = max(abs(Mi[r][c] - Mc[r][c]) for r in range(4) for c in range(4))
    mx = max(devs_pre.values())
    sv = np.linalg.svd(np.array(Mc)[:3, :3], compute_uv=False)
    log(f"gate {tag}: parts={len(pairs)} Mc_maxdev(non-ear,non-hand)={mx:.6f} sv={[round(float(v),4) for v in sv]}")
    assert mx < 0.002, f"gate {tag} Mc khong nhat quan"
    assert abs(sv[0] - sv[2]) < 0.001, f"gate {tag} Mc khong phai dong dang deu"
    gear = [(o, s) for o, s in pairs if base(s.name) in ("Head_earL", "Head_earR")]
    created = []
    if gear:
        for o, s in gear:
            Aprime = Mc @ ADJ_AD[base(s.name)] @ Mc.inverted()
            o.matrix_world = Aprime @ o.matrix_world
        bpy.context.view_layer.update()
        log(f"gate {tag}: da truyen A' cho {len(gear)} manh tai co san")
    else:
        # V10 sot manh tai (nhu vu sot net mat o V12): tao bo sung dung mau fix_v12b
        main_ears = {base(o.name): o for o, _ in GROUPS["adida"]
                     if base(o.name) in ("Head_earL", "Head_earR")}
        ref_obj = pairs[0][0]
        for bn, mo in main_ears.items():
            no = bpy.data.objects.new(f"V10_GateBuddha_{tag}_{mo.name}", mo.data)
            ref_obj.users_collection[0].objects.link(no) if ref_obj.users_collection else bpy.context.scene.collection.objects.link(no)
            no.matrix_world = Mc @ mo.matrix_world
            created.append(no.name)
        bpy.context.view_layer.update()
        log(f"gate {tag}: SOT manh tai -> da tao bo sung {created}")
    # kiem chung Mc sau sua van nhat quan (tai phai khop tro lai nho
    # phep lien hop; chi loai 4 manh tay lech san co tu V14)
    mx2 = 0.0
    for o in bpy.data.objects:
        if not o.name.startswith(f"V10_GateBuddha_{tag}_"):
            continue
        s = bpy.data.objects.get(o.name[len(f"V10_GateBuddha_{tag}_"):])
        if s is None or base(s.name) in HAND_EXCLUDE:
            continue
        Mc_i = o.matrix_world @ s.matrix_world.inverted()
        mx2 = max(mx2, max(abs(Mc_i[r][c] - Mc[r][c]) for r in range(4) for c in range(4)))
    log(f"gate {tag}: Mc_maxdev SAU sua (tru tay) = {mx2:.6f}")
    assert mx2 < 0.002, f"gate {tag} Mc vo sau sua"
    LOG["gates"][tag] = {"parts": len(pairs), "Mc_maxdev_pre": round(float(mx), 6),
                         "Mc_maxdev_post": round(float(mx2), 6),
                         "singular": [round(float(v), 4) for v in sv],
                         "gear_existing": len(gear), "created": created,
                         "hand_excluded_preexisting": sorted(HAND_EXCLUDE)}

# ---- don import tam ----
for o in imported_all:
    bpy.data.objects.remove(o, do_unlink=True)
for m in list(bpy.data.materials):
    if m.users == 0 and m.name.startswith("glTF"):
        pass  # giu nguyen, tranh xoa nham; file goc cung chua cac material thua nay neu co
log("cleanup done")

bpy.ops.wm.save_as_mainfile(filepath=DST)
log("SAVED", DST)
with open("/home/hatch/workspace/chua-online-work/layout/v13_audit.json", "w") as f:
    json.dump(LOG, f, indent=1, ensure_ascii=False)
print("BUILD V13 DONE", flush=True)
