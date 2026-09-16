#!/bin/bash
# build_bash_input.sh <KS-id> <out input.json> <brief.md> product=<repo path .sh> ref=<repo path *.test.sh> [test_file=<new test path>] [ctx=<n>]
# Builds a bash_patch input (2026-09-16 00:4x — Kam 2026-09-15 18:19 "extend the checker": ~20 Backlog tickets are one-line
# fixes in scripts/ with no checker until now): the script and the reference suite at origin/develop (read-only `git show`;
# the G6 override in night/tip_override.txt is honoured exactly as build_input.sh honours it), the brief as the task text,
# and `defect_line` from the brief: `## Where` sites (must_change when the bullet carries ** and is not "(correct)"),
# expected_plus = the fenced '+' lines under `## The exact change`, must_remove = the fenced '-' lines there.
# The new test's path is `test_file=` or the brief's line `File: \`<path>\``. rc 0 ok · 2 refused · 1 error.
set -uo pipefail
ID="${1:-}"; OUT="${2:-}"; BRIEF="${3:-}"; shift 3 2>/dev/null
[ -n "$ID" ] && [ -n "$OUT" ] && [ -f "$BRIEF" ] || { echo "usage: build_bash_input.sh <KS-id> <out> <brief.md> product=<path> ref=<path> [test_file=<path>] [ctx=N]" >&2; exit 1; }
SRC="${NIGHT_SOURCE_CHECKOUT:-/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files}"
TIP="$(git -C "$SRC" ls-remote origin refs/heads/develop 2>/dev/null | awk '{print $1}')"
[ -n "$TIP" ] || { echo "build_bash_input: ls-remote returned nothing" >&2; exit 1; }
if [ "$(git -C "$SRC" cat-file -t "$TIP" 2>/dev/null)" != "commit" ]; then
  OV="$(dirname "$0")/../../night/tip_override.txt"; OV_SHA=""; OV_AGAINST=""
  [ -f "$OV" ] && read -r OV_SHA OV_AGAINST OV_REST < "$OV"
  if [ -n "$OV_SHA" ] && [ "$OV_AGAINST" = "$TIP" ] && [ "$(git -C "$SRC" cat-file -t "$OV_SHA" 2>/dev/null)" = "commit" ]; then
    echo "build_bash_input: G6 — origin develop $TIP is not local; using VERIFIED OVERRIDE $OV_SHA ($OV_REST)" >&2; TIP="$OV_SHA"
  else
    echo "build_bash_input: REFUSED — tip $TIP not local and no valid override (no fetch from here)" >&2; exit 2
  fi
fi
python3 - "$ID" "$OUT" "$BRIEF" "$SRC" "$TIP" "$@" <<'PY'
import json, re, subprocess, sys, os
ident, out, brief, src, tip = sys.argv[1:6]
pins = dict(a.split("=",1) for a in sys.argv[6:] if "=" in a)
prod = pins.get("product") or sys.exit("build_bash_input: product= is required")
ref = pins.get("ref") or sys.exit("build_bash_input: ref= is required (an existing *.test.sh whose shape the model copies)")
def show(p):
    r = subprocess.run(["git","-C",src,"show",f"{tip}:{p}"],capture_output=True,text=True)
    if r.returncode: sys.stderr.write(f"build_bash_input: REFUSED — {p} not at {tip}\n"); sys.exit(2)
    return r.stdout
def try_show(p):
    """Read p at the tip, or None if it is not there. For OPTIONAL reads only —
    a path whose absence is a legitimate state (a test file the model will create)."""
    if not p: return None
    r = subprocess.run(["git","-C",src,"show",f"{tip}:{p}"],capture_output=True,text=True)
    return None if r.returncode else r.stdout
ptext = show(prod); rtext = show(ref)
if not ref.endswith(".test.sh"): sys.stderr.write("build_bash_input: REFUSED — ref= must be a *.test.sh\n"); sys.exit(2)
text = open(brief,encoding="utf-8").read()
test_dir = os.path.dirname(ref)
tf = pins.get("test_file")
if not tf:
    m = re.search(r"^File:\s*`([^`]+\.test\.sh)`", text, re.M)
    tf = m.group(1) if m else None
if not tf: sys.stderr.write("build_bash_input: REFUSED — no test_file= pin and no `File: \\`…test.sh\\`` line in the brief\n"); sys.exit(2)
if os.path.dirname(tf) != test_dir: sys.stderr.write(f"build_bash_input: REFUSED — the new test {tf} is not beside the reference ({test_dir})\n"); sys.exit(2)
if tf == ref: sys.stderr.write("build_bash_input: REFUSED — test_file equals ref\n"); sys.exit(2)
lines = ptext.split("\n")
sites=[]
m_where = re.search(r"^##+\s*Where\b.*?$(.*?)(?=^##+\s|\Z)", text, re.M|re.S)
if m_where:
    for b in re.finditer(r"^\s*[*-]\s*`?:(\d+)`?\s*[—–-]?\s*(.*)$", m_where.group(1), re.M):
        ln=int(b.group(1)); note=b.group(2).strip()
        if not (0 < ln <= len(lines)): sys.stderr.write(f"build_bash_input: REFUSED — Where site :{ln} is outside {prod} ({len(lines)} lines)\n"); sys.exit(2)
        sites.append({"line": ln, "text_at_tip": lines[ln-1], "note": note, "must_change": ("**" in note) and ("(correct)" not in note.lower())})
