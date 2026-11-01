#!/usr/bin/env python3
"""Delta mutants on wt_delta: re-introduce the string value into the log (gate 82 M3/M18 equivalents + extras). Restores by sha256."""
import hashlib, subprocess, re
W = "/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate82d-ks1901-mcp-1897-delta"
M = W + "/wt_delta/Blockchain/Dev/services/mcp-server/src"
HTTP, HASH = M + "/http-server.ts", M + "/tools/hash.ts"
TESTS = ["src/__tests__/" + t for t in [
 "ks1901-mcp-http-batch-items-never-echo-the-thrown-text.test.ts", "ks1893-hash-tool-never-returns-the-fs-error-text.test.ts",
 "ks1410-mcp-http-500-part-a-never-echoes-the-thrown-text.test.ts", "ks1410-mcp-http-500-part-b-never-echoes-the-thrown-text.test.ts",
 "ks1868-hash-tool-unreadable-throw.test.ts"]]
H_A = "    if (err instanceof Error) return err.message;\n"
K_A = "          if (err instanceof Error) logged = err.message;\n"
MUT = [
 ("M23d_http_number_value_in_log", HTTP, "return `non-Error ${err === null ? 'null' : typeof err} thrown`;", "return `non-Error ${err === null ? 'null' : typeof err} thrown${typeof err === 'number' ? ' ' + err : ''}`;"),
 ("M24d_hash_number_value_in_log", HASH, "else logged = `non-Error ${err === null ? 'null' : typeof err} thrown`;", "else logged = `non-Error ${err === null ? 'null' : typeof err} thrown${typeof err === 'number' ? ' ' + err : ''}`;"),
 ("M25d_http_symbol_description_in_log", HTTP, "return `non-Error ${err === null ? 'null' : typeof err} thrown`;", "return `non-Error ${err === null ? 'null' : typeof err} thrown${typeof err === 'symbol' ? ' ' + err.description : ''}`;"),
 ("M26d_hash_symbol_description_in_log", HASH, "else logged = `non-Error ${err === null ? 'null' : typeof err} thrown`;", "else logged = `non-Error ${err === null ? 'null' : typeof err} thrown${typeof err === 'symbol' ? ' ' + err.description : ''}`;"),
]
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
orig = {p: open(p).read() for p in (HTTP, HASH)}
osha = {p: sha(p) for p in orig}
out = []
for mid, path, a, b in MUT:
    n = orig[path].count(a)
    if n != 1:
        out.append(f"{mid} | PATTERN COUNT {n} (not applied)"); print(out[-1]); continue
    open(path, "w").write(orig[path].replace(a, b))
    log = f"{W}/logs/mut_{re.sub(r'[^A-Za-z0-9_.]', '_', mid)}.log"
    r = subprocess.run(["bash", W + "/scripts/vt.sh", "wt_delta", log] + TESTS, capture_output=True, text=True)
    txt = open(log).read()
    m = re.search(r"Tests\s+(.*)", txt)
    failed = sorted(set(re.findall(r"FAIL\s+src/__tests__/(\S+)", txt)))
    open(path, "w").write(orig[path])
    ok = sha(path) == osha[path]
    verdict = "KILLED" if r.returncode != 0 and "failed" in (m.group(1) if m else "") else ("SURVIVED" if r.returncode == 0 else "ERROR-NOT-ASSERTION")
    out.append(f"{mid} | {verdict} | {m.group(1) if m else '?'} | restored_sha_equal={ok} | failing files: {failed}")
    print(out[-1], flush=True)
open(W + "/logs/mutants_extra_summary.log", "w").write("\n".join(out) + "\n")
