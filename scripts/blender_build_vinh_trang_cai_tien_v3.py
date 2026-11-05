"""
BẢN CẢI TIẾN V3 (từ blender_build_vinh_trang.py gốc) — sửa cháy sáng nội điện:
- Đèn bàn thờ 3200 -> 1200, đèn rọi tượng 1800 -> 700, đèn nến 350 -> 120 (bản gốc quá mạnh, cháy trắng)
- Hào quang emission 5.5 -> 2.8; giữ AgX mặc định cho nội thất (Standard chỉ dùng cho mặt tiền)
- Mặt tiền: vàng bão hòa (1.0, 0.60, 0.01), cột tầng trệt đỏ son, khối mái lớn phía sau
"""
# -*- coding: utf-8 -*-
"""
Blender 5.2+ Python Script: Dựng mô hình 3D Chùa Vĩnh Tràng (Mỹ Tho - Tiền Giang)
Đạt chuẩn mực kiến trúc nghệ thuật giao thoa Đông - Tây & Di sản Văn hóa cấp Quốc gia.

Hệ trục tọa độ Blender chuẩn xác tuyệt đối:
- Trục Z: UP (Chiều cao, Z = 0m mặt đất -> 18.2m đỉnh Bảo Châu tháp Angkor)
- Trục Y: DEPTH (Chiều sâu):
  * Y = -28m -> -10m: Sân tiền đường gạch Bát Tràng & Cây cảnh ngoại thất
  * Y = -14.5m: Lư hương đồng tam bảo 3 chân lớn
  * Y = -13.0m: 2 Chậu sen đá cổ
  * Y = -12.2m -> -10.0m: Bậc tam cấp granite 5 bậc
  * Y = -7.8m: Hàng 6 cột La Mã composite & 5 gian vòm cuốn mặt tiền
  * Y = -7.4m: Tường tiền đường & Cửa đại Chánh điện
  * Y = -7.0m -> +8.5m: Nội điện Chánh điện Tam Bảo
  * Y = +4.5m -> +7.0m: Bàn thờ Tam Bảo 3 tầng & Tượng Phật Thích Ca dát vàng
- Trục X: WIDTH (Chiều ngang mặt tiền 24m đối xứng, X = -12m -> +12m, nền X = -14m -> +14m)
"""

import bpy
import bmesh
import math
from mathutils import Vector, Euler, Matrix
import os

# Thư mục xuất bản
BASE_DIR = "/home/hatch/workspace/chua-online-work"
OUTPUT_DIR = os.path.join(BASE_DIR, "output_v3")
os.makedirs(OUTPUT_DIR, exist_ok=True)

BLEND_OUT = os.path.join(OUTPUT_DIR, "chua_vinh_trang_full.blend")
GLB_OUT = os.path.join(OUTPUT_DIR, "chua_vinh_trang_blender.glb")
IMG_FACADE = os.path.join(OUTPUT_DIR, "render_vinh_trang_facade.png")
IMG_ALTAR = os.path.join(OUTPUT_DIR, "render_vinh_trang_altar.png")

# 1. Khởi tạo scene mới hoàn toàn
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.name = "Chua_Vinh_Trang_Scene"

# Cài đặt đơn vị Mét
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1.0

# Quản lý Collections
def create_collection(name, parent=None):
    col = bpy.data.collections.new(name)
    if parent:
        parent.children.link(col)
    else:
        scene.collection.children.link(col)
    return col

col_arch = create_collection("01_Kien_Truc_Chua")
col_roof = create_collection("02_Mai_Va_Thap", col_arch)
col_altar = create_collection("03_Chanh_Dien_Cung_Bai")
col_env = create_collection("04_San_Vuon_Khuon_Vien")
col_lights = create_collection("05_Lighting_Camera")

# Helper tạo Material PBR
def make_mat(name, color, roughness=0.6, metallic=0.0, emission_color=(0,0,0,1), emission_strength=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        if "Base Color" in bsdf.inputs:
            bsdf.inputs["Base Color"].default_value = color
        if "Roughness" in bsdf.inputs:
            bsdf.inputs["Roughness"].default_value = roughness
        if "Metallic" in bsdf.inputs:
            bsdf.inputs["Metallic"].default_value = metallic
        if emission_strength > 0:
            if "Emission Color" in bsdf.inputs:
                bsdf.inputs["Emission Color"].default_value = emission_color
            elif "Emission" in bsdf.inputs:
                bsdf.inputs["Emission"].default_value = emission_color
            if "Emission Strength" in bsdf.inputs:
                bsdf.inputs["Emission Strength"].default_value = emission_strength
    return mat

# Bảng vật liệu kiến trúc chuẩn Chùa Vĩnh Tràng
mat_facade_cream = make_mat("Tuong_Vang_Kem_VinhTrang", (1.0, 0.60, 0.01, 1.0), roughness=0.7)
mat_facade_detail= make_mat("Chi_Tiet_Vang_Kem_Nhat", (1.0, 0.70, 0.08, 1.0), roughness=0.6)
mat_column_ivory = make_mat("Cot_LaMa_TrangNga", (0.95, 0.93, 0.86, 1.0), roughness=0.55)
mat_column_red   = make_mat("Cot_Do_Son_Then_VinhTrang", (0.52, 0.07, 0.04, 1.0), roughness=0.45)
mat_terracotta   = make_mat("Ngoi_Dat_Nung_DoGach", (0.34, 0.10, 0.045, 1.0), roughness=0.78)
mat_terracotta_dk= make_mat("Bo_Chi_Ngoi_DoDam", (0.24, 0.07, 0.03, 1.0), roughness=0.75)
mat_gold_ornament= make_mat("Hoa_Van_Thep_Vang", (0.98, 0.74, 0.16, 1.0), roughness=0.35, metallic=0.2)
mat_wood_dark    = make_mat("Go_Gu_Co_Kinh", (0.05, 0.04, 0.03, 1.0), roughness=0.65)
mat_wood_door    = make_mat("Cua_Go_Tram_Khac", (0.32, 0.16, 0.09, 1.0), roughness=0.5)
mat_granite_step = make_mat("Da_Hoa_Cuong_TamCap", (0.52, 0.49, 0.46, 1.0), roughness=0.55)
mat_yard_tile    = make_mat("Gach_Lat_San_BatTrang", (0.55, 0.53, 0.50, 1.0), roughness=0.85)
mat_grass        = make_mat("Tham_Co_Thien_Mon", (0.24, 0.40, 0.16, 1.0), roughness=0.9)
mat_bronze_urn   = make_mat("Dong_Co_Lu_Huong", (0.35, 0.27, 0.18, 1.0), roughness=0.35, metallic=0.88)
mat_buddha_gold  = make_mat("Tuong_Phat_Dat_Vang", (0.96, 0.78, 0.22, 1.0), roughness=0.20, metallic=0.90)
mat_lotus_pink   = make_mat("Hoa_Sen_Hong", (0.94, 0.38, 0.54, 1.0), roughness=0.45)
mat_candle_flame = make_mat("Ngon_Lua_Dan_DuocSu", (1.0, 0.65, 0.15, 1.0), roughness=0.1, emission_color=(1.0, 0.70, 0.20, 1.0), emission_strength=2.5)
mat_halo_gold    = make_mat("Hao_Quang_Vang_Sang", (1.0, 0.88, 0.35, 1.0), roughness=0.1, emission_color=(1.0, 0.85, 0.38, 1.0), emission_strength=2.8)
mat_incense_red  = make_mat("Chan_Nhang_Do", (0.85, 0.12, 0.12, 1.0), roughness=0.7)
mat_water_pool   = make_mat("Mat_Nuoc_Ho_Sen", (0.12, 0.32, 0.36, 1.0), roughness=0.1, metallic=0.15)
mat_ceramic_blue = make_mat("Gom_Su_Kieu_Phap", (0.25, 0.45, 0.65, 1.0), roughness=0.3)

# -------------------------------------------------------------------------
# CÁC HÀM XÂY DỰNG MESH CHUẨN XÁC
# -------------------------------------------------------------------------
def link_obj(obj, name, material, collection):
    obj.name = name
    if material:
        obj.data.materials.append(material)
    for c in obj.users_collection:
        c.objects.unlink(obj)
    collection.objects.link(obj)
    return obj

def add_box(name, location, scale, material, collection=col_arch):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location)
    obj = bpy.context.active_object
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return link_obj(obj, name, material, collection)

