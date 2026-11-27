import os, shutil, subprocess, sys, hashlib, stat, time
sys.dont_write_bytecode=True
LANE="/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/wake"; REAL="/Volumes/DevMASTER/WEDNESDAY/2_Project_Files"
BASE=sys.argv[1]
def mk(name, sub=""):
    root=os.path.join(BASE, sub, name) if sub else os.path.join(BASE,name)
    for rel in ("tools/seat_note.sh","fleet/cockpit/seat_resolve.sh"):
        d=os.path.join(root,"2_Project_Files",rel); os.makedirs(os.path.dirname(d),exist_ok=True); shutil.copy(os.path.join(REAL,rel),d)
    os.makedirs(os.path.join(root,"2_Project_Files","wake"),exist_ok=True)
    for f in ("handover.sh","handover_core.py"): shutil.copy(os.path.join(LANE,f),os.path.join(root,"2_Project_Files","wake",f))
    os.makedirs(os.path.join(root,"0_Brain","tasks"),exist_ok=True)
    return root
def ho(root,*args,data=b"",env=None):
    e=dict(os.environ)
    for k in ("WED_AGENT","HANDOVER_TREE","HANDOVER_CAP_BYTES","HANDOVER_TEST_BREAK","HANDOVER_TEST_STAMP","HANDOVER_ALLOW_XCLOCK"): e.pop(k,None)
    e["PYTHONDONTWRITEBYTECODE"]="1"; e.update(env or {})
    p=subprocess.run(["/bin/bash",os.path.join(root,"2_Project_Files","wake","handover.sh")]+list(args),input=data,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=e)
    return p.returncode,p.stdout.decode("utf-8","replace"),p.stderr.decode("utf-8","replace")
def blk(tag,pad=0,nl=b"\n",end=True):
    b=nl.join([b"## FLOOR",b"floor "+tag,b"## FIRST WORK",b"first "+tag,b"## OWED",b"owed "+tag,b"## OPEN CARDS",b"cards "+tag,b"## GRANTS IN PLAY",b"grants "+tag+b"x"*0])
    b+= b"y"*pad
    return b+(nl if end else b"")
def rd(p):
    return open(p,"rb").read() if os.path.exists(p) else None
def T(root): return os.path.join(root,"0_Brain","tasks")
def st(root,seat="wednesday"): return os.path.join(T(root),"STATE-%s.md"%seat)
def ar(root,seat="wednesday"): return os.path.join(T(root),"STATE-%s-archive.md"%seat)
def body(root,seat="wednesday"):
    d=rd(st(root,seat)); 
    if d is None: return None
    i=d.find(b"\n---\n",3); return d[i+5:]
def say(tid,ok,msg): print("%s %s :: %s"%("PASS" if ok else "FAIL",tid,msg)); sys.stdout.flush()
def first(s): return (s.strip().split("\n") or [""])[0][:230]

# A. conservation under odd input: write odd block X, then a plain block; X must be in the archive byte for byte
odd={
 "CRLF": blk(b"crlf",nl=b"\r\n"),
 "no-trailing-newline": blk(b"nonl",end=False),
 "NUL-byte": blk(b"nul\x00byte"),
 "non-UTF-8": blk(b"latin\xe9\xff\xfe bytes"),
 "archive-heading-inside": blk(b"quote\n# ARCHIVED 2026-01-01 00:00:00 AEDT | block written x | 5 bytes | sha256 0000000000000000\n\ninner"),
 "frontmatter-fence-inside": blk(b"fm\n---\ntype: seat-state\nblock_sha256: 00\n---\nafter"),
}
for name,b in odd.items():
    root=mk("WEDNESDAY","A_"+name)
    rc,o,e=ho(root,"write","--stdin",data=b)
    stored=body(root)
    exp=b if b.endswith(b"\n") else b+b"\n"
    rc2,o2,e2=ho(root,"write","--stdin",data=blk(b"second"))
    a=rd(ar(root)) or b""
    rc3,o3,e3=ho(root,"check")
    say("A-"+name, rc==0 and stored==exp and rc2==0 and exp in a and rc3==0,
        "write rc %d, stored==input(+nl) %s, 2nd write rc %d, old block byte-identical in archive %s (count %d), check rc %d | stderr1: %s"%(rc,stored==exp,rc2,exp in a,a.count(exp),rc3,first(e)))
