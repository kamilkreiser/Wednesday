#!/bin/bash
# QA-ALLOW-MEASURE item 5: extract count_run() verbatim from the committed am.sh and run it against fake runs files
# of 15 and 16 lines (claude --version is shadowed by a function so no Claude Code process starts).
AM="$1"; W="$2"; mkdir -p "$W"
eval "$(awk '/^count_run\(\) \{/,/^\}/' "$AM")"
claude() { echo "0.0.0-fake (QA shim)"; }
MODEL=fake; eval "$(grep -E "^CEIL=[0-9]+$" "$AM")"; echo "CEIL from am.sh: $CEIL"
for n in 15 16; do RUNS="$W/runs.$n"; : > "$RUNS"; for i in $(seq 1 $n); do echo "x run=$i" >> "$RUNS"; done
  ( count_run QA-test headless ); echo "with $n lines: exit=$? lines-after=$(grep -c . "$RUNS")"; done
