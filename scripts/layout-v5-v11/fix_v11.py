"""V11 patch: (1) viết lại UV theo hình chiếu thế giới cho các hộp mang texture
ảnh (lattice + 3 bảng chữ) — mỗi mặt phủ trọn 0..1, mặt tiền không gương;
(2) ẩn FrontText gốc trên bệ tượng (đã có bản sao trên khối bệ mới)."""
import bpy
from mathutils import Vector

DST = "/home/hatch/workspace/chua-online-work/layout_v13_v11.blend"

def fix_uv(obj):
    me = obj.data
    if not me.uv_layers:
        me.uv_layers.new(name='UVMap')
    uv = me.uv_layers.active.data
    mw = obj.matrix_world
    for p in me.polygons:
        n = p.normal
        ax = max(range(3), key=lambda i: abs(n[i]))
        # cặp trục chiếu theo mặt trội: +-y -> (x,z); +-x -> (y,z); +-z -> (x,y)
        axes = {0: (1, 2), 1: (0, 2), 2: (0, 1)}[ax]
        pts = []
        for li in p.loop_indices:
            v = mw @ me.vertices[me.loops[li].vertex_index].co
            pts.append((li, v))
        for k, ai in enumerate(axes):
            vals = [v[ai] for _, v in pts]
            lo, hi = min(vals), max(vals)
            span = (hi - lo) or 1.0
            for li, v in pts:
                if k == 0:
                    uv[li].uv.x = (v[ai] - lo) / span
                else:
                    uv[li].uv.y = (v[ai] - lo) / span

targets = [o for o in bpy.data.objects
           if o.type == 'MESH' and (o.name == 'V11_Tier_Lattice'
                                    or o.name.startswith('V11_Ped_Panel')
                                    or o.name.startswith('V11_Pyl_Panel'))]
for o in targets:
    fix_uv(o)
    print("UV FIXED:", o.name)

ft = bpy.data.objects.get('FrontText')
assert ft is not None
ft.hide_render = True
ft.hide_viewport = True
print("FrontText hidden (render)")

bpy.ops.wm.save_as_mainfile(filepath=DST)
print("SAVED", DST)
