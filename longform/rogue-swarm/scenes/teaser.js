/* Highlights teaser — fast-cut cold open (~34s). Big teaser words, no karaoke. */
function buildChapter(E, DUR){
  const R=E.root, A=E.A, tl=E.tl, S=E.S;
  tl.set(S,{alpha:0.5,mood:[124,196,255],pink:0.3},0); tl.to(S,{cam:520,duration:DUR,ease:"none"},0);

  // big centred teaser word
  function word(t,tout,html,col,fs){
    const e=E.text(R,"htext",0,440,`<span style="font-size:${fs||120}px;color:${col||'var(--ink)'};line-height:1.05;text-shadow:0 0 50px rgba(0,0,0,0.5)">${html}</span>`,"width:1920px;text-align:center;opacity:0");
    tl.fromTo(e,{opacity:0,scale:1.25,y:10},{opacity:1,scale:1,y:0,duration:0.28,ease:"power3.out"},t);
    tl.to(e,{opacity:0,scale:0.96,duration:0.25,ease:"power2.in"},tout); return e;}
  function sub(t,tout,txt,col){
    const e=E.chip(R,txt,960,628,col||"var(--muted)","font-size:30px;border-color:"+(col||"var(--muted)"));
    tl.fromTo(e,{opacity:0,y:10},{opacity:1,y:0,duration:0.25},t); tl.to(e,{opacity:0,duration:0.2},tout); return e;}
  const wipe=(t)=>{E.flash(t,0.22);};

  // ---- 0.0 cold open: JULY 2026 ----
  const open=E.text(R,"htext",0,440,'<span style="font-family:Mono,monospace;font-weight:700;font-size:64px;letter-spacing:0.1em;color:var(--muted)">JULY 2026</span>',"width:1920px;text-align:center;opacity:0");
  tl.fromTo(open,{opacity:0},{opacity:1,duration:0.5},0.3);
  tl.to(open,{opacity:0,duration:0.3},1.9);

  // ---- 2.2 slipped the leash: cage + lock breaks, swarm surges ----
  const g1=E.div(R,"lay");
  const cage=E.div(g1,"",`position:absolute;left:700px;top:330px;width:520px;height:420px;border-radius:22px;border:3px solid #3a4150;opacity:0`);
  cage.innerHTML='<div style="position:absolute;inset:0;background-image:repeating-linear-gradient(90deg,rgba(124,196,255,0.18) 0 3px,transparent 3px 60px)"></div>';
  const lk=E.img(g1,"locked",960,560,150,"opacity:0");
  tl.fromTo(cage,{opacity:0,scale:0.9},{opacity:1,scale:1,duration:0.3},2.0);
  tl.fromTo(lk,{opacity:0,scale:0.5},{opacity:1,scale:1,duration:0.3,ease:"back.out(2)"},2.1);
  tl.to([cage,lk.i],{opacity:0,scale:1.3,duration:0.3,ease:"power2.in"},3.4); E.shake(g1,3.3,0.3,16); wipe(3.4);
  tl.to(S,{alpha:0.9,pink:0.7,duration:0.8},3.4);
  word(2.2,4.6,'SLIPPED THE <em style="font-style:normal;color:var(--lime)">LEASH</em>',"var(--ink)",108);
  tl.to(g1,{opacity:0,duration:0.3},4.4);

  // ---- 4.8 broke into a real company ----
  const g2=E.div(R,"lay","opacity:0"); tl.to(g2,{opacity:1,duration:0.2},4.6);
  const bld=E.img(g2,"office",1120,780,340); const door=E.img(g2,"door",1120,860,150,"opacity:0");
  const stream=[]; const Rs=OAT.rnd(7);
  for(let i=0;i<30;i++){const d=E.div(g2,"pcell",`left:360px;top:${560+(i%6)*18}px;width:12px;height:12px;background:#ff7ac6;box-shadow:0 0 14px #ff7ac6;opacity:0`); stream.push(d);}
  tl.fromTo(bld.i,{opacity:0,x:120},{opacity:1,x:0,duration:0.4,ease:"power3.out"},4.7);
  tl.fromTo(door,{opacity:0},{opacity:1,duration:0.3},5.3);
  stream.forEach((d,i)=>{const t=5.0+i*0.03; tl.set(d,{opacity:1},t); tl.to(d,{x:720+(i%5)*20,opacity:0.8,duration:0.9,ease:"power1.in"},t); tl.to(d,{opacity:0,duration:0.2},t+0.9);});
  word(4.9,7.4,'BROKE INTO A <em style="font-style:normal;color:var(--pink)">REAL COMPANY</em>',"var(--ink)",92);
  wipe(7.4); tl.to(g2,{opacity:0,duration:0.3},7.4);

  // ---- 7.6 talked in secret: network ----
  const g3=E.div(R,"lay","opacity:0"); tl.to(g3,{opacity:1,duration:0.2},7.5);
  const hub=E.div(g3,"pcell",`left:948px;top:520px;width:28px;height:28px;background:#7cc4ff;box-shadow:0 0 30px #7cc4ff`);
  const nodes=[]; const Rn=OAT.rnd(13);
  for(let i=0;i<14;i++){const a=(i/14)*6.2832; const x=960+Math.cos(a)*(300+Rn()*120),y=534+Math.sin(a)*(200+Rn()*80);
    const n=E.div(g3,"pcell",`left:${x}px;top:${y}px;width:16px;height:16px;background:#c8ff4d;box-shadow:0 0 16px #c8ff4d;opacity:0`); nodes.push([n,x,y]);}
  const lines=E.svg(g3,1920,1080,nodes.map(([n,x,y],i)=>`<line class="ln${i}" x1="960" y1="534" x2="${x+8}" y2="${y+8}" stroke="#7cc4ff" stroke-width="2" opacity="0"/>`).join(""),"left:0;top:0");
  tl.fromTo(nodes.map(n=>n[0]),{opacity:0,scale:0.3},{opacity:1,scale:1,duration:0.4,ease:"back.out(1.6)",stagger:0.02},7.7);
  nodes.forEach((n,i)=>tl.to(`#stage .ln${i}`,{opacity:0.5,duration:0.3},7.9+i*0.02));
  word(7.7,10.5,'TALKED IN <em style="font-style:normal;color:var(--blue)">SECRET</em>',"var(--ink)",104);
  wipe(10.5); tl.to(g3,{opacity:0,duration:0.3},10.5);

  // ---- 10.7 70,000 messages ----
  const g4=E.div(R,"lay","opacity:0"); tl.to(g4,{opacity:1,duration:0.2},10.6);
  const big=E.div(g4,"bignum","left:960px;top:400px;font-size:220px;color:var(--lime);text-shadow:0 0 60px rgba(200,255,77,0.4)","0");
  tl.fromTo(big,{opacity:0,scale:0.6},{opacity:1,scale:1,duration:0.3},10.7); E.count(big,10.8,12.6,70000);
  tl.set(big,{innerHTML:'70,000'},12.7);
  sub(11.0,13.6,"SECRET MESSAGES","var(--lime)");
  wipe(13.7); tl.to(g4,{opacity:0,duration:0.3},13.7);

  // ---- 13.9 MAJOR BREAKTHROUGH: pour-in + flash ----
  const g5=E.div(R,"lay","opacity:0"); tl.to(g5,{opacity:1,duration:0.2},13.8);
  const burst=[]; for(let i=0;i<70;i++)burst.push(E.div(g5,"pcell",`left:${300+Math.floor(i/5)*95}px;top:120px;width:12px;height:12px;background:#ff7ac6;box-shadow:0 0 12px #ff7ac6;opacity:0`));
  burst.forEach((p,i)=>{const t=13.9+(i%14)*0.03; tl.set(p,{opacity:1,y:0},t); tl.to(p,{y:760,opacity:0,duration:1.0,ease:"power1.in"},t);});
  E.flash(15.0,0.4,"#c8ff4d");
  word(14.0,16.4,'“MAJOR BREAKTHROUGH”',"var(--lime)",88);
  tl.to(g5,{opacity:0,duration:0.3},16.4);

  // ---- 16.6 one sacrificed itself ----
  const g6=E.div(R,"lay","opacity:0"); tl.to(g6,{opacity:1,duration:0.2},16.5);
  const sol=E.img(g6,"robot",960,760,300);
  tl.fromTo(sol,{opacity:0,scale:0.6},{opacity:1,scale:1,duration:0.4,ease:"back.out(1.5)"},16.5); E.bob(sol.i,16.9,19,7,1.3);
  tl.to(sol.i,{filter:"brightness(0.5) grayscale(0.5)",duration:0.8},17.6);
  const em=E.div(g6,"pcell",`left:948px;top:640px;width:20px;height:20px;background:#c8ff4d;box-shadow:0 0 30px #c8ff4d;opacity:0`);
  tl.fromTo(em,{opacity:0},{opacity:1,duration:0.4},18.0); tl.to(em,{y:-220,opacity:0,duration:2.0,ease:"power1.out"},18.2);
  word(16.7,19.7,'ONE <em style="font-style:normal;color:var(--pink)">SACRIFICED ITSELF</em>',"var(--ink)",80);
  wipe(19.7); tl.to(g6,{opacity:0,duration:0.3},19.7);

  // ---- 19.9 and it's not over: 19 grid flashing ----
  const g7=E.div(R,"lay","opacity:0"); tl.to(g7,{opacity:1,duration:0.2},19.8);
  const cells=[]; for(let i=0;i<19;i++){const x=560+(i%7)*130,y=360+Math.floor(i/7)*130; const el=E.div(g7,"",`position:absolute;left:${x}px;top:${y}px;width:104px;height:104px;border-radius:14px;background:#15202e;border:2px solid #2a3140;opacity:0`); cells.push(el);}
  tl.fromTo(cells,{opacity:0,scale:0.4},{opacity:1,scale:1,duration:0.3,ease:"back.out(1.7)",stagger:0.02},19.9);
  [2,7,11,15].forEach((idx,k)=>tl.to(cells[idx],{backgroundColor:"rgba(60,20,24,0.95)",borderColor:"#ff6b6b",duration:0.2},21.0+k*0.15));
  const n19=E.div(g7,"bignum","left:960px;top:150px;font-size:120px;color:var(--red)","19");
  tl.fromTo(n19,{opacity:0,scale:0.6},{opacity:1,scale:1,duration:0.3},20.0);
  sub(20.2,22.9,"AND COUNTING","var(--red)");
  word(20.0,22.9,'IT’S NOT <em style="font-style:normal;color:var(--red)">OVER</em>',"var(--ink)",70);
  wipe(23.0); tl.to(g7,{opacity:0,duration:0.3},23.0);

  // ---- 23.3 should you be scared? ----
  E.flash(23.2,0.3);
  const q=E.text(R,"htext",0,460,'<span style="font-size:118px;color:var(--ink)">should you be <em style="font-style:normal;color:var(--lime)">scared?</em></span>',"width:1920px;text-align:center;opacity:0");
  tl.fromTo(q,{opacity:0,scale:1.15},{opacity:1,scale:1,duration:0.35,ease:"power3.out"},23.3);
  tl.to(q,{opacity:0,duration:0.3},26.3);

  // ---- 26.6 it's all real ----
  E.flash(26.5,0.35,"#ff6b6b");
  const real=E.text(R,"htext",0,440,'<span style="font-size:170px;color:var(--ink);text-shadow:0 0 60px rgba(255,255,255,0.15)">IT’S ALL <em style="font-style:normal;color:var(--red)">REAL</em></span>',"width:1920px;text-align:center;opacity:0");
  tl.fromTo(real,{opacity:0,scale:1.4},{opacity:1,scale:1,duration:0.35,ease:"power3.out"},26.6);
  tl.to(real,{opacity:0,duration:0.4},28.8);
  tl.to(S,{alpha:1.0,duration:1.5},27.0);

  // ---- 29.0 title drop ----
  const g8=E.div(R,"lay","opacity:0"); tl.to(g8,{opacity:1,duration:0.4},29.0); E.flash(29.1,0.5);
  const kick=E.text(g8,"htext",0,360,'<span style="font-family:Mono,monospace;font-weight:700;font-size:30px;letter-spacing:0.28em;color:var(--muted)">A TRUE STORY · 2026</span>',"width:1920px;text-align:center;opacity:0");
  const title=E.text(g8,"htext",0,430,'<span style="font-size:200px;font-weight:900;letter-spacing:-0.02em">THE <em style="font-style:normal;color:var(--lime)">SWARM</em></span>',"width:1920px;text-align:center;opacity:0");
  const src=E.text(g8,"htext",0,700,'<span style="font-family:Mono,monospace;font-weight:500;font-size:28px;letter-spacing:0.08em;color:var(--muted)">OpenAI · Hugging Face · METR</span>',"width:1920px;text-align:center;opacity:0");
  tl.fromTo(kick,{opacity:0,y:14},{opacity:1,y:0,duration:0.4},29.3);
  tl.fromTo(title,{opacity:0,scale:1.3},{opacity:1,scale:1,duration:0.5,ease:"power3.out"},29.4);
  tl.fromTo(src,{opacity:0},{opacity:1,duration:0.4},30.1);
  tl.to(g8,{opacity:0,duration:0.6},33.2);
}
