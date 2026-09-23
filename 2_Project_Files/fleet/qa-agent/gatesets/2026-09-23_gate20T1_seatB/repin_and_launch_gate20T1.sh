#!/bin/bash
# repin_and_launch_gate20T1.sh — the LAUNCH ACTION for the round-20 TIER-1 batch gate (#1204 #1207 #1208 #1209 #1210 #1211 #1212).
# The re-pin and the launch are ONE action (Kam 2026-09-18: a stale pin costs a whole gate session). THE BASE HAS MOVED (tier 2 merged 08:09Z-08:10Z),
# so this script READS develop and every head AT LAUNCH and never trusts a pin it did not just re-read:
#   (0b) the launcher carries SEVEN pinned rows (incl. KS-1143) and is not a CONTROL COPY — rc 8, before any network read;
#   (0)  the pane is routed (inbox_routing.conf) — rc 1;
#   (1)  origin develop + every refs/pull/N/head + every branch by `git ls-remote`, READ from the Secuura checkout (read verb only) — rc 2;
#   (2)  every PR head re-read from the GitHub PULLS API (a second, independent instrument) — rc 3 if the read fails;
#   (3)  rc 11 unless every head == its pin on BOTH instruments AND every PR is open (a STALE HEAD REFUSES here);
#   (3b) develop: if origin develop != the launcher's pinned launch develop, RE-PIN IN THIS SAME ACTION — predict_batch_scratch_gate20T1.py over the
#        develop just read (a scratch clone FROM ORIGIN under <scratchpad>; it REFUSES unless the move is a descendant of BASE, disjoint from the 14
#        tier-1 paths and the tamper file, and every merged tree + the END_TREE re-derive cleanly in three orders), then fill_prompt_gate20T1.py and
#        gen_launcher_gate20T1.py (both re-read develop + heads again and refuse on any disagreement) — then ls-remote develop ONCE MORE: rc 10 unless it
#        still equals the new pin (a develop that moves during the re-pin refuses; run again);
#   (4)  the usage gate — rc 12;  (5) the launcher's own --check (heads, compares vs the develop read, the grep ladder) — rc 13;
#   (6)  cockpit.sh add — the fleet's own tooling, never raw tmux send-keys — rc 14, then a pane census.
# --dry-run: steps 0b-3 and a REPORT of 3b (no re-pin, no write), then stop before (4) — rc 0 only if every read agrees with the pins; the routing
# line's absence is reported, not refused, in a dry run. READ-ONLY in the Secuura checkout: ls-remote only. Nothing is merged, deployed or commented.
# The PINS are READ from the launcher itself (its PRS array, BASE_SHA, DEVELOP_SHA) so this file never carries a second copy that could drift.
# Derived from gatesets/2026-09-23_gate20T2_seatB/repin_and_launch_gate20T2.sh. Wednesday runs this; the drafter did NOT (it ran --dry-run and controls).
# Usage: repin_and_launch_gate20T1.sh <launcher path> <a scratchpad dir under /private/tmp/claude-501/> [--dry-run]
set -u
GS='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-23_gate20T1_seatB'
CHECKOUT='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
L="${1:-}"; SP="${2:-}"; DRY=0; [ "${3:-}" = "--dry-run" ] && DRY=1
[ -n "$L" ] && [ -x "$L" ] || { echo "usage: repin_and_launch_gate20T1.sh <launcher path> <scratchpad dir> [--dry-run] — e.g. $GS/launch_qa_secuura_batch1204-t1.sh"; exit 9; }
case "$SP" in /private/tmp/claude-501/*/scratchpad*) [ -d "$SP" ] || { echo "REFUSING: no such scratchpad dir $SP"; exit 9; } ;; *) echo "REFUSING: argv[2] must be a Claude session scratchpad under /private/tmp/claude-501/ (the re-pin's scratch clone lives there)"; exit 9;; esac
T="$(date -u +%H%M%S)"; OUTP="$GS/launch_$T"; [ "$DRY" = 1 ] && OUTP="$SP/repin_dry_$T"
PF="$(sed -n 's/^PROMPT_FILE="\${QAB1204_PROMPT:-\(.*\)}"$/\1/p' "$L")"
[ -s "$PF" ] || { echo "REFUSING: the launcher's prompt file is missing: $PF"; exit 8; }
/usr/bin/grep -qF 'PENDING-PR-' "$PF" && { echo "REFUSING: the launcher's prompt is PARTIAL — re-fill first (take_pr11_gate20T1.sh)"; exit 8; }
BASE="$(sed -n "s/^BASE_SHA='\([0-9a-f]\{40\}\)'.*/\1/p" "$L")"
DEV="$(sed -n "s/^DEVELOP_SHA='\([0-9a-f]\{40\}\)'.*/\1/p" "$L")"
END="$(sed -n "s/^END_TREE='\([0-9a-f]\{40\}\)'.*/\1/p" "$L")"
CC="$(sed -n 's/^CONTROL_COPY=\([01]\)$/\1/p' "$L")"
PANE='QA/Secuura-batch1204'
PRS="$(sed -n 's/^  "\([0-9]*\)|KS-[0-9]*|\([^|]*\)|\([0-9a-f]\{40\}\)|[0-9]*"$/\1:\3:\2/p' "$L")"
NROWS="$(sed -n '/^PRS=($/,/^)$/p' "$L" | /usr/bin/grep -c '^  "')"
[ -n "$BASE" ] && [ -n "$DEV" ] && [ -n "$PRS" ] || { echo "REFUSING: could not read the pins from $L"; exit 9; }
echo "LAUNCH ACTION$([ "$DRY" = 1 ] && echo ' (DRY RUN)') $(date '+%Y-%m-%d %H:%M:%S %Z') / $(date -u '+%Y-%m-%dT%H:%M:%SZ') | launcher $L | BASE $BASE | pinned launch develop $DEV | END_TREE $END | PRs: $(printf '%s\n' "$PRS" | cut -d: -f1 | tr '\n' ' ')"
echo "--- 0b. the batch is SEVEN pinned rows incl. PR 11 (KS-1143), and the launcher is not a CONTROL COPY"
NPIN="$(printf '%s\n' "$PRS" | /usr/bin/grep -c ':')"
echo "  rows in PRS=( ): $NROWS | rows with a 40-hex head: $NPIN | KS-1143 row: $(sed -n 's/^  "\([0-9A-Z]*\)|KS-1143|.*/\1/p' "$L") | CONTROL_COPY=$CC"
[ "$NROWS" -eq 7 ] && [ "$NPIN" -eq 7 ] && [ "$CC" = 0 ] && sed -n '/^  "[0-9]*|KS-1143|/p' "$L" | /usr/bin/grep -qE '\|[0-9a-f]{40}\|1"$' || { echo "REFUSING: the launcher does not carry SEVEN pinned rows incl. PR 11 (KS-1143), or it is a CONTROL COPY — run take_pr11_gate20T1.sh first"; exit 8; }

