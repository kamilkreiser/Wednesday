#!/bin/bash
# arms.sh — the Spark round runner's arms (2026-10-05). Run: bash local-model/spark/tests/arms.sh
#
#   A1a REFUSE  brief missing the kit-03 headings                       -> round.sh rc 2, "REFUSED — brief gate"
#   A1b REFUSE  brief naming another client (Client: Datasec)           -> rc 2, CLIENT
#   A1c REFUSE  dir with no KS-<n>.md                                    -> rc 2
#   A2  ENDPOINT DOWN  valid brief, SPARK_URL at a closed port           -> rc 4, "ENDPOINT DOWN"
#   A3  DRY-RUN  the real KS-1388-envexample brief                       -> rc 0, input pinned at today's develop
#   A4  BUSY  round lock held by a live pid                              -> rc 3, "BUSY"
#   A5  QUEUE drains  two refusal lines + a comment                      -> queue.sh rc 0, 2 done rows, queue empty
#   A6  QUEUE stops   endpoint down                                      -> queue.sh rc 4, loud line, line KEPT
#   A8-A12 PRUNE  removal / refusals (outside prefix, no marker, symlink out, pid 1, the root, empty) / locked + live
#                 kept / no-row kept / 24 h catch-up — all under $T
#   A7  REAL ROUND    KS-1388-envexample via queue.sh against the Spark (skipped when /v1/models != 200, or SPARK_ARMS_REAL=0)
#                     -> rc 0, PASS, patch.diff cmp golden.diff and the held 10-05 run's patch.diff
#
# Fixtures go to SPARK_TEST_TMP (default: a fresh mktemp dir under $TMPDIR). Never writes under !CODING. A7 writes a
# real run dir under local-model/runs/ (gitignored) and a work clone under spark/cache/work/ (gitignored).
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LM="$(dirname "$HERE")"
BRIEF="$LM/night/briefs/KS-1388-envexample"
REF="Blockchain/Dev/scripts/__tests__/start_secuura_marker_unknown_warning.test.sh"
HELD_RUN="$LM/runs/spark_secuura_2026-10-05_KS-1388-envexample"
T="${SPARK_TEST_TMP:-$(mktemp -d "${TMPDIR:-/tmp}/spark_arms.XXXXXX")}"; mkdir -p "$T"
CLOSED="http://127.0.0.1:9"
P=0; F=0
ok()  { echo "ARM PASS $*"; P=$((P+1)); }
bad() { echo "ARM FAIL $*"; F=$((F+1)); }
run() { # run <name> <expected rc> <expected substring> -- cmd...
  local name="$1" want="$2" sub="$3"; shift 4
  local out rc
  out="$("$@" 2>&1)"; rc=$?
  echo "$out" > "$T/$name.out"
  local last; last="$(echo "$out" | grep -E '^(SPARK ROUND|!!!!!|queue: empty)' | tail -1)"
  if [ "$rc" -eq "$want" ] && echo "$out" | grep -qF -- "$sub"; then ok "$name rc=$rc :: ${last:0:260}"
  else bad "$name rc=$rc (want $want, substring '$sub') :: ${last:0:260} (full: $T/$name.out)"; fi
}
echo "arms: fixtures in $T"

# fixtures
mkdir -p "$T/bad_shape" "$T/bad_client" "$T/no_brief" "$T/KS-1388-envexample-copy"
printf '# KS-9999 nothing — a brief with no shape\n\nFile: `observability/.env.example`\n\nJust do it.\n' > "$T/bad_shape/KS-9999.md"
{ head -1 "$BRIEF/KS-1388.md"; echo; echo "Client: Datasec"; tail -n +2 "$BRIEF/KS-1388.md"; } > "$T/bad_client/KS-1388.md"
echo "no brief here" > "$T/no_brief/notes.md"
cp "$BRIEF/KS-1388.md" "$BRIEF/golden.diff" "$T/KS-1388-envexample-copy/"
echo "ref=$REF" > "$T/KS-1388-envexample-copy/spark.pins"

