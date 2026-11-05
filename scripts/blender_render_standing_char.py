# -*- coding: utf-8 -*-
"""
Render nhân vật Nữ mặc Áo Tràng Vạt Chéo & Đội Nón Lá Sen V3 góc 3/4 toàn thân (Đứng Chánh Niệm).
"""
import bpy
import math

BASE_DIR = "/Users/macos/Desktop/Chùa online"
NU_GLB = f"{BASE_DIR}/Thiết kế giao diện/Nhân vật 3D/Chuyển động/nu-mac-ao-trang-doi-non.glb"
OUT_IMG = f"{BASE_DIR}/Thiết kế giao diện/Nhân vật 3D/Chuyển động/render-nu-ao-trang-dung.png"
BRAIN_IMG = "/Users/macos/.gemini/antigravity/brain/e586aaa5-2e71-4723-b119-f4df2ed52600/render-nu-ao-trang-dung.png"

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=NU_GLB)
arm = bpy.data.objects['world']

# Action Đứng chánh niệm
arm.animation_data.action = bpy.data.actions['Dung']
bpy.context.scene.frame_set(12)

# Ánh sáng
sun = bpy.data.lights.new(name="Sun34", type='SUN')
sun.energy = 3.2
sun.color = (1.0, 0.98, 0.94)
sun_o = bpy.data.objects.new(name="Sun34", object_data=sun)
bpy.context.scene.collection.objects.link(sun_o)
sun_o.location = (2.5, -3.0, 5.0)
sun_o.rotation_euler = (math.radians(45), math.radians(15), math.radians(-30))

fill = bpy.data.lights.new(name="Fill34", type='AREA')
fill.energy = 75.0
fill.size = 2.5
fill.color = (0.95, 0.97, 1.0)
fill_o = bpy.data.objects.new(name="Fill34", object_data=fill)
bpy.context.scene.collection.objects.link(fill_o)
fill_o.location = (-1.0, -2.5, 0.9)
fill_o.rotation_euler = (math.radians(85), 0, math.radians(15))

# Camera góc 3/4 phía trước
cam = bpy.data.cameras.new("Cam34")
cam.lens = 52
cam_o = bpy.data.objects.new("Cam34", cam)
bpy.context.scene.collection.objects.link(cam_o)
bpy.context.scene.camera = cam_o

cam_o.location = (0.65, -2.40, 0.65)
cam_o.rotation_euler = (math.radians(87), 0, math.radians(15))

bpy.context.scene.render.resolution_x = 1080
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.render.filepath = OUT_IMG

print("Đang render góc 3/4 Đứng chánh niệm...")
bpy.ops.render.render(write_still=True)
print(f"✓ Đã render: {OUT_IMG}")

import shutil
shutil.copy(OUT_IMG, BRAIN_IMG)
