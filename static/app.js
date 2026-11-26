(()=>{
const D=document,RM=matchMedia('(prefers-reduced-motion:reduce)').matches,$=(s,r=D)=>r.querySelector(s),$$=(s,r=D)=>[...r.querySelectorAll(s)];
/* header */
const hd=$('.hd');let ly=0;
function sc(){const y=scrollY;hd.classList.toggle('sol',y>innerHeight*.6);hd.classList.toggle('up',y>ly&&y>innerHeight);ly=y}
addEventListener('scroll',sc,{passive:true});sc();
/* reveal */
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.08});
$$('.rv').forEach(e=>io.observe(e));

/* hero video pause offscreen */
$$('.vh video').forEach(v=>{v.muted=true;v.defaultMuted=true;v.setAttribute('muted','');v.playsInline=true;
  const go=()=>{const p=v.play();if(p)p.catch(()=>{})};go();
  ['touchstart','pointerdown','scroll','keydown'].forEach(t=>addEventListener(t,go,{once:true,passive:true}));
  document.addEventListener('visibilitychange',()=>{if(!document.hidden)go()});
  new IntersectionObserver(es=>es.forEach(e=>e.isIntersecting?go():v.pause())).observe(v)});

/* dalston slides */
const sl=$$('.slides img');if(sl.length){let i=0;const nx=()=>{sl[i].classList.remove('on');i=(i+1)%sl.length;const im=sl[i];if(!im.src)im.src=im.dataset.src;im.classList.add('on');const n=sl[(i+1)%sl.length];if(!n.src)n.src=n.dataset.src};
  sl[0].classList.add('on');if(sl[1])sl[1].src=sl[1].dataset.src;if(!RM)setInterval(nx,3400)}

/* bricks scrollytelling */
const br=$('.bricks');if(br){const st=$$('.step',br),pi=$$('.pics img',br),mb=$('.meter b',br),bar=$('.bar',br);let cur=-1;
  function u(){const r=br.getBoundingClientRect(),h=br.offsetHeight-innerHeight,p=Math.min(1,Math.max(0,-r.top/h));const i=Math.min(st.length-1,Math.floor(p*st.length));
    if(i!==cur){st.forEach((e,j)=>e.classList.toggle('on',j===i));pi.forEach((e,j)=>{if(j===i||j===i+1){if(!e.src)e.src=e.dataset.src}e.classList.toggle('on',j===i)});cur=i}
    const to=+br.dataset.to||0;mb.parentNode.style.display=to?'':'none';mb.textContent=Math.round(to*Math.min(1,p*1.12)).toLocaleString('en-GB')+(p>.88?'+':'');bar.style.width=(p*100)+'%'}
  addEventListener('scroll',u,{passive:true});u()}
/* lottie */
const lot=$('#lot');if(lot&&window.lottie){lottie.loadAnimation({container:lot,renderer:'svg',loop:true,autoplay:!RM,path:lot.dataset.src})}

/* accordion */
$$('.sec5>button').forEach(b=>b.addEventListener('click',()=>{const s=b.parentElement;s.classList.toggle('open');b.setAttribute('aria-expanded',s.classList.contains('open'));
  if(s.classList.contains('open'))$$('img[data-src]',s).forEach(i=>{i.src=i.dataset.src;i.removeAttribute('data-src')})}));

$$('.sec5.open img[data-src]').forEach(i=>{i.src=i.dataset.src;i.removeAttribute('data-src')});
$$('.pgal img[data-src]').forEach(i=>{i.loading='lazy';i.src=i.dataset.src;i.removeAttribute('data-src')});
/* deck */
$$('.deck').forEach(d=>{const r=$('.rail',d);$$('.nv button',d).forEach(b=>b.onclick=()=>r.scrollBy({left:(b.dataset.d==='1'?1:-1)*r.clientWidth*.8,behavior:'smooth'}))});

/* label animation */
const sp=$('.spinlab');if(sp){const ims=$$('img',sp),tg=$('.tag',sp);let i=0;if(ims.length&&!RM)setInterval(()=>{ims[i].classList.remove('on');i=(i+1)%ims.length;ims[i].classList.add('on');tg.textContent=ims[i].alt},420)}

