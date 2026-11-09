import bpy

def dump_mat(name):
    m = bpy.data.materials.get(name)
    print(f"== MAT {name}: {'MISSING' if not m else 'found'}")
    if not m or not m.use_nodes:
        return
    for n in m.node_tree.nodes:
        extra = ""
        if n.type == 'TEX_IMAGE':
            img = n.image
            extra = f" img={img.name if img else None} size={tuple(img.size) if img else None} cs={img.colorspace_settings.name if img else ''} ext={n.extension}"
        if n.type == 'MAPPING':
            extra = f" vtype={n.vector_type} loc={tuple(round(v,3) for v in n.inputs['Location'].default_value)} rot={tuple(round(v,3) for v in n.inputs['Rotation'].default_value)} scale={tuple(round(v,3) for v in n.inputs['Scale'].default_value)}"
        if n.type == 'TEX_COORD':
            extra = f" from_instancer={n.from_instancer}"
        links = [f"{l.from_node.name}.{l.from_socket.name}->{l.to_socket.name}" for l in n.inputs[0].links] if n.type == 'TEX_IMAGE' and n.inputs and n.inputs[0].links else ""
        print(f"   {n.bl_idname} '{n.name}' {extra} {links}")

for name in ('V11_Lattice', 'V11_LatticeMini', 'V10_Lattice'):
    dump_mat(name)

# material names actually on the panel objects
for oname in ('V11_Ped_Panel', 'V11_Pyl_Panel', 'V11_Tier_Lattice'):
    o = bpy.data.objects.get(oname)
    if o:
        print(oname, "mats:", [ms.material.name if ms.material else None for ms in o.material_slots])

# UV bounds per object (front-facing polys by normal)
def uv_report(oname):
    o = bpy.data.objects.get(oname)
    if not o or o.type != 'MESH':
        print(oname, "no mesh"); return
    me = o.data
    if not me.uv_layers:
        print(oname, "NO UV LAYER"); return
    uv = me.uv_layers.active.data
    import collections
    per_face = collections.defaultdict(list)
    for p in me.polygons:
        for li in p.loop_indices:
            per_face[p.index].append(uv[li].uv)
    print(f"-- {oname}: {len(me.polygons)} polys")
    for i, uvs in sorted(per_face.items()):
        xs = [u[0] for u in uvs]; ys = [u[1] for u in uvs]
        n = me.polygons[i].normal
        print(f"   poly{i} n=({n.x:.2f},{n.y:.2f},{n.z:.2f}) U[{min(xs):.3f},{max(xs):.3f}] V[{min(ys):.3f},{max(ys):.3f}]")

uv_report('V11_Ped_Panel')
uv_report('V11_Tier_Lattice')
