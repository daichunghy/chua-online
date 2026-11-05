import bpy,math,os,random
from mathutils import Vector
out='/Users/macos/Desktop/Chùa online/Thiết kế giao diện/Giảng đường 3D'
bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene;random.seed(413)
s.world=bpy.data.worlds.new('Ánh sáng môi trường');s.world.color=(.19,.17,.13);s.render.engine='CYCLES';s.cycles.samples=32
s.render.resolution_x=900;s.render.resolution_y=1350;s.render.resolution_percentage=100
s.unit_settings.system='METRIC'
def material(n,c,rough=.65,metal=0):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;b=m.node_tree.nodes.get('Principled BSDF');b.inputs['Base Color'].default_value=(*c,1);b.inputs['Roughness'].default_value=rough;b.inputs['Metallic'].default_value=metal;return m
wood=material('Gỗ cột nâu đỏ',(.16,.047,.021)); wood2=material('Gỗ dầm',(.105,.032,.016));wood3=material('Gỗ sáng',(.30,.11,.035));wood4=material('Gỗ viền',(.21,.065,.02));gold=material('Đồng trang trí',(.47,.23,.06),.42,.35);wall=material('Vách màu đất',(.30,.22,.12));dark=material('Nền kệ',(.065,.025,.013));fabric=material('Đệm ngồi',(.24,.075,.043));tilem=[material('Gạch đất %02d'%i,(.37+i*.016,.12+i*.008,.065+i*.004),.82) for i in range(6)];book=material('Gáy sách',(.50,.23,.065));
def box(n,loc,dim,m,bevel=0):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(m)
 if bevel:
  mod=o.modifiers.new('Bo cạnh','BEVEL');mod.width=bevel;mod.segments=2
 return o
def cyl(n,loc,r,h,m):
 bpy.ops.mesh.primitive_cylinder_add(vertices=24,radius=r,depth=h,location=loc);o=bpy.context.object;o.name=n;o.data.materials.append(m);return o
def beam(n,a,b,w,m):
 a,b=Vector(a),Vector(b);d=b-a;o=box(n,(a+b)*.5,(w,w,d.length),m);o.rotation_euler=d.to_track_quat('Z','Y').to_euler();return o
def line(n,pts,r,m):
 c=bpy.data.curves.new(n,'CURVE');c.dimensions='3D';c.bevel_depth=r;c.bevel_resolution=2;sp=c.splines.new('POLY');sp.points.add(len(pts)-1)
 for p,v in zip(sp.points,pts):p.co=(*v,1)
 o=bpy.data.objects.new(n,c);s.collection.objects.link(o);o.data.materials.append(m)
# Hexagonal terracotta tile as one mesh with material variation.
verts=[];faces=[];ids=[];r=.38
for row in range(62):
 y=-15.0+row*1.5*r
 for col in range(27):
  x=(col-13)*math.sqrt(3)*r+(row%2)*math.sqrt(3)*r/2
  if abs(x)>8.8 or y>19:continue
  k=len(verts)
  for i in range(6):
   a=math.radians(60*i+30);verts.append((x+r*.979*math.cos(a),y+r*.979*math.sin(a),.02))
  faces.append(tuple(k+i for i in range(6)));ids.append(random.randrange(len(tilem)))
mesh=bpy.data.meshes.new('Lát nền');mesh.from_pydata(verts,[],faces);mesh.update();o=bpy.data.objects.new('Sàn gạch lục giác',mesh);s.collection.objects.link(o)
for m in tilem:o.data.materials.append(m)
for poly,i in zip(o.data.polygons,ids):poly.material_index=i
box('Nền sàn',(0,1,-.14),(18.5,36,.25),wood2)
# Dark timber columns running into the depth of the room.
for y in (-12,-6,0,6,12,18):
 for x in (-7.1,7.1):
  cyl('Chân cột đá',(x,y,.2),.49,.4,wall);cyl('Cột gỗ',(x,y,4.0),.32,7.6,wood)
  for z in (.5,7.55):cyl('Đai cột',(x,y,z),.37,.16,wood3)
 box('Xà ngang',(0,y,7.55),(14.8,.5,.46),wood2)
 # broad carved lintels and abstract floral curves, no invented writing
 if y in (-6,0,6,12):
  box('Xà chạm',(0,y-.20,7.03),(13.6,.24,.48),wood3,.035)
  for side in (-1,1):
   for j in range(7):
    cx=side*(.55+j*.86);pts=[]
    for i in range(31):
     t=i/30;a=math.tau*t;pts.append((cx+side*.31*math.sin(a),y-.345,7.02+.15*math.sin(2*a)))
    line('Hoa văn gỗ',pts,.022,wood4)
  for side in (-1,1):
   pts=[(side*(6.4-.5*math.sin(t*math.pi/2)),y-.2,7.0-1.25*t) for t in [i/20 for i in range(21)]];line('Đỡ đầu xà',pts,.10,wood3)
