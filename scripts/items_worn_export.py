"""
FIT MODEL REPO LÊN NHÂN VẬT THẬT — Chùa Online / Vĩnh Tràng (bản v2: import-and-fit)
Thay toàn bộ vật phẩm dựng nguyên thủy (bản cũ lưu ở items_worn_v1_primitives.py) bằng
MODEL HOÀN CHỈNH CÓ TEXTURE từ repo chua-online (pipeline Coohom), thư mục repo-items/:
  1. non_la_theu_sen_v3.glb  — nón lá thêu sen PBR (kèm quai lụa hồng) → thay nón côn trơn
  2. tui_vai_theu_sen.glb    — túi vải thêu sen PBR (thân + quai xách) → thay túi hộp trơn;
                               vẫn giữ quai đeo vai 3 đoạn ôm thân đã fit (model repo chỉ có quai xách)
  3. trang_hat_bo_de.obj    — tràng hạt 108 hạt + hạt hồ lô + tua chỉ đỏ (MTL màu)
  4. hoa_sen_tuoi.obj       — búp sen hồng + gương sen + cuống + lá sen (MTL màu)
  5. khan_ran_nam_bo.obj    — khăn rằn: vành caro + 2 vạt trắng + tua (MTL màu)

Kỷ luật fit giữ nguyên: mọi kích thước/vị trí suy từ posed mesh + xương của chính nhân vật
(thân đo pose Đứng, tay/cổ đo pose Chắp tay frame 15). Model repo được đo bbox thật của
chính nó rồi scale về đúng giá trị fit đã kiểm chứng (vành nón 0,252H, thân túi 0,155H×0,165H...).
Màu nhân vật = vertex color 'Color'.

Dùng: blender -b --factory-startup -noaudio --python items_worn.py -- <nu|nam|tre>

V2 FIX (2026-11-06, chỉ nam/trẻ em — nữ giữ nguyên): hoa sen repo là bó sen cắm trưng:
lá phẳng đọc như khay bay giữa thân, búp lơ lửng trên tay, búp rộng hơn cao đọc như
chùm bóng. Tách theo material, xoá lá, thu hẹp búp ngang ×0,72 + kéo cao ×1,5, đáy búp
đặt ngay trên đầu ngón tay, cuống chỉ còn đoạn ngắn xuyên tay. Xem mục 4 trong code.
"""
import bpy, math, sys, os
sys.stdout.reconfigure(line_buffering=True)
from mathutils import Vector

KEY = sys.argv[sys.argv.index('--') + 1]
CFG = {
    'nu':  dict(src="/home/hatch/workspace/user/files/nu-phuc-hoi-mau-chuyen-dong.glb",
                hat='v1', out="/home/hatch/workspace/chua-online-work/items-nu.png"),
    'nam': dict(src="/home/hatch/workspace/user/files/nam-chuyen-dong.glb",
                hat='v2', out="/home/hatch/workspace/chua-online-work/items-nam-v2.png",
                lotus_fix=True),
    'tre': dict(src="/home/hatch/workspace/user/files/tre-em-chuyen-dong.glb",
                hat='v2', out="/home/hatch/workspace/chua-online-work/items-tre-em-v2.png",
                lotus_fix=True),
}[KEY]
ITEMS = "/home/hatch/workspace/chua-online-work/repo-items"

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=CFG['src'])
arm = next(o for o in bpy.context.scene.objects if o.type == 'ARMATURE')
mesh = next(o for o in bpy.context.scene.objects if o.type == 'MESH' and o.name == 'geometry_0')
for o in list(bpy.context.scene.objects):
    if o.type == 'MESH' and o.name != 'geometry_0':
        bpy.data.objects.remove(o, do_unlink=True)

vm = bpy.data.materials.new("Mau_Vertex_NhanVat"); vm.use_nodes = True
nt = vm.node_tree
bsdf = nt.nodes["Principled BSDF"]; bsdf.inputs["Roughness"].default_value = 0.75
vc = nt.nodes.new("ShaderNodeVertexColor"); vc.layer_name = "Color"
nt.links.new(vc.outputs["Color"], bsdf.inputs["Base Color"])
mesh.data.materials.clear(); mesh.data.materials.append(vm)

def mat(name, rgba, rough=0.8):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = rgba; b.inputs["Roughness"].default_value = rough
    return m
mat_strap = mat("Quai", (0.45, 0.40, 0.34, 1), 0.9)

