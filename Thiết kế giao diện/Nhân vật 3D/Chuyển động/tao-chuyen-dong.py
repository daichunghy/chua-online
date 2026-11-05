"""Bind the three Hunyuan meshes and bake stand / walk cycles into glTF."""
import json, math as m, struct as st
from pathlib import Path

HERE = Path(__file__).resolve().parent
def smooth(a,b,x):
    t=max(0,min(1,(x-a)/(b-a)))
    return t*t*(3-2*t)

def pt_seg_dist(px, py, x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    L2 = dx*dx + dy*dy
    if L2 < 1e-6: return m.hypot(px - x1, py - y1)
    t = max(0.0, min(1.0, ((px - x1)*dx + (py - y1)*dy) / L2))
    return m.hypot(px - (x1 + t*dx), py - (y1 + t*dy))

def bake(name, shoulder, head, wrist, hip):
    raw=(HERE.parent/'Hunyuan3D'/f'{name}-chua-co-mau.glb').read_bytes()
    size=st.unpack_from('<I',raw,12)[0]
    g=json.loads(raw[20:20+size])
    buf=bytearray(raw[28+size:])
    prim=g['meshes'][0]['primitives'][0]
    pos=g['accessors'][prim['attributes']['POSITION']]
    offset=g['bufferViews'][pos['bufferView']].get('byteOffset',0)
    raw_verts=list(st.iter_unpack('<fff',buf[offset:offset+12*pos['count']]))
    verts=[]
    for i,(x,y,z) in enumerate(raw_verts):
        if abs(x)<0.020 and 0.08<y<0.46 and z>0.142:
            z=0.145
            st.pack_into('<fff',buf,offset+12*i,x,y,z)
        verts.append((x,y,z))
    def acc(data,fmt,ctype,typ,target=None,limits=False):
        data=list(data)
        while len(buf)%4: buf.append(0)
        start=len(buf)
        for row in data: buf.extend(st.pack('<'+fmt,*row))
        view={'buffer':0,'byteOffset':start,'byteLength':len(buf)-start}
        if target: view['target']=target
        a={'bufferView':len(g['bufferViews']),'componentType':ctype,'count':len(data),'type':typ}
        if limits: a.update(min=[min(r[0] for r in data)],max=[max(r[0] for r in data)])
        g['bufferViews'].append(view); g['accessors'].append(a)
        return len(g['accessors'])-1
    bones=[]; g['nodes'][1]['skin']=0
    def bone(label,p,xyz):
        idx=len(g['nodes']); xyz=tuple(xyz)
        prev=bones[p][1] if p is not None else (0,0,0)
        local=[a-b for a,b in zip(xyz,prev)]
        g['nodes'].append(dict(name=label,translation=local))
        parent=bones[p][0] if p is not None else 0
        g['nodes'][parent].setdefault('children',[]).append(idx)
        bones.append((idx,xyz,local)); return len(bones)-1
    pelvis=bone('Pelvis',None,(0,hip,0))
    spine=bone('Spine',pelvis,(0,.20,-.025))
    skull=bone('Head',spine,(0,head,-.025))
    legs=[]; arms=[]
    for s in (1,-1):
        k='L' if s==1 else 'R'
        h=bone(k+' thigh',pelvis,(s*.123,hip,-.025))
        kn=bone(k+' shin',h,(s*.123,-.51,-.019))
        foot=bone(k+' foot',kn,(s*.123,-.904,-.062))
        legs.append((h,kn,foot))
        u=bone(k+' upper arm',spine,(s*shoulder,head-.135,-.035))
        e=bone(k+' forearm',u,(s*(shoulder+.095),.22 if name!='tre-em' else .16,-.006))
        w=bone(k+' hand',e,(s*.392,wrist,.025))
        arms.append((u,e,w))
    weights=[]; joints=[]
    for x,y,z in verts:
        side=int(x<0); ax=abs(x); h,k,f=legs[side]; u,e,w=arms[side]
        arm=smooth(.247,.314,ax+max(0,.31-y)*.06)*(1-smooth(head-.13,head-.035,y))*smooth(-.28,-.21,y)
        leg=(1-smooth(hip-.12,hip+.06,y))*(1-arm)
        shin=1-smooth(-.61,-.42,y); foot=1-smooth(-.94,-.85,y)
        fore=1-smooth(.12,.33,y); hand=1-smooth(wrist-.022,wrist+.05,y)
        body=1-arm-leg
        chest=smooth(hip,.30,y); face=smooth(head-.035,head+.055,y)
        pairs=[(h,leg*(1-shin)),(k,leg*shin*(1-foot)),(f,leg*shin*foot),
               (u,arm*(1-fore)),(e,arm*fore*(1-hand)),(w,arm*fore*hand),
               (pelvis,body*(1-chest)),(spine,body*chest*(1-face)),(skull,body*chest*face)]
        top=sorted(pairs,key=lambda q:q[1],reverse=True)[:4]
        total=sum(v for _,v in top)
        joints.append(tuple(i for i,_ in top)); weights.append(tuple(v/total for _,v in top))
    prim['attributes'].update(JOINTS_0=acc(joints,'4B',5121,'VEC4',34962),WEIGHTS_0=acc(weights,'4f',5126,'VEC4',34962))
    # Bảng màu chuẩn Phật giáo Việt Nam (khớp ảnh tham khảo Áo Lam & Túi Vải Sen)
    palettes = {
        'nam': ((115, 82, 65), (78, 56, 45)), # Áo nâu sồng, quần nâu đậm
        'nu': ((165, 158, 168), (80, 75, 84)), # Áo lam khói thanh nhã, quần tối màu
        'tre-em': ((158, 145, 155), (92, 85, 90)) # Áo lam nhạt trẻ em
    }
    shirt, pants = palettes[name]
    skin = (228, 185, 156) # Màu da ấm mịn màng
    hair = (36, 28, 24) # Tóc đen tuyền tự nhiên
    shoes = (218, 208, 195) # Giày vải be mộc
    
    colors = []
    for x, y, z in verts:
        d_lhand = m.hypot(x - shoulder - 0.188, y - wrist, z - 0.025)
        d_rhand = m.hypot(x + shoulder + 0.188, y - wrist, z - 0.025)
        d_bun = m.hypot(x, y - (head + 0.05), z - (-0.11))
        
        # Bàn tay sạch (không lem vào tay áo)
        is_hand = min(d_lhand, d_rhand) < 0.095 and abs(x) > 0.31 and y < wrist + 0.015
        
        # Đường viền chân tóc tự nhiên cong theo trán và thái dương
        hairline_y = head + 0.165 + 0.022 * max(0.0, 1.0 - (abs(x) / 0.065) ** 2)
        is_hair = (y > hairline_y and (z < 0.020 or y > head + 0.22)) or (y > head + 0.05 and z < -0.040) or (d_bun < 0.085)
        
        # Khuôn mặt (giới hạn chiều ngang quai hàm abs(x) < 0.070)
        is_face = (y >= head - 0.02 and y <= head + 0.22 and z >= -0.040 and abs(x) < 0.070 and not is_hair)
        
        # Cổ (chỉ ở trung tâm họng, không lem sang vai và xương quai xanh)
        is_neck = (y >= head - 0.12 and y < head - 0.02 and abs(x) < 0.042 and abs(z) < 0.055)
        
        # Đường nẹp cổ chéo vạt Áo Tràng Phật Tử (Y-cross collar)
        d_main_collar = pt_seg_dist(x, y, -0.065, head - 0.14, 0.130, 0.02)
        d_sub_collar = pt_seg_dist(x, y, 0.065, head - 0.14, -0.035, 0.32)
        is_collar_line = (z > 0.12 and y > 0.02 and (d_main_collar < 0.014 or (d_sub_collar < 0.014 and y > 0.30)))
        collar_color = tuple(max(0, int(c * 0.88)) for c in shirt)
        
        if is_hair:
            rgb = hair
        elif is_hand or is_face or is_neck:
            rgb = skin
        elif is_collar_line:
            rgb = collar_color
        elif y < -.916:
            rgb = shoes
        elif y > -0.38:
            rgb = shirt
        else:
            rgb = pants
            
        colors.append(tuple(round(255 * ((c / 255 + 0.055) / 1.055) ** 2.4) for c in rgb) + (255,))
    color = acc(colors, '4B', 5121, 'VEC4', 34962)
    g['accessors'][color]['normalized'] = True
    prim['attributes']['COLOR_0'] = color
    g['skins']=[dict(joints=[n for n,_,_ in bones],skeleton=bones[0][0],inverseBindMatrices=acc(
        [(1,0,0,0,0,1,0,0,0,0,1,0,-x,-y,-z,1) for _,(x,y,z),_ in bones],'16f',5126,'MAT4'))]
    def quat(a,axis=0):
        q=[0.,0.,0.,m.cos(a/2)];q[axis]=m.sin(a/2);return q
    def clip(label,duration,count,walking,stairs=0):
        animation=dict(name=label,channels=[],samplers=[])
        g.setdefault('animations',[]).append(animation)
        clock=acc([(duration*i/count,) for i in range(count+1)],'f',5126,'SCALAR',limits=True)
        def track(b,path,rows):
            size=len(rows[0])
            animation['channels'].append(dict(sampler=len(animation['samplers']),target=dict(node=bones[b][0],path=path)))
            animation['samplers'].append(dict(input=clock,output=acc(rows,f'{size}f',5126,f'VEC{size}')))
        tracks={}
        for i in range(count+1):
            p=i/count; cyc=2*m.pi*p
            drop=(-.046+.008*m.cos(cyc*2)) if walking else .003*m.sin(cyc)
            tracks.setdefault((pelvis,'translation'),[]).append((.012*m.sin(cyc) if walking else 0,hip+drop,0))
            tracks.setdefault((spine,'rotation'),[]).append(quat(.055*m.sin(cyc) if walking else .012*m.sin(cyc),1))
            tracks.setdefault((skull,'rotation'),[]).append(quat(-.03*m.sin(cyc) if walking else 0,1))
            for side,((h,k,f),(u,e,w)) in enumerate(zip(legs,arms)):
                phase=(p+side*.5)%1; swing=0
                if phase<.60: forward=.225*(1-2*phase/.60)
                else:
                    t=(phase-.60)/.40
                    forward=.225*(2*smooth(0,1,t)-1)
                    swing=(.105+(.13 if stairs else 0))*m.sin(m.pi*t)**2
                a1=a2=0
                if walking:
                    y1,z1=bones[k][2][1:]; y2,z2=bones[f][2][1:]
                    L1,L2=m.hypot(y1,z1),m.hypot(y2,z2)
                    y,z=y1+y2+swing-drop+stairs*.22*forward,z1+z2+forward
                    d=min(m.hypot(y,z),L1+L2-.001)
                    ang=m.atan2(z,-y)
                    upper=ang+m.acos(max(-1,min(1,(L1*L1+d*d-L2*L2)/(2*L1*d))))
                    lower=ang-m.acos(max(-1,min(1,(L2*L2+d*d-L1*L1)/(2*L2*d))))
                    a1=m.atan2(z1,-y1)-upper
                    a2=m.atan2(z2,-y2)-lower-a1
                values=[(h,quat(a1)),(k,quat(a2)),(f,quat(-a1-a2)),
                        (u,quat((.23 if walking else .025)*m.cos(cyc+side*m.pi))),
                        (e,quat(-.12 if walking else -.04))]
                for b,q in values: tracks.setdefault((b,'rotation'),[]).append(q)
        for (b,path),rows in tracks.items():track(b,path,rows)
    clip('Dung',2.8,48,False);clip('Di bo',1.24,48,True)
    clip('Lên cầu thang',1.40,48,True,1)
    clip('Xuống cầu thang',1.40,48,True,-1)
    def gesture(label,duration,kneel=False,bow=False,incense=False):
        animation=dict(name=label,channels=[],samplers=[])
        g['animations'].append(animation)
        times=[0,.18,.36,.54,.77,1]
        clock=acc([(duration*t,) for t in times],'f',5126,'SCALAR',limits=True)
        def add(b,path,rows):
            n=len(rows[0])
            animation['channels'].append(dict(sampler=len(animation['samplers']),target=dict(node=bones[b][0],path=path)))
            animation['samplers'].append(dict(input=clock,output=acc(rows,f'{n}f',5126,f'VEC{n}')))
        def combine(x,z):
            a,b=x/2,z/2
            return [m.sin(a)*m.cos(b),-m.sin(a)*m.sin(b),m.cos(a)*m.sin(b),m.cos(a)*m.cos(b)]
        hold=[0,.85,1,1,.7,0]
        tilt=[0,0,1,.8,.15,0]
        add(pelvis,'translation',[(0,hip-(.46*t if kneel else .025*t),-.065*t if kneel else 0) for t in hold])
        add(spine,'rotation',[quat((.43 if bow else .16)*t) for t in tilt])
        add(skull,'rotation',[quat((.20 if bow else .11)*t) for t in tilt])
        for side,((h,k,f),(u,e,w)) in enumerate(zip(legs,arms)):
            sign=1 if side==0 else -1
            if kneel:
                for b,angle in ((h,-.94),(k,2.1),(f,-.64)):
                    add(b,'rotation',[quat(angle*t) for t in hold])
            if incense:
                # Thắp nhang: hai tay nâng hương trước ngực gần sát nhau
                add(u,'rotation',[combine(-.95*t,-sign*.30*t) for t in hold])
                add(e,'rotation',[combine(-.85*t,-sign*.58*t) for t in hold])
                add(w,'rotation',[quat(sign*.22*t,2) for t in hold])
            else:
                # Chắp tay búp sen / Vái / Quỳ: hai bàn tay và hai tay áo khép sát vào nhau trước ngực
                add(u,'rotation',[combine(-1.08*t,-sign*.42*t) for t in hold])
                add(e,'rotation',[combine(-.98*t,-sign*.74*t) for t in hold])
                add(w,'rotation',[quat(sign*.36*t,2) for t in hold])
    gesture('Chắp tay',3.2,bow=False)
    gesture('Vái',3.8,bow=True)
    gesture('Quỳ',5.8,kneel=True,bow=True)
    gesture('Thắp nhang',4.7,incense=True)
    g['buffers'][0]['byteLength']=len(buf)
    js=json.dumps(g,separators=(',',':')).encode()
    js+=b' '*((-len(js))%4)
    result=st.pack('<4sIIII',b'glTF',2,28+len(js)+len(buf),len(js),0x4e4f534a)+js+st.pack('<II',len(buf),0x004e4942)+buf
    (HERE/f'{name}-chuyen-dong.glb').write_bytes(result)

if __name__=='__main__':
    bake('nam',.222,.665,-.055,-.11)
    bake('nu',.204,.663,-.054,-.11)
    bake('tre-em',.191,.583,-.063,-.15)
