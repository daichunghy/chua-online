# -*- coding: utf-8 -*-
"""
Blender 5.2 Python Script:
Kiểm tra thiết kế Nẹp Cổ Vạt Chéo phẳng dạng dải vải (Flat Tailored Lapel Strip) & Nơ Eo 3D.
"""

import bpy
import bmesh
import math
import mathutils
import os

TEST_RENDER = "/Users/macos/.gemini/antigravity/brain/e586aaa5-2e71-4723-b119-f4df2ed52600/test_flat_lapel_strip.png"
NU_GLB = "/Users/macos/Desktop/Chùa online/Thiết kế giao diện/Nhân vật 3D/Chuyển động/nu-chuyen-dong.glb"

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=NU_GLB)
arm = bpy.data.objects['world']
body = bpy.data.objects['geometry_0']

# 1. Làm phẳng hoàn toàn các nốt cúc cũ trên ngực áo
for v in body.data.vertices:
    if abs(v.co.x) < 0.022 and 0.05 < v.co.z < 0.46 and v.co.y < -0.145:
        v.co.y = -0.148

body.data.update()

# 2. Màu sắc chuẩn từ ảnh tham khảo: #a0979f -> (0.628, 0.592, 0.624)
COLOR_ROBE = (0.628, 0.592, 0.624, 1.0)
COLOR_COLLAR = (0.585, 0.548, 0.580, 1.0)

mat_robe = bpy.data.materials.new(name="Mat_Ao_Trang_Lam")
bsdf = mat_robe.node_tree.nodes.get("Principled BSDF")
bsdf.inputs["Base Color"].default_value = COLOR_ROBE
bsdf.inputs["Roughness"].default_value = 0.82

mat_collar = bpy.data.materials.new(name="Mat_Nep_Co")
bsdf_c = mat_collar.node_tree.nodes.get("Principled BSDF")
bsdf_c.inputs["Base Color"].default_value = COLOR_COLLAR
bsdf_c.inputs["Roughness"].default_value = 0.78

def create_tailored_strip(pts, widths, normals, name, mat):
    """Tạo dải nẹp cổ vải phẳng ôm sát ngực với bề rộng và pháp tuyến chính xác."""
    mesh = bpy.data.meshes.new(name + "_Mesh")
    bm = bmesh.new()
    
    verts_left = []
    verts_right = []
    
    for i in range(len(pts)):
        p = mathutils.Vector(pts[i])
        n = mathutils.Vector(normals[i]).normalized()
        w = widths[i]
        
        # Vector tiếp tuyến đường chạy
        if i == 0:
            t = (mathutils.Vector(pts[1]) - p).normalized()
        elif i == len(pts) - 1:
            t = (p - mathutils.Vector(pts[i-1])).normalized()
        else:
            t = (mathutils.Vector(pts[i+1]) - mathutils.Vector(pts[i-1])).normalized()
            
        # Vector vuông góc nằm ngang trên mặt vải: b = t x n
        b = t.cross(n).normalized()
        
        vl = bm.verts.new(p - b * (w * 0.5) + n * 0.002)
        vr = bm.verts.new(p + b * (w * 0.5) + n * 0.002)
        verts_left.append(vl)
        verts_right.append(vr)
        
    bm.verts.ensure_lookup_table()
    for i in range(len(pts) - 1):
        bm.faces.new([verts_left[i], verts_right[i], verts_right[i+1], verts_left[i+1]])
        
    # Tạo độ dày vải 1.5mm
    bmesh.ops.solidify(bm, geom=bm.faces[:], thickness=0.002)
    bm.to_mesh(mesh)
    bm.free()
    
    obj = bpy.data.objects.new(name, mesh)
    obj.data.materials.append(mat)
    bpy.context.scene.collection.objects.link(obj)
    return obj

