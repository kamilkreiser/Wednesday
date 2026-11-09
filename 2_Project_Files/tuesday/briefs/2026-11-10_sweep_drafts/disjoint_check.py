# Disjointness proof: every path of the code repo at fa401da9 (1491 blobs) plus one synthetic NEW file in every existing
# directory is tested against each lane's include/exclude globs; a path owned by two lanes fails the run.
# Usage: python3 -I disjoint_check.py <paths.txt>
import re, sys, itertools
def rx(g):
    out, i = "", 0
    while i < len(g):
        if g.startswith("**/", i): out += "(?:.*/)?"; i += 3
        elif g.startswith("**", i): out += ".*"; i += 2
        elif g[i] == "*": out += "[^/]*"; i += 1
        elif g[i] == "?": out += "[^/]"; i += 1
        else: out += re.escape(g[i]); i += 1
    return re.compile("^" + out + "$")
LANES = {
 "L1-web-ui": (["web/src/components/**","web/src/app/**","web/src/content/**","web/src/server/mock/**","web/src/styles/**","web/src/assets/**","web/e2e/shell-sidebar.spec.ts","web/e2e/playbook-feedback-pill.spec.ts"],
               ["web/src/server/mock/customer-name.test.ts"]),
 "L2-web-core": (["web/src/server/**","web/src/api/**","web/src/lib/**","web/src/data/**","web/src/design/**","web/src/instrumentation.ts","web/src/proxy*.ts","web/src/proxy*.tsx"],
                 ["web/src/server/mock/**"]),
 "L3-api": (["api/**"], ["api/tests/HpsmPoc.Api.Tests/Assessment/Hpsmpoc178CustomerNameTests.cs"]),
 "L4-ci-tooling": ([".github/**","infra/**","scripts/**","web/scripts/**","web/e2e/**","web/src/e2e-runner*.test.ts","web/src/audit-dev.test.ts","web/src/standalone.test.ts","web/src/web-settings.test.ts","web/src/productName.test.tsx",
                    "api/tests/HpsmPoc.Api.Tests/Assessment/Hpsmpoc178CustomerNameTests.cs","web/src/server/mock/customer-name.test.ts"],
                   ["web/e2e/shell-sidebar.spec.ts","web/e2e/playbook-feedback-pill.spec.ts"]),
}
ANALYSIS = {  # a different tree (the analysis repo under 1_Project_Definition); disjoint from the code repo by root, and from each other by path
 "L5-docs": ["1_Project_Definition/Governance/stage-gates/**","1_Project_Definition/Deliverables/**","1_Project_Definition/Architecture/2026-11-10_*","1_Project_Definition/Demo/**"],
 "L6-records": ["1_Project_Definition/CLARIFICATIONS.md","1_Project_Definition/Briefs/2026-11-09_B1387_STATUS.md","JIRA:HPSMPOC (comments/transitions only)"],
}
paths = [l.strip() for l in open(sys.argv[1]) if l.strip()]
dirs = sorted({p.rsplit("/",1)[0] for p in paths if "/" in p})
probe = [d + "/__new_file__.x" for d in dirs] + ["__new_root__.x"]
comp = {k: ([rx(g) for g in inc], [rx(g) for g in exc]) for k,(inc,exc) in LANES.items()}
def owners(p): return [k for k,(inc,exc) in comp.items() if any(r.match(p) for r in inc) and not any(r.match(p) for r in exc)]
bad, unowned, per = [], 0, {k:0 for k in LANES}
for p in paths + probe:
    o = owners(p)
    for k in o: per[k]+=1
    if len(o) > 1: bad.append((p,o))
    if not o: unowned += 1
print("paths tested:", len(paths), "+ probes:", len(probe))
print("owned per lane (tracked paths + probes):", per)
print("unowned (allowed; nobody may touch):", unowned)
print("OVERLAPS:", len(bad)); [print("  ",b) for b in bad[:20]]
# control that can fail: a deliberately overlapping lane must be caught
comp["CONTROL"] = ([rx("web/src/lib/**")], [])
c = [p for p in paths if len(owners(p)) > 1]
print("control (web/src/lib/** added as a second owner) overlaps found:", len(c), "->", "control fires" if c else "CONTROL DID NOT FIRE")
pairs = [(a,b) for a,b in itertools.combinations(ANALYSIS,2)]
print("analysis-tree lanes:", list(ANALYSIS), "- records owns single files, docs owns directories; no shared path:",
      not any(rx(g).match(f) for g in ANALYSIS["L5-docs"] for f in ["1_Project_Definition/CLARIFICATIONS.md","1_Project_Definition/Briefs/2026-11-09_B1387_STATUS.md"]))
sys.exit(1 if bad or not c else 0)
