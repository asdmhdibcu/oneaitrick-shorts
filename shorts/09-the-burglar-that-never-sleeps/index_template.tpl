<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/js/gsap.min.js"></script>
    <script src="captions.js"></script>
    <link rel="stylesheet" href="assets/base.css" />
    <style>
      .shot { position: absolute; inset: 0; overflow: hidden; }
      .fx, .cam { position: absolute; inset: 0; transform-origin: 50% 45%; }
      .vid { position: absolute; object-fit: cover; }
      .frz { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; opacity: 0; }
      .bd { position: absolute; left: -60px; top: -60px; width: 1200px; height: 2040px; background-size: cover; background-position: center;
        filter: brightness(0.38) saturate(0.85); }
      .desk { position: absolute; inset: 0; background:
        radial-gradient(ellipse 70% 45% at 50% 38%, rgba(255,255,255,0.06), rgba(0,0,0,0) 70%),
        linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
        background-size: auto, 72px 72px, 72px 72px; }
      .card { position: absolute; overflow: hidden; border-radius: 24px; background: #fff;
        box-shadow: 0 40px 90px rgba(0,0,0,0.6), 0 0 0 1px rgba(255,255,255,0.08); }
      .card img { position: absolute; }
      .scroller { position: absolute; left: 0; top: 0; width: 100%; }
      .hl { position: absolute; mix-blend-mode: multiply; border-radius: 6px; transform-origin: 0 50%; transform: scaleX(0); }
      .redact { position: absolute; background: #0b0c10; border-radius: 3px; transform-origin: 0 50%; transform: scaleX(0); }
      .gfx { position: absolute; inset: 0; }
      .vig { position: absolute; inset: 0; background: radial-gradient(ellipse 85% 70% at 50% 42%, rgba(4,5,10,0) 55%, rgba(4,5,10,0.55) 100%); }
      .botshade { position: absolute; left: 0; top: 1020px; width: 1080px; height: 900px; background: linear-gradient(180deg, rgba(4,5,10,0) 0%, rgba(4,5,10,0.68) 36%, rgba(4,5,10,0.86) 100%); }
      .doctop { position: absolute; left: 0; top: 0; width: 1080px; height: 320px; pointer-events: none;
        background: linear-gradient(180deg, rgba(4,5,10,0.9) 0, rgba(4,5,10,0.84) 215px, rgba(4,5,10,0) 320px); }
      .docfade { position: absolute; left: 0; top: 1085px; width: 1080px; height: 835px; pointer-events: none;
        background: linear-gradient(180deg, rgba(4,5,10,0) 0, rgba(4,5,10,0.9) 130px, rgba(4,5,10,0.96) 175px, rgba(4,5,10,0.96) 100%); }
      .topshade { position: absolute; left: 0; top: 0; width: 1080px; height: 330px; background: linear-gradient(180deg, rgba(4,5,10,0.62) 0%, rgba(4,5,10,0) 100%); }
      .grain { position: absolute; inset: 0; background-image: url("assets/grain.png"); opacity: 0.075; mix-blend-mode: overlay; }
      .flash { position: absolute; inset: 0; background: #fff; opacity: 0; }
      .black { position: absolute; inset: 0; background: #000; opacity: 0; }
      .tag2 { position: absolute; left: 60px; top: 150px; display: inline-flex; align-items: center; gap: 12px; padding: 12px 22px 12px 18px;
        border: 2px solid rgba(255,255,255,0.16); border-radius: 999px; background: rgba(8,9,14,0.62); font-family: "Mono", monospace; font-weight: 700;
        font-size: 26px; letter-spacing: 0.08em; color: var(--ink); }
      .tag2 .dot { width: 14px; height: 14px; border-radius: 50%; background: var(--lime); box-shadow: 0 0 14px var(--lime); }
      .src { position: absolute; left: 60px; top: 232px; display: inline-flex; align-items: center; gap: 10px; font-family: "Mono", monospace; font-weight: 700;
        font-size: 21px; letter-spacing: 0.1em; padding: 9px 15px; border-radius: 10px; background: rgba(6,8,12,0.72); color: #d4d6de;
        border: 1.5px solid rgba(255,255,255,0.16); opacity: 0; white-space: nowrap; }
      .src .sd { width: 10px; height: 10px; border-radius: 50%; background: #ff5b5b; box-shadow: 0 0 10px #ff5b5b; }
      .src.gen .sd { background: #b9a2ff; box-shadow: 0 0 10px #b9a2ff; }

      /* designed captions */
      .cap { position: absolute; opacity: 0; font-weight: 900; text-transform: uppercase; letter-spacing: -0.02em; line-height: 1.0; color: #fff;
        text-shadow: 0 6px 26px rgba(0,0,0,0.6), 0 2px 4px rgba(0,0,0,0.55); }
      .cap.S, .cap.B { left: 40px; width: 1000px; bottom: 470px; text-align: center; font-size: 80px; }
      .cap.A { left: 66px; width: 960px; bottom: 470px; text-align: left; font-size: 72px; }
      .cw { display: inline-block; margin: 0 0.16em; transform-origin: 50% 70%; }
      .cap.A .cw { margin: 0 0.32em 0 0; }
      .cw.dim { opacity: 0.45; }
      .cw.hero { display: block; margin: 0.16em 0 0.22em; line-height: 0.92; letter-spacing: -0.04em; transform-origin: 0 60%; position: relative; }
      .cw.hero .bar { position: absolute; left: 0.02em; bottom: -0.1em; height: 0.07em; border-radius: 0.04em; transform-origin: 0 50%; }
      .cw.num { display: block; font-size: 2.1em; letter-spacing: -0.05em; line-height: 0.95; margin: 0.02em 0; }
      .cw.num.clock { font-family: "Mono", monospace; font-weight: 700; font-size: 1.7em; letter-spacing: 0.02em; }
      .cw.inl { font-size: 1.12em; }

      /* shot graphics */
      .stamp { position: absolute; font-weight: 900; font-size: 92px; letter-spacing: -0.01em; padding: 10px 30px; border: 9px solid currentColor; border-radius: 18px;
        color: #ff5b5b; background: rgba(12,6,8,0.55); opacity: 0; white-space: nowrap; }
      .chip { position: absolute; font-family: "Mono", monospace; font-weight: 700; font-size: 30px; letter-spacing: 0.08em; padding: 14px 22px;
        border-radius: 14px; background: rgba(6,8,12,0.84); border: 2px solid currentColor; opacity: 0; white-space: nowrap; color: var(--amber); }
      .chip .sw { display: inline-block; width: 14px; height: 14px; border-radius: 50%; background: currentColor; margin-right: 14px; vertical-align: 2px; box-shadow: 0 0 12px currentColor; }
      .chip s { text-decoration-thickness: 5px; text-decoration-color: #ff5b5b; }
      .readout { position: absolute; left: 0; width: 1080px; text-align: center; opacity: 0; }
      .readout .rl { font-family: "Mono", monospace; font-weight: 700; font-size: 26px; letter-spacing: 0.2em; color: #e2e4ea; text-shadow: 0 2px 12px rgba(0,0,0,0.9); }
      .readout .rv { font-weight: 900; font-size: 130px; letter-spacing: -0.04em; line-height: 1; color: #fff; }
      .readout .rs { font-family: "Mono", monospace; font-weight: 700; font-size: 26px; letter-spacing: 0.12em; color: #c9ccd6; margin-top: 10px; }
      .ring { position: absolute; border-radius: 50%; border: 6px solid var(--amber); box-shadow: 0 0 26px rgba(255,181,71,0.8), inset 0 0 20px rgba(255,181,71,0.4); opacity: 0; }
      .pin { position: absolute; left: 0; top: 0; opacity: 0; }
      .pin .pl { position: absolute; left: 26px; top: -30px; font-family: "Mono", monospace; font-weight: 700; font-size: 28px; letter-spacing: 0.06em; white-space: nowrap;
        padding: 10px 16px; border-radius: 12px; background: rgba(6,8,12,0.82); border: 2px solid currentColor; }
      .pin .pd { position: absolute; left: -11px; top: -11px; width: 22px; height: 22px; border-radius: 50%; background: currentColor; box-shadow: 0 0 18px currentColor; }
      .pin.left .pl { left: auto; right: 26px; }
      .gtag { position: absolute; font-family: "Mono", monospace; font-weight: 700; font-size: 34px; letter-spacing: 0.04em; color: #ffe2b0; padding: 8px 16px;
        border-radius: 10px; background: rgba(10,8,4,0.66); border: 2px solid rgba(255,181,71,0.75); box-shadow: 0 0 24px rgba(255,181,71,0.45); opacity: 0; white-space: nowrap; }
      .vf { position: absolute; left: 70px; top: 300px; width: 940px; height: 900px; opacity: 0; }
      .vf i { position: absolute; width: 90px; height: 90px; border: 0 solid #fff; }
      .vf .rec { position: absolute; right: 18px; top: 16px; font-family: "Mono", monospace; font-weight: 700; font-size: 28px; color: #fff; letter-spacing: 0.1em; }
      .vf .rec b { display: inline-block; width: 18px; height: 18px; border-radius: 50%; background: #ff3b30; margin-right: 10px; box-shadow: 0 0 12px #ff3b30; }
      .pop { position: absolute; width: 120px; height: 120px; margin: -60px 0 0 -60px; border-radius: 50%; opacity: 0;
        background: radial-gradient(circle, rgba(255,255,255,1) 0, rgba(255,240,220,0.7) 18%, rgba(255,255,255,0) 60%); }
      .photo { position: absolute; width: 112px; height: 84px; border: 5px solid #f3efe6; border-bottom-width: 12px; border-radius: 3px; background-size: 540px 960px;
        box-shadow: 0 8px 18px rgba(0,0,0,0.5); opacity: 0; }
      .cal { position: absolute; left: 620px; top: 330px; width: 400px; border-radius: 22px; overflow: hidden; background: #f3efe6; box-shadow: 0 30px 60px rgba(0,0,0,0.55); opacity: 0; }
      .cal .ch { background: #c9352b; color: #fff; font-family: "Mono", monospace; font-weight: 700; font-size: 26px; letter-spacing: 0.14em; padding: 16px 0; text-align: center; }
      .cal .cn { font-weight: 900; font-size: 190px; letter-spacing: -0.05em; line-height: 1; color: #15161b; text-align: center; padding: 18px 0 0; }
      .cal .cu { font-family: "Mono", monospace; font-weight: 700; font-size: 28px; letter-spacing: 0.14em; color: #5a5d66; text-align: center; padding: 6px 0 24px; }
      .cal .cb { height: 14px; background: #ddd6c8; } .cal .cb i { display: block; height: 100%; width: 100%; background: #c9352b; transform-origin: 0 50%; transform: scaleX(0); }
      .badge { position: absolute; left: 60px; top: 870px; width: 600px; padding: 26px 30px; border-radius: 22px; background: rgba(12,10,22,0.86); border: 2px solid rgba(185,156,255,0.7);
        box-shadow: 0 0 40px rgba(185,156,255,0.35), 0 30px 60px rgba(0,0,0,0.5); opacity: 0; }
      .badge .bk { font-family: "Mono", monospace; font-weight: 700; font-size: 24px; letter-spacing: 0.18em; color: #b9a2ff; }
      .badge .bn { font-weight: 900; font-size: 66px; letter-spacing: -0.03em; color: #fff; margin-top: 8px; }
      .badge .bs { font-family: "Mono", monospace; font-weight: 700; font-size: 24px; letter-spacing: 0.1em; color: #c9ccd6; margin-top: 8px; }
      .race { position: absolute; inset: 0; opacity: 0; }
      .race .rh { position: absolute; top: 330px; width: 420px; text-align: center; font-family: "Mono", monospace; font-weight: 700; font-size: 30px; letter-spacing: 0.12em; color: #d4d6de; }
      .race .rn { position: absolute; top: 380px; width: 420px; text-align: center; font-weight: 900; font-size: 120px; letter-spacing: -0.04em; color: #fff; line-height: 1; }
      .race .floor { position: absolute; left: 80px; top: 1186px; width: 920px; height: 4px; background: rgba(255,255,255,0.35); }
      .x711 { position: absolute; left: 0; width: 1080px; top: 560px; text-align: center; opacity: 0; }
      .x711 span { display: inline-block; font-weight: 900; font-size: 64px; padding: 8px 26px; border-radius: 999px; background: var(--amber); color: #0b0c10; box-shadow: 0 0 40px rgba(255,181,71,0.6); }
      .judges { position: absolute; left: 0; width: 1080px; top: 1085px; display: flex; justify-content: center; gap: 26px; }
      .judges .j { width: 150px; height: 118px; border-radius: 16px; border: 3px solid rgba(255,255,255,0.25); background: rgba(8,9,14,0.75); opacity: 0;
        display: flex; flex-direction: column; align-items: center; justify-content: center; font-family: "Mono", monospace; font-weight: 700; font-size: 22px; letter-spacing: 0.08em; color: #c9ccd6; }
      .judges .j b { font-family: "InterV", sans-serif; font-weight: 900; font-size: 46px; color: #fff; line-height: 1.05; }
      .judges .j.team { border-color: #b99cff; box-shadow: 0 0 26px rgba(185,156,255,0.5); }
      .ev { position: absolute; left: 0; top: 0; width: 600px; height: 170px; opacity: 0; transform-origin: 50% 50%; text-align: center; padding-top: 14px; }
      .ev .et { font-family: "Mono", monospace; font-weight: 700; font-size: 118px; color: #3a1d05; letter-spacing: 0.04em; line-height: 1; }
      .ev .es { font-family: "Mono", monospace; font-weight: 700; font-size: 30px; color: #6b3a0c; letter-spacing: 0.06em; margin-top: 10px; }
      .swb { position: absolute; left: 60px; top: 300px; width: 960px; padding: 26px 30px 24px; border-radius: 26px; background: rgba(10,9,8,0.82); border: 2px solid rgba(255,181,71,0.35); }
      .swb .sh { font-family: "Mono", monospace; font-weight: 700; font-size: 25px; letter-spacing: 0.14em; color: #ffcf8a; margin-bottom: 18px; }
      .swb .grid2 { display: grid; grid-template-columns: 1fr 1fr; column-gap: 40px; row-gap: 12px; }
      .swb .row { display: flex; align-items: center; justify-content: space-between; height: 62px; padding: 0 16px; border-radius: 14px; background: rgba(255,255,255,0.04); }
      .swb .gn { font-family: "Mono", monospace; font-weight: 700; font-size: 34px; color: #9a9ca6; }
      .swb .tg { position: relative; width: 92px; height: 46px; border-radius: 23px; background: #2a2c34; }
      .swb .tg i { position: absolute; left: 5px; top: 5px; width: 36px; height: 36px; border-radius: 50%; background: #6b6e78; }
      .swb .q { margin-top: 20px; font-family: Georgia, serif; font-style: italic; font-size: 33px; line-height: 1.32; color: #f3e6d0; min-height: 132px; }
      .swb .q b { font-style: normal; font-family: "Mono", monospace; font-size: 22px; letter-spacing: 0.1em; color: #ffcf8a; display: block; margin-top: 10px; font-weight: 700; }
      .redbar { position: absolute; }
      .strings { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; opacity: 0; }
      .quote { position: absolute; left: 60px; top: 330px; width: 960px; padding: 40px 44px 34px; border-radius: 26px; background: rgba(250,247,240,0.97);
        box-shadow: 0 40px 90px rgba(0,0,0,0.6); }
      .quote .qk { font-family: "Mono", monospace; font-weight: 700; font-size: 24px; letter-spacing: 0.16em; color: #2f7a52; margin-bottom: 18px; }
      .quote .qt { position: relative; z-index: 0; font-family: Georgia, serif; font-style: italic; font-size: 54px; line-height: 1.26; color: rgba(27,28,34,0.5); }
      .quote .qt + .qt { margin-top: 22px; }
      .quote .qh { color: #1b1c22; background-image: linear-gradient(rgba(255,200,80,0.62), rgba(255,200,80,0.62)); background-repeat: no-repeat;
        background-position: 0 88%; background-size: 0% 78%; }
      .quote .qh.v { background-image: linear-gradient(rgba(185,156,255,0.55), rgba(185,156,255,0.55)); }
      .quote .qa { margin-top: 20px; font-family: "Mono", monospace; font-weight: 700; font-size: 22px; letter-spacing: 0.1em; color: #5a5d66; }
      .proof { position: absolute; left: 60px; width: 960px; top: 1000px; border-radius: 14px; overflow: hidden; box-shadow: 0 20px 50px rgba(0,0,0,0.5); opacity: 0.92; }
      .proof img { display: block; width: 960px; }
      .race .rp { position: absolute; top: 505px; width: 420px; text-align: center; font-family: "Mono", monospace; font-weight: 700; font-size: 22px; letter-spacing: 0.14em; color: #9a9ca6; }
      .race .rn span { background: rgba(6,8,12,0.82); padding: 0 22px; border-radius: 22px; }

      /* end card */
      #end { position: absolute; inset: 0; opacity: 0; }
      #end .dim { position: absolute; inset: 0; background: radial-gradient(ellipse 80% 60% at 50% 40%, rgba(5,6,10,0.72), rgba(5,6,10,0.95)); }
      .mark { position: absolute; left: 420px; top: 470px; width: 240px; height: 240px; border-radius: 56px; background: var(--lime);
        display: flex; align-items: flex-end; justify-content: center; gap: 8px; padding-bottom: 54px; box-shadow: 0 0 80px rgba(200,255,77,0.45); }
      .mark .one { font-weight: 900; font-size: 168px; line-height: 0.73; color: #0b0c10; letter-spacing: -0.06em; }
      .mark .cur { width: 46px; height: 17px; border-radius: 3px; background: #0b0c10; }
      .mtitle { position: absolute; left: 0; width: 1080px; text-align: center; font-weight: 900; letter-spacing: -0.05em; line-height: 0.95; }
      .cta { position: absolute; display: inline-flex; align-items: center; gap: 16px; padding: 24px 36px; border-radius: 999px; background: var(--lime);
        color: #0b0c10; font-weight: 850; font-size: 46px; letter-spacing: -0.01em; }
      .fontwarm { position: absolute; left: -9999px; top: 0; }
      /* Short #9 */
      .hl { background: rgba(255,214,90,0.55); }
      .ph { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }
      .eyeglow { position: absolute; width: 300px; height: 120px; border-radius: 50%; opacity: 0; mix-blend-mode: screen;
        background: radial-gradient(ellipse 50% 50% at 50% 50%, rgba(255,214,120,1) 0, rgba(255,170,60,0.75) 22%, rgba(255,140,30,0) 70%); }
      .seam { position: absolute; left: 536px; top: 0; width: 8px; height: 1920px; background: linear-gradient(180deg, #ff6b6b, #c8ff4d);
        box-shadow: 0 0 30px rgba(200,255,77,0.8); transform-origin: 50% 0; }
      .dark { position: absolute; inset: 0; background: radial-gradient(ellipse 60% 50% at 50% 40%, rgba(0,0,0,0) 30%, rgba(0,0,0,0.75) 100%); opacity: 0; }
      .icon3d { position: absolute; opacity: 0; filter: drop-shadow(0 18px 30px rgba(0,0,0,0.55)); }
      #door { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; opacity: 0; transform-origin: 0 50%;
        background: linear-gradient(90deg, #1b120c 0, #2c1d13 8%, #24170f 50%, #2c1d13 92%, #1b120c 100%);
        box-shadow: inset 0 0 0 26px #120c08, 0 0 80px rgba(0,0,0,0.8); }
      #door i { position: absolute; left: 120px; width: 840px; border: 6px solid rgba(0,0,0,0.45); border-radius: 10px;
        box-shadow: inset 0 0 40px rgba(0,0,0,0.5), 0 2px 0 rgba(255,220,180,0.06); }
      #door b { position: absolute; left: 900px; top: 930px; width: 70px; height: 70px; border-radius: 50%;
        background: radial-gradient(circle at 35% 35%, #ffe2a0, #c08a2e 45%, #5a3a10 100%); box-shadow: 0 6px 20px rgba(0,0,0,0.6); }
      #kh { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; opacity: 0; }
      .grid2250 { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }
      .gauge { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; opacity: 0; }
      .dchip { position: absolute; width: 470px; height: 100px; display: flex; align-items: center; gap: 18px; padding: 0 20px 0 14px;
        border-radius: 18px; background: rgba(8,9,14,0.82); border: 2px solid rgba(255,255,255,0.16); opacity: 0;
        font-family: "Mono", monospace; font-weight: 700; font-size: 25px; letter-spacing: 0.04em; color: #e6e7ec; line-height: 1.1; }
      .dchip img { width: 72px; height: 72px; flex: none; }
      .dchip.hit { border-color: #ff6b6b; box-shadow: 0 0 34px rgba(255,107,107,0.6); color: #fff; }
      .login { position: absolute; left: 160px; top: 420px; width: 760px; padding: 44px 46px 50px; border-radius: 30px; background: #f6f6f3;
        box-shadow: 0 40px 90px rgba(0,0,0,0.6); opacity: 0; color: #15161b; }
      .login .lt { font-weight: 850; font-size: 56px; letter-spacing: -0.03em; }
      .login .ll { font-family: "Mono", monospace; font-weight: 700; font-size: 24px; letter-spacing: 0.12em; color: #6b6e78; margin-top: 34px; }
      .login .lf { position: relative; margin-top: 12px; height: 104px; border-radius: 18px; border: 3px solid #c9ccd6; background: #fff;
        font-size: 64px; letter-spacing: 0.2em; line-height: 98px; padding-left: 26px; color: #15161b; overflow: hidden; }
      .login .lx { position: absolute; left: -10px; top: 50px; height: 8px; width: 700px; background: #ff3b30; border-radius: 4px;
        transform-origin: 0 50%; transform: scaleX(0); box-shadow: 0 0 16px rgba(255,59,48,0.7); }
      .login .lb { margin-top: 30px; height: 100px; border-radius: 18px; background: #2a2c34; color: #fff; font-weight: 800; font-size: 40px;
        display: flex; align-items: center; justify-content: center; }
      .phone { position: absolute; left: 200px; top: 300px; width: 680px; height: 920px; border-radius: 70px; background: #0d0e12;
        border: 4px solid #3a3d47; box-shadow: 0 50px 100px rgba(0,0,0,0.7); opacity: 0; overflow: hidden; }
      .phone .ps { position: absolute; left: 22px; top: 22px; right: 22px; bottom: 22px; border-radius: 52px; background: #f4f4f1; color: #15161b; padding: 70px 46px 0; }
      .phone .pi { width: 120px; height: 120px; border-radius: 30px; background: linear-gradient(135deg, #7c8496, #3a3f4c); margin: 0 auto;
        display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 70px; color: #fff; }
      .phone .pt { margin-top: 30px; text-align: center; font-weight: 850; font-size: 44px; letter-spacing: -0.02em; line-height: 1.12; }
      .phone .pr { display: flex; align-items: center; gap: 22px; margin-top: 30px; font-size: 32px; font-weight: 600; line-height: 1.2; color: #2a2c34; }
      .phone .pr img { width: 64px; height: 64px; flex: none; }
      .phone .pbn { position: absolute; left: 46px; right: 46px; bottom: 60px; display: flex; gap: 22px; }
      .phone .pbn div { flex: 1; height: 100px; border-radius: 50px; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 38px; }
      .phone .pc { background: #e2e3e8; color: #2a2c34; } .phone .pa { background: #15161b; color: #c8ff4d; }
      .finger { position: absolute; width: 90px; height: 90px; border-radius: 50%; background: rgba(255,255,255,0.85); border: 4px solid rgba(0,0,0,0.25);
        box-shadow: 0 10px 30px rgba(0,0,0,0.45); opacity: 0; }
      .pulse { position: absolute; width: 300px; height: 120px; border-radius: 60px; border: 6px solid #c8ff4d; opacity: 0; box-shadow: 0 0 30px rgba(200,255,77,0.7); }
      .lane { position: absolute; left: 70px; width: 940px; height: 150px; border-radius: 24px; background: rgba(8,9,14,0.75); border: 2px solid rgba(255,255,255,0.14); opacity: 0; }
      .lane .ln { position: absolute; left: 28px; top: -46px; font-family: "Mono", monospace; font-weight: 700; font-size: 28px; letter-spacing: 0.12em; }
      .lane .lbar { position: absolute; left: 0; top: 0; height: 100%; border-radius: 24px; transform-origin: 0 50%; transform: scaleX(0); opacity: 0.35; }
      .lane img { position: absolute; top: 15px; left: 10px; width: 120px; height: 120px; }
      .finish { position: absolute; left: 900px; top: 470px; width: 10px; height: 520px; opacity: 0;
        background: repeating-linear-gradient(180deg, #fff 0, #fff 20px, #15161b 20px, #15161b 40px); }
      .netw { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; opacity: 0; }
      .qbig { font-family: "InterV", sans-serif; font-style: normal; font-weight: 850; font-size: 56px; letter-spacing: -0.03em; line-height: 1.1; color: #1b1c22; }
      .stampS { position: absolute; font-weight: 900; font-size: 46px; padding: 6px 18px; border: 6px solid currentColor; border-radius: 12px; color: #c9352b;
        background: rgba(250,247,240,0.85); opacity: 0; white-space: nowrap; }
      .proof .hlp { position: absolute; background: rgba(255,214,90,0.5); mix-blend-mode: multiply; border-radius: 4px; transform-origin: 0 50%; transform: scaleX(0); }
      .proof { overflow: hidden; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="%DUR%" data-width="1080" data-height="1920">
      <div id="base" class="clip" data-start="0" data-duration="%DUR%" style="background: #04050a; z-index: 0"></div>
%SHOTS%
      <div id="ui" class="clip" data-start="0" data-duration="%DUR%" style="z-index: 100">
        <div id="door"><i style="top:140px;height:700px"></i><i style="top:1000px;height:780px"></i><b></b></div>
        <svg id="kh" viewBox="0 0 1080 1920"><g id="khg"><path fill="#000" fill-rule="evenodd"
          d="M -20000 -20000 H 21080 V 21920 H -20000 Z M 540 640 m -62 0 a 62 62 0 1 0 124 0 a 62 62 0 1 0 -124 0 Z M 514 690 L 566 690 L 596 830 L 484 830 Z" /></g></svg>
        <div class="vig"></div>
        <div class="dark" id="dark"></div>
        <div class="topshade"></div>
        <div class="botshade" id="botshade"></div>

        <!-- s02: one light per tenant Microsoft says was tried -->
        <canvas id="grid" class="grid2250" width="1080" height="1920" style="opacity:0"></canvas>
        <!-- s03: the stopwatch and the real line -->
        <svg id="watch" viewBox="0 0 1080 1920" style="position:absolute;left:0;top:0;width:1080px;height:1920px;opacity:0">
          <circle cx="540" cy="540" r="200" fill="rgba(6,8,12,0.55)" stroke="rgba(255,255,255,0.18)" stroke-width="10" />
          <g id="wticks"></g>
          <circle id="warc" cx="540" cy="540" r="200" fill="none" stroke="#ffb547" stroke-width="14" stroke-linecap="round" transform="rotate(-90 540 540)"
            style="filter: drop-shadow(0 0 14px rgba(255,181,71,0.9))" />
          <line id="whand" x1="540" y1="540" x2="540" y2="368" stroke="#fff" stroke-width="8" stroke-linecap="round" />
          <circle cx="540" cy="540" r="16" fill="#ffb547" />
          <text id="wread" x="540" y="615" text-anchor="middle" font-family="Mono" font-weight="700" font-size="54" fill="#fff" letter-spacing="2">0:00:00</text>
        </svg>
        <div id="pf-s03"></div>
        <!-- s05 -->
        <div class="chip" id="chHouse" style="left:60px;top:1110px;color:#ffb547"><span class="sw"></span>1 HOUSE = 1 COMPANY'S CLOUD</div>
        <!-- s06 -->
        <img class="icon3d" id="icMail" src="assets/3d/email.png" alt="" style="left:70px;top:470px;width:290px" />
        <img class="icon3d" id="icFile" src="assets/3d/folder.png" alt="" style="left:395px;top:690px;width:290px" />
        <img class="icon3d" id="icLock" src="assets/3d/locked.png" alt="" style="left:720px;top:470px;width:290px" />
        <!-- s09 -->
        <div class="cal" id="cal" style="left:330px;top:330px;width:420px"><div class="ch">ON DUTY</div><div class="cn" id="calN" style="font-size:150px;padding-top:24px">3AM</div>
          <div class="cu" id="calU">TUESDAY</div></div>
        <div id="pf-s09"></div>
        <!-- s12: Microsoft's 14 sectors -->
        <div id="doors"></div>
        <!-- s14: the password spray -->
        <svg class="gauge" id="gauge" viewBox="0 0 1080 1920">
          <path d="M 220 820 A 320 320 0 0 1 860 820" fill="none" stroke="rgba(255,255,255,0.16)" stroke-width="44" stroke-linecap="round" />
          <path id="garc" d="M 220 820 A 320 320 0 0 1 860 820" fill="none" stroke="#ff6b6b" stroke-width="44" stroke-linecap="round"
            style="filter: drop-shadow(0 0 18px rgba(255,107,107,0.9))" />
          <line id="gneedle" x1="540" y1="820" x2="540" y2="560" stroke="#fff" stroke-width="12" stroke-linecap="round" />
          <circle cx="540" cy="820" r="26" fill="#fff" />
          <text x="540" y="900" text-anchor="middle" font-family="Mono" font-weight="700" font-size="32" fill="#e6e7ec" letter-spacing="5">PASSWORD TRIES / MINUTE</text>
        </svg>
        <div class="chip" id="chFail" style="left:60px;top:1110px;color:#ff8a7a"><span class="sw"></span>FAILED SIGN-INS <span id="failN">0</span></div>
        <!-- s16 -->
        <div class="readout" id="rdZero" style="top:330px;padding:24px 0 30px;background:radial-gradient(ellipse 46% 50% at 50% 50%, rgba(4,5,10,0.8), rgba(4,5,10,0) 100%)">
          <div class="rl">SUCCESSFUL SIGN-INS</div><div class="rv" style="font-size:230px">0</div></div>
        <!-- s17 -->
        <svg id="lockring" viewBox="0 0 1080 1920" style="position:absolute;left:0;top:0;width:1080px;height:1920px;opacity:0">
          <circle cx="540" cy="640" r="210" fill="rgba(6,8,12,0.62)" stroke="rgba(255,255,255,0.15)" stroke-width="26" />
          <circle id="lrarc" cx="540" cy="640" r="210" fill="none" stroke="#ff6b6b" stroke-width="26" stroke-linecap="round" transform="rotate(-90 540 640)"
            style="filter: drop-shadow(0 0 16px rgba(255,107,107,0.85))" />
          <text id="lrN" x="540" y="668" text-anchor="middle" font-family="InterV" font-weight="900" font-size="120" fill="#fff">0%</text>
          <text x="540" y="730" text-anchor="middle" font-family="Mono" font-weight="700" font-size="28" fill="#e6e7ec" letter-spacing="4">LOCKED OUT</text>
        </svg>
        <!-- s20 -->
        <div class="chip" id="chSpare" style="left:60px;top:1110px;color:#ffb547"><span class="sw"></span>SPARE KEY = AN APP YOU TRUSTED</div>
        <!-- s22: one ring, every door -->
        <svg class="netw" id="netw" viewBox="0 0 1080 1920"><g id="netL" stroke="#ffb547" stroke-width="3" fill="none" style="filter: drop-shadow(0 0 6px rgba(255,181,71,0.8))"></g></svg>
        <div id="netH"></div>
        <img class="icon3d" id="ring" src="assets/3d/oldkey.png" alt="" style="left:430px;top:590px;width:220px" />
        <div class="chip" id="chRing" style="left:340px;top:820px;color:#ffb547;font-size:26px"><span class="sw"></span>CLOUD BACKUP</div>
        <div class="chip" id="chDoorQ" style="left:60px;top:1110px;color:#ffd38a;font-size:22px;letter-spacing:0.04em"><span class="sw"></span>"ONE TRUSTED CONNECTION CAN OPEN THE DOOR TO MANY"</div>
        <!-- s24 -->
        <div class="login" id="login"><div class="lt">Sign in</div><div class="ll">PASSWORD</div>
          <div class="lf"><span id="dots"></span><div class="lx" id="lx"></div></div><div class="lb">Continue</div></div>
        <div class="chip" id="chTrusted" style="left:60px;top:1110px;color:#7ee787"><span class="sw"></span>THE APP WAS ALREADY LET IN</div>
        <!-- s27-s29: what Microsoft saw inside -->
        <div class="chip" id="chRecon" style="left:60px;top:1110px;color:#4fd0ff"><span class="sw"></span>MICROSOFT SAW: RECONNAISSANCE</div>
        <div class="chip" id="chCreds" style="left:60px;top:1110px;color:#ffb547"><span class="sw"></span>MICROSOFT SAW: NEW APP CREDENTIALS</div>
        <div class="chip" id="chRoles" style="left:60px;top:1110px;color:#ff8a7a"><span class="sw"></span>MICROSOFT SAW: PRIVILEGED ROLES CHANGED</div>
        <img class="icon3d" id="crown" src="assets/3d/crown.png" alt="" style="left:455px;top:300px;width:170px" />
        <!-- s33 -->
        <div class="chip" id="chOpen" style="left:60px;top:1110px;color:#7ee787"><span class="sw"></span>OPEN SOURCE · PUBLIC ON GITHUB</div>
        <!-- s35 -->
        <div class="chip" id="chBurglar" style="left:60px;top:1110px;color:#ff6b6b"><span class="sw"></span>BURGLAR</div>
        <div class="chip" id="chSmith" style="left:700px;top:1110px;color:#7ee787"><span class="sw"></span>LOCKSMITH</div>
        <!-- s36: the race -->
        <div class="lane" id="laneB" style="top:520px"><div class="ln" style="color:#ff6b6b">BURGLAR</div><div class="lbar" id="barB" style="width:860px;background:#ff6b6b"></div><img id="runB" src="assets/3d/robot.png" alt="" /></div>
        <div class="lane" id="laneL" style="top:800px"><div class="ln" style="color:#7ee787">LOCKSMITH</div><div class="lbar" id="barL" style="width:860px;background:#7ee787"></div><img id="runL" src="assets/3d/robot.png" alt="" /></div>
        <div class="finish" id="finish"></div>
        <div class="chip" id="chWeak" style="left:640px;top:1020px;color:#ffd38a"><span class="sw"></span>THE WEAK SPOT</div>
        <!-- s37 -->
        <div class="phone" id="phone"><div class="ps"><div class="pi">?</div><div class="pt">An app wants access to your account</div>
          <div class="pr"><img src="assets/3d/email.png" alt="" />Read and send your email</div>
          <div class="pr"><img src="assets/3d/folder.png" alt="" />See and download your files</div>
          <div class="pr"><img src="assets/3d/key.png" alt="" />Keep access, even when you're away</div>
          <div class="pbn"><div class="pc">Cancel</div><div class="pa" id="allow">Allow</div></div></div></div>
        <div class="pulse" id="pulse"></div>
        <div class="finger" id="finger"></div>
        <!-- s38 -->
        <div class="chip" id="chTip" style="left:60px;top:1110px;color:#c8ff4d"><span class="sw"></span>TIP: CHECK YOUR CONNECTED APPS</div>

        %LABELS%

        <div class="grain" id="grain"></div>
        <div class="progress" id="prog" style="background:var(--lime)"></div>
        <div class="tag2" id="tag"><span class="dot"></span>AI EXPLAINED · TRUE STORY</div>
        <div class="brandmark" id="bm" style="right: 60px; top: 158px; padding-top: 10px">@ONEAITRICK</div>
        <div id="caps"></div>
        <div id="end">
          <div class="dim"></div>
          <div class="mark" id="mark"><span class="one">1</span><span class="cur"></span></div>
          <div class="mtitle" id="ename" style="top:760px;font-size:110px">One <span style="color:var(--lime)">AI</span> Trick</div>
          <div class="mtitle" id="ehandle" style="top:900px;font-family:Mono, monospace;font-weight:500;font-size:40px;letter-spacing:0.04em;color:var(--muted)">@oneaitrick</div>
          <div class="cta" id="fol" style="left:220px;top:1000px">+ Follow for AI, explained</div>
        </div>
        <div class="flash" id="flash"></div>
        <div class="black" id="black"></div>
        <div class="fontwarm"><span style="font-family:InterV;font-weight:900">Aa</span><span style="font-family:Mono;font-weight:700">Aa</span><span style="font-family:Mono;font-weight:500">Aa</span><span style="font-family:Georgia;font-style:italic">Aa</span></div>
      </div>

      <audio id="mix" src="assets/mix.wav" data-start="0" data-duration="%DUR%" data-volume="1"></audio>
    </div>

    <script>
      const DUR = %DUR%, HND = %H%;
      const SH = %SHOTSJS%;
      const GEO = %GEO%;
      const PAGES = %PAGES%;
      const EYE = %EYE%;
      const $ = (s) => document.querySelector(s);
      const tl = gsap.timeline({ paused: true });
      const E = "power3.out";
      const fx = (id) => "#fx-" + id, cam = (id) => "#cam-" + id;
      const T0 = Object.fromEntries(SH.map((s) => [s.id, s.t0])), T1 = Object.fromEntries(SH.map((s) => [s.id, s.t1]));
      const rgba = (hex, a) => { const n = parseInt(hex.slice(1), 16); return `rgba(${n >> 16},${(n >> 8) & 255},${n & 255},${a})`; };
      const el = (tag, cls, css, parent) => { const e = document.createElement(tag); if (cls) e.className = cls; if (css) e.style.cssText = css; (parent || $("#ui")).appendChild(e); return e; };
      let seed = 9; const rnd = () => (seed = (seed * 9301 + 49297) % 233280) / 233280;

      // ---------- shots: visibility and default camera ----------
      const DOCS = ["s10", "s11", "s15", "s31"];
      const CUSTOM_CAM = new Set(DOCS.concat(["s07", "s18", "s30", "s35"]));
      SH.forEach((s, i) => {
        tl.set(fx(s.id), { opacity: i === 0 ? 1 : 0 }, 0);
        const a = Math.max(0, s.t0 - HND), b = s.t1 + HND;
        if (CUSTOM_CAM.has(s.id)) return;
        tl.fromTo(cam(s.id), { scale: 1 }, { scale: 1.07, duration: b - a, ease: "none" }, a);
      });
      const flash = (t, a, d, c) => { tl.set("#flash", { background: c || "#fff" }, t); tl.fromTo("#flash", { opacity: a }, { opacity: 0, duration: d || 0.35, ease: "power2.out", immediateRender: false }, t); };
      const cardIn = (id, t) => { const c = document.querySelectorAll("#cam-" + id + " .card");
        tl.fromTo(c, { opacity: 0, scale: 0.86, y: 60 }, { opacity: 1, scale: 1, y: 0, duration: 0.42, ease: "back.out(1.6)", stagger: 0.12 }, t); };
      const swap = (A, B, T) => { tl.set(fx(B), { opacity: 1 }, T); tl.set(fx(A), { opacity: 0 }, T); };
      const TR = {
        whip(A, B, T) { tl.fromTo(fx(B), { opacity: 1, x: 1080, filter: "blur(22px)" }, { x: 0, filter: "blur(0px)", duration: 0.28, ease: "power3.inOut" }, T - 0.16);
          tl.to(fx(A), { x: -760, filter: "blur(22px)", duration: 0.28, ease: "power3.inOut" }, T - 0.16); tl.set(fx(A), { opacity: 0 }, T + 0.14); },
        slideup(A, B, T) { tl.fromTo(fx(B), { opacity: 1, y: 1920, filter: "blur(22px)" }, { y: 0, filter: "blur(0px)", duration: 0.3, ease: "power3.inOut" }, T - 0.17);
          tl.to(fx(A), { y: -1100, filter: "blur(22px)", duration: 0.3, ease: "power3.inOut" }, T - 0.17); tl.set(fx(A), { opacity: 0 }, T + 0.15); },
        zoom(A, B, T) { tl.to(fx(A), { scale: 1.45, filter: "blur(18px)", opacity: 0, duration: 0.26, ease: "power2.in" }, T - 0.16);
          tl.fromTo(fx(B), { opacity: 0, scale: 0.84, filter: "blur(16px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.32, ease: E }, T - 0.1); flash(T - 0.02, 0.25, 0.3); },
        flash(A, B, T, c) { swap(A, B, T); flash(T, 0.6, 0.42, c); },
        light(A, B, T) { tl.to("#flash", { opacity: 1, duration: 0.14, ease: "power2.in", background: "#fffaf0" }, T - 0.14); swap(A, B, T);
          tl.to("#flash", { opacity: 0, duration: 0.6, ease: "power2.out" }, T); tl.fromTo(fx(B), { scale: 1.08 }, { scale: 1, duration: 0.7, ease: E, immediateRender: false }, T); },
        dip(A, B, T) { tl.to("#black", { opacity: 1, duration: 0.14, ease: "power1.in" }, T - 0.14); swap(A, B, T); tl.to("#black", { opacity: 0, duration: 0.28, ease: "power1.out" }, T); },
        glitch(A, B, T) { swap(A, B, T);
          [[0, 34, "hue-rotate(80deg) saturate(2)"], [0.033, -26, "hue-rotate(-60deg)"], [0.066, 16, "none"], [0.1, -8, "none"], [0.133, 0, "none"]].forEach(([dt, x, f]) => tl.set(fx(B), { x, filter: f }, T + dt));
          flash(T, 0.3, 0.25, "#4fd0ff"); },
        card(A, B, T) { tl.fromTo(fx(B), { opacity: 0 }, { opacity: 1, duration: 0.22, ease: "power1.out" }, T - 0.12); tl.set(fx(A), { opacity: 0 }, T + 0.12); cardIn(B, T - 0.05); },
        fade(A, B, T) { tl.fromTo(fx(B), { opacity: 0 }, { opacity: 1, duration: 0.5, ease: "power1.inOut" }, T - 0.25); tl.set(fx(A), { opacity: 0 }, T + 0.26); },
        // a front door swings shut over A and open on B (hinge on the left)
        door(A, B, T) { tl.set("#door", { opacity: 1, transformPerspective: 1800, rotationY: -92, x: 0 }, T - 0.2);
          tl.to("#door", { rotationY: 0, duration: 0.2, ease: "power2.in" }, T - 0.2); swap(A, B, T);
          tl.to("#door", { rotationY: 92, duration: 0.3, ease: "power2.out" }, T + 0.02); tl.set("#door", { opacity: 0 }, T + 0.33); },
        // through the keyhole: the frame closes to a keyhole on A, then opens out of it on B
        keyhole(A, B, T) { tl.set("#kh", { opacity: 1 }, T - 0.2); tl.set("#khg", { transformOrigin: "540px 735px" }, 0);
          tl.fromTo("#khg", { scale: 26 }, { scale: 1, duration: 0.2, ease: "power3.in", immediateRender: false }, T - 0.2); swap(A, B, T);
          tl.to("#khg", { scale: 26, duration: 0.34, ease: "power3.in" }, T + 0.06); tl.set("#kh", { opacity: 0 }, T + 0.42); },
        // the record scratch: a hard freeze, a jolt and the colour drains
        scratch(A, B, T) { swap(A, B, T); [[0, 26, 2], [0.04, -20, -2], [0.08, 12, 1], [0.12, -6, 0], [0.16, 0, 0]].forEach(([dt, x, r]) => tl.set(fx(B), { x, rotation: r }, T + dt));
          flash(T, 0.45, 0.3, "#ffffff"); },
      };
      const CUTS = [["s01", "s02", "zoom"], ["s02", "s03", "door"], ["s03", "s04", "keyhole"], ["s04", "s05", "door"], ["s05", "s06", "keyhole"],
        ["s06", "s07", "dip"], ["s07", "s08", "flash", "#ffb547"], ["s08", "s09", "whip"], ["s09", "s10", "card"], ["s10", "s11", "card"],
        ["s11", "s12", "slideup"], ["s12", "s13", "card"], ["s13", "s14", "glitch"], ["s14", "s15", "card"], ["s15", "s16", "zoom"],
        ["s16", "s17", "flash", "#ff6b6b"], ["s17", "s18", "dip"], ["s18", "s19", "keyhole"], ["s19", "s20", "flash", "#ffb547"], ["s20", "s21", "card"],
        ["s21", "s22", "zoom"], ["s22", "s23", "whip"], ["s23", "s24", "card"], ["s24", "s25", "door"], ["s25", "s26", "flash", "#7ee787"],
        ["s26", "s27", "door"], ["s27", "s28", "whip"], ["s28", "s29", "glitch"], ["s29", "s30", "scratch"], ["s30", "s31", "card"],
        ["s31", "s32", "light"], ["s32", "s33", "whip"], ["s33", "s34", "card"], ["s34", "s35", "whip"], ["s35", "s36", "zoom"],
        ["s36", "s37", "slideup"], ["s37", "s38", "keyhole"], ["s38", "s39", "door"]];
      CUTS.forEach(([A, B, k, c]) => TR[k](A, B, T0[B], c));
      tl.fromTo("#flash", { opacity: 0 }, { opacity: 0, duration: 0.01 }, 0);

      // ---------- helpers ----------
      const show = (sel, t0, t1, from) => { tl.fromTo(sel, Object.assign({ opacity: 0, y: 14 }, from || {}), { opacity: 1, y: 0, x: 0, duration: 0.3, ease: E }, t0);
        tl.to(sel, { opacity: 0, duration: 0.18 }, t1); };
      const stamp = (sel, t0, t1, rot) => { tl.fromTo(sel, { opacity: 0, scale: 2.4, rotation: rot || -8 }, { opacity: 1, scale: 1, rotation: rot || -8, duration: 0.2, ease: "power4.out" }, t0);
        tl.to(sel, { opacity: 0, duration: 0.18 }, t1); };
      const punch = (id, t, s) => { tl.fromTo(fx(id), { scale: 1 }, { scale: 1 + (s || 0.06), duration: 0.12, ease: "power2.out", immediateRender: false }, t);
        tl.to(fx(id), { scale: 1, duration: 0.5, ease: "power2.inOut" }, t + 0.12); };
      const shake = (id, t, a, n) => { for (let k = 0; k < (n || 6); k++) tl.set(fx(id), { x: (k % 2 ? -1 : 1) * a * (1 - k / (n || 6)), y: (k % 3 - 1) * a * 0.5 }, t + k * 0.04); tl.set(fx(id), { x: 0, y: 0 }, t + (n || 6) * 0.04); };
      const pop = (sel, t, t1, from) => { tl.fromTo(sel, Object.assign({ opacity: 0, scale: 0.3, y: 40 }, from || {}), { opacity: 1, scale: 1, y: 0, duration: 0.34, ease: "back.out(2)" }, t);
        if (t1) tl.to(sel, { opacity: 0, duration: 0.18 }, t1); };
      const countTo = (sel, v, t, d, fmt) => { const m = { v: 0 }; const e = $(sel);
        tl.fromTo(m, { v: 0 }, { v, duration: d, ease: "power2.out", onUpdate() { e.textContent = fmt ? fmt(m.v) : Math.round(m.v).toLocaleString("en-US"); } }, t); };
      const docCam = (id) => { const g = GEO[id]; const hls = g[6] || []; const a = Math.max(0, T0[id] - HND), b = T1[id] + HND;
        const kf = (S, px, py) => { let y = 740 - S * py; const dy = 300 - (y + S * g[1]); if (dy > 0 && dy <= 160) y += dy; return { scale: S, x: 540 - S * px, y }; };
        tl.set(cam(id), { transformOrigin: "0px 0px" }, 0);
        const zs = (w) => Math.max(1.05, Math.min(1.6, 880 / (w + 80)));
        const [t, hx, hy, w] = hls[0]; const end = Math.max(a + 0.35, t + 0.25);
        tl.fromTo(cam(id), kf(1, 540, 740), Object.assign(kf(zs(w), hx, hy), { duration: end - a, ease: "power2.inOut" }), a);
        if (b > end + 0.05) tl.to(cam(id), Object.assign(kf(zs(w) * 1.04, hx, hy), { duration: b - end, ease: "none" }), end); };
      // a quote set large, with the real page strip under it as proof (its highlight sweeps too)
      const quote = (host, kicker, html, t, tHl, proofName, proofTop, proofW, kcol) => { const q = el("div", "quote", "", $(host));
        q.innerHTML = `<div class="qk" style="color:${kcol || "#2f7a52"}">${kicker}</div>${html}`;
        tl.fromTo(q, { opacity: 0, y: 50, rotation: -1.5 }, { opacity: 1, y: 0, rotation: -0.6, duration: 0.35, ease: "back.out(1.4)" }, t);
        q.querySelectorAll(".qh").forEach((h) => { tl.to(h, { backgroundSize: "100% 78%", color: "#000", duration: 0.5, ease: "power2.inOut" }, tHl); });
        if (proofName) proof(host, proofName, proofTop, proofW, t + 0.2, tHl + 0.1);
        return q; };
      const proof = (host, name, top, w, t, tHl) => { const P = PAGES[name]; const s = w / P.w; const pr = el("div", "proof", `top:${top}px;left:${(1080 - w) / 2}px;width:${w}px`, $(host));
        pr.innerHTML = `<img src="assets/pages/${name}.png" alt="" style="width:${w}px" />` + P.boxes.map(([x, y, bw, bh]) => `<div class="hlp" style="left:${x * s}px;top:${y * s}px;width:${bw * s}px;height:${bh * s}px"></div>`).join("");
        tl.fromTo(pr, { opacity: 0, y: 40 }, { opacity: 0.94, y: 0, duration: 0.3, ease: E }, t);
        tl.to(pr.querySelectorAll(".hlp"), { scaleX: 1, duration: 0.25, ease: "power2.inOut", stagger: 0.12 }, tHl);
        return pr; };

      const TEXTAT = []; const textAt = (sel, steps) => TEXTAT.push([$(sel), steps]);
      tl.fromTo({ v: 0 }, { v: 0 }, { v: 1, duration: DUR, ease: "none", onUpdate() { const t = tl.time();
        TEXTAT.forEach(([e, st]) => { let txt = st[0][1]; st.forEach(([a, x]) => { if (t >= a) txt = x; }); if (e.textContent !== txt) e.textContent = txt; }); } }, 0);

      // highlights and source labels
      %HLJS%.forEach(([id, t, d]) => tl.to("#" + id, { scaleX: 1, duration: d, ease: "power2.inOut" }, t));
      %LABJS%.forEach(([sel, a, b]) => show(sel, a, b, { x: -20, y: 0 }));
      DOCS.forEach((id) => docCam(id));

      // ---------- the hook ----------
      punch("s01", 0.26, 0.05);
      // s02: 2,250 lights, one per tenant Microsoft says the AI tried to sign in to
      (function () { const cv = $("#grid"), g = cv.getContext("2d"); const C = 50, Rw = 45, x0 = 99, y0 = 330, p = 18;
        const order = Array.from({ length: C * Rw }, (_, i) => i).sort(() => rnd() - 0.5); const rank = new Array(C * Rw); order.forEach((i, k) => (rank[i] = k));
        const st = { f: 0 };
        const draw = () => { g.clearRect(0, 0, 1080, 1920); const on = st.f * C * Rw;
          for (let i = 0; i < C * Rw; i++) { const x = x0 + (i % C) * p, y = y0 + Math.floor(i / C) * p; const lit = rank[i] < on;
            g.beginPath(); g.arc(x, y, lit ? 5.5 : 3.5, 0, 6.283); g.fillStyle = lit ? "#ffcf6a" : "rgba(255,255,255,0.13)"; if (lit) { g.shadowColor = "#ffb547"; g.shadowBlur = 8; } else g.shadowBlur = 0; g.fill(); } };
        tl.fromTo("#grid", { opacity: 0 }, { opacity: 1, duration: 0.25 }, 2.36); tl.to("#grid", { opacity: 0, duration: 0.15 }, 5.42);
        tl.fromTo(st, { f: 0 }, { f: 1, duration: 2.2, ease: "power1.in", onUpdate: draw }, 2.4);
        tl.fromTo("#grid", { scale: 1, transformOrigin: "540px 735px" }, { scale: 1.08, duration: 3.2, ease: "none" }, 2.33); })();
      // s03: under three hours, on a stopwatch; then Microsoft's own line
      (function () { const g = $("#wticks"); for (let k = 0; k < 12; k++) { const a = (k / 12) * Math.PI * 2;
          const l = document.createElementNS("http://www.w3.org/2000/svg", "line"); l.setAttribute("x1", 540 + Math.sin(a) * 168); l.setAttribute("y1", 540 - Math.cos(a) * 168);
          l.setAttribute("x2", 540 + Math.sin(a) * 188); l.setAttribute("y2", 540 - Math.cos(a) * 188); l.setAttribute("stroke", "rgba(255,255,255,0.55)"); l.setAttribute("stroke-width", k % 3 ? 4 : 8); g.appendChild(l); }
        const C = 2 * Math.PI * 200; $("#warc").style.strokeDasharray = C; const m = { v: 0 };
        tl.fromTo("#watch", { opacity: 0, scale: 0.8, transformOrigin: "540px 540px" }, { opacity: 1, scale: 1, duration: 0.25, ease: E }, 5.52); tl.to("#watch", { opacity: 0, duration: 0.15 }, 8.22);
        tl.fromTo(m, { v: 0 }, { v: 0.9997, duration: 1.4, ease: "power2.inOut", onUpdate() { const h = m.v * 3; $("#warc").style.strokeDashoffset = C * (1 - h / 12);
          $("#whand").setAttribute("transform", `rotate(${h * 30} 540 540)`); const s = Math.floor(h * 3600); $("#wread").textContent = Math.floor(s / 3600) + ":" + String(Math.floor(s / 60) % 60).padStart(2, "0") + ":" + String(s % 60).padStart(2, "0"); } }, 5.6);
        tl.to("#warc", { stroke: "#ff6b6b", duration: 0.2 }, 6.86);
        proof("#pf-s03", "r1_hours", 772, 640, 6.2, 7.0); tl.to("#pf-s03", { opacity: 0, duration: 0.15 }, 8.22); })();
      punch("s04", 8.83, 0.04);
      show("#chHouse", 10.1, 11.72, { x: -20 });
      pop("#icMail", 12.1, 14.92); pop("#icFile", 13.02, 14.92); pop("#icLock", 14.1, 14.92);
      tl.to("#icLock", { rotation: -8, duration: 0.08, yoyo: true, repeat: 3 }, 14.45);
      // s07: the moving photo: the robot moves faster than the street behind it; its eye flares on "robot"
      (function () { const a = T0.s07 - HND, b = T1.s07 + HND;
        tl.set(["#phbg", "#phfg"], { transformOrigin: "540px 2234px" }, 0);
        tl.fromTo("#phbg", { scale: 1.0 }, { scale: 1.04, duration: b - a, ease: "none" }, a);
        tl.fromTo("#phfg", { scale: 1.0, x: 0 }, { scale: 1.11, x: -14, duration: b - a, ease: "none" }, a);
        tl.fromTo("#eye", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1.7, duration: 0.18, ease: "power2.out" }, 17.86);
        tl.to("#eye", { opacity: 0.55, scale: 1.1, duration: 0.6, ease: "power2.inOut" }, 18.04);
        tl.set("#eye", { transformOrigin: "150px 60px" }, 0);
        tl.fromTo("#eye", { x: 0, y: 0 }, { x: (EYE[0] - 540) * 0.11 - 14, y: (EYE[1] - 2234) * 0.11, duration: b - a, ease: "none" }, a); })();
      punch("s08", 19.39, 0.06);
      // s09: on duty, around the clock
      (function () { tl.fromTo("#cal", { opacity: 0, y: -40, rotation: 4 }, { opacity: 1, y: 0, rotation: 0, duration: 0.3, ease: "back.out(1.6)" }, 20.68); tl.to("#cal", { opacity: 0, duration: 0.15 }, 22.88);
        textAt("#calN", [[0, "3AM"], [21.22, "SUN"], [21.94, "25 DEC"]]); textAt("#calU", [[0, "TUESDAY"], [21.22, "11:40 PM"], [21.94, "CHRISTMAS"]]);
        [21.22, 21.94].forEach((t) => { tl.to("#calN", { rotationX: 90, duration: 0.08, ease: "power2.in" }, t - 0.08); tl.to("#calN", { rotationX: 0, duration: 0.12, ease: "power2.out" }, t); });
        proof("#pf-s09", "r1_clock", 860, 820, 21.0, 21.45); tl.to("#pf-s09", { opacity: 0, duration: 0.15 }, 22.88); })();
      // s12: Microsoft's 14 sectors as 14 doors; banks and governments when they're said
      (function () { const S = ["AEROSPACE &amp; DEFENSE", "AUTOMOTIVE", "CHEMICALS", "ENERGY", "FINANCIAL SERVICES", "GOVERNMENT", "LEGAL",
          "MANUFACTURING", "MEDIA", "MILITARY", "SEMICONDUCTOR", "SOFTWARE", "TECHNOLOGY", "THINK TANKS &amp; NON-PROFITS"];
        S.forEach((n, k) => { const c = el("div", "dchip", `left:${k % 2 ? 550 : 60}px;top:${330 + Math.floor(k / 2) * 116}px`, $("#doors"));
          c.innerHTML = `<img src="assets/3d/door.png" alt="" /><span>${n}</span>`; c.id = "dc" + k;
          tl.fromTo(c, { opacity: 0, x: k % 2 ? 60 : -60 }, { opacity: 1, x: 0, duration: 0.24, ease: E }, 25.6 + k * 0.085); tl.to(c, { opacity: 0, duration: 0.15 }, 29.18); });
        [[4, 27.78], [5, 28.32]].forEach(([k, t]) => { tl.set("#dc" + k, { borderColor: "#ff6b6b", boxShadow: "0 0 34px rgba(255,107,107,0.6)", color: "#ffffff", background: "rgba(40,10,12,0.88)" }, t); tl.fromTo("#dc" + k, { scale: 1.12 }, { scale: 1, duration: 0.3, ease: "back.out(2)", immediateRender: false }, t); }); })();
      // s13: China's response, set large, with the Reuters strip under it
      quote("#gx-s13", "● CHINESE EMBASSY IN WASHINGTON, TO REUTERS", '<div class="qt" style="font-size:46px">“[China] opposes and fights hacking activities in accordance with the law. At the same time, <span class="qh">we oppose smears and attacks against China</span> under the excuse of cybersecurity issues.”</div>',
        29.3, 29.75, "r4_embassy", 960, 960, "#b0413a");
      // s14: the password spray on a gauge; the failures run up
      (function () { const L = 1006; $("#garc").style.strokeDasharray = L; const m = { v: 0 };
        tl.fromTo("#gauge", { opacity: 0 }, { opacity: 1, duration: 0.25 }, 31.5); tl.to("#gauge", { opacity: 0, duration: 0.15 }, 34.65);
        tl.fromTo(m, { v: 0 }, { v: 1, duration: 0.9, ease: "power3.out", immediateRender: false, onUpdate() { $("#garc").style.strokeDashoffset = L * (1 - m.v * 0.96); $("#gneedle").setAttribute("transform", `rotate(${-90 + 172 * m.v} 540 820)`); } }, 32.4);
        for (let k = 0; k < 18; k++) tl.set("#gneedle", { attr: { transform: `rotate(${82 + (k % 2 ? -3 : 2) * (1 - k / 18)} 540 820)` } }, 33.35 + k * 0.07);
        tl.set("#gneedle", { attr: { transform: "rotate(-90 540 820)" } }, 31.4);
        show("#chFail", 32.6, 34.62, { x: -20 }); countTo("#failN", 151000, 32.7, 1.8, (v) => Math.round(v).toLocaleString("en-US") + (v > 150999 ? "+" : "")); })();
      // s16-s17: none got in; the locks jam
      tl.fromTo("#rdZero", { opacity: 0, scale: 1.4 }, { opacity: 1, scale: 1, duration: 0.22, ease: "back.out(2)" }, 36.25); tl.to("#rdZero", { opacity: 0, duration: 0.15 }, 37.33);
      shake("s16", 36.27, 10);
      (function () { const C = 2 * Math.PI * 210; $("#lrarc").style.strokeDasharray = C; const m = { v: 0 };
        tl.fromTo("#lockring", { opacity: 0, scale: 0.8, transformOrigin: "540px 640px" }, { opacity: 1, scale: 1, duration: 0.25, ease: E }, 37.5); tl.to("#lockring", { opacity: 0, duration: 0.15 }, 39.1);
        tl.fromTo(m, { v: 0 }, { v: 98, duration: 0.85, ease: "power2.out", immediateRender: false, onUpdate() { $("#lrarc").style.strokeDashoffset = C * (1 - m.v / 100); $("#lrN").textContent = Math.round(m.v) + "%"; } }, 37.6); })();
      shake("s17", 38.45, 18, 7); punch("s17", 38.45, 0.06);
      // s18: the silence: slow push into the robot at the door, the room goes dark
      tl.fromTo(cam("s18"), { scale: 1 }, { scale: 1.12, duration: T1.s18 - T0.s18 + 2 * HND, ease: "none" }, T0.s18 - HND);
      tl.fromTo("#dark", { opacity: 0 }, { opacity: 1, duration: 0.4 }, 39.2); tl.to("#dark", { opacity: 0, duration: 0.2 }, 41.0);
      punch("s19", 43.2, 0.07); flash(43.2, 0.35, 0.5, "#ffb547");
      show("#chSpare", 44.9, 46.58, { x: -20 });
      // s21: ConnectWise's own advisory
      quote("#gx-s21", "● CONNECTWISE TRUST CENTER · ADVISORY", '<div class="qbig">Cloud Backup <span style="color:#6b6e78">(formerly SkyKick)</span> Service Interruption</div><div class="qt" style="font-size:42px;margin-top:22px">“…we identified <span class="qh">unauthorized access to application credentials</span> associated with Cloud Backup”</div>',
        46.7, 47.1, "r2_creds", 930, 960, "#1f6fb2");
      // s22: one key ring threaded to every door; the files copy along the threads
      (function () { const cx = 540, cy = 700, N = 18; const ns = "http://www.w3.org/2000/svg";
        tl.fromTo("#netw", { opacity: 0 }, { opacity: 1, duration: 0.2 }, 48.3); tl.to("#netw", { opacity: 0, duration: 0.15 }, 50.75);
        pop("#ring", 48.3, 50.75); show("#chRing", 48.45, 50.75); show("#chDoorQ", 49.0, 50.75, { x: -20 });
        for (let k = 0; k < N; k++) { const a = (k / N) * Math.PI * 2 - Math.PI / 2; const x = cx + Math.cos(a) * 420, y = cy + Math.sin(a) * 340;
          const h = el("img", "icon3d", `left:${x - 45}px;top:${y - 45}px;width:90px`, $("#netH")); h.src = "assets/3d/house.png";
          tl.fromTo(h, { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)" }, 48.35 + k * 0.03); tl.to(h, { opacity: 0, duration: 0.15 }, 50.75);
          const l = document.createElementNS(ns, "line"); l.setAttribute("x1", cx); l.setAttribute("y1", cy); l.setAttribute("x2", x); l.setAttribute("y2", y); $("#netL").appendChild(l);
          const len = Math.hypot(x - cx, y - cy); l.style.strokeDasharray = len; tl.fromTo(l, { strokeDashoffset: len }, { strokeDashoffset: 0, duration: 0.3, ease: "power2.out" }, 48.5 + k * 0.035);
          const f = el("img", "icon3d", `left:${x - 26}px;top:${y - 26}px;width:52px`, $("#netH")); f.src = "assets/3d/folder.png";
          tl.fromTo(f, { opacity: 0, x: 0, y: 0 }, { opacity: 1, duration: 0.1 }, 49.5 + k * 0.04); tl.to(f, { x: cx - x, y: cy - y, scale: 0.5, duration: 0.6, ease: "power2.in" }, 49.55 + k * 0.04);
          tl.set(f, { opacity: 0 }, 50.2 + k * 0.04); } })();
      punch("s23", 51.42, 0.05);
      // s24: the password box nobody needed
      (function () { tl.fromTo("#login", { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.3, ease: "back.out(1.4)" }, 53.12); tl.to("#login", { opacity: 0, duration: 0.15 }, 54.38);
        textAt("#dots", [[0, ""]].concat(Array.from({ length: 8 }, (_, k) => [53.26 + k * 0.06, "•".repeat(k + 1)])));
        tl.to("#lx", { scaleX: 1, duration: 0.18, ease: "power3.out" }, 53.82); tl.to("#login", { filter: "grayscale(1) brightness(0.8)", duration: 0.2 }, 53.85);
        show("#chTrusted", 53.6, 54.38, { x: -20 }); })();
      punch("s25", 55.45, 0.06); flash(55.45, 0.3, 0.45, "#7ee787");
      show("#chRecon", 57.9, 59.14, { x: -20 }); show("#chCreds", 59.3, 60.22, { x: -20 }); show("#chRoles", 60.4, 62.04, { x: -20 });
      tl.fromTo("#crown", { opacity: 0, y: -300, rotation: -20 }, { opacity: 1, y: 0, rotation: -6, duration: 0.32, ease: "bounce.out" }, 61.0); tl.to("#crown", { opacity: 0, duration: 0.1 }, 62.04);
      // s30: the record scratch: frozen, drained of colour
      tl.fromTo("#still-s30", { filter: "grayscale(0) contrast(1)" }, { filter: "grayscale(1) contrast(1.15)", duration: 0.25 }, 62.1);
      tl.fromTo(cam("s30"), { scale: 1 }, { scale: 1.1, duration: 1.55, ease: "power1.out" }, 62.1);
      show("#chOpen", 67.55, 68.74, { x: -20 });
      // s34: the maker's own words; the code has gone closed since
      (function () { const q = quote("#gx-s34", "● ARTEX'S MAKER, “AUTUMN-27”", '<div class="qt" style="font-size:44px">“ARTEX was originally designed for the purpose of learning and research. It aims to help enterprises and organizations <span class="qh">conduct security risk tests within the scope of authorized assets</span>…”</div>',
          68.84, 69.62, "r3_purpose", 930, 960, "#2f7a52");
        const s = el("div", "stampS", "right:30px;bottom:-78px;transform:rotate(-5deg)", q); s.textContent = "NOW CLOSED SOURCE";
        tl.fromTo(s, { opacity: 0, scale: 2.2 }, { opacity: 1, scale: 1, duration: 0.2, ease: "power4.out" }, 70.45); })();
      // s35: night and day, the same robot
      tl.fromTo(cam("s35"), { scale: 1.06 }, { scale: 1, duration: T1.s35 - T0.s35 + 2 * HND, ease: "none" }, T0.s35 - HND);
      tl.fromTo("#seam", { scaleY: 0 }, { scaleY: 1, duration: 0.35, ease: E }, 71.15);
      show("#chBurglar", 71.57, 74.1, { x: -20 }); show("#chSmith", 72.17, 74.1, { x: 20 });
      // s36: the race to the weak spot
      (function () { ["#laneB", "#laneL"].forEach((s, k) => { tl.fromTo(s, { opacity: 0, x: k ? 80 : -80 }, { opacity: 1, x: 0, duration: 0.25, ease: E }, 74.2 + k * 0.08); tl.to(s, { opacity: 0, duration: 0.15 }, 76.3); });
        tl.fromTo("#finish", { opacity: 0 }, { opacity: 1, duration: 0.2 }, 74.3); tl.to("#finish", { opacity: 0, duration: 0.15 }, 76.3); show("#chWeak", 74.35, 76.3, { x: 20 });
        [["#runB", "#barB", 0.0], ["#runL", "#barL", 0.04]].forEach(([r, b, d]) => { tl.fromTo(r, { x: 0 }, { x: 760, duration: 1.35 - d, ease: "power1.in" }, 74.26 + d);
          tl.fromTo(b, { scaleX: 0 }, { scaleX: 0.98, duration: 1.35 - d, ease: "power1.in" }, 74.26 + d);
          for (let k = 0; k < 12; k++) tl.set(r, { y: k % 2 ? -8 : 0, rotation: k % 2 ? -6 : 6 }, 74.3 + k * 0.11); }); })();
      flash(75.59, 0.7, 0.5, "#ffffff"); punch("s36", 75.59, 0.06);
      // s37: the question to ask
      (function () { tl.fromTo("#phone", { opacity: 0, y: 120 }, { opacity: 1, y: 0, duration: 0.4, ease: "back.out(1.3)" }, 76.4); tl.to("#phone", { opacity: 0, duration: 0.15 }, 79.55);
        tl.fromTo("#finger", { opacity: 0, x: 860, y: 1500 }, { opacity: 1, x: 700, y: 1260, duration: 0.5, ease: E }, 77.1);
        tl.to("#finger", { x: 655, y: 1090, duration: 1.4, ease: "power1.inOut" }, 77.6); tl.to("#finger", { opacity: 0, duration: 0.15 }, 79.55);
        tl.set("#pulse", { left: 531, top: 1028 }, 0);
        tl.fromTo("#pulse", { opacity: 0, scale: 1.3 }, { opacity: 1, scale: 1, duration: 0.3, ease: E }, 78.89); tl.to("#pulse", { opacity: 0, duration: 0.15 }, 79.55);
        tl.to("#pulse", { scale: 1.06, duration: 0.25, yoyo: true, repeat: 1 }, 79.21); })();
      show("#chTip", 79.95, 81.44, { x: -20 });

      // ---------- end card ----------
      tl.fromTo("#end", { opacity: 0 }, { opacity: 1, duration: 0.5 }, 81.52);
      tl.fromTo("#mark", { scale: 0.3, rotation: -20, opacity: 0 }, { scale: 1, rotation: 0, opacity: 1, duration: 0.55, ease: "back.out(2)" }, 81.67);
      tl.fromTo(["#ename", "#ehandle"], { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.45, ease: E, stagger: 0.12 }, 81.92);
      tl.fromTo("#fol", { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(2.2)" }, 82.37);
      tl.to("#fol", { scale: 1.06, duration: 0.45, yoyo: true, repeat: 3, ease: "sine.inOut" }, 82.95);
      tl.to("#mark", { boxShadow: "0 0 140px rgba(200,255,77,0.8)", duration: 0.9, yoyo: true, repeat: 1, ease: "sine.inOut" }, 82.65);

      // ---------- global UI ----------
      tl.fromTo("#prog", { scaleX: 0 }, { scaleX: 1, duration: DUR, ease: "none" }, 0);
      tl.fromTo(["#tag", "#bm"], { opacity: 0, y: -16 }, { opacity: 1, y: 0, duration: 0.4 }, 0.1);
      tl.to(["#tag", "#bm"], { opacity: 0, duration: 0.4 }, 81.3);
      tl.to([".botshade", ".topshade"], { opacity: 0, duration: 0.5 }, 81.52);
      const gp = { f: 0 }; const grainEl = $("#grain");
      tl.fromTo(gp, { f: 0 }, { f: DUR * 24, duration: DUR, ease: "none", onUpdate() { const f = Math.floor(gp.f); grainEl.style.backgroundPosition = `${(f * 137) % 512}px ${(f * 271) % 512}px`; } }, 0);
      tl.fromTo("#black", { opacity: 0 }, { opacity: 1, duration: 0.4, immediateRender: false }, DUR - 0.45);

      // ---------- designed captions ----------
      const CAPLAY = %CAPLAY%, COVERS = %COVERS%;
      const layoutFor = (t) => (CAPLAY.find(([a, b]) => t >= a && t < b) || [0, 0, { m: "S", c: "#c8ff4d" }])[2];
      const covered = (a, b) => COVERS.some(([c0, c1]) => a < c1 && b > c0 - 0.02);
      const capsRoot = $("#caps");
      const fmtNum = (v, target, d) => { const pre = d.match(/^[^\d]*/)[0], suf = d.match(/[^\d]*$/)[0]; const n = Math.round(v); return pre + (target >= 1000 ? n.toLocaleString("en-US") : String(n)) + suf; };
      (window.CAPS || []).forEach((ch) => {
        if (covered(ch.t0, ch.t1)) return;
        const L = layoutFor(ch.t0); const col = L.c;
        const c = document.createElement("div"); c.className = "cap " + L.m; if (ch.w.some((w) => w.emph)) c.setAttribute("data-layout-allow-overlap", ""); capsRoot.appendChild(c);
        const spans = ch.w.map((w) => { const s = document.createElement("span"); const d = w.d;
          const isNum = L.m === "B" && /\d/.test(d); const hero = w.emph && L.m === "A";
          s.className = "cw dim" + (isNum ? " num" : "") + (hero ? " hero" : "") + (w.emph && !hero ? " inl" : "");
          if (hero) { const len = d.replace(/[^A-Z0-9']/gi, "").length; const fs = Math.min(210, Math.round(930 / (len * 0.64)));
            s.style.fontSize = fs + "px"; s.style.transform = "rotate(-3deg)"; s.style.textShadow = `0 0 40px ${rgba(col, 0.55)}, 0 8px 30px rgba(0,0,0,0.5)`; }
          s.textContent = d;
          if (hero) { const bar = document.createElement("span"); bar.className = "bar"; bar.style.width = "96%"; bar.style.background = col; bar.style.boxShadow = `0 0 20px ${col}`; s.appendChild(bar); }
          c.appendChild(s); return { s, w, isNum, hero, d }; });
        tl.fromTo(c, { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.14, ease: "back.out(2)" }, ch.t0);
        tl.set(c, { opacity: 0 }, ch.t1);
        spans.forEach(({ s, w, isNum, hero, d }, k) => {
          const end = k + 1 < spans.length ? spans[k + 1].w.s : ch.t1;
          const keep = w.emph || isNum || hero;
          tl.set(s, { opacity: 1, color: col, scale: hero ? 1 : 1.05 }, w.s);
          tl.set(s, { color: keep ? col : "#ffffff", scale: 1 }, end);
          if (hero) { tl.fromTo(s, { scale: 1.18 }, { scale: 1, duration: 0.22, ease: "power4.out", immediateRender: false }, w.s);
            const bar = s.querySelector(".bar"); if (bar) tl.fromTo(bar, { scaleX: 0 }, { scaleX: 1, duration: 0.3, ease: "power2.out" }, w.s + 0.05); }
          if (isNum) { const target = parseFloat(d.replace(/[^\d.]/g, "")); const m = { v: 0 };
            tl.set(s, { textShadow: `0 0 40px ${rgba(col, 0.6)}, 0 8px 30px rgba(0,0,0,0.5)` }, w.s);
            tl.fromTo(m, { v: 0 }, { v: target, duration: Math.max(0.4, w.e - w.s + 0.2), ease: "power2.out", onUpdate() { s.firstChild.nodeValue = fmtNum(m.v, target, d); } }, w.s);
            s.firstChild.nodeValue = fmtNum(0, target, d); }
        });
      });

      window.__timelines = window.__timelines || {};
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
