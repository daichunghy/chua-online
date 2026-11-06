"""
LAYOUT V3 — bố cục tổng thể Vĩnh Tràng bằng tài sản thật.
Base: repo khuon-vien-chanh-dien-moi.blend (mặt tiền chi tiết + tháp 7 tầng + bệ tượng
+ sân/vườn/cây, cùng hệ tọa độ với bo-cuc-theo-anh.blend: mặt tiền tâm x=23).
Ghép thêm từ repo khuon-vien-vinh-trang.blend (cùng mẫu, mặt tiền tâm x=0 → dịch +23 X):
cổng tam quan x2, 2 hồ cảnh + bờ hồ, đường chính.
Tượng: statues/verified_v2/*.glb. Vật phẩm: repo-items/fixed/*.glb (đã kiểm chứng).
Nhân vật: characters_fitted/*.glb (nón/túi/tràng hạt/hoa sen/khăn đã fit, pose Chắp tay).
Mái chánh điện: repo KHÔNG có khối mái lớn thật ('Mái ngói phía sau' chỉ là 3 dải phẳng
0,96m ở mặt đất, đã xóa) → dựng mái hông (hip roof) có độ dốc + hàng ngói trong script
này, chỉ để phục vụ góc flycam; mặt tiền (góc mặt đất) không thấy mái này.
KHÔNG render trong script này — lưu .blend rồi render riêng (mỗi lần 1 render).
"""
import bpy, math, os
from mathutils import Vector

W = "/home/hatch/workspace/chua-online-work/"
BASE = W + "repo-khuonvienchanhdienmoi.blend"
GATE_SRC = W + "repo-khuonvienvinhtrang.blend"
OUT = W + "layout_v3.blend"

bpy.ops.wm.open_mainfile(filepath=BASE)
sc = bpy.context.scene
print("LAYOUT BUILD: base =", BASE)

# ---------- 1. Xóa dải mái hỏng ở mặt đất ----------
for n in ('Mái ngói phía sau', 'Mái ngói phía sau.001', 'Mái ngói phía sau.002',
          'Mái tam giác trung tâm'):
    o = bpy.data.objects.get(n)
    if o:
        bpy.data.objects.remove(o, do_unlink=True)
        print("removed degenerate roof strip:", n)

