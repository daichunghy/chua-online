# V15 OPS — engine bien dang luoi cho sculpt bang script (khong dung brush):
# - groove: khac ranh am doc polyline (do sau/rong cho truoc, falloff Gauss)
# - dent: lom diem (lo mui) theo Gauss quanh tam, huong -normal
# - ridge: nang dai hep (song mui) theo Gauss quanh truc, huong +normal
# - blend_to_ref: keo dinh ve be mat tham chieu (BVH pristine) theo mat na
# Tat ca thao tac tren toa do THE GIOI cua mot object (matrix_world = I khi
# lam viec trong file rieng — cac script buoc se bake transform truoc).
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree

def world_verts(o):
    vs = np.empty(len(o.data.vertices) * 3, dtype=np.float64)
    o.data.vertices.foreach_get("co", vs)
    return vs.reshape(-1, 3)

def set_world_verts(o, W):
    M = np.array(o.matrix_world, dtype=np.float64)
    Minv = np.linalg.inv(M)
    L = W @ Minv[:3, :3].T + Minv[:3, 3]
    o.data.vertices.foreach_set("co", L.reshape(-1).astype(np.float32))
    o.data.update()

def vert_normals(o):
    # Blender 5 bo Mesh.calc_loop_normals -> tu tinh: phap tuyen dinh =
    # trung binh phap tuyen mat (trong so dien tich) cua cac mat ke.
    me = o.data
    n = len(me.vertices)
    pn = np.empty(len(me.polygons) * 3, dtype=np.float64)
    me.polygons.foreach_get("normal", pn)
    pn = pn.reshape(-1, 3)
    pa = np.empty(len(me.polygons), dtype=np.float64)
    me.polygons.foreach_get("area", pa)
    ls = np.empty(len(me.polygons), dtype=np.int32)
    me.polygons.foreach_get("loop_start", ls)
    lt = np.empty(len(me.polygons), dtype=np.int32)
    me.polygons.foreach_get("loop_total", lt)
    lf = np.repeat(np.arange(len(me.polygons)), lt)
    lv = np.empty(len(me.loops), dtype=np.int32)
    me.loops.foreach_get("vertex_index", lv)
    acc = np.zeros((n, 3))
    np.add.at(acc, lv, pn[lf] * pa[lf][:, None])
    norm = np.linalg.norm(acc, axis=1, keepdims=True)
    return acc / np.maximum(norm, 1e-9)

def dist_to_polyline(P, path):
    """P (N,3), path (M,3) -> khoang cach toi doan thang gan nhat (N,)"""
    best = np.full(len(P), 1e18)
    for a, b in zip(path[:-1], path[1:]):
        ab = b - a
        t = np.clip(((P - a) @ ab) / max(float(ab @ ab), 1e-12), 0.0, 1.0)
        q = a + t[:, None] * ab
        d = np.linalg.norm(P - q, axis=1)
        best = np.minimum(best, d)
    return best

def groove(o, path, depth, width, zone=None):
    """Ranh am: dich dinh vao trong (-normal) theo Gauss cua khoang cach
    toi path. zone: (center, radius) gioi han vung anh huong (loc truoc)."""
    W = world_verts(o)
    N = vert_normals(o)
    d = dist_to_polyline(W, np.array(path, dtype=np.float64))
    w = np.exp(-(d / width) ** 2)
    if zone is not None:
        c, r = np.array(zone[0]), zone[1]
        zmask = np.linalg.norm(W - c, axis=1) < r
        w = np.where(zmask, w, 0.0)
    W2 = W - N * (depth * w)[:, None]
    set_world_verts(o, W2)
    return float((depth * w).max())

def dent(o, center, radius, depth):
    """Lom diem (lo mui): -normal, Gauss theo khoang cach toi tam."""
    W = world_verts(o)
    N = vert_normals(o)
    d = np.linalg.norm(W - np.array(center, dtype=np.float64), axis=1)
    w = np.exp(-(d / radius) ** 2)
    W2 = W - N * (depth * w)[:, None]
    set_world_verts(o, W2)
    return float((depth * w).max())

def ridge(o, path, height, width):
    """Nang dai (song mui): +normal, Gauss theo khoang cach toi path."""
    W = world_verts(o)
    N = vert_normals(o)
    d = dist_to_polyline(W, np.array(path, dtype=np.float64))
    w = np.exp(-(d / width) ** 2)
    W2 = W + N * (height * w)[:, None]
    set_world_verts(o, W2)
    return float((height * w).max())

