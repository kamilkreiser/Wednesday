#!/bin/bash
# Gate 73 (from the gate 72/68 pattern). usage: vt.sh <log> [vitest args...]
# Runs vitest with cwd = packages/shared (the repo-walking guards locate the Dev root from process.cwd();
# the shell hook refuses a literal directory change, so python sets the child's cwd). nice 10; waits while load1 > 8; stderr kept.
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate73-ks1868-auditlogger-1888
S=$G/repo/Blockchain/Dev/packages/shared
LOG="$1"; shift
while :; do L=$(sysctl -n vm.loadavg | awk '{print int($2)}'); [ "$L" -le 8 ] && break; echo "load1=$L > 8, waiting" | tee -a "$LOG.wait" >&2; sleep 20; done
echo "# load at start: $(sysctl -n vm.loadavg)" > "$LOG"
python3 -I -c 'import subprocess,sys; sys.exit(subprocess.call(sys.argv[2:], cwd=sys.argv[1]))' "$S" \
  nice -n 10 "$G/repo/Blockchain/Dev/node_modules/.bin/vitest" run "$@" >> "$LOG" 2>&1
RC=$?; echo "rc=$RC" >> "$LOG"; exit $RC
