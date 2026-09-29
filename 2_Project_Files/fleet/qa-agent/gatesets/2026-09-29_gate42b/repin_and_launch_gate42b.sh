#!/bin/bash
# repin_and_launch_gate42b.sh — the LAUNCH ACTION for the gate42b kit (the directory this script lives in; kit.json beside it names the kit, its pane
# and its PR). Re-pin and launch are ONE action (Kam 2026-09-18). It READS develop, the head and `mergeable` AT LAUNCH and never trusts a pin it did
# not just re-read:
#   (0)  the pane is routed (inbox_routing.conf) — rc 1;
#   (0b) the kit is at the home it was filled for; if MOVED, re-measure + re-fill HERE (pin_gate42b.py, fill_gate42b.py) — rc 8;
#   (1)  origin develop + refs/pull/1340/head + the branch, by `git ls-remote` READ from the Secuura checkout — rc 2;
#   (2)  the head re-read from the GitHub PULLS API (a second instrument; `mergeable` re-read up to 3x while null) — rc 3;
#   (2b) the OVERLAP census: every OTHER open PR's file list (PULLS API /files): rc 15 if any touches the audit baseline (the one path this PR changes)
#        — a second baseline edit in flight must be sequenced by Wednesday, never raced;
#   (3)  rc 11 unless the head == the launcher's pin on BOTH instruments (WHOLE-FIELD), the PR is open, not `mergeable: false`, based on develop;
#   (3b) develop: if origin develop != the pinned develop, RE-PIN IN THIS ACTION (pin_gate42b.py --expect-head <pin>: refuses if the move touched the
#        baseline or the merge is unclean; then fill_gate42b.py), then ls-remote develop once more — rc 10;
#   (3c) the FUSE clock: prints the minutes left to 2026-09-30T00:00Z (a WARNING past it: the base legs red by design; never a refusal);
#   (4)  G42B_* overrides refuse a real launch — rc 16;  (5) the usage gate — rc 12;  (6) the launcher's own --check — rc 13;
#   (7)  cockpit.sh add — rc 14, then a pane census.
# --dry-run: steps 0-3c (no re-fill, no re-pin, no write outside the scratchpad), then stop before (4); the routing line's absence is REPORTED, not
# refused; a moved develop is reported and exits 10. READ-ONLY in the Secuura checkout: ls-remote only. Nothing is merged, deployed or commented.
# Controls-only overrides: G42B_ROUTING (routing file), G42B_OVERLAP_PATH (the census path), G42B_STOP_AFTER_3B (a real run stops after 3c).
# Shape copied from gate42's repin, cut to ONE PR, no stack, no WIDEN census (replaced by the baseline-overlap census).
# Usage: repin_and_launch_gate42b.sh <launcher path> <a scratchpad dir under /private/tmp/claude-501/> [--dry-run]
set -u
GS="$(dirname "$(/bin/realpath "$0")")"
CHECKOUT='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
ROUTING="${G42B_ROUTING:-/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf}"
KJ() { python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))[sys.argv[2]])' "$GS/kit.json" "$1"; }
KIT="$(KJ kit)"; PANE="$(KJ pane)"; N="$(KJ pr)"; KPATH="$(KJ path)"; FUSE="$(KJ fuse_utc)"
L="${1:-}"; SP="${2:-}"; DRY=0; [ "${3:-}" = "--dry-run" ] && DRY=1
[ -n "$L" ] && [ -x "$L" ] || { echo "usage: repin_and_launch_$KIT.sh <launcher path> <scratchpad dir> [--dry-run] — e.g. $GS/$(KJ launcher)"; exit 9; }
case "$SP" in /private/tmp/claude-501/*/scratchpad*) [ -d "$SP" ] || { echo "REFUSING: no such scratchpad dir $SP"; exit 9; } ;; *) echo "REFUSING: argv[2] must be a Claude session scratchpad under /private/tmp/claude-501/"; exit 9;; esac
T="$(date -u +%H%M%S)"; OUTP="$GS/launch_$T"; [ "$DRY" = 1 ] && OUTP="$SP/repin_${KIT}_dry_$T"
pin() { sed -n "s/^$1='\([0-9a-f]\{40\}\)'$/\1/p" "$L"; }
ROWL="$(sed -n "s/^  \"$N|[^|]*|\([^|]*\)|\([0-9a-f]\{40\}\)|.*\"$/\1 \2/p" "$L")"; BR="${ROWL% *}"; H="${ROWL#* }"
LGS="$(sed -n "s/^GS='\(.*\)'$/\1/p" "$L")"
DEV="$(pin DEVELOP_SHA)"; ET="$(pin END_TREE)"
[ -n "$DEV" ] && [ -n "$ET" ] && [ -n "$LGS" ] && [ -n "$ROWL" ] || { echo "REFUSING: could not read the pins (GS / DEVELOP_SHA / END_TREE / the #$N row) from $L"; exit 9; }
echo "LAUNCH ACTION $KIT$([ "$DRY" = 1 ] && echo ' (DRY RUN)') $(date '+%Y-%m-%d %H:%M:%S %Z') / $(date -u '+%Y-%m-%dT%H:%M:%SZ') | launcher $L | pinned develop $DEV | END_TREE $ET"
echo "  pin #$N $H ($BR)"

echo "--- 0. the pane must be routed (inbox_routing.conf) or cockpit.sh say --mail fails silently"
/usr/bin/grep -c -x -F "$PANE|coagent@agentmail.to|yes" "$ROUTING" > "$OUTP.routing.out" 2>&1
rc=$?
echo "  routing file $ROUTING — line present: $(cat "$OUTP.routing.out") (grep rc=$rc; want 1 / rc 0)"
if [ "$rc" -ne 0 ]; then
  [ "$DRY" = 1 ] && echo "  (DRY RUN: reported, not refused — the real run refuses rc 1 here)" || { echo "REFUSING: $PANE is not registered in inbox_routing.conf — add the line first (README.md section 4; the drafter did NOT write it)"; exit 1; }
fi

echo "--- 0b. the kit's home: launcher filled for $LGS | this script lives in $GS"
if [ "$LGS" != "$GS" ] || [ "$(dirname "$(/bin/realpath "$L")")" != "$GS" ]; then
  if [ "$DRY" = 1 ]; then echo "  DRY RUN: MOVED KIT — the real run re-measures + re-fills here in the same action"; else
    [ "$(dirname "$(/bin/realpath "$L")")" = "$GS" ] || { echo "REFUSING: the launcher $L is not in this kit's directory $GS"; exit 8; }
    python3 "$GS/pin_gate42b.py" "$SP" --expect-head "$H" > "$OUTP.refill_pin.out" 2>&1 && python3 "$GS/fill_gate42b.py" > "$OUTP.refill.out" 2>&1 || { echo "REFUSING TO LAUNCH: re-pin / re-fill at the new home refused (read $OUTP.refill_pin.out / $OUTP.refill.out)"; exit 8; }
    LGS="$(sed -n "s/^GS='\(.*\)'$/\1/p" "$L")"; [ "$LGS" = "$GS" ] || { echo "REFUSING: the re-filled launcher still names $LGS"; exit 8; }
    DEV="$(pin DEVELOP_SHA)"; ET="$(pin END_TREE)"; echo "  re-filled: develop $DEV | END_TREE $ET"
  fi
else echo "  AT HOME — no re-fill"; fi

echo "--- 1. instrument: git ls-remote origin (read from the Secuura checkout, READ-ONLY)"
git -C "$CHECKOUT" ls-remote origin refs/heads/develop "refs/pull/$N/head" "$BR" > "$OUTP.lsremote.out" 2>&1
rc=$?
echo "  ls-remote rc=$rc at $(date -u +%H:%M:%SZ)"; sed 's/^/    /' "$OUTP.lsremote.out"
[ "$rc" -eq 0 ] || { echo "REFUSING: ls-remote failed"; exit 2; }
CUR_DEV="$(awk '$2=="refs/heads/develop"{print $1}' "$OUTP.lsremote.out")"

echo "--- 2. instrument: the GitHub PULLS API (an independent read of the head, and mergeable) + 2b the baseline OVERLAP census"
N="$N" KPATH="${G42B_OVERLAP_PATH:-$KPATH}" python3 - > "$OUTP.api_heads.out" 2>&1 <<'PY'
import json, os, time, urllib.request, urllib.error
tok = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('GH_TOKEN='): tok = l.split('=', 1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN unset'
def get(u):
    for i in range(4):
        try: return json.load(urllib.request.urlopen(urllib.request.Request('https://api.github.com/repos/Secuura/Distributed_Secuura/' + u, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
        except urllib.error.HTTPError as e:
            if e.code < 500 or i == 3: raise
            time.sleep(10)
n, kp = os.environ['N'], os.environ['KPATH']
p = get('pulls/' + n); tries = 1
while p.get('mergeable') is None and tries < 3:
    time.sleep(10); p = get('pulls/' + n); tries += 1
print('API #%s head %s base %s mergeable %s reads %d state %s' % (n, p['head']['sha'], p['base']['ref'], p.get('mergeable'), tries, p['state']))
opened = get('pulls?state=open&per_page=100'); hits = 0
for x in opened:
    if str(x['number']) == n: continue
    fs = [f['filename'] for f in get('pulls/%s/files?per_page=100' % x['number'])]
    if kp in fs: hits += 1; print('OVERLAP #%s %s | %s | touches %s' % (x['number'], x['head']['ref'][:70], x['title'][:90], kp))
print('CENSUS %d other open PR(s) read | %d touch %s' % (len(opened) - 1, hits, kp))
PY
rc=$?
echo "  pulls API rc=$rc"; sed 's/^/    /' "$OUTP.api_heads.out"
[ "$rc" -eq 0 ] || { echo "REFUSING: the PULLS API read failed"; exit 3; }
grep -q '^OVERLAP ' "$OUTP.api_heads.out" && { echo "REFUSING TO LAUNCH: another open PR touches the path this PR changes — Wednesday sequences the two baseline edits; a re-draft decides"; exit 15; }
grep -q '^CENSUS ' "$OUTP.api_heads.out" || { echo "REFUSING: the census did not complete"; exit 3; }
echo "  OVERLAP census clean"

echo "--- 3. the head, judged (both instruments == the pin, open, not mergeable:false, based on develop)"
PH="$(awk -v r="refs/pull/$N/head" '$2==r{print $1}' "$OUTP.lsremote.out")"; BH="$(awk -v r="$BR" '$2==r{print $1}' "$OUTP.lsremote.out")"
A="$(awk '$1=="API"{print $4}' "$OUTP.api_heads.out")"; B="$(awk '$1=="API"{print $6}' "$OUTP.api_heads.out")"; M="$(awk '$1=="API"{print $8}' "$OUTP.api_heads.out")"; S="$(awk '$1=="API"{print $NF}' "$OUTP.api_heads.out")"
echo "  #$N  ls-remote pull/head ${PH:-ABSENT} | branch ${BH:-ABSENT} | API ${A:-ABSENT} (base ${B:-?}, state ${S:-?}, mergeable ${M:-?}) | pinned $H"
[ "$PH" = "$H" ] && [ "$BH" = "$H" ] && [ "$A" = "$H" ] && [ "$S" = "open" ] && [ "$B" = "develop" ] && [ "$M" != "False" ] || { echo "REFUSING TO LAUNCH: the head moved (the pin is stale), the PR is not open / not on develop, or GitHub reports mergeable:false — a new head needs pin_gate42b.py, capture_mail_gate42b.py and fill_gate42b.py first"; exit 11; }
[ "$M" = "None" ] && echo "  NOTE: GitHub has not computed mergeable after 3 reads — the kit's own merge-tree (pins_gate42b.json) is the clean-merge proof"
echo "  BOTH INSTRUMENTS AGREE with the pin."

echo "--- 3b. develop, read at launch: $CUR_DEV | the pinned develop $DEV"
if [ "$CUR_DEV" != "$DEV" ]; then
  if [ "$DRY" = 1 ]; then echo "  DRY RUN: develop MOVED since the fill — the real run RE-PINS here (pin -> fill) in the same action"; exit 10; fi
  echo "  develop MOVED — RE-PIN IN THIS ACTION over $CUR_DEV (scratch clone under $SP/g42b_sp)"
  python3 "$GS/pin_gate42b.py" "$SP" --expect-head "$H" > "$OUTP.repin_pin.out" 2>&1; rc=$?; echo "  pin rc=$rc -> $OUTP.repin_pin.out"; tail -3 "$OUTP.repin_pin.out" | sed 's/^/    /'
  [ "$rc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the re-pin over the moved develop refused (a move that touches the baseline is re-drafted, never here)"; exit 10; }
  python3 "$GS/fill_gate42b.py" > "$OUTP.repin_fill.out" 2>&1; rc=$?; echo "  fill rc=$rc"; tail -1 "$OUTP.repin_fill.out" | sed 's/^/    /'
  [ "$rc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the re-fill refused"; exit 10; }
  DEV="$(pin DEVELOP_SHA)"; ET="$(pin END_TREE)"
  AGAIN="$(git -C "$CHECKOUT" ls-remote origin refs/heads/develop | cut -f1)"
  echo "  re-pinned: develop $DEV | END_TREE $ET | develop re-read now $AGAIN"
  [ "$AGAIN" = "$DEV" ] || { echo "REFUSING TO LAUNCH: develop moved AGAIN during the re-pin ($DEV -> $AGAIN) — run this script again"; exit 10; }
else
  echo "  UNMOVED since the fill — the END_TREE $ET stands"
fi

echo "--- 3c. the fuse: $FUSE"
LEFT="$(python3 -c 'import datetime,sys; f=datetime.datetime.fromisoformat(sys.argv[1].replace("Z","+00:00")); print(int((f-datetime.datetime.now(datetime.timezone.utc)).total_seconds()//60))' "$FUSE")"
if [ "$LEFT" -gt 0 ]; then echo "  $LEFT minute(s) to the fuse — #$N must merge before it"; else echo "  WARNING: the fuse is PAST ($LEFT min) — the BASE legs are red by design now; the gate time-stamps every leg (not a refusal)"; fi
[ -n "${G42B_STOP_AFTER_3B:-}" ] && { echo "STOPPED AFTER 3c (G42B_STOP_AFTER_3B — a controls-only switch) — develop $DEV | END_TREE $ET"; exit 0; }
if [ "$DRY" = 1 ]; then echo "DRY RUN COMPLETE $(date -u '+%Y-%m-%dT%H:%M:%SZ') — every read agrees with the pins; the real run continues with the override check, the usage gate, --check and cockpit.sh add"; exit 0; fi

echo "--- 4. no test override on a real launch"
[ "$(env | grep -c '^G42B_')" = 0 ] || { echo "REFUSING TO LAUNCH: a G42B_* test override is set"; exit 16; }

echo "--- 5. usage gate"
/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/usage_gate.sh --check > "$OUTP.usage_gate.out" 2>&1
rc=$?
echo "  usage_gate rc=$rc"; sed 's/^/    /' "$OUTP.usage_gate.out"
[ "$rc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the usage gate refused (pass WED_USAGE_STOP only with Kam's recorded authority for this lane)"; exit 12; }

echo "--- 6. the launcher's own --check"
"$L" --check > "$OUTP.launcher_check.out" 2>&1
rc=$?
echo "  launcher --check rc=$rc"; sed 's/^/    /' "$OUTP.launcher_check.out"
[ "$rc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the launcher refused under --check"; exit 13; }

echo "--- 7. launch through the fleet's own tooling (cockpit.sh add), never raw tmux send-keys"
/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/cockpit/cockpit.sh add "$PANE" "$L" > "$OUTP.cockpit_add.out" 2>&1
rc=$?
echo "  cockpit.sh add rc=$rc"; sed 's/^/    /' "$OUTP.cockpit_add.out"
[ "$rc" -eq 0 ] || { echo "LAUNCH FAILED at cockpit.sh add"; exit 14; }
echo "--- pane census"
/opt/homebrew/bin/tmux list-panes -a -F '#{pane_id} | #{@cockpit_name} | #{pane_current_command} | #{session_name}:#{window_index}.#{pane_index}'
echo "LAUNCHED $(date -u '+%Y-%m-%dT%H:%M:%SZ') over develop $DEV (END_TREE $ET)"
