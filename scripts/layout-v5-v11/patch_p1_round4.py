# -*- coding: utf-8 -*-
"""PATCH P1 vòng 4 — theo chẩn đoán vật liệu:
 [2] Mặt nạ 'tường nắng' do CẢ HỌ vật liệu vàng mặt tiền tạo thành
     (Vàng trang trí 73 obj, Hoa văn vàng 60, Chỉ trắng ngà 219, Chỉ màu kem,
      ChuoiVang, LuaVangTamLinh, Kim loại vàng cổ, Gờ ngà, Vàng kem + 3 tường).
     Nhân tint/base của cả họ thêm (1.30, 1.12, 0.50) cho sâu về #D9A441.
 [5] Nền: kênh B tint Dat_Co/Đá sân/Nền xám sáng/Cây nền x0.92 (đang +12.2, sát biên).
Chạy trên layout_v6_p1.blend, lưu cùng file."""
import bpy

F = (1.30, 1.12, 0.50)
GOLD = ('Ngà sáng', 'Vữa màu vàng kem', 'Vàng tường', 'Chỉ trắng ngà', 'Chỉ màu kem',
        'Vàng trang trí', 'Hoa văn vàng', 'Gờ ngà', 'Vàng kem', 'ChuoiVang',
        'LuaVangTamLinh', 'LuaVangTamLinh.001', 'Kim loại vàng cổ')

def scale_mat(m, f):
    """Nhân hệ số vào node tint MULTIPLY (inputs[2] chưa link) hoặc Base Color phẳng."""
    done = []
    if not m or not m.use_nodes:
        return done
    for n in m.node_tree.nodes:
        if n.type == 'MIX_RGB' and n.blend_type == 'MULTIPLY' and not n.inputs[2].links:
            v = n.inputs[2].default_value
            n.inputs[2].default_value = (v[0] * f[0], v[1] * f[1], v[2] * f[2], 1)
            done.append('tint')
    if not done:
        for n in m.node_tree.nodes:
            if n.type == 'BSDF_PRINCIPLED' and not n.inputs['Base Color'].links:
                v = n.inputs['Base Color'].default_value
                n.inputs['Base Color'].default_value = (v[0] * f[0], v[1] * f[1], v[2] * f[2], 1)
                done.append('base')
    return done

for nm in GOLD:
    m = bpy.data.materials.get(nm)
    print("GOLD", nm, scale_mat(m, F) if m else "MISS")

FB = (1.0, 1.0, 0.92)
for nm in ('Dat_Co', 'Đá sân', 'Nền xám sáng', 'Cây nền'):
    m = bpy.data.materials.get(nm)
    if m:
        print("GROUND-B", nm, scale_mat(m, FB))

bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
print("SAVED round4")
