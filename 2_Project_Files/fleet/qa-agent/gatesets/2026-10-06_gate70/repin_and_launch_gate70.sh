#!/bin/bash
# repin_and_launch_gate70.sh — the LAUNCH ACTION for gate70 (T1, round 1 of 2: #1397 KS-1425 lock-only refresh + 2 baseline rows).
# Adapted from repin_and_launch_gate69.sh, with the doc merge-in machinery REMOVED (this PR touches 0 docs).
# It READS everything at launch and never trusts a pin it did not just re-read (Kam 2026-09-18):
#   (A)  the READY must name the head in full and name #1397                                                              — rc 18
#        a head != the kit's expected head refuses unless --accept-unexpected-head (then every drafter figure is VOID)    — rc 11
#   (2)  ONE `git ls-remote` of develop, refs/pull/1397/head and the branch, from the Secuura checkout: GIT_SSH_COMMAND UNSET,
#        `-c core.sshCommand=<the checkout's own>`, the github URL (read verb)                                            — rc 2
#   (3)  rc 11 unless input == READY == API head == pull/head == branch, and the PR is open, not merged, on develop
#   (3b) develop: == kit develop_at_draft (4eaf7741a6a4) -> on; MOVED -> rc 10 unless `--repin-develop <that 40-hex>`;
#        hard rc 13 (via c1 P2b / P12) if it does not descend from 4eaf or touches any of the 37 paths or the audit tooling
#   (R)  render prompt_gate70.txt -> prompt_gate70.rendered.txt ({{HEAD}} {{DEVELOP}}) + head_at_launch.txt              — rc 9
#   (0)  the pane is routed in inbox_routing.conf — rc 1 (a dry run REPORTS it instead)
#   (1)  gh_gate70.py api (rc 3 API failure) + census (rc 3 blind control; OVERLAP is PRINTED, not refused: the drafter measured
#        11 long-open lockfile PRs — Dependabot + #1360 — that overlap any lock refresh)
#   (3c) THE KIT'S OWN CLONE (<kit>/_scratch/clone, `clone --shared --no-checkout` of the checkout, origin + core.sshCommand copied,
#        NEVER an exported GIT_SSH_COMMAND): fetch head + develop BY SHA only if absent; c1 --no-remote must pass (rc 13);
#        c2 diff + c2 parse printed as the launch-time prediction (never refused: the gate rules)
#   (4)  G70_* overrides refuse a real launch — rc 16;  (5) the usage gate — rc 12;  (6) the launcher's --check — rc 13;  (7) cockpit add — rc 14
# --dry-run: A, 2, 3, 3b, R, 0, 1, 3c and the launcher's --check, then stops. Output: launch_<HHMMSS>.* (dry: dry_<HHMMSS>.*) beside this script.
# Controls-only overrides (DRY RUN ONLY): G70_ROUTING (routing stand-in), G70_LSFILE (ls-remote stand-in).
# Usage: repin_and_launch_gate70.sh <HEAD 40-hex> [--dry-run] [--repin-develop <40-hex>] [--accept-unexpected-head]   (run under `script -q /dev/null`)
set -u
export PYTHONDONTWRITEBYTECODE=1
GS="$(dirname "$(/bin/realpath "$0")")"
CHECKOUT='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
KJ() { python3 -c 'import json,sys; v=json.load(open(sys.argv[1]))
for k in sys.argv[2].split("."): v=v[k]
print(" ".join(v) if isinstance(v,list) else ("" if v is None else v))' "$GS/kit.json" "$1"; }
ROUTING="${G70_ROUTING:-$(KJ routing)}"; KDEV="$(KJ develop_at_draft)"; PANE="$(KJ pane)"; LINE="$(KJ routing_line)"; URL="$(KJ github_url)"
H_EXP="$(KJ pr.head_expected)"; BR="$(KJ pr.branch)"; READY="$(KJ pr.ready)"; PR="$(KJ pr.pr)"
L="$GS/$(KJ launcher)"; CL="$GS/_scratch/clone"
USAGE="usage: repin_and_launch_gate70.sh <HEAD 40-hex> [--dry-run] [--repin-develop <40-hex>] [--accept-unexpected-head]"
HD="${1:-}"; DRY=0; REPIN=""; ACCEPT=0
shift 1 2>/dev/null
while [ $# -gt 0 ]; do
  case "$1" in --dry-run) DRY=1; shift;; --accept-unexpected-head) ACCEPT=1; shift;; --repin-develop) REPIN="${2:-}"; shift 2 2>/dev/null || shift;;
    *) echo "$USAGE"; exit 9;; esac
