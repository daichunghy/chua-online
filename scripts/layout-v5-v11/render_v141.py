# V14.1 RENDER — chi 1 goc mat A Di Da, CUNG camera V13/V14
# (V13_CamFaceAdida: lens 42, offset (0.5, 4.4, -0.95) tu tam dau A Di Da)
# de coordinator so truc tiep voi layout_v16_face_adida.png.
# Dau ra: layout/layout_v17_face_adida.png. Bo qua neu da co file > 50KB.
import bpy, os, re
from mathutils import Vector

BLEND = "/home/hatch/workspace/chua-online-work/layout_v17_v141.blend"
OUT = "/home/hatch/workspace/chua-online-work/layout/layout_v17_face_adida.png"
bpy.ops.wm.open_mainfile(filepath=BLEND)
sc = bpy.context.scene

def base(n):
    return re.sub(r"\.\d{3}$", "", n)

def wbox(o):
    ws = [o.matrix_world @ Vector(c) for c in o.bound_box]
    return ([min(v[i] for v in ws) for i in range(3)],
            [max(v[i] for v in ws) for i in range(3)])

def head_center(pred):
    hmn = [1e9] * 3; hmx = [-1e9] * 3; n = 0
    for o in bpy.data.objects:
        if o.type != 'MESH' or not base(o.name).startswith("Head_"):
            continue
        mn, mx = wbox(o)
        c = Vector([(mn[i] + mx[i]) / 2 for i in range(3)])
        if not pred(c):
            continue
        n += 1
        for i in range(3):
            hmn[i] = min(hmn[i], mn[i]); hmx[i] = max(hmx[i], mx[i])
    assert n >= 5, f"head pieces found: {n}"
    return (Vector([(hmn[i] + hmx[i]) / 2 for i in range(3)]),
            hmx[2] - hmn[2])

def look(cam, target):
    d = (target - cam.location).normalized()
    cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()

def mkcam(name, lens, pos, target):
    if bpy.data.objects.get(name):
        cam = bpy.data.objects[name]
        cam.location = pos
        look(cam, target)
        return cam
    cd = bpy.data.cameras.new(name); cd.lens = lens
    cam = bpy.data.objects.new(name, cd)
    sc.collection.objects.link(cam)
    cam.location = pos
    look(cam, target)
    return cam

ad_ctr, ad_h = head_center(lambda c: abs(c.x + 14.0) < 3.0 and abs(c.y + 30.8) < 3.0)
print("[V141R] adida head ctr:", [round(v, 2) for v in ad_ctr], "h:", round(ad_h, 3), flush=True)
cam = mkcam('V13_CamFaceAdida', 42, ad_ctr + Vector((0.5, 4.4, -0.95)), ad_ctr)
if os.path.exists(OUT) and os.path.getsize(OUT) > 50000:
    print("SKIP done", OUT, flush=True)
else:
    sc.camera = cam
    sc.render.filepath = OUT
    bpy.ops.render.render(write_still=True)
    print("RENDERED ->", OUT, flush=True)
print("RENDER V141 DONE", flush=True)
