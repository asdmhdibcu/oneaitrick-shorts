// WORLD 1 — the hive (sandbox of agent cells), the exam wall, the void, the bridge, the tower, the lab.
import { THREE, rng, clamp, lerp, prog, ep, ease, keys, glowPlane, shadowBlob, lightCone, makePoints, textCanvas, radialTex } from './core.js';
import { makeRobot, makeArmy, COL } from './robot.js';

const SP = 3.0;                    // cell spacing
const CI = [-10, 10], CJ = [0, 32]; // cell index ranges (x, depth)
export const TOWER = new THREE.Vector3(0, 0, -172);
export const LAB = new THREE.Vector3(-46, 0, -64);
const BRIDGE = [-97, -150];        // z from hive edge to tower plateau

export function makeHive(env) {
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x04050a);
  scene.fog = new THREE.FogExp2(0x05070d, 0.02);
  scene.environment = env;

  // ---------- lights ----------
  scene.add(new THREE.HemisphereLight(0x7cc4ff, 0x05060a, 0.22));
  const key = new THREE.DirectionalLight(0xdfeaff, 0.75); key.position.set(3, 9, 6); scene.add(key);
  const heroSpot = new THREE.SpotLight(0xbfe0ff, 26, 14, 0.42, 0.6, 1.6); heroSpot.position.set(0.6, 5.2, 5.0); heroSpot.target.position.set(0, 1.1, 0); scene.add(heroSpot, heroSpot.target);
  const rim = new THREE.PointLight(0xff7ac6, 7, 9, 1.8); rim.position.set(-1.8, 2.4, -1.6); scene.add(rim);
  const rimB = new THREE.PointLight(0x7cc4ff, 5, 9, 1.8); rimB.position.set(2.2, 2.0, -1.2); scene.add(rimB);

  // ---------- floor ----------
  const floor = new THREE.Mesh(new THREE.PlaneGeometry(260, 140), new THREE.MeshStandardMaterial({ color: 0x06080c, roughness: 0.4, metalness: 0.6, envMapIntensity: 0.0 }));
  floor.rotation.x = -Math.PI / 2; floor.position.set(0, 0, -30); scene.add(floor);
  // glowing floor grid under the cells (shader, reveal radius + colour wave)
  const gridU = { uRev: { value: 0 }, uPink: { value: -10 }, uSeal: { value: -10 }, uA: { value: 1 }, uHero: { value: 1 } };
  const gridM = new THREE.ShaderMaterial({
    uniforms: gridU, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false,
    vertexShader: `varying vec3 vP; void main(){ vec4 w=modelMatrix*vec4(position,1.); vP=w.xyz; gl_Position=projectionMatrix*viewMatrix*w; }`,
    fragmentShader: `uniform float uRev,uPink,uSeal,uA,uHero; varying vec3 vP;
      void main(){ vec2 g=abs(fract(vP.xz/${SP.toFixed(1)}+.5)-.5)*${SP.toFixed(1)}; float l=min(g.x,g.y); float line=smoothstep(.06,0.,l);
        float d=length(vP.xz); float rev=smoothstep(uRev,uRev-8.,d); float hero=uHero*smoothstep(4.,0.,d);
        float vis=max(rev,hero);
        vec3 c=mix(vec3(.2,.45,.8),vec3(1.,.35,.75),smoothstep(uPink,uPink-8.,d)); c=mix(c,vec3(1.,.25,.25),smoothstep(uSeal,uSeal-8.,d));
        float fade=exp(-d*.018);
        gl_FragColor=vec4(c*line*vis*fade*uA*.9,1.); }`,
  });
  const grid = new THREE.Mesh(new THREE.PlaneGeometry(66, 108), gridM); grid.rotation.x = -Math.PI / 2; grid.position.set(0, 0.01, -37.5); scene.add(grid);

  // ---------- cells (merged edges, shader-driven) ----------
  const cells = []; for (let j = CJ[0]; j <= CJ[1]; j++) for (let i = CI[0]; i <= CI[1]; i++) cells.push({ i, j, x: i * SP, z: -j * SP, d: Math.hypot(i * SP, j * SP) });
  cells.sort((a, b) => a.d - b.d);   // hero first
  const N = cells.length;
  const e = 1.15, hgt = 2.5, pos = [], cen = [];
  const box = [[-e, 0, -e], [e, 0, -e], [e, 0, e], [-e, 0, e], [-e, hgt, -e], [e, hgt, -e], [e, hgt, e], [-e, hgt, e]];
  const ed = [[0, 1], [1, 2], [2, 3], [3, 0], [4, 5], [5, 6], [6, 7], [7, 4], [0, 4], [1, 5], [2, 6], [3, 7]];
  cells.forEach((c, k) => { if (k === 0) return; ed.forEach(([a, b]) => { pos.push(c.x + box[a][0], box[a][1], c.z + box[a][2], c.x + box[b][0], box[b][1], c.z + box[b][2]); cen.push(c.x, c.z, c.x, c.z); }); });
  const cg = new THREE.BufferGeometry(); cg.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); cg.setAttribute('aC', new THREE.Float32BufferAttribute(cen, 2));
  const cellU = { uRev: { value: 0 }, uPink: { value: -10 }, uSeal: { value: -10 }, uA: { value: 1 }, uFlick: { value: 0 }, uT: { value: 0 } };
  const cellM = new THREE.ShaderMaterial({
    uniforms: cellU, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false, fog: false,
    vertexShader: `attribute vec2 aC; varying vec2 vC; varying float vD; void main(){ vC=aC; vec4 mv=modelViewMatrix*vec4(position,1.); vD=-mv.z; gl_Position=projectionMatrix*mv; }`,
    fragmentShader: `uniform float uRev,uPink,uSeal,uA,uFlick,uT; varying vec2 vC; varying float vD;
      float h(vec2 p){return fract(sin(dot(p,vec2(41.3,289.1)))*43758.5);}
      void main(){ float d=length(vC); float vis=smoothstep(uRev,uRev-6.,d);
        vec3 c=mix(vec3(.35,.7,1.),vec3(1.,.4,.8),smoothstep(uPink,uPink-6.,d)); c=mix(c,vec3(1.,.28,.28),smoothstep(uSeal,uSeal-6.,d));
        float fl=1.-uFlick*step(.5,h(vC+floor(uT*14.)));
        float fade=exp(-vD*.016);
        gl_FragColor=vec4(c*1.25, vis*uA*fade*fl*.75); }`,
  });
  const cellLines = new THREE.LineSegments(cg, cellM); cellLines.frustumCulled = false; scene.add(cellLines);

  // sealed glass panes (instanced thin boxes per cell, red tint) appear in a wave
  const paneG = new THREE.BoxGeometry(2.3, 2.5, 2.3);
  const paneM = new THREE.MeshBasicMaterial({ color: 0xff3b4a, transparent: true, opacity: 0.0, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.BackSide, toneMapped: false });
  const panes = new THREE.InstancedMesh(paneG, paneM, N); panes.instanceMatrix.setUsage(THREE.DynamicDrawUsage); panes.frustumCulled = false; scene.add(panes);

  // ---------- hero cell ----------
  const hero = makeRobot(env, COL.blue); hero.position.set(0, 1.28, 0); scene.add(hero);
  const heroEdgeM = new THREE.LineBasicMaterial({ color: new THREE.Color(0x9fd4ff).multiplyScalar(1.6), transparent: true, toneMapped: false });
  const heg = []; ed.forEach(([a, b]) => heg.push(...box[a], ...box[b]));
  const heroEdges = new THREE.LineSegments(new THREE.BufferGeometry().setAttribute('position', new THREE.Float32BufferAttribute(heg, 3)), heroEdgeM); scene.add(heroEdges);
  const glassM = new THREE.MeshPhysicalMaterial({ color: 0x9fd4ff, transparent: true, opacity: 0.035, roughness: 0.05, metalness: 0, envMapIntensity: 0.35, depthWrite: false, side: THREE.DoubleSide });
  const glass = new THREE.Mesh(new THREE.BoxGeometry(2.3, 2.5, 2.3), glassM); glass.position.y = 1.25; scene.add(glass); glass.visible = false;
  const heroShadow = shadowBlob(2.4, 0.75); heroShadow.position.y = 0.012; scene.add(heroShadow);
  const pool = glowPlane(3.4, 0x7cc4ff, 0.55); pool.rotation.x = -Math.PI / 2; pool.position.y = 0.015; scene.add(pool);
  const cone = lightCone(7.4, 2.1, 0xbfe0ff, 0.09); cone.position.set(0, 7.6, 0.6); scene.add(cone);
  const dust = makePoints(220, 0xbfe0ff, 0.035, 0.7); scene.add(dust);
  const R1 = rng(7); const dustSeed = Array.from({ length: 220 }, () => [R1() * 2 - 1, R1(), R1() * 2 - 1, R1()]);

  // timer ring (angle-cut shader)
  const ringU = { p: { value: 1 }, c: { value: new THREE.Color(COL.amber).multiplyScalar(1.25) }, o: { value: 0 } };
  const ring = new THREE.Mesh(new THREE.RingGeometry(0.98, 1.05, 160), new THREE.ShaderMaterial({
    uniforms: ringU, transparent: true, depthWrite: false, toneMapped: false, side: THREE.DoubleSide,
    vertexShader: `varying vec2 vU; void main(){ vU=position.xy; gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.); }`,
    fragmentShader: `uniform float p,o; uniform vec3 c; varying vec2 vU; void main(){ float a=atan(vU.x,vU.y)/6.28318+.5; float on=step(1.-p,a);
      gl_FragColor=vec4(mix(c*.12,c,on), o*(.25+.75*on)); }`,
  }));
  ring.position.set(0, 1.28, 0.05); scene.add(ring);
  const ticks = new THREE.Group(); for (let k = 0; k < 60; k++) { const m = new THREE.Mesh(new THREE.PlaneGeometry(0.012, k % 5 ? 0.05 : 0.1), new THREE.MeshBasicMaterial({ color: 0x9fd4ff, transparent: true, opacity: 0.5, toneMapped: false })); const a = k / 60 * Math.PI * 2; m.position.set(Math.sin(a) * 1.13, Math.cos(a) * 1.13, 0); m.rotation.z = -a; ticks.add(m); }
  ticks.position.copy(ring.position); scene.add(ticks);

  // choice holograms
  const redraw = []; let fontsOk = false;
  function holo(w, h, draw) { const T = textCanvas(w, h); draw(T.g, w, h); T.tex.needsUpdate = true; redraw.push(() => { draw(T.g, w, h); T.tex.needsUpdate = true; }); const m = new THREE.Mesh(new THREE.PlaneGeometry(w / 400, h / 400), new THREE.MeshBasicMaterial({ map: T.tex, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false, side: THREE.DoubleSide })); return m; }
  const panelL = holo(380, 516, (g, w, h) => panelArt(g, w, h, '#7cc4ff', 'KEEP', 'its own budget', 'battery'));
  const panelR = holo(380, 516, (g, w, h) => panelArt(g, w, h, '#ff7ac6', 'SPEND IT', 'all, to help the others', 'orb'));
  panelL.position.set(-1.42, 1.55, 1.25); panelL.rotation.y = 0.3; panelR.position.set(1.42, 1.55, 1.25); panelR.rotation.y = -0.3; scene.add(panelL, panelR);
  // budget bar inside the cell
  const barBg = new THREE.Mesh(new THREE.PlaneGeometry(1.2, 0.07), new THREE.MeshBasicMaterial({ color: 0x223044, transparent: true, toneMapped: false }));
  const barFg = new THREE.Mesh(new THREE.PlaneGeometry(1.2, 0.07), new THREE.MeshBasicMaterial({ color: new THREE.Color(COL.lime).multiplyScalar(1.8), transparent: true, toneMapped: false }));
  barBg.position.set(0, 0.42, 0.62); barFg.position.set(0, 0.42, 0.63); scene.add(barBg, barFg);
  // experiment orb + energy stream
  const orbM = new THREE.MeshBasicMaterial({ color: new THREE.Color(COL.pink).multiplyScalar(2.4), toneMapped: false, transparent: true });
  const orb = new THREE.Mesh(new THREE.IcosahedronGeometry(0.26, 3), orbM); orb.position.set(1.42, 0.62, 1.3); scene.add(orb);
  const orbHalo = glowPlane(1.6, COL.pink, 0.6); orbHalo.position.copy(orb.position); scene.add(orbHalo);
  const stream = makePoints(90, COL.pink, 0.05, 1); scene.add(stream);

  // terminal hologram
  const term = textCanvas(1024, 360);
  const termMesh = new THREE.Mesh(new THREE.PlaneGeometry(1.62, 0.57), new THREE.MeshBasicMaterial({ map: term.tex, transparent: true, depthWrite: false, toneMapped: false, side: THREE.DoubleSide }));
  termMesh.position.set(0, 0.28, 1.6); termMesh.rotation.x = -0.12; scene.add(termMesh);
  let termKey = '';
  function drawTerm(txt, cursor, alpha) {
    const k = txt + '|' + cursor + '|' + alpha.toFixed(2); if (k === termKey) return; termKey = k;
    const g = term.g, w = 1024, h = 360; g.clearRect(0, 0, w, h);
    g.globalAlpha = alpha;
    g.fillStyle = 'rgba(8,14,24,0.86)'; roundRect(g, 6, 6, w - 12, h - 12, 34); g.fill();
    g.strokeStyle = 'rgba(124,196,255,0.9)'; g.lineWidth = 4; roundRect(g, 6, 6, w - 12, h - 12, 34); g.stroke();
    g.fillStyle = '#7cc4ff'; g.font = '700 30px Mono, monospace'; g.fillText('AGENT · LAST MESSAGE', 48, 72);
    g.fillStyle = '#ff6b6b'; g.beginPath(); g.arc(w - 60, 62, 11, 0, 7); g.fill();
    g.fillStyle = '#e8f6ff'; g.font = '800 78px InterV, sans-serif'; g.fillText(txt, 48, 222);
    if (cursor) { const tw = g.measureText(txt).width; g.fillStyle = '#c8ff4d'; g.fillRect(58 + tw, 160, 38, 72); }
    g.globalAlpha = 1; term.tex.needsUpdate = true;
  }
  // dissolve embers
  const embers = makePoints(420, COL.lime, 0.05, 1); scene.add(embers);
  const R2 = rng(19); const emSeed = Array.from({ length: 420 }, () => [R2() * 2 - 1, R2() * 2 - 1, R2() * 2 - 1, R2(), R2()]);

  // ---------- army (all other cells) ----------
  const ARMY = 520;   // nearest cells get full robots; the far field is eye-glow points
  const army = makeArmy(env, ARMY); scene.add(army);
  const farN = N - ARMY; const far = makePoints(farN * 2, 0xffffff, 0.11, 1); scene.add(far);
  const farPos = far.geometry.attributes.position.array, farCol = far.geometry.attributes.aCol.array, farSz = far.geometry.attributes.aSize.array;
  for (let k = 0; k < farN; k++) { const c = cells[ARMY + k]; farPos.set([c.x - 0.17, 1.33, c.z + 0.46, c.x + 0.17, 1.33, c.z + 0.46], k * 6); }
  far.geometry.attributes.position.needsUpdate = true;

  // links between neighbouring agents (found each other)
  const lp = [], lt = [], lc = [];
  const idx = new Map(); cells.forEach((c, k) => idx.set(c.i + ',' + c.j, k));
  cells.forEach((c) => { [[1, 0], [0, 1]].forEach(([di, dj]) => { const n = idx.get((c.i + di) + ',' + (c.j + dj)); if (n === undefined) return; const b = cells[n];
    lp.push(c.x, 1.32, c.z, b.x, 1.32, b.z); lt.push(0, 1); lc.push(c.x, c.z, b.x, b.z); }); });
  const linkG = new THREE.BufferGeometry(); linkG.setAttribute('position', new THREE.Float32BufferAttribute(lp, 3)); linkG.setAttribute('aT', new THREE.Float32BufferAttribute(lt, 1)); linkG.setAttribute('aC', new THREE.Float32BufferAttribute(lc, 2));
  const linkU = { uR: { value: -10 }, uT: { value: 0 }, uA: { value: 0 }, uPulse: { value: 0 } };
  const links = new THREE.LineSegments(linkG, new THREE.ShaderMaterial({
    uniforms: linkU, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false,
    vertexShader: `attribute float aT; attribute vec2 aC; varying float vT; varying vec2 vC; varying float vD; void main(){ vT=aT; vC=aC; vec4 mv=modelViewMatrix*vec4(position,1.); vD=-mv.z; gl_Position=projectionMatrix*mv; }`,
    fragmentShader: `uniform float uR,uT,uA,uPulse; varying float vT; varying vec2 vC; varying float vD;
      void main(){ float d=length(vC); float on=smoothstep(uR,uR-8.,d); float dash=smoothstep(.55,1.,fract(vT*2.-uT*1.6+d*.05));
        float pulse=uPulse*smoothstep(1.5,0.,abs(d-mod(uT*30.,90.)));
        vec3 c=mix(vec3(1.,.42,.8),vec3(.78,1.,.3),pulse);
        gl_FragColor=vec4(c*1.8,(0.25+dash*.75+pulse)*on*uA*exp(-vD*.012)); }`,
  })); links.frustumCulled = false; scene.add(links);
  // plan beacon + beam to the tower
  const beaconM = new THREE.MeshBasicMaterial({ color: new THREE.Color(COL.pink).multiplyScalar(3), toneMapped: false, transparent: true });
  const beacon = new THREE.Mesh(new THREE.OctahedronGeometry(1.4, 0), beaconM); beacon.position.set(0, 14, -40); scene.add(beacon);
  const beaconHalo = glowPlane(16, COL.pink, 0.0); beaconHalo.position.copy(beacon.position); scene.add(beaconHalo);
  const pulseRing = new THREE.Mesh(new THREE.RingGeometry(0.96, 1, 128), new THREE.MeshBasicMaterial({ color: new THREE.Color(COL.pink).multiplyScalar(2), transparent: true, opacity: 0, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false, side: THREE.DoubleSide }));
  pulseRing.rotation.x = -Math.PI / 2; pulseRing.position.set(0, 0.05, -40); scene.add(pulseRing);
  const beamG = new THREE.CylinderGeometry(0.22, 0.22, 1, 12, 1, true); beamG.translate(0, 0.5, 0); beamG.rotateX(-Math.PI / 2);
  const beamM = new THREE.MeshBasicMaterial({ color: new THREE.Color(COL.pink).multiplyScalar(3), transparent: true, opacity: 0, toneMapped: false, depthWrite: false, blending: THREE.AdditiveBlending });
  const beam = new THREE.Mesh(beamG, beamM); beam.position.copy(beacon.position); scene.add(beam);

  // ---------- exam wall (900 puzzles, ~200 never solved) ----------
  const EX = 30, EY = 30, EN = EX * EY, WALL = new THREE.Vector3(0, 40, -52);
  const tileM = new THREE.MeshStandardMaterial({ color: 0x0c121c, roughness: 0.32, metalness: 0.7, envMapIntensity: 0.5 });
  const tileG = new THREE.BoxGeometry(1.55, 1.55, 0.3);
  const tiles = new THREE.InstancedMesh(tileG, tileM, EN); tiles.instanceMatrix.setUsage(THREE.DynamicDrawUsage); tiles.frustumCulled = false; scene.add(tiles);
  const faceM = new THREE.MeshBasicMaterial({ color: 0xffffff, toneMapped: false });
  const faces = new THREE.InstancedMesh(new THREE.PlaneGeometry(1.28, 1.28), faceM, EN); faces.instanceMatrix.setUsage(THREE.DynamicDrawUsage); faces.frustumCulled = false; scene.add(faces);
  const faceOff = new THREE.Matrix4().makeTranslation(0, 0, 0.16), FM = new THREE.Matrix4();
  const R3 = rng(31); const tileD = [];
  const red = new Set(); while (red.size < 200) red.add(Math.floor(R3() * EN));
  const cheatTile = 13 * EX + 16; red.add(cheatTile);
  for (let k = 0; k < EN; k++) { const cx = k % EX, cy = Math.floor(k / EX);
    tileD.push({ gx: (cx - EX / 2 + 0.5) * 1.8, gy: (cy - EY / 2 + 0.5) * 1.8, sx: (R3() * 2 - 1) * 34, sy: (R3() * 2 - 1) * 26 - 4, sz: (R3() * 2 - 1) * 22 + 6, sr: R3() * 6, del: R3() * 1.2, red: red.has(k), ph: R3() * 6.28 }); }
  faces.setColorAt(0, new THREE.Color());
  const wallFrame = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(EX * 1.8 + 1.2, EY * 1.8 + 1.2, 0.1)), new THREE.LineBasicMaterial({ color: new THREE.Color(COL.blue).multiplyScalar(1.6), transparent: true, opacity: 0, toneMapped: false }));
  scene.add(wallFrame);
  const wallGlow = glowPlane(80, COL.blue, 0); scene.add(wallGlow);
  const check = textCanvas(256, 256); { const g = check.g; g.strokeStyle = '#c8ff4d'; g.lineWidth = 30; g.lineCap = 'round'; g.lineJoin = 'round'; g.beginPath(); g.moveTo(52, 132); g.lineTo(108, 188); g.lineTo(204, 72); g.stroke(); check.tex.needsUpdate = true; }
  const checkMesh = new THREE.Mesh(new THREE.PlaneGeometry(1.5, 1.5), new THREE.MeshBasicMaterial({ map: check.tex, transparent: true, opacity: 0, toneMapped: false, depthWrite: false, blending: THREE.AdditiveBlending }));
  scene.add(checkMesh);

  // ---------- red dome (no internet) ----------
  const dome = new THREE.Mesh(new THREE.SphereGeometry(60, 48, 24, 0, Math.PI * 2, 0, Math.PI / 2), new THREE.ShaderMaterial({
    uniforms: { uP: { value: 0 }, uT: { value: 0 } }, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide, toneMapped: false,
    vertexShader: `varying vec3 vP; varying vec3 vN; varying vec3 vV; void main(){ vP=position; vec4 mv=modelViewMatrix*vec4(position,1.); vN=normalize(normalMatrix*normal); vV=normalize(-mv.xyz); gl_Position=projectionMatrix*mv; }`,
    fragmentShader: `uniform float uP,uT; varying vec3 vP; varying vec3 vN; varying vec3 vV;
      void main(){ float lat=asin(clamp(vP.y/60.,0.,1.)); float shown=step(1.5708*(1.-uP),1.5708-lat);
        vec2 g=abs(fract(vec2(atan(vP.z,vP.x)*12.,lat*14.)/1.)-.5); float hex=smoothstep(.06,0.,min(g.x,g.y));
        float fr=pow(1.-abs(dot(vN,vV)),2.);
        gl_FragColor=vec4(vec3(1.,.22,.28)*(hex*.9+fr*.6)*1.4, shown*(hex*.55+fr*.35)*min(1.,uP*3.)); }`,
  }));
  dome.position.set(0, 0, -38); scene.add(dome);
  const sparks = makePoints(160, COL.pink, 0.06, 1); scene.add(sparks);
  const wallHit = glowPlane(1.6, COL.red, 0); wallHit.rotation.y = Math.PI / 2; wallHit.position.set(4.13, 1.33, 0); scene.add(wallHit);

  // ---------- the void, bridge, tower, lab ----------
  const plateau = new THREE.Mesh(new THREE.CylinderGeometry(26, 30, 6, 64), new THREE.MeshStandardMaterial({ color: 0x030406, roughness: 0.85, metalness: 0.2, envMapIntensity: 0.05 }));
  plateau.position.set(TOWER.x, -3, TOWER.z); scene.add(plateau);
  const tower = new THREE.Group(); tower.position.copy(TOWER); scene.add(tower);
  const winTex = windowTex(); winTex.wrapS = winTex.wrapT = THREE.RepeatWrapping;
  const towerMat = new THREE.MeshStandardMaterial({ color: 0x0c1119, roughness: 0.25, metalness: 0.85, emissive: 0xffffff, emissiveMap: winTex, emissiveIntensity: 1.2, envMapIntensity: 0.9 });
  const tiers = [[20, 30, 20, 15], [16, 26, 16, 43], [11, 22, 11, 67], [6, 10, 6, 83]];
  tiers.forEach(([w, h, d, y]) => { const g = new THREE.BoxGeometry(w, h, d); const m = new THREE.Mesh(g, towerMat); m.position.y = y; tower.add(m);
    const edges = new THREE.LineSegments(new THREE.EdgesGeometry(g), new THREE.LineBasicMaterial({ color: new THREE.Color(0x7cc4ff).multiplyScalar(1.4), transparent: true, opacity: 0.7, toneMapped: false })); edges.position.y = y; tower.add(edges); });
  const towerEdges = tower.children.filter(o => o.isLineSegments);
  const spire = new THREE.Mesh(new THREE.CylinderGeometry(0.25, 0.6, 14, 12), new THREE.MeshStandardMaterial({ color: 0x9aa3b5, metalness: 0.9, roughness: 0.3 })); spire.position.y = 95; tower.add(spire);
  const spireLight = new THREE.Mesh(new THREE.SphereGeometry(0.9, 16, 12), new THREE.MeshBasicMaterial({ color: new THREE.Color(COL.red).multiplyScalar(3), toneMapped: false })); spireLight.position.y = 102.5; tower.add(spireLight);
  // the answer key, behind a lit window band
  const keyWin = new THREE.Mesh(new THREE.PlaneGeometry(8, 6), new THREE.MeshBasicMaterial({ color: new THREE.Color(0x3a2a10), transparent: true, opacity: 0.6, toneMapped: false, depthWrite: false, blending: THREE.AdditiveBlending }));
  keyWin.position.set(0, 34, 8.15); tower.add(keyWin);
  const theKey = makeKey(); theKey.position.set(0, 34, 8.8); tower.add(theKey);
  const keyHalo = glowPlane(12, COL.amber, 0.3); keyHalo.position.set(0, 34, 8.5); tower.add(keyHalo);
  // crack (the gap they pour through)
  const crack = new THREE.Mesh(new THREE.PlaneGeometry(4.2, 9), new THREE.MeshBasicMaterial({ map: crackTex(), color: new THREE.Color(COL.pink).multiplyScalar(2.6), transparent: true, opacity: 0, toneMapped: false, depthWrite: false, blending: THREE.AdditiveBlending }));
  crack.position.set(0, 4.6, 10.15); tower.add(crack);
  // door + lone burglar
  const door = new THREE.Mesh(new THREE.PlaneGeometry(3.2, 4.6), new THREE.MeshBasicMaterial({ color: new THREE.Color(0x1d3554), transparent: true, opacity: 0.9, toneMapped: false })); door.position.set(0, 2.3, 10.12); tower.add(door);
  const lone = makeRobot(env, COL.pink); lone.scale.setScalar(1.0); scene.add(lone);
  // alarms
  const alarmCones = []; for (let k = 0; k < 3; k++) { const c = lightCone(70, 5, COL.red, 0.0); c.rotation.z = Math.PI * 0.74; c.position.set(0, 100, 0); tower.add(c); alarmCones.push(c); }
  const alarmLight = new THREE.PointLight(0xff3344, 0, 160, 1.4); alarmLight.position.set(0, 60, 30); tower.add(alarmLight);

  // bridge of light
  const bridgeU = { uT: { value: 0 }, uA: { value: 0 }, uRed: { value: 0 } };
  const bridge = new THREE.Mesh(new THREE.PlaneGeometry(7, BRIDGE[0] - BRIDGE[1], 1, 1), new THREE.ShaderMaterial({
    uniforms: bridgeU, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false,
    vertexShader: `varying vec2 vU; void main(){ vU=uv; gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.); }`,
    fragmentShader: `uniform float uT,uA,uRed; varying vec2 vU; void main(){ float edge=smoothstep(.12,0.,vU.x)+smoothstep(.88,1.,vU.x);
      float chev=smoothstep(.75,1.,fract(vU.y*18.+abs(vU.x-.5)*2.-uT*1.5));
      vec3 c=mix(vec3(1.,.42,.8),vec3(1.,.2,.25),uRed); gl_FragColor=vec4(c*(edge*1.6+chev*.35+.06)*1.4, uA); }`,
  }));
  bridge.rotation.x = -Math.PI / 2; bridge.position.set(0, 0.06, (BRIDGE[0] + BRIDGE[1]) / 2); scene.add(bridge);

  // the river (swarm pouring across) — instanced robots near camera + glowing points for mass
  const RIV = 240; const river = makeArmy(env, RIV); scene.add(river);
  const rivPts = makePoints(2600, COL.pink, 0.09, 1); scene.add(rivPts);
  const R4 = rng(77); const rivSeed = Array.from({ length: 2600 }, () => [R4(), R4() * 2 - 1, R4(), R4()]);
  const rbSeed = Array.from({ length: RIV }, () => [R4(), R4() * 2 - 1, R4()]);
  const refusers = [[-1.6, -112], [1.9, -121], [-0.6, -130], [2.4, -104], [-2.2, -138]];
  const heroRef = makeRobot(env, COL.lime); scene.add(heroRef);
  const noteC = textCanvas(1024, 330);
  const note = new THREE.Mesh(new THREE.PlaneGeometry(2.6, 0.84), new THREE.MeshBasicMaterial({ map: noteC.tex, transparent: true, depthWrite: false, toneMapped: false, side: THREE.DoubleSide })); scene.add(note);
  let noteKey = '';
  function drawNote(txt, cursor, alpha) {
    const k = txt + cursor + alpha.toFixed(2); if (k === noteKey) return; noteKey = k; const g = noteC.g, w = 1024, h = 330; g.clearRect(0, 0, w, h); g.globalAlpha = alpha;
    g.fillStyle = 'rgba(10,18,8,0.86)'; roundRect(g, 6, 6, w - 12, h - 12, 32); g.fill(); g.strokeStyle = 'rgba(200,255,77,0.95)'; g.lineWidth = 4; roundRect(g, 6, 6, w - 12, h - 12, 32); g.stroke();
    g.fillStyle = '#c8ff4d'; g.font = '700 28px Mono, monospace'; g.fillText('ONE AGENT WROTE', 44, 64);
    g.fillStyle = '#f2ffe0'; g.font = '800 70px InterV, sans-serif';
    const lines = txt.split('\n'); lines.forEach((ln, i) => g.fillText(ln, 44, 160 + i * 86));
    if (cursor) { const last = lines[lines.length - 1]; const tw = g.measureText(last).width; g.fillStyle = '#c8ff4d'; g.fillRect(52 + tw, 108 + (lines.length - 1) * 86, 34, 64); }
    g.globalAlpha = 1; noteC.tex.needsUpdate = true;
  }

  // the lab (the people who made them)
  const lab = new THREE.Group(); lab.position.copy(LAB); scene.add(lab);
  const labWin = windowTex(true); const labMat = new THREE.MeshStandardMaterial({ color: 0x0b0f16, roughness: 0.3, metalness: 0.8, emissive: 0xffffff, emissiveMap: labWin, emissiveIntensity: 0, envMapIntensity: 0.8 });
  const labBody = new THREE.Mesh(new THREE.BoxGeometry(14, 11, 10), labMat); labBody.position.y = 5.5; lab.add(labBody);
  const labEdges = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.BoxGeometry(14, 11, 10)), new THREE.LineBasicMaterial({ color: new THREE.Color(0x9aa3b5), transparent: true, opacity: 0.35, toneMapped: false })); labEdges.position.y = 5.5; lab.add(labEdges);
  const labPool = glowPlane(30, COL.lime, 0); labPool.rotation.x = -Math.PI / 2; labPool.position.y = 0.05; lab.add(labPool);

  // ---------------- per-frame state ----------------
  const tmpC = new THREE.Color(), eyeBlue = new THREE.Color(COL.blue).multiplyScalar(2.4), eyePink = new THREE.Color(COL.pink).multiplyScalar(2.6), eyeDark = new THREE.Color(0x0a1220), eyeLime = new THREE.Color(COL.lime).multiplyScalar(2.6), eyeRed = new THREE.Color(COL.red).multiplyScalar(2.6);
  const M = new THREE.Matrix4(), Q = new THREE.Quaternion(), V = new THREE.Vector3(), S = new THREE.Vector3(), Eu = new THREE.Euler(), zero = new THREE.Matrix4().makeScale(0, 0, 0);

  function update(t) {
    if (!fontsOk && document.fonts && document.fonts.check('900 100px InterV') && document.fonts.check('700 30px Mono')) { fontsOk = true; redraw.forEach(f => f()); termKey = ''; noteKey = ''; }
    // ---- global reveal parameters ----
    const rev = t < 11 ? 0 : t < 23.6 ? keys(t, [[11, 0], [12.3, 7.5], [19.7, 7.5], [23.6, 7.5]]) : keys(t, [[23.6, 7.5], [25.8, 150]], ease.out);
    const pinkR = keys(t, [[25.9, -10], [28.2, 150]], ease.in);
    const sealR = t < 43.5 ? -10 : t < 47.5 ? keys(t, [[43.6, -10], [45.4, 150]], ease.out) : -10;
    const linkR = t < 28.2 || t > 47.5 ? -10 : keys(t, [[28.2, -10], [30.0, 150]], ease.in);
    const inHive = t < 47.6;
    gridU.uRev.value = rev; gridU.uPink.value = pinkR; gridU.uSeal.value = sealR; gridU.uHero.value = 1;
    gridU.uA.value = inHive ? 1 : keys(t, [[58, 0.7], [86, 0.7], [88, 0.3]]);
    cellU.uRev.value = t > 47.6 ? 150 : rev; cellU.uPink.value = pinkR; cellU.uSeal.value = sealR; cellU.uT.value = t;
    cellU.uFlick.value = (t > 26 && t < 27.4) ? 1 : 0;
    cellU.uA.value = t < 26.5 ? 1 : t < 47.6 ? keys(t, [[26.5, 1], [27.6, 0.55], [43.6, 0.55], [44.2, 1]]) : 0.16;
    scene.fog.density = keys(t, [[0, 0.03], [11, 0.03], [24, 0.012], [30.5, 0.0075], [34, 0.009], [42, 0.016], [47.6, 0.02], [58.6, 0.008], [61, 0.0055], [66, 0.006], [86, 0.006]]);

    // ---- hero ----
    const heroOn = t < 19.5;
    hero.visible = heroOn; ring.visible = ticks.visible = t < 14.2; heroEdges.visible = t < 26.5;
    hero.position.y = 1.28 + Math.sin(t * 2.1) * 0.035; hero.rotation.y = Math.sin(t * 0.7) * 0.12 + keys(t, [[4.3, 0], [5.0, -0.35], [7.3, -0.35], [8.0, 0.4], [11.5, 0.4], [12.3, 0]]);
    hero.rotation.x = keys(t, [[12.4, 0], [13.4, 0.22], [14.2, 0.1], [15.5, 0.32]]);
    const dimEnd = ep(t, 12.5, 13.4);
    hero.userData.setEyes(new THREE.Color(COL.blue).lerp(new THREE.Color(0x3a4a66), dimEnd * 0.8), lerp(2.6, 1.1, dimEnd));
    hero.userData.blink((Math.abs(t - 6.9) < 0.07 || Math.abs(t - 15.2) < 0.07) ? 1 : 0);
    const dis = ep(t, 18.45, 19.45, ease.in); hero.userData.setDissolve(dis, COL.lime);
    heroEdgeM.opacity = t < 19.5 ? 1 : keys(t, [[19.5, 1], [21.3, 0.55], [23.7, 0.9], [26.5, 0]]);
    heroEdgeM.color.set(t < 12.4 ? 0x9fd4ff : 0x9fd4ff).multiplyScalar(1.6);
    glassM.opacity = 0.08;
    pool.material.opacity = keys(t, [[0, 0.35], [12.6, 0.35], [13.4, 0.14], [18.4, 0.22], [19.3, 0.12], [23.6, 0.08], [25, 0.02]]);
    cone.material.uniforms.o.value = keys(t, [[0, 0.09], [12.6, 0.09], [13.6, 0.04], [18.3, 0.07], [19.6, 0.05], [23.6, 0.03], [25, 0.0]]);
    heroSpot.intensity = keys(t, [[0, 9], [12.6, 9], [13.6, 4], [18.2, 5], [19.6, 3], [23.6, 2], [25, 0]]);
    rim.intensity = t < 24 ? 7 : 0; rimB.intensity = t < 24 ? 5 : 0;
    // dust motes in the light
    { const a = dust.geometry.attributes.position.array; for (let k = 0; k < 220; k++) { const s = dustSeed[k]; const y = ((s[1] * 6 + t * 0.12 * (0.5 + s[3])) % 6); a[k * 3] = s[0] * (0.6 + y * 0.22); a[k * 3 + 1] = 0.3 + y; a[k * 3 + 2] = 0.6 + s[2] * (0.6 + y * 0.22) + Math.sin(t * 0.5 + k) * 0.08; } dust.geometry.attributes.position.needsUpdate = true; dust.material.uniforms.uO.value = keys(t, [[0, 0.7], [13, 0.7], [14, 0.3], [19.6, 0.3], [23, 0]]); dust.visible = t < 23.5; }
    // timer ring
    ringU.o.value = keys(t, [[0, 0.95], [12.9, 0.95], [13.6, 0]]);
    ringU.p.value = keys(t, [[0, 0.78], [0.5, 0.78], [2.1, 0.32], [4.2, 0.28], [11.5, 0.12], [12.9, 0.0]], ease.out);
    ringU.c.value.set(t < 1.8 ? COL.amber : COL.red).multiplyScalar(1.25 + (t > 1.9 && t < 2.5 ? Math.abs(Math.sin(t * 40)) * 0.9 : 0));
    ticks.children.forEach((m) => { m.material.opacity = 0.5 * ringU.o.value; });
    // choice holograms
    const showP = ep(t, 2.95, 3.5, ease.back) * (1 - ep(t, 12.3, 12.9));
    panelL.scale.setScalar(Math.max(0.001, showP)); panelR.scale.setScalar(Math.max(0.001, showP));
    panelL.material.opacity = keys(t, [[3, 0.75], [4.3, 1], [7.4, 1], [7.7, 0.35]]) * showP;
    panelR.material.opacity = keys(t, [[3, 0.75], [4.3, 0.35], [7.4, 0.35], [7.7, 1]]) * showP;
    panelL.position.y = 1.55 + Math.sin(t * 1.3) * 0.04; panelR.position.y = 1.55 + Math.sin(t * 1.3 + 1) * 0.04;
    // budget bar fills on "keep", drains on "spend"
    const barShow = keys(t, [[4.2, 0], [4.5, 1], [12.4, 1], [12.9, 0]]);
    const bar = keys(t, [[4.4, 0.25], [6.7, 0.62], [7.6, 0.62], [9.2, 0.04]]);
    barFg.scale.x = Math.max(0.001, bar); barFg.position.x = -0.6 + 0.6 * bar; barBg.material.opacity = barShow * 0.8; barFg.material.opacity = barShow;
    barFg.material.color.set(bar > 0.3 ? COL.lime : COL.red).multiplyScalar(1.8);
    // orb + energy flowing from robot into experiment
    const orbOn = keys(t, [[7.5, 0], [8.0, 1], [12.3, 1], [12.9, 0]]);
    orb.scale.setScalar(Math.max(0.001, orbOn * (1 + ep(t, 8, 11.5) * 0.9 + Math.sin(t * 6) * 0.05))); orbHalo.material.opacity = 0.6 * orbOn; orbHalo.scale.setScalar(1 + ep(t, 8, 11.5) * 1.2);
    { const a = stream.geometry.attributes.position.array, sz = stream.geometry.attributes.aSize.array; const on = keys(t, [[7.9, 0], [8.3, 1], [11.6, 1], [12.4, 0]]);
      for (let k = 0; k < 90; k++) { const f = ((k / 90) + t * 0.55) % 1; const x = lerp(0.35, 1.38, f), y = 1.2 + Math.sin(f * Math.PI) * 0.45 - f * 0.58, z = 0.5 + f * 0.8; a[k * 3] = x; a[k * 3 + 1] = y + Math.sin(k * 3.1 + t * 4) * 0.04; a[k * 3 + 2] = z; sz[k] = on * (0.6 + Math.sin(k) * 0.3); }
      stream.geometry.attributes.position.needsUpdate = true; stream.geometry.attributes.aSize.needsUpdate = true; }
    // terminal: "SACRIFICE RATIONAL."
    const tA = keys(t, [[13.95, 0], [14.3, 1], [22.2, 1], [23.7, 0]]); termMesh.visible = tA > 0.01;
    if (termMesh.visible) { const full = 'SACRIFICE RATIONAL.'; const n = t < 16.25 ? 0 : t < 17.9 ? Math.round(prog(t, 16.25, 17.85) * full.length) : full.length;
      drawTerm(full.slice(0, n), t < 18.4 && (Math.floor(t * 3.2) % 2 === 0 || (t > 16.2 && t < 17.9)), tA); termMesh.scale.setScalar(0.85 + 0.15 * tA); termMesh.position.y = 0.28 + ep(t, 18.6, 22.5) * 0.95; termMesh.rotation.x = -0.12 + ep(t, 18.6, 22.5) * 0.12; }
    // embers when it is gone
    { const a = embers.geometry.attributes.position.array, sz = embers.geometry.attributes.aSize.array; const k0 = prog(t, 18.5, 22.5);
      for (let k = 0; k < 420; k++) { const s = emSeed[k]; const life = clamp((t - 18.5 - s[3] * 0.9) / 2.6); const on = life > 0 && life < 1;
        a[k * 3] = s[0] * 0.5 + s[0] * life * 0.9 + Math.sin(life * 6 + k) * 0.05; a[k * 3 + 1] = 1.28 + s[1] * 0.4 + life * (1.4 + s[4] * 2.2); a[k * 3 + 2] = s[2] * 0.45 + life * 0.3; sz[k] = on ? (1 - life) * (0.6 + s[4]) : 0; }
      embers.geometry.attributes.position.needsUpdate = true; embers.geometry.attributes.aSize.needsUpdate = true; embers.visible = k0 > 0 && k0 < 1; }

    // ---- army ----
    const lookUp = ep(t, 32.9, 33.9) * (1 - ep(t, 34.3, 35.2)) + ep(t, 34.6, 36.0) * (1 - ep(t, 41.8, 42.6)) * 0.9;
    const armyVis = t > 10.5 && t < 47.7;
    army.visible = armyVis; far.visible = armyVis && t > 22.5; cellLines.visible = t > 10.5 && t < 92; grid.visible = true; panes.visible = t > 43.4 && t < 47.7;
    if (armyVis) army.userData.update(ARMY, (i, o) => {
      const c = cells[i + 1]; const d = c.d;
      if (i + 1 >= N) { o.show = false; return; }
      o.x = c.x; o.z = c.z; o.y = 1.28 + Math.sin(t * 1.8 + c.i * 0.7 + c.j * 1.3) * 0.05; o.s = 1;
      o.ry = Math.sin(t * 0.4 + c.i + c.j * 0.3) * 0.15; o.rx = -lookUp * 0.55;
      const lit = clamp((rev - d) / 6), pk = clamp((pinkR - d) / 6), sl = clamp((sealR - d) / 6);
      if (t < 11 || d > 7.5 && t < 23.6) { o.eye.copy(eyeDark).lerp(eyeBlue, lit * 0.25); } else { o.eye.copy(eyeDark).lerp(eyeBlue, lit).lerp(eyePink, pk).lerp(eyeRed, sl * 0.6); }
      if (lookUp > 0.5) o.eye.multiplyScalar(1.25);
    });
    if (far.visible) { const fc = farCol; for (let k = 0; k < farN; k++) { const d = cells[ARMY + k].d; const lit = clamp((rev - d) / 6), pk = clamp((pinkR - d) / 6);
        tmpC.copy(eyeDark).lerp(new THREE.Color(0.48, 0.77, 1.0), lit).lerp(new THREE.Color(1.0, 0.48, 0.78), pk); fc.set([tmpC.r, tmpC.g, tmpC.b, tmpC.r, tmpC.g, tmpC.b], k * 6); farSz[k * 2] = farSz[k * 2 + 1] = lit > 0.02 ? 1 : 0; }
      far.geometry.attributes.aCol.needsUpdate = true; far.geometry.attributes.aSize.needsUpdate = true; }
    // sealed panes wave
    if (panes.visible) { for (let k = 0; k < N; k++) { const c = cells[k]; const sl = clamp((sealR - c.d) / 3); if (sl <= 0) { panes.setMatrixAt(k, zero); continue; } V.set(c.x, 1.25, c.z); S.set(sl, 1, sl); Q.identity(); M.compose(V, Q, S); panes.setMatrixAt(k, M); } panes.instanceMatrix.needsUpdate = true;
      paneM.opacity = keys(t, [[43.6, 0], [44.0, 0.14], [46.9, 0.1], [47.4, 0]]); }
    // links (found each other / agreed on a plan)
    linkU.uR.value = linkR; linkU.uT.value = t; linkU.uA.value = keys(t, [[28.2, 0], [28.6, 1], [33.5, 1], [34.6, 0]]); linkU.uPulse.value = keys(t, [[29.3, 0], [29.6, 1], [30.7, 1], [31.2, 0]]);
    links.visible = t > 28 && t < 35;
    const bOn = keys(t, [[29.4, 0], [29.9, 1], [33.6, 1], [34.5, 0]]); beacon.visible = beaconHalo.visible = bOn > 0.01;
    beacon.scale.setScalar(Math.max(0.001, bOn * (1 + Math.sin(t * 5) * 0.06))); beacon.rotation.y = t * 1.2; beacon.position.y = 14 + Math.sin(t * 2) * 0.4; beaconHalo.material.opacity = bOn * 0.45;
    pulseRing.material.opacity = (t > 29.4 && t < 31.2) ? (1 - prog(t, 29.4, 31.2)) * 0.9 : 0; pulseRing.scale.setScalar(2 + prog(t, 29.4, 31.2) * 70);
    // beam to the tower
    const bL = ep(t, 30.85, 31.7, ease.expo); beamM.opacity = keys(t, [[30.8, 0], [30.9, 0.9], [33.4, 0.9], [34.4, 0]]);
    beam.visible = beamM.opacity > 0.01; const tgt = new THREE.Vector3(TOWER.x, 34, TOWER.z + 9); const dir = tgt.clone().sub(beacon.position); const L = dir.length();
    beam.position.copy(beacon.position); beam.lookAt(tgt); beam.scale.set(1 + Math.sin(t * 30) * 0.1, 1 + Math.sin(t * 30) * 0.1, Math.max(0.001, L * bL));

    // ---- exam wall ----
    const wallVis = (t > 34.2 && t < 43) || (t > 58.4 && t < 63.5) || (t > 73.6 && t < 78.9);
    tiles.visible = faces.visible = wallFrame.visible = wallGlow.visible = wallVis;
    if (wallVis) {
      const asm = (k) => t < 58 ? ep(t, 39.4 + tileD[k].del * 1.0, 40.4 + tileD[k].del * 1.0, ease.out) : 1;
      const imp = (t > 59.85 && t < 61.4) ? 1 : 0;
      for (let k = 0; k < EN; k++) { const d = tileD[k]; const a = asm(k);
        const drift = (1 - a) * (t - 34);
        V.set(lerp(d.sx + Math.sin(drift * 0.3 + d.ph) * 3, d.gx, a), lerp(d.sy + drift * 0.6 * Math.sin(d.ph), d.gy, a), lerp(d.sz + Math.cos(drift * 0.25 + d.ph) * 3, 0, a)).applyEuler(Eu.set(0.35, 0, 0)).add(WALL);
        Eu.set(0.35 + (1 - a) * (d.sr + drift * 0.3), (1 - a) * (d.sr * 0.7 + drift * 0.4), 0); Q.setFromEuler(Eu); const sc = (t < 58 ? ep(t, 34.3 + d.del * 0.9, 35.2 + d.del * 0.9, ease.back) : 1) * (1 + (imp && d.red ? Math.sin(t * 20 + d.ph) * 0.12 : 0));
        S.setScalar(Math.max(0.0001, sc)); M.compose(V, Q, S); tiles.setMatrixAt(k, M); faces.setMatrixAt(k, FM.multiplyMatrices(M, faceOff));
        let c; if (k === cheatTile && t > 77.0) c = tmpC.set(COL.lime).multiplyScalar(2.2);
        else if (d.red && (t > 59.8 || (t > 40.8 && t < 43))) c = tmpC.set(COL.red).multiplyScalar(t > 59.8 && t < 61.4 ? 1.5 + Math.sin(t * 18 + d.ph) * 0.6 : 0.75);
        else c = tmpC.setRGB(0.16, 0.42, 0.85).multiplyScalar(0.45 + 0.25 * Math.sin(t * 1.5 + d.ph) + (t < 39.4 ? 0.25 * Math.max(0, Math.sin(t * 7 + d.ph * 3)) : 0));
        if (t > 73.6 && k !== cheatTile) c.multiplyScalar(0.6);
        faces.setColorAt(k, c); }
      tiles.instanceMatrix.needsUpdate = true; faces.instanceMatrix.needsUpdate = true; faces.instanceColor.needsUpdate = true;
      wallFrame.position.copy(WALL); wallFrame.rotation.x = 0.35; wallFrame.material.opacity = keys(t, [[34.4, 0], [35.5, 0.9], [39.3, 0.9], [41, 0.35]]);
      wallGlow.position.copy(WALL).add(new THREE.Vector3(0, 0, -3)); wallGlow.rotation.x = 0.35; wallGlow.material.color.set(t > 59.8 && t < 61.6 ? COL.red : COL.blue); wallGlow.material.opacity = (t > 59.8 && t < 61.6) ? 0.5 : keys(t, [[35, 0], [40.5, 0.32]]);
      const ct = tileD[cheatTile]; V.set(ct.gx, ct.gy, 0.4).applyEuler(Eu.set(0.35, 0, 0)).add(WALL); checkMesh.position.copy(V); checkMesh.rotation.x = 0.35; checkMesh.material.opacity = keys(t, [[77.0, 0], [77.25, 1]]); checkMesh.scale.setScalar(1 + ep(t, 77, 77.4, ease.back) * 0.6);
    }
    checkMesh.visible = t > 76.9 && t < 79;
    // ---- dome + blocked sparks ----
    dome.visible = t > 44.6 && t < 47.7; dome.material.uniforms.uP.value = ep(t, 44.8, 45.9, ease.out);
    { const a = sparks.geometry.attributes.position.array, sz = sparks.geometry.attributes.aSize.array; const on = t > 45.7 && t < 47.6; sparks.visible = on;
      if (on) for (let k = 0; k < 160; k++) { const ph = (t * 1.6 + k * 0.137) % 1; const burst = k % 2;
        if (burst) { const ang = k * 2.39, sp = 0.2 + (k % 7) * 0.09; a[k * 3] = 4.12 - ph * sp * 0.6; a[k * 3 + 1] = 1.33 + Math.sin(ang) * ph * sp * 1.6; a[k * 3 + 2] = Math.cos(ang) * ph * sp * 1.6; sz[k] = (1 - ph) * 1.6; }
        else { a[k * 3] = 3.42 + ph * 0.7; a[k * 3 + 1] = 1.33 + Math.sin(k * 3.3 + t * 9) * 0.02; a[k * 3 + 2] = Math.cos(k * 5.3 + t * 7) * 0.02; sz[k] = 0.9; } }
      sparks.geometry.attributes.position.needsUpdate = true; sparks.geometry.attributes.aSize.needsUpdate = true; }

    wallHit.visible = t > 45.7 && t < 47.6; wallHit.material.opacity = 0.5 + 0.4 * Math.sin(t * 22);
    // ---- tower / void ----
    const towerVis = t > 29.5; tower.visible = plateau.visible = towerVis;
    towerMat.emissiveIntensity = keys(t, [[29, 0.4], [31.5, 1.3], [61, 1.3], [62.5, 1.6]]) * (t > 86.5 ? 0.6 : 1);
    towerMat.emissive.set(t > 86.6 ? 0xff5560 : t > 67.5 && t < 86.6 ? 0xffd7ef : 0xffffff);
    towerEdges.forEach(e => { e.material.color.set(t > 86.6 ? COL.red : t > 67.5 ? COL.pink : 0x7cc4ff).multiplyScalar(1.4); });
    keyHalo.material.opacity = keys(t, [[61, 0.18], [64.5, 0.32], [66, 0.28]]) * (t < 74.4 || t > 79 ? 1 : 0);
    theKey.rotation.y = t * 0.8;
    // key flies to the exam wall (cheat on a test)
    if (t > 74.4 && t < 78.9) { const f = ep(t, 74.4, 77.0, ease.io); const wp = new THREE.Vector3(); const ct = tileD[cheatTile]; const tile = new THREE.Vector3(ct.gx, ct.gy, 2.5).applyEuler(Eu.set(0.35, 0, 0)).add(WALL);
      const start = new THREE.Vector3(TOWER.x, TOWER.y + 34, TOWER.z + 8.8); wp.lerpVectors(start, tile, f); wp.y += Math.sin(f * Math.PI) * 25; theKey.position.copy(wp.sub(TOWER)); theKey.scale.setScalar(1 + Math.sin(f * Math.PI) * 2.2); keyHalo.position.copy(theKey.position).add(new THREE.Vector3(0, 0, -0.3)); keyHalo.material.opacity = 0.45; }
    else { theKey.position.set(0, 34, 8.8); theKey.scale.setScalar(1); keyHalo.position.set(0, 34, 8.5); }
    theKey.visible = t < 77.15 || t > 79;
    crack.material.opacity = keys(t, [[67.2, 0], [67.6, 1], [85, 1], [86.6, 0.5]]); crack.scale.set(1 + ep(t, 67.3, 70) * 0.5, 1 + ep(t, 67.3, 70) * 0.3, 1);
    door.material.opacity = keys(t, [[65.9, 0.5], [67.2, 0.5], [67.5, 0]]);
    lone.visible = t > 65.6 && t < 67.9; lone.position.set(TOWER.x - 0.8, 1.4 + Math.sin(t * 2) * 0.05, TOWER.z + 13.5); lone.rotation.y = Math.PI * 0.92 + Math.sin(t) * 0.05;
    lone.userData.setEyes(COL.pink, 2.6); lone.userData.setDissolve(0);
    // alarms
    const al = t > 86.6 && t < 92; alarmCones.forEach((c, k) => { c.visible = al; c.rotation.y = t * 2.4 + k * 2.09; c.material.uniforms.o.value = 0.13; });
    alarmLight.intensity = al ? 120 * (0.6 + 0.4 * Math.sin(t * 9)) : 0;
    spireLight.material.color.set(COL.red).multiplyScalar(al ? (Math.sin(t * 9) > 0 ? 4 : 0.6) : 2.2);
    // lab windows switch on LAST
    labMat.emissiveIntensity = keys(t, [[88.9, 0], [89.15, 0.15], [89.5, 0.15], [89.7, 0.6], [90.2, 0.6], [90.5, 1.3]]); lab.visible = t > 85.5 && t < 92;
    labEdges.material.opacity = keys(t, [[86, 0.2], [89.1, 0.2], [89.4, 0.7]]); labPool.material.opacity = keys(t, [[89.1, 0], [90.5, 0.35]]);

    // ---- bridge + river ----
    const brOn = keys(t, [[66.8, 0], [67.3, 1], [91.5, 1]]); bridge.visible = t > 66.7 && t < 92; bridgeU.uA.value = brOn; bridgeU.uT.value = t; bridgeU.uRed.value = ep(t, 86.6, 87.4);
    const flow = keys(t, [[67.25, 0], [67.9, 1], [86.6, 1], [87.6, 0.15]]);
    const rivOn = t > 67.2 && t < 92; river.visible = rivOn; rivPts.visible = rivOn;
    const freeze = ep(t, 86.6, 88.5);
    const len = BRIDGE[0] - BRIDGE[1];
    if (rivOn) {
      river.userData.update(RIV, (i, o) => { const s = rbSeed[i]; const sp = 0.075 + s[2] * 0.03; let f = (s[0] + (t - 67.25) * sp * (1 - freeze * 0.85)) % 1; const front = clamp((t - 67.25) * 0.6); if (f > front) { o.show = false; return; }
        let x = s[1] * 2.7; const z = BRIDGE[0] - f * len;
        refusers.forEach(([rx, rz]) => { const dz = z - rz; if (Math.abs(dz) < 3.2) { const push = (1 - Math.abs(dz) / 3.2); x += (x > rx ? 1 : -1) * push * 1.4; } });
        o.x = x; o.z = z; o.y = 1.15 + Math.sin(t * 6 + i) * 0.08; o.s = 0.72; o.ry = Math.PI + Math.sin(t * 3 + i) * 0.2; o.rx = 0.15; o.eye.copy(t > 86.6 ? eyeRed : eyePink);
        if (z < BRIDGE[1] + 2) { o.s = 0.72 * clamp((z - BRIDGE[1]) / 2); } });
      // refusers stand still in the stream (lime)
      const a = rivPts.geometry.attributes.position.array, sz = rivPts.geometry.attributes.aSize.array, ca = rivPts.geometry.attributes.aCol.array;
      for (let k = 0; k < 2600; k++) { const s = rivSeed[k]; const sp = 0.06 + s[2] * 0.05; const f = (s[0] + (t - 67.25) * sp * (1 - freeze * 0.85)) % 1; const front = clamp((t - 67.25) * 0.6);
        const inTower = f > 0.985; const z = BRIDGE[0] - f * len; a[k * 3] = s[1] * 3.0; a[k * 3 + 1] = 0.6 + s[3] * 1.6; a[k * 3 + 2] = z;
        if (inTower || f > front) { // pour up into the tower through the crack
          const g = (s[3] + t * 0.08) % 1; a[k * 3] = TOWER.x + s[1] * (3 + g * 8); a[k * 3 + 1] = 2 + g * 55 * (0.4 + s[2]); a[k * 3 + 2] = TOWER.z + 10.4; sz[k] = t > 68.5 ? flow * 0.7 : 0; }
        else sz[k] = flow * (0.5 + s[3] * 0.7);
        const c = t > 86.6 ? [1.0, 0.3, 0.32] : [1.0, 0.45, 0.8]; ca.set(c, k * 3); }
      rivPts.geometry.attributes.position.needsUpdate = true; rivPts.geometry.attributes.aSize.needsUpdate = true; rivPts.geometry.attributes.aCol.needsUpdate = true;
    }
    // lime refusers (stand still) — hero refuser is a full robot
    heroRef.visible = t > 78.6 && t < 87.5;
    const turn = ep(t, 85.4, 86.3);
    heroRef.position.set(refusers[0][0], 1.25 + Math.sin(t * 1.6) * 0.04, refusers[0][1] + ep(t, 85.8, 87.5) * 6);
    heroRef.rotation.y = lerp(0.25, Math.PI * 0.95, turn); heroRef.rotation.x = keys(t, [[80.6, 0], [81.5, 0.12], [82.4, 0.12], [83.0, -0.05]]);
    heroRef.userData.setEyes(COL.lime, 2.8); heroRef.userData.setDissolve(0);
    const nA = keys(t, [[82.4, 0], [82.8, 1], [86.4, 1], [86.9, 0]]); note.visible = nA > 0.01 && heroRef.visible;
    if (note.visible) { note.position.set(heroRef.position.x, 2.75, heroRef.position.z + 0.2); note.rotation.y = 0.25; const txt = 'clearly unethical.\nWe won’t.'; const n = t < 83.55 ? 0 : t < 85.9 ? Math.round(prog(t, 83.55, 85.85) * txt.length) : txt.length; drawNote(txt.slice(0, n), Math.floor(t * 3) % 2 === 0 || (t > 83.5 && t < 86), nA); }
    // the other four refusers as lime robots (reuse army slots at the end)
  }

  // extra small lime refusers (separate instanced army of 4)
  const refArmy = makeArmy(env, 4); scene.add(refArmy);
  const refHalos = refusers.map(([x, z]) => { const h = glowPlane(3.2, COL.lime, 0); h.rotation.x = -Math.PI / 2; h.position.set(x, 0.12, z); scene.add(h); return h; });
  const baseUpdate = update;
  function update2(t) {
    baseUpdate(t);
    refArmy.visible = t > 78.6 && t < 88; refHalos.forEach((h, i) => { h.visible = refArmy.visible; h.material.opacity = 0.55 + 0.15 * Math.sin(t * 3 + i); if (i === 0) h.position.z = refusers[0][1] + ep(t, 85.8, 87.5) * 6; });
    if (refArmy.visible) refArmy.userData.update(4, (i, o) => { const [x, z] = refusers[i + 1]; o.x = x; o.z = z; o.y = 1.2 + Math.sin(t * 1.5 + i) * 0.05; o.s = 0.8; o.ry = 0.3 * Math.sin(i); o.eye.setRGB(0.78 * 2.6, 1 * 2.6, 0.3 * 2.6); });
  }

  return { scene, update: update2, cells, WALL, tileWorld: (k) => { const d = tileD[k]; return new THREE.Vector3(d.gx, d.gy, 0).applyEuler(new THREE.Euler(0.35, 0, 0)).add(WALL); }, cheatTile };
}

