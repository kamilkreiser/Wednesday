#!/bin/bash
# send_brief.sh — the ONLY path by which Wednesday sends a brief to a project agent.
#
# WHY THIS EXISTS (enforcement, not advice): ledger w=3, 2026-08-06.
# Three times now a load-bearing fact reached a brief without being read from
# the authoritative source — Peter's to-do type (08-04), the Tokenomics tenant
# pointer (08-04), and the Lead_Bot handoff DIRECTION (08-06, which was
# backwards; the receiving project caught it). The rule "validate every fact"
# was already written down twice and still did not fire. So it stops being a
# rule and becomes a gate: a brief without per-fact provenance does not send.
#
# Usage:
#   send_brief.sh --to "<Client>/<Project>" --subject "<topic>" --body-file <path>
#   send_brief.sh --to ... --subject ... --body-file ... --kind answer   (ANSWER/ruling relay: provenance optional)
#
# Exit codes: 0 sent · 1 refused (provenance missing/malformed) · 2 usage/env error
set -u

SELF_DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd -P "$SELF_DIR/../.." && pwd)"
ENV_FILE="$PROJECT_DIR/4_Credentials/.env"
INBOX="wednesday-agent@agentmail.to"
BUS="coagent@agentmail.to"
ROUTING="$SELF_DIR/inbox_routing.conf"

TO=""; SUBJECT=""; BODY_FILE=""; KIND="brief"
while [ $# -gt 0 ]; do
  case "$1" in
    --to) TO="${2:-}"; shift 2 ;;
    --subject) SUBJECT="${2:-}"; shift 2 ;;
    --body-file) BODY_FILE="${2:-}"; shift 2 ;;
    --kind) KIND="${2:-}"; shift 2 ;;
    *) echo "unknown arg: $1" >&2; exit 2 ;;
  esac
done

[ -n "$TO" ] && [ -n "$SUBJECT" ] && [ -n "$BODY_FILE" ] || {
  echo "usage: send_brief.sh --to '<Client>/<Project>' --subject '<topic>' --body-file <path> [--kind brief|answer]" >&2; exit 2; }
[ -f "$BODY_FILE" ] || { echo "body file not found: $BODY_FILE" >&2; exit 2; }

BODY="$(cat "$BODY_FILE")"

# ── ROUTING (WED-104) ─────────────────────────────────────────────────────
# Which inbox actually receives this. A project not listed in the routing file
# is REFUSED — never silently defaulted to the shared bus, which is exactly the
# channel the per-project migration exists to stop using.
[ -f "$ROUTING" ] || { echo "no routing file at $ROUTING" >&2; exit 2; }
ROUTE_LINE="$(grep -v '^[[:space:]]*#' "$ROUTING" | grep -F "$TO|" | head -1)"
[ -n "$ROUTE_LINE" ] || {
  echo "BRIEF REFUSED — '$TO' is not in $ROUTING." >&2
  echo "Add '<Client>/<Project>|<inbox>|<yes|no>' there (and create the inbox) before briefing it." >&2
  exit 1; }
PROJ_INBOX="$(printf '%s' "$ROUTE_LINE" | cut -d'|' -f2)"
MIGRATED="$(printf '%s' "$ROUTE_LINE" | cut -d'|' -f3)"
case "$MIGRATED" in
  yes) RECIPIENTS="$PROJ_INBOX" ;;
  no)  RECIPIENTS="$PROJ_INBOX,$BUS" ;;
  *)   echo "BRIEF REFUSED — routing entry for '$TO' has a bad migrated flag: '$MIGRATED' (want yes|no)" >&2; exit 1 ;;
esac

# ── THE GATE ──────────────────────────────────────────────────────────────
# A brief must carry a PROVENANCE block. Each entry states a fact, WHERE it was
# read (a path, URL, ticket id, or command), and WHEN it was read. The check is
# structural on purpose — it cannot know whether I actually opened the file, but
# it makes "I didn't check" a deliberate act of writing a false line rather than
# an omission I never noticed. That is the same shape as the pre-commit hook.
if [ "$KIND" = "brief" ]; then
  if ! printf '%s' "$BODY" | grep -q '^PROVENANCE:'; then
    cat >&2 <<'MSG'
