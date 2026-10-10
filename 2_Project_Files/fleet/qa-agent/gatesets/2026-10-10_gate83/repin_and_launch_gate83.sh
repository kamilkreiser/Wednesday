#!/bin/bash
# repin_and_launch_gate83.sh — the LAUNCH ACTION for gate83 (ONE PR: #1450 KS-1426, Seat F 10th, tier 2).
# Carried from repin_and_launch_gate82.sh; [g83] ONE PR (every PR constant, the base included, is a REQUIRED argument); the merge SEAT is a REQUIRED argument (no default; the GO string is
# DERIVED from it); the render fills {{HEAD1450}} {{DEVELOP}} {{LSUTC}} {{SEAT}}; the c1 `companions` census runs beside the c1 of the PR (the other writers of the two docs).
# A MOVED HEAD refuses rc 11 (re-draft, never re-gate a stale pin).
# [g72] EVERY PR-SPECIFIC CONSTANT IS A REQUIRED ARGUMENT (STANDING_LINES: "inherited tools FAIL CLOSED on unset knobs"). Each is compared
# with kit.json (the drafter's pin) AND with what this script reads live; a wrong value refuses BY NAME:
#   (V)  every argument present and well-formed                                                                  — rc 9 (missing / malformed)
#        each == kit.json                                                                                       — rc 11 (WRONG VALUE)
#   (A)  the READY names its head in full and its #<pr>                                                          — rc 18
#   (2)  ONE `git ls-remote` of develop, refs/pull/1450/head, the branch AND the four companion pull heads, from the Secuura checkout: GIT_SSH_COMMAND UNSET,
#        `-c core.sshCommand=<the checkout's own>`, the GitHub URL (a read verb)                                  — rc 2
#        --head == pull/head == branch                                                                           — rc 11 (MISMATCH)
#        a COMPANION head that differs from the kit's pin is REPORTED (INFO), never refused: the gate re-reads them and passes them to c3
#   (1)  gh_gate83.py api (rc 3 API failure; rc 11 not open / not develop / head differs) + census (OVERLAP printed, not refused).
#        `--no-api` skips both ONLY with --dry-run.
#   (3b) origin develop == --develop -> on; MOVED -> rc 10 unless `--repin-develop <origin's 40-hex>` (stale re-pin rc 10)
#   (3c) THE KIT'S OWN CLONE (<kit>/_scratch/clone, `clone --shared --no-checkout` of the checkout, origin = the GitHub URL, the checkout's
#        core.sshCommand, NEVER an exported GIT_SSH_COMMAND): fetch the head / develop / base / companion heads BY SHA only if absent INTO THE KIT CLONE (never the
#        shared checkout); any still absent refused BY NAME — rc 19. c1 + c1 companions must pass — rc 13. c2 claims printed as the launch-time PREDICTION (never refused: the gate rules).
#   (R)  render prompt_gate83.txt -> prompt_gate83.rendered.txt + head_at_launch.txt (P / B / T / D / S lines) — rc 9
#   (0)  the pane is routed in inbox_routing.conf — rc 1 (a dry run REPORTS it instead; this script only READS the file)
#   (4)  G83_* overrides refuse a real launch — rc 16;  (5) the usage gate — rc 12;  (6) the launcher's --check — rc 13;  (7) cockpit add — rc 14
# --dry-run: V, A, 2, 1 (or --no-api), 3b, 3c, R, 0 and the launcher's --check, then STOPS: no usage gate, no cockpit.sh add, no pane, no mail.
# Output: launch_<HHMMSS>.* (dry: dry_<HHMMSS>.*).
# Controls-only overrides (DRY RUN ONLY): G83_ROUTING (routing stand-in), G83_LSFILE (ls-remote stand-in).
# Usage (a real launch runs under `script -q /dev/null`):
#   repin_and_launch_gate83.sh --seat "Seat X nth" --parents-n 1 --develop <40-hex> --head-1450 <40-hex> --branch-1450 <ref> --tree-1450 <40-hex> --base-1450 <40-hex> \
#       [--dry-run [--no-api]] [--repin-develop <40-hex>]
set -u
export PYTHONDONTWRITEBYTECODE=1
GS="$(dirname "$(/bin/realpath "$0")")"
CHECKOUT='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
KJ() { python3 -c 'import json,sys; v=json.load(open(sys.argv[1]))
for k in sys.argv[2].split("."): v=v[int(k)] if isinstance(v,list) else v[k]
print(" ".join(map(str,v)) if isinstance(v,list) else ("" if v is None else v))' "$GS/kit.json" "$1"; }
ROUTING="${G83_ROUTING:-$(KJ routing)}"; PANE="$(KJ pane)"; LINE="$(KJ routing_line)"; URL="$(KJ github_url)"
L="$GS/$(KJ launcher)"; CL="$GS/_scratch/clone"; PRS="$(KJ go_prs)"
USAGE='usage: repin_and_launch_gate83.sh --seat "Seat X nth" --parents-n <n> --develop <40-hex> --head-1450 <40-hex> --branch-1450 <ref> --tree-1450 <40-hex> --base-1450 <40-hex> [--dry-run [--no-api]] [--repin-develop <40-hex>]'
SEAT=""; NPAR=""; DEV=""; DRY=0; NOAPI=0; REPIN=""
for _p in $PRS; do eval "H_$_p=''; B_$_p=''; T_$_p=''; BS_$_p=''"; done
while [ $# -gt 0 ]; do
  case "$1" in
    --seat) SEAT="${2:-}"; shift 2 2>/dev/null || shift;;        --parents-n) NPAR="${2:-}"; shift 2 2>/dev/null || shift;;
    --develop) DEV="${2:-}"; shift 2 2>/dev/null || shift;;
    --head-1450) H_1450="${2:-}"; shift 2 2>/dev/null || shift;; --branch-1450) B_1450="${2:-}"; shift 2 2>/dev/null || shift;; --tree-1450) T_1450="${2:-}"; shift 2 2>/dev/null || shift;; --base-1450) BS_1450="${2:-}"; shift 2 2>/dev/null || shift;;
    --repin-develop) REPIN="${2:-}"; shift 2 2>/dev/null || shift;;
    --dry-run) DRY=1; shift;; --no-api) NOAPI=1; shift;;
    *) echo "$USAGE"; exit 9;;
  esac
