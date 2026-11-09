"""
P2 — MAT DO & DOI SONG (KE_HOACH_TOAN_DIEN_V6.md muc P2 + dac ta V5 E11/E12/E14)
Mo layout_v6_p1.blend -> lam 6 viec -> luu layout_v7_p2.blend. KHONG ghi de.
Chay: blender5 -b layout_v6_p1.blend --factory-startup -noaudio --python build_p2.py
"""
import bpy, math, random, json
from mathutils import Vector, Matrix

W = "/home/hatch/workspace/chua-online-work/"
TEX = W + "textures/"
random.seed(1127)
LOG = []
def log(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)

def bbox(o):
    ws = [o.matrix_world @ Vector(v) for v in o.bound_box]
    xs=[v.x for v in ws]; ys=[v.y for v in ws]; zs=[v.z for v in ws]
    return (min(xs),max(xs),min(ys),max(ys),min(zs),max(zs))
def ctr(o):
    b=bbox(o); return ((b[0]+b[1])/2,(b[2]+b[3])/2)

# ---------------- materials ----------------
def img_mat(name, imgfile, tint=None, rough=0.9):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; bs = nt.nodes["Principled BSDF"]
    tex = nt.nodes.new('ShaderNodeTexImage')
    tex.image = bpy.data.images.load(TEX + imgfile)
    tex.image.alpha_mode = 'STRAIGHT'
    if tint:
        mix = nt.nodes.new('ShaderNodeMixRGB'); mix.blend_type = 'MULTIPLY'
        mix.inputs[1].default_value = (*tint, 1.0)
        nt.links.new(tex.outputs['Color'], mix.inputs[2])
        nt.links.new(tex.outputs['Alpha'], bs.inputs['Alpha'])
        nt.links.new(mix.outputs['Color'], bs.inputs['Base Color'])
    else:
        nt.links.new(tex.outputs['Color'], bs.inputs['Base Color'])
        nt.links.new(tex.outputs['Alpha'], bs.inputs['Alpha'])
    bs.inputs['Roughness'].default_value = rough
    return m

