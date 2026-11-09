"""
V7 — MAT DO SAU (TONG_KET_V6.md muc V7). Mo layout_v8_p3.blend -> luu layout_v9_v7.blend.
KHONG ghi de, KHONG doi grade (tong Sang trong giu nguyen).
Chay: blender5 -b layout_v8_p3.blend --factory-startup -noaudio --python layout/build_v7.py
"""
import bpy, math, random
from mathutils import Vector, Matrix

W = "/home/hatch/workspace/chua-online-work/"
TEX = W + "textures/"
random.seed(20260711)
LOG = []
def log(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)

def bbox(o):
    ws = [o.matrix_world @ Vector(v) for v in o.bound_box]
    xs=[v.x for v in ws]; ys=[v.y for v in ws]; zs=[v.z for v in ws]
    return (min(xs),max(xs),min(ys),max(ys),min(zs),max(zs))
def ctr(o):
    b=bbox(o); return ((b[0]+b[1])/2,(b[2]+b[3])/2)

# ---------------- reuse P2 materials (must exist in v8) ----------------
def mat(name):
    m = bpy.data.materials.get(name)
    assert m is not None, f"missing material {name}"
    return m
LA_A, LA_B, LA_C = mat("P2_LaA"), mat("P2_LaB"), mat("P2_LaC")
LA_A2, LA_C2 = mat("P2_LaA2"), mat("P2_LaC2")
LEAF_MATS = [LA_A, LA_B, LA_C, LA_A2, LA_C2]
CO_A, CO_B = mat("P2_CoA"), mat("P2_CoB")
HOA = mat("P2_HoaGiay")
THAN = mat("P2_ThanCay")
DARKSTONE = bpy.data.materials.get("DarkStone")
DAXAM = bpy.data.materials.get("Da_Xam")

# ---- new materials: moss (noise alpha) + water streak ----
def make_moss_mat():
    m = bpy.data.materials.new("V7_ReuMai"); m.use_nodes = True
    nt = m.node_tree; bs = nt.nodes["Principled BSDF"]
    tc = nt.nodes.new('ShaderNodeTexCoord')
    noise = nt.nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 3.0
    noise.inputs['Detail'].default_value = 3.5
    noise.inputs['Roughness'].default_value = 0.75
    nt.links.new(tc.outputs['Object'], noise.inputs['Vector'])
    ramp_c = nt.nodes.new('ShaderNodeValToRGB')
    ramp_c.color_ramp.elements[0].color = (0.10, 0.16, 0.05, 1)   # dark olive
    ramp_c.color_ramp.elements[0].position = 0.30
    ramp_c.color_ramp.elements[1].color = (0.28, 0.42, 0.14, 1)   # moss green
    ramp_c.color_ramp.elements[1].position = 0.75
    nt.links.new(noise.outputs['Fac'], ramp_c.inputs['Fac'])
    nt.links.new(ramp_c.outputs['Color'], bs.inputs['Base Color'])
    ramp_a = nt.nodes.new('ShaderNodeValToRGB')
    ramp_a.color_ramp.elements[0].position = 0.38
    ramp_a.color_ramp.elements[0].color = (0, 0, 0, 1)
    ramp_a.color_ramp.elements[1].position = 0.62
    ramp_a.color_ramp.elements[1].color = (1, 1, 1, 1)
    nt.links.new(noise.outputs['Fac'], ramp_a.inputs['Fac'])
    nt.links.new(ramp_a.outputs['Color'], bs.inputs['Alpha'])
    bs.inputs['Roughness'].default_value = 1.0
    return m
REU = make_moss_mat()

