"""
P3 "BÓNG BẨY" — weathering + sửa bệ Phật nằm + grade 2 tông (compositor).
Chạy: blender5 -b layout_v7_p2.blend --python build_p3.py
Lưu: layout_v8_p3.blend (grade mặc định = tông (a) "sáng trong").
KHÔNG render trong script này.
"""
import bpy, os

W = "/home/hatch/workspace/chua-online-work/"
OUT = W + "layout_v8_p3.blend"
TEX = W + "textures/"

# ---------------------------------------------------------------- plinth fix
ds = bpy.data.materials.get('DarkStone.002')
assert ds is not None, "DarkStone.002 missing"
for obj_name in ('Bệ khu tượng nằm', 'Viền bệ tượng nằm'):
    o = bpy.data.objects.get(obj_name)
    assert o is not None, f"missing object {obj_name}"
    for ms in o.material_slots:
        ms.material = ds
    print("PLINTH FIX:", obj_name, "-> DarkStone.002", flush=True)

# ---------------------------------------------------------------- weathering
def weather(mat, band_from, band_to, tint, rough_add, noise_scale, tag):
    """Thêm lớp phong hoá theo Z thế giới: nhân albedo + tăng roughness ở vùng thấp.
    band: factor=1 ở Z<=band_from, 0 ở Z>=band_to."""
    if mat is None or not mat.use_nodes:
        print("  SKIP (no nodes):", tag, flush=True); return False
    nt = mat.node_tree
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

    geo = nt.nodes.new('ShaderNodeNewGeometry'); geo.name = 'P3W_Geo'; geo.label = 'P3 weathering'
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
    nm.inputs['From Min'].default_value = 0.32
    nm.inputs['From Max'].default_value = 0.75
    nm.inputs['To Min'].default_value = 0.0
    nm.inputs['To Max'].default_value = 1.0
    nm.clamp = True
    nt.links.new(nz.outputs['Fac'], nm.inputs['Value'])
    m1 = nt.nodes.new('ShaderNodeMath'); m1.name = 'P3W_Nx'
    m1.operation = 'MULTIPLY'; m1.inputs[1].default_value = 0.70
    nt.links.new(nm.outputs['Result'], m1.inputs[0])
    a1 = nt.nodes.new('ShaderNodeMath'); a1.name = 'P3W_Na'
    a1.operation = 'ADD'; a1.inputs[1].default_value = 0.30
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
    print("  WEATHERED:", mat.name, tag, flush=True)
    return True

WALL_MATS = ['Vàng tường', 'Chỉ trắng ngà', 'Chỉ màu kem', 'Gờ vàng', 'Gờ đỏ',
             'ChuoiVang', 'Vàng trang trí', 'Hoa văn vàng', 'Vàng kem',
             'Vữa màu vàng kem', 'LuaVangTamLinh', 'Kim loại vàng cổ',
             'P1_GomTru', 'Gốm xanh']
print("--- weathering TUONG/CHAN (band 0->1.7m):", flush=True)
for name in WALL_MATS:
    m = bpy.data.materials.get(name)
    if m:
        weather(m, 0.0, 1.7, (0.36, 0.37, 0.29), 0.30, (2.2, 2.2, 0.35), 'wall')
    else:
        print("  ABSENT:", name, flush=True)
print("--- weathering MAI (band 6.2->8.6m, reu):", flush=True)
for name in ('Mai_Ngoi_Hang', 'Mai_Ngoi_Hang_Sang'):
    m = bpy.data.materials.get(name)
    if m:
        weather(m, 6.2, 8.6, (0.30, 0.42, 0.22), 0.20, (1.6, 1.6, 1.6), 'roof')
print("--- weathering ME HO (band -0.1->0.55m, reu):", flush=True)
m = bpy.data.materials.get('Vôi vàng')
if m:
    weather(m, -0.1, 0.55, (0.32, 0.42, 0.25), 0.25, (2.0, 2.0, 0.8), 'pond')

# ---------------------------------------------------------------- compositor grade
sc = bpy.context.scene
vl = bpy.context.view_layer
vl.use_pass_mist = True
vl.use_pass_ambient_occlusion = True
g = sc.compositing_node_group
assert g is not None, "no compositing group"
names = [n.name for n in g.nodes]
gout = next(n for n in g.nodes if n.bl_idname == 'NodeGroupOutput')
src = None
for lk in list(g.links):
    if lk.to_node == gout and lk.to_socket.name == 'Image':
        src = (lk.from_node, lk.from_socket)
        g.links.remove(lk)
assert src, "group output Image not linked"
rl = next(n for n in g.nodes if n.bl_idname == 'CompositorNodeRLayers')

def mixnode(name, blend):
    n = g.nodes.new('ShaderNodeMix'); n.name = name
    n.data_type = 'RGBA'; n.blend_type = blend
    n.factor_mode = 'UNIFORM'
    return n
def sock(node, *cands):
    for c in cands:
        if c in node.inputs: return node.inputs[c]
        if c in node.outputs: return node.outputs[c]
    raise KeyError((node.name, cands, [s.name for s in node.inputs], [s.name for s in node.outputs]))

if 'P3_FogMix' not in names:
    # LUU Y: Blender 5 compositor khong nhan node HueSaturation -> bo qua buoc
    # saturation; tong am cua (b) den tu nang + fog am + vignette am.
    fogfac = g.nodes.new('ShaderNodeMath'); fogfac.name = 'P3_FogFac'
    fogfac.operation = 'MULTIPLY'; fogfac.use_clamp = True
    fogfac.inputs[1].default_value = 0.50          # tong (a): fog strength 0.50
    fogrgb = g.nodes.new('CompositorNodeRGB'); fogrgb.name = 'P3_FogRGB'
    fogrgb.outputs[0].default_value = (0.82, 0.88, 0.96, 1.0)
    fog = mixnode('P3_FogMix', 'MIX')
    vigimg = g.nodes.new('CompositorNodeImage'); vigimg.name = 'P3_VigImg'
    vigimg.image = bpy.data.images.load(TEX + 'p3_vignette_a.png')
    vig = mixnode('P3_VigMix', 'MULTIPLY')
    g.links.new(src[0].outputs[src[1].name], sock(fog, 'A'))
    g.links.new(fogrgb.outputs[0], sock(fog, 'B'))
    g.links.new(rl.outputs['Mist'], fogfac.inputs[0])
    g.links.new(fogfac.outputs[0], sock(fog, 'Factor'))
    g.links.new(sock(fog, 'Result'), sock(vig, 'A'))
    g.links.new(vigimg.outputs['Image'], sock(vig, 'B'))
    sock(vig, 'Factor').default_value = 1.0
    g.links.new(sock(vig, 'Result'), gout.inputs['Image'])
    print("COMP: P3 grade chain added (Fog -> Vignette)", flush=True)
else:
    print("COMP: P3 chain already present", flush=True)

# grade (a) is the saved default: AgX exposure 1.0, sun untouched (V7)
sc.view_settings.view_transform = 'AgX'
sc.view_settings.exposure = 1.0
sc.render.engine = 'CYCLES'
sc.cycles.samples = 32
sc.cycles.use_denoising = True
sc.render.resolution_x = 1280
sc.render.resolution_y = 720

bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("SAVED", OUT, os.path.getsize(OUT), flush=True)
print("BUILD P3 DONE", flush=True)
