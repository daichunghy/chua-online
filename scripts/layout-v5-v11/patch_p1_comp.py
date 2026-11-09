# -*- coding: utf-8 -*-
"""P1 mục 6: AO qua compositor Blender 5 — gán scene.compositing_node_group:
RenderLayer.Image x RenderLayer.'Ambient Occlusion' (ShaderNodeMix MULTIPLY)
-> Group Output. Gán xong thì render thử Cam_Gate 480x270/8spp để kiểm chứng.
Chạy trên layout_v6_p1.blend (đã có patch_p1.py) và lưu lại cùng file."""
import bpy

sc = bpy.context.scene
sc.view_layers[0].use_pass_ambient_occlusion = True

# dọn group cũ nếu chạy lại
old = bpy.data.node_groups.get('P1_CompAO')
if old:
    bpy.data.node_groups.remove(old)
ng = bpy.data.node_groups.new('P1_CompAO', 'CompositorNodeTree')
ng.interface.new_socket(name='Image', in_out='OUTPUT', socket_type='NodeSocketColor')

rl = ng.nodes.new('CompositorNodeRLayers')
try:
    rl.scene = sc
    rl.layer = sc.view_layers[0].name
except Exception as e:
    print("RL set warn:", e)

mix = ng.nodes.new('ShaderNodeMix')
for dt in ('RGBA', 'FLOAT_COLOR', 'COLOR'):
    try:
        mix.data_type = dt
        break
    except Exception:
        continue
try:
    mix.blend_type = 'MULTIPLY'
except Exception as e:
    print("blend set warn:", e)

def find_sock(node, names, sock_type):
    for s in node.inputs:
        if s.name in names and s.type == sock_type and getattr(s, 'enabled', True):
            return s
    return None

outp = ng.nodes.new('NodeGroupOutput')
a_sock = find_sock(mix, ('A',), 'RGBA')
b_sock = find_sock(mix, ('B',), 'RGBA')
f_sock = find_sock(mix, ('Factor',), 'VALUE')
r_sock = None
for s in mix.outputs:
    if s.name == 'Result' and s.type == 'RGBA' and getattr(s, 'enabled', True):
        r_sock = s
print("mix sockets:", a_sock, b_sock, f_sock, r_sock, "blend:", mix.blend_type,
      "data_type:", mix.data_type)
ao_out = None
for s in rl.outputs:
    if s.name == 'Ambient Occlusion':
        ao_out = s
print("AO output:", ao_out, "| Image output:", rl.outputs.get('Image'))

if a_sock and b_sock and ao_out and r_sock:
    ng.links.new(rl.outputs['Image'], a_sock)
    ng.links.new(ao_out, b_sock)
    if f_sock:
        f_sock.default_value = 1.0
    ng.links.new(r_sock, outp.inputs[0])
    sc.compositing_node_group = ng
    print("COMPOSITOR AO ACTIVE")
else:
    print("COMPOSITOR AO FAILED — socket không khớp")

# render thử kiểm chứng
sc.camera = bpy.data.objects['Cam_Gate']
sc.render.filepath = '/tmp/p1_comp_test.png'
sc.render.resolution_x = 480
sc.render.resolution_y = 270
sc.cycles.samples = 8
bpy.ops.render.render(write_still=True)
print("TEST RENDER DONE")
sc.render.resolution_x = 1280
sc.render.resolution_y = 720
sc.cycles.samples = 32
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
print("SAVED with compositor")
