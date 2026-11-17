import os,sys
S=sys.argv[1]
src=open(S+"/drivers/mutate_r2.py").read()
ns={}
start=src.index("R1 = [")
end=src.index("TESTS = [")
exec("L='crates/coagent-roster/src/lib.rs'\nI='crates/coagent-roster/src/intake.rs'\nP='crates/coagent-roster/src/proposal.rs'\n"+src[start:end],ns)
for mid,f,old,new,what in ns["R1"]+ns["N"]:
    c=open(os.path.join(S,"mut",f)).read().count(old)
    if c!=1: print(mid,"count",c)
print("total",len(ns["R1"]),len(ns["N"]))
