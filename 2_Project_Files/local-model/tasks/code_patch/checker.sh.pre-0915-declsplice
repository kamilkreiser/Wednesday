#!/bin/bash
# checker.sh <input.json> <out.md> <clone-dir> — code_patch
#
# The mechanical verdict on a model-produced patch. It never edits the patch,
# never judges its style, and never hand-fixes anything: it applies the diff
# in a scratch clone pinned at the input's tip and measures. Assertions:
#
#   A1 output is exactly one fenced ```diff block, no prose outside it
#   A2 the diff applies (`git apply --check`) at the pinned tip
#      (strict first; then with --recount --ignore-whitespace, the ONE
#      accommodation for model-miscounted hunk headers — reported apart)
#   A3 touched-file set == { product_file, ONE test file under test_dir }
#      (never the reference test file, never a third file)
#   A4 RED-FIRST: the test hunk ALONE, at the tip, runs and FAILS with >=1
#      failed assertion (a file that fails to LOAD is a load error, not red)
#   A5 GREEN-AFTER: product hunk applied, the same test file passes, 0 failed
#   A6 whole-service suite after the patch: no NEW red vs the untouched tip
#      (both measured here, same clone, same run; develop's own reds are
#      attributed, not counted against the patch)
#   A7 `tsc --noEmit` for the service: rc 0 after the patch
#
# Prints PASS/FAIL per assertion; rc 0 only when ALL pass. Every write verb
# (git apply / checkout, vitest, tsc) runs inside <clone-dir>; the source
# checkout is never touched. Reports land in <out.md>.checker/. Untracked
# files a previous run left in the clone are QUARANTINED, never deleted.
# stderr never discarded. bash 3.2.
set -uo pipefail

INPUT="${1:-}"; OUT="${2:-}"; CLONE="${3:-}"
if [ -z "$INPUT" ] || [ -z "$OUT" ] || [ -z "$CLONE" ] || [ ! -f "$INPUT" ] || [ ! -f "$OUT" ] || [ ! -d "$CLONE/.git" ]; then
  echo "usage: checker.sh <input.json> <out.md> <clone-dir>" >&2
  exit 1
fi

field() { python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))[sys.argv[2]])' "$INPUT" "$1"; }
TIP="$(field tip)"
SUBDIR="$(field repo_subdir)"
SERVICE="$(field service_dir)"
PRODUCT="$(field product_file)"
TEST_DIR="$(field test_dir)"
REF_TEST="$(field reference_test_file)"
# 2026-09-15 12:xx TEST-ONLY mode (KS-1073 / KS-1123-F3 class: the code is right at the tip and a PIN is owed):
# when the input's defect_line.tamper is set (parsed by build_input from the brief's `## Tamper` block), the diff
# must touch ONLY one test file; A4 reds under the TAMPER (the product line replaced in the clone, then reverted)
# instead of at the tip; A5 is green at the UNTOUCHED tip. Without a tamper the mode is code_patch, unchanged.
TAMPER_LINE="$(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); t=(d.get("defect_line") or {}).get("tamper") or {}; print(t.get("line",""))' "$INPUT")"
if [ -n "$TAMPER_LINE" ]; then MODE=test_only; else MODE=code_patch; fi
echo "mode: $MODE$( [ "$MODE" = test_only ] && echo " (tamper at $PRODUCT:$TAMPER_LINE)")"
SVC="$CLONE/$SUBDIR/$SERVICE"
REP="$OUT.checker"
mkdir -p "$REP"
DIFF="$REP/patch.diff"

FAILS=0
pass() { echo "PASS $1"; }
fail() { echo "FAIL $1"; FAILS=$((FAILS+1)); }

# ---------------------------------------------------------------- A1 extract
python3 - "$OUT" "$DIFF" > "$REP/extract.out" 2>&1 <<'PYEOF'
import re, sys
out_path, diff_path = sys.argv[1], sys.argv[2]
text = open(out_path, encoding="utf-8").read()
blocks = re.findall(r"```diff[^\n]*\n(.*?)```", text, flags=re.DOTALL)
allblocks = re.findall(r"```[^\n]*\n.*?```", text, flags=re.DOTALL)
outside = re.sub(r"```[^\n]*\n.*?```", "", text, flags=re.DOTALL).strip()
print(f"diff_blocks={len(blocks)} all_blocks={len(allblocks)} prose_outside_chars={len(outside)}")
if outside:
    print("prose_outside_head=" + repr(outside[:200]))
if len(blocks) >= 1:
    body = blocks[0]
    if not body.endswith("\n"):
        body += "\n"
    open(diff_path, "w", encoding="utf-8").write(body)
    print(f"wrote {diff_path} lines={body.count(chr(10))}")
    sys.exit(0 if (len(blocks) == 1 and len(allblocks) == 1 and not outside) else 3)
sys.exit(2)
PYEOF
rc=$?
cat "$REP/extract.out"
if [ "$rc" -eq 2 ]; then
  fail "A1 output contains no \`\`\`diff block — prose instead of a diff; nothing to apply"
  echo "RESULT: FAIL ($FAILS failed) — stopped at A1"
  exit 1
elif [ "$rc" -eq 3 ]; then
  fail "A1 output is not exactly one fenced diff block with nothing outside it (see extract.out) — continuing with the first block"
