#!/bin/bash
# Arms for kam_awaiting_counts.sh and escalate_48h.sh against a TEMP store. Sends nothing.
set -u
DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOLS="$DIR/../tools"
W="$(mktemp -d)"; trap 'rm -rf "$W"' EXIT
export DQ_FILE="$W/decisions.json" ESCALATE_STATE="$W/state.json" ESCALATE_ENV="$W/none.env"
unset ESCALATE_SEND
python3 - <<'PYEOF'
import datetime, json, os
now = datetime.datetime.now().astimezone()
def card(i, cp, h, st="open"):
    return {"id": i, "client_project": cp, "title": "T " + i, "bluf": "b", "default_action": "DA " + i,
            "options": [], "recommended": "a", "ts": (now - datetime.timedelta(hours=h)).isoformat(), "status": st}
json.dump([card("arm-1h", "Datasec/ProjA", 1), card("arm-47h", "Datasec/ProjA", 47), card("arm-49h", "Datasec/ProjB", 49),
           card("arm-50h-done", "Datasec/ProjB", 50), card("arm-other-60h", "Secuura/Blockchain", 60),
           card("arm-ruled-70h", "Datasec/ProjA", 70, "ruled")], open(os.environ["DQ_FILE"], "w"))
PYEOF
P=0; F=0
chk() { if [ "$2" = "0" ]; then echo "PASS $1"; P=$((P+1)); else echo "FAIL $1"; F=$((F+1)); fi; }
has() { printf '%s' "$1" | grep -q -- "$2"; }
# pre-escalate the 50h card
printf '{"arm-50h-done": {"msg_id": "m0", "sent": "x"}}' > "$ESCALATE_STATE"
cp "$ESCALATE_STATE" "$W/state.before"
C="$(bash "$TOOLS/kam_awaiting_counts.sh" 2>&1)"; echo "$C"
has "$C" "awaiting 3 for ProjA" || { has "$C" "awaiting 2 for ProjA" && has "$C" "awaiting 2 for ProjB"; }; chk "counts ProjA=2 ProjB=2" $?
has "$C" "total awaiting: 4"; chk "total 4" $?
! has "$C" "Secuura\|arm-other"; chk "counts never show non-Datasec" $?
! has "$C" "arm-ruled"; chk "counts exclude ruled" $?
J="$(bash "$TOOLS/kam_awaiting_counts.sh" --json 2>&1)"
printf '%s' "$J" | python3 -c 'import json,sys; d=json.load(sys.stdin); assert d["total"]==4 and d["projects"]["ProjB"]["count"]==2'; chk "json valid and total 4" $?
D="$(bash "$TOOLS/escalate_48h.sh" --dry-run 2>&1)"; echo "$D"
has "$D" "arm-49h"; chk "dry-run lists 49h" $?
for x in arm-1h arm-47h arm-50h-done arm-other-60h arm-ruled-70h Secuura; do ! has "$D" "$x"; chk "dry-run omits $x" $?; done
has "$D" "1 Datasec card(s)"; chk "subject says 1 card" $?
cmp -s "$ESCALATE_STATE" "$W/state.before"; chk "state untouched by dry-run" $?
D0="$(bash "$TOOLS/escalate_48h.sh" 2>&1)"
has "$D0" "DRY RUN"; chk "default (no ESCALATE_SEND) is dry" $?
cmp -s "$ESCALATE_STATE" "$W/state.before"; chk "state untouched by default run" $?
printf '{"arm-50h-done": {"msg_id": "m0"}, "arm-49h": {"msg_id": "m1"}}' > "$ESCALATE_STATE"
D2="$(bash "$TOOLS/escalate_48h.sh" --dry-run 2>&1)"; echo "$D2"
has "$D2" "nothing to escalate"; chk "after simulated send, lists nothing" $?
# real send path must fail safe without a key and write no state
printf '{"arm-50h-done": {"msg_id": "m0"}}' > "$ESCALATE_STATE"; cp "$ESCALATE_STATE" "$W/state.before"
ESCALATE_SEND=1 bash "$TOOLS/escalate_48h.sh" >/dev/null 2>"$W/err"; RC=$?
[ "$RC" != 0 ] && cmp -s "$ESCALATE_STATE" "$W/state.before"; chk "send without key refuses, no state, no mail" $?
echo "PASS=$P FAIL=$F"; [ "$F" = 0 ]
