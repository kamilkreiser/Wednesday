#!/bin/bash
# repin_and_launch_gate71.sh — the LAUNCH ACTION for gate71, WIDENED 2026-10-07 to TWO ROWS in merge order: #1404 (KS-1436, T2, job 06
# stderr to its own file; #1398's MERGE CONDITION) then #1398 (KS-1136, T1). The pre-widen file is _superseded_2026-10-07/kit_pre_widen/.
# It READS everything at launch and never trusts a pin it did not just re-read (Kam 2026-09-18):
#   (A)  each row's READY must name its head in full and name its #pr                                                       — rc 18
#        a head != the kit's expected head refuses unless --accept-unexpected-head (then every drafter figure is VOID)    — rc 11
#   (2)  ONE `git ls-remote` of develop + both rows' refs/pull/<n>/head and branches, from the Secuura checkout: GIT_SSH_COMMAND UNSET,
#        `-c core.sshCommand=<the checkout's own>`, the github URL (read verb)                                            — rc 2
#        input == pull/head == branch for EACH row, else MISMATCH (a MOVED HEAD, named)                                   — rc 11
#   (1)  gh_gate71.py api per row (rc 3 API failure; rc 11 not open / not on develop / head differs) + census once
#        (OVERLAP / DOCS printed, not refused). `--no-api` skips both ONLY with --dry-run (no drafter holds a GitHub identity).
#   (3b) develop: == kit develop_at_draft (b39051390ff6) -> on; MOVED -> rc 10 unless `--repin-develop <that 40-hex>`
#   (3c) THE KIT'S OWN CLONE (<kit>/_scratch/clone, origin = the GitHub URL, the checkout's core.sshCommand, NEVER an exported
#        GIT_SSH_COMMAND): fetch heads / develop / base BY SHA only if absent; any still absent is REFUSED BY NAME — rc 19;
#        c1 --no-remote must pass for BOTH rows (rc 13: a moved develop that touched a code path / unaccepted tooling fails P10/P12);
#        c2 guard (#1398) + c5 guard06 (#1404) + c4 targets on the develop read now (the re-composed merge-in chain, the guard run
#        itself, merge-tree as a never-picked cross-check). On the KIT develop the targets must equal kit.json targets — rc 13 if not.
#   (R)  render prompt_gate71.txt -> prompt_gate71.rendered.txt ({{HEAD_1404}} {{HEAD_1398}} {{DEVELOP}}) + head_at_launch.txt   — rc 9
#   (0)  the pane is routed in inbox_routing.conf — rc 1 (a dry run REPORTS it instead)
#   (4)  G71_* overrides refuse a real launch — rc 16;  (5) the usage gate — rc 12;  (6) the launcher's --check — rc 13;  (7) cockpit add — rc 14
# --dry-run: A, 2, 1 (or --no-api), 3b, 3c, R, 0 and the launcher's --check, then stops. Output: launch_<HHMMSS>.* (dry: dry_<HHMMSS>.*).
# Controls-only overrides (DRY RUN ONLY): G71_ROUTING (routing stand-in), G71_LSFILE (ls-remote stand-in).
# Usage: repin_and_launch_gate71.sh 1404:<HEAD 40-hex> 1398:<HEAD 40-hex> [--dry-run [--no-api]] [--repin-develop <40-hex>] [--accept-unexpected-head]
#        (run under `script -q /dev/null`)
set -u
export PYTHONDONTWRITEBYTECODE=1
GS="$(dirname "$(/bin/realpath "$0")")"
CHECKOUT='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
KJ() { python3 -c 'import json,sys; v=json.load(open(sys.argv[1]))
for k in sys.argv[2].split("."): v=v[k]
print(" ".join(v) if isinstance(v,list) else ("" if v is None else v))' "$GS/kit.json" "$1"; }
ROUTING="${G71_ROUTING:-$(KJ routing)}"; KDEV="$(KJ develop_at_draft)"; PANE="$(KJ pane)"; LINE="$(KJ routing_line)"; URL="$(KJ github_url)"
BASE="$(KJ rows.1398.parents)"; [ "$BASE" = "$(KJ rows.1404.parents)" ] || { echo "REFUSING: the two rows do not share one base in kit.json"; exit 9; }
L="$GS/$(KJ launcher)"; CL="$GS/_scratch/clone"
USAGE="usage: repin_and_launch_gate71.sh 1404:<HEAD 40-hex> 1398:<HEAD 40-hex> [--dry-run [--no-api]] [--repin-develop <40-hex>] [--accept-unexpected-head]"
H_1404=""; H_1398=""; DRY=0; NOAPI=0; REPIN=""; ACCEPT=0
while [ $# -gt 0 ]; do
  case "$1" in 1404:*) H_1404="${1#1404:}"; shift;; 1398:*) H_1398="${1#1398:}"; shift;;
    --dry-run) DRY=1; shift;; --no-api) NOAPI=1; shift;; --accept-unexpected-head) ACCEPT=1; shift;;
    --repin-develop) REPIN="${2:-}"; shift 2 2>/dev/null || shift;; *) echo "$USAGE"; exit 9;; esac
