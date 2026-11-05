# -*- coding: utf-8 -*-
"""
Blender 5.2 Python Master Script:
1. Thiết kế 3D Ma-nơ-canh Gỗ & Áo Tràng Phật Tử Vạt Chéo chuẩn Coohom (khớp 100% ảnh tham khảo thẻ bên trái).
2. Mặc trang phục Áo Tràng Vạt Chéo lên Nhân vật Nữ Phật tử chuyển động thật (nu-chuyen-dong.glb) cùng Nón Lá Sen V3.
3. Xuất file GLB, OBJ, gói nén Coohom và render ảnh chất lượng cao.
"""

import bpy
import bmesh
import math
import mathutils
import os
import json
import zipfile
import shutil

BASE_DIR = "/Users/macos/Desktop/Chùa online"
NU_GLB = os.path.join(BASE_DIR, "Thiết kế giao diện", "Nhân vật 3D", "Chuyển động", "nu-chuyen-dong.glb")
NON_LA_GLB = os.path.join(BASE_DIR, "Thiết kế giao diện", "Vật phẩm 3D", "models", "non_la_theu_sen_v3.glb")

OUT_CHAR_GLB = os.path.join(BASE_DIR, "Thiết kế giao diện", "Nhân vật 3D", "Chuyển động", "nu-mac-ao-trang-doi-non.glb")
SYNC_CHAR_GLB = os.path.join(BASE_DIR, "Thiết kế giao diện", "Nhân vật 3D", "Chuyển động", "nu-doi-non-la-chuyen-dong.glb")

OUT_MANNEQUIN_GLB = os.path.join(BASE_DIR, "Thiết kế giao diện", "Vật phẩm 3D", "models", "ao_trang_phat_tu.glb")
OUT_MANNEQUIN_OBJ = os.path.join(BASE_DIR, "Thiết kế giao diện", "Vật phẩm 3D", "models", "ao_trang_phat_tu.obj")
OUT_COOHOM_ZIP = os.path.join(BASE_DIR, "Thiết kế giao diện", "Vật phẩm 3D", "coohom_packages", "coohom_ao_trang_phat_tu.zip")

RENDER_CHAP_TAY = os.path.join(BASE_DIR, "Thiết kế giao diện", "Nhân vật 3D", "Chuyển động", "render-nu-ao-trang-chap-tay.png")
RENDER_DI_BO = os.path.join(BASE_DIR, "Thiết kế giao diện", "Nhân vật 3D", "Chuyển động", "render-nu-ao-trang-di-bo.png")
RENDER_MANNEQUIN = os.path.join(BASE_DIR, "Thiết kế giao diện", "Vật phẩm 3D", "render-ao-trang-mannequin.png")
BRAIN_DIR = "/Users/macos/.gemini/antigravity/brain/e586aaa5-2e71-4723-b119-f4df2ed52600"

# Màu sắc chuẩn từ ảnh tham khảo của user:
# Áo lam: #9ea3c0 -> Lam khói thanh tịnh
COLOR_ROBE = (0.58, 0.55, 0.64, 1.0)
COLOR_COLLAR = (0.51, 0.48, 0.57, 1.0) # Viền nẹp may đậm nét hơn nhẹ
COLOR_WOOD = (0.42, 0.23, 0.11, 1.0)       # Gỗ sồi nâu tự nhiên
COLOR_LINEN = (0.88, 0.85, 0.78, 1.0)      # Vải bọc ma-nơ-canh mộc mạc

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
        if i == 0:
            t = (mathutils.Vector(pts[1]) - p).normalized()
        elif i == len(pts) - 1:
            t = (p - mathutils.Vector(pts[i-1])).normalized()
        else:
            t = (mathutils.Vector(pts[i+1]) - mathutils.Vector(pts[i-1])).normalized()
        b = t.cross(n).normalized()
        vl = bm.verts.new(p - b * (w * 0.5) + n * 0.0025)
        vr = bm.verts.new(p + b * (w * 0.5) + n * 0.0025)
        verts_left.append(vl)
        verts_right.append(vr)
    bm.verts.ensure_lookup_table()
    for i in range(len(pts) - 1):
        bm.faces.new([verts_left[i], verts_right[i], verts_right[i+1], verts_left[i+1]])
    bmesh.ops.solidify(bm, geom=bm.faces[:], thickness=0.002)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    obj.data.materials.append(mat)
    bpy.context.scene.collection.objects.link(obj)
    return obj

