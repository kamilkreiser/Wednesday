#!/bin/bash
# decision_queue_client_scope_arms.sh — arms for the CLIENT SCOPE of the prior-ruling gate's card-id leg
# (tools/decision_queue.sh, prior_rulings() leg 2).
# WHY (ledger _ledger_laptop_datasec.md 2026-10-21, w=3 of the cross-client store family): the gate refused a
# Datasec card and its refusal listed ruled cards from EVERY client, so another client's card titles printed
# into a Datasec seat. Another client's ruling is never a prior ruling for this client's card; a Fleet/WED-scoped
# ruling can be, so it still counts.
# Usage: decision_queue_client_scope_arms.sh [path/to/decision_queue.sh]   (default: the tracked tool)
# Scratch files only: LIVE_BOARD=0, STORE_GUARD_SKIP=1, a scratch store, chat log and refusal log.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DQ="${1:-$HERE/../tools/decision_queue.sh}"
W="$(mktemp -d "${TMPDIR:-/tmp}/dq_client_scope_arms.XXXXXX")"
printf '#!/bin/bash\nexit 0\n' > "$W/noop.sh"
export LIVE_BOARD=0 STORE_GUARD_SKIP=1 DQ_COUNT_LIST_CHECK="$W/noop.sh" WED_AGENT=tuesday
export DQ_FILE="$W/decisions.json" DQ_CHAT="$W/chat.json" DQ_REFUSAL_LOG="$W/refusals.jsonl"
echo '[]' > "$DQ_CHAT"
# Four ruled cards, one rare subject word each, in three scopes.
cat > "$DQ_FILE" <<'EOF'
[{"id":"secuura-zebrafish-quota-0901","client_project":"Secuura/Blockchain","title":"Arm: zebrafish quota","status":"ruled","ruled_choice":"a"},
 {"id":"nexusai-walrus-limit-0901","client_project":"Datasec/NexusAI","title":"Arm: walrus limit","status":"ruled","ruled_choice":"a"},
 {"id":"fleet-otter-rotation-0901","client_project":"Fleet/all projects","title":"Arm: otter rotation","status":"ruled","ruled_choice":"a"},
 {"id":"hpsmpoc-heron-window-0901","client_project":"Datasec/HPSM-POC","title":"Arm: heron window","status":"ruled","ruled_choice":"a"}]
EOF
# Six open filler cards so the project prefix "hpsmpoc" is COMMON in the store (as it is in the real one) and is
# not scored as a rare subject word; without them C1 would refuse on the prefix alone, not on the subject.
python3 - "$DQ_FILE" <<'EOF'
import json, sys
p = sys.argv[1]; s = json.load(open(p))
for i in range(6):
    s.append({"id": f"hpsmpoc-filler{i}-card-0901", "client_project": "Datasec/HPSM-POC", "title": "Arm filler", "status": "open"})
