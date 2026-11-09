"""Thay image lattice v2 (đậm nét) vào 2 material V11_Lattice + V11_LatticeMini."""
import bpy

DST = "/home/hatch/workspace/chua-online-work/layout_v13_v11.blend"
SRC = "/home/hatch/workspace/chua-online-work/textures/v11_lattice.png"

img = bpy.data.images.load(SRC, check_existing=False)
img.pack()
print("loaded:", img.name, tuple(img.size))
for mname in ('V11_Lattice', 'V11_LatticeMini'):
    m = bpy.data.materials[mname]
    for n in m.node_tree.nodes:
        if n.type == 'TEX_IMAGE':
            n.image = img
            print(mname, "-> image set")
bpy.ops.wm.save_as_mainfile(filepath=DST)
print("SAVED", DST)
