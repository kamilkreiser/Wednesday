#!/bin/bash
# self_check_view.sh — targeted view for the pre-send self-consistency read.
#
# WHY (three-strike promotion, 2026-08-18): three briefs contradicted
# themselves while every per-line gate passed (2026-08-13 "already invoiced"
# vs its own constraints section; the w=8 mixed provenance block; 2026-08-17
# "exactly once" vs "2 hits"). The read is the mechanism; this script only
# makes it targeted: it extracts the CLAIM-BEARING lines — numbers, ticket
# IDs, absolutes — and groups repeated ticket IDs so a contradiction sits
# next to its twin instead of three sections apart.
#
# This is an ASSISTANT, not a gate. The gate is send_brief.sh's SELF-CHECK
# attestation. A mechanical contradiction detector was considered and
# rejected: it would false-positive on legitimate contrasts, and a gate that
# blocks legitimate sends gets routed around (w=8 lesson).
#
# Usage: self_check_view.sh <body-file>
set -u
BODY_FILE="${1:-}"
[ -n "$BODY_FILE" ] && [ -f "$BODY_FILE" ] || { echo "usage: self_check_view.sh <body-file>" >&2; exit 2; }

echo "== Ticket IDs appearing MORE THAN ONCE (read each group as one claim set) =="
IDS="$(grep -oE '\b(KS|PS|RD|WED|HPSM|CPKEY|VSP|WIL)-[0-9]+\b' "$BODY_FILE" | sort | uniq -c | awk '$1>1{print $2}')"
if [ -n "$IDS" ]; then
  for id in $IDS; do
    echo "--- $id"
    grep -n "$id" "$BODY_FILE"
  done
else
  echo "(none repeated)"
fi

echo
echo "== Lines carrying NUMBERS (do any two disagree about the same thing?) =="
grep -nE '[0-9]' "$BODY_FILE" | grep -vE '^\s*[0-9]+:\s*$' | grep -viE 'read [0-9]{4}-[0-9]{2}-[0-9]{2}\s*$' || echo "(none)"

echo
echo "== ABSOLUTES (once/never/all/none/zero/only/every/nothing) — each is a claim =="
grep -niE '\b(exactly once|never|all of|none of|zero|only one|every|nothing|no other|always)\b' "$BODY_FILE" || echo "(none)"
