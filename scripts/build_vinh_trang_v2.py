import bpy, math, os
from mathutils import Vector

OUT = os.path.expanduser("~/workspace/vinh-trang-3d")
os.makedirs(OUT, exist_ok=True)

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

def mat(name, color, rough=0.85):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    m.diffuse_color = (*color, 1.0)
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    return m

YELLOW  = mat("GoldenYellow", (1.00, 0.74, 0.22))
YELLOW2 = mat("PaleYellow",   (1.00, 0.85, 0.45))
CREAM   = mat("Cream",  (1.00, 0.93, 0.75))
WHITE   = mat("White",  (0.97, 0.97, 0.96))
ROOF    = mat("Roof",   (0.88, 0.38, 0.16))
ROOF2   = mat("Roof2",  (0.75, 0.25, 0.12))
GOLD    = mat("Gold",   (1.00, 0.80, 0.30), 0.45)
RED     = mat("Red",    (0.74, 0.12, 0.10))
BROWN   = mat("Brown",  (0.40, 0.24, 0.13))
DARK    = mat("Dark",   (0.16, 0.12, 0.10))
TEAL    = mat("Teal",   (0.20, 0.60, 0.58))
GREEN   = mat("Green",  (0.35, 0.72, 0.32))
GREEN2  = mat("Green2", (0.20, 0.55, 0.24))
GREEN3  = mat("Green3", (0.55, 0.82, 0.40))
GROUND  = mat("Ground", (0.50, 0.78, 0.40))
STONE   = mat("Stone",  (0.78, 0.76, 0.72))
PAVE    = mat("Paving", (0.86, 0.82, 0.74))
PINK    = mat("Bougainvillea", (0.98, 0.35, 0.62))
PINK2   = mat("Pink",   (1.00, 0.60, 0.75))
BLUE    = mat("LotusBlue", (0.35, 0.65, 0.95))
GREY    = mat("StoneDark", (0.45, 0.45, 0.48))

def finish(o, material):
    if material: o.data.materials.append(material)
    return o

def box(name, loc, dims, material, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.active_object; o.name = name; o.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel > 0:
        mod = o.modifiers.new("soft", 'BEVEL'); mod.width = bevel; mod.segments = 2
    return finish(o, material)

def sphere(name, loc, radius, material, scale=(1,1,1)):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=loc, segments=24, ring_count=16)
    o = bpy.context.active_object; o.name = name; o.scale = scale
    for p in o.data.polygons: p.use_smooth = True
    return finish(o, material)

def cyl(name, loc, radius, depth, material, r2=None, verts=24):
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=radius,
        radius2=radius if r2 is None else r2, depth=depth, location=loc)
    o = bpy.context.active_object; o.name = name
    if verts > 8:
        for p in o.data.polygons: p.use_smooth = True
    return finish(o, material)

def cone(name, loc, r1, r2, depth, material, verts=20):
    return cyl(name, loc, r1, depth, material, r2=r2, verts=verts)

def roof(name, loc, w, d, h, material=ROOF):
    o = cone(name, loc, 1.0, 0.02, h, material, verts=4)
    o.rotation_euler = (0, 0, math.radians(45))
    o.scale = (w/1.414, d/1.414, 1.0)
    box(name+"_eave", (loc[0], loc[1], loc[2]-h/2+0.05), (w*1.05, d*1.05, 0.13), GOLD)
    for sx in (-1,1):
        for sy in (-1,1):
            c = cone(name+"_tip", (loc[0]+sx*w*0.48, loc[1]+sy*d*0.48, loc[2]-h/2+0.26),
                     0.02, 0.15, 0.45, GOLD, verts=10)
            c.rotation_euler = (sy*0.5, -sx*0.5, 0)
    return o

def text_obj(txt, loc, size, material):
    bpy.ops.object.text_add(location=loc, rotation=(math.radians(90),0,0))
    o = bpy.context.active_object; o.name = "Text_"+txt
    o.data.body = txt; o.data.size = size
    o.data.align_x = 'CENTER'; o.data.align_y = 'CENTER'; o.data.extrude = 0.03
    return finish(o, material)

