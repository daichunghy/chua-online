"""
V8 — MAT DO SAU (DOT 2) + MAT DI LAC AM (TONG_KET_V6.md muc V7, tiep noi V7).
Mo layout_v9_v7.blend -> luu layout_v10_v8.blend. KHONG ghi de, KHONG doi grade.
Chay: blender5 -b layout_v9_v7.blend --factory-startup -noaudio --python layout/build_v8.py

1) CAY LON HON: 14 cay trong (R 2.4-3.2, ztop 3.6-4.6) vao cac khoang trong con
   lai theo ref9 (SW, quanh thap, dong-bac, dai dong/tay/nam) + 23 cay vong
   NGOAI RAO (R 2.8-3.4, ztop 4.2-5.0) — ref9 cho thay rung bao quanh chua la
   phan lon cua mat do; vong ngoai giu khoang trong dung hanh lang nhin 2 cong
   (khong cay o x 14..32 va 36..52 phia nam ngoai rao).
   Kiem tra chong lap: moi cay moi cach than cay V7 >= 5m; tranh: dai lo
   x -10..10, chanh dien x 8..38/y -2..18, 2 ho, be Di Lac x -34..-14/y -8..14,
   be A Di Da x -18..-8/y -40..-27, be thap x -9..5/y 33..49, be Phat nam
   x 2..24/y 38..54, hanh lang cong x 16..30 & 38.5..51.5/y -42..-38.
2) MAT DI LAC: den fill am Point (khong hien hinh trong render) truoc mat
   tuong (mat huong bac, chi nhan sang troi xanh) + (chi khi test render
   cho thay chua du) nang albedo WhiteStone.001 ve #EFE9DD.
"""
import bpy, math, random
from mathutils import Vector, Matrix

W = "/home/hatch/workspace/chua-online-work/"
random.seed(20260807)
LOG = []
def log(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)

def mat(name):
    m = bpy.data.materials.get(name)
    assert m is not None, f"missing material {name}"
    return m
