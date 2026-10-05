#!/bin/bash
# c3_redfirst_gate64.sh — C3 RED-FIRST + TAMPER for #1389 (KS-1330), through the harness's OWN `RUNNER_SH` override, IN THE FOREGROUND.
#
# WHY THE FOREGROUND GUARD: a harness started as an asynchronous (`&`) job with job control off inherits SIGINT IGNORED. RULE 1 then
# refuses every INT handler, `sig_installable INT` says `no`, and both INT arms print UNREACHABLE — the INT cells silently vanish
# and the totals still look green (the builder's first red-first was exactly this). So this script:
#   (G1) probes ITS OWN shell first, the harness's way (install a trap, then look): INT not installable -> rc 4 INSTRUMENT, before any run;
#   (G2) after each run, requires the harness's own line `(signal environment: INT installable=yes, TERM installable=yes)`;
#   (G3) treats ANY `UNREACHABLE here, measured` line as an INSTRUMENT FAILURE (rc 4) — except in --tamper rule2, where EXACTLY ONE
#        (the SIGINT-to-pid arm) is the expected result.
# Modes (one per invocation; every output goes to <out>/<label>.{out,err,rc}):
#   --runner head      the head test file against the head runner (RUNNER_SH = <wt>/Blockchain/Dev/scripts/run-shell-suites.sh)
#   --runner develop   the SAME head test file against develop's runner (RUNNER_SH = --dev-runner <file>, develop's blob 85920863d704)
#   --tamper rule2     a COPY of the head test in <out>/ with the unconditional RULE-2 gate restored (asserted landed by content and sha),
#                      run against the head runner: the INT-pid arm must be UNREACHABLE and the total must drop by exactly 1
#   --tamper fgsuite   a COPY of the head RUNNER in <out>/ with the suite launched in the FOREGROUND again (no `&` / `wait`), so a
#                      trap is deferred until the slow fixture suite ends: the ITEM 2 latency cells must red while the interrupt cells
#                      (rc non-zero, 1 suite, no verdict, dir gone) can stay green — proves item 2 sees what item 1's cells cannot
# The worktree is never modified: the tamper lives in a copy under <out>. Prints `RESULT <label> rc=<n> passed=<p> failed=<f> unreachable=<u>`.
# Usage: c3_redfirst_gate64.sh --wt <worktree at the head> --out <dir> (--runner head | --runner develop --dev-runner <file> | --tamper rule2|fgsuite)
# rc 0 the run happened and the instrument is sound (the suite's own pass/fail is REPORTED, not judged) / 4 INSTRUMENT / 9 usage.
set -u
WT=""; OUT=""; MODE=""; DEVR=""
while [ $# -gt 0 ]; do
  case "$1" in
    --wt) WT="$2"; shift 2;; --out) OUT="$2"; shift 2;; --dev-runner) DEVR="$2"; shift 2;;
    --runner) MODE="runner-$2"; shift 2;; --tamper) MODE="tamper-$2"; shift 2;;
    *) echo "usage: see header"; exit 9;;
  esac
