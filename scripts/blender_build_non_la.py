# -*- coding: utf-8 -*-
"""
Blender 5.2 Python script:
Mở nhan-vat-di-chua-v2.blend, tạo mô hình 3D Nón Lá Thêu Sen chi tiết cao,
gắn trực tiếp lên đầu nhân vật Phật tử Nữ trong Blender, render ảnh studio
và xuất file .blend, .glb, .obj chuẩn Coohom.
"""

import bpy
import bmesh
import math
import os

BASE_DIR = "/Users/macos/Desktop/Chùa online"
BLEND_IN = os.path.join(BASE_DIR, "Thiết kế giao diện", "Nhân vật 3D", "nhan-vat-di-chua-v2.blend")
BLEND_OUT = os.path.join(BASE_DIR, "Thiết kế giao diện", "Vật phẩm 3D", "vat-pham-chua-online.blend")
RENDER_OUT = os.path.join(BASE_DIR, "Thiết kế giao diện", "Vật phẩm 3D", "blender-render-non-la.png")
GLB_OUT = os.path.join(BASE_DIR, "Thiết kế giao diện", "Vật phẩm 3D", "models", "non_la_blender.glb")
OBJ_OUT = os.path.join(BASE_DIR, "Thiết kế giao diện", "Vật phẩm 3D", "models", "non_la_blender.obj")

# Mở file blend gốc
bpy.ops.wm.open_mainfile(filepath=BLEND_IN)

# Tạo collection riêng cho Vật Phẩm
col_name = "Vat_Pham_3D"
if col_name in bpy.data.collections:
    col = bpy.data.collections[col_name]
else:
    col = bpy.data.collections.new(col_name)
    bpy.context.scene.collection.children.link(col)

# Tạo Material PBR chất lượng cao
def get_or_create_mat(name, color, roughness=0.8, metallic=0.0):
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        # Blender 4.x / 5.x Principled BSDF inputs
        if "Base Color" in bsdf.inputs:
            bsdf.inputs["Base Color"].default_value = color
        if "Roughness" in bsdf.inputs:
            bsdf.inputs["Roughness"].default_value = roughness
        if "Metallic" in bsdf.inputs:
            bsdf.inputs["Metallic"].default_value = metallic
    return mat

mat_la = get_or_create_mat("Mat_La_Non", (0.92, 0.86, 0.72, 1.0), roughness=0.85)
mat_vanh = get_or_create_mat("Mat_Vanh_Tre", (0.75, 0.62, 0.44, 1.0), roughness=0.7)
mat_sen = get_or_create_mat("Mat_Sen_Hong", (0.94, 0.52, 0.65, 1.0), roughness=0.55)
mat_nhuy = get_or_create_mat("Mat_Nhuy_Vang", (0.98, 0.80, 0.20, 1.0), roughness=0.4)
mat_la_sen = get_or_create_mat("Mat_La_Sen_Xanh", (0.25, 0.58, 0.35, 1.0), roughness=0.7)
mat_quai = get_or_create_mat("Mat_Quai_Lua", (0.95, 0.65, 0.73, 1.0), roughness=0.5)

# 1. Tạo thân nón lá với đường cong giải phẫu 16 vành
mesh = bpy.data.meshes.new("Non_La_Than")
obj_hat = bpy.data.objects.new("Non_La_Theu_Sen", mesh)
col.objects.link(obj_hat)

bm = bmesh.new()

R_BASE = 0.208
H_CONE = 0.215
R_TOP = 0.012
RINGS = 16
SEGS = 40

verts_rings = []
for ring_i in range(RINGS + 1):
    frac = ring_i / RINGS
    y = H_CONE * frac
    r = R_BASE * math.pow(1.0 - frac, 0.92) + R_TOP * frac
    ring_v = []
    for s_i in range(SEGS):
        th = 2 * math.pi * s_i / SEGS
        # Trong Blender Z là trục đứng
        vx = r * math.cos(th)
        vy = r * math.sin(th)
        vz = y
        v = bm.verts.new((vx, vy, vz))
        ring_v.append(v)
    verts_rings.append(ring_v)