LA_A, LA_B, LA_C = mat("P2_LaA"), mat("P2_LaB"), mat("P2_LaC")
LA_A2, LA_C2 = mat("P2_LaA2"), mat("P2_LaC2")
LEAF_MATS = [LA_A, LA_B, LA_C, LA_A2, LA_C2]
CO_A, CO_B = mat("P2_CoA"), mat("P2_CoB")
THAN = mat("P2_ThanCay")

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
    cyl_obj("V8_Than", (x, y, ztop / 2), trunk_r, trunk_r * 0.62, ztop, THAN, 9)
    mtl = LEAF_MATS[(seed // 100) % len(LEAF_MATS)]
    canopy_cards(f"V8_Tan_{tag}", x, y, ztop + 0.15, radius, mtl, seed=seed)

def palm(x, y, seed):
    rnd = random.Random(seed)
    h = rnd.uniform(5.6, 7.0)
    lean = math.radians(rnd.uniform(2, 6)); lazim = rnd.uniform(0, 6.28)
    segs = []
    px, py, pz = x, y, 0.0
    for i in range(6):
        t = (i + 1) / 6
        nx, ny = x + math.cos(lazim) * lean * h * t * t, y + math.sin(lazim) * lean * h * t * t
        seg = cyl_obj("V8_CoThan", ((px + nx) / 2, (py + ny) / 2, pz + h / 12),
                      0.16 * (1 - t * 0.35), 0.16 * (1 - (t + 0.16) * 0.35), h / 6 + 0.05, THAN, 9)
        segs.append(seg)
        px, py, pz = nx, ny, pz + h / 6
    top = (px, py, h)
    for i in range(3):
        bpy.ops.mesh.primitive_ico_sphere_add(radius=0.13, location=(top[0] + rnd.uniform(-0.16, 0.16),
                                        top[1] + rnd.uniform(-0.16, 0.16), top[2] - 0.18))
        no = bpy.context.object; no.name = "V8_CoQua"; no.data.materials.append(THAN)
        segs.append(no)
    join_objs(segs, "V8_Co")
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
            fronds.append(quad_obj("V8_CoLa", (cxv, cyv, czv), segL, 1.05, (0, d0, yaw), mtl))
    join_objs(fronds, "V8_CoTan")

# ================= 1a. CAY LON TRONG KHUON VIEN =================
TREES_IN = [
    # SW (x -38..-5, y -42..-5) — tranh be Di Lac (-34..-14, -8..14) va be A Di Da (-18..-8, -40..-27)
    (-33, -38, 4.2, 2.8), (-25, -39, 4.0, 2.6), (-37, -12, 4.4, 3.0),
    (-10, -20, 4.0, 2.6), (-4, -38, 3.8, 2.5),
    # dong-bac (x 28..52, y 18..52) — tranh be Phat nam (2..24, 38..54)
    (30, 36, 4.2, 2.8), (52, 36, 4.0, 2.6), (52, 48, 4.2, 2.8), (30, 48, 4.0, 2.6),
    # dai dong
    (53, -30, 4.2, 2.8), (53, 2, 4.0, 2.6), (53, 30, 4.2, 2.8),
    # quanh thap (tranh be thap -9..5, 33..49)
    (18, 36, 4.2, 2.8), (-16, 54, 4.4, 3.0),
    # dai nam
    (8, -37, 3.8, 2.5),
]
for i, (x, y, zt, r) in enumerate(TREES_IN):
    big_tree(x, y, zt, r, seed=8100 + i * 173, tag=f"IN{i}")
log("big trees inside:", len(TREES_IN))

# ================= 1b. VONG RUNG NGOAI RAO (theo ref9) =================
# rao: x -38.6..54.1, y -42.1..53.1. Vong ngoai cach rao ~4-6m.
# Phia nam CHUA x 14..32 va 36..52 (hanh lang nhin 2 cong tu Cam_Gate).
TREES_OUT = []
for y in (-28, -12, 4, 20, 36, 50):
    TREES_OUT.append((-43, y))
for y in (-28, -12, 4, 20, 36, 50):
    TREES_OUT.append((60, y))
for x in (-32, -16, 0, 16, 32, 48):
    TREES_OUT.append((x, 58))
for x in (-40, -24, -8, 4, 56):
    TREES_OUT.append((x, -46))
for i, (x, y) in enumerate(TREES_OUT):
    big_tree(x, y, 4.6, 3.1, seed=8600 + i * 149, tag=f"OUT{i}", trunk_r=0.26)
log("big trees outside fence:", len(TREES_OUT))

PALMS_OUT = [(-44, -38), (62, -2), (8, 59), (-46, 44)]
for i, (x, y) in enumerate(PALMS_OUT):
    palm(x, y, seed=8900 + i * 211)
log("palms outside:", len(PALMS_OUT))

# ================= 2. DEN FILL AM MAT DI LAC =================
# Mat tuong huong bac (+Y), tam mat ~(-24, -0.2, 8.3). Den Point am dat phia
# bac truoc mat (-24, 9, 8.5); Point KHONG hien hinh trong render (khac Area).
ld = bpy.data.lights.new("V8_FillDiLac", type='POINT')
ld.color = (1.0, 0.72, 0.42)
ld.energy = 1000.0
ld.shadow_soft_size = 0.6
lo = bpy.data.objects.new("V8_FillDiLac", ld)
lo.location = (-24, 9, 8.5)
bpy.context.collection.objects.link(lo)
log("fill light V8_FillDiLac: Point 1000W warm (1.0,0.72,0.42) at (-24,9,8.5)")

# ================= LUU BAN MOI =================
bpy.ops.wm.save_as_mainfile(filepath=W + "layout_v10_v8.blend")
log("SAVED layout_v10_v8.blend")
log("SUMMARY trees_in=%d trees_out=%d palms_out=%d fill=1000W" % (
    len(TREES_IN), len(TREES_OUT), len(PALMS_OUT)))
print("BUILD V8 DONE", flush=True)
