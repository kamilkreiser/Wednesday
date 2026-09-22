#!/bin/bash
# absence_claim_check.sh — ADVISORY. Reads a message on stdin and flags ABSENCE / negative claims about
# state ("waiting on nothing", "not on kintsugi", "no review", "does not exist").
#
# WHY (ledger w=4, 2026-09-18, the 10:0x Wednesday seat): four times in ONE session I stated a claim I had
# not measured, as fact. Three were absences: TND "not on kintsugi" (they were deployed), #922 "waiting on
# nothing" (Peter held it), KS-1125 "truncated" (it was complete). A negative claim asserts about a WHOLE
# space, and one field (reviewDecision, a branch ancestry, a sed window) does not cover it. The rule,
# learnings/2026-09-18_a-premise-under-a-question-to-kam-is-load-bearing-verify-it.md, did not fire
# reliably by willpower. So this makes the moment visible.
#
# ADVISORY BY DESIGN: plain English is full of harmless negatives, so this NEVER blocks and ALWAYS exits 0.
# It prints to stderr only. Its job is to make me look, not to decide for me.
# Usage: printf '%s' "$MSG" | absence_claim_check.sh      Arms: tests/absence_claim_check_arms.sh
set -u
TEXT="$(cat)"
PAT='\b(nothing|never|no one|nobody|none of|not on|not waiting|isn'"'"'t waiting|wasn'"'"'t waiting|no reviews?|no record|does not exist|doesn'"'"'t exist|there (is|are|was|were) no|there'"'"'s no)\b'
HITS="$(printf '%s' "$TEXT" | /usr/bin/grep -oiE "$PAT" | tr 'A-Z' 'a-z' | sort -u | paste -sd, - 2>/dev/null)"
if [ -n "$HITS" ]; then
  echo "ADVISORY absence-claim(s): [$HITS] — for each, NAME the measurement that covers the WHOLE space it asserts about, or restate it as what you actually measured (ledger w=4, 2026-09-18). Not blocking." >&2
fi
exit 0
