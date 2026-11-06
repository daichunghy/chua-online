"""Repair the 15 verified repo props -> GLB in fixed/ + beauty render fixed_<item>.png.
Usage: blender -b --factory-startup -noaudio --python fix_props.py -- <item> [item...]
Originals are never modified; all work happens on imported copies.
"""
import bpy, os, sys, math, random
from mathutils import Vector, Matrix

random.seed(20261106)
BASE = os.path.expanduser("~/workspace/chua-online-work/repo-items")
FIXED = os.path.join(BASE, "fixed")
os.makedirs(FIXED, exist_ok=True)

CATALOG = {  # x, y, z meters (w, d, h) from danh_muc_vat_pham.json
 "mo_go_tung_kinh": (0.240, 0.240, 0.200), "bat_nhang_tram": (0.180, 0.180, 0.320),
 "nen_hoa_sen": (0.140, 0.140, 0.100), "den_hoa_dang": (0.200, 0.200, 0.080),
 "mam_ngu_qua": (0.360, 0.360, 0.160), "bo_doan_dai_sen": (0.450, 0.450, 0.120),
 "bo_doan_tron": (0.400, 0.400, 0.100), "chieu_coi_thien": (0.800, 1.600, 0.014),
 "dia_banh_bo": (0.280, 0.280, 0.070), "dia_banh_da_lon": (0.280, 0.280, 0.060),
 "trai_dua_xiem": (0.180, 0.180, 0.260), "quat_nan_la_dua": (0.280, 0.020, 0.380),
 "gio_may_tre": (0.340, 0.280, 0.360), "chum_sanh_hoa_sen": (0.480, 0.480, 0.500),
 "den_long_luc_giac": (0.440, 0.440, 0.520),
}

# ---------------- materials ----------------
def make_mat(name, color, rough=0.6, metal=0.0, emission=None, e_strength=0.0):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if emission:
        b.inputs["Emission Color"].default_value = (*emission, 1)
        b.inputs["Emission Strength"].default_value = e_strength
    return m

MAT_TUNE = {  # (item, material) -> overrides applied to imported Principled mats
 ("bat_nhang_tram", "DongCoHoaVan"): dict(color=(0.45, 0.30, 0.15), metal=0.7, rough=0.45),
 ("bat_nhang_tram", "DiemThanRuc"): dict(emission=(1.0, 0.35, 0.08), e_strength=1.6),
 ("bat_nhang_tram", "TroNhangTrangXam"): dict(rough=1.0),
 ("nen_hoa_sen", "NgonLuaVangCam"): dict(emission=(1.0, 0.55, 0.12), e_strength=2.5),
 ("den_hoa_dang", "NgonLuaHoaDang"): dict(emission=(1.0, 0.70, 0.20), e_strength=2.2),
 ("den_hoa_dang", "CanhGiayHongSen"): dict(emission=(0.90, 0.35, 0.45), e_strength=0.22),
 ("bo_doan_dai_sen", "ChiTheuVangKim"): dict(color=(0.85, 0.70, 0.25), metal=0.85, rough=0.35),
 ("mam_ngu_qua", "VienVangKim"): dict(metal=0.8, rough=0.35),
}

def tune_materials(item):
    for m in bpy.data.materials:
        if not m.use_nodes:
            continue
        try:
            b = m.node_tree.nodes["Principled BSDF"]
        except Exception:
            continue
        b.inputs["Roughness"].default_value = 0.62
        b.inputs["Metallic"].default_value = 0.0
        ov = MAT_TUNE.get((item, m.name))
        if ov:
            if "color" in ov: b.inputs["Base Color"].default_value = (*ov["color"], 1)
            if "metal" in ov: b.inputs["Metallic"].default_value = ov["metal"]
            if "rough" in ov: b.inputs["Roughness"].default_value = ov["rough"]
            if "emission" in ov:
                b.inputs["Emission Color"].default_value = (*ov["emission"], 1)
                b.inputs["Emission Strength"].default_value = ov["e_strength"]

# ---------------- mesh extraction / rebuild ----------------
def import_obj(item):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.wm.obj_import(filepath=os.path.join(BASE, item + ".obj"))
    objs = [o for o in bpy.context.scene.objects if o.type == 'MESH']
    return objs[0]

def extract(obj):
    me = obj.data; mw = obj.matrix_world
    verts = [tuple(mw @ v.co) for v in me.vertices]
    faces = [(tuple(p.vertices), p.material_index) for p in me.polygons]
    mats = [m.name if m else None for m in me.materials]
    return verts, faces, mats

def compute_islands(nverts, faces):
    parent = list(range(nverts))
    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]; a = parent[a]
        return a
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb: parent[ra] = rb
    for idxs, _ in faces:
        for a, b in zip(idxs, idxs[1:] + idxs[:1]):
            union(a, b)
    isl = {}
    for fi, (idxs, _) in enumerate(faces):
        isl.setdefault(find(idxs[0]), []).append(fi)
    return list(isl.values())

def island_info(verts, faces, mats, fis):
    vs = set()
    mnames = {}
    for fi in fis:
        idxs, mi = faces[fi]
        vs.update(idxs)
        mnames[mats[mi]] = mnames.get(mats[mi], 0) + 1
    pts = [verts[v] for v in vs]
    mn = tuple(min(p[i] for p in pts) for i in range(3))
    mx = tuple(max(p[i] for p in pts) for i in range(3))
    return {"faces": fis, "verts": vs, "mats": mnames, "min": mn, "max": mx,
            "nf": len(fis)}

def fix_normals(ob):
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)
    if ob.data.has_custom_normals:
        try: bpy.ops.mesh.customdata_custom_splitnormals_clear()
        except Exception: pass
    try: bpy.ops.object.shade_smooth_by_angle()
    except Exception:
        for p in ob.data.polygons: p.use_smooth = True
    ob.select_set(False)
    ob.data.update()