def plain_mat(name, rgb, rough=0.85, metal=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    bs = m.node_tree.nodes["Principled BSDF"]
    bs.inputs['Base Color'].default_value = (*rgb, 1.0)
    bs.inputs['Roughness'].default_value = rough
    bs.inputs['Metallic'].default_value = metal
    return m

LA_A = img_mat("P2_LaA", "leaf_cluster_A.png")                       # #3E6B34
LA_B = img_mat("P2_LaB", "leaf_cluster_B.png")                       # #4C7A3C
LA_C = img_mat("P2_LaC", "leaf_cluster_C.png")                       # #5C8446
LA_A2 = img_mat("P2_LaA2", "leaf_cluster_A.png", tint=(0.78, 0.82, 0.74))
LA_C2 = img_mat("P2_LaC2", "leaf_cluster_C.png", tint=(1.1, 1.12, 1.02))
LEAF_MATS = [LA_A, LA_B, LA_C, LA_A2, LA_C2]
CO_A = img_mat("P2_CoA", "palm_frond_A.png", rough=0.85)
CO_B = img_mat("P2_CoB", "palm_frond_B.png", rough=0.85)
HOA = img_mat("P2_HoaGiay", "bougainvillea.png", rough=0.85)
THAN = plain_mat("P2_ThanCay", (0.30, 0.22, 0.14), 1.0)
RAO = plain_mat("P2_RaoVang", (0.788, 0.588, 0.180), 0.5, 0.3)        # #C9962E
DONG = plain_mat("P2_DongLu", (0.26, 0.20, 0.12), 0.45, 0.75)
TRO = plain_mat("P2_TroLu", (0.72, 0.70, 0.65), 1.0)
QUE = plain_mat("P2_QueNhang", (0.75, 0.62, 0.42), 0.9)
QUEDAU = plain_mat("P2_DauNhang", (0.45, 0.15, 0.08), 0.8)
GO_BIEN = plain_mat("P2_GoBien", (0.23, 0.15, 0.08), 0.9)
DARKSTONE = bpy.data.materials.get("DarkStone")
GOMXANH = bpy.data.materials.get("Gốm xanh")
CHAUDAT = bpy.data.materials.get("Chậu đất") or plain_mat("P2_ChauDat", (0.55, 0.32, 0.20), 0.95)
DAXAM = bpy.data.materials.get("Da_Xam") or plain_mat("P2_DaXam", (0.42, 0.41, 0.39), 0.95)

def img_mat_opaque(name, imgfile, rough=0.95):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; bs = nt.nodes["Principled BSDF"]
    tex = nt.nodes.new('ShaderNodeTexImage')
    tex.image = bpy.data.images.load(TEX + imgfile)
    nt.links.new(tex.outputs['Color'], bs.inputs['Base Color'])
    bs.inputs['Roughness'].default_value = rough
    return m
LA_RUNG = img_mat_opaque("P2_LaRung", "forest_leaves_diff.jpg")
SIGN_PT = img_mat_opaque("P2_BienPhuongTien", "sign_phuong_tien.png", 0.85)
SIGN_TD = img_mat_opaque("P2_BienTinhDo", "sign_tinh_do.png", 0.85)
CONGDUC = img_mat_opaque("P2_MatCongDuc", "cong_duc_front.png", 0.85)
GODO = img_mat_opaque("P2_GoDo", "wood_diff.jpg", 0.8)
# tint go do son cho thung cong duc: nhan mau qua mix
_bs = GODO.node_tree.nodes["Principled BSDF"]
_mix = GODO.node_tree.nodes.new('ShaderNodeMixRGB'); _mix.blend_type = 'MULTIPLY'
_mix.inputs[1].default_value = (1.35, 0.55, 0.42, 1.0)
_texn = next(n for n in GODO.node_tree.nodes if n.type == 'TEX_IMAGE')
GODO.node_tree.links.new(_texn.outputs['Color'], _mix.inputs[2])
GODO.node_tree.links.new(_mix.outputs['Color'], _bs.inputs['Base Color'])

# ---------------- geometry helpers ----------------
def new_obj(name, verts, faces, mat=None, uvs=None):
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    if uvs:
        uv = me.uv_layers.new(name="UVMap")
        for i, loop in enumerate(me.loops):
            uv.data[i].uv = uvs[loop.vertex_index] if False else None
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    if mat: me.materials.append(mat)
    return ob

def quad_obj(name, center, w, h, rot_euler, mat, uv_sub=None):
    """1 card (plane 2 tam giac) tai center, xoay Euler, UV day du hoac sub-window."""
    m = (Matrix.Rotation(rot_euler[2], 4, 'Z') @ Matrix.Rotation(rot_euler[1], 4, 'Y')
         @ Matrix.Rotation(rot_euler[0], 4, 'X'))
    c = Vector(center)
    pts = []
    for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        p = Vector((sx * w / 2, 0, sy * h / 2))
        pts.append(c + m @ p)
    me = bpy.data.meshes.new(name)
    me.from_pydata(pts, [], [[0, 1, 2, 3]])
    uv = me.uv_layers.new(name="UVMap")
    if uv_sub:
        x0, y0, s = uv_sub
        base = [(x0, y0), (x0 + s, y0), (x0 + s, y0 + s), (x0, y0 + s)]
    else:
        base = [(0, 0), (1, 0), (1, 1), (0, 1)]
    for i in range(4):
        uv.data[i].uv = base[i]
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    if mat: me.materials.append(mat)
    return ob

class BoxAcc:
    """Gom nhieu hop truc thang vao 1 mesh (cho hang rao)."""
    def __init__(self): self.v = []; self.f = []
    def box(self, cx, cy, cz, sx, sy, sz):
        x0, x1 = cx - sx / 2, cx + sx / 2
        y0, y1 = cy - sy / 2, cy + sy / 2
        z0, z1 = cz - sz / 2, cz + sz / 2
        i = len(self.v)
        self.v += [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
                   (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
        self.f += [[i, i + 1, i + 2, i + 3], [i + 4, i + 7, i + 6, i + 5],
                   [i, i + 4, i + 5, i + 1], [i + 1, i + 5, i + 6, i + 2],
                   [i + 2, i + 6, i + 7, i + 3], [i + 3, i + 7, i + 4, i]]
    def build(self, name, mat):
        me = bpy.data.meshes.new(name)
        me.from_pydata(self.v, [], self.f)
        ob = bpy.data.objects.new(name, me)
        bpy.context.collection.objects.link(ob)
        if mat: me.materials.append(mat)
        return ob

def box_obj(name, center, size, mat, rotz=0.0):
    acc = BoxAcc()
    acc.box(0, 0, 0, *size)
    ob = acc.build(name, mat)
    ob.location = center
    ob.rotation_euler = (0, 0, math.radians(rotz))
    return ob

def cyl_obj(name, center, r_bot, r_top, h, mat, seg=14):
    bpy.ops.mesh.primitive_cone_add(vertices=seg, radius1=r_bot, radius2=r_top,
                                    depth=h, location=center)
    ob = bpy.context.object; ob.name = name
    if mat: ob.data.materials.append(mat)
    return ob

def join_objs(objs, name):
    if not objs: return None
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join()
    ob = bpy.context.object; ob.name = name
    return ob

# ---------------- tree canopy builder ----------------
def canopy_cards(prefix, cx, cy, zc, radius, mat, seed):
    rnd = random.Random(seed)
    parts = []
    layers = [(0.35, 1.0, 3), (0.8, 0.85, 3), (1.2, 0.6, 2)]
    k = 0
    for dz, sf, n in layers:
        for i in range(n):
            yaw = math.radians(rnd.uniform(0, 180) + i * (180 / n))
            tilt = math.radians(rnd.uniform(-16, 16))
            w = 2 * radius * sf * rnd.uniform(0.9, 1.12)
            h = radius * 1.15 * sf
            cc = (cx + rnd.uniform(-0.14, 0.14) * radius, cy + rnd.uniform(-0.14, 0.14) * radius,
                  zc + dz * radius)
            parts.append(quad_obj(f"{prefix}_c{k}", cc, w, h, (tilt, 0, yaw), mat))
            k += 1
    # 1 card ngang tren dinh
    parts.append(quad_obj(f"{prefix}_top", (cx, cy, zc + 1.45 * radius),
                          1.5 * radius, 1.5 * radius, (math.radians(82), 0, rnd.uniform(0, 3)), mat))
    return join_objs(parts, prefix)

# ================= 1. THAY CAY KHOI CAU =================
trunks_main = [o for o in bpy.data.objects if o.type == 'MESH' and o.name.startswith('Thân cây') and not o.name.startswith('Thân cây nền')]
trunks_bg = [o for o in bpy.data.objects if o.type == 'MESH' and o.name.startswith('Thân cây nền')]
blobs = [o for o in bpy.data.objects if o.type == 'MESH' and (o.name.startswith('Tán cây') or o.name.startswith('Lá nền'))]
log("P2 trees: trunks_main", len(trunks_main), "trunks_bg", len(trunks_bg), "blobs", len(blobs))

BONSAI_SPOTS = [(13.0, -6.0), (16.2, -5.8), (29.8, -5.8), (33.0, -6.0)]
def is_bonsai_trunk(o):
    c = ctr(o)
    return any(abs(c[0] - x) < 0.6 and abs(c[1] - y) < 0.6 for x, y in BONSAI_SPOTS)

n_canopy = 0
main_sorted = sorted([o for o in trunks_main if not is_bonsai_trunk(o)], key=lambda o: (round(ctr(o)[0]), round(ctr(o)[1])))
for i, o in enumerate(main_sorted):
    c = ctr(o); b = bbox(o)
    mat = LEAF_MATS[i % len(LEAF_MATS)]
    canopy_cards("P2_TanCay", c[0], c[1], b[5] + 0.15, 1.45, mat, seed=1000 + i * 137)
    n_canopy += 1
bg_sorted = sorted(trunks_bg, key=lambda o: (round(ctr(o)[0]), round(ctr(o)[1])))
for i, o in enumerate(bg_sorted):
    c = ctr(o)
    mat = LEAF_MATS[(i + 2) % len(LEAF_MATS)]
    canopy_cards("P2_TanNen", c[0], c[1], 2.6, 2.7, mat, seed=5000 + i * 149)
    n_canopy += 1
log("new canopies:", n_canopy)

# xoa toan bo tan khoi cau cu + than 4 cay bonsai cu
bonsai_trunk_objs = [o for o in trunks_main if is_bonsai_trunk(o)]
for o in blobs + bonsai_trunk_objs:
    bpy.data.objects.remove(o, do_unlink=True)
log("removed blobs+old bonsai trunks:", len(blobs) + len(bonsai_trunk_objs))

# ================= 2. BONSAI truoc chanh dien =================
def bonsai(x, y, seed):
    rnd = random.Random(seed)
    parts = []
    pot = cyl_obj("P2_BonsaiChau", (x, y, 0.26), 0.46, 0.64, 0.52, GOMXANH, 16)
    soil = cyl_obj("P2_BonsaiDat", (x, y, 0.53), 0.56, 0.56, 0.05, DAXAM, 16)
    parts += [pot, soil]
    # than quan queo: 3 doan tru chong lech
    px, py = x, y
    z = 0.55
    for i, (dx, dy, dz, r) in enumerate(((0.05, 0.02, 0.34, 0.13), (-0.09, 0.05, 0.30, 0.10), (0.10, -0.03, 0.28, 0.075))):
        seg = cyl_obj(f"P2_BonsaiThan{i}", (px + dx / 2, py + dy / 2, z + dz / 2), r, r * 0.8, dz + 0.06, THAN, 10)
        seg.rotation_euler = (math.radians(dx * 160), math.radians(-dy * 160), 0)
        parts.append(seg)
        px += dx; py += dy; z += dz
    join_objs(parts, "P2_Bonsai")
    pads = []
    for i, (ox, oy, oz, s) in enumerate(((0.1, 0.05, 1.42, 1.5), (-0.34, -0.1, 1.18, 1.1), (0.36, 0.14, 1.2, 1.05))):
        for j in range(3):
            yaw = math.radians(j * 60 + rnd.uniform(-12, 12))
            pads.append(quad_obj("P2_BonsaiLa", (x + ox, y + oy, oz), s, s * 0.8,
                                 (math.radians(74 + rnd.uniform(-8, 8)), 0, yaw), LA_A))
    join_objs(pads, "P2_BonsaiTan")

for i, (x, y) in enumerate(BONSAI_SPOTS):
    bonsai(x, y, seed=500 + i)
log("bonsai built:", len(BONSAI_SPOTS))

# ================= 3. CO NHIET DOI =================
PALM_SPOTS = [(-30, -38), (34, -38), (30, -25.5), (15, -25.5), (-20, -24), (-24, 14),
              (36, 6), (52, -4), (12, 30), (-30, 20), (44, 30), (20, 44)]
def palm(x, y, seed):
    rnd = random.Random(seed)
    h = rnd.uniform(5.6, 7.0)
    lean = math.radians(rnd.uniform(2, 6)); lazim = rnd.uniform(0, 6.28)
    segs = []
    px, py, pz = x, y, 0.0
    for i in range(6):
        t = (i + 1) / 6
        nx, ny = x + math.cos(lazim) * lean * h * t * t, y + math.sin(lazim) * lean * h * t * t
        seg = cyl_obj("P2_CoThan", ((px + nx) / 2, (py + ny) / 2, pz + h / 12),
                      0.16 * (1 - t * 0.35), 0.16 * (1 - (t + 0.16) * 0.35), h / 6 + 0.05, THAN, 9)
        segs.append(seg)
        px, py, pz = nx, ny, pz + h / 6
    top = (px, py, h)
    for i in range(3):
        nut = bpy.ops.mesh.primitive_ico_sphere_add(radius=0.13, location=(top[0] + rnd.uniform(-0.16, 0.16),
                                        top[1] + rnd.uniform(-0.16, 0.16), top[2] - 0.18))
        no = bpy.context.object; no.name = "P2_CoQua"; no.data.materials.append(THAN)
        segs.append(no)
    join_objs(segs, "P2_Co")
    fronds = []
    nfr = 10
    for i in range(nfr):
        yaw = (i / nfr) * 2 * math.pi + rnd.uniform(-0.2, 0.2)
        droop = math.radians(rnd.uniform(28, 52))
        L = rnd.uniform(2.6, 3.3)
        mat = CO_B if i in (2, 7) else CO_A
        for s in range(2):
            segL = L / 2
            d0 = droop + s * math.radians(26)
            cxv = top[0] + math.cos(yaw) * math.cos(d0) * segL * (s + 0.5)
            cyv = top[1] + math.sin(yaw) * math.cos(d0) * segL * (s + 0.5)
            czv = top[2] + 0.15 - math.sin(d0) * segL * (s + 0.5)
            # card doc theo huong tau: truc dai nam ngang huong yaw, rotX = droop
            fronds.append(quad_obj("P2_CoLa", (cxv, cyv, czv), segL, 1.05,
                                   (0, d0, yaw), mat))
    join_objs(fronds, "P2_CoTan")

for i, (x, y) in enumerate(PALM_SPOTS):
    palm(x, y, seed=900 + i)
log("palms built:", len(PALM_SPOTS))
print("PART1 DONE", flush=True)

# ================= 4. HOA GIAY =================
def flower_cluster(x, y, z0, scale, seed, climb=0.0):
    rnd = random.Random(seed)
    cards = []
    levels = 5 if climb else 3
    for lv in range(levels):
        t = lv / max(1, levels - 1)
        cz = z0 + t * climb + rnd.uniform(0, 0.2)
        rr = scale * (1 - t * 0.35)
        for j in range(3):
            yaw = math.radians(rnd.uniform(0, 180))
            ox = rnd.uniform(-0.3, 0.3) * scale; oy = rnd.uniform(-0.3, 0.3) * scale
            cards.append(quad_obj("P2_HoaCard", (x + ox, y + oy, cz + scale * 0.4),
                                  rr * 1.5, rr * 1.25,
                                  (math.radians(rnd.uniform(-14, 14)), 0, yaw), HOA))
    for j in range(2):
        cards.append(quad_obj("P2_HoaLa", (x + rnd.uniform(-0.3, 0.3), y + rnd.uniform(-0.3, 0.3), z0 + scale * 0.3),
                              scale * 1.3, scale, (math.radians(rnd.uniform(-12, 12)), 0, rnd.uniform(0, 3)), LA_B))
    join_objs(cards, "P2_HoaGiay")

FLOWER_POINTS = []
# cong 1 + cong 2: leo 2 tru moi cong
for (x, y) in [(18.1, -39.6), (27.9, -39.6), (40.1, -39.6), (49.9, -39.6)]:
    flower_cluster(x, y, 0.1, 1.05, seed=int(x * 10), climb=3.0); FLOWER_POINTS.append((x, y))
# 2 ben them chanh dien
for (x, y) in [(17.7, -5.4), (28.3, -5.4)]:
    flower_cluster(x, y, 0.05, 1.15, seed=int(x * 10)); FLOWER_POINTS.append((x, y))
# quanh be A Di Da (mat bac - phia duong di)
for (x, y) in [(-18.6, -27.6), (-7.4, -27.6)]:
    flower_cluster(x, y, 0.05, 1.2, seed=int(-x * 10)); FLOWER_POINTS.append((x, y))
# quanh be Di Lac: 2 goc nam + 2 goc bac (mat truoc)
for (x, y) in [(-34.2, -10.6), (-13.8, -10.6), (-34.2, 8.2), (-13.8, 8.2)]:
    flower_cluster(x, y, 0.05, 1.25, seed=int(x * 7)); FLOWER_POINTS.append((x, y))
# goc rao trong
for (x, y) in [(-37.2, -40.6), (52.6, -40.6)]:
    flower_cluster(x, y, 0.05, 1.1, seed=int(x * 3)); FLOWER_POINTS.append((x, y))
log("flower points:", len(FLOWER_POINTS))

# ================= 5. HANG RAO VANG KIN CHU VI =================
FX0, FX1, FY0, FY1 = -38.5, 54.0, -42.0, 53.0
GAPS_SOUTH = [(16.0, 30.0), (38.5, 51.5)]
def fence_run(axis, fixed, a, b, name):
    acc = BoxAcc()
    length = b - a
    # thanh ngang tren + giua (lien tuc)
    for (rz, rh) in ((1.0, 0.09), (0.55, 0.06)):
        if axis == 'x': acc.box((a + b) / 2, fixed, rz, length, 0.06, rh)
        else: acc.box(fixed, (a + b) / 2, rz, 0.06, length, rh)
    # coc chinh moi ~3.0m + coc dau/cuoi to hon
    n = max(2, int(length / 3.0) + 1)
    for i in range(n + 1):
        t = a + (b - a) * i / n
        if axis == 'x': acc.box(t, fixed, 0.575, 0.2, 0.2, 1.15)
        else: acc.box(fixed, t, 0.575, 0.2, 0.2, 1.15)
        # chop coc
        if axis == 'x': acc.box(t, fixed, 1.19, 0.28, 0.28, 0.08)
        else: acc.box(fixed, t, 1.19, 0.28, 0.28, 0.08)
    # song dung moi 0.5m
    nb = int(length / 0.5)
    for i in range(nb + 1):
        t = a + length * i / nb
        if axis == 'x': acc.box(t, fixed, 0.52, 0.05, 0.05, 0.92)
        else: acc.box(fixed, t, 0.52, 0.05, 0.05, 0.92)
    return acc.build(name, RAO)

fence_runs = []
# mat nam (tru 2 cua cong)
segs = []
cur = FX0
for g0, g1 in GAPS_SOUTH:
    segs.append((cur, g0)); cur = g1
segs.append((cur, FX1))
for i, (a, b) in enumerate(segs):
    if b - a > 0.3: fence_runs.append(fence_run('x', FY0, a, b, f"P2_RaoNam{i}"))
fence_runs.append(fence_run('x', FY1, FX0, FX1, "P2_RaoBac"))
fence_runs.append(fence_run('y', FX0, FY0, FY1, "P2_RaoTay"))
fence_runs.append(fence_run('y', FX1, FY0, FY1, "P2_RaoDong"))
log("fence runs:", len(fence_runs), "rect", (FX0, FX1, FY0, FY1), "gaps", GAPS_SOUTH)

# ================= 6. SCATTER SAN =================
# ghe da x3
for i, (x, y, rz) in enumerate([(15.2, -30.5, 90), (30.8, -30.5, 90), (-19.0, -17.5, 0)]):
    parts = [box_obj("P2_GheChan", (x - 0.65, y, 0.22), (0.18, 0.42, 0.44), DARKSTONE, rz),
             box_obj("P2_GheChan", (x + 0.65, y, 0.22), (0.18, 0.42, 0.44), DARKSTONE, rz),
             box_obj("P2_GheMat", (x, y, 0.48), (1.8, 0.5, 0.1), DARKSTONE, rz)]
    join_objs(parts, "P2_GheDa")
# chau cay nho x6 doc duong chinh + truoc cong
for i, (x, y) in enumerate([(19, -18), (27, -18), (19, -30), (27, -30), (20.5, -37), (25.5, -37)]):
    pot = cyl_obj("P2_ChauNho", (x, y, 0.21), 0.22, 0.3, 0.42, CHAUDAT, 12)
    c1 = quad_obj("P2_ChauLa", (x, y, 0.62), 0.62, 0.5, (0, 0, 0.4), LA_B)
    c2 = quad_obj("P2_ChauLa", (x, y, 0.62), 0.62, 0.5, (0, 0, 1.95), LA_B)
    join_objs([pot, c1, c2], "P2_ChauCay")
# bien chi dan go o 2 cong
def sign(x, y, mat, name):
    p1 = box_obj("P2_BienCot", (x - 0.68, y, 0.95), (0.1, 0.1, 1.9), GO_BIEN)
    p2 = box_obj("P2_BienCot", (x + 0.68, y, 0.95), (0.1, 0.1, 1.9), GO_BIEN)
    board = box_obj("P2_BienBang", (x, y, 1.58), (1.7, 0.07, 0.55), GO_BIEN)
    face = quad_obj("P2_BienMat", (x, y - 0.045, 1.58), 1.66, 0.52, (0, 0, 0), mat)
    join_objs([p1, p2, board], name)
    face.name = name + "_Mat"
sign(16.0, -40.7, SIGN_PT, "P2_BienPhuongTien")
sign(52.1, -40.7, SIGN_TD, "P2_BienTinhDo")
log("signs: Phuong Tien (cong 1), Tinh Do (cong 2)")

# thung cong duc canh cua chanh dien (phai them, canh lan can)
merit = []
merit.append(box_obj("P2_CD_De", (27.9, -4.9, 0.08), (0.72, 0.62, 0.16), DARKSTONE))
merit.append(box_obj("P2_CD_Than", (27.9, -4.9, 0.62), (0.58, 0.48, 0.94), GODO))
merit.append(box_obj("P2_CD_Nap", (27.9, -4.9, 1.13), (0.68, 0.58, 0.07), GODO))
merit.append(box_obj("P2_CD_Khe", (27.9, -5.06, 1.13), (0.3, 0.02, 0.03), GO_BIEN))
join_objs(merit, "P2_ThungCongDuc")
quad_obj("P2_CD_Mat", (27.9, -5.145, 0.66), 0.5, 0.5, (0, 0, 0), CONGDUC)
log("merit box at (27.9,-4.9)")

# ================= 7. LU HUONG (S2 + 2 lu nho) =================
def burner(x, y, s, name):
    parts = [box_obj("P2_LuDe", (x, y, 0.22 * s), (1.05 * s, 1.05 * s, 0.44 * s), DARKSTONE),
             cyl_obj("P2_LuThan", (x, y, (0.44 + 0.28) * s), 0.40 * s, 0.54 * s, 0.56 * s, DONG, 18),
             cyl_obj("P2_LuMieng", (x, y, 1.03 * s), 0.56 * s, 0.56 * s, 0.07 * s, DONG, 18),
             cyl_obj("P2_LuTro", (x, y, 1.0 * s), 0.47 * s, 0.47 * s, 0.05 * s, TRO, 18)]
    join_objs(parts, name)
    sticks = []; tips = []
    rnd = random.Random(int(x * 13 + y))
    for i in range(14):
        ox, oy = rnd.uniform(-0.26, 0.26) * s, rnd.uniform(-0.26, 0.26) * s
        h = rnd.uniform(0.3, 0.42) * s
        st = cyl_obj("P2_Que", (x + ox, y + oy, (1.02 + h / 2) * s), 0.008, 0.008, h, QUE, 5)
        st.rotation_euler = (math.radians(rnd.uniform(-9, 9)), math.radians(rnd.uniform(-9, 9)), 0)
        sticks.append(st)
        tp = cyl_obj("P2_QueDau", (x + ox, y + oy, (1.02 + h) * s), 0.009, 0.009, 0.05 * s, QUEDAU, 5)
        tp.rotation_euler = st.rotation_euler
        tips.append(tp)
    join_objs(sticks, name + "_Que")
    join_objs(tips, name + "_Dau")
burner(23.0, -11.0, 1.25, "P2_LuHuongChinh")
burner(-24.0, -16.3, 0.8, "P2_LuDiLac")
burner(-13.0, -24.2, 0.8, "P2_LuADiDa")
log("burners: main S2 (23,-11) + Di Lac + A Di Da")

# la rung + soi (merged)
acc = BoxAcc()  # dung lai cho soi: hop phang nho
peb_positions = []
rnd = random.Random(4242)
for cx, cy, n in [(-8, -2, 8), (8, 12, 8), (16.5, -16, 6), (-43, 2, 10), (42, 2, 10), (23, -30, 6)]:
    for _ in range(n):
        peb_positions.append((cx + rnd.uniform(-2.2, 2.2), cy + rnd.uniform(-2.2, 2.2)))
for (x, y) in peb_positions:
    s = rnd.uniform(0.1, 0.24)
    acc.box(x, y, 0.03, s, s * 0.8, 0.06)
acc.build("P2_SoiRai", DAXAM)
leaf_parts = []
leaf_zones = [(-8, 5, 26), (8, 12, 26), (-43, 8, 30), (42, 8, 30), (20, -30, 12), (26, -14, 8)]
for (cx, cy, n) in leaf_zones:
    for _ in range(n):
        x = cx + rnd.uniform(-2.6, 2.6); y = cy + rnd.uniform(-3.2, 3.2)
        sub = (rnd.uniform(0, 0.65), rnd.uniform(0, 0.65), 0.35)
        leaf_parts.append(quad_obj("P2_LaRung", (x, y, 0.035), rnd.uniform(0.2, 0.34), rnd.uniform(0.2, 0.34),
                                   (math.radians(90), 0, rnd.uniform(0, 3.14)), LA_RUNG, uv_sub=sub))
join_objs(leaf_parts, "P2_LaRungRai")
log("fallen leaves:", len(leaf_parts), "pebbles:", len(peb_positions))
print("PART2 DONE", flush=True)

# ================= 8. NGUOI — them khach hanh huong =================
def ground_z(x, y):
    dg = bpy.context.evaluated_depsgraph_get()
    hit, loc, *_ = bpy.context.scene.ray_cast(dg, Vector((x, y, 60.0)), Vector((0, 0, -1)))
    if hit and loc.z < 3.0:
        return loc.z
    return 0.0

def tint_outfit(objs, target):
    """Nhuom cum mau vai chiem da so (vertex color) cua geometry_0 + Ao_Trang ve target (linear)."""
    for ob in objs:
        if not (ob.name.startswith('geometry_0') or ob.name.startswith('Ao_Trang')):
            continue
        me = ob.data
        ca = me.color_attributes.active_color if hasattr(me.color_attributes, 'active_color') else None
        if ca is None and len(me.color_attributes) > 0:
            ca = me.color_attributes[0]
        if ca is None:
            log("  tint: no color attr on", ob.name); continue
        cols = [tuple(d.color[:3]) for d in ca.data]
        from collections import Counter
        cnt = Counter(tuple(round(c / 0.04) for c in col) for col in cols)
        modal_key, modal_n = cnt.most_common(1)[0]
        modal = tuple(k * 0.04 for k in modal_key)
        mult = []
        for tc, mc in zip(target, modal):
            m = tc / mc if mc > 0.02 else 1.0
            mult.append(max(0.35, min(2.4, m)))
        changed = 0
        for d in ca.data:
            col = d.color
            key = tuple(round(c / 0.04) for c in col[:3])
            cen = tuple(k * 0.04 for k in key)
            dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(cen, modal)))
            if dist < 0.16:
                d.color = (min(1, col[0] * mult[0]), min(1, col[1] * mult[1]),
                           min(1, col[2] * mult[2]), col[3])
                changed += 1
        log(f"  tint {ob.name}: modal {tuple(round(v,3) for v in modal)} -> target {target}, loops {changed}/{len(cols)}")

def import_person(glb, target, facing, tint=None, tag=""):
    bpy.ops.import_scene.gltf(filepath=W + "characters_fitted/" + glb)
    bpy.context.view_layer.update()
    new = [o for o in bpy.context.selected_objects]
    junk = [o for o in new if o.name.lower().startswith(('ground', 'floor', 'backdrop', 'studio'))]
    for o in junk:
        bpy.data.objects.remove(o, do_unlink=True); new.remove(o)
    if tint:
        tint_outfit(new, tint)
    tops = [o for o in new if o.parent is None] or new
    ws = []
    for o in tops:
        for v in o.bound_box:
            ws.append(o.matrix_world @ Vector(v))
    xs = [v.x for v in ws]; ys = [v.y for v in ws]; zs = [v.z for v in ws]
    cx, cy, minz = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2, min(zs)
    gz = ground_z(target[0], target[1])
    delta = Vector((target[0] - cx, target[1] - cy, gz + 0.02 - minz))
    for o in tops:
        o.location += delta
    bpy.context.view_layer.update()
    rotz = math.radians(180) if facing == 'N' else 0.0
    if rotz:
        R = Matrix.Rotation(rotz, 4, 'Z')
        C = Vector((target[0], target[1], 0))
        for o in tops:
            o.matrix_world = (Matrix.Translation(C) @ R @ Matrix.Translation(-C)) @ o.matrix_world
    bpy.context.view_layer.update()
    log(f"person {tag} {glb} at {target} facing {facing} gz={gz:.2f} objs={len(new)}")
    return tops

LAM = (0.36, 0.40, 0.52); NAU = (0.40, 0.27, 0.17); XAM = (0.42, 0.41, 0.40)
masters = []
masters.append(import_person("nu.glb", (21.3, -7.0), 'N', tint=NAU, tag="S3-nu-nau"))
masters.append(import_person("nam.glb", (21.9, -12.7), 'N', tint=XAM, tag="S2-nam-xam"))
masters.append(import_person("nu.glb", (24.2, -12.6), 'N', tint=XAM, tag="S2-nu-xam"))
masters.append(import_person("nam.glb", (20.3, -33.5), 'S', tint=LAM, tag="path-nam-lam"))
masters.append(import_person("tre.glb", (25.8, -19.8), 'N', tint=NAU, tag="path-tre-nau"))
masters.append(import_person("nu.glb", (-26.5, 12.8), 'S', tint=None, tag="DiLac-nu-lam"))
masters.append(import_person("nam.glb", (-15.5, -23.6), 'S', tint=None, tag="ADiDa-nam-nau"))

def linked_copy(tops, target, delta_rot_deg):
    C = Vector((target[0], target[1], 0))
    # tam hien tai cua master (bbox cac top)
    ws = []
    for o in tops:
        for v in o.bound_box:
            ws.append(o.matrix_world @ Vector(v))
    cx = (min(v.x for v in ws) + max(v.x for v in ws)) / 2
    cy = (min(v.y for v in ws) + max(v.y for v in ws)) / 2
    minz = min(v.z for v in ws)
    gz = ground_z(target[0], target[1])
    delta = Vector((target[0] - cx, target[1] - cy, gz + 0.02 - minz))
    rotz = math.radians(delta_rot_deg)
    out = []
    for o in tops:
        cp = o.copy()
        bpy.context.collection.objects.link(cp)
        m = Matrix.Translation(delta) @ o.matrix_world
        if rotz:
            m = (Matrix.Translation(C) @ Matrix.Rotation(rotz, 4, 'Z') @ Matrix.Translation(-C)) @ m
        cp.matrix_world = m
        out.append(cp)
    bpy.context.view_layer.update()
    log(f"linked copy at {target} delta_rot {delta_rot_deg}")
    return out

linked_copy(masters[3], (27.2, -28.3), 180)   # nam lam (master huong S) -> ban sao huong N
linked_copy(masters[4], (21.5, -37.3), 0)     # tre nau (master huong N) -> giu huong N

people_bodies = [o for o in bpy.data.objects if o.type == 'MESH' and o.name.startswith('geometry_0')]
log("TOTAL people (geometry_0 bodies):", len(people_bodies))

# ================= LUU BAN MOI =================
bpy.ops.wm.save_as_mainfile(filepath=W + "layout_v7_p2.blend")
log("SAVED layout_v7_p2.blend")
log("SUMMARY blobs_removed=%d canopies=%d palms=%d bonsai=%d flowers=%d fence_runs=%d people=%d" % (
    len(blobs), n_canopy, len(PALM_SPOTS), len(BONSAI_SPOTS), len(FLOWER_POINTS),
    len(fence_runs), len(people_bodies)))
print("BUILD P2 DONE", flush=True)
