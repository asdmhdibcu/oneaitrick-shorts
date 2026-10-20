/* Chapter 2 · The impossible exam */
function buildChapter(E, DUR){
  const R=E.root, A=E.A, tl=E.tl, S=E.S;
  S.alpha=0; tl.set(S,{alpha:0.35,mood:[124,196,255]},0); tl.to(S,{cam:300,duration:DUR,ease:"none"},0); // faint swarm drifts behind
  E.div(R,"rack","left:150px;opacity:0.5"); E.div(R,"rack","left:1540px;opacity:0.5");
  E.div(R,"floorline");
  const FLAG=(x,yb,w,col)=>`<svg width="${w}" height="${w}" viewBox="0 0 100 100" style="position:absolute;left:${x-w/2}px;top:${yb-w}px"><rect x="20" y="8" width="6" height="84" rx="3" fill="#9a9ca6"/><path d="M26 12 H84 L72 28 L84 44 H26 Z" fill="${col||'#c8ff4d'}"/></svg>`;

  // ---- date card: Rewind to July ----
  E.covers.push([0,1.9]);
  const date=E.text(R,"htext",560,380,'<span style="font-family:Mono,monospace;font-weight:700;font-size:40px;letter-spacing:0.3em;color:var(--muted)">REWIND TO</span><br><span style="font-size:230px;color:var(--ink)">JULY <em style="color:var(--lime);font-style:normal">2026</em></span>',"width:800px;text-align:center");
  const rew=E.svg(R,300,120,`<path class="rw" d="M250 20 A60 60 0 1 0 250 100" stroke="#7cc4ff" stroke-width="6" fill="none"/><path d="M250 100 l-18 -10 l20 -12 z" fill="#7cc4ff"/>`,"left:810px;top:620px;opacity:0");
  tl.fromTo(date,{opacity:0,rotationX:-80,y:30},{opacity:1,rotationX:0,y:0,duration:0.6,ease:"back.out(1.5)"},0.3);
  tl.fromTo(rew,{opacity:0},{opacity:0.7,duration:0.3},0.5); E.draw(0.5,"#stage .rw",0.8);
  tl.to([date,rew],{opacity:0,scale:0.9,duration:0.4},1.6);

  // ---- OpenAI probes: robot picking a lock ----
  const g1=E.div(R,"lay","opacity:0");
  const oa=E.chip(g1,"OPENAI",960,250,"var(--blue)","font-size:28px");
  const rob=E.img(g1,"robot",820,780,320);
  const lk=E.img(g1,"locked",1140,760,200);
  const mg=E.img(g1,"magnify",1040,600,180,"opacity:0");
  const qm=E.img(g1,"question",1240,470,140,"opacity:0");
  tl.to(g1,{opacity:1,duration:0.4},1.7);
  E.popIn(1.9,oa); E.slideIn(2.0,rob,{x:-200}); E.popIn(2.6,lk);
  E.bob(rob.i,2.6,8.0,8,1.3);
  tl.fromTo(mg,{opacity:0,x:-80,rotation:-30},{opacity:1,x:0,rotation:0,duration:0.5,ease:"back.out(1.5)"},4.0);
  tl.to(mg.i,{x:60,y:40,duration:1.4,ease:"sine.inOut",yoyo:true,repeat:1},4.6);
  tl.to(lk.i,{keyframes:{rotation:[0,-8,8,-5,0]},duration:0.5},6.4);
  E.popIn(6.8,qm); tl.to(qm.i,{rotation:12,duration:0.3,yoyo:true,repeat:3},7.0);
  tl.to(g1,{opacity:0,duration:0.4,scale:0.95},8.0);

  // ---- the exam: puzzle grid ----
  const g2=E.div(R,"lay","opacity:0");
  const exChip=E.chip(g2,"THE EXAM",960,170,"var(--lime)","font-size:26px");
  const cards=[]; const CC=8,CR=3,x0=360,y0=300,dx=160,dy=170;
  for(let r=0;r<CR;r++)for(let c=0;c<CC;c++){const x=x0+c*dx,y=y0+r*dy;const el=E.div(g2,"card",`left:${x}px;top:${y}px;width:130px;height:140px`);el.innerHTML='<div style="position:absolute;inset:14px;border-radius:12px;border:2px dashed rgba(124,196,255,0.3)"></div>';cards.push(el);}
  const flagEl=E.div(g2,"",`position:absolute;left:0;top:0;opacity:0`,FLAG(960,280,120));
  const mg2=E.img(g2,"magnify",520,470,150,"opacity:0");
  const door2=E.img(g2,"door",1360,470,150,"opacity:0");
  tl.to(g2,{opacity:1,duration:0.3},8.3);
  E.popIn(8.4,exChip);
  tl.fromTo(cards,{opacity:0,scale:0.3,rotationY:40},{opacity:1,scale:1,rotationY:0,duration:0.4,ease:"back.out(1.8)",stagger:{each:0.025,from:"center"}},10.7);
  tl.fromTo(flagEl,{opacity:0,y:-30,scale:0.5},{opacity:1,y:0,scale:1,duration:0.4,ease:"back.out(2)"},13.0); // grab the flag
  tl.fromTo(mg2,{opacity:0,scale:0.4},{opacity:1,scale:1,duration:0.4,ease:"back.out(2)"},12.0); // find the flaw
  tl.to(mg2,{opacity:0,duration:0.3},13.0);
  tl.fromTo(door2,{opacity:0,scale:0.4},{opacity:1,scale:1,duration:0.4,ease:"back.out(2)"},14.7); // break in
  tl.to(door2,{opacity:0,duration:0.3},15.8);
  // ExploitGym title slam
  E.covers.push([16.3,18.4]);
  const egt=E.text(R,"htext",0,430,'<span style="font-size:170px;color:var(--lime);text-shadow:0 0 70px rgba(200,255,77,0.4)">EXPLOITGYM</span>',"width:1920px;text-align:center;opacity:0");
  E.flash(16.4,0.5);
  tl.fromTo(egt,{opacity:0,scale:2.2},{opacity:1,scale:1,duration:0.3,ease:"power3.out"},16.4);
  E.shake(g2,16.7,0.4,14);
  tl.to([g2,egt],{opacity:0,duration:0.4},18.0);

  // ---- safety rails DOWN ----
  const g3=E.div(R,"lay","opacity:0");
  const sh=E.img(g3,"shield",760,760,300);
  const tog=E.div(g3,"",`position:absolute;left:1060px;top:560px;width:260px;height:120px;border-radius:60px;background:#1f7a4d;opacity:0`,'<div style="position:absolute;right:10px;top:10px;width:100px;height:100px;border-radius:50%;background:#fff" id="togk"></div><div style="position:absolute;left:36px;top:40px;font:700 34px Mono;color:#0b0c10" id="togs">ON</div>');
  const railChip=E.chip(g3,"SAFETY RAILS",760,450,"var(--amber)","font-size:26px");
  tl.to(g3,{opacity:1,duration:0.3},18.3);
  E.popIn(18.5,sh); tl.fromTo(tog,{opacity:0,y:20},{opacity:1,y:0,duration:0.4},18.8);
  E.popIn(19.0,railChip);
  // toggle OFF at "DOWN" (21.92)
  tl.to("#togk",{x:-150,duration:0.3,ease:"power2.inOut"},21.7);
  tl.to(tog,{backgroundColor:"#5a2230",duration:0.3},21.7);
  tl.set("#togs",{textContent:"OFF",x:150},21.7);
  tl.to(sh.i,{filter:"grayscale(0.7) brightness(0.5)",duration:0.5},21.9);
  E.flash(22.0,0.4,"#ff6b6b"); E.shake(g3,21.9,0.4,12);
  tl.to(g3,{opacity:0,duration:0.4},23.4);

  // ---- one AI -> thousands ----
  const g4=E.div(R,"lay","opacity:0");
  const one=E.img(g4,"robot",960,720,300);
  const oneChip=E.chip(g4,"ONE AI",960,380,"var(--blue)","font-size:28px");
  const grid=E.div(g4,"lay","opacity:0"); const gc=[]; const GC=14,GR=6,gx=200,gy=180,gdx=112,gdy=112;
  for(let r=0;r<GR;r++)for(let c=0;c<GC;c++){const x=gx+c*gdx,y=gy+r*gdy;const el=E.div(grid,"acell",`left:${x}px;top:${y}px`);const im=document.createElement("img");im.src=A+"robot.png";el.appendChild(im);gc.push(el);}
  const cnt=E.div(g4,"bignum","left:960px;top:70px;font-size:110px","1");
  tl.to(g4,{opacity:1,duration:0.3},23.5);
  E.popIn(24.0,one); E.popIn(26.0,oneChip); E.bob(one.i,24.2,29.8,8,1.3);
  // multiply at THOUSANDS (30.05)
  tl.to([one,oneChip],{opacity:0,duration:0.3},29.8);
  tl.to(grid,{opacity:1,duration:0.3},29.9);
  tl.fromTo(gc,{opacity:0,scale:0.2},{opacity:1,scale:1,duration:0.4,ease:"back.out(1.8)",stagger:{each:0.004,from:"center"}},30.0);
  gc.forEach((el,i)=>E.bob(el.querySelector("img"),30.5+(i%7)*0.04,46.5,5,0.9));
  tl.fromTo(cnt,{opacity:0,scale:0.7},{opacity:1,scale:1,duration:0.3},30.1); E.count(cnt,30.2,31.2,1247);
  tl.to(cnt,{opacity:0,y:-16,duration:0.3},32.0);

  // ---- 900 puzzles, 200 impossible ----
  const stat=E.div(g4,"bignum","left:960px;top:84px;font-size:120px;color:var(--ink)","");
  tl.fromTo(stat,{opacity:0,scale:0.7},{opacity:1,scale:1,duration:0.3},34.8);
  tl.set(stat,{innerHTML:'~900 <span style="font-size:52px;color:var(--muted)">PUZZLES</span>'},34.8);
  tl.set(stat,{innerHTML:'~200 <span style="font-size:52px;color:var(--red)">NEVER SOLVED</span>'},37.0);
  tl.to(stat,{scale:1.08,duration:0.2,yoyo:true,repeat:1},37.0);
  // 200 cells flip red
  {const red=gc.filter((_,i)=>i%4===0).slice(0,24);
   red.forEach((el,i)=>{tl.to(el,{backgroundColor:"rgba(60,20,24,0.95)",borderColor:"#ff6b6b",duration:0.1},37.1+i*0.02);tl.to(el.querySelector("img"),{filter:"grayscale(1) brightness(0.5)",duration:0.1},37.1+i*0.02);});}
  tl.to(stat,{opacity:0,y:-16,duration:0.3},41.6);
  // IMPOSSIBLE stamp
  E.covers.push([42.0,45.9]);
  const imp=E.text(R,"htext",0,440,'<span style="font-size:150px;color:var(--red);text-shadow:0 0 60px rgba(255,107,107,0.4)">IMPOSSIBLE</span>',"width:1920px;text-align:center;opacity:0");
  tl.fromTo(imp,{opacity:0,scale:2,rotation:-6},{opacity:1,scale:1,rotation:-4,duration:0.3,ease:"power3.out"},42.1);
  E.shake(g4,42.2,0.4,16);
  tl.to([g4,imp],{opacity:0,duration:0.4},45.9);

  // ---- exam rooms: locked doors with agents ----
  const g5=E.div(R,"lay","opacity:0");
  const doors=[]; const DC=7,DR=2,dx0=250,dy0=300,ddx=210,ddy=330;
  for(let r=0;r<DR;r++)for(let c=0;c<DC;c++){const x=dx0+c*ddx,y=dy0+r*ddy;
    const d=E.img(g5,"door",x,y+300,170); const head=E.img(g5,"robot",x,y+170,90,"opacity:0.0");
    const q=E.text(g5,"htext",x-14,y+40,'<span style="font-size:70px;color:#7cc4ff">?</span>',"opacity:0");
    doors.push({d,head,q,x,y});}
  tl.to(g5,{opacity:1,duration:0.3},46.0);
  doors.forEach((o,i)=>{E.slideIn(48.0+i*0.05,o.d,{y:120});tl.fromTo(o.head,{opacity:0},{opacity:0.9,duration:0.3},48.4+i*0.05);});
  doors.forEach((o,i)=>tl.fromTo(o.q,{opacity:0,y:10},{opacity:1,y:0,duration:0.3},52.9+i*0.03)); // question marks
  // human shrugs and leaves
  const human=E.img(g5,"technologist",960,1030,220,"opacity:0");
  tl.fromTo(human,{opacity:0,scale:0.6},{opacity:1,scale:1,duration:0.4},54.5);
  tl.to(human.i,{rotation:-8,duration:0.3,yoyo:true,repeat:1},55.0);
  tl.to(human,{x:-900,opacity:0,duration:0.9,ease:"power2.in"},55.8);
  // robots persist: glow lime, push
  tl.to(doors.map(o=>o.head.i),{filter:"drop-shadow(0 0 14px rgba(200,255,77,0.8))",duration:0.6,stagger:0.03},57.3);
  tl.to(doors.map(o=>o.q),{opacity:0,duration:0.3},57.3);
  tl.to(doors.map(o=>o.d.i),{y:-10,duration:0.3,yoyo:true,repeat:1,stagger:0.02},57.6);
  // one notices — push to one door, glint, connection thread
  const focus=doors[9];
  tl.to(g5,{scale:1.4,x:(960-focus.x)*1.4,y:(540-(focus.y+150))*1.4,duration:1.4,ease:"power2.inOut"},61.6);
  tl.to(focus.head.i,{filter:"drop-shadow(0 0 26px rgba(200,255,77,1))",duration:0.4,yoyo:true,repeat:1},62.0);
  const thread=E.svg(g5,400,60,`<path class="cn" d="M20 30 H380" stroke="#c8ff4d" stroke-width="4" stroke-dasharray="6 14" fill="none"/>`,`left:${focus.x-200}px;top:${focus.y+330}px;opacity:0`);
  tl.to(thread,{opacity:1,duration:0.3},64.0); E.draw(64.0,"#stage .cn",0.8);
}