def build_object(name, verts, faces, mats, face_subset, vert_fn=None, mat_override=None):
    used = {}; new_verts = []; new_faces = []; new_mis = []
    slot_map = {}; mat_slots = []
    for fi in face_subset:
        idxs, mi = faces[fi]
        ni = []
        for vi in idxs:
            if vi not in used:
                v = verts[vi]
                if vert_fn: v = vert_fn(v, vi)
                used[vi] = len(new_verts); new_verts.append(tuple(v))
            ni.append(used[vi])
        mname = mats[mi] if mi < len(mats) else None
        if mat_override and fi in mat_override: mname = mat_override[fi]
        if mname not in slot_map:
            slot_map[mname] = len(mat_slots); mat_slots.append(mname)
        new_faces.append(ni); new_mis.append(slot_map[mname])
    me = bpy.data.meshes.new(name)
    me.from_pydata(new_verts, [], new_faces)
    for mname in mat_slots:
        me.materials.append(bpy.data.materials.get(mname) if mname else None)
    for p, mi in zip(me.polygons, new_mis):
        p.material_index = mi
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    fix_normals(ob)
    return ob

def bake(ob):
    # matrix_world is stale in background mode until the view layer updates;
    # without this, rotations set on the object are silently lost (handle
    # tubes baked as vertical dashes). Force the update first.
    bpy.context.view_layer.update()
    ob.data.transform(ob.matrix_world)
    ob.matrix_world = Matrix.Identity(4)
    ob.data.update()
    return ob

def assign_mat(ob, mat):
    ob.data.materials.clear()
    ob.data.materials.append(mat)
    return ob

def smooth(ob):
    for p in ob.data.polygons: p.use_smooth = True
    ob.data.update()
    return ob

# ---------------- primitive helpers (all return baked objects) ----------------
def disc(name, radius, loc, mat, n=40):
    bpy.ops.mesh.primitive_circle_add(vertices=n, radius=radius, fill_type='NGON', location=loc)
    ob = bpy.context.object; ob.name = name
    assign_mat(ob, mat); return bake(ob)

def box(name, dims, loc, mat, rotz=0.0):
    # NOTE: ob.dimensions= proved unreliable headless (stale bound box -> unit cubes).
    # Build the cuboid deterministically from raw data instead.
    hx, hy, hz = dims[0] / 2, dims[1] / 2, dims[2] / 2
    verts = [(sx * hx, sy * hy, sz * hz)
             for sz in (-1, 1) for sy in (-1, 1) for sx in (-1, 1)]
    # index = (x>0) + (y>0)*2 + (z>0)*4
    faces = [(0, 2, 3, 1), (4, 5, 7, 6), (0, 1, 5, 4),
             (2, 6, 7, 3), (0, 4, 6, 2), (1, 3, 7, 5)]
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.materials.append(mat)
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    ob.matrix_world = (Matrix.Translation(Vector(loc))
                       @ Matrix.Rotation(rotz, 4, 'Z'))
    return bake(ob)

def tube(name, p1, p2, r, mat, n=10):
    d = Vector(p2) - Vector(p1); mid = (Vector(p1) + Vector(p2)) / 2
    bpy.ops.mesh.primitive_cylinder_add(vertices=n, radius=r, depth=d.length, location=mid)
    ob = bpy.context.object; ob.name = name
    ob.rotation_mode = 'QUATERNION'
    ob.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d.normalized())
    assign_mat(ob, mat); return bake(ob)

def sphere(name, r, loc, mat, scale=(1, 1, 1), seg=24, rings=16):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=rings, radius=r, location=loc)
    ob = bpy.context.object; ob.name = name; ob.scale = scale
    assign_mat(ob, mat); bake(ob); return smooth(ob)

def torus(name, major, minor, loc, mat, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor,
        major_segments=40, minor_segments=10, location=loc, rotation=rot)
    ob = bpy.context.object; ob.name = name
    assign_mat(ob, mat); bake(ob); return smooth(ob)

def cone(name, r1, r2, depth, loc, mat, rot=(0, 0, 0), n=16):
    bpy.ops.mesh.primitive_cone_add(vertices=n, radius1=r1, radius2=r2, depth=depth,
                                    location=loc, rotation=rot)
    ob = bpy.context.object; ob.name = name
    assign_mat(ob, mat); bake(ob); return smooth(ob)

# ---------------- petal builder ----------------
def make_petal(name, L, W, mat, cup=0.20, bend=0.38):
    """Lotus petal: base at origin, extends +Y, tip pointed & rising (+Z curl)."""
    NY, NX = 7, 5
    verts = []; faces = []
    for j in range(NY):
        t = j / (NY - 1)
        y = t * L
        wprof = math.sin(math.pi * min(t * 1.12, 1.0)) ** 0.7
        hw = 0.5 * W * wprof
        zc = bend * L * t * t * 0.45
        for i in range(NX):
            u = i / (NX - 1)
            x = (u - 0.5) * 2 * hw
            z = zc + cup * W * ((u - 0.5) * 2) ** 2 * 0.30
            verts.append((x, y, z))
    for j in range(NY - 1):
        for i in range(NX - 1):
            a = j * NX + i; b = a + 1; c = a + NX; d = a + NX + 1
            faces.append((a, c, d, b))
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.materials.append(mat)
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    mod = ob.modifiers.new("sol", 'SOLIDIFY'); mod.thickness = 0.0016
    bpy.context.view_layer.objects.active = ob; ob.select_set(True)
    bpy.ops.object.modifier_apply(modifier="sol")
    ob.select_set(False)
    for p in ob.data.polygons: p.use_smooth = True
    ob.data.update()
    return ob

def place_petal(ob, loc, azimuth_deg, lean_deg):
    """lean: 0 = upright, 90 = horizontal pointing outward, >90 = drooping outward."""
    m = (Matrix.Rotation(math.radians(azimuth_deg - 90), 4, 'Z')
         @ Matrix.Rotation(math.radians(90 - lean_deg), 4, 'X'))
    ob.matrix_world = Matrix.Translation(Vector(loc)) @ m
    return bake(ob)

