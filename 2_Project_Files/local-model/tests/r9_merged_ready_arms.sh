#!/bin/bash
# r9_merged_ready_arms.sh — red-proof for build_comment_input.sh R9 "skip a READY already at the tip" (2026-09-17 21:2x).
#
# The defect: R9 refused a brief whose range sat within 10 lines of a hunk in ANY night/READY_* diff, even when that READY's
# change had already merged (READY_KS-932 merged as 40fe4db69 / #1004, yet it refused KS-1179 F-5's docblock at
# ssrf-guard.ts:460-461). The fix: a READY R9 would match is skipped ONLY when, for the product file, every '+' line of the
# READY is present at the tip AND every '-' line (other than a line the READY also re-adds, i.e. a moved line) is absent,
# AND at least one '+' line carries substantive text. Otherwise R9 refuses exactly as before.
#
#   ARM1   the real KS-932 READY alone + an F-5 range at ssrf-guard.ts:460-461 → OLD refuses R9 naming KS-932; NEW does not
#          refuse (rc 0 on stubs) and prints "skipped: already at tip" naming KS-932
#   ARM1b  the same brief against a scratch copy of the WHOLE night/READY_* corpus → same contrast (the in-situ defect)
#   ARM2   a synthetic UNMERGED READY (KS-932 with one '+' line changed so it is not at the tip) → NEW still refuses R9
#   ARM2b  a READY with a hunk header and no '+'/'-' lines (the comment_patch_arms R9 fixture shape) → NEW still refuses R9
#   ARM3   a PARTIAL READY (KS-932 with a context line at the tip turned into a '-' line: every '+' present, a '-' still
#          present) → NEW still refuses R9
#   ARM4   regression: the seven passed inputs rebuilt from their briefs (KS-979, KS-1118-F3 a/b, KS-1179-F4, KS-1156-A2/A3,
#          KS-1120-F3) with NEW → rc 0 and the `comment` block == night/inputs/comment_*.json; other differing top-level
#          fields are printed. READY dir = scratch copy of night/READY_* MINUS each input's own comment-PASS READY (the READY
#          produced FROM that input — with it present both OLD and NEW correctly refuse, the change is not at the tip).
#          R10/R11 go to localhost stubs (Backlog / no open PR): ticket and PR state drift is not what this arm measures.
#          Also asserts NEW's full JSON == OLD's full JSON for each build (the fix changes nothing when nothing is skipped).
#   SOURCE the Secuura checkout's tracked state is unchanged
# OLD = night/build_comment_input.sh.pre-0917-r9merged, NEW = night/build_comment_input.sh.
# Writes only under a mktemp -d. Never writes to night/ or the source checkout. rc 0 = every arm holds.
set -u
exec python3 - "$@" <<'PYARMS'
import glob, http.server, json, os, re, shutil, socketserver, subprocess, sys, tempfile, threading, time

LM = "/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model"
SRC = "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files"
NIGHT = f"{LM}/night"
NEW = f"{NIGHT}/build_comment_input.sh"
OLD = f"{NIGHT}/build_comment_input.sh.pre-0917-r9merged"
R932 = f"{NIGHT}/READY_KS-932_ornith35b-q4_PASS-7of7_2026-09-15.diff.md"
PSSRF = "Blockchain/Dev/packages/shared/src/security/ssrf-guard.ts"
for f in (NEW, OLD, R932):
    if not os.path.exists(f):
        print(f"FATAL: missing {f}"); sys.exit(2)
W = tempfile.mkdtemp(prefix="r9_merged_arms.")
print(f"r9 merged-READY arms {time.strftime('%F %T')} · scratch {W}", flush=True)
RESULTS = []
def arm(name, ok, detail):
    RESULTS.append((name, ok)); print(f"{'PASS' if ok else 'FAIL'} {name} — {detail}", flush=True)
def run(cmd, env=None, timeout=600):
    e = dict(os.environ); e.update(env or {})
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=e, timeout=timeout)
    return p.returncode, p.stdout

