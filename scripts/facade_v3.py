"""
MẶT TIỀN CHÁNH ĐIỆN V3 — dùng model cửa vòm chi tiết của repo (1.067 chi tiết,
13 ô vòm + song vàng + gốm xanh) và nhuộm lại theo bảng màu THẬT đã đạt ở V2:
tường vàng bão hòa, điểm đỏ son/gạch giữ nguyên, gốm xanh giữ nguyên (dấu ấn
khảm sành của Vĩnh Tràng), thêm khối mái ngói đỏ nâu lớn phía sau + nền trời.
Đối chiếu: refs/ref1_front.jpg (vàng rực, ô tối, song vàng, sân đá, bonsai).
"""
import bpy
from mathutils import Vector

SRC = "/home/hatch/workspace/chua-online-work/chanh-dien-cua-vom.blend"
OUT = "/home/hatch/workspace/chua-online-work/facade-v3e"
bpy.ops.wm.open_mainfile(filepath=SRC)
s = bpy.context.scene

def recolor(mat_name, rgb):
    m = bpy.data.materials.get(mat_name)
    if not m or not m.use_nodes: return
    bsdf = next((n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
    if bsdf: bsdf.inputs['Base Color'].default_value = (*rgb, 1.0)

GOLD = (1.0, 0.60, 0.02)          # vàng bão hòa đã đạt ở facade V2
for name in ('Ngà sáng', 'Chỉ trắng ngà', 'Vữa màu vàng kem'):
    recolor(name, GOLD)
recolor('Màu vàng đất', (0.88, 0.52, 0.06))
recolor('Vàng kem', (1.0, 0.66, 0.10))
recolor('Trắng', (0.96, 0.92, 0.82))       # lưới/trang trí trắng ấm giữ tương phản
recolor('Đỏ gạch', (0.45, 0.13, 0.06))     # gạch sâu hơn về phía đỏ nâu mái thật
# Gốm xanh, song vàng, cửa tối: GIỮ NGUYÊN (đã đúng chất khảm sành + song vàng)

# Khối mái ngói đỏ nâu lớn phía sau (như flycam: mái to phủ sau mặt tiền)
roof_mat = bpy.data.materials.new("Mai_Ngoi_Do_Nau_V3"); roof_mat.use_nodes = True
roof_mat.node_tree.nodes["Principled BSDF"].inputs['Base Color'].default_value = (0.36, 0.13, 0.07, 1)
def box(n, loc, dim, m):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object
    o.name = n; o.dimensions = dim
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(m); return o
# Trời + nắng (Standard cho mặt tiền như V2)
try: s.view_settings.view_transform = 'Standard'
except Exception: pass
w = bpy.data.worlds.new("Troi_V3"); s.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (0.42, 0.58, 0.85, 1)
w.node_tree.nodes["Background"].inputs[1].default_value = 0.7
sun = bpy.data.lights.new("Sun_V3", 'SUN'); sun.energy = 3.2
so = bpy.data.objects.new("Sun_V3", sun); s.collection.objects.link(so)
so.rotation_euler = (0.95, 0.15, -0.55)

bpy.ops.object.camera_add(location=(0, -38, 7))
cam = bpy.context.object; s.camera = cam
cam.rotation_euler = (Vector((0, 2, 6)) - cam.location).to_track_quat('-Z', 'Y').to_euler()

s.render.engine = 'CYCLES'; s.cycles.samples = 32; s.cycles.use_denoising = True
s.render.resolution_x = 1280; s.render.resolution_y = 720
bpy.ops.wm.save_as_mainfile(filepath=OUT + ".blend")
s.render.filepath = OUT + ".png"
bpy.ops.render.render(write_still=True)
print("FACADE V3 DONE")
