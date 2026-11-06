#!/bin/bash
# Arms for panel_sync's record union (2026-11-06): real rebase conflicts in throwaway repos, run
# through resolve_derived_or_abort extracted from a candidate script. The control arm runs an OLD
# copy of the script and must LOSE the local row, or this harness proves nothing.
# Usage: panel_sync_union_arms.sh <scratch dir> <candidate script> <old script>
W="$(cd -P "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"; SP="$1/arms_$(date +%H%M%S)"; CAND="$2"; OLD="$3"; pass=0; fail=0
mkdir -p "$SP"
run(){ # name file base up lo script expect reject
  local name="$1" f="$2" base="$3" up="$4" lo="$5" script="$6" expect="$7" reject="$8"
  local R="$SP/$name"; mkdir -p "$R/0_Brain/dashboard/data" "$R/2_Project_Files/tools" "$R/0_Brain/learnings"
  cp "$W/2_Project_Files/tools/records_union.py" "$W/2_Project_Files/tools/decisions_union.py" "$R/2_Project_Files/tools/"
  git -C "$R" init -q -b main; git -C "$R" config user.email t@t; git -C "$R" config user.name t
  printf '%s' "$base" > "$R/0_Brain/dashboard/data/$f"; git -C "$R" add -A; git -C "$R" commit -qm base
  git -C "$R" checkout -qb upstream; printf '%s' "$up" > "$R/0_Brain/dashboard/data/$f"; git -C "$R" commit -qam up
  git -C "$R" checkout -q main; printf '%s' "$lo" > "$R/0_Brain/dashboard/data/$f"; git -C "$R" commit -qam lo
  git -C "$R" rebase upstream >/dev/null 2>&1
  [ -d "$R/.git/rebase-merge" ] || { echo "ARM $name: NO CONFLICT, instrument dead"; fail=$((fail+1)); return; }
  (
    cd -P "$R" || exit 9
    ROOT="$R"; DERIVED_RE='^(0_Brain/learnings/_boot_digest(_by_tier)?\.md|0_Brain/dashboard/data/.*\.json)$'
    say(){ echo "SAY: $*"; }
    eval "$(awk '/^resolve_derived_or_abort\(\)\{/{f=1} f{print} f&&/^}/{exit}' "$script")"
    resolve_derived_or_abort
  ) > "$SP/$name.log" 2>&1
  local rc=$?
  local got; got=$(cat "$R/0_Brain/dashboard/data/$f" 2>/dev/null)
  local inprog=no; [ -d "$R/.git/rebase-merge" ] && inprog=yes
  if printf '%s' "$got" | /usr/bin/grep -q -- "$expect" && { [ -z "$reject" ] || ! printf '%s' "$got" | /usr/bin/grep -q -- "$reject"; }; then
    echo "ARM $name: PASS rc=$rc rebase-in-progress=$inprog"; pass=$((pass+1))
  else
    echo "ARM $name: FAIL rc=$rc rebase-in-progress=$inprog got=$(printf '%s' "$got" | cut -c1-200)"; tail -3 "$SP/$name.log" | cut -c1-200; fail=$((fail+1))
  fi
}
also(){ # label file pattern
  if /usr/bin/grep -q -- "$3" "$2"; then echo "ARM $1: PASS"; pass=$((pass+1)); else echo "ARM $1: FAIL"; fail=$((fail+1)); fi
}
B='[{"role":"kam","text":"base","ts":"t0","view":"wednesday"}]'
U='[{"role":"kam","text":"base","ts":"t0","view":"wednesday"},{"role":"kam","text":"UPROW","ts":"t1","view":"wednesday"}]'
L='[{"role":"kam","text":"base","ts":"t0","view":"wednesday"},{"role":"kam","text":"LOROW","ts":"t2","view":"wednesday"}]'
run keep_both chat_kam.json "$B" "$U" "$L" "$CAND" LOROW ""
also keep_both_upstream "$SP/keep_both/0_Brain/dashboard/data/chat_kam.json" UPROW
AB='{"m1":{"state":"flagged","ts":"2026-11-06T10:00:00+11:00"}}'
AU='{"m1":{"state":"flagged","ts":"2026-11-06T10:00:00+11:00"},"m2":{"state":"flagged","ts":"2026-11-06T10:01:00+11:00"}}'
AL='{"m1":{"state":"answered","ts":"2026-11-06T11:00:00+11:00"},"m3":{"state":"answered","ts":"2026-11-06T10:02:00+11:00"}}'
run ack_later_wins ack_state.json "$AB" "$AU" "$AL" "$CAND" '"answered"' ""
also ack_key_up "$SP/ack_later_wins/0_Brain/dashboard/data/ack_state.json" '"m2"'
also ack_key_lo "$SP/ack_later_wins/0_Brain/dashboard/data/ack_state.json" '"m3"'
# one side unparseable: the tool refuses and nothing is guessed.
run malformed chat_kam.json "$B" "$U" 'NOT JSON' "$CAND" 'UPROW\|NOT JSON' ""
also malformed_refused "$SP/malformed.log" 'union FAILED'
# a generated file keeps the old behaviour (upstream).
run generated news.json '{"a":1}' '{"a":2}' '{"a":3}' "$CAND" '"a":2' '"a":3'
# CONTROL: the old script must lose the local row.
run control_old chat_kam.json "$B" "$U" "$L" "$OLD" UPROW LOROW
echo "PASS=$pass FAIL=$fail DIR=$SP"
[ "$fail" -eq 0 ]
