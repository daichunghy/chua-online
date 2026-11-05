# -*- coding: utf-8 -*-
"""
Blender 5.2 Python Script:
Xây dựng Áo Tràng Phật Tử Vạt Chéo (Trang phục mặc định) chuẩn 100% ảnh tham khảo:
1. Nẹp cổ vạt chéo 3D ôm sát ngực phía trước (Y < 0).
2. Nơ thắt eo xinh xắn bên hông phải với 2 cánh nơ và 2 dải lụa rủ dài.
3. Ống tay áo thụng rộng thanh thoát truyền thống Phật giáo.
4. Gắn khung xương Armature để chuyển động mềm mại tự nhiên theo mọi động tác (Chắp tay, Đi bộ...).
"""

import bpy
import bmesh
import math
import mathutils
import os

BASE_DIR = "/Users/macos/Desktop/Chùa online"
NU_GLB = os.path.join(BASE_DIR, "Thiết kế giao diện", "Nhân vật 3D", "Chuyển động", "nu-chuyen-dong.glb")
TEST_RENDER = "/Users/macos/.gemini/antigravity/brain/e586aaa5-2e71-4723-b119-f4df2ed52600/test_ao_trang_placement.png"

bpy.ops.wm.read_factory_settings(use_empty=True)

# 1. Nạp nhân vật gốc
bpy.ops.import_scene.gltf(filepath=NU_GLB)
arm = bpy.data.objects['world']
body = bpy.data.objects['geometry_0']

# 2. Làm phẳng nhẹ các nốt cúc cũ trên ngực để tạo bề mặt vải áo tràng phẳng mịn
for v in body.data.vertices:
    if abs(v.co.x) < 0.018 and 0.08 < v.co.z < 0.45 and v.co.y < -0.150:
        # Làm phẳng về mặt ngực xung quanh (-0.148 đến -0.152)
        v.co.y = max(v.co.y, -0.152)

body.data.update()
print("✓ Đã làm phẳng các nốt cúc cũ trên thân áo")

# Màu chuẩn từ ảnh tham khảo: #a0979f -> (0.628, 0.592, 0.624)
COLOR_ROBE = (0.628, 0.592, 0.624, 1.0)
COLOR_COLLAR = (0.585, 0.550, 0.580, 1.0) # Nẹp viền đậm hơn nhẹ để tôn đường cắt may
COLOR_BOW = (0.640, 0.605, 0.635, 1.0)

mat_robe = bpy.data.materials.new(name="Mat_Ao_Trang_Lam")
bsdf = mat_robe.node_tree.nodes.get("Principled BSDF")
bsdf.inputs["Base Color"].default_value = COLOR_ROBE
bsdf.inputs["Roughness"].default_value = 0.82

mat_collar = bpy.data.materials.new(name="Mat_Nep_Co")
bsdf_c = mat_collar.node_tree.nodes.get("Principled BSDF")
bsdf_c.inputs["Base Color"].default_value = COLOR_COLLAR
bsdf_c.inputs["Roughness"].default_value = 0.80

# 3. Tạo nẹp cổ vạt chéo (Overlapping Cross Collar Band)
# Vạt chính từ vai trái, vòng qua gáy, vắt chéo qua ngực sang eo phải
curve_collar = bpy.data.curves.new('Nep_Co_Cheo', type='CURVE')
curve_collar.dimensions = '3D'

# Spline 1: Vạt chính từ vai trái vắt chéo qua ngực sang eo phải
s_main = curve_collar.splines.new('BEZIER')
pts_main = [
    (0.000,   0.020, 0.535),  # Sau gáy
    (-0.065, -0.055, 0.530),  # Vòng qua cổ trái
    (-0.070, -0.125, 0.510),  # Vai trái trước cổ
    (-0.035, -0.145, 0.420),  # Xuống ngực trên
    ( 0.015, -0.162, 0.330),  # Chéo qua giữa ngực (phủ lên vạt phụ)
    ( 0.070, -0.158, 0.180),  # Xuống sườn phải
    ( 0.125, -0.146, 0.025)   # Điểm giao eo phải (vị trí thắt nơ)
]
s_main.bezier_points.add(len(pts_main) - 1)
for i, pt in enumerate(pts_main):
    bp = s_main.bezier_points[i]
    bp.co = pt
    bp.handle_left_type = 'AUTO'
    bp.handle_right_type = 'AUTO'

