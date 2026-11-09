# -*- coding: utf-8 -*-
"""PATCH P1 vòng 3 — tinh chỉnh theo số đo vòng 1:
 [2] tường: multiplier (0.98,0.63,0.10) -> (1.13,0.68,0.065)
     (đo: cần render R x1.15, G x1.09, B x0.68; AO compositor đã kéo tối ~15%)
 [5] nền: tint các vật liệu đất/sân nhân thêm (1.06,0.97,0.80) để cắt kênh B
     (đo B đang +18 so với đích; R/G đã trong ±12)
Chạy trên layout_v6_p1.blend, lưu cùng file."""
import bpy, os

W = "/home/hatch/workspace/chua-online-work/"
TEX = W + "textures/"

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

WALL3 = (1.13, 0.68, 0.065)
for nm in ('Ngà sáng', 'Vữa màu vàng kem', 'Vàng tường'):
    m = bpy.data.materials.get(nm)
    if m:
        build_pbr_mult(m, "plaster_diff.jpg", "plaster_rough.jpg", "plaster_ao.jpg",
                       WALL3, 0.30, bump=0.25)
        print("WALL3", nm, WALL3)

ADJ = (1.06, 0.97, 0.80)
base = hx('#9A8A72')
datco = tuple(base[i] * 2.8 * ADJ[i] for i in range(3))
m = bpy.data.materials.get('Dat_Co')
if m:
    bs = build_pbr_mult(m, "paving_diff.jpg", "paving_rough.jpg", "paving_ao.jpg",
                        datco, 0.10, bump=0.30)
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
    print("Dat_Co mult ->", tuple(round(x, 2) for x in datco))

pav = tuple(base[i] * 2.9 * ADJ[i] for i in range(3))
for nm in ('Đá sân', 'Nền xám sáng'):
    mm = bpy.data.materials.get(nm)
    if mm:
        build_pbr_mult(mm, "paving_diff.jpg", "paving_rough.jpg", "paving_ao.jpg",
                       pav, 0.30, bump=0.30)
        print("paving mult ->", tuple(round(x, 2) for x in pav), nm)

m = bpy.data.materials.get('Cây nền')
if m:
    for n in m.node_tree.nodes:
        if n.type == 'MIX_RGB' and n.blend_type == 'MULTIPLY':
            v = n.inputs[2].default_value
            if not n.inputs[2].links and v[0] > 1.0:
                n.inputs[2].default_value = (v[0] * ADJ[0], v[1] * ADJ[1], v[2] * ADJ[2], 1)
                print("Cây nền tint ->", tuple(round(x, 2) for x in n.inputs[2].default_value[:3]))

bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
print("SAVED round3")
