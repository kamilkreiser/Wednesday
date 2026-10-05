#!/bin/bash
# checker.sh <input.json> <out.md> <clone-dir> — code_patch2: the MULTI-FILE code_patch verdict (2026-10-05, Kam's
# 50-a-day target needs rung 3). A code_patch2 input (tasks/code_patch2/build_input2.sh) declares
# `product_files` (1-3) and `test_files` (1-2, each new|modified). Same six-clause contract as code_patch:
#
#   A1, A2      code_patch/checker.sh ITSELF, unchanged (STAGE 1): extract, baseline suite + tsc, split per file,
#               every A2 accommodation and its recorded apply MODE. It is run on a copy of the input whose
#               product_file is a sentinel, so its own A3 stops it deterministically after A2; its lines up to A3 are
#               passed through byte for byte and its artefacts (sections.json, section_<k>.opts, baseline_suite.json,
#               hunk_audit.out ...) are this checker's subject.
#   A3          touched set == the DECLARED set exactly (missing / undeclared named); the reference test never
#               touched unless declared; every test under test_dir.
#   A3b/A3e     code_patch's own PY3B / PY3E predicates (read out of code_patch/checker.sh at run time, never
#               copied) over ALL product sections. Line-keyed / ascii_proxy sites are REFUSED (not supported here).
#   A3c/A3d     code_patch/a3c_plus.py over ALL declared sections (multiset), A3d per product against its tip.
#   A3i         code_patch/a3i_indent.py per declared file (its own section, its recorded opts).
#   A4          RED-FIRST, generalised: ALL test sections applied, NO product section -> every declared red cell red BY
#               ASSERTION, controls green, no load error (code_patch's PY4 predicate, read at run time).
#   A5          GREEN-AFTER: ALL product sections applied on top -> every declared test file green.
#   A6          whole service suite: no NEW red vs the stage-1 baseline (code_patch's own delta script, read at run time).
#   A7          tsc --noEmit for the service rc 0 (+ the INFO tsc on each new test, code_patch's tsc_test_types).
# Shared helpers (run_vitest, summ, getn, apply_section_for, tsc_test_types) are likewise read out of
# code_patch/checker.sh at run time: one implementation, two tiers. If any extraction anchor is missing the checker
# FAILS as a harness error rather than guess. RESULT line shape == code_patch's (`RESULT: PASS (7/7)` / `FAIL (n failed)`).
# bash 3.2; stderr never discarded; every write verb inside <clone-dir>; no cd in the caller's shell.
set -uo pipefail
INPUT="${1:-}"; OUT="${2:-}"; CLONE="${3:-}"
if [ -z "$INPUT" ] || [ -z "$OUT" ] || [ -z "$CLONE" ] || [ ! -f "$INPUT" ] || [ ! -f "$OUT" ] || [ ! -d "$CLONE/.git" ]; then
  echo "usage: checker.sh <input.json> <out.md> <clone-dir>" >&2; exit 1
fi
HERE2="$(cd "$(dirname "$0")" && pwd)"; CP="$(dirname "$HERE2")/code_patch"; CPC="$CP/checker.sh"
REP="$OUT.checker"; mkdir -p "$REP"
FAILS=0; pass(){ echo "PASS $*"; }; fail(){ echo "FAIL $*"; FAILS=$((FAILS+1)); }
harness_stop(){ fail "$1"; echo "RESULT: FAIL ($FAILS failed) — stopped at $2 (the harness, not the model)"; exit 1; }

