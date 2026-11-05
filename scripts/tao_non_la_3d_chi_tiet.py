#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script tạo mô hình 3D chi tiết cao cho Vật phẩm #1: NÓN LÁ THÊU HOA SEN.
Đảm bảo độ tinh xảo, đường cong sườn nón chuẩn xác, 16 vành nón tre chìm,
họa tiết đóa sen nổi, quai lụa mềm mại rủ tự nhiên và khớp khít đầu nhân vật.
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

class DetailedMeshBuilder:
    def __init__(self, name):
        self.name = name
        self.vertices = []
        self.normals = []
        self.uvs = []
        self.materials = {}
        self.current_material = "default"

    def set_material(self, mat_name, kd=(0.8, 0.8, 0.8), ks=(0.1, 0.1, 0.1), ns=20, d=1.0):
        self.current_material = mat_name
        if mat_name not in self.materials:
            self.materials[mat_name] = {
                "kd": kd,
                "ks": ks,
                "ns": ns,
                "d": d,
                "faces": []
            }

    def add_vertex(self, x, y, z):
        self.vertices.append((x, y, z))
        return len(self.vertices)

    def add_normal(self, nx, ny, nz):
        l = math.hypot(nx, ny, nz) or 1.0
        self.normals.append((nx/l, ny/l, nz/l))
        return len(self.normals)

    def add_uv(self, u, v):
        self.uvs.append((u, v))
        return len(self.uvs)

    def add_face(self, v_idx, n_idx=None, uv_idx=None):
        if self.current_material not in self.materials:
            self.set_material(self.current_material)
        self.materials[self.current_material]["faces"].append((v_idx, n_idx, uv_idx))

    def export_obj_mtl(self, out_dir, filename_prefix, scale=1.0):
        obj_path = os.path.join(out_dir, f"{filename_prefix}.obj")
        mtl_path = os.path.join(out_dir, f"{filename_prefix}.mtl")

        with open(mtl_path, "w", encoding="utf-8") as fm:
            fm.write(f"# Coohom & WebGL High-Detail Material for {filename_prefix}\n")
            for m_name, m_data in self.materials.items():
                fm.write(f"newmtl {m_name}\n")
                r, g, b = m_data["kd"]
                fm.write(f"Kd {r:.4f} {g:.4f} {b:.4f}\n")
                kr, kg, kb = m_data["ks"]
                fm.write(f"Ks {kr:.4f} {kg:.4f} {kb:.4f}\n")
                fm.write(f"Ns {m_data['ns']}\n")
                fm.write(f"d {m_data['d']:.2f}\n")
                fm.write("illum 2\n\n")

        with open(obj_path, "w", encoding="utf-8") as fo:
            fo.write(f"# High-Precision 3D Model: {filename_prefix}\n")
            fo.write(f"mtllib {filename_prefix}.mtl\n")
            for x, y, z in self.vertices:
                fo.write(f"v {x*scale:.4f} {y*scale:.4f} {z*scale:.4f}\n")
            for u, v in self.uvs:
                fo.write(f"vt {u:.4f} {v:.4f}\n")
            for nx, ny, nz in self.normals:
                fo.write(f"vn {nx:.4f} {ny:.4f} {nz:.4f}\n")

            for m_name, m_data in self.materials.items():
                if not m_data["faces"]:
                    continue
                fo.write(f"usemtl {m_name}\n")
                for v_l, n_l, uv_l in m_data["faces"]:
                    if uv_l and n_l:
                        face_s = " ".join(f"{v}/{u}/{n}" for v, u, n in zip(v_l, uv_l, n_l))
                    elif n_l:
                        face_s = " ".join(f"{v}//{n}" for v, n in zip(v_l, n_l))
                    else:
                        face_s = " ".join(str(v) for v in v_l)
                    fo.write(f"f {face_s}\n")

        return obj_path, mtl_path

