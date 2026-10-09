#!/bin/bash
# repin_and_launch_gate78.sh — the LAUNCH ACTION for gate78 (T1: #1435 KS-1452 handlebars lock refresh, 5 locks, 0 baseline rows).
# Carried from repin_and_launch_gate72.sh; [g78]: EVERY c1 FAIL refuses (gate72 let P8 through; at gate78 P8 is clean, so a P8 FAIL
# can only mean a different head). [g72] EVERY PR-SPECIFIC CONSTANT IS A REQUIRED ARGUMENT (STANDING_LINES: "inherited tools FAIL
# CLOSED on unset knobs"; Seat R 2nd: "a REQUIRED argument with a wrong-value arm"). Each is compared with kit.json (the drafter's pin)
# AND with what this script reads live; a wrong value refuses BY NAME:
#   (V)  --pr --head --branch --base --parents-n --end-tree --develop all present and well-formed            — rc 9 (missing / malformed)
#        each == kit.json                                                                                       — rc 11 (WRONG VALUE)
#   (A)  the READY names the head in full and #<pr>                                                              — rc 18
#   (2)  ONE `git ls-remote` of develop, refs/pull/<pr>/head and the branch, from the Secuura checkout: GIT_SSH_COMMAND UNSET,
#        `-c core.sshCommand=<the checkout's own>`, the GitHub URL (read verb)                                   — rc 2
#        --head == pull/head == branch                                                                           — rc 11 (MISMATCH)
#   (1)  gh_gate78.py api (rc 3 API failure; rc 11 not open / not develop / head differs) + census (OVERLAP printed, not refused).
#        `--no-api` skips both ONLY with --dry-run.
#   (3b) origin develop == --develop -> on; MOVED -> rc 10 unless `--repin-develop <origin's 40-hex>` (stale re-pin rc 10)
#   (3c) THE KIT'S OWN CLONE (<kit>/_scratch/clone, `clone --shared --no-checkout` of the checkout, origin = the GitHub URL, the
#        checkout's core.sshCommand, NEVER an exported GIT_SSH_COMMAND): fetch head / develop / base BY SHA only if absent; any still
#        absent refused BY NAME — rc 19. c1 with EVERY required pin (P2 parents, P4 END_TREE, P10/P12 tooling and a moved develop)
#        must pass — rc 13. c2 diff + c2 parse printed as the launch-time PREDICTION (never refused: the gate rules).
#   (R)  render prompt_gate78.txt -> prompt_gate78.rendered.txt ({{HEAD}} {{DEVELOP}}) + head_at_launch.txt (P / B / T / D lines) — rc 9
#   (0)  the pane is routed in inbox_routing.conf — rc 1 (a dry run REPORTS it instead)
#   (4)  G78_* overrides refuse a real launch — rc 16;  (5) the usage gate — rc 12;  (6) the launcher's --check — rc 13;  (7) cockpit add — rc 14
# --dry-run: V, A, 2, 1 (or --no-api), 3b, 3c, R, 0 and the launcher's --check, then stops. Output: launch_<HHMMSS>.* (dry: dry_<HHMMSS>.*).
# Controls-only overrides (DRY RUN ONLY): G78_ROUTING (routing stand-in), G78_LSFILE (ls-remote stand-in).
# Usage (run under `script -q /dev/null`):
#   repin_and_launch_gate78.sh --pr 1435 --head <40-hex> --branch <ref> --base <40-hex> --parents-n 1 --end-tree <40-hex> --develop <40-hex>
#                              [--dry-run [--no-api]] [--repin-develop <40-hex>]
set -u
export PYTHONDONTWRITEBYTECODE=1
GS="$(dirname "$(/bin/realpath "$0")")"
CHECKOUT='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
KJ() { python3 -c 'import json,sys; v=json.load(open(sys.argv[1]))
for k in sys.argv[2].split("."): v=v[int(k)] if isinstance(v,list) else v[k]
print(" ".join(map(str,v)) if isinstance(v,list) else ("" if v is None else v))' "$GS/kit.json" "$1"; }
ROUTING="${G78_ROUTING:-$(KJ routing)}"; PANE="$(KJ pane)"; LINE="$(KJ routing_line)"; URL="$(KJ github_url)"
L="$GS/$(KJ launcher)"; CL="$GS/_scratch/clone"
USAGE="usage: repin_and_launch_gate78.sh --pr <n> --head <40-hex> --branch <ref> --base <40-hex> --parents-n <n> --end-tree <40-hex> --develop <40-hex> [--dry-run [--no-api]] [--repin-develop <40-hex>]"
PR=""; HD=""; BR=""; BASE=""; NPAR=""; TREE=""; DEV=""; DRY=0; NOAPI=0; REPIN=""
while [ $# -gt 0 ]; do
  case "$1" in
    --pr) PR="${2:-}"; shift 2 2>/dev/null || shift;;            --head) HD="${2:-}"; shift 2 2>/dev/null || shift;;
    --branch) BR="${2:-}"; shift 2 2>/dev/null || shift;;        --base) BASE="${2:-}"; shift 2 2>/dev/null || shift;;
    --parents-n) NPAR="${2:-}"; shift 2 2>/dev/null || shift;;   --end-tree) TREE="${2:-}"; shift 2 2>/dev/null || shift;;
    --develop) DEV="${2:-}"; shift 2 2>/dev/null || shift;;      --repin-develop) REPIN="${2:-}"; shift 2 2>/dev/null || shift;;
    --dry-run) DRY=1; shift;; --no-api) NOAPI=1; shift;;
    *) echo "$USAGE"; exit 9;;
  esac
