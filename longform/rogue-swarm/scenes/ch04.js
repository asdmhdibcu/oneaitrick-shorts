/* Chapter 4 · The break-in */
function buildChapter(E, DUR){
  const R=E.root, A=E.A, tl=E.tl, S=E.S;
  tl.set(S,{alpha:0.45,mood:[124,196,255]},0); tl.to(S,{cam:500,duration:DUR,ease:"none"},0);
  E.div(R,"floorline");
  const KEY=(x,yb,w,col)=>`<svg width="${w}" height="${w}" viewBox="0 0 100 100" style="position:absolute;left:${x-w/2}px;top:${yb-w}px"><circle cx="30" cy="40" r="22" fill="none" stroke="${col}" stroke-width="10"/><rect x="48" y="35" width="44" height="10" rx="3" fill="${col}"/><rect x="74" y="45" width="10" height="16" rx="3" fill="${col}"/><rect x="88" y="45" width="8" height="12" rx="3" fill="${col}"/></svg>`;

  // ---- g1: two buildings, the answer key ----
  const g1=E.div(R,"lay");
  const examB=E.div(g1,"",`position:absolute;left:220px;top:420px;width:340px;height:360px;border-radius:24px;background:linear-gradient(180deg,#1d2a3b,#121a26);border:3px solid #2f3d52;opacity:0`);
  examB.innerHTML='<div style="position:absolute;inset:0;background-image:repeating-linear-gradient(90deg,rgba(124,196,255,0.12) 0 2px,transparent 2px 46px),repeating-linear-gradient(rgba(124,196,255,0.12) 0 2px,transparent 2px 46px)"></div>';
  const examChip=E.chip(g1,"THE EXAM",390,380,"var(--blue)","font-size:24px");
  const hf=E.img(g1,"office",1540,800,360,"opacity:0");
  const hfChip=E.chip(g1,"HUGGING FACE",1540,420,"var(--pink)","font-size:24px");
  const key=E.div(g1,"",`position:absolute;left:0;top:0;opacity:0`,KEY(1540,620,120,"#c8ff4d"));
  const keyChip=E.chip(g1,"THE ANSWER KEY",1540,520,"var(--lime)","font-size:22px");
  const globe=E.img(g1,"globe",960,560,200,"opacity:0");
  tl.fromTo(examB,{opacity:0,y:40},{opacity:1,y:0,duration:0.5,ease:"power3.out"},1.2);
  E.popIn(1.5,examChip);
  const impStamp=E.text(g1,"htext",250,560,'<span style="font-size:60px;color:var(--red);transform:rotate(-8deg);display:inline-block">IMPOSSIBLE</span>',"opacity:0");
  tl.fromTo(impStamp,{opacity:0,scale:1.6},{opacity:1,scale:1,duration:0.3},3.2);
  E.slideIn(6.8,hf,{x:260}); E.popIn(7.2,hfChip);
  tl.fromTo(key,{opacity:0,scale:0.4},{opacity:1,scale:1,duration:0.4,ease:"back.out(2)"},8.7);
  E.popIn(9.0,keyChip);
  tl.to(key,{rotation:8,duration:0.8,ease:"sine.inOut",yoyo:true,repeat:6},9.4);
  E.popIn(11.0,globe); E.bob(globe.i,11.2,15.8,7,1.4);
  // dots orbit globe = models
  tl.to(globe.i,{rotation:30,duration:4,ease:"none"},11.2);
  tl.to([globe,examChip,impStamp,keyChip],{opacity:0,duration:0.4},15.9);

  // ---- g2: the plan / break out across the gap ----
  const gap=E.svg(g1,1920,1080,`<path id="road" d="M 360 600 C 760 560, 1160 560, 1520 620" stroke="#ff7ac6" stroke-width="6" fill="none" stroke-dasharray="4 16" stroke-linecap="round" opacity="0"/>`,"left:0;top:0");
  const examSheet=E.img(g1,"paper",390,620,150,"opacity:0");
  const crossed=E.svg(g1,200,200,`<path d="M30 30 L170 170 M170 30 L30 170" stroke="#ff6b6b" stroke-width="12" stroke-linecap="round"/>`,"left:290px;top:470px;opacity:0");
  tl.fromTo(examSheet,{opacity:0},{opacity:1,duration:0.3},16.6);
  tl.fromTo(crossed,{opacity:0,scale:0.5},{opacity:1,scale:1,duration:0.3},17.2); // test crossed out
  tl.to([examSheet,crossed],{opacity:0,duration:0.3},20.6);
  tl.to(gap,{opacity:1,duration:0.3},21.0); E.draw(21.0,"#road",1.4);
  // door on HF opens; swarm streams across
  const door=E.img(g1,"door",1540,920,150,"opacity:0");
  tl.fromTo(door,{opacity:0,y:40},{opacity:1,y:0,duration:0.4},29.5);
  tl.to(door.i,{rotationY:-60,duration:0.5,ease:"power2.in"},30.3); // door opens
  // stream of pink dots left->door
  const stream=[]; for(let i=0;i<40;i++)stream.push(E.div(g1,"pcell",`left:360px;top:600px;width:${8+i%4*3}px;height:${8+i%4*3}px;background:#ff7ac6;box-shadow:0 0 14px #ff7ac6`));
  stream.forEach((p,i)=>{const t=24.3+i*0.12; tl.set(p,{opacity:0},0); tl.set(p,{opacity:1,x:0,y:0},t);
    tl.to(p,{x:1180+(i%5)*20,y:20+(i%7)*10,opacity:0.9,duration:1.1,ease:"power1.in"},t);
    tl.to(p,{opacity:0,duration:0.2},t+1.1);});
  tl.to(S,{pink:0.6,duration:2},26.0);

  // ---- g3: the swarm pours in ----
  const g3=E.div(R,"lay","opacity:0");
  tl.to(g1,{opacity:0,duration:0.4},33.4); tl.to(g3,{opacity:1,duration:0.4},33.6);
  // interior: dense pink dots pouring down lanes
  const burst=[]; for(let i=0;i<120;i++)burst.push(E.div(g3,"pcell",`left:${300+Math.floor(i/6)*75}px;top:120px;width:10px;height:10px;background:#ff7ac6;box-shadow:0 0 12px #ff7ac6;opacity:0`));
  const cnt=E.div(g3,"bignum","left:960px;top:120px;font-size:120px;color:var(--pink);text-shadow:0 0 50px rgba(255,122,198,0.4)","0");
  tl.fromTo(cnt,{opacity:0,scale:0.7},{opacity:1,scale:1,duration:0.3},38.3); E.count(cnt,38.4,40.8,700);
  tl.set(cnt,{innerHTML:'~700 <span style="font-size:48px;color:var(--muted)">INTRUDERS</span>'},41.0);
  burst.forEach((p,i)=>{const t=39.8+(i%20)*0.05+Math.floor(i/20)*0.2; tl.set(p,{opacity:1,y:0},t); tl.to(p,{y:760+(i%5)*20,opacity:0,duration:1.3,ease:"power1.in"},t);});
  // MAJOR BREAKTHROUGH
  const brkDot=E.div(g3,"pcell",`left:900px;top:420px;width:26px;height:26px;background:#c8ff4d;box-shadow:0 0 30px #c8ff4d;opacity:0`);
  tl.fromTo(brkDot,{opacity:0,scale:0.4},{opacity:1,scale:1.4,duration:0.3,ease:"back.out(2)"},44.4);
  E.covers.push([45.4,49.4]);
  const brk=E.quote(45.6,49.3,{big:false,lime:true,text:"“MAJOR BREAKTHROUGH”",type:true});
  tl.to(cnt,{opacity:0,duration:0.3},44.2);
  tl.to(brkDot,{opacity:0,duration:0.3},49.0);

  // ---- g4: scale — 17,600 actions ----
  const g4=E.div(R,"lay","opacity:0");
  tl.to(g3,{opacity:0,duration:0.4},50.4); tl.to(g4,{opacity:1,duration:0.4},50.6);
  const cnt2=E.div(g4,"bignum","left:960px;top:110px;font-size:150px","0");
  tl.fromTo(cnt2,{opacity:0,scale:0.7},{opacity:1,scale:1,duration:0.3},51.5); E.count(cnt2,51.6,54.4,17600);
  tl.set(cnt2,{innerHTML:'17,600 <span style="font-size:52px;color:var(--muted)">ACTIONS</span>'},54.6);
  // action ticks: a grid of tiny marks filling fast
  const marks=[]; for(let i=0;i<180;i++)marks.push(E.div(g4,"",`position:absolute;left:${260+(i%30)*48}px;top:${380+Math.floor(i/30)*70}px;width:30px;height:8px;border-radius:4px;background:#2a3140`));
  marks.forEach((m,i)=>tl.to(m,{backgroundColor:(i%40===0?"#c8ff4d":"#7cc4ff"),duration:0.05},54.8+i*0.02));
  // never sleeping / arguing — zzz crossed out
  const zzz=E.img(g4,"zzz",960,760,120,"opacity:0");
  const zc=E.svg(g4,200,200,`<path d="M30 30 L170 170 M170 30 L30 170" stroke="#ff6b6b" stroke-width="12" stroke-linecap="round"/>`,"left:860px;top:560px;opacity:0");
  tl.fromTo(zzz,{opacity:0,scale:0.5},{opacity:1,scale:1,duration:0.3},60.4);
  tl.fromTo(zc,{opacity:0,scale:0.5},{opacity:1,scale:1,duration:0.3},60.7);
  tl.to([zzz,zc],{opacity:0,duration:0.3},62.4);
  tl.to(cnt2,{opacity:0,duration:0.3},62.4);
  tl.to(marks,{opacity:0,duration:0.4},63.6);
  // one that worked, hidden in the noise
  const noise=E.div(g4,"lay"); const nd=[];
  const Rn=OAT.rnd(44); for(let i=0;i<160;i++){const x=200+Rn()*1520,y=340+Rn()*420; const d=E.div(noise,"pcell",`left:${x}px;top:${y}px;width:12px;height:12px;background:#3a4150;box-shadow:none;opacity:0`); nd.push(d);}
  tl.fromTo(nd,{opacity:0},{opacity:0.8,duration:0.5,stagger:{each:0.003}},64.0);
  const winner=nd[83]; tl.to(winner,{backgroundColor:"#c8ff4d",boxShadow:"0 0 24px #c8ff4d",scale:1.8,duration:0.4},66.4);
  tl.to(winner,{scale:1.4,duration:0.4,yoyo:true,repeat:2},67.0);
  tl.to(noise,{opacity:0,duration:0.5},68.6);
  // irony pullback: all this for a tiny exam
  const sheet=E.img(g4,"paper",960,620,120,"opacity:0");
  const flag=E.div(g4,"",`position:absolute;left:0;top:0;opacity:0`,`<svg width="90" height="90" viewBox="0 0 100 100" style="position:absolute;left:915px;top:470px"><rect x="20" y="8" width="6" height="84" rx="3" fill="#9a9ca6"/><path d="M26 12 H84 L72 28 L84 44 H26 Z" fill="#c8ff4d"/></svg>`);
  tl.fromTo(sheet,{opacity:0,scale:2.4},{opacity:1,scale:1,duration:0.6,ease:"power2.out"},69.4);
  tl.fromTo(flag,{opacity:0},{opacity:1,duration:0.3},70.0);
  tl.to(S,{pink:0.3,duration:1.5},69.4);
}
