#!/bin/bash
# build_input2.sh <KS-id> <out input.json> <brief.md> [pin=value ...] — the code_patch2 (multi-file) input (2026-10-05).
#
# night/build_input.sh builds ONE code_patch input (one product= pin). This wrapper runs it UNCHANGED for the brief's
# FIRST product file (every gate it has — Linear state, open PRs, the brief as prompt, red cells, expected '+' lines,
# fence shape — still runs), then adds what code_patch2 needs:
#   task_type      "code_patch2"
#   product_files  every header `File:` line (1-3), in brief order
#   test_files     every header `Test …:` line (1-2), each [{"path", "status": "new"|"modified"}] by `git cat-file -e
#                  <tip>:<path>` on the source checkout (a READ verb)
#   files[...]     each further product and each modified test at the tip: whole when <= NIGHT_EXCERPT_TRIGGER_BYTES
#                  (160000, build_input.sh's own ceiling); larger ones as build_input.sh's excerpt OBJECT shape
#                  ({excerpt, total_lines, total_bytes, carried_bytes, regions[{first_line,last_line,text}], rule}) with
#                  regions = the file's head + the old side of every brief hunk naming that file +- 25 lines, and
#                  excerpt_rule / excerpted_files set exactly as build_input.sh sets them.
#   reference_test_note  prefixed with the declared file list.
# REFUSES (rc 2): products outside 1-3 or tests outside 1-2; files not all under ONE service dir (A6/A7 measure one
# service); a test not under the input's test_dir; a declared product missing at the tip; a declared NEW test already
# present; a modified test missing. rc 0 ok · 2 refused · 1 error (builder rc passes through). Writes only <out>.
# bash 3.2; stderr never discarded; read verbs only on the source checkout.
set -uo pipefail
ID="${1:-}"; OUT="${2:-}"; BRIEF="${3:-}"; shift 3 2>/dev/null
[ -n "$ID" ] && [ -n "$OUT" ] && [ -f "$BRIEF" ] || { echo "usage: build_input2.sh <KS-id> <out> <brief.md> [pin=value ...]" >&2; exit 1; }
HERE="$(cd "$(dirname "$0")" && pwd)"; LM="$(dirname "$(dirname "$HERE")")"
FIRST="$(python3 -c 'import re,sys; h=re.split(r"(?m)^##\s", open(sys.argv[1],encoding="utf-8").read(), maxsplit=1)[0]; m=re.findall(r"(?m)^File:\s*`([^`]+)`", h); print(m[0] if m else "")' "$BRIEF")"
[ -n "$FIRST" ] || { echo "build_input2: REFUSED — the brief header has no File: line" >&2; exit 2; }
PINS=(); HAVE_PRODUCT=0
for a in "$@"; do case "$a" in product=*) HAVE_PRODUCT=1;; esac; PINS+=("$a"); done
[ "$HAVE_PRODUCT" -eq 1 ] || PINS+=("product=$FIRST")
bash "$LM/night/build_input.sh" "$ID" "$OUT" "${PINS[@]}"; RC=$?
[ "$RC" -eq 0 ] || exit "$RC"
LM_DIR="$LM" python3 - "$OUT" "$BRIEF" <<'PY'
import json, os, re, subprocess, sys
out, brief = sys.argv[1:3]
d = json.load(open(out, encoding="utf-8"))
text = open(brief, encoding="utf-8").read()
header = re.split(r"(?m)^##\s", text, maxsplit=1)[0]
products = re.findall(r"(?m)^File:\s*`([^`]+)`", header)
tests = re.findall(r"(?im)^Test[^:\n`]*:\s*`([^`]+)`", header)
repo = d.get("repo") or {}
src = d.get("source_checkout") or repo.get("source_checkout"); tip = d.get("tip") or repo.get("tip")
subdir = d.get("repo_subdir") or repo.get("repo_subdir") or "Blockchain/Dev"
service = d.get("service_dir") or repo.get("service_dir")
test_dir = d.get("test_dir") or ""
def refuse(m): sys.stderr.write(f"build_input2: REFUSED — {m}\n"); sys.exit(2)
def full(p): return p if p.startswith(subdir + "/") else f"{subdir}/{p}"
products = [full(p) for p in products]; tests = [full(t) for t in tests]
if not (1 <= len(products) <= 3): refuse(f"{len(products)} product file(s) declared; code_patch2 takes 1-3")
if not (1 <= len(tests) <= 2): refuse(f"{len(tests)} test file(s) declared; code_patch2 takes 1-2")
svc_root = f"{subdir}/{service}/"
outside = [p for p in products + tests if not p.startswith(svc_root)]
if outside: refuse(f"not under the ONE service {svc_root} (A6/A7 measure one service): {outside}")
bad_t = [t for t in tests if test_dir and not t.startswith(test_dir.rstrip("/") + "/")]
if bad_t: refuse(f"test file(s) not under test_dir {test_dir}: {bad_t}")
def at_tip(p): return subprocess.run(["git", "-C", src, "cat-file", "-e", f"{tip}:{p}"], capture_output=True).returncode == 0
def show(p): return subprocess.run(["git", "-C", src, "show", f"{tip}:{p}"], capture_output=True, text=True).stdout
for p in products:
    if not at_tip(p): refuse(f"declared product {p} is not at the tip {tip[:12]}")
