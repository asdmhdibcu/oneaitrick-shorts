// Kit: textures from <img>, highlighted paper sheets, 2.5D photo plates, a steam locomotive, smoke,
// a share certificate, coins. Everything is a pure function of time t.
import { THREE, textCanvas, rng, clamp, prog, ease, lerp, radialTex } from './core.js';

// ---------- textures from the page's <img> elements (HyperFrames waits for them before capture) ----------
export function imgTex(img, repeat) {
  const t = new THREE.Texture(img);
  t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
  if (repeat) { t.wrapS = t.wrapT = THREE.RepeatWrapping; }
  const up = () => { t.needsUpdate = true; };
  if (img.complete && img.naturalWidth) up(); else img.addEventListener('load', up);
  return t;
}

export const SERIF = '"GFS Baskerville", "FreeSerif", "DejaVu Serif", serif';
export const LIME = new THREE.Color(0xc8ff4d), AMBER = new THREE.Color(0xffb547), RED = new THREE.Color(0xff6b6b),
  BLUE = new THREE.Color(0x7cc4ff), PINK = new THREE.Color(0xff7ac6), GOLD = new THREE.Color(0xffc861);

// ---------- paper sheet with marker highlights ----------
// rects: { name: [[x0,y0,x1,y1] (0..1 from top-left), ...] }. setHL(name, p) sweeps the marker left->right.
export function makeSheet(tex, width, aspect, rects = {}, opt = {}) {
  const h = width * aspect;
  const g = new THREE.PlaneGeometry(width, h, 40, 52);
  const names = Object.keys(rects); const R = [], IDX = [];
  names.forEach((n, k) => rects[n].forEach((r) => { R.push(new THREE.Vector4(r[0] - 0.006, 1 - r[3] - 0.004, r[2] + 0.006, 1 - r[1] + 0.004)); IDX.push(k); }));
  while (R.length < 8) { R.push(new THREE.Vector4(-1, -1, -1, -1)); IDX.push(0); }
  const u = {
    map: { value: tex }, uRect: { value: R.slice(0, 8) }, uP: { value: new Array(8).fill(0) }, uFocus: { value: 0 },
    uBright: { value: opt.bright ?? 0.95 }, uWarm: { value: opt.warm ?? 0.06 }, uCurl: { value: opt.curl ?? 0.06 }, uW: { value: width },
    uCol: { value: (opt.color || LIME).clone() }, uLight: { value: new THREE.Vector2(0.5, 0.62) }, uFade: { value: 1 },
  };
  const m = new THREE.ShaderMaterial({
    uniforms: u, transparent: true, side: THREE.DoubleSide, toneMapped: false,
    vertexShader: `uniform float uCurl,uW; varying vec2 vUv; void main(){ vUv=uv; vec3 p=position;
      float x=uv.x-.5, y=uv.y-.5; p.z += uCurl*uW*(x*x*1.6 + y*y*0.5) + uCurl*uW*0.35*x*y;
      gl_Position=projectionMatrix*modelViewMatrix*vec4(p,1.); }`,
    fragmentShader: `uniform sampler2D map; uniform vec4 uRect[8]; uniform float uP[8]; uniform float uFocus,uBright,uWarm,uFade; uniform vec3 uCol; uniform vec2 uLight;
      varying vec2 vUv;
      void main(){ vec3 c=texture2D(map,vUv).rgb; float lum=dot(c,vec3(.299,.587,.114));
        float inHL=0.;
        for(int i=0;i<8;i++){ vec4 r=uRect[i]; if(r.x<0.) continue;
          float sweep=r.x+(r.z-r.x)*uP[i];
          float a=step(r.x,vUv.x)*step(vUv.x,sweep)*step(r.y,vUv.y)*step(vUv.y,r.w);
          // ragged marker edge
          float edge=smoothstep(0.,0.004,min(vUv.y-r.y,r.w-vUv.y));
          inHL=max(inHL,a*edge*step(.001,uP[i])); }
        vec3 paper=mix(c, c*vec3(1.,.96,.86), uWarm*6.);
        vec3 hl=mix(paper, uCol*mix(.18,1.,lum), .92);
        vec3 col=mix(paper, hl, inHL);
        float d=distance(vUv,uLight); float light=mix(1.,.62,smoothstep(.15,.85,d));
        col*=light*uBright*mix(1.,.38,uFocus*(1.-inHL));
        float rim=smoothstep(0.,.012,min(min(vUv.x,1.-vUv.x),min(vUv.y,1.-vUv.y)));
        gl_FragColor=vec4(col*mix(.6,1.,rim),uFade); }`,
  });
  const mesh = new THREE.Mesh(g, m);
  mesh.userData.setHL = (name, p) => { const k = names.indexOf(name); IDX.forEach((ix, i) => { if (ix === k && i < 8) u.uP.value[i] = clamp(p); }); };
  mesh.userData.u = u; mesh.userData.h = h;
  // where a rect sits in the sheet's local space (for aiming cameras at it)
  mesh.userData.local = (name, i = 0) => { const r = rects[name][i]; return new THREE.Vector3(((r[0] + r[2]) / 2 - 0.5) * width, (0.5 - (r[1] + r[3]) / 2) * h, 0); };
  return mesh;
}

