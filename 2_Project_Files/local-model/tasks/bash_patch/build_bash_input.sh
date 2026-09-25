#!/bin/bash
# build_bash_input.sh <KS-id> <out input.json> <brief.md> product=<repo path .sh> ref=<repo path *.test.sh> [test_file=<new test path>] [ctx=<n>]
# Builds a bash_patch input (2026-09-16 00:4x — Kam 2026-09-15 18:19 "extend the checker": ~20 Backlog tickets are one-line
# fixes in scripts/ with no checker until now): the script and the reference suite at origin/develop (read-only `git show`;
# the G6 override in night/tip_override.txt is honoured exactly as build_input.sh honours it), the brief as the task text,
# and `defect_line` from the brief: `## Where` sites (must_change when the bullet carries ** and is not "(correct)"),
# expected_plus = the fenced '+' lines under `## The exact change`, must_remove = the fenced '-' lines there.
# The new test's path is `test_file=` or the brief's line `File: \`<path>\``. rc 0 ok · 2 refused · 1 error.
# 2026-09-26 SELF-TESTING (KS-766 first): a brief with a `## Self-testing … test hunks: N[,M] …` heading (trailing words
# after the ordinals are tolerated, e.g. `## Self-testing: test hunks: 2 (the middle one)`) builds a ONE-file input: the
# product .sh carries its own suite and runs it via `Runner: \`bash <product> --self-test\``. No ref= / test_file= then;
# product= defaults to the brief's `File: \`<path>.sh\`` line. Declared in input.self_testing: test_hunks, runner,
# red_rc / green_rc (pins red_rc= green_rc=, else the brief's `RED (exit N)` / `GREEN (exit N)`), line_regex (pin
# lines=, else the brief's `Lines: \`<re>\``, else `^\s+(PASS|FAIL)\b`; group 1 is PASS or FAIL), and golden_diff +
# golden_sha256 (pin golden=, else `golden.diff` beside the brief). `## Red cells` bullets -> defect_line.red_cells.
# The context-as-addition gate is HUNK-AWARE in this mode (a line MOVED between hunks is not context).
# checker.sh runs this mode in a `git archive` scratch tree. Arms: tests/bash_selftest_arms.sh.
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
text = open(brief,encoding="utf-8").read()
_ms = re.search(r"^##+\s*Self-testing\b[^\n]*?test hunks?\s*:\s*([0-9]+(?:\s*,\s*[0-9]+)*)", text, re.M | re.I)
SELFTEST = bool(_ms)
prod = pins.get("product")
if not prod and SELFTEST:
    _mf = re.search(r"^File:\s*`([^`]+\.sh)`", text, re.M)
    prod = _mf.group(1) if _mf else None
prod = prod or sys.exit("build_bash_input: product= is required")
ref = pins.get("ref") or ("" if SELFTEST else sys.exit("build_bash_input: ref= is required (an existing *.test.sh whose shape the model copies)"))
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
ptext = show(prod)
if SELFTEST:
    if not prod.endswith(".sh"): sys.stderr.write(f"build_bash_input: REFUSED — self-testing product {prod} is not a .sh script\n"); sys.exit(2)
    if ref or pins.get("test_file"): sys.stderr.write("build_bash_input: REFUSED — `## Self-testing` is ONE file: no ref= / test_file= (the product carries its own suite)\n"); sys.exit(2)
    rtext = None; test_dir = os.path.dirname(prod); tf = prod
else:
    rtext = show(ref)
    if not ref.endswith(".test.sh"): sys.stderr.write("build_bash_input: REFUSED — ref= must be a *.test.sh\n"); sys.exit(2)
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
if SELFTEST and m_x:
    # HUNK-AWARE in self-testing mode (2026-09-26, KS-766): a self-testing fix may MOVE a block from one hunk into a new
    # function in another — each moved line is then a '-' in one hunk and a '+' in another, which is not context. Only a
    # '+' that repeats a '-' of the SAME hunk is context-as-addition.
    _dup = []
    for blk in re.findall(r"^```[^\n]*\n(.*?)^```", m_x.group(1), re.M|re.S):
        for h in re.split(r"^(?=@@ )", blk, flags=re.M):
            hm = {l[1:].strip() for l in h.split("\n") if l.startswith("-") and not l.startswith("---") and l[1:].strip()}
            _dup += [l[1:].strip() for l in h.split("\n") if l.startswith("+") and not l.startswith("+++") and l[1:].strip() in hm]
if _dup and os.environ.get("ALLOW_CONTEXT_AS_ADDITION") != "1":
    sys.stderr.write("build_bash_input: REFUSED — %d '+' line(s) in `## The exact change` are byte-identical to a '-' line in the same hunk, so they are CONTEXT, not additions. The model will keep them as context and B3b will refuse the correct output as a dropped addition. Rewrite the hunk minimally: a line that survives the edit gets a single leading SPACE, not a '+'. Offending: %r (ALLOW_CONTEXT_AS_ADDITION=1 overrides)\n" % (len(_dup), _dup[:3]))
    sys.exit(2)