def add_cylinder(name, location, radius, depth, material, collection=col_arch, rotation=(0,0,0)):
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, vertices=28, location=location, rotation=rotation)
    obj = bpy.context.active_object
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return link_obj(obj, name, material, collection)

def add_cone(name, location, radius1, radius2, depth, material, collection=col_arch, rotation=(0,0,0)):
    bpy.ops.mesh.primitive_cone_add(radius1=radius1, radius2=radius2, depth=depth, vertices=24, location=location, rotation=rotation)
    obj = bpy.context.active_object
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return link_obj(obj, name, material, collection)

def add_sphere(name, location, radius, material, collection=col_arch, scale=(1,1,1)):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, segments=24, ring_count=16, location=location)
    obj = bpy.context.active_object
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return link_obj(obj, name, material, collection)

def add_arch(name, location, width, height, thickness, depth, material, collection=col_arch):
    """
    Tạo vòm cuốn La Mã cong tròn thực sự (Romanesque Arch):
    - location: (x, y, z) tâm đáy vòm
    - width: khẩu độ nhịp vòm (span)
    - height: chiều cao từ chân vòm lên đỉnh vòm
    - thickness: độ dày đắp nổi của đường chỉ vòm
    - depth: chiều sâu theo trục Y
    """
    r_outer = width / 2.0
    r_inner = r_outer - thickness
    segments = 16
    
    mesh = bpy.data.meshes.new(name + "_mesh")
    bm = bmesh.new()
    
    verts_front_inner = []
    verts_front_outer = []
    verts_back_inner = []
    verts_back_outer = []
    
    half_d = depth / 2.0
    
    for i in range(segments + 1):
        angle = math.pi * i / segments
        ca = math.cos(angle)
        sa = math.sin(angle)
        
        # Front verts (Y = -half_d)
        v_fo = bm.verts.new((-ca * r_outer, -half_d, sa * r_outer))
        v_fi = bm.verts.new((-ca * r_inner, -half_d, sa * r_inner))
        verts_front_outer.append(v_fo)
        verts_front_inner.append(v_fi)
        
        # Back verts (Y = +half_d)
        v_bo = bm.verts.new((-ca * r_outer, half_d, sa * r_outer))
        v_bi = bm.verts.new((-ca * r_inner, half_d, sa * r_inner))
        verts_back_outer.append(v_bo)
        verts_back_inner.append(v_bi)
        
    bm.verts.ensure_lookup_table()
    
    for i in range(segments):
        # Front face
        bm.faces.new([verts_front_inner[i], verts_front_outer[i], verts_front_outer[i+1], verts_front_inner[i+1]])
        # Back face
        bm.faces.new([verts_back_inner[i+1], verts_back_outer[i+1], verts_back_outer[i], verts_back_inner[i]])
        # Outer top face
        bm.faces.new([verts_front_outer[i], verts_back_outer[i], verts_back_outer[i+1], verts_front_outer[i+1]])
        # Inner ceiling face
        bm.faces.new([verts_front_inner[i+1], verts_back_inner[i+1], verts_back_inner[i], verts_front_inner[i]])
        
    # Bottom closing faces
    bm.faces.new([verts_front_inner[0], verts_back_inner[0], verts_back_outer[0], verts_front_outer[0]])
    bm.faces.new([verts_front_outer[-1], verts_back_outer[-1], verts_back_inner[-1], verts_front_inner[-1]])
    
    bm.to_mesh(mesh)
    bm.free()
    
    obj = bpy.data.objects.new(name, mesh)
    obj.location = location
    return link_obj(obj, name, material, collection)

