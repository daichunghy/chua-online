# -*- coding: utf-8 -*-
"""PATCH P1 vòng 5 — mục [2] lần cuối theo chẩn đoán specular:
 Kênh B của mặt nạ tường nắng bị sàn bởi phản chiếu specular trời xanh
 (albedo B đã cắt còn 0.03-0.15 mà render B chỉ 94->92).
 -> Họ vàng mặt tiền: Specular IOR Level 0.5 -> 0.15 (cắt sheen xanh)
    + tint nhân thêm (1.10, 1.00, 0.55).
Chạy trên layout_v6_p1.blend, lưu cùng file."""
import bpy

F = (1.10, 1.00, 0.55)
GOLD = ('Ngà sáng', 'Vữa màu vàng kem', 'Vàng tường', 'Chỉ trắng ngà', 'Chỉ màu kem',
        'Vàng trang trí', 'Hoa văn vàng', 'Gờ ngà', 'Vàng kem', 'ChuoiVang',
        'LuaVangTamLinh', 'LuaVangTamLinh.001', 'Kim loại vàng cổ')

for nm in GOLD:
    m = bpy.data.materials.get(nm)
    if not m or not m.use_nodes:
        print("MISS", nm)
        continue
    acts = []
    for n in m.node_tree.nodes:
        if n.type == 'MIX_RGB' and n.blend_type == 'MULTIPLY' and not n.inputs[2].links:
            v = n.inputs[2].default_value
            n.inputs[2].default_value = (v[0] * F[0], v[1] * F[1], v[2] * F[2], 1)
            acts.append('tint')
        if n.type == 'BSDF_PRINCIPLED':
            if not n.inputs['Base Color'].links and 'tint' not in acts:
                v = n.inputs['Base Color'].default_value
                n.inputs['Base Color'].default_value = (v[0] * F[0], v[1] * F[1], v[2] * F[2], 1)
                acts.append('base')
            sp = n.inputs.get('Specular IOR Level')
            if sp and not sp.links:
                sp.default_value = 0.15
                acts.append('spec0.15')
    print("R5", nm, acts)

bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
print("SAVED round5")