echo "--- 0. the pane must be routed (inbox_routing.conf) or cockpit.sh say --mail fails silently"
/usr/bin/grep -c -F "$PANE|coagent@agentmail.to|yes" /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf > "$OUTP.routing.out" 2>&1
rc=$?
echo "  routing line present: $(cat "$OUTP.routing.out") (grep rc=$rc; want 1 / rc 0; control: QA/Secuura-batch1202 = $(/usr/bin/grep -c -F 'QA/Secuura-batch1202|coagent@agentmail.to|yes' /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf))"
if [ "$rc" -ne 0 ]; then
  [ "$DRY" = 1 ] && echo "  (DRY RUN: reported, not refused — the real run refuses rc 1 here)" || { echo "REFUSING: $PANE is not registered in inbox_routing.conf — add the line first (README.md; the drafter did NOT write it)"; exit 1; }
fi

echo "--- 1. instrument: git ls-remote origin (read from the Secuura checkout, READ-ONLY)"
refs="refs/heads/develop"
for pr in $PRS; do n="${pr%%:*}"; rest="${pr#*:}"; br="${rest#*:}"; refs="$refs refs/pull/$n/head $br"; done
# shellcheck disable=SC2086
git -C "$CHECKOUT" ls-remote origin $refs > "$OUTP.lsremote.out" 2>&1
rc=$?
echo "  ls-remote rc=$rc at $(date -u +%H:%M:%SZ)"; sed 's/^/    /' "$OUTP.lsremote.out"
[ "$rc" -eq 0 ] || { echo "REFUSING: ls-remote failed"; exit 2; }
CUR_DEV="$(awk '$2=="refs/heads/develop"{print $1}' "$OUTP.lsremote.out")"

