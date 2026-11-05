import bpy, math, os, random
from mathutils import Vector
p='/Users/macos/Desktop/Chùa online/Mô hình 3D Vĩnh Tràng/Bản dựng mới'
bpy.ops.wm.open_mainfile(filepath=os.path.join(p,'mat-tien-vinh-trang.blend'))
s=bpy.context.scene
random.seed(12)
def material(n,c,rough=.75,metal=0):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;b=m.node_tree.nodes.get('Principled BSDF');b.inputs['Base Color'].default_value=(*c,1);b.inputs['Roughness'].default_value=rough;b.inputs['Metallic'].default_value=metal;return m
stone=material('Đá sân',(.53,.51,.46)); grass=material('Cỏ',(.22,.35,.15)); water=material('Nước hồ',(.13,.27,.25),.18); ivory=material('Vôi vàng',(.82,.67,.39)); blue=material('Gốm xanh',(.14,.36,.33)); ochre=material('Gờ vàng',(.68,.39,.10)); red=material('Ngói đất',(.44,.15,.10)); leaves=[material('Lá '+str(i),c) for i,c in enumerate([(.14,.27,.08),(.19,.36,.1),(.25,.42,.13)])]; wood=material('Thân gỗ',(.20,.13,.07)); pink=material('Hoa giấy',(.66,.12,.26))
col=bpy.data.collections.new('Khuôn viên và cổng');s.collection.children.link(col)
def move(o,n,m):
 o.name=n;o.data.materials.append(m)
 for c in list(o.users_collection): c.objects.unlink(o)
 col.objects.link(o);return o
def box(n,loc,dim,m):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.dimensions=dim;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);return move(o,n,m)
def sphere(n,loc,scale,m):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=8,location=loc);o=bpy.context.object;o.scale=scale;bpy.ops.object.shade_smooth();return move(o,n,m)
def cyl(n,loc,r,h,m):
 bpy.ops.mesh.primitive_cylinder_add(vertices=12,radius=r,depth=h,location=loc);return move(bpy.context.object,n,m)
def beam(n,a,b,r,m):
 a,b=Vector(a),Vector(b);d=b-a;o=cyl(n,(a+b)/2,r,d.length,m);o.rotation_euler=d.to_track_quat('Z','Y').to_euler()
# broad grounds and paved procession axis; scale and relative location provisional
box('Nền vườn',(0,-20,-.38),(78,70,.3),grass)
box('Đường chính',(0,-20,-.18),(9,43,.08),stone)
for x in (-18,18):
 box('Hồ cảnh',(x,-16,-.13),(19,15,.18),water)
 for yy in (-23.7,-8.3): box('Bờ hồ',(x,yy,.03),(19.8,.4,.35),ivory)
 for xx in (x-9.7,x+9.7): box('Bờ hồ',(xx,-16,.03),(.4,15,.35),ivory)
# tiled paved lines
for y in range(-39,0,2): box('Mạch lát sân',(0,y,-.12),(9,.025,.012),ivory)
# Gate gateway architecture, modelled as separate objects for revision.
y=-39
for x in (-4.6,4.6):
 box('Trụ cổng',(x,y,3),(1.35,1.6,6),ivory)
 for z in (.3,1,5,5.8):box('Chỉ ngang cổng',(x,y-.83,z),(1.55,.18,.13),ochre)
 for z in (1.6,2.5,3.4,4.3):box('Mảng gốm cổng',(x,y-.84,z),(.8,.06,.66),blue)
for z,w,h in [(6,10.7,.5),(6.65,11.2,.25),(7.15,9.6,.65),(7.65,10.2,.22),(9.65,7.0,.35),(10.0,7.6,.2)]:box('Tầng mái cổng',(0,y,z),(w,2,h),ochre if h<.5 else ivory)
for x in (-3,3):box('Trụ tầng trên cổng',(x,y,8.65),(.65,1.3,2.7),ivory)
for x in (-4.7,-3,3,4.7):
 cyl('Chóp cổng',(x,y,10.25),.11,.6,ochre);sphere('Châu cổng',(x,y,10.62),(.16,.16,.16),ochre)
# arch around central gate opening
for i in range(28):
 a=math.pi*i/28;b=math.pi*(i+1)/28
 beam('Vòm cổng',(3.8*math.cos(a),y-.84,3.0+2.5*math.sin(a)),(3.8*math.cos(b),y-.84,3.0+2.5*math.sin(b)),.12,ochre)
# garden trees with clustered foliage
for x in (-32,-27,-23,-12,12,23,27,32):
 for y in (-34,-27,-6,7):
  xx=x+random.uniform(-1,1);yy=y+random.uniform(-1,1);h=random.uniform(2.7,4.2)
  cyl('Thân cây',(xx,yy,h/2),.12,h,wood)
  for j in range(11):
   a=random.random()*math.tau;rad=random.uniform(.3,1.5);z=h+random.uniform(-.5,1.1)
   sphere('Tán lá',(xx+rad*math.cos(a),yy+rad*math.sin(a),z),(random.uniform(.5,1),random.uniform(.5,1),random.uniform(.4,.8)),random.choice(leaves))
for x in (-11,11):
 for y in (-30,-25,-20,-15,-10):
  sphere('Bụi hoa',(x,y,.6),(1,.8,.75),pink)
# scene camera overview
bpy.ops.object.camera_add(location=(53,-76,55));cam=bpy.context.object;cam.name='Tổng quan khuôn viên';cam.rotation_euler=(Vector((0,-12,1))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=95;s.camera=cam
s.render.resolution_x=1500;s.render.resolution_y=950;s.render.resolution_percentage=100;s.cycles.samples=20
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(p,'khuon-vien-vinh-trang.blend'))
bpy.ops.export_scene.gltf(filepath=os.path.join(p,'khuon-vien-vinh-trang.glb'),export_format='GLB')
s.render.filepath=os.path.join(p,'khuon-vien-vinh-trang.png');bpy.ops.render.render(write_still=True)