done
printf '%s' "$HD" | grep -qE '^[0-9a-f]{40}$' || { echo "REFUSING: HEAD must be the FULL 40-hex sha, got '$HD'"; exit 9; }
[ -z "$REPIN" ] || printf '%s' "$REPIN" | grep -qE '^[0-9a-f]{40}$' || { echo "REFUSING: --repin-develop must be the FULL 40-hex sha, got '$REPIN'"; exit 9; }
T="$(date -u +%H%M%S)"; OUTP="$GS/launch_$T"; [ "$DRY" = 1 ] && OUTP="$GS/dry_$T"
echo "LAUNCH ACTION gate70$([ "$DRY" = 1 ] && echo ' (DRY RUN)') $(date '+%Y-%m-%d %H:%M:%S %Z') / $(date -u '+%Y-%m-%dT%H:%M:%SZ') | #$PR $HD | kit develop $KDEV | repin-develop ${REPIN:-none} | pane $PANE"

echo "--- A. the head must be the one the READY names"
[ -s "$READY" ] || { echo "REFUSING: READY missing or empty ('$READY')"; exit 18; }
_n="$(/usr/bin/grep -c -F "$HD" "$READY")"; _p="$(/usr/bin/grep -c -F "#$PR" "$READY")"; _c="$(/usr/bin/grep -c -i 'READY' "$READY")"
echo "  $READY (sha256/16 $(shasum -a 256 "$READY" | cut -c1-16)): lines naming the head in full $_n | naming #$PR $_p | CONTROL lines naming 'READY' $_c"
[ "$_n" -ge 1 ] && [ "$_p" -ge 1 ] || { echo "REFUSING: the READY does not name $HD in full (or #$PR)"; exit 18; }
if [ "$HD" != "$H_EXP" ]; then
  if [ "$ACCEPT" = 1 ]; then echo "  WARNING: head $HD != kit expected $H_EXP — accepted: EVERY drafter figure is VOID"
  else echo "REFUSING: head $HD != kit expected $H_EXP (the drafter's figures are for $H_EXP). Re-draft, or pass --accept-unexpected-head"; exit 11; fi
fi

echo "--- 2. ONE ls-remote (read verb) from the checkout, GIT_SSH_COMMAND unset, the checkout's own core.sshCommand"
[ -z "${GIT_SSH_COMMAND:-}" ] || echo "  NOTE: GIT_SSH_COMMAND is exported in this shell; every git call below runs under env -u GIT_SSH_COMMAND"
REFS="refs/heads/develop refs/pull/$PR/head refs/heads/$BR"
if [ -n "${G70_LSFILE:-}" ]; then
  [ "$DRY" = 1 ] || { echo "REFUSING: G70_LSFILE is a dry-run control only"; exit 16; }
  cp "$G70_LSFILE" "$OUTP.lsremote.out"; : > "$OUTP.lsremote.err"; rc=0; echo "  (CONTROL: ls-remote output read from the stand-in $G70_LSFILE)"
else
  env -u GIT_SSH_COMMAND git -C "$CHECKOUT" -c core.sshCommand="$(git -C "$CHECKOUT" config --get core.sshCommand)" ls-remote "$URL" $REFS > "$OUTP.lsremote.out" 2> "$OUTP.lsremote.err"; rc=$?
fi
get() { awk -v r="$1" '$2==r{print $1}' "$OUTP.lsremote.out"; }
CUR_DEV="$(get refs/heads/develop)"
echo "  ls-remote rc=$rc at $(date -u +%H:%M:%SZ) | develop $CUR_DEV | #$PR pull/head $(get "refs/pull/$PR/head") | branch $(get "refs/heads/$BR")"
[ "$rc" -eq 0 ] && [ -n "$CUR_DEV" ] || { echo "REFUSING: ls-remote failed or returned no develop"; sed 's/^/    stderr: /' "$OUTP.lsremote.err"; exit 2; }
[ "$(get "refs/pull/$PR/head")" = "$HD" ] && [ "$(get "refs/heads/$BR")" = "$HD" ] || { echo "REFUSING TO LAUNCH: origin pull/head '$(get "refs/pull/$PR/head")' / branch '$(get "refs/heads/$BR")' != the input head $HD — MISMATCH"; exit 11; }

