#!/bin/bash
# frontend_scan_arms.sh — arms for the FRONTEND SOURCE-SCAN tier widening (2026-11-12, operator o151, KS-1104).
# Admits EXACTLY Blockchain/Dev/frontend/verifier/src/**/*.tsx as a code_patch2 PRODUCT, ONLY when the brief's pins carry scan_host=packages/shared
# (the test is a source-scan cell hosted in packages/shared, which has the runner; verifier has none). Dry-runs only: no model, no clone writes.
# Run: bash local-model/spark/tests/frontend_scan_arms.sh
#   a  ADMIT   verifier .tsx + scan_host=packages/shared + ref=            -> round.sh --dry-run rc 0, FRONTEND SOURCE-SCAN TIER banner
#   b  REFUSE  same, NO scan_host (no host named)                          -> rc != 0, the old FRONTEND TIER refusal (no vitest config), no new banner
#   c  REFUSE  a DIFFERENT frontend dir (frontend/website) WITH scan_host   -> rc != 0, no new banner
#   d  REFUSE  scan_host= names some other host (services/x)               -> rc != 0, no new banner
#   e  REGEX   path shape: frontend/verifier/src/**/*.tsx only (.ts, '..', other dir, outside src all excluded)
#   f  MUTANT  builder with the scan_host guard removed: arm b's brief takes the NEW branch (so arm b can fail); and a builder2 with the
#              exemption removed REFUSES arm a's brief (so the code_patch2 exemption is proved load-bearing)
set -uo pipefail
SPARK="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; LM="$(dirname "$SPARK")"
SRC="$LM/night/briefs/ks_678_o147_p3_spec_examples_guard_e10_url_host"
FX="$LM/spark/tests/fixtures/fescan"; mkdir -p "$FX"
FAILS=0; ok(){ echo "ok   $*"; }; bad(){ echo "FAIL $*"; FAILS=$((FAILS+1)); }
TF="Blockchain/Dev/packages/shared/src/__tests__/ks256-spec-example-contract.test.ts"   # the brief body names this EXISTING test (modified in place); only the product File: changes
REF="Blockchain/Dev/packages/shared/src/__tests__/ks1564-admin-api-keys-page-sends-no-default-org.test.ts"
mk() { # mk <name> <first-file-path> <scan_host|-> : the KS-678 brief with its FIRST File: replaced; pins = tier + ref (+ scan_host)
  local d="$FX/$1"; mkdir -p "$d"
  { echo "# fixture (o151 arm $1)"; echo "tier=code_patch2"; echo "test_file=$TF"; echo "ref=$REF"; [ "$3" != "-" ] && echo "scan_host=$3"; echo "line=1"; echo "ctx=65536"; } > "$d/spark.pins"
  python3 - "$SRC/KS-678.md" "$d/KS-678.md" "$2" <<'PY'
import re, sys
t = open(sys.argv[1], encoding="utf-8").read()
t = re.sub(r"(?m)^File:\s*`[^`]+`", lambda m, n=[0]: m.group(0) if n.__setitem__(0, n[0] + 1) or n[0] > 1 else "File: `" + sys.argv[3] + "`", t, count=0)
open(sys.argv[2], "w", encoding="utf-8").write(t)
PY
}
bld() { # bld <builder2.sh> <briefdir> <out.json>  -> builder2 stdout+stderr (rc via $?)
  local LO; LO="$(python3 "$SPARK/brief_lint.py" "$2" 2>/dev/null)"; eval "$LO"
  NIGHT_SOURCE_CHECKOUT="$SPARK/cache/src" NIGHT_BRIEFS_DIR="$2" bash "$1" "$B_TICKET" "$3" "$B_BRIEF" "${B_PINS_ARR[@]}" < /dev/null 2>&1
}
O="${ARMS_OUT:-$FX}"
VER="Blockchain/Dev/frontend/verifier/src/components/VerifyPage.tsx"
NEWB="FRONTEND SOURCE-SCAN TIER"
mk a "$VER" packages/shared
bld "$LM/tasks/code_patch2/build_input2.sh" "$FX/a" "$O/a.json" > "$O/arm_a.out"; rca=$?
if [ "$rca" = 0 ] && /usr/bin/grep -q "$NEWB" "$O/arm_a.out"; then ok "a verifier .tsx + scan_host admitted by builder2 (rc 0, tier banner)"; else bad "a rc=$rca: $(tail -2 "$O/arm_a.out" | cut -c1-300)"; fi
mk b "$VER" -
bld "$LM/tasks/code_patch2/build_input2.sh" "$FX/b" "$O/b.json" > "$O/arm_b.out"; rcb=$?
if [ "$rcb" != 0 ] && ! /usr/bin/grep -q "$NEWB" "$O/arm_b.out" && /usr/bin/grep -qi "no vitest config" "$O/arm_b.out"; then ok "b no scan_host: still refused (rc $rcb, old no-vitest-config refusal)"; else bad "b rc=$rcb: $(tail -2 "$O/arm_b.out" | cut -c1-300)"; fi
mk c "Blockchain/Dev/frontend/website/src/App.tsx" packages/shared
bld "$LM/tasks/code_patch2/build_input2.sh" "$FX/c" "$O/c.json" > "$O/arm_c.out"; rcc=$?
if [ "$rcc" != 0 ] && ! /usr/bin/grep -q "$NEWB" "$O/arm_c.out" && /usr/bin/grep -q "frontend package frontend/website has no vitest config" "$O/arm_c.out"; then ok "c frontend/website + scan_host: still refused by the old frontend tier (rc $rcc)"; else bad "c rc=$rcc: $(tail -2 "$O/arm_c.out" | cut -c1-300)"; fi
mk d "$VER" services/originate
bld "$LM/tasks/code_patch2/build_input2.sh" "$FX/d" "$O/d.json" > "$O/arm_d.out"; rcd=$?
if [ "$rcd" != 0 ] && ! /usr/bin/grep -q "$NEWB" "$O/arm_d.out" && /usr/bin/grep -qi "no vitest config" "$O/arm_d.out"; then ok "d scan_host=services/originate: still refused (rc $rcd)"; else bad "d rc=$rcd: $(tail -2 "$O/arm_d.out" | cut -c1-300)"; fi
python3 - <<'PY' && ok "e regex: frontend/verifier/src/**/*.tsx only" || bad "e regex"
import re
R = r"frontend/verifier/src/[A-Za-z0-9_\-./]+\.tsx"
assert re.fullmatch(R, "frontend/verifier/src/components/VerifyPage.tsx")
for x in ("frontend/verifier/src/x.ts", "frontend/verifier/src/a.tsx.bak", "frontend/verifier/lib/x.tsx", "frontend/admin/src/x.tsx", "frontend/verifier-x/src/x.tsx", "services/x/src/x.tsx"):
    assert not re.fullmatch(R, x), x