done
echo "--- V. required arguments, each well-formed and == the kit's pin (a wrong value refuses BY NAME)"
_need="SEAT NPAR DEV"; for _p in $PRS; do _need="$_need H_$_p B_$_p T_$_p BS_$_p"; done
for _a in $_need; do eval "_v=\$$_a"; [ -n "$_v" ] || { echo "REFUSING: a REQUIRED argument is missing ($_a)"; echo "$USAGE"; exit 9; }; done
_hex="DEV"; for _p in $PRS; do _hex="$_hex H_$_p T_$_p BS_$_p"; done
for _a in $_hex; do eval "_v=\$$_a"; printf '%s' "$_v" | grep -qE '^[0-9a-f]{40}$' || { echo "REFUSING: $_a must be the FULL 40-hex sha, got '$_v'"; exit 9; }; done
printf '%s' "$NPAR" | grep -qE '^[0-9]+$' || { echo "REFUSING: --parents-n must be an integer"; exit 9; }
printf '%s' "$SEAT" | grep -qE '^Seat [A-Z] [0-9]+(st|nd|rd|th)$' || { echo "REFUSING: --seat must read 'Seat X nth' (e.g. \"Seat R 33rd\"), got '$SEAT'"; exit 9; }
[ -z "$REPIN" ] || printf '%s' "$REPIN" | grep -qE '^[0-9a-f]{40}$' || { echo "REFUSING: --repin-develop must be the FULL 40-hex sha, got '$REPIN'"; exit 9; }
[ "$NOAPI" = 0 ] || [ "$DRY" = 1 ] || { echo "REFUSING: --no-api is a dry-run option only (a real launch reads the PR API)"; exit 9; }
chk() { [ "$2" = "$(KJ "$3")" ] || { echo "REFUSING: WRONG VALUE $1 '$2' != kit.json $3 '$(KJ "$3")' — the kit's figures are for that value; re-draft"; exit 11; }; }
for _p in $PRS; do
  eval "_h=\$H_$_p; _b=\$B_$_p; _t=\$T_$_p; _bs=\$BS_$_p"
  chk --head-$_p "$_h" prs.$_p.head_expected; chk --branch-$_p "$_b" prs.$_p.branch; chk --tree-$_p "$_t" prs.$_p.end_tree
  chk --base-$_p "$_bs" prs.$_p.parents.0; chk --parents-n "$NPAR" prs.$_p.parent_count
