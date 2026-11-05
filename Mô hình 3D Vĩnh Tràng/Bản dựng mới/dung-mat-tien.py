import bpy, math, os
from mathutils import Vector
out='/Users/macos/Desktop/Chùa online/Mô hình 3D Vĩnh Tràng/Bản dựng mới'
bpy.ops.wm.read_factory_settings(use_empty=True)
s=bpy.context.scene
s.render.engine='CYCLES'; s.cycles.samples=32
s.render.resolution_x=1500; s.render.resolution_y=850; s.render.resolution_percentage=100
s.world=bpy.data.worlds.new('Bầu trời'); s.world.color=(0.25,0.25,0.25)
def mat(n,c):
 m=bpy.data.materials.new(n); m.diffuse_color=(*c,1); m.use_nodes=True; m.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(*c,1); return m
cream=mat('Vàng kem',(0.83,0.61,0.30)); light=mat('Ngà sáng',(0.98,0.82,0.52)); white=mat('Trắng',(0.92,0.88,0.76)); red=mat('Đỏ gạch',(0.52,0.16,0.09)); gold=mat('Vàng trang trí',(0.83,0.51,0.08)); dark=mat('Cửa tối',(0.065,0.045,0.03)); blue=mat('Gốm xanh',(0.22,0.48,0.48)); stone=mat('Sân đá',(0.58,0.58,0.53)); green=mat('Cây xanh',(0.17,0.36,0.12)); pot=mat('Chậu đất',(0.48,0.20,0.12))
def box(n,loc,dim,m):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc); o=bpy.context.object;o.name=n;o.dimensions=dim;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(m);return o
def cyl(n,loc,r,depth,m):
 bpy.ops.mesh.primitive_cylinder_add(vertices=16,radius=r,depth=depth,location=loc);o=bpy.context.object;o.name=n;o.data.materials.append(m);return o
def ball(n,loc,scale,m):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=8,location=loc);o=bpy.context.object;o.name=n;o.scale=scale;o.data.materials.append(m);bpy.ops.object.shade_smooth();return o
def arch(x,z,w,h):
 # paired piers and segmented curved moulding on front plane
 for dx in (-w/2,w/2): box('Chân vòm', (x+dx,-1.76,z+h/2),(.12,.18,h),light)
 radius=w/2
 for i in range(24):
  a=math.pi*i/24;b=math.pi*(i+1)/24
  p=Vector((x+radius*math.cos(a),-1.77,z+h+radius*math.sin(a))); q=Vector((x+radius*math.cos(b),-1.77,z+h+radius*math.sin(b)))
  d=q-p; o=box('Chỉ vòm',(p+q)/2,(.11,.18,d.length),light);o.rotation_euler=d.to_track_quat('Z','Y').to_euler()
# mass, base and cornices
box('Sân', (0,-7,-.18),(38,22,.3),stone)
box('Nền chính điện',(0,1,.35),(29,8,.7),cream)
box('Khối kiến trúc',(0,1,3.2),(28,5,5.4),cream)
box('Viền mái dưới',(0,-.1,5.95),(28.8,5.4,.22),red)
box('Diềm gốm',(0,-.1,6.25),(28.8,5.4,.38),white)
box('Viền mái trên',(0,-.1,6.52),(29,5.4,.18),gold)
# blue ornamental tile course, separate pieces
for i in range(68):
 x=-13.6+i*.405
 box('Ô gốm xanh',(x,-2.83,6.25),(.25,.035,.23),blue)
 ball('Tâm gốm',(x,-2.86,6.25),(.045,.018,.045),white)
# columns, dark bays, arches
for i in range(13):
 x=-12+i*2
 box('Cửa vòm',(x,-1.54,2.72),(1.58,.12,3.6),dark)
 arch(x,.95,1.64,2.75)
 for dx in (-.45,0,.45): box('Song cửa',(x+dx,-1.64,2.55),(.035,.05,2.75),gold)
 for z in (1.35,2.15,2.95): box('Ngang cửa',(x,-1.66,z),(1.42,.05,.035),gold)
for i in range(14):
 x=-13+i*2
 cyl('Cột', (x,-2.05,2.95),.18,3.6,white)
 for z in (1.13,4.74): box('Đầu chân cột',(x,-2.05,z),(.55,.55,.22),red)
# parapet towers and central pediment
for x,w,h in [(-12,3.3,2.2),(12,3.3,2.2),(0,4.4,3.0)]:
 box('Tháp trang trí',(x,-.35,6.5+h/2),(w,2,h),cream)
 for z in (6.75,7.2,7.65):
  box('Chỉ trang trí tháp',(x,-1.39,z),(w+.12,.15,.12),white)
  box('Dải trang trí tháp',(x,-1.49,z+.18),(w-.35,.08,.13),blue)
 bpy.ops.mesh.primitive_cone_add(vertices=3,radius1=w*.61,depth=1.05,location=(x,-.35,6.5+h+.45),rotation=(0,0,math.pi/2));bpy.context.object.name='Mái tam giác';bpy.context.object.data.materials.append(red)
 for dx in (-w*.45,w*.45):
  cyl('Đỉnh tháp',(x+dx,-.45,6.5+h+.4),.09,.8,gold);ball('Châu',(x+dx,-.45,6.5+h+.85),(.17,.17,.17),gold)
# stairs central
for i in range(6): box('Bậc thềm',(0,-4.8+i*.37,.10+i*.13),(7.2,2.6,.16),white)
for x in (-4.2,4.2):
 box('Lan can',(x,-3.5,.85),(.25,2.6,.22),light)
 for y in (-4.4,-3.8,-3.2,-2.6): cyl('Trụ lan can',(x,y,.63),.09,.7,white)
# garden trees stylized
for x,y in [(-10,-6),(-6.8,-5.8),(6.8,-5.8),(10,-6)]:
 cyl('Chậu cây',(x,y,.22),.55,.4,pot);cyl('Thân cây',(x,y,1.05),.12,1.5,mat('Gỗ'+str(x),(0.3,0.18,0.08)))
 for z,r in [(1.45,.7),(1.85,.55),(2.18,.38)]: ball('Tán cây',(x,y,z),(r,r*.65,.25),green)
# camera
bpy.ops.object.camera_add(location=(0,-35,11));cam=bpy.context.object;cam.rotation_euler=(Vector((0,0,3.8))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=35;s.camera=cam
bpy.ops.object.light_add(type='AREA',location=(-5,-12,20));bpy.context.object.data.energy=2600;bpy.context.object.data.shape='DISK';bpy.context.object.data.size=18
bpy.ops.object.light_add(type='SUN',location=(0,0,15));bpy.context.object.rotation_euler=(.4,-.5,-.3);bpy.context.object.data.energy=2
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(out,'mat-tien-vinh-trang.blend'))
bpy.ops.export_scene.gltf(filepath=os.path.join(out,'mat-tien-vinh-trang.glb'),export_format='GLB')
s.render.filepath=os.path.join(out,'mat-tien-vinh-trang.png');bpy.ops.render.render(write_still=True)