# control for the refusal arms: the same gate ACCEPTS the real brief (so a refusal is the brief, not the gate)
if python3 "$HERE/brief_lint.py" "$BRIEF" "ref=$REF" > "$T/lint_control.out" 2>&1; then ok "A0 control: brief_lint accepts the real KS-1388-envexample brief"
else bad "A0 control: brief_lint refused the real brief: $(cat "$T/lint_control.out")"; fi

run A1a-refuse-shape 2 "REFUSED — brief gate" -- env SPARK_URL="$CLOSED" bash "$HERE/round.sh" "$T/bad_shape"
run A1b-refuse-client 2 "CLIENT" -- env SPARK_URL="$CLOSED" bash "$HERE/round.sh" "$T/bad_client" "ref=$REF"
run A1c-refuse-nobrief 2 "REFUSED" -- env SPARK_URL="$CLOSED" bash "$HERE/round.sh" "$T/no_brief"
run A2-endpoint-down 4 "ENDPOINT DOWN" -- env SPARK_URL="$CLOSED" bash "$HERE/round.sh" "$T/KS-1388-envexample-copy"
run A3-dry-run 0 "DRY-RUN OK" -- bash "$HERE/round.sh" "$BRIEF" --dry-run "ref=$REF"
DEV="$(git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" ls-remote origin refs/heads/develop 2>&1 | awk '{print $1}')"
DRYDIR="$(grep -o 'in /[^;]*/state/dry/[^;]*;' "$T/A3-dry-run.out" | head -1 | sed 's/^in //; s/;$//')"
DTIP="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["tip"])' "$DRYDIR/input.json" 2>&1)"
if [ -n "$DEV" ] && [ "$DTIP" = "$DEV" ]; then ok "A3b dry-run input pinned at develop as ls-remote reads it now ($DEV)"
else bad "A3b dry-run tip '$DTIP' != develop '$DEV'"; fi

mkdir -p "$T/state_busy/round.lock"; echo $$ > "$T/state_busy/round.lock/pid"; echo "arms A4" > "$T/state_busy/round.lock/what"
run A4-busy 3 "BUSY" -- env SPARK_STATE="$T/state_busy" bash "$HERE/round.sh" "$BRIEF" --dry-run "ref=$REF"

printf '# arms queue\n%s\n\n# a comment between\n%s\n' "$T/bad_shape" "$T/no_brief" > "$T/q5.md"
run A5-queue-drains 0 "queue: empty" -- env SPARK_QUEUE="$T/q5.md" SPARK_DONE="$T/done5.md" SPARK_STATE="$T/state_q5" SPARK_URL="$CLOSED" bash "$HERE/queue.sh"
ROWS="$(grep -c '^| 20' "$T/done5.md" 2>&1)"; LEFT="$(grep -cv '^\s*\(#\|$\)' "$T/q5.md")"
if [ "$ROWS" = 2 ] && [ "$LEFT" = 0 ]; then ok "A5b done.md has 2 rows, queue has 0 brief lines left"; else bad "A5b rows=$ROWS left=$LEFT"; fi

printf '%s\n' "$T/KS-1388-envexample-copy" > "$T/q6.md"
run A6-queue-endpoint-down 4 "SPARK QUEUE STOPPED" -- env SPARK_QUEUE="$T/q6.md" SPARK_DONE="$T/done6.md" SPARK_STATE="$T/state_q6" SPARK_URL="$CLOSED" bash "$HERE/queue.sh"
if grep -qF "$T/KS-1388-envexample-copy" "$T/q6.md"; then ok "A6b the line is still in the queue after the stop"; else bad "A6b the line was dropped"; fi