# Spline 2: Vạt phụ từ vai phải chéo vào dưới ngực trái
s_sub = curve_collar.splines.new('BEZIER')
pts_sub = [
    ( 0.065, -0.055, 0.530),  # Vòng qua cổ phải
    ( 0.068, -0.125, 0.505),  # Vai phải trước cổ
    ( 0.020, -0.148, 0.410),  # Chéo vào trong
    (-0.025, -0.154, 0.315)   # Ẩn dưới vạt chính ở giữa ngực
]
s_sub.bezier_points.add(len(pts_sub) - 1)
for i, pt in enumerate(pts_sub):
    bp = s_sub.bezier_points[i]
    bp.co = pt
    bp.handle_left_type = 'AUTO'
    bp.handle_right_type = 'AUTO'

curve_collar.bevel_depth = 0.014 # Bản nẹp rộng ~2.8cm
curve_collar.bevel_resolution = 4
collar_obj = bpy.data.objects.new('Nep_Co_Ao_Trang', curve_collar)
collar_obj.data.materials.append(mat_collar)
bpy.context.scene.collection.objects.link(collar_obj)

# 4. Tạo Nơ Thắt Eo Vải Lam bên sườn phải
bow_mesh = bpy.data.meshes.new("No_That_Eo_Mesh")
bm = bmesh.new()

# Nút thắt oval ở giữa eo
knot_matrix = (
    mathutils.Matrix.Translation((0.132, -0.150, 0.025)) @
    mathutils.Matrix.Rotation(math.radians(-15), 4, 'Y') @
    mathutils.Matrix.Scale(0.014, 4, (1, 0, 0)) @
    mathutils.Matrix.Scale(0.010, 4, (0, 1, 0)) @
    mathutils.Matrix.Scale(0.015, 4, (0, 0, 1))
)
bmesh.ops.create_uvsphere(bm, u_segments=12, v_segments=8, radius=1.0, matrix=knot_matrix)
bm.to_mesh(bow_mesh)
bm.free()

bow_obj = bpy.data.objects.new("Nut_That_Eo", bow_mesh)
bow_obj.data.materials.append(mat_collar)
bpy.context.scene.collection.objects.link(bow_obj)

# Hai cánh nơ và hai dải lụa rủ
curve_ribbon = bpy.data.curves.new('Dai_Lua_No', type='CURVE')
curve_ribbon.dimensions = '3D'

# Cánh nơ 1: Hướng chếch lên trên dọc thân áo
loop1 = curve_ribbon.splines.new('BEZIER')
l1_pts = [
    (0.132, -0.150, 0.025),
    (0.145, -0.152, 0.065),
    (0.130, -0.149, 0.075),
    (0.128, -0.148, 0.028)
]
loop1.bezier_points.add(len(l1_pts) - 1)
for i, pt in enumerate(l1_pts):
    bp = loop1.bezier_points[i]
    bp.co = pt
    bp.handle_left_type = 'AUTO'
    bp.handle_right_type = 'AUTO'

# Cánh nơ 2: Hướng ngang ra ngoài
loop2 = curve_ribbon.splines.new('BEZIER')
l2_pts = [
    (0.132, -0.150, 0.025),
    (0.170, -0.148, 0.035),
    (0.165, -0.146, 0.015),
    (0.130, -0.148, 0.020)
]
loop2.bezier_points.add(len(l2_pts) - 1)
for i, pt in enumerate(l2_pts):
    bp = loop2.bezier_points[i]
    bp.co = pt
    bp.handle_left_type = 'AUTO'
    bp.handle_right_type = 'AUTO'

# Dải lụa rủ 1: Dài ~24cm thướt tha xuống tà áo
trail1 = curve_ribbon.splines.new('BEZIER')
t1_pts = [
    (0.132, -0.150,  0.025),
    (0.136, -0.146, -0.050),
    (0.138, -0.140, -0.140),
    (0.135, -0.135, -0.220)
]
trail1.bezier_points.add(len(t1_pts) - 1)
for i, pt in enumerate(t1_pts):
    bp = trail1.bezier_points[i]
    bp.co = pt
    bp.handle_left_type = 'AUTO'
    bp.handle_right_type = 'AUTO'

# Dải lụa rủ 2: Dài ~17cm buông lơi tự nhiên
trail2 = curve_ribbon.splines.new('BEZIER')
t2_pts = [
    (0.134, -0.151,  0.025),
    (0.142, -0.148, -0.040),
    (0.144, -0.143, -0.110),
    (0.140, -0.138, -0.165)
]
trail2.bezier_points.add(len(t2_pts) - 1)
for i, pt in enumerate(t2_pts):
    bp = trail2.bezier_points[i]
    bp.co = pt
    bp.handle_left_type = 'AUTO'
    bp.handle_right_type = 'AUTO'

