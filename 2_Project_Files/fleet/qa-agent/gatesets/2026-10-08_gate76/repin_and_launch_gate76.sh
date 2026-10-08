#!/bin/bash
# repin_and_launch_gate76.sh — the LAUNCH ACTION for gate76 (T2 x2: #1427 KS-1274, #1428 KS-593, batched, each its own verdict).
# NOT RUN BY THE DRAFTER except `--dry-run`. Carried from repin_and_launch_gate75.sh and re-keyed for TWO rows by the gate76 drafter.
# CHANGED at gate76 (gate75 refused ONCE at its first real run for lacking this): step 5 EXPORTS WED_USAGE_STOP=<kit usage_stop> into this
# script's own environment AFTER it reads Kam's grant file (kit usage_authority: `status: live`, the card id, the GATE clause; rc 12 otherwise),
# so the usage check AND `cockpit.sh add` (which runs usage_gate.sh itself, cockpit.sh:151) both see it. gate75 passed it to the --check only,
# and cockpit add refused at 97% (gate75 `_scratch/runs/launch_020640.cockpit_add.err`; the 020734 re-run with the value exported read
# `usage_gate: OK — weekly usage 97% < 100%` and added the pane). Read, not driven: cockpit.sh :50 unsets ONLY COCKPIT_UP_BUILD, and :151
# runs usage_gate.sh with the caller's environment, so an EXPORTED WED_USAGE_STOP reaches it. The dry run cannot drive cockpit add without
# adding a pane: it proves the --check half; the real run's step 7 output is the proof of the other half.
# EVERY PR-SPECIFIC CONSTANT IS A REQUIRED ARGUMENT, compared with kit.json (the drafter's pin) AND with what this script reads live:
#   (V)  --head-1427 --head-1428 --develop, present and full 40-hex — rc 9; each head == kit.json, --develop == kit develop_at_draft — rc 11
#   (A)  each push mail (kit rows.<n>.ready) names its head in full and #<n>                                         — rc 18
#   (2)  ONE `git ls-remote` of develop + both refs/pull/<n>/head + both branches, from the Secuura checkout: GIT_SSH_COMMAND UNSET,
#        `-c core.sshCommand=<the checkout's own>`, the GitHub URL (a read verb); each head == pull/head == branch     — rc 11 (MISMATCH)
#   (1)  gh_gate76.py api per row (rc 3 API failure; rc 11 not open / not develop / head differs) + census (REPORTED, not refused).
#        `--no-api` skips both ONLY with --dry-run.
#   (3b) origin develop == --develop -> on; MOVED -> rc 10 unless `--repin-develop <origin's 40-hex>` (stale re-pin rc 10)
#   (3c) THE KIT'S OWN CLONE (<kit>/_scratch/clone, gitignored; `clone --shared --no-checkout` of the checkout, origin = the GitHub URL,
#        the checkout's core.sshCommand, NEVER an exported GIT_SSH_COMMAND): fetch heads / develop / base / controls BY SHA only if absent;
#        any still absent refused BY NAME — rc 19. c1 per row with EVERY required pin must pass — rc 13. c4 `calibrate` must pass — rc 13.
#        c4 `chain --order <kit order> --develop <develop read NOW>` must pass (a develop that moved a row's CODE path refuses: RE-GATE) —
#        rc 13; at the draft develop its step trees must equal kit.json predicted_chain — rc 13.
#   (S)  the Actions comparator and the merge seat are RULED (kit.json) — rc 8 (a dry run REPORTS it instead)
#   (R)  render prompt_gate76.txt -> prompt_gate76.rendered.txt + head_at_launch.txt (P x2 / B / D / S / C / O / T)            — rc 9
#   (0)  the pane is routed in inbox_routing.conf — rc 1 (a dry run REPORTS it instead)
#   (4)  G76_* overrides refuse a real launch — rc 16;  (5) the usage grant + export — rc 12;  (6) the launcher's --check — rc 13;
#   (7)  cockpit add (with WED_USAGE_STOP exported) — rc 14
# --dry-run: V, A, 2, 1 (or --no-api), 3b, 3c, S (reported), R, 0 (reported), 5 (read-only: the grant read + usage --check at the exported
# stop) and the launcher's --check, then stops. Outputs: launch_<HHMMSS>.* (dry: dry_<HHMMSS>.*) under <kit>/_scratch/runs/.
# Controls-only overrides (DRY RUN ONLY): G76_ROUTING, G76_LSFILE, G76_KITJSON, G76_CLONE (an existing clone OUTSIDE !CODING).
# Usage (run under `script -q /dev/null`):
#   repin_and_launch_gate76.sh --head-1427 <40-hex> --head-1428 <40-hex> --develop <40-hex> [--dry-run [--no-api]] [--repin-develop <40-hex>]
set -u
export PYTHONDONTWRITEBYTECODE=1
GS="$(dirname "$(/bin/realpath "$0")")"
CHECKOUT='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
KITJSON="${G76_KITJSON:-$GS/kit.json}"
KJ() { python3 -c 'import json,sys; v=json.load(open(sys.argv[1]))
for k in sys.argv[2].split("."): v=v[int(k)] if isinstance(v,list) else v[k]
print(" ".join(map(str,v)) if isinstance(v,list) else ("" if v is None else v))' "$KITJSON" "$1"; }
ROUTING="${G76_ROUTING:-$(KJ routing)}"; PANE="$(KJ pane)"; LINE="$(KJ routing_line)"; URL="$(KJ github_url)"
L="$GS/$(KJ launcher)"; CL="${G76_CLONE:-$GS/_scratch/clone}"; ROWS='1427 1428'
ORDER="$(KJ merge_order_default | tr ' ' ',')"
USAGE="usage: repin_and_launch_gate76.sh --head-1427 <40-hex> --head-1428 <40-hex> --develop <40-hex> [--dry-run [--no-api]] [--repin-develop <40-hex>]"
H1427=""; H1428=""; DEV=""; DRY=0; NOAPI=0; REPIN=""
while [ $# -gt 0 ]; do
  case "$1" in
    --head-1427) H1427="${2:-}"; shift 2 2>/dev/null || shift;;     --head-1428) H1428="${2:-}"; shift 2 2>/dev/null || shift;;
    --develop) DEV="${2:-}"; shift 2 2>/dev/null || shift;;         --repin-develop) REPIN="${2:-}"; shift 2 2>/dev/null || shift;;
    --dry-run) DRY=1; shift;; --no-api) NOAPI=1; shift;;
    *) echo "$USAGE"; exit 9;;
  esac
