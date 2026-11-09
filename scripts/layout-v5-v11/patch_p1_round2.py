# -*- coding: utf-8 -*-
"""PATCH P1 vòng 2 — sửa 2 lỗi tìm được ở vòng 1:
 A) Trời: world Generated Z chạy NGƯỢC (horizon ≈0.50, lên cao GIẢM về 0) —
    đặt lại stop gradient theo thang Z đã đo:
      0.50 #DCEFFD (chân trời) / 0.42 #4F97F9 / 0.30 #1E6FD9 / 0.15 #0155C9 (đỉnh)
 B) Compositor AO: pass AO = 0 trên nền trời -> nhân thẳng làm trời đen.
    Cổng hoá bằng Alpha: AO' = 1 - (1-AO)*Alpha (trời Alpha=0 => AO'=1).
 C) Cập nhật lại ảnh frieze.png đã sửa mép trời.
Chạy trên layout_v6_p1.blend, lưu cùng file. Cuối script render thử Cam_Gate
480x270 để tự kiểm chứng (in điểm ảnh trời)."""
import bpy

sc = bpy.context.scene

def hex_lin(h):
    h = h.lstrip('#')
    r, g, b = (int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))
    def f(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return (f(r), f(g), f(b))

# --- A) ramp trời mới
nt = sc.world.node_tree
ramp = next(n for n in nt.nodes if n.bl_idname == 'ShaderNodeValToRGB')
els = ramp.color_ramp.elements
while len(els) > 2:
    els.remove(els[1])
stops = [(0.50, '#DCEFFD'), (0.42, '#4F97F9'), (0.30, '#1E6FD9'), (0.15, '#0155C9')]
els[0].position = stops[0][0]
els[0].color = (*hex_lin(stops[0][1]), 1)
els[1].position = stops[-1][0]
els[1].color = (*hex_lin(stops[-1][1]), 1)
for pos, col in stops[1:-1]:
    el = els.new(pos)
    el.color = (*hex_lin(col), 1)
print("SKY RAMP V2 set:", [(round(e.position, 2)) for e in ramp.color_ramp.elements])

# --- B) compositor AO cổng Alpha
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

def invert_node():
    n = ng.nodes.new('CompositorNodeInvert')
    for s in n.inputs:
        if s.name == 'Invert Color':
            s.default_value = True
        if s.name == 'Factor':
            s.default_value = 1.0
    return n

inv1 = invert_node()
ng.links.new(rl.outputs['Ambient Occlusion'], inv1.inputs['Color'])
mulA = mix_node('MULTIPLY')
ng.links.new(inv1.outputs['Color'], sock(mulA, 'A', 'RGBA'))
ng.links.new(rl.outputs['Alpha'], sock(mulA, 'B', 'RGBA'))
f = sock(mulA, 'Factor', 'VALUE')
if f:
    f.default_value = 1.0
inv2 = invert_node()
resA = next(s for s in mulA.outputs if s.name == 'Result' and s.type == 'RGBA'
            and getattr(s, 'enabled', True))
ng.links.new(resA, inv2.inputs['Color'])
fin = mix_node('MULTIPLY')
ng.links.new(rl.outputs['Image'], sock(fin, 'A', 'RGBA'))
ng.links.new(inv2.outputs['Color'], sock(fin, 'B', 'RGBA'))
f2 = sock(fin, 'Factor', 'VALUE')
if f2:
    f2.default_value = 1.0
outp = ng.nodes.new('NodeGroupOutput')
resF = next(s for s in fin.outputs if s.name == 'Result' and s.type == 'RGBA'
            and getattr(s, 'enabled', True))
ng.links.new(resF, outp.inputs[0])
sc.compositing_node_group = ng
print("COMPOSITOR AO alpha-gated ACTIVE")

# --- C) frieze cập nhật
im = bpy.data.images.get('frieze.png')
if im:
    im.filepath = '/home/hatch/workspace/chua-online-work/gate_tex/frieze.png'
    im.reload()
    im.pack()
    print("frieze reloaded")

bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
print("SAVED round2")

# render thử kiểm chứng ngay trong phiên
sc.camera = bpy.data.objects['Cam_Gate']
sc.render.filepath = '/tmp/p1_r2_test.png'
sc.render.resolution_x = 480
sc.render.resolution_y = 270
sc.cycles.samples = 8
bpy.ops.render.render(write_still=True)
sc.render.resolution_x = 1280
sc.render.resolution_y = 720
sc.cycles.samples = 32
print("R2 TEST RENDER DONE")
