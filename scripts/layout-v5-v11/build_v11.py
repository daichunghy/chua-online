# V11 — GIỐNG THẬT (09/11/2026): layout_v12_v10.blend -> layout_v13_v11.blend
# 1) tầng trang trí mặt tiền theo ref1  2) bệ Di Lặc có mái + tượng choán bệ
# 3) vành đai dừa/cây khối ngoài rào    4) rêu mái mảng rời nhỏ
# 5) mist start/depth + remap nhánh sương (không đụng cổng AO)
import bpy, math, random
from mathutils import Vector

random.seed(11)
SRC = "/home/hatch/workspace/chua-online-work/layout_v12_v10.blend"
DST = "/home/hatch/workspace/chua-online-work/layout_v13_v11.blend"
TEX = "/home/hatch/workspace/chua-online-work/textures/"
bpy.ops.wm.open_mainfile(filepath=SRC)
sc = bpy.context.scene

def bbox(o):
    cs = [o.matrix_world @ Vector(c) for c in o.bound_box]
    return (min(c.x for c in cs), max(c.x for c in cs),
            min(c.y for c in cs), max(c.y for c in cs),
            min(c.z for c in cs), max(c.z for c in cs))

def box(name, loc, size, mat=None, rot=None):
    # Blender 5: transform_apply(scale=True) sau cube_add(location=...) sẽ NẤU
    # location vào mesh rồi zero location -> đặt location lần nữa là gấp đôi.
    # Cách an toàn: tạo tại gốc, set dimensions + rotation + location, không apply.
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
    o = bpy.context.active_object; o.name = name
    o.dimensions = size
    if rot: o.rotation_euler = rot
    o.location = loc
    if mat: o.data.materials.append(mat)
    return o

def sphere(name, loc, r, mat):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc)
    o = bpy.context.active_object; o.name = name
    if mat: o.data.materials.append(mat)
    return o

def principled(mat):
    for n in mat.node_tree.nodes:
        if n.type == 'BSDF_PRINCIPLED': return n
    return None

def img_mat(name, path, rough=0.6, uv_scale=None):
    img = bpy.data.images.load(path)
    img.pack()
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; bs = principled(m); bs.inputs['Roughness'].default_value = rough
    tc = nt.nodes.new('ShaderNodeTexCoord')
    mp = nt.nodes.new('ShaderNodeMapping')
    if uv_scale: mp.inputs['Scale'].default_value = uv_scale
    tx = nt.nodes.new('ShaderNodeTexImage'); tx.image = img; tx.extension = 'REPEAT'
    nt.links.new(tc.outputs['UV'], mp.inputs['Vector'])
    nt.links.new(mp.outputs['Vector'], tx.inputs['Vector'])
    nt.links.new(tx.outputs['Color'], bs.inputs['Base Color'])
    return m

MAT_YELLOW = bpy.data.materials['Vàng tường']
MAT_GOLD = bpy.data.materials['Hoa văn vàng']
MAT_CREAM = bpy.data.materials['Chỉ trắng ngà']
MAT_TILE = bpy.data.materials['Mai_Ngoi_Hang']
MAT_DARKSTONE = bpy.data.materials['DarkStone']
MAT_RED = bpy.data.materials['Đỏ gạch']
MAT_PLINTH = bpy.data.materials['Be_Di_Lac_Dark']

# ================================================================ 5) MIST / SƯƠNG
w = sc.world
w.mist_settings.start = 85.0
w.mist_settings.depth = 560.0
cg = sc.compositing_node_group
fog_link = None
for l in cg.links:
    if l.to_node.name == 'P3_FogFac' and l.from_node.name == 'Render Layers':
        fog_link = l