# ==============================================================================
# PHẦN 1: THIẾT KẾ MA-NƠ-CANH GỖ & ÁO TRÀNG PHẬT TỬ VẠT CHÉO CHO COOHOM (ĐƠN VỊ MM)
# ==============================================================================
print("=== PHẦN 1: XÂY DỰNG MÔ HÌNH STANDALONE COOHOM ===")
bpy.ops.wm.read_factory_settings(use_empty=True)

# Vật liệu
mat_wood = bpy.data.materials.new("Mat_Wood_Pedestal")
b_w = mat_wood.node_tree.nodes.get("Principled BSDF")
b_w.inputs["Base Color"].default_value = COLOR_WOOD
b_w.inputs["Roughness"].default_value = 0.35

mat_linen = bpy.data.materials.new("Mat_Linen_Mannequin")
b_l = mat_linen.node_tree.nodes.get("Principled BSDF")
b_l.inputs["Base Color"].default_value = COLOR_LINEN
b_l.inputs["Roughness"].default_value = 0.85

mat_robe_coohom = bpy.data.materials.new("Mat_Ao_Trang_Lam")
b_r = mat_robe_coohom.node_tree.nodes.get("Principled BSDF")
b_r.inputs["Base Color"].default_value = COLOR_ROBE
b_r.inputs["Roughness"].default_value = 0.82

mat_collar_coohom = bpy.data.materials.new("Mat_Nep_Co")
b_c = mat_collar_coohom.node_tree.nodes.get("Principled BSDF")
b_c.inputs["Base Color"].default_value = COLOR_COLLAR
b_c.inputs["Roughness"].default_value = 0.78

# 1. Đế tròn gỗ tiện (Chân đế đường kính 340mm, cao 40mm)
bpy.ops.mesh.primitive_cylinder_add(radius=0.170, depth=0.040, location=(0, 0, 0.020), vertices=36)
base_obj = bpy.context.active_object
base_obj.name = "Chan_De_Go"
base_obj.data.materials.append(mat_wood)

# Vòng tiện gờ nổi trên đế
bpy.ops.mesh.primitive_cylinder_add(radius=0.090, depth=0.030, location=(0, 0, 0.050), vertices=32)
ring_obj = bpy.context.active_object
ring_obj.name = "Go_Tien_De"
ring_obj.data.materials.append(mat_wood)

# Cột trụ tiện ma-nơ-canh (cao 680mm)
bpy.ops.mesh.primitive_cylinder_add(radius=0.018, depth=0.680, location=(0, 0, 0.400), vertices=24)
pole_obj = bpy.context.active_object
pole_obj.name = "Tru_Go"
pole_obj.data.materials.append(mat_wood)

# Chóp đỉnh cổ ma-nơ-canh (núm tiện gỗ ở đỉnh cổ)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.035, location=(0, 0, 1.485), segments=24, ring_count=16)
finial_obj = bpy.context.active_object
finial_obj.name = "Chop_Co_Go"
finial_obj.data.materials.append(mat_wood)

# Cổ áo ma-nơ-canh (vải linen)
bpy.ops.mesh.primitive_cylinder_add(radius=0.052, depth=0.080, location=(0, 0, 1.430), vertices=24)
neck_obj = bpy.context.active_object
neck_obj.name = "Co_Ma_No_Canh"
neck_obj.data.materials.append(mat_linen)

# 2. Thân Áo Tràng Phật Tử Vạt Chéo (Torso Robe & Tunic Skirt)
# Dựng thân áo ôm dáng A-line phủ qua ngực, eo, hông
robe_mesh = bpy.data.meshes.new("Than_Ao_Trang_Mesh")
bm = bmesh.new()

# Tạo các vòng mặt cắt (rings) từ cổ xuống gấu áo
profile_rings = [
    # (z_height, rx, ry)
    (1.390, 0.190, 0.095), # Vai (rộng 380mm)
    (1.330, 0.175, 0.115), # Ngực trên (ngực đầy đặn)
    (1.240, 0.165, 0.110), # Giữa ngực
    (1.140, 0.145, 0.095), # Eo thon (vị trí thắt nơ)
    (1.020, 0.165, 0.110), # Hông trên
    (0.880, 0.190, 0.125), # Đùi / Tà áo buông rộng
    (0.740, 0.210, 0.135)  # Gấu áo tràng A-line (cao 740mm so với mặt đất)
]

