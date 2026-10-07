#!/bin/bash
# repin_and_launch_gate74.sh — the LAUNCH ACTION for gate74 (T2 + preflight weight: #1423 KS-1164).
# NOT RUN BY THE DRAFTER except `--dry-run`. Carried from repin_and_launch_gate73.sh and re-keyed for ONE row by the gate74 drafter.
# EVERY PR-SPECIFIC CONSTANT IS A REQUIRED ARGUMENT, compared with kit.json (the drafter's pin) AND with what this script reads live:
#   (V)  --head-1423 --develop, present and full 40-hex — rc 9;  the head == kit.json, --develop == kit develop_at_draft — rc 11
#   (A)  the push mail (kit rows.1423.ready) names the head in full and #1423                                       — rc 18
#   (2)  ONE `git ls-remote` of develop + refs/pull/1423/head + the branch, from the Secuura checkout: GIT_SSH_COMMAND UNSET,
#        `-c core.sshCommand=<the checkout's own>`, the GitHub URL (a read verb); head == pull/head == branch       — rc 11 (MISMATCH)
#   (1)  gh_gate74.py api (rc 3 API failure; rc 11 not open / not develop / head differs) + census (REPORTED, not refused).
#        `--no-api` skips both ONLY with --dry-run.
#   (3b) origin develop == --develop -> on; MOVED -> rc 10 unless `--repin-develop <origin's 40-hex>` (stale re-pin rc 10)
#   (3c) THE KIT'S OWN CLONE (<kit>/_scratch/clone, gitignored; `clone --shared --no-checkout` of the checkout, origin = the GitHub URL,
#        the checkout's core.sshCommand, NEVER an exported GIT_SSH_COMMAND): fetch the head / develop / base / controls BY SHA only if
#        absent; any still absent refused BY NAME — rc 19. c1 with EVERY required pin must pass — rc 13. c4 `merged` on the develop read
#        NOW must print `MERGE-IN NEEDED: no` — rc 13 otherwise (a merge-in push is refused by leg 14 while KS-1450 is open: RE-DRAFT);
#        at the draft develop its tree must equal kit.json predicted_squash.tree — rc 13.
#   (S)  the Actions comparator is RULED (kit.json actions_comparator develop|base|union) — rc 8 (a dry run REPORTS it instead)
#   (R)  render prompt_gate74.txt -> prompt_gate74.rendered.txt + head_at_launch.txt (P / B / D / S / C)                — rc 9
#   (0)  the pane is routed in inbox_routing.conf — rc 1 (a dry run REPORTS it instead)
#   (4)  G74_* overrides refuse a real launch — rc 16;  (5) the usage gate — rc 12;  (6) the launcher's --check — rc 13;  (7) cockpit add — rc 14
# --dry-run: V, A, 2, 1 (or --no-api), 3b, 3c, S (reported), R, 0 (reported) and the launcher's --check, then stops. Outputs: launch_<HHMMSS>.*
# (dry: dry_<HHMMSS>.*) under <kit>/_scratch/runs/. Controls-only overrides (DRY RUN ONLY): G74_ROUTING, G74_LSFILE, G74_KITJSON, G74_CLONE
# (an existing clone OUTSIDE !CODING to use instead of <kit>/_scratch/clone — the drafter's dry runs used its own scratchpad clone).
# Usage (run under `script -q /dev/null`):
#   repin_and_launch_gate74.sh --head-1423 <40-hex> --develop <40-hex> [--dry-run [--no-api]] [--repin-develop <40-hex>]
set -u
export PYTHONDONTWRITEBYTECODE=1
GS="$(dirname "$(/bin/realpath "$0")")"
CHECKOUT='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
KITJSON="${G74_KITJSON:-$GS/kit.json}"
KJ() { python3 -c 'import json,sys; v=json.load(open(sys.argv[1]))
for k in sys.argv[2].split("."): v=v[int(k)] if isinstance(v,list) else v[k]
print(" ".join(map(str,v)) if isinstance(v,list) else ("" if v is None else v))' "$KITJSON" "$1"; }
ROUTING="${G74_ROUTING:-$(KJ routing)}"; PANE="$(KJ pane)"; LINE="$(KJ routing_line)"; URL="$(KJ github_url)"
L="$GS/$(KJ launcher)"; CL="${G74_CLONE:-$GS/_scratch/clone}"; ROW='1423'
USAGE="usage: repin_and_launch_gate74.sh --head-1423 <40-hex> --develop <40-hex> [--dry-run [--no-api]] [--repin-develop <40-hex>]"
H1423=""; DEV=""; DRY=0; NOAPI=0; REPIN=""
while [ $# -gt 0 ]; do
  case "$1" in
    --head-1423) H1423="${2:-}"; shift 2 2>/dev/null || shift;;
    --develop) DEV="${2:-}"; shift 2 2>/dev/null || shift;;       --repin-develop) REPIN="${2:-}"; shift 2 2>/dev/null || shift;;
    --dry-run) DRY=1; shift;; --no-api) NOAPI=1; shift;;
    *) echo "$USAGE"; exit 9;;
  esac
