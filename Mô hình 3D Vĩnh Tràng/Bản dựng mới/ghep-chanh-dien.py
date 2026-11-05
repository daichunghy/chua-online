import bpy, math, os, random
from mathutils import Vector
p='/Users/macos/Desktop/Chùa online/Mô hình 3D Vĩnh Tràng/Bản dựng mới'
bpy.ops.wm.open_mainfile(filepath=os.path.join(p,'chanh-dien-cua-vom.blend'))
s=bpy.context.scene;random.seed(43)
# Align relative masses to the reference aerial, retaining the existing building as an editable assembly.
for o in list(bpy.data.objects):
 if o.type in {'MESH','CURVE'}:
  if o.name=='Sân': bpy.data.objects.remove(o,do_unlink=True)
  else: o.location.x+=23
for o in list(bpy.data.objects):
 if o.type=='CAMERA': bpy.data.objects.remove(o,do_unlink=True)
def mat(n,c):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(*c,1);return m
stone=mat('Nền xám sáng',(.46,.45,.41));grass=mat('Cây nền',(.23,.32,.13));red=mat('Mái ngói',(.51,.18,.10));yellow=mat('Vàng tường',(.83,.58,.28));ivory=mat('Gờ ngà',(.86,.76,.55));dark=mat('Ô cửa',(.19,.12,.07));tree=mat('Lá',(.15,.29,.09));trunk=mat('Thân gỗ',(.23,.14,.075))
def box(n,loc,dim,m):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(m);return o
def ball(n,loc,scale,m):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=8,location=loc);o=bpy.context.object;o.name=n;o.scale=scale;o.data.materials.append(m);bpy.ops.object.shade_smooth();return o
def cyl(n,loc,r,h,m):
 bpy.ops.mesh.primitive_cylinder_add(vertices=16,radius=r,depth=h,location=loc);o=bpy.context.object;o.name=n;o.data.materials.append(m);return o
def roof(n,x,y,z,w,d,h):
 mesh=bpy.data.meshes.new(n);mesh.from_pydata([(x-w/2,y-d/2,z),(x+w/2,y-d/2,z),(x+w/2,y+d/2,z),(x-w/2,y+d/2,z),(x,y,z+h)],[],[(0,1,4),(1,2,4),(2,3,4),(3,0,4),(3,2,1,0)]);o=bpy.data.objects.new(n,mesh);s.collection.objects.link(o);o.data.materials.append(red)
box('Nền khuôn viên',(0,12,-.38),(105,125,.4),grass)
box('Sân hành lang dọc',(-.5,10,-.14),(18,102,.15),stone)
box('Sân trước chính điện',(23,-11,-.12),(32,23,.16),stone)
# front-left pedestal for the Di Lac area; statue remains to be sculpted separately
box('Bệ khu tượng Di Lặc',(-24,-1,.85),(22,20,1.7),yellow)
box('Sân trước khu Di Lặc',(-24,-16,.08),(23,12,.25),stone)
for i in range(5):box('Bậc tam cấp Di Lặc',(-24,-22+i*.55,.10+i*.18),(9,3,.2),ivory)
# pagoda at the rear of central walk, as shown in the aerial reference
x,y=-12,43
box('Nền tháp',(x,y,.7),(13,12,1.4),yellow)
for level in range(7):
 z=1.4+level*3.15;w=9.2-level*.35;d=8.0-level*.30
 box('Tầng tháp %d'%level,(x,y,z+1.2),(w-1,d-1,2.4),yellow)
 for side in (-1,1):
  box('Cửa tầng tháp',(x+side*(w*.25),y-d/2+.43,z+1.1),(1.0,.08,1.55),dark)
  box('Trụ tầng tháp',(x+side*(w*.42),y-d/2+.38,z+1.2),(.25,.25,2.4),ivory)
 box('Diềm mái tầng tháp',(x,y,z+2.45),(w,d,.18),ivory);roof('Mái tháp',x,y,z+2.55,w,d,.85)
cyl('Đỉnh tháp',(x,y,24),.25,2.2,red)
# reclining statue site is at back right of pagoda; base only until a faithful statue exists
box('Bệ khu tượng nằm',(12,47,1.4),(24,10,2.8),yellow)
box('Viền bệ tượng nằm',(12,47,2.87),(24.4,10.4,.18),ivory)
# modest garden structure, spaced rows along central avenue
for xx in (-8,8):
 for yy in range(-30,44,7):
  box('Bồn cây',(xx,yy,.25),(1.5,1.5,.5),yellow);cyl('Thân cây',(xx,yy,1.0),.12,1.4,trunk)
  for j in range(5):
   a=j*math.tau/5;ball('Tán cây',(xx+.45*math.cos(a),yy+.45*math.sin(a),1.9),( .55,.5,.45),tree)
for xx in (-43,42):
 for yy in range(-38,60,10):
  cyl('Thân cây nền',(xx,yy,2.2),.16,4.3,trunk)
  for j in range(8):
   a=j*math.tau/8;ball('Lá nền',(xx+.8*math.cos(a),yy+.8*math.sin(a),4.5+random.uniform(-.2,.7)),(.9,.8,.8),tree)
# overall angle comparable to reference image
bpy.ops.object.camera_add(location=(-72,-100,83));cam=bpy.context.object;cam.name='Góc tổng quan';cam.rotation_euler=(Vector((0,15,4))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=125;s.camera=cam
s.cycles.samples=16;s.render.resolution_x=1500;s.render.resolution_y=900;s.render.resolution_percentage=100
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(p,'khuon-vien-chanh-dien-moi.blend'))
bpy.ops.export_scene.gltf(filepath=os.path.join(p,'khuon-vien-chanh-dien-moi.glb'),export_format='GLB')
s.render.filepath=os.path.join(p,'khuon-vien-chanh-dien-moi.png');bpy.ops.render.render(write_still=True)
