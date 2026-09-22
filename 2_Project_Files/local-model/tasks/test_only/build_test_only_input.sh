#!/bin/bash
# build_test_only_input.sh <KS-id> <out input.json> <brief.md> [tip=<sha>] [ctx=<n>] [repo_subdir=<dir>]
#
# Builds a test_only input (2026-09-18, commissioned by Wednesday: KS-1254 / KS-1137 / KS-1110-style tickets ADD TEST CELLS
# that pin EXISTING behaviour; code_patch needs a product hunk and plants ONE tamper, so it refused them). The brief is
# Wednesday's; this script turns it into the JSON the model reads and tasks/test_only/checker.sh grades, and REFUSES
# (rc 2) a brief the checker could not grade honestly. Read verbs only on the source checkout (`git show`, `ls-tree`).
#
# BRIEF SHAPE (headings are matched case-insensitively; every name in backticks):
#   File: `<repo path of the ONE test file>`            (exists at the tip = MODIFY IN PLACE; absent = NEW file)
#   Tip: `<40-hex sha>`                                 (optional; a tip= pin wins; else origin develop, as bash_patch)
#   ## The exact change      one or more fenced blocks, unified-diff body lines (`@@` header, ' ' context, '-', '+')
#   ## Cells                 optional aliases:  - `liveness` = `the boundary run is live: one E7 per firing row, ...`
#   ## Tampers               one `### <ID> ...` per tamper, each with
#                              File: `<repo path>`   Line: <n>
#                              From:  a fenced block holding EXACTLY the tip line (byte for byte)
#                              To:    a fenced block holding EXACTLY the replacement line
#                              Reds: `<cell>`, `<cell>`   (the EXACT set that must red under it)
#   ## Controls              - `<cell>`  (must stay green under every tamper)
#
# REFUSALS (each names the line): the fence's old side (context + '-') does not equal the tip test file at the header's
# line; a blank line anywhere in a modify-in-place fence (a blank context line or a blank '+': IMPROVEMENTS 2026-09-18
# 06:2x rule 1, widened at KS-1237); a pure-insertion hunk with no TRAILING context (rule 2); a non-ASCII '+' line;
# a '+' line byte-identical to a '-' line of the same fence (context marked as addition); a tamper whose file is the
# test file, whose From is not the tip's line at that number, whose To equals From or spans lines, or whose Reds is
# empty; a control also declared red; no tamper at all.
# BASH SUITES (2026-09-18 18:xx): a `File:` ending `.test.sh` selects runner `bash` (run by the checker as `/bin/bash
# <file>` from the clone root; bash 3.2.57). Cell names in Reds:/Controls are LITERAL PREFIXES of the description the
# suite prints on its `ok …` / `FAIL …` line (see tasks/test_only/checker.sh, BASH RUNNER). Extra refusals for a bash
# brief, each one a thing the checker could not grade fairly: the suite after the fence does not parse under /bin/bash
# (`bash -n`); a '+' line uses a bash-4 idiom bash 3.2 lacks (mapfile/readarray, declare -A/-n, ${x,,} ${x^^}, `timeout`,
# `|&`, `&>>`, coproc); the suite prints no `ok`/`PASS` AND `FAIL` cell line (no per-check verdict to read); a declared
# cell name that is not literally in the suite's text, or carries `$`, a backtick or a backslash (it would not be
# printed as written); a tamper on a shell file whose tampered text does not parse (a tamper that breaks parsing reds
# while executing none of the logic — the Secuura suites' own assert_parses rule); a tamper on a test file.
# HEADER FIELD (2026-09-19): the JSON carries `diff_file_headers` = the two lines the diff must open with (modify:
# `--- a/<test_file>` / `+++ b/<test_file>`; new: `--- /dev/null` / `+++ b/<test_file>`), named by task.md rule 3.
# RUNNER PIN (2026-09-19, KS-1269 N71-1: vc-issuer's package.json lists jest/ts-jest beside vitest, so detection refused
# "cannot tell the runner"): a `runner=<jest|vitest>` argument, else a `Runner: \`<jest|vitest>\`` line in the brief's
# header (before the first `## `), names the runner — the pin wins over the line, as tip= wins over Tip:. It is honoured
# ONLY when the named runner is in the service's own package.json (dependencies/devDependencies, or a token of a scripts
# command); otherwise REFUSED. Never for a *.test.sh suite (runner bash is fixed). With no pin and no Runner: line the
# build is byte-for-byte what it was, the ambiguous-service refusal included. A pinned build carries `runner_pin`.
# BLOCK TAMPER (2026-09-19, the #1070-#1076 gate's REVOKEGUARDAFTER404 / REVOKEGUARDBELOWREASON: 4-line guard MOVES that a
# one-line From/To cannot express): a tamper whose From fence holds TWO OR MORE lines is a block tamper. The From block
# must occur EXACTLY ONCE, as whole consecutive lines, in the product file at the tip (0 matches or 2+ matches is REFUSED,
# naming the count and the lines); its To fence (one or more lines, != From) replaces it. `Line:` is optional for a block
# and, when given, must be the line the block starts at (a cross-check, not the locator). A block tamper's JSON carries
# `block: true`, `line` = the matched start, `from_lines`, `to_lines`; the checker plants it after the same exact-and-
# unique check and restores by bytes (T8) as for a line. A single-line From is handled EXACTLY as before (Line: required,
# To one line) — its JSON is byte-for-byte unchanged.
# FARM (2026-09-22 15:5x, KS-1145 / the ks949 suite; feed15): a BASH suite that shells out to the workspace install (tsx) or
# needs packages/shared built dies on the bare clone the bash runner prepares (ks949_main_seed_idempotence.test.sh :113-:114
# `die`, not SKIP). A `Farm: \`<tokens>\`` line in the brief's header (before the first `## `), tokens joined by `+` from the
# set {shared, tsx}, names what the suite needs: `tsx` = the source checkout's node_modules symlink-farmed into the clone
# (node_modules/.bin/tsx resolves); `shared` = that farm PLUS packages/shared built in the clone (dist/index.js). The JSON
# carries `farm` (the tokens, canonical order shared+tsx) and, for `shared`, `shared_pkg_dir` = packages/shared; tasks/
# test_only/prepare_clone.sh reads `farm` and routes the bash branch through the code_patch farm. REFUSED (rc 2, naming
# the line): a Farm: line on a vitest/jest brief (those are always farmed), an empty value, a token outside the set, a
# duplicate token. With no Farm: line the JSON is byte-for-byte what it was (no `farm` key; shared_pkg_dir "" for bash).
# rc 0 ok · 2 refused · 1 usage/error. bash 3.2. stderr never discarded.
set -uo pipefail
ID="${1:-}"; OUT="${2:-}"; BRIEF="${3:-}"; shift 3 2>/dev/null
[ -n "$ID" ] && [ -n "$OUT" ] && [ -f "$BRIEF" ] || { echo "usage: build_test_only_input.sh <KS-id> <out> <brief.md> [tip=<sha>] [ctx=N] [repo_subdir=<dir>]" >&2; exit 1; }
SRC="${NIGHT_SOURCE_CHECKOUT:-/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files}"
TIP=""
for a in "$@"; do case "$a" in tip=*) TIP="${a#tip=}";; esac; done
[ -z "$TIP" ] && TIP="$(python3 -c 'import re,sys; m=re.search(r"^Tip:\s*`?([0-9a-f]{40})`?", open(sys.argv[1],encoding="utf-8").read(), re.M); print(m.group(1) if m else "")' "$BRIEF")"
if [ -z "$TIP" ]; then
  TIP="$(git -C "$SRC" ls-remote origin refs/heads/develop 2>/dev/null | awk '{print $1}')"
  [ -n "$TIP" ] || { echo "build_test_only_input: no tip= pin, no Tip: line, and ls-remote returned nothing" >&2; exit 1; }
  if [ "$(git -C "$SRC" cat-file -t "$TIP" 2>/dev/null)" != "commit" ]; then
    OV="$(dirname "$0")/../../night/tip_override.txt"; OV_SHA=""; OV_AGAINST=""
    [ -f "$OV" ] && read -r OV_SHA OV_AGAINST OV_REST < "$OV"
    if [ -n "$OV_SHA" ] && [ "$OV_AGAINST" = "$TIP" ] && [ "$(git -C "$SRC" cat-file -t "$OV_SHA" 2>/dev/null)" = "commit" ]; then
      echo "build_test_only_input: G6 — origin develop $TIP is not local; using VERIFIED OVERRIDE $OV_SHA" >&2; TIP="$OV_SHA"
    else
      echo "build_test_only_input: REFUSED — tip $TIP not local and no valid override (no fetch from here)" >&2; exit 2
    fi
  fi