done
echo "--- V. required arguments, each well-formed and == the kit's pin (a wrong value refuses BY NAME)"
for _a in H1427 H1428 DEV; do eval "_v=\$$_a"; [ -n "$_v" ] || { echo "REFUSING: a REQUIRED argument is missing ($_a)"; echo "$USAGE"; exit 9; }; done
for _a in H1427 H1428 DEV; do eval "_v=\$$_a"; printf '%s' "$_v" | grep -qE '^[0-9a-f]{40}$' || { echo "REFUSING: $_a must be the FULL 40-hex sha, got '$_v'"; exit 9; }; done
[ -z "$REPIN" ] || printf '%s' "$REPIN" | grep -qE '^[0-9a-f]{40}$' || { echo "REFUSING: --repin-develop must be the FULL 40-hex sha, got '$REPIN'"; exit 9; }
[ "$NOAPI" = 0 ] || [ "$DRY" = 1 ] || { echo "REFUSING: --no-api is a dry-run option only (a real launch reads the PR API)"; exit 9; }
[ "$H1427" = "$(KJ rows.1427.head_expected)" ] || { echo "REFUSING: WRONG VALUE --head-1427 '$H1427' != kit.json $(KJ rows.1427.head_expected) — re-draft"; exit 11; }
[ "$H1428" = "$(KJ rows.1428.head_expected)" ] || { echo "REFUSING: WRONG VALUE --head-1428 '$H1428' != kit.json $(KJ rows.1428.head_expected) — re-draft"; exit 11; }
[ "$DEV" = "$(KJ develop_at_draft)" ] || { echo "REFUSING: WRONG VALUE --develop '$DEV' != kit.json develop_at_draft $(KJ develop_at_draft) (pass the draft develop; a moved develop is handled by --repin-develop)"; exit 11; }
echo "  heads + develop present, well-formed and == kit.json"
[ -z "${G76_CLONE:-}" ] || [ "$DRY" = 1 ] || { echo "REFUSING: G76_CLONE is a dry-run control only"; exit 16; }
case "$(/bin/realpath "$CL" 2>/dev/null || echo "$CL")" in "/Volumes/DevMASTER/!CODING"*) echo "REFUSING: the kit clone $CL is under !CODING"; exit 16;; esac
mkdir -p "$GS/_scratch/runs"
T="$(date -u +%H%M%S)"; OUTP="$GS/_scratch/runs/launch_$T"; [ "$DRY" = 1 ] && OUTP="$GS/_scratch/runs/dry_$T"
echo "LAUNCH ACTION gate76$([ "$DRY" = 1 ] && echo ' (DRY RUN)') $(date '+%Y-%m-%d %H:%M:%S %Z') / $(date -u '+%Y-%m-%dT%H:%M:%SZ') | develop $DEV | repin-develop ${REPIN:-none} | order $ORDER | pane $PANE | outputs $OUTP.*"

