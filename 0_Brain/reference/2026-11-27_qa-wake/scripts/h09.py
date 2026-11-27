import os,sys,re
D=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,D)
src=open(os.path.join(D,"harness.py")).read(); src=src[:src.index('ORIG=os.path.join(D,"orig.command")')]
exec(src)
old="   never hardcode it: `bash 2_Project_Files/tools/note_entry.sh --where` prints today's"; new="   never hardcode it: \\`bash 2_Project_Files/tools/note_entry.sh --where\\` prints today's"
for base in ("orig","patched"):
    s=open(os.path.join(D,base+".command"),encoding="utf-8").read(); assert s.count(old)==1
    open(os.path.join(D,base+"_p09.command"),"w",encoding="utf-8").write(s.replace(old,new))
SUMMARY="x  bytes: 1  ~tokens: 1 of 60000"
for seat in ("tuesday","friday","wednesday"):
    _,_,_,p0,_,_=harness(os.path.join(D,"orig.command"),seat,0,SUMMARY,True)
    rc,o,e,p9,_,_=harness(os.path.join(D,"orig_p09.command"),seat,0,SUMMARY,True)
    rc2,o2,e2,p19,_,_=harness(os.path.join(D,"patched_p09.command"),seat,0,SUMMARY,True)
    a=p0.decode().split("\n"); b=p9.decode().split("\n"); d=[i for i,(x,y) in enumerate(zip(a,b)) if x!=y]
    print("%s: proposal 9 alone: rc %d; lines changed vs today's prompt: %d (same line count %s); stub note_entry ran: today %s / with 9 %s; literal command now in the prompt: %s | 9 + 1 together: rc %d, %s"%(
        seat,rc,len(d),len(a)==len(b),b"STUB-NOTE-ENTRY-WHERE" in p0,b"STUB-NOTE-ENTRY-WHERE" in p9,b"`bash 2_Project_Files/tools/note_entry.sh --where`" in p9,rc2,
        ("identical to 9 alone (seat untouched by proposal 1)" if p19==p9 else ("wake-pack prompt, tail carries the literal command: %s"%(b"`bash 2_Project_Files/tools/note_entry.sh --where`" in p19)))))
