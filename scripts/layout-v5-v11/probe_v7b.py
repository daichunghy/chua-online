"""V7 PROBE 2 — roof eave geometry + full Di Lac part list (no changes, no save)."""
import bpy
from mathutils import Vector

def bbox(o):
    ws = [o.matrix_world @ Vector(v) for v in o.bound_box]
    return (min(v.x for v in ws), max(v.x for v in ws),
            min(v.y for v in ws), max(v.y for v in ws),
            min(v.z for v in ws), max(v.z for v in ws))

print("== ROOF objects with Mai_Ngoi in materials ==")
n = 0
for o in bpy.data.objects:
    if o.type != 'MESH':
        continue
    if any(m and 'Mai_Ngoi' in m.name for m in o.data.materials):
        b = bbox(o)
        print(f"  {o.name!r} verts={len(o.data.vertices)} x[{b[0]:.1f},{b[1]:.1f}] y[{b[2]:.1f},{b[3]:.1f}] z[{b[4]:.2f},{b[5]:.2f}]")
        n += 1
print("  total:", n)

print("== HALL roof: objects with 'Mái' or 'Mai' in name (first 40) ==")
n = 0
for o in bpy.data.objects:
    if o.type == 'MESH' and ('Mái' in o.name or 'Mai' in o.name):
        b = bbox(o)
        print(f"  {o.name!r} verts={len(o.data.vertices)} x[{b[0]:.1f},{b[1]:.1f}] y[{b[2]:.1f},{b[3]:.1f}] z[{b[4]:.2f},{b[5]:.2f}]")
        n += 1
        if n >= 40:
            break
print("  total shown:", n)

print("== DI LAC full part list (bbox center in x -29..-19, y -3..3, z 3..11) ==")
for o in sorted(bpy.data.objects, key=lambda o: o.name):
    if o.type != 'MESH':
        continue
    b = bbox(o)
    cx, cy, cz = (b[0]+b[1])/2, (b[2]+b[3])/2, (b[4]+b[5])/2
    if -29 < cx < -19 and -3 < cy < 3 and 3 < cz < 11:
        print(f"  {o.name!r} verts={len(o.data.vertices)} x[{b[0]:.2f},{b[1]:.2f}] y[{b[2]:.2f},{b[3]:.2f}] z[{b[4]:.2f},{b[5]:.2f}] mats={[m.name if m else None for m in o.data.materials]}")

print("== DI LAC body below head (z 0.5..7.5, same x/y zone) ==")
for o in sorted(bpy.data.objects, key=lambda o: o.name):
    if o.type != 'MESH':
        continue
    b = bbox(o)
    cx, cy, cz = (b[0]+b[1])/2, (b[2]+b[3])/2, (b[4]+b[5])/2
    if -29 < cx < -19 and -3 < cy < 3 and 0.5 < cz < 7.5:
        print(f"  {o.name!r} verts={len(o.data.vertices)} x[{b[0]:.2f},{b[1]:.2f}] y[{b[2]:.2f},{b[3]:.2f}] z[{b[4]:.2f},{b[5]:.2f}]")
print("PROBE2 DONE")
