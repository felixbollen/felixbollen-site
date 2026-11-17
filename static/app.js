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
