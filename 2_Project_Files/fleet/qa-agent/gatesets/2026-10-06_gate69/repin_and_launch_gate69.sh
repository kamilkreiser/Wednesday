#!/bin/bash
# repin_and_launch_gate69.sh — the LAUNCH ACTION for gate69 (BATCHED T1: #1395 KS-1305 always; PR B KS-1256 when supplied). Adapted from
# repin_and_launch_gate68.sh. THE HEADS ARE PARAMETERS and PR B IS A PARAMETER: without --b-pr/--b-head the kit renders an A-ONLY gate.
# It READS everything at launch and never trusts a pin it did not just re-read (Kam 2026-09-18):
#   (A)  each READY must name its head in full (A: kit prs.A.ready; B: --b-ready or kit prs.B.ready, and must name #<b-pr>)        — rc 18
#        a head != the kit's expected head refuses unless --accept-unexpected-head (then every drafter figure for it is VOID)    — rc 11
#   (R)  render prompt_gate69.txt -> prompt_gate69.rendered.txt ({{HEAD_A}} {{HEAD_B}} {{PR_B}} {{DEVELOP}}; [[B]]…[[/B]] kept or cut,
#        [[NOB]]…[[/NOB]] the reverse) + head_at_launch.txt                                                                         — rc 9
#   (0)  the pane is routed in inbox_routing.conf — rc 1 (a dry run REPORTS it instead)
#   (1)  gh_gate69.py api per PR + census: rc 3 API failure / blind control, rc 15 OVERLAP
#   (2)  ONE `git ls-remote` from the Secuura checkout (read verb) — rc 2
#   (3)  rc 11 unless, per PR, input == READY == API head == pull/head == branch, open, not merged, base develop
#   (3b) develop: == kit develop_at_draft (4eaf7741a6a4) -> on; MOVED -> advance printed; rc 10 unless `--repin-develop <that 40-hex>`;
#        hard rc 10 if it does not descend from the kit develop or touches a code / hook path of either PR
#   (3c) THE KIT'S OWN CLONE (<kit>/_scratch/clone, `clone --shared` of the checkout, origin + core.sshCommand copied, NEVER an exported
#        GIT_SSH_COMMAND): fetch heads + develop BY SHA; c1 per PR (rc 13 — B's P8 alone is the drafter's MEASURED defect and does not
#        refuse); c4 chain (both orders) + mergetree per PR on the develop READ NOW (printed, never refused)
#   (4)  G69_* overrides refuse a real launch — rc 16;  (5) the usage gate — rc 12;  (6) the launcher's --check — rc 13;  (7) cockpit add — rc 14
# --dry-run: A, R, 0-3c and the launcher's --check, then stops. Output: launch_<HHMMSS>.* (dry: dry_<HHMMSS>.*) beside this script.
# Controls-only overrides: G69_ROUTING (routing stand-in), G69_LSFILE (ls-remote stand-in; DRY RUN ONLY).
# Usage: repin_and_launch_gate69.sh <HEAD_A 40-hex> [--b-pr <n> --b-head <40-hex> [--b-ready <file>]] [--dry-run]
#        [--repin-develop <40-hex>] [--accept-unexpected-head]      (run under `script -q /dev/null`)
set -u
export PYTHONDONTWRITEBYTECODE=1
GS="$(dirname "$(/bin/realpath "$0")")"
CHECKOUT='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
KJ() { python3 -c 'import json,sys; v=json.load(open(sys.argv[1]))
for k in sys.argv[2].split("."): v=v[k]
print(" ".join(v) if isinstance(v,list) else ("" if v is None else v))' "$GS/kit.json" "$1"; }
ROUTING="${G69_ROUTING:-$(KJ routing)}"; KDEV="$(KJ develop_at_draft)"; PANE="$(KJ pane)"; LINE="$(KJ routing_line)"
A_EXP="$(KJ prs.A.head_expected)"; A_BR="$(KJ prs.A.branch)"; A_READY="$(KJ prs.A.ready)"
B_EXP="$(KJ prs.B.head_expected)"; B_BR_KIT="$(KJ prs.B.branch)"; B_READY_KIT="$(KJ prs.B.ready)"
L="$GS/$(KJ launcher)"; CL="$GS/_scratch/clone"
USAGE="usage: repin_and_launch_gate69.sh <HEAD_A 40-hex> [--b-pr <n> --b-head <40-hex> [--b-ready <file>]] [--dry-run] [--repin-develop <40-hex>] [--accept-unexpected-head]"
HA="${1:-}"; DRY=0; REPIN=""; BPR=""; HB=""; BREADY=""; ACCEPT=0
shift 1 2>/dev/null
while [ $# -gt 0 ]; do
  case "$1" in --dry-run) DRY=1; shift;; --accept-unexpected-head) ACCEPT=1; shift;; --repin-develop) REPIN="${2:-}"; shift 2 2>/dev/null || shift;;
    --b-pr) BPR="${2:-}"; shift 2 2>/dev/null || shift;; --b-head) HB="${2:-}"; shift 2 2>/dev/null || shift;; --b-ready) BREADY="${2:-}"; shift 2 2>/dev/null || shift;;
    *) echo "$USAGE"; exit 9;; esac
