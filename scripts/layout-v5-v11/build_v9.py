"""
V9 — NO CON LAI CUA MODEL (TONG_KET_V6.md + NOTES V7/V8).
Mo layout_v10_v8.blend -> luu layout_v11_v9.blend. KHONG ghi de, KHONG doi
grade (tong Sang trong giu nguyen), KHONG doi vi tri cong trinh/tuong/cong.
Chay: blender5 -b layout_v10_v8.blend --factory-startup -noaudio --python layout/build_v9.py

1) KHOANG TRONG TRONG SAN: 11 cay lon (R 2.4-3.0, ztop 3.8-4.4, kieu V8) vao
   cac khoang lat trong con lon theo flycam V10 (SW quanh A Di Da, tay cua be
   Di Lac, tay-bac, dong-bac sau chanh dien, dai dong, dai nam). Moi cay moi
   duoc KIEM TRA trong script: cach moi than hien co >= 4m, nam trong rao,
   ngoai keep-out (ho, chanh dien, 3 be tuong, be thap, dai lo, hanh lang cong).
2) CAY TRUNG CANH DAY HON: 54 tan hien co (P2_TanCay, P2_TanNen, V7_Tan_T*,
   V8_Tan_IN*) moi tan them 4 card la TRONG tan (cung vat lieu cua tan do) de
   het nhin xuyen tan o khoang cach thuong. Khong cham tan tien canh V7_TanDay
   (da day) va vong rung ngoai rao V8_Tan_OUT (xa camera).
3) REU MAI: lam lai V7_ReuMai (xoa vat + material cu). Material moi V9_ReuMai:
   alpha = noise (UV rieng UVMoss, offset ngau nhien moi card) x edge-falloff
   theo UV 0..1 (mo dan ~30% me card) -> het canh hinh chu nhat sac. Card
   jitter kich thuoc/vi tri/goc, giu nguyen bo cuc + skip pattern cua patch_v7.
   Giu ramp mau G-R cua V7 (do lai sau render).
"""
import bpy, math, random
from mathutils import Vector, Matrix

W = "/home/hatch/workspace/chua-online-work/"
random.seed(20260907)
LOG = []
def log(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)

def bbox(o):
    ws = [o.matrix_world @ Vector(v) for v in o.bound_box]
    xs = [v.x for v in ws]; ys = [v.y for v in ws]; zs = [v.z for v in ws]
    return (min(xs), max(xs), min(ys), max(ys), min(zs), max(zs))
def ctr(o):
    b = bbox(o); return ((b[0]+b[1])/2, (b[2]+b[3])/2, (b[4]+b[5])/2)

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

def quad_obj(name, center, w, h, rot_euler, mtl, uv_sub=None, uv_off=None):
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
    if uv_off is not None:
        uv2 = me.uv_layers.new(name="UVMoss")
        ox, oy = uv_off
        for i in range(4):
            uv2.data[i].uv = (base[i][0] + ox, base[i][1] + oy)
        # UVMap moi phai la active: TexCoord UV (edge falloff) doc theo active
        me.uv_layers["UVMap"].active = True
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