if SELFTEST:
    import hashlib, shlex
    _th = sorted({int(x) for x in re.split(r"[,\s]+", _ms.group(1).strip()) if x})
    if not _th or min(_th) < 1: sys.stderr.write(f"build_bash_input: REFUSED — `## Self-testing` test hunk ordinals must be 1-based integers: {_ms.group(1)!r}\n"); sys.exit(2)
    _mr = re.search(r"^Runner:\s*`([^`]+)`", text, re.M)
    runner = pins.get("runner") or (_mr.group(1) if _mr else None)
    if not runner: sys.stderr.write("build_bash_input: REFUSED — self-testing needs a `Runner: \\`bash <product> --self-test\\`` line (or runner=)\n"); sys.exit(2)
    _rv = shlex.split(runner)
    if len(_rv) < 2 or _rv[0] != "bash" or _rv[1] != prod: sys.stderr.write(f"build_bash_input: REFUSED — the runner must be `bash {prod} <args>`, got {runner!r}\n"); sys.exit(2)
    _sec = re.search(r"^##+\s*Self-testing\b.*?$(.*?)(?=^##+\s|\Z)", text, re.M|re.S).group(0)
    def _rc(key, word):
        if key in pins: return int(pins[key]), "pin"
        m = re.search(word + r"\W{0,4}\(exit\s+(\d+)\)", _sec)
        return (int(m.group(1)), "brief") if m else (None, None)
    red_rc, red_src = _rc("red_rc", "RED"); green_rc, green_src = _rc("green_rc", "GREEN")
    if red_rc is None or green_rc is None: sys.stderr.write(f"build_bash_input: REFUSED — the expected RED/GREEN exit codes are not declared (red_rc={red_rc} green_rc={green_rc}; pin red_rc= green_rc= or write `RED (exit N)` / `GREEN (exit N)` under `## Self-testing`)\n"); sys.exit(2)
    if red_rc == green_rc: sys.stderr.write(f"build_bash_input: REFUSED — RED and GREEN exit codes are both {red_rc}: the split could not tell them apart\n"); sys.exit(2)
    _ml = re.search(r"^Lines:\s*`([^`]+)`", text, re.M)
    line_regex = pins.get("lines") or (_ml.group(1) if _ml else r"^\s+(PASS|FAIL)\b")
    try:
        if re.compile(line_regex).groups < 1: raise ValueError("no capture group")
    except Exception as e: sys.stderr.write(f"build_bash_input: REFUSED — line regex {line_regex!r}: {e} (group 1 must capture PASS or FAIL)\n"); sys.exit(2)
    m_rc = re.search(r"^##+\s*Red cells\b.*?$(.*?)(?=^##+\s|\Z)", text, re.M|re.S)
    red_cells = [b.strip().strip("`") for b in re.findall(r"^\s*[*-]\s+(.+?)\s*$", m_rc.group(1), re.M)] if m_rc else []
    if not red_cells: sys.stderr.write("build_bash_input: REFUSED — `## Self-testing` needs a `## Red cells` section (the split cross-checks the declared test hunk carries each cell)\n"); sys.exit(2)
    golden = pins.get("golden") or os.path.join(os.path.dirname(os.path.abspath(brief)), "golden.diff")
    golden = os.path.abspath(golden) if os.path.isfile(golden) else None
    if pins.get("golden") and not golden: sys.stderr.write(f"build_bash_input: REFUSED — golden={pins['golden']} is not a file\n"); sys.exit(2)
    inp = {"ticket": {"identifier": ident, "title": text.splitlines()[0].lstrip("# ").strip()[:200], "description": text},
           "repo": {"source_checkout": src, "tip": tip, "branch": "develop", "test_runner": "bash-self-test"},
           "product_file": prod, "test_dir": test_dir,
           "defect_line": {"sites": sites, "expected_plus": expected_plus, "must_remove": must_remove, "red_cells": red_cells},
           "self_testing": {"test_hunks": _th, "runner": runner, "red_rc": red_rc, "green_rc": green_rc, "line_regex": line_regex,
                            "golden_diff": golden, "golden_sha256": hashlib.sha256(open(golden,"rb").read()).hexdigest() if golden else None,
                            "rule": "SELF-TESTING: the product script carries its own suite (`" + runner + "`). Emit ONE diff section for it and "
                                    "NOTHING else; hunk(s) " + ",".join(str(k) for k in _th) + " (counting from the top of the section) add the "
                                    "self-test checks and must make the self-test exit " + str(red_rc) + " ALONE at the tip; every other hunk is the "
                                    "fix and turns it to exit " + str(green_rc) + ". Keep the hunks in the brief's order, in file order."},
           "files": {prod: ptext}, "tip": tip}
    json.dump(inp, open(out,"w",encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"  prompt source: WEDNESDAY BRIEF {os.path.abspath(brief)} ({len(text)} chars) — the ticket description is NOT the prompt")
    print(f"wrote {out}: SELF-TESTING {prod} ({len(ptext)} B) at {tip[:9]}; test hunk(s) {_th}; runner `{runner}`; red rc {red_rc} ({red_src}) / green rc {green_rc} ({green_src}); lines {line_regex!r}; red cells {len(red_cells)}; sites {len(sites)} ({sum(1 for s in sites if s['must_change'])} must_change); expected '+' {len(expected_plus)}; must_remove {len(must_remove)}; golden {golden or 'none'}")
    sys.exit(0)
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
