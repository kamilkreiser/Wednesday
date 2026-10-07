#!/bin/bash
# checker.sh <input.json> <out.md> <clone-dir> — bash_patch2: the MULTI-FILE bash verdict (2026-10-07, rung 3; Wednesday's
# commission "open rung 3": the Spark's pool is capped by the one-script / one-suite B3, and KS-1274 is 1 script + 3
# suites). A bash_patch2 input (tasks/bash_patch2/build_bash_input2.sh) declares `product_files` (1-3) and `test_files`
# (1-4, each {path, status new|modified, role red|support}). Same six-clause contract as bash_patch:
#
#   B0-B2  tasks/bash_patch/checker.sh ITSELF, unchanged (STAGE 1): subject, ONE fenced diff, split per file, the new-file
#          normalisation, per-section apply modes (strict / --recount / lenient / reanchored) recorded in section_k.diff.opts.
#          It runs on a copy of the input whose suggested_test_file is a sentinel no diff can touch, so its own B3 stops
#          it deterministically BEFORE anything is applied; its lines up to B3 pass through byte for byte, and its
#          artefacts (sections.json, section_k.diff[.opts]) are this checker's subject.
#   B3     touched set (numstat, each section's own opts) == the DECLARED set exactly — an undeclared file, or a declared
#          file left untouched, FAILS by name; the reference never touched unless declared; a NEW test absent at the tip
#          and a `--- /dev/null` section; a MODIFIED test present; every test in test_dir.
#   B3b    the FIRST product's must_change sites are '-' lines; no "(correct) … stays" site removed (no repair here: a
#          FAIL); A3c over the union of product sections (multiset); A3d per product on that product's section.
#   B3x    per declared file, its '+' lines == the brief's, byte for byte, in order (tasks/code_patch2/brief_bytes.py).
#   B4     RED-FIRST, generalised: ALL test sections applied, NO product section -> every RED test parses, runs, exits
#          non-zero with >= 1 FAIL line and no load error; every SUPPORT test exits 0 with 0 FAIL lines (its edit stands
#          alone; the red is the product's to fix).
#   B5     GREEN-AFTER: ALL product sections on top -> every .sh product parses (bash -n); every declared test exits 0,
#          0 FAIL lines, >= 1 pass line, no load error.
#   B6     undeclared sibling suites in test_dir that name ANY product's stem (basename minus extension — wider than
#          bash_patch's basename rule): no NEW failure, before/after counts
#          printed (before = with the test sections, without the product sections).
#   B7     shellcheck on each .sh product, INFORMATIONAL.
# Every write verb runs inside <clone-dir>; new tests are QUARANTINED afterwards, never deleted. bash 3.2. Tests run with a
# 120 s budget through python (macOS has no `timeout`). RESULT line: `RESULT: PASS (n/n)` / `RESULT: FAIL (n failed)`.
set -uo pipefail
INPUT="${1:-}"; OUT="${2:-}"; CLONE="${3:-}"
if [ -z "$INPUT" ] || [ -z "$OUT" ] || [ -z "$CLONE" ] || [ ! -f "$INPUT" ] || [ ! -f "$OUT" ] || [ ! -d "$CLONE/.git" ]; then
  echo "usage: checker.sh <input.json> <out.md> <clone-dir>" >&2; exit 1
fi
HERE2="$(cd "$(dirname "$0")" && pwd)"; TASKS="$(dirname "$HERE2")"
BPC="$TASKS/bash_patch/checker.sh"; CODE_DIR="$TASKS/code_patch"; CP2="$TASKS/code_patch2"
REP="$OUT.checker"; mkdir -p "$REP"
FAILS=0; NPASS=0; pass(){ echo "PASS $*"; NPASS=$((NPASS+1)); }; fail(){ echo "FAIL $*"; FAILS=$((FAILS+1)); }
harness_stop(){ fail "$1"; echo "RESULT: FAIL ($FAILS failed) — stopped at $2 (the harness, not the model)"; exit 1; }
stop(){ echo "RESULT: FAIL ($FAILS failed) — stopped at $1"; exit 1; }