echo "--- 2. instrument: the GitHub PULLS API (an independent read of each head)"
PRS_ENV="$PRS" python3 - > "$OUTP.api_heads.out" 2>&1 <<'PY'
import json, os, urllib.request
tok = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('GH_TOKEN='): tok = l.split('=', 1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN unset'
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
for pr in os.environ['PRS_ENV'].split():
    n = int(pr.split(':')[0])
    p = get('https://api.github.com/repos/Secuura/Distributed_Secuura/pulls/%d' % n)
    print('API #%d head %s base %s (base sha %s) state %s' % (n, p['head']['sha'], p['base']['ref'], p['base']['sha'], p['state']))
PY
rc=$?
echo "  pulls API rc=$rc"; sed 's/^/    /' "$OUTP.api_heads.out"
[ "$rc" -eq 0 ] || { echo "REFUSING: the pulls API read failed"; exit 3; }

echo "--- 3. the heads, judged (both instruments == the pin, and open)"
bad=0
for pr in $PRS; do
  n="${pr%%:*}"; rest="${pr#*:}"; h="${rest%%:*}"; br="${rest#*:}"
  P="$(awk -v r="refs/pull/$n/head" '$2==r{print $1}' "$OUTP.lsremote.out")"
  B="$(awk -v r="$br" '$2==r{print $1}' "$OUTP.lsremote.out")"
  A="$(awk -v n="$n" '$1=="API" && $2=="#"n{print $4}' "$OUTP.api_heads.out")"
  S="$(awk -v n="$n" '$1=="API" && $2=="#"n{print $NF}' "$OUTP.api_heads.out")"
  echo "  #$n  ls-remote pull/head ${P:-ABSENT} | branch ${B:-ABSENT} | API ${A:-ABSENT} (state ${S:-?}) | pinned $h"
  [ "$P" = "$h" ] && [ "$B" = "$h" ] && [ "$A" = "$h" ] && [ "$S" = "open" ] || { bad=1; echo "    ^ STALE / MOVED / CLOSED"; }
done
[ "$bad" -eq 0 ] || { echo "REFUSING TO LAUNCH: a head moved (the pin is stale) or a PR is not open — a verdict is valid only at its head; re-take with take_pr11_gate20T1.sh after the seat's READY"; exit 11; }
echo "  BOTH INSTRUMENTS AGREE with the pins (7/7)."

echo "--- 3b. develop, read at launch: $CUR_DEV | the launcher's pinned launch develop $DEV | BASE $BASE"
if [ "$CUR_DEV" != "$DEV" ]; then
  if [ "$DRY" = 1 ]; then echo "  DRY RUN: develop MOVED since the launcher was generated — the real run RE-PINS here (predict -> fill -> gen) in the same action"; exit 10; fi
  echo "  develop MOVED — RE-PIN IN THIS ACTION over $CUR_DEV (scratch clone FROM ORIGIN under $SP)"
  python3 "$GS/predict_batch_scratch_gate20T1.py" "$SP" > "$OUTP.repin_predict.out" 2>&1; rc=$?; echo "  predict rc=$rc -> $OUTP.repin_predict.out"; tail -4 "$OUTP.repin_predict.out" | sed 's/^/    /'
  [ "$rc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the re-prediction over the moved develop refused (read $OUTP.repin_predict.out — a move that touches a tier-1 path is re-predicted BY HAND, never here)"; exit 10; }
  python3 "$GS/fill_prompt_gate20T1.py" > "$OUTP.repin_fill.out" 2>&1; rc=$?; echo "  fill rc=$rc"; tail -1 "$OUTP.repin_fill.out" | sed 's/^/    /'
  [ "$rc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the prompt re-fill refused"; exit 10; }
  python3 "$GS/gen_launcher_gate20T1.py" "$L" "$SP" > "$OUTP.repin_gen.out" 2>&1; rc=$?; echo "  gen rc=$rc"; tail -1 "$OUTP.repin_gen.out" | sed 's/^/    /'
  [ "$rc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the launcher regeneration refused"; exit 10; }
  DEV="$(sed -n "s/^DEVELOP_SHA='\([0-9a-f]\{40\}\)'.*/\1/p" "$L")"; END="$(sed -n "s/^END_TREE='\([0-9a-f]\{40\}\)'.*/\1/p" "$L")"
  AGAIN="$(git -C "$CHECKOUT" ls-remote origin refs/heads/develop | cut -f1)"
  echo "  re-pinned: launch develop $DEV | END_TREE $END | develop re-read now $AGAIN"
  [ "$AGAIN" = "$DEV" ] || { echo "REFUSING TO LAUNCH: develop moved AGAIN during the re-pin ($DEV -> $AGAIN) — run this script again"; exit 10; }
else
  echo "  UNMOVED since generation — the launcher's merged trees and END_TREE $END stand"
fi
if [ "$DRY" = 1 ]; then echo "DRY RUN COMPLETE $(date -u '+%Y-%m-%dT%H:%M:%SZ') — every read agrees with the pins; the real run continues with the usage gate, --check and cockpit.sh add"; exit 0; fi

echo "--- 4. usage gate"
/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/usage_gate.sh --check > "$OUTP.usage_gate.out" 2>&1
rc=$?
echo "  usage_gate rc=$rc"; sed 's/^/    /' "$OUTP.usage_gate.out"
[ "$rc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the usage gate refused (this lane's 90% cut is lifted by Kam's 2026-09-23 14:24:05 word — pass WED_USAGE_STOP=100 only with that recorded authority)"; exit 12; }

echo "--- 5. the launcher's own --check (heads, the compares against the develop just read, the grep ladder)"
"$L" --check > "$OUTP.launcher_check.out" 2>&1
rc=$?
echo "  launcher --check rc=$rc"; sed 's/^/    /' "$OUTP.launcher_check.out"
[ "$rc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the launcher refused under --check"; exit 13; }

echo "--- 6. launch through the fleet's own tooling (cockpit.sh add), never raw tmux send-keys"
/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/cockpit/cockpit.sh add "$PANE" "$L" > "$OUTP.cockpit_add.out" 2>&1
rc=$?
echo "  cockpit.sh add rc=$rc"; sed 's/^/    /' "$OUTP.cockpit_add.out"
[ "$rc" -eq 0 ] || { echo "LAUNCH FAILED at cockpit.sh add"; exit 14; }
echo "--- pane census"
/opt/homebrew/bin/tmux list-panes -a -F '#{pane_id} | #{@cockpit_name} | #{pane_current_command} | #{session_name}:#{window_index}.#{pane_index}'
echo "LAUNCHED $(date -u '+%Y-%m-%dT%H:%M:%SZ') over develop $DEV (END_TREE $END)"
