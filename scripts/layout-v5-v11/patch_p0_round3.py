# -*- coding: utf-8 -*-
"""P0 patch round 3 — art direction theo THEME_CHUA_ONLINE.md (Chung Hy chốt
04:42 07/11): ban ngày SÁNG, bão hòa ấm, trời xanh mây trắng.
- World: đổi HDRI sang kloppenheim_02 (ngày sáng có mây), strength 0.9
- Sun: 3.0, ấm nhẹ, cao hơn; exposure 1.0
- Nền khuôn viên: mảng xanh dịu lại (max 0.35, hạt nhỏ hơn) — bản vá 2 mảng quá đậm
- Cánh giấy hồng sen: #EE7FAE (hồng theme)
Chạy TRÊN layout_v5_p0.blend (sau patch_p0.py), lưu tại chỗ."""
import bpy, os, math, mathutils

TEX = os.path.expanduser("~/workspace/chua-online-work/textures")
BLEND = os.path.expanduser("~/workspace/chua-online-work/layout_v5_p0.blend")
LOGS = []

def log(m):
    LOGS.append(m); print(m)

def hx(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16)/255.0 for i in (0, 2, 4))

def build_pbr(name, diff, rough, tint, scale, boost=1.0, bump=0.35, ao=None):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); out.location = (600, 0)
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled'); bsdf.location = (300, 0)
    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    texco = nt.nodes.new('ShaderNodeTexCoord'); texco.location = (-900, 0)
    co = texco.outputs['Object']
    def img_node(path, noncolor=False):
        n = nt.nodes.new('ShaderNodeTexImage')
        im = bpy.data.images.load(path, check_existing=True)
        n.image = im
        if noncolor: im.colorspace_settings.name = 'Non-Color'
        n.projection = 'BOX'; n.projection_blend = 0.5
        nt.links.new(co, n.inputs['Vector'])
        return n
    td = img_node(os.path.join(TEX, diff)); td.location = (-600, 200)
    mult = nt.nodes.new('ShaderNodeMixRGB'); mult.blend_type = 'MULTIPLY'
    mult.location = (-300, 200); mult.inputs[0].default_value = 1.0
    mult.inputs[2].default_value = (*[c*boost for c in hx(tint)], 1.0)
    nt.links.new(td.outputs['Color'], mult.inputs[1])
    final = mult
    if ao:
        ta = img_node(os.path.join(TEX, ao), True); ta.location = (-600, -40)
        m2 = nt.nodes.new('ShaderNodeMixRGB'); m2.blend_type = 'MULTIPLY'
        m2.location = (-80, 200); m2.inputs[0].default_value = 1.0
        nt.links.new(final.outputs['Color'], m2.inputs[1])
        nt.links.new(ta.outputs['Color'], m2.inputs[2])
        final = m2
    nt.links.new(final.outputs['Color'], bsdf.inputs['Base Color'])
    if rough:
        trm = img_node(os.path.join(TEX, rough), True); trm.location = (-600, -300)
        nt.links.new(trm.outputs['Color'], bsdf.inputs['Roughness'])
    else:
        bsdf.inputs['Roughness'].default_value = 0.9
    bnode = nt.nodes.new('ShaderNodeBump'); bnode.location = (0, -300)
    bnode.inputs['Strength'].default_value = bump
    nt.links.new(td.outputs['Color'], bnode.inputs['Height'])
    nt.links.new(bnode.outputs['Normal'], bsdf.inputs['Normal'])
    mp = nt.nodes.new('ShaderNodeMapping'); mp.location = (-1100, 0)
    mp.inputs['Scale'].default_value = (scale, scale, scale)
    nt.links.new(mp.outputs['Vector'], texco.inputs['Vector']) if False else None
    # nối mapping: TexCoord -> Mapping -> các tex (thay link trực tiếp)
    for n in list(nt.nodes):
        if n.type == 'TEX_IMAGE':
            for l in list(n.inputs['Vector'].links):
                nt.links.remove(l)
            nt.links.new(mp.outputs['Vector'], n.inputs['Vector'])
    nt.links.new(texco.outputs['Object'], mp.inputs['Vector'])
    return mat

def build_flat(name, hexcol, rough=0.85, metallic=0.0):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); out.location = (300, 0)
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled'); bsdf.location = (0, 0)
    bsdf.inputs['Base Color'].default_value = (*hx(hexcol), 1.0)
    bsdf.inputs['Roughness'].default_value = rough
    bsdf.inputs['Metallic'].default_value = metallic
    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return mat

sc = bpy.context.scene

# --- 1) World: HDRI ngày sáng ---
w = sc.world; w.use_nodes = True
wnt = w.node_tree; wnt.nodes.clear()
bg = wnt.nodes.new('ShaderNodeBackground')
out = wnt.nodes.new('ShaderNodeOutputWorld')
tex = wnt.nodes.new('ShaderNodeTexEnvironment')
img = bpy.data.images.load(os.path.join(TEX, "sky_bright_day_2k.hdr"), check_existing=True)
tex.image = img
mp = wnt.nodes.new('ShaderNodeMapping'); tc = wnt.nodes.new('ShaderNodeTexCoord')
mp.inputs['Rotation'].default_value = (0, 0, 0.6)
wnt.links.new(tc.outputs['Generated'], mp.inputs['Vector'])
wnt.links.new(mp.outputs['Vector'], tex.inputs['Vector'])
wnt.links.new(tex.outputs['Color'], bg.inputs['Color'])
bg.inputs['Strength'].default_value = 0.9
wnt.links.new(bg.outputs['Background'], out.inputs['Surface'])
log("world: bright day HDRI strength 0.9")

