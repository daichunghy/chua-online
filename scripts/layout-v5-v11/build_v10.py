# V10 — GIỐNG THẬT (09/11/2026): từ layout_v11_v9.blend -> layout_v12_v10.blend
# Sửa theo bảng xếp hạng lệch trong NOTES.md §V10:
#  1) nền ngoài rào: Dat_Co biến thiên + vòng rừng dừa dày + đường nhựa trước cổng
#  2) tháp cổng: hốc tượng Phật đứng trắng + chóp mái ngói (cả 2 cổng)
#  3) mái chánh điện: biến thiên mảng ngói (noise multiply) + bờ nóc
#  4) mặt tiền: dải lattice trắng phía trên vòm
#  5) hồ: nước tối rêu hơn + lá sen
#  6) tượng trắng ấm: WhiteStone* multiply ấm về #EFE9DD + đèn fill Di Lặc mạnh hơn
#  7) dời cây V9 khỏi trục cổng chính
#  8) Cam_Flycam lại gần/thấp khớp ref9
import bpy, math, random
from mathutils import Vector, Matrix

random.seed(10)
bpy.ops.wm.open_mainfile(filepath="/home/hatch/workspace/chua-online-work/layout_v11_v9.blend")
sc = bpy.context.scene

def bbox(o):
    cs = [o.matrix_world @ Vector(c) for c in o.bound_box]
    return (min(c.x for c in cs), max(c.x for c in cs),
            min(c.y for c in cs), max(c.y for c in cs),
            min(c.z for c in cs), max(c.z for c in cs))

def box(name, loc, size, mat=None):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.active_object; o.name = name
    o.dimensions = size
    bpy.ops.object.transform_apply(scale=True)
    if mat: o.data.materials.append(mat)
    return o

def principled(mat):
    for n in mat.node_tree.nodes:
        if n.type == 'BSDF_PRINCIPLED': return n
    return None

def final_color_source(mat):
    """node+socket feeding Principled Base Color"""
    bsdf = principled(mat)
    link = None
    for l in mat.node_tree.links:
        if l.to_node == bsdf and l.to_socket.name == 'Base Color':
            link = l
    return link

def insert_multiply(mat, color2_node_out=None, const_color=None, label=""):
    """Insert MULTIPLY mix between current Base Color source and BSDF.
       Returns the new mix node."""
    nt = mat.node_tree
    bsdf = principled(mat)
    link = final_color_source(mat)
    assert link, mat.name
    src_node, src_sock = link.from_node, link.from_socket
    nt.links.remove(link)
    mix = nt.nodes.new('ShaderNodeMixRGB'); mix.blend_type = 'MULTIPLY'
    mix.name = 'V10_Multiply' + label
    mix.inputs['Fac'].default_value = 1.0
    nt.links.new(src_node.outputs[src_sock.name], mix.inputs['Color1'])
    if const_color is not None:
        mix.inputs['Color2'].default_value = const_color
    if color2_node_out is not None:
        nt.links.new(color2_node_out, mix.inputs['Color2'])
    nt.links.new(mix.outputs['Color'], bsdf.inputs['Base Color'])
    return mix

# ---------------------------------------------------------------- Fix 6 (albedo ấm) — làm trước để tượng hốc cổng hưởng chung
for mn in ('WhiteStone', 'WhiteStone.001', 'WhiteStone.002'):
    m = bpy.data.materials.get(mn)
    if m and m.use_nodes:
        insert_multiply(m, const_color=(1.05, 0.99, 0.85, 1.0), label='_'+mn[-3:])
        print("WARMED", mn)

# đèn fill Di Lặc: tìm đèn gần (-24, 9, 8.5)
for o in bpy.data.objects:
    if o.type == 'LIGHT':
        print("LIGHT", o.name, o.data.type, [round(v,1) for v in o.location], round(o.data.energy,1),
              [round(c,2) for c in o.data.color])
        if o.data.type == 'POINT' and abs(o.location.x + 24) < 3 and abs(o.location.y - 9) < 3:
            o.data.energy = 1500
            o.data.color = (1.0, 0.70, 0.40)
            print("  -> Di Lac fill boosted")

