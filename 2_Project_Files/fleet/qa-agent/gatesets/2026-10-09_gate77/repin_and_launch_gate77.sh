#!/bin/bash
# repin_and_launch_gate77.sh — the LAUNCH ACTION (and the REPIN) for gate77: six rows (#1429 #1430 #1431 #1432 #1433 #1434), batched, each its
# own verdict. NOT RUN BY THE DRAFTER except `--dry-run`. Carried from repin_and_launch_gate76.sh and widened to six rows by the gate77 drafter.
# EXTENDED 2026-10-09 to SEVEN rows: + #1436 KS-808 (Seat F 6th, T2), a MERGE-IN row (parents [a24efb3c5e04, develop 81d2e5f4c415]);
# `--head-1436` is REQUIRED like the other six, and its merged-in base is fetched by sha with the heads. Backups: `*.pre-1009-1436`.
# THE REPIN RULE (minimise gate duplication): run IMMEDIATELY before launch. It re-reads develop and every head; a head that moved REFUSES
# (that row needs a re-draft; an unchanged diff is never re-gated); a develop that moved is read by WHAT moved (c1 P7: a row's CODE path moved
# = RE-GATE, refused; docs-only = the chain is RE-PREDICTED) and needs `--repin-develop <origin's 40-hex>` to proceed.
# CHANGED from gate76: NO WED_USAGE_STOP override. gate76's grant (2026-10-08 new-account) expired on an EVENT, the account renewal: at draft
# `usage_gate.sh --check` read 1% at the default 90. This script runs the usage check at the default and refuses rc 12 above it (Q-USAGE77).
# EVERY PR-SPECIFIC CONSTANT IS A REQUIRED ARGUMENT, compared with kit.json AND with what this script reads live:
#   (V)  --head-<n> for all seven + --develop (the DRAFT develop): present, full 40-hex — rc 9; each == kit.json — rc 11
#   (A)  each READY mail names its head in full and #<n>                                                              — rc 18
#   (2)  ONE `git ls-remote` of develop + seven refs/pull/<n>/head + seven branches + pull/1427/head, from the Secuura checkout, GIT_SSH_COMMAND
#        UNSET, `-c core.sshCommand=<the checkout's own>` (a read verb); each head == pull/head == branch                — rc 11 (MOVED HEAD)
#   (1)  gh_gate77.py api per row (rc 3 API failure; rc 11 not open / merged / not develop / head or files differ) + census (REPORTED).
#        `--no-api` skips both ONLY with --dry-run.
#   (3b) origin develop == --develop -> on; MOVED -> rc 10 unless `--repin-develop <origin's 40-hex>` (stale re-pin rc 10)
#   (3c) THE KIT'S OWN CLONE (<kit>/_scratch/clone, gitignored; `clone --shared --no-checkout`, origin = the GitHub URL): fetch heads / develop /
#        #1427 / raise_base / controls BY SHA only if absent (rc 19 if still absent). c1 --all on the develop read NOW — rc 13. c2 clean + collide —
#        rc 13. c2 chain in the EFFECTIVE order (#1427 prefixed when develop does not yet carry it) — rc 13; at the draft develop the final tree
#        must equal kit.json predicted_chain_with1427.final_tree — rc 13.
#   (S)  the Actions comparator and the merge seat are RULED (kit.json) — rc 8 (a dry run REPORTS it instead)
#   (R)  render prompt_gate77.txt -> prompt_gate77.rendered.txt + head_at_launch.txt (P x7 / B / D / S / C / O / T / Q)       — rc 9
#   (0)  the pane is routed in inbox_routing.conf — rc 1 (a dry run REPORTS it instead)
#   (4)  GATE77_* overrides refuse a real launch — rc 16;  (5) usage --check at the default — rc 12;  (6) the launcher's --check — rc 13;
#   (7)  cockpit add — rc 14
# Controls-only overrides (DRY RUN ONLY): GATE77_ROUTING, GATE77_LSFILE, GATE77_KITJSON, GATE77_CLONE (an existing clone OUTSIDE !CODING).
# Usage (run under `script -q /dev/null`):
#   repin_and_launch_gate77.sh --head-1429 <h> --head-1430 <h> --head-1431 <h> --head-1432 <h> --head-1433 <h> --head-1434 <h> --head-1436 <h> --develop <d>
#                              [--dry-run [--no-api]] [--repin-develop <40-hex>]
set -u
export PYTHONDONTWRITEBYTECODE=1
GS="$(dirname "$(/bin/realpath "$0")")"
CHECKOUT='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
KITJSON="${GATE77_KITJSON:-$GS/kit.json}"
KJ() { python3 -c 'import json,sys; v=json.load(open(sys.argv[1]))
for k in sys.argv[2].split("."): v=v[int(k)] if isinstance(v,list) else v[k]
print(" ".join(map(str,v)) if isinstance(v,list) else ("" if v is None else v))' "$KITJSON" "$1"; }
ROUTING="${GATE77_ROUTING:-$(KJ routing)}"; PANE="$(KJ pane)"; LINE="$(KJ routing_line)"; URL="$(KJ github_url)"
L="$GS/$(KJ launcher)"; CL="${GATE77_CLONE:-$GS/_scratch/clone}"; ROWS='1429 1430 1431 1432 1433 1434 1436'
ORDER="$(KJ merge_order_default | tr ' ' ',')"; P27="$(KJ pending_before_gate.0.head)"
USAGE="usage: repin_and_launch_gate77.sh --head-1429 <h> --head-1430 <h> --head-1431 <h> --head-1432 <h> --head-1433 <h> --head-1434 <h> --head-1436 <h> --develop <d> [--dry-run [--no-api]] [--repin-develop <40-hex>]"
H1429=""; H1430=""; H1431=""; H1432=""; H1433=""; H1434=""; H1436=""; DEV=""; DRY=0; NOAPI=0; REPIN=""
while [ $# -gt 0 ]; do
  case "$1" in
    --head-1429|--head-1430|--head-1431|--head-1432|--head-1433|--head-1434|--head-1436) eval "H${1#--head-}=\"\${2:-}\""; shift 2 2>/dev/null || shift;;
    --develop) DEV="${2:-}"; shift 2 2>/dev/null || shift;;  --repin-develop) REPIN="${2:-}"; shift 2 2>/dev/null || shift;;
    --dry-run) DRY=1; shift;; --no-api) NOAPI=1; shift;;
    *) echo "$USAGE"; exit 9;;
  esac