done
echo "--- V. required arguments, each well-formed and == the kit's pin (a wrong value refuses BY NAME)"
for _a in PR HD BR BASE NPAR TREE DEV; do eval "_v=\$$_a"; [ -n "$_v" ] || { echo "REFUSING: a REQUIRED argument is missing ($_a)"; echo "$USAGE"; exit 9; }; done
for _a in HD BASE TREE DEV; do eval "_v=\$$_a"; printf '%s' "$_v" | grep -qE '^[0-9a-f]{40}$' || { echo "REFUSING: $_a must be the FULL 40-hex sha, got '$_v'"; exit 9; }; done
printf '%s' "$PR$NPAR" | grep -qE '^[0-9]+$' || { echo "REFUSING: --pr and --parents-n must be integers"; exit 9; }
[ -z "$REPIN" ] || printf '%s' "$REPIN" | grep -qE '^[0-9a-f]{40}$' || { echo "REFUSING: --repin-develop must be the FULL 40-hex sha, got '$REPIN'"; exit 9; }
[ "$NOAPI" = 0 ] || [ "$DRY" = 1 ] || { echo "REFUSING: --no-api is a dry-run option only (a real launch reads the PR API)"; exit 9; }
chk() { [ "$2" = "$(KJ "$3")" ] || { echo "REFUSING: WRONG VALUE $1 '$2' != kit.json $3 '$(KJ "$3")' — the kit's figures are for that value; re-draft"; exit 11; }; }
chk --pr "$PR" pr.pr; chk --head "$HD" pr.head_expected; chk --branch "$BR" pr.branch; chk --base "$BASE" pr.parents.0
chk --parents-n "$NPAR" pr.parent_count; chk --end-tree "$TREE" pr.end_tree; chk --develop "$DEV" develop_at_draft
echo "  7 required arguments present, well-formed and == kit.json"
T="$(date -u +%H%M%S)"; OUTP="$GS/launch_$T"; [ "$DRY" = 1 ] && OUTP="$GS/dry_$T"
echo "LAUNCH ACTION gate78$([ "$DRY" = 1 ] && echo ' (DRY RUN)') $(date '+%Y-%m-%d %H:%M:%S %Z') / $(date -u '+%Y-%m-%dT%H:%M:%SZ') | #$PR $HD | base $BASE x$NPAR | tree $TREE | develop $DEV | repin-develop ${REPIN:-none} | pane $PANE"

