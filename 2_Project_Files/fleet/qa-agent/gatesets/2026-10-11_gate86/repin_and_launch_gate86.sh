#!/bin/bash
# repin_and_launch_gate86.sh — the LAUNCH ACTION for gate86 (a TIER-2 BATCH of FOUR PRs: #1451 KS-591, #1452 KS-1364, #1454 KS-1355 (partial), #1455 KS-1417 piece 2; ROUND 1; THE GATE DECIDES EACH TIER).
# Carried from repin_and_launch_gate85.sh; [g86] FOUR PRs with FOUR DIFFERENT BASES (kit prs.<n>.base = merge-base(develop, head) = the head's ONE parent: f8c86f859fe0 / 4a7cc1f697f8 / e27b9dceff39 / e27b9dceff39);
# every PR-specific constant is a REQUIRED argument per PR (--head-<n> --branch-<n> --tree-<n> --base-<n>); the merge SEAT is a REQUIRED argument (no default; the FOUR GO strings are DERIVED from it); the render fills
# {{HEAD1451}} {{HEAD1452}} {{HEAD1454}} {{HEAD1455}} {{DEVELOP}} {{LSUTC}} and the fill-at-launch token @MERGE_SEAT@; `c1 isolation` and the c3 `compose` PREDICTION (24 merge orders) are new steps.
# A MOVED HEAD refuses rc 11 (re-draft, never re-gate a stale pin). A MOVED DEVELOP refuses rc 10 unless `--repin-develop <origin's 40-hex>` names it, and then c1 P12 / isolation must still pass (rc 13).
# [g72] EVERY PR-SPECIFIC CONSTANT IS A REQUIRED ARGUMENT (STANDING_LINES: "inherited tools FAIL CLOSED on unset knobs"). Each is compared with kit.json (the drafter's pin) AND with what this script reads live; a wrong value
# refuses BY NAME:
#   (V)  every argument present and well-formed                                                                  — rc 9 (missing / malformed)
#        each == kit.json (the base against prs.<n>.base)                                                      — rc 11 (WRONG VALUE)
#   (A)  the READY copy names every head in full and every #<pr>, and hashes to kit.json ready_sha256_16          — rc 18
#   (2)  ONE `git ls-remote` of develop, refs/pull/<n>/head AND the branch of all four PRs, from the Secuura checkout: GIT_SSH_COMMAND UNSET, `-c core.sshCommand=<the checkout's own>`, the GitHub URL (a read verb) — rc 2
#        each --head == pull/head == branch                                                                      — rc 11 (MISMATCH)
#   (1)  gh_gate86.py api per PR (rc 3 API failure; rc 11 not open / not develop / head differs) + census (OVERLAP printed, not refused). `--no-api` skips both ONLY with --dry-run.
#   (3b) origin develop == --develop -> on; MOVED -> rc 10 unless `--repin-develop <origin's 40-hex>` (stale re-pin rc 10)
#   (3c) THE KIT'S OWN CLONE (<kit>/_scratch/clone, `clone --shared --no-checkout` of the checkout, origin = the GitHub URL, the checkout's core.sshCommand, NEVER an exported GIT_SSH_COMMAND): fetch each head / base /
#        develop BY SHA only if absent INTO THE KIT CLONE (never the shared checkout); any still absent refused BY NAME — rc 19. c1 pin + c1 docsbase per PR and c1 isolation must pass — rc 13.
#        c2 claims per PR are printed as the launch-time PREDICTION (never refused: the gate rules). c3 compose (the 24-order merge-in prediction) is printed the same way.
#   (R)  render prompt_gate86.txt -> prompt_gate86.rendered.txt + head_at_launch.txt (P / B / T / D / S lines) — rc 9
#   (0)  the pane is routed in inbox_routing.conf — rc 1 (a dry run REPORTS it instead; this script only READS the file)
#   (4)  G86_* overrides refuse a real launch — rc 16;  (5) the usage gate — rc 12;  (6) the launcher's --check — rc 13;  (7) cockpit add — rc 14
# --dry-run: V, A, 2, 1 (or --no-api), 3b, 3c, R, 0 and the launcher's --check, then STOPS: no usage gate, no cockpit.sh add, no pane, no mail.
# Output: launch_<HHMMSS>.* (dry: dry_<HHMMSS>.*).
# Controls-only overrides (DRY RUN ONLY): G86_ROUTING (routing stand-in), G86_LSFILE (ls-remote stand-in), G86_CLONE (kit clone elsewhere).
# Usage (a real launch runs under `script -q /dev/null`):
#   repin_and_launch_gate86.sh --seat "Seat X nth" --parents-n 1 --develop <40-hex> \
#       --head-1451 <40-hex> --branch-1451 <ref> --tree-1451 <40-hex> --base-1451 <40-hex>   (and the same four flags for 1452, 1454, 1455) \
#       [--dry-run [--no-api]] [--repin-develop <40-hex>]
set -u
export PYTHONDONTWRITEBYTECODE=1
GS="$(dirname "$(/bin/realpath "$0")")"
CHECKOUT='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
KJ() { python3 -c 'import json,sys; v=json.load(open(sys.argv[1]))
for k in sys.argv[2].split("."): v=v[int(k)] if isinstance(v,list) else v[k]
print(" ".join(map(str,v)) if isinstance(v,list) else ("" if v is None else v))' "$GS/kit.json" "$1"; }
ROUTING="${G86_ROUTING:-$(KJ routing)}"; PANE="$(KJ pane)"; LINE="$(KJ routing_line)"; URL="$(KJ github_url)"
L="$GS/$(KJ launcher)"; CL="${G86_CLONE:-$GS/_scratch/clone}"; PRS="$(KJ go_prs)"
USAGE='usage: repin_and_launch_gate86.sh --seat "Seat X nth" --parents-n <n> --develop <40-hex> (--head-<pr> <40-hex> --branch-<pr> <ref> --tree-<pr> <40-hex> --base-<pr> <40-hex>)x4 for pr in 1451 1452 1454 1455 [--dry-run [--no-api]] [--repin-develop <40-hex>]'
SEAT=""; NPAR=""; DEV=""; DRY=0; NOAPI=0; REPIN=""
for _p in $PRS; do eval "H_$_p=''; B_$_p=''; T_$_p=''; BS_$_p=''"; done
inprs() { for _x in $PRS; do [ "$_x" = "$1" ] && return 0; done; return 1; }
while [ $# -gt 0 ]; do
  case "$1" in
    --seat) SEAT="${2:-}"; shift 2 2>/dev/null || shift;;        --parents-n) NPAR="${2:-}"; shift 2 2>/dev/null || shift;;
    --develop) DEV="${2:-}"; shift 2 2>/dev/null || shift;;
    --head-*|--branch-*|--tree-*|--base-*)
      _k="${1%%-[0-9]*}"; _k="${_k#--}"; _pn="${1##*-}"
      inprs "$_pn" || { echo "REFUSING: $1 names a PR that is not in this batch ($PRS)"; echo "$USAGE"; exit 9; }
      case "$_k" in head) eval "H_$_pn=\"\${2:-}\"";; branch) eval "B_$_pn=\"\${2:-}\"";; tree) eval "T_$_pn=\"\${2:-}\"";; base) eval "BS_$_pn=\"\${2:-}\"";; *) echo "$USAGE"; exit 9;; esac
      shift 2 2>/dev/null || shift;;
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
[ -z "${G86_CLONE:-}" ] || [ "$DRY" = 1 ] || { echo "REFUSING: G86_CLONE is a dry-run control only"; exit 16; }
chk() { [ "$2" = "$(KJ "$3")" ] || { echo "REFUSING: WRONG VALUE $1 '$2' != kit.json $3 '$(KJ "$3")' — the kit's figures are for that value; re-draft"; exit 11; }; }
for _p in $PRS; do
  eval "_h=\$H_$_p; _b=\$B_$_p; _t=\$T_$_p; _bs=\$BS_$_p"
  chk --head-$_p "$_h" prs.$_p.head_expected; chk --branch-$_p "$_b" prs.$_p.branch; chk --tree-$_p "$_t" prs.$_p.end_tree
  chk --base-$_p "$_bs" prs.$_p.base; chk --parents-n "$NPAR" prs.$_p.parent_count
