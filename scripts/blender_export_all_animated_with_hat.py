# -*- coding: utf-8 -*-
"""
Gắn Nón Lá Thêu Sen và các vật phẩm trực tiếp vào khung xương (Armature)
của CẢ 3 nhân vật 3D chuyển động thật (nu, nam, tre-em) và xuất tệp GLB chuẩn Web/Coohom.
"""

import bpy
import math
import os

BASE_DIR = "/Users/macos/Desktop/Chùa online"
HAT_OBJ = os.path.join(BASE_DIR, "Thiết kế giao diện", "Vật phẩm 3D", "models", "non_la_theu_sen_v2.obj")
CHAR_DIR = os.path.join(BASE_DIR, "Thiết kế giao diện", "Nhân vật 3D", "Chuyển động")

CONFIGS = [
    {
        "key": "nu",
        "input_glb": os.path.join(CHAR_DIR, "nu-chuyen-dong.glb"),
        "output_glb": os.path.join(CHAR_DIR, "nu-doi-non-la-chuyen-dong.glb"),
        "loc": (0.0, 0.035, 0.49),
        "rot": (math.radians(86), 0, 0),
        "scale": (0.95, 0.95, 0.95)
    },
    {
        "key": "nam",
        "input_glb": os.path.join(CHAR_DIR, "nam-chuyen-dong.glb"),
        "output_glb": os.path.join(CHAR_DIR, "nam-doi-non-la-chuyen-dong.glb"),
        "loc": (0.0, 0.032, 0.52),
        "rot": (math.radians(88), 0, 0),
        "scale": (1.02, 1.02, 1.02)
    },
    {
        "key": "tre_em",
        "input_glb": os.path.join(CHAR_DIR, "tre-em-chuyen-dong.glb"),
        "output_glb": os.path.join(CHAR_DIR, "tre-em-doi-non-la-chuyen-dong.glb"),
        "loc": (0.0, 0.030, 0.43),
        "rot": (math.radians(86), 0, 0),
        "scale": (0.80, 0.80, 0.80)
    }
]

for cfg in CONFIGS:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    print(f"\n--- Đang xử lý gắn Nón Lá cho: {cfg['key']} ---")
    bpy.ops.import_scene.gltf(filepath=cfg["input_glb"])
    
    arm = bpy.data.objects.get("world")
    mesh = bpy.data.objects.get("geometry_0")
    if not arm or not mesh:
        print(f"Bỏ qua {cfg['key']}, không tìm thấy armature.")
        continue
        
    bpy.ops.wm.obj_import(filepath=HAT_OBJ)
    hat = bpy.context.selected_objects[0]
    hat.name = "Non_La_Theu_Sen"
    
    hat.rotation_euler = cfg["rot"]
    hat.location = cfg["loc"]
    hat.scale = cfg["scale"]
    
    hat.parent = arm
    hat.parent_type = 'BONE'
    hat.parent_bone = 'Head'
    
    hat.matrix_parent_inverse = arm.matrix_world.inverted() @ arm.pose.bones['Head'].matrix.inverted()
    hat.location = cfg["loc"]
    hat.rotation_euler = cfg["rot"]
    hat.scale = cfg["scale"]
    
    bpy.ops.export_scene.gltf(
        filepath=cfg["output_glb"],
        export_format='GLB',
        use_selection=False,
        export_animations=True,
        export_skins=True,
        export_morph=True
    )
    print(f"✓ Đã xuất GLB thành công: {cfg['output_glb']}")

print("\n=== HOÀN TẤT GẮN NÓN LÁ CHO CẢ 3 NHÂN VẬT THẬT ===")