def set_pose(action_name, frame):
    act = bpy.data.actions.get(action_name)
    if arm.animation_data is None: arm.animation_data_create()
    arm.animation_data.action = act
    bpy.context.scene.frame_set(frame)
    bpy.context.view_layer.update()

def posed_verts():
    dg = bpy.context.evaluated_depsgraph_get(); ev = mesh.evaluated_get(dg)
    return [ev.matrix_world @ v.co for v in ev.data.vertices]

def bone_world(name):
    pb = arm.pose.bones[name]
    return (arm.matrix_world @ pb.head, arm.matrix_world @ pb.tail)

# ---------- Đo pose Đứng ----------
set_pose('Dung_world', 1)
v0 = posed_verts()
z0min = min(v.z for v in v0); z0max = max(v.z for v in v0); H0 = z0max - z0min
band0 = [v for v in v0 if abs(v.z - (z0min + 0.78 * H0)) < 0.03 * H0 and abs(v.x) < 0.16 * H0]
FRONT_Y = min(v.y for v in band0) - 0.006

# ---------- Đo pose Chắp tay ----------
set_pose('Chắp tay_world', 15)
verts = posed_verts()
zmin = min(v.z for v in verts); zmax = max(v.z for v in verts); H = zmax - zmin
head_band = [v for v in verts if v.z > zmax - 0.16 * H]
head_cx = sum(v.x for v in head_band) / len(head_band)
head_cy = sum(v.y for v in head_band) / len(head_band)
hip_band = [v for v in verts if abs(v.z - (zmin + 0.52 * H)) < 0.03 * H]
hip_w = max(v.x for v in hip_band) - min(v.x for v in hip_band)
head_h, head_t = bone_world('Head')
shL_h, _ = bone_world('L upper arm')
shR_h, _ = bone_world('R upper arm')
lh_h, lh_t = bone_world('L hand')
rh_h, rh_t = bone_world('R hand')
palm = (lh_h + rh_h) / 2
print(f"[{KEY}] H={H:.3f} FRONT_Y={FRONT_Y:.3f} palm={tuple(round(v,3) for v in palm)}")
# Đỉnh ngón tay pose Chắp tay (để đặt đáy búp sen vừa trên tay — V2 fix):
hand_band = [v for v in verts if abs(v.x - palm.x) < 0.07 and abs(v.y - palm.y) < 0.07
             and palm.z < v.z < palm.z + 0.15]
hand_top_z = max(v.z for v in hand_band) if hand_band else palm.z + 0.06
print(f"[{KEY}] hand_top_z={hand_top_z:.3f} (palm.z={palm.z:.3f})")

# eo cổ: quét z dưới xương Head, nơi bề ngang thân hẹp nhất (như bản v1)
neck_cx, neck_cy = head_h.x, head_h.y
best = None; zc_try = head_h.z - 0.004 * H
while zc_try > head_h.z - 0.055 * H:
    band = [v for v in verts if abs(v.z - zc_try) < 0.008 * H]
    if band:
        halfw = max(abs(v.x - neck_cx) for v in band)
        if best is None or halfw < best[1]: best = (zc_try, halfw)
    zc_try -= 0.004 * H
neck_z = best[0] if best else head_h.z - 0.02 * H
print(f"[{KEY}] neck_z={neck_z:.3f}")

# ---------- Helper: import model repo, trả về list mesh mới ----------
def import_item(filename):
    before = set(bpy.context.scene.objects)
    p = os.path.join(ITEMS, filename)
    if filename.endswith('.glb'): bpy.ops.import_scene.gltf(filepath=p)
    else: bpy.ops.wm.obj_import(filepath=p)
    new = [o for o in bpy.context.scene.objects if o not in before]
    meshes = [o for o in new if o.type == 'MESH']
    for o in new:
        if o.type != 'MESH': bpy.data.objects.remove(o, do_unlink=True)
    if filename.endswith('.obj'):
        # OBJ của repo mang custom split normals HỎNG (tham chiếu vn vượt mảng) → shade
        # gần đen trong mọi importer chuẩn. verify_one.py của chính repo cũng phải xoá
        # split normals + shade_smooth_by_angle mới kiểm chứng được — áp đúng chuẩn đó.
        for o in meshes:
            bpy.context.view_layer.objects.active = o
            o.select_set(True)
            if o.data.has_custom_normals:
                try: bpy.ops.mesh.customdata_custom_splitnormals_clear()
                except Exception: pass
            try: bpy.ops.object.shade_smooth_by_angle()
            except Exception:
                for p_ in o.data.polygons: p_.use_smooth = True
            o.select_set(False)
            o.data.update()
    return meshes