done
chk --develop "$DEV" develop_at_draft
echo "  $(echo $PRS | wc -w | tr -d ' ') PRs x (head, branch, tree, base) + parents-n + develop present, well-formed and == kit.json (seat '$SEAT' has no kit pin: Wednesday names it; each --base-<n> is that PR's OWN branch point: the four bases differ)"
T="$(date -u +%H%M%S)"; OUTP="$GS/launch_$T"; [ "$DRY" = 1 ] && OUTP="$GS/dry_$T"
_hl=""; for _p in $PRS; do eval "_h=\$H_$_p; _bs=\$BS_$_p"; _hl="$_hl | #$_p ${_h:0:12} base ${_bs:0:12}"; done
echo "LAUNCH ACTION gate86$([ "$DRY" = 1 ] && echo ' (DRY RUN)') $(date '+%Y-%m-%d %H:%M:%S %Z') / $(date -u '+%Y-%m-%dT%H:%M:%SZ')$_hl | parents x$NPAR | develop $DEV | repin-develop ${REPIN:-none} | seat $SEAT | pane $PANE"

echo "--- A. every head must be the one the READY names"
READY="$GS/$(KJ ready)"
[ -s "$READY" ] || { echo "REFUSING: the READY copy is missing or empty ('$READY')"; exit 18; }
_rs="$(shasum -a 256 "$READY" | cut -c1-16)"
[ "$_rs" = "$(KJ ready_sha256_16)" ] || { echo "REFUSING: the READY copy sha256/16 $_rs != kit.json ready_sha256_16 $(KJ ready_sha256_16)"; exit 18; }
echo "  $READY (sha256/16 $_rs, EQUAL to the kit pin) | CONTROL lines naming 'READY': $(/usr/bin/grep -c -i 'READY' "$READY")"
for _p in $PRS; do
  eval "_h=\$H_$_p"
  _n="$(/usr/bin/grep -c -F "$_h" "$READY")"; _q="$(/usr/bin/grep -c -F "#$_p" "$READY")"
  echo "  #$_p: lines naming the head in full $_n | naming #$_p $_q"
  [ "$_n" -ge 1 ] && [ "$_q" -ge 1 ] || { echo "REFUSING: the READY does not name $_h in full (or #$_p)"; exit 18; }
