import bpy,math,random,os
from mathutils import Vector
p='/Users/macos/Desktop/Chùa online/Thiết kế giao diện/Giảng đường 3D';bpy.ops.wm.open_mainfile(filepath=os.path.join(p,'giang-duong-phat-phap.blend'));s=bpy.context.scene;random.seed(34)
def mat(n,c):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;b=m.node_tree.nodes.get('Principled BSDF');b.inputs['Base Color'].default_value=(*c,1);b.inputs['Roughness'].default_value=.85;return m
w=bpy.data.materials['Gỗ dầm']; frame=bpy.data.materials['Gỗ sáng'];green=[mat('Lá vườn %d'%i,c) for i,c in enumerate([(.11,.23,.07),(.17,.32,.09),(.24,.39,.12),(.31,.43,.15)])];earth=mat('Nền vườn',(.22,.3,.12));trunk=mat('Vỏ cây',(.22,.13,.06))
def box(n,loc,dim,m):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(m);return o
def cyl(n,loc,r,h,m):
 bpy.ops.mesh.primitive_cylinder_add(vertices=12,radius=r,depth=h,location=loc);o=bpy.context.object;o.name=n;o.data.materials.append(m)
def ball(n,loc,scale,m):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=8,location=loc);o=bpy.context.object;o.name=n;o.scale=scale;o.data.materials.append(m);bpy.ops.object.shade_smooth()
# Side transoms over the open galleries.
for side in (-1,1):
 x=side*7.8
 for yy in (-9,-3,3,9,15):
  box('Thanh cửa ngang',(x,yy,6.4),(.12,5.4,.13),frame)
  box('Thanh cửa trên',(x,yy,7.35),(.12,5.4,.16),w)
  for j in range(10):box('Song cửa cao',(x,yy-2.45+j*.54,6.9),(.11,.09,.88),frame)
# External gardens are part of the hall scene, not user avatars.
for side in (-1,1):
 box('Vườn bên',(side*17,2,-.22),(18,52,.3),earth)
 for y in range(-13,26,5):
  for depth in (12,20):
   x=side*(depth+random.uniform(-1,1)); yy=y+random.uniform(-1,1);h=random.uniform(4.5,7.0)
   cyl('Thân cây',(x,yy,h/2),.18,h,trunk)
   for k in range(10):
    a=random.random()*math.tau;r=random.uniform(.3,2.0)
    ball('Tán cây',(x+r*math.cos(a),yy+r*math.sin(a),h+random.uniform(-1,1)),(1.2,1.0,.7),random.choice(green))
# Warm daylight travels through openings.
s.world.use_nodes=True;bg=s.world.node_tree.nodes.get('Background');bg.inputs['Color'].default_value=(.40,.51,.40,1);bg.inputs['Strength'].default_value=.32
bpy.ops.object.light_add(type='SUN',location=(-10,-4,15));o=bpy.context.object;o.rotation_euler=(math.radians(28),math.radians(-25),math.radians(-28));o.data.energy=1.6;o.data.color=(1,.78,.56);o.data.angle=math.radians(8)
s.cycles.samples=24
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(p,'giang-duong-co-canh-quan.blend'))
bpy.ops.export_scene.gltf(filepath=os.path.join(p,'giang-duong-co-canh-quan.glb'),export_format='GLB')
s.render.filepath=os.path.join(p,'giang-duong-co-canh-quan.png');bpy.ops.render.render(write_still=True)
