"""
PATCH P3 — bo sung weathering cho cac vat lieu chan tuong bi sot o build dau
('Nga sang', 'Trang', 'Do gach', 'Men gom xanh' = cot/trang tri mat tien that)
+ tang nhe cuong do cac chuoi P3W nhom tuong. Mo layout_v8_p3.blend, luu tai cho.
"""
import bpy

def weather(mat, band_from, band_to, tint, rough_add, noise_scale, tag):
    if mat is None or not mat.use_nodes:
        print("  SKIP:", tag, flush=True); return False
    nt = mat.node_tree
    if any(n.name == 'P3W_Geo' for n in nt.nodes):
        print("  ALREADY:", mat.name, flush=True); return False
    bs = [n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED']
    out = [n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL']
    if len(bs) != 1 or len(out) != 1:
        print("  SKIP (structure):", mat.name, flush=True); return False
    bs = bs[0]
    bc_in = bs.inputs['Base Color']
    old_link = bc_in.links[0] if bc_in.links else None
    old_default = tuple(bc_in.default_value)
    rg_in = bs.inputs['Roughness']
    old_rlink = rg_in.links[0] if rg_in.links else None
    old_rdefault = rg_in.default_value
    geo = nt.nodes.new('ShaderNodeNewGeometry'); geo.name = 'P3W_Geo'
    sep = nt.nodes.new('ShaderNodeSeparateXYZ'); sep.name = 'P3W_SepZ'
    nt.links.new(geo.outputs['Position'], sep.inputs['Vector'])
    zm = nt.nodes.new('ShaderNodeMapRange'); zm.name = 'P3W_ZMask'
    zm.inputs['From Min'].default_value = band_from
    zm.inputs['From Max'].default_value = band_to
    zm.inputs['To Min'].default_value = 1.0
    zm.inputs['To Max'].default_value = 0.0
    zm.clamp = True
    nt.links.new(sep.outputs['Z'], zm.inputs['Value'])
    mp = nt.nodes.new('ShaderNodeMapping'); mp.name = 'P3W_Map'
    mp.inputs['Scale'].default_value = noise_scale
    nt.links.new(geo.outputs['Position'], mp.inputs['Vector'])
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.name = 'P3W_Noise'
    nz.noise_dimensions = '3D'
    nz.inputs['Scale'].default_value = 1.0
    nz.inputs['Detail'].default_value = 5.0
    nz.inputs['Roughness'].default_value = 0.75
    nt.links.new(mp.outputs['Vector'], nz.inputs['Vector'])
    nm = nt.nodes.new('ShaderNodeMapRange'); nm.name = 'P3W_NoiseMap'
    nm.inputs['From Min'].default_value = 0.25
    nm.inputs['From Max'].default_value = 0.75
    nm.inputs['To Min'].default_value = 0.0
    nm.inputs['To Max'].default_value = 1.0
    nm.clamp = True
    nt.links.new(nz.outputs['Fac'], nm.inputs['Value'])
    m1 = nt.nodes.new('ShaderNodeMath'); m1.name = 'P3W_Nx'
    m1.operation = 'MULTIPLY'; m1.inputs[1].default_value = 0.65
    nt.links.new(nm.outputs['Result'], m1.inputs[0])
    a1 = nt.nodes.new('ShaderNodeMath'); a1.name = 'P3W_Na'
    a1.operation = 'ADD'; a1.inputs[1].default_value = 0.35
    nt.links.new(m1.outputs[0], a1.inputs[0])
    fac = nt.nodes.new('ShaderNodeMath'); fac.name = 'P3W_Factor'
    fac.operation = 'MULTIPLY'; fac.use_clamp = True
    nt.links.new(zm.outputs['Result'], fac.inputs[0])
    nt.links.new(a1.outputs[0], fac.inputs[1])
    wm = nt.nodes.new('ShaderNodeMixRGB'); wm.name = 'P3W_TintMix'
    wm.blend_type = 'MULTIPLY'
    wm.inputs['Fac'].default_value = 1.0
    wm.inputs['Color1'].default_value = (1.0, 1.0, 1.0, 1.0)
    wm.inputs['Color2'].default_value = (*tint, 1.0)
    nt.links.new(fac.outputs[0], wm.inputs['Fac'])
    fm = nt.nodes.new('ShaderNodeMixRGB'); fm.name = 'P3W_FinalMix'
    fm.blend_type = 'MULTIPLY'
    fm.inputs['Fac'].default_value = 1.0
    if old_link:
        nt.links.new(old_link.from_node.outputs[old_link.from_socket.name], fm.inputs['Color1'])
        nt.links.remove(old_link)
    else:
        fm.inputs['Color1'].default_value = old_default
    nt.links.new(wm.outputs['Color'], fm.inputs['Color2'])
    nt.links.new(fm.outputs['Color'], bc_in)
    rm = nt.nodes.new('ShaderNodeMath'); rm.name = 'P3W_RoughMul'
    rm.operation = 'MULTIPLY'; rm.inputs[1].default_value = rough_add
    nt.links.new(fac.outputs[0], rm.inputs[0])
    ra = nt.nodes.new('ShaderNodeMath'); ra.name = 'P3W_RoughAdd'
    ra.operation = 'ADD'; ra.use_clamp = True
    if old_rlink:
        nt.links.new(old_rlink.from_node.outputs[old_rlink.from_socket.name], ra.inputs[0])
        nt.links.remove(old_rlink)
    else:
        ra.inputs[0].default_value = old_rdefault
    nt.links.new(rm.outputs[0], ra.inputs[1])
    nt.links.new(ra.outputs[0], rg_in)
    print("  WEATHERED+:", mat.name, tag, flush=True)
    return True

print("--- patch: them vat lieu chan tuong:", flush=True)
for name in ('Ngà sáng', 'Trắng', 'Đỏ gạch', 'Men gốm xanh'):
    m = bpy.data.materials.get(name)
    if m:
        weather(m, 0.0, 1.7, (0.33, 0.34, 0.27), 0.30, (2.2, 2.2, 0.35), 'wall2')
    else:
        print("  ABSENT:", name, flush=True)

print("--- patch: tang cuong do chuoi P3W nhom tuong da co:", flush=True)
ROOF = ('Mai_Ngoi_Hang', 'Mai_Ngoi_Hang_Sang'); POND = ('Vôi vàng',)
for m in bpy.data.materials:
    if not m.use_nodes or not m.node_tree: continue
    nm = m.node_tree.nodes.get('P3W_NoiseMap')
    na = m.node_tree.nodes.get('P3W_Na')
    tm = m.node_tree.nodes.get('P3W_TintMix')
    nx = m.node_tree.nodes.get('P3W_Nx')
    if not (nm and na and tm): continue
    if m.name in ROOF or m.name in POND: continue
    if m.name in ('Ngà sáng', 'Trắng', 'Đỏ gạch', 'Men gốm xanh'): continue  # vua them, da dung so moi
    nm.inputs['From Min'].default_value = 0.25
    na.inputs[1].default_value = 0.35
    if nx: nx.inputs[1].default_value = 0.65
    tm.inputs['Color2'].default_value = (0.33, 0.34, 0.27, 1.0)
    print("  STRENGTHENED:", m.name, flush=True)

print("--- patch: hieu chinh fog theo mist do that (temple ~0.67):", flush=True)
g = bpy.context.scene.compositing_node_group
fac = g.nodes.get('P3_FogFac')
assert fac is not None
fac.inputs[1].default_value = 0.15   # tong (a): fog tai chua ~0.10, nen ~0.02-0.06
print("  P3_FogFac strength -> 0.15", flush=True)

bpy.ops.wm.save_as_mainfile(filepath="/home/hatch/workspace/chua-online-work/layout_v8_p3.blend")
print("PATCH SAVED", flush=True)