# A8-A12 — prune_work.py (all in scratch: SPARK_WORK_ROOT/SPARK_DONE/SPARK_STATE under $T; never the real work root)
PW="$T/pw"; mkdir -p "$PW/work" "$PW/runs" "$PW/outside" "$PW/state/round.lock"
PENV=(env SPARK_WORK_ROOT="$PW/work" SPARK_DONE="$PW/done.md" SPARK_STATE="$PW/state")
sleep 0 & DEADPID=$!; wait "$DEADPID"
mkw() { # mkw <dir> <run_dir> <pid> [row]   — a work dir as round.sh makes it (+ a fake clone), optional done row
  mkdir -p "$1/clone/sub"; echo x > "$1/clone/sub/f"; mkdir -p "$2"
  printf 'run_dir=%s\npid=%s\ncreated=arms\n' "$2" "$3" > "$1/.spark_round_work"
  [ "${4:-}" = row ] && echo "| arms | t | PASS | 1 | 1 | - | - | $2 | line |" >> "$PW/done.md"
  return 0
}
: > "$PW/done.md"
mkw "$PW/work/r_done" "$PW/runs/r_done" "$DEADPID" row
"${PENV[@]}" python3 "$HERE/prune_work.py" "$PW/work/r_done" > "$T/A8.out" 2>&1
if [ ! -e "$PW/work/r_done" ] && [ -d "$PW/runs/r_done" ] && grep -q '^prune: REMOVED' "$T/A8.out"; then ok "A8 removal :: $(cut -c1-200 "$T/A8.out")"
else bad "A8 removal: $(cat "$T/A8.out")"; fi

mkw "$PW/outside/x" "$PW/runs/x" "$DEADPID" row
mkdir -p "$PW/work/nomarker/clone"; echo "| arms | t | PASS | 1 | 1 | - | - | $PW/runs/nomarker | l |" >> "$PW/done.md"
ln -s "$PW/outside/x" "$PW/work/link_out"
mkw "$PW/work/pid1" "$PW/runs/pid1" 1 row
for target in "$PW/outside/x" "$PW/work/nomarker" "$PW/work/link_out" "$PW/work/pid1" "$PW/work" ""; do
  o="$("${PENV[@]}" python3 "$HERE/prune_work.py" "$target" 2>&1)"
  if echo "$o" | grep -q '^prune: REFUSED' && { [ -z "$target" ] || [ -e "$target" ]; }; then ok "A9 refusal '${target#$PW/}' survives :: $(echo "$o" | cut -c1-170)"
  else bad "A9 refusal '${target}': $o"; fi
done
[ -f "$PW/outside/x/clone/sub/f" ] && ok "A9b the outside target's contents are intact" || bad "A9b outside target damaged"

mkw "$PW/work/r_locked" "$PW/runs/r_locked" "$DEADPID" row
echo $$ > "$PW/state/round.lock/pid"; echo "$PW/work/r_locked" > "$PW/state/round.lock/work"
o="$("${PENV[@]}" python3 "$HERE/prune_work.py" "$PW/work/r_locked" 2>&1)"
if [ -d "$PW/work/r_locked" ] && echo "$o" | grep -q 'KEPT.*round.lock'; then ok "A10 locked round kept :: $(echo "$o" | cut -c1-170)"; else bad "A10 locked: $o"; fi
mv "$PW/state/round.lock" "$PW/state/round.lock.released"
mkw "$PW/work/r_live" "$PW/runs/r_live" "$$" row
o="$("${PENV[@]}" python3 "$HERE/prune_work.py" "$PW/work/r_live" 2>&1)"
if [ -d "$PW/work/r_live" ] && echo "$o" | grep -q 'KEPT.*still running'; then ok "A10b live-pid round kept :: $(echo "$o" | cut -c1-150)"; else bad "A10b live: $o"; fi

mkw "$PW/work/r_norow" "$PW/runs/r_norow" "$DEADPID"
o="$("${PENV[@]}" python3 "$HERE/prune_work.py" "$PW/work/r_norow" 2>&1)"
if [ -d "$PW/work/r_norow" ] && echo "$o" | grep -q 'KEPT.*no verdict row'; then ok "A11 no-verdict-row kept :: $(echo "$o" | cut -c1-150)"; else bad "A11 norow: $o"; fi