echo "--- A. the head must be the one the READY names"
READY="$(KJ pr.ready)"
[ -s "$READY" ] || { echo "REFUSING: READY missing or empty ('$READY')"; exit 18; }
_n="$(/usr/bin/grep -c -F "$HD" "$READY")"; _p="$(/usr/bin/grep -c -F "#$PR" "$READY")"; _c="$(/usr/bin/grep -c -i 'READY' "$READY")"
echo "  $READY (sha256/16 $(shasum -a 256 "$READY" | cut -c1-16)): lines naming the head in full $_n | naming #$PR $_p | CONTROL lines naming 'READY' $_c"
[ "$_n" -ge 1 ] && [ "$_p" -ge 1 ] || { echo "REFUSING: the READY does not name $HD in full (or #$PR)"; exit 18; }

echo "--- 2. ONE ls-remote (read verb) from the checkout, GIT_SSH_COMMAND unset, the checkout's own core.sshCommand"
[ -z "${GIT_SSH_COMMAND:-}" ] || echo "  NOTE: GIT_SSH_COMMAND is exported in this shell; every git call below runs under env -u GIT_SSH_COMMAND"
REFS="refs/heads/develop refs/pull/$PR/head refs/heads/$BR"
if [ -n "${G78_LSFILE:-}" ]; then
  [ "$DRY" = 1 ] || { echo "REFUSING: G78_LSFILE is a dry-run control only"; exit 16; }
  cp "$G78_LSFILE" "$OUTP.lsremote.out"; : > "$OUTP.lsremote.err"; rc=0; echo "  (CONTROL: ls-remote output read from the stand-in $G78_LSFILE)"
else
  env -u GIT_SSH_COMMAND git -C "$CHECKOUT" -c core.sshCommand="$(git -C "$CHECKOUT" config --get core.sshCommand)" ls-remote "$URL" $REFS > "$OUTP.lsremote.out" 2> "$OUTP.lsremote.err"; rc=$?
fi
get() { awk -v r="$1" '$2==r{print $1}' "$OUTP.lsremote.out"; }
CUR_DEV="$(get refs/heads/develop)"
echo "  ls-remote rc=$rc at $(date -u +%H:%M:%SZ) | develop $CUR_DEV | #$PR pull/head $(get "refs/pull/$PR/head") | branch $(get "refs/heads/$BR")"
[ "$rc" -eq 0 ] && [ -n "$CUR_DEV" ] || { echo "REFUSING: ls-remote failed or returned no develop"; sed 's/^/    stderr: /' "$OUTP.lsremote.err"; exit 2; }
[ "$(get "refs/pull/$PR/head")" = "$HD" ] && [ "$(get "refs/heads/$BR")" = "$HD" ] || { echo "REFUSING TO LAUNCH: origin pull/head '$(get "refs/pull/$PR/head")' / branch '$(get "refs/heads/$BR")' != --head $HD — MISMATCH"; exit 11; }

echo "--- 1. PULLS API + census"
if [ "$NOAPI" = 1 ]; then echo "  SKIPPED BY NAME (--no-api, dry run only): the API state and the census are NOT read here"
else
  python3 "$GS/gh_gate78.py" api --head "$HD" > "$OUTP.api.out" 2> "$OUTP.api.err"; arc=$?
  python3 "$GS/gh_gate78.py" census > "$OUTP.census.out" 2> "$OUTP.census.err"; crc=$?
  sed 's/^/    /' "$OUTP.api.out" "$OUTP.census.out" | cut -c1-240
  echo "  api rc=$arc census rc=$crc (census rc 1 = OVERLAP printed above: REPORTED, not refused)"
  [ "$arc" -eq 3 ] || [ "$crc" -eq 3 ] && { echo "REFUSING: API failure or a BLIND census control"; exit 3; }
  [ "$arc" -eq 0 ] || { echo "REFUSING TO LAUNCH: the API does not show #$PR open, unmerged, on develop at $HD"; exit 11; }
fi

echo "--- 3b. develop: origin $CUR_DEV | --develop $DEV"
DEV_MOVED=0
if [ "$CUR_DEV" = "$DEV" ]; then echo "  UNMOVED (the PR's one parent IS develop: the squash applies the head's tree exactly)."
  [ -z "$REPIN" ] || [ "$REPIN" = "$CUR_DEV" ] || { echo "REFUSING TO LAUNCH: --repin-develop $REPIN is not origin develop $CUR_DEV (stale re-pin)"; exit 10; }
