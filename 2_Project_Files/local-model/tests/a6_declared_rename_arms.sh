#!/bin/bash
# a6_declared_rename_arms.sh — arms for the DECLARED-RENAME allowance in A6 (2026-11-11, commission
# 0_Brain/reference/2026-11-11_harness-declared-rename/commission.md). Run as:  /bin/bash <abs path>/a6_declared_rename_arms.sh
# NO MODEL CALL, NO SPARK ENDPOINT, NO SECUURA CLONE (the test_only_bash fixture stands in). Three layers:
#   D*  the REAL suite-delta script extracted from tasks/code_patch/checker.sh (code_patch / code_patch2 / test_only A6) on hand-made
#       vitest JSON reports: (a) no declaration, rename -> default behaviour; (b) pair, new passes -> PASS; (c) pair, new FAILS -> FAIL;
#       (d) old name never in baseline -> FAIL; (e) pair + an undeclared second change -> FAIL where that script can see it (a NEW red);
#       default byte-identity against the .pre-1111-rename extraction.
#   L*  brief_lint.py: a valid `## Renames` -> accepted + B_RENAMES; wildcard / not one-to-one / malformed / old==new / bash_patch -> rc 2.
#   T*  tiers/tier_checker.py test_only_bash A6 (the tier that actually reads a renamed cell as LOST), real runs on the fixture clone:
#       (a) no declaration -> FAIL LOST; (b) declared pair, new passes -> A6 PASS; (c) declared pair, new FAILS -> FAIL;
#       (d) old never in baseline -> FAIL; (e) pair + an undeclared second disappearance -> FAIL LOST.
# rc 0 all arms behaved as stated, 1 otherwise. bash 3.2; no cd; nothing deleted.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LM="$(cd "$HERE/.." && pwd)"; SPARK="$LM/spark"
ROOT="${A6R_ROOT:-/private/tmp/claude-501/a6r_arms_$(date +%Y%m%d_%H%M%S)_$$}"
case "$ROOT" in /private/tmp/claude-501/*) ;; *) echo "ROOT must be under /private/tmp/claude-501/ ($ROOT)"; exit 1 ;; esac
[ -e "$ROOT" ] && { echo "$ROOT already exists"; exit 1; }
mkdir -p "$ROOT/d"
P=0; F=0
ok()  { echo "ARM PASS $*"; P=$((P+1)); }
bad() { echo "ARM FAIL $*"; F=$((F+1)); }

# ------------------------------------------------------------ D: the real delta script
extract() { awk '/^python3 - "\$REP\/baseline_suite.json" "\$REP\/after_suite.json"/{f=1;next} f&&/^PYEOF$/{exit} f{print}' "$1"; }
extract "$LM/tasks/code_patch/checker.sh" > "$ROOT/d/delta_new.py"
extract "$LM/tasks/code_patch/checker.sh.pre-1111-rename" > "$ROOT/d/delta_old.py"
[ -s "$ROOT/d/delta_new.py" ] && [ -s "$ROOT/d/delta_old.py" ] || { echo "ARMS ERROR: delta script not extracted"; exit 9; }
mk() { # mk <name> <json: {file: [[fullName,status],...]}> -> $ROOT/d/<name>.json (vitest report shape)
  python3 - "$ROOT/d/$1.json" "$2" <<'PY'
import json, sys
spec = json.loads(sys.argv[2]); res = []
for f, cells in spec.items():
    res.append({"name": "/x/" + f, "status": "passed", "assertionResults": [{"fullName": n, "title": n, "status": s} for n, s in cells]})
n = sum(len(c) for c in spec.values()); fl = sum(1 for c in spec.values() for _, s in c if s == "failed")
json.dump({"numTotalTests": n, "numFailedTests": fl, "testResults": res}, open(sys.argv[1], "w"))
PY
}
mkin() { printf '%s' "$2" > "$ROOT/d/$1.input.json"; }
mk base '{"a.test.ts":[["svc old name","passed"],["svc keep","passed"],["svc other","passed"]]}'
mk after_rn '{"a.test.ts":[["svc new name","passed"],["svc keep","passed"],["svc other","passed"]]}'
mk after_rn_red '{"a.test.ts":[["svc new name","failed"],["svc keep","passed"],["svc other","passed"]]}'
mk after_rn_2nd_lost_newred '{"a.test.ts":[["svc new name","passed"],["svc keep","failed"],["svc other","passed"]]}'
mk after_rn_old_stays '{"a.test.ts":[["svc old name","passed"],["svc new name","passed"],["svc keep","passed"],["svc other","passed"]]}'
mkin none '{"tip":"x"}'
mkin ok '{"declared_renames":[["svc old name","svc new name"]]}'
mkin typo '{"declared_renames":[["svc old nmae","svc new name"]]}'
mkin ok_dupnew '{"declared_renames":[["svc old name","svc keep"]]}'
dl() { if [ -n "${3:-}" ]; then python3 "$ROOT/d/delta_new.py" "$ROOT/d/$1.json" "$ROOT/d/$2.json" "$ROOT/d/$3.input.json"; else python3 "$ROOT/d/delta_new.py" "$ROOT/d/$1.json" "$ROOT/d/$2.json"; fi; }
dl_old() { python3 "$ROOT/d/delta_old.py" "$ROOT/d/$1.json" "$ROOT/d/$2.json"; }
darm() { # darm <label> <after> <input|""> <want rc> <grep|""> 
  local out rc; out="$(python3 "$ROOT/d/delta_new.py" "$ROOT/d/base.json" "$ROOT/d/$2.json" ${3:+"$ROOT/d/$3.input.json"} 2>&1)"; rc=$?
  if [ "$rc" -eq "$4" ] && { [ -z "$5" ] || echo "$out" | /usr/bin/grep -q -- "$5"; }; then ok "D $1: rc $rc ${5:+(/$5/)}"; else bad "D $1: rc=$rc want $4 /$5/ :: $(echo "$out" | tail -3 | tr '\n' ' ' | cut -c1-240)"; fi
}
darm "a-no-declaration-rename (default: the vanished passing cell is not this script's business)" after_rn "" 0 ""
darm "a2-no-declaration-key-in-input" after_rn none 0 ""
darm "b-declared-new-passes" after_rn ok 0 "declared rename accepted"
darm "c-declared-new-FAILS" after_rn_red ok 1 "new cell is failed, it must pass"
darm "d-declared-old-never-in-baseline" after_rn typo 1 "old cell is in 0 baseline file"
darm "e-declared-pair-plus-undeclared-2nd-change (a NEW red on keep)" after_rn_2nd_lost_newred ok 1 "NEW reds: \[('a.test.ts', 'svc keep')\]"
darm "g-declared-old-still-present" after_rn_old_stays ok 1 "old cell is still present"
darm "h-declared-new-already-in-baseline" after_rn ok_dupnew 1 "new cell already existed in the baseline"
# default byte-identity: new script (no 3rd arg, and with an input lacking the key) vs the pre-edit script, on every after-report
for a in after_rn after_rn_red after_rn_2nd_lost_newred after_rn_old_stays; do
  o1="$(dl_old base $a 2>&1; echo "rc=$?")"; o2="$(dl base $a "" 2>&1; echo "rc=$?")"; o3="$(dl base $a none 2>&1; echo "rc=$?")"
  [ "$o1" = "$o2" ] && [ "$o1" = "$o3" ] && ok "D default-byte-identical vs .pre-1111-rename on $a ($(echo "$o1" | tail -1))" || bad "D default differs on $a"
done

# ------------------------------------------------------------ L: brief_lint
BL="$ROOT/lint"; mkdir -p "$BL"
lbrief() { # lbrief <name> <renames block text or ""> [tier line]
  local d="$BL/$1"; mkdir -p "$d"
  cat > "$d/KS-9301.md" <<B
# KS-9301 declared-rename lint fixture

Client: Secuura
Tier: \`${3:-code_patch}\`
Runner: vitest
Tip: \`0123456789abcdef0123456789abcdef01234567\`
File: \`Blockchain/Dev/services/x/src/a.ts\`
Test file: \`Blockchain/Dev/services/x/src/__tests__/a.test.ts\`

## The mode
m
## What is wrong
w
## The exact change
\`\`\`
x
\`\`\`
## The test
t
## UNMEASURED
u
## Scope
s
## Output
o

$2
B
}
lint() { # lint <name> <want rc> <grep stdout|stderr> 
  local out rc; out="$(python3 "$SPARK/brief_lint.py" "$BL/$1" 2>&1)"; rc=$?
  if [ "$rc" -eq "$2" ] && echo "$out" | /usr/bin/grep -q -- "$3"; then ok "L $1: rc $rc /$3/"; else bad "L $1: rc=$rc want $2 /$3/ :: $(echo "$out" | head -3 | tr '\n' ' ' | cut -c1-260)"; fi
}
lbrief none ""
lbrief good '## Renames
- `svc old name` -> `svc new name`
- `svc old two` -> `svc new two`'
lbrief wildcard '## Renames
- `svc old *` -> `svc new name`'
lbrief dupnew '## Renames
- `a` -> `c`
- `b` -> `c`'
lbrief chain '## Renames
- `a` -> `b`
- `b` -> `c`'
lbrief malformed '## Renames
- svc old name renamed to svc new name'
lbrief same '## Renames
- `a` -> `a`'
lbrief empty '## Renames
nothing here'
lbrief bashtier '## Renames
- `a` -> `b`' bash_patch
lint none 0 "^B_TIER=code_patch"
if python3 "$SPARK/brief_lint.py" "$BL/none" 2>&1 | /usr/bin/grep -q B_RENAMES; then bad "L none: B_RENAMES line emitted without a declaration"; else ok "L none: no B_RENAMES line (output byte-identical to before)"; fi
lint good 0 'B_RENAMES=.\[\["svc old name", "svc new name"\], \["svc old two", "svc new two"\]\]'
lint wildcard 2 "REFUSED RENAMES.*wildcard"
lint dupnew 2 "REFUSED RENAMES.*not one-to-one"
lint chain 2 "REFUSED RENAMES.*not one-to-one"
lint malformed 2 "REFUSED RENAMES.*not exactly"
lint same 2 "REFUSED RENAMES.*not a rename"
lint empty 2 "REFUSED RENAMES.*no .- "
lint bashtier 2 "REFUSED RENAMES.*not supported by tier bash_patch"

# ------------------------------------------------------------ T: tier_checker (test_only_bash) on the real fixture clone
FX="$ROOT/fx"
python3 -I "$HERE/test_only_bash_spark_fixture.py" "$FX" > "$ROOT/fixture.out" 2>&1 || { echo "ARMS ERROR: fixture build failed"; cat "$ROOT/fixture.out"; exit 9; }
TIP="$(cat "$FX/tip.txt")"
export SPARK_SECUURA_CHECKOUT="$FX/secuura" SPARK_CACHE="$FX/cache" SPARK_STATE="$FX/state" SPARK_RUNS="$FX/runs" \
       SPARK_WORK_ROOT="$FX/work" SPARK_DEPS_CHECKOUT="$FX/deps" SPARK_TIP="$TIP" SPARK_URL="http://127.0.0.1:9"
bash "$SPARK/round.sh" "$FX/briefs/bx_pass_plant" --control > "$FX/pass.out" 2>&1
RUN="$(sed -n 's/^SPARK ROUND [^:]*: .* · \(\/[^ ]*\)$/\1/p' "$FX/pass.out" | tail -1)"
[ -n "$RUN" ] && [ -f "$RUN/input.json" ] || { echo "ARMS ERROR: control round left no run dir"; tail -3 "$FX/pass.out"; exit 9; }
CLONE="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]+"/round.json"))["work_dir"])' "$RUN")/clone"
SUITE="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("test_files")[0].split("/")[-1])' "$RUN/input.json")"
OLDC="$SUITE :: a plain run says run"; NEWC="$SUITE :: a plain run says RUN"
tin() { # tin <name> <renames json or ""> -> $FX/<name>.input.json
  python3 - "$RUN/input.json" "$FX/$1.input.json" "$2" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
if sys.argv[3]: d["declared_renames"] = json.loads(sys.argv[3])
json.dump(d, open(sys.argv[2], "w"))
PY
}
tchk() { # tchk <label> <input name> <out md> <want rc> <grep A6 line>
  cp "$3" "$FX/t_$1.md" 2>/dev/null
  python3 "$SPARK/tiers/tier_checker.py" "$FX/$2.input.json" "$FX/t_$1.md" "$CLONE" > "$FX/t_$1.out" 2>&1; local rc=$?
  local st; st="$(git -C "$CLONE" status --porcelain --untracked-files=no | wc -l | tr -d ' ')"
  if [ "$rc" -eq "$4" ] && /usr/bin/grep -q -- "$5" "$FX/t_$1.out" && [ "$st" = 0 ]; then ok "T $1: checker rc $rc, $(/usr/bin/grep -m1 -- "$5" "$FX/t_$1.out" | cut -c1-230); clone clean"
  else bad "T $1: rc=$rc want $4 /$5/ clone changes=$st :: $(/usr/bin/grep -E '^(FAIL|RESULT)' "$FX/t_$1.out" | head -3 | tr '\n' ' ' | cut -c1-320)"; fi
}
LOSTMD="$FX/outs/lost_cell.md"; GOODMD="$FX/outs/good_plant.md"
tin none ""
tin ok "[[\"$OLDC\",\"$NEWC\"]]"
tin typo "[[\"$SUITE :: a plain run says rn\",\"$NEWC\"]]"
tin ok_plus_bogus "[[\"$OLDC\",\"$NEWC\"],[\"$SUITE :: never existed\",\"$SUITE :: also not\"]]"
tchk a-no-declaration-rename none "$LOSTMD" 1 "^FAIL A6 WHOLE SUITE.*LOST"
tchk b-declared-new-passes ok "$LOSTMD" 0 "^INFO A6 declared rename"
tchk b2-declared-new-passes-A6-line ok "$LOSTMD" 0 "^PASS A6 WHOLE SUITE"
tchk d-declared-old-never-in-baseline typo "$LOSTMD" 1 "never in the baseline"
tchk e-declared-pair-plus-bogus-pair ok_plus_bogus "$LOSTMD" 1 "never in the baseline"
tchk f-good-output-no-declaration-still-passes none "$GOODMD" 0 "^PASS A6 WHOLE SUITE"
# crafted model outputs: diffs of T1 built in a scratch clone of the fixture's source repo (never the clone under test)
SCR="$FX/scratch_wt"; git clone -q "$FX/secuura" "$SCR" || { echo "ARMS ERROR: scratch clone"; exit 9; }
T1REL="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["test_files"][0])' "$RUN/input.json")"
mkdiff() { # mkdiff <out md> <variant>: edit T1 in the scratch clone, write the fenced diff, restore with git checkout
  python3 - "$SCR/$T1REL" "$2" <<'PY'
import sys
p, v = sys.argv[1:3]
s = open(p).read()
sent = 'check "the unchecked sentence is pinned whole" "Digits after a separator are not checked." "$(printf \'%s\\n\' "$help_text" | sed -n \'2p\')"\n'
ren = 'check "a plain run says run" "run" "$(bash "$PF")"\n'
assert ren in s
if v == "new_fails":
    s = s.replace(ren, 'check "a plain run says RUN" "runX" "$(bash "$PF")"\n' + sent)
elif v == "two":
    s = s.replace(ren, 'check "a plain run says RUN" "run" "$(bash "$PF")"\n' + sent)
    a = 'check "help names a closing parenthesis"'
    assert a in s
    s = s.replace(a, 'check "help names the closing parenthesis"')
open(p, "w").write(s)
PY
  { echo '```diff'; git -C "$SCR" diff --no-color | /usr/bin/grep -v '^diff --git \|^index '; echo '```'; } > "$1"
  git -C "$SCR" checkout -q -- .
}
mkdiff "$FX/outs/r_new_fails.md" new_fails
mkdiff "$FX/outs/r_two.md" two
OLD2="$SUITE :: help names a closing parenthesis"; NEW2="$SUITE :: help names the closing parenthesis"
tin ok_fails "[[\"$OLDC\",\"$NEWC\"]]"
tin ok_two_decl "[[\"$OLDC\",\"$NEWC\"],[\"$OLD2\",\"$NEW2\"]]"
tchk c-declared-new-FAILS ok_fails "$FX/outs/r_new_fails.md" 1 "new cell is failed, it must pass"
tchk e-pair-plus-undeclared-second-disappearance ok_fails "$FX/outs/r_two.md" 1 "^FAIL A6 WHOLE SUITE.*LOST.*closing parenthesis"
tchk e2-both-declared-passes ok_two_decl "$FX/outs/r_two.md" 0 "^PASS A6 WHOLE SUITE"
tchk e3-two-renames-no-declaration none "$FX/outs/r_two.md" 1 "^FAIL A6 WHOLE SUITE.*LOST"

echo "a6_declared_rename_arms: $P PASS, $F FAIL (outputs in $ROOT)"
[ "$F" -eq 0 ]