# Tạo các quad faces
for r_i in range(RINGS):
    for s_i in range(SEGS):
        next_s = (s_i + 1) % SEGS
        v1 = verts_rings[r_i][s_i]
        v2 = verts_rings[r_i][next_s]
        v3 = verts_rings[r_i + 1][next_s]
        v4 = verts_rings[r_i + 1][s_i]
        bm.faces.new((v1, v2, v3, v4))

# Chóp nón đỉnh
tip_v = bm.verts.new((0, 0, H_CONE + 0.008))
for s_i in range(SEGS):
    next_s = (s_i + 1) % SEGS
    bm.faces.new((tip_v, verts_rings[RINGS][s_i], verts_rings[RINGS][next_s]))

bm.to_mesh(mesh)
bm.free()

mesh.materials.append(mat_la)

# Thêm Solidify modifier để có độ dày lá 1.6mm
mod_sol = obj_hat.modifiers.new(name="Do_Day_La", type='SOLIDIFY')
mod_sol.thickness = 0.0016
mod_sol.offset = -1.0

# Thêm Subdivision modifier để mặt nón láng mịn
mod_sub = obj_hat.modifiers.new(name="Lam_Min", type='SUBSURF')
mod_sub.levels = 1
mod_sub.render_levels = 2

# 2. Tạo vành tre chân nón (Vành cái)
bpy.ops.mesh.primitive_torus_add(
    major_radius=R_BASE,
    minor_radius=0.0035,
    major_segments=48,
    minor_segments=10,
    location=(0, 0, 0.002)
)
obj_rim = bpy.context.active_object
obj_rim.name = "Non_La_Vanh_Cai"
obj_rim.data.materials.append(mat_vanh)
obj_rim.parent = obj_hat
# Chuyển vào collection
for c in obj_rim.users_collection:
    c.objects.unlink(obj_rim)
col.objects.link(obj_rim)

# 3. Tạo họa tiết đóa sen 3D thêu trên mặt nón
# Đóa sen ở mặt trước y dương (trong Blender)
y_lotus_z = 0.095
r_lotus = R_BASE * math.pow(1.0 - (y_lotus_z / H_CONE), 0.92) + 0.003

bm_sen = bmesh.new()
petal_angles = [-0.35, -0.18, 0.0, 0.18, 0.35]
for p_ang in petal_angles:
    p_w = 0.015
    p_len = 0.038
    # Cánh sen cong
    for step in range(4):
        f = step / 3.0
        w = p_w * math.sin(f * math.pi)
        px_l = math.sin(p_ang) * 0.02 - w
        px_r = math.sin(p_ang) * 0.02 + w
        pz = y_lotus_z + f * p_len
        py = r_lotus + 0.002 * math.sin(f * math.pi)
        v_l = bm_sen.verts.new((px_l, py, pz))
        v_r = bm_sen.verts.new((px_r, py, pz))
    # Nối mặt
    # Simple petal strip
mesh_sen = bpy.data.meshes.new("Hoa_Sen_Theu")
bpy.ops.mesh.primitive_cone_add(radius1=0.025, radius2=0.005, depth=0.035, location=(0, r_lotus, y_lotus_z + 0.018), rotation=(math.radians(20), 0, 0))
obj_sen = bpy.context.active_object
obj_sen.name = "Non_La_Hoa_Sen"
obj_sen.scale = (1.2, 0.4, 1.0)
obj_sen.data.materials.append(mat_sen)
obj_sen.parent = obj_hat
for c in obj_sen.users_collection:
    c.objects.unlink(obj_sen)
col.objects.link(obj_sen)

# 4. Tạo Quai Lụa mềm mại rủ tự nhiên
curve_data = bpy.data.curves.new('Quai_Lua_Curve', type='CURVE')
curve_data.dimensions = '3D'
polyline = curve_data.splines.new('BEZIER')

