import sys, re, collections
sec=None; agg=collections.OrderedDict()
for line in open(sys.argv[1], errors="replace"):
    m=re.match(r".*QAHF (exhaustive|persistent|generated):", line)
    if line.startswith("QAHF CLASS"):
        parts=line.strip()[len("QAHF CLASS "):].split(" | ")
        kind=parts[0]; cls=parts[1]; n=int(parts[-1].lstrip("x"))
        f=cls.split("|")
        if len(f)==5: ops,ans,mem,fl,rt=f
        else: ops="(random)"; ans,mem,fl,rt=f[-4:]
        # where failed: first failed op kind classes
        where=sorted(set(o.split("/")[0].replace(":"," ") for o in ops.split("+"))) if ops not in ("", "(random)") else [ops or "none hit"]
        key=(kind,ans,mem,fl,rt)
        e=agg.setdefault(key,[0,collections.Counter()]); e[0]+=n; e[1][" + ".join(where)]+=n
for (kind,ans,mem,fl,rt),(n,w) in agg.items():
    ex="; ".join(f"{k} x{v}" for k,v in w.most_common(4))
    print(f"| {kind} | {ex} | {ans} | {mem} | {fl} | {rt} | {n} |")