# 3. Tạo Vạt Chính (Từ gáy vòng qua cổ trái, vắt chéo qua ngực phải xuống eo)
# Chi tiết tọa độ bám sát bề mặt giải phẫu cơ thể
pts_main = [
    ( 0.000,  0.020, 0.585), # Gáy sau cổ
    (-0.040, -0.020, 0.580), # Cổ trái bên
    (-0.055, -0.075, 0.555), # Chân cổ trái
    (-0.045, -0.115, 0.515), # Xương quai xanh trái
    (-0.025, -0.142, 0.440), # Bắt đầu chéo qua ngực trên
    ( 0.010, -0.160, 0.350), # Giữa ngực (giao điểm chữ Y)
    ( 0.050, -0.162, 0.240), # Xuống ngực dưới mạn phải
    ( 0.090, -0.158, 0.130), # Mạn sườn phải
    ( 0.130, -0.146, 0.025)  # Eo phải (vị trí thắt nơ)
]
normals_main = [
    ( 0.0,  1.0, 0.0),
    (-0.8,  0.6, 0.0),
    (-0.7, -0.7, 0.2),
    (-0.4, -0.9, 0.2),
    (-0.2, -0.95, 0.2),
    ( 0.0, -1.0, 0.1),
    ( 0.3, -0.95, 0.1),
    ( 0.6, -0.8, 0.1),
    ( 0.8, -0.6, 0.0)
]
# Nẹp cổ to bản 2.8cm rất trang nghiêm
widths_main = [0.026] * len(pts_main)
obj_main_collar = create_tailored_strip(pts_main, widths_main, normals_main, "Nep_Co_Vat_Chinh", mat_collar)

# 4. Tạo Vạt Phụ (Từ cổ phải chéo vào dưới ngực trái)
pts_sub = [
    ( 0.040, -0.020, 0.580), # Cổ phải bên
    ( 0.055, -0.075, 0.555), # Chân cổ phải
    ( 0.045, -0.115, 0.515), # Xương quai xanh phải
    ( 0.022, -0.140, 0.435), # Chéo vào trong
    (-0.010, -0.156, 0.345), # Giao điểm luồn dưới vạt chính
    (-0.040, -0.154, 0.260)  # Luồn vào trong thân áo
]
normals_sub = [
    ( 0.8,  0.6, 0.0),
    ( 0.7, -0.7, 0.2),
    ( 0.4, -0.9, 0.2),
    ( 0.2, -0.95, 0.2),
    ( 0.0, -1.0, 0.1),
    (-0.3, -0.95, 0.1)
]
widths_sub = [0.026] * len(pts_sub)
obj_sub_collar = create_tailored_strip(pts_sub, widths_sub, normals_sub, "Nep_Co_Vat_Phu", mat_collar)

# 5. Tạo Nơ Thắt Eo Vải Lam Tinh Tế (Waist Ribbon Bow Knot)
# Nút thắt hình thoi/oval tinh xảo
knot_mesh = bpy.data.meshes.new("Nut_That_Eo_Mesh")
bm = bmesh.new()
knot_mat = (
    mathutils.Matrix.Translation((0.134, -0.148, 0.025)) @
    mathutils.Matrix.Rotation(math.radians(-20), 4, 'Y') @
    mathutils.Matrix.Rotation(math.radians(10), 4, 'Z') @
    mathutils.Matrix.Scale(0.014, 4, (1, 0, 0)) @
    mathutils.Matrix.Scale(0.010, 4, (0, 1, 0)) @
    mathutils.Matrix.Scale(0.016, 4, (0, 0, 1))
)
bmesh.ops.create_uvsphere(bm, u_segments=16, v_segments=10, radius=1.0, matrix=knot_mat)
bm.to_mesh(knot_mesh)
bm.free()
obj_knot = bpy.data.objects.new("Nut_That_Eo", knot_mesh)
obj_knot.data.materials.append(mat_collar)
bpy.context.scene.collection.objects.link(obj_knot)

# Cánh nơ 1: Cánh nơ bướm hướng lên trên
pts_loop1 = [
    (0.134, -0.148, 0.025),
    (0.148, -0.150, 0.055),
    (0.140, -0.148, 0.075),
    (0.130, -0.146, 0.065),
    (0.132, -0.147, 0.030)
]
normals_l1 = [(0.7, -0.7, 0.2)] * len(pts_loop1)
widths_l1 = [0.018] * len(pts_loop1)
obj_l1 = create_tailored_strip(pts_loop1, widths_l1, normals_l1, "Canh_No_1", mat_collar)

# Cánh nơ 2: Cánh nơ bướm hướng ra ngoài mạn sườn
pts_loop2 = [
    (0.134, -0.148, 0.025),
    (0.165, -0.147, 0.035),
    (0.170, -0.144, 0.015),
    (0.155, -0.144, 0.005),
    (0.134, -0.146, 0.020)
]
normals_l2 = [(0.8, -0.6, 0.1)] * len(pts_loop2)
widths_l2 = [0.018] * len(pts_loop2)
obj_l2 = create_tailored_strip(pts_loop2, widths_l2, normals_l2, "Canh_No_2", mat_collar)

