# -*- coding: utf-8 -*-
"""P0 patch round 4 — hiệu chỉnh theo số đo flycam vòng 3:
- Nền đất/sân đo được (96,89,73) vs đích lát (138,122,99): QUÁ TỐI
  -> nâng boost + làm sáng tint họ lát; mảng xanh dịu & mịn hơn nữa
- Tán lá hơi chói lime so với nền -> ramp lá tối/sâu hơn ~15%
- Vàng mặt tiền: sâu thêm một nấc (#B57E22) chờ đo ở góc ground
Chạy trên layout_v5_p0.blend (sau round 3), lưu tại chỗ."""
import bpy, os

TEX = os.path.expanduser("~/workspace/chua-online-work/textures")
BLEND = os.path.expanduser("~/workspace/chua-online-work/layout_v5_p0.blend")
LOGS = []

def log(m):
    LOGS.append(m); print(m)

def hx(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16)/255.0 for i in (0, 2, 4))

def build_pbr(mat, diff, rough, tint, scale, boost=1.0, bump=0.35, ao=None):
    mat.use_nodes = True
    nt = mat.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); out.location = (600, 0)
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled'); bsdf.location = (300, 0)
    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    texco = nt.nodes.new('ShaderNodeTexCoord'); texco.location = (-1100, 0)
    mp = nt.nodes.new('ShaderNodeMapping'); mp.location = (-900, 0)
    mp.inputs['Scale'].default_value = (scale, scale, scale)
    nt.links.new(texco.outputs['Object'], mp.inputs['Vector'])
    def img_node(fname, noncolor=False, y=0):
        n = nt.nodes.new('ShaderNodeTexImage'); n.location = (-650, y)
        im = bpy.data.images.load(os.path.join(TEX, fname), check_existing=True)
        n.image = im
        if noncolor: im.colorspace_settings.name = 'Non-Color'
        n.projection = 'BOX'; n.projection_blend = 0.5
        nt.links.new(mp.outputs['Vector'], n.inputs['Vector'])
        return n
    td = img_node(diff, y=200)
    mult = nt.nodes.new('ShaderNodeMixRGB'); mult.blend_type = 'MULTIPLY'
    mult.location = (-350, 200); mult.inputs[0].default_value = 1.0
    mult.inputs[2].default_value = (*[c*boost for c in hx(tint)], 1.0)
    nt.links.new(td.outputs['Color'], mult.inputs[1])
    final = mult
    if ao:
        ta = img_node(ao, True, y=-40)
        m2 = nt.nodes.new('ShaderNodeMixRGB'); m2.blend_type = 'MULTIPLY'
        m2.location = (-100, 200); m2.inputs[0].default_value = 1.0
        nt.links.new(final.outputs['Color'], m2.inputs[1])
        nt.links.new(ta.outputs['Color'], m2.inputs[2])
        final = m2
    nt.links.new(final.outputs['Color'], bsdf.inputs['Base Color'])
    if rough:
        trm = img_node(rough, True, y=-300)
        nt.links.new(trm.outputs['Color'], bsdf.inputs['Roughness'])
    else:
        bsdf.inputs['Roughness'].default_value = 0.9
    bnode = nt.nodes.new('ShaderNodeBump'); bnode.location = (50, -300)
    bnode.inputs['Strength'].default_value = bump
    nt.links.new(td.outputs['Color'], bnode.inputs['Height'])
    nt.links.new(bnode.outputs['Normal'], bsdf.inputs['Normal'])
    return mat

def get(name):
    return bpy.data.materials.get(name)

# --- 1) Họ lát sáng lên ---
for nm, tint, boost, scale in (
    ('Đá sân',       '#9A8A72', 2.6, 0.30),
    ('Nền xám sáng', '#9A8A72', 2.6, 0.30),
    ('Dat_Co',       '#9A8A72', 2.4, 0.10),
):
    m = get(nm)
    if m:
        build_pbr(m, "paving_diff.jpg", "paving_rough.jpg", tint, scale,
                  boost=boost, bump=0.30, ao="paving_ao.jpg")
        log(f"{nm}: tint {tint} boost {boost}")
    else:
        log(f"MISS {nm}")
