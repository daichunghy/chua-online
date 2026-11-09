# V10 PATCH (09/11/2026) — sửa sau khi soi render v12 đợt 1:
#  a) Dat_Co tối hơn nữa (đợt 1 đọc thành cỏ xám nhạt)
#  b) rừng: tán ngang to hơn (0.55->0.95 bề rộng) + thêm 1 lớp tán ngang giữa,
#     giữ nguyên vị trí thân đã gieo (đọc lại từ mesh thân cũ)
#  c) lá sen: vật liệu xanh đậm phẳng thay LaSenXanh (đợt 1 đọc trắng)
#  d) mặt tiền: xóa dải lattice bị mái che khuất; gán lattice cho 'Diềm gốm'
#     (dải diềm thật của model, mặt trước y=-2.8) + chỉnh repeat
#  e) thêm Cam_V10_Niche để chụp cận cảnh hốc cổng
import bpy, math, random
from mathutils import Vector

bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/chua-online-work/layout_v12_v10.blend")
sc = bpy.context.scene

# --- a) Dat_Co ramp tối hơn
m = bpy.data.materials['Dat_Co']
for n in m.node_tree.nodes:
    if n.type == 'VALTORGB':
        cols = [e.color for e in n.color_ramp.elements]
        if all(c[0] < 0.3 for c in cols) and any(c[1] > c[0] for c in cols):
            n.color_ramp.elements[0].color = (0.045, 0.070, 0.028, 1)
            n.color_ramp.elements[1].color = (0.085, 0.068, 0.042, 1)
            if len(n.color_ramp.elements) > 2:
                n.color_ramp.elements[2].color = (0.065, 0.095, 0.038, 1)
            print("Dat_Co ramp darkened")
            break

# --- b) rừng: đọc vị trí thân cũ rồi dựng lại tán to hơn
old_t = bpy.data.objects.get('V10_Forest_Trunks')
old_c = bpy.data.objects.get('V10_Forest_Canopy')
trunks = []
if old_t:
    verts = [v.co for v in old_t.data.vertices]
    bots = {}
    for v in verts:
        if v.z < 0:
            key = (round(v.x), round(v.y))
            bots.setdefault(key, []).append(v)
    tops = {}
    for v in verts:
        if v.z > 1:
            key = (round(v.x), round(v.y))
            tops.setdefault(key, []).append(v.z)
    for key, vs in bots.items():
        cx = sum(v.x for v in vs)/len(vs); cy = sum(v.y for v in vs)/len(vs)
        h = 7.0
        # chiều cao: lấy max z của verts gần (x,y) này nhất trong tops (khớp theo tâm xấp xỉ)
        best = None
        for tk, zs in tops.items():
            d = (tk[0]-key[0])**2 + (tk[1]-key[1])**2
            if best is None or d < best[0]: best = (d, max(zs))
        if best: h = best[1]
        trunks.append((cx, cy, h))
print("trunks recovered:", len(trunks))
for o in (old_t, old_c):
    if o: bpy.data.objects.remove(o, do_unlink=True)

leaf_mats = [bpy.data.materials.get(x) for x in ('P2_LaA','P2_LaB','P2_LaC','P2_LaA2','P2_LaC2')]
leaf_mats = [x for x in leaf_mats if x]
trunk_mat = bpy.data.materials['P2_ThanCay']
random.seed(23)
tv, tf = [], []
cv, cf, cmats = [], [], []
def add_trunk(x, y, h, r):
    base = len(tv); lean = random.uniform(-0.4, 0.4)
    for i in range(4):
        a = i*math.pi/2 + math.pi/4
        tv.append((x + r*math.cos(a), y + r*math.sin(a), -0.4))
    for i in range(4):
        a = i*math.pi/2 + math.pi/4
        tv.append((x + lean + r*0.7*math.cos(a), y + r*0.7*math.sin(a), h))
    for i in range(4):
        j = (i+1) % 4
        tf.append((base+i, base+j, base+4+j, base+4+i))