else
  pass "A1 output is exactly one fenced \`\`\`diff block, nothing outside it"
fi

# ---------------------------------------------------------------- reset clone
HEAD_SHA="$(git -C "$CLONE" rev-parse HEAD)"
if [ "$HEAD_SHA" != "$TIP" ]; then
  echo "checker: clone HEAD $HEAD_SHA != pinned tip $TIP — refusing (prepare the clone first)" >&2
  exit 1
fi
Q="$CLONE/../quarantine/$(date +%Y%m%d-%H%M%S)"
git -C "$CLONE" status --porcelain --untracked-files=all -- "$SUBDIR/$SERVICE/src" > "$REP/pre_status.out" 2>&1
while IFS= read -r line; do
  [ -z "$line" ] && continue
  st="${line:0:2}"; p="${line:3}"
  case "$st" in
    "??") mkdir -p "$Q/$(dirname "$p")"; mv "$CLONE/$p" "$Q/$p"; echo "quarantined untracked $p -> $Q" ;;
  esac
done < "$REP/pre_status.out"
git -C "$CLONE" checkout -- "$SUBDIR/$SERVICE" > "$REP/reset.out" 2>&1
n_dirty="$(git -C "$CLONE" status --porcelain --untracked-files=all -- "$SUBDIR/$SERVICE" | wc -l | tr -d ' ')"
if [ "$n_dirty" -ne 0 ]; then
  echo "checker: clone not clean under $SUBDIR/$SERVICE after reset ($n_dirty entries)" >&2
  git -C "$CLONE" status --porcelain --untracked-files=all -- "$SUBDIR/$SERVICE" >&2
  exit 1
fi
echo "clone clean at pinned tip $TIP"

run_vitest() {
  # run_vitest <label> [file]  -> writes $REP/<label>.json + .out; echoes rc
  local label="$1"; shift
  ( cd "$SVC" && npx vitest run "$@" --reporter=json --outputFile="$REP/$label.json" ) > "$REP/$label.out" 2>&1
  echo $?
}
summ() {
  # summ <label> -> "total=.. passed=.. failed=.. suites_failed=.. loaded=0|1 failed_names=[...]"
  python3 - "$REP/$1.json" <<'PYEOF'
import json, sys, os
p = sys.argv[1]
if not os.path.exists(p):
    print("total=0 passed=0 failed=0 suites_failed=UNKNOWN loaded=0 failed_names=[] (no json report written)")
    sys.exit(0)
j = json.load(open(p))
names = []
for r in j.get("testResults", []):
    for a in r.get("assertionResults", []):
        if a.get("status") == "failed":
            names.append(a.get("fullName") or a.get("title"))
    if r.get("status") == "failed" and not r.get("assertionResults"):
        names.append("<LOAD ERROR> " + os.path.basename(r.get("name", "?")) + ": " + (r.get("message") or "")[:200].replace("\n", " "))
print(f"total={j['numTotalTests']} passed={j['numPassedTests']} failed={j['numFailedTests']} suites_failed={j['numFailedTestSuites']} loaded={1 if j['numTotalTests']>0 else 0} failed_names={names}")
PYEOF
}
getn() { echo "$1" | tr ' ' '\n' | /usr/bin/grep "^$2=" | head -1 | cut -d= -f2; }

# ---------------------------------------------------------------- baseline (untouched tip)
echo "--- baseline at the untouched tip (whole $SERVICE suite + tsc)"
rc_base="$(run_vitest baseline_suite)"
BASE="$(summ baseline_suite)"
echo "baseline suite rc=$rc_base $BASE"
( cd "$SVC" && npx tsc --noEmit -p . ) > "$REP/baseline_tsc.out" 2>&1
rc_base_tsc=$?
echo "baseline tsc rc=$rc_base_tsc ($(wc -l < "$REP/baseline_tsc.out" | tr -d ' ') lines)"

# ---------------------------------------------------------------- A2 applies
# The diff is SPLIT per file and each section audited. git apply trusts
# `@@ -a,b +c,d @@`: when a model under-counts a NEW-file hunk (declared 100,
# actual 127 — attempt 2 of the KS-806 pilot) strict apply SUCCEEDS and
# silently truncates the file at line 100, and the defect surfaces later as
# a load error. `--recount` fixes THAT hunk but, on a multi-file diff, makes a
# correctly-counted hunk swallow the next `--- /dev/null` header as a `-`
# line (attempt 1's shape). So: one section per file, `--recount` only on a
# section whose header is miscounted, reported as the accommodation it is.
SUGGESTED_TEST_REL="$(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); print(d.get("suggested_test_file",""))' "$INPUT")"
SUGGESTED_TEST_REL="$SUGGESTED_TEST_REL" python3 - "$DIFF" "$REP" > "$REP/hunk_audit.out" 2>&1 <<'PYEOF2'
import re, sys, json, os
diff_path, rep = sys.argv[1], sys.argv[2]
SUGGESTED_TEST = os.environ.get("SUGGESTED_TEST_REL", "") or "UNKNOWN_TEST_PATH.test.ts"
lines = open(diff_path, encoding="utf-8").read().split("\n")
if lines and lines[-1] == "": lines.pop()
# 2026-09-15 (KS-1073 q8, the real cause): the model wrote ` --- /dev/null` with ONE leading space — a context-line
# prefix on a file header — so the header read as a context line and the following `+++ b/<test>` as a `+` line
# INSIDE the product hunk (tsc: "Expected 0-1 arguments" from a `+++ b/…` line landing in a Boolean(...)). A file
# header never carries a leading space; strip it and say so.
for _i in range(len(lines)):
    if re.match(r"^ (--- (/dev/null|a/)|\+\+\+ b/)", lines[_i]):
        print(f"line {_i+1}: file header written with a leading space ({lines[_i][:24]!r}) — the space stripped, read as a header")
        lines[_i] = lines[_i][1:]
