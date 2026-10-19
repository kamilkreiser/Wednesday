#!/bin/bash
# status_watch_arms.sh — red/green arms for tuesday/tools/status_watch.sh.
# Builds a throwaway git repo under mktemp (never another project's tree) and checks:
#   A1 quiet: a non-final last line prints nothing within 3 s
#   A2 fire:  a final marker exits 0 and prints FINAL
#   A3 records branch ahead of main  -> "1 commit(s) on the branch"
#   A4 records branch equal to main  -> "EQUALS MAIN"
#   A5 records branch absent         -> "NOT FOUND"
#   A6 final line with no records ref -> no RECORDS CHECK line
W="$(cd "$(dirname "$0")/.." && pwd)/tools/status_watch.sh"
T=$(mktemp -d); trap 'echo "(scratch repo left at $T)"' EXIT
R="$T/repo"; mkdir -p "$R/1_Project_Definition/Briefs"
g() { git -C "$R" -c user.email=arms@test -c user.name=arms "$@"; }
g init -q -b main && g commit -q --allow-empty -m base && g branch records/b900 \
  && g checkout -q -b records/b901 && g commit -q --allow-empty -m rec && g checkout -q main || { echo "SETUP FAILED"; exit 1; }
ST="$R/1_Project_Definition/Briefs/X_STATUS.md"
pass=0; fail=0
ok() { echo "PASS $1"; pass=$((pass+1)); }; no() { echo "FAIL $1 :: $2"; fail=$((fail+1)); }

echo 'working on it' > "$ST"
bash "$W" "$ST" 1 > "$T/quiet.out" 2>&1 & P=$!; sleep 3; kill "$P" 2>/dev/null; wait "$P" 2>/dev/null
[ ! -s "$T/quiet.out" ] && ok "A1 quiet" || no "A1 quiet" "$(cat "$T/quiet.out")"

echo 'RECORDS DONE: records/b901, records/b900 and records/b999' >> "$ST"
OUT=$(bash "$W" "$ST" 1 2>&1); rc=$?
[ $rc -eq 0 ] && printf '%s' "$OUT" | grep -q '^FINAL ' && ok "A2 fire" || no "A2 fire" "rc=$rc $OUT"
printf '%s' "$OUT" | grep -q 'records/b901 = .* 1 commit(s) on the branch' && ok "A3 ahead" || no "A3 ahead" "$OUT"
printf '%s' "$OUT" | grep -q 'records/b900 EQUALS MAIN' && ok "A4 equals main" || no "A4 equals main" "$OUT"
printf '%s' "$OUT" | grep -q 'records/b999 NOT FOUND' && ok "A5 not found" || no "A5 not found" "$OUT"

echo 'DONE: removed one role assignment' >> "$ST"
OUT=$(bash "$W" "$ST" 1 2>&1)
printf '%s' "$OUT" | grep -q 'RECORDS CHECK' && no "A6 no ref" "$OUT" || ok "A6 no ref"

echo "arms: $pass PASS, $fail FAIL"
[ $fail -eq 0 ]