jf() { python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); r=d.get("repo") or {}; v=d.get(sys.argv[2]); v=r.get(sys.argv[2]) if v in (None,"") else v; print(v if v is not None else "")' "$INPUT" "$1"; }
TIP="$(jf tip)"; SUBDIR="$(jf repo_subdir)"; SERVICE="$(jf service_dir)"; TEST_DIR="$(jf test_dir)"; REF_TEST="$(jf reference_test_file)"
PRODUCTS="$(python3 -c 'import json,sys; print("\n".join(json.load(open(sys.argv[1])).get("product_files") or []))' "$INPUT")"
TESTS="$(python3 -c 'import json,sys; print("\n".join(t["path"] for t in (json.load(open(sys.argv[1])).get("test_files") or [])))' "$INPUT")"
NEWTESTS="$(python3 -c 'import json,sys; print("\n".join(t["path"] for t in (json.load(open(sys.argv[1])).get("test_files") or []) if t.get("status")=="new"))' "$INPUT")"
NP="$(echo "$PRODUCTS" | grep -c .)"; NT="$(echo "$TESTS" | grep -c .)"
echo "mode: code_patch2 (declared: $NP product(s), $NT test(s))"
[ "$NP" -ge 1 ] && [ "$NP" -le 3 ] && [ "$NT" -ge 1 ] && [ "$NT" -le 2 ] || harness_stop "A0 input: code_patch2 needs product_files 1-3 and test_files 1-2 (got $NP / $NT) — build it with tasks/code_patch2/build_input2.sh" "A0"
UNSUP="$(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); s=(d.get("defect_line") or {}).get("sites") or []; print(len([x for x in s if x.get("ascii_proxy") or x.get("key")=="line+text"]) + (1 if (d.get("defect_line") or {}).get("tamper") else 0) + (1 if d.get("self_testing") else 0))' "$INPUT")"
[ "$UNSUP" = 0 ] || harness_stop "A0 input: line-keyed / ascii_proxy sites, a tamper, or self_testing are not supported by code_patch2 ($UNSUP found) — use code_patch for those shapes" "A0"

# ---------------------------------------------------------------- extraction from code_patch/checker.sh (one implementation)
EXT="$REP/_from_code_patch"; mkdir -p "$EXT"
python3 - "$CPC" "$EXT" <<'PYX' > "$REP/extract_code_patch.out" 2>&1 || harness_stop "A0 could not read the shared pieces out of $CPC: $(tail -2 "$REP/extract_code_patch.out" | tr '\n' ' ')" "A0"
import os, sys
src, ext = sys.argv[1:3]
L = open(src, encoding="utf-8").read().split("\n")
def idx(pred, start=0, what=""):
    for i in range(start, len(L)):
        if pred(L[i]): return i
    raise SystemExit(f"anchor not found: {what}")
def heredoc(opener_sub, end_tok, name):
    i = idx(lambda l: opener_sub in l, 0, opener_sub); j = idx(lambda l: l == end_tok, i + 1, end_tok)
    open(os.path.join(ext, name), "w").write("\n".join(L[i + 1:j]) + "\n"); print(f"{name}: {src}:{i+2}-{j}")
# helpers: RUNNER_KIND= ... through the one-line getn()
a = idx(lambda l: l.startswith('RUNNER_KIND="$('), 0, "RUNNER_KIND"); b = idx(lambda l: l.startswith("getn() {"), a, "getn()")
open(os.path.join(ext, "helpers.sh"), "w").write("\n".join(L[a:b + 1]) + "\n"); print(f"helpers.sh: {src}:{a+1}-{b+1}")
a = idx(lambda l: l.startswith("apply_section_for() {"), 0, "apply_section_for"); b = idx(lambda l: l == "}", a, "apply_section_for end")
open(os.path.join(ext, "apply_section_for.sh"), "w").write("\n".join(L[a:b + 1]) + "\n"); print(f"apply_section_for.sh: {src}:{a+1}-{b+1}")
a = idx(lambda l: l.startswith("# BEGIN tsc_test_types"), 0, "BEGIN tsc_test_types"); b = idx(lambda l: l.startswith("# END tsc_test_types"), a, "END")
open(os.path.join(ext, "tsc_test_types.sh"), "w").write("\n".join(L[a:b + 1]) + "\n"); print(f"tsc_test_types.sh: {src}:{a+1}-{b+1}")
heredoc("<<'PY3B'", "PY3B", "py3b.py")
heredoc("<<'PY3E'", "PY3E", "py3e.py")
heredoc("<<'PY4'", "PY4", "py4.py")
heredoc('> "$REP/suite_delta.out" 2>&1 <<\'PYEOF\'', "PYEOF", "suite_delta.py")
PYX