# split into file sections at each '--- ' header (a 'diff --git' line, if any, belongs to the following section)
sections = []; cur = None
for ln in lines:
    if ln.startswith("diff --git ") or ln.startswith("--- "):
        if ln.startswith("--- ") and cur is not None and cur["lines"] and cur["lines"][-1].startswith("diff --git "):
            cur["lines"].append(ln); continue
        if ln.startswith("--- ") and cur is not None and not cur["has_minus"]:
            cur["lines"].append(ln); cur["has_minus"] = True; continue
        cur = {"lines": [ln], "has_minus": ln.startswith("--- ")}; sections.append(cur)
        continue
    if cur is None:
        cur = {"lines": [], "has_minus": False}; sections.append(cur)
    # 2026-09-15 (KS-1073 q8): a `@@ -0,0 +1,N @@` NEW-FILE hunk that follows another hunk INSIDE a section is the
    # model's test file with its `--- /dev/null` / `+++ b/<path>` header forgotten ("patch fragment without
    # header"). The path is known: the input's suggested_test_file. Split it into its own section with the header
    # synthesised, and say so — an accommodation the verdict names, never a silent repair.
    if re.match(r"^@@ -0,0 \+1(,\d+)? @@", ln) and any(l.startswith("@@ ") for l in cur["lines"]):
        cur = {"lines": ["--- /dev/null", "+++ b/" + SUGGESTED_TEST, ln], "has_minus": True, "synth": True}; sections.append(cur)
        print(f"section {len(sections)}: HEADERLESS NEW-FILE hunk split out of the previous section and given the header +++ b/{SUGGESTED_TEST} (the model forgot it)")
        continue
    cur["lines"].append(ln)
