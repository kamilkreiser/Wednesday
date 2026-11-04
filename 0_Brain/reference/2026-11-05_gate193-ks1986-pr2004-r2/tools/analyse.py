# Gate 193: per-version facts for Q2/Q3(e)(f)/Q4 from the PG runs. usage: python3 -I analyse.py
# Prints, for chosen cells: chainCalls, leaks, http, probes, a body digest; and checks the not-found body byte-equality:
# every v1 row whose body carries checks.documentExists === false is compared, per path, with the REFERENCE not-found body
# taken from a DIFFERENT source: the 577f run's S-LOOKUP-FAILURE-REGISTRY row (chain down, the pre-existing not-found branch).
import json, hashlib, sys
W = "/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate193-ks1986-pr2004-r2"
def load(v):
    return {(r["cell"], r["path"]): r for r in map(json.loads, open(f"{W}/runs/pg_{v}.jsonl"))}
V = {v: load(v) for v in ("base", "r1", "head")}
dig = lambda b: hashlib.sha256(json.dumps(b, sort_keys=True).encode()).hexdigest()[:12]
ref = {p: V["r1"][("S-LOOKUP-FAILURE-REGISTRY", p)]["body"] for p in ("/verify", "verify-file")}
print("REFERENCE not-found bodies (577f, S-LOOKUP-FAILURE-REGISTRY, chain down):")
for p, b in ref.items(): print(" ", p, dig(b), json.dumps(b)[:200])
cells = sys.argv[1:] or sorted({c for (c, p) in V["head"] if p != "v2"})
for c in cells:
    for p in ("/verify", "verify-file"):
        line = [f"{c:52s} {p:11s}"]
        for v in ("base", "r1", "head"):
            r = V[v].get((c, p))
            if r is None: line.append(f"{v}:-"); continue
            b = r["body"]
            cert = (b.get("certification") or {}).get("certificationId") if isinstance(b.get("certification"), dict) else None
            nf = "NF=" + ("REF" if b == ref[p] else "DIFF") if (b.get("checks") or {}).get("documentExists") is False else ""
            line.append(f"{v}: http={r['http']} chain={r['chainCalls']} cert={cert} leaks={len(r['leaks'])} {nf} warn={r['warnKS1986']} err={r['errors']}")
        print(" | ".join(line))