# ---------- 2. Nhuộm vàng mặt tiền theo bảng facade V3 ----------
def recolor(mat_name, rgb):
    m = bpy.data.materials.get(mat_name)
    if not m or not m.use_nodes: return
    bs = next((n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
    if bs: bs.inputs['Base Color'].default_value = (*rgb, 1.0)
GOLD = (1.0, 0.60, 0.02)
for n in ('Ngà sáng', 'Chỉ trắng ngà', 'Vữa màu vàng kem', 'Vàng trang trí'):
    recolor(n, GOLD)
recolor('Màu vàng đất', (0.88, 0.52, 0.06))
recolor('Vàng kem', (1.0, 0.66, 0.10))
recolor('Trắng', (0.96, 0.92, 0.82))
recolor('Đỏ gạch', (0.45, 0.13, 0.06))
# Giữ: 'Vàng tường' (tường/tháp màu đào), 'Gốm xanh', 'Mái ngói', 'Đỏ son', 'Cửa tối'

# ---------- 3. Ghép cổng + hồ + đường từ file khuôn viên cũ (dịch +23 X) ----------
SHIFT_X = 23.0
GATE_BASES = ('Trụ cổng', 'Vòm cổng', 'Chóp cổng', 'Tầng mái cổng', 'Châu cổng',
              'Mảng gốm cổng', 'Chỉ ngang cổng', 'Trụ tầng trên cổng')
POND_BASES = ('Hồ cảnh', 'Bờ hồ')
with bpy.data.libraries.load(GATE_SRC) as (df, dt):
    lib_names = list(df.objects)
print("library objects:", len(lib_names))
import re
def base_of(n): return re.sub(r'\.\d+$', '', n)
gate_names = [n for n in lib_names if base_of(n) in GATE_BASES]
pond_names = [n for n in lib_names if base_of(n) in POND_BASES]
road_names = [n for n in lib_names if n == 'Đường chính']
print(f"appending gate={len(gate_names)} pond={len(pond_names)} road={len(road_names)}")
bpy.ops.wm.append(filepath=os.path.join(GATE_SRC, "Object", ""),
                 directory=os.path.join(GATE_SRC, "Object") + "/",
                 files=[{"name": n} for n in gate_names + pond_names + road_names],
                 link=False)
appended = []
for n in gate_names + pond_names + road_names:
    o = bpy.data.objects.get(n)
    if o:
        o.location.x += SHIFT_X
        appended.append(o)
print("appended+shifted:", len(appended))
# Hồ nổi trên sân (tránh z-fight: mặt nước -0,04 = mặt sân -0,04)
for n in ('Hồ cảnh', 'Hồ cảnh.001'):
    o = bpy.data.objects.get(n)
    if o: o.location.z += 0.08
for o in bpy.data.objects:
    if o.name.startswith('Bờ hồ'):
        o.location.z += 0.05
# Cổng thứ 2 ở đầu phải phía trước (như ảnh thật: 2 cổng tam quan)
gate_objs = [bpy.data.objects.get(n) for n in gate_names]
gate_objs = [o for o in gate_objs if o]
bpy.ops.object.select_all(action='DESELECT')
for o in gate_objs: o.select_set(True)
bpy.context.view_layer.objects.active = gate_objs[0]
bpy.ops.object.duplicate()
for o in bpy.context.selected_objects:
    o.location.x += 22.0   # cổng 2 tại x = 23 + 22 = 45, y = -39
print("second gate duplicated at x=45")

# ---------- 4. Mái hông chánh điện (hip roof) ----------
# Chân mái z=6.5 (viền mái trên), đỉnh dọc X tại y=7, z=11.5; bao x 8..38, y -3.5..+18.
roof_mat = bpy.data.materials.new("Mai_Ngoi_Layout"); roof_mat.use_nodes = True
roof_mat.node_tree.nodes["Principled BSDF"].inputs['Base Color'].default_value = (0.36, 0.13, 0.07, 1)
row_mat = bpy.data.materials.new("Mai_Ngoi_Hang"); row_mat.use_nodes = True
row_mat.node_tree.nodes["Principled BSDF"].inputs['Base Color'].default_value = (0.28, 0.10, 0.05, 1)
import bmesh
def build_roof():
    me = bpy.data.meshes.new("Mai_Chinh_Dien")
    bm = bmesh.new()
    # eave rect corners (z=6.5) + ridge ends (z=11.5, y=7)
    A = bm.verts.new((8, -3.5, 6.5));  B = bm.verts.new((38, -3.5, 6.5))
    C = bm.verts.new((38, 18, 6.5));   D = bm.verts.new((8, 18, 6.5))
    R1 = bm.verts.new((13, 7, 11.5));  R2 = bm.verts.new((33, 7, 11.5))
    bm.verts.ensure_lookup_table()
    bm.faces.new((A, B, R2, R1))   # front slope (faces -Y)
    bm.faces.new((D, R1, R2, C))   # back slope (faces +Y)
    bm.faces.new((A, R1, D))       # west hip
    bm.faces.new((B, C, R2))       # east hip
    bm.faces.new((A, D, C, B))     # underside
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new("Mai_Chinh_Dien", me)
    sc.collection.objects.link(o)
    me.materials.append(roof_mat)
    return o
build_roof()
# Ridge beam along X
bpy.ops.mesh.primitive_cube_add(size=1, location=(23, 7, 11.65))
o = bpy.context.object; o.name = "Noc_Mai_Chinh_Dien"; o.dimensions = (21.0, 0.7, 0.5)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
o.data.materials.append(row_mat)
# Tile courses on the front slope (proud thin boxes following the slope)
# front slope: from (y=-3.5,z=6.5) to (y=7,z=11.5): angle atan(5/10.5)=25.5 deg
ang = math.atan2(5.0, 10.5)
for i in range(7):
    t = (i + 0.5) / 7.0
    y = -3.5 + t * 10.5
    z = 6.5 + t * 5.0 + 0.12
    bpy.ops.mesh.primitive_cube_add(size=1, location=(23, y, z))
    r = bpy.context.object; r.name = f"Hang_Ngoi_Truoc_{i}"
    # Rows OVERLAP (width 1.7 > spacing 1.5): from a low angle the gaps
    # between separate rows show sky over the ridge; overlapping rows read
    # as shingle courses from both flycam and ground.
    r.dimensions = (30.0, 1.7, 0.10)
    r.rotation_euler = (ang, 0, 0)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    r.data.materials.append(row_mat)
print("roof built")

# ---------- 4b. Xóa mặt phẳng studio 'Ground*' do GLB tượng/vật phẩm mang theo ----------
# (chúng nằm ở z~0-2.8 và che toàn bộ mặt đất/hồ/sân; phát hiện bằng raycast 06/11)
for o in list(bpy.data.objects):
    if o.name.lower().startswith(('ground', 'floor', 'backdrop', 'studio')):
        print("removed studio junk:", o.name)
        bpy.data.objects.remove(o, do_unlink=True)

# ---------- 5. Nền đất rộng dưới toàn khu (tránh khoảng trống ngoài khuôn viên) ----------
bpy.ops.mesh.primitive_plane_add(size=600, location=(0, 10, -0.45))
g = bpy.context.object; g.name = "Nen_Dat_Rong"
gm = bpy.data.materials.new("Dat_Co"); gm.use_nodes = True
gm.node_tree.nodes["Principled BSDF"].inputs['Base Color'].default_value = (0.24, 0.33, 0.18, 1)
g.data.materials.append(gm)

# ---------- 6. Tượng ----------
def import_glb(path, loc, rot_z_deg=0.0, name=None):
    # Import may bring several top-level objects: move/rotate them together.
    # NOTE: matrix_world is STALE right after import — update the view layer
    # first, or bbox/rotation math uses identity matrices and the model lands
    # at 2x the intended offset (bug found 06/11: characters at 40,-16).
    bpy.ops.import_scene.gltf(filepath=path)
    bpy.context.view_layer.update()
    new = [o for o in bpy.context.selected_objects]
    if not new:
        print("IMPORT FAILED:", path); return None
    tops = [o for o in new if o.parent is None]
    # Anchor = bbox center (x,y) + bbox min (z) of ALL top objects: robust when
    # tops[0] is an accessory mesh far from the model origin (character GLBs).
    import mathutils
    ws = []
    for o in tops:
        for v in o.bound_box:
            ws.append(o.matrix_world @ mathutils.Vector(v))
    xs = [v.x for v in ws]; ys = [v.y for v in ws]; zs = [v.z for v in ws]
    cx, cy, minz = (min(xs)+max(xs))/2, (min(ys)+max(ys))/2, min(zs)
    delta = Vector((loc[0]-cx, loc[1]-cy, loc[2]-minz))
    for o in tops:
        o.location += delta
    bpy.context.view_layer.update()
    if rot_z_deg:
        from mathutils import Matrix
        R = Matrix.Rotation(math.radians(rot_z_deg), 4, 'Z')
        for o in tops:
            o.matrix_world = (Matrix.Translation(loc) @ R
                              @ Matrix.Translation(-Vector(loc)) @ o.matrix_world)
    print(f"imported {name or path}: {len(tops)} top objects at {loc}")
    return tops

# A Di Đà đứng đài sen xanh — góc trước-trái, cạnh hồ/cổng (lớn nhất cảnh)
import_glb(W + "statues/verified_v2/phat-dung-adida.glb", (-40, -30, 0), 0, "Tuong_Adida_Dung")
# Di Lặc — trên bệ (-24,-1), mặt bệ cao z=1.7, mặt hướng ra trước (-Y)
import_glb(W + "statues/verified_v2/di-lac.glb", (-24, -1, 1.7), 0, "Tuong_Di_Lac")
# Phật nằm — trên bệ (12,47), mặt bệ cao z=2.8, nằm dọc X
import_glb(W + "statues/verified_v2/phat-nam.glb", (12, 47, 2.8), 0, "Tuong_Phat_Nam")

# ---------- 7. Vật phẩm (đã kiểm chứng) ----------
def import_prop(fname, loc, rot_z_deg=0.0):
    p = W + "repo-items/fixed/" + fname
    bpy.ops.import_scene.gltf(filepath=p)
    objs = list(bpy.context.selected_objects)
    if not objs:
        print("PROP IMPORT FAILED:", fname); return
    tops = [o for o in objs if o.parent is None] or objs
    # GLB vật phẩm có thể ở đơn vị mm nếu lỗi scale: kiểm tra và sửa
    mx = 0.0
    for o in tops:
        mx = max(mx, max(o.dimensions.x, o.dimensions.y, o.dimensions.z))
    if mx > 2.0:
        for o in tops: o.scale = (0.001, 0.001, 0.001)
        bpy.context.view_layer.update()
        print(f"prop {fname}: mm-scale detected ({mx:.1f}) -> x0.001")
    anchor = tops[0].location.copy()
    delta = Vector(loc) - anchor
    for o in tops:
        o.location += delta
    if rot_z_deg:
        from mathutils import Matrix
        R = Matrix.Rotation(math.radians(rot_z_deg), 4, 'Z')
        for o in tops:
            o.matrix_world = (Matrix.Translation(loc) @ R
                              @ Matrix.Translation(-Vector(loc)) @ o.matrix_world)
    print(f"prop {fname} at {loc}")

import_prop("den_long_luc_giac.glb", (19, -8, 0))
import_prop("den_long_luc_giac.glb", (27, -8, 0))
import_prop("mam_ngu_qua.glb", (20, -6, 0))
import_prop("dia_banh_bo.glb", (26, -6, 0))
import_prop("chum_sanh_hoa_sen.glb", (5, -9, 0))
import_prop("den_hoa_dang.glb", (3, -16, 0.0))
import_prop("den_hoa_dang.glb", (7, -14, 0.0))

# ---------- 8. Nhân vật (đã fit, pose Chắp tay, mặt hướng -Y) ----------
# Đặt trên sân trước chính điện, mặt hướng về chánh điện (+Y) -> xoay 180 độ
for key, x in (("nu", 20), ("nam", 23), ("tre", 26)):
    import_glb(W + f"characters_fitted/{key}.glb", (x, -8, 0), 180, f"NhanVat_{key}")

# ---------- 8b. Dọn mặt phẳng studio 'Ground*' do GLB tượng/vật phẩm mang theo ----------
# (lặp lại sau mọi import: chúng che toàn bộ mặt đất/hồ/sân)
for o in list(bpy.data.objects):
    if o.name.lower().startswith(('ground', 'floor', 'backdrop', 'studio')):
        print("removed studio junk:", o.name)
        bpy.data.objects.remove(o, do_unlink=True)

# ---------- 9. Trời / nắng / camera ----------
try: sc.view_settings.view_transform = 'Standard'
except Exception: pass
# xóa camera + đèn cũ của file gốc
for o in list(bpy.data.objects):
    if o.type in ('CAMERA', 'LIGHT') and o.name not in ('Sun_V3',):
        bpy.data.objects.remove(o, do_unlink=True)
w = bpy.data.worlds.new("Troi_Layout"); sc.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (0.42, 0.58, 0.85, 1)
w.node_tree.nodes["Background"].inputs[1].default_value = 0.7
sun = bpy.data.lights.new("Sun_Layout", 'SUN'); sun.energy = 3.2
so = bpy.data.objects.new("Sun_Layout", sun); sc.collection.objects.link(so)
so.rotation_euler = (0.95, 0.15, -0.55)

def make_cam(name, loc, tgt, lens):
    bpy.ops.object.camera_add(location=loc)
    cam = bpy.context.object; cam.name = name
    cam.data.lens = lens
    cam.data.clip_end = 500
    cam.rotation_euler = (Vector(tgt) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    return cam
fly = make_cam("Cam_Flycam", (0, -108, 68), (2, 10, 0), 35)
gnd = make_cam("Cam_Ground", (23, -38, 7), (23, 2, 6), 50)
sc.camera = fly

# Bệ Di Lặc: vật liệu riêng màu đá sẫm (dùng chung 'Vàng tường' sẽ nhuộm cả tháp)
dark = bpy.data.materials.new("Be_Di_Lac_Dark"); dark.use_nodes = True
dark.node_tree.nodes["Principled BSDF"].inputs['Base Color'].default_value = (0.16, 0.15, 0.15, 1)
plat = bpy.data.objects.get('Bệ khu tượng Di Lặc')
if plat:
    for i in range(len(plat.data.materials)):
        plat.data.materials[i] = dark
    print("Di Lac platform darkened")

sc.render.engine = 'CYCLES'; sc.cycles.samples = 32; sc.cycles.use_denoising = True
sc.render.resolution_x = 1280; sc.render.resolution_y = 720
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("LAYOUT BUILD DONE ->", OUT)