def arch(x, y, z, w, h, material=DARK):
    box("Arch", (x, y, z+h/2), (w, 0.14, h), material)
    c = cyl("ArchTop", (x, y, z+h), w/2, 0.14, material)
    c.rotation_euler = (math.radians(90), 0, 0)

def tree(x, y, s=1.0):
    cyl("Trunk", (x, y, 0.7*s), 0.16*s, 1.4*s, BROWN)
    sphere("Leaf", (x, y, 1.9*s), 1.05*s, GREEN)
    sphere("Leaf", (x-0.6*s, y+0.2*s, 1.5*s), 0.7*s, GREEN2)
    sphere("Leaf", (x+0.6*s, y-0.15*s, 1.6*s), 0.75*s, GREEN3)

def palm(x, y, s=1.0):
    t = cyl("PalmTrunk", (x, y, 1.6*s), 0.13*s, 3.2*s, BROWN)
    t.rotation_euler = (0.06, 0.04, 0)
    for a in range(6):
        ang = a * math.pi/3
        f = sphere("PalmFrond", (x+math.cos(ang)*0.85*s, y+math.sin(ang)*0.85*s, 3.35*s),
                   0.85*s, GREEN2, scale=(1.4, 0.45, 0.18))
        f.rotation_euler = (0, 0, ang)

def bonsai(x, y, s=1.0):
    cyl("Pot", (x, y, 0.35*s), 0.55*s, 0.7*s, ROOF2, r2=0.42*s)
    cyl("BonsaiTrunk", (x, y, 0.85*s), 0.09*s, 0.4*s, BROWN)
    sphere("BonsaiTop", (x, y, 1.35*s), 0.55*s, GREEN2, scale=(1.25,1.25,0.55))
    sphere("BonsaiTop", (x, y, 1.75*s), 0.42*s, GREEN, scale=(1.2,1.2,0.5))

# ---------- ground ----------
world = bpy.data.worlds["World"]; world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.60, 0.82, 1.0, 1)
box("Ground", (0, 0, -0.3), (40, 30, 0.6), GROUND)
box("SkyBackdrop", (0, 19, 14), (130, 1.0, 60), mat("Sky", (0.55, 0.80, 0.99)))
box("SkyBackdropSide", (-32, 0, 14), (1.0, 60, 60), mat("Sky", (0.55, 0.80, 0.99)))
box("Courtyard", (0, -2.0, 0.04), (24, 15, 0.10), PAVE)
box("Path", (0, -9.0, 0.08), (3.6, 5.0, 0.10), STONE)
for (x,y,z,s) in [(-12,8,11,1.2),(11,10,12,1.5),(1,13,12.5,1.0)]:
    sphere("Cloud",(x,y,z),0.8*s,WHITE); sphere("Cloud",(x+0.9*s,y,z-0.1*s),0.6*s,WHITE)
    sphere("Cloud",(x-0.9*s,y,z-0.1*s),0.55*s,WHITE)

# ---------- MAIN HALL: golden facade, many arches (from photos) ----------
box("HallPlatform", (0, 4.2, 0.35), (19, 7.5, 0.7), STONE)
box("MainBody", (0, 4.2, 2.35), (17.5, 5.6, 3.3), YELLOW, bevel=0.05)
# white lattice frieze band + gold cornice
box("Frieze", (0, 1.32, 3.55), (17.7, 0.18, 0.55), WHITE)
for x in [i*1.1-8.25 for i in range(16)]:
    box("FriezeHole", (x, 1.24, 3.55), (0.45, 0.06, 0.3), YELLOW2)