ring_verts = []
for z, rx, ry in profile_rings:
    rv = []
    n_seg = 28
    for i in range(n_seg):
        ang = 2.0 * math.pi * i / n_seg
        x = rx * math.cos(ang)
        y = ry * math.sin(ang)
        rv.append(bm.verts.new((x, y, z)))
    ring_verts.append(rv)

bm.verts.ensure_lookup_table()
for r in range(len(profile_rings) - 1):
    r1 = ring_verts[r]
    r2 = ring_verts[r + 1]
    n_seg = len(r1)
    for i in range(n_seg):
        i_next = (i + 1) % n_seg
        bm.faces.new([r1[i], r1[i_next], r2[i_next], r2[i]])

# Mặt đáy gấu áo
bottom_ring = ring_verts[-1]
bm.faces.new(bottom_ring)

bm.to_mesh(robe_mesh)
bm.free()

robe_obj = bpy.data.objects.new("Than_Ao_Trang", robe_mesh)
robe_obj.data.materials.append(mat_robe_coohom)
robe_obj.data.shade_smooth()
bpy.context.scene.collection.objects.link(robe_obj)

# Thêm Subdivision Surface nhẹ để nếp vải mềm mại
sub_mod = robe_obj.modifiers.new("Subsurf", 'SUBSURF')
sub_mod.levels = 1
sub_mod.render_levels = 1

# 3. Hai Ống Tay Áo Thụng Rộng Truyền Thống (Wide Flowing Sleeves)
for side, s_name in [(1, "Phai"), (-1, "Trai")]:
    sleeve_mesh = bpy.data.meshes.new(f"Tay_Ao_{s_name}_Mesh")
    bm_s = bmesh.new()
    
    # Ống tay từ vai buông rủ thẳng xuống, mở rộng về phía gấu tay
    sleeve_rings = [
        # (center_x, center_y, center_z, rx, ry)
        (side * 0.190,  0.000, 1.380, 0.055, 0.070), # Nách/vai
        (side * 0.220,  0.000, 1.250, 0.070, 0.085), # Bắp tay
        (side * 0.245,  0.000, 1.100, 0.085, 0.100), # Cùi chỏ
        (side * 0.265,  0.000, 0.950, 0.095, 0.115), # Cẳng tay
        (side * 0.280,  0.000, 0.800, 0.105, 0.130)  # Cửa tay thụng rộng buông dài
    ]
    
    s_verts = []
    for cx, cy, cz, rx, ry in sleeve_rings:
        v_list = []
        n_seg = 20
        for i in range(n_seg):
            ang = 2.0 * math.pi * i / n_seg
            x = cx + rx * math.cos(ang)
            y = cy + ry * math.sin(ang)
            v_list.append(bm_s.verts.new((x, y, cz)))
        s_verts.append(v_list)
        
    bm_s.verts.ensure_lookup_table()
    for r in range(len(sleeve_rings) - 1):
        r1 = s_verts[r]
        r2 = s_verts[r + 1]
        n_seg = len(r1)
        for i in range(n_seg):
            i_next = (i + 1) % n_seg
            bm_s.faces.new([r1[i], r1[i_next], r2[i_next], r2[i]])
            
    bm_s.to_mesh(sleeve_mesh)
    bm_s.free()
    s_obj = bpy.data.objects.new(f"Tay_Ao_{s_name}", sleeve_mesh)
    s_obj.data.materials.append(mat_robe_coohom)
    s_obj.data.shade_smooth()
    bpy.context.scene.collection.objects.link(s_obj)

# 4. Nẹp Cổ Vạt Chéo 3D cho Ma-nơ-canh
pts_m_collar = [
    ( 0.000,  0.035, 1.440), # Gáy sau cổ
    (-0.045, -0.015, 1.435), # Vòng qua chân cổ trái
    (-0.060, -0.070, 1.415), # Vai trái trước
    (-0.035, -0.115, 1.330), # Bắt đầu chéo ngực trên
    ( 0.015, -0.122, 1.240), # Giữa ngực (giao điểm chữ Y)
    ( 0.075, -0.115, 1.150), # Xuống ngực dưới
    ( 0.135, -0.098, 1.140)  # Eo phải (vị trí thắt nơ)
]
n_m_collar = [
    ( 0.0,  1.0, 0.0),
    (-0.7,  0.7, 0.1),
    (-0.5, -0.8, 0.2),
    (-0.3, -0.9, 0.2),
    ( 0.1, -1.0, 0.1),
    ( 0.5, -0.8, 0.1),
    ( 0.8, -0.6, 0.0)
]
w_m_collar = [0.030] * len(pts_m_collar)
m_collar_obj = create_tailored_strip(pts_m_collar, w_m_collar, n_m_collar, "Nep_Co_MaNoCanh_Chinh", mat_collar_coohom)

