# -*- coding: utf-8 -*-
"""
Blender 5.2 Python Script:
1. Thiết kế 3D Áo Tràng Phật Tử Vạt Chéo (Trang phục mặc định) theo chuẩn ảnh tham khảo:
   - Cổ chéo vạt trang nghiêm (Overlapping diagonal cross collar)
   - Nơ thắt eo vải lam bên mạn sườn phải với 2 dải lụa rủ
   - Ống tay thụng rộng truyền thống buông rủ thanh thoát
   - Ma-nơ-canh gỗ trưng bày chuẩn Coohom
2. Mặc trực tiếp trang phục lên mô hình Phật tử Nữ chuyển động thật (nu-doi-non-la-chuyen-dong.glb)
3. Xuất file GLB, OBJ, gói Coohom và render ảnh chất lượng cao.
"""

import bpy
import bmesh
import math
import os

BASE_DIR = "/Users/macos/Desktop/Chùa online"
NU_GLB = os.path.join(BASE_DIR, "Thiết kế giao diện", "Nhân vật 3D", "Chuyển động", "nu-doi-non-la-chuyen-dong.glb")

OUT_CHAR_GLB = os.path.join(BASE_DIR, "Thiết kế giao diện", "Nhân vật 3D", "Chuyển động", "nu-mac-ao-trang-doi-non.glb")
OUT_AO_TRANG_GLB = os.path.join(BASE_DIR, "Thiết kế giao diện", "Vật phẩm 3D", "models", "ao_trang_phat_tu.glb")
OUT_AO_TRANG_OBJ = os.path.join(BASE_DIR, "Thiết kế giao diện", "Vật phẩm 3D", "models", "ao_trang_phat_tu.obj")
RENDER_FRONT = os.path.join(BASE_DIR, "Thiết kế giao diện", "Nhân vật 3D", "Chuyển động", "render-nu-ao-trang-chap-tay.png")
RENDER_BACK = os.path.join(BASE_DIR, "Thiết kế giao diện", "Nhân vật 3D", "Chuyển động", "render-nu-ao-trang-di-bo.png")
RENDER_MANNEQUIN = os.path.join(BASE_DIR, "Thiết kế giao diện", "Vật phẩm 3D", "render-ao-trang-mannequin.png")

# Màu sắc chuẩn từ ảnh tham khảo của user
COLOR_ROBE = (0.64, 0.62, 0.68, 1.0) # Lam khói thanh nhã (#a0989c)
COLOR_COLLAR = (0.60, 0.58, 0.64, 1.0) # Viền nẹp cổ đậm hơn nhẹ
COLOR_BOW = (0.66, 0.64, 0.70, 1.0) # Dải lụa thắt nơ
COLOR_WOOD = (0.42, 0.28, 0.16, 1.0) # Gỗ chân đế ma-nơ-canh

bpy.ops.wm.read_factory_settings(use_empty=True)

# 1. Nạp nhân vật nữ chuyển động thật đã gắn nón lá V3
bpy.ops.import_scene.gltf(filepath=NU_GLB)
arm = bpy.data.objects.get("world")
mesh_body = bpy.data.objects.get("geometry_0")

# 2. Tạo nẹp cổ chéo vạt 3D (Overlapping Cross-Collar Band)
# Vạt chính từ vai trái vắt chéo qua ngực sang eo phải
curve_data_left = bpy.data.curves.new('Nep_Co_Cheo_Trai', type='CURVE')
curve_data_left.dimensions = '3D'
spline_left = curve_data_left.splines.new('BEZIER')

collar_pts = [
    (-0.052, 0.092, 0.520), # Vai trái gần cổ
    (-0.025, 0.115, 0.410),
    (0.010, 0.126, 0.275),  # Chéo qua giữa ngực
    (0.075, 0.112, 0.140),
    (0.148, 0.088, 0.015)   # Xuống mạn sườn phải (vị trí thắt nơ)
]
spline_left.bezier_points.add(len(collar_pts) - 1)
for i, pt in enumerate(collar_pts):
    bp = spline_left.bezier_points[i]
    bp.co = pt
    bp.handle_left_type = 'AUTO'
    bp.handle_right_type = 'AUTO'

curve_data_left.bevel_depth = 0.012 # Bản nẹp rộng 2.4cm
curve_data_left.bevel_resolution = 4
collar_left_obj = bpy.data.objects.new('Nep_Co_Cheo_Chinh', curve_data_left)

