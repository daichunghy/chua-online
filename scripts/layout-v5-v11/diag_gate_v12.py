# V12 gate diagnostic (read-only, tren file V14):
# - Nguon = cac object dung chung datablock voi ban sao cong (khop chac chan).
# - Kiem: ti le khoang cach tung cap tam manh (copy/nguon) co hang so khong
#   (= ban sao la anh dong dang cua goc), bbox nhom theo tung truc, manh lech nhat.
import bpy, itertools
import numpy as np
from mathutils import Vector

V14 = "/home/hatch/workspace/chua-online-work/layout_v14_v12.blend"

def wctr(o):
    ws = [o.matrix_world @ Vector(c) for c in o.bound_box]
    return Vector(((min(v.x for v in ws)+max(v.x for v in ws))/2,
                   (min(v.y for v in ws)+max(v.y for v in ws))/2,
                   (min(v.z for v in ws)+max(v.z for v in ws))/2))

def wbbox(o):
    ws = [o.matrix_world @ Vector(c) for c in o.bound_box]
    return (Vector((min(v.x for v in ws), min(v.y for v in ws), min(v.z for v in ws))),
            Vector((max(v.x for v in ws), max(v.y for v in ws), max(v.z for v in ws))))

bpy.ops.wm.open_mainfile(filepath=V14)

for tag in ('PT', 'TD'):
    parts = [o for o in bpy.data.objects if o.name.startswith(f'V10_GateBuddha_{tag}_')]
    pairs = []
    for p in parts:
        srcs = [o for o in bpy.data.objects
                if o.type == 'MESH' and o.data == p.data and o is not p
                and not o.name.startswith('V10_GateBuddha_')]
        if len(srcs) == 1:
            pairs.append((p, srcs[0]))
    print(f"\n[GATE {tag}] {len(pairs)} cap copy/nguon")
    # pairwise center-distance ratios
    ratios = []
    for (p1, s1), (p2, s2) in itertools.combinations(pairs, 2):
        ds = (wctr(s1) - wctr(s2)).length
        if ds < 0.05: continue
        dc = (wctr(p1) - wctr(p2)).length
        ratios.append(dc / ds)
    ratios = np.array(ratios)
    print(f"[GATE {tag}] pair-dist ratio: median={np.median(ratios):.4f} min={ratios.min():.4f} max={ratios.max():.4f}")
    # group bbox per-axis ratio
    def group_dims(objs):
        los, his = zip(*[wbbox(o) for o in objs])
        lo = Vector((min(v.x for v in los), min(v.y for v in los), min(v.z for v in los)))
        hi = Vector((max(v.x for v in his), max(v.y for v in his), max(v.z for v in his)))
        return hi - lo
    dc = group_dims([p for p, _ in pairs]); ds = group_dims([s for _, s in pairs])
    print(f"[GATE {tag}] group bbox ratio per axis: {[round(dc[i]/ds[i], 4) for i in range(3)]}")
    # per-part Mc dev from median Mc
    Mcs = np.array([(p.matrix_world @ s.matrix_world.inverted()) for p, s in pairs])
    med = np.median(Mcs, axis=0)
    devs = sorted(((float(np.abs(Mc - med).max()), p.name) for Mc, (p, s) in zip(Mcs, pairs)), reverse=True)
    print(f"[GATE {tag}] 5 manh lech Mc nhat: {[(n, round(d, 4)) for d, n in devs[:5]]}")
    print(f"[GATE {tag}] Mc median SV: {[round(float(v), 4) for v in np.linalg.svd(med[:3, :3], compute_uv=False)]}")
print("GATE DIAG DONE", flush=True)
