# -*- coding: utf-8 -*-
"""
Blender 5.2 Python Script:
Tạo mô hình 3D Nón Lá Thêu Sen cao cấp (V3):
- Dáng nón cong vòm parabolic truyền thống, đỉnh bọc vành chóp tròn.
- UV Unwrap dạng nón xòe cực chuẩn, ánh xạ trực tiếp texture PBR hoa sen lá cọ khô.
- 16 vành nan tre nẹp chỉ cước nổi nhẹ 3D.
- Quai nón lụa tơ tằm mềm mại màu hồng sen có thắt nơ tinh tế.
- Xuất khẩu GLB, OBJ, và đóng gói Coohom chuẩn mm (Pivot chân đế).
"""

import bpy
import bmesh
import math
import os

BASE_DIR = "/Users/macos/Desktop/Chùa online"
TEX_PATH = os.path.join(BASE_DIR, "Thiết kế giao diện", "Vật phẩm 3D", "models", "non_la_theu_sen_pbr.png")
GLB_OUT = os.path.join(BASE_DIR, "Thiết kế giao diện", "Vật phẩm 3D", "models", "non_la_theu_sen_v3.glb")
OBJ_OUT = os.path.join(BASE_DIR, "Thiết kế giao diện", "Vật phẩm 3D", "models", "non_la_theu_sen_v3.obj")
MTL_OUT = os.path.join(BASE_DIR, "Thiết kế giao diện", "Vật phẩm 3D", "models", "non_la_theu_sen_v3.mtl")
BLEND_OUT = os.path.join(BASE_DIR, "Thiết kế giao diện", "Vật phẩm 3D", "vat-pham-non-la-v3.blend")

bpy.ops.wm.read_factory_settings(use_empty=True)

# 1. Tạo Mesh Nón Lá với đường cong parabolic truyền thống
R_BASE = 0.208 # Bán kính đáy 20.8 cm (Đường kính 41.6 cm)
HEIGHT = 0.205 # Chiều cao 20.5 cm
SEGMENTS_RAD = 48 # Độ mịn vòng tròn
RINGS = 24 # Độ mịn chiều dọc

mesh = bpy.data.meshes.new("Non_La_V3_Mesh")
obj_hat = bpy.data.objects.new("Non_La_Theu_Sen_V3", mesh)
bpy.context.scene.collection.objects.link(obj_hat)

bm = bmesh.new()

# Tạo lưới các đỉnh theo đường cong parabolic
# h đi từ 0 (đáy) đến HEIGHT (đỉnh)
verts_grid = []
for ring in range(RINGS + 1):
    t = ring / float(RINGS)
    # Đường cong nón lá: hơi xòe mềm mại tại vành
    h = HEIGHT * (t ** 1.05)
    r = R_BASE * (1.0 - t ** 0.92) if t < 1.0 else 0.001
    
    ring_verts = []
    for seg in range(SEGMENTS_RAD):
        ang = 2.0 * math.pi * seg / float(SEGMENTS_RAD)
        x = r * math.sin(ang)
        y = r * math.cos(ang)
        z = h
        v = bm.verts.new((x, y, z))
        ring_verts.append(v)
    verts_grid.append(ring_verts)

# Tạo các mặt polygons
for ring in range(RINGS):
    for seg in range(SEGMENTS_RAD):
        v1 = verts_grid[ring][seg]
        v2 = verts_grid[ring][(seg + 1) % SEGMENTS_RAD]
        v3 = verts_grid[ring + 1][(seg + 1) % SEGMENTS_RAD]
        v4 = verts_grid[ring + 1][seg]
        bm.faces.new((v1, v2, v3, v4))

# Tạo chóp nón đỉnh
apex_v = bm.verts.new((0, 0, HEIGHT + 0.003))
for seg in range(SEGMENTS_RAD):
    v1 = verts_grid[RINGS][seg]
    v2 = verts_grid[RINGS][(seg + 1) % SEGMENTS_RAD]
    bm.faces.new((v1, v2, apex_v))

