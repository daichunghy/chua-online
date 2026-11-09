"""V7 PROBE — dump geometry facts needed by build_v7.py (no changes, no save).
Run: blender5 -b layout_v8_p3.blend --factory-startup -noaudio --python layout/probe_v7.py
"""
import bpy, math
from mathutils import Vector

def bbox(o):
    ws = [o.matrix_world @ Vector(v) for v in o.bound_box]
    return (min(v.x for v in ws), max(v.x for v in ws),
            min(v.y for v in ws), max(v.y for v in ws),
            min(v.z for v in ws), max(v.z for v in ws))

def show(tag, objs, limit=40):
    print(f"== {tag}: {len(objs)}")
    for o in objs[:limit]:
        b = bbox(o)
        print(f"  {o.name!r} verts={len(o.data.vertices) if o.type=='MESH' else '-'} "
              f"bbox x[{b[0]:.1f},{b[1]:.1f}] y[{b[2]:.1f},{b[3]:.1f}] z[{b[4]:.1f},{b[5]:.1f}] "
              f"mats={[m.name if m else None for m in o.data.materials] if o.type=='MESH' else []}")

# 1. Roof objects (hall + tower + gates) — need eave lines for moss decals
roof = [o for o in bpy.data.objects if o.type == 'MESH' and any(
    m and 'Mai_Ngoi' in m.name for m in o.data.materials)]
show("ROOF Mai_Ngoi objects", roof, 30)

# 2. Gate pillar objects (for water streaks at base)
gate = [o for o in bpy.data.objects if o.type == 'MESH' and 'Cong' in o.name or
        (o.type == 'MESH' and o.name.startswith(('TamQuan', 'Tam_Quan', 'Gate')))]
show("GATE objects", gate, 30)
# fallback: objects near gate pillars x 18/28/40/50, y -41..-38, z<8
near_gate = []
for o in bpy.data.objects:
    if o.type != 'MESH':
        continue
    b = bbox(o)
    cx, cy = (b[0]+b[1])/2, (b[2]+b[3])/2
    if -41 < cy < -38 and b[5] < 9 and (16 < cx < 30 or 38 < cx < 52):
        near_gate.append(o)
show("NEAR-GATE-PILLAR objects", near_gate, 40)

# 3. Di Lac statue — find its mesh(es)
dl = [o for o in bpy.data.objects if o.type == 'MESH' and any(
    k in o.name for k in ('DiLac', 'Di_Lac', 'Di Lac', 'di_lac', 'Maitreya', 'DiLac'.lower()))]
show("DILAC name-match", dl, 20)
# spatial: platform per P2 notes x -34..-14, y -11..8, statue z up to ~8
cand = []
for o in bpy.data.objects:
    if o.type != 'MESH':
        continue
    b = bbox(o)
    cx, cy = (b[0]+b[1])/2, (b[2]+b[3])/2
    if -36 < cx < -12 and -12 < cy < 10 and b[5] > 3.0 and b[4] > 0.5:
        cand.append(o)
show("DILAC spatial candidates (z>3, on platform)", cand, 30)

# 4. Existing P2 trees: trunk positions (for new-tree placement + foreground densify)
trunks = [o for o in bpy.data.objects if o.type == 'MESH' and o.name.startswith('Thân cây')]
print(f"== TRUNKS: {len(trunks)}")
for o in sorted(trunks, key=lambda o: (round(bbox(o)[2]), round(bbox(o)[0]))):
    b = bbox(o)
    print(f"  {o.name!r} cx={(b[0]+b[1])/2:.1f} cy={(b[2]+b[3])/2:.1f} ztop={b[5]:.2f}")
canopies = [o for o in bpy.data.objects if o.type == 'MESH' and o.name.startswith(('P2_TanCay', 'P2_TanNen'))]
print(f"== CANOPIES P2: {len(canopies)}")
palms = [o for o in bpy.data.objects if o.type == 'MESH' and o.name.startswith('P2_Co')]
print(f"== PALM parts: {len(palms)}")
flowers = [o for o in bpy.data.objects if o.type == 'MESH' and o.name.startswith('P2_HoaGiay')]
print(f"== FLOWER clusters: {len(flowers)}")

# 5. Cameras (verify names for render script)
cams = [o for o in bpy.data.objects if o.type == 'CAMERA']
print("== CAMERAS:", [(o.name, tuple(round(v, 1) for v in o.location)) for o in cams])
sc = bpy.context.scene
print("== SCENE: engine", sc.render.engine, "res", sc.render.resolution_x, sc.render.resolution_y,
      "samples", sc.cycles.samples if hasattr(sc, 'cycles') else '-', "world", sc.world.name if sc.world else None)
print("== MATERIALS P2 present:", [n for n in ('P2_LaA', 'P2_LaB', 'P2_LaC', 'P2_LaA2', 'P2_LaC2',
      'P2_CoA', 'P2_CoB', 'P2_HoaGiay', 'P2_ThanCay') if n in bpy.data.materials])
print("PROBE DONE")