done
chk --develop "$DEV" develop_at_draft
echo "  7 required arguments present, well-formed and == kit.json (seat '$SEAT' has no kit pin: Wednesday names it)"
T="$(date -u +%H%M%S)"; OUTP="$GS/launch_$T"; [ "$DRY" = 1 ] && OUTP="$GS/dry_$T"
echo "LAUNCH ACTION gate83$([ "$DRY" = 1 ] && echo ' (DRY RUN)') $(date '+%Y-%m-%d %H:%M:%S %Z') / $(date -u '+%Y-%m-%dT%H:%M:%SZ') | #1450 $H_1450 base $BS_1450 | parents x$NPAR | tree $T_1450 | develop $DEV | repin-develop ${REPIN:-none} | seat $SEAT | pane $PANE"

echo "--- A. the head must be the one its READY names"
for _p in $PRS; do
  eval "_h=\$H_$_p"; READY="$(KJ prs.$_p.ready)"
  [ -s "$READY" ] || { echo "REFUSING: the #$_p READY is missing or empty ('$READY')"; exit 18; }
  _n="$(/usr/bin/grep -c -F "$_h" "$READY")"; _q="$(/usr/bin/grep -c -F "#$_p" "$READY")"; _c="$(/usr/bin/grep -c -i 'READY' "$READY")"
  echo "  #$_p $READY (sha256/16 $(shasum -a 256 "$READY" | cut -c1-16)): lines naming the head in full $_n | naming #$_p $_q | CONTROL lines naming 'READY' $_c"
  [ "$_n" -ge 1 ] && [ "$_q" -ge 1 ] || { echo "REFUSING: the #$_p READY does not name $_h in full (or #$_p)"; exit 18; }
done

echo "--- 2. ONE ls-remote (read verb) from the checkout, GIT_SSH_COMMAND unset, the checkout's own core.sshCommand"
[ -z "${GIT_SSH_COMMAND:-}" ] || echo "  NOTE: GIT_SSH_COMMAND is exported in this shell; every git call below runs under env -u GIT_SSH_COMMAND"
REFS="refs/heads/develop"; for _p in $PRS; do eval "_b=\$B_$_p"; REFS="$REFS refs/pull/$_p/head refs/heads/$_b"; done
CPRS="$(KJ companions_list)"; for _c in $CPRS; do REFS="$REFS refs/pull/$_c/head"; done
if [ -n "${G83_LSFILE:-}" ]; then
  [ "$DRY" = 1 ] || { echo "REFUSING: G83_LSFILE is a dry-run control only"; exit 16; }
  cp "$G83_LSFILE" "$OUTP.lsremote.out"; : > "$OUTP.lsremote.err"; rc=0; echo "  (CONTROL: ls-remote output read from the stand-in $G83_LSFILE)"
else
  env -u GIT_SSH_COMMAND git -C "$CHECKOUT" -c core.sshCommand="$(git -C "$CHECKOUT" config --get core.sshCommand)" ls-remote "$URL" $REFS > "$OUTP.lsremote.out" 2> "$OUTP.lsremote.err"; rc=$?
fi
LSUTC="$(date -u +%Y-%m-%dT%H:%M:%S)"
get() { awk -v r="$1" '$2==r{print $1}' "$OUTP.lsremote.out"; }
CUR_DEV="$(get refs/heads/develop)"
_line="  ls-remote rc=$rc at $(date -u +%H:%M:%SZ) | develop $CUR_DEV"; for _p in $PRS; do eval "_b=\$B_$_p"; _line="$_line | #$_p pull/head $(get refs/pull/$_p/head) branch $(get "refs/heads/$_b")"; done; echo "$_line"
[ "$rc" -eq 0 ] && [ -n "$CUR_DEV" ] || { echo "REFUSING: ls-remote failed or returned no develop"; sed 's/^/    stderr: /' "$OUTP.lsremote.err"; exit 2; }
for _c in $CPRS; do _ch="$(get refs/pull/$_c/head)"; _ck="$(KJ companions.$_c.head_expected)"
  if [ "$_ch" = "$_ck" ]; then echo "  companion #$_c pull/head ${_ch:0:12} == the kit pin (INFO: the gate re-reads and passes --comp-head-$_c to c1 companions / c3 compose / docs)"
  else echo "  companion #$_c pull/head '${_ch:0:12}' != the kit pin ${_ck:0:12}: REPORTED (INFO, NOT refused: the companions are not gated here; the gate must use the head IT reads and say so)"; fi; done