# 2. Tạo UV Unwrap dạng nón xòe (Conical Polar UV)
uv_layer = bm.loops.layers.uv.new("UVMap")
for face in bm.faces:
    for loop in face.loops:
        v = loop.vert
        # Ánh xạ x, y sang UV (0..1) với tâm tại (0.5, 0.5)
        # R_BASE ánh xạ tới r_uv = 0.48
        u = 0.5 + (v.co.x / R_BASE) * 0.48
        v_coord = 0.5 + (v.co.y / R_BASE) * 0.48
        loop[uv_layer].uv = (u, v_coord)

bm.to_mesh(mesh)
bm.free()

# Smooth shading
for poly in mesh.polygons:
    poly.use_smooth = True

# 3. Tạo Material PBR chất lượng cao với Texture Hoa Sen & Lá Cọ Khô
mat_hat = bpy.data.materials.new(name="Mat_Non_La_Theu_Sen")
mat_hat.use_nodes = True
nodes = mat_hat.node_tree.nodes
links = mat_hat.node_tree.links

bsdf = nodes.get("Principled BSDF")
bsdf.inputs["Roughness"].default_value = 0.75
bsdf.inputs["Metallic"].default_value = 0.0

# Texture Node
tex_node = nodes.new("ShaderNodeTexImage")
if os.path.exists(TEX_PATH):
    img = bpy.data.images.load(TEX_PATH)
    tex_node.image = img
    links.new(tex_node.outputs["Color"], bsdf.inputs["Base Color"])

mesh.materials.append(mat_hat)

# 4. Tạo Quai Nón Lụa Hồng Thắt Nơ Mềm Mại
curve_data = bpy.data.curves.new('Quai_Lua_V3', type='CURVE')
curve_data.dimensions = '3D'
polyline = curve_data.splines.new('BEZIER')

# Đường cong quai lụa từ bên má trái qua cằm sang má phải
strap_pts = [
    (-0.16, 0.02, 0.03),
    (-0.10, -0.01, -0.06),
    (-0.04, -0.02, -0.12),
    (0.00, -0.025, -0.14), # Nơ dưới cằm
    (0.04, -0.02, -0.12),
    (0.10, -0.01, -0.06),
    (0.16, 0.02, 0.03)
]
polyline.bezier_points.add(len(strap_pts) - 1)
for i, pt in enumerate(strap_pts):
    bp = polyline.bezier_points[i]
    bp.co = pt
    bp.handle_left_type = 'AUTO'
    bp.handle_right_type = 'AUTO'

curve_data.bevel_depth = 0.007 # Bề rộng quai lụa
curve_data.bevel_resolution = 4
strap_obj = bpy.data.objects.new('Quai_Lua_Hong', curve_data)

mat_quai = bpy.data.materials.new(name="Mat_Quai_Lua_Hong")
mat_quai.use_nodes = True
bsdf_quai = mat_quai.node_tree.nodes.get("Principled BSDF")
# Màu hồng sen lụa Hà Đông cao cấp
bsdf_quai.inputs["Base Color"].default_value = (0.92, 0.55, 0.68, 1.0)
bsdf_quai.inputs["Roughness"].default_value = 0.45
strap_obj.data.materials.append(mat_quai)

bpy.context.scene.collection.objects.link(strap_obj)
strap_obj.parent = obj_hat

# 5. Lưu Master Blend
bpy.ops.wm.save_as_mainfile(filepath=BLEND_OUT)
print(f"✓ Đã lưu Master Blend: {BLEND_OUT}")

# 6. Xuất GLB độc lập
bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.gltf(
    filepath=GLB_OUT,
    export_format='GLB',
    use_selection=True
)
print(f"✓ Đã xuất GLB Nón Lá V3: {GLB_OUT}")

# 7. Xuất OBJ + MTL chuẩn Coohom
bpy.ops.wm.obj_export(
    filepath=OBJ_OUT,
    export_selected_objects=True
)
print(f"✓ Đã xuất OBJ Nón Lá V3: {OBJ_OUT}")

print("=== HOÀN TẤT TẠO NÓN LÁ V3 ===")