fi
[ "$(git -C "$SRC" cat-file -t "$TIP" 2>/dev/null)" = "commit" ] || { echo "build_test_only_input: REFUSED — tip $TIP is not a local commit" >&2; exit 2; }
python3 - "$ID" "$OUT" "$BRIEF" "$SRC" "$TIP" "$@" <<'PY'
import json, re, subprocess, sys, os
ident, out, brief, src, tip = sys.argv[1:6]
pins = dict(a.split("=", 1) for a in sys.argv[6:] if "=" in a)
subdir = pins.get("repo_subdir", "Blockchain/Dev").strip("/")
def refuse(msg):
    sys.stderr.write("build_test_only_input: REFUSED — " + msg + "\n"); sys.exit(2)
def show(p):
    r = subprocess.run(["git", "-C", src, "show", f"{tip}:{p}"], capture_output=True)
    return None if r.returncode else r.stdout.decode("utf-8")
def ls(p):
    r = subprocess.run(["git", "-C", src, "ls-tree", "--name-only", tip, p.rstrip("/") + "/"], capture_output=True, text=True)
    return [os.path.basename(x) for x in r.stdout.split("\n") if x]
text = open(brief, encoding="utf-8").read()
def section(name):
    m = re.search(r"^##\s*" + name + r"\b.*?$(.*?)(?=^##\s|\Z)", text, re.M | re.S | re.I)
    return m.group(1) if m else ""