echo "--- A. each head must be the one its author's push mail names"
for ROW in $ROWS; do
  eval "_H=\$H$ROW"; READY="$(KJ rows.$ROW.ready)"
  [ -s "$READY" ] || { echo "REFUSING: push mail missing or empty ('$READY')"; exit 18; }
  _n="$(/usr/bin/grep -c -F "$_H" "$READY")"; _p="$(/usr/bin/grep -c -F "#$ROW" "$READY")"; _c="$(/usr/bin/grep -c -i 'READY FOR QA' "$READY")"
  echo "  #$ROW $(basename "$READY") (sha256/16 $(shasum -a 256 "$READY" | cut -c1-16)): lines naming the head in full $_n | naming #$ROW $_p | CONTROL lines naming 'READY FOR QA' $_c"
  [ "$_n" -ge 1 ] && [ "$_p" -ge 1 ] || { echo "REFUSING: the push mail does not name $_H in full (or #$ROW)"; exit 18; }
done

echo "--- 2. ONE ls-remote (read verb) from the checkout, GIT_SSH_COMMAND unset, the checkout's own core.sshCommand"
[ -z "${GIT_SSH_COMMAND:-}" ] || echo "  NOTE: GIT_SSH_COMMAND is exported in this shell; every git call below runs under env -u GIT_SSH_COMMAND"
REFS="refs/heads/develop"; for ROW in $ROWS; do REFS="$REFS refs/pull/$ROW/head refs/heads/$(KJ rows.$ROW.branch)"; done
if [ -n "${G76_LSFILE:-}" ]; then
  [ "$DRY" = 1 ] || { echo "REFUSING: G76_LSFILE is a dry-run control only"; exit 16; }
  cp "$G76_LSFILE" "$OUTP.lsremote.out"; : > "$OUTP.lsremote.err"; rc=0; echo "  (CONTROL: ls-remote output read from the stand-in $G76_LSFILE)"
else
  env -u GIT_SSH_COMMAND git -C "$CHECKOUT" -c core.sshCommand="$(git -C "$CHECKOUT" config --get core.sshCommand)" ls-remote "$URL" $REFS > "$OUTP.lsremote.out" 2> "$OUTP.lsremote.err"; rc=$?
fi
get() { awk -v r="$1" '$2==r{print $1}' "$OUTP.lsremote.out"; }
CUR_DEV="$(get refs/heads/develop)"
echo "  ls-remote rc=$rc at $(date -u +%H:%M:%SZ) | develop $CUR_DEV"
[ "$rc" -eq 0 ] && [ -n "$CUR_DEV" ] || { echo "REFUSING: ls-remote failed or returned no develop"; sed 's/^/    stderr: /' "$OUTP.lsremote.err"; exit 2; }
for ROW in $ROWS; do
  eval "_H=\$H$ROW"; BR="$(KJ rows.$ROW.branch)"; _p="$(get "refs/pull/$ROW/head")"; _b="$(get "refs/heads/$BR")"
  echo "  #$ROW pull/head $_p | branch $_b"
  [ "$_p" = "$_H" ] && [ "$_b" = "$_H" ] || { echo "REFUSING TO LAUNCH: #$ROW origin pull/head '$_p' / branch '$_b' != --head-$ROW $_H — MISMATCH"; exit 11; }
