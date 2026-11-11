# V15 RENDER mat can (file dau rieng): rig don gian Sun + World sang,
# camera 3/4 truoc mat. Chay: blender -b --python render_face_v15.py --
# <blend> <out.png> <cx> <cy> <cz> [dist] [lens]
import bpy, sys
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
BLEND, OUT = argv[0], argv[1]
C = Vector((float(argv[2]), float(argv[3]), float(argv[4])))
DIST = float(argv[5]) if len(argv) > 5 else 4.6
LENS = float(argv[6]) if len(argv) > 6 else 50.0

bpy.ops.wm.open_mainfile(filepath=BLEND)
sc = bpy.context.scene
# an REF_merged khoi render (neu co)
for o in bpy.data.objects:
    if o.name.startswith("REF"):
        o.hide_render = True
# world sang
w = bpy.data.worlds.new("W")
sc.world = w
w.use_nodes = True
bg = w.node_tree.nodes["Background"]
bg.inputs[0].default_value = (0.85, 0.88, 0.95, 1.0)
bg.inputs[1].default_value = 0.75
# sun
sd = bpy.data.lights.new("SunR", 'SUN')
sd.energy = 3.0
so = bpy.data.objects.new("SunR", sd)
sc.collection.objects.link(so)
so.rotation_euler = (0.9, 0.15, 0.6)
# camera 3/4 truoc-phai
cam_data = bpy.data.cameras.new("CamR")
cam_data.lens = LENS
cam = bpy.data.objects.new("CamR", cam_data)
sc.collection.objects.link(cam)
cam.location = C + Vector((DIST * 0.42, DIST, DIST * 0.10))
def look_at(obj, pt):
    obj.rotation_euler = (pt - obj.location).to_track_quat('-Z', 'Y').to_euler()
look_at(cam, C + Vector((0, 0.25, 0.02)))
sc.camera = cam
sc.render.engine = 'CYCLES'
sc.cycles.samples = 32
sc.cycles.use_denoising = True
sc.render.resolution_x = 640
sc.render.resolution_y = 640
sc.render.filepath = OUT
bpy.ops.render.render(write_still=True)
print("V15 RENDER DONE", OUT, flush=True)
