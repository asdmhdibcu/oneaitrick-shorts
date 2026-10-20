/* Chapter 9 · Two futures (the debate) */
function buildChapter(E, DUR){
  const R=E.root, A=E.A, tl=E.tl, S=E.S;
  tl.set(S,{alpha:0.4,mood:[124,196,255],pink:0.3},0); tl.to(S,{cam:280,duration:DUR,ease:"none"},0);

  // ---- the split ----
  const g1=E.div(R,"lay");
  const left=E.div(g1,"",`position:absolute;left:0;top:0;width:960px;height:1080px;background:linear-gradient(180deg,rgba(124,196,255,0.12),rgba(124,196,255,0.02));opacity:0`);
  const right=E.div(g1,"",`position:absolute;left:960px;top:0;width:960px;height:1080px;background:linear-gradient(180deg,rgba(255,181,71,0.12),rgba(255,181,71,0.02));opacity:0`);
  const seam=E.div(g1,"",`position:absolute;left:958px;top:0;width:4px;height:1080px;background:#f5f5f2;opacity:0`);
  tl.fromTo([left,right],{opacity:0},{opacity:1,duration:0.5,stagger:0.1},4.3);
  tl.fromTo(seam,{opacity:0,scaleY:0},{opacity:0.7,scaleY:1,duration:0.5,ease:"power3.out"},4.5);
  const slow=E.chip(g1,"SLOW DOWN",480,220,"var(--blue)","font-size:36px");
  const speed=E.chip(g1,"SPEED UP",1440,220,"var(--amber)","font-size:36px");
  const rob1=E.img(g1,"scientist",480,900,220,"opacity:0"); const rob2=E.img(g1,"technologist",1440,900,220,"opacity:0");
  E.popIn(6.5,slow); E.slideIn(8.6,rob1,{y:120});
  // left quotes
  const ql=[];
  function sideQuote(parent,x,y,txt,col,t0,t1){const c=E.text(g1,"htext",x-380,y,`<span style="font-family:Mono,monospace;font-weight:700;font-size:40px;line-height:1.2;color:${col}">${txt}</span>`,`width:760px;text-align:center;opacity:0`);
    tl.fromTo(c,{opacity:0,y:14},{opacity:1,y:0,duration:0.4},t0); if(t1)tl.to(c,{opacity:0,duration:0.3},t1); return c;}
  sideQuote(g1,480,360,'“these are our\nwarning shots”',"#7cc4ff",11.2,16.0);
  sideQuote(g1,480,360,'“we don’t know how\nto build these safely… yet”',"#7cc4ff",19.0,29.6);
  E.popIn(30.3,speed); E.slideIn(32.3,rob2,{y:120});
  sideQuote(g1,1440,360,'“completely in\nour control”',"#ffb547",36.4,44.2);
  sideQuote(g1,1440,360,'if we pause,\nChina won’t',"#ffb547",47.6,53.4);
  // "both" — seam dissolves, colours bleed
  tl.to(g1,{opacity:0,duration:0.5},53.6);

  const g2=E.div(R,"lay","opacity:0");
  tl.to(g2,{opacity:1,duration:0.4},54.0);
  E.covers.push([58.0,59.6]);
  const both=E.text(R,"htext",0,440,'<span style="font-size:150px;color:var(--lime);text-shadow:0 0 60px rgba(200,255,77,0.4)">BOTH</span>',"width:1920px;text-align:center;opacity:0");
  tl.fromTo(both,{opacity:0,scale:1.8},{opacity:1,scale:1,duration:0.4,ease:"power3.out"},58.1);
  tl.to(both,{opacity:0,duration:0.4},59.6);
  // "capable, determined, faster" — three words stamp over growing swarm
  tl.to(S,{alpha:0.7,duration:2},66.0);
  const words=[["CAPABLE",70.5],["DETERMINED",71.5],["FASTER",72.8]];
  const wEls=words.map(([w,t],i)=>{const e=E.text(g2,"htext",0,300+i*170,`<span style="font-size:110px;color:var(--ink)">${w}</span>`,"width:1920px;text-align:center;opacity:0");
    tl.fromTo(e,{opacity:0,x:-80},{opacity:1,x:0,duration:0.4,ease:"power3.out"},t); return e;});
  tl.to(wEls[2].querySelector("span"),{color:"#ff7ac6",duration:0.3},73.2);
  tl.to(g2,{opacity:0,duration:0.5},74.6);
  // "the next models — far more capable" — one brighter new dot
  const g3=E.div(R,"lay","opacity:0");
  tl.to(g3,{opacity:1,duration:0.4},74.8);
  const nd=E.div(g3,"pcell",`left:960px;top:540px;width:30px;height:30px;background:#c8ff4d;box-shadow:0 0 40px #c8ff4d`);
  tl.fromTo(nd,{scale:0,opacity:0},{scale:1,opacity:1,duration:0.5,ease:"back.out(2)"},75.2);
  tl.to(nd,{scale:2.4,duration:3,ease:"power1.in"},75.8);
  tl.to(nd,{boxShadow:"0 0 80px #c8ff4d",duration:1,yoyo:true,repeat:2},76.0);
}
