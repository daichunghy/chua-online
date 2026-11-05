"""
FIT TRÊN MODEL THẬT — nam-chuyen-dong.glb (Logan cấp file 2026-11-05) — nhân vật ĐÀN ÔNG
Đo từ file: armature 'world', xương Head/Spine/Pelvis/L-R upper arm; 8 action
(Chắp tay, Đi bộ, Đứng, Quỳ, Thắp nhang, Vái, lên/xuống cầu thang).
Mọi kích thước suy từ số đo posed mesh (chiều cao H, bề rộng đầu) — không gõ tay.
"""
import bpy, math, sys
sys.stdout.reconfigure(line_buffering=True)
from mathutils import Vector

SRC = "/home/hatch/workspace/user/files/nam-chuyen-dong.glb"
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=SRC)
arm = next(o for o in bpy.context.scene.objects if o.type == 'ARMATURE')
mesh = next(o for o in bpy.context.scene.objects if o.type == 'MESH' and o.name == 'geometry_0')
# bỏ icosphere nền nếu có
for o in list(bpy.context.scene.objects):
    if o.type == 'MESH' and o.name != 'geometry_0':
        bpy.data.objects.remove(o, do_unlink=True)

# Model này KHÔNG có material/UV — màu nằm ở vertex color 'Color' → tự tạo material đọc vertex color
vm = bpy.data.materials.new("Mau_Vertex_NhanVat"); vm.use_nodes = True
nt = vm.node_tree
bsdf = nt.nodes["Principled BSDF"]; bsdf.inputs["Roughness"].default_value = 0.75
vc = nt.nodes.new("ShaderNodeVertexColor"); vc.layer_name = "Color"
nt.links.new(vc.outputs["Color"], bsdf.inputs["Base Color"])
mesh.data.materials.clear(); mesh.data.materials.append(vm)

# Pose chắp tay, frame giữa
act = bpy.data.actions.get('Chắp tay_world')
arm.animation_data_create().action = act
bpy.context.scene.frame_set(15)
bpy.context.view_layer.update()

# Đo mặt trước THÂN ở pose Đứng (pose chắp tay có tay chắn trước ngực, đo sẽ lệch)
act0 = bpy.data.actions.get('Dung_world')
arm.animation_data.action = act0
bpy.context.scene.frame_set(1)
bpy.context.view_layer.update()
dg0 = bpy.context.evaluated_depsgraph_get(); ev0 = mesh.evaluated_get(dg0)
v0 = [ev0.matrix_world @ v.co for v in ev0.data.vertices]
z0min = min(v.z for v in v0); H0 = max(v.z for v in v0) - z0min
band0 = [v for v in v0 if abs(v.z - (z0min + 0.78 * H0)) < 0.03 * H0 and abs(v.x) < 0.16 * H0]
FRONT_Y = min(v.y for v in band0) - 0.006
print(f"TORSO FRONT (Dung pose): FRONT_Y={FRONT_Y:.3f}")
arm.animation_data.action = act
bpy.context.scene.frame_set(15)
bpy.context.view_layer.update()

# ---- Đo posed mesh (world) ----
dg = bpy.context.evaluated_depsgraph_get()
ev = mesh.evaluated_get(dg)
verts = [ev.matrix_world @ v.co for v in ev.data.vertices]
zmin = min(v.z for v in verts); zmax = max(v.z for v in verts)
H = zmax - zmin
head_band = [v for v in verts if v.z > zmax - 0.16 * H]
head_w = max(v.x for v in head_band) - min(v.x for v in head_band)
head_cx = sum(v.x for v in head_band) / len(head_band)
head_cy = sum(v.y for v in head_band) / len(head_band)
hip_band = [v for v in verts if abs(v.z - (zmin + 0.52 * H)) < 0.03 * H]
hip_w = max(v.x for v in hip_band) - min(v.x for v in hip_band)
print(f"MEASURED posed: H={H:.3f} head_w={head_w:.3f} hip_w={hip_w:.3f} zmin={zmin:.3f} zmax={zmax:.3f}")

def bone_world(name):
    pb = arm.pose.bones[name]
    return (arm.matrix_world @ pb.head, arm.matrix_world @ pb.tail)
head_h, head_t = bone_world('Head')
shL_h, _ = bone_world('L upper arm')
shR_h, _ = bone_world('R upper arm')
print(f"Head bone world: head={tuple(round(v,2) for v in head_h)} tail={tuple(round(v,2) for v in head_t)}")
print(f"Shoulders world: L={tuple(round(v,2) for v in shL_h)} R={tuple(round(v,2) for v in shR_h)}")

def mat(name, rgba, rough=0.8):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = rgba; b.inputs["Roughness"].default_value = rough
    return m
