#!/bin/bash
# card_id_gate.sh — refuse a body that NAMES a decision card which the store cannot show.
#
# WHY THIS EXISTS (enforcement, not advice): ledger w=7, the CARD costume's THIRD
# instance, 2026-09-06. Three times in two days a sentence asserting a card existed
# was written in the SAME response as the `decision_queue.sh add` that was supposed
# to create it — and the add was REFUSED by the prior-ruling gate each time:
#   09-05  #801        — the panel told Kam a card existed that did not.
#   09-06 11:03  KS-843 cutover — the mail to seat A said "carded (`secuura-ks843-cutover-stuart`)"
#                and its PROVENANCE line said "receipt read before this line". It had not been.
#   09-06 20:0x  the demo-admin card — the panel line and the ANSWER to seat A both
#                shipped in the batch that carried the refused add.
# Root cause is the same every time: the receipt sentence composed from INTENT in a
# parallel call. The rule ("a card add is ALWAYS its own tool call; the sentence comes
# in the call AFTER `added:` is read") has now failed three times as a rule. So it
# becomes a gate, in the path of both surfaces that carry such sentences to a reader:
# `send_brief.sh` (agents) and `chat_reply.sh` (Kam's panel).
#
# THE ONE RULE IT ENFORCES:
#   a body may not name a card id on a line that CLAIMS a card, unless
#   `decision_queue.sh show <id>` exits 0.
#
# WHY THE CARD-CLAIM CONTEXT (measured, not assumed — 2026-09-06 22:2x, 750 staged briefs):
#   id pattern alone            → 90 candidates, 12 would falsely refuse (13%), dominated by
#                                 Azure resource names: secuura-demo-rg, secuura-staging-kv…
#   id + a card word on the line→ 70 candidates, 66 resolve, 1 TRUE catch (a brief asserting
#                                 "Kam ruled the sizing card `nexusai-rd296-sizing`" — not in
#                                 the store), 2 genuine false positives, both resource names.
#   A gate that fires on `secuura-demo-rg` is a gate that gets routed around
#   ([[2026-08-09_an-enforcement-you-must-arm-is-not-one]] — an enforcement people
#   work around is not one either). 2.9% on one recognisable class is armable; the
#   class is excluded BY NAME below, never by a guessed pattern.
#
# Usage: card_id_gate.sh <body-file>
# Exit:  0 = pass · 1 = refused (ids printed with the fix) · 2 = usage/env error
# Never discards stderr (ledger 2026-08-06).
set -uo pipefail

SELF_DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd -P "$SELF_DIR/.." && pwd)"
DQ="$PROJECT_DIR/tools/decision_queue.sh"
ALLOW="$SELF_DIR/card_id_gate.allow"

BODY_FILE="${1:-}"
[ -n "$BODY_FILE" ] || { echo "card_id_gate: usage: card_id_gate.sh <body-file>" >&2; exit 2; }
[ -f "$BODY_FILE" ] || { echo "card_id_gate: no body file at $BODY_FILE" >&2; exit 2; }

# The tool is the discriminator. If it is missing we REFUSE rather than pass:
# an unreadable store is not evidence that a card exists (the same fail-closed
# posture as send_brief's ruled-cards gate).
[ -f "$DQ" ] || { echo "card_id_gate: REFUSED — decision queue tool missing at $DQ; cannot verify card ids" >&2; exit 1; }

# A line that CLAIMS a card. Deliberately narrow: these are the words the three
# failing sentences actually used.
CARDWORD='([Cc]ard(ed|s)?|CARDED|decision[_ ]queue|decision queue|your queue)'
# A card id: one of the three project prefixes plus at least two further segments.
IDPAT='(secuura|nexusai|wed)-[a-z0-9]+(-[a-z0-9]+)+'

CANDIDATES="$(grep -oE "^.*${CARDWORD}.*$" "$BODY_FILE" 2>/dev/null | grep -oE "$IDPAT" | sort -u)"
[ -n "$CANDIDATES" ] || exit 0

MISSING=""
while IFS= read -r id; do
  [ -n "$id" ] || continue
  # Named non-card exclusions (infra names measured on 2026-09-06). A NAME, never a
  # guessed pattern — a new one is added to card_id_gate.allow with a dated reason.
  if [ -f "$ALLOW" ] && grep -qxF "$id" "$ALLOW"; then continue; fi
  if bash "$DQ" show "$id" >/dev/null 2>&1; then continue; fi
  MISSING="${MISSING}${id}"$'\n'
done <<< "$CANDIDATES"

[ -n "$MISSING" ] || exit 0

{
  echo "REFUSED — the body names a decision card the store cannot show:"
  printf '%s' "$MISSING" | sed 's/^/    /'
  echo
  echo "Each id above sits on a line that CLAIMS a card. Either:"
  echo "  1. the card was never added (the add was refused, or it is still in this same batch)"
  echo "     → run \`decision_queue.sh add …\` as its OWN tool call, read the 'added:' line,"
  echo "       and write the sentence in the call AFTER that receipt (ledger w=7); or"
  echo "  2. the id is wrong → copy it from \`decision_queue.sh list\`; or"
  echo "  3. it is not a card at all (an Azure resource name, a file name)"
  echo "     → add the exact id to $ALLOW with a dated reason."
} >&2
exit 1
