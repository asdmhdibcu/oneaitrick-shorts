// WORLD 2 — the shared storage core under the hive: the covert mailbox, 70,000 messages, the final note.
import { THREE, rng, clamp, lerp, prog, ep, ease, keys, glowPlane, lightCone, makePoints, textCanvas } from './core.js';
import { COL } from './robot.js';

const T = (x, y, z) => [x, y, z];
function cr(p0, p1, p2, p3, u) { const u2 = u * u, u3 = u2 * u; return 0.5 * ((2 * p1) + (-p0 + p2) * u + (2 * p0 - 5 * p1 + 4 * p2 - p3) * u2 + (-p0 + 3 * p1 - 3 * p2 + p3) * u3); }
function path(keys) { return (t) => { if (t <= keys[0][0]) return keys[0]; const n = keys.length; if (t >= keys[n - 1][0]) return keys[n - 1];
  let i = 0; while (i < n - 2 && t > keys[i + 1][0]) i++; const k0 = keys[Math.max(0, i - 1)], k1 = keys[i], k2 = keys[i + 1], k3 = keys[Math.min(n - 1, i + 2)];
  const u = (t - k1[0]) / (k2[0] - k1[0]); const f = (a) => [0, 1, 2].map(j => cr(k0[a][j], k1[a][j], k2[a][j], k3[a][j], u)); return [t, f(1), f(2), cr(k0[3], k1[3], k2[3], k3[3], u), 0]; }; }

const CEIL = 24, CARD = new THREE.Vector3(6, 10.2, 8), EYE = new THREE.Vector3(-1.8, 10.5, 21);
const _ab = new THREE.Vector3(), _ap = new THREE.Vector3();
function segDist(p, a, b) { _ab.subVectors(b, a); _ap.subVectors(p, a); const k = Math.max(0, Math.min(1, _ap.dot(_ab) / _ab.lengthSq())); return _ap.sub(_ab.multiplyScalar(k)).length(); }