/* lightbox */
const lb=D.createElement('div');lb.className='lb';lb.innerHTML='<div class="st"></div><div class="cp"></div><div class="ix"></div><button class="x" aria-label="Close">✕</button><button class="pv" aria-label="Previous">←</button><button class="nx" aria-label="Next">→</button>';D.body.appendChild(lb);
let set=[],cur=0;
function show(){const a=set[cur],st=$('.st',lb);const src=a.dataset.full||a.getAttribute('href');
  st.innerHTML=a.dataset.type==='scroll'?`<div class="scr"><img src="${src}" alt=""></div>`:a.dataset.type==='youtube'?`<iframe class="yt" src="https://www.youtube-nocookie.com/embed/${a.dataset.yt}?autoplay=1&rel=0&playsinline=1" allow="autoplay; encrypted-media; fullscreen; picture-in-picture" allowfullscreen></iframe>`:a.dataset.type==='video'?`<video src="${src}" controls autoplay playsinline></video>`:`<img src="${src}" alt="">`;
  $('.cp',lb).textContent=a.dataset.cap||'';$('.ix',lb).textContent=`${cur+1} / ${set.length}`}
function open(a){const g=a.closest('[data-lbg]');set=g?$$('a[data-lb]',g):[a];cur=set.indexOf(a);lb.classList.add('on');D.body.style.overflow='hidden';show()}
function close(){lb.classList.remove('on');$('.st',lb).innerHTML='';if(!$('.lbg.on'))D.body.style.overflow=''}
D.addEventListener('click',e=>{const a=e.target.closest('a[data-lb]');if(a){e.preventDefault();open(a)}});
$('.x',lb).onclick=close;$('.pv',lb).onclick=()=>{cur=(cur-1+set.length)%set.length;show()};$('.nx',lb).onclick=()=>{cur=(cur+1)%set.length;show()};
lb.addEventListener('click',e=>{if(e.target===lb)close()});
addEventListener('keydown',e=>{if(lb.classList.contains('on')){if(e.key==='Escape')close();if(e.key==='ArrowLeft')$('.pv',lb).click();if(e.key==='ArrowRight')$('.nx',lb).click()}else if(e.key==='Escape'){$$('.lbg.on').forEach(g=>g.classList.remove('on'));D.body.style.overflow=''}});
/* label grid overlay */
$$('[data-open]').forEach(b=>b.addEventListener('click',()=>{const g=D.getElementById(b.dataset.open);$$('img[data-src]',g).forEach(i=>{i.src=i.dataset.src});g.classList.add('on');D.body.style.overflow='hidden'}));
$$('.lbg .x').forEach(b=>b.onclick=()=>{b.parentElement.classList.remove('on');D.body.style.overflow=''});

