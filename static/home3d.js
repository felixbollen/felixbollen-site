import * as THREE from 'three';
import {SVGLoader} from '/js/SVGLoader.js';
import {RoomEnvironment} from '/js/RoomEnvironment.js';
const stk=document.querySelector('.mark .stk');
const RM=matchMedia('(prefers-reduced-motion:reduce)').matches;
try{
  const r=new THREE.WebGLRenderer({antialias:true,alpha:true});
  r.setPixelRatio(Math.min(2,devicePixelRatio||1));r.toneMapping=THREE.ACESFilmicToneMapping;r.toneMappingExposure=1.05;r.outputColorSpace=THREE.SRGBColorSpace;
  stk.appendChild(r.domElement);
  const sc=new THREE.Scene();const pm=new THREE.PMREMGenerator(r);sc.environment=pm.fromScene(new RoomEnvironment(),0.03).texture;
  const cam=new THREE.PerspectiveCamera(28,1,10,10000);cam.position.set(0,0,3600);
  const svg=stk.querySelector('svg.main').outerHTML.replace('<path','<path fill="#000"');
  const data=new SVGLoader().parse(svg);const g=new THREE.Group();
  const mat=new THREE.MeshPhysicalMaterial({color:0x060606,metalness:0.15,roughness:0.14,clearcoat:1,clearcoatRoughness:0.04,envMapIntensity:1.6});
  data.paths.forEach(p=>SVGLoader.createShapes(p).forEach(s=>{
    const geo=new THREE.ExtrudeGeometry(s,{depth:70,bevelEnabled:true,bevelThickness:34,bevelSize:26,bevelOffset:-2,bevelSegments:12,curveSegments:28});
    g.add(new THREE.Mesh(geo,mat))}));
  const box=new THREE.Box3().setFromObject(g),c=box.getCenter(new THREE.Vector3());g.children.forEach(m=>m.geometry.translate(-c.x,-c.y,-c.z));
  g.scale.set(1,-1,1);const piv=new THREE.Group();piv.add(g);sc.add(piv);
  const k1=new THREE.DirectionalLight(0xffffff,2.2);k1.position.set(-1200,1600,1800);sc.add(k1);
  const k2=new THREE.DirectionalLight(0xffffff,1.2);k2.position.set(1600,-400,1200);sc.add(k2);
  const k3=new THREE.DirectionalLight(0xffffff,1.5);k3.position.set(0,0,-2000);sc.add(k3);
  function size(){const w=r.domElement.clientWidth,h=r.domElement.clientHeight;r.setSize(w,h,false);cam.aspect=w/h;cam.updateProjectionMatrix()}
  new ResizeObserver(size).observe(stk);size();stk.classList.add('gl');
  let tx=0,ty=0,cx=0,cy=0,last=-1e4,b0=null,g0=null;
  const set=(x,y)=>{tx=Math.max(-1,Math.min(1,x));ty=Math.max(-1,Math.min(1,y));last=performance.now()};
  addEventListener('pointermove',e=>{if(e.pointerType==='mouse')set((e.clientX/innerWidth-.5)*2,(e.clientY/innerHeight-.5)*2)});
  const ori=e=>{if(e.gamma==null)return;if(b0==null){b0=e.beta;g0=e.gamma}set((e.gamma-g0)/25,(e.beta-b0)/25)};
  const btn=document.querySelector('.gyro');
  if(typeof DeviceOrientationEvent!=='undefined'){
    if(typeof DeviceOrientationEvent.requestPermission==='function'){
      if(matchMedia('(pointer:coarse)').matches&&btn)btn.classList.add('on');
      const ask=()=>DeviceOrientationEvent.requestPermission().then(s=>{if(s==='granted'){addEventListener('deviceorientation',ori);btn&&btn.classList.remove('on')}}).catch(()=>{});
      btn&&btn.addEventListener('click',ask);document.addEventListener('touchend',ask,{once:true});
    }else addEventListener('deviceorientation',ori);
  }
  let vis=true;new IntersectionObserver(es=>vis=es[0].isIntersecting).observe(stk);
  (function loop(t){requestAnimationFrame(loop);if(!vis)return;let x=tx,y=ty;
    if(t-last>2500&&!RM){x=Math.sin(t/2600)*.55;y=Math.cos(t/3300)*.3}
    cx+=(x-cx)*.06;cy+=(y-cy)*.06;piv.rotation.y=cx*.75;piv.rotation.x=cy*.5;piv.position.x=cx*60;r.render(sc,cam)})(0);
}catch(e){console.warn('3D off',e)}