done
for _r in 1404 1398; do
  eval "_h=\$H_$_r"
  printf '%s' "$_h" | grep -qE '^[0-9a-f]{40}$' || { echo "REFUSING: $_r:<HEAD> must be the FULL 40-hex sha, got '$_h'"; echo "$USAGE"; exit 9; }
done
[ -z "$REPIN" ] || printf '%s' "$REPIN" | grep -qE '^[0-9a-f]{40}$' || { echo "REFUSING: --repin-develop must be the FULL 40-hex sha, got '$REPIN'"; exit 9; }
[ "$NOAPI" = 0 ] || [ "$DRY" = 1 ] || { echo "REFUSING: --no-api is a dry-run option only (a real launch reads the PR API)"; exit 9; }
T="$(date -u +%H%M%S)"; OUTP="$GS/launch_$T"; [ "$DRY" = 1 ] && OUTP="$GS/dry_$T"
echo "LAUNCH ACTION gate71 (WIDENED: #1404 then #1398)$([ "$DRY" = 1 ] && echo ' (DRY RUN)') $(date '+%Y-%m-%d %H:%M:%S %Z') / $(date -u '+%Y-%m-%dT%H:%M:%SZ') | #1404 $H_1404 | #1398 $H_1398 | kit develop $KDEV | repin-develop ${REPIN:-none} | pane $PANE"

echo "--- A. each head must be the one its READY names"
for _r in 1404 1398; do
  eval "_h=\$H_$_r"; READY="$(KJ rows.$_r.ready)"; H_EXP="$(KJ rows.$_r.head_expected)"
  [ -s "$READY" ] || { echo "REFUSING: #$_r READY missing or empty ('$READY')"; exit 18; }
  _n="$(/usr/bin/grep -c -F "$_h" "$READY")"; _p="$(/usr/bin/grep -c -F "#$_r" "$READY")"; _c="$(/usr/bin/grep -c -i 'READY' "$READY")"
  echo "  #$_r $READY (sha256/16 $(shasum -a 256 "$READY" | cut -c1-16)): lines naming the head in full $_n | naming #$_r $_p | CONTROL lines naming 'READY' $_c"
  [ "$_n" -ge 1 ] && [ "$_p" -ge 1 ] || { echo "REFUSING: the #$_r READY does not name $_h in full (or #$_r)"; exit 18; }
  if [ "$_h" != "$H_EXP" ]; then
    if [ "$ACCEPT" = 1 ]; then echo "  WARNING: #$_r head $_h != kit expected $H_EXP — accepted: EVERY drafter figure for #$_r is VOID"
    else echo "REFUSING: #$_r head $_h != kit expected $H_EXP (the drafter's figures are for $H_EXP). Re-draft, or pass --accept-unexpected-head"; exit 11; fi
  fi
done

echo "--- 2. ONE ls-remote (read verb) from the checkout, GIT_SSH_COMMAND unset, the checkout's own core.sshCommand"
[ -z "${GIT_SSH_COMMAND:-}" ] || echo "  NOTE: GIT_SSH_COMMAND is exported in this shell; every git call below runs under env -u GIT_SSH_COMMAND"
B_1404="$(KJ rows.1404.branch)"; B_1398="$(KJ rows.1398.branch)"
REFS="refs/heads/develop refs/pull/1404/head refs/heads/$B_1404 refs/pull/1398/head refs/heads/$B_1398"
if [ -n "${G71_LSFILE:-}" ]; then
  [ "$DRY" = 1 ] || { echo "REFUSING: G71_LSFILE is a dry-run control only"; exit 16; }
  cp "$G71_LSFILE" "$OUTP.lsremote.out"; : > "$OUTP.lsremote.err"; rc=0; echo "  (CONTROL: ls-remote output read from the stand-in $G71_LSFILE)"
else
  env -u GIT_SSH_COMMAND git -C "$CHECKOUT" -c core.sshCommand="$(git -C "$CHECKOUT" config --get core.sshCommand)" ls-remote "$URL" $REFS > "$OUTP.lsremote.out" 2> "$OUTP.lsremote.err"; rc=$?