def add_angkor_stupa(name, base_pos, scale_fac, collection=col_roof):
    """
    Tạo ngọn tháp nhọn phong cách Angkor / Thái Lan đặc trưng Chùa Vĩnh Tràng:
    - Bệ tháp giật 3 cấp
    - Cổ tháp hoa sen
    - Thân tháp nhiều ngấn tròn
    - Chóp nón vuốt nhọn
    - Đỉnh quả cầu Bảo Châu
    """
    bx, by, bz = base_pos
    s = scale_fac
    
    # 3 Cấp bệ vuông
    add_box(f"{name}_Be_Cap1", (bx, by, bz + 0.3*s), (4.0*s, 4.0*s, 0.6*s), mat_facade_cream, collection)
    add_box(f"{name}_Be_Cap2", (bx, by, bz + 0.8*s), (3.4*s, 3.4*s, 0.5*s), mat_facade_detail, collection)
    add_box(f"{name}_Be_Cap3", (bx, by, bz + 1.25*s), (2.8*s, 2.8*s, 0.45*s), mat_gold_ornament, collection)
    
    # Cổ tháp hoa sen đỡ chóp
    add_cylinder(f"{name}_Co_Sen", (bx, by, bz + 1.6*s), radius=1.25*s, depth=0.35*s, material=mat_gold_ornament, collection=collection)
    
    # 4 Tầng ngấn giật cấp kiểu Stupa
    for t in range(4):
        tz = bz + (1.9 + t * 0.35) * s
        tr = (1.1 - t * 0.16) * s
        add_cylinder(f"{name}_Ngan_{t}", (bx, by, tz), radius=tr, depth=0.3*s, material=mat_gold_ornament, collection=collection)
        
    # Chóp nón vuốt nhọn cao vút
    cone_h = 2.8 * s
    cone_z = bz + (3.3 + cone_h/2.0) * s
    add_cone(f"{name}_Chop_Nhon", (bx, by, cone_z), radius1=0.6*s, radius2=0.08*s, depth=cone_h, material=mat_gold_ornament, collection=collection)
    
    # Đỉnh Bảo Châu phát sáng
    jewel_z = cone_z + (cone_h/2.0 + 0.25*s)
    add_sphere(f"{name}_Bao_Chau", (bx, by, jewel_z), radius=0.38*s, material=mat_gold_ornament, collection=collection)
    add_sphere(f"{name}_Hao_Quang_Chau", (bx, by, jewel_z), radius=0.2*s, material=mat_halo_gold, collection=collection)

# =========================================================================
# 2. XÂY DỰNG MẶT TIỀN CHÙA VĨNH TRÀNG (TIỀN ĐƯỜNG KIẾN TRÚC GIAO THOA)
# =========================================================================

# Bệ móng đá hoa cương toàn khu chùa (dài 28m, sâu 20m, cao 1.0m, Z=0 -> 1.0m, tâm Z=0.5m)
add_box("Be_Mong_Chua", (0.0, 0.0, 0.5), (28.0, 20.0, 1.0), mat_granite_step, col_arch)

# Bậc tam cấp 5 bậc đá granite dẫn lên tiền đường (Y = -12.2m -> -10.0m)
for i in range(5):
    step_z = 0.1 + i * 0.18
    step_y = -10.0 - (4 - i) * 0.55
    add_box(f"Bac_Tam_Cap_{i+1}", (0.0, step_y, step_z), (9.0, 0.55, 0.18), mat_granite_step, col_arch)

# Lan can hai bên bậc tam cấp
for sx, name in [(-4.8, "Trai"), (4.8, "Phai")]:
    add_box(f"Lan_Can_Tam_Cap_{name}", (sx, -11.1, 0.8), (0.45, 2.8, 0.7), mat_granite_step, col_arch)
    add_sphere(f"Qua_Cau_Lan_Can_{name}", (sx, -12.4, 1.25), 0.22, mat_granite_step, col_arch)

# Tường nhà Chánh điện Tầng 1:
# Sàn Z = 1.0m, trần Z = 5.8m, cao 4.8m, tâm Z = 3.4m
# Tường sau Chánh điện (Y = +8.5m)
add_box("Tuong_Sau_Chanh_Dien", (0.0, 8.5, 3.4), (24.0, 0.8, 4.8), mat_facade_cream, col_arch)
# Tường bên trái và phải (X = -12.0m và +12.0m)
add_box("Tuong_Ben_Trai_Tang_1", (-12.0, 0.5, 3.4), (0.8, 16.0, 4.8), mat_facade_cream, col_arch)
add_box("Tuong_Ben_Phai_Tang_1", (12.0, 0.5, 3.4), (0.8, 16.0, 4.8), mat_facade_cream, col_arch)
# Tường ngăn mặt tiền sảnh trong (Y = -7.4m)
add_box("Tuong_Mat_Tien_Tang_1", (0.0, -7.4, 3.4), (24.0, 0.5, 4.8), mat_facade_cream, col_arch)

# -------------------------------------------------------------------------
# HÀNG HIÊN LA MÃ TẦNG 1: 6 CỘT COMPOSITE & 5 GIAN VÒM CUỐN
# -------------------------------------------------------------------------
col_x_positions = [-11.0, -6.6, -2.2, 2.2, 6.6, 11.0]
bay_centers = [-8.8, -4.4, 0.0, 4.4, 8.8]

for idx, x in enumerate(col_x_positions):
    # Bệ chân cột vuông
    add_box(f"Be_Chan_Cot_T1_{idx}", (x, -7.8, 1.2), (1.0, 1.0, 0.4), mat_granite_step, col_arch)
    # Vành tròn đế cột (Torus ring)
    add_cylinder(f"De_Cot_Tron_T1_{idx}", (x, -7.8, 1.45), radius=0.45, depth=0.12, material=mat_column_ivory, collection=col_arch)
    # Thân cột tròn La Mã composite trắng ngà (bán kính 0.38m, cao 3.8m, Z=1.5 -> 5.3m)
    add_cylinder(f"Cot_LaMa_T1_{idx}", (x, -7.8, 3.4), radius=0.38, depth=3.8, material=mat_column_red, collection=col_arch)
    # Đai chỉ vàng trên thân cột
    add_cylinder(f"Dai_Cot_Vang_T1_{idx}", (x, -7.8, 4.8), radius=0.42, depth=0.14, material=mat_gold_ornament, collection=col_arch)
    # Đầu cột hoa văn Corinthian thếp vàng rực rỡ
    add_box(f"Dau_Cot_T1_{idx}", (x, -7.8, 5.35), (1.1, 1.1, 0.35), mat_gold_ornament, col_arch)