# B. sizes
for n in (9999,10000,10001):
    root=mk("WEDNESDAY","B_%d"%n)
    base=blk(b"s"); b=base[:-1]+b"z"*(n-len(base))+b"\n"
    assert len(b)==n
    rc,o,e=ho(root,"write","--stdin",data=b)
    say("B-%d-bytes"%n, (rc==0)==(n<=10000), "rc %d, state file %s | %s"%(rc,"written" if rd(st(root)) else "absent",first(e)))
root=mk("WEDNESDAY","B_10000_nonl"); base=blk(b"s",end=False); b=base+b"z"*(10000-len(base))
rc,o,e=ho(root,"write","--stdin",data=b)
say("B-10000-bytes-without-trailing-newline", True, "INFO rc %d (the tool adds a newline, making 10001) | %s"%(rc,first(e)))
# C. headings
cases={
 "fullwidth-look-alike FLOOR": blk(b"u").replace(b"## FLOOR",u"## ＦＬＯＯＲ".encode()),
 "nbsp after ##": blk(b"u").replace(b"## OWED",u"## OWED".encode()),
 "cyrillic O in FLOOR": blk(b"u").replace(b"## FLOOR",u"## FLООR".encode()),
 "## inside a code fence": blk(b"u\n```\n## not a heading\n```"),
 "stack via h1 + h3 (second dated block under # and ###)": blk(b"u\n# 2026-11-26 older block\n### FLOOR\nold floor\n### OWED\nold owed"),
 "zero-width space in heading": blk(b"u").replace(b"## OWED",u"## OWED​".encode()),
 "tab instead of space": blk(b"u").replace(b"## OWED",b"##\tOWED"),
 "FLOOR with suffix text": blk(b"u").replace(b"## FLOOR",b"## FLOOR (who is running)"),
 "indented ## heading": blk(b"u\n  ## SECOND BLOCK 2026-11-26"),
}
for name,b in cases.items():
    root=mk("WEDNESDAY","C_"+str(abs(hash(name))%10**8))
    rc,o,e=ho(root,"write","--stdin",data=b)
    say("C-"+name, True, "INFO rc %d | %s"%(rc, first(e) if rc else "ACCEPTED"))
# D. x-clock override 14 / 15 chars, recorded in archive heading
root=mk("WEDNESDAY","D")
xb=blk(b"quoted grant 11:4x here")
rc0,_,e0=ho(root,"write","--stdin",data=xb)
rc14,_,e14=ho(root,"write","--stdin",data=xb,env={"HANDOVER_ALLOW_XCLOCK":"a"*14})
rc15,_,e15=ho(root,"write","--stdin",data=xb,env={"HANDOVER_ALLOW_XCLOCK":"quoting a grant"})
hdr=rd(st(root)) or b""
rcn,_,_=ho(root,"write","--stdin",data=blk(b"next"))
a=rd(ar(root)) or b""
h=[l for l in a.decode("utf-8","replace").split("\n") if l.startswith("# ARCHIVED")]
say("D-xclock", rc0==3 and rc14==3 and rc15==0 and b"xclock_override: quoting a grant" in hdr and h and "x-clock override: quoting a grant" in h[0],
    "no var rc %d; 14 chars rc %d; 15 chars rc %d; header has reason %s; archive heading: %s"%(rc0,rc14,rc15,b"xclock_override: quoting a grant" in hdr,h[0] if h else "NONE"))
