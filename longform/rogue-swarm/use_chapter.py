import json,sys
k=int(sys.argv[1]); ch=json.load(open("work/chapters.json")); dur=[c for c in ch if c["ch"]==k][0]["dur"]
TPL=open("work/_tpl.html").read()
open("index.html","w").write(TPL.replace("{KK}",f"{k:02d}").replace("{DUR}",f"{dur:.3f}"))
print(f"index.html = chapter {k} ({dur:.2f}s)")