done
echo "--- V. required arguments, each well-formed and == the kit's pin (a wrong value refuses BY NAME)"
for _a in H1423 DEV; do eval "_v=\$$_a"; [ -n "$_v" ] || { echo "REFUSING: a REQUIRED argument is missing ($_a)"; echo "$USAGE"; exit 9; }; done
for _a in H1423 DEV; do eval "_v=\$$_a"; printf '%s' "$_v" | grep -qE '^[0-9a-f]{40}$' || { echo "REFUSING: $_a must be the FULL 40-hex sha, got '$_v'"; exit 9; }; done
[ -z "$REPIN" ] || printf '%s' "$REPIN" | grep -qE '^[0-9a-f]{40}$' || { echo "REFUSING: --repin-develop must be the FULL 40-hex sha, got '$REPIN'"; exit 9; }
[ "$NOAPI" = 0 ] || [ "$DRY" = 1 ] || { echo "REFUSING: --no-api is a dry-run option only (a real launch reads the PR API)"; exit 9; }
[ "$H1423" = "$(KJ rows.$ROW.head_expected)" ] || { echo "REFUSING: WRONG VALUE --head-1423 '$H1423' != kit.json $(KJ rows.$ROW.head_expected) — the kit's figures are for that head; re-draft"; exit 11; }
[ "$DEV" = "$(KJ develop_at_draft)" ] || { echo "REFUSING: WRONG VALUE --develop '$DEV' != kit.json develop_at_draft $(KJ develop_at_draft) (pass the draft develop; a moved develop is handled by --repin-develop)"; exit 11; }
echo "  head + develop present, well-formed and == kit.json"
[ -z "${G74_CLONE:-}" ] || [ "$DRY" = 1 ] || { echo "REFUSING: G74_CLONE is a dry-run control only"; exit 16; }
case "$(/bin/realpath "$CL" 2>/dev/null || echo "$CL")" in "/Volumes/DevMASTER/!CODING"*) echo "REFUSING: the kit clone $CL is under !CODING"; exit 16;; esac
mkdir -p "$GS/_scratch/runs"
T="$(date -u +%H%M%S)"; OUTP="$GS/_scratch/runs/launch_$T"; [ "$DRY" = 1 ] && OUTP="$GS/_scratch/runs/dry_$T"
echo "LAUNCH ACTION gate74$([ "$DRY" = 1 ] && echo ' (DRY RUN)') $(date '+%Y-%m-%d %H:%M:%S %Z') / $(date -u '+%Y-%m-%dT%H:%M:%SZ') | develop $DEV | repin-develop ${REPIN:-none} | pane $PANE | outputs $OUTP.*"