tlist = []
new_line = {full(m.group(1)): bool(re.search(r"\bNEW\b", m.group(2))) for m in re.finditer(r"(?im)^Test[^:\n`]*:\s*`([^`]+)`([^\n]*)", header)}
for t in tests:
    st = "modified" if at_tip(t) else "new"
    if new_line.get(t) and st == "modified": refuse(f"{t} is declared NEW but already exists at the tip")
    tlist.append({"path": t, "status": st})
sugg = d.get("suggested_test_file") or ""
if sugg and sugg not in tests: refuse(f"the builder's suggested_test_file {sugg} is not among the declared tests {tests}")
TRIG = int(os.environ.get("NIGHT_EXCERPT_TRIGGER_BYTES", "160000"))
MARGIN, HEAD = 25, 60
RULE = None
files = d.setdefault("files", {})
# old-side spans per file from the brief's own diff blocks (`--- a/<path>` then `@@ -a,b`)
spans = {}
cur = None
for ln in text.split("\n"):
    m = re.match(r"^--- a/(\S+)", ln)
    if m: cur = m.group(1); continue
    m = re.match(r"^@@ -(\d+)(?:,(\d+))? ", ln)
    if m and cur:
        a = int(m.group(1)); b = int(m.group(2) or 1); spans.setdefault(cur, []).append((a, a + max(b, 1) - 1))
excerpted = list(d.get("excerpted_files") or [])
for p in products[1:] + [t["path"] for t in tlist if t["status"] == "modified"]:
    if p in files: continue
    body = show(p)
    if len(body) <= TRIG:
        files[p] = body; print(f"  code_patch2: carried {p} whole ({len(body)} B)"); continue
    fl = body.split("\n"); n = len(fl)
    want = [(1, min(HEAD, n))] + [(max(1, a - MARGIN), min(n, b + MARGIN)) for a, b in spans.get(p, [])]
    if len(want) == 1: refuse(f"{p} is {len(body)} B (> {TRIG}) and the brief carries no hunk for it — no region can be determined")
    want.sort(); merged = []
    for a, b in want:
        if merged and a <= merged[-1][1] + 10: merged[-1] = (merged[-1][0], max(b, merged[-1][1]))
        else: merged.append((a, b))
    regions = [{"first_line": a, "last_line": b, "text": "\n".join(fl[a - 1:b])} for a, b in merged]
    carried = sum(len(r["text"]) for r in regions)
    if RULE is None:
        # build_input.sh's own rule text, read from the builder (never re-worded here)
        bi = open(os.path.join(os.environ["LM_DIR"], "night", "build_input.sh"), encoding="utf-8").read()
        m = re.search(r'_EXCERPT_RULE = \(\n(.*?)\n\)\n', bi, re.S)
        RULE = "".join(re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(1))) if m else None
        if not RULE: refuse("could not read _EXCERPT_RULE from night/build_input.sh (the excerpt contract) — not guessing it")
    files[p] = {"excerpt": True, "total_lines": n, "total_bytes": len(body), "carried_bytes": carried, "regions": regions,
                "rule": RULE, "why": f"code_patch2: {p} is {len(body)} B; only the head and the brief's hunks (+-{MARGIN}) are carried"}
    excerpted.append(p)
    print(f"  code_patch2: EXCERPTED {p}: {len(body)} B / {n} lines -> {carried} B in {len(regions)} region(s) {[(r['first_line'], r['last_line']) for r in regions]}")
if excerpted:
    d["excerpt_rule"] = RULE or d.get("excerpt_rule"); d["excerpted_files"] = excerpted
d["task_type"] = "code_patch2"
d["product_files"] = products
d["test_files"] = tlist
decl = ("CODE_PATCH2 (multi-file): your diff touches EXACTLY these files and no other - products: "
        + ", ".join(products) + "; tests: " + ", ".join(f"{t['path']} ({t['status']})" for t in tlist) + ". ")
d["reference_test_note"] = decl + (d.get("reference_test_note") or "")
json.dump(d, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(f"code_patch2: product_files={len(products)} test_files={[(t['path'].rsplit('/',1)[-1], t['status']) for t in tlist]} -> {out} ({os.path.getsize(out)} B)")
PY
