#!/usr/bin/env python3
"""Shadow-gate deterministic half for the Blockchain monorepo (TS vitest + bash tests). No LLM.
usage: shadow_facts.py WT SRC PR HEAD BASE_REF OUT [--suite] [--tests REL...] [--node-modules DIR]
  Test files = --tests (repo-relative, explicit) or, absent that, changed files matching test patterns.
  *.sh -> `/bin/bash <file>`; *.test.ts/tsx -> `npx vitest run <file>` (jest if the package has jest.config.js).
  Counts: bash suites print "N passed, M failed[, K skipped]" (last such line wins); vitest/jest "Tests ... N passed".
  rc is authoritative: a non-zero rc is a failure even if a count line says 0 failed; rc 0 with no readable count sets count_unparsed.
  This is THE non-pytest harness: spark_gate.sh calls it (2026-10-26) rather than carrying a second one.
  --node-modules DIR: symlink DIR as node_modules into each vitest package dir of the worktree (a fresh worktree has none)."""
import sys, os, re, json, subprocess, time
wt, src, pr, head, bref, out = sys.argv[1:7]; suite = "--suite" in sys.argv
def _opt(flag):
    a = sys.argv[7:]
    if flag not in a: return []
    r = []
    for x in a[a.index(flag)+1:]:
        if x.startswith("--"): break
        r.append(x)
    return r
explicit_tests = _opt("--tests"); nm = (_opt("--node-modules") or [None])[0]
os.makedirs(out, exist_ok=True)
def sh(cmd, cwd=None, t=900):
    p = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, timeout=t); return p.returncode, (p.stdout + p.stderr)
g = lambda *a: subprocess.run(["git", "-C", wt, *a], capture_output=True, text=True).stdout
T0 = time.time()
tip = subprocess.run(["git","-C",src,"ls-remote","origin",f"refs/pull/{pr}/head"],capture_output=True,text=True).stdout.split()[0]
mb = g("merge-base", head, f"origin/{bref}").strip()
ns = [l.split("\t") for l in g("diff","--name-status",mb,head).splitlines()]
nu = {l.split("\t")[2]:l.split("\t")[:2] for l in g("diff","--numstat",mb,head).splitlines()}
open(f"{out}/diff.patch","w").write(g("diff",mb,head))
touched=[{"status":s[0],"path":s[-1],"added":nu.get(s[-1],["?","?"])[0],"deleted":nu.get(s[-1],["?","?"])[1]} for s in ns]
is_test=lambda p: bool(re.search(r"(__tests__/|\.test\.(ts|tsx|sh)$|/tests?/)",p))
tests=explicit_tests or [t["path"] for t in touched if is_test(t["path"]) and t["status"][0]!="D"]
prod=[t for t in touched if t["path"] not in tests and not is_test(t["path"])]
def pkgdir(p):
    d=os.path.dirname(p)
    while d and not os.path.exists(f"{wt}/{d}/package.json"): d=os.path.dirname(d)
    return d
def run_test(t, label):
    if t.endswith(".sh"): cmd=f"/bin/bash {wt}/{t}"; cwd=wt
    else:
        pk=pkgdir(t)
        if nm and not os.path.exists(f"{wt}/{pk}/node_modules"): os.symlink(nm, f"{wt}/{pk}/node_modules")
        cmd=(f"npx jest {os.path.relpath(t,pk)}" if os.path.exists(f"{wt}/{pk}/jest.config.js") else f"npx vitest run {os.path.relpath(t,pk)} --reporter=default"); cwd=f"{wt}/{pk}"
    rc,o=sh(cmd,cwd); open(f"{out}/{label}.log","a").write(f"\n##### {t}\n{o}")
    if t.endswith(".sh"):
        bm=re.findall(r"(\d+) passed,?\s+(\d+) failed(?:,?\s+(\d+) skipped)?",o)
        p_,f_=(int(bm[-1][0]),int(bm[-1][1])) if bm else (None,None)
    else:
        m=re.search(r"Tests:?\s+(?:(\d+) failed,?\s*\|?\s*)?(?:\d+ skipped,?\s*)?(\d+) passed",o); f=re.search(r"Tests:?\s+(\d+) failed",o)
        p_=int(m.group(2)) if m else (0 if f else None); f_=int(f.group(1)) if f else None
    return {"file":t,"rc":rc,"ok":rc==0 and not f_,"passed":p_,"failed":f_ if f_ is not None else (0 if rc==0 else None),"count_unparsed":rc==0 and p_ is None,"tail":o.strip()[-300:]}
