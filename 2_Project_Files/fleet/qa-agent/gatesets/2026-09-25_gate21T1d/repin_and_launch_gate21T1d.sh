#!/bin/bash
# repin_and_launch_gate21T1d.sh — the LAUNCH ACTION for the tier-1 ROUND-2 gate over #1239 KS-1263 (head c8e1875c2, Seat B 27th). The re-pin and the
# launch are ONE action (Kam 2026-09-18: a stale pin costs a whole gate session). It READS develop, the head and `mergeable` AT LAUNCH and never trusts
# a pin it did not just re-read:
#   (0)  the pane is routed (inbox_routing.conf) — rc 1;
#   (0b) the kit is at the home it was filled for; if it was MOVED (copied into gatesets/), re-measure + re-fill HERE in the same action
#        (predict_gate21T1d.py then fill_gate21T1d.py; both re-read origin and refuse on any disagreement) — rc 8;
#   (1)  origin develop + refs/pull/1239/head + the branch, by `git ls-remote` READ from the Secuura checkout (read verb only) — rc 2;
#   (2)  the head re-read from the GitHub PULLS API (a second, independent instrument; also `mergeable`, re-read up to 3x while GitHub reports null)
#        — rc 3 if the read fails;
#   (3)  rc 11 unless the head == the launcher's pin on BOTH instruments AND the PR is open AND not `mergeable: false` (A STALE HEAD REFUSES: a new head
#        needs its READY re-captured and the kit re-drafted; this script never adopts a head it was not given). `mergeable: null` after the retries is
#        REPORTED and not refused: the kit's own merge-tree over the develop it launches on (step 3b / the pins) proves the clean merge;
#   (3b) develop: if origin develop != the launcher's pinned develop, RE-PIN IN THIS SAME ACTION — predict_gate21T1d.py over the develop just read (a
#        scratch clone under <scratchpad>/g21T1d_sp; it REFUSES on any NEW overlap with the PR's own paths, a move into db.ts / shareRepo.ts /
#        packages/shared/src/db, a move hunk INSIDE the /share or /transfer-custody handler, an unclean merge, a numstat or patch-id difference, or an
#        END_TREE disagreement), then fill_gate21T1d.py — then ls-remote develop ONCE MORE: rc 10 unless it still equals the new pin;
#   (4)  the usage gate — rc 12;  (5) the launcher's own --check — rc 13;  (6) cockpit.sh add — rc 14, then a pane census.
# --dry-run: steps 0-3 and a REPORT of 0b/3b (no re-fill, no re-pin, no write outside the scratchpad), then stop before (4); the routing line's absence
# is reported, not refused; a moved develop is reported and exits 10. READ-ONLY in the Secuura checkout: ls-remote only. Nothing is merged, deployed or
# commented. The pins are READ from the launcher itself. Shape copied from gate21T1c's repin_and_launch_gate21T1c.sh, re-keyed to one row.
# Usage: repin_and_launch_gate21T1d.sh <launcher path> <a scratchpad dir under /private/tmp/claude-501/> [--dry-run]
set -u
GS="$(dirname "$(/bin/realpath "$0")")"
CHECKOUT='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
ROUTING="${G21T1D_ROUTING:-/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf}"
L="${1:-}"; SP="${2:-}"; DRY=0; [ "${3:-}" = "--dry-run" ] && DRY=1
[ -n "$L" ] && [ -x "$L" ] || { echo "usage: repin_and_launch_gate21T1d.sh <launcher path> <scratchpad dir> [--dry-run] — e.g. $GS/launch_qa_secuura_batch1239-t1r2.sh"; exit 9; }
case "$SP" in /private/tmp/claude-501/*/scratchpad*) [ -d "$SP" ] || { echo "REFUSING: no such scratchpad dir $SP"; exit 9; } ;; *) echo "REFUSING: argv[2] must be a Claude session scratchpad under /private/tmp/claude-501/"; exit 9;; esac
T="$(date -u +%H%M%S)"; OUTP="$GS/launch_$T"; [ "$DRY" = 1 ] && OUTP="$SP/repin_g21T1d_dry_$T"
PANE='QA/Secuura-batch1239'
N=1239
pin() { sed -n "s/^$1='\([0-9a-f]\{40\}\)'$/\1/p" "$L"; }
row() { sed -n "s/^  \"$1|[^|]*|\([^|]*\)|\([0-9a-f]\{40\}\)|[0-9]*|[0-9]*|[^|\"]*\"$/\\$2/p" "$L"; }
LGS="$(sed -n "s/^GS='\(.*\)'$/\1/p" "$L")"
DEV="$(pin DEVELOP_SHA)"; ET="$(pin END_TREE)"
[ -n "$DEV" ] && [ -n "$ET" ] && [ -n "$LGS" ] || { echo "REFUSING: could not read the pins (GS / DEVELOP_SHA / END_TREE) from $L"; exit 9; }
[ -n "$(row $N 2)" ] && [ -n "$(row $N 1)" ] || { echo "REFUSING: could not read #$N's row (branch|head) from $L"; exit 9; }
echo "LAUNCH ACTION$([ "$DRY" = 1 ] && echo ' (DRY RUN)') $(date '+%Y-%m-%d %H:%M:%S %Z') / $(date -u '+%Y-%m-%dT%H:%M:%SZ') | launcher $L | pinned launch develop $DEV | END_TREE $ET"
echo "  pin #$N $(row $N 2)"

echo "--- 0. the pane must be routed (inbox_routing.conf) or cockpit.sh say --mail fails silently"
/usr/bin/grep -c -F "$PANE|coagent@agentmail.to|yes" "$ROUTING" > "$OUTP.routing.out" 2>&1
rc=$?
echo "  routing line present: $(cat "$OUTP.routing.out") (grep rc=$rc; want 1 / rc 0; control: QA/Secuura-batch1234 = $(/usr/bin/grep -c -F 'QA/Secuura-batch1234|coagent@agentmail.to|yes' "$ROUTING"))"
if [ "$rc" -ne 0 ]; then
  [ "$DRY" = 1 ] && echo "  (DRY RUN: reported, not refused — the real run refuses rc 1 here)" || { echo "REFUSING: $PANE is not registered in inbox_routing.conf — add the line first (README.md section 4; the drafter did NOT write it)"; exit 1; }
fi

echo "--- 0b. the kit's home: launcher filled for $LGS | this script lives in $GS"
if [ "$LGS" != "$GS" ] || [ "$(dirname "$(/bin/realpath "$L")")" != "$GS" ]; then
  if [ "$DRY" = 1 ]; then echo "  DRY RUN: MOVED KIT — the real run re-measures + re-fills here (predict_gate21T1d.py, fill_gate21T1d.py) in the same action"; else
    [ "$(dirname "$(/bin/realpath "$L")")" = "$GS" ] || { echo "REFUSING: the launcher $L is not in this kit's directory $GS — pass $GS/launch_qa_secuura_batch1239-t1r2.sh"; exit 8; }
    python3 "$GS/predict_gate21T1d.py" "$SP" > "$OUTP.refill_predict.out" 2>&1; rc=$?; echo "  re-measure at $GS rc=$rc -> $OUTP.refill_predict.out"; tail -2 "$OUTP.refill_predict.out" | sed 's/^/    /'
    [ "$rc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the re-measurement at the new home refused (read $OUTP.refill_predict.out)"; exit 8; }
    python3 "$GS/fill_gate21T1d.py" "$SP" > "$OUTP.refill.out" 2>&1; rc=$?; echo "  re-fill at $GS rc=$rc -> $OUTP.refill.out"; tail -2 "$OUTP.refill.out" | sed 's/^/    /'
    [ "$rc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the re-fill at the new home refused (read $OUTP.refill.out)"; exit 8; }
    LGS="$(sed -n "s/^GS='\(.*\)'$/\1/p" "$L")"; [ "$LGS" = "$GS" ] || { echo "REFUSING: the re-filled launcher still names $LGS"; exit 8; }
    DEV="$(pin DEVELOP_SHA)"; ET="$(pin END_TREE)"; echo "  re-filled: launch develop $DEV | END_TREE $ET"
  fi
else echo "  AT HOME — no re-fill"; fi

echo "--- 1. instrument: git ls-remote origin (read from the Secuura checkout, READ-ONLY)"
git -C "$CHECKOUT" ls-remote origin refs/heads/develop refs/pull/$N/head "$(row $N 1)" > "$OUTP.lsremote.out" 2>&1
rc=$?
echo "  ls-remote rc=$rc at $(date -u +%H:%M:%SZ)"; sed 's/^/    /' "$OUTP.lsremote.out"
[ "$rc" -eq 0 ] || { echo "REFUSING: ls-remote failed"; exit 2; }
CUR_DEV="$(awk '$2=="refs/heads/develop"{print $1}' "$OUTP.lsremote.out")"

echo "--- 2. instrument: the GitHub PULLS API (an independent read of the head, and mergeable)"
python3 - > "$OUTP.api_heads.out" 2>&1 <<'PY'
import json, time, urllib.request
tok = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('GH_TOKEN='): tok = l.split('=', 1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN unset'
def get(n): return json.load(urllib.request.urlopen(urllib.request.Request('https://api.github.com/repos/Secuura/Distributed_Secuura/pulls/' + n, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
p = get('1239'); tries = 1
while p.get('mergeable') is None and tries < 3:
    time.sleep(10); p = get('1239'); tries += 1
print('API #1239 head %s base %s mergeable %s reads %d state %s' % (p['head']['sha'], p['base']['ref'], p.get('mergeable'), tries, p['state']))
PY
rc=$?
echo "  pulls API rc=$rc"; sed 's/^/    /' "$OUTP.api_heads.out"
[ "$rc" -eq 0 ] || { echo "REFUSING: the pulls API read failed"; exit 3; }

echo "--- 3. the head, judged (both instruments == the pin, open, not mergeable:false)"
H="$(row $N 2)"; BR="$(row $N 1)"
P="$(awk -v r="refs/pull/$N/head" '$2==r{print $1}' "$OUTP.lsremote.out")"
B="$(awk -v r="$BR" '$2==r{print $1}' "$OUTP.lsremote.out")"
A="$(awk -v n="#$N" '$1=="API" && $2==n{print $4}' "$OUTP.api_heads.out")"; S="$(awk -v n="#$N" '$1=="API" && $2==n{print $NF}' "$OUTP.api_heads.out")"
M="$(awk -v n="#$N" '$1=="API" && $2==n{print $8}' "$OUTP.api_heads.out")"
echo "  #$N  ls-remote pull/head ${P:-ABSENT} | branch ${B:-ABSENT} | API ${A:-ABSENT} (state ${S:-?}, mergeable ${M:-?}) | pinned $H"
[ "$M" = "None" ] && echo "    NOTE: GitHub has not computed mergeable for #$N after 3 reads — the kit's own merge-tree over the launch develop is the clean-merge proof (pins_gate21T1d.json)"
[ "$P" = "$H" ] && [ "$B" = "$H" ] && [ "$A" = "$H" ] && [ "$S" = "open" ] && [ "$M" != "False" ] || { echo "REFUSING TO LAUNCH: the head moved (the pin is stale), the PR is not open, or GitHub reports mergeable:false — a verdict is valid only at its head; a new head needs the seat's READY, a capture, predict_gate21T1d.py and fill_gate21T1d.py first"; exit 11; }
echo "  BOTH INSTRUMENTS AGREE with the pin."

echo "--- 3b. develop, read at launch: $CUR_DEV | the launcher's pinned launch develop $DEV"
if [ "$CUR_DEV" != "$DEV" ]; then
  if [ "$DRY" = 1 ]; then echo "  DRY RUN: develop MOVED since the launcher was filled — the real run RE-PINS here (predict -> fill) in the same action"; exit 10; fi
  echo "  develop MOVED — RE-PIN IN THIS ACTION over $CUR_DEV (scratch clone under $SP/g21T1d_sp)"
  python3 "$GS/predict_gate21T1d.py" "$SP" > "$OUTP.repin_predict.out" 2>&1; rc=$?; echo "  predict rc=$rc -> $OUTP.repin_predict.out"; tail -3 "$OUTP.repin_predict.out" | sed 's/^/    /'
  [ "$rc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the re-measurement over the moved develop refused (read $OUTP.repin_predict.out — a move into the PR's own paths beyond the two known overlaps, into the cells' reach, or inside the two handlers is re-predicted BY HAND, never here)"; exit 10; }
  python3 "$GS/fill_gate21T1d.py" "$SP" > "$OUTP.repin_fill.out" 2>&1; rc=$?; echo "  fill rc=$rc"; tail -1 "$OUTP.repin_fill.out" | sed 's/^/    /'
  [ "$rc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the re-fill refused"; exit 10; }
  DEV="$(pin DEVELOP_SHA)"; ET="$(pin END_TREE)"
  AGAIN="$(git -C "$CHECKOUT" ls-remote origin refs/heads/develop | cut -f1)"
  echo "  re-pinned: launch develop $DEV | END_TREE $ET | develop re-read now $AGAIN"
  [ "$AGAIN" = "$DEV" ] || { echo "REFUSING TO LAUNCH: develop moved AGAIN during the re-pin ($DEV -> $AGAIN) — run this script again"; exit 10; }
else
  echo "  UNMOVED since the fill — the END_TREE $ET stands"
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
