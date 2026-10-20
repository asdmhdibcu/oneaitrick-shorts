/* One AI Trick — long-form engine. Shared toolkit for every chapter.
 * OAT.create(DUR) -> E with: tl, S, helpers (div,img,shadow,chip,svg,text),
 * motion (popIn,slideIn,bob,shake,draw,flash,glow,typeOn,count,whip),
 * swarm3d, quote(), title(), sources(), captions(CAPS,covers), ui(), finalize().
 * Captions auto-hide inside any registered cover window, so text never doubles. */
(function () {
  const NS = "http://www.w3.org/2000/svg";
  function rnd(seed){let a=seed|0;return()=>{a=(a+0x6d2b79f5)|0;let t=Math.imul(a^(a>>>15),1|a);t=(t+Math.imul(t^(t>>>7),61|t))^t;return((t^(t>>>14))>>>0)/4294967296;};}

  OAT = { rnd };

  OAT.create = function (DUR) {
    const root = document.getElementById("stage");
    const tl = gsap.timeline({ paused: true });
    const E_EASE = "power3.out";
    const covers = [];            // [t0,t1] windows where big text covers the frame
    const A = "assets/3d/";
    const $ = (s, r) => (r || document).querySelector(s);

    function div(p, c, css, html){const d=document.createElement("div");if(c)d.className=c;if(css)d.style.cssText=css;if(html!=null)d.innerHTML=html;p.appendChild(d);return d;}
    function img(p, name, x, yb, w, css){const d=div(p,"w",`left:${x-w/2}px;top:${yb-w}px;width:${w}px;height:${w}px;${css||""}`);const i=document.createElement("img");i.src=A+name+".png";d.appendChild(i);d.i=i;return d;}
    function shadow(p,x,yb,w,op){return div(p,"shadow",`left:${x-w*0.36}px;top:${yb-w*0.05}px;width:${w*0.72}px;height:${w*0.11}px;opacity:${op==null?1:op}`);}
    function chip(p,text,x,y,color,css){const d=div(p,"chipx",`left:${x}px;top:${y}px;color:${color||"var(--lime)"};${css||""}`,text);d.setAttribute("data-layout-allow-occlusion","");return d;}
    function text(p,cls,x,y,html,css){const d=div(p,cls,`left:${x}px;top:${y}px;${css||""}`,html);d.setAttribute("data-layout-allow-occlusion","");return d;}
    function svg(p,w,h,inner,css){const s=document.createElementNS(NS,"svg");s.setAttribute("width",w);s.setAttribute("height",h);s.setAttribute("viewBox",`0 0 ${w} ${h}`);s.style.cssText="position:absolute;overflow:visible;"+(css||"");s.innerHTML=inner;p.appendChild(s);return s;}

    function popIn(t,els,st){tl.fromTo(els,{opacity:0,scale:0.3},{opacity:1,scale:1,duration:0.45,ease:"back.out(2.2)",stagger:st||0},t);}
    function slideIn(t,els,from,st){tl.fromTo(els,Object.assign({opacity:0},from),{opacity:1,x:0,y:0,rotation:0,duration:0.55,ease:E_EASE,stagger:st||0},t);}
    function bob(el,t0,t1,amp,per){const n=Math.max(1,Math.floor((t1-t0)/per)*2-1);tl.fromTo(el,{y:0},{y:-amp,duration:per/2,ease:"sine.inOut",yoyo:true,repeat:n},t0);}
    function shake(el,t,dur,amp){const k=[];for(let i=0;i<8;i++)k.push(((i%2)?-1:1)*amp*(1-i/8));k.push(0);tl.to(el,{keyframes:{x:k},duration:dur,ease:"none"},t);}
    function draw(t,sel,dur,ease){document.querySelectorAll(sel).forEach((p)=>{const L=p.getTotalLength();p.style.strokeDasharray=L;tl.set(p,{opacity:1},t);tl.fromTo(p,{strokeDashoffset:L},{strokeDashoffset:0,duration:dur,ease:ease||"power2.inOut"},t);});}
    function flash(t,op,col){tl.set("#flash",{background:col||"#fff",opacity:op||0.8},t);tl.to("#flash",{opacity:0,duration:0.35,ease:"power2.out"},t+0.01);}
    function glow(el,t,col,dur){tl.to(el,{filter:`drop-shadow(0 0 22px ${col}) drop-shadow(0 0 60px ${col})`,duration:dur||0.35},t);}
    function typeOn(el,str,t0,t1){const n=str.length;for(let i=1;i<=n;i++)tl.set(el,{textContent:str.slice(0,i)},t0+(t1-t0)*(i/n));}
    function count(el,t0,t1,to,fmt){const o={v:(to>50?1:0)};tl.to(o,{v:to,duration:t1-t0,ease:"power2.out",onUpdate(){el.textContent=(fmt||((x)=>Math.round(x).toLocaleString()))(o.v);}},t0);}
    function whipOut(el,t,dir){tl.to(el,{x:(dir||-1)*2200,filter:"blur(22px)",duration:0.34,ease:"power3.in"},t);}
    function whipIn(el,t,dir){tl.fromTo(el,{x:(dir||1)*2200,filter:"blur(22px)"},{x:0,filter:"blur(0px)",duration:0.42,ease:"power3.out"},t);}

    /* ---- 3D perspective swarm (background motif) ---- */
    const sc=document.getElementById("swarm"), sx=sc.getContext("2d");
    const SN=560, R=rnd(71), P=[];
    for(let i=0;i<SN;i++)P.push({x:(R()*2-1)*1400,y:(R()*2-1)*820,z:200+R()*2600,ph:R()*6.28,sp:0.4+R()*0.9});
    const S={t:0,mood:[124,196,255],pink:0,alpha:0,cam:0,spread:1,drift:1};
    const F=1200;
    function swarmDraw(){
      sx.clearRect(0,0,1920,1080);
      if(S.alpha<=0.01)return;
      const pk=[255,122,198],m=S.mood;
      const r=Math.round(m[0]+(pk[0]-m[0])*S.pink),g=Math.round(m[1]+(pk[1]-m[1])*S.pink),b=Math.round(m[2]+(pk[2]-m[2])*S.pink);
      const list=[];
      for(let i=0;i<SN;i++){const p=P[i];let z=p.z-(S.cam%2600);if(z<60)z+=2600;list.push({p,z,i});}
      list.sort((a,c)=>c.z-a.z);
      for(const o of list){const p=o.p,z=o.z;const k=F/z;const X=960+p.x*k*S.spread+Math.sin(S.t*0.3+p.ph)*6*S.drift,Y=540+p.y*k*S.spread+Math.cos(S.t*0.26+p.ph)*6*S.drift;
        if(X<-40||X>1960||Y<-40||Y>1120)continue;
        const depth=1-(z-60)/2600;let a=(0.25+0.6*depth)*(0.55+0.45*Math.sin(S.t*p.sp+p.ph))*S.alpha;if(a<=0.02)continue;
        const rad=Math.max(0.6,3.4*k*8);
        const gl=sx.createRadialGradient(X,Y,0,X,Y,rad*3.5);gl.addColorStop(0,`rgba(${r},${g},${b},${0.5*a})`);gl.addColorStop(1,`rgba(${r},${g},${b},0)`);
        sx.fillStyle=gl;sx.beginPath();sx.arc(X,Y,rad*3.5,0,6.2832);sx.fill();
        sx.fillStyle=`rgba(${r},${g},${b},${a})`;sx.beginPath();sx.arc(X,Y,rad,0,6.2832);sx.fill();}
    }

    /* ---- big text: quote / title / sources — each registers a cover window ---- */
    function quote(t0,t1,opts){
      opts=opts||{}; covers.push([t0-0.1,t1+0.1]);
      const q=div(root,"quote"+(opts.big?" big":"")+(opts.lime?" lime":"")+(opts.pink?" pink":""),"opacity:0");
      if(opts.mk) div(q,"mk",null,opts.mk);
      const qq=div(q,"q");
      tl.fromTo(q,{opacity:0,scale:opts.big?0.9:1,y:opts.big?0:18},{opacity:1,scale:1,y:0,duration:0.45,ease:E_EASE},t0);
      if(opts.type){typeOn(qq,opts.text,t0+0.1,Math.min(t1-0.2,t0+1.9));}else{tl.set(qq,{textContent:opts.text},t0);}
      tl.to(q,{opacity:0,duration:0.4},t1);
      return q;
    }
    function title(t0,opts){
      covers.push([t0-0.1,DUR]);
      const w=div(root,"title","opacity:0");
      if(opts.k)div(w,"k",null,opts.k);
      div(w,"t",null,opts.t);
      const sub=opts.sub?div(w,"sub","",opts.sub):null;
      tl.fromTo(w,{opacity:0,scale:0.92},{opacity:1,scale:1,duration:0.6,ease:E_EASE},t0);
      return {w,sub};
    }
    function sources(t0,items,subToHide){
      const s=div(root,"sources","opacity:0");
      s.innerHTML=items.map((x,i)=>(i?'<span class="dt">•</span>':'')+`<b>${x}</b>`).join("");
      if(subToHide)tl.to(subToHide,{opacity:0,duration:0.3},t0-0.3);
      tl.fromTo(s,{opacity:0,y:16},{opacity:1,y:0,duration:0.5,ease:E_EASE},t0);
      return s;
    }

    /* ---- captions (auto-hidden inside cover windows) ---- */
    function captions(CAPS){
      const capsRoot=document.getElementById("caps");
      (CAPS||[]).forEach((cc)=>{
        const covered=covers.some(([a,b])=>cc.t0<b&&cc.t1>a);
        if(covered)return;
        const c=div(capsRoot,"cap");
        const sp=cc.w.map((w)=>{const s=document.createElement("span");s.className="cw";s.textContent=w.d;c.appendChild(s);return{s,w};});
        tl.fromTo(c,{opacity:0,y:8},{opacity:0.98,y:0,duration:0.12},cc.t0);
        tl.set(c,{opacity:0},cc.t1);
        sp.forEach(({s,w},k)=>{const end=k+1<sp.length?sp[k+1].w.s:cc.t1;tl.set(s,{color:"#c8ff4d"},w.s);tl.set(s,{color:"#ffffff"},end);});
      });
    }

    function ui(kickerText){
      tl.fromTo(["#kick","#handle"],{opacity:0,y:-12},{opacity:0.9,y:0,duration:0.5},0.6);
      if(kickerText)document.getElementById("kicklbl").textContent=kickerText;
      const gp={f:0},gEl=document.getElementById("grain");
      tl.fromTo(gp,{f:0},{f:DUR*24,duration:DUR,ease:"none",onUpdate(){const f=Math.floor(gp.f);gEl.style.backgroundPosition=`${(f*137)%512}px ${(f*271)%512}px`;}},0);
    }
    function finalize(){
      const mp={t:0};tl.to(mp,{t:DUR,duration:DUR,ease:"none",onUpdate(){S.t=mp.t;swarmDraw();}},0);
      window.__timelines=window.__timelines||{};window.__timelines["main"]=tl;tl.seek(0);swarmDraw();
    }

    return {tl,S,root,A,$,div,img,shadow,chip,text,svg,popIn,slideIn,bob,shake,draw,flash,glow,typeOn,count,whipOut,whipIn,
            swarmDraw,quote,title,sources,captions,ui,finalize,covers};
  };
})();