echo "--- A. the head must be the one the author's push mail names"
READY="$(KJ rows.$ROW.ready)"
[ -s "$READY" ] || { echo "REFUSING: push mail missing or empty ('$READY')"; exit 18; }
_n="$(/usr/bin/grep -c -F "$H1423" "$READY")"; _p="$(/usr/bin/grep -c -F "#$ROW" "$READY")"; _c="$(/usr/bin/grep -c -i 'pushed\|raised' "$READY")"
echo "  $(basename "$READY") (sha256/16 $(shasum -a 256 "$READY" | cut -c1-16)): lines naming the head in full $_n | naming #$ROW $_p | CONTROL lines naming 'pushed|raised' $_c"
[ "$_n" -ge 1 ] && [ "$_p" -ge 1 ] || { echo "REFUSING: the push mail does not name $H1423 in full (or #$ROW)"; exit 18; }

echo "--- 2. ONE ls-remote (read verb) from the checkout, GIT_SSH_COMMAND unset, the checkout's own core.sshCommand"
[ -z "${GIT_SSH_COMMAND:-}" ] || echo "  NOTE: GIT_SSH_COMMAND is exported in this shell; every git call below runs under env -u GIT_SSH_COMMAND"
BR="$(KJ rows.$ROW.branch)"; REFS="refs/heads/develop refs/pull/$ROW/head refs/heads/$BR"
if [ -n "${G74_LSFILE:-}" ]; then
  [ "$DRY" = 1 ] || { echo "REFUSING: G74_LSFILE is a dry-run control only"; exit 16; }
  cp "$G74_LSFILE" "$OUTP.lsremote.out"; : > "$OUTP.lsremote.err"; rc=0; echo "  (CONTROL: ls-remote output read from the stand-in $G74_LSFILE)"
else
  env -u GIT_SSH_COMMAND git -C "$CHECKOUT" -c core.sshCommand="$(git -C "$CHECKOUT" config --get core.sshCommand)" ls-remote "$URL" $REFS > "$OUTP.lsremote.out" 2> "$OUTP.lsremote.err"; rc=$?
fi
get() { awk -v r="$1" '$2==r{print $1}' "$OUTP.lsremote.out"; }
CUR_DEV="$(get refs/heads/develop)"
echo "  ls-remote rc=$rc at $(date -u +%H:%M:%SZ) | develop $CUR_DEV"
[ "$rc" -eq 0 ] && [ -n "$CUR_DEV" ] || { echo "REFUSING: ls-remote failed or returned no develop"; sed 's/^/    stderr: /' "$OUTP.lsremote.err"; exit 2; }
_p="$(get "refs/pull/$ROW/head")"; _b="$(get "refs/heads/$BR")"
echo "  #$ROW pull/head $_p | branch $_b"
[ "$_p" = "$H1423" ] && [ "$_b" = "$H1423" ] || { echo "REFUSING TO LAUNCH: #$ROW origin pull/head '$_p' / branch '$_b' != --head-1423 $H1423 — MISMATCH"; exit 11; }

echo "--- 1. PULLS API + census"
if [ "$NOAPI" = 1 ]; then echo "  SKIPPED BY NAME (--no-api, dry run only): the API state and the census are NOT read here"
else
  python3 "$GS/gh_gate74.py" api --pr "$ROW" --head "$H1423" > "$OUTP.api.out" 2> "$OUTP.api.err"; arc=$?
  echo "  api #$ROW rc=$arc | $(grep -E '^(CHECKED|[0-9]+ FAIL)' "$OUTP.api.out" | tr '\n' ' ')"; grep -E '^(FAIL|INFO)' "$OUTP.api.out" | sed 's/^/    /' | cut -c1-240
  [ "$arc" -eq 3 ] && { echo "REFUSING: API failure"; exit 3; }
  [ "$arc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the API does not show #$ROW open, unmerged, on develop at $H1423 with the kit's shape"; exit 11; }
  python3 "$GS/gh_gate74.py" census --pr "$ROW" > "$OUTP.census.out" 2> "$OUTP.census.err"; crc=$?
  sed 's/^/    /' "$OUTP.census.out" | cut -c1-240; echo "  census rc=$crc (REPORTED, not refused)"
