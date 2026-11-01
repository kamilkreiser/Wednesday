#!/usr/bin/env python3
# Gate 72 mutants. Applies one textual mutation to a product file, runs the 2 targeted test files, restores via git checkout.
import subprocess, sys, re
G = "/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate72-ks1868-shared-1887"
R = G + "/repo"
P = R + "/Blockchain/Dev/packages/shared/"
GS = P + "src/utils/gracefulShutdown.ts"
RC = P + "src/cache/response-cache.ts"
T = ["src/__tests__/ks1868-unhandled-rejection-handler-unreadable-reason.test.ts",
     "src/__tests__/ks1868-response-cache-read-unreadable-throw.test.ts"]
M = [
 ("M1 listener fallback text changed", GS, "detail = 'unreadable thrown value';", "detail = 'x';"),
 ("M2 listener catch rethrows", GS, "detail = 'unreadable thrown value';", "throw new Error('rethrow');"),
 ("M3 listener survive branch inverted", GS, "ctx.mode === 'survive'", "ctx.mode !== 'survive'"),
 ("M4 listener stack dropped for readable Error", GS, "${reason.message}\\n${reason.stack ?? ''}", "${reason.message}\\n"),
 ("M5 listener fallback calls String(reason) (re-reads the unreadable value)", GS, "detail = 'unreadable thrown value';", "detail = String(reason);"),
 ("M6 cache fallback emptied", RC, "reason = 'unreadable thrown value';", "reason = '';"),
 ("M7 cache catch rethrows", RC, "reason = 'unreadable thrown value';", "throw new Error('rethrow');"),
 ("M8 cache log key renamed", RC, "{ error: reason }", "{ err: reason }"),
 ("M9 cache inner try removed (guard collapsed)", RC, "      try {\n        reason = error instanceof Error ? error.message : String(error);\n      } catch {\n        reason = 'unreadable thrown value';\n      }\n", "      reason = error instanceof Error ? error.message : String(error);\n"),
 ("M10 cache readable-path: String(error) for Errors", RC, "error instanceof Error ? error.message : String(error);", "String(error);"),
]
for name, f, old, new in M:
    s = open(f).read()
    if s.count(old) != 1:
        print(f"{name}: SKIP pattern count {s.count(old)}"); continue
    open(f, "w").write(s.replace(old, new))
    log = f"{G}/logs/mutant_{name.split()[0]}.log"
    r = subprocess.run(["bash", G + "/scripts/vt.sh", log] + T)
    out = open(log).read()
    m = re.search(r"Tests\s+(.*)", out)
    print(f"{name}: rc={r.returncode} {'KILLED' if r.returncode else 'SURVIVED'} | {m.group(1) if m else '?'}", flush=True)
    subprocess.run(["git", "-C", R, "checkout", "2d1a2265", "--", f.replace(R + "/", "")], check=True)
print(subprocess.run(["git", "-C", R, "status", "--short"], capture_output=True, text=True).stdout or "status clean")
