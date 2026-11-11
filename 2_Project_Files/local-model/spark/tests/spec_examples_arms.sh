#!/bin/bash
# spec_examples_arms.sh — arms for the SPEC-EXAMPLES GUARD tier widening (2026-11-12, operator o148, KS-678).
# Admits EXACTLY Blockchain/Dev/scripts/spec-examples/check/<name>.mjs as a code_patch2 PRODUCT (test host: the pinned test_file=,
# runner: that package's vitest). Run: bash local-model/spark/tests/spec_examples_arms.sh   (dry-runs only: no model, no clone writes)
#   a  ADMIT   the KS-678 brief (rules-example.mjs + contract.mjs + ks256 test)            -> round.sh --dry-run rc 0 DRY-RUN OK
#   b  REFUSE  same brief, first File: = scripts/preflight/deps-present.sh (code_patch product) -> rc 2/5 naming the tamper-target refusal
#   c  REFUSE  same brief, first File: = scripts/spec-examples/check-spec-examples.mjs (outside check/) -> same refusal
#   d  REFUSE  same brief, first File: = scripts/spec-examples/check/sub/x.mjs shape is excluded by the regex (checked as a regex arm)
#   e  TAMPER  (o149) same admitted path WITH a `## Tamper` heading must take the OLD tamper branch (SCRIPTS TAMPER TARGET, tamper parsed),
#              NOT the new admit branch; e2: the same brief minus the heading takes the NEW branch; e3: a MUTANT builder (the
#              `and not _brief_has_tamper()` guard removed) sends the with-Tamper brief to the NEW branch, so arm e is able to fail
set -uo pipefail
SPARK="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; LM="$(dirname "$SPARK")"
SRC="$LM/night/briefs/ks_678_o147_p3_spec_examples_guard_e10_url_host"
FX="$LM/spark/tests/fixtures/specex"; mkdir -p "$FX"
FAILS=0; ok(){ echo "ok   $*"; }; bad(){ echo "FAIL $*"; FAILS=$((FAILS+1)); }
mk() { # mk <name> <first-file-path>  -> a fixture brief dir whose FIRST `File:` line is replaced (body untouched)
  local d="$FX/$1"; mkdir -p "$d"; cp "$SRC/spark.pins" "$d/spark.pins"
  python3 - "$SRC/KS-678.md" "$d/KS-678.md" "$2" <<'PY'
import re, sys
t = open(sys.argv[1], encoding="utf-8").read()
t = re.sub(r"(?m)^File:\s*`[^`]+`", lambda m, n=[0]: m.group(0) if n.__setitem__(0, n[0] + 1) or n[0] > 1 else "File: `" + sys.argv[3] + "`", t, count=0)
open(sys.argv[2], "w", encoding="utf-8").write(t)
PY
}
run() { bash "$LM/spark/round.sh" "$1" --dry-run > "$2" 2>&1; echo $?; }
O="${ARMS_OUT:-$FX}"
rc=$(run "$SRC" "$O/arm_a.out"); if [ "$rc" = 0 ] && /usr/bin/grep -q "DRY-RUN OK" "$O/arm_a.out" && /usr/bin/grep -q "SPEC-EXAMPLES GUARD TIER" "$(/usr/bin/sed -n 's/^round: run dir: //p' "$O/arm_a.out" | head -1)/build_input.out"; then ok "a KS-678 admitted (rc 0, tier banner)"; else bad "a rc=$rc"; fi
mk b "Blockchain/Dev/scripts/preflight/deps-present.sh"
rc=$(run "$FX/b" "$O/arm_b.out"); if [ "$rc" != 0 ] && /usr/bin/grep -q "admitted ONLY as a test-only tamper target" "$O/arm_b.out"; then ok "b scripts/preflight/*.sh still refused (rc $rc)"; else bad "b rc=$rc: $(tail -1 "$O/arm_b.out" | cut -c1-300)"; fi
mk c "Blockchain/Dev/scripts/spec-examples/check-spec-examples.mjs"
rc=$(run "$FX/c" "$O/arm_c.out"); if [ "$rc" != 0 ] && /usr/bin/grep -q "admitted ONLY as a test-only tamper target" "$O/arm_c.out"; then ok "c spec-examples path outside check/ still refused (rc $rc)"; else bad "c rc=$rc: $(tail -1 "$O/arm_c.out" | cut -c1-300)"; fi
python3 - <<'PY' && ok "d regex: check/<name>.mjs only (subdir, .sh, .ts, sibling dir all excluded)" || bad "d regex"
import re
R = r"scripts/spec-examples/check/[A-Za-z0-9_\-]+\.mjs"
assert re.fullmatch(R, "scripts/spec-examples/check/rules-example.mjs")
for x in ("scripts/spec-examples/check/sub/x.mjs", "scripts/spec-examples/check/x.sh", "scripts/spec-examples/check/x.ts", "scripts/spec-examples/checkx/x.mjs", "scripts/spec-examples/x.mjs", "scripts/preflight/x.mjs", "scripts/spec-examples/check/../x.mjs"):
    assert not re.fullmatch(R, x), x