done
echo "--- V. required arguments, each well-formed and == the kit's pin (a wrong value refuses BY NAME)"
for _a in H1429 H1430 H1431 H1432 H1433 H1434 H1436 DEV; do eval "_v=\$$_a"; [ -n "$_v" ] || { echo "REFUSING: a REQUIRED argument is missing ($_a)"; echo "$USAGE"; exit 9; }; done
for _a in H1429 H1430 H1431 H1432 H1433 H1434 H1436 DEV; do eval "_v=\$$_a"; printf '%s' "$_v" | grep -qE '^[0-9a-f]{40}$' || { echo "REFUSING: $_a must be the FULL 40-hex sha, got '$_v'"; exit 9; }; done
[ -z "$REPIN" ] || printf '%s' "$REPIN" | grep -qE '^[0-9a-f]{40}$' || { echo "REFUSING: --repin-develop must be the FULL 40-hex sha, got '$REPIN'"; exit 9; }
[ "$NOAPI" = 0 ] || [ "$DRY" = 1 ] || { echo "REFUSING: --no-api is a dry-run option only (a real launch reads the PR API)"; exit 9; }
for ROW in $ROWS; do eval "_H=\$H$ROW"; [ "$_H" = "$(KJ rows.$ROW.head_expected)" ] || { echo "REFUSING: WRONG VALUE --head-$ROW '$_H' != kit.json $(KJ rows.$ROW.head_expected) — re-draft"; exit 11; }; done
[ "$DEV" = "$(KJ develop_at_draft)" ] || { echo "REFUSING: WRONG VALUE --develop '$DEV' != kit.json develop_at_draft $(KJ develop_at_draft) (pass the DRAFT develop; a moved develop is handled by --repin-develop)"; exit 11; }
echo "  seven heads + develop present, well-formed and == kit.json"
[ -z "${GATE77_CLONE:-}" ] || [ "$DRY" = 1 ] || { echo "REFUSING: GATE77_CLONE is a dry-run control only"; exit 16; }
case "$(/bin/realpath "$CL" 2>/dev/null || echo "$CL")" in "/Volumes/DevMASTER/!CODING"*) echo "REFUSING: the kit clone $CL is under !CODING"; exit 16;; esac
mkdir -p "$GS/_scratch/runs"
T="$(date -u +%H%M%S)"; OUTP="$GS/_scratch/runs/launch_$T"; [ "$DRY" = 1 ] && OUTP="$GS/_scratch/runs/dry_$T"
echo "LAUNCH ACTION gate77$([ "$DRY" = 1 ] && echo ' (DRY RUN)') $(date '+%Y-%m-%d %H:%M:%S %Z') / $(date -u '+%Y-%m-%dT%H:%M:%SZ') | develop $DEV | repin-develop ${REPIN:-none} | order $ORDER | pane $PANE | outputs $OUTP.*"