def blend_to_ref(o, bvh, mask_pts_mask, factor):
    """Keo cac dinh duoc chon ve diem gan nhat tren be mat tham chieu.
    mask: boolean array tren dinh. Tra ve do dich max."""
    W = world_verts(o)
    idx = np.where(mask_pts_mask)[0]
    if len(idx) == 0:
        return 0.0
    maxd = 0.0
    for i in idx:
        loc, _, _, _ = bvh.find_nearest(Vector(W[i]))
        if loc is not None:
            delta = np.array(loc) - W[i]
            maxd = max(maxd, float(np.linalg.norm(delta)))
            W[i] = W[i] + delta * factor
    set_world_verts(o, W)
    return maxd

def smooth_region(o, mask, iterations=2, factor=0.5):
    """Lam muot Laplacian trong vung mask (hoa khoi ma): dung lien ket
    canh cua luoi."""
    import bmesh
    me = o.data
    W = world_verts(o)
    edges = np.empty(len(me.edges) * 2, dtype=np.int32)
    me.edges.foreach_get("vertices", edges)
    edges = edges.reshape(-1, 2)
    neigh = {}
    for a, b in edges:
        neigh.setdefault(int(a), []).append(int(b))
        neigh.setdefault(int(b), []).append(int(a))
    idx = np.where(mask)[0]
    for _ in range(iterations):
        new = W.copy()
        for i in idx:
            ns = neigh.get(int(i))
            if ns:
                avg = W[ns].mean(axis=0)
                new[i] = W[i] + (avg - W[i]) * factor
        W = new
    set_world_verts(o, W)

def build_bvh_from_objs(objs):
    """BVH be mat the gioi tu nhieu object (dung lam tham chieu pristine)."""
    verts = []
    polys = []
    off = 0
    for o in objs:
        W = world_verts(o)
        verts.append(W)
        for p in o.data.polygons:
            polys.append(tuple(off + i for i in p.vertices))
        off += len(W)
    V = np.vstack(verts)
    return BVHTree.FromPolygons([Vector(v) for v in V], polys,
                                all_triangles=False, epsilon=0.0)

def build_bvh_from_arrays(verts_list, polys_list):
    """BVH tu cac mang (verts, polys) da o toa do the gioi."""
    verts = []
    polys = []
    off = 0
    for V, P in zip(verts_list, polys_list):
        verts.append(np.asarray(V, dtype=np.float64))
        for p in P:
            polys.append(tuple(off + int(i) for i in p))
        off += len(V)
    V = np.vstack(verts)
    return BVHTree.FromPolygons([Vector(v) for v in V], polys,
                                all_triangles=False, epsilon=0.0)

def build_bvh_labeled(verts_list, polys_list):
    """BVH + nhan theo MAT: face_labels[i] = chi so manh cua polygon i.
    Dung de gan nhan dinh theo be mat pristine gan nhat (khong chay mau
    nhan nhu KD theo dinh mau)."""
    verts = []
    polys = []
    face_labels = []
    off = 0
    for pi, (V, P) in enumerate(zip(verts_list, polys_list)):
        verts.append(np.asarray(V, dtype=np.float64))
        for p in P:
            polys.append(tuple(off + int(i) for i in p))
            face_labels.append(pi)
        off += len(V)
    V = np.vstack(verts)
    bvh = BVHTree.FromPolygons([Vector(v) for v in V], polys,
                               all_triangles=False, epsilon=0.0)
    return bvh, face_labels

def label_by_surface(bvh, face_labels, piece_names, pts):
    """Gan nhan cho tung diem = manh chua mat pristine gan nhat."""
    out = []
    for p in pts:
        _, _, fi, _ = bvh.find_nearest(Vector(p))
        out.append(piece_names[face_labels[fi]] if fi is not None else None)
    return out

def deviation_stats(o, bvh):
    """Khoang cach dinh -> be mat tham chieu: (max, mean, p99)."""
    W = world_verts(o)
    ds = np.empty(len(W))
    for i, p in enumerate(W):
        loc, _, _, dist = bvh.find_nearest(Vector(p))
        ds[i] = dist if dist is not None else 0.0
    return float(ds.max()), float(ds.mean()), float(np.percentile(ds, 99))
