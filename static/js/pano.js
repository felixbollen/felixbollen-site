// Full-screen 360° viewer: drag, scroll/trackpad or tilt the phone to look around.
import * as THREE from 'three';

const data = document.querySelector('script.pano-data');
if (data) {
  const items = JSON.parse(data.textContent);
  const title = data.dataset.title || '360°';
  const ov = document.createElement('div');
  ov.className = 'pano';
  ov.innerHTML = `<div class="pv3"></div>
  <div class="ptop"><span class="lbl">${title}</span><button class="px" aria-label="Close">✕</button></div>
  <div class="phint lbl">Drag, scroll or tilt your phone to look around</div>
  <div class="pbar"><div class="pcap"></div><div class="pthumbs">${items.map((it, i) =>
    `<button type="button" data-i="${i}" aria-label="${it.caption}"><img src="${it.thumb || it.image}" alt=""><span>${String(i + 1).padStart(2, '0')}</span></button>`).join('')}</div>
  <button class="pgyro" type="button">Use phone motion</button></div>`;
  document.body.appendChild(ov);

  const host = ov.querySelector('.pv3');
  let renderer, scene, camera, mesh, raf = 0, cur = -1, open = false;
  let latMin = -85, lon = 180, lat = 0, vlon = 0, vlat = 0, fov = 65, useGyro = false, gq = null;
  const loader = new THREE.TextureLoader(); loader.setCrossOrigin('anonymous');
  const cache = {};

  function init() {
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setPixelRatio(Math.min(3, devicePixelRatio || 1));
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    host.appendChild(renderer.domElement);
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(fov, 1, 0.1, 1100);
    const geo = new THREE.SphereGeometry(500, 64, 40); geo.scale(-1, 1, 1);
    mesh = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: 0x111111 }));
    scene.add(mesh);
    addEventListener('resize', size); new ResizeObserver(size).observe(host); size();
  }
  function size() { if (!renderer) return; const w = host.clientWidth || innerWidth, h = host.clientHeight || innerHeight; renderer.setSize(w, h); camera.aspect = w / h; camera.updateProjectionMatrix(); }

  function show(i) {
    if (i === cur) return; cur = i;
    ov.querySelectorAll('.pthumbs button').forEach((b, j) => b.classList.toggle('on', j === i));
    ov.querySelector('.pcap').textContent = items[i].caption || '';
    host.classList.add('ld');
    const apply = t => { if (cur !== i) return;
      const vto = +items[i].vto || 1; latMin = vto < 1 ? 90 - vto * 180 + fov / 2 + 2 : -85;
      mesh.geometry.dispose(); const g = new THREE.SphereGeometry(500, 64, 40, 0, Math.PI * 2, 0, Math.PI * vto); g.scale(-1, 1, 1); mesh.geometry = g;
      mesh.material.dispose(); mesh.material = new THREE.MeshBasicMaterial({ map: t }); host.classList.remove('ld'); };
    if (cache[i]) apply(cache[i]);
    else loader.load(items[i].image, t => { t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; cache[i] = t; apply(t); });
    lon = 180; lat = 0; vlon = 0.06; if (+items[i].vto < 1) lat = 10;
    if (items[i + 1] && !cache[i + 1]) loader.load(items[i + 1].image, t => { t.colorSpace = THREE.SRGBColorSpace; cache[i + 1] = t; });
  }

  // gyro → camera quaternion (standard device-orientation maths)
  const zee = new THREE.Vector3(0, 0, 1), euler = new THREE.Euler(), q0 = new THREE.Quaternion(), q1 = new THREE.Quaternion(-Math.sqrt(0.5), 0, 0, Math.sqrt(0.5));
  let ori = null;
  function onOri(e) { if (e.alpha == null) return; ori = e; useGyro = true; ov.classList.add('gy'); }
  function gyroQuat() {
    const d = THREE.MathUtils.DEG2RAD, a = ori.alpha * d, b = ori.beta * d, g = ori.gamma * d, o = ((screen.orientation && screen.orientation.angle) || window.orientation || 0) * d;
    euler.set(b, a, -g, 'YXZ'); const q = new THREE.Quaternion().setFromEuler(euler);
    q.multiply(q1); q.multiply(q0.setFromAxisAngle(zee, -o)); return q;
  }
  function askGyro() {
    if (typeof DeviceOrientationEvent === 'undefined') return;
    if (typeof DeviceOrientationEvent.requestPermission === 'function')
      DeviceOrientationEvent.requestPermission().then(s => { if (s === 'granted') addEventListener('deviceorientation', onOri); }).catch(() => {});
    else addEventListener('deviceorientation', onOri);
  }
  let yawOff = 0;

  function loop() {
    raf = requestAnimationFrame(loop);
    if (useGyro && ori) {
      camera.quaternion.copy(gyroQuat());
      camera.rotateOnWorldAxis(new THREE.Vector3(0, 1, 0), yawOff);
    } else {
      if (!drag) { lon += vlon; vlon *= 0.95; if (Math.abs(vlon) < 0.02) vlon = 0.02; }
      lat = Math.max(Math.min(latMin, 20), Math.min(85, lat));
      const phi = THREE.MathUtils.degToRad(90 - lat), th = THREE.MathUtils.degToRad(lon);
      camera.lookAt(500 * Math.sin(phi) * Math.cos(th), 500 * Math.cos(phi), 500 * Math.sin(phi) * Math.sin(th));
    }
    renderer.render(scene, camera);
  }

  // pointer drag
  let drag = false, px = 0, py = 0, plon = 0, plat = 0, lastX = 0;
  host.addEventListener('pointerdown', e => { drag = true; px = e.clientX; py = e.clientY; plon = lon; plat = lat; lastX = e.clientX; host.setPointerCapture(e.pointerId); ov.classList.add('used'); });
  host.addEventListener('pointermove', e => {
    if (!drag) return;
    if (useGyro) { yawOff += (e.clientX - lastX) * 0.004; lastX = e.clientX; return; }
    const k = fov / (host.clientHeight || innerHeight); lon = plon - (e.clientX - px) * k * 1.2; lat = plat + (e.clientY - py) * k * 1.2; vlon = -(e.clientX - lastX) * k; lastX = e.clientX;
  });
  host.addEventListener('pointerup', () => drag = false); host.addEventListener('pointercancel', () => drag = false);
  // scroll / trackpad: look around; pinch (ctrl+wheel) zooms
  host.addEventListener('wheel', e => {
    e.preventDefault(); ov.classList.add('used');
    if (e.ctrlKey) { fov = Math.max(35, Math.min(95, fov + e.deltaY * 0.1)); camera.fov = fov; camera.updateProjectionMatrix(); return; }
    lon += (e.deltaX || 0) * 0.08 + (e.shiftKey ? 0 : e.deltaY * 0.08); if (Math.abs(e.deltaX) > Math.abs(e.deltaY)) lat -= 0; vlon = 0;
  }, { passive: false });
  addEventListener('keydown', e => {
    if (!open) return;
    if (e.key === 'Escape') close();
    if (e.key === 'ArrowRight') show((cur + 1) % items.length);
    if (e.key === 'ArrowLeft') show((cur - 1 + items.length) % items.length);
  });

  ov.querySelectorAll('.pthumbs button').forEach(b => b.addEventListener('click', () => show(+b.dataset.i)));
  ov.querySelector('.px').addEventListener('click', close);
  const gb = ov.querySelector('.pgyro');
  if (matchMedia('(pointer:coarse)').matches) gb.classList.add('on');
  gb.addEventListener('click', () => { askGyro(); gb.classList.remove('on'); });

  function openPano(i = 0) {
    if (!renderer) init();
    open = true; ov.classList.add('open'); document.documentElement.style.overflow = 'hidden';
    size(); cur = -1; show(i); cancelAnimationFrame(raf); loop();
    if (typeof DeviceOrientationEvent !== 'undefined' && typeof DeviceOrientationEvent.requestPermission !== 'function' && matchMedia('(pointer:coarse)').matches) askGyro();
  }
  function close() { open = false; ov.classList.remove('open'); document.documentElement.style.overflow = ''; cancelAnimationFrame(raf); }
  window.openPano = openPano;

  // open when the section is expanded, or from its button
  document.querySelectorAll('[data-pano-open]').forEach(b => b.addEventListener('click', e => { e.preventDefault(); openPano(0); }));
  const sec = data.closest('.sec5');
  if (sec) sec.querySelector(':scope > button').addEventListener('click', () => {
    setTimeout(() => { if (sec.querySelector(':scope > button').getAttribute('aria-expanded') === 'true') openPano(0); }, 30);
  });
}
