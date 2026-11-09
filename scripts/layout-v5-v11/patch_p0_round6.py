# -*- coding: utf-8 -*-
"""P0 patch round 6:
1) Cam_DiLac: mặt tượng hướng BẮC (+Y, đo pháp tuyến FrontText) ->
   camera đặt phía bắc (-24, 21, 4.0) nhìn về tượng, lens 40.
2) Trời: chèn Hue Saturation (Sat 1.35) vào world env -> xanh sâu hơn
   theo theme (trời xanh rực), giữ nguyên ánh sáng tổng thể.
Chạy trên layout_v5_p0.blend (sau round 5), lưu tại chỗ."""
import bpy, os, mathutils

TEX = os.path.expanduser("~/workspace/chua-online-work/textures")
BLEND = os.path.expanduser("~/workspace/chua-online-work/layout_v5_p0.blend")
sc = bpy.context.scene

cam = bpy.data.objects.get('Cam_DiLac')
assert cam is not None
cam.location = (-24.0, 21.0, 4.0)
target = mathutils.Vector((-24.0, 1.5, 4.3))
d = target - mathutils.Vector(cam.location)
cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
cam.data.lens = 40
print("Cam_DiLac -> north front view")

w = sc.world; w.use_nodes = True
wnt = w.node_tree
tex = [n for n in wnt.nodes if n.type == 'TEX_ENVIRONMENT'][0]
bg = [n for n in wnt.nodes if n.type == 'BACKGROUND'][0]
# gỡ link tex->bg hiện tại, chèn HueSat
for l in list(bg.inputs['Color'].links):
    wnt.links.remove(l)
hs = wnt.nodes.new('ShaderNodeHueSaturation')
hs.location = (bg.location.x - 200, bg.location.y)
hs.inputs['Saturation'].default_value = 1.35
hs.inputs['Hue'].default_value = 0.5
hs.inputs['Value'].default_value = 1.0
hs.inputs['Fac'].default_value = 1.0
wnt.links.new(tex.outputs['Color'], hs.inputs['Color'])
wnt.links.new(hs.outputs['Color'], bg.inputs['Color'])
print("world: HueSat saturation 1.35 inserted")

for im in bpy.data.images:
    try:
        if im.source == 'FILE':
            im.pack()
    except Exception:
        pass
bpy.ops.wm.save_as_mainfile(filepath=BLEND)
print(f"SAVED {BLEND} size={os.path.getsize(BLEND)}")
print("PATCH6 DONE")