done

echo "--- 2. ONE ls-remote (read verb) from the checkout, GIT_SSH_COMMAND unset, the checkout's own core.sshCommand"
[ -z "${GIT_SSH_COMMAND:-}" ] || echo "  NOTE: GIT_SSH_COMMAND is exported in this shell; every git call below runs under env -u GIT_SSH_COMMAND"
REFS="refs/heads/develop"; for _p in $PRS; do eval "_b=\$B_$_p"; REFS="$REFS refs/pull/$_p/head refs/heads/$_b"; done
if [ -n "${G86_LSFILE:-}" ]; then
  [ "$DRY" = 1 ] || { echo "REFUSING: G86_LSFILE is a dry-run control only"; exit 16; }
  cp "$G86_LSFILE" "$OUTP.lsremote.out"; : > "$OUTP.lsremote.err"; rc=0; echo "  (CONTROL: ls-remote output read from the stand-in $G86_LSFILE)"
else
  env -u GIT_SSH_COMMAND git -C "$CHECKOUT" -c core.sshCommand="$(git -C "$CHECKOUT" config --get core.sshCommand)" ls-remote "$URL" $REFS > "$OUTP.lsremote.out" 2> "$OUTP.lsremote.err"; rc=$?
fi
LSUTC="$(date -u +%Y-%m-%dT%H:%M:%S)"
get() { awk -v r="$1" '$2==r{print $1}' "$OUTP.lsremote.out"; }
CUR_DEV="$(get refs/heads/develop)"
_line="  ls-remote rc=$rc at $(date -u +%H:%M:%SZ) | develop $CUR_DEV"; for _p in $PRS; do eval "_b=\$B_$_p"; _line="$_line | #$_p pull/head $(get refs/pull/$_p/head | cut -c1-12) branch $(get "refs/heads/$_b" | cut -c1-12)"; done; echo "$_line"
[ "$rc" -eq 0 ] && [ -n "$CUR_DEV" ] || { echo "REFUSING: ls-remote failed or returned no develop"; sed 's/^/    stderr: /' "$OUTP.lsremote.err"; exit 2; }
for _p in $PRS; do
  eval "_h=\$H_$_p; _b=\$B_$_p"
  [ "$(get refs/pull/$_p/head)" = "$_h" ] && [ "$(get "refs/heads/$_b")" = "$_h" ] || { echo "REFUSING TO LAUNCH: #$_p origin pull/head '$(get refs/pull/$_p/head)' / branch '$(get "refs/heads/$_b")' != --head-$_p $_h — MISMATCH"; exit 11; }
