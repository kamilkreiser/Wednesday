#!/bin/bash
# doctor_pause_queue_arms.sh — arms for doctor.sh's PAUSE_QUEUE-expired check (2026-09-20).
# The check must WARN on an expired pause, stay QUIET on a live one, WARN on a pause with no
# epoch, and stay quiet with no file. Clock moved via DOCTOR_NOW_EPOCH; file via NIGHT_PAUSE_FILE.
# Negative control: the pre-fix doctor (doctor.sh.pre-0920-pausequeue) must NOT warn on the expired case.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; DOC="$HERE/../doctor.sh"; OLD="$HERE/../doctor.sh.pre-0920-pausequeue"
T="/private/tmp/claude-501/doctor_pause_queue_arms.$$"; mkdir -p "$T"; PASS=0; FAIL=0
run() { NIGHT_PAUSE_FILE="$2" DOCTOR_NOW_EPOCH="$3" bash "$1" --quiet 2>&1 | /usr/bin/grep -i -c 'PAUSE_QUEUE' ; }
arm() { local name="$1" want="$2" got="$3"; if [ "$got" = "$want" ]; then PASS=$((PASS+1)); echo "PASS $name (hits=$got)"; else FAIL=$((FAIL+1)); echo "FAIL $name (want $want got $got)"; fi; }
NOW=1789911720   # 2026-09-20 23:42 AEST
printf '%s\nreason line\n' 1789911000 > "$T/expired"    # 12 min before NOW
printf '%s\nreason line\n' 1789913803 > "$T/live"       # 00:16, after NOW
printf '%s\n' "Wednesday 2026-09-20 23:31 no epoch here" > "$T/noepoch"
arm "A1 expired pause WARNS"            1 "$(run "$DOC" "$T/expired" $NOW)"
arm "A2 live pause is quiet"            0 "$(run "$DOC" "$T/live" $NOW)"
arm "A3 no-epoch pause WARNS"           1 "$(run "$DOC" "$T/noepoch" $NOW)"
arm "A4 no file is quiet"               0 "$(run "$DOC" "$T/absent" $NOW)"
arm "A5 NEGATIVE CONTROL: old doctor silent on expired" 0 "$(run "$OLD" "$T/expired" $NOW)"
arm "A6 warn text carries the minutes"  1 "$(NIGHT_PAUSE_FILE="$T/expired" DOCTOR_NOW_EPOCH=$NOW bash "$DOC" --quiet 2>&1 | /usr/bin/grep -c 'EXPIRED 12 min')"
echo "scratch left at $T (session scratch; no rm from a script)"; echo "arms: $PASS pass / $FAIL fail"; [ "$FAIL" = 0 ]