def add_canopy(x, y, z, w, h, mi):
    for k in range(3):
        a = k*math.pi/3 + random.uniform(-0.2, 0.2)
        dx, dy = math.cos(a)*w/2, math.sin(a)*w/2
        base = len(cv)
        cv.extend([(x-dx, y-dy, z-h/2), (x+dx, y+dy, z-h/2), (x+dx, y+dy, z+h/2), (x-dx, y-dy, z+h/2)])
        cf.append((base, base+1, base+2, base+3)); cmats.append(mi)
    for dz, sc_ in ((h/2-0.2, 0.95), (-0.6, 0.75)):
        base = len(cv); s = w*sc_/2
        cv.extend([(x-s, y-s, z+dz), (x+s, y-s, z+dz), (x+s, y+s, z+dz), (x-s, y+s, z+dz)])
        cf.append((base, base+1, base+2, base+3)); cmats.append(mi)
for i, (x, y, h) in enumerate(trunks):
    add_trunk(x, y, h, 0.26)
    w = random.uniform(8.0, 12.5)
    add_canopy(x, y, h + 1.2, w, random.uniform(3.8, 4.8), i % len(leaf_mats))
for i in range(46):
    side = random.randrange(4)
    if side == 0: x, y = random.uniform(-56, 58), random.uniform(-46.5, -44.5)
    elif side == 1: x, y = random.uniform(-56, 58), random.uniform(54.5, 57)
    elif side == 2: x, y = random.uniform(-56, -53.5), random.uniform(-44, 55)
    else: x, y = random.uniform(55.5, 58.5), random.uniform(-44, 55)
    add_canopy(x, y, 1.2, random.uniform(3.2, 4.6), random.uniform(2.0, 3.0), i % len(leaf_mats))
tm = bpy.data.meshes.new('V10_ForestTrunks2'); tm.from_pydata(tv, [], tf); tm.update()
to = bpy.data.objects.new('V10_Forest_Trunks', tm); sc.collection.objects.link(to)
to.data.materials.append(trunk_mat)
cm = bpy.data.meshes.new('V10_ForestCanopy2'); cm.from_pydata(cv, [], cf); cm.update()
uv = cm.uv_layers.new(name='UVMap')
for pi, p in enumerate(cm.polygons):
    for li, v in zip(p.loop_indices, [(0,0),(1,0),(1,1),(0,1)]):
        uv.data[li].uv = v
    p.material_index = cmats[pi]
for lm in leaf_mats: cm.materials.append(lm)
co = bpy.data.objects.new('V10_Forest_Canopy', cm); sc.collection.objects.link(co)
print("forest rebuilt: canopy faces", len(cf))

# --- c) lá sen đậm
lm2 = bpy.data.materials.new('V10_LilyMat'); lm2.use_nodes = True
for n in lm2.node_tree.nodes:
    if n.type == 'BSDF_PRINCIPLED':
        n.inputs['Base Color'].default_value = (0.115, 0.235, 0.085, 1)
        n.inputs['Roughness'].default_value = 0.9
for nm in ('V10_Lily_0', 'V10_Lily_1'):
    o = bpy.data.objects.get(nm)
    if o and len(o.data.materials) > 0:
        o.data.materials[0] = lm2
        print("lily mat set", nm)

# --- d) mặt tiền: xóa dải ẩn, gán lattice cho Diềm gốm
for nm in ('V10_FacadeBand', 'V10_FacadeTrimB', 'V10_FacadeTrimT'):
    o = bpy.data.objects.get(nm)
    if o: bpy.data.objects.remove(o, do_unlink=True); print("removed", nm)
diem = bpy.data.objects.get('Diềm gốm')
lat = bpy.data.materials.get('V10_Lattice')
if diem and lat:
    diem.data.materials.clear(); diem.data.materials.append(lat)
    for n in lat.node_tree.nodes:
        if n.type == 'MAPPING': n.inputs['Scale'].default_value = (60, 1, 1)
    print("lattice assigned to Diem gom")

# --- e) camera cận cảnh hốc cổng
cam = bpy.data.cameras.new('Cam_V10_Niche'); cam.lens = 42
co2 = bpy.data.objects.new('Cam_V10_Niche', cam); sc.collection.objects.link(co2)
co2.location = (23, -50.5, 8.8)
d = (Vector((23, -39.5, 8.7)) - co2.location).normalized()
co2.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
print("niche cam added")

bpy.ops.wm.save_as_mainfile(filepath="/home/hatch/workspace/chua-online-work/layout_v12_v10.blend")
print("PATCH SAVED")