# ---------------------------------------------------------------- Fix 1a: Dat_Co biến thiên
m = bpy.data.materials['Dat_Co']; nt = m.node_tree
bsdf = principled(m)
link = final_color_source(m)
src_node, src_sock = link.from_node, link.from_socket
nt.links.remove(link)
tc = nt.nodes.new('ShaderNodeTexCoord')
noise = nt.nodes.new('ShaderNodeTexNoise'); noise.inputs['Scale'].default_value = 0.045
noise.inputs['Detail'].default_value = 4.0
ramp = nt.nodes.new('ShaderNodeValToRGB')
ramp.color_ramp.elements[0].position = 0.0
ramp.color_ramp.elements[0].color = (0.115, 0.145, 0.062, 1)   # scrub tối (linear ~ #4E5F3A/2)
ramp.color_ramp.elements[1].position = 1.0
ramp.color_ramp.elements[1].color = (0.190, 0.150, 0.095, 1)   # đất nâu
e = ramp.color_ramp.elements.new(0.55); e.color = (0.135, 0.180, 0.075, 1)  # scrub sáng
mix = nt.nodes.new('ShaderNodeMixRGB'); mix.blend_type = 'MIX'
mix.inputs['Fac'].default_value = 0.88
nt.links.new(tc.outputs['Generated'], noise.inputs['Vector'])
nt.links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
nt.links.new(src_node.outputs[src_sock.name], mix.inputs['Color1'])
nt.links.new(ramp.outputs['Color'], mix.inputs['Color2'])
nt.links.new(mix.outputs['Color'], bsdf.inputs['Base Color'])
print("Dat_Co variation added")

# ---------------------------------------------------------------- Fix 1b: đường nhựa + vai đất trước cổng
asph = bpy.data.materials.new('V10_Asphalt'); asph.use_nodes = True
bs = principled(asph); bs.inputs['Base Color'].default_value = (0.145, 0.14, 0.135, 1)
bs.inputs['Roughness'].default_value = 0.96
nt = asph.node_tree
n = nt.nodes.new('ShaderNodeTexNoise'); n.inputs['Scale'].default_value = 0.6
r = nt.nodes.new('ShaderNodeValToRGB')
r.color_ramp.elements[0].color = (0.75, 0.75, 0.75, 1); r.color_ramp.elements[1].color = (1.15, 1.15, 1.15, 1)
mx = nt.nodes.new('ShaderNodeMixRGB'); mx.blend_type = 'MULTIPLY'; mx.inputs['Fac'].default_value = 1.0
tc = nt.nodes.new('ShaderNodeTexCoord')
nt.links.new(tc.outputs['Generated'], n.inputs['Vector'])
nt.links.new(n.outputs['Fac'], r.inputs['Fac'])
mx.inputs['Color1'].default_value = (0.145, 0.14, 0.135, 1)
nt.links.new(r.outputs['Color'], mx.inputs['Color2'])
nt.links.new(mx.outputs['Color'], bs.inputs['Base Color'])
box('V10_Road', (5, -49.0, -0.365), (175, 10.4, 0.05), asph)
dirt = bpy.data.materials.new('V10_Shoulder'); dirt.use_nodes = True
bs2 = principled(dirt); bs2.inputs['Base Color'].default_value = (0.30, 0.25, 0.17, 1)
bs2.inputs['Roughness'].default_value = 1.0
box('V10_Shoulder', (5, -43.3, -0.36), (175, 1.2, 0.05), dirt)
print("Road + shoulder added")

# ---------------------------------------------------------------- Fix 1c: vòng rừng dừa dày (mesh gộp)
leaf_mats = [bpy.data.materials.get(x) for x in ('P2_LaA','P2_LaB','P2_LaC','P2_LaA2','P2_LaC2')]
leaf_mats = [x for x in leaf_mats if x]
trunk_mat = bpy.data.materials['P2_ThanCay']
print("leaf mats:", [x.name for x in leaf_mats])

# fence rect: x -52..54, y -42..53 ; expanded by 5
def outside_dist(x, y):
    return max(-57 - x, x - 59, -47 - y, y - 58)