done

echo "--- 1. PULLS API + census"
if [ "$NOAPI" = 1 ]; then echo "  SKIPPED BY NAME (--no-api, dry run only): the API state and the census are NOT read here"
else
  for _p in $PRS; do
    eval "_h=\$H_$_p"
    python3 "$GS/gh_gate86.py" api --pr $_p --head "$_h" > "$OUTP.api$_p.out" 2> "$OUTP.api$_p.err"; eval "arc_$_p=$?"
  done
  python3 "$GS/gh_gate86.py" census > "$OUTP.census.out" 2> "$OUTP.census.err"; crc=$?
  sed 's/^/    /' "$OUTP".api*.out "$OUTP.census.out" | cut -c1-240
  echo "  api rc: $(for _p in $PRS; do eval "printf '#%s=%s ' $_p \$arc_$_p"; done) census rc=$crc (census rc 1 = OVERLAP-CODE printed above: REPORTED, not refused)"
  for _p in $PRS; do eval "_a=\$arc_$_p"; [ "$_a" -ne 3 ] || { echo "REFUSING: API failure (#$_p)"; exit 3; }; done
  [ "$crc" -ne 3 ] || { echo "REFUSING: a BLIND census control"; exit 3; }
  for _p in $PRS; do eval "_a=\$arc_$_p; _h=\$H_$_p"; [ "$_a" -eq 0 ] || { echo "REFUSING TO LAUNCH: the API does not show #$_p open, unmerged, on develop at $_h"; exit 11; }; done
fi

echo "--- 3b. develop: origin $CUR_DEV | --develop $DEV"
DEV_MOVED=0
if [ "$CUR_DEV" = "$DEV" ]; then echo "  UNMOVED since the draft (#1454 / #1455 branch from it; #1451 / #1452 branch from older commits and develop is 2 / 1 commits past them; a develop that moves is REPORTED here, never hardcoded)."
  [ -z "$REPIN" ] || [ "$REPIN" = "$CUR_DEV" ] || { echo "REFUSING TO LAUNCH: --repin-develop $REPIN is not origin develop $CUR_DEV (stale re-pin)"; exit 10; }
else DEV_MOVED=1; echo "  DEVELOP MOVED: $DEV -> $CUR_DEV (step 3c checks descent and that the advance touches no PR path outside the known docs overlap, and no tooling path)"; fi