done

echo "--- 1. PULLS API + census"
if [ "$NOAPI" = 1 ]; then echo "  SKIPPED BY NAME (--no-api, dry run only): the API state and the census are NOT read here"
else
  for ROW in $ROWS; do
    eval "_H=\$H$ROW"
    python3 "$GS/gh_gate76.py" api --pr "$ROW" --head "$_H" > "$OUTP.api_$ROW.out" 2> "$OUTP.api_$ROW.err"; arc=$?
    echo "  api #$ROW rc=$arc | $(grep -E '^(CHECKED|[0-9]+ FAIL)' "$OUTP.api_$ROW.out" | tr '\n' ' ')"; grep -E '^(FAIL|INFO)' "$OUTP.api_$ROW.out" | sed 's/^/    /' | cut -c1-240
    [ "$arc" -eq 3 ] && { echo "REFUSING: API failure"; exit 3; }
    [ "$arc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the API does not show #$ROW open, unmerged, on develop at $_H with the kit's shape"; exit 11; }
  done
  python3 "$GS/gh_gate76.py" census --pr 1427 > "$OUTP.census.out" 2> "$OUTP.census.err"; crc=$?
  sed 's/^/    /' "$OUTP.census.out" | cut -c1-240; echo "  census rc=$crc (REPORTED, not refused)"
fi

echo "--- 3b. develop: origin $CUR_DEV | --develop $DEV"
DEV_MOVED=0
if [ "$CUR_DEV" = "$DEV" ]; then echo "  UNMOVED (== the draft develop: the kit's predicted chain applies)."
  [ -z "$REPIN" ] || [ "$REPIN" = "$CUR_DEV" ] || { echo "REFUSING TO LAUNCH: --repin-develop $REPIN is not origin develop $CUR_DEV (stale re-pin)"; exit 10; }
else DEV_MOVED=1; echo "  DEVELOP MOVED: $DEV -> $CUR_DEV (3c checks descent, that the advance touches no row CODE path, and RE-PREDICTS the chain)"; fi

echo "--- 3c. the kit's own clone: fetch by sha if absent, c1 per row on the develop read now, calibrate, the chain prediction"
if [ ! -d "$CL/.git" ] && [ ! -f "$CL/HEAD" ]; then
  mkdir -p "$GS/_scratch"; env -u GIT_SSH_COMMAND git clone --shared --no-checkout --quiet "$CHECKOUT" "$CL" > "$OUTP.clone.out" 2> "$OUTP.clone.err" || { echo "REFUSING: kit clone failed"; exit 13; }
fi
git -C "$CL" config remote.origin.url "$URL"
git -C "$CL" config core.sshCommand "$(git -C "$CHECKOUT" config --get core.sshCommand)"
for s in $H1427 $H1428 "$CUR_DEV" "$(KJ base)" "$(KJ trailer_control)" "$(KJ merge_tree_control.ours)" "$(KJ merge_tree_control.theirs)"; do
  git -C "$CL" cat-file -e "$s^{commit}" 2>/dev/null || env -u GIT_SSH_COMMAND git -C "$CL" fetch --quiet --no-tags --no-write-fetch-head origin "$s" >> "$OUTP.fetch.out" 2>> "$OUTP.fetch.err"
  git -C "$CL" cat-file -e "$s^{commit}" 2>/dev/null || { echo "REFUSING: $s is ABSENT from the kit clone after a by-sha fetch"; tail -3 "$OUTP.fetch.err" 2>/dev/null; exit 19; }
