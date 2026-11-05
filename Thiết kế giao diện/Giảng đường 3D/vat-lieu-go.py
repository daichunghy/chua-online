import bpy,os
p='/Users/macos/Desktop/Chùa online/Thiết kế giao diện/Giảng đường 3D';bpy.ops.wm.open_mainfile(filepath=os.path.join(p,'giang-duong-co-canh-quan.blend'));s=bpy.context.scene
# Fine wood and terracotta surface shading remains in the editable Blender source.
for name in ('Gỗ cột nâu đỏ','Gỗ dầm','Gỗ sáng','Gỗ viền'):
 m=bpy.data.materials[name];nt=m.node_tree;n=nt.nodes;l=nt.links;b=n.get('Principled BSDF');base=tuple(b.inputs['Base Color'].default_value)
 coord=n.new('ShaderNodeTexCoord');coord.location=(-900,100)
 mapping=n.new('ShaderNodeMapping');mapping.vector_type='POINT';mapping.inputs['Scale'].default_value=(2.5,2.5,.25);mapping.location=(-700,100);l.new(coord.outputs['Generated'],mapping.inputs['Vector'])
 noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=10;noise.inputs['Detail'].default_value=3;noise.inputs['Roughness'].default_value=.68;noise.location=(-500,100);l.new(mapping.outputs['Vector'],noise.inputs['Vector'])
 ramp=n.new('ShaderNodeValToRGB');ramp.location=(-270,180);ramp.color_ramp.elements[0].position=.15;ramp.color_ramp.elements[0].color=tuple(min(1,x*.55) for x in base[:3])+(1,);ramp.color_ramp.elements[1].position=.88;ramp.color_ramp.elements[1].color=tuple(min(1,x*1.25) for x in base[:3])+(1,);l.new(noise.outputs['Fac'],ramp.inputs['Fac']);l.new(ramp.outputs['Color'],b.inputs['Base Color'])
 bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.12;bump.inputs['Distance'].default_value=.035;bump.location=(-100,-90);l.new(noise.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs['Normal'],b.inputs['Normal']);b.inputs['Roughness'].default_value=.55
for m in bpy.data.materials:
 if m.name.startswith('Gạch đất'):
  nt=m.node_tree;n=nt.nodes;l=nt.links;b=n.get('Principled BSDF');noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=90;noise.inputs['Detail'].default_value=2;bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.12;bump.inputs['Distance'].default_value=.012;l.new(noise.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs['Normal'],b.inputs['Normal']);b.inputs['Roughness'].default_value=.76
# Warm sunlight lifts shaded surfaces while preserving contrast.
for o in s.objects:
 if o.type=='LIGHT' and o.data.type=='AREA':o.data.energy*=1.45
s.cycles.samples=32
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(p,'giang-duong-vat-lieu.blend'))
s.render.filepath=os.path.join(p,'giang-duong-vat-lieu.png');bpy.ops.render.render(write_still=True)