json.dump(s, open(p, "w"))
EOF
card() {  # $1 = id, $2 = client_project
  printf '{"id":"%s","client_project":"%s","title":"Arm card","bluf":"Arm card.","options":[{"key":"a","label":"A","detail":"a"},{"key":"b","label":"B","detail":"b"}],"recommended":"a","default_action":"Nothing happens."}' "$1" "$2"
}
pass=0; fail=0
check() {  # $1 name, $2 expected rc, $3 actual rc, $4 must-appear (or ""), $5 must-NOT-appear (or ""), $6 output file
  local ok=1
  [ "$2" = "$3" ] || ok=0
  if [ -n "$4" ] && ! /usr/bin/grep -q -F -- "$4" "$6"; then ok=0; fi
  if [ -n "$5" ] && /usr/bin/grep -q -F -- "$5" "$6"; then ok=0; fi
  if [ $ok = 1 ]; then pass=$((pass+1)); echo "PASS $1 (rc $3)"; else fail=$((fail+1)); echo "FAIL $1 (rc $3, expected $2${4:+, '$4' present}${5:+, '$5' absent})"; sed -n 1,4p "$6" | sed 's/^/     /'; fi
}
# C1: a Datasec card whose only rare overlap is ANOTHER client's ruled card -> not refused, and that card is not printed
card hpsmpoc-zebrafish-quota-1021 "Datasec/HPSM-POC" | bash "$DQ" add --json > "$W/c1" 2>&1; rc=$?
check "C1 other client's ruling is not a prior for a Datasec card" 0 $rc "" "secuura-zebrafish" "$W/c1"
# C2: same client (another Datasec project) -> still refused
card hpsmpoc-walrus-limit-1021 "Datasec/HPSM-POC" | bash "$DQ" add --json > "$W/c2" 2>&1; rc=$?
check "C2 same client's ruling still refuses" 3 $rc "nexusai-walrus-limit-0901" "" "$W/c2"
# C3: a Fleet-scoped ruling still counts for a client card
card hpsmpoc-otter-rotation-1021 "Datasec/HPSM-POC" | bash "$DQ" add --json > "$W/c3" 2>&1; rc=$?
check "C3 Fleet-scoped ruling still refuses" 3 $rc "fleet-otter-rotation-0901" "" "$W/c3"
# C4: the mirror: a Secuura card is not refused by a Datasec ruling, and the Datasec card is not printed
card secuura-heron-window-1021 "Secuura/Blockchain" | bash "$DQ" add --json > "$W/c4" 2>&1; rc=$?
check "C4 Datasec ruling is not a prior for a Secuura card" 0 $rc "" "hpsmpoc-heron-window" "$W/c4"
# C5: control: same-project ruling refuses (the gate still fires at all)
card hpsmpoc-heron-window-1021 "Datasec/HPSM-POC" | bash "$DQ" add --json > "$W/c5" 2>&1; rc=$?
check "C5 control: same-project ruling refuses" 3 $rc "hpsmpoc-heron-window-0901" "" "$W/c5"
# SEAT SCOPE + DATE TOKENS (2026-10-27, Wednesday pickup OWED item 7): a WED/Fleet-scoped card names no client, so
# C1-C5's clause never fired; the seat's own client stands in. Run as the wednesday seat (own client = secuura).
# C6: a WED card in the wednesday seat whose only rare overlap is a DATASEC ruled card -> not refused, not printed
card wed-heron-window-1021 "WED" | WED_AGENT=wednesday bash "$DQ" add --json > "$W/c6" 2>&1; rc=$?
check "C6 Datasec ruling is not a prior for a WED card in the wednesday seat" 0 $rc "" "hpsmpoc-heron-window" "$W/c6"
# C7: a WED card in the wednesday seat overlapping the seat's OWN client's ruled card -> still refused
card wed-zebrafish-quota-1021 "WED" | WED_AGENT=wednesday bash "$DQ" add --json > "$W/c7" 2>&1; rc=$?
check "C7 own client's ruling still refuses a WED card" 3 $rc "secuura-zebrafish-quota-0901" "" "$W/c7"
# C8: a WED card sharing ONLY a date token (MMDD) with a ruled card -> not refused (dates are not subject words)
python3 -c 'import json,sys; s=json.load(open(sys.argv[1])); s.append({"id":"fleet-pelican-sweep-0315","client_project":"Fleet/all projects","title":"Arm: pelican","status":"ruled","ruled_choice":"a"}); json.dump(s,open(sys.argv[1],"w"))' "$DQ_FILE"
card wed-morning-plan-0315 "WED" | WED_AGENT=wednesday bash "$DQ" add --json > "$W/c8" 2>&1; rc=$?
check "C8 a shared date token alone does not refuse" 0 $rc "" "ALREADY RULED" "$W/c8"
# C9: a Fleet card in the TUESDAY seat overlapping a SECUURA ruled card -> not refused, not printed (mirror of C6)
card ops-zebrafish-quota-1022 "Fleet/all projects" | WED_AGENT=tuesday bash "$DQ" add --json > "$W/c9" 2>&1; rc=$?
check "C9 Secuura ruling is not a prior for a Fleet card in the tuesday seat" 0 $rc "" "secuura-zebrafish" "$W/c9"
echo "arms: $pass passed, $fail failed (tool: $DQ; scratch: $W)"
[ $fail = 0 ]
