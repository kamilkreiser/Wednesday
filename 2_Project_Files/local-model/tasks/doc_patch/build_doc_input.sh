#!/bin/bash
# build_doc_input.sh <KS-id> <out input.json> <brief.md> product=<repo path> [ctx=<n>]
# Builds a doc_patch input: the file at origin/develop (read-only `git show`; refuses if the tip object is not local),
# the brief as the task text, and `defect_line.required` from the brief's `## Required` block —
#   - <section heading substring> :: token1, token2     (each token must be ABSENT in that section before, PRESENT after)
# 2026-09-15 20:0x (Kam 19:55: "see how the local agents perform on the docs"). rc 0 ok · 2 refused · 1 error.
set -uo pipefail
ID="${1:-}"; OUT="${2:-}"; BRIEF="${3:-}"; shift 3 2>/dev/null
[ -n "$ID" ] && [ -n "$OUT" ] && [ -f "$BRIEF" ] || { echo "usage: build_doc_input.sh <KS-id> <out> <brief.md> product=<path> [ctx=N]" >&2; exit 1; }
SRC="${NIGHT_SOURCE_CHECKOUT:-/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files}"
TIP="$(git -C "$SRC" ls-remote origin refs/heads/develop 2>/dev/null | awk '{print $1}')"
[ -n "$TIP" ] || { echo "build_doc_input: ls-remote returned nothing" >&2; exit 1; }
[ "$(git -C "$SRC" cat-file -t "$TIP" 2>/dev/null)" = "commit" ] || { echo "build_doc_input: REFUSED — tip $TIP not local (no fetch from here)" >&2; exit 2; }
python3 - "$ID" "$OUT" "$BRIEF" "$SRC" "$TIP" "$@" <<'PY'
import json, re, subprocess, sys
ident, out, brief, src, tip = sys.argv[1:6]
pins = dict(a.split("=",1) for a in sys.argv[6:] if "=" in a)
prod = pins.get("product") or sys.exit("build_doc_input: product= is required")
r = subprocess.run(["git","-C",src,"show",f"{tip}:{prod}"],capture_output=True,text=True)
if r.returncode: sys.stderr.write(f"build_doc_input: REFUSED — {prod} not at {tip}\n"); sys.exit(2)
text = open(brief,encoding="utf-8").read()
m = re.search(r"^##+\s*Required\b.*?$(.*?)(?=^##+\s|\Z)", text, re.M|re.S)
req = []
if m:
    for l in m.group(1).splitlines():
        l=l.strip()
        if l.startswith("- ") and "::" in l:
            sec, toks = l[2:].split("::",1)
            req.append({"section": sec.strip().strip("`"), "tokens": [t.strip().strip("`") for t in toks.split(",") if t.strip()]})
if not req: sys.stderr.write("build_doc_input: REFUSED — the brief has no `## Required` block (nothing the checker could prove)\n"); sys.exit(2)
# 2026-09-15 21:4x (KS-1097 D r2, a FALSE GREEN): the model dropped three old lines from its '-' side and the re-anchor kept them
# as context, so the applied doc carried the NEW annotation and the OLD one and D0-D6 all passed. The brief's fenced diff
# blocks name the lines that must go: every fenced line starting with '-' (not '---') is a must-remove line, asserted by D7.
must_remove=[]; readded=set()
for blk in re.findall(r"^```[^\n]*\n(.*?)^```", text, re.M|re.S):
    for ln in blk.split("\n"):
        if ln.startswith("-") and not ln.startswith("---") and ln[1:].strip():
            must_remove.append(ln[1:].rstrip())
        elif ln.startswith("+") and not ln.startswith("+++"):
            readded.add(ln[1:].rstrip())
# a whole-run replacement re-adds its unchanged lines as '+' — those are not removals (21:5x, KS-1097 B: line 457)
must_remove=[m for m in must_remove if m not in readded]
tipl=[l.rstrip() for l in r.stdout.split("\n")]
missing=[m for m in must_remove if m not in tipl]
if missing: sys.stderr.write(f"build_doc_input: REFUSED — {len(missing)} brief '-' line(s) do not exist at the tip (read the file, not the ticket): {missing[:2]}\n"); sys.exit(2)
inp = {"ticket": {"identifier": ident, "title": text.splitlines()[0].lstrip("# ").strip()[:200], "description": text},
       "repo": {"source_checkout": src, "tip": tip, "branch": "develop"},
       "product_file": prod, "defect_line": {"required": req, "must_remove": must_remove}, "files": {prod: r.stdout},
       # top-level `tip` as well: night_run.sh reads input["tip"] for the clone (20:02: absent → the good clone
       # was quarantined, `checkout ''` failed, the checker measured an empty tree)
       "tip": tip}
if "ctx" in pins: inp["_night_num_ctx"] = int(pins["ctx"])
json.dump(inp, open(out,"w",encoding="utf-8"), indent=1, ensure_ascii=False)
print(f"wrote {out}: {prod} ({len(r.stdout)} B at {tip[:9]}), required sections {len(req)}: {[x['section'] for x in req]}")
PY
