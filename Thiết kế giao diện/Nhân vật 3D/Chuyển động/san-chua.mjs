import * as T from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { clone } from 'three/addons/utils/SkeletonUtils.js';

const status=document.querySelector('#status'), canvas=document.querySelector('canvas');
const scene=new T.Scene();
scene.background=new T.Color(0xebe3d4);
scene.fog=new T.Fog(0xebe3d4,21,42);
const camera=new T.PerspectiveCamera(37,1,.1,60);
const renderer=new T.WebGLRenderer({canvas,antialias:true,powerPreference:'low-power'});
renderer.setPixelRatio(1);
scene.add(new T.HemisphereLight(0xfff8ef,0xb3a389,2.4));
const sun=new T.DirectionalLight(0xffe9cd,2.1);
sun.position.set(-4,9,5);scene.add(sun);
function resize(){
 const {width,height}=canvas.getBoundingClientRect();renderer.setSize(width,height,false);
 camera.aspect=width/height; camera.updateProjectionMatrix();
 camera.position.set(7,9,camera.aspect<.85?20:13);camera.lookAt(0,.45,0);
}
addEventListener('resize',resize);resize();
const floor=new T.Mesh(new T.PlaneGeometry(80,80),new T.MeshStandardMaterial({color:0xc3b397}));
floor.rotation.x=-Math.PI/2;scene.add(floor);
const yard=new T.Mesh(new T.BoxGeometry(14,.055,11),new T.MeshStandardMaterial({color:0xd2c4ad}));
yard.position.y=-.027;scene.add(yard);
const loader=new GLTFLoader();
const people=[];
const turns=(target,current)=>Math.atan2(Math.sin(target-current),Math.cos(target-current));
const clock=new T.Clock();
const anchors=[[0,-1.35],[3.5,-2.85],[2.2,-2.8],[4.75,-2.8],[1.7,3.5],[-2.5,3.4],[-4.5,1],[-2.9,-1.4],[3.8,.1]];
function box(w,h,d,x,y,z,color){
 const mesh=new T.Mesh(new T.BoxGeometry(w,h,d),new T.MeshStandardMaterial({color,roughness:.88}));
 mesh.position.set(x,y,z);scene.add(mesh);return mesh;
}
for(let n=0;n<4;n++){
 const h=.12*(n+1);
 box(2.2,h,.36,0,h/2,-1.98-.36*n,0x9b8875);
}
box(2.2,.48,1.24,0,.24,-3.68,0xa18b75);
box(3.6,.1,.94,3.5,.72,-3.92,0x674333);
for(const x of [1.93,5.07])box(.14,.67,.74,x,.335,-3.92,0x674333);
for(const x of [2.2,3.5,4.75]){
 box(.30,.13,.27,x,.83,-3.68,0x8b583b);
 for(let i=0;i<3;i++)box(.011,.19,.011,x+(i-1)*.063,.99,-3.68,0xa64c3a);
}
box(.052,.12,.052,3.61,.83,-3.49,0xe0c38b);
const flame=new T.Mesh(new T.SphereGeometry(.028,10,8),new T.MeshBasicMaterial({color:0xff9b38}));
flame.scale.set(.65,1.65,.65);
flame.position.set(3.61,.925,-3.49);scene.add(flame);
function stairHeight(z){
 if(z>=-1.8)return 0;
 return Math.min(.48,Math.floor((-z-1.8)/.36+1)*.12);
}

const types=['nam','nu','tre-em'];
const heights=[1.74,1.6,1.24];

