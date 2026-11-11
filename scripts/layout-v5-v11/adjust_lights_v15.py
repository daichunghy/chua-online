# V15 ADJUST: bu sang den hoc cong sau Light Linking. Mo V18, nang
# V10_NicheFill_PT/TD tu 140W -> muc chi dinh (argv), giu nguyen linking,
# luu de len V18, render lai khung hoc (Cam_V10_Niche) de do.
# blender -b --python adjust_lights_v15.py -- <watts> <outpng>
import bpy, sys

argv = sys.argv[sys.argv.index("--") + 1:]
WATTS, OUTPNG = float(argv[0]), argv[1]
DST = "/home/hatch/workspace/chua-online-work/layout_v18_v15.blend"
bpy.ops.wm.open_mainfile(filepath=DST)
for tag in ("PT", "TD"):
    o = bpy.data.objects.get(f"V10_NicheFill_{tag}")
    old = o.data.energy
    o.data.energy = WATTS
    rc = o.light_linking.receiver_collection
    print(f"[ADJ] {tag}: {old} -> {WATTS} W, linking="
          f"{rc.name if rc else None} ({len(rc.objects) if rc else 0})",
          flush=True)
bpy.ops.wm.save_mainfile(filepath=DST)
sc = bpy.context.scene
sc.camera = bpy.data.objects["Cam_V10_Niche"]
sc.render.filepath = OUTPNG
bpy.ops.render.render(write_still=True)
print("V15 ADJUST DONE", flush=True)
