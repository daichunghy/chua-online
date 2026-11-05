# -*- coding: utf-8 -*-
"""
Gắn Nón Lá Thêu Sen V3 (cao cấp, vân sen PBR) vào mô hình Phật tử Nữ đã sửa sạch màu
và kiểm tra hoạt cảnh Chắp tay (hai bàn tay khép sát vào nhau 1.9cm).
Xuất ảnh render studio và xuất GLB chuyển động hoàn chỉnh.
"""

import bpy
import math
import os

BASE_DIR = "/Users/macos/Desktop/Chùa online"
NU_GLB = os.path.join(BASE_DIR, "Thiết kế giao diện", "Nhân vật 3D", "Chuyển động", "nu-chuyen-dong.glb")
HAT_GLB = os.path.join(BASE_DIR, "Thiết kế giao diện", "Vật phẩm 3D", "models", "non_la_theu_sen_v3.glb")
OUT_CHAR_GLB = os.path.join(BASE_DIR, "Thiết kế giao diện", "Nhân vật 3D", "Chuyển động", "nu-doi-non-la-chuyen-dong.glb")

RENDER_FRONT = os.path.join(BASE_DIR, "Thiết kế giao diện", "Nhân vật 3D", "Chuyển động", "render-nu-v3-chap-tay.png")
RENDER_BACK = os.path.join(BASE_DIR, "Thiết kế giao diện", "Nhân vật 3D", "Chuyển động", "render-nu-v3-di-bo-back.png")
RENDER_HAT = os.path.join(BASE_DIR, "Thiết kế giao diện", "Vật phẩm 3D", "render-non-la-v3-studio.png")

# 1. Reset scene
bpy.ops.wm.read_factory_settings(use_empty=True)

# 2. Import nhân vật nữ đã sửa sạch màu & hai tay chắp sát
bpy.ops.import_scene.gltf(filepath=NU_GLB)
arm = bpy.data.objects.get("world")
mesh_body = bpy.data.objects.get("geometry_0")

# 3. Import Nón Lá V3
bpy.ops.import_scene.gltf(filepath=HAT_GLB)
hat_obj = None
for o in bpy.context.selected_objects:
    if "Non_La" in o.name:
        hat_obj = o
        break

if not hat_obj:
    # Lấy object đầu tiên
    hat_obj = [o for o in bpy.context.selected_objects if o != arm and o != mesh_body][0]

# Gắn Nón Lá vào xương Head
# Nón lá V3 đặt chụp chuẩn vòm đầu và búi tóc
hat_obj.location = (0.0, -0.015, 0.48)
hat_obj.rotation_euler = (math.radians(4.0), 0, 0)
hat_obj.scale = (1.15, 1.15, 1.15)

hat_obj.parent = arm
hat_obj.parent_type = 'BONE'
hat_obj.parent_bone = 'Head'

hat_obj.matrix_parent_inverse = arm.matrix_world.inverted() @ arm.pose.bones['Head'].matrix.inverted()
hat_obj.location = (0.0, -0.015, 0.48)
hat_obj.rotation_euler = (math.radians(4.0), 0, 0)
hat_obj.scale = (1.15, 1.15, 1.15)

print("✓ Đã gắn Nón Lá V3 khớp xương Head")

# 4. Thiết lập Đèn Studio & Mặt Trời
sun_data = bpy.data.lights.new(name="SunLight", type='SUN')
sun_data.energy = 2.8
sun_data.color = (1.0, 0.97, 0.92)
sun_obj = bpy.data.objects.new(name="SunLight", object_data=sun_data)
bpy.context.scene.collection.objects.link(sun_obj)
sun_obj.location = (2, -3, 6)
sun_obj.rotation_euler = (math.radians(40), math.radians(15), math.radians(-30))

# Fill light phía trước để sáng mặt & áo lam
fill_data = bpy.data.lights.new(name="FillLight", type='AREA')
fill_data.energy = 45.0
fill_data.size = 2.0
fill_data.color = (0.92, 0.95, 1.0)
fill_obj = bpy.data.objects.new(name="FillLight", object_data=fill_data)
bpy.context.scene.collection.objects.link(fill_obj)
fill_obj.location = (0, -2.2, 0.8)
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

# RENDER 1: Hoạt cảnh Chắp tay (Hai tay khép sát vào nhau, chính diện áo lam + nón lá)
arm.animation_data.action = bpy.data.actions['Chắp tay']
bpy.context.scene.frame_set(25) # Giữ tư thế chắp tay búp sen

cam_obj.location = (0.0, -2.15, 0.62)
cam_obj.rotation_euler = (math.radians(85), 0, 0)
bpy.context.scene.render.filepath = RENDER_FRONT
print("Đang render ảnh 1: Chính diện chắp tay khép sát...")
bpy.ops.render.render(write_still=True)
print(f"✓ Đã render: {RENDER_FRONT}")

# RENDER 2: Hoạt cảnh Đi bộ từ phía sau (Third-person như ảnh concept Chùa Vĩnh Tràng)
arm.animation_data.action = bpy.data.actions['Di bo']
bpy.context.scene.frame_set(14) # Bước chân thiền hành

# Đèn chiếu sáng phía sau nhân vật
back_light_data = bpy.data.lights.new(name="BackFillLight", type='AREA')
back_light_data.energy = 40.0
back_light_data.size = 2.0
back_light_data.color = (1.0, 0.96, 0.90)
back_light_obj = bpy.data.objects.new(name="BackFillLight", object_data=back_light_data)
bpy.context.scene.collection.objects.link(back_light_obj)
back_light_obj.location = (0, 2.2, 0.9)
back_light_obj.rotation_euler = (math.radians(95), 0, math.radians(180))

cam_obj.location = (0.05, 2.10, 0.65)
cam_obj.rotation_euler = (math.radians(94), 0, math.radians(180))
bpy.context.scene.render.filepath = RENDER_BACK
print("Đang render ảnh 2: Phía sau bước đi...")
bpy.ops.render.render(write_still=True)
print(f"✓ Đã render: {RENDER_BACK}")

# Xuất GLB mới tích hợp nón lá V3 & chuyển động
bpy.ops.export_scene.gltf(
    filepath=OUT_CHAR_GLB,
    export_format='GLB',
    use_selection=False,
    export_animations=True,
    export_skins=True,
    export_morph=True
)
print(f"✓ Đã xuất GLB chuyển động hoàn chỉnh: {OUT_CHAR_GLB}")
