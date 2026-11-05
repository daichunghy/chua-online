import bpy,math,os
from mathutils import Vector
p='/Users/macos/Desktop/Chùa online/Thiết kế giao diện/Vật phẩm 3D/Bản chỉnh sửa'
tex='/Users/macos/Desktop/Chùa online/Thiết kế giao diện/Vật phẩm 3D/models/tui_vai_theu_sen_pbr.png'
bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene;s.world=bpy.data.worlds.new('World');s.world.color=(.25,.25,.25)
s.render.engine='CYCLES';s.cycles.samples=24;s.render.resolution_x=900;s.render.resolution_y=1050;s.render.resolution_percentage=100
cloth=bpy.data.materials.new('Vải canvas');cloth.diffuse_color=(.78,.70,.58,1);cloth.use_nodes=True
b=cloth.node_tree.nodes.get('Principled BSDF');b.inputs['Base Color'].default_value=(.78,.70,.58,1);b.inputs['Roughness'].default_value=.88
noise=cloth.node_tree.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=420;noise.inputs['Detail'].default_value=2
bump=cloth.node_tree.nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.13;bump.inputs['Distance'].default_value=.00008;cloth.node_tree.links.new(noise.outputs['Fac'],bump.inputs['Height']);cloth.node_tree.links.new(bump.outputs['Normal'],b.inputs['Normal'])
printmat=bpy.data.materials.new('Mặt túi hoa sen');printmat.use_nodes=True;b=printmat.node_tree.nodes.get('Principled BSDF');b.inputs['Roughness'].default_value=.88
im=printmat.node_tree.nodes.new('ShaderNodeTexImage');im.image=bpy.data.images.load(tex);im.image.pack();printmat.node_tree.links.new(im.outputs['Color'],b.inputs['Base Color'])
# A front and a back panel with softly swollen surface, continuous quads and UVs.
W=.36;H=.38; nx=24;nz=28
for front in (True,False):
 vs=[];fs=[]
 for j in range(nz+1):
  z=H*j/nz; hwidth=W*.5*(.95+.05*math.sin(math.pi*j/nz));
  for i in range(nx+1):
   u=i/nx;x=(2*u-1)*hwidth
   depth=.038+.012*math.sin(math.pi*j/nz)*(1-(2*u-1)**2)
   vs.append((x,-depth if front else depth,z))
 for j in range(nz):
  for i in range(nx):
   a=j*(nx+1)+i;fs.append((a,a+1,a+nx+2,a+nx+1) if front else (a+1,a,a+nx+1,a+nx+2))
 mesh=bpy.data.meshes.new('Mặt vải');mesh.from_pydata(vs,[],fs);mesh.update();o=bpy.data.objects.new('Mặt trước' if front else 'Mặt sau',mesh);s.collection.objects.link(o);o.data.materials.append(printmat if front else cloth)
 if front:
  uv=mesh.uv_layers.new(name='UVMap')
  for poly in mesh.polygons:
   for l in poly.loop_indices:
    vi=mesh.loops[l].vertex_index; u=vi%(nx+1)/nx;v=vi//(nx+1)/nz
    uv.data[l].uv=(.02+.46*u,.52+.45*v)
 for f in mesh.polygons:f.use_smooth=True
 sol=o.modifiers.new('Độ dày vải','SOLIDIFY');sol.thickness=.0015
# Side gussets and bottom, separately plain cloth
for side in (-1,1):
 vs=[];fs=[]
 for j in range(nz+1):
  z=H*j/nz;hw=W*.5*(.95+.05*math.sin(math.pi*j/nz))
  for i in range(9):
   t=i/8;vs.append((side*(hw-.002*math.sin(math.pi*t)),(-.038+.076*t),z))
 for j in range(nz):
  for i in range(8):a=j*9+i;fs.append((a,a+1,a+10,a+9))
 me=bpy.data.meshes.new('Hông túi');me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new('Hông túi',me);s.collection.objects.link(o);o.data.materials.append(cloth)
 for f in me.polygons:f.use_smooth=True
 sol=o.modifiers.new('Độ dày','SOLIDIFY');sol.thickness=.0015
# rounded arch strap band along a smooth analytic path, one front and one back
for y in (-.042,.042):
 N=64;verts=[];faces=[]
 for i in range(N+1):
  t=i/N; x=-.088+.176*t;z=.35+.205*(math.sin(math.pi*t)**.78);dx=.176;dz=.205*.78*math.pi*math.cos(math.pi*t)*(max(.003,math.sin(math.pi*t))**(-.22));norm=Vector((-dz,0,dx)).normalized();c=Vector((x,y,z));v1=c-norm*.012;v2=c+norm*.012;verts.extend([v1,v2])
 for i in range(N):faces.append((2*i,2*i+1,2*i+3,2*i+2))
 me=bpy.data.meshes.new('Quai vải');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Quai trước' if y<0 else 'Quai sau',me);s.collection.objects.link(o);o.data.materials.append(cloth)
 for f in me.polygons:f.use_smooth=True
 solid=o.modifiers.new('Độ dày quai','SOLIDIFY');solid.thickness=.002
 bevel=o.modifiers.new('Bo mép quai','BEVEL');bevel.width=.001;bevel.segments=2
# Close the base so that the bottom does not appear hollow from below.
bpy.ops.mesh.primitive_cube_add(size=1,location=(0,0,.002));o=bpy.context.object;o.name='Đáy túi';o.dimensions=(.342,.078,.004);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(cloth);bevel=o.modifiers.new('Bo mép đáy','BEVEL');bevel.width=.002;bevel.segments=2
# top edge hem and understated seam lines
for y in (-.040,.040):
 bpy.ops.mesh.primitive_cube_add(size=1,location=(0,y,.366));o=bpy.context.object;o.name='Nẹp miệng túi';o.dimensions=(.34,.003,.018);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(cloth);mod=o.modifiers.new('Bo mép','BEVEL');mod.width=.002;mod.segments=2
# lighting and camera kept out of export.
bpy.ops.object.camera_add(location=(.75,-1.8,.82));cam=bpy.context.object;cam.rotation_euler=(Vector((0,0,.26))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=.72;s.camera=cam
bpy.ops.object.light_add(type='AREA',location=(-.8,-1.1,1.6));bpy.context.object.data.energy=150;bpy.context.object.data.size=1.5
bpy.ops.object.light_add(type='AREA',location=(.8,.2,1));bpy.context.object.data.energy=60;bpy.context.object.data.size=1
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(p,'tui-vai-sen.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if o.type=='MESH':o.select_set(True)
bpy.ops.export_scene.gltf(filepath=os.path.join(p,'tui-vai-sen.glb'),export_format='GLB',use_selection=True)
s.render.film_transparent=True;s.render.filepath=os.path.join(p,'tui-vai-sen.png');bpy.ops.render.render(write_still=True)
