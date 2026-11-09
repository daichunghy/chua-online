# -*- coding: utf-8 -*-
"""PATCH P1 (theo KE_HOACH_TOAN_DIEN_V6.md) — chạy trên layout_v5_p0.blend,
lưu layout_v6_p1.blend (KHÔNG ghi đè bản P0):
 1) Khôi phục texture nón/túi 0x0 từ characters_fitted/tex/*.png (hết magenta)
 2) Vàng mặt tiền: multiplier albedo mới cho 3 vật liệu tường (đích render #D9A441)
 3) Trời cobalt: world = HDRI (chiếu sáng) + gradient cobalt cho tia camera (Light Path)
 4) Cổng: gắn lại chốt lơ lửng (hạ -2.1m lên mái dưới) + decal câu đối/diềm từ ref6
    + vật liệu gốm mosaic cho trụ cổng
 5) Nền đất: Dat_Co boost 2.8 + mảng noise dịu/mịn; Cây nền tint x1.16, mảng xanh 0.15;
    Đá sân/Nền xám sáng boost 2.9
 7) Thêm camera kiểm chứng bảng chữ: Cam_PlaqueAdida, Cam_PlaquePhatNamN/S
(AO compositor ở patch_p1_comp.py riêng.)
Tham số argv (sau --): wall_mult R G B (mặc định 0.98 0.63 0.10)
"""
import bpy, os, sys, math
from mathutils import Vector

W = "/home/hatch/workspace/chua-online-work/"
TEX = W + "textures/"
GTEX = W + "gate_tex/"
OUT = W + "layout_v6_p1.blend"

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
WALL_MULT = tuple(float(x) for x in argv[:3]) if len(argv) >= 3 else (0.98, 0.63, 0.10)

def log(*a):
    print(" ".join(str(x) for x in a), flush=True)

def hex_lin(h):
    h = h.lstrip('#')
    r, g, b = (int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))
    def f(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return (f(r), f(g), f(b))

def hx(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))

def load_img(path):
    im = bpy.data.images.get(os.path.basename(path))
    if im is None:
        im = bpy.data.images.load(path)
    im.filepath = path
    return im

def build_pbr_mult(mat, diff, rough, ao, mult_rgb, scale, bump=0.30):
    """Dựng lại PBR (BOX/Object) với multiplier albedo cho trước (không qua tint hex)."""
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    bs = nt.nodes.new('ShaderNodeBsdfPrincipled')
    nt.links.new(bs.outputs['BSDF'], out.inputs['Surface'])
    tc = nt.nodes.new('ShaderNodeTexCoord')
    mp = nt.nodes.new('ShaderNodeMapping')
    mp.inputs['Scale'].default_value = (scale, scale, scale)
    nt.links.new(tc.outputs['Object'], mp.inputs['Vector'])
    def tex(fname, noncolor=False):
        n = nt.nodes.new('ShaderNodeTexImage')
        n.image = load_img(TEX + fname)
        if noncolor:
            n.image.colorspace_settings.name = 'Non-Color'
        n.projection = 'BOX'
        n.projection_blend = 0.5
        nt.links.new(mp.outputs['Vector'], n.inputs['Vector'])
        return n
    td = tex(diff)
    mult = nt.nodes.new('ShaderNodeMixRGB'); mult.blend_type = 'MULTIPLY'
    mult.inputs[0].default_value = 1.0
    mult.inputs[2].default_value = (*mult_rgb, 1.0)
    nt.links.new(td.outputs['Color'], mult.inputs[1])
    cur = mult
    if ao:
        ta = tex(ao, True)
        m2 = nt.nodes.new('ShaderNodeMixRGB'); m2.blend_type = 'MULTIPLY'
        m2.inputs[0].default_value = 1.0
        nt.links.new(cur.outputs['Color'], m2.inputs[1])
        nt.links.new(ta.outputs['Color'], m2.inputs[2])
        cur = m2
    nt.links.new(cur.outputs['Color'], bs.inputs['Base Color'])
    tr = tex(rough, True)
    nt.links.new(tr.outputs['Color'], bs.inputs['Roughness'])
    bn = nt.nodes.new('ShaderNodeBump')
    bn.inputs['Strength'].default_value = bump
    nt.links.new(td.outputs['Color'], bn.inputs['Height'])
    nt.links.new(bn.outputs['Normal'], bs.inputs['Normal'])
    return bs

