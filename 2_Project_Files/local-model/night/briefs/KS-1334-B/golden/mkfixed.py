#!/usr/bin/env python3
# KS-1334 part B: write the fixed adminConfig.ts and ks730c into the WORK dir (not the clone) from the tip text,
# then emit the golden diff with hand-set headers. Reads the tip via `git show` (read verb).
import subprocess, sys
C = "/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/d0b2ec3e-4b50-4d96-87d2-4a998799b9cd/scratchpad/sparkfeed"
W = "/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/d0b2ec3e-4b50-4d96-87d2-4a998799b9cd/scratchpad/feed/ks1334b"
PF = "Blockchain/Dev/services/originate/src/routes/adminConfig.ts"
TF = "Blockchain/Dev/services/originate/src/__tests__/ks730c-adminconfig-500-never-answers-err-message.test.ts"
def show(p): return subprocess.run(["git", "-C", C, "show", "94c9c7aa9be7:" + p], capture_output=True, text=True, check=True).stdout
P = show(PF).split("\n"); T = show(TF).split("\n")
LEAKLINE = "    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message } });"
assert P[2030] == LEAKLINE and P[2157] == LEAKLINE, (P[2030], P[2157])
NEW1 = "    fail500(res, 'Admin config request failed (POST /api/admin/seed-demo-users)', err);"
NEW2 = "    fail500(res, 'Admin config request failed (POST /api/admin/migrate-tenant-data)', err);"
Pn = list(P); Pn[2030] = NEW1; Pn[2157] = NEW2

# test edits
assert T[141] == "      .toEqual({ liveTernaries: 0, helperCalls: 48, distinctContexts: 48 });", T[141]
assert T[170:173] == ["    const KNOWN = [", "      'POST /seed-demo-users', 'POST /migrate-tenant-data',", "    ];"], T[170:173]
assert T[173] == "    let route = '';"
assert T[254] == "  });" and T[255] == "});" and len(T) == 257 and T[256] == "", (T[254:], len(T))
C3NEW = "      .toEqual({ liveTernaries: 0, helperCalls: 50, distinctContexts: 50 });"
KNOWNNEW = "    const KNOWN: string[] = [];"
INS = open(W + "/insert_block.txt").read().rstrip("\n").split("\n")
assert INS[0] == "});" and INS[-1] == "  });"
Tn = T[:141] + [C3NEW] + T[142:170] + [KNOWNNEW] + T[173:255] + INS + T[255:]
open(W + "/adminConfig.B.ts", "w").write("\n".join(Pn))
open(W + "/ks730c.B.ts", "w").write("\n".join(Tn))

# golden, hunks hand-shaped
def h(old_start, old_lines, new_start, new_lines, body):
    return f"@@ -{old_start},{old_lines} +{new_start},{new_lines} @@\n" + "\n".join(body) + "\n"
g = f"--- a/{PF}\n+++ b/{PF}\n"
g += h(2028, 5, 2028, 5, [" " + P[2027], " " + P[2028], " " + P[2029], "-" + P[2030], "+" + NEW1, " " + P[2031]])
g += h(2156, 4, 2156, 4, [" " + P[2155], " " + P[2156], "-" + P[2157], "+" + NEW2, " " + P[2158]])
g += f"--- a/{TF}\n+++ b/{TF}\n"
g += h(141, 3, 141, 3, [" " + T[140], "-" + T[141], "+" + C3NEW, " " + T[142]])
g += h(171, 4, 171, 2, ["-" + T[170], "-" + T[171], "-" + T[172], "+" + KNOWNNEW, " " + T[173]])
g += h(255, 2, 253, 2 + len(INS), [" " + T[254]] + ["+" + l for l in INS] + [" " + T[255]])
open(W + "/KS-1334-B.golden.diff", "w").write(g)
print("insert lines", len(INS), "blank", sum(1 for l in INS if l == ""))
for k, ch in (("backslash", "\\"), ("backtick", "`"), ("dquote", '"'), ("dollar", "$")):
    print(k, sum(l.count(ch) for l in INS + [NEW1, NEW2, C3NEW, KNOWNNEW]))
print("non-ascii", sum(1 for l in INS if any(ord(c) > 127 for c in l)))