# ---------------------------------------------------------------- STAGE 1: code_patch/checker.sh through A2
python3 - "$INPUT" "$REP/stage1_input.json" <<'PYS'
import json, sys
d = json.load(open(sys.argv[1])); d["product_file"] = "__code_patch2_stage1_no_product__"
json.dump(d, open(sys.argv[2], "w"), indent=1, ensure_ascii=False)
PYS
bash "$CPC" "$REP/stage1_input.json" "$OUT" "$CLONE" > "$REP/stage1_checker.out" 2>&1; S1=$?
if [ "$S1" -eq 0 ] || ! grep -q '^RESULT: FAIL .*stopped at A3 (cannot sequence red-first' "$REP/stage1_checker.out"; then
  # stage 1 stopped BEFORE A3 (A1 / A2 / A2b — a real verdict) or did something unexpected: pass it through as is
  cat "$REP/stage1_checker.out"
  [ "$S1" -eq 0 ] && harness_stop "A0 stage 1 (code_patch/checker.sh) returned rc 0 with a sentinel product — it must stop at A3" "stage 1"
  exit 1
fi
awk '/^touched files \(/{exit} /^mode: /{next} {print}' "$REP/stage1_checker.out"
TOUCHED_LINE="$(grep -m1 '^touched files (' "$REP/stage1_checker.out")"
A2_MODE="strict"; grep -q '^PASS A2 diff applies at the tip (strict' "$REP/stage1_checker.out" || A2_MODE="accommodated (see the A2 line)"
rc_base_tsc="$(sed -n 's/^baseline tsc rc=\([0-9]*\).*/\1/p' "$REP/stage1_checker.out" | head -1)"
N_SEC="$(python3 -c 'import json,sys; print(len(json.load(open(sys.argv[1]))))' "$REP/sections.json")"
SVC="$CLONE/$SUBDIR/$SERVICE"
# shellcheck disable=SC1090
. "$EXT/helpers.sh" > /dev/null; . "$EXT/apply_section_for.sh"; . "$EXT/tsc_test_types.sh"
sec_file() { python3 -c 'import json,sys; sub=sys.argv[3]; want=sys.argv[2]
for k,o in enumerate(json.load(open(sys.argv[1])), 1):
    if o["path"]==want or sub+"/"+o["path"]==want: print(k); break' "$REP/sections.json" "$1" "$SUBDIR"; }
opts_file() { local k; k="$(sec_file "$1")"; [ -n "$k" ] && sed -n 1p "$REP/section_$k.opts"; }

# ---------------------------------------------------------------- A3 declared touched set
A3_OUT="$(python3 - "$TOUCHED_LINE" "$PRODUCTS" "$TESTS" "$REF_TEST" "$TEST_DIR" <<'PY3'
import re, sys
line, prods, tests, ref, tdir = sys.argv[1:6]
m = re.match(r"^touched files \((\d+)\): (.*?)\s*\(\+\d+/-\d+\)\s*$", line)
if not m: print("MEASURE could not parse the stage-1 touched line: " + line[:200]); sys.exit(2)
touched = set(m.group(2).split()); P = [p for p in prods.split("\n") if p]; T = [t for t in tests.split("\n") if t]
declared = set(P) | set(T)
missing = sorted(declared - touched); undeclared = sorted(touched - declared)
bad = []
if missing: bad.append(f"declared but UNTOUCHED: {missing}")
if undeclared: bad.append(f"touched but UNDECLARED: {undeclared}")
if ref and ref in touched and ref not in declared: bad.append(f"the reference test {ref} was touched")
if tdir and [t for t in T if not t.startswith(tdir.rstrip('/') + '/')]: bad.append(f"a declared test is not under {tdir}")
if bad: print(" ; ".join(bad)); sys.exit(1)
print(f"{{ {' , '.join(P)} }} + {{ {' , '.join(T)} }}")
PY3
)"; A3RC=$?
if [ "$A3RC" -eq 0 ]; then pass "A3 (code_patch2) touched-file set == the declared set: $A3_OUT"
elif [ "$A3RC" -eq 1 ]; then fail "A3 (code_patch2) touched-file set != the declared set: $A3_OUT"; echo "RESULT: FAIL ($FAILS failed) — stopped at A3 (the touched set is not the declared one)"; exit 1
else harness_stop "A3 MEASURE ERROR: $A3_OUT" "A3"; fi