echo "--- A. each head must be the one its author's READY mail names"
for ROW in $ROWS; do
  eval "_H=\$H$ROW"; READY="$(KJ rows.$ROW.ready)"
  [ -s "$READY" ] || { echo "REFUSING: READY mail missing or empty ('$READY')"; exit 18; }
  _n="$(/usr/bin/grep -c -F "$_H" "$READY")"; _p="$(/usr/bin/grep -c -F "#$ROW" "$READY")"; _c="$(/usr/bin/grep -c -i 'READY FOR QA' "$READY")"
  echo "  #$ROW $(basename "$READY") (sha256/16 $(shasum -a 256 "$READY" | cut -c1-16)): lines naming the head in full $_n | naming #$ROW $_p | CONTROL 'READY FOR QA' lines $_c"
  [ "$_n" -ge 1 ] && [ "$_p" -ge 1 ] && [ "$_c" -ge 1 ] || { echo "REFUSING: the READY mail does not name $_H in full (or #$ROW, or is not a READY)"; exit 18; }
done

echo "--- 2. ONE ls-remote (read verb) from the checkout, GIT_SSH_COMMAND unset, the checkout's own core.sshCommand"
[ -z "${GIT_SSH_COMMAND:-}" ] || echo "  NOTE: GIT_SSH_COMMAND is exported in this shell; every git call below runs under env -u GIT_SSH_COMMAND"
REFS="refs/heads/develop refs/pull/1427/head"; for ROW in $ROWS; do REFS="$REFS refs/pull/$ROW/head refs/heads/$(KJ rows.$ROW.branch)"; done
if [ -n "${GATE77_LSFILE:-}" ]; then
  [ "$DRY" = 1 ] || { echo "REFUSING: GATE77_LSFILE is a dry-run control only"; exit 16; }
  cp "$GATE77_LSFILE" "$OUTP.lsremote.out"; : > "$OUTP.lsremote.err"; rc=0; echo "  (CONTROL: ls-remote output read from the stand-in $GATE77_LSFILE)"
else
  env -u GIT_SSH_COMMAND git -C "$CHECKOUT" -c core.sshCommand="$(git -C "$CHECKOUT" config --get core.sshCommand)" ls-remote "$URL" $REFS > "$OUTP.lsremote.out" 2> "$OUTP.lsremote.err"; rc=$?
fi
get() { awk -v r="$1" '$2==r{print $1}' "$OUTP.lsremote.out"; }
CUR_DEV="$(get refs/heads/develop)"
echo "  ls-remote rc=$rc at $(date -u +%H:%M:%SZ) | develop $CUR_DEV | pull/1427/head $(get refs/pull/1427/head)"
[ "$rc" -eq 0 ] && [ -n "$CUR_DEV" ] || { echo "REFUSING: ls-remote failed or returned no develop"; sed 's/^/    stderr: /' "$OUTP.lsremote.err"; exit 2; }
for ROW in $ROWS; do
  eval "_H=\$H$ROW"; BR="$(KJ rows.$ROW.branch)"; _p="$(get "refs/pull/$ROW/head")"; _b="$(get "refs/heads/$BR")"
  echo "  #$ROW pull/head $_p | branch $_b"
  [ "$_p" = "$_H" ] && [ "$_b" = "$_H" ] || { echo "REFUSING TO LAUNCH: #$ROW origin pull/head '$_p' / branch '$_b' != --head-$ROW $_H — MOVED HEAD: re-draft that row (an unchanged diff is never re-gated; a changed one is never gated on a stale pin)"; exit 11; }
