# V10 FIX3 — hốc cổng dễ đọc hơn: đèn fill ấm trong hốc (2 cổng), tượng nới
# ngang x1.35 quanh tâm cổng, inset tối hơn (vật liệu riêng).
import bpy
from mathutils import Matrix, Vector

bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/chua-online-work/layout_v12_v10.blend")
sc = bpy.context.scene

dark = bpy.data.materials.new('V10_NicheDark'); dark.use_nodes = True
for n in dark.node_tree.nodes:
    if n.type == 'BSDF_PRINCIPLED':
        n.inputs['Base Color'].default_value = (0.030, 0.024, 0.018, 1)
        n.inputs['Roughness'].default_value = 1.0
for nm in ('V10_NicheInset_PT', 'V10_NicheInset_TD'):
    o = bpy.data.objects.get(nm)
    if o:
        o.data.materials.clear(); o.data.materials.append(dark)
        print("inset darkened", nm)

for gx, tag in ((23.0, 'PT'), (45.0, 'TD')):
    # nới ngang tượng quanh x=gx
    Mx = Matrix.Translation((gx, 0, 0)) @ Matrix.Scale(1.35, 4, (1, 0, 0)) @ Matrix.Translation((-gx, 0, 0))
    cnt = 0
    for o in bpy.data.objects:
        if o.name.startswith(f'V10_GateBuddha_{tag}_'):
            o.matrix_world = Mx @ o.matrix_world
            cnt += 1
    print("widened", tag, cnt)
    # đèn fill trong hốc
    ld = bpy.data.lights.new(f'V10_NicheFill_{tag}', 'POINT')
    ld.energy = 55; ld.color = (1.0, 0.85, 0.62); ld.shadow_soft_size = 0.4
    lo = bpy.data.objects.new(f'V10_NicheFill_{tag}', ld)
    sc.collection.objects.link(lo)
    lo.location = (gx, -41.6, 8.8)
    print("fill added", tag)

bpy.ops.wm.save_as_mainfile(filepath="/home/hatch/workspace/chua-online-work/layout_v12_v10.blend")
print("FIX3 SAVED")