for _p in $PRS; do
  eval "_h=\$H_$_p; _b=\$B_$_p"
  [ "$(get refs/pull/$_p/head)" = "$_h" ] && [ "$(get "refs/heads/$_b")" = "$_h" ] || { echo "REFUSING TO LAUNCH: #$_p origin pull/head '$(get refs/pull/$_p/head)' / branch '$(get "refs/heads/$_b")' != --head-$_p $_h — MISMATCH"; exit 11; }
done

echo "--- 1. PULLS API + census"
if [ "$NOAPI" = 1 ]; then echo "  SKIPPED BY NAME (--no-api, dry run only): the API state and the census are NOT read here"
else
  for _p in $PRS; do
    eval "_h=\$H_$_p"
    python3 "$GS/gh_gate83.py" api --pr $_p --head "$_h" > "$OUTP.api$_p.out" 2> "$OUTP.api$_p.err"; eval "arc_$_p=$?"
  done
  python3 "$GS/gh_gate83.py" census > "$OUTP.census.out" 2> "$OUTP.census.err"; crc=$?
  sed 's/^/    /' "$OUTP".api*.out "$OUTP.census.out" | cut -c1-240
  echo "  api rc: $(for _p in $PRS; do eval "printf '#%s=%s ' $_p \$arc_$_p"; done) census rc=$crc (census rc 1 = OVERLAP-CODE printed above: REPORTED, not refused)"
  for _p in $PRS; do eval "_a=\$arc_$_p"; [ "$_a" -ne 3 ] || { echo "REFUSING: API failure (#$_p)"; exit 3; }; done
  [ "$crc" -ne 3 ] || { echo "REFUSING: a BLIND census control"; exit 3; }
  for _p in $PRS; do eval "_a=\$arc_$_p; _h=\$H_$_p"; [ "$_a" -eq 0 ] || { echo "REFUSING TO LAUNCH: the API does not show #$_p open, unmerged, on develop at $_h"; exit 11; }; done
fi

echo "--- 3b. develop: origin $CUR_DEV | --develop $DEV"
DEV_MOVED=0
if [ "$CUR_DEV" = "$DEV" ]; then echo "  UNMOVED since the draft (#1450 branches from $BS_1450; a develop that moves is REPORTED here, never hardcoded)."
  [ -z "$REPIN" ] || [ "$REPIN" = "$CUR_DEV" ] || { echo "REFUSING TO LAUNCH: --repin-develop $REPIN is not origin develop $CUR_DEV (stale re-pin)"; exit 10; }
else DEV_MOVED=1; echo "  DEVELOP MOVED: $DEV -> $CUR_DEV (step 3c checks descent and that the advance touches no PR path outside the known docs overlap, and no tooling path)"; fi

echo "--- 3c. the kit's own clone: fetch by sha if absent, C1 per PR + set on the develop read now, the c2 predictions"
if [ ! -d "$CL/.git" ] && [ ! -f "$CL/HEAD" ]; then
  mkdir -p "$GS/_scratch"; env -u GIT_SSH_COMMAND git clone --shared --no-checkout --quiet "$CHECKOUT" "$CL" > "$OUTP.clone.out" 2> "$OUTP.clone.err" || { echo "REFUSING: kit clone failed"; exit 13; }
fi
git -C "$CL" config remote.origin.url "$URL"
git -C "$CL" config core.sshCommand "$(git -C "$CHECKOUT" config --get core.sshCommand)"
_shas="$CUR_DEV $(KJ trailer_control)"; for _p in $PRS; do eval "_h=\$H_$_p; _bs=\$BS_$_p"; _shas="$_h $_bs $_shas"; done
for _c in $CPRS; do _shas="$(get refs/pull/$_c/head) $(KJ companions.$_c.parents.0) $_shas"; done
for s in $_shas; do
  git -C "$CL" cat-file -e "$s^{commit}" 2>/dev/null || env -u GIT_SSH_COMMAND git -C "$CL" fetch --quiet --no-tags --no-write-fetch-head origin "$s" >> "$OUTP.fetch.out" 2>> "$OUTP.fetch.err"
  git -C "$CL" cat-file -e "$s^{commit}" 2>/dev/null || { echo "REFUSING: $s is ABSENT from the kit clone after a by-sha fetch"; tail -3 "$OUTP.fetch.err" 2>/dev/null; exit 19; }