# ---------------------------------------------------------------- A3b / A3e (code_patch's predicates, all product sections)
: > "$REP/a3b_products.diff"
while IFS= read -r p; do [ -z "$p" ] && continue; k="$(sec_file "$p")"; cat "$REP/section_$k.diff" >> "$REP/a3b_products.diff"; done <<< "$PRODUCTS"
N_SITES="$(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); print(len([x for x in d.get("defect_line",{}).get("sites",[]) if x.get("must_change")]))' "$INPUT")"
if [ "${N_SITES:-0}" -gt 0 ]; then
  A3B_MISSED="$(python3 "$EXT/py3b.py" "$INPUT" "$REP/a3b_products.diff")"
  if [ -n "$A3B_MISSED" ]; then fail "A3b PARTIAL FIX — the product sections leave named site(s) untouched: $A3B_MISSED"; echo "RESULT: FAIL ($FAILS failed) — stopped at A3b (a partial fix; the tests are not run)"; exit 1; fi
  A3E_REMOVED="$(python3 "$EXT/py3e.py" "$INPUT" "$REP/a3b_products.diff")"
  if [ -n "$A3E_REMOVED" ]; then fail "A3e a line the brief says STAYS was REMOVED by a product section ('-' with no '+'): $A3E_REMOVED"; echo "RESULT: FAIL ($FAILS failed) — stopped at A3e"; exit 1; fi
  pass "A3b every must_change site the brief names is changed by a product section ($N_SITES site(s), $NP product file(s))"
else
  echo "A3b: no must_change sites in the input — skipped"
fi

# ---------------------------------------------------------------- A3c / A3d / A3i
N_PLUS="$(python3 -c 'import json,sys; print(len(json.load(open(sys.argv[1])).get("defect_line",{}).get("expected_plus",[])))' "$INPUT")"
if [ "${N_PLUS:-0}" -gt 0 ]; then
  : > "$REP/a3c_union.diff"
  while IFS= read -r p; do [ -z "$p" ] && continue; k="$(sec_file "$p")"; cat "$REP/section_$k.diff" >> "$REP/a3c_union.diff"; done <<< "$(printf '%s\n%s\n' "$PRODUCTS" "$TESTS")"
  A3C_BAD=""; A3D_BAD=""
  # A3c: the brief's '+' lines against the UNION of every declared section (multiset); the target is a path no carried
  # file has, so a3c_plus.py's A3d leg has no tip to read here (A3d runs per product below).
  o="$(python3 "$CP/a3c_plus.py" "$INPUT" "$REP/a3c_union.diff" "__code_patch2_no_target__" 2>&1)"; r=$?
  echo "$o" > "$REP/a3c_union.out"
  if [ "$r" -eq 1 ]; then A3C_BAD="$o"; elif [ "$r" -ne 0 ]; then harness_stop "A3c MEASURE ERROR rc=$r: $o" "A3c"; fi
  # A3d per product, on THAT product's section only (a union would hold a new test's `return {` against a product's
  # tip — a false duplicate, measured on KS-1278's golden 2026-10-05). The input copy's expected_plus is the brief's
  # lines this section adds (stripped multiset), so a3c_plus.py's A3c leg is satisfied by construction and its A3d leg
  # judges exactly this file.
  [ -z "$A3C_BAD" ] && while IFS= read -r p; do
    [ -z "$p" ] && continue; k="$(sec_file "$p")"
    python3 - "$INPUT" "$REP/section_$k.diff" "$REP/a3d_input_$k.json" "$p" <<'PYD'