box("Cornice", (0, 1.32, 4.05), (17.9, 0.22, 0.22), GOLD)
# low terracotta roof behind cornice
roof("HallRoof", (0, 5.3, 4.80), 17.0, 5.4, 0.9, ROOF)
# central ornate tower (Khmer-style gable)
box("CenterTower", (0, 3.6, 5.3), (3.6, 2.2, 1.6), YELLOW2, bevel=0.04)
box("CenterTower2", (0, 3.6, 6.35), (2.4, 1.7, 0.9), YELLOW, bevel=0.04)
roof("CenterRoof", (0, 3.6, 7.45), 3.0, 2.2, 1.4, ROOF)
sphere("CenterFinial", (0, 3.6, 8.35), 0.2, GOLD)
box("CenterPlaque", (0, 2.45, 5.3), (1.7, 0.14, 0.8), RED)
text_obj("VINH TRANG", (0, 2.36, 5.3), 0.34, GOLD)
# two end towers
for side in (-1,1):
    x = side*8.1
    box("EndTower", (x, 3.4, 4.9), (1.9, 1.6, 2.2), YELLOW2, bevel=0.04)
    roof("EndRoof", (x, 3.4, 6.45), 2.3, 2.0, 1.0, ROOF)
    box("EndPlaque", (x, 2.55, 5.15), (0.95, 0.12, 0.95), GOLD)
    text_obj("PHUC", (x, 2.47, 5.15), 0.30, RED)
# arched openings row: 9 arches, red pillars between
for i in range(9):
    x = -7.6 + i*1.9
    arch(x, 1.34, 0.75, 1.25, 2.1)
    sphere("GrilleDot", (x, 1.25, 1.9), 0.10, GOLD)
for i in range(10):
    x = -8.55 + i*1.9
    cyl("RedPillar", (x, 1.28, 1.95), 0.14, 2.7, RED)
# central staircase with white balustrade
for i in range(4):
    box("Stair", (0, 0.6-i*0.55, 0.62-i*0.17), (3.4, 0.55, 0.16), STONE)
for side in (-1,1):
    r = box("Balustrade", (side*1.85, 0.05, 1.05), (0.22, 2.8, 0.18), WHITE)
    r.rotation_euler = (math.radians(-32), 0, 0)
    cyl("BalusterPost", (side*1.85, -0.55, 0.55), 0.13, 1.0, GOLD)
for x,y in [(-3.4,-1.2),(3.4,-1.2),(-5.6,-1.0),(5.6,-1.0)]:
    bonsai(x, y, 1.15)

# side annex buildings
for side in (-1,1):
    x = side*11.6
    box("Annex", (x, 5.2, 1.25), (3.6, 4.6, 2.1), YELLOW2, bevel=0.05)
    arch(x, 2.85, 0.25, 1.1, 1.6, BROWN)
    roof("AnnexRoof", (x, 5.2, 3.05), 4.6, 5.6, 1.3, ROOF2)

# ---------- TAM QUAN GATE ----------
for x,w,h in [(0,2.6,3.4),(-2.9,1.7,2.4),(2.9,1.7,2.4)]:
    box("GatePost", (x-(w/2+0.18), -11.5, h/2), (0.36, 0.7, h), YELLOW)
    box("GatePost", (x+(w/2+0.18), -11.5, h/2), (0.36, 0.7, h), YELLOW)
    box("GateLintel", (x, -11.5, h+0.25), (w+0.8, 0.8, 0.5), YELLOW2)
    arch(x, -11.9, 0, w*0.72, h*0.78)
box("GatePlaque", (0, -11.95, 3.95), (3.4, 0.16, 0.65), RED)
text_obj("TAM QUAN", (0, -12.05, 3.95), 0.4, GOLD)
roof("GateRoof", (0, -11.5, 4.95), 4.6, 2.2, 1.3, ROOF)
roof("GateRoofL", (-2.9, -11.5, 3.75), 3.0, 1.9, 1.0, ROOF2)
roof("GateRoofR", ( 2.9, -11.5, 3.75), 3.0, 1.9, 1.0, ROOF2)
sphere("GateFinial", (0, -11.5, 5.95), 0.2, GOLD)

