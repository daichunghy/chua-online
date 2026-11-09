"""
PATCH P0 vòng 2 — sửa trên layout_v5_p0.blend (ghi đè cùng file):
1. Vật liệu lá P0_La_A/B/C: node tree còn output mặc định chưa clear -> cây xám trắng.
   Dựng lại sạch.
2. 'Cây nền' (mặt đất khuôn viên 13.125 m2): từ xanh lawn phẳng -> gạch/đất #7A6A52
   có mảng xanh #55703F theo noise.
3. Vàng chánh điện quá nhạt: tint sâu hơn (#C08A28 / #DFAF4E, boost 1.15).
4. Gạch lát quá tối: boost tint 1.9 cho Đá sân / Nền xám sáng / Dat_Co.
5. Trời: world strength 0.55 -> 0.8.
Chạy: blender5 -b layout_v5_p0.blend --python patch_p0.py
"""
import bpy, os
from mathutils import Vector

W = "/home/hatch/workspace/chua-online-work/"
TEX = W + "textures/"

def log(*a):
    print(" ".join(str(x) for x in a), flush=True)

def hex_lin(h):
    h = h.lstrip('#')
    r, g, b = (int(h[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    def f(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return (f(r), f(g), f(b))

def load_img(fname):
    img = bpy.data.images.get(fname)
    if img is None:
        img = bpy.data.images.load(TEX + fname)
    return img

SETS = {
    'plaster':   ('plaster_diff.jpg', 'plaster_rough.jpg', 'plaster_ao.jpg'),
    'paving':    ('paving_diff.jpg', 'paving_rough.jpg', 'paving_ao.jpg'),
}
IMGS = {s: tuple(load_img(f) for f in files) for s, files in SETS.items()}

def principled(nt):
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    bs = nt.nodes.new('ShaderNodeBsdfPrincipled')
    nt.links.new(bs.outputs['BSDF'], out.inputs['Surface'])
    return bs

def build_pbr(mat, setname, tint_hex, scale, metallic=0.0, bump=0.3,
              rough_mul=1.0, tint_boost=1.18):
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
    tint = tuple(min(1.0, c * tint_boost) for c in hex_lin(tint_hex))
    mix = nt.nodes.new('ShaderNodeMixRGB'); mix.blend_type = 'MULTIPLY'
    mix.inputs[0].default_value = 1.0
    mix.inputs[2].default_value = (*tint, 1.0)
    nt.links.new(d.outputs['Color'], mix.inputs[1])
    a = tex(ao_i, False)
    mix2 = nt.nodes.new('ShaderNodeMixRGB'); mix2.blend_type = 'MULTIPLY'
    mix2.inputs[0].default_value = 1.0
    nt.links.new(mix.outputs['Color'], mix2.inputs[1])
    nt.links.new(a.outputs['Color'], mix2.inputs[2])
    nt.links.new(mix2.outputs['Color'], bs.inputs['Base Color'])
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
    return bs

def noise_ramp(nt, scale, stops):
    tc = nt.nodes.new('ShaderNodeTexCoord')
    noise = nt.nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = scale
    noise.inputs['Detail'].default_value = 3.0
    nt.links.new(tc.outputs['Object'], noise.inputs['Vector'])
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    els = ramp.color_ramp.elements
    els[0].position = stops[0][0]
    els[0].color = stops[0][1]
    els[1].position = stops[-1][0]
    els[1].color = stops[-1][1]
    for pos, col in stops[1:-1]:
        el = els.new(pos)
        el.color = col
    nt.links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
    return ramp

# ---- 1. LÁ: dựng lại sạch ----
LEAF = {'P0_La_A': ('#3E6B34', '#2F5527'), 'P0_La_B': ('#4C7A3E', '#3A6230'),
        'P0_La_C': ('#5C8446', '#4A6E38')}
for name, (hi, lo) in LEAF.items():
    m = bpy.data.materials.get(name)
    if not m:
        log("MISS", name); continue
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    bs = principled(nt)
    ramp = noise_ramp(nt, 5.0, [(0.0, (*hex_lin(lo), 1)), (1.0, (*hex_lin(hi), 1))])
    nt.links.new(ramp.outputs['Color'], bs.inputs['Base Color'])
    bs.inputs['Roughness'].default_value = 0.9
    log("LEAF rebuilt:", name)

# ---- 2. NỀN KHUÔN VIÊN ----
m = bpy.data.materials.get('Cây nền')
if m:
    bs = build_pbr(m, 'paving', '#7A6A52', 0.12, bump=0.15, tint_boost=1.6)
    nt = m.node_tree
    ramp = noise_ramp(nt, 0.05, [(0.0, (0.0, 0.0, 0.0, 1)), (0.5, (0.0, 0.0, 0.0, 1)),
                                 (0.72, (0.55, 0.55, 0.55, 1)), (1.0, (0.55, 0.55, 0.55, 1))])
    old = bs.inputs['Base Color'].links[0]
    src_sock = old.from_socket
    nt.links.remove(old)
    mx = nt.nodes.new('ShaderNodeMixRGB'); mx.blend_type = 'MIX'
    nt.links.new(ramp.outputs['Color'], mx.inputs[0])
    nt.links.new(src_sock, mx.inputs[1])
    mx.inputs[2].default_value = (*hex_lin('#55703F'), 1.0)
    nt.links.new(mx.outputs['Color'], bs.inputs['Base Color'])
    log("GROUNDS 'Cay nen' -> paving earth + green patches")

# ---- 3. VÀNG SÂU HƠN ----
for n in ['Ngà sáng', 'Vữa màu vàng kem', 'Vàng tường']:
    mm = bpy.data.materials.get(n)
    if mm:
        build_pbr(mm, 'plaster', '#C08A28', 0.40, tint_boost=1.15)
        log("GOLD deepened:", n)
mm = bpy.data.materials.get('Chỉ trắng ngà')
if mm:
    build_pbr(mm, 'plaster', '#DFAF4E', 0.40, tint_boost=1.15)
    log("GOLD deepened: Chỉ trắng ngà")

# ---- 4. GẠCH LÁT SÁNG HƠN ----
for n in ['Đá sân', 'Nền xám sáng']:
    mm = bpy.data.materials.get(n)
    if mm:
        build_pbr(mm, 'paving', '#8A7A63', 0.30, tint_boost=1.9)
        log("PAVING brightened:", n)
mm = bpy.data.materials.get('Dat_Co')
if mm:
    bs = build_pbr(mm, 'paving', '#8A7A63', 0.10, bump=0.15, tint_boost=1.9)
    nt = mm.node_tree
    ramp = noise_ramp(nt, 0.045, [(0.0, (0.72, 0.72, 0.72, 1)), (0.35, (0.72, 0.72, 0.72, 1)),
                                  (0.75, (1.06, 1.06, 1.06, 1)), (1.0, (1.06, 1.06, 1.06, 1))])
    old = bs.inputs['Base Color'].links[0]
    src_sock = old.from_socket
    nt.links.remove(old)
    mx = nt.nodes.new('ShaderNodeMixRGB'); mx.blend_type = 'MULTIPLY'
    mx.inputs[0].default_value = 1.0
    nt.links.new(src_sock, mx.inputs[1])
    nt.links.new(ramp.outputs['Color'], mx.inputs[2])
    nt.links.new(mx.outputs['Color'], bs.inputs['Base Color'])
    log("GROUND Dat_Co brightened + noise patches")

# ---- 5. TRỜI ----
sc = bpy.context.scene
if sc.world and sc.world.use_nodes:
    bg = sc.world.node_tree.nodes.get('Background')
    if bg:
        bg.inputs['Strength'].default_value = 0.8
        log("WORLD strength -> 0.8")

bpy.ops.wm.save_as_mainfile(filepath=W + "layout_v5_p0.blend")
log("PATCH SAVED")
