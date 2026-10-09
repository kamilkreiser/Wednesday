#!/bin/bash
# Arms for friday/watch_status.sh (2026-10-03 upgrade: READY FOR GATE, STOPPED/NEEDS FRIDAY, --seed, WATCH_PANES).
# The case: three seats sat waiting on Friday unnoticed on 2026-10-03 (ledger row of that date).
# Runs the watcher from a temp copy beside a STUB seat_idle.sh (reads state_<pane> files), so no live pane is touched.
# 2026-10-04: A8-A12 = a SKELETON STATUS (READY line + template tokens) must not fire until filled; red at the 10-03 version.
# Red-proof: A1 and A4 return "leg expired" against the pre-upgrade watcher (checked by Friday 2026-10-03 19:2x).
set -u
SRC="${WATCH_STATUS_SRC:-$(cd "$(dirname "$0")/.." && pwd)/friday/watch_status.sh}"   # override to arm a candidate before install
T=$(mktemp -d); mkdir -p "$T/bin"; cp "$SRC" "$T/bin/watch_status.sh"
cat > "$T/bin/seat_idle.sh" <<'EOF'
#!/bin/bash
cat "$(dirname "$0")/state_$(echo "$1" | tr -d %)" 2>/dev/null || echo "UNKNOWN — stub"
EOF
W="$T/bin/watch_status.sh"; pass=0; fail=0
chk(){ if [ "$1" = "$2" ]; then pass=$((pass+1)); echo "PASS $3"; else fail=$((fail+1)); echo "FAIL $3 (got '$1' want '$2')"; fi; }
run(){ WATCH_LOOPS=2 WATCH_SLEEP=0 bash "$W" "$@" 2>&1 | tail -1; }
EXP="WAKE: watcher leg expired (55 "
d=$T/a1; mkdir -p $d; : > $d/seen; printf 'x\nREADY FOR GATE\n' > $d/X_STATUS.md
chk "$(run $d/seen "$d/*STATUS*" | cut -c1-7)" "WAKE: /" "A1 READY FOR GATE fires"
chk "$(run $d/seen "$d/*STATUS*" | cut -c1-30)" "$EXP" "A2 a seen READY does not re-fire"
d=$T/a3; mkdir -p $d; : > $d/seen; printf 'NOT READY FOR REVIEW yet\n' > $d/X_STATUS.md
chk "$(run $d/seen "$d/*STATUS*" | cut -c1-30)" "$EXP" "A3 NOT READY FOR REVIEW does not fire"
d=$T/a4; mkdir -p $d; : > $d/seen; printf 'STOPPED: NEEDS FRIDAY (S-1)\n' > $d/X_STATUS.md
chk "$(run $d/seen "$d/*STATUS*" | cut -c1-7)" "WAKE: /" "A4 STOPPED: NEEDS FRIDAY fires"
d=$T/a5; mkdir -p $d; : > $d/seen; printf 'READY FOR REVIEW\n' > $d/X_STATUS.md
chk "$(WATCH_LOOPS=2 WATCH_SLEEP=0 bash "$W" --seed $d/seen "$d/*STATUS*" | cut -c1-7)" "seeded:" "A5a --seed records and exits"
chk "$(run $d/seen "$d/*STATUS*" | cut -c1-30)" "$EXP" "A5b a seeded READY does not fire"
printf 'READY FOR REVIEW\n' >> $d/X_STATUS.md
chk "$(run $d/seen "$d/*STATUS*" | cut -c1-7)" "WAKE: /" "A5c a NEW READY after seeding fires"
d=$T/a6; mkdir -p $d; : > $d/seen; : > $d/X_STATUS.md
echo "BUSY — x" > "$T/bin/state_9"; ( sleep 1; echo "IDLE — turn ended" > "$T/bin/state_9" ) &
chk "$(WATCH_PANES='%9' WATCH_LOOPS=4 WATCH_SLEEP=1 bash "$W" $d/seen "$d/*STATUS*" | tail -1)" "WAKE: pane %9 went IDLE (was BUSY)" "A6 a pane going BUSY -> IDLE fires"
echo "IDLE — turn ended" > "$T/bin/state_8"
chk "$(WATCH_PANES='%8' WATCH_LOOPS=2 WATCH_SLEEP=0 bash "$W" $d/seen "$d/*STATUS*" | tail -1 | cut -c1-30)" "$EXP" "A7 a pane staying IDLE is quiet"
d=$T/a8; mkdir -p $d; : > $d/seen; printf 'READY FOR GATE\n## BLUF\n@@BODY@@\n' > $d/X_STATUS.md
chk "$(run $d/seen "$d/*STATUS*" | cut -c1-30)" "$EXP" "A8 skeleton @@BODY@@ with a READY line does not fire"
printf 'READY FOR GATE\n## BLUF\nGO WITH NOTES, all filled\n' > $d/X_STATUS.md
chk "$(run $d/seen "$d/*STATUS*" | cut -c1-7)" "WAKE: /" "A9 the same file once filled fires"
for tok in '__VERDICT__' 'CI_RESULT_PLACEHOLDER' 'CI-RUN2-LINE'; do
  d=$T/a10$tok; mkdir -p "$d"; : > "$d/seen"; printf 'READY FOR REVIEW\nci.sh: %s\n' "$tok" > "$d/X_STATUS.md"
  chk "$(run "$d/seen" "$d/*STATUS*" | cut -c1-30)" "$EXP" "A10 skeleton token $tok holds the READY"
done
d=$T/a11; mkdir -p $d; : > $d/seen; printf 'READY FOR REVIEW\nci.sh run 2 line green; the CI-run log; __init__ untouched; PRE-LINE prose\n' > $d/X_STATUS.md
chk "$(run $d/seen "$d/*STATUS*" | cut -c1-7)" "WAKE: /" "A11 ordinary prose near the tokens does not hold a real READY"
d=$T/a12; mkdir -p $d; : > $d/seen; printf 'STOPPED: NEEDS FRIDAY\n@@BODY@@\n' > $d/X_STATUS.md
chk "$(run $d/seen "$d/*STATUS*" | cut -c1-7)" "WAKE: /" "A12 a STOP in a skeleton still fires"
d=$T/a13; mkdir -p $d; : > $d/seen; printf 'READY FOR REVIEW\nE-01: all 217 question texts are PLACEHOLDER; census 217 -> 0\nKNOWN_PLACEHOLDER_ENTRIES kept\n' > $d/X_STATUS.md
chk "$(run $d/seen "$d/*STATUS*" | cut -c1-7)" "WAKE: /" "A13 real finished-STATUS prose (bare PLACEHOLDER, KNOWN_PLACEHOLDER_ENTRIES) does not hold"
# 2026-10-07: A14-A15 (they compare "WAKE: /" — a STATUS path — because the expiry line also starts "WAKE:", so a cut -c1-5 arm cannot fail) = a seat that REPLACES its single READY line (B174/B166/B92/B168, ~8 h unwoken). Red at the 10-06 version.
d=$T/a14; mkdir -p $d; : > $d/seen; printf '## Round 1\nfindings\nREADY FOR REVIEW\n' > $d/X_STATUS.md
chk "$(run $d/seen "$d/*STATUS*" | cut -c1-7)" "WAKE: /" "A14a first READY fires"
printf '## Round 1\nfindings\n## Round 2\nnew findings\nREADY FOR REVIEW\n' > $d/X_STATUS.md
chk "$(run $d/seen "$d/*STATUS*" | cut -c1-7)" "WAKE: /" "A14b the single READY REPLACED lower down (count still 1) fires"
d=$T/a15; mkdir -p $d; : > $d/seen; printf 'body\nREADY FOR REVIEW\n' > $d/X_STATUS.md
run $d/seen "$d/*STATUS*" >/dev/null; printf '## ADDENDUM-1 note appended below\n' >> $d/X_STATUS.md
chk "$(run $d/seen "$d/*STATUS*" | cut -c1-30)" "$EXP" "A15 text appended BELOW a seen READY stays quiet"
# 2026-10-10: A16-A17 = a seat's pointer line "READY FOR GATE / STOPPED line: see the end" (2x on 10-09) is neither a READY nor a STOP; the real line at the end still fires. A16 red at the 10-09 version.
d=$T/a16; mkdir -p $d; : > $d/seen; printf 'Result: READY FOR GATE / STOPPED line: see the end\nwork in progress\n' > $d/X_STATUS.md
chk "$(run $d/seen "$d/*STATUS*" | cut -c1-30)" "$EXP" "A16 a see-the-end pointer line stays quiet"
printf 'READY FOR GATE\n' >> $d/X_STATUS.md
chk "$(run $d/seen "$d/*STATUS*" | cut -c1-7)" "WAKE: /" "A17 the real READY at the end then fires"
wait; echo "pass=$pass fail=$fail"; [ "$fail" = 0 ]
