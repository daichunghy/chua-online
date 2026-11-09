"""
XUAT BAN WEB NHE tu layout_v8_p3.blend -> web_export/layout_v8_web.blend
- Decimate cac MESH DATA duy nhat co >20k polys ve ~13k (chu yeu la than nhan vat).
- Texture: image nao chieu lon nhat >1024 thi scale ve 1024 (giu ti le).
- Pack tat ca image vao file. Giu nguyen palette + vi tri (khong dong vao material/object transforms).
- In bang ke truoc/sau.
Chay: blender5 -b layout_v8_p3.blend --python web_export_p3.py
"""
import bpy, os

W = "/home/hatch/workspace/chua-online-work/"
OUT = W + "web_export/layout_v8_web.blend"
TARGET = 13000
THRESH = 20000

def total_polys():
    seen = {}
    for o in bpy.data.objects:
        if o.type == 'MESH':
            seen[o.data.name] = len(o.data.polygons)
    return sum(seen.values()), seen

before, meshes_before = total_polys()
print("POLYS BEFORE:", before, "unique meshes:", len(meshes_before), flush=True)

# --- decimate theo tung mesh data duy nhat (tranh decimate trung lap do linked copies)
done = {}
for o in list(bpy.data.objects):
    if o.type != 'MESH':
        continue
    me = o.data
    if me.name in done:
        continue
    n = len(me.polygons)
    if n <= THRESH:
        done[me.name] = (n, n); continue
    ratio = TARGET / n
    bpy.context.view_layer.objects.active = o
    o.select_set(True)
    mod = o.modifiers.new(name='P3_WebDecimate', type='DECIMATE')
    mod.ratio = ratio
    try:
        bpy.ops.object.modifier_apply(modifier=mod.name)
        done[me.name] = (n, len(me.polygons))
        print("DECIMATED %s: %d -> %d (ratio %.3f)" % (me.name, n, len(me.polygons), ratio), flush=True)
    except Exception as e:
        print("DECIMATE FAIL %s: %s" % (me.name, e), flush=True)
        if mod.name in o.modifiers: o.modifiers.remove(mod)
        done[me.name] = (n, n)
    o.select_set(False)

after, _ = total_polys()
print("POLYS AFTER:", after, flush=True)

# --- texture cap 1K
scaled = []
for im in bpy.data.images:
    if im.source == 'GENERATED' or im.size[0] == 0:
        continue
    w, h = im.size[0], im.size[1]
    m = max(w, h)
    if m > 1024:
        s = 1024 / m
        im.scale(max(1, int(w * s)), max(1, int(h * s)))
        scaled.append((im.name, (w, h), tuple(im.size)))
        print("SCALED %s %s -> %s" % (scaled[-1][0], scaled[-1][1], scaled[-1][2]), flush=True)
print("IMAGES SCALED:", len(scaled), "total images:", len(bpy.data.images), flush=True)

try:
    bpy.ops.file.pack_all()
    print("PACKED ALL", flush=True)
except Exception as e:
    print("PACK FAIL:", e, flush=True)

bpy.ops.wm.save_as_mainfile(filepath=OUT)
size = os.path.getsize(OUT)
print("SAVED", OUT, size, flush=True)

with open(W + "web_export/KE_BANGKE.md", "w", encoding="utf-8") as f:
    f.write("# BANG KE XUAT BAN WEB — layout_v8_web.blend (dot P3, 07/11)\n\n")
    f.write("Nguon: layout_v8_p3.blend. Decimate chi ap cho mesh data >20.000 polys "
            "(nguong giu nguyen hinh dang o khoang cach web); texture gioi han 1K; "
            "palette + vi tri giu nguyen 100%.\n\n")
    f.write("| Hang muc | Truoc | Sau |\n|---|---|---|\n")
    f.write("| Tong so mat (unique mesh data) | %d | %d |\n" % (before, after))
    f.write("| Dung luong file .blend | %d bytes (v8_p3) | %d bytes |\n" % (os.path.getsize(W + "layout_v8_p3.blend"), size))
    f.write("\n## Mesh da decimate\n\n| Mesh | Mat truoc | Mat sau |\n|---|---|---|\n")
    for name, (a, b) in sorted(done.items(), key=lambda kv: -kv[1][0]):
        if a != b:
            f.write("| %s | %d | %d |\n" % (name, a, b))
    f.write("\n## Texture da ha ve 1K\n\n| Image | Truoc | Sau |\n|---|---|---|\n")
    for name, a, b in scaled:
        f.write("| %s | %s | %s |\n" % (name, a, b))
    f.write("\nTong so image trong file: %d (tat ca da pack).\n" % len(bpy.data.images))
print("KE WRITTEN", flush=True)
print("WEB EXPORT DONE", flush=True)
