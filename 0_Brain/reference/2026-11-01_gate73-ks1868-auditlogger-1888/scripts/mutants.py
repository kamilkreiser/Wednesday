#!/usr/bin/env python3
# Gate 73: red-first at base + mutants on AuditLogger.flush catch.
# Each variant is applied to the product file in the working tree (never under src/__tests__),
# then the author's test file (A) and the gate probe (P) are run; the product file is restored
# from the saved original bytes and a whole-file sha256 check must match before the next variant.
import hashlib, re, subprocess, sys

G = "/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate73-ks1868-auditlogger-1888"
R = G + "/repo"
F = R + "/Blockchain/Dev/packages/shared/src/security/audit-logger.ts"
T = "src/__tests__/ks1868-audit-logger-flush-unreadable-throw.test.ts"

top = subprocess.run(["git", "-C", R, "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
assert top == R, top
ORIG = open(F, "rb").read()
SHA = hashlib.sha256(ORIG).hexdigest()
HEAD_BLOB = subprocess.run(["git", "-C", R, "show", "refs/gate/head:Blockchain/Dev/packages/shared/src/security/audit-logger.ts"], capture_output=True).stdout
assert hashlib.sha256(HEAD_BLOB).hexdigest() == SHA, "working file != head blob before start"
BASE_BLOB = subprocess.run(["git", "-C", R, "show", "refs/gate/base:Blockchain/Dev/packages/shared/src/security/audit-logger.ts"], capture_output=True).stdout
print(f"head sha256={SHA}\nbase sha256={hashlib.sha256(BASE_BLOB).hexdigest()}", flush=True)

UNSHIFT = "        this.eventBuffer.unshift(event);\n"
INNER = ("        let reason: string;\n        try {\n          reason = error instanceof Error ? error.message : String(error);\n"
         "        } catch {\n          reason = 'unreadable thrown value';\n        }\n")
LOGL = "        logger.error('Failed to process audit event', { error: reason });\n"
REBUF = "        // Re-add to buffer for retry\n" + UNSHIFT

V = [
 ("BASE", "base product file (red-first)", None, None),
 ("AM", "author's mutant: delete the unshift line", UNSHIFT, ""),
 ("M1", "unshift -> push", UNSHIFT, "        this.eventBuffer.push(event);\n"),
 ("M2", "drop the inner try (unguarded read, base shape with reason var)", INNER,
        "        const reason: string = error instanceof Error ? error.message : String(error);\n"),
 ("M3", "inner catch rethrows", "          reason = 'unreadable thrown value';\n", "          throw new Error('rethrow');\n"),
 ("M4", "double re-buffer", UNSHIFT, UNSHIFT + UNSHIFT),
 ("M5", "fallback text changed", "reason = 'unreadable thrown value';", "reason = 'unreadable';"),
 ("M6", "re-buffer only on the unreadable path (readable Error loses its retry)",
        "          reason = 'unreadable thrown value';\n        }\n", "          reason = 'unreadable thrown value';\n          this.eventBuffer.unshift(event);\n        }\n"),
 ("M7", "re-buffer skipped on the unreadable path", REBUF,
        "        // Re-add to buffer for retry\n        if (reason !== 'unreadable thrown value') this.eventBuffer.unshift(event);\n"),
 ("M8", "log key renamed error -> err", "{ error: reason }", "{ err: reason }"),
 ("M9", "logger.error removed", LOGL, ""),
 ("M10", "inner fallback re-reads String(error)", "reason = 'unreadable thrown value';", "reason = String(error);"),
 ("M11", "re-buffer moved before the log line (expected equivalent)", INNER + LOGL + REBUF, INNER + UNSHIFT + LOGL),
 ("M12", "flush loop breaks after the first failure (rest of batch dropped)", REBUF, REBUF + "        break;\n"),
 ("M13", "readable path logs String(error) for Errors", "error instanceof Error ? error.message : String(error);", "String(error);"),
]

def run(tag):
    out = {}
    for kind, script, args in (("A", "vt.sh", [T, "--reporter=verbose"]), ("P", "vp.sh", ["--reporter=verbose", "--silent=false"])):
        log = f"{G}/logs/mut_{tag}_{kind}.log"
        r = subprocess.run(["bash", f"{G}/scripts/{script}", log] + args)
        s = open(log).read()
        m = re.search(r"Tests\s+(.*)", s)
        out[kind] = (r.returncode, m.group(1).strip() if m else "?(no Tests line: see log)")
    return out

for tag, desc, old, new in V:
    if tag == "BASE":
        mut = BASE_BLOB
    else:
        s = ORIG.decode()
        n = s.count(old)
        if n != 1:
            print(f"{tag}: SKIP anchor count {n}", flush=True); continue
        mut = s.replace(old, new).encode()
    open(F, "wb").write(mut)
    o = run(tag)
    open(F, "wb").write(ORIG)
    ok = hashlib.sha256(open(F, "rb").read()).hexdigest() == SHA
    a = "KILLED" if o["A"][0] else "SURVIVED"
    p = "KILLED" if o["P"][0] else "SURVIVED"
    print(f"{tag} | {desc} | author cells: {a} ({o['A'][1]}) | gate probe: {p} ({o['P'][1]}) | restored sha256 ok={ok}", flush=True)
    if not ok:
        sys.exit("RESTORE FAILED")
print(subprocess.run(["git", "-C", R, "status", "--short"], capture_output=True, text=True).stdout or "git status clean")