echo "--- 1. PULLS API + census"
python3 "$GS/gh_gate70.py" api --head "$HD" > "$OUTP.api.out" 2> "$OUTP.api.err"; arc=$?
python3 "$GS/gh_gate70.py" census > "$OUTP.census.out" 2> "$OUTP.census.err"; crc=$?
sed 's/^/    /' "$OUTP.api.out" "$OUTP.census.out" | cut -c1-240
echo "  api rc=$arc census rc=$crc (census rc 1 = OVERLAP printed above: REPORTED, not refused)"
[ "$arc" -eq 3 ] || [ "$crc" -eq 3 ] && { echo "REFUSING: API failure or a BLIND census control"; exit 3; }

echo "--- 3. the head: input == READY == API == pull/head == branch; open, not merged, on develop"
A_LINE="$(grep '^API #' "$OUTP.api.out")"; set -- $A_LINE
# $1 API  $2 #<n>  $3 head $4 <sha>  $5 branch $6 <ref>  $7 base $8 <ref>  $9 state $10 <s>  $11 merged $12 <b> ...
[ "${4:-}" = "$HD" ] && [ "${6:-}" = "$BR" ] && [ "${8:-}" = develop ] && [ "${10:-}" = open ] && [ "${12:-}" = False ] || { echo "REFUSING TO LAUNCH: the API does not show #$PR open, unmerged, on develop at $HD: '$A_LINE'"; exit 11; }
set --
echo "  ALL INSTRUMENTS AGREE with the input head."

echo "--- 3b. develop: origin $CUR_DEV | kit (at drafting) $KDEV"
DEV_MOVED=0
if [ "$CUR_DEV" = "$KDEV" ]; then echo "  UNMOVED since drafting (the PR's one parent IS develop: the squash applies the head's tree exactly)."
  [ -z "$REPIN" ] || [ "$REPIN" = "$CUR_DEV" ] || { echo "REFUSING TO LAUNCH: --repin-develop $REPIN is not origin develop $CUR_DEV (stale re-pin)"; exit 10; }
else DEV_MOVED=1; echo "  DEVELOP MOVED: $KDEV -> $CUR_DEV  (step 3c checks descent and that the advance touches none of the 37 paths / tooling)"; fi

echo "--- R. render the prompt (head $HD, develop $CUR_DEV)"
python3 - "$GS/prompt_gate70.txt" "$GS/prompt_gate70.rendered.txt" "$GS/head_at_launch.txt" "$HD" "$BR" "$CUR_DEV" "$PR" <<'PYEOF' || { echo "REFUSING: render failed"; exit 9; }
import sys
src, dst, hf, hd, br, dev, pr = sys.argv[1:8]
t = open(src, encoding='utf-8').read()
nh, nd = t.count('{{HEAD}}'), t.count('{{DEVELOP}}')
if nh < 10 or nd < 1: raise SystemExit('template tokens HEAD x%d DEVELOP x%d (want >= 10 / 1)' % (nh, nd))
t = t.replace('{{HEAD}}', hd).replace('{{DEVELOP}}', dev)
if '{{' in t: raise SystemExit('an unknown {{token}} survived the render')
open(dst, 'w', encoding='utf-8').write(t)
open(hf, 'w').write('P %s %s %s\n' % (pr, br, hd))
print('  rendered HEAD x%d DEVELOP x%d -> %s (%d bytes); head file %s' % (nh, nd, dst, len(t.encode()), hf))
PYEOF

echo "--- 0. routing: the pane must be in inbox_routing.conf"
/usr/bin/grep -c -x -F "$LINE" "$ROUTING" > "$OUTP.routing.out" 2> "$OUTP.routing.err"; rc=$?
echo "  $ROUTING — exact line present: $(cat "$OUTP.routing.out") (grep rc=$rc; want 1 / rc 0). CONTROL: agentmail lines in the file = $(/usr/bin/grep -c -i 'agentmail' "$ROUTING")"
if [ "$rc" -ne 0 ]; then
  if [ "$DRY" = 1 ]; then echo "  (DRY RUN: reported, not refused — the real run refuses rc 1; ROUTING_LINE.txt)"; else echo "REFUSING: add the routing line first (ROUTING_LINE.txt): $LINE"; exit 1; fi
fi