positions = []
n_near, n_far, tries = 0, 0, 0
while (n_near < 105 or n_far < 75) and tries < 12000:
    tries += 1
    x = random.uniform(-170, 175); y = random.uniform(-155, 160)
    d = outside_dist(x, y)
    if d <= 0 or d > 100: continue
    want_near = d <= 35
    if want_near and n_near >= 105: continue
    if not want_near and n_far >= 75: continue
    # hành lang trước cổng chính (đường + tầm nhìn cổng): x 10..36, y -95..-47 thưa
    if 8 <= x <= 38 and -100 <= y < -47 and random.random() < 0.8: continue
    # không chồng cây cũ quá gần
    if any((x-px)**2 + (y-py)**2 < 30 for px, py, _ in positions): continue
    positions.append((x, y, want_near))
    if want_near: n_near += 1
    else: n_far += 1
print("forest positions:", len(positions), "near:", sum(1 for p in positions if p[2]))

trunk_verts, trunk_faces = [], []
can_verts, can_faces, can_uvs, can_mats = [], [], [], []
def add_trunk(x, y, h, r):
    base = len(trunk_verts)
    lean = random.uniform(-0.4, 0.4)
    for i in range(4):
        a = i * math.pi/2 + math.pi/4
        trunk_verts.append((x + r*math.cos(a), y + r*math.sin(a), -0.4))
    for i in range(4):
        a = i * math.pi/2 + math.pi/4
        trunk_verts.append((x + lean + r*0.7*math.cos(a), y + r*0.7*math.sin(a), h))
    for i in range(4):
        j = (i+1) % 4
        trunk_faces.append((base+i, base+j, base+4+j, base+4+i))

def add_canopy(x, y, z, w, h, mi):
    # 3 vertical crossed quads + 1 horizontal top quad
    for k in range(3):
        a = k * math.pi/3 + random.uniform(-0.2, 0.2)
        dx, dy = math.cos(a)*w/2, math.sin(a)*w/2
        base = len(can_verts)
        can_verts.extend([(x-dx, y-dy, z-h/2), (x+dx, y+dy, z-h/2), (x+dx, y+dy, z+h/2), (x-dx, y-dy, z+h/2)])
        can_faces.append((base, base+1, base+2, base+3))
        can_uvs.extend([(0,0),(1,0),(1,1),(0,1)])
        can_mats.extend([mi]*4)
    base = len(can_verts)
    s = w*0.55
    can_verts.extend([(x-s, y-s, z+h/2-0.2), (x+s, y-s, z+h/2-0.2), (x+s, y+s, z+h/2-0.2), (x-s, y+s, z+h/2-0.2)])
    can_faces.append((base, base+1, base+2, base+3))
    can_uvs.extend([(0,0),(1,0),(1,1),(0,1)])
    can_mats.extend([mi]*4)

for i, (x, y, near) in enumerate(positions):
    h = random.uniform(5.5, 8.5) if near else random.uniform(6.5, 10.0)
    w = random.uniform(6.5, 9.0) if near else random.uniform(8.5, 13.0)
    add_trunk(x, y, h, 0.26)
    add_canopy(x, y, h + 1.2, w, random.uniform(3.6, 4.6), i % len(leaf_mats))
# bụi thấp sát rào ngoài
for i in range(46):
    side = random.randrange(4)
    if side == 0: x, y = random.uniform(-56, 58), random.uniform(-46.5, -44.5)
    elif side == 1: x, y = random.uniform(-56, 58), random.uniform(54.5, 57)
    elif side == 2: x, y = random.uniform(-56, -53.5), random.uniform(-44, 55)
    else: x, y = random.uniform(55.5, 58.5), random.uniform(-44, 55)
    add_canopy(x, y, 1.1, random.uniform(2.4, 3.6), random.uniform(1.6, 2.4), i % len(leaf_mats))

tm = bpy.data.meshes.new('V10_ForestTrunks')
tm.from_pydata(trunk_verts, [], trunk_faces); tm.update()
to = bpy.data.objects.new('V10_Forest_Trunks', tm); sc.collection.objects.link(to)
to.data.materials.append(trunk_mat)
cm = bpy.data.meshes.new('V10_ForestCanopy')
cm.from_pydata(can_verts, [], can_faces); cm.update()
uv = cm.uv_layers.new(name='UVMap')
# gán UV theo mặt: mỗi mặt 4 loop theo thứ tự vert
for pi, p in enumerate(cm.polygons):
    for li, v in zip(p.loop_indices, [(0,0),(1,0),(1,1),(0,1)]):
        uv.data[li].uv = v
    p.material_index = can_mats[pi*4]