export function makeCore(env) {
  const scene = new THREE.Scene(); scene.background = new THREE.Color(0x03040a); scene.fog = new THREE.FogExp2(0x060812, 0.03); scene.environment = env;
  scene.add(new THREE.HemisphereLight(0x7cc4ff, 0x050608, 0.3));
  const coreLight = new THREE.PointLight(0x7cc4ff, 30, 60, 1.5); coreLight.position.set(0, 12, 0); scene.add(coreLight);

  // floor disc with radial grid
  const floor = new THREE.Mesh(new THREE.CircleGeometry(60, 96), new THREE.MeshStandardMaterial({ color: 0x07090f, roughness: 0.3, metalness: 0.8 }));
  floor.rotation.x = -Math.PI / 2; floor.position.y = -6; scene.add(floor);
  const fg = new THREE.Mesh(new THREE.CircleGeometry(60, 96), new THREE.ShaderMaterial({ transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false, uniforms: { uT: { value: 0 }, uC: { value: new THREE.Color(COL.blue) } },
    vertexShader: `varying vec2 vP; void main(){ vP=position.xy; gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.); }`,
    fragmentShader: `uniform float uT; uniform vec3 uC; varying vec2 vP; void main(){ float r=length(vP), a=atan(vP.y,vP.x);
      float rings=smoothstep(.08,0.,abs(fract(r/3.-uT*.15)-.5)-.44); float spokes=smoothstep(.03,0.,abs(fract(a*24./6.2832)-.5)-.47);
      gl_FragColor=vec4(uC*(rings*.8+spokes*.35)*exp(-r*.05)*1.2,1.); }` }));
  fg.rotation.x = -Math.PI / 2; fg.position.y = -5.98; scene.add(fg);

  // ceiling = the underside of the hive cells
  const CN = 24 * 24; const ceilM = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.9, toneMapped: false });
  const ceil = new THREE.InstancedMesh(new THREE.PlaneGeometry(2.4, 2.4), ceilM, CN); ceil.frustumCulled = false;
  const M = new THREE.Matrix4(), Q = new THREE.Quaternion().setFromEuler(new THREE.Euler(Math.PI / 2, 0, 0)), V = new THREE.Vector3(), S = new THREE.Vector3(1, 1, 1), C = new THREE.Color();
  const ceilPos = []; for (let j = 0; j < 24; j++) for (let i = 0; i < 24; i++) { const x = (i - 11.5) * 3, z = (j - 11.5) * 3; ceilPos.push([x, z]); V.set(x, CEIL, z); M.compose(V, Q, S); ceil.setMatrixAt(j * 24 + i, M); ceil.setColorAt(j * 24 + i, C.setRGB(0.05, 0.1, 0.18)); }
  scene.add(ceil);

  // the core column + rings
  const colU = { uT: { value: 0 }, uHeat: { value: 0 } };
  const column = new THREE.Mesh(new THREE.CylinderGeometry(2.2, 2.2, 34, 48, 1, true), new THREE.ShaderMaterial({ uniforms: colU, transparent: true, toneMapped: false, side: THREE.DoubleSide, blending: THREE.AdditiveBlending, depthWrite: false,
    vertexShader: `varying vec2 vU; varying vec3 vN; varying vec3 vV; void main(){ vU=uv; vec4 mv=modelViewMatrix*vec4(position,1.); vN=normalize(normalMatrix*normal); vV=normalize(-mv.xyz); gl_Position=projectionMatrix*mv; }`,
    fragmentShader: `uniform float uT,uHeat; varying vec2 vU; varying vec3 vN; varying vec3 vV;
      float h(vec2 p){return fract(sin(dot(p,vec2(12.9,78.2)))*43758.5);}
      void main(){ vec2 g=vec2(floor(vU.x*48.),floor(vU.y*90.-uT*(6.+uHeat*30.)*(.6+h(vec2(floor(vU.x*48.),1.))))); float on=step(.82-uHeat*.35,h(g));
        float fr=pow(1.-abs(dot(vN,vV)),1.5); vec3 c=mix(vec3(.45,.75,1.),vec3(1.,.45,.8),uHeat);
        gl_FragColor=vec4(c*(on*.62+fr*.3+.03), .8); }` }));
  column.position.y = 11; scene.add(column);
  const coreGlow = glowPlane(22, COL.blue, 0.18); coreGlow.position.set(0, 11, 0); scene.add(coreGlow);
  const rings = []; for (let k = 0; k < 9; k++) { const r = new THREE.Mesh(new THREE.TorusGeometry(3.6 + (k % 3) * 0.5, 0.07, 8, 96), new THREE.MeshBasicMaterial({ color: new THREE.Color(COL.blue).multiplyScalar(2), toneMapped: false, transparent: true, opacity: 0.9 }));
    r.position.y = -2 + k * 3.6; r.rotation.x = Math.PI / 2; scene.add(r); rings.push(r); }

  // pipes from the core up to the ceiling cells
  const R0 = rng(4); const pipes = []; const pipeMat = new THREE.MeshBasicMaterial({ color: new THREE.Color(0x2b6cff).multiplyScalar(0.5), transparent: true, opacity: 0.4, toneMapped: false, depthWrite: false, blending: THREE.AdditiveBlending });
  for (let k = 0; k < 34; k++) { const a = k / 34 * Math.PI * 2 + R0() * 0.2; const cp = ceilPos[Math.floor(R0() * CN)]; const end = new THREE.Vector3(Math.cos(a) * (8 + R0() * 22), CEIL - 0.1, Math.sin(a) * (8 + R0() * 22));
    const y0 = 2 + R0() * 18; const start = new THREE.Vector3(Math.cos(a) * 2.3, y0, Math.sin(a) * 2.3);
    const mid = new THREE.Vector3(Math.cos(a) * (6 + R0() * 6), y0 + 2 + R0() * 4, Math.sin(a) * (6 + R0() * 6));
    const curve = new THREE.CatmullRomCurve3([start, mid, new THREE.Vector3(end.x * 0.8, CEIL - 6 - R0() * 4, end.z * 0.8), end]);
    const tube = new THREE.Mesh(new THREE.TubeGeometry(curve, 40, 0.09, 6), pipeMat); scene.add(tube); pipes.push(curve); }
  // packets (glowing envelopes) travel the pipes
  const PK = 260; const envG = new THREE.BoxGeometry(0.62, 0.42, 0.06);
  const envM = new THREE.MeshBasicMaterial({ color: 0xffffff, toneMapped: false });
  const packets = new THREE.InstancedMesh(envG, envM, PK); packets.frustumCulled = false; packets.instanceMatrix.setUsage(THREE.DynamicDrawUsage); scene.add(packets); packets.setColorAt(0, C);
  const pkSeed = Array.from({ length: PK }, (_, k) => [Math.floor(R0() * 34), Math.floor(R0() * 34), R0(), 0.35 + R0() * 0.4]);
  // the single first letter (hero packet), bigger with a halo
  const first = new THREE.Mesh(new THREE.BoxGeometry(1.1, 0.74, 0.08), new THREE.MeshBasicMaterial({ color: new THREE.Color(COL.lime).multiplyScalar(2.2), toneMapped: false }));
  const firstHalo = glowPlane(4, COL.lime, 0.8); scene.add(first, firstHalo);
  // the storm
  const STORM = 5200; const storm = makePoints(STORM, 0xffffff, 0.05, 0.5); scene.add(storm);
  const sSeed = Array.from({ length: STORM }, () => [R0(), R0(), R0(), R0()]);
  // sea of messages (question)
  const SEA = 420; const sea = new THREE.InstancedMesh(envG, new THREE.MeshBasicMaterial({ color: 0xffffff, toneMapped: false, transparent: true }), SEA); sea.frustumCulled = false; sea.instanceMatrix.setUsage(THREE.DynamicDrawUsage); scene.add(sea); sea.setColorAt(0, C);
  const seaSeed = Array.from({ length: SEA }, () => [R0() * 2 - 1, R0(), R0() * 2 - 1, R0(), R0()]);
  // the note card
  const cardC = textCanvas(1024, 600);
  const card = new THREE.Mesh(new THREE.PlaneGeometry(3.4, 2.0), new THREE.MeshBasicMaterial({ map: cardC.tex, transparent: true, toneMapped: false, depthWrite: false, side: THREE.DoubleSide })); scene.add(card);
  const cardHalo = glowPlane(4.6, COL.lime, 0.0); scene.add(cardHalo);
  let cardKey = '';
  function drawCard(mode, n, cursor, a) {
    const key = mode + n + cursor + a.toFixed(2) + (document.fonts ? document.fonts.check('900 100px InterV') : ''); if (key === cardKey) return; cardKey = key; const g = cardC.g, w = 1024, h = 600; g.clearRect(0, 0, w, h); g.globalAlpha = a;
    const lime = mode === 2; g.fillStyle = lime ? 'rgba(14,20,6,0.9)' : 'rgba(10,14,24,0.9)'; rr(g, 8, 8, w - 16, h - 16, 44); g.fill();
    g.strokeStyle = lime ? '#c8ff4d' : '#ff7ac6'; g.lineWidth = 6; rr(g, 8, 8, w - 16, h - 16, 44); g.stroke();
    g.fillStyle = lime ? '#c8ff4d' : '#ff7ac6'; g.font = '700 32px Mono, monospace'; g.fillText(lime ? 'THE ONLY QUESTION LEFT' : 'MESSAGE 1 OF 70,000+', 56, 92);
    g.fillStyle = '#ffffff'; g.font = '900 118px InterV, sans-serif';
    const txt = mode === 2 ? 'should we?' : '“we should continue.”'; const s = txt.slice(0, n);
    if (mode !== 2) { g.font = '900 80px InterV, sans-serif'; }
    g.fillText(s, 56, 330);
    if (cursor) { const tw = g.measureText(s).width; g.fillStyle = lime ? '#c8ff4d' : '#ff7ac6'; g.fillRect(66 + tw, 250, 40, 96); }
    g.globalAlpha = 1; cardC.tex.needsUpdate = true;
  }

  const blue = new THREE.Color(COL.blue), pink = new THREE.Color(COL.pink), lime = new THREE.Color(COL.lime), Eu = new THREE.Euler(), zero = new THREE.Matrix4().makeScale(0, 0, 0);
  const tmp = new THREE.Vector3(), tmp2 = new THREE.Vector3();

  function update(t) {
    const A = t < 70;            // first visit (mailbox / storm) vs second (the question)
    const heat = A ? keys(t, [[47, 0], [53, 0.15], [56.2, 0.4], [57.5, 1]]) : keys(t, [[96, 0.35], [100, 0.12], [104.9, 0.05]]);
    colU.uT.value = t; colU.uHeat.value = heat; coreGlow.material.color.copy(blue).lerp(pink, heat); coreGlow.material.opacity = 0.12 + heat * 0.16;
    coreLight.color.copy(blue).lerp(pink, heat); coreLight.intensity = 30 + heat * 50;
    rings.forEach((r, k) => { r.rotation.z = t * (0.3 + k * 0.05) * (k % 2 ? 1 : -1); r.material.color.copy(blue).lerp(pink, heat).multiplyScalar(1.3); r.position.y = -2 + k * 3.6 + Math.sin(t * 0.8 + k) * 0.2; });
    fg.material.uniforms.uT.value = t; fg.material.uniforms.uC.value.copy(blue).lerp(pink, heat * 0.8);
    scene.fog.density = A ? 0.026 : keys(t, [[96, 0.03], [99, 0.02], [106, 0.026]]);
    // ceiling cells flicker as they get messages
    for (let k = 0; k < CN; k++) { const ph = Math.sin(t * (1.5 + (k % 7) * 0.4) + k * 1.7); const lit = A ? clamp(heat * 1.2 + (ph > 0.96 ? 0.6 : 0)) : 0.3;
      ceil.setColorAt(k, C.copy(new THREE.Color(0.03, 0.06, 0.11)).lerp(A ? pink : blue, lit * 0.5)); }
    ceil.instanceColor.needsUpdate = true;

    // first letter: drops from a cell, down pipe 0, into the core, out via pipe 9, up to another cell
    const fOn = A && t > 47.6 && t < 52.9;
    first.visible = firstHalo.visible = fOn;
    if (fOn) { let p;
      if (t < 49.6) { const u = ep(t, 47.7, 49.5, ease.io); p = pipes[0].getPointAt(1 - u); }
      else { const u = ep(t, 49.7, 52.4, ease.io); p = pipes[9].getPointAt(u); }
      first.position.copy(p); firstHalo.position.copy(p); first.rotation.set(Math.sin(t * 3) * 0.3, t * 2, 0); first.scale.setScalar(t > 52.4 ? 1 - prog(t, 52.4, 52.9) : 1);
      firstHalo.material.opacity = 0.8 * first.scale.x; }
    // packets: count grows (a few -> dozens -> hundreds) along the pipes
    const nP = A ? Math.floor(keys(t, [[49.6, 0], [50.4, 6], [53.2, 14], [54.0, 60], [55.1, 160], [56.2, 260]], ease.in)) : 0;
    for (let k = 0; k < PK; k++) { if (k >= nP) { packets.setMatrixAt(k, zero); continue; } const s = pkSeed[k]; const u = (s[2] + t * s[3] * (1 + heat * 1.8)) % 1;
      const down = u < 0.5; const p = down ? pipes[s[0]].getPointAt(1 - u * 2) : pipes[s[1]].getPointAt((u - 0.5) * 2);
      tmp.copy(p); Eu.set(t * 2 + k, t * 3 + k, 0); M.compose(tmp, new THREE.Quaternion().setFromEuler(Eu), S.setScalar(0.85)); packets.setMatrixAt(k, M);
      packets.setColorAt(k, C.copy(k % 5 === 0 ? lime : k % 2 ? pink : blue).multiplyScalar(1.4)); S.set(1, 1, 1); }
    packets.instanceMatrix.needsUpdate = true; packets.instanceColor.needsUpdate = true; packets.visible = A;
    // storm (seventy thousand)
    const sOn = A ? keys(t, [[55.8, 0], [56.3, 0.4], [57.4, 1], [59, 1]]) : 0; storm.visible = sOn > 0.01;
    if (storm.visible) { const a = storm.geometry.attributes.position.array, sz = storm.geometry.attributes.aSize.array, ca = storm.geometry.attributes.aCol.array;
      for (let k = 0; k < STORM; k++) { const s = sSeed[k]; const th = s[0] * 6.2832 + t * (0.6 + s[1] * 1.6); const r = 2.8 + s[2] * 20 * (0.5 + 0.5 * sOn); const y = -4 + ((s[3] * 30 + t * (2 + s[1] * 5)) % 30);
        a[k * 3] = Math.cos(th) * r; a[k * 3 + 1] = y; a[k * 3 + 2] = Math.sin(th) * r; sz[k] = (k / STORM < sOn) ? 0.5 + s[1] : 0;
        const c = k % 6 === 0 ? lime : k % 2 ? pink : blue; ca[k * 3] = c.r; ca[k * 3 + 1] = c.g; ca[k * 3 + 2] = c.b; }
      storm.geometry.attributes.position.needsUpdate = true; storm.geometry.attributes.aSize.needsUpdate = true; storm.geometry.attributes.aCol.needsUpdate = true; }

    // ---- the question ----
    sea.visible = !A; card.visible = cardHalo.visible = !A;
    if (!A) {
      for (let k = 0; k < SEA; k++) { const s = seaSeed[k]; const x = s[0] * 22, z = s[2] * 22, y = 1 + s[1] * 20 + Math.sin(t * 0.4 + k) * 0.6; tmp.set(x, y, z);
        if (tmp.distanceTo(CARD) < 2.6 || segDist(tmp, CARD, EYE) < 2.3) { sea.setMatrixAt(k, zero); continue; }
        Eu.set(Math.sin(t * 0.3 + k) * 0.6, t * 0.2 + k, 0); M.compose(tmp, new THREE.Quaternion().setFromEuler(Eu), S.setScalar(1)); sea.setMatrixAt(k, M);
        const dim = keys(t, [[96.4, 1], [99.8, 1], [100.6, 0.35]]); sea.setColorAt(k, C.copy(k % 4 === 0 ? lime : k % 2 ? pink : blue).multiplyScalar(1.1 * dim)); }
      sea.instanceMatrix.needsUpdate = true; sea.instanceColor.needsUpdate = true;
      // one message flies to the camera and opens
      const fly = ep(t, 98.4, 100.3, ease.out); tmp.set(14, 16, -12).lerp(CARD, fly); card.position.copy(tmp); cardHalo.position.copy(tmp).add(tmp2.set(0, 0, -0.2));
      const open = ep(t, 99.6, 100.4, ease.back); card.scale.set(lerp(0.18, 1, open), lerp(0.12, 1, open), 1); card.rotation.set(0, (1 - fly) * 2.6, (1 - fly) * 0.5);
      cardHalo.material.color.set(t > 104.8 ? COL.lime : COL.pink); cardHalo.material.opacity = 0.22 * open;
      const mode = t < 104.85 ? 1 : 2; const txt1 = '“we should continue.”';
      let n; if (mode === 1) n = t < 100.7 ? 0 : t < 101.5 ? Math.round(prog(t, 100.7, 101.45) * txt1.length) : txt1.length;
      else n = Math.round(prog(t, 104.95, 105.45) * 'should we?'.length);
      const glitch = (t > 104.55 && t < 104.95);
      drawCard(glitch ? 1 : mode, glitch ? Math.max(0, txt1.length - Math.round(prog(t, 104.55, 104.92) * txt1.length)) : n, Math.floor(t * 3) % 2 === 0 || (t > 100.6 && t < 101.6), clamp(open));
      if (glitch) { card.position.x += Math.sin(t * 90) * 0.04; }
    }
  }

  const cams = {
    'core-a': path([[47.05, T(4, 30, 14), T(0, 10, 0), 56], [48.6, T(10, 30, 30), T(0, 11, 0), 50], [49.7, T(18, 22, 30), T(0, 12, 0), 46],
      [52.8, T(31, 14, 14), T(0, 12, 0), 44], [54.2, T(31, 10, 2), T(0, 11.5, 0), 46], [56.2, T(26, 10, -16), T(0, 12, 0), 50],
      [57.8, T(14, 13, -26), T(0, 14, 0), 54], [59.0, T(8, 22, -18), T(0, 26, 0), 60]]),
    'core-b': path([[96.4, T(6, 20, 44), T(0, 11, 0), 46], [98.4, T(0, 13, 32), T(4, 10.5, 6), 40], [99.9, T(-1.8, 10.55, 20.2), T(6, 10.2, 8), 34],
      [101.4, T(-1.5, 10.45, 19.2), T(6, 10.2, 8), 34], [102.7, T(-1.7, 10.5, 19.8), T(6, 10.2, 8), 34], [104.8, T(-1.4, 10.4, 18.9), T(6, 10.2, 8), 33],
      [106.3, T(-3, 11.5, 26), T(5, 10.5, 6), 38], [110.2, T(-4, 13, 32), T(4, 11, 4), 42]]),
  };
  return { scene, update, camFor: (id) => cams[id] };
}
function rr(g, x, y, w, h, r) { g.beginPath(); g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r); g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath(); }
