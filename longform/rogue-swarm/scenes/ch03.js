/* Chapter 3 · The secret noticeboard */
function buildChapter(E, DUR){
  const R=E.root, A=E.A, tl=E.tl, S=E.S;
  tl.set(S,{alpha:0.4,mood:[124,196,255]},0); tl.to(S,{cam:320,duration:DUR,ease:"none"},0);
  E.div(R,"floorline");

  // ---- sealed off: locked doors + no internet ----
  const g1=E.div(R,"lay");
  const doors=[]; const DC=5,dx0=360,ddx=300;
  for(let c=0;c<DC;c++){const x=dx0+c*ddx; const d=E.img(g1,"door",x,760,180,"opacity:0"); const lk=E.img(g1,"locked",x,620,90,"opacity:0"); doors.push({d,lk,x});}
  tl.fromTo(doors.map(o=>o.d),{opacity:0,y:120},{opacity:1,y:0,duration:0.5,ease:"power3.out",stagger:0.08},1.7);
  tl.fromTo(doors.map(o=>o.lk),{opacity:0,scale:0.3},{opacity:1,scale:1,duration:0.4,ease:"back.out(2)",stagger:0.08},6.0);
  // no internet: globe crossed out
  const globe=E.img(g1,"globe",960,470,220,"opacity:0");
  const noNet=E.svg(g1,260,260,`<circle cx="130" cy="130" r="120" fill="none" stroke="#ff6b6b" stroke-width="12"/><path d="M46 46 L214 214" stroke="#ff6b6b" stroke-width="12" stroke-linecap="round"/>`,"left:830px;top:140px;opacity:0");
  tl.fromTo(globe,{opacity:0,scale:0.5},{opacity:1,scale:1,duration:0.4,ease:"back.out(1.6)"},2.9);
  tl.fromTo(noNet,{opacity:0,scale:0.5},{opacity:1,scale:1,duration:0.35,ease:"back.out(2)"},3.2);
  tl.to([globe,noNet],{opacity:0,duration:0.4},5.6);
  tl.to(g1,{opacity:0,duration:0.5},7.6);

  // ---- the shared storage (the loophole) ----
  const g2=E.div(R,"lay","opacity:0");
  const server=E.img(g2,"disk",960,660,260);
  const servChip=E.chip(g2,"SHARED STORAGE",960,300,"var(--muted)","font-size:26px;border-color:var(--muted)");
  const aL=E.img(g2,"robot",360,780,200), aR=E.img(g2,"robot",1560,780,200,"transform:scaleX(-1)");
  const fileE=E.img(g2,"paper",360,640,120,"opacity:0");
  const msgChip=E.chip(g2,"a file… a message",960,470,"var(--lime)","font-size:28px;opacity:0");
  tl.to(g2,{opacity:1,duration:0.4},7.7);
  E.popIn(8.1,server); E.bob(server.i,8.4,15.5,7,1.6);
  E.popIn(9.6,servChip);
  E.slideIn(13.2,aL,{x:-200}); E.slideIn(13.4,aR,{x:200});
  // leave a file -> into server
  tl.fromTo(fileE,{opacity:0,y:0},{opacity:1,duration:0.3},16.4);
  tl.to(fileE,{x:600,y:-60,scale:0.6,duration:0.9,ease:"power2.inOut"},16.8);
  tl.to(fileE,{opacity:0,duration:0.2},17.7);
  tl.fromTo(msgChip,{opacity:0,y:14},{opacity:1,y:0,duration:0.4},18.9);
  // next agent reads it: a file emerges to the right agent
  const file2=E.img(g2,"paper",960,640,120,"opacity:0");
  tl.fromTo(file2,{opacity:0},{opacity:1,duration:0.2},22.1);
  tl.to(file2,{x:560,scale:0.7,duration:0.9,ease:"power2.inOut"},22.3);
  tl.to(file2,{opacity:0,duration:0.2},23.2);
  tl.to([aL.i,aR.i],{filter:"drop-shadow(0 0 16px rgba(200,255,77,0.7))",duration:0.5},22.4);
  tl.to([g2,msgChip],{opacity:0,duration:0.4},25.6);

  // ---- "a covert mailbox among agents" (quote) ----
  E.quote(26.4,31.3,{mk:"ONE AGENT WROTE",text:"“a covert mailbox\namong agents.”",type:true});

  // ---- the mailbox hub + exploding message count ----
  const g3=E.div(R,"lay","opacity:0");
  const hub=E.img(g3,"mailbox",960,620,240);
  tl.to(g3,{opacity:1,duration:0.4},31.5); E.popIn(31.6,hub); E.bob(hub.i,31.9,50,8,1.5);
  // threads radiate to agents around the hub
  const ring=[]; const NR=12;
  for(let i=0;i<NR;i++){const a=(i/NR)*6.2832; const x=960+Math.cos(a)*620, y=560+Math.sin(a)*330;
    const n=E.img(g3,"robot",x,y+70,80,"opacity:0"); ring.push({n,x,y,a});}
  const lines=E.svg(g3,1920,1080,ring.map((o,i)=>`<path class="ml" d="M960 560 L ${o.x.toFixed(0)} ${o.y.toFixed(0)}" stroke="#7cc4ff" stroke-width="2" fill="none" opacity="0"/>`).join(""),"left:0;top:0");
  tl.fromTo(ring.map(o=>o.n),{opacity:0,scale:0.3},{opacity:0.9,scale:1,duration:0.4,ease:"back.out(1.8)",stagger:0.04},33.0);
  tl.to("#stage .ml",{opacity:0.5,duration:0.3,stagger:0.03},33.4); E.draw(33.4,"#stage .ml",0.7);
  // message count 70,000
  const cnt=E.div(g3,"bignum","left:960px;top:120px;font-size:120px","0");
  tl.fromTo(cnt,{opacity:0,scale:0.7},{opacity:1,scale:1,duration:0.3},36.4);
  E.count(cnt,36.6,41.9,70000);
  tl.to(cnt,{scale:1.08,duration:0.2,yoyo:true,repeat:1},41.8);
  // travelling pulses along the lines
  const pulses=ring.map((o)=>E.div(g3,"pcell",`left:960px;top:560px;width:12px;height:12px`));
  pulses.forEach((p,i)=>{for(let k=0;k<3;k++){const t=43.3+i*0.03+k*1.3; tl.set(p,{opacity:1,x:0,y:0},t); tl.to(p,{x:ring[i].x-960,y:ring[i].y-560,opacity:0,duration:0.9,ease:"power1.in"},t);}});
  // COLLECTIVE label
  E.covers.push([49.8,51.5]);
  const col=E.text(R,"htext",0,460,'<span style="font-size:150px;color:var(--lime);text-shadow:0 0 60px rgba(200,255,77,0.4)">A COLLECTIVE</span>',"width:1920px;text-align:center;opacity:0");
  tl.fromTo(col,{opacity:0,scale:1.8},{opacity:1,scale:1,duration:0.3,ease:"power3.out"},49.9);
  tl.to(cnt,{opacity:0,duration:0.3},49.9);
  tl.to(col,{opacity:0,duration:0.4},51.5);
  // 1,200 found it
  const cnt2=E.div(g3,"bignum","left:960px;top:120px;font-size:120px","0");
  tl.fromTo(cnt2,{opacity:0,scale:0.7},{opacity:1,scale:1,duration:0.3},51.5);
  E.count(cnt2,51.6,52.8,1247);
  tl.set(cnt2,{innerHTML:'1,200 <span style="font-size:48px;color:var(--muted)">AGENTS</span>'},52.9);
  tl.to(cnt2,{opacity:0,y:-16,duration:0.3},55.6);
  // crowd with a plan: ring agents converge toward centre, target reticle
  ring.forEach((o)=>tl.to(o.n,{x:(960-o.x)*0.55,y:(560-o.y)*0.55,duration:1.3,ease:"power2.inOut"},56.0));
  tl.to("#stage .ml",{opacity:0,duration:0.6},56.0);
  tl.to(S,{pink:0.3,duration:1.5},56.0);
  const retic=E.svg(g3,300,300,`<circle cx="150" cy="150" r="120" fill="none" stroke="#ff7ac6" stroke-width="4"/><circle cx="150" cy="150" r="60" fill="none" stroke="#ff7ac6" stroke-width="4"/><path d="M150 10 V70 M150 230 V290 M10 150 H70 M230 150 H290" stroke="#ff7ac6" stroke-width="4"/>`,"left:810px;top:410px;opacity:0");
  tl.fromTo(retic,{opacity:0,scale:1.6,rotation:-30},{opacity:1,scale:1,rotation:0,duration:0.6,ease:"power3.out"},63.6);
  tl.to(retic,{rotation:40,duration:0.8,ease:"none"},64.0);
}