for lm in leaf_mats: cm.materials.append(lm)
co = bpy.data.objects.new('V10_Forest_Canopy', cm); sc.collection.objects.link(co)
print("forest built: trunks", len(trunk_faces), "canopy faces", len(can_faces))

# ---------------------------------------------------------------- Fix 2: tháp cổng (hốc + tượng + chóp ngói)
# chọn các mảnh tượng A Di Đà (WhiteStone/HairStone trong bbox tượng)
parts = []
for o in bpy.data.objects:
    if o.type != 'MESH': continue
    mnames = [mm.name for mm in o.data.materials if mm]
    if not any(x in ('WhiteStone', 'HairStone') for x in mnames): continue
    bb = bbox(o); cx, cy = (bb[0]+bb[1])/2, (bb[2]+bb[3])/2
    if -17.5 <= cx <= -10.5 and -33.5 <= cy <= -28.0 and bb[5] <= 11.5:
        parts.append(o)
print("statue parts for niche:", [p.name for p in parts])
ux0 = min(bbox(p)[0] for p in parts); ux1 = max(bbox(p)[1] for p in parts)
uy0 = min(bbox(p)[2] for p in parts); uy1 = max(bbox(p)[3] for p in parts)
uz0 = min(bbox(p)[4] for p in parts); uz1 = max(bbox(p)[5] for p in parts)
print("statue union bbox:", [round(v,2) for v in (ux0,ux1,uy0,uy1,uz0,uz1)])
pivot = Vector(((ux0+ux1)/2, (uy0+uy1)/2, max(uz0, 2.9)))
body_h = uz1 - pivot.z
s = 1.58 / body_h
gomtru = bpy.data.materials['P1_GomTru']; govang = bpy.data.materials['Gờ vàng']
darkin = bpy.data.materials['DarkInset']; darkst = bpy.data.materials['DarkStone']
maihang = bpy.data.materials.get('Mai_Ngoi_Hang')
has_tex = maihang and any(n.type == 'TEX_IMAGE' for n in maihang.node_tree.nodes)
cap_mat = maihang if has_tex else bpy.data.materials['Mai_Ngoi_Layout']
print("gate cap material:", cap_mat.name)

for gx in (23.0, 45.0):
    tag = 'PT' if gx == 23.0 else 'TD'
    box(f'V10_NicheBack_{tag}', (gx, -39.78, 8.62), (5.6, 0.34, 2.0), gomtru)
    box(f'V10_NicheInset_{tag}', (gx, -39.58, 8.62), (3.3, 0.05, 1.8), darkin)
    box(f'V10_NicheTrimT_{tag}', (gx, -39.56, 9.55), (3.7, 0.1, 0.16), govang)
    box(f'V10_NicheTrimL_{tag}', (gx-1.76, -39.56, 8.62), (0.16, 0.1, 1.95), govang)
    box(f'V10_NicheTrimR_{tag}', (gx+1.76, -39.56, 8.62), (0.16, 0.1, 1.95), govang)
    box(f'V10_NichePlinth_{tag}', (gx, -39.42, 7.86), (1.15, 0.75, 0.13), darkst)
    M = Matrix.Translation((gx, -39.42, 7.93)) @ Matrix.Scale(s, 4) @ Matrix.Translation(-pivot)
    for p in parts:
        d = p.copy(); d.data = p.data; d.name = f'V10_GateBuddha_{tag}_{p.name}'
        sc.collection.objects.link(d)
        d.matrix_world = M @ p.matrix_world
    # chóp mái ngói 2 dốc + bờ nóc + bảo châu
    for sgn in (-1, 1):
        bpy.ops.mesh.primitive_cube_add(location=(gx, -39 + sgn*0.78, 10.72))
        o = bpy.context.active_object; o.name = f'V10_GateCap_{tag}_{sgn}'
        o.dimensions = (8.4, 2.05, 0.12); o.rotation_euler = (sgn*0.62, 0, 0)
        bpy.ops.object.transform_apply(scale=True, rotation=True)
        o.data.materials.append(cap_mat)
        box(f'V10_GateEave_{tag}_{sgn}', (gx, -39 + sgn*1.68, 10.24), (8.4, 0.16, 0.09), govang)
    box(f'V10_GateRidge_{tag}', (gx, -39.0, 11.34), (8.6, 0.26, 0.2), govang)
    for fx, fz in ((-4.15, 10.35), (4.15, 10.35), (0, 11.62)):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.17, location=(gx+fx, -39.0, fz))
        o = bpy.context.active_object; o.name = f'V10_GateFinial_{tag}'
        o.data.materials.append(govang)
