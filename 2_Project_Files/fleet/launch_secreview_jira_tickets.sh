#!/bin/bash
# launch_secreview_jira_tickets.sh — Kam's 2026-09-10 round: raise Jira tickets from 13B so the
# Datasec product findings can be worked. Creates projects CWP and TDP first.
#
# WHY THE GUARDS ARE HEAVIER THAN USUAL. This is the first round today that WRITES to Kam's live
# Jira, under credentials that act as HIS OWN ACCOUNT with admin rights. The expensive failures are
# not "the agent gets tired" — they are structural:
#   - the evidence appendix must EXIST, or the tickets cite nothing and an engineer opens a ticket
#     that sends them back to the document;
#   - the two project keys must still be FREE, because a key is permanent in every ticket id and
#     colliding with an existing project is not undoable by us;
#   - Jira must actually be reachable with these credentials, or the agent will discover that
#     halfway through a filing run and leave the board half-populated.
#
# T9 PATHS. DevMASTER is not mounted here. SELF-LOCATING per portability rule 3.
# Usage: launch_secreview_jira_tickets.sh [--check]
# Exit: 0 launched (or guards pass under --check) · 2..16 a guard refused
set -u

SELF="${BASH_SOURCE[0]}"
while [ -L "$SELF" ]; do
  D="$(cd -P "$(dirname "$SELF")" && pwd)"; SELF="$(readlink "$SELF")"
  [[ $SELF != /* ]] && SELF="$D/$SELF"
done
FLEET_DIR="$(cd -P "$(dirname "$SELF")" && pwd)"
STAGED="$FLEET_DIR/briefs_staged"

SR_DIR="${SECREVIEW_DIR:-/Volumes/KK_T9_External_HDD/!CODING/Datasec/Security Review}"
NX_ENV="/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/4_Credentials/.env"
BRIEF="$STAGED/2026-09-10_secreview-jira-tickets.md"
PROMPT_FILE="$STAGED/2026-09-10_secreview-jira-tickets.prompt.txt"
REGB="$SR_DIR/Deliverables/13B_Datasec_Products_Consolidated_Findings_Register_2026-09.md"

[ -d "$SR_DIR" ]      || { echo "Security Review project missing: $SR_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]       || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -s "$REGB" ]        || { echo "13B register missing: $REGB" >&2; exit 5; }
[ -s "$NX_ENV" ]      || { echo "Jira credentials not found at $NX_ENV" >&2; exit 6; }

# GUARD: the evidence appendix must exist, with entries. Tickets cite EV-B ids; without them the
# whole point of this round (an engineer gets file and line from the ticket) is gone.
EV=$(grep -coE 'EV-B-[0-9]{3}' "$REGB")
[ "${EV:-0}" -ge 14 ] || {
  echo "REFUSING: only ${EV:-0} EV-B evidence references in 13B (expected at least 14)." >&2
  echo "  The tickets are supposed to carry file and line from Appendix D. Without it they would" >&2
  echo "  cite a document instead, which is the thing this round exists to stop." >&2
  exit 7; }

SITE=$(grep -E '^JIRA_SITE=' "$NX_ENV" | cut -d= -f2- | tr -d '"'"'"'')
MAIL=$(grep -E '^JIRA_EMAIL=' "$NX_ENV" | cut -d= -f2- | tr -d '"'"'"'')
TOK=$(grep -E '^JIRA_API_TOKEN=' "$NX_ENV" | cut -d= -f2- | tr -d '"'"'"'')
case "$SITE" in https://*) ;; *) SITE="https://$SITE";; esac
[ -n "$MAIL" ] && [ -n "$TOK" ] || { echo "REFUSING: Jira email or token empty in $NX_ENV" >&2; exit 8; }

# GUARD: Jira must be reachable AS someone, now — not halfway through a filing run.
WHO=$(curl -s --max-time 25 -u "$MAIL:$TOK" -H "Accept: application/json" "$SITE/rest/api/3/myself" \
      | python3 -c "import sys,json
try: print(json.load(sys.stdin).get('displayName') or '')
except Exception: print('')" 2>/dev/null)
[ -n "$WHO" ] || { echo "REFUSING: Jira did not authenticate — a half-filed board is worse than none." >&2; exit 9; }

# GUARD: both new keys must still be FREE. A key is permanent in every ticket id.
# 404 = free. Anything else (200 taken, 401/403 cannot tell) refuses — an unknown is not a free key.
for K in CWP TDP; do
  CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 20 -u "$MAIL:$TOK" \
         -H "Accept: application/json" "$SITE/rest/api/3/project/$K")
  [ "$CODE" = "404" ] || {
    echo "REFUSING: project key $K is not free (HTTP $CODE)." >&2
    echo "  404 means free. 200 means taken. Anything else means the check could not tell," >&2
    echo "  and an unknown must not be treated as free — the key is permanent." >&2
    exit 10; }
done
# CONTROL: a key we KNOW is taken must not read as free, or the check above proves nothing.
RDC=$(curl -s -o /dev/null -w "%{http_code}" --max-time 20 -u "$MAIL:$TOK" -H "Accept: application/json" "$SITE/rest/api/3/project/RD")
[ "$RDC" = "200" ] || { echo "REFUSING: control failed — known-taken key RD returned $RDC, not 200. The free-key check cannot be trusted." >&2; exit 11; }

PROMPT="$(cat "$PROMPT_FILE")"
case "$PROMPT" in ultrathink*) ;; *) echo "prompt does not begin with the thinking directive — refusing" >&2; exit 12 ;; esac
case "$PROMPT" in *2026-09-10_secreview-jira-tickets.md*) ;; *) echo "prompt does not name the brief path — refusing to launch a blind agent" >&2; exit 13 ;; esac
case "$PROMPT" in *tuesday-agent@agentmail.to*) ;; *) echo "prompt does not route the wrap to tuesday-agent@ — refusing" >&2; exit 14 ;; esac
case "$PROMPT" in *wednesday-agent@*) echo "prompt routes to wednesday-agent@ — refusing: cross-client" >&2; exit 15 ;; *) ;; esac
# GUARD: the parked exclusion must be carried, or the agent files 17 tickets Kam ruled out.
case "$PROMPT" in *parked*) ;; *) echo "prompt does not carry the parked-pair exclusion — refusing" >&2; exit 16 ;; esac

if [ "${1:-}" = "--check" ]; then
  echo "launch_secreview_jira_tickets: all guards pass"
  echo "  project, brief, prompt, 13B present (T9 paths)"
  echo "  Appendix D evidence references in 13B: $EV"
  echo "  Jira authenticates as: $WHO"
  echo "  keys CWP and TDP both FREE (404), control: RD taken (200)"
  echo "  prompt: directive, brief path, tuesday-agent@ routing, no Secuura inbox, parked exclusion carried"
  exit 0
fi

cd "$SR_DIR" || { echo "cannot enter $SR_DIR" >&2; exit 17; }
exec claude --dangerously-skip-permissions --model claude-opus-5 "$PROMPT"