# Dải lụa rủ dài 1 (~24cm)
pts_trail1 = [
    (0.134, -0.148,  0.025),
    (0.138, -0.145, -0.045),
    (0.140, -0.138, -0.125),
    (0.136, -0.130, -0.210)
]
normals_t1 = [(0.8, -0.6, 0.0)] * len(pts_trail1)
widths_t1 = [0.016] * len(pts_trail1)
obj_t1 = create_tailored_strip(pts_trail1, widths_t1, normals_t1, "Dai_Lua_1", mat_collar)

# Dải lụa rủ ngắn 2 (~18cm)
pts_trail2 = [
    (0.135, -0.149,  0.025),
    (0.144, -0.146, -0.035),
    (0.146, -0.140, -0.105),
    (0.142, -0.134, -0.160)
]
normals_t2 = [(0.8, -0.6, 0.0)] * len(pts_trail2)
widths_t2 = [0.016] * len(pts_trail2)
obj_t2 = create_tailored_strip(pts_trail2, widths_t2, normals_t2, "Dai_Lua_2", mat_collar)

# Gộp tất cả chi tiết trang trí áo tràng
bpy.ops.object.select_all(action='DESELECT')
for o in [obj_main_collar, obj_sub_collar, obj_knot, obj_l1, obj_l2, obj_t1, obj_t2]:
    o.select_set(True)
bpy.context.view_layer.objects.active = obj_main_collar
bpy.ops.object.join()
ao_trang_detail = obj_main_collar
ao_trang_detail.name = "Chi_Tiet_Ao_Trang_Vat_Cheo"

# Gán Armature Modifier & Vertex Weighting
arm_mod = ao_trang_detail.modifiers.new(name="Armature", type='ARMATURE')
arm_mod.object = arm

vg_spine = ao_trang_detail.vertex_groups.new(name="Spine")
vg_pelvis = ao_trang_detail.vertex_groups.new(name="Pelvis")

for v in ao_trang_detail.data.vertices:
    z = v.co.z
    if z > 0.08:
        w_s = 1.0; w_p = 0.0
    elif z > -0.05:
        w_s = 0.8; w_p = 0.2
    else:
        w_s = 0.3; w_p = 0.7
    vg_spine.add([v.index], w_s, 'REPLACE')
    vg_pelvis.add([v.index], w_p, 'REPLACE')

print("✓ Đã dựng xong Nẹp Cổ Vạt Chéo bản phẳng và Nơ Thắt Eo")

# 6. Thiết lập Ánh Sáng Studio & Camera góc cận cảnh chính diện
sun_data = bpy.data.lights.new(name="SunLight", type='SUN')
sun_data.energy = 3.2
sun_data.color = (1.0, 0.98, 0.95)
sun_obj = bpy.data.objects.new(name="SunLight", object_data=sun_data)
bpy.context.scene.collection.objects.link(sun_obj)
sun_obj.location = (1.5, -3.0, 4.0)
sun_obj.rotation_euler = (math.radians(50), math.radians(10), math.radians(-25))

fill_data = bpy.data.lights.new(name="FillLight", type='AREA')
fill_data.energy = 65.0
fill_data.size = 2.0
fill_data.color = (0.95, 0.97, 1.0)
fill_obj = bpy.data.objects.new(name="FillLight", object_data=fill_data)
bpy.context.scene.collection.objects.link(fill_obj)
fill_obj.location = (0, -2.0, 0.35)
fill_obj.rotation_euler = (math.radians(90), 0, 0)

cam_data = bpy.data.cameras.new("TestCam")
cam_data.lens = 65
cam_obj = bpy.data.objects.new("TestCam", cam_data)
bpy.context.scene.collection.objects.link(cam_obj)
bpy.context.scene.camera = cam_obj

cam_obj.location = (0.01, -1.65, 0.32)
cam_obj.rotation_euler = (math.radians(90), 0, 0)

bpy.context.scene.render.resolution_x = 1080
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.render.filepath = TEST_RENDER

print("Đang render ảnh kiểm tra dải nẹp phẳng...")
bpy.ops.render.render(write_still=True)
print(f"✓ Hoàn tất render kiểm tra: {TEST_RENDER}")