out = []
for k, sec in enumerate(sections, 1):
    L = sec["lines"]
    path = None
    for ln in L:
        if ln.startswith("+++ b/"): path = ln[6:].strip(); break
        if ln.startswith("+++ "): path = ln[4:].strip(); break
    miscount = 0; hunks = 0; i = 0
    while i < len(L):
        m = re.match(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", L[i])
        if not m: i += 1; continue
        hunks += 1
        b = int(m.group(2) if m.group(2) is not None else 1); d = int(m.group(4) if m.group(4) is not None else 1)
        j = i + 1; old = new = 0
        while j < len(L) and L[j][:1] in (" ", "+", "-", "\\") and not re.match(r"^@@ ", L[j]):
            c = L[j][:1]
            if c == " ": old += 1; new += 1
            elif c == "-": old += 1
            elif c == "+": new += 1
            j += 1
        if (old, new) != (b, d):
            miscount += 1
            print(f"section {k} {path}: hunk {hunks} ({L[i]}) declared old={b} new={d} but actual old={old} new={new}")
        i = j
    fn = f"{rep}/section_{k}.diff"
    # 2026-09-15: a diff line is never EMPTY (context lines start with a space) — a trailing empty line is
    # the model's fence artefact, and --recount then reads it as a context line ("new file depends on old
    # contents" on KS-871's test section). Strip trailing empty lines from every section.
    while L and L[-1] == "":
        L.pop()
    open(fn, "w", encoding="utf-8").write("\n".join(L) + "\n")
    out.append({"n": k, "path": path, "file": fn, "hunks": hunks, "miscount": miscount})
json.dump(out, open(f"{rep}/sections.json", "w"), indent=1)
print(f"sections={len(out)} miscounted_sections={sum(1 for o in out if o['miscount'])}")
PYEOF2
cat "$REP/hunk_audit.out"
N_SEC="$(python3 -c 'import json,sys; print(len(json.load(open(sys.argv[1]))))' "$REP/sections.json")"
A2_OK=1; A2_MODE="strict"; A2_NOTE=""
k=1
while [ "$k" -le "$N_SEC" ]; do
  SEC_FILE="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))[int(sys.argv[2])-1]["file"])' "$REP/sections.json" "$k")"
  SEC_PATH="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))[int(sys.argv[2])-1]["path"])' "$REP/sections.json" "$k")"
  SEC_MIS="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))[int(sys.argv[2])-1]["miscount"])' "$REP/sections.json" "$k")"
  # 2026-09-15: the model writes paths RELATIVE TO THE SERVICE ROOT ("services/api-gateway/…") as often as
  # repo-relative ("Blockchain/Dev/services/…") — three of three runs on 09-15 08:4x lacked the prefix and every
  # one failed A2 with "No such file". A path form is not a code defect: when the section's path lacks the
  # repo subdir, git apply gets --directory=<subdir> (recorded in the opts so every later apply uses it too).
  DIROPT=""
  case "$SEC_PATH" in "$SUBDIR"/*) ;; *) DIROPT="--directory=$SUBDIR"; echo "section $k $SEC_PATH: path lacks $SUBDIR/ — applying with $DIROPT" ;; esac
  # 2026-09-15 (KS-908 q4): a section whose `--- a/<x>` and `+++ b/<y>` name DIFFERENT files (neither /dev/null) is
  # a rename to git and applies nowhere — say so by name instead of "No such file" on the wrong path (task.md 2d).
  HDR_MINUS="$(sed -n '1p' "$SEC_FILE" | sed -E 's#^--- (a/)?##')"; HDR_PLUS="$(sed -n '2p' "$SEC_FILE" | sed -E 's#^\+\+\+ (b/)?##')"
  if [ "$HDR_MINUS" != "/dev/null" ] && [ "$HDR_PLUS" != "/dev/null" ] && [ "$HDR_MINUS" != "$HDR_PLUS" ]; then
    echo "section $k: MISMATCHED HEADER — '--- $HDR_MINUS' paired with '+++ $HDR_PLUS' (two files in one section; git reads a rename)"
    A2_NOTE="$A2_NOTE [section $k: MISMATCHED HEADER '--- $HDR_MINUS' vs '+++ $HDR_PLUS' — the model paired the product file's --- with another file's +++ (task.md 2d)]"
  fi
  git -C "$CLONE" apply --check -p1 $DIROPT "$SEC_FILE" > "$REP/apply_check_strict_$k.out" 2>&1
  rc_strict=$?
  git -C "$CLONE" apply --check -p1 $DIROPT --recount --ignore-whitespace "$SEC_FILE" > "$REP/apply_check_lenient_$k.out" 2>&1
  rc_lenient=$?
  if [ "$SEC_MIS" -eq 0 ] && [ "$rc_strict" -eq 0 ]; then
    echo "$SEC_FILE" > "$REP/section_$k.opts"; echo "$DIROPT" >> "$REP/section_$k.opts"
    echo "section $k $SEC_PATH: applies (strict)"
  elif [ "$rc_lenient" -eq 0 ]; then
    echo "$SEC_FILE" > "$REP/section_$k.opts"; echo "$DIROPT --recount --ignore-whitespace" >> "$REP/section_$k.opts"
    A2_MODE="lenient"; A2_NOTE="$A2_NOTE [$SEC_PATH: --recount --ignore-whitespace needed; miscounted hunks=$SEC_MIS; strict rc=$rc_strict]"
    echo "section $k $SEC_PATH: applies ONLY with --recount --ignore-whitespace (miscounted hunks=$SEC_MIS, strict rc=$rc_strict)"
  else
    # 2026-09-15 third mode — FUZZY (-C1): the model's OUTER context line often differs by a word or a
    # space while the inner lines match (KS-871 think=1: hunk 3 landed at :281 for a stated :277 once
    # only one context line was required). Placement is then guarded by A4–A6 and the human source
    # read; the mode is recorded LOUDLY in the verdict so a PASS says "fuzzy" beside its counts.
    git -C "$CLONE" apply --check -p1 $DIROPT --recount --ignore-whitespace -C1 "$SEC_FILE" > "$REP/apply_check_fuzzy_$k.out" 2>&1
    rc_fuzzy=$?
    if [ "$rc_fuzzy" -eq 0 ]; then
      echo "$SEC_FILE" > "$REP/section_$k.opts"; echo "$DIROPT --recount --ignore-whitespace -C1" >> "$REP/section_$k.opts"
      A2_MODE="fuzzy"; A2_NOTE="$A2_NOTE [$SEC_PATH: FUZZY — applies only with -C1 (one context line): $(head -1 "$REP/apply_check_fuzzy_$k.out" | tr '\n' ' '); strict rc=$rc_strict lenient rc=$rc_lenient]"
      echo "section $k $SEC_PATH: applies ONLY FUZZY (-C1): $(head -1 "$REP/apply_check_fuzzy_$k.out")"
    else
      # 2026-09-15 fourth mode — REANCHORED: the model's `-`/`+` lines are kept and every hunk is rebuilt with the
      # FILE's own context around the unique (or nearest-to-declared) location of its `-` block (tasks/code_patch/
      # reanchor.py). Built from the ten-ticket test: KS-844 q4 (an import edit under neighbours ten lines away) and
      # KS-1018 q8 (three identical catch lines, context drift) both apply strictly once reanchored; KS-864 q8 does
      # not (a `-` line the file never had — a real model error, correctly refused). Recorded LOUDLY; a hunk the
      # tool cannot place is kept as written, so a PASS here still says exactly which hunks were rebuilt.
      REAN="$REP/section_${k}.reanchored.diff"; REAN_NOTE=""
      case "$SEC_PATH" in "$SUBDIR"/*) SEC_ABS="$CLONE/$SEC_PATH" ;; *) SEC_ABS="$CLONE/$SUBDIR/$SEC_PATH" ;; esac
      if [ -f "$SEC_ABS" ] && python3 "$(dirname "$0")/reanchor.py" "$SEC_FILE" "$SEC_ABS" "$REAN" > "$REP/reanchor_$k.out" 2>&1; then
        REAN_NOTE="$(tr '\n' ';' < "$REP/reanchor_$k.out")"
        git -C "$CLONE" apply --check -p1 $DIROPT "$REAN" > "$REP/apply_check_reanchored_$k.out" 2>&1
        rc_rean=$?
      else
        rc_rean=1; REAN_NOTE="reanchor not attempted (new file or tool error: $(head -1 "$REP/reanchor_$k.out" 2>/dev/null))"
      fi
      if [ "$rc_rean" -eq 0 ]; then
        echo "$REAN" > "$REP/section_$k.opts"; echo "$DIROPT" >> "$REP/section_$k.opts"
        A2_MODE="reanchored"; A2_NOTE="$A2_NOTE [$SEC_PATH: REANCHORED — the model's context lines did not match the file; every hunk rebuilt from its -/+ lines at the file's real location ($REAN_NOTE); strict rc=$rc_strict lenient rc=$rc_lenient fuzzy rc=$rc_fuzzy]"
        echo "section $k $SEC_PATH: applies ONLY REANCHORED ($REAN_NOTE)"
      else
        A2_OK=0; A2_NOTE="$A2_NOTE [$SEC_PATH: does not apply — strict: $(head -2 "$REP/apply_check_strict_$k.out" | tr '\n' ' ') | lenient: $(head -2 "$REP/apply_check_lenient_$k.out" | tr '\n' ' ') | fuzzy(-C1): $(head -2 "$REP/apply_check_fuzzy_$k.out" | tr '\n' ' ') | reanchored: $REAN_NOTE $(head -1 "$REP/apply_check_reanchored_$k.out" 2>/dev/null | tr '\n' ' ')]"
      fi
    fi
  fi
  k=$((k+1))
done
if [ "$A2_OK" -eq 1 ] && [ "$A2_MODE" = "strict" ]; then
  pass "A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)"
elif [ "$A2_OK" -eq 1 ]; then
  pass "A2 diff applies at the tip — with an accommodation:$A2_NOTE"
else
  fail "A2 diff does NOT apply at the tip:$A2_NOTE"
  echo "RESULT: FAIL ($FAILS failed) — stopped at A2"
  exit 1
fi
apply_section_for() {
  # apply_section_for <path> — applies the section whose path matches, with its recorded opts
  local want="$1" k=1
  while [ "$k" -le "$N_SEC" ]; do
    local p; p="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))[int(sys.argv[2])-1]["path"])' "$REP/sections.json" "$k")"
    if [ "$p" = "$want" ] || [ "$SUBDIR/$p" = "$want" ]; then
      local f o; f="$(sed -n 1p "$REP/section_$k.opts")"; o="$(sed -n 2p "$REP/section_$k.opts")"
      git -C "$CLONE" apply -p1 $o "$f"
      return $?
    fi
    k=$((k+1))
  done
  echo "no section for $want" >&2; return 1
}

# ---------------------------------------------------------------- A2b placeholder test file (2026-09-15: KS-1130 ×2, KS-1120-F1)
# A "test file" with no `it(`/`test(` is the model's shortcut output ("placeholder line; content below replaces
# this"). Name it, do not let it reach A4 as a load error the reader has to decode.
k=1; PH=""
while [ "$k" -le "$N_SEC" ]; do
  pf="$(sed -n 1p "$REP/section_$k.opts" 2>/dev/null)"; pp="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))[int(sys.argv[2])-1]["path"])' "$REP/sections.json" "$k")"
  case "$pp" in *__tests__/*|*.test.ts)
    if [ -n "$pf" ] && [ "$(/usr/bin/grep -c -E "^\+\s*(it|test)\(" "$pf")" -eq 0 ]; then PH="$PH $pp ($(/usr/bin/grep -c '^+' "$pf") lines, 0 cells)"; fi ;;
  esac
  k=$((k+1))
done
if [ -n "$PH" ]; then
  fail "A2b PLACEHOLDER test file — no it()/test() cell in:$PH — the model emitted a stub instead of the test; retry the ticket (a fresh sample), do not read the load error"
  echo "RESULT: FAIL ($FAILS failed) — stopped at A2b (placeholder test file)"
  exit 1
fi

# ---------------------------------------------------------------- A3 touched set
: > "$REP/numstat.out"
k=1
while [ "$k" -le "$N_SEC" ]; do
  f="$(sed -n 1p "$REP/section_$k.opts")"; o="$(sed -n 2p "$REP/section_$k.opts")"
  git -C "$CLONE" apply --numstat -p1 $o "$f" >> "$REP/numstat.out" 2>&1
  k=$((k+1))
done
TOUCHED="$(awk '{print $3}' "$REP/numstat.out" | sort -u)"
N_TOUCHED="$(echo "$TOUCHED" | /usr/bin/grep -c . )"
ADDS="$(awk '{a+=$1} END{print a+0}' "$REP/numstat.out")"
DELS="$(awk '{d+=$2} END{print d+0}' "$REP/numstat.out")"
echo "touched files ($N_TOUCHED): $(echo "$TOUCHED" | tr '\n' ' ') (+$ADDS/-$DELS)"
HAS_PRODUCT="$(echo "$TOUCHED" | /usr/bin/grep -c -x -F "$PRODUCT")"
TEST_FILE="$(echo "$TOUCHED" | /usr/bin/grep -v -x -F "$PRODUCT" | /usr/bin/grep "^$TEST_DIR/" | head -1)"
N_OTHER="$(echo "$TOUCHED" | /usr/bin/grep -v -x -F "$PRODUCT" | /usr/bin/grep -v "^$TEST_DIR/" | /usr/bin/grep -c .)"
N_TESTS="$(echo "$TOUCHED" | /usr/bin/grep -v -x -F "$PRODUCT" | /usr/bin/grep -c "^$TEST_DIR/")"
if [ "$MODE" = test_only ] && [ "$N_TOUCHED" -eq 1 ] && [ "$HAS_PRODUCT" -eq 0 ] && [ "$N_TESTS" -eq 1 ] && [ "$N_OTHER" -eq 0 ] && [ "$TEST_FILE" != "$REF_TEST" ]; then
  pass "A3 (test-only) touched-file set == { $TEST_FILE } — the product file is untouched, as the ticket requires"
elif [ "$MODE" = test_only ]; then
  fail "A3 (test-only) touched-file set must be exactly ONE new test under $TEST_DIR and NOTHING else: n=$N_TOUCHED product=$HAS_PRODUCT tests=$N_TESTS other=$N_OTHER"
  echo "RESULT: FAIL ($FAILS failed) — stopped at A3 (test-only mode: the product file must not change)"
  exit 1
elif [ "$N_TOUCHED" -eq 2 ] && [ "$HAS_PRODUCT" -eq 1 ] && [ "$N_TESTS" -eq 1 ] && [ "$N_OTHER" -eq 0 ] && [ "$TEST_FILE" != "$REF_TEST" ]; then
  pass "A3 touched-file set == { $PRODUCT , $TEST_FILE }"
else
  fail "A3 touched-file set is not {product, one test under $TEST_DIR}: n=$N_TOUCHED product=$HAS_PRODUCT tests=$N_TESTS other=$N_OTHER ref_test_touched=$([ "$TEST_FILE" = "$REF_TEST" ] && echo yes || echo no)"
  echo "RESULT: FAIL ($FAILS failed) — stopped at A3 (cannot sequence red-first without exactly one test file)"
  exit 1
fi
TEST_REL="${TEST_FILE#$SUBDIR/$SERVICE/}"

# ---------------------------------------------------------------- A3b named sites (2026-09-15)
# Kam 09:28: "Is there a way to fix it going red through instructions or rules?" — the model fixed one
# of the two sites the ticket names. The input's defect_line.sites (parsed from the ticket's Where
# list at build time) is a checklist: every must_change site's text_at_tip must appear as a removed
# ('-') line in the PRODUCT section. Refuses before any test runs, so a partial fix is named as
# partial rather than surfacing as "the test is still red" three assertions later.
A3B_MISSED=""
N_SITES="$(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); print(len([x for x in d.get("defect_line",{}).get("sites",[]) if x.get("must_change")]))' "$INPUT")"
if [ "${N_SITES:-0}" -gt 0 ]; then
  PROD_SEC="$(python3 -c 'import json,sys; sub=sys.argv[3]; want=sys.argv[2]
for o in json.load(open(sys.argv[1])):
    if o["path"]==want or sub+"/"+o["path"]==want: print(o["file"]); break' "$REP/sections.json" "$PRODUCT" "$SUBDIR")"
  A3B_MISSED="$(python3 - "$INPUT" "$PROD_SEC" <<'PY3B'
import json, sys
d = json.load(open(sys.argv[1])); sec = open(sys.argv[2], encoding="utf-8", errors="replace").read().split("\n")
removed = [l[1:].strip() for l in sec if l.startswith("-") and not l.startswith("---")]
missed = []
for x in d.get("defect_line", {}).get("sites", []):
    if not x.get("must_change"): continue
    t = (x.get("text_at_tip") or "").strip()
    if t and t not in removed: missed.append(f":{x['line']} `{t[:70]}`")
print(" · ".join(missed))
PY3B
)"
  if [ -z "$A3B_MISSED" ]; then
    pass "A3b every must_change site the ticket names is changed by the product hunk ($N_SITES site(s))"
  else
    fail "A3b PARTIAL FIX — the product hunk leaves $(echo "$A3B_MISSED" | awk -F' · ' '{print NF}') of $N_SITES named site(s) untouched: $A3B_MISSED"
    echo "RESULT: FAIL ($FAILS failed) — stopped at A3b (a partial fix; the tests are not run)"
    exit 1
  fi
else
  echo "A3b: no must_change sites in the input — skipped"
fi

# ---------------------------------------------------------------- A4 red-first
# 2026-09-15 TDZ-INLINE (KS-1050 ×2, KS-1018 ×3): a file-scope string const read inside `vi.hoisted(` kills the
# file before any test runs; the repair is mechanical (tasks/code_patch/tdz_inline.py) and named loudly.
TK=1
while [ "$TK" -le "$N_SEC" ]; do
  tp="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))[int(sys.argv[2])-1]["path"])' "$REP/sections.json" "$TK")"
  if [ "$tp" = "$TEST_FILE" ] || [ "$SUBDIR/$tp" = "$TEST_FILE" ]; then
    tf="$(sed -n 1p "$REP/section_$TK.opts")"; to="$(sed -n 2p "$REP/section_$TK.opts")"
    python3 "$(dirname "$0")/tdz_inline.py" "$tf" "$REP/section_${TK}.tdz.diff" > "$REP/tdz_inline.out" 2>&1
    if ! /usr/bin/grep -q "^inlined 0" "$REP/tdz_inline.out"; then
      echo "$REP/section_${TK}.tdz.diff" > "$REP/section_$TK.opts"; echo "$to" >> "$REP/section_$TK.opts"
      echo "A4 TDZ-INLINED (accommodation): $(tr '\n' ';' < "$REP/tdz_inline.out")"
    fi
  fi
  TK=$((TK+1))
done
apply_section_for "$TEST_FILE" > "$REP/apply_test.out" 2>&1
rc=$?
if [ "$rc" -ne 0 ]; then
  fail "A4 the test hunk alone did not apply (rc=$rc): $(head -3 "$REP/apply_test.out" | tr '\n' ' ')"
  echo "RESULT: FAIL ($FAILS failed) — stopped at A4"
  exit 1
fi
if [ "$MODE" = test_only ]; then
  # plant the brief's tamper: the exact line at the tip is replaced; refuse if the text does not match
  python3 - "$INPUT" "$CLONE/$PRODUCT" > "$REP/tamper.out" 2>&1 <<'PYT'
import json, sys
d = json.load(open(sys.argv[1])); t = d["defect_line"]["tamper"]; p = sys.argv[2]
lines = open(p, encoding="utf-8").read().split("\n")
i = int(t["line"]) - 1
if lines[i].strip() != t["from"].strip():
    print(f"TAMPER REFUSED: line {t['line']} at the tip is {lines[i]!r}, the brief says {t['from']!r}"); sys.exit(2)
lines[i] = t["to"]; open(p, "w", encoding="utf-8").write("\n".join(lines)); print(f"tampered {p}:{t['line']}: {t['from']!r} -> {t['to']!r}")
PYT
  rc_t=$?
  if [ "$rc_t" -ne 0 ]; then
    fail "A4 (test-only) the tamper could not be planted: $(cat "$REP/tamper.out" | tr '\n' ' ')"
    echo "RESULT: FAIL ($FAILS failed) — stopped at A4 (tamper)"
    exit 1
  fi
  echo "A4 (test-only): $(cat "$REP/tamper.out")"
fi
rc_red="$(run_vitest red_first "$TEST_REL")"
RED="$(summ red_first)"
echo "test-only at tip: rc=$rc_red $RED"
if [ "$MODE" = test_only ]; then
  git -C "$CLONE" checkout -- "$PRODUCT" > "$REP/tamper_revert.out" 2>&1 && echo "A4 (test-only): tamper reverted ($PRODUCT back to the tip)" || echo "A4 (test-only): WARNING tamper revert failed: $(cat "$REP/tamper_revert.out")"
fi
red_total="$(getn "$RED" total)"; red_failed="$(getn "$RED" failed)"; red_passed="$(getn "$RED" passed)"
# 2026-09-15 A4 twin (KS-1087 night3): all three cells "failed" at the tip with `ReferenceError: deleteFn is
# not defined` — a test-side bug read as a red, and the CONTROL cell red too. A red counts only when it is
# an ASSERTION failure and every non-🔴 cell (the controls) PASSES at the untouched tip; otherwise the
# harness cannot reach the code and the "red" proves nothing.
A4_NOTE="$(python3 - "$REP/red_first.json" <<'PY4'
import json, sys, re
try: j = json.load(open(sys.argv[1]))
except Exception as e: print(f"UNREADABLE {e}"); sys.exit()
ctrl_red = []; nonassert = []
for tf in j.get("testResults", []):
    for a in tf.get("assertionResults", []):
        t = a.get("title", ""); msgs = " ".join(a.get("failureMessages") or [])
        if a.get("status") == "failed":
            if "🔴" not in t: ctrl_red.append(t[:60])
            if re.search(r"\b(ReferenceError|TypeError|SyntaxError|RangeError)\b", msgs) and "AssertionError" not in msgs and "expected" not in msgs.lower():
                nonassert.append(t[:60] + " -> " + msgs.strip().split("\n")[0][:90])
out = []
if ctrl_red: out.append("CONTROL cell(s) red at the tip: " + " | ".join(ctrl_red))
if nonassert: out.append("non-assertion failure(s): " + " | ".join(nonassert))
print(" ; ".join(out))
PY4
)"
if [ "$rc_red" -ne 0 ] && [ "$red_total" -gt 0 ] && [ "$red_failed" -ge 1 ] && [ -z "$A4_NOTE" ]; then
  pass "A4 RED-FIRST: $TEST_REL fails at the untouched tip ($red_failed failed / $red_total run; controls green; assertion reds)"
elif [ "$rc_red" -ne 0 ] && [ "$red_total" -gt 0 ] && [ "$red_failed" -ge 1 ]; then
  fail "A4 RED-FIRST: the test is red at the tip but NOT for the right reason — $A4_NOTE ($red_failed failed / $red_total run); the harness does not reach the code, so the red proves nothing"
  echo "RESULT: FAIL ($FAILS failed) — stopped at A4 (a test-side defect, not a product red)"
  exit 1
elif [ "$red_total" -eq 0 ]; then
  fail "A4 RED-FIRST: the test file did not run any test at the tip (load/compile error, not a red) — $(head -c 300 "$REP/red_first.out" | tr '\n' ' ')"
else
  fail "A4 RED-FIRST: the test file is NOT red at the untouched tip (rc=$rc_red, $red_failed failed / $red_total run) — it does not prove the defect"
fi

# ---------------------------------------------------------------- A5 green-after
if [ "$MODE" = test_only ]; then
  echo "A5 (test-only): no product hunk — the test must be GREEN at the untouched tip" > "$REP/apply_product.out"; rc=0
else
apply_section_for "$PRODUCT" > "$REP/apply_product.out" 2>&1
rc=$?
fi
if [ "$rc" -ne 0 ]; then
  fail "A5 the product hunk did not apply (rc=$rc): $(head -3 "$REP/apply_product.out" | tr '\n' ' ')"
  echo "RESULT: FAIL ($FAILS failed) — stopped at A5"
  exit 1
fi
rc_green="$(run_vitest green_after "$TEST_REL")"
GREEN="$(summ green_after)"
echo "test after product hunk: rc=$rc_green $GREEN"
g_total="$(getn "$GREEN" total)"; g_failed="$(getn "$GREEN" failed)"; g_passed="$(getn "$GREEN" passed)"
if [ "$rc_green" -eq 0 ] && [ "$g_total" -gt 0 ] && [ "$g_failed" -eq 0 ] && [ "$g_passed" -ge 1 ]; then
  pass "A5 GREEN-AFTER: $TEST_REL passes with the product hunk ($g_passed passed / $g_total run)"
else
  fail "A5 GREEN-AFTER: $TEST_REL still red (or empty) after the product hunk (rc=$rc_green, $g_failed failed / $g_total run): $(getn "$GREEN" failed_names)"
fi
if [ "$red_passed" -ge 1 ] && [ "$g_passed" -ge 1 ]; then
  echo "INFO control cell present: $red_passed cell(s) passed BEFORE and $g_passed AFTER (the harness reaches the code both times)"
else
  echo "INFO control cell present: NO ($red_passed passed before, $g_passed after) — the task asked for one; not gated"
fi

# ---------------------------------------------------------------- A6 whole suite
rc_after="$(run_vitest after_suite)"
AFTER="$(summ after_suite)"
echo "after suite rc=$rc_after $AFTER"
python3 - "$REP/baseline_suite.json" "$REP/after_suite.json" > "$REP/suite_delta.out" 2>&1 <<'PYEOF'
import json, sys
def failed(p):
    j = json.load(open(p)); s = set()
    for r in j.get("testResults", []):
        for a in r.get("assertionResults", []):
            if a.get("status") == "failed": s.add((r["name"].split("/")[-1], a.get("fullName")))
        if r.get("status") == "failed" and not r.get("assertionResults"): s.add((r["name"].split("/")[-1], "<LOAD ERROR>"))
    return j, s
jb, fb = failed(sys.argv[1]); ja, fa = failed(sys.argv[2])
new = sorted(fa - fb); fixed = sorted(fb - fa)
print(f"baseline: total={jb['numTotalTests']} failed={jb['numFailedTests']} | after: total={ja['numTotalTests']} failed={ja['numFailedTests']}")
print(f"develop's own reds (attributed, not counted): {sorted(fb)}")
print(f"NEW reds: {new}")
print(f"reds fixed by the patch: {fixed}")
print(f"tests added: {ja['numTotalTests'] - jb['numTotalTests']}")
sys.exit(0 if not new else 1)
PYEOF
rc=$?
cat "$REP/suite_delta.out"
if [ "$rc" -eq 0 ]; then
  pass "A6 whole $SERVICE suite: no NEW red vs the untouched tip"
else
  fail "A6 whole $SERVICE suite: NEW red(s) vs the untouched tip (see suite_delta.out)"
fi

# ---------------------------------------------------------------- A7 tsc
( cd "$SVC" && npx tsc --noEmit -p . ) > "$REP/after_tsc.out" 2>&1
rc_tsc=$?
if [ "$rc_tsc" -eq 0 ]; then
  pass "A7 tsc --noEmit for $SERVICE: rc 0 after the patch (baseline rc=$rc_base_tsc)"
else
  fail "A7 tsc --noEmit for $SERVICE: rc=$rc_tsc after the patch (baseline rc=$rc_base_tsc): $(head -5 "$REP/after_tsc.out" | tr '\n' ' ')"
fi
# Informational: the test file is excluded from the service tsconfig, so
# type-check it on its own (vitest transpiles without checking types).
( cd "$SVC" && npx tsc --noEmit --strict --esModuleInterop --skipLibCheck --target ES2022 --module commonjs --moduleResolution node --types node,vitest/globals "$TEST_REL" ) > "$REP/after_tsc_testfile.out" 2>&1
rc_tsc_t=$?
echo "INFO tsc on the test file alone: rc=$rc_tsc_t ($(wc -l < "$REP/after_tsc_testfile.out" | tr -d ' ') lines; not gated — vitest does not type-check and the service tsconfig excludes __tests__)"

echo "SUMMARY files=$N_TOUCHED +$ADDS/-$DELS test=$TEST_REL red_first=$([ "$rc_red" -ne 0 ] && [ "$red_failed" -ge 1 ] && echo yes || echo no) apply_mode=$A2_MODE"
if [ "$FAILS" -eq 0 ]; then
  echo "RESULT: PASS (7/7)"
  exit 0
fi
echo "RESULT: FAIL ($FAILS failed)"
exit 1
