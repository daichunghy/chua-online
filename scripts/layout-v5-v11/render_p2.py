import bpy
sc = bpy.context.scene
sc.render.engine = 'CYCLES'
sc.cycles.samples = 32
sc.cycles.use_denoising = True
sc.render.resolution_x = 1280
sc.render.resolution_y = 720
OUT = "/home/hatch/workspace/chua-online-work/layout/"
for cam_name, fname in (("Cam_Flycam", "layout_v7_flycam.png"),
                        ("Cam_Ground", "layout_v7_ground.png"),
                        ("Cam_Gate", "layout_v7_gate.png"),
                        ("Cam_DiLac", "layout_v7_dilac.png")):
    cam = bpy.data.objects.get(cam_name)
    assert cam is not None, cam_name
    sc.camera = cam
    sc.render.filepath = OUT + fname
    bpy.ops.render.render(write_still=True)
    print("RENDERED", fname, flush=True)
print("ALL P2 RENDERS DONE", flush=True)
