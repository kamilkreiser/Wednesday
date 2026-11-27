import re,os,sys,subprocess,shutil
R="/Volumes/DevMASTER/WEDNESDAY"; P=R+"/2_Project_Files/wake/proposed"; SC=sys.argv[1]; os.makedirs(SC,exist_ok=True)
for f in sorted(os.listdir(P)):
    if not re.match(r"0[2-9]_.*\.md$",f): continue
    s=open(os.path.join(P,f),encoding="utf-8").read()
    m=re.search(r"^TARGET: `([^`]+)`",s,re.M); tgt=m.group(1) if m else None
    olds=re.findall(r"```old\n(.*?)\n```",s,re.S); news=re.findall(r"```new\n(.*?)\n```",s,re.S)
    rb=re.findall(r"^ROLLBACK: (.*)$",s,re.M)
    print("== %s -> %s | old blocks %d, new blocks %d, ROLLBACK lines %d"%(f,tgt,len(olds),len(news),len(rb)))
    if not tgt or not os.path.isfile(os.path.join(R,tgt)): print("   TARGET MISSING"); continue
    t=open(os.path.join(R,tgt),encoding="utf-8").read(); t2=t
    for i,o in enumerate(olds):
        n=t.count(o); print("   old #%d (%d chars, starts %r): found %d time(s) in the target%s"%(i+1,len(o),o[:50],n,"" if n==1 else "   <-- NOT EXACTLY ONCE"))
        if n==1 and i<len(news): t2=t2.replace(o,news[i])
    if not olds and news:
        t2=t.rstrip("\n")+"\n"+news[0]+"\n"; print("   append-only proposal; target currently contains its first new line %d time(s)"%t.count(news[0].split("\n")[1] if "\n" in news[0] else news[0]))
    out=os.path.join(SC,f.replace(".md","")+"__"+os.path.basename(tgt)); open(out,"w",encoding="utf-8").write(t2)
    if tgt.endswith(".sh") or tgt.endswith(".command"):
        p=subprocess.run(["/bin/bash","-n",out],stdout=subprocess.PIPE,stderr=subprocess.STDOUT); print("   bash -n on the scratch copy with the replacement applied: rc %d %s"%(p.returncode,p.stdout.decode()[:200]))
