"""
BUILD P0 "GIỐNG THẬT" — layout_v4_fixed.blend -> layout_v5_p0.blend
Áp E1–E5 của NGHEN_CUU_GIONG_THAT_V5.md:
  E1 HDRI world + sun grade (AgX, exposure 0.95)
  E2 PBR (BOX projection, Object coords) cho 6 nhóm vật liệu từ textures/ (CC0 Poly Haven)
  E3 Đổi màu toàn cảnh theo bảng B (đo từ ảnh thật)
  E4 AO: AO map trong từng bộ PBR + AO pass qua compositor (nếu API cho phép)
  E5 Nước hồ: màu rêu #4E5F3A + roughness thấp (phản chiếu HDRI) + bump gợn;
     thêm thành hồ đá + lan can thấp quanh 2 hồ
KHÔNG ghi đè bản fixed. Chạy: blender5 -b layout_v4_fixed.blend --python build_p0.py
"""
import bpy, os, math, zlib
from mathutils import Vector

W = "/home/hatch/workspace/chua-online-work/"
TEX = W + "textures/"
OUT = W + "layout_v5_p0.blend"
LOG = []

def log(*a):
    s = " ".join(str(x) for x in a)
    LOG.append(s)
    print(s, flush=True)

def hex_lin(h):
    """sRGB hex -> linear RGB tuple (Blender Base Color space)."""
    h = h.lstrip('#')
    r, g, b = (int(h[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    def f(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return (f(r), f(g), f(b))

def load_img(fname):
    path = TEX + fname
    img = bpy.data.images.get(os.path.basename(fname))
    if img is None:
        img = bpy.data.images.load(path)
    img.filepath = path
    return img

SETS = {
    'plaster':   ('plaster_diff.jpg', 'plaster_rough.jpg', 'plaster_ao.jpg'),
    'rooftiles': ('rooftiles_diff.jpg', 'rooftiles_rough.jpg', 'rooftiles_ao.jpg'),
    'paving':    ('paving_diff.jpg', 'paving_rough.jpg', 'paving_ao.jpg'),
    'concrete':  ('concrete_diff.jpg', 'concrete_rough.jpg', 'concrete_ao.jpg'),
    'wood':      ('wood_diff.jpg', 'wood_rough.jpg', 'wood_ao.jpg'),
    'metal':     ('metal_diff.jpg', 'metal_rough.jpg', 'metal_ao.jpg'),
}
IMGS = {}
for s, files in SETS.items():
    IMGS[s] = tuple(load_img(f) for f in files)
HDRI = load_img('sky_late_afternoon_2k.hdr')

def principled(nt):
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    bs = nt.nodes.new('ShaderNodeBsdfPrincipled')
    nt.links.new(bs.outputs['BSDF'], out.inputs['Surface'])
    return bs

def build_pbr(mat, setname, tint_hex, scale, metallic=0.0, bump=0.3,
              rough_mul=1.0, tint_boost=1.18):
    """Nạp lại node tree của mat: texture BOX x tint (x AO) -> Principled."""
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    bs = principled(nt)
    diff_i, rough_i, ao_i = IMGS[setname]
    tc = nt.nodes.new('ShaderNodeTexCoord')
    mp = nt.nodes.new('ShaderNodeMapping')
    mp.inputs['Scale'].default_value = (scale, scale, scale)
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector'])

    def tex(img, srgb):
        n = nt.nodes.new('ShaderNodeTexImage')
        n.image = img
        n.projection = 'BOX'
        n.projection_blend = 0.25
        if not srgb:
            n.image.colorspace_settings.name = 'Non-Color'
        nt.links.new(mp.outputs['Vector'], n.inputs['Vector'])
        return n

    d = tex(diff_i, True)
    # tint multiply (bù độ sáng trung bình của texture photo ~0.85)
    tint = hex_lin(tint_hex)
    tint = tuple(min(1.0, c * tint_boost) for c in tint)
    mix = nt.nodes.new('ShaderNodeMixRGB'); mix.blend_type = 'MULTIPLY'
    mix.inputs[0].default_value = 1.0
    mix.inputs[2].default_value = (*tint, 1.0)
    nt.links.new(d.outputs['Color'], mix.inputs[1])
    cur = mix.outputs['Color']
    if ao_i is not None:
        a = tex(ao_i, False)
        mix2 = nt.nodes.new('ShaderNodeMixRGB'); mix2.blend_type = 'MULTIPLY'
        mix2.inputs[0].default_value = 1.0
        nt.links.new(cur, mix2.inputs[1])
        nt.links.new(a.outputs['Color'], mix2.inputs[2])
        cur = mix2.outputs['Color']
    nt.links.new(cur, bs.inputs['Base Color'])
    r = tex(rough_i, False)
    if rough_mul != 1.0:
        mm = nt.nodes.new('ShaderNodeMath'); mm.operation = 'MULTIPLY'
        mm.inputs[1].default_value = rough_mul
        nt.links.new(r.outputs['Color'], mm.inputs[0])
        nt.links.new(mm.outputs['Value'], bs.inputs['Roughness'])
    else:
        nt.links.new(r.outputs['Color'], bs.inputs['Roughness'])
    bs.inputs['Metallic'].default_value = metallic
    if bump > 0:
        bw = nt.nodes.new('ShaderNodeRGBToBW')
        nt.links.new(d.outputs['Color'], bw.inputs['Color'])
        bp = nt.nodes.new('ShaderNodeBump')
        bp.inputs['Strength'].default_value = bump
        bp.inputs['Distance'].default_value = 0.12
        nt.links.new(bw.outputs['Val'], bp.inputs['Height'])
        nt.links.new(bp.outputs['Normal'], bs.inputs['Normal'])
    return mat

def build_flat(mat, hexcol, rough=0.85, metallic=0.0):
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    bs = principled(nt)
    bs.inputs['Base Color'].default_value = (*hex_lin(hexcol), 1.0)
    bs.inputs['Roughness'].default_value = rough
    bs.inputs['Metallic'].default_value = metallic
    return mat

def get(name):
    return bpy.data.materials.get(name)

# =====================================================================
# E3 — BẢNG ÁP VẬT LIỆU (tên vật liệu hiện hữu -> xử lý)
# =====================================================================
RULES = [
    # (danh sách tên, set, tint, scale, kwargs)
    (['Ngà sáng', 'Vữa màu vàng kem', 'Vàng tường'], 'plaster', '#D9A441', 0.40, {}),
    (['Chỉ trắng ngà'], 'plaster', '#E8C766', 0.40, {}),
    (['Chỉ màu kem', 'Gờ ngà'], 'plaster', '#EFE3C8', 0.40, {}),
    (['Vôi vàng'], 'plaster', '#E3CD96', 0.40, {}),
    (['Vàng trang trí'], 'plaster', '#C9A227', 0.45, {'rough_mul': 0.6}),
    (['Hoa văn vàng'], 'plaster', '#C9A227', 0.45, {'rough_mul': 0.55, 'metallic': 0.25}),
    (['Gờ vàng'], 'plaster', '#C9962E', 0.45, {'rough_mul': 0.7}),
    (['Gốm xanh'], 'plaster', '#7E2A22', 0.45, {'rough_mul': 0.62}),       # cột teal -> đỏ son
    (['Men gốm xanh'], 'plaster', '#8E2323', 0.45, {'rough_mul': 0.62}),   # bảng trụ teal -> đỏ son
    (['Đỏ son'], 'plaster', '#8E2323', 0.45, {'rough_mul': 0.62}),
    (['Gờ đỏ'], 'plaster', '#A03A2A', 0.45, {}),
    (['Đỏ gạch'], 'rooftiles', '#8A4A34', 0.50, {}),
    (['Kim loại vàng cổ'], 'metal', '#3A332E', 0.80, {'metallic': 0.5, 'rough_mul': 0.9}),  # song sắt -> sắt tối
    (['Mai_Ngoi_Hang'], 'rooftiles', '#7C4030', 0.50, {}),
    (['Mai_Ngoi_Hang_Sang'], 'rooftiles', '#8A4A34', 0.50, {}),
    (['Mai_Ngoi_Layout'], 'rooftiles', '#6E382A', 0.50, {}),
    (['Mái ngói'], 'rooftiles', '#A85A38', 0.50, {}),                      # mái tháp 7 tầng
    (['Đá sân', 'Nền xám sáng'], 'paving', '#8A7A63', 0.30, {'rough_mul': 1.0}),
    (['DarkStone', 'DarkStone.001', 'DarkStone.002', 'Da_Xam'], 'concrete', '#6E675C', 0.50, {}),
    (['Be_Di_Lac_Dark'], 'concrete', '#6E675C', 0.50, {}),
    (['RedBrownPlinth'], 'plaster', '#8A4A3A', 0.45, {}),
    (['Cửa gỗ nâu sẫm', 'Ô cửa'], 'wood', '#5A3D26', 0.70, {}),
    (['Gỗ cửa ấm'], 'wood', '#6B4A2E', 0.70, {}),
    (['KhungGoNauDo', 'KhungGoNauDo.001'], 'wood', '#7A4A34', 0.70, {}),
    (['Thân gỗ'], 'wood', '#83684F', 0.90, {}),
    (['Trắng', 'WhiteStone', 'WhiteStone.001', 'WhiteStone.002', 'DuaSoiTrang'],
     'plaster', '#EFE9DD', 0.55, {'rough_mul': 0.75, 'bump': 0.12}),
]
for names, setname, tint, scale, kw in RULES:
    for n in names:
        m = get(n)
        if m is None:
            log("MISS material:", n); continue
        build_pbr(m, setname, tint, scale, **kw)
        log("PBR", n, "->", setname, tint)

FLATS = [
    (['DarkInset'], '#4A4238', 0.95, 0.0),
    (['Cửa tối'], '#3E322A', 0.92, 0.0),
    (['BlueLotus'], '#4E86A8', 0.60, 0.0),        # đài sen A Di Đà: xanh dương (ref3)
    (['BlueLotusDark'], '#3A6A8A', 0.60, 0.0),
    (['Gốm xanh.001'], '#2C4A8A', 0.35, 0.0),     # mảng gốm cổng: cobalt (bảng B cổng)
    (['FeatureShadow', 'FeatureShadow.001', 'FeatureShadow.002'], '#EFE9DD', 0.60, 0.0),
    (['NenTrangTam', 'NenTrangTam.001', 'SapNenTrangDuc', 'SapNenTrangDuc.001',
      'TrangNga.001', 'TrangNga.002', 'TrangNga.004', 'TrangNga.005', 'TrangNga.006'], '#EFE9DD', 0.65, 0.0),
    (['Vàng kem'], '#E8C766', 0.55, 0.0),
]
for names, col, rough, met in FLATS:
    for n in names:
        m = get(n)
        if m is None:
            log("MISS material:", n); continue
        build_flat(m, col, rough, met)
        log("FLAT", n, "->", col)

# ---- Nền đất lớn (Dat_Co): gạch/đất tông #8A7A63 + mảng tối sáng theo noise ----
m = get('Dat_Co')
if m:
    build_pbr(m, 'paving', '#8A7A63', 0.10, bump=0.15)
    nt = m.node_tree
    bs = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
    # chèn lớp noise nhân tối cục bộ vào Base Color hiện tại
    tc = nt.nodes.new('ShaderNodeTexCoord')
    noise = nt.nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 0.045
    noise.inputs['Detail'].default_value = 3.0
    nt.links.new(tc.outputs['Object'], noise.inputs['Vector'])
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position = 0.35
    ramp.color_ramp.elements[0].color = (0.72, 0.72, 0.72, 1)
    ramp.color_ramp.elements[1].position = 0.75
    ramp.color_ramp.elements[1].color = (1.06, 1.06, 1.06, 1)
    nt.links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
    # lấy đầu vào Base Color hiện tại qua node nhân
    old_link = bs.inputs['Base Color'].links[0]
    src = old_link.from_node; from_sock = old_link.from_socket
    nt.links.remove(old_link)
    mmix = nt.nodes.new('ShaderNodeMixRGB'); mmix.blend_type = 'MULTIPLY'
    mmix.inputs[0].default_value = 1.0
    nt.links.new(from_sock, mmix.inputs[1])
    nt.links.new(ramp.outputs['Color'], mmix.inputs[2])
    nt.links.new(mmix.outputs['Color'], bs.inputs['Base Color'])
    log("GROUND Dat_Co -> paving #8A7A63 + noise patches")

# =====================================================================
# E5 — NƯỚC HỒ: rêu đục + phản chiếu + gợn
# =====================================================================
def build_water(mat):
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    bs = principled(nt)
    tc = nt.nodes.new('ShaderNodeTexCoord')
    noise = nt.nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 2.6
    noise.inputs['Detail'].default_value = 4.0
    nt.links.new(tc.outputs['Object'], noise.inputs['Vector'])
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].color = (*hex_lin('#42532F'), 1)
    ramp.color_ramp.elements[1].color = (*hex_lin('#5A6B40'), 1)
    nt.links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], bs.inputs['Base Color'])
    bs.inputs['Roughness'].default_value = 0.07
    bs.inputs['Metallic'].default_value = 0.0
    bp = nt.nodes.new('ShaderNodeBump')
    bp.inputs['Strength'].default_value = 0.18
    bp.inputs['Distance'].default_value = 0.35
    nt.links.new(noise.outputs['Fac'], bp.inputs['Height'])
    nt.links.new(bp.outputs['Normal'], bs.inputs['Normal'])

for n in ['Nước hồ', 'MatNuocXanhLam']:
    m = get(n)
    if m:
        build_water(m)
        log("WATER", n, "-> #4E5F3A family, rough 0.07, ripple bump")

# =====================================================================
# TÁN CÂY: 3 tông + mottle noise, gán ngẫu nhiên theo object (variation)
# =====================================================================
LEAF_TINTS = [('#3E6B34', '#2F5527'), ('#4C7A3E', '#3A6230'), ('#5C8446', '#4A6E38')]
leaf_mats = []
for i, (hi, lo) in enumerate(LEAF_TINTS):
    lm = bpy.data.materials.new(f"P0_La_{'ABC'[i]}")
    lm.use_nodes = True
    nt = lm.node_tree
    nt.nodes.clear()  # QUAN TRỌNG: không clear -> output mặc định (xám) thắng, cây trắng
    bs = principled(nt)
    tc = nt.nodes.new('ShaderNodeTexCoord')
    noise = nt.nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 5.0
    noise.inputs['Detail'].default_value = 4.0
    nt.links.new(tc.outputs['Object'], noise.inputs['Vector'])
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].color = (*hex_lin(lo), 1)
    ramp.color_ramp.elements[1].color = (*hex_lin(hi), 1)
    nt.links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], bs.inputs['Base Color'])
    bs.inputs['Roughness'].default_value = 0.9
    leaf_mats.append(lm)