// ---------- 2.5D photo plate: subdivided plane displaced by a depth function, with a grade ----------
export function photoPlate(tex, w, h, depth, seg = [80, 120]) {
  const g = new THREE.PlaneGeometry(w, h, seg[0], seg[1]); const P = g.attributes.position, UV = g.attributes.uv;
  for (let i = 0; i < P.count; i++) P.setZ(i, depth(UV.getX(i), UV.getY(i)));
  g.computeVertexNormals();
  const u = { map: { value: tex }, uBright: { value: 1 }, uSat: { value: 1 }, uWarm: { value: 0 }, uVig: { value: 0.35 }, uFade: { value: 1 }, uCool: { value: 0 } };
  const m = new THREE.ShaderMaterial({
    uniforms: u, transparent: true, toneMapped: false,
    vertexShader: `varying vec2 vUv; void main(){ vUv=uv; gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.); }`,
    fragmentShader: `uniform sampler2D map; uniform float uBright,uSat,uWarm,uVig,uFade,uCool; varying vec2 vUv;
      void main(){ vec3 c=texture2D(map,vUv).rgb; float l=dot(c,vec3(.299,.587,.114)); c=mix(vec3(l),c,uSat);
        c*=mix(vec3(1.),vec3(1.12,1.0,.8),uWarm); c*=mix(vec3(1.),vec3(.8,.92,1.15),uCool);
        float v=1.-uVig*smoothstep(.35,.95,length((vUv-.5)*vec2(1.2,1.)));
        gl_FragColor=vec4(c*uBright*v,uFade); }`,
  });
  const mesh = new THREE.Mesh(g, m); mesh.userData.u = u; return mesh;
}

// ---------- smoke / steam: deterministic puffs (normal blending, soft sprites) ----------
export function makeSmoke(n, color = 0xd9d4cc, opacity = 0.55) {
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.BufferAttribute(new Float32Array(n * 3), 3));
  g.setAttribute('aSize', new THREE.BufferAttribute(new Float32Array(n), 1));
  g.setAttribute('aA', new THREE.BufferAttribute(new Float32Array(n), 1));
  const m = new THREE.ShaderMaterial({
    uniforms: { uC: { value: new THREE.Color(color) }, uO: { value: opacity }, uS: { value: 960 } },
    vertexShader: `attribute float aSize; attribute float aA; uniform float uS; varying float vA; varying float vR;
      void main(){ vA=aA; vec4 mv=modelViewMatrix*vec4(position,1.); vR=fract(position.x*13.1+position.z*7.7);
        gl_PointSize=uS*aSize/max(.1,-mv.z); gl_Position=projectionMatrix*mv; }`,
    fragmentShader: `uniform vec3 uC; uniform float uO; varying float vA; varying float vR;
      void main(){ vec2 d=gl_PointCoord-.5; float r=length(d); float a=smoothstep(.5,.05,r);
        float n=.75+.25*sin((d.x+vR)*18.)*sin((d.y-vR)*15.);
        gl_FragColor=vec4(uC*(.85+.15*n), a*a*uO*vA*n); }`,
    transparent: true, depthWrite: false,
  });
  const p = new THREE.Points(g, m); p.frustumCulled = false;
  // update(t, emitFn): emitFn(i) -> {t0, pos:Vector3, vel:Vector3, size0, size1, life}
  p.userData.update = (t, spec) => {
    const a = g.attributes.position.array, s = g.attributes.aSize.array, al = g.attributes.aA.array;
    for (let i = 0; i < n; i++) {
      const e = spec(i); const age = e ? t - e.t0 : -1;
      if (!e || age < 0 || age > e.life) { s[i] = 0; al[i] = 0; a[i * 3] = a[i * 3 + 1] = a[i * 3 + 2] = 0; continue; }
      const k = age / e.life;
      a[i * 3] = e.pos.x + e.vel.x * age; a[i * 3 + 1] = e.pos.y + e.vel.y * age - (e.grav || 0) * age * age; a[i * 3 + 2] = e.pos.z + e.vel.z * age;
      s[i] = lerp(e.size0, e.size1, Math.sqrt(k)); al[i] = Math.min(1, age / 0.15) * (1 - k) * (e.a ?? 1);
    }
    g.attributes.position.needsUpdate = true; g.attributes.aSize.needsUpdate = true; g.attributes.aA.needsUpdate = true;
  };
  return p;
}

