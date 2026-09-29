#!/bin/bash
# repin_and_launch_<kit>.sh — the LAUNCH ACTION for the gate42 kit (the directory this script lives in; kit.json beside it names the kit, its pane and
# its PRs). The re-pin and the launch are ONE action (Kam 2026-09-18: a stale pin costs a whole gate session). It READS develop, the heads and
# `mergeable` AT LAUNCH and never trusts a pin it did not just re-read:
#   (0)  the pane is routed (inbox_routing.conf) — rc 1;
#   (0b) the kit is at the home it was filled for; if it was MOVED (copied into gatesets/), re-measure + re-fill HERE in the same action
#        (predict_gate42.py then fill_gate42.py; both re-read origin and refuse on any disagreement) — rc 8;
#   (1)  origin develop + refs/pull/<n>/head + each branch, by `git ls-remote` READ from the Secuura checkout — rc 2;
#   (2)  each head re-read from the GitHub PULLS API (a second, independent instrument; also `mergeable`, re-read up to 3x while GitHub reports null) — rc 3;
#   (2b) the WIDEN census (kit.json `widen_rx` on TITLES and `widen_branch_rx` on BRANCHES — Seat B 43rd's `-b43-<n>` and Seat B 44th's `-b44-<n>` —
#        read by the PULLS API list of open PRs): rc 15 if an open PR matching either is NOT in this kit (gate42 has no sibling) — Wednesday's widen rule:
#        such a PR must be added to the kit (with its own cells) by a re-draft, never silently left out — EXCEPT the ONE measured class of kit.json
#        `widen_disjoint_rule` (Wednesday's gate42 commission, requirement 6): an open WIDEN PR whose ENTIRE file list (PULLS API /files) is exactly
#        the audit baseline file is Seat B 44th's separate re-date PR (merges AFTER #1339): printed DISJOINT-OUT-OF-KIT and not refused;
#   (3)  rc 11 unless every head == the launcher's pin on BOTH instruments (WHOLE-FIELD equality) AND each PR is open AND not `mergeable: false` AND
#        every STACKED child's API base is still its parent's branch at the parent's pinned head (kit.json `stacks`; a retargeted child = a new shape). A
#        STALE HEAD REFUSES: a new head needs a re-capture and a re-draft; this script never adopts a head it was not given. `mergeable: null` after the
#        retries is REPORTED and not refused: the kit's own merge-tree over the develop it launches on (the pins) proves the clean merge;
#   (3b) develop: if origin develop != the launcher's pinned develop — the merge seat merges on GOs, and any other batch (e.g. another seat's squash) may land first —
#        RE-PIN IN THIS SAME ACTION: predict_gate42.py over the develop just read (a scratch clone under <scratchpad>/g42_sp; it REFUSES on an overlap
#        of the move with a PR's own paths, an unclean merge, a numstat difference, an UNDECLARED stacked pair, a pairwise overlap with the kit or
#        every other open PR, a no-op or overlap declaration it cannot prove, or an END-tree disagreement), then fill_gate42.py — then ls-remote develop ONCE MORE: rc 10 unless it still
#        equals the new pin;
#   (4)  the usage gate — rc 12;  (5) the launcher's own --check — rc 13;  (6) cockpit.sh add — rc 14, then a pane census.
# --dry-run: steps 0-3 and a REPORT of 0b/3b (no re-fill, no re-pin, no write outside the scratchpad), then stop before (4); the routing line's
# absence is reported, not refused; a moved develop is reported and exits 10. READ-ONLY in the Secuura checkout: ls-remote only. Nothing is merged,
# deployed or commented; no container is started. The pins are READ from the launcher itself. G42_ROUTING: a routing-file override for the controls only.
# G42_WIDEN_RX: a WIDEN-regex override (titles; G42_WIDEN_BRANCH_RX the same for branches; G42_BASELINE_ONLY_PATH a stand-in for the widen_disjoint_rule
# path) for the controls only (a real launch refuses when any is set).
# G42_STOP_AFTER_3B: controls only — a REAL run (not --dry-run) stops right after step 3b, so a control can exercise the real re-pin and nothing after it.
# Shape copied from gate41's repin (gate40 -> gate39 -> gate38 lineage), re-keyed to gate42's ONE row (#1339 round 2, Seat B 44th); the STACK check in
# steps 2/3 stays (kit.json `stacks` is EMPTY for gate42, so every PR must read DEVBASE OK); the widen census also reads branches (-b43-<n> / -b44-<n>: six
# are HELD unpushed — any opened as a PR before launch refuses rc 15; the baseline-only re-date PR is the one measured exception); no port step (no DB).
# Usage: repin_and_launch_<kit>.sh <launcher path> <a scratchpad dir under /private/tmp/claude-501/> [--dry-run]
set -u
GS="$(dirname "$(/bin/realpath "$0")")"
CHECKOUT='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
ROUTING="${G42_ROUTING:-/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf}"
KIT="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["kit"])' "$GS/kit.json")"
PANE="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["pane"])' "$GS/kit.json")"
NS="$(python3 -c 'import json,sys; print(" ".join(sorted(json.load(open(sys.argv[1]))["prs"])))' "$GS/kit.json")"
L="${1:-}"; SP="${2:-}"; DRY=0; [ "${3:-}" = "--dry-run" ] && DRY=1
[ -n "$L" ] && [ -x "$L" ] || { echo "usage: repin_and_launch_$KIT.sh <launcher path> <scratchpad dir> [--dry-run] — e.g. $GS/$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["launcher"])' "$GS/kit.json")"; exit 9; }
case "$SP" in /private/tmp/claude-501/*/scratchpad*) [ -d "$SP" ] || { echo "REFUSING: no such scratchpad dir $SP"; exit 9; } ;; *) echo "REFUSING: argv[2] must be a Claude session scratchpad under /private/tmp/claude-501/"; exit 9;; esac
T="$(date -u +%H%M%S)"; OUTP="$GS/launch_$T"; [ "$DRY" = 1 ] && OUTP="$SP/repin_${KIT}_dry_$T"
pin() { sed -n "s/^$1='\([0-9a-f]\{40\}\)'$/\1/p" "$L"; }
row() { sed -n "s/^  \"$1|[^|]*|\([^|]*\)|\([0-9a-f]\{40\}\)|[0-9]*|[0-9]*|[0-9a-f]*|[0-9]*|[^|\"]*|T[0-9]\"$/\\$2/p" "$L"; }
LGS="$(sed -n "s/^GS='\(.*\)'$/\1/p" "$L")"
DEV="$(pin DEVELOP_SHA)"; ET="$(pin END_TREE)"
[ -n "$DEV" ] && [ -n "$ET" ] && [ -n "$LGS" ] || { echo "REFUSING: could not read the pins (GS / DEVELOP_SHA / END_TREE) from $L"; exit 9; }
for n in $NS; do [ -n "$(row $n 2)" ] && [ -n "$(row $n 1)" ] || { echo "REFUSING: could not read #$n's row (branch|head) from $L"; exit 9; }; done
echo "LAUNCH ACTION $KIT$([ "$DRY" = 1 ] && echo ' (DRY RUN)') $(date '+%Y-%m-%d %H:%M:%S %Z') / $(date -u '+%Y-%m-%dT%H:%M:%SZ') | launcher $L | pinned launch develop $DEV | END_TREE $ET"
for n in $NS; do echo "  pin #$n $(row $n 2)"; done

echo "--- 0. the pane must be routed (inbox_routing.conf) or cockpit.sh say --mail fails silently"
/usr/bin/grep -c -x -F "$PANE|coagent@agentmail.to|yes" "$ROUTING" > "$OUTP.routing.out" 2>&1
rc=$?
echo "  routing file $ROUTING — line present: $(cat "$OUTP.routing.out") (grep rc=$rc; want 1 / rc 0)"
if [ "$rc" -ne 0 ]; then
  [ "$DRY" = 1 ] && echo "  (DRY RUN: reported, not refused — the real run refuses rc 1 here)" || { echo "REFUSING: $PANE is not registered in inbox_routing.conf — add the line first (README.md section 4; the drafter did NOT write it)"; exit 1; }
fi

echo "--- 0b. the kit's home: launcher filled for $LGS | this script lives in $GS"
if [ "$LGS" != "$GS" ] || [ "$(dirname "$(/bin/realpath "$L")")" != "$GS" ]; then
  if [ "$DRY" = 1 ]; then echo "  DRY RUN: MOVED KIT — the real run re-measures + re-fills here (predict_gate42.py, fill_gate42.py) in the same action"; else
    [ "$(dirname "$(/bin/realpath "$L")")" = "$GS" ] || { echo "REFUSING: the launcher $L is not in this kit's directory $GS"; exit 8; }
    python3 "$GS/predict_gate42.py" "$SP" > "$OUTP.refill_predict.out" 2>&1; rc=$?; echo "  re-measure at $GS rc=$rc -> $OUTP.refill_predict.out"; tail -2 "$OUTP.refill_predict.out" | sed 's/^/    /'
    [ "$rc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the re-measurement at the new home refused (read $OUTP.refill_predict.out)"; exit 8; }
    python3 "$GS/fill_gate42.py" "$SP" > "$OUTP.refill.out" 2>&1; rc=$?; echo "  re-fill at $GS rc=$rc -> $OUTP.refill.out"; tail -2 "$OUTP.refill.out" | sed 's/^/    /'
    [ "$rc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the re-fill at the new home refused (read $OUTP.refill.out)"; exit 8; }
    LGS="$(sed -n "s/^GS='\(.*\)'$/\1/p" "$L")"; [ "$LGS" = "$GS" ] || { echo "REFUSING: the re-filled launcher still names $LGS"; exit 8; }
    DEV="$(pin DEVELOP_SHA)"; ET="$(pin END_TREE)"; echo "  re-filled: launch develop $DEV | END_TREE $ET"
  fi
else echo "  AT HOME — no re-fill"; fi

echo "--- 1. instrument: git ls-remote origin (read from the Secuura checkout, READ-ONLY)"
LSREFS=(refs/heads/develop)
for n in $NS; do LSREFS+=("refs/pull/$n/head" "$(row $n 1)"); done
git -C "$CHECKOUT" ls-remote origin "${LSREFS[@]}" > "$OUTP.lsremote.out" 2>&1
rc=$?
echo "  ls-remote rc=$rc at $(date -u +%H:%M:%SZ)"; sed 's/^/    /' "$OUTP.lsremote.out"
[ "$rc" -eq 0 ] || { echo "REFUSING: ls-remote failed"; exit 2; }
CUR_DEV="$(awk '$2=="refs/heads/develop"{print $1}' "$OUTP.lsremote.out")"

echo "--- 2. instrument: the GitHub PULLS API (an independent read of each head, and mergeable)"
NS="$NS" KITJSON="$GS/kit.json" WRX_OVR="${G42_WIDEN_RX:-}" WBX_OVR="${G42_WIDEN_BRANCH_RX:-}" BO_OVR="${G42_BASELINE_ONLY_PATH:-}" python3 - > "$OUTP.api_heads.out" 2>&1 <<'PY'
import json, os, time, urllib.request, urllib.error
tok = ''
for l in open('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env', encoding='utf-8'):
    if l.startswith('GH_TOKEN='): tok = l.split('=', 1)[1].strip().strip('"').strip("'")
assert tok, 'GH_TOKEN unset'
def get(n):
    for i in range(4):
        try: return json.load(urllib.request.urlopen(urllib.request.Request('https://api.github.com/repos/Secuura/Distributed_Secuura/pulls/' + n, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'}), timeout=60))
        except urllib.error.HTTPError as e:
            if e.code < 500 or i == 3: raise
            time.sleep(10)
import re
k = json.load(open(os.environ['KITJSON'], encoding='utf-8'))
rx = os.environ.get('WRX_OVR') or k.get('widen_rx', r'(?!x)x'); bx = os.environ.get('WBX_OVR') or k.get('widen_branch_rx', r'(?!x)x'); known = set(k['this_batch']) | set(k['sibling_batch'])
req = urllib.request.Request('https://api.github.com/repos/Secuura/Distributed_Secuura/pulls?state=open&per_page=100', headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'})
bo = os.environ.get('BO_OVR') or k.get('widen_disjoint_rule', {}).get('baseline_only_path', '')
def files(num):
    r = urllib.request.Request('https://api.github.com/repos/Secuura/Distributed_Secuura/pulls/%s/files?per_page=100' % num, headers={'Authorization': 'Bearer ' + tok, 'Accept': 'application/vnd.github+json'})
    return sorted(f['filename'] for f in json.load(urllib.request.urlopen(r, timeout=60)))
for x in json.load(urllib.request.urlopen(req, timeout=60)):
    if re.match(rx, x['title']) or re.search(bx, x['head']['ref']):
        cls = 'IN-KIT' if str(x['number']) in known else ('DISJOINT-OUT-OF-KIT' if bo and files(x['number']) == [bo] else 'OUTSIDE')
        print('WIDEN #%s %s %s | %s | %s%s' % (x['number'], cls, x['head']['sha'], x['head']['ref'][:70], x['title'][:100], (' | touches ONLY %s (kit.json widen_disjoint_rule: the separate audit-baseline re-date PR, merges AFTER #1339)' % bo) if cls == 'DISJOINT-OUT-OF-KIT' else ''))
print('WIDEN-RX %s | WIDEN-BRANCH-RX %s | BASELINE-ONLY-PATH %s' % (rx, bx, bo or 'NONE'))
PP = {}
for n in os.environ['NS'].split():
    p = get(n); tries = 1
    while p.get('mergeable') is None and tries < 3:
        time.sleep(10); p = get(n); tries += 1
    PP[n] = p
    print('API #%s head %s base %s mergeable %s reads %d state %s' % (n, p['head']['sha'], p['base']['ref'], p.get('mergeable'), tries, p['state']))
for c, par in sorted(k.get('stacks', {}).items()):
    ok = PP[c]['base']['ref'] == PP[par]['head']['ref'] and PP[c]['base']['sha'] == PP[par]['head']['sha']
    print('STACKBASE #%s %s base.ref %s base.sha %s | #%s branch %s head %s' % (c, 'OK' if ok else 'MOVED', PP[c]['base']['ref'], PP[c]['base']['sha'], par, PP[par]['head']['ref'], PP[par]['head']['sha']))
for n in os.environ['NS'].split():
    if n not in k.get('stacks', {}):
        print('DEVBASE #%s %s base.ref %s' % (n, 'OK' if PP[n]['base']['ref'] == 'develop' else 'MOVED', PP[n]['base']['ref']))
PY
rc=$?
echo "  pulls API rc=$rc"; sed 's/^/    /' "$OUTP.api_heads.out"
[ "$rc" -eq 0 ] || { echo "REFUSING: a pulls API read failed"; exit 3; }

echo "--- 2b. the WIDEN census (Wednesday's widen rule): an open PR matching kit.json widen_rx must be in this kit"
awk '$1=="WIDEN" || $1=="WIDEN-RX"' "$OUTP.api_heads.out" | sed 's/^/    /'
if awk '$1=="WIDEN" && $3=="OUTSIDE"' "$OUTP.api_heads.out" | grep -q .; then echo "REFUSING TO LAUNCH: a WIDEN PR exists outside this kit — re-draft to add it (with its own cells), never launch around it"; exit 15; fi
[ -z "${G42_WIDEN_RX:-}${G42_WIDEN_BRANCH_RX:-}${G42_BASELINE_ONLY_PATH:-}" ] || [ "$DRY" = 1 ] || [ -n "${G42_STOP_AFTER_3B:-}" ] || { echo "REFUSING: G42_WIDEN_RX / G42_WIDEN_BRANCH_RX / G42_BASELINE_ONLY_PATH are controls-only overrides"; exit 15; }
echo "  WIDEN census clean: every matching open PR is in this kit, or MEASURED baseline-only (DISJOINT-OUT-OF-KIT, never refused)"
echo "--- 3. the heads, judged (both instruments == the pin, open, not mergeable:false; every stacked child still based on its parent's branch at the pinned parent head; every other PR based on develop)"
bad=0
for n in $NS; do
  H="$(row $n 2)"; BR="$(row $n 1)"
  P="$(awk -v r="refs/pull/$n/head" '$2==r{print $1}' "$OUTP.lsremote.out")"
  B="$(awk -v r="$BR" '$2==r{print $1}' "$OUTP.lsremote.out")"
  A="$(awk -v n="#$n" '$1=="API" && $2==n{print $4}' "$OUTP.api_heads.out")"; S="$(awk -v n="#$n" '$1=="API" && $2==n{print $NF}' "$OUTP.api_heads.out")"
  M="$(awk -v n="#$n" '$1=="API" && $2==n{print $8}' "$OUTP.api_heads.out")"
  echo "  #$n  ls-remote pull/head ${P:-ABSENT} | branch ${B:-ABSENT} | API ${A:-ABSENT} (state ${S:-?}, mergeable ${M:-?}) | pinned $H"
  [ "$P" = "$H" ] && [ "$B" = "$H" ] && [ "$A" = "$H" ] && [ "$S" = "open" ] && [ "$M" != "False" ] || { echo "    STALE, CLOSED or NOT MERGEABLE: #$n"; bad=1; }
  [ "$M" = "None" ] && echo "    NOTE: GitHub has not computed mergeable for #$n after 3 reads — the kit's own merge-tree over the launch develop is the clean-merge proof (pins_$KIT.json)"
done
awk '$1=="STACKBASE" || $1=="DEVBASE"' "$OUTP.api_heads.out" | sed 's/^/  /'
awk '($1=="STACKBASE" || $1=="DEVBASE") && $3!="OK"' "$OUTP.api_heads.out" | grep -q . && { echo "    A BASE MOVED: a stacked child was retargeted (or a develop-based PR re-based) — the stack this kit measured no longer exists"; bad=1; }
[ "$(awk '$1=="STACKBASE"' "$OUTP.api_heads.out" | wc -l | tr -d ' ')" = "$(python3 -c 'import json,sys; print(len(json.load(open(sys.argv[1])).get("stacks", {})))' "$GS/kit.json")" ] || { echo "    a declared stack was not read"; bad=1; }
[ "$bad" = 0 ] || { echo "REFUSING TO LAUNCH: a head moved (the pin is stale), a PR is not open, GitHub reports mergeable:false, or a base moved — a verdict is valid only at its head and its stack; a new head needs gh_read_gate42.py, capture_mail_gate42.py, predict_gate42.py and fill_gate42.py first"; exit 11; }
echo "  BOTH INSTRUMENTS AGREE with every pin."

echo "--- 3b. develop, read at launch: $CUR_DEV | the launcher's pinned launch develop $DEV"
if [ "$CUR_DEV" != "$DEV" ]; then
  if [ "$DRY" = 1 ]; then echo "  DRY RUN: develop MOVED since the launcher was filled — the real run RE-PINS here (predict -> fill) in the same action"; exit 10; fi
  echo "  develop MOVED — RE-PIN IN THIS ACTION over $CUR_DEV (scratch clone under $SP/g42_sp)"
  python3 "$GS/predict_gate42.py" "$SP" > "$OUTP.repin_predict.out" 2>&1; rc=$?; echo "  predict rc=$rc -> $OUTP.repin_predict.out"; tail -3 "$OUTP.repin_predict.out" | sed 's/^/    /'
  [ "$rc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the re-measurement over the moved develop refused (read $OUTP.repin_predict.out — a move that touches a PR's OWN path is re-predicted BY HAND, never here)"; exit 10; }
  python3 "$GS/fill_gate42.py" "$SP" > "$OUTP.repin_fill.out" 2>&1; rc=$?; echo "  fill rc=$rc"; tail -1 "$OUTP.repin_fill.out" | sed 's/^/    /'
  [ "$rc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the re-fill refused"; exit 10; }
  DEV="$(pin DEVELOP_SHA)"; ET="$(pin END_TREE)"
  AGAIN="$(git -C "$CHECKOUT" ls-remote origin refs/heads/develop | cut -f1)"
  echo "  re-pinned: launch develop $DEV | END_TREE $ET | develop re-read now $AGAIN"
  [ "$AGAIN" = "$DEV" ] || { echo "REFUSING TO LAUNCH: develop moved AGAIN during the re-pin ($DEV -> $AGAIN) — run this script again"; exit 10; }
else
  echo "  UNMOVED since the fill — the END_TREE $ET stands"
fi
[ -n "${G42_STOP_AFTER_3B:-}" ] && { echo "STOPPED AFTER 3b (G42_STOP_AFTER_3B — a controls-only switch: the re-pin ran for real, nothing past it runs) — launch develop $DEV | END_TREE $ET"; exit 0; }
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