TIP = run(["git", "-C", SRC, "ls-remote", "origin", "refs/heads/develop"])[1].split()[0]
tip_ssrf = run(["git", "-C", SRC, "show", f"{TIP}:{PSSRF}"])[1].split("\n")
src_dirty0 = run(["git", "-C", SRC, "status", "--porcelain", "--untracked-files=no"])[1]
print(f"tip {TIP} · ssrf-guard.ts {len(tip_ssrf)} lines", flush=True)

# ---- stubs for R10/R11 (localhost; the builder's http seams)
class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def _send(self, obj):
        b = json.dumps(obj).encode(); self.send_response(200); self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_POST(self):
        self.rfile.read(int(self.headers.get("Content-Length", 0)))
        self._send({"data": {"issues": {"nodes": [{"identifier": "KS-STUB", "title": "stub", "archivedAt": None, "state": {"name": "Backlog", "type": "backlog"}, "assignee": None, "attachments": {"nodes": []}}]}}})
    def do_GET(self):
        self._send([] if ("/files" in self.path or "/pulls" in self.path) else {"message": "Not Found"})
srv = socketserver.TCPServer(("127.0.0.1", 0), H); port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
STUBS = {"NIGHT_LINEAR_API": f"http://127.0.0.1:{port}/backlog", "NIGHT_GITHUB_API": f"http://127.0.0.1:{port}/clean"}

def build(builder, label, brief_path, ticket, product, ready_dir, ctx=None):
    d = os.path.join(W, label); os.makedirs(d, exist_ok=True)
    outp = os.path.join(d, "input.json")
    cmd = ["bash", builder, ticket, outp, brief_path, f"product={product}"] + ([f"ctx={ctx}"] if ctx else [])
    env = dict(STUBS); env["NIGHT_READY_DIR"] = ready_dir
    rc, o = run(cmd, env=env)
    open(os.path.join(d, "build.out"), "w").write(o)
    code = re.search(r"REFUSED (R\d+)", o)
    return rc, o, (code.group(1) if code else None), (json.load(open(outp)) if os.path.exists(outp) else None)

def ready_dir(label, files):
    d = os.path.join(W, "ready_" + label); os.makedirs(d)
    for name, text in files.items():
        open(os.path.join(d, name), "w", encoding="utf-8").write(text)
    return d
def short(o):
    m = re.search(r"REFUSED.*", o)
    return m.group(0)[:230] if m else (o.strip().splitlines()[-1][:160] if o.strip() else "")
def skipped(o, name):
    return any("skipped: already at tip" in l and name in l for l in o.splitlines())

# ---- the F-5 brief (docblock half), located by content so tip drift above it does not break the arm
i460 = next(i for i, l in enumerate(tip_ssrf) if l.startswith(" * `timeoutMs` is a TOTAL deadline on the whole operation"))
n460 = i460 + 1
assert tip_ssrf[i460 + 1].startswith(" * TLS, request, response and drain"), repr(tip_ssrf[i460 + 1])
F5 = os.path.join(W, "KS-1179-F5.md")
open(F5, "w", encoding="utf-8").write(f"""# KS-1179 F-5 (arm fixture) — comment_patch: the timeoutMs docblock covers DNS resolution

## Premises (measured)
- P1 the docblock at :{n460}-{n460 + 1} says "DNS-free connect" at the tip {TIP[:9]} — instrument: `git show <tip>:<file>` read by this arm

## Lines
- `{PSSRF}`:{n460}-{n460 + 1}

## The exact change
```diff
--- a/{PSSRF}
+++ b/{PSSRF}
@@ -{n460 - 1},4 +{n460 - 1},4 @@
 {tip_ssrf[i460 - 1]}
-{tip_ssrf[i460]}
-{tip_ssrf[i460 + 1]}
+ * `timeoutMs` is a TOTAL deadline on the whole operation -- DNS resolution,
+ * connect, TLS, request, response and drain -- not a socket-idle timer. That distinction
 {tip_ssrf[i460 + 2]}
```
""")
r932 = open(R932, encoding="utf-8").read()
N932 = os.path.basename(R932)

