#!/bin/bash
# test_only_bash_farm_arms.sh — red-proof for the test_only BASH runner's opt-in FARM (2026-09-22 15:5x, feed15 drafter,
# KS-1145 / the ks949 suite): tasks/test_only/build_test_only_input.sh reads a `Farm: \`shared+tsx\`` header line; tasks/
# test_only/prepare_clone.sh routes a `farm` input through the code_patch farm. Sibling of test_only_bash_arms.sh (its
# 20 arms must keep passing). The clone is a scratchpad clone of ORIGIN at TIP (TOF_CLONE; made by a clone.sh like
# runs/2026-09-22_feed15-drafter-precheck/clone.sh — this script NEVER clones from the checkout and runs no git write
# verb against it). Arms run in this order because (b) leaves the farm in the clone:
#   (a) a bash brief WITHOUT the line: the NEW builder's JSON == the OLD builder's byte for byte (cmp rc 0; no `farm` key);
#       the NEW prepare_clone's stdout == the OLD's byte for byte on that input (rc 0 both; the "no node farm" line);
#       the clone has NO node_modules and NO shared dist after (the bare clone as today)
#   (c) malformed: `Farm: \`shared+pg\`` → builder rc 2 naming 'pg'; an empty `Farm:` → rc 2; `Farm: \`tsx+tsx\`` → rc 2
#       (repeats); the line on a jest brief → rc 2; a hand-edited input `farm: "pg"` → prepare_clone rc 1 REFUSED and
#       NO farm lands (still no node_modules) — and the golden Farm brief still builds rc 0 (the refusals are the line's)
#   (b) WITH the line (the KS-1145 brief): JSON carries farm=shared+tsx + shared_pkg_dir=packages/shared; prepare_clone
#       rc 0 prints the FARM line and both `farm check: … ok` lines; the ks949 suite's own preconditions (:113-:114)
#       hold in the clone (`packages/shared/dist/index.js` -f, `node_modules/.bin/tsx` -x); the clone's porcelain is 0
#       (the farm is gitignored); the SOURCE checkout's tracked-modified count is unchanged (read verb)
# Usage: TOF_CLONE=<scratchpad clone at TIP> [TOF_OLD_BUILDER=… TOF_OLD_PREPARE=… TOF_SCRATCH=<dir>] bash test_only_bash_farm_arms.sh
# rc 0 only when every arm holds. Every rc read on its own line, never through a pipe. No rm. bash 3.2.
set -u
LM=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model
TD=$LM/tasks/test_only
BLD="${TOF_BUILDER:-$TD/build_test_only_input.sh}"
PREP="${TOF_PREPARE:-$TD/prepare_clone.sh}"
OLD_BLD="${TOF_OLD_BUILDER:-$TD/build_test_only_input.sh.pre-0922-1558-bashfarm}"
OLD_PREP="${TOF_OLD_PREPARE:-$TD/prepare_clone.sh.pre-0922-1558-bashfarm}"
FX=$LM/tests/fixtures/test_only
BRIEF="${TOF_BRIEF:-$FX/bash_farm_brief_ks1145.md}"
JEST_BRIEF=$FX/jest_brief.md
SRC="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files"
TIP="${TOF_TIP:-3bad652d17cf111c1e2e1bed1ae7686894637487}"
CLONE="${TOF_CLONE:-}"
SP="${TOF_SCRATCH:-$(mktemp -d "${TMPDIR:-/tmp}/tof_arms.XXXXXX")}"
RUNS="$SP/farm_arms_$(date +%Y%m%d-%H%M%S)"; mkdir -p "$RUNS"
pass=0; fail=0
ok(){ echo "  ok   $1"; pass=$((pass+1)); }
bad(){ echo "  FAIL $1 — $2"; fail=$((fail+1)); }
for f in "$BLD" "$PREP" "$OLD_BLD" "$OLD_PREP" "$BRIEF" "$JEST_BRIEF"; do [ -f "$f" ] || { echo "FATAL: missing $f"; exit 2; }; done
[ -n "$CLONE" ] && [ -d "$CLONE/.git" ] || { echo "FATAL: TOF_CLONE must name an existing scratchpad clone of ORIGIN at $TIP (this script never clones from the checkout)"; exit 2; }
case "$CLONE" in "$SRC"*) echo "FATAL: TOF_CLONE is the source checkout"; exit 2;; esac
[ "$(git -C "$CLONE" rev-parse HEAD 2>/dev/null)" = "$TIP" ] || { echo "FATAL: $CLONE is not at $TIP"; exit 2; }
SUBDIR="$(python3 -c 'import re,sys; m=re.search(r"^File:\s*`([^`]+)`", open(sys.argv[1]).read(), re.M); print(m.group(1).split("/")[0]+"/"+m.group(1).split("/")[1])' "$BRIEF")"
echo "test_only BASH FARM arms $(date '+%F %H:%M:%S') · builder $BLD ($(shasum -a 256 "$BLD" | cut -c1-12)) vs old ($(shasum -a 256 "$OLD_BLD" | cut -c1-12)) · prepare $PREP ($(shasum -a 256 "$PREP" | cut -c1-12)) vs old ($(shasum -a 256 "$OLD_PREP" | cut -c1-12)) · clone $CLONE · runs $RUNS"
SRC_DIRTY0="$(git -C "$SRC" status --porcelain --untracked-files=no | wc -l | tr -d ' ')"
[ -e "$CLONE/$SUBDIR/node_modules" ] && { echo "FATAL: the clone already carries $SUBDIR/node_modules — arm (a) needs a bare clone; use a fresh clone"; exit 2; }

echo "--- (a) a bash brief WITHOUT the Farm: line — byte-identical behaviour"
/usr/bin/grep -v '^Farm:' "$BRIEF" > "$RUNS/brief_nofarm.md"
n_farm="$(/usr/bin/grep -c '^Farm:' "$RUNS/brief_nofarm.md")"; n_farm_ctl="$(/usr/bin/grep -c '^Farm:' "$BRIEF")"
bash "$OLD_BLD" KS-ARMS-A "$RUNS/in_a_old.json" "$RUNS/brief_nofarm.md" tip="$TIP" > "$RUNS/build_a_old.out" 2>&1; rc_old=$?
bash "$BLD"     KS-ARMS-A "$RUNS/in_a_new.json" "$RUNS/brief_nofarm.md" tip="$TIP" > "$RUNS/build_a_new.out" 2>&1; rc_new=$?
cmp "$RUNS/in_a_old.json" "$RUNS/in_a_new.json" > "$RUNS/cmp_a.out" 2>&1; rc_cmp=$?
has_farm="$(python3 -c 'import json,sys; print("farm" in json.load(open(sys.argv[1])))' "$RUNS/in_a_new.json")"
shared_a="$(python3 -c 'import json,sys; print(repr(json.load(open(sys.argv[1]))["shared_pkg_dir"]))' "$RUNS/in_a_new.json")"
if [ "$n_farm" = 0 ] && [ "$n_farm_ctl" = 1 ] && [ "$rc_old" = 0 ] && [ "$rc_new" = 0 ] && [ "$rc_cmp" = 0 ] && [ "$has_farm" = False ] && [ "$shared_a" = "''" ]; then ok "(a1) builder: old rc $rc_old, new rc $rc_new, JSON cmp rc $rc_cmp (byte-identical), no farm key, shared_pkg_dir '' (Farm: lines in the copy 0, control 1)"
else bad "(a1)" "old rc $rc_old new rc $rc_new cmp rc $rc_cmp farm-key $has_farm shared $shared_a; $(head -2 "$RUNS/build_a_new.out")"; fi
bash "$OLD_PREP" "$RUNS/in_a_new.json" "$CLONE" > "$RUNS/prep_a_old.out" 2>&1; rc_pold=$?
bash "$PREP"     "$RUNS/in_a_new.json" "$CLONE" > "$RUNS/prep_a_new.out" 2>&1; rc_pnew=$?
cmp "$RUNS/prep_a_old.out" "$RUNS/prep_a_new.out" > "$RUNS/cmp_prep_a.out" 2>&1; rc_pcmp=$?
if [ "$rc_pold" = 0 ] && [ "$rc_pnew" = 0 ] && [ "$rc_pcmp" = 0 ] && /usr/bin/grep -q 'runner bash — no node farm, no shared build' "$RUNS/prep_a_new.out" && [ ! -e "$CLONE/$SUBDIR/node_modules" ] && [ ! -e "$CLONE/$SUBDIR/packages/shared/dist" ]; then ok "(a2) prepare_clone: old rc $rc_pold, new rc $rc_pnew, stdout cmp rc $rc_pcmp (byte-identical: '$(cat "$RUNS/prep_a_new.out" | cut -c1-80)…'); clone still bare (no node_modules, no shared dist)"
else bad "(a2)" "old rc $rc_pold new rc $rc_pnew cmp rc $rc_pcmp; $(cat "$RUNS/prep_a_new.out" | head -2)"; fi

echo "--- (c) malformed Farm: lines — REFUSE with the reason"
sed 's/^Farm:.*$/Farm: `shared+pg`/' "$BRIEF" > "$RUNS/brief_c1.md"
sed 's/^Farm:.*$/Farm:/' "$BRIEF" > "$RUNS/brief_c2.md"
sed 's/^Farm:.*$/Farm: `tsx+tsx`/' "$BRIEF" > "$RUNS/brief_c3.md"
awk 'NR==1{print; next} /^File:/ && !done {print; print "Farm: `shared+tsx`"; done=1; next} {print}' "$JEST_BRIEF" > "$RUNS/brief_c4.md"
jtip="$(python3 -c 'import re,sys; m=re.search(r"^Tip:\s*`?([0-9a-f]{40})`?", open(sys.argv[1]).read(), re.M); print(m.group(1) if m else "")' "$JEST_BRIEF")"
bash "$BLD" KS-ARMS-C1 "$RUNS/in_c1.json" "$RUNS/brief_c1.md" tip="$TIP" > "$RUNS/build_c1.out" 2>&1; rc_c1=$?
bash "$BLD" KS-ARMS-C2 "$RUNS/in_c2.json" "$RUNS/brief_c2.md" tip="$TIP" > "$RUNS/build_c2.out" 2>&1; rc_c2=$?
bash "$BLD" KS-ARMS-C3 "$RUNS/in_c3.json" "$RUNS/brief_c3.md" tip="$TIP" > "$RUNS/build_c3.out" 2>&1; rc_c3=$?
if [ -n "$jtip" ]; then bash "$BLD" KS-ARMS-C4 "$RUNS/in_c4.json" "$RUNS/brief_c4.md" > "$RUNS/build_c4.out" 2>&1; rc_c4=$?; else rc_c4=99; echo "(jest brief has no Tip:)" > "$RUNS/build_c4.out"; fi
if [ "$rc_c1" = 2 ] && /usr/bin/grep -q "REFUSED — Farm: line 'Farm: \`shared+pg\`' names 'pg' — not a farm token" "$RUNS/build_c1.out" && [ ! -f "$RUNS/in_c1.json" ]; then ok "(c1) rc 2: $(cut -c1-150 "$RUNS/build_c1.out")"; else bad "(c1)" "rc $rc_c1 $(head -1 "$RUNS/build_c1.out")"; fi
if [ "$rc_c2" = 2 ] && /usr/bin/grep -q "REFUSED — Farm: line 'Farm:' names no token" "$RUNS/build_c2.out"; then ok "(c2) rc 2: $(cut -c1-120 "$RUNS/build_c2.out")"; else bad "(c2)" "rc $rc_c2 $(head -1 "$RUNS/build_c2.out")"; fi
if [ "$rc_c3" = 2 ] && /usr/bin/grep -q "REFUSED — Farm: line 'Farm: \`tsx+tsx\`' repeats a token" "$RUNS/build_c3.out"; then ok "(c3) rc 2: $(cut -c1-120 "$RUNS/build_c3.out")"; else bad "(c3)" "rc $rc_c3 $(head -1 "$RUNS/build_c3.out")"; fi
if [ "$rc_c4" = 2 ] && /usr/bin/grep -q "REFUSED — Farm: line 'Farm: \`shared+tsx\`' on a jest brief" "$RUNS/build_c4.out"; then ok "(c4) rc 2: $(cut -c1-120 "$RUNS/build_c4.out")"; else bad "(c4)" "rc $rc_c4 $(head -1 "$RUNS/build_c4.out")"; fi
python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); d["farm"]="pg"; json.dump(d, open(sys.argv[2],"w"), indent=1, ensure_ascii=False)' "$RUNS/in_a_new.json" "$RUNS/in_c5.json"
bash "$PREP" "$RUNS/in_c5.json" "$CLONE" > "$RUNS/prep_c5.out" 2>&1; rc_c5=$?
if [ "$rc_c5" = 1 ] && /usr/bin/grep -q "REFUSED — farm 'pg' is not a farm token set" "$RUNS/prep_c5.out" && [ ! -e "$CLONE/$SUBDIR/node_modules" ]; then ok "(c5) prepare_clone rc 1 on a hand-edited farm='pg': $(cut -c1-110 "$RUNS/prep_c5.out"); no farm landed"; else bad "(c5)" "rc $rc_c5 $(head -1 "$RUNS/prep_c5.out")"; fi

echo "--- (b) WITH the line — the farm present, the ks949 preconditions pass"
bash "$BLD" KS-ARMS-B "$RUNS/in_b.json" "$BRIEF" tip="$TIP" > "$RUNS/build_b.out" 2>&1; rc_b=$?
farm_b="$(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); print(d.get("farm"), d["shared_pkg_dir"], d["runner"])' "$RUNS/in_b.json" 2>/dev/null)"
if [ "$rc_b" = 0 ] && [ "$farm_b" = "shared+tsx packages/shared bash" ] && /usr/bin/grep -q 'FARM shared+tsx (opt-in, brief Farm: line)' "$RUNS/build_b.out"; then ok "(b1) builder rc 0: farm=shared+tsx shared_pkg_dir=packages/shared runner=bash; printed the FARM clause"; else bad "(b1)" "rc $rc_b '$farm_b' $(head -1 "$RUNS/build_b.out")"; fi
bash "$PREP" "$RUNS/in_b.json" "$CLONE" > "$RUNS/prep_b.out" 2>&1; rc_pb=$?
if [ "$rc_pb" = 0 ] && /usr/bin/grep -q "runner bash — FARM 'shared+tsx' (opt-in by the brief's Farm: line)" "$RUNS/prep_b.out" && /usr/bin/grep -q 'farm check: Blockchain/Dev/node_modules/.bin/tsx executable — ok' "$RUNS/prep_b.out" && /usr/bin/grep -q 'farm check: Blockchain/Dev/packages/shared/dist/index.js present — ok' "$RUNS/prep_b.out" && /usr/bin/grep -q 'shared built in clone:' "$RUNS/prep_b.out"; then ok "(b2) prepare_clone rc 0: FARM line, shared built, both farm checks ok"; else bad "(b2)" "rc $rc_pb $(/usr/bin/grep -v '^farmed' "$RUNS/prep_b.out" | head -3 | tr '\n' '·')"; fi
DEV="$CLONE/$SUBDIR"
if [ -f "$DEV/packages/shared/dist/index.js" ] && [ -x "$DEV/node_modules/.bin/tsx" ] && [ -L "$DEV/node_modules/.bin" ]; then ok "(b3) the ks949 suite's :113-:114 preconditions hold in the clone (dist/index.js -f, .bin/tsx -x; .bin is a symlink INTO the source install)"; else bad "(b3)" "dist $( [ -f "$DEV/packages/shared/dist/index.js" ] && echo yes || echo no ) tsx $( [ -x "$DEV/node_modules/.bin/tsx" ] && echo yes || echo no )"; fi
porc="$(git -C "$CLONE" status --porcelain --untracked-files=all | wc -l | tr -d ' ')"
SRC_DIRTY1="$(git -C "$SRC" status --porcelain --untracked-files=no | wc -l | tr -d ' ')"
if [ "$porc" = 0 ] && [ "$SRC_DIRTY1" = "$SRC_DIRTY0" ]; then ok "(b4) clone porcelain 0 after the farm (gitignored); source tracked-modified $SRC_DIRTY0 -> $SRC_DIRTY1 (unchanged, read verb)"; else bad "(b4)" "porcelain $porc source $SRC_DIRTY0 -> $SRC_DIRTY1"; fi

echo "=== $pass ok, $fail FAIL (runs $RUNS)"
[ "$fail" -eq 0 ]