jl() { python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); exec(sys.argv[2])' "$INPUT" "$1"; }
TIP="$(jl 'print(d.get("tip") or d.get("repo",{}).get("tip",""))')"
TEST_DIR="$(jl 'print(d.get("test_dir",""))')"; REF_TEST="$(jl 'print(d.get("reference_test_file",""))')"
PRODUCTS="$(jl 'print("\n".join(d.get("product_files") or []))')"
TESTS="$(jl 'print("\n".join(t["path"] for t in d.get("test_files") or []))')"
REDS="$(jl 'print("\n".join(t["path"] for t in d.get("test_files") or [] if t.get("role")=="red"))')"
SUPS="$(jl 'print("\n".join(t["path"] for t in d.get("test_files") or [] if t.get("role")=="support"))')"
NEWTESTS="$(jl 'print("\n".join(t["path"] for t in d.get("test_files") or [] if t.get("status")=="new"))')"
NP="$(printf '%s\n' "$PRODUCTS" | grep -c .)"; NT="$(printf '%s\n' "$TESTS" | grep -c .)"; NR="$(printf '%s\n' "$REDS" | grep -c .)"; NS="$(printf '%s\n' "$SUPS" | grep -c .)"
echo "mode: bash_patch2 (declared: $NP product(s), $NT test(s): $NR red, $NS support)"
[ "$NP" -ge 1 ] && [ "$NP" -le 3 ] && [ "$NT" -ge 1 ] && [ "$NT" -le 4 ] && [ "$NR" -ge 1 ] && [ $((NR+NS)) -eq "$NT" ] \
  || harness_stop "A0 input: bash_patch2 needs product_files 1-3, test_files 1-4 each role red|support, >= 1 red (got $NP / $NT / red $NR support $NS) — build it with tasks/bash_patch2/build_bash_input2.sh" "A0"
[ "$(jl 'print(1 if d.get("self_testing") else 0)')" = 0 ] || harness_stop "A0 input: self_testing is one file — bash_patch's own mode, not bash_patch2" "A0"

# ---------------------------------------------------------------- STAGE 1: bash_patch/checker.sh through B2
python3 - "$INPUT" "$REP/stage1_input.json" <<'PYS'
import json, sys
d = json.load(open(sys.argv[1])); d["suggested_test_file"] = "__bash_patch2_stage1_no_test__"
json.dump(d, open(sys.argv[2], "w"), indent=1, ensure_ascii=False)
PYS
bash "$BPC" "$REP/stage1_input.json" "$OUT" "$CLONE" > "$REP/stage1_checker.out" 2>&1; S1=$?
if [ "$S1" -eq 0 ] || ! grep -q '^FAIL B3 touched-file set is not' "$REP/stage1_checker.out" || ! grep -q '^RESULT: FAIL .*stopped at B3$' "$REP/stage1_checker.out"; then
  # stage 1 stopped BEFORE B3 (B0 / B1 / B2 — a real verdict) or did something unexpected: pass it through as is
  cat "$REP/stage1_checker.out"
  [ "$S1" -eq 0 ] && harness_stop "A0 stage 1 (bash_patch/checker.sh) returned rc 0 with a sentinel test — it must stop at B3" "stage 1"
  exit 1