fi

echo "--- 3b. develop: origin $CUR_DEV | --develop $DEV"
DEV_MOVED=0
if [ "$CUR_DEV" = "$DEV" ]; then echo "  UNMOVED (== the draft develop: the kit's predicted squash tree applies)."
  [ -z "$REPIN" ] || [ "$REPIN" = "$CUR_DEV" ] || { echo "REFUSING TO LAUNCH: --repin-develop $REPIN is not origin develop $CUR_DEV (stale re-pin)"; exit 10; }
else DEV_MOVED=1; echo "  DEVELOP MOVED: $DEV -> $CUR_DEV (3c checks descent, that the advance touches none of the row's paths, and RE-PREDICTS the squash)"; fi

echo "--- 3c. the kit's own clone: fetch by sha if absent, C1 on the develop read now, the squash prediction"
if [ ! -d "$CL/.git" ] && [ ! -f "$CL/HEAD" ]; then
  mkdir -p "$GS/_scratch"; env -u GIT_SSH_COMMAND git clone --shared --no-checkout --quiet "$CHECKOUT" "$CL" > "$OUTP.clone.out" 2> "$OUTP.clone.err" || { echo "REFUSING: kit clone failed"; exit 13; }
fi
git -C "$CL" config remote.origin.url "$URL"
git -C "$CL" config core.sshCommand "$(git -C "$CHECKOUT" config --get core.sshCommand)"
for s in $H1423 "$CUR_DEV" "$(KJ base)" "$(KJ trailer_control)" "$(KJ rows.$ROW.ks1164_fix_commit)" "$(KJ merge_tree_control.ours)" "$(KJ merge_tree_control.theirs)" "$(KJ t3_1422.head)"; do
  git -C "$CL" cat-file -e "$s^{commit}" 2>/dev/null || env -u GIT_SSH_COMMAND git -C "$CL" fetch --quiet --no-tags --no-write-fetch-head origin "$s" >> "$OUTP.fetch.out" 2>> "$OUTP.fetch.err"
  git -C "$CL" cat-file -e "$s^{commit}" 2>/dev/null || { echo "REFUSING: $s is ABSENT from the kit clone after a by-sha fetch"; tail -3 "$OUTP.fetch.err" 2>/dev/null; exit 19; }