fence_re = re.compile(r"^```[^\n]*\n(.*?)^```", re.M | re.S)

# ---- the ONE test file
m = re.search(r"^File:\s*`([^`]+)`", text, re.M)
if not m: refuse("no `File: \\`<test file>\\`` line before the first ## heading")
tf = m.group(1).strip()
is_bash = tf.endswith(".test.sh")
if not is_bash and not re.search(r"\.(test|spec)\.[cm]?[jt]sx?$", tf): refuse(f"{tf} is not a *.test.* / *.spec.* (js/ts) file nor a *.test.sh bash suite")
if not tf.startswith(subdir + "/"): refuse(f"{tf} is not under repo_subdir {subdir}/")
ttext = show(tf); mode = "modify" if ttext is not None else "new"

# ---- the service (package) that runs it: nearest ancestor with a runner config or a package.json naming one
d = os.path.dirname(tf); svc = None; runner = None; why = ""
if is_bash:   # a bash suite needs no package: it runs from the clone root; service_dir is only its directory
    svc = d; runner = "bash"; why = "bash suite"; d = subdir
while d.startswith(subdir + "/") and d != subdir:
    names = ls(d)
    jest = [n for n in names if n.startswith("jest.config.")]; vit = [n for n in names if n.startswith("vitest.config.")]
    if "package.json" in names:
        try: pj = json.loads(show(d + "/package.json") or "{}")
        except Exception: pj = {}
        toks = str((pj.get("scripts") or {}).get("test") or "").replace("&&", " ").split()
        deps = {**(pj.get("dependencies") or {}), **(pj.get("devDependencies") or {})}
        if "jest" in toks or "jest" in deps or "ts-jest" in deps: jest.append("package.json")
        if "vitest" in toks or "vitest" in deps: vit.append("package.json")
    if jest or vit or "package.json" in names:
        svc = d; why = f"jest:{jest or '-'} vitest:{vit or '-'}"
        runner = "jest" if (jest and not vit) else ("vitest" if (vit and not jest) else None)
        break
    d = os.path.dirname(d)
if not svc: refuse(f"no package.json / runner config above {tf} inside {subdir}")
# ---- RUNNER PIN (2026-09-19): runner= arg, else the brief header's `Runner:` line; honoured only if package.json has it
rpin = pins.get("runner"); rsrc = "the runner= pin"; runner_pin = ""
if rpin is None:
    hm = re.search(r"^Runner:[ \t]*`?([^`\s]+)`?[ \t]*$", re.split(r"^##\s", text, maxsplit=1, flags=re.M)[0], re.M)
    rpin = hm.group(1) if hm else None; rsrc = "the brief's Runner: line"