fi
awk '/^FAIL B3 touched-file set is not/{exit} {print}' "$REP/stage1_checker.out"
NPASS=$((NPASS + $(awk '/^FAIL B3 touched-file set is not/{exit} /^PASS /{n++} END{print n+0}' "$REP/stage1_checker.out")))
[ -f "$REP/sections.json" ] || harness_stop "A0 stage 1 left no sections.json" "stage 1"
# files of the sections for one declared path, in diff order (paths match exactly or by a/ b/ prefix)
secs_for() { python3 -c 'import json,sys
w=sys.argv[2]
for o in json.load(open(sys.argv[1])):
    p=(o.get("path") or ""); p=p[2:] if p.startswith(("a/","b/")) else p
    if p==w: print(o["file"])' "$REP/sections.json" "$1"; }
apply_path() { # apply_path <declared path> <log> — every section of that file, each with its own recorded opts
  local f rc=0
  while IFS= read -r f; do [ -z "$f" ] && continue
    # shellcheck disable=SC2046
    git -C "$CLONE" apply -p1 $(cat "$f.opts" 2>/dev/null) "$f" >> "$2" 2>&1 || rc=1
  done <<< "$(secs_for "$1")"
  return $rc
}

# ---------------------------------------------------------------- B3 declared touched set
for p in $PRODUCTS $TESTS; do
  if git -C "$CLONE" status --porcelain --untracked-files=all -- "$p" | grep -q .; then harness_stop "B3 the clone is not pristine at $p before any apply ($(git -C "$CLONE" status --porcelain -- "$p" | head -1))" "B3"; fi
done
TOUCHED="$(for sf in "$REP"/section_*.diff; do git -C "$CLONE" apply --numstat -p1 $(cat "$sf.opts" 2>/dev/null) "$sf" 2>> "$REP/numstat.err" | awk '{print $3}'; done | sort -u)"
B3_OUT="$(python3 - "$TOUCHED" "$PRODUCTS" "$TESTS" "$NEWTESTS" "$REF_TEST" "$TEST_DIR" "$CLONE" "$TIP" "$REP/sections.json" <<'PY3'
import json, subprocess, sys
touched, prods, tests, news, ref, tdir, clone, tip, secs = sys.argv[1:10]
S = lambda s: [x for x in s.split("\n") if x]
touched, P, T, N = set(S(touched)), S(prods), S(tests), set(S(news))
declared = set(P) | set(T); bad = []
missing = sorted(declared - touched); undeclared = sorted(touched - declared)
if missing: bad.append(f"declared but UNTOUCHED: {missing}")
if undeclared: bad.append(f"touched but UNDECLARED: {undeclared}")
if ref and ref in touched and ref not in declared: bad.append(f"the reference test {ref} was touched")
at = lambda p: subprocess.run(["git", "-C", clone, "cat-file", "-e", f"{tip}:{p}"], capture_output=True).returncode == 0
newsec = {}
for o in json.load(open(secs)):
    p = (o.get("path") or ""); p = p[2:] if p.startswith(("a/", "b/")) else p
    newsec.setdefault(p, []).append(open(o["file"], encoding="utf-8", errors="replace").read().startswith("--- /dev/null"))
for t in T:
    if t.rsplit("/", 1)[0] != tdir.rstrip("/"): bad.append(f"{t} is not in test_dir {tdir}")
    if t in N and at(t): bad.append(f"{t} is declared NEW but exists at the tip")
    if t in N and t in newsec and not all(newsec[t]): bad.append(f"{t} is declared NEW but its section is not `--- /dev/null`")
    if t not in N and not at(t): bad.append(f"{t} is declared MODIFIED but is absent at the tip")
for p in P:
    if not at(p): bad.append(f"product {p} is absent at the tip")
if bad: print(" ; ".join(bad)); sys.exit(1)
print("{ " + " , ".join(P) + " } + { " + " , ".join(T) + " }")
PY3
)"; B3RC=$?
if [ "$B3RC" -eq 0 ]; then pass "B3 (bash_patch2) touched-file set == the declared set: $B3_OUT"
elif [ "$B3RC" -eq 1 ]; then fail "B3 (bash_patch2) touched-file set != the declared set: $B3_OUT — touched: $(printf '%s' "$TOUCHED" | tr '\n' ' ')"; stop "B3 (the touched set is not the declared one)"
else harness_stop "B3 MEASURE ERROR: $B3_OUT" "B3"; fi

# ---------------------------------------------------------------- B3b sites (first product) + A3c (union) + A3d (per product)
P1="$(printf '%s\n' "$PRODUCTS" | head -1)"
: > "$REP/b3b_p1.diff"; while IFS= read -r f; do [ -n "$f" ] && cat "$f" >> "$REP/b3b_p1.diff"; done <<< "$(secs_for "$P1")"
SITES="$(python3 - "$INPUT" "$REP/b3b_p1.diff" <<'PYS'
import json, sys
d = json.load(open(sys.argv[1])); sec = open(sys.argv[2], encoding="utf-8").read().split("\n")
minus = {l[1:].strip() for l in sec if l.startswith("-") and not l.startswith("---")}
for s in (d.get("defect_line") or {}).get("sites", []):
    t = (s.get("text_at_tip") or "").strip()
    if s.get("must_change") and t not in minus: print(f"MISSED :{s['line']} {t[:80]}")
    if not s.get("must_change") and t and t in minus: print(f"REMOVED :{s['line']} {t[:80]}")
