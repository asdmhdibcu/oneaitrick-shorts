// GALLERY — Charlotte Brontë's portrait in a gilded oval frame; a railway share slides out (hook),
// and returns in 1849, greyed, the share cracking from £120 to £20.
import { THREE, rng, clamp, prog, ease, ep, keys, lerp, glowPlane, lightCone, makePoints, textCanvas } from './core.js';
import { imgTex, certCanvas, noiseTex, SERIF } from './kit.js';

export function makeGallery(env, IMG) {
  const scene = new THREE.Scene(); scene.background = new THREE.Color(0x0a0807); scene.fog = new THREE.FogExp2(0x0a0807, 0.045);
  scene.add(new THREE.HemisphereLight(0x8a7a6a, 0x120d0a, 0.35));
  // wall
  const plaster = noiseTex(1024, 1024, '#4a3b30', [[900, 'rgba(20,12,6,A)', 4, 40, 0.02, 0.07], [600, 'rgba(255,230,200,A)', 2, 14, 0.02, 0.05]], 3, [3, 3]);
  const wall = new THREE.Mesh(new THREE.PlaneGeometry(40, 26), new THREE.MeshStandardMaterial({ map: plaster, color: 0x9a8676, roughness: 0.95, metalness: 0, envMap: env, envMapIntensity: 0.15 }));
  wall.position.set(0, 0, -0.02); scene.add(wall);
  const rail = new THREE.Mesh(new THREE.BoxGeometry(40, 0.12, 0.08), new THREE.MeshStandardMaterial({ color: 0x3a2a1c, roughness: 0.6, envMap: env, envMapIntensity: 0.3 })); rail.position.set(0, -2.55, 0.03); scene.add(rail);
  const wains = new THREE.Mesh(new THREE.PlaneGeometry(40, 8), new THREE.MeshStandardMaterial({ color: 0x241a13, roughness: 0.8, envMap: env, envMapIntensity: 0.2 })); wains.position.set(0, -6.6, 0.0); scene.add(wains);

  // portrait (oval mask, desaturation for 1849)
  const PW = 1.6, PH = 1.6 * 1144 / 800;
  const pu = { map: { value: imgTex(IMG.charlotte) }, uSat: { value: 1 }, uCold: { value: 0 }, uBright: { value: 1 } };
  const portrait = new THREE.Mesh(new THREE.PlaneGeometry(PW, PH), new THREE.ShaderMaterial({ uniforms: pu, transparent: true, toneMapped: false,
    vertexShader: `varying vec2 vUv; void main(){ vUv=uv; gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.); }`,
    fragmentShader: `uniform sampler2D map; uniform float uSat,uCold,uBright; varying vec2 vUv;
      void main(){ vec2 q=(vUv-vec2(.5,.5))/vec2(.47,.47); float r=length(q); float a=smoothstep(1.,.97,r);
        vec3 c=texture2D(map,vUv).rgb; float l=dot(c,vec3(.299,.587,.114)); c=mix(vec3(l),c,uSat);
        c*=mix(vec3(1.02,.98,.9),vec3(.78,.86,1.0),uCold);
        float lit=mix(1.05,.55,smoothstep(.2,1.,length(vUv-vec2(.52,.66))*1.6));
        gl_FragColor=vec4(c*lit*uBright*.92,a); }` }));
  portrait.position.set(0, 0, 0.12); scene.add(portrait);
  const back = new THREE.Mesh(new THREE.CircleGeometry(1, 64), new THREE.MeshStandardMaterial({ color: 0x1a0f0c, roughness: 0.9 })); back.scale.set(0.82, 1.14, 1); back.position.set(0, 0, 0.1); scene.add(back);
  const gold = new THREE.MeshStandardMaterial({ color: 0xc89a3e, metalness: 1, roughness: 0.3, envMap: env, envMapIntensity: 1.25 });
  const ring1 = new THREE.Mesh(new THREE.TorusGeometry(1, 0.075, 20, 120), gold); ring1.scale.set(0.83, 1.15, 1.6); ring1.position.z = 0.13; scene.add(ring1);
  const ring2 = new THREE.Mesh(new THREE.TorusGeometry(1, 0.025, 12, 120), gold); ring2.scale.set(0.765, 1.08, 1); ring2.position.z = 0.16; scene.add(ring2);
  const ring3 = new THREE.Mesh(new THREE.TorusGeometry(1, 0.03, 12, 120), gold); ring3.scale.set(0.93, 1.27, 1); ring3.position.z = 0.11; scene.add(ring3);
  // beads on the outer ring
  const bead = new THREE.InstancedMesh(new THREE.SphereGeometry(0.035, 10, 8), gold, 64); const mm = new THREE.Matrix4();
  for (let k = 0; k < 64; k++) { const a = k / 64 * Math.PI * 2; mm.makeTranslation(Math.cos(a) * 0.885, Math.sin(a) * 1.215, 0.16); bead.setMatrixAt(k, mm); } scene.add(bead);
  // plaque
  const plq = new THREE.Mesh(new THREE.BoxGeometry(1.3, 0.3, 0.04), gold); plq.position.set(0, -1.62, 0.06); scene.add(plq);
  const pt = textCanvas(1024, 236); pt.g.fillStyle = '#d8b25a'; pt.g.fillRect(0, 0, 1024, 236);
  pt.g.fillStyle = '#3a2610'; pt.g.textAlign = 'center'; pt.g.font = `700 92px ${SERIF}`; pt.g.fillText('CHARLOTTE BRONTË', 512, 118); pt.g.font = `italic 58px ${SERIF}`; pt.g.fillText('novelist · 1816–1855', 512, 196); pt.tex.needsUpdate = true;
  const plqT = new THREE.Mesh(new THREE.PlaneGeometry(1.22, 0.28), new THREE.MeshStandardMaterial({ map: pt.tex, metalness: 0.6, roughness: 0.4, envMap: env, envMapIntensity: 0.8 })); plqT.position.set(0, -1.62, 0.081); scene.add(plqT);

  // light: warm spot from above + visible beam + dust
  const spot = new THREE.SpotLight(0xffd6a0, 70, 22, 0.55, 0.65, 1.6); spot.position.set(0.4, 5.5, 4.2); spot.target.position.set(0, -0.2, 0); scene.add(spot, spot.target);
  const fill = new THREE.PointLight(0x9fb4ff, 3, 12, 2); fill.position.set(-3, -1, 4); scene.add(fill);
  const cone = lightCone(7.5, 2.4, 0xffd6a0, 0.07); cone.position.set(0.4, 5.6, 2.2); cone.rotation.x = 0.55; scene.add(cone);
  const dust = makePoints(220, 0xffe2b0, 0.03, 0.55); scene.add(dust); const R = rng(11); const ds = Array.from({ length: 220 }, () => [R() * 4 - 2, R() * 5 - 2.5, R() * 3 + 0.3, R() * 6.28, 0.3 + R() * 0.7]);

  // certificates: hook (£50 + AI glitch) and 1849 (£120 -> cracked £20)
  const c50 = certCanvas({ value: '£50' }), cAI = certCanvas({ value: '£50', glitch: true });
  const c120 = certCanvas({ value: '£120' }), c20 = certCanvas({ value: '£20', valueColor: '#8a1414', cracked: true });
  const certMat = (tex) => new THREE.MeshStandardMaterial({ map: tex, roughness: 0.88, metalness: 0, envMap: env, envMapIntensity: 0.25, transparent: true, side: THREE.DoubleSide });
  const cert = new THREE.Group(); scene.add(cert);
  const cA = new THREE.Mesh(new THREE.PlaneGeometry(1.5, 1.0, 12, 8), certMat(c50.tex)); cert.add(cA);
  const cB = new THREE.Mesh(new THREE.PlaneGeometry(1.5, 1.0, 12, 8), certMat(cAI.tex)); cB.position.z = 0.002; cert.add(cB);
  const certB = new THREE.Group(); scene.add(certB);
  const cC = new THREE.Mesh(new THREE.PlaneGeometry(1.5, 1.0, 12, 8), certMat(c120.tex)); certB.add(cC);
  const cD = new THREE.Mesh(new THREE.PlaneGeometry(1.5, 1.0, 12, 8), certMat(c20.tex)); cD.position.z = 0.002; certB.add(cD);
  const certShadow = (g) => { const s = new THREE.Mesh(new THREE.PlaneGeometry(1.6, 1.1), new THREE.MeshBasicMaterial({ color: 0, transparent: true, opacity: 0.35, depthWrite: false })); s.position.set(0.06, -0.06, -0.02); g.add(s); };
  certShadow(cert); certShadow(certB);

  function update(t) {
    // portrait grade: 1845 warm / 1849 grey + cold
    const late = t > 30;
    pu.uSat.value = late ? lerp(0.55, 0.08, ep(t, 33.9, 35.0)) : 1; pu.uCold.value = late ? lerp(0.4, 1, ep(t, 33.9, 35.0)) : 0;
    spot.intensity = late ? 38 : 70; spot.color.set(late ? 0xc8d6ff : 0xffd6a0); cone.material.uniforms.c.value.set(late ? 0xb8c8ff : 0xffd6a0);
    // hook certificate: slides from behind the frame (1.0 -> 2.3), glitches to "AI SHARE" on "AI" (2.86)
    const sl = ep(t, 0.95, 2.35, ease.out);
    cert.visible = !late;
    cert.position.set(lerp(0.1, 0.42, sl), lerp(-0.2, -0.98, sl), lerp(0.04, 0.62, sl));
    cert.rotation.set(lerp(0, -0.08, sl), lerp(0, -0.18, sl), lerp(0, -0.07, sl) + Math.sin(t * 1.3) * 0.012);
    const gOn = t > 2.86 && t < 5.4; const flick = t > 2.86 && t < 3.25 && Math.floor(t * 30) % 3 === 0;
    cB.material.opacity = gOn && !flick ? 1 : 0; cA.material.opacity = 1;
    cB.position.x = gOn ? (Math.floor(t * 30) % 4 === 0 && t < 3.4 ? 0.03 : 0) : 0;
    // 1849 certificate: in front of the portrait, cracks from £120 to £20 on "twenty" (36.69)
    certB.visible = late;
    const ent = ep(t, 33.95, 34.7, ease.out);
    certB.position.set(lerp(0.5, 0.3, ent), lerp(-1.7, -0.98, ent), 0.62); certB.rotation.set(-0.05, 0.12, lerp(0.25, -0.06, ent));
    const crack = t > 36.69; cD.material.opacity = crack ? 1 : 0;
    if (crack) { const k = prog(t, 36.69, 36.9); certB.position.x += Math.sin(t * 90) * 0.012 * (1 - k); certB.position.y -= ep(t, 36.69, 37.6, ease.out) * 0.06; }
    // dust in the beam
    const a = dust.geometry.attributes.position.array;
    for (let k = 0; k < ds.length; k++) { const d = ds[k]; a[k * 3] = d[0] + Math.sin(t * 0.3 * d[4] + d[3]) * 0.25; a[k * 3 + 1] = ((d[1] - t * 0.05 * d[4] + 2.5) % 5 + 5) % 5 - 2.5; a[k * 3 + 2] = d[2]; }
    dust.geometry.attributes.position.needsUpdate = true;
  }
  const T = (x, y, z) => [x, y, z];
  const cams = {
    'gal-a': [[0.0, T(0.05, 0.38, 3.9), T(0.02, 0.3, 0), 32], [1.0, T(0.05, 0.3, 4.6), T(0.05, 0.2, 0), 32],
      [2.5, T(0.25, -0.25, 8.4), T(0.2, -0.4, 0), 34], [3.8, T(0.3, -0.35, 7.6), T(0.3, -0.45, 0), 34], [5.35, T(0.48, -0.85, 3.2), T(0.42, -0.98, 0.62), 34]],
    'gal-b': [[33.9, T(0.15, -0.25, 7.9), T(0.08, -0.4, 0), 34], [36.6, T(0.1, -0.3, 7.1), T(0.05, -0.45, 0), 34], [38.5, T(0.05, -0.4, 6.4), T(0.05, -0.55, 0.2), 34]],
  };
  return { scene, update, cams };
}