def build_accurate_non_la():
    """
    Xây dựng Nón Lá Thêu Sen với đầy đủ cấu trúc:
    - Sườn nón cong 16 vành tre uốn cong tự nhiên
    - Đỉnh nón có búi khâu lá chóp
    - Vành cái nẹp cật tre dưới đáy
    - Đóa sen thêu nổi 3D: cánh sen hồng, nhụy vàng, lá sen xanh
    - Quai lụa mềm mại rủ tự nhiên với nút thắt nơ
    """
    builder = DetailedMeshBuilder("non_la_theu_sen_v2")

    # Kích thước tiêu chuẩn (hệ mét trong Three.js, khi xuất Coohom nhân 1000 sang mm)
    R_BASE = 0.208  # Đường kính đáy = 416 mm
    H_CONE = 0.215  # Chiều cao nón = 215 mm
    R_TOP = 0.012   # Bán kính đỉnh chóp bo tròn
    RINGS = 16      # 16 vành nón truyền thống
    SEGS = 48       # 48 lát cắt chu vi cho mặt cong mượt mà

    # 1. Thân nón lá nón sấy trắng ngà / vàng rơm dịu mát
    builder.set_material("LaNonTuNhien", kd=(0.92, 0.87, 0.74), ks=(0.15, 0.15, 0.12), ns=15)

    # Lập bảng cao độ và bán kính cho 16 vành nón (đường cong sườn nón uốn nhẹ)
    profile_points = []
    for ring_i in range(RINGS + 1):
        frac = ring_i / RINGS  # 0 ở đáy, 1 ở đỉnh
        # Hàm đường cong sườn nón lá truyền thống: hơi loe nhẹ ở vành, thon đều lên đỉnh
        # y đi từ 0 (đáy) lên H_CONE (đỉnh)
        y = H_CONE * frac
        # Bán kính tại độ cao y: đường cong uốn nhẹ tự nhiên
        r = R_BASE * math.pow(1.0 - frac, 0.92) + R_TOP * frac
        profile_points.append((y, r))

    # Tạo lưới mặt ngoài và mặt trong của thân nón (có độ dày 1.5mm)
    thickness = 0.0015
    for ring_i, (y, r) in enumerate(profile_points):
        v_u = ring_i / RINGS
        # Vòng đỉnh hơi nghiêng góc nón
        slope = math.atan2(R_BASE, H_CONE)
        ny_out = math.sin(slope)
        nr_out = math.cos(slope)

        for seg_j in range(SEGS):
            theta = 2 * math.pi * seg_j / SEGS
            ct = math.cos(theta)
            st = math.sin(theta)

            x = r * ct
            z = r * st
            # Mặt ngoài
            builder.add_vertex(x, y, z)
            builder.add_normal(nr_out * ct, ny_out, nr_out * st)
            builder.add_uv(seg_j / SEGS, v_u)

            # Mặt trong (lòng nón)
            r_in = max(0.002, r - thickness)
            builder.add_vertex(r_in * ct, y, r_in * st)
            builder.add_normal(-nr_out * ct, -ny_out, -nr_out * st)
            builder.add_uv(seg_j / SEGS, v_u)

    # Nối các mặt thân nón
    stride = SEGS * 2
    for ring_i in range(RINGS):
        r_start_curr = ring_i * stride
        r_start_next = (ring_i + 1) * stride
        for seg_j in range(SEGS):
            next_j = (seg_j + 1) % SEGS

            # Mặt ngoài (v_out)
            o1 = r_start_curr + seg_j * 2 + 1
            o2 = r_start_curr + next_j * 2 + 1
            o3 = r_start_next + next_j * 2 + 1
            o4 = r_start_next + seg_j * 2 + 1
            builder.add_face([o1, o2, o3], [o1, o2, o3], [o1, o2, o3])
            builder.add_face([o1, o3, o4], [o1, o3, o4], [o1, o3, o4])

            # Mặt trong (v_in)
            i1 = r_start_curr + seg_j * 2 + 2
            i2 = r_start_curr + next_j * 2 + 2
            i3 = r_start_next + next_j * 2 + 2
            i4 = r_start_next + seg_j * 2 + 2
            builder.add_face([i1, i3, i2], [i1, i3, i2], [i1, i3, i2])
            builder.add_face([i1, i4, i3], [i1, i4, i3], [i1, i4, i3])

    # 2. Vành cái (Vành nẹp tre chân nón)
    builder.set_material("VanhCaiTreGia", kd=(0.76, 0.65, 0.48), ks=(0.25, 0.20, 0.15), ns=30)
    # Vành tròn tiết diện elip 3mm x 4mm nẹp quanh đáy
    rim_v_start = len(builder.vertices)
    rim_segs = 48
    rim_rad_segs = 8
    rim_r_major = R_BASE
    rim_r_minor = 0.003
    for i in range(rim_segs):
        th = 2 * math.pi * i / rim_segs
        ct, st = math.cos(th), math.sin(th)
        for j in range(rim_rad_segs):
            phi = 2 * math.pi * j / rim_rad_segs
            cp, sp = math.cos(phi), math.sin(phi)
            xr = (rim_r_major + rim_r_minor * cp) * ct
            zr = (rim_r_major + rim_r_minor * cp) * st
            yr = rim_r_minor * sp + 0.002
            builder.add_vertex(xr, yr, zr)
            builder.add_normal(cp * ct, sp, cp * st)
            builder.add_uv(i / rim_segs, j / rim_rad_segs)

    for i in range(rim_segs):
        next_i = (i + 1) % rim_segs
        for j in range(rim_rad_segs):
            next_j = (j + 1) % rim_rad_segs
            idx1 = rim_v_start + 1 + i * rim_rad_segs + j
            idx2 = rim_v_start + 1 + next_i * rim_rad_segs + j
            idx3 = rim_v_start + 1 + next_i * rim_rad_segs + next_j
            idx4 = rim_v_start + 1 + i * rim_rad_segs + next_j
            builder.add_face([idx1, idx2, idx3], [idx1, idx2, idx3], [idx1, idx2, idx3])
            builder.add_face([idx1, idx3, idx4], [idx1, idx3, idx4], [idx1, idx3, idx4])

    # 3. Đỉnh chóp nón khâu lá
    builder.set_material("ChopNonTre", kd=(0.70, 0.58, 0.40), ks=(0.2, 0.2, 0.1), ns=20)
    chop_v_start = len(builder.vertices)
    builder.add_vertex(0, H_CONE + 0.008, 0) # đỉnh chóp tròn
    builder.add_normal(0, 1, 0)
    builder.add_uv(0.5, 0.5)
    c_tip = len(builder.vertices)
    for seg_j in range(SEGS):
        theta = 2 * math.pi * seg_j / SEGS
        builder.add_vertex(R_TOP * math.cos(theta), H_CONE, R_TOP * math.sin(theta))
        builder.add_normal(math.cos(theta)*0.7, 0.7, math.sin(theta)*0.7)
        builder.add_uv(0.5 + 0.4*math.cos(theta), 0.5 + 0.4*math.sin(theta))
    for seg_j in range(SEGS):
        next_j = (seg_j + 1) % SEGS
        p1 = c_tip + seg_j
        p2 = c_tip + next_j
        builder.add_face([c_tip - 1, p1, p2], [c_tip - 1, p1, p2], [c_tip - 1, p1, p2])

    # 4. Họa tiết thêu Sen 3D (Cánh sen hồng phấn, nhụy vàng, lá sen biếc)
    # Tọa độ mặt trước nón: góc theta = 0, z dương
    # Chiều cao thêu y = 0.08m đến 0.14m
    builder.set_material("ChiTheuSenHong", kd=(0.95, 0.54, 0.66), ks=(0.25, 0.20, 0.20), ns=25)
    # Tâm hoa sen tại y = 0.10, z tương ứng với sườn nón
    y_lotus = 0.095
    r_lotus_surface = R_BASE * math.pow(1.0 - (y_lotus / H_CONE), 0.92) + 0.002
    z_lotus = r_lotus_surface

    # Đóa sen gồm 5 cánh hé nở uốn cong ôm lấy nhau
    petal_angles = [-0.35, -0.18, 0.0, 0.18, 0.35]
    for p_ang in petal_angles:
        # Cánh sen cong hình elip
        p_base = len(builder.vertices)
        for py_i in range(5):
            frac_py = py_i / 4.0
            p_w = 0.016 * math.sin(frac_py * math.pi)
            p_y = y_lotus + frac_py * 0.038
            p_z = z_lotus + 0.003 * math.sin(frac_py * math.pi)
            # 2 điểm trái phải của cánh
            x_left = math.sin(p_ang) * 0.02 - p_w
            x_right = math.sin(p_ang) * 0.02 + p_w
            builder.add_vertex(x_left, p_y, p_z)
            builder.add_normal(0, 0.3, 0.95)
            builder.add_uv(0.2, frac_py)
            builder.add_vertex(x_right, p_y, p_z)
            builder.add_normal(0, 0.3, 0.95)
            builder.add_uv(0.8, frac_py)
        for py_i in range(4):
            v1 = p_base + 1 + py_i * 2
            v2 = p_base + 2 + py_i * 2
            v3 = p_base + 4 + py_i * 2
            v4 = p_base + 3 + py_i * 2
            builder.add_face([v1, v2, v3], [v1, v2, v3], [v1, v2, v3])
            builder.add_face([v1, v3, v4], [v1, v3, v4], [v1, v3, v4])

    # Nhụy sen vàng tươi
    builder.set_material("ChiTheuNhuyVang", kd=(0.98, 0.82, 0.22), ks=(0.3, 0.3, 0.1), ns=40)
    nhuy_base = len(builder.vertices)
    builder.add_vertex(0, y_lotus + 0.016, z_lotus + 0.004)
    builder.add_normal(0, 0.2, 0.98)
    builder.add_uv(0.5, 0.5)
    for k in range(8):
        th_k = 2 * math.pi * k / 8
        builder.add_vertex(0.007 * math.cos(th_k), y_lotus + 0.016 + 0.007 * math.sin(th_k), z_lotus + 0.003)
        builder.add_normal(0, 0.2, 0.98)
        builder.add_uv(0.5 + 0.5*math.cos(th_k), 0.5 + 0.5*math.sin(th_k))
    for k in range(8):
        k_next = (k + 1) % 8
        builder.add_face([nhuy_base + 1, nhuy_base + 2 + k, nhuy_base + 2 + k_next],
                         [nhuy_base + 1, nhuy_base + 2 + k, nhuy_base + 2 + k_next],
                         [nhuy_base + 1, nhuy_base + 2 + k, nhuy_base + 2 + k_next])

    # Cành lá sen thêu xanh ngọc bích
    builder.set_material("ChiTheuLaXanh", kd=(0.28, 0.62, 0.38), ks=(0.2, 0.3, 0.2), ns=25)
    # Cuống sen uốn cong từ hoa xuống vành
    stem_points = [
        (0.00, y_lotus, z_lotus),
        (0.02, y_lotus - 0.02, z_lotus * 1.08),
        (0.035, y_lotus - 0.045, z_lotus * 1.18),
        (0.045, y_lotus - 0.065, z_lotus * 1.28),
    ]
    stem_base = len(builder.vertices)
    for sp_x, sp_y, sp_z in stem_points:
        builder.add_vertex(sp_x - 0.002, sp_y, sp_z)
        builder.add_normal(0, 0.2, 0.98)
        builder.add_uv(0, 0)
        builder.add_vertex(sp_x + 0.002, sp_y, sp_z)
        builder.add_normal(0, 0.2, 0.98)
        builder.add_uv(1, 0)
    for sp_i in range(len(stem_points) - 1):
        s1 = stem_base + 1 + sp_i * 2
        s2 = stem_base + 2 + sp_i * 2
        s3 = stem_base + 4 + sp_i * 2
        s4 = stem_base + 3 + sp_i * 2
        builder.add_face([s1, s2, s3], [s1, s2, s3], [s1, s2, s3])
        builder.add_face([s1, s3, s4], [s1, s3, s4], [s1, s3, s4])

    # Lá sen non cách điệu bên cạnh
    leaf_base = len(builder.vertices)
    leaf_cx = 0.05
    leaf_cy = y_lotus - 0.035
    leaf_cz = z_lotus * 1.15
    for lk in range(12):
        th_l = 2 * math.pi * lk / 12
        lr = 0.018 * (1.0 + 0.2 * math.sin(th_l * 3))
        builder.add_vertex(leaf_cx + lr * math.cos(th_l), leaf_cy + lr * math.sin(th_l) * 0.7, leaf_cz)
        builder.add_normal(0, 0.3, 0.95)
        builder.add_uv(0.5 + 0.5*math.cos(th_l), 0.5 + 0.5*math.sin(th_l))
    center_leaf = builder.add_vertex(leaf_cx, leaf_cy, leaf_cz + 0.002)
    builder.add_normal(0, 0.3, 0.95)
    builder.add_uv(0.5, 0.5)
    for lk in range(12):
        lk_next = (lk + 1) % 12
        builder.add_face([center_leaf, leaf_base + 1 + lk, leaf_base + 1 + lk_next],
                         [center_leaf, leaf_base + 1 + lk, leaf_base + 1 + lk_next],
                         [center_leaf, leaf_base + 1 + lk, leaf_base + 1 + lk_next])

    # 5. Quai lụa tơ tằm mềm mại rủ tự nhiên
    builder.set_material("QuaiLuaHongSen", kd=(0.94, 0.65, 0.72), ks=(0.35, 0.30, 0.30), ns=45)
    # Quai gắn tại vành thứ 4 bên trong lòng nón (y = 0.05m, x = ±0.14m)
    # Rủ cong xuống dưới cằm (y = -0.16m)
    strap_nodes_L = [
        (-0.140, 0.050, 0.000),
        (-0.135, 0.010, 0.008),
        (-0.120, -0.040, 0.015),
        (-0.090, -0.090, 0.022),
        (-0.055, -0.130, 0.028),
        (-0.018, -0.155, 0.032),
        (0.000, -0.160, 0.034) # Gặp nhau tại nút thắt dưới cằm
    ]

    strap_nodes_R = [
        (0.140, 0.050, 0.000),
        (0.135, 0.010, 0.008),
        (0.120, -0.040, 0.015),
        (0.090, -0.090, 0.022),
        (0.055, -0.130, 0.028),
        (0.018, -0.155, 0.032),
        (0.000, -0.160, 0.034)
    ]

    def build_ribbon_strip(nodes, width=0.014):
        rib_base = len(builder.vertices)
        for idx, (nx, ny, nz) in enumerate(nodes):
            v_prog = idx / (len(nodes) - 1)
            builder.add_vertex(nx, ny, nz - width/2)
            builder.add_normal(0, 0.2, 0.98)
            builder.add_uv(0, v_prog)
            builder.add_vertex(nx, ny, nz + width/2)
            builder.add_normal(0, 0.2, 0.98)
            builder.add_uv(1, v_prog)
        for idx in range(len(nodes) - 1):
            q1 = rib_base + 1 + idx * 2
            q2 = rib_base + 2 + idx * 2
            q3 = rib_base + 4 + idx * 2
            q4 = rib_base + 3 + idx * 2
            builder.add_face([q1, q2, q3], [q1, q2, q3], [q1, q2, q3])
            builder.add_face([q1, q3, q4], [q1, q3, q4], [q1, q3, q4])

    build_ribbon_strip(strap_nodes_L)
    build_ribbon_strip(strap_nodes_R)

    # Nút thắt nơ rủ tự nhiên (2 dải đuôi nơ rủ xuống ngực)
    tail_nodes_1 = [
        (0.005, -0.160, 0.035),
        (0.012, -0.200, 0.040),
        (0.018, -0.245, 0.042),
        (0.022, -0.290, 0.040)
    ]
    tail_nodes_2 = [
        (-0.005, -0.160, 0.035),
        (-0.010, -0.195, 0.038),
        (-0.016, -0.235, 0.040),
        (-0.020, -0.275, 0.039)
    ]
    build_ribbon_strip(tail_nodes_1, width=0.012)
    build_ribbon_strip(tail_nodes_2, width=0.012)

    return builder

