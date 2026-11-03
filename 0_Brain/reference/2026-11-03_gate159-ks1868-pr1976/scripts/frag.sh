#!/bin/bash
# docs-fragments check over wt2_c1 (fragments are byte-identical at c1 and head: commit 2 touches only a test file),
# plus a planted unclosed <div> in each PR fragment (flow, cheat separately) with sha-verified restore.
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate159-ks1868-pr1976
T=$W/wt2_c1
S=$T/Blockchain/Dev/scripts/docs-fragments.mjs
for k in flow cheat; do
  a=$(git -C "$W/repo" rev-parse "bdc1d4d8:Projects Documents/fragments/$k/KS-1868-anchoring-reconciler-index.html")
  b=$(git -C "$W/repo" rev-parse "dba3a90a:Projects Documents/fragments/$k/KS-1868-anchoring-reconciler-index.html")
  echo "$k fragment c1==head blob: $([ "$a" = "$b" ] && echo yes || echo no)"
done
( cd "$T" && node "$S" check --root "$T" ) > "$W/logs/frag_check.log" 2>&1; echo "rc=$?" >> "$W/logs/frag_check.log"
echo "clean check: $(tail -1 "$W/logs/frag_check.log")"; grep -i -E 'ok|fail|advisory|new' "$W/logs/frag_check.log" | head -8
for k in flow cheat; do
  F="$T/Projects Documents/fragments/$k/KS-1868-anchoring-reconciler-index.html"
  before=$(shasum -a 256 "$F" | cut -d' ' -f1)
  cp "$F" "$W/logs/_pc/frag_$k.orig"
  printf '<div class="gate159-plant">\n' >> "$F"
  ( cd "$T" && node "$S" check --root "$T" ) > "$W/logs/frag_plant_$k.log" 2>&1; echo "rc=$?" >> "$W/logs/frag_plant_$k.log"
  cp "$W/logs/_pc/frag_$k.orig" "$F"
  after=$(shasum -a 256 "$F" | cut -d' ' -f1)
  echo "plant $k: $(tail -1 "$W/logs/frag_plant_$k.log") ; restore sha ok: $([ "$before" = "$after" ] && echo yes || echo NO)"
  grep -i -E 'fail|unclosed|balance' "$W/logs/frag_plant_$k.log" | head -3
done
git -C "$T" status --short | grep -v node_modules | grep -v 'packages/shared/dist'