done
[ -n "$WT" ] && [ -n "$OUT" ] && [ -n "$MODE" ] || { echo "usage: --wt <dir> --out <dir> (--runner head|develop | --tamper rule2)"; exit 9; }
case "$(cd "$OUT" 2>/dev/null && pwd -P)" in /Volumes/DevMASTER/\!CODING/*) echo "REFUSED: --out is inside !CODING"; exit 9;; esac
TEST="$WT/Blockchain/Dev/scripts/__tests__/run_shell_suites.test.sh"; HR="$WT/Blockchain/Dev/scripts/run-shell-suites.sh"
[ -f "$TEST" ] && [ -f "$HR" ] || { echo "no test/runner under $WT"; exit 9; }
mkdir -p "$OUT"

# (G1) this shell's own SIGINT disposition, measured the harness's way
_t="$( ( trap 'x' INT 2>/dev/null; trap -p INT ) 2>/dev/null )"
if [ -z "$_t" ]; then
  echo "INSTRUMENT: SIGINT is IGNORED on entry to this shell (trap -p INT empty after installing) — the harness would report the INT arms"
  echo "UNREACHABLE. Run this script in the FOREGROUND of an ordinary shell (never with '&', never under a backgrounded wrapper)."
  exit 4
fi
echo "G1 this shell: INT installable (trap -p INT -> ${_t})"

case "$MODE" in
  runner-head)    LABEL=head_runner;    RUNNER="$HR";   F="$TEST"; WANT_UNR=0;;
  runner-develop) LABEL=develop_runner; RUNNER="$DEVR"; F="$TEST"; WANT_UNR=0
                  [ -f "$DEVR" ] || { echo "--dev-runner <file> required"; exit 9; };;
  tamper-rule2)   LABEL=tamper_rule2;   RUNNER="$HR";   F="$OUT/run_shell_suites.tamper_rule2.test.sh"; WANT_UNR=1
    python3 - "$TEST" "$F" <<'PY' || exit 4
import sys
src = open(sys.argv[1]).read()
new = '  if [ "$_s" = INT ] && [ "$INT_INSTALLABLE" != yes ]; then\n'
old = ('  if [ "$_s" = INT ] && [ "$_t" = pid ]; then\n'
       '    _skip="RULE 2: bash ignores SIGINT in a background job (trap -p INT empty there, rc 0), so no handler can exist to signal. A real terminal ^C hits the process GROUP — the arm below."\n'
       '  elif [ "$_s" = INT ] && [ "$INT_INSTALLABLE" != yes ]; then\n')
assert src.count(new) == 1, 'tamper anchor found %d times' % src.count(new)
out = src.replace(new, old); assert out != src and out.count(old) == 1
open(sys.argv[2], 'w').write(out)
PY
    echo "TAMPER landed: $(grep -c 'RULE 2: bash ignores SIGINT in a background job' "$F") restored RULE-2 gate line(s); sha256 head $(shasum -a 256 "$TEST" | cut -c1-16) vs tampered $(shasum -a 256 "$F" | cut -c1-16)"
    [ "$(shasum -a 256 "$TEST" | cut -c1-64)" != "$(shasum -a 256 "$F" | cut -c1-64)" ] || { echo "INSTRUMENT: tamper did not land"; exit 4; };;
  tamper-fgsuite)  LABEL=tamper_fgsuite; RUNNER="$OUT/run-shell-suites.tamper_fgsuite.sh"; F="$TEST"; WANT_UNR=0
    python3 - "$HR" "$RUNNER" <<'PY' || exit 4
import sys
src = open(sys.argv[1]).read()
new = ('  bash "$REPO_ROOT/$rel" > "$rss_suite_log" 2>&1 &\n  rss_suite_pid=$!\n  wait "$rss_suite_pid"\n  rss_rc=$?\n')
old = ('  bash "$REPO_ROOT/$rel" > "$rss_suite_log" 2>&1\n  rss_rc=$?\n')
assert src.count(new) == 1, 'tamper anchor found %d times' % src.count(new)
out = src.replace(new, old); assert out != src
open(sys.argv[2], 'w').write(out)
PY
    echo "TAMPER landed: async launch lines in the tampered runner $(grep -c 'rss_suite_pid=\$!' "$RUNNER") (head $(grep -c 'rss_suite_pid=\$!' "$HR")); sha256 head $(shasum -a 256 "$HR" | cut -c1-16) vs tampered $(shasum -a 256 "$RUNNER" | cut -c1-16)"
    [ "$(grep -c 'rss_suite_pid=\$!' "$RUNNER")" = 0 ] || { echo "INSTRUMENT: tamper did not land"; exit 4; };;
  *) echo "unknown mode $MODE"; exit 9;;
esac
echo "RUN $LABEL: bash $F with RUNNER_SH=$RUNNER (runner sha256 $(shasum -a 256 "$RUNNER" | cut -c1-16)) — FOREGROUND — $(date -u +%Y-%m-%dT%H:%M:%SZ)"
S=$(date +%s)
RUNNER_SH="$RUNNER" bash "$F" > "$OUT/$LABEL.out" 2> "$OUT/$LABEL.err"; rc=$?
echo "$rc" > "$OUT/$LABEL.rc"
E=$(( $(date +%s) - S ))
envl="$(grep -F '(signal environment:' "$OUT/$LABEL.out")"
unr="$(grep -c 'UNREACHABLE here, measured' "$OUT/$LABEL.out")"
sum="$(grep -E '^run_shell_suites: [0-9]+ passed, [0-9]+ failed$' "$OUT/$LABEL.out")"
p="$(printf '%s' "$sum" | awk '{print $2}')"; f="$(printf '%s' "$sum" | awk '{print $4}')"
oks="$(grep -c '^  ok   ' "$OUT/$LABEL.out")"; fails="$(grep -c '^  FAIL ' "$OUT/$LABEL.out")"
echo "  harness line: ${envl:-<ABSENT>}"
echo "  summary: ${sum:-<ABSENT>} | counted ok lines $oks, FAIL lines $fails | rc $rc | ${E}s"
grep '^  FAIL ' "$OUT/$LABEL.out" | cut -c1-220 | sed 's/^/    /'
grep 'UNREACHABLE here, measured' "$OUT/$LABEL.out" | cut -c1-160 | sed 's/^/    /'
grep -E 'KS-1330: SIG|KS-1302 R2: SIG' "$OUT/$LABEL.out" | cut -c1-200 | sed 's/^/    arm: /'
bad=0
[ "$envl" = "  (signal environment: INT installable=yes, TERM installable=yes)" ] || { echo "INSTRUMENT (G2): the harness did not report INT and TERM installable"; bad=1; }
[ "$unr" = "$WANT_UNR" ] || { echo "INSTRUMENT (G3): $unr UNREACHABLE line(s), expected $WANT_UNR in mode $MODE"; bad=1; }
[ -n "$sum" ] && [ "$p" = "$oks" ] && [ "$f" = "$fails" ] || { echo "INSTRUMENT: the summary line does not match the counted ok/FAIL lines"; bad=1; }
echo "RESULT $LABEL rc=$rc passed=${p:-?} failed=${f:-?} unreachable=$unr"
[ "$bad" = 0 ] || exit 4
exit 0