fi
get() { awk -v r="$1" '$2==r{print $1}' "$OUTP.lsremote.out"; }
CUR_DEV="$(get refs/heads/develop)"
echo "  ls-remote rc=$rc at $(date -u +%H:%M:%SZ) | develop $CUR_DEV | #1404 pull/head $(get refs/pull/1404/head) branch $(get "refs/heads/$B_1404") | #1398 pull/head $(get refs/pull/1398/head) branch $(get "refs/heads/$B_1398")"
[ "$rc" -eq 0 ] && [ -n "$CUR_DEV" ] || { echo "REFUSING: ls-remote failed or returned no develop"; sed 's/^/    stderr: /' "$OUTP.lsremote.err"; exit 2; }
for _r in 1404 1398; do
  eval "_h=\$H_$_r; _b=\$B_$_r"
  [ "$(get "refs/pull/$_r/head")" = "$_h" ] && [ "$(get "refs/heads/$_b")" = "$_h" ] || { echo "REFUSING TO LAUNCH: #$_r origin pull/head '$(get "refs/pull/$_r/head")' / branch '$(get "refs/heads/$_b")' != the input head $_h — MISMATCH (the #$_r HEAD MOVED)"; exit 11; }
done

echo "--- 1. PULLS API (per row) + census"
if [ "$NOAPI" = 1 ]; then
  echo "  API NOT READ (--no-api, dry run only): the drafter holds no GitHub identity. A real launch reads it and refuses on any disagreement."
else
  for _r in 1404 1398; do
    eval "_h=\$H_$_r; _b=\$B_$_r"
    python3 "$GS/gh_gate71.py" api --pr "$_r" --head "$_h" > "$OUTP.api_$_r.out" 2> "$OUTP.api_$_r.err"; arc=$?
    sed 's/^/    /' "$OUTP.api_$_r.out" "$OUTP.api_$_r.err" | cut -c1-240; echo "  #$_r api rc=$arc"
    [ "$arc" -eq 3 ] && { echo "REFUSING: API failure (#$_r)"; exit 3; }
    A_LINE="$(grep '^API #' "$OUTP.api_$_r.out")"; set -- $A_LINE
    [ "${4:-}" = "$_h" ] && [ "${6:-}" = "$_b" ] && [ "${8:-}" = develop ] && [ "${10:-}" = open ] && [ "${12:-}" = False ] || { echo "REFUSING TO LAUNCH: the API does not show #$_r open, unmerged, on develop at $_h: '$A_LINE'"; exit 11; }
    set --
  done
  python3 "$GS/gh_gate71.py" census --pr 1398 > "$OUTP.census.out" 2> "$OUTP.census.err"; crc=$?
  sed 's/^/    /' "$OUTP.census.out" "$OUTP.census.err" | cut -c1-240
  echo "  census rc=$crc (census rc 1 = OVERLAP printed above: REPORTED, not refused)"
  [ "$crc" -eq 3 ] && { echo "REFUSING: a BLIND census control"; exit 3; }
  echo "  ALL INSTRUMENTS AGREE with both input heads."
fi

echo "--- 3b. develop: origin $CUR_DEV | kit (at widening) $KDEV"
DEV_MOVED=0
if [ "$CUR_DEV" = "$KDEV" ]; then echo "  UNMOVED since the widening (the kit's target trees apply as pinned)."
  [ -z "$REPIN" ] || [ "$REPIN" = "$CUR_DEV" ] || { echo "REFUSING TO LAUNCH: --repin-develop $REPIN is not origin develop $CUR_DEV (stale re-pin)"; exit 10; }
else DEV_MOVED=1; echo "  DEVELOP MOVED: $KDEV -> $CUR_DEV  (3c checks descent, the code paths / tooling, and re-predicts the docs merge-in chain)"; fi

echo "--- 3c. the kit's own clone: fetch by sha if absent, refuse by name if still absent, C1 x2 + guards + the merge-in chain"
if [ ! -d "$CL/.git" ] && [ ! -f "$CL/HEAD" ]; then
  mkdir -p "$GS/_scratch"; env -u GIT_SSH_COMMAND git clone --shared --no-checkout --quiet "$CHECKOUT" "$CL" > "$OUTP.clone.out" 2> "$OUTP.clone.err" || { echo "REFUSING: kit clone failed"; exit 13; }
  git -C "$CL" config remote.origin.url "$URL"
  git -C "$CL" config core.sshCommand "$(git -C "$CHECKOUT" config --get core.sshCommand)"
