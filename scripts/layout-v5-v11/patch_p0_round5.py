# -*- coding: utf-8 -*-
"""P0 patch round 5 — 2 sửa từ soi render vòng 4:
1) Trời ở góc cổng/Di Lặc xám + đốm nhiễu (fireflies từ HDRI kloppenheim_02)
   -> đổi sang kloppenheim_06_puresky (xanh trong, gradient mịn), strength 0.85
2) Cam_DiLac quay vào LƯNG tượng -> đặt lại camera sang mặt trước (đông-nam,
   phía đường đi trung tâm), nhìn vào mặt/bảng chữ của tượng Di Lặc.
Chạy trên layout_v5_p0.blend (sau round 4), lưu tại chỗ."""
import bpy, os, mathutils

TEX = os.path.expanduser("~/workspace/chua-online-work/textures")
BLEND = os.path.expanduser("~/workspace/chua-online-work/layout_v5_p0.blend")

sc = bpy.context.scene
w = sc.world; w.use_nodes = True
tex = None
for n in w.node_tree.nodes:
    if n.type == 'TEX_ENVIRONMENT':
        tex = n
assert tex is not None, "no env texture node in world"
img = bpy.data.images.load(os.path.join(TEX, "sky_blue_clear_2k.hdr"),
                           check_existing=True)
tex.image = img
for n in w.node_tree.nodes:
    if n.type == 'BACKGROUND':
        n.inputs['Strength'].default_value = 0.85
print("world -> sky_blue_clear_2k.hdr strength 0.85")

cam = bpy.data.objects.get('Cam_DiLac')
assert cam is not None
cam.location = (-6.0, -8.0, 2.6)
target = mathutils.Vector((-24.5, 2.5, 3.4))
d = target - mathutils.Vector(cam.location)
cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
cam.data.lens = 38
print("Cam_DiLac -> front view", tuple(round(v, 1) for v in cam.location))

for im in bpy.data.images:
    try:
        if im.source == 'FILE':
            im.pack()
    except Exception:
        pass
bpy.ops.wm.save_as_mainfile(filepath=BLEND)
print(f"SAVED {BLEND} size={os.path.getsize(BLEND)}")
print("PATCH5 DONE")