def big_tree(x, y, ztop, radius, seed, tag, trunk_r=0.22):
    cyl_obj("V9_Than", (x, y, ztop / 2), trunk_r, trunk_r * 0.62, ztop, THAN, 9)
    mtl = LEAF_MATS[(seed // 100) % len(LEAF_MATS)]
    canopy_cards(f"V9_Tan_{tag}", x, y, ztop + 0.15, radius, mtl, seed=seed)

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
            cards.append(quad_obj("V9_HoaCard", (x + ox, y + oy, cz + scale * 0.4),
                                  rr * 1.5, rr * 1.25,
                                  (math.radians(rnd.uniform(-14, 14)), 0, yaw), HOA))
    for j in range(2):
        cards.append(quad_obj("V9_HoaLa", (x + rnd.uniform(-0.3, 0.3), y + rnd.uniform(-0.3, 0.3), z0 + scale * 0.3),
                              scale * 1.3, scale, (math.radians(rnd.uniform(-12, 12)), 0, rnd.uniform(0, 3)), LA_B))
    join_objs(cards, "V9_HoaGiay")

def shrub_bed(x, y, r, seed):
    rnd = random.Random(seed)
    rim = cyl_obj("V9_BedRim", (x, y, 0.18), r, r * 1.08, 0.36, DARKSTONE, 20)
    soil = cyl_obj("V9_BedSoil", (x, y, 0.37), r * 0.92, r * 0.92, 0.05, DAXAM, 20)
    join_objs([rim, soil], "V9_Bed")
    canopy_cards("V9_Bui", x, y, 0.55, r * 0.55, LEAF_MATS[seed % len(LEAF_MATS)], seed=seed)
    flower_cluster(x, y, 0.5, r * 0.55, seed=seed + 7)

# ================= KIEM TRA VI TRI (tu probe V9: 77 than, keep-out V8) =================
KEEPOUTS = [  # (x0, x1, y0, y1, ten)
    (8, 38, -2, 18, "chanh dien"), (-4.5, 14.5, -23.5, -8.5, "ho trai"),
    (31.5, 50.5, -23.5, -8.5, "ho phai"), (-34, -14, -8, 14, "be Di Lac"),
    (-18, -8, -40, -27, "be A Di Da"), (-9, 5, 33, 49, "be thap"),
    (2, 24, 38, 54, "be Phat nam"), (16, 30, -42, -38, "hanh lang cong 1"),
    (38.5, 51.5, -42, -38, "hanh lang cong 2"), (-10, 10, -9, 41, "dai lo"),
]
trunks = []
for o in bpy.data.objects:
    if o.type != 'MESH':
        continue
    n = o.name
    if ("Than" in n or "Co." in n) and "Tan" not in n:
        c = ctr(o); trunks.append((n, c[0], c[1]))
log("existing trunks for spacing check:", len(trunks))

def check_pos(x, y, min_dist, label):
    if not (-37.5 <= x <= 53.0 and -41.0 <= y <= 52.0):
        log("REJECT", label, (x, y), "outside fence margin"); return False
    for (x0, x1, y0, y1, nm) in KEEPOUTS:
        if x0 <= x <= x1 and y0 <= y <= y1:
            log("REJECT", label, (x, y), "inside keepout", nm); return False
    for (n, tx, ty) in trunks:
        d = math.hypot(x - tx, y - ty)
        if d < min_dist:
            log("REJECT", label, (x, y), f"too close to {n} ({d:.1f}m < {min_dist}m)")
            return False
    return True

# ================= 1. CAY MOI TRONG SAN =================
TREES_V9 = [
    (-20, -38, 4.2, 2.8), (-35, -25, 4.0, 2.6), (-36, 6, 4.2, 2.8),
    (-25, 45, 4.2, 2.8), (-30, 52, 4.0, 2.6),
    (38, 40, 4.2, 2.8), (26, 42, 4.0, 2.6),
    (44, 8, 4.2, 2.8), (44, 20, 4.0, 2.6),
    (20, -36, 4.0, 2.6), (-2, -30, 4.0, 2.6),
]
n_tree = 0
for i, (x, y, zt, r) in enumerate(TREES_V9):
    if check_pos(x, y, 4.0, f"tree{i}"):
        big_tree(x, y, zt, r, seed=9100 + i * 173, tag=f"IN{i}")
        trunks.append((f"V9_Tan_IN{i}", x, y))
        n_tree += 1
log("new big trees inside:", n_tree, "/", len(TREES_V9))

FLOWERS_V9 = [(12, -5), (36, -4), (-6, -26), (52, -26)]  # (10,-4) bi dai lo chan -> doi (12,-5)
n_fl = 0
for i, (x, y) in enumerate(FLOWERS_V9):
    if check_pos(x, y, 1.0, f"flower{i}"):
        flower_cluster(x, y, 0.05, 1.4, seed=9700 + i * 97)
        n_fl += 1
log("new flower clusters:", n_fl, "/", len(FLOWERS_V9))

BEDS_V9 = [(18, -30, 1.2), (46, -36, 1.2)]
n_bed = 0
for i, (x, y, r) in enumerate(BEDS_V9):
    if check_pos(x, y, 2.0, f"bed{i}"):
        shrub_bed(x, y, r, seed=9300 + i * 131)
        n_bed += 1
log("new shrub beds:", n_bed, "/", len(BEDS_V9))

# ================= 2. DAY TAN TRUNG CANH =================
PREFIXES = ("P2_TanCay", "P2_TanNen", "V7_Tan_T", "V8_Tan_IN")
cans = [o for o in bpy.data.objects if o.type == 'MESH'
        and o.name.startswith(PREFIXES)]
log("mid-ground canopies found:", len(cans))
n_mid = 0
for idx, o in enumerate(sorted(cans, key=lambda v: v.name)):
    b = bbox(o)
    cx, cy, cz = (b[0]+b[1])/2, (b[2]+b[3])/2, (b[4]+b[5])/2
    R = max(b[1]-b[0], b[3]-b[2]) / 2.0
    mtl = o.data.materials[0] if o.data.materials else LA_A
    rnd = random.Random(9500 + idx * 67)
    parts = []
    for k, yaw0 in enumerate((20, 65, 110, 155)):
        yaw = math.radians(yaw0 + rnd.uniform(-10, 10))
        tilt = math.radians(rnd.uniform(-12, 12))
        w = 1.25 * R * rnd.uniform(0.9, 1.1)
        h = 0.75 * R * rnd.uniform(0.9, 1.1)
        cc = (cx + rnd.uniform(-0.2, 0.2) * R, cy + rnd.uniform(-0.2, 0.2) * R,
              cz + rnd.uniform(-0.25, 0.15) * R)
        parts.append(quad_obj(f"V9_Mid_c{k}", cc, w, h, (tilt, 0, yaw), mtl))
    join_objs(parts, f"V9_TanMid_{idx:02d}")
    n_mid += 1
log("mid-ground canopies thickened:", n_mid, "x 4 inner cards")

# ================= 3. REU MAI LAM LAI =================
old = bpy.data.objects.get("V7_ReuMai")
if old:
    bpy.data.objects.remove(old, do_unlink=True)
    log("removed old V7_ReuMai object")
oldmat = bpy.data.materials.get("V7_ReuMai")
if oldmat:
    bpy.data.materials.remove(oldmat)
    log("removed old V7_ReuMai material")

m = bpy.data.materials.new("V9_ReuMai"); m.use_nodes = True
nt = m.node_tree; bs = nt.nodes["Principled BSDF"]
# noise theo UV rieng UVMoss (offset ngau nhien moi card)
uvmap = nt.nodes.new('ShaderNodeUVMap'); uvmap.uv_map = "UVMoss"
noise = nt.nodes.new('ShaderNodeTexNoise')
noise.inputs['Scale'].default_value = 2.5
noise.inputs['Detail'].default_value = 3.5
noise.inputs['Roughness'].default_value = 0.75
nt.links.new(uvmap.outputs['UV'], noise.inputs['Vector'])
ramp_c = nt.nodes.new('ShaderNodeValToRGB')
ramp_c.color_ramp.elements[0].color = (0.05, 0.09, 0.02, 1)
ramp_c.color_ramp.elements[0].position = 0.35
ramp_c.color_ramp.elements[1].color = (0.14, 0.24, 0.07, 1)
ramp_c.color_ramp.elements[1].position = 0.80
nt.links.new(noise.outputs['Fac'], ramp_c.inputs['Fac'])
nt.links.new(ramp_c.outputs['Color'], bs.inputs['Base Color'])
ramp_a = nt.nodes.new('ShaderNodeValToRGB')
ramp_a.color_ramp.elements[0].position = 0.42
ramp_a.color_ramp.elements[0].color = (0, 0, 0, 1)
ramp_a.color_ramp.elements[1].position = 0.70
ramp_a.color_ramp.elements[1].color = (1, 1, 1, 1)
nt.links.new(noise.outputs['Fac'], ramp_a.inputs['Fac'])
# edge falloff theo UV 0..1: alpha *= smoothstep(edge, 0 -> 0.30)
tc = nt.nodes.new('ShaderNodeTexCoord')
sep = nt.nodes.new('ShaderNodeSeparateXYZ')
nt.links.new(tc.outputs['UV'], sep.inputs['Vector'])
def _min_edge(axis):
    sub = nt.nodes.new('ShaderNodeMath'); sub.operation = 'SUBTRACT'
    sub.inputs[0].default_value = 1.0
    nt.links.new(sep.outputs[axis], sub.inputs[1])
    mn = nt.nodes.new('ShaderNodeMath'); mn.operation = 'MINIMUM'
    nt.links.new(sep.outputs[axis], mn.inputs[0])
    nt.links.new(sub.outputs['Value'], mn.inputs[1])
    return mn
minU = _min_edge('X'); minV = _min_edge('Y')
edge = nt.nodes.new('ShaderNodeMath'); edge.operation = 'MINIMUM'
nt.links.new(minU.outputs['Value'], edge.inputs[0])
nt.links.new(minV.outputs['Value'], edge.inputs[1])
ramp_e = nt.nodes.new('ShaderNodeValToRGB')
ramp_e.color_ramp.elements[0].position = 0.0
ramp_e.color_ramp.elements[0].color = (0, 0, 0, 1)
ramp_e.color_ramp.elements[1].position = 0.30
ramp_e.color_ramp.elements[1].color = (1, 1, 1, 1)
nt.links.new(edge.outputs['Value'], ramp_e.inputs['Fac'])
mix = nt.nodes.new('ShaderNodeMixRGB'); mix.blend_type = 'MULTIPLY'
mix.inputs[0].default_value = 1.0
nt.links.new(ramp_a.outputs['Color'], mix.inputs[1])
nt.links.new(ramp_e.outputs['Color'], mix.inputs[2])
nt.links.new(mix.outputs['Color'], bs.inputs['Alpha'])
bs.inputs['Roughness'].default_value = 1.0
log("new moss material V9_ReuMai: UV noise + edge falloff 0.30")

rnd = random.Random(20260907)
moss = []
def moss_card(cx, cy, cz, w, h, rot, jx=0.4, jz=0.08):
    jw = w * rnd.uniform(0.82, 1.18)
    jh = h * rnd.uniform(0.88, 1.12)
    jx2 = cx + rnd.uniform(-jx, jx)
    jz2 = cz + rnd.uniform(0.0, jz)  # chi len, khong chim xuong mai
    rx, ry, rz = rot
    rot2 = (rx + math.radians(rnd.uniform(-4, 4)), ry + math.radians(rnd.uniform(-4, 4)),
            rz + math.radians(rnd.uniform(-8, 8)))
    off = (rnd.uniform(0, 1), rnd.uniform(0, 1))
    return quad_obj("V9_Reu", (jx2, cy, jz2), jw, jh, rot2, m, uv_off=off)
# mat truoc: hang 0 ngang + mat dung hang 0; bo doan thu 4 va 8
for k, xc in enumerate([10.5, 13.5, 16.5, 19.5, 22.5, 25.5, 28.5, 31.5, 34.5]):
    if k in (3, 7):
        continue
    moss.append(moss_card(xc, -3.0, 7.28, 2.7, 1.2, (math.radians(90), 0, 0)))
    moss.append(moss_card(xc, -3.72, 6.88, 2.7, 0.68, (0, 0, math.radians(180)), jx=0.3, jz=0.0))
# mat sau: hang Sau_0 ngang + mat dung
for k, xc in enumerate([13.5, 18.5, 23.5, 28.5, 33.5]):
    if k == 2:
        continue
    moss.append(moss_card(xc, 17.5, 7.28, 2.7, 1.2, (math.radians(90), 0, 0)))
    moss.append(moss_card(xc, 18.22, 6.88, 2.7, 0.68, (0, 0, 0), jx=0.3, jz=0.0))
# hong dong/tay: mat ngoai + mat tren hang 0
for k, yc in enumerate([0.0, 6.0, 12.0]):
    moss.append(moss_card(38.22, yc, 7.0, 2.4, 0.9, (0, math.radians(90), 0), jx=0.3, jz=0.05))
    moss.append(moss_card(37.65, yc, 7.52, 1.0, 2.4, (math.radians(90), 0, math.radians(90)), jx=0.3, jz=0.05))
    moss.append(moss_card(7.78, yc, 7.0, 2.4, 0.9, (0, math.radians(-90), 0), jx=0.3, jz=0.05))
    moss.append(moss_card(8.35, yc, 7.52, 1.0, 2.4, (math.radians(90), 0, math.radians(90)), jx=0.3, jz=0.05))
join_objs(moss, "V9_ReuMai")
log("moss cards rebuilt:", len(moss), "(was 34 in V7)")

# ================= LUU BAN MOI =================
bpy.ops.wm.save_as_mainfile(filepath=W + "layout_v11_v9.blend")
log("SAVED layout_v11_v9.blend")
log("SUMMARY trees=%d flowers=%d beds=%d mid=%d moss=%d" % (n_tree, n_fl, n_bed, n_mid, len(moss)))
print("BUILD V9 DONE", flush=True)
