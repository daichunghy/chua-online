"""
RENDER P3 — chay: blender5 -b layout_v8_p3.blend --python render_p3.py -- <a|b> <CamName> <out.png>
(a) = file da luu san (sang trong). (b) = 16h30 am: chinh trong bo nho, KHONG luu.
"""
import bpy, sys, math

argv = sys.argv[sys.argv.index('--') + 1:]
variant, cam_name, out = argv[0], argv[1], argv[2]
sc = bpy.context.scene
W = "/home/hatch/workspace/chua-online-work/"

if variant == 'b':
    sun = bpy.data.objects.get('Sun_Layout')
    sun.data.energy = 2.4
    sun.data.color = (1.0, 0.80, 0.58)
    sun.rotation_euler = (math.radians(58), 0.15, -0.55)
    sc.view_settings.exposure = 0.9
    w = sc.world
    for nd in w.node_tree.nodes:
        if nd.type == 'BACKGROUND':
            nd.inputs[1].default_value = round(nd.inputs[1].default_value * 0.85, 3)
    g = sc.compositing_node_group
    fac = g.nodes.get('P3_FogFac'); fac.inputs[1].default_value = 0.27
    rgb = g.nodes.get('P3_FogRGB'); rgb.outputs[0].default_value = (0.96, 0.83, 0.62, 1.0)
    vig = g.nodes.get('P3_VigImg')
    vig.image = bpy.data.images.load(W + 'textures/p3_vignette_b.png')
    print("VARIANT B applied", flush=True)

cam = bpy.data.objects.get(cam_name)
assert cam is not None, f"missing camera {cam_name}"
sc.camera = cam
sc.render.filepath = W + "layout/" + out
bpy.ops.render.render(write_still=True)
print("RENDERED", out, flush=True)