echo "--- 3c. the kit's own clone: fetch by sha if absent, C1 per PR + isolation on the develop read now, the c2 / c3 predictions"
if [ ! -d "$CL/.git" ] && [ ! -f "$CL/HEAD" ]; then
  mkdir -p "$GS/_scratch"; env -u GIT_SSH_COMMAND git clone --shared --no-checkout --quiet "$CHECKOUT" "$CL" > "$OUTP.clone.out" 2> "$OUTP.clone.err" || { echo "REFUSING: kit clone failed"; exit 13; }
  echo "  kit clone CREATED at $CL"
fi
git -C "$CL" config remote.origin.url "$URL"
git -C "$CL" config core.sshCommand "$(git -C "$CHECKOUT" config --get core.sshCommand)"
_shas="$CUR_DEV $(KJ trailer_control)"; for _p in $PRS; do eval "_h=\$H_$_p; _bs=\$BS_$_p"; _shas="$_h $_bs $_shas"; done
for s in $_shas; do
  git -C "$CL" cat-file -e "$s^{commit}" 2>/dev/null || env -u GIT_SSH_COMMAND git -C "$CL" fetch --quiet --no-tags --no-write-fetch-head origin "$s" >> "$OUTP.fetch.out" 2>> "$OUTP.fetch.err"
  git -C "$CL" cat-file -e "$s^{commit}" 2>/dev/null || { echo "REFUSING: $s is ABSENT from the kit clone after a by-sha fetch"; tail -3 "$OUTP.fetch.err" 2>/dev/null; exit 19; }
done
for _p in $PRS; do
  eval "_h=\$H_$_p; _t=\$T_$_p; _bs=\$BS_$_p"
  python3 "$GS/c1_pin_gate86.py" pin --repo "$CL" --pr "$_p" --head "$_h" --base "$_bs" --develop "$CUR_DEV" --end-tree "$_t" --parents-n "$NPAR" --no-remote > "$OUTP.c1_$_p.out" 2> "$OUTP.c1_$_p.err"; rc1=$?
  echo "  c1 pin #$_p rc=$rc1 | $(grep -E '^(CHECKED|[0-9]+ FAIL)' "$OUTP.c1_$_p.out" | tr '\n' ' ')"; grep -E '^FAIL' "$OUTP.c1_$_p.out" | sed 's/^/    /' | cut -c1-240
  # [g78] EVERY c1 FAIL refuses (rc 13).
  _hard="$(grep -E '^FAIL ' "$OUTP.c1_$_p.out" | wc -l | tr -d ' ')"
  [ "$rc1" = 0 ] && [ "$_hard" = 0 ] || { echo "REFUSING TO LAUNCH: C1 FAILED for #$_p at the head ($_hard FAIL line(s), c1 rc $rc1)"; exit 13; }
  python3 "$GS/c1_pin_gate86.py" docsbase --repo "$CL" --pr "$_p" --head "$_h" --base "$_bs" --develop "$CUR_DEV" > "$OUTP.c1_docsbase_$_p.out" 2> "$OUTP.c1_docsbase_$_p.err"; rcp=$?
  echo "  c1 docsbase #$_p rc=$rcp | $(grep -E '^(CHECKED|[0-9]+ FAIL)' "$OUTP.c1_docsbase_$_p.out" | tr '\n' ' ')"; grep -E '^FAIL' "$OUTP.c1_docsbase_$_p.out" | sed 's/^/    /' | cut -c1-240
  [ "$rcp" = 0 ] || { echo "REFUSING TO LAUNCH: the DOCS-PARENT check failed for #$_p (G83-1: the fragment base must be merge-base(develop, head) == --base-$_p, never head^; each doc must be base + ONE exact insert before the closing tags; the wrong-parent controls must refuse)"; exit 13; }