done
printf '%s' "$HA" | grep -qE '^[0-9a-f]{40}$' || { echo "REFUSING: HEAD_A must be the FULL 40-hex sha, got '$HA'"; exit 9; }
B_IN=0
if [ -n "$BPR$HB" ]; then
  printf '%s' "$BPR" | grep -qE '^[0-9]+$' && printf '%s' "$HB" | grep -qE '^[0-9a-f]{40}$' || { echo "REFUSING: PR B needs BOTH --b-pr <n> and --b-head <40-hex> (got '$BPR' / '$HB')"; exit 9; }
  B_IN=1; BREADY="${BREADY:-$B_READY_KIT}"
fi
[ -z "$REPIN" ] || printf '%s' "$REPIN" | grep -qE '^[0-9a-f]{40}$' || { echo "REFUSING: --repin-develop must be the FULL 40-hex sha, got '$REPIN'"; exit 9; }
T="$(date -u +%H%M%S)"; OUTP="$GS/launch_$T"; [ "$DRY" = 1 ] && OUTP="$GS/dry_$T"
echo "LAUNCH ACTION gate69$([ "$DRY" = 1 ] && echo ' (DRY RUN)') $(date '+%Y-%m-%d %H:%M:%S %Z') / $(date -u '+%Y-%m-%dT%H:%M:%SZ') | #1395 $HA | PR B $([ "$B_IN" = 1 ] && echo "#$BPR $HB" || echo 'NOT INCLUDED') | kit develop $KDEV | repin-develop ${REPIN:-none} | pane $PANE"

echo "--- A. each head must be the one its READY names"
chk_ready() { # file head label [prnum]
  [ -n "$1" ] && [ -s "$1" ] || { echo "REFUSING: READY for $3 missing or empty ('$1')"; exit 18; }
  _n="$(/usr/bin/grep -c -F "$2" "$1")"; _c="$(/usr/bin/grep -c -i 'READY' "$1")"; _p=1; [ -n "${4:-}" ] && _p="$(/usr/bin/grep -c -F "#$4" "$1")"
  echo "  $3: $1 (sha256/16 $(shasum -a 256 "$1" | cut -c1-16)): lines naming the head in full $_n | naming #${4:-n/a} $_p | CONTROL lines naming 'READY' $_c"
  [ "$_n" -ge 1 ] && [ "$_p" -ge 1 ] || { echo "REFUSING: the READY for $3 does not name $2 in full (or #${4:-})"; exit 18; }
}
chk_ready "$A_READY" "$HA" "#1395" 1395
[ "$B_IN" = 1 ] && chk_ready "$BREADY" "$HB" "PR B" "$BPR"
for pair in "A $HA $A_EXP" "B $HB $B_EXP"; do
  set -- $pair; [ "$1" = B ] && [ "$B_IN" = 0 ] && continue
  if [ "$2" != "$3" ]; then
    if [ "$ACCEPT" = 1 ]; then echo "  WARNING: PR $1 head $2 != kit expected $3 — accepted: EVERY drafter figure for PR $1 is VOID"
    else echo "REFUSING: PR $1 head $2 != kit expected $3 (the drafter's figures are for $3). Re-draft, or pass --accept-unexpected-head"; exit 11; fi
  fi