def petal_ring(prefix, count, radius, z, L, W, mat, lean, phase=0.0):
    obs = []
    for k in range(count):
        az = phase + k * 360.0 / count
        p = make_petal(f"{prefix}_{k}", L, W, mat)
        place_petal(p, (radius * math.cos(math.radians(az)),
                        radius * math.sin(math.radians(az)), z), az, lean)
        obs.append(p)
    return obs

# ---------------- bbox / scale ----------------
def all_bbox(objects):
    mins = Vector((1e9, 1e9, 1e9)); maxs = Vector((-1e9, -1e9, -1e9))
    for o in objects:
        if o.type != 'MESH': continue
        for c in o.bound_box:
            w = o.matrix_world @ Vector(c)
            mins = Vector(map(min, mins, w)); maxs = Vector(map(max, maxs, w))
    return mins, maxs

def vert_bbox(objects):
    """BBox from raw vertex positions (bound_box lies for rotated tube segments)."""
    mins = Vector((1e9, 1e9, 1e9)); maxs = Vector((-1e9, -1e9, -1e9))
    for o in objects:
        if o.type != 'MESH': continue
        mw = o.matrix_world
        for v in o.data.vertices:
            w = mw @ v.co
            mins = Vector(map(min, mins, w)); maxs = Vector(map(max, maxs, w))
    return mins, maxs

def scale_objects(objects, sx, sy, sz):
    for ob in objects:
        if ob.type != 'MESH': continue
        inv = ob.matrix_world.inverted()
        for v in ob.data.vertices:
            w = ob.matrix_world @ v.co
            v.co = inv @ Vector((w.x * sx, w.y * sy, w.z * sz))
        ob.data.update()

def translate_objects(objects, dx, dy, dz):
    for ob in objects:
        if ob.type != 'MESH': continue
        inv = ob.matrix_world.inverted()
        for v in ob.data.vertices:
            w = ob.matrix_world @ v.co
            v.co = inv @ Vector((w.x + dx, w.y + dy, w.z + dz))
        ob.data.update()