def checkout(ref):
    sh(f"git -C {wt} checkout -q --detach {ref} && git -C {wt} reset -q --hard && git -C {wt} clean -fdq -e node_modules",None)
    if os.path.exists(f"{wt}/Blockchain/Dev/packages/shared/package.json") and os.path.exists(f"{wt}/Blockchain/Dev/packages/shared/node_modules"): sh("npx tsc",f"{wt}/Blockchain/Dev/packages/shared")
checkout(head)
for l in ("targeted_head","targeted_base"): open(f"{out}/{l}.log","w").close()
th=[run_test(t,"targeted_head") for t in tests]
# base product + head tests
checkout(head)
for t in prod:
    p=t["path"]
    if t["status"][0]=="A": sh(f"rm -f '{wt}/{p}'")
    elif t["status"][0]=="R": pass
    else: sh(f"git -C {wt} checkout {mb} -- '{p}'")
if os.path.exists(f"{wt}/Blockchain/Dev/packages/shared/node_modules"): sh('npx tsc',f'{wt}/Blockchain/Dev/packages/shared')
tb=[run_test(t,"targeted_base") for t in tests]
tot=lambda rs:{"files":len(rs),"files_ok":sum(1 for r in rs if r["ok"]),"files_failed":sum(1 for r in rs if not r["ok"]),"passed":sum(r["passed"] or 0 for r in rs),"failed":sum(r["failed"] or 0 for r in rs),"count_unparsed_files":[r["file"] for r in rs if r["count_unparsed"]]}
res={"pr":int(pr),"head_sha":head,"pr_tip_now":tip,"head_mode":"tip" if tip==head else "STALE","merge_base":mb,"base_ref":bref,
 "touched_files":touched,"test_files":tests,"product_files":[t["path"] for t in prod],
 "diff_stat":{"files":len(touched),"added":sum(int(v[0]) for v in nu.values() if v[0].isdigit()),"deleted":sum(int(v[1]) for v in nu.values() if v[1].isdigit())},
 "targeted_on_head":th,"targeted_on_base_product_code":tb,"targeted_head_totals":tot(th),"targeted_base_totals":tot(tb),
 "not_run":["live/integration runs","security scan","network or deployed service"]}
if suite:
    pks=sorted({pkgdir(t["path"]) for t in touched if t["path"].endswith((".ts",".tsx")) and pkgdir(t["path"])})
    def suite_run(label):
        r={}
        for pk in pks:
            rc,o=sh("npx jest" if os.path.exists(f"{wt}/{pk}/jest.config.js") else "npx vitest run --reporter=default",f"{wt}/{pk}",1500); open(f"{out}/suite_{label}.log","a").write(f"\n##### {pk}\n{o}")
            m=re.search(r"Tests:?\s+(?:(\d+) failed,?\s*\|?\s*)?(?:\d+ skipped,?\s*)?(\d+) passed",o); f=re.search(r"Tests:?\s+(\d+) failed",o)
            r[pk]={"rc":rc,"passed":int(m.group(2)) if m else None,"failed":int(f.group(1)) if f else None}
        return r
    open(f"{out}/suite_head.log","w").close(); open(f"{out}/suite_base.log","w").close()
    checkout(head); res["suite_after_head"]=suite_run("head")
    checkout(mb); res["suite_before_base"]=suite_run("base")
checkout(head)
res["gate_seconds"]=int(time.time()-T0)
json.dump(res,open(f"{out}/facts.json","w"),indent=1)
print(json.dumps({k:res[k] for k in res if k not in("touched_files",)},indent=1)[:3500])
