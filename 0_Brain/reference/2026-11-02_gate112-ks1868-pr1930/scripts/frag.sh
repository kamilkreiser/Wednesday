#!/bin/bash
G=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate112-ks1868-pr1930
R=$G/repo; F="$R/Projects Documents/fragments"
N=KS-1868-security-admin-scopes-save-audit-validate-and-db-unreadable-thrown-value.html
sha(){ shasum -a 256 "$1" | awk '{print $1}'; }
chk(){ nice -n 10 node $R/Blockchain/Dev/scripts/docs-fragments.mjs check --root $R > "$1" 2>&1; echo "rc=$?" >> "$1"; }
chk $G/logs/frag_check_clean.log
for k in flow cheat; do
  f="$F/$k/$N"; h=$(sha "$f"); cp "$f" $G/logs/frag_orig_$k.html
  printf '\n<div>planted unclosed</div><div>\n' >> "$f"
  chk $G/logs/frag_check_planted_${k}_div.log
  cp $G/logs/frag_orig_$k.html "$f"; [ "$(sha "$f")" = "$h" ] && echo "$k div restore OK" || echo "$k div RESTORE FAIL"
  if [ $k = flow ]; then sed 's/<h2><!--n-->\. /<h2>/' $G/logs/frag_orig_flow.html > "$f"; else sed 's#</table>#</tabl>#' $G/logs/frag_orig_cheat.html > "$f"; fi
  chk $G/logs/frag_check_planted_${k}_2.log
  cp $G/logs/frag_orig_$k.html "$f"; [ "$(sha "$f")" = "$h" ] && echo "$k d2 restore OK" || echo "$k d2 RESTORE FAIL"
done
chk $G/logs/frag_check_after_restore.log
for l in clean planted_flow_div planted_flow_2 planted_cheat_div planted_cheat_2 after_restore; do echo "== $l"; tail -4 $G/logs/frag_check_$l.log; done
git -C /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate112-ks1868-pr1930/repo status --short
