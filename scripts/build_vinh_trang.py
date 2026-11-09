import bpy, math, os
from mathutils import Vector

OUT = os.path.expanduser("~/workspace/vinh-trang-3d")
os.makedirs(OUT, exist_ok=True)

# ---------- clean ----------
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for coll in (bpy.data.meshes, bpy.data.curves, bpy.data.cameras, bpy.data.lights):
    pass

# ---------- materials (cartoon: bright, flat) ----------
def mat(name, color, rough=0.85):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = rough
    return m

CREAM   = mat("Cream",  (1.00, 0.90, 0.68))
CREAM2  = mat("Cream2", (1.00, 0.96, 0.82))
WHITE   = mat("White",  (0.98, 0.98, 0.97))
ROOF    = mat("Roof",   (0.85, 0.32, 0.20))
ROOF2   = mat("Roof2",  (0.72, 0.22, 0.14))
GOLD    = mat("Gold",   (1.00, 0.76, 0.25), 0.45)
RED     = mat("Red",    (0.72, 0.10, 0.10))
BROWN   = mat("Brown",  (0.38, 0.22, 0.12))
DARK    = mat("Dark",   (0.20, 0.13, 0.09))
TEAL    = mat("Teal",   (0.15, 0.55, 0.55))
GREEN   = mat("Green",  (0.35, 0.72, 0.32))
GREEN2  = mat("Green2", (0.22, 0.58, 0.25))
GREEN3  = mat("Green3", (0.55, 0.82, 0.40))
GROUND  = mat("Ground", (0.48, 0.78, 0.38))
SAND    = mat("Sand",   (0.96, 0.87, 0.66))
STONE   = mat("Stone",  (0.82, 0.82, 0.80))
PINK    = mat("Pink",   (1.00, 0.55, 0.70))
BLUE    = mat("Blue",   (0.35, 0.70, 0.95))
SKIN    = mat("Skin",   (1.00, 0.82, 0.62))
ORANGE  = mat("Orange", (0.98, 0.60, 0.18))
GREY    = mat("Grey",   (0.90, 0.90, 0.90))

def finish(obj, material):
    if material:
        obj.data.materials.append(material)
    return obj

def box(name, loc, dims, material, bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.active_object; o.name = name
    o.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel > 0:
        mod = o.modifiers.new("soft", 'BEVEL'); mod.width = bevel; mod.segments = 2
    return finish(o, material)

def sphere(name, loc, radius, material, scale=(1,1,1)):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=loc, segments=28, ring_count=18)
    o = bpy.context.active_object; o.name = name; o.scale = scale
    return finish(o, material)

def cyl(name, loc, radius, depth, material, r2=None, verts=24):
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=radius,
        radius2=radius if r2 is None else r2, depth=depth, location=loc)
    o = bpy.context.active_object; o.name = name
    return finish(o, material)

def cone(name, loc, r1, r2, depth, material, verts=24):
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r1, radius2=r2, depth=depth, location=loc)
    o = bpy.context.active_object; o.name = name
    return finish(o, material)

def roof(name, loc, w, d, h, material=ROOF):
    """4-sided pyramid roof, rectangular, with gold upturned corners."""
    o = cone(name, loc, 1.0, 0.02, h, material, verts=4)
    o.rotation_euler = (0, 0, math.radians(45))
    # cone radius 1 (rotated 45deg) -> base square half-diagonal 1; scale to w/d
    o.scale = (w/1.414, d/1.414, 1.0)
    # eave slab
    box(name+"_eave", (loc[0], loc[1], loc[2]-h/2+0.06), (w*1.04, d*1.04, 0.14), GOLD)
    # upturned corners
    for sx in (-1,1):
        for sy in (-1,1):
            c = cone(name+"_tip", (loc[0]+sx*w*0.48, loc[1]+sy*d*0.48, loc[2]-h/2+0.28),
                     0.02, 0.16, 0.5, GOLD, verts=10)
            c.rotation_euler = (sy*0.5, -sx*0.5, 0)
    return o

def text_obj(txt, loc, size, material, rot=(math.radians(90),0,0)):
    bpy.ops.object.text_add(location=loc, rotation=rot)
    o = bpy.context.active_object; o.name = "Text_"+txt
    o.data.body = txt; o.data.size = size; o.data.align_x = 'CENTER'; o.data.align_y = 'CENTER'
    o.data.extrude = 0.03
    return finish(o, material)

