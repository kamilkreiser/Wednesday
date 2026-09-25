#!/bin/bash
# repin_and_launch_gate21T2b.sh — the LAUNCH ACTION for the round-21 SECOND tier-2 batch gate over #1225 KS-1291, #1227 KS-1252+1253,
# #1229 KS-865+808(3), #1231 KS-1281, #1232 KS-1128 (FROZEN at five).
# The re-pin and the launch are ONE action (Kam 2026-09-18: a stale pin costs a whole gate session). It READS develop and the five heads AT LAUNCH and
# never trusts a pin it did not just re-read (five rows; #1227 and #1229 are two commits each, ahead 2):
#   (0)  the pane is routed (inbox_routing.conf) — rc 1;
#   (0b) the kit is at the home it was filled for; if it was MOVED (copied into gatesets/), re-fill HERE in the same action (fill_gate21T2b.py re-reads
#        develop + the five heads and refuses on any disagreement with the pins) — rc 8;
#   (1)  origin develop + refs/pull/N/head + the branch for all five by `git ls-remote`, READ from the Secuura checkout (read verb only) — rc 2;
#   (2)  the five heads re-read from the GitHub PULLS API (a second, independent instrument), with `mergeable` — rc 3 if a read fails;
#   (3)  rc 11 unless every head == the launcher's pin on BOTH instruments AND every PR is open AND none reads mergeable=False (A STALE HEAD REFUSES: a new head needs its READY
#        re-captured, predict + fill re-run; this script never adopts a head it was not given);
#   (3b) develop: if origin develop != the launcher's pinned launch develop (the batch1215 tier-2 gate's and the next tier-1 batch's merges are the
#        likely movers), RE-PIN IN THIS SAME ACTION — predict_gate21T2b.py over the develop just read (a scratch clone FROM ORIGIN under <scratchpad>; it REFUSES unless the move
#        descends from BASE, touches none of the 10 paths, the BASE-INVARIANT check holds, and the END_TREE agrees in three orders + a second instrument), then fill_gate21T2b.py — then ls-remote develop ONCE MORE: rc 10 unless it still equals the new pin;
#   (4)  the usage gate — rc 12;  (5) the launcher's own --check — rc 13;  (6) cockpit.sh add — rc 14, then a pane census.
# --dry-run: steps 0-3 and a REPORT of 0b/3b (no re-fill, no re-pin, no write outside the scratchpad), then stop before (4); the routing line's absence
# is reported, not refused. READ-ONLY in the Secuura checkout: ls-remote only. Nothing is merged, deployed or commented. The pins are READ from the
# launcher itself. Derived (derive_repin_gate21T2b.py) from the sibling tier-2 kit's repin script of the same round, re-keyed to five rows.
# Usage: repin_and_launch_gate21T2b.sh <launcher path> <a scratchpad dir under /private/tmp/claude-501/> [--dry-run]
set -u
GS="$(dirname "$(/bin/realpath "$0")")"
CHECKOUT='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
ROUTING='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf'
L="${1:-}"; SP="${2:-}"; DRY=0; [ "${3:-}" = "--dry-run" ] && DRY=1
[ -n "$L" ] && [ -x "$L" ] || { echo "usage: repin_and_launch_gate21T2b.sh <launcher path> <scratchpad dir> [--dry-run] — e.g. $GS/launch_qa_secuura_batch1225-t2.sh"; exit 9; }
case "$SP" in /private/tmp/claude-501/*/scratchpad*) [ -d "$SP" ] || { echo "REFUSING: no such scratchpad dir $SP"; exit 9; } ;; *) echo "REFUSING: argv[2] must be a Claude session scratchpad under /private/tmp/claude-501/"; exit 9;; esac
T="$(date -u +%H%M%S)"; OUTP="$GS/launch_$T"; [ "$DRY" = 1 ] && OUTP="$SP/repin_g21T2b_dry_$T"
PANE='QA/Secuura-batch1225'
pin() { sed -n "s/^$1='\([0-9a-f]\{40\}\)'$/\1/p" "$L"; }
row() { sed -n "s/^  \"$1|[^|]*|\([^|]*\)|\([0-9a-f]\{40\}\)|[0-9]*|[0-9]*\"$/\\$2/p" "$L"; }
NS='1225 1227 1229 1231 1232'
LGS="$(sed -n "s/^GS='\(.*\)'$/\1/p" "$L")"
DEV="$(pin DEVELOP_SHA)"; ET="$(sed -n "s/^END_TREE='\([0-9a-f]\{40\}\)'$/\1/p" "$L")"
[ -n "$DEV" ] && [ -n "$ET" ] && [ -n "$LGS" ] || { echo "REFUSING: could not read the pins (GS / DEVELOP_SHA / END_TREE) from $L"; exit 9; }
for n in $NS; do [ -n "$(row $n 2)" ] && [ -n "$(row $n 1)" ] || { echo "REFUSING: could not read #$n's row (branch|head) from $L"; exit 9; }; done
echo "LAUNCH ACTION$([ "$DRY" = 1 ] && echo ' (DRY RUN)') $(date '+%Y-%m-%d %H:%M:%S %Z') / $(date -u '+%Y-%m-%dT%H:%M:%SZ') | launcher $L | pinned launch develop $DEV | END_TREE $ET"
for n in $NS; do echo "  pin #$n $(row $n 2)"; done

echo "--- 0. the pane must be routed (inbox_routing.conf) or cockpit.sh say --mail fails silently"
/usr/bin/grep -c -F "$PANE|coagent@agentmail.to|yes" "$ROUTING" > "$OUTP.routing.out" 2>&1
rc=$?
echo "  routing line present: $(cat "$OUTP.routing.out") (grep rc=$rc; want 1 / rc 0; control: QA/Secuura-batch1215 = $(/usr/bin/grep -c -F 'QA/Secuura-batch1215|coagent@agentmail.to|yes' "$ROUTING"))"
if [ "$rc" -ne 0 ]; then
  [ "$DRY" = 1 ] && echo "  (DRY RUN: reported, not refused — the real run refuses rc 1 here)" || { echo "REFUSING: $PANE is not registered in inbox_routing.conf — add the line first (README.md section 4; the drafter did NOT write it)"; exit 1; }
fi

echo "--- 0b. the kit's home: launcher filled for $LGS | this script lives in $GS"
if [ "$LGS" != "$GS" ] || [ "$(dirname "$(/bin/realpath "$L")")" != "$GS" ]; then
  if [ "$DRY" = 1 ]; then echo "  DRY RUN: MOVED KIT — the real run re-fills here (fill_gate21T2b.py) in the same action"; else
    [ "$(dirname "$(/bin/realpath "$L")")" = "$GS" ] || { echo "REFUSING: the launcher $L is not in this kit's directory $GS — pass $GS/launch_qa_secuura_batch1225-t2.sh"; exit 8; }
    python3 "$GS/fill_gate21T2b.py" "$SP" > "$OUTP.refill.out" 2>&1; rc=$?; echo "  re-fill at $GS rc=$rc -> $OUTP.refill.out"; tail -2 "$OUTP.refill.out" | sed 's/^/    /'
    [ "$rc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the re-fill at the new home refused (read $OUTP.refill.out)"; exit 8; }
    LGS="$(sed -n "s/^GS='\(.*\)'$/\1/p" "$L")"; [ "$LGS" = "$GS" ] || { echo "REFUSING: the re-filled launcher still names $LGS"; exit 8; }
  fi
else echo "  AT HOME — no re-fill"; fi

echo "--- 1. instrument: git ls-remote origin (read from the Secuura checkout, READ-ONLY)"
git -C "$CHECKOUT" ls-remote origin refs/heads/develop refs/pull/1225/head refs/pull/1227/head refs/pull/1229/head refs/pull/1231/head refs/pull/1232/head \
  "$(row 1225 1)" "$(row 1227 1)" "$(row 1229 1)" "$(row 1231 1)" "$(row 1232 1)" > "$OUTP.lsremote.out" 2>&1
rc=$?
echo "  ls-remote rc=$rc at $(date -u +%H:%M:%SZ)"; sed 's/^/    /' "$OUTP.lsremote.out"
[ "$rc" -eq 0 ] || { echo "REFUSING: ls-remote failed"; exit 2; }
CUR_DEV="$(awk '$2=="refs/heads/develop"{print $1}' "$OUTP.lsremote.out")"

echo "--- 2. instrument: the GitHub PULLS API (an independent read of each head)"
python3 - > "$OUTP.api_heads.out" 2>&1 <<'PY'
import json, urllib.request
tok = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('GH_TOKEN='): tok = l.split('=', 1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN unset'
for n in ('1225', '1227', '1229', '1231', '1232'):
    p = json.load(urllib.request.urlopen(urllib.request.Request('https://api.github.com/repos/Secuura/Distributed_Secuura/pulls/' + n, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
    print('API #%s head %s base %s mergeable %s state %s' % (n, p['head']['sha'], p['base']['ref'], p.get('mergeable'), p['state']))
PY
rc=$?
echo "  pulls API rc=$rc"; sed 's/^/    /' "$OUTP.api_heads.out"
[ "$rc" -eq 0 ] || { echo "REFUSING: a pulls API read failed"; exit 3; }

echo "--- 3. the heads, judged (both instruments == the pin, and open)"
bad=0
for n in $NS; do
  H="$(row $n 2)"; BR="$(row $n 1)"
  P="$(awk -v r="refs/pull/$n/head" '$2==r{print $1}' "$OUTP.lsremote.out")"
  B="$(awk -v r="$BR" '$2==r{print $1}' "$OUTP.lsremote.out")"
  A="$(awk -v n="#$n" '$1=="API" && $2==n{print $4}' "$OUTP.api_heads.out")"; S="$(awk -v n="#$n" '$1=="API" && $2==n{print $NF}' "$OUTP.api_heads.out")"; M="$(awk -v n="#$n" '$1=="API" && $2==n{print $(NF-2)}' "$OUTP.api_heads.out")"
  echo "  #$n  ls-remote pull/head ${P:-ABSENT} | branch ${B:-ABSENT} | API ${A:-ABSENT} (state ${S:-?}, mergeable ${M:-?}) | pinned $H"
  [ "$P" = "$H" ] && [ "$B" = "$H" ] && [ "$A" = "$H" ] && [ "$S" = "open" ] && [ "$M" != "False" ] || { echo "    STALE, CLOSED or NOT MERGEABLE: #$n"; bad=1; }
done
[ "$bad" = 0 ] || { echo "REFUSING TO LAUNCH: a head moved (the pin is stale) or a PR is not open — a verdict is valid only at its head; a new head needs the seat's READY, capture_mail_gate21T2b.py, predict_gate21T2b.py and fill_gate21T2b.py first"; exit 11; }
echo "  BOTH INSTRUMENTS AGREE with all five pins."

echo "--- 3b. develop, read at launch: $CUR_DEV | the launcher's pinned launch develop $DEV"
if [ "$CUR_DEV" != "$DEV" ]; then
  if [ "$DRY" = 1 ]; then echo "  DRY RUN: develop MOVED since the launcher was generated — the real run RE-PINS here (predict -> fill) in the same action"; exit 10; fi
  echo "  develop MOVED — RE-PIN IN THIS ACTION over $CUR_DEV (scratch clone FROM ORIGIN under $SP)"
  python3 "$GS/predict_gate21T2b.py" "$SP" > "$OUTP.repin_predict.out" 2>&1; rc=$?; echo "  predict rc=$rc -> $OUTP.repin_predict.out"; tail -3 "$OUTP.repin_predict.out" | sed 's/^/    /'
  [ "$rc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the re-measurement over the moved develop refused (read $OUTP.repin_predict.out — a move that touches the batch's paths is re-predicted BY HAND, never here)"; exit 10; }
  python3 "$GS/fill_gate21T2b.py" "$SP" > "$OUTP.repin_fill.out" 2>&1; rc=$?; echo "  fill rc=$rc"; tail -1 "$OUTP.repin_fill.out" | sed 's/^/    /'
  [ "$rc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the re-fill refused"; exit 10; }
  DEV="$(pin DEVELOP_SHA)"; ET="$(sed -n "s/^END_TREE='\([0-9a-f]\{40\}\)'$/\1/p" "$L")"
  AGAIN="$(git -C "$CHECKOUT" ls-remote origin refs/heads/develop | cut -f1)"
  echo "  re-pinned: launch develop $DEV | END_TREE $ET | develop re-read now $AGAIN"
  [ "$AGAIN" = "$DEV" ] || { echo "REFUSING TO LAUNCH: develop moved AGAIN during the re-pin ($DEV -> $AGAIN) — run this script again"; exit 10; }
else
  echo "  UNMOVED since generation — the END_TREE $ET stands"
fi
if [ "$DRY" = 1 ]; then echo "DRY RUN COMPLETE $(date -u '+%Y-%m-%dT%H:%M:%SZ') — every read agrees with the pins; the real run continues with the usage gate, --check and cockpit.sh add"; exit 0; fi

echo "--- 4. usage gate"
/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/usage_gate.sh --check > "$OUTP.usage_gate.out" 2>&1
rc=$?
echo "  usage_gate rc=$rc"; sed 's/^/    /' "$OUTP.usage_gate.out"
[ "$rc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the usage gate refused (pass WED_USAGE_STOP only with Kam's recorded authority for this lane)"; exit 12; }

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
echo "LAUNCHED $(date -u '+%Y-%m-%dT%H:%M:%SZ') over develop $DEV (END_TREE $ET)"
