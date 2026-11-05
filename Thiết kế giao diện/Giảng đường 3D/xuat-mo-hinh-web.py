import bpy,os
p='/Users/macos/Desktop/Chùa online/Thiết kế giao diện/Giảng đường 3D';bpy.ops.wm.open_mainfile(filepath=os.path.join(p,'giang-duong-co-canh-quan.blend'))
# Convert all static curves and apply bevels, then group meshes by material without altering the editable master.
for ob in list(bpy.context.scene.objects):
 if ob.type in {'CURVE','MESH'}:
  bpy.ops.object.select_all(action='DESELECT');ob.select_set(True);bpy.context.view_layer.objects.active=ob
  if ob.type=='CURVE':bpy.ops.object.convert(target='MESH')
  else:
   for mod in list(ob.modifiers):
    try:bpy.ops.object.modifier_apply(modifier=mod.name)
    except Exception as exc: print('MODIFIER_ERROR',ob.name,mod.name,str(exc))
groups={}
for ob in list(bpy.context.scene.objects):
 if ob.type=='MESH' and len(ob.data.materials)==1:
  key=ob.data.materials[0].name if ob.data.materials[0] else 'none';groups.setdefault(key,[]).append(ob)
for key,obs in groups.items():
 if len(obs)<2:continue
 bpy.ops.object.select_all(action='DESELECT')
 for ob in obs:ob.select_set(True)
 bpy.context.view_layer.objects.active=obs[0];bpy.ops.object.join();obs[0].name='Nhóm vật liệu '+key
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.context.scene.objects:
 if o.type=='MESH':o.select_set(True)
print('EXPORT_MESHES',len([o for o in bpy.context.scene.objects if o.type=='MESH']))
bpy.ops.export_scene.gltf(filepath=os.path.join(p,'giang-duong-web.glb'),export_format='GLB',use_selection=True)