n_leaf = 0
for o in bpy.data.objects:
    if o.type != 'MESH':
        continue
    for idx, ms in enumerate(o.data.materials):
        if ms and ms.name == 'Lá':
            o.data.materials[idx] = leaf_mats[zlib.crc32(o.name.encode()) % 3]
            n_leaf += 1
log("LEAF variation: reassigned", n_leaf, "slots to 3 tints")
for n, col in [('Cây xanh', '#4C7A3E'), ('Cây nền', '#466B38')]:
    m = get(n)
    if m:
        build_flat(m, col, 0.9)
        log("FLAT", n, "->", col)

# =====================================================================
# THÁP 7 TẦNG: thân cam đất theo bbox (ghi đè slot sau khi retint toàn局)
# =====================================================================
thap = bpy.data.materials.new("P0_Thap_Than")
build_pbr(thap, 'plaster', '#C88A4A', 0.45, rough_mul=0.85)
OVERRIDE_OK = {'Gờ ngà', 'Vàng tường', 'WhiteStone.002', 'Chỉ màu kem', 'Ngà sáng'}
n_thap = 0
def center(o):
    ws = [o.matrix_world @ Vector(c) for c in o.bound_box]
    return ((min(v.x for v in ws) + max(v.x for v in ws)) / 2,
            (min(v.y for v in ws) + max(v.y for v in ws)) / 2,
            (min(v.z for v in ws) + max(v.z for v in ws)) / 2)
