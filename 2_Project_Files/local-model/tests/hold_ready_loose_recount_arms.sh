#!/bin/bash
# hold_ready_loose_recount_arms.sh — red-proof for hold_ready.py's LOOSE-rung (4 and 6) recount tolerance at the strict-apply step.
# 2026-10-10. bash 3.2 (no declare -A, no timeout). Every hold_ready call is --dry-run (no READY_* file is ever written).
# Writes ONLY under $S (scratchpad); never modifies a real run dir; never deletes (the A3 fixture dir is unique per run). Exit 0 iff every arm behaved as expected.
L=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model
S=${S:-/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/ce91ac93-c45e-4849-a76b-deff4ef72ffc/scratchpad/holdready/arms}
NEW=$L/night/hold_ready.py
OLD=$L/night/hold_ready.py.pre-1010-loose-recount
R=$L/runs
K45=$R/spark_secuura_2026-10-10_KS-1345-originate-deliveries-failed-query-500
B45=$L/night/briefs/KS-1345-originate-deliveries-failed-query-500/KS-1345.md
T10=$R/spark_secuura_2026-10-10_KS-1410-transfer-process-expired-500
BT=$L/night/briefs/KS-1410-transfer-process-expired-500/KS-1410.md
# strict rung whose input.json['files'] covers every touched file (the only shape that reaches the strict-apply gate): KS-1432
K32=$R/spark_secuura_2026-10-07_KS-1432-apigw-ks529-guard-real-predicate
B32=$L/night/briefs/KS-1432-apigw-ks529-guard-real-predicate/KS-1432.md
mkdir -p "$S" || exit 9
FAILS=0
ok()  { echo "ARM $1: PASS — $2"; }
bad() { echo "ARM $1: FAIL — $2"; FAILS=$((FAILS+1)); }
run() { tag=$1; scr=$2; shift 2; python3 "$scr" --dry-run "$@" >"$S/$tag.out" 2>"$S/$tag.err"; RC=$?; }
has() { grep -q -- "$2" "$1"; }

# A1: KS-1345 (loose rung 6, recount-only) -> NEW tool: rc 0, DRY-RUN OK, strict=False, recount mode recorded
run a1 "$NEW" "$K45" "${K45}-control" WEBHOOKS-DELIVERIES-1 --title-from-brief "$B45" --model-tag spark-dsv4flash
if [ $RC -eq 0 ] && has "$S/a1.out" 'DRY-RUN OK' && has "$S/a1.out" 'strict=False' && has "$S/a1.out" 'APPLY MODE: NOT STRICT (strict=False)' && has "$S/a1.out" 'section 1: `git apply -p1 --recount --ignore-whitespace`'; then
  ok 1 "KS-1345 holds in dry-run, strict=False, recount mode recorded"; else bad 1 "rc=$RC; $(head -c 300 "$S/a1.err")"; fi

# A2: same dir -> OLD tool refuses at the strict-apply step (control: proves A1 discriminates)
run a2 "$OLD" "$K45" "${K45}-control" WEBHOOKS-DELIVERIES-1 --title-from-brief "$B45" --model-tag spark-dsv4flash
if [ $RC -eq 2 ] && has "$S/a2.err" 'does not apply strictly' && has "$S/a2.err" 'corrupt patch at line 29'; then ok 2 "OLD tool refuses rc=2 at strict-apply (corrupt patch at line 29)"; else bad 2 "rc=$RC; $(head -c 300 "$S/a2.err")"; fi

# A3: STRICT (non-loose) rung whose patch needs --recount -> still REFUSED by the NEW tool. Fixture = copy of the strict KS-1432 run
# with product hunk-1 header count corrupted (patch.diff + section_1.diff), section_1.opts=--recount, strict-error file non-empty,
# A2 line rewritten to the accommodation wording the real checker prints. Nothing under $R is touched.
F=$S/fixture_strict_recount_$$
cp -R "$K32" "$F" || bad 3-setup "copy failed"
python3 - "$K32" "$F" <<'PY'
import os, sys
src, dst = sys.argv[1], sys.argv[2]
for root, _, files in os.walk(dst):
    for f in files:
        p = os.path.join(root, f)
        try: t = open(p, encoding='utf-8').read()
        except Exception: continue
        if src in t: open(p, 'w', encoding='utf-8').write(t.replace(src, dst))