// ---------- an 1840s steam locomotive (front = +x) ----------
export function makeLoco(env, opt = {}) {
  const G = new THREE.Group();
  const body = new THREE.MeshPhysicalMaterial({ color: opt.body ?? 0x1d3a2c, metalness: 0.55, roughness: 0.38, clearcoat: 0.6, clearcoatRoughness: 0.25, envMap: env, envMapIntensity: 0.9 });
  const black = new THREE.MeshStandardMaterial({ color: 0x15161a, metalness: 0.6, roughness: 0.45, envMap: env, envMapIntensity: 0.7 });
  const brass = new THREE.MeshStandardMaterial({ color: 0xd6a548, metalness: 1, roughness: 0.28, envMap: env, envMapIntensity: 1.3 });
  const red = new THREE.MeshStandardMaterial({ color: 0xa3201c, metalness: 0.3, roughness: 0.5, envMap: env, envMapIntensity: 0.6 });
  const cyl = (r, l, m, seg = 36) => { const c = new THREE.Mesh(new THREE.CylinderGeometry(r, r, l, seg), m); c.rotation.z = Math.PI / 2; return c; };
  const boiler = cyl(0.46, 2.3, body); boiler.position.set(0.15, 1.18, 0); G.add(boiler);
  for (const x of [-0.6, 0.15, 0.9]) { const b = new THREE.Mesh(new THREE.TorusGeometry(0.465, 0.025, 8, 40), brass); b.rotation.y = Math.PI / 2; b.position.set(x, 1.18, 0); G.add(b); }
  const smoke = cyl(0.5, 0.42, black); smoke.position.set(1.48, 1.18, 0); G.add(smoke);
  const door = new THREE.Mesh(new THREE.CircleGeometry(0.44, 36), black); door.rotation.y = Math.PI / 2; door.position.set(1.70, 1.18, 0); G.add(door);
  const chim = new THREE.Mesh(new THREE.CylinderGeometry(0.13, 0.11, 1.15, 24), black); chim.position.set(1.45, 2.15, 0); G.add(chim);
  const cap = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.13, 0.18, 24), brass); cap.position.set(1.45, 2.78, 0); G.add(cap);
  const dome = new THREE.Mesh(new THREE.SphereGeometry(0.26, 24, 16, 0, Math.PI * 2, 0, Math.PI / 2), brass); dome.position.set(0.25, 1.6, 0); G.add(dome);
  const fire = new THREE.Mesh(new THREE.BoxGeometry(0.7, 1.05, 1.0), body); fire.position.set(-1.3, 1.2, 0); G.add(fire);
  const hay = new THREE.Mesh(new THREE.SphereGeometry(0.5, 28, 16, 0, Math.PI * 2, 0, Math.PI / 2), brass); hay.scale.set(0.72, 0.9, 1); hay.position.set(-1.3, 1.72, 0); G.add(hay);
  const frame = new THREE.Mesh(new THREE.BoxGeometry(3.6, 0.22, 0.86), black); frame.position.set(0.0, 0.52, 0); G.add(frame);
  const beam = new THREE.Mesh(new THREE.BoxGeometry(0.14, 0.34, 1.3), red); beam.position.set(1.78, 0.5, 0); G.add(beam);
  for (const z of [-0.45, 0.45]) { const bf = cyl(0.09, 0.3, black, 16); bf.position.set(1.95, 0.52, z); G.add(bf); const pad = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.14, 0.04, 20), black); pad.rotation.z = Math.PI / 2; pad.position.set(2.1, 0.52, z); G.add(pad); }
  // wheels: one big driver each side + small leading/trailing
  const wheels = [];
  const wheel = (r, x, z, spokes) => {
    const w = new THREE.Group(); const rim = new THREE.Mesh(new THREE.TorusGeometry(r, r * 0.07, 10, 48), red); w.add(rim);
    const tyre = new THREE.Mesh(new THREE.TorusGeometry(r * 1.02, r * 0.045, 8, 48), black); w.add(tyre);
    for (let k = 0; k < spokes; k++) { const s = new THREE.Mesh(new THREE.BoxGeometry(r * 0.06, r * 1.9, r * 0.05), red); s.rotation.z = k / spokes * Math.PI; w.add(s); }
    const hub = new THREE.Mesh(new THREE.CylinderGeometry(r * 0.16, r * 0.16, r * 0.14, 20), brass); hub.rotation.x = Math.PI / 2; w.add(hub);
    w.position.set(x, r, z); G.add(w); wheels.push({ w, r }); };
  for (const z of [-0.52, 0.52]) { wheel(0.78, -0.25, z, 14); wheel(0.4, 1.25, z, 8); wheel(0.4, -1.45, z, 8); }
  // ember glow at the front (Turner's train glows) + a lamp
  const glow = new THREE.Mesh(new THREE.CircleGeometry(0.12, 24), new THREE.MeshBasicMaterial({ color: new THREE.Color(1.0, 0.55, 0.2).multiplyScalar(2.2), toneMapped: false }));
  glow.rotation.y = Math.PI / 2; glow.position.set(1.715, 1.2, 0); G.add(glow);
  const lamp = new THREE.PointLight(0xffa25a, opt.lamp ?? 6, 9, 2); lamp.position.set(2.3, 1.2, 0); G.add(lamp);
  G.userData.roll = (dist) => wheels.forEach(({ w, r }) => { w.rotation.z = -dist / r; });
  G.userData.chimneyTop = new THREE.Vector3(1.45, 2.9, 0);
  G.userData.glow = glow;
  return G;
}

