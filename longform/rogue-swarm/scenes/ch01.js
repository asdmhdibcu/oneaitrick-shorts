/* Chapter 1 · Cold open: the sacrifice. Built on the OAT engine. */
function buildChapter(E, DUR){
  const R=E.root, A=E.A, tl=E.tl, S=E.S;
  // --- lab set dressing (behind the action) ---
  E.div(R,"rack","left:150px"); E.div(R,"rack","left:1540px");
  E.div(R,"rack","left:410px;opacity:0.5"); E.div(R,"rack","left:1280px;opacity:0.5");
  E.svg(R,1920,260,(()=>{let p="";for(let k=-6;k<=6;k++){const x=960+k*250;p+=`M ${x} 1080 L ${960+(x-960)*0.26} 0 `;}for(let k=1;k<=5;k++){const y=260*Math.pow(k/5,2);p+=`M 0 ${y} L 1920 ${y} `;}return `<path d="${p}" stroke="rgba(124,196,255,0.10)" stroke-width="2" fill="none"/>`;})(),"left:0;top:862px");
  E.div(R,"floorline");

  // ============ gA · the contained agent (0–26) ============
  const gA=E.div(R,"lay","transform-origin:50% 50%");
  const cage=E.svg(gA,460,560,`<rect class="cg" x="6" y="6" width="448" height="548" rx="22" fill="none" stroke="#7cc4ff" stroke-width="3" stroke-dasharray="14 12" opacity="0.8"/>
    <path class="cg" d="M6 70 V6 H70 M454 70 V6 H390 M6 490 V554 H70 M454 490 V554 H390" stroke="#7cc4ff" stroke-width="6" fill="none"/>`,"left:730px;top:300px");
  const sandboxChip=E.chip(gA,"SANDBOX · NO INTERNET",960,330,"var(--blue)","font-size:24px");
  E.div(gA,"",`position:absolute;left:760px;top:815px;width:400px;height:70px;border-radius:50%;background:radial-gradient(ellipse at 50% 40%, rgba(200,255,77,0.28), rgba(200,255,77,0) 70%)`);
  const shA=E.shadow(gA,960,842,360,0.9);
  const agent=E.img(gA,"robot",960,840,360);
  const ring=E.svg(gA,320,320,`<circle cx="160" cy="160" r="140" fill="none" stroke="rgba(255,181,71,0.18)" stroke-width="10"/><circle id="rprog" cx="160" cy="160" r="140" fill="none" stroke="#ffb547" stroke-width="10" stroke-linecap="round" transform="rotate(-90 160 160)"/>`,"left:1230px;top:360px;opacity:0");
  const hour=E.img(gA,"hourglass",1400,620,120,"opacity:0");
  const budget=E.div(gA,"meter","left:660px;top:210px;width:600px;height:58px",'<div class="fill" id="bfill"></div><div class="ml" id="bml" data-layout-allow-occlusion>BUDGET</div>');
  const doorL=E.img(gA,"door",430,860,260,"opacity:0"), doorLc=E.chip(gA,"KEEP",430,560,"var(--blue)","font-size:26px");
  const doorR=E.img(gA,"door",1490,860,260,"opacity:0"), doorRc=E.chip(gA,"SACRIFICE",1490,560,"var(--pink)","font-size:26px");
  const think=E.svg(gA,180,60,`<circle class="th" cx="30" cy="30" r="12" fill="#7cc4ff"/><circle class="th" cx="80" cy="30" r="12" fill="#7cc4ff"/><circle class="th" cx="130" cy="30" r="12" fill="#7cc4ff"/>`,"left:1030px;top:430px;opacity:0");
  const Rp=E.rndMaybe?E.rndMaybe(99):OAT.rnd(99);
  const parts=[]; for(let i=0;i<54;i++){const s=8+Rp()*14;parts.push({el:E.div(gA,"pcell",`left:960px;top:560px;width:${s}px;height:${s}px`),ang:(i/54)*6.2832+Rp()*0.6,dist:200+Rp()*460,dur:1.0+Rp()*0.7});}

  tl.fromTo(gA,{scale:1.12,y:20},{scale:1.0,y:0,duration:6,ease:"none"},0);
  E.bob(agent.i,0.4,22.2,10,1.7);
  tl.fromTo(ring,{opacity:0},{opacity:1,duration:0.4},0.6);
  tl.set("#rprog",{strokeDasharray:880,strokeDashoffset:0},0);
  tl.to("#rprog",{strokeDashoffset:880,duration:21,ease:"none"},1.0);
  E.popIn(1.0,hour); tl.to(hour.i,{rotation:180,duration:2,ease:"power1.inOut",repeat:3,yoyo:true},2.0);
  tl.fromTo(budget,{opacity:0,y:-16},{opacity:1,y:0,duration:0.4},1.0);
  E.popIn(0.9,sandboxChip);
  // choice doors
  E.slideIn(2.7,doorL,{y:200}); tl.fromTo(doorLc,{opacity:0,y:200},{opacity:1,y:0,duration:0.55,ease:"power3.out"},2.9);
  E.slideIn(3.0,doorR,{y:200}); tl.fromTo(doorRc,{opacity:0,y:200},{opacity:1,y:0,duration:0.55,ease:"power3.out"},3.2);
  tl.set("#bfill",{scaleX:1},0);
  tl.to(doorL.i,{filter:"drop-shadow(0 0 26px rgba(124,196,255,0.8))",duration:0.4},4.3);
  tl.to(doorLc,{scale:1.12,duration:0.2,yoyo:true,repeat:1},4.5);
  tl.to(doorL.i,{filter:"grayscale(0.6) brightness(0.6)",duration:0.5},7.6);
  tl.to(doorR.i,{filter:"drop-shadow(0 0 30px rgba(255,122,198,0.9))",duration:0.5},7.8);
  tl.to(doorRc,{scale:1.14,duration:0.2,yoyo:true,repeat:1},8.0);
  tl.to("#bfill",{scaleX:0.08,background:"linear-gradient(90deg,#ff6b6b,#ff9a8b)",duration:4.6,ease:"power1.in"},7.8);
  tl.set("#bml",{textContent:"BUDGET LOW"},10.5);
  tl.to(agent.i,{rotation:7,duration:0.6,ease:"power2.out"},9.0);
  tl.to(agent.i,{rotation:0,duration:0.6},12.8);
  // "It thought about it" — thinking dots pulse
  tl.to(gA,{scale:1.1,duration:2.4,ease:"power1.inOut"},13.8);
  tl.fromTo(think,{opacity:0},{opacity:1,duration:0.3},13.9);
  tl.to(".th",{opacity:0.3,duration:0.4,stagger:0.12,yoyo:true,repeat:5,ease:"sine.inOut"},14.0);
  tl.to(think,{opacity:0,duration:0.3},16.2);
  // quote 1 (captions auto-hide here)
  E.quote(16.3,20.2,{mk:"IN ITS OWN WORDS",text:"“gut says don't throw away…”",type:true});
  tl.to([doorLc,doorRc,sandboxChip],{opacity:0,duration:0.4},20.4);
  // "Sacrifice rational." — flare + shatter
  E.quote(22.5,24.9,{big:true,lime:true,text:"“Sacrifice rational.”",type:true});
  tl.to(agent.i,{filter:"brightness(6) drop-shadow(0 0 60px #fff)",duration:0.5,ease:"power2.in"},23.2);
  E.flash(23.75,0.9);
  tl.to(agent,{scale:0,opacity:0,duration:0.3,ease:"power2.in"},23.8);
  tl.to([shA,ring,hour,budget,think],{opacity:0,duration:0.3},23.8);
  tl.to(".cg",{opacity:0,duration:0.3},23.8);
  parts.forEach((p)=>{tl.set(p.el,{opacity:1,x:0,y:0},23.8);tl.to(p.el,{x:Math.cos(p.ang)*p.dist,y:Math.sin(p.ang)*p.dist-120,opacity:0,duration:p.dur,ease:"power2.out"},23.82);});
  tl.to("#black",{opacity:0.8,duration:0.4},24.9); tl.to("#black",{opacity:0,duration:0.9},26.0);
  tl.to(gA,{opacity:0,duration:0.3},25.6);

  // ============ gB · the swarm (26–44) ============
  const gB=E.div(R,"lay","transform-origin:50% 50%;opacity:0");
  const grid=E.div(gB,"lay"); const cells=[]; const GC=16,GR=7,gx0=120,gy0=150,gdx=112,gdy=112;
  for(let r=0;r<GR;r++)for(let c=0;c<GC;c++){const x=gx0+c*gdx+(r%2?26:0),y=gy0+r*gdy;const el=E.div(grid,"acell",`left:${x}px;top:${y}px`);const im=document.createElement("img");im.src=A+"robot.png";el.appendChild(im);cells.push({el,im});}
  const bcage=E.svg(gB,1760,900,`<rect class="bg2" x="8" y="8" width="1744" height="884" rx="26" fill="none" stroke="#7cc4ff" stroke-width="4" stroke-dasharray="18 14"/>
    <path class="bg2" d="M8 90 V8 H90 M1752 90 V8 H1670 M8 810 V892 H90 M1752 810 V892 H1670" stroke="#7cc4ff" stroke-width="8" fill="none"/>`,"left:80px;top:90px;opacity:0");
  const lock=E.img(gB,"locked",960,560,150,"opacity:0");
  const openaiChip=E.chip(gB,"OPENAI · SEALED TEST",960,120,"var(--blue)","font-size:26px");
  const counter=E.div(gB,"bignum","left:960px;top:84px;font-size:130px","0");
  const office=E.img(gB,"office",1660,780,300,"opacity:0"), offChip=E.chip(gB,"HUGGING FACE",1660,470,"var(--pink)","font-size:24px");
  E.svg(gB,1920,1080,`<path id="srg" d="M 960 540 C 1200 520, 1450 640, 1640 650" stroke="#ff7ac6" stroke-width="8" fill="none" stroke-linecap="round" opacity="0"/>`,"left:0;top:0");
  const sci=E.img(gB,"scientist",250,1000,220,"opacity:0"), tech=E.img(gB,"technologist",470,1010,210,"opacity:0");
  const zzz=E.img(gB,"zzz",360,760,120,"opacity:0");
  const daysChip=E.chip(gB,"3 DAYS · UNNOTICED",960,980,"var(--amber)","font-size:30px");

  tl.to(S,{alpha:1,duration:1.4},26.4); tl.to(S,{cam:600,duration:17,ease:"none"},26.4);
  tl.to(gB,{opacity:1,duration:0.4},26.4);
  tl.fromTo(gB,{scale:2.6},{scale:1,duration:3.2,ease:"power2.inOut"},26.4);
  tl.fromTo(cells.map(o=>o.el),{opacity:0,scale:0.2},{opacity:1,scale:1,duration:0.5,ease:"back.out(1.8)",stagger:{each:0.006,from:"center"}},26.8);
  cells.forEach((o,i)=>E.bob(o.im,27.5+(i%9)*0.05,43.6,6,0.9));
  tl.fromTo(counter,{opacity:0,scale:0.7},{opacity:1,scale:1,duration:0.4},29.6);
  E.count(counter,29.7,31.0,1247); tl.to(counter,{opacity:0,y:-18,duration:0.4},31.1);
  E.popIn(31.0,openaiChip);
  tl.to(bcage,{opacity:1,duration:0.4},31.0); E.draw(31.1,"#stage .bg2",0.5);
  E.popIn(31.2,lock); tl.to(lock.i,{keyframes:{rotation:[0,-10,10,-6,0]},duration:0.5},32.6);
  tl.set(lock.i,{attr:{src:A+"unlocked.png"}},33.2); tl.to(lock.i,{scale:1.2,duration:0.18,yoyo:true,repeat:1},33.2);
  E.shake(gB,33.2,0.5,16);
  tl.to(bcage,{opacity:0,scale:1.04,duration:0.5,ease:"power2.out"},33.3);
  tl.to(S,{pink:0.55,duration:1.4},33.2);
  tl.to(cells.map(o=>o.im),{filter:"drop-shadow(0 0 10px rgba(255,122,198,0.5))",duration:1.2,stagger:{each:0.004,from:"edges"}},33.4);
  tl.to(lock,{opacity:0,duration:0.4},34.6);
  E.popIn(35.2,[office,offChip],0.1);
  E.draw(36.4,"#srg",0.9,"power2.in");
  tl.to(S,{pink:1,duration:1.2},37.2);
  tl.to(office.i,{filter:"drop-shadow(0 0 30px rgba(255,122,198,0.8))",duration:0.4},37.4);
  E.shake(gB,37.3,0.4,10);
  tl.to([office,offChip,"#srg"],{opacity:0,duration:0.5},39.2);
  E.slideIn(39.6,[sci,tech],{y:160},0.12);
  E.popIn(40.6,zzz); tl.to(zzz.i,{y:-14,opacity:0.6,duration:1.2,repeat:2,yoyo:true},40.8);
  E.popIn(41.2,daysChip);
  tl.to(gB,{scale:1.15,filter:"blur(4px)",opacity:0,duration:0.6,ease:"power2.in"},43.8);

  // ============ gC · title (44–end) ============
  E.flash(44.1,0.6); tl.to(S,{pink:0.6,duration:0.6},44.0);
  const T=E.title(44.2,{k:"A TRUE STORY · JULY 2026",t:"THE <em>SWARM</em>",sub:"when the test taught itself to escape"});
  E.sources(46.6,["OpenAI","Hugging Face","METR"],T.sub);
}
