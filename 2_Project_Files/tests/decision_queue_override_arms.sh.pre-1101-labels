#!/bin/bash
# decision_queue_override_arms.sh — arms for the OVERRIDE-NEEDS-A-READ guard in tools/decision_queue.sh
# (Friday ledger w=3, 2026-10-11: card hpsmpoc-tuesday-dashboard-vs-next-phase-1011 went out with _override_prior on its
# FIRST attempt, so the prior-ruling gate's matches were never shown; the 2026-10-03 and 2026-10-06 rows were the same).
# Usage: decision_queue_override_arms.sh [path/to/decision_queue.sh]   (default: the tracked tool)
# Every arm runs on scratch files only: LIVE_BOARD=0, STORE_GUARD_SKIP=1, a scratch store, chat log and refusal log.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DQ="${1:-$HERE/../tools/decision_queue.sh}"
W="$(mktemp -d "${TMPDIR:-/tmp}/dq_override_arms.XXXXXX")"
printf '#!/bin/bash\nexit 0\n' > "$W/noop.sh"
export LIVE_BOARD=0 STORE_GUARD_SKIP=1 DQ_COUNT_LIST_CHECK="$W/noop.sh" WED_AGENT=friday
export DQ_FILE="$W/decisions.json" DQ_CHAT="$W/chat.json" DQ_REFUSAL_LOG="$W/refusals.jsonl"
echo '[]' > "$DQ_FILE"
# One Kam message sharing the subject words "tuesday" "dashboard" "preview" with the card below.
cat > "$DQ_CHAT" <<'EOF'
[{"role":"kam","ts":"2026-10-11T12:50:39+11:00","text":"Decision hpsmpoc-attribution-demo-tuesday-1011: c — A live dashboard preview on seeded data"}]
EOF
card() {  # $1 = id, $2 = title
  printf '{"id":"%s","client_project":"Datasec/HPSM-POC","title":"%s","bluf":"Arm card.","options":[{"key":"a","label":"A","detail":"a"},{"key":"b","label":"B","detail":"b"}],"recommended":"a","default_action":"Nothing happens."}' "$1" "$2"
}
with_override() { card "$1" "$2" | python3 -c 'import json,sys; d=json.load(sys.stdin); d["_override_prior"]="arm: matches read"; print(json.dumps(d))'; }
pass=0; fail=0
check() {  # $1 name, $2 expected rc, $3 actual rc, $4 expected-in-stderr (or ""), $5 stderr file
  local ok=1
  [ "$2" = "$3" ] || ok=0
  if [ -n "$4" ] && ! /usr/bin/grep -q -F -- "$4" "$5"; then ok=0; fi
  if [ $ok = 1 ]; then pass=$((pass+1)); echo "PASS $1 (rc $3)"; else fail=$((fail+1)); echo "FAIL $1 (rc $3, expected $2${4:+ and '$4' in stderr})"; sed -n 1,3p "$5" | sed 's/^/     /'; fi
}
added() { python3 -c 'import json,sys; print(sum(1 for x in json.load(open(sys.argv[1])) if x.get("id")==sys.argv[2]))' "$DQ_FILE" "$1"; }

# A1: override on the FIRST attempt (the 2026-10-11 case) -> refused, nothing added, nothing logged
with_override arm-tuesday-dashboard-preview-1 "Tuesday dashboard preview" | bash "$DQ" add --json > "$W/o" 2> "$W/e"; rc=$?
check "A1 first-attempt override refused" 3 $rc "not refused in the last hour" "$W/e"
[ "$(added arm-tuesday-dashboard-preview-1)" = 0 ] && echo "     (A1 card not in store: ok)" || { fail=$((fail+1)); echo "FAIL A1 card was ADDED"; }
# A2: plain add of the same id -> the ordinary prior-ruling refusal, and it is LOGGED
card arm-tuesday-dashboard-preview-1 "Tuesday dashboard preview" | bash "$DQ" add --json > "$W/o" 2> "$W/e"; rc=$?
check "A2 plain add refused by the prior-ruling gate" 3 $rc "Kam has already written on this subject" "$W/e"
/usr/bin/grep -q '"arm-tuesday-dashboard-preview-1"' "$DQ_REFUSAL_LOG" 2>/dev/null && echo "     (A2 refusal logged: ok)" || { fail=$((fail+1)); echo "FAIL A2 refusal NOT logged"; }
# A3: override after the logged refusal -> accepted, card added once
with_override arm-tuesday-dashboard-preview-1 "Tuesday dashboard preview" | bash "$DQ" add --json > "$W/o" 2> "$W/e"; rc=$?
check "A3 override after a read refusal accepted" 0 $rc "" "$W/e"
[ "$(added arm-tuesday-dashboard-preview-1)" = 1 ] && echo "     (A3 card added once: ok)" || { fail=$((fail+1)); echo "FAIL A3 card count != 1"; }
# A4: a DIFFERENT id with priors, overridden with no refusal of its own -> refused (one id's read does not cover another)
with_override arm-tuesday-dashboard-preview-2 "Tuesday dashboard preview again" | bash "$DQ" add --json > "$W/o" 2> "$W/e"; rc=$?
check "A4 another id's refusal does not cover this one" 3 $rc "not refused in the last hour" "$W/e"
# A5: an override on a card with NO priors is unaffected (nothing to override)
with_override arm-unrelated-subject-zebra-1 "Unrelated zebra subject" | bash "$DQ" add --json > "$W/o" 2> "$W/e"; rc=$?
check "A5 override with no priors passes" 0 $rc "" "$W/e"
# A6: a refusal older than an hour does not count
python3 - "$DQ_REFUSAL_LOG" <<'EOF'
import datetime, json, sys
old = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=2)).isoformat()
open(sys.argv[1], "a").write(json.dumps({"id": "arm-tuesday-dashboard-preview-3", "ts": old, "matches": 1}) + "\n")
EOF
with_override arm-tuesday-dashboard-preview-3 "Tuesday dashboard preview three" | bash "$DQ" add --json > "$W/o" 2> "$W/e"; rc=$?
check "A6 a refusal older than an hour does not count" 3 $rc "not refused in the last hour" "$W/e"
echo "arms: $pass passed, $fail failed (tool: $DQ; scratch: $W)"
[ $fail = 0 ]
