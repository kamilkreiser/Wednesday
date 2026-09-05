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

  # ── PATH-OWNERSHIP CHECK (ledger w=8, 2026-08-14) ────────────────────────
  # A PROVENANCE source that is a RELATIVE path resolves in whoever's tree the
  # reader is standing in. Three times now I have cited a path that exists only
  # in MY project to an agent who cannot open it — an unverifiable pointer
  # wearing a citation's clothes. The gate cannot know whose tree a path belongs
  # to, but it CAN insist the writer says. The third occurrence came one session
  # after I adopted the rule by hand, which is the definition of a rule that
  # needs a mechanism.
  #
  # Accepted: an absolute path (/...), a URL, a bare filename with no directory,
  # or a relative path whose line names an owner ("my project", "your project",
  # "not yours", "your own", "this project", or an explicit <Client>/<Project>).
  BADPATH=0
  while IFS= read -r line; do
    case "$line" in
      "- "*) ;;
      *) continue ;;
    esac
    src="$(printf '%s' "$line" | awk -F'|' '{print $2}')"
    # a relative path = contains a slash, does not start with / or a scheme.
    # FALSE POSITIVE fixed 2026-08-14, one hour after this gate shipped: a source
    # that is a COMMAND rather than a file (`git ls-remote origin refs/heads/develop`,
    # `GET /v0/inboxes/...`) contains slashes and was being refused. A gate that
    # blocks legitimate sends is worse than no gate, because the next session routes
    # around it. Commands are marked by backticks or an HTTP verb; skip those.
    case "$src" in
      *" /"*|*"http://"*|*"https://"*) continue ;;
      *'`'*) continue ;;
      *GET\ *|*POST\ *|*PUT\ *|*DELETE\ *) continue ;;
    esac
    printf '%s' "$src" | grep -q '/' || continue
    # NOTE: two greps on purpose. The phrase markers are case-insensitive; the
    # <Client>/<Project> pattern must be case-SENSITIVE. A single `grep -qiE`
    # made `[A-Z]` match lowercase, so every ordinary path like
    # `2_Project_Files/fleet/...` satisfied the Client/Project alternative and
    # the gate passed everything — caught by exercising the refuse path, which
    # is the only reason this comment exists rather than a silent hole.
    if ! printf '%s' "$line" | grep -qiE 'my project|your project|not yours|your own|this project' \
       && ! printf '%s' "$line" | grep -qE '[A-Z][A-Za-z_]+/[A-Z][A-Za-z_]+'; then
      echo "BRIEF REFUSED — PROVENANCE cites a RELATIVE path without saying whose tree it is in:" >&2
      echo "  $line" >&2
      BADPATH=1
    fi
  done <<EOF
$(printf '%s' "$BODY" | sed -n '/^PROVENANCE:/,$p' | tail -n +2)
EOF
  if [ "$BADPATH" -ne 0 ]; then
    cat >&2 <<'MSG'

Fix by doing ONE of:
  - make it absolute:      /Volumes/DevMASTER/WEDNESDAY/0_Brain/...
  - name the owner:        ... | 0_Brain/learnings/x.md - my project, not yours | read YYYY-MM-DD
  - point at THEIR tree:   ... | your own 5_Project_History/history.md | read YYYY-MM-DD