assert fog_link is not None, "fog link not found"
rl_out = fog_link.from_socket; fog_in = fog_link.to_socket
anchor = (fog_link.from_node.location.x + 180, fog_link.from_node.location.y - 320)
cg.links.remove(fog_link)
scale_node = cg.nodes.new('ShaderNodeMath'); scale_node.name = 'V11_MistScale'
scale_node.operation = 'MULTIPLY'; scale_node.use_clamp = True
scale_node.inputs[1].default_value = 0.45
scale_node.location = anchor
cg.links.new(rl_out, scale_node.inputs[0])
cg.links.new(scale_node.outputs['Value'], fog_in)
print("MIST: start=85 depth=560; fog branch scaled x0.45 (AO gate untouched)")
print("  mist pass @ hall/flycam(d~112m) =", round(max(0.0, (112 - 85) / 560), 3),
      "-> effective fog =", round(max(0.0, (112 - 85) / 560) * 0.45 * 0.15, 4))

# ================================================================ 1) TẦNG TRANG TRÍ MẶT TIỀN
mat_lat = img_mat('V11_Lattice', TEX + 'v11_lattice.png', rough=0.55, uv_scale=(9, 1, 1))
mat_lat_mini = img_mat('V11_LatticeMini', TEX + 'v11_lattice.png', rough=0.55, uv_scale=(0.45, 0.9, 1))
mat_charC = img_mat('V11_CharCenter', TEX + 'v11_char_vinhtrang.png', rough=0.5)
mat_charL = img_mat('V11_CharFu', TEX + 'v11_char_fu.png', rough=0.5)
mat_charR = img_mat('V11_CharTho', TEX + 'v11_char_tho.png', rough=0.5)

FY = -3.55  # mặt phẳng tường tầng trên
box('V11_Tier_Wall', (23, FY, 7.85), (29.6, 0.5, 2.6), MAT_YELLOW)
box('V11_Tier_Base', (23, FY - 0.03, 6.62), (29.8, 0.62, 0.28), MAT_GOLD)
box('V11_Tier_Cornice', (23, FY - 0.03, 9.21), (29.8, 0.62, 0.24), MAT_CREAM)
box('V11_Tier_Relief', (23, FY - 0.27, 7.05), (28.0, 0.1, 0.5), MAT_GOLD)
box('V11_Tier_Lattice', (23, FY - 0.28, 8.2), (28.0, 0.07, 1.5), mat_lat)
# tháp pediment giữa
box('V11_Ped_Body', (23, FY, 10.6), (6.6, 0.55, 2.75), MAT_YELLOW)
box('V11_Ped_Panel', (23, FY - 0.32, 10.8), (3.4, 0.08, 1.7), mat_charC)
box('V11_Ped_LatL', (20.15, FY - 0.31, 10.55), (1.25, 0.07, 1.25), mat_lat_mini)
box('V11_Ped_LatR', (25.85, FY - 0.31, 10.55), (1.25, 0.07, 1.25), mat_lat_mini)
# đầu hồi tam giác (prism): tam giác XZ, extrude theo Y
verts = [(19.9, -3.88, 11.97), (26.1, -3.88, 11.97), (23.0, -3.88, 12.95),
         (19.9, -3.22, 11.97), (26.1, -3.22, 11.97), (23.0, -3.22, 12.95)]
faces = [(0, 1, 2), (5, 4, 3), (0, 2, 5, 3), (2, 1, 4, 5)]
me = bpy.data.meshes.new('V11_Ped_GableMesh'); me.from_pydata(verts, [], faces)
me.materials.append(MAT_YELLOW); me.materials.append(MAT_TILE)
for i, p in enumerate(me.polygons):
    p.material_index = 0 if i < 2 else 1
gable = bpy.data.objects.new('V11_Ped_Gable', me)
sc.collection.objects.link(gable)
sphere('V11_Ped_Finial', (23, FY, 13.22), 0.2, MAT_GOLD)
bpy.ops.mesh.primitive_cylinder_add(radius=0.07, depth=0.2, location=(23, FY, 13.0))
bpy.context.active_object.name = 'V11_Ped_FinialBase'
bpy.context.active_object.data.materials.append(MAT_GOLD)
for fx in (20.35, 25.65):
    sphere('V11_Ped_FinialS', (fx, FY, 12.12), 0.13, MAT_GOLD)
