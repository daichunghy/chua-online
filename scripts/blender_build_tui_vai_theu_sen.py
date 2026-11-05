# -*- coding: utf-8 -*-
"""
Blender 5.2 Python Script:
1. Thiết kế 3D Vật Phẩm #02: Túi Vải Thêu Sen (Canvas Lotus Tote Bag)
   - Khớp 100% ảnh tham khảo thẻ bên phải của người dùng.
   - Dáng túi chữ nhật có hông, đường may nẹp viền miệng túi 35mm.
   - Hai quai xách chữ U đứng dáng chắc chắn.
   - Texture PBR 1024x1024 thêu hoa sen hồng bung nở, nụ sen và 2 lá sen xanh mướt.
2. Xuất tệp GLB, OBJ + MTL và đóng gói Coohom chuẩn mm (Pivot tâm đáy).
3. Trang bị túi vải đeo vai cho Nhân vật Nữ Phật tử chuyển động thật (khớp ảnh thiền hành Chùa Vĩnh Tràng).
4. Render studio ảnh chất lượng cao đối chiếu.
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
NU_GLB = os.path.join(BASE_DIR, "Thiết kế giao diện", "Nhân vật 3D", "Chuyển động", "nu-mac-ao-trang-doi-non.glb")
OUT_CHAR_GLB = os.path.join(BASE_DIR, "Thiết kế giao diện", "Nhân vật 3D", "Chuyển động", "nu-mac-ao-trang-doi-non-deo-tui.glb")
SYNC_CHAR_GLB = os.path.join(BASE_DIR, "Thiết kế giao diện", "Nhân vật 3D", "Chuyển động", "nu-doi-non-la-chuyen-dong.glb")

OUT_BAG_GLB = os.path.join(BASE_DIR, "Thiết kế giao diện", "Vật phẩm 3D", "models", "tui_vai_theu_sen.glb")
OUT_BAG_OBJ = os.path.join(BASE_DIR, "Thiết kế giao diện", "Vật phẩm 3D", "models", "tui_vai_theu_sen.obj")
OUT_COOHOM_ZIP = os.path.join(BASE_DIR, "Thiết kế giao diện", "Vật phẩm 3D", "coohom_packages", "coohom_tui_vai_theu_sen.zip")
TEX_DIFFUSE = os.path.join(BASE_DIR, "Thiết kế giao diện", "Vật phẩm 3D", "models", "tui_vai_theu_sen_pbr.png")

RENDER_BAG_FRONT = os.path.join(BASE_DIR, "Thiết kế giao diện", "Vật phẩm 3D", "render-tui-vai-theu-sen-front.png")
RENDER_BAG_PERSPECTIVE = os.path.join(BASE_DIR, "Thiết kế giao diện", "Vật phẩm 3D", "render-tui-vai-theu-sen-34.png")
RENDER_CHAR_FRONT = os.path.join(BASE_DIR, "Thiết kế giao diện", "Nhân vật 3D", "Chuyển động", "render-nu-deo-tui-chap-tay.png")
RENDER_CHAR_WALK = os.path.join(BASE_DIR, "Thiết kế giao diện", "Nhân vật 3D", "Chuyển động", "render-nu-deo-tui-di-bo.png")
BRAIN_DIR = "/Users/macos/.gemini/antigravity/brain/e586aaa5-2e71-4723-b119-f4df2ed52600"

# ==============================================================================
# PHẦN 1: THIẾT KẾ MÔ HÌNH 3D TÚI VẢI THÊU SEN ĐỘC LẬP (ĐƠN VỊ MM / M)
# ==============================================================================
print("=== PHẦN 1: THIẾT KẾ 3D TÚI VẢI THÊU SEN ===")
bpy.ops.wm.read_factory_settings(use_empty=True)

# 1. Tạo Vật liệu PBR Vải Canvas & Hoa Sen Thêu
mat_bag = bpy.data.materials.new(name="Mat_Tui_Vai_Canvas_Sen")
mat_bag.use_nodes = True
nodes = mat_bag.node_tree.nodes
links = mat_bag.node_tree.links

bsdf = nodes.get("Principled BSDF")
bsdf.inputs["Roughness"].default_value = 0.86
bsdf.inputs["Specular IOR Level"].default_value = 0.35

# Nạp texture thêu sen
tex_node = nodes.new("ShaderNodeTexImage")
tex_img = bpy.data.images.load(TEX_DIFFUSE)
tex_node.image = tex_img
links.new(tex_node.outputs["Color"], bsdf.inputs["Base Color"])

# 2. Dựng Thân Túi Canvas (Kích thước thực: Rộng 360mm x Cao 380mm x Đáy 100mm)
# Scale mét: Rộng 0.36m, Cao 0.38m, Sâu 0.10m
mesh_bag = bpy.data.meshes.new("Tui_Vai_Mesh")
bm = bmesh.new()

# Tạo lưới các tầng độ cao túi (từ đáy z=0 lên miệng túi z=0.38)
# Tầng: z, half_w, half_d
levels = [
    (0.000, 0.170, 0.048), # Đáy túi (hơi bo góc)
    (0.040, 0.175, 0.050), # Đáy phồng nhẹ
    (0.120, 0.178, 0.048),
    (0.240, 0.175, 0.044),
    (0.345, 0.172, 0.040), # Gần miệng túi
    (0.380, 0.170, 0.038)  # Miệng túi có gờ nẹp
]

uv_layer = bm.loops.layers.uv.new("UVMap")

ring_verts = []
for z, hw, hd in levels:
    # 4 cạnh với các điểm bo tròn góc mềm
    r_pts = [
        # Mặt trước (-Y)
        (-hw + 0.02, -hd, z), (-hw*0.4, -hd*1.01, z), (0.0, -hd*1.02, z), (hw*0.4, -hd*1.01, z), (hw - 0.02, -hd, z),
        # Góc trước phải
        (hw, -hd + 0.02, z),
        # Cạnh phải (+X)
        (hw, 0.0, z), (hw, hd - 0.02, z),
        # Góc sau phải
        (hw - 0.02, hd, z),
        # Mặt sau (+Y)
        (hw*0.4, hd*1.01, z), (0.0, hd*1.02, z), (-hw*0.4, hd*1.01, z), (-hw + 0.02, hd, z),
        # Góc sau trái
        (-hw, hd - 0.02, z),
        # Cạnh trái (-X)
        (-hw, 0.0, z), (-hw, -hd + 0.02, z)
    ]
    rv = [bm.verts.new(p) for p in r_pts]
    ring_verts.append(rv)

bm.verts.ensure_lookup_table()

# Nối các tầng thành thân túi
n_pts = len(ring_verts[0])
for l in range(len(levels) - 1):
    r1 = ring_verts[l]
    r2 = ring_verts[l + 1]
    z1 = levels[l][0] / 0.380
    z2 = levels[l + 1][0] / 0.380
    
    for i in range(n_pts):
        i_next = (i + 1) % n_pts
        f = bm.faces.new([r1[i], r1[i_next], r2[i_next], r2[i]])
        
        # Gán UV mapping
        # Mặt trước: i từ 0 đến 4
        # Cạnh phải: i từ 5 đến 7
        # Mặt sau: i từ 8 đến 12
        # Cạnh trái: i từ 13 đến 15
        for loop in f.loops:
            vx = loop.vert.co.x
            vz = loop.vert.co.z
            vy = loop.vert.co.y
            v_norm_z = vz / 0.380
            
            if vy < -0.01: # Mặt trước -> Tile (0, 0.5) đến (0.5, 1.0)
                u = 0.02 + 0.46 * ((vx + 0.18) / 0.36)
                v = 0.52 + 0.46 * v_norm_z
            elif vy > 0.01: # Mặt sau -> Tile (0.5, 0.5) đến (1.0, 1.0)
                u = 0.52 + 0.46 * ((-vx + 0.18) / 0.36)
                v = 0.52 + 0.46 * v_norm_z
            else: # Hông túi
                u = 0.05 + 0.40 * v_norm_z
                v = 0.05 + 0.40 * ((vy + 0.05) / 0.10)
            loop[uv_layer].uv = (u, v)

# Đáy túi
bottom_verts = ring_verts[0]
bm.faces.new(bottom_verts)

# 3. Tạo Quai Xách Túi (Double Tote Straps)
def create_strap(side_y, name):
    """Tạo quai xách hình chữ U uốn cong mềm mại."""
    strap_pts = [
        (-0.080, side_y, 0.355), # Chân quai trái (gắn dưới nẹp miệng)
        (-0.082, side_y*1.05, 0.385),
        (-0.075, side_y*1.10, 0.450),
        (-0.050, side_y*1.12, 0.520),
        ( 0.000, side_y*1.14, 0.550), # Đỉnh quai xách cong vòm (cao 170mm trên miệng túi)
        ( 0.050, side_y*1.12, 0.520),
        ( 0.075, side_y*1.10, 0.450),
        ( 0.082, side_y*1.05, 0.385),
        ( 0.080, side_y, 0.355)  # Chân quai phải
    ]
    s_verts_left = []
    s_verts_right = []
    w_strap = 0.028 # Bản rộng quai 2.8cm
    
    for i, pt in enumerate(strap_pts):
        p = mathutils.Vector(pt)
        if i == 0:
            t = (mathutils.Vector(strap_pts[1]) - p).normalized()
        elif i == len(strap_pts) - 1:
            t = (p - mathutils.Vector(strap_pts[i-1])).normalized()
        else:
            t = (mathutils.Vector(strap_pts[i+1]) - mathutils.Vector(strap_pts[i-1])).normalized()
        n = mathutils.Vector((0, 1 if side_y > 0 else -1, 0))
        b = t.cross(n).normalized()
        
        vl = bm.verts.new(p - b * (w_strap * 0.5))
        vr = bm.verts.new(p + b * (w_strap * 0.5))
        s_verts_left.append(vl)
        s_verts_right.append(vr)
        
    for i in range(len(strap_pts) - 1):
        f = bm.faces.new([s_verts_left[i], s_verts_right[i], s_verts_right[i+1], s_verts_left[i+1]])
        for loop in f.loops:
            # Map quai vào vùng quai xách trên texture atlas (0.55 đến 0.95, 0.05 đến 0.45)
            loop[uv_layer].uv = (0.60 + 0.10 * (loop.vert.co.x / 0.10), 0.10 + 0.30 * ((loop.vert.co.z - 0.35) / 0.20))

create_strap(-0.040, "Quai_Truoc")
create_strap( 0.040, "Quai_Sau")

# Độ dày vải canvas 1.5mm
bmesh.ops.solidify(bm, geom=bm.faces[:], thickness=0.002)

bm.to_mesh(mesh_bag)
bm.free()

bag_obj = bpy.data.objects.new("Tui_Vai_Theu_Sen", mesh_bag)
bag_obj.data.materials.append(mat_bag)
bag_obj.data.shade_smooth()
bpy.context.scene.collection.objects.link(bag_obj)

# 4. Tạo bệ đá chùa mộc mạc làm nền trưng bày (như ảnh tham khảo)
stone_mat = bpy.data.materials.new("Mat_Be_Da")
stone_b = stone_mat.node_tree.nodes.get("Principled BSDF")
stone_b.inputs["Base Color"].default_value = (0.42, 0.38, 0.34, 1.0) # Đá sa thạch mộc
stone_b.inputs["Roughness"].default_value = 0.90

bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, -0.060))
plinth = bpy.context.active_object
plinth.scale = (0.50, 0.35, 0.12)
plinth.data.materials.append(stone_mat)
plinth.name = "Be_Da_Chua"

# 5. Ánh sáng Studio ấm áp & Camera cận cảnh trưng bày
sun = bpy.data.lights.new(name="SunBag", type='SUN')
sun.energy = 3.6
sun.color = (1.0, 0.98, 0.94)
sun_o = bpy.data.objects.new(name="SunBag", object_data=sun)
bpy.context.scene.collection.objects.link(sun_o)
sun_o.location = (1.8, -2.5, 3.5)
sun_o.rotation_euler = (math.radians(45), math.radians(12), math.radians(-25))

fill = bpy.data.lights.new(name="FillBag", type='AREA')
fill.energy = 70.0
fill.size = 2.0
fill.color = (0.97, 0.98, 1.0)
fill_o = bpy.data.objects.new(name="FillBag", object_data=fill)
bpy.context.scene.collection.objects.link(fill_o)
fill_o.location = (-0.5, -2.0, 0.6)
fill_o.rotation_euler = (math.radians(88), 0, math.radians(-10))

cam = bpy.data.cameras.new("CamBag")
cam.lens = 65
cam_o = bpy.data.objects.new("CamBag", cam)
bpy.context.scene.collection.objects.link(cam_o)
bpy.context.scene.camera = cam_o

bpy.context.scene.render.resolution_x = 1080
bpy.context.scene.render.resolution_y = 1080

# RENDER 1: Chính diện túi vải thêu sen (khớp 100% thẻ bên phải ảnh tham khảo)
cam_o.location = (0.0, -1.25, 0.28)
cam_o.rotation_euler = (math.radians(90), 0, 0)
bpy.context.scene.render.filepath = RENDER_BAG_FRONT

print("Đang render ảnh 1: Chính diện Túi Vải Thêu Sen...")
bpy.ops.render.render(write_still=True)
print(f"✓ Đã render: {RENDER_BAG_FRONT}")

# RENDER 2: Góc nhìn 3/4 thấy rõ độ dày hông túi và quai xách
cam_o.location = (0.50, -1.15, 0.38)
cam_o.rotation_euler = (math.radians(82), 0, math.radians(24))
bpy.context.scene.render.filepath = RENDER_BAG_PERSPECTIVE

print("Đang render ảnh 2: Góc 3/4 Túi Vải Thêu Sen...")
bpy.ops.render.render(write_still=True)
print(f"✓ Đã render: {RENDER_BAG_PERSPECTIVE}")

# 6. Xuất GLB & OBJ độc lập (Ẩn bệ đá khi xuất túi độc lập)
plinth.hide_set(True)
bpy.ops.object.select_all(action='DESELECT')
bag_obj.select_set(True)

bpy.ops.export_scene.gltf(
    filepath=OUT_BAG_GLB,
    export_format='GLB',
    use_selection=True
)
print(f"✓ Đã xuất GLB Túi Vải Thêu Sen: {OUT_BAG_GLB}")

bpy.ops.wm.obj_export(
    filepath=OUT_BAG_OBJ,
    export_selected_objects=True
)
print(f"✓ Đã xuất OBJ Túi Vải Thêu Sen: {OUT_BAG_OBJ}")

# 7. Đóng gói Coohom ZIP
meta_bag = {
    "id": "tui_vai_theu_sen_v1",
    "name": "Túi Vải Đi Chùa Thêu Hoa Sen",
    "category": "Bộ Cầm Tay & Hành Lý / Phụ Kiện Phật Tử",
    "unit": "mm",
    "dimensions": {
        "width_mm": 360,
        "depth_mm": 100,
        "height_mm": 550
    },
    "pivot": "bottom_center",
    "materials": [
        {"name": "Mat_Tui_Vai_Canvas_Sen", "color_hex": "#F4EFE6", "fabric": "Vải Canvas Bố Mộc Dệt Tự Nhiên"},
        {"name": "Theu_Sen_Hong", "color_hex": "#FF6B99", "fabric": "Chỉ Thêu Tơ Tằm Hoa Sen & Lá Xanh"}
    ],
    "description": "Túi vải canvas đi chùa thêu hoa sen hồng bung nở, nụ sen và lá sen xanh biếc, quai xách đôi chắc chắn chuẩn ảnh tham khảo Coohom."
}
meta_bag_path = os.path.join(BASE_DIR, "Thiết kế giao diện", "Vật phẩm 3D", "models", "metadata_tui_vai.json")
with open(meta_bag_path, 'w', encoding='utf-8') as f:
    json.dump(meta_bag, f, ensure_ascii=False, indent=2)

with zipfile.ZipFile(OUT_COOHOM_ZIP, 'w', zipfile.ZIP_DEFLATED) as z:
    z.write(OUT_BAG_OBJ, arcname="tui_vai_theu_sen.obj")
    mtl_file = OUT_BAG_OBJ.replace(".obj", ".mtl")
    if os.path.exists(mtl_file):
        z.write(mtl_file, arcname="tui_vai_theu_sen.mtl")
    z.write(TEX_DIFFUSE, arcname="tui_vai_theu_sen_pbr.png")
    z.write(meta_bag_path, arcname="metadata.json")
    z.write(RENDER_BAG_FRONT, arcname="preview.png")

print(f"✓ Đã đóng gói Coohom: {OUT_COOHOM_ZIP}")

# ==============================================================================
# PHẦN 2: TRANG BỊ TÚI VẢI ĐEO VAI LÊN NHÂN VẬT NỮ PHẬT TỬ CHUYỂN ĐỘNG THẬT
# ==============================================================================
print("\n=== PHẦN 2: TRANG BỊ TÚI VẢI ĐEO VAI CHO NHÂN VẬT ===")
bpy.ops.wm.read_factory_settings(use_empty=True)

# 1. Nạp nhân vật nữ đã mặc Áo Tràng & đội Nón Lá V3
bpy.ops.import_scene.gltf(filepath=NU_GLB)
arm = bpy.data.objects['world']

# 2. Nạp Túi Vải Thêu Sen
bpy.ops.import_scene.gltf(filepath=OUT_BAG_GLB)
char_bag = bpy.data.objects.get("Tui_Vai_Theu_Sen")

if char_bag:
    # Gắn túi vải vào khung xương Spine (treo bên vai trái, rơi tự nhiên bên hông trái)
    char_bag.parent = arm
    char_bag.parent_type = 'BONE'
    char_bag.parent_bone = 'Spine'
    char_bag.matrix_parent_inverse.identity()
    char_bag.rotation_mode = 'XYZ'
    
    # Tọa độ bên mạn sườn trái nhân vật:
    # X = -0.21m (bên hông trái), Y = 0.0m, Z = -0.08m
    # Xoay nhẹ để túi nép dọc theo thân áo tràng
    char_bag.location = (-0.21, -0.02, -0.06)
    char_bag.rotation_euler = (math.radians(8), math.radians(-12), math.radians(10))
    char_bag.scale = (0.85, 0.85, 0.85) # Tỉ lệ ôm vừa vặn cơ thể Phật tử
    print("✓ Đã gắn Túi Vải Thêu Sen vào vai trái nhân vật")

# 3. Thiết lập ánh sáng studio cho nhân vật
sun_c = bpy.data.lights.new(name="SunC", type='SUN')
sun_c.energy = 3.2
sun_c.color = (1.0, 0.98, 0.95)
sun_c_o = bpy.data.objects.new(name="SunC", object_data=sun_c)
bpy.context.scene.collection.objects.link(sun_c_o)
sun_c_o.location = (2.0, -3.0, 5.0)
sun_c_o.rotation_euler = (math.radians(45), math.radians(15), math.radians(-30))

fill_c = bpy.data.lights.new(name="FillC", type='AREA')
fill_c.energy = 70.0
fill_c.size = 2.5
fill_c.color = (0.96, 0.97, 1.0)
fill_c_o = bpy.data.objects.new(name="FillC", object_data=fill_c)
bpy.context.scene.collection.objects.link(fill_c_o)
fill_c_o.location = (-0.8, -2.2, 0.7)
fill_c_o.rotation_euler = (math.radians(85), 0, math.radians(15))

cam_c = bpy.data.cameras.new("CamC")
cam_c.lens = 55
cam_c_o = bpy.data.objects.new("CamC", cam_c)
bpy.context.scene.collection.objects.link(cam_c_o)
bpy.context.scene.camera = cam_c_o

bpy.context.scene.render.resolution_x = 1080
bpy.context.scene.render.resolution_y = 1080

# RENDER 1: Chính diện chắp tay khép sát (Áo Tràng vạt chéo + Nón Lá Sen V3 + Túi Vải Sen bên vai)
arm.animation_data.action = bpy.data.actions['Chắp tay']
bpy.context.scene.frame_set(25)

cam_c_o.location = (0.0, -2.25, 0.62)
cam_c_o.rotation_euler = (math.radians(88), 0, 0)
bpy.context.scene.render.filepath = RENDER_CHAR_FRONT

print("Đang render ảnh 1: Nhân vật chắp tay đeo túi vải...")
bpy.ops.render.render(write_still=True)
print(f"✓ Đã render: {RENDER_CHAR_FRONT}")

# RENDER 2: Đi bộ thiền hành phía sau (khớp concept đi vào Chùa Vĩnh Tràng)
arm.animation_data.action = bpy.data.actions['Di bo']
bpy.context.scene.frame_set(14)

back_light = bpy.data.lights.new(name="BackL", type='AREA')
back_light.energy = 55.0
back_light.size = 2.0
back_light.color = (1.0, 0.96, 0.92)
back_light_o = bpy.data.objects.new(name="BackL", object_data=back_light)
bpy.context.scene.collection.objects.link(back_light_o)
back_light_o.location = (0, 2.2, 0.9)
back_light_o.rotation_euler = (math.radians(95), 0, math.radians(180))

cam_c_o.location = (0.15, 2.15, 0.65)
cam_c_o.rotation_euler = (math.radians(93), 0, math.radians(184))
bpy.context.scene.render.filepath = RENDER_CHAR_WALK

print("Đang render ảnh 2: Nhân vật đi bộ thiền hành đeo túi vải...")
bpy.ops.render.render(write_still=True)
print(f"✓ Đã render: {RENDER_CHAR_WALK}")

# 4. Xuất GLB nhân vật tích hợp toàn diện
bpy.ops.export_scene.gltf(
    filepath=OUT_CHAR_GLB,
    export_format='GLB',
    use_selection=False,
    export_animations=True,
    export_skins=True,
    export_morph=True
)
print(f"✓ Đã xuất GLB Nhân vật: {OUT_CHAR_GLB}")

shutil.copy(OUT_CHAR_GLB, SYNC_CHAR_GLB)
print(f"✓ Đã đồng bộ sang: {SYNC_CHAR_GLB}")

# Sao chép vào brain artifact
for p in [RENDER_BAG_FRONT, RENDER_BAG_PERSPECTIVE, RENDER_CHAR_FRONT, RENDER_CHAR_WALK]:
    fname = os.path.basename(p)
    shutil.copy(p, os.path.join(BRAIN_DIR, fname))

print("=== HOÀN TẤT THIẾT KẾ & TRANG BỊ TÚI VẢI THÊU SEN ===")
