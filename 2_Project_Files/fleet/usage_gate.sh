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
# SEAT (2026-09-23, Friday seat): WED_AGENT, else the TREE this script lives in — via the ONE
# resolver (cockpit/seat_resolve.sh). It used to fall back to the literal "wednesday", so
# Launch_Cockpit.command (which exports no WED_AGENT) on the FRIDAY tree read the Studio's
# usage_wednesday.json (90%, synced) instead of usage_friday.json (60%) and refused the
# laptop's cockpit. On the WEDNESDAY tree the tree resolves to wednesday: unchanged there.
if [ -r "$SELF_DIR/cockpit/seat_resolve.sh" ] && . "$SELF_DIR/cockpit/seat_resolve.sh" && seat_resolve "$PROJECT_DIR"; then
  :
else
  echo "usage_gate: REFUSED (rc 4) — cannot resolve the seat (cockpit/seat_resolve.sh missing or failed)" >&2; exit 4
fi
FILE="${USAGE_GATE_FILE:-$PROJECT_DIR/0_Brain/dashboard/data/usage_${SEAT}.json}"
# USAGE_STOP FILE (2026-09-16 21:1x, Kam panel: "try not to go beyond 40% token allocation"): a tracked
# fleet/USAGE_STOP whose first line is the cut (digits) sets the default for every launcher, which carry no
# env. WED_USAGE_STOP still wins; no file (or no digits) = 90 as before. Line 2 = the reason, for the record.
# SEAT-SCOPED (2026-09-16 21:3x, Kam to the Tuesday seat, verbatim: "the 40% was only for
# wednesday and Secuura projects.  you are on a different account and do not have that
# constraint.  no token constraint for you."). The shared USAGE_STOP was fleet-wide, so a cut
# written for ONE account refused launches on the OTHER — and measurably the wrong way round:
# at the time of his correction Wednesday's gauge read 7% (nowhere near the 40 written for her)
# while this seat's read 70%, so the only thing the shared file ever actually blocked was the
# account it was not written for. A per-account limit in a fleet-wide file is the same
# travel-pointer shape as a hardcoded path: correct where it was authored, wrong everywhere else.
# USAGE_STOP.<seat> wins over USAGE_STOP; env still wins over both.
_USF_DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
_USF="${USAGE_STOP_FILE:-$_USF_DIR/USAGE_STOP}"
[ -f "$_USF_DIR/USAGE_STOP.$SEAT" ] && _USF="$_USF_DIR/USAGE_STOP.$SEAT"
_USF_CUT="$( [ -f "$_USF" ] && sed -n 1p "$_USF" | tr -dc '0-9' )"
STOP="${WED_USAGE_STOP:-${_USF_CUT:-90}}"
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
# 70% ADVISORY (Kam 2026-09-25, three-tier routing grant, verbatim: "once you get to 70% of the weekly
# usage, minimize cloud agents"). NOT a refusal — rc stays 0 — because his rule is "minimise", with a
# launch still allowed when nothing local can do the work AND it matters now. So the gate says it LOUDLY
# on stderr and the launcher's caller must state which of those holds in its launch receipt.
# Grant file: 0_Brain/learnings/2026-09-25_three-tier-routing-ornith-spark-cloud-always-on.md (rule 4).
ADVISE="${WED_USAGE_ADVISE:-70}"
if [ "$PCT" -ge "$ADVISE" ]; then
  echo "usage_gate: ⚠ ADVISORY — weekly usage ${PCT}% >= ${ADVISE}% (Kam 2026-09-25: minimise cloud agents above 70%). Launch only if nothing local (Ornith/Spark) can do this AND it matters now; say which in the launch receipt. Hard stop at ${STOP}%." >&2
fi
echo "usage_gate: OK — weekly usage ${PCT}% < ${STOP}% (gauge age ${AGE} min)"
exit 0
