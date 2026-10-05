#!/bin/bash
# c3_wholerunner_gate64.sh — the WHOLE runner for #1389 (KS-1330) from its REAL path inside a checkout (cwd matters: the runner resolves
# REPO_ROOT and its ROOTS from its own location), IN THE FOREGROUND, totals only plus three readings the totals hide:
#   (W1) the tally line `shell suites: P passed, F failed, S skipped (of N)` — and N == an INDEPENDENT count of the runner's glob
#        (`<root>/*.test.sh` on disk under each ROOT read from the runner itself), so "of 67" is not taken from the runner alone;
#   (W2) inside the run, the run_shell_suites.test.sh section's OWN `(signal environment: …)` line and its UNREACHABLE lines.
#        Under the head runner every suite is launched ASYNC with job control off, so SIGINT is ignored on entry to that suite
#        (RULE 1): its INT arms are EXPECTED to read UNREACHABLE inside the runner (and inside pre-push leg 14). This is reported,
#        not judged — it is the coupling the gate rules on (does "the SIGINT-to-pid arm can now run" hold only for a DIRECT run?);
#   (W3) this shell's own INT disposition (G1 as in c3_redfirst): refuses rc 4 if ignored, because a backgrounded whole run would
#        also change what develop's FOREGROUND-pipeline runner hands its suites, and the before/after would compare two environments.
# Usage: c3_wholerunner_gate64.sh --wt <checkout/worktree at the rev under test> --out <dir> --label <name>
# rc 0 the run happened (its pass/fail REPORTED) / 4 INSTRUMENT (G1; no tally line; N != the independent count) / 9 usage.
set -u
WT=""; OUT=""; LABEL=""
while [ $# -gt 0 ]; do case "$1" in --wt) WT="$2"; shift 2;; --out) OUT="$2"; shift 2;; --label) LABEL="$2"; shift 2;; *) echo usage; exit 9;; esac; done
[ -n "$WT" ] && [ -n "$OUT" ] && [ -n "$LABEL" ] || { echo "usage: --wt <dir> --out <dir> --label <name>"; exit 9; }
mkdir -p "$OUT"
case "$(cd "$OUT" && pwd -P)" in /Volumes/DevMASTER/\!CODING/*) echo "REFUSED: --out is inside !CODING"; exit 9;; esac
case "$(cd "$WT" && pwd -P)" in /Volumes/DevMASTER/\!CODING/*) echo "REFUSED: --wt is inside !CODING (run in YOUR OWN worktree)"; exit 9;; esac
R="$WT/Blockchain/Dev/scripts/run-shell-suites.sh"; [ -f "$R" ] || { echo "no runner at $R"; exit 9; }
_t="$( ( trap 'x' INT 2>/dev/null; trap -p INT ) 2>/dev/null )"
[ -n "$_t" ] || { echo "INSTRUMENT: SIGINT is IGNORED on entry to this shell — run in the FOREGROUND"; exit 4; }
REV="$(git -C "$WT" rev-parse HEAD 2>/dev/null)"; TREE="$(git -C "$WT" rev-parse 'HEAD^{tree}' 2>/dev/null)"
DIRTY="$(git -C "$WT" status --porcelain 2>/dev/null | wc -l | tr -d ' ')"
N=0
for root in $(sed -n '/^ROOTS=(/,/^)/p' "$R" | grep -oE '"[^"]+"' | tr -d '"'); do
  for f in "$WT/$root"/*.test.sh; do [ -e "$f" ] && N=$((N + 1)); done
done
echo "RUN $LABEL: cd $WT/Blockchain/Dev && bash scripts/run-shell-suites.sh | rev $REV tree $TREE | worktree dirty lines $DIRTY | runner sha256 $(shasum -a 256 "$R" | cut -c1-16) | independent glob count $N | $(date -u +%Y-%m-%dT%H:%M:%SZ) | $(/bin/bash --version | head -1)"
S=$(date +%s)
( cd "$WT/Blockchain/Dev" && bash scripts/run-shell-suites.sh ) > "$OUT/$LABEL.out" 2> "$OUT/$LABEL.err"; rc=$?
echo "$rc" > "$OUT/$LABEL.rc"
E=$(( $(date +%s) - S ))
tally="$(grep -E '^shell suites: [0-9]+ passed, [0-9]+ failed, [0-9]+ skipped \(of [0-9]+\)$' "$OUT/$LABEL.out")"
echo "  W1 tally: ${tally:-<ABSENT>} | rc $rc | ${E}s"
grep -E '^(FAILED|SKIPPED):' "$OUT/$LABEL.out" | sed 's/^/     /'
sec="$(awk '/^=== .*run_shell_suites\.test\.sh ===$/{on=1} on&&/^=== / && !/run_shell_suites/{on=0} on' "$OUT/$LABEL.out")"
echo "  W2 run_shell_suites section: $(printf '%s\n' "$sec" | grep -F '(signal environment:' | sed 's/^ *//') | UNREACHABLE lines $(printf '%s\n' "$sec" | grep -c 'UNREACHABLE here, measured') | its summary: $(printf '%s\n' "$sec" | grep -E '^run_shell_suites: ')"
printf '%s\n' "$sec" | grep 'UNREACHABLE here, measured' | cut -c1-120 | sed 's/^/     /'
bad=0
[ -n "$tally" ] || { echo "INSTRUMENT: no tally line"; bad=1; }
of="$(printf '%s' "$tally" | sed -n 's/.*(of \([0-9]*\))$/\1/p')"
[ "$of" = "$N" ] || { echo "INSTRUMENT: the runner's (of $of) != the independent glob count $N"; bad=1; }
echo "RESULT $LABEL rc=$rc ${tally:-no-tally} independent=$N"
[ "$bad" = 0 ] || exit 4
exit 0
