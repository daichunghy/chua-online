import bpy, math, os
from mathutils import Vector
root='/Users/macos/Desktop/Chùa online/Mô hình 3D Vĩnh Tràng/Bản dựng mới'
bpy.ops.wm.open_mainfile(filepath=os.path.join(root,'mat-tien-vinh-trang.blend'))
s=bpy.context.scene
# Replace the earlier schematic pediments with layered ornamental parapets.
for o in list(bpy.data.objects):
 if o.name.startswith(('Tháp trang trí','Chỉ trang trí tháp','Dải trang trí tháp','Mái tam giác','Đỉnh tháp','Châu')): bpy.data.objects.remove(o,do_unlink=True)
def mat(n,c,metal=0,rough=.58):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;b=m.node_tree.nodes.get('Principled BSDF');b.inputs['Base Color'].default_value=(*c,1);b.inputs['Metallic'].default_value=metal;b.inputs['Roughness'].default_value=rough;return m
cream=mat('Vữa màu vàng kem',(.91,.69,.37)); ivory=mat('Chỉ trắng ngà',(.95,.86,.67)); ochre=mat('Màu vàng đất',(.76,.43,.12)); red=mat('Đỏ son',(.51,.18,.10)); blue=mat('Men gốm xanh',(.23,.45,.43)); teal=mat('Men lam sẫm',(.08,.27,.27)); gold=mat('Hoa văn vàng',(.73,.42,.10),.35,.38)
def box(n,loc,dim,m,bev=0):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(m)
 if bev:
  b=o.modifiers.new('Cạnh bo nhẹ','BEVEL');b.width=bev;b.segments=2
 return o
def sphere(n,loc,r,m):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=8,radius=r,location=loc);o=bpy.context.object;o.name=n;o.data.materials.append(m);bpy.ops.object.shade_smooth();return o
def cyl(n,loc,r,h,m):
 bpy.ops.mesh.primitive_cylinder_add(vertices=16,radius=r,depth=h,location=loc);o=bpy.context.object;o.name=n;o.data.materials.append(m);return o
def path(n,pts,r,m):
 c=bpy.data.curves.new(n,'CURVE');c.dimensions='3D';c.resolution_u=2;c.bevel_depth=r;c.bevel_resolution=2;sp=c.splines.new('POLY');sp.points.add(len(pts)-1)
 for p,co in zip(sp.points,pts):p.co=(*co,1)
 o=bpy.data.objects.new(n,c);s.collection.objects.link(o);o.data.materials.append(m);return o
def scroll(x,y,z,scale,sgn=1):
 pts=[]
 for i in range(38):
  t=i/37;ang=t*math.pi*3.5;rad=scale*(.05+.35*t);pts.append((x+sgn*rad*math.cos(ang),y,z+rad*math.sin(ang)+t*scale*.17))
 path('Hoa văn cuộn',pts,.035*scale,gold)
def ceramic_band(x,y,z,w,h):
 box('Nền ô khảm',(x,y,z),(w,.10,h),ivory)
 count=max(1,round(w/.34))
 for i in range(count):
  xx=x-w/2+(i+.5)*w/count
  box('Ô gốm',(xx,y-.065,z),(.245,.04,h*.72),blue)
  # raised central ceramic flower motif
  sphere('Tâm bông gốm',(xx,y-.10,z),.045,ivory)
def pier(x,y,z,h):
 box('Trụ chóp',(x,y,z+h/2),(.29,.38,h),cream,.02)
 for zz in (z+.1,z+h-.08):box('Gờ đầu trụ',(x,y-.015,zz),(.42,.46,.10),ivory,.01)
 cyl('Chân bảo châu',(x,y,z+h+.05),.12,.12,gold);sphere('Bảo châu',(x,y,z+h+.22),.14,gold)
