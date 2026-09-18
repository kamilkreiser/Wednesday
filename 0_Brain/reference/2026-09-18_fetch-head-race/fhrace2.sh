#!/bin/bash
set -u
S=/private/tmp/claude-501/-Volumes-KK-T9-External-HDD-TUESDAY/d7051c54-99ee-441b-bb2e-de27a27c710a/scratchpad/fhrace
W="$S/work"
sync_fixed(){ git -C "$W" fetch -q --no-write-fetch-head origin main && git -C "$W" rebase -q --autostash origin/main; }
( end=$((SECONDS+40)); while [ $SECONDS -lt $end ]; do sync_fixed >/dev/null 2>&1; done ) &
BG=$!
fail=0; race=0; other=""
for i in $(seq 1 150); do
  out=$(sync_fixed 2>&1); rc=$?
  if [ $rc -ne 0 ]; then fail=$((fail+1)); case "$out" in *"multiple branches"*) race=$((race+1));; *) other="$out";; esac; fi
done
kill $BG 2>/dev/null; wait $BG 2>/dev/null
echo "FIXED-PATTERN both loops: syncs=150 failed=$fail multiple-branches=$race"
[ -n "$other" ] && echo "last other failure: $(printf '%s' "$other" | head -2)"