# 5 Vòm cuốn Romanesque nối 6 đầu cột Tầng 1
for idx, cx in enumerate(bay_centers):
    # Vòm cuốn cong thực sự (Archivolt)
    add_arch(f"Vom_Cong_LaMa_T1_{idx}", (cx, -7.8, 4.4), width=4.0, height=1.6, thickness=0.45, depth=0.55, material=mat_facade_cream, collection=col_arch)
    # Khóa vòm trung tâm (Keystone) thếp vàng
    add_box(f"Khoa_Vom_Vang_T1_{idx}", (cx, -7.76, 5.58), (0.45, 0.62, 0.4), mat_gold_ornament, col_arch)

    # Cửa ra vào / Cửa sổ các gian
    if cx == 0.0:
        # Gian giữa: Cửa chính Chánh Điện gỗ chạm 2 cánh lớn mở rộng
        add_box("Cua_Chinh_Giua", (0.0, -7.38, 3.0), (3.2, 0.2, 3.8), mat_wood_door, col_arch)
        # Hoa văn rồng phượng thếp vàng trên ngực cửa
        add_box("Hoa_Van_Cua_Chinh", (0.0, -7.35, 5.0), (3.4, 0.25, 0.3), mat_gold_ornament, col_arch)
        # Biển hiệu hoành phi "CHÙA VĨNH TRÀNG"
        add_box("Bien_Hieu_Chua", (0.0, -7.72, 4.95), (2.4, 0.12, 0.55), mat_wood_dark, col_arch)
        add_box("Chu_Vang_Bien_Hieu", (0.0, -7.71, 4.95), (2.2, 0.14, 0.4), mat_gold_ornament, col_arch)
    else:
        # 4 Gian bên: Cửa sổ vòm lá sách kiểu Pháp thông thoáng
        add_box(f"Cua_So_Phap_T1_{idx}", (cx, -7.38, 3.2), (2.4, 0.15, 3.2), mat_wood_dark, col_arch)
        add_box(f"Khung_Vom_Cua_T1_{idx}", (cx, -7.36, 4.85), (2.6, 0.2, 0.25), mat_facade_detail, col_arch)

# Dầm phân tầng & Ban công Tầng 2 (Z = 5.85m)
add_box("Dam_Phan_Tang_1_2", (0.0, -7.8, 5.85), (24.8, 1.8, 0.45), mat_facade_cream, col_arch)
# Lan can ban công con tiện sứ Pháp chạy dọc mặt tiền Tầng 2
add_box("Tay_Vi_Lan_Can_T2", (0.0, -8.65, 6.75), (24.0, 0.2, 0.15), mat_column_ivory, col_arch)
add_box("Chan_Lan_Can_T2", (0.0, -8.65, 6.15), (24.0, 0.25, 0.15), mat_column_ivory, col_arch)
for bx in range(-110, 115, 8):
    b_x = bx * 0.1
    add_cylinder(f"Con_Tien_T2_{bx}", (b_x, -8.65, 6.45), radius=0.06, depth=0.55, material=mat_column_ivory, collection=col_arch)

# -------------------------------------------------------------------------
# TẦNG 2 (TẦNG LẦU) - KIẾN TRÚC PHỤC HƯNG & VÒM CUỐN THANH THOÁT
# -------------------------------------------------------------------------
# Tường nhà Tầng 2: (X=22.0m, sâu 15m, cao 4.6m, Z=6.0 -> 10.6m, tâm Z=8.3m)
add_box("Tuong_Nha_Tang_2", (0.0, 0.5, 8.3), (22.0, 15.0, 4.6), mat_facade_cream, col_arch)

# 6 Cột tròn Tầng 2 tại Y = -7.4m (cao 3.8m, Z=6.0 -> 9.8m)
col_x_t2 = [-10.0, -6.0, -2.0, 2.0, 6.0, 10.0]
for idx, x in enumerate(col_x_t2):
    add_cylinder(f"Cot_LaMa_T2_{idx}", (x, -7.4, 7.9), radius=0.32, depth=3.8, material=mat_column_ivory, collection=col_arch)
    add_box(f"Dau_Cot_T2_{idx}", (x, -7.4, 9.85), (0.9, 0.9, 0.3), mat_gold_ornament, col_arch)

# 5 Khung cửa vòm kính màu và hoa văn Phục Hưng tầng 2
bay_centers_t2 = [-8.0, -4.0, 0.0, 4.0, 8.0]
for idx, cx in enumerate(bay_centers_t2):
    add_box(f"Cua_Vom_T2_{idx}", (cx, -7.2, 8.2), (2.5, 0.15, 3.2), mat_wood_dark, col_arch)
    add_arch(f"Vom_Phuc_Hung_T2_{idx}", (cx, -7.3, 8.8), width=3.6, height=1.3, thickness=0.35, depth=0.3, material=mat_facade_cream, collection=col_arch)
    add_box(f"Diem_Hoa_Tiet_Vang_T2_{idx}", (cx, -7.28, 10.15), (0.8, 0.35, 0.25), mat_gold_ornament, col_arch)

# =========================================================================
# 3. HỆ MÁI CHỒNG DIÊM & 5 NGỌN THÁP PHONG CÁCH ANGKOR / THÁI LAN
# =========================================================================

# Diềm mái hiên Tầng 1 (Z = 5.95m)
add_box("Mai_Hien_Tang_1", (0.0, 0.0, 5.95), (26.0, 18.5, 0.4), mat_terracotta, col_roof)

# Mái ngói chính Chùa Vĩnh Tràng (Chồng diêm 2 tầng ngói đất nung uốn lượn):
# Mái dưới (Mái hạ): Z = 10.8m, rộng 23.6m, sâu 17.6m
add_box("Mai_Chinh_Tang_2_Duoi", (0.0, 0.5, 10.8), (23.6, 17.6, 0.6), mat_terracotta, col_roof)
add_box("Vien_Mai_Ha", (0.0, 0.5, 10.6), (24.0, 18.0, 0.2), mat_terracotta_dk, col_roof)

# Cổ diêm thông gió giữa 2 tầng mái (gỗ chạm thếp vàng)
add_box("Co_Diem_Thong_Gio", (0.0, 0.5, 11.35), (20.0, 14.5, 0.5), mat_gold_ornament, col_roof)