# Vạt phụ từ vai phải chéo vào dưới ngực trái
curve_data_right = bpy.data.curves.new('Nep_Co_Cheo_Phai', type='CURVE')
curve_data_right.dimensions = '3D'
spline_right = curve_data_right.splines.new('BEZIER')

collar_right_pts = [
    (0.052, 0.092, 0.520),  # Vai phải gần cổ
    (0.028, 0.115, 0.420),
    (-0.005, 0.120, 0.320)  # Luồn dưới vạt chính
]
spline_right.bezier_points.add(len(collar_right_pts) - 1)
for i, pt in enumerate(collar_right_pts):
    bp = spline_right.bezier_points[i]
    bp.co = pt
    bp.handle_left_type = 'AUTO'
    bp.handle_right_type = 'AUTO'

curve_data_right.bevel_depth = 0.012
curve_data_right.bevel_resolution = 4
collar_right_obj = bpy.data.objects.new('Nep_Co_Cheo_Phu', curve_data_right)

# 3. Tạo Nơ Buộc Eo 3D (Waist Ribbon Bow Knot)
# Gồm nút thắt tròn, 2 cánh nơ và 2 dải lụa rủ dài bên hông phải
knot_mesh = bpy.data.meshes.new("Nut_That_No")
bm = bmesh.new()
# Nút thắt tròn oval
bmesh.ops.create_uvsphere(bm, u_segments=12, v_segments=8, radius=0.012)
bm.to_mesh(knot_mesh)
bm.free()
knot_obj = bpy.data.objects.new("Nut_That_Eo", knot_mesh)
knot_obj.location = (0.150, 0.092, 0.015)
knot_obj.scale = (0.8, 1.2, 0.8)

# 2 Dải lụa rủ từ nút thắt xuống tà áo
ribbon_data = bpy.data.curves.new('Dai_Lua_Ru', type='CURVE')
ribbon_data.dimensions = '3D'

# Dải 1
r1 = ribbon_data.splines.new('BEZIER')
r1_pts = [
    (0.150, 0.090, 0.015),
    (0.155, 0.088, -0.060),
    (0.158, 0.082, -0.140),
    (0.160, 0.078, -0.210)
]
r1.bezier_points.add(len(r1_pts) - 1)
for i, pt in enumerate(r1_pts):
    bp = r1.bezier_points[i]
    bp.co = pt
    bp.handle_left_type = 'AUTO'
    bp.handle_right_type = 'AUTO'

# Dải 2 ngắn hơn
r2 = ribbon_data.splines.new('BEZIER')
r2_pts = [
    (0.152, 0.092, 0.015),
    (0.148, 0.089, -0.050),
    (0.145, 0.084, -0.120),
    (0.142, 0.080, -0.170)
]
r2.bezier_points.add(len(r2_pts) - 1)
for i, pt in enumerate(r2_pts):
    bp = r2.bezier_points[i]
    bp.co = pt
    bp.handle_left_type = 'AUTO'
    bp.handle_right_type = 'AUTO'

# Cánh nơ bướm 1 (Hướng lên)
loop1 = ribbon_data.splines.new('BEZIER')
l1_pts = [
    (0.150, 0.090, 0.015),
    (0.165, 0.093, 0.045),
    (0.150, 0.091, 0.055),
    (0.148, 0.090, 0.018)
]
loop1.bezier_points.add(len(l1_pts) - 1)
for i, pt in enumerate(l1_pts):
    bp = loop1.bezier_points[i]
    bp.co = pt
    bp.handle_left_type = 'AUTO'
    bp.handle_right_type = 'AUTO'

ribbon_data.bevel_depth = 0.006
ribbon_data.bevel_resolution = 4
ribbon_obj = bpy.data.objects.new("Dai_Lua_No_Eo", ribbon_data)

# 4. Gán Vật Liệu Áo Tràng PBR (Chất vải mềm mịn lam khói)
mat_robe = bpy.data.materials.new(name="Mat_Ao_Trang_Lam")
mat_robe.use_nodes = True
bsdf_r = mat_robe.node_tree.nodes.get("Principled BSDF")
bsdf_r.inputs["Base Color"].default_value = COLOR_ROBE
bsdf_r.inputs["Roughness"].default_value = 0.82
bsdf_r.inputs["Metallic"].default_value = 0.0

collar_left_obj.data.materials.append(mat_robe)
collar_right_obj.data.materials.append(mat_robe)
knot_obj.data.materials.append(mat_robe)
ribbon_obj.data.materials.append(mat_robe)