echo "--- 3c. the kit's own clone: fetch by sha if absent, C1 at the head on the develop read now, the c2 prediction"
if [ ! -d "$CL/.git" ] && [ ! -f "$CL/HEAD" ]; then
  mkdir -p "$GS/_scratch"; env -u GIT_SSH_COMMAND git clone --shared --no-checkout --quiet "$CHECKOUT" "$CL" > "$OUTP.clone.out" 2> "$OUTP.clone.err" || { echo "REFUSING: kit clone failed"; exit 13; }
  git -C "$CL" config remote.origin.url "$URL"
  git -C "$CL" config core.sshCommand "$(git -C "$CHECKOUT" config --get core.sshCommand)"
fi
for s in "$HD" "$CUR_DEV" "$KDEV"; do
  git -C "$CL" cat-file -e "$s^{commit}" 2>/dev/null || env -u GIT_SSH_COMMAND git -C "$CL" fetch --quiet --no-tags --no-write-fetch-head origin "$s" >> "$OUTP.fetch.out" 2>> "$OUTP.fetch.err" || { echo "REFUSING: fetch by sha $s into the kit clone failed"; tail -3 "$OUTP.fetch.err"; exit 13; }
done
python3 "$GS/c1_pin_gate70.py" --repo "$CL" --head "$HD" --develop "$CUR_DEV" --no-remote > "$OUTP.c1.out" 2> "$OUTP.c1.err"; rc1=$?
echo "  c1 rc=$rc1 | $(grep -E '^(CHECKED|[0-9]+ FAIL)' "$OUTP.c1.out" | tr '\n' ' ')"; grep -E '^FAIL' "$OUTP.c1.out" | sed 's/^/    /' | cut -c1-240
[ "$rc1" -eq 0 ] || { echo "REFUSING TO LAUNCH: C1 FAILED at the head (a moved develop that touched the PR's paths / tooling fails P12 here)"; exit 13; }
python3 "$GS/c2_locks_gate70.py" diff --repo "$CL" --head "$HD" > "$OUTP.c2diff.out" 2> "$OUTP.c2diff.err"; rc2=$?
python3 "$GS/c2_locks_gate70.py" parse --repo "$CL" --rev "$HD" --expect-clean > "$OUTP.c2parse.out" 2> "$OUTP.c2parse.err"; rc3=$?
echo "  c2 diff rc=$rc2 | $(grep -E '^(CHECKED|[0-9]+ FAIL)' "$OUTP.c2diff.out" | tr '\n' ' ') | c2 parse --expect-clean rc=$rc3 (PREDICTIONS for the gate, not refused)"
grep -E '^FAIL' "$OUTP.c2diff.out" "$OUTP.c2parse.out" | sed 's/^/    /' | cut -c1-240
if [ "$DEV_MOVED" = 1 ]; then
  if [ -z "$REPIN" ]; then echo "REFUSING TO LAUNCH: develop moved (c1 P12 says it touched none of the PR's paths / tooling). To re-pin and launch over it, re-run with:  --repin-develop $CUR_DEV"; exit 10
  elif [ "$REPIN" != "$CUR_DEV" ]; then echo "REFUSING TO LAUNCH: --repin-develop $REPIN is not origin develop $CUR_DEV (stale re-pin)"; exit 10; fi
  echo "repin $(date -u +%Y-%m-%dT%H:%M:%SZ): develop $KDEV -> $CUR_DEV" > "$OUTP.repin.txt"; echo "  RE-PINNED develop -> $CUR_DEV ($OUTP.repin.txt)"
fi

if [ "$DRY" = 1 ]; then
  echo "--- 6 (dry). the launcher's own --check"
  "$L" --check > "$OUTP.launcher_check.out" 2> "$OUTP.launcher_check.err"; rc=$?
  sed 's/^/    /' "$OUTP.launcher_check.out" "$OUTP.launcher_check.err"; echo "  launcher --check rc=$rc"
  [ "$rc" -eq 0 ] || { echo "DRY RUN: the launcher refused under --check (rc $rc)"; exit 13; }
  echo "DRY RUN COMPLETE $(date -u '+%Y-%m-%dT%H:%M:%SZ') — #$PR $HD, develop $CUR_DEV; the real run continues with the override check, the usage gate, --check and cockpit.sh add"; exit 0
fi
echo "--- 4. no test override on a real launch"
[ "$(env | grep -c '^G70_')" = 0 ] || { echo "REFUSING TO LAUNCH: a G70_* override is set"; exit 16; }
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
echo "LAUNCHED $(date -u '+%Y-%m-%dT%H:%M:%SZ') #$PR at $HD; develop at launch $CUR_DEV — now verify RUNG 5 (README §7)"