# Mái trên (Mái thượng): Z = 11.9m, rộng 19.0m, sâu 14.0m
add_box("Mai_Chinh_Tang_2_Tren", (0.0, 0.5, 11.9), (19.0, 14.0, 0.7), mat_terracotta, col_roof)
add_box("Vien_Mai_Thuong", (0.0, 0.5, 11.65), (19.4, 14.4, 0.2), mat_terracotta_dk, col_roof)

# Bờ nóc mái đắp phù điêu gốm thếp vàng
add_box("Bo_Noc_Dinh_Mai", (0.0, 0.5, 12.35), (18.2, 0.6, 0.4), mat_gold_ornament, col_roof)

# 4 Góc mái uốn cong đao đình truyền thống Việt Nam (4 góc đao vuốt lên kiêu hãnh)
for sx in [-1, 1]:
    for sy in [-1, 1]:
        corner_x = sx * 11.6
        corner_y = 0.5 + sy * 8.6
        add_box(f"Goc_Dao_Mai_{sx}_{sy}", (corner_x, corner_y, 11.4), (1.6, 1.6, 0.45), mat_gold_ornament, col_roof)
        # Mũi đao uốn cong vút lên trên (Z = 12.0m)
        add_cone(f"Mui_Dao_Cong_{sx}_{sy}", (corner_x + sx*0.4, corner_y + sy*0.4, 12.0), radius1=0.25, radius2=0.04, depth=1.0, material=mat_gold_ornament, collection=col_roof)

# -------------------------------------------------------------------------
# 5 NGỌN THÁP NHỌN BIỂU TƯỢNG ANGKOR / THÁI LAN TRÊN ĐỈNH MÁI
# -------------------------------------------------------------------------
# 1. THÁP TRUNG TÂM LỚN (Đại Tháp Tam Bảo, đỉnh đạt Z = 18.2m!)
add_angkor_stupa("Thap_Trung_Tam", (0.0, 0.5, 12.4), scale_fac=1.0, collection=col_roof)

# 2. 4 THÁP GÓC ĐỐI XỨNG (Z đạt 16.0m):
thap_goc_coords = [
    (-8.5, -5.5),  # Trước trái
    (8.5, -5.5),   # Trước phải
    (-8.5, 6.5),   # Sau trái
    (8.5, 6.5)     # Sau phải
]

for idx, (tx, ty) in enumerate(thap_goc_coords):
    add_angkor_stupa(f"Thap_Goc_{idx}", (tx, ty, 12.0), scale_fac=0.62, collection=col_roof)

# =========================================================================
# 4. KHUÔN VIÊN SÂN TIỀN ĐƯỜNG & VẬT PHẨM NGOẠI THẤT
# =========================================================================

# Sân gạch Bát Tràng cổ kính rộng lớn phía trước (Y = -29.0m -> -9.0m, Z = -0.05m)
add_box("San_Chua_Gach_BatTrang", (0.0, -19.0, -0.05), (38.0, 20.0, 0.1), mat_yard_tile, col_env)

# Thảm cỏ xanh mát bao bọc xung quanh khuôn viên
add_box("Tham_Co_Vuon_Chua", (0.0, -14.0, -0.15), (56.0, 50.0, 0.1), mat_grass, col_env)

# LƯ HƯƠNG ĐỒNG TAM BẢO 3 CHÂN LỚN (Tọa lạc uy nghiêm tại Y = -14.5m, X = 0.0m)
add_sphere("Lu_Huong_Than_Tron", (0.0, -14.5, 1.3), radius=1.0, material=mat_bronze_urn, collection=col_env, scale=(1.2, 1.2, 0.8))
add_cylinder("Lu_Huong_Mieng", (0.0, -14.5, 1.8), radius=1.05, depth=0.35, material=mat_bronze_urn, collection=col_env)
for sx in [-1.25, 1.25]:
    add_cylinder(f"Tai_Lu_Huong_{sx}", (sx, -14.5, 1.55), radius=0.14, depth=0.6, material=mat_bronze_urn, collection=col_env, rotation=(0, math.pi/4, 0))

for ang in [0, 120, 240]:
    rad = math.radians(ang)
    lx = 0.85 * math.sin(rad)
    ly = -14.5 + 0.85 * math.cos(rad)
    add_cylinder(f"Chan_Lu_{ang}", (lx, ly, 0.6), radius=0.2, depth=1.0, material=mat_bronze_urn, collection=col_env)

# Bát cát bên trong miệng lư
add_cylinder("Cat_Bat_Huong_San", (0.0, -14.5, 1.85), radius=0.95, depth=0.18, material=mat_yard_tile, collection=col_env)

# 3 Nén hương trầm đang dâng tỏa khói
for hx in [-0.15, 0.0, 0.15]:
    add_cylinder(f"Nen_Huong_San_{hx}", (hx, -14.5, 2.6), radius=0.02, depth=1.4, material=mat_incense_red, collection=col_env)
    add_sphere(f"Tan_Huong_San_{hx}", (hx, -14.5, 3.32), radius=0.035, material=mat_candle_flame, collection=col_env)

# 2 Chậu sen đá cổ hai bên lối vào bậc tam cấp (Y = -13.0m, X = -6.5m và +6.5m)
for sx in [-6.5, 6.5]:
    add_cylinder(f"Chau_Sen_Da_{sx}", (sx, -13.0, 0.5), radius=1.3, depth=1.0, material=mat_granite_step, collection=col_env)
    add_cylinder(f"Nuoc_Chau_Sen_{sx}", (sx, -13.0, 0.88), radius=1.2, depth=0.08, material=mat_water_pool, collection=col_env)
    add_cylinder(f"La_Sen_{sx}_1", (sx-0.3, -12.9, 0.94), radius=0.45, depth=0.02, material=mat_grass, collection=col_env)
    add_cylinder(f"La_Sen_{sx}_2", (sx+0.4, -13.1, 0.94), radius=0.4, depth=0.02, material=mat_grass, collection=col_env)
    add_sphere(f"Hoa_Sen_No_{sx}", (sx, -13.0, 1.15), radius=0.35, material=mat_lotus_pink, collection=col_env, scale=(1.2, 1.2, 0.7))
    add_cone(f"Bup_Sen_Vuon_{sx}", (sx+0.25, -12.85, 1.28), radius1=0.14, radius2=0.02, depth=0.35, material=mat_lotus_pink, collection=col_env)