done
_ISO=""; for _p in $PRS; do eval "_h=\$H_$_p"; _ISO="$_ISO --head $_p=$_h"; done
python3 "$GS/c1_pin_gate86.py" isolation --repo "$CL" --develop "$CUR_DEV" $_ISO > "$OUTP.c1_isolation.out" 2> "$OUTP.c1_isolation.err"; rci=$?
echo "  c1 isolation rc=$rci | $(grep -E '^(CHECKED|[0-9]+ FAIL)' "$OUTP.c1_isolation.out" | tr '\n' ' ')"; grep -E '^FAIL' "$OUTP.c1_isolation.out" | sed 's/^/    /' | cut -c1-240
[ "$rci" = 0 ] || { echo "REFUSING TO LAUNCH: the ISOLATION matrix failed (a PR touches another's files outside the allowed docs / yaml overlap, or a block number is taken on the develop read now)"; exit 13; }
for _p in $PRS; do
  eval "_h=\$H_$_p; _bs=\$BS_$_p"
  python3 "$GS/c2_code_gate86.py" claims --repo "$CL" --pr "$_p" --head "$_h" --base "$_bs" --yaml-structural > "$OUTP.c2claims_$_p.out" 2> "$OUTP.c2claims_$_p.err"; rc2=$?
  echo "  c2 claims #$_p rc=$rc2 | $(grep -E '^(CHECKED|[0-9]+ FAIL)' "$OUTP.c2claims_$_p.out" | tr '\n' ' ') (a PREDICTION for the gate, not refused)"
  grep -E '^FAIL' "$OUTP.c2claims_$_p.out" | sed 's/^/    /' | cut -c1-240
done
_CMP=""; for _p in $PRS; do eval "_h=\$H_$_p"; _CMP="$_CMP --head $_p=$_h"; done
python3 "$GS/c3_cells_gate86.py" compose --clone "$CL" --develop "$CUR_DEV" $_CMP --out "$OUTP.compose" > "$OUTP.compose.out" 2> "$OUTP.compose.err"; rcc=$?
echo "  c3 compose rc=$rcc | $(grep -E '^(CHECKED|[0-9]+ FAIL)' "$OUTP.compose.out" | tr '\n' ' ') (the 24-order merge-in PREDICTION for the gate, not refused)"; grep -E '^FAIL' "$OUTP.compose.out" | sed 's/^/    /' | cut -c1-240
if [ "$DEV_MOVED" = 1 ]; then
  if [ -z "$REPIN" ]; then echo "REFUSING TO LAUNCH: develop moved (c1 P12 and isolation passed against it: the advance touched no PR path outside the known docs overlap, and no tooling path). To re-pin and launch over it, re-run with:  --repin-develop $CUR_DEV"; exit 10
  elif [ "$REPIN" != "$CUR_DEV" ]; then echo "REFUSING TO LAUNCH: --repin-develop $REPIN is not origin develop $CUR_DEV (stale re-pin)"; exit 10; fi
  echo "repin $(date -u +%Y-%m-%dT%H:%M:%SZ): develop $DEV -> $CUR_DEV" > "$OUTP.repin.txt"; echo "  RE-PINNED develop -> $CUR_DEV ($OUTP.repin.txt)"
fi