# ---------- AMITABHA standing, white, blue lotus (left) ----------
bx, by = -8.6, -2.2
box("AmitabhaBase", (bx, by, 0.45), (3.2, 3.2, 0.9), ROOF2)
cyl("LotusPed", (bx, by, 1.15), 1.35, 0.5, BLUE, verts=16)
for i in range(8):
    a = i*math.pi/4
    p = cone("LotusPetal", (bx+math.cos(a)*1.05, by+math.sin(a)*1.05, 1.35),
             0.05, 0.34, 0.55, BLUE, verts=8)
    p.rotation_euler = (math.sin(a)*0.6, -math.cos(a)*0.6, 0)
cyl("AmitabhaRobe", (bx, by, 3.35), 0.98, 3.5, WHITE, r2=0.52)
sphere("AmitabhaHead", (bx, by, 5.5), 0.52, WHITE)
sphere("AmitabhaBun", (bx, by, 6.05), 0.24, WHITE)
# raised left hand
cyl("AmitabhaArm", (bx-0.62, by-0.2, 4.35), 0.14, 1.1, WHITE)
sphere("AmitabhaHand", (bx-0.62, by-0.2, 5.0), 0.18, WHITE)
sphere("AmitabhaHand2", (bx+0.45, by-0.5, 3.3), 0.17, WHITE)

# ---------- MAITREYA laughing, white, beads (front right) ----------
mx, my = 8.4, -3.2
box("MaitreyaPlatform", (mx, my, 0.4), (4.6, 3.6, 0.8), GREY)
box("MaitreyaPlatformTop", (mx, my, 0.9), (4.0, 3.0, 0.25), STONE)
sphere("MaitreyaBelly", (mx, my, 1.95), 1.15, WHITE, scale=(1.15,0.95,1.1))
sphere("MaitreyaHead", (mx, my, 3.55), 0.62, WHITE)
sphere("MaitreyaEar", (mx-0.62, my, 3.42), 0.17, WHITE, scale=(0.6,0.6,1.5))
sphere("MaitreyaEar", (mx+0.62, my, 3.42), 0.17, WHITE, scale=(0.6,0.6,1.5))
sphere("MaitreyaLeg", (mx-1.15, my-0.5, 1.25), 0.48, WHITE)
sphere("MaitreyaLeg", (mx+1.15, my-0.5, 1.25), 0.48, WHITE)
sphere("MaitreyaEye", (mx-0.21, my-0.56, 3.66), 0.06, DARK)
sphere("MaitreyaEye", (mx+0.21, my-0.56, 3.66), 0.06, DARK)
bpy.ops.mesh.primitive_torus_add(major_radius=0.24, minor_radius=0.05,
    major_segments=20, minor_segments=8, location=(mx, my-0.60, 3.38),
    rotation=(0,0,math.radians(180)))
finish(bpy.context.active_object, RED)
# prayer beads: small spheres in a loop on chest
for i in range(11):
    a = math.pi*0.15 + i*(math.pi*0.7/10)
    sphere("Bead", (mx+math.cos(a+math.pi/2)*0.78, my-0.88, 2.95-math.sin(a)*0.75), 0.085, GREY)
text_obj("DI LAC", (mx, my-1.86, 0.45), 0.34, GOLD)

# ---------- 7-STOREY TOWER (back right) ----------
tx, ty = 13.2, 8.6
box("TowerBase", (tx, ty, 0.4), (3.4, 3.4, 0.8), STONE)
lvl_w = 2.5
for i in range(7):
    z = 0.8 + i*1.05
    box("TowerLvl", (tx, ty, z+0.32), (lvl_w, lvl_w, 0.64), YELLOW2, bevel=0.03)
    arch(tx, ty-lvl_w/2-0.02, z+0.08, 0.5, 0.5, BROWN)
    roof("TowerRoof", (tx, ty, z+0.92), lvl_w+0.85, lvl_w+0.85, 0.5, ROOF)
    lvl_w *= 0.93
cone("TowerSpire", (tx, ty, 9.15), 0.02, 0.22, 0.9, RED)
sphere("TowerFinial", (tx, ty, 9.7), 0.13, GOLD)