done
set --

echo "--- 2. ONE ls-remote (read verb) from the checkout"
B_BR="$B_BR_KIT"
REFS="refs/heads/develop refs/pull/1395/head refs/heads/$A_BR"; [ "$B_IN" = 1 ] && REFS="$REFS refs/pull/$BPR/head refs/heads/$B_BR"
if [ -n "${G69_LSFILE:-}" ]; then
  [ "$DRY" = 1 ] || { echo "REFUSING: G69_LSFILE is a dry-run control only"; exit 16; }
  cp "$G69_LSFILE" "$OUTP.lsremote.out"; : > "$OUTP.lsremote.err"; rc=0; echo "  (CONTROL: ls-remote output read from the stand-in $G69_LSFILE)"
else
  git -C "$CHECKOUT" ls-remote origin $REFS > "$OUTP.lsremote.out" 2> "$OUTP.lsremote.err"; rc=$?
fi
get() { awk -v r="$1" '$2==r{print $1}' "$OUTP.lsremote.out"; }
CUR_DEV="$(get refs/heads/develop)"
echo "  ls-remote rc=$rc at $(date -u +%H:%M:%SZ) | develop $CUR_DEV | #1395 pull/head $(get refs/pull/1395/head) branch $(get "refs/heads/$A_BR")$([ "$B_IN" = 1 ] && echo " | #$BPR pull/head $(get "refs/pull/$BPR/head") branch $(get "refs/heads/$B_BR")")"
[ "$rc" -eq 0 ] && [ -n "$CUR_DEV" ] || { echo "REFUSING: ls-remote failed or returned no develop"; sed 's/^/    stderr: /' "$OUTP.lsremote.err"; exit 2; }

echo "--- R. render the prompt (develop $CUR_DEV)"
python3 - "$GS/prompt_gate69.txt" "$GS/prompt_gate69.rendered.txt" "$GS/head_at_launch.txt" "$HA" "$A_BR" "$B_IN" "$BPR" "$HB" "$B_BR" "$CUR_DEV" <<'PYEOF' || { echo "REFUSING: render failed"; exit 9; }
import re, sys
src, dst, hf, ha, abr, bin_, bpr, hb, bbr, dev = sys.argv[1:11]
t = open(src, encoding='utf-8').read()
na, nb, npr, nd = t.count('{{HEAD_A}}'), t.count('{{HEAD_B}}'), t.count('{{PR_B}}'), t.count('{{DEVELOP}}')
if na < 6 or nb < 6 or npr < 10 or nd < 3: raise SystemExit('template tokens HEAD_A x%d HEAD_B x%d PR_B x%d DEVELOP x%d (want >= 6/6/10/3)' % (na, nb, npr, nd))
if bin_ == '1':
    t = re.sub(r'\[\[NOB\]\].*?\[\[/NOB\]\]', '', t, flags=re.S); t = t.replace('[[B]]', '').replace('[[/B]]', '')
    t = t.replace('{{HEAD_B}}', hb).replace('{{PR_B}}', bpr)
else:
    t = re.sub(r'\[\[B\]\].*?\[\[/B\]\]', '', t, flags=re.S); t = t.replace('[[NOB]]', '').replace('[[/NOB]]', '')
    if '{{HEAD_B}}' in t or '{{PR_B}}' in t: raise SystemExit('A-only render left a PR B token outside a [[B]] block')
t = t.replace('{{HEAD_A}}', ha).replace('{{DEVELOP}}', dev)
open(dst, 'w', encoding='utf-8').write(t)
open(hf, 'w').write('A 1395 %s %s\n' % (abr, ha) + ('B %s %s %s\n' % (bpr, bbr, hb) if bin_ == '1' else ''))
print('  rendered HEAD_A x%d HEAD_B x%d PR_B x%d DEVELOP x%d, PR B %s -> %s (%d bytes); head file %s' % (na, nb, npr, nd, 'INCLUDED' if bin_ == '1' else 'CUT (A-only)', dst, len(t.encode()), hf))
PYEOF