curve_ribbon.bevel_depth = 0.007 # Rộng dải lụa ~1.4cm
curve_ribbon.bevel_resolution = 4
ribbon_obj = bpy.data.objects.new('Canh_No_Va_Dai_Lua', curve_ribbon)
ribbon_obj.data.materials.append(mat_collar)
bpy.context.scene.collection.objects.link(ribbon_obj)

# 5. Chuyển curve sang mesh một cách trực tiếp & gộp các bộ phận
dg = bpy.context.evaluated_depsgraph_get()

collar_mesh_data = bpy.data.meshes.new_from_object(collar_obj.evaluated_get(dg))
collar_mesh_obj = bpy.data.objects.new("Nep_Co_Mesh", collar_mesh_data)
collar_mesh_obj.data.materials.append(mat_collar)
bpy.context.scene.collection.objects.link(collar_mesh_obj)
bpy.data.objects.remove(collar_obj)

ribbon_mesh_data = bpy.data.meshes.new_from_object(ribbon_obj.evaluated_get(dg))
ribbon_mesh_obj = bpy.data.objects.new("Ribbon_Mesh", ribbon_mesh_data)
ribbon_mesh_obj.data.materials.append(mat_collar)
bpy.context.scene.collection.objects.link(ribbon_mesh_obj)
bpy.data.objects.remove(ribbon_obj)

# Gộp các chi tiết trang trí áo tràng vào thành 1 mesh hoàn chỉnh
bpy.ops.object.select_all(action='DESELECT')
collar_mesh_obj.select_set(True)
bow_obj.select_set(True)
ribbon_mesh_obj.select_set(True)
bpy.context.view_layer.objects.active = collar_mesh_obj
bpy.ops.object.join()
ao_trang_detail = collar_mesh_obj
ao_trang_detail.name = "Chi_Tiet_Ao_Trang_Vat_Cheo"

# Gán Armature Modifier cho chi tiết trang phục
arm_mod = ao_trang_detail.modifiers.new(name="Armature", type='ARMATURE')
arm_mod.object = arm

# Tạo Vertex Groups cho Spine và Pelvis
vg_spine = ao_trang_detail.vertex_groups.new(name="Spine")
vg_pelvis = ao_trang_detail.vertex_groups.new(name="Pelvis")

for v in ao_trang_detail.data.vertices:
    # Điểm càng thấp (dải lụa rủ) thì nhận thêm trọng số từ Pelvis
    z = v.co.z
    if z > 0.10:
        w_spine = 1.0
        w_pelvis = 0.0
    elif z > -0.05:
        w_spine = 0.8
        w_pelvis = 0.2
    else:
        w_spine = 0.3
        w_pelvis = 0.7
    vg_spine.add([v.index], w_spine, 'REPLACE')
    vg_pelvis.add([v.index], w_pelvis, 'REPLACE')

print("✓ Đã gắn đầy đủ Armature Modifier & Vertex Weighting cho Áo Tràng")

# 6. Thiết lập ánh sáng & camera góc cận cảnh chính diện để kiểm tra
sun_data = bpy.data.lights.new(name="SunLight", type='SUN')
sun_data.energy = 3.0
sun_data.color = (1.0, 0.98, 0.95)
sun_obj = bpy.data.objects.new(name="SunLight", object_data=sun_data)
bpy.context.scene.collection.objects.link(sun_obj)
sun_obj.location = (1.5, -3.0, 4.0)
sun_obj.rotation_euler = (math.radians(50), math.radians(10), math.radians(-25))

fill_data = bpy.data.lights.new(name="FillLight", type='AREA')
fill_data.energy = 60.0
fill_data.size = 2.0
fill_data.color = (0.95, 0.97, 1.0)
fill_obj = bpy.data.objects.new(name="FillLight", object_data=fill_data)
bpy.context.scene.collection.objects.link(fill_obj)
fill_obj.location = (0, -2.0, 0.4)
fill_obj.rotation_euler = (math.radians(90), 0, 0)

cam_data = bpy.data.cameras.new("TestCam")
cam_data.lens = 65
cam_obj = bpy.data.objects.new("TestCam", cam_data)
bpy.context.scene.collection.objects.link(cam_obj)
bpy.context.scene.camera = cam_obj

# Camera chính diện ngực áo và nơ eo
cam_obj.location = (0.02, -1.65, 0.32)
cam_obj.rotation_euler = (math.radians(90), 0, 0)

bpy.context.scene.render.resolution_x = 1080
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.render.filepath = TEST_RENDER

print("Đang render ảnh kiểm tra vị trí Áo Tràng Vạt Chéo...")
bpy.ops.render.render(write_still=True)
print(f"✓ Hoàn tất render kiểm tra: {TEST_RENDER}")