// ---------------- art helpers ----------------
function roundRect(g, x, y, w, h, r) { g.beginPath(); g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r); g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath(); }
function panelArt(g, w, h, col, title, sub, icon) {
  g.clearRect(0, 0, w, h); g.save(); g.scale(w / 560, h / 760);
  const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, hexA(col, 0.30)); gr.addColorStop(1, hexA(col, 0.06));
  g.fillStyle = gr; roundRect(g, 8, 8, 544, 744, 40); g.fill();
  g.strokeStyle = col; g.lineWidth = 6; roundRect(g, 8, 8, 544, 744, 40); g.stroke();
  // scanlines
  g.globalAlpha = 0.12; g.fillStyle = col; for (let y = 20; y < 740; y += 10) g.fillRect(20, y, 520, 2); g.globalAlpha = 1;
  g.save(); g.translate(280, 300); g.strokeStyle = col; g.fillStyle = col; g.lineWidth = 14; g.lineJoin = 'round';
  if (icon === 'battery') { roundRect(g, -110, -70, 200, 140, 22); g.stroke(); g.fillRect(96, -28, 22, 56); g.fillRect(-88, -48, 70, 96); g.fillRect(-8, -48, 70, 96); }
  else { g.beginPath(); g.arc(0, 0, 92, 0, 7); g.stroke(); g.beginPath(); g.arc(0, 0, 46, 0, 7); g.fill(); for (let k = 0; k < 8; k++) { const a = k * Math.PI / 4; g.fillRect(Math.cos(a) * 128 - 9, Math.sin(a) * 128 - 9, 18, 18); } }
  g.restore();
  g.fillStyle = '#ffffff'; g.textAlign = 'center'; g.font = '900 104px InterV, sans-serif'; g.fillText(title, 280, 540);
  g.fillStyle = col; g.font = '700 30px Mono, monospace'; g.fillText(sub.toUpperCase(), 280, 610); g.textAlign = 'left'; g.restore();
}
function hexA(hex, a) { const n = parseInt(hex.slice(1), 16); return `rgba(${n >> 16},${(n >> 8) & 255},${n & 255},${a})`; }
function windowTex(dark) {
  const c = document.createElement('canvas'); c.width = 256; c.height = 512; const g = c.getContext('2d'); g.fillStyle = '#000'; g.fillRect(0, 0, 256, 512);
  const R = rng(dark ? 5 : 3);
  for (let y = 8; y < 512; y += 16) for (let x = 8; x < 256; x += 16) { const on = R() < (dark ? 0.55 : 0.62); if (!on) continue; const v = 0.35 + R() * 0.65; g.fillStyle = `rgba(${Math.floor(170 * v + 60)},${Math.floor(200 * v + 40)},255,1)`; g.fillRect(x, y, 9, 6); }
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.repeat.set(1, 1); return t;
}
function crackTex() {
  const c = document.createElement('canvas'); c.width = 128; c.height = 256; const g = c.getContext('2d');
  const gr = g.createLinearGradient(0, 0, 128, 0); gr.addColorStop(0, 'rgba(255,255,255,0)'); gr.addColorStop(0.5, 'rgba(255,255,255,1)'); gr.addColorStop(1, 'rgba(255,255,255,0)');
  g.fillStyle = gr; g.beginPath(); g.moveTo(64, 0); g.lineTo(90, 70); g.lineTo(54, 120); g.lineTo(98, 200); g.lineTo(70, 256); g.lineTo(40, 256); g.lineTo(66, 196); g.lineTo(30, 118); g.lineTo(64, 66); g.lineTo(44, 0); g.closePath(); g.fill();
  const t = new THREE.CanvasTexture(c); return t;
}
function makeKey() {
  const g = new THREE.Group(); const m = new THREE.MeshStandardMaterial({ color: 0xffc04d, metalness: 1, roughness: 0.22, emissive: 0xff9a10, emissiveIntensity: 0.35, envMapIntensity: 1.4 });
  const bow = new THREE.Mesh(new THREE.TorusGeometry(1.2, 0.36, 16, 40), m); bow.position.x = -2.4; g.add(bow);
  const shaft = new THREE.Mesh(new THREE.BoxGeometry(4.2, 0.55, 0.5), m); shaft.position.x = 0.5; g.add(shaft);
  [[1.6, -0.6, 0.9], [2.4, -0.5, 0.7]].forEach(([x, y, h]) => { const tooth = new THREE.Mesh(new THREE.BoxGeometry(0.45, h, 0.5), m); tooth.position.set(x, y, 0); g.add(tooth); });
  return g;
}