echo "--- 0. routing: the pane must be in inbox_routing.conf"
/usr/bin/grep -c -x -F "$LINE" "$ROUTING" > "$OUTP.routing.out" 2> "$OUTP.routing.err"; rc=$?
echo "  $ROUTING — exact line present: $(cat "$OUTP.routing.out") (grep rc=$rc; want 1 / rc 0). CONTROL: agentmail lines in the file = $(/usr/bin/grep -c -i 'agentmail' "$ROUTING")"
if [ "$rc" -ne 0 ]; then
  if [ "$DRY" = 1 ]; then echo "  (DRY RUN: reported, not refused — the real run refuses rc 1; ROUTING_LINE.txt)"; else echo "REFUSING: add the routing line first (ROUTING_LINE.txt): $LINE"; exit 1; fi
fi

echo "--- 1. PULLS API (per PR) + census"
python3 "$GS/gh_gate69.py" api --pr A --head "$HA" > "$OUTP.api_A.out" 2> "$OUTP.api_A.err"; arcA=$?; arcB=0
[ "$B_IN" = 1 ] && { python3 "$GS/gh_gate69.py" api --pr B --b-pr "$BPR" --head "$HB" > "$OUTP.api_B.out" 2> "$OUTP.api_B.err"; arcB=$?; }
if [ "$B_IN" = 1 ]; then python3 "$GS/gh_gate69.py" census --b-pr "$BPR" > "$OUTP.census.out" 2> "$OUTP.census.err"; crc=$?
else python3 "$GS/gh_gate69.py" census --a-only > "$OUTP.census.out" 2> "$OUTP.census.err"; crc=$?; fi
sed 's/^/    /' "$OUTP.api_A.out" $([ "$B_IN" = 1 ] && echo "$OUTP.api_B.out") "$OUTP.census.out" | cut -c1-240
echo "  api A rc=$arcA B rc=$arcB census rc=$crc"
[ "$arcA" -eq 3 ] || [ "$arcB" -eq 3 ] || [ "$crc" -eq 3 ] && { echo "REFUSING: API failure or a BLIND census control"; exit 3; }
[ "$crc" -eq 1 ] && { echo "REFUSING: an OVERLAP on a batch code path (or a KS-1305 / KS-1256 title) — read it first"; exit 15; }

echo "--- 3. the heads: input == READY == API == pull/head == branch; open, not merged, on develop"
okhead() { # label input apifile pull branch
  A_LINE="$(grep '^API #' "$3")"; set -- "$1" "$2" "$3" "$4" "$5" $A_LINE
  # API #<n> head <sha> branch <ref> base <ref> state <s> merged <b> ...
  [ "${9:-}" = "$2" ] && [ "$4" = "$2" ] && [ "$5" = "$2" ] && [ "${15:-}" = open ] && [ "${17:-}" = False ] && [ "${13:-}" = develop ]
}
okhead A "$HA" "$OUTP.api_A.out" "$(get refs/pull/1395/head)" "$(get "refs/heads/$A_BR")" || { echo "REFUSING TO LAUNCH: #1395's head is not $HA on every instrument, or the PR is not open / merged / off develop"; exit 11; }
if [ "$B_IN" = 1 ]; then okhead B "$HB" "$OUTP.api_B.out" "$(get "refs/pull/$BPR/head")" "$(get "refs/heads/$B_BR")" || { echo "REFUSING TO LAUNCH: #$BPR's head is not $HB on every instrument, or the PR is not open / merged / off develop (branch per kit: $B_BR)"; exit 11; }; fi
echo "  ALL INSTRUMENTS AGREE with the input head(s)."

echo "--- 3b. develop: origin $CUR_DEV | kit (at drafting) $KDEV"
DEV_MOVED=0
if [ "$CUR_DEV" = "$KDEV" ]; then echo "  UNMOVED since drafting (both PRs branch from 3f9ff4e1e1b9: each still needs the docs-only merge-in)."
  [ -z "$REPIN" ] || [ "$REPIN" = "$CUR_DEV" ] || { echo "REFUSING TO LAUNCH: --repin-develop $REPIN is not origin develop $CUR_DEV (stale re-pin)"; exit 10; }