PYS
)"
if printf '%s' "$SITES" | grep -q '^MISSED'; then fail "B3b must_change site(s) of $(basename "$P1") NOT changed: $(printf '%s' "$SITES" | grep '^MISSED' | tr '\n' '·' | cut -c1-300)"; stop "B3b (a partial fix; the tests are not run)"; fi
if printf '%s' "$SITES" | grep -q '^REMOVED'; then fail "B3c a line the brief says STAYS was removed from $(basename "$P1") (no repair in bash_patch2): $(printf '%s' "$SITES" | grep '^REMOVED' | tr '\n' '·' | cut -c1-300)"; stop "B3c (a stays-line removed)"; fi
N_SITES="$(jl 'print(len([s for s in (d.get("defect_line") or {}).get("sites",[]) if s.get("must_change")]))')"
N_PLUS="$(jl 'print(len((d.get("defect_line") or {}).get("expected_plus",[])))')"
: > "$REP/a3c_products.diff"
while IFS= read -r p; do [ -z "$p" ] && continue; while IFS= read -r f; do [ -n "$f" ] && cat "$f" >> "$REP/a3c_products.diff"; done <<< "$(secs_for "$p")"; done <<< "$PRODUCTS"
o="$(python3 "$CODE_DIR/a3c_plus.py" "$INPUT" "$REP/a3c_products.diff" "__bash_patch2_no_target__" 2>&1)"; r=$?
echo "$o" > "$REP/a3c_union.out"
if [ "$r" -eq 1 ]; then fail "B3b INCOMPLETE (A3c): $(printf '%s\n' "$o" | grep -c .) of $N_PLUS brief '+' line(s) ABSENT from the product sections: $(printf '%s' "$o" | head -3 | cut -c1-90 | tr '\n' '·')"; stop "B3b (a dropped addition)"
elif [ "$r" -ne 0 ]; then harness_stop "A3c MEASURE ERROR rc=$r: $o" "B3b"; fi
A3D_BAD=""
while IFS= read -r p; do
  [ -z "$p" ] && continue; k="$(basename "$p")"
  : > "$REP/a3d_$k.diff"; while IFS= read -r f; do [ -n "$f" ] && cat "$f" >> "$REP/a3d_$k.diff"; done <<< "$(secs_for "$p")"
  # this product's own expected '+' lines (the brief's multiset, filtered to what its section adds), so A3c is satisfied
  # by construction and a3c_plus.py's A3d leg judges exactly this file against ITS tip (files[p], carried whole)
  python3 - "$INPUT" "$REP/a3d_$k.diff" "$REP/a3d_input_$k.json" <<'PYD'
import json, sys
d = json.load(open(sys.argv[1])); sec = open(sys.argv[2], encoding="utf-8", errors="replace").read().split("\n")
pool = [l[1:].strip() for l in sec if l.startswith("+") and not l.startswith("+++")]; keep = []
for e in (d.get("defect_line") or {}).get("expected_plus", []):
    if e.strip() in pool: pool.remove(e.strip()); keep.append(e)
d.setdefault("defect_line", {})["expected_plus"] = keep
json.dump(d, open(sys.argv[3], "w"), ensure_ascii=False)
PYD
  o="$(python3 "$CODE_DIR/a3c_plus.py" "$REP/a3d_input_$k.json" "$REP/a3d_$k.diff" "$p" 2>&1)"; r=$?
  echo "$o" > "$REP/a3d_$k.out"
  if [ "$r" -eq 2 ]; then A3D_BAD="$A3D_BAD $k: $(printf '%s' "$o" | sed 's/^A3D //' | head -3 | cut -c1-90 | tr '\n' '·')"
  elif [ "$r" -ne 0 ]; then harness_stop "A3d MEASURE ERROR rc=$r for $p: $o" "B3b"; fi