done
python3 "$GS/c1_pin_gate74.py" --pr "$ROW" --repo "$CL" --head "$H1423" --base "$(KJ base)" --parents-n 1 --end-tree "$(KJ rows.$ROW.end_tree)" --develop "$CUR_DEV" --others "1422=$(KJ t3_1422.head)" > "$OUTP.c1.out" 2> "$OUTP.c1.err"; rc1=$?
echo "  c1 #$ROW rc=$rc1 | $(grep -E '^(CHECKED|[0-9]+ FAIL)' "$OUTP.c1.out" | tr '\n' ' ')"; grep -E '^FAIL' "$OUTP.c1.out" | sed 's/^/    /' | cut -c1-240
[ "$rc1" -eq 0 ] || { echo "REFUSING TO LAUNCH: C1 FAILED at the head (a pin moved: re-draft)"; exit 13; }
_XT=""; [ "$DEV_MOVED" = 0 ] && _XT="$(KJ predicted_squash.tree)"
python3 "$GS/c4_docs_gate74.py" merged --pr "$ROW" --repo "$CL" --base "$(KJ base)" --head "$H1423" --develop "$CUR_DEV" ${_XT:+--expect-tree "$_XT"} > "$OUTP.c4merged.out" 2> "$OUTP.c4merged.err"; rc4=$?
grep -E '^(MERGE-IN NEEDED|LEG-14|PREDICTED_TREE|FAIL)' "$OUTP.c4merged.out" | sed 's/^/    /' | cut -c1-240; echo "  c4 merged rc=$rc4"
[ "$rc4" -eq 0 ] && grep -q '^MERGE-IN NEEDED: no' "$OUTP.c4merged.out" || { echo "REFUSING TO LAUNCH: the squash onto develop $CUR_DEV is NOT predicted merge-in-free (read $OUTP.c4merged.out). A merge-in push is refused by leg 14 while KS-1450 is open: RE-DRAFT, never --no-verify."; exit 13; }
PRED="$(grep '^PREDICTED_TREE=' "$OUTP.c4merged.out" | cut -d= -f2)"
if [ "$DEV_MOVED" = 1 ]; then
  if [ -z "$REPIN" ]; then echo "REFUSING TO LAUNCH: develop moved (c1 P12 says it touched none of the row's paths; the squash is RE-PREDICTED above: $PRED). To re-pin and launch over it, re-run with:  --repin-develop $CUR_DEV"; exit 10
  elif [ "$REPIN" != "$CUR_DEV" ]; then echo "REFUSING TO LAUNCH: --repin-develop $REPIN is not origin develop $CUR_DEV (stale re-pin)"; exit 10; fi
  echo "repin $(date -u +%Y-%m-%dT%H:%M:%SZ): develop $DEV -> $CUR_DEV; squash $PRED" > "$OUTP.repin.txt"; echo "  RE-PINNED develop -> $CUR_DEV ($OUTP.repin.txt)"
fi

echo "--- S. the Actions comparator must be RULED (RULINGS Q-SCHEMA74)"
COMP="$(KJ actions_comparator)"; SEAT="$(KJ merge_seat_ordinal)"
if [ -z "$COMP" ]; then
  if [ "$DRY" = 1 ]; then echo "  (DRY RUN: REPORTED, not refused — kit.json actions_comparator is null; a real run refuses rc 8 and the launcher refuses rc 8)"; COMP="UNRULED"
  else echo "REFUSING TO LAUNCH: RULING NEEDED — kit.json actions_comparator is null (RULINGS Q-SCHEMA74)"; exit 8; fi
else echo "  comparator: $COMP"; fi
echo "  merge seat: $SEAT ($(KJ merge_seat))"

echo "--- R. render the prompt (head, develop $CUR_DEV, merge seat $SEAT, comparator $COMP, predicted squash $PRED)"
python3 - "$GS/prompt_gate74.txt" "$GS/prompt_gate74.rendered.txt" "$GS/head_at_launch.txt" "$KITJSON" "$CUR_DEV" "$SEAT" "$PRED" "$H1423" "$COMP" <<'PYEOF' || { echo "REFUSING: render failed"; exit 9; }
import json, sys
src, dst, hf, kj, dev, seat, pred, head, comp = sys.argv[1:10]
K = json.load(open(kj)); t = open(src, encoding='utf-8').read()
need = {'{{HEAD_1423}}': 5, '{{DEVELOP}}': 2, '{{MERGE_SEAT}}': 1, '{{PREDICTED_TREE}}': 2, '{{COMPARATOR}}': 3}
low = ['%s x%d' % (k, t.count(k)) for k, n in need.items() if t.count(k) < n]
if low: raise SystemExit('template tokens below their floor: %s' % low)
t = t.replace('{{HEAD_1423}}', head).replace('{{DEVELOP}}', dev).replace('{{MERGE_SEAT}}', seat).replace('{{PREDICTED_TREE}}', pred).replace('{{COMPARATOR}}', comp)
if '{{' in t: raise SystemExit('an unknown {{token}} survived the render')
open(dst, 'w', encoding='utf-8').write(t)
R = K['rows']['1423']
lines = ['P 1423 %s %s %s' % (R['branch'], head, R['end_tree']), 'B %s 1' % K['base'], 'D %s' % dev, 'S %s' % seat, 'C %s' % comp]
open(hf, 'w').write('\n'.join(lines) + '\n')
print('  rendered -> %s (%d bytes); head file %s (P / B / D / S / C)' % (dst, len(t.encode()), hf))
PYEOF