# 2 tháp đầu hồi hai đầu
for px, cm in ((9.9, mat_charL), (36.1, mat_charR)):
    box('V11_Pyl_Body', (px, FY, 8.5), (2.4, 0.6, 3.9), MAT_YELLOW)
    box('V11_Pyl_Panel', (px, FY - 0.34, 9.35), (1.5, 0.08, 1.5), cm)
    bpy.ops.mesh.primitive_cone_add(radius1=1.55, radius2=0.03, depth=0.85, vertices=4,
                                    location=(px, FY, 10.87), rotation=(0, 0, math.radians(45)))
    cap = bpy.context.active_object; cap.name = 'V11_Pyl_Cap'; cap.data.materials.append(MAT_TILE)
    sphere('V11_Pyl_Finial', (px, FY, 11.42), 0.12, MAT_GOLD)
# hàng bảo châu nhỏ trên nóc tầng
for fx in (13.2, 16.4, 18.6, 27.4, 29.6, 32.8):
    sphere('V11_Tier_Finial', (fx, FY, 9.45), 0.11, MAT_GOLD)
print("FACADE TIER built")

# ================================================================ 2) BỆ DI LẶC
STAT_MATS = {'WhiteStone.001', 'FeatureShadow.001', 'DarkInset', 'DiLacFront'}
statue = []
for o in bpy.data.objects:
    if o.type != 'MESH': continue
    mats = {m.name for m in o.data.materials if m}
    if not (mats & STAT_MATS): continue
    b = bbox(o); cx, cy = (b[0] + b[1]) / 2, (b[2] + b[3]) / 2
    if -31 <= cx <= -17 and -3 <= cy <= 3.5:
        statue.append(o)
plat = bpy.data.objects.get('Platform')
assert len(statue) == 93, f"statue parts={len(statue)}"
assert plat is not None
statue.append(plat)
DZ = 1.5  # bệ mới cao hơn mặt kê cũ 1.7 -> 3.2
for o in statue:
    o.location.z += DZ
print(f"STATUE moved +{DZ}: {len(statue)} objects")

old = bpy.data.objects.get('Bệ khu tượng Di Lặc')
assert old is not None
bpy.data.objects.remove(old, do_unlink=True)
box('V11_Terrace', (-24, 0, 0.175), (15, 13, 0.35), MAT_DARKSTONE)
box('V11_PlinthBase', (-24, 0, 0.575), (12.3, 10.0, 0.45), MAT_RED)
box('V11_PlinthBlock', (-24, 0, 1.7), (11.5, 9.2, 1.8), MAT_PLINTH)
box('V11_PlinthCornice', (-24, 0, 2.69), (12.1, 9.8, 0.18), MAT_DARKSTONE)
box('V11_PlinthCap', (-24, 0, 3.125), (11.9, 9.6, 0.15), MAT_DARKSTONE)
# diềm mái ngói quanh đỉnh bệ (4 tấm nghiêng 30 độ)
box('V11_Skirt_F', (-24, 4.95, 2.86), (12.3, 1.04, 0.09), MAT_TILE, rot=(math.radians(-30), 0, 0))
box('V11_Skirt_B', (-24, -4.95, 2.86), (12.3, 1.04, 0.09), MAT_TILE, rot=(math.radians(30), 0, 0))
box('V11_Skirt_L', (-30.3, 0, 2.86), (1.04, 9.0, 0.09), MAT_TILE, rot=(0, math.radians(150), 0))
box('V11_Skirt_R', (-17.7, 0, 2.86), (1.04, 9.0, 0.09), MAT_TILE, rot=(0, math.radians(30), 0))
box('V11_PlinthStep', (-24, 6.8, 0.09), (3.4, 0.6, 0.18), MAT_DARKSTONE)
# chữ vàng trên mặt bệ (bản sao FrontText của tượng, đã nâng cùng tượng)
ft = bpy.data.objects.get('FrontText')
assert ft is not None
dup = ft.copy(); dup.name = 'V11_PlinthText'; sc.collection.objects.link(dup)
b = bbox(dup); ctr = ((b[0] + b[1]) / 2, (b[2] + b[3]) / 2, (b[4] + b[5]) / 2)
dup.location.x += -24 - ctr[0]; dup.location.y += 4.66 - ctr[1]; dup.location.z += 1.72 - ctr[2]
dup.scale = (dup.scale.x * 0.92, dup.scale.y * 0.92, dup.scale.z * 0.92)
print("PLINTH built; FrontText copy bb:", [round(v, 2) for v in bbox(dup)])