// a carriage (open 1840s coach) to trail the loco
export function makeCarriage(env, color = 0x5a1d1d) {
  const G = new THREE.Group();
  const m = new THREE.MeshPhysicalMaterial({ color, metalness: 0.2, roughness: 0.45, clearcoat: 0.5, envMap: env, envMapIntensity: 0.6 });
  const dark = new THREE.MeshStandardMaterial({ color: 0x141418, metalness: 0.5, roughness: 0.5, envMap: env, envMapIntensity: 0.5 });
  const box = new THREE.Mesh(new THREE.BoxGeometry(2.6, 1.15, 1.25), m); box.position.y = 1.25; G.add(box);
  const roof = new THREE.Mesh(new THREE.CylinderGeometry(0.75, 0.75, 2.7, 24, 1, false, 0, Math.PI), dark); roof.rotation.z = Math.PI / 2; roof.rotation.x = -Math.PI / 2; roof.scale.set(1, 1, 0.3); roof.position.y = 1.83; G.add(roof);
  const winM = new THREE.MeshBasicMaterial({ color: new THREE.Color(1, 0.72, 0.38).multiplyScalar(1.6), toneMapped: false });
  for (let k = 0; k < 3; k++) for (const z of [-0.63, 0.63]) { const wdw = new THREE.Mesh(new THREE.PlaneGeometry(0.5, 0.42), winM); wdw.position.set(-0.8 + k * 0.8, 1.38, z); wdw.rotation.y = z > 0 ? 0 : Math.PI; G.add(wdw); }
  const frame = new THREE.Mesh(new THREE.BoxGeometry(2.8, 0.18, 0.9), dark); frame.position.y = 0.6; G.add(frame);
  const wheels = [];
  for (const x of [-0.85, 0.85]) for (const z of [-0.5, 0.5]) { const w = new THREE.Mesh(new THREE.TorusGeometry(0.36, 0.05, 8, 28), dark); w.position.set(x, 0.38, z); G.add(w); wheels.push(w); }
  G.userData.roll = (dist) => wheels.forEach((w) => { w.rotation.z = -dist / 0.36; });
  return G;
}