fi
echo "  kit clone origin: $(git -C "$CL" config --get remote.origin.url) (must be the GitHub URL, never the local checkout)"
for pair in "head 1404:$H_1404" "head 1398:$H_1398" "develop:$CUR_DEV" "base:$BASE"; do
  n="${pair%%:*}"; s="${pair#*:}"
  if ! git -C "$CL" cat-file -e "$s^{commit}" 2>/dev/null; then
    echo "  $n $s absent from the kit clone: fetch BY SHA from $URL"
    env -u GIT_SSH_COMMAND git -C "$CL" fetch --quiet --no-tags --no-write-fetch-head origin "$s" >> "$OUTP.fetch.out" 2>> "$OUTP.fetch.err"
  fi
  git -C "$CL" cat-file -e "$s^{commit}" 2>/dev/null || { echo "REFUSING BY NAME: the $n $s is ABSENT from the kit clone after a by-sha fetch (see $OUTP.fetch.err)"; exit 19; }
  echo "  $n ${s:0:12} PRESENT"
done
for _r in 1404 1398; do
  eval "_h=\$H_$_r"
  python3 "$GS/c1_pin_gate71.py" --pr "$_r" --repo "$CL" --head "$_h" --develop "$CUR_DEV" --no-remote > "$OUTP.c1_$_r.out" 2> "$OUTP.c1_$_r.err"; rc1=$?
  echo "  c1 #$_r rc=$rc1 | $(grep -E '^(CHECKED|[0-9]+ FAIL)' "$OUTP.c1_$_r.out" | tr '\n' ' ')"; grep -E '^(FAIL|INFO P12[ad])' "$OUTP.c1_$_r.out" | sed 's/^/    /' | cut -c1-240
  [ "$rc1" -eq 0 ] || { echo "REFUSING TO LAUNCH: C1 FAILED for #$_r (a moved develop that touched a code path / an unaccepted tooling path fails P10/P12 here: RE-GATE)"; exit 13; }
done
python3 "$GS/c2_product_gate71.py" guard --pr 1398 --repo "$CL" --head "$H_1398" > "$OUTP.c2guard.out" 2> "$OUTP.c2guard.err"; rcg=$?
python3 "$GS/c5_job06_gate71.py" guard06 --pr 1404 --repo "$CL" --head "$H_1404" --head-1398 "$H_1398" > "$OUTP.c5guard06.out" 2> "$OUTP.c5guard06.err"; rc5=$?
mkdir -p "$OUTP.targets.d"
python3 "$GS/c4_docs_gate71.py" targets --pr 1404 --repo "$CL" --develop-after "$CUR_DEV" --out "$OUTP.targets.d/run" > "$OUTP.c4targets.out" 2> "$OUTP.c4targets.err"; rct=$?
echo "  c2 guard (#1398) rc=$rcg | c5 guard06 (#1404) rc=$rc5 | c4 targets rc=$rct (PREDICTIONS for the gate)"
grep -hE '^(FAIL|PASS T|CROSS-CHECK|REFUSED)' "$OUTP.c2guard.out" "$OUTP.c5guard06.out" "$OUTP.c4targets.out" | sed 's/^/    /' | cut -c1-260
_TJ="$OUTP.targets.d/run/targets.json"
if [ "$DEV_MOVED" = 0 ]; then
  python3 - "$_TJ" "$GS/kit.json" > "$OUTP.targets_vs_kit.out" 2>&1 <<'PYEOF'
import json, sys
t = json.load(open(sys.argv[1])); k = json.load(open(sys.argv[2]))['targets']
a, b = t.get('target_1404'), t.get('target_1398')
ok = a == k['1404']['tree'] and b == k['1398']['tree']
print('  targets on the KIT develop: #1404 %s (kit %s) | #1398 %s (kit %s) -> %s' % (a, k['1404']['tree'], b, k['1398']['tree'], 'EQUAL' if ok else 'DIFFER'))
sys.exit(0 if ok else 1)
PYEOF
  rtk=$?; cat "$OUTP.targets_vs_kit.out"
  [ "$rct" -eq 0 ] && [ "$rtk" -eq 0 ] || { echo "REFUSING TO LAUNCH: on the kit develop the merge-in chain must reproduce kit.json targets (c4 targets rc $rct, compare rc $rtk)"; exit 13; }