done

echo "--- 1. PULLS API + census"
if [ "$NOAPI" = 1 ]; then echo "  SKIPPED BY NAME (--no-api, dry run only): the API state and the census are NOT read here"
else
  for ROW in $ROWS; do
    python3 "$GS/gh_gate77.py" api --pr "$ROW" > "$OUTP.api_$ROW.out" 2> "$OUTP.api_$ROW.err"; arc=$?
    echo "  api #$ROW rc=$arc | $(grep -E '^(CHECKED|[0-9]+ FAIL)' "$OUTP.api_$ROW.out" | tr '\n' ' ')"; grep -E '^FAIL' "$OUTP.api_$ROW.out" | sed 's/^/    /' | cut -c1-240
    [ "$arc" -eq 3 ] && { echo "REFUSING: API failure"; exit 3; }
    [ "$arc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the API does not show #$ROW open, unmerged, on develop at its head with the kit's file set"; exit 11; }
  done
  python3 "$GS/gh_gate77.py" census > "$OUTP.census.out" 2> "$OUTP.census.err"; crc=$?
  sed 's/^/    /' "$OUTP.census.out" | cut -c1-240; echo "  census rc=$crc (REPORTED, not refused)"
fi

echo "--- 3b. develop: origin $CUR_DEV | --develop $DEV"
DEV_MOVED=0
if [ "$CUR_DEV" = "$DEV" ]; then echo "  UNMOVED (== the draft develop: the kit's predicted chain applies)."
  [ -z "$REPIN" ] || [ "$REPIN" = "$CUR_DEV" ] || { echo "REFUSING TO LAUNCH: --repin-develop $REPIN is not origin develop $CUR_DEV (stale re-pin)"; exit 10; }
else DEV_MOVED=1; echo "  DEVELOP MOVED: $DEV -> $CUR_DEV (3c reads WHAT moved: c1 P7 per row, then the chain is RE-PREDICTED)"; fi

echo "--- 3c. the kit's own clone: fetch by sha if absent, c1 --all, c2 clean + collide, the chain prediction"
if [ ! -d "$CL/.git" ] && [ ! -f "$CL/HEAD" ]; then
  mkdir -p "$GS/_scratch"; env -u GIT_SSH_COMMAND git clone --shared --no-checkout --quiet "$CHECKOUT" "$CL" > "$OUTP.clone.out" 2> "$OUTP.clone.err" || { echo "REFUSING: kit clone failed"; exit 13; }
fi
git -C "$CL" config remote.origin.url "$URL"
git -C "$CL" config core.sshCommand "$(git -C "$CHECKOUT" config --get core.sshCommand)"
for s in $H1429 $H1430 $H1431 $H1432 $H1433 $H1434 $H1436 "$(KJ rows.1436.base)" "$(KJ rows.1436.pre_merge_base)" "$(KJ develop_at_draft)" "$P27" "$CUR_DEV" "$(KJ raise_base)" "$(KJ trailer_control)" "$(KJ merge_tree_control.ours)" "$(KJ merge_tree_control.theirs)"; do
  git -C "$CL" cat-file -e "$s^{commit}" 2>/dev/null || env -u GIT_SSH_COMMAND git -C "$CL" fetch --quiet --no-tags --no-write-fetch-head origin "$s" >> "$OUTP.fetch.out" 2>> "$OUTP.fetch.err"
  git -C "$CL" cat-file -e "$s^{commit}" 2>/dev/null || { echo "REFUSING: $s is ABSENT from the kit clone after a by-sha fetch"; tail -3 "$OUTP.fetch.err" 2>/dev/null; exit 19; }