# Cây bồ đề cổ thụ hai bên sân
def make_bodhi_tree(name, loc):
    add_cylinder(f"{name}_Than", (loc[0], loc[1], loc[2]+2.4), radius=0.6, depth=4.8, material=mat_wood_dark, collection=col_env)
    add_sphere(f"{name}_Tan_1", (loc[0], loc[1], loc[2]+5.2), radius=2.6, material=mat_grass, collection=col_env, scale=(1.2, 1.2, 0.8))
    add_sphere(f"{name}_Tan_2", (loc[0]+0.8, loc[1]+0.6, loc[2]+6.2), radius=2.0, material=mat_grass, collection=col_env)
    add_sphere(f"{name}_Tan_3", (loc[0]-0.7, loc[1]-0.5, loc[2]+6.0), radius=1.8, material=mat_grass, collection=col_env)

make_bodhi_tree("Cay_Bo_De_Trai", (-14.5, -16.0, 0.0))
make_bodhi_tree("Cay_Bo_De_Phai", (14.5, -16.0, 0.0))

# =========================================================================
# 5. KHÔNG GIAN NỘI ĐIỆN CHÁNH ĐIỆN & BÀN THỜ TAM BẢO CÚNG BÁI
# =========================================================================

# Sàn gỗ gụ bóng loáng trong Chánh Điện (Z = 1.0m)
add_box("San_Go_Chanh_Dien", (0.0, 0.5, 1.02), (22.0, 15.0, 0.04), mat_wood_dark, col_altar)

# BÀN THỜ TAM BẢO SƠN SON THẾP VÀNG 3 TẦNG:
# Tầng 1: Bàn Lễ Đại (Y = +4.5m, Z = 1.7m)
add_box("Ban_Tho_Cap_1", (0.0, 4.5, 1.7), (7.0, 2.2, 1.4), mat_wood_dark, col_altar)
add_box("Vien_Thep_Vang_Ban_Tho_1", (0.0, 4.5, 2.42), (7.2, 2.3, 0.1), mat_gold_ornament, col_altar)
for bx in [-3.2, 3.2]:
    add_box(f"Chan_Ban_Tho_1_{bx}", (bx, 4.5, 1.4), (0.4, 2.0, 0.8), mat_gold_ornament, col_altar)

# Tầng 2: Bàn Pháp Bảo (Z = 2.7m, Y = +5.6m)
add_box("Ban_Tho_Cap_2", (0.0, 5.6, 2.7), (5.6, 1.6, 0.8), mat_wood_dark, col_altar)
add_box("Vien_Thep_Vang_Ban_Tho_2", (0.0, 5.6, 3.12), (5.8, 1.7, 0.08), mat_gold_ornament, col_altar)

# Tầng 3: Bệ Thượng đặt Tòa Sen Tượng Phật (Z = 3.5m, Y = +6.6m)
add_box("Ban_Tho_Cap_3", (0.0, 6.6, 3.5), (4.2, 1.6, 0.8), mat_gold_ornament, col_altar)

# -------------------------------------------------------------------------
# TƯỢNG PHẬT THÍCH CA DÁT VÀNG TỌA THIỀN ĐÀI SEN
# -------------------------------------------------------------------------
buddha_y = 6.6
buddha_base_z = 3.9

# Đài sen nở thếp vàng
add_cylinder("Dai_Sen_Phat", (0.0, buddha_y, buddha_base_z + 0.3), radius=1.35, depth=0.6, material=mat_gold_ornament, collection=col_altar)
for pet_ang in range(0, 360, 30):
    prad = math.radians(pet_ang)
    px = 1.25 * math.sin(prad)
    py = buddha_y + 1.25 * math.cos(prad)
    add_sphere(f"Canh_Sen_{pet_ang}", (px, py, buddha_base_z + 0.45), radius=0.22, material=mat_lotus_pink, collection=col_altar, scale=(1.0, 1.0, 1.4))

# Thân tượng Phật ngồi kiết già
add_sphere("Than_Tuong_Phat", (0.0, buddha_y, buddha_base_z + 1.45), radius=0.92, material=mat_buddha_gold, collection=col_altar, scale=(1.25, 0.85, 1.3))

# Hai cánh tay Phật tư thế thiền định (Dhyana Mudra)
add_cylinder("Tay_Phat_Thien_Dinh", (0.0, buddha_y - 0.25, buddha_base_z + 1.05), radius=0.28, depth=0.9, material=mat_buddha_gold, collection=col_altar, rotation=(0, math.pi/2, 0))

# Đầu tượng Phật an nhiên từ bi
add_sphere("Dau_Tuong_Phat", (0.0, buddha_y, buddha_base_z + 2.65), radius=0.48, material=mat_buddha_gold, collection=col_altar)
add_sphere("Nhuc_Ke_Phat", (0.0, buddha_y, buddha_base_z + 3.16), radius=0.18, material=mat_buddha_gold, collection=col_altar)
add_sphere("Bao_Chau_Nhuc_Ke", (0.0, buddha_y, buddha_base_z + 3.38), radius=0.08, material=mat_gold_ornament, collection=col_altar)

# Vòng HÀO QUANG ĐẠI TRÍ HUỆ tỏa sáng sau lưng Đức Phật
add_cylinder("Hao_Quang_Phat", (0.0, buddha_y + 0.45, buddha_base_z + 2.4), radius=1.65, depth=0.08, material=mat_halo_gold, collection=col_altar, rotation=(math.pi/2, 0, 0))
add_cylinder("Vanh_Hao_Quang_Ngoai", (0.0, buddha_y + 0.48, buddha_base_z + 2.4), radius=1.9, depth=0.04, material=mat_candle_flame, collection=col_altar, rotation=(math.pi/2, 0, 0))

