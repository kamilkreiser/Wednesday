#!/bin/bash
# config_tier_arms.sh — arms for the CONFIG TIER in night/build_input.sh (2026-10-26, Wednesday tooling; KS-1391 / KS-1289).
# Run as:  /bin/bash <abs path>/config_tier_arms.sh   (SPARK_TEST_TMP=<scratch dir> optional; NO_CONTROLS=1 skips the 4 slow --control arms)
#
# The tier: a narrow allow-list of repo CONFIG product files that were refused "product path is neither services/* nor
# packages/shared". EXACTLY: <frontend|services|packages>/<x>/package.json and `.dockerignore` files. Nothing else.
#
# NO MODEL CALL: dry-runs build the input only; --control puts the brief's golden.diff in place of a model answer.
# Arms 1-2 pin override_not_runnable=<reason> because both briefs' headers still say NOT RUNNABLE (a brief-text fact the
# README's pin exists for); the pin is on the command line here, in no file.
#   1  KS-1391 dry-run                       -> ACCEPTED (DRY-RUN OK)
#   2  KS-1289 dry-run                       -> ACCEPTED (DRY-RUN OK)
#   3  .github/workflows/x.yml               -> REFUSED by the builder's classifier
#   4  Blockchain/Dev/.env                   -> REFUSED
#   5a services/foo/src/a.ts                 -> passes the classifier (stops later: services/foo does not exist at the tip)
#   5b a real existing services/ brief       -> OLD builder (.pre-1026-configtier) == NEW builder, stdout + input.json bytes
#   6  package-lock.json                     -> REFUSED
#   7a-7g more negatives (lockfile under a package, Dockerfile, nested package.json, .dockerignore.bak, '..', root package.json)
#   C1 KS-1391 --control (golden)            -> CONTROL-PASS, 7/7, red leg by assertion
#   C2 KS-1289 --control (golden)            -> CONTROL-PASS
#   B1 KS-1391 golden with `vitest run` -> `vitest`  (deliberate break)  -> must FAIL (cell R1 stays red after the patch)
#   B2 KS-1289 golden with `**/__tests__` -> `**/__test__` (break)       -> must FAIL
#   B3,B4 the same breaks written into brief AND golden (A3c passes) -> must FAIL at A5 (the runner is reached)
# rc 0 all arms PASS · 1 any FAIL. bash 3.2; no cd; nothing deleted.
set -uo pipefail
SPARK="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; LM="$(dirname "$SPARK")"
BR="$LM/night/briefs"; OLD="$LM/night/build_input.sh.pre-1026-configtier"; NEW="$LM/night/build_input.sh"
T="${SPARK_TEST_TMP:-$(mktemp -d "${TMPDIR:-/tmp}/cfg_arms.XXXXXX")}"; mkdir -p "$T"
P=0; F=0
ok()  { echo "ARM PASS $*"; P=$((P+1)); }
bad() { echo "ARM FAIL $*"; F=$((F+1)); }
echo "config_tier_arms: fixtures in $T"
NOTRUN="override_not_runnable=config-tier-now-exists-2026-10-26"
rround() { # rround <out> <cmd...> : retry while BUSY (the ONE-request lock)
  local out="$1"; shift; local i=0 rc
  while :; do
    "$@" > "$out" 2>&1; rc=$?
    if [ "$rc" -eq 3 ] && tail -1 "$out" | /usr/bin/grep -q "BUSY" && [ "$i" -lt 180 ]; then i=$((i+1)); sleep 10; continue; fi
    return "$rc"
  done
}
verdict() { /usr/bin/grep '^SPARK ROUND' "$1" | tail -1 | cut -c1-330; }

# ---- 1, 2: dry-run ACCEPTED
for k in 1391 1289; do
  n=1; [ "$k" = 1289 ] && n=2
  rround "$T/dry$k.out" bash "$SPARK/round.sh" "$BR/ks_${k}_p1" --dry-run "$NOTRUN" < /dev/null; rc=$?
  line="$(verdict "$T/dry$k.out")"
  if [ "$rc" -eq 0 ] && echo "$line" | /usr/bin/grep -q 'DRY-RUN OK'; then ok "$n KS-$k dry-run ACCEPTED rc=0 :: $line"; else bad "$n KS-$k dry-run rc=$rc :: $line"; fi
done

