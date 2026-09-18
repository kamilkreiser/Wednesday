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
if not re.search(r"\.(test|spec)\.[cm]?[jt]sx?$", tf): refuse(f"{tf} is not a *.test.* / *.spec.* file")
if not tf.startswith(subdir + "/"): refuse(f"{tf} is not under repo_subdir {subdir}/")
ttext = show(tf); mode = "modify" if ttext is not None else "new"

# ---- the service (package) that runs it: nearest ancestor with a runner config or a package.json naming one
d = os.path.dirname(tf); svc = None; runner = None; why = ""
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
if not runner: refuse(f"cannot tell the runner of {svc} ({why}) — exactly one of jest / vitest must be marked")
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

src_repo = os.path.abspath(src)
cmd = "npx jest <file>" if runner == "jest" else "npx vitest run <file>"
inp = {"ticket": {"identifier": ident, "title": text.splitlines()[0].lstrip("# ").strip()[:200], "description": text},
       "repo": {"source_checkout": src_repo, "tip": tip, "branch": "develop",
                "test_runner": f"{runner} (run one file with `{cmd}` from {subdir}/{service_dir})"},
       "task_type": "test_only", "tip": tip, "source_checkout": src_repo, "repo_subdir": subdir,
       "service_dir": service_dir, "shared_pkg_dir": pins.get("shared_pkg_dir", "packages/shared"),
       "shared_pkg_name": pins.get("shared_pkg_name", "@secuura/shared"),
       "test_file": tf, "test_file_rel_to_service": test_rel, "test_mode": mode, "runner": runner,
       "expected_plus": expected_plus, "must_remove": must_remove, "cells": alias,
       "tampers": tampers, "controls": controls, "files": {}}
if ttext is not None: inp["files"][tf] = ttext
if "ctx" in pins: inp["_night_num_ctx"] = int(pins["ctx"])
json.dump(inp, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(f"wrote {out}: test_only {mode} {tf} ({runner}, service {service_dir}) at {tip[:9]}; '+' {len(expected_plus)} '-' {len(must_remove)} in {hunks} hunk(s); tampers {len(tampers)} ({', '.join(t['id'] + '->' + str(len(t['reds'])) for t in tampers)}); controls {len(controls)}")
PY