assert ".." in "frontend/verifier/src/../../admin/src/x.tsx".split("/")   # the builder also refuses any '..' segment
PY
# ---- f: mutants
mkdir -p "$FX/mut/night" "$FX/mut/tasks/code_patch2"
sed 's/ and pins.get("scan_host", "") == "packages\/shared":/:/' "$LM/night/build_input.sh" > "$FX/mut/night/build_input.sh"
if cmp -s "$LM/night/build_input.sh" "$FX/mut/night/build_input.sh"; then bad "f1 mutant identical (scan_host guard text not found)"; else
  cp "$LM/tasks/code_patch2/build_input2.sh" "$FX/mut/tasks/code_patch2/build_input2.sh"
  bld "$FX/mut/tasks/code_patch2/build_input2.sh" "$FX/b" "$O/f1.json" > "$O/arm_f1.out"; rcf=$?
  if /usr/bin/grep -q "$NEWB" "$O/arm_f1.out"; then ok "f1 MUTANT (scan_host guard removed) sends the NO-HOST brief to the NEW branch (rc $rcf): arm b can fail"; else bad "f1 mutant did not change the branch: $(tail -2 "$O/arm_f1.out" | cut -c1-300)"; fi
fi
sed 's/ and (_SPEC.match(p) or _fe_ok(p)))/ and _SPEC.match(p))/' "$LM/tasks/code_patch2/build_input2.sh" > "$FX/mut/tasks/code_patch2/build_input2.sh"
cp "$LM/night/build_input.sh" "$FX/mut/night/build_input.sh"
if cmp -s "$LM/tasks/code_patch2/build_input2.sh" "$FX/mut/tasks/code_patch2/build_input2.sh"; then bad "f2 mutant identical (exemption text not found)"; else
  bld "$FX/mut/tasks/code_patch2/build_input2.sh" "$FX/a" "$O/f2.json" > "$O/arm_f2.out"; rcg=$?
  if [ "$rcg" != 0 ] && /usr/bin/grep -q "not under the ONE service" "$O/arm_f2.out"; then ok "f2 MUTANT (builder2 exemption removed) REFUSES arm a's brief (rc $rcg): the exemption is load-bearing"; else bad "f2 rc=$rcg: $(tail -2 "$O/arm_f2.out" | cut -c1-300)"; fi
fi
[ "$FAILS" -eq 0 ] && { echo "RESULT: PASS (all arms)"; exit 0; }
echo "RESULT: FAIL ($FAILS)"; exit 1
