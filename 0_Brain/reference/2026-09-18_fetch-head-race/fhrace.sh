#!/bin/bash
# Reproduce the FETCH_HEAD race in a THROWAWAY repo under the scratchpad only.
set -u
S=/private/tmp/claude-501/-Volumes-KK-T9-External-HDD-TUESDAY/d7051c54-99ee-441b-bb2e-de27a27c710a/scratchpad/fhrace
case "$S" in /private/tmp/claude-501/*/scratchpad/*) ;; *) echo "REFUSED: not scratchpad"; exit 9;; esac
mkdir -p "$S"; [ -d "$S/origin.git" ] || {
  git init -q --bare -b main "$S/origin.git"
  git clone -q "$S/origin.git" "$S/seed" 2>/dev/null
  git -C "$S/seed" -c user.email=t@t -c user.name=t commit -q --allow-empty -m init
  git -C "$S/seed" push -q origin main
  for b in a b c d e f g h; do git -C "$S/seed" push -q origin main:refs/heads/br-$b; done
  git clone -q "$S/origin.git" "$S/work"
}
MODE="${1:-plain}"   # plain = panel_sync's current `git fetch -q origin`; nowrite = with --no-write-fetch-head
N="${2:-150}"
( end=$((SECONDS+40)); while [ $SECONDS -lt $end ]; do
    if [ "$MODE" = nowrite ]; then git -C "$S/work" fetch -q --no-write-fetch-head origin; elif [ "$MODE" = pull ]; then git -C "$S/work" pull --rebase -q >/dev/null 2>&1; else git -C "$S/work" fetch -q origin; fi
  done ) &
BG=$!
fail=0; race=0
for i in $(seq 1 "$N"); do
  out=$(git -C "$S/work" pull --rebase -q 2>&1); rc=$?
  if [ $rc -ne 0 ]; then fail=$((fail+1)); case "$out" in *"multiple branches"*) race=$((race+1));; esac; fi
done
kill $BG 2>/dev/null; wait $BG 2>/dev/null
echo "MODE=$MODE pulls=$N failed=$fail multiple-branches=$race"