# ---------------- studio render + finish ----------------
def point_at(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat('-Z', 'Y').to_euler()

def render_studio(item, objects):
    mins, maxs = all_bbox(objects)
    center = (mins + maxs) / 2; dims = maxs - mins; diag = max(dims.length, 0.05)
    mat_floor = make_mat("Floor", (0.52, 0.48, 0.44), 0.95)
    bpy.ops.mesh.primitive_plane_add(size=max(diag * 8, 4), location=(center.x, center.y, mins.z - 0.001))
    assign_mat(bpy.context.object, mat_floor)
    mat_bd = make_mat("Backdrop", (0.62, 0.58, 0.53), 0.95)
    bpy.ops.mesh.primitive_plane_add(size=max(diag * 10, 6),
        location=(center.x, center.y + diag * 2.2, center.z))
    bd = bpy.context.object; bd.rotation_euler = (math.radians(90), 0, 0)
    assign_mat(bd, mat_bd)
    def add_light(name, loc, energy, color, size):
        ld = bpy.data.lights.new(name, 'AREA'); ld.energy = energy; ld.color = color
        ld.shape = 'DISK'; ld.size = size
        lo = bpy.data.objects.new(name, ld); bpy.context.collection.objects.link(lo)
        lo.location = loc; point_at(lo, center); return lo
    add_light("Key", center + Vector((diag * 1.6, -diag * 1.4, diag * 1.8)), 45 * diag * diag, (1.0, 0.9, 0.78), diag * 2.5)
    add_light("Fill", center + Vector((-diag * 1.8, -diag * 0.6, diag * 0.7)), 15 * diag * diag, (0.78, 0.86, 1.0), diag * 2.5)
    add_light("Rim", center + Vector((0, diag * 1.8, diag * 1.2)), 25 * diag * diag, (1.0, 0.95, 0.85), diag * 2.0)
    w = bpy.data.worlds.new("W"); bpy.context.scene.world = w; w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = (0.30, 0.28, 0.26, 1)
    w.node_tree.nodes["Background"].inputs[1].default_value = 0.3
    cam_data = bpy.data.cameras.new("Cam"); cam_data.lens = 50
    cam = bpy.data.objects.new("Cam", cam_data); bpy.context.collection.objects.link(cam)
    dist = max(diag * 1.8, 0.3)
    cam.location = center + Vector((dist * 0.72, -dist * 0.72, dist * 0.45))
    point_at(cam, center + Vector((0, 0, -dims.z * 0.08)))
    bpy.context.scene.camera = cam
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'; sc.cycles.samples = 32; sc.cycles.use_denoising = True
    sc.render.resolution_x = 720; sc.render.resolution_y = 720
    sc.view_settings.view_transform = 'AgX'
    sc.render.filepath = os.path.join(BASE, "fixed_" + item + ".png")
    bpy.ops.render.render(write_still=True)

def finish(item, objects):
    mins, _ = all_bbox(objects)
    if mins.z < -0.001:
        translate_objects(objects, 0, 0, -mins.z)
    bpy.ops.object.select_all(action='DESELECT')
    for ob in objects: ob.select_set(True)
    bpy.context.view_layer.objects.active = objects[0]
    bpy.ops.export_scene.gltf(filepath=os.path.join(FIXED, item + ".glb"),
        export_format='GLB', use_selection=True, export_apply=True)
    mins, maxs = all_bbox(objects)
    dims = [round((maxs[i] - mins[i]) * 1000) for i in range(3)]
    if os.environ.get("FIX_RENDER", "1") != "0":
        render_studio(item, objects)
    else:
        print("RENDER_SKIPPED (coordination hold)", item)
    print("FIX_DONE", item, "dims_mm=", dims, "catalog_mm=",
          [round(c * 1000) for c in CATALOG[item]])
    return dims

def load(item):
    """Import OBJ, return (verts, faces, mats, islands_info, src_obj)."""
    src = import_obj(item)
    verts, faces, mats = extract(src)
    islands = [island_info(verts, faces, mats, fis)
               for fis in compute_islands(len(verts), faces)]
    return verts, faces, mats, islands, src

def drop_src(src):
    bpy.data.objects.remove(src, do_unlink=True)

def faces_where(islands, pred):
    out = []
    for isl in islands:
        if pred(isl): out += isl["faces"]
    return out

# ================= item fixers =================
def fix_bo_doan_tron(item):
    verts, faces, mats, islands, src = load(item)
    ob = build_object(item, verts, faces, mats, list(range(len(faces))))
    drop_src(src); tune_materials(item)
    return finish(item, [ob])

def fix_chieu_coi_thien(item):
    verts, faces, mats, islands, src = load(item)
    ob = build_object(item, verts, faces, mats, list(range(len(faces))))
    drop_src(src); tune_materials(item)
    # woven read: generated UVs + procedural checker bump on the sedge material
    bpy.context.view_layer.objects.active = ob; ob.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    try: bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=0.002)
    except Exception as e: print("UV_FAIL", e)
    bpy.ops.object.mode_set(mode='OBJECT'); ob.select_set(False)
    img = bpy.data.images.new("WeaveBump", 256, 256)
    px = []
    for y in range(256):
        for x in range(256):
            c = 0.78 if ((x // 32) + (y // 32)) % 2 == 0 else 0.32
            px += [c, c, c, 1.0]
    img.pixels = px
    mat = bpy.data.materials.get("CoiTuNhienVangRom")
    if mat:
        nt = mat.node_tree; bsdf = nt.nodes["Principled BSDF"]
        coord = nt.nodes.new("ShaderNodeTexCoord")
        mapn = nt.nodes.new("ShaderNodeMapping"); mapn.inputs["Scale"].default_value = (7, 14, 1)
        tex = nt.nodes.new("ShaderNodeTexImage"); tex.image = img; tex.extension = 'REPEAT'
        tex.image.colorspace_settings.name = 'Non-Color'
        bump = nt.nodes.new("ShaderNodeBump")
        bump.inputs["Strength"].default_value = 0.65; bump.inputs["Distance"].default_value = 0.0012
        nt.links.new(coord.outputs["UV"], mapn.inputs["Vector"])
        nt.links.new(mapn.outputs["Vector"], tex.inputs["Vector"])
        nt.links.new(tex.outputs["Color"], bump.inputs["Height"])
        nt.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    return finish(item, [ob])

def fix_trai_dua_xiem(item):
    verts, faces, mats, islands, src = load(item)
    shell = faces_where(islands, lambda i: "VoDuaXanhNon" in i["mats"])
    # drop shell faces fully below the cut plane z=0.012
    drop = set()
    for fi in shell:
        idxs, _ = faces[fi]
        if all(verts[v][2] < 0.012 for v in idxs): drop.add(fi)
    keep = [fi for fi in range(len(faces)) if fi not in drop]
    ob = build_object(item, verts, faces, mats, keep)
    # flat base disc sized from the lowest remaining shell verts
    low = [v.co for v in ob.data.vertices if v.co.z < 0.02]
    zc = min(v.z for v in low); r = max(math.hypot(v.x, v.y) for v in low)
    green = bpy.data.materials.get("VoDuaXanhNon")
    d = disc("dua_base", r * 1.02, (0, 0, zc + 0.0005), green)
    drop_src(src); tune_materials(item)
    objs = [ob, d]
    scale_objects(objs, 1.0, 1.0, 260 / 300)  # total height 300 -> 260
    return finish(item, objs)

def fix_dia_banh_da_lon(item):
    verts, faces, mats, islands, src = load(item)
    plate = faces_where(islands, lambda i: "DiaGomMocTrang" in i["mats"])
    ob = build_object(item, verts, faces, mats, plate)
    drop_src(src); tune_materials(item)
    layers = [(0.32, 0.60, 0.36), (0.95, 0.94, 0.90), (0.90, 0.80, 0.40),
              (0.45, 0.30, 0.55), (0.92, 0.55, 0.65)]  # pandan, coconut, mung, purple, pink
    lmats = [make_mat(f"DaLon_L{k}", c, 0.25) for k, c in enumerate(layers)]
    objs = [ob]
    positions = [(-0.040, -0.030, 0.14), (0.042, -0.028, -0.21),
                 (-0.038, 0.034, -0.10), (0.040, 0.032, 0.24)]
    for si, (px, py, rz) in enumerate(positions):
        for li, lm in enumerate(lmats):
            z = 0.013 + li * 0.0092 + 0.0046
            objs.append(box(f"slice{si}_l{li}", (0.068, 0.046, 0.0092),
                            (px, py, z), lm, rotz=rz))
    return finish(item, objs)

def fix_dia_banh_bo(item):
    verts, faces, mats, islands, src = load(item)
    cake_verts = set()
    for isl in islands:
        if "BanhBoThotNotVang" in isl["mats"]: cake_verts |= isl["verts"]
    def jitter(v, vi):
        if vi in cake_verts and v[2] > 0.045:
            f = (v[2] - 0.045) / 0.027
            return (v[0] + random.uniform(-0.0008, 0.0008) * f,
                    v[1] + random.uniform(-0.0008, 0.0008) * f,
                    v[2] + random.uniform(-0.0018, 0.0012) * f)
        return v
    ob = build_object(item, verts, faces, mats, list(range(len(faces))), vert_fn=jitter)
    drop_src(src); tune_materials(item)
    objs = [ob]
    strand_mat = make_mat("DuaSoiTrang", (0.96, 0.94, 0.89), 0.9)
    centers = [(-0.045, -0.045), (0.045, -0.045), (-0.045, 0.045), (0.045, 0.045), (0.0, 0.0)]
    for ci, (cx, cy) in enumerate(centers):
        for s in range(7):
            a = random.uniform(0, math.pi)
            dx, dy = math.cos(a) * 0.011, math.sin(a) * 0.011
            ox, oy = cx + random.uniform(-0.012, 0.012), cy + random.uniform(-0.012, 0.012)
            objs.append(box(f"strand_{ci}_{s}", (0.023, 0.0016, 0.0011),
                            (ox, oy, 0.0728), strand_mat, rotz=a))
    return finish(item, objs)

def fix_quat_nan_la_dua(item):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    leaf = make_mat("NanLaDuaVangNhat", (0.85, 0.78, 0.60), 0.8)
    wood = make_mat("CanTreGia", (0.65, 0.50, 0.30), 0.7)
    objs = []
    objs.append(cone("quat_handle", 0.007, 0.0105, 0.12, (0, 0, 0.06), wood, n=14))
    # blade: elliptical paddle, centre (0,0,0.25), rx=0.14, rz=0.13
    cx, cz, rx, rz = 0.0, 0.25, 0.14, 0.13
    SEG = 28
    verts = [(cx, 0.0, cz)]
    rings = []
    for t in (0.38, 0.72, 1.0):
        ring = []
        for k in range(SEG):
            a = 2 * math.pi * k / SEG
            x = cx + rx * t * math.cos(a)
            z = cz + rz * t * math.sin(a)
            y = 0.006 * math.sin(3 * a) * t
            ring.append(len(verts)); verts.append((x, y, z))
        rings.append(ring)
    faces = []
    for k in range(SEG):
        faces.append((0, rings[0][k], rings[0][(k + 1) % SEG]))
    for r in range(2):
        for k in range(SEG):
            a, b = rings[r][k], rings[r][(k + 1) % SEG]
            c, d = rings[r + 1][k], rings[r + 1][(k + 1) % SEG]
            faces.append((a, c, d, b))
    me = bpy.data.meshes.new("quat_blade"); me.from_pydata(verts, [], faces)
    me.materials.append(leaf)
    blade = bpy.data.objects.new("quat_blade", me)
    bpy.context.collection.objects.link(blade)
    mod = blade.modifiers.new("sol", 'SOLIDIFY'); mod.thickness = 0.003
    bpy.context.view_layer.objects.active = blade; blade.select_set(True)
    bpy.ops.object.modifier_apply(modifier="sol"); blade.select_set(False)
    smooth(blade); objs.append(blade)
    # radial ribs from handle top to blade edge
    pivot = Vector((0, 0.004, 0.125))
    for k in range(-5, 6):
        a = math.radians(k * 14)
        end = Vector((cx + rx * 0.97 * math.sin(a), 0.004,
                      cz + rz * 0.97 * math.cos(a) * (1 if k == 0 else 0.92)))
        if k != 0: end.z = cz + rz * 0.80 * math.cos(a)
        objs.append(tube(f"rib_{k}", pivot, end, 0.0022, wood, n=6))
    # two cross weave strips
    for zz, half in ((0.20, 0.128), (0.29, 0.133)):
        objs.append(box(f"weave_{zz}", (half * 2, 0.0016, 0.006), (0, 0.0045, zz), leaf))
    return finish(item, objs)

def fix_gio_may_tre(item):
    verts, faces, mats, islands, src = load(item)
    body = faces_where(islands, lambda i: i["max"][2] < 0.19)  # body island only (z 0..180)
    # drop any horizontal cap faces near the top of the body
    def is_cap(fi):
        idxs, _ = faces[fi]
        pts = [verts[v] for v in idxs]
        cz = sum(p[2] for p in pts) / len(pts)
        if cz < 0.168: return False
        # face normal z via first 3 verts
        a, b, c = (Vector(pts[0]), Vector(pts[1]), Vector(pts[2]))
        n = (b - a).cross(c - a)
        return n.length > 0 and abs(n.normalized().z) > 0.7
    body = [fi for fi in body if not is_cap(fi)]
    ob = build_object(item, verts, faces, mats, body)
    drop_src(src); tune_materials(item)
    rattan = bpy.data.materials.get("MayTreDanNauVang")
    objs = [ob]
    objs.append(torus("gio_rim", 0.163, 0.010, (0, 0, 0.182), rattan))
    dark = make_mat("GioTrongSam", (0.23, 0.16, 0.09), 1.0)
    objs.append(disc("gio_inner", 0.155, (0, 0, 0.115), dark))
    # handle: semicircle of tubes across the top, attached at both rim sides
    N = 14
    prev = None
    for k in range(N + 1):
        a = math.pi * k / N
        p = Vector((-0.148 * math.cos(a), 0, 0.185 + 0.148 * math.sin(a)))
        if prev is not None:
            objs.append(tube(f"gio_handle_{k}", prev, p, 0.0085, rattan, n=8))
        prev = p
    objs.append(tube("gio_post_l", (-0.148, 0, 0.150), (-0.148, 0, 0.190), 0.0085, rattan, n=8))
    objs.append(tube("gio_post_r", (0.148, 0, 0.150), (0.148, 0, 0.190), 0.0085, rattan, n=8))
    mins, maxs = vert_bbox(objs)
    hz = maxs.z - mins.z
    scale_objects(objs, 1.0, 280 / 334, 0.360 / hz)
    # second pass on true vertex extremes: force exact catalog height
    mins, maxs = vert_bbox(objs)
    scale_objects(objs, 1.0, 1.0, 0.360 / (maxs.z - mins.z))
    return finish(item, objs)

def fix_chum_sanh(item):
    verts, faces, mats, islands, src = load(item)
    dome = faces_where(islands, lambda i: "GomSanhDatNung" in i["mats"] and i["min"][2] > 0.40)
    lotus = faces_where(islands, lambda i: "HoaSenNoiHong" in i["mats"])
    rest = [fi for fi in range(len(faces)) if fi not in set(dome) and fi not in set(lotus)]
    # The jar body itself is a convex terracotta dome inside the mouth
    # (max z 0.48 at center) that buries the water disc (z 0.42-0.43):
    # flatten the dome below the water plane so the water surface shows.
    water_vis = set()
    for fi in rest:
        if mats[faces[fi][1]] == "MatNuocXanhLam":
            water_vis.update(faces[fi][0])
    def rest_fn(v, vi):
        if vi in water_vis: return (v[0] * 0.88, v[1] * 0.88, v[2])
        if v[2] > 0.40 and math.hypot(v[0], v[1]) < 0.175:
            return (v[0], v[1], 0.398)
        return v
    ob = build_object(item, verts, faces, mats, rest, vert_fn=rest_fn)
    # The source lotus (123 faces, no petal structure) is unusable: drop it
    # and rebuild a bud with real petal lobes, porting the cone-petal rings
    # that passed on the characters' held lotus (items_worn_v1_primitives):
    # flattened cones in 3 rings (outer 5 @32deg, mid 4 @18deg, inner 3 @8deg)
    # + green sepals, so the flower reads at a glance.
    drop_src(src); tune_materials(item)
    terracotta = bpy.data.materials.get("GomSanhDatNung")
    # (1) Rim torus so the mouth opening reads as a jar mouth. (A solid
    # neck cylinder was tried in v4 and its top cap sealed the mouth again
    # with terracotta, hiding the water — the rim alone frames the water.)
    rim = torus("chum_rim", 0.155, 0.012, (0, 0, 0.450), terracotta)
    # (2) Petal-lobed bud rising from the water (base at water level 0.42).
    mat_petal_o = make_mat("SenHongNgoai", (0.87, 0.50, 0.58), 0.7)
    mat_petal_m = make_mat("SenHongGiua", (0.92, 0.58, 0.64), 0.7)
    mat_petal_i = make_mat("SenHongTrong", (0.95, 0.68, 0.72), 0.7)
    mat_sepal = make_mat("SenSepalXanh", (0.25, 0.50, 0.30), 0.7)
    bud_base = Vector((0, 0, 0.420))
    def cone_petal(center, azimuth, tilt_deg, length, rad, material, name):
        tilt = math.radians(tilt_deg)
        dirv = Vector((math.sin(tilt) * math.cos(azimuth),
                       math.sin(tilt) * math.sin(azimuth), math.cos(tilt)))
        bpy.ops.mesh.primitive_cone_add(radius1=rad, radius2=0.0015, depth=length,
                                        vertices=12, location=center + dirv * (length * 0.38))
        p = bpy.context.object; p.name = name
        p.scale = (1.0, 0.42, 1.0)
        p.rotation_mode = 'QUATERNION'
        p.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(dirv)
        p.data.materials.append(material)
        return bake(p)
    bud = []
    for i in range(5):
        bud.append(cone_petal(bud_base, i * 2 * math.pi / 5, 32, 0.070, 0.020, mat_petal_o, f"SenNgoai_{i}"))
    for i in range(4):
        bud.append(cone_petal(bud_base, i * 2 * math.pi / 4 + 0.4, 18, 0.080, 0.018, mat_petal_m, f"SenGiua_{i}"))
    for i in range(3):
        bud.append(cone_petal(bud_base, i * 2 * math.pi / 3 + 0.8, 8, 0.085, 0.016, mat_petal_i, f"SenTrong_{i}"))
    for i in range(3):
        bud.append(cone_petal(bud_base + Vector((0, 0, -0.006)), i * 2 * math.pi / 3 + 0.3, 55, 0.045, 0.011, mat_sepal, f"SenSepal_{i}"))
    # (3) Leaves angled up out of the water (not flat plates). Rotation
    # must be set in the operator call, NOT on the object after bake():
    # bake() resets the origin to world (0,0,0), so a post-bake rotation
    # swings the leaf around the world origin (v4 bug: leaves flung to the
    # jar sides, dims blew out to 579x712).
    leaf_mat = make_mat("LaSenXanh", (0.25, 0.50, 0.30), 0.7)
    def tilted_disc(name, radius, loc, rot):
        bpy.ops.mesh.primitive_cylinder_add(vertices=40, radius=radius, depth=0.004,
                                            location=loc, rotation=rot)
        o = bpy.context.object; o.name = name
        assign_mat(o, leaf_mat); return bake(o)
    la1 = tilted_disc("la_1", 0.070, (-0.095, 0.055, 0.436),
                      (math.radians(52), 0, math.radians(25)))
    la2 = tilted_disc("la_2", 0.055, (0.105, 0.060, 0.436),
                      (math.radians(-48), 0, math.radians(-30)))
    objs = [ob, rim] + bud + [la1, la2]
    return finish(item, objs)

def fix_den_long(item):
    verts, faces, mats, islands, src = load(item)
    roof = faces_where(islands, lambda i: "KhungGoNauDo" in i["mats"] and i["min"][2] > 0.25)
    ob = build_object(item, verts, faces, mats, roof,
                      vert_fn=lambda v, vi: (v[0], v[1], v[2] + 0.140))
    drop_src(src)
    frame = make_mat("KhungGoNauDo", (0.50, 0.22, 0.16), 0.55)
    silk = make_mat("LuaVangTamLinh", (0.98, 0.72, 0.20), 0.7,
                    emission=(1.0, 0.72, 0.25), e_strength=0.55)
    red = make_mat("TuaRuaDoChua", (0.85, 0.15, 0.15), 0.8)
    objs = [ob]
    R = 0.212; apo = R * math.cos(math.radians(30))
    for k in range(6):
        a = math.radians(60 * k)
        objs.append(box(f"post_{k}", (0.016, 0.016, 0.262),
                        (R * math.cos(a), R * math.sin(a), 0.280), frame, rotz=a))
        fa = math.radians(30 + 60 * k)
        objs.append(box(f"panel_{k}", (0.190, 0.004, 0.244),
                        (apo * math.cos(fa), apo * math.sin(fa), 0.280), silk,
                        rotz=fa - math.pi / 2))
    for zz in (0.149, 0.411):
        bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=0.2275, depth=0.018,
                                            location=(0, 0, zz))
        rim = bpy.context.object; rim.name = f"rim_{zz}"
        assign_mat(rim, frame); objs.append(bake(rim))
    objs.append(box("tassel_link", (0.012, 0.012, 0.020), (0, 0, 0.135), frame))
    objs.append(sphere("tassel_bead", 0.016, (0, 0, 0.118), red))
    objs.append(cone("tassel", 0.020, 0.006, 0.095, (0, 0, 0.0575), red, n=14))
    cord_mat = make_mat("DayTreo", (0.25, 0.18, 0.12), 0.9)
    objs.append(tube("cord", (0, 0, 0.508), (0, 0, 0.545), 0.003, cord_mat, n=6))
    objs.append(torus("hook", 0.016, 0.0032, (0, 0, 0.560), cord_mat, rot=(math.radians(90), 0, 0)))
    mins, maxs = all_bbox(objs)
    sx = 0.440 / (maxs.x - mins.x); sz = 0.520 / (maxs.z - mins.z)
    scale_objects(objs, sx, sx, sz)
    return finish(item, objs)

def fix_mo_go(item):
    verts, faces, mats, islands, src = load(item)
    striker_mats = ("CanGoDui", "DauBocVaiNi")
    main_faces = faces_where(islands, lambda i: not any(m in i["mats"] for m in striker_mats))
    stk_faces = faces_where(islands, lambda i: any(m in i["mats"] for m in striker_mats))
    head_verts = set()
    for isl in islands:
        if "DauBocVaiNi" in isl["mats"]: head_verts |= isl["verts"]
    ob = build_object(item, verts, faces, mats, main_faces)
    P0 = Vector((0.150, -0.050, 0.020))
    DH = Vector((0, 0.120, 0.229))  # head centre -> shaft top
    R = Matrix.Rotation(math.radians(90), 4, 'Z') @ Matrix.Rotation(math.radians(90), 4, 'X')
    T = Vector((-0.114, -0.096, 0.047))
    def stk_fn(v, vi):
        p = Vector(v)
        if vi in head_verts: p += DH
        p = Vector((p.x, p.y, P0.z + (p.z - P0.z) * 0.88))
        return tuple(R @ (p - P0) + T)
    sob = build_object(item + "_dui", verts, faces, mats, stk_faces, vert_fn=stk_fn)
    drop_src(src); tune_materials(item)
    return finish(item, [ob, sob])

def fix_bat_nhang(item):
    verts, faces, mats, islands, src = load(item)
    override = {}
    for isl in islands:
        if "DiemThanRuc" in isl["mats"] and (isl["max"][2] - isl["min"][2]) > 0.10:
            for fi in isl["faces"]: override[fi] = "ChanHuongDo"  # shaft mislabeled as ember
    keep = [fi for fi in range(len(faces)) if mats[faces[fi][1]] != "TroNhangTrangXam"]
    def sc(v, vi): return (v[0] * 0.918, v[1] * 0.918, v[2] * 0.988)
    ob = build_object(item, verts, faces, mats, keep, vert_fn=sc, mat_override=override)
    drop_src(src); tune_materials(item)
    ash = bpy.data.materials.get("TroNhangTrangXam")
    d = disc("ash_top", 0.0745, (0, 0, 0.1065), ash, n=36)
    return finish(item, [ob, d])

def fix_nen_hoa_sen(item):
    verts, faces, mats, islands, src = load(item)
    boxes = faces_where(islands, lambda i: "DaiSenSapHong" in i["mats"] and i["nf"] == 12)
    keep = [fi for fi in range(len(faces)) if fi not in set(boxes)]
    def sc(v, vi): return (v[0] * 0.85, v[1] * 0.95, v[2] * 1.03)
    ob = build_object(item, verts, faces, mats, keep, vert_fn=sc)
    drop_src(src); tune_materials(item)
    wax = bpy.data.materials.get("DaiSenSapHong")
    objs = [ob] + petal_ring("nen_petal", 8, 0.043, 0.030, 0.037, 0.021, wax, lean=55)
    return finish(item, objs)

def fix_den_hoa_dang(item):
    verts, faces, mats, islands, src = load(item)
    boxes = faces_where(islands, lambda i: "CanhGiayHongSen" in i["mats"])
    keep = [fi for fi in range(len(faces)) if fi not in set(boxes)]
    def sc(v, vi): return (v[0], v[1], v[2] * 1.236)
    ob = build_object(item, verts, faces, mats, keep, vert_fn=sc)
    drop_src(src); tune_materials(item)
    paper = bpy.data.materials.get("CanhGiayHongSen")
    objs = [ob]
    objs += petal_ring("hd_outer", 8, 0.030, 0.017, 0.052, 0.026, paper, lean=68)
    objs += petal_ring("hd_inner", 6, 0.020, 0.021, 0.038, 0.020, paper, lean=38, phase=30)
    return finish(item, objs)

def fix_mam_ngu_qua(item):
    verts, faces, mats, islands, src = load(item)
    fruit_mats = ("MangCauXanh", "DuaXiemXanh", "XoaiCatVang", "DuDuVangCam")
    tray_faces = faces_where(islands, lambda i: not any(m in i["mats"] for m in fruit_mats)
                             and "ChumSungXanh" not in i["mats"])
    fig_faces = faces_where(islands, lambda i: "ChumSungXanh" in i["mats"])
    ob = build_object(item, verts, faces, mats, tray_faces,
                      vert_fn=lambda v, vi: (v[0] * 0.968, v[1] * 0.978, v[2]))
    sung_z = min(verts[vi][2] for fi in fig_faces for vi in faces[fi][0])
    fob = build_object(item + "_sung", verts, faces, mats, fig_faces,
                       vert_fn=lambda v, vi: (v[0] * 0.968, v[1] * 0.978 - 0.085, v[2] - sung_z + 0.028))
    drop_src(src); tune_materials(item)
    objs = [ob, fob]
    pomelo_m = make_mat("BuoiXanh", (0.62, 0.72, 0.32), 0.55)
    objs.append(sphere("pomelo1", 0.052, (0.0, 0.012, 0.078), pomelo_m, scale=(1, 1, 0.94)))
    objs.append(sphere("pomelo2", 0.040, (0.006, 0.006, 0.152 - 0.038), pomelo_m, scale=(1, 1, 0.94)))
    objs.append(tube("pomelo_stem", (0.006, 0.006, 0.148), (0.006, 0.006, 0.160),
                     0.0035, make_mat("CuongXanh", (0.35, 0.45, 0.2), 0.7), n=8))
    ca_m = make_mat("MangCauDa", (0.42, 0.62, 0.28), 0.6)
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, radius=0.042, location=(-0.075, 0.048, 0.068))
    ca = bpy.context.object; ca.name = "custard_apple"
    for v in ca.data.vertices:
        n = v.co.normalized(); v.co += n * random.uniform(-0.0032, 0.0032)
    assign_mat(ca, ca_m); bake(ca); smooth(ca); objs.append(ca)
    df_m = make_mat("ThanhLongHong", (0.86, 0.22, 0.42), 0.5)
    dfc = sphere("dragon_fruit", 0.036, (0.078, 0.048, 0.070), df_m, scale=(0.85, 0.85, 1.2))
    objs.append(dfc)
    sc_m = make_mat("VayThanhLong", (0.35, 0.65, 0.30), 0.6)
    for i in range(16):
        yy = 1 - (i / 15) * 1.6
        rr = math.sqrt(max(0.0, 1 - yy * yy)); th = i * 2.39996
        d = Vector((rr * math.cos(th), rr * math.sin(th), yy))
        pos = Vector((0.078 + d.x * 0.036 * 0.85, 0.048 + d.y * 0.036 * 0.85,
                      0.070 + d.z * 0.036 * 1.2)) + d * 0.002
        # rotation must go through cone()'s rot param: cone() bakes inside,
        # so a post-bake quaternion rotates the cone around the world origin
        # and flings the scales off the fruit (v2 bug: green cones floating
        # below the tray).
        q = Vector((0, 0, 1)).rotation_difference(d)
        c = cone(f"df_scale_{i}", 0.0045, 0.0, 0.009, tuple(pos), sc_m,
                 rot=q.to_euler(), n=6)
        objs.append(c)
    or_m = make_mat("CamVang", (0.95, 0.55, 0.10), 0.5)
    objs.append(sphere("orange", 0.030, (0.072, -0.072, 0.058), or_m))
    objs.append(tube("orange_dimple", (0.072, -0.072, 0.086), (0.072, -0.072, 0.0895),
                     0.004, make_mat("NumCam", (0.4, 0.35, 0.15), 0.8), n=8))
    bn_m = make_mat("ChuoiVang", (0.92, 0.80, 0.25), 0.55)
    bunch_o = Vector((0.058, -0.075, 0.030))
    for b in range(6):
        fan = math.radians(-40 + 16 * b)
        for s in range(4):
            t = -0.9 + s * 0.45
            lx = 0.052 * math.sin(t); lz = 0.052 * (1 - math.cos(t)) * 0.9 + s * 0.004
            p = Vector((lx * math.cos(fan), lx * math.sin(fan), lz)) + bunch_o
            objs.append(sphere(f"banana_{b}_{s}", 0.0135 - s * 0.0011, tuple(p), bn_m,
                               seg=12, rings=8))
    objs.append(tube("banana_stem", tuple(bunch_o + Vector((0, 0, -0.004))),
                     tuple(bunch_o + Vector((0, 0, 0.016))),
                     0.007, make_mat("CuongChuoi", (0.55, 0.5, 0.25), 0.8), n=8))
    return finish(item, objs)