import json, sys
d = json.load(open(sys.argv[1])); sec = open(sys.argv[2], encoding="utf-8", errors="replace").read().split("\n")
plus = [l[1:].strip() for l in sec if l.startswith("+") and not l.startswith("+++")]
pool = list(plus); keep = []
for e in (d.get("defect_line") or {}).get("expected_plus", []):
    if e.strip() in pool: pool.remove(e.strip()); keep.append(e)
d.setdefault("defect_line", {})["expected_plus"] = keep
# A3d's subject is this product's WHOLE tip: keep only this file, as an excerpt OBJECT with no regions, so a3c_plus.py
# reads it with `git show <tip>:<path>` (its own excerpt-mode path) whatever the input carried for the model
d["files"] = {sys.argv[4]: {"excerpt": True, "regions": []}}
json.dump(d, open(sys.argv[3], "w"), ensure_ascii=False)
PYD
    o="$(python3 "$CP/a3c_plus.py" "$REP/a3d_input_$k.json" "$REP/section_$k.diff" "$p" 2>&1)"; r=$?
    echo "$o" > "$REP/a3d_$(basename "$p").out"
    if [ "$r" -eq 2 ]; then A3D_BAD="$A3D_BAD $(basename "$p"): $(echo "$o" | sed 's/^A3D //' | head -3 | cut -c1-90 | tr '\n' '·')"; elif [ "$r" -ne 0 ]; then harness_stop "A3d MEASURE ERROR rc=$r for $p: $o" "A3d"; fi
  done <<< "$PRODUCTS"
  if [ -n "$A3C_BAD" ]; then fail "A3c INCOMPLETE — $(printf '%s\n' "$A3C_BAD" | grep -c .) of $N_PLUS line(s) the brief adds are ABSENT from the declared sections: $(printf '%s' "$A3C_BAD" | head -3 | cut -c1-90 | tr '\n' '·')"; echo "RESULT: FAIL ($FAILS failed) — stopped at A3c (a dropped addition; the tests are not run)"; exit 1; fi
  if [ -n "$A3D_BAD" ]; then fail "A3d CONTEXT MARKED AS ADDITION — '+' line(s) that already exist at a product's tip and are not in the brief:$A3D_BAD — the diff would DUPLICATE them"; echo "RESULT: FAIL ($FAILS failed) — stopped at A3d"; exit 1; fi
  pass "A3c every '+' line the brief adds is in the declared sections ($N_PLUS line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)"
  A3I_BAD=""; A3I_OK=""
  # A3i per file on THAT file's brief lines only: the brief's `## The exact change` blocks are split at their own
  # `--- a/<path>` headers (the builder's regexes), and each file gets an input copy whose description and
  # expected_plus are its own lines — so a `/**` the brief adds to a product at indent 4 is never held against a new
  # test's `/**` at indent 0 (a false SHIFT measured on KS-1278's golden, 2026-10-05). A file with no brief lines is not
  # measured (INFO). Lines before any header cannot be attributed: then every file gets the WHOLE list (fail-safe).
  python3 - "$INPUT" "$REP" "$SUBDIR" <<'PYI' > "$REP/a3i_split.out" 2>&1
import json, re, sys
inp, rep, sub = sys.argv[1:4]
d = json.load(open(inp)); desc = (d.get("ticket") or {}).get("description") or ""
mx = re.search(r"^##+\s*The exact change\b.*?$(.*?)(?=^##+\s|\Z)", desc, re.M | re.S)
per, cur, unattributed = {}, None, 0
if mx:
    for blk in re.findall(r"^```[^\n]*\n(.*?)^```", mx.group(1), re.M | re.S):
        for ln in blk.split("\n"):
            m = re.match(r"^\+\+\+ b/(\S+)", ln)
            if m: cur = m.group(1); continue
            if ln.startswith("+") and not ln.startswith("+++") and ln[1:].strip():
                if cur is None: unattributed += 1
                per.setdefault(cur, []).append(ln)
