#!/bin/bash
# c2_legs_gateD2.sh — gateD2 C2: the pre-push preflight legs 2 (lockfile-cleanroom.sh), 6 (audit-gate.mjs) and 7 (audit-locks.mjs), run by
# the TESTER in its OWN worktree (a NEW COPY of gate54f's c5_legs_gate54f.sh, re-keyed: this PR REMOVES the GHSA-86w9 row, so the reading
# that matters is the CLEANUP list). macOS bash 3.2 / zsh safe: every rc is read as `cmd > f 2> g; rc=$?` on its own line, never via a pipe.
#
#   c2_legs_gateD2.sh --help
#   c2_legs_gateD2.sh plan <repo> <sha>                 READ-ONLY: the leg files exist at <sha>; both gates read AUDIT_BASELINE_PATH there.
#   c2_legs_gateD2.sh parse-selftest <outdir>           the parsers on planted lines: a FAIL row counts as FAIL, a CLEANUP row as CLEANUP.
#   c2_legs_gateD2.sh run <devdir> <label> <outdir>     <devdir> = <your worktree>/Blockchain/Dev at the HEAD. Installs scripts/audit's OWN
#        lock (npm ci --ignore-scripts), then legs 2, 6, 7. Want: rc 0 0 0; GHSA-86w9-cpqp-85rv named NOWHERE (no FAIL row, no CLEANUP row);
#        the CLEANUP count printed (builder: 15). rc 2 from a leg = SKIP (registry unreachable) and is NEVER a pass.
#   c2_legs_gateD2.sh cleanup-control <devdir> <outdir> <base-baseline.json>
#        the MUST-HIT CONTROL: legs 6 and 7 at the HEAD tree with the BASE baseline passed by AUDIT_BASELINE_PATH (the worktree is never
#        edited; extract it with `git show <base>:Blockchain/Dev/scripts/audit/audit-baseline.json > <outdir>/base_baseline.json`). Want:
#        GHSA-86w9-cpqp-85rv named in a CLEANUP list (the dependency is gone, so the stale row is reported) — proving `named nowhere` at head
#        is a reading of an instrument that can see it. NO-OP CONTROL in the same run: the head baseline copied to <outdir> by the same
#        variable gives the same rc as `run`.
# Every write is inside <outdir>, which must lie under /private/tmp/claude-501/ or the QA reports root (checked LEXICALLY before any mkdir).
# Exit: 0 every expectation held; 1 one did not (MISMATCH lines say which); 2 usage / refusal.
set -u
GS="$(dirname "$(/bin/realpath "$0")")"
RM="GHSA-86w9-cpqp-85rv"
usage() { sed -n '2,22p' "$0" | sed 's/^# \{0,1\}//'; }
MODE="${1:-}"
[ -n "$MODE" ] || { usage; exit 2; }
if [ "$MODE" = "--help" ] || [ "$MODE" = "-h" ]; then usage; exit 0; fi
guard_out() {
  _l="$(python3 -c 'import os,sys; print(os.path.abspath(sys.argv[1]))' "$1")"
  case "$_l" in "/private/tmp/claude-501/"*|"/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/"*) ;; *) echo "REFUSING: outdir $_l is not under /private/tmp/claude-501/ or the QA reports root (nothing was created)"; exit 2;; esac
  mkdir -p "$_l" || exit 2; OUT="$_l"
}
fails() { sed -n 's/^  - \(GHSA-[a-z0-9]\{4\}-[a-z0-9]\{4\}-[a-z0-9]\{4\}\) \[.*$/\1/p' "$1" | sort -u; }
cleanups() {  # ids listed under a CLEANUP header (`  - GHSA-x (pkg, ticket)`), in stdout or stderr
  awk '/^CLEANUP/{c=1;next} /^[A-Z]/{c=0} c' "$1" | sed -n 's/^  - \(GHSA-[a-z0-9]\{4\}-[a-z0-9]\{4\}-[a-z0-9]\{4\}\) (.*$/\1/p' | sort -u
}
class() { case "$1" in 0) echo PASS;; 1) echo FAIL;; 2) echo "SKIP (not a pass)";; 3) echo REFUSED;; *) echo "ERROR rc $1";; esac; }
guard_dev() {
  DEV="$1"
  case "$(python3 -c 'import os,sys; print(os.path.realpath(sys.argv[1]))' "$DEV")" in /Volumes/DevMASTER/*) echo "REFUSING: $DEV is on /Volumes/DevMASTER — run legs only in YOUR OWN worktree under /private/tmp/claude-501/"; exit 2;; esac
  [ -f "$DEV/scripts/audit/audit-gate.mjs" ] && [ -f "$DEV/scripts/preflight/lockfile-cleanroom.sh" ] || { echo "REFUSING: $DEV is not a Blockchain/Dev directory"; exit 2; }
  DIRTY="$(git -C "$DEV" status --porcelain --untracked-files=no 2>&1)"
  [ -z "$DIRTY" ] || { echo "REFUSING: tracked changes in $DEV — the legs must read the committed tree:"; echo "$DIRTY"; exit 2; }
  TSHA="$(git -C "$DEV" rev-parse HEAD)"
}
case "$MODE" in
plan)
  REPO="${2:?repo}"; SHA="${3:?sha}"; BAD=0
  echo "c2 legs plan $(date -u +%Y-%m-%dT%H:%M:%SZ) | repo $REPO | sha $SHA (read-only: cat-file / show)"
  for P in Blockchain/Dev/scripts/preflight/lockfile-cleanroom.sh Blockchain/Dev/scripts/audit/audit-gate.mjs Blockchain/Dev/scripts/audit/audit-locks.mjs Blockchain/Dev/scripts/audit/package-lock.json; do
    git -C "$REPO" cat-file -e "$SHA:$P" > /dev/null 2>&1
    rc=$?
    echo "  $P at ${SHA:0:12}: $([ $rc -eq 0 ] && echo present || echo ABSENT) (cat-file rc $rc)"; [ $rc -eq 0 ] || BAD=1
  done
  git -C "$REPO" cat-file -e "$SHA:Blockchain/Dev/scripts/audit/no-such-file.mjs" > /dev/null 2>&1
  rc=$?
  echo "  CONTROL a path that does not exist: cat-file rc $rc (want non-zero)"; [ $rc -ne 0 ] || BAD=1
  for P in Blockchain/Dev/scripts/audit/audit-gate.mjs Blockchain/Dev/scripts/audit/audit-locks.mjs; do
    git -C "$REPO" show "$SHA:$P" > "/private/tmp/claude-501/.gd2_plan_$$.txt" 2>&1
    L="$(grep -n 'process.env.AUDIT_BASELINE_PATH' "/private/tmp/claude-501/.gd2_plan_$$.txt" | head -1)"; C="$(grep -c '^ *console.log(`\\nCLEANUP' "/private/tmp/claude-501/.gd2_plan_$$.txt")"
    echo "  $P reads AUDIT_BASELINE_PATH: ${L:-NOT FOUND} | CLEANUP printer lines: $C"; [ -n "$L" ] || BAD=1
  done
  git -C "$REPO" show "$SHA:Blockchain/Dev/scripts/audit/audit-baseline.json" > "/private/tmp/claude-501/.gd2_plan_$$.txt" 2>&1
  echo "  $RM in the baseline at ${SHA:0:12}: $(grep -c "\"$RM\"" "/private/tmp/claude-501/.gd2_plan_$$.txt") (head: want 0; base: 1)"
  mv "/private/tmp/claude-501/.gd2_plan_$$.txt" "/private/tmp/claude-501/.gd2_plan_last.txt"
  echo "PLAN $([ $BAD -eq 0 ] && echo OK || echo MISMATCH)"; exit $BAD ;;
parse-selftest)
  guard_out "${2:?outdir}"; F="$OUT/parse_plant.txt"
  printf '%s\n' 'audit-gate: 3 distinct advisories reported, 24 baselined.' '' 'CLEANUP (advisory): 2 baseline entries are no longer reported — remove:' \
    '  - GHSA-86w9-cpqp-85rv (node-forge, KS-1404)' '  - GHSA-2mjp-6q6p-2qxm (undici, KS-470)' 'FAIL — 1 NEW advisory not in the baseline:' \
    '  - GHSA-ch52-4w7c-c8xp [high] http-cache-semantics: planted title' '    https://github.com/advisories/GHSA-ch52-4w7c-c8xp' > "$F"
  NF="$(fails "$F" | tr '\n' ' ')"; NC="$(cleanups "$F" | tr '\n' ' ')"
  echo "c2 legs parse-selftest | planted $F | FAIL ids [${NF}] | CLEANUP ids [${NC}]"
  [ "$NF" = "GHSA-ch52-4w7c-c8xp " ] && [ "$NC" = "GHSA-2mjp-6q6p-2qxm GHSA-86w9-cpqp-85rv " ] && { echo "PARSE OK — FAIL rows and CLEANUP rows are told apart; the URL line counts as neither"; exit 0; }
  echo "PARSE MISMATCH"; exit 1 ;;
run)
  guard_dev "${2:?devdir}"; LABEL="${3:?label}"; guard_out "${4:?outdir}"
  echo "c2 legs run $LABEL $(date -u +%Y-%m-%dT%H:%M:%SZ) | tree HEAD $TSHA | node $(node -v) | npm $(npm -v) | outdir $OUT"
  npm --prefix "$DEV/scripts/audit" ci --ignore-scripts --no-audit --no-fund > "$OUT/install_audit.out" 2> "$OUT/install_audit.err"
  rc=$?
  echo "$rc" > "$OUT/install_audit.rc"; echo "  scripts/audit npm ci rc $rc"
  bash "$DEV/scripts/preflight/lockfile-cleanroom.sh" > "$OUT/leg2.out" 2> "$OUT/leg2.err"
  rc2=$?
  echo "$rc2" > "$OUT/leg2.rc"
  node "$DEV/scripts/audit/audit-gate.mjs" > "$OUT/leg6.out" 2> "$OUT/leg6.err"
  rc6=$?
  echo "$rc6" > "$OUT/leg6.rc"
  node "$DEV/scripts/audit/audit-locks.mjs" > "$OUT/leg7.out" 2> "$OUT/leg7.err"
  rc7=$?
  echo "$rc7" > "$OUT/leg7.rc"
  cat "$OUT/leg6.out" "$OUT/leg6.err" > "$OUT/leg6.all"; cat "$OUT/leg7.out" "$OUT/leg7.err" > "$OUT/leg7.all"
  fails "$OUT/leg6.all" > "$OUT/leg6.fail"; fails "$OUT/leg7.all" > "$OUT/leg7.fail"; cleanups "$OUT/leg6.all" > "$OUT/leg6.cleanup"; cleanups "$OUT/leg7.all" > "$OUT/leg7.cleanup"
  N="$(cat "$OUT/leg6.all" "$OUT/leg7.all" | grep -c "$RM")"
  echo "  leg 2 rc $rc2 $(class $rc2) | last: $(tail -1 "$OUT/leg2.out")"
  echo "  leg 6 rc $rc6 $(class $rc6) | FAIL rows: $(tr '\n' ' ' < "$OUT/leg6.fail") | CLEANUP rows $(wc -l < "$OUT/leg6.cleanup" | tr -d ' '): $(tr '\n' ' ' < "$OUT/leg6.cleanup")"
  echo "  leg 7 rc $rc7 $(class $rc7) | FAIL rows: $(tr '\n' ' ' < "$OUT/leg7.fail") | CLEANUP rows $(wc -l < "$OUT/leg7.cleanup" | tr -d ' '): $(tr '\n' ' ' < "$OUT/leg7.cleanup")"
  echo "  $RM mentioned anywhere in legs 6/7 output: $N (want 0)"
  BAD=0; [ $rc2 -eq 0 ] && [ $rc6 -eq 0 ] && [ $rc7 -eq 0 ] && [ "$N" = 0 ] || BAD=1
  echo "LEGS $LABEL: want 2/6/7 rc 0 0 0 and $RM named nowhere | got $rc2 $rc6 $rc7, $N mention(s) -> $([ $BAD -eq 0 ] && echo OK || echo MISMATCH)"; exit $BAD ;;
cleanup-control)
  guard_dev "${2:?devdir}"; guard_out "${3:?outdir}"; BB="${4:?base baseline json}"
  [ -s "$BB" ] && grep -q "\"$RM\"" "$BB" || { echo "REFUSING: $BB is empty or does not carry $RM (extract the BASE blob first)"; exit 2; }
  cp "$DEV/scripts/audit/audit-baseline.json" "$OUT/head_baseline_copy.json"
  echo "c2 legs cleanup-control $(date -u +%Y-%m-%dT%H:%M:%SZ) | tree HEAD $TSHA | base baseline $BB | outdir $OUT"
  BAD=0
  for V in base copy; do
    if [ "$V" = base ]; then F="$BB"; else F="$OUT/head_baseline_copy.json"; fi
    AUDIT_BASELINE_PATH="$F" node "$DEV/scripts/audit/audit-gate.mjs" > "$OUT/cc_${V}_leg6.out" 2> "$OUT/cc_${V}_leg6.err"
    r6=$?
    echo "$r6" > "$OUT/cc_${V}_leg6.rc"
    AUDIT_BASELINE_PATH="$F" node "$DEV/scripts/audit/audit-locks.mjs" > "$OUT/cc_${V}_leg7.out" 2> "$OUT/cc_${V}_leg7.err"
    r7=$?
    echo "$r7" > "$OUT/cc_${V}_leg7.rc"
    cat "$OUT/cc_${V}_leg6.out" "$OUT/cc_${V}_leg6.err" "$OUT/cc_${V}_leg7.out" "$OUT/cc_${V}_leg7.err" > "$OUT/cc_${V}.all"
    NC="$(cleanups "$OUT/cc_${V}.all" | grep -cx "$RM")"
    if [ "$V" = base ]; then
      [ "$NC" -ge 1 ] && W=OK || { W=MISMATCH; BAD=1; }
      echo "  MUST-HIT: head tree + BASE baseline: leg 6 rc $r6, leg 7 rc $r7 | $RM in a CLEANUP list ${NC}x (want >= 1): $W"
    else
      [ "$NC" = 0 ] && W=OK || { W=MISMATCH; BAD=1; }
      echo "  NO-OP: head tree + a COPY of the head baseline via the same variable: leg 6 rc $r6, leg 7 rc $r7 | $RM in CLEANUP ${NC}x (want 0): $W"
    fi
  done
  echo "CLEANUP-CONTROL $([ $BAD -eq 0 ] && echo OK || echo MISMATCH)"; exit $BAD ;;
*) usage; exit 2 ;;
esac