def tree(x, y, s=1.0):
    cyl("Trunk", (x, y, 0.7*s), 0.16*s, 1.4*s, BROWN)
    sphere("Leaf", (x, y, 1.9*s), 1.05*s, GREEN)
    sphere("Leaf", (x-0.6*s, y+0.2*s, 1.5*s), 0.7*s, GREEN2)
    sphere("Leaf", (x+0.6*s, y-0.15*s, 1.6*s), 0.75*s, GREEN3)

def arch_door(x, y, z, w, h, material=DARK):
    box("Door", (x, y, z+h/2), (w, 0.14, h), material)
    c = cyl("DoorArch", (x, y, z+h), w/2, 0.14, material)
    c.rotation_euler = (math.radians(90), 0, 0)

# ---------- world / ground ----------
world = bpy.data.worlds["World"]; world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.62, 0.83, 1.0, 1)
world.node_tree.nodes["Background"].inputs[1].default_value = 1.0

box("Ground", (0, 0, -0.3), (38, 28, 0.6), GROUND)
box("Courtyard", (0, -3.5, 0.04), (20, 13, 0.10), SAND)
box("Path", (0, -8.2, 0.08), (3.4, 6.5, 0.10), STONE)

# cartoon clouds
for (x,y,z,s) in [(-11,7,10.5,1.2),(10,9,11.5,1.5),(0,12,12,1.0)]:
    sphere("Cloud",(x,y,z),0.8*s,WHITE)
    sphere("Cloud",(x+0.9*s,y,z-0.1*s),0.6*s,WHITE)
    sphere("Cloud",(x-0.9*s,y,z-0.1*s),0.55*s,WHITE)

# ---------- MAIN HALL (chanh dien) ----------
hz = 0.55
for i,(w,d) in enumerate([(14.5,8.5),(13.5,7.8),(12.5,7.1)]):
    box("Step", (0, 3.6, 0.15+i*0.22), (w, d, 0.3), STONE)
box("MainBody", (0, 3.6, hz+1.6), (11.5, 6.2, 3.2), CREAM, bevel=0.06)
# front pillars
for x in (-5.2,-3.1,0,3.1,5.2):
    if x == 0: continue
    cyl("Pillar", (x, 0.35, hz+1.6), 0.22, 3.2, RED)
    cyl("PillarBase", (x, 0.35, hz+0.15), 0.30, 0.3, GOLD)
# doors & windows on front face (y = 0.5)
arch_door(0, 0.44, hz, 1.9, 2.5)
arch_door(-3.4, 0.44, hz, 1.3, 2.1, BROWN)
arch_door( 3.4, 0.44, hz, 1.3, 2.1, BROWN)
for x in (-5.0, 5.0):
    arch_door(x, 0.44, hz+0.7, 0.95, 1.3, TEAL)
# side windows as simple teal boxes
for side in (-1,1):
    for yy in (2.0, 3.6, 5.2):
        box("SideWin", (side*5.78, yy, hz+1.7), (0.12, 0.9, 1.4), TEAL)
# sign plaque
box("Plaque", (0, 0.38, hz+3.05), (4.6, 0.16, 0.75), RED)
text_obj("CHUA VINH TRANG", (0, 0.28, hz+3.05), 0.42, GOLD)
# roof tier 1
roof("Roof1", (0, 3.6, hz+3.2+1.05), 13.6, 8.2, 2.1, ROOF)
# upper body + roof tier 2
box("UpperBody", (0, 3.6, hz+4.55), (7.6, 4.2, 1.5), CREAM2, bevel=0.05)
for x in (-2.6, 0, 2.6):
    arch_door(x, 1.44, hz+3.95, 0.9, 1.1, TEAL)
roof("Roof2", (0, 3.6, hz+5.3+0.85), 9.4, 5.8, 1.7, ROOF2)
# top + roof tier 3 + finial
box("TopBody", (0, 3.6, hz+6.75), (4.2, 2.6, 1.0), CREAM, bevel=0.05)
roof("Roof3", (0, 3.6, hz+7.25+0.65), 5.6, 3.6, 1.3, ROOF)
sphere("Finial", (0, 3.6, hz+8.65), 0.28, GOLD)
cone("FinialTip", (0, 3.6, hz+9.05), 0.02, 0.16, 0.6, GOLD)