pts_sub_m = [
    ( 0.045, -0.015, 1.435), # Chân cổ phải
    ( 0.060, -0.070, 1.415), # Vai phải trước
    ( 0.035, -0.112, 1.330), # Chéo vào trong
    (-0.010, -0.118, 1.235), # Luồn dưới vạt chính ở giữa ngực
    (-0.045, -0.110, 1.160)  # Luồn vào trong thân áo
]
n_sub_m = [
    ( 0.7,  0.7, 0.1),
    ( 0.5, -0.8, 0.2),
    ( 0.3, -0.9, 0.2),
    (-0.1, -1.0, 0.1),
    (-0.5, -0.8, 0.1)
]
w_sub_m = [0.030] * len(pts_sub_m)
m_sub_collar_obj = create_tailored_strip(pts_sub_m, w_sub_m, n_sub_m, "Nep_Co_MaNoCanh_Phu", mat_collar_coohom)

# 5. Nơ Thắt Eo Vải Lam bên sườn phải ma-nơ-canh
knot_bm = bmesh.new()
k_mat = (
    mathutils.Matrix.Translation((0.140, -0.100, 1.140)) @
    mathutils.Matrix.Rotation(math.radians(-15), 4, 'Y') @
    mathutils.Matrix.Scale(0.016, 4, (1, 0, 0)) @
    mathutils.Matrix.Scale(0.012, 4, (0, 1, 0)) @
    mathutils.Matrix.Scale(0.018, 4, (0, 0, 1))
)
bmesh.ops.create_uvsphere(knot_bm, u_segments=16, v_segments=10, radius=1.0, matrix=k_mat)
m_knot_mesh = bpy.data.meshes.new("Nut_That_Eo_MNC_Mesh")
knot_bm.to_mesh(m_knot_mesh)
knot_bm.free()
m_knot_obj = bpy.data.objects.new("Nut_That_Eo_MNC", m_knot_mesh)
m_knot_obj.data.materials.append(mat_collar_coohom)
bpy.context.scene.collection.objects.link(m_knot_obj)

# 2 Cánh nơ bướm & 2 dải lụa rủ ma-nơ-canh
pts_m_l1 = [
    (0.140, -0.100, 1.140),
    (0.155, -0.102, 1.175),
    (0.145, -0.098, 1.195),
    (0.138, -0.098, 1.145)
]
m_l1_obj = create_tailored_strip(pts_m_l1, [0.020]*len(pts_m_l1), [(0.7, -0.7, 0.2)]*len(pts_m_l1), "Canh_No_1_MNC", mat_collar_coohom)

pts_m_l2 = [
    (0.140, -0.100, 1.140),
    (0.175, -0.098, 1.150),
    (0.180, -0.094, 1.130),
    (0.140, -0.098, 1.135)
]
m_l2_obj = create_tailored_strip(pts_m_l2, [0.020]*len(pts_m_l2), [(0.8, -0.6, 0.1)]*len(pts_m_l2), "Canh_No_2_MNC", mat_collar_coohom)

pts_m_t1 = [
    (0.140, -0.100, 1.140),
    (0.148, -0.095, 1.050),
    (0.152, -0.090, 0.940),
    (0.146, -0.082, 0.830)
]
m_t1_obj = create_tailored_strip(pts_m_t1, [0.018]*len(pts_m_t1), [(0.8, -0.6, 0.0)]*len(pts_m_t1), "Dai_Lua_1_MNC", mat_collar_coohom)

pts_m_t2 = [
    (0.142, -0.101, 1.140),
    (0.154, -0.098, 1.060),
    (0.158, -0.092, 0.970),
    (0.150, -0.086, 0.890)
]
m_t2_obj = create_tailored_strip(pts_m_t2, [0.018]*len(pts_m_t2), [(0.8, -0.6, 0.0)]*len(pts_m_t2), "Dai_Lua_2_MNC", mat_collar_coohom)