for o in bpy.data.objects:
    if o.type != 'MESH':
        continue
    cx, cy, cz = center(o)
    if -9 < cx < 5 and 33 < cy < 49 and cz > 1.2:
        for idx, ms in enumerate(o.data.materials):
            if ms and ms.name in OVERRIDE_OK:
                o.data.materials[idx] = thap
                n_thap += 1
log("TOWER override slots:", n_thap)

# =====================================================================
# E5b — THÀNH HỒ ĐÁ + LAN CAN THẤP quanh 2 hồ
# =====================================================================
stone_mat = get('DarkStone')
fence_mat = bpy.data.materials.new("P0_Rao_Ho")
build_flat(fence_mat, '#C9962E', 0.45, 0.35)

def add_box(name, loc, dims, mat):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object
    o.name = name
    o.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if mat:
        o.data.materials.append(mat)
    return o

def pond_frame(tag, x0, x1, y0, y1):
    # thành đá: 4 cạnh, cao 0.5, dày 0.45, mặt trên z=0.43
    Lx, Ly = x1 - x0, y1 - y0
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    add_box(f"ThanhHo_{tag}_B", (cx, y1 + 0.225, 0.18), (Lx + 0.9, 0.45, 0.5), stone_mat)
    add_box(f"ThanhHo_{tag}_N", (cx, y0 - 0.225, 0.18), (Lx + 0.9, 0.45, 0.5), stone_mat)
    add_box(f"ThanhHo_{tag}_T", (x0 - 0.225, cy, 0.18), (0.45, Ly, 0.5), stone_mat)
    add_box(f"ThanhHo_{tag}_D", (x1 + 0.225, cy, 0.18), (0.45, Ly, 0.5), stone_mat)
    # lan can: trụ mỗi ~2.2m + tay vịn trên z=0.93
    posts = []
    x = x0
    while x <= x1 + 0.01:
        posts += [(x, y0 - 0.225), (x, y1 + 0.225)]
        x += 2.2
    y = y0 + 2.2
    while y < y1:
        posts += [(x0 - 0.225, y), (x1 + 0.225, y)]
        y += 2.2
    for i, (px, py) in enumerate(posts):
        add_box(f"RaoHo_{tag}_tru_{i}", (px, py, 0.68), (0.07, 0.07, 0.5), fence_mat)
    add_box(f"RaoHo_{tag}_tay_B", (cx, y1 + 0.225, 0.93), (Lx + 0.9, 0.07, 0.07), fence_mat)
    add_box(f"RaoHo_{tag}_tay_N", (cx, y0 - 0.225, 0.93), (Lx + 0.9, 0.07, 0.07), fence_mat)
    add_box(f"RaoHo_{tag}_tay_T", (x0 - 0.225, cy, 0.93), (0.07, Ly, 0.07), fence_mat)
    add_box(f"RaoHo_{tag}_tay_D", (x1 + 0.225, cy, 0.93), (0.07, Ly, 0.07), fence_mat)
    log("POND frame", tag, "posts:", len(posts))