# ================================================================ 4) RÊU MÁI MẢNG RỜI
reu = bpy.data.objects.get('V9_ReuMai')
assert reu is not None
bpy.data.objects.remove(reu, do_unlink=True)
img = bpy.data.images.load(TEX + 'v11_moss.png'); img.pack()
mat_moss = bpy.data.materials.new('V11_ReuMai'); mat_moss.use_nodes = True
nt = mat_moss.node_tree; bs = principled(mat_moss); bs.inputs['Roughness'].default_value = 1.0
tx = nt.nodes.new('ShaderNodeTexImage'); tx.image = img
nt.links.new(tx.outputs['Color'], bs.inputs['Base Color'])
nt.links.new(tx.outputs['Alpha'], bs.inputs['Alpha'])

SLOPE = 5.0 / 10.66
TH = math.atan(SLOPE); CT, ST = math.cos(TH), math.sin(TH)
def slope_patch(verts, faces, uvs, cx, cy, r, front=True):
    if front:
        z = 6.5 + (cy + 3.66) * SLOPE
        n = Vector((0, -ST, CT)); v = Vector((0, CT, ST))
    else:
        z = 11.5 - (cy - 7.0) * SLOPE
        n = Vector((0, ST, CT)); v = Vector((0, -CT, ST))
    c = Vector((cx, cy, z)) + n * 0.05
    qx, qy = random.choice((0.0, 0.5)), random.choice((0.0, 0.5))
    base = len(verts)
    verts.append(tuple(c)); uvs.append((qx + 0.25, qy + 0.25))
    N = 9
    angs = sorted(random.uniform(0, 2 * math.pi) for _ in range(N))
    for a in angs:
        rr = r * random.uniform(0.7, 1.3)
        p = c + Vector((math.cos(a) * rr * 1.15, 0, 0)) + v * (math.sin(a) * rr * 0.85)
        verts.append(tuple(p))
        uvs.append((qx + 0.25 + math.cos(a) * 0.23, qy + 0.25 + math.sin(a) * 0.23))
    for i in range(N):
        faces.append((base, base + 1 + i, base + 1 + (i + 1) % N))

mv, mf, muv = [], [], []
for _ in range(14):  # cụm rêu dọc diềm mái trước
    ccx, ccy = random.uniform(9, 37), random.uniform(-3.3, 0.6)
    for _ in range(random.randint(3, 5)):
        slope_patch(mv, mf, muv, ccx + random.gauss(0, 1.5), max(-3.55, min(6.8, ccy + random.gauss(0, 0.5))),
                    random.uniform(0.3, 0.8), front=True)
for _ in range(22):  # rải trên mái trước, một nửa bám rãnh ngói
    x = random.uniform(8.5, 37.5); y = random.uniform(-3.4, 5.8)
    if random.random() < 0.5:
        y = -3.66 + 1.05 * random.randint(1, 9) + random.uniform(-0.18, 0.18)
    slope_patch(mv, mf, muv, x, y, random.uniform(0.3, 0.9), front=True)
for _ in range(20):  # mái sau
    slope_patch(mv, mf, muv, random.uniform(8.5, 37.5), random.uniform(8.0, 16.8),
                random.uniform(0.35, 1.0), front=False)
me = bpy.data.meshes.new('V11_ReuMaiMesh'); me.from_pydata(mv, [], mf)
uvl = me.uv_layers.new(name='UVMap')
for loop in me.loops:
    uvl.data[loop.index].uv = muv[loop.vertex_index]