done
for _p in $PRS; do
  eval "_h=\$H_$_p; _t=\$T_$_p; _bs=\$BS_$_p"
  python3 "$GS/c1_pin_gate83.py" --repo "$CL" --pr "$_p" --head "$_h" --base "$_bs" --develop "$CUR_DEV" --end-tree "$_t" --parents-n "$NPAR" --no-remote > "$OUTP.c1_$_p.out" 2> "$OUTP.c1_$_p.err"; rc1=$?
  echo "  c1 #$_p rc=$rc1 | $(grep -E '^(CHECKED|[0-9]+ FAIL)' "$OUTP.c1_$_p.out" | tr '\n' ' ')"; grep -E '^FAIL' "$OUTP.c1_$_p.out" | sed 's/^/    /' | cut -c1-240
  # [g78] EVERY c1 FAIL refuses (rc 13).
  _hard="$(grep -E '^FAIL ' "$OUTP.c1_$_p.out" | wc -l | tr -d ' ')"
  [ "$rc1" = 0 ] && [ "$_hard" = 0 ] || { echo "REFUSING TO LAUNCH: C1 FAILED for #$_p at the head ($_hard FAIL line(s), c1 rc $rc1)"; exit 13; }
done
CARGS=""; for _c in $CPRS; do CARGS="$CARGS --comp-head-$_c $(get refs/pull/$_c/head)"; done
python3 "$GS/c1_pin_gate83.py" companions --repo "$CL" --head1450 "$H_1450" --base1450 "$BS_1450" --develop "$CUR_DEV" $CARGS > "$OUTP.c1_companions.out" 2> "$OUTP.c1_companions.err"; rcp=$?
echo "  c1 companions rc=$rcp | $(grep -E '^(CHECKED|[0-9]+ FAIL)' "$OUTP.c1_companions.out" | tr '\n' ' ')"; grep -E '^FAIL' "$OUTP.c1_companions.out" | sed 's/^/    /' | cut -c1-240
[ "$rcp" = 0 ] || { echo "REFUSING TO LAUNCH: the COMPANION census failed (#1450 and the other writers of the two docs must share the two docs and NO non-doc path, and no two may number the same flow block; a companion's LIVE head is read here)"; exit 13; }
for _p in $PRS; do
  eval "_h=\$H_$_p; _bs=\$BS_$_p"
  python3 "$GS/c2_code_gate83.py" claims --repo "$CL" --pr "$_p" --head "$_h" --base "$_bs" > "$OUTP.c2claims_$_p.out" 2> "$OUTP.c2claims_$_p.err"; rc2=$?
  echo "  c2 claims #$_p rc=$rc2 | $(grep -E '^(CHECKED|[0-9]+ FAIL)' "$OUTP.c2claims_$_p.out" | tr '\n' ' ') (a PREDICTION for the gate, not refused)"
  grep -E '^FAIL' "$OUTP.c2claims_$_p.out" | sed 's/^/    /' | cut -c1-240
done
if [ "$DEV_MOVED" = 1 ]; then
  if [ -z "$REPIN" ]; then echo "REFUSING TO LAUNCH: develop moved (c1 P12 says it touched no PR path outside the known docs overlap, and no tooling path). To re-pin and launch over it, re-run with:  --repin-develop $CUR_DEV"; exit 10
  elif [ "$REPIN" != "$CUR_DEV" ]; then echo "REFUSING TO LAUNCH: --repin-develop $REPIN is not origin develop $CUR_DEV (stale re-pin)"; exit 10; fi
  echo "repin $(date -u +%Y-%m-%dT%H:%M:%SZ): develop $DEV -> $CUR_DEV" > "$OUTP.repin.txt"; echo "  RE-PINNED develop -> $CUR_DEV ($OUTP.repin.txt)"
fi

