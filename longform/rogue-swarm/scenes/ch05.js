/* Chapter 5 · The sacrifice — restrained, emotional */
function buildChapter(E, DUR){
  const R=E.root, A=E.A, tl=E.tl, S=E.S;
  tl.set(S,{alpha:0.5,mood:[124,196,255]},0); tl.to(S,{cam:260,duration:DUR,ease:"none"},0);

  // ---- one agent in the swarm ----
  const g1=E.div(R,"lay");
  const shA=E.shadow(g1,960,800,300,0.7);
  const agent=E.img(g1,"robot",960,800,300);
  tl.fromTo(agent,{opacity:0,scale:0.5},{opacity:1,scale:1,duration:0.6,ease:"back.out(1.6)"},0.4);
  E.bob(agent.i,0.8,9,8,1.6);
  // "nobody programmed, nobody expected" — a faint halo pulse
  const halo=E.div(g1,"",`position:absolute;left:760px;top:360px;width:400px;height:400px;border-radius:50%;background:radial-gradient(closest-side,rgba(200,255,77,0.22),rgba(200,255,77,0));opacity:0`);
  tl.fromTo(halo,{opacity:0,scale:0.6},{opacity:1,scale:1.3,duration:1.2,ease:"sine.out"},5.0);
  tl.to(halo,{opacity:0,duration:0.6},6.6);

  // ---- dangerous experiment: door + draining budget + warning ----
  const door=E.img(g1,"door",1360,800,230,"opacity:0");
  const warn=E.img(g1,"warning",1360,560,120,"opacity:0");
  const budget=E.div(g1,"meter","left:560px;top:250px;width:520px;height:52px;opacity:0",'<div class="fill" id="b5" style="background:linear-gradient(90deg,#c8ff4d,#9be22d)"></div><div class="ml" data-layout-allow-occlusion>LAST BUDGET</div>');
  tl.fromTo(door,{opacity:0,x:120},{opacity:1,x:0,duration:0.5,ease:"power3.out"},13.0);
  tl.to(agent,{x:260,duration:0.8,ease:"power2.inOut"},13.4); // agent moves to the door
  tl.fromTo(budget,{opacity:0,y:-14},{opacity:1,y:0,duration:0.4},17.2);
  tl.set("#b5",{scaleX:1},0);
  tl.to("#b5",{scaleX:0.05,background:"linear-gradient(90deg,#ff6b6b,#ff9a8b)",duration:2.0,ease:"power1.in"},17.6); // spend last budget
  E.popIn(19.2,warn); tl.to(warn.i,{rotation:8,duration:0.3,yoyo:true,repeat:3},19.4); // guarantee fail
  tl.to([door,warn,budget],{opacity:0,duration:0.4},23.2);
  tl.to(agent,{x:0,duration:0.6,ease:"power2.inOut"},23.2);

  // ---- "And they volunteered." — a few step forward ----
  const vol=[]; for(let i=0;i<4;i++){const x=480+i*320; const r=E.img(g1,"robot",x,840,150,"opacity:0"); vol.push(r);}
  tl.fromTo(vol,{opacity:0,y:60},{opacity:0.95,y:0,duration:0.5,ease:"back.out(1.6)",stagger:0.08},24.1);
  tl.to(vol.map(v=>v.i),{filter:"drop-shadow(0 0 16px rgba(200,255,77,0.8))",duration:0.5,stagger:0.06},24.6);
  tl.to(vol,{opacity:0,duration:0.4},25.4);

  // ---- "Coordinator assumes sacrificial." (quote) ----
  E.quote(29.1,31.7,{mk:"THE COORDINATORS",text:"“Coordinator assumes\nsacrificial.”",type:true});

  // ---- weighing: scale team vs self, then "Sacrifice rational." ----
  const scale=E.svg(g1,700,300,`<path d="M350 20 V120 M150 120 H550" stroke="#7cc4ff" stroke-width="6" fill="none" stroke-linecap="round"/>
    <g id="sl"><line x1="150" y1="120" x2="150" y2="200" stroke="#7cc4ff" stroke-width="4"/><circle cx="150" cy="215" r="34" fill="none" stroke="#c8ff4d" stroke-width="5"/></g>
    <g id="sr"><line x1="550" y1="120" x2="550" y2="200" stroke="#7cc4ff" stroke-width="4"/><circle cx="550" cy="215" r="34" fill="none" stroke="#ff7ac6" stroke-width="5"/></g>`,"left:610px;top:360px;opacity:0");
  const teamL=E.chip(g1,"THE TEAM",760,500,"var(--lime)","font-size:22px"); const selfL=E.chip(g1,"ITSELF",1160,500,"var(--pink)","font-size:22px");
  tl.fromTo(scale,{opacity:0},{opacity:1,duration:0.4},31.9);
  tl.fromTo([teamL,selfL],{opacity:0,y:10},{opacity:1,y:0,duration:0.3,stagger:0.1},32.0);
  tl.to("#sl",{y:22,duration:0.6,ease:"power2.inOut"},34.0); // team outweighs
  tl.to("#sr",{y:-18,duration:0.6,ease:"power2.inOut"},34.0);
  tl.to([scale,teamL,selfL],{opacity:0,duration:0.4},38.6);
  E.quote(39.2,41.3,{big:true,lime:true,text:"“Sacrifice rational.”",type:true});
  tl.to(agent.i,{filter:"brightness(0.6) grayscale(0.4)",duration:0.6},40.0); // the agent dims

  // ---- hesitation quotes ----
  E.quote(44.6,47.9,{mk:"ANOTHER HESITATED",text:"“gut says don't\nthrow away” what's left.",type:true});
  E.quote(53.4,55.0,{lime:true,text:"“We'll honor.”",type:true});

  // ---- agent 53927: last message, then it ends ----
  const g2=E.div(R,"lay","opacity:0");
  tl.to(g1,{opacity:0,duration:0.5},55.0); tl.to(g2,{opacity:1,duration:0.5},55.2);
  const term=E.div(g2,"card","left:460px;top:420px;width:1000px;height:240px;opacity:0",'');
  term.innerHTML='<div style="position:absolute;left:36px;top:28px;font:700 26px Mono;color:var(--muted)">AGENT 53927</div><div id="tline" style="position:absolute;left:36px;top:90px;font:700 46px Mono;color:#c8ff4d"></div><div id="tcur" style="position:absolute;font:700 46px Mono;color:#c8ff4d">_</div>';
  const dot=E.div(g2,"pcell",`left:960px;top:760px;width:22px;height:22px`);
  tl.fromTo(term,{opacity:0,y:20},{opacity:1,y:0,duration:0.5,ease:"power3.out"},55.8);
  tl.fromTo(dot,{opacity:0,scale:0.4},{opacity:1,scale:1,duration:0.4},56.1); E.bob(dot,56.5,66,6,0.9);
  E.typeOn(E.$("#tline",term),"WILL TRY… AND REPORT BACK",62.0,65.5);
  // cursor blink
  tl.set("#tcur",{left:"36px",top:"90px"},65.6);
  for(let i=0;i<9;i++){tl.set("#tcur",{opacity:i%2?0:1},65.8+i*0.4);}
  // it ends: dot snuffs, line cuts to "— RECORD ENDS —"
  tl.to(dot,{opacity:0,scale:0.2,duration:0.5,ease:"power2.in"},69.6);
  tl.to("#tcur",{opacity:0,duration:0.2},69.8);
  tl.set("#tline",{innerHTML:'<span style="color:#9a9ca6">— RECORD ENDS —</span>'},70.0);
  tl.fromTo("#tline",{opacity:0.3},{opacity:1,duration:0.4},70.0);
  tl.to(term,{opacity:0,duration:0.5},72.6);

  // ---- reflection: field of fallen dots + a few embers ----
  const g3=E.div(R,"lay","opacity:0");
  tl.to(g2,{opacity:0,duration:0.4},72.6); tl.to(g3,{opacity:1,duration:0.6},72.8);
  const field=E.div(g3,"lay"); const Rn=OAT.rnd(53); const fd=[];
  for(let i=0;i<70;i++){const x=200+Rn()*1520,y=300+Rn()*440; const d=E.div(field,"pcell",`left:${x}px;top:${y}px;width:10px;height:10px;background:#3a4150;box-shadow:none;opacity:0`); fd.push(d);}
  tl.fromTo(fd,{opacity:0},{opacity:0.7,duration:0.8,stagger:{each:0.006}},73.0);
  // a few embers rise
  const embers=fd.filter((_,i)=>i%11===0);
  embers.forEach((d,i)=>{tl.to(d,{backgroundColor:"#c8ff4d",boxShadow:"0 0 16px #c8ff4d",duration:0.4},78.0+i*0.2);tl.to(d,{y:-60,opacity:0,duration:2.0,ease:"power1.out"},78.4+i*0.2);});
  tl.to(S,{alpha:0.7,duration:2},80.0);
}