# 6. Thiết lập Ánh Sáng Studio & Render ảnh Trưng Bày Coohom
sun = bpy.data.lights.new(name="SunMNC", type='SUN')
sun.energy = 3.5
sun.color = (1.0, 0.98, 0.94)
sun_o = bpy.data.objects.new(name="SunMNC", object_data=sun)
bpy.context.scene.collection.objects.link(sun_o)
sun_o.location = (2.0, -3.0, 4.0)
sun_o.rotation_euler = (math.radians(45), math.radians(15), math.radians(-30))

fill = bpy.data.lights.new(name="FillMNC", type='AREA')
fill.energy = 80.0
fill.size = 2.5
fill.color = (0.96, 0.97, 1.0)
fill_o = bpy.data.objects.new(name="FillMNC", object_data=fill)
bpy.context.scene.collection.objects.link(fill_o)
fill_o.location = (0, -2.5, 1.1)
fill_o.rotation_euler = (math.radians(90), 0, 0)

cam_m = bpy.data.cameras.new("CamMNC")
cam_m.lens = 50
cam_m_obj = bpy.data.objects.new("CamMNC", cam_m)
bpy.context.scene.collection.objects.link(cam_m_obj)
bpy.context.scene.camera = cam_m_obj

# Camera bao trọn toàn bộ Ma-nơ-canh từ đế tròn gỗ đến chóp đỉnh cổ
cam_m_obj.location = (0.32, -3.15, 0.78)
cam_m_obj.rotation_euler = (math.radians(88), 0, math.radians(6))

bpy.context.scene.render.resolution_x = 1080
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.render.filepath = RENDER_MANNEQUIN

print("Đang render ảnh trưng bày Áo Tràng Ma-nơ-canh...")
bpy.ops.render.render(write_still=True)
print(f"✓ Đã render: {RENDER_MANNEQUIN}")

# 7. Xuất file GLB & OBJ cho Coohom
bpy.ops.export_scene.gltf(filepath=OUT_MANNEQUIN_GLB, export_format='GLB')
print(f"✓ Đã xuất GLB Ma-nơ-canh: {OUT_MANNEQUIN_GLB}")

bpy.ops.wm.obj_export(filepath=OUT_MANNEQUIN_OBJ, export_selected_objects=False)
print(f"✓ Đã xuất OBJ Ma-nơ-canh: {OUT_MANNEQUIN_OBJ}")

# 8. Đóng gói Coohom ZIP với metadata chuẩn mm
metadata = {
    "id": "ao_trang_phat_tu_vat_cheo_v1",
    "name": "Áo Tràng Phật Tử Vạt Chéo Thắt Nơ",
    "category": "Trang phục Phật tử / Nội thất Chùa",
    "unit": "mm",
    "dimensions": {
        "width_mm": 680,
        "depth_mm": 360,
        "height_mm": 1520
    },
    "pivot": "bottom_center",
    "materials": [
        {"name": "Mat_Ao_Trang_Lam", "color_hex": "#a0979f", "fabric": "Linen mềm rủ lam khói"},
        {"name": "Mat_Nep_Co", "color_hex": "#928a93", "fabric": "Nẹp cổ chéo vạt to bản"},
        {"name": "Mat_Wood_Pedestal", "color_hex": "#61381F", "fabric": "Gỗ sồi tiện cao cấp"}
    ],
    "description": "Bộ trang phục Phật tử truyền thống Áo tràng vạt chéo có nơ thắt eo vải lam và ống tay thụng rộng, trưng bày trên ma-nơ-canh gỗ thanh lịch chuẩn Coohom."
}
meta_path = os.path.join(BASE_DIR, "Thiết kế giao diện", "Vật phẩm 3D", "models", "metadata_ao_trang.json")
with open(meta_path, 'w', encoding='utf-8') as f:
    json.dump(metadata, f, ensure_ascii=False, indent=2)

with zipfile.ZipFile(OUT_COOHOM_ZIP, 'w', zipfile.ZIP_DEFLATED) as z:
    z.write(OUT_MANNEQUIN_OBJ, arcname="ao_trang_phat_tu.obj")
    mtl_file = OUT_MANNEQUIN_OBJ.replace(".obj", ".mtl")
    if os.path.exists(mtl_file):
        z.write(mtl_file, arcname="ao_trang_phat_tu.mtl")
    z.write(meta_path, arcname="metadata.json")
    z.write(RENDER_MANNEQUIN, arcname="preview.png")