if rpin is not None:
    if is_bash: refuse(f"runner pin {rpin!r} ({rsrc}) on a *.test.sh suite — a bash suite's runner is bash, never pinned")
    if rpin not in ("jest", "vitest"): refuse(f"runner pin {rpin!r} ({rsrc}) is not jest or vitest")
    pjt = show(svc + "/package.json")
    if pjt is None: refuse(f"runner pin {rpin} ({rsrc}): {svc} has no package.json to confirm it against")
    try: pj = json.loads(pjt)
    except Exception: refuse(f"runner pin {rpin} ({rsrc}): {svc}/package.json does not parse")
    deps = {**(pj.get("dependencies") or {}), **(pj.get("devDependencies") or {})}
    stoks = set(" ".join(str(v) for v in (pj.get("scripts") or {}).values()).replace("&&", " ").replace(";", " ").split())
    if rpin not in deps and rpin not in stoks:
        refuse(f"runner pin {rpin} ({rsrc}) is NOT in {svc}/package.json (no {rpin} in dependencies/devDependencies, no scripts command running it) — a pin must name a runner the service actually has (detected {why})")
    runner = rpin; runner_pin = f"{rpin} by {rsrc}; detected {why}"
if not runner: refuse(f"cannot tell the runner of {svc} ({why}) — exactly one of jest / vitest must be marked")
# ---- FARM (2026-09-22): the brief header's `Farm:` line — bash suites only; tokens from {shared, tsx}
farm = ""
fm = re.search(r"^Farm:[ \t]*(.*?)[ \t]*$", re.split(r"^##\s", text, maxsplit=1, flags=re.M)[0], re.M)
if fm:
    raw = fm.group(1).strip().strip("`").strip()
    if not is_bash: refuse(f"Farm: line {fm.group(0)!r} on a {runner} brief — only a *.test.sh suite runs on a bare clone; vitest/jest briefs are always farmed")
    toks = [x.strip() for x in raw.split("+")] if raw else []
    if not toks or any(not x for x in toks): refuse(f"Farm: line {fm.group(0)!r} names no token — write Farm: `shared+tsx` (tokens from shared, tsx)")
    badt = [x for x in toks if x not in ("shared", "tsx")]
    if badt: refuse(f"Farm: line {fm.group(0)!r} names {badt[0]!r} — not a farm token (the set is shared, tsx); a suite that needs more is not briefable on this runner")
    if len(set(toks)) != len(toks): refuse(f"Farm: line {fm.group(0)!r} repeats a token")
    farm = "+".join(x for x in ("shared", "tsx") if x in toks)
service_dir = svc[len(subdir) + 1:]
test_rel = tf[len(svc) + 1:]

# ---- the exact change
xs = section("The exact change")
blocks = fence_re.findall(xs)
if not blocks: refuse("`## The exact change` has no fenced block")
tip_lines = (ttext or "").split("\n")
if tip_lines and tip_lines[-1] == "": tip_lines.pop()
expected_plus, must_remove, hunks = [], [], 0
for bi, blk in enumerate(blocks, 1):
    body = blk.split("\n")
    if body and body[-1] == "": body.pop()
    if mode == "new":
        for ln in body:
            if ln.startswith("@@") or ln.startswith("+++") or ln.startswith("---"): continue
            if not ln.startswith("+"): refuse(f"fence {bi}: a NEW test file's fence is all '+' lines; saw {ln[:60]!r}")
            expected_plus.append(ln[1:])
        continue
    cur = None
    def close(h):
        if h is None: return
        kinds = [k for k, _ in h["lines"]]
        if "-" not in kinds and kinds and kinds[-1] != " ":
            refuse(f"fence {bi} hunk @@ -{h['start']}: a pure insertion must END with trailing context (rule 2, 2026-09-18 06:2x) — its last line is a '+'")
        old = [t for k, t in h["lines"] if k in " -"]
        s = h["start"] - 1
        if tip_lines[s:s + len(old)] != old:
            first = next((i for i, (a, b) in enumerate(zip(tip_lines[s:s + len(old)], old)) if a != b), min(len(old), len(tip_lines) - s))
            refuse(f"fence {bi} hunk @@ -{h['start']}: old-side line {first + 1} is {old[first] if first < len(old) else '(past EOF)'!r} but the tip's line {s + first + 1} is {tip_lines[s + first] if s + first < len(tip_lines) else '(EOF)'!r} — write the fence from the file at {tip[:9]}")
    for li, ln in enumerate(body, 1):
        mh = re.match(r"^@@ -(\d+)(?:,\d+)? \+\d+(?:,\d+)? @@", ln)
        if mh:
            close(cur); cur = {"start": int(mh.group(1)), "lines": []}; hunks += 1; continue
        if cur is None: refuse(f"fence {bi} line {li}: a body line before any `@@ -N,… @@` header")
        if ln == "" or (ln[:1] in " +-" and ln[1:].strip() == ""):
            refuse(f"fence {bi} line {li}: a BLANK line in a modify-in-place fence (context or '+') — the model will not reproduce it (IMPROVEMENTS 2026-09-18 06:2x rule 1, widened); anchor on non-blank lines")
        k = ln[0]
        if k not in " +-": refuse(f"fence {bi} line {li}: {ln[:40]!r} is not ' ', '+' or '-'")
        cur["lines"].append((k, ln[1:]))
        if k == "+": expected_plus.append(ln[1:])
        elif k == "-": must_remove.append(ln[1:])
    close(cur)
    if not cur: refuse(f"fence {bi}: no `@@` hunk")