# ---- direct builder arms: ticket KS-1391 (Todo), its brief, product= pinned to the path under test
bld() { # bld <builder> <product-pin> <out.json> -> prints builder stdout+stderr; rc via $?
  NIGHT_SOURCE_CHECKOUT="$SPARK/cache/src" NIGHT_BRIEFS_DIR="$BR/ks_1391_p1" bash "$1" KS-1391 "$3" "product=$2" ref=Blockchain/Dev/frontend/issuer/src/__tests__/provenance-timeline.test.tsx line=10 < /dev/null 2>&1
}
refuse_arm() { # refuse_arm <id> <product>
  local id="$1" prod="$2" out rc line
  out="$(bld "$NEW" "$prod" "$T/ref_$id.json")"; rc=$?
  line="$(echo "$out" | /usr/bin/grep -m1 'REFUSED')"
  if [ "$rc" -eq 2 ] && echo "$line" | /usr/bin/grep -q 'product path is neither services/\* nor packages/shared' && [ ! -e "$T/ref_$id.json" ]; then
    ok "$id product=$prod REFUSED rc=2 :: $line"
  else bad "$id product=$prod rc=$rc (want 2 + the classifier refusal, no input.json) :: ${line:-no REFUSED line: $(echo "$out" | tail -1 | cut -c1-200)}"; fi
}
refuse_arm 3  ".github/workflows/x.yml"
refuse_arm 4  "Blockchain/Dev/.env"
refuse_arm 6  "package-lock.json"
refuse_arm 7a "Blockchain/Dev/frontend/issuer/package-lock.json"
refuse_arm 7b "Blockchain/Dev/frontend/issuer/Dockerfile"
refuse_arm 7c "Blockchain/Dev/frontend/issuer/sub/package.json"
refuse_arm 7d "Blockchain/Dev/.dockerignore.bak"
refuse_arm 7e "Blockchain/Dev/../.dockerignore"
refuse_arm 7f "Blockchain/Dev/package.json"
refuse_arm 7g "Blockchain/Dev/frontend/issuer/.env.production"

# ---- 5a: an existing-class path still gets PAST the classifier
out="$(bld "$NEW" "services/foo/src/a.ts" "$T/five_a.json")"; rc=$?
line="$(echo "$out" | /usr/bin/grep -m1 'REFUSED')"
if echo "$line" | /usr/bin/grep -q 'neither services'; then bad "5a services/foo/src/a.ts hit the classifier refusal :: $line"
elif [ "$rc" -eq 2 ] && echo "$line" | /usr/bin/grep -q 'services/foo/package.json is not at the tip'; then
  ok "5a services/foo/src/a.ts passes the classifier; stops at the next gate (services/foo does not exist) rc=2 :: $line"
else bad "5a services/foo/src/a.ts rc=$rc :: ${line:-$(echo "$out" | tail -1 | cut -c1-200)}"; fi

# ---- 5b: real services/ brief: OLD builder vs NEW builder, byte for byte (first code_patch brief the OLD builder accepts)
pick=""
for d in ks_1705_p1; do pick="$BR/$d"; done
LO="$(python3 "$SPARK/brief_lint.py" "$pick" 2>/dev/null)"; eval "$LO"
mkdir -p "$T/old" "$T/new"
NIGHT_SOURCE_CHECKOUT="$SPARK/cache/src" NIGHT_BRIEFS_DIR="$pick" bash "$OLD" "$B_TICKET" "$T/old/input.json" "${B_PINS_ARR[@]}" < /dev/null > "$T/old/stdout" 2>&1; orc=$?
NIGHT_SOURCE_CHECKOUT="$SPARK/cache/src" NIGHT_BRIEFS_DIR="$pick" bash "$NEW" "$B_TICKET" "$T/new/input.json" "${B_PINS_ARR[@]}" < /dev/null > "$T/new/stdout" 2>&1; nrc=$?
sed "s#$T/old/#X/#g; s#ticket .* updated .*#ticket-line#" "$T/old/stdout" > "$T/old/stdout.n"; sed "s#$T/new/#X/#g; s#ticket .* updated .*#ticket-line#" "$T/new/stdout" > "$T/new/stdout.n"
if [ "$orc" -eq "$nrc" ] && cmp -s "$T/old/stdout.n" "$T/new/stdout.n" && { [ "$orc" -ne 0 ] || cmp -s "$T/old/input.json" "$T/new/input.json"; }; then
  ok "5b $(basename "$pick") (product $B_FILE) OLD rc=$orc == NEW rc=$nrc; stdout identical$([ "$orc" -eq 0 ] && echo ", input.json byte-identical") :: $(tail -1 "$T/new/stdout" | cut -c1-200)"
else bad "5b $(basename "$pick") OLD rc=$orc vs NEW rc=$nrc differ (diff: $(diff "$T/old/stdout.n" "$T/new/stdout.n" | head -3 | tr '\n' ' '))"; fi
if [ "$orc" -eq 0 ]; then
  rround "$T/dry5b.out" bash "$SPARK/round.sh" "$pick" --dry-run < /dev/null; rc=$?; line="$(verdict "$T/dry5b.out")"
  if [ "$rc" -eq 0 ] && echo "$line" | /usr/bin/grep -q 'DRY-RUN OK'; then ok "5c $(basename "$pick") round.sh --dry-run ACCEPTED rc=0 :: $line"; else bad "5c $(basename "$pick") dry-run rc=$rc :: $line"; fi