echo "--- 0. routing: the pane must be in inbox_routing.conf"
/usr/bin/grep -c -x -F "$LINE" "$ROUTING" > "$OUTP.routing.out" 2> "$OUTP.routing.err"; rc=$?
echo "  $ROUTING — exact line present: $(cat "$OUTP.routing.out") (grep rc=$rc; want 1 / rc 0). CONTROL: agentmail lines in the file = $(/usr/bin/grep -c -i 'agentmail' "$ROUTING")"
if [ "$rc" -ne 0 ]; then
  if [ "$DRY" = 1 ]; then echo "  (DRY RUN: reported, not refused — the real run refuses rc 1; ROUTING_LINE.txt)"; else echo "REFUSING: add the routing line first (ROUTING_LINE.txt): $LINE"; exit 1; fi
fi

if [ "$DRY" = 1 ]; then
  echo "--- 6 (dry). the launcher's own --check"
  G74_KITJSON="$KITJSON" "$L" --check > "$OUTP.launcher_check.out" 2> "$OUTP.launcher_check.err"; rc=$?
  sed 's/^/    /' "$OUTP.launcher_check.out" "$OUTP.launcher_check.err"; echo "  launcher --check rc=$rc"
  [ "$rc" -eq 0 ] || { echo "DRY RUN: the launcher refused under --check (rc $rc)"; exit 13; }
  echo "DRY RUN COMPLETE $(date -u '+%Y-%m-%dT%H:%M:%SZ') — develop $CUR_DEV; the real run continues with the override check, the usage gate, --check and cockpit.sh add"; exit 0
fi
echo "--- 4. no test override on a real launch"
[ "$(env | grep -c '^G74_')" = 0 ] || { echo "REFUSING TO LAUNCH: a G74_* override is set"; exit 16; }
echo "--- 5. usage gate"
"$(KJ usage_gate)" --check > "$OUTP.usage_gate.out" 2> "$OUTP.usage_gate.err"; rc=$?
sed 's/^/    /' "$OUTP.usage_gate.out" "$OUTP.usage_gate.err"; echo "  usage_gate rc=$rc (WED_USAGE_STOP=${WED_USAGE_STOP:-unset})"
[ "$rc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the usage gate refused (WED_USAGE_STOP only with Kam's recorded authority)"; exit 12; }
echo "--- 6. the launcher's own --check"
"$L" --check > "$OUTP.launcher_check.out" 2> "$OUTP.launcher_check.err"; rc=$?
sed 's/^/    /' "$OUTP.launcher_check.out" "$OUTP.launcher_check.err"; echo "  launcher --check rc=$rc"
[ "$rc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the launcher refused under --check"; exit 13; }
echo "--- 7. cockpit.sh add (the fleet's own tooling, never raw send-keys)"
"$(KJ cockpit)" add "$PANE" "$L" > "$OUTP.cockpit_add.out" 2> "$OUTP.cockpit_add.err"; rc=$?
sed 's/^/    /' "$OUTP.cockpit_add.out" "$OUTP.cockpit_add.err"; echo "  cockpit.sh add rc=$rc"
[ "$rc" -eq 0 ] || { echo "LAUNCH FAILED at cockpit.sh add"; exit 14; }
echo "--- pane census"
/opt/homebrew/bin/tmux list-panes -a -F '#{pane_id} | #{@cockpit_name} | #{pane_current_command} | #{session_name}:#{window_index}.#{pane_index}'
echo "LAUNCHED $(date -u '+%Y-%m-%dT%H:%M:%SZ'); develop at launch $CUR_DEV — now verify RUNG 5 (KIT_REPORT §8)"
