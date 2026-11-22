#!/bin/bash
# QA-WIN-FOLLOWUP item 8: each WD/WF row of scripts/red-controls-daemon.sh, run as the runner selects it.
W=/private/tmp/claude-501/qwf; O=$W/logs/red; mkdir -p $O
grep -E '^\s*"COAGENT_RED_WD\|' $W/h/scripts/red-controls-daemon.sh | tr -d ' "' | while IFS='|' read -r var name pkg target test item; do
  log=$O/$item.log; log=${log//\//_}; log=$O/$(basename "$log")
  env "$var=$name" $W/run.sh $W/h h cargo test --locked -p "$pkg" --test "$target" -- --exact "$test" > "$log" 2>&1
  if grep -q "test result: FAILED" "$log" && grep -qF "test $test ... FAILED" "$log"; then r="RED: $(grep -m1 -A1 'panicked at' "$log" | tail -1 | cut -c1-260)"
  elif grep -q "test result: ok" "$log"; then r="STILL GREEN"; else r="ERROR"; fi
  echo "$item $name $test -> $r"
done