if not expected_plus: refuse("the exact change adds no '+' line — a test_only ticket ADDS cells")
nona = [p for p in expected_plus if any(ord(c) > 127 for c in p)]
if nona: refuse(f"{len(nona)} '+' line(s) carry non-ASCII (the model echoes \\u escapes; KS-1133/KS-1180): {nona[0][:70]!r}")
dup = sorted({p for p in expected_plus if p.strip() and p in must_remove})
if dup: refuse(f"'+' line(s) byte-identical to a '-' line in the fence — CONTEXT marked as addition: {dup[:2]}")

# ---- cells, tampers, controls
alias = {}
for a, t in re.findall(r"^\s*[-*]\s*`([^`]+)`\s*=\s*`([^`]+)`", section("Cells"), re.M):
    alias[a.strip()] = t.strip()
res = lambda n: alias.get(n.strip(), n.strip())
tampers = []
ts = section("Tampers")
parts = re.split(r"^###\s+", ts, flags=re.M)[1:]
if not parts: refuse("`## Tampers` has no `### <ID>` entry — test_only is graded by named tampers")
seen = set()
for p in parts:
    tid = p.split()[0].strip().rstrip(":—-")
    if tid in seen: refuse(f"tamper id {tid} appears twice")
    seen.add(tid)
    mf = re.search(r"^File:\s*`([^`]+)`", p, re.M); ml = re.search(r"^Line:[ \t]*`?(\d+)`?", p, re.M)
    mfrom = re.search(r"^From:\s*\n```[^\n]*\n(.*?)\n```", p, re.M | re.S); mto = re.search(r"^To:\s*\n```[^\n]*\n(.*?)\n```", p, re.M | re.S)
    mr = re.search(r"^Reds:[ \t]*(.*)$", p, re.M)
    if mf and mfrom and mto and mr and "\n" in mfrom.group(1):
        # ---- BLOCK TAMPER (2026-09-19): From spans 2+ lines; located by an exact, unique whole-line match at the tip
        f = mf.group(1).strip(); frm = mfrom.group(1); to = mto.group(1)
        if f == tf: refuse(f"tamper {tid}: its file is the test file — a tamper mutates PRODUCT code the cells pin")
        if frm == to: refuse(f"tamper {tid}: To equals From — nothing is tampered")
        ftext = show(f)
        if ftext is None: refuse(f"tamper {tid}: {f} is not at {tip[:9]}")
        fl = ftext.split("\n"); bl = frm.split("\n"); n = len(bl)
        hits = [i + 1 for i in range(len(fl) - n + 1) if fl[i:i + n] == bl]
        if not hits: refuse(f"tamper {tid}: the {n}-line From block does not occur in {f} at {tip[:9]} (whole lines, byte for byte); its first line {bl[0]!r} occurs at line(s) {[i + 1 for i, x in enumerate(fl) if x == bl[0]][:8] or 'none'}")
        if len(hits) > 1: refuse(f"tamper {tid}: the {n}-line From block occurs {len(hits)} times in {f} at {tip[:9]} (starting at lines {hits[:8]}) — a block tamper must match EXACTLY ONCE; widen the block until it is unique")
        if ml and int(ml.group(1)) != hits[0]: refuse(f"tamper {tid}: Line: {ml.group(1)} but the From block starts at {f}:{hits[0]} at {tip[:9]}")
        reds = [res(x) for x in re.findall(r"`([^`]+)`", mr.group(1))]
        if not reds: refuse(f"tamper {tid}: Reds is empty — a tamper that should red nothing grades nothing")
        tampers.append({"id": tid, "file": f, "line": hits[0], "from": frm, "to": to, "reds": reds,
                        "reds_as_written": re.findall(r"`([^`]+)`", mr.group(1)),
                        "block": True, "from_lines": n, "to_lines": len(to.split("\n"))})
        continue
    if not (mf and ml and mfrom and mto and mr): refuse(f"tamper {tid}: needs File:, Line:, From: (fenced), To: (fenced) and Reds: — missing {[n for n, x in (('File', mf), ('Line', ml), ('From', mfrom), ('To', mto), ('Reds', mr)) if not x]}")
    f = mf.group(1).strip(); ln = int(ml.group(1)); frm = mfrom.group(1); to = mto.group(1)
    if f == tf: refuse(f"tamper {tid}: its file is the test file — a tamper mutates PRODUCT code the cells pin")
    if "\n" in frm or "\n" in to: refuse(f"tamper {tid}: From/To must be ONE line each")
    if frm == to: refuse(f"tamper {tid}: To equals From — nothing is tampered")
    ftext = show(f)
    if ftext is None: refuse(f"tamper {tid}: {f} is not at {tip[:9]}")
    fl = ftext.split("\n")
    if not (0 < ln <= len(fl)) or fl[ln - 1] != frm:
        refuse(f"tamper {tid}: {f}:{ln} at the tip is {fl[ln - 1] if 0 < ln <= len(fl) else '(out of range)'!r}, the brief's From is {frm!r} (byte for byte)")
    reds = [res(x) for x in re.findall(r"`([^`]+)`", mr.group(1))]
    if not reds: refuse(f"tamper {tid}: Reds is empty — a tamper that should red nothing grades nothing")
    tampers.append({"id": tid, "file": f, "line": ln, "from": frm, "to": to, "reds": reds,
                    "reds_as_written": re.findall(r"`([^`]+)`", mr.group(1))})
