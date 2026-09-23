#!/bin/bash
# repin_and_launch_r2.sh — the LAUNCH ACTION for the #1210 KS-1239 round-2 re-gate. The re-pin and the launch are ONE action (Kam 2026-09-18: a stale pin
# costs a whole gate session). It READS develop and the head AT LAUNCH and never trusts a pin it did not just re-read:
#   (0)  the pane is routed (inbox_routing.conf) — rc 1;
#   (1)  origin develop + refs/pull/1210/head + the branch by `git ls-remote`, READ from the Secuura checkout (read verb only) — rc 2;
#   (2)  the head re-read from the GitHub PULLS API (a second, independent instrument) — rc 3 if the read fails;
#   (3)  rc 11 unless the head == the launcher's pin on BOTH instruments AND the PR is open (A STALE HEAD REFUSES — a new head needs a new READY, a new
#        capture and a re-fill; this script never adopts a head it was not given);
#   (3b) develop: if origin develop != the launcher's pinned launch develop, RE-PIN IN THIS SAME ACTION — predict_r2.py over the develop just read (a
#        scratch clone FROM ORIGIN under <scratchpad>; it REFUSES unless the move descends from dd8f99cc75b9, touches none of #1210's 3 paths, the merged
#        tree agrees in three instruments and the #1212-overlap control fires), then fill_r2.py (re-reads develop + head again, refuses on any
#        disagreement) — then ls-remote develop ONCE MORE: rc 10 unless it still equals the new pin;
#   (4)  the usage gate — rc 12;  (5) the launcher's own --check — rc 13;  (6) cockpit.sh add — rc 14, then a pane census.
# --dry-run: steps 0-3 and a REPORT of 3b (no re-pin, no write outside the scratchpad), then stop before (4); the routing line's absence is reported, not
# refused. READ-ONLY in the Secuura checkout: ls-remote only. Nothing is merged, deployed or commented. The pins are READ from the launcher itself.
# Derived from gatesets/2026-09-23_gate20T1_seatB/repin_and_launch_gate20T1.sh, reduced to one PR. Wednesday runs this; the drafter ran only --dry-run + controls.
# Usage: repin_and_launch_r2.sh <launcher path> <a scratchpad dir under /private/tmp/claude-501/> [--dry-run]
set -u
GS='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-23_gate20T1r2_1210'
CHECKOUT='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
L="${1:-}"; SP="${2:-}"; DRY=0; [ "${3:-}" = "--dry-run" ] && DRY=1
[ -n "$L" ] && [ -x "$L" ] || { echo "usage: repin_and_launch_r2.sh <launcher path> <scratchpad dir> [--dry-run] — e.g. $GS/launch_qa_secuura_1210-t1r2.sh"; exit 9; }
case "$SP" in /private/tmp/claude-501/*/scratchpad*) [ -d "$SP" ] || { echo "REFUSING: no such scratchpad dir $SP"; exit 9; } ;; *) echo "REFUSING: argv[2] must be a Claude session scratchpad under /private/tmp/claude-501/"; exit 9;; esac
T="$(date -u +%H%M%S)"; OUTP="$GS/launch_$T"; [ "$DRY" = 1 ] && OUTP="$SP/repin_r2_dry_$T"
PANE='QA/Secuura-1210r2'
HEAD="$(sed -n "s/^HEAD_SHA='\([0-9a-f]\{40\}\)'$/\1/p" "$L")"
BR="$(sed -n "s/^PR_BR='\(refs\/heads\/[^']*\)'$/\1/p" "$L")"
DEV="$(sed -n "s/^DEVELOP_SHA='\([0-9a-f]\{40\}\)'$/\1/p" "$L")"
MT="$(sed -n "s/^MERGED_TREE='\([0-9a-f]\{40\}\)'$/\1/p" "$L")"
[ -n "$HEAD" ] && [ -n "$BR" ] && [ -n "$DEV" ] && [ -n "$MT" ] || { echo "REFUSING: could not read the pins (HEAD_SHA / PR_BR / DEVELOP_SHA / MERGED_TREE) from $L"; exit 9; }
echo "LAUNCH ACTION$([ "$DRY" = 1 ] && echo ' (DRY RUN)') $(date '+%Y-%m-%d %H:%M:%S %Z') / $(date -u '+%Y-%m-%dT%H:%M:%SZ') | launcher $L | head pin $HEAD | pinned launch develop $DEV | merged tree $MT"

echo "--- 0. the pane must be routed (inbox_routing.conf) or cockpit.sh say --mail fails silently"
/usr/bin/grep -c -F "$PANE|coagent@agentmail.to|yes" /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf > "$OUTP.routing.out" 2>&1
rc=$?
echo "  routing line present: $(cat "$OUTP.routing.out") (grep rc=$rc; want 1 / rc 0; control: QA/Secuura-batch1204 = $(/usr/bin/grep -c -F 'QA/Secuura-batch1204|coagent@agentmail.to|yes' /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf))"
if [ "$rc" -ne 0 ]; then
  [ "$DRY" = 1 ] && echo "  (DRY RUN: reported, not refused — the real run refuses rc 1 here)" || { echo "REFUSING: $PANE is not registered in inbox_routing.conf — add the line first (README.md; the drafter did NOT write it)"; exit 1; }
fi

echo "--- 1. instrument: git ls-remote origin (read from the Secuura checkout, READ-ONLY)"
git -C "$CHECKOUT" ls-remote origin refs/heads/develop refs/pull/1210/head "$BR" > "$OUTP.lsremote.out" 2>&1
rc=$?
echo "  ls-remote rc=$rc at $(date -u +%H:%M:%SZ)"; sed 's/^/    /' "$OUTP.lsremote.out"
[ "$rc" -eq 0 ] || { echo "REFUSING: ls-remote failed"; exit 2; }
CUR_DEV="$(awk '$2=="refs/heads/develop"{print $1}' "$OUTP.lsremote.out")"

echo "--- 2. instrument: the GitHub PULLS API (an independent read of the head)"
python3 - > "$OUTP.api_head.out" 2>&1 <<'PY'
import json, urllib.request
tok = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('GH_TOKEN='): tok = l.split('=', 1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN unset'
p = json.load(urllib.request.urlopen(urllib.request.Request('https://api.github.com/repos/Secuura/Distributed_Secuura/pulls/1210', headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
print('API #1210 head %s base %s state %s' % (p['head']['sha'], p['base']['ref'], p['state']))
PY
rc=$?
echo "  pulls API rc=$rc"; sed 's/^/    /' "$OUTP.api_head.out"
[ "$rc" -eq 0 ] || { echo "REFUSING: the pulls API read failed"; exit 3; }

echo "--- 3. the head, judged (both instruments == the pin, and open)"
P="$(awk '$2=="refs/pull/1210/head"{print $1}' "$OUTP.lsremote.out")"
B="$(awk -v r="$BR" '$2==r{print $1}' "$OUTP.lsremote.out")"
A="$(awk '$1=="API"{print $4}' "$OUTP.api_head.out")"; S="$(awk '$1=="API"{print $NF}' "$OUTP.api_head.out")"
echo "  #1210  ls-remote pull/head ${P:-ABSENT} | branch ${B:-ABSENT} | API ${A:-ABSENT} (state ${S:-?}) | pinned $HEAD"
[ "$P" = "$HEAD" ] && [ "$B" = "$HEAD" ] && [ "$A" = "$HEAD" ] && [ "$S" = "open" ] || { echo "REFUSING TO LAUNCH: the head moved (the pin is stale) or the PR is not open — a verdict is valid only at its head; a new head needs the seat's READY, capture_mail_r2.py, predict_r2.py and fill_r2.py first"; exit 11; }
echo "  BOTH INSTRUMENTS AGREE with the pin."

echo "--- 3b. develop, read at launch: $CUR_DEV | the launcher's pinned launch develop $DEV"
if [ "$CUR_DEV" != "$DEV" ]; then
  if [ "$DRY" = 1 ]; then echo "  DRY RUN: develop MOVED since the launcher was generated — the real run RE-PINS here (predict -> fill) in the same action"; exit 10; fi
  echo "  develop MOVED — RE-PIN IN THIS ACTION over $CUR_DEV (scratch clone FROM ORIGIN under $SP)"
  python3 "$GS/predict_r2.py" "$SP" > "$OUTP.repin_predict.out" 2>&1; rc=$?; echo "  predict rc=$rc -> $OUTP.repin_predict.out"; tail -3 "$OUTP.repin_predict.out" | sed 's/^/    /'
  [ "$rc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the re-measurement over the moved develop refused (read $OUTP.repin_predict.out — a move that touches #1210's paths is re-predicted BY HAND, never here)"; exit 10; }
  python3 "$GS/fill_r2.py" > "$OUTP.repin_fill.out" 2>&1; rc=$?; echo "  fill rc=$rc"; tail -1 "$OUTP.repin_fill.out" | sed 's/^/    /'
  [ "$rc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the re-fill refused"; exit 10; }
  [ "$L" = "$GS/launch_qa_secuura_1210-t1r2.sh" ] || { echo "REFUSING TO LAUNCH: fill_r2.py regenerated $GS/launch_qa_secuura_1210-t1r2.sh, not $L — launch that one"; exit 10; }
  DEV="$(sed -n "s/^DEVELOP_SHA='\([0-9a-f]\{40\}\)'$/\1/p" "$L")"; MT="$(sed -n "s/^MERGED_TREE='\([0-9a-f]\{40\}\)'$/\1/p" "$L")"
  AGAIN="$(git -C "$CHECKOUT" ls-remote origin refs/heads/develop | cut -f1)"
  echo "  re-pinned: launch develop $DEV | merged tree $MT | develop re-read now $AGAIN"
  [ "$AGAIN" = "$DEV" ] || { echo "REFUSING TO LAUNCH: develop moved AGAIN during the re-pin ($DEV -> $AGAIN) — run this script again"; exit 10; }
else
  echo "  UNMOVED since generation — the merged tree $MT stands"
fi
if [ "$DRY" = 1 ]; then echo "DRY RUN COMPLETE $(date -u '+%Y-%m-%dT%H:%M:%SZ') — every read agrees with the pins; the real run continues with the usage gate, --check and cockpit.sh add"; exit 0; fi

echo "--- 4. usage gate"
/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/usage_gate.sh --check > "$OUTP.usage_gate.out" 2>&1
rc=$?
echo "  usage_gate rc=$rc"; sed 's/^/    /' "$OUTP.usage_gate.out"
[ "$rc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the usage gate refused (this lane's 90% cut is lifted by Kam's 2026-09-23 14:24:05 word — pass WED_USAGE_STOP=100 only with that recorded authority)"; exit 12; }

echo "--- 5. the launcher's own --check"
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
echo "LAUNCHED $(date -u '+%Y-%m-%dT%H:%M:%SZ') over develop $DEV (merged tree $MT)"