def bbox_of(objs):
    xs, ys, zs = [], [], []
    for o in objs:
        for c in o.bound_box:
            w = o.matrix_world @ Vector(c)
            xs.append(w.x); ys.append(w.y); zs.append(w.z)
    return (min(xs), max(xs), min(ys), max(ys), min(zs), max(zs))

# ---------- 1. NÓN REPO: scale vành về 0,252H, vành tại rim_z đã fit ----------
hat_objs = import_item("non_la_theu_sen_v3.glb")
cone = next(o for o in hat_objs if 'Non_La' in o.name)
# Quai lụa của GLB: vòng đai nằm trong mặt phẳng XZ qua trục đầu — khi đội lên đầu thật,
# cung dưới của nó cắt ngang mặt (đã kiểm chứng bằng render) → loại mesh quai, giữ thân nón.
for o in list(hat_objs):
    if o is not cone:
        nm = o.name
        bpy.data.objects.remove(o, do_unlink=True)
        hat_objs.remove(o)
        print(f"[{KEY}] repo hat: removed strap mesh '{nm}' (face-clipping as authored)")
hb = bbox_of([cone]); brim_d = hb[1] - hb[0]
s_hat = (0.252 * H) / brim_d
if CFG['hat'] == 'v2':
    rim_z = zmin + 0.885 * H; hat_cx, hat_cy = head_cx, head_cy
else:
    rim_z = zmin + 0.895 * H; hat_cx, hat_cy = head_h.x, head_h.y
for o in hat_objs:
    o.scale = (s_hat, s_hat, s_hat)
    o.rotation_euler = (math.radians(3), 0, 0)
    o.location = (hat_cx, hat_cy, rim_z)   # origin GLB nằm tại tâm vành (z=0)
print(f"[{KEY}] repo hat: brim {brim_d:.3f} -> scale {s_hat:.3f}, rim_z={rim_z:.3f}")

# ---------- 2. TÚI REPO + quai đeo vai 3 đoạn đã fit ----------
bag_objs = import_item("tui_vai_theu_sen.glb")
bag = bag_objs[0]
bb = bbox_of(bag_objs)
bag_w, bag_d = bb[1] - bb[0], bb[3] - bb[2]
# thân túi repo: z 0..0,38 trong tổng cao 0,564 (phần trên là quai xách) — tỉ lệ thân suy từ file chưa gộp
BODY_FRAC = 0.38 / 0.564
bag_total_h = bb[5] - bb[4]
body_h_local = bag_total_h * BODY_FRAC
s_bag = (0.155 * H) / bag_w
bag_c = Vector((hip_w / 2 + 0.055 * H, 0.0, zmin + 0.47 * H))
origin_z = bag_c.z - (body_h_local * s_bag) / 2
for o in bag_objs:
    o.scale = (s_bag, s_bag, s_bag)
    o.rotation_euler = (0, 0, math.radians(-4))
    o.location = (bag_c.x, bag_c.y, origin_z)
print(f"[{KEY}] repo bag: w {bag_w:.3f} -> scale {s_bag:.3f}, body_h={(body_h_local*s_bag):.3f} target {0.165*H:.3f}")
# quai đeo vai 3 đoạn ôm bề mặt (giữ nguyên bản fit đã đạt)
def surf_y_fit(zfrac, x):
    zt = z0min + zfrac * H0
    band = [v.y for v in v0 if abs(v.z - zt) < 0.02 * H0 and abs(v.x - x) < 0.06 * H0]
    if not band: return FRONT_Y
    return max(min(band) - 0.004, FRONT_Y - 0.015)
p1 = Vector((bag_c.x - 0.02, FRONT_Y + 0.03, bag_c.z + (body_h_local * s_bag) / 2))
p2 = Vector((shR_h.x + 0.01, FRONT_Y, shR_h.z - 0.01))
pts = [p1]
for t in (0.33, 0.66):
    q = p1.lerp(p2, t); q.y = surf_y_fit((q.z - zmin) / H, q.x); pts.append(q)