C = dst + '/out.md.checker/'
for f in ('patch.diff', 'section_1.diff'):
    t = open(C + f).read(); assert '@@ -259,3 +259,12 @@' in t
    open(C + f, 'w').write(t.replace('@@ -259,3 +259,12 @@', '@@ -259,3 +259,14 @@'))
o = open(C + 'section_1.opts').read().split('\n'); o[1] = '--recount'; open(C + 'section_1.opts', 'w').write('\n'.join(o))
open(C + 'apply_check_strict_1.out', 'w').write('error: corrupt patch at line 20\n')
co = open(dst + '/checker.out').read()
co = co.replace('PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)',
                'PASS A2 diff applies at the tip — with an accommodation: [x: --recount needed; miscounted hunks=1; strict rc=128]')
open(dst + '/checker.out', 'w').write(co)
PY
run a3 "$NEW" "$F" "${K32}-control" GUARD-1 --title-from-brief "$B32" --model-tag spark-dsv4flash
if [ $RC -eq 2 ] && has "$S/a3.err" 'does not apply strictly' && ! has "$S/a3.out" 'DRY-RUN OK'; then ok 3 "strict rung needing --recount still REFUSED rc=2 at strict-apply"; else bad 3 "rc=$RC; $(head -c 300 "$S/a3.err")"; fi

# A4: real strict runs -> unchanged verdict (NEW == OLD on rc, stdout, stderr after clock normalisation), DRY-RUN OK strict=True.
# KS-1432 reaches the strict-apply gate (files cover touched); KS-1410 transfer (new test file) does not — both kept.
norm() { sed -e 's/from `ls` at [0-9:]* [0-9-]*/from ls at CLOCK/g' "$1"; }
for pair in "a4a|$K32|GUARD-1|$B32" "a4b|$T10|TRANSFEREXP-1|$BT"; do
  tg=${pair%%|*}; rest=${pair#*|}; rd=${rest%%|*}; rest=${rest#*|}; rw=${rest%%|*}; br=${rest#*|}
  run ${tg}o "$OLD" "$rd" "${rd}-control" "$rw" --title-from-brief "$br" --model-tag spark-dsv4flash; RO=$RC
  run ${tg}n "$NEW" "$rd" "${rd}-control" "$rw" --title-from-brief "$br" --model-tag spark-dsv4flash; RN=$RC
  norm "$S/${tg}o.out" > "$S/${tg}o.n"; norm "$S/${tg}n.out" > "$S/${tg}n.n"
  if [ $RO -eq 0 ] && [ $RN -eq 0 ] && cmp -s "$S/${tg}o.n" "$S/${tg}n.n" && cmp -s "$S/${tg}o.err" "$S/${tg}n.err" && has "$S/${tg}n.out" 'strict=True'; then ok 4${tg#a4} "$(basename "$rd") identical OLD vs NEW, rc 0, strict=True"; else bad 4${tg#a4} "rcOLD=$RO rcNEW=$RN"; fi
done

# A5: the rung-3/4 arms still pass
S="$S/rung34" bash "$L/tests/hold_ready_rung34_arms.sh" >"$S/a5.out" 2>&1; R5=$?
F5=$(grep 'TOTAL FAILS=' "$S/a5.out" | tail -1)
if [ $R5 -eq 0 ] && [ "$F5" = "TOTAL FAILS=0" ]; then ok 5 "hold_ready_rung34_arms.sh rc=0 ($F5)"; else bad 5 "rc=$R5 $F5"; fi

echo "TOTAL FAILS=$FAILS"
[ $FAILS -eq 0 ]