done
python3 "$GS/c1_pin_gate77.py" --all --repo "$CL" --develop "$CUR_DEV" > "$OUTP.c1.out" 2> "$OUTP.c1.err"; rc1=$?
echo "  c1 --all rc=$rc1 | $(grep -E '^(CHECKED|[0-9]+ FAIL)' "$OUTP.c1.out" | tr '\n' ' ')"; grep -E '^FAIL' "$OUTP.c1.out" | sed 's/^/    /' | cut -c1-240
[ "$rc1" -eq 0 ] || { echo "REFUSING TO LAUNCH: C1 FAILED (a pin moved, or develop moved a row's CODE path: P7 = RE-GATE that row)"; exit 13; }
for m in clean collide; do
  python3 "$GS/c2_merge_gate77.py" $m --repo "$CL" --develop "$CUR_DEV" > "$OUTP.c2$m.out" 2> "$OUTP.c2$m.err"; r=$?
  echo "  c2 $m rc=$r | $(grep -E '^(CHECKED|[0-9]+ FAIL)' "$OUTP.c2$m.out" | tr '\n' ' ')"; grep -E '^FAIL' "$OUTP.c2$m.out" | sed 's/^/    /' | cut -c1-240
  [ "$r" -eq 0 ] || { echo "REFUSING TO LAUNCH: c2 $m FAILED (read $OUTP.c2$m.out)"; exit 13; }
done
# #1427 lands first when develop does not yet carry it: its job-04 blob at develop decides (never the sha)
_J='Blockchain/Testing/jobs/04-container-trivy.sh'
if [ "$(git -C "$CL" ls-tree "$CUR_DEV" -- "$_J" | awk '{print $3}')" = "$(git -C "$CL" ls-tree "$P27" -- "$_J" | awk '{print $3}')" ]; then
  EFF="$ORDER"; PEND="LANDED on develop $(printf '%.12s' "$CUR_DEV") (its job-04 blob is on develop): it is NOT a chain step"
else EFF="1427,$ORDER"; PEND="NOT YET LANDED at launch: the chain models it as step 1 (gate76 GO 2). If it lands mid-gate, read the advance with c1 P7 and re-run the chain"; fi
mkdir -p "$OUTP.chain"   # a fresh timestamped dir; nothing is ever deleted (Kam 2026-08-26: quarantine, never delete)
python3 "$GS/c2_merge_gate77.py" chain --repo "$CL" --develop "$CUR_DEV" --order "$EFF" --out "$OUTP.chain" > "$OUTP.c2chain.out" 2> "$OUTP.c2chain.err"; rcq=$?
grep -E '^(STEP|FINAL|FAIL|CHAIN)' "$OUTP.c2chain.out" | sed 's/^/    /' | cut -c1-200; echo "  c2 chain (order $EFF) rc=$rcq"
[ "$rcq" -eq 0 ] || { echo "REFUSING TO LAUNCH: the chain onto develop $CUR_DEV is NOT predicted (read $OUTP.c2chain.out). A moved CODE path is a RE-GATE; never --no-verify."; exit 13; }
FINAL="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["final_tree"])' "$OUTP.chain/chain.json")"
# (2026-10-09, seven rows) origin develop is already 81d2e5f4c415, a descendant of develop_at_draft, so DEV_MOVED=0 cannot recur; were it
# reached, the chain above already refused rc 13 (c2 BASE-CONTAINED: #1436 carries 81d2e5f4c415). The 7-row predictions are kit predicted_chain7_*.
if [ "$DEV_MOVED" = 0 ]; then
  _W="$(KJ predicted_chain_with1427.final_tree)"
  [ "$FINAL" = "$_W" ] || { echo "REFUSING TO LAUNCH: at the draft develop the chain's final tree $FINAL != kit.json predicted $_W"; exit 13; }
  echo "  at the draft develop the chain == kit.json predicted_chain_with1427 (final ${_W:0:12})"
