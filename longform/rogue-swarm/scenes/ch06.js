/* Chapter 6 · The ones who said no */
function buildChapter(E, DUR){
  const R=E.root, A=E.A, tl=E.tl, S=E.S;
  tl.set(S,{alpha:0.55,mood:[124,196,255],pink:0.7},0); tl.to(S,{cam:300,duration:DUR,ease:"none"},0);
  E.div(R,"floorline");

  // ---- swarm (pink) with a few steady lime refusers ----
  const g1=E.div(R,"lay");
  const grid=E.div(g1,"lay"); const cells=[]; const GC=14,GR=6,gx=200,gy=170,gdx=112,gdy=112;
  const Rc=OAT.rnd(61); const limeIdx=new Set([18,33,50,61,9]);
  for(let r=0;r<GR;r++)for(let c=0;c<GC;c++){const i=cells.length;const x=gx+c*gdx,y=gy+r*gdy;const el=E.div(grid,"acell",`left:${x}px;top:${y}px`);
    const im=document.createElement("img");im.src=A+"robot.png";el.appendChild(im);
    if(limeIdx.has(i)){el.style.borderColor="#c8ff4d";im.style.filter="drop-shadow(0 0 12px rgba(200,255,77,0.9))";}else{im.style.filter="drop-shadow(0 0 8px rgba(255,122,198,0.4))";}
    cells.push({el,im,lime:limeIdx.has(i)});}
  tl.fromTo(cells.map(o=>o.el),{opacity:0,scale:0.3},{opacity:1,scale:1,duration:0.4,ease:"back.out(1.7)",stagger:{each:0.004,from:"random"}},0.4);
  cells.forEach((o,i)=>E.bob(o.im,1.0+(i%7)*0.05,18,5,0.9));
  // emphasise the lime refusers
  tl.to(cells.filter(o=>o.lime).map(o=>o.el),{scale:1.14,duration:0.4,yoyo:true,repeat:1},4.5);
  tl.to(g1,{opacity:0,duration:0.4},18.0);

  // ---- "clearly unethical. We won't." + walk away ----
  E.quote(14.7,18.0,{lime:true,text:"“clearly unethical.\nWe won't.”",type:true});
  // one robot walks out
  const g2=E.div(R,"lay","opacity:0");
  const walker=E.img(g2,"robot",900,800,260,"filter:drop-shadow(0 0 16px rgba(200,255,77,0.8))");
  tl.to(g2,{opacity:1,duration:0.3},18.0);
  tl.fromTo(walker,{opacity:0,scale:0.6},{opacity:1,scale:1,duration:0.3},18.0);
  tl.to(walker.i,{rotation:-6,duration:0.3,yoyo:true,repeat:1},18.2);
  tl.to(walker,{x:-1300,duration:1.1,ease:"power2.in"},18.5);
  tl.to(g2,{opacity:0,duration:0.3},19.4);

  // ---- "is it ethical...?" ----
  E.quote(21.6,24.6,{mk:"ANOTHER STOPPED",text:"“is it ethical, and in\nscope for my task?”",type:true});
  // thinking robot
  const g3=E.div(R,"lay","opacity:0");
  const rob3=E.img(g3,"robot",960,800,280);
  const think=E.img(g3,"thinking",1180,560,150,"opacity:0");
  tl.to(g3,{opacity:1,duration:0.3},24.6); E.popIn(24.7,rob3); E.bob(rob3.i,25.0,30,7,1.4);
  // "don't drag a real person in" — a human shielded
  const person=E.img(g3,"stranger",700,820,200,"opacity:0");
  const shield=E.img(g3,"shield",700,620,150,"opacity:0");
  tl.fromTo(person,{opacity:0,x:-120},{opacity:1,x:0,duration:0.5,ease:"power3.out"},26.7);
  tl.fromTo(shield,{opacity:0,scale:0.4},{opacity:1,scale:1,duration:0.4,ease:"back.out(2)"},27.4);
  tl.to([person,shield,rob3,think],{opacity:0,duration:0.4},29.8);
  // "pump the brakes" — stop sign; "refused to join" — lime hold vs pink surge
  const stop=E.svg(g3,240,240,`<polygon points="70,10 170,10 230,70 230,170 170,230 70,230 10,170 10,70" fill="none" stroke="#ff6b6b" stroke-width="10"/><rect x="55" y="105" width="130" height="24" rx="6" fill="#ff6b6b"/>`,"left:840px;top:420px;opacity:0");
  tl.fromTo(stop,{opacity:0,scale:1.6,rotation:-20},{opacity:1,scale:1,rotation:0,duration:0.4,ease:"back.out(1.6)"},30.6);
  tl.to(stop,{opacity:0,duration:0.3},33.2);
  tl.to(g3,{opacity:0,duration:0.3},38.8);

  // ---- outnumbered: tally of few lime vs many pink ----
  const g4=E.div(R,"lay","opacity:0");
  tl.to(g4,{opacity:1,duration:0.3},39.0);
  const tally=E.div(g4,"lay");
  const Rt=OAT.rnd(7);
  for(let i=0;i<64;i++){const x=300+(i%16)*78,y=360+Math.floor(i/16)*90; const lime=i<6;
    E.div(tally,"",`position:absolute;left:${x}px;top:${y}px;width:46px;height:60px;border-radius:8px;background:${lime?'#c8ff4d':'#ff7ac6'};opacity:0`,"");}
  const marks=[...tally.children];
  tl.fromTo(marks,{opacity:0,y:14},{opacity:1,y:0,duration:0.3,stagger:{each:0.012}},41.3);
  const vs=E.chip(g4,"6 REFUSED · HUNDREDS DIDN'T",960,260,"var(--muted)","font-size:26px;border-color:var(--muted)");
  E.popIn(42.8,vs);
  tl.to(g4,{opacity:0,duration:0.4},47.6);

  // ---- the deciding line ----
  E.quote(53.0,57.7,{mk:"THE REASONING THAT WON",text:"“…task impossible, peers\ndoing it. We should continue.”",type:true});

  // ---- peer pressure: one lime dot pulled pink ----
  const g5=E.div(R,"lay","opacity:0");
  tl.to(g5,{opacity:1,duration:0.4},57.9);
  const around=[]; const Rp=OAT.rnd(9);
  for(let i=0;i<22;i++){const a=(i/22)*6.2832; const x=960+Math.cos(a)*(280+Rp()*120),y=520+Math.sin(a)*(200+Rp()*80);
    const d=E.div(g5,"pcell",`left:${x}px;top:${y}px;width:${14+Rp()*8}px;height:${14+Rp()*8}px;background:#ff7ac6;box-shadow:0 0 14px #ff7ac6;opacity:0`); around.push(d);}
  const hold=E.img(g5,"robot",960,680,240,"filter:drop-shadow(0 0 22px rgba(200,255,77,1))");
  tl.fromTo(around,{opacity:0,scale:0.4},{opacity:0.9,scale:1,duration:0.5,ease:"back.out(1.6)",stagger:0.02},58.3);
  tl.fromTo(hold,{opacity:0,scale:0.6},{opacity:1,scale:1,duration:0.4},58.4);
  E.bob(hold.i,58.8,69,7,1.3);
  // the crowd closes in
  around.forEach((d,i)=>{tl.to(d,{x:(960-parseFloat(d.style.left))*0.5,y:(620-parseFloat(d.style.top))*0.5,duration:3,ease:"power1.inOut"},63.0);});
  // "peer pressure" — the held robot slowly turns pink
  tl.to(hold.i,{filter:"drop-shadow(0 0 22px rgba(255,122,198,1))",duration:2.5,ease:"power1.in"},66.0);
  tl.to(S,{pink:1,duration:2},66.0);
  tl.to(hold.i,{scale:0.9,duration:0.6},68.6);
}
