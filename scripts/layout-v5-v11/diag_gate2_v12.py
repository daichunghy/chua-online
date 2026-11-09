# V12 gate diagnostic 2 (read-only): sau khi hoan tra x1.35 — manh nao con lech
# Mc, lech o khoi xoay hay dich, va ti le khoang cach cap tam con hang so khong.
import bpy, itertools
import numpy as np
from mathutils import Vector

F = "/home/hatch/workspace/chua-online-work/layout_v14_v12.blend"

def wctr(o):
    ws = [o.matrix_world @ Vector(c) for c in o.bound_box]
    return Vector(((min(v.x for v in ws)+max(v.x for v in ws))/2,
                   (min(v.y for v in ws)+max(v.y for v in ws))/2,
                   (min(v.z for v in ws)+max(v.z for v in ws))/2))

bpy.ops.wm.open_mainfile(filepath=F)
tag = 'PT'
parts = [o for o in bpy.data.objects if o.name.startswith(f'V10_GateBuddha_{tag}_')]
pairs = []
for p in parts:
    srcs = [o for o in bpy.data.objects
            if o.type == 'MESH' and o.data == p.data and o is not p
            and not o.name.startswith('V10_GateBuddha_')]
    if len(srcs) == 1:
        pairs.append((p, srcs[0]))
Mcs = np.array([(p.matrix_world @ s.matrix_world.inverted()) for p, s in pairs])
med = np.median(Mcs, axis=0)
print("[DIAG2] per-part dev vs median Mc:")
for Mc, (p, s) in zip(Mcs, pairs):
    d = float(np.abs(Mc - med).max())
    if d > 0.01:
        dR = float(np.abs(Mc[:3, :3] - med[:3, :3]).max())
        dT = float(np.abs(Mc[:3, 3] - med[:3, 3]).max())
        print(f"   {p.name:<36} dev={d:.4f} (rot-block {dR:.4f}, transl {dT:.4f})")
ratios = []
for (p1, s1), (p2, s2) in itertools.combinations(pairs, 2):
    ds = (wctr(s1) - wctr(s2)).length
    if ds < 0.05: continue
    ratios.append((wctr(p1) - wctr(p2)).length / ds)
ratios = np.array(ratios)
print(f"[DIAG2] pair-dist ratio: median={np.median(ratios):.4f} min={ratios.min():.4f} max={ratios.max():.4f} "
      f"pairs>1% off: {(np.abs(ratios - np.median(ratios)) > 0.002).sum()}/{len(ratios)}")
print("DIAG2 DONE", flush=True)