# Roof rafters and gable geometry.
for side in (-1,1):
 beam('Xà mái dọc',(side*7.3,-15,7.75),(side*7.3,19,7.75),.32,wood2)
 beam('Đòn nóc',(0,-15,11),(0,19,11),.38,wood2)
 for y in [-15+i*1.15 for i in range(31)]:
  beam('Kèo mái',(0,y,10.85),(side*7.5,y,7.65),.18,wood2)
 for x in (1.4,2.8,4.2,5.6,7):
  z=10.9-x*3.1/7.4;beam('Li tô mái',(side*x,-15,z),(side*x,19,z),.13,wood3)
 # Sloped terracotta roof panels prevent open sky at ceiling.
 verts=[(0,-15,10.95),(0,19,10.95),(side*7.6,19,7.65),(side*7.6,-15,7.65)]
 me=bpy.data.meshes.new('Mái');me.from_pydata(verts,[],[(0,1,2,3)]);me.update();o=bpy.data.objects.new('Mặt trong mái',me);s.collection.objects.link(o);o.data.materials.append(wood3)
# Railings and lower balustrades, sides open to daylight.
for side in (-1,1):
 for x in (side*7.65,side*8.5):
  beam('Tay vịn',(x,-14,1.2),(x,18,1.2),.12,wood3)
  beam('Gờ chân lan can',(x,-14,.28),(x,18,.28),.12,wood2)
  for i in range(52):
   y=-14+i*.62;box('Song gỗ',(x,y,.72),(.09,.09,.9),wood3)
# Raised stage with steps and lectern, deliberately no unverified inscription.
for i in range(4):box('Bậc giảng đường',(0,10+i*.42,.11+i*.17),(7.5,2,.22),wood3)
box('Bục giảng',(0,14,.65),(9,5,1.3),wood2)
box('Mặt bục',(0,14,1.33),(9.2,5.2,.12),wood3)
box('Bàn giảng',(0,14.1,1.92),(2.8,.8,1.15),wood3,.04)
box('Mặt bàn',(0,14.1,2.54),(3,.9,.12),wood4,.025)
for side in (-1,1):box('Chân bàn',(side*1.1,14.1,1.58),(.2,.7,.55),wood2)
# Rear bookshelf / wall pattern based on the approved image.
box('Tường hậu',(0,18,4.0),(14.7,.35,8.0),wood2)
box('Phông giữa',(0,17.72,4.3),(6.3,.15,5.3),wall)
box('Kệ sách',(0,17.58,3.25),(5.8,.25,3.1),dark)
for row in range(4):
 z=1.95+row*.71
 box('Đợt kệ',(0,17.37,z),(5.9,.35,.08),wood3)
 for i in range(21):
  x=-2.75+i*.275;h=.45+random.random()*.12
  box('Gáy kinh sách',(x,17.34,z+.08+h/2),(.19,.16,h),book)
  for zz in (z+.18,z+.26):box('Nẹp gáy sách',(x,17.24,zz),(.12,.02,.025),wood2)
# Low seating cushions in 2 rows, leaving a central approach.
for y in (-6,-1,4):
 for x in (-5,-3.35,3.35,5):
  o=box('Đệm ngồi',(x,y,.16),(1.12,.9,.24),fabric,.08)
# Lamp housings with actual lights; screens are warm ivory, not fake text.
lamp=material('Giấy đèn',(.91,.55,.22));b=lamp.node_tree.nodes.get('Principled BSDF');b.inputs['Emission Color'].default_value=(1,.45,.12,1);b.inputs['Emission Strength'].default_value=1.8
for x in (-4.4,4.4):
 cyl('Chân đèn',(x,11.6,1.1),.07,2.2,wood2);box('Lồng đèn',(x,11.6,2.35),(.55,.55,.85),lamp)
 for xx in (-.30,.30):box('Khung đèn',(x+xx,11.6,2.35),(.08,.64,.98),wood2)
 box('Mái đèn',(x,11.6,2.84),(.75,.75,.12),wood2)
 bpy.ops.object.light_add(type='POINT',location=(x,11.3,2.35));bpy.context.object.data.energy=55;bpy.context.object.data.color=(1,.53,.22)
# Light entering from side, warm and grounded, camera faces lectern.
bpy.ops.object.light_add(type='AREA',location=(-11,-2,7));o=bpy.context.object;o.data.energy=1600;o.data.size=9;o.rotation_euler=(Vector((0,5,1))-o.location).to_track_quat('-Z','Y').to_euler();o.data.color=(1,.73,.48)
bpy.ops.object.light_add(type='AREA',location=(10,6,7));o=bpy.context.object;o.data.energy=1200;o.data.size=8;o.rotation_euler=(Vector((0,6,2))-o.location).to_track_quat('-Z','Y').to_euler();o.data.color=(1,.78,.54)
bpy.ops.object.camera_add(location=(0,-15.2,2.6));c=bpy.context.object;c.rotation_euler=(Vector((0,13,4.0))-c.location).to_track_quat('-Z','Y').to_euler();c.data.lens=24;s.camera=c
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(out,'giang-duong-phat-phap.blend'))
bpy.ops.export_scene.gltf(filepath=os.path.join(out,'giang-duong-phat-phap.glb'),export_format='GLB')
s.render.filepath=os.path.join(out,'giang-duong-phat-phap.png');bpy.ops.render.render(write_still=True)
