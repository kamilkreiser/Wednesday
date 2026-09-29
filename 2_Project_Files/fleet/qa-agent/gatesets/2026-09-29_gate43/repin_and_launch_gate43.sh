#!/bin/bash
# repin_and_launch_gate43.sh — the LAUNCH ACTION for the gate43 kit (the directory this script lives in; kit.json beside it names the kit, its pane
# and its five PRs). Re-pin and launch are ONE action (Kam 2026-09-18). It READS develop, every head and `mergeable` AT LAUNCH and never trusts a
# pin it did not just re-read:
#   (0)  the pane is routed (inbox_routing.conf) — rc 1;
#   (0b) the kit is at the home it was filled for; if MOVED, re-measure + re-fill HERE (pin, testrefs, fill) — rc 8;
#   (1)  origin develop + refs/pull/<n>/head + each branch, by ONE `git ls-remote` READ from the Secuura checkout — rc 2;
#   (2)  every head re-read from the GitHub PULLS API (a second instrument; `mergeable` re-read up to 3x while null) — rc 3;
#   (2b) the OVERLAP / WIDEN census over every OTHER open PR's file list (PULLS API /files): rc 15 if any touches one of the kit's 11 paths, or is
#        titled with a kit key; a `-b43-`/`-b44-`/`-b45-` PR outside the kit that is path-disjoint is REPORTED (DISJOINT OUT-OF-KIT), never refused;
#   (3)  rc 11 unless every head == the launcher's pin on BOTH instruments (WHOLE-FIELD), each PR is open, not `mergeable: false`, based on develop;
#   (3b) develop: if origin develop != the pinned develop, RE-PIN IN THIS ACTION (pin_gate43.py --expect-head n=<pin> x5: refuses if the move
#        reaches any PR's own paths or any chain step is unclean; then testrefs_gate43.py and fill_gate43.py), then ls-remote develop once more — rc 10;
#   (4)  G43_* overrides refuse a real launch — rc 16;  (5) the usage gate — rc 12;  (6) the launcher's own --check — rc 13;
#   (7)  cockpit.sh add — rc 14, then a pane census.
# --dry-run: steps 0-3b (no re-fill, no re-pin, no write outside the scratchpad), then stop before (4); the routing line's absence is REPORTED, not
# refused; a moved develop is reported and exits 10. READ-ONLY in the Secuura checkout: ls-remote only. Nothing is merged, deployed or commented.
# Controls-only overrides: G43_ROUTING (routing file), G43_OVERLAP_EXTRA (an extra path the census treats as a kit path), G43_TITLE_KEY (an extra
# title key for the census), G43_WIDEN_RX (a branch regex standing in for the seat-branch rule, to make the DISJOINT line print), G43_STOP_AFTER_3B (a real run stops after 3b).
# Shape copied from gate42b's repin, widened to FIVE PRs (the gate42 WIDEN census cut to the path-overlap rule of kit.json widen_note).
# Usage: repin_and_launch_gate43.sh <launcher path> <a scratchpad dir under /private/tmp/claude-501/> [--dry-run]
set -u
GS="$(dirname "$(/bin/realpath "$0")")"
CHECKOUT='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
ROUTING="${G43_ROUTING:-/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf}"
KJ() { python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))[sys.argv[2]])' "$GS/kit.json" "$1"; }
KIT="$(KJ kit)"; PANE="$(KJ pane)"; ORDER="$(python3 -c 'import json,sys; print(" ".join(json.load(open(sys.argv[1]))["order"]))' "$GS/kit.json")"
L="${1:-}"; SP="${2:-}"; DRY=0; [ "${3:-}" = "--dry-run" ] && DRY=1
[ -n "$L" ] && [ -x "$L" ] || { echo "usage: repin_and_launch_$KIT.sh <launcher path> <scratchpad dir> [--dry-run] — e.g. $GS/$(KJ launcher)"; exit 9; }
case "$SP" in /private/tmp/claude-501/*/scratchpad*) [ -d "$SP" ] || { echo "REFUSING: no such scratchpad dir $SP"; exit 9; } ;; *) echo "REFUSING: argv[2] must be a Claude session scratchpad under /private/tmp/claude-501/"; exit 9;; esac
T="$(date -u +%H%M%S)"; OUTP="$GS/launch_$T"; [ "$DRY" = 1 ] && OUTP="$SP/repin_${KIT}_dry_$T"
pin() { sed -n "s/^$1='\([0-9a-f]\{40\}\)'$/\1/p" "$L"; }
rowf() { sed -n "s/^  \"$1|[^|]*|\([^|]*\)|\([0-9a-f]\{40\}\)|.*\"$/\1 \2/p" "$L"; }
LGS="$(sed -n "s/^GS='\(.*\)'$/\1/p" "$L")"
DEV="$(pin DEVELOP_SHA)"; ET="$(pin END_TREE)"
[ -n "$DEV" ] && [ -n "$ET" ] && [ -n "$LGS" ] || { echo "REFUSING: could not read the pins (GS / DEVELOP_SHA / END_TREE) from $L"; exit 9; }
REFS="refs/heads/develop"; EXPARGS=""
for n in $ORDER; do
  r="$(rowf "$n")"; [ -n "$r" ] || { echo "REFUSING: could not read the #$n row from $L"; exit 9; }
  eval "BR_$n='${r% *}'; H_$n='${r#* }'"; REFS="$REFS ${r% *} refs/pull/$n/head"; EXPARGS="$EXPARGS --expect-head $n=${r#* }"
done
echo "LAUNCH ACTION $KIT$([ "$DRY" = 1 ] && echo ' (DRY RUN)') $(date '+%Y-%m-%d %H:%M:%S %Z') / $(date -u '+%Y-%m-%dT%H:%M:%SZ') | launcher $L | pinned develop $DEV | END_TREE $ET"
for n in $ORDER; do eval "echo \"  pin #$n \$H_$n (\$BR_$n)\""; done

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
    python3 "$GS/pin_gate43.py" "$SP" $EXPARGS > "$OUTP.refill_pin.out" 2>&1 && python3 "$GS/testrefs_gate43.py" "$SP" > "$GS/testrefs_1.out" 2>&1 && python3 "$GS/fill_gate43.py" > "$OUTP.refill.out" 2>&1 || { echo "REFUSING TO LAUNCH: re-pin / testrefs / re-fill at the new home refused (read $OUTP.refill_pin.out / $OUTP.refill.out)"; exit 8; }
    LGS="$(sed -n "s/^GS='\(.*\)'$/\1/p" "$L")"; [ "$LGS" = "$GS" ] || { echo "REFUSING: the re-filled launcher still names $LGS"; exit 8; }
    DEV="$(pin DEVELOP_SHA)"; ET="$(pin END_TREE)"; echo "  re-filled: develop $DEV | END_TREE $ET"
  fi
else echo "  AT HOME — no re-fill"; fi

echo "--- 1. instrument: git ls-remote origin (ONE read from the Secuura checkout, READ-ONLY)"
git -C "$CHECKOUT" ls-remote origin $REFS > "$OUTP.lsremote.out" 2>&1
rc=$?
echo "  ls-remote rc=$rc at $(date -u +%H:%M:%SZ)"; sed 's/^/    /' "$OUTP.lsremote.out"
[ "$rc" -eq 0 ] || { echo "REFUSING: ls-remote failed"; exit 2; }
CUR_DEV="$(awk '$2=="refs/heads/develop"{print $1}' "$OUTP.lsremote.out")"

echo "--- 2. instrument: the GitHub PULLS API (an independent read of each head, and mergeable) + 2b the OVERLAP / WIDEN census"
GS="$GS" EXTRA="${G43_OVERLAP_EXTRA:-}" TKEY="${G43_TITLE_KEY:-}" WRX="${G43_WIDEN_RX:-}" python3 - > "$OUTP.api_heads.out" 2>&1 <<'PY'
import json, os, re, time, urllib.request, urllib.error
K = json.load(open(os.path.join(os.environ['GS'], 'kit.json'), encoding='utf-8'))
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
kit = set(K['order']); paths = set(p for n in K['order'] for p in K['prs'][n]['files'])
if os.environ.get('EXTRA'): paths.add(os.environ['EXTRA'])
keys = set(k for n in K['order'] for k in K['prs'][n]['keys'])
if os.environ.get('TKEY'): keys.add(os.environ['TKEY'])
for n in K['order']:
    p = get('pulls/' + n); tries = 1
    while p.get('mergeable') is None and tries < 3:
        time.sleep(10); p = get('pulls/' + n); tries += 1
    print('API #%s head %s base %s mergeable %s reads %d state %s' % (n, p['head']['sha'], p['base']['ref'], p.get('mergeable'), tries, p['state']))
opened = get('pulls?state=open&per_page=100'); hits = 0; wide = 0; others = 0
for x in opened:
    if str(x['number']) in kit: continue
    others += 1
    fs = set(f['filename'] for f in get('pulls/%s/files?per_page=100' % x['number']))
    ov = sorted(fs & paths); tk = sorted(set(re.findall(r'KS-\d+', x['title'])) & keys); wb = bool(re.search(os.environ.get('WRX') or K['widen_branch_rx'], x['head']['ref']))
    if ov or tk: hits += 1; print('OVERLAP #%s %s | %s | paths %s | title keys %s' % (x['number'], x['head']['ref'][:70], x['title'][:90], ov, tk))
    elif wb: wide += 1; print('DISJOINT OUT-OF-KIT #%s %s | %s | %d file(s), none a kit path' % (x['number'], x['head']['ref'][:70], x['title'][:90], len(fs)))
print('CENSUS %d other open PR(s) read | %d touch a kit path or carry a kit key | %d seat-branch PR(s) disjoint | %d kit path(s), %d kit key(s)' % (others, hits, wide, len(paths), len(keys)))
PY
rc=$?
echo "  pulls API rc=$rc"; sed 's/^/    /' "$OUTP.api_heads.out"
[ "$rc" -eq 0 ] || { echo "REFUSING: the PULLS API read failed"; exit 3; }
grep -q '^OVERLAP ' "$OUTP.api_heads.out" && { echo "REFUSING TO LAUNCH: another open PR touches a kit path or carries a kit key — Wednesday sequences it; a re-draft decides"; exit 15; }
grep -q '^CENSUS ' "$OUTP.api_heads.out" || { echo "REFUSING: the census did not complete"; exit 3; }
echo "  OVERLAP census clean"

echo "--- 3. the heads, judged (both instruments == the pin, open, not mergeable:false, based on develop)"
BADH=0
for n in $ORDER; do
  eval "H=\$H_$n; BR=\$BR_$n"
  PH="$(awk -v r="refs/pull/$n/head" '$2==r{print $1}' "$OUTP.lsremote.out")"; BH="$(awk -v r="$BR" '$2==r{print $1}' "$OUTP.lsremote.out")"
  A="$(awk -v n="#$n" '$1=="API" && $2==n{print $4}' "$OUTP.api_heads.out")"; B="$(awk -v n="#$n" '$1=="API" && $2==n{print $6}' "$OUTP.api_heads.out")"
  M="$(awk -v n="#$n" '$1=="API" && $2==n{print $8}' "$OUTP.api_heads.out")"; S="$(awk -v n="#$n" '$1=="API" && $2==n{print $NF}' "$OUTP.api_heads.out")"
  echo "  #$n  ls-remote pull/head ${PH:-ABSENT} | branch ${BH:-ABSENT} | API ${A:-ABSENT} (base ${B:-?}, state ${S:-?}, mergeable ${M:-?}) | pinned $H"
  if [ "$PH" = "$H" ] && [ "$BH" = "$H" ] && [ "$A" = "$H" ] && [ "$S" = "open" ] && [ "$B" = "develop" ] && [ "$M" != "False" ]; then :; else BADH=1; echo "    ^ DISAGREES"; fi
  [ "$M" = "None" ] && echo "    NOTE: GitHub has not computed mergeable after 3 reads — the kit's own merge-tree chain (pins_gate43.json) is the clean-merge proof"
done
[ "$BADH" = 0 ] || { echo "REFUSING TO LAUNCH: a head moved (the pin is stale), a PR is not open / not on develop, or GitHub reports mergeable:false — a new head needs pin_gate43.py, capture_mail_gate43.py, testrefs_gate43.py and fill_gate43.py first"; exit 11; }
echo "  BOTH INSTRUMENTS AGREE with the pin, 5 of 5."

echo "--- 3b. develop, read at launch: $CUR_DEV | the pinned develop $DEV"
if [ "$CUR_DEV" != "$DEV" ]; then
  if [ "$DRY" = 1 ]; then echo "  DRY RUN: develop MOVED since the fill — the real run RE-PINS here (pin -> testrefs -> fill) in the same action"; exit 10; fi
  echo "  develop MOVED — RE-PIN IN THIS ACTION over $CUR_DEV (scratch clone under $SP/g43_sp)"
  python3 "$GS/pin_gate43.py" "$SP" $EXPARGS > "$OUTP.repin_pin.out" 2>&1; rc=$?; echo "  pin rc=$rc -> $OUTP.repin_pin.out"; tail -3 "$OUTP.repin_pin.out" | sed 's/^/    /'
  [ "$rc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the re-pin over the moved develop refused (a move that reaches a PR's paths, or an unclean chain step, is re-drafted, never here)"; exit 10; }
  python3 "$GS/testrefs_gate43.py" "$SP" > "$GS/testrefs_1.out" 2>&1; rc=$?; echo "  testrefs rc=$rc"; tail -1 "$GS/testrefs_1.out" | sed 's/^/    /'
  [ "$rc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the test census at the new END refused"; exit 10; }
  python3 "$GS/fill_gate43.py" > "$OUTP.repin_fill.out" 2>&1; rc=$?; echo "  fill rc=$rc"; tail -1 "$OUTP.repin_fill.out" | sed 's/^/    /'
  [ "$rc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the re-fill refused"; exit 10; }
  DEV="$(pin DEVELOP_SHA)"; ET="$(pin END_TREE)"
  AGAIN="$(git -C "$CHECKOUT" ls-remote origin refs/heads/develop | cut -f1)"
  echo "  re-pinned: develop $DEV | END_TREE $ET | develop re-read now $AGAIN"
  [ "$AGAIN" = "$DEV" ] || { echo "REFUSING TO LAUNCH: develop moved AGAIN during the re-pin ($DEV -> $AGAIN) — run this script again"; exit 10; }
else
  echo "  UNMOVED since the fill — the END_TREE $ET stands"
fi
[ -n "${G43_STOP_AFTER_3B:-}" ] && { echo "STOPPED AFTER 3b (G43_STOP_AFTER_3B — a controls-only switch) — develop $DEV | END_TREE $ET"; exit 0; }
if [ "$DRY" = 1 ]; then echo "DRY RUN COMPLETE $(date -u '+%Y-%m-%dT%H:%M:%SZ') — every read agrees with the pins; the real run continues with the override check, the usage gate, --check and cockpit.sh add"; exit 0; fi

echo "--- 4. no test override on a real launch"
[ "$(env | grep -c '^G43_')" = 0 ] || { echo "REFUSING TO LAUNCH: a G43_* test override is set"; exit 16; }

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