echo "--- R. render the prompt (head $H_1450, develop $CUR_DEV, seat $SEAT, ls-remote $LSUTC UTC)"
python3 - "$GS/prompt_gate83.txt" "$GS/prompt_gate83.rendered.txt" "$GS/head_at_launch.txt" "$NPAR" "$CUR_DEV" "$SEAT" "$LSUTC" \
  "1450" "$H_1450" "$B_1450" "$T_1450" "$BS_1450" <<'PYEOF' || { echo "REFUSING: render failed"; exit 9; }
import sys
a = sys.argv[1:]
src, dst, hf, npar, dev, seat, lsutc = a[:7]
prs = [a[7 + 5 * i: 12 + 5 * i] for i in range(1)]      # [pr, head, branch, tree, base]
t = open(src, encoding='utf-8').read()
want = dict((('{{HEAD%s}}' % p[0]), (2, p[1])) for p in prs); want.update({'{{DEVELOP}}': (2, dev), '{{SEAT}}': (2, seat), '{{LSUTC}}': (1, lsutc)})
for tok, (n, _) in want.items():
    if t.count(tok) < n: raise SystemExit('template token %s x%d (want >= %d)' % (tok, t.count(tok), n))
counts = dict((tok, t.count(tok)) for tok in want)
for tok, (_, val) in want.items(): t = t.replace(tok, val)
if '{{' in t: raise SystemExit('an unknown {{token}} survived the render')
open(dst, 'w', encoding='utf-8').write(t)
open(hf, 'w').write(''.join('P %s %s %s\n' % (p[0], p[2], p[1]) for p in prs) + ''.join('B %s %s %s\n' % (p[0], p[4], npar) for p in prs) + ''.join('T %s %s\n' % (p[0], p[3]) for p in prs) + 'D %s\nS %s\n' % (dev, seat))
print('  rendered %s -> %s (%d bytes); head file %s (P / B / T / D / S)' % (counts, dst, len(t.encode()), hf))
PYEOF

echo "--- 0. routing: the pane must be in inbox_routing.conf (READ only here)"
/usr/bin/grep -c -x -F "$LINE" "$ROUTING" > "$OUTP.routing.out" 2> "$OUTP.routing.err"; rc=$?
echo "  $ROUTING — exact line present: $(cat "$OUTP.routing.out") (grep rc=$rc; want 1 / rc 0). CONTROL: agentmail lines in the file = $(/usr/bin/grep -c -i 'agentmail' "$ROUTING")"
if [ "$rc" -ne 0 ]; then
  if [ "$DRY" = 1 ]; then echo "  (DRY RUN: reported, not refused — the real run refuses rc 1; ROUTING_LINE.txt)"; else echo "REFUSING: add the routing line first (ROUTING_LINE.txt): $LINE"; exit 1; fi
fi

if [ "$DRY" = 1 ]; then
  echo "--- 6 (dry). the launcher's own --check"
  # a dry run driven by the G83_LSFILE stand-in hands the SAME stand-in to the launcher (G83_LS), so a SIM develop is checked end to end
  # instead of being refused by the launcher's real ls-remote; the launcher names the override in its output.
  if [ -n "${G83_LSFILE:-}" ]; then G83_LS="$G83_LSFILE" "$L" --check > "$OUTP.launcher_check.out" 2> "$OUTP.launcher_check.err"; rc=$?
  else "$L" --check > "$OUTP.launcher_check.out" 2> "$OUTP.launcher_check.err"; rc=$?; fi
  sed 's/^/    /' "$OUTP.launcher_check.out" "$OUTP.launcher_check.err"; echo "  launcher --check rc=$rc"
  [ "$rc" -eq 0 ] || { echo "DRY RUN: the launcher refused under --check (rc $rc)"; exit 13; }
  echo "DRY RUN COMPLETE $(date -u '+%Y-%m-%dT%H:%M:%SZ') — #1450 $H_1450, develop $CUR_DEV; NO usage gate, NO cockpit.sh add, NO pane was touched. The real run continues with the override check, the usage gate, --check and cockpit.sh add"; exit 0
fi
echo "--- 4. no test override on a real launch"
[ "$(env | grep -c '^G83_')" = 0 ] || { echo "REFUSING TO LAUNCH: a G83_* override is set"; exit 16; }
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
echo "LAUNCHED $(date -u '+%Y-%m-%dT%H:%M:%SZ') #1450 at $H_1450; develop at launch $CUR_DEV — now verify RUNG 5 (KIT_REPORT §8)"