# Dat_Co: thêm mảng noise như cũ nhưng dịu
m = get('Dat_Co')
if m:
    nt = m.node_tree
    texco = [n for n in nt.nodes if n.type == 'TEX_COORD'][0]
    noise = nt.nodes.new('ShaderNodeTexNoise'); noise.location = (-1100, -350)
    noise.inputs['Scale'].default_value = 0.05
    noise.inputs['Detail'].default_value = 6.0
    nt.links.new(texco.outputs['Generated'], noise.inputs['Vector'])
    ramp = nt.nodes.new('ShaderNodeValToRGB'); ramp.location = (-850, -350)
    ramp.color_ramp.elements[0].position = 0.35
    ramp.color_ramp.elements[0].color = (1, 1, 1, 1)
    ramp.color_ramp.elements[1].position = 0.75
    ramp.color_ramp.elements[1].color = (0.78, 0.78, 0.78, 1)
    nt.links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
    mults = [n for n in nt.nodes if n.type == 'MIX_RGB']
    if mults:
        target = mults[0]
        m3 = nt.nodes.new('ShaderNodeMixRGB'); m3.blend_type = 'MULTIPLY'
        m3.location = (150, 260); m3.inputs[0].default_value = 1.0
        old = list(target.outputs['Color'].links)
        nt.links.new(target.outputs['Color'], m3.inputs[1])
        nt.links.new(ramp.outputs['Color'], m3.inputs[2])
        bsdf = [n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'][0]
        for l in old:
            nt.links.new(m3.outputs['Color'], l.to_socket)
    log("Dat_Co: mảng noise dịu (0.78)")

# --- 2) Cây nền: base sáng + mảng mịn/dịu ---
m = get('Cây nền')
if m:
    nt = m.node_tree
    for n in nt.nodes:
        if n.type == 'MIX_RGB' and n.blend_type == 'MULTIPLY':
            # mult đầu (tint paving): inputs[2] là màu tint*boost
            if abs(n.inputs[2].default_value[0] - 0.478*1.6) < 0.3:
                n.inputs[2].default_value = (*[c*2.2 for c in hx('#8A7A63')], 1.0)
        if n.type == 'MIX_RGB' and n.blend_type == 'MIX':
            n.inputs[2].default_value = (*hx('#66804E'), 1.0)
        if n.type == 'VALTORGB':
            n.color_ramp.elements[1].color = (0.22, 0.22, 0.22, 1)
        if n.type == 'TEX_NOISE':
            n.inputs['Scale'].default_value = 3.4
    for n in nt.nodes:
        if n.type == 'MAPPING':
            n.inputs['Scale'].default_value = (0.16, 0.16, 0.16)
    log("Cây nền: base boost 2.2, mảng max 0.22 xanh #66804E, hạt 0.16")

# --- 3) Lá: ramp sâu hơn ---
LEAF = {
    'P0_La_A': ((0.09, 0.19, 0.06), (0.28, 0.45, 0.18)),
    'P0_La_B': ((0.11, 0.22, 0.07), (0.31, 0.49, 0.20)),
    'P0_La_C': ((0.14, 0.26, 0.09), (0.35, 0.53, 0.24)),
}
for nm, (c0, c1) in LEAF.items():
    m = get(nm)
    if not m:
        log(f"MISS {nm}"); continue
    for n in m.node_tree.nodes:
        if n.type == 'VALTORGB':
            n.color_ramp.elements[0].color = (*c0, 1)
            n.color_ramp.elements[1].color = (*c1, 1)
    log(f"{nm}: ramp sâu hơn")

# --- 4) Vàng chính sâu thêm 1 nấc ---
for nm in ('Ngà sáng', 'Vữa màu vàng kem', 'Vàng tường'):
    m = get(nm)
    if not m:
        log(f"MISS {nm}"); continue
    build_pbr(m, "plaster_diff.jpg", "plaster_rough.jpg", '#B57E22', 0.30,
              boost=1.15, bump=0.25, ao="plaster_ao.jpg")
    log(f"{nm}: tint #B57E22")

for im in bpy.data.images:
    try:
        if im.source == 'FILE':
            im.pack()
    except Exception:
        pass
bpy.ops.wm.save_as_mainfile(filepath=BLEND)
log(f"SAVED {BLEND} size={os.path.getsize(BLEND)}")
print("PATCH4 DONE")