PY
# ---- e: a scripts/spec-examples/check/*.mjs product WITH a `## Tamper` heading keeps the OLD tamper branch (o149)
mkT() { # mkT <name>: fixture = the KS-678 brief + a valid `## Tamper` block on rules-example.mjs line 74 (read at the pin)
  local d="$FX/$1"; mkdir -p "$d"; cp "$SRC/spark.pins" "$d/spark.pins"; cp "$SRC/KS-678.md" "$d/KS-678.md"
  local ln; ln="$(sed -n '74p' "$SPARK/cache/src/Blockchain/Dev/scripts/spec-examples/check/rules-example.mjs")"
  printf '\n## Tamper (planted by spec_examples_arms.sh arm e)\nline: 74\nfrom: `%s`\nto: `  if (false) return;`\n' "$ln" >> "$d/KS-678.md"
}
bld() { # bld <builder> <briefdir> <out.json> -> builder stdout+stderr; rc via $?
  local LO; LO="$(python3 "$SPARK/brief_lint.py" "$2" 2>/dev/null)"; eval "$LO"
  NIGHT_SOURCE_CHECKOUT="$SPARK/cache/src" NIGHT_BRIEFS_DIR="$2" bash "$1" "$B_TICKET" "$3" "${B_PINS_ARR[@]}" < /dev/null 2>&1
}
mkT e
bld "$LM/night/build_input.sh" "$FX/e" "$O/e.json" > "$O/arm_e.out"; rce=$?
if /usr/bin/grep -q "SCRIPTS TAMPER TARGET" "$O/arm_e.out" && ! /usr/bin/grep -q "SPEC-EXAMPLES GUARD TIER" "$O/arm_e.out" && /usr/bin/grep -q "TEST-ONLY tamper from the brief: .*rules-example.mjs:74" "$O/arm_e.out"; then ok "e scripts/spec-examples/check/*.mjs + ## Tamper takes the OLD tamper branch (rc $rce, tamper parsed at :74)"; else bad "e rc=$rce: $(tail -2 "$O/arm_e.out" | cut -c1-300)"; fi
bld "$LM/night/build_input.sh" "$SRC" "$O/e2.json" > "$O/arm_e2.out"; rce2=$?
if /usr/bin/grep -q "SPEC-EXAMPLES GUARD TIER" "$O/arm_e2.out" && ! /usr/bin/grep -q "SCRIPTS TAMPER TARGET" "$O/arm_e2.out"; then ok "e2 same brief without the heading takes the NEW admit branch (rc $rce2)"; else bad "e2 rc=$rce2: $(tail -2 "$O/arm_e2.out" | cut -c1-300)"; fi
mkdir -p "$FX/mut"; sed 's/ and not _brief_has_tamper():/:/' "$LM/night/build_input.sh" > "$FX/mut/build_input.sh"
if cmp -s "$LM/night/build_input.sh" "$FX/mut/build_input.sh"; then bad "e3 mutant identical to the builder (guard text not found)"; else
  bld "$FX/mut/build_input.sh" "$FX/e" "$O/e3.json" > "$O/arm_e3.out"
  if /usr/bin/grep -q "SPEC-EXAMPLES GUARD TIER" "$O/arm_e3.out" && ! /usr/bin/grep -q "SCRIPTS TAMPER TARGET" "$O/arm_e3.out"; then ok "e3 MUTANT (guard removed) sends the with-Tamper brief to the NEW branch: arm e can fail"; else bad "e3 mutant did not change the branch: $(tail -2 "$O/arm_e3.out" | cut -c1-300)"; fi
fi
[ "$FAILS" -eq 0 ] && { echo "RESULT: PASS (all arms)"; exit 0; }
echo "RESULT: FAIL ($FAILS)"; exit 1
