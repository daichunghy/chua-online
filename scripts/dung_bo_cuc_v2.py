"""
BỐ CỤC V2 — bổ sung các hạng mục còn thiếu so với flycam thật (ref9/ref14)
vào bo-cuc-theo-anh.blend sẵn có của repo:
- Hồ nước chữ nhật phía trước (bản cũ THIẾU)
- Tượng Phật đứng khổng lồ đài sen xanh ở góc trước–trái (bản cũ THIẾU — đính chính theo ref14)
- 2 cổng tam quan khảm sành ở hai đầu mặt tiền (bản cũ THIẾU) — theo ảnh cận ref10:
  tháp cổng cao hẹp, ô giữa có tượng Phật đứng, mái ngói đỏ
- Hàng rào vàng mặt tiền (bản cũ THIẾU)
Tượng Di Lặc + Phật nằm: giữ nguyên bệ của bản cũ (chưa có tượng điêu khắc trung thực —
giữ trạng thái trung thực đó, không bịa tượng thô).
"""
import bpy, math, os
from mathutils import Vector

SRC = "/home/hatch/workspace/chua-online-work/bo-cuc-theo-anh-raw.blend"
OUT = "/home/hatch/workspace/chua-online-work/bo-cuc-v2"
bpy.ops.wm.open_mainfile(filepath=SRC)
s = bpy.context.scene

def mat(n, c, rough=0.8):
    m = bpy.data.materials.new(n); m.use_nodes = True
    m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (*c, 1)
    m.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = rough
    return m
yellow = mat("Vang_Tuong_V2", (0.85, 0.60, 0.10))
ivory = mat("Nga_V2", (0.88, 0.80, 0.60))
red = mat("Ngoi_Do_V2", (0.48, 0.16, 0.08))
dark = mat("O_Cua_V2", (0.10, 0.08, 0.06))
white = mat("Tuong_Trang_V2", (0.93, 0.92, 0.90), 0.55)
water = mat("Nuoc_Ho_V2", (0.16, 0.38, 0.48), 0.15)
stone = mat("Da_Xam_V2", (0.48, 0.47, 0.44))
blue = mat("Sen_Xanh_V2", (0.20, 0.45, 0.62), 0.5)
base_rb = mat("Be_Do_Nau_V2", (0.45, 0.22, 0.16))

def box(n, loc, dim, m):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object
    o.name = n; o.dimensions = dim
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(m); return o
def cyl(n, loc, r, h, m, verts=24):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=h, location=loc)
    o = bpy.context.object; o.name = n; o.data.materials.append(m); return o
def ball(n, loc, scale, m):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=16, location=loc)
    o = bpy.context.object; o.name = n; o.scale = scale
    o.data.materials.append(m); bpy.ops.object.shade_smooth(); return o
def cone(n, loc, r1, r2, h, m):
    bpy.ops.mesh.primitive_cone_add(vertices=32, radius1=r1, radius2=r2, depth=h, location=loc)
    o = bpy.context.object; o.name = n; o.data.materials.append(m)
    bpy.ops.object.shade_smooth(); return o

# ---------- HỒ NƯỚC CHỮ NHẬT (trước–trái, theo ref14) ----------
box("Vien_Ho", (-28, -36, 0.10), (27, 11, 0.35), stone)
box("Mat_Nuoc_Ho", (-28, -36, 0.22), (25.5, 9.5, 0.12), water)

# ---------- TƯỢNG PHẬT ĐỨNG ĐÀI SEN XANH (góc trước–trái) ----------
gx, gy = -40, -33
box("Be_Tuong_Dung", (gx, gy, 0.8), (7.5, 7.5, 1.6), base_rb)
for i, r in enumerate((2.6, 2.2, 1.8)):
    ball(f"Canh_Sen_Xanh_{i}", (gx, gy, 1.75 + i * 0.28), (r, r, 0.30), blue)
cone("Ao_Tuong_Dung", (gx, gy, 2.1 + 2.8), 1.95, 0.60, 5.6, white)          # áo choàng
ball("Vai_Tuong_Dung", (gx, gy, 7.55), (0.85, 0.68, 0.58), white)            # vai
ball("Dau_Tuong_Dung", (gx, gy, 8.35), (0.55, 0.52, 0.65), white)            # đầu
ball("Bui_Toc_Tuong", (gx, gy, 8.98), (0.21, 0.21, 0.19), white)             # búi tóc

# ---------- 2 CỔNG TAM QUAN (theo ref10) ----------
def gate(x, y, name):
    box(f"{name}_Be", (x, y, 1.5), (5.2, 3.4, 3.0), yellow)
    box(f"{name}_Vom", (x, y - 1.55, 1.35), (2.0, 0.5, 2.7), dark)           # ô vòm tối mặt trước
    box(f"{name}_TangTren", (x, y, 4.4), (4.2, 2.8, 2.8), yellow)
    box(f"{name}_O_Tuong", (x, y - 1.30, 4.5), (1.1, 0.4, 1.9), dark)        # ô giữa
    cone(f"{name}_TuongPhat", (x, y - 1.32, 4.15), 0.26, 0.10, 1.1, white)   # tượng Phật đứng trong ô
    ball(f"{name}_DauTuong", (x, y - 1.32, 4.85), (0.13, 0.13, 0.15), white)
    box(f"{name}_Mai", (x, y, 6.05), (4.9, 3.4, 0.35), red)
    box(f"{name}_DinhMai", (x, y, 6.45), (2.6, 1.2, 0.45), red)
gate(-47, -26, "Cong_Trai")
gate(45, -26, "Cong_Phai")

# ---------- HÀNG RÀO VÀNG MẶT TIỀN (y=-26, chừa 2 cổng) ----------
for (x0, x1) in ((-52, -49.8), (-44.2, 42.2), (47.8, 52)):
    wdt = x1 - x0
    if wdt <= 0: continue
    box("Hang_Rao", ((x0 + x1) / 2, -26, 0.55), (wdt, 0.35, 1.1), yellow)
    n = int(wdt // 6)
    for i in range(n + 1):
        box("Tru_Rao", (x0 + i * 6, -26, 0.75), (0.45, 0.5, 1.5), ivory)

# Nới khung hình để thấy đủ 2 cổng + toàn khuôn viên
for o in bpy.data.objects:
    if o.type == 'CAMERA':
        o.data.ortho_scale = 148
# Render bằng Eevee cho nhanh trên máy không GPU, giữ nguyên camera tổng quan của bản cũ
s.render.engine = 'CYCLES'
s.cycles.samples = 32
s.cycles.use_denoising = True
try: s.view_settings.view_transform = 'Standard'
except Exception: pass
w = bpy.data.worlds.new("Troi_V2"); s.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (0.45, 0.60, 0.85, 1)
w.node_tree.nodes["Background"].inputs[1].default_value = 0.6
sun = bpy.data.lights.new("Sun_V2", 'SUN'); sun.energy = 2.2
so = bpy.data.objects.new("Sun_V2", sun); s.collection.objects.link(so)
so.rotation_euler = (math.radians(48), 0, math.radians(-35))
bpy.ops.wm.save_as_mainfile(filepath=OUT + ".blend")
s.render.filepath = OUT + ".png"
bpy.ops.render.render(write_still=True)
print("BO CUC V2 DONE")
