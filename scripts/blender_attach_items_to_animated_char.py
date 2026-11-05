# -*- coding: utf-8 -*-
"""
Gắn vật phẩm 3D (Nón Lá Thêu Sen, Khăn Rằn, Túi Vải) trực tiếp vào khung xương (Armature)
của nhân vật 3D chuyển động thật (nu-chuyen-dong.glb, nam-chuyen-dong.glb, tre-em-chuyen-dong.glb).
Xuất tệp GLB có chuyển động hoàn chỉnh và render ảnh góc nhìn phía sau (giống concept ảnh Chùa Vĩnh Tràng).
"""

import bpy
import math
import os

BASE_DIR = "/Users/macos/Desktop/Chùa online"
NU_GLB = os.path.join(BASE_DIR, "Thiết kế giao diện", "Nhân vật 3D", "Chuyển động", "nu-chuyen-dong.glb")
HAT_OBJ = os.path.join(BASE_DIR, "Thiết kế giao diện", "Vật phẩm 3D", "models", "non_la_theu_sen_v2.obj")
OUTPUT_GLB = os.path.join(BASE_DIR, "Thiết kế giao diện", "Nhân vật 3D", "Chuyển động", "nu-doi-non-la-chuyen-dong.glb")
OUTPUT_RENDER = os.path.join(BASE_DIR, "Thiết kế giao diện", "Nhân vật 3D", "Chuyển động", "render-nu-that-doi-non-chuyen-dong.png")
OUTPUT_BLEND = os.path.join(BASE_DIR, "Thiết kế giao diện", "Nhân vật 3D", "nhan-vat-that-chuyen-dong-master.blend")

# 1. Reset scene
bpy.ops.wm.read_factory_settings(use_empty=True)

# 2. Import nhân vật nữ chuyển động thật
bpy.ops.import_scene.gltf(filepath=NU_GLB)

arm = bpy.data.objects.get("world")
mesh = bpy.data.objects.get("geometry_0")

if not arm or not mesh:
    raise RuntimeError("Không tìm thấy armature hoặc mesh nhân vật thật!")

print(f"✓ Đã nạp nhân vật nữ chuyển động thật: {mesh.name}, Armature: {arm.name}")

# 3. Import Nón Lá Thêu Sen V2
bpy.ops.wm.obj_import(filepath=HAT_OBJ)
hat = bpy.context.selected_objects[0]
hat.name = "Non_La_Theu_Sen"

# Gán vị trí nón lá khớp đỉnh đầu nhân vật nữ thật
# non_la_theu_sen_v2 có trục nón theo Y, cần xoay 90 độ quanh X để đỉnh nón hướng lên (+Z)
hat.rotation_euler = (math.radians(90), 0, 0)
# Tọa độ vành nón hạ vừa vặn chụp trên đỉnh đầu và búi tóc
hat.location = (0.0, 0.035, 0.49)
hat.rotation_euler = (math.radians(86), 0, 0) # Nghiêng nhẹ theo trục đầu
hat.scale = (0.95, 0.95, 0.95)

# Gán Nón Lá làm con của Xương 'Head' (Bone Parenting)
hat.parent = arm
hat.parent_type = 'BONE'
hat.parent_bone = 'Head'

# Giữ transform sau khi parent
hat.matrix_parent_inverse = arm.matrix_world.inverted() @ arm.pose.bones['Head'].matrix.inverted()
hat.location = (0.0, 0.035, 0.49)
hat.rotation_euler = (math.radians(86), 0, 0)
hat.scale = (0.95, 0.95, 0.95)

print(f"✓ Đã gắn Nón Lá thành công vào xương Head của {arm.name}")

# 4. Kích hoạt hoạt cảnh 'Di bo' (Walk cycle) tại khung hình chân thực
if arm.animation_data:
    action_walk = bpy.data.actions.get("Di bo")
    if action_walk:
        arm.animation_data.action = action_walk
        bpy.context.scene.frame_set(12) # Khung hình bước đi khoan thai
        print("✓ Đã kích hoạt hoạt ảnh 'Di bo' tại frame 12")

