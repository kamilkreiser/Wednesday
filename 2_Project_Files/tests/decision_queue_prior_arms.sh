#!/bin/bash
# decision_queue_prior_arms.sh: arms for the read-only `prior` verb of tools/decision_queue.sh
# (Tuesday ledger w=3, 2026-11-01 s214: a write verb was used twice as a probe of the prior-ruling gate).
# Scratch files only: LIVE_BOARD=0, STORE_GUARD_SKIP=1, scratch store, chat log and refusal log.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DQ="${1:-$HERE/../tools/decision_queue.sh}"
W="$(mktemp -d "${TMPDIR:-/tmp}/dq_prior_arms.XXXXXX")"
export LIVE_BOARD=0 STORE_GUARD_SKIP=1 WED_AGENT=tuesday
export DQ_FILE="$W/decisions.json" DQ_CHAT="$W/chat.json" DQ_REFUSAL_LOG="$W/refusals.jsonl"
echo '[]' > "$DQ_FILE"
cat > "$DQ_CHAT" <<'EOF'
[{"role":"kam","ts":"2026-10-11T12:50:39+11:00","text":"Decision hpsmpoc-attribution-demo-tuesday-1011: c - A live dashboard preview on seeded data"}]
EOF
pass=0; fail=0
ok() { pass=$((pass+1)); echo "PASS $1"; }
no() { fail=$((fail+1)); echo "FAIL $1"; }
before="$(shasum -a 256 "$DQ_FILE")"

# A1 a real match prints the message (the positive control for A2's zero)
bash "$DQ" prior --id arm-tuesday-dashboard-preview-1 --title "Tuesday dashboard preview" > "$W/o" 2> "$W/e"; rc=$?
[ "$rc" = 0 ] && /usr/bin/grep -q '^1 prior' "$W/o" && /usr/bin/grep -q 'dashboard preview' "$W/o" && ok "A1 match printed" || no "A1 rc=$rc $(cat "$W/o" "$W/e")"
# A2 no shared subject words prints a zero
bash "$DQ" prior --id arm-unrelated-subject-words --title "Quantum pineapple orchard" > "$W/o" 2> "$W/e"; rc=$?
[ "$rc" = 0 ] && /usr/bin/grep -q '^0 prior' "$W/o" && ok "A2 zero printed" || no "A2 rc=$rc $(cat "$W/o" "$W/e")"
# A3 nothing written: store byte-equal, no refusal log (the gate's add path would have logged A1)
[ "$(shasum -a 256 "$DQ_FILE")" = "$before" ] && ok "A3 store unchanged" || no "A3 store changed"
[ ! -e "$DQ_REFUSAL_LOG" ] && ok "A4 no refusal logged" || no "A4 refusal log written"
# A5 control for A3/A4: the same subject through `add` DOES refuse and log, so A4's absence means something
printf '{"id":"arm-tuesday-dashboard-preview-1","client_project":"Datasec/HPSM-POC","title":"Tuesday dashboard preview","bluf":"Arm card.","options":[{"key":"a","label":"Alpha","detail":"a"},{"key":"b","label":"Bravo","detail":"b"}],"recommended":"a","default_action":"Nothing moves."}' \
  | bash "$DQ" add --json > "$W/o" 2> "$W/e"; rc=$?
[ "$rc" = 3 ] && [ -s "$DQ_REFUSAL_LOG" ] && ok "A5 add refuses and logs (control)" || no "A5 rc=$rc $(cat "$W/e")"
# A6 bad flag and empty call refuse, writing nothing
bash "$DQ" prior --bluf x > "$W/o" 2> "$W/e"; rc=$?
[ "$rc" != 0 ] && ok "A6 unknown flag refused rc=$rc" || no "A6 accepted"
bash "$DQ" prior > "$W/o" 2> "$W/e"; rc=$?
[ "$rc" != 0 ] && ok "A7 empty call refused rc=$rc" || no "A7 accepted"

echo "RESULT pass=$pass fail=$fail"
[ "$fail" = 0 ]
