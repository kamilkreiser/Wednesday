# Classify every value the leak sweep would count as a hit: is it CRAFTED (appears verbatim in the PR suite, my harness,
# or gate 166/173 case files) or GENERATED (48-hex / openssl shape, nowhere in any source)? Prints counts and shapes only.
import os, re, pathlib, runpy, io, contextlib
W = pathlib.Path("/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate174-ks915-pr1989-r2")
src = (W/"repo/Blockchain/Dev/scripts/__tests__/restore_local_secrets.test.sh").read_text(errors="replace")
for p in (W/"harness").rglob("*"):
    if p.is_file() and p.name not in ("leak_classify.py",): src += p.read_text(errors="replace")
g = {}
with contextlib.redirect_stdout(io.StringIO()):
    g = runpy.run_path(str(W/"harness/leak_sweep.py"))
vals = g["vals"]; hits = {}
for kind, p in g["carriers"]():
    try: data = p.read_bytes().decode("utf-8", "replace")
    except Exception: continue
    for v in vals:
        if v in data: hits.setdefault(v, set()).add(str(p).replace(str(W), "<W>"))
crafted = {v for v in hits if v in src}
gen = {v for v in hits if v not in src}
print(f"distinct values hit: {len(hits)}; crafted (verbatim in suite/harness source): {len(crafted)}; NOT in any source: {len(gen)}")
for v in sorted(gen, key=len):
    print(f"  NOT-IN-SOURCE value: len={len(v)} hex48={bool(re.fullmatch(r'[0-9a-f]{48}', v))} shape={re.sub(r'[A-Za-z]','a',re.sub(r'[0-9]','9',v))[:40] if len(v)<60 else 'long'} carriers={len(hits[v])} e.g. {sorted(hits[v])[0]}")
for v in sorted(crafted, key=len): print(f"  crafted: len={len(v)} carriers={len(hits[v])}")
