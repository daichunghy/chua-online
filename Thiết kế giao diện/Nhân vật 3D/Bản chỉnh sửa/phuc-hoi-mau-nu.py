import bpy,os
from mathutils import Vector
root='/Users/macos/Desktop/Chùa online/Thiết kế giao diện/Nhân vật 3D';out=os.path.join(root,'Bản chỉnh sửa')
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=os.path.join(root,'Chuyển động/nu-chuyen-dong.glb'))
body=bpy.data.objects['geometry_0'];arm=bpy.data.objects['world'];attr=body.data.color_attributes['Color'];mesh=body.data
group=body.vertex_groups['Head'].index
weights={v.index:next((g.weight for g in v.groups if g.group==group),0.0) for v in mesh.vertices}
counts={'quan':0,'vet_ao':0,'mat':0}
# Colors are existing linear vertex colors from the source. Avoid repainting hair, cuffs, or bone weights.
cloth=(.376,.342,.392,1);skin=(.776,.485,.332,1)
def near(c,target):return max(abs(c[i]-target[i]) for i in range(3))<.004
for poly in mesh.polygons:
 for li in poly.loop_indices:
  vi=mesh.loops[li].vertex_index;v=mesh.vertices[vi];c=attr.data[li].color;p=body.matrix_world@v.co
  if near(c,(.078,.070,.091)) and -.92<p.z<-.37:
   attr.data[li].color=cloth;counts['quan']+=1
  elif near(c,(.283,.258,.292)) and -.07<p.x<.15 and .02<p.z<.52:
   attr.data[li].color=cloth;counts['vet_ao']+=1
  elif weights[vi]>=.75 and near(c,cloth) and .68<p.z<.88 and p.y<.035 and abs(p.x)<.12:
   attr.data[li].color=skin;counts['mat']+=1
print('LOOPS_REPAINTED',counts)
# Keep a Blender source and export only the body and its original armature/actions.
arm.animation_data.action=bpy.data.actions['Dung'];bpy.context.scene.frame_set(0)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(out,'nu-phuc-hoi-mau.blend'))
bpy.ops.object.select_all(action='DESELECT');body.select_set(True);arm.select_set(True);bpy.context.view_layer.objects.active=arm
bpy.ops.export_scene.gltf(filepath=os.path.join(out,'nu-phuc-hoi-mau.glb'),export_format='GLB',use_selection=True,export_animation_mode='ACTIONS',export_animations=True)
# Render a reference pose.
s=bpy.context.scene;s.world=bpy.data.worlds.new('World') if not s.world else s.world;s.world.color=(.25,.25,.25);s.render.engine='CYCLES';s.cycles.samples=16;s.render.resolution_x=700;s.render.resolution_y=1000;s.render.resolution_percentage=100
bpy.ops.object.light_add(type='AREA',location=(0,-3,3));bpy.context.object.data.energy=350;bpy.context.object.data.size=4
bpy.ops.object.camera_add(location=(0,-4,.1));o=bpy.context.object;o.rotation_euler=(Vector((0,0,0))-o.location).to_track_quat('-Z','Y').to_euler();o.data.type='ORTHO';o.data.ortho_scale=2.35;s.camera=o;s.render.film_transparent=True;s.render.filepath=os.path.join(out,'nu-phuc-hoi-mau.png');bpy.ops.render.render(write_still=True)
