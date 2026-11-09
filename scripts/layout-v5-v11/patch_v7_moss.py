"""
V7 FIX rêu mái (vòng 2): bản đầu rêu quá nhạt/liên tục — đọc như tuyết/vôi trắng
ở góc ground (G-R tăng +19/+34 nhưng VALUE quá sáng, dải liền 2 hàng ngói).
Sửa: (1) màu tối hơn + alpha loang hơn (ngưỡng 0.42->0.70); (2) noise theo UV
từng card (trước đây theo Object trên mesh join 30m -> vệt loang 10m liền mạch);
(3) bỏ hàng ngang hàng ngói 1, chỉ giữ hàng 0 + mặt đứng; (4) chừa khoảng trống
mỗi đoạn thứ 4. Ghi đè layout_v9_v7.blend (cùng vòng V7, chưa giao).
"""
import bpy, math
from mathutils import Vector, Matrix

W = "/home/hatch/workspace/chua-online-work/"

def log(*a):
    print(" ".join(str(x) for x in a), flush=True)

# --- xoa reu cu ---
old = bpy.data.objects.get("V7_ReuMai")
if old:
    bpy.data.objects.remove(old, do_unlink=True)
    log("removed old V7_ReuMai")
oldmat = bpy.data.materials.get("V7_ReuMai")
if oldmat:
    bpy.data.materials.remove(oldmat)

# --- material moi: toi hon, loang hon, noise theo UV ---
m = bpy.data.materials.new("V7_ReuMai"); m.use_nodes = True
nt = m.node_tree; bs = nt.nodes["Principled BSDF"]
tc = nt.nodes.new('ShaderNodeTexCoord')
noise = nt.nodes.new('ShaderNodeTexNoise')
noise.inputs['Scale'].default_value = 2.5
noise.inputs['Detail'].default_value = 3.5
noise.inputs['Roughness'].default_value = 0.75
nt.links.new(tc.outputs['UV'], noise.inputs['Vector'])
ramp_c = nt.nodes.new('ShaderNodeValToRGB')
ramp_c.color_ramp.elements[0].color = (0.05, 0.09, 0.02, 1)
ramp_c.color_ramp.elements[0].position = 0.35
ramp_c.color_ramp.elements[1].color = (0.14, 0.24, 0.07, 1)
ramp_c.color_ramp.elements[1].position = 0.80
nt.links.new(noise.outputs['Fac'], ramp_c.inputs['Fac'])
nt.links.new(ramp_c.outputs['Color'], bs.inputs['Base Color'])
ramp_a = nt.nodes.new('ShaderNodeValToRGB')
ramp_a.color_ramp.elements[0].position = 0.42
ramp_a.color_ramp.elements[0].color = (0, 0, 0, 1)
ramp_a.color_ramp.elements[1].position = 0.70
ramp_a.color_ramp.elements[1].color = (1, 1, 1, 1)
nt.links.new(noise.outputs['Fac'], ramp_a.inputs['Fac'])
nt.links.new(ramp_a.outputs['Color'], bs.inputs['Alpha'])
bs.inputs['Roughness'].default_value = 1.0
log("new moss material: darker, patchier, UV noise")

def quad_obj(name, center, w, h, rot_euler, mtl):
    mm = (Matrix.Rotation(rot_euler[2], 4, 'Z') @ Matrix.Rotation(rot_euler[1], 4, 'Y')
          @ Matrix.Rotation(rot_euler[0], 4, 'X'))
    c = Vector(center)
    pts = []
    for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        pts.append(c + mm @ Vector((sx * w / 2, 0, sy * h / 2)))
    me = bpy.data.meshes.new(name)
    me.from_pydata(pts, [], [[0, 1, 2, 3]])
    uv = me.uv_layers.new(name="UVMap")
    for i, (u, v) in enumerate([(0, 0), (1, 0), (1, 1), (0, 1)]):
        uv.data[i].uv = (u, v)
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    if mtl: me.materials.append(mtl)
    return ob

def join_objs(objs, name):
    if not objs: return None
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join()
    ob = bpy.context.object; ob.name = name
    return ob

moss = []
# mat truoc: hang 0 ngang + mat dung hang 0; bo doan thu 4 va 8 (khoang trong)
for k, xc in enumerate([10.5, 13.5, 16.5, 19.5, 22.5, 25.5, 28.5, 31.5, 34.5]):
    if k in (3, 7):
        continue
    moss.append(quad_obj("V7_Reu", (xc, -3.0, 7.28), 2.7, 1.2, (math.radians(90), 0, 0), m))
    moss.append(quad_obj("V7_Reu", (xc, -3.72, 6.88), 2.7, 0.68, (0, 0, math.radians(180)), m))
# mat sau: hang Sau_0 ngang + mat dung
for k, xc in enumerate([13.5, 18.5, 23.5, 28.5, 33.5]):
    if k == 2:
        continue
    moss.append(quad_obj("V7_Reu", (xc, 17.5, 7.28), 2.7, 1.2, (math.radians(90), 0, 0), m))
    moss.append(quad_obj("V7_Reu", (xc, 18.22, 6.88), 2.7, 0.68, (0, 0, 0), m))
# hong dong/tay: mat ngoai + mat tren hang 0 (giu nguyen so luong)
for k, yc in enumerate([0.0, 6.0, 12.0]):
    moss.append(quad_obj("V7_Reu", (38.22, yc, 7.0), 2.4, 0.9, (0, math.radians(90), 0), m))
    moss.append(quad_obj("V7_Reu", (37.65, yc, 7.52), 1.0, 2.4, (math.radians(90), 0, math.radians(90)), m))
    moss.append(quad_obj("V7_Reu", (7.78, yc, 7.0), 2.4, 0.9, (0, math.radians(-90), 0), m))
    moss.append(quad_obj("V7_Reu", (8.35, yc, 7.52), 1.0, 2.4, (math.radians(90), 0, math.radians(90)), m))
join_objs(moss, "V7_ReuMai")
log("moss cards rebuilt:", len(moss), "(was 54)")

bpy.ops.wm.save_as_mainfile(filepath=W + "layout_v9_v7.blend")
log("SAVED layout_v9_v7.blend (moss v2)")
print("PATCH MOSS DONE", flush=True)