if unattributed or not per:
    print("WHOLE"); sys.exit(0)
for path, lines in per.items():
    full = path if path.startswith(sub + "/") else f"{sub}/{path}"
    e = dict(d); e["defect_line"] = dict(d.get("defect_line") or {})
    e["defect_line"]["expected_plus"] = [l[1:].strip() for l in lines]
    e["ticket"] = dict(d.get("ticket") or {}); e["ticket"]["description"] = "## The exact change\n\n```diff\n" + "\n".join(lines) + "\n```\n"
    json.dump(e, open(f"{rep}/a3i_input_{full.rsplit('/', 1)[-1]}.json", "w"), ensure_ascii=False)
    print(f"FILE {full} {len(lines)}")
PYI
  A3I_WHOLE=0; grep -q '^WHOLE' "$REP/a3i_split.out" && A3I_WHOLE=1
  while IFS= read -r p; do
    [ -z "$p" ] && continue; k="$(sec_file "$p")"
    A3I_IN="$INPUT"
    if [ "$A3I_WHOLE" -eq 0 ]; then
      if ! grep -q "^FILE $p " "$REP/a3i_split.out"; then echo "INFO A3i: the brief's edit blocks add no line to $(basename "$p") — not measured"; continue; fi
      A3I_IN="$REP/a3i_input_$(basename "$p").json"
    fi
    python3 "$CP/a3i_indent.py" "$A3I_IN" "$CLONE" "$(sed -n 1p "$REP/section_$k.opts")" "$p" "$(sed -n 2p "$REP/section_$k.opts")" > "$REP/a3i_$(basename "$p").out" 2>&1; r=$?
    if [ "$r" -eq 1 ]; then A3I_BAD="$A3I_BAD $(basename "$p"): $(grep -m2 '^SHIFT' "$REP/a3i_$(basename "$p").out" | tr '\n' ' ' | cut -c1-200)"
    elif [ "$r" -eq 0 ]; then A3I_OK="$A3I_OK $(basename "$p")"
    elif [ "$r" -ne 5 ]; then harness_stop "A3i INDENT MEASURE ERROR rc=$r for $p: $(head -2 "$REP/a3i_$(basename "$p").out" | tr '\n' ' ')" "A3i"; fi
  done <<< "$(printf '%s\n%s\n' "$PRODUCTS" "$TESTS")"
  if [ -n "$A3I_BAD" ]; then fail "A3i INDENT SHIFT — brief lines landed with DIFFERENT leading whitespace:$A3I_BAD (apply mode $A2_MODE)"; echo "RESULT: FAIL ($FAILS failed) — stopped at A3i (an indentation shift; the tests are not run)"; exit 1; fi
  echo "A3i: brief '+' lines byte-exact incl. leading whitespace in:${A3I_OK:- (none measurable — skipped)}"
else
  echo "INFO A3c/A3i skipped — the input carries no expected '+' lines"
fi