mat_straw = mat("La_Tre", (0.84, 0.70, 0.44, 1), 0.85)
mat_bag = mat("Vai_Tui", (0.62, 0.58, 0.52, 1), 0.9)
mat_strap = mat("Quai", (0.45, 0.40, 0.34, 1), 0.9)
mat_lotus = mat("Sen", (0.87, 0.50, 0.58, 1), 0.8)

# ---- NÓN: vành Ø = 0.252*H (0.416m/1.65m), vành ôm ở 0.90*H từ chân ----
R = 0.126 * H
rim_z = zmin + 0.885 * H
bpy.ops.mesh.primitive_cone_add(radius1=R, radius2=0.055 * H, depth=0.125 * H, vertices=48,
                                location=(head_cx, head_cy, rim_z + 0.0625 * H))
hat = bpy.context.object; hat.name = "Non_La_FitThat"
hat.data.materials.append(mat_straw)
hat.rotation_euler = (math.radians(3), 0, 0)

# ---- TÚI: thân ngoài hông trái, quai chéo lên vai phải (mặt trước = −Y hay +Y: lấy theo tay chắp) ----
# hông trái world x âm (L side = +X theo xương L upper arm x=+0.204 → trái là +X). Dùng phía +X.
bag_c = Vector((hip_w / 2 + 0.055 * H, 0.0, zmin + 0.47 * H))
bpy.ops.mesh.primitive_cube_add(size=1, location=bag_c)
bag = bpy.context.object; bag.name = "Tui_FitThat"
bag.dimensions = (0.155 * H, 0.05 * H, 0.165 * H)
bag.rotation_euler = (0, 0, math.radians(-4))
bag.data.materials.append(mat_bag)
# quai: từ miệng túi lên vai đối diện (R shoulder, x âm), chạy sát mặt trước thân (y = min y của thân tại ngực)
front_y = FRONT_Y
p1 = Vector((bag_c.x - 0.02, front_y + 0.03, bag_c.z + 0.085 * H))
p2 = Vector((shR_h.x + 0.01, front_y, shR_h.z - 0.01))
def surf_y(zfrac, x):
    zt = z0min + zfrac * H0
    band = [v.y for v in v0 if abs(v.z - zt) < 0.02 * H0 and abs(v.x - x) < 0.06 * H0]
    if not band: return front_y
    return max(min(band) - 0.004, front_y - 0.015)
pts = [p1]
for t in (0.33, 0.66):
    q = p1.lerp(p2, t)
    q.y = surf_y((q.z - zmin) / H, q.x)
    pts.append(q)
pts.append(p2)
for i in range(len(pts) - 1):
    a, b = pts[i], pts[i + 1]; mid = (a + b) / 2; d = b - a
    bpy.ops.mesh.primitive_cube_add(size=1, location=mid)
    seg = bpy.context.object; seg.name = f"Quai_Deo_FitThat_{i}"
    seg.dimensions = (0.016 * H, 0.004, d.length)
    seg.rotation_mode = 'QUATERNION'
    seg.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d.normalized())
    seg.data.materials.append(mat_strap)
print(f"Bag center={tuple(round(v,2) for v in bag_c)} strap {tuple(round(v,2) for v in p1)} -> {tuple(round(v,2) for v in p2)} front_y={front_y:.3f}")

# ---- Sân/đèn/camera ----
bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, zmin - 0.005))
bpy.context.object.data.materials.append(mat("San", (0.5, 0.48, 0.46, 1), 0.95))
sun = bpy.data.lights.new("Sun", 'SUN'); sun.energy = 1.15
so = bpy.data.objects.new("Sun", sun); bpy.context.collection.objects.link(so)
so.rotation_euler = (math.radians(50), 0, math.radians(-35))
w = bpy.data.worlds.new("Troi"); bpy.context.scene.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (0.55, 0.68, 0.88, 1)
w.node_tree.nodes["Background"].inputs[1].default_value = 0.35
cam = bpy.data.cameras.new("Cam"); cam.clip_end = 100
co = bpy.data.objects.new("Cam", cam); bpy.context.collection.objects.link(co)
cx = (min(v.x for v in verts) + max(v.x for v in verts)) / 2
cam.sensor_fit = 'VERTICAL'
co.location = (cx + 0.70 * H, -2.30 * H, zmin + 0.58 * H)
_tgt = Vector((cx, 0, zmin + 0.50 * H))
co.rotation_euler = (_tgt - co.location).to_track_quat('-Z', 'Y').to_euler()
bpy.context.scene.camera = co
sc = bpy.context.scene
sc.render.engine = 'CYCLES'; sc.cycles.samples = 32; sc.cycles.use_denoising = False
sc.view_settings.view_transform = 'AgX'
sc.render.resolution_x = 960; sc.render.resolution_y = 540
sc.render.filepath = "/home/hatch/workspace/chua-online-work/fit-nam.png"
bpy.ops.render.render(write_still=True)
print("FIT REAL DONE")
