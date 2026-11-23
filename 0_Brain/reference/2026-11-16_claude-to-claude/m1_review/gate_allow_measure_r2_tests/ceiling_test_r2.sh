#!/bin/bash
# QA-ALLOW-MEASURE-R2 item 7: count_run() extracted VERBATIM from the committed am.sh at the head (CEIL read from it),
# run against fake counters of 19 and 20 lines; `claude` is a shell function, so no Claude Code process can start.
AM="$1"; W="$2"; mkdir -p "$W"
eval "$(awk '/^count_run\(\) \{/,/^\}/' "$AM")"
claude() { echo "0.0.0-fake (QA shim)"; }
MODEL=fake; eval "$(grep -E "^CEIL=[0-9]+" "$AM" | sed 's/ *#.*//')"; echo "CEIL from am.sh: $CEIL"
for n in 19 20; do RUNS="$W/runs.$n"; : > "$RUNS"; for i in $(seq 1 $n); do echo "x run=$i" >> "$RUNS"; done
  ( count_run QA-test headless ); echo "with $n lines: exit=$? lines-after=$(grep -c . "$RUNS")"; done