# 5. Thiết lập Camera góc nhìn thứ 3 phía sau (Third-person view như ảnh concept)
cam_data = bpy.data.cameras.new("ThirdPersonCam")
cam_data.lens = 50
cam_obj = bpy.data.objects.new("ThirdPersonCam", cam_data)
bpy.context.scene.collection.objects.link(cam_obj)
bpy.context.scene.camera = cam_obj

# Camera đặt phía sau lệch góc 15 độ, nhìn về hướng chùa
cam_obj.location = (0.15, -2.4, 1.15)
cam_obj.rotation_euler = (math.radians(82), 0, math.radians(4))

# 6. Thiết lập Ánh sáng ngoài trời (Mặt trời Chùa Vĩnh Tràng)
sun_data = bpy.data.lights.new(name="SunLight", type='SUN')
sun_data.energy = 3.5
sun_data.color = (1.0, 0.95, 0.88)
sun_obj = bpy.data.objects.new(name="SunLight", object_data=sun_data)
bpy.context.scene.collection.objects.link(sun_obj)
sun_obj.rotation_euler = (math.radians(45), math.radians(20), math.radians(-35))

# Đèn môi trường ấm
world = bpy.data.worlds.new("TempleWorld")
world.use_nodes = True
bg_node = world.node_tree.nodes.get("Background")
if bg_node:
    bg_node.inputs["Color"].default_value = (0.92, 0.89, 0.83, 1.0)
    bg_node.inputs["Strength"].default_value = 0.8
bpy.context.scene.world = world

# 7. Render ảnh: 1 ảnh chính diện và 1 ảnh phía sau (Third-person như ảnh concept Chùa Vĩnh Tràng)
OUTPUT_FRONT = os.path.join(BASE_DIR, "Thiết kế giao diện", "Nhân vật 3D", "Chuyển động", "render-nu-that-doi-non-front.png")
OUTPUT_BACK = os.path.join(BASE_DIR, "Thiết kế giao diện", "Nhân vật 3D", "Chuyển động", "render-nu-that-doi-non-back.png")

bpy.context.scene.render.resolution_x = 1280
bpy.context.scene.render.resolution_y = 800
bpy.context.scene.render.image_settings.file_format = 'PNG'

# Render ảnh chính diện
cam_obj.location = (0.15, -2.2, 0.95)
cam_obj.rotation_euler = (math.radians(85), 0, math.radians(4))
bpy.context.scene.render.filepath = OUTPUT_FRONT
print("Đang render ảnh chính diện...")
bpy.ops.render.render(write_still=True)

# Render ảnh phía sau (Third person walking toward temple)
cam_obj.location = (0.05, 2.0, 0.65)
cam_obj.rotation_euler = (math.radians(90), 0, math.radians(180))
bpy.context.scene.render.filepath = OUTPUT_BACK
print("Đang render ảnh phía sau (Third-person)...")
bpy.ops.render.render(write_still=True)

# 8. Lưu Master Blend
bpy.ops.wm.save_as_mainfile(filepath=OUTPUT_BLEND)
print(f"✓ Đã lưu Master Blend: {OUTPUT_BLEND}")

# 9. Xuất GLB hoàn chỉnh (Bao gồm nhân vật thật + nón lá gắn xương + toàn bộ animations)
try:
    bpy.ops.export_scene.gltf(
        filepath=OUTPUT_GLB,
        export_format='GLB',
        use_selection=False,
        export_animations=True,
        export_skins=True,
        export_morph=True
    )
    print(f"✓ Đã xuất GLB chuyển động tích hợp nón lá: {OUTPUT_GLB}")
except Exception as e:
    print("Export GLTF lỗi:", e)

print("=== HOÀN TẤT GẮN VẬT PHẨM LÊN NHÂN VẬT THẬT ===")