fi

# ---- controls + deliberate breaks (no model call; ~2 min each)
if [ "${NO_CONTROLS:-0}" != 1 ]; then
  for k in 1391 1289; do
    n=C1; [ "$k" = 1289 ] && n=C2
    rround "$T/ctl$k.out" bash "$SPARK/round.sh" "$BR/ks_${k}_p1" --control "$NOTRUN" < /dev/null; rc=$?; line="$(verdict "$T/ctl$k.out")"
    if [ "$rc" -eq 0 ] && echo "$line" | /usr/bin/grep -q 'CONTROL-PASS' && echo "$line" | /usr/bin/grep -q 'BYTE-IDENTICAL'; then ok "$n KS-$k --control golden :: $line"; else bad "$n KS-$k --control rc=$rc :: $line"; fi
  done
  python3 - "$BR" "$T" <<'PY'
import os, sys
br, t = sys.argv[1:3]
def mk(name, ks, old, new):
    src = os.path.join(br, f"ks_{ks}_p1"); d = os.path.join(t, name); os.makedirs(d, exist_ok=True)
    for fn in os.listdir(src):
        s = open(os.path.join(src, fn), encoding="utf-8").read()
        if fn == "golden.diff":
            assert s.count(old) == 1, (name, s.count(old)); s = s.replace(old, new)
        open(os.path.join(d, fn), "w", encoding="utf-8").write(s)
mk("cfgbreak_ks1391", "1391", '+    "test": "vitest run",', '+    "test": "vitest",')
mk("cfgbreak_ks1289", "1289", "+**/__tests__\n", "+**/__test__\n")
# B3/B4: the SAME break written consistently into the brief AND the golden, so A3c (brief == hunk) passes and the checker must
# reach the runner: the new test's RED cell still expects the real value, so it must stay red AFTER the (wrong) product hunk (A5).
def mk2(name, ks, old, new):
    src = os.path.join(br, f"ks_{ks}_p1"); d = os.path.join(t, name); os.makedirs(d, exist_ok=True)
    for fn in os.listdir(src):
        s = open(os.path.join(src, fn), encoding="utf-8").read()
        if fn in ("golden.diff", f"KS-{ks}.md"):
            assert s.count(old) == 1, (name, fn, s.count(old)); s = s.replace(old, new)
        open(os.path.join(d, fn), "w", encoding="utf-8").write(s)
mk2("cfgbreak2_ks1391", "1391", '+    "test": "vitest run",', '+    "test": "vitest",')
mk2("cfgbreak2_ks1289", "1289", "+**/__tests__\n", "+**/__test__\n")
PY
  for k in 1391 1289; do
    n=B1; [ "$k" = 1289 ] && n=B2
    rround "$T/brk$k.out" bash "$SPARK/round.sh" "$T/cfgbreak_ks$k" --control "$NOTRUN" < /dev/null; rc=$?; line="$(verdict "$T/brk$k.out")"
    if [ "$rc" -eq 1 ] && echo "$line" | /usr/bin/grep -q 'CONTROL-FAIL'; then ok "$n KS-$k broken golden FAILS as it must rc=1 :: $line"; else bad "$n KS-$k broken golden rc=$rc (want 1 CONTROL-FAIL) :: $line"; fi
  done
  for k in 1391 1289; do
    n=B3; [ "$k" = 1289 ] && n=B4
    rround "$T/brk2$k.out" bash "$SPARK/round.sh" "$T/cfgbreak2_ks$k" --control "$NOTRUN" < /dev/null; rc=$?; line="$(verdict "$T/brk2$k.out")"
    rd="$(sed -n 's/^SPARK ROUND [^:]*: .* · \(\/[^ ]*\)$/\1/p' "$T/brk2$k.out" | tail -1)"
    why="$(/usr/bin/grep -m1 '^FAIL' "$rd/checker.out" 2>/dev/null | cut -c1-200)"
    if [ "$rc" -eq 1 ] && echo "$why" | /usr/bin/grep -q 'A5'; then ok "$n KS-$k consistent-but-wrong product line FAILS at A5 (runner reached) :: $why"; else bad "$n KS-$k consistent break rc=$rc (want 1, FAIL A5) :: ${why:-$line}"; fi
  done
fi
echo "config_tier_arms: $P passed, $F failed"
[ "$F" -eq 0 ]