# ---------- RECLINING BUDDHA (back left garden) ----------
rx, ry = -9.5, 8.8
box("ReclineBase", (rx, ry, 0.45), (6.2, 2.0, 0.9), STONE)
sphere("ReclineBody", (rx+0.4, ry, 1.35), 1.0, WHITE, scale=(2.55, 0.85, 0.72))
sphere("ReclineHead", (rx-2.35, ry, 1.6), 0.62, WHITE)
sphere("ReclineHair", (rx-2.35, ry, 2.12), 0.34, DARK)
box("ReclineArm", (rx-1.95, ry-0.55, 1.0), (0.35, 0.35, 1.1), WHITE)

# ---------- LOTUS POND (foreground centre-left) ----------
px, py = -4.6, -9.6
cyl("Pond", (px, py, 0.12), 2.3, 0.24, BLUE, verts=28)
cyl("PondRim", (px, py, 0.06), 2.55, 0.12, STONE, verts=28)
for (lx,ly) in [(-0.9,0.4),(0.7,-0.5),(0.1,0.9),(-0.3,-1.0)]:
    cyl("LilyPad", (px+lx, py+ly, 0.27), 0.42, 0.05, GREEN2, verts=14)
for (lx,ly) in [(0.5,0.6),(-0.8,-0.4)]:
    cone("Lotus", (px+lx, py+ly, 0.55), 0.05, 0.30, 0.5, PINK2, verts=10)

# ---------- greenery ----------
for (x,y,s) in [(-15,-4,1.2),(15,-5,1.2),(-6,11,1.3),(3,12,1.15),(-15,11,1.0)]:
    tree(x,y,s)
for (x,y,s) in [(12,-9.5,1.1),(-13,-9,1.0),(5.5,10.5,1.05),(-3,7.5,0.9)]:
    palm(x,y,s)
for x in (-6.2,-4.4,4.4,6.2):
    sphere("Bougainvillea", (x, -5.6, 0.5), 0.62, PINK, scale=(1.15,1,0.8))
    sphere("Bush", (x, -5.6, 0.3), 0.55, GREEN2, scale=(1,1,0.7))
for x in (-2.8, 2.8):
    for y in (-6.8, -11.0):
        cyl("LampPost", (x, y, 0.6), 0.07, 1.2, DARK)
        sphere("Lamp", (x, y, 1.35), 0.22, GOLD)

# ---------- lights & camera ----------
bpy.ops.object.light_add(type='SUN', location=(8,-6,16))
sun = bpy.context.active_object; sun.data.energy = 3.0
sun.rotation_euler = (math.radians(50), 0, math.radians(30))
bpy.ops.object.camera_add()
cam = bpy.context.active_object; bpy.context.scene.camera = cam; cam.data.lens = 38

def look_at(obj, target):
    d = Vector(target) - obj.location
    obj.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()

scene = bpy.context.scene
scene.render.engine = 'BLENDER_WORKBENCH'
sh = scene.display.shading
sh.light = 'FLAT'; sh.color_type = 'MATERIAL'
sh.show_shadows = False
try:
    sh.background_type = 'VIEWPORT'
    sh.background_color = (0.58, 0.81, 0.98)
except Exception as e:
    print("bg skip", e)
scene.render.resolution_x = 1280; scene.render.resolution_y = 960
scene.render.image_settings.file_format = 'PNG'
scene.render.film_transparent = False
try:
    scene.view_settings.view_transform = 'Standard'
    scene.view_settings.look = 'None'
except Exception as e:
    print("view transform skip", e)

views = [
    ("preview_front.png", (0, -26, 5.0),  (0, 0, 2.6)),
    ("preview_hero.png",  (15, -17, 10),  (0, 0, 2.2)),
    ("preview_side.png",  (21, -4, 7.5),  (0, 1, 2.2)),
]
for fname, loc, tgt in views:
    cam.location = loc; look_at(cam, tgt)
    scene.render.filepath = os.path.join(OUT, fname)
    bpy.ops.render.render(write_still=True)
    print("RENDERED", fname)

bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "Chua_Vinh_Trang_Cartoon3D.blend"))
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, "Chua_Vinh_Trang_Cartoon3D.glb"), export_format='GLB')
print("DONE_OK")
