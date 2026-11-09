# V12 FIX B — bo sung 7 manh net mat (FeatureShadow) bi thieu o tuong hoc cong.
# Ban sao V10 loc theo vat lieu WhiteStone/HairStone nen sot cac ong net mat
# (may/moi/mieng) — tuong cong thieu mat. Bo sung bang dung phep dong dang S
# cua nhom sao (do tu 32 cap copy/nguon, da kiem: hang so tuyet doi), chia se
# mesh goc nhu cach V10 lam. Dai sen/be/bang cua ban chinh KHONG dua vao —
# hoc cong co be rieng (dung thiet ke V10 + ref6).
import bpy
import numpy as np

F = "/home/hatch/workspace/chua-online-work/layout_v14_v12.blend"
FEATURES = ['Head_browL', 'Head_browR', 'Head_eyeL', 'Head_eyeR',
            'Head_lidL', 'Head_lidR', 'Head_mouth']

bpy.ops.wm.open_mainfile(filepath=F)
sc = bpy.context.scene

for gx, tag in ((23.0, 'PT'), (45.0, 'TD')):
    parts = [o for o in bpy.data.objects if o.name.startswith(f'V10_GateBuddha_{tag}_')]
    Mcs = []
    for p in parts:
        srcs = [o for o in bpy.data.objects
                if o.type == 'MESH' and o.data == p.data and o is not p
                and not o.name.startswith('V10_GateBuddha_')]
        if len(srcs) == 1:
            Mcs.append(np.array(p.matrix_world @ srcs[0].matrix_world.inverted()))
    S = np.median(Mcs, axis=0)
    from mathutils import Matrix
    Sm = Matrix(S.tolist())
    coll = parts[0].users_collection[0] if parts and parts[0].users_collection else sc.collection
    added = []
    for fname in FEATURES:
        src = bpy.data.objects.get(fname)
        assert src is not None, f"missing source {fname}"
        d = src.copy(); d.data = src.data
        d.name = f'V10_GateBuddha_{tag}_{fname}'
        coll.objects.link(d)
        d.matrix_world = Sm @ src.matrix_world
        added.append(d)
    # kiem: Mc cua manh moi phai trung S
    devs = []
    for d in added:
        src = bpy.data.objects.get(d.name[len(f'V10_GateBuddha_{tag}_'):])
        Mc = np.array(d.matrix_world @ src.matrix_world.inverted())
        devs.append(float(np.abs(Mc - S).max()))
    print(f"[V12FIXB] {tag}: added {len(added)} feature parts, Mc dev vs S max = {max(devs):.5f}", flush=True)

bpy.ops.wm.save_as_mainfile(filepath=F)
print("FIX V12B SAVED", flush=True)