# ---------- SIDE WINGS ----------
for side in (-1,1):
    x = side*9.3
    box("WingStep", (x, 3.4, 0.18), (5.6, 6.4, 0.36), STONE)
    box("Wing", (x, 3.4, 1.45), (4.8, 5.4, 2.2), CREAM2, bevel=0.06)
    arch_door(x, 0.64, 0.36, 1.2, 1.7, BROWN)
    roof("WingRoof", (x, 3.4, 3.45), 6.2, 6.8, 1.6, ROOF)

# ---------- TAM QUAN GATE ----------
gz = 0.0
for x,w,h in [(0,2.6,3.4),(-2.9,1.7,2.4),(2.9,1.7,2.4)]:
    box("GatePost", (x- (w/2+0.18), -9.5, gz+h/2), (0.36, 0.7, h), CREAM)
    box("GatePost", (x+ (w/2+0.18), -9.5, gz+h/2), (0.36, 0.7, h), CREAM)
    box("GateLintel", (x, -9.5, gz+h+0.25), (w+0.8, 0.8, 0.5), CREAM)
    arch_door(x, -9.88, gz, w*0.72, h*0.78)
box("GatePlaque", (0, -9.95, 3.95), (3.4, 0.16, 0.65), RED)
text_obj("TAM QUAN", (0, -10.05, 3.95), 0.4, GOLD)
roof("GateRoof", (0, -9.5, 4.95), 4.6, 2.2, 1.3, ROOF)
roof("GateRoofL", (-2.9, -9.5, 3.75), 3.0, 1.9, 1.0, ROOF2)
roof("GateRoofR", ( 2.9, -9.5, 3.75), 3.0, 1.9, 1.0, ROOF2)
sphere("GateFinial", (0, -9.5, 5.95), 0.2, GOLD)

# ---------- STANDING BUDDHA - A DI DA (left) ----------
bx, by = -8.2, -2.6
cyl("LotusBase", (bx, by, 0.35), 1.25, 0.7, PINK, verts=12)
cyl("LotusBase2", (bx, by, 0.85), 0.95, 0.35, WHITE, verts=12)
cyl("Robe", (bx, by, 2.75), 0.95, 3.4, WHITE, r2=0.52)
sphere("BuddhaHead", (bx, by, 4.85), 0.52, SKIN)
sphere("HairBun", (bx, by, 5.38), 0.24, DARK)
c = cyl("Halo", (bx, by+0.28, 4.85), 0.95, 0.10, GOLD); c.rotation_euler=(math.radians(90),0,0)
sphere("Hand", (bx-0.35, by-0.55, 3.1), 0.17, SKIN)
sphere("Hand", (bx+0.35, by-0.55, 3.1), 0.17, SKIN)

# ---------- MAITREYA - DI LAC laughing (front right) ----------
mx, my = 7.6, -3.4
cyl("MaitreyaBase", (mx, my, 0.4), 1.5, 0.8, PINK, verts=12)
sphere("Belly", (mx, my, 1.55), 1.05, GOLD, scale=(1,0.9,1.05))
sphere("MaitreyaHead", (mx, my, 2.95), 0.58, GOLD)
sphere("Ear", (mx-0.58, my, 2.85), 0.16, GOLD, scale=(0.6,0.6,1.4))
sphere("Ear", (mx+0.58, my, 2.85), 0.16, GOLD, scale=(0.6,0.6,1.4))
sphere("Leg", (mx-0.95, my-0.45, 0.95), 0.42, GOLD)
sphere("Leg", (mx+0.95, my-0.45, 0.95), 0.42, GOLD)
sphere("Eye", (mx-0.2, my-0.52, 3.05), 0.06, DARK)
sphere("Eye", (mx+0.2, my-0.52, 3.05), 0.06, DARK)
# smile: half torus
bpy.ops.mesh.primitive_torus_add(major_radius=0.22, minor_radius=0.045,
    major_segments=20, minor_segments=8, location=(mx, my-0.55, 2.82),
    rotation=(0, 0, math.radians(180)))
