#!/bin/bash
# Arms for friday/watch_status.sh (2026-10-03 upgrade: READY FOR GATE, STOPPED/NEEDS FRIDAY, --seed, WATCH_PANES).
# The case: three seats sat waiting on Friday unnoticed on 2026-10-03 (ledger row of that date).
# Runs the watcher from a temp copy beside a STUB seat_idle.sh (reads state_<pane> files), so no live pane is touched.
# Red-proof: A1 and A4 return "leg expired" against the pre-upgrade watcher (checked by Friday 2026-10-03 19:2x).
set -u
SRC="$(cd "$(dirname "$0")/.." && pwd)/friday/watch_status.sh"
T=$(mktemp -d); mkdir -p "$T/bin"; cp "$SRC" "$T/bin/"
cat > "$T/bin/seat_idle.sh" <<'EOF'
#!/bin/bash
cat "$(dirname "$0")/state_$(echo "$1" | tr -d %)" 2>/dev/null || echo "UNKNOWN — stub"
EOF
W="$T/bin/watch_status.sh"; pass=0; fail=0
chk(){ if [ "$1" = "$2" ]; then pass=$((pass+1)); echo "PASS $3"; else fail=$((fail+1)); echo "FAIL $3 (got '$1' want '$2')"; fi; }
run(){ WATCH_LOOPS=2 WATCH_SLEEP=0 bash "$W" "$@" 2>&1 | tail -1; }
EXP="WAKE: watcher leg expired (55 "
d=$T/a1; mkdir -p $d; : > $d/seen; printf 'x\nREADY FOR GATE\n' > $d/X_STATUS.md
chk "$(run $d/seen "$d/*STATUS*" | cut -c1-5)" "WAKE:" "A1 READY FOR GATE fires"
chk "$(run $d/seen "$d/*STATUS*" | cut -c1-30)" "$EXP" "A2 a seen READY does not re-fire"
d=$T/a3; mkdir -p $d; : > $d/seen; printf 'NOT READY FOR REVIEW yet\n' > $d/X_STATUS.md
chk "$(run $d/seen "$d/*STATUS*" | cut -c1-30)" "$EXP" "A3 NOT READY FOR REVIEW does not fire"
d=$T/a4; mkdir -p $d; : > $d/seen; printf 'STOPPED: NEEDS FRIDAY (S-1)\n' > $d/X_STATUS.md
chk "$(run $d/seen "$d/*STATUS*" | cut -c1-5)" "WAKE:" "A4 STOPPED: NEEDS FRIDAY fires"
d=$T/a5; mkdir -p $d; : > $d/seen; printf 'READY FOR REVIEW\n' > $d/X_STATUS.md
chk "$(WATCH_LOOPS=2 WATCH_SLEEP=0 bash "$W" --seed $d/seen "$d/*STATUS*" | cut -c1-7)" "seeded:" "A5a --seed records and exits"
chk "$(run $d/seen "$d/*STATUS*" | cut -c1-30)" "$EXP" "A5b a seeded READY does not fire"
printf 'READY FOR REVIEW\n' >> $d/X_STATUS.md
chk "$(run $d/seen "$d/*STATUS*" | cut -c1-5)" "WAKE:" "A5c a NEW READY after seeding fires"
d=$T/a6; mkdir -p $d; : > $d/seen; : > $d/X_STATUS.md
echo "BUSY — x" > "$T/bin/state_9"; ( sleep 1; echo "IDLE — turn ended" > "$T/bin/state_9" ) &
chk "$(WATCH_PANES='%9' WATCH_LOOPS=4 WATCH_SLEEP=1 bash "$W" $d/seen "$d/*STATUS*" | tail -1)" "WAKE: pane %9 went IDLE (was BUSY)" "A6 a pane going BUSY -> IDLE fires"
echo "IDLE — turn ended" > "$T/bin/state_8"
chk "$(WATCH_PANES='%8' WATCH_LOOPS=2 WATCH_SLEEP=0 bash "$W" $d/seen "$d/*STATUS*" | tail -1 | cut -c1-30)" "$EXP" "A7 a pane staying IDLE is quiet"
wait; echo "pass=$pass fail=$fail"; [ "$fail" = 0 ]