else DEV_MOVED=1; echo "  DEVELOP MOVED: $KDEV -> $CUR_DEV  (every kit prediction is VOID; step 3c recomputes)"; fi

echo "--- 3c. the kit's own clone: fetch by sha, C1 per PR, the merge-in predictions RECOMPUTED on the develop read now"
[ -z "${GIT_SSH_COMMAND:-}" ] || { echo "REFUSING: GIT_SSH_COMMAND is exported in this shell (never export it; the clone carries core.sshCommand)"; exit 16; }
if [ ! -d "$CL/.git" ] && [ ! -f "$CL/HEAD" ]; then
  mkdir -p "$GS/_scratch"; git clone --shared --no-checkout --quiet "$CHECKOUT" "$CL" > "$OUTP.clone.out" 2> "$OUTP.clone.err" || { echo "REFUSING: kit clone failed"; exit 13; }
  git -C "$CL" config remote.origin.url "$(git -C "$CHECKOUT" config --get remote.origin.url)"
  git -C "$CL" config core.sshCommand "$(git -C "$CHECKOUT" config --get core.sshCommand)"
fi
for s in "$HA" "$CUR_DEV" "$KDEV" $([ "$B_IN" = 1 ] && echo "$HB"); do
  git -C "$CL" cat-file -e "$s^{commit}" 2>/dev/null || git -C "$CL" fetch --quiet origin "$s" >> "$OUTP.fetch.out" 2>> "$OUTP.fetch.err" || { echo "REFUSING: fetch by sha $s into the kit clone failed"; tail -3 "$OUTP.fetch.err"; exit 13; }
done
if [ "$DEV_MOVED" = 1 ]; then
  python3 - "$GS" "$CL" "$KDEV" "$CUR_DEV" > "$OUTP.advance.out" 2> "$OUTP.advance.err" <<'PYEOF'
import os, subprocess, sys
gs, cl, kd, nd = sys.argv[1:5]; sys.path.insert(0, gs)
from lib_gate69 import K
anc = subprocess.run(['git', '-C', cl, 'merge-base', '--is-ancestor', kd, nd]).returncode == 0
files = [f for f in subprocess.run(['git', '-C', cl, 'diff', '--name-only', kd, nd], capture_output=True, text=True).stdout.split('\n') if f]
code = set(K['prs']['A']['code_paths']) | set(K['prs']['B']['code_paths']) | set(K['hook_blobs'])
hit = sorted(set(files) & code)
print('STATUS %s' % ('ahead' if anc else 'NOT-A-DESCENDANT')); print('ADVANCE %d path(s); docs among them %d' % (len(files), len(set(files) & {K['flow'], K['cheat']})))
print('KITHIT %s' % (hit or 'none'))
for f in files[:40]: print('  path %s' % f)
raise SystemExit(0 if anc and not hit else 10)
PYEOF
  arc=$?; sed 's/^/    /' "$OUTP.advance.out" | cut -c1-200
  [ "$arc" -eq 0 ] || { echo "REFUSING TO LAUNCH (NOT re-pinnable): develop does not descend from the kit develop or touches a CODE / hook path (rc $arc)"; exit 10; }
fi
python3 "$GS/c1_pin_gate69.py" --pr A --repo "$CL" --head "$HA" --develop "$CUR_DEV" --no-remote > "$OUTP.c1A.out" 2> "$OUTP.c1A.err"; rcA=$?
echo "  c1 A rc=$rcA | $(grep -E '^(CHECKED|[0-9]+ FAIL)' "$OUTP.c1A.out" | tr '\n' ' ')"; grep -E '^FAIL' "$OUTP.c1A.out" | sed 's/^/    /' | cut -c1-240
[ "$rcA" -eq 0 ] || { echo "REFUSING TO LAUNCH: C1 FAILED for #1395 at its head"; exit 13; }
if [ "$B_IN" = 1 ]; then
  python3 "$GS/c1_pin_gate69.py" --pr B --b-pr "$BPR" --repo "$CL" --head "$HB" --develop "$CUR_DEV" --no-remote > "$OUTP.c1B.out" 2> "$OUTP.c1B.err"; rcB=$?
  _fails="$(grep -E '^[0-9]+ FAIL' "$OUTP.c1B.out")"
  echo "  c1 B rc=$rcB | $(grep -E '^CHECKED' "$OUTP.c1B.out") | $_fails"; grep -E '^FAIL' "$OUTP.c1B.out" | sed 's/^/    /' | cut -c1-240
  if [ "$rcB" -ne 0 ] && [ "$_fails" != "1 FAIL (P8)" ]; then echo "REFUSING TO LAUNCH: C1 FAILED for #$BPR beyond the drafter's measured P8 defect"; exit 13; fi
  [ "$rcB" -ne 0 ] && echo "  (P8 alone: the drafter's MEASURED defect — foreign hyphenated keys in the commit messages; the gate rules it)"