# =====================================================================
# 1) TEXTURE NÓN/TÚI 0x0 -> khôi phục từ file đã trích
# =====================================================================
n_fix = 0
for im in list(bpy.data.images):
    if tuple(im.size) == (0, 0):
        base = im.name.split('.')[0]
        path = W + "characters_fitted/tex/" + base + ".png"
        if os.path.exists(path):
            im.filepath = path
            im.reload()
            im.pack()
            log("TEX FIX", im.name, "->", os.path.basename(path), "size:", tuple(im.size))
            n_fix += 1
        else:
            log("TEX MISS (no file):", im.name)
log("textures restored:", n_fix)

# =====================================================================
# 2) VÀNG MẶT TIỀN — multiplier mới
# =====================================================================
for nm in ('Ngà sáng', 'Vữa màu vàng kem', 'Vàng tường'):
    m = bpy.data.materials.get(nm)
    if m:
        build_pbr_mult(m, "plaster_diff.jpg", "plaster_rough.jpg", "plaster_ao.jpg",
                       WALL_MULT, 0.30, bump=0.25)
        log("WALL mult", nm, WALL_MULT)
    else:
        log("MISS", nm)

# =====================================================================
# 3) TRỜI COBALT — HDRI chiếu sáng + gradient cho camera
# =====================================================================
sc = bpy.context.scene
w = sc.world
w.use_nodes = True
wnt = w.node_tree
wnt.nodes.clear()
out = wnt.nodes.new('ShaderNodeOutputWorld')
tcw = wnt.nodes.new('ShaderNodeTexCoord')
mpw = wnt.nodes.new('ShaderNodeMapping')
mpw.inputs['Rotation'].default_value = (0, 0, 0.6)
env = wnt.nodes.new('ShaderNodeTexEnvironment')
env.image = load_img(TEX + 'sky_blue_clear_2k.hdr')
hs = wnt.nodes.new('ShaderNodeHueSaturation')
hs.inputs['Saturation'].default_value = 1.35
bgA = wnt.nodes.new('ShaderNodeBackground')
bgA.inputs['Strength'].default_value = 0.85
wnt.links.new(tcw.outputs['Generated'], mpw.inputs['Vector'])
wnt.links.new(mpw.outputs['Vector'], env.inputs['Vector'])
wnt.links.new(env.outputs['Color'], hs.inputs['Color'])
wnt.links.new(hs.outputs['Color'], bgA.inputs['Color'])
# nhánh gradient
sep = wnt.nodes.new('ShaderNodeSeparateXYZ')
wnt.links.new(tcw.outputs['Generated'], sep.inputs['Vector'])
ramp = wnt.nodes.new('ShaderNodeValToRGB')
els = ramp.color_ramp.elements
stops = [(0.44, '#DCEFFD'), (0.52, '#4F97F9'), (0.63, '#1E6FD9'), (0.80, '#0155C9')]
els[0].position = stops[0][0]
els[0].color = (*hex_lin(stops[0][1]), 1)
els[1].position = stops[-1][0]
els[1].color = (*hex_lin(stops[-1][1]), 1)
for pos, col in stops[1:-1]:
    el = els.new(pos)
    el.color = (*hex_lin(col), 1)
wnt.links.new(sep.outputs['Z'], ramp.inputs['Fac'])
bgB = wnt.nodes.new('ShaderNodeBackground')
bgB.inputs['Strength'].default_value = 1.0
wnt.links.new(ramp.outputs['Color'], bgB.inputs['Color'])
lp = wnt.nodes.new('ShaderNodeLightPath')
mix = wnt.nodes.new('ShaderNodeMixShader')
wnt.links.new(lp.outputs['Is Camera Ray'], mix.inputs[0])
wnt.links.new(bgA.outputs['Background'], mix.inputs[1])
wnt.links.new(bgB.outputs['Background'], mix.inputs[2])
wnt.links.new(mix.outputs['Shader'], out.inputs['Surface'])
log("WORLD: HDRI lighting + cobalt gradient camera branch")