controls = [res(x) for x in re.findall(r"^\s*[-*]\s*`([^`]+)`", section("Controls"), re.M)]
if not controls: refuse("`## Controls` lists no cell — a control must stay green under every tamper (proves the run is live)")
clash = sorted({c for c in controls for t in tampers if c in t["reds"]})
if clash: refuse(f"control(s) also declared red under a tamper: {clash}")

if runner == "bash":
    # ---- the suite as it will run: the tip file with the fence applied (modify), or the fence's '+' lines (new)
    if mode == "new":
        after = expected_plus[:]
    else:
        after = tip_lines[:]; off = 0
        for blk in blocks:
            body = blk.split("\n")
            if body and body[-1] == "": body.pop()
            cur = None; hs = []
            for ln in body:
                mh = re.match(r"^@@ -(\d+)", ln)
                if mh: cur = {"start": int(mh.group(1)), "lines": []}; hs.append(cur); continue
                cur["lines"].append((ln[0], ln[1:]))
            for h in hs:
                old = [t for k, t in h["lines"] if k in " -"]; new = [t for k, t in h["lines"] if k in " +"]
                s0 = h["start"] - 1 + off; after[s0:s0 + len(old)] = new; off += len(new) - len(old)
    atext = "\n".join(after) + "\n"
    r = subprocess.run(["/bin/bash", "-n"], input=atext.encode("utf-8"), capture_output=True)
    if r.returncode: refuse(f"the suite after the fence does not parse under /bin/bash (bash -n): {r.stderr.decode('utf-8', 'replace').strip()[:200]}")
    B4 = re.compile(r"\b(mapfile|readarray|coproc)\b|\bdeclare\s+-[a-zA-Z]*[An]|\$\{[A-Za-z_][A-Za-z0-9_]*(,,?|\^\^?)[}]|(^|[\s;&|(])timeout\s|\|&|&>>")
    b4 = [p for p in expected_plus if B4.search(p) and not p.lstrip().startswith("#")]
    if b4: refuse(f"a '+' line uses a bash-4 idiom /bin/bash 3.2 lacks: {b4[0].strip()[:90]!r}")
    if not (re.search(r"""(printf|echo)\s+(-e\s+)?['"]\s{0,3}(ok|PASS)\b""", atext) and re.search(r"""(printf|echo)\s+(-e\s+)?['"]\s{0,3}FAIL\b""", atext)):
        refuse("the suite prints no `ok`/`PASS` AND `FAIL` cell line (printf/echo) — the checker reads one verdict line per check and this suite gives none to read")
    allnames = sorted({n for t in tampers for n in t["reds"]} | set(controls))
    for n in allnames:
        if re.search(r"[$`\\]", n): refuse(f"cell name {n[:80]!r} carries `$`, a backtick or a backslash — the suite prints it expanded, so the name would not match what runs")
        if n not in atext: refuse(f"cell name {n[:80]!r} is not literally in the suite's text — a bash cell is named by a literal prefix of the description its ok/FAIL line prints")
    for t in tampers:
        f = t["file"]
        if re.search(r"(^|/)__tests__/|\.test\.sh$", f): refuse(f"tamper {t['id']}: {f} is a test file — a tamper mutates PRODUCT code")
        ftext = show(f); fl = ftext.split("\n")
        shelly = f.endswith((".sh", ".bash", ".command")) or (fl and re.match(r"^#!.*\b(ba)?sh\b", fl[0]))
        if shelly:
            fl2 = fl[:]
            if t.get("block"): fl2[t["line"] - 1:t["line"] - 1 + t["from_lines"]] = t["to"].split("\n")
            else: fl2[t["line"] - 1] = t["to"]
            r = subprocess.run(["/bin/bash", "-n"], input="\n".join(fl2).encode("utf-8"), capture_output=True)
            if r.returncode: refuse(f"tamper {t['id']}: {f} does not parse with the tamper planted (bash -n: {r.stderr.decode('utf-8', 'replace').strip()[:140]}) — a tamper that breaks parsing reds while executing none of the logic")