fi
export G69_SCRATCH="$GS/_scratch/kitout"
C4B=(--a-only); [ "$B_IN" = 1 ] && C4B=(--b-pr "$BPR" --head-b "$HB")
python3 "$GS/c4_docs_gate69.py" chain --repo "$CL" --head-a "$HA" "${C4B[@]}" --develop-after "$CUR_DEV" > "$OUTP.chain.out" 2> "$OUTP.chain.err"; crc=$?
echo "  c4 chain rc=$crc"; grep -E '^  (A alone|B alone|B on SIM|A on SIM|FINAL)' "$OUTP.chain.out" | sed 's/^/  /' | cut -c1-200
for w in A $([ "$B_IN" = 1 ] && echo B); do
  python3 "$GS/c4_docs_gate69.py" mergetree --pr "$w" --repo "$CL" --head-a "$HA" "${C4B[@]}" --develop-after "$CUR_DEV" > "$OUTP.mergetree_$w.out" 2> "$OUTP.mergetree_$w.err"
  echo "  PR $w: $(grep -E '^(AGREE|DIVERGENCE)' "$OUTP.mergetree_$w.out" | cut -c1-200)"; grep -E 'conflicted paths' "$OUTP.mergetree_$w.out" | sed 's/^/    /' | cut -c1-200
done
unset G69_SCRATCH
if [ "$DEV_MOVED" = 1 ]; then
  if [ -z "$REPIN" ]; then echo "REFUSING TO LAUNCH: develop moved. To re-pin and launch over it, re-run with:  --repin-develop $CUR_DEV"; exit 10
  elif [ "$REPIN" != "$CUR_DEV" ]; then echo "REFUSING TO LAUNCH: --repin-develop $REPIN is not origin develop $CUR_DEV (stale re-pin)"; exit 10; fi
  { echo "repin $(date -u +%Y-%m-%dT%H:%M:%SZ): develop $KDEV -> $CUR_DEV"; cat "$OUTP.advance.out"; } > "$OUTP.repin.txt"; echo "  RE-PINNED develop -> $CUR_DEV ($OUTP.repin.txt)"
fi

if [ "$DRY" = 1 ]; then
  echo "--- 6 (dry). the launcher's own --check"
  "$L" --check > "$OUTP.launcher_check.out" 2> "$OUTP.launcher_check.err"; rc=$?
  sed 's/^/    /' "$OUTP.launcher_check.out" "$OUTP.launcher_check.err"; echo "  launcher --check rc=$rc"
  [ "$rc" -eq 0 ] || { echo "DRY RUN: the launcher refused under --check (rc $rc)"; exit 13; }
  echo "DRY RUN COMPLETE $(date -u '+%Y-%m-%dT%H:%M:%SZ') — #1395 $HA$([ "$B_IN" = 1 ] && echo ", #$BPR $HB"), develop $CUR_DEV; the real run continues with the override check, the usage gate, --check and cockpit.sh add"; exit 0
fi
echo "--- 4. no test override on a real launch"
[ "$(env | grep -c '^G69_')" = 0 ] || { echo "REFUSING TO LAUNCH: a G69_* override is set"; exit 16; }
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
echo "LAUNCHED $(date -u '+%Y-%m-%dT%H:%M:%SZ') #1395 at $HA$([ "$B_IN" = 1 ] && echo " + #$BPR at $HB"); develop at launch $CUR_DEV — now verify RUNG 5 (README §7)"