// ---------- share certificate (canvas) ----------
export function certCanvas(opt) {
  const W = 1200, H = 800; const { c, g, tex } = textCanvas(W, H);
  const draw = (o) => {
    g.clearRect(0, 0, W, H);
    const grd = g.createLinearGradient(0, 0, W, H); grd.addColorStop(0, '#efe3c6'); grd.addColorStop(1, '#e3d1a8'); g.fillStyle = grd; g.fillRect(0, 0, W, H);
    // foxing
    const R = rng(7); for (let k = 0; k < 140; k++) { g.fillStyle = `rgba(120,80,30,${0.02 + R() * 0.05})`; g.beginPath(); g.arc(R() * W, R() * H, 2 + R() * 18, 0, 7); g.fill(); }
    g.strokeStyle = '#3d2a14'; g.lineWidth = 10; g.strokeRect(30, 30, W - 60, H - 60); g.lineWidth = 3; g.strokeRect(52, 52, W - 104, H - 104);
    g.lineWidth = 2; for (let k = 0; k < 4; k++) { const x = k % 2 ? W - 90 : 90, y = k > 1 ? H - 90 : 90; g.beginPath(); g.arc(x, y, 26, 0, 7); g.stroke(); g.beginPath(); g.arc(x, y, 14, 0, 7); g.stroke(); }
    // guilloche band
    g.strokeStyle = 'rgba(80,50,20,0.35)'; g.lineWidth = 1.2; for (let k = 0; k < 9; k++) { g.beginPath(); for (let x = 120; x <= W - 120; x += 6) { const y = 600 + Math.sin(x * 0.03 + k * 0.7) * 22 + k * 3; x === 120 ? g.moveTo(x, y) : g.lineTo(x, y); } g.stroke(); }
    g.textAlign = 'center'; g.fillStyle = '#2b1c0c';
    if (o.glitch) {
      g.fillStyle = '#0b0c10'; g.fillRect(150, 110, W - 300, 150);
      g.fillStyle = '#c8ff4d'; g.font = `900 108px InterV, Inter, sans-serif`; g.fillText('AI SHARE', W / 2, 225);
    } else {
      g.font = `700 92px ${SERIF}`; g.fillText('RAILWAY SHARE', W / 2, 220);
    }
    g.fillStyle = '#2b1c0c'; g.font = `italic 44px ${SERIF}`; g.fillText('One Share · Anno 1845', W / 2, 310);
    g.font = `700 ${o.valueSize || 190}px ${SERIF}`; g.fillStyle = o.valueColor || '#2b1c0c'; g.fillText(o.value, W / 2, 520);
    if (o.cracked) { g.strokeStyle = '#7a1010'; g.lineWidth = 7; g.beginPath(); g.moveTo(330, 360); g.lineTo(520, 470); g.lineTo(470, 540); g.lineTo(700, 640); g.lineTo(880, 560); g.stroke();
      g.lineWidth = 3; g.beginPath(); g.moveTo(520, 470); g.lineTo(610, 400); g.moveTo(700, 640); g.lineTo(760, 700); g.stroke(); }
    tex.needsUpdate = true;
  };
  draw(opt); return { tex, draw, W, H };
}

// ---------- coins ----------
export function makeCoins(n, env, color = 0xe8b64a) {
  const m = new THREE.MeshStandardMaterial({ color, metalness: 1, roughness: 0.3, envMap: env, envMapIntensity: 1.4 });
  const g = new THREE.CylinderGeometry(0.16, 0.16, 0.035, 24);
  const im = new THREE.InstancedMesh(g, m, n); im.frustumCulled = false; return im;
}

// noise-y canvas texture (plaster, wood, stone)
export function noiseTex(w, h, base, spots, seed = 1, repeat) {
  const { c, g, tex } = textCanvas(w, h); g.fillStyle = base; g.fillRect(0, 0, w, h); const R = rng(seed);
  spots.forEach(([n, col, r0, r1, a0, a1]) => { for (let k = 0; k < n; k++) { g.fillStyle = col.replace('A', (a0 + R() * (a1 - a0)).toFixed(3)); g.beginPath(); g.arc(R() * w, R() * h, r0 + R() * (r1 - r0), 0, 7); g.fill(); } });
  if (repeat) { tex.wrapS = tex.wrapT = THREE.RepeatWrapping; tex.repeat.set(repeat[0], repeat[1]); }
  tex.needsUpdate = true; return tex;
}

export { radialTex };