async function start(){
 const assets=await Promise.all(types.map(type=>loader.loadAsync(new URL(type+'-chuyen-dong.glb',import.meta.url).href)));
 for(const a of assets){
  a.scene.traverse(o=>{if(o.isSkinnedMesh){
   o.geometry.computeVertexNormals();
   o.material=new T.MeshStandardMaterial({vertexColors:true,roughness:.9});
   o.frustumCulled=false;
  }});
 }
 const count=matchMedia('(max-width: 600px)').matches?6:9;
 for(let i=0;i<count;i++){
  const type=i%3, asset=assets[type], root=new T.Group(), model=clone(asset.scene);
  let box;
  model.traverse(o=>{if(o.isSkinnedMesh){o.geometry.computeBoundingBox();box=o.geometry.boundingBox;}});
  const scale=heights[type]/(box.max.y-box.min.y);
  model.scale.setScalar(scale);model.position.y=-box.min.y*scale;
  root.add(model);scene.add(root);
  const shadow=new T.Mesh(new T.CircleGeometry(.33,22),new T.MeshBasicMaterial({color:0x514434,transparent:true,opacity:.14,depthWrite:false}));
  shadow.rotation.x=-Math.PI/2;shadow.scale.set(1,.64,1);scene.add(shadow);
  const [x,z]=anchors[i];
  root.position.set(x,0,z);
  const mixer=new T.AnimationMixer(model);
  const idle=mixer.clipAction(asset.animations.find(a=>a.name==='Dung')).play();
  const walk=mixer.clipAction(asset.animations.find(a=>a.name==='Di bo')).play();
  walk.time=(i*.34)%walk.getClip().duration;
  walk.setEffectiveWeight(0);idle.setEffectiveWeight(1);
  const label=['Cầu thang','Thắp nhang','Quỳ','Vái'][i];
  const special=(i===0?['Lên cầu thang','Xuống cầu thang']:label?[label]:[])
   .map(name=>mixer.clipAction(asset.animations.find(a=>a.name===name)).play().setEffectiveWeight(0));
  let incense, ember;
  if(i===1){
   incense=new T.Mesh(new T.CylinderGeometry(.006,.006,.31,8),new T.MeshStandardMaterial({color:0x9c3b30}));
   model.traverse(o=>{if(o.isBone && o.name.replace(/[ _]/g,'')==='Lhand')o.add(incense);});
   incense.position.set(.01,.12,.015);
   ember=new T.Mesh(new T.SphereGeometry(.010,8,6),new T.MeshBasicMaterial({color:0xff713d}));
   ember.position.y=.15;incense.add(ember);
  }
  people.push({root,shadow,mixer,idle,walk,special,incense,ember,label,blend:0,speed:0,desired:.45*scale/(.6*1.24),
    angle:i*.85,timer:.25+i*.15,origin:new T.Vector2(x,z),target:new T.Vector2(x,z),visit:0,i,scale});
 }
 status.textContent=people.length+' nhân vật';
 canvas.dataset.characters=String(people.length);
 clock.start();renderer.setAnimationLoop(frame);
}
function frame(){
 const dt=Math.min(clock.getDelta(),.05);
 let moving=0, turning=0;
 for(const p of people){
  const {root,target,origin}=p;
  if(p.label && p.i!==0){
   const action=p.special[0];
   const duration=action.getClip().duration;
   const phase=(clock.elapsedTime+1+p.i*.9)%(duration+1.9);
   action.time=Math.min(phase,duration);
   action.paused=true;
   const weight=phase<duration?1:0;
   p.idle.setEffectiveWeight(1-weight);
   action.setEffectiveWeight(weight);
   if(p.incense){
    p.incense.visible=phase>.4 && phase<duration*.77;
    p.ember.visible=phase>duration*.36;
   }
   root.rotation.y=Math.PI;
   p.shadow.position.set(root.position.x,.004,root.position.z);
   p.mixer.update(dt);
   continue;
  }
  const dx=target.x-root.position.x,dz=target.y-root.position.z,d=Math.hypot(dx,dz);
  let goal=0;
  if(d<.045){
   p.timer-=dt;
   if(p.timer<=0){
    p.visit++;
    if(p.i===0)target.set(0,p.visit%2?-3.72:-1.35);
    else {
     const a=2.39996*p.visit+p.i*.84;
     const radius=.92+.25*Math.sin(p.visit+p.i);
     target.set(origin.x+radius*Math.cos(a),origin.y+radius*Math.sin(a));
    }
    p.timer=.5+(p.i%4)*.28;
   }
  }else{
   const error=turns(Math.atan2(dx,dz),p.angle);
   p.angle+=T.MathUtils.clamp(error,-3*dt,3*dt);
   if(Math.abs(error)>.18)turning++;
   goal=p.desired*Math.min(1,d/.32)*T.MathUtils.clamp(1-Math.abs(error)/1.15,0,1);
  }
  p.speed=T.MathUtils.damp(p.speed,goal,7,dt);
  const step=Math.min(d,p.speed*dt);
  if(d>.045){
   root.position.x+=dx/d*step;root.position.z+=dz/d*step;
  }
  root.rotation.y=p.angle;
  const ground=p.i===0?stairHeight(root.position.z):0;
  root.position.y=T.MathUtils.damp(root.position.y,ground,12,dt);
  p.shadow.position.set(root.position.x,ground+.004,root.position.z);
  p.blend=T.MathUtils.damp(p.blend,T.MathUtils.clamp(p.speed/(p.desired*.7),0,1),8,dt);
  p.idle.setEffectiveWeight(1-p.blend);p.walk.setEffectiveWeight(p.i===0?0:p.blend);
  if(p.i===0){
   const ascending=p.visit%2===1;
   p.special.forEach((action,index)=>{
    action.setEffectiveWeight(index===Number(!ascending)?p.blend:0);
    action.setEffectiveTimeScale(Math.max(.3,p.speed/p.desired));
   });
   canvas.dataset.stairs=ground.toFixed(2);
  }
  p.walk.setEffectiveTimeScale(Math.max(.3,p.speed/p.desired));
  p.mixer.update(dt);
  if(p.speed>.12)moving++;
 }
 canvas.dataset.moving=String(moving);
 canvas.dataset.turning=String(turning);
 renderer.render(scene,camera);
}
start().catch(e=>{status.textContent='Không tải được nhân vật';console.error(e);});