pts.append(p2)
for i in range(len(pts) - 1):
    a, b = pts[i], pts[i + 1]; mid = (a + b) / 2; d = b - a
    bpy.ops.mesh.primitive_cube_add(size=1, location=mid)
    seg = bpy.context.object; seg.name = f"Quai_Deo_FitThat_{i}"
    seg.dimensions = (0.016 * H, 0.004, d.length)
    seg.rotation_mode = 'QUATERNION'
    seg.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d.normalized())
    seg.data.materials.append(mat_strap)

# ---------- 3. TRÀNG HẠT REPO: xoay đứng, kéo giãn theo trục vòng, treo qua hai tay ----------
bead_objs = import_item("trang_hat_bo_de.obj")
beads = bead_objs[0]
# Model gốc: vòng oval nằm phẳng XY (0,296 × 0,416), hạt chủ ở đầu −Y, tua rủ −Z tại hạt chủ.
# Xoay X +90°: trục dài → trục Z (hạt chủ xuống đáy), tua ra phía +Y (về phía thân) — nghiêng thêm −5° cho đáy vòng ngả ra trước.
LOOP_H = 0.50 * H          # chiều cao vòng sau fit — khớp đáy vòng bản nguyên thủy đã đạt (top tay → đáy ≈ 0,97 với H≈1,99)
bb = bbox_of(bead_objs)
long_local = bb[3] - bb[2]  # 0,416
wid_local = bb[1] - bb[0]   # 0,296
sz_long = LOOP_H / long_local
sx_wid = 0.35 / wid_local * (H / 1.985)   # bề ngang vòng ≈ 0,35 ở H chuẩn (≈ bề ngang thân), tỉ lệ theo H
# Model gốc: obj_import đặt sẵn rotation X +90° trên object (geometry local khác hệ world).
# Ở world sau import: vòng oval nằm phẳng XY (0,296 × 0,416), hạt chủ ở đầu −Y, tua rủ −Z.
# Fit: cộng thêm Rx +85° vào rotation object (= 175°) để trục dài thành trục Z, hạt chủ
# xuống đáy, đáy vòng ngả trước 5°. Scale theo trục LOCAL: x = bề ngang (file X),
# z = trục dài (file Y), y = bề dày vòng (giữ 1,0).
for o in bead_objs:
    o.rotation_euler = (math.radians(90 + 85), 0, 0)
    o.scale = (sx_wid, 1.0, sz_long)
    top_z = palm.z + 0.03
    o.location = (palm.x, palm.y + 0.010, top_z - (long_local / 2) * sz_long)
print(f"[{KEY}] repo beads: scale_x={sx_wid:.2f} scale_long={sz_long:.2f} top_z={palm.z + 0.03:.3f} bottom_z={palm.z + 0.03 - LOOP_H:.3f}")