# ---------------------------------------------------------------- ARM1 real KS-932 alone
rd = ready_dir("arm1", {N932: r932})
rc_o, o_o, c_o, _ = build(OLD, "ARM1_old", F5, "KS-1179-F5", PSSRF, rd)
rc_n, o_n, c_n, j_n = build(NEW, "ARM1_new", F5, "KS-1179-F5", PSSRF, rd)
arm("ARM1 real KS-932 READY + range :460-461 → OLD refuses R9 naming KS-932",
    rc_o == 2 and c_o == "R9" and N932 in o_o, f"rc={rc_o} {short(o_o)}")
arm("ARM1 NEW does not refuse on R9, names KS-932 'skipped: already at tip', rc 0",
    rc_n == 0 and c_n is None and j_n is not None and skipped(o_n, N932), f"rc={rc_n} code={c_n} :: {[l for l in o_n.splitlines() if 'skipped' in l][:1]} :: {short(o_n)}")

# ---------------------------------------------------------------- ARM1b whole corpus
corpus = {os.path.basename(p): open(p, encoding="utf-8", errors="replace").read() for p in sorted(glob.glob(f"{NIGHT}/READY_*")) if not p.endswith((".pre-0916-d7fix",)) and ".pre-" not in os.path.basename(p)}
rd = ready_dir("arm1b", corpus)
rc_o, o_o, c_o, _ = build(OLD, "ARM1b_old", F5, "KS-1179-F5", PSSRF, rd)
rc_n, o_n, c_n, j_n = build(NEW, "ARM1b_new", F5, "KS-1179-F5", PSSRF, rd)
arm(f"ARM1b whole READY corpus ({len(corpus)} files) → OLD refuses R9 naming KS-932",
    rc_o == 2 and c_o == "R9" and N932 in o_o, f"rc={rc_o} {short(o_o)}")
arm("ARM1b NEW rc 0, KS-932 skipped as already at tip",
    rc_n == 0 and c_n is None and skipped(o_n, N932), f"rc={rc_n} code={c_n} :: {[l for l in o_n.splitlines() if 'READY' in l][:3]}")

# ---------------------------------------------------------------- ARM2 synthetic UNMERGED
OLDPLUS = "+  const startedAt = Date.now();"; NEWPLUS = "+  const startedAt = performance.now();"
assert r932.count(OLDPLUS) == 1 and NEWPLUS[1:] not in tip_ssrf
NU = "READY_KS-0001_arm-unmerged.diff.md"
rd = ready_dir("arm2", {NU: r932.replace(OLDPLUS, NEWPLUS)})
rc_o, o_o, c_o, _ = build(OLD, "ARM2_old", F5, "KS-1179-F5", PSSRF, rd)
rc_n, o_n, c_n, _ = build(NEW, "ARM2_new", F5, "KS-1179-F5", PSSRF, rd)
arm("ARM2 unmerged READY (one '+' line not at the tip) → NEW still refuses R9 naming it, nothing skipped (OLD refuses too)",
    rc_n == 2 and c_n == "R9" and NU in o_n and "skipped" not in o_n and rc_o == 2 and c_o == "R9",
    f"new rc={rc_n} {short(o_n)} · old rc={rc_o} code={c_o}")

# ---------------------------------------------------------------- ARM2b no +/- lines at all
NE = "READY_KS-0002_arm-emptyhunk.diff.md"
rd = ready_dir("arm2b", {NE: f"# arm\n```diff\n--- a/packages/shared/src/security/ssrf-guard.ts\n+++ b/packages/shared/src/security/ssrf-guard.ts\n@@ -{n460 + 5},3 +{n460 + 5},3 @@\n```\n"})
rc_n, o_n, c_n, _ = build(NEW, "ARM2b_new", F5, "KS-1179-F5", PSSRF, rd)
arm("ARM2b READY hunk with no '+'/'-' lines (no evidence it merged) → NEW still refuses R9",
    rc_n == 2 and c_n == "R9" and NE in o_n and "skipped" not in o_n, f"rc={rc_n} {short(o_n)}")

