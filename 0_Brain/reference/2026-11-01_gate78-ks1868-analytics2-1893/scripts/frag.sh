#!/bin/bash
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate78-ks1868-analytics2-1893
R=$G/repo; F="$R/Projects Documents/fragments"
N=KS-1868-analytics-db-save-catches-unreadable-thrown-value.html
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
chk(){ nice -n 10 node $R/Blockchain/Dev/scripts/docs-fragments.mjs check --root $R > "$1" 2>&1; echo "rc=$?" >> "$1"; }
chk $G/logs/frag_check_clean.log
for k in flow cheat; do
  f="$F/$k/$N"; h=$(sha "$f"); cp "$f" $G/logs/frag_orig_$k.html
  printf '\n<div>planted unclosed</div><div>\n' >> "$f"
  chk $G/logs/frag_check_planted_${k}_div.log
  cp $G/logs/frag_orig_$k.html "$f"; [ "$(sha "$f")" = "$h" ] && echo "$k div restore OK" || echo "$k div RESTORE FAIL"
  # defect 2: remove the number token (flow) / break a table
  if [ $k = flow ]; then sed 's/<!--n-->\. analytics/analytics/' $G/logs/frag_orig_flow.html > "$f"; else sed 's#</table>#</tabl>#' $G/logs/frag_orig_cheat.html > "$f"; fi
  chk $G/logs/frag_check_planted_${k}_2.log
  cp $G/logs/frag_orig_$k.html "$f"; [ "$(sha "$f")" = "$h" ] && echo "$k d2 restore OK" || echo "$k d2 RESTORE FAIL"
done
chk $G/logs/frag_check_after_restore.log
git -C $R status --short
