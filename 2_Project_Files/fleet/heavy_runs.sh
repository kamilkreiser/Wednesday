#!/bin/bash
# heavy_runs.sh — count the machine's heavy CoAgent test JOBS (not processes).
#
# WHY (Friday ledger 2026-11-20, w=2): the count written into every build brief
# ("ps | grep -c <anchored script pattern>") reads one high for as long as a runner
# that re-executes itself in a child shell is going (the policy crate's runner shows
# as two lines for its whole run). Seats then wait for a slot that is free; on
# 2026-11-20 that held the one check the owner was waiting on for about 20 minutes.
#
# WHAT IT COUNTS: processes whose command line begins with one of the heavy scripts,
# MINUS those whose parent is itself such a process (a child shell of the same job).
#
# Usage:
#   heavy_runs.sh            -> prints one integer: the number of heavy jobs
#   heavy_runs.sh --list     -> one line per job: pid, elapsed, command (and the raw count on stderr)
#   heavy_runs.sh --selftest -> runs the counting function on fixed process tables; exit 0 = all arms pass
# Exit: 0 ok · 2 usage · 3 ps or the count failed (never prints a number it could not measure).
set -u
# Process command lines can hold bytes that are not valid text in the user's locale; awk then aborts
# ("towc: multibyte conversion failure") and an empty result would read as ZERO jobs (found live
# 2026-11-20 21:27). So: byte-wise locale, and an awk failure is a FAILURE, never a count.
export LC_ALL=C LANG=C
PATTERN='^(/bin/)?bash (scripts/(check\.sh|red-controls-[a-z-]+\.sh|test-daemon\.sh|test-p1p\.sh|windows/build\.sh)|crates/coagent-[a-z]+/red-controls\.sh)'

# stdin: lines "pid ppid etime command…"; stdout: the lines that are JOBS (parent not a match).
jobs_of() {
  /usr/bin/awk -v pat="$PATTERN" '
    { pid=$1; ppid=$2; et=$3; cmd=$0; sub(/^[ ]*[0-9]+[ ]+[0-9]+[ ]+[^ ]+[ ]+/, "", cmd)
      if (cmd ~ pat) { m[pid]=1; pp[pid]=ppid; e[pid]=et; c[pid]=cmd; order[++n]=pid } }
    END { for (i=1;i<=n;i++) { p=order[i]; if (!(pp[p] in m)) print p, e[p], c[p] } }'
}

selftest() {
  local fails=0 got
  # arm 1: empty table -> 0
  got=$(printf '' | jobs_of | /usr/bin/wc -l | /usr/bin/tr -d ' '); [ "$got" = 0 ] || { echo "FAIL arm1 empty: $got"; fails=1; }
  # arm 2: one plain job -> 1
  got=$(printf '10 1 01:00 bash scripts/check.sh\n' | jobs_of | /usr/bin/wc -l | /usr/bin/tr -d ' '); [ "$got" = 1 ] || { echo "FAIL arm2 one: $got"; fails=1; }
  # arm 3: runner + its child shell (same command line) -> 1
  got=$(printf '20 1 07:55 bash crates/coagent-policy/red-controls.sh\n21 20 00:05 bash crates/coagent-policy/red-controls.sh\n' | jobs_of | /usr/bin/wc -l | /usr/bin/tr -d ' '); [ "$got" = 1 ] || { echo "FAIL arm3 child: $got"; fails=1; }
  # arm 4: two separate jobs with the same command line (different parents) -> 2
  got=$(printf '30 1 10:00 bash scripts/check.sh\n31 5 02:00 bash scripts/check.sh\n' | jobs_of | /usr/bin/wc -l | /usr/bin/tr -d ' '); [ "$got" = 2 ] || { echo "FAIL arm4 two: $got"; fails=1; }
  # arm 5: look-alikes are not jobs (a grep of the pattern, an editor on the script, a waiting loop naming it) -> 0
  got=$(printf '40 1 00:01 grep -E bash scripts/check.sh\n41 1 00:01 vim scripts/check.sh\n42 1 00:09 bash -c until bash scripts/check.sh\n' | jobs_of | /usr/bin/wc -l | /usr/bin/tr -d ' '); [ "$got" = 0 ] || { echo "FAIL arm5 lookalikes: $got"; fails=1; }
  # arm 6: mixed: 3 jobs + 1 child -> 3
  got=$(printf '50 1 60:00 bash scripts/check.sh\n51 1 26:00 /bin/bash scripts/test-daemon.sh 3\n52 1 07:00 bash crates/coagent-policy/red-controls.sh\n53 52 00:02 bash crates/coagent-policy/red-controls.sh\n' | jobs_of | /usr/bin/wc -l | /usr/bin/tr -d ' '); [ "$got" = 3 ] || { echo "FAIL arm6 mixed: $got"; fails=1; }
  # arm 7: the Windows kit build is a job -> 1
  got=$(printf '60 1 03:00 bash scripts/windows/build.sh\n' | jobs_of | /usr/bin/wc -l | /usr/bin/tr -d ' '); [ "$got" = 1 ] || { echo "FAIL arm7 windows build: $got"; fails=1; }
  # arm 8: a process line holding bytes that are not valid text must not break the count -> 2
  got=$(printf '70 1 01:00 bash scripts/check.sh\n71 1 00:10 someprog \377\376\200bad\n72 1 00:20 bash scripts/test-daemon.sh 3\n' | jobs_of | /usr/bin/wc -l | /usr/bin/tr -d ' '); [ "$got" = 2 ] || { echo "FAIL arm8 invalid bytes: $got"; fails=1; }
  [ "$fails" = 0 ] && { echo "heavy_runs selftest: 8 arms pass"; return 0; }
  return 1
}

case "${1:-}" in
  --selftest) selftest; exit $? ;;
  ""|--list) ;;
  *) echo "usage: heavy_runs.sh [--list|--selftest]" >&2; exit 2 ;;
esac

table="$(/bin/ps -ax -o pid=,ppid=,etime=,command= 2>&1)" || { echo "heavy_runs: ps failed: $table" >&2; exit 3; }
jobs="$(set -o pipefail; printf '%s\n' "$table" | jobs_of)"; jrc=$?
if [ "$jrc" != 0 ]; then
  echo "heavy_runs: the count FAILED (rc=$jrc); treat the machine as FULL and count again in 2 minutes" >&2
  exit 3
fi
if [ -z "$jobs" ]; then n=0; else n=$(printf '%s\n' "$jobs" | /usr/bin/wc -l | /usr/bin/tr -d ' '); fi
if [ "${1:-}" = "--list" ]; then
  [ -n "$jobs" ] && printf '%s\n' "$jobs"
  raw=$(printf '%s\n' "$table" | /usr/bin/awk -v pat="$PATTERN" '{cmd=$0; sub(/^[ ]*[0-9]+[ ]+[0-9]+[ ]+[^ ]+[ ]+/, "", cmd); if (cmd ~ pat) k++} END{print k+0}')
  echo "heavy_runs: jobs=$n raw_lines=$raw" >&2
else
  echo "$n"
fi