mkw "$PW/work/r_old" "$PW/runs/r_old" "$DEADPID" row; touch -t 202610030000 "$PW/work/r_old"
mkw "$PW/work/r_fresh" "$PW/runs/r_fresh" "$DEADPID" row
o="$("${PENV[@]}" python3 "$HERE/prune_work.py" --older-than-hours 24 2>&1)"
if [ ! -e "$PW/work/r_old" ] && [ -d "$PW/work/r_fresh" ] && [ -d "$PW/work/r_norow" ] && [ -d "$PW/work/nomarker" ]; then ok "A12 catch-up removed only the >24h recorded clone :: $(echo "$o" | grep -E 'REMOVED|catch-up' | tr '\n' ' ' | cut -c1-220)"
else bad "A12 catch-up: $o"; fi

# A7 — one REAL round, THROUGH queue.sh (scratch queue + done) so the post-row prune path runs
CODE="$(curl -s -m 10 -o /dev/null -w '%{http_code}' http://127.0.0.1:47788/v1/models 2>&1)"
if [ "${SPARK_ARMS_REAL:-1}" = 0 ]; then echo "ARM SKIP A7 real round (SPARK_ARMS_REAL=0)"
elif [ "$CODE" != 200 ]; then echo "ARM SKIP A7 real round — the Spark is not up (/v1/models answered '$CODE'); not restarting it"
else
  printf '%s ref=%s\n' "$BRIEF" "$REF" > "$T/q7.md"
  run A7-real-round 0 "SPARK ROUND KS-1388-envexample: PASS" -- env SPARK_QUEUE="$T/q7.md" SPARK_DONE="$T/done7.md" bash "$HERE/queue.sh"
  RD="$(grep '^SPARK ROUND' "$T/A7-real-round.out" | grep -o '/[^ ]*/runs/spark_secuura_[^ ]*' | tail -1)"
  WD="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["work_dir"])' "$RD/round.json" 2>&1)"
  if grep -qF "| $RD |" "$T/done7.md" && [ ! -e "$WD" ] && [ -d "$RD" ] && grep -qF "prune: REMOVED $WD" "$T/A7-real-round.out"; then
    ok "A7e verdict row written, work clone removed, run dir kept :: $(grep '^prune: REMOVED' "$T/A7-real-round.out" | cut -c1-220)"
  else bad "A7e prune after the real round (work $WD, run $RD)"; fi
  if [ -n "$RD" ] && cmp -s "$RD/out.md.checker/patch.diff" "$BRIEF/golden.diff"; then ok "A7b patch.diff BYTE-IDENTICAL to $BRIEF/golden.diff"
  else bad "A7b patch.diff differs from golden.diff (run $RD)"; fi
  if [ -n "$RD" ] && cmp -s "$RD/out.md.checker/patch.diff" "$HELD_RUN/out.md.checker/patch.diff"; then ok "A7c patch.diff BYTE-IDENTICAL to the held 10-05 run's patch.diff"
  else bad "A7c patch.diff differs from $HELD_RUN/out.md.checker/patch.diff"; fi
  MISS=""
  for f in input.json out.md out.md.meta.json out.md.raw.json run.log checker.out out.md.checker/patch.diff out.md.checker/a2a_anchor.out out.md.checker/sections_with_n.json; do
    [ -e "$RD/$f" ] || MISS="$MISS $f"
  done
  [ -n "$MISS" ] && bad "A7d run dir lacks:$MISS"
  [ -z "$MISS" ] && ok "A7d run dir has the 10-05 shape (input.json, out.md+meta+raw, run.log, checker.out, patch.diff, a2a_anchor.out, sections_with_n.json)"
fi
echo "arms: $P pass, $F fail (fixtures $T)"
[ "$F" -eq 0 ]
