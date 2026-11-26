import sys, re, difflib, subprocess
W="/private/tmp/claude-501/qan2/"
LB="/Volumes/Laptop-DEV/FRIDAY/2_Project_Files/friday/briefs_drafts/2026-11-26_coagent_AUDIT-NEXT-A_brief.md"
CL="/Volumes/Laptop-DEV/!CODING/Claude to Claude/coagent/1_Project_Definition/CLARIFICATIONS.md"
rd=lambda p: open(p, encoding="utf-8").read()
q="No: end the session and pair again"
lb=rd(LB).splitlines(); cl=rd(CL).splitlines()
print("lane brief lines:",len(lb)," line154 has quote:", q in lb[153]); print("  L154:", lb[153][:400])
print("CLARIFICATIONS line176 has quote:", q in cl[175]); print("  L176:", cl[175][:400])
for i,l in enumerate(lb,1):
    if q in l: print("  brief hit line",i)
for i,l in enumerate(cl,1):
    if q in l: print("  clar hit line",i)
# context of the quote in each source (what the round's quote leaves out)
for name,l in (("brief",lb[153]),("clar",cl[175])):
    k=l.find(q); print(f"  {name} 20 chars before quote: {l[max(0,k-20):k]!r} after: {l[k+len(q):k+len(q)+20]!r}")
for f in ("e_m2.txt","e_msg.txt"):
    t=rd(W+f); print(f, "contains quote with quotes:", ("'"+q+"'") in t, " count:", t.count(q))
# removed lines
def removed(a,b):
    out=[]
    for tag,i1,i2,j1,j2 in difflib.SequenceMatcher(None,a,b,autojunk=False).get_opcodes():
        if tag in ("replace","delete"): out+=a[i1:i2]
    return out
def subseq(base,head):
    j=0
    for l in head:
        if j<len(base) and l==base[j]: j+=1
    return j
for nm,(f0,f1,f2) in {"BACKLOG":("e_b0.txt","e_b1.txt","e_b2.txt"),"M0":("e_m0.txt","e_m1.txt","e_m2.txt")}.items():
    a0=rd(W+f0).splitlines(); a1=rd(W+f1).splitlines(); a2=rd(W+f2).splitlines()
    r=removed(a1,a2); s0=set(a0); s1=a1
    print(f"{nm}: removed d79ae1c->head {len(r)}; in d79ae1c {sum(1 for x in r if x in s1)}; in base {sum(1 for x in r if x in s0)}")
    print(f"{nm}: removed base->head {len(removed(a0,a2))}; base lines kept in order {subseq(a0,a2)} of {len(a0)}; base a byte prefix of head: {rd(W+f2).startswith(rd(W+f0))}")
# word-level paragraph comparison
m1=rd(W+"e_m1.txt").splitlines(); m2=rd(W+"e_m2.txt").splitlines()
p1=" ".join(m1[254:263]); p2=" ".join(m2[254:267])
print("old para first/last:", m1[254][:50], "|", m1[262][-40:]); print("new para first/last:", m2[254][:50], "|", m2[266][-40:])
w1=p1.split(); w2=p2.split(); print("words old",len(w1),"new",len(w2))
for tag,i1,i2,j1,j2 in difflib.SequenceMatcher(None,w1,w2,autojunk=False).get_opcodes():
    if tag!="equal": print(f"  {tag}: OLD[{i1}:{i2}] {' '.join(w1[i1:i2])!r}\n        NEW[{j1}:{j2}] {' '.join(w2[j1:j2])!r}")
print("line after old para:", repr(m1[263][:60]), " after new:", repr(m2[267][:60]))
