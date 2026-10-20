// Core: renderer, environment, two-scene dissolve transition, bloom, helpers.
// Everything is a pure function of time t (seconds) so any frame can be rendered in any order.
import * as THREE from 'three';
import { EffectComposer } from 'three/examples/jsm/postprocessing/EffectComposer.js';
import { Pass, FullScreenQuad } from 'three/examples/jsm/postprocessing/Pass.js';
import { UnrealBloomPass } from 'three/examples/jsm/postprocessing/UnrealBloomPass.js';
import { OutputPass } from 'three/examples/jsm/postprocessing/OutputPass.js';
import { RoomEnvironment } from 'three/examples/jsm/environments/RoomEnvironment.js';

export const W = 1080, H = 1920;
export const FRAME_Y = 760;          // screen y where a camera's look-at target lands (visual zone 280-1220)

// ---------- deterministic helpers ----------
export function rng(seed) { let a = seed | 0; return () => { a = (a + 0x6d2b79f5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
export const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
export const lerp = (a, b, k) => a + (b - a) * k;
export const prog = (t, t0, t1) => clamp((t - t0) / (t1 - t0));          // 0..1 over [t0,t1]
export const ease = {
  io: (k) => k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2,
  out: (k) => 1 - Math.pow(1 - k, 3),
  in: (k) => k * k * k,
  expo: (k) => k === 1 ? 1 : 1 - Math.pow(2, -10 * k),
  back: (k) => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(k - 1, 3) + c1 * Math.pow(k - 1, 2); },
  sine: (k) => -(Math.cos(Math.PI * k) - 1) / 2,
};
export const ep = (t, t0, t1, fn = ease.io) => fn(prog(t, t0, t1));
// keyframed scalar: [[t,v],...] with easing between keys
export function keys(t, ks, fn = ease.io) {
  if (t <= ks[0][0]) return ks[0][1];
  for (let i = 1; i < ks.length; i++) if (t <= ks[i][0]) return lerp(ks[i - 1][1], ks[i][1], fn(prog(t, ks[i - 1][0], ks[i][0])));
  return ks[ks.length - 1][1];
}
export function keysV(t, ks, fn = ease.io) { // vec3 keys
  return new THREE.Vector3(keys(t, ks.map(k => [k[0], k[1][0]]), fn), keys(t, ks.map(k => [k[0], k[1][1]]), fn), keys(t, ks.map(k => [k[0], k[1][2]]), fn));
}

// ---------- camera that frames the look-at target at FRAME_Y ----------
export function makeCam(fov = 38) {
  const c = new THREE.PerspectiveCamera(fov, W / H, 0.05, 600);
  // virtual frame taller than the screen so the principal point sits at FRAME_Y
  const extra = 2 * (H / 2 - FRAME_Y);
  c.setViewOffset(W, H + extra, 0, extra, W, H);
  return c;
}
export function aim(cam, pos, target, roll = 0) {
  cam.position.copy(pos); cam.up.set(Math.sin(roll), Math.cos(roll), 0); cam.lookAt(target);
}

// ---------- dissolve between two scenes ----------
class DualScenePass extends Pass {
  constructor(renderer, rw = W, rh = H) {
    super();
    const o = { type: THREE.HalfFloatType };
    this.rtA = new THREE.WebGLRenderTarget(rw, rh, o); this.rtB = new THREE.WebGLRenderTarget(rw, rh, o);
    this.mat = new THREE.ShaderMaterial({
      uniforms: { tA: { value: null }, tB: { value: null }, p: { value: 0 }, mode: { value: 0 }, edge: { value: new THREE.Color(0xc8ff4d) } },
      vertexShader: `varying vec2 vUv; void main(){ vUv=uv; gl_Position=vec4(position.xy,0.,1.); }`,
      fragmentShader: `
        uniform sampler2D tA,tB; uniform float p; uniform int mode; uniform vec3 edge; varying vec2 vUv;
        float h(vec2 q){ return fract(sin(dot(q,vec2(127.1,311.7)))*43758.5453); }
        float n(vec2 q){ vec2 i=floor(q),f=fract(q); f=f*f*(3.-2.*f);
          return mix(mix(h(i),h(i+vec2(1,0)),f.x),mix(h(i+vec2(0,1)),h(i+vec2(1,1)),f.x),f.y); }
        float fbm(vec2 q){ float s=0.,a=.5; for(int i=0;i<4;i++){ s+=a*n(q); q*=2.03; a*=.5; } return s; }
        void main(){
          vec4 A=texture2D(tA,vUv), B;
          if(mode==1){ // zoom-through: B scales in from centre with a radial blur feel
            vec2 c=vec2(.5,.6); float z=mix(1.6,1.,p); vec2 uv=c+(vUv-c)/z; B=texture2D(tB,uv);
            vec2 ua=c+(vUv-c)*mix(1.,.55,p); vec4 A2=texture2D(tA,ua);
            gl_FragColor=mix(A2,B,smoothstep(.15,.85,p)); return; }
          B=texture2D(tB,vUv);
          float k=fbm(vUv*vec2(3.,5.3))*.85+ (1.-vUv.y)*.15;          // noise field
          float th=mix(-.2,1.2,p);
          float m=smoothstep(th-.06,th+.06,k);                        // 0 -> B, 1 -> A
          float e=1.-abs(m*2.-1.);                                    // glowing seam
          vec3 col=mix(B.rgb,A.rgb,m)+edge*pow(e,3.)*2.2*(1.-abs(p*2.-1.));
          gl_FragColor=vec4(col,1.);
        }`,
      depthTest: false, depthWrite: false,
    });
    this.fsq = new FullScreenQuad(this.mat);
    this.A = null; this.B = null; this.p = 0; this.mode = 0;
  }
  render(renderer, writeBuffer) {
    renderer.setRenderTarget(this.rtA); renderer.clear(); renderer.render(this.A.scene, this.A.cam);
    if (this.B && this.p > 0) { renderer.setRenderTarget(this.rtB); renderer.clear(); renderer.render(this.B.scene, this.B.cam); }
    this.mat.uniforms.tA.value = this.rtA.texture;
    this.mat.uniforms.tB.value = (this.B && this.p > 0) ? this.rtB.texture : this.rtA.texture;
    this.mat.uniforms.p.value = (this.B ? this.p : 0); this.mat.uniforms.mode.value = this.mode;
    renderer.setRenderTarget(this.renderToScreen ? null : writeBuffer); this.fsq.render(renderer);
  }
}

// lite = HyperFrames `check` session (layout/contrast lint only): same picture at quarter resolution so its 120 s budget holds.
export function makeRenderer(canvas, lite = false) {
  const RW = lite ? W / 4 : W, RH = lite ? H / 4 : H;
  const r = new THREE.WebGLRenderer({ canvas, antialias: false, preserveDrawingBuffer: true, powerPreference: 'high-performance' });
  r.setPixelRatio(1); r.setSize(RW, RH, false);
  r.toneMapping = THREE.ACESFilmicToneMapping; r.toneMappingExposure = 0.95;
  r.outputColorSpace = THREE.SRGBColorSpace;
  const pm = new THREE.PMREMGenerator(r);
  const env = pm.fromScene(new RoomEnvironment(), 0.04).texture;
  const comp = new EffectComposer(r);
  comp.setPixelRatio(1); comp.setSize(RW, RH);
  const dual = new DualScenePass(r, RW, RH); comp.addPass(dual);
  const bloom = new UnrealBloomPass(new THREE.Vector2(RW / 2, RH / 2), 0.7, 0.32, 1.0); comp.addPass(bloom);
  comp.addPass(new OutputPass());
  return { r, env, comp, dual, bloom };
}

// ---------- shared materials / textures ----------
export function radialTex(inner = 'rgba(255,255,255,1)', outer = 'rgba(255,255,255,0)', size = 256) {
  const c = document.createElement('canvas'); c.width = c.height = size; const g = c.getContext('2d');
  const gr = g.createRadialGradient(size / 2, size / 2, 0, size / 2, size / 2, size / 2);
  gr.addColorStop(0, inner); gr.addColorStop(1, outer); g.fillStyle = gr; g.fillRect(0, 0, size, size);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
}
export const SOFT = () => radialTex('rgba(255,255,255,1)', 'rgba(255,255,255,0)');

// glowing additive sprite-plane (halo, light pool, blob)
export function glowPlane(size, color, opacity = 1, tex) {
  const m = new THREE.MeshBasicMaterial({ map: tex || SOFT(), color, transparent: true, opacity, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false });
  return new THREE.Mesh(new THREE.PlaneGeometry(size, size), m);
}
export function shadowBlob(size, opacity = 0.7) {
  const m = new THREE.MeshBasicMaterial({ map: radialTex('rgba(0,0,0,1)', 'rgba(0,0,0,0)'), transparent: true, opacity, depthWrite: false });
  const p = new THREE.Mesh(new THREE.PlaneGeometry(size, size), m); p.rotation.x = -Math.PI / 2; return p;
}
// volumetric light cone (fake god-ray)
export function lightCone(h, r, color, opacity = 0.18) {
  const g = new THREE.ConeGeometry(r, h, 48, 1, true); g.translate(0, -h / 2, 0);
  const m = new THREE.ShaderMaterial({
    uniforms: { c: { value: new THREE.Color(color) }, o: { value: opacity }, h: { value: h } },
    vertexShader: `varying float vY; varying vec3 vN; varying vec3 vV; void main(){ vY=position.y; vec4 mv=modelViewMatrix*vec4(position,1.); vN=normalize(normalMatrix*normal); vV=normalize(-mv.xyz); gl_Position=projectionMatrix*mv; }`,
    fragmentShader: `uniform vec3 c; uniform float o,h; varying float vY; varying vec3 vN; varying vec3 vV;
      void main(){ float f=1.+vY/h; float rim=pow(abs(dot(vN,vV)),1.6); gl_FragColor=vec4(c, o*rim*(1.-f)*(1.-f)*1.4); }`,
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide, toneMapped: false,
  });
  return new THREE.Mesh(g, m);
}

// soft point particles (dust, data, embers). positions are recomputed by the caller each frame.
export function makePoints(n, color, size = 0.06, opacity = 1) {
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.BufferAttribute(new Float32Array(n * 3), 3));
  g.setAttribute('aCol', new THREE.BufferAttribute(new Float32Array(n * 3).fill(1), 3));
  g.setAttribute('aSize', new THREE.BufferAttribute(new Float32Array(n).fill(1), 1));
  const m = new THREE.ShaderMaterial({
    uniforms: { uC: { value: new THREE.Color(color) }, uS: { value: size * H * 0.5 }, uO: { value: opacity } },
    vertexShader: `attribute vec3 aCol; attribute float aSize; uniform float uS; varying vec3 vC; varying float vA;
      void main(){ vC=aCol; vec4 mv=modelViewMatrix*vec4(position,1.); gl_PointSize=uS*aSize/max(.1,-mv.z); vA=step(.01,aSize); gl_Position=projectionMatrix*mv; }`,
    fragmentShader: `uniform vec3 uC; uniform float uO; varying vec3 vC; varying float vA;
      void main(){ vec2 d=gl_PointCoord-.5; float r=length(d); float a=smoothstep(.5,0.,r); a=a*a; gl_FragColor=vec4(uC*vC*1.6, a*uO*vA); }`,
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, toneMapped: false,
  });
  const p = new THREE.Points(g, m); p.frustumCulled = false; return p;
}

// text drawn into a canvas texture (for holograms / screens inside the 3D world)
export function textCanvas(w, h) {
  const c = document.createElement('canvas'); c.width = w; c.height = h; const g = c.getContext('2d');
  const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 4;
  return { c, g, tex };
}

export { THREE };
