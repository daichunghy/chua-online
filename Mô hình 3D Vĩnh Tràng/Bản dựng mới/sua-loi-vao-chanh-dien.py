import bpy,os,math
from mathutils import Vector
p='/Users/macos/Desktop/Chùa online/Mô hình 3D Vĩnh Tràng/Bản dựng mới';bpy.ops.wm.open_mainfile(filepath=os.path.join(p,'chanh-dien-cua-vom.blend'));s=bpy.context.scene
remove=('Khoảng cửa chính','Khung cửa chính','Cánh cửa chính','Nẹp cửa chính','Thềm cửa chính','Bậc thềm','Lan can','Trụ lan can')
for o in list(s.objects):
 if o.name.startswith(remove):bpy.data.objects.remove(o,do_unlink=True)
def material(n,c,metal=0):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;b=m.node_tree.nodes.get('Principled BSDF');b.inputs['Base Color'].default_value=(*c,1);b.inputs['Metallic'].default_value=metal;return m
cream=material('Lan can màu kem',(.85,.69,.44));white=material('Con tiện trắng',(.88,.83,.69));gold=material('Sắt vàng cổ',(.48,.28,.065),.4);brown=material('Gờ màu đất',(.52,.19,.1));rock=material('Bậc đá',(.41,.40,.36))
def box(n,loc,dim,m):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(m);return o
def cyl(n,loc,r,h,m):
 bpy.ops.mesh.primitive_cylinder_add(vertices=12,radius=r,depth=h,location=loc);o=bpy.context.object;o.name=n;o.data.materials.append(m);return o
def line(n,pts,r,m):
 c=bpy.data.curves.new(n,'CURVE');c.dimensions='3D';c.bevel_depth=r;c.bevel_resolution=1;sp=c.splines.new('POLY');sp.points.add(len(pts)-1)
 for k,v in zip(sp.points,pts):k.co=(*v,1)
 o=bpy.data.objects.new(n,c);s.collection.objects.link(o);o.data.materials.append(m)
# Restore the centre bay's iron grille.
for x in (-.45,0,.45):box('Song cửa gian giữa',(x,-1.67,2.55),(.035,.05,2.75),gold)
for z in (1.35,2.15,2.95):box('Ngang cửa gian giữa',(0,-1.69,z),(1.42,.05,.035),gold)
for z in (1.8,2.65,3.4):line('Hoa sắt gian giữa',[(.24*math.cos(math.tau*j/32),-1.74,z+.24*math.sin(math.tau*j/32)) for j in range(33)],.016,gold)
# The raised terrace in front has a decorative balustrade rather than a central doorway.
box('Bệ tiền đình',(0,-3.6,.42),(6.7,3.0,.84),rock)
box('Nền tiền đình',(0,-3.6,.87),(6.8,3.1,.12),cream)
box('Lan can mặt trước',(0,-5.0,1.4),(4.4,.20,.14),cream)
box('Đế lan can mặt trước',(0,-5.0,1.0),(4.4,.20,.13),brown)
for i in range(19):
 x=-2.0+i*4/18;cyl('Con tiện mặt trước',(x,-5.0,1.20),.055,.38,white)
for x in (-2.3,2.3):box('Trụ lan can chính',(x,-5,1.23),(.30,.35,.8),cream)
# Mirrored side steps indicate lateral access; sizes are approximate pending survey.
for side in (-1,1):
 for i in range(5):
  x=side*(3.3+i*.30);z=.76-i*.15
  box('Bậc vào bên',(x,-3.55,z),(.34,2.4,.15),rock)
 for y in (-4.65,-2.45):
  for i in range(5):
   x=side*(3.05+i*.30);z=1.28-i*.15;cyl('Con tiện bên',(x,y,z),.04,.45,white)
  line('Tay vịn bên',[(side*3.05,y,1.55),(side*4.27,y,.95)],.085,cream)
# End bays are open side passages, visible as darker recesses.
for x in (-12,12):
 for obj in list(s.objects):
  if obj.name.startswith(('Song cửa','Ngang cửa','Hoa sắt cửa','Hoa văn sắt')) and abs(obj.location.x-x)<.9:bpy.data.objects.remove(obj,do_unlink=True)
# Save independently, preserve all prior versions.
s.cycles.samples=24;s.render.resolution_x=1800;s.render.resolution_y=1000
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(p,'chanh-dien-loi-ben.blend'))
bpy.ops.export_scene.gltf(filepath=os.path.join(p,'chanh-dien-loi-ben.glb'),export_format='GLB')
s.render.filepath=os.path.join(p,'chanh-dien-loi-ben.png');bpy.ops.render.render(write_still=True)