BRIEF REFUSED — no PROVENANCE block.

Every load-bearing fact in a brief must name where it was read and when. Add:

PROVENANCE:
- <fact> | <source path / URL / ticket / command> | read YYYY-MM-DD
- ...

Ledger w=3 (2026-08-06): the Lead_Bot brief asserted the handoff direction from
a ticket title instead of the project's own history entry — and it was backwards.
MSG
    exit 1
  fi
  # Each provenance line needs a source AND a read-date; two pipes minimum.
  BAD=0
  while IFS= read -r line; do
    case "$line" in
      "- "*)
        pipes="$(printf '%s' "$line" | tr -cd '|' | wc -c | tr -d ' ')"
        if [ "$pipes" -lt 2 ] || ! printf '%s' "$line" | grep -qE 'read [0-9]{4}-[0-9]{2}-[0-9]{2}'; then
          echo "BRIEF REFUSED — malformed provenance line (need '<fact> | <source> | read YYYY-MM-DD'):" >&2
          echo "  $line" >&2
          BAD=1
        fi ;;
      "") break ;;
    esac
  done <<EOF
$(printf '%s' "$BODY" | sed -n '/^PROVENANCE:/,$p' | tail -n +2)
EOF
  [ "$BAD" -eq 0 ] || exit 1
fi

# ── Send ──────────────────────────────────────────────────────────────────
[ -f "$ENV_FILE" ] || { echo "no .env at $ENV_FILE" >&2; exit 2; }
# shellcheck disable=SC1090
set -a; . "$ENV_FILE" 2>/dev/null; set +a
[ -n "${AGENTMAIL_API_KEY:-}" ] || { echo "AGENTMAIL_API_KEY unset" >&2; exit 2; }

# Kam is CC'd on every brief. This is NOT cosmetic: my briefs routinely tell an
# agent "Kam is CC'd — one line from him closes it", and that sentence names the
# ONLY path by which an approval-class action becomes Kam-traceable under v1.2.
# Until 2026-08-07 this script sent no cc at all, so that path never existed and
# every such sentence I wrote was false. Found by the Datasec/NexusAI agent, who
# checked the cc field through the API and held a built, verified deploy rather
# than accept a relay whose named closing mechanism was broken. Same family as
# validate-brief-pointers: I pointed an agent at a verification path without
# opening it myself.
# CC REMOVED 2026-08-12 on Kam's explicit instruction ("no need to copy me on
# emails to agents. I am happy tracking things this way"). Under v1.3 the
# signed delegation grant is the authority mechanism, so the cc had become
# informational only. Consequence of the history above still binds: NEVER
# write "Kam is CC'd" (or any closing-mechanism claim) into a brief — there
# is no cc to point at. Re-add only on a recorded Kam instruction.

FULL_SUBJECT="[Wednesday -> $TO] $SUBJECT"
CODE="$(BODY="$BODY" SUBJ="$FULL_SUBJECT" RCPTS="$RECIPIENTS" INBOXADDR="$INBOX" python3 - <<'PYEOF'
import json, os, urllib.request
payload = {"to": os.environ["RCPTS"].split(","),
           "subject": os.environ["SUBJ"], "text": os.environ["BODY"]}
req = urllib.request.Request(
    f"https://api.agentmail.to/v0/inboxes/{os.environ['INBOXADDR']}/messages/send",
    data=json.dumps(payload).encode(),
    headers={"Authorization": "Bearer " + os.environ["AGENTMAIL_API_KEY"], "Content-Type": "application/json"})
try:
    print(urllib.request.urlopen(req, timeout=20).status)
except Exception as e:
    print(f"ERR {e}")
PYEOF
)"
if [ "$CODE" = "200" ]; then
  echo "sent: $FULL_SUBJECT"
  echo "  -> $RECIPIENTS"
else
  echo "SEND FAILED ($CODE)" >&2; exit 2
fi