# =====================================================================
# 4a) CỔNG — gắn lại chốt lơ lửng
# =====================================================================
def bbox(o):
    ws = [o.matrix_world @ Vector(c) for c in o.bound_box]
    return (min(v.x for v in ws), max(v.x for v in ws),
            min(v.y for v in ws), max(v.y for v in ws),
            min(v.z for v in ws), max(v.z for v in ws))

slabs = []
for o in bpy.data.objects:
    if o.name.startswith('Tầng mái cổng'):
        b = bbox(o)
        if 9.85 < b[4] and b[5] < 10.2:  # mái trên cùng z 9.9..10.1
            slabs.append((b[0], b[1]))
log("top slabs x-ranges:", slabs)
n_moved = 0
for o in bpy.data.objects:
    if o.name.startswith(('Châu cổng', 'Chóp cổng')):
        b = bbox(o)
        cx = (b[0] + b[1]) / 2
        on_slab = any(s0 - 0.05 <= cx <= s1 + 0.05 for s0, s1 in slabs)
        if not on_slab:
            o.location.z -= 2.1
            n_moved += 1
            log("FINIAL reattached:", o.name, "cx=", round(cx, 1), "dz=-2.1")
log("finials moved:", n_moved)

# =====================================================================
# 4b) CỔNG — vật liệu gốm mosaic cho trụ + decal photo từ ref6
# =====================================================================
def build_tex_mat(name, fname, rough=0.5, box=False, scale=0.5, tint=(1.0, 1.0, 1.0)):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    o = nt.nodes.new('ShaderNodeOutputMaterial')
    bs = nt.nodes.new('ShaderNodeBsdfPrincipled')
    nt.links.new(bs.outputs['BSDF'], o.inputs['Surface'])
    t = nt.nodes.new('ShaderNodeTexImage')
    t.image = load_img(GTEX + fname)
    if box:
        tc = nt.nodes.new('ShaderNodeTexCoord')
        mp = nt.nodes.new('ShaderNodeMapping')
        mp.inputs['Scale'].default_value = (scale, scale, scale)
        nt.links.new(tc.outputs['Object'], mp.inputs['Vector'])
        nt.links.new(mp.outputs['Vector'], t.inputs['Vector'])
        t.projection = 'BOX'
        t.projection_blend = 0.4
    if tint != (1.0, 1.0, 1.0):
        mx = nt.nodes.new('ShaderNodeMixRGB'); mx.blend_type = 'MULTIPLY'
        mx.inputs[0].default_value = 1.0
        mx.inputs[2].default_value = (*tint, 1.0)
        nt.links.new(t.outputs['Color'], mx.inputs[1])
        nt.links.new(mx.outputs['Color'], bs.inputs['Base Color'])
    else:
        nt.links.new(t.outputs['Color'], bs.inputs['Base Color'])
    bs.inputs['Roughness'].default_value = rough
    return m

tru_mat = build_tex_mat('P1_GomTru', 'mosaic_sq.png', rough=0.5, box=True,
                        scale=0.5, tint=(1.03, 0.99, 0.90))
n_tru = 0
for o in bpy.data.objects:
    if o.name.startswith(('Trụ cổng', 'Trụ tầng trên cổng')) and o.type == 'MESH':
        if len(o.data.materials):
            o.data.materials[0] = tru_mat
        else:
            o.data.materials.append(tru_mat)
        n_tru += 1
log("pillar mosaic assigned:", n_tru)

matL = build_tex_mat('P1_Decal_CouL', 'couplet_L.png', rough=0.55)
matR = build_tex_mat('P1_Decal_CouR', 'couplet_R.png', rough=0.55)
matF = build_tex_mat('P1_Decal_Frieze', 'frieze.png', rough=0.55)

def add_decal(name, cx, cy, cz, wdt, hgt, mat):
    bpy.ops.mesh.primitive_plane_add(size=1, location=(cx, cy, cz))
    o = bpy.context.object
    o.name = name
    o.scale = (wdt, hgt, 1.0)
    o.rotation_euler = (math.pi / 2, 0, 0)
    o.data.materials.append(mat)
    return o