else
  if [ -z "$REPIN" ]; then echo "REFUSING TO LAUNCH: develop moved (c1 P7: no row CODE path touched; the chain is RE-PREDICTED above: final tree $FINAL). To re-pin and launch over it, re-run with:  --repin-develop $CUR_DEV"; exit 10
  elif [ "$REPIN" != "$CUR_DEV" ]; then echo "REFUSING TO LAUNCH: --repin-develop $REPIN is not origin develop $CUR_DEV (stale re-pin)"; exit 10; fi
  echo "repin $(date -u +%Y-%m-%dT%H:%M:%SZ): develop $DEV -> $CUR_DEV; order $EFF; final tree $FINAL" > "$OUTP.repin.txt"; echo "  RE-PINNED develop -> $CUR_DEV ($OUTP.repin.txt)"
fi

echo "--- S. the Actions comparator and the merge seat must be ruled (kit.json)"
COMP="$(KJ actions_comparator)"; SEAT="$(KJ merge_seat_ordinal)"
if [ -z "$COMP" ] || [ -z "$SEAT" ]; then
  if [ "$DRY" = 1 ]; then echo "  (DRY RUN: REPORTED, not refused — comparator '$COMP' / merge seat '$SEAT'; a real run refuses rc 8)"; COMP="${COMP:-UNRULED}"; SEAT="${SEAT:-UNRULED}"
  else echo "REFUSING TO LAUNCH: RULING NEEDED — kit.json actions_comparator / merge_seat_ordinal is null"; exit 8; fi
else echo "  comparator: $COMP | merge seat: $SEAT ($(KJ merge_seat))"; fi

echo "--- R. render the prompt (seven heads, develop $CUR_DEV, merge seat $SEAT, comparator $COMP, order $EFF, final tree $FINAL)"
python3 - "$GS/prompt_gate77.txt" "$GS/prompt_gate77.rendered.txt" "$GS/head_at_launch.txt" "$KITJSON" "$CUR_DEV" "$SEAT" "$FINAL" "$COMP" "$EFF" "$PEND" "$H1429" "$H1430" "$H1431" "$H1432" "$H1433" "$H1434" "$H1436" <<'PYEOF' || { echo "REFUSING: render failed"; exit 9; }
import json, sys
src, dst, hf, kj, dev, seat, final, comp, order, pend = sys.argv[1:11]; heads = dict(zip(['1429', '1430', '1431', '1432', '1433', '1434', '1436'], sys.argv[11:18]))
if len(heads) != 7 or any(len(h) != 40 for h in heads.values()): raise SystemExit('render: seven 40-hex heads required, got %r' % heads)
K = json.load(open(kj)); t = open(src, encoding='utf-8').read()
need = {'{{DEVELOP}}': 3, '{{MERGE_SEAT}}': 7, '{{PREDICTED_FINAL_TREE}}': 1, '{{COMPARATOR}}': 2, '{{ORDER}}': 3, '{{PENDING_1427}}': 1}
need.update({'{{HEAD_%s}}' % n: 1 for n in heads})
low = ['%s x%d' % (k, t.count(k)) for k, n in need.items() if t.count(k) < n]
if low: raise SystemExit('template tokens below their floor: %s' % low)
for k, v in [('{{DEVELOP}}', dev), ('{{MERGE_SEAT}}', seat), ('{{PREDICTED_FINAL_TREE}}', final), ('{{COMPARATOR}}', comp), ('{{ORDER}}', order),
             ('{{PENDING_1427}}', pend)] + [('{{HEAD_%s}}' % n, h) for n, h in heads.items()]:
    t = t.replace(k, v)
if '{{' in t: raise SystemExit('an unknown {{token}} survived the render')
open(dst, 'w', encoding='utf-8').write(t)
lines = ['P %s %s %s %s' % (n, K['rows'][n]['branch'], h, K['rows'][n]['end_tree']) for n, h in heads.items()]
lines += ['B %s 1' % K['raise_base'], 'D %s' % dev, 'S %s' % seat, 'C %s' % comp, 'O %s' % order, 'T %s' % final, 'Q %s' % pend]
open(hf, 'w').write('\n'.join(lines) + '\n')
print('  rendered -> %s (%d bytes); head file %s (P x7 / B / D / S / C / O / T / Q)' % (dst, len(t.encode()), hf))
PYEOF