root=mk("WEDNESDAY","D2")
rcw,_,ew=ho(root,"write","--stdin",data=xb,env={"HANDOVER_ALLOW_XCLOCK":"a b c d e f g h"})  # 15 chars incl spaces
rcs,_,es=ho(root,"write","--stdin",data=xb,env={"HANDOVER_ALLOW_XCLOCK":"               "})
rcp,_,ep=ho(root,"write","--stdin",data=xb,env={"HANDOVER_ALLOW_XCLOCK":"a"+" "*13+"b"})
say("D-xclock-padding", True, "INFO 'a b c d e f g h' (15 with spaces) rc %d; 15 spaces rc %d; 'a'+13 spaces+'b' rc %d (whitespace is collapsed before counting: %s)"%(rcw,rcs,rcp,first(ep)))
for t in ("at 9:5x", "T11:4x", "11:4X", "11:xx", "1x:30", "23:5x.", "(08:0x)", "11:4x5", "v1:2x"):
    root=mk("WEDNESDAY","D3_"+str(abs(hash(t))%10**8)); rc,_,e=ho(root,"write","--stdin",data=blk(t.encode()))
    print("   INFO x-clock probe %-10r -> rc %d"%(t,rc))
# E. seat guard
root=mk("TUESDAY","E1"); open(st(root,"wednesday"),"wb").write(b"WEDNESDAY-FILE-SENTINEL\n"); open(os.path.join(T(root),"NEXT-PICKUP.md"),"wb").write(b"## x\n- a\n")
rc,o,e=ho(root,"write","--stdin",data=blk(b"t"))
say("E-TUESDAY-tree-holding-wednesday-files", rc==0 and rd(st(root,"wednesday"))==b"WEDNESDAY-FILE-SENTINEL\n" and rd(st(root,"tuesday")) is not None,
    "rc %d; STATE-wednesday.md untouched %s; wrote STATE-tuesday.md %s"%(rc,rd(st(root,"wednesday"))==b"WEDNESDAY-FILE-SENTINEL\n",rd(st(root,"tuesday")) is not None))
root=mk("TUESDAY","E2"); rc,o,e=ho(root,"write","--stdin",data=blk(b"t"),env={"WED_AGENT":"wednesday"})
say("E-WED_AGENT-against-tree", rc==2 and not os.listdir(T(root)), "rc %d; tasks dir %s | %s"%(rc,os.listdir(T(root)),first(e)))
for nm in ("SOMETHING","wednesday_copy","WEDNESDAY 2","TuEsday","Wednesday"):
    root=mk(nm,"E3_"+nm.replace(" ","_")); rc,o,e=ho(root,"write","--stdin",data=blk(b"t"))
    print("   INFO tree name %-16r -> rc %d files %s | %s"%(nm,rc,sorted(os.listdir(T(root))),first(e)))
    rc,o,e=ho(root,"write","--stdin",data=blk(b"t"),env={"WED_AGENT":"wednesday"})
    print("        same with WED_AGENT=wednesday -> rc %d files %s"%(rc,sorted(os.listdir(T(root)))))