me.materials.append(mat_moss)
mo = bpy.data.objects.new('V11_ReuMai', me); sc.collection.objects.link(mo)
print("MOSS patches:", len(mf) // 9, "faces:", len(mf))

# ================================================================ 3) VÀNH ĐAI DỪA + CÂY KHỐI
def srgb_lin(c):
    return tuple((v / 255.0) ** 2.2 for v in c)
GREENS = [srgb_lin(h) for h in ((0x3E, 0x6B, 0x34), (0x4A, 0x7A, 0x3C), (0x5C, 0x84, 0x46), (0x2F, 0x55, 0x27))]
BROWN = srgb_lin((0x6B, 0x4A, 0x2E))
FX0, FX1, FY0, FY1 = -38.6, 54.1, -42.1, 53.1
def outd(x, y):
    return max(FX0 - x, x - FX1, FY0 - y, y - FY1)
def excluded(x, y):
    if y < FY0 and y > -85 and ((13 < x < 33) or (35 < x < 53)): return True   # 2 hành lang cổng nam
    if -54.5 < y < -43.5 and -85 < x < 95: return True                          # đường nhựa
    if -44.5 < y < FY0 and -60 < x < 70: return True                            # sân trước rào
    return False
pts = []
grid = {}
def try_add(x, y):
    d = outd(x, y)
    if d < 4 or d > 42 or excluded(x, y): return False
    sp = 4.3 if d < 15 else 5.6
    gx, gy = int(x // 4), int(y // 4)
    for ax in range(gx - 1, gx + 2):
        for ay in range(gy - 1, gy + 2):
            for (px, py) in grid.get((ax, ay), []):
                if (x - px) ** 2 + (y - py) ** 2 < sp * sp: return False
    grid.setdefault((gx, gy), []).append((x, y)); pts.append((x, y, d)); return True
tries = 0
while len(pts) < 340 and tries < 40000:
    tries += 1
    try_add(random.uniform(-95, 115), random.uniform(-95, 110))
print("BELT positions:", len(pts), "tries:", tries)

bv, bf, bc = [], [], []
def push(v, col):
    bv.append(v); bc.append(col); return len(bv) - 1
def quad(a, b, c, dd):
    bf.append((a, b, c, dd))
def prism(cx, cy, h, r0, r1, col, lean=(0.0, 0.0), sides=5):
    idx = []
    for lvl, (rr, zz) in enumerate(((r0, -0.45), (r1, h))):
        ring = []
        for i in range(sides):
            a = i * 2 * math.pi / sides + 0.3
            ox = lean[0] * (zz / h) if lvl else 0.0
            oy = lean[1] * (zz / h) if lvl else 0.0
            ring.append(push((cx + ox + rr * math.cos(a), cy + oy + rr * math.sin(a), zz), col))
        idx.append(ring)
    for i in range(sides):
        j = (i + 1) % sides
        quad(idx[0][i], idx[0][j], idx[1][j], idx[1][i])
def palm(x, y, h):
    lean = (random.uniform(-0.7, 0.7), random.uniform(-0.7, 0.7))
    prism(x, y, h, 0.17, 0.11, BROWN, lean)
    crown = Vector((x + lean[0], y + lean[1], h + 0.15))
    g = random.choice(GREENS)
    nf = random.randint(8, 10)
    L = random.uniform(0.9, 1.15)
    for i in range(nf):
        phi = i * 2 * math.pi / nf + random.uniform(-0.25, 0.25)
        dv = Vector((math.cos(phi), math.sin(phi), 0))
        sv = Vector((-math.sin(phi), math.cos(phi), 0))
        prof = [(0.0, 0.0, 0.30), (1.0 * L, 0.42, 0.26), (2.05 * L, 0.28, 0.16), (3.0 * L, -0.5, 0.03)]
        rows = []
        for dist, dz, hw in prof:
            c = crown + dv * dist + Vector((0, 0, dz))
            rows.append((push(tuple(c - sv * hw), g), push(tuple(c + sv * hw), g)))
        for k in range(3):
            quad(rows[k][0], rows[k][1], rows[k + 1][1], rows[k + 1][0])
def ico_blob(cx, cy, cz, r, seed):
    rnd = random.Random(seed)
    t = (1 + math.sqrt(5)) / 2
    raw = [(-1, t, 0), (1, t, 0), (-1, -t, 0), (1, -t, 0), (0, -1, t), (0, 1, t),
           (0, -1, -t), (0, 1, -t), (t, 0, -1), (t, 0, 1), (-t, 0, -1), (-t, 0, 1)]
    vs = []
    for v in raw:
        vv = Vector(v).normalized()
        vs.append(vv)
    faces = [(0, 11, 5), (0, 5, 1), (0, 1, 7), (0, 7, 10), (0, 10, 11), (1, 5, 9), (5, 11, 4),
             (11, 10, 2), (10, 7, 6), (7, 1, 8), (3, 9, 4), (3, 4, 2), (3, 2, 6), (3, 6, 8),
             (3, 8, 9), (4, 9, 5), (2, 4, 11), (6, 2, 10), (8, 6, 7), (9, 8, 1)]
    def mid(a, b, cache):
        key = (min(a, b), max(a, b))
        if key in cache: return cache[key]
        vv = (vs[a] + vs[b]).normalized(); vs.append(vv)
        cache[key] = len(vs) - 1
        return cache[key]
    cache = {}
    nf = []
    for a, b, c in faces:
        ab, bc2, ca = mid(a, b, cache), mid(b, c, cache), mid(c, a, cache)
        nf += [(a, ab, ca), (b, bc2, ab), (c, ca, bc2), (ab, bc2, ca)]
    g = random.choice(GREENS)
    idx = []
    for i, vv in enumerate(vs):
        f = 1 + (rnd.random() - 0.5) * 0.4
        p = (cx + vv.x * r * f, cy + vv.y * r * f, cz + vv.z * r * f * 0.82)
        shade = 0.85 + 0.3 * max(0.0, vv.z)
        idx.append(push(p, tuple(min(1.0, ch * shade) for ch in g)))
    for a, b, c in nf:
        bf.append((idx[a], idx[b], idx[c]))
def canopy_tree(x, y, seed):
    th = random.uniform(2.6, 3.6)
    prism(x, y, th, 0.15, 0.11, BROWN)
    ico_blob(x + random.uniform(-0.4, 0.4), y + random.uniform(-0.4, 0.4),
             th + random.uniform(1.6, 2.2), random.uniform(2.4, 4.0), seed)
npalm = 0
for i, (x, y, d) in enumerate(pts):
    if random.random() < 0.55:
        palm(x, y, random.uniform(7, 11)); npalm += 1
    else:
        canopy_tree(x, y, 1000 + i)
me = bpy.data.meshes.new('V11_BeltMesh'); me.from_pydata(bv, [], bf)
ca = me.color_attributes.new(name='Col', type='FLOAT_COLOR', domain='POINT')
for i, col in enumerate(bc):
    ca.data[i].color = (col[0], col[1], col[2], 1.0)
me.materials.append(None)
mat_belt = bpy.data.materials.new('V11_BeltVC'); mat_belt.use_nodes = True
nt = mat_belt.node_tree; bs = principled(mat_belt); bs.inputs['Roughness'].default_value = 0.95
vc = nt.nodes.new('ShaderNodeVertexColor'); vc.layer_name = 'Col'
nt.links.new(vc.outputs['Color'], bs.inputs['Base Color'])
me.materials[0] = mat_belt
belt = bpy.data.objects.new('V11_Belt', me); sc.collection.objects.link(belt)
print(f"BELT built: {len(pts)} trees ({npalm} palms), verts={len(bv)}, faces={len(bf)}")

# ================================================================ CAMERAS KIỂM CHỨNG
def add_cam(name, pos, target, lens):
    cd = bpy.data.cameras.new(name); cd.lens = lens
    o = bpy.data.objects.new(name, cd); sc.collection.objects.link(o)
    o.location = pos
    o.rotation_euler = (Vector(target) - Vector(pos)).to_track_quat('-Z', 'Y').to_euler()
    return o
add_cam('Cam_V11_Facade', (23, -27, 5.2), (23, -3.2, 7.4), 40)
add_cam('Cam_V11_DiLac', (-24, 24.5, 5.0), (-24, 0.5, 5.6), 40)
print("CAMS added")

bpy.ops.wm.save_as_mainfile(filepath=DST)
print("SAVED", DST)