# ---------------------------------------------------------------- A4 red-first (ALL test sections, NO product section)
TEST_RELS=""
while IFS= read -r t; do
  [ -z "$t" ] && continue; k="$(sec_file "$t")"
  tf="$(sed -n 1p "$REP/section_$k.opts")"; to="$(sed -n 2p "$REP/section_$k.opts")"
  # code_patch's two named test-side accommodations, by its own tools, recorded the same way (opts rewritten)
  if echo "$NEWTESTS" | grep -qxF "$t" && [ -n "$REF_TEST" ] && [ -f "$CLONE/$REF_TEST" ]; then
    python3 "$CP/decl_splice.py" "$tf" "$CLONE/$REF_TEST" "$REP/section_${k}.decl.diff" > "$REP/decl_splice_$k.out" 2>&1
    if ! grep -q "^spliced 0" "$REP/decl_splice_$k.out"; then tf="$REP/section_${k}.decl.diff"; printf '%s\n%s\n' "$tf" "$to" > "$REP/section_$k.opts"; echo "A4 DECL-SPLICED (accommodation) $t: $(tr '\n' ';' < "$REP/decl_splice_$k.out")"; fi
  fi
  python3 "$CP/tdz_inline.py" "$tf" "$REP/section_${k}.tdz.diff" > "$REP/tdz_inline_$k.out" 2>&1
  if ! grep -q "^inlined 0" "$REP/tdz_inline_$k.out"; then printf '%s\n%s\n' "$REP/section_${k}.tdz.diff" "$to" > "$REP/section_$k.opts"; echo "A4 TDZ-INLINED (accommodation) $t: $(tr '\n' ';' < "$REP/tdz_inline_$k.out")"; fi
  apply_section_for "$t" >> "$REP/apply_test.out" 2>&1 || { fail "A4 the test section for $t did not apply alone (rc=$?): $(tail -3 "$REP/apply_test.out" | tr '\n' ' ')"; echo "RESULT: FAIL ($FAILS failed) — stopped at A4"; exit 1; }
  rel="${t#$SUBDIR/$SERVICE/}"; TEST_RELS="$TEST_RELS $rel"
done <<< "$TESTS"
# shellcheck disable=SC2086
rc_red="$(run_vitest red_first $TEST_RELS)"
RED="$(summ red_first)"
echo "tests with ALL test sections, NO product section: rc=$rc_red $RED"
red_total="$(getn "$RED" total)"; red_failed="$(getn "$RED" failed)"; red_passed="$(getn "$RED" passed)"
A4_NOTE="$(python3 "$EXT/py4.py" "$REP/red_first.json" "$INPUT" "$REP/a4_declared_green.out")"
A4_GREEN_DECL="$(tr '\n' '|' < "$REP/a4_declared_green.out" 2>/dev/null | sed 's/|$//; s/|/ | /g')"
if [ "$rc_red" -ne 0 ] && [ "$red_total" -gt 0 ] && [ "$red_failed" -ge 1 ] && [ -z "$A4_NOTE" ] && [ -z "$A4_GREEN_DECL" ]; then
  pass "A4 RED-FIRST: the declared test(s) fail with every test section and no product section ($red_failed failed / $red_total run; controls green; assertion reds)"
elif [ "$rc_red" -ne 0 ] && [ "$red_total" -gt 0 ] && [ "$red_failed" -ge 1 ] && [ -n "$A4_NOTE" ]; then
  fail "A4 RED-FIRST: red but NOT for the right reason — $A4_NOTE ($red_failed failed / $red_total run); the red proves nothing"
  echo "RESULT: FAIL ($FAILS failed) — stopped at A4 (a test-side defect, not a product red)"; exit 1
elif [ "$rc_red" -ne 0 ] && [ "$red_total" -gt 0 ] && [ "$red_failed" -ge 1 ]; then
  fail "A4 RED-FIRST: declared red cell(s) did NOT fail by assertion before the product sections — $A4_GREEN_DECL ($red_failed failed / $red_total run)"
  echo "RESULT: FAIL ($FAILS failed) — stopped at A4 (a declared red cell stayed green)"; exit 1
elif [ "$red_total" -eq 0 ]; then
  fail "A4 RED-FIRST: the test file(s) ran no test with the test sections alone (load/compile error, not a red) — $(head -c 300 "$REP/red_first.out" | tr '\n' ' ')"
else
  fail "A4 RED-FIRST: the declared test(s) are NOT red before the product sections (rc=$rc_red, $red_failed failed / $red_total run) — they do not prove the defect${A4_GREEN_DECL:+; declared reds green: $A4_GREEN_DECL}"
fi