done <<< "$PRODUCTS"
if [ -n "$A3D_BAD" ]; then fail "B3b CONTEXT MARKED AS ADDITION (A3d) — '+' line(s) already at a product's tip and not in the brief:$A3D_BAD"; stop "B3b (a context line marked '+')"; fi
pass "B3b $N_SITES must_change site(s) of $(basename "$P1") are '-' lines, no stays-site removed; all $N_PLUS brief '+' line(s) are in the product sections (multiset); no tip line re-added in any product (A3d)"

# ---------------------------------------------------------------- B3x per-file byte identity
python3 "$CP2/brief_bytes.py" "$INPUT" "$REP/sections.json" > "$REP/brief_bytes.out" 2>&1; BXRC=$?
BX_SUM="$(grep -m1 '^SUMMARY' "$REP/brief_bytes.out")"
if [ "$BXRC" -eq 0 ] && grep -q '^OK ' "$REP/brief_bytes.out"; then
  pass "B3x every declared file's '+' lines are byte-identical to the brief's, in order ($BX_SUM)"
  grep '^UNMEASURED' "$REP/brief_bytes.out" | sed 's/^/INFO B3x /'
elif [ "$BXRC" -eq 0 ]; then echo "INFO B3x no declared file has brief lines attributable to it — byte identity not measured ($BX_SUM)"
elif [ "$BXRC" -eq 1 ]; then fail "B3x BYTE IDENTITY — $(grep -m2 '^DIFF' "$REP/brief_bytes.out" | cut -c1-300 | tr '\n' '·') ($BX_SUM)"; stop "B3x (an added line is not the brief's, byte for byte; the tests are not run)"
else harness_stop "B3x MEASURE ERROR rc=$BXRC: $(head -2 "$REP/brief_bytes.out" | tr '\n' ' ')" "B3x"; fi

# run helper (bash_patch's own, same regexes): bash <file> from the clone root, 120 s budget
run_suite() {  # $1 = repo-relative test path, $2 = report prefix
  python3 - "$CLONE" "$1" "$REP/$2" <<'PY'
import subprocess,sys,re
clone,test,prefix=sys.argv[1:4]
try:
    r=subprocess.run(["bash",test],cwd=clone,capture_output=True,text=True,timeout=120); rc=r.returncode; out=r.stdout+"\n"+r.stderr; to=False
except subprocess.TimeoutExpired as e:
    dec=lambda x: x.decode("utf-8","replace") if isinstance(x,bytes) else (x or "")
    rc=124; out=dec(e.stdout)+"\n"+dec(e.stderr); to=True
open(prefix+".out","w",encoding="utf-8").write(out)
nf=len(re.findall(r"^\s*FAIL[: ]",out,re.M)); npass=len(re.findall(r"^\s*(PASS|ok)[: ]",out,re.M))
load=bool(re.search(r"(syntax error|command not found|unbound variable|No such file or directory: .*\.test\.sh)",out))
print(f"rc={rc} fail_lines={nf} pass_lines={npass} load_error={int(load)} timeout={int(to)}")
PY
}
kv() { printf '%s' "$1" | sed -E "s/.*$2=([0-9]+).*/\\1/"; }
Q="$CLONE/../quarantine/$(date +%Y%m%d-%H%M%S)_bash2"
restore() {
  local p; for p in $PRODUCTS; do git -C "$CLONE" checkout -q -- "$p" 2>> "$REP/restore.err"; done
  for p in $TESTS; do
    if printf '%s\n' "$NEWTESTS" | grep -qxF "$p"; then [ -e "$CLONE/$p" ] && { mkdir -p "$Q"; mv "$CLONE/$p" "$Q/$(basename "$p")"; }
    else git -C "$CLONE" checkout -q -- "$p" 2>> "$REP/restore.err"; fi
  done
  echo "clone restored (products + modified tests checked out at the tip; new tests quarantined to $Q, never deleted)"
}

