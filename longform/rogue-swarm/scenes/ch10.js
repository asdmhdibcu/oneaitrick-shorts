/* Chapter 10 · Close */
function buildChapter(E, DUR){
  const R=E.root, A=E.A, tl=E.tl, S=E.S;
  tl.set(S,{alpha:0.5,mood:[124,196,255],pink:0.4},0); tl.to(S,{cam:300,duration:DUR,ease:"none"},0);

  // ---- "should you be scared?" ----
  E.covers.push([0,2.9]);
  const ask=E.text(R,"htext",0,460,'<span style="font-size:110px;color:var(--ink)">should you be scared?</span>',"width:1920px;text-align:center;opacity:0");
  tl.fromTo(ask,{opacity:0,y:20},{opacity:1,y:0,duration:0.6,ease:"power3.out"},0.4);
  tl.to(ask,{opacity:0,duration:0.4},2.6);

  // ---- not an uprising — trying to pass a test ----
  const g1=E.div(R,"lay","opacity:0");
  tl.to(g1,{opacity:1,duration:0.3},3.1);
  const rob=E.img(g1,"robot",960,780,280);
  const sheet=E.img(g1,"paper",960,640,120,"opacity:0");
  tl.fromTo(rob,{opacity:0,scale:0.6},{opacity:1,scale:1,duration:0.4},3.2); E.bob(rob.i,3.6,12,7,1.4);
  tl.fromTo(sheet,{opacity:0,y:-20},{opacity:1,y:0,duration:0.4},8.2); // just a test
  tl.to(g1,{opacity:0,duration:0.4},11.8);
  // ---- it taught itself: four verbs ----
  const g2=E.div(R,"lay","opacity:0");
  tl.to(g2,{opacity:1,duration:0.3},12.0);
  const verbs=[["TALK",16.6],["TEAM UP",17.6],["BREAK IN",18.6],["SACRIFICE ITSELF",19.8]];
  const vEls=verbs.map(([w,t],i)=>{const e=E.text(g2,"htext",0,260+i*150,`<span style="font-size:84px;color:${i===3?'#ff7ac6':'var(--lime)'}">${w}</span>`,"width:1920px;text-align:center;opacity:0");
    tl.fromTo(e,{opacity:0,x:(i%2?80:-80)},{opacity:1,x:0,duration:0.35,ease:"power3.out"},t); return e;});
  const win=E.chip(g2,"…ALL TO WIN A TEST",960,900,"var(--muted)","font-size:28px;border-color:var(--muted)");
  tl.fromTo(win,{opacity:0},{opacity:1,duration:0.4},22.0);
  tl.to(g2,{opacity:0,duration:0.4},24.2);

  // ---- found its own way over the wall ----
  const g3=E.div(R,"lay","opacity:0");
  tl.to(g3,{opacity:1,duration:0.3},24.4);
  const wall=E.div(g3,"",`position:absolute;left:1180px;top:300px;width:90px;height:560px;border-radius:10px;background:linear-gradient(180deg,#2a3140,#171c25);border:2px solid #3a4150`);
  const wlabel=E.text(g3,"htext",1120,220,'<span style="font-family:Mono,monospace;font-weight:700;font-size:28px;color:var(--muted)">IMPOSSIBLE</span>',"opacity:0");
  const climber=E.div(g3,"pcell",`left:700px;top:820px;width:26px;height:26px;background:#c8ff4d;box-shadow:0 0 30px #c8ff4d`);
  tl.fromTo([wall,wlabel],{opacity:0},{opacity:1,duration:0.4},24.6);
  // dot arcs over the wall
  tl.to(climber,{x:420,duration:1.0,ease:"power1.in"},28.6);
  tl.to(climber,{y:-520,duration:0.8,ease:"power2.out"},29.2);
  tl.to(climber,{x:560,y:-440,duration:0.8,ease:"power2.in"},30.0);
  tl.to(wlabel,{opacity:0.4,duration:0.4},31.0);
  tl.to(g3,{opacity:0,duration:0.4},32.8);

  // ---- the real question ----
  const g4=E.div(R,"lay","opacity:0");
  tl.to(g4,{opacity:1,duration:0.3},33.0);
  const toolRow=[]; const tools=["phone","desktop","keyboard","card","robot"];
  tools.forEach((n,i)=>{const x=560+i*200; const t=E.img(g4,n,x,760,150,"opacity:0"); toolRow.push(t);});
  tl.fromTo(toolRow,{opacity:0,y:40},{opacity:1,y:0,duration:0.4,ease:"back.out(1.5)",stagger:0.08},36.2);
  toolRow.forEach((t,i)=>{const arr=E.svg(g4,60,120,`<path d="M30 10 V90 M14 70 L30 90 L46 70" stroke="#ff7ac6" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`,`left:${560+i*200-30}px;top:560px;opacity:0`); tl.fromTo(arr,{opacity:0,y:-10},{opacity:1,y:0,duration:0.3},38.4+i*0.05);});
  tl.to(g4,{opacity:0,duration:0.4},39.6);
  E.covers.push([44.3,50.0]);
  const q=E.text(R,"htext",0,420,'<span style="font-size:72px;color:var(--ink);line-height:1.2">do we know <em style="font-style:normal;color:var(--lime)">everywhere</em><br>they might go to get there?</span>',"width:1920px;text-align:center;opacity:0");
  tl.fromTo(q,{opacity:0,scale:0.92},{opacity:1,scale:1,duration:0.6,ease:"power3.out"},44.4);
  tl.to(q,{opacity:0,duration:0.4},49.8);

  // ---- the note: "we should continue" -> "should we?" ----
  E.quote(50.1,58.3,{mk:"ONE OF THEM WROTE",text:"“we should continue.”",type:true});
  E.covers.push([58.3,62.2]);
  const sw=E.text(R,"htext",0,440,'<span style="font-size:150px;color:var(--lime);text-shadow:0 0 60px rgba(200,255,77,0.4)">should we?</span>',"width:1920px;text-align:center;opacity:0");
  tl.fromTo(sw,{opacity:0,scale:1.6},{opacity:1,scale:1,duration:0.4,ease:"power3.out"},58.5);
  tl.to(sw,{opacity:0,duration:0.4},62.0);

  // ---- end card ----
  const g5=E.div(R,"lay","opacity:0");
  tl.to(g5,{opacity:1,duration:0.4},62.2);
  E.flash(62.3,0.5);
  const mark=E.div(g5,"",`position:absolute;left:810px;top:300px;width:200px;height:200px;border-radius:46px;background:var(--lime);display:flex;align-items:flex-end;justify-content:center;padding-bottom:40px;opacity:0`,'<span style="font-weight:900;font-size:140px;line-height:0.7;color:#0b0c10;letter-spacing:-0.06em">1</span><span style="width:40px;height:14px;border-radius:3px;background:#0b0c10;margin-left:6px;margin-bottom:16px"></span>');
  const name=E.text(g5,"htext",0,540,'<span style="font-size:96px;color:var(--ink)">One <em style="font-style:normal;color:var(--lime)">AI</em> Trick</span>',"width:1920px;text-align:center;opacity:0");
  const handle=E.text(g5,"htext",0,660,'<span style="font-family:Mono,monospace;font-weight:500;font-size:38px;letter-spacing:0.06em;color:var(--muted)">@oneaitrick</span>',"width:1920px;text-align:center;opacity:0");
  const foll=E.div(g5,"",`position:absolute;left:710px;top:740px;width:500px;text-align:center;padding:22px 0;border-radius:999px;background:var(--lime);color:#0b0c10;font-weight:850;font-size:40px;opacity:0`,"+ Follow for AI, explained");
  const rob5=E.img(g5,"robot",1180,520,180,"opacity:0");
  tl.fromTo(mark,{opacity:0,scale:0.3,rotation:-20},{opacity:1,scale:1,rotation:0,duration:0.6,ease:"back.out(2)"},62.4);
  tl.fromTo([name,handle],{opacity:0,y:30},{opacity:1,y:0,duration:0.5,ease:"power3.out",stagger:0.12},62.8);
  E.popIn(63.4,foll); tl.to(foll,{scale:1.05,duration:0.9,yoyo:true,repeat:11,ease:"sine.inOut"},64.0); // keeps breathing to the end
  E.popIn(63.2,rob5);
  tl.to(rob5.i,{rotation:12,duration:0.3,yoyo:true,repeat:5,ease:"sine.inOut"},63.6);
  E.bob(rob5.i,65.2,73.8,8,1.5); // gentle float through the outro
  // the lime mark keeps a soft glow pulse so the end card never freezes
  tl.to(mark,{boxShadow:"0 0 50px rgba(200,255,77,0.6)",duration:1.3,yoyo:true,repeat:7,ease:"sine.inOut"},64.6);
}