pond_frame("Trai", -4.5, 14.5, -23.5, -8.5)
pond_frame("Phai", 31.5, 50.5, -23.5, -8.5)

# =====================================================================
# E1 — WORLD HDRI + grade
# =====================================================================
sc = bpy.context.scene
w = bpy.data.worlds.new("Troi_P0_HDRI")
sc.world = w
w.use_nodes = True
nt = w.node_tree
nt.nodes.clear()
out = nt.nodes.new('ShaderNodeOutputWorld')
bg = nt.nodes.new('ShaderNodeBackground')
env = nt.nodes.new('ShaderNodeTexEnvironment')
env.image = HDRI
tcw = nt.nodes.new('ShaderNodeTexCoord')
mpw = nt.nodes.new('ShaderNodeMapping')
mpw.inputs['Rotation'].default_value = (0, 0, 0.6)
nt.links.new(tcw.outputs['Generated'], mpw.inputs['Vector'])
nt.links.new(mpw.outputs['Vector'], env.inputs['Vector'])
nt.links.new(env.outputs['Color'], bg.inputs['Color'])
bg.inputs['Strength'].default_value = 0.55
nt.links.new(bg.outputs['Background'], out.inputs['Surface'])
sc.view_settings.view_transform = 'AgX'
sc.view_settings.exposure = 0.95
sun = bpy.data.objects.get('Sun_Layout')
if sun:
    sun.data.energy = 2.6
    sun.data.color = (1.0, 0.82, 0.62)