def fix_bo_doan_dai_sen(item):
    verts, faces, mats, islands, src = load(item)
    keep = faces_where(islands, lambda i: "GamLamTimSang" in i["mats"])
    def sc(v, vi): return (v[0] * 0.9545, v[1] * 0.9545, v[2] * 1.045)
    ob = build_object(item, verts, faces, mats, keep, vert_fn=sc)
    drop_src(src); tune_materials(item)
    # Rose-pink petals (the previous gray-brown blended into the pale
    # cushion and the petals read as tabs): they must contrast to read.
    petal_m = make_mat("CanhSenHong", (0.78, 0.42, 0.50), 0.7)
    gold = bpy.data.materials.get("ChiTheuVangKim") or make_mat(
        "ChiTheuVangKim", (0.85, 0.70, 0.25), 0.35, metal=0.85)
    objs = [ob]
    # Petals sit ON the body surface (r 0.175 vs body r ~0.215), nearly
    # horizontal (lean 85) so they catch light and read as a petal ring
    # instead of drooping tabs hidden against the side.
    objs += petal_ring("bd_petal", 8, 0.175, 0.075, 0.055, 0.13, petal_m, lean=85)
    objs.append(torus("bd_gold_ring", 0.100, 0.0028, (0, 0, 0.1145), gold))
    return finish(item, objs)

FIXERS = {
 "bo_doan_tron": fix_bo_doan_tron, "chieu_coi_thien": fix_chieu_coi_thien,
 "trai_dua_xiem": fix_trai_dua_xiem, "dia_banh_da_lon": fix_dia_banh_da_lon,
 "dia_banh_bo": fix_dia_banh_bo, "quat_nan_la_dua": fix_quat_nan_la_dua,
 "gio_may_tre": fix_gio_may_tre, "chum_sanh_hoa_sen": fix_chum_sanh,
 "den_long_luc_giac": fix_den_long, "mo_go_tung_kinh": fix_mo_go,
 "bat_nhang_tram": fix_bat_nhang, "nen_hoa_sen": fix_nen_hoa_sen,
 "den_hoa_dang": fix_den_hoa_dang, "mam_ngu_qua": fix_mam_ngu_qua,
 "bo_doan_dai_sen": fix_bo_doan_dai_sen,
}

if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:]
    for item in argv:
        try:
            FIXERS[item](item)
        except Exception as e:
            import traceback; traceback.print_exc()
            print("FIX_FAIL", item, e)