src_repo = os.path.abspath(src)
cmd = "npx jest <file>" if runner == "jest" else ("npx vitest run <file>" if runner == "vitest" else "/bin/bash <repo path> (bash 3.2) from the repo root")
inp = {"ticket": {"identifier": ident, "title": text.splitlines()[0].lstrip("# ").strip()[:200], "description": text},
       "repo": {"source_checkout": src_repo, "tip": tip, "branch": "develop",
                "test_runner": (f"{runner} (run one file with `{cmd}` from {subdir}/{service_dir})" if runner != "bash" else
                                f"bash (the suite runs as `{cmd}`; a cell is one `ok <desc>` / `FAIL <desc>` line the suite's own helper prints; bash 3.2: no mapfile, no declare -A, no ${{x,,}}, no timeout)")},
       "task_type": "test_only", "tip": tip, "source_checkout": src_repo, "repo_subdir": subdir,
       "service_dir": service_dir, "shared_pkg_dir": (("" if "shared" not in farm else pins.get("shared_pkg_dir", "packages/shared")) if runner == "bash" else pins.get("shared_pkg_dir", "packages/shared")),
       "shared_pkg_name": pins.get("shared_pkg_name", "@secuura/shared"),
       "test_file": tf, "test_file_rel_to_service": test_rel, "test_mode": mode,
       # 2026-09-19 (IMPROVEMENTS 08:06, KS-739 F1 r1 FAIL T2): the EXACT two file-header lines the diff must open with,
       # derived from test_file + test_mode (never from the brief text) — the fence cannot carry them (the validator above
       # refuses a body line before the first @@), and a model given only a bare @@ fence can drop them. task.md rule 3.
       "diff_file_headers": ([f"--- a/{tf}", f"+++ b/{tf}"] if mode == "modify" else ["--- /dev/null", f"+++ b/{tf}"]),
       "runner": runner,
       "expected_plus": expected_plus, "must_remove": must_remove, "cells": alias,
       "tampers": tampers, "controls": controls, "files": {}}
if ttext is not None: inp["files"][tf] = ttext
if runner_pin: inp["runner_pin"] = runner_pin
if farm: inp["farm"] = farm
if "ctx" in pins: inp["_night_num_ctx"] = int(pins["ctx"])
json.dump(inp, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(f"wrote {out}: test_only {mode} {tf} ({runner}, service {service_dir}) at {tip[:9]}; '+' {len(expected_plus)} '-' {len(must_remove)} in {hunks} hunk(s); tampers {len(tampers)} ({', '.join(t['id'] + '->' + str(len(t['reds'])) for t in tampers)}); controls {len(controls)}" + (f"; RUNNER PINNED {runner_pin}" if runner_pin else "") + (f"; FARM {farm} (opt-in, brief Farm: line)" if farm else ""))
PY