# ---------------------------------------------------------------- A5 green-after (ALL product sections on top)
: > "$REP/apply_product.out"
while IFS= read -r p; do
  [ -z "$p" ] && continue
  apply_section_for "$p" >> "$REP/apply_product.out" 2>&1 || { fail "A5 the product section for $p did not apply on top of the tests (rc=$?): $(tail -3 "$REP/apply_product.out" | tr '\n' ' ')"; echo "RESULT: FAIL ($FAILS failed) — stopped at A5"; exit 1; }
done <<< "$PRODUCTS"
# shellcheck disable=SC2086
rc_green="$(run_vitest green_after $TEST_RELS)"
GREEN="$(summ green_after)"
echo "tests after ALL product sections: rc=$rc_green $GREEN"
g_total="$(getn "$GREEN" total)"; g_failed="$(getn "$GREEN" failed)"; g_passed="$(getn "$GREEN" passed)"
if [ "$rc_green" -eq 0 ] && [ "$g_total" -gt 0 ] && [ "$g_failed" -eq 0 ] && [ "$g_passed" -ge 1 ]; then
  pass "A5 GREEN-AFTER: every declared test passes with all $NP product section(s) ($g_passed passed / $g_total run)"
else
  fail "A5 GREEN-AFTER: still red (or empty) after the product sections (rc=$rc_green, $g_failed failed / $g_total run): $(getn "$GREEN" failed_names)"
fi
echo "INFO control cells: $red_passed passed BEFORE the product sections, $g_passed AFTER"

# ---------------------------------------------------------------- A6 whole suite (code_patch's delta script)
rc_after="$(run_vitest after_suite)"
AFTER="$(summ after_suite)"
echo "after suite rc=$rc_after $AFTER"
python3 "$EXT/suite_delta.py" "$REP/baseline_suite.json" "$REP/after_suite.json" > "$REP/suite_delta.out" 2>&1; rc=$?
cat "$REP/suite_delta.out"
if [ "$rc" -eq 0 ]; then pass "A6 whole $SERVICE suite: no NEW red vs the untouched tip"; else fail "A6 whole $SERVICE suite: NEW red(s) vs the untouched tip (see suite_delta.out)"; fi

# ---------------------------------------------------------------- A7 tsc
( cd "$SVC" && npx tsc --noEmit -p . ) > "$REP/after_tsc.out" 2>&1; rc_tsc=$?
if [ "$rc_tsc" -eq 0 ]; then pass "A7 tsc --noEmit for $SERVICE: rc 0 after the patch (baseline rc=${rc_base_tsc:-?})"
else fail "A7 tsc --noEmit for $SERVICE: rc=$rc_tsc after the patch (baseline rc=${rc_base_tsc:-?}): $(head -5 "$REP/after_tsc.out" | tr '\n' ' ')"; fi
TSC_T_LINE="$(tsc_test_types "$SVC")"; TSC_TYPES="${TSC_T_LINE%%	*}"; [ -z "$TSC_TYPES" ] && TSC_TYPES="node,vitest/globals"
while IFS= read -r t; do
  [ -z "$t" ] && continue; rel="${t#$SUBDIR/$SERVICE/}"
  ( cd "$SVC" && npx tsc --noEmit --strict --esModuleInterop --skipLibCheck --target ES2022 --module commonjs --moduleResolution node --types "$TSC_TYPES" "$rel" ) > "$REP/after_tsc_$(basename "$t").out" 2>&1
  echo "INFO tsc on $rel alone (--types $TSC_TYPES): rc=$? (not gated, as in code_patch)"
done <<< "$NEWTESTS"

echo "SUMMARY files=$((NP+NT)) products=$NP tests=$NT red_first=$([ "$rc_red" -ne 0 ] && [ "$red_failed" -ge 1 ] && echo yes || echo no) apply_mode=$A2_MODE"
if [ "$FAILS" -eq 0 ]; then echo "RESULT: PASS (7/7)"; exit 0; fi
echo "RESULT: FAIL ($FAILS failed)"; exit 1