echo "--- 0. routing: the pane must be in inbox_routing.conf"
/usr/bin/grep -c -x -F "$LINE" "$ROUTING" > "$OUTP.routing.out" 2> "$OUTP.routing.err"; rc=$?
echo "  $ROUTING — exact line present: $(cat "$OUTP.routing.out") (grep rc=$rc; want 1 / rc 0). CONTROL: agentmail lines in the file = $(/usr/bin/grep -c -i 'agentmail' "$ROUTING")"
if [ "$rc" -ne 0 ]; then
  if [ "$DRY" = 1 ]; then echo "  (DRY RUN: reported, not refused — the real run refuses rc 1; ROUTING_LINE.txt)"; else echo "REFUSING: add the routing line first (ROUTING_LINE.txt): $LINE"; exit 1; fi
fi

echo "--- 5. usage at the DEFAULT stop ($(KJ usage_stop_default)%; no override: the gate76 grant expired at the account renewal)"
unset WED_USAGE_STOP
"$(KJ usage_gate)" --check > "$OUTP.usage_gate.out" 2> "$OUTP.usage_gate.err"; rc=$?
sed 's/^/    /' "$OUTP.usage_gate.out" "$OUTP.usage_gate.err"; echo "  usage_gate --check rc=$rc"
if [ "$rc" -ne 0 ]; then
  if [ "$DRY" = 1 ]; then echo "  (DRY RUN: reported — a real run refuses rc 12)"; else echo "REFUSING TO LAUNCH: the usage gate refused at the default stop (no override without a new recorded grant from Kam)"; exit 12; fi
fi

if [ "$DRY" = 1 ]; then
  echo "--- 6 (dry). the launcher's own --check"
  # a dry run's ls-remote stand-in (if any) is handed to the launcher's own re-read too, so both read the SAME origin state
  if [ -n "${GATE77_LSFILE:-}" ]; then GATE77_LS="$GATE77_LSFILE" GATE77_KITJSON="$KITJSON" "$L" --check > "$OUTP.launcher_check.out" 2> "$OUTP.launcher_check.err"; rc=$?
  else GATE77_KITJSON="$KITJSON" "$L" --check > "$OUTP.launcher_check.out" 2> "$OUTP.launcher_check.err"; rc=$?; fi
  sed 's/^/    /' "$OUTP.launcher_check.out" "$OUTP.launcher_check.err"; echo "  launcher --check rc=$rc"
  [ "$rc" -eq 0 ] || { echo "DRY RUN: the launcher refused under --check (rc $rc)"; exit 13; }
  echo "DRY RUN COMPLETE $(date -u '+%Y-%m-%dT%H:%M:%SZ') — develop $CUR_DEV; the real run continues with the override check, --check and cockpit.sh add"; exit 0
fi
echo "--- 4. no test override on a real launch"
[ "$(env | grep -c '^GATE77_')" = 0 ] || { echo "REFUSING TO LAUNCH: a GATE77_* override is set"; exit 16; }
echo "--- 6. the launcher's own --check"
"$L" --check > "$OUTP.launcher_check.out" 2> "$OUTP.launcher_check.err"; rc=$?
sed 's/^/    /' "$OUTP.launcher_check.out" "$OUTP.launcher_check.err"; echo "  launcher --check rc=$rc"
[ "$rc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the launcher refused under --check"; exit 13; }
echo "--- 7. cockpit.sh add (the fleet's own tooling, never raw send-keys)"
"$(KJ cockpit)" add "$PANE" "$L" > "$OUTP.cockpit_add.out" 2> "$OUTP.cockpit_add.err"; rc=$?
sed 's/^/    /' "$OUTP.cockpit_add.out" "$OUTP.cockpit_add.err"; echo "  cockpit.sh add rc=$rc"
[ "$rc" -eq 0 ] || { echo "LAUNCH FAILED at cockpit.sh add (STOP and tell Wednesday, never retry blind)"; exit 14; }
echo "--- pane census"
/opt/homebrew/bin/tmux list-panes -a -F '#{pane_id} | #{@cockpit_name} | #{pane_current_command} | #{session_name}:#{window_index}.#{pane_index}'
echo "LAUNCHED $(date -u '+%Y-%m-%dT%H:%M:%SZ'); develop at launch $CUR_DEV — now verify RUNG 5 (KIT_REPORT §7)"