else DEV_MOVED=1; echo "  DEVELOP MOVED: $DEV -> $CUR_DEV (step 3c checks descent and that the advance touches none of the 5 paths / tooling)"; fi

echo "--- 3c. the kit's own clone: fetch by sha if absent, C1 with every pin on the develop read now, the c2 prediction"
if [ ! -d "$CL/.git" ] && [ ! -f "$CL/HEAD" ]; then
  mkdir -p "$GS/_scratch"; env -u GIT_SSH_COMMAND git clone --shared --no-checkout --quiet "$CHECKOUT" "$CL" > "$OUTP.clone.out" 2> "$OUTP.clone.err" || { echo "REFUSING: kit clone failed"; exit 13; }
fi
git -C "$CL" config remote.origin.url "$URL"
git -C "$CL" config core.sshCommand "$(git -C "$CHECKOUT" config --get core.sshCommand)"
for s in "$HD" "$CUR_DEV" "$BASE" "$(KJ trailer_control)"; do
  git -C "$CL" cat-file -e "$s^{commit}" 2>/dev/null || env -u GIT_SSH_COMMAND git -C "$CL" fetch --quiet --no-tags --no-write-fetch-head origin "$s" >> "$OUTP.fetch.out" 2>> "$OUTP.fetch.err"
  git -C "$CL" cat-file -e "$s^{commit}" 2>/dev/null || { echo "REFUSING: $s is ABSENT from the kit clone after a by-sha fetch"; tail -3 "$OUTP.fetch.err" 2>/dev/null; exit 19; }
done
python3 "$GS/c1_pin_gate78.py" --repo "$CL" --head "$HD" --base "$BASE" --develop "$CUR_DEV" --end-tree "$TREE" --parents-n "$NPAR" --no-remote > "$OUTP.c1.out" 2> "$OUTP.c1.err"; rc1=$?
echo "  c1 rc=$rc1 | $(grep -E '^(CHECKED|[0-9]+ FAIL)' "$OUTP.c1.out" | tr '\n' ' ')"; grep -E '^FAIL' "$OUTP.c1.out" | sed 's/^/    /' | cut -c1-240
# [g78] EVERY c1 FAIL refuses (rc 13), P8 / P8b included.
_hard="$(grep -E '^FAIL ' "$OUTP.c1.out" | wc -l | tr -d ' ')"
[ "$rc1" = 0 ] && [ "$_hard" = 0 ] || { echo "REFUSING TO LAUNCH: C1 FAILED at the head ($_hard FAIL line(s), c1 rc $rc1)"; exit 13; }
python3 "$GS/c2_locks_gate78.py" diff --repo "$CL" --head "$HD" --base "$BASE" > "$OUTP.c2diff.out" 2> "$OUTP.c2diff.err"; rc2=$?
python3 "$GS/c2_locks_gate78.py" parse --repo "$CL" --rev "$HD" --expect-clean > "$OUTP.c2parse.out" 2> "$OUTP.c2parse.err"; rc3=$?
echo "  c2 diff rc=$rc2 | $(grep -E '^(CHECKED|[0-9]+ FAIL)' "$OUTP.c2diff.out" | tr '\n' ' ') | c2 parse --expect-clean rc=$rc3 (PREDICTIONS for the gate, not refused)"
grep -E '^FAIL' "$OUTP.c2diff.out" "$OUTP.c2parse.out" | sed 's/^/    /' | cut -c1-240
if [ "$DEV_MOVED" = 1 ]; then
  if [ -z "$REPIN" ]; then echo "REFUSING TO LAUNCH: develop moved (c1 P12 says it touched none of the PR's paths / tooling). To re-pin and launch over it, re-run with:  --repin-develop $CUR_DEV"; exit 10
  elif [ "$REPIN" != "$CUR_DEV" ]; then echo "REFUSING TO LAUNCH: --repin-develop $REPIN is not origin develop $CUR_DEV (stale re-pin)"; exit 10; fi
  echo "repin $(date -u +%Y-%m-%dT%H:%M:%SZ): develop $DEV -> $CUR_DEV" > "$OUTP.repin.txt"; echo "  RE-PINNED develop -> $CUR_DEV ($OUTP.repin.txt)"