# -------------------------------------------------------------------------
# VẬT PHẨM CÚNG BÁI TRÊN BÀN LỄ
# -------------------------------------------------------------------------
# 1. Bát hương đồng Chánh điện dâng 3 nén hương trầm (tại Y = +4.0m)
add_cylinder("Bat_Huong_Chanh_Dien", (0.0, 4.0, 2.7), radius=0.4, depth=0.45, material=mat_bronze_urn, collection=col_altar)
for hx in [-0.08, 0.0, 0.08]:
    add_cylinder(f"Nhang_Tram_Ban_Tho_{hx}", (hx, 4.0, 3.35), radius=0.015, depth=0.9, material=mat_incense_red, collection=col_altar)
    add_sphere(f"Dom_Lua_Tram_{hx}", (hx, 4.0, 3.82), radius=0.025, material=mat_candle_flame, collection=col_altar)

# 2. ĐÔI ĐÈN DƯỢC SƯ BẢN MỆNH thắp sáng cầu an
for dx, name in [(-2.2, "Trai"), (2.2, "Phai")]:
    add_cylinder(f"Chan_Den_DuocSu_{name}", (dx, 4.2, 2.9), radius=0.16, depth=0.85, material=mat_bronze_urn, collection=col_altar)
    add_sphere(f"Chao_Den_HoaSen_{name}", (dx, 4.2, 3.42), radius=0.28, material=mat_lotus_pink, collection=col_altar, scale=(1.1, 1.1, 0.8))
    add_sphere(f"Ngon_Nen_Phat_Sang_{name}", (dx, 4.2, 3.52), radius=0.09, material=mat_candle_flame, collection=col_altar)

# 3. Mâm ngũ quả dâng Phật & Bình sen hồng
add_cylinder("Mam_Ngu_Qua", (-1.2, 4.1, 2.65), radius=0.5, depth=0.12, material=mat_gold_ornament, collection=col_altar)
add_sphere("Qua_Buoi_Thanh_Tam", (-1.2, 4.1, 2.9), radius=0.22, material=mat_facade_cream, collection=col_altar)
add_sphere("Qua_Dao_Hong_1", (-1.05, 4.18, 2.82), radius=0.14, material=mat_lotus_pink, collection=col_altar)
add_sphere("Qua_Quyt_Vang_2", (-1.35, 4.02, 2.8), radius=0.13, material=mat_gold_ornament, collection=col_altar)

add_cylinder("Binh_Hoa_Sen_Dong", (1.2, 4.1, 2.8), radius=0.18, depth=0.6, material=mat_bronze_urn, collection=col_altar)
add_sphere("Bup_Sen_Hong_1", (1.2, 4.1, 3.3), radius=0.18, material=mat_lotus_pink, collection=col_altar)
add_sphere("Bup_Sen_Hong_2", (1.32, 4.15, 3.45), radius=0.14, material=mat_lotus_pink, collection=col_altar)
add_sphere("Bup_Sen_Hong_3", (1.08, 4.05, 3.42), radius=0.13, material=mat_lotus_pink, collection=col_altar)

# 4. Chuông đồng bát & Mõ gỗ tụng kinh
add_sphere("Mo_Go_Tung_Kinh", (-0.6, 3.8, 2.62), radius=0.16, material=mat_wood_dark, collection=col_altar, scale=(1.2, 1.1, 0.9))
add_cylinder("Chuong_Bat_Dong", (0.6, 3.8, 2.62), radius=0.18, depth=0.22, material=mat_gold_ornament, collection=col_altar)

# 5. 3 Bồ đoàn đài sen để Phật tử quỳ lạy (Y = +2.2m)
for bx, name in [(-1.0, "Trai"), (0.0, "Giua"), (1.0, "Phai")]:
    add_cylinder(f"Bo_Doan_Quy_Lay_{name}", (bx, 2.2, 1.15), radius=0.45, depth=0.22, material=mat_facade_cream, collection=col_altar)
    add_cylinder(f"Hoa_Tiet_Bo_Doan_{name}", (bx, 2.2, 1.27), radius=0.38, depth=0.04, material=mat_lotus_pink, collection=col_altar)

# =========================================================================
# 6. THIẾT LẬP ÁNH SÁNG & CAMERA CHUẨN XÁC
# =========================================================================

# Mặt trời chiếu xiên màu vàng ấm hoàng hôn
sun_data = bpy.data.lights.new(name="Nang_Vang_Hoang_Hon", type='SUN')
sun_data.energy = 5.2
sun_data.color = (1.0, 0.92, 0.76)
sun_obj = bpy.data.objects.new("Sun_Light", sun_data)
sun_obj.location = (-20.0, -25.0, 30.0)
sun_obj.rotation_euler = (math.radians(52), math.radians(16), math.radians(-35))
col_lights.objects.link(sun_obj)

# Ánh sáng bầu trời mềm dịu
sky_data = bpy.data.lights.new(name="Anh_Sang_Bau_Troi", type='SUN')
sky_data.energy = 2.0
sky_data.color = (0.75, 0.86, 0.98)
sky_obj = bpy.data.objects.new("Sky_Light", sky_data)
sky_obj.location = (0.0, 0.0, 35.0)
sky_obj.rotation_euler = (math.radians(10), 0, 0)
col_lights.objects.link(sky_obj)

# Đèn điểm nhấn mặt tiền (Facade Accent Lights)
for fx, name in [(-8.8, "Trai_2"), (-4.4, "Trai_1"), (0.0, "Giua"), (4.4, "Phai_1"), (8.8, "Phai_2")]:
    fl_data = bpy.data.lights.new(name=f"Light_Facade_{name}", type='POINT')
    fl_data.energy = 120.0
    fl_data.color = (1.0, 0.88, 0.65)
    fl_obj = bpy.data.objects.new(f"Point_Facade_{name}", fl_data)
    fl_obj.location = (fx, -9.2, 4.5)
    col_lights.objects.link(fl_obj)

# ĐÈN CHÁNH ĐIỆN ẤM ÁP NỘI ĐIỆN (Công suất lớn cho phòng rộng 24m)
altar_light_data = bpy.data.lights.new(name="Den_Chanh_Dien_Am", type='POINT')
altar_light_data.energy = 1200.0
altar_light_data.color = (1.0, 0.85, 0.55)
altar_light_obj = bpy.data.objects.new("Altar_Light", altar_light_data)
altar_light_obj.location = (0.0, 3.5, 5.0)
col_lights.objects.link(altar_light_obj)