echo "--- R. render the prompt (develop $CUR_DEV, seat $SEAT, ls-remote $LSUTC UTC)"
_RARGS=""; for _p in $PRS; do eval "_h=\$H_$_p; _b=\$B_$_p; _t=\$T_$_p; _bs=\$BS_$_p"; _RARGS="$_RARGS $_p $_h $_b $_t $_bs"; done
python3 - "$GS/prompt_gate86.txt" "$GS/prompt_gate86.rendered.txt" "$GS/head_at_launch.txt" "$NPAR" "$CUR_DEV" "$SEAT" "$LSUTC" $_RARGS <<'PYEOF' || { echo "REFUSING: render failed"; exit 9; }
import sys
a = sys.argv[1:]
src, dst, hf, npar, dev, seat, lsutc = a[:7]
rest = a[7:]
prs = [rest[5 * i: 5 * i + 5] for i in range(len(rest) // 5)]      # [pr, head, branch, tree, base]
assert len(prs) * 5 == len(rest) and len(prs) == 4, 'expected four PRs'
t = open(src, encoding='utf-8').read()
want = dict((('{{HEAD%s}}' % p[0]), (2, p[1])) for p in prs); want.update({'{{DEVELOP}}': (2, dev), '@MERGE_SEAT@': (2, seat), '{{LSUTC}}': (1, lsutc)})
for tok, (n, _) in want.items():
    if t.count(tok) < n: raise SystemExit('template token %s x%d (want >= %d)' % (tok, t.count(tok), n))
counts = dict((tok, t.count(tok)) for tok in want)
for tok, (_, val) in want.items(): t = t.replace(tok, val)
if '{{' in t or '@MERGE_SEAT@' in t: raise SystemExit('an unknown {{token}} or the @MERGE_SEAT@ token survived the render')
open(dst, 'w', encoding='utf-8').write(t)
open(hf, 'w').write(''.join('P %s %s %s\n' % (p[0], p[2], p[1]) for p in prs) + ''.join('B %s %s %s\n' % (p[0], p[4], npar) for p in prs) + ''.join('T %s %s\n' % (p[0], p[3]) for p in prs) + 'D %s\nS %s\n' % (dev, seat))
print('  rendered %s -> %s (%d bytes); head file %s (P / B / T x%d, D, S)' % (counts, dst, len(t.encode()), hf, len(prs)))
PYEOF

echo "--- 0. routing: the pane must be in inbox_routing.conf (READ only here)"
/usr/bin/grep -c -x -F "$LINE" "$ROUTING" > "$OUTP.routing.out" 2> "$OUTP.routing.err"; rc=$?
echo "  $ROUTING — exact line present: $(cat "$OUTP.routing.out") (grep rc=$rc; want 1 / rc 0). CONTROL: agentmail lines in the file = $(/usr/bin/grep -c -i 'agentmail' "$ROUTING")"
if [ "$rc" -ne 0 ]; then
  if [ "$DRY" = 1 ]; then echo "  (DRY RUN: reported, not refused — the real run refuses rc 1; ROUTING_PROPOSAL.txt)"; else echo "REFUSING: add the routing line first (ROUTING_PROPOSAL.txt): $LINE"; exit 1; fi
fi

if [ "$DRY" = 1 ]; then
  echo "--- 6 (dry). the launcher's own --check"
  # a dry run driven by the G86_LSFILE stand-in hands the SAME stand-in to the launcher (G86_LS), so a SIM develop is checked end to end
  # instead of being refused by the launcher's real ls-remote; the launcher names the override in its output.
  if [ -n "${G86_LSFILE:-}" ]; then G86_LS="$G86_LSFILE" "$L" --check > "$OUTP.launcher_check.out" 2> "$OUTP.launcher_check.err"; rc=$?
  else "$L" --check > "$OUTP.launcher_check.out" 2> "$OUTP.launcher_check.err"; rc=$?; fi
  sed 's/^/    /' "$OUTP.launcher_check.out" "$OUTP.launcher_check.err"; echo "  launcher --check rc=$rc"
  [ "$rc" -eq 0 ] || { echo "DRY RUN: the launcher refused under --check (rc $rc)"; exit 13; }
  echo "DRY RUN COMPLETE $(date -u '+%Y-%m-%dT%H:%M:%SZ') —$_hl, develop $CUR_DEV; NO usage gate, NO cockpit.sh add, NO pane was touched. The real run continues with the override check, the usage gate, --check and cockpit.sh add"; exit 0
fi
echo "--- 4. no test override on a real launch"
[ "$(env | grep -c '^G86_')" = 0 ] || { echo "REFUSING TO LAUNCH: a G86_* override is set"; exit 16; }
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
echo "LAUNCHED $(date -u '+%Y-%m-%dT%H:%M:%SZ')$_hl; develop at launch $CUR_DEV — now verify RUNG 5 (KIT_REPORT §5)"