def main():
    print("=== TẠO MÔ HÌNH 3D CHI TIẾT CAO: NÓN LÁ THÊU SEN (ITEM #1) ===")
    builder = build_accurate_non_la()

    # 1. Xuất WebGL / Three.js (Hệ mét)
    obj_m, mtl_m = builder.export_obj_mtl(OUTPUT_MODELS_DIR, "non_la_theu_sen_v2", scale=1.0)
    print(f"✓ Đã xuất OBJ (Meters): {obj_m} ({len(builder.vertices)} đỉnh, {sum(len(m['faces']) for m in builder.materials.values())} đa giác)")

    # 2. Xuất Coohom ZIP Package (Hệ mm)
    coohom_temp = os.path.join(OUTPUT_MODELS_DIR, "coohom_temp_nonla")
    os.makedirs(coohom_temp, exist_ok=True)
    obj_mm, mtl_mm = builder.export_obj_mtl(coohom_temp, "non_la_theu_sen", scale=1000.0)

    zip_path = os.path.join(OUTPUT_ZIP_DIR, "coohom_non_la_theu_sen.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(obj_mm, arcname="non_la_theu_sen.obj")
        zf.write(mtl_mm, arcname="non_la_theu_sen.mtl")
        meta = {
            "id": "non_la_theu_sen",
            "name": "Nón Lá Thêu Hoa Sen Nam Bộ",
            "category": "Accessories / Headwear",
            "dimensions_mm": {"width": 416, "depth": 416, "height": 223},
            "features": [
                "16 vành tre truyền thống sườn nón uốn cong chuẩn xác",
                "Họa tiết đóa hoa sen thêu nổi 3D, cánh sen hồng, nhụy vàng, lá biếc",
                "Vành cái nẹp cật tre đáy nón bóng mịn",
                "Quai lụa mềm mại rủ tự nhiên với nút thắt nơ dưới cằm"
            ],
            "units": "mm",
            "pivot": "rim_center"
        }
        zf.writestr("metadata.json", json.dumps(meta, ensure_ascii=False, indent=2))

    os.remove(obj_mm)
    os.remove(mtl_mm)
    os.rmdir(coohom_temp)
    print(f"✓ Đã đóng gói Coohom: {zip_path}")

if __name__ == "__main__":
    main()