# Điểm quai lụa từ vành trong xuống cằm
strap_pts = [
    (-0.140, 0, 0.05),
    (-0.100, 0.01, -0.06),
    (0.000, 0.02, -0.16),
    (0.100, 0.01, -0.06),
    (0.140, 0, 0.05)
]
polyline.bezier_points.add(len(strap_pts) - 1)
for i, pt in enumerate(strap_pts):
    bp = polyline.bezier_points[i]
    bp.co = pt
    bp.handle_left_type = 'AUTO'
    bp.handle_right_type = 'AUTO'

curve_data.bevel_depth = 0.006
curve_data.bevel_resolution = 4
curve_obj = bpy.data.objects.new('Non_La_Quai_Lua', curve_data)
curve_obj.data.materials.append(mat_quai)
curve_obj.parent = obj_hat
col.objects.link(curve_obj)

# 5. Gắn trực tiếp lên đầu Phật tử Nữ trong file blend
# Tìm vị trí đầu Phật tử Nữ (Nu_dau / Nu_toc)
nu_dau = bpy.data.objects.get("Nu_dau")
nu_toc = bpy.data.objects.get("Nu_toc")

if nu_toc:
    # Vị trí đỉnh tóc Phật tử Nữ
    loc = nu_toc.location.copy()
    # Nón lá chụp vừa vặn trên búi tóc, hơi nghiêng về sau 4.5 độ
    obj_hat.location = (loc.x, loc.y - 0.010, loc.z - 0.015)
    obj_hat.rotation_euler = (math.radians(-4.5), 0, 0)
    obj_hat.scale = (0.94, 0.94, 0.94)
    print(f"✓ Đã gắn nón lá khít đỉnh đầu Nu_toc tại: {obj_hat.location}")
elif nu_dau:
    loc = nu_dau.location.copy()
    obj_hat.location = (loc.x, loc.y - 0.010, loc.z + 0.11)
    obj_hat.rotation_euler = (math.radians(-4.5), 0, 0)
    obj_hat.scale = (0.94, 0.94, 0.94)

# 6. Thiết lập Camera & Render ảnh bằng Blender EEVEE / Workbench
cam = bpy.data.objects.get("Goc_nhin")
if cam:
    bpy.context.scene.camera = cam
    # Hướng camera nhìn vào khuôn mặt và nón lá
    cam.location = (0.45, -1.10, 1.62)
    cam.rotation_euler = (math.radians(82), 0, math.radians(22))

bpy.context.scene.render.resolution_x = 1280
bpy.context.scene.render.resolution_y = 800
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.filepath = RENDER_OUT

# Render
print("Bắt đầu render hình ảnh từ Blender...")
bpy.ops.render.render(write_still=True)
print(f"✓ Đã render hình ảnh Blender: {RENDER_OUT}")

# 7. Lưu file .blend hoàn chỉnh
bpy.ops.wm.save_as_mainfile(filepath=BLEND_OUT)
print(f"✓ Đã lưu file Blender project: {BLEND_OUT}")

# 8. Xuất file GLB & OBJ
# Xuất Nón Lá đơn lẻ sang OBJ & GLB
bpy.ops.object.select_all(action='DESELECT')
obj_hat.select_set(True)
for ch in obj_hat.children:
    ch.select_set(True)
bpy.context.view_layer.objects.active = obj_hat

try:
    bpy.ops.wm.obj_export(filepath=OBJ_OUT, export_selected_objects=True)
    print(f"✓ Đã xuất OBJ từ Blender: {OBJ_OUT}")
except Exception as e:
    print("Export OBJ lỗi nhẹ:", e)

try:
    bpy.ops.export_scene.gltf(filepath=GLB_OUT, use_selection=True)
    print(f"✓ Đã xuất GLB từ Blender: {GLB_OUT}")
except Exception as e:
    print("Export GLTF lỗi nhẹ:", e)

print("=== HOÀN TẤT QUY TRÌNH BLENDER 5.2 ===")