# ---------------------------------------------------------------- ARM3 PARTIAL: every '+' at tip, a '-' still at tip
CTX = "         error: `request exceeded its ${timeoutMs}ms deadline (connect, transfer and drain)`,"
assert r932.count("\n" + CTX + "\n") == 1 and CTX[1:] in tip_ssrf, "ARM3 fixture line not found"
NP = "READY_KS-0003_arm-partial.diff.md"
rd = ready_dir("arm3", {NP: r932.replace("\n" + CTX + "\n", "\n-" + CTX[1:] + "\n")})
rc_o, o_o, c_o, _ = build(OLD, "ARM3_old", F5, "KS-1179-F5", PSSRF, rd)
rc_n, o_n, c_n, _ = build(NEW, "ARM3_new", F5, "KS-1179-F5", PSSRF, rd)
arm("ARM3 partial READY ('+' present, a '-' line still present) → NEW still refuses R9, nothing skipped (OLD refuses too)",
    rc_n == 2 and c_n == "R9" and NP in o_n and "skipped" not in o_n and rc_o == 2 and c_o == "R9",
    f"new rc={rc_n} {short(o_n)} · old rc={rc_o} code={c_o}")

# ---------------------------------------------------------------- ARM4 regression: the seven passed inputs
MAP = [("comment_979.json", "KS-979.md"), ("comment_1118F3a.json", "KS-1118-F3.md"), ("comment_1118F3b.json", "KS-1118-F3.md"),
       ("comment_1179F4.json", "KS-1179-F4.md"), ("comment_1156A2.json", "KS-1156-A2A3.md"), ("comment_1156A3.json", "KS-1156-A2A3.md"),
       ("comment_1120F3.json", "KS-1120-F3.md")]
for inp_name, brief_name in MAP:
    inp = json.load(open(f"{NIGHT}/inputs/{inp_name}", encoding="utf-8"))
    ident, prod, ctx = inp["ticket"]["identifier"], inp["product_file"], inp.get("_night_num_ctx")
    own = [n for n in corpus if n.startswith(f"READY_{ident}_") and "comment-PASS" in n]
    rd = ready_dir("arm4_" + ident, {n: t for n, t in corpus.items() if n not in own})
    rc_n, o_n, c_n, j_n = build(NEW, f"ARM4_{ident}_new", f"{NIGHT}/briefs/{brief_name}", ident, prod, rd, ctx)
    rc_o, o_o, c_o, j_o = build(OLD, f"ARM4_{ident}_old", f"{NIGHT}/briefs/{brief_name}", ident, prod, rd, ctx)
    same_comment = j_n is not None and j_n["comment"] == inp["comment"]
    diff_fields = sorted(k for k in set(inp) | set(j_n or {}) if (j_n or {}).get(k) != inp.get(k)) if j_n else ["<no output>"]
    new_eq_old = j_n is not None and j_n == j_o
    arm(f"ARM4 {ident} rebuilt from {brief_name} (excluded own READY {own}) → NEW rc 0, comment block identical, NEW json == OLD json",
        rc_n == 0 and same_comment and new_eq_old and len(own) == 1,
        f"new rc={rc_n} old rc={rc_o} comment_same={same_comment} new==old={new_eq_old} differing top-level fields vs input: {diff_fields} (tip {inp['tip'][:9]}→{(j_n or {}).get('tip', '?')[:9]}) :: {short(o_n)}")

srv.shutdown()
src_dirty1 = run(["git", "-C", SRC, "status", "--porcelain", "--untracked-files=no"])[1]
arm("SOURCE checkout tracked state unchanged across the arms", src_dirty0 == src_dirty1, f"before={len(src_dirty0.splitlines())} after={len(src_dirty1.splitlines())} lines")
n_ok = sum(1 for _, ok in RESULTS if ok)
print(f"SUMMARY {n_ok}/{len(RESULTS)} arms hold · scratch {W}", flush=True)
sys.exit(0 if n_ok == len(RESULTS) else 1)
PYARMS
