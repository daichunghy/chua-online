import bpy,math,os
from mathutils import Vector
p='/Users/macos/Desktop/Chùa online/Mô hình 3D Vĩnh Tràng/Bản dựng mới'
bpy.ops.wm.open_mainfile(filepath=os.path.join(p,'chanh-dien-chi-tiet.blend'))
s=bpy.context.scene
# Remove the centre grille so the central arch reads as an entrance.
for o in list(bpy.data.objects):
 if o.name.startswith(('Song cửa','Ngang cửa')) and abs(o.location.x)<.6: bpy.data.objects.remove(o,do_unlink=True)
def mat(n,c,metal=0):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;b=m.node_tree.nodes.get('Principled BSDF');b.inputs['Base Color'].default_value=(*c,1);b.inputs['Metallic'].default_value=metal;b.inputs['Roughness'].default_value=.48;return m
gold=mat('Kim loại vàng cổ',(.48,.28,.065),.45); dark=mat('Cửa gỗ nâu sẫm',(.09,.05,.025));lit=mat('Gỗ cửa ấm',(.25,.11,.035));stone=mat('Gạch sân',(.56,.53,.48)); white=mat('Chỉ màu kem',(.91,.81,.62));terracotta=mat('Gờ đỏ',(.53,.20,.11))
def box(n,loc,dim,m):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(m);return o
def path(n,pts,r,m):
 c=bpy.data.curves.new(n,'CURVE');c.dimensions='3D';c.resolution_u=1;c.bevel_depth=r;c.bevel_resolution=1;sp=c.splines.new('POLY');sp.points.add(len(pts)-1)
 for p,v in zip(sp.points,pts):p.co=(*v,1)
 o=bpy.data.objects.new(n,c);s.collection.objects.link(o);o.data.materials.append(m)
def circle(n,x,y,z,r,m):path(n,[(x+r*math.cos(math.tau*j/32),y,z+r*math.sin(math.tau*j/32)) for j in range(33)],.016,m)
# Iron gates: symmetry, curls and floral rosettes referenced from the black/gold facade.
for i in range(13):
 x=-12+i*2
 if abs(x)<.1:continue
 for z in (1.8,2.65,3.4):
  circle('Hoa sắt cửa',x,-1.73,z,.24,gold)
  for side in (-1,1):
   pts=[]
   for j in range(18):
    t=j/17;a=t*math.pi*2;rad=.025+.13*t;pts.append((x+side*(.28+rad*math.cos(a)),-1.735,z+rad*math.sin(a)))
   path('Hoa văn sắt',pts,.015,gold)
 # scalloped red/yellow moulding atop each opening
 pts=[]
 for j in range(41):
  t=j/40;xx=-.84+1.68*t;zz=3.70+.78*(max(0,1-(xx/.84)**2)**.5)+.07*math.cos(t*math.pi*6)
  pts.append((x+xx,-1.97,zz))
 path('Vòm đa múi',pts,.055,terracotta)
# Entrance opening, intentionally unlettered.
box('Khoảng cửa chính',(0,-1.66,2.48),(1.52,.08,2.95),dark)
for side in (-1,1):
 x=side*.73;box('Khung cửa chính',(x,-1.78,2.43),(.14,.16,2.9),lit)
 box('Cánh cửa chính',(side*.54,-1.79,2.45),(.28,.13,2.65),lit)
 for z in (1.4,2.05,2.7,3.35):box('Nẹp cửa chính',(side*.54,-1.87,z),(.24,.04,.04),gold)
box('Thềm cửa chính',(0,-1.95,.96),(1.65,.8,.15),white)
# paving visible in foreground, subtle joints rather than an image texture.
for x in range(-17,18,2):box('Mạch gạch dọc',(x,-8.0,-.015),(.025,14,.015),white)
for y in range(-14,-1,2):box('Mạch gạch ngang',(0,y,-.012),(34,.025,.015),white)
# warmer daylight and soft shadow
s.world.color=(.52,.52,.52);s.cycles.samples=20;s.render.resolution_x=1800;s.render.resolution_y=1000;s.render.resolution_percentage=100
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(p,'chanh-dien-cua-vom.blend'))
bpy.ops.export_scene.gltf(filepath=os.path.join(p,'chanh-dien-cua-vom.glb'),export_format='GLB')
s.render.filepath=os.path.join(p,'chanh-dien-cua-vom.png');bpy.ops.render.render(write_still=True)
