#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tạo mô hình 3D cho toàn bộ các bộ vật phẩm Chùa Online (Chùa Vĩnh Tràng)
Tương thích hoàn hảo với Coohom (OBJ + MTL + ZIP) và Three.js WebGL (meters).
Đồng bộ thẩm mỹ phong cách Cartoon 3D và tỷ lệ nhân vật (nam, nữ, trẻ em).
"""

import os
import math
import zipfile
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_MODELS_DIR = os.path.join(BASE_DIR, "Thiết kế giao diện", "Vật phẩm 3D", "models")
OUTPUT_ZIP_DIR = os.path.join(BASE_DIR, "Thiết kế giao diện", "Vật phẩm 3D", "coohom_packages")
os.makedirs(OUTPUT_MODELS_DIR, exist_ok=True)
os.makedirs(OUTPUT_ZIP_DIR, exist_ok=True)

class OBJMeshBuilder:
    def __init__(self, name):
        self.name = name
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.materials = {} # mat_name -> list of faces
        self.current_material = "default"

    def set_material(self, mat_name, kd=(0.8, 0.8, 0.8), roughness=0.8, metalness=0.1):
        self.current_material = mat_name
        if mat_name not in self.materials:
            self.materials[mat_name] = {
                "kd": kd,
                "roughness": roughness,
                "metalness": metalness,
                "faces": []
            }

    def add_vertex(self, x, y, z):
        self.vertices.append((x, y, z))
        return len(self.vertices)

    def add_normal(self, nx, ny, nz):
        l = math.sqrt(nx*nx + ny*ny + nz*nz) or 1.0
        self.normals.append((nx/l, ny/l, nz/l))
        return len(self.normals)

    def add_face(self, v_indices, n_indices=None):
        if self.current_material not in self.materials:
            self.set_material(self.current_material)
        self.materials[self.current_material]["faces"].append((v_indices, n_indices))

    def add_cylinder(self, r_bottom, r_top, height, segments=16, y_offset=0, x_offset=0, z_offset=0):
        v_start = len(self.vertices)
        # Vertices for top and bottom rings
        for i in range(segments):
            theta = 2 * math.pi * i / segments
            c, s = math.cos(theta), math.sin(theta)
            # bottom
            self.add_vertex(x_offset + r_bottom * c, y_offset, z_offset + r_bottom * s)
            # top
            self.add_vertex(x_offset + r_top * c, y_offset + height, z_offset + r_top * s)

        # Center top and bottom
        c_bot = self.add_vertex(x_offset, y_offset, z_offset)
        c_top = self.add_vertex(x_offset, y_offset + height, z_offset)

        n_up = self.add_normal(0, 1, 0)
        n_down = self.add_normal(0, -1, 0)

        # Side faces
        for i in range(segments):
            next_i = (i + 1) % segments
            b1 = v_start + 1 + i * 2
            t1 = v_start + 2 + i * 2
            b2 = v_start + 1 + next_i * 2
            t2 = v_start + 2 + next_i * 2

            theta = 2 * math.pi * (i + 0.5) / segments
            ns = self.add_normal(math.cos(theta), 0, math.sin(theta))
            self.add_face([b1, b2, t2], [ns, ns, ns])
            self.add_face([b1, t2, t1], [ns, ns, ns])

            # bottom cap
            if r_bottom > 0.0001:
                self.add_face([c_bot, b2, b1], [n_down, n_down, n_down])
            # top cap
            if r_top > 0.0001:
                self.add_face([c_top, t1, t2], [n_up, n_up, n_up])

    def add_sphere(self, radius, segments=12, rings=8, x_offset=0, y_offset=0, z_offset=0):
        v_start = len(self.vertices)
        for i in range(rings + 1):
            phi = math.pi * i / rings
            y = radius * math.cos(phi)
            r_ring = radius * math.sin(phi)
            for j in range(segments):
                theta = 2 * math.pi * j / segments
                x = r_ring * math.cos(theta)
                z = r_ring * math.sin(theta)
                self.add_vertex(x_offset + x, y_offset + y, z_offset + z)
                self.add_normal(x / radius if radius else 0, y / radius if radius else 1, z / radius if radius else 0)

        for i in range(rings):
            for j in range(segments):
                next_j = (j + 1) % segments
                i1 = v_start + 1 + i * segments + j
                i2 = v_start + 1 + i * segments + next_j
                i3 = v_start + 1 + (i + 1) * segments + next_j
                i4 = v_start + 1 + (i + 1) * segments + j
                self.add_face([i1, i2, i3], [i1, i2, i3])
                self.add_face([i1, i3, i4], [i1, i3, i4])

    def add_box(self, width, height, depth, x_offset=0, y_offset=0, z_offset=0):
        w2, h2, d2 = width / 2, height / 2, depth / 2
        coords = [
            (-w2, -h2, d2), (w2, -h2, d2), (w2, h2, d2), (-w2, h2, d2), # front
            (w2, -h2, -d2), (-w2, -h2, -d2), (-w2, h2, -d2), (w2, h2, -d2), # back
        ]
        v_base = len(self.vertices)
        for cx, cy, cz in coords:
            self.add_vertex(x_offset + cx, y_offset + h2 + cy, z_offset + cz)

        normals = [
            (0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0)
        ]
        n_idx = [self.add_normal(*n) for n in normals]

        faces = [
            ([1, 2, 3, 4], n_idx[0]), # front
            ([5, 6, 7, 8], n_idx[1]), # back
            ([4, 3, 8, 7], n_idx[2]), # top
            ([6, 5, 2, 1], n_idx[3]), # bottom
            ([2, 5, 8, 3], n_idx[4]), # right
            ([6, 1, 4, 7], n_idx[5]), # left
        ]
        for f, ni in faces:
            v1, v2, v3, v4 = [v_base + idx for idx in f]
            self.add_face([v1, v2, v3], [ni, ni, ni])
            self.add_face([v1, v3, v4], [ni, ni, ni])

    def add_torus(self, r_major, r_minor, seg_major=24, seg_minor=12, x_offset=0, y_offset=0, z_offset=0):
        v_start = len(self.vertices)
        for i in range(seg_major):
            theta = 2 * math.pi * i / seg_major
            ct, st = math.cos(theta), math.sin(theta)
            for j in range(seg_minor):
                phi = 2 * math.pi * j / seg_minor
                cp, sp = math.cos(phi), math.sin(phi)
                r = r_major + r_minor * cp
                x = r * ct
                z = r * st
                y = r_minor * sp
                self.add_vertex(x_offset + x, y_offset + y, z_offset + z)
                nx = cp * ct
                nz = cp * st
                ny = sp
                self.add_normal(nx, ny, nz)

        for i in range(seg_major):
            next_i = (i + 1) % seg_major
            for j in range(seg_minor):
                next_j = (j + 1) % seg_minor
                i1 = v_start + 1 + i * seg_minor + j
                i2 = v_start + 1 + i * seg_minor + next_j
                i3 = v_start + 1 + next_i * seg_minor + next_j
                i4 = v_start + 1 + next_i * seg_minor + j
                self.add_face([i1, i2, i3], [i1, i2, i3])
                self.add_face([i1, i3, i4], [i1, i3, i4])

    def export_obj_mtl(self, out_dir, scale=1.0):
        obj_path = os.path.join(out_dir, f"{self.name}.obj")
        mtl_path = os.path.join(out_dir, f"{self.name}.mtl")

        with open(mtl_path, "w", encoding="utf-8") as f_mtl:
            f_mtl.write(f"# Coohom & WebGL Material Library for {self.name}\n")
            for mat_name, mat_data in self.materials.items():
                f_mtl.write(f"newmtl {mat_name}\n")
                r, g, b = mat_data["kd"]
                f_mtl.write(f"Kd {r:.4f} {g:.4f} {b:.4f}\n")
                f_mtl.write("Ka 0.1 0.1 0.1\n")
                f_mtl.write("Ks 0.15 0.15 0.15\n")
                f_mtl.write(f"Ns {max(2, int((1 - mat_data['roughness']) * 100))}\n")
                f_mtl.write("d 1.0\nillum 2\n\n")

        with open(obj_path, "w", encoding="utf-8") as f_obj:
            f_obj.write(f"# 3D Model: {self.name}\n")
            f_obj.write(f"mtllib {self.name}.mtl\n")
            for x, y, z in self.vertices:
                f_obj.write(f"v {x*scale:.4f} {y*scale:.4f} {z*scale:.4f}\n")
            for nx, ny, nz in self.normals:
                f_obj.write(f"vn {nx:.4f} {ny:.4f} {nz:.4f}\n")
            for mat_name, mat_data in self.materials.items():
                if not mat_data["faces"]:
                    continue
                f_obj.write(f"usemtl {mat_name}\n")
                for v_list, n_list in mat_data["faces"]:
                    if n_list:
                        face_str = " ".join(f"{v}//{n}" for v, n in zip(v_list, n_list))
                    else:
                        face_str = " ".join(f"{v}" for v in v_list)
                    f_obj.write(f"f {face_str}\n")

        return obj_path, mtl_path

# ==================== CÁC HÀM XÂY DỰNG TỪNG VẬT PHẨM ====================

def create_non_la():
    """1. Nón lá thêu sen - Đường kính 42cm, cao 22cm"""
    m = OBJMeshBuilder("non_la_theu_sen")
    # Chóp nón lá dừa vàng rơm
    m.set_material("LaDuaVangRom", kd=(0.91, 0.85, 0.71), roughness=0.85)
    m.add_cylinder(r_bottom=0.21, r_top=0.015, height=0.22, segments=24)
    # Vành nón
    m.set_material("VanhNonTre", kd=(0.78, 0.70, 0.54), roughness=0.9)
    m.add_torus(r_major=0.21, r_minor=0.005, seg_major=24, seg_minor=8)
    # Họa tiết hoa sen thêu hồng phấn
    m.set_material("TheuSenHong", kd=(0.92, 0.52, 0.62), roughness=0.7)
    m.add_box(width=0.08, height=0.08, depth=0.004, x_offset=0, y_offset=0.09, z_offset=0.13)
    # Quai lụa hồng nhạt
    m.set_material("QuaiLuaHong", kd=(0.95, 0.68, 0.74), roughness=0.6)
    m.add_box(width=0.015, height=0.32, depth=0.004, x_offset=0.17, y_offset=-0.16, z_offset=0)
    m.add_box(width=0.015, height=0.32, depth=0.004, x_offset=-0.17, y_offset=-0.16, z_offset=0)
    return m

def create_khan_ran():
    """2. Khăn rằn Nam Bộ - Vắt vai/quấn cổ"""
    m = OBJMeshBuilder("khan_ran_nam_bo")
    m.set_material("CaroDenTrang", kd=(0.25, 0.25, 0.25), roughness=0.9)
    # Vòng khăn quấn quanh cổ
    m.add_torus(r_major=0.14, r_minor=0.035, seg_major=20, seg_minor=10, y_offset=0.035)
    # 2 vạt khăn buông trước ngực
    m.set_material("TrangNga", kd=(0.92, 0.90, 0.86), roughness=0.9)
    m.add_box(width=0.07, height=0.36, depth=0.02, x_offset=-0.06, y_offset=-0.18, z_offset=0.10)
    m.add_box(width=0.07, height=0.42, depth=0.02, x_offset=0.06, y_offset=-0.21, z_offset=0.09)
    # Tua rua viền khăn
    m.set_material("TuaRuaTrang", kd=(0.95, 0.94, 0.92), roughness=0.95)
    m.add_box(width=0.075, height=0.03, depth=0.01, x_offset=-0.06, y_offset=-0.38, z_offset=0.10)
    m.add_box(width=0.075, height=0.03, depth=0.01, x_offset=0.06, y_offset=-0.44, z_offset=0.09)
    return m

def create_trang_hat_bo_de():
    """3. Tràng hạt Bồ Đề 108 hạt - Đường kính chuỗi 28cm"""
    m = OBJMeshBuilder("trang_hat_bo_de")
    m.set_material("HatBoDeNauGụ", kd=(0.38, 0.24, 0.16), roughness=0.45)
    # Vòng tràng hạt xếp theo đường elip
    bead_count = 54 # Mô phỏng gập đôi 108 hạt
    r_a, r_b = 0.14, 0.20
    for i in range(bead_count):
        theta = 2 * math.pi * i / bead_count
        bx = r_a * math.cos(theta)
        bz = r_b * math.sin(theta)
        m.add_sphere(radius=0.008, segments=8, rings=6, x_offset=bx, y_offset=0, z_offset=bz)

    # Hạt mẹ (Guru bead) hồ lô
    m.set_material("HatMeHoLo", kd=(0.48, 0.28, 0.18), roughness=0.3)
    m.add_sphere(radius=0.015, segments=10, rings=8, x_offset=0, y_offset=0, z_offset=r_b)
    m.add_sphere(radius=0.010, segments=8, rings=6, x_offset=0, y_offset=0.018, z_offset=r_b)

    # Tua rua đỏ may mắn
    m.set_material("TuaRuaChiDo", kd=(0.82, 0.16, 0.14), roughness=0.8)
    m.add_cylinder(r_bottom=0.012, r_top=0.004, height=0.08, segments=10, y_offset=-0.08, z_offset=r_b)
    return m

def create_mo_go():
    """4. Mõ gỗ tụng kinh & dùi mõ - Rộng 20cm, cao 16cm"""
    m = OBJMeshBuilder("mo_go_tung_kinh")
    # Thân mõ gỗ chạm hình cá hóa rồng
    m.set_material("GoCanhGian", kd=(0.52, 0.27, 0.17), roughness=0.35)
    m.add_sphere(radius=0.10, segments=16, rings=12, y_offset=0.10)
    # Miệng mõ xẻ rãnh
    m.set_material("KheMiengMo", kd=(0.18, 0.10, 0.06), roughness=0.9)
    m.add_box(width=0.16, height=0.025, depth=0.12, y_offset=0.09, z_offset=0.04)
    # Gối đệm vuông thêu hoa dưới đế mõ
    m.set_material("GoiDemGamVang", kd=(0.85, 0.65, 0.20), roughness=0.7)
    m.add_box(width=0.24, height=0.04, depth=0.24, y_offset=0)
    # Dùi mõ đặt cạnh
    m.set_material("CanGoDui", kd=(0.60, 0.40, 0.25), roughness=0.5)
    m.add_cylinder(r_bottom=0.006, r_top=0.006, height=0.22, segments=8, y_offset=0.02, x_offset=0.15, z_offset=0.05)
    m.set_material("DauBocVaiNi", kd=(0.70, 0.15, 0.15), roughness=0.9)
    m.add_sphere(radius=0.022, segments=10, rings=8, x_offset=0.15, y_offset=0.02, z_offset=0.17)
    return m

def create_bat_nhang():
    """5. Bát nhang & Ba nén hương trầm có làn khói"""
    m = OBJMeshBuilder("bat_nhang_tram")
    # Bát nhang đồng cổ
    m.set_material("DongCoHoaVan", kd=(0.72, 0.55, 0.28), roughness=0.3, metalness=0.7)
    m.add_cylinder(r_bottom=0.07, r_top=0.09, height=0.11, segments=20)
    # Vành miệng bát nhang
    m.add_torus(r_major=0.09, r_minor=0.008, seg_major=20, seg_minor=8, y_offset=0.11)
    # Lớp tro nhang xám trắng
    m.set_material("TroNhangTrangXam", kd=(0.82, 0.80, 0.77), roughness=0.95)
    m.add_cylinder(r_bottom=0.082, r_top=0.082, height=0.015, segments=16, y_offset=0.095)
    # Ba nén hương trầm thẳng đứng
    m.set_material("ChanHuongDo", kd=(0.80, 0.18, 0.18), roughness=0.8)
    stick_pos = [(-0.025, 0), (0, 0.02), (0.025, 0)]
    for sx, sz in stick_pos:
        # Tăm nhang
        m.add_cylinder(r_bottom=0.002, r_top=0.002, height=0.22, segments=6, y_offset=0.10, x_offset=sx, z_offset=sz)
        # Đốm than đỏ rực cháy
        m.set_material("DiemThanRuc", kd=(1.0, 0.35, 0.10), roughness=0.2)
        m.add_sphere(radius=0.004, segments=6, rings=4, x_offset=sx, y_offset=0.32, z_offset=sz)
    return m

def create_hoa_sen():
    """6. Búp sen hồng & Hoa sen dâng Phật"""
    m = OBJMeshBuilder("hoa_sen_tuoi")
    # Cành sen xanh
    m.set_material("CanhSenXanh", kd=(0.28, 0.52, 0.32), roughness=0.7)
    m.add_cylinder(r_bottom=0.006, r_top=0.005, height=0.30, segments=8)
    # Gương sen nhụy vàng
    m.set_material("GuongSenVang", kd=(0.95, 0.80, 0.22), roughness=0.6)
    m.add_cylinder(r_bottom=0.02, r_top=0.025, height=0.025, segments=12, y_offset=0.30)
    # Các lớp cánh sen hồng hé nở
    m.set_material("CanhSenHong", kd=(0.94, 0.50, 0.65), roughness=0.5)
    petal_layers = [(8, 0.045, 0.30), (6, 0.035, 0.315), (4, 0.022, 0.33)]
    for count, radius, py in petal_layers:
        for i in range(count):
            theta = 2 * math.pi * i / count
            px = radius * math.cos(theta)
            pz = radius * math.sin(theta)
            m.add_sphere(radius=0.016, segments=8, rings=6, x_offset=px, y_offset=py, z_offset=pz)
    # Lá sen tròn nâng đỡ
    m.set_material("LaSenXanhNgoc", kd=(0.22, 0.48, 0.28), roughness=0.8)
    m.add_cylinder(r_bottom=0.14, r_top=0.13, height=0.006, segments=18, y_offset=0.05, x_offset=0.08)
    return m

def create_nen_hoa_sen():
    """7. Nến hoa sen tỏa sáng - Rộng 14cm, cao 10cm"""
    m = OBJMeshBuilder("nen_hoa_sen")
    # Đài sen 8 cánh sáp hồng
    m.set_material("DaiSenSapHong", kd=(0.95, 0.60, 0.70), roughness=0.4)
    m.add_cylinder(r_bottom=0.05, r_top=0.065, height=0.035, segments=16)
    for i in range(8):
        theta = 2 * math.pi * i / 8
        m.add_box(width=0.045, height=0.02, depth=0.025, x_offset=0.065*math.cos(theta), y_offset=0.02, z_offset=0.065*math.sin(theta))
    # Cốc sáp nến trắng trong
    m.set_material("SapNenTrangDuc", kd=(0.95, 0.94, 0.90), roughness=0.3)
    m.add_cylinder(r_bottom=0.035, r_top=0.035, height=0.04, segments=14, y_offset=0.035)
    # Ngọn lửa nến vàng cam ấm
    m.set_material("NgonLuaVangCam", kd=(1.0, 0.65, 0.15), roughness=0.1)
    m.add_sphere(radius=0.012, segments=8, rings=8, y_offset=0.085)
    return m

def create_den_hoa_dang():
    """8. Đèn hoa đăng thả nước tâm linh"""
    m = OBJMeshBuilder("den_hoa_dang")
    # Bè đế vuông màu xanh lá sen
    m.set_material("BeLaSenXanh", kd=(0.25, 0.50, 0.30), roughness=0.85)
    m.add_box(width=0.20, height=0.015, depth=0.20, y_offset=0)
    # Cánh giấy xếp hoa sen 3 lớp
    m.set_material("CanhGiayHongSen", kd=(0.96, 0.45, 0.60), roughness=0.7)
    for i in range(12):
        theta = 2 * math.pi * i / 12
        m.add_box(width=0.04, height=0.05, depth=0.01, x_offset=0.07*math.cos(theta), y_offset=0.025, z_offset=0.07*math.sin(theta))
    # Nến tròn giữa tâm
    m.set_material("NenTrangTam", kd=(0.98, 0.96, 0.92), roughness=0.4)
    m.add_cylinder(r_bottom=0.025, r_top=0.025, height=0.035, segments=12, y_offset=0.015)
    m.set_material("NgonLuaHoaDang", kd=(1.0, 0.75, 0.20), roughness=0.1)
    m.add_sphere(radius=0.010, segments=8, rings=6, y_offset=0.055)
    return m

def create_mam_ngu_qua():
    """9. Mâm ngũ quả dâng Phật - 5 thứ quả Nam Bộ"""
    m = OBJMeshBuilder("mam_ngu_qua")
    # Đĩa gốm tròn viền vàng
    m.set_material("DiaGomTrangSu", kd=(0.92, 0.90, 0.86), roughness=0.25)
    m.add_cylinder(r_bottom=0.16, r_top=0.18, height=0.03, segments=22)
    m.set_material("VienVangKim", kd=(0.88, 0.72, 0.25), roughness=0.3, metalness=0.8)
    m.add_torus(r_major=0.18, r_minor=0.006, seg_major=22, seg_minor=8, y_offset=0.03)
    # 1. Trái mãng cầu gai xanh
    m.set_material("MangCauXanh", kd=(0.42, 0.58, 0.28), roughness=0.8)
    m.add_sphere(radius=0.045, segments=10, rings=8, x_offset=-0.06, y_offset=0.065, z_offset=-0.05)
    # 2. Quả dừa xanh nhỏ
    m.set_material("DuaXiemXanh", kd=(0.46, 0.62, 0.32), roughness=0.7)
    m.add_sphere(radius=0.055, segments=10, rings=8, x_offset=0.06, y_offset=0.075, z_offset=-0.04)
    # 3. Quả đu đủ vàng cam
    m.set_material("DuDuVangCam", kd=(0.95, 0.60, 0.18), roughness=0.6)
    m.add_cylinder(r_bottom=0.032, r_top=0.022, height=0.10, segments=10, x_offset=0, y_offset=0.04, z_offset=0.06)
    # 4. Quả xoài cát vàng óng
    m.set_material("XoaiCatVang", kd=(0.98, 0.80, 0.20), roughness=0.45)
    m.add_sphere(radius=0.038, segments=10, rings=8, x_offset=0.05, y_offset=0.055, z_offset=0.07)
    # 5. Chùm sung xanh sung túc đỉnh tháp
    m.set_material("ChumSungXanh", kd=(0.35, 0.52, 0.25), roughness=0.7)
    m.add_sphere(radius=0.020, segments=8, rings=6, x_offset=0, y_offset=0.12, z_offset=0)
    m.add_sphere(radius=0.018, segments=8, rings=6, x_offset=0.02, y_offset=0.11, z_offset=0.015)
    m.add_sphere(radius=0.018, segments=8, rings=6, x_offset=-0.02, y_offset=0.11, z_offset=-0.015)
    return m

def create_bo_doan_dai_sen():
    """10. Bồ đoàn đài sen - Đường kính 45cm, cao 12cm"""
    m = OBJMeshBuilder("bo_doan_dai_sen")
    # Lõi đệm tròn vải gấm lam tím
    m.set_material("GamLamTimSang", kd=(0.58, 0.48, 0.52), roughness=0.85)
    m.add_cylinder(r_bottom=0.22, r_top=0.21, height=0.11, segments=24)
    # 8 cánh sen may nổi bao quanh
    m.set_material("CanhSenGhiNau", kd=(0.48, 0.38, 0.34), roughness=0.8)
    for i in range(8):
        theta = 2 * math.pi * i / 8
        cx = 0.215 * math.cos(theta)
        cz = 0.215 * math.sin(theta)
        m.add_box(width=0.10, height=0.08, depth=0.04, x_offset=cx, y_offset=0.02, z_offset=cz)
    # Viền thêu chỉ vàng tâm đệm
    m.set_material("ChiTheuVangKim", kd=(0.85, 0.70, 0.25), roughness=0.5)
    m.add_torus(r_major=0.10, r_minor=0.005, seg_major=20, seg_minor=8, y_offset=0.11)
    return m

def create_bo_doan_tron():
    """11. Bồ đoàn tròn mộc vải bố - D40cm x H10cm"""
    m = OBJMeshBuilder("bo_doan_tron")
    m.set_material("VaiBoNauSong", kd=(0.42, 0.30, 0.24), roughness=0.9)
    m.add_cylinder(r_bottom=0.20, r_top=0.19, height=0.10, segments=24)
    # Gân chỉ viền quanh
    m.set_material("GanChiBaoViền", kd=(0.32, 0.22, 0.18), roughness=0.95)
    m.add_torus(r_major=0.195, r_minor=0.006, seg_major=24, seg_minor=8, y_offset=0.05)
    # Quai xách tiện dụng
    m.add_box(width=0.08, height=0.02, depth=0.03, x_offset=0.20, y_offset=0.05, z_offset=0)
    return m

def create_chieu_coi():
    """12. Chiếu cói thiền tọa - 80cm x 160cm x 1cm"""
    m = OBJMeshBuilder("chieu_coi_thien")
    m.set_material("CoiTuNhienVangRom", kd=(0.86, 0.80, 0.68), roughness=0.92)
    m.add_box(width=0.80, height=0.012, depth=1.60, y_offset=0)
    # Viền vải nâu gụ bao 4 cạnh
    m.set_material("VienVaiNauGu", kd=(0.38, 0.26, 0.20), roughness=0.85)
    m.add_box(width=0.81, height=0.014, depth=0.05, y_offset=0, z_offset=0.78)
    m.add_box(width=0.81, height=0.014, depth=0.05, y_offset=0, z_offset=-0.78)
    m.add_box(width=0.05, height=0.014, depth=1.60, y_offset=0, x_offset=0.38)
    m.add_box(width=0.05, height=0.014, depth=1.60, y_offset=0, x_offset=-0.38)
    return m

def create_dia_banh_bo():
    """13. Đĩa bánh bò thốt nốt Nam Bộ"""
    m = OBJMeshBuilder("dia_banh_bo")
    m.set_material("DiaSuTrangMen", kd=(0.95, 0.94, 0.90), roughness=0.2)
    m.add_cylinder(r_bottom=0.12, r_top=0.14, height=0.02, segments=20)
    # 4 chiếc bánh bò vàng ươm nở rễ tre
    m.set_material("BanhBoThotNotVang", kd=(0.92, 0.70, 0.25), roughness=0.7)
    positions = [(-0.045, -0.045), (0.045, -0.045), (-0.045, 0.045), (0.045, 0.045), (0, 0)]
    for bx, bz in positions:
        m.add_sphere(radius=0.032, segments=10, rings=8, x_offset=bx, y_offset=0.04, z_offset=bz)
    return m

def create_dia_banh_da_lon():
    """14. Đĩa bánh da lợn ngũ sắc"""
    m = OBJMeshBuilder("dia_banh_da_lon")
    m.set_material("DiaGomMocTrang", kd=(0.93, 0.92, 0.88), roughness=0.3)
    m.add_cylinder(r_bottom=0.12, r_top=0.14, height=0.02, segments=20)
    # Các lớp bánh da lợn cắt hình thoi
    m.set_material("LopLaDuaXanh", kd=(0.32, 0.60, 0.36), roughness=0.4)
    m.add_box(width=0.08, height=0.012, depth=0.14, y_offset=0.02, x_offset=-0.03)
    m.set_material("LopDauXanhVang", kd=(0.90, 0.80, 0.40), roughness=0.45)
    m.add_box(width=0.08, height=0.012, depth=0.14, y_offset=0.032, x_offset=-0.03)
    m.set_material("LopLaDuaXanh2", kd=(0.32, 0.60, 0.36), roughness=0.4)
    m.add_box(width=0.08, height=0.012, depth=0.14, y_offset=0.044, x_offset=-0.03)
    return m

def create_trai_dua_xiem():
    """15. Trái dừa xiêm tươi cắm ống hút tre"""
    m = OBJMeshBuilder("trai_dua_xiem")
    # Trái dừa gọt nhọn đầu vỏ xanh non
    m.set_material("VoDuaXanhNon", kd=(0.50, 0.68, 0.34), roughness=0.65)
    m.add_sphere(radius=0.09, segments=16, rings=12, y_offset=0.09)
    # Đỉnh gọt phẳng
    m.set_material("ThitDuaTrangNga", kd=(0.95, 0.94, 0.88), roughness=0.4)
    m.add_cylinder(r_bottom=0.04, r_top=0.035, height=0.01, segments=12, y_offset=0.175)
    # Ống hút tre mộc
    m.set_material("OngHutTre", kd=(0.78, 0.68, 0.48), roughness=0.7)
    m.add_cylinder(r_bottom=0.005, r_top=0.005, height=0.14, segments=8, y_offset=0.16, x_offset=0.01, z_offset=0.01)
    return m

def create_tui_vai():
    """16. Túi vải đi chùa (Tote canvas mộc)"""
    m = OBJMeshBuilder("tui_vai_di_chua")
    m.set_material("VaiCanvasMoc", kd=(0.88, 0.84, 0.76), roughness=0.9)
    # Thân túi chữ nhật dẹp
    m.add_box(width=0.32, height=0.36, depth=0.08, y_offset=0)
    # Quai đeo đôi
    m.set_material("QuaiTuiNauLam", kd=(0.55, 0.45, 0.40), roughness=0.85)
    m.add_box(width=0.025, height=0.25, depth=0.008, x_offset=-0.08, y_offset=0.36*0.5 + 0.125, z_offset=0.04)
    m.add_box(width=0.025, height=0.25, depth=0.008, x_offset=0.08, y_offset=0.36*0.5 + 0.125, z_offset=0.04)
    # Họa tiết hoa sen in trên túi
    m.set_material("SenInNauTram", kd=(0.42, 0.28, 0.22), roughness=0.8)
    m.add_box(width=0.12, height=0.12, depth=0.002, y_offset=0.02, z_offset=0.042)
    return m

def create_quat_nan():
    """17. Quạt nan lá dừa che nắng sân chùa"""
    m = OBJMeshBuilder("quat_nan_la_dua")
    m.set_material("NanLaDuaVangNhat", kd=(0.85, 0.78, 0.60), roughness=0.88)
    # Phiến quạt dẹt hình tim
    m.add_cylinder(r_bottom=0.14, r_top=0.14, height=0.006, segments=18, y_offset=0.15)
    # Cán tre kẹp
    m.set_material("CanTreGia", kd=(0.65, 0.50, 0.30), roughness=0.7)
    m.add_cylinder(r_bottom=0.008, r_top=0.008, height=0.30, segments=8, y_offset=0)
    return m

def create_gio_may_tre():
    """18. Giỏ mây tre đan đựng lễ vật"""
    m = OBJMeshBuilder("gio_may_tre")
    m.set_material("MayTreDanNauVang", kd=(0.76, 0.60, 0.38), roughness=0.9)
    # Thùng giỏ oval
    m.add_cylinder(r_bottom=0.14, r_top=0.17, height=0.18, segments=18)
    # Quai xách vòng cung
    m.add_torus(r_major=0.16, r_minor=0.012, seg_major=20, seg_minor=8, y_offset=0.22)
    return m

def create_chum_sanh_sen():
    """19. Chum sành hoa sen thả nước sân chùa"""
    m = OBJMeshBuilder("chum_sanh_hoa_sen")
    m.set_material("GomSanhDatNung", kd=(0.58, 0.32, 0.22), roughness=0.75)
    # Thân chum bầu tròn
    m.add_sphere(radius=0.24, segments=20, rings=14, y_offset=0.24)
    # Miệng chum loe
    m.add_torus(r_major=0.18, r_minor=0.025, seg_major=20, seg_minor=8, y_offset=0.46)
    # Mặt nước trong vắt
    m.set_material("MatNuocXanhLam", kd=(0.28, 0.55, 0.65), roughness=0.1)
    m.add_cylinder(r_bottom=0.17, r_top=0.17, height=0.01, segments=18, y_offset=0.42)
    # Hoa sen thả nổi
    m.set_material("HoaSenNoiHong", kd=(0.95, 0.52, 0.65), roughness=0.4)
    m.add_sphere(radius=0.045, segments=10, rings=8, x_offset=0.04, y_offset=0.43, z_offset=0.03)
    return m

def create_den_long_luc_giac():
    """20. Đèn lồng lục giác treo chùa"""
    m = OBJMeshBuilder("den_long_luc_giac")
    # Khung gỗ 6 cạnh
    m.set_material("KhungGoNauDo", kd=(0.50, 0.22, 0.16), roughness=0.6)
    m.add_cylinder(r_bottom=0.18, r_top=0.22, height=0.28, segments=6)
    # Mái chóp đèn lồng
    m.add_cylinder(r_bottom=0.24, r_top=0.02, height=0.09, segments=6, y_offset=0.28)
    # Lụa vàng dán phát quang
    m.set_material("LuaVangTamLinh", kd=(0.98, 0.72, 0.20), roughness=0.4)
    m.add_cylinder(r_bottom=0.16, r_top=0.20, height=0.26, segments=6, y_offset=0.01)
    # Chùm tua rua đỏ treo đáy
    m.set_material("TuaRuaDoChua", kd=(0.85, 0.15, 0.15), roughness=0.85)
    m.add_cylinder(r_bottom=0.02, r_top=0.005, height=0.14, segments=8, y_offset=-0.14)
    return m

# ==================== MAIN RUNNER & PACKAGER ====================

ITEMS = [
    ("non_la_theu_sen", "Bộ Phụ Kiện Đội & Choàng", "Nón Lá Thêu Sen", 420, 420, 220, create_non_la),
    ("khan_ran_nam_bo", "Bộ Phụ Kiện Đội & Choàng", "Khăn Rằn Nam Bộ", 280, 240, 440, create_khan_ran),
    ("trang_hat_bo_de", "Bộ Pháp Khí & Chuỗi Tràng", "Tràng Hạt Bồ Đề 108 Hạt", 280, 400, 40, create_trang_hat_bo_de),
    ("mo_go_tung_kinh", "Bộ Pháp Khí & Chuỗi Tràng", "Bộ Mõ Gỗ & Dùi Tụng Kinh", 240, 240, 200, create_mo_go),
    ("bat_nhang_tram", "Bộ Đồ Lễ & Cúng Dường", "Bát Nhang & Ba Nén Hương Trầm", 180, 180, 320, create_bat_nhang),
    ("hoa_sen_tuoi", "Bộ Đồ Lễ & Cúng Dường", "Búp Sen Hồng & Lá Sen Tươi", 280, 280, 340, create_hoa_sen),
    ("nen_hoa_sen", "Bộ Đồ Lễ & Cúng Dường", "Nến Hoa Sen Phát Sáng", 140, 140, 100, create_nen_hoa_sen),
    ("den_hoa_dang", "Bộ Đồ Lễ & Cúng Dường", "Đèn Hoa Đăng Thả Nước", 200, 200, 80, create_den_hoa_dang),
    ("mam_ngu_qua", "Bộ Đồ Lễ & Cúng Dường", "Mâm Ngũ Quả Dâng Phật", 360, 360, 160, create_mam_ngu_qua),
    ("bo_doan_dai_sen", "Bộ Tọa Cụ & Bồ Đoàn", "Bồ Đoàn Đài Sen 8 Cánh", 450, 450, 120, create_bo_doan_dai_sen),
    ("bo_doan_tron", "Bộ Tọa Cụ & Bồ Đoàn", "Bồ Đoàn Tròn Vải Bố Mộc", 400, 400, 100, create_bo_doan_tron),
    ("chieu_coi_thien", "Bộ Tọa Cụ & Bồ Đoàn", "Chiếu Cói Thiền Tọa Nam Bộ", 800, 1600, 14, create_chieu_coi),
    ("dia_banh_bo", "Bộ Ẩm Thực Chay & Thức Quà", "Đĩa Bánh Bò Thốt Nốt", 280, 280, 70, create_dia_banh_bo),
    ("dia_banh_da_lon", "Bộ Ẩm Thực Chay & Thức Quà", "Đĩa Bánh Da Lợn Ngũ Sắc", 280, 280, 60, create_dia_banh_da_lon),
    ("trai_dua_xiem", "Bộ Ẩm Thực Chay & Thức Quà", "Trái Dừa Xiêm Ống Hút Tre", 180, 180, 260, create_trai_dua_xiem),
    ("tui_vai_di_chua", "Bộ Cầm Tay & Hành Lý", "Túi Vải Đi Chùa Chữ Thư Pháp", 320, 80, 480, create_tui_vai),
    ("quat_nan_la_dua", "Bộ Cầm Tay & Hành Lý", "Quạt Nan Lá Dừa Che Nắng", 280, 20, 380, create_quat_nan),
    ("gio_may_tre", "Bộ Cầm Tay & Hành Lý", "Giỏ Mây Tre Đan Nam Bộ", 340, 280, 360, create_gio_may_tre),
    ("chum_sanh_hoa_sen", "Bộ Cảnh Quan & Pháp Bảo", "Chum Sành Hoa Sen Thả Nước", 480, 480, 500, create_chum_sanh_sen),
    ("den_long_luc_giac", "Bộ Cảnh Quan & Pháp Bảo", "Đèn Lồng Lục Giác Treo Chùa", 440, 440, 520, create_den_long_luc_giac),
]

def main():
    print("=== BẮT ĐẦU TẠO 20 MÔ HÌNH 3D VẬT PHẨM CHÙA ONLINE ===")
    catalog = []

    for item_id, group, name_vi, w_mm, d_mm, h_mm, builder_func in ITEMS:
        builder = builder_func()

        # 1. Xuất file WebGL / Three.js (Hệ mét: 1 unit = 1m)
        obj_m, mtl_m = builder.export_obj_mtl(OUTPUT_MODELS_DIR, scale=1.0)

        # 2. Xuất gói Coohom chuẩn (Hệ mm: 1 unit = 1000mm)
        coohom_temp_dir = os.path.join(OUTPUT_MODELS_DIR, "coohom_temp")
        os.makedirs(coohom_temp_dir, exist_ok=True)
        obj_mm, mtl_mm = builder.export_obj_mtl(coohom_temp_dir, scale=1000.0)

        # Đóng gói zip chuẩn cho Coohom upload
        zip_filename = f"coohom_{item_id}.zip"
        zip_path = os.path.join(OUTPUT_ZIP_DIR, zip_filename)
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.write(obj_mm, arcname=f"{item_id}.obj")
            zf.write(mtl_mm, arcname=f"{item_id}.mtl")
            # metadata cho Coohom
            meta = {
                "id": item_id,
                "name": name_vi,
                "category": group,
                "dimensions_mm": {"width": w_mm, "depth": d_mm, "height": h_mm},
                "format": "OBJ+MTL",
                "units": "mm",
                "pivot": "bottom_center"
            }
            zf.writestr("metadata.json", json.dumps(meta, ensure_ascii=False, indent=2))

        # Dọn dẹp temp
        os.remove(obj_mm)
        os.remove(mtl_mm)

        catalog.append({
            "id": item_id,
            "group": group,
            "name": name_vi,
            "dimensions_mm": {"w": w_mm, "d": d_mm, "h": h_mm},
            "obj_file": f"./models/{item_id}.obj",
            "mtl_file": f"./models/{item_id}.mtl",
            "coohom_zip": f"./coohom_packages/{zip_filename}",
            "vertex_count": len(builder.vertices),
            "face_count": sum(len(m["faces"]) for m in builder.materials.values()),
            "materials": list(builder.materials.keys())
        })
        print(f"✓ Đã tạo: {name_vi} ({item_id}) -> {len(builder.vertices)} đỉnh, {sum(len(m['faces']) for m in builder.materials.values())} đa giác")

    # Xóa thư mục temp
    if os.path.exists(coohom_temp_dir):
        os.rmdir(coohom_temp_dir)

    # Xuất file catalog JSON
    catalog_path = os.path.join(BASE_DIR, "Thiết kế giao diện", "Vật phẩm 3D", "danh_muc_vat_pham_3d.json")
    with open(catalog_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)

    print(f"\n=> Hoàn tất 20 mô hình 3D! Đã lưu danh mục vào: {catalog_path}")

if __name__ == "__main__":
    main()