else
  [ "$rct" -eq 0 ] || { echo "REFUSING TO LAUNCH: the merge-in chain could not be predicted on the moved develop $CUR_DEV (c4 targets rc $rct): RE-DRAFT"; exit 13; }
  if [ -z "$REPIN" ]; then echo "REFUSING TO LAUNCH: develop moved (c1 says it touched no code path / unaccepted tooling; the re-predicted chain is above). To re-pin and launch over it, re-run with:  --repin-develop $CUR_DEV"; exit 10
  elif [ "$REPIN" != "$CUR_DEV" ]; then echo "REFUSING TO LAUNCH: --repin-develop $REPIN is not origin develop $CUR_DEV (stale re-pin)"; exit 10; fi
  echo "repin $(date -u +%Y-%m-%dT%H:%M:%SZ): develop $KDEV -> $CUR_DEV (kit targets VOID; the gate re-derives them)" > "$OUTP.repin.txt"; echo "  RE-PINNED develop -> $CUR_DEV ($OUTP.repin.txt)"
fi

echo "--- R. render the prompt (#1404 $H_1404, #1398 $H_1398, develop $CUR_DEV)"
python3 - "$GS/prompt_gate71.txt" "$GS/prompt_gate71.rendered.txt" "$GS/head_at_launch.txt" "$H_1404" "$B_1404" "$H_1398" "$B_1398" "$CUR_DEV" <<'PYEOF' || { echo "REFUSING: render failed"; exit 9; }
import sys
src, dst, hf, h4, b4, h8, b8, dev = sys.argv[1:9]
t = open(src, encoding='utf-8').read()
n4, n8, nd = t.count('{{HEAD_1404}}'), t.count('{{HEAD_1398}}'), t.count('{{DEVELOP}}')
if n4 < 5 or n8 < 5 or nd < 1: raise SystemExit('template tokens HEAD_1404 x%d HEAD_1398 x%d DEVELOP x%d (want >= 5 / >= 5 / >= 1)' % (n4, n8, nd))
t = t.replace('{{HEAD_1404}}', h4).replace('{{HEAD_1398}}', h8).replace('{{DEVELOP}}', dev)
if '{{' in t: raise SystemExit('an unknown {{token}} survived the render')
open(dst, 'w', encoding='utf-8').write(t)
open(hf, 'w').write('P 1404 %s %s\nP 1398 %s %s\nD %s\n' % (b4, h4, b8, h8, dev))
print('  rendered HEAD_1404 x%d HEAD_1398 x%d DEVELOP x%d -> %s (%d bytes); head file %s' % (n4, n8, nd, dst, len(t.encode()), hf))
PYEOF

echo "--- 0. routing: the pane must be in inbox_routing.conf"
/usr/bin/grep -c -x -F "$LINE" "$ROUTING" > "$OUTP.routing.out" 2> "$OUTP.routing.err"; rc=$?
echo "  $ROUTING — exact line present: $(cat "$OUTP.routing.out") (grep rc=$rc; want 1 / rc 0). CONTROL: agentmail lines in the file = $(/usr/bin/grep -c -i 'agentmail' "$ROUTING")"
if [ "$rc" -ne 0 ]; then
  if [ "$DRY" = 1 ]; then echo "  (DRY RUN: reported, not refused — the real run refuses rc 1; ROUTING_LINE.txt)"; else echo "REFUSING: add the routing line first (ROUTING_LINE.txt): $LINE"; exit 1; fi
fi

if [ "$DRY" = 1 ]; then
  echo "--- 6 (dry). the launcher's own --check"
  "$L" --check > "$OUTP.launcher_check.out" 2> "$OUTP.launcher_check.err"; rc=$?
  sed 's/^/    /' "$OUTP.launcher_check.out" "$OUTP.launcher_check.err"; echo "  launcher --check rc=$rc"
  [ "$rc" -eq 0 ] || { echo "DRY RUN: the launcher refused under --check (rc $rc)"; exit 13; }
  echo "DRY RUN COMPLETE $(date -u '+%Y-%m-%dT%H:%M:%SZ') — #1404 $H_1404, #1398 $H_1398, develop $CUR_DEV; the real run continues with the API, the override check, the usage gate, --check and cockpit.sh add"; exit 0
fi
echo "--- 4. no test override on a real launch"
[ "$(env | grep -c '^G71_')" = 0 ] || { echo "REFUSING TO LAUNCH: a G71_* override is set"; exit 16; }
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
echo "LAUNCHED $(date -u '+%Y-%m-%dT%H:%M:%SZ') #1404 at $H_1404 + #1398 at $H_1398; develop at launch $CUR_DEV — now verify RUNG 5 (README §8)"