done
for ROW in $ROWS; do
  eval "_H=\$H$ROW"
  python3 "$GS/c1_pin_gate76.py" --pr "$ROW" --repo "$CL" --head "$_H" --base "$(KJ base)" --parents-n 1 --end-tree "$(KJ rows.$ROW.end_tree)" --develop "$CUR_DEV" > "$OUTP.c1_$ROW.out" 2> "$OUTP.c1_$ROW.err"; rc1=$?
  echo "  c1 #$ROW rc=$rc1 | $(grep -E '^(CHECKED|[0-9]+ FAIL)' "$OUTP.c1_$ROW.out" | tr '\n' ' ')"; grep -E '^FAIL' "$OUTP.c1_$ROW.out" | sed 's/^/    /' | cut -c1-240
  [ "$rc1" -eq 0 ] || { echo "REFUSING TO LAUNCH: C1 FAILED for #$ROW (a pin moved: re-draft)"; exit 13; }
done
HE="1427=$H1427,1428=$H1428"
python3 "$GS/c4_docs_gate76.py" calibrate --repo "$CL" --heads "$HE" > "$OUTP.c4cal.out" 2> "$OUTP.c4cal.err"; rcc=$?
echo "  c4 calibrate rc=$rcc | $(grep -E '^(CHECKED|[0-9]+ FAIL)' "$OUTP.c4cal.out" | tr '\n' ' ')"
[ "$rcc" -eq 0 ] || { echo "REFUSING TO LAUNCH: c4 calibrate FAILED (read $OUTP.c4cal.out)"; exit 13; }
mkdir -p "$OUTP.chain"   # a fresh timestamped dir; nothing is ever deleted (Kam 2026-08-26: quarantine, never delete)
python3 "$GS/c4_docs_gate76.py" chain --repo "$CL" --order "$ORDER" --develop "$CUR_DEV" --heads "$HE" --out "$OUTP.chain" > "$OUTP.c4chain.out" 2> "$OUTP.c4chain.err"; rcq=$?
grep -E '^(STEP|   guard|FINAL|CHAIN|REFUSED)' "$OUTP.c4chain.out" | sed 's/^/    /' | cut -c1-240; echo "  c4 chain rc=$rcq"
[ "$rcq" -eq 0 ] || { echo "REFUSING TO LAUNCH: the chain onto develop $CUR_DEV is NOT predicted (read $OUTP.c4chain.out). A moved CODE path is a RE-GATE; never --no-verify."; exit 13; }
PRED2="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["steps"][-1]["tree"])' "$OUTP.chain/chain.json")"
if [ "$DEV_MOVED" = 0 ]; then
  _W1="$(KJ predicted_chain.steps.0.tree)"; _W2="$(KJ predicted_chain.steps.1.tree)"
  _G1="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["steps"][0]["tree"])' "$OUTP.chain/chain.json")"
  [ "$_G1" = "$_W1" ] && [ "$PRED2" = "$_W2" ] || { echo "REFUSING TO LAUNCH: at the draft develop the chain read $_G1 / $PRED2, kit.json predicted $_W1 / $_W2"; exit 13; }
  echo "  at the draft develop the chain == kit.json predicted_chain (step 1 ${_W1:0:12}, step 2 ${_W2:0:12})"
fi
if [ "$DEV_MOVED" = 1 ]; then
  if [ -z "$REPIN" ]; then echo "REFUSING TO LAUNCH: develop moved (c1 P12 says it touched no row CODE path; the chain is RE-PREDICTED above: step-2 tree $PRED2). To re-pin and launch over it, re-run with:  --repin-develop $CUR_DEV"; exit 10
  elif [ "$REPIN" != "$CUR_DEV" ]; then echo "REFUSING TO LAUNCH: --repin-develop $REPIN is not origin develop $CUR_DEV (stale re-pin)"; exit 10; fi
  echo "repin $(date -u +%Y-%m-%dT%H:%M:%SZ): develop $DEV -> $CUR_DEV; step-2 tree $PRED2" > "$OUTP.repin.txt"; echo "  RE-PINNED develop -> $CUR_DEV ($OUTP.repin.txt)"
fi

