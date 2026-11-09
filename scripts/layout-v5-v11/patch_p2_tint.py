"""PATCH P2: sua nhuom 2 nhan vat nam (S2-nam-xam geometry_0.006, path-nam-lam
geometry_0.008) — vong build dung phep nhan bi clamp 2.4 nen mau khong toi dich.
Cach dung: dat lai mau theo ti le luminance: new = target * (lum_loop/lum_modal).
Mo layout_v7_p2.blend, sua, luu lai cung file."""
import bpy, math
from collections import Counter

W = "/home/hatch/workspace/chua-online-work/"
JOBS = [("geometry_0.006", (0.42, 0.41, 0.40)),   # xam
        ("geometry_0.008", (0.36, 0.40, 0.52))]   # lam

def lum(c): return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]

for name, target in JOBS:
    ob = bpy.data.objects.get(name)
    assert ob is not None, name
    me = ob.data
    ca = me.color_attributes[0]
    cols = [tuple(d.color[:3]) for d in ca.data]
    cnt = Counter(tuple(round(c / 0.04) for c in col) for col in cols)
    modal_key = cnt.most_common(1)[0][0]
    modal = tuple(k * 0.04 for k in modal_key)
    lm = lum(modal)
    changed = 0
    for d in ca.data:
        col = d.color
        cen = tuple(round(c / 0.04) * 0.04 for c in col[:3])
        dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(cen, modal)))
        if dist < 0.16 and lm > 0.01:
            f = lum(col[:3]) / lm
            d.color = (min(1, target[0] * f), min(1, target[1] * f), min(1, target[2] * f), col[3])
            changed += 1
    print(f"PATCH {name}: modal {tuple(round(v,3) for v in modal)} lum {lm:.3f} -> target {target}, loops {changed}/{len(cols)}", flush=True)

bpy.ops.wm.save_as_mainfile(filepath=W + "layout_v7_p2.blend")
print("PATCH SAVED", flush=True)