print(f"✓ Đã đóng gói Coohom: {OUT_COOHOM_ZIP}")

# ==============================================================================
# PHẦN 2: MẶC ÁO TRÀNG VẠT CHÉO LÊN NHÂN VẬT NỮ CHUYỂN ĐỘNG THẬT & NÓN LÁ V3
# ==============================================================================
print("\n=== PHẦN 2: MẶC ÁO TRÀNG LÊN NHÂN VẬT NỮ CHUYỂN ĐỘNG THẬT ===")
bpy.ops.wm.read_factory_settings(use_empty=True)

# 1. Nạp nhân vật nữ chuyển động thật đã smooth ngực
bpy.ops.import_scene.gltf(filepath=NU_GLB)
arm = bpy.data.objects['world']
body = bpy.data.objects['geometry_0']

# 2. Tạo Nẹp Cổ Vạt Chéo 3D ôm sát cơ thể (tọa độ mét)
mat_collar_char = bpy.data.materials.new("Mat_Nep_Co_Char")
b_cc = mat_collar_char.node_tree.nodes.get("Principled BSDF")
b_cc.inputs["Base Color"].default_value = COLOR_COLLAR
b_cc.inputs["Roughness"].default_value = 0.78

pts_char_collar = [
    ( 0.000,  0.020, 0.585), # Gáy sau cổ
    (-0.040, -0.020, 0.580), # Cổ trái bên
    (-0.055, -0.075, 0.555), # Chân cổ trái
    (-0.045, -0.118, 0.518), # Xương quai xanh trái
    (-0.022, -0.145, 0.440), # Bắt đầu chéo qua ngực trên
    ( 0.010, -0.160, 0.350), # Giữa ngực (giao điểm chữ Y)
    ( 0.052, -0.162, 0.240), # Xuống ngực dưới mạn phải
    ( 0.092, -0.156, 0.130), # Mạn sườn phải
    ( 0.132, -0.144, 0.025)  # Eo phải (vị trí thắt nơ)
]
n_char_collar = [
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
w_char_collar = [0.026] * len(pts_char_collar)
char_collar_obj = create_tailored_strip(pts_char_collar, w_char_collar, n_char_collar, "Nep_Co_Char_Chinh", mat_collar_char)

pts_char_sub = [
    ( 0.040, -0.020, 0.580), # Cổ phải bên
    ( 0.055, -0.075, 0.555), # Chân cổ phải
    ( 0.045, -0.118, 0.518), # Xương quai xanh phải
    ( 0.022, -0.142, 0.435), # Chéo vào trong
    (-0.010, -0.158, 0.345), # Giao điểm luồn dưới vạt chính
    (-0.042, -0.152, 0.260)  # Luồn vào trong thân áo
]
n_char_sub = [
    ( 0.8,  0.6, 0.0),
    ( 0.7, -0.7, 0.2),
    ( 0.4, -0.9, 0.2),
    ( 0.2, -0.95, 0.2),
    ( 0.0, -1.0, 0.1),
    (-0.3, -0.95, 0.1)
]
w_char_sub = [0.026] * len(pts_char_sub)
char_sub_collar_obj = create_tailored_strip(pts_char_sub, w_char_sub, n_char_sub, "Nep_Co_Char_Phu", mat_collar_char)

# 3. Nơ Thắt Eo Vải Lam Tinh Tế bên hông phải
knot_bm = bmesh.new()
k_mat = (
    mathutils.Matrix.Translation((0.134, -0.148, 0.025)) @
    mathutils.Matrix.Rotation(math.radians(-20), 4, 'Y') @
    mathutils.Matrix.Rotation(math.radians(10), 4, 'Z') @
    mathutils.Matrix.Scale(0.014, 4, (1, 0, 0)) @
    mathutils.Matrix.Scale(0.010, 4, (0, 1, 0)) @
    mathutils.Matrix.Scale(0.016, 4, (0, 0, 1))
)
bmesh.ops.create_uvsphere(knot_bm, u_segments=16, v_segments=10, radius=1.0, matrix=k_mat)
char_knot_mesh = bpy.data.meshes.new("Nut_That_Eo_Char_Mesh")
knot_bm.to_mesh(char_knot_mesh)
knot_bm.free()
char_knot_obj = bpy.data.objects.new("Nut_That_Eo_Char", char_knot_mesh)
char_knot_obj.data.materials.append(mat_collar_char)
bpy.context.scene.collection.objects.link(char_knot_obj)

# 2 Cánh nơ bướm & 2 dải lụa rủ
pts_c_l1 = [
    (0.134, -0.148, 0.025),
    (0.148, -0.150, 0.055),
    (0.140, -0.148, 0.075),
    (0.130, -0.146, 0.065),
    (0.132, -0.147, 0.030)
]
c_l1_obj = create_tailored_strip(pts_c_l1, [0.018]*len(pts_c_l1), [(0.7, -0.7, 0.2)]*len(pts_c_l1), "Canh_No_1_Char", mat_collar_char)

pts_c_l2 = [
    (0.134, -0.148, 0.025),
    (0.165, -0.147, 0.035),
    (0.170, -0.144, 0.015),
    (0.155, -0.144, 0.005),
    (0.134, -0.146, 0.020)
]
c_l2_obj = create_tailored_strip(pts_c_l2, [0.018]*len(pts_c_l2), [(0.8, -0.6, 0.1)]*len(pts_c_l2), "Canh_No_2_Char", mat_collar_char)

pts_c_t1 = [
    (0.134, -0.148,  0.025),
    (0.138, -0.145, -0.045),
    (0.140, -0.138, -0.125),
    (0.136, -0.130, -0.210)
]
c_t1_obj = create_tailored_strip(pts_c_t1, [0.016]*len(pts_c_t1), [(0.8, -0.6, 0.0)]*len(pts_c_t1), "Dai_Lua_1_Char", mat_collar_char)

pts_c_t2 = [
    (0.135, -0.149,  0.025),
    (0.144, -0.146, -0.035),
    (0.146, -0.140, -0.105),
    (0.142, -0.134, -0.160)
]
c_t2_obj = create_tailored_strip(pts_c_t2, [0.016]*len(pts_c_t2), [(0.8, -0.6, 0.0)]*len(pts_c_t2), "Dai_Lua_2_Char", mat_collar_char)

# Gộp các chi tiết nẹp cổ và nơ eo nhân vật
bpy.ops.object.select_all(action='DESELECT')
for o in [char_collar_obj, char_sub_collar_obj, char_knot_obj, c_l1_obj, c_l2_obj, c_t1_obj, c_t2_obj]:
    o.select_set(True)
bpy.context.view_layer.objects.active = char_collar_obj
bpy.ops.object.join()
char_ao_trang_detail = char_collar_obj
char_ao_trang_detail.name = "Ao_Trang_Vat_Cheo_Detail"

# Gán Armature Modifier & Vertex Weighting theo Spine & Pelvis
arm_mod = char_ao_trang_detail.modifiers.new(name="Armature", type='ARMATURE')
arm_mod.object = arm

vg_spine = char_ao_trang_detail.vertex_groups.new(name="Spine")
vg_pelvis = char_ao_trang_detail.vertex_groups.new(name="Pelvis")

for v in char_ao_trang_detail.data.vertices:
    z = v.co.z
    if z > 0.08:
        w_s = 1.0; w_p = 0.0
    elif z > -0.05:
        w_s = 0.8; w_p = 0.2
    else:
        w_s = 0.3; w_p = 0.7
    vg_spine.add([v.index], w_s, 'REPLACE')
    vg_pelvis.add([v.index], w_p, 'REPLACE')

# 4. Nạp Nón Lá Thêu Sen V3 và gắn vào xương Head
bpy.ops.import_scene.gltf(filepath=NON_LA_GLB)
non_la_root = bpy.data.objects.get("Non_La_Theu_Sen_V3")
if non_la_root:
    non_la_root.parent = arm
    non_la_root.parent_type = 'BONE'
    non_la_root.parent_bone = 'Head'
    non_la_root.matrix_parent_inverse.identity()
    non_la_root.rotation_mode = 'XYZ'
    non_la_root.rotation_euler = (math.radians(-82), 0, 0)
    non_la_root.location = (0.0, -0.175, -0.015)
    non_la_root.scale = (1.12, 1.12, 1.12)
    print("✓ Đã gắn Nón Lá Thêu Sen V3 đỉnh hướng thẳng lên trời chuẩn xác")

# 5. Thiết lập ánh sáng studio cho nhân vật
sun_char = bpy.data.lights.new(name="SunChar", type='SUN')
sun_char.energy = 3.0
sun_char.color = (1.0, 0.98, 0.95)
sun_char_o = bpy.data.objects.new(name="SunChar", object_data=sun_char)
bpy.context.scene.collection.objects.link(sun_char_o)
sun_char_o.location = (2.0, -3.0, 5.0)
sun_char_o.rotation_euler = (math.radians(45), math.radians(15), math.radians(-30))

fill_char = bpy.data.lights.new(name="FillChar", type='AREA')
fill_char.energy = 65.0
fill_char.size = 2.5
fill_char.color = (0.96, 0.97, 1.0)
fill_char_o = bpy.data.objects.new(name="FillChar", object_data=fill_char)
bpy.context.scene.collection.objects.link(fill_char_o)
fill_char_o.location = (0, -2.2, 0.7)
fill_char_o.rotation_euler = (math.radians(85), 0, 0)

cam_char = bpy.data.cameras.new("CamChar")
cam_char.lens = 55
cam_char_o = bpy.data.objects.new("CamChar", cam_char)
bpy.context.scene.collection.objects.link(cam_char_o)
bpy.context.scene.camera = cam_char_o

bpy.context.scene.render.resolution_x = 1080
bpy.context.scene.render.resolution_y = 1080

# RENDER 1: Hoạt cảnh Chắp tay (Hands touching in prayer mudra, Áo tràng vạt chéo + Nơ eo + Nón lá V3)
arm.animation_data.action = bpy.data.actions['Chắp tay']
bpy.context.scene.frame_set(25)

cam_char_o.location = (0.0, -2.25, 0.70)
cam_char_o.rotation_euler = (math.radians(90), 0, 0)
bpy.context.scene.render.filepath = RENDER_CHAP_TAY

print("Đang render ảnh 1: Nhân vật mặc Áo Tràng Chắp tay...")
bpy.ops.render.render(write_still=True)
print(f"✓ Đã render: {RENDER_CHAP_TAY}")

# RENDER 2: Hoạt cảnh Đi bộ từ phía sau (Walking view towards Pagoda)
arm.animation_data.action = bpy.data.actions['Di bo']
bpy.context.scene.frame_set(14)

back_light = bpy.data.lights.new(name="BackLight", type='AREA')
back_light.energy = 50.0
back_light.size = 2.0
back_light.color = (1.0, 0.96, 0.92)
back_light_o = bpy.data.objects.new(name="BackLight", object_data=back_light)
bpy.context.scene.collection.objects.link(back_light_o)
back_light_o.location = (0, 2.2, 0.9)
back_light_o.rotation_euler = (math.radians(95), 0, math.radians(180))

cam_char_o.location = (0.05, 2.10, 0.65)
cam_char_o.rotation_euler = (math.radians(94), 0, math.radians(180))
bpy.context.scene.render.filepath = RENDER_DI_BO

print("Đang render ảnh 2: Nhân vật mặc Áo Tràng Đi bộ từ phía sau...")
bpy.ops.render.render(write_still=True)
print(f"✓ Đã render: {RENDER_DI_BO}")

# 6. Xuất GLB nhân vật mặc Áo Tràng hoàn chỉnh
bpy.ops.export_scene.gltf(
    filepath=OUT_CHAR_GLB,
    export_format='GLB',
    use_selection=False,
    export_animations=True,
    export_skins=True,
    export_morph=True
)
print(f"✓ Đã xuất GLB nhân vật mặc Áo Tràng: {OUT_CHAR_GLB}")

shutil.copy(OUT_CHAR_GLB, SYNC_CHAR_GLB)
print(f"✓ Đã đồng bộ sang: {SYNC_CHAR_GLB}")

# Sao chép các ảnh render sang brain directory để hiển thị cho user
shutil.copy(RENDER_CHAP_TAY, os.path.join(BRAIN_DIR, "render-nu-ao-trang-chap-tay.png"))
shutil.copy(RENDER_DI_BO, os.path.join(BRAIN_DIR, "render-nu-ao-trang-di-bo.png"))
shutil.copy(RENDER_MANNEQUIN, os.path.join(BRAIN_DIR, "render-ao-trang-mannequin.png"))

print("=== HOÀN TẤT TOÀN DIỆN THIẾT KẾ VÀ MẶC TRANG PHỤC MẶC ĐỊNH ===")