GATES = [(18.4, 27.6, 23.0), (40.4, 49.6, 45.0)]  # (trụ trái, trụ phải, tâm) mỗi cổng
for gi, (lx, rx, cx) in enumerate(GATES):
    add_decal(f"P1_Decal_CouL_{gi}", lx, -39.97, 2.95, 0.95, 3.3, matL)
    add_decal(f"P1_Decal_CouR_{gi}", rx, -39.97, 2.95, 0.95, 3.3, matR)
    add_decal(f"P1_Decal_Frieze_{gi}", cx, -40.06, 6.60, 9.8, 1.9, matF)
    log("decals gate", gi, "at pillars", lx, rx)

# =====================================================================
# 5) NỀN ĐẤT
# =====================================================================
m = bpy.data.materials.get('Dat_Co')
if m:
    bs = build_pbr_mult(m, "paving_diff.jpg", "paving_rough.jpg", "paving_ao.jpg",
                        tuple(c * 2.8 for c in hx('#9A8A72')), 0.10, bump=0.30)
    nt = m.node_tree
    tc = next(n for n in nt.nodes if n.type == 'TEX_COORD')
    noise = nt.nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 0.085
    noise.inputs['Detail'].default_value = 6.0
    nt.links.new(tc.outputs['Generated'], noise.inputs['Vector'])
    ramp2 = nt.nodes.new('ShaderNodeValToRGB')
    ramp2.color_ramp.elements[0].position = 0.35
    ramp2.color_ramp.elements[0].color = (1, 1, 1, 1)
    ramp2.color_ramp.elements[1].position = 0.75
    ramp2.color_ramp.elements[1].color = (0.90, 0.90, 0.90, 1)
    nt.links.new(noise.outputs['Fac'], ramp2.inputs['Fac'])
    old = bs.inputs['Base Color'].links[0]
    src_sock = old.from_socket
    nt.links.remove(old)
    m3 = nt.nodes.new('ShaderNodeMixRGB'); m3.blend_type = 'MULTIPLY'
    m3.inputs[0].default_value = 1.0
    nt.links.new(src_sock, m3.inputs[1])
    nt.links.new(ramp2.outputs['Color'], m3.inputs[2])
    nt.links.new(m3.outputs['Color'], bs.inputs['Base Color'])
    log("Dat_Co: boost 2.8, noise patches 0.90 @ scale 0.085")

for nm in ('Đá sân', 'Nền xám sáng'):
    mm = bpy.data.materials.get(nm)
    if mm:
        build_pbr_mult(mm, "paving_diff.jpg", "paving_rough.jpg", "paving_ao.jpg",
                       tuple(c * 2.9 for c in hx('#9A8A72')), 0.30, bump=0.30)
        log("paving boost 2.9:", nm)

m = bpy.data.materials.get('Cây nền')
if m:
    nt = m.node_tree
    for n in nt.nodes:
        if n.type == 'MIX_RGB' and n.blend_type == 'MULTIPLY':
            v = n.inputs[2].default_value
            if not n.inputs[2].links and v[0] > 1.0:  # node tint lát
                n.inputs[2].default_value = (v[0] * 1.16, v[1] * 1.16, v[2] * 1.16, 1)
                log("Cây nền tint x1.16 ->", tuple(round(x, 2) for x in n.inputs[2].default_value[:3]))
        if n.type == 'VALTORGB':
            n.color_ramp.elements[1].color = (0.15, 0.15, 0.15, 1)
            log("Cây nền green patch max -> 0.15")
        if n.type == 'TEX_NOISE':
            n.inputs['Scale'].default_value = 5.0
            log("Cây nền noise scale -> 5.0")

# =====================================================================
# 7) CAMERA KIỂM CHỨNG BẢNG CHỮ
# =====================================================================
def add_cam(name, loc, target, lens):
    if bpy.data.objects.get(name):
        return
    cd = bpy.data.cameras.new(name)
    cd.lens = lens
    cd.clip_end = 600
    co = bpy.data.objects.new(name, cd)
    sc.collection.objects.link(co)
    co.location = loc
    co.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    log("CAM", name, loc)

add_cam("Cam_PlaqueAdida", (-14, -19.5, 1.5), (-14, -29.1, 0.75), 55)
add_cam("Cam_PlaquePhatNamN", (12, 63, 4.8), (12, 49.7, 4.1), 42)
add_cam("Cam_PlaquePhatNamS", (12, 36, 4.8), (12, 49.7, 4.1), 42)

bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=OUT)
log("SAVED ->", OUT, os.path.getsize(OUT))
log("PATCH P1 DONE")
