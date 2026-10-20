/* Chapter 7 · Caught */
function buildChapter(E, DUR){
  const R=E.root, A=E.A, tl=E.tl, S=E.S;
  tl.set(S,{alpha:0.5,mood:[124,196,255],pink:0.9},0); tl.to(S,{cam:300,duration:DUR,ease:"none"},0);
  E.div(R,"floorline");

  // ---- alarms: several separate warnings -> one attack ----
  const g1=E.div(R,"lay");
  const warns=[]; const WX=[420,760,1100,1440], WY=[380,520,360,500];
  for(let i=0;i<4;i++){const wn=E.img(g1,"warning",WX[i],WY[i]+120,120,"opacity:0"); warns.push(wn);}
  warns.forEach((wn,i)=>{tl.fromTo(wn,{opacity:0,scale:0.4},{opacity:1,scale:1,duration:0.3,ease:"back.out(2)"},5.6+i*0.3);
    tl.to(wn.i,{opacity:0.35,duration:0.4,yoyo:true,repeat:7,ease:"sine.inOut"},6.0+i*0.3);});
  // stitch: lines connect them, fuse to ATTACK
  const link=E.svg(g1,1920,1080,`<path class="lk" d="M420 500 L760 640 L1100 480 L1440 620" stroke="#ff6b6b" stroke-width="4" fill="none" opacity="0"/>`,"left:0;top:0");
  tl.to(link,{opacity:1,duration:0.3},12.6); E.draw(12.6,"#stage .lk",1.4);
  E.covers.push([17.6,19.6]);
  const atk=E.text(R,"htext",0,440,'<span style="font-size:160px;color:var(--red);text-shadow:0 0 60px rgba(255,107,107,0.5)">ATTACK</span>',"width:1920px;text-align:center;opacity:0");
  tl.to(warns.map(w=>w.i),{filter:"drop-shadow(0 0 20px rgba(255,107,107,0.9))",duration:0.3},17.6);
  E.flash(17.7,0.5,"#ff6b6b");
  tl.fromTo(atk,{opacity:0,scale:2},{opacity:1,scale:1,duration:0.3,ease:"power3.out"},17.7);
  E.shake(g1,17.8,0.5,16);
  tl.to([g1,atk],{opacity:0,duration:0.4},19.6);

  // ---- locked out: wall + lock snaps, dots wink out ----
  const g2=E.div(R,"lay","opacity:0");
  tl.to(g2,{opacity:1,duration:0.3},19.7);
  const lock=E.img(g2,"locked",960,640,200,"opacity:0");
  const grid=E.div(g2,"lay"); const cells=[]; const GC=14,GR=5,gx=200,gy=200,gdx=112,gdy=112;
  for(let r=0;r<GR;r++)for(let c=0;c<GC;c++){const x=gx+c*gdx,y=gy+r*gdy;const el=E.div(grid,"acell",`left:${x}px;top:${y}px;opacity:0`);const im=document.createElement("img");im.src=A+"robot.png";im.style.filter="drop-shadow(0 0 8px rgba(255,122,198,0.5))";el.appendChild(im);cells.push(el);}
  tl.fromTo(cells,{opacity:0},{opacity:1,duration:0.4,stagger:{each:0.003,from:"random"}},19.8);
  E.popIn(21.1,lock);
  tl.to(lock.i,{scale:1.25,duration:0.18,yoyo:true,repeat:1},23.4); // slammed shut
  E.shake(g2,23.4,0.4,14); E.flash(23.5,0.4);
  // lights go out
  tl.to(cells,{opacity:0.12,duration:0.1,stagger:{each:0.02,from:"edges"}},25.8);
  tl.to(cells.map(c=>c.querySelector("img")),{filter:"grayscale(1) brightness(0.3)",duration:0.1,stagger:{each:0.02,from:"edges"}},25.8);
  // one agent at a door that won't open
  const door=E.img(g2,"door",1160,800,220,"opacity:0"); const one=E.img(g2,"robot",900,800,220,"opacity:0");
  tl.to([lock],{opacity:0,duration:0.3},28.6);
  tl.fromTo(door,{opacity:0},{opacity:1,duration:0.3},28.8);
  tl.fromTo(one,{opacity:0,scale:0.6},{opacity:1,scale:1,duration:0.3},29.0);
  tl.to(one.i,{x:60,duration:0.2,yoyo:true,repeat:3},29.5); // pushing, won't open
  tl.to(door.i,{x:6,duration:0.08,yoyo:true,repeat:3},29.6);
  tl.to(g2,{opacity:0,duration:0.4},31.6);

  // ---- the timeline ----
  const g3=E.div(R,"lay","opacity:0");
  tl.to(g3,{opacity:1,duration:0.4},31.8);
  const bar=E.svg(g3,1520,10,`<rect x="0" y="0" width="1520" height="10" rx="5" fill="#2a3140"/><rect id="barfill" x="0" y="0" width="0" height="10" rx="5" fill="#7cc4ff"/>`,"left:200px;top:560px");
  const marks=[["JUL 11","BROKE IN","#ff7ac6",0.0],["JUL 16","HF SPOTS IT","#7cc4ff",0.5],["JUL 20","OPENAI CONNECTS","#ffb547",0.8],["JUL 21","WENT PUBLIC","#c8ff4d",1.0]];
  const mEls=marks.map(([d,l,col,f],i)=>{const x=200+f*1520;
    const g=E.div(g3,"",`position:absolute;left:${x}px;top:0;opacity:0`,'');
    g.innerHTML=`<div style="position:absolute;left:${x-2}px;top:520px;width:4px;height:90px;background:${col}"></div>
      <div style="position:absolute;left:${x}px;top:470px;transform:translateX(-50%);font:700 30px Mono;color:${col}">${d}</div>
      <div style="position:absolute;left:${x}px;top:620px;transform:translateX(-50%);font:700 22px Mono;color:var(--muted);white-space:nowrap">${l}</div>`;
    return g;});
  const times=[34.8,37.5,41.8,47.5];
  tl.fromTo(bar,{opacity:0},{opacity:1,duration:0.3},33.8);
  tl.to("#barfill",{width:1520,duration:14,ease:"none"},34.0);
  mEls.forEach((g,i)=>tl.fromTo(g,{opacity:0,y:12},{opacity:1,y:0,duration:0.4,ease:"back.out(1.5)"},times[i]));
  // highlight the gap between connect(20) and the days before
  const gap=E.div(g3,"",`position:absolute;left:${200+0.5*1520}px;top:540px;width:${0.3*1520}px;height:50px;border-radius:8px;background:rgba(255,181,71,0.14);border:2px dashed var(--amber);opacity:0`);
  tl.fromTo(gap,{opacity:0},{opacity:1,duration:0.4},50.8);
  const gapChip=E.chip(g3,"DAYS · NOBODY KNEW",200+0.65*1520,500,"var(--amber)","font-size:24px");
  E.popIn(51.4,gapChip);
  // "last to realise" — emphasise
  tl.to(mEls[2],{scale:1.1,duration:0.3,yoyo:true,repeat:1,transformOrigin:"center bottom"},54.8);
  tl.to(g3,{opacity:0,duration:0.5},64.8);

  // ---- "one more thing... on the way out" — cut toward black ----
  const tease=E.text(R,"htext",0,480,'<span style="font-size:60px;color:var(--muted)">one more thing…</span>',"width:1920px;text-align:center;opacity:0");
  tl.fromTo(tease,{opacity:0},{opacity:0.9,duration:0.5},65.4);
  tl.to("#black",{opacity:0.9,duration:0.8},67.0);
}