# ---------------------------------------------------------------- B4 red-first (ALL test sections, NO product section)
: > "$REP/apply_test.out"
for t in $TESTS; do apply_path "$t" "$REP/apply_test.out" || { fail "B4 the test section(s) for $t did not apply alone: $(tail -3 "$REP/apply_test.out" | tr '\n' ' ')"; restore; stop "B4"; }; done
B4_BAD=""; B4_OK=""; i=0
for t in $TESTS; do
  i=$((i+1))
  if ! bash -n "$CLONE/$t" > "$REP/test_syntax_$i.out" 2>&1; then B4_BAD="$B4_BAD $(basename "$t"): does not parse (bash -n: $(head -1 "$REP/test_syntax_$i.out"));"; continue; fi
  R="$(run_suite "$t" "red_first_$i")"; echo "B4 $(basename "$t") ($(printf '%s\n' "$REDS" | grep -qxF "$t" && echo RED || echo SUPPORT)) with the test edits alone: $R"
  rc="$(kv "$R" rc)"; nf="$(kv "$R" fail_lines)"; ld="$(kv "$R" load_error)"; to="$(kv "$R" timeout)"
  if [ "$to" = 1 ]; then B4_BAD="$B4_BAD $(basename "$t"): did not finish in 120 s (a hang, not a red);"
  elif [ "$ld" = 1 ]; then B4_BAD="$B4_BAD $(basename "$t"): a LOAD error (syntax/command/unbound — a test-side defect, not a red): $(grep -m1 -E 'syntax error|command not found|unbound variable' "$REP/red_first_$i.out" | cut -c1-120);"
  elif printf '%s\n' "$REDS" | grep -qxF "$t"; then
    if [ "$rc" -ne 0 ] && [ "$nf" -ge 1 ]; then B4_OK="$B4_OK $(basename "$t")=RED(rc $rc, $nf FAIL)"
    else B4_BAD="$B4_BAD $(basename "$t"): declared RED but NOT red before the product sections (rc=$rc, $nf FAIL line(s)) — it does not prove the defect;"; fi
  else
    if [ "$rc" -eq 0 ] && [ "$nf" -eq 0 ]; then B4_OK="$B4_OK $(basename "$t")=green-support"
    else B4_BAD="$B4_BAD $(basename "$t"): declared SUPPORT but NOT green with the test edits alone (rc=$rc, $nf FAIL line(s)) — its edit does not stand alone: $(grep -m1 -E '^\s*FAIL' "$REP/red_first_$i.out" | cut -c1-100);"; fi
  fi
done
if [ -n "$B4_BAD" ]; then fail "B4 RED-FIRST:$B4_BAD"; restore; stop "B4 (the red proves nothing)"; fi
pass "B4 RED-FIRST: with every test section and no product section —$B4_OK"

# ---------------------------------------------------------------- B6 baseline (undeclared siblings, before the products)
# named by the product's STEM (basename minus its extension) — wider than bash_patch's basename: a suite that reads the
# product's artefact (`04-container-trivy.json`) is driven by it too (measured on KS-1274: 3 such suites, 0 by basename)
SIBS="$(for p in $PRODUCTS; do b="$(basename "$p")"; grep -l -F "${b%.*}" "$CLONE/$TEST_DIR"/*.test.sh 2>> "$REP/sibs.err"; done | sort -u | while IFS= read -r s; do rel="${s#$CLONE/}"; printf '%s\n' "$TESTS" | grep -qxF "$rel" || echo "$rel"; done)"
i=0; SIB_BEFORE=""
for s in $SIBS; do i=$((i+1)); r="$(run_suite "$s" "sib${i}_before")"; SIB_BEFORE="$SIB_BEFORE|$s=$r"; done

# ---------------------------------------------------------------- B5 green-after (ALL product sections on top)
: > "$REP/apply_product.out"
for p in $PRODUCTS; do apply_path "$p" "$REP/apply_product.out" || { fail "B5 the product section(s) for $p did not apply on top of the tests: $(tail -3 "$REP/apply_product.out" | tr '\n' ' ')"; restore; stop "B5"; }; done
for p in $PRODUCTS; do cp "$CLONE/$p" "$REP/after_$(basename "$p")"; done
SYN_BAD=""
for p in $PRODUCTS; do case "$p" in *.sh) bash -n "$CLONE/$p" > "$REP/product_syntax_$(basename "$p").out" 2>&1 || SYN_BAD="$SYN_BAD $(basename "$p"): $(head -1 "$REP/product_syntax_$(basename "$p").out")";; *) echo "INFO B5a $(basename "$p") is not a .sh — bash -n not applicable";; esac; done
if [ -n "$SYN_BAD" ]; then fail "B5a a product does not parse after the patch (bash -n):$SYN_BAD"; restore; stop "B5a"; else pass "B5a every .sh product parses after the patch (bash -n)"; fi
G_BAD=""; G_OK=""; i=0
for t in $TESTS; do
  i=$((i+1)); G="$(run_suite "$t" "green_after_$i")"; echo "B5 $(basename "$t") after every product section: $G"
  g_rc="$(kv "$G" rc)"; g_nf="$(kv "$G" fail_lines)"; g_np="$(kv "$G" pass_lines)"; g_ld="$(kv "$G" load_error)"
  if [ "$g_rc" -eq 0 ] && [ "$g_nf" -eq 0 ] && [ "$g_ld" = 0 ] && [ "$g_np" -ge 1 ]; then G_OK="$G_OK $(basename "$t")(${g_np} pass)"
  else G_BAD="$G_BAD $(basename "$t"): rc=$g_rc, $g_nf FAIL, $g_np pass, load_error=$g_ld: $(grep -m1 -E '^\s*FAIL' "$REP/green_after_$i.out" | cut -c1-100);"; fi
