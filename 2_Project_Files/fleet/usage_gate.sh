#!/bin/bash
# usage_gate.sh — refuse a NEW agent/gate launch once the weekly Claude allowance
# reaches Kam's cut.
#
# WHY (Kam, panel 2026-09-14 19:14:25, verbatim): "Based on the clawed usage, close off
# the obvious tickets.  Once it reaches 90%, let's stop using other agents and we'll move
# to a model of you working with the local model to close off backlog." — confirmed
# 19:15:46 "Perfect, that works." against Wednesday's reading: the gauge is the
# statusline's 7-day figure; at 90% no NEW agent or gate is launched; whatever is
# mid-item finishes its item and wraps; Wednesday then works the backlog with the local
# model (Ornith). Grant file: 0_Brain/learnings/2026-09-14_at-90pct-weekly-usage-no-new-agents-wednesday-plus-local-model.md
#
# WHY A GATE AND NOT A RULE: a threshold a seat has to remember is not a threshold
# (2026-08-09_an-enforcement-you-must-arm-is-not-one). This sits in the two launch
# paths (brief_and_launch.sh, cockpit.sh add). The Agent-tool drafters cannot be gated
# here — the checkpoint ritual runs `usage_gate.sh --check` before commissioning one.
#
# INSTRUMENT: 0_Brain/dashboard/data/usage_<seat>.json, written by
# tools/statusline_publish.sh from Claude Code's own rate_limits.seven_day payload on
# every statusline render of THIS seat. It is fresh whenever the seat is taking turns and
# stale when it is not — a stale gauge cannot prove headroom, so staleness REFUSES too.
#
# Exit codes: 0 under the cut · 3 AT/OVER the cut (no launch) · 4 gauge missing/stale/
# unreadable (no launch; USAGE_GATE_ALLOW_STALE=1 overrides with the reason printed) ·
# 2 usage. `--check` prints the reading and exits by the same codes.
# Env: USAGE_GATE_FILE (default the seat's json) · WED_USAGE_STOP (default 90) ·
# USAGE_GATE_MAX_AGE_MIN (default 30).
set -u
SELF_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)
PROJECT_DIR=$(CDPATH= cd -- "$SELF_DIR/../.." && pwd -P)
SEAT="${WED_AGENT:-wednesday}"
FILE="${USAGE_GATE_FILE:-$PROJECT_DIR/0_Brain/dashboard/data/usage_${SEAT}.json}"
STOP="${WED_USAGE_STOP:-90}"
MAX_AGE_MIN="${USAGE_GATE_MAX_AGE_MIN:-30}"
MODE="${1:-gate}"
case "$MODE" in gate|--check) ;; *) echo "usage: usage_gate.sh [--check]" >&2; exit 2 ;; esac

[ -r "$FILE" ] || { echo "usage_gate: REFUSED (rc 4) — gauge file missing/unreadable: $FILE" >&2; exit 4; }
read -r PCT TS < <(python3 - "$FILE" <<'PY'
import json,sys,datetime
try:
    d=json.load(open(sys.argv[1]))
    pct=float(d['pct']); ts=d['ts']
    t=datetime.datetime.strptime(ts,'%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=datetime.timezone.utc)
    age=int((datetime.datetime.now(datetime.timezone.utc)-t).total_seconds()//60)
    print(f"{pct:.0f} {age}")
except Exception as e:
    print(f"ERR {e}")
PY
)
if [ "$PCT" = "ERR" ]; then echo "usage_gate: REFUSED (rc 4) — gauge unparseable: $TS" >&2; exit 4; fi
AGE="$TS"
if [ "$AGE" -gt "$MAX_AGE_MIN" ]; then
  if [ "${USAGE_GATE_ALLOW_STALE:-0}" = 1 ]; then
    echo "usage_gate: gauge STALE (${AGE} min > ${MAX_AGE_MIN}) — proceeding on USAGE_GATE_ALLOW_STALE=1; last reading ${PCT}%" >&2
  else
    echo "usage_gate: REFUSED (rc 4) — gauge STALE: ${AGE} min old (max ${MAX_AGE_MIN}); last reading ${PCT}%. Take a turn in the seat so the statusline republishes, or USAGE_GATE_ALLOW_STALE=1 with the reason stated." >&2
    exit 4
  fi
fi
if [ "$PCT" -ge "$STOP" ]; then
  echo "usage_gate: REFUSED (rc 3) — weekly usage ${PCT}% >= ${STOP}% (Kam 2026-09-14 19:14: no new agents at 90%; in-flight items finish and wrap; Wednesday + the local model from here). Gauge age ${AGE} min." >&2
  exit 3
fi
echo "usage_gate: OK — weekly usage ${PCT}% < ${STOP}% (gauge age ${AGE} min)"
exit 0