finish(bpy.context.active_object, RED)

# ---------- RECLINING BUDDHA (back right garden) ----------
rx, ry = 8.6, 8.6
box("ReclineBase", (rx, ry, 0.45), (6.0, 1.9, 0.9), STONE)
sphere("ReclineBody", (rx+0.4, ry, 1.35), 1.0, GREY, scale=(2.5, 0.85, 0.72))
sphere("ReclineHead", (rx-2.3, ry, 1.55), 0.62, SKIN)
sphere("ReclineHair", (rx-2.3, ry, 2.05), 0.34, DARK)
box("ReclineArm", (rx-1.9, ry-0.5, 1.0), (0.35, 0.35, 1.1), GREY)

# ---------- LOTUS POND (front left) ----------
px, py = -7.6, -8.6
cyl("Pond", (px, py, 0.12), 2.3, 0.24, BLUE, verts=28)
cyl("PondRim", (px, py, 0.06), 2.55, 0.12, STONE, verts=28)
for (lx,ly) in [(-0.9,0.4),(0.7,-0.5),(0.1,0.9),(-0.3,-1.0)]:
    cyl("LilyPad", (px+lx, py+ly, 0.27), 0.42, 0.05, GREEN2, verts=14)
for (lx,ly) in [(0.5,0.6),(-0.8,-0.4)]:
    cone("Lotus", (px+lx, py+ly, 0.55), 0.05, 0.30, 0.5, PINK, verts=10)

# ---------- trees, bushes, lamps ----------
for (x,y,s) in [(-13,-6,1.2),(-13,4,1.4),(13,-7,1.25),(13.5,1,1.1),(-5,9.5,1.3),(4,10,1.2),(-14,10,1.0),(14,11,1.15)]:
    tree(x,y,s)
for x in (-6.5,-4.5,4.5,6.5,-11,11):
    sphere("Bush", (x, -6.2, 0.35), 0.55, GREEN2, scale=(1,1,0.7))
for x in (-2.6, 2.6):
    for y in (-6.5, -10.5):
        cyl("LampPost", (x, y, 0.6), 0.07, 1.2, DARK)
        s = sphere("Lamp", (x, y, 1.35), 0.22, GOLD)
        s.material_slots[0].material.node_tree.nodes["Principled BSDF"].inputs["Emission Color"].default_value = (1,0.8,0.3,1)
        s.material_slots[0].material.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 0.6

# ---------- lights & camera ----------
bpy.ops.object.light_add(type='SUN', location=(8,-6,16))
sun = bpy.context.active_object; sun.data.energy = 3.2
sun.rotation_euler = (math.radians(50), 0, math.radians(30))
bpy.ops.object.light_add(type='AREA', location=(0,-12,10))
fill = bpy.context.active_object; fill.data.energy = 500; fill.data.shape='DISK'; fill.data.size=10

bpy.ops.object.camera_add()
cam = bpy.context.active_object
bpy.context.scene.camera = cam
cam.data.lens = 38

def look_at(obj, target):
    d = Vector(target) - obj.location
    obj.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()

scene = bpy.context.scene
try:
    scene.render.engine = 'BLENDER_EEVEE_NEXT'
except Exception:
    scene.render.engine = 'BLENDER_EEVEE'
scene.eevee.taa_render_samples = 64
scene.render.resolution_x = 1280
scene.render.resolution_y = 960
scene.render.image_settings.file_format = 'PNG'

views = [
    ("preview_front.png", (0, -21, 6.5),  (0, 0, 2.6)),
    ("preview_hero.png",  (14, -16, 10),  (0, 0, 2.2)),
    ("preview_side.png",  (20, -3, 7),    (0, 1, 2.2)),
]
for fname, loc, tgt in views:
    cam.location = loc; look_at(cam, tgt)
    scene.render.filepath = os.path.join(OUT, fname)
    bpy.ops.render.render(write_still=True)
    print("RENDERED", fname)

bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "Chua_Vinh_Trang_Cartoon3D.blend"))
bpy.ops.export_scene.gltf(filepath=os.path.join(OUT, "Chua_Vinh_Trang_Cartoon3D.glb"),
                          export_format='GLB')
print("DONE_OK")