expected_plus=[]; must_remove=[]
m_x = re.search(r"^##+\s*The exact change\b.*?$(.*?)(?=^##+\s|\Z)", text, re.M|re.S)
if m_x:
    for blk in re.findall(r"^```[^\n]*\n(.*?)^```", m_x.group(1), re.M|re.S):
        for ln in blk.split("\n"):
            if ln.startswith("+") and not ln.startswith("+++") and ln[1:].strip(): expected_plus.append(ln[1:].strip())
            elif ln.startswith("-") and not ln.startswith("---") and ln[1:].strip(): must_remove.append(ln[1:].rstrip())
tipl=[l.rstrip() for l in lines]
missing=[m for m in must_remove if m not in tipl]
if missing: sys.stderr.write(f"build_bash_input: REFUSED — {len(missing)} brief '-' line(s) do not exist at the tip (read the file, not the ticket): {missing[:2]}\n"); sys.exit(2)
if not expected_plus: sys.stderr.write("build_bash_input: REFUSED — the brief's `## The exact change` has no fenced '+' lines (nothing the checker could hold the script to)\n"); sys.exit(2)
# ---------------------------------------------------------------- CONTEXT-AS-ADDITION GATE (2026-09-16 15:4x)
# A '+' line is a CLAIM that the line is not in the file. When a brief's '+' set repeats a line it also
# removes, that line is CONTEXT, the model rightly emits the honest minimal hunk, and B3b/A3c then refuse
# a CORRECT output as "a dropped addition". Three instances in one day, the third written by Wednesday's
# own hand minutes after filing the rule against it: KS-1089 (06:xx), KS-1168 x2, KS-998. w=3 -> in the path.
_dup = [a for a in expected_plus if a in {m.strip() for m in must_remove}]
if _dup and os.environ.get("ALLOW_CONTEXT_AS_ADDITION") != "1":
    sys.stderr.write("build_bash_input: REFUSED — %d '+' line(s) in `## The exact change` are byte-identical to a '-' line in the same hunk, so they are CONTEXT, not additions. The model will keep them as context and B3b will refuse the correct output as a dropped addition. Rewrite the hunk minimally: a line that survives the edit gets a single leading SPACE, not a '+'. Offending: %r (ALLOW_CONTEXT_AS_ADDITION=1 overrides)\n" % (len(_dup), _dup[:3]))
    sys.exit(2)
inp = {"ticket": {"identifier": ident, "title": text.splitlines()[0].lstrip("# ").strip()[:200], "description": text},
       "repo": {"source_checkout": src, "tip": tip, "branch": "develop", "test_runner": "bash"},
       "product_file": prod, "reference_test_file": ref, "suggested_test_file": tf, "test_dir": test_dir,
       "defect_line": {"sites": sites, "expected_plus": expected_plus, "must_remove": must_remove},
       "files": {prod: ptext, ref: rtext}, "tip": tip}
# 2026-09-16 (KS-1163): a test_file= that EXISTS at the tip is a MODIFY-IN-PLACE test (the vitest tier's shape) —
# its full content goes into files[] so the model copies context byte-for-byte, and the checker's B3 accepts it.
# 2026-09-16 13:5x — this MUST be the optional read: `show()` EXITS on a missing path, and the whole point of the
# default (NEW test) mode is a test_file that is NOT at the tip. Written as `show(tf)` it made the new-test path
# unreachable — build_bash_input refused KS-1011 with "not at <tip>" for a file it was being asked to create.
ttext = try_show(tf)
if ttext is not None:
    inp["files"][tf] = ttext; inp["test_mode"] = "modify"
    sys.stderr.write(f"build_bash_input: test_file EXISTS at the tip — MODIFY-IN-PLACE ({len(ttext)} B in files[])\n")
if "ctx" in pins: inp["_night_num_ctx"] = int(pins["ctx"])
json.dump(inp, open(out,"w",encoding="utf-8"), indent=1, ensure_ascii=False)
print(f"wrote {out}: {prod} ({len(ptext)} B) + ref {ref} ({len(rtext)} B) at {tip[:9]}; sites {len(sites)} ({sum(1 for s in sites if s['must_change'])} must_change); expected '+' {len(expected_plus)}; must_remove {len(must_remove)}; new test {tf}")
PY