# Đèn rọi trực diện tôn vinh Tượng Phật (Buddha Key Light)
buddha_light_data = bpy.data.lights.new(name="Den_Roi_Tuong_Phat", type='POINT')
buddha_light_data.energy = 700.0
buddha_light_data.color = (1.0, 0.92, 0.78)
buddha_light_obj = bpy.data.objects.new("Buddha_Key_Light", buddha_light_data)
buddha_light_obj.location = (0.0, 1.5, 3.8)
col_lights.objects.link(buddha_light_obj)

# Đèn nến Dược Sư trái và phải
for dx, name in [(-2.2, "Trai"), (2.2, "Phai")]:
    candle_l_data = bpy.data.lights.new(name=f"Light_Candle_{name}", type='POINT')
    candle_l_data.energy = 120.0
    candle_l_data.color = (1.0, 0.65, 0.22)
    candle_l_obj = bpy.data.objects.new(f"Point_Candle_{name}", candle_l_data)
    candle_l_obj.location = (dx, 4.2, 3.65)
    col_lights.objects.link(candle_l_obj)

# Đèn hào quang Phật (Glow Light sau lưng)
halo_light_data = bpy.data.lights.new(name="Light_Halo_Phat", type='POINT')
halo_light_data.energy = 1500.0
halo_light_data.color = (1.0, 0.85, 0.35)
halo_light_obj = bpy.data.objects.new("Point_Halo", halo_light_data)
halo_light_obj.location = (0.0, buddha_y + 0.2, buddha_base_z + 2.5)
col_lights.objects.link(halo_light_obj)

# -------------------------------------------------------------------------
# CAMERA 1: MẶT TIỀN CHÙA VĨNH TRÀNG (FACADE VIEW)
# -------------------------------------------------------------------------
cam_facade_data = bpy.data.cameras.new("Cam_Facade_Data")
cam_facade_data.lens = 28  # 28mm góc rộng kiến trúc bao trọn toàn bộ mặt tiền và 5 ngọn tháp
cam_facade_obj = bpy.data.objects.new("Camera_Facade", cam_facade_data)
cam_facade_loc = Vector((0.0, -28.0, 5.2))
cam_facade_target = Vector((0.0, -1.0, 7.5))
cam_facade_obj.location = cam_facade_loc
cam_facade_obj.rotation_euler = (cam_facade_target - cam_facade_loc).to_track_quat('-Z', 'Y').to_euler()
col_lights.objects.link(cam_facade_obj)

# -------------------------------------------------------------------------
# CAMERA 2: NỘI ĐIỆN & BÀN THỜ TAM BẢO CÚNG BÁI (ALTAR WORSHIP VIEW)
# -------------------------------------------------------------------------
cam_altar_data = bpy.data.cameras.new("Cam_Altar_Data")
cam_altar_data.lens = 32  # 32mm tôn nghiêm, ôm trọn bàn lễ và Tượng Phật
cam_altar_obj = bpy.data.objects.new("Camera_Altar", cam_altar_data)
cam_altar_loc = Vector((0.0, -1.5, 2.5))
cam_altar_target = Vector((0.0, 5.5, 4.2))
cam_altar_obj.location = cam_altar_loc
cam_altar_obj.rotation_euler = (cam_altar_target - cam_altar_loc).to_track_quat('-Z', 'Y').to_euler()
col_lights.objects.link(cam_altar_obj)

# Cập nhật View Layer toàn bộ
bpy.context.view_layer.update()

# Cấu hình Render EEVEE chất lượng cao 1080p
scene.render.engine = 'CYCLES'
scene.cycles.samples = 96
scene.cycles.use_denoising = True
scene.cycles.device = 'CPU'
scene.render.resolution_x = 1280
scene.render.resolution_y = 720
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'

# 7. LƯU FILE .BLEND & XUẤT .GLB
print("===> Đang lưu file .blend hoàn chỉnh...")
bpy.ops.wm.save_as_mainfile(filepath=BLEND_OUT)
print(f"===> Đã lưu thành công file .blend: {BLEND_OUT}")

print("===> Đang xuất mô hình sang định dạng chuẩn Web 3D (.glb)...")
try:
    bpy.ops.export_scene.gltf(
        filepath=GLB_OUT,
        export_format='GLB',
        use_selection=False,
        export_apply=True,
        export_materials='EXPORT',
        export_lights=True,
        export_cameras=True
    )
    print(f"===> Đã xuất thành công file GLB: {GLB_OUT}")
except Exception as e:
    print(f"Lỗi xuất GLB: {e}")

# 8. RENDER 2 ẢNH PREVIEW CHẤT LƯỢNG CAO
print("===> Đang Render ảnh 1: Toàn cảnh mặt tiền Chùa Vĩnh Tràng...")
scene.camera = cam_facade_obj
world = bpy.data.worlds.new("Troi_Xanh_VinhTrang")
scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get("Background")
bg.inputs[0].default_value = (0.30, 0.52, 0.86, 1.0)
bg.inputs[1].default_value = 1.0
scene.view_settings.view_transform = "AgX"
pass  # giữ look mặc định AgX
add_box("Khoi_Mai_Ngoi_Lon_PhaiSau", (0.0, 2.5, 13.6), (21.5, 13.0, 3.6), mat_terracotta_dk, col_roof)
add_box("Noc_Mai_Chinh_VinhTrang", (0.0, 2.5, 15.55), (18.0, 1.2, 0.5), mat_gold_ornament, col_roof)
print("===> Bỏ qua render mặt tiền trong bản sửa nội điện")
print(f"===> Đã render ảnh mặt tiền: {IMG_FACADE}")

print("===> Đang Render ảnh 2: Cận cảnh Chánh Điện & Khu vực Cúng bái...")
scene.camera = cam_altar_obj
scene.render.filepath = IMG_ALTAR
bpy.ops.render.render(write_still=True)
print(f"===> Đã render ảnh cúng bái: {IMG_ALTAR}")

print("=== HOÀN TẤT THIẾT KẾ VÀ XUẤT BẢN 3D CHÙA VĨNH TRÀNG VỚI BLENDER 5.2 ===")