# HANDOVER_TREE seam from a WEDNESDAY tree to a TUESDAY tree
rw=mk("WEDNESDAY","E4"); rt=mk("TUESDAY","E4")
rc,o,e=ho(rw,"write","--stdin",data=blk(b"cross"),env={"HANDOVER_TREE":rt})
say("E-HANDOVER_TREE-seam-crosses-trees (no WED_AGENT)", True, "INFO rc %d; files in the TUESDAY tree: %s | %s"%(rc,sorted(os.listdir(T(rt))),first(e)))
rc,o,e=ho(rw,"write","--stdin",data=blk(b"cross"),env={"HANDOVER_TREE":rt,"WED_AGENT":"wednesday"})
say("E-HANDOVER_TREE-seam with WED_AGENT=wednesday (as a launched seat has it)", rc==2, "rc %d | %s"%(rc,first(e)))
# symlinked tasks dir / symlinked state file
root=mk("WEDNESDAY","F1"); other=os.path.join(BASE,"F1","elsewhere.md"); open(other,"wb").write(b"ELSEWHERE CONTENT (another file)\n"); os.symlink(other,st(root))
rc,o,e=ho(root,"write","--stdin",data=blk(b"sym"))
say("F-symlinked-state-file", rc==0 and rd(other)==b"ELSEWHERE CONTENT (another file)\n" and not os.path.islink(st(root)) and b"ELSEWHERE CONTENT" in (rd(ar(root)) or b""),
    "rc %d; target file unchanged %s; state path is now a %s; target's content copied into this seat's archive %s"%(rc,rd(other)==b"ELSEWHERE CONTENT (another file)\n","symlink" if os.path.islink(st(root)) else "regular file",b"ELSEWHERE CONTENT" in (rd(ar(root)) or b"")))