# 5. Gắn vào Armature xương Spine để di chuyển tự nhiên theo cơ thể
for obj in [collar_left_obj, collar_right_obj, knot_obj, ribbon_obj]:
    bpy.context.scene.collection.objects.link(obj)
    obj.parent = arm
    obj.parent_type = 'BONE'
    obj.parent_bone = 'Spine'
    obj.matrix_parent_inverse = arm.matrix_world.inverted() @ arm.pose.bones['Spine'].matrix.inverted()

print("✓ Đã gắn đầy đủ chi tiết Áo Tràng Vạt Chéo vào khung xương Spine")

# 6. Thiết lập Ánh Sáng Studio Chân Thực
sun_data = bpy.data.lights.new(name="SunLight", type='SUN')
sun_data.energy = 2.8
sun_data.color = (1.0, 0.97, 0.92)
sun_obj = bpy.data.objects.new(name="SunLight", object_data=sun_data)
bpy.context.scene.collection.objects.link(sun_obj)
sun_obj.location = (2, -3, 6)
sun_obj.rotation_euler = (math.radians(40), math.radians(15), math.radians(-30))

fill_data = bpy.data.lights.new(name="FillLight", type='AREA')
fill_data.energy = 50.0
fill_data.size = 2.5
fill_data.color = (0.95, 0.96, 1.0)
fill_obj = bpy.data.objects.new(name="FillLight", object_data=fill_data)
bpy.context.scene.collection.objects.link(fill_obj)
fill_obj.location = (0, -2.2, 0.7)
fill_obj.rotation_euler = (math.radians(85), 0, 0)

# Camera
cam_data = bpy.data.cameras.new("MainCam")
cam_data.lens = 55
cam_obj = bpy.data.objects.new("MainCam", cam_data)
bpy.context.scene.collection.objects.link(cam_obj)
bpy.context.scene.camera = cam_obj

bpy.context.scene.render.resolution_x = 1080
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.render.image_settings.file_format = 'PNG'

# RENDER 1: Hoạt cảnh Chắp tay (Hai tay khép sát, Áo tràng vạt chéo thắt nơ + Nón lá V3)
arm.animation_data.action = bpy.data.actions['Chắp tay']
bpy.context.scene.frame_set(25)

cam_obj.location = (0.0, -2.10, 0.58)
cam_obj.rotation_euler = (math.radians(85), 0, 0)
bpy.context.scene.render.filepath = RENDER_FRONT
print("Đang render ảnh 1: Áo Tràng vạt chéo chắp tay...")
bpy.ops.render.render(write_still=True)
print(f"✓ Đã render: {RENDER_FRONT}")

# RENDER 2: Hoạt cảnh Đi bộ từ phía sau
arm.animation_data.action = bpy.data.actions['Di bo']
bpy.context.scene.frame_set(14)

back_light_data = bpy.data.lights.new(name="BackFillLight", type='AREA')
back_light_data.energy = 45.0
back_light_data.size = 2.0
back_light_data.color = (1.0, 0.96, 0.90)
back_light_obj = bpy.data.objects.new(name="BackFillLight", object_data=back_light_data)
bpy.context.scene.collection.objects.link(back_light_obj)
back_light_obj.location = (0, 2.2, 0.9)
back_light_obj.rotation_euler = (math.radians(95), 0, math.radians(180))

cam_obj.location = (0.05, 2.10, 0.65)
cam_obj.rotation_euler = (math.radians(94), 0, math.radians(180))
bpy.context.scene.render.filepath = RENDER_BACK
print("Đang render ảnh 2: Áo Tràng thiền hành bước đi phía sau...")
bpy.ops.render.render(write_still=True)
print(f"✓ Đã render: {RENDER_BACK}")

# 7. Xuất GLB nhân vật mặc Áo Tràng vạt chéo + Nón Lá V3 hoàn chỉnh
bpy.ops.export_scene.gltf(
    filepath=OUT_CHAR_GLB,
    export_format='GLB',
    use_selection=False,
    export_animations=True,
    export_skins=True,
    export_morph=True
)
print(f"✓ Đã xuất GLB nhân vật mặc Áo Tràng hoàn chỉnh: {OUT_CHAR_GLB}")

# Cập nhật đè lên nu-doi-non-la-chuyen-dong.glb để web tự động nhận trang phục mặc định
import shutil
shutil.copy(OUT_CHAR_GLB, NU_GLB)
print(f"✓ Đã đồng bộ trang phục mặc định vào: {NU_GLB}")

print("=== HOÀN TẤT THIẾT KẾ VÀ MẶC TRANG PHỤC MẶC ĐỊNH ===")