Ledger w=8 (validate-brief-pointers family): a relative path resolves in whoever's
tree the reader is standing in. Twice the receiving agent had to tell me the file
did not exist in their project.
MSG
    exit 1
  fi

  # ── SCOPE-CLAIM CHECK (ledger w=9, 2026-08-16) ───────────────────────────
  # The provenance gate refuses a brief whose FACTS lack a source. It cannot see
  # a CHARACTERISATION appended to a properly-sourced fact — and that is the one
  # that matters, because "reversible" is the exact word separating what v1.3
  # lets me authorise from what needs Kam's signature.
  #
  # 2026-08-16: my brief queued RD-93 as "duplicate transition id 51 on the RD
  # board. Board config, reversible." The predecessor's wrap said no such thing;
  # I appended the scope judgement, and the PROVENANCE line cited the wrap, so
  # the whole sentence travelled looking sourced. Reality: that transition lives
  # in a workflow shared by 25 of the site's 57 schemes — editing it changes
  # other teams' boards. I did not merely misinform the agent; I manufactured my
  # own permission to delegate it. Caught by the agent in 15 minutes.
  #
  # Deliberately NARROW, per the w=8 false-positive lesson (a gate that blocks
  # legitimate sends is worse than no gate): it fires only on words that assert
  # LOW risk, only on --kind brief, and is satisfied by ONE provenance line
  # mentioning scope / blast radius / consumers / reversib. Cheap to satisfy
  # honestly, impossible to satisfy by accident.
  # TRIGGER LIST, narrowed 2026-08-16 by running it against the three real briefs
  # sent that morning. `demo[- ]only` fired on two of them and both were FALSE
  # POSITIVES: in my briefs "demo-only" is a RESTRICTION I am imposing ("the
  # Kintsugi lift is demo-only"), not a low-risk claim about the work. It is
  # dropped. The list keeps only words that assert the work is SAFE or SMALL.
  # (The third brief fired correctly — on the real "Board config, reversible"
  # defect this gate exists for, which is the evidence it works.)
  SCOPE_HIT="$(printf '%s' "$BODY" | grep -oiE '\breversible\b|board config|low[- ]risk|blast radius|contained change|local change' | head -1)"
  if [ -n "$SCOPE_HIT" ]; then
    if ! printf '%s' "$BODY" | sed -n '/^PROVENANCE:/,$p' | tail -n +2 \
         | grep -qiE 'scope|blast radius|consumers|reversib|who else|shared by'; then
      cat >&2 <<MSG
BRIEF REFUSED — it makes a SCOPE claim ("$SCOPE_HIT") with nothing in PROVENANCE
establishing the blast radius.

A scope word is not framing. It is the field that decides whether the work is
inside my delegated authority — so it needs a source like any other fact:

PROVENANCE:
- reversible: only <X> consumes this | <the command that enumerated the consumers> | read YYYY-MM-DD

If you have NOT established it, say so in the brief instead:
  "I have not established the blast radius — establish it before acting."

Ledger w=9 (2026-08-16): "board config, reversible" on a workflow shared by 25
schemes across a 35-project Jira. The fact was sourced; the classification was
not, and it rode through on the fact's citation.
MSG
      exit 1
    fi
  fi

  # ── QUEUED-TICKET FRESHNESS CHECK (w=7 in the stale-brief family, 2026-08-17) ──
  # Twice now a brief has queued work that was ALREADY DONE, because the queue
  # was built from a frozen record (a history entry, a carry-forward block, a
  # predecessor's wrap) instead of the newest record OF THAT WORK — the ticket.
  # 2026-08-13: briefed HPSM to redo work my own SCORE mail had verified done.
  # 2026-08-17: queued KS-490 E-2/E-3 as work; s38 had dispositioned both in a
  # ticket comment 19 hours before my brief. The agent re-verified instead of
  # redoing, both times — the catch cost them a read; the gate makes it mine.
  #
  # NARROW, per the w=8 false-positive lesson: fires only on a "## QUEUE"
  # section (my brief template's work list), and only requires that each ticket
  # ID queued there appears in SOME provenance line — i.e. I opened the ticket,
  # or at least had to write a false line saying I did. Holds, context and
  # ANSWER mails are untouched.
  if printf '%s' "$BODY" | grep -qiE '^## *QUEUE'; then
    QUEUE_IDS="$(printf '%s' "$BODY" | sed -n '/^## *[Qq][Uu][Ee][Uu][Ee]/,/^## /p' \
                 | grep -oE '\b(KS|PS|RD|WED|HPSM|CPKEY|VSP|WIL)-[0-9]+\b' | sort -u)"
    PROV_BLOCK="$(printf '%s' "$BODY" | sed -n '/^PROVENANCE:/,$p')"
    MISSING=""
    for id in $QUEUE_IDS; do
      printf '%s' "$PROV_BLOCK" | grep -q "$id" || MISSING="$MISSING $id"
    done
    if [ -n "$MISSING" ]; then
      cat >&2 <<MSG
BRIEF REFUSED — the QUEUE section names ticket(s) with no provenance line:
 $MISSING

A queued ticket is a claim that the work is still open. The newest record of
that work is the TICKET, not a wrap, a history entry or a carry-forward block.
Open each one and add:

PROVENANCE:
- <ticket> state (open, last comment <when>) | Linear/Jira ticket <id> | read YYYY-MM-DD

