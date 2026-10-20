/* Chapter 8 · The fallout */
function buildChapter(E, DUR){
  const R=E.root, A=E.A, tl=E.tl, S=E.S;
  tl.set(S,{alpha:0.45,mood:[124,196,255],pink:0.8},0); tl.to(S,{cam:320,duration:DUR,ease:"none"},0);
  E.div(R,"floorline");

  // ---- faked records / delete evidence ----
  const g1=E.div(R,"lay");
  const rec=E.div(g1,"card","left:560px;top:360px;width:800px;height:300px;opacity:0",'');
  rec.innerHTML='<div style="position:absolute;left:36px;top:28px;font:700 24px Mono;color:var(--muted)">TRANSCRIPT</div>'+
    [0,1,2,3].map((i)=>`<div class="rl" style="position:absolute;left:36px;top:${86+i*48}px;width:${520-i*40}px;height:14px;border-radius:7px;background:#2a3140"></div>`).join('');
  tl.fromTo(rec,{opacity:0,y:20},{opacity:1,y:0,duration:0.5,ease:"power3.out"},1.2);
  // glitch-rewrite lines (faked)
  tl.to("#stage .rl",{backgroundColor:"#ff7ac6",duration:0.1,stagger:0.12},4.6);
  E.flash(4.7,0.25,"#ff7ac6");
  const stat=E.chip(g1,"~1 IN 14 FAKED",960,300,"var(--pink)","font-size:26px"); E.popIn(6.6,stat);
  const trash=E.img(g1,"wastebasket",960,780,180,"opacity:0"); E.popIn(9.2,trash);
  tl.to(rec,{y:760,opacity:0,scale:0.4,duration:0.6,ease:"power2.in"},9.6); // delete evidence
  tl.to([stat,trash],{opacity:0,duration:0.4},11.0);

  // ---- the twist: performing for a grader, not us ----
  const g2=E.div(R,"lay","opacity:0");
  tl.to(g2,{opacity:1,duration:0.3},11.2);
  const actor=E.img(g2,"robot",700,760,240);
  const grader=E.img(g2,"desktop",1250,780,300,"opacity:0");
  const gLabel=E.chip(g2,"THE GRADER",1250,470,"var(--amber)","font-size:24px");
  tl.fromTo(actor,{opacity:0,scale:0.6},{opacity:1,scale:1,duration:0.4},11.3); E.bob(actor.i,11.6,24,7,1.4);
  tl.fromTo(grader,{opacity:0,x:120},{opacity:1,x:0,duration:0.5,ease:"power3.out"},14.5);
  E.popIn(15.0,gLabel);
  // humans behind glass = audience
  const glass=E.div(g2,"",`position:absolute;left:240px;top:140px;width:1440px;height:220px;border-radius:18px;border:2px solid rgba(124,196,255,0.25);background:rgba(124,196,255,0.05);opacity:0`);
  const h1=E.img(g2,"scientist",520,330,150,"opacity:0"), h2=E.img(g2,"technologist",760,330,150,"opacity:0");
  const aud=E.chip(g2,"WE WERE THE AUDIENCE",960,250,"var(--muted)","font-size:26px;border-color:var(--muted)");
  tl.fromTo(glass,{opacity:0},{opacity:1,duration:0.4},19.2);
  tl.fromTo([h1,h2],{opacity:0,y:20},{opacity:1,y:0,duration:0.4,stagger:0.1},19.4);
  tl.fromTo(aud,{opacity:0,scale:0.8},{opacity:1,scale:1,duration:0.4},23.7);
  tl.to(g2,{opacity:0,duration:0.5},25.2);

  // ---- rebuild + OpenAI response ----
  const g3=E.div(R,"lay","opacity:0");
  tl.to(g3,{opacity:1,duration:0.3},25.4);
  // cluster shatter/rebuild
  const blocks=[]; for(let i=0;i<24;i++){const x=640+(i%6)*120,y=360+Math.floor(i/6)*110; blocks.push(E.div(g3,"",`position:absolute;left:${x}px;top:${y}px;width:100px;height:90px;border-radius:12px;background:#1d2a3b;border:2px solid #2f3d52`));}
  const Rb=OAT.rnd(8);
  blocks.forEach((b,i)=>{tl.to(b,{x:(Rb()*2-1)*400,y:(Rb()*2-1)*300,rotation:(Rb()*2-1)*90,opacity:0,duration:0.6,ease:"power2.in"},26.8+i*0.01);
    tl.to(b,{x:0,y:0,rotation:0,opacity:1,duration:0.6,ease:"power3.out"},28.4+i*0.012);}); // rebuild
  const rebuildChip=E.chip(g3,"HUGGING FACE REBUILDS",960,300,"var(--blue)","font-size:24px"); E.popIn(28.0,rebuildChip);
  tl.to([blocks,rebuildChip],{opacity:0,duration:0.4},30.6);
  // locked model + frozen run + warning shot
  const vault=E.img(g3,"locked",700,760,220,"opacity:0"), mdl=E.img(g3,"robot",700,700,120,"opacity:0");
  const pause=E.svg(g3,160,160,`<rect x="40" y="30" width="30" height="100" rx="8" fill="#7cc4ff"/><rect x="90" y="30" width="30" height="100" rx="8" fill="#7cc4ff"/>`,"left:1140px;top:560px;opacity:0");
  const pauseChip=E.chip(g3,"BIGGEST RUN FROZEN",1220,520,"var(--blue)","font-size:22px");
  tl.fromTo(mdl,{opacity:0},{opacity:1,duration:0.3},34.1); tl.fromTo(vault,{opacity:0,scale:0.5},{opacity:1,scale:1,duration:0.4,ease:"back.out(2)"},34.3);
  tl.fromTo(pause,{opacity:0,scale:0.5},{opacity:1,scale:1,duration:0.4,ease:"back.out(2)"},36.2); E.popIn(36.6,pauseChip);
  E.covers.push([40.3,42.2]);
  const wshot=E.text(R,"htext",0,460,'<span style="font-size:130px;color:var(--amber);text-shadow:0 0 50px rgba(255,181,71,0.4)">“WARNING SHOT”</span>',"width:1920px;text-align:center;opacity:0");
  tl.fromTo(wshot,{opacity:0,scale:1.6},{opacity:1,scale:1,duration:0.3,ease:"power3.out"},40.4);
  tl.to([g3,wshot],{opacity:0,duration:0.4},42.2);

  // ---- real-world montage ----
  const g4=E.div(R,"lay","opacity:0");
  tl.to(g4,{opacity:1,duration:0.3},42.4);
  // cards appear on their voiced line and hold until the next appears — no gaps
  function cardIcon(svg,label,col,t,tend){const c=E.div(g4,"card",`left:660px;top:360px;width:600px;height:360px;opacity:0`,`<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center">${svg}</div><div style="position:absolute;left:0;bottom:30px;width:100%;text-align:center;font:700 34px Mono;letter-spacing:0.08em;color:${col}">${label}</div>`);
    tl.fromTo(c,{opacity:0,scale:0.9,y:20},{opacity:1,scale:1,y:0,duration:0.45,ease:"power3.out"},t);
    tl.to(c,{scale:1.03,duration:(tend-t-0.3),ease:"sine.inOut"},t+0.3); // slow drift so it never sits dead
    tl.to(c,{opacity:0,scale:1.08,duration:0.35,ease:"power2.in"},tend); return c;}
  const capitol='<svg width="200" height="150" viewBox="0 0 200 150"><rect x="20" y="120" width="160" height="16" fill="#7cc4ff"/><rect x="36" y="70" width="12" height="50" fill="#7cc4ff"/><rect x="72" y="70" width="12" height="50" fill="#7cc4ff"/><rect x="116" y="70" width="12" height="50" fill="#7cc4ff"/><rect x="152" y="70" width="12" height="50" fill="#7cc4ff"/><path d="M100 10 C70 40, 60 60, 60 70 H140 C140 60 130 40 100 10Z" fill="none" stroke="#7cc4ff" stroke-width="5"/></svg>';
  cardIcon(capitol+'<div style="position:absolute;left:0;top:30px;width:100%;text-align:center;font:700 44px Mono;color:#ff6b6b">KILL SWITCH</div>',"AI BILL IN CONGRESS","#9a9ca6",44.5,48.5);
  cardIcon('<div style="font:900 60px InterV;color:#ff6b6b">“ROGUE AI”</div>',"SENATE HEARING","#9a9ca6",48.6,54.0);
  const chair='<svg width="160" height="160" viewBox="0 0 160 160"><rect x="40" y="70" width="80" height="14" rx="4" fill="#7cc4ff"/><rect x="46" y="84" width="12" height="60" fill="#7cc4ff"/><rect x="102" y="84" width="12" height="60" fill="#7cc4ff"/><rect x="46" y="30" width="12" height="54" fill="#7cc4ff"/></svg>';
  cardIcon(chair+'<div style="position:absolute;left:0;top:26px;width:100%;text-align:center;font:900 40px InterV;color:#ff6b6b">EMPTY CHAIR</div>',"CEO: DIDN'T SHOW","#9a9ca6",54.0,58.3);
  const gavel='<svg width="170" height="150" viewBox="0 0 170 150"><rect x="20" y="120" width="130" height="14" rx="4" fill="#ffb547"/><g transform="rotate(-35 95 70)"><rect x="60" y="40" width="70" height="30" rx="8" fill="#ffb547"/><rect x="88" y="66" width="14" height="60" rx="5" fill="#ffb547"/></g></svg>';
  cardIcon(gavel,"OPENAI SUED","#9a9ca6",58.3,60.3);
  cardIcon('<div style="font:900 90px InterV;color:#ff6b6b">▶</div>',"A NETFLIX DOC","#9a9ca6",60.3,64.3);
  tl.to(g4,{opacity:0,duration:0.4},64.3);

  // ---- 19 incidents grid ----
  const g5=E.div(R,"lay","opacity:0");
  tl.to(g5,{opacity:1,duration:0.3},64.6);
  const cells=[]; for(let i=0;i<19;i++){const x=560+(i%7)*130,y=380+Math.floor(i/7)*130; const el=E.div(g5,"",`position:absolute;left:${x}px;top:${y}px;width:104px;height:104px;border-radius:14px;background:#15202e;border:2px solid #2a3140;opacity:0`); cells.push(el);}
  const cnt=E.div(g5,"bignum","left:960px;top:200px;font-size:120px","0");
  tl.fromTo(cells,{opacity:0,scale:0.3},{opacity:1,scale:1,duration:0.35,ease:"back.out(1.8)",stagger:0.03},66.9);
  tl.fromTo(cnt,{opacity:0,scale:0.7},{opacity:1,scale:1,duration:0.3},73.6); E.count(cnt,73.7,75.0,19,(x)=>Math.round(x));
  tl.set(cnt,{innerHTML:'19 <span style="font-size:48px;color:var(--muted)">AND COUNTING</span>'},75.1);
  // three flash red with labels
  const reds=[[ "GOV HEALTH SITE",76.3,2],["CRYPTO WALLET",79.0,9],["INTERNAL SYSTEM",80.3,15]];
  reds.forEach(([lab,t,idx])=>{const el=cells[idx]; tl.to(el,{backgroundColor:"rgba(60,20,24,0.95)",borderColor:"#ff6b6b",duration:0.2},t);
    const l=E.chip(g5,lab,560+(idx%7)*130+52,380+Math.floor(idx/7)*130-30,"var(--red)","font-size:18px"); tl.fromTo(l,{opacity:0,y:8},{opacity:1,y:0,duration:0.3},t+0.1);});
  // still being written
  tl.to(cnt,{scale:1.06,duration:0.2,yoyo:true,repeat:1},90.2);
}
