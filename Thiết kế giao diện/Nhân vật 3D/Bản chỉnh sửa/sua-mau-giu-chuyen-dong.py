import json, struct, numpy as np, os
root='/Users/macos/Desktop/Chùa online/Thiết kế giao diện/Nhân vật 3D';source=os.path.join(root,'Chuyển động','nu-chuyen-dong.glb');out=os.path.join(root,'Bản chỉnh sửa','nu-phuc-hoi-mau-chuyen-dong.glb')
b=bytearray(open(source,'rb').read());magic,ver,total,jsonlen,typ=struct.unpack_from('<4sIIII',b,0)
assert magic==b'glTF' and ver==2 and total==len(b) and typ==0x4e4f534a
j=json.loads(bytes(b[20:20+jsonlen])); start=20+jsonlen;binlen,bintype=struct.unpack_from('<II',b,start);assert bintype==0x004e4942;base=start+8
prim=j['meshes'][0]['primitives'][0]
def read(name,dtype,width):
 a=j['accessors'][prim['attributes'][name]];v=j['bufferViews'][a['bufferView']];assert v.get('buffer')==0 and not v.get('byteStride')
 arr=np.frombuffer(b,dtype=dtype,count=a['count']*width,offset=base+v.get('byteOffset',0)+a.get('byteOffset',0)).reshape(-1,width)
 return arr
pos=read('POSITION','<f4',3);joints=read('JOINTS_0','u1',4);weights=read('WEIGHTS_0','<f4',4);colors=read('COLOR_0','u1',4)
# glTF Y is height, Blender forward coordinate is -glTF Z.
z=pos[:,1];front=-pos[:,2];x=pos[:,0];cloth=np.array([96,87,100,255],dtype='u1');skin=np.array([198,124,85,255],dtype='u1')
dark=np.all(colors[:,:3]==[20,18,23],axis=1);stain=np.all(colors[:,:3]==[72,66,74],axis=1);gray=np.all(colors[:,:3]==cloth[:3],axis=1)
mask_pants=dark & (z>-.92) & (z<-.37);mask_stain=stain & (x>-.07) & (x<.15) & (z>.02) & (z<.52)
head_idx=next(i for i,node in enumerate(j['skins'][0]['joints']) if j['nodes'][node].get('name')=='Head')
headweight=np.sum(np.where(joints==head_idx,weights,0),axis=1);mask_face=gray & (headweight>=.75) & (z>.68) & (z<.88) & (front<.035) & (abs(x)<.12)
colors[mask_pants]=cloth;colors[mask_stain]=cloth;colors[mask_face]=skin
with open(out,'wb') as f:f.write(b)
print('VERTICES_CHANGED',{'pants':int(mask_pants.sum()),'shirt':int(mask_stain.sum()),'face':int(mask_face.sum())});print('OUT',out)