print("gate towers done")

# ---------------------------------------------------------------- Fix 3: mái chánh điện biến thiên + bờ nóc
m = bpy.data.materials['Mai_Ngoi_Layout']; nt = m.node_tree
tc = None
for n in nt.nodes:
    if n.type == 'TEX_COORD': tc = n
noise = nt.nodes.new('ShaderNodeTexNoise'); noise.inputs['Scale'].default_value = 0.22
noise.inputs['Detail'].default_value = 3.0
ramp = nt.nodes.new('ShaderNodeValToRGB')
ramp.color_ramp.elements[0].position = 0.25; ramp.color_ramp.elements[0].color = (0.60, 0.53, 0.50, 1)
ramp.color_ramp.elements[1].position = 0.75; ramp.color_ramp.elements[1].color = (1.09, 1.04, 1.0, 1)
nt.links.new(tc.outputs['Object'], noise.inputs['Vector'])
nt.links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
insert_multiply(m, color2_node_out=ramp.outputs['Color'], label='_Roof')
print("roof variation added")

roof = bpy.data.objects['Mai_Chinh_Dien']
rb = bbox(roof)
print("roof bbox:", [round(v,1) for v in rb])
# đỉnh nóc: verts gần z max
import bmesh
verts = [roof.matrix_world @ v.co for v in roof.data.vertices]
zmax = max(v.z for v in verts)
top = [v for v in verts if v.z > zmax - 0.35]
tx = (min(v.x for v in top) + max(v.x for v in top))/2; ty = (min(v.y for v in top) + max(v.y for v in top))/2
xspan = max(v.x for v in top) - min(v.x for v in top); yspan = max(v.y for v in top) - min(v.y for v in top)
print("ridge top: center", round(tx,1), round(ty,1), "zmax", round(zmax,1), "xspan", round(xspan,1), "yspan", round(yspan,1))
rdark = bpy.data.materials.new('V10_RoofDark'); rdark.use_nodes = True
principled(rdark).inputs['Base Color'].default_value = (0.135, 0.062, 0.045, 1)
principled(rdark).inputs['Roughness'].default_value = 0.9
if xspan >= yspan and xspan > 3:
    bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=xspan*0.92, location=(tx, ty, zmax+0.02), rotation=(0, math.radians(90), 0))
    o = bpy.context.active_object; o.name = 'V10_RidgeRoll'; o.data.materials.append(rdark)
    for fx in (tx - xspan*0.42, tx, tx + xspan*0.42):
        bpy.ops.mesh.primitive_cone_add(radius1=0.24, radius2=0.02, depth=0.55, location=(fx, ty, zmax+0.3))
        o = bpy.context.active_object; o.name = 'V10_RidgeFinial'; o.data.materials.append(govang)
    print("ridge roll added along X")
else:
    print("ridge skipped (no clear ridge line)")