/* form */
const f=D.getElementById('cf');
if(f)f.addEventListener('submit',e=>{e.preventDefault();fetch('/',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:new URLSearchParams(new FormData(f)).toString()}).then(r=>{if(!r.ok)throw 0;f.classList.add('ok')}).catch(()=>location.href='mailto:felixbollen@gmail.com')});
const ib=D.getElementById('imp'),dg=D.getElementById('impd');if(ib&&dg)ib.onclick=()=>dg.showModal();
})();
/* festival block + reels */
(function(){
  document.querySelectorAll('.fest .fv').forEach(w=>{const v=w.querySelector('video'),b=w.querySelector('.snd');
    new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){v.play().catch(()=>{})}else v.pause()}),{threshold:.3}).observe(v);
    b.addEventListener('click',()=>{v.muted=!v.muted;b.textContent=v.muted?'Sound on':'Sound off';if(!v.muted)v.play()})});
  const hov=matchMedia('(hover:hover)').matches;
  document.querySelectorAll('.reel').forEach(r=>{const v=r.querySelector('video');
    if(!hov)return;
    r.addEventListener('mouseenter',()=>{if(!v.src)v.src=v.dataset.src;v.currentTime=0;v.play().then(()=>r.classList.add('play')).catch(()=>{})});
    r.addEventListener('mouseleave',()=>{v.pause();r.classList.remove('play')})});
  /* swipe in lightbox */
  const lb=document.querySelector('.lb');if(lb){let x0=null;
    lb.addEventListener('touchstart',e=>{x0=e.touches[0].clientX},{passive:true});
    lb.addEventListener('touchend',e=>{if(x0===null)return;const dx=e.changedTouches[0].clientX-x0;x0=null;if(Math.abs(dx)>50)lb.querySelector(dx<0?'.nx':'.pv').click()},{passive:true});}
})();
/* instagram embeds: lazy-load on section open, size to grid */
(function(){
  const fit=f=>{const w=f.clientWidth;if(w)f.style.height=Math.round((w<500?124:164)+w*2/3)+'px'};
  const load=()=>document.querySelectorAll('.igw iframe[data-src]').forEach(f=>{if(f.offsetParent){f.src=f.dataset.src;f.removeAttribute('data-src');fit(f)}});
  document.addEventListener('click',()=>setTimeout(load,350));load();
  addEventListener('resize',()=>document.querySelectorAll('.igw iframe').forEach(fit));
})();
/* flip book */
(function(){document.querySelectorAll('.book').forEach(b=>{
  const pages=JSON.parse(b.querySelector('.bkd').textContent),c=b.querySelector('.bkc'),pg=c.querySelector('.pg img'),lf=c.querySelector('.lf'),li=lf.querySelector('img');
  const fix=u=>{const m=document.querySelector('.bkc img').src.match(/^(.*?)\/static\/a\//);return m&&u.startsWith('/a/')?m[1]+'/static'+u:u};
  let i=0,t=null;const pre=n=>{const im=new Image();im.src=fix(pages[n%pages.length])};
  function step(){const n=(i+1)%pages.length;pg.src=fix(pages[n]);lf.classList.add('go');
    setTimeout(()=>{li.src=fix(pages[n]);lf.classList.remove('go');i=n;c.setAttribute('href',fix(pages[i]));pre(i+1)},780)}
  c.addEventListener('mouseenter',()=>{pre(1);if(!t){step();t=setInterval(step,1400)}});
  c.addEventListener('mouseleave',()=>{clearInterval(t);t=null});
  c.addEventListener('click',e=>{if(i){e.preventDefault();e.stopPropagation();const a=[c,...b.querySelectorAll('a[hidden]')][i];a&&a.click()}},true);
})})();
/* case study viewer */
document.querySelectorAll('.csv').forEach(function(v){var L=JSON.parse(v.querySelector('.csv-d').textContent),im=v.querySelector('.csv-st img'),ix=v.querySelector('.csv-i'),c=0,pre={};var LV=null;
function ld(i){if(LV||i<0||i>=L.length||pre[i])return;var x=new Image();x.src=L[i];pre[i]=x}
function go(i){c=(i+L.length)%L.length;if(LV)LV(c);else im.src=L[c];im.alt=im.alt.replace(/\d+$/,c+1);ix.textContent=String(c+1).padStart(2,'0')+' / '+String(L.length).padStart(2,'0');ld(c+1);ld(c-1)}
v.querySelector('.csv-p').onclick=function(){go(c-1)};v.querySelector('.csv-n').onclick=function(){go(c+1)};
im.addEventListener('load',function(){if(!pre[1])ld(1)},{once:true});
var fb=v.querySelector('.csv-f');function fsOn(){return document.fullscreenElement===v||v.classList.contains('fs')}
function upd(){fb.textContent=fsOn()?'Exit full screen ✕':'Full screen ⤢'}
fb.onclick=function(){if(fsOn()){if(document.fullscreenElement)document.exitFullscreen();v.classList.remove('fs');document.body.style.overflow=''}else if(v.requestFullscreen&&!/iP(hone|od)/.test(navigator.userAgent)){v.requestFullscreen().catch(function(){v.classList.add('fs');document.body.style.overflow='hidden';upd()})}else{v.classList.add('fs');document.body.style.overflow='hidden'}upd()};
document.addEventListener('fullscreenchange',upd);
v.addEventListener('keydown',function(e){if(e.key==='ArrowRight'){go(c+1);e.preventDefault()}if(e.key==='ArrowLeft'){go(c-1);e.preventDefault()}if(e.key==='Escape'&&v.classList.contains('fs')){v.classList.remove('fs');document.body.style.overflow='';upd()}});
var sx=null;v.querySelector('.csv-st').addEventListener('touchstart',function(e){sx=e.touches[0].clientX},{passive:true});v.querySelector('.csv-st').addEventListener('touchend',function(e){if(sx===null)return;var d=e.changedTouches[0].clientX-sx;if(Math.abs(d)>40)go(c+(d<0?1:-1));sx=null});
v.addEventListener('click',function(e){if(!e.target.closest('button,a'))v.focus({preventScroll:true})});
if(v.dataset.live&&window.fetch&&v.attachShadow&&window.ResizeObserver){(function(){var B=v.dataset.live,st=v.querySelector('.csv-st');
var io=new IntersectionObserver(function(es){if(es[0].isIntersecting){io.disconnect();boot()}},{rootMargin:'300px'});io.observe(v);
function boot(){Promise.all([fetch(B+'deck.html').then(function(r){return r.text()}),fetch(B+'deck.css').then(function(r){return r.text()})]).then(function(a){
if(!document.getElementById('csv-ff')){var ff=document.createElement('style');ff.id='csv-ff';ff.textContent='@font-face{font-family:"Larken Display";src:url('+B+'f/larken-bold.woff2) format("woff2")}@font-face{font-family:"Larken Italic";src:url('+B+'f/larken-lightitalic.woff2) format("woff2")}@font-face{font-family:"Hero New";src:url('+B+'f/hero-regular.woff2) format("woff2")}@font-face{font-family:"IBM Plex Mono";font-weight:400;src:url('+B+'f/plex-400.woff2) format("woff2")}@font-face{font-family:"IBM Plex Mono";font-weight:500;src:url('+B+'f/plex-500.woff2) format("woff2")}';document.head.appendChild(ff)}
var t=document.createElement('template');t.innerHTML=a[0].replace(/src="img\//g,'src="'+B+'img/');var S=[].slice.call(t.content.querySelectorAll('section'));if(!S.length)return;
var css=a[1].replace(/:root\s*\{/g,':host{').replace(/(^|\})\s*body\s*\{/g,'$1 .sc{');
var h=document.createElement('div');h.className='csv-lv';st.insertBefore(h,st.firstChild);var sr=h.attachShadow({mode:'open'});
sr.innerHTML='<style>:host{all:initial}.vp{position:absolute;inset:0;overflow:hidden}.sc{position:absolute;left:0;top:0;width:1920px;height:1080px;transform-origin:0 0;font:32px/1.2 sans-serif}.sc *{margin:0}.sc section{width:1920px;height:1080px;overflow:hidden;box-sizing:border-box;position:relative;isolation:isolate}.sc aside{display:none}.sc h1{font-size:96px;font-weight:600}.sc h2{font-size:64px;font-weight:600}.sc h3{font-size:44px;font-weight:600}.sc p,.sc h1,.sc h2,.sc h3{overflow-wrap:break-word}'+css+'</style><div class="vp"><div class="sc"></div></div>';
var sc=sr.querySelector('.sc');function fit(){var w=h.clientWidth,hh=h.clientHeight,k=Math.min(w/1920,hh/1080);sc.style.transform='translate('+(w-1920*k)/2+'px,'+(hh-1080*k)/2+'px) scale('+k+')'}
new ResizeObserver(fit).observe(h);fit();
function warm(i){var s=S[(i+S.length)%S.length];[].forEach.call(s.querySelectorAll('img'),function(x){var y=new Image();y.src=x.getAttribute('src')})}
LV=function(i){var s=S[i%S.length].cloneNode(true);[].forEach.call(s.querySelectorAll('img[data-crop]'),function(x){var p=x.getAttribute('data-crop').split(' ');if(p.length>2)x.style.objectPosition=p[1]+' '+p[2]});sc.style.counterReset='page '+(i%S.length);sc.replaceChildren(s);
for(var j=0;j<s.children.length;j++){var ch=s.children[j];if(getComputedStyle(ch).position!=='absolute')break;ch.style.zIndex=-1}warm(i+1)};
LV(c);v.classList.add('live')}).catch(function(){})}})()}
});