fi

echo "--- R. render the prompt (head $HD, develop $CUR_DEV)"
python3 - "$GS/prompt_gate78.txt" "$GS/prompt_gate78.rendered.txt" "$GS/head_at_launch.txt" "$HD" "$BR" "$CUR_DEV" "$PR" "$BASE" "$NPAR" "$TREE" <<'PYEOF' || { echo "REFUSING: render failed"; exit 9; }
import sys
src, dst, hf, hd, br, dev, pr, base, npar, tree = sys.argv[1:11]
t = open(src, encoding='utf-8').read()
nh, nd = t.count('{{HEAD}}'), t.count('{{DEVELOP}}')
if nh < 8 or nd < 2: raise SystemExit('template tokens HEAD x%d DEVELOP x%d (want >= 8 / 2)' % (nh, nd))
t = t.replace('{{HEAD}}', hd).replace('{{DEVELOP}}', dev)
if '{{' in t: raise SystemExit('an unknown {{token}} survived the render')
open(dst, 'w', encoding='utf-8').write(t)
open(hf, 'w').write('P %s %s %s\nB %s %s\nT %s\nD %s\n' % (pr, br, hd, base, npar, tree, dev))
print('  rendered HEAD x%d DEVELOP x%d -> %s (%d bytes); head file %s (P / B / T / D)' % (nh, nd, dst, len(t.encode()), hf))
PYEOF

echo "--- 0. routing: the pane must be in inbox_routing.conf"
/usr/bin/grep -c -x -F "$LINE" "$ROUTING" > "$OUTP.routing.out" 2> "$OUTP.routing.err"; rc=$?
echo "  $ROUTING — exact line present: $(cat "$OUTP.routing.out") (grep rc=$rc; want 1 / rc 0). CONTROL: agentmail lines in the file = $(/usr/bin/grep -c -i 'agentmail' "$ROUTING")"
if [ "$rc" -ne 0 ]; then
  if [ "$DRY" = 1 ]; then echo "  (DRY RUN: reported, not refused — the real run refuses rc 1; ROUTING_LINE.txt)"; else echo "REFUSING: add the routing line first (ROUTING_LINE.txt): $LINE"; exit 1; fi
fi

if [ "$DRY" = 1 ]; then
  echo "--- 6 (dry). the launcher's own --check"
  # [g78] a dry run driven by the G78_LSFILE stand-in hands the SAME stand-in to the launcher (G78_LS), so a SIM develop is checked
  # end to end instead of being refused by the launcher's real ls-remote; the launcher names the override in its output.
  if [ -n "${G78_LSFILE:-}" ]; then G78_LS="$G78_LSFILE" "$L" --check > "$OUTP.launcher_check.out" 2> "$OUTP.launcher_check.err"; rc=$?
  else "$L" --check > "$OUTP.launcher_check.out" 2> "$OUTP.launcher_check.err"; rc=$?; fi
  sed 's/^/    /' "$OUTP.launcher_check.out" "$OUTP.launcher_check.err"; echo "  launcher --check rc=$rc"
  [ "$rc" -eq 0 ] || { echo "DRY RUN: the launcher refused under --check (rc $rc)"; exit 13; }
  echo "DRY RUN COMPLETE $(date -u '+%Y-%m-%dT%H:%M:%SZ') — #$PR $HD, develop $CUR_DEV; the real run continues with the override check, the usage gate, --check and cockpit.sh add"; exit 0
fi
echo "--- 4. no test override on a real launch"
[ "$(env | grep -c '^G78_')" = 0 ] || { echo "REFUSING TO LAUNCH: a G78_* override is set"; exit 16; }
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
echo "LAUNCHED $(date -u '+%Y-%m-%dT%H:%M:%SZ') #$PR at $HD; develop at launch $CUR_DEV — now verify RUNG 5 (KIT_REPORT §8)"