# ---------------------------------------------------------------- Fix 4: dải lattice mặt tiền
img = bpy.data.images.load('/home/hatch/workspace/chua-online-work/textures/v10_lattice.png')
img.pack()
lm = bpy.data.materials.new('V10_Lattice'); lm.use_nodes = True
nt = lm.node_tree; bs = principled(lm)
tex = nt.nodes.new('ShaderNodeTexImage'); tex.image = img; tex.extension = 'REPEAT'
tco = nt.nodes.new('ShaderNodeTexCoord'); mp = nt.nodes.new('ShaderNodeMapping')
mp.inputs['Scale'].default_value = (10, 1, 1)
nt.links.new(tco.outputs['Generated'], mp.inputs['Vector'])
nt.links.new(mp.outputs['Vector'], tex.inputs['Vector'])
nt.links.new(tex.outputs['Color'], bs.inputs['Base Color'])
bs.inputs['Roughness'].default_value = 0.8
band = box('V10_FacadeBand', (23, -2.36, 6.95), (29.5, 0.24, 1.15), lm)
box('V10_FacadeTrimB', (23, -2.38, 6.30), (29.5, 0.26, 0.12), govang)
box('V10_FacadeTrimT', (23, -2.38, 7.60), (29.5, 0.26, 0.12), govang)
print("facade band added")

# ---------------------------------------------------------------- Fix 5: hồ tối hơn + lá sen
m = bpy.data.materials['Nước hồ']
for n in m.node_tree.nodes:
    if n.type == 'VALTORGB':
        n.color_ramp.elements[0].color = (0.026, 0.050, 0.017, 1)
        n.color_ramp.elements[1].color = (0.052, 0.092, 0.028, 1)
principled(m).inputs['Roughness'].default_value = 0.16
leaf = bpy.data.materials['LaSenXanh']; pink = bpy.data.materials['CanhSenHong']
for ci, (cx, cy) in enumerate(((5.0, -16.0), (41.0, -16.0))):
    vs, fs, ms = [], [], []
    for i in range(17):
        px = cx + random.uniform(-8.2, 8.2); py = cy + random.uniform(-6.2, 6.2)
        r = random.uniform(0.32, 0.62); seg = 9; base = len(vs)
        vs.append((px, py, 0.125))
        for k in range(seg):
            a = k/seg*2*math.pi
            vs.append((px + r*math.cos(a), py + r*math.sin(a), 0.12))
        for k in range(seg):
            fs.append((base, base+1+k, base+1+(k+1) % seg))
        ms += [0]*(seg)
        if i % 4 == 0:
            b2 = len(vs); rr = 0.10
            vs.append((px+0.2, py+0.15, 0.21))
            for k in range(7):
                a = k/7*2*math.pi
                vs.append((px+0.2 + rr*math.cos(a), py+0.15 + rr*math.sin(a), 0.15))
            for k in range(7):
                fs.append((b2, b2+1+k, b2+1+(k+1) % 7))
            ms += [1]*7
    me = bpy.data.meshes.new(f'V10_Lily{ci}')
    me.from_pydata(vs, [], fs); me.update()
    me.materials.append(leaf); me.materials.append(pink)
    for pi, p in enumerate(me.polygons): p.material_index = ms[pi]
    ob = bpy.data.objects.new(f'V10_Lily_{ci}', me); sc.collection.objects.link(ob)
print("ponds done")

# ---------------------------------------------------------------- Fix 7: dời cây V9 khỏi trục cổng
t = bpy.data.objects.get('V9_Than.009')
if t:
    print("V9_Than.009 at", [round(v,1) for v in t.location])
    delta = Vector((-5.5, 1.0, 0))
    t.location = t.location + delta
    # tán của nó: tìm object V9_Tan* có bbox tâm gần vị trí cũ
    for o in bpy.data.objects:
        if o.type == 'MESH' and o.name.startswith('V9_Tan'):
            bb = bbox(o); cx, cy = (bb[0]+bb[1])/2, (bb[2]+bb[3])/2
            if abs(cx - 20) < 2.5 and abs(cy + 36) < 2.5:
                o.location = o.location + delta
                print("moved canopy", o.name)
else:
    print("V9_Than.009 NOT FOUND")

# ---------------------------------------------------------------- Fix 8: Cam_Flycam khớp ref9 hơn
cam = bpy.data.objects['Cam_Flycam']
cam.location = (-2, -97, 57)
target = Vector((5, 2, 1))
d = (target - cam.location).normalized()
cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
print("flycam moved, lens", cam.data.lens)

bpy.ops.wm.save_as_mainfile(filepath="/home/hatch/workspace/chua-online-work/layout_v12_v10.blend")
print("SAVED layout_v12_v10.blend")