def parapet(x,w,base,h):
 y=-1.84
 box('Thân ô mái',(x,y,base+h/2),(w,.38,h),cream)
 box('Đế ô mái',(x,y-.08,base+.09),(w+.24,.52,.18),ivory)
 ceramic_band(x,y-.24,base+.35,w-.4,.22)
 box('Chỉ trên ô mái',(x,y-.08,base+h-.08),(w+.18,.52,.14),ivory)
 for px in (x-w/2+.12,x+w/2-.12):pier(px,y-.1,base,h+.12)
 # broad curved flanking scrolls framing the inset medallion
 for k in (-1,1):scroll(x+k*w*.29,y-.33,base+h+.08,.70,k)
 box('Nền huy hiệu',(x,y-.26,base+h+.25),(w*.32,.16,.52),ivory)
 box('Ô huy hiệu',(x,y-.37,base+h+.25),(w*.25,.05,.40),blue)
 for px in (x-w*.09,x,x+w*.09):sphere('Hoa gốm huy hiệu',(px,y-.41,base+h+.25),.055,gold)
# Layered roofline: corner masses, secondary flanks and raised central pediment.
for x,w,h in [(-12,3.45,1.08),(12,3.45,1.08),(-5.8,3.2,.62),(5.8,3.2,.62),(0,5.0,1.38)]:parapet(x,w,6.62,h)
# upper tier on the central ridge
parapet(0,2.9,8.05,.95)
# front-facing triangular gable inset
verts=[(-1.72,-2.14,9.0),(1.72,-2.14,9.0),(0,-2.14,10.15),(-1.72,-1.76,9.0),(1.72,-1.76,9.0),(0,-1.76,10.15)]
mesh=bpy.data.meshes.new('Mái tam giác');mesh.from_pydata(verts,[],[(0,1,2),(3,5,4),(0,3,4,1),(1,4,5,2),(2,5,3,0)]);mesh.update();o=bpy.data.objects.new('Mái tam giác trung tâm',mesh);s.collection.objects.link(o);o.data.materials.append(red)
path('Chỉ mái giữa',[(-1.76,-2.20,9.02),(0,-2.20,10.20),(1.76,-2.20,9.02)],.065,ivory)
scroll(-.48,-2.25,9.23,.55,-1);scroll(.48,-2.25,9.23,.55,1)
pier(0,-2.03,10.05,.30)
# Intermediate ornamental finials along the parapet.
for x in (-10,-8.8,-4,-3,3,4,8.8,10):pier(x,-1.88,6.61,.36)
# Additional coloured panels on the front face of each pier and layered arch mouldings.
for i in range(14):
 x=-13+i*2
 box('Bảng gốm trụ',(x,-2.245,3.0),(.18,.05,2.85),blue)
 for z in (1.65,2.05,2.45,2.85,3.25,3.65,4.05): sphere('Hoa gốm trụ',(x,-2.29,z),.042,ivory)
for i in range(13):
 x=-12+i*2;z=3.70;r=.83
 for radius,thick,ma in ((.89,.06,red),(.97,.045,ochre)):
  pts=[]
  for j in range(33):
   a=math.pi*j/32;pts.append((x+radius*math.cos(a),-1.90,z+radius*math.sin(a)))
  path('Chỉ cuốn vòm',pts,thick,ma)
# Connect roof to a building with depth, whose pitch and colour follow reference photography.
for y in (.7,2.2,3.7):
 roofverts=[(-13.3,y-.72,5.84),(13.3,y-.72,5.84),(-13.3,y,6.8),(13.3,y,6.8),(-13.3,y+.72,5.84),(13.3,y+.72,5.84)]
 me=bpy.data.meshes.new('Ngói dốc');me.from_pydata(roofverts,[],[(0,1,3,2),(2,3,5,4)]);me.update();ob=bpy.data.objects.new('Mái ngói phía sau',me);s.collection.objects.link(ob);ob.data.materials.append(red)
 for j in range(32):
  xx=-13.2+j*.85;path('Luống ngói',[(xx,y-.72,5.87),(xx,y,6.82),(xx,y+.72,5.87)],.018,ochre)
# Camera and a brighter environment suitable for comparing colours.
s.world.color=(.38,.38,.38);s.cycles.samples=24;s.render.resolution_x=1800;s.render.resolution_y=1000;s.render.resolution_percentage=100
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(root,'chanh-dien-chi-tiet.blend'))
bpy.ops.export_scene.gltf(filepath=os.path.join(root,'chanh-dien-chi-tiet.glb'),export_format='GLB')
s.render.filepath=os.path.join(root,'chanh-dien-chi-tiet.png');bpy.ops.render.render(write_still=True)
