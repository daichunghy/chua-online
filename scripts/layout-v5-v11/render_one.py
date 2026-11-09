import bpy, sys
argv = sys.argv[sys.argv.index('--')+1:]
cam_name, out = argv[0], argv[1]
sc = bpy.context.scene
cam = bpy.data.objects.get(cam_name)
assert cam is not None, "missing camera " + cam_name
sc.camera = cam
sc.render.filepath = out
bpy.ops.render.render(write_still=True)
print("RENDERED", cam_name, "->", out, flush=True)