echo "--- S. the Actions comparator and the merge seat must be ruled (kit.json)"
COMP="$(KJ actions_comparator)"; SEAT="$(KJ merge_seat_ordinal)"
if [ -z "$COMP" ] || [ -z "$SEAT" ]; then
  if [ "$DRY" = 1 ]; then echo "  (DRY RUN: REPORTED, not refused — comparator '$COMP' / merge seat '$SEAT'; a real run refuses rc 8 and the launcher refuses rc 8)"; COMP="${COMP:-UNRULED}"; SEAT="${SEAT:-UNRULED}"
  else echo "REFUSING TO LAUNCH: RULING NEEDED — kit.json actions_comparator / merge_seat_ordinal is null"; exit 8; fi
else echo "  comparator: $COMP | merge seat: $SEAT ($(KJ merge_seat))"; fi

echo "--- R. render the prompt (heads, develop $CUR_DEV, merge seat $SEAT, comparator $COMP, order $ORDER, step-2 tree $PRED2)"
python3 - "$GS/prompt_gate76.txt" "$GS/prompt_gate76.rendered.txt" "$GS/head_at_launch.txt" "$KITJSON" "$CUR_DEV" "$SEAT" "$PRED2" "$H1427" "$H1428" "$COMP" "$ORDER" <<'PYEOF' || { echo "REFUSING: render failed"; exit 9; }
import json, sys
src, dst, hf, kj, dev, seat, pred, h7, h8, comp, order = sys.argv[1:12]
K = json.load(open(kj)); t = open(src, encoding='utf-8').read()
need = {'{{HEAD_1427}}': 1, '{{HEAD_1428}}': 1, '{{DEVELOP}}': 2, '{{MERGE_SEAT}}': 3, '{{PREDICTED_STEP2_TREE}}': 2, '{{COMPARATOR}}': 2, '{{ORDER}}': 3}
low = ['%s x%d' % (k, t.count(k)) for k, n in need.items() if t.count(k) < n]
if low: raise SystemExit('template tokens below their floor: %s' % low)
for k, v in (('{{HEAD_1427}}', h7), ('{{HEAD_1428}}', h8), ('{{DEVELOP}}', dev), ('{{MERGE_SEAT}}', seat), ('{{PREDICTED_STEP2_TREE}}', pred),
             ('{{COMPARATOR}}', comp), ('{{ORDER}}', order)):
    t = t.replace(k, v)
if '{{' in t: raise SystemExit('an unknown {{token}} survived the render')
open(dst, 'w', encoding='utf-8').write(t)
R7, R8 = K['rows']['1427'], K['rows']['1428']
lines = ['P 1427 %s %s %s' % (R7['branch'], h7, R7['end_tree']), 'P 1428 %s %s %s' % (R8['branch'], h8, R8['end_tree']),
         'B %s 1' % K['base'], 'D %s' % dev, 'S %s' % seat, 'C %s' % comp, 'O %s' % order, 'T %s' % pred]
open(hf, 'w').write('\n'.join(lines) + '\n')
print('  rendered -> %s (%d bytes); head file %s (P x2 / B / D / S / C / O / T)' % (dst, len(t.encode()), hf))
PYEOF

echo "--- 0. routing: the pane must be in inbox_routing.conf"
/usr/bin/grep -c -x -F "$LINE" "$ROUTING" > "$OUTP.routing.out" 2> "$OUTP.routing.err"; rc=$?
echo "  $ROUTING — exact line present: $(cat "$OUTP.routing.out") (grep rc=$rc; want 1 / rc 0). CONTROL: agentmail lines in the file = $(/usr/bin/grep -c -i 'agentmail' "$ROUTING")"
if [ "$rc" -ne 0 ]; then
  if [ "$DRY" = 1 ]; then echo "  (DRY RUN: reported, not refused — the real run refuses rc 1; ROUTING_LINE.txt)"; else echo "REFUSING: add the routing line first (ROUTING_LINE.txt): $LINE"; exit 1; fi
fi