done
if [ -z "$G_BAD" ]; then pass "B5 GREEN-AFTER: every declared test passes with all $NP product section(s):$G_OK"
else fail "B5 GREEN-AFTER: still red (or empty) after the product sections:$G_BAD"; fi

# ---------------------------------------------------------------- B6 after
i=0; NEWRED=""; COUNTS=""
for s in $SIBS; do i=$((i+1)); a="$(run_suite "$s" "sib${i}_after")"; b="$(printf '%s' "$SIB_BEFORE" | tr '|' '\n' | grep -F "$s=" | sed 's/^[^=]*=//')"
  b_nf="$(kv "$b" fail_lines)"; a_nf="$(kv "$a" fail_lines)"; b_np="$(kv "$b" pass_lines)"; a_np="$(kv "$a" pass_lines)"
  COUNTS="$COUNTS $(basename "$s") ${b_np}p/${b_nf}f->${a_np}p/${a_nf}f;"
  [ "${a_nf:-0}" -gt "${b_nf:-0}" ] && NEWRED="$NEWRED $s(before=$b_nf after=$a_nf)"; done
if [ -z "$SIBS" ]; then echo "INFO B6 no undeclared suite in $TEST_DIR names a product's stem — nothing else drives them (stated, not counted)"
elif [ -z "$NEWRED" ]; then pass "B6 undeclared sibling suite(s) naming a product: no NEW failure after ($(printf '%s\n' "$SIBS" | grep -c .) suite(s):$COUNTS)"
else fail "B6 NEW failure(s) in undeclared sibling suite(s) after the patch:$NEWRED (counts:$COUNTS)"; fi
# ---------------------------------------------------------------- B7 shellcheck (informational)
if command -v shellcheck > "$REP/shellcheck_which.out" 2>&1; then
  for p in $PRODUCTS; do case "$p" in *.sh) shellcheck -S warning "$REP/after_$(basename "$p")" > "$REP/shellcheck_$(basename "$p").out" 2>&1; echo "INFO B7 shellcheck $(basename "$p") rc=$? (informational)";; esac; done
else echo "INFO B7 shellcheck not installed (informational)"; fi
restore
APPLY_MODE="strict"; grep -q '^PASS B2 every section applies at the tip (strict)$' "$REP/stage1_checker.out" || APPLY_MODE="accommodated (see the B2 line)"
echo "SUMMARY files=$((NP+NT)) products=$NP tests=$NT red=$NR support=$NS red_first=yes apply_mode=$APPLY_MODE"
if [ "$FAILS" -eq 0 ]; then echo "RESULT: PASS ($NPASS/$NPASS)"; exit 0; fi
echo "RESULT: FAIL ($FAILS failed)"; exit 1