# ---------- 4. HOA SEN REPO: búp đứng giữa hai lòng bàn tay ----------
lotus_objs = import_item("hoa_sen_tuoi.obj")
s_lotus = 1.15 * (H / 1.985)
if CFG.get('lotus_fix'):
    # --- V2 FIX (nam/trẻ em): model repo là bó sen cắm trưng, không phải sen cầm tay.
    # Đo thật từng bộ phận (world, chưa scale): cuống z 0..0,300; gương sen z 0,300..0,325;
    # cánh búp hồng z 0,284..0,346 (rộng 0,122 × cao 0,062 → đọc như chùm bóng);
    # lá sen: đĩa phẳng 0,28×0,276 tại z≈0,053, lệch +X 0,08 (đọc như khay bay giữa thân).
    # Lỗi cũ: gốc đặt tại palm.z − 0,10H → búp lơ lửng ~0,13 trên đầu ngón tay,
    # lá nằm ngang giữa thân như khay. Fix: tách theo material, XOÁ lá, thu hẹp búp
    # ngang ×0,72 + kéo cao ×1,5 (búp cao ~0,107 × rộng ~0,101), đáy búp đặt ngay trên
    # đầu ngón tay +0,01, cuống chỉ còn đoạn ngắn từ đáy búp xuyên tay xuống palm.z − 0,08.
    bpy.ops.object.select_all(action='DESELECT')
    for o in lotus_objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = lotus_objs[0]
    bpy.ops.mesh.separate(type='MATERIAL')
    parts = {}
    for o in [x for x in bpy.context.scene.objects if x.type == 'MESH' and x.name.startswith('hoa_sen_tuoi')]:
        mn_ = o.data.materials[0].name if o.data.materials else ''
        parts[mn_] = o
    leaf = parts.pop('LaSenXanhNgoc', None)
    if leaf is not None:
        bpy.data.objects.remove(leaf, do_unlink=True)
        print(f"[{KEY}] lotus V2: removed flat leaf disc (tray read)")
    bud_target_bottom = hand_top_z + 0.01
    bud_objs = [parts[k] for k in ('CanhSenHong', 'GuongSenVang') if k in parts]
    for o in bud_objs:
        # scale local (X->world X, Y->world Z, Z->world Y): world ngang ×0,72, cao ×1,5
        o.scale = (0.72 * s_lotus, 1.5 * s_lotus, 0.72 * s_lotus)
        o.location = (palm.x, palm.y + 0.005, palm.z - 0.10 * H)
    bpy.context.view_layer.update()
    dz = bud_target_bottom - bbox_of(bud_objs)[4]
    for o in bud_objs:
        o.location.z += dz
    stem = parts.get('CanhSenXanh')
    if stem is not None:
        # cuống: giữ đường kính ×s_lotus, co chiều cao (local Y = world Z) về đúng đoạn
        # từ đáy búp xuống palm.z − 0,08; gốc local Y=0 nằm ở đáy cuống.
        stem_len = bud_target_bottom - (palm.z - 0.08)
        stem.scale = (s_lotus, stem_len / 0.300, s_lotus)
        stem.location = (palm.x, palm.y + 0.005, palm.z - 0.08)
    print(f"[{KEY}] lotus V2: bud_bottom={bud_target_bottom:.3f} (hand_top={hand_top_z:.3f}) stem_len={stem_len:.3f}")
else:
    lb = bbox_of(lotus_objs)
    lotus_h = lb[5] - lb[4]
    for o in lotus_objs:
        o.scale = (s_lotus, s_lotus, s_lotus)
        o.location = (palm.x, palm.y + 0.005, palm.z - 0.10 * H)
    print(f"[{KEY}] repo lotus: scale={s_lotus:.2f} bud_top_z={palm.z - 0.10*H + lotus_h*s_lotus:.3f}")

# ---------- 5. KHĂN RẰN REPO: vành ôm eo cổ, nghiêng trước cho vạt áp ngực ----------
scarf_objs = import_item("khan_ran_nam_bo.obj")
sb = bbox_of(scarf_objs)
ring_d = sb[1] - sb[0]      # 0,35
s_scarf = 0.30 / ring_d * (H / 1.985)   # vành drap Ø ≈ 0,30 ở H chuẩn
for o in scarf_objs:
    o.scale = (s_scarf, s_scarf, s_scarf)
    # Giữ rotation X +90° do obj_import đặt (ở world khăn đã đúng tư thế đeo: vành ngang,
    # vạt rủ trước −Y), chỉ trừ 15° để vạt ngả áp vào ngực.
    o.rotation_euler = (math.radians(90 - 15), 0, 0)
    o.location = (neck_cx, neck_cy - 0.005, neck_z - 0.018)
print(f"[{KEY}] repo scarf: ring {ring_d:.3f} -> scale {s_scarf:.2f} at neck_z={neck_z:.3f}")


# ---------- Export fitted character (baked pose) ----------
import bpy
arm = next((o for o in bpy.context.scene.objects if o.type == 'ARMATURE'), None)
mesh = next((o for o in bpy.context.scene.objects if o.type == 'MESH' and o.name == 'geometry_0'), None)
if arm and mesh:
    bpy.context.view_layer.objects.active = mesh
    for m in list(mesh.modifiers):
        if m.type == 'ARMATURE':
            try:
                bpy.ops.object.modifier_apply(modifier=m.name)
                print(f"[{KEY}] baked armature modifier {m.name}")
            except Exception as e:
                print(f"[{KEY}] bake failed: {e}")
    bpy.data.objects.remove(arm, do_unlink=True)
for o in list(bpy.context.scene.objects):
    if o.type in ('LIGHT','CAMERA'):
        bpy.data.objects.remove(o, do_unlink=True)
out = f"/home/hatch/workspace/chua-online-work/characters_fitted/{KEY}.glb"
bpy.ops.export_scene.gltf(filepath=out, export_format='GLB')
print(f"[{KEY}] FITTED CHARACTER EXPORTED -> {out}")