echo "--- 5. usage: Kam's grant (kit usage_authority), then WED_USAGE_STOP=$(KJ usage_stop) EXPORTED for the usage check AND cockpit add"
GRANT="$(KJ usage_authority)"; USTOP="$(KJ usage_stop)"; CARD="$(KJ usage_authority_card)"
[ -s "$GRANT" ] || { echo "REFUSING TO LAUNCH: the grant file $GRANT is missing — no WED_USAGE_STOP override without Kam's recorded authority"; exit 12; }
/usr/bin/grep -q -i '^status: live' "$GRANT" && /usr/bin/grep -q -F "$CARD" "$GRANT" && /usr/bin/grep -q -i 'gate' "$GRANT" \
  || { echo "REFUSING TO LAUNCH: $GRANT does not read 'status: live' + card $CARD + the gate clause"; exit 12; }
echo "  authority: $(basename "$GRANT") (sha256/16 $(shasum -a 256 "$GRANT" | cut -c1-16)) — status live, card $CARD, clause: GATE. Expiry is an EVENT (the account renewal ~Fri 9 Oct morning, an account switch, or Kam's word): if it has happened, STOP."
export WED_USAGE_STOP="$USTOP"
"$(KJ usage_gate)" --check > "$OUTP.usage_gate.out" 2> "$OUTP.usage_gate.err"; rc=$?
sed 's/^/    /' "$OUTP.usage_gate.out" "$OUTP.usage_gate.err"; echo "  usage_gate --check rc=$rc (WED_USAGE_STOP=$WED_USAGE_STOP EXPORTED, named authority above)"
if [ "$rc" -ne 0 ]; then
  if [ "$DRY" = 1 ]; then echo "  (DRY RUN: reported — a real run refuses rc 12)"; else echo "REFUSING TO LAUNCH: the usage gate refused even at WED_USAGE_STOP=$USTOP"; exit 12; fi
fi

if [ "$DRY" = 1 ]; then
  echo "--- 6 (dry). the launcher's own --check"
  G76_KITJSON="$KITJSON" "$L" --check > "$OUTP.launcher_check.out" 2> "$OUTP.launcher_check.err"; rc=$?
  sed 's/^/    /' "$OUTP.launcher_check.out" "$OUTP.launcher_check.err"; echo "  launcher --check rc=$rc"
  [ "$rc" -eq 0 ] || { echo "DRY RUN: the launcher refused under --check (rc $rc)"; exit 13; }
  echo "DRY RUN COMPLETE $(date -u '+%Y-%m-%dT%H:%M:%SZ') — develop $CUR_DEV; the real run continues with the override check, --check and cockpit.sh add (WED_USAGE_STOP exported)"; exit 0
fi
echo "--- 4. no test override on a real launch"
[ "$(env | grep -c '^G76_')" = 0 ] || { echo "REFUSING TO LAUNCH: a G76_* override is set"; exit 16; }
echo "--- 6. the launcher's own --check"
"$L" --check > "$OUTP.launcher_check.out" 2> "$OUTP.launcher_check.err"; rc=$?
sed 's/^/    /' "$OUTP.launcher_check.out" "$OUTP.launcher_check.err"; echo "  launcher --check rc=$rc"
[ "$rc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the launcher refused under --check"; exit 13; }
echo "--- 7. cockpit.sh add (the fleet's own tooling, never raw send-keys), WED_USAGE_STOP=$WED_USAGE_STOP exported"
"$(KJ cockpit)" add "$PANE" "$L" > "$OUTP.cockpit_add.out" 2> "$OUTP.cockpit_add.err"; rc=$?
sed 's/^/    /' "$OUTP.cockpit_add.out" "$OUTP.cockpit_add.err"; echo "  cockpit.sh add rc=$rc"
[ "$rc" -eq 0 ] || { echo "LAUNCH FAILED at cockpit.sh add (if it reads 'REFUSED by usage_gate', the export did not reach cockpit.sh: STOP and tell Wednesday, never retry blind)"; exit 14; }
echo "--- pane census"
/opt/homebrew/bin/tmux list-panes -a -F '#{pane_id} | #{@cockpit_name} | #{pane_current_command} | #{session_name}:#{window_index}.#{pane_index}'
echo "LAUNCHED $(date -u '+%Y-%m-%dT%H:%M:%SZ'); develop at launch $CUR_DEV — now verify RUNG 5 (KIT_REPORT §8)"