def plain_alpha_mat(name, rgb, alpha, rough=1.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    bs = m.node_tree.nodes["Principled BSDF"]
    bs.inputs['Base Color'].default_value = (*rgb, 1.0)
    bs.inputs['Alpha'].default_value = alpha
    bs.inputs['Roughness'].default_value = rough
    return m
VET = plain_alpha_mat("V7_VetNuoc", (0.16, 0.19, 0.12), 0.5)

# ---------------- geometry helpers (copied pattern from build_p2.py) ----------------
def quad_obj(name, center, w, h, rot_euler, mtl, uv_sub=None):
    m = (Matrix.Rotation(rot_euler[2], 4, 'Z') @ Matrix.Rotation(rot_euler[1], 4, 'Y')
         @ Matrix.Rotation(rot_euler[0], 4, 'X'))
    c = Vector(center)
    pts = []
    for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        pts.append(c + m @ Vector((sx * w / 2, 0, sy * h / 2)))
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
    if mtl: me.materials.append(mtl)
    return ob

class BoxAcc:
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
    def build(self, name, mtl):
        me = bpy.data.meshes.new(name)
        me.from_pydata(self.v, [], self.f)
        ob = bpy.data.objects.new(name, me)
        bpy.context.collection.objects.link(ob)
        if mtl: me.materials.append(mtl)
        return ob

def cyl_obj(name, center, r_bot, r_top, h, mtl, seg=14):
    bpy.ops.mesh.primitive_cone_add(vertices=seg, radius1=r_bot, radius2=r_top,
                                    depth=h, location=center)
    ob = bpy.context.object; ob.name = name
    if mtl: ob.data.materials.append(mtl)
    return ob

def join_objs(objs, name):
    if not objs: return None
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join()
    ob = bpy.context.object; ob.name = name
    return ob

def canopy_cards(prefix, cx, cy, zc, radius, mtl, seed):
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
            parts.append(quad_obj(f"{prefix}_c{k}", cc, w, h, (tilt, 0, yaw), mtl))
            k += 1
    parts.append(quad_obj(f"{prefix}_top", (cx, cy, zc + 1.45 * radius),
                          1.5 * radius, 1.5 * radius, (math.radians(82), 0, rnd.uniform(0, 3)), mtl))
    return join_objs(parts, prefix)

def new_tree(x, y, ztop, radius, seed, tag):
    cyl_obj("V7_Than", (x, y, ztop / 2), 0.16, 0.10, ztop, THAN, 9)
    mtl = LEAF_MATS[(seed // 100) % len(LEAF_MATS)]
    canopy_cards(f"V7_Tan_{tag}", x, y, ztop + 0.15, radius, mtl, seed=seed)

def palm(x, y, seed):
    rnd = random.Random(seed)
    h = rnd.uniform(5.6, 7.0)
    lean = math.radians(rnd.uniform(2, 6)); lazim = rnd.uniform(0, 6.28)
    segs = []
    px, py, pz = x, y, 0.0
    for i in range(6):
        t = (i + 1) / 6
        nx, ny = x + math.cos(lazim) * lean * h * t * t, y + math.sin(lazim) * lean * h * t * t
        seg = cyl_obj("V7_CoThan", ((px + nx) / 2, (py + ny) / 2, pz + h / 12),
                      0.16 * (1 - t * 0.35), 0.16 * (1 - (t + 0.16) * 0.35), h / 6 + 0.05, THAN, 9)
        segs.append(seg)
        px, py, pz = nx, ny, pz + h / 6
    top = (px, py, h)
    for i in range(3):
        bpy.ops.mesh.primitive_ico_sphere_add(radius=0.13, location=(top[0] + rnd.uniform(-0.16, 0.16),
                                        top[1] + rnd.uniform(-0.16, 0.16), top[2] - 0.18))
        no = bpy.context.object; no.name = "V7_CoQua"; no.data.materials.append(THAN)
        segs.append(no)
    join_objs(segs, "V7_Co")
    fronds = []
    nfr = 10
    for i in range(nfr):
        yaw = (i / nfr) * 2 * math.pi + rnd.uniform(-0.2, 0.2)
        droop = math.radians(rnd.uniform(28, 52))
        L = rnd.uniform(2.6, 3.3)
        mtl = CO_B if i in (2, 7) else CO_A
        for s in range(2):
            segL = L / 2
            d0 = droop + s * math.radians(26)
            cxv = top[0] + math.cos(yaw) * math.cos(d0) * segL * (s + 0.5)
            cyv = top[1] + math.sin(yaw) * math.cos(d0) * segL * (s + 0.5)
            czv = top[2] + 0.15 - math.sin(d0) * segL * (s + 0.5)
            fronds.append(quad_obj("V7_CoLa", (cxv, cyv, czv), segL, 1.05, (0, d0, yaw), mtl))
    join_objs(fronds, "V7_CoTan")

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
            cards.append(quad_obj("V7_HoaCard", (x + ox, y + oy, cz + scale * 0.4),
                                  rr * 1.5, rr * 1.25,
                                  (math.radians(rnd.uniform(-14, 14)), 0, yaw), HOA))
    for j in range(2):
        cards.append(quad_obj("V7_HoaLa", (x + rnd.uniform(-0.3, 0.3), y + rnd.uniform(-0.3, 0.3), z0 + scale * 0.3),
                              scale * 1.3, scale, (math.radians(rnd.uniform(-12, 12)), 0, rnd.uniform(0, 3)), LA_B))
    join_objs(cards, "V7_HoaGiay")

def shrub_bed(x, y, r, seed):
    rnd = random.Random(seed)
    rim = cyl_obj("V7_BedRim", (x, y, 0.18), r, r * 1.08, 0.36, DARKSTONE, 20)
    soil = cyl_obj("V7_BedSoil", (x, y, 0.37), r * 0.92, r * 0.92, 0.05, DAXAM, 20)
    join_objs([rim, soil], "V7_Bed")
    canopy_cards("V7_Bui", x, y, 0.55, r * 0.55, LEAF_MATS[seed % len(LEAF_MATS)], seed=seed)
    flower_cluster(x, y, 0.5, r * 0.55, seed=seed + 7)

# ================= 1. MAT DO SAU: cay moi =================
TREES = [
    # SW quanh A Di Da
    (-30, -32, 2.8, 1.8), (-35, -20, 3.0, 1.9), (-26, -14, 2.6, 1.6), (-15, -33, 2.6, 1.6),
    # quanh thap (chua hanh lang x -2..4)
    (-12, 36, 2.8, 1.8), (12, 37, 2.6, 1.7), (-13, 46, 3.0, 1.9), (-6, 50, 2.6, 1.6),
    # dong-bac
    (38, 28, 2.8, 1.8), (46, 36, 2.6, 1.7), (48, 26, 2.6, 1.6), (44, 46, 2.8, 1.8), (36, 50, 2.6, 1.6),
    # dai dong
    (50, -18, 2.8, 1.8), (50, 14, 2.6, 1.6),
    # dai nam
    (12, -33, 2.6, 1.6), (34, -33, 2.6, 1.6),
    # dai tay
    (-38, 14, 2.8, 1.8), (-38, 26, 2.6, 1.7),
]
for i, (x, y, zt, r) in enumerate(TREES):
    new_tree(x, y, zt, r, seed=7100 + i * 173, tag=f"T{i}")
log("new trees:", len(TREES))

PALMS = [(-20, -35), (-36, -33), (-12, 50), (36, 44), (49, 4), (4, -34), (-38, -4)]
for i, (x, y) in enumerate(PALMS):
    palm(x, y, seed=7900 + i * 211)
log("new palms:", len(PALMS))

BEDS = [(-28, -22, 1.6), (-20, -28, 1.3), (-13, 42, 1.2), (18, 28, 1.2), (26, 30, 1.2)]
for i, (x, y, r) in enumerate(BEDS):
    shrub_bed(x, y, r, seed=8300 + i * 131)
log("shrub beds:", len(BEDS))

FLOWERS = [
    (-30, -40.5), (-10, -40.5), (10, -40.5), (34, -40.5),   # doc rao nam
    (-5, -24.5), (15.5, -8), (30.5, -24.5), (51.5, -8),     # goc ho
    (-14, 40), (2, 52),                                       # chan thap
    (-33, -36), (-8, -38),                                     # tay-nam
    (40, 20), (52, 32),                                        # dong
    (24, 34), (14, 22),                                        # dai bac chanh dien
]
for i, (x, y) in enumerate(FLOWERS):
    flower_cluster(x, y, 0.05, 1.4, seed=8700 + i * 97)
log("new flower clusters:", len(FLOWERS))

# ================= 3. CAY TIEN CANH DAY HON =================
# 8 tan dai lo x=+-8, y -9..12 (gan them chanh dien): them 1 lop card lon hon, thap hon
BONSAI_SPOTS = [(13.0, -6.0), (16.2, -5.8), (29.8, -5.8), (33.0, -6.0)]
trunks_main = [o for o in bpy.data.objects if o.type == 'MESH' and o.name.startswith('Thân cây') and not o.name.startswith('Thân cây nền')]
main_sorted = sorted([o for o in trunks_main if not any(abs(ctr(o)[0]-x) < 0.6 and abs(ctr(o)[1]-y) < 0.6 for x, y in BONSAI_SPOTS)],
                     key=lambda o: (round(ctr(o)[0]), round(ctr(o)[1])))
n_dense = 0
for i, o in enumerate(main_sorted):
    c = ctr(o); b = bbox(o)
    if abs(c[0]) in (8.0,) and -9.5 <= c[1] <= 12.5:
        mtl = LEAF_MATS[i % len(LEAF_MATS)]
        canopy_cards(f"V7_TanDay{i}", c[0], c[1], b[5] - 0.3, 1.8, mtl, seed=9100 + i * 61)
        n_dense += 1
log("densified foreground canopies:", n_dense)

# ================= 2. DECAL REU MAI + VET NUOC CHAN CONG =================
# Mai chanh dien: hang ngoi xay bac thang -> reu nam tren MAT TREN hang (ngang, z = dinh hang + 0.02)
# + MAT DUNG mat nam hang 0 (doc duoc tu goc ground).
moss = []
# --- mat truoc (nam): hang 0 dinh z 7.26 (y -3.7..-2.3), hang 1 dinh z 7.76 (y -2.6..-1.2)
for k, xc in enumerate([10.5, 13.5, 16.5, 19.5, 22.5, 25.5, 28.5, 31.5, 34.5]):
    moss.append(quad_obj("V7_Reu", (xc, -3.0, 7.28), 2.7, 1.2, (math.radians(90), 0, 0), REU))
    moss.append(quad_obj("V7_Reu", (xc, -1.9, 7.78), 2.7, 1.2, (math.radians(90), 0, 0), REU))
    # mat dung hang 0 (y=-3.7), huong nam
    moss.append(quad_obj("V7_Reu", (xc, -3.72, 6.88), 2.7, 0.68, (0, 0, math.radians(180)), REU))
# --- mat sau (bac): hang Sau_0 dinh 7.26 (y 16.8..18.2), Sau_1 dinh 7.76 (y 15.7..17.1)
for k, xc in enumerate([13.5, 18.5, 23.5, 28.5, 33.5]):
    moss.append(quad_obj("V7_Reu", (xc, 17.5, 7.28), 2.7, 1.2, (math.radians(90), 0, 0), REU))
    moss.append(quad_obj("V7_Reu", (xc, 16.4, 7.78), 2.7, 1.2, (math.radians(90), 0, 0), REU))
    moss.append(quad_obj("V7_Reu", (xc, 18.22, 6.88), 2.7, 0.68, (0, 0, 0), REU))
# --- hong dong/tay: mat ngoai + mat tren hang 0 (z dinh 7.50)
for k, yc in enumerate([0.0, 6.0, 12.0]):
    moss.append(quad_obj("V7_Reu", (38.22, yc, 7.0), 2.4, 0.9, (0, math.radians(90), 0), REU))
    moss.append(quad_obj("V7_Reu", (37.65, yc, 7.52), 1.0, 2.4, (math.radians(90), 0, math.radians(90)), REU))
    moss.append(quad_obj("V7_Reu", (7.78, yc, 7.0), 2.4, 0.9, (0, math.radians(-90), 0), REU))
    moss.append(quad_obj("V7_Reu", (8.35, yc, 7.52), 1.0, 2.4, (math.radians(90), 0, math.radians(90)), REU))
join_objs(moss, "V7_ReuMai")
log("moss decal cards:", len(moss))

# vet nuoc chan tru cong (mat nam y=-39.9): 3 vet/tru, 4 tru
streaks = []
rnd = random.Random(555)
for (px0, px1) in [(17.6, 19.2), (26.8, 28.4), (39.6, 41.2), (48.8, 50.4)]:
    for j in range(3):
        sx = px0 + (px1 - px0) * (0.22 + 0.28 * j) + rnd.uniform(-0.05, 0.05)
        wdt = rnd.uniform(0.18, 0.34); hgt = rnd.uniform(0.9, 1.5)
        streaks.append(quad_obj("V7_Vet", (sx, -39.94, 0.05 + hgt / 2), wdt, hgt,
                                (0, 0, math.radians(180)), VET))
join_objs(streaks, "V7_VetNuoc")
log("water streak cards:", len(streaks))

# ================= 4. MAT TUONG DI LAC (khoi lon, co the hoan tac) =================
def scale_about_pivot(obj, pivot, scale):
    M = Matrix.Translation(Vector(pivot)) @ Matrix.Diagonal((*scale, 1.0)) @ Matrix.Translation(-Vector(pivot))
    obj.matrix_world = M @ obj.matrix_world

def translate_obj(obj, d):
    obj.matrix_world = Matrix.Translation(Vector(d)) @ obj.matrix_world

earL = bpy.data.objects.get('Head_earL.001')
earR = bpy.data.objects.get('Head_earR.001')
if earL and earR:
    # dai dai tai: keo Z x1.4 quanh dinh tai (z=8.85)
    scale_about_pivot(earL, (-23.1, -0.9, 8.85), (1.0, 1.0, 1.4))
    scale_about_pivot(earR, (-24.9, -0.9, 8.85), (1.0, 1.0, 1.4))
    log("ears elongated x1.4 Z about top (bottom now ~7.60)")
smile = bpy.data.objects.get('Head_smile')
if smile:
    scale_about_pivot(smile, (-24.0, -0.22, 8.27), (1.3, 1.0, 1.0))
    log("smile widened x1.3")
chL = bpy.data.objects.get('Head_cheekL')
chR = bpy.data.objects.get('Head_cheekR')
if chL and chR:
    translate_obj(chL, (0.06, 0, 0))
    translate_obj(chR, (-0.06, 0, 0))
    log("cheeks widened +-0.06")

# bung tron hon: day dinh Torso theo +Y (mat truoc, huong Bac) trong dai bung z 4.9..6.0,
# falloff muot, KHONG cham nguc (z>6.0: chuoi hat + me ao) va chan (z<4.9)
torso = bpy.data.objects.get('Torso')
if torso:
    me = torso.data
    mw = torso.matrix_world
    mi = mw.inverted()
    n_push = 0
    for v in me.vertices:
        w = mw @ v.co
        # falloff z: 0 tai 4.85 -> 1 tai 5.3 -> 0 tai 6.0
        if w.z < 4.85 or w.z > 6.0:
            continue
        fz = (w.z - 4.85) / 0.45 if w.z < 5.3 else (6.0 - w.z) / 0.7
        fz = max(0.0, min(1.0, fz))
        # chi day phan truoc (y>0.2), manh dan o giua bung
        if w.y <= 0.2:
            continue
        fy = min(1.0, (w.y - 0.2) / 1.0)
        push = 0.14 * fz * fy
        w.y += push
        v.co = mi @ w
        n_push += 1
    me.update()
    log(f"belly pushed: {n_push}/{len(me.vertices)} verts, max +0.14m in band z 4.85..6.0")

# giam phan xa troi xanh tren da trang tuong (giong cach P1 xu ly vang): Specular IOR 0.5 -> 0.25
ws = bpy.data.materials.get('WhiteStone.001')
if ws and ws.use_nodes:
    bs = next((n for n in ws.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
    if bs and 'Specular IOR Level' in bs.inputs:
        bs.inputs['Specular IOR Level'].default_value = 0.25
        log("WhiteStone.001 Specular IOR 0.5 -> 0.25 (bot am xam-xanh mat tuong)")

# ================= LUU BAN MOI =================
bpy.ops.wm.save_as_mainfile(filepath=W + "layout_v9_v7.blend")
log("SAVED layout_v9_v7.blend")
log("SUMMARY trees=%d palms=%d beds=%d flowers=%d dense=%d moss=%d streaks=%d" % (
    len(TREES), len(PALMS), len(BEDS), len(FLOWERS), n_dense, len(moss), len(streaks)))
print("BUILD V7 DONE", flush=True)