Stale-brief family w=7 (2026-08-13 HPSM redo-brief; 2026-08-17 KS-490 E-2/E-3
queued 19 hours after the ticket said done).
MSG
      exit 1
    fi
  fi

  # ── SELF-CONSISTENCY ATTESTATION (three-strike promotion, 2026-08-18) ─────
  # Three times a brief of mine has CONTRADICTED ITSELF while every per-line
  # gate passed, because per-line gates cannot see a document arguing with
  # itself:
  #   2026-08-13 (w=5): "the A$187,500 already invoiced" in a brief whose own
  #     constraints section said "SOW unsigned" — the disproof travelled in the
  #     same document.
  #   2026-08-14 (w=8): the ownership rule applied to two provenance lines and
  #     not the third, inside one mail.
  #   2026-08-17 (w=2 family): QUEUE said Purview appears "exactly once" while
  #     the same brief's PROVENANCE line said "2 hits". Caught by the agent.
  # A self-contradiction is a READING defect, not a line defect, so the
  # mechanism is the provenance gate's: convert "never noticed I hadn't done
  # the read" into "I would have to write a false line". The brief must carry a
  # fresh, TODAY-dated attestation that the end-to-end contradiction read was
  # done:
  #     SELF-CHECK: re-read end-to-end for contradictions | YYYY-MM-DD HH:MM
  # The date must be today — a copy-pasted line from yesterday's brief refuses,
  # which is what makes the attestation a fresh act rather than a template
  # fossil. HONEST LIMIT (same as the provenance gate's, stated there too): it
  # cannot know whether the read actually happened. It makes skipping it a
  # deliberate falsehood instead of an omission — that shift is the mechanism.
  # Helper: fleet/self_check_view.sh <body-file> prints the claim-bearing lines
  # (numbers, ticket IDs, absolutes) grouped, so the re-read is targeted.
  # NARROW per the w=8 false-positive lesson: --kind brief only; ANSWER mails
  # and holds are untouched.
  # LOCAL date only. The first draft also accepted the UTC date — and because
  # AEST is UTC+10, every morning before 10:00 the UTC date is still YESTERDAY,
  # so a stale attestation carried from last night would have passed. Caught by
  # exercising the refuse path before arming (the stale test did not refuse).
  TODAY_LOCAL="$(date +%Y-%m-%d)"
  SC_LINE="$(printf '%s' "$BODY" | grep -E '^SELF-CHECK: *re-read end-to-end for contradictions \| [0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}' | tail -1)"
  if [ -z "$SC_LINE" ]; then
    cat >&2 <<MSG
BRIEF REFUSED — no SELF-CHECK attestation.

Per-line gates cannot see a document contradicting itself (three instances:
2026-08-13 "already invoiced" vs its own constraints; the w=8 mixed block;
2026-08-17 "exactly once" vs "2 hits"). Re-read the WHOLE brief asking one
question — does any sentence contradict another? — then attest it, freshly:

SELF-CHECK: re-read end-to-end for contradictions | $TODAY_LOCAL $(date +%H:%M)

Targeted view of the claim-bearing lines:
  2_Project_Files/fleet/self_check_view.sh <body-file>
MSG
    exit 1
  fi
  SC_DATE="$(printf '%s' "$SC_LINE" | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}')"
  if [ "$SC_DATE" != "$TODAY_LOCAL" ]; then
    cat >&2 <<MSG
BRIEF REFUSED — SELF-CHECK attestation is STALE ($SC_DATE, today is $TODAY_LOCAL).
A carried-forward attestation is a template fossil, not a read. Do the read on
THIS version of the brief, then re-date the line.
MSG
    exit 1
  fi
fi

# ── DRY RUN ───────────────────────────────────────────────────────────────
# Stops here, after every gate and before any network call. Added 2026-08-16 so
# the PASS branch of each gate can be exercised without sending mail to a live
# agent's inbox — on 2026-08-14 a junk "gate test" mail reached a working agent
# and cost a disavowal. A gate whose pass path can only be tested by really
# sending is a gate that gets tested in production, once, on someone else.
if [ "${SEND_BRIEF_DRY_RUN:-}" = "1" ]; then
  echo "DRY RUN — all gates PASSED, nothing sent."
  echo "  to:         $TO"
  echo "  recipients: $RECIPIENTS"
  echo "  subject:    [Wednesday -> $TO] $SUBJECT"
  exit 0
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