log("WORLD HDRI set, strength 0.55; sun 2.6 warm; exposure 0.95")

# =====================================================================
# E4 — AO: (1) AO map nhân trong mọi bộ PBR ở trên (factor 1.0);
# (2) bật cờ AO pass của view layer để dành cho hậu kỳ.
# Không gán compositor group: chỉ số socket Mix của Blender 5 chưa kiểm chứng,
# tránh composite sai lên ảnh nghiệm thu. Bóng tiếp xúc ở hốc vòm/chân cột còn
# được hỗ trợ bởi song sắt tối #2B2320 + cửa tối + bóng nắng gắt.
# =====================================================================
try:
    sc.view_layers[0].use_pass_ambient_occlusion = True
    log("AO pass flag ON (texture AO la chinh)")
except Exception as e:
    log("AO pass flag FAILED:", type(e).__name__, str(e)[:120])

# =====================================================================
# CAMERA MỚI: cổng + Di Lặc
# =====================================================================
def add_cam(name, loc, target, lens):
    cd = bpy.data.cameras.new(name)
    cd.lens = lens
    cd.clip_end = 600
    co = bpy.data.objects.new(name, cd)
    sc.collection.objects.link(co)
    co.location = loc
    co.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    log("CAM", name, loc, "->", target)
    return co

add_cam("Cam_Gate", (23, -63, 3.0), (23, -39.5, 5.0), 38)
add_cam("Cam_DiLac", (-13.5, -25.5, 2.8), (-24.5, 3, 4.2), 40)

sc.render.engine = 'CYCLES'
sc.cycles.samples = 32
sc.cycles.use_denoising = True
sc.render.resolution_x = 1280
sc.render.resolution_y = 720

bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=OUT)
log("SAVED ->", OUT)
log("BUILD P0 DONE")
