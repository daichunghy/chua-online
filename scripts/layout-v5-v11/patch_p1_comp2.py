# -*- coding: utf-8 -*-
"""P1 mục 6 vòng 2: AO compositor cổng bằng pass MIST.
AO pass = 0 trên trời và Alpha pass = 1 khắp nơi (film không trong suốt)
nên cổng Alpha thất bại. Mist: vật thể gần = 0, xa dần -> 1, trời = 1.
AO' = LIGHTEN(AO, Mist) => trời AO'=1 (không bị nhân đen), vật gần AO'=AO.
Chạy trên layout_v6_p1.blend (đã có round2), lưu cùng file + render thử."""
import bpy

sc = bpy.context.scene
sc.view_layers[0].use_pass_ambient_occlusion = True
sc.view_layers[0].use_pass_mist = True
w = sc.world
w.mist_settings.start = 40.0
w.mist_settings.depth = 400.0
w.mist_settings.falloff = 'LINEAR'

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
    print("RL warn:", e)

def mix_node(blend):
    m = ng.nodes.new('ShaderNodeMix')
    for dt in ('RGBA', 'FLOAT_COLOR', 'COLOR'):
        try:
            m.data_type = dt
            break
        except Exception:
            continue
    m.blend_type = blend
    return m

def sock(node, name, typ):
    for s in node.inputs:
        if s.name == name and s.type == typ and getattr(s, 'enabled', True):
            return s
    return None

def res(node):
    return next(s for s in node.outputs if s.name == 'Result' and s.type == 'RGBA'
                and getattr(s, 'enabled', True))

print("RL outputs:", [s.name for s in rl.outputs])
gate = mix_node('LIGHTEN')
print("gate blend:", gate.blend_type)
ng.links.new(rl.outputs['Ambient Occlusion'], sock(gate, 'A', 'RGBA'))
ng.links.new(rl.outputs['Mist'], sock(gate, 'B', 'RGBA'))
f = sock(gate, 'Factor', 'VALUE')
if f:
    f.default_value = 1.0
fin = mix_node('MULTIPLY')
ng.links.new(rl.outputs['Image'], sock(fin, 'A', 'RGBA'))
ng.links.new(res(gate), sock(fin, 'B', 'RGBA'))
f2 = sock(fin, 'Factor', 'VALUE')
if f2:
    f2.default_value = 1.0
outp = ng.nodes.new('NodeGroupOutput')
ng.links.new(res(fin), outp.inputs[0])
sc.compositing_node_group = ng
print("COMPOSITOR AO mist-gated ACTIVE")

bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
print("SAVED comp2")

sc.camera = bpy.data.objects['Cam_Gate']
sc.render.filepath = '/tmp/p1_comp2_test.png'
sc.render.resolution_x = 480
sc.render.resolution_y = 270
sc.cycles.samples = 8
bpy.ops.render.render(write_still=True)
sc.render.resolution_x = 1280
sc.render.resolution_y = 720
sc.cycles.samples = 32
print("COMP2 TEST DONE")