# --- 2) Sun + exposure ---
sun = bpy.data.objects.get('Sun_Layout')
if sun and sun.type == 'LIGHT':
    sun.data.energy = 3.0
    sun.data.color = (1.0, 0.88, 0.72)
    sun.rotation_euler = (0.88, 0.15, -0.55)
sc.view_settings.exposure = 1.0
log("sun 3.0 warm-high, exposure 1.0")

# --- 3) Nền khuôn viên: mảng xanh dịu ---
mat = bpy.data.materials.get('Cây nền')
if mat:
    nt = mat.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); out.location = (900, 0)
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled'); bsdf.location = (600, 0)
    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    texco = nt.nodes.new('ShaderNodeTexCoord'); texco.location = (-1100, 0)
    mpn = nt.nodes.new('ShaderNodeMapping'); mpn.location = (-900, 0)
    mpn.inputs['Scale'].default_value = (0.09, 0.09, 0.09)
    nt.links.new(texco.outputs['Object'], mpn.inputs['Vector'])
    noise = nt.nodes.new('ShaderNodeTexNoise'); noise.location = (-700, -260)
    noise.inputs['Scale'].default_value = 2.2
    noise.inputs['Detail'].default_value = 5.0
    nt.links.new(mpn.outputs['Vector'], noise.inputs['Vector'])
    ramp = nt.nodes.new('ShaderNodeValToRGB'); ramp.location = (-450, -260)
    ramp.color_ramp.elements[0].position = 0.45
    ramp.color_ramp.elements[0].color = (0, 0, 0, 1)
    ramp.color_ramp.elements[1].position = 0.85
    ramp.color_ramp.elements[1].color = (0.35, 0.35, 0.35, 1)
    nt.links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
    td = nt.nodes.new('ShaderNodeTexImage'); td.location = (-700, 200)
    td.image = bpy.data.images.load(os.path.join(TEX, "paving_diff.jpg"), check_existing=True)
    td.projection = 'BOX'; td.projection_blend = 0.5
    nt.links.new(mpn.outputs['Vector'], td.inputs['Vector'])
    ta = nt.nodes.new('ShaderNodeTexImage'); ta.location = (-700, -40)
    ta.image = bpy.data.images.load(os.path.join(TEX, "paving_ao.jpg"), check_existing=True)
    ta.image.colorspace_settings.name = 'Non-Color'
    ta.projection = 'BOX'; ta.projection_blend = 0.5
    nt.links.new(mpn.outputs['Vector'], ta.inputs['Vector'])
    mult = nt.nodes.new('ShaderNodeMixRGB'); mult.blend_type = 'MULTIPLY'
    mult.location = (-400, 200); mult.inputs[0].default_value = 1.0
    mult.inputs[2].default_value = (*[c*1.6 for c in hx('#7A6A52')], 1.0)
    nt.links.new(td.outputs['Color'], mult.inputs[1])
    m2 = nt.nodes.new('ShaderNodeMixRGB'); m2.blend_type = 'MULTIPLY'
    m2.location = (-150, 200); m2.inputs[0].default_value = 1.0
    nt.links.new(mult.outputs['Color'], m2.inputs[1])
    nt.links.new(ta.outputs['Color'], m2.inputs[2])
    mixg = nt.nodes.new('ShaderNodeMixRGB'); mixg.blend_type = 'MIX'
    mixg.location = (250, 100)
    mixg.inputs[2].default_value = (*hx('#5B7346'), 1.0)
    nt.links.new(ramp.outputs['Color'], mixg.inputs[0])
    nt.links.new(m2.outputs['Color'], mixg.inputs[1])
    nt.links.new(mixg.outputs['Color'], bsdf.inputs['Base Color'])
    trm = nt.nodes.new('ShaderNodeTexImage'); trm.location = (-450, -520)
    trm.image = bpy.data.images.load(os.path.join(TEX, "paving_rough.jpg"), check_existing=True)
    trm.image.colorspace_settings.name = 'Non-Color'
    trm.projection = 'BOX'; trm.projection_blend = 0.5
    nt.links.new(mpn.outputs['Vector'], trm.inputs['Vector'])
    nt.links.new(trm.outputs['Color'], bsdf.inputs['Roughness'])
    bnode = nt.nodes.new('ShaderNodeBump'); bnode.location = (350, -300)
    bnode.inputs['Strength'].default_value = 0.3
    nt.links.new(td.outputs['Color'], bnode.inputs['Height'])
    nt.links.new(bnode.outputs['Normal'], bsdf.inputs['Normal'])
    log("Cây nền: mảng xanh dịu (max 0.35, hạt 0.09)")

# --- 4) Hồng theme cho cánh giấy ---
for nm in ('CanhGiayHongSen', 'CanhGiayHongSen.001'):
    if bpy.data.materials.get(nm):
        build_flat(nm, '#EE7FAE', 0.7)
        log(f"{nm} -> #EE7FAE")

# --- pack + save ---
for im in bpy.data.images:
    try:
        if im.source == 'FILE':
            im.pack()
    except Exception:
        pass
bpy.ops.wm.save_as_mainfile(filepath=BLEND)
log(f"SAVED {BLEND} size={os.path.getsize(BLEND)}")
print("PATCH3 DONE")