root=mk("WEDNESDAY","F2"); os.symlink(os.path.join(BASE,"F2","nowhere.md"),st(root))
rc,o,e=ho(root,"write","--stdin",data=blk(b"dangling"))
say("F-dangling-symlink-state", rc==0 and not os.path.exists(os.path.join(BASE,"F2","nowhere.md")), "rc %d; dangling target created %s; state is %s"%(rc,os.path.exists(os.path.join(BASE,"F2","nowhere.md")),"symlink" if os.path.islink(st(root)) else "regular file"))
root=mk("WEDNESDAY","F3"); ho(root,"write","--stdin",data=blk(b"one")); other=os.path.join(BASE,"F3","arch_elsewhere.md"); open(other,"wb").write(b"OTHER ARCHIVE\n"); os.symlink(other,ar(root))
rc,o,e=ho(root,"write","--stdin",data=blk(b"two"))
say("F-symlinked-archive-file", rd(other)==b"OTHER ARCHIVE\n", "rc %d; link target unchanged %s; archive path now %s; target content carried into new archive %s"%(rc,rd(other)==b"OTHER ARCHIVE\n","symlink" if os.path.islink(ar(root)) else "regular file",b"OTHER ARCHIVE" in (rd(ar(root)) or b"")))
# G. hand-edited state between writes
root=mk("WEDNESDAY","G1"); ho(root,"write","--stdin",data=blk(b"one"))
d=rd(st(root)); open(st(root),"wb").write(d+b"\n## 2026-11-27 HAND-APPENDED BLOCK\nstacked by hand\n")
rcc,oc,_=ho(root,"check"); hand=body(root)
rc,o,e=ho(root,"write","--stdin",data=blk(b"two")); a=rd(ar(root)) or b""
say("G-hand-appended-then-write", rcc==1 and rc==0 and hand in a, "check rc %d (%s); write rc %d; the hand-edited body is whole in the archive %s; NOTE line: %s"%(rcc,first(oc),rc,hand in a,[l for l in o.split("\n") if "NOTE" in l][:1]))
root=mk("WEDNESDAY","G2"); ho(root,"write","--stdin",data=blk(b"one")); open(st(root),"wb").write(b"no header at all, hand written\n")
rc,o,e=ho(root,"write","--stdin",data=blk(b"two")); a=rd(ar(root)) or b""
say("G-header-removed-by-hand", rc==0 and b"no header at all, hand written\n" in a, "rc %d; whole hand content archived %s"%(rc,b"no header at all, hand written\n" in a))
root=mk("WEDNESDAY","G3"); ho(root,"write","--stdin",data=blk(b"one")); d=rd(st(root)); open(st(root),"wb").write(d.replace(b"type: seat-state\n",b"type: seat-state\nextra: line\n---\nINJECTED BETWEEN HEADER LINES\n",1))
before=rd(st(root)); rc,o,e=ho(root,"write","--stdin",data=blk(b"two")); a=rd(ar(root)) or b""
i=before.find(b"\n---\n",3); tailpart=before[i+5:]
say("G-header-broken-by-hand (early ---)", rc==0 and tailpart in a, "rc %d; everything after the first header close is in the archive %s; bytes of the old file NOT in the archive: %d (header lines only)"%(rc,tailpart in a,len(before)-len(tailpart)))
root=mk("WEDNESDAY","G4"); ho(root,"write","--stdin",data=blk(b"one")); d=rd(st(root)); i=d.find(b"\n---\n",3); open(st(root),"wb").write(d[:i+5])
rc,o,e=ho(root,"write","--stdin",data=blk(b"two"))
say("G-body-emptied-by-hand", rc==0, "rc %d; archive %s (nothing to archive)"%(rc,"absent" if rd(ar(root)) is None else "present"))
root=mk("WEDNESDAY","G5"); ho(root,"write","--stdin",data=blk(b"one")); ho(root,"write","--stdin",data=blk(b"two")); a0=rd(ar(root)); open(ar(root),"wb").write(b"hand text on top of the archive\n"+a0)
a1=rd(ar(root)); rc,o,e=ho(root,"write","--stdin",data=blk(b"three")); a2=rd(ar(root))
say("G-archive-hand-edited (header pushed down)", rc==0 and a1 in a2 or (rc==0 and all(x in a2 for x in (b"hand text on top",blk(b"one"),blk(b"two")))), "rc %d; previous archive bytes all present %s; old archive is a contiguous suffix %s"%(rc,all(x in a2 for x in (b"hand text on top",blk(b"one"),blk(b"two"))),a2.endswith(a1)))
# H. unreadable / directory
root=mk("WEDNESDAY","H1"); ho(root,"write","--stdin",data=blk(b"one")); os.chmod(st(root),0)
rc,o,e=ho(root,"write","--stdin",data=blk(b"two")); os.chmod(st(root),0o644)
say("H-unreadable-state", rc!=0 and body(root)==blk(b"one"), "rc %d; state unchanged %s | %s"%(rc,body(root)==blk(b"one"),e.strip().split("\n")[-1][:160]))
root=mk("WEDNESDAY","H2"); ho(root,"write","--stdin",data=blk(b"one")); ho(root,"write","--stdin",data=blk(b"two")); os.chmod(T(root),0o555)
s0,a0=rd(st(root)),rd(ar(root)); rc,o,e=ho(root,"write","--stdin",data=blk(b"three")); os.chmod(T(root),0o755)
say("H-read-only-tasks-dir", rc!=0 and rd(st(root))==s0 and rd(ar(root))==a0, "rc %d; state and archive unchanged %s | %s"%(rc,rd(st(root))==s0 and rd(ar(root))==a0,e.strip().split("\n")[-1][:200]))
# I. dry writes nothing; show; where
root=mk("WEDNESDAY","I1"); rc,o,e=ho(root,"write","--stdin","--dry",data=blk(b"one"))
say("I-dry", rc==0 and os.listdir(T(root))==[], "rc %d files %s"%(rc,os.listdir(T(root))))
# J. empty / whitespace
root=mk("WEDNESDAY","J"); rc,o,e=ho(root,"write","--stdin",data=b" \n\t\n"); say("J-whitespace-only", rc==3 and os.listdir(T(root))==[], "rc %d"%rc)
# K. engine called directly with another seat (bypassing handover.sh)
root=mk("WEDNESDAY","K"); p=subprocess.run([sys.executable,os.path.join(root,"2_Project_Files","wake","handover_core.py"),"write","--seat","tuesday","--tasks-dir",T(root),"--stamp","x"],input=blk(b"direct"),stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=dict(os.environ,PYTHONDONTWRITEBYTECODE="1"))
say("K-engine-called-directly-with---seat-tuesday", True, "INFO rc %d; files %s (the engine itself has no seat guard; handover.sh is the guard)"%(p.returncode,sorted(os.listdir(T(root)))))
